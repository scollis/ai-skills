
"""Helpers for derechos-landuse-imagery. Verified live 2026-09-05."""
import os
import re
import json

LANDUSE_BBOX = [-94.2, 40.7, -87.4, 42.6]
DERECHOS_SITES = {"M1": (41.1933, -91.4839), "S1": (41.356, -91.136),
                  "NIU": (41.93, -88.77), "NACHUSA": (41.858, -89.652)}
PLANET_DATA_V1 = "https://api.planet.com/data/v1"
CMR_SEARCH = "https://cmr.earthdata.nasa.gov/search"
APPEEARS_API = "https://appeears.earthdatacloud.nasa.gov/api"
NASS_API = "https://quickstats.nass.usda.gov/api"
MRLC_WCS = "https://www.mrlc.gov/geoserver/wcs"
MRLC_WMS = "https://www.mrlc.gov/geoserver/wms"
PC_STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
PC_SAS = "https://planetarycomputer.microsoft.com/api/sas/v1/token"
CROPSCAPE = "https://nassgeodata.gmu.edu/axis2/services/CDLService"
GDAL_ENV = {"GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR", "GDAL_HTTP_MAX_RETRY": 4,
            "GDAL_HTTP_RETRY_DELAY": 2, "VSI_CACHE": True, "GDAL_CACHEMAX": 512}
NLCD_CLASSES = {11: "Open Water", 12: "Perennial Ice/Snow", 21: "Developed, Open Space",
                22: "Developed, Low Intensity", 23: "Developed, Medium Intensity",
                24: "Developed, High Intensity", 31: "Barren Land", 41: "Deciduous Forest",
                42: "Evergreen Forest", 43: "Mixed Forest", 52: "Shrub/Scrub", 71: "Herbaceous",
                81: "Hay/Pasture", 82: "Cultivated Crops", 90: "Woody Wetlands",
                95: "Emergent Herbaceous Wetlands"}
LCMAP_CLASSES = {0: "No Data", 1: "Developed", 2: "Cropland", 3: "Grass/Shrub", 4: "Tree Cover",
                 5: "Water", 6: "Wetlands", 7: "Snow/Ice", 8: "Barren"}
CDL_NONCROP = (0, 63, 64, 65, 81, 82, 83, 87, 88, 92, 111, 112, 121, 122, 123, 124, 131,
               141, 142, 143, 152, 171, 176, 181, 190, 195)


def albers5070(lat, lon):
    from pyproj import Transformer
    return Transformer.from_crs("EPSG:4326", "EPSG:5070", always_xy=True).transform(lon, lat)


def albers5070_bbox(bbox=None):
    if bbox is None:
        bbox = LANDUSE_BBOX
    xs, ys = [], []
    for lo, la in [(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[2], bbox[3]), (bbox[0], bbox[3])]:
        x, y = albers5070(la, lo)
        xs.append(x); ys.append(y)
    return min(xs), max(xs), min(ys), max(ys)


def planet_probe():
    """What api.planet.com answers with no credential. Verified 2026-09-05."""
    import requests
    out = {}
    for path, url in [("data_v1_root", PLANET_DATA_V1 + "/"),
                      ("data_v1_spec", PLANET_DATA_V1 + "/spec"),
                      ("item_types", PLANET_DATA_V1 + "/item-types"),
                      ("basemaps", "https://api.planet.com/basemaps/v1/mosaics"),
                      ("subscriptions", "https://api.planet.com/subscriptions/v1/"),
                      ("orders", "https://api.planet.com/compute/ops/orders/v2")]:
        try:
            r = requests.get(url, timeout=30)
            out[path] = {"status": r.status_code, "body": r.text[:160]}
        except Exception as exc:
            out[path] = {"status": "EXC", "body": "%s: %s" % (type(exc).__name__, str(exc)[:120])}
    return out


