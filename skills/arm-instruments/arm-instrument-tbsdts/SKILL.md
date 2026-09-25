---
name: arm-instrument-tbsdts
description: ARM Distributed Temperature Sensing aboard Tethered Balloon System (tbsdts) - handbook-derived instrument reference. Measurement principle, reported quantities (Sampling Resolution, Sampling Resolution, Temperature Resolution, Temperature Resolution), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbsdtsch1C1.b1) and the variable inventory of a real file. Use when working with tbsdts data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Profiling; Surface Meteorology; Surface/Subsurface Properties. Triggers - tbsdts, sgptbsdtsch1C1.b1, Sampling Resolution, Temperature Resolution, Airborne Observations, Atmospheric Profiling, Surface Meteorology, Surface/Subsurface Properties.
---

# TBSDTS - Distributed Temperature Sensing aboard Tethered Balloon System

The DTS payload uses a fiber-optic cable deployed on the TBS tether beneath a helium-filled tethered balloon to measure distributed air temperature along the fiber via Raman scattering, with the laser interrogator ground-based and the fiber itself acting as the sensor.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbsdts` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling; Surface Meteorology; Surface/Subsurface Properties |
| Manufacturer / model | Silixa XT Distributed Temperature Sensing (DTS) and Sensornet Oryx+ DTS-XR |
| Primary measurements | Atmospheric temperature |
| Record | 2019-04-25 to 2026-09-24 (active) |
| Datastreams with data | 8 across 4 sites |
| Sites | bnf, crg, hou, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbsdts |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbsdts`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsground`, `tbsins`, `tbslws`, `tbsmet`, `tbspops`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbsdts` until checked against that document's own section for it.

## How it measures

A Sensornet Oryx+ DTS-XR and Silixa XT DTS collect air temperature measurements based on Raman scattering distributed temperature sensing. The TBS DTS system measures atmospheric temperature using only the properties of a fiber optic cable, with the fiber serving as the thermometer and the laser interrogator housed in the ground-based DTS system serving as the illumination source. One fiber is generally deployed from the DTS in the Ch1 position and is spliced into a fiber optic rotary joint on a shaft connected to a motorized fiber optic reel; the reel motor spools and unspools the fiber at a matching rate to the balloon tether, and light is transmitted from the rotating fiber reel through the fiber optic rotary joint to the stationary DTS. A second fiber may be deployed from the DTS in the Ch2 position when the balloon is stationary aloft; the Ch2 fiber does not operate through a fiber optic rotary joint. Two PT100 temperature probes and 15-m-long fiber coils are deployed into calibration baths (one circulating ice water bath, one heated bath) at the surface during operation to represent the minimum and maximum temperatures expected during airborne DTS measurements, and an iMet 4-RSB radiosonde deployed at the end of the fiber immediately below the balloon is used as an end-point calibration reference for the DTS fiber measurements.

**Siting.** TBS-platform-level: One fiber is generally deployed from the DTS in the Ch1 position, spliced into a fiber optic rotary joint on a shaft connected to a motorized fiber optic reel that spools and unspools the fiber at a matching rate to the balloon tether as the balloon ascends/descends. An iMet 4-RSB radiosonde is typically deployed at the end of the fiber immediately below the balloon as an end-point calibration reference. A second fiber may be deployed in the Ch2 position (without a rotary joint) only when the balloon is stationary aloft. Two calibration baths (ice water and heated) with 15-m fiber coils and PT100 probes are maintained at the surface during DTS operation.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sampling Resolution (Silixa XT DTS) | cm | 0 - 5 km | +/- 0.4 °C (temperature accuracy) | 25 cm | (hb p. 15) |
| Sampling Resolution (Sensornet Oryx+ DTS-XR) | cm | 0 - 12 km | +/- 0.6 °C (temperature accuracy) | 100 cm | (hb p. 15) |
| Temperature Resolution (Silixa XT DTS) | °C | 0 - 5 km | +/- 0.4 | 0.09 | (hb p. 15) |
| Temperature Resolution (Sensornet Oryx+ DTS-XR) | °C | 0 - 12 km | +/- 0.6 | 0.12 | (hb p. 15) |


## Specifications

| parameter | value | source |
|---|---|---|
| Silixa XT DTS - Sampling Resolution | 25 cm | (hb p. 15) |
| Silixa XT DTS - Temperature Resolution | 0.09 °C | (hb p. 15) |
| Silixa XT DTS - Temperature Accuracy | +/- 0.4 °C | (hb p. 15) |
| Silixa XT DTS - Range | 0 - 5 km | (hb p. 15) |
| Silixa XT DTS - Measurement Time | 30 s | (hb p. 15) |
| Sensornet Oryx+ DTS-XR - Sampling Resolution | 100 cm | (hb p. 15) |
| Sensornet Oryx+ DTS-XR - Temperature Resolution | 0.12 °C | (hb p. 15) |
| Sensornet Oryx+ DTS-XR - Temperature Accuracy | +/- 0.6 °C | (hb p. 15) |
| Sensornet Oryx+ DTS-XR - Range | 0 - 12 km | (hb p. 15) |
| Sensornet Oryx+ DTS-XR - Measurement Time | 30 s | (hb p. 15) |
| Calibration bath fiber coil length | 15 m | (hb p. 15) |
| Calibration probe type | Two PT100 temperature probes | (hb p. 15) |


## The data

