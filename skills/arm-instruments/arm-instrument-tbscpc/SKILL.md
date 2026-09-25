---
name: arm-instrument-tbscpc
description: ARM Condensation Particle Counter aboard Tethered Balloon System (tbscpc) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbscpcC1.b1) and the variable inventory of a real file. Use when working with tbscpc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - tbscpc, sgptbscpcC1.b1, Aerosols, Airborne Observations, TSI Condensation Particle Counter (CPC) 3007, iMet, POPS.
---

# TBSCPC - Condensation Particle Counter aboard Tethered Balloon System

The TSI CPC 3007 (tbscpc) measures total airborne aerosol number concentration from 10 nm to greater than 1 µm diameter once per second, flown on the ARM Tethered Balloon System at various altitudes together with a diffusion dryer and a co-located iMet radiosonde.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbscpc` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | TSI Condensation Particle Counter (CPC) 3007 |
| Primary measurements | Aerosol concentration |
| Record | 2018-07-24 to 2026-09-24 (active) |
| Datastreams with data | 11 across 6 sites |
| Sites | bnf, crg, guc, hou, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbscpc |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbscpc`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbsdts`, `tbsground`, `tbsins`, `tbslws`, `tbsmet`, `tbspops`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbscpc` until checked against that document's own section for it.

## How it measures

The CPC instruments are used to measure airborne aerosol number concentration from 10 nm to greater than 1 µm diameter once a second. Multiple CPC units may be operated on the same TBS flight at different altitudes to profile aerosol concentration vertically. CPCs are operated with a diffusion dryer to remove excess moisture from the sampled aerosol stream before detection. The instrument reports total number concentration of aerosol particles from 10 nm up to 1.0 µm in diameter every second as its primary output.

**Siting.** CPC units are flown aboard the TBS at variable altitudes below cloud base (typically 152 m below cloud base, up to 1.5 km agl maximum unless authorized otherwise); tether angle from zenith must not exceed 45° in flight. CPCs are operated with a diffusion dryer, and up to six CPC units are available, with multiple CPCs potentially operated on the same flight at different altitudes. The tbscpc datastream includes co-located data from an iMet radiosonde operating on the tether within one meter of the CPC (altitude, gps_pressure, imet_pressure, lat, lon, relative_humidity, temperature).

**Sampling.** native rate once per second (1 Hz); reported every 1 s; averaging none stated for tbscpc primary output; total number concentration reported every second (hb p. 14).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Airborne aerosol number concentration | #/cm3 | 10 nm - greater than  1.0 µm... | +/- 20% | 1 s | (hb p. 14) |
| Maximum particle concentration range with less than  10%... | #/cm3 | 100,000 #/cm3 | - | - | (hb p. 14) |


## Specifications

| parameter | value | source |
|---|---|---|
| Detectable particle size range | 10 nm - greater than  1.0 µm | (hb p. 14) |
| Maximum particle concentration range with less than  10%... | 100,000 #/cm3 | (hb p. 14) |
| Particle concentration accuracy | +/- 20% | (hb p. 14) |
| Sample flow rate - Detected aerosol | 100 cm3/min | (hb p. 14) |
| Sample flow rate - Inlet | 700 cm3/min | (hb p. 14) |
| Operating temperature range | 10 °C to 35 °C | (hb p. 14) |
| Laser | Class I | (hb p. 14) |


## The data

