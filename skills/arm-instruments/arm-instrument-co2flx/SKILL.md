---
name: arm-instrument-co2flx
description: ARM Carbon Dioxide Flux Measurement Systems (co2flx) - handbook-derived instrument reference. Measurement principle, reported quantities (u, v, w winds; sonic temperature, Wind Speed, Wind Speed Offset, Speed of Sound, CO2 concentration, CO2 Zero Drift, CO2 RMS Noise), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpco2flxwindC1.b1) and the variable inventory of a real file. Use when working with co2flx data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Carbon. Triggers - co2flx, Carbon Dioxide Flux Measurement Systems, sgpco2flxwindC1.b1, u, v, w winds; sonic temperature, Wind Speed, Wind Speed Offset, Speed of Sound, CO2 concentration, Atmospheric Carbon, Gill Instruments R3-50 (sonic anemometer), LI-COR LI-7500RS (infrared gas analyzer), CO2FLX, IRGA, NetCDF, LBNL.
---

# CO2FLX - Carbon Dioxide Flux Measurement Systems

The carbon dioxide flux measurement system (CO2FLX) provides half-hour-averaged turbulent fluxes of CO2, H2O (latent heat), sensible heat, and momentum using the eddy covariance technique, deployed at three heights (4, 25, 60 m) on the SGP Central Facility tower and tripod/satellite stations.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 46 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `co2flx` |
| Handbook | [DOE/SC-ARM-TR-048 / WS Chan, SC Biraud / September 2022](https://www.arm.gov/publications/tech_reports/handbooks/co2flx_handbook.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Gill Instruments R3-50 (sonic anemometer); LI-COR LI-7500RS (infrared gas analyzer); Kipp & Zonen CNR4 (net radiometer) and PQS1 (PAR sensor); Delta-T SPN1 (sunshine pyranometer); Apogee SI-111... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Atmospheric turbulence; Carbon dioxide (CO2) concentration; Carbon dioxide (CO2) flux |
| Record | 2001-01-01 to 2026-09-23 (active) |
| Datastreams with data | 31 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/co2flx |


## Credit

Everything this skill knows about the instrument is the work of **WS Chan, SC Biraud** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> WS Chan, SC Biraud. *Carbon Dioxide Flux Measurement System (CO2FLX) Instrument Handbook*, DOE/SC-ARM-TR-048, September 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/co2flx_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Fluxes are calculated using the eddy covariance technique which requires high-frequency (10 Hz) observations of wind speed using a sonic anemometer and a scalar of interest such as carbon dioxide (CO2) and water vapor (H2O) concentrations using an infrared gas analyzer. The sonic anemometer uses three pairs of ultrasonic transmit/receive transducers to measure the transit time of sound signals traveling between the transducer pairs; wind speed along each axis is determined from the difference in transit times, and sonic temperature is computed from the speed of sound determined from the average transit time along the vertical axis. A pair of measurements are made along each axis 100 times per second, and ten measurements are averaged to produce 10 wind measurements and 10 temperatures each second. The IRGA measures CO2 and H2O densities by detecting the absorption of infrared radiation in the light path.

**Siting.** Turbulent fluxes collected at three heights (4, 25, 60 m) at SGP Central Facility (C1). The 25 and 60-m instruments are on a 60-m triangular, guyed tower with mechanically lowerable booms; an instrument shed at the tower base houses the primary data acquisition computer. The 4-m flux instruments are on a tripod southeast of the 60-m tower, with a datalogger for T/RH, barometric pressure, rain gauge, and 6-level soil moisture/temperature profile; line power and data communications present. Below-ground observations are at a soil 'satellite' station south of the 4-m tripod (solar/battery power, RF radio communications). Radiation sensors are on a remote 'satellite' station south of the soil...

**Sampling.** native rate 10 Hz (high-frequency raw observations from sonic anemometer and IRGA); reported every 30-minute (half-hour) averages; averaging 30-minute-averaged fluxes and related statistics from eddy covariance processing (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| u, v, w winds; sonic temperature | - | - | - | - | (hb p. 10) |
| CO2 and H2O concentrations; ambient temperature and pressure | - | - | - | - | (hb p. 10) |
| Wind Speed | ms-1 | 0 to 45 ms-1 | less than 1% rms | 0.01 ms-1 | (hb p. 24) |
| Wind Speed Offset | ms-1 | - | less than ±0.01ms-1 | - | (hb p. 24) |
| Speed of Sound (SOS) | ms-1 | 300-370 ms-1 | less than ±0.5% (For wind speeds less than 30... | 0.01ms-1 | (hb p. 24) |
| CO2 concentration | μmol mol-1 | 0 to 3000 μmol mol-1 | Within 1% of reading | - | (hb p. 24) |
| CO2 Zero Drift | ppm per °C | - | ±0.1 ppm typical, ±0.3 ppm maximum | - | (hb p. 24) |
| CO2 RMS Noise (@370 ppm CO2) | ppm | - | @5 Hz: 0.08 ppm; @10 Hz: 0.11 ppm; @20 Hz: 0.16... | - | (hb p. 24) |
| CO2 Gain Drift (% of reading per °C @ 370 ppm) | % | - | ±0.02% typical, ±0.1% maximum | - | (hb p. 24) |
| Direct Sensitivity to H2O (CO2 channel) | mol CO2 mol-1 H2O | - | ±2.00E-05 typical, ±4.00E-05 maximum | - | (hb p. 24) |
| H2O concentration | mmol mol-1 | 0 to 60 mmol mol-1 | Within 1% of reading | - | (hb p. 24) |
| H2O Zero Drift | mmol mol-1 per °C | - | ±0.03 mmol mol-1 typical, ±0.05 mmol mol-1... | - | (hb p. 24) |
| H2O RMS Noise (@10 mmol mol-1 H2O) | mmol mol-1 | - | @5 Hz: 0.0034; @10 Hz: 0.0047; @20 Hz: 0.0067 | - | (hb p. 24) |
| H2O Gain Drift (% of reading per °C @ 20 mmol mol-1) | % | - | ±0.15% typical, ±0.30% maximum | - | (hb p. 25) |
| Direct Sensitivity to CO2 (H2O channel) | mol H2O mol-1 CO2 | - | ±0.02 typical, ±0.05 maximum | - | (hb p. 25) |
| upwelling/downwelling shortwave and longwave radiation | - | - | - | - | (hb p. 10) |
| upwelling/downwelling PAR | - | - | - | - | (hb p. 10) |
| downwelling direct, diffuse, and total shortwave radiation | - | - | - | - | (hb p. 11) |
| surface temperature | - | - | - | - | (hb p. 11) |
| soil heat flux | - | - | - | - | (hb p. 11) |
| volumetric water content, soil electrical conductivity,... | - | - | - | - | (hb p. 11) |
| atmospheric pressure | - | - | - | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Measurement Rate (wind) | 50 s-1 (Full 3-axis measurement) | (hb p. 24) |
| Data Output Rates | From 0.4 to 50 s-1 | (hb p. 24) |
| Wind Speed Range | 0 to 45 ms-1 | (hb p. 24) |
| Wind Speed Accuracy | less than 1% rms | (hb p. 24) |
| Wind Speed Resolution | 0.01 ms-1 | (hb p. 24) |
| Wind Speed Offset | less than ±0.01ms-1 | (hb p. 24) |
| SOS Measurement Rate | 50 s-1 (Synchronous to wind measurement) | (hb p. 24) |
| SOS Range | 300-370 ms-1 | (hb p. 24) |
| SOS Accuracy | less than ±0.5% (For wind speeds less than 30 ms-1) | (hb p. 24) |
| SOS Resolution | 0.01ms-1 | (hb p. 24) |
| CO2 Calibration Range | 0 to 3000 μmol mol-1 | (hb p. 24) |
| CO2 Accuracy | Within 1% of reading | (hb p. 24) |
| H2O Calibration Range | 0 to 60 mmol mol-1 | (hb p. 24) |
| H2O Accuracy | Within 1% of reading | (hb p. 24) |
| R3-50 Input Voltage | 9-30 VDC | (hb p. 25) |
| LI-7500 Input Voltage | 10.5 to 30 VDC | (hb p. 25) |
| R3-50 Input Current | less than 300 mA at 12 VDC | (hb p. 25) |
| LI-7500 Input Current | 0.6-1.5 A (temperature dependent) at 12 VDC | (hb p. 25) |
| General Instrument Voltage | 12 VDC or 5 VDC nominal | (hb p. 25) |


## The data

Verified example: **`sgpco2flxwindC1.b1`**, file `sgpco2flxwindC1.b1.20260917.001500.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=48, `bound`=2 |
| Data variables | 36 |
| QC variables | 6 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2026-09-17T00:15:00 to 2026-09-17T23:45:00 |
| dod version | co2flxwind-b1-1.0 |
| process version | ingest-co2flxwind-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `wind_direction_25m` | degree | time | yes | Direction from which the wind blows, with respect to Geographic or... |
| `wind_direction_4m` | degree | time | yes | Direction from which the wind blows, with respect to Geographic or... |
| `wind_direction_60m` | degree | time | yes | Direction from which the wind blows, with respect to Geographic or... |
| `wind_speed_25m` | m/s | time | yes | Mean wind speed at 25m |
| `wind_speed_4m` | m/s | time | yes | Mean wind speed at 4m |
| `wind_speed_60m` | m/s | time | yes | Mean wind speed at 60m |
| `cross_wind_speed_variance_25m` | m^2/s^2 | time | - | Variance of cross wind speed at 25m |
| `cross_wind_speed_variance_4m` | m^2/s^2 | time | - | Variance of cross wind speed at 4m |
| `cross_wind_speed_variance_60m` | m^2/s^2 | time | - | Variance of cross wind speed at 60m |
| `max_wind_speed_25m` | m/s | time | - | Maximum instantaneous wind speed at 25m |
| `max_wind_speed_4m` | m/s | time | - | Maximum instantaneous wind speed at 4m |
| `max_wind_speed_60m` | m/s | time | - | Maximum instantaneous wind speed at 60m |
| `time` | - | time | - | Time offset from midnight |
| `vertical_wind_25m` | m/s | time | - | Wind component along the w anemometer axis at 25m |
| `vertical_wind_4m` | m/s | time | - | Wind component along the w anemometer axis at 4m |
| `vertical_wind_60m` | m/s | time | - | Wind component along the w anemometer axis at 60m |
| `vertical_wind_variance_25m` | m^2/s^2 | time | - | Variance of vertical wind at 25m |
| `vertical_wind_variance_4m` | m^2/s^2 | time | - | Variance of vertical wind at 4m |
| `vertical_wind_variance_60m` | m^2/s^2 | time | - | Variance of vertical wind at 60m |
| `wind_direction_variance_25m` | m^2/s^2 | time | - | Variance of wind direction at 25m |
| `wind_direction_variance_4m` | m^2/s^2 | time | - | Variance of wind direction at 4m |
| `wind_direction_variance_60m` | m^2/s^2 | time | - | Variance of wind direction at 60m |
| `wind_speed_variance_25m` | m^2/s^2 | time | - | Variance of wind speed at 25m |
| `wind_speed_variance_4m` | m^2/s^2 | time | - | Variance of wind speed at 4m |
| `wind_speed_variance_60m` | m^2/s^2 | time | - | Variance of wind speed at 60m |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpco2flxwindC1.b1", "2026-09-17", "2026-09-17")
ds = armlive_open("sgpco2flxwindC1.b1", "2026-09-17", "2026-09-17", cleanup_qc=True)
```

## Quality control in this datastream

6 `qc_` companion variables cover 6 of the
36 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("sgpco2flxwindC1.b1", "20010101", "20260923")
```

The handbook's own note on data quality: Many variables have associated QC flags included in the datastream (only for b1-level data), with 'qc_' prefix on variable name; descriptions in NetCDF global or variable-specific attributes. QC flags for turbulent fluxes (H, LE, co2_flux, etc.) have flags 1-9 corresponding to micrometeorological test results based on Foken et al. (2004), where lower values are better for satisfying eddy covariance assumptions. All IRGA-derived variables also have flag 10, triggered when the sensing path is not clear (dirt, precipitation, etc.). No QC flags are generated for unprocessed a1-level data....

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sensing path contamination (dirt, precipitation) on sonic anemometer and IRGA | IRGA-derived variables trigger QC flag 10 when sensing path is not clear; reference_signal_strength drops below 93 | Periods when signal strength is below 93 should be treated cautiously; routine cleaning is necessary | (hb p. 16) |
| No QC flags generated for unprocessed a1-level data | Raw high-frequency a1 data have exposed sensing paths sensitive to environmental contamination but carry no QC flag | - | (hb p. 16) |
| Micrometeorological test failures (Foken et al. 2004 rubric) | QC flags 1-9 on turbulent flux variables (H, LE, co2_flux, etc.), lower values better for satisfying eddy covariance assumptions | - | (hb p. 16) |
| Removal of 25 and 60-m IRGAs after July 2015 | CO2 and H2O concentration/flux variables absent from sgpco2flx25mC1.b1 and sgpco2flx60mC1.b1 datastreams after transition to baseline system | - | (hb p. 3) |
| Working at height and environmental hazards | N/A - operational safety consideration, not a data artifact | Follow ARM SGP site safety protocols; hard hats near 60m tower | (hb p. 21) |
| Historical (pre-2015) uncertainty from low turbulence at night | Nighttime periods with mean wind speed less than 2 m/s show imperfect mixing under low turbulence conditions, dominating measurement uncertainty | - | (hb p. 38) |
| Historical airborne material obscuring sound/light path | Noise caused by rain or other airborne material briefly obscuring sound or light path of sensors | Diagnostic variables provided to identify sources of uncertainty | (hb p. 38) |
| Historical spectral energy loss due to sensor separation (no correction applied) | Estimated error of 3-7% for 4-m measurements above crops; less significant at 25/60 m | None applied; estimated using Moore (1986) | (hb p. 40) |
| Historical lack of storage flux correction | Fluxes reflect only turbulent fluxes and omit storage of CO2, H2O, or heat in air column between sensor and land surface; often significant for 60-m system | Working to incorporate precision gas system data to include storage correction for 25- and 60-m heights | (hb p. 40) |
| Historical density/specific heat estimation assumption at 25/60 m | 25 and 60 m systems assume constant pressure of 98 kPa when estimating air density and specific heat from virtual temperature and H2O density, causing small errors when actual... | - | (hb p. 40) |
| Historical soil moisture sensor temperature sensitivity | Large temperature sensitivity observed in soil moisture sensors, especially in shallow soil with large temperature variations; not corrected in processing to date | Users may consider using diurnal soil temperature variations to correct diurnal variations in moisture signals; future files planned to include... | (hb p. 40) |
| Historical raw data spike/out-of-range values | nspk_unrot_u/v/w counts when speed greater than  40 m/s or deviation from mean greater than  6*(std dev); nspk_t for deviation greater than  5*(std dev); nspk_q for values greater than 2000... | Spikes replaced with running mean value and not used to update mean; counted and mean spike value calculated | (hb p. 37) |
| Historical occasional data loss | Loss of power, communications, or instrument malfunction causes intermittent gaps; data quality reported greater than 80% for a large fraction of operating lifetime | Review quality reports describing intermittent problems and changes to sensors/processing; contact instrument mentor | (hb p. 38) |
| Historical qc flag scheme (b1 level) | qc values: 0=not suspect,1=missing,2=below min/above max or +-infinity,4=dependency failed,8=large variance,16=suspect due to greater than 100 spikes (applies to t,q,c),32=suspect due to... | See Data Description File for specific min/max/other values | (hb p. 38) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | All instrument calibrations are performed by the instrument manufacturers. Historically, IRGA offset and gain calibrated by introducing gas of known concentration into a calibration hood surrounding the light path; offset calibrated using dry N2 from a gas bottle, gain calibrated using a bottle with known CO2... (hb p. 21) |
| Calibration interval | Following calibration intervals as recommended by the manufacturer. Historical example (60-m system): October 18, 2000; July 13, 2001; December 18, 2001; December 20, 2002 (replaced). Portable flux systems calibrated before each portable deployment period. (hb p. 21) |
| Routine maintenance | SGP site operations conduct daily checks of the CO2FLX system. Both eddy covariance sensors are sensitive to environmental contaminants blocking the sensing path, so routine cleaning is necessary to maintain instrument performance. Radiation sensors require regular cleaning. (hb p. 21) |
| Maintenance interval | Daily checks (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `3D` | three-dimensional |
| `ARM` | Atmospheric Radiation Measurement |
| `C1` | Central Facility |
| `CO2FLX` | carbon dioxide flux measurement system |
| `IRGA` | infrared gas analyzer |
| `NetCDF` | Network Common Data Form |
| `PAR` | photosynthetically active radiation |
| `QC` | quality control |
| `RF` | radio frequency |
| `RH` | relative humidity |
| `rms` | root mean square |
| `SGP` | Southern Great Plains |
| `SOS` | speed of sound |
| `VDC` | voltage, direct current |


### References the handbook cites

- Aubinet, M, T Vesala, and D Papale. (Eds.). 2012. Eddy Covariance. Springer, Dordrecht, Netherlands.
- Bagley, JE, LM Kueppers, DP Billesbach, IN Williams, SC Biraud, and MS Torn. 2017. "The Influence of Land Cover on Surface Energy Partitioning and Evaporative Fraction Regimes in the U.S. Southern Great Plains."...
- Burba, G. 2013. Eddy Covariance Method for Scientific, Industrial, Agricultural and Regulatory Applications. LI-COR Biosciences.
- Fischer, ML, DP Billesbach, JA Berry, WJ Riley, and MS Torn. 2007. "Spatiotemporal Variations in Growing Season Exchanges of CO2, H2O, and Sensible Heat in Agricultural Fields of the Southern Great Plains." Earth...
- Foken, T. 2017. Micrometeorology. Springer, Berlin Heidelberg.
- Foken, T, M Gockede, M Mauder, L Mahrt, BD Amiro, and JW Munger. 2004. Post-field quality control, in Handbook of Micrometeorology. Kluwer Academic, Dordrecht, Netherlands, 81-108.
- Raz-Yaseef, N, DP Billesbach, ML Fischer, SC Biraud, SA Gunter, JA Bradford, and MS Torn. 2015. "Vulnerability of crops and native grasses to summer drying in the U.S. Southern Great Plains." Agriculture, Ecosystems &...
- Kaimal, J.C., Finnigan, J.J., 1994. Atmospheric Boundary Layer Flows: Their Structure and Measurement. Oxford University Press, New York.
- Moore, C.J., 1986. Frequency Response Corrections for Eddy Correlation Systems. Boundary-Layer Meteorol. 37, 17-35.
- Paw U, K.T., Baldocchi, D.D., Meyers, T.P., Wilson, K.B. Correction of Eddy-Covariance Measurements Incorporating Both Advective Effects and Density Fluxes. Boundary-Layer Meteorol. 97, 487-511.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/co2flx_handbook.pdf (46 pages, DOE/SC-ARM-TR-048, by WS Chan, SC Biraud)
- Catalog record: ARM data-source index, `instrument_class_code=co2flx`, read 2026-09-23
- Example file: `sgpco2flxwindC1.b1.20260917.001500.nc` from `sgpco2flxwindC1.b1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
