---
name: arm-vap-sfccldgrid
description: ARM Surface Cloud Grid (sfccldgrid) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (downwelling_shortwave, Clearsky_downwelling_shortwave, Downwelling_longwave, Clearsky_downwelling_longwave, Upwelling_shortwave, Upwelling_longwave), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpsfccldgrid2longstationN1.c1) and the variable inventory of a real file. Use when working with sfccldgrid data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Derived Quantities and Models. Triggers - sfccldgrid, Surface Cloud Grid, sgpsfccldgrid2longstationN1.c1, downwelling_shortwave, Clearsky_downwelling_shortwave, Downwelling_longwave, Clearsky_downwelling_longwave.
---

# SFCCLDGRID - Surface Cloud Grid

The Surface Cloud Grid VAP produces gridded surface-based cloud fraction, cloud transmissivity, and broadband shortwave/longwave radiation quantities over the ARM SGP domain by interpolating radiative flux analysis outputs from the network of SGP Central Facility and extended facility surface stations onto a 0.25-degree latitude/longitude grid.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 25 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sfccldgrid` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-010 / L Riihimaki, K Gaustad / March 2020](https://www.arm.gov/publications/tech_reports/arm-tr-010.pdf?id=48) |
| Category | Cloud Properties; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1997-01-01 to 2020-06-01 (retired) |
| Datastreams with data | 3 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sfccldgrid |


## Credit

Everything this skill knows about the retrieval is the work of **L Riihimaki, K Gaustad** -
the ARM developers and mentors who wrote the technical report it derives from:

> L Riihimaki, K Gaustad. *Surface Cloud Grid Version 2 (SFCCLDGRID2) Value-Added Product: Description of Updates to Algorithm Operational Details in Version 2*, DOE/SC-ARM-TR-010, March 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-tr-010.pdf?id=48

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Clouds decrease downwelling shortwave (SW) irradiance and increase downwelling longwave (LW) irradiance relative to cloudless conditions, so surface broadband radiation measurements can be used to infer cloud properties. The VAP takes RADFLUXANAL VAP output (clear-sky broadband radiation estimates and derived parameters from SIRS and MET measurements run through QCRAD) for each SGP extended facility station, averages it to 15-minute resolution, and combines multi-station station files. These station values are then interpolated onto a 0.25-degree by 0.25-degree latitude/longitude grid over the SGP domain using a multi-pass, weighted-sum, analytic approximation (objective Gaussian interpolation) technique (Caracena 1987) with a 100 km Gaussian length scale and 16 passes. The ratio of measured over clear-sky-fit SW irradiance (cloud transmissivity) is used because it effectively removes instrument characteristics such as cosine response errors and calibration drifts, allowing high-confidence comparison to model cloudy/cloudless ratios. Output is only provided when solar elevation angles are 10 degrees or greater, and at least 13 different station locations must be present for a successful VAP run.

**Cadence.** output every 15-minute-average time resolution; averaging Input data averaged to 15-minute time resolution before gridding; comparisons in Table 3 use daily averages (hb p. 10).

## Inputs

The report names these instruments and sibling products: SWFLUXANAL (Shortwave Flux Analysis VAP), RADFLUXANAL (Radiative Flux Analysis VAP), QCRAD (Data Quality Assessment for ARM Radiation Data VAP), SIRS (solar and infrared radiation station), MET (surface meteorology measurements), VISST (Visible Infrared Solar-Infrared Split Window Technique..., SfcCldGrid1Long (Version 1 Surface Cloud Grid VAP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| downwelling_shortwave | - | - | - | (hb p. 11) |
| Clearsky_downwelling_shortwave | - | - | - | (hb p. 11) |
| Downwelling_longwave | - | - | - | (hb p. 11) |
| Clearsky_downwelling_longwave | - | - | - | (hb p. 11) |
| Upwelling_shortwave | - | - | - | (hb p. 11) |
| Upwelling_longwave | - | - | - | (hb p. 11) |
| Clearsky_upwelling_longwave | - | - | - | (hb p. 11) |
| Diffuse_downwelling_shortwave | - | - | - | (hb p. 11) |
| Clearsky_diffuse_downwelling_shortwave | - | - | - | (hb p. 11) |
| Direct_downwelling_shortwave | - | - | - | (hb p. 11) |
| Clearsky_direct_downwelling_shortwave | - | - | - | (hb p. 11) |
| Cloudfraction_longwave | - | - | considered preliminary; should be used with... | (hb p. 11) |
| Cloudfraction_shortwave | - | 0 to 1.1 (QA limit) | - | (hb p. 11) |
| Cloud_transmissivity_shortwave | - | - | - | (hb p. 12) |
| Visible_cloud_optical_depth | - | - | only available for overcast conditions, many... | (hb p. 12) |
| Cloud_radiating_temperature | - | - | roughly equivalent to an infrared thermometer... | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Grid resolution | 0.25° by 0.25° latitude/longitude | (hb p. 8) |
| Original domain (Version 1) | 95.5° to 99.5° west longitude and 34.5° to 38.5° north latitude, 300 km domain, 21 sites | (hb p. 8) |
| Interpolation technique | multi-pass, weighted sum, analytic approximation (Gaussian weighting), Caracena 1987 | (hb p. 8) |
| Interpolation Gaussian length scale | 100 km | (hb p. 12) |
| Interpolation passes | 16 passes | (hb p. 12) |
| Minimum station locations required | At least 13 different locations | (hb p. 12) |
| Output solar elevation threshold | solar elevation angles 10° or greater | (hb p. 8) |
| Station data temporal resolution | 15-minute-average | (hb p. 10) |
| Cloud fraction QA limits | between 0 and 1.1 | (hb p. 13) |
| SW variable low-sun-angle missing threshold | cosz greater than  80 (set to missing) | (hb p. 13) |
| VISST comparison product resolution | 30-minute temporal resolution and 0.5-degree latitude/longitude resolution | (hb p. 14) |


## The data

Verified example: **`sgpsfccldgrid2longstationN1.c1`**, file `sgpsfccldgrid2longstationN1.c1.20200529.060000.nc`
(0.38 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=96, `bound`=2, `station`=19 |
| Data variables | 62 |
| QC variables | 18 (`qc_` companions) |
| Median time step | 900 s |
| File time span | 2020-05-29T06:00:00 to 2020-05-30T05:45:00 |
| dod version | sfccldgrid2longstation-c1-1.1 |
| process version | vap-sfccldgrid2long_station-1.4-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cflw` | 1 | time,station | yes | Estimated effective longwave fractional sky cover |
| `cfsw` | 1 | time,station | yes | Estimated shortwave fractional sky cover |
| `clearsky_status` | 1 | time,station | yes | Clear-sky status |
| `cloud_radiating_temperature` | K | time,station | yes | Estimated effective cloud radiating temperature |
| `clwdn` | W/m^2 | time,station | yes | Estimated clear-sky downwelling longwave irradiance |
| `clwup` | W/m^2 | time,station | yes | Estimated clear-sky upwelling longwave irradiance |
| `cswdif` | W/m^2 | time,station | yes | Estimated clear-sky diffuse downwelling shortwave irradiance |
| `cswdir` | W/m^2 | time,station | yes | Estimated clear-sky direct downwelling shortwave irradiance |
| `cswdn` | W/m^2 | time,station | yes | Estimated clear-sky broadband downwelling shortwave irradiance |
| `cswup` | W/m^2 | time,station | yes | Estimated clear-sky upwelling shortwave irradiance |
| `lwdn` | W/m^2 | time,station | yes | Downwelling longwave irradiance from pyrgeometer |
| `lwup` | W/m^2 | time,station | yes | Upwelling longwave irradiance from pyrgeometer |
| `swdif` | W/m^2 | time,station | yes | Measured broadband diffuse downwelling shortwave irradiance |
| `swdir` | W/m^2 | time,station | yes | Measured direct downwelling shortwave irradiance |
| `swdn` | W/m^2 | time,station | yes | Broadband downwelling shortwave irradiance from sum or global... |
| `swup` | W/m^2 | time,station | yes | Upwelling shortwave irradiance from pyranometer |
| `trans` | 1 | time,station | yes | Shortwave cloud transmissivity |
| `visible_cloud_optical_depth` | 1 | time,station | yes | Estimated effective visible cloud optical depth |
| `cosine_zenith` | 1 | time,station | - | Cosine of solar zenith angle |
| `num_sites_cflw` | 1 | time | - | Number of Facilities with Estimated effective longwave fractional sky... |
| `num_sites_cfsw` | 1 | time | - | Number of Facilities with Estimated shortwave fractional sky cover |
| `num_sites_clearsky` | 1 | time | - | Number of Facilities with Clear-sky status |
| `num_sites_cloud_radiating_temperature` | 1 | time | - | Number of Facilities with Estimated effective cloud radiating... |
| `num_sites_clwdn` | 1 | time | - | Number of Facilities with Estimated clear-sky downwelling longwave... |
| `num_sites_clwup` | 1 | time | - | Number of Facilities with Estimated clear-sky upwelling longwave... |
| `num_sites_cswdif` | 1 | time | - | Number of Facilities with Estimated clear-sky diffuse downwelling... |
| `num_sites_cswdir` | 1 | time | - | Number of Facilities with Estimated clear-sky direct downwelling... |
| `num_sites_cswdn` | 1 | time | - | Number of Facilities with Estimated clear-sky broadband downwelling... |
| `num_sites_cswup` | 1 | time | - | Number of Facilities with Estimated clear-sky upwelling shortwave... |
| `num_sites_lwdn` | 1 | time | - | Number of Facilities with Downwelling longwave irradiance from... |


