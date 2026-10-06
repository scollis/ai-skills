
BOX = (-94.2, 40.7, -87.4, 42.6)
USGS_LEGACY = "https://waterservices.usgs.gov/nwis"
USGS_OGC = "https://api.waterdata.usgs.gov/ogcapi/v0"
NWPS = "https://api.water.noaa.gov/nwps/v1"
IFIS_APP = "https://ifis.iowafloodcenter.org/ifis/app/"
IFIS_HLM = "https://ifis.iowafloodcenter.org/hlm-plus/api"
HADS_DEFS = "https://hads.ncep.noaa.gov/compressed_defs/all_dcp_defs.txt"
IEM_HADS = "https://mesonet.agron.iastate.edu/cgi-bin/request/hads.py"
NWM_PDS = "https://noaa-nwm-pds.s3.amazonaws.com"
NWM_RETRO3_CHRTOUT = "noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr"

import re


def usgs_parse_rdb(text):
    """Parse a USGS RDB (tab-delimited, '#' comments, dtype row) into a DataFrame."""
    import pandas as pd
    lines = [l for l in text.split("\n") if l and not l.startswith("#")]
    hdr = lines[0].split("\t")
    body = [l.split("\t") for l in lines[2:] if l.strip()]
    return pd.DataFrame([r + [""] * (len(hdr) - len(r)) for r in body], columns=hdr)


def usgs_sites_box(box=None, site_type="ST", parameter_cd="00060,00065",
                   site_status="all", expanded=True, timeout=180):
    """USGS site metadata inside a lon/lat box via the LEGACY site service (RDB).

    expanded=True returns drain_area_va, alt_va, construction_dt and 30 more columns.
    Legacy waterservices is scheduled for decommission in early 2027 - see
    usgs_ogc_locations_box for the replacement.
    """
    import requests
    if box is None:
        box = BOX
    p = {"format": "rdb", "bBox": ",".join(str(x) for x in box),
         "siteType": site_type, "siteStatus": site_status}
    if parameter_cd:
        p["parameterCd"] = parameter_cd
    if expanded:
        p["siteOutput"] = "expanded"
    r = requests.get(USGS_LEGACY + "/site/", params=p, timeout=timeout)
    r.raise_for_status()
    return usgs_parse_rdb(r.text)


def usgs_series_catalog(box=None, site_type="ST", timeout=300):
    """Per-site, per-parameter period of record (begin_date/end_date/count_nu).

    One call returns every time series for every site in the box. data_type_cd is
    'uv' (instantaneous), 'dv' (daily), 'pk' (annual peak), 'qw', 'gw'.
    """
    import requests
    if box is None:
        box = BOX
    r = requests.get(USGS_LEGACY + "/site/", params={
        "format": "rdb", "bBox": ",".join(str(x) for x in box), "siteType": site_type,
        "outputDataTypeCd": "iv,dv,pk", "seriesCatalogOutput": "true"}, timeout=timeout)
    r.raise_for_status()
    return usgs_parse_rdb(r.text)


def usgs_iv(sites, start, end, parameter_cd="00060,00065", timeout=300):
    """Instantaneous values (legacy /nwis/iv, JSON) -> long DataFrame.

    sites: one site number or a list. Times are returned tz-aware.
    """
    import requests, pandas as pd
    if isinstance(sites, str):
        sites = [sites]
    r = requests.get(USGS_LEGACY + "/iv/", params={
        "format": "json", "sites": ",".join(sites), "parameterCd": parameter_cd,
        "startDT": start, "endDT": end, "siteStatus": "all"}, timeout=timeout)
    r.raise_for_status()
    rows = []
    for ts in r.json()["value"]["timeSeries"]:
        sn = ts["sourceInfo"]["siteCode"][0]["value"]
        pc = ts["variable"]["variableCode"][0]["value"]
        unit = ts["variable"]["unit"]["unitCode"]
        for v in ts["values"][0]["value"]:
            try:
                val = float(v["value"])
            except (TypeError, ValueError):
                continue
            if val <= -999:
                continue
            rows.append((sn, pc, unit, v["dateTime"], val))
    df = pd.DataFrame(rows, columns=["site_no", "parameter_cd", "unit", "time", "value"])
    if len(df):
        df["time"] = pd.to_datetime(df["time"], utc=True, format="ISO8601")
    return df


