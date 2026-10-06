---
name: radar-cell-tracking
description: "Track convective cells in gridded weather radar volumes with tobac: feature detection, watershed segmentation and trackpy linking. Covers the tobac 1.6.3 API, multi-threshold ladders and n_min sizing, range-annulus handling, the weighted_diff no-segmented-area population and its denominator, gridder choice (spectral/NUFFT vs Barnes distance weighting) and its effect on the feature population, and verifying parameter identity across parallel tracking runs."
---

# Tracking convective cells in gridded radar with tobac

Practical guidance for building a cell-track database from gridded radar
volumes. Numbers marked *(measured)* come from a KDVN (WSR-88D) decade build:
55 cases, ~9,000 volumes, two parallel tracking lanes. Re-measure thresholds
against your own grid spacing and radar.

## tobac 1.6.3 API facts

These cost a discovery turn each if you follow older tutorials:

- `feature_detection_multithreshold(field_in, ...)` takes an **`xr.DataArray`
  directly** - not an iris cube, despite older documentation. Gridded radar
  volumes feed it without conversion.
- Signature order: `(field_in, dxy, threshold, min_num, target,
  position_threshold, sigma_threshold, n_erosion_threshold, n_min_threshold,
  min_distance, ...)`.
- `segmentation_2D(features, field, dxy, threshold, target, level, method='watershed', ...)`
  and `linking_trackpy(features, field_in, dt, dxy, dz, v_max, d_max, memory,
  stubs, time_cell_min, ...)`.
- `merge_split` is available for merger/splitter handling.
- A statistic dict passed to segmentation computes per-feature properties
  **during** segmentation, avoiding a second pass over the mask.
- `numba` absence only affects periodic-boundary calculations. For a radar
  domain set `PBC_flag='none'` and ignore the warning.

## Gridder choice sets the feature population

**The gridder is a scientific decision, not a preprocessing detail.** Feature
detection responds to the effective smoothing of the reflectivity field, so the
gridder fixes the feature population before any threshold is chosen. **A
climatology must not mix gridders across cases.**

*(measured)* Head-to-head on one case (148 volumes, identical input field, grid,
tobac parameters and worker count both ways), spectral/NUFFT interpolation
against Py-ART Barnes²:

| | spectral | Barnes² |
|---|---|---|
| throughput | 11.836 s/vol | **9.465 s/vol** |
| peak-Z loss vs polar truth | **1.6 dB** | 7.3 dB |
| median \|grad Z\|, M1 band (45-55 km) | **2.47** | 1.20 (2.05x) |
| median \|grad Z\|, S1 band (85-95 km) | **2.09** | 0.94 (2.22x) |
| median \|grad Z\|, far field (135-145 km) | **0.76** | 0.24 (3.12x) |
| interior holes | **0** | 17,328 cells |
| features, identical thresholds | 5,867 | 3,139 |

**The spectral method is ~25% SLOWER at identical settings.** It was chosen on
accuracy, not throughput. Beware quoting production rates as a comparison: a
tilt-parallelism option added *after* the benchmark took spectral to 5.9-7.0
s/volume, but the distance-weighted path was never re-run with an equivalent
optimisation, so those figures are not like-for-like.

The gradient advantage **growing with range** (2.05x -> 2.22x -> 3.12x) is the
substantive result - it is the signature of a distance-weighted radius of
influence that grows with range, smearing exactly the gradients that matter at
long range. If your science sits far from the radar, that is the argument.

Two further notes:

- A **spectral gridder needs gap-free input.** A masked field has no
  well-defined spectrum. Backfilling non-detections with a range-dependent
  minimum-detectable value gives a dense field whose low-amplitude regions are
  genuinely low - and removes the censoring boundary that would otherwise be an
  edge to ring at. The place a real discontinuity survives is the **detected-echo
  margin**, where a storm edge drops to the censored envelope in a couple of
  gates; that is a physical gradient, and the honest place to look for ringing.
- A spectral path may honestly report **partial coverage** at a height where a
  distance-weighted path claims full coverage it does not have. *(measured)* At a
  2 km level, 0.588 vs 0.999 claimed coverage; beyond ~130 km the lowest beam is
  already above 2 km. Prefer the honest number.

## Choosing the detection field

*(measured)* A **column maximum erases the gridder difference entirely** (9.1 km
effective resolution either way) because it is itself a maximum filter over all
levels. A **layer maximum over the detection layer** (1-4 km in this build)
preserves it (7.8 vs 9.1 km).

Whatever you choose, **make the code and the documentation agree** - a verdict
document describing one field while the code used another survived unnoticed
until the two were diffed, and the whole database rested on which was right.

