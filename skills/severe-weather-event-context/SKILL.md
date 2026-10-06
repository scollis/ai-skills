---
name: severe-weather-event-context
description: Analyse a severe convective weather event and place it in climatological context - NWS storm reports and surveyed tornado damage paths, HRRR mesoscale environment fields, GFS integrated vapour transport and back trajectories to the moisture source, soil moisture and Bowen-ratio partitioning along the advection path, river-gauge flood status, and percentile ranking against observed radiosonde and station climatologies. Use when asked why a storm was severe, where its moisture came from, how a month or event compares to normal, or to build an interview or briefing package from a tornado, hail, wind or flooding event.
---

# Severe-weather event context

Turns a convective event into a defensible narrative: what made it severe, where
the moisture came from, and how unusual it was. Built from a Chicagoland tornado
outbreak plus the flood that followed four days later.

`kernel.py` loads with this skill. Every helper below encodes a trap that cost
real debugging time.

## Radar goes through the radar skills

For NEXRAD volumes, PPI plotting and animations, load `nexrad-radar-gcs`
(THREDDS/GCS fetch, `make_radar_geoaxes`, `plot_ppi_map`) or `nexrad-arco` (ARCO
Zarr store, `add_stations` for METAR overlays). **Do not** hand-roll a radar map
axes: `nexrad-radar-gcs` documents the cartopy `AzimuthalEquidistant` bug that
silently shifts a radar field ~20 km and ships the Mercator fix.

Two Py-ART traps worth restating because they cost hours:

- **Split cuts** put reflectivity and dual-pol on one sweep and Doppler velocity
  on the *next*. Applying a `cross_correlation_ratio` gate filter to the velocity
  sweep blanks the panel entirely. Select sweeps per field.
- **Velocity is aliased.** A folded field at +/-24 m/s hides true motion reaching
  +/-60. Run `pyart.correct.dealias_region_based` - it dominates per-volume cost
  (10-60 s) and is essential to see rotation.

## Establish the event before analysing it

Fetch the ground truth first and let it set your analysis window. News coverage
of an event is frequently wrong about timing.

```python
lsr = iem_storm_reports("2026-07-27T12:00", "2026-07-28T12:00", ["LOT", "MKX"])
lsr["cdt"] = lsr.VALID.dt.tz_convert("America/Chicago")
lsr.groupby([lsr.cdt.dt.floor("1h"), "TYPETEXT"]).size().unstack(fill_value=0)
```

Then get the **surveyed** tornado paths - real damage geometry, not point
approximations:

```python
gj = dat_tornado_tracks("LOT", "2026-07-27")     # GeoJSON, layer 1 = Damage Lines
```

Carries `efscale`, `starttime`/`endtime` (epoch ms), `length`, `width`,
`maxwind` and full polylines. Layer 0 (damage points) is often empty. **Never
"tidy" the vertex order**: one surveyed path in the source event traced a genuine
2.8 km loop, and reordering along the principal axis inflated it from 18.4 to
46 km. Validate against the survey's own `length` field before touching geometry.

Justify your window from what you fetched, not from prose you were handed.

## The mesoscale environment

Use Herbie for HRRR. Two hard-won points:

- **`fxx=1`, not `fxx=0`.** The F00 analysis carries no spun-up convection, so
  vertical velocity is near-zero and the max-in-previous-hour diagnostics
  (`MXUPHL`, `MAXUVV`, `APCP`) do not exist. F01 ascent measured ~38x stronger.
- **The two SRH layers collide.** `HLCY` at 0-1 km and 0-3 km share both the
  variable name and `typeOfLevel`, so one harvest dict silently keeps one. Fetch
  them in separate calls with explicit level search strings.

Ask which ingredient is *anomalous* rather than merely large. In the source event
instability was extreme but unremarkable for July; **65 kt of deep-layer shear in
late July, where 20-30 kt is normal**, was the story.

