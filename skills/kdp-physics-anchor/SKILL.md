---
name: kdp-physics-anchor
description: Physics-first constraints and a non-circular protocol for DESIGNING or SCORING a KDP retrieval. Carries the T-matrix-verified separability KDP = W x g(D0), the size-sensitivity exponents giving a predicted KDP-core / Z-core width ratio of 1.18 as a falsification test, verified drop-shape polynomials (Brandes 2002, Thurai & Bringi 2005) with the inversion convention, and how to measure structure scale from Z and ZDR rather than from anybody's KDP field. Read BEFORE choosing a smoothing length, window size or penalty scale, and before quoting any KDP structure statistic. Triggers - KDP retrieval design, smoothing length, window length, penalty scale, structure scale, decorrelation length, core width, forward model, rustmatrix, T-matrix, drop shape relation, axis ratio, oblateness, Brandes, Thurai Bringi, Beard Chuang, dsr_bc, self-consistency, Gourley, mass-weighted axis ratio, resolution floor, oversampling, threshold sweep, estimator circularity.
---

# KDP physics anchor

**The organising principle: all KDP is a retrieval.** A radar measures power, a
power ratio, and a phase. KDP is *defined* as half the range gradient of the
propagation differential phase, and propagation phase is itself only one term of
a measured mixture:

```
Psi_DP(measured) = Phi_propagation + delta(backscatter) + NUBF contamination + noise
```

So KDP sits two removes from anything measured. ARM's shipped
`specific_differential_phase`, Py-ART's estimators, and a disdrometer's
`specific_differential_phase_cband20c` (a T-matrix forward computation from a
measured DSD) are **all retrievals**. None is a measurement of KDP, and none can
serve as the reference that defines KDP's true spatial structure.

**The consequence for design:** you cannot recover the KDP structure scale from
the phase field, because the high-wavenumber end of the phase spectrum is exactly
where delta and NUBF live. You must anchor on Z and ZDR.

Sibling skills: `kdp-retrieval-cautionary-tale` (failure modes + acceptance
tests), `kdp-structure-priors` (published literature priors by structure class),
`pyart-dualpol-phase` (running the Py-ART estimators),
`rustmatrix-scattering` (the T-matrix library API).

---

## 1. The physics, verified numerically

Computed with rustmatrix 2.2.0, C band, water at 10 degC, Brandes 2002 shapes,
64-point table, normalized gamma PSD with mu=3.

### KDP = W x g(D0), exactly separable

`KDP / W` is **independent of Nw to 0.0%** across Nw = 1e3 to 1e5, at every D0
from 0.75 to 3.0 mm. And

```
(KDP / W) / (1 - r_mass)  =  11.55 .. 13.66     over that whole range
```

where `r_mass` is the mass-weighted mean axis ratio (v/h). So KDP is liquid
water content times mass-weighted oblateness, and the oblateness factor is a
pure function of mean drop size. This is the physical content of "KDP is the
difference between horizontal and vertical liquid water".

**Why it matters for design:** W and D0 are both obtainable from *measured* Z and
ZDR. So KDP's expected structure and amplitude can be predicted with no phase
processing at all, in a completely separate error channel from phase filtering.

### Size-sensitivity exponents (fixed Nw)

| field | exponent |
|---|---|
| Z_H | D0^**7.37** |
| K_DP | D0^**6.23** |
| W | D0^**4.00** |

**Z and KDP are BOTH exactly linear in Nw.** Two fields with identical
concentration dependence and size exponents of 7.37 and 6.23 must have
near-identical spatial structure.

### THE FALSIFICATION TEST

```
predicted KDP-core width / Z-core width  =  7.37 / 6.23  =  1.18
```

A retrieved KDP field materially broader than Z **in the same gates** is the
estimator, not the storm. Measured on ARM's shipped product at BNF: **2.0-2.5x**
in the resolved regime — i.e. roughly 2x over-broad. Run this before you believe
any KDP field, yours included.

Re-derive the exponents for your own band/temperature/shape relation with
`sensitivity_exponents()` — 7.37/6.23/4.00 are C-band, 10 degC, Brandes.

---

## 2. Measuring structure scale without circularity

Four steps, in this order. Skipping any one of them has produced a wrong answer.

### Step 1 — measure the resolution floor, never assume it

Gate spacing is not range resolution, and beamwidth is often absent from the
file. Measure the instrumental correlation from **noise gates** (`rho_HV < 0.3`,
`Z < -5 dBZ`): if the lag-1 autocorrelation is ~0, the gates are not oversampled
and any measured scale above one gate is atmosphere.

