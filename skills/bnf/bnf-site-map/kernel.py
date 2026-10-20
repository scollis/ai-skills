"""Map layers, imagery and the multi-panel asset map for ARM BNF (AMF3).

Exec-loaded sidecar: top level holds only stdlib imports, functions and
literals. cartopy, geopandas, osmnx, matplotlib and pyproj are imported inside
the functions that need them.
"""
import math
import os
import re
import time


def map_config():
    """Boxes (W, E, S, N), sources, styles and label layout."""
    return dict(
        main=(-87.70, -86.84, 34.10, 34.72),
        inset=(-92.0, -82.0, 29.6, 37.0),
        layer_zoom=(-87.74, 34.06, -86.80, 34.76),        # W, S, E, N
        layer_inset=(-93.5, 28.5, -80.5, 38.0),
        # close-ups: letter -> (centre key, half-width m, half-height m,
        # imagery zoom, title)
        closeups={
            "b": ("M1_S10", 1200, 800, 16, "M1 main site and S10 tower"),
            "c": ("s10_tower", 75, 50, 19, "Tower complex: S10, S13, S14"),
            "d": ("s3_csapr2", 450, 300, 17, "S3: C-SAPR2"),
            "e": ("s4_sacr", 450, 300, 17, "S4: SACR"),
            "f": ("s20", 450, 300, 17, "S20: Courtland"),
            "g": ("s30", 450, 300, 17, "S30: Falkville"),
            "h": ("s40", 450, 300, 17, "S40: Double Springs"),
            "i": ("u2_takeoff", 2000, 1333, 15,
                  "U2: ArcticShark, Posey Field"),
        },
        # main-map labels: key -> (text, dx, dy) in offset points
        lab_main={
            "m1": ("M1 main site (b)", 16, -24),
            "s10_tower": ("S10 tower (b, c)", -16, 22),
            "s3_csapr2": ("S3 C-SAPR2 (d)", 14, 14),
            "s4_sacr": ("S4 SACR (e)", 16, -4),
            "s20": ("S20 Courtland (f)", 14, 18),
            "s30": ("S30 Falkville (g)", -12, 22),
            "s40": ("S40 Double Springs (h)", 16, -16),
            "u2_takeoff": ("U2 ArcticShark (i)", 12, 22),
        },
        # region labels on the main map; "" draws the marker unlabelled
        lab_region={
            "9a4": ("Courtland airport (AWOS,\nUSRCRN, LMA K, PSL)", 8,
                    -40),
            "lma_n": ("LMA N", 8, -12), "moua1": ("COOP MOUA1", -8, 10),
            "hvla1": ("COOP HVLA1", 6, -14), "cmd": ("AWOS CMD", -8, 10),
            "usgs_03586500": ("USGS 03586500", 8, 12),
            "aqs_01_103_0011": ("AQS 01-103-0011", 10, 14),
            "lma_j": ("LMA J", -10, -4), "wpta1": ("COOP WPTA1", -8, 12),
            "lcxa1": ("", 0, 0), "lma_k": ("", 0, 0), "psl_ctd": ("", 0, 0),
        },
        # fixed close-up label slots: key -> (text or None, x, y, ha) in
        # axes fraction, placed clear of every marker
        lab_detail={
            "b": {"sonde_launch": ("M1 sonde launch\n(first fix, 0.01°)",
                                   0.45, 0.88, "right"),
                  "m1": (None, 0.99, 0.86, "right"),
                  "bhfa1": ("RAWS BHFA1", 0.99, 0.72, "right"),
                  "improve_sips1": (None, 0.55, 0.36, "right"),
                  "m1_dl": (None, 0.99, 0.27, "right"),
                  "m1_csphot": (None, 0.99, 0.19, "right"),
                  "m1_aeri": (None, 0.99, 0.11, "right"),
                  "tbs_launch": ("M1 TBS launch\n(first fix)", 0.62, 0.20,
                                 "right")},
            "i": {"1m4": ("AWOS 1M4", 0.56, 0.17, "left")},
        },
        lab_inset={
            "kgwx": ("KGWX", -6, 6), "khtx": ("KHTX", 8, 12),
            "kbmx": ("KBMX + sonde", 6, -6), "kohx": ("KOHX + sonde", 6, -6),
            "kmxx": ("KMXX", 6, 8), "knqa": ("KNQA", 6, 6),
            "khpx": ("KHPX", -6, -4), "tbna": ("TBNA", -6, -8),
            "tmem": ("TMEM", 6, -8), "nws_hun": ("NWS HUN", 6, 2),
            "armor": ("ARMOR", 6, -10),
            "neon_tall": ("NEON TALL/MAYF", 8, 0),
            "neon_dela": ("NEON DELA/BLWA", -8, 0),
            "neon_leno": ("NEON LENO/TOMB", 8, -2),
        },
        # geodesic legs: (from, to, text, side, label position along leg)
        legs=(("s3_csapr2", "m1", "S3 C-SAPR2 → M1", 1, 0.30),
              ("s4_sacr", "m1", "S4 SACR → M1", -1, 0.50)),
        # (lon, lat, text, kind) for named areas; kind sets the style
        area_labels=((-87.40, 34.255, "Bankhead\nNational Forest", "forest"),
                     (-87.41, 34.335, "Sipsey\nWilderness", "wild"),
                     (-87.06, 34.690, "Wheeler Lake\n(Tennessee River)",
                      "water"),
                     (-87.21, 34.140, "Lewis Smith\nLake", "water")),
        inset_cities=("Birmingham", "Mobile"),
        counties=("01033", "01043", "01059", "01077", "01079", "01083",
                  "01093", "01103", "01127", "01133"),
        tiger="https://www2.census.gov/geo/tiger/TIGER2024",
        cb="https://www2.census.gov/geo/tiger/GENZ2024/shp",
        usfs="https://apps.fs.usda.gov/arcx/rest/services/EDW",
        esri="https://server.arcgisonline.com/ArcGIS/rest/services",
        tile={"imagery": "World_Imagery", "hillshade":
              "Elevation/World_Hillshade"},
        fs=dict(label=13, small=11, title=15, letter=20, road=10),
        col={"ARM": "#0072B2", "NOAA": "#E69F00", "NEON": "#009E73",
             "Other": "#CC79A7"},
        size={"*": 420, "s": 130, "^": 170, "o": 80, "D": 90},
        # scanning radars only (KAZR at M1 is vertically pointing)
        radar_classes=("csapr2", "csapr", "kasacr", "sacr", "xsacr",
                       "xsapr"),
        main_keys=("m1",),
        anchor=("m1", "s10_tower"),
        net_prefix={"NWS COOP": "COOP ", "ASOS/AWOS": "AWOS ",
                    "NWS HADS": "RAWS ", "USRCRN (Alabama)": "USRCRN ",
                    "USCRN": "USCRN ", "NEXRAD WSR-88D": "",
                    "TDWR": ""},
        skip_networks=("Census geography",),
        skip_types=("polygon", "reservoir", "dam", "research centre"),
        inset_types=("radar", "radiosonde", "forecast office", "neon",
                     "core ", "gradient "),
    )


def lonlat_crs():
    """A PlateCarree that is plain lon/lat in degrees.

    With PROJ 9.8 (cartopy 0.25), ccrs.PlateCarree() is eqc on the WGS84
    ellipsoid scaled by +to_meter, which is not linear in latitude; lon/lat
    passed through it land about 24 km off near 34 N in an ellipsoidal
    projection. On a sphere globe eqc is linear and the error is zero.
    """
    import cartopy.crs as ccrs

    return ccrs.PlateCarree(globe=ccrs.Globe(
        ellipse=None, semimajor_axis=6378137, semiminor_axis=6378137))


def map_tools():
    from types import SimpleNamespace

    import cartopy.crs as ccrs
    import matplotlib.patheffects as pe
    import pyproj

    return SimpleNamespace(
        ccrs=ccrs, pc=lonlat_crs(), geod=pyproj.Geod(ellps="WGS84"),
        to_ll=pyproj.Transformer.from_crs(3857, 4326, always_xy=True),
        to_m=pyproj.Transformer.from_crs(4326, 3857, always_xy=True),
        halo=[pe.withStroke(linewidth=3.2, foreground="white")],
        halo_dk=[pe.withStroke(linewidth=3.0, foreground="black")])


