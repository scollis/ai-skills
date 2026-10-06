---
name: arm-instrument-co-air
description: ARM Carbon Monoxide- Airborne (co-air) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafcoF1.c1) and the variable inventory of a real file. Use when working with co-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Carbon. Triggers - co-air, Carbon Monoxide- Airborne, sgpaafcoF1.c1, Airborne Observations, Atmospheric Carbon, Tylan mass flow controller (FC-2900), ESRL, LBNL, NOAA, TE48C.
---

# CO-AIR - Carbon Monoxide- Airborne

The CO Mixing Ratio System provides continuous accurate measurements of carbon monoxide mixing ratio in dry air, deployed at the ARM SGP Central Facility 60-meter tower using a Thermo Electron 48C-TL trace level gas filter correlation CO analyzer.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `co-air` |
| Handbook | [DOE/SC-ARM/TR-072 / SC Biraud / February 2011](https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Carbon |
| Manufacturer / model | Thermo Electron Corporation Model 48C-TL trace level gas filter correlation CO analyzer; Tylan mass flow controller (FC-2900); MKS Pressure controller (model 640); Vaisala Dewpoint Transmitter DMT142 |
| Primary measurements | Atmospheric moisture; Carbon monoxide (CO) Concentration; Nitrogen oxides |
| Record | 2013-07-01 to 2026-09-24 (retired) |
| Datastreams with data | 15 across 7 sites |
| Sites | acx, cor, ena, mao, nsa, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/co-air |


## Credit

Everything this skill knows about the instrument is the work of **SC Biraud** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SC Biraud. *CO (Carbon Monoxide Mixing Ratio System) Handbook*, DOE/SC-ARM/TR-072, February 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `co-air`, ARM links no handbook to this class. The facts below come from the **Carbon Monoxide Mixing Ratio System** (`co`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `co-air` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

The Model 48C is based on the principle that carbon monoxide absorbs infrared radiation at a wavelength of 4.6 microns, and since infrared absorption is a non-linear measurement technique, the instrument electronics use an exact calibration curve to linearize the output over concentrations up to 10,000 ppm. Sample is drawn through the optical bench where radiation from an infrared source is chopped and passed through a gas filter alternating between CO and N2, then through a narrow bandpass interference filter into the optical bench where absorption by the sample gas occurs before falling on an infrared detector. The CO gas filter produces a reference beam that cannot be further attenuated by CO in the sample cell, while the N2 side of the filter wheel is transparent and produces a measure beam that can be absorbed by CO in the cell. The chopped detector signal is modulated by the alternation between the two gas filters with an amplitude related to CO concentration in the sample cell; other gases do not cause modulation since they absorb the reference and measure beams equally, so the gas filter correlation (GFC) system responds specifically to CO concentrations.

**Siting.** Deployed at the ARM SGP Central Facility (CF) 60-meter tower (36.607 °N, 97.489 °W, 314 meters above sea level); system deployed on May 25, 2005.

**Sampling.** native rate raw data time stamped every 5 seconds (a1 files); described elsewhere as 5-Hz data; reported every one sample measured for 5 minutes at a time; averaging reported value is the average of the last 2 minutes of the 5-minute sample (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Carbon monoxide mixing ratio in dry air | ppb (ppbv) | 60 to 1000 ppb | 4 ppb accuracy; uncertainty estimated on the... | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Zero Noise | 5.0 ppb RMS (120-second averaging time) | (hb p. 8) |
| Zero Drift (24 hour) | less than 100 ppb | (hb p. 8) |
| Response Time | 60 seconds (30-second averaging time) | (hb p. 8) |
| Precision | 10.0 ppb | (hb p. 8) |
| Sample Flow Rate | 0.5 liter/min | (hb p. 8) |
| Operating Temperature | 20°-30°C (may be safely operated over the range 5°-45°C) | (hb p. 8) |
| Power Requirements (analyzer) | 90-100 VAC; 210-240 VAC, 50 Hz, 100 Watts | (hb p. 8) |
| Tylan mass flow controller Flow | 0.5 LPM | (hb p. 8) |
| Tylan mass flow controller Step Response Time | 1 second (dependent on step request and conditions) | (hb p. 8) |
| Tylan mass flow controller Accuracy | ± 1.0% full scale | (hb p. 8) |
| Tylan mass flow controller Linearity | ± 0.5% full scale | (hb p. 8) |
| Tylan mass flow controller Repeatability | ± 0.2% full scale | (hb p. 8) |
| Tylan mass flow controller Supply Voltage | ± 12 VDC to ± 18 VDC | (hb p. 8) |
| Tylan mass flow controller Supply Current | 110 mA nominal (125 mA max @ ± 18 VDC) | (hb p. 8) |
| Tylan mass flow controller Power Consumption | 3.3 watts @ ± 15 volts | (hb p. 8) |
| Tylan mass flow controller Input/Output Signal | 0-5 VDC | (hb p. 8) |
| MKS Pressure controller Pressure | 100 PSI | (hb p. 8) |
| MKS Pressure controller Supply Voltage | 15 VDC ± 5% | (hb p. 8) |
| MKS Pressure controller Supply Current | 200 mA max | (hb p. 8) |
| MKS Pressure controller Input/Output Signal | 0-5 VDC | (hb p. 8) |
| Vaisala DMT142 Operating Dewpoint Temperature | -50°C +60 °C (-76°F +140 °F) | (hb p. 9) |
| Vaisala DMT142 Accuracy | ±3 °C (± 5.4 °F) | (hb p. 9) |
| Range | 60 to 1000 ppb | (hb p. 11) |
| Accuracy | 4 ppb | (hb p. 11) |
| Uncertainty | estimated to be on the order of 5 ppb | (hb p. 11) |
| Input Voltage | 105-125 VAC, 60Hz | (hb p. 11) |


_2 further specification rows are in the handbook._

## The data

Verified example: **`sgpaafcoF1.c1`**, file `sgpaafcoF1.c1.20160920.202755.nc`
(0.21 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=5104 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aafco-c1-1.0 |
| process version | ingest-aafcome-1.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `co` | ppmv | time | - | Carbon monoxide (CO) mixing ratio calculated with nominal sensitivity... |
| `h2o` | ppmv | time | - | Water vapor mixing ratio calculated with nominal sensitivity... |
| `n2o` | ppmv | time | - | Nitrous oxide (N2O) mixing ratio calculated with nominal sensitivity... |
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
                     params={"user": f"{user}:{token}", "ds": "sgpaafcoF1.c1",
                             "start": "2016-09-20", "end": "2016-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaafcoF1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaafcoF1.c1", "2016-09-20", "2016-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaafcoF1.c1", "2016-09-20", "2016-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("h2o")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaafcoF1.c1", "20130701", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality is evaluated by inspecting Quality Control (qc) flags and variables in the processed datastream, achieved in two stages: raw a0 files are processed to intermediate a1 daily files (time-stamped 5-Hz data, not yet corrected for offset/drift; truncated lines from system hiccups are purged); a1 files are then processed to calculate CO mixing ratios and associated qc flags by averaging concentrations for each channel (sampled, zero, span air), correcting for instrument offset, finding calibration data to correct for drifts, and writing output in netCDF format. Almost every variable...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Windows operating system 'hiccups' causing truncated data lines | a0 raw data files contain truncated lines | Truncated lines are purged during the a0 to a1 processing | (hb p. 10) |
| Instrument warning/bad range for CO concentration | qc_co flag set to warning when 50 less than  CO less than  60 or 600 less than  CO less than  800 ppb; set to bad when CO less than  50 or CO greater than  800 ppb | Flagged via qc_co variable in Table 1/Table 2 scheme | (hb p. 10) |
| Internal temperature (int_temp) out of range | qc flag warning when 25 less than  int_temp less than  30 or 40 less than  int_temp less than  45 °C; bad when int_temp less than  25 or int_temp greater than  45 °C | Flagged via qc_int_temp variable | (hb p. 10) |
| Chamber temperature (chamber_temp) out of range | qc flag warning when 35.0 less than  chamber_temp less than  42.4 or 47.5 less than  chamber_temp less than  55.0 °C; bad when chamber_temp less than  35.0 or greater than  55.0 °C | Flagged via qc_chamber_temp variable | (hb p. 10) |
| Automatic gain control (agc) out of range | qc flag warning when 1.90e5 less than  agc less than  1.95e5 or 2.05e5 less than  agc less than  2.1e5 Hz; bad when agc less than  1.9e5 or agc greater than  2.1e5 Hz | Flagged via qc_agc variable | (hb p. 10) |
| TE48C pressure (pres_TE48C) out of range | qc flag warning when 790 less than  pres_TE48C less than  800 or 820 less than  pres_TE48C less than  830 Torr; bad when pres_TE48C less than  790 or greater than  830 Torr | Flagged via qc_pres_TE48C variable | (hb p. 10) |
| TE48C flow (flow_TE48C) out of range | qc flag warning when 0.40 less than  flow_TE48C less than  0.45 or 0.55 less than  flow_TE48C less than  0.60 LPM; bad when flow_TE48C less than  0.40 or greater than  0.60 LPM | Flagged via qc_flow_TE48C variable | (hb p. 10) |
| Control pressure (pres_control) out of range | qc flag warning when 785 less than  pres_control less than  795 or 805 less than  pres_control less than  815 Torr; bad when pres_control less than  785 or greater than  815 Torr | Flagged via qc_pres_control variable | (hb p. 10) |
| Control flow (flow_control) out of range | qc flag warning when 0.40 less than  flow_control less than  0.45 or 0.55 less than  flow_control less than  1.00 LPM; bad when flow_control less than  0.40 or greater than  1.00 LPM | Flagged via qc_flow_control variable | (hb p. 10) |
| Dew point temperature (dpt) out of range | qc flag warning when -15 less than  dpt less than  -10 °C; bad when dpt greater than  -10.0 °C | Flagged via qc_dpt variable | (hb p. 10) |
| Zero and span drift of the analyzer | Would appear as offset in raw signal relative to known zero/span standards if uncorrected | Periodically calibrated out using a CO scrubber and two concentrations of span gas (100 and 300 ppb CO in air); corrections for offset and span... | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Every 6 hours, two calibration standards certified by NOAA ESRL at approximately 100 and 300 ppb are run; sample CO concentration is calculated with the standards run before and after it; instrument electronics periodically calibrate out zero and span drifts using a CO scrubber and two concentrations of span gas (100... (hb p. 14) |
| Calibration interval | every 6 hours (hb p. 14) |
| Traceability | Primary standards: SCOTT MARRIN 150A CA05962, CO in air 95±1 ppb, NOAA - D. Kitzis, 12/1/2003; SCOTT MARRIN 150A CA05909, CO in air 292.5±2.9 ppb, NOAA - D. Kitzis, 12/1/2003 (hb p. 14) |
| Routine maintenance | ARM staff performs preventive maintenance checks and posts post-preventive maintenance reports on the Internet; ARM carbon staff at LBNL checks these reports; instrument mentor routinely views graphical displays of CO concentrations, flow rate, pressure, automatic gain control, and dew point temperature. (hb p. 14) |
| Maintenance interval | weekly (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `CF` | Central Facility |
| `CO` | Carbon Monoxide |
| `DQ` | Data Quality |
| `ESRL` | National Earth System Research Laboratory |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `NOAA` | National Oceanic & Atmospheric Administration |
| `PC` | personal computer |
| `SGP` | Southern Great Plains |
| `STS` | Site Transfer Suite |
| `QC` | Quality Control |
| `TE48C` | Thermo Electron 48C |


### References the handbook cites

- Chaney, LW, and WA McClenny. 1977. "Unique ambient carbon monoxide monitor based on gas filter correlation: performance and application." Environmental Science and Technology 11: 1186–1190.
- Dickerson RR, and AC Delany. 1988. "Modification of a commercial gas filter correlation CO detector for enhanced sensitivity." Journal of Atmospheric and Oceanic Technology 5: 424–431.
- Novelli, PC, JW Elkins, and LP Steele. 1991. "The development and evaluation of a gravimetric reference scale for measurements of atmospheric carbon monoxide." Journal of Geophysical Research 96: 13,109–13,121.
- Parrish, DD. JS Holloway, and FC Fehsenfeld. 1994. "Routine, continuous measurement of carbon monoxide with parts per billion precision." Environmental Science and Technology 28: 1615–1618.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/co_handbook.pdf (15 pages, DOE/SC-ARM/TR-072, by SC Biraud)
- Catalog record: ARM data-source index, `instrument_class_code=co-air`, read 2026-09-24
- Example file: `sgpaafcoF1.c1.20160920.202755.nc` from `sgpaafcoF1.c1`, 0.21 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