Verified example: **`sgptbsdtsch1C1.b1`**, file `sgptbsdtsch1C1.b1.20241111.170319.nc`
(23.48 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=334, `max_length`=5857 |
| Data variables | 9 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2024-11-11T17:03:19 to 2024-11-11T19:54:50 |
| dod version | tbsdtsch1-b1-1.0 |
| process version | ingest-tbsdtsme-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `temperature` | degC | time,max_length | yes | Temperature |
| `height` | m | time,max_length | - | Height above ground level |
| `profile_length` | 1 | time | - | Number of values in height/temperature profile |
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
                     params={"user": f"{user}:{token}", "ds": "sgptbsdtsch1C1.b1",
                             "start": "2024-11-11", "end": "2024-11-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptbsdtsch1C1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptbsdtsch1C1.b1", "2024-11-11", "2024-11-11")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgptbsdtsch1C1.b1", "2024-11-11", "2024-11-11"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("profile_length")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
9 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_temperature"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("temperature", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["temperature"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgptbsdtsch1C1.b1.20241111.170319.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `temperature` | Value is equal to missing_value. | 1091730 | 55.8076 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgptbsdtsch1C1.b1", "20190425", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Each datastream includes quality control variables for each scientific variable, per the handbook's general Data section statement.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Different spatial sampling resolution between the two DTS units | Silixa XT DTS reports at 25 cm sampling resolution while Sensornet Oryx+ DTS-XR reports at 100 cm sampling resolution over its longer range; comparing data from the two units directly will... | - | (hb p. 15) |
| Range/resolution tradeoff between the two DTS units | Silixa XT DTS covers only 0-5 km range with finer temperature resolution (0.09 °C) and accuracy (+/- 0.4 °C), while Sensornet Oryx+ DTS-XR covers 0-12 km with coarser resolution (0.12 °C)... | - | (hb p. 15) |
| Ch2 fiber restricted to stationary balloon operation | Data from the Ch2 fiber position will only be present during periods when the balloon is stationary aloft, since the Ch2 fiber does not operate through the fiber optic rotary joint and... | Deploy Ch2 fiber only when balloon is stationary aloft | (hb p. 15) |
| Fiber spooling rate must match tether rate | Any mismatch between the fiber optic reel motor spooling rate and the balloon tether rate would introduce spatial/altitude registration errors between reported fiber distance and true... | Reel motor spools and unspools the fiber at a matching rate to the balloon tether | (hb p. 15) |
| 30 s measurement time (temporal averaging) for both DTS units | Reported DTS temperature profiles represent a 30 s integration, so higher-frequency temperature fluctuations along the fiber are smoothed out | - | (hb p. 15) |
| Calibration bath end points bound expected temperature range | Ice water bath and heated bath represent the minimum and maximum temperatures expected during airborne DTS measurements; temperatures outside this bracketed range during flight may fall... | Use two calibration baths (ice water, heated) with PT100 probes and 15-m fiber coils at the surface during each DTS operation | (hb p. 15) |
| Dependence on iMet radiosonde end-point reference | DTS temperature calibration accuracy near the balloon end of the fiber depends on the co-located iMet 4-RSB radiosonde reading; any iMet sensor error or radiosonde placement offset from the... | - | (hb p. 15) |
| Only 2-year vendor calibration interval for DTS units | Calibration coefficients for Silixa XT DTS and Sensornet Oryx DTS are updated only every two years by the vendor, so drift between calibration events would not be captured by campaign-level... | Every two years, Vendor calibration mode | (hb p. 29) |
| TBS platform-level altitude ceiling and cloud clearance constraints affect DTS profile... | DTS profiles collected during flight will not extend above 1.5 km agl maximum altitude, and in-cloud DTS/TBS flights are limited to Restricted Airspace, truncating available profile range... | TBS flights generally conducted 152 m below cloud base, in greater than =3 sm visibility, to max altitude 1.5 km agl; in-cloud flights within... | (hb p. 9) |
| Tether angle deviation from zenith with wind speed (platform-level) | As wind speed increases, tether angle deviates from zenith (up to 45° max), meaning the DTS fiber's along-fiber distance does not correspond 1:1 with vertical altitude, distorting height... | Tether angle not allowed to exceed 45° in flight | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Vendor calibration; in-field calibration baths (one circulating ice water bath held at constant temperature, one heated bath held at constant temperature) with PT100 temperature probes and 15-m fiber coils bracket the min/max expected airborne temperatures, and an iMet 4-RSB radiosonde at the fiber end (immediately... (hb p. 29) |
| Calibration interval | Every two years (Silixa XT DTS); Every two years (Sensornet Oryx DTS) (hb p. 29) |
| Traceability | Vendor (hb p. 29) |
| Routine maintenance | ARM TBS instrumentation calibrated per Table 15; Silixa XT DTS and Sensornet Oryx DTS calibration mode is Vendor. (hb p. 29) |
| Maintenance interval | Every two years (hb p. 29) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: iMet-4 RSB radiosonde, TBS ground station (Campbell Scientific EE181/CS100), tbsmerged Value-Added Product.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `DTS` | distributed temperature sensing |
| `TBS` | tethered balloon system |


### References the handbook cites

- Dexheimer, D, M Airey, E Roesler, CM Longbottom, K Nicoll, S Kneifel, F Mei, RG Harrison, G Marlton, and PD Williams. 2019. "Evaluation of ARM tethered-balloon system instrumentation for supercooled liquid water and...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbsdts`, read 2026-09-24
- Example file: `sgptbsdtsch1C1.b1.20241111.170319.nc` from `sgptbsdtsch1C1.b1`, 23.48 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
