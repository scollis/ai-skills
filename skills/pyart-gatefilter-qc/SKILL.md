---
name: pyart-gatefilter-qc
description: Quality-control weather radar gates with Py-ART GateFilter - exclude/include method semantics and their five silent traps, op='or' vs 'and' chaining, exclude_masked inversion, the wrong-shape filter after extract_sweeps, despeckle_field mutating your filter in place, marginal cost of each criterion, the canned filters (moment_based, moment_and_texture_based, temp_based, iso0_based), custom masks via exclude_gates for sector blanking and range-ring removal, and measured downstream sensitivity of rain rate and gridded reflectivity to QC choice. Triggers - gatefilter, GateFilter, gate filter, radar QC, clutter masking, exclude_below, despeckle, speckle, rhoHV threshold, velocity texture filter, non-meteorological echo, second trip, radar data quality.
---

# Gate filtering and QC in Py-ART

Measured against **Py-ART 2.2.5** on a NEXRAD VCP-212 surveillance volume
(KIWA 2026-08-20 04:14 UTC, 14 sweeps, 11,211,840 gates) and an ARM C-SAPR MDV volume
(MC3E 2011-05-20). `kernel.py` auto-loads.

**Gate filtering is not a preprocessing detail — it is the largest single source of
variance in every number Py-ART produces downstream.** Six QC recipes on one volume
gave mean rain rates from 2.28 to 4.39 mm/h. Same radar, same minute, same estimator.

## 1. What a criterion actually costs you

Cumulative exclusion, applied in order, on the 14-sweep NEXRAD volume:

| Criterion | Alone | Cumulative | **Marginal** |
|---|---|---|---|
| `exclude_invalid("reflectivity")` | 0.8380 | 0.8380 | **0.8380** |
| `exclude_below("cross_correlation_ratio", 0.85)` | 0.8820 | 0.8820 | +0.0440 |
| `exclude_below("reflectivity", 0)` | 0.8788 | 0.9035 | +0.0215 |
| `exclude_outside("differential_reflectivity", -4, 6)` | 0.8588 | 0.9076 | +0.0041 |
| `exclude_transition()` | 0.0000 | 0.9076 | +0.0000 |
| `exclude_above_toa(15000.)` | 0.5103 | 0.9077 | +0.0001 |
| `exclude_last_gates("reflectivity", 10)` | 0.0055 | 0.9077 | +0.0000 |

**83.8% of a radar volume is simply no-echo.** Everything else is a 6-point refinement.
This matters for expectations: if a QC recipe is excluding 90%, that is normal, not a
sign of an over-aggressive filter.

`exclude_transition()` is a **silent no-op on NEXRAD** — there is no
`antenna_transition` field to act on. It costs nothing and does nothing; don't count
it as clutter suppression. `exclude_above_toa` is worth 0.0001 on a 14-tilt volume;
it earns its place only when gridding with a top-of-atmosphere limit.

## 2. The five traps

All five are silent — no exception, no warning, wrong answer.

### 2.1 `include_*` on a default filter is a no-op

```python
gf = pyart.filters.GateFilter(radar)          # exclude_based=True: starts all-INCLUDED
gf.include_above("reflectivity", 20)
gf.gate_excluded.mean()                       # 0.0000  <- nothing happened
```

`include_above` merges with `op="and"`, and `and`-ing anything with an all-`False`
exclusion array leaves it all-`False`. To use the include idiom you must start from
the other end:

```python
gf = pyart.filters.GateFilter(radar, exclude_based=False)   # starts all-EXCLUDED
gf.include_above("reflectivity", 20)
gf.gate_excluded.mean()                       # 0.9655  <- as intended
```

### 2.2 Mixing `include_*` and `exclude_*` destroys the include chain

```python
gf = pyart.filters.GateFilter(radar, exclude_based=False)
gf.include_not_masked("reflectivity")               # 0.8380
gf.exclude_below("cross_correlation_ratio", 0.85)   # 0.8820 -- re-excluded
```

