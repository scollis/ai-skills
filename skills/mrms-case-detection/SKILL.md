---
name: mrms-case-detection
description: Detect heavy-rain and convective events over a fixed radar or instrument site from MRMS gauge-corrected QPE on AWS, confirm each candidate against independent surface networks (ASOS, mPING, CoCoRaHS, HADS), then retrieve and morphologically classify scanning-radar volumes. Use whenever the task is to find which hours are worth pulling radar for, screen a week or month of weather over a site, build or extend a radar case-study archive or database, rank storms by rainfall intensity, cross-check a rainfall claim against gauges, or classify volumes as QLCS / supercell / multicell cluster / isolated cells. Also the reference for MRMS-on-S3 access and the ARM Live retrieve-and-validate recipe. Triggers - MRMS, MultiSensor_QPE, noaa-mrms-pds, QPE, gauge-corrected precipitation, case detection, event detection, find events, which volumes to download, heavy rain screening, storm catalogue, ARM Live, C-SAPR2, BNF, mPING, ASOS precipitation, convective morphology, QLCS, supercell, multicell, storm mode.
---

# MRMS-driven radar case detection

Point gauges tell you it rained somewhere; a national gridded QPE tells you
*where and how hard*, on a grid fine enough to resolve individual convective
cores. That makes MRMS the right instrument for deciding which radar volumes are
worth the download, and gauges the right instrument for deciding whether to
believe the MRMS.

The workflow has a fixed shape, and the order is what keeps it cheap:

**detect on MRMS -> confirm against independent networks -> check radar
availability per event window -> retrieve a few frames -> classify -> file.**

Detection costs megabytes; radar costs gigabytes per volume. Every step before
retrieval exists to avoid downloading the wrong hour.

`kernel.py` loads with this skill and carries the access recipes and the traps
as executable functions. Read section 6 before asserting anything about
rotation, and section 7 before quoting any areal statistic.

## 1. MRMS on AWS

Bucket `s3://noaa-mrms-pds`, anonymous — `s3_anon()` returns a client with
unsigned requests. 243 CONUS products; the ones that matter for rainfall:

| Product | What it is | Use for |
|---|---|---|
| `MultiSensor_QPE_01H_Pass2_00.00` | gauge-corrected 1-h accumulation | **the default** — detection and any quoted accumulation |
| `MultiSensor_QPE_01H_Pass1_00.00` | earlier, less gauge input | when Pass2 is not yet available for a recent hour |
| `RadarOnly_QPE_01H_00.00` | no gauge correction | isolating radar-only bias; not for validation |
| `PrecipRate_00.00` | instantaneous rate, 2-min | sub-hourly timing once you know the hour |
| `PrecipFlag_00.00` | precip type classification | separating rain from snow/hail cases |

Keys are `CONUS/<product>/<YYYYMMDD>/*.grib2.gz`. **The 1-h QPE products are
hourly — 24 files a day, roughly half a megabyte each gzipped.** A week is about
95 MB, a month about 350 MB. That is small enough that a month of detection is a
few minutes of downloading, which is the whole reason this ordering works.

Five conventions in these files will each silently corrupt your statistics:

- Read with `engine='cfgrib', backend_kwargs={'indexpath': ''}` — without the
  empty `indexpath`, cfgrib tries to write an index file next to the data.
- **The variable is named `unknown`.** MRMS ships no standard name, so xarray
  cannot give it a better one. Don't guess at `precipitation` or `qpe`.
- **Longitude is stored 0–360** (CONUS spans 230–300 °E). Subtract 360 before
  comparing with a negative site longitude. Latitude *descends*.
- **Negative values are fill codes** (`-1` no coverage, `-3` missing). Set them
  to NaN before any max, mean or percentile. A mean over unmasked `-1`s is
  quietly wrong rather than obviously wrong.
- **The accumulation is hour-ending.** The grid valid at 04:00Z covers
  03:00–04:00Z. `mrms_hour_ending(t)` returns the right stamp for a time.

```python
idx = mrms_grid_index(files[0], site_lat, site_lon, radius_km=120)
t, mm = mrms_read_subset(files[0], idx)
domain_max = np.nanmax(mm[idx['mask']])
```

`mrms_grid_index` handles the descending-latitude and 0–360 subsetting and hands
back a range mask; `mrms_read_subset` handles the variable name and the fill
codes. Build a `(time, y, x)` cube from the per-file arrays and keep it — it is
cheap to store and expensive to re-download, so it belongs in a checkpoint.

## 2. Defining events

