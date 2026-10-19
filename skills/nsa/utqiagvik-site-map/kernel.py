"""Map layers, imagery and the four-panel asset map for ARM NSA / Utqiagvik.

Exec-loaded sidecar: top level holds only stdlib imports, functions and
literals. cartopy, geopandas, osmnx, matplotlib and pyproj are imported inside
the functions that need them, so loading the skill never fails in an
environment without the geo stack.
"""
import math
import os
import time


def map_config():
    """Boxes (W, E, S, N), styles and label layout used by build_site_map."""
    return dict(
        main=(-156.90, -156.38, 71.245, 71.405),
        c1_box=(-156.6265, -156.6000, 71.3185, 71.3265),
        e12_box=(-156.6520, -156.5930, 71.2715, 71.2860),
        e12_half_m=200,
        inset=(-167.5, -141.5, 66.3, 71.9),
        # BAID layer extent; the BEO polygon itself is not public (2026-10)
        beo_box=(-156.6664, -156.4078, 71.2565, 71.3291),
        # (lon, lat, text, dx, dy, marker) - ARM locations pages / catalog
        inset_sites=((-156.615, 71.323, "Utqiaġvik (NSA C1)", 8, 6, "*"),
                     (-157.407, 70.4718, "Atqasuk C2\n(1999–2011)", -8, -14,
                      "s"),
                     (-149.886, 70.495, "Oliktok Point\nAMF3 (2013–21)", 6,
                      -16, "s")),
        layer_zoom=(-157.0, 71.20, -156.25, 71.42),      # W, S, E, N
        layer_inset=(-168.0, 66.0, -140.0, 72.0),
        tile_url=("https://server.arcgisonline.com/ArcGIS/rest/services/"
                  "World_Imagery/MapServer/tile/{z}/{y}/{x}"),
        tiger="https://www2.census.gov/geo/tiger/TIGER2024",
        cb="https://www2.census.gov/geo/tiger/GENZ2024/shp",
        fs=dict(label=9, small=8, title=11, letter=14),
        col={"ARM": "#0072B2", "NOAA": "#E69F00", "NEON": "#009E73",
             "Research": "#CC79A7", "Historic": "#6E6E6E"},
        mark={"main": "*", "ext": "s", "radar": "^", "stn": "o",
              "sonde": "D"},
        size={"*": 210, "s": 70, "^": 95, "o": 46, "D": 50},
        lab_main={
            "xsapr": ("X-SAPR on BARC roof", -10, 30),
            "narl": ("NARL (1947–81)", -14, -20),
            "dew": ("DEW Line LRR", 16, 40),
            "cimel": ("Cimel / AERONET", -16, -12),
            "e11": ("ARM E11 Point Barrow\n(ECOR, SEBS)", -14, -20),
            "asos": ("ASOS PABR", 14, -10),
            "ua": ("NWS upper air 70026", -16, -12),
            "iceradar": ("UAF sea-ice radar", -16, 12),
            "coops": ("CO-OPS Barrow Offshore\n(2008–10)", 12, 12),
            "mbs": ("Sea-ice mass balance\nsite (approx.)", 12, 10),
            "b1": ("SIZONet\nmooring B1", 10, -16),
            "calm": ("CALM U1", 12, -8),
            "mp1": ("NEON megapit\n(2016)", -14, -10)},
        # close-up labels: (text, x, y, ha) in axes fraction, in columns
        lab_c1={
            "ecor": ("ECOR (E10)", 0.30, 0.87, "right"),
            "c1_page": ("C1 (locations page)", 0.30, 0.79, "right"),
            "dl": ("Doppler lidar", 0.30, 0.71, "right"),
            "mag": ("USGS magnetic obs.", 0.03, 0.43, "left"),
            "aos": ("AOS (E30/X3)", 0.50, 0.29, "right"),
            "sonde": ("Sonde launch (files: 0.01°)", 0.33, 0.12, "left"),
            "brw": ("NOAA GML BRW", 0.52, 0.95, "right"),
            "sebs": ("SEBS, LPM (E10)", 0.80, 0.89, "left"),
            "aeri": ("AERI", 0.80, 0.77, "left"),
            "bsrn": ("BSRN BAR\n(to 2016)", 0.80, 0.66, "left"),
            "c1_file": ("C1 nominal\n(26 files)", 0.80, 0.51, "left"),
            "sg27": ("GNSS SG27", 0.80, 0.40, "left"),
            "crn": ("USCRN 27516", 0.80, 0.30, "left")},
        lab_e12={
            "mp1": ("NEON megapit (2016)", 0.05, 0.85, "left"),
            "tower": ("NEON BARR tower + hut", 0.47, 0.95, "right"),
            "sp3": ("NEON soil plots SP1–5", 0.52, 0.95, "left"),
            "ngeeD": ("NGEE D", 0.97, 0.86, "right"),
            "ngeeA": ("NGEE A", 0.60, 0.55, "right"),
            "ngeeB": ("NGEE B", 0.75, 0.40, "right"),
            "ngeeC": ("NGEE C", 0.97, 0.40, "right"),
            "e12": ("ARM E12 snow array", 0.30, 0.13, "left")},
        lab_e12_zoom={"e12": ("ARM E12: all 9 instrument classes\n"
                              "share this file coordinate", 0.52, 0.30,
                              "left")},
        # triangle legs: name, +1 label outside the triangle, -1 inside
        triangle=(("c1_page", "e12", "C1 → E12", 1),
                  ("c1_page", "xsapr", "C1 → X-SAPR", -1),
                  ("e12", "xsapr", "E12 → X-SAPR", -1)),
    )


