
"""Verified access helpers for the regional data sources DERECHOS depends on."""

import os
import sys
import json
import re

IEM = "https://mesonet.agron.iastate.edu"
ARMLIVE = "https://adc.arm.gov/armlive/livedata"
MPING = "https://mping.ou.edu/mping/api/v2/reports"
CDL = "https://nassgeodata.gmu.edu/axis2/services/CDLService"
E84 = "https://earth-search.aws.element84.com/v1"
CDSE_ODATA = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
NEXRAD_BUCKET = "unidata-nexrad-level2"
DERECHOS_BBOX = [-94.2, 40.7, -87.4, 42.6]

SOURCE_MATRIX = [
    ("ARM Data Center / ARM Live", "campaign M1/S1/R1 instruments",
     "SQ1 SQ2 SQ3 SQ4 SQ5 SQ6 SQ7", "tested", "arm_query, arm_download"),
    ("IEM - ASOS/AWOS", "surface met, gusts, 1-5 min precip",
     "SQ2 SQ6 SQ7", "tested", "iem_asos"),
    ("IEM - ISUSM soil network", "soil moisture + soil temperature profiles at M1 and S1",
     "SQ1 SQ2", "tested", "iem_isusm"),
    ("IEM - RAOB", "KDVN/KILX sounding archive",
     "SQ3 SQ6 SQ7", "tested", "iem_raob"),
    ("Illinois Climate Network / WARM", "soil moisture + soil temperature, eastern domain",
     "SQ1 SQ2 SQ3", "blocked-login", "icn_stations"),
    ("NEXRAD Level II (KDVN, KLOT)", "convective organization, wind extremes",
     "SQ1 SQ2 SQ6 SQ7", "tested", "derechos_nexrad_keys"),
    ("USDA Cropland Data Layer (CropScape)", "crop type per 30 m pixel",
     "SQ1 SQ2 SQ4 SQ5", "tested", "cdl_point, cdl_stats, cdl_clip"),
    ("AmeriFlux", "flux-tower ET comparison (ATMOS, downtown Chicago)",
     "SQ1 SQ2", "blocked-network", "ameriflux_status"),
    ("Sentinel-2 L2A (Element84 STAC)", "land-surface state, greenness, snow",
     "SQ1 SQ2 SQ3 SQ4 SQ5", "tested", "s2_search, s2_ndvi"),
    ("Sentinel-2 (Copernicus CDSE)", "same, native SAFE products",
     "SQ1 SQ2 SQ3", "partial-search-only", "cdse_search"),
    ("mPING", "crowdsourced precipitation type, hail, wind damage",
     "SQ2 SQ3 SQ6", "tested", "mping_reports"),
    ("HRRR archive (AWS)", "SCREAM IC/BC, IOP forecast scorecard",
     "SQ1 SQ6 SQ7", "tested", "hrrr_field, hrrr_point"),
]


def derechos_data_dir():
    """Directory holding this skill's shipped data files."""
    return os.path.dirname(sys._getframe().f_code.co_filename)


def derechos_stations():
    """Load the shipped station/site reference (sites, radars, ISUSM, ICN)."""
    path = os.path.join(derechos_data_dir(), "derechos_stations.json")
    with open(path) as fh:
        return json.load(fh)


def derechos_site(key):
    """One entry from derechos_stations()['sites'], e.g. 'M1', 'S1', 'NIU'."""
    return derechos_stations()["sites"][key.upper()]


def derechos_sources(status=None, sq=None):
    """The source -> science-question matrix as a list of dicts.

    status: filter on 'tested' / 'blocked-login' / 'blocked-network' / 'partial-search-only'
    sq:     integer 1-7, keep only sources serving that science question
    """
    out = []
    for name, provides, sqs, stat, helpers in SOURCE_MATRIX:
        if status is not None and stat != status:
            continue
        if sq is not None and ("SQ%d" % int(sq)) not in sqs:
            continue
        out.append({"source": name, "provides": provides, "science_questions": sqs.split(),
                    "status": stat, "helpers": helpers.split(", ")})
    return out


def derechos_credential(name):
    """Fetch a configured credential VALUE by name. Never print or log the return value.

    The kernel injects `host` into the interactive cell globals, which is NOT
    sys.modules['__main__'].__dict__, so this walks the caller frames to find it.
    """
    hostobj = None
    depth = 1
    while depth < 60:
        try:
            fr = sys._getframe(depth)
        except ValueError:
            break
        cand = fr.f_globals.get("host", None)
        if cand is not None and hasattr(cand, "credentials"):
            hostobj = cand
            break
        depth = depth + 1
    if hostobj is None:
        import __main__
        hostobj = getattr(__main__, "host", None)
    if hostobj is None or not hasattr(hostobj, "credentials"):
        raise RuntimeError("host object unavailable; pass user/token explicitly")
    return hostobj.credentials.get(name)["value"]


