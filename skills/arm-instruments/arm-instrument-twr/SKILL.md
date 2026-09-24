---
name: arm-instrument-twr
description: ARM Facility-specific multi-level Meteorological Instrumentation (twr) - handbook-derived instrument reference: measurement principle, reported quantities (Temperature, Relative humidity, Vapor Pressure, Aspirator status, Battery voltage, Standard deviation of temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptowermetC1.b1) and the variable inventory of a real file. Use when working with twr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling; Surface Meteorology. Triggers - twr, sgptowermetC1.b1, Temperature, Relative humidity, Vapor Pressure, Aspirator status, Battery voltage, Standard deviation of temperature, Atmospheric Profiling, Surface Meteorology, SGP CF: Vaisala HMP35D/HMP45D T/RH probes, Minco Products Model S853PD60X72 PRTD, T/RH/VP, PRTD, RMSE, Uncertainty.
---

# TWR - Facility-specific multi-level Meteorological Instrumentation

Multi-level towers (SGP CF 60-m, SGP Okmulgee 21-m, NSA Barrow 40-m) carry meteorological (temperature, relative humidity, vapor pressure, wind, pressure, precipitation) and radiological/flux instrumentation at fixed heights, with the SGP CF tower's T/RH/VP measurements at 25-m and 60-m levels on both a west elevator and southeast elevator described in detail.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 30 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `twr` |
| Handbook | [DOE/SC-ARM/TR-050 / D R Cook / January 2016](https://www.arm.gov/publications/tech_reports/handbooks/twr_handbook.pdf) |
| Measurement category | Atmospheric Profiling; Surface Meteorology |
| Manufacturer / model | SGP CF: Vaisala HMP35D/HMP45D T/RH probes, Minco Products Model S853PD60X72 PRTD, Qualimetrics Model 8151-B aspirated radiation shield, R.M. Young Model 43408/43482 aspirated radiation shield,... |
| Primary measurements | Atmospheric moisture; Atmospheric temperature; Horizontal wind; Vertical velocity |
| Record | 1993-07-21 to 2026-09-22 (active) |
| Datastreams with data | 28 across 3 sites |
| Sites | bnf, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/twr |


## Credit

Everything this skill knows about the instrument is the work of **D R Cook** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D R Cook. *Towers Handbook*, DOE/SC-ARM/TR-050, January 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/twr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Air temperature is measured with platinum resistance temperature detectors (PRTDs) and relative humidity with Vaisala Humicap capacitive elements (or, historically, Qualimetrics capacitive probes), housed in motor-aspirated radiation shields at 25-meter and 60-meter levels on both the west and southeast elevators of the SGP CF tower. A datalogger performs the resistance-to-temperature conversion using a built-in polynomial function and computes ambient vapor pressure from the measured temperature and relative humidity via a saturation-vapor-pressure instruction (Vapor Pressure = Relative Humidity/Saturation Vapor Pressure, in kPa). On the NSA Barrow tower, additional sensors measure wind (sonic anemometer), pressure (BAROCAP capacitive sensor), humidity/temperature (HUMICAP/Pt100), and present weather/visibility (optical/present weather detectors) at multiple heights. Aspirators maintain airflow across the T/RH probes to reduce solar radiation heating errors, though flow rates differ between the metal west-side (~1.8 L/min) and plastic southeast-side (~3 L/min) shields.

**Siting.** SGP CF 60-meter tower has duplicate T/RH/VP instrumentation on west elevator and southeast elevator at 25-m and 60-m levels; data users advised to use southeast side measurements unless unavailable, because southeast aspiration/radiation shielding is better than west side. Lat/lon/alt dimension variables refer to ground surface, not instrument height. SGP Okmulgee tower sited in forest and subject to vulture roosting affecting instruments. NSA tower sensors subject to freeze-up/rime ice in winter.

**Sampling.** native rate 1 minute; reported every 1 and 30 minute; averaging 30-minute standard deviations reported for temperature, RH and vapor pressure alongside 1- and 30-minute means (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Temperature (temp) | degC | - | +/- 0.2°C | - | (hb p. 9) |
| Relative humidity (rh) | %RH | 0-100% RH | +/- 2% (0-90% RH), +/- 3% (90-100% RH) | - | (hb p. 9) |
| Vapor Pressure (vap_pres) | kPa | - | not provided by manufacturer; T and RH... | - | (hb p. 9) |
| Aspirator status (aspirator) | - | - | - | - | (hb p. 10) |
| Battery voltage (vbat) | volts | - | - | - | (hb p. 10) |
| Standard deviation of temperature (sd_temp) | degC | - | - | - | (hb p. 10) |
| Standard deviation of relative humidity (sd_rh) | %RH | - | - | - | (hb p. 10) |
| Standard deviation of vapor pressure (sd_vap_pres) | kPa | - | - | - | (hb p. 10) |
| NSA visibility/precipitation (PWD22) | m | 10m-10000m (vis), 10km-20km | +/- 10% vis 10m-10000m, +/-15% vis 10km-20km;... | - | (hb p. 22) |
| NSA chilled mirror hygrometer temp/dew point (CMH) | degF/deg | -58 to 122F (temp) | +/-0.5deg (-58 to 122F); +/-1deg remainder; dew... | - | (hb p. 22) |
| NSA wind speed/direction (WS425) | m/s, deg | 1 to 65 m/s | speed +/- 0.135 or 3% of reading (whichever... | - | (hb p. 22) |
| NSA atmospheric pressure (PTB220) | hPa | 50 to 1100 hPa | +/- 0.15 hPa (linearity +/- 0.1 hPa/yr) | - | (hb p. 22) |
| NSA T/RH/VP/Dew Point (HMT337) | degC, %RH | 0 to 100% RH; -70 to 180C | (temp) +/- 0.2C @ 20C increasing to +/- 0.5C at... | - | (hb p. 22) |


## Specifications

| parameter | value | source |
|---|---|---|
| West Elevator Air temperature sensor | PRTD, 100 ohm, Minco Products Inc., Model S853PD60X72; Detection Limits -30 to 40°C; Operating Temperature Range -40 to 50°C; Accuracy +/- 0.2°C | (hb p. 16) |
| West Elevator RH before September 1996 | Capacitive element, Vaisala Inc. Humicap; probe Qualimetrics Model 5120-E or 5134-E; Detection Limits 0-100% RH; Accuracy +/- 2% (0-80% RH) and +/-... | (hb p. 16) |
| West Elevator RH after September 1996 | Vaisala Inc. HMP35D or HMP45D; Humicap capacitive element; Detection Limits 0-100% RH; Accuracy +/- 2% (0-90% RH) and +/- 3% (90-100%) over -20 to... | (hb p. 16) |
| West Elevator Motor Aspirated Radiation Shield | Qualimetrics Model 8151-B with flow sensor; nominal ventilation rate 1.83 m/s into inlet; radiation error 0.05°C; operating temperature range -40 to... | (hb p. 16) |
| West Elevator Flow Sensor | Qualimetrics Model T450009, heated-element-type sensor | (hb p. 16) |
| Southeast Elevator Air Temperature | PRTD, 100 ohm; Detection Limits -30 to 40°C; Operating Temperature Range -40 to 50°C; Accuracy +/- 0.2°C | (hb p. 16) |
| Southeast Elevator Relative Humidity | Humicap capacitive element; Detection Limits 0-100% RH; Accuracy +/- 2% (0-90% RH) and +/- 3% (90-100%) over -20 to 50°C; uncertainty of RH... | (hb p. 16) |
| Southeast Elevator Motor Aspirated Radiation Shield | R.M. Young Model 43408/43482; nominal ventilation rate 3 m/s into inlet; radiation error 0.05°C; operating temperature range -40 to 55°C | (hb p. 16) |
| NSA PWD22 | Uncertainty +/- 10% vis 10m-10000m, +/-15% vis 10km-20km; precip detection .05mm/hr or less within 10min; operating conditions -40 to 60C, up to 100%... | (hb p. 22) |
| NSA CMH (chilled mirror hygrometer) | Temp +/-0.5deg (-58 to 122F); +/-1deg remainder; dew point +/-2deg RMS (30-86F); +/-3deg RMS (-10-30F); +/-4deg (-30 to -10F); operating conditions... | (hb p. 22) |
| NSA WS425 | Measurement range 1 to 65 m/s; speed accuracy +/- 0.135 or 3% of reading (whichever greater); direction accuracy +/- 2deg; operating temp -55 to 55C | (hb p. 22) |
| NSA PTB220 | Vaisala BAROCAP silicon capacitive absolute sensor; uncertainty +/- 0.15 hPa (linearity +/- 0.1 hPa/yr); range 50 to 1100 hPa; operating temp -40 to... | (hb p. 22) |
| NSA HMT337 | Vaisala HUMICAP180 capacitive thin film polymer sensor (RH) and Pt100 resistive platinum sensor (temp); operating conditions -70 to 180C, 0-100% RH;... | (hb p. 22) |


## The data

Verified example: **`sgptowermetC1.b1`**, file `sgptowermetC1.b1.20260919.000000.nc`
(0.3 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 46 |
| QC variables | 14 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| dod version | towermet-b1-1.1 |
| process version | ingest-towermet-2.2-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `battery_voltage` | V | time | yes | Logger voltage |
| `logger_temperature` | degC | time | yes | Logger temperature |
| `relative_humidity_SE_25m_avg` | % | time | yes | Relative humidity at southeast 25m tower |
| `relative_humidity_SE_60m_avg` | % | time | yes | Relative humidity at southeast 60m tower |
| `relative_humidity_W_25m_avg` | % | time | yes | Relative humidity at west 25m tower |
| `relative_humidity_W_60m_avg` | % | time | yes | Relative humidity at west 60m tower |
| `temperature_SE_25m_avg` | degC | time | yes | Air temperature at southeast 25m tower |
| `temperature_SE_60m_avg` | degC | time | yes | Air temperature at southeast 60m tower |
| `temperature_W_25m_avg` | degC | time | yes | Air temperature at west 25m tower |
| `temperature_W_60m_avg` | degC | time | yes | Air temperature at west 60m tower |
| `vapor_pressure_SE_25m_avg` | kPa | time | yes | Vapor pressure at southeast 25m tower |
| `vapor_pressure_SE_60m_avg` | kPa | time | yes | Vapor pressure at southeast 60m tower |
| `vapor_pressure_W_25m_avg` | kPa | time | yes | Vapor pressure at west 25m tower |
| `vapor_pressure_W_60m_avg` | kPa | time | yes | Vapor pressure at west 60m tower |
| `relative_humidity_SE_25m_std` | % | time | - | Standard deviation of relative humidity at southeast 25m tower |
| `relative_humidity_SE_60m_std` | % | time | - | Standard deviation of relative humidity at southeast 60m tower |
| `relative_humidity_W_25m_std` | % | time | - | Standard deviation of relative humidity at west 25m tower |
| `relative_humidity_W_60m_std` | % | time | - | Standard deviation of relative humidity at west 60m tower |
| `temperature_SE_25m_std` | degC | time | - | Standard deviation of air temperature at southeast 25m tower |
| `temperature_SE_60m_std` | degC | time | - | Standard deviation of air temperature at southeast 60m tower |
| `temperature_W_25m_std` | degC | time | - | Standard deviation of air temperature at west 25m tower |
| `temperature_W_60m_std` | degC | time | - | Standard deviation of air temperature at west 60m tower |
| `time` | - | time | - | Time offset from midnight |
| `vapor_pressure_SE_25m_std` | kPa | time | - | Standard deviation of vapor pressure at southeast 25m tower |
| `vapor_pressure_SE_60m_std` | kPa | time | - | Standard deviation of vapor pressure at southeast 60m tower |
| `vapor_pressure_W_25m_std` | kPa | time | - | Standard deviation of vapor pressure at west 25m tower |
| `vapor_pressure_W_60m_std` | kPa | time | - | Standard deviation of vapor pressure at west 60m tower |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgptowermetC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("sgptowermetC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

This datastream carries 46 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgptowermetC1.b1", start, end,
                  keep_variables=["battery_voltage", "logger_temperature", "relative_humidity_SE_25m_avg", "qc_battery_voltage", "qc_logger_temperature", "qc_relative_humidity_SE_25m_avg"])
```

## Quality control in this datastream

14 `qc_` companion variables cover 14 of the
46 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("sgptowermetC1.b1", "19930721", "20260923")
```

The handbook's own note on data quality: 30-minute datastreams include QC flags: qc_temp, qc_rh, qc_vap_pres, qc_aspirator (west elevator 25m and 60m); qc_temp_25m, qc_rh_25m, qc_vap_pres_25m, qc_temp_60m, qc_rh_60m, qc_vap_pres_60m (southeast elevator). The aspirator QC flag is considered a nuisance flag and should not be reported in DQO assessment reports since aspirator status indication is unreliable/always shows "good" due to long cable lengths. Data Quality Reports (DQRs) are prepared and archived; monthly reviews were submitted to the Instrument Mentor Monthly Summary (IMMS) database until late 2014; beginning FY2006, DQRs...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Bent receiver brackets on SGP CF tower elevator | Loss of electronic connection between elevator carriage connector and tower receiver, resulting in data loss/gaps at that level | Maintenance by the installer required to fix | (hb p. 14) |
| Pre-September 1996 Qualimetrics RH probe miscalibration on west elevator | Significant periods of poor relative humidity measurements; incorrect conversion to engineering units in datalogger; RH data below ~90% corrected but no sensitivity above 90% RH | Switched to Vaisala HMP35D/HMP45D probes after September 1996; four-point calibration including checks above 90% RH | (hb p. 14) |
| West-side Vaisala probe high bias (August 2003) | RH bias ramping up to as much as 13% excess relative humidity at 60-meter west elevator after a few months | Probe replaced | (hb p. 14) |
| West vs southeast side temperature/RH differences due to solar heating and aspirator... | West-side temperatures slightly higher (up to ~1°C) and RH lower than southeast side during high solar/low wind conditions, especially summer; differences greater than 2°C temp or greater... | Use southeast side data preferentially; report large differences in DQ assessment | (hb p. 14) |
| West elevator 25m/60m datalogger connections reversed | From 19 May 1999 to 20 Sep 2000, 25-meter measurements recorded as 60-meter and vice versa in datastreams/files/fields; valid values but mislabeled heights, difficult to detect during... | Data reprocessed to correct levels; corrected data in ARM Archive (see DQR D001011.1) | (hb p. 14) |
| NSA tower rime ice buildup in winter | Blocking of T/RH probe inlets and interference with chilled mirror hygrometer and present weather detector measurements | Sonic anemometers are heated and do not accumulate rime ice | (hb p. 14) |
| SGP Okmulgee vulture roosting/bird droppings | Deterioration of radiometry, precipitation, sonic anemometry and other measurements | Bird spikes and rotating shafts installed, effective since early 2004 | (hb p. 15) |
| Original SGP Okmulgee tower booms difficult to operate | Operational difficulty affecting instrument deployment/servicing | New booms manufactured by Tower Systems, Inc. installed in 2003 | (hb p. 15) |
| Aspirator status diagnostic is not a reliable indicator | Aspirator status flag on west side always indicates aspirators working, even when not verifiable due to long cable lengths; QC aspirator flag may trip spuriously | Aspirator status/QC flag should be disregarded/not reported in DQ assessments; maintained only for datastream format continuity | (hb p. 6) |
| False aspirator status indication at high wind speed (pre-24 May 1996) | Wind speeds in excess of about 10 m/s produced false aspirator status indication | Aspiration limit value changed in CR10X programs so aspiration status is now continuously good | (hb p. 15) |
| Low battery voltage causing unreliable data | When datalogger battery voltage (vbat) is less than 10.5 volts, all measurements are unreliable | Consider data incorrect when vbat less than  10.5 V | (hb p. 17) |
| RH probe saturation hysteresis | RH probe saturated with moisture reads 98% or more for many hours; after persisting several hours, RH may read too high for as much as a day during recovery | Detect via comparison with other RH measurements on tower or with EBBR and SMOS measurements | (hb p. 18) |
| Vapor pressure lacks manufacturer-provided uncertainty | vap_pres values reported without dedicated accuracy; T and RH accuracies quoted instead since vapor pressure is calculated from T and RH | Use quoted T/RH accuracies as proxy | (hb p. 9) |
| High wind speed effect on radiation shield ventilation (West Elevator) | Wind speeds over 10 m/s, particularly from south, can reduce ventilation rate in radiation shield | Uncertainties thought negligible because radiation errors from shield heating are reduced in high winds | (hb p. 16) |
| Difficulty comparing tower T/RH with MET (E13) and EBBR | Large differences in measurements between MET/EBBR (~2m) and tower 25m/60m levels, especially when tower level is decoupled atmospherically from surface | Use caution; account for different vegetation surfaces and heights when comparing | (hb p. 12) |
| Difficulty comparing tower T/RH with SONDE | Large differences between SONDE and tower measurements when vertical gradients of T/RH are strong; SONDE sensors lag actual T/RH and SONDE may be horizontally displaced from tower at given... | Do not expect close agreement; account for lag and spatial offset | (hb p. 12) |
| Elevator carriage/receiver hardware or electronic problems | Elevator carriage connector fails to mate properly with tower receiver, causing incorrect measurements at that level, obvious when comparing data between the two tower sides | Report in DQ assessment if obvious | (hb p. 12) |
| DQRs not written for missing data or clear QC-flagged incorrect data (since FY2006) | Periods of missing or QC-flagged bad data lack corresponding DQR documentation | DQRs are instead written for tower-carriage-down periods when QC flags do not appear despite bad data | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Four-point relative humidity calibration (0%, 12%, 75%, 97%) above saturated salt solutions (12%, 75%), zero air (0%), and almost-saturated air (97%); PRTD checked for accuracy and electronics adjusted; PRTDs also calibrated annually by mentor with ice bath check in field; T and RH probes annually checked against each... (hb p. 18) |
| Calibration interval | Annual (calibration and probe replacement); previously NovaLynx calibrated at 12%, 40%, 75% before Sept 1996 (hb p. 18) |
| Traceability | Vaisala, Inc. performs annual sensor calibration since September 1996 (previously NovaLynx, Inc. for west elevator only) (hb p. 18) |
| Routine maintenance | In-field calibration checks, ice bath checks for PRTDs, aspirated psychrometer comparisons; tower structural inspection every two years by Tower Systems, Inc. (SGP CF and NSA) or by mentor (SGP Okmulgee) (hb p. 8) |
| Maintenance interval | Annual for sensor calibration/checks; biennial for tower structural inspection (hb p. 8) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MET (Surface Meteorological Instrumentation), EBBR (Energy Balance Bowen Ratio), SONDE, ECOR (Eddy Correlation System), SIRS (Solar and Infrared Station), TWRMR (VAP), RLPROF/RLPROFMR (VAP), QMEAERIPROF (QME).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `T/RH/VP` | Temperature/Relative Humidity/Vapor Pressure |
| `PRTD` | Platinum Resistance Temperature Detector |
| `RMSE` | Root-mean-square error, defined as vector sum of bias error B and variance V: RMSE = (B^2... |
| `Uncertainty` | Range of probable maximum deviation of a measured value from the true value within a 95%... |
| `CF` | Central Facility |
| `CO2FLX` | Carbon Dioxide Flux Measurement System |
| `DQ` | Data Quality |
| `DQ Explorer` | Data Quality Explorer |
| `ECOR` | Eddy Correlation System |
| `GPS` | global positioning system |
| `MFR` | Multi-Filter Radiometer |
| `NSA` | North Slope of Alaska |
| `PGS` | precision gas system |
| `RMS` | root mean square |


### References the handbook cites

- Revercomb, HE, DD Turner, DC Tobin, RO Knuteson, WF Feltz, J Barnard, J Bosenberg, S Clough, D Cook, R Ferrare, J Goldsmith, S Gutman, R Halthore, B Lesht, J Liljegren, H Linne, J Michalsky, V Morris, W Porch, S...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/twr_handbook.pdf (30 pages, DOE/SC-ARM/TR-050, by D R Cook)
- Catalog record: ARM data-source index, `instrument_class_code=twr`, read 2026-09-23
- Example file: `sgptowermetC1.b1.20260919.000000.nc` from `sgptowermetC1.b1`, 0.3 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