_9 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpsfccldgrid2longstationN1.c1",
                             "start": "2020-05-29", "end": "2020-05-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsfccldgrid2longstationN1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsfccldgrid2longstationN1.c1", "2020-05-29", "2020-05-29")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsfccldgrid2longstationN1.c1", "2020-05-29", "2020-05-29"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("num_sites_swdn")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 62 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpsfccldgrid2longstationN1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["swdn", "cswdn", "lwdn", "qc_swdn", "qc_cswdn", "qc_lwdn"],
                                cleanup_qc=True)
```

## Quality control in this product

18 `qc_` companion variables cover 18 of the
62 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_swdn"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("swdn", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["swdn", "cswdn", "lwdn"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpsfccldgrid2longstationN1.c1.20200529.060000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `visible_cloud_optical_depth` | QC_BAD: Transformation could not finish, value set to... | 1824 | 100.0 |
| `cloud_radiating_temperature` | QC_BAD: Transformation could not finish, value set to... | 1823 | 99.9452 |
| `visible_cloud_optical_depth` | QC_ALL_BAD_INPUTS: All the input values in the transformation... | 1536 | 84.2105 |
| `cloud_radiating_temperature` | QC_SOME_BAD_INPUTS: Some, but not all, of the inputs in the... | 1536 | 84.2105 |
| `visible_cloud_optical_depth` | QC_SOME_BAD_INPUTS: Some, but not all, of the inputs in the... | 1536 | 84.2105 |
| `cloud_radiating_temperature` | QC_ALL_BAD_INPUTS: All the input values in the transformation... | 1535 | 84.1557 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpsfccldgrid2longstationN1.c1", "19970101", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Input data pass through QCRAD VAP quality control testing (Long and Shi 2006, 2008) before being used in RADFLUXANAL and then SFCCLDGRID2. SFCCLDGRID2 applies additional QA including maximum/minimum limits (cloud fraction between 0 and 1.1) and sets SW variables (cloud fraction SW, transmissivity, direct, diffuse, SW down, SW up) to missing when sun angle is low (cosz greater than  80) in both station and gridded products. An "edge qc" test flags grid cells near domain edges with missing/bad facility data as suspect, applied independently to each of the four quadrants by working inward from...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Edge-of-domain suspect interpolation | Red filled rectangles/shaded regions on the grid, particularly the lower row of the bottom-left quadrant and right column of the upper-right quadrant, always marked suspect; e.g., southeast... | These edge areas are based on extrapolation from sites to the interior and should not be used, or should be used with significant caution | (hb p. 13) |
| Missing/insufficient station data affecting interpolation | Open green circles indicate a facility did not report data for a given time sample, reducing constraint on the interpolation near that location | At least 13 different locations must be present for a successful VAP run | (hb p. 12) |
| Cloudfraction_longwave is preliminary | LW-derived fractional sky cover values may be unreliable or inconsistent compared to SW-derived cloud fraction | Should be used with significant caution | (hb p. 11) |
| Clearsky_upwelling_longwave only available during clear periods | Large gaps/missing values during cloudy periods since no clear-sky LW upwelling estimate is produced when cloudy | None stated beyond noting the limitation in current RADFLUXANAL version | (hb p. 11) |
| Visible_cloud_optical_depth limited to overcast conditions | Many missing periods in the optical depth variable outside overcast conditions | None stated; expected limitation of the retrieval | (hb p. 12) |
| Low solar elevation angle exclusion | No VAP output when solar elevation angle is below 10°; SW variables set to missing when cosz greater than  80 | Output only generated for solar elevation greater than =10°; SW variables (cloud fraction SW, transmissivity, direct, diffuse, SW down, SW up) set to... | (hb p. 13) |
| Collocated CF instrument redundancy handling | Only one value used for CF grid point even though three instruments (C1, E13, BRS) are collocated there, which could mask disagreement between the three station measurements | Average of closest two of three stations if all report; average of two if only two report; otherwise use the single reporting station | (hb p. 10) |
| Point-vs-domain averaging discrepancy | Standard deviations of daily average differences between CF point measurement and domain averages increase with box size (e.g., cloud fraction st.dev. 0.06 for 1x1 up to 0.11 for Full... | None specific; presented as an estimate of how point measurements compare to model gridbox or satellite footprint geometry | (hb p. 15) |
| Interpolation uncertainty is site-dependent | Sites on the edge of the domain show larger influence/uncertainty than sites in the middle of the domain; 15-minute resolution SW variable uncertainties on the order of 10-20% depending on... | Uncertainty decreases significantly with longer averaging time; see Long and Christy (2005) and Christy et al. (2002) for detailed uncertainty... | (hb p. 14) |
| Network reconfiguration discontinuity | Version 1 of the VAP was paused in November 2009 when the SGP extended facility network was reconfigured to a smaller domain, creating a data gap/version break between SfcCldGrid1 and... | Updated Version 2 (SfcCldGrid2) developed to run on the reconfigured, smaller domain using RADFLUXANAL VAP inputs | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Barnard, JC, and CN Long. 2004. A Simple Empirical Equation to Calculate Cloud Optical Thickness Using Shortwave Broadband Measurements. Journal of the Applied Meteorology and Climatology 43(7): 1057-1066
- Caracena, F. 1987. Analytic Approximation of Discrete Field Samples with Weighted Sums and the Gridless Computation of Field Derivatives. Journal of the Atmospheric Sciences 44(24): 3753-3768
- Christy, JE, CN Long, and TR Shippert. 2002. Interpolation Uncertainties Across the ARM SGP Area. Proceedings of the Twelfth ARM Science Team Meeting
- Christy, JE, and CN Long. 2005. Surface Cloud Grid (SfcCldGrid) Value-Added Product: Algorithm Operational Details and Explanations. DOE/SC-ARM-TR-010
- Long, CN. 2001. The Shortwave (SW) Clear-Sky Detection and Fitting Algorithm: Algorithm Operational Details and Explanations. DOE/SC-ARM TR-004
- Long, CN, TP Ackerman, JJ DeLuisi, and J Augustine. 1999. Estimation of Fractional Sky Cover from Broadband SW Radiometer Measurements. AMS Tenth Conference on Atmospheric Radiation
- Long, CN, and TP Ackerman. 2000. Identification of Clear Skies from Broadband Pyranometer Measurements and Calculation of Downwelling Shortwave Cloud Effects. Journal of Geophysical Research - Atmospheres 105(D12):...
- Long, CN, TP Ackerman, KL Gaustad, and JNS Cole. 2006. Estimation of fractional sky cover from broadband shortwave radiometer measurements. Journal of Geophysical Research - Atmospheres 111(D11): D11204
- Long, CN, and DD Turner. 2008. A method for continuous estimation of clear-sky downwelling longwave radiative flux developed using ARM surface measurements. Journal of Geophysical Research 113(D18): D18206
- Long, CN, and Y Shi. 2006. The QCRad Value Added Product: Surface Radiation Measurement Quality Control Testing, Including Climatology Configurable Limits. DOE/SC-ARM/TR-074

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-tr-010.pdf?id=48 (25 pages, DOE/SC-ARM-TR-010, by L Riihimaki, K Gaustad)
- Catalog record: ARM data-source index, `instrument_class_code=sfccldgrid`, read 2026-09-24
- Example file: `sgpsfccldgrid2longstationN1.c1.20200529.060000.nc` from `sgpsfccldgrid2longstationN1.c1`, 0.38 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
