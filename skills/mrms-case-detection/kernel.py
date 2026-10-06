"""Helpers for MRMS-driven radar case detection.

Every function here encodes something that cost a debugging cycle to find.
The MRMS readers handle the 0-360 longitude and negative-fill conventions;
the shear and morphology helpers handle the masked-array and NaN-propagation
traps documented in SKILL.md.
"""
import os

MRMS_BUCKET = "noaa-mrms-pds"
MRMS_QPE_1H = "CONUS/MultiSensor_QPE_01H_Pass2_00.00"
MRMS_FILL_FLOOR = 0.0
EARTH_R_KM = 6371.0088
ARMLIVE_QUERY = "https://adc.arm.gov/armlive/livedata/query"
ARMLIVE_SAVE = "https://adc.arm.gov/armlive/livedata/saveData"
MPING_REPORTS = "https://mping.ou.edu/mping/api/v2/reports"
BNF_CSAPR2 = (34.63080597, -87.13311768, 180.0)


def s3_anon():
    """Anonymous S3 client for the NOAA open-data buckets."""
    import boto3
    from botocore import UNSIGNED
    from botocore.config import Config
    return boto3.client("s3", config=Config(signature_version=UNSIGNED))


def great_circle_km(lat, lon, ref_lat, ref_lon):
    """Great-circle range (km) and bearing (deg) from a reference point."""
    import numpy as np
    lat = np.asarray(lat, float)
    lon = np.asarray(lon, float)
    p1 = np.radians(ref_lat)
    p2 = np.radians(lat)
    dl = np.radians(lon - ref_lon)
    cosd = np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl)
    d = EARTH_R_KM * np.arccos(np.clip(cosd, -1, 1))
    y = np.sin(dl) * np.cos(p2)
    x = np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl)
    return d, (np.degrees(np.arctan2(y, x)) % 360)


def mrms_list_day(day, product=None, client=None):
    """S3 keys for one UTC day. `day` is 'YYYYMMDD'. MRMS 1-h QPE is HOURLY."""
    if product is None:
        product = MRMS_QPE_1H
    if client is None:
        client = s3_anon()
    r = client.list_objects_v2(Bucket=MRMS_BUCKET, Prefix=product + "/" + day + "/")
    return sorted(k["Key"] for k in r.get("Contents", []))


def mrms_fetch(keys, outdir, client=None, workers=8):
    """Download and gunzip MRMS grib2 keys. Returns local paths."""
    import gzip
    import concurrent.futures as cf
    if client is None:
        client = s3_anon()
    os.makedirs(outdir, exist_ok=True)

    def one(key):
        out = os.path.join(outdir, os.path.basename(key)[:-3])
        if os.path.exists(out) and os.path.getsize(out) > 0:
            return out
        body = client.get_object(Bucket=MRMS_BUCKET, Key=key)["Body"].read()
        with open(out, "wb") as fh:
            fh.write(gzip.decompress(body))
        return out

    with cf.ThreadPoolExecutor(workers) as ex:
        return list(ex.map(one, keys))


def mrms_grid_index(path, ref_lat, ref_lon, radius_km=120.0, pad_deg=1.4):
    """Row/col slices and a range mask for a site-centred subset of the MRMS grid.

    Handles the two grid conventions that bite: latitude DESCENDS, and longitude
    is stored 0-360 (230-300 E for CONUS) so it needs -360 to compare with a
    negative site longitude.
    """
    import numpy as np
    import xarray as xr
    ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
    lat_g = ds.latitude.values
    lon_g = ds.longitude.values - 360.0
    ds.close()
    i0 = int(np.searchsorted(-lat_g, -(ref_lat + pad_deg)))
    i1 = int(np.searchsorted(-lat_g, -(ref_lat - pad_deg)))
    j0 = int(np.searchsorted(lon_g, ref_lon - pad_deg * 1.25))
    j1 = int(np.searchsorted(lon_g, ref_lon + pad_deg * 1.25))
    sub_lat = lat_g[i0:i1]
    sub_lon = lon_g[j0:j1]
    lon2, lat2 = np.meshgrid(sub_lon, sub_lat)
    rng, _ = great_circle_km(lat2, lon2, ref_lat, ref_lon)
    return dict(rows=(i0, i1), cols=(j0, j1), lat=sub_lat, lon=sub_lon,
                mask=(rng <= radius_km), range_km=rng)


