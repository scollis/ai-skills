---
name: arm-instrument-sws
description: ARM Shortwave Spectroradiometer (sws) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpswsC1.b1) and the variable inventory of a real file. Use when working with sws data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Radiometric. Triggers - sws, Shortwave Spectroradiometer, sgpswsC1.b1, Radiometric, Hamamatsu Si 256-element linear diode array, MMS 1 NIR, NIR-PGS 2.2.
---

# SWS - Shortwave Spectroradiometer

The SWS measures absolute visible and near-infrared spectral radiance of the zenith directly above the instrument, deployed in a darkroom within the SGP Central Facility Optical Trailer with light delivered via a fiber-optic collector at the top of a chimney port.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sws` |
| Handbook | [DOE/SC-ARM/TR-062 / Peter Pilewskie, John Pommier / May 2007](https://www.arm.gov/publications/tech_reports/handbooks/sws_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Zeiss MMS 1 NIR enhanced and Zeiss NIR-PGS 2.2 spectrometers; Hamamatsu Si 256-element linear diode array; Hamamatsu InGaAs 256-element linear diode array |
| Primary measurements | Longwave spectral radiance; Shortwave narrowband radiance; Shortwave spectral radiance |
| Record | 1989-12-31 to 2026-09-23 (active) |
| Datastreams with data | 3 across 2 sites |
| Sites | ena, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/sws |


## Credit

Everything this skill knows about the instrument is the work of **Peter Pilewskie, John Pommier** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> Peter Pilewskie, John Pommier. *Shortwave Spectroradiometer (SWS) Handbook*, DOE/SC-ARM/TR-062, May 2007.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sws_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Photons incident on the collimator at the fore-optics of the light collector travel through the multi-optical fiber to the SWS where the fiber is bifurcated with the light passing through entrance slits to either the Si grating or the InGaAs grating. There the wavelength components are separated and imaged onto their respective diode array. The array is then read by an electronic interface which passes the data to the computer via a USB connection. Dark signals are obtained each hour, at the same integration time used to measure the intensity, by closing the shutter located at the base of the light collector.

**Siting.** The SWS is located in a darkroom, constructed by SGP site personnel in the south east corner of the Optical Trailer at the SGP Central Facility, to permit calibrations without moving the instrument. The light collector is attached to a high quality fiber optic passed through a port at the top of the optical trailer to the SWS.

**Sampling.** native rate 1 Hz; reported every Measurements are made at the rate of one per second during the day. The SWS does not collect data between the hours of 0200 - 1100 UTC.; averaging The spectra are not averaged; they are the 1 Hz spectrum collected at the indicated times. (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Absolute spectral radiance of the zenith above the... | Wm-2nm-1sr-1 | 350 - 2170 nm | 30" sphere error 1-2% over 300-2200 nm... | 8 nm (MMS 1 NIR), 12 nm... | (hb p. 4) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavelengths Measured | 256 channels in the Si (300 - 1100 nm), 256 channels for the InGaAs (900 - 2200 nm) | (hb p. 10) |
| Instrument Field of View | 1.4 degrees | (hb p. 10) |
| Sampling Interval | one per second during the day; SWS does not collect data between the hours of 0200 - 1100 UTC | (hb p. 10) |
| Integration Time | 75 - 100 ms for the Si detector; approximately 150 - 250 ms for the InGaAs detector | (hb p. 10) |
| Spectral range (overall) | 350 - 2170 nm | (hb p. 4) |
| Spectral resolution | 8 nm for the MMS 1 NIR and 12 nm for the NIR-PGS 2.2 | (hb p. 4) |
| Sampling frequency | 1 Hz | (hb p. 4) |
| Field of view | 1.4 degrees | (hb p. 4) |


## The data

Verified example: **`sgpswsC1.b1`**, file `sgpswsC1.b1.20150328.000000.cdf`
(181.35 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=53907, `wavelength`=418 |
| Data variables | 8 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2015-03-28T00:00:00 to 2015-03-28T23:59:59 |
| sampling interval | 1 second |
| dod version | sws-b1-1.2 |
| process version | ingest-sws-5.4-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `zen_spec_calib` | W/m^2/nm/sr | time,wavelength | yes | Calibrated spectrum |
| `shutter_closed` | unitless | time | - | Shutter state (0:open, 1: closed) |
| `time` | - | time | - | Time offset from midnight |
| `wavelength` | nm | wavelength | - | Wavelength |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpswsC1.b1", "2015-03-28", "2015-03-28")
ds = armlive_open("sgpswsC1.b1", "2015-03-28", "2015-03-28", cleanup_qc=True)
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
8 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpswsC1.b1.20150328.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `zen_spec_calib` | Value is equal to missing_value. | 1611390 | 7.1512 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpswsC1.b1", "19891231", "20260923")
```

