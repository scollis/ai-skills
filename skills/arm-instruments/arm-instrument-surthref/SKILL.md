---
name: arm-instrument-surthref
description: ARM Surface Temperature and Humidity Reference System for Sondes (surthref) - handbook-derived instrument reference: measurement principle, reported quantities (Temperature, Relative Humidity, Sonde Present Bit Flag, Temperature, Relative Humidity, Temperature, Relative Humidity, Vaisala HMP-45D Temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpsurthrefC1.b1) and the variable inventory of a real file. Use when working with surthref data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface Meteorology. Triggers - surthref, sgpsurthrefC1.b1, Temperature, Relative Humidity, Sonde Present Bit Flag, Surface Meteorology, Vaisala HMP-45D (HMP-4D Series) T/RH probes, Rotronic MP100H Series T/RH probes, Relative humidity, NIST, SONDE, T/RH.
---

# SURTHREF - Surface Temperature and Humidity Reference System for Sondes

SURTHREF provides accurate reference values of ambient temperature and relative humidity, measured by six co-located T/RH probes (three Vaisala, three Rotronic) in an aspirated chamber at the SGP Central Facility, for comparison with radiosonde prelaunch values.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `surthref` |
| Handbook | [DOE/SC-ARM/TR-068 / February 2011](https://www.arm.gov/publications/tech_reports/handbooks/surthref_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala HMP-45D (HMP-4D Series) T/RH probes; Rotronic MP100H Series T/RH probes; Campbell Scientific CR23X Micrologger data logger |
| Primary measurements | Atmospheric moisture; Atmospheric temperature |
| Record | 2005-07-28 to 2014-09-15 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/surthref |


## Credit

The handbook this skill derives from names no individual author on its cover;
it is issued by the ARM facility. The instrument knowledge in it is still the
mentor programme's work, not this file's:

> ARM Climate Research Facility. *Surface Temperature and Humidity Reference System (SURTHREF) Handbook*, DOE/SC-ARM/TR-068, February 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/surthref_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The SURTHREF system combines three temperature and relative humidity probes each from two different manufacturers (Vaisala and Rotronic) for a total of six probes, housed in a fan-aspirated chamber within a modified Stevenson screen shelter. Radiosondes are placed inside the aspirator on a sonde positioning platform so that comparisons between the six T/RH probes and the radiosonde can be accomplished before launch. A user-operated switch indicates when a radiosonde is placed in or removed from the chamber, and the datalogger counts the seconds each minute the switch is in the "up" position to flag sonde presence. The data logger measures each input once every second, and temperature and relative humidity data are averaged for each of the six probes once per minute, with minimums, maximums, and sonde-present counts also calculated.

**Siting.** The SURTHREF is located at the SGP Central Facility site in Oklahoma, installed in July 2005. It is housed in a modified NWS "Stevenson screen" instrument shelter allowing operator access on two sides, with an internal fan-aspirated chamber. Note: lat/lon/alt dimension variables refer to the ground where the instrument is sited, NOT the height of the sensor.

**Sampling.** native rate each input measured once every second; reported every 1 min (most variables); 5 min (dimension variables base_time/time_offset/time/lat/lon/alt); averaging temperature and relative humidity averaged for each of six probes once per minute; minimums and maximums also calculated per minute (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Temperature (V1, V2, V3, R1, R2, R3) Average | C | - | - | 0.01 | (hb p. 7) |
| Relative Humidity (V1, V2, V3, R1, R2, R3) Average | % | - | - | 0.1 | (hb p. 7) |
| Sonde Present Bit Flag | count | - | - | 1 | (hb p. 8) |
| Temperature (V1, V2, V3, R1, R2, R3) Maximum | C | - | - | 0.01 | (hb p. 8) |
| Relative Humidity (V1, V2, V3, R1, R2, R3) Maximum | % | - | - | 0.1 | (hb p. 8) |
| Temperature (V1, V2, V3, R1, R2, R3) Minimum | C | - | - | 0.01 | (hb p. 8) |
| Relative Humidity (V1, V2, V3, R1, R2, R3) Minimum | % | - | - | 0.1 | (hb p. 8) |
| Vaisala HMP-45D Temperature | C | - | See Data Acquisition Errors | 0.01 C (Precision) | (hb p. 14) |
| Vaisala HMP-45D Relative Humidity | % RH | 0% to 90% RH; 90% to 100% RH | +/-2.0% RH (0% to 90% RH), +/-3.0% RH (90% to... | 0.1% RH (Precision) | (hb p. 14) |
| Rotronic MP100H Temperature | C | - | +/- 0.2 C | 0.01 C (Precision) | (hb p. 14) |
| Rotronic MP100H Relative Humidity | % RH | - | +/-1.5% | 0.1% RH (Precision) | (hb p. 14) |
| Logger Panel Temperature | - | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Vaisala HMP-45D Temperature Precision | 0.01 C | (hb p. 14) |
| Vaisala HMP-45D Temperature Uncertainty | See "Data Acquisition Errors" | (hb p. 14) |
| Vaisala HMP-45D RH Precision | 0.1% RH | (hb p. 14) |
| Vaisala HMP-45D RH Uncertainty | +/-2.0% RH (0% to 90% RH), +/-3.0% RH (90% to 100% RH) | (hb p. 14) |
| Rotronic MP100H Temperature Precision | 0.01 C | (hb p. 14) |
| Rotronic MP100H Temperature Uncertainty | +/- 0.2 C | (hb p. 14) |
| Rotronic MP100H RH Precision | 0.1% RH | (hb p. 14) |
| Rotronic MP100H RH Uncertainty | +/-1.5% | (hb p. 14) |
| CR23X A/D converter accuracy | +/-0.1 % of full-scale range | (hb p. 14) |
| Datalogger time base accuracy | +/-1 min per month, or about 23 ppm | (hb p. 14) |
| Clock correction threshold | corrected if off by more than 2 seconds (checked once per day) | (hb p. 14) |
| Meteorological Instrument Shelter dimensions | 20" x 30" x 34" | (hb p. 13) |
| Aspirated Chamber dimensions | 11" x 13" x 18" (volume = 1.49 ft3) | (hb p. 13) |
| Aspirated Chamber access port | 7" x 7.5" | (hb p. 13) |
| Muffin fans | two, each rated at 115 cfm | (hb p. 13) |
| Estimated face flow | 10.49 fps or 3.2 m/s | (hb p. 13) |
| Sonde platform height above chamber bottom | approximately 1" | (hb p. 13) |


## The data

Verified example: **`sgpsurthrefC1.b1`**, file `sgpsurthrefC1.b1.20140912.000000.cdf`
(0.56 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 93 |
| QC variables | 38 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2014-09-12T00:00:00 to 2014-09-12T23:59:00 |
| sampling interval | 60 seconds |
| averaging interval | None |
| dod version | surthref-b1-1.2 |
| process version | ingest-surthref-3.5-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `count` | unitless | time | yes | Sonde present bit flag |
| `rh_r1_max` | % | time | yes | Relative humidity, Rotronic probe 1, maximum |
| `rh_r1_mean` | % | time | yes | Relative humidity, Rotronic probe 1, mean |
| `rh_r1_min` | % | time | yes | Relative humidity, Rotronic probe 1, minimum |
| `rh_r2_max` | % | time | yes | Relative humidity, Rotronic probe 2, minimum |
| `rh_r2_mean` | % | time | yes | Relative humidity, Rotronic probe 2, mean |
| `rh_r2_min` | % | time | yes | Relative humidity, Rotronic probe 2, minimum |
| `rh_r3_max` | % | time | yes | Relative humidity, Rotronic probe 3, minimum |
| `rh_r3_mean` | % | time | yes | Relative humidity, Rotronic probe 3, mean |
| `rh_r3_min` | % | time | yes | Relative humidity, Rotronic probe 3, minimum |
| `rh_v1_max` | % | time | yes | Relative humidity, Vaisala probe 1, maximum |
| `rh_v1_mean` | % | time | yes | Relative humidity, Vaisala probe 1, mean |
| `rh_v1_min` | % | time | yes | Relative humidity, Vaisala probe 1, minimum |
| `rh_v2_max` | % | time | yes | Relative humidity, Vaisala probe 2, maximum |
| `rh_v2_mean` | % | time | yes | Relative humidity, Vaisala probe 2, mean |
| `rh_v2_min` | % | time | yes | Relative humidity, Vaisala probe 2, minimum |
| `rh_v3_max` | % | time | yes | Relative humidity, Vaisala probe 3, maximum |
| `rh_v3_mean` | % | time | yes | Relative humidity, Vaisala probe 3, mean |
| `rh_v3_min` | % | time | yes | Relative humidity, Vaisala probe 3, minimum |
| `temp_r1_max` | degC | time | yes | Temperature, Rotronic probe 1, maximum |
| `temp_r1_mean` | degC | time | yes | Temperature, Rotronic probe 1, mean |
| `temp_r1_min` | degC | time | yes | Temperature, Rotronic probe 1, minimum |
| `temp_r2_max` | degC | time | yes | Temperature, Rotronic probe 2, maximum |
| `temp_r2_mean` | degC | time | yes | Temperature, Rotronic probe 2, mean |
| `temp_r2_min` | degC | time | yes | Temperature, Rotronic probe 2, minimum |
| `temp_r3_max` | degC | time | yes | Temperature, Rotronic probe 3, maximum |
| `temp_r3_mean` | degC | time | yes | Temperature, Rotronic probe 3, mean |
| `temp_r3_min` | degC | time | yes | Temperature, Rotronic probe 3, minimum |
| `temp_v1_max` | degC | time | yes | Temperature, Vaisala probe 1, maximum |
| `temp_v1_mean` | degC | time | yes | Temperature, Vaisala probe 1, mean |


_21 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpsurthrefC1.b1", "2014-09-12", "2014-09-12")
ds = armlive_open("sgpsurthrefC1.b1", "2014-09-12", "2014-09-12", cleanup_qc=True)
```

This datastream carries 93 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpsurthrefC1.b1", start, end,
                  keep_variables=["count", "rh_r1_max", "rh_r1_mean", "qc_count", "qc_rh_r1_max", "qc_rh_r1_mean"])
```

## Quality control in this datastream

38 `qc_` companion variables cover 37 of the
93 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpsurthrefC1.b1", "20050728", "20260923")
```

The handbook's own note on data quality: Data quality is tracked via Data Quality Health and Status (DQ HandS) and NCVweb. No routine data reviews by the instrument mentor are documented (listed as "None"). The ARM Data Quality Office uses the Data Quality Assessment (DQA) system to inform Site Operators, Site Scientists, and Instrument Team members of instrument and data flow problems and general data quality observations; routine assessment reports are performed on the most recently collected data and used with the Data Quality Problem reports tool to track resolution (forms at http://www.db.arm.gov/). Each primary variable has an...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Temperature dependency of RH% measurements | Differences between Rotronic RH values and Vaisala RH values vary systematically with temperature, as shown in Figure 1 (Rotronic RH minus Vaisala RH at various temperatures) | Calibrations of the various RH values at different temperatures need to be done to characterize the dependency and to account for and correct it | (hb p. 11) |
| Single-temperature RH calibration | Both Rotronic and Vaisala probes are calibrated at one temperature for a variety of RH readings, contributing to the RH-temperature dependency artifact | - | (hb p. 11) |
| Sonde presence detection relies on manual switch | Sonde Present Bit Flag (qc_count) counts seconds per minute the operator-controlled switch was in the 'up' position; any count greater than zero suggests the radiosonde is in the aspirator,... | - | (hb p. 8) |
| QC range/delta flags on temperature and RH | qc_temp variables flagged if outside -40 to 50 C (delta 10); qc_RH variables flagged if outside -2 to 104 % (delta 30) | - | (hb p. 10) |
| Datalogger clock drift | Time base accuracy is +/-1 min per month (about 23 ppm), which could shift timestamps if uncorrected | Collector computer checks the datalogger clock once per day and corrects it if off by more than 2 seconds | (hb p. 14) |
| A/D converter accuracy limitation | Campbell Scientific CR23X A/D converter accuracy is +/-0.1% of full-scale range, contributing to overall measurement uncertainty | - | (hb p. 14) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | See Section 7.4.1 of the SURTHREF User Manual for procedures (hb p. 14) |
| Routine maintenance | This section is not applicable to this instrument (per handbook Section 7.4.2) (hb p. 15) |


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
| `Relative humidity` | Percentage of saturated vapor pressure at the specified temperature |
| `AC` | alternating current |
| `A/D` | Analog to Digital converter |
| `DQA` | Data Quality Assessment |
| `NIST` | National Institute of Standards and Technology |
| `QME` | Quality Measurement Experiment |
| `RH` | Relative Humidity |
| `rms` | root mean square |
| `SGP` | Southern Great Plains |
| `SONDE` | balloon-borne sounding system |
| `T/RH` | temperature/relative humidity (sensor) |
| `VAP` | value-added product |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/surthref_handbook.pdf (16 pages, DOE/SC-ARM/TR-068, no individual author named on the cover)
- Catalog record: ARM data-source index, `instrument_class_code=surthref`, read 2026-09-23
- Example file: `sgpsurthrefC1.b1.20140912.000000.cdf` from `sgpsurthrefC1.b1`, 0.56 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