Watch for composite parameters peaking at the wrong time. Significant tornado
parameter was 4.2 during the tornadoes and 7.7 four hours later - during a
linear round that produced no tornadoes but most of the wind damage. **Storm mode,
not environment alone, sets the hazard**, and a panel title claiming otherwise is
contradicted by its own data.

A model sounding inside outflow is not the storm environment. Diagnose it from a
theta-e collapse plus a temperature drop during peak heating after measurable
rain - not from a surface-to-925 inversion, which may not exist.

## Where the moisture came from

GFS 0.25 deg via Herbie (`model="gfs"`, `product="pgrb2.0p25"`). Four gotchas:

- Longitude is 0-360: `np.where(lon > 180, lon - 360, lon)`.
- Latitude **descends** - flip to ascending before any `RegularGridInterpolator`.
- Levels are stored decreasing, so a `trapezoid` over p yields negative dp.
  `ivt()` handles the sign and is level-order invariant.
- `PWAT` exists only as `":PWAT:entire atmosphere (considered as a single layer):anl:"`.

```python
qu, qv, mag = ivt(q, u, v, levels_hpa)          # >250 is atmospheric-river magnitude
```

**Validate the sign** by comparing the flux vector direction against the 850 hPa
wind at the same point. Then trace the air back:

```python
t, la, lo, q_gkg = back_trajectory(41.88, -88.08, "2026-07-27 12:00",
                                   times, lat_1d, lon_1d, u_cube, v_cube, q_cube)
```

Run several levels. In the source event only 925 hPa was Gulf-sourced (Texas
coast, four days upstream, gaining 44% more vapour); 850 hPa came from the High
Plains and 700 hPa from Montana. The low-level path is the relevant one when the
boundary layer holds most of the column - check that fraction rather than
assuming it. Dry air stacked above moist is itself favourable: it steepens lapse
rates.

Trajectories are **isobaric** - enough to attribute a source region over a few
days, not a substitute for a kinematic or HYSPLIT path. Say so.

## Did the land surface help?

Soil moisture (`SOILW`) comes back from Herbie as **one** dataset with all four
layers stacked on `depthBelowLandLayer`, shape `(4, lat, lon)` - a subset helper
must handle `ndim == 3`.

**Surface fluxes are time-averaged, so the window must be local daytime.** The
06Z cycle at `fxx=6` covers 06-12 UTC - the middle of the night over the Plains -
and yields negative sensible heat. Use the 12Z cycle at `fxx=9` (6-9 h average =
18-21 UTC).

```python
b = bowen(lhtfl, shtfl)      # b["bowen"], b["ef"], b["ef_clipped"]
```

Evaporative fraction exceeding 1 is real where sensible heat is slightly
downward over a wet surface cooler than the air. Report the Bowen ratio as the
robust metric and clip EF only for display.

GFS soil moisture is the **Noah land-surface model state inside the GFS
assimilation**, not a measurement - spun up by GFS's own precipitation history.
Corroborate with gauge rainfall as a percentage of local normal; the source event
showed a dry gap (Wichita 9% of normal, 3rd percentile) flanked by wet ground
(Des Moines 220%, 97th), and the parcel lost vapour over the dry leg and regained
it over the wet one.

**The link worth making:** wet soil is simultaneously an ingredient for severe
storms and a precondition for flooding. It explains why one week produced both.

## Percentiles, and the tie trap

```python
r = pct_rank(july_totals, 5.36)
# {'n':57,'rank':9,'percentile':86.0,'n_above':8,'n_tied':1,'is_record':False}
```

`rank` counts values >= yours; `percentile` is the share <= yours. **With integer
counts these are not reciprocal** and the naive `(n-rank+1)/n` is wrong: two
metrics can share rank 16 of 57 yet sit at the 77th and 82nd percentile because 3
years tie one and 6 tie the other. A 100th percentile means `is_record` - no year
exceeded it - which may still involve ties. State the convention in any table you
publish; a reader recomputing with the naive formula will otherwise think you
erred.

