---
name: arm-instrument-wacr
description: ARM W-Band (95 GHz) ARM Cloud Radar (wacr) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflectivity, MeanDopplerVelocity, SpectralWidth), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with wacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - wacr, W-Band (95 GHz) ARM Cloud Radar, sgpwacrC1.b1, Reflectivity, MeanDopplerVelocity, SpectralWidth, Cloud Properties, ProSensing, Inc., EIKA, Lidar, MMCR, NOAA.
---

# WACR - W-Band (95 GHz) ARM Cloud Radar

The WACR is a zenith-pointing Doppler radar operating at 95.04 GHz that probes the extent and composition of clouds to determine cloud boundaries (tops and bottoms), deployed at fixed ARM sites (e.g., SGP, AMF) in the same shelter arrangement as other cloud radars.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `wacr` |
| Handbook | [ARM-TR-073 / K. B. Widener, K. Johnson / April 2006](https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. |
| Primary measurements | Radar Doppler; Radar reflectivity |
| Record | 2005-06-22 to 2017-08-14 (retired) |
| Datastreams with data | 30 across 8 sites |
| Sites | asi, fkb, grw, hfe, mao, nim, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/wacr |


## Credit

Everything this skill knows about the instrument is the work of **K. B. Widener, K. Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K. B. Widener, K. Johnson. *W-band ARM Cloud Radar (WACR) Handbook*, ARM-TR-073, April 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The WACR works by transmitting a pulse of millimeter-wave energy from its transmitter through the antenna. The energy propagates through the atmosphere until it intercepts objects that reflect some of the energy back to the WACR, such as clouds, precipitation, insects, spider webs, or man-made objects. The same antenna is used to receive the return signal, which is downconverted into an intermediate frequency and fed to a digital receiver that processes the signal to provide the radar spectra. From the radar spectra, power, Doppler velocity, and spectral width are calculated, and the power measurement is processed using the WACR's calibration coefficient to provide radar reflectivity. Radar sensitivity is proportional to transmit power, the square of antenna gain, and the square of wavelength, and inversely proportional to the square of range to the target.

**Siting.** The WACR is zenith pointing. The first WACR was installed at the Southern Great Plains (SGP) site in the same shelter as the 35-GHz MMCR. Antenna diameter differs by site (SGP: 2 ft, AMF: 4 ft), which the handbook lists separately in specifications.

**Sampling.** native rate Pulse Repetition Frequency 10000 Hz; Obs./Processing Time 2.14 (sec, implied); averaging Spectral Averages: 160; FFT Length: 256 (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Reflectivity | dBZ | - | 0.5dB | - | (hb p. 6) |
| MeanDopplerVelocity | m/s | - | 0.1 m/s | less than 0.1 m/s (Doppler... | (hb p. 6) |
| SpectralWidth | m/s | - | 0.1 m/s | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Frequency | 95 GHz (Wavelength 3.16 mm, W band) | (hb p. 12) |
| Peak Transmitted Power | 1500 W | (hb p. 12) |
| Maximum Duty Cycle | 0.1% | (hb p. 12) |
| Antenna Diameter | SGP: 2 ft, AMF: 4 ft | (hb p. 12) |
| Antenna Gain | see table under Calibration History | (hb p. 12) |
| Beam Width (full-width, half-maximum) | see table under Calibration History | (hb p. 12) |
| PRF (max) | 20 kHz | (hb p. 12) |
| Pulse Repetition Frequency (Hz) | 10000 (SGP/AMF) | (hb p. 13) |
| Pulse Width (microsec) | 0.3 | (hb p. 13) |
| Gate Spacing (microsec) | 0.143 | (hb p. 13) |
| Number of Gates | 348 | (hb p. 13) |
| Spectral Averages | 160 | (hb p. 13) |
| FFT Length | 256 | (hb p. 13) |
| Obs./Processing Time | 2.14 | (hb p. 13) |
| Nyquist Velocity (m/s) | 7.885 | (hb p. 13) |
| Maximum range gate height | up to 15 km | (hb p. 4) |


## The data

**No example file was verified for this instrument.** ARM Live listed files for every WACR datastream but each download returned an HTTP error.

ARM's catalog lists 30 datastreams with data across 8 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
files = armlive_list_files("sgpwacrC1.b1", start, end)
```

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpwacrC1.b1", "2008-09-23", "2008-09-23")
ds = armlive_open("sgpwacrC1.b1", "2008-09-23", "2008-09-23", cleanup_qc=True)
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `act_qc_variables(ds)` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpwacrC1.b1", "20050622", "20260923")
```

The handbook's own note on data quality: There are three data quality flags in the wacr data stream: qc_time (checks sample time deltas: 1=within expected interval, 2=zero/duplicate, 4=greater than expected, 8=less than expected), qc_Reflectivity, and qc_MeanDopplerVelocity (both compare values to reasonable maximum/minimum: 0=within valid range, 1=missing, 2=less than valid minimum, 4=greater than valid maximum, 8=failed valid delta check relative to previous value). Data Quality Office website has DQ HandS, DQ HandS Plot Browser, and NCVweb tools for inspecting/assessing WACR data quality. Plots of reflectivity, Doppler radial...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Transmitter problem causing operational outage | Gap in data record; removal from operation noted in deployment history (SGP, early August 2005 to December 2005) | Reinstallation of the unit after repair | (hb p. 5) |
| Large raw spectra data volume with archival delay | Approximately 15 GB of raw spectra files generated per day; spectra data not immediately available in archive | Disks containing spectra files are mailed to the archive every few weeks | (hb p. 5) |
| Spectra data stored in non-standard binary format, not NetCDF | Users cannot directly read spectra files with standard NetCDF tools; requires header block parsing (PRF, number of range gates, FFT points) plus system temperature and m x n spectrum array | Contact Karen Johnson (kjohnson@bnl.gov) for detailed information on reading the binary spectra data format | (hb p. 5) |
| Different index of refraction for water (Kw) used at 95 GHz vs 35 GHz | Reflectivity values computed with Kw=0.84 at 95 GHz differ from those computed with Kw=0.93 at 35 GHz (e.g., MMCR), causing apparent discrepancies when comparing reflectivity between W-band... | - | (hb p. 11) |
| Duplicate or irregular sample times | qc_time flag values: 2 = Delta_time is zero (duplicate sample times), 4 = Delta_time greater than expected, 8 = Delta_time less than expected | Check qc_time flag values against expected interval | (hb p. 7) |
| Reflectivity out-of-range or invalid values | qc_Reflectivity flag nonzero: 1=missing, 2=less than valid minimum, 4=greater than valid maximum, 8=failed valid delta check relative to previous value | Filter/inspect using qc_Reflectivity flag | (hb p. 8) |
| MeanDopplerVelocity out-of-range or invalid values | qc_MeanDopplerVelocity flag nonzero: 1=missing, 2=less than valid minimum, 4=greater than valid maximum, 8=failed valid delta check relative to previous value | Filter/inspect using qc_MeanDopplerVelocity flag | (hb p. 8) |
| Non-cloud targets contaminating returns | Returns in reflectivity/Doppler data attributable to insects, spider webs, man-made objects, or precipitation rather than cloud hydrometeors | - | (hb p. 10) |
| System not operational (outage) detectable via moment plots | Plots of reflectivity, Doppler radial velocity, and Doppler spectral width show anomalous or flat patterns indicating system not operational | Use plots as indicator of system operational status; reviewed weekly by instrument mentor | (hb p. 8) |
| No pulse coding used, unlike MMCR | Operational/processing differences from MMCR moments; only copolarization and cross-polarization modes available, alternating continuously | - | (hb p. 4) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Several systems within the radar require calibration at regular intervals. The values obtained from these calibrations are stored as constants, polynomials, or curves in the calibration files or programs. These are used by the software to convert raw radar moment files to range-corrected power (dBm) and reflectivity... (hb p. 10) |
| Calibration interval | N/A (Procedures: N/A; History: N/A) (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MMCR, Lidar, MPL.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `EIKA` | Extended Interaction Klystron Amplifier |
| `FFT` | fast Fourier transformation |
| `Lidar` | Light Detection and Ranging |
| `MMCR` | millimeter wave cloud radar |
| `MMW` | Millimeter wave (30GHz - 300GHz) |
| `MPL` | Micropulse LIDAR |
| `NIM` | Niamey, Niger |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `NSA` | North Slope of Alaska |
| `QC` | quality control |
| `RMSE` | root-mean-square error |
| `SGP` | Southern Great Plains |


### References the handbook cites

- Albrecht et al. 1991 - A surface-based cloud observing system
- Baum et al. 1995 - Satellite remote sensing of multiple cloud layers
- Bogush 1989 - Radar and the Atmosphere
- Clothiaux et al. 1995 - An evaluation of a 94-GHz radar for remote sensing of cloud properties
- Currie and Brown 1987 - Principles and Applications of Millimeter-Wave Radar
- Dong et al. 1997 - Microphysical and radiative properties of boundary layer stratiform clouds
- Doviak and Zrni 1993 - Doppler Radar and Weather Observations
- Frisch et al. 1995 - Measurement of stratus cloud and drizzle parameters in ASTEX
- Hobbs et al. 1985 - Evaluation of a 95-GHz radar for cloud physics research
- Intrieri et al. 1993 - A method for determining cirrus cloud particle sizes

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf (17 pages, ARM-TR-073, by K. B. Widener, K. Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=wacr`, read 2026-09-23
- Example file: none - ARM Live listed files for every WACR datastream but each download returned an HTTP error
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
