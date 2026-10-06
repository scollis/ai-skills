---
name: nexrad-decade-archive
description: "Build a multi-year WSR-88D NEXRAD Level II archive as analysis-ready Zarr with gate-ID classification and range-dependent MDS backfill. Covers case screening and priority ordering, container and codec choice on constrained filesystems, bit-exact int16 round-trip verification, georeference persistence, resumable per-case checkpointing, and measured throughput. Worked example: KDVN (Davenport IA) decade build for the DOE ARM DERECHOS campaign."
---

# Building a multi-year NEXRAD Level II -> Zarr archive

Procedure and measured constraints for converting years of WSR-88D Level II
volumes into a self-describing, analysis-ready Zarr archive. Every number marked
*(measured)* was measured during the KDVN decade build on a 14-core / 36 GB
macOS machine; re-measure on your own hardware before budgeting.

## The decision order that matters

These four questions must be answered **in this order**. Answering them out of
order is how a build produces an archive that is provably faithful and still
useless.

1. **Is the site in an analysis-ready store?** Check before assuming raw access
   is necessary. If a Zarr/Icechunk cube exists for the site, long base-tilt
   series are far cheaper from it. *(measured)* For KDVN it did not exist, which
   forced raw Level II and made cheap gridded screening the load-bearing layer.
2. **What does the target filesystem actually cost per file?** See below. This
   decides the container before any codec question.
3. **What must be persisted for the archive to be self-sufficient?** Moments
   alone are not enough. See "Georeference".
4. **Only then**: codec, chunking, compression.

## Source access

- Bucket: `s3://unidata-nexrad-level2`, keys `YYYY/MM/DD/<SITE>/<SITE>YYYYMMDD_HHMMSS_V06`.
  Skip `*_MDM` keys when listing.
- The legacy `noaa-nexrad-level2` bucket returns a genuine `AccessDenied` and
  has **no fallback**. Do not build a retry path against it.
- Anonymous access: `boto3` with `signature_version=UNSIGNED`. Prefer `boto3`
  directly over `s3fs` unless you have verified the installed `s3fs` version;
  conda has been observed resolving it to an ancient 0.4.2.
- *(measured)* Download is **not** the bottleneck: 7.61 MB/s serial, 15.98 MB/s
  at 16 threads, with per-volume latency flat at 0.98 s from 8 to 16 threads
  (scales linearly, had not saturated). A later re-fetch measured 17.28 MB/s at
  12 threads. **CPU and memory are the constraints.**
- **Integrity**: verify `Content-Length` on every object and write
  `.part`-then-`os.replace`. A dropped connection returns EOF rather than
  raising, so a truncated volume reads clean and fails hours later. Retry with
  backoff on `IncompleteRead`.
- *(measured)* Era matters. Pre-2017 objects are whole-file gzipped
  (`*_V06.gz`); they decode fine (0.71 s) and compress *better* than modern
  dual-pol volumes. Discriminate on the **key suffix**, not the year.
- Watch for non-canonical re-archive fragments (`*_V06.001`) with duplicate
  timestamps. *(measured)* One case had 254 objects covering 247 distinct
  observation times; dropping the 7 fragments lost no observation time.

## Filesystem cost model - measure before choosing a container

**Always measure real size with `du`, never the logical sum of array bytes.**
On the KDVN staging volume they differed by orders of magnitude.

*(measured)* On exFAT with a ~1 MiB cluster size, where macOS writes an
AppleDouble `._` shadow per file: **200 files of 512 B consumed 401 MB of real
disk** - roughly 2 MiB per logical file. Small-file writes were ~5x slower than
on APFS.

*(measured)* Same 61.5 MB of real data, three containers:

| container | on-disk | files |
|---|---|---|
| **ZipStore** | **61.87 MB** | **1** |
| Zarr v3 sharding | 349.18 MB | 196 |
| plain directory store | 3054.50 MB | 1945 |

