---
name: arm-instrument-tbsmet
description: ARM Meteorological Instrumentation aboard TBS (tbsmet) - handbook-derived instrument reference. Measurement principle, reported quantities (3D Sonic Wind Speed, Wind Direction, GPS Position, Horizontal wind speed, Vertical wind speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbsimetxq2C1.b1) and the variable inventory of a real file. Use when working with tbsmet data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Profiling. Triggers - tbsmet, Meteorological Instrumentation aboard TBS, sgptbsimetxq2C1.b1, 3D Sonic Wind Speed, Wind Direction, GPS Position, Horizontal wind speed, Vertical wind speed, Airborne Observations, Atmospheric Profiling, NRG Systems 40H Anemometer, RM Young 27106T Vertical Anemometer.
---

# TBSMET - Meteorological Instrumentation aboard TBS

The tbsmet subsystem is a sonic anemometer-based wind sensor boom package flown aboard the ARM Tethered Balloon System (TBS) that measures 3D sonic wind speed, wind direction, IMU-derived turbulence, and co-located temperature/humidity/pressure at altitude on the balloon tether.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbsmet` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling |
| Manufacturer / model | NRG Systems 40H Anemometer, RM Young 27106T Vertical Anemometer, Tallysman HC872 Helical Antennas, Hemisphere GNSS Vega 28, LI-COR LI-560 Trisonica Sphere |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Navigation variables |
| Record | 2016-04-18 to 2026-09-24 (active) |
| Datastreams with data | 34 across 6 sites |
| Sites | bnf, crg, guc, hou, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbsmet |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbsmet`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbsins`, `tbslws`, `tbspops`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbsmet` until checked against that document's own section for it.

## How it measures

The tbsmet datastream uses a sonic-based 3D wind speed sensor (LI-COR LI-560 Trisonica Sphere) collected at 60 Hz, along with IMU and wind direction data (Tallysman HC872 helical antennas and Hemisphere GNSS Vega 28 compass board) collected at 50 Hz, mounted on a TBS wind sensor boom alongside the tbswind cup/propeller anemometer sensors. Turbulent kinetic energy estimates are generated from the higher-frequency sonic wind speed data. Each wind sensor boom is operated with an iMet XQ2 sensor to provide co-located temperature, relative humidity, and pressure data at the same altitude as the wind sensor. 3-minute and 30-minute means of GPS position and acceleration are used to provide motion-corrected estimates of turbulence in the related tbswind3d product, which is derived from tbsmet's 60 Hz 3D sonic wind observations.

**Siting.** Wind sensor booms are mounted on the TBS tether at altitude (Left: tbswind sensor above tbsmet sensor on TBS); each wind sensor boom is operated with an iMet XQ2 sensor to provide co-located temperature, relative humidity, and pressure at the same altitude. Multiple wind sensor booms may be operated on the same TBS flight at different altitudes. Tether angle from zenith increases with wind speed and is not allowed to exceed 45 degrees in flight.