# ---------------------------------------------------------------- layers

def census_layer(url, cache="layer_cache"):
    """Download (cached) a Census zip and read it as EPSG:4326."""
    import geopandas as gpd
    import requests

    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, url.rsplit("/", 1)[-1])
    if not os.path.exists(path):
        r = requests.get(url, timeout=300)
        r.raise_for_status()
        with open(path, "wb") as f:
            f.write(r.content)
    return gpd.read_file(path).to_crs(4326)


def arcgis_query(url, where, fields="*"):
    """Features from an ArcGIS REST layer as EPSG:4326 (GeoJSON output)."""
    import geopandas as gpd
    import requests

    p = dict(where=where, outFields=fields, f="geojson", outSR=4326,
             returnGeometry="true")
    js = requests.get(url + "/query", params=p, timeout=120).json()
    return gpd.GeoDataFrame.from_features(js.get("features", []), crs=4326)


def usfs_layers():
    """Bankhead Ranger District, Sipsey Wilderness and the Sipsey Fork
    Wild and Scenic River from the USFS Enterprise Data Warehouse."""
    u = map_config()["usfs"]
    return {
        "forest_district": arcgis_query(
            f"{u}/EDW_RangerDistricts_01/MapServer/0",
            "districtname LIKE '%Bankhead%'"),
        "wilderness": arcgis_query(f"{u}/EDW_Wilderness_01/MapServer/0",
                                   "wildernessname LIKE '%Sipsey%'"),
        "wild_scenic_river": arcgis_query(
            f"{u}/EDW_WildScenicRiverSegments_01/MapServer/0",
            "wsr_river_name LIKE '%Sipsey%'"),
    }


def kmz_polygons(path):
    """Polygons in a KMZ (offline fallback for the forest boundary)."""
    import zipfile
    import xml.etree.ElementTree as ET

    import geopandas as gpd
    from shapely.geometry import Polygon

    ns = {"k": "http://www.opengis.net/kml/2.2"}
    with zipfile.ZipFile(path) as z:
        kml = next(n for n in z.namelist() if n.endswith(".kml"))
        root = ET.fromstring(z.read(kml))
    out = []
    for pm in root.iter("{%s}Placemark" % ns["k"]):
        name = pm.findtext("k:name", default="", namespaces=ns)
        for ring in pm.iterfind(".//k:Polygon/k:outerBoundaryIs//"
                                "k:coordinates", ns):
            xy = [tuple(map(float, c.split(",")[:2]))
                  for c in ring.text.split()]
            out.append(dict(name=name, geometry=Polygon(xy)))
    return gpd.GeoDataFrame(out, crs=4326)


def fetch_osm(bbox, tags, tries=6, cache="layer_cache"):
    """One Overpass pull via osmnx (its user agent is accepted; the default
    python-requests agent gets HTTP 406). bbox is (W, S, E, N).

    Pulls are pickled under cache, keyed by bbox and tags. An empty box
    (osmnx InsufficientResponseError) returns an empty frame, not a retry.
    """
    import hashlib

    import geopandas as gpd
    import osmnx as ox
    import pandas as pd

    keep = ["osmid", "element", "name", "ref", "natural", "water",
            "waterway", "building", "highway", "aeroway", "man_made",
            "landuse", "barrier", "geometry"]
    os.makedirs(cache, exist_ok=True)
    h = hashlib.md5(repr((tuple(bbox), sorted(tags.items()))).encode())
    path = os.path.join(cache, f"osm_{h.hexdigest()[:12]}.pkl")
    if os.path.exists(path):
        return pd.read_pickle(path)
    # osmnx polls /api/status between requests and can wait there for many
    # minutes when Overpass is overloaded; retry here instead
    ox.settings.overpass_rate_limit = False
    ox.settings.requests_timeout = 90
    for i in range(tries):
        try:
            gdf = ox.features_from_bbox(bbox, tags).reset_index()
            gdf = gdf[[c for c in keep if c in gdf.columns]]
            break
        except ox._errors.InsufficientResponseError:
            gdf = gpd.GeoDataFrame(columns=keep, geometry="geometry",
                                   crs=4326)
            break
        except Exception as err:          # Overpass busy or timed out
            print(f"Overpass attempt {i + 1}: {err!s:.80}")
            time.sleep(20 * 2 ** i)
    else:
        raise RuntimeError("Overpass unavailable")
    gdf.to_pickle(path)
    return gdf


def clip_layer(gdf, bbox):
    import geopandas as gpd
    from shapely.geometry import box

    out = gpd.clip(gdf, box(*bbox))
    return out[~out.is_empty].reset_index(drop=True)


def pick_osm(gdf, bbox, geom=None, **tags):
    """Subset OSM features by tag (True = any value, list = any of)."""
    import numpy as np
    import pandas as pd

    keep = pd.Series(False, index=gdf.index)
    for k, v in tags.items():
        if k in gdf:
            col = gdf[k]
            keep |= col.notna() if v is True else col.isin(np.atleast_1d(v))
    out = gdf[keep]
    if geom:
        out = out[out.geom_type.isin(geom)]
    return clip_layer(out, bbox)


def closeup_boxes(A=None):
    """Close-up boxes (W, E, S, N) keyed by panel letter."""
    A = site_map_assets() if A is None else A
    out = {}
    for k, (key, hw, hh, *_) in map_config()["closeups"].items():
        r = A[A.key == key].iloc[0]
        out[k] = box_around(r.lat, r.lon, hw, hh)
    return out


def zoom_layers():
    """Network-scale layers (TIGER/CB 2024, USFS EDW, OSM) plus OSM detail
    layers for each close-up box (detail_<letter>_*)."""
    import pandas as pd

    cfg = map_config()
    zoom, tiger, cb = cfg["layer_zoom"], cfg["tiger"], cfg["cb"]
    poly = ["Polygon", "MultiPolygon"]
    line = ["LineString", "MultiLineString"]
    major = ["motorway", "trunk", "primary", "secondary", "tertiary",
             "motorway_link", "trunk_link", "primary_link"]
    o = fetch_osm(zoom, {"highway": major, "waterway": ["river", "canal"],
                         "aeroway": ["aerodrome", "runway"]})
    water = pd.concat([census_layer(f"{tiger}/AREAWATER/tl_2024_{c}_"
                                    "areawater.zip")
                       for c in cfg["counties"]], ignore_index=True)
    place = census_layer(f"{tiger}/PLACE/tl_2024_01_place.zip")
    county = census_layer(f"{cb}/cb_2024_us_county_500k.zip")
    layers = {
        "places": clip_layer(place, zoom),
        "counties": clip_layer(county[county.STATEFP == "01"], zoom),
        "water_tiger": clip_layer(water, zoom),
        "roads_tiger": clip_layer(census_layer(
            f"{tiger}/PRISECROADS/tl_2024_01_prisecroads.zip"), zoom),
        "roads_osm": pick_osm(o, zoom, line, highway=True),
        "rivers_osm": pick_osm(o, zoom, line, waterway=True),
        "airports": pick_osm(o, zoom, aeroway="aerodrome"),
        "runways": pick_osm(o, zoom, aeroway="runway"),
    }
    layers.update({k: clip_layer(v, zoom) for k, v in usfs_layers().items()})
    detail_tags = {k: True for k in ("building", "highway", "waterway",
                                     "aeroway", "man_made", "natural",
                                     "landuse", "barrier")}
    for letter, b in closeup_boxes().items():
        bb = (b[0], b[2], b[1], b[3])
        try:                           # best effort: vector close-ups only
            d = fetch_osm(bb, detail_tags, tries=2)
        except RuntimeError:
            print(f"detail {letter}: Overpass unavailable, skipped")
            continue
        pre = f"detail_{letter}_"
        layers.update({
            pre + "buildings": pick_osm(d, bb, poly, building=True),
            pre + "roads": pick_osm(d, bb, line, highway=True),
            pre + "water": pick_osm(d, bb, poly, natural="water"),
            pre + "waterways": pick_osm(d, bb, line, waterway=True),
            pre + "aeroway": pick_osm(d, bb, aeroway=True),
            pre + "man_made": pick_osm(d, bb, man_made=True),
        })
    return layers


