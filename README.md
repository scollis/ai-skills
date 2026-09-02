# ai-skills

Agent skills for atmospheric and radar science, authored by **Scott Collis** with
**Claude** (Anthropic) and used with Claude Science.

A *skill* here is a directory holding a `SKILL.md` — prose an agent loads as
reference — and usually a `kernel.py` of helper functions that load alongside it.
The point of committing them is not the code volume; it is that **the factual
claims are checked**. Bucket names, cost constants, and layout quirks go stale
quietly, so the test suites in `tests/` re-verify them against live services and
the offline suite refuses documentation that has drifted from its own code.

## What is here

| skill | what it does |
|---|---|
| [`nexrad-aws-2025`](skills/nexrad-aws-2025/) | NEXRAD on AWS after the 2025 migration: bucket map, VCP/SAILS/AVSET detection, ARCO access primitives |
| [`nexrad-cloud-router`](skills/nexrad-cloud-router/) | Chooses among the four NEXRAD access paths on measured cost, and names the skill to load per step |
| [`nexrad-cost-calibration`](skills/nexrad-cost-calibration/) | Re-measures those cost constants for the local machine and link |
| [`nexrad-arco`](skills/nexrad-arco/) | ARCO Icechunk/Zarr store to Py-ART; QVPs, METAR overlays, animations |
| [`nexrad-radar-gcs`](skills/nexrad-radar-gcs/) | GCS mirror fallback when AWS is blocked, plus PPI / dual-pol plotting helpers |

The first tranche — NEXRAD cloud access and routing — chosen because the 2025
bucket migration broke most existing code and these five cross-reference each
other.

### Py-ART processing

| skill | what it does |
|---|---|
| [`pyart-foundations`](skills/pyart-foundations/) | The `Radar` object, scan anatomy and split-cut handling, field naming, the `extract_sweeps` sweep_number trap, IO and xradar interop. Router for the rest |
| [`pyart-mapping`](skills/pyart-mapping/) | Projection semantics, the `PlateCarree`-vs-`Geodetic` datum trap, cone-of-silence georeferencing verification, geodesic range rings, `grid_origin` |
| [`pyart-gatefilter-qc`](skills/pyart-gatefilter-qc/) | `GateFilter` semantics and its five silent traps, marginal cost per criterion, measured downstream sensitivity |
| [`pyart-velocity-dealias`](skills/pyart-velocity-dealias/) | The three dealiasers, velocity texture, Nyquist handling, reference-velocity paths and their unbounded extrapolation |
| [`pyart-dualpol-phase`](skills/pyart-dualpol-phase/) | KDP method selection on measured cost and plausibility, PhiDP unfolding, attenuation correction, the LP solver crash |
| [`pyart-gridding`](skills/pyart-gridding/) | `grid_from_radars`, radius-of-influence selection by holdout cross-validation, weighting choice, multi-radar and `GateMapper` |
| [`pyart-retrievals`](skills/pyart-retrievals/) | QPE, echo classification, hydrometeor ID, the dependency order the errors do not name, CAPPI/QVP/CFAD products |

Measured against Py-ART 2.2.5 on two radar classes, because most Py-ART surprises
come from assuming one when you have the other: **NEXRAD WSR-88D** (KIWA
2026-08-20 04:14 UTC, VCP 212 with SAILSx1 — 19 sweeps over 14 unique elevations,
split cuts, per-sweep Nyquist, no `normalized_coherent_power`) and a **research
C-band** (ARM SGP C-SAPR, MC3E 2011-05-20 11:29 UTC — 17 tilts one sweep per
elevation, uniform 16.52 m/s Nyquist, NCP present).

### ARM VAPs

| skill | what it does |
|---|---|
| [`cmac-vap`](skills/cmac-vap/) | The ARM CMAC 2.0 VAP: config system, fuzzy gate classification, sounding ingest, clutter retrieval |

`cmac-vap` is deliberately **not** part of the Py-ART tranche. CMAC is a consumer
of Py-ART, so what it teaches about idiomatic Py-ART usage — call order, which
guards a production VAP actually needs — is folded into the `pyart-*` skills,
while its own machinery (config dicts, membership functions, VAP conventions)
lives only in `cmac-vap`. A Py-ART user should never have to install
`scikit-fuzzy` to follow a `pyart-*` skill; `test_structure_pyart.py` enforces
that boundary.

### ARM data standards

| skill | what it does |
|---|---|
| [`arm-netcdf-standards`](skills/arm-netcdf-standards/) | The ARM Data File Standards (DOE/SC-ARM-15-004 v1.3) made operational: filename and datastream construction, the `base_time`/`time_offset`/`time` triple, coordinate and location variables, required attributes, bit-packed QC, state and source variables, global attributes. Ships `arm_standards_check.py`, a rule engine that cites the section behind every finding, and helpers that write a compliant file rather than retrofit one |

Calibrating this one against released ARM data changed it. Run against one file
from each of 143 local datastreams, five rules turned out to be wrong rather
than the files — §6.1.4 makes `units` *not* recommended on a bounds variable,
which alone was 55 false positives — and the survivors are deviations the
standard itself records as retired practice: `units = "unitless"`, `valid_min`
used as a QC limit, `"Quality check results on field:"`. So the skill documents
what ARM's own files do as well as what the document says, and the checker
carries two profiles: what the ADC's published files actually satisfy, and the
literal reading of §6.7.1. A released file is not a safe compliance template,
which is the sort of thing you only learn by measuring.