def arm_query(datastream, start, end, user=None, token=None):
    """ARM Live file listing for one datastream. Dates 'YYYY-MM-DD'.

    Returns {'files': [...], 'num_found': int, 'total_size': float}.
    Reuses the pattern documented in the gpm-storm-targeted-radar-fetch skill,
    which is the fuller reference for ARM Live failure modes.
    """
    import requests
    user = user or derechos_credential("ARMUSER")
    token = token or derechos_credential("ARMTOKEN")
    r = requests.get(ARMLIVE + "/query",
                     params={"user": "%s:%s" % (user, token), "ds": datastream,
                             "start": start, "end": end, "wt": "json"}, timeout=120)
    r.raise_for_status()
    return r.json()


def arm_download(datastream, start, end, output="arm_data", user=None, token=None):
    """Download an ARM datastream via ACT so the citation text is surfaced."""
    import act
    user = user or derechos_credential("ARMUSER")
    token = token or derechos_credential("ARMTOKEN")
    os.makedirs(output, exist_ok=True)
    return act.discovery.download_arm_data(user, token, datastream, start, end, output=output)


def iem_network(network):
    """Station table for an IEM network as a DataFrame. e.g. 'IA_ASOS', 'IL_ASOS', 'ISUSM'."""
    import requests
    import pandas as pd
    r = requests.get("%s/geojson/network/%s.geojson" % (IEM, network), timeout=120)
    r.raise_for_status()
    rows = []
    for f in r.json()["features"]:
        p = dict(f["properties"])
        p["id"] = f["id"]
        p["lon"], p["lat"] = f["geometry"]["coordinates"][:2]
        rows.append(p)
    return pd.DataFrame(rows)


def iem_asos(stations, start, end, data=None, tz="UTC"):
    """ASOS/AWOS observations as a DataFrame. start/end are 'YYYY-MM-DD' or datetimes.

    data defaults to a severe-convection-relevant set. report_type 3,4 = routine + specials,
    so gust peaks in SPECI reports are retained.
    """
    import requests
    import pandas as pd
    import io
    import datetime as dtm
    if data is None:
        data = ["tmpf", "dwpf", "relh", "sknt", "drct", "gust", "p01i", "mslp", "vsby"]
    if isinstance(stations, str):
        stations = [stations]
    s = start if hasattr(start, "year") else dtm.datetime.fromisoformat(str(start))
    e = end if hasattr(end, "year") else dtm.datetime.fromisoformat(str(end))
    params = {"station": stations, "data": data, "tz": tz, "format": "onlycomma",
              "latlon": "yes", "missing": "empty", "trace": "0.0001",
              "report_type": [3, 4],
              "year1": s.year, "month1": s.month, "day1": s.day,
              "year2": e.year, "month2": e.month, "day2": e.day}
    r = requests.get("%s/cgi-bin/request/asos.py" % IEM, params=params, timeout=600)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))


def iem_isusm(stations, start, end, mode="hourly", tz="UTC"):
    """ISU Soil Moisture Network (ISUSM) data as a DataFrame.

    mode: 'hourly' | 'daily'. start/end MUST be timezone-aware ISO strings; this helper
    appends 'T00:00:00Z' to bare dates because the service returns HTTP 422 otherwise.
    Units are US customary: soil*t in deg F, soil*vwc in percent, precip/et in inches.
    QC the VWC columns - see soil_sensor_health() for a known dead-sensor case at S1.
    """
    import requests
    import pandas as pd
    import io
    if isinstance(stations, str):
        stations = [stations]

    def stamp(v):
        v = str(v)
        if "T" not in v:
            v = v + "T00:00:00Z"
        return v
    r = requests.get("%s/cgi-bin/request/isusm.py" % IEM,
                     params={"station": stations, "format": "comma", "mode": mode,
                             "sts": stamp(start), "ets": stamp(end), "tz": tz, "na": "blank"},
                     timeout=600)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))


def soil_sensor_health():
    """Known ISUSM soil-sensor condition at the DERECHOS core sites (measured over 2024)."""
    return derechos_stations()["soil_sensor_health_2024"]


