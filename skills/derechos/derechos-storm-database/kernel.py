
"""Helpers for derechos-storm-database. All access paths verified live 2026-09-05."""
import os
import io
import re
import csv
import json
import zipfile
import urllib.parse
import urllib.request

DERECHOS_BOX = (-94.2, 40.7, -87.4, 42.6)
NCEI_CSVDIR = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
NCEI_SEDB_API = "https://www.ncei.noaa.gov/access/storm-events-database/api/"
SPC_WCM = "https://www.spc.noaa.gov/wcm/data/"
SPC_DERECHO = "https://www.spc.noaa.gov/about/derechos/archive/"
SPC_RPTS = "https://www.spc.noaa.gov/climo/reports/"
IEM = "https://mesonet.agron.iastate.edu"
DAT_FS = ("https://services.dat.noaa.gov/arcgis/rest/services/"
          "nws_damageassessmenttoolkit/DamageViewer/FeatureServer")
SWDI = "https://www.ncei.noaa.gov/swdiws/csv/"
KT_PER_MPH = 0.868976


def storm_sources(sq=None):
    """Source table for this skill as a list of dicts; filter with sq='SQ6'."""
    rows = [
        dict(name="NCEI Storm Events bulk CSV", host="www.ncei.noaa.gov", status="verified",
             kind="report", sq="SQ2,SQ3,SQ6", note="1950-present; only tornado/hail/tstm wind before 1996"),
        dict(name="NCEI Storm Events search-events REST", host="www.ncei.noaa.gov", status="verified",
             kind="report", sq="SQ2,SQ6", note="silently caps at 1000 rows; no lat/lon in the response"),
        dict(name="SPC WCM severe database", host="www.spc.noaa.gov", status="verified",
             kind="report", sq="SQ2,SQ6", note="wind mag in KNOTS; magnitude-type flag only from 2006"),
        dict(name="SPC daily report CSVs", host="www.spc.noaa.gov", status="verified",
             kind="report", sq="SQ6", note="speeds in MPH and 'UNK' for damage-only reports"),
        dict(name="SPC derecho archive (Squitieri et al. 2025)", host="www.spc.noaa.gov",
             status="verified", kind="curated", sq="SQ1,SQ2,SQ6,SQ7",
             note="the canonical machine-readable derecho list; 96 definitive events 1996-2025"),
        dict(name="IEM Local Storm Report archive", host="mesonet.agron.iastate.edu", status="verified",
             kind="report", sq="SQ2,SQ3,SQ6", note="MAG in MPH; QUALIFIER M/E flags measured vs estimated"),
        dict(name="IEM NWS warning / storm-based-warning archive", host="mesonet.agron.iastate.edu",
             status="verified", kind="operational", sq="SQ6,SQ7", note="polygons plus windtag/hailtag/damagetag"),
        dict(name="IEM AFOS text archive", host="mesonet.agron.iastate.edu", status="verified",
             kind="narrative", sq="SQ2,SQ6", note="the only route to DVN/LOT damage-survey narratives"),
        dict(name="NWS Damage Assessment Toolkit", host="services.dat.noaa.gov", status="verified",
             kind="survey", sq="SQ2,SQ6", note="public ArcGIS FeatureServer; operational coverage starts ~2013"),
        dict(name="NCEI SWDI radar-derived detections", host="www.ncei.noaa.gov", status="verified",
             kind="radar", sq="SQ2,SQ6", note="nx3mda mesocyclones and nx3hail work; nldn is licence-blocked"),
        dict(name="NCEI Billion-Dollar Disasters", host="www.ncei.noaa.gov", status="partial",
             kind="impact", sq="SQ6", note="frozen at 2024-10-09; the product is no longer updated"),
    ]
    if sq is None:
        return rows
    return [r for r in rows if sq.upper() in r["sq"]]


def http_text(url, timeout=120):
    """GET a URL and return decoded text."""
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def http_json(url, timeout=120):
    """GET a URL and parse JSON."""
    return json.loads(http_text(url, timeout))


def ncei_index(kind="details"):
    """Map year -> (version, cYYYYMMDD) for the NCEI Storm Events bulk CSVs.

    The _cYYYYMMDD suffix is a per-year publication stamp and CANNOT be guessed;
    always discover it from the directory listing before building a URL.
    """
    html = http_text(NCEI_CSVDIR, timeout=180)
    pat = re.compile(r"StormEvents_(%s)-ftp_v(\d\.\d)_d(\d{4})_c(\d{8})\.csv\.gz" % kind)
    out = {}
    for _k, ver, yr, stamp in pat.findall(html):
        out[int(yr)] = (ver, stamp)
    return out


