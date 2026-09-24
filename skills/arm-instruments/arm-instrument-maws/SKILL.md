---
name: arm-instrument-maws
description: ARM Automatic Weather Station (maws) - handbook-derived instrument reference. Measurement principle, reported quantities (Temperature, Relative humidity, Barometric pressure, Wind speed, Wind direction), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmawsC1.b1) and the variable inventory of a real file. Use when working with maws data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - maws, Automatic Weather Station, sgpmawsC1.b1, Temperature, Relative humidity, Barometric pressure, Wind speed, Wind direction, Surface Meteorology, Vaisala, Inc. - MAWS system with HMP155 (T/RH), BBSS, MAWS, SONDE.
---

# MAWS - Automatic Weather Station

MAWS is a Vaisala-manufactured automatic weather station mounted on a tiltable 10-m mast that provides surface measurements of barometric pressure, temperature, relative humidity, wind speed, and wind direction to initialize each ARM radiosonde (BBSS) profile at launch.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 11 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `maws` |
| Handbook | [DOE/SC-ARM-TR-195 / E Keeler / July 2025](https://www.arm.gov/publications/tech_reports/handbooks/maws_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala, Inc. - MAWS system with HMP155 (T/RH), PTB330 (barometric pressure), WMT700 (winds, heated), QML201C data logger |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind |
| Record | 2014-09-08 to 2026-09-23 (active) |
| Datastreams with data | 19 across 13 sites |
| Sites | anx, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, nsa, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/maws |


## Credit

Everything this skill knows about the instrument is the work of **E Keeler** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> E Keeler. *Meteorological Automatic Weather Station (MAWS) Instrument Handbook*, DOE/SC-ARM-TR-195, July 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/maws_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Temperature measurement is based on resistive platinum sensors (Pt100). Humidity measurement is based on the capacitive thin-film HUMICAP® polymer sensor. Pressure measurement is based on a BAROCAP® silicon capacitive absolute pressure sensor. Wind speed and direction are measured using ultrasound to determine horizontal wind speed and direction based on the transit time of the ultrasound from one transducer to another, measured in both directions for a pair of transducer heads. Measurements are calculated using two measurements for each of the three ultrasonic paths at 60° angles to each other.

**Siting.** Sensors mounted on a tiltable 10-m mast at standard heights defined for each variable: temperature and relative humidity at 2 meters above ground or structure, barometric pressure at 1 meter, and winds at 10 meters. The digital barometer is mounted inside a weatherproof enclosure at the base of the mast (1 m); the T/RH probe is mounted inside an aspirated radiation shield above the electronics enclosure at 2 m; the ultrasonic wind sensor is mounted at the top of the 10-m mast. The mast has a lightning rod and grounding system installed.

**Sampling.** averaging Arithmetic-averaged wind speed (m/s); Vector-averaged wind direction (deg) (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Temperature | °C | -80 - +60°C (-112 - +140 °F) | -80...+20 °C ±(0.176 - 0.0028 x temperature)... | - | (hb p. 7) |
| Relative humidity | %RH | 0 - 100 %RH | +15 to +25 °C: ±1 %RH (0 to 90 %RH), ±1.7 %RH... | - | (hb p. 7) |
| Barometric pressure | hectopascals (hPa) | 50 - 1100 hPa | 500 to 1100 hPa ±0.25 hPa; 50 to 1100 hPa ±0.45... | - | (hb p. 7) |
| Wind speed | meters/second (m/s) | 0 to 75 m/s | ±0.1 m/s or 2% of reading, whichever is greater | - | (hb p. 8) |
| Wind direction | degrees | 0 to 360 degrees | ±2 degrees | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Temperature and relative humidity sensor | Vaisala T/RH Sensor, Model HMP155, installed in an R. M. Young aspirator Model 53502 | (hb p. 7) |
| Barometric pressure sensor | Vaisala Digital Barometer, Model PTB330 | (hb p. 7) |
| Wind sensor | Vaisala Ultrasonic Wind Sensor, Model WMT700 (heated) | (hb p. 7) |
| Data logger | Vaisala QML201C | (hb p. 7) |
| Temperature and RH mounting height | 2 meters above ground or structure | (hb p. 6) |
| Barometric pressure mounting height | 1 meter | (hb p. 6) |
| Wind sensor mounting height | 10 meters | (hb p. 6) |
| Relative Humidity uncertainty (+20 °C) | ±1.0 %RH (40 to 97 %RH) for +20 °C | (hb p. 8) |
| Barometric pressure calibration uncertainty | ±0.07 hPa | (hb p. 8) |
| Winds Ultrasonic Wind Sensor uncertainty |  | (hb p. 8) |
| QML201 Data Logger voltage measurement uncertainty | For temperature range -50 to +60 °C ±5.0 V range | (hb p. 8) |


## The data

Verified example: **`sgpmawsC1.b1`**, file `sgpmawsC1.b1.20260919.000007.nc`
(0.12 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1439, `bound`=2 |
| Data variables | 18 |
| QC variables | 6 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:07 to 2026-09-19T23:59:07 |
| dod version | maws-b1-2.0 |
| process version | ingest-maws-1.2-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `atmospheric_dew_point` | degC | time | yes | Atmospheric dew point temperature |
| `atmospheric_pressure` | hPa | time | yes | Atmospheric pressure |
| `atmospheric_relative_humidity` | % | time | yes | Atmospheric relative humidity |
| `atmospheric_temperature` | degC | time | yes | Dry bulb temperature |
| `wind_direction` | degree | time | yes | Wind direction |
| `wind_speed` | m/s | time | yes | Wind speed |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmawsC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("sgpmawsC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

## Quality control in this datastream

6 `qc_` companion variables cover 6 of the
18 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("sgpmawsC1.b1", "20140908", "20260923")
```

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| SONDE surface bias / instrumentation not designed for near-zero airflow | SONDE surface-level readings at time 0 would show biases if used directly, since SONDE instrumentation is designed for use in flight with ~5 m/s of air moving across the sensors rather than... | MAWS data (not SONDE data) is used for the first (time 0) data point in the ARM radiosonde profile | (hb p. 9) |
| Historical manual entry of surface data (2011-2014, prior to MAWS) | Prior to MAWS implementation, the first sounding data point at time 0 came from the MET system via manual entry, introducing potential for transcription error or delay compared to automated... | - | (hb p. 9) |
| T/RH probe filter contamination/debris | Anomalous or drifting temperature/RH readings if the removable filter protecting the sensors, or the probe housing, becomes fouled with debris | Daily check that T/RH probe housing is free of debris and fans are running; bi-weekly visual inspection of T/RH probe for debris | (hb p. 9) |
| Barometer intake tube blockage | Erroneous pressure readings if the barometer intake tube becomes obstructed | Bi-weekly visual inspection of barometer intake tube | (hb p. 9) |
| Wind sensor debris/fouling | Erroneous or dropped-out wind speed/direction readings if the ultrasonic transducers are obstructed by debris | Bi-weekly visual inspection of wind sensor for debris | (hb p. 9) |
| Tower/mast alignment or grounding fault | Systematic wind direction offset if tower arms are misaligned; potential instrument damage/data gaps from lightning if grounding system is compromised | Bi-weekly inspection of grounds near MAWS, inspection of tower, and checking tower arms for proper alignment; lightning rod and grounding system... | (hb p. 9) |
| Sensor calibration drift | Gradual offset between MAWS readings and reference/handheld calibration probe over time | Annual field calibration of HMP155 and PTB330 using Vaisala MH70 handheld probe; instrument sent to Vaisala for calibration if found out of... | (hb p. 9) |
| Data logger/software timing fault | Timestamp mismatch between MAWS data and expected launch time if software date/time is incorrect, or stale/non-updating data stream | Daily check that software date/time is correct and that data is updating on the software | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field calibration; HMP155 calibrated using a Vaisala MH70 handheld probe that is also calibrated regularly. If a sensor is out of calibration, the instrument is sent to Vaisala for calibration. ARM also generally tries to check the calibration of the sensor upon uninstallation/installation. (hb p. 9) |
| Calibration interval | Temperature/RH (HMP155) and Barometric pressure (PTB330): field calibrated annually. Winds (WMT700): may be field checked if needed at any time. (hb p. 9) |
| Routine maintenance | Daily checks: cables connected and undamaged, logger housing securely closed, T/RH probe housing free of debris and fans running, software date/time correct, data updating on the software. Bi-weekly checks: inspection of grounds near MAWS, inspection of tower, checking tower arms for proper alignment, visual... (hb p. 9) |
| Maintenance interval | Daily and bi-weekly (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Vaisala MW41 sounding system, digiCORA-III, MET (surface meteorological system), SONDE (radiosonde/BBSS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `BBSS` | balloon-borne sounding system |
| `MAWS` | meteorological automatic weather station |
| `MET` | surface meteorological system |
| `RH` | relative humidity |
| `SONDE` | radiosonde (or BBSS) |
| `T` | temperature |


### References the handbook cites

- Vaisala WINDCAP® Ultrasonic Wind Sensor Series WMT700 User's Guide, https://docs.vaisala.com/r/M211095EN-K/en-US
- Vaisala BAROCAP® Digital Barometer PTB330 User's Guide, https://docs.vaisala.com/r/M210855EN-E/en-US
- Vaisala HUMICAP® Humidity and Temperature Probe HMP155 User's Guide, https://docs.vaisala.com/r/M210912EN-G.1/en-US

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/maws_handbook.pdf (11 pages, DOE/SC-ARM-TR-195, by E Keeler)
- Catalog record: ARM data-source index, `instrument_class_code=maws`, read 2026-09-23
- Example file: `sgpmawsC1.b1.20260919.000007.nc` from `sgpmawsC1.b1`, 0.12 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