def mrms_read_subset(path, idx):
    """(valid_time, 2-D mm array) for one MRMS file over the subset in `idx`.

    The GRIB variable is named 'unknown' (MRMS ships no standard name), and
    negative values are fill codes (-1 no coverage, -3 missing) that MUST become
    NaN before any statistic -- otherwise means and maxima are silently wrong.
    """
    import numpy as np
    import pandas as pd
    import xarray as xr
    ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
    i0, i1 = idx["rows"]
    j0, j1 = idx["cols"]
    var = "unknown" if "unknown" in ds.data_vars else list(ds.data_vars)[0]
    a = ds[var].values[i0:i1, j0:j1].astype("float32")
    t = pd.Timestamp(ds.valid_time.values)
    ds.close()
    a[a < MRMS_FILL_FLOOR] = np.nan
    return t, a


def mrms_hour_ending(when):
    """The hour-ending stamp whose MRMS 1-h accumulation covers `when`.

    MRMS 1-h QPE is hour-ENDING: the 04:00Z grid covers 03:00-04:00Z. Pairing a
    radar frame with the wrong stamp makes a raining frame look dry.
    """
    import pandas as pd
    return pd.Timestamp(when).floor("h") + pd.Timedelta("1h")


def armlive_files(datastream, start, end, user=None, token=None, day=None):
    """ARM Live file list. Pass `day`='YYYYMMDD' to filter by the date IN THE
    FILENAME -- the query range spans into the end date, so a bare 'start to
    start+1' request returns two days of files and inflates any count."""
    import json
    import urllib.request
    if user is None:
        user = os.environ.get("ARMUSER", "")
    if token is None:
        token = os.environ.get("ARMTOKEN", "")
    url = (ARMLIVE_QUERY + "?user=" + user + ":" + token + "&ds=" + datastream
           + "&start=" + start + "&end=" + end + "&wt=json")
    with urllib.request.urlopen(url, timeout=120) as r:
        files = [f for f in json.load(r).get("files", []) if ".a1." in f]
    if day is not None:
        files = [f for f in files if f.split(".a1.")[1][:8] == day]
    return sorted(files)


def armlive_window(files, day, hour0, hour1):
    """Files whose timestamp falls in [hour0, hour1] UTC on `day`.

    Report event coverage with this, never a whole-day total -- the two differ
    by ~3x on a typical event and the day figure overstates what observed it.
    """
    return sorted(f for f in files
                  if f.split(".a1.")[1][:8] == day
                  and hour0 <= int(f.split(".a1.")[1][9:11]) <= hour1)


def armlive_size(filename, user=None, token=None):
    """Remote byte size via HEAD -- the cheap scan-type discriminator.

    For the interleaved bnfcsapr2cfr stream an RHI is ~18 MB and a PPI volume
    ~730 MB, so this tells you what a file is before spending 5 minutes on it.
    """
    import urllib.request
    if user is None:
        user = os.environ.get("ARMUSER", "")
    if token is None:
        token = os.environ.get("ARMTOKEN", "")
    url = ARMLIVE_SAVE + "?user=" + user + ":" + token + "&file=" + filename
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=120) as r:
        return int(r.headers.get("Content-Length", 0))