**Sharding lost for a non-obvious reason: the overhead is per ARRAY, not per
chunk.** The shards themselves spanned 2.1-14.9 MiB. But 29 arrays each bring a
nested `c/0/0/0` directory chain, a `zarr.json` and an AppleDouble shadow, and
each of those consumes a full cluster. So on a large-cluster filesystem the rule
is stronger than "keep files large" - **keep the file count near one**. One
`ZipStore` per case.

Other constraints on such volumes: no POSIX permissions or symlinks; `git`
cannot create a `.git` directory (clone repos elsewhere and move bundles);
filter `._*` entries out of every listing and file count.

## Encoding

Store moments as **int16 with scale/offset matching the instrument's native
quantisation** (NEXRAD reflectivity is already 0.5 dB steps on disk, velocity
0.5 m/s). This is **bit-exact against the source, not an approximation**, and
roughly halves the bytes before the codec runs - integers compress far better
than float32 mantissas.

*(measured)* Codec choice, counter to general advice: **byte shuffle beat
bitshuffle** (60.98 vs 67.45 MB) with zstd, because these are 8-bit codes in an
int16 word - the high byte is constant, and byte-grouping hands zstd a long
constant run that bitshuffle scatters.

*(measured)* The codec compresses the logical int16 cube **28.2x**. But the
product is still slightly **larger** than the Level II it replaces - realised
on-disk ratio **1.028-1.048** for modern cases, and **0.865-0.915** for gzip-era
cases (those come out smaller). Budget ~1.03x overall.

**Consequence worth stating plainly: converting to Zarr is not a space saving.**
Level II stores only the gates the radar detected; a dense cube materialises
every gate, and MDS backfill alone costs +3.1%. If your justification for
deleting sources was disk space, that justification is void - re-check it before
deleting anything.

## Georeference - the trap that nearly cost a decade

**A bit-exact moment round-trip does NOT make an archive self-sufficient.**

*(measured)* The KDVN archive stored per-sweep `fixed_angle`, `ray_time`,
`n_rays`, `n_gates` and the site coordinate - and was still ungriddable, because
it lacked:

- per-ray **azimuth**
- the **range** axis
- the antenna **altitude**

None is recoverable by convention: *(measured)* one volume's sweep 0 began at
azimuth 351.263 deg and another's at 143.264 deg, with a median spacing of
0.4834 deg rather than the nominal 0.5. So neither the origin nor the step can
be assumed, and ray index cannot yield azimuth at all. The tracking stage
silently re-downloaded the sources to recover geometry.

**Persist `azimuth`, `elevation`, `range_m` and `radar_altitude_m` per volume.**
*(measured)* The increment is **0.151 MB/volume** (~21 MB for a 140-volume case)
against ~11 MB/volume to re-download - a re-download is ~73x more expensive per
volume, and stops working the day the sources are cleaned up.

Read the antenna altitude from a volume (`radar.altitude`); do not hardcode it.

For an archive already built without geometry, a **sidecar geometry cache** is
the cheap retrofit: *(measured)* ~6.7 MB per case (161 MB for 24 cases) against
~2.6 GB per case of retained sources, and it needs no rewrite of the stores.

## Gate-ID on WSR-88D - requires a censored SNR

*(measured)* A fuzzy-logic gate-ID classifier tuned on research radar does
**not** transfer to Level II out of the box, because **Level II carries no SNR
field**. That silently disables the power half of the noise-floor test and
leaves the no-scatter class below its evidence threshold, so empty air is won by
whichever class has a geometry-only term: **33.2% unclassified, 43.2% ice_snow,
8.6% heavy_rain - all of it clear air.**

The fix is to synthesise a **censored SNR** from the MDS model,
`SNR = Z - Zmin(r)` with non-detections at 0 dB. *(measured)* That took
unclassified to **0.0%**.

Also expect instrument-specific thresholds (an incoherence/texture fraction
tuned on another radar needs its own WSR-88D value) and check field-naming
assumptions against the actual Py-ART field names.

