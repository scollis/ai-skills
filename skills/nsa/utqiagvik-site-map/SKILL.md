---
name: utqiagvik-site-map
description: "Build maps of the ARM North Slope of Alaska (NSA) site and Utqiagvik (Barrow) - fetch town, coast, water, roads, buildings and airport layers from OpenStreetMap (Overpass via osmnx) and Census TIGER/CB 2024, Esri World Imagery for close-ups and backgrounds, and render five map variants (overview or four-panel with C1/NOAA BRW and E12 close-ups, on vector, colour imagery, grey imagery or a dark theme) with a northern-Alaska inset shaded by the 1991-2020 mean day of sea-ice closing, GMRT bathymetry and isobaths on the main map (Barrow Canyon), and a C1-E12-X-SAPR distance triangle. ARM markers are instruments only, positioned from the most recent a-level file. Records the cartopy PlateCarree latitude trap under PROJ 9.8 (about 23 km at 71 N) and the GeoDataFrame.plot aspect trap. Use for any NSA, Utqiagvik or high-latitude site map, especially one mixing XYZ tiles or pyproj coordinates with cartopy."
---

# Site maps for ARM NSA and Utqiagvik

`kernel.py` renders five map variants from one table of assets. Each has a main map (about 18 x 18
km, local Transverse Mercator) with a northern-Alaska inset top-left and geodesic distance lines from
C1 to E12 and to the X-band radar. Some variants also carry close-ups: **b**, the C1 / NOAA BRW complex;
**c**, E12 with NEON BARR and NGEE Arctic; **d**, E12 at 400 m. The assets come from `arm-nsa-site`
and `utqiagvik-research-assets`, frozen into `site_map_assets.csv` (37 assets) and
`neon_barr_plot_centres.csv` (93 plot centres).

ARM markers are instruments only (no VAPs or retrievals), one per distinct file position from the
`arm-nsa-site` instrument audit (most recent a-level file, b-level where a-level is unserved or holds no
better position; 2026-10-19), labelled with the instruments there. **E10 is not drawn
as a site.** It is a catch-all code for instruments that are not co-located, so its SEBS/LPM and ECOR
appear at their own positions.

## Credit

Map data © OpenStreetMap contributors (ODbL 1.0). US Census Bureau TIGER/Line and Cartographic
Boundary files 2024 (public domain). Imagery: Esri World Imagery, source Vantor WorldView-3,
7 Sep 2025, 0.31 m, stated accuracy 8.47 m (`imagery_metadata()` at E12, 2026-10-19). Asset
coordinates are credited in the two companion skills.

## Environment and network

Make a `geo` environment with geopandas, shapely, pyogrio, cartopy, pyproj, scipy, osmnx, matplotlib
and pillow. Hosts: `overpass-api.de` (OSM) and `server.arcgisonline.com` (imagery) need allowlist
grants, and `www2.census.gov` was already allowlisted. Blocked as of 2026-10-19: naciscdn.org (Natural Earth), osmdata.openstreetmap.de (OSM
land polygons) and basemap.nationalmap.gov (USGS imagery). Esri's Light Gray, Dark Gray, Street and
Topo canvases are nearly empty this far north (faint roads only), and Shaded Relief has no tiles,
so the variants draw land and water from the OSM layers instead.

## Recipe

```python
import matplotlib.pyplot as plt

# kernel helpers from this skill
write_layers(zoom_layers(), "utqiagvik_layers.gpkg")       # OSM + TIGER, ~2 min
write_layers(inset_layers(), "alaska_inset_layers.gpkg")   # CB 500k + lakes
for name in map_themes():
    fig = build_map_variant("utqiagvik_layers.gpkg", "alaska_inset_layers.gpkg",
                            name, path=f"nsa_map_{name}.png", dpi=300)
    plt.close(fig)
```

| variant | main map | close-ups |
|---|---|---|
| overview_vector | light OSM/TIGER vector | none; every asset on the main map |
| overview_imagery | colour imagery (zoom 13) with white line work | none |
| reference | light vector | b–d on colour imagery |
| grey_imagery | desaturated imagery | b–d on desaturated imagery |
| dark_vector | dark vector theme | b–d on dark vector (OSM buildings, roads) |

`build_site_map()` is the reference variant. `map_config()` holds every box, colour, font size,
label position and the triangle legs, and `map_themes()` holds the variants; edit those, not the
drawing code. Imagery backgrounds are resampled per pixel by `warp_mosaic()` (target projection to
lon/lat to EPSG:3857 to bilinear sample), which is exact at any panel size.

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
Label it with both. The Barrow Environmental Observatory polygon is in neither OSM nor any public
service that answered (see `utqiagvik-research-assets`), so the map draws the BAID bounding box.

## Backgrounds: sea-ice closing date and bathymetry

Every theme now carries two sea backgrounds (switch off per theme with `inset="plain"`, `bathy=False`):

- **Inset: 1991-2020 mean day of ice closing** (`seaice_doc_grid()`, shipped `seaice_doc_1991_2020.csv`,
  25 km, 4027 cells). Day of closing = first day the 5-day running mean of sea-ice
  concentration exceeds 80% after the final summer minimum, per ice year 1 Mar to end Feb - the DOC
  definition of NSIDC-0747 (Steele et al. 2019, doi:10.5067/KINANQKEZI4T; Peng et al. 2018,
  doi:10.3390/rs10091328), with the 5-day smoothing of Stroeve et al. 2016 - computed from the NOAA/NSIDC CDR v6 (G02202, doi:10.7265/b18j-z797,
  public at `noaadata.apps.nsidc.org/NOAA/G02202_V6/north/aggregate/`). Spectral, limits fitted to the
  2-98th percentile of cells inside the inset; 50/200/1000 m GMRT isobaths over it. At the ocean cell
  nearest C1 (14 km offshore) the mean is 8 Nov and the 1979-2025 trend is +11.7 days/decade.
  The official NSIDC-0747 sits behind Earthdata Login on `daacdata.apps.nsidc.org`, which takes a
  username and password through URS (an EDL bearer token is refused with "HTTP Basic: Access denied").
