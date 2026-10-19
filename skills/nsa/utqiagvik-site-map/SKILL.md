---
name: utqiagvik-site-map
description: "Build maps of the ARM North Slope of Alaska (NSA) site and Utqiagvik (Barrow) - fetch town, coast, water, roads, buildings and airport layers from OpenStreetMap (Overpass via osmnx) and Census TIGER/CB 2024, Esri World Imagery tiles for site close-ups, and a four-panel publication map with a northern-Alaska inset, C1/NOAA BRW and E12 imagery close-ups and a C1-E12-X-SAPR distance triangle. Records the cartopy Web-Mercator datum trap (about 23 km at 71 N), the GeoDataFrame.plot aspect trap, and the tight-bbox inset crop. Use for any NSA, Utqiagvik or other high-latitude site map, especially one mixing XYZ imagery tiles with vector data in cartopy."
---

# Site maps for ARM NSA and Utqiagvik

This skill builds a four-panel map, with the builder in `kernel.py`. Panel **a** is the main map
(about 18 x 18 km, in a local Transverse Mercator), with a northern-Alaska inset top-left and
geodesic distance lines from C1 to E12 and to the X-band radar. Panel **b** is an imagery close-up
of the C1 / NOAA BRW complex, **c** is E12 with NEON BARR and NGEE Arctic, and **d** is E12 at
400 m. The assets come from `arm-nsa-site` and `utqiagvik-research-assets`, frozen into
`site_map_assets.csv` (38 mapped assets) and `neon_barr_plot_centres.csv` (93 plot centres).

## Credit

Map data © OpenStreetMap contributors (ODbL 1.0). US Census Bureau TIGER/Line and Cartographic
Boundary files 2024 (public domain). Imagery: Esri World Imagery, source Vantor WorldView-3,
7 Sep 2025, 0.31 m, stated accuracy 8.47 m, read with `imagery_metadata()` at E12 on
2026-10-19. Asset coordinates are credited in the two companion skills.

## Environment and network

Make a `geo` environment with geopandas, shapely, pyogrio, cartopy, pyproj, osmnx, matplotlib and
pillow. Hosts that must be reachable: `overpass-api.de` (OSM), `www2.census.gov` (TIGER/CB,
allowlisted), and `server.arcgisonline.com` (imagery). Request allowlist access for the first and
last. Hosts that were blocked here as of 2026-10-19: naciscdn.org (Natural Earth),
osmdata.openstreetmap.de (OSM land polygons) and basemap.nationalmap.gov (USGS imagery).

## Recipe

```python
import matplotlib.pyplot as plt

# kernel helpers from this skill
write_layers(zoom_layers(), "utqiagvik_layers.gpkg")       # OSM + TIGER, ~2 min
write_layers(inset_layers(), "alaska_inset_layers.gpkg")   # CB 500k + lakes
fig = build_site_map("utqiagvik_layers.gpkg", "alaska_inset_layers.gpkg",
                     path="nsa_utqiagvik_asset_map.png", dpi=300)
plt.close(fig)
```

`map_config()` holds every box, colour, font size, label position and the triangle legs. Edit
that dict, not the drawing code. The Overpass pull retries with exponential backoff because the
public server is often at capacity.

## Layers and what they hold

| layer | source | note |
|---|---|---|
| coastline, land | OSM natural=coastline | land is polygonized from the coastline ways (land lies left of the way direction); islands are closed rings |
| water_osm, waterways_osm | OSM | generic water polygons (ponds, lagoons, rivers), not lakes only |
| water_tiger | TIGER 2024 AREAWATER 02185 | includes sea and lagoon polygons; filter MTFCC == "H2030" for lakes |
| town_boundary | TIGER 2024 PLACE | select GEOID 0281920; the NAME carries a diacritic (Utqiaġvik) |
| buildings, roads_osm, airport | OSM | about 2,000 buildings in the zoom box; roads keyed by highway= |
| roads_tiger | TIGER 2024 ROADS 02185 | coarser than OSM, kept for cross-checking |
| detail_c1_*, detail_e12_* | OSM | close-up subsets; E12 has one building, Eastfield Road and a footway, and no pad, mast or fence |
| alaska_land, north_slope_borough, lakes_gt5km2 | CB 2024 500k, TIGER | inset; the ocean polygon east of 141 W uses a hand-drawn Yukon mask, so frame the inset at or west of 141.5 W |