Avoid a fixed-height CAPPI for detection unless you have checked coverage at that
height.

## Threshold ladder and `n_min_threshold`

Use a multi-threshold ladder so separate cores inside one low-threshold envelope
resolve (that is what a bow echo is). *(measured)* `[30, 35, 40, 45, 50, 55]` dBZ
with 30 dBZ as the conventional convective boundary.

**Set `n_min_threshold` at the SAMPLING scale, not an organised-convection
scale.** *(measured)* At 1 km grid spacing, 12 km² is a ~4 km disc, about three
cross-beam sample widths at 88.7 km - so a feature can never be smaller than the
radar footprint. Relax at higher thresholds where small area is a real core:
`{30:12, 35:8, 40:6, 45:4, 50:4, 55:4}`.

**Prefer the permissive ladder: it is the reversible choice.** *(measured)*
Comparing a `{30:50, ...}` ladder against `{30:12, ...}` on the same cases, 62.8%
of features at 30 dBZ sat in the band one keeps and the other rejects (85% of the
permissive lane's features were below the strict cut), and median cell lifetime
shifted 27.6 vs 32.4 min *among the cells both shared* - a lower detection floor
extends a cell's tracked life at both the growth and decay ends. The strict
population is recoverable from the permissive one by post-hoc area filtering; the
reverse needs a full re-tracking pass.

Other linking parameters, with the reasoning that generalises:

- `v_max`: set above the fastest cells you expect. *(measured)* 40 m/s for
  derecho cells running 25-35 m/s. **The failure modes are asymmetric**: too low
  *fragments* a fast cell into several short tracks, corrupting every lifetime
  statistic; too high risks spurious links that `memory=1` plus adaptive search
  suppress.
- `memory=1`: tolerate one missed volume so a cell dipping below threshold is not
  split in two.
- `stubs=3`, i.e. ~15 min at NEXRAD cadence.
- Segment the linking at temporal gaps (e.g. > 1.8x the case median cadence) so a
  data hole cuts the track rather than being linked across.

## Range annulus: filter the feature table, never mask the input

Restricting analysis to a range annulus is usually right - inside the cone of
silence the top tilt does not reach high altitudes, so echo tops there are
interpolation artefacts, and at long range the beam is high and wide enough that
features are not comparable to near-range ones. *(measured)* 20-150 km for a
+/-150 km square, whose corners reach 212 km.

**Apply it as a filter on the feature table after detection, segmentation AND
linking - never as a mask on the input field.** *(measured)* With ordering as the
only change, input-masking cost **-2.9% of features** (spurious detections off
the artificial fill edge) and **-15.2% of cells** (real cells lost where the
truncated watershed could not grow). It is wrong in both directions: it loses
real cells and invents false ones at the seam.

Filter after **linking**, not before: filtering first fragments any cell that
crosses the boundary into short-lived stubs, which the `stubs` threshold then
cuts, biasing the lifetime distribution downward. Carry `in_annulus` and
`range_from_radar_m` as columns instead.

## The no-segmented-area population - report it, do not hide it

*(measured)* With `position_threshold='weighted_diff'`, **~10-12% of features
detected at the 30 dBZ rung receive ZERO segmentation pixels** (T1 mean 10.65%
over 8 cases; T2 mean 12.10% over 10 cases) - or **1.86% across all rungs**.

**The two denominators are not interchangeable.** On one case the same data is
1.39% all-rungs and 14.9% at the 30 dBZ rung. Conflating them caused three
separate misattributions in one build. State which you mean.

*(measured)* Mechanism, established rather than assumed: `weighted_diff` places
the feature at an intensity-weighted centroid and tobac seeds the watershed from
that pixel. For the crescent-shaped low-threshold feature a squall line makes,
the centroid lands in a sub-threshold notch - 100% of affected features sit where
the field is below the segmentation threshold at their own reported position
(median 28.3-29.0 dBZ) against 0.8% of segmented features, with qualifying echo
immediately adjacent (median 3x3 max 34.4 dBZ). They also lie *farther* from
segmented higher-threshold cores (30.8 vs 20.4 grid cells), ruling out nested
competition.

**Required practice:**

- Record `ncells = 0`, **never NaN** - a NaN averages away silently.
- Carry `has_segment` (bool) and `unsegmented_reason`.
- Leave other mask-derived properties null; they are genuinely undefined.
- **Compute every area, VIL and echo-top statistic over `has_segment` rows and
  publish that denominator alongside.**

*(measured)* The population is eliminable: `position_threshold='extreme'` seeds
at the feature maximum, always inside the above-threshold region, and measures
**0.0%** at ~0.5% cost in feature count. It was **not** adopted, because the
intensity-weighted centroid is the physically meaningful storm position for
motion vectors and site-crossing statistics. Document the alternative as proof
the mechanism is understood.

Two things that do **not** fix it, both tested: annulus ordering (13.2% ->
12.45%) and the NaN fill value (bit-identical, because a dense backfilled field
leaves `fillna` almost nothing to act on).

## The unlinked-feature sentinel — exclude `cell < 0` before ANY cell-level aggregation

`linking_trackpy` assigns **`cell = -1`** to every feature it could not link into a
track (below `stubs`, isolated in time, or unmatched). *(measured)* That was **15.0% of
rows** in one build.

Grouping on `cell` without filtering pools every unlinked feature in a case into a
single fake "cell" — one per case — and any extremum over it is meaningless.
*(measured)* Doing so inflated the cell-level p99 peak reflectivity from **57.9 to 62.5
dBZ** and added 24 phantom cells to an 11,454-cell database.

```python
cells = trk[trk.cell >= 0]            # ALWAYS, before groupby('cell')
per_cell = cells.groupby(['case_id', 'cell']).agg(...)
```

Cell ids are only unique **within** a case, so always group on `(case_id, cell)`.

### `cell = -1` is the `stubs` filter, not link failure

*(measured)* Do not read the sentinel as "trackpy failed". Re-running linking from a grid
cache with **`stubs=1`** and everything else identical drops the unlinked share from
**23.39% to 0.00%** on one case (cells 635 -> 1384) and **14.42% to 0.00%** on another
(cells 893 -> 1523). **Every feature finds a partner**; `cell = -1` means the chain is
shorter than `stubs` frames and was deliberately discarded.

So the tables are defined on a population that excludes all chains shorter than `stubs`
frames, and that must be published as a denominator — *"n features retained in chains >=
3 frames"* — not left implicit.

**The rate is population-dependent, so it differs between any two case sets.**
*(measured)* 14.97% vs 24.1% between two lanes running provably identical parameters, and
3.12-44.77% between cases. Explanations tested and **refuted** as causes of the spread:

- **Rung composition** — standardising every case to the lane-wide rung mix removed none
  of the variance. (The rate *is* steeply rung-dependent, 25.4% at 30 dBZ falling
  monotonically to 7.0% at 55 dBZ, but the mix does not explain the spread.)
- **Segment fragmentation** — devastating *per segment* (89.6% unlinked in a 3-frame
  segment vs 14.5% in 60+ frame segments) but only 0.92% of features live in segments
  under 10 frames, so it explains a single extreme outlier case, not the lane rate.
- **Cadence** (rho -0.05) and **segment count** (rho 0.00) — no correlation.

The strongest correlates are **median feature area (rho +0.69)** and **features per frame
(rho +0.47)** — both storm-population properties. Note the unlinked features are *not*
systematically smaller than linked ones within a case (*(measured)* median 13 vs 13 km²):
it is chain length, not feature size, that the filter acts on.

**Practical rule: compare case sets on CELL-level statistics, not feature-level unlinked
fractions.** The cells that exist are real; only short chains are missing.

### Delivered row counts are NOT chain lengths — threshold on the chain

A range-annulus filter applied AFTER linking (the correct order — see below) still
**truncates the retained rows** of cells that cross the boundary. So the number of rows
a cell has in the delivered table is not the chain length tobac evaluated.

*(measured)* 28.1% of cells lose rows to the filter and 1,071 fall below tobac's floor of
3 on delivered rows, while the true chain length is below 3 for **zero** cells.

Thresholding on delivered rows therefore discards cells that passed the stub test.
*(measured)* A `>= 4` delivered-row cut dropped **1,091 cells (9.5%)** whose true chain
length was >= 4 (median 5, up to 32). Those cells are not a random sample: median range
span 140-146 km, with **66% within 5 km of an annulus boundary against 29% of all
cells** — i.e. the cut preferentially removes fast-moving boundary-crossers.

```python
# emit this column from the pipeline, before the annulus filter
trk["cell_rows_total"] = trk.groupby("cell")["cell"].transform("size")
# ...then threshold on it, never on the delivered count
cells = trk[(trk.cell >= 0) & (trk.cell_rows_total >= 4)]
```

### Edge-truncated lifetimes are censored, not short

Once the filter is understood, the statistic needs care too. *(measured)* 31.3% of
retained cells are edge-truncated, keeping a median 4 rows of a true 8-row chain, so
their observed lifetime understates their real one:

| treatment | median lifetime |
|---|---|
| delivered-row filter (wrong) | 32.4 min |
| all chain>=4, truncated lifetimes as-is | 29.6 min |
| **fully-observed cells only** | **31.7 min** |
| edge-truncated only (censored lower bounds) | 22.8 min |

Pooling censored with fully-observed cells biases lifetime **low**; excluding them biases
the census and the density map. Carry an `edge_truncated` flag and report the two
populations separately — the distribution *shape* is robust either way (p90 68.1 vs 69.7
min), it is the cell census and spatial statistics that move.

### A diagnostic signature worth knowing

*(measured)* A **detect/segment field mismatch** — detecting on the full field but
segmenting on a masked one — reproduces a 24.7% zero-cell population of which 96.4% lies
*outside* the analysis annulus, and it is the only configuration tested that yields **NaN**
`ncells` rather than explicit zeros. If a lane shows a case-varying share of null
segmentation, check for that mismatch first.

## Shared output directories plus glob: a structural hazard

*(measured)* One lane's finalisation script globbed a **shared** `tracks/` directory and
rewrote the other lane's tables, inferring `has_segment` from `ncells.notna()` — correct
for its own nullable convention, but the other lane used explicit zeros with no nulls, so
every row came out `True` and **the column's meaning was inverted**. It was caught,
reverted and disclosed, and the tables verified intact afterwards.

The lesson is structural, not about the script: **write lane outputs to lane-prefixed
subdirectories** (`tracks/T1/`, `tracks/T2/`) so a glob cannot reach another lane's files
at all. And never infer a convention from the data — a nullable convention and an
explicit-zero convention are indistinguishable by inspection but opposite in meaning.

## Which extreme is publishable — three figures, >20 dB apart

*(measured)* On the same 24-case database, the "maximum reflectivity" differs by more
than 20 dB depending on the object being maximised:

| object | value | verdict |
|---|---|---|
| feature-level, max over segmented pixels | 79.3 dBZ | indefensible — one bad gate |
| feature-level, p99 | 73.7 dBZ | robust to one gate, but still a *feature* extreme |
| **cell-level, p99** | **57.9 dBZ** | **the climatological maximum to publish** |

Decide which object your statistic is about before quoting an extreme, and say so.

## Verifying parameter identity across parallel runs

**Parallel tracking lanes silently diverge.** *(measured)* Five divergences were
found one at a time, each of which would have made the halves non-poolable:
the `n_min_threshold` ladder (4x at the detection rung), the vertical grid extent
and base, `v_max`, whether a range annulus was applied at all, and the fill value
fed to the detection field.

**The only reliable guard: have each lane emit its live parameter block to
`params_<lane>.json` and diff them programmatically.** A correct diff returns
only the lane label itself. Do not accept "we used the same parameters".

Corollaries:

- **Standardising on one lane's block imports its bugs along with its
  justifications.** When adopting another lane's parameters, verify the quality
  metrics that were previously clean stay clean.
- **Audit outputs on COLUMNS, not write timestamps.** A stale-module write was
  caught by checking for expected columns; a timestamp check had missed it.
- A lane-correlated data-quality difference reads, in a pooled climatology, as a
  physical difference between two storm populations. That is the failure this
  discipline prevents.

## Performance

*(measured)* **Gridding dominates; tobac is cheap.** Spectral gridding ran
5.6-11.8 s/volume while feature detection + segmentation + linking ran 1.7-30 s
**per case**.

Two consequences:

- **Cache the gridded stacks to disk, tagged with the grid spec.** Then a tobac
  parameter change is minutes, not hours. *(measured)* This absorbed the
  regridding cost of three forced re-runs, each of which would otherwise have
  cost ~8.5 h.
- Memory, not cores, binds the worker pool. Size it from live available memory,
  set `maxtasksperchild` to bound worker heap accumulation, and log system free
  memory rather than `ru_maxrss` (a high-water mark that cannot decrease, so it
  cannot evidence growth either way).

## Per-feature properties worth computing during segmentation

`ref_max`, `ref_mean`, `ref_p50/p90/p99`, `ncells` (area), `area_ge40_km2`,
`area_ge50_km2`, echo tops at 18/30/40 dBZ (max/mean/p90), VIL
(Greene & Clark: `sum 3.44e-6 * Z^(4/7) * dz`, capping Z to bound hail
contamination), plus `has_segment`, `unsegmented_reason`, `in_annulus`,
`range_from_radar_m`, `case_id` and the gridder name.

**Scope limit to state explicitly:** if only reflectivity was gridded, every
per-feature property is reflectivity-derived - including echo top and VIL - and
no wind-structure question can be answered from the track database. Gridding raw
Doppler velocity is separately inadvisable without dealiasing first.
