---
name: arm-vap-qcrad
description: ARM Data Quality Assessment for ARM Radiation Data (qcrad) - value-added product reference from its technical report. Derived from gndrad, mfrsr, sirs, skyrad. The retrieval algorithm, reported quantities (Global SWdn, Diffuse SW, Direct Normal SW, SWup, LWdn, LWup), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpqcradbrs1longC1.c1) and the variable inventory of a real file. Use when working with qcrad data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Radiometric. Triggers - qcrad, Data Quality Assessment for ARM Radiation Data, sgpqcradbrs1longC1.c1, gndrad VAP, mfrsr VAP, sirs VAP, Global SWdn, Diffuse SW, Direct Normal SW, SWup, LWdn, Radiometric.
---

# QCRAD - Data Quality Assessment for ARM Radiation Data

QCRad is an ARM value-added product that automatically applies a hierarchy of physical, climatological, and cross-comparison quality control tests to broadband surface radiation measurements (from SIRS, MFRSR, SKYRAD, GNDRAD instruments) and outputs QC-flagged and best-estimate global shortwave irradiance data.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 70 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `qcrad` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-074 / C.N. Long, Y. Shi / September 2006](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-074.pdf) |
| Category | Radiometric |
| Input instruments | `gndrad`, `mfrsr`, `sirs`, `skyrad` |
| Record | 1993-09-01 to 2026-09-23 (active) |
| Datastreams with data | 174 across 25 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/qcrad |


## Credit

Everything this skill knows about the retrieval is the work of **C.N. Long, Y. Shi** -
the ARM developers and mentors who wrote the technical report it derives from:

> C.N. Long, Y. Shi. *The QCRad Value Added Product: Surface Radiation Measurement Quality Control Testing, Including Climatology Configurable Limits*, DOE/SC-ARM/TR-074, September 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-074.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Extraction coverage.** the report is 70 pages; pages 1-52 and 69-70 were read, and Appendix B's CDL output-field dump was not, so the datastream and quantity lists here are partial. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

QCRad uses climatological analyses of surface radiation measurements to define reasonable limits for testing data for unusual values, assuming that the majority of climatological data are 'good.' Data outside normal ranges are labeled 'indeterminate' (possible but rare) or 'bad' depending on how far outside the range they fall. The methodology applies three levels of testing in order of severity: BSRN Physically Possible global limits, extremely-rare/second-level configurable climatological limits, and first-level configurable climatological limits, using the cosine of the solar zenith angle as the independent variable for shortwave and comparisons to 2-meter air temperature (via Stefan-Boltzmann relations) for longwave. Cross-comparison tests (e.g., Global/Sum SW ratio, Diffuse/Global ratio, clear-sky tracker-off test, Rayleigh diffuse limit, SWup vs Sum SW, LWdn vs LWup, pyrgeometer case/dome vs air temperature) are also applied to detect instrument problems such as solar tracker misalignment, IR loss, and thermal sensor anomalies. A best estimate of global shortwave is derived from the sum of direct and diffuse components, gap-filled using fitted relationships with the unshaded pyranometer or MFRSR measurements.

