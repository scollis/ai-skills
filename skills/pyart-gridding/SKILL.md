---
name: pyart-gridding
description: Interpolate weather radar volumes onto Cartesian grids with Py-ART - choosing radius of influence by holdout cross-validation instead of guessing, the dist_beam vs dist vs constant ROI functions and what nb/bsp mean physically, Barnes2 vs Cressman vs Nearest weighting, grid_from_radars vs map_gates_to_grid vs map_to_grid, the (z, y, x) grid_shape/grid_limits ordering trap, grid_origin control for site-centred and multi-radar composites, dual-radar composites and GateMapper inter-radar calibration, gatefilters tuple semantics, Grid output via to_xarray/write/write_grid_geotiff, and grid_displacement_pc advection. Triggers - grid, gridding, grid_from_radars, map_gates_to_grid, map_to_grid, radius of influence, roi, dist_beam, constant_roi, nb, bsp, Barnes, Cressman, Nearest, weighting_function, grid_shape, grid_limits, grid_origin, Cartesian, CAPPI, composite, multi-radar, GateMapper, Grid.to_xarray, write_grid_geotiff, grid_displacement_pc, advection.
---

# Gridding radar data with Py-ART

Measured against **Py-ART 2.2.5** on KIWA (NEXRAD WSR-88D, VCP 212, SAILSx1, 19 sweeps,
2026-08-20 04:14 UTC), KFSX as a second radar at a 149 km baseline, and ARM SGP C-SAPR
(research C-band, MC3E 2011-05-20 11:29 UTC, MDV, 17 tilts, one sweep per elevation).
`kernel.py` auto-loads.

**Read section 1 before you pick a radius of influence.** ROI is the single parameter
that decides whether your grid is an interpolation of the radar or an invention. It is
measurable on your own volume in about a minute, and the default is not the best choice
for every job.

## 1. Radius of influence is measurable, not a guess

Hold out data the radar already collected, grid from what is left, and ask the grid to
predict the gates you removed. Every ROI and weighting decision below was scored this
way.

Method:

1. Withhold every 5th ray of the volume with a `GateFilter` (gate geometry unchanged,
   those gates simply stop contributing).
2. Grid the remainder with the candidate ROI configuration.
3. Interpolate the resulting grid back to the withheld gate positions with
   `scipy.interpolate.RegularGridInterpolator` over `(grid.z, grid.y, grid.x)`.
4. Score RMSE, MAE and bias against the withheld gate values, and record **coverage** —
   the fraction of withheld gates the grid could predict at all.

```python
train, truth = holdout_split(radar, field="reflectivity", every=5)
spec  = grid_spec(radar)                      # (z, y, x) ordered, see section 4
grid  = pyart.map.grid_from_radars(
    (radar,), gatefilters=(train,), **spec,
    roi_func="dist_beam", nb=1.5, bsp=1.0, min_radius=500.0,
    weighting_function="Barnes2")
score_grid_against_holdout(grid, truth)       # -> rmse, mae, bias, coverage, grid_filled
sweep_roi_configs(radar)                      # -> DataFrame, one row per config
```

Two scores move in opposition and you must report both. **Coverage** is skill at
answering; **RMSE** is skill at answering correctly. A configuration with excellent RMSE
and 43% coverage has mostly declined to interpolate.

### ROI function and parameters, scored on the same volume

Reflectivity, every 5th ray withheld, Barnes2 weighting throughout. `grid_filled` is the
fraction of grid cells that received any data; `coverage` is the fraction of withheld
gates the grid could predict.

| ROI config | coverage | RMSE dBZ | MAE dBZ | bias dBZ | grid_filled | s |
|---|---|---|---|---|---|---|
| `dist_beam` nb 0.75, min_radius 250 | 0.430 | **4.520** | 3.501 | **-0.271** | 0.277 | 0.63 |
| `dist_beam` nb 1.0, min_radius 250 | 0.669 | 4.556 | 3.514 | -0.086 | 0.363 | 0.75 |
| `dist_beam` nb 1.0, min_radius 500 | 0.741 | 4.625 | 3.571 | -0.107 | 0.365 | 0.71 |
| **`dist_beam` nb 1.5, min_radius 500** | **0.924** | **4.625** | 3.555 | **-0.010** | 0.460 | 1.13 |
| `dist_beam` nb 2.0, min_radius 500 | 0.967 | 4.787 | 3.679 | 0.030 | 0.530 | 1.91 |
| `constant` 500 m | 0.275 | 5.336 | 4.133 | -0.298 | 0.110 | 0.44 |
| `constant` 1000 m | 0.717 | 4.787 | 3.703 | -0.160 | 0.262 | 0.54 |
| `constant` 2000 m | 0.984 | 4.919 | 3.755 | 0.028 | 0.427 | 1.13 |
| `constant` 4000 m | 1.000 | 5.806 | 4.425 | 0.147 | 0.596 | 5.31 |