def planet_search_payload(bbox=None, start=None, end=None, item_types=None, max_cloud=0.2):
    """Build a Data API v1 quick-search body over a lon/lat bbox."""
    if bbox is None:
        bbox = LANDUSE_BBOX
    if item_types is None:
        item_types = ["PSScene"]
    if start is None:
        start = "2020-08-09T00:00:00Z"
    if end is None:
        end = "2020-08-12T00:00:00Z"
    geom = {"type": "Polygon", "coordinates": [[[bbox[0], bbox[1]], [bbox[2], bbox[1]],
                                                [bbox[2], bbox[3]], [bbox[0], bbox[3]],
                                                [bbox[0], bbox[1]]]]}
    return {"item_types": list(item_types),
            "filter": {"type": "AndFilter", "config": [
                {"type": "GeometryFilter", "field_name": "geometry", "config": geom},
                {"type": "DateRangeFilter", "field_name": "acquired",
                 "config": {"gte": start, "lte": end}},
                {"type": "RangeFilter", "field_name": "cloud_cover",
                 "config": {"lte": max_cloud}},
                {"type": "PermissionFilter", "config": ["assets:download"]}]}}


def planet_quick_search(api_key, bbox=None, start=None, end=None, item_types=None,
                        max_cloud=0.2, page_size=250):
    """POST /data/v1/quick-search with HTTP basic auth (key as username, empty password)."""
    import requests
    from requests.auth import HTTPBasicAuth
    body = planet_search_payload(bbox, start, end, item_types, max_cloud)
    r = requests.post(PLANET_DATA_V1 + "/quick-search", json=body,
                      params={"_page_size": page_size},
                      auth=HTTPBasicAuth(api_key, ""), timeout=120)
    if r.status_code != 200:
        return {"status": r.status_code, "body": r.text[:400], "sent": body}
    j = r.json()
    return {"status": 200, "n": len(j.get("features", [])),
            "ids": [f["id"] for f in j.get("features", [])][:20], "raw": j}


def cmr_granules(short_name, bbox=None, start=None, end=None, page_size=50, version=None):
    """CMR granule search. Returns (n_hits, entries)."""
    import requests
    if bbox is None:
        bbox = LANDUSE_BBOX
    p = {"short_name": short_name, "bounding_box": ",".join(str(v) for v in bbox),
         "page_size": page_size}
    if start and end:
        p["temporal"] = "%s,%s" % (start, end)
    if version:
        p["version"] = version
    r = requests.get(CMR_SEARCH + "/granules.json", params=p, timeout=120)
    r.raise_for_status()
    return int(r.headers.get("CMR-Hits", 0)), r.json()["feed"]["entry"]


def hls_presign(url, token=None):
    """Resolve an LP DAAC protected URL to its presigned CloudFront URL."""
    import requests
    if token is None:
        token = os.environ["NASAEDTOKEN"]
    r = requests.get(url, headers={"Authorization": "Bearer " + token},
                     allow_redirects=False, timeout=90)
    if r.status_code in (301, 302, 303, 307, 308):
        return r.headers["location"]
    raise RuntimeError("expected a redirect from LP DAAC, got HTTP %d" % r.status_code)


def hls_download(url, dest, token=None):
    """Authenticated LP DAAC download with Content-Length verification."""
    import requests
    pre = hls_presign(url, token)
    r = requests.get(pre, timeout=600, stream=True)
    r.raise_for_status()
    n = 0
    with open(dest + ".part", "wb") as fh:
        for chunk in r.iter_content(1 << 20):
            fh.write(chunk); n += len(chunk)
    cl = r.headers.get("Content-Length")
    if cl and int(cl) != n:
        raise IOError("short read: %d of %s bytes" % (n, cl))
    os.replace(dest + ".part", dest)
    return n


def hls_window(url, lat, lon, half_m=300.0, token=None):
    """Windowed read of one HLS band around a point. Returns a float array with fill as NaN."""
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    pre = hls_presign(url, token)
    x, y = None, None
    with rasterio.Env(**GDAL_ENV):
        with rasterio.open("/vsicurl/" + pre) as ds:
            from pyproj import Transformer
            x, y = Transformer.from_crs("EPSG:4326", ds.crs, always_xy=True).transform(lon, lat)
            win = from_bounds(x - half_m, y - half_m, x + half_m, y + half_m, ds.transform)
            arr = ds.read(1, window=win).astype("float32")
            if ds.nodata is not None:
                arr[arr == ds.nodata] = np.nan
    return arr


