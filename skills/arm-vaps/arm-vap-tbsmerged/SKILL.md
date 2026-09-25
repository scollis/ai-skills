---
name: arm-vap-tbsmerged
description: ARM Tethered Balloon System (TBS) Merged Data Product (tbsmerged) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (planetary boundary layer height, cloud base height, aerosol total number concentration, atmospheric temperature, atmospheric moisture), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgptbsmergedC1.c1) and the variable inventory of a real file. Use when working with tbsmerged data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Airborne Observations. Triggers - tbsmerged, Tethered Balloon System (TBS) Merged Data Product, sgptbsmergedC1.c1, planetary boundary layer height, cloud base height, aerosol total number concentration, atmospheric temperature.
---

# TBSMERGED - Tethered Balloon System (TBS) Merged Data Product

TBSMERGED is a value-added product that merges in situ tethered balloon system (TBS) measurements of temperature, humidity, wind speed/direction, and aerosol properties with ceilometer-derived cloud base and boundary-layer height estimates onto a common time/altitude grid, one file per TBS flight.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbsmerged` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-286 / D Dexheimer, K Gaustad, F Mei, D Zhang / February 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-286.pdf) |
| Category | Airborne Observations |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2017-04-09 to 2025-08-24 (retired) |
| Datastreams with data | 7 across 6 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/tbsmerged |


## Credit

Everything this skill knows about the retrieval is the work of **D Dexheimer, K Gaustad, F Mei, D Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Dexheimer, K Gaustad, F Mei, D Zhang. *Tethered Balloon System Merged Data (TBSMERGED) Value-Added Product Report*, DOE/SC-ARM-TR-286, February 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-286.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The TBSMERGED VAP does not apply special retrieval algorithms or scientific analysis; it consolidates data from six ARM input datastreams (ceilpblht, tbscpc, tbsimet, tbsimetxq2, tbspops, tbswind) onto a common coordinate grid indexed to tbsimet timestamps and altitudes. For each tbsimet.b1 file in a processing period, the corresponding overlapping portions of the other datastreams are retrieved and merged; if multiple non-tbsimet files with differing non-time dimension shapes are found, the file spanning the longest time period is kept and others are deleted. Derived quantities within the merge include cloud base height and up to three candidate planetary boundary-layer heights (with quality indices) from the Vaisala CL-31 ceilometer's built-in algorithms, based on gradient amount, detected cloud bases, and distance to other gradient minima. In the TBSMERGEDINCLOUD variant, supercooled liquid water content (SLWC) is calculated from the rate of change of a vibrating wire on an Anasphere SLWC sonde, combined with TBS vertical speed, horizontal wind speed, and estimates of mean droplet diameter and droplet collection efficiency. Quality checks are applied to 55 variables in the merged output.

**Cadence.** input rate 1-second airborne measurements from wind sensors (tbswind); output every output file produced per TBS flight, timestamps matching tbsimet.b1 input files (hb p. 9).

## Inputs

The report names these instruments and sibling products: ceilpblht (Vaisala CL-31 ceilometer), tbscpc (TSI CPC 3007), tbsimet (iMet RSB-4 radiosonde), tbsimetxq2 (iMet XQ2 UAV sensor), tbspops (Handix Scientific POPS), tbswind (NRG 40C anemometer, RM Young 27106, Vega 28 GNSS compass), tbsground (NRG IceFree3 heated anemometer, Campbell Scientific..., tbsslwc (Anasphere supercooled liquid water content sonde), TBSMERGEDINCLOUD.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| planetary boundary layer height | m | surface to 4,000 m above the... | - | (hb p. 5) |
| cloud base height | m | surface to 7,700 m above the... | - | (hb p. 7) |
| aerosol total number concentration (CPC) | - | 10 nm - 1 µm | - | (hb p. 7) |
| aerosol number concentration and size distribution (POPS) | - | 140 nm - 3 µm | - | (hb p. 7) |
| atmospheric temperature | - | - | - | (hb p. 5) |
| atmospheric moisture (relative humidity, frostpoint, vapor... | - | - | - | (hb p. 5) |
| vertical velocity / ascent rate | - | - | - | (hb p. 9) |
| horizontal wind speed, gust wind speed, wind direction | - | - | - | (hb p. 9) |
| supercooled liquid water content (SLWC, TBSMERGEDINCLOUD... | - | - | - | (hb p. 15) |
| surface temperature, pressure, wind speed, gust wind speed,... | - | - | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Ceilometer cloud layer detection | up to three cloud layers simultaneously between surface and 7,700 m above the surface at 10 m vertical resolution | (hb p. 7) |
| Ceilometer boundary-layer height candidates | up to three candidate planetary boundary-layer heights between surface and 4,000 m above the surface | (hb p. 7) |
| CPC aerosol size range | 10 nm to 1 µm (0.01 μm to 1 μm) | (hb p. 9) |
| POPS aerosol size range | 140 nm to 3 μm | (hb p. 9) |
| Number of CPC units | six TSI CPC 3007 units | (hb p. 9) |
| Number of POPS units | six Handix Scientific POPS units | (hb p. 9) |
| Number of wind sensor units | eight wind sensors units | (hb p. 9) |
| iMet RSB-4 proximity to CPC/POPS | operated within 5 m of each CPC or POPS on the TBS | (hb p. 9) |
| Quality checks applied | 55 variables | (hb p. 11) |
| tbswind sampling rate | 1-second airborne measurements | (hb p. 9) |


## The data

Verified example: **`sgptbsmergedC1.c1`**, file `sgptbsmergedC1.c1.20241111.170511.nc`
(7.45 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=13235, `num_cpc`=1, `num_imet`=1, `num_xq2`=1, `num_pops`=1, `num_anem`=1 |
| Data variables | 147 |
| QC variables | 67 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-11-11T17:05:11 to 2024-11-11T20:45:49 |
| dod version | tbsmerged-c1-1.5 |
| process version | tbsmerged-1.1.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bl_height_1` | m | time | yes | First boundary layer height candidate |
| `bl_height_2` | m | time | yes | Second boundary layer height candidate |
| `bl_height_3` | m | time | yes | Third boundary layer height candidate |
| `bl_index_1` | 1 | time | yes | Quality index for first boundary layer height candidate |
| `bl_index_2` | 1 | time | yes | Quality index for second boundary layer height candidate |
| `bl_index_3` | 1 | time | yes | Quality index for third boundary layer height candidate |
| `first_cbh` | m | time | yes | Lowest cloud base height |
| `second_cbh` | m | time | yes | Second lowest cloud base height |
| `tbscpc_alt` | m | time,num_cpc | yes | Altitude above mean sea level from iMET sensor from CPC |
| `tbscpc_lat` | degree_N | time,num_cpc | yes | North latitude from iMET sensor from CPC |
| `tbscpc_lon` | degree_E | time,num_cpc | yes | East longitude from iMET sensor from CPC |
| `tbscpc_total_concentration` | 1/cm^3 | time,num_cpc | yes | Total number concentration from CPC for the aerosol particles larger... |
| `tbsimet_air_temperature` | degC | time,num_imet | yes | Air temperature corrected for solar radiation from iMET |
| `tbsimet_air_temperature_raw` | degC | time,num_imet | yes | Raw air temperature from iMET |
| `tbsimet_alt` | km | time,num_imet | yes | Altitude above mean sea level from iMET |
| `tbsimet_ascent_rate` | m/s | time,num_imet | yes | Ascent rate of iMET |
| `tbsimet_battery_volt` | V | time,num_imet | yes | Voltage of iMET battery |
| `tbsimet_frostpoint` | degC | time,num_imet | yes | Frostpoint of iMET |
| `tbsimet_gps_ascent_rate` | m/s | time,num_imet | yes | Ascent rate derived from iMET GPS measurements |
| `tbsimet_gps_num_satellites` | count | time,num_imet | yes | Number of GPS satellites from which iMET is receiving signals |
| `tbsimet_gps_pressure` | hPa | time,num_imet | yes | Atmospheric pressure derived from GPS height and radiosonde... |
| `tbsimet_imet_altitude` | km | time,num_imet | yes | Height above ground level from iMET |
| `tbsimet_internal_temperature` | degC | time,num_imet | yes | Internal iMET temperature |
| `tbsimet_lat` | degree_N | time,num_imet | yes | North latitude from iMET |
| `tbsimet_lon` | degree_E | time,num_imet | yes | East longitude from iMET |
| `tbsimet_pressure` | hPa | time,num_imet | yes | Air pressure from iMET |
| `tbsimet_pressure_sensor_temperature` | degC | time,num_imet | yes | Temperature of iMET pressure sensor |
| `tbsimet_rh` | % | time,num_imet | yes | Relative humidity from iMET |
| `tbsimet_rh_sensor_temperature` | degC | time,num_imet | yes | Temperature of humidity sensor from iMET |
| `tbsimet_theta` | K | time,num_imet | yes | Potential temperature from iMET |


