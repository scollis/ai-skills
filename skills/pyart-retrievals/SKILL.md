---
name: pyart-retrievals
description: Run Py-ART's derived-product layer correctly - rain rate (est_rain_rate_z/_kdp/_a/_zkdp/_hydro, ZtoR), convective-stratiform classification on grids (conv_strat_raut, conv_strat_yuter, feature_detection, steiner_conv_strat), hydrometeor ID (hydroclass_semisupervised), temperature-on-gates via map_profile_to_gates and fetch_radar_time_profile, and products such as CAPPI, composite reflectivity, CFAD, storm-relative velocity, QVP/RQVP/EVP/SVP and VAD - with the dependency order, the sweep_number trap, and the QC sensitivity of any areal mean spelled out. Triggers - rain rate, QPE, est_rain_rate, ZtoR, Z-R, hydrometeor classification, hydroclass_semisupervised, hydrometeor ID, convective stratiform, steiner, conv_strat, feature detection, echo classification, CAPPI, composite reflectivity, CFAD, storm relative velocity, QVP, RQVP, EVP, SVP, VAD, wind profile, map_profile_to_gates, temperature field, sounding on gates, echo top, accumulation.
---

# pyart-retrievals

Derived products in Py-ART 2.2.5. Everything below was measured on two radar
classes: a NEXRAD WSR-88D volume (KIWA, 2026-08-20 04:14 UTC, VCP 212, 19
sweeps with split cuts, Nyquist 25.0-34.7 m/s, no `normalized_coherent_power`)
and a research C-band volume (ARM SGP C-SAPR, MC3E 2011-05-20 11:29 UTC, MDV;
17 tilts, one sweep per elevation, 120 m gates to 118 km, uniform Nyquist
16.52 m/s, NCP present, KDP and PhiDP shipped in the file).

Read `pyart-foundations` first if you have not; this skill assumes you can
read a volume, build a `GateFilter`, and know what `extract_sweeps` does.
CMAC (the ARM VAP) is a separate skill: `cmac-vap`.

## 1. The chain is the whole problem

The high-value retrievals are not standalone functions. They read fields that
other retrievals write, and when a prerequisite is absent they raise a bare
`KeyError` naming **one** missing field - never the chain. You then add that
one field, rerun, and get a `KeyError` for the next one. Budget for that loop
or short-circuit it.

Dependency order, non-negotiable:

```
attenuation           calculate_attenuation_zphi   -> specific_attenuation (+ PIA, corrected Z/ZDR)
      |
KDP                   kdp_vulpiani (or ship-supplied)-> specific_differential_phase
      |
temperature           map_profile_to_gates          -> temperature (on gates)
      |
classification        hydroclass_semisupervised     -> hydrometeor class ('hydro')
      |
QPE                   est_rain_rate_hydro           -> rain_rate
```

| Function | Needs | Fails as |
|---|---|---|
| `hydroclass_semisupervised` | Z, ZDR, RhoHV, **KDP**, **temperature mapped to gates**; `radar_freq` for anything that is not C-band | `KeyError` on whichever of KDP/temperature it reaches first |
| `est_rain_rate_hydro` | Z, KDP, **`specific_attenuation`**, **an echo-classification field** | `KeyError` naming one of them |
| `est_rain_rate_zkdp` | `alphakdp` and `betakdp` passed **explicitly** | `TypeError` from comparing to `NoneType` - the defaults are `None` |
| `calculate_attenuation_zphi` | Z, ZDR, PhiDP, plus either `fzl=` (`temp_ref='fixed_fzl'`) or a temperature field (`temp_ref='temperature'`) | `KeyError` on the temperature field |

`stage_retrieval_chain()` in this skill's sidecar runs the steps in that order
and raises up front with every missing field named at once.

Radar-class differences that bite here:

| | NEXRAD WSR-88D | Research C-band (C-SAPR) |
|---|---|---|
| KDP in file | no - you must compute it (`pyart-dualpol-phase`) | yes, `specific_differential_phase` and `differential_phase` shipped |
| `radar_freq` for `hydroclass_semisupervised` | required (S band) | can be omitted (C-band defaults) |
| `normalized_coherent_power` | absent | present - usable as `min_ncp` in `moment_based_gate_filter` |
| Sweep structure | split cuts, two sweeps per low elevation | one sweep per elevation, 17 tilts |
| Nyquist | 25.0-34.7 m/s, varies by sweep | 16.52 m/s uniform |

