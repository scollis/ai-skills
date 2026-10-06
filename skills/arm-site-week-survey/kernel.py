"""Helpers for surveying an ARM site over a multi-day window via ARM Live."""
import os
import json
import pathlib
import urllib.parse
import urllib.request

ARM_QUERY_URL = "https://adc.arm.gov/armlive/data/query"
ARM_SAVE_URL = "https://adc.arm.gov/armlive/data/saveData"
COMMON_INSTRUMENTS = ("met", "aosmet", "ceil", "ld", "ldquants", "sirs", "sebs",
                      "ecorsf", "stamp", "mwr3c", "mwrlos", "mplpolfs", "mfrsr7nch",
                      "sondewnpn", "pblhtsonde1mcfarl", "interpolatedsonde",
                      "dlfpt", "dlprofwind4news", "wbpluvio2", "vdis", "aoscpcf",
                      "aosccn2cola", "aosnephdry", "aosaps", "aoso3", "qcrad1long",
                      "tsiskycover", "irt", "smos", "rwpwindcon", "kazrcfrge")
COMMON_LEVELS = ("b1", "c1", "a1", "s1", "b0")
LIGHT_INSTRUMENTS = ("met", "ld", "ldquants", "ceil", "sirs", "sebs", "mwr3c",
                     "mfrsr7nch", "sondewnpn", "pblhtsonde1mcfarl", "wbpluvio2",
                     "dlprofwind4news")


def arm_survey_credentials():
    """Return (user, token) for ARM Live from environment variables.

    Never hardcode credentials. Checks ARM_USER/ARM_TOKEN, then ARMUNAME and
    ALIVE_TOKEN, which are the names the Claude Science credential store
    exports for ARM.
    """
    user = os.environ.get("ARM_USER") or os.environ.get("ARMUNAME")
    token = os.environ.get("ARM_TOKEN") or os.environ.get("ALIVE_TOKEN")
    if not user or not token:
        raise RuntimeError("Set ARM_USER/ARM_TOKEN (or ARMUNAME/ALIVE_TOKEN)")
    return user, token


def arm_list_files(datastream, start, end, user=None, token=None):
    """Filenames in a datastream between two YYYY-MM-DD dates; [] if none."""
    if user is None or token is None:
        user, token = arm_survey_credentials()
    query = urllib.parse.urlencode({"user": "%s:%s" % (user, token),
                                    "ds": datastream, "start": str(start),
                                    "end": str(end), "wt": "json"})
    with urllib.request.urlopen(ARM_QUERY_URL + "?" + query, timeout=60) as resp:
        return sorted(json.load(resp).get("files", []))


def arm_get_file(fname, dest_dir, user=None, token=None):
    """Download one ARM file unless already present. Returns (Path, cached)."""
    if user is None or token is None:
        user, token = arm_survey_credentials()
    target = pathlib.Path(dest_dir) / fname
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        return target, True
    query = urllib.parse.urlencode({"user": "%s:%s" % (user, token), "file": fname})
    tmp = target.with_suffix(target.suffix + ".part")
    urllib.request.urlretrieve(ARM_SAVE_URL + "?" + query, tmp)
    tmp.rename(target)
    return target, False


def discover_datastreams(site, facilities, start, end, instruments=None,
                         levels=None, workers=16):
    """Probe constructed datastream names; return {name: file_count} for hits.

    The ARM discovery/Solr endpoints are unusable (HTML shell / 502), so this
    sweeps <site><instrument><facility>.<level> combinations against the Live
    query endpoint. Nonexistent names return empty lists, not errors, so a
    1000-name sweep is safe. ~3% hit rate is normal.
    """
    import concurrent.futures as cf
    if instruments is None:
        instruments = COMMON_INSTRUMENTS
    if levels is None:
        levels = COMMON_LEVELS
    user, token = arm_survey_credentials()
    names = []
    for inst in instruments:
        for fac in facilities:
            for lvl in levels:
                names.append("%s%s%s.%s" % (site, inst, fac, lvl))
    names = list(dict.fromkeys(names))

    def probe(ds):
        try:
            return ds, len(arm_list_files(ds, start, end, user, token))
        except Exception:
            return ds, -1

    with cf.ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(probe, names))
    return {ds: n for ds, n in sorted(results) if n > 0}


