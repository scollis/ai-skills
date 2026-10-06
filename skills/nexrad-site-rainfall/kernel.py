"""Helpers for KIWA/NEXRAD rainfall analysis over a fixed ground site.

All third-party imports are deferred into function bodies so that merely
loading the skill never fails on a bare python kernel. Requires (in the
target env): arm_pyart, boto3, numpy, pandas, cartopy, cmweather.
"""

NEXRAD_BUCKET = "unidata-nexrad-level2"   # anonymous LIST+GET works here
EARTH_R_KM = 6371.0
ZR_A = 200.0   # Marshall-Palmer Z = A * R**b
ZR_B = 1.6


def nexrad_s3_client():
    """Anonymous (UNSIGNED) boto3 S3 client for the Unidata NEXRAD bucket."""
    import boto3
    from botocore import UNSIGNED
    from botocore.config import Config
    return boto3.client(
        "s3", region_name="us-east-1",
        config=Config(signature_version=UNSIGNED,
                      s3={"addressing_style": "virtual"},
                      retries={"max_attempts": 4}))


def list_scan_keys(radar_id, start, end, client=None):
    """List Level II object keys for radar_id between start/end (UTC dates or
    datetimes). Returns list of dicts: {key, timestamp}. NEXRAD keys are laid
    out as YYYY/MM/DD/RADAR/RADARYYYYMMDD_HHMMSS_V06."""
    import pandas as pd, re
    if client is None:
        client = nexrad_s3_client()
    start = pd.Timestamp(start); end = pd.Timestamp(end)
    out = []
    pat = re.compile(rf"{radar_id}(\d{{8}})_(\d{{6}})")
    for day in pd.date_range(start.normalize(), end.normalize(), freq="D"):
        prefix = f"{day:%Y/%m/%d}/{radar_id}/"
        token = None
        while True:
            kw = dict(Bucket=NEXRAD_BUCKET, Prefix=prefix, MaxKeys=1000)
            if token:
                kw["ContinuationToken"] = token
            resp = client.list_objects_v2(**kw)
            for o in resp.get("Contents", []):
                k = o["Key"]
                m = pat.search(k)
                if not m or k.endswith("_MDM"):
                    continue
                ts = pd.Timestamp(m.group(1) + m.group(2))
                if start <= ts <= end:
                    out.append({"key": k, "timestamp": ts})
            if resp.get("IsTruncated"):
                token = resp.get("NextContinuationToken")
            else:
                break
    out.sort(key=lambda d: d["timestamp"])
    return out


def zr_rate(dbz, a=None, b=None):
    """Marshall-Palmer rain rate (mm/hr) from reflectivity (dBZ). Vectorized."""
    import numpy as np
    if a is None: a = ZR_A
    if b is None: b = ZR_B
    z_lin = 10.0 ** (np.asarray(dbz) / 10.0)
    return (z_lin / a) ** (1.0 / b)


def site_gatefilter(radar):
    import pyart
    gf = pyart.filters.GateFilter(radar)
    gf.exclude_transition(); gf.exclude_invalid('reflectivity')
    if 'cross_correlation_ratio' in radar.fields:
        gf.exclude_below('cross_correlation_ratio', 0.85)
    gf.exclude_below('reflectivity', 5.0)
    return gf


def extract_site_stats(path, site_lat, site_lon, radius_km=10.0, rainy_dbz=20.0):
    """Read one NEXRAD volume, QC the lowest sweep, and summarize reflectivity
    within radius_km of (site_lat, site_lon). Returns dict with max_dbz,
    p95_dbz, rainy_frac, mean_rr (disk-mean mm/hr over rainy gates), ngate."""
    import numpy as np, math, pyart
    radar = pyart.io.read_nexrad_archive(path)
    sweep0 = radar.extract_sweeps([0])
    gf = site_gatefilter(sweep0)
    lat, lon, _ = sweep0.get_gate_lat_lon_alt(0)
    dlat = (lat - site_lat) * 111.0
    dlon = (lon - site_lon) * 111.0 * math.cos(math.radians(site_lat))
    dist = np.sqrt(dlat**2 + dlon**2)
    disk = dist <= radius_km
    z = sweep0.fields['reflectivity']['data']
    z = np.ma.masked_where(gf.gate_excluded, z)
    valid = z[disk].compressed(); ngate = int(disk.sum())
    if valid.size == 0:
        return dict(max_dbz=float("nan"), p95_dbz=float("nan"),
                    rainy_frac=0.0, mean_rr=0.0, ngate=ngate)
    rr = zr_rate(valid)
    return dict(max_dbz=float(valid.max()),
                p95_dbz=float(np.percentile(valid, 95)),
                rainy_frac=float((valid >= rainy_dbz).sum() / ngate),
                mean_rr=float(rr[valid >= rainy_dbz].sum() / ngate),
                ngate=ngate)


