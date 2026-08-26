"""kernel.py for the nexrad-arco skill.

Helpers to read the NEXRAD ARCO Icechunk/Zarr store (s3://nexrad-arco) as
Py-ART radar objects, plus a surface-METAR overlay for maps/animations.

Nothing here imports icechunk at module scope: the native rustls S3 client
caches its trust store on first init, so connect() sets the CA env vars BEFORE
the first `import icechunk` (done lazily inside the function body). See SKILL.md.
"""
import copy
import numpy as np
import pandas as pd

BUCKET = "nexrad-arco"
ENGINE = "rustytree"

# ODIM field name -> Py-ART standard name (units filled on the alias)
ALIAS = {
    "reflectivity": "DBZH",
    "cross_correlation_ratio": "RHOHV",
    "differential_reflectivity": "ZDR",
    "differential_phase": "PHIDP",
    "velocity": "VRADH",
    "spectrum_width": "WRADH",
}
UNITS = {"reflectivity": "dBZ", "cross_correlation_ratio": "",
         "differential_reflectivity": "dB", "differential_phase": "deg",
         "velocity": "m/s", "spectrum_width": "m/s"}

ASOS_NETS = ["IL_ASOS", "WI_ASOS", "IN_ASOS", "IA_ASOS", "MI_ASOS"]