def inset_layers():
    """Southeast-US inset: CB 2024 500k states, an ocean polygon (box minus
    US land, so the Gulf coast comes from the state outlines) and cities."""
    import geopandas as gpd
    from shapely.geometry import box

    cfg = map_config()
    b = cfg["layer_inset"]
    st = clip_layer(census_layer(f"{cfg['cb']}/cb_2024_us_state_500k.zip"),
                    b)
    place = census_layer(f"{cfg['tiger']}/PLACE/tl_2024_01_place.zip")
    city = place[place.NAME.isin(cfg["inset_cities"])
                 & (place.LSAD == "25")].copy()
    city["geometry"] = city.representative_point()
    ocean = box(*b).difference(st.union_all())
    return {"states": st, "ocean": gpd.GeoDataFrame(geometry=[ocean],
                                                    crs=4326),
            "cities": city[["NAME", "GEOID", "geometry"]]}


def write_layers(layers, path):
    """Write a dict of GeoDataFrames as one GeoPackage, one layer each."""
    if os.path.exists(path):
        os.remove(path)
    for name, gdf in layers.items():
        print(f"{path}:{name} {len(gdf)}")
        if gdf.empty:
            continue
        gdf = gdf.copy()
        for col in gdf.columns.drop("geometry"):
            if gdf[col].map(type).isin([list, dict]).any():
                gdf[col] = gdf[col].astype(str)
        gdf.to_file(path, layer=name, driver="GPKG")


def read_layer(gpkg, name, box=None):
    """One GeoPackage layer, optionally features touching a (W, E, S, N)
    box (not clipped). Missing layers return an empty frame."""
    import geopandas as gpd
    import pyogrio

    if name not in [n for n, _ in pyogrio.list_layers(gpkg)]:
        return gpd.GeoDataFrame(geometry=[], crs=4326)
    bbox = None if box is None else (box[0], box[2], box[1], box[3])
    return gpd.read_file(gpkg, layer=name, bbox=bbox)


# ---------------------------------------------------------------- assets

def skill_dir():
    return os.path.dirname(os.path.abspath(
        skill_dir.__code__.co_filename))


def fetch_locations_page():
    """ARM BNF facilities from the `const locations` JSON on arm.gov."""
    import json
    import re

    import pandas as pd
    import requests

    url = "https://www.arm.gov/capabilities/observatories/bnf/locations"
    html = requests.get(url, timeout=60).text
    locs = json.loads(re.search(r"const\s+locations\s*=\s*(\[.*?\]);",
                                html, re.S).group(1))
    return pd.DataFrame([dict(
        facility=d["facility_code"], name=d["facility_name"],
        lat=float(d["latitude"]), lon=float(d["longitude"]),
        alt=float(d["altitude"]), start=d["start_date"][:10],
        classes=";".join(sorted({c["class"] for c in d["class"] or []})))
        for d in locs])


def facility_marker(fac):
    """Shape by facility role: star main, triangle scanning radar,
    square extended or supplemental facility."""
    return {"M1": "*", "S3": "^", "S4": "^"}.get(fac, "s")


def page_rows(p):
    """Hollow facility markers from the locations page (fallback only)."""
    rows = []
    for (lat, lon), g in p[p.lat != 0].groupby(["lat", "lon"], sort=False):
        fac = g.facility.iloc[0]
        rows.append(dict(key=fac, group="ARM", marker=facility_marker(fac),
                         precise=False, label=" / ".join(g.facility) +
                         " (page)", lat=lat, lon=lon, n=len(g),
                         classes=g.classes.fillna("").iloc[0],
                         layer="main", source="arm.gov locations page"))
    return rows


def build_asset_table(page_csv=None, positions_csv=None, region_csv=None,
                      out=None):
    """Regenerate site_map_assets.csv.

    ARM markers come from arm-bnf-site/bnf_instrument_positions.csv (file
    positions), or from the frozen locations page (hollow) if that file is
    absent. Non-ARM rows come from bnf-research-assets/bnf_region_assets.csv.
    layer: main (main map and close-ups), detail (close-ups only: within
    100 m of a larger ARM cluster, or inside a close-up box) or inset.
    """
    import pandas as pd

    cfg, here = map_config(), skill_dir()
    bnf = os.path.dirname(here)
    page_csv = page_csv or os.path.join(here, "bnf_locations_page.csv")
    positions_csv = positions_csv or os.path.join(
        bnf, "arm-bnf-site", "bnf_instrument_positions.csv")
    region_csv = region_csv or os.path.join(
        bnf, "bnf-research-assets", "bnf_region_assets.csv")
    if os.path.exists(positions_csv):
        rows = instrument_rows(pd.read_csv(positions_csv), cfg)
    else:
        rows = page_rows(pd.read_csv(page_csv))
    big = sorted(rows, key=lambda r: -r["n"])
    for r in rows:                     # collapse sub-100 m clusters
        if any(q["n"] > r["n"] and haversine_m(r["lat"], r["lon"], q["lat"],
                                               q["lon"]) < 100 for q in big):
            r["layer"] = "detail"
    by = {r["key"]: r for r in rows}
    m, t = (by[k] for k in cfg["anchor"])
    rows.append(dict(key="M1_S10", group="anchor", marker="", precise=False,
                     label="", lat=(m["lat"] + t["lat"]) / 2,
                     lon=(m["lon"] + t["lon"]) / 2, n=0, classes="",
                     layer="none", source="midpoint " + "-".join(
                         cfg["anchor"])))
    A = pd.DataFrame(rows)
    if os.path.exists(region_csv):
        R = pd.DataFrame(region_rows(pd.read_csv(region_csv), cfg))
        boxes = closeup_boxes(A).values()
        near = pd.concat([inside(R, b) for b in boxes], axis=1).any(axis=1)
        R.loc[near & (R.layer == "main"), "layer"] = "detail"
        A = pd.concat([A, R], ignore_index=True)
    w, e, s, n = cfg["main"]
    keep = (A.lon.between(w, e) & A.lat.between(s, n)) | (A.layer == "inset")
    A = A[keep].reset_index(drop=True)
    if out:
        A.to_csv(out, index=False)
    return A


def instrument_label(fac, classes, n, kind):
    """'M1: 42 instruments', 'S4 KASACR, LDIS, XSACR', 'U2 first nav fix'."""
    if kind != "fixed":
        what = {"sonde": "sonde launch", "tbswind": "TBS launch",
                "nav-air": "ArcticShark take-off"}.get(classes[0],
                                                       classes[0])
        return f"{fac} {what} (first fix)"
    if n > 3:
        return f"{fac}: {n} instruments"
    return f"{fac} {', '.join(c.upper() for c in classes)}"


def instrument_rows(df, cfg):
    """One ARM marker per file position in bnf_instrument_positions.csv
    (arm-bnf-site): star for the main cluster, triangle if a scanning radar
    is there, square for a facility cluster (over 3 instruments), diamond
    for a launch first fix, circle otherwise; hollow where the note says
    the value is rounded."""
    rows = []
    for _, r in df.dropna(subset=["lat", "lon"]).iterrows():
        cl = sorted(set(str(r.instruments).split(";")))
        fac = str(r.facilities).split(";")[0]
        launch = r.kind != "fixed" and cl[0] in ("sonde", "tbswind")
        mk = ("D" if launch else "*" if r.key in cfg["main_keys"] else
              "^" if set(cl) & set(cfg["radar_classes"]) else
              "s" if r.kind == "fixed" and r.n_instruments > 3 else "o")
        note = str(r.get("note", ""))
        rows.append(dict(
            key=r.key, group="ARM", marker=mk,
            precise=not re.search(r"0\.0\d|rounded|nominal", note),
            label=instrument_label(fac, cl, int(r.n_instruments), r.kind),
            lat=r.lat, lon=r.lon, n=int(r.n_instruments),
            classes=";".join(cl), layer="main",
            source="ARM file position (arm-bnf-site)"))
    return rows


