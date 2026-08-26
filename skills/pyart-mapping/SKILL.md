---
name: pyart-mapping
description: Cartographic plotting of weather radar with Py-ART and cartopy - RadarMapDisplay.plot_ppi_map and GridMapDisplay projection semantics, the PlateCarree vs Geodetic transform_points datum trap that displaces data by 21 km, verifying georeferencing with the cone of silence as ground truth, geodesic range rings, grid_origin control, multi-panel composition with add_axes, embellish and gridline behaviour, annotation primitives (plot_point, plot_line_geo, plot_range_rings), cross sections and max-CAPPI, and the cartopy cache workaround. Triggers - plot_ppi_map, RadarMapDisplay, GridMapDisplay, plot_maxcappi, cartopy, projection, PlateCarree, LambertConformal, AzimuthalEquidistant, transform_points, range rings, cone of silence, blind zone, georeferencing, radar map, gate_longitude, grid_origin, multi-panel radar figure.
---

# Mapping radar data with Py-ART

Measured against **Py-ART 2.2.5 / cartopy 0.25.0 / pyproj 3.7.2** on KIWA
(NEXRAD VCP 212, 2026-08-20 04:14 UTC) and ARM C-SAPR (MC3E MDV). `kernel.py` auto-loads.

**Read section 2 before writing any plotting code.** One wrong cartopy call displaces
your data by 21 km and produces a figure that looks entirely plausible.

## 1. Verify georeferencing with the cone of silence

Every scanning radar has an unsampled cone above it — the antenna cannot point
straight up, so above the top tilt there is nothing. Its radius grows linearly with
height as `z / tan(top_elevation)`. **That hole is a physical ground-truth marker
whose position you know exactly: it sits on the radar.**

Use it as an assertion, not a decoration:

```python
check_georeference(radar)            # kernel.py -> offset in metres, raises if large
cone_radius_km(radar, height_m=8000.)
```

Measured offsets between the innermost plotted gates and the radar coordinate:

| Case | Offset |
|---|---|
| KIWA `plot_ppi_map`, top tilt (19.51°) | **0.1 m** |
| KIWA `plot_ppi_map`, base tilt (0.48°) | 0.2 m |
| C-SAPR `plot_ppi_map`, any tilt | 0.0 m |
| Gridded, `grid_origin` = radar | within 1 cell of (0,0) |
| Gridded, `grid_origin` = a site 57 km away | 214 m from predicted offset (cell = 1000 m) |

Py-ART's own georeferencing is correct to well under a gate. When the cone lands
somewhere other than the radar, **your plotting code is wrong, not the data.**

Gridded verification — grid a constant field so coverage is purely geometric, then
the hole is the sampling geometry with no meteorology mixed in:

```python
g = sampling_grid(radar, grid_shape=(21,301,301), ...)   # kernel.py, grids a field of ones
cone = measure_cone(g, level=8)     # centroid, cell count, max radius
```

Measured on KIWA, cone radius vs height (top tilt 19.51°, predicted `z/tan`):

| Height AGL | Predicted | Measured hole radius |
|---|---|---|
| 2 km | 5.6 km | 4.1 km |
| 4 km | 11.3 km | 9.5 km |
| 6 km | 16.9 km | 24.1 km |
| 8 km | 22.6 km | 32.1 km |
| 10 km | 28.2 km | 40.1 km |

Below ~4 km the measured hole is *smaller* than `z/tan(top)` because the ROI spreads
data inward; above it the hole is *larger* because beam spreading leaves gaps between
widely separated tilts. `z/tan(top_elev)` is the right order-of-magnitude check, not
an exact prediction — expect agreement to a few km, and treat a factor-of-two
mismatch or an off-centre hole as a bug.

## 2. The transform_points datum trap

**`ccrs.PlateCarree()` is not a geodetic CRS.** Its proj4 carries `+a=6378137.0`
with no flattening — a sphere. `ccrs.Geodetic()` is the WGS84 ellipsoid. Feeding
projected metres through `PlateCarree().transform_points` therefore does a
sphere/ellipsoid mismatch:

```python
aeqd = ccrs.AzimuthalEquidistant(central_longitude=lon0, central_latitude=lat0)

ccrs.PlateCarree().transform_points(aeqd, [0.], [0.])   # (-111.6699, 33.1014)  WRONG
ccrs.Geodetic().transform_points(aeqd, [0.], [0.])      # (-111.6699, 33.2892)  correct
# radar is at                                             (-111.6699, 33.2892)
```