### Scattering forward models

| skill | what it does |
|---|---|
| [`rustmatrix-scattering`](skills/rustmatrix-scattering/) | T-matrix scattering for nonspherical hydrometeors: `Scatterer`, polarimetric observables, PSD tabulation, orientation averaging, `HydroMix`. Carries the axis-ratio convention the upstream docs invert, the solver's convergence envelope, and the paths that return silently wrong numbers |
| [`rustmatrix-spectra`](skills/rustmatrix-spectra/) | The Doppler and polarimetric spectra engine: `SpectralIntegrator`, fall-speed presets and their real validity limits, turbulence and beam broadening, receiver noise, `BeamIntegrator` over a scene |

[rustmatrix](https://github.com/swnesbitt/rustmatrix) is by **Prof. Stephen W.
Nesbitt** (University of Illinois Urbana-Champaign) — a Rust-backed replacement
for the numerical core of pytmatrix, adding multi-species mixtures, spectral
polarimetry, and beam-pattern integration, and growing out of his ATMS 410 Radar
Meteorology course and *Radar Meteorology: A First Course* (Rauber & Nesbitt,
2018). These two skills document it; they do not vendor it.

Measured against rustmatrix 2.2.0 on macOS arm64 / CPython 3.13. The library
itself validated well — Mie parity at 7.7e-08 across six bands with zero
convergence failures at default settings, exact reflectivity additivity in
`HydroMix`, a spectral-to-bulk round-trip closing to 1 ulp. What the skills are
*for* is the other half: several of rustmatrix's traps produce wrong numbers
rather than exceptions, so each is documented with the measured magnitude — a
scatter table loaded at the wrong wavelength costs 30 dB in Ka-band Zh, an even
`n_alpha` in orientation averaging aliases by up to 2.3 dB and does not improve
with refinement, and passing a drop-shape relation directly to `axis_ratio`
inverts the sign of Zdr with no error at all. Solver limits raise
`pyo3_runtime.PanicException`, which subclasses `BaseException`, so `except
Exception` misses them.

Two skills referenced by the NEXRAD tranche are **not yet published here**:
`nexrad-site-rainfall` and `nexrad-area-over-threshold`. They belong to a later
tranche; until then those cross-references point at nothing in this repo.

## Using a skill

With Claude Science, load by name and the helpers arrive in your kernel:

```python
skill("nexrad-cloud-router")
plan = plan_analysis("three month base tilt series", site="KLOT", n_volumes=2000)
print(format_plan(plan))
```

Without it, `SKILL.md` is readable on its own and `kernel.py` imports as an
ordinary module:

```python
import sys; sys.path.insert(0, "skills/nexrad-aws-2025")
import kernel as nexrad
keys = nexrad.nexrad_keys("KLOT", start, end, client=nexrad.s3_anon())
```

The one thing to know: **`kernel.py` files are exec'd by the skill loader, not
imported**, so they define no `__file__` and may only contain functions, imports,
and literal top-level assignments. `tests/test_structure.py` enforces that.

## Tests

```bash
pip install -r requirements.txt
pytest tests/test_structure.py        # offline, all skills, runs on every push
pytest tests/test_structure_pyart.py  # offline, pyart-* + cmac-vap claim checks
pytest tests/test_structure_rustmatrix.py   # offline, rustmatrix-* claim checks
pytest tests/test_arm_standards.py    # offline, arm-netcdf-standards drift + round trips
pytest tests/test_live_*.py           # hits live buckets, runs weekly
```

The offline suites check skill structure, the loader's constraints, absence of
secrets, and documentation-vs-code agreement. `test_structure_pyart.py` adds the
Py-ART tranche's claim checks: physical invariants (cone radius linear in height,
exclusion fractions inside [0,1], the dealiasing ratio dividing out against the
stated Nyquist), internal consistency (a number stated twice must agree), and
provenance (measured values carry a named radar and date; every helper the prose
tells you to call exists). One of them exists because the drift already happened
— a KDP row that paired one run's runtime with another run's percentiles — and it
fails if either half of that pair is quoted alone.

`test_structure_rustmatrix.py` does the same for the scattering tranche, and
where rustmatrix is installed it re-derives the load-bearing claims rather than
trusting the prose: it solves for the drop-shape zero crossings, checks that the
documented axis-ratio recipe gives positive Zdr while the bare relation gives
negative, reproduces the `n_alpha` parity result, and confirms a solver panic
still arrives as a `BaseException`. Two of its checks also exist because the
drift already happened: an "exact to floating point" claim that the document's
own table contradicted (five-decimal display of a 3.0e-07 residual), so
exactness now has to be stated with a ulp or residual figure; and a guard-rail
check that fails any `assert_*`/`check_*` helper containing no `assert` or
`raise`, which caught a Mie-parity gate that documented a tolerance and never
enforced it. The live suites are the ones that
detect service drift — a changed bucket layout or store schema shows up as a
failing scheduled run rather than as a wrong answer in someone's analysis.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: edit under `skills/`, run the
offline suite, and keep every numeric claim in a `SKILL.md` derived from
something a test can check.

## Authors

- Scott Collis
- Claude (Anthropic) — co-author of the skills, helpers, and test suites

## License

[MIT](LICENSE). The skills describe public datasets (NOAA NEXRAD via the NSF
Unidata AWS buckets, the NEXRAD ARCO store, and the Google Cloud mirror); the
data carry their own terms.

_Skill contents last synced from the registry: 2026-08-26._
