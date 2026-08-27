---
name: rustmatrix-scattering
description: Run T-matrix scattering for nonspherical hydrometeors with rustmatrix (Stephen Nesbitt, UIUC) - single-particle Scatterer, polarimetric radar observables (Zh, Zdr, Kdp, rho_hv, delta_hv, Ai), PSDIntegrator tabulation across drop-size distributions, orientation/canting averaging, HydroMix multi-species mixtures, and the Doppler/polarimetric spectra engine. Carries the verified axis_ratio convention, measured convergence settings, and cost scaling. Triggers - rustmatrix, T-matrix, tmatrix, pytmatrix, polarimetric radar simulation, differential reflectivity, Zdr, Kdp, specific differential phase, drop shape relation, Thurai, raindrop axis ratio, PSD integration, GammaPSD, drop size distribution scattering, hydrometeor scattering, radar forward model, Mie sphere, HydroMix, Doppler spectra simulation, spectral polarimetry, fall speed, canting angle, orientation averaging.
---

# rustmatrix — T-matrix scattering for nonspherical hydrometeors

`rustmatrix` is a Rust-backed T-matrix scattering library for nonspherical
particles, developed by **Prof. Stephen W. Nesbitt** (Department of Climate,
Meteorology & Atmospheric Sciences, University of Illinois Urbana-Champaign).
It is a drop-in replacement for the numerical core of
[pytmatrix](https://github.com/jleinonen/pytmatrix) (Leinonen 2014), adding
capabilities that have no pytmatrix analogue: `HydroMix` multi-species
mixtures, a full Doppler + polarimetric spectra engine, and beam-pattern ×
scene integration.

The library grows out of Nesbitt's instructional material for *ATMS 410 —
Radar Meteorology* and accompanies the textbook *Radar Meteorology: A First
Course* (Rauber & Nesbitt, 2018, Wiley). Please credit Nesbitt's work when
you publish results built on it.

- Repo: <https://github.com/swnesbitt/rustmatrix>
- Docs: <https://rustmatrix.readthedocs.io>  ·  Rust API: <https://docs.rs/rustmatrix>
- DOI: [10.5281/zenodo.20077529](https://doi.org/10.5281/zenodo.20077529)
- Companion: [**myPSD**](https://github.com/swnesbitt/myPSD), Nesbitt's
  interactive web frontend for radar simulation, driven by `rustmatrix`.

**Cite it** (see `CITATION.cff` upstream): Nesbitt, S. W., *rustmatrix:
Rust-backed T-matrix scattering for nonspherical hydrometeors*, v2.2.0,
doi:10.5281/zenodo.20077529.

## Install

```bash
pip install rustmatrix
```

Pre-built ABI3 wheels ship for macOS (arm64/x86_64), manylinux
(x86_64/aarch64), and Windows x64 — **no Rust toolchain needed**. Verified:
the macOS arm64 wheel for v2.2.0 installs and imports with no compiler
present. Requires numpy>=1.23, scipy>=1.10.

## THE convention that will bite you first

`Scatterer(axis_ratio=...)` wants **horizontal/vertical, > 1 = oblate**.
The drop-shape relations in `tmatrix_aux` (`dsr_thurai_2007`, `dsr_pb`,
`dsr_bc`) return the **inverse** — v/h, < 1 for an oblate drop. So you must
invert them:

```python
axis_ratio = 1.0 / dsr_thurai_2007(D)   # correct — oblate, Zdr > 0
```

Verified at D=3 mm, C-band: `dsr_thurai_2007(3.0)` returns **0.8590**.
Using `1/0.8590 = 1.1642` gives **Zdr = +1.569 dB** (correct, oblate drop).
Passing `0.8590` directly gives **Zdr = -1.616 dB** — a prolate particle,
wrong sign, no error raised. This is the single most common porting bug.

> Note: upstream `docs/conventions.md` states the drop-shape relations
> report h/v (">= 1 for oblate drops"). Measured behavior is the opposite.
> The docs' *recipe* (`1.0/dsr_thurai_2007(D)`) is correct; the prose
> describing why is inverted. Trust the recipe.

**Sanity check every setup**: for rain in a horizontal backscatter geometry,
Zdr must be positive and grow with D0. If it is negative, you have the axis
ratio inverted.

## The five-line core workflow

```python
import numpy as np
from rustmatrix import Scatterer, radar
from rustmatrix.refractive import m_w_10C
from rustmatrix.tmatrix_aux import wl_C, K_w_sqr, dsr_thurai_2007, geom_horiz_back

D = 2.0                                     # equivalent-volume diameter, mm
s = Scatterer(radius=D / 2.0, wavelength=wl_C, m=m_w_10C[wl_C],
              axis_ratio=1.0 / dsr_thurai_2007(D), Kw_sqr=K_w_sqr[wl_C])
s.set_geometry(geom_horiz_back)
print(10 * np.log10(radar.Zdr(s)))          # +0.9997 dB
```

Note `radius` is a **radius** (D/2), not a diameter — and everything is in
**mm**.

## Units and geometry cheat-sheet

| Quantity | Unit |
|---|---|
| radius, diameter, wavelength | **mm** |
| reflectivity (linear) | mm⁶ m⁻³ (`10*log10` for dBZ) |
| Kdp | ° km⁻¹ |
| Ai (specific attenuation) | dB km⁻¹ |
| cross sections | mm² |
| fall speed, Doppler velocity | m s⁻¹ |
| canting_std | **degrees** |

Geometry tuples are `(thet0, thet, phi0, phi, alpha, beta)` in **degrees**:

| Preset | Drives |
|---|---|
| `geom_horiz_back` | Zh, Zdr, rho_hv, delta_hv |
| `geom_horiz_forw` | Kdp, Ai |
| `geom_vert_back` | profiler / cloud-radar spectra |

`set_geometry()` is O(1) — the T-matrix is cached on the `Scatterer` and
reused across geometries, orientations, and PSDs.

Bands (mm): `wl_S`=111.0, `wl_C`=53.5, `wl_X`=33.3, `wl_Ku`=22.0,
`wl_Ka`=8.43, `wl_W`=3.19. Use them as dict keys into `K_w_sqr` and the
refractive tables.

## Refractive index — the second gotcha

```python
from rustmatrix.refractive import m_w_0C, m_w_10C, m_w_20C, mi
m_rain = m_w_10C[wl_C]        # dicts keyed by wavelength in mm
m_snow = mi(wl_C, 0.1)        # mi is a CALLABLE: mi(wavelength_mm, density)
```

`m_w_*C` are dicts (liquid water at 0/10/20 °C). **`mi` is a function**, not
a dict — `mi(wavelength_mm, snow_density)` returns the complex index for ice
of that bulk density (g cm⁻³), so it handles snow/graupel by density.
Verified: `mi(33.3, 0.9167)` = `1.7861+0.000213j` (solid ice);
`mi(8.43, 0.3)` = `1.2168+0.000172j` (low-density snow).

> Upstream `docs/conventions.md` refers to this symbol as `m_i` and shows it
> being indexed like a dict. The installed name is `mi` and it is callable —
> `from rustmatrix.refractive import m_i` raises `ImportError`.

Also useful: `mg_refractive(m, mix)` (Maxwell-Garnett) and
`bruggeman_refractive(m, mix)` for two-phase effective media.

## Accuracy: the Mie parity gate

Setting `axis_ratio=1` drives the T-matrix into its Mie limit, where
`mie_qsca`/`mie_qext` give the closed-form answer. This is the gate the whole
library rests on, and it is worth running once in your own environment:

```python
import numpy as np
from rustmatrix import Scatterer, mie_qsca, scatter
from rustmatrix.refractive import m_w_10C
from rustmatrix.tmatrix_aux import wl_X, geom_horiz_back

r, m = 1.0, m_w_10C[wl_X]
s = Scatterer(radius=r, wavelength=wl_X, m=m, axis_ratio=1.0)
s.set_geometry(geom_horiz_back)
x = 2 * np.pi * r / wl_X
rel = abs(scatter.sca_xsect(s) - mie_qsca(x, m.real, m.imag) * np.pi * r**2)
print(rel / (mie_qsca(x, m.real, m.imag) * np.pi * r**2))   # ~6e-08
```

**Measured across a 132-point sweep** — all six bands (S/C/X/Ku/Ka/W) ×
size parameter x = 0.1 to 15, water spheres at 10 °C, **default `ddelt=1e-3`,
`ndgs=2`**:

| Band | median rel. err (σ_sca) | max rel. err (σ_sca) | max rel. err (σ_ext) |
|---|---|---|---|
| S  | 1.8e-08 | 7.7e-08 | 1.7e-09 |
| C  | 1.9e-08 | 6.9e-08 | 1.9e-09 |
| X  | 2.1e-08 | 6.3e-08 | 1.7e-09 |
| Ku | 2.4e-08 | 5.9e-08 | 1.3e-09 |
| Ka | 4.0e-08 | 5.5e-08 | 7.0e-10 |
| W  | 5.3e-08 | 6.0e-08 | 9.1e-10 |

Zero convergence failures, zero points worse than 1e-4, across the whole
sweep. **The defaults are already excellent** — tightening `ddelt` to 1e-4
or 1e-5, or raising `ndgs` from 2 to 4 or 8, changed the error by a factor of
**exactly 1.0** in a 27-case controlled sweep (S band x=0.26, X band x=5,
W band x=15). Do not reflexively tighten `ddelt`; for spheres it buys nothing
and costs time. Tighten only when a specific case actually fails to converge
(elongated particles and large size parameters are the realistic candidates).

## Cost scaling — plan before you launch

Single-particle T-matrix build+evaluate cost, measured on 14 cores (macOS
arm64), fitted over x >= 2:

```
t ≈ 2.4 ms · x^2.72          (x = 2πr/λ)
```

Measured anchors: x=0.1 → 1.6 ms; x=1 → ~2.4 ms; x=5 → 0.19 s;
x=15 → **4.9 s**. The steep exponent is the nmax growth in the solver, and it
is the dominant cost in any large job. Practical consequence: **W-band
(λ=3.19 mm) hail is expensive** — a 10 mm particle at W band is x≈9.8,
roughly 1 s per particle, so a 64-point table is a minute of compute, while
the same table at S band is milliseconds.

## PSD integration — tabulate once, evaluate many

One drop is not a radar echo. `PSDIntegrator` tabulates S(D) and Z(D) once
across the diameter range using the rayon-parallel Rust kernel, then any
number of PSD shapes evaluate from the cached table.

```python
import numpy as np
from rustmatrix import Scatterer, radar, psd
from rustmatrix.refractive import m_w_10C
from rustmatrix.tmatrix_aux import (wl_C, K_w_sqr, dsr_thurai_2007,
                                    geom_horiz_back, geom_horiz_forw)

s = Scatterer(wavelength=wl_C, m=m_w_10C[wl_C], Kw_sqr=K_w_sqr[wl_C])
ig = psd.PSDIntegrator()
ig.D_max = 8.0                                        # mm — see trap below
ig.num_points = 64
ig.axis_ratio_func = lambda D: 1.0 / dsr_thurai_2007(D)
ig.geometries = (geom_horiz_back, geom_horiz_forw)    # both, for Kdp
s.psd_integrator = ig
ig.init_scatter_table(s)                              # the expensive step

for D0 in (1.0, 2.0, 3.0):
    s.psd = psd.GammaPSD(D0=D0, Nw=8e3, mu=4)
    s.set_geometry(geom_horiz_back)
    Zh, Zdr = 10*np.log10(radar.refl(s)), 10*np.log10(radar.Zdr(s))
    s.set_geometry(geom_horiz_forw)
    print(f"D0={D0}  Zh={Zh:6.2f} dBZ  Zdr={Zdr:5.2f} dB  Kdp={radar.Kdp(s):6.3f}")
```

Measured output (C-band, Nw=8e3, mu=4):

```
D0=1.0  Zh= 26.23 dBZ  Zdr= 0.35 dB  Kdp= 0.027
D0=2.0  Zh= 47.21 dBZ  Zdr= 1.45 dB  Kdp= 2.215
D0=3.0  Zh= 60.99 dBZ  Zdr= 3.60 dB  Kdp=22.756
```

**Validated independently**: the 64-point table reproduces direct integration
over 400 individually-solved single drops to **+0.0034 dB** in Zh.

**The economics** (measured, C-band rain, 64 points, 2 geometries):
tabulation 4 ms, then each PSD evaluation **0.08 ms**. That ~50× ratio is why
the idiom is *tabulate once, evaluate many* — sweeping 1000 PSDs costs
essentially the same as sweeping 10.

### Two traps

**`D_max` truncation.** `D_max` must cover the tail that actually carries
Zh. At high rain rates the large-drop tail dominates the 6th moment; setting
`D_max=4` for a D0=3 mm distribution silently discards it and under-reports
Zh with no warning. Use 8 mm for rain, more for hail/graupel.

**`num_points` convergence** (measured, C-band, D0=2 mm, GammaPSD):

| num_points | Zh (dBZ) | Zdr (dB) |
|---|---|---|
| 8   | 47.1961 | 1.4807 |
| 16  | 47.2200 | 1.4608 |
| 32  | 47.2134 | 1.4557 |
| 64  | 47.2096 | 1.4528 |
| 128 | 47.2076 | 1.4513 |

Zh is converged to ~0.02 dB by 16 points, but **Zdr converges more slowly**
— it is a small difference of two large numbers. 64 points puts Zdr within
0.002 dB of the 128-point value; 8 points is off by 0.03 dB. **Use 64 for
production, 32 for exploration, 128 when Zdr precision matters.**

### PSD classes

`GammaPSD(D0, Nw, mu)` (normalized gamma, Bringi & Chandrasekar),
`ExponentialPSD(N0, Lambda, D_max)`, `UnnormalizedGammaPSD`, and
`BinnedPSD(bin_edges, bin_psd)` for disdrometer data. Custom forms subclass
`psd.PSD` — implement `__call__(D)` **and `__eq__`**, because the integrator
caches on PSD equality.

### Table persistence

```python
ig.save_scatter_table("table_C.dat", description="C-band rain, Thurai 2007, 64 pts")
ig2 = psd.PSDIntegrator(); ig2.load_scatter_table("table_C.dat")
```

Verified: reload reproduces Zdr to 15 significant figures
(1.4527906340426333 vs 1.4527906340426324). A 64-point 2-geometry table is
26 KiB. **The table does not carry a wavelength guard** — it is your
responsibility to pair a loaded table with a `Scatterer` of the same
wavelength, refractive index, and axis-ratio function. Encode those in the
filename and the `description` string.

## Orientation and canting — use the fixed scheme

Real hydrometeors wobble. Three strategies, all measured on the same case
(X-band, r=1.5 mm, axis_ratio=1.3, gaussian_pdf(std=10°)):

| Strategy | Zdr | Cost |
|---|---|---|
| `orient_single` | +3.0721 dB | 0.11 ms |
| `orient_averaged_fixed` (n_alpha=5, n_beta=10) | **+2.7846 dB** | **0.89 ms** |
| `orient_averaged_adaptive` | +2.7846 dB | 410 ms |

**The fixed scheme matches the adaptive one to four decimals at 460× lower
cost.** Use `orient_averaged_fixed`; reach for the adaptive integrator only
to validate a new particle class, never in a loop. Note also that ignoring
canting entirely (`orient_single`) overestimates Zdr by 0.29 dB here — a real
bias, not a rounding difference.

```python
from rustmatrix import orientation
s = Scatterer(radius=1.5, wavelength=wl_X, m=m_w_10C[wl_X], axis_ratio=1.3,
              orient=orientation.orient_averaged_fixed,
              or_pdf=orientation.gaussian_pdf(std=10.0),
              n_alpha=5, n_beta=10)
```

Canting sweep (same case), showing how canting washes out Zdr:

| canting_std | 0.1° | 5° | 10° | 20° | 40° | 60° | `uniform_pdf()` |
|---|---|---|---|---|---|---|---|
| Zdr (dB) | +3.0721 | +2.9974 | +2.7846 | +2.0859 | +0.7406 | +0.1759 | **+0.0000** |

`uniform_pdf()` gives exactly 0 dB — full random orientation, the correct
limit and a good self-test that your orientation machinery is wired up.

## HydroMix — multiple species in one target

Combines species into a single Scatterer-shaped object, so `radar.*` helpers
work unchanged. No pytmatrix analogue.

```python
from rustmatrix import HydroMix, MixtureComponent
mix = HydroMix([MixtureComponent(rain_sc, rain_psd, label="rain"),
                MixtureComponent(snow_sc, snow_psd, label="snow")], Kw_sqr=Kw)
mix.set_geometry(geom_vert_back)
print(10*np.log10(radar.refl(mix)))
```

Each component is a `Scatterer` with its own initialized `psd_integrator`
(and hence its own refractive index, axis-ratio function, and D_max) plus a
`PSD`. Pass `Kw_sqr` to the mixture.

**Verified: linear reflectivity is exactly additive** (relative error
0.0e+00 — rain 33.218 dBZ + snow 29.253 dBZ = mix 34.684 dBZ at Ka band).
That exactness is a useful invariant to assert in your own tests.

## Doppler + polarimetric spectra

```python
from rustmatrix import SpectralIntegrator, spectra
si = SpectralIntegrator(
    mix,
    component_kinematics={
        "rain": (spectra.fall_speed.atlas_srivastava_sekhon_1973,
                 spectra.GaussianTurbulence(0.2)),
        "snow": (spectra.fall_speed.locatelli_hobbs_1974_aggregates,
                 spectra.GaussianTurbulence(0.3))},
    v_min=-1.0, v_max=10.0, n_bins=256, w=0.0,
    geometry_backscatter=geom_vert_back, geometry_forward=geom_vert_forw)
res = si.run()
```

`res` is a `SpectralResult` with `v` (M,), `S_spec` (2,2,M), `Z_spec`
(4,4,M), and the spectral observables `sZ_h`, `sZ_v`, `sZ_dr`, `sKdp`,
`srho_hv`, `sdelta_hv`, `sLDR`.

- A `HydroMix` source **requires** `component_kinematics` mapping every
  component (by label or index) to `(fall_speed, turbulence)`; a bare
  `Scatterer` source requires `fall_speed=` instead. Mixing the two styles
  raises.
- `geometry_forward` is required for `sKdp` — without it `res.sKdp is None`.
- Fall-speed presets: `atlas_srivastava_sekhon_1973`, `brandes_et_al_2002`,
  `beard_1976(D, T, P)`, `locatelli_hobbs_1974_aggregates`,
  `locatelli_hobbs_1974_graupel_hex`, `power_law(a, b, D_ref, c)`.
- Turbulence: `NoTurbulence`, `GaussianTurbulence(sigma_t)`,
  `InertialZeng2023` (size-dependent particle inertia),
  `turbulence.from_params(...)`.
- Beam broadening: `sigma_beam = u_h * beamwidth / (2*sqrt(2*ln2))`, from
  `u_h=` (m/s) and `beamwidth=` (**radians**).
- **Doppler sign**: positive velocity = fall direction = toward a
  *down*-pointing radar. **For an up-looking profiler you must negate the
  fall speed too** — not just `w` and `v_bins`. The upstream docs (and an
  earlier version of this skill) say it is a pure sign flip of `w` and
  `v_bins`; measured, that recipe **silently retains only 16.4% of the
  spectral power** (integrated sZ_h 1168.43 vs 7124.10) and returns
  v_mean = +3.29 instead of -8.16 m/s. The kernel is even in `(v - v_exp)`,
  but `v_exp = v_t(D) + w` is not. Correct form:

  ```python
  si = SpectralIntegrator(s, fall_speed=lambda D: -np.asarray(vt(D), float),
                          w=-w, v_bins=-v_bins[::-1], ...)
  ```

  Verified to mirror the down-looking result exactly (`max|diff| = 0.0` in
  every observable). Simpler and equally exact: run it down-looking and
  mirror the arrays yourself (`v -> -v[::-1]`, each field `-> field[::-1]`).

**`collapse_to_bulk()` round-trips to 1 ulp** — integrating the spectrum back
over velocity reproduces the bulk observables (Zh agrees to 8.5e-16 relative,
i.e. -3.9e-15 dB, and Zdr bitwise; verified against both a bare `Scatterer`
and a `HydroMix`), *but only with `noise=None`*. Passing `noise="realistic"` / a scalar / an `(h, v)` tuple
biases `sZ_dr`, `srho_hv`, and `sLDR` through per-bin SNR by design, which
breaks the round-trip. **Use `noise=None` when validating; add noise only
when simulating what a real receiver sees.**

Make `v_bins` span the full fall-speed range of your particles — a grid that
clips the tail silently loses signal.

For non-uniform beams where the closed-form `sigma_beam` breaks down,
`rustmatrix.spectra.beam` provides `GaussianBeam`, `AiryBeam`,
`TabulatedBeam`, `Scene`, `BeamIntegrator`, and
`marshall_palmer_psd_factory`.

## Parallelism

Since v2.2 **every** entrypoint releases the GIL, including single-particle
`calctmat`/`calcampl`. Verified directly: independent T-matrix builds from a
`ThreadPoolExecutor` reach **8.04x at 14 workers**, statistically identical to
a fork process pool (8.04x), while a duration-matched pure-Python control on
the same executor is flat at 1.03x. The GIL really is released.

But calibrate expectations: **"near-linear" holds to about 4-6 workers**
(efficiency 0.98 at 4, 0.88 at 6), then decays — 0.78 at 8, 0.57 at 14. The
honest figure on 14 cores is **8x, not 14x**. Use 8 workers for efficiency,
14 for peak throughput.

**Use threads, not processes.** Not just for speed — processes barely work
here: `TMatrixHandle` raises `TypeError: cannot pickle`, any `Scatterer`
raises `AttributeError` (the default `or_pdf` is a closure), and a configured
`PSDIntegrator` raises `PicklingError` on its `axis_ratio_func` lambda.
Threads share handles and tables for free with no pickling surface.

`TMatrixHandle` is immutable and safe to share: one handle evaluated from
1-14 threads over 10,000 geometries returned **bit-identical** results
(max abs diff exactly 0) at every width. Worth knowing it only pays off when
one `calcampl` exceeds ~50 us (nmax >~ 25); at nmax=12 threading is *slower*
than serial (0.80x).

Don't nest an outer thread pool over `init_scatter_table` — rayon already
saturates the machine (14 outer threads over W-band 64-point tables buys only
1.43x). `RAYON_NUM_THREADS` controls the pool but is **silently ignored once
rayon's global pool is built** — set it in the shell or before
`import rustmatrix`.

Free-threaded CPython (3.14t+) is supported natively with `cp314t` wheels.

## Porting from pytmatrix

Usually just change the imports — `Scatterer`, `radar.*`, `psd.*`,
`refractive`, and `tmatrix_aux` are 1:1 where the physics matches. Deliberate
divergences: `HydroMix` and `SpectralIntegrator` are new; full-random
orientation averaging is closed-form (exact) rather than quadrature; private
pytmatrix attributes are not preserved. Legacy kwargs (`axi`, `lam`, `eps`,
`rat`, `np`, `scatter`) still work but emit `DeprecationWarning` — pass
`suppress_warning=True` to silence during a migration.

## Failure modes: the exception you cannot catch

Non-convergence surfaces as `pyo3_runtime.PanicException`, which subclasses
**`BaseException`, not `Exception`**. So this does not work:

```python
try:
    integ.init_scatter_table(s)      # large/elongated particles
except Exception:                    # NEVER FIRES for a solver panic
    ...
```

Your worker, batch loop, or thread pool dies instead. Guard with
`except BaseException` (and note `import pyo3_runtime` itself raises
`ModuleNotFoundError` — you can only reach the type via `type(e)` after a
first catch).

The underlying limits are hard Fortran-inherited caps: `nmax <= 200` (NPN1)
and `ngauss = nmax*ndgs <= 300` (NPNG1). The usable envelope depends strongly
on axis ratio — measured largest size parameter x that succeeds at
`ndgs=2`:

| axis_ratio (h/v) | 1.0 | 1.3 | 1.6 | 1.872 | 2.5 | 3.0 |
|---|---|---|---|---|---|---|
| max x | 80 | 40 | 25 | 19 | 8 | 5 |

Since `1.0/dsr_thurai_2007(8.0) = 1.872`, **a W-band table with D_max=20 mm
and the standard Thurai relation panics.**

### Three counter-intuitive rules for a non-converging particle

1. **Do not tighten `ddelt`.** It forces `nmax` up into the cap and makes
   failure *worse* — cases often switch from "singular Q matrix" to "NGAUSS
   exceeds NPNG1". (Tightening is also pointless for spheres: a 27-case sweep
   moved the error by a factor of exactly 1.0.)
2. **Do not loosen `ddelt` to force success.** At `ddelt=0.1` every hard case
   returns a number — wrong by a median 2.6 dB and up to **8.06 dB in Zdr**.
   Treat "needs ddelt > 1e-3" as *outside the reliable envelope*, not solved.
   Only 1e-2 is defensible (median 0.10 dB), and should be reported.
3. **Do not set `ndgs=1` to make it "work".** It reports **success on 29 of 31
   otherwise-failing cases with `nmax` pinned at 199** — the refinement loop
   exhausted NPN1 and the solver falls through with best-effort unconverged
   state and no error at all. Assert `s.nmax < 190` after any solve you did
   not otherwise validate.

Raising `ndgs` *is* the right first move for a genuine "singular Q matrix"
(it fixed 2 of 2 such cases, and thin plates/long columns as cylinders need
`ndgs=4`-`8`) — but it cannot help the NGAUSS-cap cases, because it *shrinks*
the usable nmax to `300//ndgs`. For those, reduce the size parameter or
moderate the axis ratio.

**Drop-shape relations go negative if extrapolated.** `dsr_thurai_2007`
crosses zero at **D = 13.6186 mm** (`dsr_bc` at 12.5118, `dsr_pb` at
16.6129), so `1.0/dsr(D)` diverges and then flips sign, panicking the core.
Always clamp:

```python
integ.axis_ratio_func = lambda D: 1.0 / dsr_thurai_2007(min(D, 8.0))
```

For genuine hail, supply a real hail axis-ratio model and cap it near 2 —
large hail is rounder than an extrapolated raindrop fit implies.

## Silent-wrong-answer paths (the dangerous class)

These raise nothing and print nothing. Each was measured.

| Trap | Measured cost |
|---|---|
| Loading a C-band table into an X / Ka / S-band `Scatterer` | **-9.27 / -30.28 / +12.22 dB** in Zh |
| Mutating `s.wavelength` after `init_scatter_table` | -9.27 dB in Zh |
| Mutating `s.m` (water→ice) after tabulation | **6.90 dB** — observables don't change *at all* |
| PSD subclass inheriting a parent `__eq__` that misses a new parameter | **exactly 20.000 dB** |
| Mutating a PSD in place (even with a correct `__eq__`) | **14.02 dB** |
| Declaring `RADIUS_MAXIMUM` while passing an equal-volume radius | -1.3 to -12.9 dB |
| Even `n_alpha` in `orient_averaged_fixed` | up to **2.3 dB** in Zdr |
| HydroMix components with mismatched `D_max` | 0.91 dB under-report |

**Treat a `Scatterer` with an initialized `psd_integrator` as immutable** in
wavelength, `m`, axis-ratio function, and `D_max`. To change any of them,
build a new `Scatterer` and a new `PSDIntegrator`. Per-diameter refractive
index belongs in `PSDIntegrator.m_func`, which *is* baked into the table.

`load_scatter_table` has **no wavelength, refractive-index, or axis-ratio
guard**, and it overwrites `num_points`/`D_max` while leaving
`axis_ratio_func` and `m_func` as `None`. Encode band, index, relation,
D_max, and num_points in both the filename and the `description=` string,
and assert on the description after loading.

### `n_alpha` must be ODD

The alpha grid is `linspace(0, 360, n_alpha+1)[:-1]`, which for **even**
`n_alpha` samples pairs of points 180° apart and aliases the `cos(2α)`
dependence. Errors of 1.0–2.3 dB that **do not shrink with refinement** —
`n_alpha=12` is still 1.0 dB wrong against the exact 0 dB `uniform_pdf()`
answer. With odd `n_alpha >= 5` the error is < 2e-6 dB.

Measured Zdr against `uniform_pdf()`, whose exact answer is **0 dB**
(C band, r=1.5 mm, axis_ratio=1.5):

| n_alpha | n_beta=4 | n_beta=8 | n_beta=16 | |
|---|---|---|---|---|
| 2 | +0.87174 | -0.99772 | +0.74130 | even |
| 3 | +0.00649 | +0.00018 | +0.00018 | odd |
| 4 | -0.00256 | -1.10780 | -0.07396 | even |
| 5 | +0.00632 | **0.00000** | **0.00000** | odd |
| 7 | +0.00632 | **0.00000** | **0.00000** | odd |
| 9 | +0.00632 | **0.00000** | **0.00000** | odd |
| 12 | -0.01790 | -0.43324 | -0.04697 | even |

Note `n_alpha=12, n_beta=8` is **0.43 dB wrong** — refinement does not save
you. (The `0.00000` entries above are 5-decimal display: odd `n_alpha >= 5`
with `n_beta >= 8` actually lands at **3.0e-07 dB**, and `n_alpha=3` plateaus
at **1.8e-04 dB**. Both are far below any physical significance — the point is
the *parity*, which costs 0.4-2.3 dB, not the residual.)

This is also what makes wide-canting results look "unstable in `n_beta`".
The cheapest rule robust to 0.01 dB is **`(n_alpha=3, n_beta=4)`** (3×
cheaper than `(5, 10)`); use **`n_alpha >= 5` with `n_beta >= 8`** to push the
residual from 1.8e-04 to 3.0e-07 dB.
Always self-test with `uniform_pdf()`.

### A raising PSD poisons the integrator cache

`PSDIntegrator.get_SZ` clears `_S_dict`/`_Z_dict` *before* evaluating the
PSD but sets `_previous_psd` only *after*. If your PSD raises mid-evaluation
(buggy `__call__`, or `psd=None`), the integrator is left with empty dicts
while `_previous_psd` still points at **the last PSD that worked** — and that
innocent earlier PSD is the casualty. It now matches `_previous_psd`, takes
the cache-hit branch, and dies on
`KeyError: (90.0, 90.0, 0.0, 180.0, 0.0, 0.0)`. The PSD that actually raised
keeps raising its own honest exception; the one that was fine is silently
destroyed. Through `HydroMix` this is fatal and the traceback blames the
*geometry*, giving no hint that a PSD exception was the cause.

Recover with `integ._previous_psd = None`. Prevent it by validating first:
`assert np.all(np.isfinite(p(np.linspace(0.1, D_max, 8))))`.

## Band-dependent convergence

`num_points` guidance is not band-universal. At Ka band, 8 points gives Zh to
0.12 dB and Zdr to 0.035 dB — both *looking* converged — while **Kdp is 21.2%
wrong**. Size `num_points` against the observable you actually need: Ka-band
Kdp needs 64 points for ~1%, 128 for ~0.25%; C/X-band Kdp is fine at 16.

`D_max` truncation is also band-dependent, and opposite to intuition. For
heavy rain (D0=3 mm), `D_max=4` mm discards **5.19 dB** of Zh at C band and
5.43 dB at X, but only **0.13 dB** at Ka — short-wavelength backscatter
saturates and stops rewarding the large-drop tail.

Extra geometries are **free**: 128 points at C band costs 2.55 ms for one
geometry and 2.48 ms for four. Always pass both `geom_horiz_back` and
`geom_horiz_forw` so Kdp needs no second table. `angular_integration=True`,
by contrast, costs 30-46x.

## Other API traps worth knowing

- **`RADIUS_EQUAL_AREA` is non-functional.** The constant is the float `0.0`
  and the core computes `a = rat*axi`, so it zeroes the radius and panics
  `spherical_jn requires x > 0 (got 0)`. Pass the `sarea()` ratio as
  `radius_type` instead (`radius_type` is just a multiplier).
- **The Chebyshev shape code *is* the order.** `SHAPE_CHEBYSHEV == 1` means
  n=1; pass `shape=n` for any order, and `axis_ratio` becomes the deformation
  amplitude (must be > 0). For cylinders, `axis_ratio` is diameter/length
  (>1 plate, <1 column).
- **`shape=-3` silently returns a sphere** for every `axis_ratio` — the core
  passes a hardcoded zero coefficient array. Don't use it.
- **`SpectralIntegrator` applies no elevation projection.** The velocity axis
  is `v_t(D) + w` regardless of `geometry_backscatter`. Scale the fall speed
  yourself: `lambda D: np.sin(np.deg2rad(elev)) * vt(D)`. (`BeamIntegrator`
  *does* project by cos θ — don't double-correct there.)
- **`beamwidth` and every `hpbw` are in RADIANS.** Passing `3.0` for "3
  degrees" inflates σ_beam by 57x with no error.
- **Never validate polarimetry at `geom_vert_back`** — vertical incidence
  forces Zdr = 0 and ρ_hv = 1 identically, so a "perfect" round-trip proves
  nothing. Use a slant or horizontal geometry, and note the backscatter
  branch is `phi=180`, not `phi=0`.
- **`InertialZeng2023`'s default `L_o=100` m disables its own size
  dependence** (Stokes number stays < 0.021 for all rain), making it
  bit-comparable to `GaussianTurbulence`. Set `L_o ≈ sqrt(tau_p^3 * eps)` —
  centimetres for rain.
- **`realistic_noise_floor`'s wavelength argument is ignored** — it returns
  0.01 for every band. Pass `Z_dBZ=` explicitly.
- **Fall-speed presets go unphysical past ~8 mm.** `brandes_et_al_2002` is
  non-monotonic *inside* its stated range (local max at 5.98 mm) and returns
  7.18 m/s at 15 mm, **0.0 at 20 mm**; `beard_1976` wraps Brandes and
  inherits it. Use `atlas_srivastava_sekhon_1973` above 8 mm (bounded,
  monotone, 9.65 m/s at 20 mm) — but clamp it below D=0.109 mm, where it goes
  *negative*.
- **`noise=` never enters `S_spec`/`Z_spec`**, so `collapse_to_bulk` round-trips
  exactly even with noise on — it cannot detect that noise is enabled. Check
  `res.noise_h`/`res.noise_v` instead.

## Debugging checklist

1. **Zdr negative for rain?** Axis ratio inverted — use `1.0/dsr_*(D)`.
2. **`ImportError` on `m_i`?** It is `mi`, and it is a function: `mi(λ_mm, ρ)`.
3. **Zh lower than expected?** `D_max` is truncating the large-drop tail
   (5.19 dB at C band for D0=3 mm at D_max=4).
4. **Zdr off by 1-2 dB and refinement doesn't help?** Even `n_alpha`. Use odd.
5. **Zdr unstable at the 0.01 dB level?** Raise `num_points` to 128.
6. **Ka-band Kdp wrong while Zh/Zdr look converged?** `num_points` too low —
   Kdp needs 64-128 at Ka.
7. **`radar.Kdp` looks wrong?** You need `geom_horiz_forw`, not backscatter.
8. **`sKdp is None`?** Pass `geometry_forward=` to `SpectralIntegrator`.
9. **Process died mid-sweep with no traceback you could catch?**
   `PanicException` is a `BaseException` — use `except BaseException`.
10. **`KeyError` on a geometry tuple that worked a moment ago?** A PSD raised
    and poisoned the cache. Set `integ._previous_psd = None`.
11. **Changed `wavelength` or `m` and nothing moved?** The scatter table is
    stale — rebuild the `Scatterer` and `PSDIntegrator`.
12. **Up-looking spectrum nearly empty?** You negated `w` and `v_bins` but not
    the fall speed.
13. **Spectral width ignores your `beamwidth`?** It's in radians.
14. **Something takes forever?** Cost goes as x^2.72 — check your size
    parameter, and make sure you are not calling `orient_averaged_adaptive`
    in a loop.
15. **Radius vs diameter** — `Scatterer(radius=...)` takes D/2.

## Verified against

Last re-run: 2026-08-27.

rustmatrix 2.2.0 (PyPI ABI3 wheel `rustmatrix-2.2.0-cp39-abi3-macosx_11_0_arm64.whl`),
CPython 3.13, numpy 2.x, macOS arm64, 14 cores. Every number in this document was
measured on that configuration.

Accuracy claims (Mie parity, PSD moments, `HydroMix` additivity, the `n_alpha`
parity table, the silent-error magnitudes) are properties of the library and should
reproduce anywhere. **Timings and the convergence envelope are machine-specific:**
the `x^2.72` cost law, the 8.04x thread scaling, and the tabulation costs were
fitted on this hardware and will differ on yours. Re-measure before planning a
large run.

## Acknowledgements

All of the above was measured against rustmatrix v2.2.0. The library is the
work of **Prof. Stephen W. Nesbitt** (UIUC), and it holds up well under
scrutiny: Mie parity at 1e-8 across six bands and two decades of size
parameter with zero convergence failures at default settings, exact linear
reflectivity additivity in `HydroMix`, a spectral→bulk round-trip that closes
to 1 ulp (Zh 8.5e-16 relative), and genuine GIL release confirmed against a
process-pool control. The traps documented here are almost all inherited
Fortran-era limits or documentation gaps, not defects in the physics.
