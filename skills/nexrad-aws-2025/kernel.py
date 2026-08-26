"""Helpers for post-2025 NEXRAD access on AWS: the Unidata Level II buckets,
the NEXRAD ARCO Icechunk store, and WSR-88D VCP / SAILS / MRLE / AVSET logic.

All bucket constants and gotcha workarounds in this module were verified
against the live buckets (see SKILL.md "Verified against" for the date).
"""

import os
import re
import datetime as dt

# ----------------------------------------------------------------------------
# Buckets. The legacy noaa-nexrad-level2 bucket is DEAD (genuine S3
# AccessDenied since the Sep-2025 deprecation) -- do not fall back to it.
# ----------------------------------------------------------------------------
ARCHIVE_BUCKET = "unidata-nexrad-level2"          # YYYY/MM/DD/SITE/SITEYYYYMMDD_HHMMSS_V06
CHUNKS_BUCKET = "unidata-nexrad-level2-chunks"    # SITE/VOLNUM/YYYYMMDD-HHMMSS-NNN-{S,I,E}
LEVEL3_BUCKET = "unidata-nexrad-level3"           # SITE_PROD_YYYY_MM_DD_HH_MM_SS
ARCO_BUCKET = "nexrad-arco"                       # <SITE>/ and <SITE>-lowsweeps/ Icechunk repos
LEGACY_DEAD_BUCKET = "noaa-nexrad-level2"
AWS_REGION = "us-east-1"

# Level II volume keys; MDM sidecars share a timestamp with a real volume and
# must be excluded (they are ~0.65-0.7 MB against 4-9 MB for a volume).
VOLUME_PATTERN = r"^(?P<site>[A-Z0-9]{4})(?P<stamp>\d{8}_\d{6})_V(?P<ver>\d{2})$"
MDM_SUFFIX = "_MDM"


def volume_re():
    """Compiled matcher for Level II volume object names."""
    return re.compile(VOLUME_PATTERN)

# ----------------------------------------------------------------------------
# VCP table. Nominal elevation angles (deg) of the ascending backbone, i.e.
# SPLIT CUTS COLLAPSED and supplemental (SAILS/MRLE) cuts excluded.
# ----------------------------------------------------------------------------
VCP_TABLE = {
    11: {"elevs": [0.5, 1.45, 2.4, 3.35, 4.3, 5.25, 6.2, 7.5, 8.7, 10.0, 12.0, 14.0, 16.7, 19.5],
         "mode": "precip", "nominal_s": 300, "split_cuts": 5, "legacy": True,
         "note": "Legacy 14-tilt precip pattern, superseded by VCP 12/212."},
    12: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4, 8.0, 10.0, 12.5, 15.6, 19.5],
         "mode": "precip", "nominal_s": 258, "split_cuts": 3, "legacy": False,
         "note": "Dense low-level sampling; the standard convective pattern."},
    21: {"elevs": [0.5, 1.45, 2.4, 3.35, 4.3, 6.0, 9.9, 14.6, 19.5],
         "mode": "precip", "nominal_s": 360, "split_cuts": 2, "legacy": True,
         "note": "9-tilt legacy precip pattern."},
    31: {"elevs": [0.5, 1.5, 2.5, 3.5, 4.5],
         "mode": "clear-air", "nominal_s": 600, "split_cuts": 2, "legacy": False,
         "note": "Clear-air, LONG pulse -- most sensitive, best for snow/light rain."},
    32: {"elevs": [0.5, 1.5, 2.5, 3.5, 4.5],
         "mode": "clear-air", "nominal_s": 600, "split_cuts": 2, "legacy": False,
         "note": "Clear-air, short pulse."},
    34: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4, 10.0],
         "mode": "clear-air", "nominal_s": 600, "split_cuts": 3, "legacy": False,
         "note": "Clear-air with dense low-level cuts (VCP 12-like geometry)."},
    35: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4],
         "mode": "clear-air", "nominal_s": 420, "split_cuts": 3, "legacy": False,
         "note": "Clear-air 9-tilt; common non-precip default on modern builds."},
    112: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4, 8.0, 10.0, 12.5, 15.6, 19.5],
          "mode": "precip", "nominal_s": 280, "split_cuts": 3, "legacy": False,
          "note": "MPDA variant of VCP 12 for wide-area velocity dealiasing."},
    121: {"elevs": [0.5, 1.45, 2.4, 3.35, 4.3, 6.0, 9.9, 14.6, 19.5],
          "mode": "precip", "nominal_s": 300, "split_cuts": 5, "legacy": True,
          "note": "Multi-PRF, extra Doppler cuts for velocity dealiasing."},
    211: {"elevs": [0.5, 1.45, 2.4, 3.35, 4.3, 5.25, 6.2, 7.5, 8.7, 10.0, 12.0, 14.0, 16.7, 19.5],
          "mode": "precip", "nominal_s": 300, "split_cuts": 5, "legacy": True,
          "note": "SZ-2 phase-coded version of VCP 11."},
    212: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4, 8.0, 10.0, 12.5, 15.6, 19.5],
          "mode": "precip", "nominal_s": 258, "split_cuts": 3, "legacy": False,
          "note": "SZ-2 version of VCP 12; the workhorse severe-convection pattern."},
    215: {"elevs": [0.5, 0.9, 1.3, 1.8, 2.4, 3.1, 4.0, 5.1, 6.4, 8.0, 10.0, 12.0, 14.0, 16.7, 19.5],
          "mode": "precip", "nominal_s": 360, "split_cuts": 3, "legacy": False,
          "note": "15-tilt deep pattern for tropical / deep-convection coverage."},
}

