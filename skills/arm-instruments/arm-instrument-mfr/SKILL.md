---
name: arm-instrument-mfr
description: ARM Multifilter Radiometer (mfr) - handbook-derived instrument reference. Measurement principle, reported quantities (Irradiance), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmfr7nch25mC1.b1) and the variable inventory of a real file. Use when working with mfr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - mfr, Multifilter Radiometer, sgpmfr7nch25mC1.b1, Irradiance, Radiometric, Yankee Environmental Systems, Inc. MFRSR head (used as MFR), ESRL, IMMS, MFRSR, NIMFR.
---

# MFR - Multifilter Radiometer

The MFR is the head of an MFRSR mounted on a tower pointing down at the surface to measure reflected solar irradiance at six narrowband channels (415, 500, 615, 673, 870, 940 nm) plus one broadband channel.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mfr` |
| Handbook | [DOE/SC-ARM/TR-059 / GB Hodges, JJ Michalsky / January 2011](https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Yankee Environmental Systems, Inc. MFRSR head (used as MFR); Campbell Scientific CR1000 data logger |
| Primary measurements | Shortwave broadband total upwelling irradiance; Shortwave narrowband total upwelling irradiance |
| Record | 1994-03-26 to 2026-09-23 (active) |
| Datastreams with data | 36 across 18 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mao, mos |
| ARM page | https://www.arm.gov/capabilities/instruments/mfr |


## Credit

Everything this skill knows about the instrument is the work of **GB Hodges, JJ Michalsky** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> GB Hodges, JJ Michalsky. *Multifilter Rotating Shadowband Radiometer (MFRSR) Handbook With subsections for the following derivative instruments: Multifilter Radiometer (MFR), Normal Incidence Multifilter Radiometer (NIMFR)*, DOE/SC-ARM/TR-059, January 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `nimfr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `mfr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The MFRSR (and derivative MFR head) is a passive radiometer that measures solar energy in six narrowband channels and one broadband channel using filter detectors housed in a cube. For the MFRSR configuration, four measurements are taken per sample cycle: a nadir (home) measurement, two side-band measurements, and a sun-blocked measurement, with the side-bands used to correct for the portion of sky obscured by the shadowband. When the head is instead mounted on a tower pointing at the surface (as the MFR), it provides spectral measurements of reflected irradiance at the same nominal wavelengths rather than cycling the shadowband to separate diffuse/direct/global components. Corrections applied to the core MFRSR measurements include cosine correction (for angular response to incident irradiance, determined on a cosine bench), diffuse correction (modeled using a Rayleigh sky and the cosine response file), and offset correction (derived from averaged nighttime data to correct inherent sensor bias). Fundamental raw measurements are made in millivolts before conversion to irradiance units.

**Siting.** The instrument should be mounted on a stable post or platform with as few obstructions as possible, ideally with no site obstructions casting a shadow at any point during the day. It must be mounted with the motor toward the equator and aligned north-south, with the shadowband motor angle set to local latitude for correct ephemeris calculation, and the shadowband adjusted at solar noon to shade the diffuser squarely at the sun-blocked stop. For the MFR derivative, the head is instead mounted on a tower pointing at the surface (e.g., at 25-meter and 10-meter levels on towers at SGP, and on the NSA Barrow tower) to measure reflected irradiance rather than sky irradiance.

**Sampling.** native rate Sampling intervals started at 20-second intervals (per catalog description; handbook describes shadowband motor half-step increments occurring every five or six 20-second sampling intervals); averaging Sampling rates and averaging periods can be changed on original logger; new CR1000 logger provides programming flexibility for tailoring operation (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Irradiance (reflected, via MFR head pointed at surface;... | millivolts (fundamental... | ± 250 millivolts | 0.06% of 250 millivolts, i.e., 0.15 millivolts | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | millivolts (fundamental measurements) | (hb p. 13) |
| Range | ± 250 millivolts | (hb p. 13) |
| Accuracy | 0.06% of 250 millivolts, i.e., 0.15 millivolts | (hb p. 13) |
| Repeatability | 33.3 µvolts (if differential measurement) | (hb p. 13) |
| Uncertainty | 0.06% of 250 millivolts | (hb p. 14) |
| Input Voltage | Excitation voltage for thermistors is 5 volts | (hb p. 14) |
| Input Current | 1 nano-amperes (typical) | (hb p. 14) |
| Narrowband channel wavelengths | 415, 500, 615, 673, 870, 940 nm | (hb p. 7) |


## The data

Verified example: **`sgpmfr7nch25mC1.b1`**, file `sgpmfr7nch25mC1.b1.20260920.070000.nc`
(0.74 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4320, `bench_angle`=181, `wavelength`=750 |
| Data variables | 81 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-09-20T07:00:00 to 2026-09-21T06:59:40 |
| sampling interval | 20 seconds |
| dod version | mfr7nch25m-b1-1.0 |
| process version | ingest-mfr7nch-1.6-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `head_temp` | degC | time | yes | Detector cluster temperature |
| `head_temp2` | degC | time | yes | HTC3000 feedback temperature |
| `logger_temperature` | degC | time | yes | Internal logger temperature |
| `logger_volt` | V | time | yes | Data logger supply voltage |
| `up_hemisp_narrowband_filter1` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter1, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter2` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter2, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter3` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter3, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter4` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter4, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter5` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter5, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter6` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter6, offset corrected, diffuse... |
| `up_hemisp_narrowband_filter7` | W/(m^2 nm) | time | yes | 25m surface reflected irradiance filter7, offset corrected, diffuse... |
| `airmass` | 1 | time | - | Airmass |
| `azimuth_angle` | degree | time | - | Azimuth angle |
| `bench_angle` | degree | bench_angle | - | Angle of incidence during cosine bench measurements |
| `cosine_correction_sn_filter1` | 1 | bench_angle | - | Cosine correction, south to north, filter1 |
| `cosine_correction_sn_filter2` | 1 | bench_angle | - | Cosine correction, south to north, filter2 |
| `cosine_correction_sn_filter3` | 1 | bench_angle | - | Cosine correction, south to north, filter3 |
| `cosine_correction_sn_filter4` | 1 | bench_angle | - | Cosine correction, south to north, filter4 |
| `cosine_correction_sn_filter5` | 1 | bench_angle | - | Cosine correction, south to north, filter5 |
| `cosine_correction_sn_filter6` | 1 | bench_angle | - | Cosine correction, south to north, filter6 |
| `cosine_correction_sn_filter7` | 1 | bench_angle | - | Cosine correction, south to north, filter7 |
| `cosine_correction_we_filter1` | 1 | bench_angle | - | Cosine correction, west to east, filter1 |
| `cosine_correction_we_filter2` | 1 | bench_angle | - | Cosine correction, west to east, filter2 |
| `cosine_correction_we_filter3` | 1 | bench_angle | - | Cosine correction, west to east, filter3 |
| `cosine_correction_we_filter4` | 1 | bench_angle | - | Cosine correction, west to east, filter4 |
| `cosine_correction_we_filter5` | 1 | bench_angle | - | Cosine correction, west to east, filter5 |
| `cosine_correction_we_filter6` | 1 | bench_angle | - | Cosine correction, west to east, filter6 |
| `cosine_correction_we_filter7` | 1 | bench_angle | - | Cosine correction, west to east, filter7 |
| `cosine_solar_zenith_angle` | 1 | time | - | Cosine apparent solar zenith angle |
| `diffuse_correction_filter1` | 1 | - | - | Diffuse correction derived from Cosine correction of filter1,... |


