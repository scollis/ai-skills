---
name: arm-vap-mmcg
description: ARM Precipitation Radar Moments Mapped to a Cartesian Grid (mmcg) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Reflectivity, Corrected reflectivity, Total power, Mean Doppler velocity, Corrected velocity, Spectral width / Spectrum width), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpxsaprmmcgI5.c1) and the variable inventory of a real file. Use when working with mmcg data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - mmcg, Precipitation Radar Moments Mapped to a Cartesian Grid, sgpxsaprmmcgI5.c1, Reflectivity, Corrected reflectivity, Total power, Mean Doppler velocity, Corrected velocity, Cloud Properties.
---

# MMCG - Precipitation Radar Moments Mapped to a Cartesian Grid

MMCG is an ARM value-added product that maps CMAC-corrected X-SAPR precipitation radar moments in antenna coordinates (range, azimuth, elevation) onto a regularly spaced Cartesian grid using objective analysis interpolation.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 26 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mmcg` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-243 / Z Sherman, S Collis, J Hemedinger / April 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-243.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-08-18 to 2019-04-05 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mmcg |


## Credit

Everything this skill knows about the retrieval is the work of **Z Sherman, S Collis, J Hemedinger** -
the ARM developers and mentors who wrote the technical report it derives from:

> Z Sherman, S Collis, J Hemedinger. *Mapped Moments to a Cartesian Grid (MMCG) Value-Added Product Report*, DOE/SC-ARM-TR-243, April 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-243.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Objective analysis (OA) is used to interpolate scanning radar data from antenna coordinates (range, azimuth, elevation) onto a regularly spaced Cartesian grid using the Python ARM Radar Toolkit (Py-ART). Radar reflectivity and related dBZ-unit fields are first converted back to linear units (mm6 m-3, or Z) before interpolation, because interpolating in linear Z is more accurate than in logarithmic dBZ, especially in regions of high reflectivity and strong reflectivity gradients. Most fields are interpolated using an inverse-distance weight function based on Cressman (1959): weights = (r2 - dist2) / (r2 + dist2), where r2 is the radius of influence (ROI) squared and dist2 is the squared distance between two points; the ROI varies as a function of distance from the radar in x, y, and height. The hydrometeor classification (gate_id) field is instead interpolated using nearest neighbor because each gate carries its own identification number. After interpolation, the linear-Z fields are converted back to logarithmic dBZ units via dBZ = 10log10Z, and the resulting grid is written with the new Cartesian coordinate system.

**Cadence.** averaging Interpolation via Cressman weighting (inverse distance) for most fields; nearest neighbor for hydrometeor classification field (hb p. 7).

## Inputs

The report names these instruments and sibling products: CMAC (Corrected Precipitation Radar Moments in Antenna Coordinates), X-SAPR (X-band Scanning ARM Precipitation Radar).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Reflectivity | dBZ | -327.67 to 327.66 | - | (hb p. 11) |
| Corrected reflectivity | dBZ | - | - | (hb p. 21) |
| Total power | dBZ | -327.67 to 327.66 | - | (hb p. 12) |
| Mean Doppler velocity | m/s | -327.67 to 327.66 | - | (hb p. 12) |
| Corrected velocity | meters_per_second | -32.0849990844727 to... | - | (hb p. 15) |
| Spectral width / Spectrum width | m/s | 0.01 to 655.34 | - | (hb p. 13) |
| Cross correlation ratio (RhoHV) | unitless | 0 to 1 | - | (hb p. 12) |
| Normalized coherent power | unitless | 0 to 1 | - | (hb p. 12) |
| Differential reflectivity (ZDR) | dB | -327.67 to 327.66 | - | (hb p. 13) |
| Specific differential phase (KDP) | degree/km | -327.67 to 327.66 | - | (hb p. 13) |
| Differential phase (PhiDP) | degree | 0 to 359.99 | - | (hb p. 13) |
| Gate ID (hydrometeor classification) | 1 | 0 to 5 | - | (hb p. 15) |
| Rain rate (rain_rate_A) | mm/hr | 0 to 400 | - | (hb p. 15) |
| Radar echo classification | 1 | flag values 0 1 2 3 4 5 6 255... | - | (hb p. 16) |
| Radius of influence for mapping (ROI) | m | - | - | (hb p. 25) |
| Signal to noise ratio (SNR) | dB | - | - | (hb p. 15) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Grid dimensions (example output) | z=31, y=101, x=101 | (hb p. 19) |
| Projection | pyart_aeqd (azimuthal_equidistant) | (hb p. 20) |
| Semi major axis | 6370997. m | (hb p. 20) |
| Inverse flattening | 298.25 | (hb p. 20) |


## The data

Verified example: **`sgpxsaprmmcgI5.c1`**, file `sgpxsaprmmcgI5.c1.20190331.190008.nc`
(9.47 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1, `nradar`=1, `z`=31, `y`=101, `x`=101 |
| Data variables | 43 |
| QC variables | 0 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2019-03-31T19:00:08 to 2019-03-31T19:00:08 |
| dod version | v1.0 |
| process version | EVAL-0.5 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ROI` | m | time,z,y,x | - | Radius of influence for mapping |
| `SNR` | dB | time,z,y,x | - | Signal to noise ratio |
| `corrected_differential_phase` | degree | time,z,y,x | - | Corrected differential phase (PhiDP) |
| `corrected_differential_reflectivity` | dB | time,z,y,x | - | Corrected differential reflectivity |
| `corrected_reflectivity` | dBZ | time,z,y,x | - | Corrected reflectivity |
| `corrected_specific_diff_phase` | degree/km | time,z,y,x | - | Corrected specific differential phase (KDP) |
| `corrected_velocity` | m/s | time,z,y,x | - | Corrected mean doppler velocity |
| `cross_correlation_ratio_hv` | 1 | time,z,y,x | - | Cross correlation ratio (RhoHV) |
| `differential_phase` | degree | time,z,y,x | - | Differential phase (PhiDP) |
| `differential_reflectivity` | dB | time,z,y,x | - | Differential reflectivity (ZDR) |
| `filtered_corrected_differential_phase` | degree | time,z,y,x | - | Filtered differential phase (PhiDP) |
| `filtered_corrected_specific_diff_phase` | degree/km | time,z,y,x | - | Filtered specific differential phase (KDP) |
| `gate_id` | 1 | time,z,y,x | - | Classification of dominant scatterer |
| `ground_clutter` | 1 | time,z,y,x | - | Ground clutter flag |
| `mean_doppler_velocity` | m/s | time,z,y,x | - | Mean Doppler velocity |
| `normalized_coherent_power` | 1 | time,z,y,x | - | Normalized coherent power |
| `origin_altitude` | m | time | - | Altitude at grid origin |
| `origin_latitude` | degree_N | time | - | Latitude at grid origin |
| `origin_longitude` | degree_E | time | - | Longitude at grid origin |
| `path_integrated_attenuation` | dB | time,z,y,x | - | Path integrated attenuation |
| `path_integrated_differential_attenuation` | dB | time,z,y,x | - | Path integrated differential attenuation |
| `radar_altitude` | m | nradar | - | Altitude of radars used to make the grid. |
| `radar_echo_classification` | 1 | time,z,y,x | - | Radar echo classification |
| `radar_latitude` | degree_N | nradar | - | Latitude of radars used to make the grid. |
| `radar_longitude` | degree_E | nradar | - | Longitude of radars used to make the grid. |
| `radar_name` | - | nradar | - | Name of radar used to make the grid |
| `radar_time` | - | nradar | - | Time in seconds of the volume start for each radar |
| `rain_rate_A` | mm/hr | time,z,y,x | - | rainfall_rate |
| `reflectivity` | dBZ | time,z,y,x | - | Equivalent reflectivity factor |
| `specific_attenuation` | dB/km | time,z,y,x | - | Specific attenuation |


