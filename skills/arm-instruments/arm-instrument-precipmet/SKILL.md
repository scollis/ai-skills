---
name: arm-instrument-precipmet
description: ARM Precipitation Meteorological Instruments (precipmet) - handbook-derived instrument reference: measurement principle, reported quantities (Air temperature, Relative humidity, Atmospheric pressure, Wind speed, arithmetic mean, Wind speed, vector mean, Wind direction, vector mean, WXT mean precipitation rate, WXT cumulative precipitation), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpprecipmetI9.b1) and the variable inventory of a real file. Use when working with precipmet data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface Meteorology. Triggers - precipmet, Precipitation Meteorological Instruments, sgpprecipmetI9.b1, Air temperature, Relative humidity, Atmospheric pressure, Wind speed, arithmetic mean, Wind speed, vector mean, Wind direction, vector mean, Surface Meteorology, Vaisala WXT520 weather transmitter, Novalynx 260-2500E-12 tipping bucket rain gauge, DQAR, PARS2, PRECIPMET, TBRG.
---

# PRECIPMET - Precipitation Meteorological Instruments

The PRECIPMET system measures ambient temperature, relative humidity, pressure, wind speed/direction, and precipitation (via an acoustic sensor and a tipping bucket rain gauge) as reference data for co-located precipitation network instruments (PARS2 laser disdrometer and RWP radar wind profiler) at ARM SGP intermediate facilities.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `precipmet` |
| Handbook | [DOE/SC-ARM-TR-226 / J Kyrouac / September 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-226.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala WXT520 weather transmitter; Novalynx 260-2500E-12 tipping bucket rain gauge; Campbell Scientific CR1000 data logger |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation |
| Record | 2017-03-30 to 2023-09-29 (retired) |
| Datastreams with data | 3 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/precipmet |


## Credit

Everything this skill knows about the instrument is the work of **J Kyrouac** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Kyrouac. *Precipitation Meteorological Instruments (PRECIPMET) Handbook*, DOE/SC-ARM-TR-226, September 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-226.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Pressure, temperature, and relative humidity are measured by a pan and tilt unit (PTU) module containing Vaisala proprietary capacitive sensors (capacitive silicon for pressure, capacitive ceramic for temperature, capacitive thin film polymer for humidity), based on an advanced resistor-capacitor (RC) oscillator that continuously measures the capacitance of two reference capacitors, with temperature dependency corrected in the microprocessor. Wind speed and direction are measured using equally spaced ultrasonic transducers in the same horizontal plane, computing transit time differences between transducers via Vw = 0.5 x L x (1/tf - 1/tr). The WXT520 precipitation sensor uses a steel cover and piezoelectric sensor to detect precipitation impact proportional to drop volume, translating impact energy into rain amount, with filtering to eliminate non-precipitation noise; it operates in time mode with messages sent at 1-minute intervals. The tipping bucket rain gauge uses a 12-inch diameter catchment funnel directing precipitation into a tipping mechanism that tips once filled with 0.254 mm of precipitation, recorded via a magnetic reed switch pulse, with a thermostatic heater to melt frozen precipitation.

**Siting.** The WXT520 is mounted on top of the control building at a height of approximately 4 meters; due to site limitations, the mounting does not necessarily adhere to manufacturer installation recommendations, but effects are considered negligible since data are used as reference for similarly mounted instrumentation. The tipping bucket rain gauge is installed at the north-western corner of each IF to minimize physical interference from surrounding structures and situate it on the side of prevailing winds, mounted within the chain link security fencing on a pole at approximately 2 meters so the top of the gauge funnel is level with the top rail of the fencing.

**Sampling.** reported every 1-minute intervals; averaging WXT precipitation intensity is a running one minute average in 10s steps (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Air temperature | °C | - | ± 0.3°C at 20°C (see manual for extended... | - | (hb p. 8) |
| Relative humidity | % | - | ± 3% (from 0% to 90%); ± 5% (from 90% to 100%) | - | (hb p. 8) |
| Atmospheric pressure | kPa | - | ± 0.05 kPa from 0°C to 30°C | - | (hb p. 8) |
| Wind speed, arithmetic mean | m/s | - | ± 3% at 10 m/s | - | (hb p. 8) |
| Wind speed, vector mean | m/s | - | ± 3% at 10 m/s | - | (hb p. 9) |
| Wind direction, vector mean | degree | - | ± 3° | - | (hb p. 9) |
| WXT mean precipitation rate | mm/hr | - | ± 5% (not including errors induced by wind) | - | (hb p. 9) |
| WXT cumulative precipitation | mm | - | ± 5% (not including errors induced by wind) | - | (hb p. 9) |
| Tipping bucket rain gauge (TBRG) precipitation total | mm | - | ± 1% at 1 to 3 in/hr; ± 3% at 0 to 6 in/hr | - | (hb p. 9) |
| TBRG precipitation total, corrected | mm | - | Undefined; lab-measured correction | - | (hb p. 9) |
| Temperature standard deviation | °C | - | - | - | (hb p. 9) |
| Relative humidity standard deviation | % | - | - | - | (hb p. 9) |
| Wind direction, vector mean standard deviation | degrees | - | - | - | (hb p. 9) |
| Logger voltage | V | - | - | - | (hb p. 9) |
| Logger temperature | °C | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Temperature Range (operation) | -52°C to 60°C | (hb p. 13) |
| Temperature Range (storage) | -60°C to 70°C | (hb p. 13) |
| Temperature Resolution | 0.1°C | (hb p. 13) |
| Relative humidity Range | 0% to 100% | (hb p. 13) |
| Relative humidity Resolution | 0.1 % | (hb p. 13) |
| Pressure Range | 600 hPa to 1100 hPa | (hb p. 13) |
| Pressure Resolution | 0.1 hPa | (hb p. 13) |
| Wind speed Range | 0 m/s to 60 m/s | (hb p. 13) |
| Wind speed Resolution | 0.1 m/s | (hb p. 13) |
| Wind speed Response time | 0.25 s | (hb p. 13) |
| Wind direction Range | 0° to 360° | (hb p. 13) |
| Wind direction Resolution | 1° | (hb p. 13) |
| Wind direction Response time | 0.25 s | (hb p. 13) |
| Precipitation accumulation Collection area | 60 cm2 | (hb p. 13) |
| Precipitation accumulation Resolution | 0.01 mm | (hb p. 13) |
| Precipitation intensity Range | 0 to 200 mm/hr | (hb p. 13) |
| Precipitation intensity Response time | running one min average in 10s steps | (hb p. 13) |
| Tipping Bucket Collection diameter | 12 inches | (hb p. 13) |
| Tipping Bucket Calibration | 1 tip = 0.01 inch of precipitation | (hb p. 13) |


## The data

Verified example: **`sgpprecipmetI9.b1`**, file `sgpprecipmetI9.b1.20230926.000100.nc`
(0.2 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1416, `bound`=2 |
| Data variables | 32 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2023-09-26T00:01:00 to 2023-09-26T23:59:00 |
| dod version | precipmet-b1-1.1 |
| process version | ingest-precipmet-1.1-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `atmos_pressure` | kPa | time | yes | Atmospheric pressure |
| `logger_temp` | degC | time | yes | Logger temperature |
| `logger_volt` | V | time | yes | Logger voltage |
| `rh_mean` | % | time | yes | Relative humidity mean |
| `tbrg_precip_total` | mm | time | yes | TBRG precipitation total |
| `temp_mean` | degC | time | yes | Temperature mean |
| `wdir_vec_mean` | degree | time | yes | Wind direction vector mean |
| `wspd_arith_mean` | m/s | time | yes | Wind speed arithmetic mean |
| `wspd_vec_mean` | m/s | time | yes | Wind speed vector mean |
| `wxt_cumul_precip` | mm | time | yes | WXT cumulative precipitation |
| `wxt_precip_rate_mean` | mm/hr | time | yes | WXT mean precipitation rate |
| `rh_std` | % | time | - | Relative humidity standard deviation |
| `tbrg_precip_total_corr` | mm | time | - | TBRG precipitation total, corrected |
| `temp_std` | degC | time | - | Temperature standard deviation |
| `time` | - | time | - | Time offset from midnight |
| `wdir_vec_std` | degree | time | - | Wind direction vector mean standard deviation |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpprecipmetI9.b1", "2023-09-26", "2023-09-26")
ds = armlive_open("sgpprecipmetI9.b1", "2023-09-26", "2023-09-26", cleanup_qc=True)
```

## Quality control in this datastream

11 `qc_` companion variables cover 11 of the
32 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpprecipmetI9.b1", "20170330", "20260923")
```

The handbook's own note on data quality: All variables are level b1 with quality flags applied. Each primary variable has a corresponding qc_ variable containing a bit-packed representation of true/false QC test results; a QC value of zero means no tests failed. Bit tests check for missing_value (Bad), less than valid_min (Bad), greater than valid_max (Bad), and difference between current and previous values exceeding valid_delta (Indeterminate). Table 4 lists minimum, maximum, and delta limits for each qc_ variable. The instrument mentor performs routine data checks and files Data Quality Reports (DQR) when problems are found. The...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Wind measurement dropout during snow | Wind speed/direction data occasionally drop out or show gaps during periods of snow | None stated beyond noting cause is transducer blockage | (hb p. 5) |
| Under-reporting of light rain by WXT520 acoustic sensor | WXT precipitation values read lower than nearby precipitation instruments during light rain events | Manufacturer confirms cause is sensor mechanics (precipitation must fall at terminal velocity to register); tipping bucket rain gauge recommended as... | (hb p. 5) |
| WXT520 acoustic precipitation measurement unreliable in light precipitation | Discrepancy between wxt520_precip_rate_mean/cumul_precip and tbrg_precip_total during light precipitation events | Use TBRG data as most reliable precipitation measurement | (hb p. 5) |
| TBRG underestimation of precipitation at high rain rates | tbrg_precip_total reads low compared to actual precipitation during high-intensity rain | Annual laboratory dynamic calibration produces a second-order polynomial correction applied to raw data, stored in tbrg_precip_total_corr | (hb p. 9) |
| Non-ideal/limited siting of instruments | Data may not represent true ambient surface meteorological conditions typical of standard MET siting standards | None; user should note PRECIPMET not intended as substitute for MET datastream | (hb p. 11) |
| Not research-grade / larger uncertainties than standard MET instrumentation | Larger stated uncertainties in temperature, RH, pressure, wind vs. dedicated MET systems | Data intended only as supplemental/reference data for precipitation network instruments (PARS2, RWP), not for surface meteorological studies | (hb p. 9) |
| Non-adherence to manufacturer installation recommendations for WXT520 mount | Possible minor deviations in wind/temperature/pressure readings due to non-standard mounting height/location on control building roof | Effects considered negligible since data are reference-only for similarly mounted precipitation instruments | (hb p. 6) |
| QC delta test failures (rate-of-change exceedance) | qc_ variables flagged 'Indeterminate' when difference between current and previous values exceeds valid_delta (e.g., temp_mean change greater than 20°C, rh_mean change greater than 30%,... | Flag is bit-packed into qc_ variable; assessed as Indeterminate rather than Bad | (hb p. 10) |
| Missing, below valid_min, or above valid_max values | qc_ variable bit 1/2/3 set when value equals missing_value, is less than valid_min, or greater than valid_max; assessed as Bad | Documented via bit-packed QC flag in file header metadata | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | WXT520: wind data verified to read zero via bag placed over ultrasonic transducers, and PTU module replaced. TBRG: known amount of water (500 mL) passed through gauge and tip count checked/adjusted (static calibration); annual lab-driven dynamic calibration compares pump output to gauge output at known target... (hb p. 9) |
| Calibration interval | WXT520: annual (PTU module replacement); TBRG static calibration: twice a year (every 6 months); TBRG dynamic calibration: once annually (hb p. 9) |
| Routine maintenance | Preventative visual checks of the instrument and live data are performed daily; if a problem is noted, steps are taken to correct the issue and maintenance is documented using internal reporting forms. If data quality has been compromised, a DQR will be filed. (hb p. 10) |
| Maintenance interval | Daily visual checks (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: PARS2 (laser disdrometer), RWP (radar wind profiler), MET (surface meteorological instrumentation).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `DOE` | U.S. Department of Energy |
| `DQAR` | Data Quality Assessment Report |
| `DQR` | Data Quality Report |
| `IF` | intermediate facility |
| `MET` | surface meteorological instrumentation |
| `PARS2` | laser disdrometer |
| `PRECIPMET` | precipitation meteorological instruments |
| `PTU` | pan and tilt unit |
| `QC` | quality checks |
| `RC` | resistor-capacitor |
| `RWP` | radar wind profiler |
| `SGP` | Southern Great Plains |
| `TBRG` | tipping bucket rain gauge |


### References the handbook cites

- Vaisala. 2012. USER'S GUIDE: Vaisala Weather Transmitter WXT520. Helsinki, Finland: Vaisala Oyj.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-226.pdf (17 pages, DOE/SC-ARM-TR-226, by J Kyrouac)
- Catalog record: ARM data-source index, `instrument_class_code=precipmet`, read 2026-09-23
- Example file: `sgpprecipmetI9.b1.20230926.000100.nc` from `sgpprecipmetI9.b1`, 0.2 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
