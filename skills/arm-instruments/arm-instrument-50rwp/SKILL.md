---
name: arm-instrument-50rwp
description: ARM Radar Wind Profiler (50 MHz) (50rwp) - handbook-derived instrument reference: measurement principle, reported quantities (Wind speed, Wind direction, Virtual temperature, Wind profiles), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgp50rwpwindC1.b1) and the variable inventory of a real file. Use when working with 50rwp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling. Triggers - 50rwp, Radar Wind Profiler (50 MHz), sgp50rwpwindC1.b1, Wind speed, Wind direction, Virtual temperature, Wind profiles, Atmospheric Profiling, Radian Corporation, 50-MHz Radar Wind Profiler/RASS (RWP50), RASS, BBSS.
---

# 50RWP - Radar Wind Profiler (50 MHz)

The 50-MHz Radar Wind Profiler/RASS (RWP50) measures wind profiles from (nominally) 2 to 12 km and virtual temperature profiles from 2 to 4 km by transmitting electromagnetic energy into the atmosphere and measuring the strength and frequency of backscattered energy, deployed at the SGP Central Facility.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `50rwp` |
| Handbook | [ARM TR-045 / R. Coulter / November 2004](https://www.arm.gov/publications/tech_reports/handbooks/50rwp_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Radian Corporation, 50-MHz Radar Wind Profiler/RASS (RWP50) |
| Primary measurements | Backscattered radiation; Horizontal wind; Radar Doppler; Vertical velocity; Virtual temperature |
| Record | 1997-05-19 to 2006-05-04 (retired) |
| Datastreams with data | 14 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/50rwp |


## Credit

Everything this skill knows about the instrument is the work of **R. Coulter** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> R. Coulter. *Radar Wind Profiler and RASS (RWP50) Handbook*, ARM TR-045, November 2004.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/50rwp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrument transmits electromagnetic energy into the atmosphere and measures the strength (intensity/SNR) and Doppler frequency of energy backscattered from refractive index fluctuations (caused primarily by temperature fluctuations) embedded within the atmosphere, which are moving with the mean wind, to derive wind speed. Virtual temperatures are recovered by transmitting an acoustic signal vertically (RASS) and measuring the electromagnetic energy scattered from the acoustic wavefront; the propagation speed of the acoustic wave is proportional to the square root of the virtual temperature. A single phased array antenna transmits alternately along three pointing directions (one vertical, one tilted ~15 degrees south, one tilted ~14 degrees west of vertical) to determine three components of motion, assuming horizontal homogeneity since the beam components are not collocated in space. Consensus averaging is used, where a percentage of values falling within a defined range of each other are averaged to produce the radial wind estimate, which are then combined to produce the wind profile.

**Siting.** Large antenna field created by coaxial cable suspended roughly 1.5 m above a ground plane; approximately 70-m square antenna oriented horizontally so the 'in-phase' beam travels vertically. Three acoustic sources located at southwest and southeast corners and center of north edge of antenna array. Deployed at SGP Central Facility, installed and operating since April 1994.

**Sampling.** native rate Transmit pulses at about a 1- to 10-kHz rate; backscatter sampled at, for example, a 250-kHz rate; reported every 1-hour consensus averaged winds; virtual temperature profiles determined during first 10 minutes of every hour, wind profile averaged over remaining 50 minutes; averaging Dwell time nominally 30 to 45 seconds per pointing direction; system cycles through three beams at low power then three beams at high power, taking about five minutes to return to beginning of sequence; 11 to 12 beam-power combination estimates saved in a 1-hour period; RASS averaging time about 10 minutes (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Wind speed | m/s | - | 1.5 m/s (nominal accuracy) | - | (hb p. 4) |
| Radial wind components along pointing direction (e.g.,... | m/s | - | 0.75 m/s (nominal accuracy) | - | (hb p. 4) |
| Wind direction | degrees | - | 3 degrees (nominal accuracy) | - | (hb p. 4) |
| Virtual temperature | - | 2 to 4 km | 0.5 (nominal accuracy) | - | (hb p. 4) |
| Wind profiles | - | nominally 2 to 12 km | - | - | (hb p. 3) |


## Specifications

| parameter | value | source |
|---|---|---|
| Frequency | 50 MHz | (hb p. 9) |
| Maximum Range | 16 km 10 km | (hb p. 9) |
| Range Gate | 0.3-1 km | (hb p. 9) |
| Pulse Length | 250, 500, 750, 1000 m | (hb p. 9) |
| # Spectra/Ave Spectrum | 1-100 | (hb p. 10) |
| # Pulse/Time Domain Integration | 1-1000 | (hb p. 10) |
| Output Power (ATP) | 3990 W y | (hb p. 10) |
| Center Frequency (transmit) | 49.8 MHz | (hb p. 10) |
| Dynamic Range | at least 55 dB | (hb p. 10) |
| System Sensitivity (minimum detectable level) | at least -127 dBm | (hb p. 10) |
| Range verification accuracy | +/- 50 m | (hb p. 10) |
| Antenna size | approximately 70-m square | (hb p. 6) |
| Antenna height above ground plane | roughly 1.5 m | (hb p. 6) |
| Transmit pulse rate | about a 1- to 10-kHz rate | (hb p. 6) |
| Backscatter sampling rate | 250-kHz rate | (hb p. 6) |
| Range resolution from sampling | one sample every 600 m in range | (hb p. 6) |


## The data

Verified example: **`sgp50rwpwindC1.b1`**, file `sgp50rwpwindC1.b1.20010328.001042.cdf`
(0.38 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=24, `range_gate`=75, `power`=2 |
| Data variables | 72 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 3597 s |
| File time span | 2001-03-28T00:10:42 to 2001-03-28T23:10:09 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `avgint` | minutes | time,power | - | Average Interval |
| `azimuth0` | Deg relative to true... | power | - | Azimuth of Beam 0 for WINDS data |
| `azimuth1` | Deg relative to true... | power | - | Azimuth of Beam 1 for WINDS data |
| `azimuth2` | Deg relative to true... | power | - | Azimuth of Beam 2 for WINDS data |
| `azimuth3` | Deg relative to true... | power | - | Azimuth of Beam 3 for WINDS data |
| `azimuth4` | Deg relative to true... | power | - | Azimuth of Beam 4 for WINDS data |
| `bswitch` | - | power | - | Rx bandwidth switch code |
| `dir` | deg | time,range_gate,power | - | Horizontal wind direction |
| `dly` | microseconds | power | - | Delay Time |
| `elevation0` | Deg | power | - | Elevation angle of Beam 0 for WINDS data |
| `elevation1` | Deg | power | - | Elevation angle of Beam 1 for WINDS data |
| `elevation2` | Deg | power | - | Elevation angle of Beam 2 for WINDS data |
| `elevation3` | Deg | power | - | Elevation angle of Beam 3 for WINDS data |
| `elevation4` | Deg | power | - | Elevation angle of Beam 4 for WINDS data |
| `height_p` | km | range_gate,power | - | Array of heights for each power |
| `ipp` | microseconds | power | - | Interpulse Period |
| `ncns0` | Count | time,range_gate,power | - | Number of values that passed consensus, beam 0 |
| `ncns1` | Count | time,range_gate,power | - | Number of values that passed consensus, beam 1 |
| `ncns2` | Count | time,range_gate,power | - | Number of values that passed consensus, beam 2 |
| `ncns3` | Count | time,range_gate,power | - | Number of values that passed consensus, beam 3 |
| `ncns4` | Count | time,range_gate,power | - | Number of values that passed consensus, beam 4 |
| `ncoh` | Count | power | - | Number of Coherent Samples/Spectral Point |
| `nheight` | Count | power | - | Number of valid heights for each power |
| `nrcns0` | Count | time,power | - | Number of Values Required for Consensus, Beam 0 |
| `nrcns1` | Count | time,power | - | Number of Values Required for Consensus, Beam 1 |
| `nrcns2` | Count | time,power | - | Number of Values Required for Consensus, Beam 2 |
| `nrcns3` | Count | time,power | - | Number of Values Required for Consensus, Beam 3 |
| `nrcns4` | Count | time,power | - | Number of Values Required for Consensus, Beam 4 |
| `nrec0` | Count | time,power | - | Number of Spectra/ave int, Beam 0 |
| `nrec1` | Count | time,power | - | Number of Spectra/ave int, Beam 1 |


_40 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgp50rwpwindC1.b1", "2001-03-28", "2001-03-28")
ds = armlive_open("sgp50rwpwindC1.b1", "2001-03-28", "2001-03-28", cleanup_qc=True)
```

This datastream carries 72 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgp50rwpwindC1.b1", start, end,
                  keep_variables=["avgint", "azimuth0", "azimuth1"])
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
act.qc.print_dqr("sgp50rwpwindC1.b1", "19970519", "20260923")
```

The handbook's own note on data quality: No flags are applied during ingest of consensus-averaged '.a2' winds and virtual temperatures. A parallel '.b2' data stream has data flags applied based on relative values of temperatures or wind components, comparing neighboring values in space (height) and time (sequential profiles, forward and backward) against predefined limits in the netCDF metadata; flags are 1 or 0. QC frequency is daily; QC delay is instantaneous/daily; QC type includes min/max flags, graphical plots, and comparisons. Additional QC includes daily comparison with BBSS radiosonde data (mean, standard deviation, max,...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Birds contaminating radar returns (especially 915 MHz systems) | Anomalous or corrupted wind velocity values; RWP 'may be detecting birds rather than the true wind'; discrepancies with radiosonde comparisons | 50 MHz wavelength is much larger than most birds, so birds capable of significant scattering (e.g., cranes) do not normally fly at altitudes used by... | (hb p. 5) |
| Disagreement between profiler and radiosonde (BBSS) values | Wind/temperature discrepancies when comparing RWP and BBSS profiles | Understood to result from RWP being a 1-hour average vs. BBSS grab sample, non-collocation since balloon travels with mean wind, RWP volume averaging... | (hb p. 5) |
| Horizontal homogeneity assumption in wind vector derivation | Wind vector errors when atmosphere is not horizontally homogeneous, since the five beam components are not collocated in space | None stated beyond noting the assumption is used to derive the wind vector as a function of height | (hb p. 4) |
| Suspect/questionable data flagged by consensus/QC delta checks | Flag field (1 or 0) in '.b2' data stream indicating values that fail neighboring comparisons in space (height) and time (sequential profiles) against predefined limits | Flags point at suspect values; no flags applied during ingest of consensus-averaged '.a2' winds/temperatures, but parallel '.b2' stream carries flags | (hb p. 4) |
| Beam/transmit power imbalance among the three beams | Large, consistent differences in returned signal strength between beams in the lowest few acceptable range gates | Daily comparison among output power for the three beams; large consistent differences indicate transmit problems | (hb p. 7) |
| Degraded maximum height of return | Decreasing maximum height attained in 25%, 50%, and 75% of daily profiles, tracked over time | Data appended to file and plotted occasionally to determine trends indicating hardware problems | (hb p. 7) |
| Mean velocity scaling error in '.a1' files if misinterpreted | Incorrect velocity values if 'mdf' column is used directly without proper scaling | Velocity estimates determined by multiplying the 'mdf' column times the 'oband' or 'vband' values and dividing by 10,000; values are 1% of full scale... | (hb p. 6) |
| SDS ingest limitations for vertical-only mode operation | Data ingest issues or gaps when instrument operates in vertical-only mode | Listed as a current difficulty; no specific mitigation given | (hb p. 13) |
| Data storage/backup limits on instrument | Potential data loss if not retrieved within backup window | Hard disk holds spectra and consensus files for approximately 12 days, consensus-only files for 1 year; optical disk holds spectral data for 1 to 2... | (hb p. 13) |
| Data loss during basic factory calibration | Gap in data record during ATP calibration procedure | None stated; noted that all data is lost during basic factory calibration | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Acceptance Test Plan (ATP) procedures carried out by Radian personnel and instrument mentor, including output power, center frequency, Doppler direction, dynamic range, system sensitivity, and range verification checks (hb p. 10) |
| Calibration interval | Factory calibrations done at time of installation and recommended by mentor for every year; every 3 mo operating level comparison; every 2 yr antenna analysis (factory procedure); monthly RASS sources level check (hb p. 10) |
| Traceability | No explicit NIST traceability stated; only true calibration procedures carried out during ATP immediately before instruments put into service (hb p. 10) |
| Routine maintenance | Clean air filters, remove dust, check cables, inspect antenna/fences/exterior cables/guys/anchors; regular noise level checks; regular final amplifier current checks; daily data existence check; vertical time sections of winds and temperatures; continuous maximum height attained monitoring (hb p. 13) |
| Maintenance interval | Daily: check operation, verify data existence; Weekly: check data quality; Monthly: check system alignment, cables, output levels, antenna switching; Yearly: repeat ATP (hb p. 13) |


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

Instruments the handbook names as complements or predecessors: 915 MHz Radar Wind Profiler, BBSS (radiosonde), MWR (Microwave Radiometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `RASS` | Radio Acoustic Sounding System - used with the RWP to obtain virtual temperature profiles... |
| `BBSS` | Balloon-Borne Sounding System (radiosonde) used for comparison with profiler wind and... |
| `QME` | Quality Measurement Experiment - a special class of VAP that does not output geophysical... |
| `VAP` | Value-Added Product - analysis and processing of existing data products into higher-level... |
| `SNR` | Signal-to-noise ratio |
| `Consensus averaging` | A method of determining if a certain percentage (e.g., 50%) of values fall within a... |
| `ATP` | Acceptance Test Plan - factory calibration/performance procedures carried out before... |


### References the handbook cites

- Angevine, W. M., and J. I. MacPherson. 1995. Comparison of Wind Profiler and Aircraft Wind Measurements at Chebogue Point, Nova Scotia. J. Atmos. and Oceanic Tech. 12, pp. 421-426.
- Merritt, D.A. 1995. Statistical Averaging Method for Wind Profiler Doppler Spectra. J. Atmos. and Oceanic Tech. 12, pp. 985-995.
- Nastrom, G.D., and F.D. Eaton. 1995. Variations of Winds and Turbulence seen by the 50-MHz Radar at White Sands Missile Range, New Mexico. Journ. Appl. Meteorol. 10, pp. 2135-2148.
- Wilczak, J. M., and collaborators. 1995. Contamination of Wind Profiler Data by Migrating Birds: Characteristics of Corrupted Data and Potential Solutions. J. Atmos. and Oceanic Tech. 12, pp. 449-467.
- Williams, C.R., W.L. Ecklund, and K.L. Gage. 1995. Classification of Precipitating Clouds in the Tropics Using 915-MHz Wind Profilers. J. Atmos. and Oceanic Tech. 12, pp. 996-1012.
- Ecklund, W.L., D.A. Carter, and B.B. Balsley. 1988. A UHF Wind Profiler for the Boundary Layer: Brief Description and Initial Results. J. Atmos. Oceanic Technol. 5, pp. 432-441.
- Ecklund, W.L., D.A. Carter, B.B. Balsley, P.E. Currier, J.L. Green, B.L. Weber, and K.S. Gage. 1990. Field Tests of a Lower Tropospheric Wind Profiler. Radio Sci. 25, pp. 899-906.
- Coulter and Lesht, 'Results of an Automated Comparison Between Winds and Virtual Temperatures from Radiosonde and Profilers', Proceedings of the Sixth Atmospheric Radiation Measurement (ARM) Science Team Meeting,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/50rwp_handbook.pdf (17 pages, ARM TR-045, by R. Coulter)
- Catalog record: ARM data-source index, `instrument_class_code=50rwp`, read 2026-09-23
- Example file: `sgp50rwpwindC1.b1.20010328.001042.cdf` from `sgp50rwpwindC1.b1`, 0.38 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
