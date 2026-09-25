---
name: arm-instrument-kazr
description: ARM Ka ARM Zenith Radar (kazr) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflectivity, copolar, Reflectivity, cross-polar, Mean doppler velocity, copolar, Mean doppler velocity, cross-polar, Spectral width, copolar, Spectral width, cross-polar, Signal to noise ratio, copolar, Signal to noise ratio, cross-polar), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpkazrcfrmdqcC1.b1) and the variable inventory of a real file. Use when working with kazr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - kazr, Ka ARM Zenith Radar, sgpkazrcfrmdqcC1.b1, Reflectivity, copolar, Reflectivity, cross-polar, Mean doppler velocity, copolar, Mean doppler velocity, cross-polar, Spectral width, copolar, Spectral width.
---

# KAZR - Ka ARM Zenith Radar

The KAZR is a zenith-pointing Doppler cloud radar operating at approximately 35 GHz that provides vertical profiles of clouds by measuring the first three Doppler moments (reflectivity, radial Doppler velocity, and spectral width) from near-ground to nearly 20 km altitude at fixed ARM ground sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 25 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `kazr` |
| Handbook | [DOE/SC-ARM/TR-106 / K Widener, N Bharadwaj, K Johnson / February 2012](https://www.arm.gov/publications/tech_reports/handbooks/kazr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Applied Systems Engineering (transmitter), Mercury Computers (receiver), Millitech (antenna); Instrument developed by ProSensing, Inc. |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2011-01-06 to 2026-09-23 (active) |
| Datastreams with data | 240 across 21 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, gan, guc, hou, kcg |
| ARM page | https://www.arm.gov/capabilities/instruments/kazr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj, K Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj, K Johnson. *Ka-Band ARM Zenith Radar (KAZR)*, DOE/SC-ARM/TR-106, February 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/kazr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The KAZR transmits pulses of RF energy at approximately 35 GHz from a Cassegrain parabolic reflector antenna pointed at zenith and receives the backscattered signal with a dual-channel digital receiver. It uses two pulse types: a simple burst pulse and a longer frequency-modulated chirp pulse, the latter providing greater sensitivity while retaining range resolution similar to the burst pulse, at the cost of range sidelobes that require blanking near the ground. From the received signal the system computes the first three Doppler moments-reflectivity (dBZ), mean Doppler velocity, and spectral width-at each range gate, using the meteorological radar range equation which relates received power, range, wavelength, antenna gain, pulse width, system losses, and the index of refraction factor for liquid water (Kw^2) to reflectivity (Z). Velocity spectra are also continuously recorded for each range gate. At sites with dual-polarization capability, moments are computed for both copolar and cross-polar channels.

**Siting.** Zenith-pointing installation at fixed ARM sites (SGP, NSA/Barrow, TWP Manus, TWP Darwin, AMF2). Dual-polarization measurements are only made at SGP and Barrow; Manus, Darwin, and AMF2 are single-polarization installations with different antenna diameter, beamwidth, and gain than SGP.

**Sampling.** native rate Receiver sampling rate: 120 MHz (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Reflectivity, copolar | dBZ | - | 3 dBZ | - | (hb p. 8) |
| Reflectivity, cross-polar | dBZ | - | 3 dBZ | - | (hb p. 8) |
| Mean doppler velocity, copolar | m/s | - | 0.1 m/s | 0.001 | (hb p. 8) |
| Mean doppler velocity, cross-polar | m/s | - | 0.1 m/s | 0.001 | (hb p. 8) |
| Spectral width, copolar | m/s | - | 0.1 m/s | 0.001 | (hb p. 8) |
| Spectral width, cross-polar | m/s | - | 0.1 m/s | 0.001 | (hb p. 8) |
| Signal to noise ratio, copolar | dB | - | - | 0.001 | (hb p. 6) |
| Signal to noise ratio, cross-polar | dB | - | - | 0.001 | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Transmitter type | TWTA | (hb p. 7) |
| Center frequency | 35 GHz | (hb p. 7) |
| Peak power output | ~ 200 watts | (hb p. 7) |
| Pulse width | 100 ns–20 µs | (hb p. 7) |
| Polarization | dual-polarization at the Southern Great Plains (SGP) and Barrow, single-polarization at Manus, Darwin, and the second ARM Mobile Facility (AMF2) | (hb p. 7) |
| Maximum duty cycle | 25% | (hb p. 7) |
| PRF | maximum 20 kHz | (hb p. 7) |
| Transmitter manufacturer | Applied Systems Engineering | (hb p. 7) |
| Receiver type | dual-channel digital | (hb p. 7) |
| Receiver dynamic range | greater than  80 dB | (hb p. 7) |
| Receiver noise figure | 4.5 dB | (hb p. 8) |
| Receiver sampling rate | 120 MHz | (hb p. 8) |
| Decimation factor | Adjustable | (hb p. 8) |
| Video bandwidth | Adjustable | (hb p. 8) |
| Receiver manufacturer | Mercury Computers | (hb p. 8) |
| Antenna type | Cassegrain parabolic reflector | (hb p. 8) |
| Antenna diameter | 3 m at SGP, 2m at other sites | (hb p. 8) |
| 3 dB beam width | 0.2° at SGP, 0.3° at other sites | (hb p. 8) |
| Antenna gain | 57.5 dBi at SGP, 53 dBi at other sites | (hb p. 8) |
| Cross polarization isolation | - 27 dB | (hb p. 8) |
| 2-way radome loss | less than  2.0 dB | (hb p. 8) |
| Antenna manufacturer | Millitech | (hb p. 8) |
| Range resolution | approximately 30 meters (per ARM catalog description) | (hb p. 1) |


## The data

Verified example: **`sgpkazrcfrmdqcC1.b1`**, file `sgpkazrcfrmdqcC1.b1.20251229.000010.nc`
(10.74 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=977, `range`=657, `sweep`=1, `r_calib`=1, `frequency`=1 |
| Data variables | 40 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 3 s |
| File time span | 2025-12-29T00:00:10 to 2025-12-29T01:00:16 |
| dod version | kazrcfrmdqc-b1-1.4 |
| process version | ingest-kazrcfrqc-1.1-0.dev30.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_agl` | m | - | - | Altitude above ground level |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `classification_mask` | 1 | time,range | - | Non-meteorological echo classification |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `frequency` | Hz | frequency | - | Transmit center frequency |
| `linear_depolarization_ratio` | dB | time,range | - | Linear depolarization ratio, channel unspecified |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `mean_doppler_velocity_crosspolar_v` | m/s | time,range | - | Doppler velocity, crosspolar for vertical channel |
| `n_samples` | 1 | time | - | Number of Samples used to compute moments |
| `noise_figure` | dB | time | - | Receiver noise figure estimated from noise source using y-factor... |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |
| `prt` | s | time | - | Pulse repetition time |
| `pulse_width` | s | time | - | Transmitter pulse width |
| `r_calib_radar_constant_copol` | dB | r_calib | - | Calibrated radar constant copolar |
| `r_calib_radar_constant_crosspol` | dB | r_calib | - | Calibrated radar constant crosspolar |
| `r_calib_two_way_radome_loss_h` | dB | r_calib | - | Radar calibration two way radome loss horizontal channel |
| `radar_beam_width_h` | degree | - | - | Half power radar beam width horizontal channel |
| `radar_beam_width_v` | degree | - | - | Half power radar beam width vertical channel |
| `radar_measured_sky_noise_h` | dBm | time | - | Measured sky noise, horizontal channel |
| `radar_measured_sky_noise_v` | dBm | time | - | Measured sky noise, vertical channel |
| `radar_measured_transmit_power` | dBm | time | - | Radar measured transmit peak power |
| `range` | m | range | - | Range to measurement volume |
| `receiver_gain_copol` | 1 | time | - | Receiver gain copol |
| `reflectivity` | dBZ | time,range | - | Equivalent reflectivity factor |
| `reflectivity_crosspolar_v` | dBZ | time,range | - | Equivalent reflectivity factor, crosspolar for vertical channel |
| `signal_to_noise_ratio_copolar_h` | dB | time,range | - | Signal-to-noise ratio, horizontal channel |
| `signal_to_noise_ratio_crosspolar_v` | dB | time,range | - | Signal-to-noise ratio, Cross-polar for vertical channel |
| `spectral_width` | m/s | time,range | - | Spectral width |


_7 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpkazrcfrmdqcC1.b1",
                             "start": "2025-12-29", "end": "2025-12-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpkazrcfrmdqcC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpkazrcfrmdqcC1.b1", "2025-12-29", "2025-12-29")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpkazrcfrmdqcC1.b1", "2025-12-29", "2025-12-29"))   # cite what you pulled
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 1 sweep, 977 rays x 657 gates, `scan_type='vpt'`, fixed angle 90.0 deg.

```python
import pyart
radar = pyart.io.read("sgpkazrcfrmdqcC1.b1.20251229.000010.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `censor_mask`, `classification_mask`, `linear_depolarization_ratio`, `mean_doppler_velocity`, `mean_doppler_velocity_crosspolar_v`, `reflectivity`, `reflectivity_crosspolar_v`, `signal_to_noise_ratio_copolar_h`, `signal_to_noise_ratio_crosspolar_v`, `spectral_width`, `spectral_width_crosspolar_v`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`, `classification_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpkazrcfrmdqcC1.b1", "20110106", "20260923")
```

The handbook's own note on data quality: The handbook directs users to the ARM Data Quality Reports for the latest known issues. Data quality is monitored via DQ Explorer, DQ Plot Browser, and NCVweb tools linked from the Data Quality Office website. Plots of reflectivity, Doppler radial velocity, and Doppler spectral width provide a good indicator of whether the system is operational. A separate health-and-status netCDF file (coincident with moments/spectra files) contains lock alarms, temperatures, humidities, power supply voltages, TWTA status, fault flags, and calibration/noise/gain values, updated approximately hourly....

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Range sidelobes from chirp pulse | Corruption/contamination near the ground in reflectivity, visible as spurious signal in the 'blanked' near-surface region if not removed | A 'blanked' portion is inserted at the bottom of chirp-pulse plots to remove corruption from range sidelobes generated by the chirped pulse | (hb p. 8) |
| Trade-off between sensitivity and near-ground coverage across kazrbl/kazrci/kazrge... | kazrci moments (longest chirp pulse) are most sensitive but have the deepest blanked-out region near the ground; kazrbl moments (shorter chirp) are slightly less sensitive but extend closer... | Select appropriate datastream (kazrge, kazrbl, or kazrci) depending on whether full range-to-ground coverage or maximum sensitivity is needed; Table... | (hb p. 5) |
| Burst pulse lower sensitivity | Fewer clouds visible in burst pulse (kazrge) reflectivity plots compared to chirp pulse plots at the same time/height, e.g. clouds at 8-10 km between 0200-0300 visible in chirp but not... | - | (hb p. 8) |
| Single-polarization vs dual-polarization site differences | xpol (cross-polar) variables only populated with real data at SGP and Barrow; other sites (Manus, Darwin, AMF2) will not have meaningful cross-polar moments | Check site before using xpol variables; only SGP and NSA/Barrow files contain both copol and xpol moments | (hb p. 5) |
| TWT (Traveling Wave Tube) end-of-life failure | Declining transmit power output (tx_power field) over time indicates an approaching TWT failure | Track transmit power output as indicator of failure; maintain spare TWTA at each installation and spare TWTs at SGP warehouse; replace and send... | (hb p. 10) |
| Oscillator lock alarms (120/360/1620/16560 MHz) | lock_alarm_120, lock_alarm_360, lock_alarm_1620, lock_alarm_16560 fields read 0 (unlocked) instead of 1 (locked), indicating hardware/oscillator malfunction that would degrade moment data... | Monitored via health and status files; instrument mentors review data and are notified automatically by the KAZR's built-in test (BIT) email messages | (hb p. 12) |
| Fault flags / status faults | fault_flags, twta_status_state, pdu_status_j1_logic, j2_logic fields set to non-nominal values indicating instrument faults | Reviewed by instrument mentors via health and status files | (hb p. 14) |
| Missing/undefined data values | Fields populated with missing_value = -9999.f | - | (hb p. 6) |
| qc_time bit-packed flags for irregular sample timing | qc_time bit_1 set when delta time between current and previous samples is zero; bit_2 set when delta time is less than delta_t_lower_limit (1.); bit_3 set when delta time is greater than... | Assessment for all three bits is 'Indeterminate'; comment notes how prior_sample_flag affects first-sample qc_time value | (hb p. 6) |
| Known data issues not exhaustively listed in handbook | N/A - handbook defers to external report | See the ARM Data Quality Reports for the latest list of currently known issues with KAZR data | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | See KAZR Operations Manual and ARM Calibration database. (hb p. 6) |
| Calibration interval | Cal constants (cal_constant_copol, cal_constant_xpol, rx_noise) updated on an approximately hourly basis, as new raw data files are collected. (hb p. 6) |
| Routine maintenance | Transmit power output is tracked as an indicator of impending TWT failure; a spare TWTA is kept for each radar installation to minimize downtime; spare TWTs are also kept at the SGP warehouse. When a TWT fails, the failed TWTA and a new TWT are sent to the vendor for replacement and recertification. (hb p. 10) |
| Maintenance interval | TWT advertised lifetime is 20,000 operating hours (2.3 years of continuous operation) (hb p. 10) |


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

Instruments the handbook names as complements or predecessors: MMCR, SACR, ARSCL.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement (Climate Research Facility) |
| `ARSCL` | Active Remote Sensing of Clouds |
| `C band` | frequencies between 4 GHz and 8 GHz |
| `dB` | decibel |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `DMF` | Data Management Facility |
| `DOE` | U.S. Department of Energy |
| `DQO` | Data Quality Office (ARM) |
| `GHz` | gigahertz (10^9 Hz) |
| `Hz` | hertz |
| `Ka band` | frequencies between 26.5 GHz and 40 GHz |
| `KAZR` | Ka-band ARM Zenith Radar |


### References the handbook cites

- Mead, J. 2010. MMCR Calibration Study. U.S. Department of Energy. DOE/SC-ARM/TR-088.
- Baldi, C, and J Mead. "Ka-Band ARM Zenith Radar (KAZR) System Description and Operations Manual." In progress.
- Doviak, RJ, and DS Zrnic. 1993. "Doppler Radar and Weather Observations. 2nd Edition, Academic Press.
- Bringi, VN and V Chandrasekar. 2001. "Polarimetric Doppler Weather Radar." Cambridge University Press.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/kazr_handbook.pdf (25 pages, DOE/SC-ARM/TR-106, by K Widener, N Bharadwaj, K Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=kazr`, read 2026-09-23
- Example file: `sgpkazrcfrmdqcC1.b1.20251229.000010.nc` from `sgpkazrcfrmdqcC1.b1`, 10.74 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