**These absolute numbers are volume- and QC-specific.** Re-running the same sweep with
a different base gatefilter moved nb-1.5 RMSE between 4.57 and 4.96 dBZ and coverage
between 0.858 and 0.924. What transfers is the **ranking**, which was stable in every
run: `dist_beam` ahead of `constant` at matched coverage, and the knee at nb 1.5.
Run `sweep_roi_configs` on your own volume with your own QC recipe and read the ordering,
not these digits.

Conclusions that hold across the whole sweep:

- **`dist_beam` beats `constant` at every coverage level.** At matched coverage:
  0.741 vs 0.717 coverage gives RMSE 4.625 vs 4.787; 0.924 vs 0.984 gives 4.625 vs
  4.919. `dist_beam` is the only ROI function that grows with range the way the sampling
  volume itself grows, so it is the only one that is doing physics rather than
  book-keeping. Use it unless you have a specific reason not to.
- **nb 1.5, bsp 1.0, min_radius 500 is the knee.** It is the largest coverage (0.924)
  available before RMSE starts climbing, and its bias (-0.010 dBZ) is the smallest in
  the table.
- **Small ROI buys accuracy and pays in coverage *and* bias.** nb 0.75 has the best RMSE
  in the table (4.520) with 43% coverage and a -0.271 dBZ bias: only the nearest, and in
  convection the strongest, gates survive inside a tiny influence radius, so the grid
  systematically under-reports.
- **Large constant ROI is the worst of both.** `constant` 4000 m reaches full coverage
  but at RMSE 5.806 — worse than every `dist_beam` row — and costs 5.31 s against 1.13 s
  at the knee. Over-smoothing is not conservative; it is a different kind of wrong.
- Bias crosses zero between nb 1.5 (-0.010) and nb 2.0 (+0.030). If your downstream
  product is a bias-sensitive accumulation, that crossing is where to sit.

### Weighting function

| ROI config | weighting | coverage | RMSE dBZ | MAE dBZ | bias dBZ | s |
|---|---|---|---|---|---|---|
| nb 1.0, min 250 | Barnes2 | 0.669 | 4.556 | 3.514 | -0.086 | 0.73 |
| nb 1.0, min 250 | Cressman | 0.669 | 4.581 | 3.536 | -0.087 | 0.68 |
| nb 1.0, min 250 | Nearest | **0.058** | 5.452 | 4.196 | 0.081 | 0.88 |
| nb 1.5, min 500 | Barnes2 | 0.924 | 4.625 | 3.555 | -0.010 | 1.18 |
| nb 1.5, min 500 | Cressman | 0.924 | 4.672 | 3.592 | -0.008 | 1.00 |
| nb 1.5, min 500 | Nearest | **0.077** | 5.447 | 4.187 | 0.045 | 1.62 |

- **Barnes2 and Cressman are indistinguishable** — 0.025 to 0.047 dBZ RMSE apart, with
  identical coverage. Barnes2 (the default) is marginally ahead in both configurations.
  Do not spend time choosing between them; spend it on ROI.
- **`Nearest` is a lookup, not an interpolator.** It recovers 5.8% and 7.7% of withheld
  gates, and is a dBZ worse where it does answer. It assigns each gate to one cell
  rather than distributing it, so a grid built with `Nearest` is sparse by construction.
  Use it only when you deliberately want unsmoothed gate values on a grid, never as a
  general-purpose choice.

The weight formulas, from the Cython mapper, with `roi2` the squared radius of influence
and `dist2` the squared gate-to-cell distance:

| weighting_function | weight |
|---|---|
| `Barnes` | `exp(-dist2 / (2*roi2)) + 1e-5` |
| `Barnes2` (default) | `exp(-dist2 / (roi2/4)) + 1e-5` |
| `Cressman` | `(roi2 - dist2) / (roi2 + dist2)` |
| `Nearest` | nearest cell only |

Barnes2 is a narrower Gaussian than Barnes at the same ROI — the `/4` is why the two ROI
knobs and the weighting choice are not independent.

## 2. The three ROI functions