**Sampling.** native rate tbsmet: 3D sonic wind at 60 Hz; IMU and wind direction at 50 Hz (tbswind cup/propeller anemometers at 1 Hz); reported every Turbulence estimates and merged products use 3-minute and 30-minute means of GPS position and acceleration for motion-corrected turbulence in tbswind3d; averaging 3-minute and 30-minute means of GPS position and acceleration used for motion-corrected turbulence estimates (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| 3D Sonic Wind Speed | m/s | 0-50 | +/- 1 % | 0.01 m/s | (hb p. 13) |
| Wind Direction | degrees | 0-360 | +/- 0.08 | 0.1 | (hb p. 13) |
| GPS Position | - | - | ≥ 8 mm | 1 ppm | (hb p. 13) |
| Horizontal wind speed (via wind sensor boom, tbswind3d... | m/s | 1-96 | +/- 0.1 | 0.765 | (hb p. 13) |
| Vertical wind speed (via wind sensor boom, tbswind3d... | m/s | 0-25 | +/- 1 % | 0.4 | (hb p. 13) |
| Air temperature, relative humidity, pressure (co-located... | degC / % / hPa | -90-50 / 0-100 / 10-1200 | +/- 0.3 / +/- 5 / +/- 1.5 | 0.01 / 0.1 / 0.01 | (hb p. 10) |
| Turbulent kinetic energy / turbulence intensity | - | - | - | - | (hb p. 20) |


## Specifications

| parameter | value | source |
|---|---|---|
| Horizontal wind speed (m/s)... | 0.765 / +/- 0.1 / 1-96 / less than 1 s | (hb p. 13) |
| Vertical wind speed (m/s)... | 0.4 / +/- 1 % / 0-25 / less than 1 s | (hb p. 13) |
| Wind Direction (deg) resolution/accuracy/range/response time | 0.1 / +/- 0.08 / 0-360 / 0.1 s | (hb p. 13) |
| GPS Position resolution/accuracy/range/response time | 1 ppm / ≥ 8 mm / n/a / 0.1 s | (hb p. 13) |
| 3D Sonic Wind Speed (m/s)... | 0.01 m/s / +/- 1 % / 0-50 / 0.02 s | (hb p. 13) |
| Number of wind sensor booms available | Thirteen | (hb p. 12) |
| tbsmet sonic wind sampling rate | 60 Hz | (hb p. 12) |
| tbsmet IMU and wind direction sampling rate | 50 Hz | (hb p. 12) |


## The data

Verified example: **`sgptbsimetxq2C1.b1`**, file `sgptbsimetxq2C1.b1.20241110.143517.nc`
(0.11 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1194, `num_xq2`=1 |
| Data variables | 20 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-11-10T14:35:17 to 2024-11-10T14:55:10 |
| dod version | tbsimetxq2-b1-1.0 |
| process version | ingest-tbsimetxq2-1.3-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `air_temperature` | degC | time,num_xq2 | yes | Air temperature corrected for solar radiation |
| `pressure` | hPa | time,num_xq2 | yes | Air pressure |
| `rh` | % | time,num_xq2 | yes | Relative humidity |
| `rh_sensor_temperature` | degC | time,num_xq2 | yes | Temperature of humidity sensor |
| `sat_count` | count | time,num_xq2 | yes | Satellite count |
| `serial_number` | 1 | num_xq2 | - | Serial number of XQ2 sensors |
| `time` | - | time | - | Time offset from midnight |
| `xq2_file_name` | 1 | num_xq2 | - | iMet XQ2 file names |


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
                     params={"user": f"{user}:{token}", "ds": "sgptbsimetxq2C1.b1",
                             "start": "2024-11-10", "end": "2024-11-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptbsimetxq2C1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptbsimetxq2C1.b1", "2024-11-10", "2024-11-10")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgptbsimetxq2C1.b1", "2024-11-10", "2024-11-10"))   # cite what you pulled
```

## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
20 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_pressure"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("pressure", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["pressure", "air_temperature", "rh"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgptbsimetxq2C1.b1.20241110.143517.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sat_count` | Value is less than fail_min. | 8 | 0.67 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgptbsimetxq2C1.b1", "20160418", "20260924")
```

The handbook's own note on data quality: Each datastream includes quality control variables for each scientific variable. The tbscpc, tbsimet, tbsimetxq2, tbspops, and tbswind datastreams are time-synced and merged with surface-based ceilometer estimates of cloud base and boundary-layer height in the tbsmerged Value-Added Product; tbsmergedincloud further incorporates tbsslwc. Wind sensor booms undergo heading checks at the start of each field campaign against a reference compass bearing, and NRG 40H cup anemometer wind speed and iMet radiosonde RH/temperature are compared against tbsground reference sensor outputs at the start of...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Tether angle deviation from zenith increases with wind speed, limited to 45° maximum | Reported altitude/position of the wind sensor boom may deviate from vertical directly above the ground station, especially in higher wind; flights suspended if wind speed aloft exceeds 14... | Flights are suspended and balloon retrieved if wind speeds aloft exceed 14 m/s; tether angle not allowed to exceed 45° in flight | (hb p. 9) |
| Differing sampling rates between tbswind (1 Hz cup/propeller) and tbsmet (60 Hz sonic, 50... | Turbulence estimates in tbswind3d based on 60 Hz sonic data differ from 1 Hz tbswind cup/propeller measurements; users must be careful not to conflate the two datastreams' native resolution | tbswind3d documents which measurements come from which sensor and sampling rate | (hb p. 20) |
| Ascent/descent motion of the wind sensor boom affects vertical wind measurement | Apparent vertical wind speed includes contribution from boom's own ascent/descent rate unless corrected | The ascent and descent speed of the wind sensor boom are corrected for in the vertical_wind variable by applying an offset for the calculated change... | (hb p. 19) |
| Multiple wind sensor booms operated at different altitudes on same flight | Data files distinguished by altitude; comparing across booms requires altitude metadata | Each boom paired with its own iMet XQ2 for co-located T/RH/P | (hb p. 12) |
| TBS flight envelope restrictions (cloud clearance, visibility, altitude ceiling) | No data collected above 1.5 km agl typically, or when clouds are within 152 m, or visibility less than 3 sm, unless specially authorized | Flights conducted under FAA Certificate of Authorization specific to mission location; in-cloud flights conducted within Restricted Airspace | (hb p. 9) |
| Component/instrument configuration changes between flights | Available measurements and sensor combination on tbsmet/tbswind may vary flight to flight depending on desired measurements, atmospheric conditions, operating location, and flight strategy | None stated beyond noting variability | (hb p. 9) |
| Ground station wind speed measured at different height than airborne tbsmet sensor | Direct comparison of tbsground wind speed (~4 m agl) to airborne tbsmet/tbswind values without altitude correction will show systematic offset | Cross-check comparisons are made against tbsground reference outputs at start of flight day, implicitly acknowledging the height difference | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Vendor calibration; wind sensor booms undergo heading checks at the start of each field campaign against a reference compass bearing. NRG 40H cup anemometer wind speed compared with tbsground sensor reference outputs at start of each flight day. (hb p. 21) |
| Calibration interval | Annually (NRG 40H cup anemometer, NRG IceFree3 anemometer, RM Young 27106T anemometer, LI-COR LI-560 Trisonica); heading checks at start of each field campaign (hb p. 21) |
| Traceability | Vendor calibration mode (hb p. 21) |
| Routine maintenance | Heading checks for wind sensor booms against reference compass bearing at start of each field campaign; wind speed from NRG 40H cup anemometer compared with tbsground reference sensors at start of each flight day (hb p. 21) |
| Maintenance interval | Annually (vendor calibration) / start of each field campaign (heading check) / start of each flight day (cross-check) (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: tbswind, tbswind3d, tbsimet, tbsimetxq2, tbsground, tbsmerged, tbsmergedincloud, tbscpc, tbspops.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `IMU` | inertial measurement unit |
| `TKE` | turbulent kinetic energy (as generated from higher-frequency wind speed data in tbsmet... |
| `agl` | above ground level |
| `GPS` | Global Positioning System |
| `TBS` | tethered balloon system |


### References the handbook cites

- Dexheimer, D, K Gaustad, F Mei, and D Zhang. 2023. Tethered Balloon System Merged Data (TBSMERGED) Value-added Product Report. DOE/SC-ARM-TR-286. https://doi.org/10.2172/1958999

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbsmet`, read 2026-09-24
- Example file: `sgptbsimetxq2C1.b1.20241110.143517.nc` from `sgptbsimetxq2C1.b1`, 0.11 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
