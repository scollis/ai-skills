---
name: arm-instrument-sashe
description: ARM Shortwave Array Spectroradiometer-Hemispheric (sashe) - handbook-derived instrument reference. Measurement principle, reported quantities (direct_horizontal_zzz, direct_normal_zzz, diffuse_hemisp_zzz, total_hemisp_zz, diffuse_transmittance, direct_normal transmittance, aerosol_optical_depth, Wavelengths Measured), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpsashevisC1.b1) and the variable inventory of a real file. Use when working with sashe data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - sashe, Shortwave Array Spectroradiometer-Hemispheric, sgpsashevisC1.b1, direct_horizontal_zzz, direct_normal_zzz, diffuse_hemisp_zzz, total_hemisp_zz, diffuse_transmittance, direct_normal transmittance, Radiometric, ARRA, GSFC, MFRSR, NASA.
---

# SASHE - Shortwave Array Spectroradiometer-Hemispheric

SASHe measures spectrally resolved direct-normal, diffuse-horizontal, and total-horizontal shortwave irradiance from about 300-1700 nm using a hemispheric Spectralon diffuser and rotating shadowband, deployed outdoors at ARM sites with fiber-optic-linked spectrometers indoors.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sashe` |
| Handbook | [CJ Flynn](https://www.arm.gov/publications/tech_reports/handbooks/sashe_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Avantes Avaspec ULS 2048 (VIS/CCD spectrometer) and Avantes Avaspec NIR256-1.7 (NIR/InGaAs spectrometer) |
| Primary measurements | Shortwave narrowband diffuse downwelling irradiance; Shortwave narrowband direct downwelling irradiance; Shortwave narrowband direct normal irradiance; Shortwave narrowband total downwelling irradiance; Shortwave spectral diffuse downwelling irradiance; Shortwave spectral direct downwelling irradiance |
| Record | 2011-03-22 to 2024-06-02 (retired) |
| Datastreams with data | 39 across 8 sites |
| Sites | asi, cor, epc, hou, mao, pgh, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/sashe |


## Credit

Everything this skill knows about the instrument is the work of **CJ Flynn** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> CJ Flynn. *Shortwave Array Spectroradiometer–Hemispheric Instrument Handbook*.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sashe_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Photons incident on the collimator at the fore optics of the light collector travel through a large single-core optical fiber through an in-line shutter to a 50/50 bifurcated Y-fiber that diverts the signal equally to VIS and NIR spectrometers. Within each spectrometer the light is spectrally dispersed by a diffraction grating and focused onto a solid-state linear detector array, which is read electronically and passed to a computer via USB. Dark signals are obtained periodically at the same integration time by closing the in-line shutter. By coordinated operation of the spectrometers with the shadowband, diffuse hemispheric irradiance is isolated from direct solar irradiance, and the SASHe measurement is fundamentally a self-referential measurement of atmospheric transmittance obtained by extrapolating measured surface irradiance to an idealized top-of-atmosphere value via Langley regression.

**Siting.** Deployed outdoors with sky collector connected via fiber optic/electrical umbilical to indoor climate-controlled spectrometers; requires unobstructed sky view (susceptible to shading by nearby structures such as the AOS mast at AMF1 MAO); requires robust network connection and reliable time server for accurate solar ephemeris.

**Sampling.** native rate Shadowband cycle takes about 30 seconds to complete; reported every ~30 seconds per shadowband sequence; averaging Data acquisition software averages as many individual spectra as possible within a given 1-second interval, per step of the shadowband sequence (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| direct_horizontal_zzz (direct solar irradiance on... | W/(m2 nm) | - | typically ~1% | - | (hb p. 6) |
| direct_normal_zzz (direct solar irradiance at normal... | W/(m2 nm) | - | typically ~1% | - | (hb p. 6) |
| diffuse_hemisp_zzz (diffuse hemispheric irradiance on... | W/(m2 nm) | - | typically ~1% | - | (hb p. 6) |
| total_hemisp_zz (total solar irradiance) | W/(m2 nm) | - | typically ~1% | - | (hb p. 6) |
| diffuse_transmittance (sashevisaod.c1/sasheniraod.c1) | unitless (transmittance) | - | - | - | (hb p. 6) |
| direct_normal transmittance (sashevisaod.c1/sasheniraod.c1) | unitless (transmittance) | - | - | - | (hb p. 6) |
| aerosol_optical_depth | unitless | - | - | - | (hb p. 6) |
| Wavelengths Measured (Si CCD) | nm | 300-1100 nm | - | 2048 channels | (hb p. 13) |
| Wavelengths Measured (InGaAs) | nm | 900-2200 nm | - | 256 channels | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavelengths Measured | 2048 channels Si (300-1100 nm); 256 channels for the InGaAs (900-2200 nm) | (hb p. 13) |
| Instrument Field of View | Hemispheric FOV. Shadowband subtends a full-angle of about 3.6 deg or about 1.8 deg in scattering angle when centered on the sun. | (hb p. 13) |
| Sampling Interval | The shadowband cycle takes about 30 seconds to complete. The SASHe does not collect data before sunrise or after sunset. | (hb p. 13) |
| Integration Time | Adjusted by site and over the course of the year to approach spectrometer dynamic range while avoiding saturation; data acquisition software averages... | (hb p. 13) |
| Avantes Avaspec ULS 2048 (VIS spectrometer) | ~300-1100 nm, pixel spacing less than 0.6 nm, spectral resolution ~2.4 nm FWHM | (hb p. 11) |
| Avantes Avaspec NIR256-1.7 (NIR spectrometer) | ~950-1700 nm, pixel spacing less than 4 nm, spectral resolution ~6 nm FWHM | (hb p. 11) |
| Spectralon diffuser button | 8-mm-diameter, custom-machined | (hb p. 11) |
| Shadowband | 8-in.-radius, 1/2-in.-wide (also listed as 16-in.-diameter shadowband with 1/2-in. width) | (hb p. 11) |
| Refrigerator temperature control | +/- 1 degF | (hb p. 11) |
| Optical fiber | Low-OH-silica-fiber, 600-um core for transmission from 350-2500 nm | (hb p. 12) |
| Fiber-optic Y-splitter | 600 um to two 300-micron arms | (hb p. 12) |


## The data

Verified example: **`sgpsashevisC1.b1`**, file `sgpsashevisC1.b1.20240531.000012.nc`
(50.71 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1537, `test_incident_angle`=101, `wavelength_vis`=2048 |
| Data variables | 60 |
| QC variables | 22 (`qc_` companions) |
| Median time step | 26 s |
| File time span | 2024-05-31T00:00:12 to 2024-05-31T23:59:57 |
| dod version | sashevis-b1-1.4 |
| process version | ingest-sashe-1.12-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ad_temperature_vis` | degC | time | yes | Temperature of Si CCD AD board |
| `airmass` | unitless | time | yes | Airmass |
| `atmos_pressure` | kPa | time | yes | Atmospheric pressure |
| `band_azimuth` | degree_N | time | yes | Band axis orientation with respect to north |
| `bench_temperature_vis` | degC | time | yes | Temperature of Si CCD optical bench |
| `chiller_dewpoint` | degC | time | yes | Spectrometer chiller internal dew point |
| `chiller_rh` | % | time | yes | Spectrometer chiller internal RH |
| `chiller_temperature` | degC | time | yes | Spectrometer chiller internal temperature |
| `collector_dewpoint` | degC | time | yes | Collector internal dew point |
| `collector_rh` | % | time | yes | Collector internal relative humidity from TRH sensor |
| `collector_temperature` | degC | time | yes | Collector internal temperature from TRH sensor |
| `collector_x_tilt` | degree | time | yes | Collector tilt along band axis |
| `collector_x_tilt_std` | degree | time | yes | Standard deviation of collector tilt measured along band axis. |
| `collector_y_tilt` | degree | time | yes | Collector tilt perpendicular to band axis |
| `collector_y_tilt_std` | degree | time | yes | Standard deviation of collector tilt measured perpendicular to band... |
| `integration_time_vis` | ms | time | yes | Integration time of individual scans from Si CCD spectrometer |
| `mio_rh` | % | time | yes | MIO relative humidity from TRH sensor |
| `mio_temperature_mems` | degC | time | yes | Temperature of multi-IO box from MEMS sensor |
| `mio_temperature_trh` | degF | time | yes | Temperature of MIO box from TRH sensor |
| `number_of_scans_vis` | unitless | time | yes | Number of spectrometer scans averaged for Si CCD spectra |
| `solar_azimuth` | degree_N | time | yes | Solar azimuth angle relative to north |
| `solar_zenith` | degree | time | yes | Solar zenith angle relative to vertical zenith. |
| `cosine_correction_computed` | unitless | time | - | Cosine correction applied to direct_horizontal component |
| `cosine_correction_hisun` | unitless | test_incident_angle | - | Cosine correction for high sun angles |
| `cosine_correction_lowsun` | unitless | test_incident_angle | - | Cosine correction for low sun angles |
| `cosine_solar_zenith_angle` | unitless | time | - | Cosine of apparent solar zenith angle |
| `cosine_test_incident_angle` | unitless | test_incident_angle | - | Cosine of angle of incidence during cosine bench test |
| `diffuse_correction` | unitless | - | - | Cosine correction of diffuse component assuming isotropic sky |
| `diffuse_hemisp_vis` | W/m^2/nm | time,wavelength_vis | - | Diffuse hemispheric irradiance component, Si CCD spectrometer |
| `direct_horizontal_vis` | W/m^2/nm | time,wavelength_vis | - | Direct horizontal solar irradiance from Si CCD spectrometer |


