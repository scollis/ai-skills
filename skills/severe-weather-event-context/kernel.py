"""Helpers for severe-weather event case studies and climatological context.

Each function here encodes a trap that cost real debugging time. Thin wrappers
around one API call live in SKILL.md instead.
"""
import numpy as np
import pandas as pd

IEM = "https://mesonet.agron.iastate.edu"
DAT_FS = ("https://services.dat.noaa.gov/arcgis/rest/services/"
          "nws_damageassessmenttoolkit/DamageViewer/FeatureServer")


def iem_storm_reports(start, end, wfos=None):
    """NWS local storm reports. wfos e.g. ['LOT','MKX']. Times are UTC."""
    import io, requests
    if wfos is None:
        wfos = ["LOT"]
    q = "&".join("wfo[]=" + w for w in wfos)
    u = (IEM + "/cgi-bin/request/gis/lsr.py?sts=" + pd.Timestamp(start).strftime("%Y-%m-%dT%H:%MZ")
         + "&ets=" + pd.Timestamp(end).strftime("%Y-%m-%dT%H:%MZ") + "&" + q + "&fmt=csv")
    d = pd.read_csv(io.StringIO(requests.get(u, timeout=180).text))
    if "VALID" in d.columns:
        d["VALID"] = pd.to_datetime(d.VALID, format="%Y%m%d%H%M", utc=True)
    return d


def iem_asos(station, start, end, extra=None):
    """ASOS observations. Returns tz-naive UTC 'valid' plus requested fields.

    NOTE p01i is a RUNNING hourly accumulation repeated at each observation --
    summing it double-counts. Use asos_hourly_precip() for totals.
    """
    import io, requests
    fields = ["tmpf", "dwpf", "sknt", "drct", "gust", "mslp", "p01i", "skyc1", "wxcodes"]
    if extra:
        fields = fields + [f for f in extra if f not in fields]
    u = (IEM + "/cgi-bin/request/asos.py?station=" + station
         + "".join("&data=" + f for f in fields)
         + "&tz=UTC&sts=" + pd.Timestamp(start).strftime("%Y-%m-%dT%H:%MZ")
         + "&ets=" + pd.Timestamp(end).strftime("%Y-%m-%dT%H:%MZ")
         + "&format=onlycomma&missing=M")
    d = pd.read_csv(io.StringIO(requests.get(u, timeout=180).text), na_values=["M", ""])
    if "valid" in d.columns:
        d["valid"] = pd.to_datetime(d.valid)
    return d


def asos_hourly_precip(df):
    """Correct storm-total precip from ASOS. p01i repeats a running hourly
    accumulation, so take the max within each clock hour and sum those."""
    d = df.dropna(subset=["p01i"]).copy()
    if not len(d):
        return 0.0
    return float(d.set_index("valid").p01i.resample("1h").max().sum())


def iem_raob(station, start, end):
    """Radiosondes, one row per level. A whole month is a single request.

    The Wyoming CGI endpoint has moved and 404s; use this. `end` must be
    STRICTLY later than `start` or the query returns nothing.
    """
    import io, requests
    u = (IEM + "/cgi-bin/request/raob.py?station=" + station
         + "&sts=" + pd.Timestamp(start).strftime("%Y-%m-%dT%H:%MZ")
         + "&ets=" + pd.Timestamp(end).strftime("%Y-%m-%dT%H:%MZ") + "&fmt=csv")
    d = pd.read_csv(io.StringIO(requests.get(u, timeout=300).text), na_values=["M", ""])
    if "validUTC" in d.columns:
        d["validUTC"] = pd.to_datetime(d.validUTC)
    return d


def pwat_mm(pressure_hpa, dewpoint_c, ptop=300.0):
    """Precipitable water by integrating q over p. Agrees with
    metpy.calc.precipitable_water to <1 mm. Needs a surface-based profile."""
    p = np.asarray(pressure_hpa, dtype=float)
    td = np.asarray(dewpoint_c, dtype=float)
    m = np.isfinite(p) & np.isfinite(td)
    p, td = p[m], td[m]
    if p.size < 5:
        return float("nan")
    o = np.argsort(-p)
    p, td = p[o], td[o]
    keep = p >= ptop
    p, td = p[keep], td[keep]
    if p.size < 5 or p[0] < 800:
        return float("nan")
    e = 6.112 * np.exp(17.67 * td / (td + 243.5))
    w = 0.622 * e / (p - e)
    q = w / (1.0 + w)
    return float(-np.trapezoid(q, p * 100.0) / (1000.0 * 9.80665) * 1000.0)


