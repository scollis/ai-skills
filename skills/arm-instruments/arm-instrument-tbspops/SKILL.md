---
name: arm-instrument-tbspops
description: ARM Portable Optical Particle Spectrometer aboard Tethered Balloon System (tbspops) - handbook-derived instrument reference. Measurement principle, reported quantities (Detectable particle size range, Particle concentration accuracy, Sample flow rate, Operating temperature range, Laser wavelength), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbspopsC1.b1) and the variable inventory of a real file. Use when working with tbspops data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - tbspops, sgptbspopsC1.b1, Detectable particle size range, Particle concentration accuracy, Sample flow rate, Operating temperature range, Aerosols, Airborne Observations, Handix Portable Optical Particle Spectrometer (POPS), POPS.
---

# TBSPOPS - Portable Optical Particle Spectrometer aboard Tethered Balloon System

The Handix Portable Optical Particle Spectrometer (POPS) measures airborne aerosol number concentration and particle size distribution from 140 nm to 3 µm diameter once a second, flown on the ARM Tethered Balloon System (TBS) at different altitudes along with a diffusion dryer and an iMet radiosonde for co-located meteorological data.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbspops` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Handix Portable Optical Particle Spectrometer (POPS) |
| Primary measurements | Aerosol particle size distribution; Aerosol concentration |
| Record | 2018-07-24 to 2026-09-24 (active) |
| Datastreams with data | 10 across 6 sites |
| Sites | bnf, crg, guc, hou, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbspops |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbspops`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbsins`, `tbslws`, `tbsmet`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbspops` until checked against that document's own section for it.

## How it measures

The POPS optically detects and sizes individual airborne particles by drawing a sample flow (0.05-0.35 LPM) past a 405 nm laser, with light scattering from each particle used to classify it into one of several diameter size bins ranging from 140 nm to 3.0 µm. The instrument is operated with a diffusion dryer to remove ambient humidity effects on particle sizing. Multiple POPS units can be flown simultaneously at different altitudes on the same TBS flight to build a vertical profile of aerosol size distribution and number concentration. Output is reported once per second as size-resolved particle number distribution (dn_*) bins plus total particle number concentration.

**Siting.** Six POPS units are available; multiple POPS units may be operated on the same TBS flight at different altitudes to build vertical aerosol profiles. POPS are operated with a diffusion dryer. The tbspops datastream includes co-located variables from an iMet radiosonde attached to the POPS (altitude, gps-derived pressure, barometric pressure, latitude, longitude, relative humidity, air temperature corrected for solar radiation).

