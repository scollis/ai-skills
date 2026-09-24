---
name: arm-instrument-so2-air
description: ARM Sulfur Dioxide Monitor aboard Aircraft (so2-air) - handbook-derived instrument reference: measurement principle, reported quantities (Sulfur Dioxide), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (oscaafso2F1.c1) and the variable inventory of a real file. Use when working with so2-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations; Other. Triggers - so2-air, Sulfur Dioxide Monitor aboard Aircraft, oscaafso2F1.c1, Sulfur Dioxide, Airborne Observations, Other, TEI) Model 43i Trace Level-Enhanced (43i-TLE) SO2 Analyzer, DQPR/DQR, MAOS.
---

# SO2-AIR - Sulfur Dioxide Monitor aboard Aircraft

The Sulfur Dioxide Analyzer (Thermo Scientific Model 43i-TLE) measures ambient sulfur dioxide mixing ratio via pulsed UV fluorescence and is deployed aboard the ARM Aerial Facility and in ground-based ARM Aerosol Observing Systems (AAF, MAOS-C, SGP AOS).

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 30 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `so2-air` |
| Handbook | [DOE/SC-ARM-TR-180 / SR Springston / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/so2_handbook.pdf) |
| Measurement category | Airborne Observations; Other |
| Manufacturer / model | Thermo Fisher Scientific (Thermo Scientific / Thermo Electron Instruments, TEI) Model 43i Trace Level-Enhanced (43i-TLE) SO2 Analyzer, also referenced as Model 49i in modification diagram |
| Primary measurements | Sulfur Dioxide (SO2) Concentration |
| Record | 2013-06-30 to 2018-12-08 (retired) |
| Datastreams with data | 5 across 3 sites |
| Sites | cor, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/so2-air |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston. *Sulfur Dioxide Monitor Instrument Handbook*, DOE/SC-ARM-TR-180, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/so2_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `so2` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `so2-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The instrument measures SO2 based on absorbance of UV light at one wavelength by SO2 molecules, which then decay to a lower energy state by emitting UV light at a longer wavelength (SO2 + hv1 -greater than  SO2* -greater than  SO2 + hv2). The emitted light is proportional to the concentration of SO2 in the optical cell. Sample air is drawn through a hydrocarbon "kicker" that removes hydrocarbons by permeation through the tube wall while SO2 passes through unaffected. The sample flows into the fluorescence chamber where pulsating UV light excites SO2 molecules; a mirror assembly with eight selective mirrors reflects only wavelengths that excite SO2, and a bandpass filter allows only the emitted wavelengths to reach the photomultiplier tube (PMT), which detects the UV emission proportional to SO2 concentration. A photodetector continuously monitors the pulsating UV light source to compensate for fluctuations.

**Siting.** Trace-gas inlet in AOS systems consists of high-flow 1/2\" o.d. PFA tubing sampling from under the aerosol inlet rain hat at ~10-m AGL. Air is pulled into the container at 30 LPM controlled by a rotometer and the sum of instrument flow rates sampling from the manifold. Residence time to the back of the instrument is ~1-2 s. Local sources can in some instances be identified by referring to wind direction measured at the point of sampling, but identification of local interference is quite subjective.

**Sampling.** native rate nearly 1 Hz for primary signals; some parameters reported much less often; reported every 1-s time base (monotonic) in AOS final output stream; raw can have 0, 1, or 2 points per 1-s interval; averaging Averaging time (Avg Time) normally set to 1 s; Mentor QA/QC data also provided as 60-s running numerical average (arithmetic mean of present point and next 59 points) (hb p. 3).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sulfur Dioxide (SO2) mixing ratio | ppbv | extends well past conceivable ambient... | initial calibration within 1-2% accuracy; field... | ~1-s resolution (1-s time... | (hb p. 3) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | parts-per-billion (ppbv) | (hb p. 13) |
| Range | somewhat arbitrary; extends well past conceivable ambient levels in a non-power plant location | (hb p. 13) |
| Accuracy (initial, on receipt) | within 1-2% accuracy | (hb p. 13) |
| Accuracy (field variation from original standard) | ~5-10% | (hb p. 14) |
| Repeatability, 1-s signal | [SO2] sigma = 1 ppbv | (hb p. 14) |
| Repeatability, 60-s averaged | [SO2]60-s avg sigma = 0.15 ppbv | (hb p. 14) |
| 95% Confidence Interval, 1-s | +/- 2 ppbv | (hb p. 14) |
| 95% Confidence Interval, 60-s avg | +/- 0.3 ppbv | (hb p. 14) |
| Manufacturer zero noise (60-s average) | 0.25 ppb RMS | (hb p. 14) |
| Sensitivity (lower detectable limit, 1-s as reported to ARM) | 2 ppbv (95% CI above baseline) | (hb p. 14) |
| Manufacturer Lower Detectable Limit (60-s average) | 0.1 ppb | (hb p. 14) |
| Pump life | 2-3 years under continuous operation | (hb p. 13) |
| Inlet filter | 47-mm diam, 5-µm PFA membrane filter Type LS (Millipore Catalog # LSWPO4700) | (hb p. 21) |
| Sample flow through instrument | 0.5 SLPM (MAOS C / SGP AOS schematic) | (hb p. 23) |
| Trace gas manifold flow | 30 LPM (controlled by rotometer) | (hb p. 16) |


## The data

Verified example: **`oscaafso2F1.c1`**, file `oscaafso2F1.c1.20131020.190344.nc`
(0.37 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=11469 |
| Data variables | 6 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2013-10-20T19:03:44 to 2013-10-20T22:14:52 |
| dod version | aafso2-c1-1.0 |
| process version | ingest-aafso2me-1.1-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `so2` | ppbv | time | - | Sulfur dioxide (SO2) mixing ratio calculated with nominal sensitivity... |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("oscaafso2F1.c1", "2013-10-20", "2013-10-20")
ds = armlive_open("oscaafso2F1.c1", "2013-10-20", "2013-10-20", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("oscaafso2F1.c1", "20130630", "20260923")
```

