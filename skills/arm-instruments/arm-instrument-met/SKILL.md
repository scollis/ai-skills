---
name: arm-instrument-met
description: ARM Surface Meteorological Instrumentation (met) - handbook-derived instrument reference: measurement principle, reported quantities (Pressure, Relative Humidity, Temperature, Relative Humidity, Temperature, Wind Speed, Wind Direction, Wind Speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsametC1.b1) and the variable inventory of a real file. Use when working with met data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface Meteorology. Triggers - met, Surface Meteorological Instrumentation, nsametC1.b1, Pressure, Relative Humidity, Temperature, Wind Speed, Surface Meteorology, Vaisala PTB330 Barometer, Vaisala HMP155 Humidity and Temperature Probe, AOSMET, TBRG.
---

# MET - Surface Meteorological Instrumentation

The MET system uses a suite of conventional in situ sensors deployed at standard heights following WMO guidelines to record once-a-minute surface meteorological measurements of temperature, relative humidity, pressure, wind speed and direction, precipitation, and (at most locations) visibility and present weather.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `met` |
| Handbook | [DOE/SC-ARM-TR-086 / J Kyrouac, M Tuftedal / June 2024](https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala PTB330 Barometer; Vaisala HMP155 Humidity and Temperature Probe; Vaisala HMT337 Humidity and Temperature Transmitter; RM Young 43502 Aspirated Radiation Shield; RM Young 05103/05106 Wind... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation; Visibility |
| Record | 1993-06-29 to 2026-09-22 (active) |
| Datastreams with data | 69 across 29 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/met |


## Credit

Everything this skill knows about the instrument is the work of **J Kyrouac, M Tuftedal** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Kyrouac, M Tuftedal. *Surface Meteorological System (MET) Instrument Handbook*, DOE/SC-ARM-TR-086, June 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Atmospheric pressure is measured using a Vaisala proprietary BAROCAP silicon capacitive absolute sensor with microprocessor correction for linearity and temperature dependence. Temperature is measured with a Pt100 resistive platinum sensor and humidity with the Vaisala proprietary HUMICAP capacitive thin film polymer sensor, or via a warmed-probe transmitter that prevents saturation at high humidity. Wind speed is measured with a helicoid four-blade propeller producing an AC sine wave signal proportional to wind speed, with wind direction transmitted via a potentiometer producing an output voltage proportional to vane position; ultrasonic sensors alternatively measure transit time of pulses between transducers with no moving parts. Visibility and present weather are sensed using light-scattering principles combined with a capacitive RAINCAP rain sensor, with precipitation intensity calculated from the amplitude of rapid signal changes. Precipitation is measured via a tipping bucket mechanism (magnetic reed switch registering discrete tips) or an optical rain gauge that translates scintillation intensity of an infrared beam into precipitation rate and type.

**Siting.** Measurements are taken once a minute at standard heights following WMO guidelines (WMO 2008): barometer at 1 meter inside the electronics enclosure, temperature/humidity probe at 2 meters in an aspirated radiation shield on a crossarm, wind sensor at standard 10 meters, and visibility/present weather and precipitation sensors mounted on a tripod or crossarm at 2-3 meters. Slight variations exist depending on site or mobile facility deployment (e.g., wind sensor mounted at 3m during PYE/NIM, 12m during COR, 6m at ENA until Feb 24, 2014). Pressure is measured at 1m above ground-level (station pressure) and is not corrected for sea level.

**Sampling.** native rate once a minute; reported every 1-minute statistics; daily quality-flagged file; averaging raw data once a minute processed into daily quality-flagged file (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Pressure | hPa | 500-1100 hPa | ± 0.15 hPa (total accuracy) | - | (hb p. 7) |
| Relative Humidity (HMP155) | % RH | 0-100% | ± (1.0 + 0.008 x reading) % RH (at -20-40°C) | - | (hb p. 7) |
| Temperature (HMP155) | °C | -80-60°C | ± (0.1 + 0.00167 x /temperature/) °C | - | (hb p. 7) |
| Relative Humidity (HMT337) | % RH | 0-100% | ± 1 % RH (at 0-90 % RH, 15-25°C); ± 1.7 % RH... | - | (hb p. 7) |
| Temperature (HMT337) | °C | -70-180°C | ± 0.1°C | - | (hb p. 7) |
| Wind Speed (RM Young 05103/05106) | m/s | 0-100 m/s | ± 0.3 m/s, or 1% of reading, whichever is... | - | (hb p. 8) |
| Wind Direction (RM Young 05103/05106) | degrees | 0°-360° | ± 3° | - | (hb p. 8) |
| Wind Speed (Vaisala WMT700) | m/s | 0-75 m/s | ± 0.1 m/s or 2% of reading, whichever is greater | - | (hb p. 8) |
| Wind Direction (Vaisala WMT700) | degrees | 0-360° | ± 2° | - | (hb p. 8) |
| Visibility (PWD22) | m | 0-20000 m | ± 10% (at 10-10000 m); ± 20% (at 10000-20000 m) | - | (hb p. 8) |
| Precipitation Intensity (PWD22) | mm | 0-999.99 mm | none listed | - | (hb p. 8) |
| Precipitation Amount (PWD22) | mm | 0-99.99 mm | none listed | - | (hb p. 8) |
| Snow (PWD22) | mm | 0-999 mm | none listed | - | (hb p. 8) |
| Precipitation (Novalynx TBRG) | in/hr | - | ± 1% (at 1 - 3 in/hr); ± 3% (at 0 – 6 in/hr) | 0.254 mm per tip | (hb p. 8) |
| Precipitation Intensity (ORG-815-DS) | mm/hr | 0.1-500 mm/hr | - | - | (hb p. 8) |
| Precipitation Accumulation (ORG-815-DS) | mm | 0.001-999.999 mm | ± 5% accumulation | - | (hb p. 8) |
| Snow Intensity (ORG-815-DS) | mm/hr, liquid equivalent | 0.01-50 mm/hr, liquid equivalent | ± 10% | - | (hb p. 8) |
| Snow Accumulation (ORG-815-DS) | mm, liquid equivalent | 0.001-999.999 mm, liquid equivalent | ± 10% | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Vaisala PTB330 Barometer Range | 500-1100 hPa | (hb p. 7) |
| Vaisala PTB330 Barometer Total accuracy | ± 0.15 hPa | (hb p. 7) |
| Vaisala HMP155 RH range | 0-100% | (hb p. 7) |
| Vaisala HMP155 RH accuracy (at -20-40°C) | ± (1.0 + 0.008 x reading) % RH | (hb p. 7) |
| Vaisala HMP155 Temperature range | -80-60°C | (hb p. 7) |
| Vaisala HMP155 Temperature accuracy | ± (0.1 + 0.00167 x /temperature/) °C | (hb p. 7) |
| Vaisala HMT337 RH range | 0-100% | (hb p. 7) |
| Vaisala HMT337 RH accuracy at 15-25°C | ± 1 % RH (at 0-90 % RH), ± 1.7 % RH (at 90-100 % RH) | (hb p. 7) |
| Vaisala HMT337 RH accuracy at -20-40°C | ± (1.0 + 0.008 x reading) % RH | (hb p. 7) |
| Vaisala HMT337 Temperature range | -70-180°C | (hb p. 7) |
| Vaisala HMT337 Temperature accuracy | ± 0.1°C | (hb p. 7) |
| RM Young 43502 Aspirated Radiation Shield Radiation error | 0.2°C RMS at 1000 W/m2 intensity | (hb p. 7) |
| RM Young 05103/05106 Wind speed range | 0-100 m/s | (hb p. 8) |
| RM Young 05103/05106 Wind speed accuracy | ± 0.3 m/s, or 1% of reading, whichever is greater | (hb p. 8) |
| RM Young 05103/05106 Wind direction range | 0°-360° | (hb p. 8) |
| RM Young 05103/05106 Wind direction accuracy | ± 3° | (hb p. 8) |
| Vaisala WMT700 Wind speed range | 0-75 m/s | (hb p. 8) |
| Vaisala WMT700 Wind speed accuracy | ± 0.1 m/s or 2% of reading, whichever is greater | (hb p. 8) |
| Vaisala WMT700 Wind direction range | 0-360° | (hb p. 8) |
| Vaisala WMT700 Wind direction accuracy | ± 2° | (hb p. 8) |
| Vaisala PWD22 Visibility range | 0-20000 m | (hb p. 8) |
| Vaisala PWD22 Visibility accuracy | ± 10% (at 10-10000 m), ± 20% (at 10000-20000 m) | (hb p. 8) |
| Vaisala PWD22 Precipitation Intensity range | 0-999.99 mm | (hb p. 8) |
| Vaisala PWD22 Precipitation Amount range | 0-99.99 mm | (hb p. 8) |
| Vaisala PWD22 Snow range | 0-999 mm | (hb p. 8) |
| Vaisala PWD22 Precipitation accuracy | none listed | (hb p. 8) |


_7 further specification rows are in the handbook._

## The data

Verified example: **`nsametC1.b1`**, file `nsametC1.b1.20260922.000000.cdf`
(0.38 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 59 |
| QC variables | 23 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-22T00:00:00 to 2026-09-22T23:59:00 |
| sampling interval | variable, see instrument handbook |
| averaging interval | 60 seconds |
| dod version | met-b1-6.4 |
| process version | ingest-met-4.59-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `atmos_pressure` | kPa | time | yes | Atmospheric pressure |
| `cmh_dew_point` | degC | time | yes | CMH dew point |
| `cmh_rh` | % | time | yes | CMH relative humidity, calculated |
| `cmh_sat_vapor_pressure` | kPa | time | yes | CMH saturation vapor pressure, calculated |
| `cmh_temp` | degC | time | yes | CMH temperature |
| `cmh_vapor_pressure` | kPa | time | yes | CMH vapor pressure, calculated |
| `dew_point_mean` | degC | time | yes | Dew point mean, calculated |
| `logger_temp` | degC | time | yes | Logger temperature |
| `logger_volt` | V | time | yes | Logger voltage |
| `pwd_cumul_rain` | mm | time | yes | PWD cumulative liquid precipitation |
| `pwd_cumul_snow` | mm | time | yes | PWD cumulative snow |
| `pwd_mean_vis_10min` | m | time | yes | PWD 10 minute mean visibility |
| `pwd_mean_vis_1min` | m | time | yes | PWD 1 minute mean visibility |
| `pwd_precip_rate_mean_1min` | mm/hr | time | yes | PWD 1 minute mean precipitation rate |
| `pwd_pw_code_15min` | 1 | time | yes | PWD 15 minute present weather code |
| `pwd_pw_code_1hr` | 1 | time | yes | PWD 1 hour present weather code |
| `pwd_pw_code_inst` | 1 | time | yes | PWD instantaneous present weather code |
| `rh_mean` | % | time | yes | Relative humidity mean |
| `temp_mean` | degC | time | yes | Temperature mean |
| `vapor_pressure_mean` | kPa | time | yes | Vapor pressure mean, calculated |
| `wdir_vec_mean` | degree | time | yes | Wind direction vector mean |
| `wspd_arith_mean` | m/s | time | yes | Wind speed arithmetic mean |
| `wspd_vec_mean` | m/s | time | yes | Wind speed vector mean |
| `dew_point_std` | degC | time | - | Dew point standard deviation |
| `pwd_err_code` | 1 | time | - | PWD alarm |
| `rh_std` | % | time | - | Relative humidity standard deviation |
| `temp_std` | degC | time | - | Temperature standard deviation |
| `time` | - | time | - | Time offset from midnight |
| `trh_err_code` | 1 | time | - | Temperature and relative humidity sensor error code |
| `vapor_pressure_std` | kPa | time | - | Vapor pressure standard deviation |


_1 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsametC1.b1", "2026-09-22", "2026-09-22")
ds = armlive_open("nsametC1.b1", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

This datastream carries 59 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("nsametC1.b1", start, end,
                  keep_variables=["atmos_pressure", "cmh_dew_point", "cmh_rh", "qc_atmos_pressure", "qc_cmh_dew_point", "qc_cmh_rh"])
```

## Quality control in this datastream

23 `qc_` companion variables cover 23 of the
59 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (nsametC1.b1.20260922.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cmh_temp` | Value is equal to missing_value. | 1440 | 100.0 |
| `cmh_dew_point` | Value is equal to missing_value. | 1440 | 100.0 |
| `cmh_sat_vapor_pressure` | Value is equal to missing_value. | 1440 | 100.0 |
| `cmh_vapor_pressure` | Value is equal to missing_value. | 1440 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsametC1.b1", "19930629", "20260923")
```

The handbook's own note on data quality: Data Quality Reports (DQRs) are provided with MET data downloads for specified times/variables where data quality may have been compromised (e.g., instrument problems, power outages, calibration issues, known environmental events). These events are not necessarily flagged by automated QC variables, so DQRs should be reviewed before using data; suggestions for use are often included and discretion can be used on how to proceed. PWD communication-interruption values (serial number reported as rain rate) are flagged by QC and should be removed from study. Raw and corrected tipping bucket rain...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Cold bias in high humidity for HMP45 sensors (SGP, ~2007-2018) | Temperature/RH readings show cold bias when humidity is high; possible drift in relative humidity readings | See technical report DOE/SC-ARM-TR-192 for details | (hb p. 16) |
| Ultrasonic wind sensor dropouts/spikes due to transducer interference | Occasional wind data dropouts or spikes, typically during heavy wet snow or ice conditions; can also be caused by bird interference | - | (hb p. 16) |
| Optical rain gauge unsuited for solid precipitation | Poor/erratic measurement of snow events | Use heated tipping bucket or present weather detector precipitation data instead during snow | (hb p. 16) |
| Optical rain gauge overestimation of precipitation | Overestimated precipitation especially in light or transitional rain conditions; sensitive to fog or high humidity, reported as small precipitation events | Cross-reference precipitation data with other sensors (TBRG, PWD, etc.) to verify validity | (hb p. 16) |
| Chilled mirror hygrometer (CMH) daily self-check spike/drop | Spike/drop evident in relative humidity and dew point data at a consistent daily time | Compare with HMT337 data if the self-check anomaly is unclear on a time series plot | (hb p. 16) |
| CMH delayed operating temperature after self-check | Mirror takes more than the typical few minutes to reach normal operating temperature, visible as extended anomaly in RH/dew point after the daily self-check | Compare with HMT337 data to verify readings are similar | (hb p. 16) |
| PWD communication interruption reporting serial number as rain rate | Sensor serial number momentarily reported as rain rate value, appearing as an anomalous spike in precipitation data | These values are flagged by QC and should be removed from study | (hb p. 16) |
| Chilled mirror hygrometer (TSL-1088) poor performance in arctic conditions | Degraded/unreliable RH and dew point measurements at NSA and AMF3-Oliktok | Removed from deployment (NSA and OLI, late 2019) | (hb p. 13) |
| Optical rain gauge poor performance in arctic conditions (NSA) | Unreliable precipitation measurement at NSA | Removed from NSA MET datastream in late 2003 | (hb p. 14) |
| Historical siting variations in wind sensor mounting height | Wind speed/direction values reflect non-standard mounting heights (3m at PYE/NIM, 12m at COR, 6m at ENA until Feb 24 2014) rather than standard 10m, affecting comparability across sites/time | Documented in Section 3.0 historical background; check site/period before comparing wind data across deployments | (hb p. 12) |
| Instrument/model changes over time at each site | Step-changes or discontinuities in data characteristics coinciding with instrument upgrades (e.g., PTB220 to PTB330, HMP45D to HMP155D, WS425 to WMT700) | Refer to Historical Background (Section 3.0) for dates/details of changes at each site | (hb p. 12) |
| Precipitation datastream reorganization | Tipping bucket or optical rain gauge data found in separate datastreams (e.g., raintb, sgporgC1) prior to certain dates rather than in main MET datastream | Check historical background for datastream location by date/site | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field-checked using transfer standard equipment or field calibration kit; if out of tolerance, instrument is replaced/adjusted and sent back to manufacturer for calibration (hb p. 15) |
| Calibration interval | Every 6 months (pressure, HMP155, wind monitor, TBRG); Yearly (HMT337, PWD22); None required (WMT700, ORG-815-DS) (hb p. 15) |
| Traceability | Manufacturer calibration upon replacement (hb p. 15) |
| Routine maintenance | Daily: live data checked on remote display to verify communications, updating data, and no errors/dropouts/flatlines. Biweekly: instruments, cabling, mountings, and electronics inspected for physical damage, obstructions, and cleanliness; tip test performed on tipping bucket rain gauges. (hb p. 14) |
| Maintenance interval | Daily and Biweekly (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AOSMET (Aerosol Observing System Meteorological Sensor).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AC` | alternating current |
| `AMF1` | ARM Mobile Facility 1 |
| `AMF2` | ARM Mobile Facility 2 |
| `AMF3` | ARM Mobile Facility 3 |
| `ANX` | Andenes, Norway (AMF1) |
| `AOSMET` | Aerosol Observing System Meteorological Sensor |
| `ARM` | Atmospheric Radiation Measurement |
| `ASI` | Ascension Island, South Atlantic Ocean (AMF1) |
| `BNF` | Bankhead National Forest, Alabama, United States (AMF3) |
| `CMH` | chilled mirror hygrothermometer |
| `COR` | Cordoba, Argentina (AMF1) |
| `DQO` | Data Quality Office |
| `DQR` | Data Quality Report |
| `EF` | Extended Facility |


### References the handbook cites

- Kyrouac, J, and A Theisen. 2018. Biases of the MET Temperature and Relative Humidity Sensor (HMP45) Report. ARM Climate Research Facility. DOE/SC-ARM-TR-192, https://doi.org/10.2172/1366737
- World Meteorological Organization. 2008. Guide to Meteorological Instruments and Methods of Observation (Seventh Edition). WMO-No. 8.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf (20 pages, DOE/SC-ARM-TR-086, by J Kyrouac, M Tuftedal)
- Catalog record: ARM data-source index, `instrument_class_code=met`, read 2026-09-23
- Example file: `nsametC1.b1.20260922.000000.cdf` from `nsametC1.b1`, 0.38 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
