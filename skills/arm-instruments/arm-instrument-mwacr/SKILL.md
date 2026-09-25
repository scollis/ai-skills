---
name: arm-instrument-mwacr
description: ARM Marine W-Band (95 GHz) ARM Cloud Radar (mwacr) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflectivity, MeanDopplerVelocity, SpectralWidth), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (kcgmwacrcfrqcM1.b1) and the variable inventory of a real file. Use when working with mwacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - mwacr, Marine W-Band (95 GHz) ARM Cloud Radar, kcgmwacrcfrqcM1.b1, Reflectivity, MeanDopplerVelocity, SpectralWidth, Cloud Properties, ProSensing, Inc. (instrument developer), EIKA, Lidar, MMCR, NOAA.
---

# MWACR - Marine W-Band (95 GHz) ARM Cloud Radar

The WACR is a zenith-pointing 95.04 GHz Doppler radar that probes the extent and composition of clouds, reporting reflectivity, mean Doppler velocity, and spectral width for each range gate up to 15 km to determine cloud boundaries such as cloud bottoms and tops.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mwacr` |
| Handbook | [ARM-TR-073 / K. B. Widener, K. Johnson / April 2006](https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. (instrument developer); no specific model designation printed |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2012-11-01 to 2025-09-15 (retired) |
| Datastreams with data | 21 across 7 sites |
| Sites | acx, awr, kcg, mag, mar, mos, tmp |
| ARM page | https://www.arm.gov/capabilities/instruments/mwacr |


## Credit

Everything this skill knows about the instrument is the work of **K. B. Widener, K. Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K. B. Widener, K. Johnson. *W-band ARM Cloud Radar (WACR) Handbook*, ARM-TR-073, April 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/wacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `mwacr`, ARM links no handbook to this class. The facts below come from the **W-Band (95 GHz) ARM Cloud Radar** (`wacr`) handbook, which documents the parent system. The same document also covers `swacr`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `mwacr` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

The WACR works by transmitting a pulse of millimeter-wave energy from its transmitter through the antenna, which propagates through the atmosphere until it intercepts objects (clouds, precipitation, insects, spider webs, man-made objects, etc.) that reflect some of the energy back to the WACR. The same antenna receives the return signal, which is downconverted into an intermediate frequency and fed to a digital receiver. The digital receiver processes the signal and provides the radar spectra, from which power, Doppler velocity, and spectral width are calculated. The power measurement is processed using the WACR's calibration coefficient to provide radar reflectivity. Unlike the millimeter wavelength cloud radar (MMCR), the WACR does not use pulse coding and operates in only copolarization and cross-polarization modes, alternating between these two modes continuously.

**Siting.** The WACR systems are zenith pointing Doppler radars. First WACR installed at SGP in the same shelter as the 35-GHz MMCR.

**Sampling.** native rate PRF 10000 Hz (SGP/AMF); averaging Spectral Averages: 160; FFT Length: 256; Obs./Processing Time: 2.14 (units not specified) (hb p. 13).

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
| Antenna Diameter | SGP: 2 ft; AMF: 4 ft | (hb p. 12) |
| Antenna Gain | see table under Calibration History | (hb p. 12) |
| Beam Width (full-width, half-maximum) | see table under Calibration History | (hb p. 12) |
| PRF (max) | 20 kHz | (hb p. 12) |
| Pulse Repetition Frequency (Hz) - SGP/AMF | 10000 | (hb p. 13) |
| Pulse Width (microsec) - SGP/AMF | 0.3 | (hb p. 13) |
| Gate Spacing (microsec) - SGP/AMF | 0.143 | (hb p. 13) |
| Number of Gates - SGP/AMF | 348 | (hb p. 13) |
| Spectral Averages - SGP/AMF | 160 | (hb p. 13) |
| FFT Length - SGP/AMF | 256 | (hb p. 13) |
| Obs. / Processing Time - SGP/AMF | 2.14 | (hb p. 13) |
| Nyquist Velocity (m/s) - SGP/AMF | 7.885 | (hb p. 13) |
| Range gates reported up to | 15 km | (hb p. 4) |


## The data

Verified example: **`kcgmwacrcfrqcM1.b1`**, file `kcgmwacrcfrqcM1.b1.20250427.110001.nc`
(14.19 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=3114, `range`=605, `sweep`=1, `r_calib`=1, `frequency`=1 |
| Data variables | 61 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2025-04-27T11:00:01 to 2025-04-27T11:59:59 |
| dod version | mwacrcfrqc-b1-1.1 |
| process version | ingest-mwacrcfrqc-0.0-0.dev0.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_agl` | m | time | - | Altitude above ground level |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `first_usable_range_gate` | 1 | - | - | First suggested usable gate |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `frequency` | Hz | frequency | - | Transmit center frequency |
| `gps_altitude` | m | time | - | Altitude of instrument from onboard GPS |
| `gps_heading_angle` | degree_N | time | - | Angle of platform heading from onboard GPS |
| `gps_heading_magnitude` | km/hour | time | - | Speed of platform heading from onboard GPS |
| `gps_latitude` | degree_N | time | - | Latitude of instrument from onboard GPS |
| `gps_longitude` | degree_E | time | - | Longitude of instrument from onboard GPS |
| `instrument_type` | 1 | - | - | Type of instrument |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `mean_doppler_velocity_crosspolar_v` | m/s | time,range | - | Doppler velocity, crosspolar for vertical channel |
| `n_samples` | 1 | time | - | Number of Samples used to compute moments |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |
| `platform_type` | 1 | - | - | Platform type |
| `polarization_mode` | 1 | sweep | - | Polarization mode for sweep |
| `prt` | s | time | - | Pulse repetition time |
| `prt_mode` | 1 | sweep | - | Transmit pulse mode |
| `pulse_width` | s | time | - | Transmitter pulse width |
| `r_calib_dielectric_factor_used` | 1 | r_calib | - | Calibrated radar dielectric factor in use |
| `r_calib_index` | 1 | time | - | Calibration data array index per ray |
| `r_calib_probert_jones_correction` | dB | r_calib | - | Calibrated radar Probert-Jones correction factor |
| `r_calib_radar_constant_h` | dB | r_calib | - | Calibrated radar constant horizontal channel |
| `r_calib_radar_constant_v` | dB | r_calib | - | Calibrated radar constant vertical channel |
| `r_calib_receiver_gain_hc` | dB | r_calib | - | Calibrated radar receiver gain horizontal copolar channel |
| `r_calib_receiver_gain_vx` | dB | r_calib | - | Calibrated radar receiver gain vertical crosspolar channel |
| `r_calib_receiver_mismatch_loss_h` | dB | r_calib | - | Calibrated radar finite bandwidth loss horizontal channel |


