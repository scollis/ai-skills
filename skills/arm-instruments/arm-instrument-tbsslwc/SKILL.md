---
name: arm-instrument-tbsslwc
description: ARM Supercooled Liquid Water Content Sondes aboard Tethered Balloon System (tbsslwc) - handbook-derived instrument reference. Measurement principle, reported quantities (Supercooled liquid water content), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (olitbsslwcM1.b1) and the variable inventory of a real file. Use when working with tbsslwc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Profiling; Cloud Properties. Triggers - tbsslwc, olitbsslwcM1.b1, Supercooled liquid water content, Airborne Observations, Atmospheric Profiling, Cloud Properties, Anasphere Supercooled Liquid Water Content (SLWC) Sonde, SLWC.
---

# TBSSLWC - Supercooled Liquid Water Content Sondes aboard Tethered Balloon System

The Anasphere SLWC sonde, flown on the ARM Tethered Balloon System only during in-cloud flights in restricted airspace, uses a vibrating wire to measure supercooled liquid water content approximately every three seconds.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbsslwc` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling; Cloud Properties |
| Manufacturer / model | Anasphere Supercooled Liquid Water Content (SLWC) Sonde |
| Primary measurements | Atmospheric pressure; Atmospheric temperature; Horizontal wind; Liquid water content; Navigation variables |
| Record | 2016-04-18 to 2020-11-20 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | oli |
| ARM page | https://www.arm.gov/capabilities/instruments/tbsslwc |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbsslwc`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbsins`, `tbslws`, `tbsmet`, `tbspops`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbsslwc` until checked against that document's own section for it.

## How it measures

Anasphere supercooled liquid water content (SLWC) sondes deploy a vibrating wire that is exposed to the cloud environment. As ice accretes on the wire in the presence of supercooled liquid water, the wire's vibration frequency depresses over time. This frequency depression is used to calculate the supercooled liquid water content, following the technique described in Serke et al. 2014 and Dexheimer et al. 2019, with measurements produced approximately every three seconds.