Per hour, over the range mask, compute the domain max, mean, and the *area*
exceeding a few thresholds. Area is what separates a genuine event from one hot
pixel: a single 60 mm cell is often ground clutter or a bright-band artefact,
while 2,000 km² above 25 mm is unambiguous.

A rule that has worked well over a mid-latitude continental site:

```
wet hour  = (area above 5 mm > 200 km²) OR (domain max > 10 mm)
event     = contiguous run of wet hours
```

Then rank events by peak 1-h accumulation and by `area > 25 mm`. Report every
detected event, but pull radar only for the intense subset — on a typical week
two or three events carry the weather and the rest are marginal.

Record for each event: start, end, duration, peak 1-h accumulation and its time,
max area above 10 and 25 mm. Those five numbers are what make events comparable
across periods.

## 3. Confirming against independent networks

MRMS is itself a radar-plus-gauge product, so treating it as ground truth for a
radar study is close to circular. Confirm with instruments that are not in the
MRMS ingest chain, or at least not in the same way.

**ASOS hourly precipitation** via the Iowa Environmental Mesonet request
service — `data=p01i, tz=UTC, format=onlycomma, report_type=3`, repeated
`&station=`. Values are **inches**; multiply by 25.4. This is the strongest
routine check: over one week of a continental domain, MRMS versus ASOS on wet
hours gave Spearman ρ ≈ +0.46 with a median bias of +1.2 mm and closely matching
maxima (55 mm gauge, 57 mm MRMS). MRMS reading slightly *wet* is expected — a
tipping bucket under-catches in heavy rain.

**mPING** crowdsourced reports for precipitation type and hail. Three things the
API does that cost a debugging cycle each: the host is `mping.ou.edu` (the older
`mping.nssl.ou.edu` name no longer resolves at all — DNS failure, not a
firewall), the endpoint path takes **no trailing slash** (a slash returns 404),
and the server-side `dist` filter **over-returns by roughly 10%**, so re-filter
on computed great-circle range. `mping_reports()` handles the pagination and the
`http://`-to-`https://` rewrite in the `next` links.

A fourth one is nastier because it looks like a real answer: the time filters
want a **space-separated** timestamp (`obtime_gte='2026-07-27 00:00:00'`). An
ISO string with a `T` and a `Z` — the form most APIs prefer, and the form the
docs suggest — returns `count=0` **silently** rather than erroring. An empty
result then reads as "no reports in this window", which is indistinguishable
from a genuinely quiet period. Whenever a time-filtered mPING query returns
zero, re-run it without the time filter before believing it.

**Fixed gauge networks** — CoCoRaHS, NWS COOP, HADS/DCP, USCRN — are worth
inventorying once per site. Two cautions: most CoCoRaHS and COOP stations report
a single 24-hour total, so they confirm *that* an event happened but cannot time
it; and GHCN-Daily in a given domain is substantially a re-publication of
CoCoRaHS and COOP, so counting it as independent double-counts. Deduplicate on
position (a few hundred metres) with a network-preference ranking before quoting
a station count.

**USGS NWIS parameter 00045 is a trap.** At many sites the series rises *and
falls* within an hour, so it is not a monotonic accumulator and cannot be
integrated as one. Naive summation produced 46,000 mm/h in one test; differencing
with a negative clamp produced 2.4 mm in a week against MRMS's 65 mm. Unless the
specific site's parameter documentation says otherwise, leave it out and say you
did.

Record per event how many stations recorded meaningful rain and how many
crowdsourced reports fell in the window. An event confirmed by two independent
networks is a case; an event visible only in MRMS needs a caveat.

## 4. Radar availability — per event window

**Count volumes inside the event window, never the whole day.** On a real event
the two differ by around threefold, and the day figure overstates what actually
observed the event. This is worth stating in any catalogue column header.

For ARM Live (`armlive_files`, `armlive_window`), two counting rules:

- The query range **spans into the end date**, so `start=D, end=D+1` returns two
  days of files. Filter on the date embedded in each filename, not on the query
  range.
- Filter on the hour in the filename to get the in-window count.

**Do not assume continuous radar coverage.** Research radars have outages,
calibration periods and campaign boundaries. In one week-long screening, volumes
existed on only four of eight days, and one of the two most intense events had
none at all. Check availability *before* planning a case study, and when an
event has no coverage, record that as a finding — "no radar data existed" and "I
chose not to download it" are different statements and a future reader needs to
know which applies.

## 5. Retrieval that fails loudly

