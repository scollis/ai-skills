---
name: arm-instrument-vdis
description: ARM Video Disdrometer (vdis) - handbook-derived instrument reference. Measurement principle, reported quantities (Center diameter of drop size bin, Number of drops per bin, Number density, Rain amount, Rain rate, Total number of drops, Liquid water content, Smallest drop observed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpvdisdropsC1.b1) and the variable inventory of a real file. Use when working with vdis data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - vdis, Video Disdrometer, sgpvdisdropsC1.b1, Center diameter of drop size bin, Number of drops per bin, Number density, Rain amount, Rain rate, Total number of drops, Surface Meteorology, Joanneum Research 2D-Video Disdrometer (VDIS), DQPR, VDIS.
---

# VDIS - Video Disdrometer

The video disdrometer measures the drop size spectra, shape, and fall velocity of hydrometeors (rain drops) using two orthogonal optical line-scan cameras, deployed outdoors at ARM sites making periodic one-minute observations.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `vdis` |
| Handbook | [DOE/SC-ARM-TR-111 / MJ Bartholomew / June 2020](https://www.arm.gov/publications/tech_reports/handbooks/vdis_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Joanneum Research 2D-Video Disdrometer (VDIS) |
| Primary measurements | Hydrometeor Geometry; Hydrometeor Size Distribution; Hydrometeor fall velocity; Hydrometeor size; Precipitation |
| Record | 1999-12-31 to 2026-09-21 (active) |
| Datastreams with data | 28 across 12 sites |
| Sites | bnf, cor, crg, dst, ena, epc, gan, hou, kcg, sgp, tmp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/vdis |


## Credit

Everything this skill knows about the instrument is the work of **MJ Bartholomew** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MJ Bartholomew. *Two-Dimensional Video Disdrometer (VDIS) Instrument Handbook*, DOE/SC-ARM-TR-111, June 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/vdis_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `disdrometer` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `vdis`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The compact 2D video disdrometer contains two optical paths (A and B), each consisting of an illumination unit with a halogen lamp, a mirror, and a Fresnel lens that shapes the light cone and sets the distance to the center of the measurement area. Two charged-coupled device (CCD) line-scan cameras are directed toward the illumination units, and objects passing through the measurement area (defined by the cross-section of the two optical paths as seen from above) obstruct the light and are detected as shadows by the cameras. The two optical paths are displaced vertically by about 6mm, which allows reconstruction of observables like falling velocity and oblateness by matching each particle's view from camera A and camera B using a synchronous line trigger signal to synchronize shutter/capture control. Additional slit plates and mirrors contribute to compact dimensions and insensitivity to spray.

**Siting.** The site must be level and far enough removed from buildings or structures that might have an impact on local winds. Note: lat/lon/alt refers to the ground where the instrument is sited, NOT the height of the sensor.

**Sampling.** reported every 1 min; averaging All disdrometers make periodic one-minute observations; default observation period t = 60 seconds for W and Z calculations (hb p. 15).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Center diameter of drop size bin | millimeters | - | - | - | (hb p. 8) |
| Number of drops per bin | unitless | - | - | - | (hb p. 8) |
| Number density | 1/m^3 mm | - | - | - | (hb p. 8) |
| Rain amount | millimeters | - | - | - | (hb p. 9) |
| Rain rate | Millimeters/hour | - | - | - | (hb p. 9) |
| Total number of drops | unitless | - | - | - | (hb p. 9) |
| Liquid water content | mm^3/m^3 | - | - | - | (hb p. 9) |
| Smallest drop observed (diameter_min) | millimeters | - | - | - | (hb p. 9) |
| Largest drop observed (diameter_max) | millimeters | - | - | - | (hb p. 9) |
| Calculated radar reflectivity | mm^6/m^3 | - | - | - | (hb p. 9) |
| Marshall-Palmer intercept parameter | 1/m^3mm | - | - | - | (hb p. 9) |
| Marshall-Palmer slope parameter | 1/mm | - | - | - | (hb p. 9) |
| Median volume diameter | millimeters | - | - | - | (hb p. 9) |
| Liquid water distribution mean | millimeters | - | - | - | (hb p. 9) |
| First thru sixth moments of the distribution | mm^1/m^3...mm^6/m^3 | - | - | - | (hb p. 9) |
| Width of bins | millimeters | - | - | 0.2mm | (hb p. 9) |
| Equivolumetric sphere diameter | millimeters | - | - | - | (hb p. 10) |
| Volume of drop | mm^3 | - | - | - | (hb p. 10) |
| Fall speed of drop | m/s | - | - | - | (hb p. 10) |
| Oblateness of drop | unitless | - | - | - | (hb p. 10) |
| Effective measurement area of instrument | mm^2 | - | - | - | (hb p. 10) |
| Height of drop as observed by camera a/b | mm | - | - | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Vertical displacement between optical paths A and B | typically about 6mm | (hb p. 15) |
| Width of bins (bin_width) | 0.2mm | (hb p. 11) |
| Illumination lamp intensity | between 100 and 200 counts | (hb p. 17) |


## The data

Verified example: **`sgpvdisdropsC1.b1`**, file `sgpvdisdropsC1.b1.20260917.025805.cdf`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=6 |
| Data variables | 23 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2026-09-17T02:58:05 to 2026-09-17T14:20:16 |
| dod version | vdisdrops-b1-1.2 |
| process version | ingest-vdis-1.22-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `area` | mm^2 | time | yes | Instrument effective measurement area |
| `drop_height_a` | mm | time | yes | Individual drop height as measured by camera A |
| `drop_height_b` | mm | time | yes | Individual drop height as measured by camera B |
| `drop_volume` | mm^3 | time | yes | Drop volume |
| `drop_width_a` | mm | time | yes | Individual drop width as measured by camera A |
| `drop_width_b` | mm | time | yes | Individual drop width as measured by camera B |
| `equivolumetric_sphere_diameter` | mm | time | yes | Equivolumetric sphere diameter |
| `fall_speed` | m/s | time | yes | Fall speed |
| `oblateness` | unitless | time | yes | Oblateness |
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
                     params={"user": f"{user}:{token}", "ds": "sgpvdisdropsC1.b1",
                             "start": "2026-09-17", "end": "2026-09-17", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpvdisdropsC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpvdisdropsC1.b1", "2026-09-17", "2026-09-17")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpvdisdropsC1.b1", "2026-09-17", "2026-09-17"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("equivolumetric_sphere_diameter", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
23 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_equivolumetric_sphere_diameter"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("equivolumetric_sphere_diameter", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["equivolumetric_sphere_diameter", "drop_volume", "fall_speed"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpvdisdropsC1.b1.20260917.025805.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `drop_width_a` | Value is greater than the fail_max. | 1 | 16.6667 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpvdisdropsC1.b1", "19991231", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: If data are missing for a sample time, a missing_value of -999 is assigned to that field. QC data quality variables (qc_diameter_min, qc_diameter_max, qc_liquid_water_content, qc_liquid_water_distribution_mean, qc_median_volume_diameter, qc_number_drops, qc_rain_amount, qc_rain_rate, qc_slope_parameter, qc_total_drops) are provided per Table 4. Instrument mentor reviews QC once or twice a week, with QC delay of three days behind the current day, using DSview plots for instrument operation status and otherwise DQ HandS diagnostic plots; outputs are DQPR and DQR as needed. Data Quality Office...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Outliers from hydrometeors falling on the edge of the instrument's field of view | Shows up as small drops moving too fast for their expected terminal fall speed | Filter out drops with fall speeds greater than or less than 50% of Gunn and Kinzer (1949) empirically derived terminal fall speeds for rain drops | (hb p. 12) |
| Hydrometeors entering field of view after splashing on the device | Shows up as large drops with fall speeds less than expected for their terminal fall speed | Filter out drops with fall speeds greater than or less than 50% of Gunn and Kinzer (1949) empirically derived terminal fall speeds for rain drops;... | (hb p. 12) |
| Contamination by insects, leaves, spider webs, etc. | Anomalous results in the drop size/velocity data | Filter using fall speed thresholds relative to Gunn and Kinzer (1949) terminal fall speeds; keep sensor free of leaves/debris during maintenance | (hb p. 12) |
| Missing data | Field is assigned a value of -999 (missing_value) | None stated beyond flagging | (hb p. 11) |
| General presence of outliers in disdrometer data | Outliers visible in raw drop distributions/scatterplots of diameter vs. fall speed | Raw data provided in b1-level files; researchers can choose their own level of filtering | (hb p. 12) |
| Illumination lamp intensity drift | Detection/shadow contrast quality changes if lamp intensity drifts outside 100-200 counts | Monitor lamp intensity during maintenance and adjust as necessary to keep within 100-200 counts | (hb p. 17) |
| Vertical displacement between optical paths (plane distance) drift affecting... | Errors in reconstructed observables like falling velocity and oblateness if displacement is mismeasured | Plane distances measured every four months with adjustments made as needed | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | The plane distances (vertical displacement between the two optical paths) are measured and adjustments made as needed. (hb p. 16) |
| Calibration interval | every four months (hb p. 16) |
| Routine maintenance | Inspection of site grounds near the instrument for hazards (rodent burrows, buried conduit trench settling, insect nests); visual inspection of conduit, cables, and connectors for damage, water intrusion, tightness; keep sensor free of leaves/debris; monitor illumination lamp intensity and adjust to keep between 100... (hb p. 16) |
| Maintenance interval | weekly (hb p. 16) |


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
| `2D` | two-dimensional |
| `ARM` | Atmospheric Radiation Measurement |
| `CCD` | charged-coupled device |
| `DQ` | data quality |
| `DQPR` | Data Quality Problem Report |
| `DQR` | Data Quality Report |
| `PM` | preventive maintenance |
| `QC` | quality control |
| `QME` | Quality Measurement Experiment |
| `SGP` | Southern Great Plains |
| `TWP` | Tropical Western Pacific |
| `VAP` | value-added product |
| `VDIS` | video disdrometer |


### References the handbook cites

- Bringi, VN. 2011. Inter-Comparison and Reliability Study of the Next-Generation 2D-Video Disdrometer. U.S. National Aeronautics and Space Administration. Final Report NNX09AD72G.
- Gunn, R, and GD Kinzer. 1949. "The terminal velocity of fall for water droplets in stagnant air." Journal of Meteorology 6(4): 243-248, https://doi.org/10.1175/1520-0469(1949)006less than 0243:TTVOFFgreater than 2.0.CO;2
- Thurai, M, WA Peterson, A Tokay, C Schultz, and P Gatlin. 2011. "Drop size distribution comparison between Parsivel and 2-D video disdrometers." Advances in Geoscience 30: 3-9, https://doi.org/10.5194/adgeo-30-3-2011

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/vdis_handbook.pdf (18 pages, DOE/SC-ARM-TR-111, by MJ Bartholomew)
- Catalog record: ARM data-source index, `instrument_class_code=vdis`, read 2026-09-23
- Example file: `sgpvdisdropsC1.b1.20260917.025805.cdf` from `sgpvdisdropsC1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
