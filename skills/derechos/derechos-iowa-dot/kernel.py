
IADOT_HUB = "https://data.iowadot.gov/api/search/v1/collections/dataset/items"
IADOT_AGS = "https://gis.iowadot.gov/agshost/rest/services"
IADOT_AGOL = "https://services.arcgis.com/8lRhdTsQyJpO52F1/arcgis/rest/services"
IEM = "https://mesonet.agron.iastate.edu"
DERECHOS_BOX = (-94.2, 40.7, -87.4, 42.6)
RWIS_VARS = ("tmpf", "dwpf", "relh", "sknt", "drct", "gust",
             "tfs0", "tfs0_text", "tfs1", "tfs1_text", "tfs2", "tfs2_text",
             "tfs3", "tfs3_text", "subf")


def iadot_catalogue(match=None, limit=100):
    """Full Iowa DOT open-data catalogue (OGC API Records). 162 items on 2026-09-05.

    `startindex` is 1-BASED; 0 returns HTTP 400.
    """
    import requests
    import pandas as pd
    rows, si = [], 1
    while True:
        j = requests.get(IADOT_HUB, params={"limit": limit, "startindex": si},
                         timeout=60).json()
        feats = j.get("features", [])
        for f in feats:
            p = f["properties"]
            rows.append({"title": p.get("title"), "type": p.get("type"),
                         "id": p.get("id"), "url": p.get("url") or "",
                         "tags": ",".join(p.get("tags") or []),
                         "snippet": p.get("snippet")})
        si += len(feats)
        if not feats or si > j.get("numberMatched", 0):
            break
    df = pd.DataFrame(rows)
    if match:
        df = df[df.title.str.contains(match, case=False, na=False)
                | df.tags.str.contains(match, case=False, na=False)]
    return df.reset_index(drop=True)


def iadot_services(instance=None):
    """Walk the ArcGIS Server REST directory. `private` is 401; `agshost` is public."""
    import requests
    import pandas as pd
    base = IADOT_AGS if instance is None else \
        "https://gis.iowadot.gov/%s/rest/services" % instance
    root = requests.get(base, params={"f": "json"}, timeout=60).json()
    out = [{"folder": "", "name": s["name"], "type": s["type"]}
           for s in root.get("services", [])]
    for fo in root.get("folders", []):
        j = requests.get("%s/%s" % (base, fo), params={"f": "json"},
                         timeout=60).json()
        for s in j.get("services", []):
            out.append({"folder": fo, "name": s["name"], "type": s["type"]})
    df = pd.DataFrame(out)
    df["url"] = base + "/" + df["name"] + "/" + df["type"]
    return df


def ags_layers(service_url):
    """Layers + tables of a FeatureServer/MapServer. Returns [] and an 'error' key
    for token-gated services (HTTP 200, error code 499)."""
    import requests
    j = requests.get(service_url, params={"f": "json"}, timeout=60).json()
    if "error" in j:
        return {"error": j["error"], "layers": [], "tables": []}
    return {"maxRecordCount": j.get("maxRecordCount"),
            "layers": [(l["id"], l["name"], l.get("geometryType"))
                       for l in j.get("layers", [])],
            "tables": [(t["id"], t["name"]) for t in j.get("tables", [])]}


def ags_fields(service_url, layer=0):
    """Field names/types plus any coded-value domains for one layer."""
    import requests
    j = requests.get("%s/%d" % (service_url, layer), params={"f": "json"},
                     timeout=60).json()
    doms = {}
    for f in j.get("fields", []):
        d = f.get("domain") or {}
        if d.get("codedValues"):
            doms[f["name"]] = {cv["code"]: cv["name"] for cv in d["codedValues"]}
    return {"name": j.get("name"),
            "fields": [(f["name"], f["type"].replace("esriFieldType", ""))
                       for f in j.get("fields", [])],
            "domains": doms, "extent": j.get("extent")}


def ags_count(service_url, layer=0, where="1=1", bbox=None):
    """returnCountOnly. bbox is (lon_min, lat_min, lon_max, lat_max); inSR=4326 is
    ALWAYS sent - omitting it returns count 0 with HTTP 200."""
    import requests
    p = {"where": where, "returnCountOnly": "true", "f": "json"}
    if bbox:
        p.update({"geometry": ",".join(str(v) for v in bbox),
                  "geometryType": "esriGeometryEnvelope", "inSR": 4326,
                  "spatialRel": "esriSpatialRelIntersects"})
    j = requests.get("%s/%d/query" % (service_url, layer), params=p,
                     timeout=120).json()
    return j.get("count", j)