def ppi_map(path, outpng, site_lat, site_lon, event_id="", when="",
            metrics="", radius_km=10.0, cmap="ChaseSpectral",
            vmin=None, vmax=65):
    """Render a QC'd reflectivity PPI map of the lowest sweep, centered on the
    radar, with a site marker, dashed analysis disk, and range rings.
    Uses the colorblind-safe ChaseSpectral colormap (cmweather)."""
    if vmin is None:
        vmin = -10   # dBZ floor, negated here (gate: no UnaryOp default)
    import numpy as np, matplotlib.pyplot as plt
    import cartopy.crs as ccrs, cartopy.feature as cfeature
    import pyart, cmweather  # noqa: F401  (registers ChaseSpectral)
    radar = pyart.io.read_nexrad_archive(path)
    rlat = float(radar.latitude['data'][0]); rlon = float(radar.longitude['data'][0])
    disp = pyart.graph.RadarMapDisplay(radar)
    gf = site_gatefilter(radar)
    proj = ccrs.LambertConformal(central_latitude=rlat, central_longitude=rlon)
    fig = plt.figure(figsize=(7.5, 7.0))
    ax = plt.axes(projection=proj)
    disp.plot_ppi_map('reflectivity', sweep=0, ax=ax, gatefilter=gf,
                      vmin=vmin, vmax=vmax, cmap=cmap,
                      colorbar_label='Reflectivity (dBZ)',
                      min_lat=rlat-1.1, max_lat=rlat+1.1,
                      min_lon=rlon-1.3, max_lon=rlon+1.3,
                      resolution='10m', embellish=False, title_flag=False)
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='0.4', lw=0.6)
    disp.plot_point(site_lon, site_lat, symbol='k^', markersize=9)
    for rr in (50, 100, 150):
        disp.plot_range_ring(rr, col='0.5', ls=':', lw=0.5)
    th = np.linspace(0, 2*np.pi, 180)
    dlat = radius_km/111.0; dlon = radius_km/(111.0*np.cos(np.radians(site_lat)))
    ax.plot(site_lon+dlon*np.cos(th), site_lat+dlat*np.sin(th),
            transform=ccrs.PlateCarree(), color='k', lw=1.2, ls='--')
    ax.annotate("site", xy=(site_lon, site_lat),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                xytext=(6, 6), textcoords='offset points',
                fontsize=8, fontweight='bold')
    ttl = "reflectivity (0.5° sweep)"
    if event_id:
        ttl += f" — Event {event_id}"
    ax.set_title(f"{ttl}\n{when} UTC", fontsize=11)
    if metrics:
        ax.text(0.015, 0.985, metrics, transform=ax.transAxes, fontsize=8.5,
                va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='0.5', alpha=0.85))
    gl = ax.gridlines(draw_labels=True, lw=0.3, color='0.7', alpha=0.5)
    gl.top_labels = False; gl.right_labels = False
    fig.savefig(outpng, dpi=170, bbox_inches='tight'); plt.close(fig)
    return outpng