def usgs_dv(sites=None, box=None, start=None, end=None, parameter_cd="00065",
            stat_cd="00003", timeout=900):
    """Daily values (legacy /nwis/dv). Pass EITHER sites or box.

    stat_cd 00003 = daily MEAN. In the DERECHOS domain gage height (00065) exists
    as a daily series at 183 sites but essentially only as the mean - daily max
    (00001) is published at exactly one site - so daily values understate crests.
    Use usgs_iv or usgs_peaks for peak stage.
    """
    import requests, pandas as pd
    p = {"format": "json", "parameterCd": parameter_cd, "statCd": stat_cd,
         "startDT": start, "endDT": end, "siteStatus": "all"}
    if sites is not None:
        p["sites"] = ",".join([sites] if isinstance(sites, str) else sites)
    else:
        p["bBox"] = ",".join(str(x) for x in (box or BOX))
    r = requests.get(USGS_LEGACY + "/dv/", params=p, timeout=timeout)
    r.raise_for_status()
    rows = []
    for ts in r.json()["value"]["timeSeries"]:
        sn = ts["sourceInfo"]["siteCode"][0]["value"]
        for v in ts["values"][0]["value"]:
            try:
                val = float(v["value"])
            except (TypeError, ValueError):
                continue
            if val <= -999:
                continue
            rows.append((sn, v["dateTime"][:10], val))
    return pd.DataFrame(rows, columns=["site_no", "date", "value"])


def usgs_peaks_legacy(site_no, timeout=180):
    """Annual peak streamflow/stage, RDB, from nwis.waterdata.usgs.gov/nwis/peak.

    Columns include peak_dt, peak_va (cfs), gage_ht (ft), ag_dt/ag_gage_ht for
    gage-height-only peaks. Needs the nwis.waterdata.usgs.gov allowlist entry.
    """
    import requests, pandas as pd
    r = requests.get("https://nwis.waterdata.usgs.gov/nwis/peak",
                     params={"site_no": site_no, "agency_cd": "USGS", "format": "rdb"},
                     timeout=timeout)
    r.raise_for_status()
    if "peak_va" not in r.text:
        return pd.DataFrame()
    df = usgs_parse_rdb(r.text)
    for c in ("peak_va", "gage_ht", "ag_gage_ht"):
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def usgs_ogc_items(collection, params=None, cap=50000, timeout=300):
    """Page an OGC API collection with the CURSOR links (rel='next').

    The `offset` parameter also works but the documented pager is the cursor.
    Values arrive as STRINGS in `properties.value` - cast them yourself.
    """
    import requests
    url = USGS_OGC + "/collections/%s/items" % collection
    p = dict(params or {})
    p["f"] = "json"
    p.setdefault("limit", 1000)
    feats = []
    while True:
        r = requests.get(url, params=p, timeout=timeout)
        r.raise_for_status()
        j = r.json()
        got = j.get("features", [])
        feats += got
        nxt = [l["href"] for l in j.get("links", []) if l.get("rel") == "next"]
        if not nxt or not got or len(feats) >= cap:
            break
        url, p = nxt[0], None
    return feats


def usgs_ogc_locations_box(box=None, site_type_code="ST", agency_code="USGS", timeout=300):
    """Monitoring locations in a box from the CURRENT OGC API -> DataFrame.

    WARNING: this collection is the whole site inventory, including sites that
    never had a time series and non-USGS agencies. In the DERECHOS box it returns
    2360 stream locations against 248 from the filtered legacy site service.
    Join against usgs_ogc_timeseries_meta (or usgs_series_catalog) to keep only
    locations that actually carry data.
    """
    import pandas as pd
    if box is None:
        box = BOX
    p = {"bbox": ",".join(str(x) for x in box)}
    if site_type_code:
        p["site_type_code"] = site_type_code
    feats = usgs_ogc_items("monitoring-locations", p, timeout=timeout)
    df = pd.json_normalize([f["properties"] for f in feats])
    if agency_code and "agency_code" in df:
        df = df[df.agency_code == agency_code]
    return df.reset_index(drop=True)