```python
floor = resolution_floor_acf(z, noise_mask, maxlag=8)   # -> {lag1, lag2, ..., verdict}
```

Measured on BNF C-SAPR2 (100 m gates, 4202 noise runs): **lag-1 acf 0.006** —
not oversampled.

### Step 2 — anchor on Z and ZDR, not on any KDP field

Z and ZDR are direct measurements with no delta term and no differentiation.
They carry the DSD field whose moments KDP also is.

### Step 3 — noise-correct the autocorrelation

A noisy field has an artificially SHORT decorrelation length: white noise
contributes only at lag 0 and depresses every other lag. Fit an exponential to
lags >= 1 and extrapolate back:

```python
decorrelation_km_noise_corrected(runs, dr_km)
# -> {'signal_fraction': .., 'L_km': .., 'valid': bool, 'reason': ..}
```

**The guard matters.** `signal_fraction > 1` is physically impossible and means
the exponential model does not describe the field — which is what a *filtered*
field looks like. The helper returns `valid=False` rather than a number.

Measured at BNF, rain gates below 0 degC:

| field | signal fraction | noise-corrected L |
|---|---|---|
| Z | 1.049 | **0.75 km** |
| ZDR | 0.560 (44% noise) | **0.98 km** |
| shipped KDP | 2.014 | **invalid — do not quote** |

The raw 1/e length of ZDR is 0.40 km; almost all of that shortening is noise.
Reporting it uncorrected understates the DSD scale by 2.5x.

### Step 4 — sweep the threshold, never use one

Core-width comparisons at a single threshold are worthless, and fail in **both**
directions:

- Fixed unmatched thresholds (KDP >= 1 deg/km vs Z >= 40 dBZ) select different
  populations and gave the right ratio for the wrong reason.
- Percentile-matched at the 98th gave ratio 1.00 and looked like a clean bill of
  health — but at the 98th and above **both** fields sit on the 2-3 gate
  resolution floor, so the ratio is floor-limited and carries no information.

```python
core_width_threshold_sweep(fieldA, fieldB, mask, dr_km, pcts=(85,90,95,98,99))
# flags floor_limited rows for you
```

Measured at BNF (shipped KDP vs Z, thresholds pooled over all sweeps):

| pct | 85 | 90 | 95 | 98 | 99 | 99.5 |
|---|---|---|---|---|---|---|
| median Z (km) | 0.40 | 0.40 | 0.30 | 0.30 | 0.30 | 0.30 |
| median KDP (km) | 1.00 | 0.80 | 0.50 | 0.30 | 0.30 | 0.20 |
| ratio | **2.50** | **2.00** | 1.67* | 1.00* | 1.00* | 0.67* |

`*` floor-limited (either median <= 3 gates). **Only the 85th and 90th are
usable**, and they give 2.0-2.5x against 1.18 predicted. Everything at the 95th
and above is measuring the gate spacing.

Note how narrow the usable window is: this comparison needs a field whose cores
span well over 3 gates, which at 100 m gates means you are testing 0.4-1.0 km
features with a 0.1 km ruler. On coarser gates the window may close entirely -
check `floor_limited` before believing any ratio. Smearing shows up in the
*flanks* of features, not the peaks.

---

## 3. Drop-shape relations — verified coefficients and the inversion trap

Both relations below return **b/a = vertical / horizontal**, i.e. **< 1 for an
oblate drop**. `rustmatrix.Scatterer(axis_ratio=...)` wants **h/v, > 1 for
oblate**. Passing them straight through gives a prolate particle, negative Zdr,
and no error. Use `to_tmatrix_axis_ratio()`.

**Brandes, Zhang & Vivekanandan (2002), Eq. (2)** — read off p. 685:

```
r = 0.9951 + 0.02510 D - 0.03644 D^2 + 0.005030 D^3 - 0.0002492 D^4
```

**Thurai & Bringi (2005), Eq. (7)** — their own fit to 80 m bridge 2DVD data,
rms error 0.0003 for 1.5 <= D <= 8 mm:

```
b/a = 0.9707 + 4.26e-2 D - 4.29e-2 D^2 + 6.5e-3 D^3 - 3.0e-4 D^4
```

### NAMING TRAP: `dsr_bc` is NOT Brandes

Verified by identity test: `rustmatrix.tmatrix_aux.dsr_bc` **is Beard & Chuang
(1987)** (max|diff| = 0.00e+00 against their polynomial), not Brandes despite the
initials. Against Brandes it differs by up to **0.043 in axis ratio at 6 mm**.
The library ships no Brandes relation — supply it with `axis_ratio_func`.