_6 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpsashevisC1.b1",
                             "start": "2024-05-31", "end": "2024-05-31", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsashevisC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsashevisC1.b1", "2024-05-31", "2024-05-31")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsashevisC1.b1", "2024-05-31", "2024-05-31"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("atmos_pressure", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This datastream carries 60 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpsashevisC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["airmass", "atmos_pressure", "mio_temperature_mems", "qc_airmass", "qc_atmos_pressure", "qc_mio_temperature_mems"],
                                cleanup_qc=True)
```

## Quality control in this datastream

22 `qc_` companion variables cover 22 of the
60 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_airmass"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("airmass", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["airmass", "atmos_pressure", "mio_temperature_mems"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpsashevisC1.b1.20240531.000012.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `bench_temperature_vis` | Value is equal to missing_value. | 1537 | 100.0 |
| `ad_temperature_vis` | Value is less than the fail_min. | 1537 | 100.0 |
| `airmass` | Value is equal to missing_value. | 45 | 2.9278 |
| `chiller_dewpoint` | Value is greater than the fail_max. | 29 | 1.8868 |
| `chiller_temperature` | Value is less than the fail_min. | 19 | 1.2362 |
| `collector_temperature` | Value is greater than the fail_max. | 5 | 0.3253 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpsashevisC1.b1", "20110322", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are generated for almost 20 of the diagnostic and secondary variables, following standard ARM conventions. The sashe aod files include comprehensive QC for aerosol optical depth, direct and diffuse transmittances, and atmospheric pressure. Data quality health/status is available via the DQ Hands website (http://dq.arm.gov/). c1-level AOD data should be preferred over b1-level because of more confident calibration and more comprehensive QC.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Shading by AOS mast at AMF1 MAO | During morning in fall and spring at MAO, SASHe direct normal irradiance does not track the direct normal from the MFRSR and is near zero due to shadow from the nearby AOS stack (see DQR... | No solution besides avoiding time periods when the SASHe is shaded | (hb p. 9) |
| Limitations of Langley Analysis | Spectral regions with water vapor or other strong absorbers show non-linear curves of growth and fail to generate linear Langley regression curves; some spectral regions cannot be... | Apply modified Langley approach; augment with lamp-derived spectral responsivity measurements (planned FY16) | (hb p. 9) |
| Temperature response of Spectralon | Because Langley calibrations occur during rapid sunrise/sunset temperature changes, instrument artifacts can appear in the calibration despite active heating of the Spectralon button | Active heating applied to the Spectralon button from within the sky collector | (hb p. 9) |
| Azimuth control/drive problems | Instrument outages/data gaps at SGP due to azimuth control problem (2011-04-22 to 2011-05-01) and intermittent azimuth drive (2013-04-18 to 2013-05-07), requiring return to PNNL for repair... | Repair/replacement of azimuth drive | (hb p. 3) |
| Band failure | Data outage at SGP 2011-10-13 to 2011-11-01 due to shadowband failure | - | (hb p. 3) |
| Azimuth coupler failure | Data outage at PGH 2011-06-11 to 2011-09-09 described as 'sad' | - | (hb p. 3) |
| Monsoon prevents alignment | Extended outage/misalignment at PGH 2011-09-11 to 2012-02-14 | - | (hb p. 3) |
| Shadowband failure (SASHe2) | Data outage at PVC 2012-11-06 to 2012-12-06 | - | (hb p. 3) |
| Band misalignment (Go-Amazon) | Data quality issue at MAO 2013-12-11 to 2014-01-13 due to shadowband misalignment | - | (hb p. 3) |
| Shutter failure | Data outage at MAO 2015-06-23 to 2015-07-08 | - | (hb p. 3) |
| Internal spectrometer stray light | Cross-talk seen in stray-light scan (Figure 11) between grating-reported wavelength and true source wavelength; stray light levels generally below 0.1 to 0.01% except at isolated 'hot... | Characterized via double-slit monochromator scan; corrections considered for hot pixels | (hb p. 16) |
| External stray light leakage | Potential leakage of direct sunlight through fiber-optic jacketing; confirmed negligible by exposing/shading collector under direct solar exposure | Verified negligible; no correction needed | (hb p. 17) |
| Spectrometer signal nonlinearity | Small but non-negligible nonlinearity in spectrometer response to incident light levels/integration times | Nonlinearity documented; corrections being evaluated for robustness but not yet incorporated in current processing | (hb p. 17) |
| Spectrometer temperature sensitivity | CCD spectrometers show temperature response less than 0.1%/degree; InGaAs spectrometers show higher sensitivity mostly in thermal background (dark) levels, and exhibit a trough in... | Frequent dark measurements; chiller operated centered on temperature-sensitivity minimum rather than coldest achievable temperature | (hb p. 17) |
| Spectrometer polarization sensitivity | Grating spectrometers and off-axis reflectors show intrinsic sensitivity to linear polarization orientation | End-to-end optical train measured; sensitivity to 100% polarized light confirmed below 1% | (hb p. 17) |
| Absolute radiance calibration discrepancy | Differences between similarly calibrated radiometers observed to be as large as 10%, even though reference sphere calibration accuracy is 1-2% | Topic of current research; absolute radiance uncertainty is not the dominant term for ratio-based products like AOD | (hb p. 18) |
| Langley Io day-to-day variability | Day-to-day top-of-atmosphere Io values from Langley regression are not statistically robust, mainly due to atmospheric variability during the regression | Use robust/averaged calibrations from SASHe AOD VAP applied only to pixels free from strong molecular absorbers | (hb p. 18) |
| Real-time data only nominal calibration | Near-real-time plots have only nominal calibrations applied to both SASHe and MFRSR and should only be used to verify similar behavior, not for quantitative analysis | Use b1/c1 processed and calibrated data files instead for quantitative work | (hb p. 3) |
| b1 vs c1 AOD calibration confidence | b1-level SASHe AOD data has less confident calibration and less comprehensive QC than c1-level, which is delayed 6 weeks for robust calibration and OMI ozone data | Always use c-level AOD data in preference to b-level whenever available | (hb p. 6) |
| No pre-dawn/post-dusk data | Data gaps before sunrise and after sunset | - | (hb p. 13) |
| Instrument shading assumption violated under unstable sky | Elementary subtraction of BK from mean of S1/S2 to get raw direct horizontal signal is only valid under stable conditions where sky covered by band in S1, BK, S2 positions is equivalent;... | - | (hb p. 14) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | In situ Langley regression of log(direct normal irradiance) vs airmass extrapolated to zero-airmass intercept ('Io'), performed via the SASHe Langley VAP; supplemented for regions with strong absorbers by lamp-derived spectral responsivity / NIST-traceable broadband light source calibration (planned FY16); related... (hb p. 16) |
| Calibration interval | Langley calibration derived over periods of several weeks; SASZe annual radiance calibration (hb p. 16) |
| Traceability | NIST standards via NASA Ames Research Center or Goddard Space Flight Center integrating spheres (absolute accuracy typically 1-2% depending on wavelength) (hb p. 16) |
| Routine maintenance | Daily cleaning of optical surfaces; supply of desiccant and/or dry air to prevent condensation; routine inspection and cleaning of optical surfaces, confirmation of housekeeping measurements in nominal ranges, confirmation of shutter action and appearance of spectra (hb p. 19) |
| Maintenance interval | Daily, weekly, and monthly preventative maintenance procedures (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR, RSS, SASZe.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOD` | aerosol optical depth |
| `AOS` | Aerosol Observing System |
| `ARC` | Ames Research Center (NASA) |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `ARRA` | American Recovery and Reinvestment Act |
| `CCD` | charge-coupled device |
| `CWV` | column water vapor |
| `DOE` | U.S. Department of Energy |
| `GSFC` | Goddard Space Flight Center (NASA) |
| `IOP` | intensive operational period |
| `MFRSR` | Multi-Filter Rotating Shadowband Radiometer |
| `NASA` | National Aeronautics and Space Administration |
| `NIR` | near infrared |
| `NIST` | National Institute of Standards and Technology |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sashe_handbook.pdf (26 pages, by CJ Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=sashe`, read 2026-09-23
- Example file: `sgpsashevisC1.b1.20240531.000012.nc` from `sgpsashevisC1.b1`, 50.71 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
