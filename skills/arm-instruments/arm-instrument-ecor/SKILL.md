---
name: arm-instrument-ecor
description: ARM Eddy Correlation Flux Measurement System (ecor) - handbook-derived instrument reference: measurement principle, reported quantities (u, v, w wind components, Speed of sound, Atmospheric temperature, ta, Water vapor density, q, CO2 concentration, c, Atmospheric pressure, pa, Sensible heat flux, H, Latent heat flux, LvE), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaecorsfC1.b1) and the variable inventory of a real file. Use when working with ecor data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface/Subsurface Properties. Triggers - ecor, Eddy Correlation Flux Measurement System, enaecorsfC1.b1, u, v, w wind components, Speed of sound, Atmospheric temperature, ta, Water vapor density, q, CO2 concentration, c, Atmospheric pressure, pa, Surface/Subsurface Properties, 3D sonic anemometer: Gill Instruments Ltd, model Windmaster (SGP, ECOR, IRGA, EBBR, SEBS.
---

# ECOR - Eddy Correlation Flux Measurement System

The ECOR system provides in situ, half-hour (30-minute) measurements of surface turbulent fluxes of momentum, sensible heat, latent heat, CO2, and (at some sites) methane, deployed on towers/booms at ARM surface sites where other flux methods like EBBR are difficult to employ.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 24 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ecor` |
| Handbook | [DOE/SC-ARM-TR-052 / DR Cook, RC Sullivan / July 2025](https://www.arm.gov/publications/tech_reports/handbooks/ecor_handbook.pdf) |
| Measurement category | Surface/Subsurface Properties |
| Manufacturer / model | 3D sonic anemometer: Gill Instruments Ltd, model Windmaster (SGP, ENA, AMF1) and WindMaster Pro (NSA, AMF2, AMF3 before 2024); IRGA CO2/H2O: LI-COR, Inc. model LI-7500 and LI-7500DS; IRGA CH4:... |
| Primary measurements | Atmospheric turbulence; Carbon dioxide (CO2) concentration; Carbon dioxide (CO2) flux; Horizontal wind; Latent heat flux; Methane concentration |
| Record | 1995-06-02 to 2026-09-23 (active) |
| Datastreams with data | 82 across 24 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, grw, guc, hfe, hou |
| ARM page | https://www.arm.gov/capabilities/instruments/ecor |


## Credit

Everything this skill knows about the instrument is the work of **DR Cook, RC Sullivan** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> DR Cook, RC Sullivan. *Eddy Correlation Flux Measurement System (ECOR) Instrument Handbook*, DOE/SC-ARM-TR-052, July 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ecor_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The eddy covariance technique correlates the vertical wind component with the horizontal wind component, air temperature, water vapor density, and CO2 concentration to obtain surface fluxes. A fast-response 3D sonic anemometer (WindMaster/WindMaster Pro) measures orthogonal wind components and speed of sound (SOS) by timing ultrasonic transit times between transducer pairs along three axes, from which air temperature is derived with a humidity correction. An open-path infrared gas analyzer (IRGA) measures water vapor density and CO2 concentration by detecting absorption of IR radiation at wavelength bands centered on strong absorption lines of each gas. The sonic anemometer synchronously samples the IRGA analog outputs at 10 Hz and combines all data into a single serial datastream, which is processed every half hour to compute means, variances, covariances, skewness, and kurtosis, with 2D coordinate rotations applied to achieve zero mean vertical wind speed. Momentum flux is determined from correlation of horizontal and vertical rotated wind components, and sensible heat, latent heat, and CO2 fluxes are determined from correlation of rotated vertical velocity with temperature, water vapor density, and CO2 concentration respectively.

**Siting.** Typical arrangement places the ECOR system on the north side of a field (e.g., wheat field), with sonic and IRGA sensor heads mounted on a small tower at 3 m above ground level at the end of a horizontal boom pointing south (except Okmulgee EF21, where system is on a 15 m tall tower about 3 m above the forest canopy). The standard ARM site arrangement has the sonic sensor 'North' mark pointing along the boom to the tower, boom usually pointing due south; u is north-south (positive north), v is east-west (positive west); no correction is made for boom misalignment from south (u is 'along boom', v is 'cross boom'). Appropriate fetch was determined from a 1/70 measurement height-to-fetch...

**Sampling.** native rate 10 Hz (primary measurements); sonic sampling 30 times per second per axis averaged to 10-Hz datastream; reported every 30-minute (half-hour) calculated quantities; averaging Half-hour averaging with statistics (mean, variance, covariance, skewness, kurtosis) and two-axis coordinate rotation for vertical turbulent fluxes (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| u, v, w wind components | m s-1 | - | - | - | (hb p. 9) |
| Speed of sound (SOS), s | m s-1 | 307 to 367 ms-1 | 3% RMS error for winds less than  20 ms-1, 6%... | 0.01 ms-1 | (hb p. 13) |
| Atmospheric temperature, ta | °K | - | - | - | (hb p. 9) |
| Water vapor density, q | mmol m-3 | 0 to 2000 mmol m-3 (software selectable) | About 1% (limited by calibration) | About 0.14 mmol m-3... | (hb p. 13) |
| CO2 concentration, c | mmol m-3 | 8 to 32 mmol m-3 (software selectable) | About 1% (limited by calibration) | About 4 µmol m-3 (typical... | (hb p. 13) |
| Atmospheric pressure, pa | kPa | - | - | - | (hb p. 9) |
| Sensible heat flux, H | W m-2 | - | 6% | - | (hb p. 9) |
| Latent heat flux, LvE | W m-2 | - | 5% | - | (hb p. 9) |
| Momentum flux (dynamic), M | K kg m-1 s-2 | - | 5% | - | (hb p. 9) |
| Friction velocity, u* | m s-1 | - | - | - | (hb p. 9) |
| CO2 flux, FCO2 | µmol m-2 s-1 | - | 4% | - | (hb p. 9) |
| Mean wind speed (vector averaged), V | m s-1 | - | - | - | (hb p. 10) |
| Mean wind direction, D | deg | - | - | - | (hb p. 10) |
| Mean atmospheric temperature, Ta | °K | - | - | - | (hb p. 10) |
| Mean water vapor density, Q | mmol m-3 | - | - | - | (hb p. 10) |
| Mean CO2 concentration, C | mmol m-3 | - | - | - | (hb p. 10) |
| Mean atmospheric pressure, Pa | kPa | - | - | - | (hb p. 10) |
| Methane concentration | ppm | 0 to 25 ppm | About 1 (limited by concentration) | 5 ppb | (hb p. 20) |


## Specifications

| parameter | value | source |
|---|---|---|
| Ultrasonic anemometer u,v accuracy | 1.5% RMS error for winds below 20 ms-1, 3% otherwise | (hb p. 13) |
| Ultrasonic anemometer w accuracy | 3% of magnitude | (hb p. 13) |
| SOS Range | 307 to 367 ms-1 | (hb p. 13) |
| SOS Resolution | 0.01 ms-1 | (hb p. 13) |
| SOS Accuracy | 3% RMS error for winds less than  20 ms-1, 6% RMS error for winds 20 to 60 ms-1 | (hb p. 13) |
| Analog inputs Type | eight single-ended or four differential (software selectable) | (hb p. 13) |
| Analog inputs Range | -5 to +5 VDC | (hb p. 13) |
| Analog inputs Resolution | 14 bit | (hb p. 13) |
| Analog inputs Accuracy | 0.05% of full scale (for temperature from +5 to +35°C); 0.1% of full scale (for -40 to +5°C, +35 to +60°C) | (hb p. 13) |
| LI-7500 Water vapor density Range | 0 to 2000 mmol m-3 (software selectable) | (hb p. 13) |
| LI-7500 Water vapor density Accuracy | About 1% (limited by calibration) | (hb p. 13) |
| LI-7500 Water vapor density Precision | About 0.14 mmol m-3 (typical RMS noise) | (hb p. 13) |
| LI-7500 CO2 concentration Range | 8 to 32 mmol m-3 (software selectable) | (hb p. 13) |
| LI-7500 CO2 concentration Accuracy | About 1% (limited by calibration) | (hb p. 13) |
| LI-7500 CO2 concentration Precision | About 4 µmol m-3 (typical RMS noise) | (hb p. 13) |
| LI-7500 Analog outputs Type | Two-user selectable | (hb p. 13) |
| LI-7500 Analog outputs Range | 0 to 5 V DC | (hb p. 13) |
| LI-7500 Analog outputs Resolution | 16 bit | (hb p. 13) |
| LI-7500 Analog outputs Update rate | 300 Hz | (hb p. 13) |
| LI-7500DS Water vapor density Range |  | (hb p. 13) |
| LI-7500DS Water vapor density Accuracy | Within 1% | (hb p. 13) |
| LI-7500DS Water vapor density Precision | About 0.0047 mmol m-3 (typical RMS noise) | (hb p. 13) |
| LI-7500DS CO2 concentration Range |  | (hb p. 14) |
| LI-7500DS CO2 concentration Accuracy | Within 1% | (hb p. 14) |
| LI-7500DS CO2 concentration Precision | About 0.11 ppm (typical RMS noise) | (hb p. 14) |
| LI-7700 Methane concentration Range | 0 to 25 ppm | (hb p. 14) |


_5 further specification rows are in the handbook._

## The data

Verified example: **`enaecorsfC1.b1`**, file `enaecorsfC1.b1.20260922.000000.nc`
(0.09 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=48, `bound`=2 |
| Data variables | 146 |
| QC variables | 31 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2026-09-22T00:00:00 to 2026-09-22T23:30:00 |
| dod version | ecorsf-b1-1.6 |
| process version | ingest-ecorsf-2.2-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `air_density` | kg/m^3 | time | yes | Density of ambient air |
| `air_heat_capacity` | J/(kg K) | time | yes | Specific heat at constant pressure of ambient air |
| `air_pressure` | kPa | time | yes | Mean pressure of ambient air, calculated from high frequency air... |
| `air_temperature` | K | time | yes | Mean temperature of ambient air, calculated from high frequency air... |
| `ch4_flux` | nmol/(m^2 s) | time | yes | Corrected ch4 flux |
| `ch4_molar_density` | nmol/m^3 | time | yes | Measured molar density of ch4 |
| `co2_flux` | umol/(m^2 s) | time | yes | Corrected co2 flux |
| `co2_molar_density` | mmol/m^3 | time | yes | Measured molar density of co2 |
| `friction_velocity` | m/s | time | yes | Friction velocity |
| `h2o_flux` | mmol/(m^2 s) | time | yes | Corrected h2o flux |
| `h2o_molar_density` | mmol/m^3 | time | yes | Measured molar density of h2o |
| `latent_flux` | W/m^2 | time | yes | Corrected latent heat flux |
| `mean_wind` | m/s | time | yes | Mean wind speed |
| `momentum_flux` | kg/(m s^2) | time | yes | Corrected momentum flux |
| `sensible_heat_flux` | W/m^2 | time | yes | Corrected sensible heat flux |
| `sonic_temperature` | K | time | yes | Mean temperature of ambient air measured by the anemometer, ts |
| `uncorrected_ch4_flux` | nmol/(m^2 s) | time | yes | Uncorrected ch4 flux |
| `uncorrected_co2_flux` | umol/(m^2 s) | time | yes | Uncorrected co2 flux |
| `uncorrected_latent_heat_flux` | W/m^2 | time | yes | Uncorrected latent heat flux |
| `uncorrected_sensible_heat_flux` | W/m^2 | time | yes | Uncorrected sensible heat flux |
| `variance_ch4` | nmol^2/m^6 | time | yes | Variance of ch4 |
| `variance_co2` | mmol^2/m^6 | time | yes | Variance of co2 |
| `variance_h2o` | mmol^2/m^6 | time | yes | Variance of h2o |
| `variance_ts` | K^2 | time | yes | Variance of ts |
| `variance_u` | m^2/s^2 | time | yes | Variance of u |
| `variance_v` | m^2/s^2 | time | yes | Variance of v |
| `variance_w` | m^2/s^2 | time | yes | Variance of w |
| `wind_direction_from_north` | degree | time | yes | Direction from which the wind blows, with respect to Geographic north |
| `wind_u_component` | m/s | time | yes | Wind component along the u anemometer axis |
| `wind_v_component` | m/s | time | yes | Wind component along the v anemometer axis |


_80 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaecorsfC1.b1", "2026-09-22", "2026-09-22")
ds = armlive_open("enaecorsfC1.b1", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

This datastream carries 146 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enaecorsfC1.b1", start, end,
                  keep_variables=["air_density", "air_heat_capacity", "air_pressure", "qc_air_density", "qc_air_heat_capacity", "qc_air_pressure"])
```

## Quality control in this datastream

31 `qc_` companion variables cover 31 of the
146 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaecorsfC1.b1.20260922.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `ch4_flux` | Value is equal to missing_value. | 48 | 100.0 |
| `ch4_molar_density` | Value is equal to missing_value. | 48 | 100.0 |
| `uncorrected_ch4_flux` | Value is equal to missing_value. | 48 | 100.0 |
| `variance_ch4` | Value is equal to missing_value. | 48 | 100.0 |
| `variance_h2o` | Value is less than fail_min. | 35 | 72.9167 |
| `variance_co2` | Value is less than fail_min. | 12 | 25.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaecorsfC1.b1", "19950602", "20260923")
```

The handbook's own note on data quality: The data ingest process adds QC flags and generates daily b1-level NetCDF files. Basic data quality flags use bit values: 0x0 = within range, 0x1 = missing_value, 0x2 = less than valid_min, 0x4 = greater than valid_max, 0x8 = failed valid_delta check. Upgraded SGP systems (Oct 2019) include additional flags for steady state/well-developed turbulence assumptions, spike count/removal, amplitude resolution, drop-outs, absolute limits, and skewness/kurtosis thresholds. Instrument mentor performs daily-to-weekly visual QC with 1-3 day delay, comparing plots against adjacent ECOR/EBBR, SEBS, and...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| WindMaster Pro sonic SOS-derived temperature bias/slope error | Real temperature values derived from sonic SOS overestimated at low temperatures, underestimated at high temperatures; calibration of nine sonic anemometers showed slope ranging 0.71 to... | A linear correction procedure was implemented to account for the sensor deficiency (see Pekour 2004); vertical alignment and sonic SOS temperature... | (hb p. 11) |
| General ECOR calibration/measurement uncertainty | About 10% measurement uncertainty due to calibration issues, biases, vertical alignment, etc. | Part of uncertainty reduced through judicious processing every half hour, mostly in ECOR VAP post-processing | (hb p. 12) |
| Flux shortfall (underestimation) | Shortfalls of 10% to 25% commonly seen (35% less common) even after post-processing; smallest for bare soil/short vegetation, largest for tall vegetation like forests/corn | - | (hb p. 12) |
| Canopy energy storage not captured | Energy stored in vegetation canopy/litter not accounted for by eddy covariance technique or radiation/soil heat flux measurements, contributing to energy balance mismatch | - | (hb p. 12) |
| Sonic anemometer frequency measurement limitation | Sensing volume size limits ability to capture low-frequency flux components (atmospheric wave motions, advection from topography, dissimilar surfaces downwind, air mass changes) | - | (hb p. 12) |
| Non-steady atmospheric conditions | Rapid changes in wind direction, stability, temperature, pressure, water vapor, CO2 over seconds to minutes prevent proper covariance calculation | - | (hb p. 12) |
| Precipitation, fog, dew/frost wetting the LI-7500 optical window | Incorrect water vapor and CO2 measurements; CO2 more sensitive so latent heat flux can be correct while CO2 flux is not; off-scale or spiked readings in nighttime hours before dawn... | Use SEBS wetness measurement, collocated/nearby MET/SMOS rain gauges, or DQ HandS ECOR plots to identify precipitation times; no DQRs written for... | (hb p. 17) |
| Spikes in CO2 flux near zero flux | Large positive and negative spikes in CO2 flux when flux is essentially zero (example: E16, 08/16/05, 0800-0930 GMT) | - | (hb p. 17) |
| Low wind speed flagging of ustar/momentum flux | Friction velocity (ustar) and momentum flux (k) frequently flagged, especially at forested E21 Okmulgee site; sonic anemometer cannot make proper flux measurements below about 1 m/s | Only be concerned when minimum flag is tripped; values below minimum normally indicate untrustworthy low-wind-speed data | (hb p. 13) |
| Sudden wind direction shifts and coordinate transform | Spike in fluxes for a half-hour period due to poor handling of sudden wind direction shifts by ECOR coordinate transform routine | - | (hb p. 17) |
| Momentum flux/friction velocity sign mirroring | Momentum flux and friction velocity have opposite signs and mirror each other in DQ HandS plots (plotted with opposite sign scales) since ustar is computed from momentum flux | - | (hb p. 17) |
| Time stamp convention mismatch between ECOR and SMOS/EBBR | ECOR time stamps mark beginning of half hour (ECORSF marks end of half hour) whereas SMOS and EBBR mark end of half hour; ECOR measurements appear half hour earlier when compared on DQ... | - | (hb p. 12) |
| Water vapor flux and CO2 flux mirroring | Plots of lv_e and fc normally mirror each other; plotted to scales with opposite sign orientations in DQ HandS plots so they trend together | - | (hb p. 12) |
| Elevation (angle of attack) QC flag exceedance | QC flag for elevation angle occasionally exceeded, usually on positive side, especially at forested Okmulgee EF21 site due to uneven tree heights | QC flag limits for elevation set generously to accommodate forest site angles | (hb p. 12) |
| Elevated fluxes and noise at forest site (Okmulgee E21) | CO2, sensible heat, and latent heat fluxes often larger than other sites, water vapor and CO2 fluxes often twice as large; plots show more noise due to rougher, less homogeneous forest... | - | (hb p. 12) |
| Missing LI-7500 serial datastream defaults | When LI-7500 CO2/H2O serial datastream unavailable (pressure/temperature missing), default values used in CO2 and latent heat flux calculations | Resulting errors remain within the +/-10% system error | (hb p. 12) |
| Missing data periods | Gaps in data typically due to site data system collection/communication problems or ECOR data acquisition computer failure | Missing data sometimes filled in later from manual or automatic re-collection | (hb p. 12) |
| Insufficient fetch / vegetation heterogeneity by wind direction | Fluxes suspect for wind directions not meeting minimum fetch (210 m, from 1/70 height-to-fetch ratio); site-specific wind-direction-dependent vegetation/surface tables show suspect ranges... | Use documented wind-direction dependency tables per site to filter/interpret suspect directions | (hb p. 8) |
| Different vegetation surfaces preclude cross-site comparison | E14 (wheat/corn/stubble/bare soil) and E21 (forest) fluxes cannot be reliably compared with other grass-covered ECOR sites; significant differences expected | - | (hb p. 7) |
| ECOR vs EBBR comparison limitations | Only collocated ECOR (E14) and EBBR (E13) at SGP CF and E39; comparisons valid mainly for straight north/northwest wind (same grass surface) or when ground is snow covered; other directions... | - | (hb p. 7) |
| ECOR vs MET/SMOS comparison limitations | Wind speed/direction measured at different heights (SMOS 10 m vs ECOR 3 m) so SMOS wind speed expected greater than ECOR; ECOR temperature and pressure only approximate, differing... | - | (hb p. 8) |
| u/v wind component boom misalignment (no meteorological correction) | No correction made to convert u or v into meteorological north/east wind components when tower boom is not aligned to due south; u is 'along boom', v is 'cross boom' | - | (hb p. 5) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Sonic anemometer wind measurements ideally require no calibration, but WindMaster Pro SOS channel needs calibration to achieve accurate sensible heat measurement. IRGA calibrated by passing gas of known concentration through a calibration tube in the sensor head surrounding the light path; zero (offset) calibrated... (hb p. 16) |
| Calibration interval | Periodic (specific interval not stated) (hb p. 16) |
| Traceability | Calibration information stored in the Operations Status System (OSS), available to instrument mentors (hb p. 16) |
| Routine maintenance | ECOR Preventive Maintenance procedures and reports stored in the OSS; contact instrument mentor for details. No single comprehensive user manual available; vendor-supplied documentation and mentor-prepared procedures used internally by Site Operations. (hb p. 22) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: EBBR, SEBS, MET/SMOS, QCECOR VAP.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ECOR` | eddy correlation flux measurement system |
| `IRGA` | infrared gas analyzer |
| `SOS` | speed of sound |
| `WPL` | Webb, Pearman, Leuning |
| `EBBR` | energy balance Bowen ratio system |
| `SEBS` | surface energy balance system |
| `MET` | surface meteorological instrumentation |
| `SMOS` | surface meteorological observation system |
| `QCECOR` | Quality Controlled Eddy Correlation Flux Measurement Value-Added Product |
| `DQR` | Data Quality Report |
| `IMMS` | Instrument Mentor Monthly Summary |
| `OSS` | Operations Status System |
| `VAP` | value-added product |
| `DAC` | digital-to-analog converter |


### References the handbook cites

- Cook, DR, ML Fischer, and DJ Holdridge. 2006. "Comparison of ECOR, EBBR, and CO2FLX System Fluxes."
- Kaimal, JC, and JJ Finnigan. 1994. Atmospheric Boundary Layer Flows: Their Structure and Measurement.
- Massman, WJ and X Lee. 2002. "Eddy covariance flux corrections and uncertainties in long-term Studies of carbon and energy exchanges." Agricultural and Forest Meteorology 113(1-4):121-144.
- Moore, CJ. 1986. "Frequency response corrections for eddy correlation systems." Boundary-Layer Meteorology 37(1-2):17-35.
- Pekour, MS. 2004. "Experiences with the Windmaster Pro Sonic Anemometer."
- Twine, TE, et al. 2000. "Correcting eddy-covariance flux underestimates over a grassland." Journal of Agricultural and Forest Meteorology 103(3):279-300.
- Webb, EK, GI Pearman, and R Leuning. 1980. "Correction of flux measurements for density effects due to heat and water vapour transfer." QJRMS 106(44):85-100.
- Wilczak, JM, SP Oncley, and SA Stage. 2001. "Sonic Anemometer Tilt Correction Algorithms." Boundary-Layer Meteorology 99(1):127-150.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ecor_handbook.pdf (24 pages, DOE/SC-ARM-TR-052, by DR Cook, RC Sullivan)
- Catalog record: ARM data-source index, `instrument_class_code=ecor`, read 2026-09-23
- Example file: `enaecorsfC1.b1.20260922.000000.nc` from `enaecorsfC1.b1`, 0.09 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