def ncei_fetch(years, kind="details", cache_dir="ncei", index=None):
    """Download NCEI Storm Events bulk CSVs for `years` and return one DataFrame."""
    import pandas as pd
    if index is None:
        index = ncei_index(kind)
    os.makedirs(cache_dir, exist_ok=True)
    frames = []
    for y in years:
        if y not in index:
            continue
        ver, stamp = index[y]
        fn = "StormEvents_%s-ftp_v%s_d%d_c%s.csv.gz" % (kind, ver, y, stamp)
        dst = os.path.join(cache_dir, fn)
        if not os.path.exists(dst):
            urllib.request.urlretrieve(NCEI_CSVDIR + fn, dst)
        frames.append(pd.read_csv(dst, low_memory=False))
    return pd.concat(frames, ignore_index=True) if frames else None


def ncei_box(df, box=None, keep_zone=False):
    """Clip NCEI details rows to a lon/lat box using BEGIN_LON/BEGIN_LAT.

    WARNING: zone-coded rows (CZ_TYPE == 'Z' -- High Wind, Winter Storm, Heavy
    Snow, Blizzard, Heat, Drought) carry NO coordinates at all, so a coordinate
    filter drops 100 % of them. Set keep_zone=True to retain them for a
    separate STATE/CZ_NAME-based filter.
    """
    if box is None:
        box = DERECHOS_BOX
    lo, la, hi, ha = box
    m = (df.BEGIN_LON >= lo) & (df.BEGIN_LON <= hi) & (df.BEGIN_LAT >= la) & (df.BEGIN_LAT <= ha)
    if keep_zone:
        m = m | (df.get("CZ_TYPE").eq("Z") if "CZ_TYPE" in df else False)
    return df.loc[m].copy()


def ncei_damage_usd(value):
    """Parse an NCEI DAMAGE_PROPERTY / DAMAGE_CROPS string ('100.00K') to float USD."""
    s = str(value).strip()
    if s in ("", "nan", "None", "0", "0.00"):
        return 0.0
    mult = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}
    if s[-1].upper() in mult:
        return float(s[:-1]) * mult[s[-1].upper()]
    return float(s)