def hls_ndvi(granule_entry, lat, lon, half_m=300.0, token=None):
    """NDVI from one HLS granule. S30 uses B08/B04, L30 uses B05/B04."""
    import numpy as np
    hrefs = [l["href"] for l in granule_entry["links"] if l["href"].endswith(".tif")]
    gid = granule_entry["producer_granule_id"]
    nir_band = "B05" if ".L30." in gid else "B08"
    red = [h for h in hrefs if h.endswith("B04.tif")][0]
    nir = [h for h in hrefs if h.endswith(nir_band + ".tif")][0]
    r = hls_window(red, lat, lon, half_m, token)
    n = hls_window(nir, lat, lon, half_m, token)
    return {"granule": gid, "nir_band": nir_band,
            "red_mean_dn": float(np.nanmean(r)), "nir_mean_dn": float(np.nanmean(n)),
            "ndvi": float(np.nanmean((n - r) / (n + r))), "n_valid": int(np.isfinite(r).sum())}


def appeears_products(pattern=None):
    """Public AppEEARS product catalogue, optionally regex-filtered."""
    import requests
    r = requests.get(APPEEARS_API + "/product", timeout=90)
    r.raise_for_status()
    prods = r.json()
    if pattern:
        rx = re.compile(pattern, re.I)
        prods = [p for p in prods
                 if rx.search(p.get("ProductAndVersion", "") + " " + p.get("Description", ""))]
    return [{"product": p["ProductAndVersion"], "res": p.get("Resolution"),
             "cadence": p.get("TemporalGranularity"), "start": p.get("TemporalExtentStart"),
             "end": p.get("TemporalExtentEnd"), "desc": p.get("Description")} for p in prods]


def appeears_layers(product):
    """Layer names for one AppEEARS product (public endpoint)."""
    import requests
    r = requests.get(APPEEARS_API + "/product/" + product, timeout=90)
    r.raise_for_status()
    return sorted(r.json().keys())


def nass_key_help():
    """How to obtain a Quick Stats key. No key is configured in this sandbox."""
    return {"register_url": NASS_API,
            "form_fields": ["name", "email", "agree"],
            "method": "POST to https://quickstats.nass.usda.gov/api",
            "delivery": "key is emailed immediately",
            "record_limit": 50000,
            "note": "Every /api path returns HTTP 401 {\"error\":[\"unauthorized\"]} without a key."}


def nass_query(key, fmt="JSON", **params):
    """GET /api/api_GET. Pass commodity_desc, statisticcat_desc, agg_level_desc, etc."""
    import requests
    p = dict(params); p["key"] = key; p["format"] = fmt
    r = requests.get(NASS_API + "/api_GET/", params=p, timeout=180)
    if r.status_code != 200:
        return {"status": r.status_code, "body": r.text[:300]}
    if fmt.upper() == "JSON":
        return r.json()
    return r.text


def nass_count(key, **params):
    """GET /api/get_counts - check the 50k record cap before a big pull."""
    import requests
    p = dict(params); p["key"] = key
    r = requests.get(NASS_API + "/get_counts/", params=p, timeout=180)
    return r.json() if r.status_code == 200 else {"status": r.status_code, "body": r.text[:300]}


def pc_sas(collection):
    """Planetary Computer SAS token for a collection (anonymous, ~1 h validity)."""
    import requests
    r = requests.get("%s/%s" % (PC_SAS, collection), timeout=60)
    r.raise_for_status()
    return r.json()["token"]


def pc_search(collection, bbox=None, query=None, limit=500):
    """Paged STAC item search. Returns a list of features."""
    import requests
    if bbox is None:
        bbox = LANDUSE_BBOX
    body = {"collections": [collection], "bbox": list(bbox), "limit": limit}
    if query:
        body["query"] = query
    out = []
    while True:
        r = requests.post(PC_STAC + "/search", json=body, timeout=240)
        r.raise_for_status()
        j = r.json()
        out += j["features"]
        nxt = [l for l in j.get("links", []) if l.get("rel") == "next"]
        if not nxt or not nxt[0].get("body"):
            break
        body = nxt[0]["body"]
    return out


