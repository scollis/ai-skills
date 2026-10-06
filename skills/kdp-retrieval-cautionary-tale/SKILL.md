---
name: kdp-retrieval-cautionary-tale
description: Failure modes and physical acceptance tests for specific differential phase (KDP) retrieval from radar differential phase. Read before writing, tuning, or plotting any KDP field. Documents a real session where an oversmoothed, physically impossible KDP field passed every internal check and was only caught by a domain expert looking at one figure - plus the three one-cell tests that would have caught it first, the driver bugs that produced it, and the reasoning errors that let it survive. Triggers - KDP, specific differential phase, differential phase, PhiDP, Psi_DP, phase processing, linear programming phase, phase_proc_lp, Giangrande, KDP estimator, KDP smoothing, backscatter phase, delta, non-uniform beam filling, NUBF, melting layer sign, negative KDP, dual-pol retrieval validation, disdrometer comparison, LDQUANTS, VDISQUANTS.
---

# KDP retrieval: a cautionary tale

*Written after a session that produced a KDP field where 36% of light-rain gates
exceeded 1 deg/km — roughly two orders of magnitude above physical — and where the
agent's first instinct on seeing the figure was to check the colormap.*

**Read the acceptance tests (§2) before you write or tune anything. They cost one cell
and they are the check the whole failure turned on.**

---

## §1 What KDP is, and why that constrains the answer

KDP is one half the range derivative of propagation differential phase:

    K_DP(r) = (1/2) dPhi_DP/dr        [deg/km, r in km]

Physically it measures the **difference in liquid water content sampled by horizontal
versus vertical polarisation**. Raindrops are oblate spheroids whose oblateness
*increases with size*, so KDP is proportional to the mean drop diameter weighted by
concentration. Two consequences follow, and both are testable:

**It is a smooth function of the drop-size distribution.** A T-matrix calculation at
C band gives median KDP rising *strictly monotonically and smoothly* with median drop
diameter D0 across five orders of magnitude — from ~1e-4 deg/km at D0 = 0.5 mm to
~17 deg/km at D0 = 3.5 mm, with no plateaus and no jumps. Since D0 varies continuously
in space (sedimentation, breakup and advection forbid discontinuities at 100 m scales),
**a step-like or staircase KDP field implies a step-like D0 field, which no physical
process produces.** Step-likeness is therefore a *falsification test*, not a matter of
aesthetic preference.

**It lives where the big drops are.** KDP maxima are collocated with high reflectivity
and are *fine-scale* — comparable to the Z structure, because both derive from the same
DSD. A KDP field that is broader than the Z field in the same gates has been smeared by
the estimator.

**Two sign regimes, and they are not the same problem.** Below the freezing level the
scatterers are oblate liquid drops, KDP >= 0 physically, and Z-KDP self-consistency is a
valid relation. Above the melting layer, in electrically active storms, ice crystals
align *vertically* and **negative KDP is real signal, not noise** — the quantity of
interest, in fact. A positivity prior applied aloft erases exactly what you are looking
for; a self-consistency relation applied aloft is a rain relation used out of scope.

---

## §2 The three acceptance tests — run these FIRST, on every retrieval

None needs a truth field, a reference product, or a scattering model. Together they are
one cell. **A retrieval that fails these is wrong regardless of its RMSE against
anything.**

### Test 1 — Z-conditional amplitude (cheapest, and the one that caught the failure)

Bin retrieved KDP by reflectivity in rain gates and read the median and the tail:

```python
for lo, hi in [(5,20),(20,30),(30,40),(40,50),(50,70)]:
    m = rain & (Z >= lo) & (Z < hi)
    print(lo, hi, m.sum(), np.median(K[m]), np.percentile(K[m], 90),
          (K[m] > 1).mean())
```

**Pass:** median rises **monotonically** with Z; light rain (5-20 dBZ) sits near the
noise floor with only a small tail above 1 deg/km.