def rainrate_map(path, outpng, site_lat, site_lon, event_id="", when="",
                 metrics="", radius_km=10.0, cmap="ChaseSpectral",
                 bounds=None):
    """Render a QC'd Marshall-Palmer rain-rate PPI map (mm/hr) of the lowest
    sweep with a discrete log-like colorbar. Colorblind-safe ChaseSpectral."""
    import numpy as np, matplotlib.pyplot as plt
    import cartopy.crs as ccrs, cartopy.feature as cfeature
    from matplotlib.colors import BoundaryNorm
    import pyart, cmweather  # noqa: F401
    if bounds is None:
        bounds = [0.1, 0.5, 1, 2, 5, 10, 20, 35, 50, 75, 100]
    radar = pyart.io.read_nexrad_archive(path)
    rlat = float(radar.latitude['data'][0]); rlon = float(radar.longitude['data'][0])
    dbz = radar.fields['reflectivity']['data']
    rr = zr_rate(dbz)
    radar.add_field_like('reflectivity', 'rain_rate',
                         np.ma.masked_array(rr, mask=np.ma.getmaskarray(dbz)),
                         replace_existing=True)
    radar.fields['rain_rate']['units'] = 'mm/hr'
    radar.fields['rain_rate']['long_name'] = 'Rain rate (Marshall-Palmer)'
    disp = pyart.graph.RadarMapDisplay(radar)
    gf = site_gatefilter(radar)
    proj = ccrs.LambertConformal(central_latitude=rlat, central_longitude=rlon)
    fig = plt.figure(figsize=(7.5, 7.0))
    ax = plt.axes(projection=proj)
    cmo = plt.get_cmap(cmap, len(bounds)-1)
    norm = BoundaryNorm(bounds, cmo.N)
    disp.plot_ppi_map('rain_rate', sweep=0, ax=ax, gatefilter=gf,
                      norm=norm, cmap=cmo, colorbar_label='Rain rate (mm/hr)',
                      min_lat=rlat-1.1, max_lat=rlat+1.1,
                      min_lon=rlon-1.3, max_lon=rlon+1.3,
                      resolution='10m', embellish=False, title_flag=False)
    ax.add_feature(cfeature.STATES.with_scale('10m'), edgecolor='0.4', lw=0.6)
    disp.plot_point(site_lon, site_lat, symbol='k^', markersize=9)
    for rr_ring in (50, 100, 150):
        disp.plot_range_ring(rr_ring, col='0.5', ls=':', lw=0.5)
    th = np.linspace(0, 2*np.pi, 180)
    dlat = radius_km/111.0; dlon = radius_km/(111.0*np.cos(np.radians(site_lat)))
    ax.plot(site_lon+dlon*np.cos(th), site_lat+dlat*np.sin(th),
            transform=ccrs.PlateCarree(), color='k', lw=1.2, ls='--')
    ax.annotate("site", xy=(site_lon, site_lat),
                xycoords=ccrs.PlateCarree()._as_mpl_transform(ax),
                xytext=(6, 6), textcoords='offset points',
                fontsize=8, fontweight='bold')
    ttl = "rain rate (Z-R, 0.5° sweep)"
    if event_id:
        ttl += f" — Event {event_id}"
    ax.set_title(f"{ttl}\n{when} UTC", fontsize=11)
    if metrics:
        ax.text(0.015, 0.985, metrics, transform=ax.transAxes, fontsize=8.5,
                va='top', ha='left',
                bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='0.5', alpha=0.85))
    gl = ax.gridlines(draw_labels=True, lw=0.3, color='0.7', alpha=0.5)
    gl.top_labels = False; gl.right_labels = False
    fig.savefig(outpng, dpi=170, bbox_inches='tight'); plt.close(fig)
    return outpng


def download_key(key, client=None, scratch="scratch"):
    """Download one NEXRAD key to a temp file (caller/pipeline deletes it)."""
    import tempfile, os
    if client is None:
        client = nexrad_s3_client()
    os.makedirs(scratch, exist_ok=True)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix="_V06", dir=scratch).name
    client.download_file(NEXRAD_BUCKET, key, tmp)
    return tmp


def subsample_hourly(catalog, every_h=1):
    """Keep the first scan in each every_h-hour UTC bin. catalog: list of
    {key,timestamp} (or DataFrame rows)."""
    import pandas as pd
    seen = {}
    for rec in sorted(catalog, key=lambda d: pd.Timestamp(d["timestamp"])):
        t = pd.Timestamp(rec["timestamp"])
        b = t.floor(f"{int(every_h)}h")
        if b not in seen:
            seen[b] = rec
    return list(seen.values())