def ensure_ca():
    """Point the standard CA env vars at certifi so icechunk's rustls client
    trusts Amazon's cert. MUST run before the first `import icechunk` in the
    process; setdefault makes it a no-op if already set."""
    import os
    import certifi
    b = certifi.where()
    for v in ("SSL_CERT_FILE", "AWS_CA_BUNDLE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        os.environ.setdefault(v, b)


def connect(prefix, branch="main", region="us-east-1"):
    """Open a read-only anonymous Icechunk session on s3://nexrad-arco/<prefix>.

    `prefix` is the radar id (e.g. "KLOT"). Requires network access to the
    virtual-hosted host <bucket>.s3.<region>.amazonaws.com (grantable);
    s3.amazonaws.com path-style is denylisted."""
    ensure_ca()
    import icechunk
    import xradar  # noqa: F401 — registers the .xradar accessor
    storage = icechunk.s3_storage(bucket=BUCKET, prefix=prefix, region=region,
                                  anonymous=True)
    virtual_auth = icechunk.containers_credentials(
        {"s3://%s/" % BUCKET: icechunk.s3_anonymous_credentials()})
    repo = icechunk.Repository.open(storage,
                                    authorize_virtual_chunk_access=virtual_auth)
    return repo.readonly_session(branch)


def list_vcps(session):
    """VCP group names present in the store (e.g. ['VCP-212', 'VCP-35', ...])."""
    import xarray as xr
    dt = xr.open_datatree(session.store, engine=ENGINE, chunks=None)
    return sorted({g.split("/")[1] for g in dt.groups if "/" in g[1:]})


def vcp_time_bounds(session, vcps=None):
    """DataFrame (VCP, n_scans, first, last) for each VCP's sweep_0, newest first."""
    import xarray as xr
    if vcps is None:
        vcps = list_vcps(session)
    rows = []
    for v in vcps:
        try:
            d = xr.open_datatree(session.store, engine=ENGINE,
                                 group_filter="/%s/sweep_0" % v)
            vt = d["%s/sweep_0" % v]["vcp_time"].values
            rows.append((v, int(len(vt)), pd.Timestamp(vt.min()),
                         pd.Timestamp(vt.max())))
        except Exception:
            continue
    df = pd.DataFrame(rows, columns=["VCP", "n_scans", "first", "last"])
    return df.sort_values("last", ascending=False).reset_index(drop=True)


def latest_scan(session, georeference=True):
    """Globally newest volume across all VCPs.

    Returns (scan, meta): `scan` is the georeferenced sweep_0 xarray Dataset at
    that time; `meta` = dict(vcp, time, bounds)."""
    import xarray as xr
    bounds = vcp_time_bounds(session)
    if bounds.empty:
        raise RuntimeError("no VCP groups with data found")
    top = bounds.iloc[0]
    vcp, t = top["VCP"], pd.Timestamp(top["last"])
    dt0 = xr.open_datatree(session.store, engine=ENGINE,
                           group_filter="/%s/sweep_0" % vcp)
    ds = dt0["%s/sweep_0" % vcp].to_dataset(inherit="all_coords").sel(
        vcp_time=t, method="nearest")
    if georeference:
        ds = ds.xradar.georeference()
    meta = {"vcp": vcp, "time": pd.Timestamp(ds.vcp_time.values), "bounds": bounds}
    return ds, meta


def count_sweeps(session, vcp):
    """Sorted sweep group names under a VCP (['sweep_0', 'sweep_1', ...])."""
    import xarray as xr
    dt = xr.open_datatree(session.store, engine=ENGINE, group_filter="/%s/*" % vcp)
    return sorted((g.split("/")[-1] for g in dt.groups
                   if g.split("/")[-1].startswith("sweep_")),
                  key=lambda s: int(s.split("_")[1]))


def to_pyart(session, meta, nsweeps=None):
    """Build a Py-ART Radar for the volume at meta['time'] in meta['vcp'].

    Selects that timestamp across the VCP's sweeps, wraps as a CfRadial2
    DataTree, and adds Py-ART standard field-name aliases. `nsweeps` limits the
    sweep count (default all). GOTCHA: the store's sweep_number is 1-based
    float32; Py-ART's Xradar accessor indexes by 0-based sequential int64
    matching group order, so each sweep's sweep_number is rebuilt as np.int64(i)."""
    import xarray as xr
    from xarray import DataTree
    import pyart
    vcp, t = meta["vcp"], pd.Timestamp(meta["time"])
    sweep_names = count_sweeps(session, vcp)
    if nsweeps is not None:
        sweep_names = sweep_names[:nsweeps]

    sweeps, fixed = [], []
    for i, sname in enumerate(sweep_names):
        g = "/%s/%s" % (vcp, sname)
        dtk = xr.open_datatree(session.store, engine=ENGINE, group_filter=g)
        dsk = dtk["%s/%s" % (vcp, sname)].to_dataset(inherit="all_coords").sel(
            vcp_time=t, method="nearest")
        dsk = dsk.drop_vars([v for v in ["vcp_time"] if v in dsk.coords])
        dsk = dsk.copy()
        dsk["sweep_number"] = xr.DataArray(np.int64(i))  # 0-based, group order
        sweeps.append(dsk)
        fixed.append(float(dsk.sweep_fixed_angle.values))

    root = xr.Dataset(
        coords=dict(latitude=sweeps[0].latitude, longitude=sweeps[0].longitude,
                    altitude=sweeps[0].altitude),
        data_vars=dict(
            sweep_fixed_angle=("sweep", np.array(fixed)),
            sweep_group_name=("sweep",
                              np.array(["sweep_%d" % i for i in range(len(sweeps))]))))
    children = {"sweep_%d" % i: DataTree(dsk) for i, dsk in enumerate(sweeps)}
    tree = DataTree(root, children=children)
    tree.attrs["Conventions"] = "Cf/Radial"

    radar = pyart.xradar.Xradar(tree, default_sweep="sweep_0")
    for std, odim in ALIAS.items():
        if odim in radar.fields and std not in radar.fields:
            radar.fields[std] = copy.deepcopy(radar.fields[odim])
            radar.fields[std]["units"] = UNITS[std]
    return radar


# --- surface METAR overlay --------------------------------------------------

def fetch_asos(extent, start, end, nets=None, tol_pad_min=60):
    """Fetch ASOS/METAR surface obs from the Iowa Environmental Mesonet for the
    map `extent` [W, E, S, N] over [start, end] (UTC timestamps).

    Rosters are pulled per network geojson and clipped to extent; obs come from
    the IEM asos.py CGI as comma output with tmpf/dwpf/drct/sknt. Returns a
    DataFrame [station, valid(UTC), lon, lat, tmpf, dwpf, drct, sknt]."""
    import io
    import requests
    if nets is None:
        nets = ASOS_NETS
    w, e, s, n = extent
    # station roster clipped to extent
    rows = []
    for net in nets:
        try:
            gj = requests.get(
                "https://mesonet.agron.iastate.edu/geojson/network/%s.geojson" % net,
                timeout=60).json()
        except Exception:
            continue
        for f in gj.get("features", []):
            lon, lat = f["geometry"]["coordinates"][:2]
            if w <= lon <= e and s <= lat <= n:
                rows.append((f["properties"].get("sid") or f["id"], lat, lon))
    sdf = pd.DataFrame(rows, columns=["sid", "lat", "lon"]).drop_duplicates("sid")
    if sdf.empty:
        return pd.DataFrame(columns=["station", "valid", "lon", "lat",
                                     "tmpf", "dwpf", "drct", "sknt"])
    start = pd.Timestamp(start) - pd.Timedelta(minutes=tol_pad_min)
    end = pd.Timestamp(end) + pd.Timedelta(minutes=tol_pad_min)
    params = {"data": ["tmpf", "dwpf", "drct", "sknt"], "tz": "Etc/UTC",
              "format": "onlycomma", "latlon": "yes", "missing": "empty",
              "year1": start.year, "month1": start.month, "day1": start.day,
              "hour1": start.hour, "minute1": start.minute,
              "year2": end.year, "month2": end.month, "day2": end.day,
              "hour2": end.hour, "minute2": end.minute,
              "station": list(sdf["sid"])}
    r = requests.get("https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py",
                     params=params, timeout=180)
    obs = pd.read_csv(io.StringIO(r.text))
    obs["valid"] = pd.to_datetime(obs["valid"], utc=True).dt.tz_localize(None)
    for c in ("tmpf", "dwpf", "drct", "sknt"):
        obs[c] = pd.to_numeric(obs[c], errors="coerce")
    return obs[["station", "valid", "lon", "lat", "tmpf", "dwpf", "drct", "sknt"]]


def obs_for_time(obs, t, tol_min=45):
    """Nearest ob per station to time t within tol; drop stations with no data."""
    t = pd.Timestamp(t)
    df = obs.copy()
    df["dt"] = (df["valid"] - t).abs()
    df = df[df["dt"] <= pd.Timedelta(minutes=tol_min)]
    df = df.sort_values("dt").groupby("station", as_index=False).first()
    df = df[df[["tmpf", "dwpf", "drct", "sknt"]].notna().any(axis=1)]
    return df


def add_stations(ax, df, min_deg=0.42, fontsize=8):
    """Thin `df` (one time slice from obs_for_time) then draw station models on a
    cartopy GeoAxes: temp (NW, red) + dewpoint (SW, blue) as text, wind barbs.

    Deliberately bypasses MetPy's StationPlot text artist, which is broken under
    matplotlib >= 3.11 (tuple-unpack error in _get_layout); uses ax.annotate for
    the numbers and MetPy only for wind-barb geometry."""
    import cartopy.crs as ccrs
    from metpy.calc import reduce_point_density, wind_components
    from metpy.units import units
    pts = np.c_[df["lon"].values, df["lat"].values]
    mask = reduce_point_density(pts, min_deg)
    d = df[mask]
    lon = d["lon"].values
    lat = d["lat"].values
    pc = ccrs.PlateCarree()
    for x, y, t, td in zip(lon, lat, d["tmpf"].values, d["dwpf"].values):
        if np.isfinite(t):
            ax.annotate("%.0f" % t, (x, y), xytext=(-7, 5), textcoords="offset points",
                        transform=pc, color="#b2182b", fontsize=fontsize, fontweight="bold",
                        ha="right", va="bottom", zorder=12, clip_on=True)
        if np.isfinite(td):
            ax.annotate("%.0f" % td, (x, y), xytext=(-7, -5), textcoords="offset points",
                        transform=pc, color="#2166ac", fontsize=fontsize, fontweight="bold",
                        ha="right", va="top", zorder=12, clip_on=True)
    ax.scatter(lon, lat, s=6, c="k", transform=pc, zorder=11, clip_on=True)
    wok = np.isfinite(d["drct"].values) & np.isfinite(d["sknt"].values)
    if wok.any():
        u, v = wind_components(d["sknt"].values * units.knots, d["drct"].values * units.deg)
        ax.barbs(lon[wok], lat[wok], u.m[wok], v.m[wok], length=6, linewidth=0.6,
                 color="k", transform=pc, zorder=11)
    return int(mask.sum())


# --- QVP (quasi-vertical profile) -------------------------------------------

def qvp(session, vcp, times, sweep, fields=("DBZH", "ZDR", "RHOHV"),
        rho_min=0.80, min_az=15, hmax_m=None):
    """Build a time-height quasi-vertical profile from a single high tilt.

    Azimuthally averages each field per range gate over the chosen `times`
    (list/array of vcp_time timestamps or a pandas DatetimeIndex), mapping slant
    range -> height AGL with the 4/3-earth beam model. Returns a dict with keys:
    'times' (DatetimeIndex), 'height' (m AGL, 1-D), 'elev' (deg), and one 2-D
    array (time x range) per requested field.

    QC (essential — see SKILL.md): gates are kept only where RHOHV > rho_min
    (drops low-SNR noise whose rho is random-low and otherwise drags the
    azimuthal mean toward the floor), and a range gate is averaged only if at
    least `min_az` azimuths survive that mask. Pick a HIGH tilt (e.g. sweep_9 at
    ~4 deg) that is actually populated at these times — VCP-212 leaves its
    highest cuts empty at many archived times.
    """
    import numpy as np
    import pandas as pd
    import xarray as xr
    times = pd.DatetimeIndex(pd.to_datetime(list(times)))
    d = xr.open_datatree(session.store, engine=ENGINE, group_filter="/%s/%s" % (vcp, sweep))
    node = d["/%s/%s" % (vcp, sweep)].to_dataset(inherit="all_coords")
    rng = node["range"].values.astype("f8")
    vindex = node.get_index("vcp_time")
    elev = float(np.nanmean(node["ray_elevation_angle"].isel(
        vcp_time=vindex.get_indexer([times[0]], method="nearest")).values))
    Re = 4.0 / 3.0 * 6371000.0
    el = np.deg2rad(elev)
    height = np.sqrt(rng ** 2 + Re ** 2 + 2 * rng * Re * np.sin(el)) - Re
    idx = vindex.get_indexer(times, method="nearest")
    out = {f: [] for f in fields}
    for i in idx:
        rho = node["RHOHV"].isel(vcp_time=i).values.astype("f4")
        base = np.isfinite(rho) & (rho > rho_min)
        for f in fields:
            a = node[f].isel(vcp_time=i).values.astype("f4")
            m = base & np.isfinite(a)
            ok = m.sum(axis=0) >= min_az
            am = np.where(m, a, np.nan)
            with np.errstate(invalid="ignore"):
                v = np.nanmean(am, axis=0)
            out[f].append(np.where(ok, v, np.nan))
    res = {"times": times, "height": height, "elev": elev}
    for f in fields:
        res[f] = np.array(out[f])
    if hmax_m is not None:
        k = height <= hmax_m
        res["height"] = height[k]
        for f in fields:
            res[f] = res[f][:, k]
    return res