def region_id(ids, network):
    """Short identifier: FAA code, NWSLI, USGS number, LMA letter, radar."""
    ids = str(ids)
    pats = ((r"IMPROVE (\w+)", "IMPROVE {}"), (r"FAA (\w+)", "{}"),
            (r"(USFS) district", "USFS office"),
            (r"NWSLI (\w+)", "{}"), (r"USGS (\d+)", "USGS {}"),
            (r"(\d+):AL:SCAN", "SCAN {}"), (r"NALMA (\w)", "LMA {}"),
            (r"WMO (\d+)", "sonde {}"), (r"NEON (\w+)", "NEON {}"),
            (r"WFO (\w+)", "NWS {}"), (r"AERONET (\w+)", "AERONET {}"),
            (r"CASTNET (\w+)", "CASTNET {}"), (r"PSL (\w+)", "PSL {}"),
            (r"AQS ([\d-]+)", "AQS {}"), (r"WBAN (\d+)", "WBAN {}"),
            (r"^([A-Z]{4,5})$", "{}"))
    for pat, fmt in pats:
        m = re.search(pat, ids)
        if m and m.group(1) != "-":
            return fmt.format(m.group(1))
    return ids.split(";")[0]


def region_rows(df, cfg):
    """Non-ARM assets from bnf-research-assets. Operator group comes from
    the first operator named (NOAA, NEON, else Other). Census, polygon,
    reservoir, research-centre and AmeriFlux rows (ARM duplicates) are
    skipped. Far rows of the inset types go to the inset."""
    rows = []
    w, e, s, n = cfg["main"]
    for _, r in df.dropna(subset=["lat", "lon"]).iterrows():
        kind, op = str(r.asset_type).lower(), str(r.operator)
        if (r.network in cfg["skip_networks"] or op.startswith("DOE ARM")
                or any(x in kind for x in cfg["skip_types"])):
            continue
        first = op.split("/")[0]
        grp = ("NOAA" if "NOAA" in first else
               "NEON" if "NEON" in first else "Other")
        mk = ("^" if "radar" in kind else "D" if "radiosonde" in kind else
              "s" if "office" in kind else "o")
        rid = region_id(r.ids, r.network)
        here = w <= r.lon <= e and s <= r.lat <= n
        layer = ("main" if here else "inset" if any(
            x in kind for x in cfg["inset_types"]) else "none")
        if layer == "none":
            continue
        prec = str(r.coord_precision)
        rows.append(dict(
            key=re.sub(r"\W+", "_", rid.lower()), group=grp, marker=mk,
            precise=not re.search(r"2 dp|3 dp|~1 km|Nominatim|geocode",
                                  prec),
            label=("ASOS " if "(asos)" in kind else
                   cfg["net_prefix"].get(r.network, "")) + rid,
            lat=r.lat, lon=r.lon, n=1, classes=kind,
            layer=layer, source=f"bnf-research-assets: {r['name']}"))
    return rows


def haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = (math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2)
         * math.sin(math.radians(lon2 - lon1) / 2) ** 2)
    return 2 * 6371008.8 * math.asin(math.sqrt(a))


def site_map_assets():
    """The shipped asset table (site_map_assets.csv) with a colour column."""
    import pandas as pd

    a = pd.read_csv(os.path.join(skill_dir(), "site_map_assets.csv"))
    a["color"] = a.group.map(map_config()["col"])
    return a


def inside(df, box):
    return df.lon.between(box[0], box[1]) & df.lat.between(box[2], box[3])


def box_around(lat, lon, half_w, half_h=None):
    """(W, E, S, N) box of half-sizes in metres around a point."""
    half_h = half_w if half_h is None else half_h
    dlat = half_h / 110900
    dlon = half_w / (111320 * math.cos(math.radians(lat)))
    return lon - dlon, lon + dlon, lat - dlat, lat + dlat


def leg_table(A=None):
    """Geodesic (WGS84) km and initial bearing for map_config()['legs']."""
    t = map_tools()
    A = site_map_assets() if A is None else A
    P = A.set_index("key")
    out = []
    for a, b, *_ in map_config()["legs"]:
        az, _, d = t.geod.inv(P.lon[a], P.lat[a], P.lon[b], P.lat[b])
        out.append((a, b, round(d / 1000, 2), round(az % 360)))
    return out


# --------------------------------------------------------------- imagery

def xyz_tile(lat, lon, z):
    """Web-Mercator XYZ tile index containing a point."""
    n = 2 ** z
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)
    return x, y


def imagery_mosaic(w, e, s, n, z, service="imagery", cache="/tmp/esri"):
    """Esri tile mosaic (World Imagery or World Hillshade) over a box.

    Returns (RGB uint8 array, extent in EPSG:3857 as x0, x1, y0, y1).
    """
    import io

    import numpy as np
    import requests
    from PIL import Image

    cfg = map_config()
    url = (f"{cfg['esri']}/{cfg['tile'][service]}/MapServer/tile/"
           "{z}/{y}/{x}")
    cache = os.path.join(cache, service)
    os.makedirs(cache, exist_ok=True)
    x0, y0 = xyz_tile(n, w, z)
    x1, y1 = xyz_tile(s, e, z)
    rows = []
    for ty in range(y0, y1 + 1):
        row = []
        for tx in range(x0, x1 + 1):
            f = os.path.join(cache, f"{z}_{tx}_{ty}")
            if not os.path.exists(f):
                r = requests.get(url.format(z=z, y=ty, x=tx), timeout=30)
                r.raise_for_status()
                with open(f, "wb") as out:
                    out.write(r.content)
            with open(f, "rb") as fh:
                row.append(np.asarray(Image.open(io.BytesIO(fh.read()))
                                      .convert("RGB")))
        rows.append(np.hstack(row))
    r0 = math.pi * 6378137.0
    span = 2 * r0 / 2 ** z
    ext = (x0 * span - r0, (x1 + 1) * span - r0,
           r0 - (y1 + 1) * span, r0 - y0 * span)
    return np.vstack(rows), ext


def imagery_metadata(lat, lon):
    """Source, date and resolution of Esri World Imagery at a point."""
    import requests

    url = f"{map_config()['esri']}/World_Imagery/MapServer/identify"
    p = dict(geometry=f"{lon},{lat}", geometryType="esriGeometryPoint",
             sr=4326, tolerance=1, imageDisplay="400,400,96", f="json",
             mapExtent=f"{lon - 0.05},{lat - 0.05},{lon + 0.05},{lat + 0.05}",
             returnGeometry="false")
    res = requests.get(url, params=p, timeout=30).json().get("results", [])
    return res[0]["attributes"] if res else {}


def imagery_credit(lat, lon):
    """Short credit, e.g. 'Esri; Vantor WV03 2025-10-12, 0.31 m'."""
    try:
        m = imagery_metadata(lat, lon)
        d = m.get("DATE (YYYYMMDD)", "")
        return (f"Esri; {m.get('SOURCE', '')} {m.get('DESCRIPTION', '')} "
                f"{d[:4]}-{d[4:6]}-{d[6:]}, {m.get('RESOLUTION (M)', '?')} m")
    except Exception:
        return "Esri World Imagery"


def local_tm(box):
    """Ellipsoidal Transverse Mercator centred on a (W, E, S, N) box."""
    import cartopy.crs as ccrs

    return ccrs.TransverseMercator(central_longitude=(box[0] + box[1]) / 2,
                                   central_latitude=(box[2] + box[3]) / 2)