`exclude_*` defaults to `op="or"`, which unions its mask back over everything the
include chain had carefully kept. **Pick one idiom per filter.** Exclude-based is
the idiom used everywhere in Py-ART's own code; prefer it.

### 2.3 `exclude_masked=False` inverts your intent

```python
gf.exclude_below("cross_correlation_ratio", 0.85, exclude_masked=True)   # 0.8820
gf.exclude_below("cross_correlation_ratio", 0.85, exclude_masked=False)  # 0.0395
```

The flag decides what happens to gates where the *test field* is masked. With
`False` those gates become **included** — so a filter meant to remove low-RhoHV
noise instead admits every gate that had no RhoHV at all. There is almost no
situation where you want this.

### 2.4 A wrong-shape filter is accepted without error

The most dangerous one. A filter built on the parent radar, used on an
`extract_sweeps` child:

```python
gpar = pyart.filters.GateFilter(radar)      # (9720, 1832)
gpar.exclude_below("reflectivity", 0)
rs = radar.extract_sweeps(surv)             # (6120, 1832)
pyart.map.grid_from_radars((rs,), ..., gatefilters=(gpar,))   # NO ERROR
```

Gridded means from the same data:

| Filter | grid mean Z | grid max | fill |
|---|---|---|---|
| correct shape | **18.40** dBZ | 59.75 | 0.509 |
| parent shape (wrong) | 13.04 dBZ | 60.50 | 0.471 |
| no filter | 11.95 dBZ | 59.75 | 0.638 |

The wrong-shape result sits between "correct" and "none" and looks entirely
plausible. **Build the filter on the radar object you will actually pass.**
`assert_filter_matches(gf, radar)` in `kernel.py` catches it.

### 2.5 `despeckle_field` mutates the filter you hand it

```python
gf = pyart.filters.GateFilter(radar); gf.exclude_below("reflectivity", 0)
gf.gate_excluded.mean()                                  # 0.8820
out = pyart.correct.despeckle_field(radar, "reflectivity", size=25, gatefilter=gf)
out is gf                                                # True
gf.gate_excluded.mean()                                  # 0.8906  <- gf CHANGED
```

It calls `gatefilter.exclude_gates(...)` on your object and returns the same
reference. If you need the pre-despeckle filter (e.g. to compare recipes), pass
`gf.copy()` — `copy()` is a genuine deep copy, verified.

With `gatefilter=None` it builds its own and returns 0.8426 — a *different, weaker*
result, because it then despeckles unfiltered data.

## 3. The idiom that works

```python
gf = pyart.filters.GateFilter(radar)          # exclude-based
gf.exclude_invalid("reflectivity")            # no-echo, ~84%
gf.exclude_below("cross_correlation_ratio", 0.85)
gf.exclude_below("reflectivity", 0)
gf.exclude_outside("differential_reflectivity", -4, 6)
```

`kernel.py` ships this as named recipes:

```python
gf = qc_recipe(radar, "dualpol")        # the four above
gf = qc_recipe(radar, "velocity")       # texture-gated, for dealiasing
gf = qc_recipe(radar, "permissive")     # invalid + rhoHV 0.80 only
marginal_cost(radar, recipe="dualpol")  # the table from section 1, for your volume
```

### Method inventory

`exclude_below/above/inside/outside/equal/not_equal` (all take `inclusive=`),
`exclude_invalid`, `exclude_masked`, `exclude_transition`, `exclude_above_toa`,
`exclude_last_gates(field, n_gates)`, `exclude_gates(mask)`, `exclude_all`,
`exclude_none`, plus the `include_*` mirrors, `copy()`, and the
`gate_excluded`/`gate_included` properties.

`exclude_last_gates` takes **field first** — `exclude_last_gates(10)` raises
`TypeError: can only concatenate str (not "int") to str` from deep inside
`check_field_exists`.

## 4. The four canned filters

Measured on the NEXRAD surveillance volume:

