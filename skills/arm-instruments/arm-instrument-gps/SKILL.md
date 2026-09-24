---
name: arm-instrument-gps
description: ARM Global Positioning System (gps) - handbook-derived instrument reference: measurement principle, reported quantities (UTC time, Temperature, Humidity, Barometric pressure, u_w – North wind component, v_w – East wind component, GPS latitude, GPS longitude), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (shbgpsC1.a1) and the variable inventory of a real file. Use when working with gps data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Other. Triggers - gps, Global Positioning System, shbgpsC1.a1, UTC time, Temperature, Humidity, Barometric pressure, u_w – North wind component, v_w – East wind component, Other, Aventech Research Inc., AIMMS-20, AIMMS, NAVMET-AIR, ODMS.
---

# GPS - Global Positioning System

The AIMMS-20 probe, mounted on the ARM Aerial Facility's G-1 aircraft, measures platform position, velocity, attitude, ambient temperature, static pressure, and differential pressures from a 5-port hemispheric gust probe to compute ambient winds.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 13 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gps` |
| Handbook | [DOE/SC-ARM-TR-260 / A Matthews, L Goldberger / November 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf) |
| Measurement category | Other |
| Manufacturer / model | Aventech Research Inc., AIMMS-20 |
| Primary measurements | Navigation variables |
| Record | 1997-10-17 to 1998-10-04 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | shb |
| ARM page | https://www.arm.gov/capabilities/instruments/gps |


## Credit

Everything this skill knows about the instrument is the work of **A Matthews, L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Matthews, L Goldberger. *Aircraft-Integrated Meteorological Measurement System (AIMMS) Instrument Handbook*, DOE/SC-ARM-TR-260, November 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `aimms20-air`, `gustprobe-air`, `met-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `gps`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The AIMMS-20 combines platform position, velocity, and attitude data with ambient temperature, static pressure, and differential pressures measured by a 5-port hemispheric gust probe to calculate the ambient winds. Raw measurements are communicated over the CAN bus to the onboard data management system (ODMS) and stored in flight in binary .rXX files. These files are combined in post-processing using the Aventech program asmbl.exe into .raw files, one per flight, which are then processed using ekf553_oemv.exe to regenerate the wind estimates at an output rate of 20 Hz. Note the Aventech engineers use the aircraft-centric frame of reference common to aeronautical engineering, which defines z as down.

**Siting.** AIMMS probe installed/mounted on the ARM G-1 aircraft (canister housing); Aventech engineers use aircraft-centric frame of reference where z is defined as down.

**Sampling.** native rate 20 Hz (post-processed wind estimates); Broadcast/Log Update Rate 1-10 Hz per specification; reported every Data ingested and available at arm.gov in ICARTT format at 20 Hz; merged NAVMET-AIR product at 1 Hz (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| UTC time | Seconds | - | - | - | (hb p. 8) |
| Temperature | Celsius | - | 0.30 C | 0.01 C | (hb p. 8) |
| Humidity | %RH/100 | - | 2.0%RH | 0.1%RH | (hb p. 8) |
| Barometric pressure | Pa | - | - | - | (hb p. 8) |
| u_w – North wind component | m/s [+'ve North] | - | - | - | (hb p. 8) |
| v_w – East wind component | m/s [+'ve East] | - | - | - | (hb p. 8) |
| GPS latitude | decimal degrees | - | - | - | (hb p. 8) |
| GPS longitude | decimal degrees | - | - | - | (hb p. 8) |
| GPS altitude | M | - | - | - | (hb p. 8) |
| u_i – Aircraft longitudinal inertial velocity | m/s [+'ve forward] | - | - | - | (hb p. 8) |
| v_i – Aircraft lateral inertial velocity | m/s [+'ve to starboard] | - | - | - | (hb p. 8) |
| w_i – Aircraft vertical velocity | m/s [+'ve down] | - | - | - | (hb p. 8) |
| Roll | degrees | - | - | - | (hb p. 8) |
| Pitch | degrees | - | - | - | (hb p. 8) |
| Yaw or heading | degrees | - | - | - | (hb p. 8) |
| True air speed (TAS) | m/s | - | - | - | (hb p. 8) |
| w_w – Vertical wind component | m/s | - | - | - | (hb p. 8) |
| Dimensional sideslip angle | degrees | - | - | - | (hb p. 8) |
| Non-dimensional angle-of-attack | - | - | - | - | (hb p. 8) |
| Non-dimensional sideslip angle | - | - | - | - | (hb p. 8) |
| Wind status flag | 0 – Invalid; 1 – Valid;... | - | - | - | (hb p. 8) |
| Wind speed horizontal (North/East components) | m/s | - | 0.50 m/s (1.0 knot) @ 150 knot | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| WIND SPEED ACCURACY - Horizontal North and East Components | 0.50 m/s (1.0 knot) @ 150 knot | (hb p. 10) |
| WIND SPEED ACCURACY - TAS Vertical | 0.75 m/s (1.5 knot) @ 150 knot TAS | (hb p. 10) |
| TEMPERATURE Accuracy | 0.30 C | (hb p. 10) |
| TEMPERATURE Resolution | 0.01 C | (hb p. 10) |
| RELATIVE HUMIDITY Accuracy | 2.0%RH | (hb p. 10) |
| RELATIVE HUMIDITY Resolution | 0.1%RH | (hb p. 10) |
| Broadcast / Log Update Rate | 1 - 10 Hz | (hb p. 10) |
| Log Capacity | 45000 Records | (hb p. 10) |
| Log Capacity duration | 12.5 hours @ 1 Hz | (hb p. 10) |


## The data

Verified example: **`shbgpsC1.a1`**, file `shbgpsC1.a1.19981001.000254.cdf`
(0.12 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=260, `max_tracked_satellites`=10 |
| Data variables | 24 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 315 s |
| File time span | 1998-10-01T00:02:54 to 1998-10-01T23:57:39 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `GPS_UTC_time` | HHMMSS.SS (hours,... | time | - | UTC time reported by GPS |
| `GPS_altitude` | Meters | time | - | Altitude reported by GPS |
| `GPS_att_baseline_meas_error` | Meters | time | - | Attitude baseline length measurement rms error |
| `GPS_att_phase_meas_error` | Meters | time | - | Attitude phase measurement rms error |
| `GPS_att_reset_flag` | Meters | time | - | Attitude reset flag 0 is good, 1 is bad |
| `GPS_heading` | degrees | time | - | Heading reported by GPS |
| `GPS_latitude` | ddmm.mmmm (degrees... | time | - | Latitude reported by GPS |
| `GPS_latitude_hemisphere` | None | time | - | Hemisphere (N or S) for latitude reported by GPS |
| `GPS_longitude` | dddmm.mmmm (degrees... | time | - | Longitude reported by GPS |
| `GPS_longitude_hemisphere` | None | time | - | Hemisphere (E or W) for longitude reported by GPS |
| `GPS_pitch` | degrees | time | - | Pitch reported by GPS |
| `GPS_roll` | degrees | time | - | Roll reported by GPS |
| `PRN_number` | None | time,max_tracked_satellites | - | Satellite PRN number |
| `filename` | None | time | - | GPS raw data filename |
| `num_tracked_satellites` | None | time | - | Number of tracked satellites |
| `satellite_SNR` | None | time | - | Satellite SNR |
| `satellite_azimuth` | degrees | time,max_tracked_satellites | - | Satellite azimuth |
| `satellite_elevation` | degrees | time,max_tracked_satellites | - | Satellite elevation |
| `satellite_usable_flag` | None | time,max_tracked_satellites | - | Satellite usable (U=usable -=not usable) |
| `time` | - | time | - | Time offset from base_time |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("shbgpsC1.a1", "1998-10-01", "1998-10-01")
ds = armlive_open("shbgpsC1.a1", "1998-10-01", "1998-10-01", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `GPS_att_reset_flag`, `satellite_usable_flag`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("shbgpsC1.a1", "19971017", "20260923")
```

