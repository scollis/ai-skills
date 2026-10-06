"""Helpers for ARM BNF C-SAPR2 + NASA NALMA storm case studies."""
import os
import json
import gzip
import pathlib
import zipfile
import datetime as dt
import urllib.parse
import urllib.request
import subprocess
import xml.etree.ElementTree as ET

ARM_QUERY_URL = "https://adc.arm.gov/armlive/data/query"
ARM_SAVE_URL = "https://adc.arm.gov/armlive/data/saveData"
CMR_URL = "https://cmr.earthdata.nasa.gov/search"
BNF_KMZ_URL = "https://github.com/ARM-Development/bnf-radar-examples/raw/main/notebooks/locations/BNF.kmz"
KML_NS = "{http://www.opengis.net/kml/2.2}"
PPI_RHI_SIZE_SPLIT = 300000000


def arm_credentials():
    """Return (user, token) for ARM Live from env, credential store, or file.

    Never hardcode these. Order: ARM_USER/ARM_TOKEN env vars, then a
    Claude Science credential store, then ~/.arm_live_creds.json.
    """
    user = os.environ.get("ARM_USER")
    token = os.environ.get("ARM_TOKEN")
    if user and token:
        return user, token
    try:
        return (host.credentials.get("ARM_USER")["value"],
                host.credentials.get("ARM_TOKEN")["value"])
    except Exception:
        pass
    path = pathlib.Path.home() / ".arm_live_creds.json"
    if path.exists():
        blob = json.loads(path.read_text())
        return blob["user"], blob["token"]
    raise RuntimeError("no ARM Live credentials: set ARM_USER/ARM_TOKEN or "
                       "write ~/.arm_live_creds.json {'user':..,'token':..}")


def arm_query(datastream, start, end, user=None, token=None):
    """List filenames in an ARM datastream between two dates (YYYY-MM-DD)."""
    if user is None or token is None:
        user, token = arm_credentials()
    query = urllib.parse.urlencode({"user": "%s:%s" % (user, token),
                                    "ds": datastream, "start": str(start),
                                    "end": str(end), "wt": "json"})
    with urllib.request.urlopen(ARM_QUERY_URL + "?" + query, timeout=60) as resp:
        return sorted(json.load(resp).get("files", []))


def arm_fetch(fname, dest_dir, user=None, token=None):
    """Download one ARM file unless already present. Returns (Path, cached)."""
    if user is None or token is None:
        user, token = arm_credentials()
    target = pathlib.Path(dest_dir) / fname
    if target.exists() and target.stat().st_size > 0:
        return target, True
    query = urllib.parse.urlencode({"user": "%s:%s" % (user, token), "file": fname})
    tmp = target.with_suffix(target.suffix + ".part")
    urllib.request.urlretrieve(ARM_SAVE_URL + "?" + query, tmp)
    tmp.rename(target)
    return target, False


def arm_file_time(fname):
    """Parse the timestamp from an ARM filename: datastream.YYYYMMDD.HHMMSS.nc"""
    parts = pathlib.Path(fname).name.split(".")
    return dt.datetime.strptime(parts[2] + parts[3], "%Y%m%d%H%M%S")


def arm_stage_window(datastream, day, start, end, dest_dir, workers=6):
    """Stage every file of a datastream inside [start, end]. Returns list of Paths."""
    from concurrent.futures import ThreadPoolExecutor
    user, token = arm_credentials()
    dest = pathlib.Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    listing = arm_query(datastream, day, day + dt.timedelta(days=1), user, token)
    wanted = [f for f in listing if start <= arm_file_time(f) <= end]
    with ThreadPoolExecutor(workers) as pool:
        got = list(pool.map(lambda f: arm_fetch(f, dest, user, token), wanted))
    return [p for p, _ in got]


def split_ppi_rhi(paths, size_split=None):
    """Split an interleaved C-SAPR2 file list into (ppi_volumes, rhis) by size.

    BNF publishes ONE interleaved datastream; PPI volumes are ~40x larger than
    single-sweep RHIs, so file size separates them without opening every file.
    """
    if size_split is None:
        size_split = PPI_RHI_SIZE_SPLIT
    paths = [pathlib.Path(p) for p in paths]
    ppi = [p for p in paths if p.stat().st_size > size_split]
    rhi = [p for p in paths if p.stat().st_size <= size_split]
    return sorted(ppi), sorted(rhi)