_37 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpmfr7nch25mC1.b1",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmfr7nch25mC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmfr7nch25mC1.b1", "2026-09-20", "2026-09-20")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmfr7nch25mC1.b1", "2026-09-20", "2026-09-20"))   # cite what you pulled
```

This datastream carries 81 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpmfr7nch25mC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["head_temp", "head_temp2", "logger_temperature", "qc_head_temp", "qc_head_temp2", "qc_logger_temperature"],
                                cleanup_qc=True)
```

## Quality control in this datastream

11 `qc_` companion variables cover 11 of the
81 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_up_hemisp_narrowband_filter1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("up_hemisp_narrowband_filter1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["up_hemisp_narrowband_filter1", "up_hemisp_narrowband_filter2", "up_hemisp_narrowband_filter3"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpmfr7nch25mC1.b1", "19940326", "20260923")
```

The handbook's own note on data quality: Data quality is monitored via the ARM Data Quality Health and Status (DQ HandS) system (http://dq.arm.gov/), which contains tables and graphs showing techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality. Near real-time data plots are available via the DQ HandS plot browser (http://plot.dmf.arm.gov/plotbrowser/). Data levels progress from .00 (raw) to .b1 (lamp-calibrated) to .c1 (Langley-calibrated with aerosol optical depth) to .s1 (subset of .c1, sufficient for most users).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Shadowband coarse stepping / shading issue (MFRSR-specific, relevant to head design... | If the shadowband is adjusted either right after or just before it moves to a new position, it can result in a shading issue in the morning or afternoon, since the shadowband only moves to... | Finer stepping (e.g., 1/8 steps or 0.225 degrees) would all but eliminate the shadowband adjusting issue; not yet implemented by ARM | (hb p. 7) |
| EMF interference from bang-on/bang-off heater (original logger) | Creation of a 'saw tooth' trace of head temperature; EMF interference with irradiance measurements when heater cycles on/off | Original logger designed to stop heater during measurement; new Campbell logger uses proportional heating, eliminating the saw-tooth pattern and EMF... | (hb p. 6) |
| Inherent sensor offset bias | Each sensor exhibits an inherent bias that varies with time, seen when comparing daytime signal to nighttime baseline | Nighttime data are averaged to produce an offset correction for the following day, calculated on an ongoing basis rather than relying on a single... | (hb p. 16) |
| Cosine response error (angular dependence of instrument response) | Instrument has a varying response to incident irradiance depending on solar disc direction; deviates from theoretical cosine response of one at non-overhead sun angles | Cosine correction determined in laboratory with a cosine bench at one-degree intervals between -90° and 90° in S-N and W-E directions, used to build... | (hb p. 15) |
| Diffuse correction approximation | Diffuse irradiance correction based on modeled Rayleigh/isotropic sky rather than actual sky conditions at time of measurement | Handbook states using an isotropic sky produces a value within one percent of actual sky conditions, and since diffuse correction is small it is not... | (hb p. 16) |
| 940 nm channel cannot be Langley-calibrated | 940 nm channel calibration relies only on lamp (nominal) calibration, not the more accurate Langley calibration; may show greater calibration uncertainty relative to other channels | Each head returned to SGP calibration facility annually for lamp calibration of the 940 channel due to highly variable atmospheric water vapor | (hb p. 18) |
| Old-style logger cannot capture side-band, sun-blocked, or thermistor data for analysis | Certain internally used measurements (side-band, sun-blocked, head thermistors) are absent from data produced by original/old-style loggers, limiting diagnostic capability | Campbell CR1000-based logging system now records and makes available side-band measurements, sun-blocked measurement, and both head thermistors | (hb p. 11) |
| Rapidly changing sky conditions affecting side-band measurements | Side-band measurements (just before/after sun-blocked measurement) show impact of rapidly changing sky conditions on final derived values | - | (hb p. 11) |
| Site obstructions causing shadowing | Instrument output shows shadow-induced dips/anomalies if obstructions (trees, buildings) cast a shadow over the instrument at some point during the day | Site selection should avoid obstructions where possible; perfect sites not usually available so compromise is required | (hb p. 17) |
| NIMFR shading issues absent but tracker-dependent | Not directly an MFR artifact, but noted contrast: NIMFR has no shading issues since it has no shadowband, unlike MFRSR/MFR shared head design | - | (hb p. 18) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Standard lamp calibration (nominal calibration), cosine response determination on a cosine bench, spectral response (filter function) mapping, and field Langley calibration once deployed with sufficient data collected (hb p. 17) |
| Calibration interval | Annual return to SGP calibration facility for lamp calibration (since Langley calibration cannot be performed for the 940 nm channel due to variable water vapor) (hb p. 17) |
| Traceability | Lamp calibration performed at SGP calibration facility prior to deployment; nominal calibration data in .b1 files, Langley-calibrated data in .c1 files (hb p. 17) |
| Routine maintenance | Cleaning of the Spectralon diffuser; checking and replacing desiccant in heads that include desiccant holders (hb p. 18) |
| Maintenance interval | Diffuser cleaned from once daily to once every two weeks depending on site location; desiccant checked monthly and replaced as necessary (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR (Multifilter Rotating Shadowband Radiometer), NIMFR (Normal Incidence Multifilter Radiometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `EMF` | electromagnetic field |
| `ESRL` | Earth System Research Laboratory |
| `FOV` | field-of-view |
| `GMD` | Global Monitoring Division |
| `IMMS` | Instrument Mentor Monthly Summary |
| `MFR` | multifilter radiometer |
| `MFRSR` | multifilter rotating shadowband radiometer |
| `NIMFR` | normal incidence multifilter radiometer |
| `NOAA` | National Oceanic Atmospheric Administration |
| `NSA` | North Slope of Alaska |
| `SGP` | Southern Great Plains |
| `TWP` | Tropical Western Pacific |


### References the handbook cites

- Harrison, Lee, Joseph Michalsky, and Jerry Berndt. 1994. "Automated Multifilter Rotating Shadow-Band Radiometer: An Instrument for Optical Depth and Radiation Measurements." Applied Optics 33: 5118-5125.
- Harrison, Lee, and Joseph Michalsky. 1994. "Objective Algorithms for the Retrieval of Optical Depths from Ground-Based Measurements." Applied Optics 33: 5126-5132.
- Michalsky, J.J., J.C. Liljegren, and L.C. Harrison. 1995. "A Comparison of Sun Photometer Derivations of Total Column Water Vapor and Ozone to Standard Measures of Same at the Southern Great Plains Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf (20 pages, DOE/SC-ARM/TR-059, by GB Hodges, JJ Michalsky)
- Catalog record: ARM data-source index, `instrument_class_code=mfr`, read 2026-09-23
- Example file: `sgpmfr7nch25mC1.b1.20260920.070000.nc` from `sgpmfr7nch25mC1.b1`, 0.74 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
