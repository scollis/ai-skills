---
name: arm-instrument-amc
description: ARM Ameriflux Measurement Component (amc) - handbook-derived instrument reference: measurement principle, reported quantities (Soil volumetric water content, Soil temperature, Soil bulk electrical conductivity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaamcC1.b1) and the variable inventory of a real file. Use when working with amc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Radiometric; Surface/Subsurface Properties. Triggers - amc, Ameriflux Measurement Component, nsaamcC1.b1, Soil volumetric water content, Soil temperature, Soil bulk electrical conductivity, Radiometric, Surface/Subsurface Properties, Campbell Scientific CS650L (NSA VWC/soil temp sensors), Campbell Scientific CS655 (OLI, LBNL.
---

# AMC - Ameriflux Measurement Component

The AmeriFlux Measurement Component (AMC) is an in-situ tripod-mounted system deployed within the flux footprint of ARM eddy correlation systems that measures soil temperature and volumetric water content at two depths across six microsites, plus upwelling and downwelling photosynthetically active radiation (PAR), to support interpretation of methane flux measurements.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `amc` |
| Handbook | [DOE/SC-ARM-TR-143 / K Reichl, S Biraud, A Moyes / April 2026](https://www.arm.gov/publications/tech_reports/handbooks/amc_handbook.pdf) |
| Measurement category | Radiometric; Surface/Subsurface Properties |
| Manufacturer / model | Campbell Scientific CS650L (NSA VWC/soil temp sensors); Campbell Scientific CS655 (OLI, SGP VWC/soil temp sensors); Kipp & Zonen PQS-1 (PAR sensors) |
| Primary measurements | Photosynthetically Active Radiation; Soil moisture; Soil temperature |
| Record | 2012-08-08 to 2024-11-22 (retired) |
| Datastreams with data | 3 across 3 sites |
| Sites | nsa, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/amc |


## Credit

Everything this skill knows about the instrument is the work of **K Reichl, S Biraud, A Moyes** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Reichl, S Biraud, A Moyes. *AmeriFlux Measurement Component Instrument Handbook*, DOE/SC-ARM-TR-143, April 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/amc_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Soil water content is measured using water content reflectometers in which a differential emitter-coupled logic oscillator drives two parallel stainless-steel rods that form an open-ended transmission line; the wave propagation velocity along the rods depends on the dielectric permittivity of the surrounding soil, which increases with water content and slows propagation, so the two-way travel time (oscillation period) is related to water content. Signal attenuation from soil electrical conductivity increases oscillation period at a given water content, so an electrical conductivity measurement is used to correct the period before a calibration equation converts period and conductivity to bulk dielectric permittivity. The Topp equation or a mentor-defined soil-specific calibration then converts permittivity to volumetric water content (VWC). PAR is measured by the Kipp & Zonen PQS-1 sensor, where irradiance E (µmol/m2/s) is calculated as the ratio of the sensor's output voltage U (µV) to a sensitivity factor S (µV/µmol/m2/s) determined by calibration of each sensor.

**Siting.** System consists of 12 combination soil temperature/VWC reflectometers and one set of up/down-welling PAR sensors deployed within the fetch of the eddy correlation flux measurement system at each site. Soil sensors are placed at two depths (10 and 30 cm below the vegetation layer) at six microsite locations to monitor soil property inhomogeneity across the landscape. Sensors are installed horizontally, parallel to the earth surface, in pits 40 cm long by 15 cm wide by 33 cm deep; deeper sensor is inserted first, then soil replaced and the shallower sensor installed at the same location. Sensor cables are wrapped in stainless steel cable armor and sealed with electrical tape to minimize...

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Soil volumetric water content (VWC) | - | - | - | - | (hb p. 7) |
| Soil temperature | - | - | - | - | (hb p. 7) |
| Soil bulk electrical conductivity | - | - | - | - | (hb p. 3) |
| Upwelling and downwelling photosynthetically active... | µmol/m2/s | - | - | - | (hb p. 4) |


## The data

Verified example: **`nsaamcC1.b1`**, file `nsaamcC1.b1.20241119.000000.nc`
(0.26 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=48, `bound`=2 |
| Data variables | 332 |
| QC variables | 161 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2024-11-19T00:00:00 to 2024-11-19T23:30:00 |
| sampling interval | 5 minutes |
| averaging interval | 30 minutes |
| dod version | amc-b1-3.7 |
| process version | ingest-amc-1.10-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `batt_volt_min` | V | time | yes | Minimum battery voltage in 30 minute interval |
| `ec_1` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 1 |
| `ec_10` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 10 |
| `ec_10_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 10 |
| `ec_11` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 11 |
| `ec_11_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 11 |
| `ec_12` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 12 |
| `ec_12_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 12 |
| `ec_1_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 1 |
| `ec_2` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 2 |
| `ec_2_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 2 |
| `ec_3` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 3 |
| `ec_3_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 3 |
| `ec_4` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 4 |
| `ec_4_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 4 |
| `ec_5` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 5 |
| `ec_5_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 5 |
| `ec_6` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 6 |
| `ec_6_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 6 |
| `ec_7` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 7 |
| `ec_7_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 7 |
| `ec_8` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 8 |
| `ec_8_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 8 |
| `ec_9` | dS/m | time | yes | Average bulk soil electrical conductivity sensor 9 |
| `ec_9_std` | 1 | time | yes | Standard deviation in bulk soil electrical conductivity sensor 9 |
| `par_inc` | umol/m^2/s | time | yes | Average incident PAR |
| `par_inc_std` | 1 | time | yes | Standard deviation incident PAR |
| `par_ref` | umol/m^2/s | time | yes | Average reflected PAR |
| `par_ref_std` | 1 | time | yes | Standard deviation reflected PAR |
| `period_1` | us | time | yes | Average signal oscillation period sensor 1 |


_136 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsaamcC1.b1", "2024-11-19", "2024-11-19")
ds = armlive_open("nsaamcC1.b1", "2024-11-19", "2024-11-19", cleanup_qc=True)
```

This datastream carries 332 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("nsaamcC1.b1", start, end,
                  keep_variables=["batt_volt_min", "ec_1", "ec_10", "qc_batt_volt_min", "qc_ec_1", "qc_ec_10"])
```

## Quality control in this datastream

161 `qc_` companion variables cover 161 of the
332 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (nsaamcC1.b1.20241119.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `par_ref` | Value is less than fail_min. | 38 | 79.1667 |
| `par_inc` | Value is less than fail_min. | 9 | 18.75 |
| `ec_4_std` | Value is equal to missing_value. | 1 | 2.0833 |
| `ec_7_std` | Value is equal to missing_value. | 1 | 2.0833 |
| `ec_9_std` | Value is equal to missing_value. | 1 | 2.0833 |
| `ec_10_std` | Value is equal to missing_value. | 1 | 2.0833 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsaamcC1.b1", "20120808", "20260923")
```

The handbook's own note on data quality: Best data are those with qc_* values of 0. QC flag_method is "bit": bit_1 (value 1) = value equals missing_value -9999; bit_2 (value 2) = value less than valid_min; bit_3 (value 4) = value greater than valid_max. An additional QC bit (bit_4, value 8) applies to PAR sensors at NSA: "Instrument shaded, solar position is within region defined by solar_obstruction_azimuth_range and solar_obstruction_elevation_range."

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Soil bulk electrical conductivity attenuates the high-frequency signal on the probe rods,... | Apparent water content readings shift depending on soil solution electrical conductivity even without a true change in water content; comparisons across soils/sites at differing... | Increases in oscillation period from signal attenuation are corrected using an electrical conductivity measurement before conversion to permittivity | (hb p. 3) |
| Bulk electrical conductivity is temperature dependent (changes ~2% per degree Celsius) | Reported EC values drift with soil temperature independent of actual conductivity changes | Convert EC readings to a standard temperature (e.g., 25°C) using EC25 = ECT ÷ (1 + 0.023) × (Tsoil−25) | (hb p. 3) |
| VWC sensors do not report values during periods of water saturation using the... | Data gaps in vwc_* variables during saturated soil conditions | Use mentor-defined calibrated VWC (vwc_*_corr) at SGP and NSA, which has fewer data gaps because permittivity data were more continuous through... | (hb p. 5) |
| Differing VWC calibration methods and function types by site (Topp vs. mentor-defined;... | VWC values and their relationship to permittivity differ systematically between NSA, OLI, and SGP datastreams and are not directly comparable without accounting for calibration method | When available, use the VWC data from mentor-defined calibration functions (vwc_*_corr); recognize that OLI only has Topp-equation-based VWC while... | (hb p. 5) |
| 40-meter tower at NSA causes shading obstruction of PAR sensors | PAR values dip or are flagged during an approximately one-hour window each day throughout spring and summer months due to tower shadow | Automatically flagged in the ingested data using QC variables (bit_4, solar obstruction flag) | (hb p. 5) |
| Sensor cables vulnerable to animal chewing | Potential data gaps or erratic readings from damaged cables | Cables wrapped in stainless steel cable armor and sealed with electrical tape at each end | (hb p. 4) |
| Site-specific sensor depth/orientation assignment differs (which sensor number is shallow... | Sensor index numbers (1-12) do not correspond to the same depth across NSA, OLI, and SGP datastreams | Consult Table 2 for sensor depth assignment per site before comparing sensor numbers across sites | (hb p. 4) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | VWC: Topp equation (manufacturer-provided third-degree polynomial) for all sites; additionally mentor-defined, soil-specific calibration functions derived from gravimetric calibration experiments performed by the LBNL AmeriFlux QA/QC Calibration Laboratory are used at SGP and NSA (separate coefficients for shallow and... (hb p. 5) |
| Calibration interval | PAR sensors deployed are replaced every two years with sensors with updated calibration values; removed sensors are sent back to the Calibration Laboratory and assigned new calibration values before redeployment. (hb p. 5) |
| Traceability | Mentor-defined VWC calibration functions derived from gravimetric laboratory measurements of water content of soil cores collected on site, transported intact to LBNL, instrumented with sensors, wetted to field capacity, and slowly dried over several weeks. (hb p. 5) |
| Routine maintenance | PAR sensors are replaced every two years with sensors carrying updated calibration values; removed sensors are returned to the LBNL Calibration Laboratory and assigned new calibration values before redeployment. (hb p. 6) |
| Maintenance interval | two years (PAR sensor replacement) (hb p. 6) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ECOR, SEBS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `AMC` | AmeriFlux measurement component |
| `ARM` | Atmospheric Radiation Measurement |
| `DOE` | U.S. Department of Energy |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `NSA` | North Slope of Alaska |
| `OLI` | Oliktok Point, Alaska |
| `PAR` | photosynthetically active radiation |
| `QA` | quality assurance |
| `QC` | quality control |
| `SGP` | Southern Great Plains |
| `VWC` | volumetric water content |


### References the handbook cites

- Rhoades, JD, PAC Raats, and RJ Prather. 1976. "Effects of liquid-phase electrical conductivity, water content, and surface conductivity on bulk soil electrical conductivity." Journal of the Soil Science Society of...
- Rhoades, JD, NA Manteghi, PJ Shouse, and WJ Alves. 1989. "Soil electrical conductivity and soil salinity: New formulations and calibrations." Journal of the Soil Science Society of America 53(2): 433–439,...
- Topp, GC, JL Davis, and AP Annan. 1980. "Electromagnetic determination of soil water content: Measurements in coaxial transmission lines." Water Resources Research 16(3): 574–582, doi:10.1029/WR016i003p00574

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/amc_handbook.pdf (14 pages, DOE/SC-ARM-TR-143, by K Reichl, S Biraud, A Moyes)
- Catalog record: ARM data-source index, `instrument_class_code=amc`, read 2026-09-23
- Example file: `nsaamcC1.b1.20241119.000000.nc` from `nsaamcC1.b1`, 0.26 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
