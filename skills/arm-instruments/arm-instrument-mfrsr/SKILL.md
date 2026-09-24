---
name: arm-instrument-mfrsr
description: ARM Multifilter Rotating Shadowband Radiometer (mfrsr) - handbook-derived instrument reference. Measurement principle, reported quantities (Narrowband channel wavelengths, Open/broadband channel irradiance, Direct, Aerosol optical depth, Fundamental voltage measurement, Head thermistor temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmfrsr7nchC1.b1) and the variable inventory of a real file. Use when working with mfrsr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - mfrsr, Multifilter Rotating Shadowband Radiometer, sgpmfrsr7nchC1.b1, Narrowband channel wavelengths, Open/broadband channel irradiance, Direct, Aerosol optical depth, Fundamental voltage measurement, Radiometric, Yankee Environmental Systems, Inc. MFRSR head, cordif.
---

# MFRSR - Multifilter Rotating Shadowband Radiometer

The visible Multifilter Rotating Shadowband Radiometer (MFRSR) is a passive instrument, mounted on a fixed north-south aligned post/platform with its motor pointed toward the equator, that measures global and diffuse components of solar irradiance at six narrowband channels (415, 500, 615, 673, 870, 940 nm) and one open/broadband channel, from which direct irradiance and aerosol optical depth are derived.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mfrsr` |
| Handbook | [DOE/SC-ARM-TR-144 / GB Hodges, JJ Michalsky / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Yankee Environmental Systems, Inc. MFRSR head; Campbell Scientific CR1000 data logger |
| Primary measurements | Shortwave broadband diffuse downwelling irradiance; Shortwave broadband direct normal irradiance; Shortwave broadband total downwelling irradiance; Shortwave narrowband diffuse downwelling irradiance; Shortwave narrowband direct normal irradiance; Shortwave narrowband total downwelling irradiance |
| Record | 1996-10-21 to 2026-09-23 (active) |
| Datastreams with data | 160 across 29 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/mfrsr |


## Credit

Everything this skill knows about the instrument is the work of **GB Hodges, JJ Michalsky** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> GB Hodges, JJ Michalsky. *Multifilter Rotating Shadowband Radiometer Instrument Handbook (With subsections for derivative instruments: Multifilter Radiometer (MFR), Normal Incidence Multifilter Radiometer (NIMFR))*, DOE/SC-ARM-TR-144, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `gndmfr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `mfrsr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The MFRSR is a passive radiometer, not a sun photometer, that measures solar energy in six narrowband channels and one broadband channel by taking four measurements per data record: the shadowband-in-home (nadir/unblocked) position, a first side-band measurement, the sun-blocked measurement, and a second side-band measurement. The side-band measurements correct for the portion of sky obscured by the shadowband during the sun-blocked measurement. Direct beam irradiance is not measured directly but is calculated from the global (total) and diffuse measurements. Three corrections are then applied: a cosine correction (for the instrument's varying angular response, determined on a laboratory cosine bench), a diffuse correction (modeled using a Rayleigh sky with the cosine response file, since diffuse energy arrives from all directions), and an offset correction (derived from averaged nighttime data to remove sensor bias). From the resulting optical depths at each wavelength, column abundances of ozone, water vapor, aerosol, and other atmospheric constituents can be inferred.

**Siting.** The instrument should be mounted on a stable post or platform in a location with as few obstructions as possible, ideally with no obstructions casting a shadow over the instrument at any time of day. It must be mounted with the motor toward the Equator and aligned north-south, with the shadowband motor angle set to the local latitude (needed for the ephemeris calculation). The shadowband must be adjusted, ideally at solar noon, so it shades the diffuser squarely at the sun-blocked shadowband stop. Newer Yankee MFRSR versions (with three motor mounting holes) use a different mounting/adjustment method, not currently operated by ARM.

**Sampling.** native rate sampling intervals started at 20-second intervals; reported every one data record comprises 4 shadowband-position measurements (home, first side-band, sun-blocked, second side-band); averaging nighttime data averaged to produce offset correction for the following day (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Global and diffuse solar irradiance (narrowband) | millivolts (fundamental... | - | - | - | (hb p. 7) |
| Narrowband channel wavelengths | nm | 415, 500, 615, 673, 870, 940 nm nominal | - | - | (hb p. 7) |
| Open/broadband channel irradiance | - | - | - | - | (hb p. 7) |
| Direct (direct beam) irradiance | - | - | - | - | (hb p. 7) |
| Aerosol optical depth | - | - | - | - | (hb p. 7) |
| Fundamental voltage measurement | millivolts | ± 250 millivolts | 0.06% of 250 millivolts, i.e., 0.15 millivolts | - | (hb p. 14) |
| Head thermistor temperature | - | - | - | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | millivolts (fundamental measurements) | (hb p. 14) |
| Range | ± 250 millivolts | (hb p. 14) |
| Accuracy | 0.06% of 250 millivolts, i.e., 0.15 millivolts | (hb p. 14) |
| Repeatability | 33.3 µvolts (if differential measurement) | (hb p. 14) |
| Uncertainty | 0.06% of 250 millivolts | (hb p. 14) |
| Input Voltage | Excitation voltage for thermistors is 5 volts | (hb p. 14) |
| Input Current | 1 nano-ampere (typical) | (hb p. 15) |
| Head operating temperature | near 40°C | (hb p. 13) |
| Shadowband motor step | half-step increment moves the band 0.45 degrees (original Campbell motor controller); one-eighth step option = 0.225 degrees | (hb p. 8) |
| Sampling interval | 20-second intervals | (hb p. 8) |
| Power | 120 VAC | (hb p. 19) |


## The data

Verified example: **`sgpmfrsr7nchC1.b1`**, file `sgpmfrsr7nchC1.b1.20260922.070000.nc`
(2.1 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4320, `bench_angle`=181, `wavelength`=750 |
| Data variables | 158 |
| QC variables | 46 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-09-22T07:00:00 to 2026-09-23T06:59:40 |
| sampling interval | 20 seconds |
| dod version | mfrsr7nch-b1-1.1 |
| process version | ingest-mfrsr7nch-1.8-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `alltime_hemisp_narrowband_filter1` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 1 |
| `alltime_hemisp_narrowband_filter2` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 2 |
| `alltime_hemisp_narrowband_filter3` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 3 |
| `alltime_hemisp_narrowband_filter4` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 4 |
| `alltime_hemisp_narrowband_filter5` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 5 |
| `alltime_hemisp_narrowband_filter6` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 6 |
| `alltime_hemisp_narrowband_filter7` | mV | time | yes | Alltime narrowband hemispheric irradiance, filter 7 |
| `diffuse_hemisp_narrowband_filter1` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 1, offset and... |
| `diffuse_hemisp_narrowband_filter2` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 2, offset and... |
| `diffuse_hemisp_narrowband_filter3` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 3, offset and... |
| `diffuse_hemisp_narrowband_filter4` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 4, offset and... |
| `diffuse_hemisp_narrowband_filter5` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 5, offset and... |
| `diffuse_hemisp_narrowband_filter6` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 6, offset and... |
| `diffuse_hemisp_narrowband_filter7` | W/(m^2 nm) | time | yes | Narrowband diffuse hemispheric irradiance, filter 7, offset and... |
| `direct_diffuse_ratio_filter1` | 1 | time | yes | Ratio of direct_normal_filter1 to diffuse_hemisp_filter1 |
| `direct_diffuse_ratio_filter2` | 1 | time | yes | Ratio of direct_normal_filter2 to diffuse_hemisp_filter2 |
| `direct_diffuse_ratio_filter3` | 1 | time | yes | Ratio of direct_normal_filter3 to diffuse_hemisp_filter3 |
| `direct_diffuse_ratio_filter4` | 1 | time | yes | Ratio of direct_normal_filter4 to diffuse_hemisp_filter4 |
| `direct_diffuse_ratio_filter5` | 1 | time | yes | Ratio of direct_normal_filter5 to diffuse_hemisp_filter5 |
| `direct_diffuse_ratio_filter6` | 1 | time | yes | Ratio of direct_normal_filter6 to diffuse_hemisp_filter6 |
| `direct_diffuse_ratio_filter7` | 1 | time | yes | Ratio of direct_normal_filter6 to diffuse_hemisp_filter7 |
| `direct_horizontal_narrowband_filter1` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 1, cosine corrected |
| `direct_horizontal_narrowband_filter2` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 2, cosine corrected |
| `direct_horizontal_narrowband_filter3` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 3, cosine corrected |
| `direct_horizontal_narrowband_filter4` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 4, cosine corrected |
| `direct_horizontal_narrowband_filter5` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 5, cosine corrected |
| `direct_horizontal_narrowband_filter6` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 6, cosine corrected |
| `direct_horizontal_narrowband_filter7` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 7, cosine corrected |
| `direct_normal_narrowband_filter1` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 1, cosine corrected |
| `direct_normal_narrowband_filter2` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 2, cosine corrected |


_79 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmfrsr7nchC1.b1", "2026-09-22", "2026-09-22")
ds = armlive_open("sgpmfrsr7nchC1.b1", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

This datastream carries 158 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpmfrsr7nchC1.b1", start, end,
                  keep_variables=["alltime_hemisp_narrowband_filter1", "alltime_hemisp_narrowband_filter2", "alltime_hemisp_narrowband_filter3", "qc_alltime_hemisp_narrowband_filter1", "qc_alltime_hemisp_narrowband_filter2", "qc_alltime_hemisp_narrowband_filter3"])
```