The handbook's own note on data quality: Data Quality Flags are not available for this instrument at this time. Data quality health and status is available from the DQ Hands website (http://dq.arm.gov/). Monthly review by the mentor is available from the same ARM website. Data assessments by Site Scientist/Data Quality Office are not applicable to this instrument. Value-added procedures and quality measurement experiments are to be determined.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Nighttime/pre-dawn data gap | No data recorded between 0200 - 1100 UTC each day | None stated; instrument only operates during daytime hours | (hb p. 10) |
| Hourly dark signal shutter closure | Small gaps in radiance time series on the hour (e.g., 1400, 1500 UTC) when shutter closed to obtain dark signal | Dark signals obtained each hour at same integration time as intensity measurement by closing shutter | (hb p. 8) |
| Calibration transfer uncertainty | Absolute accuracy of spectral radiance depends on accuracy of transfer standard from 30" sphere to 12" sphere | 30" sphere calibrated to NIST standards; 12" sphere calibration checked weekly on-site and applied to adjust primary SWS response function if... | (hb p. 6) |
| 30" sphere calibration error | Error over spectral range 300 - 2200 nm of between 1-2% | None stated beyond noting the error magnitude | (hb p. 6) |
| Diagnostic temperature/voltage deviations | Si spectrometer temperature deviating from normal 27 C, InGaAs spectrometer temperature deviating from normal -10 C, box temperature deviating from ambient ~22 C, or PC104/PS2 voltages... | Diagnostic channels monitor health of the SWS to detect failing components | (hb p. 6) |
| No data quality flags available | Data files lack quality control flags | Not available for this instrument at this time | (hb p. 7) |
| No documented history of calibration changes | N/A - no calibration history data provided | No history is available at this time | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated at NASA Ames Airborne Science and Application Laboratory using a 30" integrating sphere (calibrated to NIST standards); calibration transferred to ARM SGP on-site 12" integrating sphere used to calibrate/monitor SWS response, with light collector lowered through ceiling port into a holder aligned with the... (hb p. 11) |
| Calibration interval | Annually at NASA Ames; weekly on-site with the ARM 12" integrating sphere at SGP (hb p. 11) |
| Traceability | 30" sphere calibrated according to NIST standards; transferred to 12" LabSphere integrating sphere used at SGP (hb p. 11) |
| Routine maintenance | Instrument preventative maintenance reports accessible at SGP operations site (hb p. 8) |


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
| `SWS` | Shortwave Spectroradiometer |
| `MMS 1 NIR` | Zeiss spectrometer for visible detection (300-1100 nm) with Si diode array |
| `NIR-PGS 2.2` | Zeiss spectrometer for near-infrared detection (900-2200 nm) with InGaAs diode array |
| `UTC` | Universal Time Coordinates |
| `SGP` | Southern Great Plains |
| `CF` | Central Facility |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sws_handbook.pdf (12 pages, DOE/SC-ARM/TR-062, by Peter Pilewskie, John Pommier)
- Catalog record: ARM data-source index, `instrument_class_code=sws`, read 2026-09-23
- Example file: `sgpswsC1.b1.20150328.000000.cdf` from `sgpswsC1.b1`, 181.35 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