**Sampling.** native rate once a second (1 Hz); reported every 1 s (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Airborne aerosol number concentration and particle size... | - | 140 nm to 3 µm diameter | - | 1 s | (hb p. 10) |
| Detectable particle size range | µm/nm | 140 nm-3.0 µm | - | - | (hb p. 11) |
| Maximum particle concentration range with less than  10%... | #/cm3 | 1250 #/cm3 | - | - | (hb p. 11) |
| Particle concentration accuracy | % | less than  1000 #/cm3 at 0.1 LPM sample... | +/- 10 % | - | (hb p. 11) |
| Sample flow rate | LPM | 0.05-0.35 LPM | - | - | (hb p. 11) |
| Operating temperature range | °C | -40 °C to 35 °C | - | - | (hb p. 11) |
| Laser wavelength | nm | 405 nm | - | - | (hb p. 11) |
| Aerosol particle size distribution bins (tbspops) | dN (per bin) | dn_135_150, dn_150_170, dn_170_195,... | - | 1 s | (hb p. 19) |
| Total particle number concentration | - | - | - | 1 s | (hb p. 19) |


## Specifications

| parameter | value | source |
|---|---|---|
| Detectable particle size range | 140 nm-3.0 µm | (hb p. 11) |
| Maximum particle concentration range with less than  10%... | 1250 #/cm3 | (hb p. 11) |
| Particle concentration accuracy | +/- 10 % less than  1000 #/cm3 at 0.1 LPM sample flow rate | (hb p. 11) |
| Sample flow rate | 0.05-0.35 LPM | (hb p. 11) |
| Operating temperature range | -40 °C to 35 °C | (hb p. 11) |
| Laser wavelength | 405 nm | (hb p. 11) |


## The data

Verified example: **`sgptbspopsC1.b1`**, file `sgptbspopsC1.b1.20241111.170300.nc`
(1.66 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=13321, `num_pops`=1 |
| Data variables | 29 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-11-11T17:03:00 to 2024-11-11T20:45:00 |
| dod version | tbspops-b1-2.0 |
| process version | ingest-tbspops-1.3-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `gps_pressure` | hPa | time,num_pops | yes | GPS pressure from iMet sensor |
| `imet_pressure` | hPa | time,num_pops | yes | Pressure from iMet sensor |
| `imet_temperature` | degC | time,num_pops | yes | Temperature from iMet sensor |
| `relative_humidity` | % | time,num_pops | yes | Relative humidity from iMet sensor |
| `total_concentration` | 1/cm^3 | time,num_pops | yes | Total number concentration from POPS including anything less than 135... |
| `dn_135_150` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 135 nm to 150 nm |
| `dn_1380_1760` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 1380 nm to 1760 nm |
| `dn_150_170` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 150 nm to 170 nm |
| `dn_170_195` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 170 nm to 195 nm |
| `dn_1760_2550` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 1760 nm to 2550 nm |
| `dn_195_220` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 195 nm to 220 nm |
| `dn_220_260` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 220 nm to 260 nm |
| `dn_2550_3615` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 2550 nm to 3615 nm |
| `dn_260_335` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 260 nm to 335 nm |
| `dn_335_510` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 335 nm to 510 nm |
| `dn_510_705` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 510 nm to 705 nm |
| `dn_705_1380` | 1/cm^3 | time,num_pops | - | Aerosol number concentration between 705 nm to 1380 nm |
| `pressure` | hPa | time,num_pops | - | Pressure from POPS sensor |
| `temperature` | degC | time,num_pops | - | Temperature from POPS sensor |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgptbspopsC1.b1", "2024-11-11", "2024-11-11")
ds = armlive_open("sgptbspopsC1.b1", "2024-11-11", "2024-11-11", cleanup_qc=True)
```

## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
29 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgptbspopsC1.b1.20241111.170300.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `imet_temperature` | Value is equal to missing_value. | 131 | 0.9834 |
| `imet_pressure` | Value is equal to missing_value. | 131 | 0.9834 |
| `relative_humidity` | Value is equal to missing_value. | 131 | 0.9834 |
| `gps_pressure` | Value is equal to missing_value. | 131 | 0.9834 |
| `gps_pressure` | Value is greater than fail_max. | 3 | 0.0225 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgptbspopsC1.b1", "20180724", "20260924")
```

The handbook's own note on data quality: Each datastream includes quality control variables for each scientific variable. The tbspops, tbscpc, tbsimet, tbsimetxq2, and tbswind datastreams are time-synced and merged with surface-based ceilometer estimates of cloud base and boundary-layer height in the tbsmerged Value-Added Product.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Coincidence error at high particle concentrations | Reported particle number concentration undercounts or plateaus when actual concentrations approach or exceed 1250 #/cm3, since accuracy of +/- 10% is only guaranteed below 1000 #/cm3 at 0.1... | - | (hb p. 11) |
| Particle size blind range below 140 nm and above 3 µm | No particles are reported outside the 140 nm-3.0 µm detectable size range; aerosol modes outside this window (e.g., ultrafine less than 140 nm or coarse greater than 3 µm) will be absent... | Use TSI CPC 3007 (10 nm-greater than 1.0 µm) for smaller particles | (hb p. 11) |
| Humidity effects on particle sizing | Without drying, ambient relative humidity could swell hygroscopic particles and shift apparent size distribution | POPS are operated with a diffusion dryer | (hb p. 10) |
| Operating temperature range limit | Instrument performance/data validity may be affected outside -40 °C to 35 °C operating temperature range | - | (hb p. 11) |
| Sample flow rate dependency of accuracy | Stated +/- 10% accuracy applies specifically at 0.1 LPM sample flow rate and below 1000 #/cm3; accuracy at other flow rates within the 0.05-0.35 LPM range is not specified | - | (hb p. 11) |
| Daily flow rate and zero filter check requirement | Uncorrected drift in flow rate or non-zero baseline counts on a zero filter would bias reported concentrations if checks are skipped | Daily flow rate and zero filter checks during field campaigns | (hb p. 21) |
| tbsmerged integration relies on time-syncing multiple datastreams | Any misalignment in time-sync between tbspops and other merged streams (tbscpc, tbsimet, tbswind, ceilometer) could show as apparent lag/offset in tbsmerged aerosol-meteorology relationships | Full details of the tbsmerged Value-Added Product are available in Dexheimer et al. 2023 | (hb p. 18) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Instrument mentor calibration (hb p. 21) |
| Calibration interval | Prior to each campaign (hb p. 21) |
| Routine maintenance | POPS undergo daily flow rate and zero filter checks during field campaigns. (hb p. 21) |
| Maintenance interval | Daily during field campaigns; calibrated prior to each campaign (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: TSI CPC 3007, iMet Radiosonde, TBS wind sensor booms, tbsmerged Value-Added Product.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `POPS` | portable optical particle spectrometer |
| `TBS` | tethered balloon system |
| `IOP` | intensive operational period |
| `agl` | above ground level |
| `LPM` | liters per minute |


### References the handbook cites

- Mei, F, and M Pekour. 2020. Portable Optical Particle Spectrometer (POPS) Instrument Handbook. DOE/SC-ARM-TR-259, https://doi.org/10.2172/1725831
- Dexheimer, D, K Gaustad, F Mei, and D Zhang. 2023. Tethered Balloon System Merged Data (TBSMERGED) Value-added Product Report. DOE/SC-ARM-TR-286. https://doi.org/10.2172/1958999

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbspops`, read 2026-09-24
- Example file: `sgptbspopsC1.b1.20241111.170300.nc` from `sgptbspopsC1.b1`, 1.66 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