Build a real distribution rather than borrowing a normal. A month of radiosondes
is one request:

```python
d = iem_raob("KILX", "2026-07-01T00:00", "2026-08-01T00:00")
pw = [pwat_mm(g.pressure_mb.values, g.dwpc.values) for _, g in d.groupby("validUTC")]
```

`pwat_mm` agrees with `metpy.calc.precipitable_water` to <1 mm. 27 years x 3
stations is ~81 requests and a few minutes. The Wyoming CGI endpoint has moved
and 404s; `end` must be strictly later than `start`.

**Do not quote a model domain maximum as an environmental value.** In the source
event raw PWAT reached 3.50 in, but only 104 of 659,984 grid-hours exceeded 3.0 -
isolated points inside convective cores where the column includes condensed
water. Use the 99th percentile or a named inflow point.

## Trends need a significance gate

```python
t = trend_screen(years, values)     # per_decade, pvalue, significant
```

**Draw a trend line only where `significant` is True.** Of ten July metrics over
57 years at one station, only the overnight minimum temperature cleared p<0.05
(+0.48 F/decade, p=0.022); mean temperature (p=0.079) and total precipitation
(p=0.057) did not. Saying "the nights are measurably warming, and this record is
too short to call the rainfall trend" is a stronger position than a claim someone
can pick apart. OLS on annual values is a screening test, not an attribution
study.

The same discipline applies to scatter plots. An appealing hourly relationship in
the source work gave r=+0.10, p=0.35 - interpolation noise. Aggregating to four
legs showed the real signal, and the aggregate was still not reportable as a
correlation, so the leg values were published instead of a regression. Test
before you plot.

## Rainfall and flooding

**ASOS `p01i` is a running hourly accumulation repeated at each observation.**
Summing it double-counts badly - in testing, a naive sum gave 26.88 in where the
true total was 2.94.

```python
total_in = asos_hourly_precip(iem_asos("MDW", start, end))
```

Gauge identity and official flood stage come from the **warning product text**:

```python
g = nws_flood_gauges(product_ids)   # nwsli, name, flood_stage_ft, forecast_crest_ft
s = hads_river_stage("THNI2", start, end)      # HG* columns are feet
```

The IEM `nwsli.json` endpoint 404s for these IDs, and guessing a river name from
the code gets it wrong. One product covers several rivers, each with its own
stage and crest, so it must be split per segment.

Plot the **full** hydrograph, not just the current event. In the source work that
panel produced the headline: every warned gauge had already flooded four days
earlier, receded without returning to baseline, then exceeded its earlier crest.
Antecedent wetness, not rainfall rate, was the load-bearing explanation - and it
would have been missed on a single-event window.

## Figures

Load `figure-style` and call `apply_figure_style()` for deliverables. Use
`cmweather` colormaps. Two things:

- A **pale low end matters** on a field where most of the domain is
  unremarkable - 59% of an IVT domain fell below 150 kg/m/s, and a dark-low-end
  colormap buried the geography. Mask below a floor and say so in the caption.
- MetPy's `StationPlot` is broken under matplotlib >= 3.11 (`Text._get_layout`
  returns a 3-tuple). Place station text with `ax.annotate` and use MetPy only
  for wind-barb geometry - `nexrad-arco` ships a working `add_stations`.

Check for overlapping text geometrically rather than by eye, and re-render
after every fix.

## Publishing to a notebook repo

If the work becomes a notebook PR: figures embedded as `{{artifact:...}}` markers
render as broken images on GitHub. Export them to a sibling `<stem>_outputs/`
directory, rewrite the markers to relative paths, then assert zero markers remain
and that each path resolves on the pushed branch. Validate generated notebooks
with `ast.parse("".join(cell["source"]))` **and** check that no `source` entry
except the last lacks a trailing newline - bare lines are valid JSON but
concatenate into one unreadable line.