def pct_rank(series, value):
    """Weak percentile rank and rank, handling TIES correctly.

    rank counts values >= value; percentile is the share <= value. With integer
    counts (days >=90F, wet days) many years tie, so rank and percentile are NOT
    reciprocal and the naive (n-rank+1)/n formula is wrong. Returns a dict with
    n_above / n_tied / is_record so a 100th percentile can be explained.
    """
    s = pd.Series(series).dropna().astype(float)
    v = float(value)
    n = len(s)
    return {"n": n,
            "rank": int((s >= v).sum()),
            "percentile": float((s <= v).mean() * 100.0),
            "n_above": int((s > v).sum()),
            "n_tied": int((s == v).sum()),
            "n_below": int((s < v).sum()),
            "is_record": bool((s > v).sum() == 0)}


def trend_screen(years, values, alpha=0.05):
    """OLS trend per decade with a significance gate. Draw a trend line on a
    figure ONLY where significant is True -- a few decades at one station is
    usually too short to separate trend from variability."""
    from scipy import stats
    x = np.asarray(years, dtype=float)
    y = np.asarray(values, dtype=float)
    m = np.isfinite(x) & np.isfinite(y)
    r = stats.linregress(x[m], y[m])
    return {"per_decade": float(r.slope * 10.0), "pvalue": float(r.pvalue),
            "r": float(r.rvalue), "n": int(m.sum()),
            "significant": bool(r.pvalue < alpha),
            "intercept": float(r.intercept), "slope": float(r.slope)}


def ivt(q, u, v, levels_hpa, g=9.80665):
    """Integrated vapour transport (kg m-1 s-1) from (level, y, x) stacks.

    Levels may ascend or descend in index; the sign is fixed internally. Above
    ~250 is atmospheric-river magnitude. VALIDATE by checking the flux vector
    direction against the 850 hPa wind at the same point.
    """
    p = np.asarray(levels_hpa, dtype=float) * 100.0
    o = np.argsort(-p)
    p = p[o]
    qu = np.trapezoid(np.asarray(q)[o] * np.asarray(u)[o], p, axis=0) / g * -1.0
    qv = np.trapezoid(np.asarray(q)[o] * np.asarray(v)[o], p, axis=0) / g * -1.0
    return qu, qv, np.hypot(qu, qv)


def back_trajectory(lat0, lon0, t_end, times, lat_1d, lon_1d, u_cube, v_cube,
                    q_cube=None, hours=96, dt_h=1.0):
    """Isobaric RK2 back trajectory on a (time, lat, lon) cube.

    lat_1d may descend (GFS does); it is flipped internally along with the cubes.
    Returns (timestamps, lats, lons, q). Isobaric means constant-pressure, not
    true 3-D motion -- fine to attribute a source region over a few days, but do
    not over-read the exact path.
    """
    from scipy.interpolate import RegularGridInterpolator
    la1 = np.asarray(lat_1d, dtype=float)
    flip = la1[0] > la1[-1]
    if flip:
        la1 = la1[::-1]
    tn = np.array([pd.Timestamp(t).value / 1e9 for t in times], dtype=float)

    def mk(cube):
        c = np.asarray(cube, dtype=float)
        return RegularGridInterpolator((tn, la1, np.asarray(lon_1d, dtype=float)),
                                       c[:, ::-1, :] if flip else c,
                                       bounds_error=False, fill_value=np.nan)

    fu, fv = mk(u_cube), mk(v_cube)
    fq = mk(q_cube) if q_cube is not None else None
    t = pd.Timestamp(t_end).value / 1e9
    la, lo = float(lat0), float(lon0)
    T, LA, LO, Q = [t], [la], [lo], [float(fq([[t, la, lo]])[0]) if fq else np.nan]
    for _ in range(int(hours / dt_h)):
        dt = dt_h * 3600.0
        u1 = float(fu([[t, la, lo]])[0]); v1 = float(fv([[t, la, lo]])[0])
        if not np.isfinite(u1):
            break
        lam = la - v1 * dt / 2 / 111000.0
        lom = lo - u1 * dt / 2 / (111000.0 * np.cos(np.radians(la)))
        u2 = float(fu([[t - dt / 2, lam, lom]])[0])
        v2 = float(fv([[t - dt / 2, lam, lom]])[0])
        if not np.isfinite(u2):
            u2, v2 = u1, v1
        la = la - v2 * dt / 111000.0
        lo = lo - u2 * dt / (111000.0 * np.cos(np.radians(la)))
        t = t - dt
        if not (la1.min() < la < la1.max()):
            break
        T.append(t); LA.append(la); LO.append(lo)
        Q.append(float(fq([[t, la, lo]])[0]) if fq else np.nan)
    return ([pd.Timestamp(int(x * 1e9)) for x in T],
            np.array(LA), np.array(LO), np.array(Q) * (1000.0 if fq else 1.0))