def stage_datastreams(datastreams, start, end, dest_root, workers=8):
    """Download whole datastreams into dest_root/<datastream>/.

    Returns {datastream: [Path, ...]}. Skips files already on disk. Intended
    for lightweight surface/profiling streams -- stage scanning radar
    separately and subsampled.
    """
    import concurrent.futures as cf
    user, token = arm_survey_credentials()
    root = pathlib.Path(dest_root)
    jobs = []
    for ds in datastreams:
        for fname in arm_list_files(ds, start, end, user, token):
            jobs.append((ds, fname))

    def fetch(job):
        ds, fname = job
        path, _ = arm_get_file(fname, root / ds, user, token)
        return ds, path

    out = {ds: [] for ds in datastreams}
    with cf.ThreadPoolExecutor(workers) as ex:
        for ds, path in ex.map(fetch, jobs):
            out[ds].append(path)
    return {ds: sorted(paths) for ds, paths in out.items()}


def load_datastream(ds_dir, variables, apply_qc=True, freq=None):
    """Concatenate a datastream's daily files into a DataFrame.

    Applies each variable's companion qc_<var> flag (keeps qc == 0) when
    present. Pass freq (e.g. "1min") to reindex onto a regular grid so gaps
    plot as gaps rather than interpolated lines.
    """
    import glob
    import pandas as pd
    import xarray as xr
    files = sorted(glob.glob(str(pathlib.Path(ds_dir) / "*")))
    if not files:
        raise FileNotFoundError("no files in %s" % ds_dir)
    data = xr.open_mfdataset(files, combine="nested", concat_dim="time",
                             drop_variables=["base_time", "time_offset"])
    columns = {}
    for var in variables:
        if var not in data:
            continue
        arr = data[var]
        qc_name = "qc_" + var
        if apply_qc and qc_name in data:
            arr = arr.where(data[qc_name] == 0)
        columns[var] = arr.to_series()
    data.close()
    frame = pd.DataFrame(columns).sort_index()
    if freq is not None:
        frame = frame.reindex(pd.date_range(frame.index.min(),
                                            frame.index.max(), freq=freq))
    return frame


def facility_geometry(met_frames_dir, site_lon, site_lat):
    """Range (km) and bearing (deg) of each facility from a reference point.

    met_frames_dir maps facility -> a directory of that facility's met files;
    lat/lon are read from the first file. Supplementary facilities can sit tens
    of km apart, which drives spatial differences in convective rainfall.
    """
    import glob
    import numpy as np
    import xarray as xr
    out = {}
    for fac, ds_dir in met_frames_dir.items():
        files = sorted(glob.glob(str(pathlib.Path(ds_dir) / "*")))
        if not files:
            continue
        data = xr.open_dataset(files[0])
        lon = float(np.asarray(data["lon"].values).ravel()[0])
        lat = float(np.asarray(data["lat"].values).ravel()[0])
        data.close()
        dx = (lon - site_lon) * 111.32 * np.cos(np.deg2rad(site_lat))
        dy = (lat - site_lat) * 110.57
        out[fac] = {"lon": lon, "lat": lat,
                    "range_km": float(np.hypot(dx, dy)),
                    "bearing_deg": float(np.degrees(np.arctan2(dx, dy)) % 360)}
    return out