def usgs_ogc_series(collection, monitoring_location_ids, parameter_code=None,
                    datetime_range=None, limit=10000, sortby=None, timeout=300):
    """Fetch from an OGC value collection ('daily', 'continuous', 'peaks', ...).

    monitoring_location_ids must carry the 'USGS-' prefix; a comma-joined list works.
    GOTCHA: `datetime` filters `daily` and `continuous` but on `peaks` it silently
    returns ZERO features with HTTP 200 - fetch the whole record and filter locally,
    or pass sortby='-time'.
    """
    import pandas as pd
    ids = [monitoring_location_ids] if isinstance(monitoring_location_ids, str) else list(monitoring_location_ids)
    ids = [i if i.startswith("USGS-") else "USGS-" + i for i in ids]
    out = []
    for i in range(0, len(ids), 20):
        p = {"monitoring_location_id": ",".join(ids[i:i + 20]), "limit": limit}
        if parameter_code:
            p["parameter_code"] = parameter_code
        if datetime_range:
            p["datetime"] = datetime_range
        if sortby:
            p["sortby"] = sortby
        out += usgs_ogc_items(collection, p, timeout=timeout)
    df = pd.json_normalize([f["properties"] for f in out])
    if "value" in df:
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
    if "monitoring_location_id" in df:
        df["site_no"] = df.monitoring_location_id.str.replace("USGS-", "", regex=False)
    return df


def usgs_ogc_timeseries_meta(monitoring_location_ids, timeout=300):
    """Time-series metadata: parameter_code, statistic_id, begin/end, units."""
    return usgs_ogc_series("time-series-metadata", monitoring_location_ids, timeout=timeout)


def nwps_gauges_box(box=None, timeout=300):
    """NWPS gauges inside a lon/lat box -> DataFrame (353 in the DERECHOS box).

    CRITICAL: srid=EPSG_4326 is REQUIRED. Without it the bbox.* filters are
    accepted, return HTTP 200, and yield ZERO gauges. Any spelling the server
    does not recognise (xmin=, state=, wfo=, bbox=csv) is silently ignored and
    you get the FULL national list (12,873 gauges) with HTTP 200.
    """
    import requests, pandas as pd
    if box is None:
        box = BOX
    r = requests.get(NWPS + "/gauges", params={
        "bbox.xmin": box[0], "bbox.ymin": box[1], "bbox.xmax": box[2], "bbox.ymax": box[3],
        "srid": "EPSG_4326"}, timeout=timeout)
    r.raise_for_status()
    g = r.json().get("gauges", [])
    df = pd.json_normalize(g)
    if len(df):
        assert df.longitude.between(box[0], box[2]).all(), "bbox was ignored - check srid"
    return df


def nwps_flood_categories(lid, timeout=120):
    """Flood-category thresholds + historic crests for one NWPS gauge (LID).

    Returns action/minor/moderate/major stage and flow, usgsId, and reachId
    (the NWM feature_id / NHDPlus COMID). -9999 is the missing sentinel and is
    mapped to None here; 119 of 353 DERECHOS-box gauges have no thresholds.
    """
    import requests
    r = requests.get(NWPS + "/gauges/%s" % lid, timeout=timeout)
    r.raise_for_status()
    d = r.json()
    fl = d.get("flood") or {}
    cat = fl.get("categories") or {}

    def _v(name, key):
        x = (cat.get(name) or {}).get(key)
        return None if x in (None, -9999) else x

    return {"lid": d.get("lid"), "name": d.get("name"), "usgs_id": d.get("usgsId") or None,
            "reach_id": d.get("reachId") or None,
            "lat": d.get("latitude"), "lon": d.get("longitude"),
            "stage_units": fl.get("stageUnits"), "flow_units": fl.get("flowUnits"),
            "action": _v("action", "stage"), "minor": _v("minor", "stage"),
            "moderate": _v("moderate", "stage"), "major": _v("major", "stage"),
            "action_flow": _v("action", "flow"), "minor_flow": _v("minor", "flow"),
            "moderate_flow": _v("moderate", "flow"), "major_flow": _v("major", "flow"),
            "crests": (fl.get("crests") or {}).get("historic", []),
            "wfo": (d.get("wfo") or {}).get("abbreviation"),
            "rfc": (d.get("rfc") or {}).get("abbreviation")}