def cdl_class_names():
    """CDL code -> class name, from the Planetary Computer STAC classification extension."""
    import requests
    r = requests.get(PC_STAC + "/collections/usda-cdl", timeout=60)
    r.raise_for_status()
    cls = r.json()["item_assets"]["cropland"]["classification:classes"]
    return {int(c["value"]): (c.get("description") or c.get("name")) for c in cls}


def cog_point(href, sas, x_albers, y_albers):
    """Single-pixel read from a COG in EPSG:5070. None if the point is outside the tile."""
    import rasterio
    from rasterio.windows import Window
    with rasterio.Env(**GDAL_ENV):
        with rasterio.open("/vsicurl/%s?%s" % (href, sas)) as ds:
            bx0, by0, bx1, by1 = ds.bounds
            if not (bx0 <= x_albers < bx1 and by0 <= y_albers < by1):
                return None
            row, col = ds.index(x_albers, y_albers)
            return int(ds.read(1, window=Window(col, row, 1, 1))[0, 0])


def cog_window_hist(href, sas, x_albers, y_albers, half_m=510.0):
    """256-bin histogram of a square window from a COG in EPSG:5070."""
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    with rasterio.Env(**GDAL_ENV):
        with rasterio.open("/vsicurl/%s?%s" % (href, sas)) as ds:
            bx0, by0, bx1, by1 = ds.bounds
            if not (bx0 <= x_albers < bx1 and by0 <= y_albers < by1):
                return None
            win = from_bounds(x_albers - half_m, y_albers - half_m,
                              x_albers + half_m, y_albers + half_m, ds.transform)
            arr = ds.read(1, window=win)
    return np.bincount(arr.ravel(), minlength=256).astype("int64")


def cdl_field_crop(lat, lon, year, half_m=510.0, items=None, sas=None, names=None):
    """Dominant CDL *crop* class in a square window - the field-scale label.

    Use this rather than a single-pixel query: the S1 station pixel reads
    Developed/Open Space in 2008-2018.
    """
    import numpy as np
    if items is None:
        items = pc_search("usda-cdl", query={"usda_cdl:type": {"eq": "cropland"}})
    if sas is None:
        sas = pc_sas("usda-cdl")
    if names is None:
        names = cdl_class_names()
    x, y = albers5070(lat, lon)
    for it in items:
        if int(re.search(r"_(\d{4})_", it["id"]).group(1)) != int(year):
            continue
        hist = cog_window_hist(it["assets"]["cropland"]["href"], sas, x, y, half_m)
        if hist is None:
            continue
        crop = hist.copy()
        for c in CDL_NONCROP:
            crop[c] = 0
        dom = int(np.argmax(crop))
        return {"year": int(year), "code": dom, "crop": names.get(dom),
                "dominant_frac": float(crop[dom] / hist.sum()),
                "crop_frac": float(crop.sum() / hist.sum()),
                "n_px": int(hist.sum())}
    return None


def cdl_domain_counts(year, bbox=None, items=None, sas=None, workers=8):
    """Exact 30 m class-pixel counts for one CDL year clipped to a lon/lat bbox."""
    import numpy as np
    import rasterio
    from rasterio.windows import from_bounds
    from concurrent.futures import ThreadPoolExecutor
    if items is None:
        items = pc_search("usda-cdl", bbox=bbox, query={"usda_cdl:type": {"eq": "cropland"}})
    if sas is None:
        sas = pc_sas("usda-cdl")
    x0, x1, y0, y1 = albers5070_bbox(bbox)

    def one(it):
        with rasterio.Env(**GDAL_ENV):
            with rasterio.open("/vsicurl/%s?%s" % (it["assets"]["cropland"]["href"], sas)) as ds:
                bx0, by0, bx1, by1 = ds.bounds
                ix0, ix1 = max(x0, bx0), min(x1, bx1)
                iy0, iy1 = max(y0, by0), min(y1, by1)
                if ix0 >= ix1 or iy0 >= iy1:
                    return np.zeros(256, dtype="int64")
                arr = ds.read(1, window=from_bounds(ix0, iy0, ix1, iy1, ds.transform))
        return np.bincount(arr.ravel(), minlength=256).astype("int64")

    sel = [i for i in items if int(re.search(r"_(\d{4})_", i["id"]).group(1)) == int(year)]
    with ThreadPoolExecutor(workers) as ex:
        parts = list(ex.map(one, sel))
    return sum(parts)