## Quality control in this datastream

46 `qc_` companion variables cover 46 of the
158 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpmfrsr7nchC1.b1.20260922.070000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `diffuse_hemisp_narrowband_filter6` | Value is less than the fail_min. | 2140 | 49.537 |
| `hemisp_narrowband_filter6` | Value is less than the fail_min. | 2136 | 49.4444 |
| `diffuse_hemisp_narrowband_filter7` | Value is less than the fail_min. | 2111 | 48.8657 |
| `hemisp_narrowband_filter7` | Value is less than the fail_min. | 2106 | 48.75 |
| `hemisp_narrowband_filter2` | Value is less than the fail_min. | 1972 | 45.6481 |
| `hemisp_narrowband_filter5` | Value is less than the fail_min. | 1836 | 42.5 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpmfrsr7nchC1.b1", "19961021", "20260923")
```

The handbook's own note on data quality: Near-real-time data plots can be accessed via the ARM Data Quality Health and Status (DQ HandS) plot browser. Current data quality health and status results, including tables and graphs used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality, are available at the DQ HandS link (http://dq.arm.gov/). An Instrument Mentor Monthly Summary is also produced.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Direct irradiance is not a primary measurement | Direct beam values are calculated (derived) from diffuse and global measurements rather than measured directly; users may mistakenly treat MFRSR as a sun photometer | Recognize MFRSR derives direct beam from total and diffuse measurements; use NIMFR if a true sun-photometer direct measurement is needed | (hb p. 16) |
| Shadowband obscuration of sky requiring side-band correction | Sun-blocked measurement includes loss of sky signal from the portion of sky blocked by the shadowband; corrected using average of first and second side-band measurements | Use first and second side-band measurements to correct the sun-blocked measurement (Dif = blk + [th-(fsb+ssb)/2]) | (hb p. 10) |
| Shading issues from coarse motor stepping | If the shadowband is adjusted right after or just before it moves to a new position, a shading issue can occur in the morning or afternoon, visible as anomalous readings at those times | Finer stepping (one-eighth step, 0.225 degrees) with new Campbell motor controller would largely eliminate the issue; not yet implemented network-wide | (hb p. 8) |
| Bang-on/bang-off heater electromagnetic interference (older logger) | Head temperature shows a 'saw tooth' trace, and heater on/off cycling near irradiance measurement times can produce EMF interference in the irradiance signal | Original logger prioritizes irradiance measurements by stopping the heater during a measurement; new logging system uses proportional heating,... | (hb p. 13) |
| 940 nm channel cannot be Langley-calibrated | The 940 nm (water vapor) channel data lack the more accurate Langley calibration applied to other channels because of highly variable atmospheric water vapor | Each head is returned annually to the SGP calibration facility for lamp calibration of this channel | (hb p. 19) |
| Sensor offset bias | Total and diffuse irradiance channels show a bias/offset that varies with time if uncorrected | Nighttime data are averaged to produce an offset correction for the following day, applied on an ongoing basis rather than relying on a single... | (hb p. 17) |
| Cosine response error | Instrument has a varying response to incident irradiance depending on the solar disc's direction/angle, causing errors in direct and diffuse irradiance if uncorrected | Cosine correction determined in the laboratory with a cosine bench (measured at 1° intervals -90° to 90° in both south-north and west-east... | (hb p. 16) |
| Diffuse cosine correction approximation | Diffuse irradiance cosine effect is approximated using an isotropic/Rayleigh sky model rather than actual sky conditions | Handbook notes the isotropic-sky-based correction is within about one percent of actual sky conditions and considered small enough not to warrant... | (hb p. 17) |
| Site obstructions casting shadows | Anomalous dips in global/diffuse irradiance at specific times of day caused by trees, buildings, or other obstructions near the site | Site should ideally have no obstructions that cast a shadow over the instrument at any time during the day; a compromise siting location is usually... | (hb p. 12) |
| Instrument logger power loss requiring re-initialization (older logger) | Data gaps after a power outage because the original logger must be manually re-initialized locally or remotely | New CR1000-based logging system holds the program in non-volatile memory and resumes automatically once power is restored | (hb p. 12) |
| Diffuser contamination | Degraded/attenuated irradiance readings from a dirty Spectralon diffuser | Regular cleaning of the diffuser, as frequently as reasonably possible (daily to biweekly depending on site) | (hb p. 19) |
| Decommissioned/missing network stations | Data gaps at certain SGP extended facility locations after 2009-2010 shutdowns; some sites intended to have an MFRSR did not have a functioning unit for a period | Network was refurbished and restored to full capacity by end of 2008 at SGP; closed stations planned to be re-established closer to the Central... | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Standard lamp calibration (nominal calibration, .b1 data), cosine response determination on a cosine bench, and spectral response (filter function) mapping performed at the SGP calibration facility before deployment; once deployed with sufficient data, Langley calibration is performed (.c1 data), considered superior... (hb p. 18) |
| Calibration interval | Each head returned to the SGP calibration facility annually for lamp (and cosine/spectral) calibration; Langley calibration performed once enough field data are collected (hb p. 18) |
| Traceability | SGP calibration facility lamp standard and cosine bench measurements at 1° intervals between -90° and 90° in south-north and west-east directions (hb p. 18) |
| Routine maintenance | Cleaning the Spectralon diffuser; checking/replacing desiccant in heads with desiccant holders (hb p. 19) |
| Maintenance interval | Diffuser cleaned from once daily to once every two weeks depending on site; desiccant checked monthly and replaced as necessary (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Normal Incidence Multifilter Radiometer (NIMFR), Multifilter Radiometer (MFR).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `blk` | sun-blocked measurement |
| `cordif` | cosine-corrected diffuse measurement |
| `cordirhor` | cosine-corrected direct horizontal |
| `corth` | corrected total horizontal calculated using cordirhor and cordif |
| `dif` | sideband-corrected sun-blocked measurement |
| `dirhor` | vertical component of the direct beam on a horizontal surface |
| `fsb` | first side-band |
| `ssb` | second side-band |
| `th` | total horizontal |
| `MFR` | Multifilter Radiometer |
| `MFRSR` | Multifilter Rotating Shadowband Radiometer |
| `NIMFR` | Normal Incidence Multifilter Radiometer |
| `CF` | Central Facility |
| `AMF` | ARM Mobile Facility |


### References the handbook cites

- Harrison, L, J Michalsky, and J Berndt. 1994. "Automated multifilter rotating shadow-band radiometer: An instrument for optical depth and radiation measurements." Applied Optics 33(22):5118-5125,...
- Harrison, L, and J Michalsky. 1994. "Objective algorithms for the retrieval of optical depths from ground-based measurements." Applied Optics 33(22):5126-5132, doi:10.1364/AO.33.005126.
- Michalsky, JJ, JC Liljegren, and LC Harrison. 1995. "A comparison of sun photometer derivations of total column water vapor and ozone to standard measures of same at the Southern Great Plains Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf (21 pages, DOE/SC-ARM-TR-144, by GB Hodges, JJ Michalsky)
- Catalog record: ARM data-source index, `instrument_class_code=mfrsr`, read 2026-09-23
- Example file: `sgpmfrsr7nchC1.b1.20260922.070000.nc` from `sgpmfrsr7nchC1.b1`, 2.1 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