def nwps_stageflow(lid, timeout=180):
    """Observed + forecast stage/flow for one LID -> (observed_df, forecast_df).

    'primary' is stage (ft) and 'secondary' flow (kcfs) for an HG gauge; check
    pedts. The OBSERVED series is a ~30-day rolling window only - it is NOT an
    archive. For anything older use usgs_iv / IEM HADS.
    """
    import requests, pandas as pd
    r = requests.get(NWPS + "/gauges/%s/stageflow" % lid, timeout=timeout)
    r.raise_for_status()
    j = r.json()
    out = []
    for k in ("observed", "forecast"):
        d = pd.DataFrame((j.get(k) or {}).get("data", []))
        if len(d):
            d["validTime"] = pd.to_datetime(d.validTime, utc=True, format="ISO8601")
        out.append(d)
    return out[0], out[1]


def nwps_reach_streamflow(reach_id, series="short_range", timeout=180):
    """NWM streamflow for one reach straight off the NWPS API (no S3).

    series: analysis_assimilation | short_range | medium_range | long_range |
    medium_range_blend. Only the requested series is populated; the others come
    back as empty dicts. Returns (DataFrame, reach_metadata) where the metadata
    carries route.upstream / route.downstream reachIds.
    """
    import requests, pandas as pd
    r = requests.get(NWPS + "/reaches/%s/streamflow" % reach_id,
                     params={"series": series}, timeout=timeout)
    r.raise_for_status()
    j = r.json()
    key = "".join([p.capitalize() if i else p for i, p in enumerate(series.split("_"))])
    blk = j.get(key) or {}
    ser = blk.get("series") or blk
    df = pd.DataFrame(ser.get("data", []))
    if len(df):
        df["validTime"] = pd.to_datetime(df.validTime, utc=True, format="ISO8601")
        df.attrs["units"] = ser.get("units")
        df.attrs["referenceTime"] = ser.get("referenceTime")
    return df, j.get("reach", {})


def ifis_objects(timeout=180):
    """Every IFIS map object statewide -> DataFrame(ifis_id, lat, lon, obj_type).

    Undocumented endpoint (inc/inc_get_object.php?id=0). The payload is a
    JavaScript array-of-arrays, not JSON. obj_type is the IFIS data PANEL type,
    not a sensor class: 2/3/4 stream gauge, 8 outlet, 11 rain, 15 hydrostation,
    17 well. Statewide it returns 1951 objects; 901 fall in the DERECHOS box.
    """
    import requests, pandas as pd
    t = requests.get(IFIS_APP + "inc/inc_get_object.php", params={"id": 0}, timeout=timeout).text
    depth = 0
    start = None
    secs = []
    instr = False
    q = None
    for i, ch in enumerate(t):
        if instr:
            if ch == q:
                instr = False
            continue
        if ch in "'\"":
            instr, q = True, ch
            continue
        if ch == "[":
            depth += 1
            if depth == 2:
                start = i
        elif ch == "]":
            if depth == 2:
                secs.append((start, i + 1))
            depth -= 1
    if not secs:
        return pd.DataFrame()
    body = t[secs[-1][0]:secs[-1][1]]
    rows = [rw.split(",") for rw in re.findall(r"\[([^\[\]]*)\]", body)]
    df = pd.DataFrame([r[:4] for r in rows if len(r) >= 4],
                      columns=["ifis_id", "lat", "lon", "obj_type"])
    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["lat", "lon"])