_10 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpxsaprmmcgI5.c1",
                             "start": "2019-03-31", "end": "2019-03-31", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpxsaprmmcgI5.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpxsaprmmcgI5.c1", "2019-03-31", "2019-03-31")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpxsaprmmcgI5.c1", "2019-03-31", "2019-03-31"))   # cite what you pulled
```

This product carries 43 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpxsaprmmcgI5.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['ROI', 'SNR', 'corrected_differential_phase'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpxsaprmmcgI5.c1", "20110818", "20260924")
```

The report's own note on quality: The MMCG data does not have quality control methods applied to it directly; quality control was performed upstream in the CMAC VAP package when the input datastreams for MMCG were created.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Gridding/interpolation uncertainty | Gridded MMCG data can show uncertainties introduced by interpolating/extrapolating radar gate data to common Cartesian grid points, appearing as smoothing or artifacts relative to native... | - | (hb p. 9) |
| Complex parameter space for ROI/interpolation weighting | Retention of storm structure detail versus introduction of artifacts depends on ROI formulation, radar scanning strategy, beam spacing, and the meteorological event occurring, so grid... | ROI is formulated to vary with distance from radar (x, y, height) matched to the scanning strategy so there are enough gates for a reasonable... | (hb p. 6) |
| Reflectivity interpolated in dBZ vs linear Z | If interpolation were done directly in dBZ rather than linear Z, high-reflectivity regions and strong reflectivity gradients would show reduced accuracy, particularly affecting large rain... | MMCG converts dBZ fields to linear Z (mm6 m-3) before interpolation, then converts back to dBZ after interpolation | (hb p. 6) |
| No independent quality control applied in MMCG | MMCG output data quality is entirely inherited from the CMAC input; any QC issues, artifacts or mis-flagged gates in CMAC-processed data pass through unaltered to the Cartesian grid | Quality control was performed upstream in the CMAC VAP package before MMCG mapping | (hb p. 7) |
| Hydrometeor classification (gate_id) mapped with different method than other fields | Gate ID field boundaries on the Cartesian grid may look blockier/steppier or misaligned relative to smoothly-interpolated fields like reflectivity, since it uses nearest neighbor rather... | Documented explicitly in the output NetCDF header: 'This gate id field has been mapped to a Cartesian grid using nearest neighbor. This may differ... | (hb p. 24) |
| Input CMAC data raw moments uncalibrated/uncorrected in original source file | Original XSAPR raw moments file (before CMAC/MMCG processing) carries comment 'Data in this file has not been calibrated, corrected, or had any quality control performed, use with caution' | Use CMAC-processed input (not raw XSAPR file) for MMCG; CMAC applies corrections upstream | (hb p. 17) |
| Time interpolation/approximation flags in input data | file_status flag bits indicate interpolated_time_sec, interpolated_time_ms, approximated_time, missing_rays, or no_kdp_variable conditions in the input CMAC file, meaning some ray times or... | Rounding interpolated time values to nearest second/millisecond can recover original times; refer to .00 files for exact values when rays are not... | (hb p. 14) |
| Missing specific_differential_phase variable in some files | When bit_5 of file_status flag is set, the specific_differential_phase variable contains only _FillValue for that file | - | (hb p. 14) |
| Rain rate set to zero under certain conditions | rain_rate_A values read as 0.0 in regions where normalized coherent power less than  0.4 or rhohv less than  0.8, which could be mistaken for true zero rainfall | - | (hb p. 16) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Cressman, GP. 1959. An operational objective analysis system. Monthly Weather Review 87(10): 367-374
- Helmus, JJ, and SM Collis. 2016. The Python ARM Radar Toolkit (Py-ART), a Library for Working with Weather Radar Data in the Python Programming Language. Journal of Open Research Software 4(1), p.e25
- Trapp, RJ, and CA Doswell. 2000. Radar Data Objective Analysis. Journal of Atmospheric and Oceanic Technology 17(2): 105-120
- Warren, RA, and A Protat. 2019. Should Interpolation of Radar Reflectivity be Performed in Z or dBZ? Journal of Atmospheric and Oceanic Technology 36(6): 1143-1156

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-243.pdf (26 pages, DOE/SC-ARM-TR-243, by Z Sherman, S Collis, J Hemedinger)
- Catalog record: ARM data-source index, `instrument_class_code=mmcg`, read 2026-09-24
- Example file: `sgpxsaprmmcgI5.c1.20190331.190008.nc` from `sgpxsaprmmcgI5.c1`, 9.47 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
