---
name: arm-vap-diffcor
description: ARM Correction of Diffuse Shortwave Measurements (diffcor) - value-added product reference from its technical report. Derived from brs, sirs, skyrad. The retrieval algorithm, reported quantities (Rayleigh limit diffuse SW, PIR Detector Flux), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpbrs1duttC1.c1) and the variable inventory of a real file. Use when working with diffcor data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - diffcor, Correction of Diffuse Shortwave Measurements, sgpbrs1duttC1.c1, brs VAP, sirs VAP, skyrad VAP, Rayleigh limit diffuse SW, Derived Quantities and Models.
---

# DIFFCOR - Correction of Diffuse Shortwave Measurements

The DIFFCORR1DUTT VAP corrects clear-sky diffuse shortwave irradiance measured by shaded Eppley PSP pyranometers at ARM SGP, TWP, and NSA sites for infrared (IR) loss to the sky, using empirically derived relationships with co-located pyrgeometer (PIR) detector flux and case-dome temperature difference data.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 50 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `diffcor` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-009 / K. Younkin, C. N. Long / November 2003](https://www.arm.gov/publications/tech_reports/arm-tr-009.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | `brs`, `sirs`, `skyrad` |
| Record | 1993-09-01 to 2001-06-19 (retired) |
| Datastreams with data | 48 across 3 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/diffcor |


## Credit

Everything this skill knows about the retrieval is the work of **K. Younkin, C. N. Long** -
the ARM developers and mentors who wrote the technical report it derives from:

> K. Younkin, C. N. Long. *Improved Correction of IR Loss in Diffuse Shortwave Measurements: An ARM Value-Added Product*, DOE/SC-ARM/TR-009, November 2003.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-tr-009.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Simple single black detector pyranometers such as the Eppley PSP lose energy via infrared emission to the sky, especially during clear-sky diffuse shortwave measurements, causing an underestimate of diffuse SW. Following Dutton et al. (2001), an empirical relationship is derived at night (when there is no solar input to the pyranometer) between the co-located pyrgeometer detector flux (and optionally the pyrgeometer case-dome temperature difference converted to flux via the Stephan-Boltzman relation) and the pyranometer's nighttime negative offset (IR loss). This relationship, fit separately for two humidity-dependent behavior modes ('dry' and 'moist'), is then applied to correct daytime diffuse SW data, with an additional multiplicative adjustment factor applied to the detector term during daylight to account for under-correction. Two correction forms are produced: a 'Detector Only' correction (one independent variable, the PIR detector flux) and a 'Full' correction (two independent variables, PIR detector flux plus the case-dome temperature flux term), with the Full correction considered the preferred quantity when available.

**Cadence.** input rate 20 second (SIRS a0, SIROS a1, SKYRAD 20s a1 data streams); output every 60 second (1-minute) averaged data used for fitting and correction application; 15-min average data used in some QC figures; averaging 20-second PIR case/dome temperature and detector flux data averaged into 60-second intervals, time-stamped at end of interval, with MISSING (-9999) values excluded; 11-minute running mean/average and running standard deviation used for noise smoothing and QC (e.g., E25 facility) (hb p. 4).

## Inputs

ARM's catalog declares these input instrument classes: `brs`, `sirs`, `skyrad`.

The report names these instruments and sibling products: SIRS, SIROS, BRS (BSRN platform), SKYRAD, MFRSR (Multi-Frequency Rotating Shadowband Radiometer), Eppley 8-48 Black and White pyranometer.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Down-welling Shortwave Diffuse Hemispheric Irradiance... | Wm-2 | - | - | (hb p. 22) |
| Down-welling Shortwave Diffuse Hemispheric Irradiance... | Wm-2 | - | - | (hb p. 24) |
| Down-welling Shortwave Diffuse Hemispheric Irradiance, Best... | Wm-2 | - | - | (hb p. 44) |
| Down-welling Shortwave Hemispheric Irradiance, Sum... | Wm-2 | - | - | (hb p. 44) |
| Rayleigh limit diffuse SW | Wm-2 | - | - | (hb p. 13) |
| PIR Detector Flux | Wm-2 | -300.0 to 0.0 Wm-2 (QC acceptance) | - | (hb p. 7) |
| Down-welling Broadband IR Brightness Temperature (Te) | K | - | - | (hb p. 10) |
| PIR Case Temperature (Tc) | K | - | - | (hb p. 5) |
| PIR Dome Temperature (Td) | K | - | - | (hb p. 5) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Nighttime data window (SGP, mid/lower latitude sites) | 6 hours, 3 hours either side of local midnight (0300-0900 UTC example for SGP) | (hb p. 5) |
| Nighttime data window (NSA site) | cosine of SZA (µ0) less than  -0.2 | (hb p. 5) |
| Case-Dome temperature acceptance range (Detector only fit) | Td greater than = (Tc - 2.0 K) | (hb p. 5) |
| Case-Dome temperature acceptance range (Full correction fit) | (Tc + 0.5 K) greater than = Td greater than = (Tc - 2.0 K) | (hb p. 6) |
| PIR original vs calculated agreement limit | Abs(PIR_orig - PIR_calc) less than = 2.0 Wm-2 | (hb p. 6) |
| PIR Detector Flux min/max limit | -300.0 Wm-2 less than = Df less than = 0.0 Wm-2 | (hb p. 7) |
| IR brightness temp vs ambient air temp limit | Te less than = (Ta + 1.5 K) | (hb p. 7) |
| PIR case temperature running std dev QC limit | Tc_sdev - Tc_avg_sdev less than = 0.1 | (hb p. 7) |
| Moist mode detection (Detector Only method) | (Tc - Te) less than  6.0 K and RH greater than  80% | (hb p. 10) |
| Dry mode detection (Full correction method) | PIR Detector flux less than  -100 Wm-2, ~RH less than  80% | (hb p. 10) |
| Detector Only adjustment factor (dry mode, daylight) | 1.4 | (hb p. 19) |
| Full correction detector-term adjustment factor (dry and... | 2.0 | (hb p. 19) |
| Rayleigh limit test tolerance | +/- 1.0 Wm-2 | (hb p. 27) |
| Corrected minus uncorrected PSP difference limit... | greater than  30.0 Wm-2 | (hb p. 27) |
| Overcast discrimination test | unshaded PSP - shaded PSP greater than  20 Wm-2 indicates not overcast | (hb p. 27) |
| SGP default barometric pressure | 979 mb | (hb p. 16) |
| Stephan-Boltzman constant used | 5.67E-08 W/(m2 K4) | (hb p. 11) |
| PIR Dome Correction Factor C2 (SIRS, SKYRAD) | 4.0 | (hb p. 42) |
| PIR Dome Correction Factor C2 (BRS) | 3.5 | (hb p. 42) |
| PIR Dome Correction Factor C2 (SIROS) | 4.0 (fixed for ALL SIROS PIRs) | (hb p. 40) |


## The data

Verified example: **`sgpbrs1duttC1.c1`**, file `sgpbrs1duttC1.c1.20010119.000000.cdf`
(0.41 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 68 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2001-01-19T00:00:00 to 2001-01-19T23:59:00 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `dsdh_detector_corrected` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `dsdh_full_corrected` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `air_temperature` | K | time | - | Air Temperature |
| `bar_pres` | mb | time | - | Barometric pressure |
| `cos_zenith` | unitles | time | - | Cosine of the Solar Zenith Angle |
| `detector_flux` | W/m^2 | time | - | Detector flux (Downwelling pyrgeometer thermopile voltage * PIR-DIR... |
| `detector_flux_backup` | W/m^2 | time | - | Detector Flux, Backup |
| `down_long_case_temperature` | K | time | - | Downwelling Pyrgeometer Case Thermistor Temperature |
| `down_long_case_temperature_backup` | K | time | - | Downwelling Pyrgeometer Case Thermistor Temperature, Backup |
| `down_long_dome_temperature` | K | time | - | Downwelling Pyrgeometer Dome Thermistor Temperature |
| `down_long_dome_temperature_backup` | K | time | - | Downwelling Pyrgeometer Dome Thermistor Temperature, Backup |
| `down_long_hemisp` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer |
| `down_long_hemisp_backup` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_backup_max` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_backup_min` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_backup_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_max` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_min` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_long_hemisp_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_short_diffuse_hemisp_uncorrected` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance Uncorrected,... |
| `down_short_diffuse_hemisp_uncorrected_max` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance Uncorrected,... |
| `down_short_diffuse_hemisp_uncorrected_min` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance Uncorrected,... |
| `down_short_diffuse_hemisp_uncorrected_std` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance Uncorrected,... |
| `down_short_hemisp_sum` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Calculated, Sum of... |
| `down_short_hemisp_uncorrected` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_short_hemisp_uncorrected_max` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_short_hemisp_uncorrected_min` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `down_short_hemisp_uncorrected_std` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `dsdh_best_estimate` | W/m^2 | time | - | Downwelling Shortwave Hemispheric Irradiance, Ventilated Pyrgeometer,... |
| `dsdh_detector_corrected_mode` | unitles | time | - | Detector only correction mode for Downwelling Shortwave Hemispheric... |


_30 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpbrs1duttC1.c1",
                             "start": "2001-01-19", "end": "2001-01-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpbrs1duttC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpbrs1duttC1.c1", "2001-01-19", "2001-01-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpbrs1duttC1.c1", "2001-01-19", "2001-01-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("down_short_hemisp_sum")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 68 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpbrs1duttC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["dsdh_full_corrected", "dsdh_detector_corrected", "qc_dsdh_full_corrected", "qc_dsdh_detector_corrected"],
                                cleanup_qc=True)
```

## Quality control in this product

4 `qc_` companion variables cover 2 of the
68 data variables. Assessments present in the example file: .

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_dsdh_full_corrected"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("dsdh_full_corrected", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["dsdh_full_corrected", "dsdh_detector_corrected"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpbrs1duttC1.c1", "19930901", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The VAP applies a tiered QC flag system (Table 1: GOOD/MISSING/BAD/QUESTIONABLE, bitwise flags 0-16384) separately for Detector-only and Full corrected diffuse SW, covering: missing shortwave diffuse; PIR original-vs-calculated mismatch (greater than 2.0 Wm-2); case-dome temperature relationship violations; IR brightness vs ambient air temperature violations; corrected value vs Rayleigh limit comparison; corrected-minus-uncorrected magnitude check (greater than 30 Wm-2); PIR case temperature running standard deviation noise test; and PIR detector flux range check. 'Bad' data have corrected...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Bimodal 'dry' vs 'moist' behavior between pyrgeometer detector flux and pyranometer... | Scatter of nighttime PSP offset vs PIR detector flux shows two distinct linear trends rather than one; aggregate single fit does not pass through (0,0) although each separated mode does | Separate data into dry/moist modes using RHgreater than 80% and case-temperature-minus-sky-brightness-temperature (less than 6K) criteria for... | (hb p. 8) |
| Daytime under-correction relative to nighttime-derived fit | Corrected diffuse SW still shows ~4 Wm-2 average residual under-correction versus co-located Eppley 8-48 B&W during daylight when only night-derived bi-modal coefficients are applied | Apply daylight adjustment factors to the detector portion of correction: 1.4 for Detector Only (dry mode only), 2.0 for detector part of Full... | (hb p. 18) |
| Sub-Rayleigh diffuse SW values (physically impossible, uncorrected data) | 8.3% of daylight (SZAless than 80) uncorrected shaded PSP data exhibit diffuse SW below the theoretical Rayleigh limit (2.6% under confirmed clear sky after excluding thick-overcast cases) | Apply Detector-Only or Full IR loss correction, which eliminates sub-Rayleigh behavior under clear skies; if still below Rayleigh limit after... | (hb p. 15) |
| Noisy PIR case/dome thermistor data (MFRSR-logger 'bug'), notably at SIROS/SGP facility... | Rapid, unphysical fluctuations in PIR case and dome temperature time series (visible against smooth co-located ambient air temperature) causing large excursions in calculated longwave... | Apply 11-minute running mean smoothing to noisy input variables (E25); use 11-minute running standard deviation test (Tc_sdev - Tc_avg_sdev less than... | (hb p. 28) |
| PIR case temperature theoretically should be greater than = dome temperature; violations... | Case-minus-dome temperature difference outside expected ranges, e.g. dome exceeding case by more than 0.5K (BAD) or case exceeding dome by more than 2.0K (BAD, 'beyond clear-sky loss'),... | Apply tiered QC flags (GOOD/QUESTIONABLE/BAD) per defined temperature-difference thresholds; set corrected value to -9999 when BAD | (hb p. 24) |
| IR brightness temperature exceeding ambient air temperature beyond uncertainty range | Te greater than  Ta + 1.5K, indicating erroneous data such as thermal shock from rainfall or instrument malfunction | Reject/flag as BAD when Te greater than  Ta+1.5K; flag as QUESTIONABLE when Te far below Ta (greater than 25K difference, up to 50K allowed);... | (hb p. 25) |
| Gross calibration/processing errors in PIR longwave irradiance | Difference between calculated PIR (from a0 20-sec detector data) and original PIR (from a1/b1 60-sec stream) exceeds 2.0 Wm-2 | Reject sample from both fitting and correction application when difference exceeds limit; note this check cannot be applied to SIROS (missing a0... | (hb p. 6) |
| PIR Detector Flux out-of-range values | Calculated detector flux falls outside -300 to 0 Wm-2 range, indicating PIR instrument or datalogger problem; typical good-data maximum magnitude is only about 150 Wm-2 at SGP | Flag data as BAD and set Detector-only and Full corrected PSP outputs to -9999 | (hb p. 31) |
| Missing collocated meteorological (SMOS/EBBR/SMET) data at some facilities | Ambient air temperature, RH, wind, vapor pressure, precipitation fields set to MISSING (-9999) at SGP facilities E10 and E16, which lack collocated SMOS or EBBR instruments; barometric... | Substitute PIR case temperature for ambient air temperature in QC checks; use barometric pressure from closest facility; use site default barometric... | (hb p. 16) |
| TWP site lacks detectable 'dry mode' nighttime data | Ambient RH at TWP remains above the 80% dry/moist threshold year-round during the correction period, so no dry-mode Full-correction coefficients can be fit | Use moist-mode Full correction coefficients to correct all TWP diffuse SW data; note tropical atmosphere IR loss is inherently minimal | (hb p. 11) |
| SIROS instrument lacks a0 thermopile voltage data | PIR detector flux for SIROS must be back-calculated as a residual from downwelling LW minus case/case-dome terms rather than directly from thermopile voltage; certain QC checks... | Compute detector flux via residual formula (Appendix C) using fixed PIR Dome Correction Factor C2=4.0; skip PIR original-vs-calculated QC check for... | (hb p. 6) |
| Method applicability limited to specific instrument configuration | Correction coefficients and QC limits derived only for ventilated, shaded Eppley PSP/PIR pairs; would not directly transfer to unventilated or unshaded configurations or other instrument... | Caution stated that results do not necessarily apply outside this configuration | (hb p. 4) |
| Rayleigh-limit polynomial fit residual error | 5th-order polynomial fit to SBDART Rayleigh model shows worst-case disagreement (at SZA=70°, typical SGP pressure range 980-1000mb) of just under 0.5 Wm-2 versus full model | Used only as an approximation for QC comparison; fit coefficients tabulated per site (Appendix G) | (hb p. 14) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `brs`: load `arm-instrument-brs` for its handbook facts and artifacts
- input instrument `sirs`: load `arm-instrument-sirs` for its handbook facts and artifacts
- input instrument `skyrad`: load `arm-instrument-skyrad` for its handbook facts and artifacts

### References the report cites

- Dutton, E. G., et al., 2001: Measurement of broadband diffuse solar irradiance using current commercial instrumentation with a correction for thermal offset errors. J. Atmos. and Ocean. Tech., 18(3), 297-314.
- Long, C. N., K. Younkin, and D. M. Powell, 2001: Analysis of the Dutton et al. IR loss correction technique applied to ARM diffuse SW measurements. ARM Science Team Meeting Proceedings, ARM-CONF-2001.
- Long, C. N., K. L. Gaustad, K. Younkin, and J. A. Augustine, 2003: An improved daylight correction for IR loss in ARM diffuse SW measurements. ARM Science Team Meeting Proceedings, ARM-CONF-2003.
- Philipona, R., 2002: Underestimation of solar global and diffuse radiation measured at Earth's surface. J. Geophys. Res., 107(D22), 4654.
- Michalsky, J. J., et al., 2002: Comparison of diffuse shortwave irradiance measurements. ARM Science Team Meeting Proceedings, ARM-CONF-2002.
- Younkin, K., and C. N. Long, 2002: Results of the Dutton et al. IR loss correction VAP: Statistical Analysis of Corrected and Uncorrected SW Measurements. ARM Science Team Meeting Proceedings, ARM-CONF-2002.
- Cess, R. D., T. T. Qian, and M. G. Sun, 2000: Consistency tests applied to the measurement of total, direct, and diffuse shortwave radiation at the surface. J. Geophys. Res., 105(D20), 24,881-24,887.
- Nels Larson, 1992: Solarposition: Integer function for calculating the position of the Sun as seen from a place on Earth at a specific time, Pacific Northwest Laboratory.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-tr-009.pdf (50 pages, DOE/SC-ARM/TR-009, by K. Younkin, C. N. Long)
- Catalog record: ARM data-source index, `instrument_class_code=diffcor`, read 2026-09-24
- Example file: `sgpbrs1duttC1.c1.20010119.000000.cdf` from `sgpbrs1duttC1.c1`, 0.41 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
