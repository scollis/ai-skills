---
name: arm-instrument-isssonde
description: ARM Integrated Sounding System (isssonde) - handbook-derived instrument reference. Measurement principle, reported quantities (Pressure, Temperature, Relative humidity, Wind speed, Wind direction, Altitude, Dew point, Ascent rate), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaisssonde10sC1.b1) and the variable inventory of a real file. Use when working with isssonde data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Profiling. Triggers - isssonde, Integrated Sounding System, nsaisssonde10sC1.b1, Pressure, Temperature, Relative humidity, Wind speed, Wind direction, Altitude, Atmospheric Profiling, ASCII, BBBS, CLASS, GCOS.
---

# ISSSONDE - Integrated Sounding System

The balloon-borne sounding system (SONDE) launches Vaisala RS-41SGP radiosondes on weather balloons from ARM sites to provide in situ vertical profiles of atmospheric thermodynamic state, wind speed, and wind direction as the balloon ascends.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `isssonde` |
| Handbook | [DOE/SC-ARM-TR-029 / E Keeler / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/sonde_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Vaisala MW41 sounding system with RS-41SGP radiosondes (AS41 autosonde at NSA C1) |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind |
| Record | 1996-03-01 to 2002-05-14 (retired) |
| Datastreams with data | 5 across 2 sites |
| Sites | nsa, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/isssonde |


## Credit

Everything this skill knows about the instrument is the work of **E Keeler** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> E Keeler. *Balloon-Borne Sounding System (SONDE) Instrument Handbook*, DOE/SC-ARM-TR-029, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sonde_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `isssonde`, ARM links no handbook to this class. The facts below come from the **Balloon-Borne Sounding System** (`sonde`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `isssonde` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

The RS-41SGP radiosonde carries a platinum resistor temperature sensor, a thin-film capacitor humidity sensor, and a silicon capacitor pressure sensor, along with GPS-derived wind speed, wind direction, and heights, all measured once every second or every 5 meters of ascent. A 350g balloon filled with lifting gas carries the radiosonde to achieve a 5 m/s ascent rate. Prior to launch, a ground-check process compares the platinum resistor temperature sensor against the humidity sensor's temperature element, and the humidity sensor is baselined to a physical 0% humidity reference (and, at some sites, also 100% humidity) with the MW41 software applying a correction based on these measurements. The MAWS (Meteorological Automatic Weather Station) provides the first data point (time zero) as ground truth since the radiosonde needs air moving across its sensors for accurate readings. RF signals from the radiosonde are received by ground station antennas and decoded by the Signal Processing System (SPS), which passes data to the MW41 software for processing and distribution.

**Siting.** All sites have manual launch systems with the exception of North Slope of Alaska (NSA) C1, which uses an AS41 autosonde. Launch frequency and times vary by site (see Table 1): SGP 2/day, ENA 2/day, NSA 4/day, AMF1/AMF2/AMF3 4/day varying with campaign requirements. ARM follows manufacturer guidelines for antenna placement.

**Sampling.** native rate once every second or one data point every 5 meters ascending (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Pressure | hPa | Surface pressure to 3 hPa | greater than  100 hPa: 1.0 hPa; 100 - 3 hPa:... | 0.01 hPa | (hb p. 10) |
| Temperature | °C | -90 to +60°C | 0.3 °C less than  16km; 0.3 °C greater than ... | 0.01°C | (hb p. 10) |
| Relative humidity | %RH | 0 to 100 %RH | 3 %RH (combined uncertainty in sounding) | 0.1 %RH | (hb p. 10) |
| Wind speed | m/s | less than  180 m/s | 0.15 m/s (combined uncertainty in sounding) | 0.1 m/s | (hb p. 10) |
| Wind direction | deg | 0 to 360 deg | 2 deg (combined uncertainty in sounding) | 0.1 deg | (hb p. 10) |
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
| Response time - Temperature | 20 °C: less than  0.3 s, −40 °C: less than  10 s | (hb p. 10) |
| Repeatability - Pressure | greater than  100 hPa: 0.4 hPa, 100 - 3 hPa: 0.3 hPa | (hb p. 10) |
| Repeatability - Temperature | 0.1 °C | (hb p. 10) |
| Repeatability - Humidity | 2 %RH | (hb p. 10) |
| Reproducibility - Pressure | greater than  100 hPa: 0.5 hPa, 100 - 3 hPa: 0.3 hPa | (hb p. 10) |
| Reproducibility - Temperature | 0.15 °C greater than  100hPa, 0.30 °C less than  100hPa | (hb p. 10) |
| Reproducibility - Humidity | 2 %RH | (hb p. 10) |
| Combined uncertainty in sounding - Pressure | greater than  100 hPa: 1.0 hPa, 100 - 3 hPa: 0.6 hPa | (hb p. 10) |
| Combined uncertainty in sounding - Temperature | 0.3 °C less than  16km, 0.3 °C greater than  16km | (hb p. 10) |
| Combined uncertainty in sounding - Humidity | 3 %RH | (hb p. 10) |
| Combined uncertainty in sounding - Wind Speed | 0.15 m/s | (hb p. 10) |
| Combined uncertainty in sounding - Wind Direction | 2 deg | (hb p. 10) |
| Balloon | 350g balloon filled with enough lifting gas for an ascent rate of 5 m/s | (hb p. 7) |


## The data

Verified example: **`nsaisssonde10sC1.b1`**, file `nsaisssonde10sC1.b1.20020510.230348.cdf`
(0.1 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=720 |
| Data variables | 28 |
| QC variables | 6 (`qc_` companions) |
| Median time step | 10 s |
| File time span | 2002-05-10T23:03:48 to 2002-05-11T01:04:13 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `asc` | m/s | time | yes | Ascent Rate |
| `dp` | C | time | yes | Dewpoint Temperature |
| `pres` | hPa | time | yes | Pressure |
| `rh` | % | time | yes | Relative Humidity |
| `tdry` | C | time | yes | Dry Bulb Temperature |
| `time` | - | time | yes | Time offset from midnight |
| `ang` | deg | time | - | Azimuth Angle; degrees to sonde from launch point |
| `deg` | deg | time | - | Wind Direction |
| `pres_std` | hPa | time | - | Pressure, Standard Deviation |
| `rh_std` | % | time | - | Relative Humidity, Standard Deviation |
| `rng` | km | time | - | Range from launch point |
| `tdry_std` | C | time | - | Dry Bulb Temperature, Standard Deviation |
| `u_wind` | m/s | time | - | Eastward Wind Component |
| `u_wind_std` | m/s | time | - | Eastward Wind Component, Standard Deviation |
| `v_wind` | m/s | time | - | Northward Wind Component |
| `v_wind_std` | m/s | time | - | Northward Wind Component, Standard Deviation |
| `wspd` | m/s | time | - | Wind Speed |
| `wspd_std` | m/s | time | - | Wind Speed, Standard Deviation |


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
                     params={"user": f"{user}:{token}", "ds": "nsaisssonde10sC1.b1",
                             "start": "2002-05-10", "end": "2002-05-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsaisssonde10sC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsaisssonde10sC1.b1", "2002-05-10", "2002-05-10")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsaisssonde10sC1.b1", "2002-05-10", "2002-05-10"))   # cite what you pulled
```
### First look

A sounding: the profile, not a time series.

```python
import matplotlib.pyplot as plt

# A skew-T is the conventional view, but ACT's SkewTDisplay goes through MetPy,
# which raises InvalidSoundingError when the profile contains any pressure
# reversal - and raw ARM soundings routinely do. Filter to monotonic pressure
# first if you want the skew-T; this plain profile always runs.
fig, ax = plt.subplots(figsize=(4.5, 6))
ax.plot(ds["tdry"], ds["pres"], label="tdry")
ax.plot(ds["dp"], ds["pres"], label="dp")
ax.invert_yaxis()
ax.set_xlabel("degC"); ax.set_ylabel("pres"); ax.legend()
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```

## Quality control in this datastream

6 `qc_` companion variables cover 5 of the
28 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_pres"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("pres", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["pres", "tdry", "dp"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsaisssonde10sC1.b1.20020510.230348.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `pres` | Value is equal to missing_value. | 493 | 68.4722 |
| `dp` | Value is equal to missing_value. | 493 | 68.4722 |
| `asc` | Value is equal to missing_value. | 493 | 68.4722 |
| `tdry` | Value is equal to missing_value. | 492 | 68.3333 |
| `rh` | Value is equal to missing_value. | 492 | 68.3333 |
| `asc` | Difference between current and previous values exceeds... | 34 | 4.7222 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("nsaisssonde10sC1.b1", "19960301", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The ARM Data Quality Office (dq.arm.gov) provides tools to view data including DQ-Explorer, DQ-Plotbrowser, and DQ-Zoom. Ground-check values are compared with MAWS values to ensure no systematic bias appears over time. GRUAN produces an independent GRUAN Data Product (GDP) for SGP, ENA, and NSA sites with vertically resolved uncertainty estimates, documented correction algorithms, and extensive metadata, which can be used to cross-check ARM/Vaisala processed data.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Signal degradation and signal loss (RF interference) | Early termination of sounding before balloon burst, seen as truncated profile in data | MW41 software automatically terminates the launch if the signal degrades; ARM follows manufacturer guidelines for antenna placement to mitigate; data... | (hb p. 12) |
| GPS RF interference/jamming | Loss or degradation of GPS-derived position, wind, or height data | Rare since GPS jammers are generally illegal and primarily used by other government entities | (hb p. 12) |
| Solar heating of radiosonde temperature sensors | Uncorrected effects can reach up to 1K at 30km; apparent warm bias in temperature profile at high altitude | Vaisala applies a proprietary correction in MW41 software; ARM data contains this correction; GRUAN Data Product offers an alternative independent... | (hb p. 13) |
| First data point sensor inaccuracy (radiosonde needs airflow across sensors) | Time-zero data point would be anomalous if taken directly from radiosonde before airflow is established | First data point is replaced with MAWS ground-truth data; if MAWS data unavailable, radiosonde data is used instead | (hb p. 8) |
| Ground-check failure | Radiosonde not launched if it fails ground-check process | Radiosonde is discarded/not launched if it fails ground check | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | No regular calibration is required for the SONDE systems since the ground-check phase uses measurements independent of the ground station hardware; humidity is checked under a physical 0% or 100% environment and the main temperature sensor is compared with a secondary temperature sensor onboard the radiosonde.... (hb p. 12) |
| Calibration interval | prior to every flight (ground check) (hb p. 12) |
| Traceability | manufacturer-independent standard humidity chamber used at SGP, ENA, and NSA manual launches (hb p. 12) |
| Routine maintenance | MW41 sounding software kept updated with latest Vaisala version; antennas checked for debris buildup; GPS card inside the SPS occasionally updated in compliance with GNSS/GPS system updates. (hb p. 12) |
| Maintenance interval | occasional/as needed (hb p. 12) |


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
- Catalog record: ARM data-source index, `instrument_class_code=isssonde`, read 2026-09-24
- Example file: `nsaisssonde10sC1.b1.20020510.230348.cdf` from `nsaisssonde10sC1.b1`, 0.1 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