**0.19° of latitude — 20.9 km at 33°N, 23.2 km at 40°N — at the projection origin.**
The magnitude is latitude-dependent; `assert_no_datum_error(lon0=, lat0=)` measures it
where you actually work. Consequences measured on the same KIWA sweep:

| Construction | Cone offset from radar | Range-ring error |
|---|---|---|
| `gate_x/gate_y` → `PlateCarree().transform_points` | **20,891 m** | 21.1 km at every radius |
| `gate_x/gate_y` → `Geodetic().transform_points` | 0.1 m | < 0.1 m |
| `radar.gate_longitude` / `gate_latitude` | 0.1 m | — |
| `pyproj.Transformer` on Py-ART's `grid_projection` | 0.0 m | 0.0 m |

The error is a constant offset, so the *pattern* looks perfect — storms have the
right shape, the right texture, the right gradients. Only the absolute position is
wrong, and only by an amount that matters for exactly the comparisons you'd make a
radar map for (gauge matchups, site overlays, multi-sensor work).

Three rules:

1. **Prefer `radar.gate_longitude["data"]` / `gate_latitude["data"]`.** Py-ART computes
   these correctly; there is no reason to reproject `gate_x`/`gate_y` yourself.
2. If you must transform projected coordinates to lon/lat, the source is
   `ccrs.Geodetic()` or a `pyproj.Transformer`, **never `ccrs.PlateCarree()`**.
3. When you `pcolormesh` lon/lat arrays onto a cartopy axis, `transform=ccrs.PlateCarree()`
   is correct **and required** — cartopy rejects `Geodetic` for pcolormesh
   (`ValueError: Invalid transform: Spherical pcolormesh is not supported`). The
   asymmetry is real: `PlateCarree` as a *plotting transform* for lon/lat data is
   fine; `PlateCarree` as a *source CRS* for `transform_points` on projected metres
   is not.

`kernel.py` gives `gates_to_lonlat(radar, sweep)` which just returns Py-ART's own
arrays, and `assert_no_datum_error()` which runs the origin round-trip as a test.

## 3. Projection handling in `plot_ppi_map`

```python
disp = pyart.graph.RadarMapDisplay(radar)
disp.plot_ppi_map("reflectivity", sweep=0, ax=ax, ...)
```

Verified behaviours:

- **`ax` wins over `projection=`.** Passing both silently ignores `projection=` and
  keeps the axis's own. Set the projection when you create the axis.
- With no `ax`, `projection=` creates one; the default is `PlateCarree`.
- `display.grid_projection` is a **pyproj CRS**, an azimuthal-equidistant centred on
  the radar (`+proj=aeqd +ellps=WGS84 +lon_0=... +lat_0=...`). Rings built in it are
  geodesically exact (verified to 0.0 m at 60 and 120 km). This is the object to
  reuse if you need to place things in radar-relative metres.
- Georeferencing is correct in **every** axis projection tested — PlateCarree,
  LambertConformal, AzimuthalEquidistant, Mercator all put the gates within 35
  projected metres of truth.

Recommended axis projection: `LambertConformal` centred on the radar for regional
maps (conformal, so storm shapes are preserved), or `AzimuthalEquidistant` centred on
the radar when range from the radar is what you're reading off the figure.

### `embellish` and gridlines

`embellish=True` (the default) adds coastlines, borders and a `Gridliner`. It fights
`fig.add_axes` layouts and makes multi-panel composition unpredictable. For any
figure you control the layout of:

```python
disp.plot_ppi_map(..., embellish=False, add_grid_lines=False,
                  lat_lines=[], lon_lines=[], title_flag=False)
ax.add_feature(cfeature.STATES.with_scale("10m"), lw=.4, edgecolor="#999999")
```

Then add exactly the features and gridlines you want. `resolution="10m"` for regional
work, `"110m"` for continental.

**Sandbox:** cartopy cannot write its default cache — `setup_cartopy_cache()` from
`pyart-foundations` (also re-exported here) must run before any `add_feature`.

## 4. Annotation primitives — no `ax` kwarg

```python
disp.plot_ppi_map(...)                     # sets display.ax
disp.plot_range_rings([30., 60., 90., 120.])
disp.plot_point(lon, lat, label_text="C-SAPR2")
disp.plot_line_geo([lon0, lon1], [lat0, lat1])
disp.plot_line_xy([0, 50000], [0, 50000])
```