def ags_query(service_url, layer=0, where="1=1", bbox=None, out_fields="*",
              geometry=True, page=None, decode=True, max_pages=200, extra=None):
    """Page a layer with resultOffset/resultRecordCount into a DataFrame.

    Requests are capped at the service maxRecordCount (1000 on AGOL views,
    2000 on agshost) regardless of what you ask for; exceededTransferLimit
    signals more rows. `decode=True` maps coded-value domains to labels.
    Geometry, when returned, is added as x/y (points) in EPSG:4326.
    """
    import requests
    import pandas as pd
    if page is None:
        page = 2000
    meta = ags_fields(service_url, layer)
    feats, off = [], 0
    for _ in range(max_pages):
        p = {"where": where, "outFields": out_fields, "f": "json",
             "resultOffset": off, "resultRecordCount": page,
             "returnGeometry": "true" if geometry else "false", "outSR": 4326}
        if bbox:
            p.update({"geometry": ",".join(str(v) for v in bbox),
                      "geometryType": "esriGeometryEnvelope", "inSR": 4326,
                      "spatialRel": "esriSpatialRelIntersects"})
        if extra:
            p.update(extra)
        j = requests.get("%s/%d/query" % (service_url, layer), params=p,
                         timeout=300).json()
        if "error" in j:
            raise RuntimeError(j["error"])
        fs = j.get("features", [])
        feats += fs
        if not fs or (not j.get("exceededTransferLimit") and len(fs) < page):
            break
        off += len(fs)
    df = pd.DataFrame([f["attributes"] for f in feats])
    if geometry and feats and isinstance(feats[0].get("geometry"), dict):
        gt = feats[0]["geometry"]
        if "x" in gt:
            df["x"] = [f["geometry"]["x"] if f.get("geometry") else None
                       for f in feats]
            df["y"] = [f["geometry"]["y"] if f.get("geometry") else None
                       for f in feats]
    if decode:
        for col, m in meta["domains"].items():
            if col in df.columns:
                df[col + "_label"] = df[col].map(m)
    for c in df.columns:
        if c.upper().endswith(("_DATE", "_UTC", "DATETIME", "FILEDATE",
                               "_START", "_END", "UPDATED")):
            try:
                df[c + "_dt"] = pd.to_datetime(df[c], unit="ms")
            except Exception:
                pass
    return df


def iadot_rwis_sites(kind=None):
    """Live Iowa DOT RWIS tables. kind='atmos'|'surface'|'traffic'|'camera'.

    Current conditions only - one row per station (atmos) or per pavement
    sensor (surface). NWS_ID is the IEM IA_RWIS station id, so it is the join
    key to the archive. 9999 is the missing sentinel in the surface table.
    """
    svc = {"atmos": "RWIS_Atmospheric_Data_View", "surface": "RWIS_Surface_Data_View",
           "traffic": "RWIS_Traffic_Data_View", "camera": "RWIS_Camera_Info_View"}
    if kind is None:
        kind = "atmos"
    return ags_query("%s/%s/FeatureServer" % (IADOT_AGOL, svc[kind]), 0,
                     page=1000, geometry=(kind != "camera"))


def iem_rwis_network(state=None):
    """IEM RWIS station metadata incl. archive_begin/archive_end. state='IA'|'IL'."""
    import requests
    import pandas as pd
    if state is None:
        state = "IA"
    j = requests.get("%s/geojson/network/%s_RWIS.geojson" % (IEM, state),
                     timeout=120).json()
    return pd.DataFrame([dict(f["properties"],
                              lon=f["geometry"]["coordinates"][0],
                              lat=f["geometry"]["coordinates"][1])
                         for f in j["features"]])


def iem_rwis(stations, start, end, variables=None, tz=None, tries=4):
    """IEM RWIS archive (/cgi-bin/request/rwis.py). Parameter is `stations`
    (plural). One call for the whole range - do not loop days. The CGI streams
    chunked and can raise IncompleteRead; this retries."""
    import io
    import time
    import requests
    import pandas as pd
    if variables is None:
        variables = list(RWIS_VARS)
    if tz is None:
        tz = "Etc/UTC"
    if isinstance(stations, str):
        stations = [stations]
    p = {"stations": stations, "vars": variables, "tz": tz, "delim": "comma",
         "what": "txt", "gis": "no",
         "year1": start[:4], "month1": int(start[5:7]), "day1": int(start[8:10]),
         "hour1": 0, "minute1": 0,
         "year2": end[:4], "month2": int(end[5:7]), "day2": int(end[8:10]),
         "hour2": 0, "minute2": 0}
    last = None
    for i in range(tries):
        try:
            r = requests.get("%s/cgi-bin/request/rwis.py" % IEM, params=p,
                             timeout=900)
            r.raise_for_status()
            if len(r.text.splitlines()) < 2:
                return pd.DataFrame()
            df = pd.read_csv(io.StringIO(r.text))
            df["obtime"] = pd.to_datetime(df["obtime"])
            return df
        except Exception as exc:
            last = exc
            time.sleep(3 * (i + 1))
    raise last


