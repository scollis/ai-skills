---
name: arm-instrument-hsrl
description: ARM High Spectral Resolution Lidar (hsrl) - handbook-derived instrument reference. Measurement principle, reported quantities (Optical depth, Extinction coefficient, Backscattering coefficient, Depolarization, Backscatter phase function), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgphsrlscanC1.a1) and the variable inventory of a real file. Use when working with hsrl data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Cloud Properties. Triggers - hsrl, High Spectral Resolution Lidar, sgphsrlscanC1.a1, Optical depth, Extinction coefficient, Backscattering coefficient, Depolarization, Backscatter phase function, Aerosols, Cloud Properties, HSRL, STORMVEX, AMIE, MAGIC.
---

# HSRL - High Spectral Resolution Lidar

The HSRL provides vertical profiles of optical depth, extinction coefficient, backscattering coefficient, and depolarization of clouds and aerosols by transmitting laser pulses at 532 nm (and 1064 nm) and measuring the Doppler-broadened molecular and narrow aerosol backscatter returns, deployed at fixed ARM sites and mobile facilities.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `hsrl` |
| Handbook | [DOE/SC-ARM-TR-157 / R Bambha, J Garcia, I Razenkov, E Eloranta / September 2025](https://www.arm.gov/publications/tech_reports/handbooks/hsrl_handbook.pdf) |
| Measurement category | Aerosols; Cloud Properties |
| Primary measurements | Aerosol backscattered radiation; Aerosol extinction; Backscatter depolarization ratio; Backscattered radiation |
| Record | 2011-01-21 to 2026-09-23 (active) |
| Datastreams with data | 25 across 11 sites |
| Sites | acx, awr, bnf, gan, guc, mag, mos, nsa, sbs, sgp, tmp |
| ARM page | https://www.arm.gov/capabilities/instruments/hsrl |


## Credit

Everything this skill knows about the instrument is the work of **R Bambha, J Garcia, I Razenkov, E Eloranta** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> R Bambha, J Garcia, I Razenkov, E Eloranta. *High-Spectral-Resolution Lidar (HSRL) Instrument Handbook*, DOE/SC-ARM-TR-157, September 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/hsrl_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Two primary optical mechanisms produce a lidar signal: backscatter of the laser beam by particles (including molecules), and attenuation of the beam en route to and from the backscatter region. A simple backscatter lidar provides only one measurement and must assume a functional relationship between these unknowns (e.g., the Klett method), whereas the HSRL method uses two measured profiles to avoid this assumption. This is achieved by exploiting Doppler frequency shifts: molecular thermal motion (~300 m/s) produces broad Doppler-shifted (~1 GHz) backscatter, while aerosols and cloud particles moving with wind/turbulence velocities (~10 m/s and ~1 m/s) produce much narrower Doppler shifts (~30 MHz and ~3 MHz). The resulting spectrum is a narrow aerosol spike riding on a broad molecular pedestal, which the receiver's narrow-band spectroscopic filters separate into molecular and combined aerosol+molecular channels. Ratios of these channels are used to derive backscatter coefficient, cancelling range-sensitive instrumental artifacts, while extinction is derived from the slope of the molecular channel alone. All measurements are calibrated by reference to molecular scattering measured at each point in the profile.

**Siting.** Continuous profiles start at an altitude of ~100 m and extend to 30 km. Deployed at fixed ARM sites (SGP, NSA) and mobile facilities (AMF2); has been used at STORMVEX (Steamboat Springs, Colorado), SGP, SAIL (Gothic, Colorado), AMIE (Gan Island, Maldives), MAGIC (Los Angeles to Hawaii voyage), BAECC (Hyytiälä, Finland), ACAPEX (Hawaii to San Diego voyage), MOSAiC (Arctic), and BNF (Bankhead National Forest, Alabama). Some instruments have short-range elevation scanning capability to scan over zenith to measure angular dependence of backscatter/depolarization from aligned ice particles; data near zenith (-3° to +3°) should be treated separately due to specular reflection effects.

**Sampling.** native rate 4 kHz repetition rate, 50 nsec (7.5 m) range bins, photon counting per laser shot; reported every Typical time resolution 2.5 s (programable); averaging Photon counts can be summed in time (multiple laser shots) and/or in space (adjacent range bins) to reduce uncertainty at the expense of resolution; sums applied before calculating derived backscatter coefficient/depolarization due to nonlinearity (hb p. 2).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Optical depth | - | - | - | - | (hb p. 1) |
| Extinction coefficient | - | - | - | - | (hb p. 1) |
| Backscattering coefficient | - | - | - | - | (hb p. 1) |
| Depolarization | - | - | - | - | (hb p. 1) |
| Backscatter phase function | - | - | - | - | (hb p. 1) |
| Photon counts per laser shot per 50 ns time bin | counts | - | Poisson statistics | 7.5 m range bin | (hb p. 3) |


## Specifications

| parameter | value | source |
|---|---|---|
| Power and wavelength transmitted (late 2020) | ~400 mw at 532 nm | (hb p. 1) |
| Power and wavelength transmitted (late 2020) | ~170 mW at532nm; ~400 mW at 1064 nm | (hb p. 1) |
| Laser pulse duration | 40 ns | (hb p. 2) |
| Repetition rate | 4 kHz | (hb p. 2) |
| Receiver field of view, narrow | 100 microradians | (hb p. 2) |
| Region of geometrical overlap, narrow FOV | ~6km and above | (hb p. 2) |
| Receiver field of view, wide | 700 microradians | (hb p. 2) |
| Region of geometrical overlap, wide FOV | ~575m and above | (hb p. 2) |
| Receiver aperture | 40 cm | (hb p. 2) |
| Receiver spectral bandpass @ 532nm | ~ 8 GHz (pressure-tuned etalon) | (hb p. 2) |
| Aerosol blocking filter bandwidth @ 532nm | 1.8 GHz (line 1109 of iodine spectrum) | (hb p. 2) |
| Receiver spectral bandpass @ 1064nm | ~ 7 GHz (thermally tuned etalon) | (hb p. 2) |
| Aerosol blocking filter bandwidth @ 1064nm | 1.5 GHz (FSR of Michelson Interferometer for HSRL2) | (hb p. 2) |
| Detection mode | Photon counting | (hb p. 2) |
| Range resolution | 7.5 m (50 nsec bin width) | (hb p. 2) |
| Altitude range recorded | 0 to 30km | (hb p. 2) |
| Typical time resolution | 2.5 s (programable) | (hb p. 2) |


## The data

Verified example: **`sgphsrlscanC1.a1`**, file `sgphsrlscanC1.a1.20260913.010003.nc`
(27.95 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=16, `bound`=2, `cal_time`=1, `calibration_altitude`=678, `geo_bin_range`=4000, `scan_angle`=44, `scan_range`=987 |
| Data variables | 40 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 4800 s |
| File time span | 2026-09-13T01:00:03 to 2026-09-13T23:20:02 |
| dod version | hsrlscan-a1-1.3 |
| process version | hsrl-6.3.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `beta_a_1064_backscatter` | 1/(m sr) | time,scan_angle,scan_range | - | Particulate 1064nm backscatter cross section per unit volume |
| `beta_a_backscatter` | 1/(m sr) | time,scan_angle,scan_range | - | Particulate backscatter cross section per unit volume |
| `beta_m` | 1/m | cal_time,calibration_altitude | - | Raob molecular scattering cross section per unit volume |
| `cal_time` | - | cal_time | - | Time of calibration change |
| `calibration_altitude` | m | calibration_altitude | - | Altitude above sea level for calibration |
| `color_ratio` | 1 | time,scan_angle,scan_range | - | Color ratio |
| `combined_gain` | 1 | cal_time | - | Combined gain factor |
| `combined_merge_threshold` | 1 | cal_time | - | Combined merge threshold |
| `combined_to_cross_pol_gain_ratio` | 1 | cal_time | - | Combined to cross polarization gain |
| `dewpoint_profile` | K | cal_time,calibration_altitude | - | Raob dewpoint temperature profile |
| `geo_cor` | 1 | cal_time,geo_bin_range | - | Overlap correction |
| `ground_distance` | m | time,scan_angle,scan_range | - | Distance from instrument along ground, projected into polar |
| `height` | m | time,scan_angle,scan_range | - | Height above instrument, projected into polar |
| `lidar_calibration_Cam` | 1 | cal_time | - | Aerosol in molecular calibration |
| `lidar_calibration_Cam_wfov` | 1 | cal_time | - | Aerosol in molecular calibration for wide-field-of-view |
| `lidar_calibration_Cmc` | 1 | cal_time,calibration_altitude | - | Molecular in combined calibration |
| `lidar_calibration_Cmc_wfov` | 1 | cal_time,calibration_altitude | - | Molecular in combined calibration for wide-field-of-view |
| `lidar_calibration_Cmm` | 1 | cal_time,calibration_altitude | - | Molecular in molecular calibration |
| `lidar_calibration_Cmm_wfov` | 1 | cal_time,calibration_altitude | - | Molecular in molecular calibration for wide-field-of-view |
| `linear_depol` | 1 | time,scan_angle,scan_range | - | Linear depolarization ratio for particulate |
| `linear_depol_1064` | 1 | time,scan_angle,scan_range | - | 1064nm total linear depolarization ratio |
| `molecular_to_wfov_gain_ratio` | 1 | cal_time | - | Molecular to wide-field-of-view gain |
| `polarization_cross_talk` | 1 | cal_time | - | Polarization cross talk |
| `pressure_profile` | hPa | cal_time,calibration_altitude | - | Raob pressure profile |
| `profile_mask` | 1 | time,scan_angle,scan_range | - | Mask for qc data |
| `raob_station` | 1 | cal_time | - | Radiosonde station ID |
| `raw_color_ratio` | 1 | time,scan_angle,scan_range | - | Raw color ratio |
| `scan_angle` | degree | scan_angle | - | Angle of telescope from zenith |
| `scan_range` | m | scan_range | - | Range from instrument along optical path |
| `sonde_latitude` | degree_N | cal_time | - | Latitude of temperature profiles |


_8 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgphsrlscanC1.a1", "2026-09-13", "2026-09-13")
ds = armlive_open("sgphsrlscanC1.a1", "2026-09-13", "2026-09-13", cleanup_qc=True)
```

Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `profile_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgphsrlscanC1.a1", "20110121", "20260923")
```

The handbook's own note on data quality: Because the HSRL data system is photon counting rather than analog detection, noise can be treated as Poisson and directly quantified; standard propagation-of-error methods applied to the Poisson statistical uncertainties of photon counts are used to derive measurement uncertainties. Rigorous error estimates can be computed for all measurements. Temporal/spatial averaging trades resolution for reduced uncertainty and must be applied before computing derived quantities to avoid nonlinearity bias.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Extinction measurement sensitivity to systematic effects (overlap function drift) | Extinction profiles show more noise and bias than backscatter-coefficient measurements, especially near geometric overlap regions; derived from a single (molecular) channel rather than a... | Requires significantly longer averaging intervals; use clear-sky measurements to correct drifts in geometric overlap and detector after-pulsing | (hb p. 3) |
| Reduced correction update frequency during extended cloudy/aerosol-laden periods | Extinction and overlap corrections become stale/less effective during long cloudy or aerosol-laden periods, potentially degrading data quality | Corrections rely on clear-sky measurements; effectiveness is reduced without them | (hb p. 7) |
| Alignment drift correlated with humidity (pre-2019 AMF2 HSRL) | Instability in boundary-layer extinction coefficient estimates from the narrow FOV channel | Addressed via 2019/2021 hardware upgrades to receiver/transmitter | (hb p. 7) |
| Near-field signal limitation from small FOV and high repetition rate | Continuous profiles only start at ~100 m altitude; region of geometrical overlap for narrow FOV channel is ~6 km and above, wide FOV ~575 m and above - data below these heights affected by... | Wide-field-of-view receiver (700 microradians) used to generate the instrument overlap function for narrow-FOV channels | (hb p. 1) |
| Temporal averaging nonlinearity bias | Because the relationship between photon counts and derived products is nonlinear, summing counts in time to reduce noise can introduce systematic biases if not applied before calculating... | Sums applied before calculating derived backscatter coefficient and/or depolarization values | (hb p. 3) |
| Specular reflection from aligned ice particles near zenith | Enhancement in backscatter near zenith at 532 nm and suppression of depolarization near zenith at 532 nm during scanning operations, seen as anomalous near-zenith signal in RHI plots | Avoid using data taken at scan angles within -3° to +3° of zenith when constructing standard backscatter/depolarization plots | (hb p. 4) |
| Discontinuation of circularly polarized measurements variable change (HSRL1 2019 upgrade) | Pre-upgrade circular polarization variables replaced by linear polarization analogs in the dataset, requiring analysts to note the variable definition change across the upgrade date | None stated beyond noting the change | (hb p. 6) |
| Photon-counting (Poisson) noise requiring averaging trade-off | High per-shot/per-bin noise in raw photon counts; noise reduced only by summing in time and/or space, trading off temporal/spatial resolution | Sum photon counts in time and/or space to reduce uncertainties to acceptable values | (hb p. 3) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Three major components: calibration using radiosonde inputs (vertical profiles of temperature and pressure used to determine expected clear-air backscatter as a function of range, serving as calibration source for molecular channels), measurement of the receiver's transmission spectrum (internal calibrations of... (hb p. 6) |
| Calibration interval | Radiosonde calibration updated at the frequency of available radiosondes; spectroscopic filter internal calibrations performed daily; receiver channel baseline characterization performed monthly (hb p. 6) |
| Traceability | Radiosonde-derived expected molecular backscatter profiles from atmospheric temperature/pressure; iodine absorption spectrum line #1109 locking for emission wavelength (hb p. 6) |
| Routine maintenance | Regular cleaning of the shelter window (weekly inspection and possible cleaning); laser coolant level checked monthly (typically requires no maintenance) (hb p. 6) |
| Maintenance interval | Weekly (window inspection/cleaning); monthly (coolant check, baseline characterization) (hb p. 6) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Raman lidar (RL), micropulse lidar (MPL).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `HSRL` | high-spectral-resolution lidar |
| `FOV` | field of view |
| `DFB` | distributed-feedback (laser) |
| `RL` | Raman lidar |
| `MPL` | micropulse lidar |
| `AMF` | ARM Mobile Facility |
| `NSA` | North Slope of Alaska |
| `SGP` | Southern Great Plains |
| `BNF` | Bankhead National Forest |
| `STORMVEX` | Storm Peak Lab Cloud Property Validation Experiment |
| `AMIE` | ARM Madden-Julian Oscillation Investigation Experiment-Gan Island |
| `MAGIC` | Marine ARM GPCI Investigation of Clouds |
| `BAECC` | Biogenic Aerosols-Effects on Clouds and Climate |
| `ACAPEX` | ARM Cloud Aerosol Precipitation Experiment |


### References the handbook cites

- Eloranta, EW. 2005. High Spectral Resolution Lidar in Lidar: Range-Resolved Optical Remote Sensing of the Atmosphere. Klaus Weitkamp editor, Springer Series in Optical Sciences, Springer-Verlag, New York.
- Holz, R.E. 2002. Measurements of cirrus backscatter phase functions using a high-spectral-resolution lidar. Master's Thesis, University of Wisconsin-Madison.
- Tenti, G, CD Boley, and RC Desai. 1974. "On the kinetic model description of Rayleigh–Brillouin scattering from molecular gases." Canadian Journal of Physics 52(4), 285–290, https://doi.org/10.1139/p74-041
- Turner, DD, and EW Eloranta. 2008. "Validating Mixed-Phase Cloud Optical Depth Retrieved from Infrared Observations with High Spectral Resolution Lidar." IEEE Geoscience and Remote Sensing Letters 5(2): 285–288,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/hsrl_handbook.pdf (14 pages, DOE/SC-ARM-TR-157, by R Bambha, J Garcia, I Razenkov, E Eloranta)
- Catalog record: ARM data-source index, `instrument_class_code=hsrl`, read 2026-09-23
- Example file: `sgphsrlscanC1.a1.20260913.010003.nc` from `sgphsrlscanC1.a1`, 27.95 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
