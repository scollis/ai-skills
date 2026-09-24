---
name: arm-instrument-nav
description: ARM Navigational Location and Attitude (nav) - handbook-derived instrument reference. Measurement principle, reported quantities (Latitude, Longitude, INS depth, Roll, Pitch, Yaw, X velocity, Y velocity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (mosnavM1.a1) and the variable inventory of a real file. Use when working with nav data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Ocean Observations. Triggers - nav, Navigational Location and Attitude, mosnavM1.a1, Latitude, Longitude, INS depth, Roll, Pitch, Yaw, Ocean Observations, previously Kearfott SEANAV INS model KN-5051-G S/N 1001, ACAPEX, MWACR.
---

# NAV - Navigational Location and Attitude

The NAV (HYDRINS GPS-aided inertial navigation system) measures ship position (latitude/longitude), true heading, attitude (roll, pitch, yaw), speed, and motion (velocities/accelerations, surge/sway/heave) on sea-based ARM Mobile Facility deployments.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nav` |
| Handbook | [DOE/SC-ARM-TR-236 / SM Walton / December 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-236.pdf) |
| Measurement category | Ocean Observations |
| Manufacturer / model | iXSea/iXBlue HYDRINS III GPS-aided inertial navigation system (INS); previously Kearfott SEANAV INS model KN-5051-G S/N 1001 |
| Primary measurements | Navigation variables |
| Record | 2012-10-01 to 2020-09-30 (retired) |
| Datastreams with data | 5 across 4 sites |
| Sites | acx, mag, mar, mos |
| ARM page | https://www.arm.gov/capabilities/instruments/nav |


## Credit

Everything this skill knows about the instrument is the work of **SM Walton** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SM Walton. *Navigational Location and Attitude (NAV) Instrument Handbook*, DOE/SC-ARM-TR-236, December 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-236.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `nav-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `nav`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

HYDRINS is a GPS-aided inertial navigation system built around fiber-optic gyroscopes coupled to an embedded digital signal processor that runs a Kalman filter developed for marine applications. A fiber-optic gyroscope is a 2-wave ring interferometer made of a multi-turn fiber coil enclosing an area; light is split into two counter-propagating waves that recombine in phase after traveling the same path in opposite directions. When rotating, the Sagnac effect induces a difference in transit time between the two waves that is measured interferometrically and is proportional to the rotation rate and the enclosed coil area. The Kalman filter hybridizes GPS data with the inertial solution for surface alignment and accurate position/attitude computation. Data fusion of the INS and GPS datastreams produces high-accuracy, drift-free location, attitude, and motion data in three translational (surge/sway/heave or X/Y/Z) and three rotational (roll/pitch/yaw) frames of reference.

**Siting.** The HYDRINS unit is mounted to a fixed position in the operations van, near the center line of the ship; for ACAPEX it was installed on the RV Ron Brown to agree within one degree with the ship's gyrocompass. The offset from the ship's center of gravity to the HYDRINS unit must be entered into the unit's settings via its web application.

**Sampling.** native rate SEANAV ID=1 raw binary output records of 56 bytes streamed from HYDRINS (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Latitude | deg | -90 to +90 deg | - | 180*2-31 | (hb p. 9) |
| Longitude | deg | -180 to +180 deg | - | 180*2-31 | (hb p. 9) |
| INS depth (negative altitude MSL) | cm | - | - | - | (hb p. 9) |
| Roll | deg | -180 to +180 deg (port up positive) | 0.01 deg. (dynamic accuracy) | 180*2-15 | (hb p. 9) |
| Pitch | deg | -90 to +90 deg (bow up positive) | 0.01 deg. (dynamic accuracy) | 180*2-15 | (hb p. 9) |
| Yaw (true heading) | deg | 0 to 360 deg from N | 0.01 deg. secant latitude | 180*2-15 | (hb p. 9) |
| X velocity (forward) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| Y velocity (toward port) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| Z velocity (up) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| X acceleration (forward) | m/s*2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Y acceleration (to port) | m/s*2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Z acceleration (up) | m/s*2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Roll rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Pitch rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Yaw rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Surge | m | -64 to +64 m (forward positive) | - | 2-9 m | (hb p. 9) |
| Sway | m | -64 to +64 m (port positive) | - | 2-9 m | (hb p. 9) |
| Heave | m | -64 to 64 m (up positive) | 2.5 cm or 2.5% (Smart Heave) | 2-9 m | (hb p. 9) |
| Speed over ground | m/s | - | - | - | (hb p. 12) |
| Course over ground | deg from true north | - | - | - | (hb p. 12) |
| Position | m | - | With GPS: 3 times better than GPS (real time);... | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Operating/storage temperature | -20 to 55 °C / -40 to 80 °C | (hb p. 12) |
| Rotation rate dynamic range | Up to 750 deg/s | (hb p. 12) |
| Acceleration dynamic range | ± 15 g | (hb p. 12) |
| Heading/roll/pitch | 0 to + 360 deg / ± 180 deg / ± 90 deg | (hb p. 12) |
| Mean time between failures (computed/observed) | 40,000/80,000 hours | (hb p. 12) |
| Warm-up effects | No warm-up effects | (hb p. 12) |
| Shock and vibration | Shock and vibration proof | (hb p. 12) |
| Position accuracy Real Time (With GPS) | 3 times better than GPS | (hb p. 12) |
| Position accuracy Real Time, No aiding for 1 min/2 min | 0.8 m/3.2 m | (hb p. 12) |
| Position accuracy post-processed (With GPS) | 4 times better than GPS | (hb p. 12) |
| Position accuracy post-processed, No aiding for 1 min/2 min | 0.2 m/1 m | (hb p. 12) |
| Heading accuracy | 0.01 deg. secant latitude | (hb p. 12) |
| Roll and pitch dynamic accuracy | 0.01 deg. | (hb p. 12) |
| Heave accuracy (Smart Heave) | 2.5 cm or 2.5% | (hb p. 12) |
| Fiber-optic gyroscope bias range | 0.1 degree per hour bias to 0.0003 degree per hour bias (for space applications) | (hb p. 13) |
| Input Voltage | 24 volts using 15 watts | (hb p. 14) |
| Input Current | 2.5 amperes | (hb p. 14) |
| Fine alignment end criterion | heading covariance below 0.1 degree | (hb p. 17) |
| Cable clearance | at least 210mm of clearance on the side where cables connect | (hb p. 17) |


## The data

Verified example: **`mosnavM1.a1`**, file `mosnavM1.a1.20200927.000000.nc`
(69.6 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=644380 |
| Data variables | 23 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2020-09-27T00:00:00 to 2020-09-27T23:59:59 |
| sampling interval | 50 Hz |
| averaging interval | N/A |
| dod version | nav-a1-1.1 |
| process version | ingest-nav-3.4-1.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cycle_count` | unitless | time | - | Free running cycle counter |
| `heave` | m | time | - | Heave: up positive |
| `heave_acceleration` | m/sec^2 | time | - | Heave directional acceleration, up positive |
| `heave_velocity` | m/s | time | - | Heave directional velocity, up positive |
| `pitch` | degree | time | - | Pitch: bow up positive |
| `pitch_angular_rate` | degree/sec | time | - | Pitch angular rate, bow up positive |
| `roll` | degree | time | - | Roll: starboard down positive |
| `roll_angular_rate` | degree/sec | time | - | Roll angular rate, starboard down positive |
| `seanav_mode` | unitless | time | - | Seanav system mode |
| `seanav_monitor` | unitless | time | - | Seanav monitor value as true/false conditions |
| `surge` | m | time | - | Surge: bow forward positive |
| `surge_acceleration` | m/sec^2 | time | - | Surge directional acceleration, bow forward positive |
| `surge_velocity` | m/s | time | - | Surge directional velocity, bow forward positive |
| `sway` | m | time | - | Sway: toward port positive |
| `sway_acceleration` | m/sec^2 | time | - | Sway directional acceleration, toward port positive |
| `sway_velocity` | m/s | time | - | Sway directional velocity, toward port positive |
| `time` | - | time | - | Time offset from midnight |
| `yaw` | degree | time | - | Heading from geodetic north, clockwise bow rotation |
| `yaw_angular_rate` | degree/sec | time | - | Yaw angular rate, clockwise bow rotation positive |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("mosnavM1.a1", "2020-09-27", "2020-09-27")
ds = armlive_open("mosnavM1.a1", "2020-09-27", "2020-09-27", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("mosnavM1.a1", "20121001", "20260923")
```

The handbook's own note on data quality: While reading data from the HYDRINS unit, errors are possible from communication issues, corrupt data, or loss of signal. When an error occurs, the system stops processing and removes the current output file so that other systems do not read old or corrupted data, then attempts to re-start processing as soon as possible to minimize missing data. The searead program can be used to count records, data gaps, and checksum errors in raw data files.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| HYDRINS communication/data errors (corrupt data or loss of signal) | System stops processing and removes the current output file; gaps in the data record appear where files are missing | System automatically removes current output file so other systems do not read old or corrupted data and attempts to re-start processing as soon as... | (hb p. 11) |
| Missing $TSINV/$WINAV records during substandard navigation mode | The $TSINV output and the winav.txt file will be missing from the data stream | Records are only sent if valid HYDRINS data are being received; monitor navigation mode status | (hb p. 10) |
| Longitude convention mismatch between SEANAV and HYDRINS | Longitude values appear as 0 to +360 instead of expected -180 to +180 | Apply correction logic: if (longitudegreater than 180.0) longitude = longitude-360.0 | (hb p. 9) |
| Negative-zero altitude/depth encoding artifact | Depth/altitude values may show a negative zero | Apply correction logic: if(alt!=0) alt = -alt | (hb p. 9) |
| Pitch sign-sense inversion between SEANAV and HYDRINS | Pitch and pitch rate appear with opposite sign compared to HYDRINS native convention | Apply correction logic: if (pitch!=0.0) pitch = -pitch | (hb p. 9) |
| GPS time not yet available | Time field (D43-D46) MSB=1 indicates time is seconds since turn-on rather than since start of day | Check MSB of time field: if 0, GPS time is available (seconds since start of day); if 1, GPS not yet received; for GPS dropouts extrapolated time may... | (hb p. 9) |
| Inertial error propagation over time | Drift in computed position/attitude/velocity increases with time since alignment, especially without GPS aiding | Accuracy depends on sensor accuracy and initial alignment errors; errors propagate and influence each other since velocity, position, and attitude... | (hb p. 8) |
| External physical shock and inaccurate GPS input degrading accuracy | Sudden accuracy degradation or anomalous jumps in position/attitude data | None specified beyond noting these as external factors impacting accuracy | (hb p. 8) |
| Heading/yaw does not represent ship's direction of motion | Yaw value differs from actual course over ground; can be misinterpreted as ship movement direction | Note that yaw or heading is the direction the bow is pointing, NOT what direction the ship is actually moving | (hb p. 12) |
| Discontinued Instrument Mentor Monthly Summary report | No monthly summary report available for this instrument | Report has been discontinued; no replacement noted | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Upon power-on, HYDRINS performs alignment using manually input position stored in HYDRINS PROM: coarse alignment for the first five minutes, then automatic switch to 'fine alignment' phase to improve roll, pitch, and heading estimation accuracy; fine alignment ends automatically when heading covariance falls below 0.1... (hb p. 16) |
| Traceability | For ACAPEX (2015), the INS system was installed to agree within one degree with the RV Ron Brown gyrocompass. (hb p. 16) |
| Routine maintenance | Regular inspections of the equipment, wires, and cables should be made to ensure there is no damage. Software updates should be made only if there is an issue or an additional feature needed. (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Marine W-band ARM Cloud Radar (MWACR), SEANAV (Kearfott KN-5051-G, predecessor system).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ACAPEX` | ARM Cloud Aerosol Precipitation Experiment |
| `ADC` | ARM Data Center |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `GPS` | Global Positioning System |
| `INS` | inertial navigation system |
| `MSL` | mean sea level |
| `MWACR` | Marine W-band ARM Cloud Radar |
| `RPH` | roll, pitch, and heave |
| `RV` | Research Vessel |
| `SBP` | submarine broadcast processor |
| `SCP` | Secure Copy Protocol |
| `UDP` | User Datagram Protocol |
| `UTC` | Coordinated Universal Time |


### References the handbook cites

- HYDRINS User Guide. 2010. iXSea.
- HYDRINS Quick Start Guide. 2010. iXSea.
- Martin, TJ. AMF2 HYDRINS Operation. 2013. U.S. Department of Energy, Argonne National Laboratory.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-236.pdf (18 pages, DOE/SC-ARM-TR-236, by SM Walton)
- Catalog record: ARM data-source index, `instrument_class_code=nav`, read 2026-09-23
- Example file: `mosnavM1.a1.20200927.000000.nc` from `mosnavM1.a1`, 69.6 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
