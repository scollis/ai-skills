---
name: arm-instrument-marinemet
description: ARM Marine Surface Meteorological Instrumentation (marinemet) - handbook-derived instrument reference. Measurement principle, reported quantities (Pressure, Relative humidity, Temperature, Relative humidity, Temperature, Radiation error, Wind speed, Wind direction), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (magmarinemet1sM1.b1) and the variable inventory of a real file. Use when working with marinemet data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - marinemet, Marine Surface Meteorological Instrumentation, magmarinemet1sM1.b1, Pressure, Relative humidity, Temperature, Radiation error, Surface Meteorology, Vaisala PTB330 Barometer, Vaisala HMP155 Humidity and Temperature Probe, AOSMET, TBRG.
---

# MARINEMET - Marine Surface Meteorological Instrumentation

The MET system is a suite of surface instruments (barometer, temperature/RH probe, wind monitor, present weather/visibility detector, and rain gauges) deployed at ARM fixed sites and the ARM Mobile Facilities (AMF1, AMF2, AMF3) to record standard surface meteorological measurements; the handbook notes that instrumentation varies slightly by site or mobile-facility deployment and gives AMF2 its own change-history section (hb p. 13), where a tipping bucket rain gauge is described as added "for land-based deployments" - the only place the document distinguishes AMF2 land from non-land platforms.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `marinemet` |
| Handbook | [DOE/SC-ARM-TR-086 / J Kyrouac, M Tuftedal / June 2024](https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala PTB330 Barometer; Vaisala HMP155 Humidity and Temperature Probe; Vaisala HMT337 Humidity and Temperature Transmitter; RM Young 43502/43408 Aspirated Radiation Shield; RM Young 05103/05106... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation |
| Record | 2012-10-05 to 2018-03-23 (retired) |
| Datastreams with data | 3 across 2 sites |
| Sites | mag, mar |
| ARM page | https://www.arm.gov/capabilities/instruments/marinemet |


## Credit

Everything this skill knows about the instrument is the work of **J Kyrouac, M Tuftedal** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Kyrouac, M Tuftedal. *Surface Meteorological System (MET) Instrument Handbook*, DOE/SC-ARM-TR-086, June 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `marinemet`, ARM links no handbook to this class. The facts below come from the **Surface Meteorological Instrumentation** (`met`) handbook, which documents the parent system. The same document also covers `metwxt`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `marinemet` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

Pressure is measured using a Vaisala proprietary BAROCAP silicon capacitive absolute sensor whose microprocessor corrects for linearity and temperature dependence. Temperature is measured with a Pt100 resistive platinum sensor and relative humidity with a Vaisala proprietary HUMICAP capacitive thin film polymer sensor, housed in an aspirated radiation shield to reduce solar heating error. Wind speed and direction are measured either mechanically, with a helicoid four-blade propeller producing an AC sine wave signal proportional to wind speed and a potentiometer producing a voltage proportional to vane position, or ultrasonically, by measuring transit time of pulses between transducers with no moving parts. Visibility and present weather are sensed using light-scattering principles combined with a capacitive RAINCAP rain sensor, where precipitation intensity is derived from the amplitude of rapid signal changes and the ratio of water equivalence to volume determines precipitation type. Precipitation amount is measured by tipping bucket mechanisms (magnetic reed switch tip counting) or by optical rain gauges that translate scintillation intensity of an infrared beam into precipitation rate and type.

**Siting.** Measurements are taken at standard heights following WMO guidelines: barometer at 1 meter (inside electronics enclosure, with pressure port routed via silicon tube/outside inlet at some sites), temperature/RH sensor at 2 meters mounted on a crossarm in an aspirated radiation shield, wind sensor at standard 10 meters (though historically mounted at 3m, 6m, or 12m at some AMF1/ENA deployments), and present weather/optical rain gauge instruments mounted on tripod or crossarm at 2-3 meters (moved to separate tripod mountings from the 10m tower beginning in 2011/2014 at some sites). Slight variations in instrumentation and siting exist depending on site or mobile facility deployment, including...

**Sampling.** native rate once a minute; reported every raw data collected once a minute; processed into a daily quality-flagged file (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Pressure | hPa | 500-1100 hPa | ± 0.15 hPa (total accuracy) | - | (hb p. 7) |
| Relative humidity (HMP155) | % RH | 0-100% | ± (1.0 + 0.008 x reading) % RH (at -20-40°C) | - | (hb p. 7) |
| Temperature (HMP155) | °C | -80-60°C | ± (0.1 + 0.00167 x /temperature/) °C | - | (hb p. 7) |
| Relative humidity (HMT337) | % RH | 0-100% | ± 1 % RH (at 0-90 % RH, 15-25°C); ± 1.7 % RH... | - | (hb p. 7) |
| Temperature (HMT337) | °C | -70-180°C | ± 0.1°C | - | (hb p. 7) |
| Radiation error (RM Young 43502 shield) | °C RMS | - | 0.2°C RMS at 1000 W/m2 intensity | - | (hb p. 7) |
| Wind speed (RM Young 05103/05106) | m/s | 0-100 m/s | ± 0.3 m/s, or 1% of reading, whichever is... | - | (hb p. 8) |
| Wind direction (RM Young 05103/05106) | degrees | 0°-360° | ± 3° | - | (hb p. 8) |
| Wind speed (Vaisala WMT700) | m/s | 0-75 m/s | ± 0.1 m/s or 2% of reading, whichever is greater | - | (hb p. 8) |
| Wind direction (Vaisala WMT700) | degrees | 0-360° | ± 2° | - | (hb p. 8) |
| Visibility (PWD22) | m | 0-20000 m | ± 10% (at 10-10000 m); ± 20% (at 10000-20000 m) | - | (hb p. 8) |
| Precipitation intensity (PWD22) | mm | 0-999.99 mm | none listed | - | (hb p. 8) |
| Precipitation amount (PWD22) | mm | 0-99.99 mm | none listed | - | (hb p. 8) |
| Snow (PWD22) | mm | 0-999 mm | none listed | - | (hb p. 8) |
| Precipitation accuracy (Novalynx TBRG) | % | - | ± 1% (at 1-3 in/hr); ± 3% (at 0-6 in/hr) | - | (hb p. 8) |
| Precipitation intensity (ORG-815-DS) | mm/hr | 0.1-500 mm/hr | - | - | (hb p. 8) |
| Precipitation accumulation (ORG-815-DS) | mm | 0.001-999.999 mm | ± 5% accumulation | - | (hb p. 8) |
| Snow intensity (ORG-815-DS) | mm/hr, liquid equivalent | 0.01-50 mm/hr | ± 10% | - | (hb p. 8) |
| Snow accumulation (ORG-815-DS) | mm, liquid equivalent | 0.001-999.999 mm | ± 10% | - | (hb p. 8) |


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
| Vaisala HMT337 RH accuracy at 15-25°C | ± 1 % RH (0-90% RH); ± 1.7 % RH (90-100% RH) | (hb p. 7) |
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
| Vaisala PWD22 Visibility accuracy | ± 10% (10-10000 m); ± 20% (10000-20000 m) | (hb p. 8) |
| Vaisala PWD22 Precipitation intensity range | 0-999.99 mm | (hb p. 8) |
| Vaisala PWD22 Precipitation amount range | 0-99.99 mm | (hb p. 8) |
| Vaisala PWD22 Snow range | 0-999 mm | (hb p. 8) |
| Vaisala PWD22 Precipitation accuracy | none listed | (hb p. 8) |


_12 further specification rows are in the handbook._

## The data

Verified example: **`magmarinemet1sM1.b1`**, file `magmarinemet1sM1.b1.20131006.000000.cdf`
(24.56 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=86400 |
| Data variables | 72 |
| QC variables | 34 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2013-10-06T00:00:00 to 2013-10-06T23:59:59 |
| dod version | marinemet1s-b1-1.3 |
| process version | ingest-marinemet-1.6-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `air_temp_adc` | volt | time | yes | Air temperature from the T/RH sensor in a forced ventilator (Young... |
| `air_temp_wx1` | degC | time | yes | Air temperature from passive shield of the instrument mounted on the... |
| `air_temp_wx2` | degC | time | yes | Air temperature from passive shield of the instrument mounted on the... |
| `bar_pressure_wx1` | hPa | time | yes | Barometric pressure from the instrument mounted on the port side of... |
| `bar_pressure_wx2` | hPa | time | yes | Barometric pressure from the instrument mounted on the starboard side... |
| `cog_gps` | degTrue | time | yes | Course over ground (True) from the GPS receiver |
| `cog_nav` | degTrue | time | yes | Course over ground (True) from the NAV system |
| `hdg_nav` | degrees | time | yes | Heading of the ship bow from the NAV system |
| `lat_gps` | degree_N | time | yes | North latitude from the GPS receiver |
| `lat_nav` | degree_N | time | yes | North latitude, float point, positive is north hemisphere, from the... |
| `lon_gps` | degree_E | time | yes | East longitude from the GPS receiver |
| `lon_nav` | degree_E | time | yes | East longitude, float point, positive for E longitude, from the NAV... |
| `pitch_nav` | degrees | time | yes | Pitch (bow up) from the NAV system |
| `pitch_tcm` | degrees | time | yes | Pitch (bow up) from the TCM sensor mounted in the MET DAQ enclosure |
| `rain_intensity_org` | mm/hr | time | yes | Rain intensity from the OSI ORG instrument mounted on the met boom |
| `rain_intensity_wx1` | mm/hr | time | yes | Rain intensity from the instrument mounted on the port side of the... |
| `rain_intensity_wx2` | mm/hr | time | yes | Rain intensity from the instrument mounted on the starboard side of... |
| `rh_adc` | volt | time | yes | Relative humidity from the T/RH sensor in a forced ventilator (Young... |
| `rh_wx1` | % | time | yes | Relative humidity from passive shield of the instrument mounted on... |
| `rh_wx2` | % | time | yes | Relative humidity from passive shield of the instrument mounted on... |
| `roll_nav` | degrees | time | yes | Roll (port up) from the NAV system |
| `roll_tcm` | degrees | time | yes | Roll (port up) from the TCM sensor mounted in the MET DAQ enclosure |
| `siphon_rain_gauge_adc` | volt | time | yes | Siphon rain gauge, measures total rain fall up to 50 mm then the... |
| `sog_gps` | kts | time | yes | Speed over ground from the GPS receiver |
| `sog_nav` | kts | time | yes | Speed over ground from the NAV system |
| `tachometer_voltage_adc` | volt | time | yes | Tachometer from the aspirator, indicates aspirator fan is operating |
| `time` | - | time | yes | Time offset from midnight |
| `var_gps` | degree | time | yes | Local magnetic variation from the GPS receiver |
| `wdir_adc` | volt | time | yes | Wind direction measured by the wind monitor mounted at the peak of... |
| `wdir_wx1` | degree | time | yes | Apparent wind direction from the instrument mounted on the port side... |


_4 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("magmarinemet1sM1.b1", "2013-10-06", "2013-10-06")
ds = armlive_open("magmarinemet1sM1.b1", "2013-10-06", "2013-10-06", cleanup_qc=True)
```

This datastream carries 72 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("magmarinemet1sM1.b1", start, end,
                  keep_variables=["air_temp_adc", "air_temp_wx1", "air_temp_wx2", "qc_air_temp_adc", "qc_air_temp_wx1", "qc_air_temp_wx2"])
```

## Quality control in this datastream

34 `qc_` companion variables cover 33 of the
72 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (magmarinemet1sM1.b1.20131006.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sog_gps` | Value is equal to missing_value. | 69162 | 80.0486 |
| `lat_gps` | Value is equal to missing_value. | 69162 | 80.0486 |
| `lon_gps` | Value is equal to missing_value. | 69162 | 80.0486 |
| `var_gps` | Value is equal to missing_value. | 69162 | 80.0486 |
| `cog_gps` | Value is equal to missing_value. | 69161 | 80.0475 |
| `rain_intensity_org` | Value is equal to missing_value. | 69120 | 80.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("magmarinemet1sM1.b1", "20121005", "20260924")
```

The handbook's own note on data quality: Data Quality Reports (DQRs) are provided with MET data downloads for specified times/variables where data quality may have been compromised (e.g., instrument problems, power outages, calibration issues, environmental events). These events are not necessarily flagged by automated QC variables, so DQRs should be viewed before using data; suggestions for use are often included and discretion can be applied. PWD communication interruption values are flagged by QC and should be removed from study. Information on variables and data quality flags can be found in the file headers.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| HMP45 cold bias in high humidity | Temperature readings show a cold bias under high relative humidity conditions; also potential drift in RH readings over time | See technical report DOE/SC-ARM-TR-192 outlining these issues; sensor was later upgraded to HMP155D | (hb p. 16) |
| Ultrasonic wind sensor data dropouts or spikes | Wind data show dropouts or spikes due to transducer interference, typically during heavy wet snow, ice conditions, or bird interference | - | (hb p. 16) |
| Optical rain gauge unsuitable for solid precipitation | Optical rain gauge precipitation data is unreliable/inaccurate during snow events | Use heated tipping bucket or present weather detector precipitation data instead during snow | (hb p. 16) |
| Optical rain gauge overestimation in light/transitional rain and fog/humidity sensitivity | Small precipitation events reported that may be spurious, especially in light or transitional rain, fog, or high humidity conditions | Cross-reference precipitation data with other sensors (TBRG, PWD, etc.) to verify validity | (hb p. 16) |
| Chilled mirror hygrometer (CMH) daily self-check artifact | Spike/drop in relative humidity and dew point data occurring once daily due to mirror self-check | Compare with HMT337 data to verify readings, though usually obvious on a time series plot | (hb p. 16) |
| CMH delayed operating temperature after self-check | Mirror occasionally takes longer than the typical few minutes to return to normal operating temperature after self-check, visible as an extended anomaly in RH/dew point data | Compare with HMT337 data to verify readings are similar | (hb p. 16) |
| Present weather detector (PWD) communication interruption | Sensor serial number momentarily reported as rain rate value in the data | These values are flagged by QC and should be removed from study | (hb p. 16) |
| Chilled mirror hygrometer poor performance in arctic conditions | Degraded/unreliable hygrometer performance leading to its removal from the datastream | CMH (TSL-1088) was removed from NSA and AMF3-Oliktok deployments in late 2019 | (hb p. 13) |
| Optical rain gauge poor performance in arctic conditions | Unreliable precipitation measurement in arctic climate | Optical rain gauge was removed from NSA MET datastream in late 2003 | (hb p. 14) |
| Non-standard wind sensor mounting heights at some historical AMF1/ENA deployments | Wind speed/direction values not comparable to standard 10 m height record; discontinuities when height changes (e.g., PYE/NIM at 3m, COR at 12m, ENA at 6m until Feb 24 2014) | - | (hb p. 12) |
| Pressure not corrected to sea level | Reported pressure values represent station pressure at instrument altitude (1m above ground level), not sea-level-reduced pressure | - | (hb p. 18) |
| Snow measurement performance issues with ORG-815-DS | Snow intensity/accumulation values from optical rain gauge unreliable | This instrument is not typically used for snow due to performance issues | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field-checked using transfer standard equipment or field calibration kits; instruments replaced/adjusted if out of tolerance and sent to manufacturer for calibration; TBRG dynamically calibrated by comparing known rain rates prior to installation, calibration coefficients applied in data logger program (hb p. 15) |
| Calibration interval | Pressure: every 6 months (also at install/removal). HMP155: every 6 months (also at install/removal). HMT337: yearly (also at installation). Wind (RM Young): every 6 months. WMT700: none required. PWD22: yearly (also at installation). TBRG: every 6 months (also at installation). ORG-815-DS: none required. (hb p. 15) |
| Routine maintenance | Daily: live data checked on remote display to verify communications, updating data, and absence of errors/dropouts/flatlines. Biweekly: instruments, cabling, mountings, and electronics inspected for physical damage, obstructions, and cleanliness; tip test performed on tipping bucket rain gauges. (hb p. 14) |
| Maintenance interval | Daily and biweekly (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AOSMET.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AC` | alternating current |
| `AMF1` | ARM Mobile Facility 1 |
| `AMF2` | ARM Mobile Facility 2 |
| `AMF3` | ARM Mobile Facility 3 |
| `AOSMET` | Aerosol Observing System Meteorological Sensor |
| `ARM` | Atmospheric Radiation Measurement |
| `CMH` | chilled mirror hygrothermometer |
| `DQO` | Data Quality Office |
| `DQR` | Data Quality Report |
| `ENA` | Eastern North Atlantic |
| `MET` | surface meteorological system |
| `NSA` | North Slope of Alaska |
| `OLI` | Oliktok Point |
| `ORG` | optical rain gauge |


### References the handbook cites

- Kyrouac, J, and A Theisen. 2018. Biases of the MET Temperature and Relative Humidity Sensor (HMP45) Report. ARM Climate Research Facility. DOE/SC-ARM-TR-192, https://doi.org/10.2172/1366737
- World Meteorological Organization. 2008. Guide to Meteorological Instruments and Methods of Observation (Seventh Edition). WMO-No. 8.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf (20 pages, DOE/SC-ARM-TR-086, by J Kyrouac, M Tuftedal)
- Catalog record: ARM data-source index, `instrument_class_code=marinemet`, read 2026-09-24
- Example file: `magmarinemet1sM1.b1.20131006.000000.cdf` from `magmarinemet1sM1.b1`, 24.56 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
