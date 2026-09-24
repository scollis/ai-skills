---
name: arm-instrument-mfr-air
description: ARM Multifilter Radiometer aboard aircraft (mfr-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflected, Fundamental voltage measurement), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmfraafF2.b1) and the variable inventory of a real file. Use when working with mfr-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Radiometric. Triggers - mfr-air, Multifilter Radiometer aboard aircraft, sgpmfraafF2.b1, Reflected, Fundamental voltage measurement, Airborne Observations, Radiometric, Yankee Environmental Systems, Inc. MFRSR head (used as MFR), MFRSR, NIMFR, IMMS.
---

# MFR-AIR - Multifilter Radiometer aboard aircraft

The MFR (Multifilter Radiometer), of which the mfr-air aircraft variant is an airborne deployment, is simply the head of an MFRSR mounted and pointed at the surface (rather than the sky) to measure reflected/upwelling shortwave broadband and narrowband irradiance, with ARM operating one such unit mounted on a Cessna flying out of Ponca City airport.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mfr-air` |
| Handbook | [DOE/SC-ARM/TR-059 / GB Hodges, JJ Michalsky / January 2011](https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf) |
| Measurement category | Airborne Observations; Radiometric |
| Manufacturer / model | Yankee Environmental Systems, Inc. MFRSR head (used as MFR); Campbell Scientific CR1000 data logger (for tower/ground MFR units; NIMFR and some MFR variants use older-style loggers) |
| Primary measurements | Shortwave broadband total upwelling irradiance; Shortwave narrowband total upwelling irradiance |
| Record | 2012-10-15 to 2016-09-10 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/mfr-air |


## Credit

Everything this skill knows about the instrument is the work of **GB Hodges, JJ Michalsky** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> GB Hodges, JJ Michalsky. *Multifilter Rotating Shadowband Radiometer (MFRSR) Handbook With subsections for the following derivative instruments: Multifilter Radiometer (MFR), Normal Incidence Multifilter Radiometer (NIMFR)*, DOE/SC-ARM/TR-059, January 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `mfr-air`, ARM links no handbook to this class. The facts below come from the **Multifilter Radiometer** (`mfr`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `mfr-air` until checked against that document's own section for it.

## How it measures

The MFR is the head of a multifilter rotating shadowband radiometer (MFRSR) mounted so that it points at the surface rather than the sky, using the same electronics cube and sensors as the MFRSR. It is a passive radiometer measuring solar energy reflected from the surface in six narrowband channels (nominal wavelengths 415, 500, 615, 673, 870, and 940 nm) and one open/broadband channel. Because it is not making the shadowband-based diffuse/global/direct decomposition against the sky, it reports the reflected (upwelling) irradiance at these channels rather than the direct/diffuse/global downwelling components described for the standard MFRSR. The internal electronics and sensors are the same as the MFRSR head; only the housing and mounting differ for tower or aircraft deployment.

**Siting.** For the MFR variant, the MFRSR head is mounted on a tower or platform pointed at the surface (nadir-viewing) rather than at the sky, to measure reflected irradiance. ARM operates ground-based MFRs at SGP (25-m and 10-m levels of towers) and at NSA Barrow, and one MFR is mounted on a Cessna flying out of the Ponca City airport for airborne measurements (data were collected up until about December 2009; the instrument remains on the plane with plans to resume measurements). The Barrow (and former Atqasuk) MFR units use the same internal electronics/sensors as SGP units but in a custom housing providing more insulation and facilitating tower mounting. For the parent MFRSR, siting requires...

**Sampling.** native rate Sampling intervals started at 20-second intervals for shadowband positioning on the parent MFRSR; not separately specified for the aircraft MFR (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Reflected (upwelling) irradiance at six narrowband channels... | - | - | - | - | (hb p. 19) |
| Fundamental voltage measurement (as for parent MFRSR head) | millivolts | ± 250 millivolts | 0.06% of 250 millivolts, i.e., 0.15 millivolts | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | millivolts | (hb p. 13) |
| Range | ± 250 millivolts | (hb p. 13) |
| Accuracy | 0.06% of 250 millivolts, i.e., 0.15 millivolts | (hb p. 13) |
| Repeatability | 33.3 µvolts (if differential measurement) | (hb p. 13) |
| Uncertainty | 0.06% of 250 millivolts | (hb p. 14) |
| Input Voltage | Excitation voltage for thermistors is 5 volts | (hb p. 14) |
| Input Current | 1 nano-amperes (typical) | (hb p. 14) |
| Nominal narrowband channel wavelengths | 415, 500, 615, 673, 870, and 940 nm | (hb p. 7) |


## The data

Verified example: **`sgpmfraafF2.b1`**, file `sgpmfraafF2.b1.20160905.142406.nc`
(2.33 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=14471 |
| Data variables | 59 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-05T14:24:06 to 2016-09-05T18:25:37 |
| sampling interval | 1 second |
| averaging interval | None |
| dod version | mfraaf-b1-2.3 |
| process version | ingest-mfraaf-1.4-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `head_temp` | degC | time | yes | Detector temperature |
| `head_temp2` | degC | time | yes | Second detector temperature |
| `logger_volt` | V | time | yes | Data logger supply voltage |
| `temp_logger` | degC | time | yes | Logger temperature |
| `up_hemisp_broadband` | counts | time | yes | Upwelling broadband hemispheric irradiance via aircraft |
| `up_hemisp_narrowband_filter1` | W/(m^2 nm) | time | yes | Upwelling narrowband hemispheric irradiance, filter 1, via aircraft |
| `up_hemisp_narrowband_filter2` | W/(m^2 nm) | time | yes | Upwelling narrowband hemispheric irradiance, filter 2, via aircraft |
| `up_hemisp_narrowband_filter3` | W/(m^2 nm) | time | yes | Upwelling narrowband hemispheric irradiance, filter 3, via aircraft |
| `up_hemisp_narrowband_filter4` | W/(m^2 nm) | time | yes | Upwelling narrowband hemispheric irradiance, filter 4, via aircraft |
| `up_hemisp_narrowband_filter5` | W/(m^2 nm) | time | yes | Upwelling narrowband hemispheric irradiance, filter 5, via aircraft |
| `up_hemisp_narrowband_filter6` | W/m^2-nm | time | yes | Upwelling narrowband hemispheric irradiance, filter 6, via aircraft |
| `course_true` | degree | time | - | True course over ground |
| `diffuse_correction_broadband` | unitless | - | - | Cosine correction of broadband diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter1` | unitless | - | - | Cosine correction of filter1 diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter2` | unitless | - | - | Cosine correction of filter2 diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter3` | unitless | - | - | Cosine correction of filter3 diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter4` | unitless | - | - | Cosine correction of filter4 diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter5` | unitless | - | - | Cosine correction of filter5 diffuse, assuming Rayleigh sky at 45... |
| `diffuse_correction_filter6` | unitless | - | - | Cosine correction of filter6 diffuse, assuming Rayleigh sky at 45... |
| `fix_quality` | unitless | time | - | GPS signal quality indicator |
| `gps_date_utc` | unitless | time | - | Time as recorded by GPS, date in ddmmyy form. |
| `gps_ready` | unitless | time | - | Number of valid sentences that must be received before clock... |
| `gps_time_utc` | unitless | time | - | Time as recorded by GPS, time in the form hhmmss. |
| `ground_speed` | m/s | time | - | Speed over ground |
| `magnetic_variation` | degree | time | - | Magnetic direction correction (+ for east, - for west) |
| `max_time_adjust` | s | time | - | Maximum time adjustment that has occurred since the data logger... |
| `nominal_calibration_factor_broadband` | count/(W/m^2) | - | - | Nominal calibration factor, applied to broadband data |
| `nominal_calibration_factor_filter1` | count/W/(m^2 nm) | - | - | Nominal calibration factor, applied to filter1 data |
| `nominal_calibration_factor_filter2` | count/W/(m^2 nm) | - | - | Nominal calibration factor, applied to filter2 data |
| `nominal_calibration_factor_filter3` | count/W/(m^2 nm) | - | - | Nominal calibration factor, applied to filter3 data |