def week_overview_figure(met_by_facility, precip_rate=None, cloud_base=None,
                         pbl=None, radiation=None, mwr=None, colors=None,
                         figsize=(11.0, 10.6)):
    """Six-panel week overview on a shared time axis.

    met_by_facility maps facility -> DataFrame with temp_mean,
    wspd_arith_mean and tbrg_precip_total_corr. The other arguments are
    optional Series/DataFrames: precip_rate (1-min rain rate), cloud_base
    (m AGL), pbl (m AGL), radiation (W/m2), mwr (columns pwv, lwp).
    Returns (fig, axes) so panels can be relabelled before saving.
    """
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    if colors is None:
        colors = {}
    palette = ["#1b3a6b", "#c1666b", "#3f8f6b", "#d99a2b", "#6b4a8f"]
    facilities = list(met_by_facility)
    for i, fac in enumerate(facilities):
        colors.setdefault(fac, palette[i % len(palette)])

    fig = plt.figure(figsize=figsize)
    heights = [0.148, 0.128, 0.118, 0.118, 0.128, 0.118]
    axes = []
    y = 0.945
    for height in heights:
        y -= height
        axes.append(fig.add_axes([0.075, y, 0.845, height]))
        y -= 0.023

    for fac, frame in met_by_facility.items():
        if "temp_mean" in frame:
            axes[0].plot(frame.index, frame["temp_mean"], lw=0.8, color=colors[fac])
        if "tbrg_precip_total_corr" in frame:
            axes[1].plot(frame.index,
                         frame["tbrg_precip_total_corr"].fillna(0).cumsum(),
                         lw=1.4, color=colors[fac])
        if "wspd_arith_mean" in frame:
            axes[2].plot(frame.index, frame["wspd_arith_mean"], lw=0.7,
                         color=colors[fac])
    axes[0].set_ylabel("Air temp (°C)")
    axes[1].set_ylabel("Cumulative\nrain (mm)")
    axes[2].set_ylabel("Wind speed\n(m s$^{-1}$)")
    for i, fac in enumerate(facilities):
        axes[0].text(1.004, 0.86 - 0.13 * i, fac, transform=axes[0].transAxes,
                     color=colors[fac], fontsize=8, va="center")

    if precip_rate is not None:
        twin = axes[1].twinx()
        twin.plot(precip_rate.index, precip_rate, lw=0.5, color="#8a8a8a",
                  alpha=0.85, zorder=0)
        twin.set_ylabel("Rain rate\n(mm h$^{-1}$)", color="#8a8a8a")
        twin.tick_params(colors="#8a8a8a")
        twin.spines["right"].set_color("#8a8a8a")
    if radiation is not None:
        axes[3].plot(radiation.index, radiation, lw=0.6, color="#d99a2b")
    axes[3].set_ylabel("Downwelling\nSW (W m$^{-2}$)")
    if cloud_base is not None:
        axes[4].plot(cloud_base.index, cloud_base / 1000.0, ls="none", marker=".",
                     ms=1.0, color="#4a4a4a", alpha=0.45)
    if pbl is not None:
        axes[4].plot(pbl.index, pbl / 1000.0, marker="o", ms=4, lw=1.0,
                     color="#c1666b")
    axes[4].set_ylabel("Height (km AGL)")
    if mwr is not None:
        axes[5].plot(mwr.index, mwr["pwv"], lw=0.9, color="#1b3a6b")
        axes[5].set_ylabel("PWV (cm)")
        twin2 = axes[5].twinx()
        twin2.plot(mwr.index, mwr["lwp"].clip(lower=0), lw=0.6, color="#3f8f6b",
                   alpha=0.85)
        twin2.set_ylabel("LWP (mm)", color="#3f8f6b")
        twin2.tick_params(colors="#3f8f6b")
        twin2.spines["right"].set_color("#3f8f6b")

    for ax in axes:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18]))
        ax.grid(axis="x", color="0.9", lw=0.6)
        if ax is not axes[-1]:
            ax.set_xticklabels([])
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    axes[-1].set_xlabel("UTC")
    return fig, axes


def daily_summary(met_by_facility, precip_rate=None, radiation=None, mwr=None,
                  cloud_base=None):
    """Daily aggregate table across the survey streams.

    Returns a DataFrame indexed by date with per-facility rain totals, daily
    temperature range, peak and integrated shortwave, mean PWV, peak LWP and
    ceilometer cloudy fraction.
    """
    import pandas as pd
    temps = pd.concat([f["temp_mean"] for f in met_by_facility.values()
                       if "temp_mean" in f], axis=1)
    cols = {"T_max_C": temps.max(axis=1).resample("1D").max(),
            "T_min_C": temps.min(axis=1).resample("1D").min()}
    for fac, frame in met_by_facility.items():
        if "tbrg_precip_total_corr" in frame:
            cols["rain_%s_mm" % fac] = (frame["tbrg_precip_total_corr"]
                                        .fillna(0).resample("1D").sum())
    if precip_rate is not None:
        cols["peak_rainrate_mmh"] = precip_rate.resample("1D").max()
    if radiation is not None:
        cols["SW_peak_Wm2"] = radiation.resample("1D").max()
        cols["SW_daily_MJm2"] = (radiation.clip(lower=0).resample("1D").sum()
                                 * 60 / 1e6)
    if mwr is not None:
        cols["PWV_mean_cm"] = mwr["pwv"].resample("1D").mean()
        cols["LWP_max_mm"] = mwr["lwp"].resample("1D").max()
    if cloud_base is not None:
        cols["cloudy_frac"] = cloud_base.notna().resample("1D").mean()
    table = pd.DataFrame(cols)
    table.index = table.index.date
    return table
