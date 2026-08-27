---
name: rustmatrix-spectra
description: Simulate Doppler and polarimetric radar spectra with rustmatrix.spectra (Stephen Nesbitt, UIUC) - SpectralIntegrator on a velocity grid, fall-speed presets, Gaussian and Zeng-2023 inertial turbulence, beam broadening, receiver noise, HydroMix multi-species spectra, and pattern-times-scene integration via BeamIntegrator with Gaussian/Airy/tabulated beams. Carries the corrected up-looking sign convention, measured validity limits of every preset, and the noise-bias SNR law. Triggers - Doppler spectrum simulation, spectral polarimetry, sZdr, spectral differential reflectivity, sKdp, srho_hv, Doppler velocity bins, fall speed, terminal velocity, turbulence broadening, spectral broadening, beam broadening, cloud radar spectra, vertically pointing radar, profiler simulation, Ka-band W-band spectra, bimodal spectrum, rain snow spectral separation, antenna pattern weighting, sidelobe contamination, BeamIntegrator, radar forward model spectra.
---

# rustmatrix.spectra — Doppler & polarimetric spectra

The spectra engine in `rustmatrix` has **no pytmatrix analogue** — it is
original work by **Prof. Stephen W. Nesbitt** (Climate, Meteorology &
Atmospheric Sciences, University of Illinois Urbana-Champaign), built out of
his ATMS 410 Radar Meteorology teaching material and the textbook *Radar
Meteorology: A First Course* (Rauber & Nesbitt, 2018, Wiley).

- Repo: <https://github.com/swnesbitt/rustmatrix> · Docs:
  <https://rustmatrix.readthedocs.io>
