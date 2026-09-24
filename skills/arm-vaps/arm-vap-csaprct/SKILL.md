---
name: arm-vap-csaprct
description: ARM C-Band Scanning ARM Precipitation Radar, Adaptive Scanning Cell Tracking (csaprct) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (frame, idx, hdim_1, hdim_2, num, threshold_value, feature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (houcsapr2cfrqctobacmaskS2.c1) and the variable inventory of a real file. Use when working with csaprct data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - csaprct, houcsapr2cfrqctobacmaskS2.c1, frame, idx, hdim_1, hdim_2, num, threshold_value, Cloud Properties.
---

# CSAPRCT - C-Band Scanning ARM Precipitation Radar, Adaptive Scanning Cell Tracking

This ARM value-added product derives tracked convective-cloud cell life-cycle characteristics over the Houston, Texas TRACER domain by running the tobac object-tracking algorithm on composite reflectivity fields computed from CSAPR2 adaptive-scanning (MAAS) 3-degree elevation-angle PPI scans.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 21 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `csaprct` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-324 / S Gupta, A Theisen / October 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-324.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2022-06-04 to 2022-09-20 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/csaprct |


## Credit

Everything this skill knows about the retrieval is the work of **S Gupta, A Theisen** -
the ARM developers and mentors who wrote the technical report it derives from:

> S Gupta, A Theisen. *A Cloud-Tracking Data Set for the CSAPR2 Adaptive Scanning during TRACER*, DOE/SC-ARM-TR-324, October 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-324.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The CSAPR2 radar performed adaptive scan bundles of three PPI scans (the first two at cell-dependent elevation angles, the third always at a fixed 3-degree elevation angle) followed by RHI scans every two minutes, targeting convective cells selected by the Multisensor Agile Adaptive Scanning (MAAS) framework. Because the varying elevation angles of the first two PPIs produced inconsistent spatial grids, only the constant 3-degree PPI scan was used, gridded with Py-ART at 0.5-km horizontal and 1-km vertical resolution, and the column-maximum reflectivity from that grid was defined as composite reflectivity using bias- and attenuation-corrected b1-level reflectivity. This composite reflectivity field was fed into tobac (Tracking and Object-Based Analysis of Clouds), which performs feature identification (regions of local maxima above multiple reflectivity thresholds, smoothed with a Gaussian filter), segmentation (watershedding of the identified regions down to a threshold), and linking (trackpy-based prediction of feature motion across timesteps using threshold parameters) to assemble cells composed of features tracked across time. Output feature/cell properties (position, velocity, distance to nearest neighbor, cell time) and a corresponding 2-D segmentation mask are produced for each of 72 days with tracked cells.

**Cadence.** input rate scan bundles every 2 minutes (3 PPI + 4-6 RHI scans per bundle); output every per-timestep tracking output over each day with tracked cells (hb p. 7).

## Inputs

The report names these instruments and sibling products: CSAPR2 (2nd-Generation C-band Scanning ARM Precipitation Radar, PI..., AMF1 (ARM Mobile Facility 1), csapr2cfrqctobac (tracking output datastream), csapr2cfrqctobacmask (cloud mask datastream).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| frame | 1 | - | - | (hb p. 11) |
| idx (feature number within frame) | 1 | - | - | (hb p. 11) |
| hdim_1, hdim_2 (grid point space location) | 1 | - | - | (hb p. 11) |
| num (number of grid points within threshold for feature) | 1 | - | - | (hb p. 11) |
| threshold_value (max threshold reached by feature) | dBZ | - | - | (hb p. 11) |
| feature (unique feature number) | 1 | - | - | (hb p. 11) |
| projection_y_coordinate | kilometer | - | - | (hb p. 11) |
| latitude | Decimal degrees | - | - | (hb p. 11) |
| longitude | Decimal degrees | - | - | (hb p. 11) |
| projection_x_coordinate | kilometer | - | - | (hb p. 11) |
| Cell (tracked cell number) | 1 | - | - | (hb p. 11) |
| velocity (feature velocity) | Meter per second | - | - | (hb p. 11) |
| Min_distance (distance from nearest neighbor) | Meter | - | - | (hb p. 11) |
| Cell_time (time since first detection of cell) | s | - | - | (hb p. 11) |
| segmentation_mask (cloud/feature mask) | 1 | - | - | (hb p. 19) |
| composite reflectivity (input field, column-maximum radar... | dBZ | - | - | (hb p. 8) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Identification thresholds | 20, 30, 40, 50 dBZ | (hb p. 11) |
| Target (identification) | 'maxima' | (hb p. 11) |
| Position threshold | 'weighted_diff' (weighted center of regions satisfying identification thresholds) | (hb p. 11) |
| Sigma threshold (Gaussian filter std dev) | 0.5 | (hb p. 11) |
| Segmentation threshold | 20 dBZ | (hb p. 11) |
| Target (segmentation) | 'maxima' | (hb p. 11) |
| Method (segmentation) | 'watershed' | (hb p. 11) |
| Method_linking | 'predict' | (hb p. 11) |
| Subnetwork size | 10 | (hb p. 11) |
| Maximum Velocity | 20 m/s | (hb p. 11) |
| Adaptive Step | 0.95 | (hb p. 11) |
| Adaptive Stop | 0.20 | (hb p. 11) |
| Stubs | 2 (minimum number of timesteps to report features) | (hb p. 11) |
| Extrapolate | 0 (timesteps to extrapolate features) | (hb p. 11) |
| Memory | 1 (timesteps for which feature can vanish) | (hb p. 11) |
| Gridding resolution for composite reflectivity | 0.5-km horizontal, 1-km vertical | (hb p. 8) |
| PPI elevation used for compositing | 3 degree elevation angle | (hb p. 7) |
| Scan bundle composition | 3 PPI scans over narrow sectors followed by 4-6 RHI scans every 2 minutes | (hb p. 7) |
| Cloud mask grid dimensions (example file) | time=201, projection_y_coordinate=401, projection_x_coordinate=401 | (hb p. 19) |
| Tracking output time dimension (example file) | time = 183 | (hb p. 16) |


## The data

Verified example: **`houcsapr2cfrqctobacmaskS2.c1`**, file `houcsapr2cfrqctobacmaskS2.c1.20220918.000000.nc`
(104.9 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=318, `projection_y_coordinate`=401, `projection_x_coordinate`=401 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 125 s |
| File time span | 2022-09-18T00:00:32 to 2022-09-18T23:59:13 |
| dod version | csapr2cfrqctobacmask.c1-1.0 |
| process version | N/A |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `projection_x_coordinate` | kilometer | projection_x_coordinate | - | X location of the feature in projection coordinates |
| `projection_y_coordinate` | kilometer | projection_y_coordinate | - | Y location of the feature in projection coordinates |
| `segmentation_mask` | 1 | time,projection_y_coordinate,projection_x_coordinate | - | Segmentation mask using feature number |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("houcsapr2cfrqctobacmaskS2.c1", "2022-09-18", "2022-09-18")
ds = armlive_open("houcsapr2cfrqctobacmaskS2.c1", "2022-09-18", "2022-09-18", cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `segmentation_mask`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("houcsapr2cfrqctobacmaskS2.c1", "20220604", "20260924")
```

The report's own note on quality: Daily images and animations of CSAPR2 radar reflectivity factor were created to help users identify cases for detailed analysis and are available on the ARM DQ plot browser (site='HOU', class='csapr2', facility='S2'). The comment attribute in the output NetCDF files notes this is experimental data with various caveats, directing users to the technical report and to contact the developer for questions.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Varying elevation angles of first two PPI scans in each scan bundle | Inconsistent spatial grids across different scan bundles if those PPIs are included in gridding/CAPPI construction | Only the constant 3-degree elevation-angle PPI scan was used to derive CAPPIs/composite reflectivity; the first two PPIs were excluded from gridding | (hb p. 7) |
| Limited spatial coverage of CAPPIs at fixed altitude derived from a single PPI scan | CAPPIs at 1-, 2-, and 3-km altitude show restricted/patchy spatial extent (Figure 3) | Composite (column-maximum) reflectivity from the 3-degree PPI was used as tobac input instead of CAPPIs | (hb p. 8) |
| PI-level vs b1-level data set differences in tracked cell counts and longevity | Fewer and shorter-lived cells identified/tracked when PI data set (uncorrected) used as tobac input compared to b1-level (bias/attenuation corrected) data, due to systematically lower... | b1-level data set (with bias and attenuation corrections applied) was used as the operational input for this data set; tobac output based on PI data... | (hb p. 10) |
| Missing 3-degree PPI scans on certain dates | Dates marked in red in Table 1 have no 3-degree PPI scans and thus no composite reflectivity/tobac input available | - | (hb p. 11) |
| No cloud objects tracked on some available dates | Underlined dates in Table 1 had CSAPR2 data available but no tracked cells identified by tobac | - | (hb p. 11) |
| Coverage gaps: only 72 of 76 IOP days produced tracking output | CSAPR2 collected data on 76 days but at least one cloud object was tracked on only 72 days; two output files exist only for those 72 days | - | (hb p. 10) |
| Non-standard/unique scan strategy relative to conventional radars/NEXRAD VCPs | Scans are narrow-sector PPI/RHI bundles targeting a single cell rather than full 360-degree volumetric coverage, so spatial context around non-targeted regions is absent | - | (hb p. 7) |
| Experimental/limited-support data set status | Global attribute comment flags data as experimental with various caveats | Refer to the technical report and contact the developer (Sid Gupta, ANL) with questions | (hb p. 18) |
| Missing values in output files | Variables use missing_value = -9999 (or -99 for segmentation_mask) where no valid feature/cell/value is present, e.g., pixels with no cloud object at a timestep assigned 0 in the cloud mask | - | (hb p. 10) |
| tobac software version/threshold sensitivity | Threshold parameters (Table 2) govern feature identification/segmentation/linking outcomes and are subject to change with software updates | Consult the tobac documentation for the latest threshold definitions and updates | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Oue, M, BP Treserras, EP Luke, and P Kollias. 2023. CSAPR2 Optimized Convective Cell Tracking Data during TRACER. DOE/SC-ASR-23-001
- Feng, Y-C et al. 2024a. TRACER b1 Data Processing: Corrections, Calibrations, and Processing Report. DOE/SC-ARM-TR-297
- Feng, Y-C et al. 2024b. ARM FY2025 Radar Plan. DOE/SC-ARM-TR-308
- Sokolowsky, GA et al. 2024. tobac v1.5. Geoscientific Model Development 17(13): 5309-5330
- Gupta, S et al. 2024. Lifecycle of updrafts and mass flux in isolated deep convection over the Amazon rainforest. ACP 24(7): 4487-4510
- Hahn, T et al. 2025. CoCoMET v1.0. EGUsphere preprint
- Helmus, JJ and SM Collis. 2016. Py-ART. Journal of Open Research Software 4(1): e25
- Kollias, P, E Luke, M Oue, and K Lamer. 2020. Agile Adaptive Radar Sampling. GRL 47(14)
- Lamer, K et al. 2023. Multisensor Agile Adaptive Sampling (MAAS). BAMS 40(11): 1509-1522
- Allan, DB et al. 2025. soft-matter/trackpy v0.7

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-324.pdf (21 pages, DOE/SC-ARM-TR-324, by S Gupta, A Theisen)
- Catalog record: ARM data-source index, `instrument_class_code=csaprct`, read 2026-09-24
- Example file: `houcsapr2cfrqctobacmaskS2.c1.20220918.000000.nc` from `houcsapr2cfrqctobacmaskS2.c1`, 104.9 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
