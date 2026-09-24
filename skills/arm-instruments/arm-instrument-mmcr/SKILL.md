---
name: arm-instrument-mmcr
description: ARM Millimeter Wavelength Cloud Radar (mmcr) - handbook-derived instrument reference. Measurement principle, reported quantities (Reflectivity, MeanDopplerVelocity, SpectralWidth, CircularDepolarizationRatio, Overall measurement accuracy, Doppler resolution), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmmcrmomC1.b1) and the variable inventory of a real file. Use when working with mmcr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - mmcr, Millimeter Wavelength Cloud Radar, sgpmmcrmomC1.b1, Reflectivity, MeanDopplerVelocity, SpectralWidth, CircularDepolarizationRatio, Overall measurement accuracy, Doppler resolution, Cloud Properties, ACRF, ARCS, ARSCL, CUDC.
---

# MMCR - Millimeter Wavelength Cloud Radar

The MMCR is a zenith-pointing 35 GHz (Ka-band) radar deployed at fixed ARM sites that determines cloud boundaries (bottoms and tops), radar reflectivity of the atmosphere up to 20 km, and Doppler cloud-constituent vertical velocities.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mmcr` |
| Handbook | [ARM TR-018 / K. Johnson / January 2005](https://www.arm.gov/publications/tech_reports/handbooks/mmcr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | First five MMCRs built by NOAA Environment Technology Laboratory (ETL); sixth radar built by Radian International. Components include Applied Systems Engineering TWTA, Spacek Labs Coherent Up/Down... |
| Primary measurements | Radar Doppler; Radar reflectivity; Vertical velocity |
| Record | 1996-11-07 to 2021-06-04 (retired) |
| Datastreams with data | 38 across 5 sites |
| Sites | nsa, sgp, smt, twp, yeu |
| ARM page | https://www.arm.gov/capabilities/instruments/mmcr |


## Credit

Everything this skill knows about the instrument is the work of **K. Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K. Johnson. *Millimeter Wave Cloud Radar (MMCR) Handbook*, ARM TR-018, January 2005.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mmcr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The MMCR transmits a pulse of millimeter-wave energy from its transmitter through the antenna, which propagates through the atmosphere until it hits objects (clouds, precipitation, insects, spider webs, man-made objects, etc.) that reflect some energy back. The same antenna receives the return signal, which is split into two channels, I (in-phase) and Q (quadrature). A digital signal processor processes these signals to provide power, Doppler velocity, and spectral width. The power measurement is processed using the MMCR's calibration coefficient to yield radar reflectivity. Per the meteorological radar range equation, sensitivity is proportional to transmit power, the square of antenna gain, and the square of wavelength, and inversely proportional to the square of range to the target.

**Siting.** The radar is a zenith-pointing instrument. The radar is located at approximately 318 m MSL (SGP example), and the lowest measurement height in the data is computed as height above ground level plus site altitude (e.g., 105 m AGL + 318 m = 423 m MSL). Siting affects the minimum measurable height and susceptibility to non-hydrometeor clutter (e.g., insects, vegetation, dust), which is often seen at low levels at the SGP site.

**Sampling.** native rate combined dwell and processing times of approximately 9 seconds per mode (historical, 4-mode cycle); ~2 seconds per mode with new C40 processor; reported every Historical NSA/SGP/TWP: full 4-mode sequence ~9s per mode; Current NSA: full 8-mode sequence in just under 18 seconds; Current SGP: full sequence of ~2s per mode completing in about 32.5 seconds; averaging Coherent and spectral averages per mode as listed in Table 7 (e.g., 10/6/6/1 coherent averages; 64/21/60/29 spectral averages); hourly averages for PeakTransmittedPowerAvg and MinimumDetectableReflectivity (hb p. 15).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Reflectivity | dBZ | atmosphere up to 20 km | 0.5 dB (0.5dB / 0.5 dB) | - | (hb p. 6) |
| MeanDopplerVelocity | m/s | - | 0.1 m/s | - | (hb p. 6) |
| SpectralWidth | m/s | - | 0.1 m/s | - | (hb p. 6) |
| CircularDepolarizationRatio | dB | - | - | - | (hb p. 6) |
| Overall measurement accuracy | dB | over receiver dynamic range | 0.5 dB | - | (hb p. 7) |
| Doppler resolution | m/s | - | - | less than 0.1 meters/second | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Frequency | 34.86 GHz (Wavelength 8.66mm, Ka-band) | (hb p. 15) |
| Peak Transmitted Power | 100 W | (hb p. 15) |
| Maximum Duty Cycle | 25% | (hb p. 15) |
| Antenna Diameter | see table under Calibration History | (hb p. 15) |
| Antenna Gain | see table under Calibration History | (hb p. 15) |
| Beam Width (full-width, half-maximum) | see table under Calibration History | (hb p. 15) |
| PRF (max) | 20 kHz | (hb p. 15) |
| Inter-Pulse Period (microsec) [Mode 1 Stratus/2 Cirrus/3... | 68 / 126 / 106 / 106 | (hb p. 16) |
| Pulse Width (microsec) | 0.3 / 0.6 / 0.6 / 0.6 | (hb p. 16) |
| Gate Spacing (microsec) | 0.3 / 0.6 / 0.6 / 0.6 | (hb p. 16) |
| Number of Gates | 110 / 167 / 167 / 167 | (hb p. 16) |
| Coherent Averages | 10 / 6 / 6 / 1 | (hb p. 16) |
| Spectral Averages | 64 / 21 / 60 / 29 | (hb p. 16) |
| FFT Length | 64 / 64 / 64 / 128 | (hb p. 16) |
| Coded Bits | 8 / 32 / 0 / 0 | (hb p. 16) |
| Dwell Time (sec) | 0.7 / 0.6 / 1.0 / 0.7 | (hb p. 16) |
| Obsv./Processing Time (sec) | 9 / 8.7 / 8.5 / 9 | (hb p. 16) |
| Minimum Detectable Signal (dBm) | ~ -132 / ~ -132 / ~ -132 / ~ -132 | (hb p. 16) |
| Antenna: 2m diameter, ARCS-1 Albuquerque | Gain 53.37 dBi, Beam Width 0.32˚ | (hb p. 18) |
| Antenna: 2m diameter, SHEBA | Gain 53.48 dBi, Beam Width 0.30˚ | (hb p. 18) |
| Antenna: 2m diameter, ARCS-2 Nauru | Gain 52.73 dBi, Beam Width 0.31˚ | (hb p. 18) |
| Antenna: 2m diameter, Barrow, AK | Gain 53.37 dBi, Beam Width 0.31˚ | (hb p. 18) |
| Antenna: 3m diameter, SGP | Gain 57.48 dBi, Beam Width 0.19˚ | (hb p. 18) |
| Index of refraction for water used to compute reflectivity... | 0.98 | (hb p. 13) |


## The data

Verified example: **`sgpmmcrmomC1.b1`**, file `sgpmmcrmomC1.b1.20110101.000011.cdf`
(337.88 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

**Reading note.** use_base_time=True with combine="nested" (a non-indexed coordinate blocks combine_by_coords).

|  |  |
|---|---|
| Dimensions | `time`=62816, `mode`=10, `hourly`=24, `heights`=167 |
| Data variables | 45 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2011-01-01T00:00:11 to 2011-01-01T23:59:59 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `time` | - | time | yes | Time offset from midnight |
| `AvgNoiseLevel` | dB | time | - | Average Noise Level (S/Nless than 0) |
| `CalCheckLevel` | dB | time,mode | - | Receiver Cal Check Level |
| `CalCheckTime` | s | time,mode | - | Receiver Cal Check Time Stamp |
| `CircularDepolarizationRatio` | dB | time,heights | - | Circular Depolarization Ratio |
| `ClutterHeight` | m | time,mode | - | Max. height of clutter removal |
| `DCFilterONOFF` | count | time,mode | - | DC Filtering ON-OFF Status |
| `DataQualityStatus` | code | time | - | Data Quality Status |
| `GateSpacing` | ns | time,mode | - | Gate Spacing |
| `InterPulsePeriod` | ns | time,mode | - | Inter-Pulse Period |
| `MeanDopplerVelocity` | m/s | time,heights | - | Mean Doppler Velocity |
| `MinimumDetectableReflectivity` | dBZ | time,hourly,mode,heights | - | Minimum detectable reflectivity |
| `ModeDescription` | unitless | time,mode | - | radar mode char identifier |
| `ModeNum` | count | time | - | Operating Set for this Record |
| `NoiseLevel` | dB | time,heights | - | Mean Noise Level |
| `NumCodeBits` | count | time,mode | - | Number of Code Bits |
| `NumCoherentIntegrations` | count | time,mode | - | Number of Coherent Integrations |
| `NumFFT` | count | time,mode | - | Number of Points in FFT |
| `NumHeights` | count | time,mode | - | Number of Range Gates |
| `NumReceivers` | count | time,mode | - | Number of Receiver |
| `NumSpectralAverages` | count | time,mode | - | Number of Spectral Averages |
| `NyquistVelocity` | m/s | time,mode | - | Nyquist Velocity |
| `PeakTransmittedPowerAvg` | dBm | time,hourly | - | Peak transmitted power, averaged over the course of the hour |
| `Power` | dB | time,heights | - | Power (uncalibrated) |
| `PulseWidth` | ns | time,mode | - | Pulse Width |
| `RadarConstant` | dB | time,hourly,mode | - | Radar Constant |
| `RangeCorrectedPower` | dBm | time,heights | - | Range Corrected Calibrated Power |
| `ReceiverMode` | count | time,mode | - | Receiver Mode |
| `ReceiverNumber` | count | time,mode | - | Current Receiver Number |
| `Reflectivity` | dBZ | time,heights | - | Reflectivity |


_11 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmmcrmomC1.b1", "2011-01-01", "2011-01-01")
ds = armlive_open("sgpmmcrmomC1.b1", "2011-01-01", "2011-01-01", cleanup_qc=True)
```

