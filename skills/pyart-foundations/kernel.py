"""Helpers for pyart-foundations: scan anatomy, split-cut dedup, field reports."""
import os


def setup_cartopy_cache(path="cartopy_data"):
    """Point cartopy's Natural Earth cache at a writable workspace dir.

    The default (~/.local/share/cartopy) is read-only in this sandbox and raises
    PermissionError on the first add_feature call. Call before any cartopy feature use.
    """
    import cartopy
    os.makedirs(path, exist_ok=True)
    ap = os.path.abspath(path)
    cartopy.config["data_dir"] = ap
    cartopy.config["pre_existing_data_dir"] = ap
    return ap


def classify_sweep_kind(radar, sweep):
    """Return 'surv' (dual-pol, no velocity), 'dop' (velocity, no dual-pol) or 'batch'.

    NEXRAD split cuts pair a surveillance sweep (Z/ZDR/RhoHV/PhiDP) with a Doppler
    sweep (V/SW) at the same elevation. Above the split-cut region, sweeps carry
    everything ('batch'). Research radars return 'batch' for every sweep.
    """
    import numpy as np
    sl = radar.get_slice(sweep)
    has = {}
    for name, d in radar.fields.items():
        blk = d["data"][sl]
        has[name] = bool(np.ma.count(blk) > 0)
    dualpol = any(has.get(f, False) for f in
                  ("differential_reflectivity", "cross_correlation_ratio",
                   "differential_phase"))
    doppler = has.get("velocity", False)
    if dualpol and doppler:
        return "batch"
    if dualpol:
        return "surv"
    if doppler:
        return "dop"
    return "batch"


def scan_anatomy(radar):
    """DataFrame of per-sweep elevation, ray count, timing, kind and split partner.

    Columns: sweep, elev, nrays, t_start, t_end, kind, nfields, split_partner
    (-1 when the sweep has no partner). Read this before any per-sweep processing.
    """
    import numpy as np
    import pandas as pd
    rows = []
    for s in range(radar.nsweeps):
        sl = radar.get_slice(s)
        t = radar.time["data"][sl]
        nf = sum(1 for d in radar.fields.values()
                 if np.ma.count(d["data"][sl]) > 0)
        rows.append(dict(sweep=s,
                         elev=round(float(radar.fixed_angle["data"][s]), 2),
                         nrays=int(sl.stop - sl.start),
                         t_start=round(float(t[0]), 1),
                         t_end=round(float(t[-1]), 1),
                         kind=classify_sweep_kind(radar, s),
                         nfields=nf,
                         split_partner=-1))
    df = pd.DataFrame(rows)
    for i, r in df.iterrows():
        if r["kind"] not in ("surv", "dop"):
            continue
        want = "dop" if r["kind"] == "surv" else "surv"
        cand = df[(df.elev == r.elev) & (df.kind == want) &
                  (abs(df.index - i) <= 2)]
        if len(cand):
            df.loc[i, "split_partner"] = int(cand.index[0])
    return df


def dedup_split_cuts(radar, prefer="surv"):
    """Sweep indices with one entry per unique elevation.

    prefer='surv' picks the dual-pol member of each split cut (for Z/ZDR/KDP work);
    prefer='dop' picks the Doppler member (for velocity work). Sweeps that carry
    everything are always included. On a research radar this returns every sweep.
    """
    import numpy as np
    df = scan_anatomy(radar)
    keep = []
    for elev in sorted(df.elev.unique()):
        sub = df[df.elev == elev]
        pick = sub[sub.kind == prefer]
        if len(pick) == 0:
            pick = sub[sub.kind == "batch"]
        if len(pick) == 0:
            pick = sub
        keep.append(int(pick.iloc[0].sweep))
    return sorted(keep)


def renumber_sweeps(radar):
    """Reset sweep_number to arange(nsweeps), in place.

    extract_sweeps preserves the ORIGINAL sweep numbers, so functions that loop
    sweep_number and call get_slice raise IndexError('Sweep out of range').
    Confirmed to affect composite_reflectivity and storm_relative_velocity.
    """
    import numpy as np
    dt = radar.sweep_number["data"].dtype
    radar.sweep_number["data"] = np.arange(radar.nsweeps, dtype=dt)
    return radar


def field_report(radar, fill_floor_magnitude=1000.0):
    """DataFrame of every field: units, valid fraction, p1/p50/p99.

    Values below -fill_floor_magnitude are masked as sentinel fill (-9999, -32768),
    which some readers and algorithms leave in place; they otherwise dominate the
    percentiles. The threshold is passed as a positive magnitude because the skill
    loader rejects negative literals as top-level defaults.
    """
    import numpy as np
    import pandas as pd
    rows = []
    for name, d in radar.fields.items():
        a = np.ma.filled(d["data"], np.nan).astype(float)
        a[a < -fill_floor_magnitude] = np.nan
        ok = np.isfinite(a)
        rows.append(dict(field=name, units=d.get("units", "?"),
                         valid_frac=round(float(ok.mean()), 4),
                         p1=round(float(np.nanpercentile(a, 1)), 3) if ok.any() else None,
                         p50=round(float(np.nanmedian(a)), 3) if ok.any() else None,
                         p99=round(float(np.nanpercentile(a, 99)), 3) if ok.any() else None))
    return pd.DataFrame(rows)


def nyquist_values(radar):
    """Sorted list of the unique Nyquist velocities in the volume, rounded.

    A single value means uniform (research radars); several means per-sweep values
    (NEXRAD), which is why velocity algorithms need check_nyquist_uniform=False.
    For the full decision dict (which flags to pass to which dealiaser) use
    nyquist_summary from pyart-velocity-dealias instead.
    """
    import numpy as np
    ip = radar.instrument_parameters
    if not ip or "nyquist_velocity" not in ip:
        return None
    return sorted(set(np.round(ip["nyquist_velocity"]["data"], 2).tolist()))
