---
name: arm-vap-pccp
description: ARM Stereo Reconstructed Point Cloud of Cloud Points (PCCP) (pccp) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (x_relative, y_relative, z_relative, camera_b_col, camera_b_row, lat), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgppccpE45.c1) and the variable inventory of a real file. Use when working with pccp data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - pccp, Stereo Reconstructed Point Cloud of Cloud Points (PCCP), sgppccpE45.c1, x_relative, y_relative, z_relative, camera_b_col, camera_b_row, Cloud Properties.
---

# PCCP - Stereo Reconstructed Point Cloud of Cloud Points (PCCP)

PCCP is a VAP that reconstructs 3D positions of cloud edge/surface features (a point cloud) over tens of square kilometers by stereophotogrammetric triangulation of synchronized image pairs from ARM stereo camera pairs positioned around the SGP Central Facility.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 27 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `pccp` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-252 / DM Romps, R Öktem / December 2022](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-252.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2017-09-01 to 2022-09-28 (retired) |
| Datastreams with data | 15 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/pccp |


## Credit

Everything this skill knows about the retrieval is the work of **DM Romps, R Öktem** -
the ARM developers and mentors who wrote the technical report it derives from:

> DM Romps, R Öktem. *Retrieving Point Cloud of Cloud Points (PCCP) Value-Added Product from Stereo Cameras*, DOE/SC-ARM-TR-252, December 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-252.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Stereo reconstruction uses projective geometry and a pinhole camera model: each camera's intrinsic parameters (focal length, sensor size, pinhole position, radial distortion) are estimated via checkerboard calibration (OpenCV), and extrinsic parameters (three Euler angles, three translations) are estimated using GPS for translation and angular positions of bright stars/planets (Sirius, Venus, Jupiter) for orientation, refined by an epipolar constraint so paired cameras are cross-calibrated to ~0.01 degree accuracy. Distinct cloud features are extracted from the reference camera image using a Canny edge detector within a cloud mask, and corresponding matches are found in the pairing image along the epipolar line via a hierarchical block search using cross-correlation of image intensity blocks across successively higher resolutions. Matched 2D feature pairs are triangulated into 3D coordinates using direct linear transformation (DLT), which forms a homogeneous linear equation combining the 3D-to-2D projection relations for both cameras and solves for 3D coordinates via singular value decomposition. A 3D filtering post-processing step removes false-positive matches before final back-projected coordinates are reported. The related COGS VAP further combines PCCP outputs from three camera pairs (six cameras) via cross-validation back-projection onto other camera planes, missing-point/hollow-region detection, and rematching/validation to build a 4D gridded cloud map.

**Cadence.** input rate synchronized still image pairs captured throughout daylight; output every processed from sunrise until sunset for a day (PCCP); COGS reported at 20-second time resolution (hb p. 5).

## Inputs

The report names these instruments and sibling products: Stereo Cameras for Clouds (STEREOCAM), Doppler lidar (used as base position reference), Clouds Optically Gridded by Stereo (COGS) VAP (sibling product built....

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| x_relative | meters | - | - | (hb p. 6) |
| y_relative | meters | - | - | (hb p. 6) |
| z_relative | meters | - | - | (hb p. 6) |
| camera_b_col | pixel index | - | - | (hb p. 6) |
| camera_b_row | pixel index | - | - | (hb p. 6) |
| lat | degrees North | - | - | (hb p. 7) |
| lon | degrees East | - | - | (hb p. 7) |
| alt | meters above mean sea... | - | - | (hb p. 7) |
| cloud_status (COGS) | categorical: 0=no cloud,... | 0-2 | - | (hb p. 11) |
| cldfrac (COGS) | fraction | - | - | (hb p. 11) |
| cbh (COGS cloud base height) | meters | - | estimated as the 1% of the cloudy grid heights | (hb p. 11) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Number of stereo pairs (SGP) | three stereo pairs, six cameras total | (hb p. 7) |
| camera_a_col | 2592 (number of columns of reference image) | (hb p. 6) |
| camera_a_row | 1944 (number of rows of reference image) | (hb p. 6) |
| External Euler angle calibration accuracy (celestial only) | ~0.1 degree accuracy | (hb p. 3) |
| Required inter-camera calibration accuracy (with epipolar... | at least 0.01 degree accuracy with respect to each other | (hb p. 3) |
| Feature matching downscale factor (initial hierarchical... | reduced by a factor of eight in both dimensions | (hb p. 4) |
| COGS domain size | 6 km x 6 km x 6 km region at SGP Central Facility centered at Doppler lidar position | (hb p. 8) |
| COGS grid resolution (horizontal/vertical) | 50 m | (hb p. 8) |
| COGS grid resolution (time) | 20 seconds | (hb p. 8) |
| COGS x dimension | 121 grids, -3 km to 3 km, 50-m intervals | (hb p. 10) |
| COGS y dimension | 121 grids, -3 km to 3 km, 50-m intervals | (hb p. 10) |
| COGS z dimension | 120 grids, 25 m to 5975 m, 50-m intervals | (hb p. 10) |
| COGS preprocessing detection interval | half-hour intervals inspected for shallow cumulus cloud events | (hb p. 9) |
| PCCP missing-data fill value | -99999 (no cloud point detected at that pixel) | (hb p. 7) |
| PCCP processing window | each time interval starting from sunrise until sunset for a day | (hb p. 5) |


## The data

Verified example: **`sgppccpE45.c1`**, file `sgppccpE45.c1.20201228.152540.nc`
(5.84 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=9, `camera_a_col`=2592, `camera_a_row`=1944, `nfiles`=1439 |
| Data variables | 14 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2020-12-28T15:25:40 to 2020-12-28T18:24:20 |
| dod version | pccp-c1-1.0 |
| process version | vap-pccpag-1.4-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `base_alt` | m | - | - | Altitude of the base coordinate above mean sea level |
| `base_lat` | degree_N | - | - | North latitude of the base coordinate |
| `base_lon` | degree_E | - | - | East longitude of the base coordinate |
| `camera_b_col` | 1 | time,camera_a_col,camera_a_row | - | References camera_b x axis to camera_a pixel axes |
| `camera_b_row` | 1 | time,camera_a_col,camera_a_row | - | References camera_b y axis to camera_a pixel axes |
| `input_images` | 1 | nfiles | - | Names of input stereocamera input images processed. |
| `time` | - | time | - | Time offset from midnight |
| `x_relative` | m | time,camera_a_col,camera_a_row | - | East relative distance to base_lon dimensioned by pixels in camera_a... |
| `y_relative` | m | time,camera_a_col,camera_a_row | - | North relative distance to base_lat dimensioned by pixels in camera_a... |
| `z_relative` | m | time,camera_a_col,camera_a_row | - | Height relative distance to base_alt dimensioned by pixels in... |


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
                     params={"user": f"{user}:{token}", "ds": "sgppccpE45.c1",
                             "start": "2020-12-28", "end": "2020-12-28", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgppccpE45.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgppccpE45.c1", "2020-12-28", "2020-12-28")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgppccpE45.c1", "2020-12-28", "2020-12-28"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgppccpE45.c1", "20170901", "20260924")
```

The report's own note on quality: Post-processing 3D filtering is applied to PCCP data to remove false positives from feature matching, though the handbook notes it does not completely eliminate false detections at all times (e.g., under hazy clear-sky conditions with low sun angle). COGS VAP applies a cross-validation step (back-projecting PCCP from each camera pair onto the other four camera planes) specifically to eliminate false positives by incorporating information from other cameras, followed by missing cloud point detection and a rematching/validation step (requiring a cloudy-pixel hit plus agreement between reference...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| False cloud-point detections under clear-sky but hazy conditions with low sun near... | Spurious PCCP points appear under clear/hazy sky when sun is close to horizon and in camera FOV; number of false detections is on the order of tens, much smaller than the thousands of... | 3D filtering post-processing is applied to remove false positives, though it does not completely eliminate them at all times | (hb p. 6) |
| No cloud points detected during heavy rain, fog, snow, or other featureless cloud... | PCCP datastream shows no or very few valid (non -99999) cloud point entries during such weather even though clouds may be present | - | (hb p. 6) |
| Wide-angle lens radial distortion | Raw images show geometric distortion (visible curvature of straight lines) before correction; uncorrected images would bias 3D triangulation | Distortion parameters estimated per-lens via calibration packages (OpenCV) and corrected by inverse mapping before feature extraction; example shown... | (hb p. 2) |
| Feature-matching threshold discards weakly correlated features | Fewer valid PCCP entries than total pixels; features with cross-correlation coefficient below a hierarchical-level-specific threshold produce no match and are dropped (left as -99999) | Threshold set separately for each hierarchical level; hierarchical block search narrows search area to reduce false matches | (hb p. 4) |
| Sparse valid data fraction / large fill-value array | Most x_relative, y_relative, z_relative entries in the datastream equal -99999, denoting no cloud point detected at that pixel, since valid features are a small subset of total camera_a_row... | - | (hb p. 7) |
| Sun-obstructed/overexposed cloud regions cause missed cloud points | Hollow or missing regions appear within otherwise filled cloud boundaries in COGS grids, corresponding to overexposed cloud regions in the source image (as in Figure 3) or points not lying... | COGS VAP performs missing cloud point detection and rematching/validation step to recover missing cloudy grids using cross-camera back-projection,... | (hb p. 10) |
| NA (not available) grid regions outside common field of view | COGS cloud_status variable shows value 1 (NA) for grids not within the common field of view of all three camera pairs; NA grid positions vary with height | Grids outside CFOV are simply labeled NA rather than cloud/no-cloud | (hb p. 9) |
| Slight drift in NA grid positions over long time periods due to camera orientation change | Comparing COGS NA grid masks across months or years shows slight positional differences | Extrinsic (orientation) calibration should be updated when camera orientation changes by as little as 0.01 degree | (hb p. 11) |
| Sun region discarded from cloud mask | Region of the image corresponding to the sun (if within FOV) is excluded from cloud feature extraction, so no PCCP points are generated there | Sun detection step in pre-processing discards sun region before feature extraction | (hb p. 5) |
| COGS restricted to shallow cumulus cloud events | COGS VAP output is only produced for half-hour intervals where the preprocessing algorithm detects shallow cumulus cloud events; other cloud regimes are not represented in COGS | - | (hb p. 9) |
| lat/lon/alt variables refer to reference camera position, not to the PCCP cloud-point... | Users might mistakenly interpret lat/lon/alt as the location of detected cloud points rather than the camera; actual cloud point positions are given by x_relative/y_relative/z_relative... | - | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Bradski, G. and A Kaehler. 2008. Learning OpenCV, Computer Vision with the OpenCV Library. O'Reilly Media.
- Hartley, R, and A Zisserman. 2003. Multiple View Geometry in Computer Vision. Cambridge University Press.
- Öktem, R, Prabhat, J Lee, A Thomas, P Zuidema, and DM Romps. 2014. Stereophotogrammetry of oceanic clouds. JTECH 31(7):1482-1501.
- Öktem, R, and DM Romps. 2015. Observing atmospheric clouds through stereo reconstruction. Proceedings of SPIE 9393.
- Öktem, R, and DM Romps. 2021. Prediction for cloud spacing confirmed using stereo cameras. JAS 78(11):3717-3725.
- Romps, DM, and R Öktem. 2017. Stereo Cameras for Clouds (STEREOCAM) Instrument Handbook. DOE/SC-ARM-TR-204.
- Romps, DM, and R Öktem. 2018. Observing Clouds in 4D with Multiview Stereophotogrammetry. BAMS 99(12):2575-2586.
- Romps, DM, R Öktem, S Endo, and A Vogelmann. 2021. On the lifecycle of a shallow cumulus cloud. JAS 78(9):2823-2833.
- Tian, J, Y Zhang, SA Klein, L Wang, R Öktem, and DM Romps. 2021. Summertime continental shallow cumulus cloud detection using GOES-16 satellite and ground-based stereo cameras. Remote Sensing 13(12):2309.
- Williams, CR, KL Johnson, SE Giangrande, JC Hardin, R Öktem, and DM Romps. 2021. Identifying insects, clouds, and precipitation using vertically pointing polarimetric radar Doppler velocity spectra. AMT 14(6):4425-4444.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-252.pdf (27 pages, DOE/SC-ARM-TR-252, by DM Romps, R Öktem)
- Catalog record: ARM data-source index, `instrument_class_code=pccp`, read 2026-09-24
- Example file: `sgppccpE45.c1.20201228.152540.nc` from `sgppccpE45.c1`, 5.84 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