Scanning radars often interleave scan strategies in one datastream. A HEAD
request reading `Content-Length` (`armlive_size`) identifies the scan type for
free — in the ARM `bnfcsapr2cfr` stream an RHI is ~18 MB and a PPI volume
~730 MB, and the PPI is the second of each pair about 43 s apart. Checking size
before downloading saves five minutes per wrong guess.

Then transfer with resume and a stall guard, and **validate every file**:

```
curl -sL -C - --speed-limit 20000 --speed-time 120 "<url>" -o "<out>"
```

**Magic bytes are not enough.** A stalled transfer writes a valid HDF5 header
and then stops, so the file passes a magic-byte check and fails only when
something reads deep into it. A 78 MB fragment of a 720 MB volume passed a
magic-only gate here and was caught afterwards by netCDF4 raising `HDF error`
on open — the stall guard had fired, the exit status was 0, and the logged rate
(0.38 MB/s against a 2.4 MB/s batch median) was the only hint. `armlive_fetch()`
therefore applies three checks, cheapest first: magic bytes (catches an HTML
error body), size against `Content-Length` (catches truncation without opening
the file), and `armlive_readable()`, which reads the **last element** of the
largest variable — a truncated file keeps its dimensions and metadata intact,
so anything that merely opens it or reads attributes will call it healthy. A
size or readability failure keeps the partial file so `curl -C -` can resume;
only a bad-magic file is deleted, since an HTML body is never resumable.
A batch-level check is worth running too: flag any file whose size deviates
from the batch median, which is what made the 78 MB outlier obvious.

Pick frames that span the event's intense hours rather than three consecutive
volumes — the point is to capture evolution. And budget the disk: three volumes
per event across eight events is around 17 GB.

## 6. Classification, and the limit of reflectivity

Classify from *gridded* structure, not from raw sweeps — object geometry needs
constant-altitude horizontal slices. Grid with Py-ART (`grid_shape` and
`grid_limits` are **`(z, y, x)`**; `gatefilters=` takes a **tuple**, one per
radar), take a level below the melting layer, threshold for convection, and
measure objects. `convective_morphology()` returns the numbers that matter:

| Quantity | What it discriminates |
|---|---|
| number of objects | cluster vs a few cells |
| largest object's **share** of convective area | whether one storm dominates |
| principal-axis aspect and major length | line vs blob |
| total convective area | whether it is convective at all |

`classify_morphology()` maps these onto class names and returns the reason
alongside the label:

| Class | Reached when |
|---|---|
| `light_drizzle` | convective area below ~20 km² **and** no intense or deep echo |
| `qlcs` | one object holds >60% of convective area, aspect ≥3, major axis ≥25 km |
| `multicell_cluster` | ≥8 objects and no object above 60% share |
| `isolated_cells` | a few discrete cores, none dominant enough to be a line |
| `supercell` | **only** with dealiased velocity — see below |

The share is the key discriminator: a QLCS is one dominant elongated object,
whereas 15–20 cores with the largest holding a fifth of the area is a
`multicell_cluster` no matter how intense the individual cores are. The
thresholds above are defaults worth re-tuning per radar and per gridding recipe;
what should not move is which evidence each class rests on.

**Pass `zmax` and `echo_top_km`, and note the ordering.** The intensity gate they
feed runs *before* the small-area test, because area alone mislabels scattered
deep convection: a frame carrying 47–55 dBZ cores and a 12 km echo top can hold
only 12–19 km² of contiguous ≥40 dBZ once isolated pixels are opened away, and an
area-only rule files it as `light_drizzle`. Small area plus high intensity is
isolated convection. Without those arguments the classifier falls back to area
alone, which is the behaviour that produced the mislabel.

**Choose the classification level by beam geometry, not convention.** A fixed
2 km AGL level looks natural and is wrong over a wide domain: at 1.5° elevation
the lowest beam centre is 2.15 km at 70 km range and 4.08 km at 120 km, so 2 km
AGL sits *below* the lowest beam over most of a 120 km domain and gridded values
there are downward extrapolations. Classifying nine frames both ways disagreed on
**4 of 9**, always toward more cores and larger area on the composite. Use
**column-max composite** reflectivity, and render the PPI to check the metrics
against what is visibly present — the tell in this case was a frame reported as
"1 core, 100% share" that plainly showed several separate echo regions.

