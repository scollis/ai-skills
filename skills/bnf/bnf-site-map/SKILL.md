---
name: bnf-site-map
description: "Build maps of the ARM Bankhead National Forest (BNF, AMF3) observatory in northern Alabama - fetch places, counties, roads, water, airports (Census TIGER/CB 2024, OpenStreetMap via osmnx), the Bankhead National Forest, Sipsey Wilderness and Sipsey Fork Wild and Scenic River (USFS EDW ArcGIS REST), Esri World Hillshade and World Imagery, and render a nine-panel map - network main map in local Transverse Mercator with a southeast-US inset, geodesic S3 (C-SAPR2) to M1 and S4 (SACR) to M1 distance lines, and eight close-ups (M1 and tower, tower complex, S3, S4, S20, S30, S40, U2). ARM markers are instrument file positions from arm-bnf-site; non-ARM assets come from bnf-research-assets, with far radars, sondes and NEON sites in the inset. Records the cartopy PlateCarree latitude trap under PROJ 9.8 (about 21 km at 34 N). Use for any BNF site map, BNF close-up, or a southeastern-US map mixing XYZ tiles or pyproj coordinates with cartopy."
---

# Site maps for ARM BNF

`kernel.py` renders one figure from one asset table: a main map of the whole BNF network (about
79 x 69 km, local Transverse Mercator) with a southeast-US inset top-left (**a**) and eight
close-ups (**b**-**i**) in two columns on the right. The main map carries geodesic distance lines from the C-SAPR2
(S3) and SACR (S4) sites to M1, a 10 km scale bar and a true-north arrow. Each close-up has its
own scale bar and an Esri imagery credit (source, date, resolution) read live at render time.

Assets are frozen in `site_map_assets.csv` (66 mapped assets: 24 ARM file positions and 42 non-ARM) by `build_asset_table()`, which
reads `arm-bnf-site/bnf_instrument_positions.csv` (ARM instrument file positions) and
`bnf-research-assets/bnf_region_assets.csv` (non-ARM assets). Rerun it whenever either sibling CSV
changes; `tests/test_structure_bnf_map.py` fails while the frozen table is stale. The `layer` column
says where a row is drawn: `main` (main map and close-ups), `detail` (close-ups only: within 100 m
of a larger ARM cluster, such as the M1 AERI, CSPHOT and DL, or inside a close-up box, such as
IMPROVE SIPS1, RAWS BHFA1, SCAN 2179 and AWOS 1M4) and `inset` (outside the main map: WSR-88D,
TDWR, ARMOR, radiosonde sites, NWS HUN and NEON). Census context rows (places and counties come
from TIGER instead), polygon rows, reservoirs, dams, NASA MSFC and the four DOE AmeriFlux rows
(registrations of ARM towers already drawn) are skipped.

`bnf_locations_page.csv` holds the 13 facilities parsed from the `const locations` JSON on arm.gov
(2026-10-20). It names the facilities and serves as a hollow-marker fallback when the positions
CSV is absent; it is not drawn otherwise.

| facility | role | lat | lon |
|---|---|---|---|
| M1 | main site | 34.342481 | -87.338177 |
| S1 | collocated main | 34.342481 | -87.338177 |
| S2 | collocated main | 34.342481 | -87.338177 |
| S3 | C-SAPR2 | 34.630806 | -87.133118 |
| S4 | SACR | 34.464279 | -87.236001 |
| S10 | tower | 34.3437276 | -87.35044401 |
| S11 | collocated tower | 0.0 | 0.0 |
| S13 | STAMP2 | 34.344015 | -87.35062209 |
| S14 | STAMP3 | 34.343399 | -87.350858 |
| S20 | Courtland | 34.653784 | -87.292676 |
| S30 | Falkville | 34.384829 | -86.927905 |
| S40 | Double Springs | 34.178796 | -87.453905 |
| U2 | AAF ArcticShark UAS | 34.280111 | -87.597858 |

S1 and S2 share the M1 page coordinate. S11 (collocated tower) is 0, 0 on the page.

## Credit

Map data © OpenStreetMap contributors (ODbL 1.0). US Census Bureau TIGER/Line and Cartographic
Boundary files 2024 (public domain). USDA Forest Service Enterprise Data Warehouse (Bankhead Ranger
District, National Wilderness Areas, Wild and Scenic River segments). Esri World Hillshade and World
Imagery (Esri, Vantor, Earthstar Geographics). ARM facility and instrument positions, with their
datastream DOIs and mentor credit, are documented in `arm-bnf-site`.

## Environment and network

