---
name: arm-instrument-wcm-air
description: ARM Water content meter aboard aircraft (wcm-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Total water content, Liquid water content, Liquid water content, Ice water content), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with wcm-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Cloud Properties. Triggers - wcm-air, Water content meter aboard aircraft, coraafwcmF1.a1, Total water content, Liquid water content, Ice water content, Airborne Observations, Cloud Properties, SEA Inc. (Science Engineering Associates, Inc.) Model WCM-2000, ACAPEX, ASCII, CAPS, CSIRO.
---

# WCM-AIR - Water content meter aboard aircraft

The WCM-2000 measures liquid water content, total water content, and ice water content (by difference) aboard research aircraft using heated sensing elements exposed to the airstream.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `wcm-air` |
| Handbook | [DOE/SC-ARM-TR-261 / A Matthews, L Goldberger / November 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-261.pdf) |
| Measurement category | Airborne Observations; Cloud Properties |
| Manufacturer / model | SEA Inc. (Science Engineering Associates, Inc.) Model WCM-2000 |
| Primary measurements | Liquid water content |
| Record | 2018-11-04 to 2018-11-04 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | cor |
| ARM page | https://www.arm.gov/capabilities/instruments/wcm-air |


## Credit

Everything this skill knows about the instrument is the work of **A Matthews, L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Matthews, L Goldberger. *Multi-Element Water Content System Instrument Handbook*, DOE/SC-ARM-TR-261, November 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-261.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The sensor head contains four heated stainless steel elements, each of different size or shape, used to measure solid and/or liquid water suspended in the atmosphere. Each element is heated by a low-voltage DC current maintaining a constant temperature (typically 140 deg C) via a digital closed-loop control system. The power required to maintain constant temperature for each element is directly related to the water content of the airstream and can be converted to grams per meter cubed using the dimensions of each element and the true airspeed of the airflow. A scoop element measures total water content (liquid plus ice); two wire elements of different diameters (0.5 mm and 2 mm) measure liquid water content; and a reference/comp element exposed to airflow but not to cloud water establishes the 'dry power term' subtracted from the other elements' power readings to obtain the measured water content. Ice water content is calculated by subtracting LWC from TWC.

**Siting.** The sensor head is installed on a strut on the fuselage of the aircraft, unimpeded in the free stream. The power box and control unit are installed inside the cabin.

**Sampling.** reported every 1 Hz (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Total water content (TWC) | g/m3 | 0-2 g/m3 typical, up to 10 g/m3 | - | - | (hb p. 9) |
| Liquid water content (LWC083, 0.5 mm diameter element) | g/m3 | 0-2 g/m3 typical, up to 10 g/m3 | - | - | (hb p. 8) |
| Liquid water content (LWC021, 2 mm diameter element) | g/m3 | 0-2 g/m3 typical, up to 10 g/m3 | - | - | (hb p. 8) |
| Ice water content (IWC, calculated) | g/m3 | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | g/m3 | (hb p. 9) |
| Range | 0−2 g/m3 typically, up to 10 g/m3 | (hb p. 9) |
| Reporting rate | 1 Hz | (hb p. 9) |
| Element temperature | typically 140°C | (hb p. 6) |
| Small LWC element diameter | 0.5 mm (same as classic JW/CT LWC sensor) | (hb p. 6) |
| Large LWC element diameter | 2 mm (same as CSIRO (King) LWC sensor) | (hb p. 6) |
| False response to IWC (LWC elements) | less than 1% | (hb p. 6) |
| False response to IWC (wire-wound LWC elements, for... | 10 to 20% | (hb p. 6) |


## The data

**No example file was verified for this instrument.** the datastream serves a tar containing a nested zip archive, not netCDF.

ARM's catalog lists 1 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "coraafwcmF1.a1", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
                     params={"user": f"{user}:{token}", "ds": "coraafwcmF1.a1",
                             "start": "2018-11-04", "end": "2018-11-04", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./coraafwcmF1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "coraafwcmF1.a1", "2018-11-04", "2018-11-04")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("coraafwcmF1.a1", "2018-11-04", "2018-11-04"))   # cite what you pulled
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("coraafwcmF1.a1", "20181104", "20260923")
```

The handbook's own note on data quality: Under extremely cold and humid conditions the WCM can freeze up, resulting in an unreal spike in the data; auxiliary LWC measurements on the aircraft should be used to validate. Data are also unreliable during takeoff and landing.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Freeze-up under extremely cold and humid conditions | Unreal spike in the data | Use auxiliary LWC measurements taken on the aircraft to validate | (hb p. 10) |
| Unreliable data during takeoff and landing | Data during these flight phases should not be trusted | Use auxiliary LWC measurements taken on the aircraft to validate | (hb p. 10) |
| False response to ice water content on LWC elements | Small (less than 1%) apparent LWC signal contamination when IWC is present in airstream | Design uses small-diameter wire elements (0.5 mm and 2 mm) which have less false response than wire-wound elements; compare to wire-wound elements... | (hb p. 6) |
| Insect contamination on wires and scoop | Anomalous power readings/water content values from obstructed elements | Clean wires and scoop prior to each flight with a dry Q-tip | (hb p. 13) |
| Zero-offset bias | Baseline offset in water content readings in clear air | Each flight is corrected for zero-offset bias using clear-air measurements | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated according to manufacturer's instructions, involving a dedicated test flight in cloud-free air; in flight, in clear air, fly three different altitudes at three different speeds to calibrate. Each flight is also corrected for zero-offset bias using clear-air measurements. (hb p. 12) |
| Routine maintenance | Wires and scoop should be cleaned prior to each flight with a dry Q-tip to remove any insects that may have become stuck to the wires. (hb p. 13) |
| Maintenance interval | prior to each flight (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: particle volume monitor (PVM-100a), cloud aerosol and precipitation spectrometer (CAPS) hotwire.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ACAPEX` | ARM Cloud Aerosol Precipitation Experiment |
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `CAPS` | cloud aerosol and precipitation spectrometer |
| `CSIRO` | Commonwealth Science and Industrial Research Organisation (Australia) |
| `DAQ` | data acquisition system |
| `DC` | direct current |
| `HI-SCALE` | Holistic Interactions of Shallow Clouds, Aerosols, and Land-Ecosystems |
| `IWC` | ice water content |
| `LWC` | liquid water content |
| `netCDF` | Network Common Data Format |
| `PVM` | particle volume monitor |
| `SEA` | Science Engineering Associates, Inc. |


### References the handbook cites

- Vendor website: Science Engineering Associates, Inc. http://www.scieng.com/products/multi.htm

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-261.pdf (14 pages, DOE/SC-ARM-TR-261, by A Matthews, L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=wcm-air`, read 2026-09-23
- Example file: none - the datastream serves a tar containing a nested zip archive, not netCDF
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
