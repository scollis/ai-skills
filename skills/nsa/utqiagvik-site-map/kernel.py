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
            "e11": ("ARM E11 Point Barrow\n(ECOR, SEBS; to 2016)", -14, -20),
            "asos": ("ASOS PABR", 14, -10),
            "ua": ("NWS upper air 70026", -16, -12),
            "iceradar": ("UAF sea-ice radar", -16, 12),
            "coops": ("CO-OPS Barrow Offshore\n(2008–10)", 12, -16),
            "mbs": ("Sea-ice mass balance\nsite (approx.)", 12, 10),
            "b1": ("SIZONet\nmooring B1", 10, -16),
            "mp1": ("NEON megapit\n(2016)", -14, -10)},
        # close-up labels: (text, x, y, ha) in axes fraction, in columns
        lab_c1={
            "ecor": ("ECOR", 0.30, 0.87, "right"),
            "dl": ("Doppler lidar", 0.30, 0.71, "right"),
            "mag": ("USGS magnetic obs.", 0.03, 0.43, "left"),
            "aos": ("Aerosol: ARM E30 + NOAA AOS", 0.50, 0.29, "right"),
            "sonde": ("Sonde launch (files: 0.01°)", 0.33, 0.12, "left"),
            "brw": ("NOAA GML BRW", 0.52, 0.95, "right"),
            "sebs": ("SEBS, LPM", 0.80, 0.89, "left"),
            "aeri": ("AERI", 0.80, 0.77, "left"),
            "bsrn": ("BSRN BAR\n(to 2016)", 0.80, 0.66, "left"),
            "c1_file": ("C1 nominal\n(39 instruments)", 0.80, 0.51, "left"),
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
        lab_e12_zoom={"e12": ("ARM E12: 6 instruments\n"
                              "share this file position", 0.52, 0.30,
                              "left")},
        # triangle legs: name, +1 label outside the triangle, -1 inside
        triangle=(("c1_file", "e12", "C1 → E12", 1),
                  ("c1_file", "xsapr", "C1 → X-SAPR", -1),
                  ("e12", "xsapr", "E12 → X-SAPR", -1)),
    )


def lonlat_crs():
    """A PlateCarree that is plain lon/lat in degrees.

    With PROJ 9.8 (cartopy 0.25), ccrs.PlateCarree() is eqc on the WGS84
    ellipsoid scaled by +to_meter; ellipsoidal eqc is no longer linear in
    latitude, so lon/lat passed through it land about 23 km off at 71 N
    (24 km at 45 N, 0 at the equator) in any ellipsoidal projection. On a
    sphere globe eqc is linear and the error is zero.
    """
    import cartopy.crs as ccrs

    return ccrs.PlateCarree(globe=ccrs.Globe(
        ellipse=None, semimajor_axis=6378137, semiminor_axis=6378137))