`plot_point`, `plot_line_geo` and `plot_line_xy` **do not accept `ax=`** — passing it
raises `AttributeError: Line2D.set() got an unexpected keyword argument 'ax'`, because
the kwargs go straight to `ax.plot`. They draw on `display.ax`, set by the most recent
`plot_ppi_map`. `plot_range_ring` *does* accept `ax` — it pops and discards it. In a
multi-panel figure, either create one display per axis or call the annotations
immediately after each panel's `plot_ppi_map`.

`plot_range_ring` builds its circle in `grid_projection` (the radar-centred aeqd), so
the rings are geodesically correct. If you need rings you control (multiple radars,
custom styling), use `cartopy.geodesic.Geodesic().circle(...)` — also exact — via
`range_ring(lon, lat, km)` in `kernel.py`. Do **not** draw `plt.Circle` with a
degree radius; that is only correct at the equator.

## 5. Grid plotting and `grid_origin`

`grid_from_radars` defaults its origin to the **first radar's** position. For
multi-radar composites, or when the figure should be centred on a site rather than an
instrument, set it explicitly:

```python
g = pyart.map.grid_from_radars((r1, r2), grid_shape=(21,301,301),
        grid_limits=((0.,20000.),(-200000.,200000.),(-200000.,200000.)),
        grid_origin=(site_lat, site_lon), fields=["reflectivity"], ...)
```

Verified: with `grid_origin` set to a site 57 km from the radar, the cone of silence
appeared at x=44,740 y=−35,462 m against a predicted x=44,954 y=−35,420 — **214 m
error on a 1000 m grid**. `grid_origin` is honoured exactly; `origin_latitude`/
`origin_longitude` on the Grid record what was used.

`GridMapDisplay` methods, all working and all fast (<0.1 s):

| Method | Purpose |
|---|---|
| `plot_grid(field, level=, ax=)` | horizontal slice at a z level |
| `plot_latitude_slice` / `plot_longitude_slice` | vertical cuts through the grid |
| `plot_cross_section(field, start=(lat,lon), end=(lat,lon))` | arbitrary vertical section |
| `plot_crosshairs` | mark the origin |
| `plot_maxcappi(grid, field, add_map=True)` | column-max with side panels |

`plot_maxcappi` is a module-level function (`pyart.graph.plot_maxcappi`) as well as a
`GridMapDisplay` method. It creates its own figure — pass `show_figure=False` and
`savedir=` in a script, or grab `plt.gcf()`.

## 6. Multi-panel composition

`fig.add_axes` with explicit rectangles is the reliable route; `tight_layout` and
`bbox_inches="tight"` both interact badly with cartopy `GeoAxes` (a tight bbox has
been observed to crop a map panel out of the canvas entirely). Save with an explicit
dpi and no bbox adjustment:

```python
fig = plt.figure(figsize=(14, 9))
ax = fig.add_axes([0.05, 0.55, 0.27, 0.38], projection=P)
...
fig.savefig("out.png", dpi=175)          # NOT bbox_inches="tight"
```

`mpl.rcParams["savefig.bbox"]` may be `"tight"` from a style; set it to
`"standard"` explicitly if a panel goes missing.

For deliverable figures load the `figure-style` skill and call `apply_figure_style()`
first; for multi-panel deliverables, `figure-composer`.

Colormaps: cmweather, as house convention — `ChaseSpectral` for Z/KDP/rain rate,
`balance` for velocity, `plasmidis` for RhoHV (note the spelling; `plasmidic` is not
a colormap and raises).

## 7. Diagnostic checklist

Run these before trusting any radar map:

1. `check_georeference(radar)` — cone on the radar, offset in metres.
2. `assert_no_datum_error()` — the PlateCarree/Geodetic origin round-trip.
3. Plot the radar position as a marker on every panel. If it isn't in the middle of
   the blind zone, stop.
4. Overlay a known range ring and confirm the data edge sits at the documented
   maximum range (`radar.range["data"].max()`).
5. For grids, confirm `origin_latitude`/`origin_longitude` are what you passed.

## Verified against

Py-ART 2.2.5, cartopy 0.25.0, pyproj 3.7.2. Datum round-trip, cone-of-silence offsets and geodesic range rings re-measured on KIWA 2026-08-20 04:14 UTC. The PlateCarree displacement is latitude-dependent: 20.9 km at 33.29 N, 23.2 km at 40 N.

Last re-run: 2026-08-26.
