---
name: arm-instrument-swacr
description: ARM W-Band (95 GHz) ARM Cloud Radar, mounted to scan (swacr) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflectivity, MeanDopplerVelocity, SpectralWidth), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with swacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - swacr, W-Band (95 GHz) ARM Cloud Radar, mounted to scan, sgpswacrvptC1.b1, Reflectivity, MeanDopplerVelocity, SpectralWidth, Cloud Properties, ProSensing, Inc. (developer), EIKA, Lidar, MMCR, NOAA.
---

# SWACR - W-Band (95 GHz) ARM Cloud Radar, mounted to scan

The WACR is a zenith-pointing Doppler radar operating at 95.04 GHz that probes the extent and composition of clouds, primarily to determine cloud boundaries such as cloud bottoms and tops, and is deployed at fixed ARM sites (SGP, AMF).

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `swacr` |
| Handbook | [ARM-TR-073 / K. B. Widener, K. Johnson / April 2006](https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. (developer) |
| Primary measurements | Radar Doppler; Radar reflectivity |
| Record | 2009-10-05 to 2011-04-25 (retired) |
| Datastreams with data | 23 across 3 sites |
| Sites | grw, sbs, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/swacr |


## Credit

Everything this skill knows about the instrument is the work of **K. B. Widener, K. Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K. B. Widener, K. Johnson. *W-band ARM Cloud Radar (WACR) Handbook*, ARM-TR-073, April 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `swacr`, ARM links no handbook to this class. The facts below come from the **W-Band (95 GHz) ARM Cloud Radar** (`wacr`) handbook, which documents the parent system. The same document also covers `mwacr`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `swacr` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

The WACR works by transmitting a pulse of millimeter-wave energy from its transmitter through the antenna; the energy propagates through the atmosphere until it intercepts objects that reflect some of the energy back to the WACR, such as clouds, precipitation, insects, spider webs, or man-made objects. The same antenna receives the return signal, which is downconverted into an intermediate frequency and fed to a digital receiver that processes the signal to provide the radar spectra. From the radar spectra, power, Doppler velocity, and spectral width are calculated, and the power measurement is processed using the WACR's calibration coefficient to provide the radar reflectivity. The radar reports estimates for the first three spectral moments (0th = reflectivity, 1st = radial velocity, 2nd = spectral width) for each range gate up to 15 km. Unlike the millimeter wavelength cloud radar (MMCR), the WACR does not use pulse coding and operates in only copolarization and cross-polarization modes.

**Siting.** The WACR is zenith pointing. At SGP it was installed in the same shelter as the 35-GHz MMCR. Antenna diameter differs by site (SGP: 2 ft; AMF: 4 ft), which the handbook lists among specifications. Some diagnostic temperature variables are site-specific (e.g., Temp_Chiller for SGP only; Temp_Antenna_Top, Temp_Antenna_Bottom, Temp_Modulator_Control, Temp_Outside, Temp_Computer_Enclosure, Temp_Chiller_Supply, Temp_Chiller_Return for AMF only).

**Sampling.** native rate Pulse Repetition Frequency 10000 Hz; Spectral Averages 160; FFT Length 256; reported every Obs./Processing Time 2.14 (units not specified); averaging Spectral Averages 160 (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Reflectivity | dBZ | - | 0.5dB | - | (hb p. 6) |
| MeanDopplerVelocity | m/s | - | 0.1 m/s | - | (hb p. 6) |
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
| Pulse Repetition Frequency (Hz) | 10000 (SGP and AMF) | (hb p. 13) |
| Pulse Width (microsec) | 0.3 (SGP and AMF) | (hb p. 13) |
| Gate Spacing (microsec) | 0.143 (SGP and AMF) | (hb p. 13) |
| Number of Gates | 348 (SGP and AMF) | (hb p. 13) |
| Spectral Averages | 160 (SGP and AMF) | (hb p. 13) |
| FFT Length | 256 (SGP and AMF) | (hb p. 13) |
| Obs. / Processing Time | 2.14 (SGP and AMF) | (hb p. 13) |
| Nyquist Velocity (m/s) | 7.885 (SGP and AMF) | (hb p. 13) |
| Reporting range | up to 15 km | (hb p. 4) |
| Index of refraction for water (Kw) at 95 GHz | 0.84 at 95 GHz vs. 0.93 for 35 GHz | (hb p. 11) |


## The data

**No example file was verified for this instrument.** ARM Live listed files for every SWACR datastream but each download returned an HTTP error, the same failure the WACR datastreams show.

ARM's catalog lists 23 datastreams with data across 3 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "sgpswacrvptC1.b1", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
                     params={"user": f"{user}:{token}", "ds": "sgpswacrvptC1.b1",
                             "start": "2010-04-19", "end": "2010-04-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpswacrvptC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpswacrvptC1.b1", "2010-04-19", "2010-04-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpswacrvptC1.b1", "2010-04-19", "2010-04-19"))   # cite what you pulled
```

### Reading it as a radar object

Read with `act.io.arm.read_arm_netcdf`; Py-ART's readers are for the CfRadial
scanning products, not this one.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpswacrvptC1.b1", "20091005", "20260924")
```

The handbook's own note on data quality: There are three data quality flags in the wacr data stream: qc_time (checks sample time intervals: 1=within expected interval, 2=Delta_time zero/duplicate, 4=Delta_time greater than expected, 8=Delta_time less than expected), qc_Reflectivity (0=acceptable/within valid range, 1=missing, 2=less than valid minimum, 4=greater than valid maximum, 8=failed valid delta check relative to previous value), and qc_MeanDopplerVelocity (same 0/1/2/4/8 scheme as qc_Reflectivity). DQ HandS (Data Quality Health and Status), DQ HandS Plot Browser, and NCVweb are tools for inspecting and assessing WACR data...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Transmitter problem leading to removal from operation | Gap in data record; system status flag indicating non-operational; missing wacr data stream for the affected period (early August to reinstallation in December 2005 at SGP) | Reinstallation of the unit | (hb p. 5) |
| Non-meteorological targets contaminating returns | Reflectivity/velocity returns from insects, spider webs, man-made objects, or precipitation appearing in the data alongside cloud returns | - | (hb p. 10) |
| No pulse coding (unlike MMCR) | Different sensitivity/range characteristics compared to MMCR data; direct comparison between WACR and MMCR moments should account for this difference | - | (hb p. 4) |
| Copolarization/cross-polarization mode alternation | Data alternates between copol and crosspol samples (Polarization variable 0=copol/1=crosspol), so a given time step reflects only one polarization mode, visible as interleaved moments in... | - | (hb p. 6) |
| Sample time irregularities | qc_time flag values: duplicate sample times (Delta_time=0), Delta_time greater than expected, or Delta_time less than expected relative to prior sample | Use qc_time flag to identify and handle timing anomalies | (hb p. 7) |
| Reflectivity out-of-range or failed values | qc_Reflectivity flag nonzero: value missing, less than valid minimum, greater than valid maximum, or failed valid delta check relative to previous value | Use qc_Reflectivity flag to filter unacceptable values | (hb p. 8) |
| MeanDopplerVelocity out-of-range or failed values | qc_MeanDopplerVelocity flag nonzero: value missing, less than valid minimum, greater than valid maximum, or failed valid delta check relative to previous value | Use qc_MeanDopplerVelocity flag to filter unacceptable values | (hb p. 8) |
| Large raw spectra data volume and archival delay | Approximately 15 GB of raw spectra files generated per day; spectra data not available in near-real time because disks are mailed to the archive every few weeks | Disks are mailed to the archive periodically; contact instrument mentor for binary format details | (hb p. 2) |
| Spectra data stored in non-standard binary format | Spectra files are not in NetCDF format but in binary files with header block and m x n array structure, requiring special reading tools | Email Karen Johnson for detailed information on reading the binary spectra data format | (hb p. 2) |
| Different dielectric factor (Kw) at 95 GHz vs 35 GHz affecting reflectivity computation | Reflectivity values computed using Kw=0.84 at 95 GHz differ from those computed at 35 GHz (Kw=0.93), affecting direct comparison between WACR and other-frequency radars | - | (hb p. 11) |
| No Value-Added Products or Quality Measurement Experiments exist for WACR | Absence of VAP-derived quality-checked products; analysts must rely on raw/qc-flagged moments only | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Several systems within the radar require calibration at regular intervals; values obtained are stored as constants, polynomials, or curves in calibration files or programs, used by software to convert raw radar moment files to range-corrected power (dBm) and reflectivity (dBZ) data in netCDF format. (hb p. 12) |
| Calibration interval | N/A (Procedures: N/A; History: N/A) (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |
| `pyart-foundations` | the `Radar` object, fields, sweeps, IO, cmweather |
| `pyart-gatefilter-qc` | gate filtering for radar moments |

Instruments the handbook names as complements or predecessors: MMCR (millimeter wave cloud radar).

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

- Albrecht et al. 1991
- Baum et al. 1995
- Bogush 1989
- Clothiaux et al. 1995
- Currie and Brown 1987
- Dong et al. 1997
- Doviak and Zrni 1993
- Frisch et al. 1995
- Hobbs et al. 1985
- Intrieri et al. 1993

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf (17 pages, ARM-TR-073, by K. B. Widener, K. Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=swacr`, read 2026-09-24
- Example file: none - ARM Live listed files for every SWACR datastream but each download returned an HTTP error, the same failure the WACR datastreams show
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