def cdl_frequency(lat, lon, band="corn", half_m=510.0):
    """CDL crop-frequency (years planted, 2008-2021). 255 is nodata and MUST be masked."""
    import numpy as np
    items = pc_search("usda-cdl", query={"usda_cdl:type": {"eq": "frequency"}})
    sas = pc_sas("usda-cdl")
    x, y = albers5070(lat, lon)
    for it in items:
        if band not in it["assets"]:
            continue
        pt = cog_point(it["assets"][band]["href"], sas, x, y)
        if pt is None:
            continue
        hist = cog_window_hist(it["assets"][band]["href"], sas, x, y, half_m)
        masked = hist.copy(); masked[255] = 0
        vals = np.arange(256)
        n = masked.sum()
        return {"band": band, "point_years": pt,
                "window_mean_years": float((vals * masked).sum() / n) if n else float("nan"),
                "nodata_px": int(hist[255]), "n_px": int(hist.sum())}
    return None


def lcmap_point_history(lat, lon, years=None, asset="lcpri"):
    """USGS LCMAP CONUS v1.3 annual 30 m land cover at a point, 1985-2021."""
    if years is None:
        years = [1985, 1995, 2005, 2015, 2021]
    items = pc_search("usgs-lcmap-conus-v13")
    sas = pc_sas("usgs-lcmap-conus-v13")
    x, y = albers5070(lat, lon)
    out = {}
    for yr in years:
        sel = [i for i in items if int(re.search(r"_(\d{4})_V13", i["id"]).group(1)) == int(yr)]
        for it in sel:
            v = cog_point(it["assets"][asset]["href"], sas, x, y)
            if v is not None:
                out[int(yr)] = {"code": v, "class": LCMAP_CLASSES.get(v)}
                break
    return out


def mrlc_coverages(pattern=None):
    """WCS 2.0.1 coverage ids on the MRLC GeoServer, optionally regex-filtered."""
    import requests
    r = requests.get(MRLC_WCS, params={"service": "WCS", "version": "2.0.1",
                                       "request": "GetCapabilities"}, timeout=180)
    r.raise_for_status()
    ids = re.findall(r"<wcs:CoverageId>([^<]+)</wcs:CoverageId>", r.text)
    if pattern:
        rx = re.compile(pattern, re.I)
        ids = [i for i in ids if rx.search(i)]
    return sorted(set(ids))


def mrlc_wcs_geotiff(coverage_id, dest, bbox=None, half_m=None, centre=None,
                     scalefactor=None, timeout=900):
    """GetCoverage a subset of an MRLC coverage as GeoTIFF.

    Either pass a lon/lat `bbox`, or a `centre` (lat, lon) plus `half_m`.
    A full-domain 30 m request drops the connection - use scalefactor<=0.1 for
    domain-wide work and full resolution only for site windows.
    """
    import requests
    if centre is not None:
        cx, cy = albers5070(centre[0], centre[1])
        h = 5000.0 if half_m is None else float(half_m)
        x0, x1, y0, y1 = cx - h, cx + h, cy - h, cy + h
    else:
        x0, x1, y0, y1 = albers5070_bbox(bbox)
    p = {"service": "WCS", "version": "2.0.1", "request": "GetCoverage",
         "coverageId": coverage_id, "format": "image/tiff",
         "subset": ["X(%f,%f)" % (x0, x1), "Y(%f,%f)" % (y0, y1)]}
    if scalefactor:
        p["scalefactor"] = scalefactor
    try:
        r = requests.get(MRLC_WCS, params=p, timeout=timeout, stream=True)
    except Exception as exc:
        return {"ok": False, "error": "%s: %s" % (type(exc).__name__, str(exc)[:160])}
    ct = r.headers.get("Content-Type", "")
    if r.status_code != 200 or "tiff" not in ct:
        return {"ok": False, "status": r.status_code, "content_type": ct, "body": r.text[:300]}
    n = 0
    with open(dest + ".part", "wb") as fh:
        for chunk in r.iter_content(1 << 20):
            fh.write(chunk); n += len(chunk)
    os.replace(dest + ".part", dest)
    return {"ok": True, "path": dest, "bytes": n}