- DOI: [10.5281/zenodo.20077529](https://doi.org/10.5281/zenodo.20077529)
- Companion: [**myPSD**](https://github.com/swnesbitt/myPSD), Nesbitt's
  interactive radar-simulation frontend driven by `rustmatrix`.

Cite as: Nesbitt, S. W., *rustmatrix: Rust-backed T-matrix scattering for
nonspherical hydrometeors*, v2.2.0, doi:10.5281/zenodo.20077529.

For the underlying scattering layer (`Scatterer`, `PSDIntegrator`,
`HydroMix`, conventions, the axis-ratio foot-gun), load the companion skill
**`rustmatrix-scattering`** first — everything here assumes a tabulated
`Scatterer` or `HydroMix` already exists.

## What a spectrum is here

A radar Doppler spectrum distributes backscattered power across
line-of-sight velocity. `SpectralIntegrator` builds it by mapping each
diameter in the PSD to an expected velocity

```
v_exp(D) = v_t(D) + w
```

and smearing it with a Gaussian kernel of width
`sigma_eff = sqrt(sigma_turb(D)^2 + sigma_beam^2)`, then weighting by the
polarimetric scattering matrices at that diameter. The output is
per-velocity-bin `S` and `Z` matrices, from which the spectral observables
`sZ_h`, `sZ_v`, `sZ_dr`, `sKdp`, `srho_hv`, `sdelta_hv`, `sLDR` follow.

The physics that makes this worth doing: **species separate in velocity space
even when they are indistinguishable in the bulk observables.** A rain +
rimed-ice mixture can have one bulk Zdr while `sZ_dr` crosses that value
twice, and `srho_hv` dips only in the bins where the two populations overlap.

## Minimum working example

```python
import numpy as np
from rustmatrix import Scatterer, psd, SpectralIntegrator, spectra
from rustmatrix.refractive import m_w_10C
from rustmatrix.tmatrix_aux import (wl_Ka, K_w_sqr, dsr_thurai_2007,
                                    geom_vert_back, geom_vert_forw)

lam = wl_Ka
s = Scatterer(wavelength=lam, m=m_w_10C[lam], Kw_sqr=K_w_sqr[lam])
ig = psd.PSDIntegrator()
ig.D_max, ig.num_points = 8.0, 64
ig.axis_ratio_func = lambda D: 1.0 / dsr_thurai_2007(min(D, 8.0))
ig.geometries = (geom_vert_back, geom_vert_forw)
s.psd_integrator = ig
ig.init_scatter_table(s)
s.psd = psd.GammaPSD(D0=1.5, Nw=8e3, mu=3)

si = SpectralIntegrator(
    s,
    fall_speed=spectra.fall_speed.atlas_srivastava_sekhon_1973,
    turbulence=spectra.GaussianTurbulence(0.3),
    v_min=-2.0, v_max=12.0, n_bins=512,
    w=0.0,
    geometry_backscatter=geom_vert_back,
    geometry_forward=geom_vert_forw,      # omit and res.sKdp is None
    noise=None,                            # None for validation
)
res = si.run()
```

`res.v` is (M,), `res.S_spec` (2,2,M), `res.Z_spec` (4,4,M), and each
spectral observable (M,). A `HydroMix` source instead takes
`component_kinematics={label: (fall_speed, turbulence)}` covering **every**
component, and must not also receive `fall_speed=`/`turbulence=`.

## Sign convention — the documented recipe is wrong

Positive velocity = fall direction = toward a **down**-pointing radar.

The module docstring says an up-looking profiler needs only a sign flip of
`w` and `v_bins` because the kernels are even in v. **Measured, that recipe
silently keeps 16.4% of the power** (integrated `sZ_h` 1168.43 vs 7124.10)
and returns `v_mean = +3.29` instead of `-8.16` m/s, tripping a range
warning. The kernel is even in `(v - v_exp)`, but `v_exp = v_t(D) + w` is
not — negating `w` alone leaves the fall speed positive and the whole
distribution lands off the mirrored grid.

**Negate the fall speed too:**

```python
si = SpectralIntegrator(s,
    fall_speed=lambda D: -np.asarray(vt(D), dtype=float),
    w=-w, v_bins=-v_bins[::-1], ...)
```

Verified to mirror the down-looking result **exactly** — `max|diff| = 0.0`
across `sZ_h`, `sZ_v`, `sZ_dr`, `srho_hv`, `sLDR`, `sKdp`. Equally exact and
simpler: run it down-looking and mirror the arrays yourself
(`v -> -v[::-1]`, each field `-> field[::-1]`).

## No elevation projection

`SpectralIntegrator` applies **no beam projection**. The velocity axis is
`v_t(D) + w` regardless of `geometry_backscatter`: at a 20°-elevation
geometry the measured `v_mean` is 7.839 m/s, essentially the vertical-pointing
7.800, where the physical line-of-sight value is ~2.67 m/s. The polarimetry
respects the geometry; the kinematics does not.

```python
fall_speed = lambda D: np.sin(np.deg2rad(elev)) * vt(D)   # verified 2.681 m/s at 20 deg
```

`BeamIntegrator` is different — it *does* apply cos θ about its own
boresight. Don't double-correct there.

## Fall-speed presets and their real limits

| Preset | Class | Measured behavior |
|---|---|---|
| `atlas_srivastava_sekhon_1973` | rain | Bounded, monotone; 9.65 m/s at 20 mm. **Negative below D=0.1086 mm** (-0.346 m/s at 0.05 mm) |
| `brandes_et_al_2002` | rain | **Non-monotonic inside its stated 0.1-8 mm range** (local max 9.1826 at 5.98 mm, min 9.1610 at 7.37 mm); collapses on extrapolation: 7.177 m/s at 15 mm, **0.0 at 20 mm** |
| `beard_1976(D, T, P)` | rain + density | **Not the Beard three-regime formulation** — it is Brandes × sqrt(rho0/rho), so it inherits the defect above. Equals Brandes to 7e-05 at default T/P |
| `locatelli_hobbs_1974_aggregates` | snow aggregates | — |
| `locatelli_hobbs_1974_graupel_hex` | graupel / hex plates | — |
| `power_law(a, b, D_ref, c)` | user-fitted | Factory: `a*(D/D_ref)**b + c` |

**Return shape quirk:** the presets return a shape-`(1,)` ndarray even for
scalar input (`beard_1976(2.0)` → `array([6.5477])`), so `float(vt(2.0))`
raises `TypeError: only 0-dimensional arrays can be converted to Python
scalars` under numpy 2. Index with `[0]` or use the `safe_rain_fall_speed()`
helper, which preserves the caller's rank.

**Recommendations.** Use `atlas_srivastava_sekhon_1973` for rain, wrapped as
`lambda D: np.maximum(ASS(D), 0.0)` if your D grid reaches below 0.11 mm (the
64-point default over D_max=8 starts at 0.125 mm and is safe). **Above ~8 mm
never use the Brandes-based presets** — they return values slower than a 1 mm
drop, or exactly zero, with no warning. Cite Beard (1977) for the density
correction and Brandes et al. (2002) for the sea-level curve if you use
`beard_1976`. Note `rho0 = 1.2041` is the 20 °C reference, so ICAO sea-level
gives 0.99143 — slightly *slower* than nominal.

## Turbulence

`NoTurbulence`, `GaussianTurbulence(sigma_t)`, `InertialZeng2023`, and the
`turbulence.from_params(...)` builder.

**`InertialZeng2023`'s default `L_o = 100` m switches off the size dependence
the class exists to represent.** Measured: Stokes number stays below 0.021 for
every rain diameter and every dissipation rate from 1e-4 to 1e-1, so
`InertialZeng2023(0.5, 1e-2)` returns sigma_t = 0.5000 at *every* diameter
from 0.125 to 8 mm — identical to `GaussianTurbulence(0.5)` to four decimals.
You pay extra evaluation cost for a Gaussian model.

Real size dependence needs eddy scales of order **centimetres**:

```python
# L_o that puts St = 1 at the diameter you care about
tau_p = vt(D) / 9.81
L_o = np.sqrt(tau_p**3 * eps)      # rain D=5mm: 0.0090/0.0284/0.0899 m at eps=1e-4/1e-3/1e-2
```

At `L_o = 0.03` m the small-over-large sigma_t ratio reaches **4.79**, which
no Gaussian model can reproduce. Physically: small particles couple to the
turbulent eddies, large ones lag from inertia. Its spectral fingerprint is
**skewness** (-0.51 vs -0.35 for a matched Gaussian), not width. Always print
`sigma_t(D)` at both ends of your diameter range before trusting it, and pass
`v_t_ref` = the same fall-speed callable you gave `SpectralIntegrator`
(leaving the rain default while modelling aggregates moves sigma_t(8 mm) from
0.3917 to 0.1043 m/s — the Stokes cut-off lands at the wrong diameter).

## Beam broadening

```
sigma_beam = u_h * theta_b / (2*sqrt(2*ln 2))
```

Verified to **max relative error 7.7e-06** across 20 cases — when isolated
with a near-monodisperse PSD. `beamwidth` is in **RADIANS**; passing `3.0`
for "3 degrees" inflates sigma_beam by 57× with no error.

Trying to recover sigma_beam by quadrature subtraction
(`sqrt(sigma_total^2 - sigma_intrinsic^2)`) from a *realistic* PSD spectrum
looks like a library bug — it returns exactly 0.0 for beamwidth=0.3° — but it
is the measurement that fails: the intrinsic PSD width (~0.92 m/s) swamps a
sigma_beam of 0.02-0.07 m/s and the subtraction is ill-conditioned. It is
trustworthy only when sigma_beam is a substantial fraction of the total.

## Grid sizing — the silent power loss

`v_bins` must span the full velocity range. Too narrow and you get a
`UserWarning` ("Spectral power extends beyond v_bins...") and a
plausible-looking but wrong spectrum: measured, integrated `sZ_h` fell from
427162 to 1057.7 — **99.75% of the power lost**, `collapse_to_bulk` 26 dB
low. Inside a loop with warnings suppressed there is no other signal.

**Never suppress warnings around `.run()`.** Size the grid as
`[min(v_t) - 4*sigma_eff, max(v_t) + 4*sigma_eff]` over the full
`PSDIntegrator` D grid (the built-in check uses 3 sigma; at 3.37 sigma the
width is already 0.5% low). Use `n_bins = 512` for production and keep at
least 3 bins per sigma_eff — below 0.5 bin the kernel switches to
integral-preserving delta-binning, which cost +2.7% in measured width.

## Noise

`noise=None` (default), `"realistic"`/`True`, a scalar, or an `(h, v)` tuple.

The bias on `sZ_dr` and `srho_hv` follows an **exact analytic SNR law**
(agreement 2.7e-15 dB), so thresholds can be solved rather than sampled:

| Quantity | Bias threshold | Per-bin SNR |
|---|---|---|
| `sZ_dr` | 0.1 dB | 5.8-14.6 dB (depends on true Zdr) |
| `sZ_dr` | < 0.03 dB | above ~20 dB |
| `srho_hv` | 0.01 | above ~19.9 dB |

Below 10 dB SNR the measured `sZ_dr` bias reached 5.1 dB. Noise pushes
`sZ_dr` toward 0 dB and `srho_hv` down, worst in the low-SNR spectrum tails.

**Critical trap: noise never enters `S_spec`/`Z_spec`**, so
`collapse_to_bulk()` round-trips *exactly* even with noise enabled — the
round-trip **cannot** tell you noise is on. Check `res.noise_h` /
`res.noise_v` (both 0.0 when clean). Keep `noise=None` for all validation.

Also: `realistic_noise_floor`'s wavelength argument is **ignored** —
`realistic_noise_floor(3.19)` and `(111.0)` both return 0.01. Pass `Z_dBZ=`
explicitly (`REALISTIC_NOISE_DBZ = -20` is a research-radar mid-range
default, not a per-band calibration).

## Validating a spectrum

`collapse_to_bulk()` integrates the spectrum back over velocity and returns a
Scatterer-shaped shim, so the bulk `radar.*` helpers work on it. Verified to
round-trip to **1 ulp** for both a single `Scatterer` and a `HydroMix` — Zh
agrees to 8.5e-16 relative (−3.9e-15 dB) and Zdr is bitwise equal. That is
round-off, not approximation: the quadrature is genuinely conservative.

**But never validate at `geom_vert_back`.** Vertical incidence sees a
circular cross-section, so Zdr is exactly 0.0000 dB and rho_hv exactly
1.0000 regardless of your axis-ratio function — a "perfect" round-trip proves
nothing about the polarimetric path. Use a slant or horizontal geometry, and
mind the tuple: the backscatter branch is `phi=180`, not `phi=0`. At
thet0=30, `(30,150,0,180,0,0)` gives Zdr = +0.160 dB while
`(30,150,0,0,0,0)` gives +3.964 dB — the latter is not backscatter at all.
Sanity check by sweeping thet0 0→90 with phi=180: Zdr must rise monotonically
from 0.0000 to +0.6287 dB.

## Beam pattern × scene (`spectra.beam`)

For non-uniform beams where the closed-form sigma_beam breaks down.
`GaussianBeam`, `AiryBeam`, `TabulatedBeam`, `Scene`, `BeamIntegrator`,
`marshall_palmer_psd_factory`.

**When it matters — measured.** On a homogeneous scene `BeamIntegrator`
reduces to the closed form (dZh = -0.0000 dB, dv = 7e-04 m/s), so it buys
nothing. On a heterogeneous one:

| Scene | Departure from closed form |
|---|---|
| 40 dBZ/km reflectivity gradient across a 3° beam | **+1.30 dB** Zh, **+0.50 m/s** mean Doppler |
| 20 m/s/km vertical shear | **+0.68 m/s** of width the closed form cannot see at all |
| Sharp convective edge crossing the footprint | **36.9 dB** Zh swing, 4.13 m/s in mean velocity |

**Sidelobes need an Airy beam.** A 55-dBZ cell 2.2° off boresight of a 1°
beam reads as 14.891 dBZ / +4.556 m/s under `GaussianBeam` — *identical to an
empty scene* — while `AiryBeam` gives 20.131 dBZ / +0.598 m/s. That is a
5.2 dB and 3.96 m/s error reported as a clean measurement, because Gaussian
gain at 2.2×hpbw is 1.49e-06 against Airy's 6.28e-05, a factor of 42. Use
`AiryBeam` or a measured `TabulatedBeam` whenever off-boresight
contamination is in scope, and raise `max_theta_over_hpbw` past 3 so the
sidelobes are inside the sampling cone.

**Resolution and memory.** `32x24` (the default) is within 0.009 dB and
0.003 m/s of a 96x72 reference at 1/9 the cost; go to `48x36` only when the
Doppler shift itself is the answer. The dominant array is float64 of shape
`(n_theta*n_phi, n_bins, n_D)` — the source comment's "~37 MB" understates
realistic use by two orders of magnitude: 64x48 with 512 bins and 48
diameters measured **4.0 GB** peak RSS. Budget before scaling up.

`BeamPattern.sample()` weights are **two-way (G²) and carry a sin(theta)
solid-angle factor**, so the theta=0 sample has weight exactly 0.0 and
`BeamIntegrator` skips it. Don't read `sample()[0]` as the boresight answer
(use `SpectralIntegrator` with `beamwidth=0`), and don't re-square the
weights.

## Quick reference of traps

1. **Up-looking spectrum nearly empty?** You negated `w`/`v_bins` but not the
   fall speed.
2. **Elevation ignored?** There is no projection — scale `fall_speed` by
   sin(elevation) yourself.
3. **`InertialZeng2023` behaving exactly like Gaussian?** Default `L_o=100` m;
   set it to centimetres.
4. **Hail falling slower than drizzle?** A Brandes-based preset extrapolated
   past 8 mm.
5. **Power at negative velocity?** `atlas_srivastava_sekhon_1973` below
   D=0.109 mm.
6. **99% of the power gone?** `v_bins` too narrow — read the warning.
7. **sigma_beam 57× too big?** `beamwidth` is radians.
8. **`res.sKdp is None`?** Pass `geometry_forward=`.
9. **Round-trip perfect but sZdr biased?** Noise is on; the round-trip cannot
   detect it.
10. **Zdr exactly 0 and rho_hv exactly 1?** You validated at vertical
    incidence, which tests nothing polarimetric.
11. **Sidelobe cell invisible?** `GaussianBeam` — use `AiryBeam`.
12. **4 GB of RAM gone?** `n_theta*n_phi*n_bins*n_D` float64.

## Verified against

rustmatrix 2.2.0 (PyPI ABI3 wheel), CPython 3.13, numpy 2.x, macOS arm64, 14 cores.
Spectral measurements used Ka band (8.43 mm), a 64-point `PSDIntegrator` over
D_max = 8 mm with the Thurai 2007 drop-shape relation, and `GammaPSD(D0=1.5,
Nw=8e3, mu=3)` unless stated otherwise; beam-pattern cases used a 5 km range and
the beamwidths named inline.

The preset validity limits, sign-convention result, noise-bias SNR law, and
beam-pattern departures are library properties. Memory figures and resolution
timings are machine-specific.

Last re-run: 2026-08-27.

## Acknowledgements

Every number above was measured against rustmatrix v2.2.0. The engine is
Nesbitt's original contribution and it is solid where it counts: the
spectral→bulk round-trip closes to floating-point exactness, sigma_beam
matches its closed form to 7.7e-06, the noise bias obeys an exact analytic
law, and `BeamIntegrator` reduces correctly to the closed form on a
homogeneous scene. The traps above are mostly defaults and documentation
gaps, not physics errors.
