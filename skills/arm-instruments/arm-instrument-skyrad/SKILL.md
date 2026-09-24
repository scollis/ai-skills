---
name: arm-instrument-skyrad
description: ARM Sky Radiometers on Stand for Downwelling Radiation (skyrad) - handbook-derived instrument reference. Measurement principle, reported quantities (Direct Normal Shortwave Irradiance, Downwelling Longwave Irradiance, Ultra Violet Irradiance UV-B), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaskyrad60sC1.b1) and the variable inventory of a real file. Use when working with skyrad data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - skyrad, Sky Radiometers on Stand for Downwelling Radiation, nsaskyrad60sC1.b1, Direct Normal Shortwave Irradiance, Downwelling Longwave Irradiance, Ultra Violet Irradiance UV-B, Radiometric.
---

# SKYRAD - Sky Radiometers on Stand for Downwelling Radiation

The SKYRAD collection of radiometers provides continuous 1-minute measurements of downwelling broadband shortwave (solar), longwave (infrared), and ultraviolet irradiances at ARM Atmospheric Radiation and Cloud Stations in the Tropical Western Pacific and North Slope of Alaska.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 7 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `skyrad` |
| Handbook | [ARM TR-026 / T. Stoffel / November 2004](https://www.arm.gov/publications/tech_reports/handbooks/skyrad_handbook.pdf) |
| Measurement category | Radiometric |
| Primary measurements | Longwave broadband downwelling irradiance; Longwave narrowband brightness temperature; Shortwave broadband diffuse downwelling irradiance; Shortwave broadband direct normal irradiance; Shortwave broadband total downwelling irradiance |
| Record | 1996-10-09 to 2026-09-23 (active) |
| Datastreams with data | 79 across 29 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/skyrad |


## Credit

Everything this skill knows about the instrument is the work of **T. Stoffel** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> T. Stoffel. *SKYRAD Handbook*, ARM TR-026, November 2004.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/skyrad_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Downwelling shortwave (0.3 to 3.0 micrometers) global hemispheric irradiance is measured by an unshaded pyranometer with a hemispheric field of view. Diffuse shortwave irradiance (0.3 to 3.0 micrometers) is measured by a shaded pyranometer with a hemispheric field of view. Direct normal shortwave irradiance is measured by a solar tracking pyrheliometer with a 5.7 degree field of view. Downwelling longwave irradiance (4.0 to 50 micrometers) is measured by a shaded pyrgeometer with a hemispheric field of view, and ultraviolet UV-B irradiance is measured by a UV-Biometer with a hemispheric field of view.

**Siting.** The SKYRAD is operational at the North Slope of Alaska and Tropical Western Pacific sites, part of a network of stations to help determine the total radiative energy exchange within these regions.

**Sampling.** reported every 1-minute (hb p. 3).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Downwelling Shortwave Global Hemispheric Irradiance | - | 0.3 TO 3.0 micrometers | - | - | (hb p. 4) |
| Diffuse Shortwave Diffuse Hemispheric Irradiance | - | 0.3 TO 3.0 micrometers | - | - | (hb p. 4) |
| Direct Normal Shortwave Irradiance | - | - | - | 5.7 degree field of view | (hb p. 4) |
| Downwelling Longwave Irradiance | - | 4.0 to 50 micrometers | - | - | (hb p. 4) |
| Ultra Violet Irradiance UV-B | - | - | - | - | (hb p. 4) |


## The data

Verified example: **`nsaskyrad60sC1.b1`**, file `nsaskyrad60sC1.b1.20260919.000000.nc`
(0.43 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 65 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 60 seconds |
| dod version | skyrad60s-b1-5.2 |
| process version | ingest-skyrad-1.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `down_long_hemisp1` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1 |
| `down_long_hemisp1_max` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Maxima |
| `down_long_hemisp1_min` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Minima |
| `down_long_hemisp1_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_long_hemisp2` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2 |
| `down_long_hemisp2_max` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Maxima |
| `down_long_hemisp2_min` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Minima |
| `down_long_hemisp2_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_short_diffuse_hemisp` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer |
| `down_short_diffuse_hemisp_corrected` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_corrected_max` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_corrected_min` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_max` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_diffuse_hemisp_min` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_diffuse_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Diffuse Hemispheric... |
| `down_short_hemisp` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `down_short_hemisp_corrected` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `down_short_hemisp_corrected_max` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_corrected_min` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_max` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer, Maxima |
| `down_short_hemisp_min` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer, Minima |
| `down_short_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Hemispheric... |
| `short_direct_normal` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer |
| `short_direct_normal_max` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer, Maxima |
| `short_direct_normal_min` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer, Minima |
| `down_long_hemisp1_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Standard... |
| `down_long_hemisp2_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Standard... |
| `down_short_diffuse_hemisp_corrected_std` | W/m^2 | time | - | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_std` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_corrected_std` | W/m^2 | time | - | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |


_5 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsaskyrad60sC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("nsaskyrad60sC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

This datastream carries 65 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("nsaskyrad60sC1.b1", start, end,
                  keep_variables=["down_long_hemisp1", "down_long_hemisp1_max", "down_long_hemisp1_min", "qc_down_long_hemisp1", "qc_down_long_hemisp1_max", "qc_down_long_hemisp1_min"])
```

## Quality control in this datastream

25 `qc_` companion variables cover 25 of the
65 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("nsaskyrad60sC1.b1", "19961009", "20260923")
```

The handbook's own note on data quality: Data quality health and status results are available via DQ HandS (Data Quality Health and Status) and NCVweb for interactive data plotting; these contain the techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality. All DQ Office and most Site Scientist checking techniques have been incorporated within DQ HandS and can be viewed there. Data Quality Flags are described in the SKYRAD Data Object Design Changes for ARM netCDF file header descriptions. Value-added products (VAPs) and Quality Measurement Experiments (QMEs)...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| This section is not applicable to this instrument (no documented artifacts/known problems... | No user notes, known problems, or theory-of-operation details provided in handbook | - | (hb p. 4) |


## Calibration and maintenance

_none recorded in the handbook._


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/skyrad_handbook.pdf (7 pages, ARM TR-026, by T. Stoffel)
- Catalog record: ARM data-source index, `instrument_class_code=skyrad`, read 2026-09-23
- Example file: `nsaskyrad60sC1.b1.20260919.000000.nc` from `nsaskyrad60sC1.b1`, 0.43 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
