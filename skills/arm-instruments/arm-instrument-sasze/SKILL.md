---
name: arm-instrument-sasze
description: ARM Shortwave Array Spectroradiometer-Zenith (sasze) - handbook-derived instrument reference. Measurement principle, reported quantities (zenith spectral shortwave radiance, zenith_transmittance), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpsaszenirC1.a1) and the variable inventory of a real file. Use when working with sasze data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - sasze, Shortwave Array Spectroradiometer-Zenith, sgpsaszenirC1.a1, zenith spectral shortwave radiance, zenith_transmittance, Radiometric, Thorlabs RC08FC collimator, ARRA, ASCII, FWHM, GPCI.
---

# SASZE - Shortwave Array Spectroradiometer-Zenith

The Shortwave Array Spectroradiometer–Zenith (SASZe) measures zenith spectral shortwave sky radiance at 1 Hz from about 300 nm to 1700 nm using an outdoor collimating optical collector fiber-coupled to two indoor grating spectrometers, deployed at ARM fixed and mobile facility sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sasze` |
| Handbook | [DOE/SC-ARM-TR-178 / CJ Flynn / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/sasze_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Avantes Avaspec ULS 2048 CCD Si array spectrometer and Avantes Avaspec NIR256-1.7 linear InGaAs array spectrometer; Thorlabs RC08FC collimator; Avantes FOS-1 inline fiber optic shutter |
| Primary measurements | Shortwave spectral direct normal irradiance; Shortwave spectral radiance |
| Record | 2011-03-22 to 2024-06-02 (retired) |
| Datastreams with data | 34 across 9 sites |
| Sites | asi, cor, epc, hou, mag, mao, pgh, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/sasze |


## Credit

Everything this skill knows about the instrument is the work of **CJ Flynn** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> CJ Flynn. *Shortwave Array Spectroradiometer–Zenith Instrument Handbook*, DOE/SC-ARM-TR-178, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sasze_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Photons incident on the collimator at the fore optics of the light collector travel through a large single-core optical fiber through an in-line shutter to a 50/50 bifurcated Y-fiber that diverts the signal equally to the VIS and NIR spectrometers. Within each spectrometer, light is spectrally dispersed by a diffraction grating and focused onto a solid-state linear detector array, which is read by an electronic interface that passes data to the computer via USB. Dark signals are obtained periodically at the same integration time used to measure intensity by closing the in-line shutter. Raw spectra (digital counts) are calibrated to radiance by subtracting background (shutter-closed) values and dividing by spectral responsivity determined from annual calibration against NIST-traceable integrating spheres.

**Siting.** The optical collector is located outdoors and oriented to view the zenith sky, connected via an umbilical fiber optic/electrical cable to spectrometers and data acquisition equipment located indoors in a climate-controlled building. The collector requires active heat control (Minco heating tape) and dry-air venting to prevent condensation. Type "b" collector relies on a passive 18-inch Gershun baffle tube (rather than a shadowband) to block direct sunlight unless the sun is very close to zenith. Daily cleaning of optical surfaces and a supply of desiccant/dry air are required; a robust network connection and reliable time server are needed for accurate solar ephemeris computation.

**Sampling.** native rate 1 Hz (one measurement per second during daytime); reported every 1 second; averaging the data acquisition software averages as many individual spectra as possible within a given 1-second interval (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| zenith spectral shortwave radiance (zenith_radiance) | W/(m^2 um sr) | approximately 300 nm to 1700 nm | absolute accuracy of reference standards... | - | (hb p. 7) |
| zenith_transmittance (unitless, filterbands file) | unitless | 31 selected wavelengths | - | - | (hb p. 5) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavelengths Measured | 2048 channels Si (300-1100 nm); 256 channels for the InGaAs (900-2200 nm) | (hb p. 9) |
| Instrument Field of View | 1° FWHM | (hb p. 9) |
| Sampling Interval | one per second during the day; does not collect data before sunrise or after sunset | (hb p. 10) |
| Integration Time | adjusted by site and over the course of the year to approach spectrometer dynamic range while avoiding saturation by bright cloud | (hb p. 10) |
| Avaspec ULS 2048 (VIS/Si CCD) wavelength range | about 300-1100 nm | (hb p. 7) |
| Avaspec ULS 2048 pixel spacing | less than 0.6 nm | (hb p. 7) |
| Avaspec ULS 2048 spectral resolution | about 2.4 nm FWHM | (hb p. 7) |
| Avaspec NIR256-1.7 wavelength range | about 950 nm to 1700 nm | (hb p. 7) |
| Avaspec NIR256-1.7 pixel spacing | less than 4 nm | (hb p. 7) |
| Avaspec NIR256-1.7 spectral resolution | about 6 nm FWHM | (hb p. 7) |
| Collimator field of view | 1-degree Full Width at Half Maximum (FWHM) | (hb p. 7) |
| Spectrometer thermal control | housed in refrigerator thermostatically controlled to +/- 1°F | (hb p. 8) |
| Fiber optic core | 600 um core, Low OH silica fiber, transmission 350-2500 nm | (hb p. 9) |
| Y-splitter | 600 um to two 300 micron arms | (hb p. 9) |


## The data

Verified example: **`sgpsaszenirC1.a1`**, file `sgpsaszenirC1.a1.20240530.000001.nc`
(30.42 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=26770, `wavelength`=256 |
| Data variables | 31 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-05-30T00:00:01 to 2024-05-30T23:59:58 |
| dod version | saszenir-a1-1.0 |
| process version | ingest-sasze-1.5-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ad_temperature` | degC | time | - | Temperature of avantes AD board for InGaAs NIR spectrometer |
| `band_azimuth` | degree_N | time | - | Band axis orientation with respect to north |
| `bench_temperature` | degC | time | - | Temperature of avantes optical bench for InGaAs NIR spectrometer |
| `chiller_dewpoint` | degC | time | - | Spectrometer chiller internal dew point |
| `chiller_rh` | % | time | - | Spectrometer chiller internal RH |
| `chiller_temperature` | degC | time | - | Spectrometer chiller internal temperature |
| `clock_ticks` | s | time | - | Spectrometer internal clock ticks for InGaAs NIR spectrometer |
| `collector_dewpoint` | degC | time | - | Collector internal dew point |
| `collector_rh` | % | time | - | Collector internal relative humidity from TRH sensor |
| `collector_temperature` | degC | time | - | Collector internal temperature from TRH sensor |
| `collector_x_tilt` | degree | time | - | Collector tilt along band axis |
| `collector_x_tilt_std` | degree | time | - | Standard deviation of collector tilt measured along band axis. |
| `collector_y_tilt` | degree | time | - | Collector tilt perpendicular to band axis |
| `collector_y_tilt_std` | degree | time | - | Standard deviation of collector tilt measured perpendicular to band... |
| `inner_band_angle` | degree | time | - | Inner band orientation relative to operational vertical |
| `inner_band_scattering_angle` | degree | time | - | Scattering angle occluded by point of inner band nearest to the solar... |
| `integration_time` | ms | time | - | Integration time per scan for InGaAs NIR spectrometer |
| `mio_rh` | % | time | - | MIO relative humidity from TRH sensor |
| `mio_temperature_mems` | degC | time | - | Temperature of multi-IO box from MEMS sensor |
| `mio_temperature_mems_fahr` | degF | time | - | Temperature of multi-IO box from MEMS sensor in Fahrenheit |
| `mio_temperature_trh` | degF | time | - | Temperature of MIO box from TRH sensor |
| `number_of_scans` | unitless | time | - | Number of spectrometer scans averaged for InGaAs NIR spectrometer |
| `responsivity` | (count/ms)/(W/(m^2 um... | wavelength | - | Responsivity for InGaAs NIR spectrometer |
| `solar_azimuth` | degree_N | time | - | Solar azimuth angle relative to north |
| `solar_zenith` | degree | time | - | Solar zenith angle relative to vertical zenith. |
| `time` | - | time | - | Time offset from midnight |
| `wavelength` | nm | wavelength | - | Wavelength of NIR spectrometer pixels |
| `zenith_radiance` | W/(m^2 um sr) | time,wavelength | - | Spectral zenith radiance from InGaAs NIR spectrometer |


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
                     params={"user": f"{user}:{token}", "ds": "sgpsaszenirC1.a1",
                             "start": "2024-05-30", "end": "2024-05-30", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsaszenirC1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsaszenirC1.a1", "2024-05-30", "2024-05-30")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsaszenirC1.a1", "2024-05-30", "2024-05-30"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("mio_temperature_mems")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpsaszenirC1.a1", "20110322", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are "Not available for this instrument at this time." Near-real-time diagnostic and sky radiance plots are generated by the ARM Data Quality Office and viewable via the Plot Browser; overall data quality health/status is maintained at http://dq.arm.gov/ by DQ Hands. There are currently no Value-Added Products (VAPs) or Quality Measurement Experiments (QMEs) for the SASZe.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Absolute radiance calibration uncertainty / disagreement between similarly calibrated... | Differences as large as 10% observed when comparing SASZe to other similarly calibrated instruments (SWS, Cimel sky channels, NFOV2, SSFR) measuring zenith radiance, despite reference... | Topic of current research; not yet resolved | (hb p. 6) |
| Signal-to-noise limitations of UV/VIS spectrometer near ~1000 nm | Disagreement between VIS and NIR spectrometer radiance spectra around 1000 nm overlap region | None stated | (hb p. 5) |
| Internal spectrometer stray light | Stray light levels at or below 0.01% relative to peak signal, with isolated 'hot pixels'; may approach 1% of measured spectra near wavelength detection limits of either detector | Evaluating potential corrections; not yet incorporated | (hb p. 10) |
| External stray light (e.g., direct sunlight) scattered from fore optics or leaking... | Would appear as anomalous elevated signal when comparing exposed vs shaded collector | Confirmed to be at negligible levels via exposure/shading tests | (hb p. 10) |
| Spectrometer signal nonlinearity | Nonlinearity less than 1% over most ambient light levels, approaching 5% at the lowest intensity | Evaluating corrections for robustness; not yet incorporated in current processing | (hb p. 10) |
| Spectrometer temperature sensitivity | CCD spectrometers show temperature response less than 0.1% per degree; InGaAs spectrometer shows higher sensitivity, mainly in thermal background/dark levels, with a trough (minimum) in... | Address via frequent dark measurements; operate chiller centered on the temperature-sensitivity minimum rather than coldest temperature | (hb p. 11) |
| Spectrometer/optical train polarization sensitivity | Sensitivity to 100% linearly polarized light measured at below 1% | Two OFR DPU-15 uncoated broadband depolarizers in series reduce polarization sensitivity to a few percent with 100% polarized light | (hb p. 11) |
| Optical alignment drift / baffle tube occlusion of field of view | Slow systematic downward drift in measured radiance, or rapid drop in response to severe weather/winds | Cannot currently be detected unambiguously; must be considered a possible calibration uncertainty | (hb p. 11) |
| Optical surface soiling/condensation | Condensation observed under exterior optical window, especially during MAGIC deployment and at SGP in 2011-12 before dry air supply was added | Dry air supply provided to keep optical surfaces free of condensation; effect difficult to detect unambiguously from data, considered additional... | (hb p. 11) |
| No data before sunrise or after sunset | Data gaps/blind period during nighttime hours in time series | None stated (instrument does not collect at night by design) | (hb p. 10) |
| Integration time adjustment to avoid saturation by bright cloud | Integration times vary by site and season; potential saturation under bright cloud conditions if not adjusted | Integration times adjusted by site and time of year to approach dynamic range while avoiding saturation | (hb p. 10) |
| No data quality flags currently available | Data files lack QC flag variables | None stated; 'Not available for this instrument at this time' | (hb p. 5) |
| Fiber breakage / shipping damage | Instances of broken fiber and shipping damage noted in deployment history requiring recalibration (e.g., ARCHI post-broken fiber, damaged on return shipping) | Recalibration performed post-repair (e.g., with Grande or HISS) | (hb p. 3) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Annual end-to-end radiance calibration by reference against integrating spheres at NASA Ames or NASA GSFC (using the Grande/HISS reference sources), calibrated according to NIST standards; spectral registration verified with discharge lamps and discrete laser lines; spectral resolution verified against observed... (hb p. 10) |
| Calibration interval | annual (hb p. 10) |
| Traceability | NIST standards via NASA GSFC/NASA Ames integrating spheres (hb p. 10) |
| Routine maintenance | Routine inspection and cleaning of optical surfaces, confirmation of housekeeping measurements falling in nominal ranges, and confirmation of shutter action and appearance of spectra; daily cleaning of optical surfaces; desiccant/dry air supply maintained. (hb p. 13) |
| Maintenance interval | Daily, weekly, and monthly preventative maintenance procedures (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SASHe (Shortwave Array Spectroradiometer–Hemispheric), SWS, Cimel sun photometer, NFOV2, SSFR, Rotating Shadowband Spectroradiometer (RSS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOD` | aerosol optical depth |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `ARRA` | American Recovery and Reinvestment Act |
| `ASCII` | American Standard Code for Information Interchange |
| `CCD` | charge-coupled device |
| `CWV` | column water vapor |
| `DOE` | U.S. Department of Energy |
| `FWHM` | Full Width at Half Maximum |
| `GPCI` | GEWEX/WGNE Pacific Cross-section Intercomparison |
| `GSFC` | Goddard Space Flight Center (NASA) |
| `IOP` | intensive operational period |
| `MAGIC` | Marine ARM GPCI Investigation of Clouds |
| `NASA` | National Aeronautics and Space Administration |
| `NIR` | near infrared |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sasze_handbook.pdf (20 pages, DOE/SC-ARM-TR-178, by CJ Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=sasze`, read 2026-09-23
- Example file: `sgpsaszenirC1.a1.20240530.000001.nc` from `sgpsaszenirC1.a1`, 30.42 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