The handbook's own note on data quality: Measurements of position, winds, temperature, and RH are validated with redundant measurements from other instrumentation on board. For a merged data set containing navigational and meteorological data at 1 Hz, refer to the ARM value-added product NAVMET-AIR.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Clogging of 5-port gust probe from moisture/clouds | Erroneous or invalid wind/pressure measurements after flying through clouds | Purge with dry air delivered via canistered air after flying through clouds, at flight scientists' discretion | (hb p. 10) |
| Water accumulation in bulb/canister | Degraded temperature/humidity/pressure readings | Purge in flight after moist or cloudy levels; check bulb occasionally for water | (hb p. 12) |
| Wind status flag indicating invalid or missing data | Wind status flag column reads 0 (Invalid) or -9999 (missing) instead of 1 (Valid) | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Requires clear air flights in smooth air at increasing and decreasing true air speeds and yaws of 5-10 degrees, heading true north followed by true south; data sent to vendor who provides calibration files (hb p. 11) |
| Calibration interval | Recommended prior to each campaign (hb p. 11) |
| Routine maintenance | Instrument should be purged in flight after particularly moist or cloudy levels to remove moisture from the canister and bulb; bulb should also be checked occasionally for water. (hb p. 12) |
| Maintenance interval | At flight scientists' discretion / after moist or cloudy flight levels (hb p. 12) |


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
- Beswick, KM, MW Gallagher, AR Webb, EG Norton, and F Perry. 2008. “Application of the Aventech AIMMS20AQ airborne probe for turbulence measurements during the Convective Storm Initiation Project.” Atmospheric Chemistry...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-260.pdf (13 pages, DOE/SC-ARM-TR-260, by A Matthews, L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=gps`, read 2026-09-23
- Example file: `shbgpsC1.a1.19981001.000254.cdf` from `shbgpsC1.a1`, 0.12 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
