---
name: arm-instrument-smps-air
description: ARM Scanning mobility particle sizer aboard aircraft (smps-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Particle concentration range), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (coraafsmpsF1.b1) and the variable inventory of a real file. Use when working with smps-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - smps-air, Scanning mobility particle sizer aboard aircraft, coraafsmpsF1.b1, Particle concentration range, Aerosols, Airborne Observations, Brechtel, mSEMS (Manual ver. 83-00031-01), aMCPC, mSEMS, SMPS.
---

# SMPS-AIR - Scanning mobility particle sizer aboard aircraft

The mSEMS measures aerosol particle size distributions (5-375 nm) aboard aircraft using scanning electrical mobility sizing combined with a condensation particle counter to detect and count size-classified particles.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `smps-air` |
| Handbook | [DOE/SC-ARM-TR-310 / F Mei / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Brechtel, mSEMS (Manual ver. 83-00031-01) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution |
| Record | 2018-11-04 to 2018-12-08 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | cor |
| ARM page | https://www.arm.gov/capabilities/instruments/smps-air |


## Credit

Everything this skill knows about the instrument is the work of **F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> F Mei. *Miniaturized Scanning Electrical Mobility Sizer (mSEMS) Instrument Handbook – Airborne Version*, DOE/SC-ARM-TR-310, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `msems-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `smps-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The mSEMS operates on the principle of using electrical mobility to measure and characterize aerosol particles. A monodisperse aerosol is generated through a differential mobility analyzer (DMA), where charged particles are introduced into an electric field within the mSEMS cylindrical chamber, inducing characteristic velocities (electrical mobility) that cause particles to separate based on size. The DMA systematically varies voltage, scanning through different particle sizes and measuring their corresponding electrical mobility. A particle counter (an advanced mixing condensation particle counter, aMCPC) then detects and counts the separated particles, enabling construction of a detailed particle size distribution, which is analyzed to provide insights into aerosol concentration at various size ranges.

**Sampling.** native rate READINGS file records all settings and readings every second; reported every SCAN results file written at the end of each scan (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Selectable particle diameter size range | nm | 5-375 nm | - | Variable (10:1 typical),... | (hb p. 7) |
| Particle concentration range (with aMCPC) | /cc | 1 - 10^7 /cc | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Selectable particle diameter size range | 5-375 nm | (hb p. 7) |
| Size resolution (set by Qaer/Qsheath) | Variable (10:1 typical) | (hb p. 7) |
| Scan time range | 5 secs to several mins | (hb p. 7) |
| Sheath flow range | 2-3 lpm | (hb p. 7) |
| Aerosol sample flow range | 0.1-0.76 lpm | (hb p. 7) |
| Particle concentration range with aMCPC | 1- 10^7 /cc | (hb p. 7) |
| Range of high voltage | 0-3,000 Volts | (hb p. 7) |
| Communications | RS-232 | (hb p. 7) |
| aMCPC butanol use | 1.9 ml/hr | (hb p. 7) |
| Operating temperature | -20-35°C | (hb p. 7) |
| Operating Pressure (unpressurized cabin) | 300-1,000 mb | (hb p. 7) |
| Physical size mSEMS Sizer | 18x13x10 cm | (hb p. 7) |
| Physical size aMCPC | 18x12x13 cm | (hb p. 7) |
| Weight mSEMS Sizer | 1.55 kg | (hb p. 7) |
| Weight aMCPC | 1.80 kg | (hb p. 7) |
| Power usage mSEMS Sizer | 9 Watts avg; 13 Watts peak | (hb p. 7) |
| Power usage aMCPC | 40 Watts avg; 90 Watts peak (at startup) | (hb p. 7) |
| Voltage input range | 10-14 VDC | (hb p. 7) |


## The data

Verified example: **`coraafsmpsF1.b1`**, file `coraafsmpsF1.b1.20181205.000000.txt.tar`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

**Reading note.** this datastream serves a gzipped tar containing one CSV (aaf.smps.g1.cacti.20181205.b1.txt), not netCDF; columns recorded instead of netCDF variables.

|  |  |
|---|---|
| Dimensions | `rows`=193 |
| Data variables | 19 |
| QC variables | 0 (`qc_` companions) |
| Median time step | n/a |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Dp_100_nm` | - | rows | - | - |
| `Dp_122_nm` | - | rows | - | - |
| `Dp_147_nm` | - | rows | - | - |
| `Dp_15_nm` | - | rows | - | - |
| `Dp_178_nm` | - | rows | - | - |
| `Dp_18_nm` | - | rows | - | - |
| `Dp_215_nm` | - | rows | - | - |
| `Dp_22_nm` | - | rows | - | - |
| `Dp_27_nm` | - | rows | - | - |
| `Dp_32_nm` | - | rows | - | - |
| `Dp_39_nm` | - | rows | - | - |
| `Dp_47_nm` | - | rows | - | - |
| `Dp_57_nm` | - | rows | - | - |
| `Dp_69_nm` | - | rows | - | - |
| `Dp_83_nm` | - | rows | - | - |
| `N` | - | rows | - | - |
| `QA_Flag` | - | rows | - | - |
| `Scan_end_time` | - | rows | - | - |
| `Scan_start_time` | - | rows | - | - |


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
files = act.discovery.download_arm_data(user, token, "coraafsmpsF1.b1", start, end)

# These files are gzip-compressed text (magic 1f 8b), not netCDF - `read_arm_netcdf` fails with
# "did not find a match in any of xarray's currently installed IO backends".
import gzip
with gzip.open(files[0], "rt") as fh:
    print(fh.readline())   # inspect the header, then parse with pandas
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("coraafsmpsF1.b1", "20181104", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality of SMPS measurements is generally high due to high-resolution particle size distribution information, but calibration, particle charging efficiency, and particle shape assumptions can introduce uncertainties. A data quality report will be filed when the spherical particle shape assumption is expected to be invalid.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Instrument calibration drift / flow rate instability | Inaccurate sizing and counting of particles; shifts in measured size distribution | Calibrate the DMA flow and aMCPC flow before each field campaign, and perform regular checking during deployment | (hb p. 9) |
| Particle Charging Efficiency variation in DMA | Uncertainties in size measurement accuracy | Routinely compare charger performance with a standard instrument to minimize the impact | (hb p. 9) |
| Particle Shape (non-spherical particles) | SMPS assumes spherical particle shape for size calculations; non-spherical particles introduce uncertainties in derived size | A data quality report will be filed when the spherical particle shape assumption is expected to be invalid | (hb p. 9) |
| Data Inversion Algorithms | Choice and accuracy of inversion algorithm used to convert raw data into particle size distribution can influence final results, seen as differences in reported size distribution depending... | Researchers must be mindful of their impact on data quality | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrating the DMA flow and aMCPC flow (hb p. 9) |
| Calibration interval | Before each field campaign, with regular checking during deployment (hb p. 9) |
| Routine maintenance | The mSEMS column can be disassembled for cleaning: unscrew the bottom cap and remove it, unscrew the top cap and remove it, lift out the upper collet, disassemble each piece for cleaning. (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SMPS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `aMCPC` | advanced mixing condensation particle counter |
| `CPC` | condensation particle counter |
| `DMA` | differential mobility analyzer |
| `mSEMS` | miniaturized scanning electrical mobility sizer |
| `SMPS` | scanning mobility particle sizer |
| `UAV` | unmanned aerial vehicle |


### References the handbook cites

- Ku, BK, and P Kulkarni. 2012. "Evaluation of the Scanning Mobility Particle Sizer (SMPS) for measurement of atmospheric aerosol particles: Method development and field tests." Aerosol Science and Technology 46(5):...
- McMurry, PH. 2000. "A review of atmospheric aerosol measurements." Atmospheric Environment 34(12-14): 1959–1999
- Park, K, DB Kittelson, MR Zachariah, and PH McMurry. 2004. "Measurement of inherent material density of nanoparticle agglomerates." Journal of Nanoparticle Research 6: 267–272
- Stolzenburg, MR, and PH McMurry. 2008. "Equations Governing Single and Tandem DMA Configurations and a New Lognormal Approximation to the Transfer Function." Aerosol Science and Technology 42(6): 421–432
- Wang, J, DR Collins, DS Covert, and B Karcher. 2002. "Single particle measurement of atmospheric black carbon and other light-absorbing particles." Journal of Geophysical Research – Atmospheres 107(D21)
- Wiedensohler, A. 1998. "An approximation of the bipolar charge distribution for particles in the submicron size range." Journal of Aerosol Science 19(3): 387–389

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf (12 pages, DOE/SC-ARM-TR-310, by F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=smps-air`, read 2026-09-23
- Example file: `coraafsmpsF1.b1.20181205.000000.txt.tar` from `coraafsmpsF1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