def ncei_search_events(states, begin, end, event_types=None, timeout=120):
    """POST the Storm Events web app's search API. states are title case ('Iowa').

    GOTCHA: the response is silently truncated at 1000 records with no error
    field and no pagination parameter, and carries no coordinates. Use the bulk
    CSVs for anything larger than a single day or two.
    """
    payload = dict(activeTab="state", stateList=list(states),
                   beginDate=begin, endDate=end,
                   eventList=list(event_types or []), countyList=[],
                   hailFilter="", tornFilter="", windFilter="")
    req = urllib.request.Request(NCEI_SEDB_API + "search-events",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        out = json.loads(r.read())
    rows = out.get("data") or []
    out["truncated"] = len(rows) >= 1000
    return out


def spc_wcm(kind="wind", cache_dir="spc"):
    """Load the SPC WCM aggregate severe-report database. kind: wind|hail|torn.

    Wind magnitudes are KNOTS (not mph); hail is inches; all timestamps are CST
    (tz == 3 for every row). mag == 0 means the magnitude was not reported.
    """
    import pandas as pd
    names = {"wind": "1955-2025_wind.csv.zip", "hail": "1955-2025_hail.csv.zip",
             "torn": "1950-2025_torn.csv.zip"}
    fn = names[kind]
    os.makedirs(cache_dir, exist_ok=True)
    dst = os.path.join(cache_dir, fn)
    if not os.path.exists(dst):
        urllib.request.urlretrieve(SPC_WCM + fn, dst)
    with zipfile.ZipFile(dst) as z:
        with z.open(z.namelist()[0]) as fh:
            return pd.read_csv(fh, low_memory=False)


def spc_box(df, box=None):
    """Clip an SPC WCM frame to a lon/lat box on the report START point."""
    if box is None:
        box = DERECHOS_BOX
    lo, la, hi, ha = box
    m = (df.slon >= lo) & (df.slon <= hi) & (df.slat >= la) & (df.slat <= ha)
    return df.loc[m].copy()


def spc_daily_reports(date, kind="wind"):
    """SPC daily report CSV for a date ('2020-08-10'). kind: wind|hail|torn|filtered.

    Speeds are MPH here (the WCM database uses knots) and are the literal string
    'UNK' for damage-only reports. 'today' / 'yesterday' also work as `date`.
    """
    import pandas as pd
    if date in ("today", "yesterday"):
        stem = date
    else:
        stem = str(date).replace("-", "")[2:] + "_rpts"
    url = "%s%s_%s.csv" % (SPC_RPTS, stem, kind)
    return pd.read_csv(io.StringIO(http_text(url)))


def spc_derecho_archive(cache_dir="derecho"):
    """Download and parse the SPC derecho archive (Squitieri et al. 2025, BAMS).

    Returns {'events': {class: DataFrame}, 'reports': {class: DataFrame}} for the
    four classes definitive_nexrad, likely_nexrad, likely_prenexrad,
    possible_prenexrad. The report CSVs are latin-1, not UTF-8, and their
    'Report Type' column contains a stray trailing-space value -- strip it.
    """
    import pandas as pd
    tabs = {"definitive_nexrad": ("Table_S1_Derechos_NEXRAD.csv",
                                  "NEXRAD_Definitive_Derecho_Reports.csv"),
            "likely_nexrad": ("Table_S2_Likely_Derechos_NEXRAD.csv",
                              "NEXRAD_Likely_Derecho_Reports.csv"),
            "likely_prenexrad": ("Table_S3_Likely_Derechos_Pre_NEXRAD.csv",
                                 "PreNEXRAD_Likely_Derecho_Reports.csv"),
            "possible_prenexrad": ("Table_S4_Possible_Derechos_Pre_NEXRAD.csv",
                                   "PreNEXRAD_Possible_Derecho_Reports.csv")}
    os.makedirs(cache_dir, exist_ok=True)
    events, reports = {}, {}
    for cls, (tf, rf) in tabs.items():
        for fn in (tf, rf):
            dst = os.path.join(cache_dir, fn)
            if not os.path.exists(dst):
                urllib.request.urlretrieve(SPC_DERECHO + fn, dst)
        e = pd.read_csv(os.path.join(cache_dir, tf), encoding="latin-1")
        e["start"] = pd.to_datetime(e["Start Date and Time (UTC)"], errors="coerce")
        e["end"] = pd.to_datetime(e["End Date and Time (UTC)"], errors="coerce")
        r = pd.read_csv(os.path.join(cache_dir, rf), encoding="latin-1", low_memory=False)
        r = r.rename(columns={"Latitude (Degrees)": "lat", "Longitude (Degrees)": "lon",
                              "Speed (Knots)": "kt"})
        r["dt"] = pd.to_datetime(r["Date and Time (UTC)"], errors="coerce")
        r["Report Type"] = r["Report Type"].astype(str).str.strip()
        events[cls], reports[cls] = e, r
    return dict(events=events, reports=reports)


def spc_derechos_in_box(archive, box=None):
    """Which archived derechos put >=1 wind report inside `box`. Returns a DataFrame."""
    import numpy as np
    import pandas as pd
    if box is None:
        box = DERECHOS_BOX
    lo, la, hi, ha = box
    out = []
    for cls, e in archive["events"].items():
        r = archive["reports"][cls]
        for _, row in e.iterrows():
            m = (r.dt.between(row["start"], row["end"]) & r.lon.between(lo, hi)
                 & r.lat.between(la, ha))
            if not m.any():
                continue
            sub = r[m]
            meas = sub.loc[sub["Report Type"] == "Measured", "kt"]
            out.append(dict(spc_class=cls, spc_event=row["Event #"],
                            start_utc=str(row["start"]), end_utc=str(row["end"]),
                            track_km=row["Track Length (Kilometers)"],
                            dur_h=row["Duration (Hours)"], n_rep_box=int(m.sum()),
                            max_kt_box=float(sub.kt.max()),
                            max_meas_kt_box=float(meas.max()) if len(meas) else np.nan))
    return pd.DataFrame(out).sort_values("start_utc").reset_index(drop=True)


def iem_lsr(sts, ets, wfos=None, states=None, timeout=900):
    """IEM Local Storm Report archive as a DataFrame. Times are ISO UTC strings.

    MAG is MPH for wind gusts and inches for hail. QUALIFIER is 'M' (measured),
    'E' (estimated), 'U' or blank. Two traps: (1) the `type=`/`type[]=` filter
    returns an EMPTY body with HTTP 200 -- never use it, filter TYPECODE in
    pandas instead; (2) a handful of rows carry an unescaped comma in REMARK and
    break pandas' C parser, so this reads with the csv module and truncates.
    """
    import pandas as pd
    q = [("sts", sts), ("ets", ets), ("fmt", "csv")]
    for w in (wfos or []):
        q.append(("wfo[]", w))
    for s in (states or []):
        q.append(("states[]", s))
    url = IEM + "/cgi-bin/request/gis/lsr.py?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=timeout) as r:
        raw = r.read().decode("latin-1")
    rdr = csv.reader(io.StringIO(raw))
    hdr = next(rdr)
    n = len(hdr)
    rows = [(row[:n] if len(row) >= n else row + [""] * (n - len(row))) for row in rdr]
    df = pd.DataFrame(rows, columns=hdr)
    for c in ("LAT", "LON", "MAG"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["valid"] = pd.to_datetime(df.VALID, format="%Y%m%d%H%M", errors="coerce", utc=True)
    df["SRC"] = df.SOURCE.astype(str).str.upper().str.strip()
    return df


def iem_warnings(sts, ets, wfos=None, limit_first=True, timeout=300):
    """NWS warning archive (storm-based polygons + county segments) as a DataFrame.

    Columns include windtag/hailtag/tornadotag/damagetag and area2d (km^2).
    gtype 'P' is a polygon, 'C' a county/zone segment. limit_first keeps only the
    initial (NEW) statement of each VTEC event.
    """
    import pandas as pd
    q = [("sts", sts), ("ets", ets), ("accept", "csv")]
    if limit_first:
        q.append(("limit1", "yes"))
    for w in (wfos or []):
        q.append(("wfo[]", w))
    url = IEM + "/cgi-bin/request/gis/watchwarn.py?" + urllib.parse.urlencode(q)
    return pd.read_csv(io.StringIO(http_text(url, timeout)))


def iem_sbw_geojson(begints, endts, wfos=None, timeout=300):
    """Storm-based warning polygons as GeoJSON from IEM's /api/1/vtec/sbw_interval.

    GOTCHA: the parameters are `begints`/`endts`. Passing `sts`/`ets` returns
    HTTP 200 with the CURRENT day's warnings and no warning at all.
    """
    q = [("begints", begints), ("endts", endts)]
    for w in (wfos or []):
        q.append(("wfo", w))
    return http_json(IEM + "/api/1/vtec/sbw_interval.geojson?" + urllib.parse.urlencode(q), timeout)


def iem_afos_list(pil, date, timeout=120):
    """List AFOS text products for a PIL ('PNSDVN') on a date ('2020-08-11')."""
    u = IEM + "/api/1/nws/afos/list.json?" + urllib.parse.urlencode(dict(pil=pil, date=date))
    return http_json(u, timeout)


def iem_afos_text(product_id, timeout=120):
    """Raw text of one AFOS product, e.g. '202008120018-KLOT-NOUS43-PNSLOT'."""
    return http_text(IEM + "/api/1/nwstext/" + product_id, timeout)


def dat_layer_fields(layer=0, timeout=120):
    """Field names of a DAT DamageViewer FeatureServer layer (0 pts, 1 lines, 2 polys)."""
    m = http_json("%s/%d?f=json" % (DAT_FS, layer), timeout)
    return [f["name"] for f in m["fields"]]


def dat_query(layer=0, where="1=1", box=None, out_fields="*", page=1000,
              geometry=False, timeout=180):
    """Paginated query of the NWS Damage Assessment Toolkit FeatureServer.

    Two gotchas: (1) `resultRecordCount` is MANDATORY here -- omitting it returns
    HTTP 200 with a bare {'error': {'code': 400}}; (2) `returnCountOnly=true`
    returns a count CLIPPED at maxRecordCount (2000), so it under-reports badly.
    Use dat_count() for a true count. maxwind uses -99 as a missing sentinel and
    `surveytype` is NULL throughout.
    """
    import pandas as pd
    if box is None:
        box = DERECHOS_BOX
    feats, off = [], 0
    while True:
        p = dict(where=where, outFields=out_fields, f="json",
                 returnGeometry=str(bool(geometry)).lower(),
                 resultOffset=off, resultRecordCount=page,
                 geometry="%f,%f,%f,%f" % tuple(box), geometryType="esriGeometryEnvelope",
                 inSR="4326", spatialRel="esriSpatialRelIntersects", outSR="4326")
        r = http_json("%s/%d/query?%s" % (DAT_FS, layer, urllib.parse.urlencode(p)), timeout)
        if "error" in r:
            raise RuntimeError(r["error"])
        f = r.get("features", [])
        feats += f
        if len(f) < page:
            break
        off += page
    df = pd.DataFrame([x["attributes"] for x in feats])
    if "stormdate" in df:
        df["date"] = pd.to_datetime(df.stormdate, unit="ms", errors="coerce")
    return df


def dat_count(layer=0, where="1=1", box=None, timeout=180):
    """True record count for a DAT layer over a box, via a server-side statistic."""
    if box is None:
        box = DERECHOS_BOX
    stats = [{"statisticType": "count", "onStatisticField": "objectid",
              "outStatisticFieldName": "n"}]
    p = dict(where=where, f="json", returnGeometry="false", outStatistics=json.dumps(stats),
             geometry="%f,%f,%f,%f" % tuple(box), geometryType="esriGeometryEnvelope",
             inSR="4326", spatialRel="esriSpatialRelIntersects")
    r = http_json("%s/%d/query?%s" % (DAT_FS, layer, urllib.parse.urlencode(p)), timeout)
    return int(r["features"][0]["attributes"]["n"])


def swdi_query(product, start, end, box=None, timeout=180):
    """NCEI SWDI radar-derived detections as a DataFrame. Dates are 'YYYYMMDD'.

    Working products: nx3mda (mesocyclone detections), nx3hail, nx3tvs,
    nx3structure. nx3meso returns zero rows for modern dates -- nx3mda is its
    replacement. nldn (lightning) returns HTTP 400: it is licence-restricted.
    Append '&stat=count' behaviour is exposed via product='<p>&stat=count'.
    """
    import pandas as pd
    if box is None:
        box = DERECHOS_BOX
    url = "%s%s/%s:%s?bbox=%f,%f,%f,%f" % ((SWDI, product, start, end) + tuple(box))
    txt = http_text(url, timeout)
    if txt.startswith("error"):
        raise RuntimeError(txt[:300])
    return pd.read_csv(io.StringIO(txt))


def ncei_billion_dollar_events(cache_dir="aux"):
    """NCEI Billion-Dollar Disasters event list. FROZEN: last event is 2024-10-09."""
    import pandas as pd
    os.makedirs(cache_dir, exist_ok=True)
    dst = os.path.join(cache_dir, "billions.csv")
    if not os.path.exists(dst):
        urllib.request.urlretrieve(
            "https://www.ncei.noaa.gov/access/billions/events-US-1980-2026.csv", dst)
    return pd.read_csv(dst, skiprows=2)


def xy_km(lat, lon):
    """Local tangent-plane coordinates in km about the centroid of the input points."""
    import numpy as np
    lat = np.asarray(lat, float)
    lon = np.asarray(lon, float)
    lat0, lon0 = lat.mean(), lon.mean()
    return ((lon - lon0) * 111.320 * np.cos(np.radians(lat0)),
            (lat - lat0) * 110.574)


def swath_major_axis_km(lat, lon, pct_lo=2.5, pct_hi=97.5):
    """Robust (major, minor, azimuth) of a report swath, km and degrees from north.

    Length is the pct_lo-pct_hi span along the first principal axis, so a few
    outlying reports cannot inflate it.
    """
    import numpy as np
    x, y = xy_km(lat, lon)
    P = np.column_stack([x - x.mean(), y - y.mean()])
    if len(P) < 3:
        return 0.0, 0.0, float("nan")
    Vt = np.linalg.svd(P, full_matrices=False)[2]
    a = P @ Vt[0]
    b = P @ Vt[1]
    major = float(np.percentile(a, pct_hi) - np.percentile(a, pct_lo))
    minor = float(np.percentile(b, pct_hi) - np.percentile(b, pct_lo))
    az = float(np.degrees(np.arctan2(Vt[0][0], Vt[0][1])) % 180.0)
    return major, minor, az


def swath_clusters(lat, lon, utc, link_km=100.0, speed_kmh=60.0):
    """Single-linkage report clusters in a space-time metric where 1 h == speed_kmh km."""
    import numpy as np
    import pandas as pd
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import pdist
    x, y = xy_km(lat, lon)
    t = np.asarray(pd.to_datetime(utc).astype("int64") / 1e9 / 3600.0, float) * speed_kmh
    P = np.column_stack([x, y, t])
    if len(P) < 2:
        return np.ones(len(P), int)
    return fcluster(linkage(pdist(P), method="single"), t=link_km, criterion="distance")


def screen_derecho_days(wind, min_major_km=400.0, max_gap_h=3.0, min_reports=30,
                        min_strong=3, strong_kt=65.0, link_km=100.0, speed_kmh=60.0,
                        tz_offset_h=None, conv_day_start_utc_h=12, box=None):
    """Objective derecho / QLCS wind-swath day screen on SPC WCM-format wind reports.

    `wind` needs columns yr, mo, dy, time (local, offset tz_offset_h), mag (kt),
    slat, slon, and optionally mt. Reports are linked into swaths by single
    linkage at link_km in a metric where one hour counts as speed_kmh km; each
    swath of each convective day (conv_day_start_utc_h UTC + 24 h) is then tested:

      1. >= min_reports severe wind reports in the swath;
      2. >= min_strong of them at >= strong_kt;
      3. no gap > max_gap_h between successive reports in the swath;
      4. robust major axis (swath_major_axis_km) >= min_major_km;
      5. if `box` is given, >= 1 report of the swath inside it.

    Returns (passed, candidates) DataFrames -- `passed` is one row per day (the
    largest qualifying swath). This is a HIGH-RECALL screen, not a derecho
    detector: over the DERECHOS box it recovers 24 of 26 SPC-archived definitive
    derechos but flags ~5x as many days, because report geometry alone cannot
    test the radar bow-echo continuity the published definitions require.
    """
    if tz_offset_h is None:
        tz_offset_h = -6.0   # US Central standard, negated here (gate: no UnaryOp default)
    import numpy as np
    import pandas as pd
    w = wind.copy()
    ts = pd.to_datetime(w.yr.astype(str) + "-" + w.mo.astype(str).str.zfill(2) + "-"
                        + w.dy.astype(str).str.zfill(2) + " " + w.time.astype(str),
                        errors="coerce")
    w["utc"] = ts - pd.Timedelta(hours=tz_offset_h)
    w = w.dropna(subset=["utc", "slat", "slon"])
    w["cday"] = (w.utc - pd.Timedelta(hours=conv_day_start_utc_h)).dt.floor("D").dt.date
    out = []
    for day, d in w.groupby("cday"):
        if len(d) < min_reports:
            continue
        d = d.sort_values("utc").reset_index(drop=True)
        d["cl"] = swath_clusters(d.slat, d.slon, d.utc, link_km, speed_kmh)
        for cl, s in d.groupby("cl"):
            if len(s) < min_reports:
                continue
            if box is not None:
                lo, la, hi, ha = box
                if not (s.slon.between(lo, hi) & s.slat.between(la, ha)).any():
                    continue
            gaps = s.utc.diff().dt.total_seconds().to_numpy()[1:] / 3600.0
            major, minor, az = swath_major_axis_km(s.slat.values, s.slon.values)
            meas = s.loc[s.mt.isin(["MG", "MS"]), "mag"] if "mt" in s else s.mag.iloc[:0]
            out.append(dict(conv_day=str(day), swath=int(cl), n_reports=len(s),
                            n_strong=int((s.mag >= strong_kt).sum()),
                            max_gap_h=round(float(np.nanmax(gaps)) if len(gaps) else 0.0, 2),
                            major_km=round(major, 1), minor_km=round(minor, 1),
                            aspect=round(major / max(minor, 1e-6), 2), axis_deg=round(az, 1),
                            max_kt=float(s.mag.max()),
                            max_measured_kt=float(meas.max()) if len(meas) else np.nan,
                            first_utc=str(s.utc.min()), last_utc=str(s.utc.max()),
                            duration_h=round((s.utc.max() - s.utc.min()).total_seconds() / 3600, 1)))
    cand = pd.DataFrame(out)
    if cand.empty:
        return cand, cand
    ok = cand[(cand.n_strong >= min_strong) & (cand.max_gap_h <= max_gap_h)
              & (cand.major_km >= min_major_km)]
    ok = (ok.sort_values(["conv_day", "n_reports"], ascending=[True, False])
            .drop_duplicates("conv_day").reset_index(drop=True))
    return ok, cand
