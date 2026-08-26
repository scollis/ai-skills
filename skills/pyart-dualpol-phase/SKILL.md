---
name: pyart-dualpol-phase
description: Select and run a KDP estimator in Py-ART with measured cost and quality (kdp_vulpiani as the working default, kdp_maesaka and kdp_schneebeli characterised, phase_proc_lp_gf documented as an upstream crash), unfold folded PhiDP before differentiating it, correct a ZDR offset and estimate the noise floor, run calculate_attenuation_zphi to produce the specific_attenuation that attenuation-based and hydrometeor-based QPE require, and decide whether to trust a research radar's shipped KDP or recompute it. Triggers - KDP, specific differential phase, kdp_vulpiani, kdp_maesaka, kdp_schneebeli, phase_proc_lp, phase_proc_lp_gf, LP solver, cvxopt infeasible, sol['x'] is None, PhiDP, differential phase, phidp unfolding, folded phidp, ZDR offset, calc_zdr_offset, calc_noise_floor, attenuation correction, calculate_attenuation_zphi, calculate_attenuation_philinear, specific_attenuation, PIA, dual-pol, dual polarisation, C-SAPR, NEXRAD dual-pol, split cut surveillance.
---

# Py-ART dual-pol and phase processing

Measured on Py-ART 2.2.5 against two radar classes: NEXRAD WSR-88D (KIWA, 2026-08-20
04:14 UTC, VCP 212 with SAILSx1, 19 sweeps, split cuts, Nyquist 25.0-34.7 m/s, no
`normalized_coherent_power`) and a research C-band (ARM SGP C-SAPR, MC3E 2011-05-20
11:29 UTC, MDV, 17 tilts one sweep per elevation, 120 m gates to 118 km, Nyquist
16.52 m/s uniform, NCP present, `differential_phase` and `specific_differential_phase`
shipped in the file). Every number below was measured on one of those two volumes.

## Read this first

| Mistake | What it costs |
|---|---|
| Reaching for `phase_proc_lp_gf` because the literature says LP is the best PhiDP method | It raises `TypeError: 'NoneType' object is not subscriptable` after ~38 s. It is an upstream bug, not your data. Use `kdp_vulpiani`. |
| Running `kdp_schneebeli` on a volume | 146-165 s **per sweep**, single-threaded - over 40 minutes for a 17-sweep volume - and the tail stays unphysical even with QC (p99 37.65 deg/km gatefiltered, 79.22 unfiltered, at S band). |
| Reading `kdp_maesaka`'s enormous valid-gate count as better retrieval | It fills the whole volume (3.96 M gates) with near-zero values: median 2e-4, p99 0.21 deg/km. Coverage is not signal. |
| Computing KDP on Doppler members of NEXRAD split cuts | Those sweeps carry velocity and spectrum width only. Dual-pol work runs on the surveillance members. |
| Differentiating folded PhiDP | Wraps become large negative jumps and inject spurious KDP. Unfold first. |
| Calling `est_rain_rate_a` or `est_rain_rate_hydro` before attenuation | They need `specific_attenuation`, which only `calculate_attenuation_zphi` (or `_philinear`) produces. Attenuation comes before QPE. |
| Trusting a shipped `specific_differential_phase` because it is in the file | On C-SAPR the shipped field and a fresh FIR recomputation have visibly different distributions. Decide deliberately - see below. |

## KDP estimator selection

Measured on the KIWA (S-band) volume unless the scope column says otherwise. Note the
scope column before comparing valid-gate counts - the denominators differ, and
`kdp_maesaka`'s 3.96 M is **every gate in the subvolume**: the variational solver
returns a value everywhere regardless of the gatefilter it was handed (verified - the
same filter excluded 91.0% of gates, and the output was still 100% finite). A large
valid-gate count from that method is fill, not retrieval.