_28 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "kcgmwacrcfrqcM1.b1",
                             "start": "2025-04-27", "end": "2025-04-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./kcgmwacrcfrqcM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "kcgmwacrcfrqcM1.b1", "2025-04-27", "2025-04-27")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("kcgmwacrcfrqcM1.b1", "2025-04-27", "2025-04-27"))   # cite what you pulled
```

This datastream carries 61 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "kcgmwacrcfrqcM1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["altitude_agl", "azimuth", "censor_mask"],
                                cleanup_qc=True)
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 1 sweep, 3114 rays x 605 gates, `scan_type='other'`, fixed angle 90.0 deg.

```python
import pyart
radar = pyart.io.read("kcgmwacrcfrqcM1.b1.20250427.110001.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `censor_mask`, `mean_doppler_velocity`, `mean_doppler_velocity_crosspolar_v`, `reflectivity`, `reflectivity_crosspolar_v`, `signal_to_noise_ratio_copolar_h`, `signal_to_noise_ratio_crosspolar_v`, `spectral_width`, `spectral_width_crosspolar_v`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("kcgmwacrcfrqcM1.b1", "20121101", "20260924")
```

The handbook's own note on data quality: There are three data quality flags in the wacr data stream: qc_time (checks sample time regularity: 1=within expected interval, 2=duplicate/zero delta, 4=greater than expected, 8=less than expected), qc_Reflectivity (0=within valid range, 1=missing, 2=less than valid minimum, 4=greater than valid maximum, 8=failed valid delta check relative to previous value), and qc_MeanDopplerVelocity (same coding as qc_Reflectivity). Data Quality Office website has DQ HandS, DQ HandS Plot Browser, and NCVweb tools for inspecting WACR data quality. Plots of reflectivity, Doppler radial velocity, and Doppler...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Transmitter problem causing removal from operation | Data gap in record; unit removed from operation in early August 2005 due to transmitter problem | Reinstallation occurred in December 2005 | (hb p. 5) |
| Large raw spectra data volume causing archive delay | Approximately 15 GB of raw spectra files generated per day; disks mailed to archive every few weeks, resulting in delayed availability of spectra data | Disks containing spectra files are mailed to the archive every few weeks | (hb p. 5) |
| Non-standard spectra data format | WACR spectra data are not stored in NetCDF format, but rather in binary data files consisting of a header block followed by data values | Detailed information on reading the binary spectra data format available by emailing Karen Johnson | (hb p. 5) |
| Sample time irregularities | qc_time flag values indicate duplicate sample times (Delta_time is zero), Delta_time greater than expected, or Delta_time less than expected | Flagged via qc_time field (values 1,2,4,8) | (hb p. 7) |
| Reflectivity out-of-range or missing values | qc_Reflectivity flag nonzero: value missing, less than valid minimum, greater than valid maximum, or failed valid delta check relative to previous value | Use qc_Reflectivity flag to filter data | (hb p. 8) |
| MeanDopplerVelocity out-of-range or missing values | qc_MeanDopplerVelocity flag nonzero: value missing, less than valid minimum, greater than valid maximum, or failed valid delta check relative to previous value | Use qc_MeanDopplerVelocity flag to filter data | (hb p. 8) |
| Different index of refraction for water (Kw) at 95 GHz vs 35 GHz | Reflectivity computed using Kw = 0.84 at 95 GHz, differing from Kw = 0.93 used for 35 GHz radars, affecting reflectivity comparisons between frequencies | - | (hb p. 11) |
| Non-meteorological targets detected | Returned energy can be reflected from insects, spider webs, man-made objects, etc., in addition to clouds and precipitation, appearing as spurious echoes in reflectivity/velocity data | - | (hb p. 10) |
| Sensitivity dependence on range and radar parameters | Radar sensitivity is proportional to transmit power, square of antenna gain, and square of wavelength, and inversely proportional to square of range to target; sensitivity decreases with... | - | (hb p. 10) |
| No pulse coding (unlike MMCR) | WACR operates without pulse coding and only in copolarization/cross-polarization modes, differing from MMCR data characteristics | - | (hb p. 4) |
| No Value-Added Products or Quality Measurement Experiments exist | No VAP/QME-derived quality-controlled products available for WACR at time of writing | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Several systems within the radar require calibration at regular intervals; values obtained are stored as constants, polynomials, or curves in calibration files or programs, used by software to convert raw radar moment files to range-corrected power (dBm) and reflectivity (dBZ) data in netCDF format. (hb p. 10) |
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
- Catalog record: ARM data-source index, `instrument_class_code=mwacr`, read 2026-09-24
- Example file: `kcgmwacrcfrqcM1.b1.20250427.110001.nc` from `kcgmwacrcfrqcM1.b1`, 14.19 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
