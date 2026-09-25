---
name: arm-instrument-mettwr
description: ARM Surface and Tower Meteorological Instrumentation at NSA (mettwr) - handbook-derived instrument reference. Measurement principle, reported quantities (wind speed, wind direction, air temperature, dew point, humidity, barometric pressure, visibility, precipitation), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsapwsC2.b1) and the variable inventory of a real file. Use when working with mettwr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - mettwr, Surface and Tower Meteorological Instrumentation at NSA, nsapwsC2.b1, wind speed, wind direction, air temperature, dew point, humidity, barometric pressure, Surface Meteorology, METTWR2H, METTWR4H, AMET, BMET.
---

# METTWR - Surface and Tower Meteorological Instrumentation at NSA

Conventional in situ sensors mounted on towers at Atqasuk (10-m tower) and Barrow (40-m tower) at NSA measure wind speed, wind direction, air temperature, dew point, humidity, and obtain barometric pressure, visibility, and precipitation data from sensors at or near the base of the tower.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 4 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mettwr` |
| Handbook | [M.T. Ritsche / January 2006](https://www.arm.gov/publications/tech_reports/handbooks/mettwr_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation; Visibility |
| Record | 1998-03-20 to 2003-10-25 (retired) |
| Datastreams with data | 14 across 1 sites |
| Sites | nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/mettwr |


## Credit

Everything this skill knows about the instrument is the work of **M.T. Ritsche** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> M.T. Ritsche. *Surface and Tower Meteorological Instrumentation at NSA*, January 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mettwr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrumentation uses mainly conventional in situ sensors mounted on a tower to measure wind speed, wind direction, air temperature, dew point and humidity. At Atqasuk, temperature and relative humidity probes are mounted at 2 m and 5 m on the 10-m tower, with a Chilled Mirror Hygrometer located at 1 m for comparison purposes. At Barrow, sensors are mounted at four different heights (2 m, 10 m, 20 m, and 40 m) on a 40-m tower to obtain profiles of wind speed, wind direction, air temperature, dew point and humidity, with a Chilled Mirror Hygrometer and an ultrasonic wind speed sensor located near the 2 m level for comparison purposes. Barometric pressure, visibility, and precipitation data are obtained from sensors at or near the base of the tower.

**Siting.** Atqasuk (METTWR2H): sensors mounted on a 10-m tower, with temperature and relative humidity probes at 2 m and 5 m, and a Chilled Mirror Hygrometer at 1 m for comparison purposes; pressure, visibility, and precipitation sensors located at or near the base of the tower. Barrow (METTWR4H): sensors mounted at 2 m, 10 m, 20 m, and 40 m on a 40-m tower, with a Chilled Mirror Hygrometer and ultrasonic wind speed sensor near the 2 m level for comparison purposes; pressure, visibility, and precipitation sensors located at the base of the tower.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| wind speed | - | - | - | - | (hb p. 4) |
| wind direction | - | - | - | - | (hb p. 4) |
| air temperature | - | - | - | - | (hb p. 4) |
| dew point | - | - | - | - | (hb p. 4) |
| humidity | - | - | - | - | (hb p. 4) |
| barometric pressure | - | - | - | - | (hb p. 4) |
| visibility | - | - | - | - | (hb p. 4) |
| precipitation | - | - | - | - | (hb p. 4) |


## The data

Verified example: **`nsapwsC2.b1`**, file `nsapwsC2.b1.20031022.000000.cdf`
(0.18 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1439 |
| Data variables | 32 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2003-10-22T00:00:00 to 2003-10-22T23:59:00 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cumul_liq_water_equiv` | mm | time | yes | Cumulative Liquid Water Equivalent |
| `cumulative_snow` | mm | time | yes | Cumulative Snow |
| `one_hour_PW_code` | unitless | time | yes | One Hour PW code \(WMO SYNOP code\) |
| `one_minute_PW_code` | unitless | time | yes | One Minute PW code \(WMO SYNOP code\) |
| `one_minute_visibility` | m | time | yes | one Minute Visibility |
| `precip_rate` | mm/hr | time | yes | Precipitation Rate |
| `ten_minute_PW_code` | unitless | time | yes | Ten Minute PW code \(WMO SYNOP code\) |
| `ten_minute_visibility` | m | time | yes | Ten Minute Visibility |
| `cumul_liq_water_equiv_out_of_range_err` | unitless | time | - | Liquid Water Equivalent out of range error |
| `cumul_snow_out_of_range_error` | unitless | time | - | Cumulative Snow out of range error |
| `one_hour_pw_code_out_of_range_error` | unitless | time | - | One Hour PW code out of range error |
| `one_min_pw_code_out_of_range_error` | unitless | time | - | One Minute PW code out of range error |
| `one_minute_vis_out_of_range_error` | unitless | time | - | One Minute Visibility out of range error |
| `precip_rate_out_of_range_error` | unitless | time | - | PWS Precipitation Rate out of range error |
| `present_weather_sensor_NWS_code` | unitless | time | - | NWS code |
| `pws_read_timeout_error` | unitless | time | - | Present Weather Sensor Read Timeout Error |
| `pws_serial_error` | unitless | time | - | Present Weather Sensor Serial Error |
| `ten_min_pw_code_out_of_range_error` | unitless | time | - | Ten Minute PW code out of range error |
| `ten_minute_vis_out_of_range_error` | unitless | time | - | Ten Minute Visibility out of range error |
| `time` | - | time | - | Time offset from base_time |


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
                     params={"user": f"{user}:{token}", "ds": "nsapwsC2.b1",
                             "start": "2003-10-22", "end": "2003-10-22", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsapwsC2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsapwsC2.b1", "2003-10-22", "2003-10-22")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsapwsC2.b1", "2003-10-22", "2003-10-22"))   # cite what you pulled
```

## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
32 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_one_minute_visibility"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("one_minute_visibility", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["one_minute_visibility", "ten_minute_visibility", "one_minute_PW_code"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsapwsC2.b1.20031022.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `one_minute_visibility` | Difference between current and previous values exceeds... | 135 | 9.3815 |
| `ten_minute_visibility` | Difference between current and previous values exceeds... | 8 | 0.5559 |
| `cumulative_snow` | Difference between current and previous values exceeds... | 2 | 0.139 |
| `cumul_liq_water_equiv` | Difference between current and previous values exceeds... | 2 | 0.139 |
| `precip_rate` | Difference between current and previous values exceeds... | 2 | 0.139 |
| `precip_rate` | Value is equal to missing_value. | 1 | 0.0695 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsapwsC2.b1", "19980320", "20260923")
```

## Known artifacts and failure modes

The handbook documents no artifacts or failure modes explicitly. That is a gap in the
handbook, not evidence the instrument has none.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Chilled Mirror Hygrometer, ultrasonic wind speed sensor, Atqasuk Meteorology Station (AMET), Barrow Meteorology Station (BMET).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `METTWR2H` | Surface and Tower Meteorological Instrumentation at Atqasuk |
| `METTWR4H` | Surface and Tower Meteorological Instrumentation at Barrow |
| `AMET` | Atqasuk Meteorology Station |
| `BMET` | Barrow Meteorology Station |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mettwr_handbook.pdf (4 pages, by M.T. Ritsche)
- Catalog record: ARM data-source index, `instrument_class_code=mettwr`, read 2026-09-23
- Example file: `nsapwsC2.b1.20031022.000000.cdf` from `nsapwsC2.b1`, 0.18 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
