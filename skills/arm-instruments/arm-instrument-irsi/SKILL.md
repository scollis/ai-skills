---
name: arm-instrument-irsi
description: ARM Infra-Red Sky Imager (irsi) - handbook-derived instrument reference. Measurement principle, reported quantities (sky_cover_high_emission_narrow, sky_cover_low_emission_narrow, sky_cover_high_emission_wide, sky_cover_low_emission_wide, sky_cover_opaque_narrow, sky_cover_thin_narrow, sky_cover_opaque_wide, sky_cover_thin_wide), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpirsivisC1.b1) and the variable inventory of a real file. Use when working with irsi data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties; Radiometric. Triggers - irsi, Infra-Red Sky Imager, sgpirsivisC1.b1, sky_cover_high_emission_narrow, sky_cover_low_emission_narrow, sky_cover_high_emission_wide, sky_cover_low_emission_wide, sky_cover_opaque_narrow, sky_cover_thin_narrow.
---

# IRSI - Infra-Red Sky Imager

The Infrared Sky Imager is an automatic, continuously operating hemispheric camera system deployed at ARM sites that captures radiometrically calibrated mid-infrared and visible sky images to derive time series of fractional sky cover day and night.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `irsi` |
| Handbook | [DOE/SC-ARM-TR-182 / VR Morris / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/irsi_handbook.pdf) |
| Measurement category | Cloud Properties; Radiometric |
| Manufacturer / model | Solmirus Corporation, All Sky Infrared Visible Analyzer |
| Primary measurements | Cloud fraction; Precipitable water |
| Record | 2014-05-20 to 2025-09-15 (retired) |
| Datastreams with data | 9 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/irsi |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Infrared Sky Imager Instrument Handbook*, DOE/SC-ARM-TR-182, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/irsi_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The IRSI's primary function is to provide radiometrically calibrated imagery in the mid-infrared atmospheric window from 8-14 µm, using an uncooled microbolometer array with a 10.2-micron filter that optimizes cloud/clear-sky contrast for fractional sky cover determination and an 8.1-micron filter used in conjunction with it to provide color temperature information and precipitable water vapor (PWV). The instrument response is the product of the filter transmission, lens transmission, and the nominal detector response, which is used in image analysis and calibration procedures. A visible subsystem with a cooled CCD detector provides imagery in visible wavelengths for cloud retrievals during daylight hours. The software automatically identifies cloudy and clear regions at user-defined intervals and calculates fractional sky cover, providing a real-time display of sky conditions. Absolute radiance calibration is attained via a hatch-integrated blackbody reference with embedded temperature sensors and a heater, allowing automatic field calibration by heating to ~80ºC and observing cooling to determine instrument response as a function of blackbody radiance.

**Siting.** The instrument should be mounted on a level 24-inch x 24-inch platform using four 1/2-inch bolts positioned at corners on 22-inch centers. It is recommended that the enclosure access door be directed to the south (for Northern Hemisphere installations) so the external blackbody reference is situated to the north, though this is not critical since the IR and visible cameras can be rotated internally to accommodate any orientation. A more important criterion is to minimize any unwanted obstructions in the IRSI's 180-degree field of view.

