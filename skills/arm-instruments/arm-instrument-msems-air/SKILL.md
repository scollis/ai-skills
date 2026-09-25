---
name: arm-instrument-msems-air
description: ARM ARM Aerial Facility (AAF) Miniaturized Scanning Electrical Mobility Sizer (msems-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Particle concentration), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafmsemsU2.b1) and the variable inventory of a real file. Use when working with msems-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - msems-air, bnfaafmsemsU2.b1, Particle concentration, Aerosols, Airborne Observations, Brechtel mSEMS (Manual ver. 83-00031-01), aMCPC, mSEMS, SMPS.
---

# MSEMS-AIR - ARM Aerial Facility (AAF) Miniaturized Scanning Electrical Mobility Sizer 

The mSEMS is an airborne instrument that uses scanning electrical mobility sizing with a DMA and an advanced mixing condensation particle counter (aMCPC) to measure aerosol particle size distributions and concentrations from aircraft or UAV platforms.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `msems-air` |
| Handbook | [DOE/SC-ARM-TR-310 / F Mei / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Brechtel mSEMS (Manual ver. 83-00031-01) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution |
| Record | 2023-06-15 to 2025-06-20 (retired) |
| Datastreams with data | 4 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/msems-air |


## Credit

Everything this skill knows about the instrument is the work of **F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> F Mei. *Miniaturized Scanning Electrical Mobility Sizer (mSEMS) Instrument Handbook – Airborne Version*, DOE/SC-ARM-TR-310, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `smps-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `msems-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The mSEMS operates on the principle of using electrical mobility to measure and characterize aerosol particles. A monodisperse aerosol is generated through a differential mobility analyzer (DMA), where charged particles are introduced into an electric field within the mSEMS cylindrical chamber, inducing characteristic velocities (electrical mobility) that cause particles to separate based on size. The DMA systematically varies voltage, scanning through different particle sizes and measuring their corresponding electrical mobility. An advanced mixing condensation particle counter (aMCPC) then detects and counts the separated particles, enabling construction of a detailed particle size distribution. The collected data is analyzed to provide insights into aerosol concentration at various size ranges.

**Sampling.** native rate Records settings and readings every second in the READINGS file; reported every SCAN results file written at the end of each scan; scan time range 5 secs to several mins (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle size distribution / diameter | nm | 5-375 nm | - | Variable (10:1 typical),... | (hb p. 7) |
| Particle concentration (with aMCPC) | /cc | 1-10^7 /cc | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Selectable particle diameter size range | 5-375 nm | (hb p. 7) |
| Size resolution (set by Qaer/Qsheath) | Variable (10:1 typical) | (hb p. 7) |
| Scan time range | 5 secs to several mins | (hb p. 7) |
| Sheath flow range | 2-3 lpm | (hb p. 7) |
| Aerosol sample flow range | 0.1-0.76 lpm | (hb p. 7) |
| Particle concentration range with aMCPC | 1-10^7 /cc | (hb p. 7) |
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

Verified example: **`bnfaafmsemsU2.b1`**, file `bnfaafmsemsU2.b1.20250610.162539.nc`
(0.6 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=823, `electrical_mobility_diameter`=48, `bound`=2 |
| Data variables | 34 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 15 s |
| File time span | 2025-06-10T16:25:39 to 2025-06-10T19:57:19 |
| dod version | aafmsems-b1-1.0 |
| process version | ingest-aafmsemscorr-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `size_distribution` | cm^-3 | time,electrical_mobility_diameter | yes | Particle size distribution in dNdlogDp |
| `total_number_concentration` | 1/cm^3 | time | yes | Total number concentration |
| `actual_max_diameter` | nm | time | - | Maximum diameter for each scan |
| `dlogDp` | 1 | electrical_mobility_diameter | - | Relative width of bins |
| `electrical_mobility_diameter` | nm | electrical_mobility_diameter | - | Aerosol electrical mobility diameter |
| `max_scan_voltage` | V | time | - | Maximum scan voltage |
| `mcpc_condenser_temperature` | degC | time | - | Latest reading of the condenser temperature |
| `mcpc_sample_flow` | L/min | time | - | Latest reading of the instant sample flow rate |
| `mcpc_sample_flow_avg` | L/min | time | - | Average aerosol sample flow rate for MCPC |
| `mcpc_sample_flow_stdev` | L/min | time | - | Standard deviation of aerosol sample flow rate for MCPC |
| `mcpc_saturator_flow` | L/min | time | - | Latest reading of the saturator flow rate |
| `mcpc_saturator_temperature` | degC | time | - | Latest reading of the saturator temperature |
| `min_scan_voltage` | V | time | - | Minimum scan voltage |
| `msems_errors` | 1 | time | - | Error codes for mSEMS operation |
| `raw_bin_counts` | count | time,electrical_mobility_diameter | - | Raw counts in each size bin |
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
                     params={"user": f"{user}:{token}", "ds": "bnfaafmsemsU2.b1",
                             "start": "2025-06-10", "end": "2025-06-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaafmsemsU2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaafmsemsU2.b1", "2025-06-10", "2025-06-10")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaafmsemsU2.b1", "2025-06-10", "2025-06-10"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("scan_direction")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
34 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_size_distribution"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("size_distribution", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["size_distribution", "total_number_concentration", "lat"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (bnfaafmsemsU2.b1.20250610.162539.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `lat` | Value is equal to missing_value. | 4 | 0.486 |
| `lon` | Value is equal to missing_value. | 4 | 0.486 |
| `alt` | Value is equal to missing_value. | 4 | 0.486 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("bnfaafmsemsU2.b1", "20230615", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality is generally high due to high-resolution particle size distribution capability, but calibration, particle charging efficiency, and particle shape assumptions (spherical) contribute to uncertainties. Calibration of DMA and aMCPC flows is recommended before each field campaign with regular checks during deployment. A data quality report will be filed when the spherical particle shape assumption is expected to be invalid.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Instrument calibration drift / flow rate instability | Inaccurate sizing and counting of particles; shifts in reported particle size distribution | Calibrate the DMA flow and aMCPC flow before each field campaign, and perform regular checking during deployment | (hb p. 9) |
| Particle Charging Efficiency variations | Uncertainties in size measurement accuracy, apparent as discrepancies against a standard instrument | Routinely compare the charger performance with a standard instrument to minimize the impact | (hb p. 9) |
| Particle Shape (non-spherical particles) | Sizing uncertainties since SMPS assumes spherical particle shape for size calculations | A data quality report will be filed when the spherical particle shape assumption is expected to be invalid | (hb p. 9) |
| Data Inversion Algorithms | Final particle size distribution results can vary depending on the choice and accuracy of the inversion algorithm used to convert raw data | Researchers must be mindful of the impact of algorithm choice on data quality | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrating the DMA flow and aMCPC flow (hb p. 9) |
| Calibration interval | Before each field campaign, with regular checking during deployment (hb p. 9) |
| Routine maintenance | Disassemble the mSEMS column for cleaning: unscrew and remove bottom cap, unscrew and remove top cap, lift out the upper collet, disassemble each piece for cleaning (hb p. 9) |


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

- McMurry, PH. 2000. "A review of atmospheric aerosol measurements." Atmospheric Environment 34(12-14): 1959-1999
- Stolzenburg, MR, and PH McMurry. 2008. "Equations Governing Single and Tandem DMA Configurations and a New Lognormal Approximation to the Transfer Function." Aerosol Science and Technology 42(6): 421-432
- Wiedensohler, A. 1998. "An approximation of the bipolar charge distribution for particles in the submicron size range." Journal of Aerosol Science 19(3): 387-389
- Wang, J, DR Collins, DS Covert, and B Karcher. 2002. "Single particle measurement of atmospheric black carbon and other light-absorbing particles." Journal of Geophysical Research - Atmospheres 107(D21)
- Ku, BK, and P Kulkarni. 2012. "Evaluation of the Scanning Mobility Particle Sizer (SMPS) for measurement of atmospheric aerosol particles: Method development and field tests." Aerosol Science and Technology 46(5):...
- Park, K, DB Kittelson, MR Zachariah, and PH McMurry. 2004. "Measurement of inherent material density of nanoparticle agglomerates." Journal of Nanoparticle Research 6: 267-272

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-310.pdf (12 pages, DOE/SC-ARM-TR-310, by F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=msems-air`, read 2026-09-23
- Example file: `bnfaafmsemsU2.b1.20250610.162539.nc` from `bnfaafmsemsU2.b1`, 0.6 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