def setup_radar_plotting(cartopy_cache=None):
    """Apply the two matplotlib/cartopy settings this workflow depends on.

    savefig.bbox='tight' silently mis-crops cartopy GeoAxes placed at explicit
    figure rectangles; cartopy also needs a writable shapefile cache.
    """
    import matplotlib
    matplotlib.rcParams["savefig.bbox"] = "standard"
    if cartopy_cache is None:
        cartopy_cache = os.environ.get("CARTOPY_DATA_DIR",
                                       str(pathlib.Path.home() / ".cartopy_cache"))
    pathlib.Path(cartopy_cache).mkdir(parents=True, exist_ok=True)
    os.environ["CARTOPY_DATA_DIR"] = str(cartopy_cache)
    import cartopy
    cartopy.config["data_dir"] = str(cartopy_cache)
    return str(cartopy_cache)


def dualpol_gatefilter(radar, snr_min=8.0, rhohv_min=0.8, z_min=0.0, speckle=25):
    """Conservative gate filter for C-band dual-pol precipitation analysis.

    Note despeckle_field is a module-level function returning a GateFilter --
    it is not a GateFilter method.
    """
    import pyart
    gatefilter = pyart.correct.despeckle_field(radar, "reflectivity", size=speckle)
    gatefilter.exclude_masked("reflectivity")
    gatefilter.exclude_below("signal_to_noise_ratio_copolar_h", snr_min)
    gatefilter.exclude_below("copol_correlation_coeff", rhohv_min)
    gatefilter.exclude_below("reflectivity", z_min)
    return gatefilter


def to_datetime(stamp):
    """Coerce a Py-ART time (possibly cftime) to stdlib datetime for plotting."""
    if isinstance(stamp, dt.datetime):
        return stamp
    return dt.datetime(stamp.year, stamp.month, stamp.day, stamp.hour,
                       stamp.minute, int(stamp.second),
                       int((stamp.second - int(stamp.second)) * 1e6))


def read_rhi(path, filtered=True, fields=None):
    """Load one RHI as a dict of plane coordinates and fields.

    filtered=True applies the dual-pol gate filter (quantitative use).
    filtered=False leaves Z_H fully raw and masks only sub-noise gates in
    Z_DR/velocity, which is what you want for display and animation.
    """
    import numpy as np
    import pyart
    if fields is None:
        fields = ["reflectivity", "differential_reflectivity",
                  "mean_doppler_velocity", "copol_correlation_coeff",
                  "signal_to_noise_ratio_copolar_h"]
    radar = pyart.io.read(path, include_fields=fields)
    gx, gy, gz = radar.get_gate_x_y_z(0)
    if filtered:
        gatefilter = dualpol_gatefilter(radar)
        excluded = gatefilter.gate_excluded
        zh = np.ma.masked_where(excluded, radar.fields["reflectivity"]["data"])
        zdr = np.ma.masked_where(excluded, radar.fields["differential_reflectivity"]["data"])
        vel = np.ma.masked_where(excluded, radar.fields["mean_doppler_velocity"]["data"])
    else:
        snr = radar.fields["signal_to_noise_ratio_copolar_h"]["data"]
        no_signal = np.ma.filled(snr, -999) < 0.0
        zh = radar.fields["reflectivity"]["data"]
        zdr = np.ma.masked_where(no_signal, radar.fields["differential_reflectivity"]["data"])
        vel = np.ma.masked_where(no_signal, radar.fields["mean_doppler_velocity"]["data"])
    out = {"rng": np.hypot(gx, gy) / 1000.0, "ht": gz / 1000.0,
           "Z": zh, "D": zdr, "V": vel,
           "az": float(radar.fixed_angle["data"][0]),
           "nyquist": float(radar.get_nyquist_vel(0)),
           "time": to_datetime(pyart.util.datetime_from_radar(radar))}
    del radar
    return out


def echo_top(scan, threshold=40.0):
    """Highest gate (km) at or above a reflectivity threshold; NaN if absent."""
    import numpy as np
    zh = scan["Z"]
    mask = (zh >= threshold)
    if np.ma.isMaskedArray(mask):
        mask = mask.filled(False)
    if not mask.any():
        return float("nan")
    return float(scan["ht"][mask].max())


def sweep_echo_areas(path, thresholds=None):
    """Range-weighted echo area (km^2) above each threshold on the lowest sweep.

    Gate cell area is (r * dphi) * dr, so cells tile the sweep without overlap
    and no Cartesian regridding is needed.
    """
    import numpy as np
    import pyart
    if thresholds is None:
        thresholds = (30, 40, 50, 55)
    radar = pyart.io.read(path, include_fields=["reflectivity"])
    sweep = radar.extract_sweeps([0])
    zh = sweep.fields["reflectivity"]["data"]
    gx, gy, _ = sweep.get_gate_x_y_z(0)
    rng_km = np.hypot(gx, gy) / 1000.0
    dr = float(np.diff(radar.range["data"])[0]) / 1000.0
    daz = np.deg2rad(float(np.median(np.abs(np.diff(sweep.azimuth["data"][:50])))) or 1.0)
    cell = (rng_km * daz) * dr
    valid = ~np.ma.getmaskarray(zh)
    out = {"time": to_datetime(pyart.util.datetime_from_radar(radar)),
           "max_dbz_volume": float(np.ma.max(radar.fields["reflectivity"]["data"])),
           "max_dbz_sweep0": float(np.ma.max(zh))}
    for thresh in thresholds:
        out["area_ge%s_km2" % thresh] = float(cell[valid & (zh >= thresh)].sum())
    del radar, sweep
    return out