All these polynomials go negative if extrapolated (Brandes crosses zero near
10.7 mm), so `1/r` diverges and then flips sign, panicking the T-matrix core.
`to_tmatrix_axis_ratio()` clamps at 8 mm.

---

## 4. Self-consistency relations are a fallback, not the anchor

If you cannot run a forward model, the C-band self-consistency relation is
[Aldana et al. 2025](https://doi.org/10.5194/amt-18-793-2025) Eq. (1), whose
coefficients originate in
[Gourley et al. 2009](https://doi.org/10.1175/2008JTECHA1152.1):

```
KDP_sc = z_H x 1e-5 x (a1 + a2 Zdr + a3 Zdr^2 + a4 Zdr^3)
z_H = 10^(0.1 Z_H) in mm^6 m^-3,  Zdr in dB
a1 = 6.78, a2 = -2.65, a3 = 0.562, a4 = -0.0624
```

Three limits that must travel with any result using it:

1. **It is CUBIC in ZDR.** A 1 dB ZDR offset moves the polynomial from 4.63 to
   6.78 — a 46% error in KDP. **Calibrate ZDR before using this at all.**
2. The polynomial **goes negative above ZDR = 4.87 dB**.
3. The coefficients are fitted to **Finnish summer DSDs** (Leinonen et al. 2012,
   June-September 2014-2019). Applying them elsewhere is a climatology transfer.

Prefer a forward model with an explicit drop-shape relation (section 3) — it
makes the assumptions visible and is not tied to one climatology.

---

## 5. Reference numbers (BNF C-SAPR2)

Site-specific; re-measure elsewhere. 11 curated RHIs, az 210.17 deg, 100 m gates,
rain gates `rho_HV > 0.95`, `Z > 5 dBZ`, below the sonde 0 degC level.

| quantity | value |
|---|---|
| range resolution floor | ~0.1 km (gates not oversampled) |
| Z decorrelation | 0.75 km |
| ZDR decorrelation (noise-corrected) | 0.98 km |
| Z-core median width (85th pct) | 0.30 km |
| sigma_Phi per gate | ~1.8 deg |

**Design consequence:** the DSD field varies on **0.75-1.0 km** along range. A
smoothing scale of 4.66 km — as was once inherited into a penalty term — is ~5x
longer than the field it is smoothing.

### Datastream facts worth not rediscovering

- `differential_phase` and `uncorrected_differential_phase` have **identical**
  gate-to-gate SD (2.572 deg) and identical lag-1 acf (0.4971), differing only by
`differential_phase` and `uncorrected_differential_phase` are **raw with an offset applied, NOT unfolded**. They have identical gate-to-gate SD (2.572 deg) and identical lag-1 acf (0.4971), differing only by a smooth offset, and no filtering or delta removal has been done. The absence of wraps in the `hi_kdp` RHIs is NOT evidence of unfolding: those files are `sapr2cfr-1.7.1`, whose system phase sits at -137.65 deg on a +/-180 branch with ~8 sigma of headroom, so they simply never reach the cut. The **>=1.10 processor stream is different** - system phase +9.75 deg on a 0/360 branch, ~2 sigma of headroom, a median 5.9% of rays folded and up to 81.2%. Survey of 359 volumes found **0 pre-unfolded**. Always unfold; never infer 'already unfolded' from an absence of wraps.
- `reflectivity` is **not thresholded** — every gate including pure noise carries
  a number. Apply your own QC.
- **ZDR is suspect**: median 0.18 dB inside Z >= 40 dBZ rain gates, where rain
  should give 1-3 dB. Undiagnosed — offset or mixed phase. This blocks section 4.

---

## 6. Checklist before writing retrieval code

- [ ] Smoothing length stated in km and compared against 0.75-1.0 km (or the
      locally measured DSD scale), not inherited
- [ ] Resolution floor measured from noise gates, not assumed from gate spacing
- [ ] Structure claims anchored on Z/ZDR, never on a KDP field
- [ ] Any decorrelation length noise-corrected, with the `signal_fraction <= 1`
      guard honoured
- [ ] Core-width comparison run as a threshold SWEEP with floor flagging
- [ ] Output tested against the 1.18 width-ratio prediction
- [ ] Drop-shape relation named, and inverted before reaching the T-matrix
- [ ] ZDR calibration settled before any self-consistency constraint is trusted
- [ ] `kdp-retrieval-cautionary-tale` acceptance tests run on the actual output