def cropscape_point(lat, lon, year, timeout=180, attempts=3):
    """CropScape GetCDLValue. DEGRADED as of 2026-09-05: expect ~1 in 3 to time out."""
    import time
    import requests
    x, y = albers5070(lat, lon)
    last = None
    for _ in range(attempts):
        try:
            r = requests.get(CROPSCAPE + "/GetCDLValue",
                             params={"year": str(year), "x": "%.2f" % x, "y": "%.2f" % y},
                             timeout=timeout)
            if r.status_code == 200:
                m = re.search(r'value:\s*(-?\d+),\s*category:\s*"([^"]*)"', r.text)
                if m:
                    return {"year": int(year), "code": int(m.group(1)), "category": m.group(2)}
                return {"year": int(year), "raw": r.text[:240]}
            last = "HTTP %d" % r.status_code
        except Exception as exc:
            last = "%s" % type(exc).__name__
        time.sleep(5)
    return {"year": int(year), "error": last}


def derechos_landuse_sources(sq=None):
    """Source -> science-question table for this skill."""
    rows = [
        {"source": "Planet Labs Data API v1", "host": "api.planet.com", "status": "auth_required",
         "sq": "SQ1,SQ2,SQ4", "provides": "PlanetScope 3 m daily / SkySat; field-scale surface state"},
        {"source": "NASA HLS (HLSS30/HLSL30)", "host": "data.lpdaac.earthdatacloud.nasa.gov",
         "status": "verified", "sq": "SQ1,SQ2,SQ4,SQ5",
         "provides": "30 m harmonized Landsat+Sentinel-2 reflectance, ~2-3 day revisit"},
        {"source": "NASA AppEEARS", "host": "appeears.earthdatacloud.nasa.gov",
         "status": "auth_required", "sq": "SQ1,SQ2",
         "provides": "point/area extraction for 187 MODIS/VIIRS/ECOSTRESS/SMAP/Landsat products"},
        {"source": "NASA CMR", "host": "cmr.earthdata.nasa.gov", "status": "verified",
         "sq": "SQ1,SQ2,SQ3", "provides": "granule discovery for MOD16 ET, MCD12Q1, LAI, LST, ECOSTRESS"},
        {"source": "USDA NASS Quick Stats", "host": "quickstats.nass.usda.gov",
         "status": "auth_required", "sq": "SQ1,SQ4",
         "provides": "county corn/soy acreage, yield, planting progress"},
        {"source": "USDA CDL via Planetary Computer", "host": "planetarycomputer.microsoft.com",
         "status": "verified", "sq": "SQ1,SQ2,SQ4,SQ5",
         "provides": "annual 30 m crop type 2008-2021 + crop-frequency and cultivated layers"},
        {"source": "USDA CropScape", "host": "nassgeodata.gmu.edu", "status": "partial",
         "sq": "SQ1,SQ2", "provides": "point/stat/clip CDL 1999-2024, including 2022-2024"},
        {"source": "NLCD via MRLC GeoServer", "host": "www.mrlc.gov", "status": "verified",
         "sq": "SQ1,SQ2,SQ4", "provides": "30 m land cover, impervious fraction, tree-canopy cover"},
        {"source": "USGS LCMAP CONUS v1.3", "host": "planetarycomputer.microsoft.com",
         "status": "verified", "sq": "SQ1,SQ2",
         "provides": "annual 30 m land cover + change magnitude/date, 1985-2021"},
    ]
    if sq is None:
        return rows
    tag = "SQ%d" % int(sq)
    return [r for r in rows if tag in r["sq"]]
