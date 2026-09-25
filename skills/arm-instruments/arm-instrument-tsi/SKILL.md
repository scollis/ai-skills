---
name: arm-instrument-tsi
description: ARM Total Sky Imager (tsi) - handbook-derived instrument reference. Measurement principle, reported quantities (Percent opaque cloud, Percentage thin cloud, Sunshine meter, Sun altitude above horizon, Solar azimuth angle, Relative strength of direct sun), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptsiskycoverC1.b1) and the variable inventory of a real file. Use when working with tsi data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - tsi, Total Sky Imager, sgptsiskycoverC1.b1, Percent opaque cloud, Percentage thin cloud, Sunshine meter, Sun altitude above horizon, Solar azimuth angle, Relative strength of direct sun, Cloud Properties, Yankee Environmental Systems (YES), Inc., JPEG, Sky cover.
---

# TSI - Total Sky Imager

The Total Sky Imager provides time series of hemispheric sky images during daylight hours and retrievals of fractional sky cover for periods when the solar elevation is greater than 10 degrees, deployed as an automatic outdoor sky-imaging system at ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `tsi` |
| Handbook | [ARM TR-017 / V. R. Morris / June 2005](https://www.arm.gov/publications/tech_reports/handbooks/tsi_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Yankee Environmental Systems (YES), Inc., Total Sky Imager Model TSI-660 |
| Primary measurements | Cloud fraction |
| Record | 2000-07-01 to 2025-08-21 (retired) |
| Datastreams with data | 142 across 27 sites |
| Sites | acx, anx, asi, awr, cor, ena, epc, fkb, gan, grw, guc, hfe, hou, mag |
| ARM page | https://www.arm.gov/capabilities/instruments/tsi |


## Credit

Everything this skill knows about the instrument is the work of **V. R. Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> V. R. Morris. *Total Sky Imager (TSI) Handbook*, ARM TR-017, June 2005.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tsi_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Images from the sky are captured via a solid-state charge-coupled device looking downward onto a heated, rotating hemispherical mirror. A solar-ephemeris guided shadowband on the mirror blocks the intense direct-normal light from the sun, protecting the imager optics. An image-processing program captures images via TCP/IP at a user-defined sampling rate (max one image every 30 sec) and saves them to JPEG files. The analysis software first masks out known obstructions (the camera, its arm, and the sun-blocking shadowband), then a processing algorithm examines the color relationships of the remaining image pixels to infer whether each pixel represents clear sky or thin or opaque cloud. The differential of brightness along the sun-blocking band is also analyzed to infer if the sun is blocked by cloud, functioning as a sunshine meter.

**Siting.** The TSI is a daytime imager; once the sun rises above a user-selectable minimum solar zenith angle, image acquisition begins. TSI retrievals of fractional sky cover are valid only for solar elevation angles of 10 degrees or greater.

**Sampling.** native rate max. of one image every 30 sec; reported every 30-sec sampling interval (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Percent opaque cloud | percent | 0-100 (threshold) | - | - | (hb p. 5) |
| Percentage thin cloud | percent | 0-100 (threshold) | - | - | (hb p. 5) |
| Sunshine meter (sunny) | - | 0-1 (threshold) | - | - | (hb p. 5) |
| Sun altitude above horizon (solar.altitude) | degrees | -90 to 90 (threshold) | - | - | (hb p. 5) |
| Solar azimuth angle (solar.azimuth) | degrees | 0-360 (threshold) | - | - | (hb p. 5) |
| Relative strength of direct sun (sun.strength) | - | -100 to 100 (threshold) | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Image Resolution | 352 x 288 color, 24-bit JPEG format | (hb p. 10) |
| Sampling rate | Variable, with max. of one image every 30 sec | (hb p. 10) |
| Operating Temperature | -40° C to +44° C | (hb p. 10) |
| Weight/Size | Approx.70 lbs.(32 kg); dims: 20.83”x18.78”; height is 34.19”; mounts on 16.75x12” 1/4-20 bolt square | (hb p. 10) |
| Power Requirements | 115/230 VAC; mirror heater duty cycle varies with air temperature: 560W with heater on / 60W off | (hb p. 10) |
| Software | Image application supports MS-Windows® | (hb p. 10) |
| Data Storage | Local workstation disk | (hb p. 10) |
| Communication | 10BaseT/RJ45 (15m) | (hb p. 10) |


## The data

Verified example: **`sgptsiskycoverC1.b1`**, file `sgptsiskycoverC1.b1.20250818.000000.cdf`
(0.35 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1599 |
| Data variables | 52 |
| QC variables | 24 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2025-08-18T00:00:00 to 2025-08-18T23:59:30 |
| sampling interval | 30 seconds |
| averaging interval | None |
| dod version | tsiskycover-b1-3.2 |
| process version | ingest-tsi-12.8-7.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `count_box` | pixels | time | yes | Pixel count: number in box, outside mirror area |
| `count_mask` | pixels | time | yes | Pixel count: number in camera and sun strip mask |
| `count_opaque` | pixels | time | yes | Pixel count: number total opaque |
| `count_sky` | pixels | time | yes | Pixel count: number total in processed circle |
| `count_sub_horz` | pixels | time | yes | Pixel count: number below horizon in image |
| `count_sub_proczen` | pixels | time | yes | Pixel count: number total between horizon and processed circle |
| `count_thin` | pixels | time | yes | Pixel count: number total thin |
| `count_unknown` | pixels | time | yes | Pixel count: number total indeterminate |
| `percent_opaque` | % | time | yes | Percent opaque cloud |
| `percent_thin` | % | time | yes | Percent thin cloud |
| `region_horizon_count` | pixels | time | yes | Pixel count: number total in horizon area |
| `region_horizon_count_opaque` | pixels | time | yes | Pixel count: number opaque in horizon area |
| `region_horizon_count_thin` | pixels | time | yes | Pixel count: number thin in horizon area |
| `region_sun_count` | pixels | time | yes | Pixel count: number total in sun circle |
| `region_sun_count_opaque` | pixels | time | yes | Pixel count: number opaque in sun circle |
| `region_sun_count_thin` | pixels | time | yes | Pixel count: number thin in sun circle |
| `region_zenith_count` | pixels | time | yes | Pixel count: number total in zenith circle |
| `region_zenith_count_opaque` | pixels | time | yes | Pixel count: number opaque in zenith circle |
| `region_zenith_count_thin` | pixels | time | yes | Pixel count: number thin in zenith circle |
| `solar_altitude` | degree | time | yes | Sun altitude above horizon |
| `solar_azimuth` | degree | time | yes | Solar azimuth angle |
| `sun_strength` | unitless | time | yes | Relative 'strength' of direct sun |
| `sunny` | unitless | time | yes | Sunshine meter |
| `time` | - | time | yes | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgptsiskycoverC1.b1",
                             "start": "2025-08-18", "end": "2025-08-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptsiskycoverC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptsiskycoverC1.b1", "2025-08-18", "2025-08-18")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgptsiskycoverC1.b1", "2025-08-18", "2025-08-18"))   # cite what you pulled
```

This datastream carries 52 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgptsiskycoverC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["count_box", "count_mask", "count_opaque", "qc_count_box", "qc_count_mask", "qc_count_opaque"],
                                cleanup_qc=True)
```

## Quality control in this datastream

24 `qc_` companion variables cover 23 of the
52 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_percent_opaque"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("percent_opaque", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["percent_opaque", "percent_thin", "sunny"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgptsiskycoverC1.b1.20250818.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sun_strength` | Value is equal to missing_value. | 1599 | 100.0 |
| `percent_opaque` | Value is less than the fail_min. | 62 | 3.8774 |
| `percent_thin` | Value is less than the fail_min. | 62 | 3.8774 |
| `sunny` | Value is equal to missing_value. | 62 | 3.8774 |
| `region_zenith_count_thin` | Value is equal to missing_value. | 62 | 3.8774 |
| `region_zenith_count_opaque` | Value is equal to missing_value. | 62 | 3.8774 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgptsiskycoverC1.b1", "20000701", "20260923")
```

The handbook's own note on data quality: Most fields have a corresponding, sample-by-sample automated quality-check field in the b1 level datastreams named qc_less than fieldnamegreater than  (e.g., qc_percent.opaque). Flag values 0-15 indicate combinations of passed checks, missing data, below-minimum, above-maximum, and delta (sample-to-sample change) check failures, per Table 4. Minimum/maximum thresholds for each field are defined in Table 5. Sky cover retrievals are also monitored via visual inspection comparing sky images to cloud decision images; non-optimal periods are reprocessed and updated files sent to the ARM Archive....

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Valid only for solar elevation greater than = 10 degrees | Fractional sky cover retrievals absent or invalid during low sun angle periods (early morning/late afternoon) | Retrievals reported only valid for solar elevation angles of 10 degrees or greater | (hb p. 4) |
| Nighttime blind period | No images or sky cover data outside daylight hours; imager only operates once sun rises above a user-selectable minimum solar zenith angle | None stated beyond daytime-only operation | (hb p. 6) |
| Obstruction masking (camera arm, sun-blocking shadowband, mirror mount) | Masked pixels appear as count.box, count.mask, and other non-sky pixel counts in the data rather than sky cover values | Analysis software masks out these known obstructions before processing | (hb p. 6) |
| Indeterminate/unknown pixels | count.unknown field shows pixels that could not be classified as clear, thin, or opaque | None stated | (hb p. 3) |
| Sky cover algorithm requires manual visual QC, cannot be fully automated | Periods with erroneous cloud decision images identified only by visual inspection comparison of sky images and cloud decision images | Instrument mentor spot-checks and reprocesses non-optimal periods; updated files sent to ARM Archive | (hb p. 5) |
| Mirror heater dependency on air temperature | Power draw varies (560W heater on / 60W off) with ambient temperature, could indicate heater cycling in cold conditions | None stated | (hb p. 7) |
| Operating temperature range limit | Instrument specified only for -40°C to +44°C; performance outside this range not characterized | None stated | (hb p. 7) |
| Data quality delta check failures | qc_less than fieldnamegreater than  flag values 8-15 indicate sample failed delta check (large change from previous sample) possibly combined with min/max/missing checks | Flagged via qc_less than fieldnamegreater than  companion fields with defined threshold table | (hb p. 3) |
| Missing data values | qc_less than fieldnamegreater than  flag value 1 (or combinations) indicates sample contained 'missing data' value | Flagged via qc_less than fieldnamegreater than  fields | (hb p. 3) |
| Comparison discrepancy with other sky cover estimates not yet resolved | Differences between TSI-retrieved total sky cover and Shortwave Flux Analysis VAP or whole sky imager (WSI) retrievals | Comparison planned/underway as part of SGP CF system evaluation (QME) | (hb p. 5) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Sky cover processing limits are set by the instrument mentor, based on experience and tailored to human observations. (hb p. 7) |
| Routine maintenance | SGP Preventative Maintenance Procedure; TWP Operating Procedure (hb p. 8) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Whole Sky Imager (WSI), Shortwave Flux Analysis Value-Added Product (VAP).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `TSI` | Total Sky Imager |
| `JPEG` | Joint Photographic Experts Group compressed digital image format |
| `PNG` | Portable Network Graphics digital image format |
| `TXT` | ASCII text format |
| `YES` | Yankee Environmental Systems |
| `Sky cover` | The amount of the hemispheric field-of-view of the sky from the viewpoint of an observer... |
| `QME` | Quality Measurement Experiment, a special class of VAP that adds value to input... |
| `VAP` | Value-Added Product, derived from analyzing and processing existing data products to meet... |


### References the handbook cites

- Kassianov, E, and C Long. 2003. "Paired Ground-Based Hemispherical Observations for Cloud Base Height Estimation." Thirteenth ARM Program Science Team Meeting.
- Kassianov, E, C Long, and J Christy. 2004. "ARM Cloudiness Intercomparison IOP 2003 Analysis: Cloud Base Height." Fourteenth ARM Science Team Meeting.
- Kassianov, E, CN Long, M Ovtchinnikov, and J Christy. 2004. "Cloud properties retrievals from surface hemispherical observations." International Radiation Symposium 2004 IRS.
- Kassianov, E, CN Long, and M Ovtchinnikov. 2005. "Cloud sky cover versus cloud fraction: whole-sky simulations and observations." Journal of Applied Meteorology 44: 86-98.
- Long, CN, and JJ DeLuisi. 1998. "Development of an Automated Hemispheric Sky Imager for Cloud Fraction Retrievals." Proceedings 10th Symposium on Meteorological Observations and Instrumentation.
- Long, CN, DW Slater, and T Tooman. 2001. Total Sky Imager Model 880 Status and Testing Results. ARM Technical Report ARM TR-006.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tsi_handbook.pdf (12 pages, ARM TR-017, by V. R. Morris)
- Catalog record: ARM data-source index, `instrument_class_code=tsi`, read 2026-09-23
- Example file: `sgptsiskycoverC1.b1.20250818.000000.cdf` from `sgptsiskycoverC1.b1`, 0.35 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