**Sampling.** native rate Data acquisition sequence is 30 seconds in length; reported every user-defined intervals (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| sky_cover_high_emission_narrow | % | - | - | - | (hb p. 7) |
| sky_cover_low_emission_narrow | % | - | - | - | (hb p. 7) |
| sky_cover_high_emission_wide | % | - | - | - | (hb p. 7) |
| sky_cover_low_emission_wide | % | - | - | - | (hb p. 7) |
| sky_cover_opaque_narrow | % | - | - | - | (hb p. 7) |
| sky_cover_thin_narrow | % | - | - | - | (hb p. 7) |
| sky_cover_opaque_wide | % | - | - | - | (hb p. 7) |
| sky_cover_thin_wide | % | - | - | - | (hb p. 7) |
| precipitable_water_vapor | mm | - | - | - | (hb p. 7) |
| reference_bb_temperature (sensors 1-3) | C | - | - | - | (hb p. 8) |
| external_bb_temperature (sensors 1-3) | C | - | - | - | (hb p. 8) |
| enclosure_temperature | C | - | - | - | (hb p. 8) |
| camera_temperature | C | - | - | - | (hb p. 8) |
| blackbody_radiance | W/(m^2 sr) | - | - | - | (hb p. 8) |
| Radiometric imagery in mid-infrared atmospheric window | - | 8-14 µm wavelength range | ±0.2 W/m2-µm-sr for typical sky radiances | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Infrared Detector | Uncooled microbolometer, 644x512 array | (hb p. 10) |
| IR Wavelength range | 8-14 µm | (hb p. 10) |
| IR Filters | 10-12 µm (sky cover, brightness temperature) and 8-9 µm (color temperature and PWV) | (hb p. 10) |
| IR Image resolution | 640 x 512 pixel, 14-bit | (hb p. 10) |
| IR Field of view | 180º | (hb p. 10) |
| Visible Detector | Interline cooled CCD (color) with electronic and mechanical shutter | (hb p. 10) |
| Visible Filters | Neutral density x10-2 and x10-4 | (hb p. 10) |
| Visible Image resolution | 3296 x 2472 pixel, 16-bit per color | (hb p. 10) |
| Visible Field of view | 180º | (hb p. 10) |
| Range | Hemispheric field of view, centered on zenith | (hb p. 10) |
| Accuracy | ±0.2 W/m2-µm-sr for typical sky radiances | (hb p. 11) |
| Repeatability |  | (hb p. 11) |
| Sensitivity | ±1.4ºC for temperatures near 25ºC; pixel-to-pixel sensitivity of less than 0.01 W/m2-sr-µm | (hb p. 11) |
| Uncertainty |  | (hb p. 11) |
| Input Voltage | 115 VAC, ±10% | (hb p. 11) |
| Input Current | 500 W maximum, with heating | (hb p. 11) |
| Lens | 180-degree (all sky), custom-designed, hard-carbon-coated, waterproof lens | (hb p. 10) |
| Filter wheel | eight-position filter wheel for use with 1-inch filters | (hb p. 10) |


## The data

Verified example: **`sgpirsivisC1.b1`**, file `sgpirsivisC1.b1.20230926.000104.nc`
(0.05 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=444 |
| Data variables | 24 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 68 s |
| File time span | 2023-09-26T00:01:04 to 2023-09-26T23:59:21 |
| dod version | irsivis-b1-3.0 |
| process version | ingest-irsi-3.1-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_sun` | degree | time | yes | Calculated altitude for the sun |
| `azimuth_sun` | degree | time | yes | Calculated azimuth for the sun |
| `camera_temperature` | degC | time | yes | Camera temperature |
| `sky_cover_opaque_narrow` | % | time | yes | Opaque sky cover for narrow field of view |
| `sky_cover_opaque_wide` | % | time | yes | Opaque sky cover for wide field of view |
| `sky_cover_thin_narrow` | % | time | yes | Thin sky cover narrow field of view |
| `sky_cover_thin_wide` | % | time | yes | Thin sky cover for wide field of view |
| `sky_cover_total_narrow` | % | time | yes | Total sky cover for narrow field of view |
| `sky_cover_total_wide` | % | time | yes | Total sky cover for wide field of view |
| `exposure_duration` | us | time | - | Exposure duration |
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
                     params={"user": f"{user}:{token}", "ds": "sgpirsivisC1.b1",
                             "start": "2023-09-26", "end": "2023-09-26", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpirsivisC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpirsivisC1.b1", "2023-09-26", "2023-09-26")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpirsivisC1.b1", "2023-09-26", "2023-09-26"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("camera_temperature", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
24 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_camera_temperature"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("camera_temperature", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["camera_temperature", "sky_cover_opaque_narrow", "sky_cover_thin_narrow"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpirsivisC1.b1.20230926.000104.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `camera_temperature` | Value is greater than fail_max. | 323 | 72.7477 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpirsivisC1.b1", "20140520", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Most fields contain a corresponding, sample-by-sample, automated quality check field in the b1 level datastreams, named qc_less than fieldnamegreater than  (e.g., qc_sky_cover_thin_wide for sky_cover_thin_wide). Flag values range from 0 (all QC checks passed) through combinations of missing-data, minimum-value, maximum-value, and delta checks (values 1-15, with 5, 6, 7 noted as "highly unlikely" in some cases). Minimum and maximum thresholds are defined per field (e.g., sky cover fields 0-100%, blackbody temperatures -20 to 50 C, enclosure/camera temperature 0-40 C).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Hatch gearbox backlash | Hatch motion through an angle of ~10º before movement begins; noticeable play when moving hatch by hand | Inspect periodically to ensure hatch moves freely with little resistance within this extent | (hb p. 15) |
| Repeatability unknown | No documented repeatability metric to assess measurement-to-measurement consistency | - | (hb p. 11) |
| Uncertainty unknown | No documented overall uncertainty value provided for measurements | - | (hb p. 11) |
| Lens/dome contamination | Degraded image quality or radiometric accuracy from dirt or residue on infrared lens or visible glass dome | Periodically clean with a lens-cleaning solution and a micro-fiber cloth | (hb p. 15) |
| Sample outside minimum/maximum QC thresholds | qc_less than fieldnamegreater than  flag values of 2, 4, 5, 7, 10-15 indicating sample below/above prescribed min/max or failing delta checks | - | (hb p. 9) |
| Delta check failure | qc_less than fieldnamegreater than  flag value 8 (or combined values 9-15) indicating change between sample and previous sample exceeds a prescribed value | - | (hb p. 9) |
| Missing data | qc_less than fieldnamegreater than  flag value 1 (or combined values 3,7,9,11,15) indicating sample contained a 'missing data' value | - | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Absolute radiance calibration is attained using Solmirus' hatch design incorporating a blackbody reference with embedded temperature sensors and a heater. The blackbody reference is heated to ~80ºC and then allowed to cool to near ambient temperature while acquiring image data in each of the IR filters, determining... (hb p. 14) |
| Calibration interval | Calibration procedure takes about an hour (hb p. 14) |
| Routine maintenance | The infrared lens and visible glass dome should be periodically cleaned with a lens-cleaning solution and a micro-fiber cloth. The hatch subsystem requires no maintenance but should be inspected periodically to ensure it is moving freely by moving the hatch up and down by hand while in the open position. (hb p. 15) |
| Maintenance interval | periodically (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### References the handbook cites

- Klebe D, RD Blatherwick, and VR Morris. 2014. "Ground-based all-sky mid-infrared and visible imagery for purposes of characterizing cloud properties." Atmospheric Measurement Techniques 7:637-645,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/irsi_handbook.pdf (16 pages, DOE/SC-ARM-TR-182, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=irsi`, read 2026-09-23
- Example file: `sgpirsivisC1.b1.20230926.000104.nc` from `sgpirsivisC1.b1`, 0.05 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
