---
name: arm-instrument-wb
description: ARM Weighing Bucket Precipitation Gauge (wb) - handbook-derived instrument reference. Measurement principle, reported quantities (Intensity, Accumulated precipitation NRT), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpwbpluvio2C1.a1) and the variable inventory of a real file. Use when working with wb data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - wb, Weighing Bucket Precipitation Gauge, sgpwbpluvio2C1.a1, Intensity, Accumulated precipitation NRT, Surface Meteorology, Ott Hydromet GmbH, Pluvio2-L weighing bucket rain gauge, intensity, rain_rate, accum_rtnrt, maintenance_flag.
---

# WB - Weighing Bucket Precipitation Gauge

The Pluvio2-L weighing bucket rain gauge measures the weight of a collection bucket once a minute to determine liquid, solid, or mixed precipitation amount and intensity, deployed in the field mounted on a pipe/pedestal with a wind shield as part of ARM surface meteorology sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 30 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `wb` |
| Handbook | [DOE/SC-ARM-TR-232 / MJ Bartholomew / June 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-232.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Ott Hydromet GmbH, Pluvio2-L weighing bucket rain gauge |
| Primary measurements | Precipitation |
| Record | 2016-11-22 to 2026-09-22 (active) |
| Datastreams with data | 15 across 15 sites |
| Sites | anx, asi, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mos, nsa, oli |
| ARM page | https://www.arm.gov/capabilities/instruments/wb |


## Credit

Everything this skill knows about the instrument is the work of **MJ Bartholomew** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MJ Bartholomew. *Weighing Bucket Rain Gauge Instrument Handbook*, DOE/SC-ARM-TR-232, June 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-232.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrument works using the balance principle: the heavier the collecting bucket, the more precipitation has occurred. A high-precision stainless-steel load cell, hermetically sealed against environmental influences, measures the weight of the collecting bucket once a minute, and the difference between successive measurements determines the rainfall amount over the sampling interval. An integrated temperature sensor compensates for temperature changes in the weighing mechanism. The orifice of the gauge is heated so that when snow/ice precipitation occurs, the weight of its water equivalent is the amount observed. Two liters of mineral oil are kept in the bucket at all times to prevent evaporation from influencing the bucket contents.

**Siting.** Typically a 4-inch round pipe is mounted vertically in a concrete pad to support the gauge, with the base directly bolted to the pipe; ARM Mobile Operations staff try to avoid concrete pads and use a custom stand instead. The concrete pads/custom stand also provide a base for the wind shield that accompanies each instrument. Cables between major components must be protected from weather and animals. The World Meteorological Organization recommends a double-fence wind shield (or other shielding method) because wind can have a large impact on snow collection; ARM's Pluvio2 gauges during MOSAiC and COMBLE had a double-fence wind-type shield but the fencing was not as tall as WMO-recommended,...

**Sampling.** native rate 1 minute (weight of collection bucket measured once a minute); reported every 1 minute (sampling_interval = '1 minute'); averaging accum_nrt uses a sampling interval at most 1 hour long ending at the given time; ptemp and volt_min use time bounds [-60,0] (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Intensity (heavy precipitation alarm), intensity_rt | mm/hr | 0 to 3000 | plus/minus 6 | - | (hb p. 3) |
| Accumulated amount RT/NRT, accum_rtnrt | mm | 0 to 500 | plus/minus 0.1 | threshold 0.05 mm | (hb p. 4) |
| Accumulated precipitation NRT (delayed 5 min), accum_nrt | mm | 0 to 500 | plus/minus 0.1 | threshold 0.05 mm | (hb p. 4) |
| Sum of accum_nrt since last device start, accum_total_nrt | mm | 0 to 500 | plus/minus 0.1 | threshold 0.05 mm | (hb p. 4) |
| Bucket contents, unfiltered since last reset, bucket_rt | mm | 20 to 1800 | plus/minus 0.1 | threshold 0.01 mm | (hb p. 5) |
| Bucket contents, filtered since last reset, bucket_nrt | mm | 20 to 1800 | plus/minus 0.1 | threshold 0.01 mm | (hb p. 5) |
| Load cell temperature, load_cell_temp | degC | -50 to 70 | plus/minus 1 | - | (hb p. 5) |
| Electronics unit temperature, elec_unit_temp | degC | -50 to 70 | plus/minus 1 | - | (hb p. 6) |
| Supply voltage, supply_volts | V | 4.5 to 28 | plus/minus 0.5 | - | (hb p. 6) |
| Orifice rim temperature, orifice_temp | degC | -50 to 70 | - | - | (hb p. 7) |
| Rain intensity based upon accum_rtnrt, intensity_rtnrt | mm/hr | 0 to 30000 | plus/minus 6 | threshold 0.3 mm/hr | (hb p. 7) |
| Minimum supply voltage of logger, volt_min | V | 0 to 20 | - | - | (hb p. 7) |
| Panel temperature average, ptemp | degC | -50 to 70 | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Recordable precipitation | Liquid, solid, and mixed | (hb p. 15) |
| Collecting area | 400 cm² | (hb p. 15) |
| Recordable precipitation amount | 750 mm | (hb p. 15) |
| Measurement method | Weighing measurement method | (hb p. 15) |
| Sensor element | Sealed load cell | (hb p. 15) |
| Precipitation measuring range | 0 ... 50 mm/min or 0 ... 3000 mm/h | (hb p. 15) |
| Cumulative precipitation threshold at 60 min collection time | 0.05 mm/h | (hb p. 15) |
| Precipitation intensity threshold | 0.1 mm/min or 6 mm/h | (hb p. 15) |
| Accuracy (at -25 ... +45 °C) - Amount | ±0.1 mm or ±1 % of measured value | (hb p. 15) |
| Accuracy (at -25 ... +45 °C) - Intensity | ±0.1 mm/min, ±6 mm/h or ±1 % of measured value | (hb p. 15) |
| Resolution - SDI-12- and RS-485 interface | 0.01 mm, 0.01 mm/min or mm/h | (hb p. 15) |
| Resolution - Impulse output | 0.05/0.1/0.2 mm | (hb p. 15) |
| Intensity output interval | 1 minute | (hb p. 15) |
| Query interval | 1 minute ... 60 minutes | (hb p. 15) |
| Output delay - Real-time (RT) | less than  1 minute | (hb p. 16) |
| Output delay - Non-real-time (NRT) | 5 minutes | (hb p. 16) |
| Measurement output | Intensity RT, amount RT/NRT, amount NRT, amount total NRT, bucket content RT and NRT, temperature load cell | (hb p. 16) |
| Status output | OTT Pluvio2-L Status, Heating status (if present) | (hb p. 16) |
| Digital interfaces | SDI-12 V1.3, RS-485 2- or 4-wire (SDI-12 protocol and ASCII) | (hb p. 16) |
| Digital outputs (2/5 Hz) | Impulse: 0.05/0.1/0.2 mm (adjustable) | (hb p. 16) |
| Digital outputs Status | 0 ... 120 impulses/min | (hb p. 16) |
| USB | USB 2.0 (for service mode) | (hb p. 16) |
| Power supply | 5.5 ... 28V DC, typically 12V DC | (hb p. 16) |
| Current consumption | typ. 9.2 mA at 12V (without heating) | (hb p. 16) |
| Power consumption | ≤ 110 mW (without heating) | (hb p. 16) |
| Ring heating power supply | 12 ... 28V DC, typ. 12/24V DC | (hb p. 16) |


_17 further specification rows are in the handbook._

## The data

Verified example: **`sgpwbpluvio2C1.a1`**, file `sgpwbpluvio2C1.a1.20260919.000000.nc`
(0.13 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 22 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| sampling interval | 1 minute |
| dod version | wbpluvio2-a1-1.0 |
| process version | ingest-wbpluvio2-1.1-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `accum_nrt` | mm | time | - | Accumulated precipitation over the sampling interval filtered and... |
| `accum_rtnrt` | mm | time | - | Accumulated amounts of precipitation over the sampling interval... |
| `accum_total_nrt` | mm | time | - | Sum of accum_nrt values since the last device start |
| `bucket_nrt` | mm | time | - | The currently measured, filtered bucket contents since last reset |
| `bucket_rt` | mm | time | - | The currently measured, unfiltered bucket contents since last reset |
| `elec_unit_temp` | degC | time | - | Temperature of electronics unit |
| `heater_status` | unitless | time | - | Heater status |
| `intensity_rt` | mm/hr | time | - | Heavy precipitation alarm |
| `intensity_rtnrt` | mm/hr | time | - | Rain intensity based upon accum_rtnrt |
| `load_cell_temp` | degC | time | - | Temperature of load cell |
| `maintenance_flag` | count | time | - | Bucket is being emptied or serviced |
| `orifice_temp` | degC | time | - | Temperature of orifice rim |
| `pluvio_status` | unitless | time | - | Pluvio status |
| `ptemp` | degC | time | - | Panel temperature average |
| `reset_flag` | count | time | - | Bucket emptied |
| `supply_volts` | V | time | - | Supply voltage |
| `time` | - | time | - | Time offset from midnight |
| `volt_min` | V | time | - | Minimum supply voltage of logger |


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
                     params={"user": f"{user}:{token}", "ds": "sgpwbpluvio2C1.a1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpwbpluvio2C1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpwbpluvio2C1.a1", "2026-09-19", "2026-09-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpwbpluvio2C1.a1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `maintenance_flag`, `reset_flag`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpwbpluvio2C1.a1", "20161122", "20260923")
```

The handbook's own note on data quality: The instrument mentor and the ARM Data Quality Office work together to develop automated means to review the data, backed up by weekly inspections. Ancillary variables such as pluvio_status, maintenance_flag, and reset_flag should be used to interpret/flag questionable accum and bucket values (e.g., ignore bucket/accum values when maintenance_flag or reset_flag is not 0). Data are quality-controlled using valid_min/valid_max ranges and missing_value = -9999 flags per variable.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Negative rain amounts/rates during extreme cold (no suitable oil for antifreeze/oil film) | Negative rain amounts and negative rain rates appear in the data during periods of frozen precipitation in extreme cold conditions (e.g., COMBLE, MOSAiC campaigns) | These should be interpreted as periods without rain or snow. | (hb p. 2) |
| Wind effects on snow/precipitation collection | Undercatch or anomalous precipitation amounts especially during snow, since wind can have a large impact on snow collection | WMO recommends double-fence wind shield or other shielding; ARM's shield for MOSAiC/COMBLE was not as tall as WMO recommendation and wind corrections... | (hb p. 2) |
| intensity_rt variable has a high lower threshold and is not a true rain-rate variable | intensity (intensity_rt) reports 0 mm/hr for any rainfall below 6 mm/hr threshold; only heavy rainfall events register non-zero values | ARM ingest calculates additional rain_rate variable with lower 3 mm/hour threshold, derived from accum_rtnrt * 60. | (hb p. 3) |
| Non-real-time (NRT) data time stamp delay | NRT variables (accum_nrt, bucket_nrt, etc.) are delayed by 5 minutes from actual time of observation | Note that NRT data, while highest quality, has a time stamp 5 minutes delayed from actual observation time; account for this offset in time-series... | (hb p. 3) |
| Proprietary internal NRT correction processing | NRT values differ from RT values due to internal corrections for wind, temperature, and evaporation, but the exact algorithm is not disclosed | None stated (proprietary); user should be aware exact correction methodology is unknown. | (hb p. 3) |
| Below-threshold accumulation/intensity values reported as zero | accum_rtnrt, accum_nrt, accum_total_nrt report 0 mm when below 0.05 mm threshold; intensity_rt/intensity_rtnrt report 0 mm/hr when below their thresholds; bucket_rt/bucket_nrt report no... | None stated beyond noting the threshold behavior in variable comments. | (hb p. 3) |
| Maintenance/reset flag periods invalidate bucket and accumulation data | maintenance_flag or reset_flag nonzero coincides with bucket_rt/bucket_nrt/accum_* values that are not meaningful, occurring only when not raining | If maintenance_flag or reset_flag is not 0, any values for bucket or accum variables should be ignored. | (hb p. 6) |
| Heater status fault conditions | heater_status flag is nonzero (sum of bit values) indicating orifice rim overtemperature (greater than 40C), undertemperature (less than -20C), sensor disconnection/short circuit,... | 0 indicates heater operating properly; nonzero values indicate specific fault per flag_meanings bit descriptions. | (hb p. 5) |
| Pluvio (gauge) status fault conditions | pluvio_status flag nonzero (sum of bit values) indicating bucket fill greater than 80%, USB connected, restart due to power failure/firmware, weight change not permitted, low supply voltage... | 0 indicates gauge operating properly; nonzero values indicate specific fault per flag_meanings bit descriptions. | (hb p. 6) |
| Evaporation effects on bucket contents | Would appear as anomalous loss of bucket weight/content if oil film is absent or insufficient | Two liters of mineral oil are kept in the bucket at all times to prevent evaporation influence; oil should be checked/replenished during maintenance. | (hb p. 1) |
| Bucket overflow / capacity limit | Bucket contents (bucket_rt/bucket_nrt) approaching valid_max of 1800 mm or gauge capacity equivalent to 750 mm rainfall accumulation could saturate, requiring manual emptying (max 36 kg) | Operations staff must periodically empty the bucket manually. | (hb p. 21) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | The Pluvio2 arrives from the manufacturer fully calibrated. After initial setup, the system is tested for accuracy with calibrated weights (a light weight ~50 grams and a heavier weight ~300 grams of known accuracy) using Ott-provided 'Guided Accuracy Test' software running on Microsoft Windows. (hb p. 9) |
| Calibration interval | Yearly (once initial test is passed, no further calibration needed, but accuracy test done yearly) (hb p. 9) |
| Routine maintenance | Weekly: inspect site grounds near instrument for hazards; visually inspect conduit, cables, connectors for damage/water intrusion/tightness; check Port 8 LED on CR1000 logger flashes once per minute; check clock values on LoggerNet Connect screen; check oil floating on precipitation in bucket and remove leaves/debris;... (hb p. 13) |
| Maintenance interval | weekly (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Two-dimensional video disdrometer.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `RT` | real-time |
| `NRT` | non-real-time |
| `intensity` | rain rate variable name (Ott convention), with a lower threshold of 6 mm/hour, intended... |
| `rain_rate` | ARM-calculated rain rate variable with 3 mm/hour threshold, determined by accum_rtnrt... |
| `accum_rtnrt` | rainfall amount collected over the last sample interval (one minute), an example of Ott's... |
| `maintenance_flag` | flag indicating bucket is being emptied or serviced; if not 0, instrument is being... |
| `reset_flag` | flag indicating bucket emptied; if not 0, bucket is being emptied and it is not raining |
| `COMBLE` | Cold-Air Outbreaks in the Marine Boundary Layer Experiment |
| `MOSAiC` | Multidisciplinary Drifting Observatory for the Study of Arctic Climate |
| `WMO` | World Meteorological Organization |


### References the handbook cites

- Kochendorfer, J, R Rassmussen, M Wolff, B Baker, ME Hall, T Meyers, S Landolt, A Jahcik, K Isaksen, R Braekkam, and R Leeper. 2017. "The quantification and correction of wind-induced precipitation measurement errors."...
- Goodison, BE, PYT Louie, and D Yang. 1998. Instruments and Observing Methods: WMO Solid Precipitation Measurement Intercomparison Final Report. World Meteorological Organization. Report No. 67.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-232.pdf (30 pages, DOE/SC-ARM-TR-232, by MJ Bartholomew)
- Catalog record: ARM data-source index, `instrument_class_code=wb`, read 2026-09-23
- Example file: `sgpwbpluvio2C1.a1.20260919.000000.nc` from `sgpwbpluvio2C1.a1`, 0.13 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
