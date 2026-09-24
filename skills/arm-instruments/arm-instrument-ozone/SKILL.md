---
name: arm-instrument-ozone
description: ARM Ozone Monitor (ozone) - handbook-derived instrument reference. Measurement principle, reported quantities (Ozone), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaoso3C1.b1) and the variable inventory of a real file. Use when working with ozone data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Other. Triggers - ozone, Ozone Monitor, enaaoso3C1.b1, Ozone, Other, Thermo Fisher Scientific Inc., Model 49i (i-series), DQPR, NIST, NYS DEC, o.d..
---

# OZONE - Ozone Monitor

The Ozone Monitor measures ambient atmospheric ozone (O3) concentration in situ via UV absorbance at 254 nm in a dual-cell photometer, deployed at ARM AAF, AMF1/AMF2/AMF3 AOS, SGP, and ENA sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ozone` |
| Handbook | [DOE/SC-ARM-TR-179 / SR Springston, R Trojanowski, C Hayes / April 2025](https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf) |
| Measurement category | Other |
| Manufacturer / model | Thermo Fisher Scientific Inc., Model 49i (i-series) |
| Primary measurements | Ozone Concentration |
| Record | 2010-10-04 to 2026-09-23 (active) |
| Datastreams with data | 63 across 22 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mag |
| ARM page | https://www.arm.gov/capabilities/instruments/ozone |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston, R Trojanowski, C Hayes** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston, R Trojanowski, C Hayes. *Ozone Monitor (OZONE) Instrument Handbook*, DOE/SC-ARM-TR-179, April 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `ozone-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `ozone`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The ozone monitor measures ozone based on the absorbance of ultraviolet (UV) light at a wavelength of 254 nm by ozone molecules, with absorbance related to concentration through the Beer-Lambert Law: I/I0 = e-KLC, where K is the molecular absorption coefficient (308 cm-1 at 0C and 1 atm), L is the cell length (38 cm), and C is ozone concentration in ppm. The sample is split into two gas streams: one passes through an ozone scrubber to become the reference gas (Io), while the other flows directly as sample gas (I). Solenoid valves alternate the reference and sample gas streams between cells A and B every 10 seconds (actual 4 s), so optical effects such as changes in lamp output, detector gain, and cell cleanliness are rejected. The dual cell configuration with selective removal of ozone in the reference cell reduces response from interfering species, and the instrument contains an internal ozone source to measure response stability over time.

**Siting.** The trace-gas inlet used in the AOS systems consists of high-flow 1/2 inch o.d. PFA tubing sampling from under the aerosol inlet rain hat at ~10-m above ground level; air is pulled into the container at 30 LPM controlled by a rotometer; residence time to the back of the instrument is ~1-2 s.

