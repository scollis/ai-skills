---
name: arm-instrument-so2
description: ARM Sulfur Dioxide Monitor (so2) - handbook-derived instrument reference. Measurement principle, reported quantities (Sulfur dioxide), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaosso2M1.b1) and the variable inventory of a real file. Use when working with so2 data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Other. Triggers - so2, Sulfur Dioxide Monitor, bnfaosso2M1.b1, Sulfur dioxide, Other, referred to elsewhere as TEI Model 49i / Model 43i, DQPR/DQR, MAOS.
---

# SO2 - Sulfur Dioxide Monitor

The Sulfur Dioxide Analyzer (Thermo Fisher Model 43i-TLE trace level-enhanced pulsed fluorescence SO2 analyzer) continuously measures ambient sulfur dioxide mixing ratio in ppbv and is permanently installed in ARM AOS systems (AAF, MAOS-C, SGP AOS) sampling from a trace-gas manifold inlet.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 30 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `so2` |
| Handbook | [DOE/SC-ARM-TR-180 / SR Springston / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/so2_handbook.pdf) |
| Measurement category | Other |
| Manufacturer / model | Thermo Fisher Scientific Model 43i-TLE (trace level-enhanced pulsed fluorescence SO2 analyzer); referred to elsewhere as TEI Model 49i / Model 43i |
| Primary measurements | Sulfur Dioxide (SO2) Concentration |
| Record | 2012-06-24 to 2026-09-22 (active) |
| Datastreams with data | 39 across 9 sites |
| Sites | asi, bnf, crg, dst, epc, hou, mao, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/so2 |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston. *Sulfur Dioxide Monitor Instrument Handbook*, DOE/SC-ARM-TR-180, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/so2_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `so2-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `so2`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The instrument measures SO2 based on absorbance of UV light at one wavelength by SO2 molecules, which then decay to a lower energy state by emitting UV light at a longer wavelength (SO2 + hν1 → SO2* → SO2 + hν2). The emitted light is proportional to the concentration of SO2 in the optical cell. Sample air is drawn through a hydrocarbon "kicker" that removes hydrocarbons by permeation through the tube wall while SO2 passes unaffected, then flows into the fluorescence chamber where pulsating UV light excites SO2 molecules. A mirror assembly with eight selective mirrors reflects only wavelengths that excite SO2, and a bandpass filter allows only the emitted wavelengths from decaying SO2 molecules to reach the photomultiplier tube (PMT), which detects the UV emission. A photodetector continuously monitors the pulsating UV light source to compensate for fluctuations.

**Siting.** Trace-gas inlet used in AOS systems consists of high-flow 1/2" o.d. PFA tubing sampling from under the aerosol inlet rain hat at ~10-m AGL; air pulled into container at 30 LPM controlled by a rotometer and sum of instrument flow rates; residence time to back of instrument is ~1-2 s. Instrument permanently installed in shock-isolated 19" instrument rack in AOS systems (AAF, MAOS-C, SGP AOS).

**Sampling.** native rate ~1 Hz (nearly 1 Hz for primary signals); some housekeeping signals reported much less often; reported every 1-s monotonic time base in AOS output; Mentor QA/QC data also provided as 60-s running average; averaging 60-s running numerical average (arithmetic mean of present point and next 59 points) for Column 3 of Mentor QA/QC data; Avg Time normally set to 1 (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sulfur dioxide (SO2) mixing ratio | ppbv | extends well past conceivable ambient... | initial calibration within 1-2% accuracy; field... | ~1-s (jitter can yield 0,... | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | parts-per-billion (ppbv) | (hb p. 13) |
| Range | somewhat arbitrary; extends well past conceivable ambient levels in a non-power plant location | (hb p. 13) |
| Accuracy (initial, on receipt) | within 1-2% accuracy | (hb p. 13) |
| Accuracy (field variation) | ~5-10% variation from original measurement standard | (hb p. 13) |
| Repeatability (1-s, ambient) | [SO2] sigma = 1 ppbv | (hb p. 14) |
| Repeatability (60-s avg) | [SO2]60-s avg sigma = 0.15 ppbv | (hb p. 14) |
| 95% Confidence Interval (1-s) | ± 2 ppbv | (hb p. 14) |
| 95% Confidence Interval (60-s avg) | ± 0.3 ppbv | (hb p. 14) |
| Manufacturer zero noise (60-s avg) | 0.25 ppb RMS | (hb p. 14) |
| Sensitivity (lower detectable limit, 1 Hz) | 2 ppbv (95% confidence interval above baseline) | (hb p. 14) |
| Sensitivity (60-s avg, manufacturer LDL) | 0.1 ppb | (hb p. 14) |
| Sample flow (trace gas inlet) | ~0.5 SLPM (instrument); manifold pulled at 30 LPM | (hb p. 16) |
| Inlet residence time | ~1-2 s | (hb p. 16) |
| Flash lamp voltage replacement threshold | Values above ~1300 V indicate lamp replacement is needed | (hb p. 10) |
| Lamp intensity (normal) | normally about 90% | (hb p. 5) |
| Pump life | 2-3 years under continuous operation | (hb p. 13) |


## The data

Verified example: **`bnfaosso2M1.b1`**, file `bnfaosso2M1.b1.20260908.000000.nc`
(9.32 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86199 |
| Data variables | 27 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-08T00:00:00 to 2026-09-08T23:59:59 |
| sampling interval | 1 second |
| dod version | aosso2-b1-4.0 |
| process version | ingest-aosso2corr-2.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `so2` | ppbv | time | yes | Sulfur dioxide (SO2) mixing ratio |
| `auto_range` | 1 | time | - | Indicates which concentration is being used in Auto Range Mode |
| `averaging_time` | s | time | - | Instrument averaging time |
| `bench_pressure` | mmHg | time | - | Bench pressure |
| `bench_temp` | degC | time | - | Bench temperature |
| `flow` | L/min | time | - | Sample flow |
| `gas_mode_state` | 1 | time | - | Instrument sample state |
| `high_range_conc` | ppbv | time | - | High range concentration |
| `internal_temp` | degC | time | - | Internal instrument temperature |
| `lamp_intensity` | % | time | - | Measure of the current lamp intensity as a percentage of the nominal... |
| `lamp_volt` | V | time | - | Lamp voltage |
| `low_range_conc` | ppbv | time | - | Low range concentration |
| `perm_body_temp` | degC | time | - | Permeation body temperature |
| `perm_oven_temp` | degC | time | - | Permeation oven temperature |
| `pmt_volt` | V | time | - | PMT voltage |
| `pump_pressure` | mmHg | time | - | Pump pressure |
| `set_point_for_MFC` | cm^3/min | time | - | Set point for span calibration mass flow controller |
| `so2_background_correction` | ppbv | time | - | Instrument SO2 background correction |
| `so2_flags` | 1 | time | - | SO2 flags |
| `so2_offset` | ppbv | time | - | Offset used in SO2 correction |
| `time` | - | time | - | Time offset from midnight |
| `time_of_last_state_change` | - | time | - | Time of last state change |


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
                     params={"user": f"{user}:{token}", "ds": "bnfaosso2M1.b1",
                             "start": "2026-09-08", "end": "2026-09-08", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaosso2M1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaosso2M1.b1", "2026-09-08", "2026-09-08")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaosso2M1.b1", "2026-09-08", "2026-09-08"))   # cite what you pulled
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
27 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_so2"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("so2", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["so2"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (bnfaosso2M1.b1.20260908.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `so2` | non-equilibrium conditions, (start of calibration cycle - time)... | 485 | 0.5627 |
| `so2` | gas_mode_state != 0 | 240 | 0.2784 |
| `so2` | automated calibration period | 240 | 0.2784 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfaosso2M1.b1", "20120624", "20260923")
```

