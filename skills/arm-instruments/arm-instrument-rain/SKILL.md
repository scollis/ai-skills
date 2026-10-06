---
name: arm-instrument-rain
description: ARM Rain Gauge (rain) - handbook-derived instrument reference. Measurement principle, reported quantities (Precipitation, Rainfall rate, Precipitation amount, Precipitation rate, Sensor temperature, Sensor weight, Sensor frequency, Logger panel temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgprainwbC1.b1) and the variable inventory of a real file. Use when working with rain data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - rain, Rain Gauge, sgprainwbC1.b1, Precipitation, Rainfall rate, Precipitation amount, Precipitation rate, Sensor temperature, Sensor weight, Surface Meteorology, Tipping Buckets - NovaLynx Corp., Weighing Bucket Rain Gauges - Belfort Instrument Company, DIST, RMSE, VDIS.
---

# RAIN - Rain Gauge

The rain gauge (RAIN datastream) gathers and measures the amount of liquid precipitation over time, deployed near disdrometers at ARM sites using either a tipping bucket or weighing bucket mechanism.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `rain` |
| Handbook | [DOE/SC-ARM-TR-110 / MJ Bartholomew / January 2016](https://www.arm.gov/publications/tech_reports/handbooks/rain_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Tipping Buckets: NovaLynx Corp.; Weighing Bucket Rain Gauges: Belfort Instrument Company |
| Primary measurements | Atmospheric pressure; Precipitation |
| Record | 2006-03-01 to 2026-09-22 (active) |
| Datastreams with data | 25 across 12 sites |
| Sites | asi, bnf, cor, ena, epc, gan, guc, mao, mos, sgp, tmp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/rain |


## Credit

Everything this skill knows about the instrument is the work of **MJ Bartholomew** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MJ Bartholomew. *Rain Gauge Instrument Handbook*, DOE/SC-ARM-TR-110, January 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/rain_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Tipping bucket rain gauges collect precipitation in a funnel that channels water into small buckets on a pivot; each bucket tip corresponds to a fixed amount of rainfall (0.254 mm per tip) and tips are counted by a data logger. Weighing bucket rain gauges instead measure the total weight of accumulated precipitation in a bucket using load sensors (weight1, weight2, weight3) and frequency outputs, from which precipitation amount and rate are derived. Data acquisition for the tipping bucket is carried out with a CR1000 Campbell Scientific data logger, sampling once a minute. The rain gauges are sited near disdrometers to complement drop-size distribution measurements with bulk precipitation totals.

**Siting.** The site requirements for the rain gauges include a solid footing. A wind screen will be required for an open Southern Great Plains prairie installation and may be needed at the ARM Darwin site as well. Nearby objects should be placed away at a distance least twice their height. If snowfall could occur at the site, the opening of the gauge should be above average snow level. Note: lat/lon/alt refer to the ground where the instrument is sited, NOT the height of the sensor.

**Sampling.** native rate once a minute (both disdrometer and rain gauge); reported every 1 min (most variables); some dimensional variables 1 min or 30 min; some QC variables 60 min (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Precipitation (tipping bucket) | millimeters | - | 0.01 mm | - | (hb p. 9) |
| Rainfall rate (tipping bucket) | millimeters/hr | - | 0.6 mm/hr | - | (hb p. 9) |
| Precipitation amount (weighing bucket) | Millimeters | - | 0.01 mm | - | (hb p. 10) |
| Precipitation rate (weighing bucket) | Millimeters/hour | - | 0.6 mm/hr | - | (hb p. 10) |
| Sensor temperature (1,2,3) | Degrees C | - | - | - | (hb p. 10) |
| Sensor weight (1,2,3) | kg | - | - | - | (hb p. 10) |
| Sensor frequency (1,2,3) | Hz | - | - | - | (hb p. 10) |
| Logger panel temperature | Degrees C | - | - | - | (hb p. 10) |
| Logger minimum voltage | volts | - | - | - | (hb p. 10) |
| Bucket total weight | kg | - | - | - | (hb p. 10) |
| Bucket total mm of precipitation | Millimeters | - | - | - | (hb p. 10) |
| Drop diameter (impact disdrometer, for comparison context) | mm | 0.3 to 5.4 mm | 3% of drop diameter (center of sensor); ±5%... | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Precipitation uncertainty (tipping and weighing bucket) | 0.01 mm | (hb p. 9) |
| Rain rate uncertainty | 0.6 mm/hr | (hb p. 9) |
| Disdrometer drop-size measurement range | 0.3 to 5.4 mm | (hb p. 9) |
| Disdrometer drop-size accuracy | 3% of drop diameter (center of sensor); ±5% standard deviation over sensitive surface | (hb p. 9) |
| qc_precip_tbrg minimum/maximum | 0 / 10 | (hb p. 12) |
| qc_vbat minimum/maximum | 9.6 / 16 | (hb p. 12) |
| qc_batt_min minimum/maximum | 9.6 / 16 | (hb p. 12) |
| qc_panel_temp minimum/maximum | -25.0 / 50.0 | (hb p. 12) |
| qc_precip minimum/maximum (weighing bucket) | -10 / 200 | (hb p. 13) |
| qc_precip_rate minimum/maximum | -600 / 1200 | (hb p. 13) |
| qc_temp1/2/3 minimum/maximum | -40 / 100 | (hb p. 13) |
| qc_weight1/2/3 minimum/maximum | 0.33 / 8 | (hb p. 13) |
| qc_ptemp minimum/maximum | -40 / 100 | (hb p. 13) |
| qc_volt_min minimum/maximum | 8 / 20 | (hb p. 13) |
| qc_total_weight minimum/maximum | 1 / 8 | (hb p. 13) |
| qc_total_mm minimum/maximum | -20 / 200 | (hb p. 13) |
| qc_scans_per_minute minimum/maximum | 16 / 21 | (hb p. 13) |
| qc_stat_latch minimum/maximum | 000 / 111 | (hb p. 13) |
| qc_error_latch minimum/maximum | 0 / 1 | (hb p. 13) |
| Tip test rain amount per tip | 0.254 mm per tip (rain_mm = # tips × 0.254) | (hb p. 18) |


## The data

Verified example: **`sgprainwbC1.b1`**, file `sgprainwbC1.b1.20160601.000000.cdf`
(0.07 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=288, `bound`=2 |
| Data variables | 39 |
| QC variables | 16 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2016-06-01T00:00:00 to 2016-06-01T23:55:00 |
| sampling interval | 1 minute |
| averaging interval | 5 minutes |
| dod version | rainwb-b1-1.0 |
| process version | ingest-rainwb-1.1-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `frequency1` | Hz | time | yes | Frequency average, sensor 1 |
| `frequency2` | Hz | time | yes | Frequency average, sensor 2 |
| `frequency3` | Hz | time | yes | Frequency average, sensor 3 |
| `maintenance_cnt` | unitless | time | yes | Total maintenance count |
| `precip` | mm | time | yes | Total precipitation over one minute sampling period |
| `precip_rate` | mm/hr | time | yes | Precipitation rate |
| `ptemp` | degC | time | yes | Panel temperature average |
| `temp1` | degC | time | yes | Temperature average, sensor 1 |
| `temp2` | degC | time | yes | Temperature average, sensor 2 |
| `temp3` | degC | time | yes | Temperature average, sensor 3 |
| `total_mm` | mm | time | yes | Millimeters of precipitation accumulated in the gauge since the last... |
| `total_weight` | kg | time | yes | Weight of accumulated precipitation in the gauge since the last tare |
| `volt_min` | V | time | yes | Voltage minimum |
| `weight1` | kg | time | yes | Sensor 1 maximum weight |
| `weight2` | kg | time | yes | Sensor 2 maximum weight |
| `weight3` | kg | time | yes | Sensor 3 maximum weight |
| `stat_latch` | unitless | time | - | Sensor status |
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
                     params={"user": f"{user}:{token}", "ds": "sgprainwbC1.b1",
                             "start": "2016-06-01", "end": "2016-06-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgprainwbC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgprainwbC1.b1", "2016-06-01", "2016-06-01")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgprainwbC1.b1", "2016-06-01", "2016-06-01"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("precip", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

16 `qc_` companion variables cover 16 of the
39 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_precip"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("precip", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["precip", "precip_rate", "weight1"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgprainwbC1.b1.20160601.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `precip` | Sensor status for transducer #2 indicates a potential problem,... | 288 | 100.0 |
| `precip_rate` | Sensor status for transducer #2 indicates a potential problem,... | 288 | 100.0 |
| `total_weight` | Sensor status for transducer #2 indicates a potential problem,... | 288 | 100.0 |
| `total_mm` | Sensor status for transducer #2 indicates a potential problem,... | 288 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgprainwbC1.b1", "20060301", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: If data are missing for a sample time, a missing_value of -999 is assigned to that field. Data-quality flags are provided for tipping bucket (Table 5: qc_time, qc_precip_tbrg, qc_vbat, qc_batt_min, qc_batt_max, qc_panel_temp, qc_panel_min, qc_panel_max) and weighing bucket (Table 6: qc_time_offset, time, qc_precip, qc_precip_rate, qc_temp1/2/3, qc_weight1/2/3, qc_frequency1/2/3, qc_ptemp, qc_volt_min, qc_total_weight, qc_total_mm, qc_scans_per_minute, qc_stat_latch, qc_error_latch) with minimum/maximum bounds. Data-Quality Health and Status (DQ HandS) and NCVweb are used for interactive...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Drop impact location dependence on disdrometer sensor | Pulse amplitudes of drops of equal diameter form a distribution around the average amplitude rather than a single value; measured drop diameters show ~±5% standard deviation spread even for... | Accuracy specified as ±5% assuming drops evenly distributed over sensitive surface; 3% uncertainty only applies to drops landing at very center of... | (hb p. 9) |
| Missing data | Field value of -999 assigned when data are missing for a sample time | Recognize -999 as missing_value flag | (hb p. 12) |
| Tipping bucket vs weighing bucket discrepancy | Total rain amounts over an event differing by more than 15% between weighing/tipping bucket comparisons when rainfall rate is between 1 and 10 mm/hr for several hours | Compare tipping bucket and weighing bucket totals over event; agreement should be within 15%; otherwise investigate via QC flags | (hb p. 11) |
| Debris/blockage in funnel | Reduced or anomalous precipitation totals if funnel openings are clogged | Remove rain gauge funnel and ensure both large and small funnels are clear of debris during maintenance | (hb p. 18) |
| Snow accumulation blocking gauge opening | Precipitation under-catch or zero readings during/after snowfall if gauge opening is buried | Gauge opening should be positioned above average snow level at sites where snowfall could occur | (hb p. 16) |
| Wind effects on catch | Under-catch or noisy precipitation totals at open, windy sites | Install wind screen at open prairie sites (e.g., Southern Great Plains) and possibly at Darwin | (hb p. 16) |
| Nearby obstacles affecting catch | Anomalous or reduced precipitation catch due to wind shadow/turbulence from nearby structures | Site nearby objects at a distance at least twice their height from the gauge | (hb p. 16) |
| Clock drift between data logger and server | Timestamps in RAIN datastream offset from true time if station clock drifts | LoggerNet automatically syncs station clock to server clock if times differ by 1 second or more; times should never differ by more than 1 minute;... | (hb p. 18) |
| Bucket tip mechanism sticking | Missed or inconsistent tips in tipping bucket counts | Manually tip the rain gauge bucket several times during maintenance to verify free movement | (hb p. 18) |
| Sensor/wiring damage or water intrusion | Erratic or missing readings, possible connector faults | Check conduits, cables, and connectors for damage, water intrusion, and tightness during visual inspection | (hb p. 17) |
| Battery voltage out of range | qc_vbat, qc_batt_min, qc_batt_max flags trigger outside 9.6-16 V range | Monitored via QC flags; check power system if flagged | (hb p. 12) |
| Panel/logger temperature out of range | qc_panel_temp, qc_ptemp flags trigger outside specified min/max bounds | Monitored via QC flags | (hb p. 12) |
| Sensor status/error latch flags | stat_latch and error_latch variables indicate sensor status/error conditions (qc_stat_latch, qc_error_latch) | Monitor via QC flags for weighing bucket sensor health | (hb p. 13) |
| Scan rate irregularities | scans_per_minute variable and qc_scans_per_minute flag outside 16-21 range indicating logger scan issues | Monitored via QC flag | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Tipping bucket gauges follow calibration procedures used for the ARM MET system; tip test conducted (see maintenance); full calibration to be done via ARM's dynamic calibration system when ready. (hb p. 17) |
| Calibration interval | Tip test once every 2 weeks; full calibration once a year (when dynamic calibration system is ready) (hb p. 17) |
| Routine maintenance | Weekly inspection: site ground check for hazards (rodent burrows, settling in trenches, insect nests); visual inspection of conduit, cables, connectors; check CR1000 data logger LED (should flash once per second); check power LED on Disdrometer Processor (should be lit green); check clock values on LoggerNet Connect... (hb p. 17) |
| Maintenance interval | Weekly (general); tip test every 2 weeks; full calibration annually (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: DISD (disdrometer), VDIS (video disdrometer), MET (surface meteorology instrument suite).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `DIST` | disdrometer |
| `DQ` | data quality |
| `LED` | light-emitting diode |
| `PM` | planned maintenance |
| `QME` | quality measurement experiment |
| `RMSE` | root-mean-square error |
| `VAP` | value-added products |
| `VDIS` | video disdrometer |


### References the handbook cites

- 260-2500e-manual.pdf (Tipping Bucket Manual)
- Belfort AEPG Manual Rev 11162012 (Weighing Bucket Manual)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/rain_handbook.pdf (21 pages, DOE/SC-ARM-TR-110, by MJ Bartholomew)
- Catalog record: ARM data-source index, `instrument_class_code=rain`, read 2026-09-23
- Example file: `sgprainwbC1.b1.20160601.000000.cdf` from `sgprainwbC1.b1`, 0.07 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