This datastream carries 45 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpmmcrmomC1.b1", start, end,
                  keep_variables=["time", "AvgNoiseLevel", "CalCheckLevel", "qc_time"])
```

### Reading it as a radar object

Read with `act.io.arm.read_arm_netcdf`; Py-ART's readers are for the CfRadial
scanning products, not this one.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

1 `qc_` companion variables cover 0 of the
45 data variables. Assessments present in the example file: .

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpmmcrmomC1.b1", "19961107", "20260923")
```

The handbook's own note on data quality: DataQualityStatus (mmcrmom stream) flags per time value whether Reflectivity and RangeCorrectedCalibratedPower exist and how they were calibrated (1=no values, 2=abbreviated calibration, 4=default radar constant, 8=TWT fault/possible lost data). qc_time flags sample-time interval anomalies (1=expected, 2=duplicate, 4=greater than expected, 8=less than expected). TWTStatusCode reports hourly percentage of acceptable TWT peak power and retry counts. Data reviews by the Instrument Mentor are done weekly; DQ HandS (Data Quality Health and Status), DQ HandS Plot Browser, and NCVweb are DQO tools...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Non-hydrometeor clutter | Areas of enhanced/spurious reflectivity typically from insects, bits of vegetation or dust, often seen at low levels at the SGP site; can be difficult to distinguish from hydrometeor echoes | The ARSCL VAP generally does a good job of identifying and eliminating clutter echoes | (hb p. 10) |
| Bright band | Area of enhanced reflectivity caused by melting ice particles, appears as a distinct layer in reflectivity plots | - | (hb p. 10) |
| Pulse-coding artifacts in Mode 2 (Cirrus) | Spiked artifacts in the presence of strong reflectivity gradients caused by imperfect pulse decoding; can contaminate adjacent areas with weaker returns | - | (hb p. 10) |
| Mode-dependent sensitivity/coverage tradeoffs | Mode 1 (Boundary Layer) samples only lowest kilometers but is more sensitive there; Mode 2 (Cirrus) most sensitive above 3 km but has pulse-coding artifacts; Mode 3 (General) less sensitive... | - | (hb p. 10) |
| Receiver saturation during light precipitation | High reflectivity regions such as drizzle can saturate the receiver in less-tolerant modes | A new precipitation mode was added at SGP with about 27 dB of additional loss in the receiver to reduce receiver saturation during light precipitation | (hb p. 16) |
| Minimum measurable height / near-surface blind range | Data below the computed minimum measurement height (e.g., ~423 m MSL at SGP for Mode 1) are unavailable, limited by system delays (StartGateDelay, RxDelay) | Compute Min. Meas. Hgt = 0.5(StartGateDelay - RxDelay) x c; account for site MSL altitude | (hb p. 12) |
| Pulse coding renders low gates useless | First n-1 heights are useless where n is the number of coded bits (e.g., 8-bit code renders first 360 m of enhanced-resolution data unusable, pushing first usable data to ~465 m AGL) | - | (hb p. 12) |
| TWT (Traveling Wave Tube) faults / retries | TWTStatusCode field shows percentage of time TWT power was within acceptable bounds and number of retries per time window; possible lost data flagged via DataQualityStatus=8 (TWT fault... | After 5 retries the TWT is shut down due to a fault; monitor TWTStatusCode | (hb p. 8) |
| Data quality/calibration degradation flags (DataQualityStatus) | DataQualityStatus value of 1 = no Reflectivity/RangeCorrectedCalibratedPower values; 2 = abbreviated calibration applied (Calibrated Power = f(RxGain)); 4 = default radar constant used (no... | Check DataQualityStatus field for each time value | (hb p. 8) |
| Sample-timing irregularities (qc_time) | qc_time flag: 2 = duplicate sample times (Delta_time zero); 4 = Delta_time greater than expected; 8 = Delta_time less than expected | Inspect qc_time field for anomalous time steps | (hb p. 9) |
| Data stream format change over time | MMCR data streams change from 'mmcrcal'/'mmcrmoments' to a single 'mmcrmom' stream after processor upgrade (SGP 2003.09.09, NSA 2004.04.13); field definitions differ between old and new... | See MMCR Data Stream Format Changes comparison document for field differences | (hb p. 12) |
| Polarization mode change at SGP | Prior to 2004.08.11 SGP transmits/receives at same (non-adjustable) polarization; from 2004.08.11 onward SGP alternates polarization horizontal-to-vertical pulse to pulse, altering... | - | (hb p. 13) |
| Spectral data volume and archive lag | mmcrspecmom spectral data (~8 GB/day) available only at upgraded sites (SGP, NSA); archive availability lags collection by several weeks due to periodic disk shipment | Order limited date ranges (a few hours to a few days) via web interface | (hb p. 12) |
| TWT lifetime limitation | Advertised TWTA lifetime is 20,000 hours (~2.3 years of continuous operation), after which transmitter tube may need replacement, potentially causing gaps or power degradation | - | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration constants (inclinometer, RF noise diode, receiver path loss, transmitter path loss, TWT RF test point, forward power monitor, RF attenuator, IF attenuator, radar parameters, noise diode path loss, antenna gain, receiver bandwidth, range delay, coded pulse loss) are stored as constants, polynomials, or... (hb p. 17) |
| Calibration interval | Varies by component: Inclinometer 120 months; RF noise diode 12 months; Receiver Path Loss 12 months; Transmitter Path Loss 12 months; TWT RF Test Point 60 months; Forward Power Monitor 36 months; RF Attenuator 36 months; IF Attenuator 36 months; Radar Parameters 6 months; Noise Diode Path Loss 36 months; Antenna Gain... (hb p. 17) |
| Routine maintenance | Semi-autonomous operation: operator required only to power up and power down the system; once powered up, MMCR automatically enters standby mode ready to take data. SGP Preventative Maintenance Procedures and Preventive/Corrective Maintenance Logs are available online for SGP site instruments. (hb p. 14) |


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

Instruments the handbook names as complements or predecessors: MPL LIDAR (Micropulse Lidar), Vaisala ceilometer (VCEIL), ARSCL VAP.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAO` | Adjacent Arctic Ocean |
| `ACRF` | ARM Climate Research Facility |
| `AGL` | above ground level |
| `ARCS` | Atmospheric Radiation and Cloud Station |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `ARSCL` | Active Remote Sensing Cloud Layer |
| `CUDC` | Coherent Up/Down Converter |
| `DMF` | Data Management Facility |
| `DOE` | U.S. Department of Energy |
| `DQO` | Data Quality Office |
| `ETL` | Environment Technology Laboratory (NOAA) |
| `IF` | intermediate frequency |
| `LIDAR` | light detection and ranging |
| `MMCR` | millimeter cloud radar |


### References the handbook cites

- Moran, K.P., B.E. Martner, DC Welsh, DA Merritt, MJ Post, and T Uttal. 1997. "ARM's cloud-profiling radar." Proceedings of the 28th Conf. on Radar Meteorology, Austin, TX.
- Clothiaux, E.E., M.A. Miller, B.A. Albrecht, T.A. Ackerman, J. Verlinde, D.M. Babb, R.M. Peters, and W.J. Syrett. 1995. "An evaluation of a 94-GHz radar for remote sensing of cloud properties." J. Atmos.Ocean.Tech....
- Post, M.J., K.P. Moran, and B Martner. 1996. Contractors for the Department of Energy ARM Program Millimeter-Wave Radars. Environmental Technology Laboratory, ERL, NOAA.
- Doviak, R.J., and D.S. Zrni. 1993. "Doppler Radar and Weather Observations." 2 ed., Academic Press, p. 562.
- Probert-Jones, J.R. 1962. "The radar equation in meteorology." Quart. J. Roy. Met. Soc. 88:485-495.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mmcr_handbook.pdf (22 pages, ARM TR-018, by K. Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=mmcr`, read 2026-09-23
- Example file: `sgpmmcrmomC1.b1.20110101.000011.cdf` from `sgpmmcrmomC1.b1`, 337.88 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
