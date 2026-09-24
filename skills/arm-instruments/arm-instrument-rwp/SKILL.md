---
name: arm-instrument-rwp
description: ARM Radar Wind Profiler (rwp) - handbook-derived instrument reference: measurement principle, reported quantities (Wind speed, Wind direction, Virtual temperature, Mean Doppler shift, Spectral width, Noise level), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgp915rwppreciploC1.b1) and the variable inventory of a real file. Use when working with rwp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling. Triggers - rwp, Radar Wind Profiler, sgp915rwppreciploC1.b1, Wind speed, Wind direction, Virtual temperature, Mean Doppler shift, Atmospheric Profiling, Vaisala Corporation (915/1290 MHz RWP), Scintec Corporation (1290/915 MHz RWP), RASS, BSRWP, FMC-BL, BBSS.
---

# RWP - Radar Wind Profiler

The radar wind profiler (RWP) is an active remote-sensing instrument that measures vertical profiles of wind (and backscattered signal strength) nominally between 0.1 km and 6 km by transmitting electromagnetic pulses vertically and at oblique angles and analyzing the Doppler-shifted backscatter from clear-air turbulence, deployed unattended at fixed and mobile ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 27 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `rwp` |
| Handbook | [DOE/SC-ARM-TR-044 / P Muradyan, R Coulter / March 2020](https://www.arm.gov/publications/tech_reports/handbooks/rwp_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Vaisala Corporation (915/1290 MHz RWP); Scintec Corporation (1290/915 MHz RWP); Radiometrics / DeTect, Inc. (1290 MHz FMC-BL beam-steered RWP, BSRWP) |
| Primary measurements | Atmospheric turbulence; Backscattered radiation; Horizontal wind; Radar Doppler; Radar reflectivity; Vertical velocity |
| Record | 1996-12-30 to 2026-09-23 (active) |
| Datastreams with data | 305 across 28 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/rwp |


## Credit

Everything this skill knows about the instrument is the work of **P Muradyan, R Coulter** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> P Muradyan, R Coulter. *Radar Wind Profiler (RWP) and Radio Acoustic Sounding System (RASS) Instrument Handbook*, DOE/SC-ARM-TR-044, March 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/rwp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The RWP is a Doppler radar that sends electromagnetic pulses in the vertical and several tilted (oblique) directions and measures the signal scattered back by atmospheric turbulence (refractive index irregularities caused mainly by moisture, and to a lesser extent temperature, fluctuations) at all heights. Radial components of motion along each pointing direction are determined from the mean Doppler shift of the returned spectrum, and by combining radial velocities from at least three beams (assuming horizontal wind homogeneity over the beam separation) the three-dimensional wind vector is derived. Raw spectra are averaged and analyzed to produce moments (mean Doppler shift, spectral width, noise level, SNR) at each range gate, beam direction and power level, and these are consensus-averaged over time (nominally 1 hour) to produce reported wind profiles. When paired with a RASS, the atmosphere is seeded with an acoustic pulse and the Doppler shift of microwave energy scattered from the acoustic wavefront is used to derive virtual temperature, since the propagation speed of sound depends on both air motion and virtual temperature (c = vr + 20.05*sqrt(Tv)).

**Siting.** The RWP assumes the wind field is homogeneous over the spatial separation of the antenna beams (safe under stable conditions); antenna is oriented horizontally so the in-phase beam points vertically, with oblique beams tilted ~14 degrees from vertical in north-south and east-west planes; the vertical beam samples different heights than tilted beams due to 1/sin(elevation angle) geometry (~3% difference, e.g. 1035 m vs 1000 m nominal), which can be significant at large ranges; RWP data are volume averages over nominally 60-240 m in height by 9 degrees horizontally, so comparisons with point measurements like radiosondes will show differences.

**Sampling.** native rate Transmit pulses at about 1-10 kHz; backscatter sampled at e.g. 1 MHz; spectra averaged over dwell time of nominally 30-45 seconds per beam/power combination; reported every Time-averaged profiles usually calculated over 1 hour for ARM data (RASS operates only during first 10 minutes of the hour); averaging Consensus averaging: a percentage (e.g. 50%) of values within a defined range (e.g. 2 m/s) of each other are averaged to produce the radial wind/virtual temperature estimate (hb p. 4).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Wind speed | m/s | - | 1 m/s | - | (hb p. 15) |
| Wind direction | degrees relative to true... | - | 3 deg | - | (hb p. 15) |
| Radial wind speed / vertical velocity | m/s | - | 0.5 m/s | - | (hb p. 15) |
| Virtual temperature | degrees C (Co) | - | 0.5 K | - | (hb p. 15) |
| Backscattered signal strength / SNR | dB | - | - | - | (hb p. 8) |
| Mean Doppler shift | % of Nyquist frequency | - | - | - | (hb p. 8) |
| Spectral width | % of Nyquist frequency | - | - | - | (hb p. 8) |
| Noise level | dB | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Frequency | 915 or 1290 MHz | (hb p. 24) |
| Maximum range | 3–6 km (16 km for precipitation detection) | (hb p. 24) |
| Range gate | 0.06–1 km | (hb p. 24) |
| Pulse length | 60, 100, 200, 400 m | (hb p. 24) |
| Number of spectra per average spectrum | 1-100 | (hb p. 24) |
| Number of pulse/time domain integrations | 1-1000 | (hb p. 24) |
| Output power (Acceptance Test) | 3990 W and greater than 500 W forward/reflected for 50 MHz and 915 MHz respectively | (hb p. 19) |
| Center frequency (Acceptance Test) | 49.8 MHz and 915 MHz for 50 MHz and 915 MHz RWPs respectively | (hb p. 19) |
| Dynamic range (Acceptance Test) | at least 55 dB | (hb p. 19) |
| System sensitivity (Acceptance Test) | minimum detectable level of at least -127 dBm | (hb p. 19) |
| Range verification accuracy (Acceptance Test) | +/- 30 m | (hb p. 19) |
| Antenna size | approximately 4-m square | (hb p. 22) |
| Non-vertical beam tilt | about 14 degrees from vertical | (hb p. 22) |
| Dwell time per beam | nominally 30-45 seconds | (hb p. 23) |
| Full averaging cycle time | about three minutes | (hb p. 23) |
| Transmit pulse rate | about 1-10 kHz | (hb p. 23) |
| Backscatter sample rate | 1 MHz (e.g.) | (hb p. 23) |


## The data

Verified example: **`sgp915rwppreciploC1.b1`**, file `sgp915rwppreciploC1.b1.20190817.043113.nc`
(11.95 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=2832, `gate`=150 |
| Data variables | 27 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 6 s |
| File time span | 2019-08-17T04:31:13 to 2019-08-17T19:34:30 |
| dod version | 915rwppreciplo-b1-1.0 |
| process version | rwpprecipcal-1.1.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `beam_azimuth_angle` | degree | - | - | Beam azimuth angle from North |
| `beam_elevation_angle` | degree | - | - | Beam elevation angle from horizontal |
| `height_above_radar` | m | gate | - | Height above the radar without regard to horizontal displacement |
| `interpulse_period` | second | - | - | Interpulse Period, time between transmitted pulses |
| `num_code_bits` | 1 | - | - | Number of phase bits in transmitted coded pulse |
| `num_fft_points` | 1 | - | - | Number of FFT points in frequency domain spectra |
| `num_frequency_domain_integrations` | 1 | - | - | Number of integrated frequency domain spectra. |
| `num_time_domain_integrations` | 1 | - | - | Number of integrated time domain samples |
| `nyquist_velocity` | m/s | - | - | Unambiguous radial velocity, also known as Nyquist velocity |
| `operating_frequency_MHz` | MHz | - | - | Radar operating frequency |
| `pulse_width` | second | - | - | Duration of transmitted pulse |
| `r_calib_radar_constant` | dB | - | - | Calibration constant relative to reference of 0 dB |
| `radial_velocity` | m/s | time,gate | - | Doppler velocity power spectrum mean radial velocity, also known as... |
| `range_along_beam` | m | gate | - | Range in the radial direction from the radar to center of the range... |
| `range_resolution` | m | - | - | Range resolution |
| `reference_noise_power` | dB | - | - | Reference noise power used in calibration |
| `reflectivity_factor` | dBZ | time,gate | - | Radar reflectivity factor |
| `signal_to_noise_ratio` | dB | time,gate | - | Doppler velocity power spectrum signal-to-noise ratio with mean noise... |
| `spectrum_kurtosis` | (m/s)^4 | time,gate | - | Doppler velocity power spectrum kurtosis, also known as 4th moment,... |
| `spectrum_mean_noise_level` | dB | time,gate | - | Doppler velocity power spectrum mean noise level determined from... |
| `spectrum_skewness` | (m/s)^3 | time,gate | - | Doppler velocity power spectrum skewness, also known as 3rd moment,... |
| `spectrum_width` | m/s | time,gate | - | Doppler velocity power spectrum width, defined as 2*sqrt(spectrum... |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgp915rwppreciploC1.b1", "2019-08-17", "2019-08-17")
ds = armlive_open("sgp915rwppreciploC1.b1", "2019-08-17", "2019-08-17", cleanup_qc=True)
```

### Reading it as a radar object

Read with `act.io.arm.read_arm_netcdf`; Py-ART's readers are for the CfRadial
scanning products, not this one.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgp915rwppreciploC1.b1", "19961230", "20260923")
```

The handbook's own note on data quality: No flags are applied during data ingest of consensus-averaged winds and virtual temperatures. DQO creates monthly files identifying locations (temporally/spatially) where data should be eliminated via brute-force multi-pass comparison with neighboring points (above, below, before, after); this eliminates most questionable data, but some situations (precipitation, birds, 60-Hz noise) defy objective analysis and require monthly subjective review by the instrument mentor. Historically (procedure used to be in place) a parallel '.a2' flag datastream was produced with flags based on differences...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Wind field inhomogeneity between beams | Erroneous wind calculations when the actual wind differs between beam positions, especially under unstable/rapidly changing conditions; mitigated by averaging radial measurements over... | Radial measurements are averaged over a sufficient time period to validate the assumption of homogeneity | (hb p. 7) |
| Vertical vs tilted beam height mismatch | Vertical beam samples heights ~3% higher than tilted beams (e.g., 1035 m vs 1000 m nominal) due to 1/sin(elevation angle) geometry, which can be significant at large ranges | - | (hb p. 15) |
| Precipitation contamination of wind estimates | Large downward velocities, increased SNR extending to greater heights (e.g., up to 5 km), and adversely affected wind speed estimates especially during peak precipitation; rain shows large... | Adaptive algorithm implemented at SGP sites since 05/2018 switches profiler to precipitation-only vertical-beam mode when precipitating conditions... | (hb p. 10) |
| Migrating bird contamination | Wind direction shifts (e.g., near 2000 hours local time for ~5 hour periods) and wind speed increases of 5 m/s or more during migrating seasons (fall/spring), especially at night;... | Difficult to remove via purely objective analysis; requires subjective/manual review by instrument mentor; referenced techniques in Wilczak et al.... | (hb p. 10) |
| 60-Hz electrical noise contamination | Detected as a spurious Doppler shift corresponding to a radial wind speed of ~10 m/s, sometimes aliased into the spectrum because Nyquist frequency for winds is often near 10 m/s; raised... | Some occurrences reduced by adjusting (not changing) ground wire configuration (~75% reduction at Beaumont); maintenance on phase shifter assembly... | (hb p. 11) |
| Antenna/phase shifter corrosion degradation (ENA Scintec 1290 MHz RWP) | Degradation of sensitivity observed starting Spring 2019; antenna and phase shifter dramatically affected by heavy corrosion | Could not be repaired; required purchase and installation of new components before profiler could resume operation | (hb p. 12) |
| Phase shifter relay failure (AMF1 COMBLE deployment) | 1290 MHz RWP not switching beams during initial setup/data validation | All phase shifter relays were upgraded for the remainder of COMBLE after determining relays were affected by age and corrosion | (hb p. 12) |
| No automated data quality flags applied at ingest | Consensus-averaged winds and virtual temperatures carry no flags in the base data; erroneous-looking-good data can pass through undetected without subjective review | Instrument mentor performs monthly subjective analysis in addition to DQO brute-force multi-pass comparison with neighboring points (above, below,... | (hb p. 10) |
| Discrepancy between RWP and balloon-borne sounding system (BBSS) values | RWP and BBSS winds/temperatures disagree because RWP is a ~1 hour time average vs BBSS instantaneous grab sample; BBSS balloon drifts with mean wind and is not collocated with RWP... | - | (hb p. 12) |
| RASS vertical motion correction ambiguity during precipitation | During precipitation, detected descending motion in the acoustic signal is not due to actual air motion, making the vertical-motion-corrected virtual temperature unreliable in that situation | Both corrected and uncorrected virtual temperature are computed and reported; analyst should be cautious using corrected value during precipitation | (hb p. 6) |
| Precipitation mode limits wind measurement capability | In precipitation mode the RWP transmits only vertically with shorter averaging times and larger spectral domains, so it cannot obtain winds efficiently while in that mode | Adaptive algorithm only switches to precipitation mode when precipitating conditions are identified, restoring wind mode otherwise | (hb p. 7) |
| Data loss during factory calibration | All data during the basic factory calibration period (1-2 days) is lost at installation | - | (hb p. 20) |
| Limited on-board data storage buffering | Hard disk holds spectra and consensus files for approximately 12 days, consensus-only data for 1 year; optical disk holds spectral data for 12 months, implying data can be lost if not... | - | (hb p. 20) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Acceptance Test (AT) performed by vendor and instrument mentor immediately before instrument is put into service: output power, center frequency, Doppler direction (sign check via special control parameter file), dynamic range (greater than =55 dB), system sensitivity (greater than =-127 dBm minimum detectable level),... (hb p. 19) |
| Calibration interval | Factory calibration performed at time of installation only; no periodic mentor calibration procedures beyond comparison of data with other available data sources (a QC check, not true calibration) (hb p. 19) |
| Traceability | Performed by vendor and instrument mentor using signal generators, variable attenuators, and delay lines (hb p. 19) |
| Routine maintenance | Routine preventative maintenance (weekly, monthly, yearly) and corrective maintenance designed by the mentor for site operators, including factory-recommended inspection of antenna, clutter screen, cables and electronics; performance checks include control lights, date/time accuracy, final amplifier current, antenna... (hb p. 24) |
| Maintenance interval | Weekly, monthly, and yearly preventative maintenance; daily QC review by instrument mentor; factory calibration only at installation (1-2 days of data lost during that calibration) (hb p. 24) |


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

Instruments the handbook names as complements or predecessors: balloon-borne sounding system (BBSS)/radiosonde, cloud scanning radars, 50 MHz wind profiler.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `RWP` | radar wind profiler |
| `RASS` | radio acoustic sounding system |
| `BSRWP` | beam-steered radar wind profiler |
| `FMC-BL` | full motion control−boundary layer |
| `SNR` | signal-to-noise ratio |
| `FFT` | fast Fourier transform |
| `BBSS` | balloon-borne sounding system |
| `AT` | Acceptance Test |
| `MII` | Modulator, Intermediate Frequency and Interface |
| `FA` | final amplifier |
| `IMU` | Inertial Measurement Unit |
| `GPS` | Global Positioning System |
| `DQO` | Data Quality Office |
| `VAP` | value-added product |


### References the handbook cites

- Gage, KS, and BB Balsley. 1978. Doppler radar probing of the clear atmosphere. Bulletin of the American Meteorological Society 59(9): 1074-1094.
- Hildebrand, PH, and RS Sekhon. 1974. Objective determination of the noise level in Doppler spectra. Journal of Applied Meteorology 13(7): 808-811.
- Coulter, RL, and DJ Holdridge. 1995/1996. A three-month comparison of hourly winds and temperatures from co-located 50-MHz and 915-MHz RASS profilers.
- Pekour, MS, and RL Coulter. 1998/1999. A technique for removing the effect of migrating birds in 915-MHz wind profiler data. JAOT 16(12): 1941-1948.
- Wilczak, JM, et al. 1995. Contamination of Wind Profiler Data by Migrating Birds: Characteristics of Corrupted Data and Potential Solutions. JAOT 12(3): 449-467.
- Coulter, RL, and BM Lesht. 1997. Results of an automated comparison between winds and virtual temperatures from radiosonde and profilers. 6th ARM Science Team Meeting.
- Merritt, DA. 1995. A Statistical Averaging Method for Wind Profiler Doppler Spectra. JAOT 12(5): 985-995.
- Ecklund WL, DA Carter, and BB Balsley. 1988. A UHF Wind Profiler for the Boundary Layer.
- Angevine, WM, and JI MacPherson. 1995. Comparison of Wind Profiler and Aircraft Wind Measurements at Chebogue Point, Nova Scotia.
- Cohn, SA, and WM Angevine. 2000. Boundary layer height and entrainment zone thickness measured by lidars and wind-profiling radars.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/rwp_handbook.pdf (27 pages, DOE/SC-ARM-TR-044, by P Muradyan, R Coulter)
- Catalog record: ARM data-source index, `instrument_class_code=rwp`, read 2026-09-23
- Example file: `sgp915rwppreciploC1.b1.20190817.043113.nc` from `sgp915rwppreciploC1.b1`, 11.95 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