# Supplemental-scan feature names, for classify_scan() output.
SAILS_MAX = 3          # SAILS x1 .. MESO-SAILS x3 (three supplemental base tilts)
MRLE_CHOICES = (2, 3, 4)   # MRLE+2 / +3 / +4 lowest tilts repeated


# ----------------------------------------------------------------------------
# Anonymous S3
# ----------------------------------------------------------------------------
def s3_anon():
    """Unsigned boto3 S3 client for the public NEXRAD buckets."""
    import boto3
    from botocore import UNSIGNED
    from botocore.config import Config

    return boto3.client("s3", region_name=AWS_REGION,
                        config=Config(signature_version=UNSIGNED))


def parse_volume_stamp(name):
    m = volume_re().match(name)
    if not m:
        return None
    return dt.datetime.strptime(m.group("stamp"), "%Y%m%d_%H%M%S").replace(
        tzinfo=dt.timezone.utc)


def nexrad_keys(site, start, end=None, client=None, min_bytes=1_500_000):
    """List Level II volume objects for `site` between `start` and `end` (UTC).

    Excludes ``*_V06_MDM`` sidecars by suffix AND anything below `min_bytes`,
    which is the robust filter -- MDM objects are 0.65-0.7 MB where real
    volumes are 4-9 MB.

    Returns a list of dicts: key, name, time, size, version.
    """
    c = client or s3_anon()
    if end is None:
        end = start + dt.timedelta(hours=1)
    if getattr(start, "tzinfo", None) is None:
        start = start.replace(tzinfo=dt.timezone.utc)
    if getattr(end, "tzinfo", None) is None:
        end = end.replace(tzinfo=dt.timezone.utc)

    out = []
    pag = c.get_paginator("list_objects_v2")
    day = start.date()
    while day <= end.date():
        prefix = f"{day:%Y/%m/%d}/{site.upper()}/"
        for page in pag.paginate(Bucket=ARCHIVE_BUCKET, Prefix=prefix):
            for obj in page.get("Contents", []):
                name = obj["Key"].rsplit("/", 1)[-1]
                if name.endswith(MDM_SUFFIX) or obj["Size"] < min_bytes:
                    continue
                t = parse_volume_stamp(name)
                if t is None or not (start <= t <= end):
                    continue
                m = volume_re().match(name)
                out.append(dict(key=obj["Key"], name=name, time=t,
                                size=obj["Size"], version=int(m.group("ver"))))
        day += dt.timedelta(days=1)
    return sorted(out, key=lambda r: r["time"])


