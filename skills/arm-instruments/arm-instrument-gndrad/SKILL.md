---
name: arm-instrument-gndrad
description: ARM Ground Radiometers on Stand for Upwelling Radiation (gndrad) - handbook-derived instrument reference. Measurement principle, reported quantities (Upwelling Shortwave, Upwelling Longwave), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpgndrad25m60sC1.b1) and the variable inventory of a real file. Use when working with gndrad data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - gndrad, Ground Radiometers on Stand for Upwelling Radiation, sgpgndrad25m60sC1.b1, Upwelling Shortwave, Upwelling Longwave, Radiometric, The Eppley Laboratory, CART, SIRS, ARCS, BORCAL.
---

# GNDRAD - Ground Radiometers on Stand for Upwelling Radiation

The GNDRAD collection of radiometers provides continuous 1-minute measurements of broadband upwelling shortwave (reflected solar) and longwave (terrestrial infrared) irradiance, mounted inverted above the ground at Atmospheric Radiation and Cloud Station (ARCS) sites to help determine total radiative energy exchange within the Tropical Western Pacific.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 13 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gndrad` |
| Handbook | [ARM TR-027 / T. Stoffel / November 2004](https://www.arm.gov/publications/tech_reports/handbooks/gndrad_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | The Eppley Laboratory, Inc. - Model PSP (precision spectral pyranometer) for shortwave; Model PIR (precision infrared radiometer) for longwave; data logger: Coastal Environmental Systems Model... |
| Primary measurements | Longwave broadband upwelling irradiance; Shortwave broadband total upwelling irradiance; Surface skin temperature |
| Record | 1996-10-09 to 2026-09-23 (active) |
| Datastreams with data | 82 across 30 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/gndrad |


## Credit

Everything this skill knows about the instrument is the work of **T. Stoffel** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> T. Stoffel. *Ground Radiation (GNDRAD) Handbook*, ARM TR-027, November 2004.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/gndrad_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Upwelling shortwave irradiance is measured by an inverted pyranometer (Eppley PSP) with a hemispheric (2π sr) field of view sensitive to 0.3-3.0 micrometer wavelengths, producing an output voltage via a thermoelectric, single-black detector under two Schott Glass hemisphere domes. Upwelling longwave irradiance is measured by an inverted pyrgeometer (Eppley PIR) with a hemispheric field of view sensitive to 4.0-50 micrometer wavelengths. Irradiance is derived from the instrument's output voltage divided by its responsivity (µV/W/sq m), with the pyrgeometer computation also incorporating thermopile voltage, case and dome temperatures, a calibration factor, a dome correction factor, and the Stefan-Boltzmann constant. Both radiometer types are mounted inverted without ventilation, 10 m above ground level, to view the surface.

**Siting.** Upwelling Shortwave (US) pyranometer is inverted, unventilated, and mounted 10 m above ground level; Upwelling Longwave (UIR) pyrgeometer is likewise inverted without ventilation. Both have hemispheric (2π sr) fields of view looking down at the surface. Deployed at North Slope of Alaska and Tropical Western Pacific ARCS sites as part of a network to determine total radiative energy exchange.

**Sampling.** reported every 1-minute data (hb p. 3).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Upwelling Shortwave (reflected) irradiance [US] | Wm-2 | 0.0 to 1100 Wm-2 (theoretical);... | ±6.0% or 15 Wm-2 (field); ±3.0% or 10 Wm-2... | - | (hb p. 4) |
| Upwelling Longwave (terrestrial) irradiance [UIR] | Wm-2 | 100 to 800 Wm-2 (theoretical);... | ±2.5% or 4 Wm-2 (field); ±2% or 2 Wm-2... | - | (hb p. 4) |


## Specifications

| parameter | value | source |
|---|---|---|
| Upwelling Shortwave - Radiometer Model | PSP | (hb p. 6) |
| Upwelling Shortwave - Mounting Arrangement | Inverted w/o ventilation | (hb p. 6) |
| Upwelling Shortwave - Typical Responsivity | 9.0 µV/Wm-2 | (hb p. 6) |
| Upwelling Shortwave - Typical Calibration Uncertainty | ±3.0% or 10 Wm-2 | (hb p. 6) |
| Upwelling Longwave - Radiometer Model | PIR | (hb p. 6) |
| Upwelling Longwave - Mounting Arrangement | Inverted w/o ventilation | (hb p. 6) |
| Upwelling Longwave - Typical Responsivity | 4.0 µV/Wm-2 | (hb p. 6) |
| Upwelling Longwave - Typical Calibration Uncertainty | ±2% or 2 Wm-2 | (hb p. 6) |
| Upwelling Shortwave [US] - Field of View | 2π sr | (hb p. 7) |
| Upwelling Shortwave [US] - Wavelength Range | 0.3 to 3.0 microns | (hb p. 7) |
| Upwelling Shortwave [US] - Minimum Irradiance | 0.0 Wm-2 | (hb p. 7) |
| Upwelling Shortwave [US] - Maximum Irradiance | 1100 Wm-2 | (hb p. 7) |
| Upwelling Longwave [UIR] - Field of View | 2π sr | (hb p. 7) |
| Upwelling Longwave [UIR] - Wavelength Range | 4.0 to 50 microns | (hb p. 7) |
| Upwelling Longwave [UIR] - Minimum Irradiance | 100 Wm-2 | (hb p. 7) |
| Upwelling Longwave [UIR] - Maximum Irradiance | 800 Wm-2 | (hb p. 7) |
| Data acquisition system | Coastal Environmental Systems Model ZENO-3200 Datalogger | (hb p. 7) |


## The data

Verified example: **`sgpgndrad25m60sC1.b1`**, file `sgpgndrad25m60sC1.b1.20260919.000000.nc`
(0.18 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 26 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 60 seconds |
| dod version | gndrad25m60s-b1-2.0 |
| process version | ingest-gndrad-1.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `up_long_hemisp` | W/m^2 | time | yes | Upwelling Longwave Hemispheric Irradiance, Pyrgeometer |
| `up_long_hemisp_max` | W/m^2 | time | yes | Upwelling Longwave Hemispheric Irradiance, Pyrgeometer, Maxima |
| `up_long_hemisp_min` | W/m^2 | time | yes | Upwelling Longwave Hemispheric Irradiance, Pyrgeometer, Minima |
| `up_long_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Upwelling Longwave Hemispheric Irradiance,... |
| `up_short_hemisp` | W/m^2 | time | yes | Upwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `up_short_hemisp_max` | W/m^2 | time | yes | Upwelling Shortwave Hemispheric Irradiance, Pyranometer, Maxima |
| `up_short_hemisp_min` | W/m^2 | time | yes | Upwelling Shortwave Hemispheric Irradiance, Pyranometer, Minima |
| `up_short_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Upwelling Shortwave Hemispheric... |
| `logger_temp` | degC | time | - | Logger temperature |
| `logger_volt` | V | time | - | Logger voltage |
| `time` | - | time | - | Time offset from midnight |
| `up_long_hemisp_std` | W/m^2 | time | - | Upwelling Longwave Hemispheric Irradiance, Pyrgeometer, Standard... |
| `up_short_hemisp_std` | W/m^2 | time | - | Upwelling Shortwave Hemispheric Irradiance, Pyranometer, Standard... |


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
                     params={"user": f"{user}:{token}", "ds": "sgpgndrad25m60sC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpgndrad25m60sC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpgndrad25m60sC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpgndrad25m60sC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("up_long_hemisp", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
26 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_up_long_hemisp"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("up_long_hemisp", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["up_long_hemisp", "up_short_hemisp", "up_long_hemisp_max"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpgndrad25m60sC1.b1", "19961009", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality is monitored via DQ HandS (Data Quality Health and Status) and NCVweb interactive plotting tools, which contain the techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality. All DQ Office and most Site Scientist checking techniques are incorporated within DQ HandS. Value-added procedures (VAPs) and Quality Measurement Experiments (QMEs) provide continuous assessment of input data quality based on internal consistency checks, comparisons between independent similar measurements, or comparisons with modeled results.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Thermal offsets in pyranometers | Non-zero output signal in absence of solar radiation; clear-sky nighttime thermal offsets producing as much as 30 Wm-2; daytime downwelling diffuse shortwave measurements also require... | ARM uses a correction method based on correlations with the net infrared and observed diffuse irradiances [Dutton, et al, 2001] | (hb p. 6) |
| Angular response characteristics of pyranometer (PSP) | Contributes major uncertainty to shortwave irradiance measurements, especially at varying solar zenith/azimuth angles | Determined and verified with calibration; responsivities and uncertainty provided within bins of solar zenith angles to help users understand... | (hb p. 7) |
| Limited angular response mapping during BORCAL calibration event | Uncertainty values are empirically derived only for the solar zenith/azimuth angles encountered during the calibration period, not the full possible range | Uncertainty quoted for composite responsivity is 'probably reasonable for general applications' since calibration period generally covers a... | (hb p. 9) |
| General measurement uncertainty not fully characterized | Estimating radiometer measurement uncertainties remains 'a topic for additional research'; uncertainty values in Table 1 are conservative estimates | - | (hb p. 4) |
| Field measurement uncertainty larger than calibration uncertainty | Field uncertainties (e.g., ±6.0% or 15 Wm-2 for US) exceed pure calibration uncertainties (±3.0% or 10 Wm-2) due to added installation, operation, and maintenance factors | - | (hb p. 4) |
| Spectral response nominal values vary by instrument model | Precise spectral response differs unit-to-unit even though nominal values are listed | - | (hb p. 6) |
| Minimum irradiance floor for longwave measurements | UIR measurement range has a nonzero minimum of 100 Wm-2 (theoretical), unlike shortwave which can read down to 0.0 Wm-2 | - | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Component Summation Method (modified shading method per ASTM E913-82) using Broadband Outdoor Radiometer CALibration (BORCAL) at the SGP Radiometer Calibration Facility (RCF); pyrgeometers calibrated via Pyrgeometer Blackbody Calibration System developed by Eppley Laboratory and/or outdoor comparisons with transfer... (hb p. 7) |
| Calibration interval | Radiometers are re-calibrated annually (hb p. 7) |
| Traceability | Shortwave: traceable to World Radiometric Reference (WRR) maintained by World Radiation Center (WRC) for WMO, via NREL absolute cavity radiometer reference standards, maintained through International Pyrheliometer Comparisons (IPC) held every five years (IPC-IX completed October 2000). Longwave: traceable to... (hb p. 7) |
| Routine maintenance | Radiometers re-calibrated annually; 100% spares inventory maintained to reduce station downtime during calibration; maintenance performed during maintenance visits to ARCS facilities (hb p. 12) |
| Maintenance interval | Annual recalibration (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SKYRAD.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `US` | Upwelling Shortwave (reflected solar) Irradiance |
| `UIR` | Upwelling Infrared/Longwave (terrestrial) Irradiance |
| `DNI` | Direct Normal (beam) Irradiance |
| `DD` | Diffuse Horizontal (sky) Irradiance |
| `DS` | Downwelling Shortwave (global) Irradiance |
| `DIR` | Downwelling Longwave (atmospheric) Irradiance |
| `CART` | Cloud and Radiation Testbed |
| `NIP` | normal incidence pyrheliometer |
| `PIR` | precision infrared radiometer |
| `PSP` | precision spectral pyranometer |
| `SIRS` | Solar Infrared Station |
| `ARCS` | Atmospheric Radiation and Cloud Station |
| `BORCAL` | Broadband Outdoor Radiometer CALibration |
| `RCF` | Radiometer Calibration Facility |


### References the handbook cites

- Iqbal, M. 1983. An Introduction to Solar Radiation. Academic Press, New York, New York. ISBN 0-12-373750-8.
- Maxwell, E.L, and D.R. Myers. 1992. Daily Estimates of Aerosol Optical Depth for Solar Radiation Models. Solar '92, Proceedings of 1992 Annual Conference of the American Solar Energy Society, p.323.
- Reda, I. 1999. Improving the Shade/Unshade Method to Calculate the Responsivities of Solar Pyranometers. NREL/TR-26483 (June 1999).
- Dutton, et al, 2001 (thermal offset correction method)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/gndrad_handbook.pdf (13 pages, ARM TR-027, by T. Stoffel)
- Catalog record: ARM data-source index, `instrument_class_code=gndrad`, read 2026-09-23
- Example file: `sgpgndrad25m60sC1.b1.20260919.000000.nc` from `sgpgndrad25m60sC1.b1`, 0.18 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
