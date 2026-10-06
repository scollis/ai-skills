---
name: act-plotting
description: Plot atmospheric time series and profiles with ACT's Display family (act-atmos) - TimeSeriesDisplay (multi-panel, day/night shading, QC flag block plots, assessment overplots, wind barbs, time-height sections, climate stripes), SkewTDisplay (enhanced skew-T with stability box and hodograph), WindRoseDisplay, DistributionDisplay (histogram, heatmap, violin, scatter, size distribution), GeographicPlotDisplay, XSectionDisplay and ContourDisplay. Use whenever ARM or ACT-read data needs a figure, a QC flag timeline or flagged-point overlay is wanted, a radiosonde needs a skew-T, the same variable is compared across sites, or a wind rose or size distribution is requested. Triggers - ACT plotting, TimeSeriesDisplay, SkewTDisplay, WindRoseDisplay, DistributionDisplay, GeographicPlotDisplay, XSectionDisplay, ContourDisplay, qc_flag_block_plot, day_night_background, assessment_overplot, skew-T, hodograph, wind rose, time-height, plot_barbs_from_u_v, plot_stripes, cmweather, ARM plot.
---

# Plotting with ACT

Every ACT plot class inherits from `act.plotting.Display`. The pattern is the same
throughout: construct with a dataset (or a dict of datasets), add subplots, then call
plotting methods with a `subplot_index`. The class owns `display.fig` and
`display.axes` — plain matplotlib objects you can style afterwards.

Companions: `act-arm-live` (data in), `act-qc` (flags these plots visualise),
`act-retrievals`. Run in an env with `act-atmos` installed.

## The shared contract

```python
display = act.plotting.TimeSeriesDisplay(ds, figsize=(12, 8), subplot_shape=(3,))
display.plot("temp_mean", subplot_index=(0,))
display.fig.savefig("out.png", dpi=150, bbox_inches="tight")
```

- **`subplot_shape`** is `(nrows,)` or `(nrows, ncols)`, and `subplot_index` must match
  its rank: `(0,)` for a 1-D layout, `(0, 1)` for 2-D. Mixing them is the most common
  ACT plotting error.
- **A dict of datasets** enables multi-source figures:
  `TimeSeriesDisplay({"E13": ds1, "C1": ds2})`. Once more than one dataset is loaded,
  `dsname=` is required on every method call — with a single dataset it is optional.
- **`display.fig.savefig(...)`**, never `plt.savefig()` — figure lineage tracks the
  namespace object.
- Colormaps: importing `act.plotting` registers the `cmweather` colormaps
  (`ChaseSpectral`, `HomeyerRainbow`, `balance`, ...), so `cmap="ChaseSpectral"` works
  without importing cmweather yourself.
- `Display.add_colorbar`, `Display.put_display_in_subplot` (embed a single-panel
  display into another figure's axis), `Display.assign_to_figure_axis(fig, ax)` (draw
  into an axis you made) and `Display.group_by(units)` (split into a
  `DisplayGroupby` over `'hour'`, `'day'`, `'month'`, ...) are available on all
  subclasses.

## TimeSeriesDisplay

The workhorse. `plot()` carries a lot of behaviour behind keywords:

| Keyword | Effect |
|---|---|
| `day_night_background=True` | yellow/grey shading for daylight; needs `lat`/`lon` in the dataset |
| `assessment_overplot=True` | overplot QC-flagged points in red (Incorrect/Bad) and orange (Suspect/Indeterminate); customise with `assessment_overplot_category` / `_color` |
| `force_line_plot=True` | draw a 2-D field as a set of lines instead of a mesh |
| `use_var_for_y="alt"` | plot against a data variable rather than the second dimension |
| `y_axis_flag_meanings=True` | label the y axis with a categorical variable's `flag_meanings` |
| `abs_limits=(lo, hi)`, `time_rng`, `y_rng` | axis clamps |
| `add_nan=True` | insert NaN across data gaps so lines break instead of interpolating across an outage |
| `cvd_friendly=True` | colour-vision-deficiency-safe palette |
| `yerror=` + `error_kw=` | error bars |
| `set_title=""` | suppress the auto title (needed when overlaying, or titles stack illegibly) |

Beyond `plot()`:

- `qc_flag_block_plot(var)` — one row per QC test, coloured by assessment across time.
  The single most informative QC figure ARM data can produce; pair it with the data
  panel above it (`act_qc_panel` does exactly this).
- `plot_barbs_from_u_v` / `plot_barbs_from_spd_dir` — wind barbs, including
  time-height barbs when `pres_field`/`use_var_for_y` is given; thin with
  `num_barbs_x`, `num_barbs_y` or `barb_step_x/y`.
