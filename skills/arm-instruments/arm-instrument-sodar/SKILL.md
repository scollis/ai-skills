---
name: arm-instrument-sodar
description: ARM Mini Sound Detection and Ranging (sodar) - handbook-derived instrument reference. Measurement principle, reported quantities (Wind speed, Wind direction, Vertical wind speed, Vertical wind standard deviation, Average backscatter strength, Mean Doppler shift, Doppler width, Signal-to-noise ratio), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (anxsodarM1.b1) and the variable inventory of a real file. Use when working with sodar data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Profiling. Triggers - sodar, Mini Sound Detection and Ranging, anxsodarM1.b1, Wind speed, Wind direction, Vertical wind speed, Vertical wind standard deviation, Average backscatter strength, Mean Doppler shift, Atmospheric Profiling, Scintec, Inc. (Scintec Corporation) SODAR system.
---

# SODAR - Mini Sound Detection and Ranging

The SODAR wind profiler measures vertical profiles of horizontal and vertical wind speed/direction and backscattered acoustic signal strength between nominally 15 m and 500 m, deployed as part of the ARM Mobile Facility (AMF) instrumentation suite.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sodar` |
| Handbook | [DOE/SC-ARM-TR-154 / P Muradyan, R Coulter / May 2020](https://www.arm.gov/publications/tech_reports/handbooks/sodar_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Scintec, Inc. (Scintec Corporation) SODAR system |
| Primary measurements | Atmospheric turbulence; Horizontal wind; Vertical velocity |
| Record | 1997-04-01 to 2020-06-01 (retired) |
| Datastreams with data | 12 across 6 sites |
| Sites | anx, asi, cor, mao, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/sodar |


## Credit

Everything this skill knows about the instrument is the work of **P Muradyan, R Coulter** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> P Muradyan, R Coulter. *Sonic Detection and Ranging (SODAR) Wind Profiler Instrument Handbook*, DOE/SC-ARM-TR-154, May 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sodar_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The SODAR transmits acoustic energy into the atmosphere and measures the strength and frequency of backscattered energy. The strength of the backscattered signal is determined by the strength of temperature inhomogeneities with size on the order of 10 cm, and assuming the scattering elements move with the mean wind, the horizontal wind field can be derived. A single-phased array antenna transmits alternately along five pointing directions (one vertical, two in the north-south plane, two in the east-west plane, tilted ~14 degrees from vertical) to determine the three components of motion. Spectra are analyzed to produce estimates of mean Doppler shift (first moment), Doppler width (spectral width), noise level, and SNR at each range gate, from which wind speed, direction, and vertical velocity are derived.

**Siting.** The antenna is oriented in a horizontal plane so the in-phase beam travels vertically. The system transmits along five pointing directions: one vertical, two in the north-south vertical plane, two in the east-west vertical plane, with non-vertical beams tilted about 14 degrees from vertical. Because the beam components are not collocated in space, horizontal homogeneity is assumed to derive the wind vector at a single height. SODAR values are volume averages over nominally 10-20 meters in height by 9 degrees horizontally.

**Sampling.** native rate Transmits pulses at about 1−10 Hz; backscatter sampled at, e.g., 1 kHz; FFT takes on the order of 1 second per range gate; dwell time nominally 30−45 seconds per pointing direction; about five minutes elapse before system returns to beginning of its sequence (11−12 beam-power estimates saved in a 1-hour period); reported every Time-averaged profiles calculated over a user-defined period, usually 1 hour for ARM data; averaging Spectrum represents an average of several (e.g., 60) individual spectra obtained over several seconds (e.g., 30); about 30 spectra averaged together during dwell time (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Wind speed | m/s | - | 0.5 m/s (nominal accuracy) | - | (hb p. 10) |
| Wind direction | degrees relative to true... | - | 3° (nominal accuracy) | - | (hb p. 10) |
| Vertical wind speed | m/s; positive = upward | - | 0.3 m/s (nominal accuracy for radial wind... | - | (hb p. 10) |
| Vertical wind standard deviation | m/s | - | - | - | (hb p. 10) |
| Average backscatter strength | unitless | - | - | - | (hb p. 10) |
| Mean Doppler shift (frequency) | - | - | - | - | (hb p. 8) |
| Doppler width | - | - | - | - | (hb p. 8) |
| Signal-to-noise ratio (SNR) | - | - | - | - | (hb p. 8) |
| Height/range of measurement | m | nominally 15 m to 500 m | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Frequency | 2000−4500 Hz | (hb p. 15) |
| Maximum range | 500 m | (hb p. 15) |
| Range gate | 20−50 m | (hb p. 15) |
| Pulse length | 20−50 m | (hb p. 15) |
| # Spectra/ave spectrum | 1−100 | (hb p. 15) |
| Antenna size | approximately 1.5 m square | (hb p. 14) |
| Dynamic range (ATP) | at least 55 dB | (hb p. 15) |
| System sensitivity (ATP) | minimum detectable level of at least -127 dBm | (hb p. 15) |
| Transmit pulse rate | about 1−10 Hz | (hb p. 14) |
| Backscatter sampling rate | 1 kHz rate (example) | (hb p. 14) |
| FFT samples | 64 samples every 20 m in range | (hb p. 14) |
| Beam tilt angle | about 14 degrees from vertical | (hb p. 8) |


## The data

Verified example: **`anxsodarM1.b1`**, file `anxsodarM1.b1.20200529.000000.cdf`
(0.05 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=48, `height`=38 |
| Data variables | 11 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2020-05-29T00:00:00 to 2020-05-29T23:30:00 |
| sampling interval | variable |
| averaging interval | None |
| dod version | sodar-b1-2.0 |
| process version | ingest-sodar-1.4-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `backscatter` | unitless | time,height | - | Backscatter, as total intensity of received signal, filtered and... |
| `height` | m | height | - | Center of sodar height level |
| `instrument_error` | unitless | time,height | - | Instrument error codes |
| `time` | - | time | - | Time offset from midnight |
| `vertical_wind_speed` | m/s | time,height | - | Vertical component of wind speed |
| `vertical_wind_speed_std` | m/s | time,height | - | Standard deviation of vertical component of wind speed |
| `wind_direction` | degree | time,height | - | Horizontal wind direction |
| `wind_speed` | m/s | time,height | - | Horizontal wind speed |


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
                     params={"user": f"{user}:{token}", "ds": "anxsodarM1.b1",
                             "start": "2020-05-29", "end": "2020-05-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./anxsodarM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "anxsodarM1.b1", "2020-05-29", "2020-05-29")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("anxsodarM1.b1", "2020-05-29", "2020-05-29"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("anxsodarM1.b1", "19970401", "20260923")
```

