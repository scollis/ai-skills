---
name: arm-instrument-org
description: ARM Optical Rain Gauge (org) - handbook-derived instrument reference. Measurement principle, reported quantities (rainfall intensity, maximum rainfall intensity, minimum rainfall intensity, org gauge carrier level), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgporgC1.b1) and the variable inventory of a real file. Use when working with org data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - org, Optical Rain Gauge, sgporgC1.b1, rainfall intensity, maximum rainfall intensity, minimum rainfall intensity, org gauge carrier level, Surface Meteorology, Optical Scientific Inc., ORG_815-DA, ascii, RMSE.
---

# ORG - Optical Rain Gauge

The Optical Rain Gauge (ORG) measures rainfall intensity by detecting optical scintillation caused by precipitating particles falling through a beam of partially coherent infrared light, and is deployed on a mounting pole in the field (e.g., at the ARM SGP Site) as part of ARM's surface meteorology rain gauge network.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 67 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `org` |
| Handbook | [DOE/SC-ARM-TR-153 / MJ Bartholomew / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/org_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Optical Scientific Inc., ORG_815-DA |
| Primary measurements | Precipitation |
| Record | 1998-03-20 to 2024-02-14 (retired) |
| Datastreams with data | 4 across 3 sites |
| Sites | epc, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/org |


## Credit

Everything this skill knows about the instrument is the work of **MJ Bartholomew** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MJ Bartholomew. *Optical Rain Gauge Instrument Handbook*, DOE/SC-ARM-TR-153, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/org_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The ORG measures rainfall by detecting the optical irregularities induced within the sample volume by precipitating particles falling through a beam of partially coherent infrared light. These irregularities are known as scintillation. By detecting the intensity of the scintillation, the actual rainfall rate can be measured. The instrument consists of a transmit head containing an infrared emitting diode and lens with heater, and a receive head containing a photodiode, lens and aperture, heater, and electronics, connected by a frame and a 15-meter-long power/signal cable. The Campbell Scientific data logger produces ASCII files with the results, and no further processing of the data is required.

**Siting.** Siting requirements for ORGs include a solid footing with at 10-foot-high mounting pole. Objects such as trees and buildings should be at least twice as far away from a site as their height. If snowfall can be expected at the site, the opening of the gauge should be above average snow level. Optical rain gauges should not be located near exhaust vents of buildings, runways, and roads.

**Sampling.** native rate one measurement per minute; reported every 1 min (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| rainfall intensity | mm/hour | 0.1 to 500 mm/hr | ±5% of observed intensity | - | (hb p. 8) |
| maximum rainfall intensity | mm/hour | - | - | - | (hb p. 8) |
| minimum rainfall intensity | mm/hour | - | - | - | (hb p. 8) |
| rainfall intensity standard deviation | mm/hour | - | - | - | (hb p. 8) |
| org gauge carrier level | volts | 2.5 V to 5 V (normal) | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Accuracy | ±5% of observed intensity over a range from 0.1 to 500 mm/hr | (hb p. 9) |
| org_car (carrier level) normal range | 2.5 V to 5 V | (hb p. 9) |
| Cable length | 15-meter-long power/signal cable | (hb p. 11) |
| Manufacturer/Model | Optical Scientific Inc., model ORG_815-DA | (hb p. 12) |
| Mounting pole height | 10-foot-high mounting pole | (hb p. 12) |


## The data

Verified example: **`sgporgC1.b1`**, file `sgporgC1.b1.20160720.175000.cdf`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=40 |
| Data variables | 15 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2016-07-20T17:50:00 to 2016-07-20T18:29:00 |
| sampling interval | 60 seconds |
| averaging interval | None |
| dod version | org-b1-1.2 |
| process version | ingest-org-2.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `org_car` | V | time | yes | ORG IR Carrier Level |
| `precip_max` | mm/hr | time | yes | Precipitation maximum |
| `precip_mean` | mm/hr | time | yes | Precipitation mean |
| `precip_min` | mm/hr | time | yes | Precipitation minimum |
| `time` | - | time | yes | Time offset from midnight |
| `precip_sd` | mm/hr | time | - | Precipitation standard deviation |


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
                     params={"user": f"{user}:{token}", "ds": "sgporgC1.b1",
                             "start": "2016-07-20", "end": "2016-07-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgporgC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgporgC1.b1", "2016-07-20", "2016-07-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgporgC1.b1", "2016-07-20", "2016-07-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("precip_mean", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

5 `qc_` companion variables cover 4 of the
15 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_precip_mean"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("precip_mean", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["precip_mean", "precip_max", "precip_min"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgporgC1.b1", "19980320", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags include qc_time and qc_org (org carrier voltage, min 2.5 volts, max 5 volts). Missing data are assigned a missing_value of -999. The org_car variable is the one indicator of instrument health and should always be between 2.5 V and 5 V; other values indicate suspect data. Health and status are monitored via DQ HandS and NCVweb interactive plotting. Instrument mentor reviews occur once or twice a week, with QC delay of three days behind the current day, using DSview plots for operational status and DQ HandS diagnostic plots otherwise; outputs are Data Quality Problem Reports...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Poor performance at sub-freezing ambient temperatures | ORG performs poorly at ambient temperatures below zero degrees Centigrade (C); data collected under those conditions appears unreliable and should not be trusted | Data collected below 0°C should not be trusted; use other observations of precipitation intensity from the MET, RAIN, DISD, and VDIS datastreams... | (hb p. 9) |
| Abnormal org_car (carrier level) voltage | org_car variable value falls outside the normal 2.5 V to 5 V range | Any value outside 2.5 V to 5 V indicates suspect data; qc_org flag uses minimum 2.5 volts and maximum 5 volts to flag data. | (hb p. 9) |
| Missing data | A field for a sample time contains the value -999 | A "missing_value" value of -999 is assigned to that field when data are missing for a sample time. | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration is done at the manufacturer's facility. (hb p. 12) |
| Routine maintenance | Inspection of site grounds near the instrument for hazards; visual inspection of instrument components (conduits, wires, connections); check status of LED on CR1000 data logger; check clock values shown on LoggerNet screen; active maintenance and testing procedures. (hb p. 12) |
| Maintenance interval | Weekly (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MET, RAIN, DISD, VDIS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ascii` | American Standard Code for Information Interchange |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `C` | centigrade |
| `DOE` | U.S. Department of Energy |
| `mm` | millimeter |
| `ORG` | optical rain gauge |
| `QME` | Quality Measurement Experiment |
| `RMSE` | root-mean-square error |
| `SGP` | Southern Great Plains, an ARM megasite |
| `VAP` | value-added product |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/org_handbook.pdf (67 pages, DOE/SC-ARM-TR-153, by MJ Bartholomew)
- Catalog record: ARM data-source index, `instrument_class_code=org`, read 2026-09-23
- Example file: `sgporgC1.b1.20160720.175000.cdf` from `sgporgC1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
