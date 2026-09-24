---
name: arm-instrument-assist
description: ARM Atmospheric Sounder Spectrometer for Infrared Spectral Technology (assist) - handbook-derived instrument reference: measurement principle, reported quantities (Sky brightness temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (magassistsummaryM1.b1) and the variable inventory of a real file. Use when working with assist data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Radiometric. Triggers - assist, magassistsummaryM1.b1, Sky brightness temperature, Radiometric, LR Tech, Inc. ASSIST, AERI, ASSIST, FTIR, LBLRTM.
---

# ASSIST - Atmospheric Sounder Spectrometer for Infrared Spectral Technology

The ASSIST measures the absolute infrared spectral radiance (W/m2/sr/cm-1) of the sky directly above it at high spectral resolution, and is deployed with the AMF2 mobile facility in a thru-wall configuration viewing straight up via a rotating scene mirror.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `assist` |
| Handbook | [DOE/SC-ARM-TR-174 / C Flynn / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/assist_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | LR Tech, Inc. ASSIST |
| Primary measurements | Longwave spectral brightness temperature; Longwave spectral radiance |
| Record | 2012-12-07 to 2018-09-24 (retired) |
| Datastreams with data | 14 across 3 sites |
| Sites | mag, sgp, tmp |
| ARM page | https://www.arm.gov/capabilities/instruments/assist |


## Credit

Everything this skill knows about the instrument is the work of **C Flynn** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> C Flynn. *Atmospheric Sounder Spectrometer for Infrared Spectral Technology (ASSIST) Instrument Handbook*, DOE/SC-ARM-TR-174, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/assist_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The ASSIST is an FTIR (Fourier Transform Infrared) spectrometer that gathers IR spectra using a Michelson-type interferometer that algebraically combines light from two paths, one of which is scanned to vary optical path length, producing interference fringes whose intensity varies as the cosine of the phase difference. For broadband light from the sky, the resulting temporal signal is a superposition of cosines that is decomposed by Fast Fourier Transform to recover the incident spectrum. A Helium Neon laser shares the moving mirror in a separate reference interferometer and is used solely to measure the retardation position of the moving mirror, enabling precise conversion of the interferogram I(x) into spectra. The instrument alternately views the sky and two internal calibration blackbodies (ambient and ~330K) via a rotating scene-viewing mirror to derive a linear (slope/offset) radiometric calibration at each wavenumber.

**Siting.** Deployed as part of the AMF2 mobile facility in a thru-wall configuration; the viewing mirror and two calibration blackbodies are separated by a thermal barrier from the interferometer and data acquisition computer. The viewing mirror is at ambient temperature while the interferometer and computer are at room temperature in the trailer. The instrument views straight up into the atmosphere with a 1.3-degree field-of-view; the viewing mirror rotates to view the sky and alternately the calibration sources.

**Sampling.** native rate 6 radiance spectra per cycle with dwell times of about 14 seconds each; reported every Calibrated sky radiance spectra produced on a cycle of about 141 seconds; spectra co-added and processed every 2 minutes; averaging Hourly-averaged zenith radiance shown in near-real-time plots (Figures 1 and 2) (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Absolute spectral radiance of the sky | watts per square meter per... | 3300 to 520 wavenumbers (cm-1) / 3-19.2... | - | 1.0 cm-1 | (hb p. 8) |
| Sky brightness temperature | degrees Kelvin | - | - | - | (hb p. 11) |
| Variance of sky infrared spectral radiance | - | - | - | as a function of wavenumber | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Spectral measurement range (normal-range instruments) | 3300 to 520 wavenumbers (cm-1) or 3-19.2 microns | (hb p. 8) |
| Spectral measurement range (extended-range polar... | 3300 to 400 cm-1 or 3-25 microns | (hb p. 8) |
| Spectral resolution | 1.0 cm-1 | (hb p. 8) |
| Instrument field-of-view | 1.3 degrees | (hb p. 8) |
| Measurement cycle | about 141 seconds with a group of 6 radiance spectra zenith having dwell times of about 14 seconds each interspersed with 55 seconds of calibration... | (hb p. 8) |
| Resolution (Instrument Details section) | one wavenumber (1/cm) | (hb p. 16) |
| Range of wavelengths (Instrument Details section) | 520 to 3300 wavenumbers | (hb p. 16) |
| Field-of-view (Instrument Details section) | 1.3-degree field-of-view, viewing straight up | (hb p. 16) |
| Calibration blackbody temperatures | ambient temperature and 330K | (hb p. 17) |
| Calibration agreement to known temperatures | within 1 Kelvin (290K and 330K) | (hb p. 17) |


## The data

Verified example: **`magassistsummaryM1.b1`**, file `magassistsummaryM1.b1.20121207.000547.cdf`
(55.36 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=3626, `wnum1`=85, `wnum2`=103 |
| Data variables | 96 |
| QC variables | 46 (`qc_` companions) |
| Median time step | 16 s |
| File time span | 2012-12-07T00:05:47 to 2012-12-07T23:59:50 |
| dod version | assistsummary-b1-1.2 |
| process version | ingest-assist-1.5-0.el5 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ch1_elevated_layer_bt` | K | time | yes | Longwave elevated air brightness temperature from radiance average... |
| `ch1_elevated_layer_radiance` | mW/(m^2 sr cm^-1) | time | yes | Longwave radiance average (700_705 cm^-1) elevated air |
| `ch1_elevated_layer_radiance_std` | mW/(m^2 sr cm^-1) | time | yes | Radiance standard deviation during sky view averaged over (700_705... |
| `ch1_hbb_nen1` | mW/(m^2 sr cm^-1) | time,wnum1 | yes | HBB 2 min NESR estimate #1 derived from variance during HBB view (ch1) |
| `ch1_hbb_nen2` | mW/(m^2 sr cm^-1) | time,wnum1 | yes | HBB 2min NESR estimate #2 derived from sequential HBB views (ch1) |
| `ch1_hbb_nen_1000wn` | mW/(m^2 sr cm^-1) | time | yes | Longwave HBB noise-equivalent radiance |
| `ch1_irt_band_brightness_temp` | deg K | time | yes | Brightness temperature computed over irt band with IRT responsivity. |
| `ch1_mean_radiance` | mW/(m^2 sr cm^-1) | time,wnum1 | yes | ASSIST longwave scene radiance spectral averages (ch1) |
| `ch1_offset_im` | mw/(m^2 sr cm^-1) | time,wnum1 | yes | Ch 1 calibration offset, imaginary component |
| `ch1_offset_re` | mw/(m^2 sr cm^-1) | time,wnum1 | yes | Ch 1 calibration offset, real component |
| `ch1_resp_im` | counts/(mW/(m^2 sr... | time,wnum1 | yes | Ch 1 responsivity, imaginary component |
| `ch1_resp_re` | counts/(mW/(m^2 sr... | time,wnum1 | yes | Ch 1 responsivity, real component |
| `ch1_responsivity_1000wn` | counts/[mW/(m^2 sr... | time | yes | Characteristic value representing overall shortwave channel... |
| `ch1_sky_nen` | mW/(m^2 sr cm^-1) | time,wnum1 | yes | Scene NESR ch 1 |
| `ch1_sky_nen_1000wn` | mW/(m^2 sr cm^-1) | time | yes | The noise equivalent radiance observed in the longwave channel during... |
| `ch1_sky_temp` | K | time,wnum1 | yes | Sky brightness temp ch1 |
| `ch1_sky_variance` | (mW/(m^2 sr cm^-1))^2 | time,wnum1 | yes | Variance of sky radiance ch 1 |
| `ch1_surface_layer_bt` | K | time | yes | Longwave surface air brightness temperature from radiance average... |
| `ch1_surface_layer_radiance` | mW/(m^2 sr cm^-1) | time | yes | Longwave radiance average (675-680 cm^-1) surface air |
| `ch1_surface_layer_radiance_std` | mW/(m^2 sr cm^-1) | time | yes | Radiance standard deviation during sky view averaged over (675_680... |
| `ch1_window_bt` | K | time | yes | Longwave window brightness temperature from radiance average (985_990... |
| `ch1_window_radiance` | mW/(m^2 sr cm^-1) | time | yes | Longwave window radiance average (985_990 cm^-1) |
| `ch1_window_radiance_std` | mW/(m^2 sr cm^-1) | time | yes | Radiance standard deviation during sky view averaged over (985_990... |
| `ch2_elevated_layer_bt` | K | time | yes | Shortwave elevated air brightness temperature from radiance average... |
| `ch2_elevated_layer_radiance` | mW/(m^2 sr cm^-1) | time | yes | Shortwave radiance average (2282_2287 cm^-1) elevated air |
| `ch2_elevated_layer_radiance_std` | mW/(m^2 sr cm^-1) | time | yes | Radiance standard deviation during sky view averaged over (2282_2287... |
| `ch2_hbb_nen1` | mW/(m^2 sr cm^-1) | time,wnum2 | yes | HBB 2min NESR estimate #1 derived from variance during HBB view (ch2) |
| `ch2_hbb_nen2` | mW/(m^2 sr cm^-1) | time,wnum2 | yes | HBB 2min NESR estimate #2 derived from sequential HBB views (ch2) |
| `ch2_hbb_nen_2500wn` | mW/(m^2 sr cm^-1) | time | yes | Shortwave hbb noise-equivalent radiance |
| `ch2_mean_radiance` | mW/(m^2 sr cm^-1) | time,wnum2 | yes | ASSIST shortwave scene radiance spectral averages (ch2) |


_18 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("magassistsummaryM1.b1", "2012-12-07", "2012-12-07")
ds = armlive_open("magassistsummaryM1.b1", "2012-12-07", "2012-12-07", cleanup_qc=True)
```

This datastream carries 96 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("magassistsummaryM1.b1", start, end,
                  keep_variables=["ch1_elevated_layer_bt", "ch1_elevated_layer_radiance", "ch1_elevated_layer_radiance_std", "qc_ch1_elevated_layer_bt", "qc_ch1_elevated_layer_radiance", "qc_ch1_elevated_layer_radiance_std"])
```

## Quality control in this datastream

46 `qc_` companion variables cover 45 of the
96 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (magassistsummaryM1.b1.20121207.000547.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `ch2_offset_im` | Value is equal to missing_value. | 311266 | 83.3425 |
| `ch2_offset_re` | Value is equal to missing_value. | 311266 | 83.3425 |
| `ch1_offset_re` | Value is equal to missing_value. | 256870 | 83.3425 |
| `ch1_offset_im` | Value is equal to missing_value. | 256870 | 83.3425 |
| `ch1_sky_variance` | Value is equal to missing_value. | 256785 | 83.3149 |
| `ch2_sky_variance` | Value is equal to missing_value. | 311163 | 83.3149 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("magassistsummaryM1.b1", "20121207", "20260923")
```

The handbook's own note on data quality: Diagnostic variables reside in .SUM files; if flagged red, data quality is usually compromised (Hatch Open, Detector Temp, LW/SW HBB NEN, LW/SW Responsivity, Rain Intensity). Additional diagnostic/maintenance flags relate mostly to temperature and humidity problems in the enclosure and components, with some indicating impending critical component failure or need for routine maintenance. Data quality flags related to ambient/hot blackbody temperature or electronic instability during calibration are also tracked; slight deviations don't affect quality but larger deviations increase noise. Data...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Hatch closed or in intermediate position | Hatch Open flag; there is no sky data when the hatch is closed (calibration data still present) | Monitor Hatch Open diagnostic flag | (hb p. 12) |
| Warm detector | Detector Temp flag indicating degraded data | - | (hb p. 12) |
| High detector noise in long wave | LW HBB NEN (Noise-equivalent Radiance in Hot Blackbody at 1000 cm-1) high values indicate degraded data | - | (hb p. 12) |
| High detector noise in shortwave | SW HBB NEN (Noise-equivalent Radiance in Hot Blackbody at 2500 cm-1) high values indicate degraded data | - | (hb p. 12) |
| Low longwave channel sensitivity | LW Responsivity low values indicate a problem; very low values affect data quality | - | (hb p. 12) |
| Low shortwave channel sensitivity | SW Responsivity low values indicate a problem; very low values affect data quality | - | (hb p. 12) |
| Rain on sky aperture / dirty rain sensor | Rain Intensity flag; rain sensor (analog output) can falsely flag under sunny skies when dirty; if rain detected the scene mirror will be safed to the down-looking position, so no sky data... | Sensor is independent indicator that hatch has not closed to protect interferometer front end in presence of rain; no explicit cleaning mitigation... | (hb p. 12) |
| Temperature/electronic instability of ambient and hot blackbodies during calibration | Data quality flags triggered by deviations from optimum ambient/hot blackbody temperature or electronics; slight deviations do not affect quality, larger deviations cause more noise and can... | Significance of deviations noted by mentor in data reviews (Section 6.2) | (hb p. 12) |
| Small temperature difference between ambient and hot blackbody | Reduced quality of temperature calibration for sky data; larger differences between ambient and hot blackbodies improve the calibration | - | (hb p. 12) |
| Cooler/detector dewar beginning to fail | Cooler Current flag; can lead to warming of the detector, which affects data quality | Immediate action warranted | (hb p. 13) |
| Cooler expander overheating | Cooler Expander Temp flag; expander too warm caused by dirty cooling fins or failed cooling motor, preventing proper cooling | - | (hb p. 13) |
| Scene mirror enclosure overheating | Scene Mirror Temp flag; usually flags with warm outside air | - | (hb p. 13) |
| Instrument enclosure too warm | Flags on BB Support Struct. Temp, Air Temp Near BBs, Spare (Shelter) Temp, Interfer. Window Temp, Interfer. 2nd Port Temp, Air Temp Near Interfer, Rack Ambient Temp, Computer Temp - can... | - | (hb p. 13) |
| Component overheating leading to failure | Flags on Cooler Comp. Temp, Mirror Motor Temp, ABB Controller Temp, HBB Controller Temp, Cooler Pwr Sup. Temp, Motor Driver Temp | - | (hb p. 13) |
| Non-constant raw/calibrated data file formats over instrument history | Housekeeping, annotator, and interferogram file formats have changed over time (ASCII strings vs csv, xls vs csv, igm/mat vs netcdf), complicating reprocessing | Newer formats (csv, netcdf) noted as improvements ('better!') | (hb p. 10) |
| Processing/ingest delays for archived data | Data collected during facility deployments available from ARM archive but processing issues have hindered autonomous processing; ingest into netcdf feasible but delayed due to effort level... | - | (hb p. 2) |
| Measurement bias relative to AERI / possible fan module aperture artifact | ASSIST-AERI collocations at SGP agreed only to within about 2 sigma of quoted specifications rather than 1 sigma; suspected cause is that the clear aperture of a fan module mounted over the... | Clear sky data collected at SGP with and without the fan module in place for comparison with collocated AERI (ongoing investigation at time of... | (hb p. 14) |
| No data collection during rain/snow | No data taken when precipitation sensors on the instrument hatch are triggered, protecting steering mirror from water/snow that would obscure optical throughput | - | (hb p. 14) |
| Residual calibration error from beam-splitter | After calibration, brightness temperature vs. wavenumber agrees with known blackbody temperatures (290K and 330K) only within 1 Kelvin; residual error thought to originate from angular... | - | (hb p. 17) |
| No VAPs currently run for ASSIST | No value-added products currently applied; noise not filtered by PCA-based methods used for AERI | Intend to process ASSIST data with the PCA Noise Filter VAP developed for AERI | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Two blackbody sources (one at ambient temperature, one at 330K) are viewed every two minutes; the magnitude of the difference between these blackbody spectra is used to compute the responsivity and offset (slope and offset defining linear instrument response at each wavenumber). Calibration procedures are performed... (hb p. 17) |
| Calibration interval | Every two minutes (hb p. 17) |
| Traceability | Compared/matched to AERI operating specifications; see Knuteson et al. 2004a,b and Revercomb et al. 2004 (hb p. 17) |
| Routine maintenance | No routine or corrective procedures beyond routine cleaning of the scene mirror with distilled or de-ionized water; because ASSIST uses a first-surface gold mirror, no contact is allowed with the mirror during cleaning - liquids or dry air only. (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AERI (Atmospheric Emitted Radiance Interferometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AERI` | Atmospheric Emitted Radiance Interferometer |
| `ARM` | Atmospheric Radiation Measurement |
| `ASSIST` | Atmospheric Sounder Spectrometer for Infrared Spectral Technology |
| `FTIR` | Fourier Transform Infrared |
| `IR` | infrared |
| `LBLRTM` | line-by-line radiative transfer model |
| `SGP` | Southern Great Plains |
| `UTC` | Universal Time Coordinates |
| `VAP` | value-added product |
| `HgCdTe` | Mercury Cadmium Telluride Detector for long wavelength infrared detection (5 to 15... |
| `InSb` | or "insbee" detector optimized for near-to-mid-infrared 1 to 5 microns |
| `Wavenumber` | the inverse of the wavelength in centimeters; wavenumber is proportional to photon energy... |


### References the handbook cites

- Knuteson et al. 2004a - Atmospheric Emitted Radiance Interferometer. Part I: Instrument Design. J. Atmos. Oceanic Technol. 21:1763-1776.
- Knuteson et al. 2004b - Atmospheric Emitted Radiance Interferometer. Part II: Instrument Performance. J. Atmos. Oceanic Technol. 21:1777-1789.
- Revercomb, HE, H Buijs, HB Howell, DD LaPorte, WL Smith, and LA Sromovsky. 2004. Radiometric Calibration of IR Fourier Transform Spectrometers: Solution to a Problem with the High-Resolution Interferometer Sounder....
- Brown, PD, SA Clough, NE Miller, TR Shippert, DR Turner, RO Knuteson, HE Revercomb, and WL Smith. 1995. Initial Analyses of Surface Spectral Radiance between Observations and Line-by-Line Calculations.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/assist_handbook.pdf (22 pages, DOE/SC-ARM-TR-174, by C Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=assist`, read 2026-09-23
- Example file: `magassistsummaryM1.b1.20121207.000547.cdf` from `magassistsummaryM1.b1`, 55.36 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