_14 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmfraafF2.b1", "2016-09-05", "2016-09-05")
ds = armlive_open("sgpmfraafF2.b1", "2016-09-05", "2016-09-05", cleanup_qc=True)
```

This datastream carries 59 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpmfraafF2.b1", start, end,
                  keep_variables=["head_temp", "head_temp2", "logger_volt", "qc_head_temp", "qc_head_temp2", "qc_logger_volt"])
```

## Quality control in this datastream

11 `qc_` companion variables cover 11 of the
59 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpmfraafF2.b1.20160905.142406.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `head_temp2` | Difference between current and previous values exceeds... | 1273 | 8.7969 |
| `head_temp` | Difference between current and previous values exceeds... | 62 | 0.4284 |
| `head_temp2` | Value is less than the fail_min. | 17 | 0.1175 |
| `up_hemisp_broadband` | Value is less than the fail_min. | 11 | 0.076 |
| `up_hemisp_narrowband_filter4` | Value is less than the fail_min. | 11 | 0.076 |
| `up_hemisp_narrowband_filter2` | Value is less than the fail_min. | 9 | 0.0622 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpmfraafF2.b1", "20121015", "20260924")
```

The handbook's own note on data quality: Data quality is monitored via the ARM Data Quality Health and Status (DQ HandS) system (http://dq.arm.gov/) and near real-time plots via the plot browser (http://plot.dmf.arm.gov/plotbrowser/); the tables/graphs there contain techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality. An Instrument Mentor Monthly Summary is also produced.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Shading issues from coarse shadowband stepping (relevant to parent MFRSR/MFR... | Anomalous dip or spike in irradiance values in the morning or afternoon when the shadowband is adjusted near a step transition | Use finer stepping increments (e.g., 1/8 step or finer) in motor controller design; adjust shadowband away from step transition times | (hb p. 7) |
| 940 nm channel cannot be Langley-calibrated | 940 nm channel data quality/calibration traceability differs from other channels; relies solely on lamp (nominal) calibration rather than higher-accuracy Langley calibration | Each head is returned annually to the SGP calibration facility for lamp calibration of this channel | (hb p. 18) |
| EMF interference from bang-on/bang-off head heater (older-style logger/instrument... | Saw-tooth pattern in head temperature trace; potential irradiance measurement interference coincident with heater on/off transitions | Original logger gives irradiance measurements priority and stops heater during a measurement; newer Campbell-based systems use proportional heating... | (hb p. 12) |
| Sensor bias/offset inherent in each sensor | Non-zero nighttime baseline signal | Nighttime data are averaged to produce an offset correction applied to the following day's data on an ongoing basis (rather than a single... | (hb p. 16) |
| Instrument angular (cosine) response error | Departure of measured irradiance from theoretical cosine response depending on solar disc direction/zenith angle | Cosine correction determined in the laboratory with a cosine bench at one-degree intervals between -90 and 90 degrees in S-N and W-E directions, used... | (hb p. 15) |
| Site obstructions casting shadows | Anomalous irradiance dips at times of day corresponding to obstruction shadow crossing the instrument | Site selection should avoid obstructions (trees, buildings) that cast a shadow over the instrument at any point during the day; perfect sites are... | (hb p. 16) |
| Diffuse correction approximation using isotropic sky model | Diffuse irradiance correction differs from true sky conditions by up to about one percent | Handbook notes the diffuse correction is small enough that point-by-point correction based on current sky conditions is not considered worth the... | (hb p. 16) |
| Data collection gap on aircraft-mounted MFR | No data recorded from about December 2009 onward for the Cessna-mounted MFR (mfr-air) until measurements resume | Instrument remains mounted on the plane with plans to resume measurements in the future | (hb p. 19) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Each instrument head is run through the SGP calibration facility including a standard lamp calibration, cosine response determination, and mapping of the spectral response function (filter function) of each filter detector; once deployed with enough data collected, the instrument is Langley-calibrated (though Langley... (hb p. 17) |
| Calibration interval | Heads are returned to the SGP calibration facility annually for lamp calibration (and re-run through cosine and spectral benches). (hb p. 17) |
| Traceability | Nominal (lamp) calibration data are contained in .b1 data files; Langley-calibrated data are contained in .c1 data files. (hb p. 17) |
| Routine maintenance | Low-maintenance instrument; the only regular maintenance required once deployed is cleaning of the Spectralon diffuser. Some heads include desiccant holders whose desiccant should be checked and replaced as necessary. (hb p. 18) |
| Maintenance interval | Diffuser cleaning from once daily to once every two weeks depending on site location; desiccant checked monthly. (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR, NIMFR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `MFR` | multifilter radiometer |
| `MFRSR` | multifilter rotating shadowband radiometer |
| `NIMFR` | normal incidence multifilter radiometer |
| `FOV` | field-of-view |
| `AMF` | ARM Mobile Facility |
| `SGP` | Southern Great Plains |
| `NSA` | North Slope of Alaska |
| `TWP` | Tropical Western Pacific |
| `VAP` | value-added product |
| `EMF` | electromagnetic field |
| `VAC` | volts alternating current |
| `IMMS` | Instrument Mentor Monthly Summary |


### References the handbook cites

- Harrison, Lee, Joseph Michalsky, and Jerry Berndt. 1994. "Automated Multifilter Rotating Shadow-Band Radiometer: An Instrument for Optical Depth and Radiation Measurements." Applied Optics 33: 5118–5125.
- Harrison, Lee, and Joseph Michalsky. 1994. "Objective Algorithms for the Retrieval of Optical Depths from Ground-Based Measurements." Applied Optics 33: 5126–5132.
- Michalsky, J.J., J.C. Liljegren, and L.C. Harrison. 1995. "A Comparison of Sun Photometer Derivations of Total Column Water Vapor and Ozone to Standard Measures of Same at the Southern Great Plains Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mfr_handbook.pdf (20 pages, DOE/SC-ARM/TR-059, by GB Hodges, JJ Michalsky)
- Catalog record: ARM data-source index, `instrument_class_code=mfr-air`, read 2026-09-24
- Example file: `sgpmfraafF2.b1.20160905.142406.nc` from `sgpmfraafF2.b1`, 2.33 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