**Sampling.** native rate instrument makes an independent measurement every 4 seconds due to internal pneumatic switching limitations; reported every 1-s resolution in AOS systems (same concentration repeated ~4 times at uniform 1-s time base); averaging Avg Time field reports 10 s (2.5X actual averaging time) when averaging time is actually 4 s in fast response mode (default for AOS) (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Ozone (O3) mixing ratio | ppbv (raw data reported in... | linearity demonstrated up to 1500 ppbv | initial calibration within 1-2%; field... | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | parts per million (ppm) by the instrument | (hb p. 19) |
| Range | Linearity up to 1500 ppbv demonstrated with automatic span checks twice daily; full range extends well past conceivable ambient levels | (hb p. 20) |
| Accuracy | Initial (on receipt) calibration within 1-2% accuracy; field variation from original measurement standard ~5% | (hb p. 20) |
| Repeatability | [O3] sigma = 2 ppbv; [O3] 95% Confidence Interval = +/- 4 ppbv | (hb p. 20) |
| Manufacturer zero noise | 0.25 ppb RMS (60-s average) | (hb p. 20) |
| Sensitivity | 95% confidence interval above baseline = 4 ppbv (1 value/sec, each representing 4 repetitive 4-s integrations); similar to 1.0 ppb Lower Detectable... | (hb p. 20) |
| Molecular absorption coefficient (K) | 308 cm-1 (at 0C and 1 atmosphere) | (hb p. 8) |
| Cell length (L) | 38 cm | (hb p. 8) |
| Measurement cycle | 4-s measurement cycle; reference and sample cells reversed after each cycle | (hb p. 8) |
| Pump life | 2-3 years under continuous operation | (hb p. 13) |
| Filter change schedule | every two weeks | (hb p. 13) |
| Filter type | 47-mm diam. 5-µm PFA membrane filter Type LS (Millipore Catalog # LSWPO4700) | (hb p. 17) |


## The data

Verified example: **`enaaoso3C1.b1`**, file `enaaoso3C1.b1.20260827.000000.nc`
(16.26 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86377 |
| Data variables | 46 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-08-27T00:00:00 to 2026-08-27T23:59:59 |
| sampling interval | 1 second |
| dod version | aoso3-b1-3.1 |
| process version | ingest-aoso3corr-2.3-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `o3` | ppb | time | yes | Ozone concentration at STP |
| `averaging_time` | s | time | - | Instrument averaging time |
| `calibration_level_1` | % | time | - | Calibration ratio level 1 |
| `calibration_level_2` | % | time | - | Calibration ratio level 2 |
| `calibration_level_3` | % | time | - | Calibration ratio level 3 |
| `calibration_level_4` | % | time | - | Calibration ratio level 4 |
| `calibration_level_5` | % | time | - | Calibration ratio level 5 |
| `diagnostic_voltage_mb_15` | V | time | - | Diagnostic +15 volts at motherboard |
| `diagnostic_voltage_mb_24` | V | time | - | Diagnostic +24 volts at motherboard |
| `diagnostic_voltage_mb_3p3` | V | time | - | Diagnostic +3.3 volts at motherboard |
| `diagnostic_voltage_mb_5` | V | time | - | Diagnostic +5 volts at motherboard |
| `diagnostic_voltage_mb_minus_3p3` | V | time | - | Diagnostic -3.3 volts at motherboard |
| `diagnostic_voltage_mib_15` | V | time | - | Diagnostic +15 volts at measurement interface board |
| `diagnostic_voltage_mib_24` | V | time | - | Diagnostic +24 volts at measurement interface board |
| `diagnostic_voltage_mib_3p3` | V | time | - | Diagnostic +3.3 volts at measurement interface board |
| `diagnostic_voltage_mib_5` | V | time | - | Diagnostic +5 volts at measurement interface board |
| `diagnostic_voltage_mib_minus_15` | V | time | - | Diagnostic -15 volts at measurement interface board |
| `flow_a` | L/min | time | - | Flow in cell A |
| `flow_b` | L/min | time | - | Flow in cell B |
| `gas_state` | 1 | time | - | Gas state |
| `intensity_a` | Hz | time | - | Intensity in cell A |
| `intensity_b` | Hz | time | - | Intensity in cell B |
| `lamp_level` | % | time | - | Lamp level |
| `lamp_temperature` | degC | time | - | Lamp temperature |
| `lamp_voltage_bench` | V | time | - | Lamp bench voltage |
| `lamp_voltage_ozonizer` | V | time | - | Lamp voltage ozonizer |
| `noise_a` | Hz | time | - | Electric noise in cell A |
| `noise_b` | Hz | time | - | Electric noise in cell B |
| `o3_background` | ppb | time | - | Ozone background |
| `o3_bench_temperature` | degC | time | - | Bench temperature |


_11 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaoso3C1.b1", "2026-08-27", "2026-08-27")
ds = armlive_open("enaaoso3C1.b1", "2026-08-27", "2026-08-27", cleanup_qc=True)
```

This datastream carries 46 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enaaoso3C1.b1", start, end,
                  keep_variables=["o3", "averaging_time", "calibration_level_1", "qc_o3"])
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
46 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaoso3C1.b1.20260827.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `o3` | Scheduled calibration | 1068 | 1.2364 |
| `o3` | pressure_compensation_state = 0 OR... | 1059 | 1.226 |
| `o3` | noise_b less than  noise_b_min_alarm OR noise_b greater than ... | 1004 | 1.1623 |
| `o3` | noise_a less than  noise_a_min_alarm OR noise_a greater than ... | 1000 | 1.1577 |
| `o3` | Value is greater than fail_max. | 595 | 0.6888 |
| `o3` | non-equilibrium conditions, (start of calibration cycle - time)... | 240 | 0.2779 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaoso3C1.b1", "20101004", "20260923")
```

The handbook's own note on data quality: Three levels of data quality: (1) automatic flagging during zero/span state changes (first 105 s after zero, first 30 s after each span level eliminated; centroid = ~30-s average); (2) inspection of 2X daily zeros and span checks via monthly time series, typically showing less than 1-2% relative standard deviation and minimal drift (less than 2%), values greater indicating need for recalibration at NYS DEC (no ARM capability to deliver calibration source to remote field sites); (3) visual inspection of output data stream to identify instrument/inlet failure periods and short 4-s instrumental...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| 4-s duration signal spikes (instrumental aberrations) | Short positive or negative excursions of 20-40 ppbv lasting ~4 s (one measurement cycle) that dramatically affect daily max/min readings; a step function on this time scale is nonsensical... | These excursions are flagged for deletion; distinguishable from real ambient titration events by duration | (hb p. 13) |
| NO titration of ambient ozone from local combustion sources | Negative peaks of 30-s to 10-min duration, visually distinguishable from 4-s instrumental spikes | These represent real ambient changes and are NOT flagged; local sources can sometimes be identified by referring to wind direction, though... | (hb p. 13) |
| Zero/span check periods embedded in data stream | Automatic zero and span check occurs every midnight and noon (00:00:00 and 12:00:00), lasting 4 minutes each, visible as distinct excursions in raw data plots | First 105 seconds after zero actuation and first 30 seconds after each span level are automatically flagged/eliminated; centroid taken as ~30-second... | (hb p. 12) |
| Span check source (photolysis lamp) instability/drift | Difference between measured span and calibrated span value usually less than 5%; monitored via monthly zero/span stability plots; drift greater than 5% over greater than 1 year indicates... | Judged to be instability/drift in the photolysis lamp, not the measurement cell; recalibrate at NYS DEC laboratory when drift exceeds 5% | (hb p. 11) |
| Lamp intensity degradation | Cell A/B raw detector Hz value (Cell Int) decreases; when Intensity goes below ~60,000 Hz | Lamp voltage must be increased or lamp replaced; mentor raises lamp intensity to 110-120,000 Hz | (hb p. 12) |
| Excess electronic noise in channels A/B | Noise A/Noise B values normally less than 10; excess values observed | Can indicate the need to clean the cell or replace the lamp | (hb p. 11) |
| Dirty or blocked inlet filter | Flow A/Flow B (uncalibrated) values change, useful indicator of filter condition; visible dark trapped dirt circle on filter during inspection | Change filter every two weeks; if visibly dark, increase change frequency and notify mentor; given two-week schedule, dirt accumulation not observed... | (hb p. 5) |
| Twice-daily negative pressure spikes in housekeeping data | Momentary negative spikes in sample cell pressure in housekeeping plots, coincident with zero/span checks | Due to flow interruptions proximate to zero/span checks; considered a normal artifact | (hb p. 10) |
| No water vapor correction | Reported O3 mixing ratio may be biased if ambient water vapor affects measurement | None stated; instrument's primary measurement of O3 mixing volume in ambient air has no water vapor correction | (hb p. 7) |
| Instrument failure / inlet failure periods | Nonsensical values in output data stream; requires visual inspection to identify | Periods flagged by mentor via visual inspection; documented in DQPR/DQR system as unique individual events; complete housekeeping recording aids... | (hb p. 13) |
| Inlet filter mistakenly replaced with impermeable spacer | Documented instances where blue plastic spacer used instead of white filter, causing flow/data issues | DO NOT USE THE SPACER! USE THE WHITE FILTER (error made multiple times); mentor documents such instances | (hb p. 13) |
| Ozone span generator pressure sensitivity | Output span concentration can vary with atmospheric pressure since span generator draws ambient air (varies with inverse square of ambient pressure) | Supplied pressure regulator only supplies consistent gauge pressure not absolute pressure; effect noted as similar | (hb p. 16) |
| Clock/timing dithering | Minor irregularities (dithering) in output data stream timestamps because neither instrument clock nor instrument computer clock are perfect | Processing of raw data must handle more than 1 record per second and periods with no data or only date/time stamp | (hb p. 7) |
| Reported averaging time field mislabeled | Avg Time field reports 10 s in AOS systems when actual averaging time is 4 s (fast response mode reports 2.5X actual averaging time) | None stated beyond noting the discrepancy for correct interpretation | (hb p. 6) |
| PFA tubing abrasion inside instrument | Internal PFA tubing can abrade even against other PFA tubing, potentially causing leaks/failures | All tubing must be strain-relieved with tie wraps to prevent rubbing | (hb p. 19) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated for response upon receipt from manufacturer by the mentor at the NYS DEC testing laboratory in Albany, NY; internal calibration checked against NYS DEC standard along with the internal span source; 2X daily internal zero and 5-level span checks reveal short-term (daily) and long-term (annual) drifts (hb p. 19) |
| Calibration interval | 2X daily zero and span checks; recalibration at NYS DEC when drift exceeds 5% over periods greater than 1 year (hb p. 19) |
| Traceability | The DEC reference standard is certified by the U.S. EPA with a NIST-traceable reference (hb p. 19) |
| Routine maintenance | Change the inlet particle filter (47-mm diam. 5-µm PFA membrane filter Type LS, Millipore Catalog # LSWPO4700); filter is not directional; use the white filter, NOT the blue plastic spacer; inspect filter for dirt buildup (hb p. 17) |
| Maintenance interval | every two weeks (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ARM Aerial Facility (AAF), AMF1 AOS, AMF2 AOS, AMF3 AOS, SGP atmospheric observatory, ENA.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AMF` | ARM Mobile Facility |
| `AMF1` | first ARM Mobile Facility |
| `AMF2` | second ARM Mobile Facility |
| `AMF3` | third ARM Mobile Facility |
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `atm` | atmosphere |
| `BNL` | Brookhaven National Laboratory |
| `DOE` | U.S. Department of Energy |
| `DQPR` | Data Quality Problem Report |
| `DQR` | Data Quality Report |
| `ENA` | Eastern North Atlantic |
| `LPM` | liters per minute |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf (26 pages, DOE/SC-ARM-TR-179, by SR Springston, R Trojanowski, C Hayes)
- Catalog record: ARM data-source index, `instrument_class_code=ozone`, read 2026-09-23
- Example file: `enaaoso3C1.b1.20260827.000000.nc` from `enaaoso3C1.b1`, 16.26 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