**Reflectivity morphology cannot establish a mesocyclone, so do not assign
"supercell" from it.** A supercell is defined by a persistent rotating updraft,
which is a *velocity* signature. Reaching it honestly requires dealiased
velocity: `classify_morphology()` therefore gates that class behind an explicit
`dealiased=True`. Research radars often have a low Nyquist velocity (~16 m/s is
common at C band), and on a folded field an apparent couplet may be an artefact.
`azimuthal_shear()` returns an `aliased_frac` alongside the percentiles for
exactly this reason — and a sanity anchor: **mesocyclone-scale azimuthal shear is
of order 0.01 s⁻¹**, so values of 0.1–0.3 s⁻¹ are noise, not rotation.

Two array traps live in this neighbourhood and both fail silently:

- **`scipy.ndimage.uniform_filter` propagates NaN across its entire window.**
  Smoothing a velocity field with a few bad gates can return an all-NaN array,
  which reads downstream as "no data" rather than as a bug. Use normalised
  convolution — `smooth_nan_aware()` does this.
- **A boolean comparison on a numpy masked array yields *masked*, not `False`.**
  `z > 30` on a masked `z` produces a mask that empties the downstream selection.
  Call `np.ma.filled(z, -999)` before comparing.

When a morphology genuinely does not fit the existing classes, adding one is
better than forcing a bad label — but write down the metrics that ruled out each
alternative, so the class means something to whoever reads the archive next.

## 7. Reporting that survives review

These numbers end up in a database someone trusts later, so calibration matters
more than volume.

- **Name the QC recipe with any areal statistic.** Gate-filter choice moves an
  areal mean rain rate by a factor of about two on identical data. A number
  without its filter is not reproducible.
- **Per-window radar counts**, with the day total only in parentheses if at all.
- **Say which class a count refers to.** If you draw or analyse a subset,
  quoting the parent total overstates it — count what you actually used.
- **Report disagreement between MRMS and the gauges** rather than the flattering
  source. A factor-of-two spread across QC recipes is normal; hiding it is not.
- **Distinguish absent data from skipped data**, explicitly.
- **Verify georeferencing on any site-centred map.** Transform the site's own
  coordinates and assert they land at the origin, then compare a few plotted
  ranges against independently computed great-circle ranges; agreement should be
  sub-kilometre. On a cartopy azimuthal-equidistant projection, passing
  `PlateCarree` as the *source* CRS for point data displaces markers by tens of
  kilometres at mid-latitudes — use `Geodetic`. Cartopy refuses `Geodetic` for
  `pcolormesh`, so pre-transform the mesh with `proj.transform_points(Geodetic,
  ...)` and plot in projected metres rather than falling back to `PlateCarree`.

## 8. Filing

Separate the two kinds of output, because they have different lifetimes:

- **Radar volumes** into the archive's own taxonomy — typically flat per-class
  directories holding the files directly. Check the existing convention before
  inventing a layout.
- **Analysis products** (event catalogues, hourly series, figures, notes)
  somewhere else entirely. They are small, they change often, and they should not
  be mixed in with multi-gigabyte binaries.

Each filed case wants a note recording: how it was selected and by what
threshold, the confirming networks and their counts, the classification with the
metrics behind it *and the alternatives ruled out*, the QC recipe, and the
caveats — especially any comparably intense event that could not be studied for
lack of coverage. That last item is what stops a future reader mistaking the
archive for a climatology.

## Sidecar

`kernel.py` defines: `s3_anon`, `great_circle_km`, `mrms_list_day`,
`mrms_fetch`, `mrms_grid_index`, `mrms_read_subset`, `mrms_hour_ending`,
`armlive_files`, `armlive_window`, `armlive_size`, `armlive_fetch`,
`mping_reports`, `mping_timestamp`, `smooth_nan_aware`, `azimuthal_shear`,
`convective_morphology`, `classify_morphology`.

Needs `boto3`, `cfgrib`, `xarray`, `scipy` for detection; `arm-pyart` for
classification.

## Siblings

`arm-site-week-survey` finds events from ARM's own surface and profiling
datastreams — use it when the question is what the instruments saw; use this
skill when the question is where the rain was on a grid. `arm-bnf-storm-case-study`
takes a single known BNF event deep, including dual-pol and lightning.
`pyart-gridding` and `pyart-retrievals` cover the gridding parameters and
derived products; `nexrad-site-rainfall` is the WSR-88D analogue when no
research radar is available.

## Verified against

Live services on **2026-08-27**, over the ARM BNF C-SAPR2 domain (34.6308 N,
-87.1331 E, 120 km):

- **MRMS/S3** — `MultiSensor_QPE_01H_Pass2_00.00` read for 27 Jul – 20 Aug 2026:
  600 hourly grids, 374 MB decompressed, full valid coverage over the 44,468-cell
  mask. All five grid conventions in section 1 exercised on those files.