def iem_raob(station, start, end):
    """Radiosonde profiles from the IEM RAOB archive as a DataFrame.

    station e.g. 'KDVN'. Missing values arrive as the literal string 'M' and are
    converted to NaN here.
    """
    import requests
    import pandas as pd
    import io
    if isinstance(station, str):
        station = [station]

    def stamp(v):
        v = str(v)
        if "T" not in v:
            v = v + "T00:00:00Z"
        return v
    r = requests.get("%s/cgi-bin/request/raob.py" % IEM,
                     params={"station": station, "sts": stamp(start), "ets": stamp(end),
                             "format": "comma", "dl": "1"}, timeout=600)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), na_values=["M", ""])


def icn_stations():
    """Illinois Climate Network station codes and names, plus the access caveat."""
    st = derechos_stations()
    return {"stations": st["icn_sites"], "domain_subset": st["icn_domain_subset"],
            "access": "Station metadata pages under warm.isws.illinois.edu/warm/climnet/ are "
                      "public. Bulk data (/warm/cdflist.asp) returns an 'Access WARM Data - "
                      "Login' page: an ISWS account is required. Route the request through "
                      "co-author Trent Ford (Illinois State Climatologist, ISWS).",
            "note": st["icn_note"] if "icn_note" in st else ""}


def ameriflux_status():
    """Why AmeriFlux has no working recipe here, and what to do about it."""
    return {"hosts_tried": ["amfcdata.lbl.gov", "ameriflux-data.lbl.gov", "ameriflux.lbl.gov"],
            "result": "amfcdata.lbl.gov and ameriflux-data.lbl.gov: proxy CONNECT tunnel returns "
                      "502 Bad Gateway on every attempt even after the domain was allowlisted. "
                      "ameriflux.lbl.gov: HTTP 403 from nginx. Not verified from this sandbox.",
            "documented_api": "The amerifluxr R client uses GET amfcdata.lbl.gov/api/v1/"
                              "site_display/AmeriFlux for the site table, /api/v1/data_"
                              "availability/AmeriFlux/<SITE> for coverage, and a POST to "
                              "/api/v1/data_download carrying user_id, user_email, data_product "
                              "(BASE-BADM), data_policy (CCBY4.0), site_ids and intended_use. "
                              "UNVERIFIED from here - treat as a starting point, not a recipe.",
            "action": "An AmeriFlux account is needed regardless (downloads are logged against a "
                      "user id and the data policy must be accepted). Register the DERECHOS "
                      "ATMOS and downtown-Chicago tower site IDs, then re-test."}


def derechos_nexrad_keys(site, start, end, min_bytes=2000000):
    """List Level II volume keys for KDVN or KLOT from the Unidata archive bucket.

    Anonymous S3, no credentials. Filters *_V06_MDM sidecars by size.
    nexrad-aws-2025 is the fuller reference (VCPs, split cuts, SAILS/MRLE/AVSET, ARCO).
    """
    import boto3
    import botocore
    from botocore import UNSIGNED
    from botocore.client import Config
    import datetime as dtm
    cl = boto3.client("s3", region_name="us-east-1", config=Config(signature_version=UNSIGNED))
    s = start if hasattr(start, "year") else dtm.datetime.fromisoformat(str(start))
    e = end if hasattr(end, "year") else dtm.datetime.fromisoformat(str(end))
    out = []
    day = dtm.datetime(s.year, s.month, s.day)
    while day <= e:
        prefix = "%04d/%02d/%02d/%s/" % (day.year, day.month, day.day, site.upper())
        tok = None
        while True:
            kw = {"Bucket": NEXRAD_BUCKET, "Prefix": prefix}
            if tok:
                kw["ContinuationToken"] = tok
            resp = cl.list_objects_v2(**kw)
            for o in resp.get("Contents", []):
                if o["Size"] < min_bytes or o["Key"].endswith("_MDM"):
                    continue
                m = re.search(r"(\d{8})_(\d{6})", o["Key"])
                if not m:
                    continue
                t = dtm.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")
                if s <= t <= e:
                    out.append({"key": o["Key"], "time": t, "size": o["Size"]})
            if not resp.get("IsTruncated"):
                break
            tok = resp.get("NextContinuationToken")
        day = day + dtm.timedelta(days=1)
    return sorted(out, key=lambda d: d["time"])


def cdl_point(lat, lon, year):
    """USDA Cropland Data Layer class at one point. Returns {'value','category','color'}."""
    import requests
    from pyproj import Transformer
    tf = Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True)
    x, y = tf.transform(lon, lat)
    r = requests.get(CDL + "/GetCDLValue", params={"year": int(year), "x": x, "y": y}, timeout=180)
    r.raise_for_status()
    return cdl_parse(r.text)