The handbook's own note on data quality: No flags are applied during data ingest of the averaged winds; however, data are examined regularly by the instrument mentor for quality assurance via daily inspection of vertical time sections of hourly averaged wind and temperature over a 24-hour period. QC frequency is daily; QC delay is instantaneous/daily; QC type includes min/max flags, graphical plots, and intercomparisons; inputs are raw data; outputs are summary reports. The Data Quality Office website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting and assessing data quality. Data Quality Reports document...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Precipitation contamination (rain) | Large downward velocity in vertical velocity moments and elevated SNR extending to all heights; region of red/magenta in SNR profile plots; can lead to significant errors in estimated true... | Rainfall is more amenable to objective analysis detection due to large downward velocity; some precipitation-affected data is discarded by quality... | (hb p. 11) |
| Precipitation contamination (snow) | Similar to rain but harder to detect because snow has quite small terminal velocities, so it does not show the characteristic large downward velocity signature | None specifically stated beyond general QC review | (hb p. 11) |
| Beam non-collocation / horizontal inhomogeneity assumption | Wind vector at a single height derived from five non-collocated beams; errors when horizontal homogeneity assumption is violated | None beyond noting the assumption is made | (hb p. 11) |
| Height sampling difference between vertical and tilted beams | Vertical beam sampled at larger height intervals than tilted beams by factor 1/sin(elevation angle), approx. 3% difference; e.g., at nominal height of 1000 m (tilted beams), vertical beam... | None stated beyond noting it 'could be a significant difference in some situations' | (hb p. 11) |
| Disagreement with balloon-borne sounding system (BBSS) | SODAR winds/temperature values do not match BBSS values | Recognize SODAR is a 1-hour average and volume average (10-20 m height x 9 degrees horizontally) while BBSS is an instantaneous grab sample carried... | (hb p. 12) |
| No automated data quality flags applied at ingest | Averaged wind data files show no QC flags despite potential erroneous 'seemingly good' data | Data are examined regularly by the instrument mentor for quality assurance via daily inspection of vertical time sections | (hb p. 11) |
| Instrument blind range near surface | No data below nominally 15 m | None stated | (hb p. 7) |
| Maximum range limitation | No data above nominally 500 m; precipitation can extend effective range but with error potential | None stated | (hb p. 7) |
| Data loss during basic factory calibration (ATP) | All data lost during the 1-2 day ATP calibration period | None stated beyond noting duration | (hb p. 16) |
| Communication lines/links and ingest modules as data pipeline risk points | Potential effects on data stream from communication lines/links and ingest modules | None specifically stated | (hb p. 18) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Acceptance Test Plan (ATP) performed by Scintec personnel immediately before instruments are put into service; includes output power, center frequency, dynamic range (signal generator with variable attenuator, at least 55 dB), and system sensitivity (minimum detectable level of at least -127 dBm) checks. No true... (hb p. 15) |
| Calibration interval | Basic factory calibration (ATP) repeated yearly (hb p. 15) |
| Traceability | Scintec factory ATP; documented in ATP, system Operator's Manual supplied by Scintec, and Operators manual specific to SODAR supplied by instrument mentor (hb p. 15) |
| Routine maintenance | Factory-recommended: clean air filters, remove dust, check cables, inspect antenna, fences, exterior cables, clutter screens, guys, anchors. Mentor procedures: regular noise level checks, regular final amplifier current checks, daily data existence, vertical time sections of winds and temperatures, continuous daily... (hb p. 17) |
| Maintenance interval | Daily: check operation, verify data existence; Weekly: check data quality; Monthly: check system alignment, cables, output levels, antenna switching; Yearly: repeat ATP (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: radar wind profiler, balloon-borne sounding system (BBSS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `ATP` | Acceptance Test Plan |
| `BBBS` | balloon-borne sounding system |
| `DQO` | Data Quality Office |
| `FFT` | fast Fourier transform |
| `LST` | local standard time |
| `NCAR` | National Center for Atmospheric Research |
| `netCDF` | Network Common Data Form |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `QC` | quality control |
| `QME` | quality measurement experiment |
| `SNR` | signal-to-noise ratio |
| `SODAR` | Sonic Detection and Ranging |


### References the handbook cites

- Symposium on Lower Tropospheric Profiling: Needs and Technologies, Boulder, Colorado 10-13 September 1991. Sponsored by NOAA and NCAR.
- Third International Symposium on Tropospheric Profiling: Needs and Technologies, Max-Planck-Gesellschaft zur Forderung der Wissenschaften, Hamburg, Germany, 30 August-2 September 1994. Sponsored by NOAA/NCAR.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sodar_handbook.pdf (20 pages, DOE/SC-ARM-TR-154, by P Muradyan, R Coulter)
- Catalog record: ARM data-source index, `instrument_class_code=sodar`, read 2026-09-23
- Example file: `anxsodarM1.b1.20200529.000000.cdf` from `anxsodarM1.b1`, 0.05 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
