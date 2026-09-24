---
name: arm-instrument-sonde
description: ARM Balloon-Borne Sounding System (sonde) - handbook-derived instrument reference: measurement principle, reported quantities (Pressure, Temperature, Relative humidity, Wind speed, Wind direction, Altitude, Dew point, Ascent rate), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpsondewnpnC1.b1) and the variable inventory of a real file. Use when working with sonde data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling. Triggers - sonde, Balloon-Borne Sounding System, sgpsondewnpnC1.b1, Pressure, Temperature, Relative humidity, Wind speed, Wind direction, Altitude, Atmospheric Profiling, ASCII, BBBS, CLASS, GCOS.
---

# SONDE - Balloon-Borne Sounding System

The SONDE system launches balloon-borne RS-41SGP radiosondes via Vaisala MW41 ground stations at ARM sites to provide in situ vertical profiles of atmospheric thermodynamic state and wind speed/direction.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sonde` |
| Handbook | [DOE/SC-ARM-TR-029 / E Keeler / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/sonde_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Vaisala MW41 ground station with Vaisala RS-41SGP radiosonde (AS41 autosonde at NSA C1) |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind |
| Record | 1970-01-01 to 2026-09-23 (active) |
| Datastreams with data | 110 across 32 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc |
| ARM page | https://www.arm.gov/capabilities/instruments/sonde |


## Credit

Everything this skill knows about the instrument is the work of **E Keeler** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> E Keeler. *Balloon-Borne Sounding System (SONDE) Instrument Handbook*, DOE/SC-ARM-TR-029, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sonde_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The RS-41SGP radiosonde carries a platinum resistor temperature sensor, a thin-film capacitor humidity sensor, and a silicon capacitor pressure sensor, along with GPS-derived wind speed, wind direction, and heights. The instrument is lifted by a 350g balloon filled to achieve a 5 m/s ascent rate, transmitting RF data back to a ground station that decodes signals via a Signal Processing System (SPS) and antennas. Prior to launch, a ground-check process compares the temperature sensor to a secondary humidity-sensor temperature element and baselines the humidity sensor against a physical 0% (and at some sites 100%) humidity reference, with the MW41 software applying corrections. The first data point at time zero is replaced with MAWS (Meteorological Automatic Weather Station) surface data because the radiosonde needs air moving across its sensors for accurate readings. Profiles are recorded once every second or about every 5 meters of ascent, yielding vertical profiles of pressure, temperature, humidity, and GPS-derived wind and position.

**Siting.** All sites have manual launch systems except North Slope of Alaska (NSA) C1, which uses an AS41 autosonde. The MAWS provides ground-truth surface data used as the first data point of each launch. ARM follows manufacturer guidelines for antenna placement to reduce RF interference.

**Sampling.** native rate once every second or one data point every 5 meters ascending; reported every SGP: 2 launches/day (23:30UTC,05:30UTC / 11:30UTC,17:30UTC alternating); ENA: 2 launches/day (23:30UTC,11:30UTC); NSA: 4 launches/day (23:30,05:30,11:30,17:30 UTC); AMF1/AMF2/AMF3: 4 launches/day (23:30,05:30,11:30,17:30 UTC), varies by campaign (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Pressure | hPa | Surface pressure to 3 hPa | greater than  100 hPa: 1.0 hPa; 100 - 3 hPa:... | 0.01 hPa | (hb p. 4) |
| Temperature | °C | -90 to +60°C | 0.3 °C less than  16km; 0.3 °C greater than ... | 0.01°C | (hb p. 4) |
| Relative humidity | %RH | 0 to 100 %RH | 3 %RH (combined uncertainty in sounding) | 0.1 %RH | (hb p. 4) |
| Wind speed | m/s | less than  180 m/s | 0.15 m/s (combined uncertainty in sounding) | 0.1 m/s | (hb p. 4) |
| Wind direction | deg | 0 to 360 deg | 2 deg (combined uncertainty in sounding) | 0.1 deg | (hb p. 4) |
| Altitude | masl | - | - | - | (hb p. 9) |
| Dew point | °C | - | - | - | (hb p. 9) |
| Ascent rate | m/s | - | - | - | (hb p. 9) |
| Latitude of sonde | °N | - | - | - | (hb p. 9) |
| Longitude of sonde | °W | - | - | - | (hb p. 9) |
| u-component of wind velocity | m/s | - | - | - | (hb p. 9) |
| v-component of wind velocity | m/s | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Range - Pressure | Surface pressure to 3 hPa | (hb p. 10) |
| Range - Temperature | -90 to +60°C | (hb p. 10) |
| Range - Humidity | 0 to 100 %RH | (hb p. 10) |
| Range - Wind Speed | less than  180 m/s | (hb p. 10) |
| Range - Wind Direction | 0 to 360 deg | (hb p. 10) |
| Resolution - Pressure | 0.01 hPa | (hb p. 10) |
| Resolution - Temperature | 0.01°C | (hb p. 10) |
| Resolution - Humidity | 0.1 %RH | (hb p. 10) |
| Resolution - Wind Speed | 0.1 m/s | (hb p. 10) |
| Resolution - Wind Direction | 0.1 deg | (hb p. 10) |
| Response time - Pressure | 0.5 s | (hb p. 10) |
| Response time - Temperature | 20 °C: less than  0.3 s; −40 °C: less than  10 s | (hb p. 10) |
| Repeatability - Pressure | greater than  100 hPa: 0.4 hPa; 100 - 3 hPa: 0.3 hPa | (hb p. 10) |
| Repeatability - Temperature | 0.1 °C | (hb p. 10) |
| Repeatability - Humidity | 2 %RH | (hb p. 10) |
| Reproducibility - Pressure | greater than  100 hPa: 0.5 hPa; 100 - 3 hPa: 0.3 hPa | (hb p. 10) |
| Reproducibility - Temperature | 0.15 °C greater than  100hPa; 0.30 °C less than  100hPa | (hb p. 10) |
| Reproducibility - Humidity | 2 %RH | (hb p. 10) |
| Combined uncertainty in sounding - Pressure | greater than  100 hPa: 1.0 hPa; 100 - 3 hPa: 0.6 hPa | (hb p. 10) |
| Combined uncertainty in sounding - Temperature | 0.3 °C less than  16km; 0.3 °C greater than  16km | (hb p. 10) |
| Combined uncertainty in sounding - Humidity | 3 %RH | (hb p. 10) |
| Combined uncertainty in sounding - Wind Speed | 0.15 m/s | (hb p. 10) |
| Combined uncertainty in sounding - Wind Direction | 2 deg | (hb p. 10) |
| Balloon type | 350g balloon filled for 5 m/s ascent rate | (hb p. 7) |
| RF communication frequency | 400-406 MHz | (hb p. 7) |


## The data

Verified example: **`sgpsondewnpnC1.b1`**, file `sgpsondewnpnC1.b1.20260921.113143.nc`
(0.52 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4872 |
| Data variables | 24 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-21T11:31:43 to 2026-09-21T12:52:53 |
| dod version | sondewnpn-b1-3.0 |
| process version | ingest-sonde-11.1-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `asc` | m/s | time | yes | Ascent Rate |
| `deg` | degree | time | yes | Wind Direction |
| `dp` | degC | time | yes | Dewpoint Temperature |
| `pres` | hPa | time | yes | Pressure |
| `rh` | % | time | yes | Relative Humidity |
| `tdry` | degC | time | yes | Dry Bulb Temperature |
| `u_wind` | m/s | time | yes | Eastward Wind Component |
| `v_wind` | m/s | time | yes | Northward Wind Component |
| `wspd` | m/s | time | yes | Wind Speed |
| `time` | - | time | - | Time offset from midnight |
| `wstat` | 1 | time | - | Wind Status |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpsondewnpnC1.b1", "2026-09-21", "2026-09-21")
ds = armlive_open("sgpsondewnpnC1.b1", "2026-09-21", "2026-09-21", cleanup_qc=True)
```

## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
24 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

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
act.qc.print_dqr("sgpsondewnpnC1.b1", "19700101", "20260923")
```

The handbook's own note on data quality: Plots of ARM sounding data from all sites may be accessed via DQ-Explorer, DQ-Plotbrowser, or DQ-Zoom tools provided by the ARM Data Quality Office (https://dq.arm.gov/). Ground-check values are compared with MAWS values to ensure no systematic bias appears over time. GRUAN GDP data for SGP, ENA, and NSA sites includes best possible vertically resolved uncertainty estimates, well-documented correction algorithms, and extensive metadata, providing an independent quality-assured alternative dataset.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Signal degradation and signal loss (RF interference) | Early termination of the sounding before balloon burst, visible as a truncated profile ending before expected altitude | MW41 software automatically terminates the launch if signal degrades; ARM follows manufacturer guidelines for antenna placement to mitigate; data... | (hb p. 7) |
| GPS RF spectrum interference (GPS jamming) | Loss or corruption of GPS-derived position/wind data | Rare since GPS jammers are generally illegal and primarily used by government entities; no specific mitigation given beyond noting rarity | (hb p. 7) |
| Solar heating of radiosonde temperature sensors | Warm bias in temperature profile increasing with altitude, uncorrected effects reaching up to 1K at 30km | Vaisala applies a proprietary correction in the MW41 software; GRUAN GDP offers an independent alternative solar radiation correction (differs from... | (hb p. 8) |
| First data point unreliable without airflow across sensors | Time-zero data point differs from expected in-flight sensor behavior; appears as a discontinuity if not replaced | First data point of launch is replaced with MAWS ground-truth data; if MAWS unavailable, radiosonde data is used instead | (hb p. 3) |
| Differences between GRUAN GDP and Vaisala EDT processed data | Small systematic offset between GDP and ARM (Vaisala) temperature values, +0.1K in troposphere growing to +0.35K near 35km | Both differences are within stated uncertainty limits of the two data products; users needing alternative correction can obtain GRUAN GDP data | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | No regular calibration is required since the ground-check phase uses measurements independent of the ground station hardware: humidity checked under physical 0% or 100% environment, and main temperature sensor compared with secondary temperature sensor onboard the radiosonde; ground-check values compared with MAWS... (hb p. 7) |
| Calibration interval | Performed prior to every flight (ground check) (hb p. 7) |
| Traceability | Manufacturer-independent standard humidity chamber used at SGP, ENA, and NSA manual launches for baselining against physical 0% and 100% humidity; manufacturer corrections applied only to 0% humidity check. (hb p. 7) |
| Routine maintenance | MW41 sounding software kept updated with latest Vaisala version; antennas checked for debris buildup; GPS card inside the SPS occasionally updated in compliance with GNSS/GPS system updates. (hb p. 7) |
| Maintenance interval | Not specified as a fixed interval; ongoing/occasional (hb p. 7) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MAWS (Meteorological Automatic Weather Station).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ADC` | ARM Data Center |
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `BBBS` | balloon-borne sounding system (old name) |
| `BF` | boundary facility |
| `CF` | Central Facility |
| `CLASS` | Cross-chain Loran Atmospheric Sounding System |
| `ENA` | Eastern North Atlantic |
| `GCOS` | Global Climate Observing System |
| `GDP` | GRUAN Data Product |
| `GNSS` | Global Navigation Satellite System |
| `GPS` | Global Positioning System |
| `GRUAN` | GCOS Reference Upper-Air Network |
| `IOP` | intensive operational period |


### References the handbook cites

- von Rohden, C, M Sommer, T Naebert, V Motuz, and RJ Dirksen. 2022. "Laboratory characterisation of the radiation temperature error of radiosondes and its application to the GRUAN data processing for the Vaisala RS41."...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sonde_handbook.pdf (15 pages, DOE/SC-ARM-TR-029, by E Keeler)
- Catalog record: ARM data-source index, `instrument_class_code=sonde`, read 2026-09-23
- Example file: `sgpsondewnpnC1.b1.20260921.113143.nc` from `sgpsondewnpnC1.b1`, 0.52 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