def warp_mosaic(img, ext, proj, box, width_px=2400):
    """Resample an EPSG:3857 mosaic onto a regular grid in proj covering box
    (W, E, S, N): proj -> lon/lat -> EPSG:3857 (pyproj) -> bilinear sample.
    Returns (RGB array, extent in proj units)."""
    import numpy as np
    from scipy.ndimage import map_coordinates

    t = map_tools()
    c = proj.transform_points(t.pc, np.array([box[0], box[1], box[0], box[1]]),
                              np.array([box[2], box[2], box[3], box[3]]))
    x0, x1 = c[:, 0].min(), c[:, 0].max()
    y0, y1 = c[:, 1].min(), c[:, 1].max()
    h = int(width_px * (y1 - y0) / (x1 - x0))
    gx, gy = np.meshgrid(np.linspace(x0, x1, width_px),
                         np.linspace(y1, y0, h))
    ll = t.pc.transform_points(proj, gx.ravel(), gy.ravel())
    mx, my = t.to_m.transform(ll[:, 0], ll[:, 1])
    col = (mx - ext[0]) / (ext[1] - ext[0]) * img.shape[1] - 0.5
    row = (ext[3] - my) / (ext[3] - ext[2]) * img.shape[0] - 0.5
    out = np.stack([map_coordinates(img[..., b].astype(float), [row, col],
                                    order=1, mode="nearest")
                    .reshape(h, width_px) for b in range(3)], -1)
    return out.clip(0, 255).astype(np.uint8), (x0, x1, y0, y1)


def raster_background(ax, box, z, service="imagery", grey=False,
                      width_px=2400, alpha=1.0, zorder=0):
    """Esri tiles resampled exactly into the axes projection."""
    import numpy as np

    img, ext = imagery_mosaic(*box, z, service=service)
    pad = (box[1] - box[0]) * 0.03, (box[3] - box[2]) * 0.03
    big = (box[0] - pad[0], box[1] + pad[0], box[2] - pad[1], box[3] + pad[1])
    out, oext = warp_mosaic(img, ext, ax.projection, big, width_px)
    if grey:
        lum = out @ np.array([0.299, 0.587, 0.114])
        out = np.repeat((0.55 * lum + 0.45 * 200)[..., None], 3, -1)
        out = out.clip(0, 255).astype(np.uint8)
    ax.imshow(out, extent=oext, transform=ax.projection, origin="upper",
              interpolation="lanczos", alpha=alpha, zorder=zorder)


# --------------------------------------------------------------- drawing

def draw(ax, gdf, **kw):
    """Add GeoDataFrame geometries; never gdf.plot on a cartopy axes (it
    resets the aspect to 1/cos(lat))."""
    if len(gdf):
        ax.add_geometries(gdf.geometry, crs=map_tools().pc, **kw)


def scalebar(ax, metres, text, loc=(0.05, 0.05), color="k"):
    """True-distance (geodesic) scale bar with a half-way tick."""
    import numpy as np

    t, fs = map_tools(), map_config()["fs"]
    x0, x1, y0, y1 = ax.get_extent(t.pc)
    lon0, lat0 = x0 + loc[0] * (x1 - x0), y0 + loc[1] * (y1 - y0)
    pts = [t.geod.fwd(lon0, lat0, 90, d)[:2] for d in (0, metres / 2, metres)]
    p = ax.projection.transform_points(t.pc, *map(np.array, zip(*pts)))
    halo = t.halo if color == "k" else t.halo_dk
    for a, b, c in ((0, 1, color), (1, 2, "white" if color == "k" else "k")):
        ax.plot(p[[a, b], 0], p[[a, b], 1], color=c, lw=5,
                solid_capstyle="butt", transform=ax.projection, zorder=20,
                path_effects=halo if a == 0 else None)
    ax.text(p[1, 0], p[0, 1], text + "\n", ha="center", va="center",
            color=color, transform=ax.projection, zorder=20,
            fontsize=fs["small"], path_effects=halo)


def north_arrow(ax, loc=(0.95, 0.08), color="k"):
    """Arrow along the local meridian (true north) at an axes position."""
    import numpy as np

    t, fs = map_tools(), map_config()["fs"]
    x0, x1, y0, y1 = ax.get_extent(t.pc)
    lon, lat = x0 + loc[0] * (x1 - x0), y0 + loc[1] * (y1 - y0)
    p = ax.projection.transform_points(t.pc, np.array([lon, lon]),
                                       np.array([lat, lat + 0.01]))
    ang = math.atan2(p[1, 1] - p[0, 1], p[1, 0] - p[0, 0])
    dx, dy = 0.05 * math.cos(ang), 0.05 * math.sin(ang)
    halo = t.halo if color == "k" else t.halo_dk
    ax.annotate("N", xy=(loc[0] + dx, loc[1] + dy), xytext=loc,
                xycoords="axes fraction", textcoords="axes fraction",
                ha="center", va="top", fontsize=fs["title"],
                fontweight="bold", color=color, path_effects=halo, zorder=21,
                arrowprops=dict(arrowstyle="-|>,head_width=0.5,head_length=1",
                                lw=2.5, color=color))


def plot_assets(ax, df, scale=1.0, edge="k"):
    """Colour = operator group, shape = asset type, hollow = nominal."""
    pc, size = map_tools().pc, map_config()["size"]
    df = df[df.marker.fillna("").astype(bool)]
    for (mk, prec), g in df.groupby(["marker", "precise"]):
        if not prec:     # white underlay so hollow markers read on imagery
            ax.scatter(g.lon, g.lat, transform=pc, marker=mk, zorder=11,
                       s=size[mk] * scale, facecolors="none",
                       edgecolors="white", linewidths=4.5)
        ax.scatter(g.lon, g.lat, transform=pc, marker=mk, zorder=12,
                   s=size[mk] * scale, linewidths=1.2 if prec else 2.4,
                   c=g.color if prec else "none",
                   edgecolors=edge if prec else g.color.tolist())


def label(ax, lon, lat, text, dx, dy, dark=False, ha=None, frac=False,
          **kw):
    """Label with a leader anchored at the text edge nearest the point.
    (dx, dy) are offset points, or an axes-fraction position if frac."""
    t = map_tools()
    ha = ha or ("left" if dx >= 0 else "right")
    to_ax = t.pc._as_mpl_transform(ax) + ax.transAxes.inverted()
    east = dx > to_ax.transform((lon, lat))[0] if frac else dx >= 0
    kw.setdefault("fontsize", map_config()["fs"]["label"])
    return ax.annotate(
        text, (lon, lat), xycoords=t.pc._as_mpl_transform(ax),
        xytext=(dx, dy), ha=ha, va="center", zorder=15,
        textcoords="axes fraction" if frac else "offset points",
        color="white" if dark else "k",
        path_effects=t.halo_dk if dark else t.halo,
        arrowprops=dict(arrowstyle="-", lw=0.8, shrinkA=0, shrinkB=5,
                        color="white" if dark else "k",
                        relpos=(0, 0.5) if east else (1, 0.5)), **kw)


def column_labels(ax, A, box, dark, skip=(), fixed=None):
    """Label every asset in a close-up from two columns of evenly spaced
    text (left half of the points to the left column), so leaders do not
    cross."""
    import numpy as np

    sub = A[inside(A, box) & A.label.fillna("").astype(bool)]
    for b in skip:                     # labelled in a nested close-up
        sub = sub[~inside(sub, b)]
    fixed = fixed or {}
    for _, r in sub[sub.key.isin(list(fixed))].iterrows():
        text, x, y, ha = fixed[r.key]
        label(ax, r.lon, r.lat, text or r.label, x, y, dark=dark, ha=ha,
              frac=True)
    sub = sub[~sub.key.isin(list(fixed))]
    mid = (box[0] + box[1]) / 2
    for side, g in ((0, sub[sub.lon < mid]), (1, sub[sub.lon >= mid])):
        g = g.sort_values("lat", ascending=False)
        top, bot = (0.80, 0.22) if side else (0.88, 0.30)
        ys = np.linspace(top, bot, len(g)) if len(g) > 1 else [top]
        for (_, r), y in zip(g.iterrows(), ys):
            label(ax, r.lon, r.lat, r.label, 0.97 if side else 0.03, y,
                  dark=dark, ha="right" if side else "left", frac=True)


