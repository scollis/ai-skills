---
name: arm-instrument-msems
description: ARM Miniatured Scanning Electrical Mobility Sizer (msems) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfminiaosmsemsM1.a1) and the variable inventory of a real file. Use when working with msems data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - msems, Miniatured Scanning Electrical Mobility Sizer, bnfminiaosmsemsM1.a1, Aerosols, Brechtel, mSEMS Manual ver. 83-00031-01, aMCPC, mSEMS, SMPS.
---

# MSEMS - Miniatured Scanning Electrical Mobility Sizer

The mSEMS measures aerosol particle size distribution (5-375 nm) by scanning electrical mobility using a miniaturized DMA paired with an advanced mixing condensation particle counter (aMCPC), deployed as a compact standalone or airborne/UAV-mounted instrument.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `msems` |
| Handbook | [DOE/SC-ARM-TR-310 / F Mei / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Brechtel; mSEMS Manual ver. 83-00031-01 |
| Primary measurements | Aerosol particle size distribution; Aerosol concentration |
| Record | 2025-11-10 to 2026-09-24 (active) |
| Datastreams with data | 2 across 1 sites |
| Sites | bnf |
| ARM page | https://www.arm.gov/capabilities/instruments/msems |


## Credit

Everything this skill knows about the instrument is the work of **F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> F Mei. *Miniaturized Scanning Electrical Mobility Sizer (mSEMS) Instrument Handbook – Airborne Version*, DOE/SC-ARM-TR-310, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `msems`, ARM links no handbook to this class. The facts below come from the **ARM Aerial Facility (AAF) Miniaturized Scanning Electrical Mobility Sizer ** (`msems-air`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `msems` until checked against that document's own section for it.

## How it measures

The mSEMS operates on the principle of using electrical mobility to measure and characterize aerosol particles. Beginning with generation of a monodisperse aerosol through a differential mobility analyzer (DMA), charged particles are introduced into an electric field within the mSEMS cylindrical chamber. This electric field induces characteristic velocities, known as electrical mobility, causing particles to separate based on size. The DMA systematically varies voltage, scanning through different particle sizes and measuring their corresponding electrical mobility. A particle counter (an advanced mixing condensation particle counter, aMCPC) then detects and counts the separated particles, enabling construction of a detailed particle size distribution.

**Siting.** Controlled via a computer running the "unmanned aerial vehicle (UAV) reader" program; airborne version intended for UAV/tethered-platform deployment; operating pressure range specified for unpressurized cabin (300-1,000 mb) and operating temperature -20-35°C, relevant for airborne deployment.

**Sampling.** native rate READINGS file records all settings and readings every second; reported every SCAN results file written at the end of each scan; scan time range 5 secs to several mins (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Selectable particle diameter size range | nm | 5-375 nm | - | Variable (10:1 typical),... | (hb p. 7) |
| Particle concentration range with aMCPC | /cc | 1-10^7 /cc | - | - | (hb p. 7) |


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

Verified example: **`bnfminiaosmsemsM1.a1`**, file `bnfminiaosmsemsM1.a1.20260629.000002.nc`
(2.11 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1350, `bound`=2, `bin`=60 |
| Data variables | 31 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 64 s |
| File time span | 2026-06-29T00:00:02 to 2026-06-29T23:59:10 |
| dod version | miniaosmsems-a1-1.1 |
| process version | ingest-miniaosmsems-1.1-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `actual_max_diameter` | nm | time | - | Maximum diameter for each scan |
| `dN_dlogDp` | 1/cm^3 | time,bin | - | Number size distribution, electrical mobility diameter |
| `diameter_mobility` | nm | time,bin | - | Midpoint of geometric mean mobility diameter |
| `dlogDp` | 1 | time,bin | - | Relative width of bins |
| `max_scan_voltage` | V | time | - | Maximum scan voltage |
| `mcpc_condenser_temperature` | degC | time | - | Latest reading of the condenser temperature |
| `mcpc_errors` | 1 | time | - | Error codes for MCPC operation |
| `mcpc_sample_flow` | L/min | time | - | Latest reading of the instant sample flow rate |
| `mcpc_sample_flow_avg` | L/min | time | - | Average aerosol sample flow rate for MCPC |
| `mcpc_sample_flow_stdev` | L/min | time | - | Standard deviation of aerosol sample flow rate for MCPC |
| `mcpc_saturator_flow` | L/min | time | - | Latest reading of the saturator flow rate |
| `mcpc_saturator_temperature` | degC | time | - | Latest reading of the saturator temperature |
| `min_scan_voltage` | V | time | - | Minimum scan voltage |
| `msems_errors` | 1 | time | - | Error codes for mSEMS operation |
| `raw_bin_counts` | count | time,bin | - | Raw counts in each size bin |
| `sample_pressure_avg` | hPa | time | - | Average aerosol sample pressure |
| `sample_pressure_stdev` | hPa | time | - | Standard deviation of aerosol sample pressure |
| `sample_temperature_avg` | degC | time | - | Average sample temperature |
| `sample_temperature_stdev` | degC | time | - | Standard deviation of sample temperature |
| `scan_direction` | 1 | time | - | Aerosol sizing scan direction |
| `sheath_flow_avg` | L/min | time | - | Average sheath flow rate |
| `sheath_flow_stdev` | L/min | time | - | Standard deviation of sheath flow rate |
| `sheath_relative_humidity_avg` | % | time | - | Average relative humidity of the sheath flow air |
| `sheath_relative_humidity_stdev` | % | time | - | Standard deviation of the relative humidity of the sheath flow air |
| `time` | - | time | - | Time offset from midnight |
| `total_N_conc` | 1/cm^3 | time | - | Total number concentration from integrated size distribution |


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
                     params={"user": f"{user}:{token}", "ds": "bnfminiaosmsemsM1.a1",
                             "start": "2026-06-29", "end": "2026-06-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfminiaosmsemsM1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfminiaosmsemsM1.a1", "2026-06-29", "2026-06-29")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfminiaosmsemsM1.a1", "2026-06-29", "2026-06-29"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfminiaosmsemsM1.a1", "20251110", "20260924")
```

The handbook's own note on data quality: The handbook notes that data quality of SMPS measurements is generally high but subject to uncertainties from instrument calibration, particle charging efficiency, and particle shape assumptions. A data quality report will be filed when the spherical particle shape assumption is expected to be invalid.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Instrument calibration drift / unstable flow rates | Inaccurate sizing and counting of particles; shifts in sized distribution if sheath/sample flow rates are not stable | Calibrate the DMA flow and aMCPC flow before each field campaign, and perform regular checking during deployment | (hb p. 9) |
| Particle Charging Efficiency variability | Uncertainties in size measurements due to variations in charging efficiency within the DMA | Routinely compare charger performance with a standard instrument to minimize the impact | (hb p. 9) |
| Particle Shape assumption (non-spherical particles) | SMPS assumes spherical particle shape for size calculations; uncertainties arise for non-spherical particles | File a data quality report when the spherical particle shape assumption is expected to be invalid; additional characterization techniques may be... | (hb p. 9) |
| Data Inversion Algorithms | Choice and accuracy of inversion algorithm used to convert raw data into particle size distribution can influence final results | Researchers must be mindful of their impact on data quality | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrating the DMA flow and aMCPC flow (hb p. 9) |
| Calibration interval | Before each field campaign, with regular checking during deployment (hb p. 9) |
| Routine maintenance | mSEMS column can be disassembled for cleaning: unscrew the bottom cap and remove it; unscrew the top cap and remove it; lift out the upper collet; disassemble each piece for cleaning. (hb p. 9) |


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

- McMurry, PH. 2000. "A review of atmospheric aerosol measurements." Atmospheric Environment 34(12-14): 1959–1999
- Stolzenburg, MR, and PH McMurry. 2008. "Equations Governing Single and Tandem DMA Configurations and a New Lognormal Approximation to the Transfer Function." Aerosol Science and Technology 42(6): 421–432
- Wiedensohler, A. 1998. "An approximation of the bipolar charge distribution for particles in the submicron size range." Journal of Aerosol Science 19(3): 387–389
- Wang, J, DR Collins, DS Covert, and B Karcher. 2002. "Single particle measurement of atmospheric black carbon and other light-absorbing particles." Journal of Geophysical Research – Atmospheres 107(D21)
- Ku, BK, and P Kulkarni. 2012. "Evaluation of the Scanning Mobility Particle Sizer (SMPS) for measurement of atmospheric aerosol particles: Method development and field tests." Aerosol Science and Technology 46(5):...
- Park, K, DB Kittelson, MR Zachariah, and PH McMurry. 2004. "Measurement of inherent material density of nanoparticle agglomerates." Journal of Nanoparticle Research 6: 267–272

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf (12 pages, DOE/SC-ARM-TR-310, by F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=msems`, read 2026-09-24
- Example file: `bnfminiaosmsemsM1.a1.20260629.000002.nc` from `bnfminiaosmsemsM1.a1`, 2.11 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