def bowen(lh, sh, min_net=20.0):
    """Bowen ratio SH/LH and evaporative fraction LH/(LH+SH).

    EF can exceed 1 where SH is slightly NEGATIVE (downward sensible heat over a
    wet surface cooler than the air) -- physically real but ill-behaved, so
    ef_clipped is provided for display and the Bowen ratio is the robust metric.
    """
    lh = np.asarray(lh, dtype=float); sh = np.asarray(sh, dtype=float)
    net = lh + sh
    ef = np.where(np.abs(net) > min_net, lh / np.where(net == 0, np.nan, net), np.nan)
    return {"bowen": sh / np.where(lh == 0, np.nan, lh),
            "ef": ef, "ef_clipped": np.clip(ef, 0.0, 1.0)}


def dat_tornado_tracks(wfo, date, layer=1):
    """NWS-surveyed tornado damage paths with full polyline geometry.

    Layer 1 = Damage Lines (efscale, starttime/endtime in epoch ms, length,
    width, maxwind). Layer 0 = damage points, often empty. The public viewer at
    apps.dat.noaa.gov is a JS app whose REST paths 404 -- this services host is
    the working one. Returns a GeoJSON FeatureCollection dict.
    """
    import requests
    d = pd.Timestamp(date).strftime("%Y-%m-%d")
    nxt = (pd.Timestamp(date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")
    q = {"where": ("wfo='" + wfo + "' AND stormdate >= DATE '" + d
                   + "' AND stormdate <= DATE '" + nxt + "'"),
         "outFields": "*", "f": "geojson", "returnGeometry": "true", "outSR": "4326"}
    return requests.get(DAT_FS + "/" + str(layer) + "/query", params=q, timeout=120).json()


def nws_flood_gauges(product_ids):
    """Gauge identity, official flood stage and forecast crest from FLW text.

    The IEM nwsli.json endpoint 404s for these IDs and guessing a river name
    from the code gets it wrong. One FLW product covers SEVERAL rivers, so it
    must be split per gauge segment.
    """
    import re, requests
    out = []
    for pid in list(dict.fromkeys(product_ids)):
        txt = requests.get(IEM + "/api/1/nwstext/" + str(pid), timeout=90).text
        flat = re.sub(r"\s+", " ", txt)
        for seg in re.split(r"(?=&&)", flat):
            nm = re.search(r"(?i)((?:[A-Z][a-z]+ )+(?:Creek|River)(?: at [A-Z][a-z]+)?)", seg)
            fs = re.search(r"(?i)Flood stage is ([\d.]+) f", seg)
            if not (nm and fs):
                continue
            ob = re.search(r"(?i)stage was ([\d.]+) f", seg)
            cr = re.search(r"(?i)crest of ([\d.]+) f", seg)
            nwsli = re.search(r"/([A-Z]{4}\d)\.", seg)
            out.append({"product_id": pid, "nwsli": nwsli.group(1) if nwsli else None,
                        "name": nm.group(1).strip(), "flood_stage_ft": float(fs.group(1)),
                        "observed_ft": float(ob.group(1)) if ob else None,
                        "forecast_crest_ft": float(cr.group(1)) if cr else None})
    return pd.DataFrame(out)


def hads_river_stage(nwsli, start, end, network="IL_DCP"):
    """River stage time series (HG* columns are gauge height in feet)."""
    import io, requests
    u = (IEM + "/cgi-bin/request/hads.py?network=" + network + "&stations=" + nwsli
         + "&sts=" + pd.Timestamp(start).strftime("%Y-%m-%dT%H:%MZ")
         + "&ets=" + pd.Timestamp(end).strftime("%Y-%m-%dT%H:%MZ") + "&what=txt")
    d = pd.read_csv(io.StringIO(requests.get(u, timeout=180).text))
    if "utc_valid" in d.columns:
        d["utc_valid"] = pd.to_datetime(d.utc_valid, utc=True)
    return d