**The failing run:** median 0.581 at 5-20 dBZ, *falling* to 0.432 at 20-30, then rising
to 2.08 / 2.66 / 2.74. **Non-monotonic**, and 36.3% of 5-20 dBZ gates above 1 deg/km
where the scattering tables put KDP 1-2 orders of magnitude lower. corr(KDP, Z) was
0.408.

A non-monotonic Z-KDP median is decisive on its own: no DSD-driven quantity can do that.

### Test 2 — decorrelation-length ratio against Z

Along-range 1/e decorrelation length of KDP, divided by that of Z **in the same gates**:

**Pass:** ratio near 1. Both fields come from the same DSD.

**The failing run:** KDP 3.78 km vs Z 1.62 km, **ratio 2.33**. The cause was in the
config, not the data: the curvature-penalty scale was 4.66 km, which at 108 m gate
spacing is **43 gates** — wider than a convective core. That number had been inherited
through several sessions and *never derived from anything*.

**Caution — this metric has bitten twice.** An earlier session measured filter-based
estimators at ratio 0.49-0.57 (too *rough*) and constrained methods near 1.0, on a
different radar configuration and gate spacing. The two measurements disagree in sign and
were never reconciled. Report the gate spacing and scan type alongside any value, and do
not quote one campaign's ratio as a target for another.

### Test 3 — step-likeness

`d2_over_d1` (mean |second difference| / mean |first difference|), `frac_repeat`
(fraction of gates exactly equal to a neighbour), `n_distinct_frac`.

**Pass:** compare against the *truth's own* value, or against other estimators on the
same gates — **closer is better, not lower.** An earlier session initially read this
metric as lower-is-better and consequently rated several oversmoothed estimators as good.

**A shipped configuration once produced 84.7% of gates repeating a neighbour's exact
value, with flat runs up to 9.7 km through a supercell where Z varied by 20 dBZ.** The
cause was structural: the objective penalised **total variation** on KDP,
`|k_i - k_{i-1}|`, whose solution family is *piecewise constant*. The formulation did not
merely tolerate staircases, it **preferred** them. Switching to a second-difference
(curvature) penalty, `|k_{i+1} - 2k_i + k_{i-1}|`, prefers piecewise-linear ramps and
improved both error and peak recovery while cutting the staircase signature by an order
of magnitude.

**But do not swap blindly:** at genuine discontinuities — the melting-layer bottom — the
TV prior is measurably better and curvature *rings* past the edge. Keep both reachable.

**Step-likeness and over-smoothing are INDEPENDENT failures — do not use one to clear the
other.** On the field described in §3 the curvature prior had already fixed the staircase:
`frac_repeat` 0.022, `n_distinct_frac` 0.936, `d2_over_d1` 0.908 — a healthy-looking
step-likeness result. The *same field* failed Test 1 and Test 2 outright. A smooth field
can be smoothly wrong, and a field that passes Test 3 has told you nothing about whether
its amplitude or its scale is physical. Run all three.

### Verified output on the failing field

`kernel.py` ships all four tests. Run on the field described in §3 they give:

```
[FAIL] amplitude_vs_Z    monotonic False  frac_light_rain_above_thresh 0.3633  corr 0.4080
       Z  5-20  n= 6248  med 0.581  p90 2.531  frac>1 0.363
       Z 20-30  n=11273  med 0.432  p90 2.934  frac>1 0.394     <- median FALLS
       Z 30-40  n= 9295  med 2.076  p90 3.915  frac>1 0.653
[FAIL] scale_vs_Z        kdp 3.78 km   z 1.62 km   ratio 2.333   (dr 0.108 km)
[----] steplikeness      d2_over_d1 0.908  frac_repeat 0.022  n_distinct_frac 0.936
[PASS] sign_by_altitude  frac_neg_below 0.0000 (n=31845)  frac_neg_aloft 0.3444
```

Two decisive failures, one pass, one uninformative — in a single cell, on the field that
took a domain expert's eye to reject. Usage:

```python
res = {"amplitude_vs_Z":   kdp_amplitude_vs_z(kdp, z, rain_mask),
       "scale_vs_Z":       kdp_scale_vs_z(kdp, z, rain_mask, dr_km),
       "steplikeness":     steplikeness(kdp, np.isfinite(kdp)),
       "sign_by_altitude": sign_by_altitude(kdp, height_km, iso0_km)}
print(report(res))
```

`check_offset_invariance(solve_fn, psi)` tests the §3.4 bug class separately.

### Test 4 (if a melting-layer regime is implemented) — sign by altitude

Fraction of negative KDP, binned by height relative to the 0 C level.

**Pass:** identically 0.0000% at and below the isotherm; freely signed above, with the
transition over a stated blend depth.

---

## §3 What actually went wrong, in order

A ranked account, because the *order* is the lesson.

### 3.1 The architecture decision was silently reverted

The user had already directed a restructure away from a monolithic linear program
("start with a basic definition and look for new methods") and chosen *cheap smoother +
targeted constraints*. That work existed and had validated well.

When the user next asked for storm plots, **the agent reassembled the superseded LP** —
because it was the thing sitting in the artifact store — and spent an hour debugging a
driver against it. The user had to reject the same approach twice.

> **Rule.** After an architecture decision, the default path for any new request is the
> NEW architecture. Reaching for the superseded implementation because it is more readily
> available re-litigates a settled decision.

### 3.2 Rendering was blamed before physics was checked

Presented with a visibly wrong field, the agent tested — in this order — the colormap,
the shading mode, the ray sampling geometry, and the aspect ratio. Three cells and two
figure rebuilds. **The physics check in §2 was run only after the user said the field was
wrong**, and it returned a decisive answer in one cell.

> **Rule.** When a field looks wrong, test the *values* before the *picture*. Rendering
> artifacts and physical impossibility look identical on screen; only one of them shows
> up in a percentile table.

### 3.3 A plausible mechanism was asserted, then refuted by its own data

The agent measured adjacent-ray correlation, found KDP (0.986) *more* coherent than Z
(0.886), and concluded the visible streaking was a plotting artifact. That test was
answering the wrong question: adjacent rays at matched **gate index** in an RHI are at
matched **range**, not matched height, and a constant per-ray offset still correlates at
0.99. Correlation cannot see an offset. The right test is the **offset** (ray-median
spread and adjacent-ray jump), normalised by each field's own variability.

> **Rule.** Before trusting a diagnostic, state what it is blind to.

### 3.4 Four driver bugs, all in the caller

Every one was in the calling code, not the retrieval module — and each silently produced
a plausible-looking wrong answer:

1. **An invalid enum value swallowed by a bare `except Exception`.** `smooth_mode` was
   passed as `'curvature'`; the valid value was `'curv'`. All 32 rays reported as failed
   with no reason recorded. *Always capture exception text per unit of work.*
2. **A 3-tuple return unpacked as an array.** The floor function returned
   `(floor, kdp_hi, provenance)`.
3. **Zero-fill broke offset invariance.** `np.nan_to_num(psi, nan=0.0)` puts 0 *inside*
   the data range; those gates carried zero weight in the data term but still entered the
   phase-KDP link equality. Measured: offsetting the input phase by a constant moved
   `frac_negative` from 39% to 76%, and `psi + 1000` pinned KDP at the ceiling everywhere.
   **A KDP retrieval must be invariant to an additive phase constant — test this
   explicitly.** Fix: interpolate non-finite gates, and reference *each ray* to its own
   first weighted gate (a solver imposing `phi[0] == 0` anchors at the array origin, so a
   single sweep-wide constant is not sufficient).
4. **The hard sign bound was never passed.** Only the soft self-consistency floor was
   supplied, which makes non-negativity *economic* (a gate can buy a negative value by
   paying the slack price) rather than *structural*. Result: 0.21-0.49% of rain gates
   negative. Passing the sign bound gave exactly 0.0000% below the isotherm while
   retaining 21.6-37.7% negative aloft.

### 3.5 A metric artefact was promoted to "most robust finding"

A log-log slope against a disdrometer reference showed a 21.8x spread between estimators
and was reported to the user as the project's strongest result. It was an artefact of two
uncontrolled effects:

- **No signal floor.** Below ~0.25 deg/km both sides are noise; a log transform gives
  those gates equal leverage. Imposing the floor removed 74% of the spread.
- **Differential data loss.** A log-log fit silently discards non-positive retrievals, and
  that censoring is *not uniform*: estimators carrying a non-negativity constraint kept
  100% of their gates while unconstrained ones kept 77-79%, and the discarded gates are
  exactly the low-signal ones that flatten a slope. **The metric was rewarding the sign
  constraint, not dynamic-range fidelity.**

On common support above the floor, the spread was **1.6x** and the ranking bore little
resemblance to the original.

> **Rule.** Any ratio-like metric on a quantity that legitimately approaches zero needs a
> stated signal floor AND identical support across the things being compared. Report the
> retained n for every restricted statistic.

---

## §4 References are not truth

- **Disdrometer KDP products are forward-modelled from a DSD and carry their own bias.**
  One ARM product measured ~21% high against an independent T-matrix calculation at
  matched (Z, ZDR), with the disagreement **structured in ZDR and changing sign** (~0.5x
  at low ZDR to ~3x at high) — consistent with differing drop axis-ratio assumptions. A
  single multiplicative correction is therefore inadequate. Two co-located products
  disagreed with each other by 14-18%, which sets the floor on what any comparison can
  resolve.
- **A reference bias that varies with intensity manufactures an apparent retrieval
  trend.** Every one of ten estimators read low at high KDP; the cause was the reference,
  not the retrievals.
- **Beam geometry over a surface point is measurable, not just a caveat.** RHIs aimed
  down the disdrometer radial give the vertical profile directly. Measured there, the
  gradient was small and highly variable (significant in ~28% of profiles) and surface
  extrapolation *worsened* the bias for 8 of 12 estimators — so the geometric correction
  everyone assumes is needed could not be applied reliably.
- **The community's best C-band KDP benchmark excludes by construction** the three
  regimes this kind of work exists for: high ZDR (suppressing backscatter phase), high Z
  (hail), and the melting layer and above. It cannot evaluate constraint work at all.

---

## §5 Data-handling traps that produce wrong KDP

- **Field semantics change between datastream versions.** In one ARM version
  `differential_phase` is *propagation* phase; in the next it is *total measured* phase,
  with propagation moved to a new field name. Reading by name across versions silently
  compares different quantities. **Check `long_name`, not the variable name.**
- **Do not unwrap without measuring folds first.** One stream showed 0.000% of weather
  gates with gate-to-gate jumps > 90 deg (smooth, just offset); the other showed 2.7% —
  but those were *backscatter phase excursions in total phase*, not folds. `np.unwrap`
  cannot distinguish them, and applying it produced +-4900 deg excursions. It destroyed
  the data it was meant to repair.
- **A shipped KDP field is another retrieval, not truth.** One dataset's operational KDP
  was 34.5% negative on weather gates.
- **An incumbent that "fails on your data" may just have hardcoded field names.** A
  reported infeasibility was actually `KeyError` on a canonical field name absent from the
  datastream; aliasing three fields made it solve normally. That wrong diagnosis was used
  to justify leaving the incumbent out of every real-data comparison.
- **Regime-blend sign conventions are easy to invert.** Check whether 0 means rain or ice,
  and whether the function takes metres or kilometres, by evaluating it on a known ladder
  of heights before trusting it.

---

## §6 Before you report a KDP result

- [ ] §2 tests run, with n stated, on the actual output being reported
- [ ] Additive-phase-offset invariance verified
- [ ] Every headline number recomputed over the **full** table, not a filtered or
      truncated view — the single most repeated error in the source session was
      generalising from a partial view of data already fetched in full
- [ ] Signal floor and support stated for every ratio-like statistic
- [ ] Reference uncertainty quoted alongside any bias, so differences inside it are not
      claimed as resolved
- [ ] Figure titles checked against the numbers they assert (two false titles were caught
      only by re-reading a rendered figure)