A `geo` environment with geopandas, shapely, pyogrio, cartopy, pyproj, scipy, osmnx, matplotlib
and pillow. Reachable on 2026-10-20: `www2.census.gov`, `apps.fs.usda.gov`, `server.arcgisonline.com`
(imagery and hillshade tiles, identify), `www.arm.gov` and `overpass-api.de` (osmnx user agent only;
plain requests get HTTP 406). On 2026-10-20 Overpass answered HTTP 502, then proxy "tunnel
connection failed: 502", for most of two hours; the main pull and two close-up pulls succeeded.
`fetch_osm()` backs off, pickles each pull under `layer_cache/`, returns an empty frame for a box
with no features, and `zoom_layers()` skips a close-up whose pull fails. Blocked: `elevation.nationalmap.gov` (USGS 3DEP), so relief comes from Esri
World Hillshade.

## Recipe

```python
import os

import matplotlib.pyplot as plt

# kernel helpers from this skill
build_asset_table(out=os.path.join(skill_dir(), "site_map_assets.csv"))
write_layers(zoom_layers(), "bnf_layers.gpkg")       # TIGER, CB, USFS, OSM
write_layers(inset_layers(), "se_us_inset_layers.gpkg")
fig, ax = build_map_variant("bnf_layers.gpkg", "se_us_inset_layers.gpkg",
                            "reference", path="bnf_site_map.png", dpi=300)
plt.close(fig)
```

| variant | main map | close-ups |
|---|---|---|
| reference | vector over Esri World Hillshade | Esri World Imagery |
| imagery | Esri World Imagery | Esri World Imagery |
| vector | vector over Esri World Hillshade | OSM vector |

`map_config()` holds every box, close-up size and zoom, label offset, colour, font size and the
distance legs; edit it, not the drawing code. Close-up labels are placed automatically in two
columns (points west of the panel centre to the left column), so a new asset needs no layout
entry; `lab_detail` pins fixed slots where a cluster needs them (panel b, and AWOS 1M4 in i). A
leader always starts at the text edge nearest its point. A close-up nested inside another (c
inside b) is outlined there and its assets are labelled only in its own panel.

On the main map, markers and asset labels are drawn first. Town names then try up to nine
offsets until their text box clears every marker and label (`keep_label()`). Shields are placed
last, sliding along their road, and any label whose box leaves the axes or falls under the inset
is dropped. On 2026-10-20 this dropped 6 places (Hillsboro, Leighton, Littleville, North
Courtland, Town Creek, Tuscumbia; under the inset, at the edge or blocked by an asset label) and
10 shields (among them I-565, which cannot clear Mooresville).

## Layers and what they hold

| layer | source | features | note |
|---|---|---|---|
| places | TIGER 2024 PLACE 01 | 38 | incorporated places (CLASSFP C*) filled and labelled; CDPs not drawn |
| counties | CB 2024 500k county | 9 | Alabama only |
| water_tiger | TIGER 2024 AREAWATER, 10 counties | 6402 | Wheeler Lake / Tennessee River, Lewis Smith Lake and ponds |
| roads_tiger | TIGER 2024 PRISECROADS 01 | 540 | source of the US, state and interstate shields (`route_shield()`) |
| roads_osm | OSM highway motorway to tertiary | 3851 | drawn by class |
| rivers_osm | OSM waterway river, canal | 224 | Sipsey Fork, Flint Creek, Brushy Creek labelled |
| airports, runways | OSM aeroway | 12, 14 | |
| forest_district | USFS EDW_RangerDistricts_01 | 1 | Bankhead Ranger District (administrative boundary, includes inholdings) |
| wilderness | USFS EDW_Wilderness_01 | 1 | Sipsey Wilderness |
| wild_scenic_river | USFS EDW_WildScenicRiverSegments_01 | 1 | Sipsey Fork |
| detail_b_*, detail_d_* | OSM, all tags in the close-up box | 4 roads + 1 man_made; 1 road | c and e-i not fetched (Overpass unreachable, 2026-10-20) |
| states, ocean, cities | CB 2024 500k state, TIGER PLACE | 15, 1, 2 | inset; ocean is the box minus US land, so the Gulf coast comes from the state outlines |

## Traps that cost a wrong figure

1. **`ccrs.PlateCarree()` is not plain lon/lat with PROJ 9.8.** Under cartopy 0.25.0, pyproj 3.7.2 and
   PROJ 9.8.1 it is ellipsoidal `eqc`, which is not linear in latitude. Measured into the main-map
   Transverse Mercator on 2026-10-20, the y error was 21.34 km at M1. Layers that all go through
   PlateCarree stay mutually consistent, which hides it, but tiles, pyproj output and radar gate
   x/y do not. `lonlat_crs()` (PlateCarree on a sphere) and `ccrs.Geodetic()` agree with pyproj
   to under 1 cm; every helper here uses `lonlat_crs()`.