def cdl_parse(text):
    """Parse a CropScape response body.

    CropScape's 'format=json' is a JavaScript object literal with UNQUOTED keys and is
    NOT valid JSON - json.loads() raises. This quotes the keys first.
    """
    m = re.search(r"<Result>(.*?)</Result>", text, re.S)
    body = m.group(1) if m else text
    m2 = re.search(r"<returnURL>(.*?)</returnURL>", text, re.S)
    if m2:
        return {"returnURL": m2.group(1)}
    fixed = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', body)
    return json.loads(fixed)


def cdl_stats(lat, lon, year, half_km=5.0):
    """CDL class areas in a square box around a point, as a DataFrame (acreage per class)."""
    import requests
    import pandas as pd
    from pyproj import Transformer
    tf = Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True)
    x, y = tf.transform(lon, lat)
    h = half_km * 1000.0
    bbox = "%f,%f,%f,%f" % (x - h, y - h, x + h, y + h)
    r = requests.get(CDL + "/GetCDLStat", params={"year": int(year), "bbox": bbox,
                                                 "format": "json"}, timeout=300)
    r.raise_for_status()
    url = cdl_parse(r.text)["returnURL"]
    body = requests.get(url, timeout=300).text
    fixed = re.sub(r"([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:", r'\1"\2":', body)
    d = json.loads(fixed)
    df = pd.DataFrame(d["rows"])
    return df.sort_values("acreage", ascending=False).reset_index(drop=True)


def cdl_clip(lat, lon, year, half_km=5.0, path=None):
    """Download a CDL GeoTIFF clipped to a box around a point. Returns the local path.

    The raster is EPSG:5070 Albers, 30 m, uint8 class codes.
    """
    import requests
    from pyproj import Transformer
    tf = Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True)
    x, y = tf.transform(lon, lat)
    h = half_km * 1000.0
    bbox = "%f,%f,%f,%f" % (x - h, y - h, x + h, y + h)
    r = requests.get(CDL + "/GetCDLFile", params={"year": int(year), "bbox": bbox}, timeout=300)
    r.raise_for_status()
    url = cdl_parse(r.text)["returnURL"]
    path = path or ("cdl_%s_%.3f_%.3f.tif" % (year, lat, lon))
    with open(path, "wb") as fh:
        fh.write(requests.get(url, timeout=600).content)
    return path


def mping_reports(start, end, bbox=None, token=None, max_pages=200, **filters):
    """mPING crowdsourced reports as a DataFrame, spatially subset and paginated.

    CRITICAL: the parameter that actually subsets space is 'in_bbox'. Passing 'bbox'
    (or lonmin/latmin, geom_within, lat+lon+radius, state) is accepted with HTTP 200
    and SILENTLY IGNORED, returning the global report set. Verified: identical counts
    with and without 'bbox', results spanning lon -151 to +32.
    Page size is 5000; 'next' comes back as http:// and is upgraded to https here.
    filters: category='Rain/Snow', description='Freezing Rain', ...
    """
    import requests
    import pandas as pd
    token = token or derechos_credential("MPINGTOK")
    bbox = bbox or DERECHOS_BBOX
    if not isinstance(bbox, str):
        bbox = ",".join(str(v) for v in bbox)
    params = {"in_bbox": bbox, "obtime_gte": mping_stamp(start), "obtime_lte": mping_stamp(end)}
    params.update(filters)
    headers = {"Authorization": "Token %s" % token, "Accept": "application/json"}
    rows = []
    url = MPING
    n = 0
    while url and n < max_pages:
        r = requests.get(url, headers=headers, params=params if n == 0 else None, timeout=300)
        r.raise_for_status()
        j = r.json()
        for x in j.get("results", []):
            c = x.get("geom", {}).get("coordinates", [None, None])
            rows.append({"id": x.get("id"), "obtime": x.get("obtime"),
                         "category": x.get("category"), "description": x.get("description"),
                         "description_id": x.get("description_id"), "lon": c[0], "lat": c[1]})
        nxt = j.get("next")
        url = nxt.replace("http://", "https://") if nxt else None
        n = n + 1
    df = pd.DataFrame(rows)
    if len(df):
        df["obtime"] = pd.to_datetime(df["obtime"])
    return df


def mping_stamp(v):
    """Format a date/datetime for the mPING obtime filters."""
    v = str(v)
    if "T" in v:
        v = v.replace("T", " ").replace("Z", "")
    if len(v) == 10:
        v = v + " 00:00:00"
    return v