**Cadence.** input rate 1-minute resolution data; output every Daily NetCDF output files (processes previous day's data); averaging 11-minute running standard deviation and 11-minute running average used for pyrgeometer noise testing (hb p. 39).

## Inputs

ARM's catalog declares these input instrument classes: `gndrad`, `mfrsr`, `sirs`, `skyrad`.

The report names these instruments and sibling products: gndrad, mfrsr, sirs, skyrad, Diffuse IR Loss Correction VAP, Best Estimate Flux VAP.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Global SWdn (downwelling shortwave, unshaded pyranometer) | Wm-2 | Min -4 Wm-2; Max Sa x 1.5 x... | - | (hb p. 8) |
| Diffuse SW (shaded pyranometer) | Wm-2 | Min -4 Wm-2; Max Sa x 0.95 x... | - | (hb p. 8) |
| Direct Normal SW | Wm-2 | Min -4 Wm-2; Max Sa (BSRN... | - | (hb p. 8) |
| SWup (upwelling shortwave) | Wm-2 | Min -4 Wm-2; Max Sa x 1.2 x... | - | (hb p. 8) |
| LWdn (downwelling longwave) | Wm-2 | Min 40 Wm-2; Max 700 Wm-2 (BSRN... | - | (hb p. 8) |
| LWup (upwelling longwave) | Wm-2 | Min 40 Wm-2; Max 900 Wm-2 (BSRN... | - | (hb p. 8) |
| Air temperature (Ta) | K | 170 K less than  Ta less than ... | - | (hb p. 6) |
| Pyrgeometer case temperature (Tc) | K | - | - | (hb p. 6) |
| Pyrgeometer dome temperature (Td) | K | - | - | (hb p. 6) |
| Surface station pressure (Prs) | millibars | - | - | (hb p. 6) |
| Best Estimate Global Downwelling Shortwave Hemispheric... | W/m^2 | - | - | (hb p. 51) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| S0 (solar constant at mean Earth-Sun distance) | 1368 Wm-2 | (hb p. 6) |
| sigma (Stefan-Boltzmann constant) | 5.67 x 10-8 Wm-2 K-4 | (hb p. 6) |
| Tsnw (SGP) | 8-9.0 degC (snow-covered ground Ta limit for albedo tests) | (hb p. 11) |
| Tsnw (TWP) | 0.0 degC | (hb p. 38) |
| Tsnw (NSA) | 5.0 degC | (hb p. 38) |
| Tmin (SGP) | -20 degC (Min climatological allowable Ta,Td,Tc) | (hb p. 38) |
| Tmax (SGP) | 42 degC (Max climatological allowable Ta,Td,Tc) | (hb p. 38) |
| Tmin/Tmax global bound | 170 K less than  Ta less than  350 K | (hb p. 6) |
| 11-minute running standard deviation noise test threshold | Tc(d)_sdev - Tc(d)_avg_sdev greater than  0.1 K = data BAD | (hb p. 14) |
| Tracker off limit (SGP & NSA) | 0.9 | (hb p. 43) |
| Tracker off limit (TWP) | 0.85 | (hb p. 43) |


## The data

Verified example: **`sgpqcradbrs1longC1.c1`**, file `sgpqcradbrs1longC1.c1.20260827.000000.nc`
(0.45 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 70 |
| QC variables | 21 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-08-27T00:00:00 to 2026-08-27T23:59:00 |
| dod version | qcradbrs1long-c1-2.1 |
| process version | qcrad1long-7.1.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `BestEstimate_down_short_hemisp` | W/m^2 | time | yes | Best Estimate Global Downwelling Shortwave Hemispheric Irradiance |
| `LWdnTc` | degC | time | yes | Downwelling LW Case Temperature |
| `LWdnTd` | degC | time | yes | Downwelling LW Dome Temperature |
| `LWupTc` | degC | time | yes | Upwelling LW Case Temperature |
| `LWupTd` | degC | time | yes | Upwelling LW Dome Temperature |
| `MFRSR_diffuse_hemisp_broadband` | W/m^2 | time | yes | MFRSR Broadband Diffuse SW |
| `MFRSR_direct_normal_broadband` | W/m^2 | time | yes | MFRSR Broadband Direct Normal SW |
| `MFRSR_hemisp_broadband` | W/m^2 | time | yes | MFRSR Broadband Global SW |
| `Temp_Air` | degC | time | yes | Air Temperature |
| `detector_flux` | W/m^2 | time | yes | Detector flux (Downwelling pyrgeometer thermopile voltage * PIR-DIR... |
| `down_long_hemisp` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance |
| `down_short_diffuse_hemisp` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance |
| `down_short_hemisp` | W/m^2 | time | yes | IR corrected Global Downwelling Shortwave Hemispheric Irradiance |
| `precip` | mm | time | yes | Precipitation |
| `press` | kPa | time | yes | Atmospheric Pressure |
| `rh` | % | time | yes | Relative Humidity |
| `short_direct_normal` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance |
| `up_long_hemisp` | W/m^2 | time | yes | Upwelling (10 meter) Longwave Hemispheric Irradiance |
| `up_short_hemisp` | W/m^2 | time | yes | Upwelling Shortwave Hemispheric Irradiance |
| `wind_direction` | degree | time | yes | Wind Direction |
| `wind_speed` | m/s | time | yes | Wind Speed |
| `MFRSR_flag` | 1 | time | - | MFRSR Data Usage Flag |
| `aqc_DifSW2GSW` | 1 | time | - | DifSW/GSW test |
| `aqc_GSW2SumSW` | 1 | time | - | GSW/SumSW test |
| `aqc_LWdn2LWup` | 1 | time | - | down_long_hemisp (LWdn) to up_long_hemisp (LWup) test |
| `aqc_LWdn2Ta` | 1 | time | - | down_long_hemisp (LWdn) to Ta test |
| `aqc_LWdnTc2Ta` | 1 | time | - | LWdn Tc vs Ta |
| `aqc_LWdnTc2Td` | 1 | time | - | LWdn Tc vs Td |
| `aqc_LWdnTd2Ta` | 1 | time | - | LWdn Td vs Ta |
| `aqc_LWup2Ta` | 1 | time | - | up_long_hemisp (LWup) to Ta test |


_15 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpqcradbrs1longC1.c1",
                             "start": "2026-08-27", "end": "2026-08-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpqcradbrs1longC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpqcradbrs1longC1.c1", "2026-08-27", "2026-08-27")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpqcradbrs1longC1.c1", "2026-08-27", "2026-08-27"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("BestEstimate_down_short_hemisp", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 70 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpqcradbrs1longC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["BestEstimate_down_short_hemisp", "down_short_hemisp", "down_short_diffuse_hemisp", "qc_BestEstimate_down_short_hemisp", "qc_down_short_hemisp", "qc_down_short_diffuse_hemisp"],
                                cleanup_qc=True)
```

## Quality control in this product

21 `qc_` companion variables cover 21 of the
70 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_BestEstimate_down_short_hemisp"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("BestEstimate_down_short_hemisp", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["BestEstimate_down_short_hemisp", "down_short_hemisp", "down_short_diffuse_hemisp"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpqcradbrs1longC1.c1.20260827.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `LWdnTc` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |
| `LWdnTd` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |
| `LWupTc` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |
| `LWupTd` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |
| `detector_flux` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |
| `MFRSR_hemisp_broadband` | Data value not available in input file, data value set to -9999... | 1440 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpqcradbrs1longC1.c1", "19930901", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: QC flag of 0 indicates data passed all tests ('good'). Odd QC flag values generally indicate a measurement below the corresponding minimum limit; even values indicate above the maximum limit. A flag of -1 means the test could not be performed (e.g., due to missing input), not that data are bad. Testing is applied hierarchically from largest (BSRN Physically Possible, flags 5-6) to smallest (1st level configurable, flags 1-2) limits; data failing 2nd-level or PP limits (flags 3-6) have their value set to -9999.0 ('bad'), while 1st-level failures (flags 1-2) retain the data value but flag it as...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| IR loss in unshaded (global) pyranometer measurements | Negative or anomalously low GSW values at night; GSW/Sum SW ratio decreasing with increasing SZA resembling cosine response error; 40-60% of data failing minimum GSW Physically Possible... | Generic detector-only correction coefficients (moist/dry mode, from historical nighttime data vs detector flux) applied to unshaded pyranometer... | (hb p. 9) |
| Diffuse pyranometer IR loss (thermal offset) | Diffuse SW falling below Rayleigh limit; Diffuse/Global ratio failures | Corrected via ARM Diffuse IR Loss Correction VAP (Younkin and Long 2004) | (hb p. 6) |
| Wrong date/time stamp on shortwave data | Points from SZA ~65 degrees upward residing above physically possible limits and increasing as SZA increases | - | (hb p. 10) |
| Solar tracker misalignment / 'tracker off' | Ratio of measured/clear-sky SWdn greater than 0.85 AND ratio of shaded/unshaded pyranometer greater than 0.85 simultaneously (mutually exclusive conditions); pink dots in diffuse SW plots;... | Flagged via 'tracker off' test (QC flag 9); test does not work when cloud blocks direct beam but sum of direct+diffuse remains valid | (hb p. 6) |
| Snow-covered ground causing high albedo/upwelling SW | SWup values elevated at high SZA (greater than 55 deg); data between 1st and 2nd level SWup limits during snow events; sharp drop in SWup after spring snowmelt (e.g., NSA Barrow) | Use air-temperature-based discrimination (Tsnw limit, e.g., 8 degC at SGP) to apply more restrictive albedo limits when snow is unlikely;... | (hb p. 11) |
| Non-definitive comparison test failures (Global/Sum SW ratio, Diffuse/Global SW ratio,... | Ratio tests fail but cannot identify which of the compared measurements is bad | QC flag set (1 or 2) but no data values are set to -9999 for non-definitive tests | (hb p. 9) |
| Pyrgeometer case/dome temperature 'noisy' behavior | 11-minute running standard deviation of 1-minute data much larger than standard deviation of 11-minute running average ('smoothed') data; extremely noisy LW time series since Tc/Td used to... | Flag data as bad when Tc(d)_sdev - Tc(d)_avg_sdev greater than  0.1 K; example shown for SGP E1 June 10, 2000 | (hb p. 8) |
| Pyrgeometer case/dome temperature disagreement with air temperature (thermal shock) | Case or dome temperature differing from air temperature beyond set limits (Figure 11); occurs e.g. under thermal shock such as onset of heavy cold rain on a warm day | Flag data as bad (QC flag 4 or higher, data set to -9999) when tests fail | (hb p. 17) |
| Case minus dome temperature difference anomalies | Downwelling dome cooler than case by more than 2degC, or upwelling case/dome differing beyond normal ~0.5degC range | Tested via C18/C19 limits (Tc-Td difference test), flagged QC13-18 | (hb p. 16) |
| Instrument/system-wide anomalies (e.g., beginning of September event) | Significant simultaneous test failures across total, diffuse, and upwelling SW on the same day, indicating a system problem rather than a single instrument issue | - | (hb p. 30) |
| Unrealistically high upwelling SW at tropical sites (Nauru, Manus) | SWup exceeding max albedo limit for near-freezing temperatures at sites where freezing never occurs (e.g., Nauru day ~220 1999) | Flagged by temperature-screened SWup test | (hb p. 32) |
| Correlated LWup low / SWup high anomalies during RESET visits at TWP | Anomalously low upwelling LW coinciding with anomalously high upwelling SW during instrument RESET visits when downward-facing instruments are turned upward for comparison | - | (hb p. 34) |
| Missing input data (air temperature, pyrgeometer temps, etc.) | Tests dependent on missing values cannot be applied | QC flag set to -1, meaning test could not be applied (not indicative of bad data) | (hb p. 2) |
| Ambiguity in Ta discrimination for cold conditions | Lower air temperatures can occur in winter with no snow present, so cold-temperature albedo testing is less reliable than warm-temperature testing | Accepted limitation; testing improves more for warmer conditions than cold | (hb p. 6) |
| Different instrument replacement dates across sites/years introduce calibration... | Step changes in derived correction coefficients or measurement offsets between years | Annual radiometer replacement with newly calibrated units; correction coefficients derived per site/facility per historical analysis | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `gndrad`: load `arm-instrument-gndrad` for its handbook facts and artifacts
- input instrument `mfrsr`: load `arm-instrument-mfrsr` for its handbook facts and artifacts
- input instrument `sirs`: load `arm-instrument-sirs` for its handbook facts and artifacts
- input instrument `skyrad`: load `arm-instrument-skyrad` for its handbook facts and artifacts

### References the report cites

- Long, CN, and TP Ackerman. 2000. 'Identification of clear skies from broadband pyranometer measurements and calculation of downwelling shortwave cloud effects.' JGR 105(D12)15609-15626.
- Long, CN, and EG Dutton. 2002. 'BSRN Global Network recommended QC tests, V2.0.' BSRN Technical Report.
- Long, CN, and KL Gaustad. 2004. 'The Shortwave (SW) Clear-Sky Detection and Fitting Algorithm.' ARM TR-004.
- Ohmura, A, et al. 1998. 'Baseline Surface Radiation Network (BSRN/WCRP): New precision radiometry for climate research.' Bulletin of the American Meteorological Society 79(10)2115-2136.
- Reda, I, et al. 2005. 'Using a blackbody to calculate net-longwave responsivity of shortwave solar pyranometers...' JAOT 22(10)1531-1540.
- Shi, Y, and CN Long. 2003. 'Preliminary analysis of surface radiation measurement data quality at the SGP Extended Facilities.' ARM Science Team Meeting.
- Shi, Y, and CN Long. 2006. 'Surface radiation measurement data quality assessment at the ARM TWP and NSA sites.' ARM Science Team Meeting.
- WMO. 1996. 'Guide to Meteorological Instruments and Methods of Observation.' WMO-No. 8.
- Younkin, K, and CN Long. 2004. 'Improved Correction of IR Loss in Diffuse Shortwave Measurements: An ARM Value Added Product.' ARM TR-009.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-074.pdf (70 pages, DOE/SC-ARM/TR-074, by C.N. Long, Y. Shi)
- Catalog record: ARM data-source index, `instrument_class_code=qcrad`, read 2026-09-24
- Example file: `sgpqcradbrs1longC1.c1.20260827.000000.nc` from `sgpqcradbrs1longC1.c1`, 0.45 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 70 pages; pages 1-52 and 69-70 were read, and Appendix B's CDL output-field dump was not, so the datastream and quantity lists here are partial
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