Verified example: **`sgptbscpcC1.b1`**, file `sgptbscpcC1.b1.20241111.170300.nc`
(0.91 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=13321, `num_cpc`=1 |
| Data variables | 15 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-11-11T17:03:00 to 2024-11-11T20:45:00 |
| dod version | tbscpc-b1-3.0 |
| process version | ingest-tbscpc-2.3-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `gps_pressure` | hPa | time,num_cpc | yes | GPS pressure from iMet sensor |
| `imet_pressure` | hPa | time,num_cpc | yes | Pressure from iMet sensor |
| `relative_humidity` | % | time,num_cpc | yes | Relative humidity from iMet sensor |
| `temperature` | degC | time,num_cpc | yes | Temperature from iMet sensor |
| `total_concentration` | 1/cm^3 | time,num_cpc | yes | Total number concentration from CPC for the aerosol particles larger... |
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
                     params={"user": f"{user}:{token}", "ds": "sgptbscpcC1.b1",
                             "start": "2024-11-11", "end": "2024-11-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptbscpcC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptbscpcC1.b1", "2024-11-11", "2024-11-11")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgptbscpcC1.b1", "2024-11-11", "2024-11-11"))   # cite what you pulled
```

## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
15 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_temperature"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("temperature", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["temperature", "relative_humidity", "imet_pressure"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgptbscpcC1.b1.20241111.170300.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `temperature` | Value is equal to missing_value. | 131 | 0.9834 |
| `relative_humidity` | Value is equal to missing_value. | 131 | 0.9834 |
| `imet_pressure` | Value is equal to missing_value. | 131 | 0.9834 |
| `gps_pressure` | Value is equal to missing_value. | 131 | 0.9834 |
| `gps_pressure` | Value is greater than fail_max. | 3 | 0.0225 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgptbscpcC1.b1", "20180724", "20260924")
```

The handbook's own note on data quality: Each datastream, including tbscpc, includes quality control variables for each scientific variable. The CPC undergoes daily flow rate and zero filter checks during field campaigns in addition to instrument-mentor calibration prior to each campaign.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Coincidence error at high particle concentrations | Reported number concentration undercounts or plateaus when true concentration approaches/exceeds 100,000 #/cm3, the level at which coincidence error exceeds 10% | Handbook notes maximum particle concentration range with less than 10% coincidence error is 100,000 #/cm3; no further correction described | (hb p. 14) |
| Lower size-detection limit / blind range below 10 nm | Particles smaller than 10 nm diameter are not counted, so ultrafine nucleation-mode particles below this cutoff are absent from tbscpc concentration totals | None stated | (hb p. 14) |
| Upper size range ambiguity (greater than 1.0 µm) | Particles above ~1.0 µm are still counted by the CPC as part of total number but are not size-resolved, unlike POPS which resolves size bins up to 3 µm | None stated; use tbspops for size-resolved data above 140 nm | (hb p. 14) |
| Particle concentration accuracy limited to +/- 20% | Reported concentrations may differ from true concentration by up to 20% | None stated beyond calibration prior to each campaign | (hb p. 14) |
| Operating temperature range limitation (10 °C to 35 °C) | CPC performance/data quality may be affected or instrument may not operate correctly outside 10-35 °C ambient/operating temperature, relevant for cold-altitude or Arctic TBS flights | Diffusion dryer used with CPC; no explicit cold-weather mitigation stated | (hb p. 14) |
| Moisture/humidity interference on aerosol sizing/counting | Without drying, high relative humidity could bias particle counts or sizing due to hygroscopic growth or condensation in sample line | CPCs are operated with a diffusion dryer | (hb p. 14) |
| Co-located iMet radiosonde measurement offset from CPC inlet | Temperature, pressure, humidity, and position variables in tbscpc are from an iMet radiosonde within one meter of the CPC, not measured at the exact CPC inlet location, introducing a small... | None stated beyond noting the iMet is within one meter of the CPC | (hb p. 26) |
| Flight envelope constraints affecting profiling coverage | Data gaps or altitude limits in tbscpc profiles corresponding to flight rules: generally 152 m below cloud base, max altitude 1.5 km agl unless authorized, tether angle limited to less than... | In-cloud flights conducted within Restricted Airspace when authorized | (hb p. 9) |
| Only tbsground is continuous; tbscpc data only exist during flights | tbscpc records have temporal gaps corresponding to non-flight periods, unlike tbsground which is continuous | None stated | (hb p. 26) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Instrument mentor calibration (hb p. 29) |
| Calibration interval | Prior to each campaign (hb p. 29) |
| Traceability | Instrument mentor; additionally daily flow rate and zero filter checks during field campaigns (hb p. 29) |
| Routine maintenance | Daily flow rate and zero filter checks during field campaigns (hb p. 29) |
| Maintenance interval | Daily during field campaigns; calibration prior to each campaign (hb p. 29) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Handix Portable Optical Particle Spectrometer (POPS), interMet (iMet) Radiosonde, interMet (iMet) XQ2 Sensor, TBS ground station instruments (tbsground), tbsmerged Value-Added Product.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `CPC` | condensation particle counter |
| `TBS` | tethered balloon system |
| `agl` | above ground level |
| `iMet` | interMet radiosonde |
| `POPS` | portable optical particle spectrometer |
| `LPM` | liters per minute |
| `IOP` | intensive operational period |


### References the handbook cites

- Mei, F, and M Pekour. 2020. Portable Optical Particle Spectrometer (POPS) Instrument Handbook. DOE/SC-ARM-TR-259, https://doi.org/10.2172/1725831
- Dexheimer, D, K Gaustad, F Mei, and D Zhang. 2023. Tethered Balloon System Merged Data (TBSMERGED) Value-added Product Report. DOE/SC-ARM-TR-286. https://doi.org/10.2172/1958999

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbscpc`, read 2026-09-24
- Example file: `sgptbscpcC1.b1.20241111.170300.nc` from `sgptbscpcC1.b1`, 0.91 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
