---
name: kdp-structure-priors
description: Physical priors for the SHAPE, SIZE, AMPLITUDE and SIGN of KDP structures in storms - KDP columns above the melting level, KDP cores and feet near it, dendritic-growth-layer bands, melting-layer backscatter phase, and negative KDP aloft - with the published numbers, the artifacts that imitate each structure, and helpers to measure feature width, decorrelation length and column depth on a retrieved field. Read BEFORE choosing a smoothing length, window size, sign prior or self-consistency constraint for a KDP estimator, and when interpreting a KDP map. Triggers - KDP structure, KDP column, KDP core, KDP foot, specific differential phase column, updraft signature, downburst precursor, dendritic growth layer KDP, negative KDP, ice alignment, backscatter differential phase, delta, non-uniform beam filling, NUBF, smoothing window length, phase_proc_lp window_len, kdp_vulpiani windsize, kdp_maesaka Clpf, KDP benchmark, Reimel Kumjian known-truth, Aldana benchmarking.
---

# KDP structure priors

Companion to **`kdp-retrieval-cautionary-tale`**, which supplies the acceptance tests and the
failure log. This skill supplies the *physics targets* those tests are scored against: what KDP
objects exist in storms, how deep, how wide, how strong, what sign, and which artifacts imitate
each one. Load both before tuning an estimator.

