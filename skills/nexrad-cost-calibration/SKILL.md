---
name: nexrad-cost-calibration
description: Re-measure NEXRAD access-path costs (raw Level II download bandwidth, ARCO chunk and probe latency, lowsweeps scan cost, volume size by weather regime) on the current machine and network link, then apply them to the nexrad-cloud-router cost model. Use when running NEXRAD work on a new machine or cluster, when the router's routing decision sits near its raw-vs-ARCO crossover, when the shipped constants look wrong, or when the buckets may have changed. Produces a dated calibration.json with provenance. Triggers - recalibrate, calibration, benchmark NEXRAD, cost model, crossover, how fast is this link, measure throughput, router constants, new machine, different cluster.
---

# Recalibrating the NEXRAD cost model

`nexrad-cloud-router` chooses between four access paths using constants
measured on one machine at one moment. Two of those constants travel badly:
**bandwidth** (set by the network path) and **volume size** (set by the weather
in the window sampled). This skill re-measures and applies them.

## 1. Run it

```python
doc = run_calibration(site="KLOT", quick=True)     # ~2-4 min
print(calibration_report(doc))
apply_calibration(doc)                             # writes into the router's COST
```

Drop `quick=True` for the full version (8 volumes instead of 2, plus
compressed-chunk sampling) when you want constants you will keep.

The measurement runs as a **subprocess** (`measure.py`), and that is
structural, not stylistic: the icechunk Rust client caches its TLS trust store
on first import, so a kernel that has already imported icechunk cannot be
corrected in place. Calling `run_calibration()` from a kernel that has already
done ARCO work is still fine — the subprocess is clean.

`measure.py` also runs standalone, which is what you want on a cluster login
node:

```bash
python measure.py --site KLOT --out calibration.json
python measure.py --site KTLX --quick --window 2026-07-27T16:00,2026-07-27T19:00
```

It needs `nexrad-aws-2025/kernel.py` for the bucket primitives — beside this
skill, under the working directory, or named by `NEXRAD_AWS_2025_KERNEL`.

## 2. Decide before you apply

Recalibration is not automatically an improvement — a noisy quick run can be
worse than a careful shipped constant. Look before applying:

```python
for r in compare_to_shipped(doc)[:5]:
    print(r)     # {'constant', 'shipped', 'measured', 'ratio', 'sensitivity'}
```

`sensitivity` says why a constant might differ:

| label | meaning | trust the measurement? |
|---|---|---|
| `link` | set by the network path | yes — this is what you came for |
| `weather` | set by what the radar was seeing | only if the window matches your case |
| `machine` | local CPU/disk | yes |
| `fixed` | array geometry | a change means the store's chunking changed |

Apply selectively when you trust only part of it:

```python
apply_calibration(doc, keys=["raw_MB_per_s"])   # bandwidth only
```

`should_recalibrate()` reports what to check without measuring anything.

## 3. What it measures, and the traps baked in

**Bandwidth and volume size come from different samples, deliberately.**
Bandwidth needs real transfers, so it is timed over the downloaded volumes.
Volume size must *not* come from those same few — in `quick` mode that is two
volumes, and two volumes from the end of a window are not the window. A
measured example: a window whose 36 listed volumes averaged **13.34 MB**
handed back two volumes averaging **8.46 MB**. Taking size from the download
sample would have understated it by 58% and pulled the crossover down with it.
Sizes are free from the LIST call, so all of them are used.

**It searches for a busy window rather than using "now".** Volume size is
bimodal — quiet ~6.7 MB against convective ~13.3 MB on KLOT — and calibrating
during fair weather produces constants that under-cost every convective case.
`busy_window()` scans recent days and takes the one with the largest mean
volume; the three regimes are sampled separately and written to
`VOLUME_MB_BY_REGIME`.

**Reassembly cost is separated from chunk cost.** Pulling a SAILS-fragmented
volume also probes every (sweep, index) pair to find which sweeps were
recorded. The probe term is measured on its own and subtracted, so
`arco_chunk_in_loop_s` is a real per-read cost rather than a blend.

## 4. Reading the output

`calibration.json` carries `COST`, `VOLUME_MB_BY_REGIME`, and a `provenance`
block with the site, timestamp, window, and the raw observations
(`_n_listed`, `_n_downloaded`, `_downloaded_mean_MB`, `_reassembly_s`, …)
behind each constant. Keep it next to any results whose runtime you quote.

A single `quick` run has real variance — ARCO chunk latency in particular
moved by ~2x between two runs minutes apart on the same link. If a routing
decision hinges on it, run the full version, or run `quick` twice and compare
before trusting either.

## 5. What the constants do

They set one thing: the **crossover**, the number of (sweep × field) chunks at
which downloading a whole raw volume beats reading pieces from ARCO. Below it,
ARCO; above it, raw. Halving bandwidth roughly halves the crossover, so the
same task routes differently on a slow link. Everything else in the router —
hard constraints on ray geometry and site coverage — is unaffected by
calibration and stays true regardless.

## Environment

Needs `nexrad-aws-2025` (bucket primitives) and, to apply, `nexrad-cloud-router`
loaded in the same kernel. `arm-pyart`, `icechunk`, `zarr`, `boto3`, `certifi`.
Project env: `radar`.

## Verified against

Live KLOT buckets on **2026-08-26**; 27 checks in `test_calibration.py` pass,
including two that assert the volume-size sampling trap stays closed and four
that assert `measure.py` still resolves when the sidecar is exec'd without
`__file__` from an unrelated working directory. The runs that produced them
measured a 0.5–1.2 MB/s link — varying by a factor of two between runs minutes
apart, which is itself the argument for measuring rather than assuming.
