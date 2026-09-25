---
name: arm-instrument-nav-air
description: ARM Navigational Location, Motion, and Attitude for Airborne Platforms (nav-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Latitude, Longitude, INS depth, Roll, Pitch, Yaw, X velocity, Y velocity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafnavU2.b1) and the variable inventory of a real file. Use when working with nav-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations. Triggers - nav-air, bnfaafnavU2.b1, Latitude, Longitude, INS depth, Roll, Pitch, Yaw, Airborne Observations, ACAPEX, MWACR.
---

# NAV-AIR - Navigational Location, Motion, and Attitude for Airborne Platforms

The NAV instrument is a GPS-aided inertial navigation system (iXSea/iXBlue HYDRINS III) mounted on the ARM Mobile Facility 2 (aboard ship) that provides true heading, attitude (roll, pitch, yaw), speed, and position for the platform.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nav-air` |
| Handbook | [DOE/SC-ARM-TR-236 / SM Walton / December 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-236.pdf) |
| Measurement category | Airborne Observations |
| Manufacturer / model | iXSea/iXBlue HYDRINS III GPS-aided INS (prior to Dec 2012: Kearfott SEANAV INS model KN-5051-G S/N 1001) |
| Primary measurements | Atmospheric pressure; Atmospheric temperature; Horizontal wind; Navigation variables |
| Record | 2013-06-24 to 2026-09-23 (active) |
| Datastreams with data | 46 across 8 sites |
| Sites | acx, bnf, cor, ena, mao, nsa, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/nav-air |


## Credit

Everything this skill knows about the instrument is the work of **SM Walton** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SM Walton. *Navigational Location and Attitude (NAV) Instrument Handbook*, DOE/SC-ARM-TR-236, December 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-236.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `nav` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `nav-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

HYDRINS is an inertial navigation system with a high-level inertial heart based on fiber-optic gyroscopes coupled to an embedded digital signal processor running a Kalman filter developed for marine applications, holding GPS hybridation for surface alignment and accurate position/altitude computation. A fiber-optic gyroscope is a 2-wave ring interferometer made of a multi-turn fiber coil enclosing an area; light entering is split into two counter-propagating waves that recombine in phase after traveling the same path in opposite directions. When the gyroscope rotates, the Sagnac effect induces a difference in transit time between the two waves, measurable interferometrically, proportional to the product of rotation rate and enclosed coil area. Gyroscope sensitivity can be increased by increasing the number of fiber coil turns and/or coil diameter. Data fusion of INS and GPS datastreams via Kalman filtering produces high-accuracy, drift-free location, attitude, and motion data in three translational (surge, sway, heave) and three rotational (roll, pitch, yaw) frames of reference.