def map_tools():
    """Heavy imports and CRS objects, resolved at call time."""
    from types import SimpleNamespace

    import cartopy.crs as ccrs
    import matplotlib.patheffects as pe
    import pyproj

    return SimpleNamespace(
        ccrs=ccrs, pc=lonlat_crs(),
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

    Corners go through pyproj to lon/lat, then (via lonlat_crs) into the
    target projection, and the mosaic is drawn axis-aligned. Over a box a few
    km across the residual distortion is sub-metre; for larger boxes use
    warp_mosaic, which resamples per pixel.
    """
    import numpy as np

    t = map_tools()
    lon, lat = t.to_ll.transform([ext[0], ext[1]], [ext[2], ext[3]])
    p = proj.transform_points(t.pc, np.array(lon), np.array(lat))
    return p[0, 0], p[1, 0], p[0, 1], p[1, 1]


def warp_mosaic(img, ext, proj, box, width_px=2400):
    """Resample an EPSG:3857 mosaic onto a regular grid in proj covering box
    (W, E, S, N). Exact per pixel: proj -> lon/lat -> EPSG:3857 (pyproj) ->
    bilinear sample. Returns (RGB array, extent in proj units)."""
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
    to3857 = t.to_ll.__class__.from_crs(4326, 3857, always_xy=True)
    mx, my = to3857.transform(ll[:, 0], ll[:, 1])
    col = (mx - ext[0]) / (ext[1] - ext[0]) * img.shape[1] - 0.5
    row = (ext[3] - my) / (ext[3] - ext[2]) * img.shape[0] - 0.5
    out = np.stack([map_coordinates(img[..., b].astype(float), [row, col],
                                    order=1, mode="nearest").reshape(h, width_px)
                    for b in range(3)], -1)
    return out.clip(0, 255).astype(np.uint8), (x0, x1, y0, y1)


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
    halo = t.halo_dk if color.lower() in ("#ffffff", "w", "white") else t.halo
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
                transform=ax.projection, path_effects=halo)
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
                    color=color, path_effects=halo, zorder=16)


def legend_handles(dark=False):
    from matplotlib.lines import Line2D

    col = map_config()["col"]
    ec = "w" if dark else "k"
    h = [Line2D([], [], ls="", marker="s", ms=8, mfc=c, mec=ec, label=g)
         for g, c in [("ARM", col["ARM"]), ("NOAA", col["NOAA"]),
                      ("NSF NEON", col["NEON"]),
                      ("Other research", col["Research"])]]
    h += [Line2D([], [], ls="", marker=m, ms=s, mfc="#bdbdbd", mec=ec,
                 label=text) for m, s, text in
          [("*", 13, "Main facility / observatory"),
           ("s", 7, "Extended facility / building"),
           ("^", 8, "Scanning radar"), ("o", 6, "Station / instrument"),
           ("D", 6, "Sounding launch")]]
    h += [Line2D([], [], ls="", marker="o", ms=6, mfc="none", mec=ec,
                 label="Hollow = nominal or rounded coordinate"),
          Line2D([], [], ls="", marker=".", ms=5, color=col["NEON"],
                 label="NEON observational plot"),
          Line2D([], [], color="#c9ced3" if dark else "#3a3a3a", lw=1.0,
                 label="Road (OSM)"),
          Line2D([], [], color="#8a8a8a", lw=0.9, ls=(0, (4, 2)),
                 label="Utqiaġvik city limit (TIGER)"),
          Line2D([], [], color="#7a3f8f", lw=1.0, ls=(0, (1, 1.5)),
                 label="BEO bounding box")]
    return h


# ---------------------------------------------------------------- panels


def gmrt_grid(box, resolution="high", cache="layer_cache"):
    """GMRT topography/bathymetry (m, +up) for box=(w, e, s, n), from the
    GMRT GridServer as Esri ASCII (no raster library needed). Cached.
    Returns (z, extent) with z north-up and extent=(w, e, s, n)."""
    import numpy as np
    import requests

    w, e, s, n = box
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, f"gmrt_{w}_{e}_{s}_{n}_{resolution}.asc")
    if not os.path.exists(path):
        r = requests.get("https://www.gmrt.org/services/GridServer", timeout=300,
                         params=dict(minlongitude=w, maxlongitude=e,
                                     minlatitude=s, maxlatitude=n,
                                     format="esriascii", layer="topo",
                                     resolution=resolution))
        r.raise_for_status()
        open(path, "w").write(r.text)
    with open(path) as f:
        hdr = {k.lower(): float(v) for k, v in (next(f).split() for _ in range(6))}
        z = np.loadtxt(f, dtype="f4")
    z[z == hdr["nodata_value"]] = np.nan
    x0, y0, c = hdr["xllcorner"], hdr["yllcorner"], hdr["cellsize"]
    nc, nr = int(hdr["ncols"]), int(hdr["nrows"])
    return z, (x0, x0 + nc * c, y0, y0 + nr * c)


def seaice_doc_grid():
    """1991-2020 mean day of sea-ice closing (shipped seaice_doc_1991_2020.csv).

    Day of closing = first day SIC exceeds 80% after the final summer minimum
    of a 5-day running mean, per ice year (1 Mar - end Feb), from the
    NOAA/NSIDC CDR v6 (G02202, doi:10.7265/b18j-z797), 25 km. Day of year from
    1 Jan; values > 365 fall in January. Returns (x_edges, y_edges, doc, crs)
    with crs the NSIDC north polar stereographic grid as a cartopy CRS."""
    import sys

    import cartopy.crs as ccrs
    import numpy as np

    here = os.path.dirname(sys._getframe().f_code.co_filename)
    rows = [r for r in open(os.path.join(here, "seaice_doc_1991_2020.csv"))
            if not r.startswith("#")]
    x = np.array(rows[0].strip().split(",")[1:], float)
    y = np.array([r.split(",")[0] for r in rows[1:]], float)
    doc = np.array([[float(v) if v else np.nan for v in r.strip().split(",")[1:]]
                    for r in rows[1:]])
    xe = np.r_[x - 12500, x[-1] + 12500]
    ye = np.r_[y + 12500, y[-1] - 12500]
    hughes = ccrs.Globe(ellipse=None, semimajor_axis=6378273.0,
                        semiminor_axis=6356889.449)
    crs = ccrs.NorthPolarStereo(central_longitude=-45, true_scale_latitude=70,
                                globe=hughes)
    return xe, ye, doc, crs


def doy_label(v):
    import datetime as dt
    return (dt.date(2001, 1, 1) + dt.timedelta(days=int(v) - 1)).strftime("%-d %b")


def bathy_cmap(dark=False):
    from matplotlib.colors import LinearSegmentedColormap
    cols = (["#2a4f6b", "#0b1824"] if dark else ["#e3f0f7", "#4f86ad"])
    return LinearSegmentedColormap.from_list("bathy", cols)


def draw_bathymetry(ax, box, dark=False, fill=True, levels=(10, 20, 50, 100),
                    resolution="max", smooth=3.0):
    """GMRT bathymetry under the land layers (fill) and labelled isobaths.

    GMRT's coastline is coarser than OSM's, so non-sea cells are filled from
    the nearest sea cell and the field is Gaussian-smoothed (smooth, in grid
    cells) before shading and contouring; land polygons drawn on top mask
    the land. Colour limits fit the 2-98th percentile of true sea depths."""
    import numpy as np
    from scipy.ndimage import distance_transform_edt, gaussian_filter

    t = map_tools()
    z, (w, e, s, n) = gmrt_grid(box, resolution)
    sea = np.isfinite(z) & (z < 0)
    idx = distance_transform_edt(~sea, return_distances=False,
                                 return_indices=True)
    dep = gaussian_filter(np.clip(-z[tuple(idx)], 0.5, None), smooth)
    lon = np.linspace(w, e, z.shape[1], endpoint=False) + (e - w) / z.shape[1] / 2
    lat = np.linspace(n, s, z.shape[0], endpoint=False) - (n - s) / z.shape[0] / 2
    vmin, vmax = np.nanpercentile(-z[sea], [2, 98])
    im = None
    if fill:
        im = ax.pcolormesh(lon, lat, dep, cmap=bathy_cmap(dark), vmin=vmin,
                           vmax=vmax, transform=t.pc, shading="nearest",
                           zorder=0.5, rasterized=True)
    cs = ax.contour(lon, lat, dep, levels=list(levels), transform=t.pc,
                    colors="#9fc3dc" if dark else "#3f6f93", linewidths=0.5,
                    zorder=0.6)
    ax.clabel(cs, fmt="%d m", fontsize=7, inline=True)
    return im, (vmin, vmax)

def map_themes():
    """Five map variants: background treatment and which close-ups to draw.

    main/detail backgrounds: vector (OSM/TIGER), imagery, imagery_grey.
    palette: light or dark vector styling and label contrast.
    inset: "seaice_doc" (1991-2020 mean day of closing) or "plain".
    bathy: GMRT bathymetry on the main map.
    """
    themes = {
        "overview_vector": dict(main="vector", palette="light", details=()),
        "overview_imagery": dict(main="imagery", palette="dark", details=()),
        "reference": dict(main="vector", palette="light",
                          details=("b", "c", "d"), detail="imagery"),
        "grey_imagery": dict(main="imagery_grey", palette="dark",
                             details=("b", "c", "d"), detail="imagery_grey"),
        "dark_vector": dict(main="vector", palette="dark",
                            details=("b", "c", "d"), detail="vector"),
    }
    # every theme: inset sea = mean day of ice closing; main-map sea = GMRT
    # bathymetry (filled on vector maps, isobaths only over imagery)
    for th in themes.values():
        th.setdefault("inset", "seaice_doc")
        th.setdefault("bathy", True)
    return themes


def palette(name):
    light = dict(ocean="#cfe3ef", land="#f2efe6", water="#cfe3ef",
                 lake_edge="#8fb3c9", coast="#5b87a6", town="#8a8a8a",
                 airport="#d4d4d4", building="#4d4d4d", road_major="#3a3a3a",
                 road_minor="#6b6b6b", text="#333333", sea_text="#2f5f80",
                 line="#1a1a1a", dark=False)
    dark = dict(ocean="#0e1a26", land="#262a2e", water="#0e1a26",
                lake_edge="#2f4a60", coast="#5f8fb3", town="#9a9a9a",
                airport="#3c4146", building="#b8bec4", road_major="#c9ced3",
                road_minor="#8a9299", text="#e8e8e8", sea_text="#8fb9d8",
                line="#f2f2f2", dark=True)
    return dark if name == "dark" else light


def base_layers(ax, gpkg, box, pal=None, fill=True, marine=True):
    """OSM land/water/coast/buildings/roads and the TIGER town limit.
    fill=False draws only line work, for use over imagery. marine=False
    drops water polygons lying outside the land layer (TIGER area water
    includes coastal sea to a straight offshore limit), so bathymetry
    drawn underneath stays visible."""
    pal = pal or palette("light")
    if fill:
        ax.set_facecolor(pal["ocean"])
        land = read_layer(gpkg, "land", box)
        draw(ax, land, facecolor=pal["land"], edgecolor="none")
        for name in ("water_osm", "water_tiger"):
            wat = read_layer(gpkg, name, box)
            if not marine and len(wat) and len(land):
                inland = wat.representative_point().within(land.union_all())
                wat = wat[inland]
            draw(ax, wat, facecolor=pal["water"],
                 edgecolor=pal["lake_edge"], lw=0.3)
        air = read_layer(gpkg, "airport", box)
        draw(ax, air[air.geom_type.str.contains("Polygon")],
             facecolor=pal["airport"], edgecolor="none")
        draw(ax, read_layer(gpkg, "buildings", box),
             facecolor=pal["building"], edgecolor="none")
    draw(ax, read_layer(gpkg, "coastline", box), facecolor="none",
         edgecolor=pal["coast"], lw=0.7)
    draw(ax, read_layer(gpkg, "town_boundary", box), facecolor="none",
         edgecolor=pal["town"], lw=0.9, linestyle=(0, (4, 2)))
    roads = read_layer(gpkg, "roads_osm", box)
    for kinds, ec, lw, ls in (
            (("tertiary", "unclassified"), pal["road_major"], 1.0, "-"),
            (("residential", "service"), pal["road_minor"], 0.5, "-"),
            (("track", "path", "footway", "steps"), pal["road_minor"], 0.4,
             (0, (2, 1.5)))):
        draw(ax, roads[roads.highway.isin(kinds)], facecolor="none",
             edgecolor=ec, lw=lw, linestyle=ls)


def imagery_background(ax, box, z, grey=False, width_px=2400):
    """Esri imagery resampled exactly into the axes projection.
    grey=True desaturates and lightens it so coloured markers dominate."""
    import numpy as np

    img, ext = imagery_mosaic(*box, z)
    pad = (box[1] - box[0]) * 0.02, (box[3] - box[2]) * 0.02
    big = (box[0] - pad[0], box[1] + pad[0], box[2] - pad[1], box[3] + pad[1])
    out, oext = warp_mosaic(img, ext, ax.projection, big, width_px)
    if grey:
        lum = out @ np.array([0.299, 0.587, 0.114])
        out = np.repeat((0.55 * lum + 0.45 * 200)[..., None], 3, -1)
        out = out.clip(0, 255).astype(np.uint8)
    ax.imshow(out, extent=oext, transform=ax.projection, origin="upper",
              interpolation="lanczos", zorder=0)


def detail_panel(fig, rect, A, plots, box, z, labels, letter, title,
                 bg="imagery", gpkg=None, pal=None):
    """Close-up in a local TM: imagery, grey imagery or vector background,
    assets and column labels."""
    t, fs = map_tools(), map_config()["fs"]
    pal = pal or palette("light")
    axd = fig.add_axes(rect, projection=local_tm(box))
    axd.set_extent(box, t.pc)
    if bg == "vector":
        base_layers(axd, gpkg, box, pal)
    else:
        imagery_background(axd, box, z, grey=bg == "imagery_grey",
                           width_px=1800)
    axd.set_extent(box, t.pc)
    dark = bg != "vector" or pal["dark"]
    nb = plots[inside(plots, box)]
    axd.scatter(nb.lon, nb.lat, transform=t.pc, s=14, zorder=10, lw=0.5,
                c=map_config()["col"]["NEON"],
                edgecolors="w" if dark else "k")
    plot_assets(axd, A[inside(A, box)], edge="w" if dark else "k")
    for k, (text, x, y, ha) in labels.items():
        r = A[A.key == k].iloc[0]
        label(axd, r.lon, r.lat, text, x, y, dark=dark, ha=ha, frac=True,
              fontsize=fs["label"])
    tcol = pal["text"] if pal["dark"] else "k"
    axd.text(0.0, 1.012, letter, transform=axd.transAxes, va="bottom",
             fontsize=fs["letter"], fontweight="bold", color=tcol)
    axd.text(0.05, 1.012, title, transform=axd.transAxes, va="bottom",
             color=tcol)
    if bg != "vector":
        axd.text(0.99, 0.01, "Imagery: Esri, Vantor WV03 (7 Sep 2025)",
                 transform=axd.transAxes, ha="right", va="bottom",
                 fontsize=fs["small"], color="w", path_effects=t.halo_dk,
                 zorder=20)
    return axd, dark


def main_map(fig, rect, A, plots, gpkg, theme, outlines=True):
    import numpy as np
    from matplotlib.patches import Rectangle

    t, cfg = map_tools(), map_config()
    fs, beo, box = cfg["fs"], cfg["beo_box"], cfg["main"]
    pal = palette(theme["palette"])
    ax = fig.add_axes(rect, projection=local_tm(box))
    ax.set_extent(box, t.pc)
    bim = None
    if theme["main"] == "vector":
        if theme.get("bathy"):
            bim, blim = draw_bathymetry(ax, box, dark=pal["dark"],
                                        resolution="max")
        base_layers(ax, gpkg, box, pal, marine=not theme.get("bathy"))
    else:
        imagery_background(ax, box, 13, grey=theme["main"] == "imagery_grey",
                           width_px=2600)
        if theme.get("bathy"):
            draw_bathymetry(ax, box, dark=True, fill=False, resolution="max")
        base_layers(ax, gpkg, box, palette("dark"), fill=False)
    ax.set_extent(box, t.pc)
    if bim is not None:
        cax = ax.inset_axes([0.44, 0.835, 0.18, 0.014])
        cb = fig.colorbar(bim, cax=cax, orientation="horizontal")
        cb.set_label("Sea depth (m), GMRT", fontsize=fs["small"], labelpad=1,
                     color=pal["text"] if pal["dark"] else "k")
        cb.ax.tick_params(labelsize=fs["small"] - 1, length=2,
                          colors=pal["text"] if pal["dark"] else "k")
    dark = pal["dark"] or theme["main"] != "vector"
    halo = t.halo_dk if dark else t.halo
    ax.add_patch(Rectangle((beo[0], beo[2]), beo[1] - beo[0],
                           beo[3] - beo[2], transform=t.pc, fc="none",
                           ec="#d9a3e6" if dark else "#7a3f8f", lw=1.0,
                           ls=(0, (1, 1.5)), zorder=6))
    ax.scatter(plots.lon, plots.lat, transform=t.pc, s=6, zorder=8, lw=0,
               c=cfg["col"]["NEON"])
    if outlines:
        keep = A.key.isin(["c1_file", "brw", "e12", "tower"])
        shown = A[(~inside(A, cfg["c1_box"]) & ~inside(A, cfg["e12_box"]))
                  | keep]
    else:
        shown = A
    plot_assets(ax, shown, scale=0.8, edge="w" if dark else "k")
    for k, (text, dx, dy) in cfg["lab_main"].items():
        r = A[A.key == k].iloc[0]
        label(ax, r.lon, r.lat, text, dx, dy, dark=dark, fontsize=fs["label"])
    if outlines:
        oc = "w" if dark else "k"
        outline(ax, cfg["c1_box"], " b", color=oc, dark=dark)
        outline(ax, cfg["e12_box"], " c", va="top", color=oc, dark=dark)
    else:
        for k, (text, dx, dy) in (("c1_file", ("ARM C1 + NOAA BRW", 18, 26)),
                                  ("e12", ("ARM E12, NEON BARR,\nNGEE Arctic",
                                           18, -30))):
            r = A[A.key == k].iloc[0]
            label(ax, r.lon, r.lat, text, dx, dy, dark=dark,
                  fontsize=fs["label"], fontweight="bold")
    for lo, la, text in [(-156.835, 71.335, "Chukchi Sea"),
                         (-156.50, 71.355, "Elson Lagoon"),
                         (-156.765, 71.300, "Utqiaġvik"),
                         (-156.60, 71.397, "Barrow Canyon"),
                         (-156.47, 71.383, "Point Barrow (Nuvuk)"),
                         (-156.53, 71.262, "Barrow Environmental\n"
                                           "Observatory (BEO)")]:
        water = "Sea" in text or "Lagoon" in text
        col = ("w" if dark else pal["text"]) if not water else (
            "#bfe0f5" if dark else pal["sea_text"])
        ax.text(lo, la, text, transform=t.pc, ha="center", zorder=9,
                style="italic" if water else "normal", path_effects=halo,
                color=col)
    gl = ax.gridlines(t.pc, draw_labels=True, lw=0.3,
                      color="#bbbbbb" if dark else "#777", alpha=0.5,
                      xlocs=np.arange(-157, -156.2, 0.1),
                      ylocs=np.arange(71.20, 71.45, 0.05))
    gl.top_labels = gl.right_labels = False
    lab_col = pal["text"] if pal["dark"] else "k"
    gl.xlabel_style = gl.ylabel_style = dict(size=fs["small"], rotation=0,
                                             color=lab_col)
    scalebar(ax, 2000, "2 km", loc=(0.05, 0.035), color="w" if dark else "k")
    distance_triangle(ax, A, cfg["triangle"],
                      color="#ffffff" if dark else "#1a1a1a")
    return ax


def wide_inset(fig, rect, gpkg, pal=None, bg="plain"):
    """Northern-Alaska inset. bg="seaice_doc" fills the sea with the
    1991-2020 mean day of ice closing and adds 50/200/1000 m isobaths."""
    import numpy as np

    t, cfg = map_tools(), map_config()
    fs, pal = cfg["fs"], pal or palette("light")
    axi = fig.add_axes(rect, projection=t.ccrs.LambertConformal(
        central_longitude=-154.5, central_latitude=69,
        standard_parallels=(66, 71)))
    axi.set_extent(cfg["inset"], t.pc)
    axi.set_facecolor(pal["ocean"])
    if bg == "seaice_doc":
        xe, ye, doc, crs = seaice_doc_grid()
        lo, la = (np.array(v) for v in zip(*[t.pc.transform_point(
            x, y, crs) for y in ye[:-1] for x in xe[:-1]]))
        w, e, s, n = cfg["inset"]
        inside_ = ((lo >= w) & (lo <= e) & (la >= s) & (la <= n)).reshape(doc.shape)
        vmin, vmax = np.nanpercentile(doc[inside_], [2, 98])
        pm = axi.pcolormesh(xe, ye, doc, cmap="Spectral", vmin=vmin, vmax=vmax,
                            transform=crs, shading="flat", zorder=0.5)
        z, (bw, be, bs, bn) = gmrt_grid((-170, -138, 65.5, 73.5), "med")
        blon = np.linspace(bw, be, z.shape[1])
        blat = np.linspace(bn, bs, z.shape[0])
        cs = axi.contour(blon, blat, -z, levels=[50, 200, 1000],
                         colors="#3a3a3a", linewidths=0.45, transform=t.pc,
                         zorder=0.6)
        axi.clabel(cs, fmt="%d m", fontsize=6, inline=True)
        cax = axi.inset_axes([0.53, 0.20, 0.43, 0.035])
        cb = fig.colorbar(pm, cax=cax, orientation="horizontal")
        tk = np.arange(np.ceil(vmin / 15) * 15, vmax + 1, 15)
        cb.set_ticks(tk)
        cb.set_ticklabels([doy_label(v) for v in tk])
        cb.ax.tick_params(labelsize=fs["small"] - 1.5, length=2,
                          colors=pal["text"] if pal["dark"] else "k")
        cb.ax.set_title("Mean day of ice closing\n(SIC > 80%), 1991–2020",
                        fontsize=fs["small"] - 1, pad=2,
                        color=pal["text"] if pal["dark"] else "k")
    draw(axi, read_layer(gpkg, "alaska_land"), facecolor=pal["land"],
         edgecolor=pal["coast"], lw=0.5)
    draw(axi, read_layer(gpkg, "lakes_gt5km2"), facecolor=pal["water"],
         edgecolor="none")
    draw(axi, read_layer(gpkg, "north_slope_borough"), facecolor="none",
         edgecolor=pal["town"], lw=0.6, linestyle=(0, (4, 2)))
    arm = cfg["col"]["ARM"]
    for lo, la, text, dx, dy, mk in cfg["inset_sites"]:
        main = mk == "*"
        axi.scatter(lo, la, transform=t.pc, marker=mk, lw=1.1, zorder=11,
                    s=120 if main else 36, c=arm if main else "none",
                    edgecolors=("w" if pal["dark"] else "k") if main else arm)
        label(axi, lo, la, text, dx, dy, dark=pal["dark"],
              fontsize=fs["label"])
    for lo, la, text in [(-163.5, 70.6, "Chukchi\nSea"),
                         (-145.5, 70.75, "Beaufort Sea"),
                         (-157.0, 67.2, "North Slope\nBorough")]:
        water = "Sea" in text
        axi.text(lo, la, text, transform=t.pc, ha="center",
                 fontsize=fs["label"],
                 path_effects=t.halo_dk if pal["dark"] else t.halo,
                 style="italic" if water else "normal",
                 color=pal["sea_text"] if water else pal["text"])
    for sp in axi.spines.values():
        sp.set_edgecolor(pal["text"] if pal["dark"] else "k")
    return axi


def build_map_variant(layers_gpkg, inset_gpkg, theme="reference",
                      path="nsa_utqiagvik_asset_map.png", dpi=300):
    """Render one of map_themes(). With close-ups: main map + inset (a),
    C1/NOAA BRW (b), E12 with NEON and NGEE (c), E12 at 400 m (d). Without:
    a single larger main map, every asset drawn on it.

    Saves without bbox_inches='tight': a tight bbox is recomputed around the
    manually placed inset and crops the main map away.
    """
    import matplotlib.pyplot as plt

    th = map_themes()[theme] if isinstance(theme, str) else theme
    cfg = map_config()
    fs, pal = cfg["fs"], palette(th["palette"])
    A, plots = site_map_assets()
    plt.rcParams["savefig.bbox"] = None
    details = bool(th["details"])
    fig = plt.figure(figsize=(15.5, 12.8) if details else (11.0, 12.6),
                     facecolor="#15191d" if pal["dark"] else "white")
    tcol = pal["text"] if pal["dark"] else "k"
    if details:
        rect, irect, lx, ncol = ([0.045, 0.20, 0.60, 0.76],
                                 [0.052, 0.715, 0.235, 0.245], 0.045, 4)
    else:
        rect, irect, lx, ncol = ([0.07, 0.215, 0.90, 0.75],
                                 [0.08, 0.72, 0.33, 0.24], 0.07, 3)
    ax = main_map(fig, rect, A, plots, layers_gpkg, th, outlines=details)
    wide_inset(fig, irect, inset_gpkg, pal, bg=th.get("inset", "plain"))
    leg = fig.legend(handles=legend_handles(pal["dark"]), loc="upper left",
                     ncol=ncol,
                     bbox_to_anchor=(lx, 0.165 if details else 0.19),
                     frameon=False,
                     fontsize=fs["label"], labelspacing=0.6,
                     handlelength=1.6, handletextpad=0.6, columnspacing=1.6,
                     alignment="left", title_fontsize=fs["label"],
                     title="Colour = operator · shape = asset type")
    for txt in leg.get_texts() + [leg.get_title()]:
        txt.set_color(tcol)
    src = ("Basemap: © OpenStreetMap contributors (ODbL); US Census "
           "TIGER/Line 2024 and CB 2024.")
    if th["main"] != "vector" or (details and th.get("detail") != "vector"):
        src += "\nImagery: Esri World Imagery, Vantor WorldView-3, 7 Sep 2025."
    if th.get("inset") == "seaice_doc":
        src += ("\nInset sea ice: 1991–2020 mean day of closing from the NOAA/NSIDC CDR v6"
                " (G02202, doi:10.7265/b18j-z797), 25 km.")
    if th.get("bathy"):
        src += ("\nBathymetry: GMRT v4.5.0 (Ryan et al. 2009, doi:10.1029/2008GC002332).")
    src += ("\nARM instruments only (no VAPs or retrievals); positions from the most recent"
            " a-level file, or b-level where the a-level holds none.")
    fig.text(lx, 0.006 if details else 0.004, src, fontsize=fs["small"],
             linespacing=1.4, va="bottom",
             color="#bbbbbb" if pal["dark"] else "#444")
    fig.text(lx + 0.002, 0.972, "a", fontsize=fs["letter"],
             fontweight="bold", color=tcol)
    fig.text(lx + 0.025, 0.972, "ARM North Slope of Alaska observatory and "
             "neighbouring research assets, Utqiaġvik",
             fontsize=fs["title"], color=tcol)
    if details:
        bg = th.get("detail", "imagery")
        axb, dk = detail_panel(fig, [0.665, 0.625, 0.325, 0.33], A, plots,
                               cfg["c1_box"], 17, cfg["lab_c1"], "b",
                               "Main site: ARM C1/E30 and NOAA GML BRW", bg,
                               layers_gpkg, pal)
        towers = read_layer(layers_gpkg, "detail_c1_towers_masts")
        draw(axb, towers, facecolor="none", edgecolor="#ffd84d", lw=1.2,
             zorder=9)
        if len(towers):
            t0 = towers.to_crs(3857).centroid.to_crs(4326).iloc[0]
            label(axb, t0.x, t0.y, "Towers (OSM)", 0.58, 0.95, ha="left",
                  frac=True, dark=dk, fontsize=fs["label"])
        scalebar(axb, 200, "200 m", loc=(0.06, 0.05),
                 color="w" if dk else "k")
        connect(fig, ax, cfg["c1_box"], axb)
        axc, dk = detail_panel(fig, [0.665, 0.335, 0.325, 0.25], A, plots,
                               cfg["e12_box"], 16, cfg["lab_e12"], "c",
                               "ARM E12 on the BEO, with NEON BARR and NGEE "
                               "Arctic", bg, layers_gpkg, pal)
        rd = read_layer(layers_gpkg, "roads_osm", cfg["e12_box"])
        line_label(axc, rd[rd.name == "Eastfield Road"], cfg["e12_box"],
                   "Cake Eater Rd\n(OSM: Eastfield Rd)", frac=0.55, rot=82)
        scalebar(axc, 500, "500 m", loc=(0.06, 0.05),
                 color="w" if dk else "k")
        connect(fig, ax, cfg["e12_box"], axc)
        e = A[A.key == "e12"].iloc[0]
        zb = box_around(e.lat, e.lon, cfg["e12_half_m"])
        outline(axc, zb, " d", color="w" if dk else "k", dark=dk)
        axd, dk = detail_panel(fig, [0.665, 0.035, 0.325, 0.26], A, plots,
                               zb, 18, cfg["lab_e12_zoom"], "d",
                               "E12 close-up (400 m)", bg, layers_gpkg, pal)
        rz = read_layer(layers_gpkg, "roads_osm", zb)
        foot = rz[rz.highway == "footway"]
        draw(axd, foot, facecolor="none", edgecolor="#ffd84d", lw=1.0,
             zorder=9)
        line_label(axd, foot, zb, "footway\n(OSM)", frac=0.2)
        hut = read_layer(layers_gpkg, "detail_e12_buildings", zb)
        draw(axd, hut, facecolor="none", edgecolor="#ffd84d", lw=1.2,
             zorder=9)
        if len(hut):
            h0 = hut.to_crs(3857).centroid.to_crs(4326).iloc[0]
            label(axd, h0.x, h0.y, "Building (OSM)", 0.62, 0.62, ha="left",
                  frac=True, dark=dk, fontsize=fs["label"])
        line_label(axd, rz[rz.name == "Eastfield Road"], zb, "Cake Eater Rd",
                   frac=0.3, rot=72)
        scalebar(axd, 50, "50 m", loc=(0.06, 0.05), color="w" if dk else "k")
        connect(fig, axc, zb, axd, below=True)
    fig.savefig(path, dpi=dpi, facecolor=fig.get_facecolor())
    return fig


def build_site_map(layers_gpkg, inset_gpkg, path="nsa_utqiagvik_asset_map.png",
                   dpi=300):
    """The reference variant (vector main map, imagery close-ups)."""
    return build_map_variant(layers_gpkg, inset_gpkg, "reference", path, dpi)
