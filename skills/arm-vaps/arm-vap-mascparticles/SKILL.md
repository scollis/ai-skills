---
name: arm-vap-mascparticles
description: ARM Multi-Angle Snowflake Camera Particle Analysis (mascparticles) - value-added product reference from its technical report. Derived from masc. The retrieval algorithm, reported quantities (Fallspeed, Maximum dimension, Geometric cross-section, Area-equivalent radius, Perimeter, Orientation), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (nsamascparticlesavgC1.c1) and the variable inventory of a real file. Use when working with mascparticles data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - mascparticles, Multi-Angle Snowflake Camera Particle Analysis, nsamascparticlesavgC1.c1, masc VAP, Fallspeed, Maximum dimension, Geometric cross-section, Area-equivalent radius, Perimeter, Cloud Properties.
---

# MASCPARTICLES - Multi-Angle Snowflake Camera Particle Analysis

The MASC particle analysis VAP derives per-particle geometric, textural, and fall-speed properties of hydrometeors from Multi-Angle Snowflake Camera (MASC) triple-camera imagery and near-infrared trigger timing, aggregated into per-particle and 5-minute time-bin datastreams.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 74 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mascparticles` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-187 / K Shkurko, T Garrett, A Talaei, K Gaustad / March 2018](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-187.pdf) |
| Category | Cloud Properties |
| Input instruments | `masc` |
| Record | 2015-11-01 to 2025-05-20 (retired) |
| Datastreams with data | 4 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mascparticles |


## Credit

Everything this skill knows about the retrieval is the work of **K Shkurko, T Garrett, A Talaei, K Gaustad** -
the ARM developers and mentors who wrote the technical report it derives from:

> K Shkurko, T Garrett, A Talaei, K Gaustad. *Multi-Angle Snowflake Camera Particle Analysis Value-Added Product*, DOE/SC-ARM-TR-187, March 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-187.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The MASC consists of three cameras separated by 36 degrees, each aimed at a common focal point, with near-infrared emitter-detector arrays separated vertically by 32 mm that trigger all cameras and lights simultaneously when a hydrometeor passes; fallspeed is calculated from the transit time between the upper and lower trigger arrays. The VAP processes each of the three images per particle using OpenCV: images are cropped to remove IR emitters, foreground pixels are separated from background via brightness thresholding and Otsu's binarization, edges are found via Canny and contours extracted using the Suzuki 1985 border-following algorithm. For each contour (region of interest), bounding box, area, perimeter, best-fit ellipse (Fitzgibbon 1995 algorithm), and mean/variability of pixel intensity are computed, from which maximum dimension, geometric cross-section, area-equivalent radius, perimeter, orientation, aspect ratio, complexity, and flatness are derived. Contours are filtered using six parameters (size, maximum pixel intensity, pixel intensity variability, edge-touch length, focus measure, and ROI bottom position); particles are then averaged first across up to three per-particle images and then aggregated into 5-minute time bins using only particles that pass all quality filters.

**Cadence.** input rate Per-particle event-triggered capture (max detection frequency 2 Hz at input instrument); output every Per particle (mascparticles.c1) and 5-minute time bins (mascparticlesavg.c1); averaging Per-particle: average of up to 3 camera images passing filters; per-time-bin: average over all valid particles within 5-min bin (bin bounds -150,150 sec) (hb p. 5).

## Inputs

ARM's catalog declares these input instrument classes: `masc`.

The report names these instruments and sibling products: Multi-Angle Snowflake Camera (MASC) raw imagery (olimascM1.b1).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Fallspeed | m/s | valid_min 0, valid_max 10... | - | (hb p. 47) |
| Maximum dimension | mm | - | - | (hb p. 6) |
| Geometric cross-section | mm2 | warn_min 0.04 | - | (hb p. 6) |
| Area-equivalent radius | mm | - | - | (hb p. 6) |
| Perimeter | mm | - | - | (hb p. 6) |
| Orientation | degrees | - | - | (hb p. 6) |
| Aspect ratio | unitless | - | - | (hb p. 7) |
| Mean pixel intensity | unitless | [0,1]; warn_min 0.2 | - | (hb p. 7) |
| Intensity variability | unitless | [0,1]; warn_min 0.019 | - | (hb p. 7) |
| Complexity / habit | unitless | 1 = circle; less than 1.35... | - | (hb p. 7) |
| Flatness | unitless | 0 = sphere; requires greater than... | - | (hb p. 7) |
| Rain flag | unitless | 0, 1, or NA | - | (hb p. 7) |
| Particle edge touch | mm | warn_max 0.5 | - | (hb p. 8) |
| ROI bottom vertical position | mm | warn_min 32, warn_max 36 | - | (hb p. 8) |
| ROI focus | unitless | warn_min 0.01 | - | (hb p. 9) |
| Number of objects in frame | unitless | - | - | (hb p. 9) |
| Number of images used for average (per particle) | unitless | valid_min 1, warn_min 2 (2 for... | - | (hb p. 9) |
| Number of images used for average (per time bin) | unitless | valid_min 10 (for 5-min bin; 60... | - | (hb p. 9) |
| Number of particles total per time bin | unitless | - | - | (hb p. 16) |
| Number of particles used for average per time bin | unitless | - | - | (hb p. 16) |
| maximum_dimension | mm | - | - | (hb p. 57) |
| particle_area | mm^2 | - | - | (hb p. 58) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| additionalImageCrop | top 460, bottom 360, left 600, right 600 pixels | (hb p. 40) |
| backgroundThreshold01 | 0.03 (= 7.6/255) | (hb p. 40) |
| lineFillInMicrons | 200 microns | (hb p. 40) |
| minFlakeSizeInMicrons | 200 microns | (hb p. 40) |
| maxEdgeTouchLengthInMicrons | 500 microns | (hb p. 40) |
| minMaxPixelIntensity01 | 0.2 (range [0,1]) | (hb p. 40) |
| rangeIntensityThreshold01 | 0.01961 (= 5/255) | (hb p. 40) |
| flagRejectOutOfFocus | 1 (should always be set to 1) | (hb p. 41) |
| focusThreshold01 | 0.01 | (hb p. 41) |
| boundingBoxThresholdInMM bottomMin/bottomMax | bottomMin 33, bottomMax 39 mm | (hb p. 41) |
| horizFOVPerPixelInMM (per camera) | 0.030637255 mm (= 75mm/2448 pixels) | (hb p. 41) |
| binWidthInSec | 300 sec (5 min) | (hb p. 42) |
| maxFallSpeedInMetersPS | 5 m/s | (hb p. 42) |
| minNumParticlesPerBin | 10 | (hb p. 42) |
| snowflake_fall_speed valid_min/valid_max/warn_max | valid_min 0, valid_max 10, warn_max 5 m/s | (hb p. 47) |
| geometric_cross_section warn_min | 0.04 mm^2 | (hb p. 52) |
| mean_pixel_intensity warn_min | 0.2 | (hb p. 52) |
| mean_pixel_intensity_variability warn_min | 0.019 | (hb p. 53) |
| roi_focus warn_min | 0.01 | (hb p. 54) |
| roi_bot_position warn_min/warn_max | warn_min 32, warn_max 36 mm | (hb p. 55) |
| particle_edge_touch warn_max | 0.5 mm | (hb p. 49) |
| Cameras (input instrument) | Unibrain Fire-i 980b grayscale, max resolution 2448 x 2048 pixels | (hb p. 9) |
| Lenses (input instrument) | 12.5 mm Fujinon Megapixel C-mount lens, 75 mm horizontal field of view, 30.5 micron horizontal resolution per pixel | (hb p. 9) |
| Exposure (input instrument) | 40 microsec (1/25,000 sec) | (hb p. 9) |
| NIR detectors (input instrument) | detect hydrometeors with max dimension greater than  0.1 mm; max detection frequency 2 Hz | (hb p. 9) |
| flagSaveCroppedImages | false | (hb p. 63) |


_6 further rows in the report._

## The data

Verified example: **`nsamascparticlesavgC1.c1`**, file `nsamascparticlesavgC1.c1.20250509.151230.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=2, `bound`=2 |
| Data variables | 34 |
| QC variables | 14 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2025-05-09T15:12:30 to 2025-05-09T18:07:30 |
| dod version | mascparticlesavg-c1-1.0 |
| process version | masc_flake_anal-1.2.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `area_eq_radius_avg` | mm | time | yes | Average area equivalent radius |
| `aspect_ratio_avg` | unitless | time | yes | Average aspect ratio |
| `complexity_avg` | unitless | time | yes | Average complexity |
| `fall_speed_avg` | m/s | time | yes | Average fallspeed |
| `flatness_avg` | unitless | time | yes | Average flatness |
| `geometric_cross_section_avg` | mm^2 | time | yes | Average geometric cross section |
| `maximum_dimension_avg` | mm | time | yes | Average maximum dimension |
| `mean_pixel_intensity_avg` | unitless | time | yes | Average mean pixel intensity |
| `mean_pixel_intensity_variability_avg` | unitless | time | yes | Average mean pixel intensity variability |
| `num_particles_for_avg` | unitless | time | yes | Number of particles used to average |
| `num_particles_total` | unitless | time | yes | Total number of particles that fell into this bin. |
| `orientation_avg` | degree | time | yes | Average orientation |
| `particle_area_avg` | mm^2 | time | yes | Average particle area |
| `perimeter_avg` | mm | time | yes | Average perimeter |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