def outline(ax, b, text, color="k", dark=False):
    from matplotlib.patches import Rectangle

    t, fs = map_tools(), map_config()["fs"]
    ax.add_patch(Rectangle((b[0], b[2]), b[1] - b[0], b[3] - b[2],
                           transform=t.pc, fc="none", ec=color, lw=1.6,
                           zorder=13))
    if text:
        ax.text(b[1], b[3], text, transform=t.pc, va="bottom",
                fontweight="bold", fontsize=fs["title"], color=color,
                path_effects=t.halo_dk if dark else t.halo, zorder=15)


def route_shield(name):
    """'US Hwy 278' -> 'US 278', 'State Hwy 33' -> 'AL 33', 'I- 65' ->
    'I-65'; None for other names."""
    import re

    m = re.match(r"\s*(US Hwy|I-|State (?:Hwy|Rte|Route))\s*(\d+)\s*$",
                 str(name))
    if not m:
        return None
    pre = {"US Hwy": "US ", "I-": "I-"}.get(m.group(1), "AL ")
    return pre + m.group(2)


def route_labels(ax, roads, box, taken, avoid=None):
    """One shield per US/state/interstate route on its longest clipped part.
    Positions along the road are tried in turn until the shield's text box
    clears every box in taken (place labels, earlier shields), the axes
    edge and avoid (the inset footprint, display units)."""
    t, fs = map_tools(), map_config()["fs"]
    g = roads.assign(shield=roads.FULLNAME.map(route_shield)).dropna(
        subset=["shield"])
    g = g.assign(geometry=g.geometry.clip_by_rect(box[0], box[2], box[1],
                                                  box[3]))
    g = g[~g.is_empty]
    for shield, part in g.groupby("shield"):
        geom = part.geometry.union_all()
        ln = max(getattr(geom, "geoms", [geom]), key=lambda x: x.length)
        for f in (0.5, 0.35, 0.65, 0.2, 0.8, 0.1, 0.9):
            pt = ln.interpolate(f, normalized=True)
            txt = ax.text(pt.x, pt.y, shield, transform=t.pc, ha="center",
                          va="center", fontsize=fs["road"], zorder=14,
                          fontweight="bold",
                          bbox=dict(boxstyle="round,pad=0.2", fc="white",
                                    ec="#333", lw=0.8))
            if keep_label(ax, txt, taken, avoid, pad=4):
                break


def keep_label(ax, art, taken=(), avoid=None, pad=0):
    """Keep art if its box lies inside the axes and clear of avoid and of
    every box in taken (then append it); otherwise remove it."""
    r = ax.figure.canvas.get_renderer()
    bb = art.get_window_extent(r).expanded(1, 1).padded(pad)
    ok = (ax.bbox.contains(bb.x0, bb.y0) and ax.bbox.contains(bb.x1, bb.y1)
          and not (avoid is not None and bb.overlaps(avoid))
          and not any(bb.overlaps(o) for o in taken))
    if ok:
        if isinstance(taken, list):
            taken.append(bb)
    else:
        art.remove()
    return ok


def line_label(ax, gdf, box, text, frac=0.5, color="#1f5f8b", rot=0,
               **kw):
    """Label a line feature on its part inside box (clip first)."""
    t, fs = map_tools(), map_config()["fs"]
    g = gdf.geometry.clip_by_rect(box[0], box[2], box[1], box[3])
    g = g[~g.is_empty]
    if len(g):
        geom = g.union_all()
        ln = max(getattr(geom, "geoms", [geom]), key=lambda x: x.length)
        pt = ln.interpolate(frac, normalized=True)
        return ax.text(pt.x, pt.y, text, transform=t.pc, color=color,
                       fontsize=fs["small"], rotation=rot, ha="center",
                       va="center", path_effects=t.halo, zorder=14, **kw)


def distance_legs(ax, A, legs, color="#1a1a1a"):
    """Geodesic dimension lines between assets, labelled km and bearing.
    legs: (key_a, key_b, text, side, frac); side flips the label across
    the line, frac places it along the leg."""
    import numpy as np

    t, fs = map_tools(), map_config()["fs"]
    halo = t.halo_dk if color.lower() in ("#ffffff", "w", "white") else t.halo
    P = A.set_index("key")
    for a, b, name, side, frac in legs:
        p, q = P.loc[a], P.loc[b]
        az, _, d = t.geod.inv(p.lon, p.lat, q.lon, q.lat)
        pts = t.geod.npts(p.lon, p.lat, q.lon, q.lat, 50)
        lo, la = map(np.array, zip(*([(p.lon, p.lat)] + pts +
                                     [(q.lon, q.lat)])))
        xy = ax.projection.transform_points(t.pc, lo, la)[:, :2]
        ax.plot(xy[:, 0], xy[:, 1], color=color, lw=1.8, zorder=7,
                ls=(0, (6, 3)), transform=ax.projection, path_effects=halo)
        v = (xy[-1] - xy[0]) / np.hypot(*(xy[-1] - xy[0]))
        n = np.array([-v[1], v[0]])
        for e in (xy[0], xy[-1]):                       # 600 m end ticks
            ax.plot([e[0] - 600 * n[0], e[0] + 600 * n[0]],
                    [e[1] - 600 * n[1], e[1] + 600 * n[1]], color=color,
                    lw=1.8, zorder=7, transform=ax.projection)
        ang = np.degrees(np.arctan2(v[1], v[0]))
        ang = ang - 180 if ang > 90 else ang + 180 if ang < -90 else ang
        ax.annotate(f"{name}\n{d / 1000:.2f} km, {az % 360:.0f}°",
                    xy[int(frac * (len(xy) - 1))],
                    xycoords=ax.projection._as_mpl_transform(ax),
                    xytext=n * side * 22, textcoords="offset points",
                    rotation=ang, rotation_mode="anchor", ha="center",
                    va="center", fontsize=fs["label"], fontweight="bold",
                    color=color, path_effects=halo, zorder=16)


def legend_handles(pal):
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    col = map_config()["col"]
    ec = "w" if pal["dark"] else "k"
    h = [Line2D([], [], ls="", marker="s", ms=11, mfc=c, mec=ec, label=g)
         for g, c in [("ARM", col["ARM"]), ("NOAA", col["NOAA"]),
                      ("NSF NEON", col["NEON"]), ("Other", col["Other"])]]
    h += [Line2D([], [], ls="", marker=m, ms=s, mfc="#bdbdbd", mec=ec,
                 label=text) for m, s, text in
          [("*", 17, "Main facility"),
           ("s", 10, "Extended / supplemental facility"),
           ("^", 11, "Scanning radar"), ("o", 9, "Station / instrument"),
           ("D", 9, "Sounding launch")]]
    h += [Line2D([], [], ls="", marker="o", ms=10, mfc="none", mec=ec,
                 mew=2, label="Hollow = rounded / nominal position"),
          Patch(fc=pal["forest"], ec=pal["forest_edge"],
                label="Bankhead NF (ranger district)"),
          Patch(fc=pal["wild"], ec=pal["forest_edge"], hatch="//",
                label="Sipsey Wilderness"),
          Patch(fc=pal["water"], ec="none", label="Water (TIGER)"),
          Patch(fc=pal["town"], ec=pal["town_edge"],
                label="Incorporated place (TIGER)"),
          Line2D([], [], color=pal["road"], lw=2.0, label="Road (OSM)"),
          Line2D([], [], color=pal["county"], lw=1.2, ls=(0, (5, 2)),
                 label="County line"),
          Line2D([], [], color=pal["line"], lw=1.8, ls=(0, (6, 3)),
                 label="Geodesic distance")]
    return h


# ---------------------------------------------------------------- panels

def map_themes():
    """Map variants: main background and close-up background."""
    return {
        "reference": dict(main="vector", palette="light", detail="imagery"),
        "imagery": dict(main="imagery", palette="light", detail="imagery"),
        "vector": dict(main="vector", palette="light", detail="vector"),
    }


