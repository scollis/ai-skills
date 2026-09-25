---
name: arm-vap-cogs
description: ARM Clouds Optically Gridded by Stereo (COGS) product (cogs) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (cloud_status, cldfrac, cbh, x_relative, y_relative, z_relative), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpcogsN1.c1) and the variable inventory of a real file. Use when working with cogs data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - cogs, Clouds Optically Gridded by Stereo (COGS) product, sgpcogsN1.c1, cloud_status, cldfrac, cbh, x_relative, y_relative, Cloud Properties.
---

# COGS - Clouds Optically Gridded by Stereo (COGS) product

COGS is a 4D (space+time) gridded map of shallow cumulus cloudiness over a 6 km x 6 km x 6 km volume at the SGP Central Facility, produced by combining multiview stereo-camera cloud point reconstructions (PCCP) from three stereo camera pairs surrounding the site.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 27 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `cogs` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-252 / DM Romps, R Öktem / December 2022](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-252.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2017-09-01 to 2019-10-27 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/cogs |


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

The PCCP VAP triangulates 3D positions of cloud edge features from synchronized image pairs captured by a stereo camera pair, using camera calibration (intrinsic parameters from checkerboard calibration, extrinsic Euler angles from celestial-object sightings plus an epipolar constraint), Canny-edge feature extraction and hierarchical block-search cross-correlation matching along epipolar lines, and direct linear transformation (DLT) back-projection via singular value decomposition to recover 3D coordinates. COGS then combines PCCP data from the three ARM SGP stereo pairs (six cameras) covering a common field of view (CFOV): a cloud surface visible to at least one camera pair but obstructed from another can still be captured by a third pair, and obstructed regions are estimated from the retrieved data. COGS grids are filled through cross-validation (back-projecting each pair's PCCP points onto the other four camera planes and checking they hit a cloudy pixel), missing cloud point detection (identifying hollow parts of filled cloud boundaries), and rematching/validation (assigning missing grids as cloudy if their back-projections hit a cloudy pixel and reference/pairing projections agree). The result is a trinary cloud_status grid (no cloud / NA / cloud) as a function of x, y, z, and time, with cloud fraction and cloud base height diagnostics also computed.

**Cadence.** input rate PCCP processed for each time interval from sunrise to sunset each day; COGS time resolution 20 seconds; output every COGS: 20 s; PCCP variable by image capture; averaging COGS VAP executed only over half-hour intervals with detected shallow cumulus events (hb p. 9).

## Inputs

The report names these instruments and sibling products: Stereo Cameras for Clouds (STEREOCAM), PCCP (Point Cloud of Cloud Points) VAP, Doppler lidar.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| cloud_status | categorical [0,1,2] = [no... | - | - | (hb p. 11) |
| cldfrac | fraction | - | - | (hb p. 11) |
| cbh (cloud base height) | m (implied, altitude grid) | - | - | (hb p. 11) |
| x_relative (PCCP) | meters | - | - | (hb p. 6) |
| y_relative (PCCP) | meters | - | - | (hb p. 6) |
| z_relative (PCCP) | meters | - | - | (hb p. 6) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| COGS domain size | 6 km x 6 km x 6 km region at SGP Central Facility centered at the Doppler lidar position | (hb p. 14) |
| COGS grid resolution | 50 m in horizontal and vertical directions and 20 seconds in time | (hb p. 14) |
| COGS x dimension | 121 grids, distance to East in meters, from -3 km to 3 km, in 50-m intervals | (hb p. 16) |
| COGS y dimension | 121 grids, distance to North in meters, from -3 km to 3 km, in 50-m intervals | (hb p. 16) |
| COGS z dimension | 120 grids, altitude above the ground in meters, from 25 m to 5975 m in 50-m intervals | (hb p. 16) |
| Number of stereo pairs / cameras | 3 stereo pairs (6 cameras) at ARM SGP site around the Central Facility | (hb p. 7) |
| Extrinsic calibration accuracy (celestial) | Euler angles estimated within around 0.1 degree accuracy | (hb p. 9) |
| Stereo pair relative calibration accuracy required | at least 0.01 degree accuracy with respect to each other | (hb p. 9) |
| Reference camera image size (PCCP) | camera_a_col = 2592, camera_a_row = 1944 pixels | (hb p. 12) |
| Feature matching downsampling factor (initial pass) | reduced by a factor of eight in both dimensions | (hb p. 10) |
| COGS execution scope | only run over half-hour intervals in which a preprocessing algorithm detects shallow cumulus cloud events | (hb p. 9) |
| PCCP invalid/no-detection value | -99999 for x_relative, y_relative, z_relative entries with no cloud point detected | (hb p. 13) |


## The data

Verified example: **`sgpcogsN1.c1`**, file `sgpcogsN1.c1.20191027.190800.nc`
(5.06 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=136, `z`=120, `x`=121, `y`=121, `nfiles`=136 |
| Data variables | 9 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2019-10-27T19:08:00 to 2019-10-27T20:07:00 |
| dod version | cogs-c1-1.2 |
| process version | vap-pccp-1.6-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cbh` | m | time | - | Cloud Base Height |
| `cldfrac` | 1 | time | - | Vertically projected cloudfraction |
| `cloud_status` | 1 | time,z,x,y | - | Cloud Status |
| `input_images` | 1 | nfiles | - | Names of input pccpa.c1 input images processed. |
| `time` | - | time | - | Time offset from midnight |
| `x` | m | x | - | X grid representing distance to East |
| `y` | m | y | - | Y grid representing distance to North |
| `z` | m | z | - | Z grid representing height above the ground |


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
                     params={"user": f"{user}:{token}", "ds": "sgpcogsN1.c1",
                             "start": "2019-10-27", "end": "2019-10-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpcogsN1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpcogsN1.c1", "2019-10-27", "2019-10-27")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpcogsN1.c1", "2019-10-27", "2019-10-27"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpcogsN1.c1", "20170901", "20260924")
```

The report's own note on quality: The PCCP algorithm applies a 3D filtering post-processing step to remove false positives from feature matching, though it does not completely eliminate them at all times (e.g., under hazy clear-sky conditions near sunrise/sunset with sun in FOV). The COGS algorithm performs cross-validation by back-projecting PCCP points from each camera pair onto the other four camera planes and only accepting back-projections that hit a cloudy pixel as true positives, in order to eliminate false positives; missing cloud point detection and rematching/validation steps then attempt to recover genuinely...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| False positive cloud detections under clear-sky but hazy conditions | Algorithm reports false detections when the sun is close to the horizon and in the FOV, appearing as spurious cloud points; however the number of false detections is on the order of tens... | 3D filtering in post-processing removes most but not all false positives | (hb p. 6) |
| No cloud point detection possible under featureless cloud conditions | Algorithm may not detect any cloud points at all during heavy rain, fog, snow, etc., because clouds do not exhibit distinct features | - | (hb p. 6) |
| Wide-angle lens radial distortion | Raw camera images show noticeable geometric distortion compared to a pinhole model, visible as curved/warped features especially near image edges | Inverse mapping correction applied using estimated distortion parameters from calibration package | (hb p. 8) |
| Overexposed cloud regions causing missed cloud points | Hollow/missing parts appear within otherwise filled cloud boundaries in COGS grids where PCCP failed to detect distinctive features (e.g., overexposed cloud region) | COGS missing cloud point detection and rematching/validation steps attempt to recover these hollow grids | (hb p. 10) |
| NA grids outside common field of view (CFOV) | Grids labeled NA (cloud_status=1) in COGS output where not all three camera pairs have field of view coverage; NA grid positions vary with height | - | (hb p. 11) |
| Slight drift in NA grid positions over long time spans | Over intervals of months or years, NA grid positions may slightly vary due to slight changes in orientation of any of the cameras | Re-calibration of extrinsic parameters when orientation changes by as little as 0.01 degree | (hb p. 11) |
| Sparse valid data in PCCP arrays | Most entries of x_relative, y_relative, z_relative in the PCCP datastream equal -99999, denoting no cloud point detected at that pixel; only a minority of grid/pixel entries are valid at... | - | (hb p. 13) |
| Camera orientation change requiring extrinsic recalibration | A change in camera orientation as small as 0.01 degree invalidates prior extrinsic calibration, degrading stereo triangulation accuracy if not updated | Extrinsic calibration module regenerates camera-specific configuration files as needed | (hb p. 5) |
| COGS restricted to shallow cumulus regime | COGS VAP only executes over half-hour intervals where the preprocessing algorithm detects shallow cumulus cloud events; other cloud regimes are not represented in COGS output for that period | - | (hb p. 9) |
| lat/lon/alt variables in PCCP refer to reference camera, not to cloud data | Users might mistakenly interpret lat/lon/alt as describing the PCCP cloud point locations, but these describe only the reference camera position, not the retrieved data points | - | (hb p. 7) |


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
- Öktem, R, Prabhat, J Lee, A Thomas, P Zuidema, and DM Romps. 2014. Stereophotogrammetry of oceanic clouds. Journal of Atmospheric and Oceanic Technology 31(7):1482–1501.
- Öktem, R, and DM Romps. 2015. Observing atmospheric clouds through stereo reconstruction. Proceedings of SPIE 9393.
- Öktem, R, and DM Romps. 2021. Prediction for cloud spacing confirmed using stereo cameras. Journal of the Atmospheric Sciences 78(11): 3717-3725.
- Romps, DM, and R Öktem. 2017. Stereo Cameras for Clouds (STEREOCAM) Instrument Handbook. DOE/SC-ARM-TR-204.
- Romps, DM, and R Öktem. 2018. Observing Clouds in 4D with Multiview Stereophotogrammetry. BAMS 99(12): 2575-2586.
- Romps, DM, R Öktem, S Endo, and A Vogelmann. 2021. On the lifecycle of a shallow cumulus cloud. JAS 78(9): 2823-2833.
- Tian, J, Y Zhang, SA Klein, L Wang, R Öktem, and DM Romps. 2021. Summertime continental shallow cumulus cloud detection using GOES-16 satellite and ground-based stereo cameras. Remote Sensing 13(12): 2309.
- Williams, CR, KL Johnson, SE Giangrande, JC Hardin, R Öktem, and DM Romps. 2021. Identifying insects, clouds, and precipitation using vertically pointing polarimetric radar Doppler velocity spectra. AMT 14(6): 4425-4444.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-252.pdf (27 pages, DOE/SC-ARM-TR-252, by DM Romps, R Öktem)
- Catalog record: ARM data-source index, `instrument_class_code=cogs`, read 2026-09-24
- Example file: `sgpcogsN1.c1.20191027.190800.nc` from `sgpcogsN1.c1`, 5.06 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
