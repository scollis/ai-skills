---
name: arm-instrument-caps-pmex
description: ARM Cavity Attenuated Phase Shift Extinction Monitor (caps-pmex) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol optical extinction, Extinction, Loss, Pressure, Temperature, Signal, Flow Sensor, Last Baseline), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaoscaps3wC1.b1) and the variable inventory of a real file. Use when working with caps-pmex data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - caps-pmex, Cavity Attenuated Phase Shift Extinction Monitor, enaaoscaps3wC1.b1, Aerosol optical extinction, Extinction, Loss, Pressure, Temperature, Signal, Aerosols, Aerodyne Research, Inc. CAPS PMex Monitor, ASCII, CalNex, CAPS, CAPS PMex.
---

# CAPS-PMEX - Cavity Attenuated Phase Shift Extinction Monitor

The CAPS PMex monitor measures aerosol optical extinction (the sum of scattering and absorption) in situ via an optical extinction spectrometer sampling ambient or process air through an inlet.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `caps-pmex` |
| Handbook | [DOE/SC-ARM-TR-155 / AJ Sedlacek, S Smith / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/caps-pmex_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Aerodyne Research, Inc. CAPS PMex Monitor |
| Primary measurements | Aerosol extinction |
| Record | 2014-02-18 to 2026-09-23 (active) |
| Datastreams with data | 15 across 4 sites |
| Sites | bnf, ena, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/caps-pmex |


## Credit

Everything this skill knows about the instrument is the work of **AJ Sedlacek, S Smith** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> AJ Sedlacek, S Smith. *Cavity Attenuated Phase Shift Extinction Monitor Instrument Handbook*, DOE/SC-ARM-TR-155, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/caps-pmex_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Unlike a conventional absorption spectrometer that measures light attenuation directly, the CAPS monitor measures the average time light spends in the sample cell, which decreases as particle concentration increases due to scattering/absorption. A square-wave modulated LED is directed into a high-reflectivity mirror (Rgreater than =0.9998) sample cell providing an optical path length of 1-2 km, and the light exiting through the back mirror is detected as a phase-shifted, distorted waveform relative to the LED modulation. The phase shift (theta) relates to extinction via cot(theta) = cot(theta_o) + c/(2*pi*f)*epsilon, where theta_o is obtained from a periodic particle-free baseline measurement, c is the speed of light, f is the LED modulation frequency, and epsilon is the absolute extinction. This yields an absolute measurement requiring no calibration, averaged over the effective spectral output of the LED, band-pass filter, and mirror reflectivity.

**Siting.** Monitor is rack-mounted (19-inch rack, 5U/7U) with inlet and outlet ports on back panel requiring removal of Swagelock shipping plugs before startup; sample flow drawn through inlet with critical orifice/diaphragm pump; when shipped to field, units are run with dry air and re-plugged to prevent mirror contamination during transit.

**Sampling.** native rate 1 second sample period (default); reported every Sample period can be set to integer values; recommended not to exceed 30 seconds; averaging Data can be averaged after measurements are made; example plots show 1-hour and 1-minute averages (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol optical extinction | Mm-1 | 0 to 4000 Mm-1 | less than 5% (Massoli et al. 2010) | 0.1 Mm-1 | (hb p. 11) |
| Extinction (front panel display) | Mm-1 | below 200 Mm-1 at 0.1 Mm-1 resolution;... | - | 0.1 Mm-1 (less than 200... | (hb p. 8) |
| Loss | Mm-1 | - | - | - | (hb p. 8) |
| Pressure | Torr | - | - | - | (hb p. 8) |
| Temperature | K | - | - | - | (hb p. 8) |
| Signal | arbitrary units (mV) | - | - | - | (hb p. 8) |
| Flow Sensor | cm3 s-1 | - | - | - | (hb p. 8) |
| Last Baseline | Mm-1 | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Measurement range | 0 to 4000 Mm-1 | (hb p. 11) |
| Resolution | 0.1 Mm-1 | (hb p. 11) |
| Precision (3σ, 1 s) | less than 3 Mm-1 | (hb p. 11) |
| Time response | less than 2 seconds | (hb p. 11) |
| Baseline drift | automated baseline provided | (hb p. 11) |
| Span drift | negligible | (hb p. 11) |
| Sample flow rate | 0.85 liters per minute/cell | (hb p. 11) |
| Purge flow | provided internally | (hb p. 11) |
| Cell pressure | ambient | (hb p. 11) |
| Cell temperature | ~5º above ambient | (hb p. 11) |
| Power usage | less than 50 Watts (@120 VAC)/less than  200 watts (3 cell system) | (hb p. 11) |
| Weight | 12 kg/30kg | (hb p. 11) |
| Size | ~65 cm x 43 cm x 23 cm (length × width × height) | (hb p. 11) |
| Rack mount | 19-inch rack mount, 5U/7U, 24 inches deep | (hb p. 11) |
| Accuracy - Resolution | 0.1 Mm-1 | (hb p. 11) |
| Repeatability - Precision (3σ, 1s) | less than 3 Mm-1 | (hb p. 11) |
| Sensitivity (SNR=3) | 2.5 Mm-1 (1 second), 0.25 Mm-1 (60 seconds) | (hb p. 11) |
| Uncertainty | less than 5% (Massoli et al. 2010) | (hb p. 12) |
| Input Voltage | 50 W; 100 to 250 VAC (50 to 60 Hz) | (hb p. 12) |
| Mirror reflectivity | R ≥0.9998 | (hb p. 13) |
| Optical path length | 1 to 2 km | (hb p. 13) |
| Vacuum tolerance | up to ~300 Torr below ambient | (hb p. 17) |


## The data

Verified example: **`enaaoscaps3wC1.b1`**, file `enaaoscaps3wC1.b1.20250929.000000.nc`
(9.35 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86386 |
| Data variables | 27 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2025-09-29T00:00:00 to 2025-09-29T23:59:59 |
| sampling interval | 1 second |
| dod version | aoscaps3w-b1-1.2 |
| process version | ingest-aoscaps3wcorr-1.2-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Bext_B` | Mm-1 | time | yes | Aerosol extinction coefficient, blue wavelength |
| `Bext_G` | Mm-1 | time | yes | Aerosol extinction coefficient, green wavelength |
| `Bext_R` | Mm-1 | time | yes | Aerosol extinction coefficient, red wavelength |
| `impactor_state` | 1 | time | yes | Impactor state in terms of aerodynamic diameter cut off |
| `ambient_temperature` | K | time | - | Ambient temperature near instrument |
| `internal_pressure` | torr | time | - | Internal instrument pressure |
| `last_baseline_B` | Mm-1 | time | - | Last baseline check, blue wavelength |
| `last_baseline_G` | Mm-1 | time | - | Last baseline check, green wavelength |
| `last_baseline_R` | Mm-1 | time | - | Last baseline check, red wavelength |
| `raw_loss_B` | Mm-1 | time | - | Raw measure of cavity loss, blue wavelength |
| `raw_loss_G` | Mm-1 | time | - | Raw measure of cavity loss, green wavelength |
| `raw_loss_R` | Mm-1 | time | - | Raw measure of cavity loss, red wavelength |
| `seconds_after_transition` | s | time | - | Seconds since last impactor transition |
| `signal_B` | 1 | time | - | Light signal level, blue wavelength |
| `signal_G` | 1 | time | - | Light signal level, green wavelength |
| `signal_R` | 1 | time | - | Light signal level, red wavelength |
| `status_baseline` | 1 | time | - | Baseline status |
| `status_pump` | 1 | time | - | Status of pump |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaoscaps3wC1.b1", "2025-09-29", "2025-09-29")
ds = armlive_open("enaaoscaps3wC1.b1", "2025-09-29", "2025-09-29", cleanup_qc=True)
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
27 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaoscaps3wC1.b1.20250929.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Bext_R` | qc_impactor_state is bad | 6960 | 8.0569 |
| `Bext_G` | qc_impactor_state is bad | 6960 | 8.0569 |
| `Bext_B` | qc_impactor_state is bad | 6960 | 8.0569 |
| `Bext_R` | status_baseline == 1 or status_baseline == 2 (baseline_on,... | 6048 | 7.0011 |
| `Bext_G` | status_baseline == 1 or status_baseline == 2 (baseline_on,... | 6048 | 7.0011 |
| `Bext_B` | status_baseline == 1 or status_baseline == 2 (baseline_on,... | 6048 | 7.0011 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaoscaps3wC1.b1", "20140218", "20260923")
```

The handbook's own note on data quality: The mentor performs a monthly quality-control check of data before it is submitted to the ARM Data Center. The Status code (5-digit number a-e: pump status, baseline status, unused, monitor type, wavelength) is typically used in subsequent data analysis to determine periods of baseline measurement or other upset conditions; if using a user-supplied data-acquisition program, it is recommended that all output fields be recorded to allow reconstruction of data in case of problems with baseline procedures, calibration, etc., and to provide diagnostic information.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Front-panel display offset error | Front panel digital voltmeter display (converted from 0-10V analog signal) shows readings with accuracy limited by offset errors; disagrees with RS-232 reported values | Use RS-232 output for true and most accurate readings rather than relying on front panel display | (hb p. 8) |
| Display saturation/resolution change at high concentration | Front panel readings revert from 0.1 Mm-1 resolution to 1 Mm-1 resolution above 200 Mm-1, and display stops providing readings above 2000 Mm-1 even though digital output continues | Rely on digital RS-232 output rather than front panel display for high-concentration periods | (hb p. 8) |
| Onboard memory overwrite | After ~6 months of 1-second data, oldest onboard files begin to be overwritten | Periodically copy files via USB port using the supplied data-acquisition program | (hb p. 9) |
| Baseline/flush periods reduce duty cycle | Periods flagged by Baseline Status codes (1=flush,2=measurement) in Status field represent non-ambient measurement time, lowering the fraction of time actual extinction is measured | Set flush 10-15s, baseline 60s, and choose baseline interval (15-30 min for low-extinction air) to maintain duty cycle of 90% or greater; lengthen... | (hb p. 16) |
| Mirror contamination from vacuum release | Increased noise and elevated optical Loss values (approaching 1000 Mm-1, versus shipping baseline 400-550 Mm-1) indicating loss of sensitivity | Release any substantial vacuum (up to ~300 Torr below ambient) very slowly to avoid disturbing particles that could contaminate mirrors | (hb p. 17) |
| High particle loading filter pressure drop / clogging | Pressure drop during baseline measurement period exceeds 20 Torr, or inlet filter pressure drop reaches ~30 Torr | Check pressure drop during baseline for high-particle-loading samples (e.g., diesel exhaust); replace filter when drop exceeds recommended thresholds | (hb p. 17) |
| Extinction levels above 1000 Mm-1 causing frequent filter changes and mirror... | Frequent need to replace filter elements; possible mirror contamination evidenced by rising Loss values | Dilute sample flow with particle-free air if extinction levels above 1000 Mm-1 are regularly encountered | (hb p. 17) |
| Onboard clock drift (battery-backed) | Loss of correct date/time on onboard computer if AA batteries in the internal battery case fail | Replace the two AA batteries in the black battery case; data-acquisition program automatically time-synchronizes monitor with computer at ~12:00 a.m.... | (hb p. 17) |
| Mirror/cell contamination from particulates or liquid condensation during cleaning | Single visible particle on mirror surface causes significant optical loss; performing cleaning in high relative humidity leads to liquid water condensation on mirrors, seen as further... | Avoid lint/particulate contamination during mirror handling; avoid cleaning mirrors in high relative humidity environments | (hb p. 22) |
| Cell knife-edge damage | Misalignment of mirrors leading to degraded optical performance if the knife-edge surface inside the cell is damaged (e.g., by brushing) | Do not clean inside of cell with a brush or other device; if knife-edge is damaged, cell must be replaced | (hb p. 22) |
| Shipping-related mirror contamination | Elevated optical loss values noted upon initial startup after shipment | Run dry air through the monitor for several hours before shipping and then plug inlet/outlet ports with Swagelock plugs | (hb p. 15) |
| Averaged spectral extinction value | Reported extinction is not a single monochromatic value but an average over the effective spectral output of the specific LED, band-pass filter, and mirror reflectivity used | - | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | The CAPS instrument provides an absolute measurement based on phase-shift theory (cot(theta)=cot(theta_o)+c/(2*pi*f)*epsilon) and does not require calibration; periodic automated baseline (particle-free air) measurement is used to obtain cot(theta_o). (hb p. 10) |
| Calibration interval | Automated baseline default: 15 s flush, 60 s zero periods; recommended baseline interval every 15 or 30 minutes for low-extinction environments (less than 10 Mm-1); longer intervals for higher-extinction environments (hb p. 10) |
| Traceability | Absolute physical measurement (no external calibration standard required); uncertainty referenced to Massoli et al. 2010 laboratory validation (hb p. 10) |
| Routine maintenance | Replacement of inline inlet particle filter and outlet disposable filter; periodic mirror cleaning if contaminated; cell cleaning via ultrasonic bath if contaminated (hb p. 19) |
| Maintenance interval | Annual replacement under normal ambient conditions; as often as several hours under high particle loadings (combustion sampling); inlet filter replaced when pressure drop reaches ~30 Torr (hb p. 19) |


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
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `CalNex` | California Nexus |
| `CAPS` | cavity attenuated phase shift |
| `CAPS PMex` | cavity attenuated phase shift extinction monitor |
| `DOE` | U.S. Department of Energy |
| `DOS` | disk operating system |
| `LED` | light-emitting diode |
| `MS` | Microsoft |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `USB` | Universal Serial Bus |
| `VAC` | volts alternating current |


### References the handbook cites

- Massoli, P, P Kebabian, T Onasch, F Hills, and A Freedman. 2010. "Aerosol light extinction measurements by Cavity Attenuated Phase Shift Spectroscopy (CAPS): Laboratory validation and field deployment of a compact...
- Kebabian, PL, WA Robinson, and A Freedman. 2007. "Optical extinction monitor using cw cavity enhanced detection." Review of Scientific Instruments 78:063102, https://doi.org/10.1063/1.2744223
- Kebabian, PL, and A Freedman. 2007. "System and Method for Trace Species Detection using Cavity Attenuated Phase Shift Spectroscopy with an Incoherent Light Source." U.S. Patent No. 7301639 (issued November 27, 2007).

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/caps-pmex_handbook.pdf (23 pages, DOE/SC-ARM-TR-155, by AJ Sedlacek, S Smith)
- Catalog record: ARM data-source index, `instrument_class_code=caps-pmex`, read 2026-09-23
- Example file: `enaaoscaps3wC1.b1.20250929.000000.nc` from `enaaoscaps3wC1.b1`, 9.35 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