def sounding_temperature_level(path, target_c=0.0, ref_alt_m=0.0):
    """Height (m) where an ARM sonde profile first crosses target_c.

    Pass ref_alt_m=radar altitude to get height above the radar instead of MSL.
    """
    import numpy as np
    import netCDF4
    with netCDF4.Dataset(path) as nc:
        temp = np.ma.masked_invalid(nc["tdry"][:])
        alt = np.ma.masked_invalid(nc["alt"][:])
    crossings = np.where((temp[:-1] > target_c) & (temp[1:] <= target_c))[0]
    if not len(crossings):
        return float("nan")
    idx = crossings[0]
    frac = (temp[idx] - target_c) / (temp[idx] - temp[idx + 1])
    return float(alt[idx] + frac * (alt[idx + 1] - alt[idx])) - ref_alt_m


def parse_bnf_kmz(dest_dir, url=None):
    """Download and parse the ARM BNF KMZ. Returns {name: (lat, lon)}.

    Use the github.com/.../raw/... URL -- raw.githubusercontent.com returns a
    404 stub for this path. Most of the 41 placemarks are instruments packed
    within ~200 m at M1; filter to spatially distinct sites before plotting.
    """
    if url is None:
        url = BNF_KMZ_URL
    dest = pathlib.Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    kmz = dest / "BNF.kmz"
    if not (kmz.exists() and zipfile.is_zipfile(kmz)):
        urllib.request.urlretrieve(url, kmz)
    if not zipfile.is_zipfile(kmz):
        raise RuntimeError("BNF.kmz did not download as a zip archive")
    with zipfile.ZipFile(kmz) as archive:
        kml = archive.read("doc.kml").decode("utf-8", "replace")
    sites = {}
    for placemark in ET.fromstring(kml).iter(KML_NS + "Placemark"):
        name_el = placemark.find(KML_NS + "name")
        coord_el = placemark.find(".//" + KML_NS + "Point/" + KML_NS + "coordinates")
        if name_el is None or coord_el is None or not (coord_el.text or "").strip():
            continue
        lon, lat = (coord_el.text or "").strip().split(",")[:2]
        name = (name_el.text or "").strip()
        if name and name not in sites:
            sites[name] = (float(lat), float(lon))
    return sites


def cmr_granules(short_name, t_start, t_end, provider="GHRC_DAAC"):
    """Find (title, download_url) for CMR granules over a time range.

    Query CMR rather than constructing filenames -- it catches boundary
    granules a hand-built loop misses.
    """
    coll = urllib.parse.urlencode({"short_name": short_name, "provider": provider})
    with urllib.request.urlopen(CMR_URL + "/collections.json?" + coll, timeout=60) as resp:
        entries = json.load(resp)["feed"]["entry"]
    if not entries:
        raise RuntimeError("no CMR collection named %r at %s" % (short_name, provider))
    window = "%s,%s" % (t_start.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        t_end.strftime("%Y-%m-%dT%H:%M:%SZ"))
    gran = urllib.parse.urlencode({"collection_concept_id": entries[0]["id"],
                                   "temporal": window, "page_size": 200,
                                   "sort_key": "start_date"})
    with urllib.request.urlopen(CMR_URL + "/granules.json?" + gran, timeout=60) as resp:
        granules = json.load(resp)["feed"]["entry"]
    out = []
    for granule in granules:
        links = [l["href"] for l in granule.get("links", [])
                 if l.get("rel", "").endswith("/data#")]
        if links:
            out.append((granule["title"], links[0]))
    return out


def earthdata_fetch(url, dest, netrc=None):
    """Download one Earthdata-protected file via curl. Returns (Path, cached).

    curl follows the OAuth chain with --location-trusted plus a cookie jar;
    urllib does not. Needs a ~/.netrc entry using the SHORT EDL username.
    """
    if netrc is None:
        netrc = os.environ.get("NETRC_PATH", str(pathlib.Path.home() / ".netrc"))
    target = pathlib.Path(dest)
    if target.exists() and target.stat().st_size > 1000:
        return target, True
    target.parent.mkdir(parents=True, exist_ok=True)
    cookies = target.parent / ".edl_cookies"
    subprocess.run(["curl", "-sSL", "--netrc-file", str(netrc), "--location-trusted",
                    "-b", str(cookies), "-c", str(cookies), "-o", str(target),
                    "--max-time", "300", url], check=True)
    if target.stat().st_size < 1000:
        head = target.read_text(errors="replace")[:120]
        target.unlink()
        raise RuntimeError("Earthdata download failed (%r). Check the SHORT EDL "
                          "username in %s, and that the DAAC is an authorized "
                          "app in your EDL profile." % (head, netrc))
    return target, False