`calculate_attenuation_zphi` returns a **6-tuple**: `(specific_attenuation,
path_integrated_attenuation, corrected_reflectivity,
specific_differential_attenuation, path_integrated_differential_attenuation,
corrected_differential_reflectivity)`. Measured 1.3 s on the KIWA volume with
`temp_ref='fixed_fzl'`. At C band the attenuation correction is not optional
cosmetics - it is the input to the A-R estimator below.

## 2. The sweep_number trap

`composite_reflectivity` and `storm_relative_velocity` raise
`IndexError('Sweep out of range')` when handed the child of an
`extract_sweeps` call. `extract_sweeps` **preserves the original sweep
numbers**; both functions loop over `sweep_number['data']` and use those
values to slice the child's own arrays. Extract sweeps 4-8 and the functions
ask for index 8 of a 5-sweep object.

```python
sub = radar.extract_sweeps([0, 2, 4])
sub.sweep_number["data"] = np.arange(sub.nsweeps, dtype="int32")   # or reset_sweep_numbers(sub)
comp = pyart.retrieve.composite_reflectivity(sub, field="reflectivity")
```

This is the same class of bug as the other `extract_sweeps` metadata surprises
in `pyart-foundations`. It is silent until it is an `IndexError`; there is no
warning.

## 3. QPE estimators

All live in `pyart.retrieve`, all ~0.5 s on a full volume, all return a field
dict you add with `radar.add_field`.

| Estimator | Use when | Notes |
|---|---|---|
| `est_rain_rate_z` | stratiform rain, single-pol, or a sanity baseline | Z-R power law; a/b are climatological, wrong in convection and in hail |
| `ZtoR` (`pyart.retrieve.qpe`) | you want the plain Z-R conversion without the field-dict wrapper | same physics as above, lighter API |
| `est_rain_rate_kdp` | heavy rain, hail contamination, partial beam blockage | KDP is immune to attenuation and calibration bias, but noisy below ~0.3 deg/km - see the KDP magnitude table in `pyart-dualpol-phase` |
| `est_rain_rate_a` | C band, moderate to heavy rain | needs `specific_attenuation` from `calculate_attenuation_zphi`; the strongest single estimator at C band, weak at S band where attenuation is small |
| `est_rain_rate_zkdp` | blend Z at low rates with KDP at high rates | **must** pass `alphakdp=` and `betakdp=`; defaults are `None` and raise `TypeError` |
| `est_rain_rate_hydro` | you have a classification field and want the estimator chosen per gate | needs `specific_attenuation` **and** an echo-classification field; the whole chain in section 1 |

Rain rate is a gate-level quantity. Anything areal - a domain mean, a
catchment accumulation, a basin total - needs a grid and a stated QC recipe
(section 8).

## 4. Convective-stratiform classification: on grids, not radars

All four classifiers operate on a **`Grid`**, not a `Radar`. Grid first
(`pyart-gridding`), then classify. Cost spread is 50x across the four:

| Function | Measured | Character |
|---|---|---|
| `conv_strat_raut` | 0.57 s | wavelet-based, fastest |
| `conv_strat_yuter` | 1.86 s | Yuter/Houze background-difference; the default choice |
| `feature_detection` | 1.82 s | generalised Yuter, works on any field, not just Z |
| `steiner_conv_strat` | 28.0 s | the 1995 reference implementation; 15x slower than `conv_strat_yuter` for the same job |

Use `steiner_conv_strat` when you need the canonical Steiner result for
comparison with published work. Use `conv_strat_yuter` or `conv_strat_raut`
for everything else, and `feature_detection` when the field is not
reflectivity.

Arguments that matter:

- `dx`, `dy` - the grid spacing in metres. These are **not** read from the
  grid object; pass them and pass them correctly or every length scale in the
  algorithm is wrong by the ratio.
- `work_level` / `level_m` - the altitude (m) of the horizontal slice being
  classified. Pick a level below the melting layer, or you are classifying ice.
- `always_core_thres`, `bkg_rad_km`, `use_cosine` - the tuning knobs; the
  defaults are tuned to mid-latitude continental convection.

Feed the classification into `est_rain_rate_hydro`, or use it as a mask to
report convective and stratiform rain separately.

## 5. Hydrometeor ID

`hydroclass_semisupervised(radar, refl_field=..., zdr_field=...,
rhv_field=..., kdp_field=..., temp_field=..., radar_freq=...)`. Measured
6.22 s.

**It returns a `dict` of field dicts, not a field dict.** The classification
is under the `'hydro'` key:

```python
res = pyart.retrieve.hydroclass_semisupervised(radar, ...)
radar.add_field("radar_echo_classification", res["hydro"])
```

Passing `res` straight to `add_field` gives you an obscure failure inside the
field-dict validation, not a helpful message. `as_field_dict(res, key='hydro')`
in the sidecar handles both shapes.

| Code | Abbr | Meaning |
|---|---|---|
| 0 | NC | not classified |
| 1 | AG | aggregates (dry snow) |
| 2 | CR | ice crystals |
| 3 | LR | light rain |
| 4 | RP | rimed particles / graupel |
| 5 | RN | rain |
| 6 | VI | vertically oriented ice |
| 7 | WS | wet snow (melting layer) |
| 8 | MH | melting hail |
| 9 | IH/HDG | ice hail / high-density graupel |

Sanity check the output against the temperature field: RN above the 0 C level
or AG below it means the temperature mapping is wrong, not that the storm is
exotic. On the C-SAPR volume the 0 C level was at 4.02 km.

`radar_freq` is required for non-C-band radars - the membership centroids are
frequency-dependent, and omitting it on a WSR-88D silently applies C-band
centroids.

## 6. Temperature on gates

Two-step: get a profile, map it to gates.

```python
profile = pyart.util.fetch_radar_time_profile(sonde_ds, radar)   # heights + temp at radar time
tfield  = pyart.retrieve.map_profile_to_gates(temp, heights, radar)
radar.add_field("temperature", tfield)
```

**`fetch_radar_time_profile` returns RAW FILL VALUES.** It does not mask.
Feed its output straight into `map_profile_to_gates` and a fill-dominated
profile raises `ValueError: cannot reshape array of size 0` - which tells you
nothing about the cause. Mask everything below -500 first.

**A sounding stream can be entirely fill at your radar time.** On the C-SAPR
case the gridded sonde stream (`sgpgriddedsondeC1.c0`) was -9999 at all 332
levels at 11:29 UTC; the interpolated stream (`sgpinterpolatedsondeC1.c1`)
had 227 valid levels to 10.2 km for the same minute. Same site, same time,
one usable and one not. Check coverage at the radar time before you trust a
stream, and check it per-time - a stream that worked an hour earlier can be
empty now.

`map_temperature_to_gates()` in the sidecar does the masking and raises a
message that names the valid-level count.

A constant-lapse-rate temperature (`crude_temperature_field()`) is fine for
getting the chain to run end-to-end while you debug. It is not fine for
publication: it has no melting-layer structure, so wet-snow and melting-hail
classes are placed by fiat, and every QPE estimator that switches on
temperature inherits the error.

Related trap in the same family: `simulated_vel_from_profile` extrapolates
without bound above the profile top. On the C-SAPR volume 38.9% of gates sat
above the sounding top and received wind speeds up to 14080 m/s. Mask
`gate_altitude > profile_top` before using it (see `pyart-velocity-dealias`).

## 7. Products and profiles

| Function | Measured | Argument to get right |
|---|---|---|
| `create_cappi` | 1.12 s | `height=` in metres |
| `composite_reflectivity` | 0.36 s | sweep_number reset after `extract_sweeps` (section 2) |
| `storm_relative_velocity` | 0.09 s | same reset; storm motion vector |
| `create_cfad` | 0.14 s | **bin EDGES**, not `[nbins, min, max]` |
| `compute_qvp` | 0.09 s | `angle=` (elevation, deg), `hres=` (m) |
| `compute_rqvp` | 1.44 s | range-defined; `rmax=` |
| `compute_evp` | - | elevation-defined vertical profile |
| `compute_svp` | - | slanted vertical profile over a point |
| `quasi_vertical_profile` | - | **legacy.** Raises `TypeError: unhashable type: list`. Use `compute_qvp` |
| `vad_browning`, `vad_michelson` | 0.43 s | Doppler sweeps only; dealias first |
| `column_vertical_profile`, `get_field_location` | 1.05 s | the site-column extraction pair |

`create_cfad` is the sharpest of these. Its docstring says bin edges, and the
`[50, -10, 60]` triplet that most histogram APIs accept raises
`bins[0] must be monotonically increasing`. Build edges explicitly -
`cfad_edges(-10, 60, 1.0)` in the sidecar returns them.

VAD wants dealiased velocity. Folded velocity produces a wind profile that is
smooth, plausible, and wrong; see `pyart-velocity-dealias` for how badly
region-growing can fail on a research radar (the C-SAPR volume went to 22x
Nyquist with a gate-ID filter alone, and to 2.9x with velocity texture added).

