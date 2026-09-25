---
name: arm-instrument-aosmet
description: ARM Meteorological Measurements associated with the Aerosol Observing System (aosmet) - handbook-derived instrument reference. Measurement principle, reported quantities (Ambient air relative humidity, Ambient air temperature, Ambient pressure, Wind speed, Rain amount, Rain duration, Rain intensity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaosmetC1.a1) and the variable inventory of a real file. Use when working with aosmet data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - aosmet, enaaosmetC1.a1, Ambient air relative humidity, Ambient air temperature, Ambient pressure, Wind speed, Rain amount, Surface Meteorology, Vaisala WXT520 Weather Transmitter, DQAR.
---

# AOSMET - Meteorological Measurements associated with the Aerosol Observing System

The AOSMET is a Vaisala WXT520 Weather Transmitter mounted atop the AOS aerosol inlet at approximately 10 meters height that measures ambient temperature, relative humidity, pressure, wind speed/direction, and precipitation for hyper-local analysis of AOS aerosol data.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `aosmet` |
| Handbook | [DOE/SC-ARM-TR-184 / J Kyrouac / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/aosmet_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala WXT520 Weather Transmitter |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation |
| Record | 2010-10-03 to 2026-09-23 (active) |
| Datastreams with data | 27 across 22 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mag |
| ARM page | https://www.arm.gov/capabilities/instruments/aosmet |


## Credit

Everything this skill knows about the instrument is the work of **J Kyrouac** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Kyrouac. *Aerosol Observing System Surface Meteorology (AOSMET) Instrument Handbook*, DOE/SC-ARM-TR-184, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/aosmet_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Pressure, temperature, and relative humidity measurements use a PTU module with Vaisala proprietary sensors: a capacitive silicon sensor, a capacitive ceramic sensor, and a capacitive thin-film polymer sensor, respectively. The measurement is based on an advanced RC oscillator, with capacitance of two reference capacitors continuously measured, and temperature dependency of the pressure and humidity measurements is accounted for in the microprocessor. Wind measurements use equally spaced ultrasonic transducers in the same horizontal plane, measuring transit time between each to determine speed and direction via Vw = 0.5 x L x (1/tf - 1/tr). Precipitation measurements use a steel cover and piezoelectric sensor to detect precipitation impact proportional to drop volume, translated to rain amount, with filtering techniques to eliminate noise from non-precipitation sources; precipitation is operated in time mode with messages sent at 1 second intervals.

**Siting.** The WXT520 sensor is mounted on top of the AOS aerosol inlet at a height of approximately 10 meters, intended to provide hyper-local meteorological data relevant to the aerosol stack rather than for general surface meteorological studies.

**Sampling.** native rate 1-second intervals; reported every 1 second; averaging Precipitation intensity uses running one min average in 10s steps (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Ambient air relative humidity | % | - | ± 3% (from 0% to 90%); ± 5% (from 90% to 100%) | - | (hb p. 8) |
| Ambient air temperature | °C | - | ± 0.3°C at 20°C (see manual for extended... | - | (hb p. 9) |
| Ambient pressure | hPa | - | ± 0.5 hPa from 0°C to 30°C | - | (hb p. 9) |
| Wind speed | m/s | - | ± 3% at 10 m/s | - | (hb p. 9) |
| Wind direction, relative to true North | degree | - | ± 3% | - | (hb p. 9) |
| Rain amount | mm/s | - | ± 5% (not including errors induced by wind) | - | (hb p. 9) |
| Rain duration | s | - | ± 5% (not including errors induced by wind) | - | (hb p. 9) |
| Rain intensity | mm/hr | - | ± 5% (not including errors induced by wind) | - | (hb p. 9) |
| Heater temperature | °C | - | - | - | (hb p. 9) |
| Heater voltage | V | - | - | - | (hb p. 9) |
| Supply voltage | V | - | - | - | (hb p. 9) |
| Reference voltage | V | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Temperature Range (operation) | -52°C to 60°C | (hb p. 12) |
| Temperature Range (storage) | -60°C to 70°C | (hb p. 12) |
| Temperature Resolution | 0.1°C | (hb p. 12) |
| Relative humidity Range | 0% to 100% | (hb p. 12) |
| Relative humidity Resolution | 0.1 % | (hb p. 12) |
| Pressure Range | 600 hPa to 1100 hectopascals (hPa) | (hb p. 12) |
| Pressure Resolution | 0.1 hPa | (hb p. 12) |
| Wind speed Range | 0 m/s to 60 meters per second (m/s) | (hb p. 12) |
| Wind speed Resolution | 0.1 m/s | (hb p. 12) |
| Wind speed Response time | 0.25 second (s) | (hb p. 12) |
| Wind direction Range | 0° to 360° | (hb p. 12) |
| Wind direction Resolution | 1° | (hb p. 12) |
| Wind direction Response time | 0.25 s | (hb p. 12) |
| Precipitation cumulation Collection area | 60 square centimeters (cm2) | (hb p. 12) |
| Precipitation cumulation Resolution | 0.01 millimeter (mm) | (hb p. 12) |
| Precipitation duration Response time | 10 s | (hb p. 12) |
| Precipitation intensity Range | 0 to 200 mm/ hour (hr) | (hb p. 12) |
| Precipitation intensity Response time | running one min average in 10s steps | (hb p. 12) |


## The data

Verified example: **`enaaosmetC1.a1`**, file `enaaosmetC1.a1.20260919.000000.nc`
(5.53 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86400 |
| Data variables | 17 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:59 |
| sampling interval | 1 second |
| dod version | aosmet-a1-3.0 |
| process version | ingest-aosmet-1.2-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `heater_temp` | degC | time | - | Heater temperature |
| `heater_volts` | V | time | - | Heater voltage |
| `pressure_ambient` | hPa | time | - | Ambient pressure |
| `rain_amount` | mm/s | time | - | Rain amount |
| `rain_duration` | s | time | - | Rain duration |
| `rain_intensity` | mm/hr | time | - | Rain intensity |
| `ref_volts` | V | time | - | Reference voltage |
| `rh_ambient` | % | time | - | Ambient air relative humidity |
| `supply_volts` | V | time | - | Supply voltage |
| `temperature_ambient` | degC | time | - | Ambient air temperature |
| `time` | - | time | - | Time offset from midnight |
| `wind_direction` | degree | time | - | Wind direction, relative to true North |
| `wind_speed` | m/s | time | - | Wind speed |


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
                     params={"user": f"{user}:{token}", "ds": "enaaosmetC1.a1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enaaosmetC1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enaaosmetC1.a1", "2026-09-19", "2026-09-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enaaosmetC1.a1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaosmetC1.a1", "20101003", "20260923")
```

The handbook's own note on data quality: All variables in the AOSMET data files are .a1 level, meaning no quality flags are applied to the data. The instrument mentor performs routine data checks to diagnose potential problems; if found, maintenance is initiated and a Data Quality Report (DQR) may be filed. The ARM Data Quality Office also submits weekly Data Quality Assessment Reports (DQAR), which include visual inspection of the data and comparison with co-located instrument systems measuring similar variables. Data quality and instrument status information can be found at http://dq.arm.gov.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Wind measurement dropouts in snow | Wind measurements occasionally drop out (missing or erroneous wind speed/direction data) during times of snow | None stated other than noting cause is transducer blockage | (hb p. 10) |
| Under-reporting of very light rain | Rain amount/intensity reads lower than nearby precipitation instruments during light rain events | Manufacturer confirms this is due to sensor mechanics; sensor plate requires precipitation at terminal velocity to register, and light rain often... | (hb p. 10) |
| No quality flags applied to data | All variables in the AOSMET data files are .a1 level with no quality flags applied | None stated | (hb p. 8) |
| Not intended for general surface meteorological studies | Data represent hyper-local conditions at the aerosol inlet rather than representative surface meteorology | Use MET datastream as primary source for surface meteorological data; AOSMET may be suggested as secondary source only when MET data quality is... | (hb p. 10) |
| No routine calibration | Larger measurement uncertainties than research-grade instruments; no calibration correction applied over instrument lifetime | Since 2016, wind zero-check and annual/pre-deployment PTU module replacement performed instead of full calibration | (hb p. 13) |
| Heater activation threshold effects | Heating elements below the precipitation sensor and inside ultrasonic transducers activate when ambient temperature reaches 4°C, which may affect heater temperature/voltage diagnostic... | Diagnostic variables (heater_temp, heater_volts, supply_volts, ref_volts) recorded to help identify potential sensor problems | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Wind speed verification: a bag is placed over the ultrasonic transducers and speed is verified to be 0 m/s; if not, instrument is replaced and sent to manufacturer for evaluation. PTU module replacement: sensor removed from aerosol inlet, old PTU module removed via fixing screws, new module inserted, sensor... (hb p. 13) |
| Calibration interval | Beginning in 2016, wind data are verified to read zero, and an annual (or pre-deployment in the case of mobile facilities) replacement of the PTU module is performed. To date, no routine calibrations have been performed on the sensors. (hb p. 13) |
| Routine maintenance | Preventative visual checks of the instrument and live data are performed daily. If a problem is noted, steps are taken to correct the issue. Any performed maintenance is documented using internal reporting forms. If data quality has been compromised, a DQR will be filed and supplied to the user with the user's order. (hb p. 13) |
| Maintenance interval | Daily visual checks (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MET.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOS` | Aerosol Observing System |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `DQAR` | Data Quality Assessment Report |
| `DQR` | Data Quality Report |
| `VAP` | Value-Added Product |
| `hPa` | hectopascal |
| `PTU` | Pressure, Temperature, and Humidity module |


### References the handbook cites

- Vaisala (2012). USER'S GUIDE: Vaisala Weather Transmitter WXT520. Helsinki, Finland: Vaisala Oyj.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/aosmet_handbook.pdf (15 pages, DOE/SC-ARM-TR-184, by J Kyrouac)
- Catalog record: ARM data-source index, `instrument_class_code=aosmet`, read 2026-09-23
- Example file: `enaaosmetC1.a1.20260919.000000.nc` from `enaaosmetC1.a1`, 5.53 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