- **Event rule** — 32 events detected in that window, 15 with peak 1-h ≥ 30 mm.
  An earlier 7-day run over the same domain gave 8 events, 4 independently
  confirmed.
- **MRMS vs ASOS** — 120 wet hours: Spearman ρ = +0.457 (p = 1.6e-07), median
  MRMS-minus-gauge bias +1.17 mm, maxima 55.1 mm gauge vs 57.4 mm MRMS.
- **mPING** — space-separated `obtime_gte` returned 292 raw / 282 in-range / 187
  precip-relevant reports; the ISO `T…Z` form returned `count=0` silently on the
  same window, which is what the helper now normalises away.
- **ARM Live** — a nine-day C-SAPR2 outage (9–17 Aug 2026) found by per-window
  counting. Of the three most intense events, two fall inside it and cannot be
  studied (11 Aug, 65.0 mm/h; 09 Aug, 62.3 mm/h), while a third at the same
  62.3 mm/h began on 08 Aug just before the outage opened and has 19 in-window
  volumes covering only its first hour, three hours before its peak — a
  same-day gap, not the multi-day one. Content-Length
  discriminator measured at ~18 MB (RHI) vs ~730 MB (PPI).
- **Throughput** — highly variable, so treat any single figure as a sample, not a
  constant. ARM Live single-stream, 9 timed transfers of ~724 MB volumes:
  per-transfer median 10.75 MB/s, range 5.96–12.49, mean 9.77 (σ 2.43),
  6,351 MB in 694 s; an earlier session on the same endpoint saw 1.8–2.7 MB/s.
  The spread was structured rather than random — volumes from two event dates ran
  9.9–12.5 MB/s while all three from a third ran 6.0–8.2, suggesting server-side
  variation. A third batch ~40 min later ran at 2.47–2.48 MB/s across three
  consecutive volumes (spread 0.01 MB/s — a hard ceiling, not jitter), matching
  what an earlier session had seen. **The endpoint is bimodal**, moving between a
  ~2.5 MB/s and a ~10 MB/s regime, so no stored figure predicts the next batch:
  time the FIRST volume and extrapolate from it. The difference is 20 min versus
  75 min for a 15-volume pull, which is exactly when it is worth asking whether a
  no-concurrency preference still holds. MRMS/S3 sequential: 600 files, 350 MB wire in 696 s, per-file median
  0.61 MB/s, aggregate 0.50 MB/s; the same pull with 16 threads ran ~3× faster in
  files/second. Exclude interrupted transfers before computing a rate: a stalled
  request inflates `time_total` and produced a spurious 2.47 MB/s outlier here. The asymmetry is the useful part: at ~0.6 MB per MRMS file
  request latency dominates and concurrency pays, whereas at ~724 MB per volume
  transfer dominates and single-stream costs little. Quote a median over several
  files, never one measurement.
- **A VPN does not help, and costs a little.** Tested directly: six ~723 MB
  volumes over VPN gave a per-file median of 2.08 MB/s (range 2.04–2.21) against
  2.48 MB/s without it on the same day — about 16% slower, consistent with tunnel
  overhead on a link that is not the bottleneck. The diagnostic that identifies a
  server-side ceiling before you try to work around it is the **per-file spread**:
  consecutive near-identical files landing within 0.01–0.2 MB/s of each other is
  metering at the far end, not local contention, and no amount of re-routing will
  lift it. Reach for concurrency (~3× on small files) rather than tunnelling.
- **Classification** — thresholds exercised on three 21 Aug 2026 PPI volumes
  (15–20 cores, largest 21–43% of convective area, aspect 2.9–4.3, peak 61 dBZ,
  tops 16 km), classified `multicell_cluster`. Gate filter NCP ≥ 0.4,
  RhoHV ≥ 0.7; 1 km grid, `dist_beam` nb=1.5 bsp=1.0 min_radius=500, Barnes2.
  Measured azimuthal shear p90 0.011 s⁻¹, p99.9 0.036–0.071 s⁻¹, no ray-to-ray
  aliasing — but C-SAPR2's 16.3 m/s Nyquist means velocity was not dealiased, so
  `supercell` was not asserted for any frame.

The 13 checks for this skill in `tests/test_structure.py` assert the documented
product, hour-ending convention, fill-code floor, timestamp normalisation,
endpoint form, the dealiasing gate on `supercell`, class-name agreement between
code and prose, NaN containment in the smoother, and per-window volume counting.
Re-verify the MRMS product path and the mPING host if much time has passed.