OSM calls the E12 access road "Eastfield Road"; Sturm et al. (2025) call it Cake Eater Road.
Label it with both. The Barrow Environmental Observatory polygon is in neither OSM nor any
public service that answered (see `utqiagvik-research-assets`), so the map draws the BAID
bounding box and says so in the legend.

## Traps that cost a wrong figure

1. **cartopy's Web Mercator is not EPSG:3857 for PlateCarree input.** With cartopy 0.25 and
   pyproj 3.7.2, `ccrs.GOOGLE_MERCATOR` and `ccrs.epsg(3857)` convert PlateCarree (WGS84)
   points to the Web-Mercator sphere with a datum shift. Measured against pyproj EPSG:4326 to
   3857 on 2026-10-19, the y-offset was 0 at the equator and 22.6, 34.7, 50.3 and 72.2 km of
   Mercator y at 30, 45, 60 and 71.32 N. On the ground that is about 20-25 km, so XYZ tiles
   drawn in such an axes are misregistered against every vector layer. `tiles_in()` is the fix:
   it takes the mosaic corners through pyproj to lon/lat, then into an ellipsoidal local TM,
   and the tiles are drawn with `transform=` set to that TM so nothing is regridded. Check the
   registration by overlaying OSM roads; on these panels they fall on the imaged roads.
2. **`GeoDataFrame.plot(ax=geoaxes)` resets the aspect** to 1/cos(lat), about 3 at 71 N, and
   squashes the panel. Use `ax.add_geometries` (the `draw()` helper).
3. **`bbox_inches="tight"` crops away the main map** when an inset is placed with
   `fig.add_axes`. The figure-style skill sets it by default, so `build_site_map` resets
   `savefig.bbox` to None.
4. **A bbox read returns whole geometries.** A road label placed at a fraction along a
   `read_layer(..., box)` result can land outside the panel, so `line_label()` clips first.
5. **Imagery zoom.** Zoom 19 returns "Map data not yet available" tiles at NSA; use 17 for
   about 1 km panels and 18 for 400 m. In this session a cartopy `GoogleTiles` subclass
   pointed at the same URL drew placeholder tiles, so the mosaic is fetched directly with
   `imagery_mosaic()`.
6. **Labels on dense clusters.** At C1, 13 mapped assets sit within 400 m of the facility point. Offset-point labels
   collided. Labels placed in columns at fixed axes-fraction positions, with each leader
   anchored at the text edge nearest the point, do not cross.

## Encoding

Colour gives the operator (Okabe-Ito: ARM blue, NOAA orange, NEON green, other research reddish
purple, historic grey). Shape gives the asset type: star for a main facility or observatory,
square for an extended facility or building, triangle for a scanning radar, circle for a station,
diamond for a sounding launch. A **hollow marker means a nominal or rounded coordinate** (the C1
facility point, the 26-file C1 nominal, SEBS at 3 decimals, sondes at 0.01 degrees, BSRN, E11,
NARL, DEW Line, the sea-ice mass-balance site). Filled markers are instrument-specific or
surveyed positions.

## Distances drawn

Geodesic (WGS84) from the C1 locations-page coordinate. They match `nsa_distance()` in
`arm-nsa-site`:

| leg | distance | bearing |
|---|---|---|
| C1 → E12 | 5.47 km | 190° |
| C1 → X-SAPR | 1.90 km | 276° |
| E12 → X-SAPR | 5.66 km | 350° |

## Verified against

2026-10-19: layers fetched (Overpass OSM base 2026-10-19T16:02:45Z, TIGER/CB 2024), imagery
tiles and metadata from server.arcgisonline.com, and the figure rendered from `kernel.py` matching
the reviewed figure pixel for pixel. `tests/test_structure_nsa.py` checks the tile arithmetic, the
config boxes against the mapped assets, the triangle table against `site_map_assets.csv`, and
(with cartopy installed) that `tiles_in` agrees with pyproj while cartopy's EPSG:3857 does not.