def map_tools():
    """Heavy imports and CRS objects, resolved at call time."""
    from types import SimpleNamespace

    import cartopy.crs as ccrs
    import matplotlib.patheffects as pe
    import pyproj

    return SimpleNamespace(
        ccrs=ccrs, pc=ccrs.PlateCarree(),
        geod=pyproj.Geod(ellps="WGS84"),
        to_ll=pyproj.Transformer.from_crs(3857, 4326, always_xy=True),
        halo=[pe.withStroke(linewidth=2.6, foreground="white")],
        halo_dk=[pe.withStroke(linewidth=2.4, foreground="black")])


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


def fetch_osm(bbox, tries=8):
    """One Overpass pull for all themes via osmnx, with exponential backoff.

    bbox is (W, S, E, N). Overpass answers HTTP 406 to the default
    python-requests user agent; osmnx's own agent is accepted.
    """
    import osmnx as ox

    keep = ["osmid", "element", "name", "natural", "water", "waterway",
            "building", "highway", "surface", "aeroway", "ref", "boundary",
            "protect_class", "leisure", "operator", "man_made", "barrier",
            "landuse", "geometry"]
    tags = {k: True for k in ["natural", "water", "waterway", "building",
                              "highway", "aeroway", "man_made", "barrier",
                              "landuse", "surface", "boundary", "leisure"]}
    for i in range(tries):
        try:
            gdf = ox.features_from_bbox(bbox, tags).reset_index()
            return gdf[[c for c in keep if c in gdf.columns]]
        except Exception as err:          # Overpass busy or timed out
            print(f"Overpass attempt {i + 1}: {err!s:.80}")
            time.sleep(30 * 2 ** i)
    raise RuntimeError("Overpass unavailable")


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