| Function | Wall time | Scope measured | Valid gates | Median | p99 | Verdict |
|---|---|---|---|---|---|---|
| `pyart.retrieve.kdp_vulpiani` | 1.71 s | 3 surv sweeps, gatefiltered | 339 k | 0.058 | 1.19 | **Default.** Fast, physically plausible tail. |
| `pyart.retrieve.kdp_maesaka` | 17.8 s | 3 surv sweeps, gatefilter passed but filled through | 3.96 M | 0.0002 | 0.21 | Variational; over-smoothed at S-band default `Clpf`. Fills everything with near-zero. |
| `pyart.retrieve.kdp_schneebeli` (no gatefilter) | 165.0 s | **one sweep**, `parallel=False` | 173,761 | 0.3027 | 79.22 | Kalman. Effectively unusable on a full volume; tail requires post-clipping. |
| `pyart.retrieve.kdp_schneebeli` (RhoHV > 0.85, Z > 5 dBZ) | 146.0 s | **one sweep**, `parallel=False` | 84,470 | 0.1597 | 37.65 | Same method, QC'd input. Still unphysical - see the note below. |
| `pyart.correct.phase_proc_lp_gf` | 38 s to crash | 3 sweeps | - | 0.0003 | 59.5 | **Broken - see next section.** Numbers are from the instrumented run that found the bug, not a usable product. |
| Bringi-style FIR (CSU-derived, **not in Py-ART core**) | 1.6 s | full 17-sweep C-SAPR volume | 54.3 % of gates | 0.150 | 1.75 | What production VAPs use. Not importable from `pyart`. |

Notes on that table:

- Units are deg/km throughout; median and p99 are over valid (unmasked) gates.
- The two `kdp_schneebeli` rows are the same sweep with and without a gatefilter, and
  they are the reason the method is not recommended. Filtering roughly halves the
  unphysical tail (p99 79.22 -> 37.65 deg/km) and halves the median (0.3027 -> 0.1597),
  but 37.65 deg/km is still an order of magnitude above physical at S band. QC does not
  rescue this estimator; the Kalman output needs post-clipping regardless, and at
  146-165 s per sweep you pay 40+ minutes a volume for a field you then have to clip.
- The FIR row is the reason `kdp_vulpiani` is the recommendation rather than the ideal:
  a fast FIR-based estimator reaches a comparable cost (1.6 s for a whole volume) with
  a higher median and a still-plausible p99, but it lives outside Py-ART core. If you
  need FIR, you are reaching for an external package; see `cmac-vap` for the ARM
  production path.
- `kdp_vulpiani` takes a `band` argument. Set it. The default is not your radar.

**Physical sanity anchor.** At S band, a p99 above roughly 10 deg/km is unphysical -
real rain does not do that at 10 cm wavelength, and anything above it is phase noise
that survived the gatefilter. Use it as a hard gate on any KDP field before you feed it
to QPE or hydrometeor classification. `kdp_sanity()` in the sidecar applies this check
and scales the ceiling by wavelength for C and X.

## `phase_proc_lp_gf` is broken in 2.2.5

```
TypeError: 'NoneType' object is not subscriptable
```

Root cause, established by instrumenting the solver rather than inferring it: in
`pyart/correct/phase_proc.py`, `LP_solver_cvxopt` returns `sol['x'] = None` when cvxopt
reports `primal infeasible`. On the KIWA volume, 20 of 720 rays came back infeasible.
The extraction loop that follows indexes `sol['x']` without checking - there is an `XXX`
comment immediately above that loop in the source acknowledging the unguarded access.
One infeasible ray kills the whole call.

Reproduces **identically** on NEXRAD KIWA and on C-SAPR. Two radar classes, two bands,
two file formats, same failure: this is a library bug, not a property of your data.

Tested and ruled out - do not spend time on these:

| Attempted workaround | Result |
|---|---|
| Stricter QC / more aggressive gatefilter | Still infeasible rays |
| Limiting the range extent | Still infeasible rays |
| Relaxed cvxopt tolerances (`abstol`, `reltol`, `feastol`) | Still infeasible rays |
| The `glpk` solver backend | Same failure |

Use `kdp_vulpiani`. If a reviewer asks specifically for LP-processed PhiDP, the honest
answer is that the Py-ART implementation cannot complete a volume in 2.2.5.

## PhiDP: unfold before you differentiate

KDP is a range derivative of PhiDP, so any wrap in PhiDP becomes a spike in KDP.

- On the C-SAPR volume, `differential_phase` is folded: the gates carrying values below
  0 deg are the wrapped ones and need +360 deg applied before differentiation.
- Check the distribution first, not the field's `valid_min`/`valid_max` metadata -
  the attributes are frequently inherited from a template and do not describe the array.
- `unfold_phidp_field()` in the sidecar does the offset on a copy and reports how many
  gates it touched. If that count is a large fraction of the volume, your threshold is
  wrong, not the data.
- `kdp_vulpiani` and `kdp_maesaka` both accept a `phidp_field` / `psidp_field` argument.
  Point them at the unfolded copy you just made, not at the raw field.

## ZDR offset and noise floor