def read_nalma_sources(path):
    """Parse a NALMA analysed-data file into an (N, 7) array.

    Columns: sec_of_day, lat, lon, alt_m, reduced_chi2, power_dBW, n_stations
    """
    import numpy as np
    rows = []
    in_data = False
    with gzip.open(path, "rt", errors="replace") as handle:
        for line in handle:
            if not in_data:
                in_data = line.startswith("*** data ***")
                continue
            parts = line.split()
            if len(parts) < 7:
                continue
            rows.append((float(parts[0]), float(parts[1]), float(parts[2]),
                         float(parts[3]), float(parts[4]), float(parts[5]),
                         bin(int(parts[6], 16)).count("1")))
    return np.array(rows)


def nalma_quality_mask(sources, chi2_max=1.0, nsta_min=7, alt_max_km=20.0):
    """Boolean mask of scientifically usable VHF sources (~13% of raw).

    The solver accepts chi2 <= 5; standard practice is much tighter.
    """
    return ((sources[:, 4] <= chi2_max) & (sources[:, 6] >= nsta_min)
            & (sources[:, 3] / 1000.0 <= alt_max_km))


def project_sources_to_rhi_plane(sources, radar_lon, radar_lat, azimuth,
                                 half_width_km=10.0, max_range_km=110.0):
    """Project VHF sources onto an RHI plane.

    Returns (along_km, cross_km, alt_km, in_plane_mask). Plot along_km vs
    alt_km for sources where in_plane_mask is True. State the tolerance in the
    figure: some plotted sources belong to convection beside the slice.
    """
    import numpy as np
    from pyart.core import geographic_to_cartesian_aeqd
    sx, sy = geographic_to_cartesian_aeqd(sources[:, 2], sources[:, 1],
                                          radar_lon, radar_lat)
    sx = np.asarray(sx).ravel() / 1000.0
    sy = np.asarray(sy).ravel() / 1000.0
    unit_x = np.sin(np.deg2rad(azimuth))
    unit_y = np.cos(np.deg2rad(azimuth))
    along = sx * unit_x + sy * unit_y
    cross = -sx * unit_y + sy * unit_x
    alt_km = sources[:, 3] / 1000.0
    in_plane = ((np.abs(cross) <= half_width_km) & (along > 0)
                & (along <= max_range_km))
    return along, cross, alt_km, in_plane


def aeqd_origin_offset(radar):
    """Metres by which a radar-centred cartopy AEQD misplaces the radar itself.

    cartopy's AzimuthalEquidistant is inaccurate at its own origin for non-zero
    central latitude, so pyart's plot_ppi_map draws gates displaced by this
    amount. Returns (dx, dy) in metres; |dy| of order 20 km means the bug is
    present. Plot on a Mercator axes with gate lon/lat instead.
    """
    import cartopy.crs as ccrs
    lon = float(radar.longitude["data"][0])
    lat = float(radar.latitude["data"][0])
    aeqd = ccrs.AzimuthalEquidistant(central_longitude=lon, central_latitude=lat)
    x, y = aeqd.transform_point(lon, lat, ccrs.PlateCarree())
    return float(x), float(y)


def ppi_gate_latlon(radar, field, sweep=0, gatefilter=None):
    """Gate lon/lat and masked field for one sweep, for correct map plotting.

    Draw with ax.pcolormesh(glon, glat, data, transform=ccrs.PlateCarree()) on a
    Mercator axes -- never a radar-centred AEQD (see aeqd_origin_offset).
    """
    import numpy as np
    sl = radar.get_slice(sweep)
    glon = radar.gate_longitude["data"][sl]
    glat = radar.gate_latitude["data"][sl]
    data = np.ma.masked_array(radar.fields[field]["data"][sl])
    if gatefilter is not None:
        data = np.ma.masked_where(gatefilter.gate_excluded[sl], data)
    return glon, glat, data


def clutter_centroid(radar, sweep=0, max_range_km=12.0):
    """Mean (lon, lat) of near-range gates -- should equal the site metadata.

    A centroid displaced from radar.longitude/latitude means the plotted field
    and the site marker are in different coordinate references.
    """
    import numpy as np
    sl = radar.get_slice(sweep)
    glon = radar.gate_longitude["data"][sl]
    glat = radar.gate_latitude["data"][sl]
    rng_km = radar.range["data"] / 1000.0
    near = np.broadcast_to(rng_km < max_range_km, glon.shape)
    return float(np.mean(glon[near])), float(np.mean(glat[near]))