2. **`GeoDataFrame.plot(ax=geoaxes)` resets the aspect** to 1/cos(lat). Use `draw()`.
3. **`bbox_inches="tight"` crops `fig.add_axes` layouts.** figure-style sets it; the builder resets
   `savefig.bbox` to None.
4. **osmnx raises on an empty box.** `features_from_bbox` throws `InsufficientResponseError` for a
   box with no matching features (the 150 m tower close-up). Treating that as a server error retried
   with backoff and lost the earlier pulls; `fetch_osm()` now returns an empty frame and caches.
5. **Vertically pointing radars are not scanning radars.** M1 holds KAZR; `radar_classes` lists
   scanning radars only, so M1 stays a star.
6. **osmnx waits on `/api/status`.** With its rate limiter on, osmnx polls the Overpass status
   endpoint between requests and sat there for 14 minutes on a 150 m box; `fetch_osm()` sets
   `ox.settings.overpass_rate_limit = False` and a 90 s timeout and does its own backoff.
7. **Relative `co_filename`.** When `kernel.py` is compiled with a relative path, the skill directory
   resolves to "" and the sibling CSVs are silently missed; `skill_dir()` takes `abspath`.

## Encoding

Colour gives the operator (Okabe-Ito: ARM blue, NOAA orange, NSF NEON green, other reddish
purple). Shape gives the asset type: star for the main facility, square for an extended or
supplemental facility (a file position shared by more than 3 instruments), triangle for a scanning
radar, circle for a single instrument or station, diamond for a sounding launch first fix or
radiosonde site. **Hollow means a rounded or nominal position**: the M1 sonde launch (stored to
0.01°) and non-ARM rows whose recorded precision is 2-3 decimals, about 1 km, a Nominatim point or
a geocode (PSL Courtland, NWS HUN, USFS office, TDWR).

## Distances drawn

Geodesic (WGS84) between ARM file positions (`leg_table()`; the test recomputes them from
`bnf_instrument_positions.csv`):

| leg | distance | bearing |
|---|---|---|
| S3 C-SAPR2 → M1 | 37.12 km | 211° |
| S4 SACR → M1 | 16.46 km | 215° |

## Known gaps

1. OSM detail layers for close-ups c and e-i were not fetched: overpass-api.de returned HTTP 502
   and then proxy tunnel failures for most of 2026-10-20. The reference and imagery variants do not
   use them; the vector variant draws those close-ups with no OSM line work until
   `zoom_layers()` is rerun (cached pulls are reused).
2. Relief is Esri World Hillshade, not USGS 3DEP (`elevation.nationalmap.gov` blocked; access was
   not requested because the hillshade sufficed).
3. The forest polygon is the Bankhead Ranger District (administrative), not National Forest System
   land ownership; inholdings are included. EDW_ForestSystemBoundaries_01 holds the latter and was
   not used.
4. A locally cached BNF KMZ (36 polygons: an airshed and M1 building outlines, provenance
   unrecorded) is not drawn; `kmz_polygons(path)` reads such a file for offline use.
5. The imagery variant's legend still lists the vector fills (places, water) that it does not draw.
6. Non-ARM markers inherit the coordinate precision recorded by `bnf-research-assets`; the PSL
   Courtland profiler (2 dp, about 1 km) and the TDWR sites (3 dp) are hollow.
7. Esri imagery dates differ by panel (2022-11-30 to 2025-10-12 on 2026-10-20). The S3
   (2023-04-30), S4 and S20 (2022-11-30) tiles predate the 2024-10-01 start, so they cannot show the
   AMF3 installations.

## Verified against

2026-10-20: locations page and imagery metadata from arm.gov and server.arcgisonline.com, layers
fetched from Census, USFS EDW and Overpass, and all variants rendered from `kernel.py`.
`tests/test_structure_bnf_map.py` checks the facility and distance tables, the asset counts,
config keys against the asset table, ARM rows against the positions CSV, cluster collapsing, the
close-up layout, asset-table regeneration, the tile arithmetic, route shields and (with cartopy) the
PlateCarree trap at M1. Plotted marker offsets were compared with pyproj in display space: 0.0000 m
for m1, s3_csapr2, s4_sacr, u2_takeoff and 9a4, against 21.3-21.5 km for a naive PlateCarree.
