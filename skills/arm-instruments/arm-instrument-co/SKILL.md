---
name: arm-instrument-co
description: ARM Carbon Monoxide Mixing Ratio System (co) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpcoC1.b1) and the variable inventory of a real file. Use when working with co data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Carbon. Triggers - co, Carbon Monoxide Mixing Ratio System, sgpcoC1.b1, Atmospheric Carbon, Thermo Electron Corporation, ESRL, LBNL, NOAA, TE48C.
---

# CO - Carbon Monoxide Mixing Ratio System

The CO system provides continuous measurements of carbon monoxide mixing ratio in dry air at the ARM SGP Central Facility 60-meter tower using a Thermo Electron 48C-TL trace level gas filter correlation CO analyzer.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `co` |
| Handbook | [DOE/SC-ARM/TR-072 / SC Biraud / February 2011](https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Thermo Electron Corporation, Model 48C-TL trace level gas filter correlation CO analyzer (Model 48C) |
| Primary measurements | Carbon monoxide (CO) Concentration |
| Record | 2005-06-01 to 2011-12-31 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/co |


## Credit

Everything this skill knows about the instrument is the work of **SC Biraud** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SC Biraud. *CO (Carbon Monoxide Mixing Ratio System) Handbook*, DOE/SC-ARM/TR-072, February 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The Model 48C is based on the principle that carbon monoxide (CO) absorbs infrared radiation at a wavelength of 4.6 microns. Because infrared absorption is a non-linear measurement technique, the instrument electronics transform the basic analyzer signal into a linear output using an exact calibration curve valid up to a concentration of 10,000 ppm. The sample is drawn through the optical bench, where infrared radiation from a chopped source passes through a gas filter alternating between CO and N2 and then a narrow bandpass interference filter before absorption by the sample gas occurs and the beam falls on an infrared detector. The CO gas filter produces a reference beam that cannot be further attenuated by CO in the sample cell, while the N2 side of the filter wheel is transparent and produces a measure beam absorbable by CO in the cell; the chopped detector signal is modulated by alternation between the two gas filters with an amplitude related to CO concentration. Other gases do not cause modulation of the detector signal since they absorb the reference and measure beams equally, so the gas filter correlation (GFC) system responds specifically to CO concentrations.

**Siting.** Deployed at the ARM SGP Central Facility (CF) 60-meter tower (36.607 °N, 97.489 °W, 314 meters above sea level); data acquisition PC located in an instrument shed at the base of the 60-m tower.

**Sampling.** native rate raw data time stamped every 5 seconds (a1 files); described also as 5-Hz data; reported every 10-minute intervals (per ARM catalog); sample measured for 5 minutes at a time; averaging reported value is the average of the last 2 minutes of a 5-minute sample; Zero Noise 120-second averaging; Response Time 30-second averaging (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Carbon monoxide mixing ratio in dry air | ppb (parts per billion by... | 60 to 1000 ppb | 5 ppb (order of); Accuracy 4 ppb | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | See Table 1 | (hb p. 11) |
| Range | 60 to 1000 ppb | (hb p. 11) |
| Accuracy | 4 ppb | (hb p. 11) |
| Uncertainty | on the order of 5 ppb | (hb p. 11) |
| Input Voltage | 105–125 VAC, 60Hz | (hb p. 11) |
| Input Current | 100 Watts | (hb p. 11) |
| Input Values |  | (hb p. 11) |
| Output Values | Carbon monoxide mixing ratios; Selectable voltage; 4–20mA, RS-232, RS-485 | (hb p. 11) |
| Zero Noise | 5.0 ppb RMS (120-second averaging time) | (hb p. 8) |
| Zero Drift (24 hour) | less than 100 ppb | (hb p. 8) |
| Response Time | 60 seconds (30-second averaging time) | (hb p. 8) |
| Precision | 10.0 ppb | (hb p. 8) |
| Sample Flow Rate | 0.5 liter/min | (hb p. 8) |
| Operating Temperature | 20° 30°C (may be safely operated over the range 5°–45°C) | (hb p. 8) |
| Power Requirements | 90–100 VAC; 210–240 VAC, 50 Hz, 100 Watts | (hb p. 8) |
| Tylan mass flow controller Flow | 0.5 LPM | (hb p. 8) |
| Tylan mass flow controller Step Response Time | 1 second (dependent on step request and conditions) | (hb p. 8) |
| Tylan mass flow controller Accuracy | ± 1.0% full scale | (hb p. 8) |
| Tylan mass flow controller Linearity | ± 0.5% full scale | (hb p. 8) |
| Tylan mass flow controller Repeatability | ± 0.2% full scale | (hb p. 8) |
| Tylan mass flow controller Valve | Normally open or normally closed solenoid | (hb p. 8) |
| Tylan mass flow controller Supply Voltage | ± 12 VDC to ± 18 VDC | (hb p. 8) |
| Tylan mass flow controller Supply Current | 110 mA nominal (125 mA max @ ± 18 VDC) | (hb p. 8) |
| Tylan mass flow controller Power Consumption | 3.3 watts @ ± 15 volts | (hb p. 8) |
| Tylan mass flow controller Input/Output Signal | 0-5 VDC | (hb p. 8) |
| MKS Pressure controller (model 640) Pressure | 100 PSI | (hb p. 8) |


_6 further specification rows are in the handbook._

## The data

Verified example: **`sgpcoC1.b1`**, file `sgpcoC1.b1.20111228.000232.cdf`
(0.04 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

**Reading note.** read with use_base_time=True: the file time units string is not CF-decodable.

|  |  |
|---|---|
| Dimensions | `time`=286 |
| Data variables | 31 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2011-12-28T00:02:32 to 2011-12-28T23:57:32 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `agc` | Hz | time | yes | Automatic Gain Control |
| `chamber_temp` | Degrees Celcius | time | yes | Chamber Temperature |
| `co` | ppb | time | yes | Calculated CO concentration |
| `dpt` | Degrees Celcius | time | yes | Dew Point Temperature |
| `flow_TE48C` | LPM | time | yes | Flow measure by TE48C |
| `flow_control` | LPM | time | yes | flow measured by the flow controller |
| `int_temp` | Degrees C | time | yes | Internal temperature |
| `press_TE48C` | Torr | time | yes | Presure mesure by TE48C |
| `press_control` | Torr | time | yes | pressure measured by the pressure controller |
| `channel` | unitless | time | - | Sequential data channel number. See channel_explanation global... |
| `day` | day of month | time | - | Day |
| `hour` | hour of day | time | - | Hour |
| `min` | minute of hour | time | - | Minute |
| `month` | month of year | time | - | Month |
| `sec` | second of minute | time | - | Second |
| `site_elevation` | meters above sea level | - | - | height of base of instrument tower |
| `site_latitude` | degrees | - | - | latitude of instrument tower |
| `site_longitude` | degrees | - | - | longitude of instrument tower |
| `time` | - | time | - | Time offset from midnight of date of file. For CO data, this is... |
| `year` | four digit year in... | time | - | Year |
| `yyyydddhhmmss` | unitless | time | - | Date and time in alternate form |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpcoC1.b1", "2011-12-28", "2011-12-28")
ds = armlive_open("sgpcoC1.b1", "2011-12-28", "2011-12-28", cleanup_qc=True)
```

## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
31 data variables. Assessments present in the example file: .

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
act.qc.print_dqr("sgpcoC1.b1", "20050601", "20260923")
```

The handbook's own note on data quality: Data quality is evaluated via QC flags in two processing stages: raw a0 files (with truncated lines purged) are processed to a1 files (time-stamped, uncorrected 5-second/5-Hz data), then a1 files are processed to calculate CO mixing ratios and associated qc flags, involving averaging concentrations for sampled/zero/span air channels, correcting for instrument offset, finding calibration data and correcting for drifts, and writing netCDF output. Almost every variable 'x' has a corresponding qc flag 'qc_x'. qc flag values: 0 = value not suspect, 1 = value in a range that might point toward a...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Windows operating system 'hiccups' causing truncated data lines in raw (a0) files | Truncated lines appear in a0 raw data files; these are purged during a0 to a1 processing, so gaps or missing 5-second records may appear in a1 files | Truncated lines are purged during the a0 to a1 processing | (hb p. 10) |
| CO out-of-range warning/bad thresholds | qc_co flag = 1 (warning) when 50 less than  CO less than  60 ppb or 600 less than  CO less than  800 ppb; qc_co flag = 2 (bad) when CO less than  50 ppb or CO greater than  800 ppb | - | (hb p. 10) |
| Instrument internal temperature (int_temp) drift/out-of-range | qc flag = 1 when 25 less than  int_temp less than  30 °C or 40 less than  int_temp less than  45 °C; qc flag = 2 when int_temp less than  25 °C or int_temp greater than  45 °C | - | (hb p. 10) |
| Chamber temperature (chamber_temp) out-of-range | qc flag = 1 when 35.0 less than  chamber_temp less than  42.4 °C or 47.5 less than  chamber_temp less than  55.0 °C; qc flag = 2 when chamber_temp less than  35.0 °C or greater than  55.0 °C | - | (hb p. 10) |
| Automatic gain control (agc) out-of-range, indicating optical/detector issues | qc flag = 1 when 1.90e5 less than  agc less than  1.95e5 Hz or 2.05e5 less than  agc less than  2.1e5 Hz; qc flag = 2 when agc less than  1.9e5 Hz or agc greater than  2.1e5 Hz | - | (hb p. 10) |
| TE48C internal pressure (pres_TE48C) out-of-range | qc flag = 1 when 790 less than  pres_TE48C less than  800 Torr or 820 less than  pres_TE48C less than  830 Torr; qc flag = 2 when pres_TE48C less than  790 Torr or greater than  830 Torr | - | (hb p. 10) |
| TE48C flow rate (flow_TE48C) out-of-range | qc flag = 1 when 0.40 less than  flow_TE48C less than  0.45 LPM or 0.55 less than  flow_TE48C less than  0.60 LPM; qc flag = 2 when flow_TE48C less than  0.40 or greater than  0.60 LPM | - | (hb p. 10) |
| Pressure controller (pres_control) out-of-range | qc flag = 1 when 785 less than  pres_control less than  795 Torr or 805 less than  pres_control less than  815 Torr; qc flag = 2 when pres_control less than  785 or greater than  815 Torr | - | (hb p. 10) |
| Flow controller (flow_control) out-of-range | qc flag = 1 when 0.40 less than  flow_control less than  0.45 LPM or 0.55 less than  flow_control less than  1.00 LPM; qc flag = 2 when flow_control less than  0.40 or greater than  1.00 LPM | - | (hb p. 10) |
| Dew point (dpt) too high, risk of condensation affecting sample | qc flag = 1 when -15 less than  dpt less than  -10 °C; qc flag = 2 when dpt greater than  -10.0 °C | DMT142 dewpoint transmitter withstands condensation | (hb p. 10) |
| Non-linear infrared absorption response of the analyzer | Would produce non-linear analyzer signal if not corrected | Instrument electronics use an exact calibration curve to linearize output over any range up to 10,000 ppm concentration | (hb p. 12) |
| Zero and span drift of the instrument over time | Apparent offset or scale change in reported CO values over 24-hour or longer periods (Zero Drift 24 hour: less than 100 ppb) | Periodically calibrate out zero and span drifts using a CO scrubber and two concentrations of span gas (100 and 300 ppb CO in air); samples bracketed... | (hb p. 8) |
| Interference from other gases | None expected in modulated detector signal | GFC design: other gases absorb reference and measure beams equally, so they do not cause modulation of the detector signal, giving specificity to CO | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Every 6 hours, two calibration standards certified by NOAA ESRL at approximately 100 and 300 ppb are run; sample CO concentration is calculated with the standards run before and after it. Samples are bracketed by two secondary calibration standards, which have been calibrated against two primary NOAA ESRL-certified... (hb p. 13) |
| Calibration interval | every 6 hours (hb p. 13) |
| Traceability | NOAA ESRL-certified primary standards (SCOTT MARRIN 150A, CA05962: 95±1 ppb; CA05909: 292.5±2.9 ppb CO in air, performed by NOAA - D. Kitzis, 12/1/2003) (hb p. 13) |
| Routine maintenance | ARM staff performs preventive maintenance checks and posts post-preventive maintenance reports on the Internet; ARM carbon staff at LBNL checks these reports; instrument mentor routinely views graphical displays of CO concentrations, flow rate, pressure, automatic gain control, and dew point temperature. (hb p. 14) |
| Maintenance interval | weekly (hb p. 14) |


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
| `CF` | Central Facility |
| `CO` | Carbon Monoxide |
| `DQ` | Data Quality |
| `ESRL` | National Earth System Research Laboratory |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `NOAA` | National Oceanic & Atmospheric Administration |
| `PC` | personal computer |
| `SGP` | Southern Great Plains |
| `STS` | Site Transfer Suite |
| `QC` | Quality Control |
| `TE48C` | Thermo Electron 48C |


### References the handbook cites

- Chaney, LW, and WA McClenny. 1977. "Unique ambient carbon monoxide monitor based on gas filter correlation: performance and application." Environmental Science and Technology 11: 1186–1190.
- Dickerson RR, and AC Delany. 1988. "Modification of a commercial gas filter correlation CO detector for enhanced sensitivity." Journal of Atmospheric and Oceanic Technology 5: 424–431.
- Novelli, PC, JW Elkins, and LP Steele. 1991. "The development and evaluation of a gravimetric reference scale for measurements of atmospheric carbon monoxide." Journal of Geophysical Research 96: 13,109–13,121.
- Parrish, DD. JS Holloway, and FC Fehsenfeld. 1994. "Routine, continuous measurement of carbon monoxide with parts per billion precision." Environmental Science and Technology 28: 1615–1618.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf (15 pages, DOE/SC-ARM/TR-072, by SC Biraud)
- Catalog record: ARM data-source index, `instrument_class_code=co`, read 2026-09-23
- Example file: `sgpcoC1.b1.20111228.000232.cdf` from `sgpcoC1.b1`, 0.04 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
