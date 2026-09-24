---
name: arm-instrument-gustprobe-air
description: ARM Gust Probe aboard aircraft (gustprobe-air) - handbook-derived instrument reference: measurement principle, reported quantities (Temperature, Humidity, Barometric pressure, u_w - North wind component, v_w - East wind component, w_w - Vertical wind component, GPS latitude, GPS longitude), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafgust1hzF1.a1) and the variable inventory of a real file. Use when working with gustprobe-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations. Triggers - gustprobe-air, Gust Probe aboard aircraft, sgpaafgust1hzF1.a1, Temperature, Humidity, Barometric pressure, u_w - North wind component, v_w - East wind component, w_w - Vertical wind component, Airborne Observations, Aventech Research Inc., AIMMS-20, AIMMS, NAVMET-AIR, ODMS.
---

# GUSTPROBE-AIR - Gust Probe aboard aircraft

The AIMMS-20 is a 5-port hemispheric gust probe mounted on the front of the ARM G-1 aircraft that measures platform position, velocity, attitude, ambient temperature, static pressure, and differential pressures to compute ambient three-dimensional winds.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 13 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gustprobe-air` |
| Handbook | [DOE/SC-ARM-TR-260 / A Matthews, L Goldberger / November 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf) |
| Measurement category | Airborne Observations |
| Manufacturer / model | Aventech Research Inc., AIMMS-20 |
| Primary measurements | Atmospheric pressure; Atmospheric temperature; Atmospheric turbulence |
| Record | 2013-06-24 to 2026-09-23 (retired) |
| Datastreams with data | 13 across 6 sites |
| Sites | acx, cor, ena, mao, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/gustprobe-air |


## Credit

Everything this skill knows about the instrument is the work of **A Matthews, L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Matthews, L Goldberger. *Aircraft-Integrated Meteorological Measurement System (AIMMS) Instrument Handbook*, DOE/SC-ARM-TR-260, November 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `aimms20-air`, `gps`, `met-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `gustprobe-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The AIMMS-20 probe measures platform position, velocity, attitude, ambient temperature, static pressure, and the differential pressures from a 5-port hemispheric gust probe, and combines all these measured data into a calculation of the ambient winds. Raw measurements are communicated over the CAN bus to the onboard data management system (ODMS) and stored in flight in binary .rXX files. These are combined in post-processing using the Aventech program asmbl.exe into .raw files, which are then processed using the Aventech program ekf553_oemv.exe, which regenerates the wind estimates, in this case at an output rate of 20 Hz. Aventech engineers use the aircraft-centric frame of reference common to aeronautical engineering, which defines z as down.

**Siting.** The AIMMS probe is mounted on the front of the aircraft (ARM G-1), with the probe canister housing mounted on the aircraft; Aventech engineers use the aircraft-centric frame of reference common to aeronautical engineering, which defines z as down.

**Sampling.** native rate Broadcast / Log Update Rate: 1 - 10 Hz; reported every Data ingested and available at arm.gov in icartt format at 20 Hz (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Temperature | Celsius | - | 0.30 C | 0.01 C | (hb p. 8) |
| Humidity | %RH/100 | - | 2.0%RH | 0.1%RH | (hb p. 8) |
| Barometric pressure | Pa | - | - | - | (hb p. 8) |
| u_w - North wind component | m/s [+'ve North] | - | 0.50 m/s (1.0 knot) @ 150 knot | - | (hb p. 8) |
| v_w - East wind component | m/s [+'ve East] | - | 0.50 m/s (1.0 knot) @ 150 knot | - | (hb p. 8) |
| w_w - Vertical wind component | m/s | - | 0.75 m/s (1.5 knot) @ 150 knot TAS | - | (hb p. 8) |
| GPS latitude | decimal degrees | - | - | - | (hb p. 8) |
| GPS longitude | decimal degrees | - | - | - | (hb p. 8) |
| GPS altitude | M | - | - | - | (hb p. 8) |
| u_i - Aircraft longitudinal inertial velocity | m/s [+'ve forward] | - | - | - | (hb p. 8) |
| v_i - Aircraft lateral inertial velocity | m/s [+'ve to starboard] | - | - | - | (hb p. 8) |
| w_i - Aircraft vertical velocity | m/s [+'ve down] | - | - | - | (hb p. 8) |
| Roll | degrees | - | - | - | (hb p. 8) |
| Pitch | degrees | - | - | - | (hb p. 8) |
| Yaw or heading | degrees | - | - | - | (hb p. 8) |
| True air speed (TAS) | m/s | - | - | - | (hb p. 8) |
| Dimensional sideslip angle | degrees | - | - | - | (hb p. 8) |
| Non-dimensional angle-of-attack | - | - | - | - | (hb p. 8) |
| Non-dimensional sideslip angle | - | - | - | - | (hb p. 8) |
| Wind status flag | 0 - Invalid; 1 - Valid;... | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wind Speed Accuracy - Horizontal North and East Components | 0.50 m/s (1.0 knot) @ 150 knot | (hb p. 10) |
| Wind Speed Accuracy - TAS Vertical | 0.75 m/s (1.5 knot) @ 150 knot TAS | (hb p. 10) |
| Temperature Accuracy | 0.30 C | (hb p. 10) |
| Temperature Resolution | 0.01 C | (hb p. 10) |
| Relative Humidity Accuracy | 2.0%RH | (hb p. 10) |
| Relative Humidity Resolution | 0.1%RH | (hb p. 10) |
| Broadcast / Log Update Rate | 1 - 10 Hz | (hb p. 10) |
| Log Capacity | 45000 Records | (hb p. 10) |
| Log Capacity (time) | 12.5 hours @ 1 Hz | (hb p. 10) |


## The data

Verified example: **`sgpaafgust1hzF1.a1`**, file `sgpaafgust1hzF1.a1.20160920.200815.nc`
(0.53 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=6592 |
| Data variables | 21 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:08:15 to 2016-09-20T21:58:06 |
| dod version | aafgust1hz-a1-1.0 |
| process version | ingest-aafgust-1.3-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `acceleration_x` | gravity | time | - | Acceleration along fuselage, calibrated |
| `acceleration_x_raw` | V | time | - | Acceleration along fuselage, raw |
| `acceleration_y` | gravity | time | - | Acceleration across fuselage, calibrated |
| `acceleration_y_raw` | V | time | - | Acceleration across fuselage, raw |
| `acceleration_z` | gravity | time | - | Acceleration in vertical direction, calibrated |
| `acceleration_z_raw` | V | time | - | Acceleration in vertical direction, raw |
| `alpha_pressure` | hPa | time | - | Alpha pressure, calibrated |
| `alpha_pressure_raw` | V | time | - | Alpha pressure, raw |
| `beta_pressure` | hPa | time | - | Beta pressure, calibrated |
| `beta_pressure_raw` | V | time | - | Beta pressure, raw |
| `dynamic_pressure` | hPa | time | - | Dynamic pressure, calibrated |
| `dynamic_pressure_raw` | V | time | - | Dynamic pressure, raw |
| `measured_temperature` | degC | time | - | Measured temperature, calibrated |
| `measured_temperature_raw` | V | time | - | Measured temperature, raw |
| `static_pressure` | hPa | time | - | Static pressure, calibrated |
| `static_pressure_raw` | V | time | - | Static pressure, raw |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaafgust1hzF1.a1", "2016-09-20", "2016-09-20")
ds = armlive_open("sgpaafgust1hzF1.a1", "2016-09-20", "2016-09-20", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaafgust1hzF1.a1", "20130624", "20260923")
```