The handbook's own note on data quality: First level of QC is automatic flagging of data during instrument state changes for zero/span checks (first 50 s after zero, first 270 s after span check eliminated; valid ambient samples not taken until 250 s after state change; centroid = average of valid period). Second level is inspection of 2x daily zero and span checks over the month; typical relative standard deviation less than 3-5% and drift less than 3-5%; larger values indicate need for recalibration with zero air. Third level is visual inspection of output data stream by Mentor to identify and flag periods of instrument or inlet...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Jitter in reporting frequency | A true 1-s interval can have 0, 1, or 2 measurements reported; empty field assigned when zero points reported, average assigned when two points reported | Final output stream reports at monotonic 1-s time base used in AOS systems | (hb p. 3) |
| Instrument/inst. computer clock imperfection (dithering) | Minor irregularities in output data stream timing | Processing of raw data must handle more than 1 record per second and periods with no data or only a timestamp | (hb p. 5) |
| Acg int mislabeled header (coding error) | Column header reads 'acg' instead of correct 'agc' for automatic gain control of reference channel | Error not corrected in order to preserve body of processing code | (hb p. 5) |
| Analog output Range parameter irrelevant | Range field present in raw data but analog output unused in AOS systems | None; parameter can be ignored | (hb p. 5) |
| Twice-daily negative pressure spikes | Momentary negative spikes in cell pressure at zero check times, visible in housekeeping plots | Attributed to flow interruptions proximate to the zero checks; expected/benign | (hb p. 10) |
| Flash lamp aging | Flash lamp voltage automatically raised by instrument as lamp ages; values above ~1300 V indicate lamp replacement needed | Replace lamp and electronic 'flash pack' together | (hb p. 10) |
| Span response drift/instability | Difference between measured span and calibrated span value usually less than 15%, visible as offset in zero/span check time series | Judged to be instability/drift in dilution flow within trace gas manifold, not the measurement cell; monitor over greater than 1 year, recalibrate if... | (hb p. 11) |
| Residual tailing from standard addition | 2x daily spikes in processed ambient SO2 data record due to slight residual tailing from the standard addition | None specified beyond noting cause | (hb p. 12) |
| Data invalid immediately after state changes (zero/span) | First 50 seconds after zero actuation and first 270 seconds after span check are flagged/eliminated; valid ambient samples not taken until 250 seconds after a change in state | Automatic flagging of data during state transitions; centroid taken once stable level achieved | (hb p. 12) |
| Elevated relative standard deviation or drift in zero/span checks | Zero/span check time series over month shows greater than 3-5% relative standard deviation or drift greater than 3-5% | Indicates need for instrument recalibration with zero air by Mentor | (hb p. 12) |
| Inlet filter dirt accumulation / pump degradation affecting flow rate | Reduced flow rate; visibly dark circle of trapped dirt on filter | 2-week filter change schedule prevents observed flow reduction from dirt; pump life under continuous operation is 2-3 years | (hb p. 13) |
| Instrument or inlet failure periods | Nonsensical values in output data stream; periods of instrument inoperation | Identified and flagged by Mentor via visual inspection of housekeeping and data stream; documented in DQPR/DQR system | (hb p. 13) |
| Inlet filter accidentally replaced with impermeable spacer | Documented instances where blue plastic spacer used instead of white filter, blocking flow | DO NOT USE THE SPACER; use the white filter only | (hb p. 13) |
| Local source interference | Localized SO2 spikes correlated with wind direction | Can sometimes be identified by referring to wind direction at sampling point, but identification is subjective | (hb p. 13) |
| Standard addition dilution flow uncertainty | At least 10-20% uncertainty in measured dilution flow over course of typical IOP, affecting span check accuracy | New calibration method (standard addition with MFC) being retrofitted, beginning with SGP AOS | (hb p. 18) |
| Field accuracy variation from factory calibration | Variation from original measurement standard appears to be ~5-10% under field conditions | Present system of in-field calibration being phased out by new, more accurate standard addition system | (hb p. 13) |
| PFA tubing abrasion inside instrument | Tubing can abrade even against another PFA tube, potentially causing leaks | All tubing must be strain relieved (with tie wraps) to prevent rubbing | (hb p. 22) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | 2x daily automatic zero check using scrubbed (K2CO3 impregnated filter) sample air at midnight and noon UTC, and 2x daily automatic span check using external standard addition at 03:00 and 15:00 UTC; initial calibration performed by Mentor at Brookhaven National Laboratory upon receipt from Manufacturer (hb p. 12) |
| Calibration interval | 2x daily zero/span checks; long-term drift monitored over periods greater than 1 year; multipoint recalibration in zero air needed if drift greater than 10% (hb p. 12) |
| Traceability | Calibration results tabulated by Mentor for inclusion into the OSS; span check level dependent on accurate measurement of dilution (inlet manifold flow), measured by Mentor during system integration at each site (hb p. 12) |
| Routine maintenance | Change inlet particle filter (47-mm diam, 5-µm PFA membrane filter Type LS, Millipore Catalog # LSWPO4700); filter is not directional; use white filter, not blue plastic spacer; inspect old filter for dirt buildup - if visibly dark circle, increase change frequency and notify Mentor (hb p. 21) |
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
- Catalog record: ARM data-source index, `instrument_class_code=so2-air`, read 2026-09-23
- Example file: `oscaafso2F1.c1.20131020.190344.nc` from `oscaafso2F1.c1`, 0.37 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