**The one-line reason this matters.** Every KDP estimator is a differentiator plus a smoother, so
its window length is a claim about the smallest real structure in the field. Published defaults
encode claims that are wrong by an order of magnitude: on a 500 m gate C-band radar, Py-ART's
`phase_proc_lp` default `window_len = 35` is a **17.5 km** smoothing window, while the optimised
value on that radar was **5 gates = 2.5 km** ([Aldana et al. 2025](https://doi.org/10.5194/amt-18-793-2025)).
Convert every window to kilometres before you accept it — `kdp_smoothing_budget()` below.

---

## 1. The structure inventory

Numbers are from the cited papers; ranges without a citation are stated as such and should not be
quoted as literature values.

### Convective KDP columns (above the 0 degC level)

- **Shape**: vertical extension of positive KDP straddling / adjacent to the updraft, reaching
  several km above the environmental melting level
  ([Loney et al. 2002](https://doi.org/10.1175/1520-0450%282002%29041%3C1179:eprsat%3E2.0.co;2);
  [Kumjian and Ryzhkov 2008](https://doi.org/10.1175/2007jamc1874.1)).
- **Size scales with the updraft**: forward-operator simulations find the size and depth of KDP
  columns directly proportional to the size and intensity of the updraft, and the columns are
  composed of large quantities of *rain*
  ([Snyder et al. 2017](https://doi.org/10.1175/jamc-d-16-0139.1)). There is **no fixed column
  scale** - do not hardcode one.
- **Companion ZDR column** extends >3 km above 0 degC; its height correlates with updraft strength
  and leads surface ZH / hail-mass increases by 10-15 min
  ([Kumjian et al. 2014](https://doi.org/10.1175/jamc-d-13-0354.1)).
- **Microphysics**: melting ice >3 mm plus shed drops <2 mm in the archetypal case
  ([Loney et al. 2002](https://doi.org/10.1175/1520-0450%282002%29041%3C1179:eprsat%3E2.0.co;2)).
- **Bulk KDP volume above the melting level** correlates with updraft mass flux, lightning flash
  rate and intense rain ([van Lier-Walqui et al. 2016](https://doi.org/10.1175/mwr-d-15-0100.1)).

### KDP cores near / below the melting level

- **Working definition in the operational literature**: an S-band enhancement at or within a few km
  below the environmental melting layer; [Kuster et al. 2021](https://doi.org/10.1175/waf-d-21-0005.1)
  analyse 81 downbursts and profile core maximum, median and *size* against height relative to the
  melting layer. A commonly quoted threshold from that work is **KDP >= 1.0 deg/km** near or within
  3 km below the melting layer.
- **Time scale**: cores evolve slowly, typically longer than 15 min, so 5-min volumetric updates
  resolve them ([Kuster et al. 2021](https://doi.org/10.1175/waf-d-21-0005.1)). Contrast with
  ice-alignment layers aloft, which reorient in ~10 s.
- **Prevalence**: descending KDP cores in 85% of 53 automatically tracked downbursts, with KDP at
  and 1 km below the freezing level among the strongest composite signals
  ([Gibson and Carlin 2025](https://doi.org/10.1175/waf-d-24-0222.1)); KDP drops precede ~95% of
  167 QLCS mesovortices ([Kuster et al. 2024](https://doi.org/10.1175/waf-d-23-0144.1)).
- **KDP foot** at low levels in supercells, introduced with the ZDR shield
  ([Romine et al. 2008](https://doi.org/10.1175/2008mwr2330.1)).
- **Diagnostic quantity is the vertical GRADIENT** as much as the peak - a scale-dependent smoother
  distorts the gradient even where it reproduces the peak.

### Hail cores

KDP keeps usable rain information inside hail: R(KDP) matched gauges to within 10% in a rain-hail
mixture ([Aydin et al. 1995](https://doi.org/10.1175/1520-0450-34.2.404)) and to ~40 mm through a
severe hailstorm ([Hubbert et al. 1998](https://doi.org/10.1175/1520-0450%281998%29037%3C0749:ccprmf%3E2.0.co;2)),
and KDP-based rain estimation in hail is supported by melting-hail scattering theory
([Ryzhkov et al. 2013](https://doi.org/10.1175/jamc-d-13-074.1)). **Consequence:** a Z-KDP
self-consistency constraint fitted in rain will fight the true high-KDP hail core. Bound it by
hydrometeor class, not globally.

### Layers aloft - one to two orders of magnitude weaker

- **Dendritic growth / aggregation-onset bands**: KDP local maxima of only **0.15-0.4 deg/km** near
  the -15 degC isotherm, with organised regions above ~0.1-0.2 deg/km diagnostic of active dendritic
  growth; consistent with oblate ice of 0.8-1.2 mm
  ([Kennedy and Rutledge 2011](https://doi.org/10.1175/2010jamc2558.1)). Refined interpretation: KDP
  bands mark the *onset of aggregation* (high concentrations of oblate early aggregates), whereas
  ZDR bands without detectable KDP mark crystal growth - which is why the two are offset in height
  ([Moisseev et al. 2015](https://doi.org/10.1002/2015jd023884)).
- **Two-layer structure in TCs**: enhanced nonspherical ice just above the melting level and near
  8 km ([Didlake and Kumjian 2017](https://doi.org/10.1175/mwr-d-17-0035.1)).
- **Consequence:** a noise floor set to suppress convective speckle (a few tenths of a deg/km)
  **erases the entire ice-phase signal**. State the floor and justify it per regime.

### Negative KDP is signal, not error

- Vertically aligned crystals in strong electric fields: alignment layer spanning **20 km in range
  and 3 km deep**, reorienting on ~10 s time scales with lightning
  ([Caylor and Chandrasekar 1996](https://doi.org/10.1109/36.508402)).
- **|KDP| up to 0.8 deg/km in BOTH signs with ZDR near 0 dB** in convective ice
  ([Hubbert et al. 2014](https://doi.org/10.1175/jamc-d-13-0158.1)); radial ZDR / Phi_DP streaks from
  the same mechanism on simultaneous-transmit radars
  ([Ryzhkov and Zrnić 2007](https://doi.org/10.1175/jtech2034.1)).
- Canting flips horizontal-to-vertical ~7 min before the first intracloud flash, peaking 30 s before
  it ([Wang et al. 2024](https://doi.org/10.1029/2023jd039942)).
- Negative KDP also in overshooting tops at ZH 15-30 dBZ (small hail / conical graupel)
  ([Homeyer and Kumjian 2015](https://doi.org/10.1175/jas-d-13-0388.1)).
- **Consequence:** the sign prior must be altitude-conditioned. A global non-negativity constraint
  deletes the ice-alignment measurement.

### Melting layer - phase, not just KDP

Backscatter differential phase delta is a real variable carrying dominant-size information, with
maxima of **8.5 deg at X band and up to 70 deg at S band** in the melting layer - values standard
melting-layer assumptions cannot reproduce
([Trömel et al. 2013](https://doi.org/10.1175/jamc-d-13-0124.1);
[Trömel et al. 2014](https://doi.org/10.1175/jamc-d-14-0050.1)). Retrieve delta jointly rather than
filtering it away ([Otto and Russchenberg 2011](https://doi.org/10.1109/lgrs.2011.2145354);
[Reinoso-Rondinel et al. 2018](https://doi.org/10.1175/jtech-d-17-0219.1);
[Mishler et al. 2024](https://doi.org/10.1175/jamc-d-23-0204.1)).

---

## 2. Structures that are NOT real

Check these before interpreting any KDP feature.

| Apparent structure | Actual cause | Test |
|---|---|---|
| Enhancement / depression at a sharp echo edge or on an isolated cell | Cross-beam NBF; grows with range, worse at short wavelength and wide beam ([Ryzhkov 2007](https://doi.org/10.1175/jtech2003.1); [Ryzhkov and Zrnić 1998](https://doi.org/10.1175/1520-0426%281998%29015%3C0624:beotdp%3E2.0.co;2)) | Does the feature scale with range / disappear at close range? |
| Vertically stacked positive/negative KDP couplet across a gradient | Vertical NBF **bias dipole**; appeared at one radar and not a nearly collocated one ([Carlin et al. 2023](https://doi.org/10.1175/jtech-d-22-0076.1)) | Compare radars / elevations; check the Z gradient |
| Along-path bias of either sign in nonuniform rain | Slope-over-nonuniform-path bias, grows with reflectivity variation along the path ([Gorgucci et al. 1999](https://doi.org/10.1175/1520-0426%281999%29016%3C1690:sdpeit%3E2.0.co;2)) | Bin error against along-path Z variance |
| "Liquid water" signature in non-Rayleigh regimes | Unmodelled delta absorbed into KDP; has propagated into incorrect operational terminology ([Mishler et al. 2024](https://doi.org/10.1175/jamc-d-23-0204.1)) | Classify Rayleigh rain before processing |
| Range-periodic banding | Iterative estimator ringing on noisy phase (see `kdp-retrieval-cautionary-tale`) | Swap estimator on the same ray |
| Staircase / flat runs | TV-penalty solution family, piecewise constant (see `kdp-retrieval-cautionary-tale` §2 Test 3) | `steplikeness()` from that skill |

---

## 3. What the benchmarks do not cover

Do not report benchmark performance as performance on storms.

- [Aldana et al. 2025](https://doi.org/10.5194/amt-18-793-2025) (C band, 652 624 gates): **excludes
  ZH >= 50 dBZ (hail), masks the melting layer and above by discarding ranges beyond 70 km, and
  flags attenuated gates** - rain only, 20-50 dBZ. Best pairwise correlation between methods was
  only **0.65-0.66**, so published KDP *structure* statistics are partly statements about the
  estimator. The self-consistency reference shares its relation with the LP method being scored, so
  part of that method's advantage is correlated uncertainty (the authors say so).
- [Reimel and Kumjian 2021](https://doi.org/10.1175/jtech-d-20-0060.1): 1-D Gaussian synthetic KDP
  profiles in rain with S-band noise, magnitude and width varied; **no algorithm optimal across all
  conditions**, performance depends on the Phi_DP field received.
- Neither scores a column, a melting-layer core, an ice band, or a sign reversal aloft. Neither
  scores sign fidelity at all.
- Smaller windows recover more at high rain rate: a smaller window length gave higher KDP and less
  underestimation above ~100 mm/h in the Zhengzhou extreme event
  ([Li et al. 2023](https://doi.org/10.5194/hess-27-1033-2023)).

**Known gap worth exploiting:** cross-storm distributions of KDP feature *width* (horizontal /
along-beam) are essentially unpublished; depth is well documented, width is not. `kdp_segment_widths()`
below exists to let you build that distribution on your own data rather than tuning blind.

---

## 4. Helpers (`kernel.py`, auto-loaded)

```python
kdp_regime_priors()                 # the table above as a dict, per regime
kdp_regime_priors("dgl_band")       # one regime: amplitude, depth, sign, citation

# convert a filter setting into a physical claim BEFORE running anything
kdp_smoothing_budget(dr_km=0.5, window_gates=35, feature_km=2.0)
# -> {'window_km': 17.5, 'gates_per_feature': 4.0, 'window_over_feature': 8.75,
#     'verdict': 'window is 8.8x the feature you claim to resolve - oversmoothed'}

# measure the widths of supra-threshold KDP runs along each ray -> build the missing distribution
kdp_segment_widths(kdp, dr_km=0.25, thresh=1.0, min_len_km=0.5)
# -> {'n': ..., 'widths_km': array([...]), 'median_km': ..., 'p90_km': ..., 'peak': array([...])}

# along-range 1/e decorrelation length; run it on KDP and on Z in the SAME gates and compare
kdp_decorrelation_km(field, dr_km, mask=None)

# depth of a positive KDP column above the 0 degC level, per horizontal column
kdp_column_depth(kdp_col, height_km, iso0_km, thresh=0.5)
```

`kdp_segment_widths` and `kdp_decorrelation_km` accept a 2-D `(ray, gate)` array or a single ray.
Always report gate spacing, band and scan type alongside any scale you quote - the
decorrelation-ratio metric has given opposite verdicts on different radar configurations
(see `kdp-retrieval-cautionary-tale` §2 Test 2).

## 5. Checklist before shipping a KDP field

- [ ] Filter window converted to km and compared against the smallest feature claimed
- [ ] Noise floor stated per regime, and checked against the 0.1-0.2 deg/km ice-band scale if the
      field extends above the melting layer
- [ ] Sign policy altitude-conditioned, not global
- [ ] Self-consistency / Z-KDP constraint bounded to rain, not applied in hail or aloft
- [ ] delta handled explicitly (estimated or classified out), not absorbed
- [ ] NBF candidates ruled out for any edge feature or vertical couplet
- [ ] `kdp-retrieval-cautionary-tale` §2 acceptance tests run on the actual output