The handbook's own note on data quality: Data quality has three levels: (1) automatic flagging during zero/span state changes - first 50 s after zero actuation and first 270 s after span check eliminated, valid ambient samples not taken until 250 s after a state change, with 'centroid' of each state taken as average of the valid period once stable level achieved; (2) inspection of 2x daily zero/span checks - time series typically shows less than 3-5% relative standard deviation and minimal drift (less than 3-5%), values greater indicate need for recalibration; (3) visual inspection of the output data stream for periods of...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Reporting jitter in 1-Hz data stream | A true 1-s interval can have 0, 1, or 2 measurements reported; empty field assigned if zero points, average of two assigned if two points | LabView interface outputs data on a monotonic 1-s time base; empty fields assigned when no data | (hb p. 3) |
| Twice-daily automatic zero and span checks interrupt ambient sampling | Zero check every midnight and noon UTC; span check every 03:00 and 15:00 UTC visible as distinct excursions in raw data plot | First 50 seconds after zero actuation and first 270 seconds after span check are automatically flagged/eliminated; valid ambient samples not taken... | (hb p. 12) |
| Span/zero drift | Difference between measured span and calibrated span value; time series of 2x daily zero/span checks typically shows less than 3-5% relative standard deviation and minimal drift (less than... | Difference usually less than 15%, judged to be instability/drift in dilution flow within trace gas manifold, not measurement cell; drift greater than... | (hb p. 11) |
| Twice-daily negative spikes in pressure | Momentary negative spikes in cell pressure housekeeping data twice daily | Due to flow interruptions proximate to the zero checks; noted as expected artifact | (hb p. 10) |
| Flash lamp aging | Lamp intensity decreases over time from ~90%; flash lamp voltage automatically raised by instrument as lamp ages | Values above ~1300 V indicate lamp replacement is needed; lamp and 'flash pack' generally replaced together | (hb p. 10) |
| Residual tailing from standard addition | 2x daily spikes visible in processed ambient SO2 data plot | None specified beyond noting cause | (hb p. 12) |
| Inlet filter buildup causing SO2 hold up or destruction | Would be obvious in the span checks | All zero and span checks done through the ambient inlet filter so buildup would be detected; 2-week filter change schedule prevents dirt accumulation... | (hb p. 13) |
| Pump degradation | Change in instrument flow rate | Pump life under continuous operation is 2-3 years; monitor flow | (hb p. 13) |
| Uncertainty in standard addition dilution flow (MAOS C) | At least 10-20% uncertainty in measured dilution flow over course of typical IOP, affecting span calibration accuracy | New calibration method being retrofitted, beginning with SGP AOS | (hb p. 18) |
| Instrument/inlet failure periods | Nonsensical values in output data stream; periods of instrument inoperation | Identified and flagged via visual inspection by Mentor; documented in DQPR/DQR system | (hb p. 13) |
| Local source interference | Elevated SO2 values potentially correlated with wind direction | Can sometimes be identified by referring to wind direction at sampling point, but identification is 'quite subjective' | (hb p. 13) |
| Inlet filter replaced with impermeable spacer by mistake | Data anomaly documented in specific instances | Documented in DQPR write-ups; operators cautioned DO NOT USE SPACER, USE WHITE FILTER | (hb p. 13) |
| Acronym/header typo 'acg' instead of 'agc' | Column header in raw data labeled 'Acg int' instead of correct 'agc' | Error not corrected to preserve body of processing code | (hb p. 5) |
| Warm-up period after extended shutdown | Delayed stabilization of temperature and lamp after power-on | Warm up period can be 5-10 minutes or more for temperature and lamp stabilization | (hb p. 20) |
| PFA tubing abrasion inside instrument | Tubing wear/failure even from rubbing against another PFA tube | All tubing must be strain relieved (with tie wraps) to prevent rubbing | (hb p. 22) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | 2x daily automatic zero check (scrubbed/filtered ambient air via K2CO3 impregnated filter) at midnight and noon UTC, and 2x daily span check via standard addition at 03:00 and 15:00 UTC; initial calibration for response done by Mentor at Brookhaven National Laboratory upon receipt from manufacturer; new more accurate... (hb p. 13) |
| Calibration interval | 2x daily (zero and span checks); multipoint recalibration in zero air needed if drift greater than 10% over greater than 1 year (hb p. 13) |
| Traceability | Results tabulated by Mentor and included in the OSS (calibration database); span check level dependent on accurate measurement of dilution (inlet manifold flow), normally measured by Mentor during system integration at each site (hb p. 13) |
| Routine maintenance | Change inlet particle filter (47-mm diam, 5-µm PFA membrane filter Type LS, Millipore Catalog # LSWPO4700); use white filter, NOT the blue plastic spacer; inspect for dirt accumulation and increase change frequency if circle is visibly dark (hb p. 21) |
| Maintenance interval | every 2 weeks (hb p. 21) |


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
| `AAF` | ARM Aerial Facility |
| `AMF` | ARM Mobile Facility |
| `AMF1` | first ARM Mobile Facility |
| `AOS` | Aerosol Observing System |
| `DQPR/DQR` | Data Quality Problem Report/Data Quality Report |
| `SGP` | Southern Great Plains |
| `SO2` | sulfur dioxide |
| `MAOS` | Mobile Aerosol Observing System |


### References the handbook cites

- Daum PH and DF Leahy. The Brookhaven National Laboratory Filter Pack System For Collection and Determination of Air Pollutants, BNL #31381R2. Brookhaven National Laboratory, November 1985, p 13.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/so2_handbook.pdf (30 pages, DOE/SC-ARM-TR-180, by SR Springston)
- Catalog record: ARM data-source index, `instrument_class_code=so2`, read 2026-09-23
- Example file: `bnfaosso2M1.b1.20260908.000000.nc` from `bnfaosso2M1.b1`, 9.32 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
