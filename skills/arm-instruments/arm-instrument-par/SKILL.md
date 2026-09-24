---
name: arm-instrument-par
description: ARM Photosynthetically Active Radiation Sensors (par) - handbook-derived instrument reference. Measurement principle, reported quantities (relative humidity, battery voltage), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfparS14.b1) and the variable inventory of a real file. Use when working with par data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - par, Photosynthetically Active Radiation Sensors, bnfparS14.b1, relative humidity, battery voltage, Radiometric, LI-190R, LI-COR Inc., PPFD, LBNL, METWXT.
---

# PAR - Photosynthetically Active Radiation Sensors

The PAR instrument measures photosynthetically active radiation (400-700 nm) as photosynthetic photon flux density using upward- and downward-facing LI-190R sensors mounted at multiple heights on ARM Bankhead National Forest towers to capture upwelling and downwelling PAR and spatial heterogeneity of the land surface.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 13 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `par` |
| Handbook | [DOE/SC-ARM-TR-319 / AB Moyes, SC Biraud / August 2025](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-319.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | LI-190R, LI-COR Inc., USA (PAR sensor); datalogger CR1000X, Campbell Scientific, USA; backup battery power supply PS200, Campbell Scientific, USA; internal humidity sensor CS210, Campbell Scientific,... |
| Primary measurements | Photosynthetically Active Radiation |
| Record | 2024-08-05 to 2026-09-22 (active) |
| Datastreams with data | 3 across 1 sites |
| Sites | bnf |
| ARM page | https://www.arm.gov/capabilities/instruments/par |


## Credit

Everything this skill knows about the instrument is the work of **AB Moyes, SC Biraud** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> AB Moyes, SC Biraud. *Photosynthetically Active Radiation (PAR) Instrument Handbook*, DOE/SC-ARM-TR-319, August 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-319.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

PAR sensors measure radiation reaching the sensor with wavelengths from 400-700 nm, per unit area, per unit time, i.e. the photosynthetic photon flux density (PPFD, µmol photons m-2 s-1). The LI-190R uses a high-quality silicon photodiode and glass optical filter to create uniform sensitivity to light between 400 nm and 700 nm, which closely corresponds to light used by most plants. A newly designed optical filter tailors the spectral response and is unaffected by environmental factors such as heat or humidity. The filter blocks light with wavelengths beyond 700 nm, which is critical for measurements under vegetation where the ratio of infrared to visible light may be high.

**Siting.** On the 43-meter tower of BNF supplemental site S10, sensors are located at 43 m, 22 m, 10 m, and 5 m from ground level; downwelling radiation is measured with upward-facing sensors at all heights, and upwelling radiation is measured with downward-facing sensors at 43 m and 5 m. On the two 10-m towers of BNF supplemental sites S13 and S14, upwelling radiation is measured at 8 m and 2 m, and downwelling radiation is measured at 8 m. Sensors are mounted on booms extending horizontally 2-3 m from the vertical tower structure, leveled to point either directly upwards (downwelling) or directly downwards (upwelling). At S10, sensors are located off the most southward-facing "D" face of the tower...

**Sampling.** native rate measurements collected every 10 s; reported every 1 minute average and standard deviation stored; averaging Every 1 minute, an average and standard deviation is stored in the output data table for each sensor, as well as the minimum battery voltage measured. (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Photosynthetically active radiation (PAR) / photosynthetic... | µmol m-2 s-1 | valid_min -10 µmol m-2 s-1 to valid_max... | ± 5% | - | (hb p. 10) |
| relative humidity (internal enclosure) | % | 0% to 100% | - | - | (hb p. 10) |
| battery voltage | V | 0 V to 17.5 V | - | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Calibration | ± 5% traceable to U.S. National Institute of Standards and Technology | (hb p. 7) |
| Sensitivity | Typically 5 μA to 10 μA per 1,000 μmol s-1 m-2 | (hb p. 7) |
| Linearity | Maximum deviation of 1% up to 10,000 µmol m-2 s-1 | (hb p. 7) |
| Response time | less than  1 µs | (hb p. 7) |
| Temperature Dependence | ± 0.15% per °C maximum | (hb p. 7) |
| Cosine Correction | Cosine corrected up to 82° angle of incidence | (hb p. 7) |
| Azimuth | less than  ± 1% error over 360° at a 45° elevation | (hb p. 7) |
| Tilt | No error induced from orientation | (hb p. 7) |
| Operating Temperature Range | −40 °C to 65 °C | (hb p. 7) |
| Relative Humidity Range | 0% to 100% RH, non-condensing | (hb p. 7) |
| Detector | High-stability silicon photovoltaic detector (blue enhanced) | (hb p. 7) |
| Size | 2.36 cm diameter × 3.63 cm (0.93” × 1.43”) | (hb p. 7) |
| Weight | 24 g head; 60 g base/cable (2 m) with screws | (hb p. 7) |


## The data

Verified example: **`bnfparS14.b1`**, file `bnfparS14.b1.20260919.000000.nc`
(0.17 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 26 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| dod version | par-b1-1.1 |
| process version | ingest-par-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `batt_volt_min` | V | time | yes | Minimum battery voltage |
| `par_1_dwell` | umol/m^2/s | time | yes | Average downwelling radiation for sensor 1 |
| `par_1_dwell_std` | umol/m^2/s | time | yes | Standard deviation of downwelling radiation for sensor 1 |
| `par_2_uwell` | umol/m^2/s | time | yes | Average upwelling radiation for sensor 2 |
| `par_2_uwell_std` | umol/m^2/s | time | yes | Standard deviation of upwelling radiation for sensor 2 |
| `par_3_uwell` | umol/m^2/s | time | yes | Average upwelling radiation for sensor 3 |
| `par_3_uwell_std` | umol/m^2/s | time | yes | Standard deviation of upwelling radiation for sensor 3 |
| `rh` | % | time | yes | Average logger enclosure relative humidity |
| `rh_std` | % | time | yes | Standard deviation of logger enclosure relative humidity |
| `panel_temp` | degC | time | - | Average logger panel temperature |
| `panel_temp_std` | degC | time | - | Standard deviation of logger panel temperature |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("bnfparS14.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("bnfparS14.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
26 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("bnfparS14.b1", "20240805", "20260923")
```

The handbook's own note on data quality: QC definition for all qc variables corresponding to primary variables uses flag_method = "bit": bit_1_description = "Value is equal to missing_value -9999." (bit value 1); bit_2_description = "Value is less than the valid_min." (bit value 2); bit_3_description = "Value is greater than the valid_max." (bit value 4). Valid_min/valid_max: PAR -10 to 3000 µmol m-2 s-1; relative humidity 0% to 100%; battery voltage 0 V to 17.5 V. Additionally, a code flags PAR data as "suspect" in data quality reports during electrical storm interference periods based on a test for PAR less than -10 µmol m-2 s-1...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Electrical storm interference on low-voltage passive PAR sensors | Short periods of artificially noisy measurements, often including negative PAR values that do not occur in the absence of electrical interference; flagged code tests for PAR measurements... | A code flags the PAR data as "suspect" in data quality reports for each data set based on the test; this test is largely effective but not 100%... | (hb p. 12) |
| Shadow-induced noise from trees or clouds | Large short-term fluctuations in PAR measurements and high standard deviations of measurements within each 1-minute averaging interval | - | (hb p. 12) |
| Missing value flag | Value equal to missing_value -9999, flagged via bit_1 in qc variable | flag_method = bit; bit_1_description used to mark equal to missing_value -9999 | (hb p. 10) |
| Out-of-range values below valid_min | PAR value less than -10 µmol m-2 s-1 (or RH less than 0%, or battery voltage less than 0V), flagged via bit_2 in qc variable | flag_method = bit; bit_2_description flags value less than valid_min | (hb p. 10) |
| Out-of-range values above valid_max | PAR value greater than 3000 µmol m-2 s-1 (or RH greater than 100%, or battery voltage greater than 17.5V), flagged via bit_3 in qc variable | flag_method = bit; bit_3_description flags value greater than valid_max | (hb p. 10) |
| Enclosure humidity/condensation risk | Internal humidity sensor readings exceeding 80%, potential for liquid water damaging electrical components | Replace desiccant packs inside the enclosure with fresh packs when humidity exceeds 80%. | (hb p. 11) |
| Physical obstruction of sensor optics | Anomalously low or altered PAR readings due to dust, litter, or bird droppings on sensor | Routine maintenance includes checking for obstructions, cleaning, and sensor leveling as needed. | (hb p. 11) |
| Sensor misleveling | Systematic bias in PAR readings due to non-horizontal or non-vertical sensor orientation | Sensor leveling performed as needed during routine maintenance. | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Mentors replace PAR sensors with recently calibrated sensors and perform calibrations of previously deployed sensors at LBNL for re-deployment; calibration is conducted by comparing paired measurements of natural sunlight against a set of 10 reference sensors, while installed on a shared, machine-leveled surface over... (hb p. 11) |
| Calibration interval | approximately annually (hb p. 11) |
| Traceability | ± 5% traceable to U.S. National Institute of Standards and Technology (hb p. 11) |
| Routine maintenance | Humidity inside the enclosure is monitored to avoid liquid water condensation which could damage electrical components; when humidity inside the enclosure exceeds 80%, desiccant packs inside the enclosure should be replaced with fresh packs. Routine maintenance of PAR sensors should include checking for obstructions... (hb p. 11) |
| Maintenance interval | as needed / when humidity exceeds 80% (hb p. 11) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: WXT520/530 meteorological instrument system (METWXT), infrared thermometer (IRT).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `PAR` | photosynthetically active radiation (400-700-nm wavelength) |
| `PPFD` | photosynthetic photon flux density (µmol m-2 s-1) |
| `A/C` | alternating current |
| `ARM` | Atmospheric Radiation Measurement |
| `BNF` | Bankhead National Forest |
| `IRT` | infrared thermometer |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `METWXT` | WXT520/530 meteorological instrument system |
| `RH` | relative humidity |


### References the handbook cites

- PAR calibration procedure manuscript in preparation. To be added.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-319.pdf (13 pages, DOE/SC-ARM-TR-319, by AB Moyes, SC Biraud)
- Catalog record: ARM data-source index, `instrument_class_code=par`, read 2026-09-23
- Example file: `bnfparS14.b1.20260919.000000.nc` from `bnfparS14.b1`, 0.17 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