def scan_worker(rec, client, site_lat, site_lon, radius_km, rainy_dbz):
    tmp = download_key(rec["key"], client)
    try:
        s = extract_site_stats(tmp, site_lat, site_lon, radius_km=radius_km, rainy_dbz=rainy_dbz)
    except Exception:
        s = dict(max_dbz=float("nan"), p95_dbz=float("nan"),
                 rainy_frac=float("nan"), mean_rr=float("nan"), ngate=0)
    finally:
        try: os.remove(tmp)
        except OSError: pass
    s["key"] = rec["key"]; s["timestamp"] = pd.Timestamp(rec["timestamp"])
    return s


def process_keys(records, client, site_lat, site_lon, radius_km, rainy_dbz, workers):
    rows = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(scan_worker, r, client, site_lat, site_lon, radius_km, rainy_dbz)
                for r in records]
        for f in as_completed(futs):
            rows.append(f.result())
    return pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)


def run_site_rainfall(radar_id, site_lat, site_lon, start, end,
                      radius_km=10.0, rainy_dbz=20.0, survey_every_h=1,
                      detect_dbz=35.0, event_gap_h=2.0, min_rainy_scans=3,
                      accum_gap_min=20.0, workers=12, outdir=".",
                      make_maps=True, client=None, verbose=True):
    """End-to-end site-rainfall pipeline for one NEXRAD radar.

    catalog -> hourly survey -> event detection -> full-res drill-down ->
    accumulation -> per-event peak PPI maps. Returns a dict:
      {events, survey, drilldown, catalog, figures, totals}
    and writes CSVs + PNGs to outdir.
    """
    import os, pandas as pd, numpy as np
    if client is None:
        client = nexrad_s3_client()
    os.makedirs(outdir, exist_ok=True)
    def log(*a):
        if verbose: print(*a, flush=True)

    # 1. Catalog -------------------------------------------------------------
    catalog = list_scan_keys(radar_id, start, end, client=client)
    if not catalog:
        raise ValueError(f"no {radar_id} scans found in {start}..{end}")
    cat_df = pd.DataFrame(catalog)
    cat_df.to_csv(os.path.join(outdir, "scan_catalog.csv"), index=False)
    log(f"catalog: {len(catalog)} scans")

    # 2. Coarse survey -------------------------------------------------------
    survey_recs = subsample_hourly(catalog, every_h=survey_every_h)
    log(f"survey: {len(survey_recs)} scans (~1/{survey_every_h}h)")
    survey = process_keys(survey_recs, client, site_lat, site_lon,
                           radius_km, rainy_dbz, workers)
    survey.to_csv(os.path.join(outdir, "survey_timeseries.csv"), index=False)

    # 3. Detect candidate events --------------------------------------------
    survey["wet"] = (survey["max_dbz"] >= detect_dbz) | (survey["rainy_frac"] > 0)
    gap = pd.Timedelta(hours=event_gap_h)
    windows = []
    cur = None
    for _, r in survey[survey["wet"]].iterrows():
        t = pd.Timestamp(r["timestamp"])
        if cur is None:
            cur = [t, t]
        elif t - cur[1] <= gap:
            cur[1] = t
        else:
            windows.append(cur); cur = [t, t]
    if cur is not None:
        windows.append(cur)
    log(f"detected {len(windows)} candidate window(s)")

    # 4-5. Drill-down + accumulate per window --------------------------------
    pad = pd.Timedelta(minutes=30)
    cat_ts = pd.to_datetime(cat_df["timestamp"])
    ev_rows, all_dd, figures = [], [], []
    for i, (w0, w1) in enumerate(windows, start=1):
        eid = f"E{i:02d}"
        m = (cat_ts >= w0 - pad) & (cat_ts <= w1 + pad)
        recs = cat_df[m].to_dict("records")
        dd = process_keys(recs, client, site_lat, site_lon, radius_km, rainy_dbz, workers)
        dd["event_id"] = eid
        all_dd.append(dd)
        wet = dd[(dd["max_dbz"] >= detect_dbz) | (dd["rainy_frac"] > 0)].copy()
        n_rainy = int((dd["rainy_frac"].fillna(0) > 0).sum())

        # trapezoidal time integration of rain rate, skipping big gaps
        d = dd.dropna(subset=["mean_rr"]).sort_values("timestamp")
        t_h = (pd.to_datetime(d["timestamp"]).astype("int64")/1e9/3600.0).to_numpy()
        rr_disk = d["mean_rr"].to_numpy()
        rf = d["rainy_frac"].to_numpy()
        rr_cond = np.where(rf > 0, rr_disk/np.where(rf==0, np.nan, rf), 0.0)
        rr_cond = np.nan_to_num(rr_cond)
        accum_disk = accum_cond = 0.0
        for j in range(1, len(t_h)):
            dth = t_h[j]-t_h[j-1]
            if dth <= accum_gap_min/60.0:
                accum_disk += 0.5*(rr_disk[j]+rr_disk[j-1])*dth
                accum_cond += 0.5*(rr_cond[j]+rr_cond[j-1])*dth

        peak_dbz = float(dd["max_dbz"].max()) if dd["max_dbz"].notna().any() else float("nan")
        if wet.empty:
            r_start = r_end = pd.NaT; dur = 0.0
        else:
            r_start = pd.Timestamp(wet["timestamp"].min())
            r_end   = pd.Timestamp(wet["timestamp"].max())
            dur = (r_end - r_start).total_seconds()/60.0
        cls = ("significant" if (peak_dbz >= detect_dbz and n_rainy >= min_rainy_scans)
               else "marginal" if n_rainy >= 1 else "trace/no rain")
        # peak scan + map
        fig_png = ""
        if make_maps and dd["max_dbz"].notna().any():
            prow = dd.loc[dd["max_dbz"].idxmax()]
            when = pd.Timestamp(prow["timestamp"]).strftime("%Y-%m-%d %H:%M")
            metrics = f"peak {peak_dbz:.0f} dBZ\ncond. accum ≈ {accum_cond:.1f} mm\nrain dur ≈ {dur:.0f} min"
            tmp = download_key(prow["key"], client)
            try:
                fig_png = os.path.join(outdir, f"event_{eid}_ppi.png")
                ppi_map(tmp, fig_png, site_lat, site_lon, event_id=eid, when=when, metrics=metrics,
                        radius_km=radius_km)
                figures.append(fig_png)
            finally:
                try: os.remove(tmp)
                except OSError: pass
        ev_rows.append(dict(event_id=eid, cls=cls, rain_start=r_start, rain_end=r_end,
                            rain_dur_min=round(dur,1), peak_dbz=peak_dbz,
                            accum_conditional_mm=round(accum_cond,2),
                            accum_diskmean_mm=round(accum_disk,3),
                            n_scans=len(dd), n_rainy_scans=n_rainy, peak_map=fig_png))
        log(f"  {eid}: {cls}, peak {peak_dbz:.0f} dBZ, cond {accum_cond:.1f} mm, {n_rainy} rainy scans")

    events = pd.DataFrame(ev_rows)
    events.to_csv(os.path.join(outdir, "rainfall_events.csv"), index=False)
    drilldown = pd.concat(all_dd, ignore_index=True) if all_dd else pd.DataFrame()
    if len(drilldown):
        drilldown.to_csv(os.path.join(outdir, "event_timeseries.csv"), index=False)
    totals = dict(n_events=len(events),
                  n_significant=int((events["cls"]=="significant").sum()) if len(events) else 0,
                  total_accum_conditional_mm=round(float(events["accum_conditional_mm"].sum()),1) if len(events) else 0.0,
                  total_accum_diskmean_mm=round(float(events["accum_diskmean_mm"].sum()),2) if len(events) else 0.0)
    log("totals:", totals)
    return dict(events=events, survey=survey, drilldown=drilldown,
                catalog=cat_df, figures=figures, totals=totals)