**Never recompute gate-ID from a raw volume for downstream analysis.** Read the
archive's stored classification. *(measured)* Recomputing without the censored
SNR gave 67.6% of gates classed meteorological with a median of -33 dBZ, against
9.8% from the correctly-computed stored field on the same volume.

## Range-dependent MDS backfill

Fill non-detection gates with the minimum detectable reflectivity at that range,
`dBZ_min(r) = dBZ0 + 20*log10(r/r0)`, with `dBZ0` calibrated per volume from the
weakest-echo envelope. A non-detection becomes a **censored value rather than a
gap**.

This turns out to be load-bearing for three separate things, none of them
storage:

1. **Gate-ID cannot function without it** (above).
2. **It conditions the field for spectral gridding.** A masked field with a hole
   at every non-detection has no well-defined spectrum - a transform would act
   on an arbitrary fill or an irregular support. Range-dependence rather than a
   scalar floor is what keeps the censored background as smooth as the
   sensitivity itself; a constant floor plants ~20 dB steps across the domain at
   exactly the ranges a spectral method is most sensitive to.
3. **It makes area-over-threshold statistics well posed** - censored values, not
   holes.

**Never reimplement the envelope inline.** Call the package's own function.
*(measured)* A hand-rolled version with the wrong reference range made three
CFAD panels disagree by 25 dB on modal reflectivity; with the library function
all three agreed within 1.4 dB.

Keep the classification field alongside the moments so measured and synthesised
gates stay distinguishable without a separate mask array - the no-scatter class
carries that distinction at no extra cost.

## Volume decoding traps

- **Detect VCP and sweep configuration per volume.** Sweep count is not a
  property of the VCP number: *(measured)* 61 consecutive volumes all reporting
  VCP-212 split into 17-, 21- and 24-sweep configurations under MESO-SAILS and
  MRLE.
- **Split cuts** repeat the lowest tilts (surveillance + Doppler). Never select a
  sweep by field-iteration order. De-duplicate to one sweep per tilt on an
  explicit rule (e.g. earliest sweep within 2% of the group's best valid-gate
  count).

## Header corruption: a zeroed `fixed_angle` that per-ray elevations survive

*(measured)* One volume in ~9,000 decoded 21 sweeps and 11,160 rays with per-ray
elevations correctly spanning 0.43-19.47 deg, but its **`fixed_angle` array read all
0.0** — the same unreadable header that left its VCP at -1. A gridder that
de-duplicates sweeps *by elevation* then collapsed 21 sweeps into one and refused the
volume for having a single distinct elevation. Neither the gridder nor sweep selection
was at fault: the geometry was read from the one place it was corrupt.

**Guard for it explicitly.** If the per-sweep nominal elevations have zero spread while
the per-ray elevations do not, take the nominal angles from another source (the archive's
own `fixed_angle`, if it was written from a good read) and **record the substitution per
volume** — e.g. an `n_fixed_angle_from_archive` count — so it is never silent. Validate
the substitute against the surviving per-ray values (*(measured)* archive sweep-0 median
0.48 deg vs source per-ray 0.48).

The loss is not one volume. *(measured)* Dropping it left a 788 s gap against a 282 s
median cadence, which a temporal-gap guard correctly split into separate linking
segments — so one bad header fragmented a case into four.

Audit the scope rather than assuming it is isolated: count affected volumes across every
case. *(measured)* Exactly one volume in that lane was affected.

## Case screening and build order

For a site with no analysis-ready store, a continuous multi-year conversion is
usually infeasible - *(measured)* a decade of continuous KDVN Level II is ~7.2 TB
and ~1,900 serial hours. Screen first, then convert cases.

- Run **at least two independent screens** with different biases (gridded QPE,
  storm reports, objective wind-swath days) and **report the disagreements as a
  result**. *(measured)* 51% of wind-swath days carried no heavy-rain signal, and
  71% of QPE events produced no severe report.
- **Order the build by science stratum, not by the screening metric.**
  *(measured)* Derecho cases sat at mean rainfall rank 149 of 229 because wind
  swaths are rainfall-*weak*, so converting in rainfall order would have done the
  campaign-relevant cases last. Priority ordering means any interruption leaves a
  scientifically coherent subset.