def ifis_sensor(ifis_id, obj_type=4, timeout=90):
    """Metadata + latest reading for one IFIS object (chart/chart-bridge.php).

    Returns name ('river | road | town'), native sensor_id, water elevation as a
    ft-in string, and last-report time. HTML scrape of an undocumented endpoint.
    An IFC sensor with no recent report gives elev='no data available' and a
    1969 epoch-zero timestamp rather than an error.
    """
    import requests, html
    r = requests.get(IFIS_APP + "chart/chart-bridge.php",
                     params={"id": int(ifis_id), "type": int(obj_type)}, timeout=timeout)
    r.raise_for_status()
    x = r.text

    def g(pat):
        m = re.search(pat, x, re.S)
        return html.unescape(re.sub("<[^>]+>", "", m.group(1))).strip() if m else None

    return {"ifis_id": int(ifis_id), "name": g(r'class="lngtxt">(.*?)</div>'),
            "kind": g(r'class="type">(.*?)</div>'),
            "sensor_id": g(r"<b>Sensor ID:</b>(.*?)&nbsp;"),
            "elevation": g(r"<b>Water Elevation:</b>(.*?)<BR>"),
            "last_reported": g(r"<b>Last Reported:</b>(.*?)&nbsp;")}


def ifis_hydrostations(timeout=120):
    """IFC hydrostation list from the 2025 IFIS app (getObjectList?otype=15).

    The only otype that returns anything (59 statewide). Real JSON, and the only
    IFIS endpoint that hands back link_id and comid directly.
    """
    import requests, pandas as pd
    r = requests.get(IFIS_HLM + "/getObjectList/", params={"otype": 15}, timeout=timeout)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def hads_dcp_defs(states=None, timeout=600):
    """National HADS DCP definition table (23 MB pipe-delimited) -> DataFrame.

    Field order, read off a real line: 0 nesdis_id, 1 nws_lid, 2 owner, 3 state,
    4 hsa, 5 lat_dms, 6 lon_dms, 7 elevation (hundredths of a foot, zero-padded),
    8 transmission interval (s), 9 name, 10 flag, then repeating SHEF physical
    element blocks. Note fields 7-8: the NAME is field 9, not field 8. Decimal
    lat/lon are derived here; every field is space-padded.
    """
    import requests, pandas as pd
    r = requests.get(HADS_DEFS, timeout=timeout)
    r.raise_for_status()
    rows = []
    for line in r.text.split("\n"):
        f = line.split("|")
        if len(f) < 12:
            continue
        rows.append(f[:12])
    df = pd.DataFrame(rows, columns=["nesdis_id", "nws_lid", "owner", "state", "hsa",
                                     "lat_dms", "lon_dms", "elevation", "interval_s",
                                     "name", "flag", "first_pe"])
    for c in ("nws_lid", "owner", "state", "hsa", "name", "flag", "first_pe", "elevation"):
        df[c] = df[c].str.strip()

    def dms_to_dec(s):
        p = s.split()
        try:
            v = abs(float(p[0])) + float(p[1]) / 60 + float(p[2]) / 3600
        except (IndexError, ValueError):
            return None
        return -v if s.strip().startswith("-") else v

    df["lat"] = df.lat_dms.map(dms_to_dec)
    df["lon"] = df.lon_dms.map(dms_to_dec)
    if states:
        df = df[df.state.isin([s.strip() for s in states])]
    return df.reset_index(drop=True)