The `act-arm-live` and `act-qc` skills wrap these calls in shorter helpers
(`armlive_open`, `armlive_list_files`, `act_qc_table`, `act_qc_apply`). Those are helpers
those skills define, **not** ACT functions - nothing below uses them, so every block here
runs against a bare `act-atmos` install.

```python
import os, requests, act

user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]

# ACT has no list-only call, so size the request against ARM Live's query endpoint
# before transferring anything.
avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f"{user}:{token}", "ds": "nsamascparticlesavgC1.c1",
                             "start": "2025-05-09", "end": "2025-05-09", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsamascparticlesavgC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsamascparticlesavgC1.c1", "2025-05-09", "2025-05-09")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsamascparticlesavgC1.c1", "2025-05-09", "2025-05-09"))   # cite what you pulled
```

## Quality control in this product

14 `qc_` companion variables cover 14 of the
34 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_num_particles_total"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("num_particles_total", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["num_particles_total", "num_particles_for_avg", "fall_speed_avg"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsamascparticlesavgC1.c1.20250509.151230.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `num_particles_for_avg` | Value is less than the warn_min | 2 | 100.0 |
| `fall_speed_avg` | num_particles_for_avg is less than warn_min. Could indicate... | 2 | 100.0 |
| `flatness_avg` | Value set to missing_value | 2 | 100.0 |
| `mean_pixel_intensity_variability_avg` | num_particles_for_avg is less than warn_min. Could indicate... | 2 | 100.0 |
| `mean_pixel_intensity_variability_avg` | Value set to missing_value | 2 | 100.0 |
| `mean_pixel_intensity_avg` | num_particles_for_avg is less than warn_min. Could indicate... | 2 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("nsamascparticlesavgC1.c1", "20151101", "20260924")
```

The report's own note on quality: Quality is tracked via bit-packed qc_ variables for nearly every reported field, with bits classified as 'Bad' (data set to MISSING_VALUE, e.g., missing fallspeed, missing camera_id, missing image file, no particle detected in image) or 'Indeterminate' (data retained but flagged, e.g., value exceeds warn_max/warn_min, low particle counts for averaging). Plots generated with ARM's dq_inspector tool color data as gray (no data), green (good, badness bit not set), or yellow (indeterminate). Bad data (MISSING_VALUE) is not shown on the top portion of such plots. Users are advised it is up to them...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Fallspeed too fast (exceeds valid_max) | qc_snowflake_fall_speed bit 3 set (bad); snowflake_fall_speed and all associated per-particle data set to MISSING_VALUE | Value filtered via valid_max threshold in diagnostic variable configuration | (hb p. 4) |
| Fallspeed exceeds warn_max threshold (5 m/s default) | qc_snowflake_fall_speed bit 4 set (indeterminate); particle still retained but excluded from time-bin averaging | Used to filter particles before binning in time; data still considered ok but flagged indeterminate | (hb p. 47) |
| Missing or dropped camera image for a particle | camera_id set to MISSING_VALUE for that camera; corresponding per-image variables set to MISSING_VALUE; qc bits 2/3 set (bad) | VAP checks whether camera index is MISSING_VALUE or image file cannot be found and sets quality bits accordingly | (hb p. 4) |
| All camera images/indices missing for a particle | Per-particle averages (maximum_dimension_avg, etc.) set to MISSING_VALUE; associated qc bits set | None beyond flagging via quality bits | (hb p. 4) |
| No particle/contour detected in an image (out of focus, background noise, etc.) | qc_*_ bit 4 set (bad) for that per-image variable; value set to MISSING_VALUE | Filtered using six contour-filter parameters (size, max intensity, intensity variability, edge touch, focus, ROI bottom location) | (hb p. 5) |
| Out-of-focus image (property of most-in-focus particle outside warn_min/warn_max) | qc_* bit 5 set (indeterminate) across multiple variables; roi_focus below warn_min (0.01) or intensity/variability below warn_min | flagRejectOutOfFocus should always be set to 1; focusThreshold01 is a guess threshold, not a hard rule | (hb p. 41) |
| Insufficient valid images to compute flatness | flatness set to MISSING_VALUE when 0 or 1 valid images available; qc_flatness bit set | Requires at least two valid images to compute flatness | (hb p. 4) |
| Low number of images used for per-particle average (below warn_min of 2) | qc_num_imgs_used_avg bit 5 (indeterminate) set; could indicate not enough data for a statistically meaningful average | None beyond flagging | (hb p. 15) |
| Too few particles in a 5-minute time bin for statistically significant average (below... | qc_num_particles_for_avg bit 2 set (indeterminate); bin data still stored but flagged as possibly not statistically significant | minNumParticlesPerBin default of 10 for 5-min bins (suggested 60 for 1-hour bins); user should decide whether to ignore flagged bins | (hb p. 9) |
| Empty time bin (zero particles or zero valid particles) | qc_num_particles_total bit 2 / qc_num_particles_for_avg bit 3 set (indeterminate); all averaged data except particle count set to MISSING_VALUE; bin not created if no particles overlap | None beyond flagging; bin simply not generated if no particles overlap | (hb p. 16) |
| Particle overlapping/touching image edge beyond threshold | particle_edge_touch value exceeds warn_max (0.5 mm default); qc_particle_edge_touch bit 6 set (indeterminate) | maxEdgeTouchLengthInMicrons default 500 microns used as filter threshold | (hb p. 8) |
| Low geometric cross-section (small/faint particle) below warn_min | qc_geometric_cross_section bit 6 set (indeterminate) when value less than  0.04 mm^2 | warn_min threshold of 0.04 applied | (hb p. 8) |
| Low mean pixel intensity (dark/faint or out-of-focus particle) | qc_mean_pixel_intensity bit 6 set (indeterminate) when value less than  warn_min 0.2 | Darker flakes tend to be out of focus; warn_min threshold of 0.2 applied | (hb p. 8) |
| Low intensity variability (indicative of background/out-of-focus image) | qc_mean_pixel_intensity_variability bit 6 set (indeterminate) when value less than  warn_min 0.019 | Irregularities in background or out-of-focus images have very low internal variability; warn_min threshold applied | (hb p. 8) |
| ROI bottom position (vertical trigger position) outside expected 'sweet spot' range | qc_roi_bot_position bits 6/7 set (indeterminate) when value outside warn_min 32 / warn_max 36 mm; particle image inconsistent with expected trigger geometry | Range should be determined by histogramming roi_bot_position for all particles at a given site/configuration; no fallspeeds/particles accepted... | (hb p. 8) |
| Low ROI focus estimate | qc_roi_focus bit 6 set (indeterminate) when round(roi_focus*100)/100 less than  warn_min (0.01) | Focus estimate = mean_pixel_intensity * mean_pixel_intensity_variability; threshold is a guess, not a hard rule | (hb p. 9) |
| Multiple objects detected in frame (N greater than  1) | num_objects value greater than 1; may indicate blowing snow or coincident hydrometeors confusing the fallspeed measurement; qc_num_objects bit 5 set (bad) if property of most-in-focus... | Only the contour most in focus is used for stored analysis results | (hb p. 9) |
| Ambiguous rain vs. snow classification | rain variable set to NA when hydrometeor does not pass quality checks or when multi-camera rain estimates conflict (at least two images NA) | Combines rain estimates from mean pixel intensity, intensity variability, and number of particles; majority-vote logic across three camera images... | (hb p. 9) |
| Timestamp ambiguity in raw image data files due to boundary crossing | Image acquisition timestamps for the three camera images of one particle may differ slightly and can span across second/minute/hour boundaries | Handbook cautions to be careful when parsing timestamps across these boundaries | (hb p. 3) |
| Dropped/missing image for one of three cameras during acquisition | Snowflake ID does not repeat exactly three times (once per camera) in raw_imgInfo.txt file; image file may be listed but absent from disk | None beyond noting the discrepancy; missing images are treated as MISSING_VALUE downstream | (hb p. 3) |
| Configuration/field-of-view parameters not updated after camera change or instrument move | Downstream pixel-to-mm conversions (maximum_dimension, area, etc.) would be systematically wrong if fieldOfViewInmm or crop values are stale | fieldOfViewInmm and crop parameters must be updated every time camera configuration changes; extracted from saved copy of configuration XML file | (hb p. 3) |
| Default JSON analysis configuration values overridden by datastream valid/warn attributes | Values in defImgAnlParams.json may not match the actual filtering thresholds used, since valid_min/valid_max/warn_min/warn_max in datastream attributes take precedence | Treat JSON parameters as defaults only; check anal_config_json global attribute in mascparticlesM1.c1 for actual values used | (hb p. 4) |
| snowflake_fall_speed set to bad value | Dependent variables (roi position, roi_half_width_height, num_imgs_used_avg, all *_avg fields) are set to missing_value; QC bit_1 flagged as Bad on nearly all variables | Value set to missing_value | (hb p. 56) |
| camera_id missing for a camera | roi_bot_position and related fields for that camera set to missing_value; QC bit_2 flagged Bad | Value set to missing_value | (hb p. 56) |


_17 further items in the report._

## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `masc`: load `arm-instrument-masc` for its handbook facts and artifacts

### References the report cites

- Garrett, TJ, SE Yuter, C Fallgatter, K Shkurko, SR Rhodes, and JL Endries. 2015. "Orientations and aspect ratios of falling snow." Geophysical Research Letters 42(11): 4617-4622, doi:10.1002/2015GL064040.
- Garrett, TJ, and SE Yuter. 2014. "Observed influence of riming, temperature, and turbulence on the fallspeed of solid precipitation." Geophysical Research Letters 41(18): 6515-6522, doi:10.1002/2014GL061016.
- Garrett, TJ, C Fallgatter, K Shkurko, and D Howlett. 2012. "Fall speed measurement and high-resolution multi-angle photography of hydrometeors in free fall." Atmospheric Measurement Techniques 5(11): 2625-2633,...
- OpenCV Documentation
- Fitzgibbon, A, and A Fisher. 1995. "A Buyer's Guide to Conic Fitting." Proceedings of the 5th British Machine Vision Conference, Birmingham, United Kingdom, pp. 513-522.
- Suzuki, S, and K Abe. 1985. "Topological Structural Analysis of Digitized Binary Images by Border Following." CVGIP 30(1): pp 32-46.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-187.pdf (74 pages, DOE/SC-ARM-TR-187, by K Shkurko, T Garrett, A Talaei, K Gaustad)
- Catalog record: ARM data-source index, `instrument_class_code=mascparticles`, read 2026-09-24
- Example file: `nsamascparticlesavgC1.c1.20250509.151230.nc` from `nsamascparticlesavgC1.c1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