**Siting.** Anasphere SLWC sondes are deployed on the TBS tether only when operating inside of clouds during flights conducted within restricted airspace; not flown during standard out-of-cloud flights (which are otherwise generally conducted 152 m (500') below cloud base per platform-level TBS flight rules).

**Sampling.** reported every approximately every three seconds; averaging Not specified as averaged; each measurement represents a single vibrating-wire cycle (hb p. 20).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Supercooled liquid water content (SLWC) | g/m3 | - | +/- 0.01 g/m3 | 0.02 Hz (vibrating wire... | (hb p. 20) |


## Specifications

| parameter | value | source |
|---|---|---|
| Vibrating Wire Resolution (Hz) | 0.02 | (hb p. 20) |
| SLWC resolution (g/m3) | less than = .04 | (hb p. 20) |
| Accuracy (g/m3) | +/- 0.01 | (hb p. 20) |
| Measurement Time (s) | 3 | (hb p. 20) |


## The data

Verified example: **`olitbsslwcM1.b1`**, file `olitbsslwcM1.b1.20201113.082841.nc`
(0.84 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=5873, `num_slwc`=1 |
| Data variables | 30 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2020-11-13T08:28:41 to 2020-11-13T10:57:29 |
| dod version | tbsslwc-b1-2.0 |
| process version | ingest-tbsslwc-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `air_temperature` | degC | time,num_slwc | yes | Air temperature corrected for solar radiation |
| `imet_altitude` | km | time,num_slwc | yes | Altitude above mean sea level from iMet instrument |
| `pressure` | hPa | time,num_slwc | yes | Air pressure |
| `slwc` | g/m^3 | time,num_slwc | yes | Estimated supercooled liquid water content |
| `slwc_frequency` | Hz | time,num_slwc | yes | Frequency of the SLWC (Supercooled Liquid Water Content sonde) |
| `wind_speed` | m/s | time,num_slwc | yes | Wind speed |
| `air_density` | kg/m^3 | time,num_slwc | - | Air density |
| `deriv_smooth_slwc_frequency` | Hz/s | time,num_slwc | - | Derivative of smooth_slwc_frequency over time |
| `droplet_collection_efficiency` | 1 | time,num_slwc | - | Droplet collection efficiency |
| `droplet_diameter` | m | - | - | Estimate of median droplet diameter |
| `dynamic_air_viscosity` | Pa*s | time,num_slwc | - | Dynamic viscosity of the airstream |
| `imet_file_name` | 1 | num_slwc | - | iMet flle names |
| `inertia` | 1 | time,num_slwc | - | Langmuir inertia parameter (K) |
| `modified_inertia_param` | 1 | time,num_slwc | - | Modified inertia parameter (K0) |
| `reynolds_number` | 1 | time,num_slwc | - | Reynolds number |
| `smooth_slwc_frequency` | Hz | time,num_slwc | - | Smoothed slwc_frequency using LOESS |
| `time` | - | time | - | Time offset from midnight |
| `un_iced_slwc_frequency` | Hz | num_slwc | - | Un-iced wire frequency |
| `wire_diameter` | m | - | - | Wire diameter |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("olitbsslwcM1.b1", "2020-11-13", "2020-11-13")
ds = armlive_open("olitbsslwcM1.b1", "2020-11-13", "2020-11-13", cleanup_qc=True)
```

## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
30 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (olitbsslwcM1.b1.20201113.082841.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `slwc` | Value is equal to missing_value. | 5873 | 100.0 |
| `wind_speed` | Value is equal to missing_value. | 5873 | 100.0 |
| `lat` | Value is equal to missing_value. | 1225 | 20.8582 |
| `lon` | Value is equal to missing_value. | 1225 | 20.8582 |
| `imet_altitude` | Value is less than fail_min. | 500 | 8.5135 |
| `slwc_frequency` | Value is equal to missing_value. | 483 | 8.2241 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("olitbsslwcM1.b1", "20160418", "20260924")
```

The handbook's own note on data quality: Each datastream (implicitly including tbsslwc as part of the TBS data products) includes quality control variables for each scientific variable. The tbsmergedincloud product builds upon tbsmerged to incorporate the tbsslwc datastream, which estimates in-cloud supercooled liquid water content.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| SLWC sondes deployed only in-cloud/restricted airspace | tbsslwc datastream is only populated during specific in-cloud flight segments conducted within restricted airspace; data absent for out-of-cloud flights | Anasphere SLWC sondes are deployed on the TBS only when operating inside of clouds during flights in restricted airspace. | (hb p. 19) |
| Vibrating wire icing/deicing measurement cycle limits temporal resolution | SLWC values reported approximately every 3 seconds (measurement time), coarser than most other 1 Hz TBS sensors | - | (hb p. 20) |
| Coarse SLWC resolution near instrument floor | SLWC resolution stated as less than = .04 g/m3 with accuracy +/- 0.01 g/m3; values near or below this threshold may not be reliably distinguished from noise/zero | - | (hb p. 20) |
| Vibrating wire frequency depression principle requires ice accretion, implying a wire... | Frequency depression of the wire over time due to ice accreting on the wire in presence of supercooled liquid water is used to calculate SLWC; sudden resets or frequency jumps could occur... | - | (hb p. 19) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Not stated for SLWC sonde specifically; general TBS instrumentation calibrated per Table 15 (vendor or instrument mentor calibration for other instruments) (hb p. 29) |
| Calibration interval | Not separately listed for Anasphere SLWC sonde in Table 15 (TBS instrument calibration information); EMSL instruments and PUFIN are calibrated prior to each campaign by ARM TBS staff, but SLWC sonde specific calibration is not listed in the table (hb p. 29) |
| Routine maintenance | Not specifically detailed for the SLWC sonde in the maintenance plan section (Section 6); general TBS instrumentation maintenance covers balloons, winches, tethers, and instrumentation calibration checks (CPC/POPS flow checks, wind boom heading checks, iMet RH/temperature comparisons), but no SLWC-specific maintenance... (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Silixa XT DTS (distributed temperature sensing), Sensornet Oryx+ DTS-XR, iMet Radiosonde, tbsmerged Value-Added Product.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `SLWC` | supercooled liquid water content |
| `TBS` | tethered balloon system |
| `ARM` | Atmospheric Radiation Measurement |
| `INP` | ice nucleating particle |


### References the handbook cites

- Serke, D, E Hall, J Bognar, A Jordan, S Abdo, K Baker, T Seitel, M Nelson, A Reehorst, R Ware, F McDonough, and M Politovich. 2014. "Supercooled liquid water content profiling case studies with a new vibrating wire...
- Dexheimer, D, M Airey, E Roesler, CM Longbottom, K Nicoll, S Kneifel, F Mei, RG Harrison, G Marlton, and PD Williams. 2019. "Evaluation of ARM tethered-balloon system instrumentation for supercooled liquid water and...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbsslwc`, read 2026-09-24
- Example file: `olitbsslwcM1.b1.20201113.082841.nc` from `olitbsslwcM1.b1`, 0.84 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