def palette(name="light"):
    return dict(land="#f4f1ea", water="#9cc7e4", river="#3d85c6",
                town="#e3d9c6", town_edge="#9b8f78", forest="#cfe3c4",
                wild="#a9cc98", forest_edge="#4d7a3a", county="#6b6b6b",
                road="#4a4a4a", road_minor="#8a8a8a", runway="#555555",
                text="#222222", line="#1a1a1a", dark=name == "dark")


def base_layers(ax, gpkg, box, pal, hill=0):
    """Vector basemap; hill > 0 adds Esri World Hillshade at that zoom."""
    t = map_tools()
    ax.set_facecolor(pal["land"])
    if hill:
        raster_background(ax, box, hill, "hillshade", width_px=2600,
                          alpha=0.40, zorder=1)
    kw = dict(zorder=2)
    draw(ax, read_layer(gpkg, "forest_district", box), fc=pal["forest"],
         ec=pal["forest_edge"], lw=1.2, alpha=0.75, **kw)
    draw(ax, read_layer(gpkg, "wilderness", box), fc=pal["wild"],
         ec=pal["forest_edge"], lw=1.0, hatch="//", alpha=0.8, **kw)
    pl = read_layer(gpkg, "places", box)
    draw(ax, pl[pl.CLASSFP.str.startswith("C")], fc=pal["town"],
         ec=pal["town_edge"], lw=0.6, zorder=3)
    draw(ax, read_layer(gpkg, "water_tiger", box), fc=pal["water"],
         ec="none", zorder=4)
    riv = read_layer(gpkg, "rivers_osm", box)
    draw(ax, riv, fc="none", ec=pal["river"], lw=0.9, zorder=4)
    draw(ax, read_layer(gpkg, "wild_scenic_river", box), fc="none",
         ec=pal["river"], lw=2.0, zorder=4)
    draw(ax, read_layer(gpkg, "counties", box), fc="none", ec=pal["county"],
         lw=1.2, linestyle=(0, (5, 2)), zorder=5)
    rd = read_layer(gpkg, "roads_osm", box)
    for kinds, lw, c in ((("tertiary",), 0.6, pal["road_minor"]),
                         (("secondary",), 1.1, pal["road"]),
                         (("primary", "primary_link"), 1.7, pal["road"]),
                         (("motorway", "trunk", "motorway_link",
                           "trunk_link"), 2.4, pal["road"])):
        draw(ax, rd[rd.highway.isin(kinds)], fc="none", ec=c, lw=lw,
             zorder=6)
    draw(ax, read_layer(gpkg, "runways", box), fc=pal["runway"],
         ec=pal["runway"], lw=1.5, zorder=6)
    return t


def main_map(fig, rect, A, gpkg, theme, boxes, avoid=None):
    import numpy as np

    t, cfg = map_tools(), map_config()
    fs, box, pal = cfg["fs"], cfg["main"], palette(theme["palette"])
    ax = fig.add_axes(rect, projection=local_tm(box))
    ax.set_extent(box, t.pc)
    if theme["main"] == "vector":
        base_layers(ax, gpkg, box, pal, hill=11)
    else:
        raster_background(ax, box, 12, width_px=2800)
        draw(ax, read_layer(gpkg, "forest_district", box), fc="none",
             ec="#b8f08f", lw=1.6, zorder=2)
    ax.set_extent(box, t.pc)
    dark = theme["main"] != "vector"
    halo = t.halo_dk if dark else t.halo
    tc = "w" if dark else pal["text"]
    ax.apply_aspect()
    from matplotlib.transforms import Bbox

    if avoid is not None:              # inset footprint, figure fraction
        avoid = Bbox.from_bounds(*avoid).transformed(fig.transFigure)
    styles = {"water": ("#1f5f8b", "italic", "normal"),
              "forest": ("#2f5a22", "normal", "bold"),
              "wild": ("#2f5a22", "italic", "normal")}
    for lo, la, text, kind in cfg["area_labels"]:
        c, st, wt = styles[kind]
        ax.text(lo, la, text, transform=t.pc, ha="center", va="center",
                color="w" if dark else c, style=st, fontweight=wt,
                fontsize=fs["label"], path_effects=halo, zorder=9)
    shown = A[A.layer == "main"]
    plot_assets(ax, shown, scale=0.9, edge="w" if dark else "k")
    reg = shown[~shown.group.isin(["ARM", "anchor"])]
    for _, r in reg.iterrows():
        text, dx, dy = cfg["lab_region"].get(r.key, (r.label, 7, 7))
        if text:
            keep_label(ax, label(ax, r.lon, r.lat, text, dx, dy, dark=dark,
                                 fontsize=fs["small"]), (), avoid)
    distance_legs(ax, A, cfg["legs"], color="#ffffff" if dark else "#1a1a1a")
    for k, (text, dx, dy) in cfg["lab_main"].items():
        r = A[A.key == k].iloc[0]
        label(ax, r.lon, r.lat, text, dx, dy, dark=dark, fontweight="bold")
    for letter, b in boxes.items():
        outline(ax, b, None, color="w" if dark else "k")
    # town names, then shields and rivers, each clear of markers and text
    rend = fig.canvas.get_renderer()
    taken = [tx.get_window_extent(rend) for tx in ax.texts]
    xy = (t.pc._as_mpl_transform(ax)).transform(shown[["lon", "lat"]].values)
    rad = 9 * fig.dpi / 72
    taken += [Bbox.from_extents(x - rad, y - rad, x + rad, y + rad)
              for x, y in xy]
    pl = read_layer(gpkg, "places", box)
    pl = pl[pl.CLASSFP.str.startswith("C")]
    for _, r in pl.iterrows():
        p = r.geometry.representative_point()
        if not (box[0] < p.x < box[1] and box[2] < p.y < box[3]):
            continue
        big = r.ALAND > 2.5e7
        for off in ((0, 0), (0, 14), (0, -14), (34, 0), (-34, 0), (0, 28),
                    (0, -28), (-40, 14), (-40, -14)):
            txt = ax.annotate(r.NAME, (p.x, p.y),
                              xycoords=t.pc._as_mpl_transform(ax),
                              xytext=off, textcoords="offset points",
                              ha="center", va="center",
                              fontsize=fs["label"] if big else fs["small"],
                              fontweight="bold" if big else "normal",
                              color=tc, path_effects=halo, zorder=9)
            if keep_label(ax, txt, taken, avoid):
                break
    riv = read_layer(gpkg, "rivers_osm", box)
    if "name" in riv:
        for name in ("Sipsey Fork", "Flint Creek", "Brushy Creek"):
            sel = riv[riv.name.fillna("").str.startswith(name)]
            txt = line_label(ax, sel, box, name, frac=0.4, style="italic")
            if txt is not None:
                keep_label(ax, txt, taken, avoid)
    route_labels(ax, read_layer(gpkg, "roads_tiger", box), box, taken, avoid)
    gl = ax.gridlines(t.pc, draw_labels=True, lw=0.4, color="#888",
                      alpha=0.6, xlocs=np.arange(-87.8, -86.7, 0.2),
                      ylocs=np.arange(34.0, 34.9, 0.1))
    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = gl.ylabel_style = dict(size=fs["small"], rotation=0)
    scalebar(ax, 10000, "10 km", loc=(0.70, 0.04), color="w" if dark else "k")
    north_arrow(ax, (0.955, 0.06), color="w" if dark else "k")
    return ax