`roi_func` selects one of three Cython classes. Each returns, per grid cell, the minimum
radius over all radars in the composite — which is what makes the multi-radar case work
without extra arguments.

| `roi_func` | parameters | radius at cell offset (z, y, x) from a radar |
|---|---|---|
| `dist_beam` (default) | `nb`, `bsp`, `min_radius`, `h_factor` | `sqrt((h_z·z)² + (h_y·y)² + (h_x·x)²) · tan(nb·bsp·π/180)`, floored at `min_radius` |
| `dist` | `z_factor`, `xy_factor`, `min_radius` | `z_factor·z + xy_factor·sqrt(y² + x²)`, floored at `min_radius` |
| `constant` | `constant_roi` | `constant_roi` everywhere |

`nb·bsp` is **an angle in degrees**: `nb` is the number of beams to span and `bsp` the
beam spacing in degrees. `tan()` of it converts that angular width into a cross-beam
distance at the cell's slant range, so `dist_beam`'s radius is literally "how wide are
`nb` beams out here". That is why it tracks beam spreading and `dist` (a linear
range ramp with separate vertical and horizontal slopes) only approximates it. For a
radar with a beamwidth near 1°, `bsp=1.0` and `nb=1.5` means a 1.5° influence cone;
KIWA's beamwidth is 0.925°, C-SAPR's near 1°, so the same knee applies to both classes
here. On a radar with a materially different beamwidth, set `bsp` to that beamwidth and
keep `nb` as the number of beams.

`h_factor` and `dist_factor` (3-element, `(z, y, x)`) scale the vertical term in the
radius and in the distance-weighting respectively. Setting both to `(0.0, 1.0, 1.0)`
removes height from the calculation, which is how the single-sweep helpers work —
`pyart.map.grid_ppi_sweeps` and `grid_rhi_sweeps` wrap `grid_from_radars` with those
factors preset and grid each sweep to its own plane. Do not pass `h_factor` or
`dist_factor` through their `**kwargs`; they set them for you.

`min_radius` matters more than it looks: it is the floor near the radar, where the beam
is narrow and cells outnumber gates. Raising it from 250 to 500 m at nb 1.0 bought
coverage 0.669 to 0.741 for 0.069 dBZ of RMSE.

## 3. Which mapper to call

| Call | Returns | Use when |
|---|---|---|
| `pyart.map.grid_from_radars(radars, grid_shape, grid_limits, ...)` | `Grid` object | Almost always. Wraps the mapper, builds coordinates, metadata and radar location arrays. |
| `pyart.map.map_gates_to_grid(...)` | `dict` of arrays | You want the bare field arrays and will assemble your own container. This is `grid_from_radars`' default engine (`gridding_algo="map_gates_to_grid"`). |
| `pyart.map.map_to_grid(...)` | `dict` of arrays | Legacy kd-tree/ball-tree path (`algorithm=`, `leafsize=`, `copy_field_data=`). Reach for it only to reproduce an older result; select it via `gridding_algo="map_to_grid"`. |
| `pyart.map.grid_ppi_sweeps` / `grid_rhi_sweeps` | `Grid` | Per-sweep 2D gridding with the vertical term switched off. |

Both `map_*` functions return plain dictionaries keyed by field name — no coordinates,
no georeferencing. If you find yourself rebuilding `Grid` metadata by hand, you wanted
`grid_from_radars`.

## 4. `grid_shape` and `grid_limits` are (z, y, x)

Not `(x, y, z)`. This is the most common gridding error and it is silent: a transposed
shape produces a legal `Grid` with the wrong aspect, and the plot looks like data.

```python
grid_shape  = (41, 401, 401)                                   # nz, ny, nx
grid_limits = ((0., 20000.), (-100000., 100000.), (-100000., 100000.))  # z, y, x metres
```

Limits are metres relative to `grid_origin`, not degrees, and not relative to the radar
unless the origin is the radar. Use `grid_spec(radar)` from `kernel.py` to build both in
the right order from the radar's own range.

Cell spacing follows from the pair: `(limits[i][1] - limits[i][0]) / (shape[i] - 1)`.
Choose it against your ROI, not independently — a 250 m grid under a 2000 m ROI is
storing the same smoothed field four times over.

## 5. `grid_origin` defaults to the first radar

With `grid_origin=None` the grid is centred on `radars[0]`'s latitude and longitude
(`grid_origin_alt` likewise on its altitude). Two cases where that default is wrong:

- **Multi-radar composites.** The origin silently becomes whichever radar you listed
  first, so reordering the tuple moves your grid. Set it.