def hads_via_iem(stations, start, end, network="IA_DCP", timeout=600):
    """HADS/DCP 15-minute SHEF observations from the IEM archive -> DataFrame.

    This is the working HADS data path: hads.ncep.noaa.gov's own DecodedData
    servlet returns HTTP 200 with an EMPTY body for every parameter combination
    tried. Columns are SHEF physical elements - HGIRGZZ river stage (ft),
    PCIRGZZ accumulated precip, PPHRGZZ incremental precip, VBIRGZZ battery.
    network: IA_DCP, IL_DCP, ... (one state per call).
    Etiquette: IEM is university hardware - one call per whole date range.
    """
    import requests, pandas as pd, io
    if isinstance(stations, str):
        stations = [stations]
    r = requests.get(IEM_HADS, params={
        "network": network, "stations": ",".join(stations),
        "sts": start if "T" in start else start + "T00:00Z",
        "ets": end if "T" in end else end + "T00:00Z",
        "what": "txt", "delim": "comma"}, timeout=timeout)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    if "utc_valid" in df:
        df["utc_valid"] = pd.to_datetime(df.utc_valid, utc=True)
    return df


def nwm_pds_keys(day, config="short_range", cycle="t00z", product="channel_rt", timeout=180):
    """List noaa-nwm-pds keys for one day/configuration.

    day: 'YYYYMMDD' or a date. The bucket is a ROLLING window (about 20 months) -
    not an archive. For anything older use nwm_retro_open.
    """
    import requests
    d = day if isinstance(day, str) else day.strftime("%Y%m%d")
    pref = "nwm.%s/%s/nwm.%s.%s.%s" % (d, config, cycle, config, product)
    keys, tok = [], None
    while True:
        p = {"list-type": "2", "prefix": pref, "max-keys": "1000"}
        if tok:
            p["continuation-token"] = tok
        r = requests.get(NWM_PDS + "/", params=p, timeout=timeout)
        r.raise_for_status()
        keys += re.findall(r"<Key>([^<]+)</Key>", r.text)
        m = re.search(r"<NextContinuationToken>([^<]+)<", r.text)
        if not m:
            break
        tok = m.group(1)
    return keys


def nwm_retro_open(store=None):
    """Open the NWM v3.0 retrospective channel-routing Zarr store (anonymous).

    51 TB, hourly 1979-02-01 to 2023-02-01, 2,776,734 reaches. Chunks are
    (672 time, 30000 feature) = 161 MB decompressed each, and feature_id is NOT
    spatially sorted, so a bbox subset touches almost as many chunks as CONUS.
    Measured from this sandbox: 1 reach x 1 month 36 s; 1 reach x 1 year 98 s;
    all 50,631 DERECHOS-box reaches x 24 h 152 s. Extract a domain slab once and
    cache it; never loop reach-by-reach.
    """
    import xarray, s3fs
    fs = s3fs.S3FileSystem(anon=True)
    return xarray.open_zarr(s3fs.S3Map(store or NWM_RETRO3_CHRTOUT, s3=fs), consolidated=True)


def nwm_gage_map(ds):
    """USGS site number -> NWM feature_id, read off the retrospective's gage_id coord.

    8660 of 2,776,734 CONUS reaches carry a gage_id. Verified against NWPS
    reachId: 05465500 (Iowa River at Wapello) -> 11919825 both ways.
    """
    import numpy as np, pandas as pd
    g = np.char.strip(ds.gage_id.values.astype(str))
    df = pd.DataFrame({"feature_id": ds.feature_id.values, "gage_id": g})
    return df[df.gage_id != ""].reset_index(drop=True)


def nwm_box_features(ds, box=None):
    """Integer positions of reaches whose lat/lon fall in the box (50,631 for DERECHOS)."""
    import numpy as np
    if box is None:
        box = BOX
    lat = ds.latitude.values
    lon = ds.longitude.values
    m = (lon >= box[0]) & (lon <= box[2]) & (lat >= box[1]) & (lat <= box[3])
    return np.where(m)[0]


def flood_category(stage, thresholds):
    """Classify a stage against a nwps_flood_categories() dict.

    Returns 'major'|'moderate'|'minor'|'action'|'below'|'undefined'.
    """
    order = [("major", thresholds.get("major")), ("moderate", thresholds.get("moderate")),
             ("minor", thresholds.get("minor")), ("action", thresholds.get("action"))]
    if all(v is None for _, v in order):
        return "undefined"
    if stage is None:
        return "undefined"
    for name, v in order:
        if v is not None and stage >= v:
            return name
    return "below"