def armlive_fetch(filename, outdir, user=None, token=None, keep_partial=True):
    """Download one ARM Live file and VALIDATE it. Returns the path, or raises.

    Validation is not optional, and MAGIC BYTES ARE NOT ENOUGH. A stalled
    transfer writes a valid HDF5 *header* and then stops: the file passes a
    magic-byte check, passes a "looks like netCDF" eyeball, and fails only when
    something reads deep into it. One such 78 MB fragment of a 720 MB volume got
    through a magic-only gate and was caught later by netCDF4 raising
    "HDF error" on open. Three checks, cheapest first:

      1. magic bytes           -- catches an HTML error body
      2. size vs Content-Length -- catches truncation without opening the file
      3. read the LAST element of the largest variable -- catches a file whose
         header and dimensions are intact but whose data blocks are missing

    On failure the partial file is KEPT by default so `curl -C -` or a ranged
    retry can resume it rather than re-transferring from zero; pass
    keep_partial=False to delete instead.
    """
    import shutil
    import urllib.request
    if user is None:
        user = os.environ.get("ARMUSER", "")
    if token is None:
        token = os.environ.get("ARMTOKEN", "")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, filename)
    url = ARMLIVE_SAVE + "?user=" + user + ":" + token + "&file=" + filename
    expected = None
    with urllib.request.urlopen(url, timeout=2400) as r:
        cl = r.headers.get("Content-Length")
        expected = int(cl) if cl and cl.isdigit() else None
        with open(out, "wb") as fh:
            shutil.copyfileobj(r, fh, 1 << 20)

    def _fail(msg):
        if not keep_partial and os.path.exists(out):
            os.remove(out)
        raise IOError(msg + " (" + out + ")")

    with open(out, "rb") as fh:
        magic = fh.read(4)
    if magic[:3] != b"CDF" and magic != b"\x89HDF":
        if os.path.exists(out):
            os.remove(out)          # an HTML body is never resumable
        raise IOError("not netCDF/HDF5 (got " + repr(magic) + "); removed " + out)
    got = os.path.getsize(out)
    if expected is not None and got != expected:
        _fail("truncated: " + str(got) + " of " + str(expected) + " bytes")
    if not armlive_readable(out):
        _fail("header intact but data unreadable; likely truncated")
    return out


def armlive_readable(path, field="reflectivity"):
    """True if a radar file opens AND its last data element reads.

    The point is the last element: a stalled download leaves dimensions and
    metadata readable while the trailing data blocks are absent, so anything
    that only opens the file or reads its attributes will call it healthy.
    """
    try:
        import netCDF4
    except ImportError:
        return True                     # cannot check; do not block the caller
    try:
        with netCDF4.Dataset(path) as d:
            var = d.variables.get(field)
            if var is None:
                cands = [v for v in d.variables.values() if v.ndim >= 2]
                if not cands:
                    return True
                var = max(cands, key=lambda v: v.size)
            _ = var[tuple(slice(s - 1, s) for s in var.shape)]
        return True
    except Exception:
        return False


def mping_timestamp(t):
    """Format a time for mPING's obtime filters: 'YYYY-MM-DD HH:MM:SS'.

    The API wants a SPACE-separated stamp. An ISO string with 'T' and/or a 'Z'
    suffix -- what most APIs prefer, and what the docs imply -- makes the filter
    match nothing and the endpoint returns count=0 SILENTLY. An empty result is
    then indistinguishable from a genuinely dry window, so this normalises the
    form rather than trusting the caller to remember.
    """
    s = str(t).strip()
    if s.endswith("Z"):
        s = s[:-1]
    s = s.replace("T", " ")
    if "+" in s[10:]:
        s = s[:10] + s[10:].split("+")[0]
    if len(s) == 10:
        s = s + " 00:00:00"
    return s.strip()


