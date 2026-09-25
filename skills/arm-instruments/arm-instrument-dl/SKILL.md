---
name: arm-instrument-dl
description: ARM Doppler Lidar (dl) - handbook-derived instrument reference. Measurement principle, reported quantities (Radial, Attenuated backscatter, Intensity, Nyquist velocity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpdlppiC1.b1) and the variable inventory of a real file. Use when working with dl data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - dl, Doppler Lidar, sgpdlppiC1.b1, Radial, Attenuated backscatter, Intensity, Nyquist velocity, Cloud Properties, Halo Photonics Stream Line, Stream Line Pro, MOPA, DLWSTATS.
---

# DL - Doppler Lidar

The Doppler lidar is an active remote-sensing instrument that transmits pulses of near-infrared laser energy and measures the backscattered signal to provide range- and time-resolved measurements of the line-of-sight (radial) component of air velocity and attenuated aerosol backscatter, typically deployed as a small self-contained scanning ground-based (or ship-based) system at ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 59 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `dl` |
| Handbook | [DOE/SC-ARM-TR-101 / RK Newsom, R Krishnamurthy / December 2022](https://www.arm.gov/publications/tech_reports/handbooks/dl_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Halo Photonics Stream Line, Stream Line Pro, Stream Line XR, XR+ |
| Primary measurements | Backscattered radiation; Lidar Doppler |
| Record | 2010-10-21 to 2026-09-23 (active) |
| Datastreams with data | 148 across 19 sites |
| Sites | anx, asi, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mao, mos, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/dl |


## Credit

Everything this skill knows about the instrument is the work of **RK Newsom, R Krishnamurthy** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> RK Newsom, R Krishnamurthy. *Doppler Lidar (DL) Instrument Handbook*, DOE/SC-ARM-TR-101, December 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/dl_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The DL uses a monostatic heterodyne detection technique in which pulses of near-IR (1.548 micron) laser radiation are transmitted into the atmosphere and backscattered from micron-sized aerosols; the return signal is mixed with a frequency-stable local oscillator beam, producing a modulation whose frequency indicates the Doppler shift. The range to the scatterer is inferred from the time delay between transmission and reception, while the radial velocity is determined from the Doppler frequency shift of the backscattered radiation via complex demodulation to baseband (in-phase and quadrature signals). The Doppler power spectrum for each range gate is obtained from the Fourier transform of the truncated autocovariance function (ACF) computed from the I&Q signal, and the frequency of the global maximum in the corrected spectrum gives the Doppler shift, converted to radial velocity using the wavelength. The energy content of the Doppler spectra is also used, together with a factory calibration curve, to estimate attenuated backscatter, and radial velocities are defined positive for motion away from the lidar.

**Siting.** Ground-based systems require leveling (to within 0.1°, historically via circular level on scanner plate, later via internal tilt sensor from Dec 2020) and heading calibration relative to true north using hard-target scans (Stream Line/XR) or manual arrow alignment via GPS compass (Stream Line Pro). Full hemispheric scanning systems (Stream Line, XR, XR+) are typically mounted on trailers/towers; Stream Line Pro units (limited to ±20° from zenith) are used primarily for vertical profiling. Ship-based deployment (MOSAiC) required correction for platform motion using the ARM NAV system and internal tilt sensor, with heading axis aligned by eye to the stern-to-bow line. Proximity to wind...

**Sampling.** native rate I&Q sampled at 50 MHz; pulse repetition frequency 15 kHz (Stream Line/Pro) or 10 kHz (XR/XR+); reported every Temporal resolution 0.1 to 30 sec; typical pulse integration time ~1 s (15000 pulse average for SL/Pro, 10000 for XR/XR+); averaging Averaged over prescribed number of laser pulses per pulse integration period (typically ~1 sec); vertical velocity statistics VAP uses 30-min averages (hb p. 38).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Radial (line-of-sight) velocity | m s-1 | - | typically ~10 cm/sec precision | 0.038 m/s (velocity... | (hb p. 10) |
| Attenuated backscatter | m-1 sr-1 | - | - | - | (hb p. 18) |
| Intensity (SNR+1) | unitless | - | - | - | (hb p. 18) |
| Nyquist velocity | m s-1 | 19.4 | - | - | (hb p. 46) |


## Specifications

| parameter | value | source |
|---|---|---|
| Eye safety | Class 1M | (hb p. 46) |
| Wavelength (µm) | 1.5 | (hb p. 46) |
| Laser pulse energy (µJ) | less than 100 | (hb p. 46) |
| Aperture (mm) | 50 (Stream Line Pro); 75 (Stream Line, XR, XR+) | (hb p. 46) |
| Max data acquisition range (km) | 9.6 (Stream Line Pro, Stream Line); 12 (XR, XR+) | (hb p. 46) |
| Nyquist velocity (ms-1) | 19.4 | (hb p. 46) |
| Laser pulse width | ~150 ns (22.5 m) | (hb p. 46) |
| Pulse rate (kHz) | 15 (Stream Line Pro, Stream Line); 10 (XR, XR+) | (hb p. 46) |
| Minimum range (m) | ~50 (Stream Line Pro); ~90 (Stream Line, XR, XR+) | (hb p. 46) |
| Power consumption (W) | less than  300 | (hb p. 46) |
| Volume (m3) | ~ 1 | (hb p. 46) |
| Mass (kg) | ~ 85 | (hb p. 46) |
| Temporal resolution (sec) | 0.1 to 30 | (hb p. 46) |
| Range gate size (m) | 18 to 60 | (hb p. 46) |
| Scanning | ±20o from zenith (Stream Line Pro); Upper hemisphere+ (Stream Line, XR, XR+) | (hb p. 46) |
| Enclosure | Weatherproof, temperature stabilized | (hb p. 46) |
| Sampling rate (I&Q) | 50 MHz | (hb p. 11) |
| Wavelength (raw data variable) | 1548 nm | (hb p. 11) |
| Range sample spacing | 3 m (for fs=50MHz) | (hb p. 11) |
| Maximum unambiguous range (MUR) | 10 km (Stream Line, Stream Line Pro, 15 kHz PRF); 15 km (XR, XR+, 10 kHz PRF) | (hb p. 46) |


## The data

Verified example: **`sgpdlppiC1.b1`**, file `sgpdlppiC1.b1.20260919.120017.cdf`
(0.39 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=60, `range`=400 |
| Data variables | 13 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2026-09-19T12:00:17 to 2026-09-19T12:04:18 |
| dod version | dlppi-b1-1.3 |
| process version | ingest-dl-2.33-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `radial_velocity` | m/s | time,range | yes | Radial velocity |
| `attenuated_backscatter` | 1/(m sr) | time,range | - | Attenuated backscatter |
| `azimuth` | degree | time | - | Azimuth relative to true north |
| `elevation` | degree | time | - | Beam elevation |
| `intensity` | 1 | time,range | - | Intensity (signal to noise ratio + 1) |
| `pitch` | degree | time | - | Platform pitch angle |
| `range` | m | range | - | Distance from Lidar to center of range gate |
| `roll` | degree | time | - | Platform roll angle |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgpdlppiC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpdlppiC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpdlppiC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpdlppiC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

A 2-D field over time, so pcolormesh rather than a line.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4.5))
disp.plot("radial_velocity", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
13 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_radial_velocity"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("radial_velocity", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["radial_velocity"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpdlppiC1.b1", "20101021", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data availability is characterized as the percentage of valid samples exceeding an SNR threshold of 0.008 below a given altitude (Table 24). Quicklook plots are viewable via ARM Data Quality Office's dq-plotbrowser web tool and an instrument-mentor-maintained site. Analysts are advised to apply a minimum SNR threshold (0.01 or 0.008) to filter poor-quality velocity data, and potentially an upper threshold to remove fog/cloud/hard-target contamination. Velocity precision and noise can be assessed via autocovariance analysis of staring (fpt) data using linear or model-based extrapolation...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Range ambiguity from distant targets (clouds, hard targets) beyond the maximum... | Targets beyond MUR (10 km for Stream Line/Pro, 15 km for XR/XR+) can erroneously appear at closer ranges if backscatter is sufficient | Under normal conditions return signal beyond MUR is weak so effect is small; no active correction described | (hb p. 46) |
| Small systematic radial velocity offset/bias per system | Doppler velocity derived from spectral peak shows a fixed offset unique to each serial number (Table 22 lists offsets from 0.0 to 0.5 m/s) | Add the factory-determined offset u_offset to the raw velocity estimate to obtain unbiased radial velocity | (hb p. 16) |
| Noise in Doppler spectrum / velocity measurement (random error) increasing with range and... | Observed variance exceeds true atmospheric variance; manifests as a spike at zero lag in the autocovariance of the velocity time series | Estimate and remove noise variance by extrapolating nonzero-lag autocovariance to zero lag (linear or model-based/2-3 power law extrapolation, per... | (hb p. 28) |
| SNR threshold needed to filter poor-quality velocity data | Unfiltered vertical velocity shows noisy/spurious values, especially at low SNR; artifacts can appear as sinusoidal variation with height in unfiltered vertical velocity | Apply a minimum SNR threshold (commonly 0.01 or 0.008) to filter velocities; may also need an upper threshold to remove dense fog, cloud, or... | (hb p. 18) |
| Contamination of vertical stare periods by other scan types (PPI/RHI) | White vertical bands appear in time-height plots of attenuated backscatter/velocity during periods when other scans (e.g., PPI) were being performed | None specified beyond recognizing these gaps | (hb p. 18) |
| Low data availability at arctic/polar sites | Arctic systems (0116-108 at SGP E32 and 0514-82 at NSA) show markedly lower percentage of valid samples with SNRgreater than 0.008 than other sites (Table 24) | None specified | (hb p. 21) |
| Precipitation/rain contamination of Doppler spectrum | Corrected Doppler spectrum during precipitation shows two distinct modes - one from falling raindrops (apparent fall speed) and one from air motion - global maximum may correspond to... | None specified beyond recognizing dual-mode spectra | (hb p. 14) |
| Beam pointing (heading/leveling) inaccuracy | Errors in reported azimuth/elevation relative to true beam direction affect wind direction retrievals and dual-Doppler accuracy; detected via flip test as azimuth/elevation offsets (e.g.,... | Level system (via tilt sensor since Dec 2020), determine home point via hard-target scans, perform flip test to quantify azimuth/elevation offsets;... | (hb p. 44) |
| Hard-target radial velocity bias | Non-zero mean bias and standard deviation observed for stationary hard-target radial velocity measurements at different SGP facilities (Table 26, e.g., E37 bias -5.96 cm/s, std 33.86 cm/s) | Quantified via daily hard-target scans; used to monitor/calibrate heading, not corrected in data | (hb p. 28) |
| Wind farm impacts on low-level wind measurements at SGP | Wind turbines located near SGP facilities (e.g., ~3 km south of C1) may bias low-level wind measurements, especially given prevailing southerly flow | None specified beyond awareness; impacts expected to increase with further wind farm development | (hb p. 32) |
| Raw data logging only during select IOPs due to data volume | Raw autocovariance (ACF) data not available for most time periods; only processed (b1) data routinely available | Raw data enabled only during selected intensive operational periods (IOPs) | (hb p. 8) |
| Fixed FFT resolution limits velocity resolution | Velocity resolution constrained to receiver bandwidth/NFFT (0.038 m/s for standard settings) since no interpolation between frequency bins is performed | None specified; determined by number of FFT points, wavelength, and sampling rate | (hb p. 16) |
| Ship motion effects on radial velocity (ship-based deployment) | Uncorrected ship translational motion (surge, sway, heave) and attitude changes would bias radial velocity and beam angles | Corrected using ARM NAV system data, lidar tilt sensor, and measured pitch/roll offsets and NAV-to-lidar displacement vector; uncertainty remains due... | (hb p. 44) |
| Range performance limited by processed data range-gate/temporal-resolution settings | Standard processed (1-sec, 30-m) vertical velocity shows reduced range performance compared to reprocessed data with coarser range gate/temporal resolution | Reprocess raw data using larger range gate size (e.g., 60 m) and longer temporal resolution (e.g., 10 sec) to improve range performance | (hb p. 21) |
| Precision estimate sensitivity to extrapolation method | Linear extrapolation method tends to produce smaller noise variance estimates compared to model-based (2/3 power law) extrapolation; differences increase with altitude/decreasing SNR | Handbook notes both approaches and describes a model-based alternative (Section 5.4.2) for more physically motivated fit | (hb p. 31) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Attenuated backscatter derived from range-corrected SNR using a factory-determined calibration curve (differs between Stream Line/XR models and Stream Line Pro); radial velocities require no calibration but have a small fixed factory-determined velocity offset added per system; heading/home-point calibration performed... (hb p. 40) |
| Calibration interval | Hard-target heading scans performed once per day at sites with full scanning capability; background noise measurements acquired hourly (hb p. 40) |
| Traceability | Factory calibration curves for backscatter; beam offset/heading determined and monitored by instrument mentors and onsite technicians (hb p. 40) |
| Routine maintenance | Levelness of ground-based systems routinely monitored/adjusted by onsite technicians; heading maintained via configuration file history maintained by instrument mentors; if any subcomponent of main enclosure/scanner/heat exchanger fails, entire unit must be returned to vendor for servicing. User/operations manual is... (hb p. 41) |
| Maintenance interval | Daily hard-target heading scans; hourly background noise acquisition (hb p. 41) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Raman lidar (RL), 915MHz radar wind profiler, 10-m meteorological tower anemometer (sgpmetE13.b1), ARM Navigational Location and Attitude (NAV) system, Doppler Lidar Wind Value-Added Product, Doppler Lidar Vertical Velocity Statistics Value-Added Product....

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `DL` | Doppler lidar |
| `ACF` | autocovariance function |
| `SNR` | signal-to-noise ratio |
| `PRF` | pulse repetition frequency |
| `MUR` | maximum unambiguous range |
| `LO` | local oscillator |
| `I&Q` | in-phase and quadrature signals |
| `PPI` | plan position indicator |
| `RHI` | range height indicator |
| `MOPA` | master oscillator power amplifier |
| `FFT` | fast Fourier transform |
| `AET` | After Effects Project Template (raw data format storing hourly background data) |
| `TKE` | total kinetic energy |
| `DLWSTATS` | Doppler Lidar Vertical Velocity Statistics Value-Added Product |


### References the handbook cites

- Lenschow, DH, V Wulfmeyer, and C Senff. 2000. Journal of Atmospheric and Oceanic Technology 17(10): 1330-1347
- Pearson, GN, F Davies, and C Collier. 2009. Journal of Atmospheric and Oceanic Technology 26(2): 240-250
- Frehlich, RG. 2001. Journal of Atmospheric and Oceanic Technology 18(10): 1628-1639
- Frehlich, R. 2004. Journal of Atmospheric and Oceanic Technology 21(6): 905-920
- Grund, CJ, et al. 2001. Journal of Atmospheric and Oceanic Technology 18(3): 376-393
- Manninen AJ, EJ O'Connor, V Vakkari, and T Petaja. 2016. Atmospheric Measurement Techniques 9(2): 817-827
- Newsom RK, C Sivaraman, TR Shippert, and LD Riihimaki. 2019a. Doppler Lidar Wind Value-Added Product. DOE/SC-ARM/TR-148
- Newsom RK, C Sivaraman, TR Shippert, and LD Riihimaki. 2019b. Doppler Lidar Vertical Velocity Statistics Value-Added Product. DOE/SC-ARM-TR-149
- Berg, LK, RK Newsom, and DD Turner. 2017. Journal of Applied Meteorology and Climatology 56(9): 2441-2454
- Pearson, GN, PJ Roberts, JR Eacock, and M Harris. 2002. Applied Optics 41(30): 6442-6450

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/dl_handbook.pdf (59 pages, DOE/SC-ARM-TR-101, by RK Newsom, R Krishnamurthy)
- Catalog record: ARM data-source index, `instrument_class_code=dl`, read 2026-09-23
- Example file: `sgpdlppiC1.b1.20260919.120017.cdf` from `sgpdlppiC1.b1`, 0.39 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