## 8. Any areal mean is a QC statement

Six QC recipes were run on one KIWA volume, differing only in the gate filter
upstream of the same Z-R estimator:

| QC recipe | Gates excluded | Mean rain rate (mm/h) | p99.9 rain rate | Grid mean Z |
|---|---|---|---|---|
| none | 0.0% | 2.28 | 143.7 | 8.37 |
| invalid only | 83.8% | 2.28 | 143.7 | 8.37 |
| RhoHV > 0.80 | 87.5% | 2.93 | 169.4 | 8.79 |
| RhoHV > 0.95 | 90.1% | 3.66 | 183.9 | 8.85 |
| `moment_based_gate_filter` | 90.4% | 3.79 | 183.9 | 10.37 |
| `moment_and_texture_based_gate_filter` | 91.9% | 4.39 | 199.6 | 12.40 |

The mean rain rate spans **2.28 to 4.39 mm/h - a factor of 1.93** on identical
radar data. The echo-top p99 was 11.96 km in every recipe. That is the general
pattern: peaks and heights are robust to QC, means and accumulations are not,
because QC removes low-reflectivity gates and the mean is dominated by how
many near-zero gates survive.

Consequences:

- Never report an areal mean, a domain accumulation, or a basin total without
  naming the QC recipe alongside it. A number without its filter is not
  reproducible.
- Do not compare your accumulation to a published one unless you can match
  the filter, and expect a factor-of-two disagreement if you cannot.
- The largest single jump is `none`/`invalid only` (identical) to any RhoHV
  threshold. `exclude_invalid` on Z removes 83.8% of gates and changes nothing
  downstream, because those gates were already masked in the arithmetic.

See `pyart-gatefilter-qc` for how to build these filters and what each
criterion costs at the margin.

## 9. Plotting the products

House colormaps, from `cmweather`:

| Field | Colormap | Typical limits |
|---|---|---|
| Reflectivity, KDP, rain rate | `ChaseSpectral` | Z -20..60 dBZ; rain rate 0..50 mm/h |
| Velocity, storm-relative velocity | `balance` | symmetric about 0 at +/- Nyquist |
| RhoHV | `plasmidis` (note the spelling) | 0.7..1.0 |

```python
import cmweather  # registers the colormaps
display.plot_ppi_map("rain_rate", 0, vmin=0, vmax=50, cmap="ChaseSpectral")
```

Hydrometeor class is categorical - plot it with a discrete colormap and a
labelled colorbar using the code table in section 5, not a continuous scale.
`hydroclass_code_table()` returns the codes for building the tick labels.

## 10. Sidecar

`kernel.py` loads with this skill and defines:

| Function | Returns |
|---|---|
| `stage_retrieval_chain(radar, ...)` | dict of `{step: [fields added]}`; runs attenuation -> kdp -> temperature -> classification -> qpe and raises with **all** missing prerequisites named |
| `map_temperature_to_gates(radar, heights_m, temperature_c, ...)` | name of the temperature field added, after masking fill values below -500 |
| `crude_temperature_field(radar, surface_temp_c, ...)` | name of a lapse-rate temperature field - testing only |
| `cfad_edges(vmin, vmax, step)` | monotonic bin-edge array for `create_cfad` |
| `reset_sweep_numbers(radar)` | the radar with `sweep_number` reset to `arange(nsweeps)` |
| `check_required_fields(radar, needed, step)` | None, or `KeyError` naming every missing field |
| `as_field_dict(result, key=None)` | a single field dict from a bare dict, a named dict (`'hydro'`), or a tuple |
| `hydroclass_code_table()` | list of `(code, abbr, meaning)` for the hydrometeor classes |

## Siblings

`pyart-foundations` (reading volumes, sweep metadata, `extract_sweeps`),
`pyart-mapping` (display objects, georeferencing), `pyart-gatefilter-qc` (the
filters behind section 8), `pyart-velocity-dealias` (before VAD or
storm-relative velocity), `pyart-dualpol-phase` (KDP before classification),
`pyart-gridding` (before any convective-stratiform classifier), `cmac-vap`
(the ARM VAP that wraps much of this chain).

## Verified against

Py-ART 2.2.5. Retrieval chain, echo-classification timings and all four QPE branches re-run end to end on the KIWA 2026-08-20 04:14 UTC surveillance volume; sounding ingest against ARM sgpinterpolatedsondeC1.c1 for MC3E 2011-05-20.

Last re-run: 2026-08-26.