- **Interleave lanes down the priority order** so both halves descend it
  together, and give each lane exclusive ownership of its rows. **A lane must
  never adopt another lane's case**, even one recorded as failed - two writers on
  one output path is a corruption race.
- Expect **window overlap between adjacent cases**. *(measured)* 9,083 case-volume
  rows covered only 8,205 distinct volumes; 878 volumes belonged to two cases
  each across 17 pairs, affecting 31 of 55 cases. Every store is individually
  correct - the duplication is *between* cases, from how windows were cut. Keep
  per-case tables un-deduplicated and apply a deterministic rule at pooling time
  (e.g. nearest window centre, ties by build order).

## Resumable checkpointing

A multi-day build must survive interruption. What actually works:

1. **One self-contained container per case** - a case is either
   complete-and-verified or absent, never half-written.
2. **Write to `.part` and rename only after the round-trip test passes.**
3. **Flush the manifest row and speed-log row after EVERY case**, with atomic
   temp-then-rename, never an open append handle.
4. **Read the manifest at startup and skip verified cases**, so re-invocation is
   idempotent.
5. **Per-case heartbeat line** to a log file, so progress is visible from outside
   the process.
6. **Priority order**, so any stop point is a usable subset.

**The round-trip test is what licenses deleting a source.** Read the store back
and assert exact integer equality against the decoded original; record the
result in the manifest; only then remove the source. Never delete a volume whose
verification did not pass, and **never repair by deletion** - a suspect
final-named store gets reported and left in place.

*(measured)* 133.9 billion gates compared bit-exact with zero mismatches in one
lane, and exactly one volume in ~9,000 failed to decode.

## Throughput and the memory ceiling

*(measured)* Per-stage, per volume: gate-ID dominates. A naive first reading gave
19.9 s/volume; after fixes the pool optimum was **5.19 s/volume at 6 workers**,
degrading to 5.48 at 8 and **10.03 at 12** - the degradation is paging, not
contention.

**The binding constraint is memory, not cores.** *(measured)* Peak worker RSS
was 4.47 GB in benchmarks but **5.2-7.9 GB on real convective cases**, so 36 GB
supported ~2 workers per lane, not 6. Production ran 10.6-10.8 s/volume
end-to-end.

Practical consequences:

- **Size the pool from live available memory per case**
  (`min(cap, floor(avail_GB / measured_GB_per_worker))`), not from a constant.
  Then a restart picks up memory the user frees, and a growing neighbour process
  makes the next case size down instead of thrashing.
- Use **threads for download, processes for processing**.
- Set **`maxtasksperchild`** (6 worked). *(measured)* Per-volume time climbing
  within a case was worker heap accumulation - each task building a fresh Radar
  object that is not returned to the OS - not the retained data.
- **Log system free memory, not just RSS.** `ru_maxrss` is a high-water mark
  that cannot decrease, so it can never evidence growth either way. Free memory
  is what predicts paging.

## Failure modes to guard against

- **A failed process listing is indistinguishable from a dead process** in a
  sandbox. Never conclude liveness from `ps`/`pgrep` failing. Use load average
  and the modification time of the process's own scratch tree. *(measured)*
  Trusting `ps` spawned three overlapping runner instances, which caused the
  first corruption.
- **Never quote a value whose denominator or units you have not established.**
  Reading a file is not the same as reading its units. Three separate
  misattributions in one build came from this: a per-level deficit census quoted
  as a ringing bound; a whole-store size quoted as a per-volume increment
  (90x error); an all-thresholds rate compared against a single-threshold rate
  (order-of-magnitude error).
- **When correcting a published number, search its magnitude phrasings, not its
  literal string.** A paraphrase ("already nearly 3x") survived a grep for
  `2.9x`.
- **Check code against prose.** A verdict document stating that detection ran on
  one field while the code used another went unnoticed until diffed.
