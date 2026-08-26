---
name: nexrad-cloud-router
description: Decide HOW to work with NEXRAD WSR-88D radar in the cloud before writing any code - which of the four AWS access paths (Level II archive, real-time chunks, ARCO per-VCP Icechunk store, ARCO lowsweeps base-tilt cube) fits the task, and which NEXRAD skill to load for each step. Use when the task is open-ended ("analyse this storm", "build a rainfall climatology", "what is the radar showing"), when a choice between raw Level II and cloud-optimised Zarr is unclear, or when a plan needs cost estimates in seconds and megabytes before committing. Routes to nexrad-aws-2025, nexrad-arco, nexrad-radar-gcs, nexrad-site-rainfall, nexrad-area-over-threshold. Triggers - NEXRAD, WSR-88D, Level II, radar data plan, which bucket, ARCO vs raw, cloud-optimised radar, access path, cost estimate, base tilt series, radar climatology.
---

# Routing NEXRAD work in the cloud

This skill decides *which path and which toolchain* to use. It does not read
radar data itself — it names the sibling skill that does. `kernel.py`
auto-loads; the cost constants in it are measured, not guessed (see
**Calibration**).

## 1. The decision in one call

```python
plan = plan_analysis("three month base tilt reflectivity series",
                     site="KLOT", n_volumes=500)
print(format_plan(plan))
```

That returns the archetype, the chosen source with its reason, a cost estimate
in seconds and megabytes, the runner-up path, the ordered steps, **which skills
to load for each step**, and the guardrails that apply. Load the named skills
and execute the steps.

If you already know the shape of the work, skip to `choose_source(...)`.

## 2. The four paths, and what each is *for*

| Path | Use when | Cost per unit (measured) | Hard limit |
|---|---|---|---|
| **raw Level II** (`unidata-nexrad-level2`) | you need every sweep/field, or **true ray geometry** | 8.4 MB, ~7.8 s per volume | ~7 min latency |
| **ARCO per-VCP** (`nexrad-arco/<SITE>`) | you need a few sweeps × fields over many times | ~0.47 s per (sweep × field) chunk | azimuth pre-regridded; few sites |
| **ARCO lowsweeps** (`nexrad-arco/<SITE>-lowsweeps`) | base-tilt series, 2015→now, any length | ~0.36 s per scan | base tilt only |
| **chunks bucket** (`unidata-nexrad-level2-chunks`) | sub-minute latency | seconds | must reassemble S/I/E |

`noaa-nexrad-level2` is **dead** — it denies access. Never fall back to it.

## 3. The two decisions that actually matter

**Hard constraints come before cost.** Two of them override any speed argument:

1. **True ray geometry.** ARCO stores azimuth as a *shared* exact-grid
   coordinate (720 or 360 values reused across scans). Raw KLOT rays jitter up
   to 0.19 of nominal spacing. So anything testing gridding, spectral or
   non-uniform-FFT interpolation, or dealiasing **must** use raw Level II —
   ARCO has already thrown away the quantity under test.
2. **Site coverage.** ARCO publishes only a handful of sites. Call
   `arco_coverage()` — it lists them live — rather than assuming.

**Then cost, and the lever is chunk count.** ARCO bills per (sweep × field)
chunk; a raw volume is one sequential transfer that carries *everything*. So
the question is only ever "how many chunks do I need?":

```python
crossover_chunks()               # 17 at 8.4 MB volumes on a 1.2 MB/s link
crossover_chunks("quiet")        # 15
crossover_chunks("convective")   # 25 -- bigger volumes push it up
```

Call it rather than quoting it: the value moves with both volume size and
`COST["raw_MB_per_s"]`.

Below the crossover ARCO wins; above it, download the volume. One base-tilt PPI
(1 sweep × 1 field) is 1 chunk — ARCO. A full dual-pol volume (17 × 5, ×3 for
SAILS fragmentation = 255 chunks) is far past it — raw.

## 4. Worked routes