- **Site-centred grids.** Products for an instrument site (a profiler, a disdrometer, an
  ARM facility) should be centred on the site, not the radar.

```python
grid = pyart.map.grid_from_radars(
    (radar,), grid_shape=(41, 401, 401),
    grid_limits=((0., 20000.), (-100000., 100000.), (-100000., 100000.)),
    grid_origin=(site_lat, site_lon), grid_origin_alt=site_alt_m,
    roi_func="dist_beam", nb=1.5, bsp=1.0, min_radius=500.)
```

**Gridded georeferencing is verifiable, and it verifies.** The cone of silence is a
physical hole whose position you know exactly, so its location in the grid is an
assertion you can run. With `grid_origin` set to a site 57 km from the radar, the cone
appeared 214 m from its geometrically predicted position on a 1000 m grid — a fifth of a
cell. See **pyart-mapping** for the full method; do not re-derive it here. If your cone
lands somewhere else, the origin or the projection is wrong, not the data.

## 6. `gatefilters` is a tuple, one per radar

Not a single filter, even for a single radar. `gatefilters=(gf,)` — the trailing comma
is load-bearing. And each filter must have been built against the radar object at the
same position in `radars`:

```python
gf_a = pyart.filters.GateFilter(radar_a)   # NOT reusable on radar_b
gf_b = pyart.filters.GateFilter(radar_b)
grid = pyart.map.grid_from_radars((radar_a, radar_b), gatefilters=(gf_a, gf_b), ...)
```

A filter carries an `(nrays, ngates)` mask. Applying one radar's filter to another —
easy to do when you have re-read, subset or `extract_sweeps`-ed a volume — either raises
on shape or, worse, matches by accident and masks the wrong gates. See the wrong-shape
trap in **pyart-gatefilter-qc**, and build the filter *after* the last operation that
changes ray count.

QC before gridding is not optional: the exclusion recipe changes gridded means by
several dBZ on the same volume. **pyart-gatefilter-qc** has the marginal-value table.

## 7. Multi-radar composites and inter-radar comparison

Adding a radar buys fill, and the price is a disagreement you must look at.

| Quantity | Measured |
|---|---|
| Grid cells filled, KIWA alone | 0.196 |
| Grid cells filled, KIWA + KFSX | 0.265 |
| Baseline separation | 149 km |
| Mean absolute reflectivity difference in the overlap | 2.06 dBZ |

Two radars, one call — `roi_func="dist_beam"` already takes the minimum radius over both
radar positions, so no extra arguments are needed:

```python
grid = pyart.map.grid_from_radars(
    (radar_a, radar_b), grid_shape=..., grid_limits=...,
    grid_origin=(mid_lat, mid_lon),          # set it; see section 5
    gatefilters=(gf_a, gf_b),
    roi_func="dist_beam", nb=1.5, bsp=1.0, min_radius=500.)
```

A 2.06 dBZ mean absolute difference in the overlap is the *post-interpolation* residual.
For the calibration question — is radar B offset from radar A — do not use the grid. Use
`pyart.map.GateMapper`, which matches individual gates between volumes:

```python
gm = pyart.map.GateMapper(src_radar, dest_radar,
                          distance_tolerance=500., time_tolerance=60.,
                          gatefilter_src=gf_src)
mapped = gm.mapped_radar        # src fields resampled onto dest's geometry
```

At the 149 km baseline this matched **10,988 gates** and gave a **+5.31 dBZ mean offset
with 18.1 dBZ scatter**. Read both numbers together: a mean offset an order of magnitude
smaller than its own scatter is not a calibration constant. At long baselines the two
radars are sampling different parts of different beams at different heights, and that
geometry dominates. GateMapper is the right primitive for inter-radar calibration; a
149 km baseline is the wrong geometry for it. Shrink the baseline, tighten
`distance_tolerance` and `time_tolerance`, restrict to low elevations and stratiform
echo, and re-read the scatter before quoting an offset. **arm-dualpol-calibration**
covers the single-radar calibration checks.

## 8. Grid output

| Call | Notes |
|---|---|
| `grid.to_xarray()` | `xr.Dataset` with `time, z, y, x` dims and CF-ish coordinates. The route to anything xarray, and to plotting outside Py-ART. 0.15 s. |
| `grid.write("out.nc")` | Grid-format netCDF, round-trips through `pyart.io.read_grid`. 0.15 s. |
| `pyart.io.write_grid_geotiff(grid, fn, field, ...)` | **Needs GDAL, which a plain conda Py-ART env does not have** — raises `MissingOptionalDependency`. Install GDAL first, or write netCDF and convert outside Py-ART. |
| `grid.get_point_longitude_latitude(level=...)` | Per-cell lon/lat for a horizontal level. |

