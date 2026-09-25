---
name: arm-instrument-pgsiso
description: ARM Precision Gas System Isotope Analyzer (pgsiso) - handbook-derived instrument reference. Measurement principle, reported quantities (CO2, 12CO2, 13CO2, delta13C, delta18O, CH4, CO, N2O), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgppgsisocoeffC1.b1) and the variable inventory of a real file. Use when working with pgsiso data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Carbon. Triggers - pgsiso, Precision Gas System Isotope Analyzer, sgppgsisocoeffC1.b1, CO2, 12CO2, 13CO2, delta13C, delta18O, CH4, Atmospheric Carbon, Spectronus FTIR spectrometer, developed by the Centre for Atmospheric Chemistry, ASCII, FTIR, HITRAN, MALT.
---

# PGSISO - Precision Gas System Isotope Analyzer

The PGSISO is a Spectronus FTIR-based trace gas analyzer that continuously measures CO2, 12CO2, 13CO2 (delta13C), delta18O, CH4, CO, and N2O in air sampled sequentially from four tower inlet heights and five calibration cylinders at an ARM tower observatory (SGP and, upcoming, BNF).

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `pgsiso` |
| Handbook | [DOE/SC-ARM-TR-237 / S Biraud, K Reichl / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-237.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Spectronus FTIR spectrometer, developed by the Centre for Atmospheric Chemistry, University of Wollongong, Australia, manufactured by Ecotech Pty Ltd (Melbourne, Australia); FTIR spectrometer... |
| Primary measurements | Carbon dioxide (CO2) concentration; Carbon monoxide (CO) Concentration; Isotope ratio; Methane concentration; Nitrogen oxides |
| Record | 2013-08-01 to 2026-09-23 (active) |
| Datastreams with data | 8 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pgsiso |


## Credit

Everything this skill knows about the instrument is the work of **S Biraud, K Reichl** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Biraud, K Reichl. *Precision Gas System Isotope Analyzer (PGSISO) Instrument Handbook*, DOE/SC-ARM-TR-237, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-237.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The Spectronus FTIR trace gas analyzer determines simultaneous concentrations of trace gases by collecting and analyzing the Fourier Transform Infrared spectrum of a closed-path sample cell (a 24-meter multi-pass gas cell coupled to a Bruker IR cube with thermoelectrically cooled MCT detector, wavenumber range 1500-7800 cm-1) through which the gas sample is multi-passed by the IR beam. A computational approach (the MALT program, Multiple Atmospheric Layer Transmission) best-fits selected regions of the measured spectrum with a calculated spectrum based on sample conditions (pressure, temperature, pathlength), the HITRAN spectral line database, and a model of the FTIR instrument line shape, iteratively adjusting trace gas concentrations and instrument parameters to achieve best fit. For CH4, CO, N2O, and CO2 combination bands near 3600 cm-1, the low-resolution spectrometer does not resolve individual isotopologues and fits whole absorption bands assuming natural isotopic abundance, while for 12CO2 and 13CO2 in the nu3 bands near 2300 cm-1, individual isotopologue concentrations are determined independently, enabling calculation of isotopic ratios. MALT retrieves the concentration of each target gas from each spectrum and converts to a mole-fraction scale using measured total pressure and temperature of the sample.

**Siting.** Four tower sample inlet channels correspond to four tower sample heights, sequentially selected via a Valco multi-port valve along with five calibration cylinders. Tower sample data correspond to VALCOPOSITION variable equal to integers 1, 2, 3, or 4 for the four tower sample heights respectively.

**Sampling.** averaging Four span cylinders measured about every seven days; one Target cylinder measured at the same pace, another Target once per day; four tower sample inlet channels sequentially selected via Valco multi-port valve (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| CO2 | ppm | - | MEAN -0.1, STDERR 0.0, RMSE 0.2 (Target... | - | (hb p. 6) |
| 12CO2 (16O12C16O) | - | - | - | - | (hb p. 6) |
| 13CO2 (16O13C16O) | - | - | - | - | (hb p. 6) |
| delta13C | ‰ (VPDB scale) | - | MEAN 0.1, STDERR 0.0, RMSE 0.2 (N=1350) | - | (hb p. 6) |
| delta18O | ‰ (VPDB scale) | - | MEAN -0.1, STDERR 0.0, RMSE 0.5 (N=1404) | - | (hb p. 6) |
| CH4 | ppb | - | MEAN -0.1, STDERR 0.0, RMSE 0.3 (N=1329) | - | (hb p. 6) |
| CO | ppb | - | MEAN 1.3, STDERR 0.0, RMSE 1.6 (N=1325) | - | (hb p. 6) |
| N2O | ppb | - | MEAN 0.1, STDERR 0.0, RMSE 0.2 (N=712) | - | (hb p. 6) |
| H2O | - | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavenumber range (MCT detector) | 1500-7800 cm-1 | (hb p. 7) |
| Multi-pass gas cell pathlength | 24-meter | (hb p. 7) |
| Digital I/O switching | 12-channel digital input/output (I/O) switching capability for 12 (or optionally more) solenoid valves | (hb p. 6) |
| Analogue-digital converter | 8-channel analogue-digital converter for logging environmental variables (temperatures, pressures, flows) | (hb p. 6) |
| Number of tower sample inlet channels | four (for four tower sample heights) | (hb p. 6) |
| Number of calibration cylinders | five | (hb p. 6) |
| Reference cross-sensitivity conditions | Q0 = 0 ppm (H2O); P0 = 1100 mbar (cell pressure); T0 = 35 C (cell temperature); F0 = 1 LPM (cavity sample flow); C0 = 400 ppm (CO2) | (hb p. 10) |
| 13rref | 0.111802 (abundance ratio of 16O13C16O to 16O12C16O) | (hb p. 11) |
| 18rref | 0.00208835 (abundance ratio of 18O12C16O to 16O12C16O) | (hb p. 11) |
| 17rref | 0.0003931 (abundance ratio of 17O12C16O to 16O12C16O) | (hb p. 11) |
| x626 | 0.984054 (abundance of 16O12C16O in reference to VPDB) | (hb p. 11) |
| CO2 calibration scale (as of July 2018) | WMO-CO2-X2019 | (hb p. 10) |
| CH4 calibration scale (as of July 2018) | WMO-CH4-X2004A | (hb p. 10) |
| CO calibration scale (as of July 2018) | WMO-CO-X2014A | (hb p. 10) |
| N2O calibration scale (as of July 2018) | WMO-N2O-X2006A | (hb p. 10) |


## The data

Verified example: **`sgppgsisocoeffC1.b1`**, file `sgppgsisocoeffC1.b1.20230419.120420.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1, `bound`=2 |
| Data variables | 48 |
| QC variables | 14 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2023-04-19T12:04:20 to 2023-04-19T12:04:20 |
| dod version | pgsisocoeff-b1-1.4 |
| process version | ingest-pgsisoavg-2.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ch4_gain` | 1 | time | yes | Methane gain coefficient |
| `ch4_offset` | ppb | time | yes | Methane offset coefficient |
| `co2_12_gain` | 1 | time | yes | 12CO2 gain coefficient |
| `co2_12_offset` | ppm | time | yes | 12CO2 offset coefficient |
| `co2_13_gain` | 1 | time | yes | 13CO2 gain coefficient |
| `co2_13_offset` | ppm | time | yes | 13CO2 offset coefficient |
| `co2_18_gain` | 1 | time | yes | 18O12C16O gain coefficient |
| `co2_18_offset` | ppm | time | yes | 18O12C16O offset coefficient |
| `co2_gain` | 1 | time | yes | Carbon dioxide gain coefficient |
| `co2_offset` | ppm | time | yes | Carbon dioxide offset coefficient |
| `co_gain` | 1 | time | yes | CO gain coefficient |
| `co_offset` | ppb | time | yes | CO offset coefficient |
| `n2o_gain` | 1 | time | yes | N2O gain coefficient |
| `n2o_offset` | ppb | time | yes | N2O offset coefficient |
| `ch4_gain_err` | 1 | time | - | Methane gain coefficient error |
| `ch4_offset_err` | ppb | time | - | Methane offset coefficient error |
| `co2_12_gain_err` | 1 | time | - | 12CO2 gain coefficient error |
| `co2_12_offset_err` | ppm | time | - | 12CO2 offset coefficient error |
| `co2_13_gain_err` | 1 | time | - | 13CO2 gain coefficient error |
| `co2_13_offset_err` | ppm | time | - | 13CO2 offset coefficient error |
| `co2_18_gain_err` | 1 | time | - | 18O12C16O gain coefficient error |
| `co2_18_offset_err` | ppm | time | - | 18O12C16O offset coefficient error |
| `co2_gain_err` | 1 | time | - | Carbon dioxide gain coefficient error |
| `co2_offset_err` | ppm | time | - | Carbon dioxide offset coefficient error |
| `co_gain_err` | 1 | time | - | CO gain coefficient error |
| `co_offset_err` | ppb | time | - | CO offset coefficient error |
| `n2o_gain_err` | 1 | time | - | N2O gain coefficient error |
| `n2o_offset_err` | ppb | time | - | N2O offset coefficient error |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "sgppgsisocoeffC1.b1",
                             "start": "2023-04-19", "end": "2023-04-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgppgsisocoeffC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgppgsisocoeffC1.b1", "2023-04-19", "2023-04-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgppgsisocoeffC1.b1", "2023-04-19", "2023-04-19"))   # cite what you pulled
```
### First look

Discrete samples rather than a continuous record, so markers.

```python
import matplotlib.pyplot as plt

# Discrete samples, not a continuous record - a line plot of one or a few points
# is meaningless (and ACT's TimeSeriesDisplay raises IndexError on a length-1
# series), so plot the samples as markers.
fig, ax = plt.subplots(figsize=(9, 3.5))
ax.plot(ds["time"], ds["ch4_gain"], marker="o", linestyle="none")
ax.set_ylabel("ch4_gain")
fig.autofmt_xdate()
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```

## Quality control in this datastream

14 `qc_` companion variables cover 14 of the
48 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_co2_gain"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("co2_gain", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["co2_gain", "co2_offset", "co2_12_gain"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgppgsisocoeffC1.b1", "20130801", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: QC variables use a bit-flag method (flag_method = "bit") with 11 defined bits covering: missing value (-9999), value below/above valid_min/valid_max, missing slope or slope_err values, slope out of valid range, slope significantly nonzero, auxiliary variable QC not zero, insufficient residual correction following certain tanks, and N2 Purge Tank measurements. "Best data" are those with *_QC values of 0 for tower sample or Target measurements. Tower sample data correspond to VALCOPOSITION equal to 1, 2, 3, or 4 for the four tower sample heights. Not all Target cylinder measurements are used...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| H2O vapor displacement effect on measured concentrations | Measured species concentrations shift systematically depending on coincident H2O concentration if not corrected | Apply H2O correction: chi' = chi / (1 - q/10^6) for all species prior to further corrections | (hb p. 9) |
| Residual air carryover from previous sample measurement | Measured concentration biased toward previous sample's value, especially for tower/target inlets not fully flushed; varies by deployment period (Aug 2013-Sep2015, Sep2015-Jan2017) | Apply residual correction using Presid formulas specific to time period and inlet type; no correction needed Jan 2017-present or for BNF deployment | (hb p. 9) |
| Cross-sensitivity of spectral fit to H2O, pressure, temperature, flow, and CO2... | Small systematic dependence of apparent (raw) mole fractions on Q (H2O), P (cell pressure), T (cell temperature), F (flow), C (CO2 concentration) even after MALT fit | Apply cross-sensitivity correction subtracting coefficient-weighted deviations from reference conditions (Q0=0 ppm, P0=1100 mbar, T0=35C, F0=1 LPM,... | (hb p. 10) |
| Raw FTIR/HITRAN scale offset from standard reference scales | Raw retrieved mole fractions differ from established standard reference scales by up to a few percent due to HITRAN parameter accuracy, MALT model, optical pathlength, T, P uncertainties | Rescale via calibration coefficients and CO2 isotope rescaling from HITRAN to VPDB scale | (hb p. 7) |
| Instrument instability periods affecting Target/calibration measurements | Abnormally high or variable H2O measurements; calibration coefficient outliers or periods of systematic deviation from expected values | Periods are identified via mentor-compiled DQR csv configuration file and excluded from residual statistics; coefficients set to missing value and... | (hb p. 8) |
| Insufficient residual correction after certain tank measurements | QC bit 10 flagged when measurement follows a tank for which residual correction is not sufficient | Flagged via bit_10 in QC variable; users should treat flagged data with caution | (hb p. 9) |
| N2 purge tank measurements included in stream | QC bit 11 set for measurements of N2 Purge Tank, which are not atmospheric samples | Flagged via bit_11 in QC variable; exclude from atmospheric analysis | (hb p. 9) |
| Calibration coefficient dependency on auxiliary variable QC | QC bit 9 set when QC state for at least one mentor-defined auxiliary variable is not equal to 0, indicating coefficient may be unreliable | Flagged via bit_9 | (hb p. 9) |
| Slope-based QC flags for calibration coefficients out of range or significant nonzero... | Bits 4-8 flag missing slope/slope_err values, slope below/above valid_min/max, or slope significantly different from zero | Flagged via bits 4 through 8 in QC variable | (hb p. 9) |
| Missing value and out-of-range flags | Value equals missing_value -9999, or less than valid_min, or greater than valid_max | Flagged via bits 1, 2, 3 respectively; best data are those with *_QC = 0 | (hb p. 9) |
| Low-resolution FTIR cannot resolve individual isotopologues for CH4, CO, N2O, CO2... | Whole absorption bands fitted assuming natural isotopic abundance; isotopic information unavailable for these species/bands | Natural variations in isotopic abundance assumed not to significantly affect these FTIR measurements | (hb p. 7) |
| Calibration regime changes over deployment history affect data continuity | Discontinuities or different calibration precision/uncertainty across time segments: 3-point linear (Aug2013-Sep2015), 4-point linear (Sep2015-Apr2023), 5-point quadratic (Jan2024-present) | Users should be aware which calibration regime applies to their data period | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Measurement of four span cylinders about every seven days and one Target cylinder at the same pace, another Target once per day; linearly (or quadratically, from Jan 2024) interpolated gain and offset coefficients applied to sample data. Regimes: Aug 2013-Sep2015 3-point linear; Sep2015-Apr2023 4-point linear;... (hb p. 8) |
| Calibration interval | Span cylinders about every 7 days; Target cylinder about every 7 days and also once per day; calibration tank values updated about once every five years when tanks are changed out (hb p. 8) |
| Traceability | Calibration tank values provided by the World Meteorological Organization (WMO) Central Calibration Laboratory (CCL) at NOAA's Earth System Research Laboratory, using WMO CCL scales (e.g., WMO-CO2-X2019, WMO-CH4-X2004A, WMO-CO-X2014A, WMO-N2O-X2006A as of July 2018) (hb p. 8) |
| Routine maintenance | Calibration tank values are transcribed to a machine-readable configuration file updated by the mentor each time the calibration tanks are changed out (hb p. 14) |
| Maintenance interval | about once every five years (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `BNF` | Bankhead National Forest |
| `CCL` | Central Calibration Laboratory |
| `DOE` | U.S. Department of Energy |
| `DQR` | Data Quality Report |
| `FTIR` | Fourier Transform Infrared |
| `HITRAN` | high-resolution transmission molecular absorption line parameters database |
| `I/O` | input/output |
| `IR` | infrared |
| `LPM` | liters per minute |
| `MALT` | Multiple Atmospheric Layer Transmission |
| `MCT` | mercury-cadmium-telluride |
| `NOAA` | National Oceanic and Atmospheric Administration |


### References the handbook cites

- Griffith, DWT. 1996. "Synthetic calibration and quantitative analysis of gas-phase FT-IR spectra." Applied Spectroscopy 50(1): 59-70
- Griffith, DWT, NM Deutscher, G Kettlewell, M Riggenbach, C Caldow, and S Hammer. 2012. "A Fourier transform Infrared trace gas analyser for atmospheric applications." Atmospheric Measurement Techniques 5(10): 2481-2498
- Griffith, DWT. 2018. "Calibration of isotopologue-specific optical trace gas analyzers: a practical guide." Atmospheric Measurement Techniques 11(11): 6189-6201
- Rothman, LS, et al. 2005. "The HITRAN 2004 molecular spectroscopic database." Journal of Quantitative Spectroscopy and Radiative Transfer 96(2): 139-204
- Rothman, LS, et al. 2009. "The HITRAN 2008 molecular spectroscopic database." Journal of Quantitative Spectroscopy and Radiative Transfer 110(9-10): 533-572
- Smith, TEL, MJ Wooster, M Tattaris, and DWT Griffith. 2011. "Absolute accuracy and sensitivity analysis of OP-FTIR retrievals of CO2, CH4 and CO..." Atmospheric Measurement Techniques 4(1): 97-116
- World Meteorological Organization (WMO). 2014. "GAW Report No. 213."

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-237.pdf (17 pages, DOE/SC-ARM-TR-237, by S Biraud, K Reichl)
- Catalog record: ARM data-source index, `instrument_class_code=pgsiso`, read 2026-09-23
- Example file: `sgppgsisocoeffC1.b1.20230419.120420.nc` from `sgppgsisocoeffC1.b1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