| Function | Module | What it is for |
|---|---|---|
| `pyart.correct.calc_zdr_offset` | `correct` | Estimates the system ZDR bias, conventionally from light rain or dry snow gates you select with a gatefilter. Subtract the offset before ZDR enters attenuation correction, hydrometeor classification, or a ZDR-dependent QPE relation. |
| `pyart.util.calc_noise_floor` | `util` | Per-sweep noise floor estimate from the reflectivity field. Use it to set a defensible lower Z bound in the gatefilter instead of a guessed constant. |

A ZDR offset of even a few tenths of a dB propagates straight into differential
attenuation and into any hydrometeor class boundary defined in ZDR. Check it once per
deployment, not once per volume.

## Attenuation, and why it comes before QPE

`pyart.correct.calculate_attenuation_zphi` returns a **six-tuple**, in this order:

```python
spec_at, pia, cor_z, spec_diff_at, pida, cor_zdr = pyart.correct.calculate_attenuation_zphi(...)
```

| Entry | Field | Notes |
|---|---|---|
| `spec_at` | `specific_attenuation` | The one downstream QPE needs. |
| `pia` | path integrated attenuation | |
| `cor_z` | corrected reflectivity | |
| `spec_diff_at` | specific differential attenuation | Can be `None`. |
| `pida` | path integrated differential attenuation | Can be `None`. |
| `cor_zdr` | corrected ZDR | Can be `None`. |

**Several entries can be `None`** depending on `temp_ref` and which optional fields you
supply. Check each for `None` before `radar.add_field(...)`; unpacking blind and adding
all six is the common failure. `attenuation_zphi_named()` in the sidecar returns a dict
with the `None` entries reported rather than silently passed on.

Requirements and cost:

- Needs a freezing level: either `fzl` with `temp_ref='fixed_fzl'`, or a gate-mapped
  temperature field with `temp_ref='temperature'`, or an iso0 field with
  `temp_ref='iso0'`. Measured at 1.3 s on the 14-sweep KIWA surveillance volume with
  `temp_ref='fixed_fzl'`.
- `a_coef`, `beta`, `c`, `d` are **band-specific** and the defaults are S-band. Override
  them for C or X band or the correction is wrong by a factor, not a percent.
- If you are sourcing the freezing level from a sounding, pick the stream deliberately.
  On the MC3E case `sgpinterpolatedsondeC1.c1` was the usable one - 227 valid levels to
  10.2 km, 0 deg C at 4.02 km - while `sgpgriddedsondeC1.c0` was -9999 fill for all 332
  levels at that time and `map_profile_to_gates` raised `cannot reshape array of size 0`
  on it. Separately, `fetch_radar_time_profile` returns the raw fill values regardless of
  stream, so mask below -500 before `map_profile_to_gates`. See `pyart-foundations` for
  the profile ingest.
- `pyart.correct.calculate_attenuation_philinear` is the simpler linear-in-PhiDP
  alternative; use it when you have no reliable freezing level.

**Ordering.** `pyart.retrieve.est_rain_rate_a` and `est_rain_rate_hydro` both require
`specific_attenuation` in the radar object, and `est_rain_rate_hydro` additionally
requires an echo classification. So the chain is: gatefilter -> unfold PhiDP -> KDP ->
attenuation -> classification -> QPE. Getting that order wrong produces a `KeyError`
that looks like a missing-field problem and is actually a sequencing problem. QPE itself
is `pyart-retrievals`.

## NEXRAD versus research radar

| | NEXRAD WSR-88D (KIWA) | Research C-band (C-SAPR) |
|---|---|---|
| Sweep structure | 19 sweeps, VCP 212, split cuts - surveillance and Doppler members at the low elevations | 17 tilts, 0.75-42.0 deg, **one sweep per elevation**, no split cuts |
| Sweeps usable for dual-pol | The 14 surveillance members | All 17 |
| `normalized_coherent_power` | Absent | **Present** - usable as an extra gatefilter criterion |
| PhiDP shipped | Yes | Yes, and **folded** |
| KDP shipped | No | **Yes** (`specific_differential_phase`) |
| Nyquist | 25.0-34.7 m/s, varies by sweep | 16.52 m/s uniform |
| Band for `kdp_vulpiani` / attenuation coefficients | S | C |

The single most common cross-class error is carrying S-band assumptions - band argument,
attenuation coefficients, the 10 deg/km sanity ceiling - onto a C-band research volume,
or assuming a research radar's one-sweep-per-elevation geometry has split cuts to
select from.

## Shipped KDP versus recomputed KDP