- `wind_quiver_plot` — surface wind arrows coloured by speed.
- `plot_time_height_xsection_from_1d_data(data_field, pres_field)` — build a
  time-height section from soundings or other 1-D profile records.
- `time_height_scatter(data_field, alt_field="alt")` — scatter profiles in time-height
  space, e.g. a month of sonde launches.
- `fill_between(field)` — shaded band, e.g. accumulated precipitation.
- `plot_stripes(field, reference_period=...)` — warming-stripes rendering of an
  anomaly series.
- `set_xrng`, `set_yrng` (with `match_axes_ylimits=True` to sync panels),
  `day_night_background(subplot_index=...)` as a standalone call.

**Twin axes.** `add_subplots(..., secondary_y=True)` accepts the argument but does not
act on it, and `plot(..., secondary_y=True)` raises `Line2D.set() got an unexpected
keyword argument`. Make the twin yourself:

```python
display.plot("temp_mean", subplot_index=(0,))
ax2 = display.axes[0].twinx()
display.assign_to_figure_axis(display.fig, ax2)
display.plot("rh_mean", color="tab:orange", set_title="")
```

**Overlaying datasets on one axis.** Each `plot()` call resets the x range to its own
dataset's span, so plotting two periods leaves only the last one visible. Restore the
union afterwards with `display.set_xrng([t0, t1], subplot_index=(0,))` —
`act_compare_datasets` handles this.

## SkewTDisplay

```python
sk = act.plotting.SkewTDisplay(sonde, figsize=(14, 10))
sk.plot_enhanced_skewt(spd_name="wspd", dir_name="deg", temp_name="tdry",
                       td_name="dp", p_name="pres")
```

`plot_enhanced_skewt` is the one-call option: skew-T with parcel path and shaded
CAPE/CIN, a hodograph, and a stability box (lifted index, SBCAPE/SBCIN, MUCAPE/MUCIN,
LCL). For finer control use `plot_from_spd_and_dir` or `plot_from_u_and_v`
(`show_parcel`, `shade_cape`, `shade_cin`, `plot_dry_adiabats`, `plot_moist_adiabats`,
`plot_mixing_lines`, `p_levels_to_plot`), plus `plot_hodograph` and
`add_stability_info` separately. ARM `sondewnpn` variables are `pres`, `tdry`, `dp`,
`wspd`, `deg`, `u_wind`, `v_wind`, `alt`.

MetPy emits `UserWarning: Interpolation point out of data bounds` on soundings that do
not reach the LFC — that is the profile, not a bug.

## WindRoseDisplay

```python
wr = act.plotting.WindRoseDisplay(ds, figsize=(7, 7))
wr.plot("wdir_vec_mean", "wspd_vec_mean", spd_bins=[0, 2, 4, 6, 8, 10, 20],
        num_dirs=16, tick_interval=3, calm_threshold=1.0)
```

`plot_data(dir_field, spd_field, data_field, plot_type="Line"|"Contour"|"Boxplot")`
puts a third variable on the rose — concentration by wind sector, for instance —
with `line_plot_calc` choosing `'mean'`, `'median'` or `'stdev'`.

## DistributionDisplay

`plot_stairstep` and `plot_stacked_bar` (histograms, optionally split by a
`sortby_field`), `plot_heatmap(x_field, y_field)` (2-D joint distribution),
`plot_scatter(x_field, y_field, m_field=...)` with `set_ratio_line()` for a 1:1
reference, `plot_violin`, `plot_pie_chart`, and `plot_size_distribution(field, bins)`
for aerosol or drop spectra.

## Spatial and gridded

- `GeographicPlotDisplay.geoplot(data_field, lat_field, lon_field)` — points on a
  cartopy map with `projection`, `cartopy_feature`, `img_tile` (background imagery
  needs network access to the tile server) and `plot_buffer`.
- `XSectionDisplay.plot_xsection(field, x=..., y=...)` and `plot_xsection_map` —
  slices of gridded data, with `sel_kwargs`/`isel_kwargs` to pick the other dimensions.
- `ContourDisplay.create_contour(fields, time=...)` — interpolate scattered station
  values onto a grid and contour them; `plot_vectors_from_spd_dir`, `barbs` and
  `plot_station` add a station-plot overlay.

## Kernel helpers

- `act_timeseries(ds, variables, day_night=True, assessment_overplot=False)` -> stacked panels, one per variable
- `act_qc_panel(ds, variable)` -> two-panel data + QC block figure
- `act_compare_datasets({label: ds, ...}, variable)` -> overlay with a correct x range and legend
- `act_save_display(display, path, dpi=150)` -> save and close, returns the path

For a figure that ships as a deliverable, load the `figure-style` skill and apply it
before rendering — ACT's defaults are functional, not publication-grade.
