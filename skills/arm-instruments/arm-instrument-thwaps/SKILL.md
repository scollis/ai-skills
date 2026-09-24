---
name: arm-instrument-thwaps
description: ARM Temperature, Humidity, Wind and Pressure Sensors (thwaps) - handbook-derived instrument reference. Measurement principle, reported quantities (Pressure, Temperature, RH, Vapor Pressure, Mean Wind Speed, Unit Vector Wind Direction), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpthwapsC1.b1) and the variable inventory of a real file. Use when working with thwaps data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - thwaps, Temperature, Humidity, Wind and Pressure Sensors, sgpthwapsC1.b1, Pressure, Temperature, RH, Vapor Pressure, Mean Wind Speed, Unit Vector Wind Direction, Surface Meteorology, Wind speed/direction - R.M. Young Model 05103 Wind Monitor, Temperature/RH - Vaisala HMP233 Series Transmitters, Relative humidity, Wind Monitor, NIST, SONDE.
---

# THWAPS - Temperature, Humidity, Wind and Pressure Sensors

THWAPS provides calibration-quality surface reference measurements of temperature, relative humidity, barometric pressure, and wind speed/direction near a balloon-borne sounding (SONDE) launch site to serve as ground-truth comparison values for radiosonde readings, while also logging continuous time series of these variables.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `thwaps` |
| Handbook | [ARM TR-030 / January 2011](https://www.arm.gov/publications/tech_reports/handbooks/thwaps_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Wind speed/direction: R.M. Young Model 05103 Wind Monitor; Temperature/RH: Vaisala HMP233 Series Transmitters; Barometric pressure: Vaisala Model PTB201A; Data logger: Campbell Scientific Model CR10... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind |
| Record | 1999-09-21 to 2016-01-26 (retired) |
| Datastreams with data | 10 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/thwaps |


## Credit

The handbook this skill derives from names no individual author on its cover;
it is issued by the ARM facility. The instrument knowledge in it is still the
mentor programme's work, not this file's:

> ARM Climate Research Facility. *Temperature, Humidity, Wind, and Pressure System (THWAPS) Handbook*, ARM TR-030, January 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/thwaps_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The wind monitor uses a propeller anemometer that produces a magnetically controlled AC output whose frequency is proportional to wind speed, while a wind vane drives a potentiometer that is part of a resistance bridge to determine direction. The temperature sensor is an RTD that is also part of a resistance bridge, and the Vaisala RH circuitry produces a voltage proportional to the capacitance of a water-vapor-absorbing thin polymer film. The barometric pressure sensor uses a silicon capacitive pressure sensor housed in a weatherproof enclosure. The data logger samples each input once every 3 s and computes 5-minute averages (including vector-averaged wind speed and direction) along with vapor pressure derived from air temperature and RH, plus standard deviations of several variables.

**Siting.** The THWAPS is located adjacent to the SONDE launch site at the SGP Central Facility to serve as a ground reference point for radiosonde launches. The T/RH sensor is mounted at a height of 1 m in an R.M. Young Model 43408 Gill Aspirated Radiation Shield; the PTB201 barometer is located in the BBSS trailer and vented to the outside, mounted at 1 m; the wind monitor is mounted on a mast on the SONDE trailer at a height of 5 m. Note: lat/lon/alt in the data refers to the ground where the instrument is sited, NOT the height of the sensor. The system is not generally used as a surface meteorological measurement system, and many variables do not conform to WMO standards for surface meteorological...

**Sampling.** native rate each input measured once every 3 s; reported every 5 min; averaging 5-min averages of wind speed, vector-averaged wind speed, vector-averaged wind direction, air temperature, RH, vapor pressure, and barometric pressure; standard deviations also calculated (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Pressure | hPa | - | +/-0.035 kPa | 0.1 | (hb p. 8) |
| Temperature | C | - | +/-0.4 C (sensor); +/-0.57 C (95% confidence... | 0.1 | (hb p. 8) |
| RH | % | - | +/-2.06% RH (0-90% RH), +/-3.04% RH (90-100% RH) | 1 | (hb p. 8) |
| Vapor Pressure | kPa | - | - | 0.001 | (hb p. 8) |
| Mean Wind Speed | m/s | - | +/-1% for 2.5 to 30 m/s | 0.1 | (hb p. 8) |
| Unit Vector Wind Direction | deg | - | +/-5 deg | 1 | (hb p. 8) |
| Standard Deviation of Wind Direction | deg | - | - | 1 | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wind speed at 5 m, Precision | 0.01 m/s | (hb p. 13) |
| Wind speed at 5 m, Uncertainty | +/-1% for 2.5 to 30 m/s | (hb p. 13) |
| Wind direction at 5 m, Precision | 0.1° | (hb p. 13) |
| Wind direction at 5 m, Uncertainty | +/-5° | (hb p. 13) |
| Air temperature at 1 m, Precision | 0.01 C | (hb p. 13) |
| Air temperature at 1 m, Uncertainty | a function of wind speed | (hb p. 13) |
| RH at 1 m, Precision | 0.1% RH | (hb p. 13) |
| RH at 1 m, Uncertainty | +/-2.06% RH (0% to 90% RH), +/-3.04% RH (90% to 100% RH) | (hb p. 13) |
| Barometric pressure at 1 m, Precision | 0.01 kPa | (hb p. 13) |
| Barometric pressure at 1 m, Uncertainty | +/-0.035 kPa | (hb p. 13) |
| Data logger precision | A function of input type and range | (hb p. 12) |
| Data logger uncertainty (analog inputs) | 0.2% of Full-Scale Range for Analog Inputs | (hb p. 12) |
| CR10 A/D converter accuracy | +/-0.2% of full-scale range | (hb p. 13) |
| Time base accuracy | +/-1 min per month, or about 23 ppm | (hb p. 13) |
| Wind sensor threshold | 1 m/s | (hb p. 13) |
| Wind direction sensor accuracy | +/-3° | (hb p. 14) |
| Wind direction A/D conversion accuracy | +/- 0.7° over 0 to 40°C for a period of one year | (hb p. 14) |
| Wind direction sensor alignment to true north | +/-3° | (hb p. 14) |
| Temperature radiation error of aspirated shield | +/- 0.2 C rms | (hb p. 14) |
| RH A/D conversion accuracy | +/-0.5% RH | (hb p. 14) |
| NIST wind speed calibration uncertainty | +/-1% for wind speeds from sensor threshold to 30 m/s | (hb p. 13) |


## The data

Verified example: **`sgpthwapsC1.b1`**, file `sgpthwapsC1.b1.20160123.000000.cdf`
(0.04 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=288 |
| Data variables | 29 |
| QC variables | 12 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2016-01-23T00:00:00 to 2016-01-23T23:55:00 |
| sampling interval | 3 seconds |
| averaging interval | 5 minutes |
| dod version | thwaps-b1-2.1 |
| process version | ingest-thwaps-8.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pres` | hPa | time | yes | Atmospheric pressure |
| `rh` | % | time | yes | Relative humidity |
| `sd_pres` | hPa | time | yes | Standard deviation of atmospheric pressure |
| `sd_rh` | % | time | yes | Standard deviation of relative humidity |
| `sd_temp` | degC | time | yes | Standard deviation of temperature |
| `sd_vap_pres` | kPa | time | yes | Standard deviation of vapor pressure |
| `sd_wdir` | degree | time | yes | Standard deviation of wind direction |
| `temp` | degC | time | yes | Temperature |
| `vap_pres` | kPa | time | yes | Vapor pressure |
| `vbat` | V | time | yes | Battery voltage |
| `wdir` | degree | time | yes | Unit vector wind direction |
| `wspd` | m/s | time | yes | Mean wind speed |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpthwapsC1.b1", "2016-01-23", "2016-01-23")
ds = armlive_open("sgpthwapsC1.b1", "2016-01-23", "2016-01-23", cleanup_qc=True)
```

## Quality control in this datastream

12 `qc_` companion variables cover 12 of the
29 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("sgpthwapsC1.b1", "19990921", "20260923")
```

The handbook's own note on data quality: Data quality flags (qc_ variables) are provided for each primary/diagnostic variable with defined min/max acceptable ranges (e.g., qc_pres 800-1100 hPa, qc_temp -40 to 50 C, qc_rh -2 to 104%, qc_vap_pres 0-10 kPa, qc_wspd 0-45 m/s, qc_wdir 0-360 deg, qc_sd_wdir 0-90 deg, qc_sd_temp 0-2, qc_vbat 9.6-16 V). Data Quality Health and Status (DQ HandS) and NCVweb provide interactive data plotting for quality checks (http://dq.arm.gov). The ARM Data Quality Office uses the Data Quality Assessment (DQA) system to inform Site Operators, Site Scientists, and Instrument Team members of instrument and...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Non-WMO-conforming measurements | Many of the variables measured do not conform to WMO standards for surface meteorological measurements, so THWAPS data may differ systematically from standard surface met station data | THWAPS should be used to gather reference values for the SONDE rather than as a general surface meteorological measurement system | (hb p. 6) |
| Boundary facility calibration/multiplier errors causing RH greater than  100% | RH% values recorded greater than 100% at boundary facilities B1, B4, B5, B6 prior to correction dates | Calibrations and datalogging program were corrected on specific dates in 2005 (B1 08/01/2005, B4 07/30/2005, B6 07/30/2005, B5 07/31/2005); vapor... | (hb p. 10) |
| RH ceiling artifact from calibration error | The calibration error forced the probe to output a maximum of 1V translating to 100%, arbitrarily instituting a ceiling of 100% and preventing normal overrange behavior of the sensor | Corrected via the 2005 calibration/multiplier fixes | (hb p. 10) |
| Wind speed underestimation below sensor threshold | Reported wind speeds near or below the 1 m/s threshold are biased low; e.g., reported 0.5 m/s implies ~0.5 m/s underestimate, reported 1.0 m/s implies 0.19-0.30 m/s underestimate, reported... | - | (hb p. 13) |
| Temperature uncertainty dependent on wind speed | Air temperature uncertainty at 1 m is described as 'a function of wind speed', implying variable accuracy under different wind conditions | - | (hb p. 13) |
| Unknown long-term stability of temperature sensor | Temperature accuracy specification does not include a characterized long-term drift; the long-term stability is not known | - | (hb p. 14) |
| Radiation error in aspirated shield | Temperature readings may include a radiation error of +/- 0.2 C rms from the aspirated radiation shield, contributing to overall 95% confidence uncertainty of +/-0.57 C | - | (hb p. 14) |
| Data acquisition (A/D) error | Analog input measurements carry an uncertainty of +/-0.2% of full-scale range from the CR10 A/D converter | - | (hb p. 13) |
| Datalogger clock drift | Time base accuracy of +/-1 min per month (~23 ppm) could cause timestamp drift in the data | The Site Data System checks the time-of-day clock once per day and corrects the THWAPS clock if it is off by more than a minute | (hb p. 13) |
| Lack of formal calibration program | No calibration records or history exist for THWAPS instruments; calibration theory/procedures/history sections are not applicable | Work is in progress on creating a 6-month calibration procedure | (hb p. 15) |
| QC range flags for physically implausible values | QC flags trigger when pressure is outside 800-1100 hPa, temperature outside -40 to 50 C, RH outside -2 to 104%, vapor pressure outside 0-10 kPa, wind speed outside 0-45 m/s, wind direction... | - | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | The THWAPs have not been calibrated. Work is in progress on creating a 6-month calibration procedure. (hb p. 15) |
| Calibration interval | not established (6-month procedure in progress) (hb p. 15) |
| Traceability | NIST calibration uncertainty specified for wind speed sensor (hb p. 15) |
| Routine maintenance | Section not applicable to this instrument (no routine/corrective maintenance documentation provided) (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SONDE (balloon-borne sounding system).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Barometric pressure` | Local station pressure measured at the THWAPS station at a height of 1 m. |
| `Relative humidity` | Percentage of saturated vapor pressure at the specified temperature. |
| `Vector-averaged wind...` | Wind speed computed as the vector sum of the orthogonal u and v components which are... |
| `Wind Monitor` | Trade name for R.M. Young propeller anemometer and wind vane. |
| `AC` | alternating current |
| `A/D` | Analog to Digital converter |
| `DQA` | Data Quality Assessment |
| `NIST` | National Institute of Standards and Technology |
| `QME` | Quality Measurement Experiment |
| `RH` | Relative Humidity |
| `rms` | root mean square |
| `SGP` | Southern Great Plains |
| `SONDE` | balloon-borne sounding system |
| `THWAPS` | Temperature, Humidity, Wind, and Pressure System |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/thwaps_handbook.pdf (17 pages, ARM TR-030, no individual author named on the cover)
- Catalog record: ARM data-source index, `instrument_class_code=thwaps`, read 2026-09-23
- Example file: `sgpthwapsC1.b1.20160123.000000.cdf` from `sgpthwapsC1.b1`, 0.04 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