def iadot_road_conditions(season, where="1=1", bbox=None):
    """Historic Iowa Road Conditions for one winter season, e.g. season='2019_2020'.

    Open seasons on 2026-09-05: 2019_2020, 2020_2021, 2021_2022, 2022_2023,
    2023_2024, 2025_2026. 2024_2025 returns error code 499 Token Required.
    Date field is CONDITION_CHANGE_START; use TIMESTAMP 'YYYY-MM-DD HH:MM:SS'.
    """
    url = ("%s/Winter_Operations/Historic_Iowa_Road_Conditions_%s/FeatureServer"
           % (IADOT_AGS, season))
    return ags_query(url, 0, where=where, bbox=bbox, geometry=False)


def iadot_crashes(start, end, bbox=None, extra_where=None):
    """Iowa DOT crash records over a date window, with WEATHER / CSRFCND / CSEV
    decoded to labels. Archive measured 2015-01-01 to 2026-09-02."""
    url = "%s/Traffic_Safety/Crash_Data/FeatureServer" % IADOT_AGS
    w = ("CRASH_DATE >= TIMESTAMP '%s 00:00:00' AND CRASH_DATE < TIMESTAMP '%s 00:00:00'"
         % (start, end))
    if extra_where:
        w = "(%s) AND (%s)" % (w, extra_where)
    return ags_query(url, 0, where=w, bbox=bbox)


def iadot_plowcam(bbox=None, fetch=0):
    """Snowplow dashcam images from the past hour. Set fetch=N to download N JPEGs
    from cloud.iowadot.gov into ./plowcam/. Empty of winter content off-season."""
    import os
    import requests
    df = ags_query("%s/AVL_Images_Past_1HR_View/FeatureServer" % IADOT_AGOL, 0,
                   page=2000)
    if bbox and len(df):
        df = df[(df.PHOTO_LONGITUDE.between(bbox[0], bbox[2]))
                & (df.PHOTO_LATITUDE.between(bbox[1], bbox[3]))]
    if fetch and len(df):
        os.makedirs("plowcam", exist_ok=True)
        for _, r in df.head(fetch).iterrows():
            url = r.SECURE_PHOTO_URL or r.PHOTO_URL
            if not url:
                continue
            name = r.PHOTO_FILENAME or url.rsplit("/", 1)[-1]
            b = requests.get(url, timeout=120).content
            open(os.path.join("plowcam", name), "wb").write(b)
    return df


def derechos_iadot_sources(sq=None):
    """Iowa DOT source -> DERECHOS science-question table, as measured 2026-09-05."""
    import pandas as pd
    rows = [
        ("RWIS atmospheric (live)", "AGOL", "verified", "SQ2, SQ3, SQ6",
         "94 stations statewide, 52 in box; air T, Td, RH, wind, precip type/rate, visibility"),
        ("RWIS surface (live)", "AGOL", "verified", "SQ3",
         "203 pavement sensors, 120 in box; pavement T, surface condition, ice %, friction"),
        ("RWIS archive via IEM", "mesonet.agron.iastate.edu", "verified", "SQ2, SQ3",
         "59 IA stations in box, record from 2000-02-08; tmpf/dwpf/wind + tfs0-3 pavement"),
        ("RWIS cameras", "AGOL + cloud.iowadot.gov", "verified", "SQ3",
         "68 sites / 305 positions, 146 positions in box, 10 rolling images each"),
        ("Iowa 511 winter road conditions", "AGOL", "verified", "SQ3",
         "1014 CARS segments, 563 in box; current condition only"),
        ("Historic road conditions", "agshost", "partial", "SQ3, SQ6",
         "6 of 7 seasons open, 2019-2026; 2024_2025 token-gated"),
        ("Crash records", "agshost", "verified", "SQ3, SQ6",
         "452,586 in box 2015-2026, with weather + surface-condition codes"),
        ("Snowplow AVL (live)", "AGOL", "partial", "SQ3",
         "per-truck road+air temp and plow state; 0 features off-season, no archive"),
        ("Plow dashcam images", "AGOL + cloud.iowadot.gov", "verified", "SQ3",
         "rolling 1 h; 85 images statewide, 16 in box at time of test"),
        ("Plow photo ML classifications", "agshost", "partial", "SQ3",
         "CLASSIFICATION + CONFIDENCE + MODEL_VERSION; 0 features off-season"),
        ("Winter storm analysis 48 h", "AGOL", "partial", "SQ3, SQ6",
         "salt/liquid quantity, passes, mean road+air T per segment; 0 off-season"),
        ("AADT / traffic log book", "AGOL", "verified", "SQ6",
         "4299 segments in box with truck/bus split"),
        ("RAMS road network", "agshost", "verified", "SQ3, SQ6",
         "208,314 LRS segments in box, 122 attributes"),
        ("Bridges / structures", "agshost", "verified", "SQ6",
         "11,018 bridge points in box plus historic inspection table"),
        ("Iowa 511 native API", "api.iowaroadconditions.org", "dead", "SQ3",
         "allowlisted but 502 on CONNECT; the AGOL CARS mirrors replace it"),
    ]
    df = pd.DataFrame(rows, columns=["source", "host", "status",
                                     "science_questions", "note"])
    if sq is not None:
        df = df[df.science_questions.str.contains("SQ%d" % sq)]
    return df.reset_index(drop=True)