| Task | Route | Why |
|---|---|---|
| "plot the 27 Jul tornado at KLOT" | raw Level II → `nexrad-radar-gcs` for plotting | one volume, all fields, needs real geometry for a faithful PPI |
| "three-month base-tilt series" | ARCO lowsweeps | measured **22.8× faster** than raw for the same numbers |
| "echo-top climatology" | cost-compared per volume count | needs upper tilts → 17 sweeps/volume, so raw usually wins |
| "rainfall accumulation over a site" | source by cost → `nexrad-site-rainfall` | Z-R and QC live in that skill |
| "area above a threshold" | source by cost → `nexrad-area-over-threshold` | needs the lowest usable sweep only |
| "what's it doing right now" | chunks bucket | archive lags ~7 min, ARCO ~8 min |
| "test my gridding code" | raw Level II, always | ARCO azimuth is pre-regridded |

## 5. Calibration

Constants were measured on KLOT, 2026-08-25, on a ~1.2 MB/s sandbox link:

- raw volume **8.4 MB mean** (mixed/quiet) — this is **bimodal**: quiet 3 h
  window 7.67 MB (5.21–8.46), convective 13.29 MB (7.96–16.95). Pass
  `regime="convective"` when the weather warrants; it moves the crossover from
  17 chunks to 25.
- ARCO chunk **0.47 s** bare, **0.60 s** inside a reassembly loop, plus
  **0.066 s** per (sweep, index) probe — reassembling a 3-index KLOT volume
  measured 12.7 s for 21 sweep-reads and 51 probes.
- lowsweeps scan **0.36 s**; repo open **4.9 s**; whole 1 M-scan time axis
  **5.6 s**.
- ARCO chunks are zstd, ~4.3× smaller on the wire than decoded (1.2 MB vs
  5.3 MB for 720 × 1832 float32).

**Bandwidth is the constant that travels worst.** It sets the crossover, so
when a decision is close:

```python
measure_throughput("KLOT", n=2)   # updates COST["raw_MB_per_s"] only
```

It deliberately leaves the volume-size constants alone — one volume's size
tells you about that day's weather, not about the archive.

**Equivalence was verified, not assumed:** 8 base-tilt scans pulled through raw
Level II and through lowsweeps returned *identical* peak dBZ
(68.0/68.0/66.0/64.0/66.5/65.0/63.0/62.5) at 22.8× the speed. The paths agree;
only the cost differs.

## 6. Guardrails every route carries

These bite regardless of path, so `plan_analysis()` attaches them to every plan:

- **Sweep count is not a property of the VCP.** 61 consecutive KLOT volumes all
  reporting VCP-212 split into 17-, 21- and 24-sweep configurations (plain,
  MESO-SAILS ×2, MRLE+4). Detect per volume.
- **Split cuts** repeat the three lowest tilts (surveillance + Doppler). Never
  select a sweep by field-iteration order.
- **ARCO `-999` fill** is base64-encoded in the attrs, so nothing masks it —
  ~75% of gates in a low sweep.
- **SAILS fragmentation**: one physical volume spans ~3 consecutive ARCO scan
  indices. Reading one index silently loses the upper tilts.
- Fix the CA bundle **before** the first `icechunk` import, once per process.

Details and the helpers for all of these live in `nexrad-aws-2025`.

## 7. Where the work happens

| Skill | Owns |
|---|---|
| `nexrad-aws-2025` | buckets, keys, VCP/SAILS/AVSET logic, ARCO access primitives |
| `nexrad-arco` | ARCO→Py-ART workflow, QVPs, METAR overlays, animations |
| `nexrad-radar-gcs` | PPI/dual-pol plotting, gate filters, GCS mirror fallback |
| `nexrad-site-rainfall` | Z-R rain rate, site extraction, QC, parallel scan processing |
| `nexrad-area-over-threshold` | areal statistics above thresholds |

All five now point at the live buckets; `nexrad-radar-gcs` is the GCS mirror
fallback for when AWS is proxy-blocked, plus the plotting helpers.

## Environment

Needs `nexrad-aws-2025` loaded in the same kernel for `measure_throughput()`
(it borrows `s3_anon`/`nexrad_keys`/`download_volume`). `arco_coverage()` needs
only `boto3`. Project env: `radar`.

## Verified against

Live buckets on **2026-08-25**; 43 checks in the router's test suite pass,
including six that assert the cost model reproduces the measured benchmarks
within tolerance. Re-run `measure_throughput()` on a different link, and
re-check `arco_coverage()` if much time has passed.
