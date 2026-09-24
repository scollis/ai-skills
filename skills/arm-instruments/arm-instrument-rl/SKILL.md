---
name: arm-instrument-rl
description: ARM Raman Lidar (rl) - handbook-derived instrument reference: measurement principle, reported quantities (Water vapor mixing ratio, Temperature, Aerosol backscatter coefficient, Aerosol extinction, Linear depolarization ratio, Height coverage, Aerosol optical depth, Relative humidity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with rl data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols; Atmospheric Profiling; Cloud Properties. Triggers - rl, Raman Lidar, sgprlC1.a0, Water vapor mixing ratio, Temperature, Aerosol backscatter coefficient, Aerosol extinction, Linear depolarization ratio, Height coverage, Aerosols, Atmospheric Profiling, Cloud Properties, Enclosure: Orca, Laser: frequency-tripled Nd:YAG, ANSI, ARRA, CONUS, Copol.
---

# RL - Raman Lidar

The Raman lidar is a semi-autonomous, land-based, laser remote-sensing system deployed at fixed ARM sites (SGP, ENA, and formerly AMF3 Oliktok Point) that provides height- and time-resolved measurements of atmospheric water vapor mixing ratio, temperature, aerosol backscatter, extinction, and linear depolarization ratio from about 200 m to greater than 10 km AGL.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 31 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `rl` |
| Handbook | [DOE/SC-ARM-TR-038 / RK Newsom, R Bambha, D Chand / December 2022](https://www.arm.gov/publications/tech_reports/handbooks/rl_handbook.pdf) |
| Measurement category | Aerosols; Atmospheric Profiling; Cloud Properties |
| Manufacturer / model | Enclosure: Orca; Laser: frequency-tripled Nd:YAG, Continuum Inc.; Telescope: Optical Guidance Systems; Detectors: Electron Tubes 9954B PMTs; Data acquisition: Licel transient data recorders; Pulse... |
| Primary measurements |  |
| Record | 1996-06-03 to 2026-09-23 (active) |
| Datastreams with data | 9 across 5 sites |
| Sites | bnf, ena, oli, sgp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/rl |


## Credit

Everything this skill knows about the instrument is the work of **RK Newsom, R Bambha, D Chand** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> RK Newsom, R Bambha, D Chand. *Raman Lidar (RL) Instrument Handbook*, DOE/SC-ARM-TR-038, December 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/rl_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The RL transmits short pulses of ultraviolet (355 nm) laser light into the atmosphere and records the backscattered return as a function of time, with the time axis converted to range using the speed of light. As the pulse propagates, its energy is scattered elastically by aerosols and molecules (Rayleigh) and inelastically via the Raman effect, inducing vibrational and rotational transitions in molecular H2O, N2, and O2 that lead to re-emission at shifted wavelengths. Separate narrowband detection channels measure the elastic return at 355 nm and Raman backscatter from H2O (408 nm) and N2 (387 nm); water vapor mixing ratio is derived from the ratio of the H2O and N2 signals, while aerosol backscatter/extinction are derived from the elastic and N2 returns. Two additional channels measure energy in different portions of the rotational Raman spectra of N2 and O2 to derive temperature. The system uses both a narrow field of view (NFOV) for far-range discrimination above solar background and a wide field of view (WFOV) for closer-range detection.

**Siting.** The RL is housed inside an environmentally controlled shipping container enclosure, transmitting the laser beam vertically out through a roof hatch/window. RL01 (SGP, Tornado Alley) uses a hail shield on the window; other ARM RLs do not. RL02 (originally TWP/Darwin, high solar angle site) has its hatch programmed to close when the solar angle is within ~27° of zenith to prevent PMT damage; this is not needed at other sites. RL01 was relocated ~300 m at SGP C1 in 2015 to be collocated with a Doppler lidar and radar systems. RL03 was deployed at a remote arctic site (Oliktok Point, AK) where logistical and power reliability issues caused low uptime; it is planned for relocation to the...

**Sampling.** native rate 10 s time resolution, 7.5 m range resolution (raw); reported every Two raw data files per day: AM (0-12 UTC) and PM period; raw packets transmitted to ADC every 15 minutes; averaging shots_summed variables record number of laser pulses averaged per channel; derived WVMR and temperature VAPs reported at 10-minute resolution (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Water vapor mixing ratio | - | - | - | - | (hb p. 8) |
| Temperature | - | - | - | - | (hb p. 8) |
| Aerosol backscatter coefficient | - | - | - | - | (hb p. 8) |
| Aerosol extinction | - | - | - | - | (hb p. 8) |
| Linear depolarization ratio | - | - | - | - | (hb p. 8) |
| Height coverage | AGL | about 200 m to greater than 10 km | - | - | (hb p. 8) |
| Aerosol optical depth | - | - | - | - | (hb p. 9) |
| Relative humidity (derived) | - | - | - | - | (hb p. 9) |
| Aerosol scattering ratio | - | - | - | - | (hb p. 9) |
| Cloud base height | - | - | - | - | (hb p. 9) |
| Photon counts (raw, per detection channel) | counts | - | Poisson (sqrt of counts) | 10 s, 7.5 m | (hb p. 15) |
| Analog voltage (raw, per detection channel) | mV (after conversion) | - | Poisson (sqrt of value) | 10 s, 7.5 m | (hb p. 15) |


## Specifications

| parameter | value | source |
|---|---|---|
| Manufacturer (enclosure) | Orca | (hb p. 18) |
| total weight | ~11000 lbs | (hb p. 18) |
| lidar power requirement | 240 VAC single phase @ 10 A | (hb p. 18) |
| HVAC manufacturer | Daikin | (hb p. 18) |
| HVAC power requirement | 240 VAC single phase @ 50 A | (hb p. 18) |
| Laser/manufacturer | frequency-tripled Nd:YAG/Continuum | (hb p. 18) |
| Output wavelength | 355 nm | (hb p. 18) |
| Pulse generator manufacturer | Stanford Research Systems | (hb p. 18) |
| Pulse energy | ~300mJ | (hb p. 18) |
| Pulse repetition frequency | 30 Hz | (hb p. 18) |
| exit beam diameter | 13 cm | (hb p. 18) |
| exit beam divergence | ~0.1 mrad | (hb p. 18) |
| pulse width | ~5 ns | (hb p. 18) |
| Telescope diameter, f#, manufacturer | 61 cm, f/9.3, Optical Guidance Systems | (hb p. 18) |
| Wide FOV | 2 mrad | (hb p. 18) |
| Narrow FOV | 0.3 mrad | (hb p. 18) |
| Interference filters | See Table 2 | (hb p. 19) |
| Detectors | Photomultiplier tubes, electron tubes (9954B) | (hb p. 19) |
| HV supplies | LeCroy | (hb p. 19) |
| Data acquisition | Licel data recorders. Simultaneous photon counting and analog voltage measurement | (hb p. 19) |
| raw data resolution | 10s, 7.5m | (hb p. 19) |
| Enclosure outside dimensions | approximately 2.4 m high by 2.4 m wide by 6.1 m long | (hb p. 9) |
| Total system weight | approximately 5000 kg | (hb p. 9) |
| Nominal power draw | 14400VA (60 A @ 240 VAC) | (hb p. 9) |
| Window material | high-optical-quality uncoated plate glass, 6.3 mm thick, 69 cm diameter | (hb p. 9) |
| NFOV samples per profile | 4000 samples | (hb p. 13) |


_17 further specification rows are in the handbook._

## The data

**No example file was verified for this instrument.** every Raman Lidar datastream in the catalog is level a0, which ARM Live does not serve by policy.

ARM's catalog lists 9 datastreams with data across 5 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
files = armlive_list_files("sgprlC1.a0", start, end)
```

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgprlC1.a0", "2026-09-22", "2026-09-22")
ds = armlive_open("sgprlC1.a0", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `act_qc_variables(ds)` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgprlC1.a0", "19960603", "20260923")
```

The handbook's own note on data quality: Raw signals are assumed to obey Poisson statistics, with uncertainty given by the square root of the observed photon counts or analog voltage; further uncertainty propagation details are provided in the VAP documentation (Newsom et al. 2017, 2018). Engineering/diagnostic variables (Table 6), including thermocouple measurements, alignment module signals, and cloud check values, provide information on system health but are not used in generation of value-added products.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Pulse pileup effects in photon counting data | Raw photon counting data are uncorrected for pulse pileup; nonlinearity apparent at high count rates until corrected | Corrections applied by the MERGE VAP (Newsom et al. 2017) | (hb p. 13) |
| Analog voltage DC offset | Raw analog voltages show a fixed DC offset (generally 2 to 4 mV) that differs slightly between channels | Requires conversion to floating point physical units as explained in Newsom et al. 2017 | (hb p. 16) |
| Delay between analog and photon-counting signals | Short delay (several nanoseconds) in the analog signal relative to the photon counting signal, visible when comparing profiles | - | (hb p. 16) |
| Ground bin spike (multiple scattering artifact) | Prominent spike at the ground bin in elastic channel data (but not in N2 data), caused by multiple-scattered photons following strong initial ground reflection as pulse leaves lidar | - | (hb p. 17) |
| Incomplete overlap at near range (NFOV) | NFOV channels achieve complete overlap only at much higher altitude (~4 km) compared to WFOV (~800 m), limiting near-range usable data in NFOV channels | WFOV channels provide detection at closer range; NFOV/WFOV comparison figures used to assess overlap | (hb p. 21) |
| WFOV sensitivity to solar background | WFOV channels show much higher background counts/voltages than NFOV during daytime, evident as elevated baseline in time-height plots | Narrow FOV with narrowband filters used to reduce background skylight and increase maximum daytime range for derived parameters | (hb p. 21) |
| Solar/high solar angle damage risk to PMTs (RL02 at Darwin) | Reduced daily uptime during periods of high solar angle, visible as systematic dips/zeroed uptime in RL02 TWP uptime statistics | Hatch programmed to close when solar angle within ~27° of zenith | (hb p. 6) |
| Low instrument uptime / logistical downtime at remote/austere sites | RL02 at TWP averaged ~41% uptime, RL02 at ENA ~57% uptime, RL03 at Oliktok ~26-27% uptime, seen as large gaps in daily uptime time series | None specific stated beyond noting causes (logistics, power reliability, COVID-19 travel restrictions) | (hb p. 7) |
| COVID-19 pandemic related downtime | Instrument downtime in spring 2020 (RL01) and prolonged outage fall 2019 to November 2020 (RL02 ENA) due to travel restrictions delaying repairs | - | (hb p. 4) |
| System relocation/reinstallation downtime | Major downtime period in fall/winter 2015 in RL01 uptime record coinciding with system move to new container/location | - | (hb p. 4) |
| Discontinued liquid water channel | Liquid water content channel added in 2005 is no longer supported; absence of corresponding variable/data in current datastream | - | (hb p. 3) |
| Unused filter wheel flag | The 'filter' variable is a legacy flag for filter wheel position no longer used in current design; values of 1 or 2 indicate open aperture, 0 indicates closed aperture | Interpret 'filter' variable per current design convention (1/2=open, 0=closed) rather than legacy filter wheel meaning | (hb p. 14) |
| Cloud/cloudiness contamination indicator | n2_cloud_check_value and cloud_value_check engineering variables flag cloudiness based on nitrogen_high signal from 1.9-2.4 km normalized by shots and pulse energy | These are diagnostic variables not used in VAPs but can indicate cloud presence affecting signal interpretation | (hb p. 15) |
| Eye safety hazard (Class IV laser) | N/A to data but relevant to operations: risk of eye/skin damage from direct/reflected beams inside enclosure; potential MPE exceedance with multiple shot exposure (e.g., slow-moving... | Safety interlock system restricts enclosure access to authorized personnel with eye protection; system operated such that aircraft exposure to... | (hb p. 12) |
| Height/ground bin determination dependency | Height array determination depends on precise 'ground_bin' value (~300-400 pre-pulse samples) determined offline per system; errors would shift apparent range registration | ground_bin values determined through offline analysis and stored in configuration file for MERGE VAP | (hb p. 14) |
| Poisson-limited measurement uncertainty | Uncertainty in photon counts or analog voltage scales as the square root of the observed value, so low-signal (high-range or low backscatter) regions show proportionally larger noise | Uncertainties propagated through RL VAPs per Newsom et al. 2017, 2018 | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Raw return signals (photon counts, analog voltages) do not require calibration per se; derived quantities (water vapor mixing ratio, temperature, aerosol optical properties) require careful calibration as described in VAP documentation (hb p. 12) |
| Traceability | Calibration procedures described in Newsom et al. 2019, 2020 and Chand et al. 2020 (VAP documentation) (hb p. 12) |
| Routine maintenance | Major refurbishment of RL01 in 2004 (resurfaced telescope, replaced optics/filters, replaced photon-counting electronics with Licel recorders) following degraded sensitivity; boresight alignment module added April 2007 for alignment stability; ground_bin values determined offline per system and stored in configuration... (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Doppler lidar, radar systems, radiosonde (sondewnpn).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AGL` | above ground level |
| `AMF` | ARM Mobile Facility |
| `ANSI` | American National Standards Institute |
| `ARM` | Atmospheric Radiation Measurement |
| `ARRA` | American Recovery and Reinvestment Act |
| `CF` | Central Facility |
| `CONUS` | continental United States |
| `Copol` | copolarization (i.e., parallel to transmit polarization) |
| `DBS` | dichroic beam splitter |
| `depol` | depolarization (i.e., perpendicular to transmit polarization) |
| `DOE` | U.S. Department of Energy |
| `ENA` | Eastern North Atlantic |
| `FEX` | feature extraction and extinction |
| `FOV` | field of view |


### References the handbook cites

- Goldsmith et al. 1998, Applied Optics 37(21):4979-4990
- Whiteman, Melfi, Ferrare 1992, Applied Optics 31(16):3068-3082
- Whiteman et al. 2006, JTECH 23(2):157-169
- Turner and Goldsmith 1999, JTECH 16(8):1062-1076
- Turner, Feltz, Ferrare 2000, BAMS 81(6):1301-1317
- Turner et al. 2002, JTECH 19(1):37-50
- Turner and Goldsmith 2005, Fifteenth ARM Science Team Meeting Proceedings
- Turner, Goldsmith, Ferrare 2016, AMS Meteorological Monograph 57:18.1-18.15
- Ferrare et al. 2006, JGR-Atmospheres 111(D5):D05S08
- Newsom et al. 2009, Applied Optics 48(20):3903-3914

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/rl_handbook.pdf (31 pages, DOE/SC-ARM-TR-038, by RK Newsom, R Bambha, D Chand)
- Catalog record: ARM data-source index, `instrument_class_code=rl`, read 2026-09-23
- Example file: none - every Raman Lidar datastream in the catalog is level a0, which ARM Live does not serve by policy
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