**Siting.** The HYDRINS unit is mounted to a fixed position in the operations van, near the center line of the ship. The offset from the center of gravity of the ship to the HYDRINS unit must be entered into the web application settings. For ACAPEX, the INS system was installed to agree within one degree with the RV Ron Brown gyrocompass, and the operations van was placed near the ship's center line (see Figure 2). At least 210mm of clearance is required on the cable-connection side.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Latitude | deg | -90 to +90 deg | - | 180*2-31 | (hb p. 9) |
| Longitude | deg | -180 to +180 deg | - | 180*2-31 | (hb p. 9) |
| INS depth (negative altitude MSL) | cm | - | - | - | (hb p. 9) |
| Roll | deg | -180 to +180 deg | 0.01 deg. (dynamic accuracy) | 180*2-15 | (hb p. 9) |
| Pitch | deg | -90 to +90 deg | 0.01 deg. (dynamic accuracy) | 180*2-15 | (hb p. 9) |
| Yaw (true heading) | deg | 0 to 360 deg | 0.01 deg. secant latitude | 180*2-15 | (hb p. 9) |
| X velocity (forward) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| Y velocity (toward port) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| Z velocity (up) | m/s | -32 to +32 m/s | - | 2-10 m/s | (hb p. 9) |
| X accel (forward) | m/s^2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Y accel (to port) | m/s^2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Z accel (up) | m/s^2 | -32 to +32 m/s*2 | - | 2-10 m/s | (hb p. 9) |
| Roll rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Pitch rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Yaw rate | rad/s | -4 to +4 radians/sec | - | 2-13 rad/s | (hb p. 9) |
| Time (UTC since 00:00:00) | sec | - | - | 2-14 sec | (hb p. 9) |
| Surge (forward) | m | -64 to +64 m | - | 2-9 m | (hb p. 9) |
| Sway (port) | m | -64 to +64 m | - | 2-9 m | (hb p. 9) |
| Heave (up) | m | -64 to 64 m | 2.5 cm or 2.5% (Smart Heave) | 2-9 m | (hb p. 9) |
| Speed Over Ground (SOG) | m/s | - | - | - | (hb p. 12) |
| Course Over Ground (COG) | deg from true north | - | - | - | (hb p. 12) |
| Position | m/deg | - | Real Time with GPS: 3 times better than GPS; No... | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Operating/storage temperature | -20 to 55 °C / -40 to 80 °C | (hb p. 12) |
| Rotation rate dynamic range | Up to 750 deg/s | (hb p. 12) |
| Acceleration dynamic range | ± 15 g | (hb p. 12) |
| Heading/roll/pitch | 0 to +360 deg / ± 180 deg / ± 90 deg | (hb p. 12) |
| Mean time between failures (computed/observed) | 40,000/80,000 hours | (hb p. 12) |
| Position accuracy Real Time - With GPS | 3 times better than GPS | (hb p. 12) |
| Position accuracy Real Time - No aiding for 1 min/2 min | 0.8 m/3.2 m | (hb p. 12) |
| Position accuracy post-processed - With GPS | 4 times better than GPS | (hb p. 12) |
| Position accuracy post-processed - No aiding for 1 min/2 min | 0.2 m/1 m | (hb p. 12) |
| Heading accuracy | 0.01 deg. secant latitude | (hb p. 12) |
| Roll and pitch dynamic accuracy | 0.01 deg. | (hb p. 12) |
| Heave accuracy (Smart Heave) | 2.5 cm or 2.5% | (hb p. 12) |
| Gyroscope bias range | 0.1 degree per hour bias to 0.0003 degree per hour bias (for space applications) | (hb p. 13) |
| Input Voltage | 24 volts using 15 watts | (hb p. 14) |
| Input Current | 2.5 amperes | (hb p. 14) |
| Clearance requirement | at least 210mm of clearance on the side where cables connect | (hb p. 17) |


## The data