def mping_reports(lat, lon, radius_m=120000, since=None, until=None,
                  token=None, pages=200):
    """mPING reports near a point. Re-filter on computed range afterwards.

    Four things the API will do to you: the host is mping.ou.edu (the old
    nssl.ou.edu name no longer resolves), the path takes NO trailing slash
    (a slash returns 404), the server-side `dist` filter over-returns by
    ~10 percent, and the obtime filters need a space-separated timestamp --
    an ISO 'T'/'Z' form returns count=0 without an error. `since`/`until` are
    normalised through mping_timestamp(), so any reasonable input works; a
    zero-result time-filtered query is then a real result, not a format bug.
    """
    import json
    import urllib.parse
    import urllib.request
    if token is None:
        token = os.environ.get("MPINGTOK", "")
    q = {"dist": radius_m, "point": str(lon) + "," + str(lat)}
    if since is not None:
        q["obtime_gte"] = mping_timestamp(since)
    if until is not None:
        q["obtime_lte"] = mping_timestamp(until)
    url = MPING_REPORTS + "?" + urllib.parse.urlencode(q)
    out = []
    for _ in range(pages):
        if not url:
            break
        req = urllib.request.Request(url, headers={
            "Authorization": "Token " + token, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            j = json.load(r)
        out.extend(j.get("results", []))
        url = j.get("next") or ""
        if url.startswith("http://"):
            url = "https://" + url[7:]
    return out


def smooth_nan_aware(a, size=None, min_weight=0.4):
    """Box-smooth an array containing NaN, without spreading it.

    scipy's uniform_filter propagates NaN across its whole window, so smoothing
    a velocity field with a few bad gates can return an entirely-NaN array (and
    an empty mask downstream, which reads as 'no data' rather than 'bug').
    Normalised convolution -- smoothed data over smoothed weights -- keeps the
    finite gates.
    """
    import numpy as np
    from scipy.ndimage import uniform_filter
    if size is None:
        size = (3, 5)
    w = np.isfinite(a).astype(float)
    num = uniform_filter(np.nan_to_num(a), size=size, mode="nearest")
    den = uniform_filter(w, size=size, mode="nearest")
    return np.where(den > min_weight, num / np.maximum(den, 1e-9), np.nan)


def azimuthal_shear(radar, vel_field=None, refl_field=None, z_min=30.0,
                    r_min_m=10000.0, r_max_m=80000.0):
    """Low-level azimuthal shear percentiles (s^-1) from the lowest sweep.

    Returns {'p50','p90','p99','p999','n','aliased_frac'}. Treat this as a
    rotation SCREEN, not a mesocyclone detection: if the volume's velocity is
    not dealiased, a folded couplet masquerades as shear. `aliased_frac` counts
    ray-to-ray differences exceeding Nyquist, which is the cheap warning.
    """
    import numpy as np
    if vel_field is None:
        vel_field = "mean_doppler_velocity"
    if refl_field is None:
        refl_field = "reflectivity"
    s = radar.get_slice(0)
    v = np.ma.masked_invalid(radar.fields[vel_field]["data"][s])
    z = np.ma.masked_invalid(radar.fields[refl_field]["data"][s])
    az = radar.azimuth["data"][s]
    rng = radar.range["data"]
    o = np.argsort(az)
    vs = smooth_nan_aware(np.ma.filled(v[o], np.nan))
    dv = np.diff(vs, axis=0)
    arc = np.clip(rng[None, :] * np.radians(np.diff(az[o]))[:, None], 1.0, None)
    shear = np.abs(dv) / arc
    # filled(), not the masked compare: `z > 30` on a masked array yields
    # masked (not False), which silently empties the mask.
    zf = np.ma.filled(z[o], -999.0)
    R = np.broadcast_to(rng[None, :], shear.shape)
    ok = np.asarray((zf[:-1] > z_min) & (R > r_min_m) & (R < r_max_m)
                    & np.isfinite(shear), bool)
    ny = 0.0
    ip = radar.instrument_parameters or {}
    if "nyquist_velocity" in ip:
        ny = float(np.max(ip["nyquist_velocity"]["data"]))
    if ok.sum() < 100:
        return dict(p50=float("nan"), p90=float("nan"), p99=float("nan"),
                    p999=float("nan"), n=int(ok.sum()), aliased_frac=float("nan"))
    sv = shear[ok]
    af = float(np.mean(np.abs(dv[ok]) > ny)) if ny > 0 else float("nan")
    return dict(p50=float(np.nanpercentile(sv, 50)), p90=float(np.nanpercentile(sv, 90)),
                p99=float(np.nanpercentile(sv, 99)), p999=float(np.nanpercentile(sv, 99.9)),
                n=int(ok.sum()), aliased_frac=af)


def convective_morphology(grid, level_m=2000.0, dbz_thresh=40.0, field=None):
    """Object statistics for the convective region of a gridded reflectivity level.

    Returns core count, areas, the largest object's share of convective area,
    and its principal-axis aspect -- the quantities that separate a line from a
    cluster from a few discrete cells.
    """
    import numpy as np
    from scipy import ndimage
    if field is None:
        field = "reflectivity"
    z = np.ma.filled(grid.fields[field]["data"], np.nan)
    k = int(np.abs(grid.z["data"] - level_m).argmin())
    z2 = z[k]
    dx = float(np.abs(np.diff(grid.x["data"]).mean()))
    conv = ndimage.binary_opening(np.nan_to_num(z2) >= dbz_thresh, np.ones((2, 2)))
    lab, n = ndimage.label(conv)
    out = dict(dx_m=dx, n_cores=int(n), conv_area_km2=float(conv.sum() * (dx / 1000.0) ** 2),
               largest_km2=0.0, frac_in_largest=0.0, aspect=0.0, major_km=0.0)
    if n == 0:
        return out
    sizes = ndimage.sum(conv, lab, range(1, n + 1))
    big = int(np.argmax(sizes)) + 1
    ys, xs = np.where(lab == big)
    out["largest_km2"] = float(sizes.max() * (dx / 1000.0) ** 2)
    out["frac_in_largest"] = float(sizes.max() / sizes.sum())
    pts = np.c_[xs * dx, ys * dx]
    if len(pts) > 2:
        pts = pts - pts.mean(0)
        ev = np.linalg.eigvalsh(np.cov(pts.T))
        major = 2 * np.sqrt(max(ev)) / 1000.0
        minor = 2 * np.sqrt(max(min(ev), 1e-9)) / 1000.0
        out["major_km"] = float(major)
        out["aspect"] = float(major / max(minor, 0.1))
    return out


def classify_morphology(m, zmax=None, echo_top_km=None, shear=None, dealiased=False):
    """Map morphology stats onto the bnf_radar class names.

    Returns (class_name, reason). Deliberately conservative about 'supercell':
    reflectivity structure cannot establish a mesocyclone, so that class is only
    reachable with `dealiased=True` and a real rotation signal. Everything else
    is decided on object geometry, which reflectivity does support.

    Pass `zmax` (max composite dBZ) and `echo_top_km` whenever available. The
    INTENSITY GATE they feed runs BEFORE the small-area test, because area alone
    mislabels scattered deep convection: a frame carrying 47-55 dBZ cores and a
    12 km echo top can hold only 12-19 km2 of contiguous >=40 dBZ, and an
    area-only rule files it as light_drizzle. Small area plus high intensity is
    isolated convection, not stratiform.
    """
    convective = ((zmax is not None and zmax >= 45.0)
                  or (echo_top_km is not None and echo_top_km >= 8.0))
    if m["conv_area_km2"] < 20 and not convective:
        return "light_drizzle", "negligible convective area, no deep or intense echo"
    dominant = m["frac_in_largest"] > 0.6
    linear = m["aspect"] >= 3.0 and m["major_km"] >= 25.0
    if dominant and linear:
        return "qlcs", "single dominant elongated convective line"
    if dominant and dealiased and shear is not None and shear.get("p999", 0) > 0.005:
        return "supercell", "dominant cell with rotation in dealiased velocity"
    if m["n_cores"] >= 8 and not dominant:
        return ("multicell_cluster",
                str(m["n_cores"]) + " cores, largest only "
                + format(m["frac_in_largest"] * 100, ".0f") + "% of convective area")
    return "isolated_cells", "few discrete convective cores"