| Filter | Runtime | Excluded | Notes |
|---|---|---|---|
| `moment_based_gate_filter` | 0.06 s | 0.9035 | `min_ncp=None` required on NEXRAD (no NCP field) |
| `moment_and_texture_based_gate_filter` | 3.05 s | 0.9188 | **must** pass field names |
| `temp_based_gate_filter` | 3.58 s | 0.8561 | needs a temperature field on gates |
| `iso0_based_gate_filter` | 3.47 s | 0.8711 | needs `height_over_iso0` |

`moment_and_texture_based_gate_filter` defaults to
`phi_field="uncorrected_differential_phase"` and raises
`KeyError: 'uncorrected_differential_phase'`. Always:

```python
pyart.filters.moment_and_texture_based_gate_filter(
    radar, phi_field="differential_phase",
    zdr_field="differential_reflectivity",
    rhv_field="cross_correlation_ratio",
    refl_field="reflectivity", wind_size=7)
```

`min_ncp` is usable on **research radars** (`normalized_coherent_power` present) and
must be `None` on NEXRAD. This is the main QC difference between the two classes.

The thermal filters need fields mapped to gates first; `add_lapse_rate_temperature`
in `kernel.py` gives a crude standard-atmosphere version for testing, but real work
should use a sounding (see `pyart-retrievals`).

## 5. Custom masks — the escape hatch

`exclude_gates(mask)` takes any boolean array shaped `(nrays, ngates)`. This is how
you do sector blanking, range-ring removal, terrain masks and anything else the
built-ins don't cover.

```python
az  = radar.azimuth["data"]; rng = radar.range["data"]
sector = ((az >= 120) & (az <= 150))[:, None] & np.ones((1, radar.ngates), bool)
ring   = np.ones((radar.nrays, 1), bool) & ((rng > 118e3) & (rng < 122e3))[None, :]
gf.exclude_gates(sector | ring)     # +2.3 points over invalid-only
```

`sector_ring_mask(radar, az_ranges=..., range_ranges=...)` in `kernel.py`.

## 6. Downstream sensitivity — report the recipe

Six recipes, one NEXRAD volume, identical downstream code:

| Recipe | Excluded | mean rain rate | gridded mean Z | grid max | grid fill |
|---|---|---|---|---|---|
| none | 0.0000 | 2.28 mm/h | 8.37 dBZ | 58.4 | 0.622 |
| invalid only | 0.8380 | 2.28 | 8.37 | 58.4 | 0.622 |
| rhoHV > 0.80 | 0.8751 | 2.93 | 8.79 | 58.4 | 0.603 |
| rhoHV > 0.95 | 0.9014 | 3.66 | 8.85 | 58.4 | 0.599 |
| `moment_based` | 0.9035 | 3.79 | 10.37 | 58.4 | 0.574 |
| `moment_and_texture_based` | 0.9188 | 4.39 | 12.40 | 58.4 | 0.453 |

Three conclusions worth carrying:

1. **Means are QC-dependent, peaks are not.** Grid maximum was 58.4 dBZ in all six.
   Any domain-mean, areal-average or accumulation must be reported with its recipe.
2. **Masking raises means.** Every criterion removes weak echo preferentially, so
   the conditional mean rises. Tighter QC is not a more conservative estimate.
3. **Coverage is the price.** The texture filter costs 17 points of grid fill for
   3 s of compute. On a case study that is fine; on a month of volumes it is not.

Echo top (highest gate above 18 dBZ) was **11.96 km in all six recipes** — some
metrics are genuinely QC-insensitive. Test yours rather than assuming.

## 7. Velocity QC is a special case

Region-based dealiasing is region *growing*, so a few noisy gates bridging two
aliased regions propagate a wrong unfolding across the connected region. On the
C-SAPR volume, filtering on gate classification alone gave **±366 m/s (22× Nyquist)**;
adding `velocity_texture < 3` — 0.7 percentage points more gates excluded — gave
±48 m/s.

Velocity QC has a much lower tolerance for leakage than dual-pol QC. Full treatment
in `pyart-velocity-dealias`.

## Verified against

Py-ART 2.2.5. Marginal exclusion, the five semantic traps and the six-recipe downstream sweep re-run on the KIWA 2026-08-20 04:14 UTC surveillance volume (14 sweeps).

Last re-run: 2026-08-26.