def wide_inset(fig, rect, gpkg, A, main_box, pal):
    t, cfg = map_tools(), map_config()
    fs = cfg["fs"]
    axi = fig.add_axes(rect, projection=t.ccrs.LambertConformal(
        central_longitude=-87.0, central_latitude=32.8,
        standard_parallels=(30, 35)))
    axi.set_extent(cfg["inset"], t.pc)
    axi.set_facecolor(pal["water"])
    st = read_layer(gpkg, "states")
    draw(axi, st, fc=pal["land"], ec="#777", lw=0.7)
    draw(axi, st[st.STUSPS == "AL"], fc="#e6dcc8", ec="#333", lw=1.1)
    draw(axi, read_layer(gpkg, "forest_district"), fc=pal["wild"],
         ec="none")
    outline(axi, main_box, None)
    for _, r in read_layer(gpkg, "cities").iterrows():
        axi.scatter(r.geometry.x, r.geometry.y, transform=t.pc, s=22,
                    c="#333", zorder=12)
        axi.text(r.geometry.x - 0.15, r.geometry.y, r.NAME, transform=t.pc,
                 fontsize=fs["small"] - 1, va="center", ha="right",
                 path_effects=t.halo, zorder=12)
    far = A[A.layer == "inset"]
    plot_assets(axi, far, scale=0.45)
    for k, (text, dx, dy) in cfg["lab_inset"].items():
        r = far[far.key == k]
        if len(r):
            axi.annotate(text, (r.lon.iloc[0], r.lat.iloc[0]),
                         xycoords=t.pc._as_mpl_transform(axi),
                         xytext=(dx, dy), textcoords="offset points",
                         ha="left" if dx >= 0 else "right", va="center",
                         fontsize=fs["small"] - 1, path_effects=t.halo,
                         zorder=14)
    m1 = A[A.key == cfg["anchor"][0]].iloc[0]
    axi.scatter(m1.lon, m1.lat, transform=t.pc, marker="*", s=300,
                c=cfg["col"]["ARM"], edgecolors="k", lw=0.8, zorder=13)
    for lo, la, text in [(-89.9, 33.7, "MS"), (-86.6, 32.3, "AL"),
                         (-83.4, 33.6, "GA"), (-87.6, 35.25, "TN"),
                         (-83.4, 30.2, "FL")]:
        axi.text(lo, la, text, transform=t.pc, ha="center", color="#555",
                 fontsize=fs["label"], fontweight="bold", zorder=11)
    axi.text(-88.6, 29.75, "Gulf of Mexico", transform=t.pc, ha="center",
             style="italic", color="#1f5f8b", fontsize=fs["label"],
             path_effects=t.halo, zorder=11)
    for sp in axi.spines.values():
        sp.set_linewidth(1.4)
    return axi


def detail_panel(fig, rect, A, box, z, letter, title, bg, gpkg, pal,
                 nested=None):
    """Close-up in a local TM: imagery or OSM vector background, assets and
    column labels, scale bar."""
    t, fs = map_tools(), map_config()["fs"]
    axd = fig.add_axes(rect, projection=local_tm(box))
    axd.set_extent(box, t.pc)
    dark = bg != "vector"
    if dark:
        raster_background(axd, box, z, width_px=1600)
    else:
        axd.set_facecolor(pal["land"])
        pre = f"detail_{letter}_"
        draw(axd, read_layer(gpkg, pre + "water", box), fc=pal["water"],
             ec="none")
        draw(axd, read_layer(gpkg, pre + "aeroway", box), fc="#d8d8d8",
             ec="#888", lw=0.6)
        draw(axd, read_layer(gpkg, pre + "buildings", box), fc="#9a9a9a",
             ec="none")
        draw(axd, read_layer(gpkg, pre + "roads", box), fc="none",
             ec=pal["road"], lw=1.2)
        draw(axd, read_layer(gpkg, pre + "waterways", box), fc="none",
             ec=pal["river"], lw=1.0)
    axd.set_extent(box, t.pc)
    near = A[inside(A, box) & A.layer.isin(["main", "detail"])]
    plot_assets(axd, near, edge="w" if dark else "k")
    nested = nested or {}
    column_labels(axd, near, box, dark, skip=nested.values(),
                  fixed=map_config()["lab_detail"].get(letter))
    for k, b in nested.items():
        outline(axd, b, f" {k}", color="w" if dark else "k", dark=dark)
    axd.text(0.0, 1.03, letter, transform=axd.transAxes, va="bottom",
             fontsize=fs["letter"], fontweight="bold")
    axd.text(0.08, 1.03, title, transform=axd.transAxes, va="bottom",
             fontsize=fs["title"])
    w = t.geod.inv(box[0], box[2], box[1], box[2])[2]
    bar = [b for b in (10, 20, 50, 100, 200, 500, 1000) if b <= w / 3][-1]
    scalebar(axd, bar, f"{bar:g} m" if bar < 1000 else f"{bar / 1000:g} km",
             loc=(0.06, 0.07), color="w" if dark else "k")
    if dark:
        c = imagery_credit((box[2] + box[3]) / 2, (box[0] + box[1]) / 2)
        axd.text(0.99, 0.015, c, transform=axd.transAxes, ha="right",
                 va="bottom", fontsize=fs["small"] - 2, color="w",
                 path_effects=t.halo_dk, zorder=20)
    return axd


def panel_rects():
    """Figure-fraction rects: main, inset, and eight close-ups (2 x 4)."""
    rows = (0.745, 0.505, 0.265, 0.025)
    cols = (0.605, 0.805)
    close = [[x, y, 0.185, 0.19] for y in rows for x in cols]
    return [0.025, 0.19, 0.555, 0.76], [0.030, 0.695, 0.18, 0.25], close


def build_map_variant(layers_gpkg, inset_gpkg, theme="reference",
                      path="bnf_site_map_reference.png", dpi=300):
    """Render one of map_themes(): main map (a) with SE-US inset and
    close-ups b-i. Saves without a tight bbox (it crops add_axes figures)."""
    import matplotlib.pyplot as plt

    th = map_themes()[theme] if isinstance(theme, str) else theme
    cfg = map_config()
    fs, pal = cfg["fs"], palette(th["palette"])
    A = site_map_assets()
    boxes = closeup_boxes(A)
    plt.rcParams["savefig.bbox"] = None
    fig = plt.figure(figsize=(20, 13), facecolor="white")
    rect, irect, close = panel_rects()
    ax = main_map(fig, rect, A, layers_gpkg, th, boxes, avoid=irect)
    wide_inset(fig, irect, inset_gpkg, A, cfg["main"], pal)
    for (letter, (key, hw, hh, z, title)), r in zip(cfg["closeups"].items(),
                                                     close):
        b = boxes[letter]
        nest = {k: o for k, o in boxes.items() if k != letter and
                b[0] < o[0] and o[1] < b[1] and b[2] < o[2] and o[3] < b[3]}
        detail_panel(fig, r, A, b, z, letter, title, th["detail"],
                     layers_gpkg, pal, nest)
    fig.legend(handles=legend_handles(pal), loc="upper left", ncol=4,
               bbox_to_anchor=(0.025, 0.175), frameon=False,
               fontsize=fs["small"], labelspacing=0.7, handlelength=1.8,
               columnspacing=1.4, title_fontsize=fs["small"],
               alignment="left",
               title="Colour = operator · shape = asset type")
    src = ("ARM instruments only (no VAPs): positions from the most recent "
           "instrument file (arm-bnf-site); non-ARM assets from "
           "bnf-research-assets.\nBasemap: © OpenStreetMap contributors "
           "(ODbL); US Census TIGER/Line and CB 2024; USFS EDW (ranger "
           "district,\nwilderness, wild and scenic river); Esri World "
           "Hillshade")
    src += (" and World Imagery (Esri, Vantor; source and date per panel)."
            if "imagery" in th.values() else ".")
    fig.text(0.025, 0.008, src, fontsize=fs["small"] - 1, color="#444",
             linespacing=1.4)
    fig.text(0.025, 0.958, "a", fontsize=fs["letter"], fontweight="bold")
    fig.text(0.05, 0.958, "ARM Bankhead National Forest (BNF, AMF3) "
             "observatory, northern Alabama", fontsize=fs["title"] + 2)
    fig.savefig(path, dpi=dpi, facecolor="white")
    return fig, ax


def build_site_map(layers_gpkg, inset_gpkg, path="bnf_site_map_reference.png",
                   dpi=300):
    """The reference variant (vector + hillshade main map, imagery
    close-ups)."""
    return build_map_variant(layers_gpkg, inset_gpkg, "reference", path, dpi)