The handbook's own note on data quality: Measurements of position, winds, temperature, and RH are validated with redundant measurements from other instrumentation on board. A wind status flag (0 - Invalid, 1 - Valid, -9999 missing) is included in the data. For a merged data set containing navigational and meteorological data at 1 Hz, refer to the ARM value-added product NAVMET-AIR. Data quality can be reviewed via the ARM Data Quality Plot Browser (wind speed and static pressure time series).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Clogging of 5-port gust probe after flying through clouds | Erroneous or degraded wind/pressure measurements following cloud penetration; abrupt shifts or noise in wind speed and static pressure time series | Requires purging with dry air delivered via canistered air after flying through clouds, done at flight scientists' discretion | (hb p. 10) |
| Moisture/water accumulation in canister and bulb after moist or cloudy flight levels | Degraded temperature/humidity/pressure readings; bulb contamination with water | Purge in flight after moist or cloudy levels; check bulb occasionally for water | (hb p. 12) |
| Aircraft-centric reference frame convention (z defined as down) | Sign convention for vertical velocity/wind components may appear inverted relative to standard meteorological convention unless accounted for | Note: Aventech engineers use aircraft-centric frame of reference common to aeronautical engineering, which defines z as down | (hb p. 7) |
| Wind status flag indicating invalid or missing data | Wind status flag column shows 0 (Invalid), 1 (Valid), or -9999 (missing) alongside wind variables | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Clear air flights in smooth air at increasing and decreasing true air speeds and yaws of 5-10 degrees, heading true north followed by true south; data sent to vendor who provides calibration files (hb p. 11) |
| Calibration interval | Prior to each campaign (hb p. 11) |
| Traceability | Vendor (Aventech Research Inc.) provided calibration files (hb p. 11) |
| Routine maintenance | Purge instrument in flight after particularly moist or cloudy levels to remove moisture from the canister and bulb; check bulb occasionally for water (hb p. 12) |
| Maintenance interval | After moist/cloudy flight levels; occasional bulb checks (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: NAVMET-AIR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AIMMS` | aircraft-integrated meteorological measurement system |
| `ARM` | Atmospheric Radiation Measurement |
| `G-1` | Gulfstream-159 |
| `GPS` | Global Positioning System |
| `NAVMET-AIR` | Navigation and Meteorological Data from Multiple Sensors on Airborne Platform |
| `ODMS` | onboard data management system |
| `RH` | relative humidity |
| `TAS` | true air speed |
| `UTC` | Coordinated Universal Time |
| `VAP` | value-added product |


### References the handbook cites

- Mei, F, J Wang, JM Comstock, R Weigel, M Kramer, C Mahnke, JE Shilling, J Schneider, C Schulz, CN Long, M Wendisch, LAT Machado, B Schmid, T Krisna, M Pekour, J Hubbe, A Giez, B Weinzierl, M Zoeger, ML Pohlker, H...
- Beswick, KM, MW Gallagher, AR Webb, EG Norton, and F Perry. 2008. "Application of the Aventech AIMMS20AQ airborne probe for turbulence measurements during the Convective Storm Initiation Project." Atmospheric Chemistry...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf (13 pages, DOE/SC-ARM-TR-260, by A Matthews, L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=gustprobe-air`, read 2026-09-23
- Example file: `sgpaafgust1hzF1.a1.20160920.200815.nc` from `sgpaafgust1hzF1.a1`, 0.53 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