def land_from_coastline(coast, bbox):
    """Polygonize OSM coastline against the bbox (land lies left of ways).

    Closed rings (islands) lose orientation in osmnx, so they are taken as
    land directly.
    """
    import geopandas as gpd
    from shapely.geometry import LineString, Point, Polygon, box
    from shapely.ops import polygonize, unary_union

    frame = box(*bbox)
    lines = [g for g in coast.geometry.explode(index_parts=False)
             if isinstance(g, LineString)]
    islands = [Polygon(g) for g in lines if g.is_ring]
    open_ways = [g for g in lines if not g.is_ring]
    faces = list(polygonize(unary_union(open_ways + [frame.exterior])))
    land = set()
    for ln in open_ways:
        for a, b in zip(ln.coords[:-1], ln.coords[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            norm = (dx ** 2 + dy ** 2) ** 0.5 or 1
            p = Point((a[0] + b[0]) / 2 - 1e-6 * dy / norm,
                      (a[1] + b[1]) / 2 + 1e-6 * dx / norm)
            land.update(i for i, f in enumerate(faces) if f.contains(p))
    geom = unary_union([faces[i] for i in land] + islands)
    return gpd.GeoDataFrame(geometry=[geom], crs=4326).explode(
        index_parts=False)


def zoom_layers(sites=None):
    """Town-scale layers: OSM coast, land, water, buildings, roads, airport,
    plus TIGER 2024 water, roads and the Utqiagvik place boundary.

    sites maps a name to (lat, lon) for close-up detail layers
    (detail_<name>_buildings, _roads_tracks, _towers_masts, _ponds, ...).
    """
    import geopandas as gpd

    cfg = map_config()
    zoom, tiger = cfg["layer_zoom"], cfg["tiger"]
    sites = sites or {"c1": (71.3230, -156.6114), "e12": (71.2747, -156.6412)}
    o = fetch_osm(zoom)
    poly = ["Polygon", "MultiPolygon"]
    line = ["LineString", "MultiLineString"]
    coast = pick_osm(o, zoom, natural="coastline")
    coast = gpd.GeoDataFrame(coast.drop(columns="geometry"), crs=4326,
                             geometry=[g.boundary if g.geom_type == "Polygon"
                                       else g for g in coast.geometry])
    place = census_layer(f"{tiger}/PLACE/tl_2024_02_place.zip")
    layers = {
        "coastline": coast,
        "land": land_from_coastline(coast, zoom).reset_index(drop=True),
        "water_osm": pick_osm(o, zoom, poly, natural="water", water=True),
        "waterways_osm": pick_osm(o, zoom, line, waterway=True),
        "water_tiger": clip_layer(census_layer(
            f"{tiger}/AREAWATER/tl_2024_02185_areawater.zip"), zoom),
        # select by GEOID: the NAME carries a diacritic (Utqiaġvik)
        "town_boundary": place[place.GEOID == "0281920"].reset_index(
            drop=True),
        "buildings": pick_osm(o, zoom, poly, building=True),
        "roads_osm": pick_osm(o, zoom, line, highway=True),
        "roads_tiger": clip_layer(census_layer(
            f"{tiger}/ROADS/tl_2024_02185_roads.zip"), zoom),
        "airport": pick_osm(o, zoom, aeroway=True),
        "protected_areas": pick_osm(o, zoom, boundary="protected_area",
                                    leisure="nature_reserve"),
    }
    for name, (lat, lon) in sites.items():
        bb = (lon - 0.017, lat - 0.0055, lon + 0.017, lat + 0.0055)
        pre = f"detail_{name}_"
        layers.update({
            pre + "buildings": pick_osm(o, bb, poly, building=True),
            pre + "pads_landuse": pick_osm(o, bb, poly, landuse=True,
                                           surface=True, aeroway="apron"),
            pre + "roads_tracks": pick_osm(o, bb, line, highway=True),
            pre + "towers_masts": pick_osm(o, bb, man_made=["mast", "tower",
                                                            "antenna"]),
            pre + "fences": pick_osm(o, bb, barrier=True),
            pre + "ponds": pick_osm(o, bb, poly, natural="water", water=True),
            pre + "other_man_made": pick_osm(o, bb, man_made=True),
        })
    return layers


def inset_layers():
    """Northern-Alaska inset: CB 2024 500k state and North Slope Borough,
    TIGER lakes over 5 km2, and an ocean polygon (approximate east of 141 W).
    """
    import geopandas as gpd
    from shapely.geometry import Polygon, box

    cfg = map_config()
    inset, tiger, cb = cfg["layer_inset"], cfg["tiger"], cfg["cb"]
    states = census_layer(f"{cb}/cb_2024_us_state_500k.zip")
    ak = clip_layer(states[states.STUSPS == "AK"], inset)
    county = census_layer(f"{cb}/cb_2024_us_county_500k.zip")
    lakes = census_layer(f"{tiger}/AREAWATER/tl_2024_02185_areawater.zip")
    lakes = lakes[(lakes.MTFCC == "H2030")
                  & (lakes.to_crs(3338).area > 5e6)]
    yukon = Polygon([(-141.0006, 66), (-140, 66), (-140, 69.58),
                     (-141.0006, 69.65)])      # no Canadian source used
    ocean = gpd.GeoDataFrame(geometry=[box(*inset).difference(
        ak.union_all()).difference(yukon)], crs=4326)
    return {
        "alaska_land": ak,
        "coastline": clip_layer(gpd.GeoDataFrame(
            geometry=ak.boundary.explode(index_parts=False).values,
            crs=4326), inset),
        "ocean": ocean,
        "north_slope_borough": county[county.GEOID == "02185"].reset_index(
            drop=True),
        "lakes_gt5km2": clip_layer(lakes, inset),
    }


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
    """Read one GeoPackage layer, optionally only features touching a
    (W, E, S, N) box. Geometries are not clipped."""
    import geopandas as gpd

    bbox = None if box is None else (box[0], box[2], box[1], box[3])
    return gpd.read_file(gpkg, layer=name, bbox=bbox)


# --------------------------------------------------------------- imagery

def xyz_tile(lat, lon, z):
    """Web-Mercator XYZ tile index containing a point."""
    n = 2 ** z
    x = int((lon + 180) / 360 * n)
    y = int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n)
    return x, y


def imagery_mosaic(w, e, s, n, z, cache="/tmp/esri_tiles"):
    """Esri World Imagery mosaic covering a box.

    Returns (RGB uint8 array, extent in EPSG:3857 as x0, x1, y0, y1). Needs
    server.arcgisonline.com on the allowlist. Zoom 18 is the deepest level
    with imagery at NSA (19 returns 'Map data not yet available' tiles).
    """
    import io

    import numpy as np
    import requests
    from PIL import Image

    url = map_config()["tile_url"]
    os.makedirs(cache, exist_ok=True)
    x0, y0 = xyz_tile(n, w, z)
    x1, y1 = xyz_tile(s, e, z)
    rows = []
    for ty in range(y0, y1 + 1):
        row = []
        for tx in range(x0, x1 + 1):
            f = os.path.join(cache, f"{z}_{tx}_{ty}.jpg")
            if not os.path.exists(f):
                r = requests.get(url.format(z=z, y=ty, x=tx), timeout=30)
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
    """Source, date and resolution of the Esri World Imagery at a point."""
    import requests

    url = ("https://server.arcgisonline.com/ArcGIS/rest/services/"
           "World_Imagery/MapServer/identify")
    p = dict(geometry=f"{lon},{lat}", geometryType="esriGeometryPoint",
             sr=4326, tolerance=1, imageDisplay="400,400,96", f="json",
             mapExtent=f"{lon - 0.05},{lat - 0.05},{lon + 0.05},{lat + 0.05}",
             returnGeometry="false")
    res = requests.get(url, params=p, timeout=30).json().get("results", [])
    return res[0]["attributes"] if res else {}


def local_tm(box):
    """Ellipsoidal Transverse Mercator centred on a (W, E, S, N) box."""
    import cartopy.crs as ccrs

    return ccrs.TransverseMercator(central_longitude=(box[0] + box[1]) / 2,
                                   central_latitude=(box[2] + box[3]) / 2)


def tiles_in(proj, ext):
    """Map an EPSG:3857 mosaic extent into an ellipsoidal projection.

    Never hand Web-Mercator tiles to ccrs.GOOGLE_MERCATOR or epsg(3857):
    cartopy converts PlateCarree (WGS84) points to that sphere with a datum
    shift, misplacing them by about 23 km at 71 N relative to the tiles.
    Corners go through pyproj to lon/lat, then into the target projection;
    over a box a few km across the residual distortion is sub-metre.
    """
    import numpy as np

    t = map_tools()
    lon, lat = t.to_ll.transform([ext[0], ext[1]], [ext[2], ext[3]])
    p = proj.transform_points(t.pc, np.array(lon), np.array(lat))
    return p[0, 0], p[1, 0], p[0, 1], p[1, 1]


# --------------------------------------------------------------- drawing

def site_map_assets():
    """The shipped mapped-asset table (site_map_assets.csv) and NEON plot
    centres (neon_barr_plot_centres.csv) as two DataFrames."""
    import sys

    import pandas as pd

    here = os.path.dirname(sys._getframe().f_code.co_filename)
    a = pd.read_csv(os.path.join(here, "site_map_assets.csv"))
    a["color"] = a.group.map(map_config()["col"])
    plots = pd.read_csv(os.path.join(here, "neon_barr_plot_centres.csv"))
    return a, plots


def inside(df, box):
    return df.lon.between(box[0], box[1]) & df.lat.between(box[2], box[3])


def box_around(lat, lon, half_m):
    dlat = half_m / 111200
    dlon = half_m / (111320 * math.cos(math.radians(lat)))
    return lon - dlon, lon + dlon, lat - dlat, lat + dlat


def draw(ax, gdf, **kw):
    """Add GeoDataFrame geometries; never gdf.plot on a cartopy axes (it
    resets the aspect to 1/cos(lat), about 3 at 71 N)."""
    if len(gdf):
        ax.add_geometries(gdf.geometry, crs=map_tools().pc, **kw)


def scalebar(ax, metres, text, loc=(0.05, 0.05), color="k"):
    """True-distance (geodesic) scale bar, valid in any projection."""
    import numpy as np

    t = map_tools()
    x0, x1, y0, y1 = ax.get_extent(t.pc)
    lon0, lat0 = x0 + loc[0] * (x1 - x0), y0 + loc[1] * (y1 - y0)
    lon1, lat1, _ = t.geod.fwd(lon0, lat0, 90, metres)
    p = ax.projection.transform_points(t.pc, np.array([lon0, lon1]),
                                       np.array([lat0, lat1]))
    halo = t.halo if color == "k" else t.halo_dk
    ax.plot(p[:, 0], p[:, 1], color=color, lw=3, solid_capstyle="butt",
            transform=ax.projection, zorder=20, path_effects=halo)
    ax.text(p[:, 0].mean(), p[0, 1], text + "\n", ha="center", va="center",
            color=color, transform=ax.projection, zorder=20,
            path_effects=halo)


def plot_assets(ax, df, scale=1.0, edge="k"):
    """Colour = operator group, shape = asset type, hollow = nominal."""
    pc, size = map_tools().pc, map_config()["size"]
    for (mk, prec), g in df.groupby(["marker", "precise"]):
        ax.scatter(g.lon, g.lat, transform=pc, marker=mk, zorder=12,
                   s=size[mk] * scale, linewidths=1.0,
                   c=g.color if prec else "none",
                   edgecolors=edge if prec else g.color.tolist())
        if not prec:     # thin halo so hollow markers read on imagery
            ax.scatter(g.lon, g.lat, transform=pc, marker=mk, zorder=11,
                       s=size[mk] * scale, facecolors="none",
                       edgecolors="white", linewidths=2.6)


def label(ax, lon, lat, text, dx, dy, dark=False, ha=None, frac=False,
          **kw):
    """Label with a thin leader anchored at the text edge nearest the point.
    (dx, dy) are offset points, or an axes-fraction position if frac."""
    t = map_tools()
    ha = ha or ("left" if dx >= 0 else "right")
    rel = (1, 0.5) if ha == "right" else (0, 0.5)
    ax.annotate(text, (lon, lat), xycoords=t.pc._as_mpl_transform(ax),
                xytext=(dx, dy), ha=ha, va="center", zorder=15,
                textcoords="axes fraction" if frac else "offset points",
                color="white" if dark else "k",
                path_effects=t.halo_dk if dark else t.halo,
                arrowprops=dict(arrowstyle="-", lw=0.6, shrinkA=0, shrinkB=3,
                                color="white" if dark else "k", relpos=rel),
                **kw)


def outline(ax, b, text, va="bottom", color="k", dark=False):
    from matplotlib.patches import Rectangle

    t, fs = map_tools(), map_config()["fs"]
    ax.add_patch(Rectangle((b[0], b[2]), b[1] - b[0], b[3] - b[2],
                           transform=t.pc, fc="none", ec=color, lw=1.2,
                           zorder=13))
    ax.text(b[1], b[3] if va == "bottom" else b[2], text, transform=t.pc,
            va=va, fontweight="bold", fontsize=fs["title"], color=color,
            path_effects=t.halo_dk if dark else t.halo, zorder=15)


def connect(fig, ax, b, axd, below=False):
    """Leader lines from box b on ax to close-up axd (to the right/below)."""
    from matplotlib.patches import ConnectionPatch

    pc = map_tools().pc
    pairs = ((((b[0], b[2]), (0, 1)), ((b[1], b[2]), (1, 1))) if below else
             (((b[1], b[3]), (0, 1)), ((b[1], b[2]), (0, 0))))
    for (lo, la), xyb in pairs:
        fig.add_artist(ConnectionPatch(
            (lo, la), xyb, coordsA=pc._as_mpl_transform(ax),
            coordsB=axd.transAxes, color="#444", lw=0.7, zorder=30))


def line_label(ax, gdf, box, text, frac=0.5, rot=0):
    """Label a line feature on its part inside box (clip first: bbox reads
    return whole geometries that may extend far outside the panel)."""
    t, fs = map_tools(), map_config()["fs"]
    g = gdf.geometry.clip_by_rect(box[0], box[2], box[1], box[3])
    g = g[~g.is_empty]
    if len(g):
        pt = g.iloc[0].interpolate(frac, normalized=True)
        ax.text(pt.x, pt.y, text, transform=t.pc, color="w",
                fontsize=fs["label"], rotation=rot, ha="center",
                va="center", path_effects=t.halo_dk, zorder=14)


def distance_triangle(ax, A, legs, color="#1a1a1a"):
    """Geodesic dimension lines between assets, labelled km and bearing.

    legs: (key_a, key_b, name, side) with side +1 outside the triangle and
    -1 inside.
    """
    import numpy as np

    t, fs = map_tools(), map_config()["fs"]
    keys = sorted({k for leg in legs for k in leg[:2]})
    pts = {k: A[A.key == k].iloc[0] for k in keys}
    cen = ax.projection.transform_points(
        t.pc, np.array([pts[k].lon for k in keys]),
        np.array([pts[k].lat for k in keys]))[:, :2].mean(axis=0)
    for a, b, name, side in legs:
        p, q = pts[a], pts[b]
        az, _, d = t.geod.inv(p.lon, p.lat, q.lon, q.lat)
        xy = ax.projection.transform_points(
            t.pc, np.array([p.lon, q.lon]), np.array([p.lat, q.lat]))[:, :2]
        ax.plot(xy[:, 0], xy[:, 1], color=color, lw=1.3, zorder=7,
                transform=ax.projection, path_effects=t.halo)
        v = (xy[1] - xy[0]) / np.hypot(*(xy[1] - xy[0]))
        n = np.array([-v[1], v[0]])
        for e in xy:                                   # 90 m end ticks
            ax.plot([e[0] - 90 * n[0], e[0] + 90 * n[0]],
                    [e[1] - 90 * n[1], e[1] + 90 * n[1]], color=color,
                    lw=1.3, zorder=7, transform=ax.projection)
        out = n if np.dot(n, xy.mean(axis=0) - cen) >= 0 else -n
        ang = np.degrees(np.arctan2(v[1], v[0]))
        ang = ang - 180 if ang > 90 else ang + 180 if ang < -90 else ang
        ax.annotate(f"{name}\n{d / 1000:.2f} km, {az % 360:.0f}°",
                    xy.mean(axis=0),
                    xycoords=ax.projection._as_mpl_transform(ax),
                    xytext=out * side * 16, textcoords="offset points",
                    rotation=ang, rotation_mode="anchor", ha="center",
                    va="center", fontsize=fs["label"], fontweight="bold",
                    color=color, path_effects=t.halo, zorder=16)


def legend_handles():
    from matplotlib.lines import Line2D

    col = map_config()["col"]
    h = [Line2D([], [], ls="", marker="s", ms=8, mfc=c, mec="k", label=g)
         for g, c in [("ARM", col["ARM"]), ("NOAA", col["NOAA"]),
                      ("NSF NEON", col["NEON"]),
                      ("Other research", col["Research"]),
                      ("Historic / military", col["Historic"])]]
    h += [Line2D([], [], ls="", marker=m, ms=s, mfc="#bdbdbd", mec="k",
                 label=text) for m, s, text in
          [("*", 13, "Main facility / observatory"),
           ("s", 7, "Extended facility / building"),
           ("^", 8, "Scanning radar"), ("o", 6, "Station / instrument"),
           ("D", 6, "Sounding launch")]]
    h += [Line2D([], [], ls="", marker="o", ms=6, mfc="none", mec="k",
                 label="Hollow = nominal or rounded coordinate"),
          Line2D([], [], ls="", marker=".", ms=5, color=col["NEON"],
                 label="NEON observational plot"),
          Line2D([], [], color="#3a3a3a", lw=1.0, label="Road (OSM)"),
          Line2D([], [], color="#8a8a8a", lw=0.9, ls=(0, (4, 2)),
                 label="Utqiaġvik city limit (TIGER)"),
          Line2D([], [], color="#7a3f8f", lw=1.0, ls=(0, (1, 1.5)),
                 label="BEO bounding box")]
    return h


# ---------------------------------------------------------------- panels

def base_layers(ax, gpkg, box):
    """Ocean background, OSM land/water/coast/buildings/roads, TIGER town."""
    ax.set_facecolor("#cfe3ef")
    draw(ax, read_layer(gpkg, "land", box), facecolor="#f2efe6",
         edgecolor="none")
    for name in ("water_osm", "water_tiger"):
        draw(ax, read_layer(gpkg, name, box), facecolor="#cfe3ef",
             edgecolor="#8fb3c9", lw=0.3)
    draw(ax, read_layer(gpkg, "coastline", box), facecolor="none",
         edgecolor="#5b87a6", lw=0.7)
    draw(ax, read_layer(gpkg, "town_boundary", box), facecolor="none",
         edgecolor="#8a8a8a", lw=0.9, linestyle=(0, (4, 2)))
    air = read_layer(gpkg, "airport", box)
    draw(ax, air[air.geom_type.str.contains("Polygon")], facecolor="#d4d4d4",
         edgecolor="none")
    draw(ax, read_layer(gpkg, "buildings", box), facecolor="#4d4d4d",
         edgecolor="none")
    roads = read_layer(gpkg, "roads_osm", box)
    for kinds, ec, lw, ls in (
            (("tertiary", "unclassified"), "#3a3a3a", 1.0, "-"),
            (("residential", "service"), "#6b6b6b", 0.5, "-"),
            (("track", "path", "footway", "steps"), "#6b6b6b", 0.4,
             (0, (2, 1.5)))):
        draw(ax, roads[roads.highway.isin(kinds)], facecolor="none",
             edgecolor=ec, lw=lw, linestyle=ls)


def detail_panel(fig, rect, A, plots, box, z, labels, letter, title):
    """Imagery close-up in a local TM, with assets and column labels."""
    t, fs = map_tools(), map_config()["fs"]
    proj = local_tm(box)
    axd = fig.add_axes(rect, projection=proj)
    img, ext = imagery_mosaic(*box, z)
    axd.imshow(img, extent=tiles_in(proj, ext), transform=proj,
               origin="upper", interpolation="lanczos", zorder=0)
    axd.set_extent(box, t.pc)
    nb = plots[inside(plots, box)]
    axd.scatter(nb.lon, nb.lat, transform=t.pc, s=14, zorder=10, lw=0.5,
                c=map_config()["col"]["NEON"], edgecolors="w")
    plot_assets(axd, A[inside(A, box)], edge="w")
    for k, (text, x, y, ha) in labels.items():
        r = A[A.key == k].iloc[0]
        label(axd, r.lon, r.lat, text, x, y, dark=True, ha=ha, frac=True,
              fontsize=fs["label"])
    axd.text(0.0, 1.012, letter, transform=axd.transAxes, va="bottom",
             fontsize=fs["letter"], fontweight="bold")
    axd.text(0.05, 1.012, title, transform=axd.transAxes, va="bottom")
    axd.text(0.99, 0.01, "Imagery: Esri, Vantor WV03 (7 Sep 2025)",
             transform=axd.transAxes, ha="right", va="bottom",
             fontsize=fs["small"], color="w", path_effects=t.halo_dk,
             zorder=20)
    return axd


def main_map(fig, rect, A, plots, gpkg):
    import numpy as np
    from matplotlib.patches import Rectangle

    t, cfg = map_tools(), map_config()
    fs, beo = cfg["fs"], cfg["beo_box"]
    ax = fig.add_axes(rect, projection=local_tm(cfg["main"]))
    ax.set_extent(cfg["main"], t.pc)
    base_layers(ax, gpkg, cfg["main"])
    ax.add_patch(Rectangle((beo[0], beo[2]), beo[1] - beo[0],
                           beo[3] - beo[2], transform=t.pc, fc="none",
                           ec="#7a3f8f", lw=1.0, ls=(0, (1, 1.5)), zorder=6))
    ax.scatter(plots.lon, plots.lat, transform=t.pc, s=6, zorder=8, lw=0,
               c=cfg["col"]["NEON"])
    keep = A.key.isin(["c1_page", "brw", "e12", "tower"])
    plot_assets(ax, A[(~inside(A, cfg["c1_box"])
                       & ~inside(A, cfg["e12_box"])) | keep], scale=0.8)
    for k, (text, dx, dy) in cfg["lab_main"].items():
        r = A[A.key == k].iloc[0]
        label(ax, r.lon, r.lat, text, dx, dy, fontsize=fs["label"])
    outline(ax, cfg["c1_box"], " b")
    outline(ax, cfg["e12_box"], " c", va="top")
    for lo, la, text in [(-156.835, 71.335, "Chukchi Sea"),
                         (-156.50, 71.355, "Elson Lagoon"),
                         (-156.765, 71.300, "Utqiaġvik"),
                         (-156.47, 71.383, "Point Barrow (Nuvuk)"),
                         (-156.53, 71.262, "Barrow Environmental\n"
                                           "Observatory (BEO)")]:
        water = "Sea" in text or "Lagoon" in text
        ax.text(lo, la, text, transform=t.pc, ha="center", zorder=9,
                style="italic" if water else "normal", path_effects=t.halo,
                color="#2f5f80" if water else "#333")
    gl = ax.gridlines(t.pc, draw_labels=True, lw=0.3, color="#777",
                      alpha=0.5, xlocs=np.arange(-157, -156.2, 0.1),
                      ylocs=np.arange(71.20, 71.45, 0.05))
    gl.top_labels = gl.right_labels = False
    gl.xlabel_style = gl.ylabel_style = dict(size=fs["small"], rotation=0)
    scalebar(ax, 2000, "2 km", loc=(0.05, 0.035))
    distance_triangle(ax, A, cfg["triangle"])
    return ax


def wide_inset(fig, rect, gpkg):
    t, cfg = map_tools(), map_config()
    fs = cfg["fs"]
    axi = fig.add_axes(rect, projection=t.ccrs.LambertConformal(
        central_longitude=-154.5, central_latitude=69,
        standard_parallels=(66, 71)))
    axi.set_extent(cfg["inset"], t.pc)
    axi.set_facecolor("#cfe3ef")
    draw(axi, read_layer(gpkg, "alaska_land"), facecolor="#f2efe6",
         edgecolor="#5b87a6", lw=0.5)
    draw(axi, read_layer(gpkg, "lakes_gt5km2"), facecolor="#cfe3ef",
         edgecolor="none")
    draw(axi, read_layer(gpkg, "north_slope_borough"), facecolor="none",
         edgecolor="#8a8a8a", lw=0.6, linestyle=(0, (4, 2)))
    arm = cfg["col"]["ARM"]
    for lo, la, text, dx, dy, mk in cfg["inset_sites"]:
        main = mk == "*"
        axi.scatter(lo, la, transform=t.pc, marker=mk, lw=1.1, zorder=11,
                    s=120 if main else 36, c=arm if main else "none",
                    edgecolors="k" if main else arm)
        label(axi, lo, la, text, dx, dy, fontsize=fs["label"])
    for lo, la, text in [(-163.5, 70.6, "Chukchi\nSea"),
                         (-145.5, 70.75, "Beaufort Sea"),
                         (-151.5, 67.4, "North Slope\nBorough")]:
        water = "Sea" in text
        axi.text(lo, la, text, transform=t.pc, ha="center",
                 fontsize=fs["label"], path_effects=t.halo,
                 style="italic" if water else "normal",
                 color="#2f5f80" if water else "#555")
    return axi


def build_site_map(layers_gpkg, inset_gpkg, path="nsa_utqiagvik_asset_map.png",
                   dpi=300):
    """Four-panel map: a) main map with the northern-Alaska inset top-left
    and the C1-E12-X-SAPR distance triangle, b) C1/NOAA BRW imagery
    close-up, c) E12 with NEON BARR and NGEE, d) E12 at 400 m.

    layers_gpkg/inset_gpkg come from write_layers(zoom_layers(), ...) and
    write_layers(inset_layers(), ...). Save without bbox_inches='tight':
    the tight bbox is recomputed around the manually placed inset and crops
    the main map away.
    """
    import matplotlib.pyplot as plt

    cfg = map_config()
    fs = cfg["fs"]
    A, plots = site_map_assets()
    plt.rcParams["savefig.bbox"] = None
    fig = plt.figure(figsize=(15.5, 12.8))
    ax = main_map(fig, [0.045, 0.20, 0.60, 0.76], A, plots, layers_gpkg)
    wide_inset(fig, [0.052, 0.715, 0.235, 0.245], inset_gpkg)
    fig.legend(handles=legend_handles(), loc="upper left", ncol=4,
               bbox_to_anchor=(0.045, 0.165), frameon=False,
               fontsize=fs["label"], labelspacing=0.6, handlelength=1.6,
               handletextpad=0.6, columnspacing=1.6, alignment="left",
               title_fontsize=fs["label"],
               title="Colour = operator · shape = asset type")
    fig.text(0.045, 0.035, "Basemap: © OpenStreetMap contributors (ODbL); "
             "US Census TIGER/Line 2024 and CB 2024. Imagery (b–d): Esri "
             "World Imagery, Vantor WorldView-3, 7 Sep 2025, 0.31 m.",
             fontsize=fs["small"], color="#444")
    fig.text(0.047, 0.972, "a", fontsize=fs["letter"], fontweight="bold")
    fig.text(0.07, 0.972, "ARM North Slope of Alaska observatory and "
             "neighbouring research assets, Utqiaġvik", fontsize=fs["title"])
    axb = detail_panel(fig, [0.665, 0.625, 0.325, 0.33], A, plots,
                       cfg["c1_box"], 17, cfg["lab_c1"], "b",
                       "Main site: ARM C1/E10/E30 and NOAA GML BRW")
    towers = read_layer(layers_gpkg, "detail_c1_towers_masts")
    draw(axb, towers, facecolor="none", edgecolor="#ffd84d", lw=1.2,
         zorder=9)
    if len(towers):
        t0 = towers.to_crs(3857).centroid.to_crs(4326).iloc[0]
        label(axb, t0.x, t0.y, "Towers (OSM)", 0.58, 0.95, ha="left",
              frac=True, dark=True, fontsize=fs["label"])
    scalebar(axb, 200, "200 m", loc=(0.06, 0.05), color="w")
    connect(fig, ax, cfg["c1_box"], axb)
    axc = detail_panel(fig, [0.665, 0.335, 0.325, 0.25], A, plots,
                       cfg["e12_box"], 16, cfg["lab_e12"], "c",
                       "ARM E12 on the BEO, with NEON BARR and NGEE Arctic")
    rd = read_layer(layers_gpkg, "roads_osm", cfg["e12_box"])
    line_label(axc, rd[rd.name == "Eastfield Road"], cfg["e12_box"],
               "Cake Eater Rd\n(OSM: Eastfield Rd)", frac=0.55, rot=82)
    scalebar(axc, 500, "500 m", loc=(0.06, 0.05), color="w")
    connect(fig, ax, cfg["e12_box"], axc)
    e = A[A.key == "e12"].iloc[0]
    zb = box_around(e.lat, e.lon, cfg["e12_half_m"])
    outline(axc, zb, " d", color="w", dark=True)
    axd = detail_panel(fig, [0.665, 0.035, 0.325, 0.26], A, plots, zb, 18,
                       cfg["lab_e12_zoom"], "d", "E12 close-up (400 m)")
    rz = read_layer(layers_gpkg, "roads_osm", zb)
    foot = rz[rz.highway == "footway"]
    draw(axd, foot, facecolor="none", edgecolor="#ffd84d", lw=1.0, zorder=9)
    line_label(axd, foot, zb, "footway\n(OSM)", frac=0.2)
    hut = read_layer(layers_gpkg, "detail_e12_buildings", zb)
    draw(axd, hut, facecolor="none", edgecolor="#ffd84d", lw=1.2, zorder=9)
    if len(hut):
        h0 = hut.to_crs(3857).centroid.to_crs(4326).iloc[0]
        label(axd, h0.x, h0.y, "Building (OSM)", 0.62, 0.62, ha="left",
              frac=True, dark=True, fontsize=fs["label"])
    line_label(axd, rz[rz.name == "Eastfield Road"], zb, "Cake Eater Rd",
               frac=0.3, rot=72)
    scalebar(axd, 50, "50 m", loc=(0.06, 0.05), color="w")
    connect(fig, axc, zb, axd, below=True)
    fig.savefig(path, dpi=dpi)
    return fig