_46 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgptbsmergedC1.c1",
                             "start": "2024-11-11", "end": "2024-11-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptbsmergedC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptbsmergedC1.c1", "2024-11-11", "2024-11-11")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgptbsmergedC1.c1", "2024-11-11", "2024-11-11"))   # cite what you pulled
```

This product carries 147 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgptbsmergedC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['bl_height_1', 'bl_height_2', 'bl_height_3', 'qc_bl_height_1', 'qc_bl_height_2', 'qc_bl_height_3'],
                                cleanup_qc=True)
```

## Quality control in this product

67 `qc_` companion variables cover 67 of the
147 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_bl_height_1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("bl_height_1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["bl_height_1", "bl_height_2", "bl_height_3"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgptbsmergedC1.c1.20241111.170511.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `third_cbh` | Transformation could not finish (all values bad or outside... | 13235 | 100.0 |
| `bl_height_3` | Transformation could not finish (all values bad or outside... | 13235 | 100.0 |
| `bl_index_3` | Transformation could not finish (all values bad or outside... | 13235 | 100.0 |
| `first_cbh` | Transformation could not finish (all values bad or outside... | 13235 | 100.0 |
| `second_cbh` | Transformation could not finish (all values bad or outside... | 13235 | 100.0 |
| `bl_height_2` | Transformation could not finish (all values bad or outside... | 4374 | 33.0487 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgptbsmergedC1.c1", "20170409", "20260924")
```

The report's own note on quality: Quality checks are applied for 55 variables in the TBSMERGED output. Each primary variable and many secondary variables have corresponding qc_ variables (e.g., qc_bl_height_1, qc_tbscpc_total_concentration, qc_tbsimet_air_temperature, etc.) included in the output file. Boundary-layer height candidates include a quality index (bl_index_1/2/3) based on gradient amount, detected nearby cloud bases, and distance to other gradient minima.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Dependence on tbsimet.b1 data for output timing | If there is no tbsimet.b1 data for a given period, there will be no tbsmerged data for that same period; output file timestamps match tbsimet.b1 sample times exactly | None stated | (hb p. 11) |
| Non-mergeable extra files with differing shapes | When multiple non-tbsimet.b1 files exist for the same period with differing non-time dimension sizes, only the file spanning the longest overlapping time period is retained and the others... | The shape of the non-tbsimet file spanning the longest time period of the tbsimet.b1 file is used; extra files with a different shape are deleted | (hb p. 10) |
| TBSMERGEDINCLOUD (SLWC) data availability limitation | tbsslwc data will only be included when made available on ARM's Data Discovery; product currently limited to OLI site | SLWC will be included in TBSMERGEDINCLOUD once tbsslwc data are available on ARM Data Discovery | (hb p. 7) |
| No independent scientific/QC algorithm applied by the VAP itself | TBSMERGED and TBSMERGEDINCLOUD do not apply special algorithms or perform scientific analysis; users should treat this as a consolidation of raw/QC'd inputs, not a new retrieval | None stated | (hb p. 9) |
| Boundary-layer height quality index affected by nearby clouds and low gradients | Quality index for each boundary-layer height candidate is reduced when clouds are detected in the vicinity of a boundary layer; low gradient amount yields high quality index while high... | Use provided quality index (bl_index_1/2/3) to assess candidate reliability | (hb p. 7) |
| Different aerosol concentration scales between POPS and CPC | Different limits on the particle concentration color bars between the POPS and CPC plots (as noted in Figure 1) can cause misinterpretation if not accounted for | Note the different limits when comparing plots | (hb p. 8) |
| Multiple redundant instruments on tether not resolved to single 'truth' value | More than one CPC, POPS, iMet RSB-4, iMet XQ2, or wind sensor may be operated from different locations on the tether during the same flight, producing multiple values per variable... | None stated beyond dimensioning output arrays by instrument count | (hb p. 9) |
| iMet XQ2 as redundant backup only | tbsimetxq2 datastream functions as a redundant source of altitude and meteorological data only in the event of an iMet RSB-4 radiosonde failure, so its presence/absence in merged output... | None stated | (hb p. 9) |
| Vertical wind speed requires correction for platform motion | The vertical wind speed measurement (RM Young 27106) is corrected for the ascent rate of the TBS measured in the tbsimet datastream; uncorrected data would show platform-induced bias | Corrected using ascent rate from tbsimet datastream | (hb p. 9) |
| Missing EMSL microscopy/spectroscopy/mass spectrometry data | PNNL's EMSL microscopy, spectroscopy, and advanced mass spectrometry results are not currently available on ARM Data Discovery and thus not integrated into TBSMERGED | Could be integrated into TBSMERGED in the future if made available | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Bezantakos, S, and G Biskos. 2022. Journal of Aerosol Science 159: 105877
- Dexheimer D, et al. 2019. Atmospheric Measurement Techniques 12(12): 6845-6864
- Kuang, C, and F Mei. 2016. Condensation Particle Counter (CPC) Instrument Handbook. DOE/SC-ARM-TR-145
- Mei, F, and M Pekour. 2020. Portable Optical Particle Spectrometer (POPS) Instrument Handbook. DOE/SC-ARM-TR-259
- Mei, F, et al. 2020b. Sensors 20(21): 6294
- Morris VR. 2016. Ceilometer Instrument Handbook. DOE/SC-ARM-TR-020

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-286.pdf (17 pages, DOE/SC-ARM-TR-286, by D Dexheimer, K Gaustad, F Mei, D Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=tbsmerged`, read 2026-09-24
- Example file: `sgptbsmergedC1.c1.20241111.170511.nc` from `sgptbsmergedC1.c1`, 7.45 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