A research file that ships `specific_differential_phase` has already made processing
decisions you cannot see. On the C-SAPR volume, recomputing with a FIR estimator gave a
median of 0.150 deg/km over 54.3 % of gates, and a visibly different distribution from
the field shipped in the MDV. Neither is automatically right.

How to decide:

1. Run `kdp_sanity()` on both. If the shipped field has an unphysical tail for its band,
   recompute.
2. Ask whether the shipped field's masking matches the gatefilter you are about to use
   for everything else. A shipped KDP masked under different QC will not co-register
   with your Z and ZDR, and any pixel-wise combination (ZKDP rain rate, hydrometeor
   classification) is then comparing different gate populations.
3. If you recompute, keep both fields in the radar object under distinct names and say
   in the output metadata which one the products used. Overwriting the native field is
   how provenance gets lost.
4. For reproducing an ARM product exactly, the shipped field is not the reference either
   - the VAP recomputes. See `cmac-vap`.

## Sweep selection

Dual-pol work runs on the **surveillance** members of split cuts. On the KIWA VCP 212
volume that is 14 of the 19 sweeps; the Doppler members duplicate the low elevations
with velocity and spectrum width only, and a KDP call that includes them either fails on
the missing PhiDP or returns a masked sweep that quietly halves your coverage
statistics.

After `radar.extract_sweeps(...)`, `sweep_number` is **not** renumbered. Several
downstream products (`composite_reflectivity`, `storm_relative_velocity`) index by
`sweep_number` and raise `IndexError` on a subset volume. Renumber after extracting -
see `pyart-foundations` for the fix.

Research volumes with one sweep per elevation need no selection; extract by elevation
range only if you have a reason to.

## The gatefilter dominates KDP quality

KDP is a derivative, so it amplifies whatever noise the gatefilter left behind. The
marginal contributions measured on the KIWA volume:

| Criterion added | Cumulative gates excluded | Marginal |
|---|---|---|
| `exclude_invalid(reflectivity)` | 83.8 % | 83.8 pts |
| `exclude_below(rhoHV, 0.85)` | 88.2 % | 4.4 pts |
| `exclude_below(reflectivity, 0 dBZ)` | 90.35 % | 2.15 pts |
| `exclude_outside(ZDR, -4, 6)` | 90.76 % | 0.41 pts |

Everything after the RhoHV threshold is decoration for KDP purposes. Build the filter
deliberately - `pyart-gatefilter-qc` has the full marginal-value analysis, the
`moment_based_gate_filter` field-name traps, and the research-radar `min_ncp` option
that NEXRAD cannot use.

## Plotting

House convention, `cmweather` colormaps:

| Field | Colormap |
|---|---|
| Reflectivity, KDP, rain rate | `ChaseSpectral` |
| Velocity | `balance` |
| RhoHV (`plasmidis` - note the spelling) | `plasmidis` |

Plot KDP with symmetric limits around zero (`vmin=-1, vmax=4` is a reasonable S-band
start given a measured p99 of 1.19 deg/km) and always plot the gatefilter-masked field,
not the raw retrieval. Mapping, projections and multi-panel layout are
`pyart-mapping`; gridded KDP is `pyart-gridding`.

## Sidecar helpers

Loaded into the kernel when this skill is loaded:

| Function | Returns |
|---|---|
| `kdp_with_fallback(radar, gatefilter, method=...)` | KDP dict plus aux outputs and timing; refuses the LP path and routes to `kdp_vulpiani`. |
| `kdp_sanity(kdp_dict, band=...)` | Percentile summary and a physical-plausibility verdict against the band ceiling. |
| `attenuation_zphi_named(radar, ...)` | The six-tuple as a named dict, with `None` entries reported. |
| `unfold_phidp_field(radar, ...)` | An unfolded copy of the PhiDP field plus the count of gates offset. |

## Related skills

`pyart-foundations` (IO, sweep geometry, `sweep_number` renumbering, profile ingest),
`pyart-gatefilter-qc` (the filter this skill depends on), `pyart-velocity-dealias`,
`pyart-mapping`, `pyart-gridding`, `pyart-retrievals` (QPE and classification consuming
`specific_attenuation` and KDP), `cmac-vap` (the ARM production chain).

## Verified against

Py-ART 2.2.5, cvxopt 1.3.2. KDP timings and percentiles re-run on KIWA 2026-08-20 04:14 UTC; the phase_proc_lp_gf infeasible-ray crash reproduced on both KIWA and ARM SGP C-SAPR MC3E 2011-05-20 11:29 UTC.

Last re-run: 2026-08-26.
