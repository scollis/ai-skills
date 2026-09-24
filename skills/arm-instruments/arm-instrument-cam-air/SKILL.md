---
name: arm-instrument-cam-air
description: ARM Video camera aboard aircraft (cam-air) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with cam-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations. Triggers - cam-air, Video camera aboard aircraft, coraafcammovieF1.a1, Airborne Observations, AXIS Communications AB, models P1344 and P1347 network cameras, ACE-ENA, CACTI, CAM-AIR.
---

# CAM-AIR - Video camera aboard aircraft

Forward-looking and nadir-looking AXIS network video cameras mounted aboard ARM's research aircraft capture images every minute during flight, combined into videos, to provide visual context (cloud field, in-cloud/clear air status, and surface type) for other onboard instrument measurements.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cam-air` |
| Handbook | [DOE/SC-ARM-TR-231 / A Matthews / October 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-231.pdf) |
| Measurement category | Airborne Observations |
| Manufacturer / model | AXIS Communications AB, models P1344 and P1347 network cameras |
| Primary measurements | Instrument monitoring non-geophysical variables |
| Record | 2018-11-04 to 2018-12-08 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | cor |
| ARM page | https://www.arm.gov/capabilities/instruments/cam-air |


## Credit

Everything this skill knows about the instrument is the work of **A Matthews** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Matthews. *Aircraft Video Camera (CAM-AIR) Instrument Handbook*, DOE/SC-ARM-TR-231, October 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-231.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrument consists of two commercial AXIS network video cameras installed on the aircraft: one (P1344 or P1347) mounted in the cockpit looking forward out the window, and one mounted in a custom hatch in the belly of the aircraft looking down (nadir). The cameras capture still images every minute during flight, which are combined into an MP4 video for each camera. The forward camera images indicate whether the plane is in cloud or clear air and give overall context of the cloud field, while the nadir camera images show the surface being flown over (land, water, or cloud) and can indicate vegetation cover, providing insight into factors affecting the onboard nadir radiometers. There is no calibration procedure or measurement theory described beyond straightforward optical image capture via the vendor's network camera hardware.

**Siting.** Forward camera is mounted on a small, custom stand near the center of the aircraft cockpit looking forward out the window. Nadir camera is mounted in a custom hatch on the belly of the aircraft, co-located with the nadir radiometers. All installations on the aircraft must be examined by an aircraft mechanic prior to flight. Prior to ACE-ENA (2017), P1344 flew forward and P1347 flew nadir; since only the forward camera was flown for ACE-ENA and CACTI (2018-2019), the higher-resolution P1347 was moved to the cockpit (forward) position.

**Sampling.** reported every 1 minute during flight (images taken every minute) (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Video/still images of clouds and terrain (forward and nadir... | - | - | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Camera models | AXIS P1344 (forward, pre-2017) and AXIS P1347 (nadir, pre-2017; forward, post-2017 due to higher resolution) | (hb p. 7) |
| Ethernet interface | RJ-45 ethernet cable to shuttle computer | (hb p. 8) |
| Power input | 2-pin terminal block for DC power input | (hb p. 8) |


## The data

**No example file was verified for this instrument.** the only datastream with data serves aircraft video averaging 8677 MB per file.

ARM's catalog lists 1 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
files = armlive_list_files("coraafcammovieF1.a1", start, end)
```

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("coraafcammovieF1.a1", "2018-12-08", "2018-12-08")
ds = armlive_open("coraafcammovieF1.a1", "2018-12-08", "2018-12-08", cleanup_qc=True)
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `act_qc_variables(ds)` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("coraafcammovieF1.a1", "20181104", "20260923")
```

The handbook's own note on data quality: Data quality is reported through ARM's Data Quality Reports, documenting missing or bad data. The download link also contains a read-me file that contains a table of data quality. There is no calibration database for this instrument, and data plots are not created for this instrument.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| No recording if record button not pressed | No data recorded for that flight; missing video file | Prior to flight, cameras must be accessed via AXIS Camera Management program and recording started | (hb p. 8) |
| Files must be exported after flight before download | Data not available for download until export step completed | Export files after flight has ended, prior to download | (hb p. 8) |
| Difficult access to nadir install location | Installation/configuration errors if IP address not verified beforehand | Ensure cameras running properly with assigned, working IP address before completing hardware installation | (hb p. 8) |
| Focus drift | Blurry images in video | Refocus by loosening focus puller, adjusting lens while checking live view, then tightening | (hb p. 9) |
| No data plots created for this instrument | Analyst cannot rely on standard ARM data plots to assess data quality visually via plotting tools | None stated | (hb p. 3) |
| No calibration database or procedures | No calibration reference values or drift corrections available for image data | None stated | (hb p. 3) |
| Missing or bad data | Gaps or errors noted in ARM Data Quality Reports and read-me file table of data quality | Consult ARM Data Quality Reports and read-me file accompanying download | (hb p. 3) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | None - there are no calibration procedures for the AXIS cameras (hb p. 9) |
| Routine maintenance | Little maintenance required; cameras may be refocused as needed by loosening the focus puller at the front of the camera, turning the lens while checking live view, then tightening the focus puller (hb p. 9) |
| Maintenance interval | As needed (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: nadir radiometers.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `CAM-AIR` | aircraft video camera |
| `DC` | direct current |
| `IP` | internet protocol |


### References the handbook cites

- AXIS Communications AB. 2012. "User Manual AXIS P1344 Network Camera." https://www.axis.com/files/manuals/um_p1344_48168_en_1208.pdf, accessed on October 11, 2019.
- AXIS Communications AB. 2012. "User Manual AXIS P1347 Network Camera." https://www.axis.com/files/manuals/um_p1347_45969r2_en_1212.pdf, accessed on October 11, 2019.
- AXIS Communications AB. 2010. "Installation Guide AXIS P13 Network Camera Series." https://www.axis.com/files/manuals/ig_p13Series_38731_en_1006.pdf, accessed on October 11, 2019.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-231.pdf (15 pages, DOE/SC-ARM-TR-231, by A Matthews)
- Catalog record: ARM data-source index, `instrument_class_code=cam-air`, read 2026-09-23
- Example file: none - the only datastream with data serves aircraft video averaging 8677 MB per file
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