`write_grid_geotiff` takes `field` (one field per file), optional `level`, `rgb`,
`cmap`, `vmin`/`vmax`, `warp` and `sld`. It is a visualisation export, not an archive
format.

Plotting: use `GridMapDisplay`, and cmweather colormaps — `ChaseSpectral` for
reflectivity, KDP and rain rate, `balance` for velocity, `plasmidis` for RhoHV.
**pyart-mapping** has the projection semantics.

## 9. Advection between two grids

`pyart.retrieve.grid_displacement_pc(grid1, grid2, field, level, return_value="pixels")`
cross-correlates one horizontal level of two grids and returns the displacement.
`return_value` also accepts distance and velocity forms. Both grids must share shape,
limits and origin — grid the two times with identical `grid_shape`, `grid_limits` and
`grid_origin` or the displacement is meaningless. Level choice matters: pick one with
echo in both frames, well below echo top.

## 10. Runtime budget

All timings below are the same volume and the same grid; the spread comes from ROI
alone. Cost scales with the number of cells each gate touches, i.e. with ROI³.

| Configuration | s |
|---|---|
| `constant` 500 m | 0.44 |
| `constant` 1000 m | 0.54 |
| `dist_beam` nb 1.0 | 0.71 - 0.75 |
| `dist_beam` nb 1.5 (knee) | 1.13 - 1.18 |
| `dist_beam` nb 2.0 | 1.91 |
| `constant` 2000 m | 1.13 |
| `constant` 4000 m | 5.31 |
| `grid.write` / `to_xarray` | 0.15 |

A 12x runtime range from one parameter on an identical grid. Gridding is cheap enough
that the holdout sweep in section 1 — nine configurations — costs about 12 s of compute.
There is no budget argument for guessing the ROI.

## 11. Radar-class differences that reach the grid

| | NEXRAD WSR-88D (KIWA) | Research C-band (C-SAPR) |
|---|---|---|
| Sweeps per elevation | Split cuts: surveillance + Doppler at the same tilt | One sweep per elevation, 17 tilts 0.75-42.0° |
| Consequence for gridding | The same elevation contributes twice, with different fields valid on each. Subset to one cut per tilt before gridding or you are weighting that layer twice. | Grid the volume as read. |
| Gate spacing / range | Coarser gates, longer range | 120 m gates to 118 km — finer than most grids people build; do not choose 1000 m cells by habit |
| `normalized_coherent_power` | Absent | Present, usable in the pre-grid gate filter |
| Nyquist | 25.0 - 34.7 m/s, varies by sweep | 16.52 m/s uniform |
| Gridding velocity | Dealias first, per-sweep Nyquist | Dealias first, uniform Nyquist |

Never grid raw Doppler velocity. Aliased velocity averaged inside an ROI produces values
that are neither of the two folds. Dealias, then grid — **pyart-velocity-dealias**.

## 12. Checklist

1. QC the volume and build the `GateFilter` last, after any `extract_sweeps` or subset
   (**pyart-gatefilter-qc**).
2. Dealias velocity before gridding it (**pyart-velocity-dealias**); KDP and PhiDP
   likewise want processing on the polar grid first (**pyart-dualpol-phase**).
3. For NEXRAD, subset split cuts to one sweep per elevation.
4. Build `grid_shape`/`grid_limits` as `(z, y, x)`; check cell spacing against ROI.
5. Set `grid_origin` explicitly for anything but a single radar-centred grid.
6. Run `sweep_roi_configs(radar)` once per radar class and per season; start from
   `recommended_roi(radar)`.
7. Pass `gatefilters` as a tuple, one filter per radar, each matching its radar.
8. Verify the cone of silence lands where geometry says (**pyart-mapping**).
9. Grid-space retrievals and classifications: **pyart-retrievals**. The ARM
   corrected-moments VAP that consumes gridded output: **cmac-vap**.

## Verified against

Py-ART 2.2.5, scipy 1.14. Holdout ROI and weighting sweeps re-run on KIWA 2026-08-20 04:14 UTC; multi-radar coverage and GateMapper offsets against KFSX at a 149 km baseline. Absolute RMSE is volume- and QC-specific; re-run sweep_roi_configs on your own data.

Last re-run: 2026-08-26.