def s2_search(lat, lon, start, end, max_cloud=20, collection="sentinel-2-l2a"):
    """Search Sentinel-2 on the Element84 STAC API (anonymous). Returns pystac Items."""
    from pystac_client import Client
    cl = Client.open(E84)
    srch = cl.search(collections=[collection],
                     intersects={"type": "Point", "coordinates": [lon, lat]},
                     datetime="%s/%s" % (start, end),
                     query={"eo:cloud_cover": {"lt": max_cloud}})
    return list(srch.items())


def s2_ndvi(lat, lon, start, end, half_m=1500, max_cloud=20):
    """NDVI statistics in a box around a point from the least-cloudy Sentinel-2 scene.

    Reads only the needed window out of the red/nir COGs, so this costs a few MB.
    """
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    from pyproj import Transformer
    items = s2_search(lat, lon, start, end, max_cloud=max_cloud)
    if not items:
        return None
    it = sorted(items, key=lambda i: i.properties.get("eo:cloud_cover", 100))[0]
    band = {}
    for name in ("red", "nir"):
        with rasterio.open(it.assets[name].href) as ds:
            tf = Transformer.from_crs("EPSG:4326", ds.crs, always_xy=True)
            cx, cy = tf.transform(lon, lat)
            w = from_bounds(cx - half_m, cy - half_m, cx + half_m, cy + half_m, ds.transform)
            band[name] = ds.read(1, window=w).astype("float32") / 10000.0
    ndvi = (band["nir"] - band["red"]) / (band["nir"] + band["red"])
    return {"item_id": it.id, "datetime": str(it.datetime),
            "cloud_cover": it.properties.get("eo:cloud_cover"),
            "shape": list(ndvi.shape), "ndvi_mean": float(np.nanmean(ndvi)),
            "ndvi_p10": float(np.nanpercentile(ndvi, 10)),
            "ndvi_p90": float(np.nanpercentile(ndvi, 90))}


def cdse_search(lat, lon, start, end, collection="SENTINEL-2", top=10):
    """Copernicus Data Space OData catalogue search. Anonymous - no token needed.

    Product DOWNLOAD does need a CDSE bearer token, which the configured ESATOK is not
    (it is an ESA MAAP offline token, issuer iam.maap.eo.esa.int).
    """
    import requests
    flt = ("Collection/Name eq '%s' and OData.CSC.Intersects(area=geography'SRID=4326;"
           "POINT(%f %f)') and ContentDate/Start gt %sT00:00:00.000Z and "
           "ContentDate/Start lt %sT00:00:00.000Z") % (collection, lon, lat, start, end)
    r = requests.get(CDSE_ODATA, params={"$filter": flt, "$top": int(top)}, timeout=180)
    r.raise_for_status()
    return [{"name": p["Name"], "id": p["Id"], "start": p.get("ContentDate", {}).get("Start")}
            for p in r.json()["value"]]


def hrrr_field(when, search, fxx=0, product="sfc", model="hrrr"):
    """One HRRR field as an xarray Dataset from the AWS open-data archive via Herbie.

    search is a Herbie/wgrib2 regex on the .idx inventory, e.g. ':CAPE:surface:anl:'.
    HRRR longitudes are 0-360; hrrr_point handles the conversion.
    """
    from herbie import Herbie
    H = Herbie(str(when), model=model, product=product, fxx=int(fxx), priority=["aws"])
    return H.xarray(search, remove_grib=False)


def hrrr_point(when, search, lat, lon, fxx=0, product="sfc"):
    """Nearest-gridpoint HRRR value at a lat/lon. Returns a dict with the value and grid point."""
    import numpy as np
    ds = hrrr_field(when, search, fxx=fxx, product=product)
    glat = ds.latitude.values
    glon = ds.longitude.values
    tgt = lon + 360.0 if glon.max() > 180.0 and lon < 0 else lon
    d = (glat - lat) ** 2 + (glon - tgt) ** 2
    i, j = np.unravel_index(np.argmin(d), d.shape)
    var = [v for v in ds.data_vars if ds[v].ndim == 2]
    val = float(ds[var[0]].values[i, j]) if var else None
    return {"variable": var[0] if var else None, "value": val,
            "grid_lat": float(glat[i, j]), "grid_lon": float(glon[i, j]),
            "valid_time": str(ds.valid_time.values) if "valid_time" in ds else None}


def hrrr_inventory(when, search=None, fxx=0, product="sfc"):
    """HRRR .idx inventory as a DataFrame, for discovering search strings."""
    from herbie import Herbie
    H = Herbie(str(when), model="hrrr", product=product, fxx=int(fxx), priority=["aws"])
    return H.inventory(search) if search else H.inventory()