- **Main map: GMRT v4.5.0 bathymetry** (`gmrt_grid()`, `draw_bathymetry()`; Ryan et al. 2009,
  doi:10.1029/2008GC002332) from the GMRT GridServer as Esri ASCII (`www.gmrt.org` must be allowlisted).
  Filled on vector themes, isobaths (10/20/50/100 m) only over imagery. The head of Barrow Canyon reaches
  about 120 m in the box.

Two coastline traps, both visible as artefacts until fixed:

- **TIGER area water includes coastal sea** out to a straight offshore limit. Drawn over bathymetry it
  paints a pale wedge with a ruler-straight edge that looks like a canyon wall. `base_layers(...,
  marine=False)` keeps only water polygons inside the land layer (5 of 29 dropped here, incl. 130, 110
  and 59 km2 sea polygons).
- **GMRT's coastline is coarser than OSM's**, so sea-side cells at or above 0 m show as a blocky white
  band. `draw_bathymetry` fills non-sea cells from the nearest sea cell and Gaussian-smooths (3 cells)
  before shading and contouring; land polygons on top mask true land. Colour limits use true sea depths.

## Traps that cost a wrong figure

1. **`ccrs.PlateCarree()` is not plain lon/lat with PROJ 9.8.** With cartopy 0.25.0, pyproj 3.7.2
   and PROJ 9.8.1, PlateCarree is `eqc` on the WGS84 ellipsoid scaled by `+to_meter`. Ellipsoidal
   `eqc` is no longer linear in latitude, so lon/lat passed with `transform=ccrs.PlateCarree()`
   land off in any ellipsoidal projection. Measured into a Transverse Mercator on 2026-10-19, the
   y error was 0 m at the equator, 24.4 km at 45 N and
   23.1 km at 71.32 N. Layers that all go through PlateCarree stay mutually
   consistent, which hides the error. Anything placed in true projected coordinates does not:
   XYZ tiles in EPSG:3857, pyproj output, or radar gate x/y. `ccrs.Geodetic()` and a PlateCarree
   on a sphere globe agree with pyproj to 0.0 m, and `lonlat_crs()` returns the latter. An earlier
   version of this skill blamed `ccrs.GOOGLE_MERCATOR`; that was wrong, because Geodetic input
   into GOOGLE_MERCATOR matches pyproj exactly.
2. **`GeoDataFrame.plot(ax=geoaxes)` resets the aspect** to 1/cos(lat), about 3 at 71 N, and
   squashes the panel. Use `ax.add_geometries` (the `draw()` helper).
3. **`bbox_inches="tight"` crops away the main map** when an inset is placed with
   `fig.add_axes`. The figure-style skill sets it by default, so the builders reset
   `savefig.bbox` to None.
4. **A bbox read returns whole geometries.** A road label placed at a fraction along a
   `read_layer(..., box)` result can land outside the panel, so `line_label()` clips first.
5. **Imagery zoom.** Zoom 19 returns "Map data not yet available" tiles at NSA. Use 13 for the
   18 km main map, 16-17 for 1-2 km panels and 18 for 400 m. A cartopy `GoogleTiles` subclass
   pointed at the same URL drew placeholder tiles in this session, so `imagery_mosaic()` fetches
   tiles directly.
6. **Labels on dense clusters.** At C1, 13 mapped assets sit within 400 m of the facility point.
   Offset-point labels collided. Labels placed in columns at fixed axes-fraction positions, with each
   leader anchored at the text edge nearest the point, do not cross.

## Encoding

Colour gives the operator (Okabe-Ito: ARM blue, NOAA orange, NEON green, other research reddish
purple). Shape gives the asset type: star for a main facility or observatory,
square for an extended facility or building, triangle for a scanning radar, circle for a station,
diamond for a sounding launch. A **hollow marker means a nominal or rounded coordinate**: the C1
page point, the C1 nominal shared by 39 instruments, SEBS/LPM at 3 decimals, sondes at 0.01 degrees,
the ISS sonde (1998–2002), BSRN, E11 and the sea-ice mass-balance site. Historic and context places (NARL,
the DEW Line) are not drawn. Filled markers are
instrument-specific or surveyed positions.

## Distances drawn

Geodesic (WGS84) from the C1 locations-page coordinate. They match `nsa_distance()` in
`arm-nsa-site`:

| leg | distance | bearing |
|---|---|---|
| C1 → E12 | 5.47 km | 190° |
| C1 → X-SAPR | 1.90 km | 276° |
| E12 → X-SAPR | 5.66 km | 350° |

## Verified against

2026-10-19: layers fetched (Overpass OSM base 2026-10-19T16:02:45Z, TIGER/CB 2024), imagery tiles
and metadata from server.arcgisonline.com, and all five variants rendered from `kernel.py`.
`tests/test_structure_nsa.py` checks the tile arithmetic, the config boxes and labels against
`site_map_assets.csv`, the triangle table, the variant list, and (with cartopy installed) both the
PlateCarree trap and that `lonlat_crs()` and `tiles_in` agree with pyproj.