def latest_volume(site, client=None, lookback_hours=6):
    """Most recent archived Level II volume for `site` (archive lag ~7 min)."""
    now = dt.datetime.now(dt.timezone.utc)
    keys = nexrad_keys(site, now - dt.timedelta(hours=lookback_hours), now,
                       client=client)
    return keys[-1] if keys else None


def download_volume(key, dest_dir=".", client=None, overwrite=False):
    """Download one Level II object; returns the local path."""
    c = client or s3_anon()
    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, key.rsplit("/", 1)[-1])
    if overwrite or not os.path.exists(path):
        c.download_file(ARCHIVE_BUCKET, key, path)
    return path


def nexrad_sites(day=None, client=None):
    """Site IDs reporting to the archive bucket on `day` (default: yesterday)."""
    c = client or s3_anon()
    day = day or (dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1))
    r = c.list_objects_v2(Bucket=ARCHIVE_BUCKET, Prefix=f"{day:%Y/%m/%d}/",
                          Delimiter="/")
    return sorted(p["Prefix"].split("/")[-2] for p in r.get("CommonPrefixes", []))


def realtime_chunks(site, client=None, volume=None):
    """List real-time 'chunk' objects for `site` from the chunks bucket.

    The chunks bucket carries the live LDM feed split into per-sweep messages:
    ``SITE/<volnum>/YYYYMMDD-HHMMSS-NNN-{S,I,E}`` where the trailing letter is
    Start / Intermediate / End of volume. `volnum` cycles 1..999, so it orders
    volumes only locally -- sort by the timestamp in the object name.
    Latency is seconds, against ~7 minutes for the archive bucket.
    """
    c = client or s3_anon()
    prefix = f"{site.upper()}/" + (f"{volume}/" if volume is not None else "")
    if volume is None:
        r = c.list_objects_v2(Bucket=CHUNKS_BUCKET, Prefix=prefix, Delimiter="/")
        return sorted(p["Prefix"].split("/")[-2] for p in r.get("CommonPrefixes", []))
    out = []
    for page in c.get_paginator("list_objects_v2").paginate(
            Bucket=CHUNKS_BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            nm = obj["Key"].rsplit("/", 1)[-1]
            out.append(dict(key=obj["Key"], name=nm, size=obj["Size"],
                            kind=nm[-1], modified=obj["LastModified"]))
    return sorted(out, key=lambda r: r["name"])


# ----------------------------------------------------------------------------
# VCP / SAILS / MRLE / AVSET logic
# ----------------------------------------------------------------------------
def vcp_info(vcp):
    """Static description of a VCP number (see VCP_TABLE)."""
    return VCP_TABLE.get(int(vcp))


def classify_scan(elevs, vcp=None, tol=0.15):
    """Identify SAILS / MESO-SAILS / MRLE / AVSET from an as-scanned elevation list.

    Pass the fixed angle of EVERY sweep in volume order (split cuts included,
    e.g. ``radar.fixed_angle['data']`` from Py-ART). The algorithm collapses
    consecutive equal elevations (split cuts), then walks the sequence: the
    ascending backbone is the nominal VCP, and any DESCENT starts a
    supplemental block.

    - every supplemental block is a single cut at the base tilt -> ``SAILSxN``
      (N=1 SAILS, N=2..3 MESO-SAILS)
    - a supplemental block that climbs through several low tilts -> ``MRLE+K``
      where K is the number of tilts in the block
    - backbone top below the VCP's nominal top -> ``avset_active`` (AVSET cut
      the volume short because upper tilts held no echo)

    Returns dict(mode, n_supplemental, extra_blocks, base_elev, backbone,
                 backbone_top, nominal_top, avset_active, unique_elevs,
                 n_sweeps, vcp).
    """
    import numpy as np

    e = np.asarray(list(elevs), dtype=float)
    if e.size == 0:
        raise ValueError("empty elevation list")
    base = float(e.min())

    runs = [float(e[0])]
    for v in e[1:]:
        if abs(float(v) - runs[-1]) > tol:
            runs.append(float(v))

    backbone, extra, i = [runs[0]], [], 1
    while i < len(runs):
        if runs[i] > backbone[-1] + tol:
            backbone.append(runs[i])
            i += 1
        else:
            block = [runs[i]]
            i += 1
            while (i < len(runs) and runs[i] > block[-1] + tol
                   and runs[i] < backbone[-1] - tol):
                block.append(runs[i])
                i += 1
            extra.append([round(x, 2) for x in block])

    n = len(extra)
    if n == 0:
        mode = "none"
    elif all(len(b) == 1 and abs(b[0] - base) <= tol for b in extra):
        mode = f"SAILSx{n}"
    else:
        mode = f"MRLE+{max(len(b) for b in extra)}"

    info = vcp_info(vcp) if vcp is not None else None
    nominal_top = max(info["elevs"]) if info else None
    top = round(max(backbone), 2)
    avset = bool(nominal_top is not None and top < nominal_top - 0.3)

    return dict(mode=mode, n_supplemental=n, extra_blocks=extra,
                base_elev=round(base, 2),
                backbone=[round(x, 2) for x in backbone], backbone_top=top,
                nominal_top=nominal_top, avset_active=avset,
                unique_elevs=int(np.unique(np.round(e, 2)).size),
                n_sweeps=int(e.size), vcp=(int(vcp) if vcp is not None else None))


def scan_anatomy(radar):
    """Per-sweep table for a Py-ART NEXRAD Radar: elevation, rays, timing, cut kind.

    ``kind`` is inferred from which moments carry data in that sweep:
    ``surv`` (reflectivity + dual-pol, no velocity -- the surveillance half of
    a split cut), ``dop`` (velocity, no dual-pol -- the Doppler half), or
    ``batch`` (everything, a single non-split cut).

    Returns a pandas DataFrame; also flags the split-cut partner index.
    """
    import numpy as np
    import pandas as pd

    fa = np.asarray(radar.fixed_angle["data"], dtype=float)
    rows = []
    for i in range(radar.nsweeps):
        s, e = radar.get_start_end(i)
        t = np.asarray(radar.time["data"][s:e + 1], dtype=float)
        present = []
        for name, fld in radar.fields.items():
            blk = fld["data"][s:e + 1]
            filled = blk.filled(np.nan) if hasattr(blk, "filled") else blk
            if np.isfinite(filled).any():
                present.append(name)
        has_vel = any("velocity" in f for f in present)
        has_pol = any(f in present for f in
                      ("differential_reflectivity", "cross_correlation_ratio",
                       "differential_phase"))
        kind = "batch" if (has_vel and has_pol) else ("dop" if has_vel else "surv")
        rows.append(dict(sweep=i, elev=round(float(fa[i]), 2), nrays=int(e - s + 1),
                         t_start=round(float(t[0]), 1), t_end=round(float(t[-1]), 1),
                         kind=kind, nfields=len(present)))
    df = pd.DataFrame(rows)

    partner = [-1] * len(df)
    for i in range(len(df) - 1):
        if (abs(df.elev[i] - df.elev[i + 1]) < 0.05
                and {df.kind[i], df.kind[i + 1]} == {"surv", "dop"}):
            partner[i], partner[i + 1] = i + 1, i
    df["split_partner"] = partner
    return df


def dedup_split_cuts(radar, prefer="surv"):
    """Sweep indices with one cut per distinct elevation (split cuts resolved).

    NEXRAD split cuts record the same elevation twice -- a long-PRT
    surveillance cut (reflectivity + dual-pol, full unambiguous range) and a
    Doppler cut (velocity, shorter range). ``pyart.xradar.Xradar`` runs
    ``np.unique`` on sweep_fixed_angle, so a 17-sweep VCP-212 volume yields a
    14-element fixed_angle array and any code indexing it by sweep number
    raises IndexError. Deduplicating first avoids that.

    `prefer` selects which half of each split pair to keep: "surv" for
    reflectivity/dual-pol work, "dop" for velocity work.
    """
    df = scan_anatomy(radar)
    keep, seen = [], {}
    for _, r in df.iterrows():
        key = round(r.elev, 2)
        if key not in seen:
            seen[key] = int(r.sweep)
            keep.append(int(r.sweep))
        else:
            prev = seen[key]
            if df.kind[prev] != prefer and r.kind == prefer:
                keep[keep.index(prev)] = int(r.sweep)
                seen[key] = int(r.sweep)
    return sorted(keep)


def read_nexrad_volume(path_or_key, dest_dir=".", client=None, **kwargs):
    """Read a Level II volume with Py-ART, downloading from S3 if given a key."""
    import pyart

    path = path_or_key
    if "/" in str(path_or_key) and not os.path.exists(str(path_or_key)):
        path = download_volume(path_or_key, dest_dir=dest_dir, client=client)
    return pyart.io.read_nexrad_archive(path, **kwargs)


# ----------------------------------------------------------------------------
# NEXRAD ARCO (Icechunk / Zarr v3)
# ----------------------------------------------------------------------------
ARCO_EPOCH = "1950-01-01"   # units of the per-ray `time` arrays
ARCO_MISSING_THRESHOLD = 900.0  # gates with value <= -this are the -999 sentinel


def ensure_ca():
    """Point the native (Rust) S3 client at certifi's CA bundle.

    icechunk's object_store client does not read certifi by default and fails
    the S3 handshake with ``invalid peer certificate: UnknownIssuer``. The
    native trust store initialises ONCE PER PROCESS and is cached, so this
    must run BEFORE the first ``import icechunk`` -- a kernel that already
    imported icechunk without it cannot recover and must be restarted.
    """
    import certifi

    bundle = certifi.where()
    for var in ("SSL_CERT_FILE", "AWS_CA_BUNDLE", "REQUESTS_CA_BUNDLE",
                "CURL_CA_BUNDLE"):
        os.environ.setdefault(var, bundle)
    return bundle


def arco_open(site, lowsweeps=False, branch="main"):
    """Open a NEXRAD ARCO Icechunk repo anonymously; returns the zarr root group.

    Reading at the ZARR level (not xarray) is deliberate: the store has ~12
    VCP groups x 8-20 sweeps, and ``xr.open_datatree`` eagerly opens and
    CF-decodes every one of them, which takes many minutes. Zarr access is
    lazy per array.

    Two gotchas are handled here:
      * virtual chunk containers -- some groups reference chunks by
        ``s3://nexrad-arco/`` URL and need explicit anonymous authorisation,
        else reads raise "a virtual chunk in this repository resolves to ...".
      * TLS trust for the Rust client (see ensure_ca).
    """
    ensure_ca()
    import icechunk as ic
    import zarr

    prefix = f"{site.upper()}-lowsweeps" if lowsweeps else site.upper()
    storage = ic.s3_storage(bucket=ARCO_BUCKET, prefix=prefix,
                            region=AWS_REGION, anonymous=True)
    repo = ic.Repository.open(
        storage,
        authorize_virtual_chunk_access=ic.containers_credentials(
            {f"s3://{ARCO_BUCKET}/": ic.s3_credentials(anonymous=True)}
        ),
    )
    return zarr.open_group(repo.readonly_session(branch).store, mode="r")


def arco_vcps(root):
    """Inventory of a site repo: one row per VCP group.

    Includes the scan-configuration attributes the store now carries
    (``avset_enabled``, ``num_base_tilts``, ``dynamic_scan_type``,
    ``vcp_truncated``, ``super_res_status``, ``rda_build_number``). Older
    groups predate these attributes and report None.
    """
    import pandas as pd

    keys = ("scan_name", "dynamic_scan_type", "num_base_tilts", "base_tilt_vcp",
            "mpda_vcp", "vcp_truncated", "vcp_sequence_active",
            "number_elevation_cuts", "actual_elevation_cuts", "avset_enabled",
            "ebc_enabled", "super_res_status", "rda_build_number",
            "operational_mode", "vcp_pulse_width", "doppler_velocity_resolution",
            "time_domain")
    rows = []
    for name, g in root.groups():
        attrs = dict(g.attrs)
        n_sweeps = sum(1 for _ in g.groups())
        n_scans = int(g["vcp_time"].shape[0]) if "vcp_time" in g else -1
        row = dict(group=name, n_sweeps=n_sweeps, n_scans=n_scans)
        num = re.sub(r"[^0-9]", "", name)
        row["vcp"] = int(num) if num else None
        row.update({k: attrs.get(k) for k in keys})
        rows.append(row)
    df = pd.DataFrame(rows)
    return df.sort_values("n_scans", ascending=False).reset_index(drop=True)


def arco_times(root, group):
    """Decoded scan times for one VCP (or lowsweeps) group, as datetime64[ns].

    The `vcp_time` axis is coarsely chunked (whole-array or ~62k), so reading
    it entirely is ONE request and takes a second or two -- do that, then
    ``np.searchsorted``. Never scan the per-ray ``time`` array by column: it is
    chunked ``(1, nrays)``, so a column read issues one request PER SCAN.

    Handles both epoch conventions found in the store: per-VCP `vcp_time` is
    nanoseconds since 1950-01-01, while the lowsweeps groups carry a
    store-specific ``units`` attribute ("nanoseconds since 2015-01-01 ...").
    """
    import numpy as np

    g = root[group]
    arr = g["vcp_time"] if "vcp_time" in g else g["sweep_0"]["vcp_time"]
    raw = arr[:]
    units = dict(arr.attrs).get("units", f"nanoseconds since {ARCO_EPOCH}")
    m = re.search(r"since\s+(.+)$", str(units))
    epoch = m.group(1).strip().replace(" ", "T") if m else ARCO_EPOCH
    return np.datetime64(epoch, "ns") + raw.astype("timedelta64[ns]")


def arco_nearest(root, group, when):
    """Index of the scan nearest `when` in `group`; returns (index, actual_time)."""
    import numpy as np

    times = arco_times(root, group)
    t = np.datetime64(when, "ns")
    i = int(np.clip(np.searchsorted(times, t), 0, times.size - 1))
    if i > 0 and abs(times[i - 1] - t) < abs(times[i] - t):
        i -= 1
    return i, times[i]


def arco_mask(a):
    """Mask the -999 sentinel that ARCO float fields carry (NOT auto-decoded).

    The stored ``_FillValue`` is base64-encoded in the attrs, so neither zarr
    nor xarray masks it. Left unmasked, ~75% of gates in a low sweep enter an
    analysis as -999 dBZ.
    """
    import numpy as np

    out = np.asarray(a, dtype="float32")
    return np.where(out <= -ARCO_MISSING_THRESHOLD, np.nan, out)


def arco_sweep(root, group, index, sweep=0, fields=None, mask=True):
    """One sweep of one scan from ARCO as an xarray Dataset (CfRadial2-ish).

    Returns georeferenced x/y/z via the xradar accessor, with -999 masked.
    """
    import numpy as np
    import xarray as xr
    import xradar  # noqa: F401  (registers the .xradar accessor)

    g = root[group]
    sg = g[f"sweep_{sweep}"] if f"sweep_{sweep}" in g else g
    names = fields or [k for k, _ in sg.arrays()
                       if k not in ("azimuth", "range", "elevation", "time",
                                    "vcp_time", "sweep_fixed_angle",
                                    "sweep_number", "ray_elevation_angle",
                                    "latitude", "longitude", "altitude",
                                    "volume_number", "prt_mode", "follow_mode",
                                    "sweep_mode", "platform_type",
                                    "instrument_type")]
    az = sg["azimuth"][:]
    rng = sg["range"][:]
    data = {}
    for f in names:
        arr = sg[f]
        if arr.ndim != 3:
            continue
        v = arr[index]
        data[f] = (("azimuth", "range"), arco_mask(v) if mask else np.asarray(v))
    if not data:
        raise ValueError(f"no 2-D fields found in {group}/sweep_{sweep}")

    src = g if "latitude" in g else sg
    t = np.int64(sg["time"][index, 0])
    ds = xr.Dataset(
        data,
        coords=dict(
            azimuth=("azimuth", np.asarray(az)),
            range=("range", np.asarray(rng)),
            elevation=("azimuth", np.asarray(sg["ray_elevation_angle"][index])),
            latitude=float(src["latitude"][()]),
            longitude=float(src["longitude"][()]),
            altitude=float(src["altitude"][()]),
            time=np.datetime64(ARCO_EPOCH, "ns") + t.astype("timedelta64[ns]"),
        ),
        attrs=dict(dict(g.attrs), sweep_fixed_angle=float(sg["sweep_fixed_angle"][index]),
                   sweep_number=float(sg["sweep_number"][index]), source_group=group,
                   scan_index=int(index)),
    )
    ds["range"].attrs.update(dict(sg["range"].attrs))
    ds = ds.assign_coords(sweep_mode="azimuth_surveillance")
    return ds.xradar.georeference()


def arco_volume_indices(root, group, index, max_span=4):
    """Consecutive scan indices that together make ONE physical volume.

    This is the ARCO layout trap. A scan index is not always a complete
    volume: when the radar runs SAILS/MESO-SAILS the writer splits one
    physical volume across SEVERAL consecutive indices -- measured on KLOT
    VCP-212 during the 27 Jul 2026 outbreak, a repeating 3-index cycle of
    low cuts (0.48/0.88/1.27), then mid cuts (0.48 + 1.8-6.42), then upper
    cuts (0.48 + 8.0-19.51). Grid only ``index`` and you silently lose two
    thirds of the volume.

    Groups by ascending elevation structure: ignoring repeats of the base
    tilt (the SAILS cuts, which appear in every fragment), a new volume
    starts wherever a non-base elevation stops exceeding the running
    maximum.

    Returns a sorted list of indices (``[index]`` when that index is already
    a complete volume, as in quiet periods).
    """
    import numpy as np

    n = int(root[group]["vcp_time"].shape[0]) if "vcp_time" in root[group] \
        else int(root[group]["sweep_0"]["vcp_time"].shape[0])

    def nonbase_max(i):
        els = [e["fixed_angle"] for e in arco_scan_elevations(root, group, i)
               if e["recorded"] and e["fixed_angle"] is not None]
        if not els:
            return None, []
        base = min(els)
        nb = [x for x in els if x > base + 0.15]
        return (max(nb) if nb else None), els

    start = int(index)
    while start - 1 >= 0 and start > index - max_span:
        hi_prev, _ = nonbase_max(start - 1)
        hi_cur, _ = nonbase_max(start)
        if hi_prev is None or hi_cur is None or hi_prev >= hi_cur:
            break
        start -= 1

    out, run_max = [start], None
    i = start
    while i < min(n, start + max_span):
        hi, els = nonbase_max(i)
        if i > start:
            if hi is None or (run_max is not None and hi <= run_max):
                break
            out.append(i)
        run_max = hi if hi is not None else run_max
        i += 1
    return out


def arco_scan_elevations(root, group, index):
    """Fixed angles of every sweep group at one scan index, in sweep order.

    NaN (or a non-positive first-ray time) marks a sweep the radar did not
    record at that index -- normally AVSET truncation of the upper tilts.
    Feed the finite values to classify_scan() to label the scan.
    """
    import numpy as np

    g = root[group]
    names = sorted((k for k, _ in g.groups()),
                   key=lambda s: int(re.sub(r"[^0-9]", "", s) or 0))
    out = []
    for s in names:
        sg = g[s]
        fa = float(sg["sweep_fixed_angle"][index])
        t0 = np.int64(sg["time"][index, 0])
        out.append(dict(sweep=s, fixed_angle=(None if not np.isfinite(fa) else round(fa, 2)),
                        recorded=bool(t0 > 0)))
    return out