Verified example: **`bnfaafnavU2.b1`**, file `bnfaafnavU2.b1.20260910.163627.nc`
(1.06 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=13837 |
| Data variables | 14 |
| QC variables | 6 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-10T16:36:27 to 2026-09-10T20:27:02 |
| dod version | aafnav-b1-1.0 |
| process version | ingest-aafnav-1.6-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `velocity_east` | m/s | time | yes | Eastward component of aircraft velocity |
| `velocity_north` | m/s | time | yes | Northward component of aircraft velocity |
| `velocity_up` | m/s | time | yes | Upward component of aircraft velocity |
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
                     params={"user": f"{user}:{token}", "ds": "bnfaafnavU2.b1",
                             "start": "2026-09-10", "end": "2026-09-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaafnavU2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaafnavU2.b1", "2026-09-10", "2026-09-10")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaafnavU2.b1", "2026-09-10", "2026-09-10"))   # cite what you pulled
```

## Quality control in this datastream

6 `qc_` companion variables cover 6 of the
14 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_velocity_east"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("velocity_east", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["velocity_east", "velocity_north", "velocity_up"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfaafnavU2.b1", "20130624", "20260923")
```

The handbook's own note on data quality: While reading data from the HYDRINS unit, errors are possible (communication issues, corrupt data, loss of signal). When an error occurs, the system stops processing and removes the current output file so other systems do not read old or corrupted data, then attempts to restart processing as soon as possible to minimize missing data. The Instrument Mentor Monthly Summary report has been discontinued. Summary plots are used to examine NAV motion data quality and the quality of leveling control for the MWACR antenna on the RPH motion table.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Communication/data errors from HYDRINS unit | Data gaps or missing output files; system stops processing and removes current output file when error occurs | System attempts to re-start processing as soon as possible to minimize missing data | (hb p. 11) |
| Corrupt data or loss of signal | Old or corrupted data would otherwise be read by other systems if not removed | System removes current output file so other systems do not read old or corrupted data | (hb p. 11) |
| Missing $WINAV and $TSINV records | winav.txt file and $TSINV output missing from data stream | Records are only sent if valid HYDRINS data are being received; occurs if HYDRINS data flow is interrupted or navigation mode is substandard | (hb p. 16) |
| Longitude convention difference between SEANAV and HYDRINS | Longitude values appear as 0-360 instead of expected -180 to +180 | Apply correction: if (longitudegreater than 180.0) longitude = longitude-360.0 | (hb p. 9) |
| Depth/altitude sign convention and negative zero issue | Depth field may appear as negative zero or wrong sign relative to altitude MSL | Apply correction: if(alt!=0) alt = -alt | (hb p. 9) |
| Pitch sign sense difference between SEANAV and HYDRINS | Pitch and pitch rate values appear opposite in sign from expected convention | Apply correction: if (pitch!=0.0) pitch = -pitch | (hb p. 9) |
| GPS time not yet received at startup | Time field D43-D46 MSB=1, indicating time is seconds since turn-on rather than since start of day | Check MSB: if MSB=0, GPS time is available (seconds since start of day); for GPS dropouts extrapolated time may be used with MSB=0 | (hb p. 9) |
| GPS dropouts | Time values may be extrapolated rather than GPS-derived, with MSB=0 despite lack of live GPS fix | Extrapolated time may be used during dropouts | (hb p. 9) |
| Degraded position accuracy without GPS aiding | Position accuracy degrades from GPS-aided levels (e.g., 3-4x better than GPS) to 0.8m/3.2m (real-time) or 0.2m/1m (post-processed) after 1/2 minutes without aiding | None specified beyond noted accuracy figures | (hb p. 12) |
| Error propagation in pure inertial computation | Accumulating drift/errors in velocity, position, and attitude over time when relying on pure inertial (non-GPS-aided) computation | None specified; noted as inherent since gyrometer/accelerometer data are integrated over time and errors propagate and influence each other in the... | (hb p. 14) |
| Physical shock to the device | Impacts accuracy of the data output | None specified beyond noting it as an external factor | (hb p. 14) |
| Inaccurate GPS input data | Impacts accuracy of the data output | None specified beyond noting it as an external factor | (hb p. 14) |
| Yaw/heading does not represent actual ship movement direction | Yaw (heading) value differs from course over ground / actual direction of ship travel | Note that yaw or heading is the direction the bow is pointing, NOT the direction the ship is actually moving; use course over ground (cog) for... | (hb p. 12) |
| SEANAV Ring Laser Gyro end of life (legacy system) | Historical hardware failure leading to system replacement | Replaced with HYDRINS system equipped with firmware to emulate SEANAV ID1 protocol | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | As soon as HYDRINS is powered on, it starts its alignment phase with the manually input position stored into HYDRINS PROM. During the first five minutes after powering on, HYDRINS performs coarse alignment; afterward it switches to 'fine alignment' phase to improve accuracy of roll, pitch, and heading estimations.... (hb p. 17) |
| Calibration interval | Performed at each power-on/startup (hb p. 17) |
| Routine maintenance | Regular inspections of the equipment, wires, and cables should be made to ensure there is no damage. Software updates should be made only if there is an issue or additional feature needed. (hb p. 18) |
| Maintenance interval | Regular (unspecified) (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Marine W-band ARM Cloud Radar (MWACR).

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
- Catalog record: ARM data-source index, `instrument_class_code=nav-air`, read 2026-09-23
- Example file: `bnfaafnavU2.b1.20260910.163627.nc` from `bnfaafnavU2.b1`, 1.06 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
