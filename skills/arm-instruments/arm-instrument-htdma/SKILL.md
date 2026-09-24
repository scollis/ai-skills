---
name: arm-instrument-htdma
description: ARM Humidified Tandem Differential Mobility Analyzer (htdma) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol particle size, Aerosol particle concentration, Relative humidity, Growth factor, Hygroscopicity parameter kappa, Sample temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaoshtdmaC1.b1) and the variable inventory of a real file. Use when working with htdma data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - htdma, Humidified Tandem Differential Mobility Analyzer, enaaoshtdmaC1.b1, Aerosol particle size, Aerosol particle concentration, Relative humidity, Growth factor, Hygroscopicity parameter kappa, Sample temperature, Aerosols, Brechtel Manufacturing, Inc. (BMI), HSEMS, HTDMA, NIST, SEMS.
---

# HTDMA - Humidified Tandem Differential Mobility Analyzer

The HTDMA measures how ambient aerosol particles of selected dry sizes grow or shrink in size when exposed to controlled relative humidity, deployed as a fixed ground-based instrument system (SEMS + HSEMS) at ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `htdma` |
| Handbook | [DOE/SC-ARM-TR-161 / J Uin / April 2024](https://www.arm.gov/publications/tech_reports/handbooks/htdma_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Brechtel Manufacturing, Inc. (BMI), HTDMA Model 3002 (consisting of SEMS and HSEMS units) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution; Hygroscopic growth |
| Record | 2012-11-16 to 2026-09-23 (active) |
| Datastreams with data | 26 across 17 sites |
| Sites | acx, anx, asi, awr, bnf, crg, ena, epc, guc, hou, mag, mar, mos, oli |
| ARM page | https://www.arm.gov/capabilities/instruments/htdma |


## Credit

Everything this skill knows about the instrument is the work of **J Uin** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin. *3002 Humidified Tandem Differential Mobility Analyzer (HTDMA) Instrument Handbook*, DOE/SC-ARM-TR-161, April 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/htdma_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Dry monodisperse particles are selected using an upstream DMA (DMA #1) based on their electrical mobility, which is related to particle size. These selected particles are then exposed to a controlled RH in a humidification system upstream of a second DMA (DMA #2). The voltage in the second DMA is scanned over time to determine changes in particle size due to water uptake, producing a size distribution of the humidified particles. A condensation particle counter (CPC) downstream of the second DMA counts particles as a function of selected size to obtain this size distribution. The growth factor (humidified size/dry size) and the hygroscopicity parameter kappa are calculated from this size distribution and the selection size of the upstream DMA.

**Siting.** During deployments, the instrument is operated in an air-conditioned enclosure and care is taken to minimize temperature changes, since HTDMA operation is sensitive to temperature fluctuations and low RH of the ambient aerosol sample (e.g., arctic conditions).

**Sampling.** reported every Output data recorded after each size distribution scan, typically every 10 minutes (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle size (selected initial size and humidified... | nanometers (nm) | 20 to 2,500 nm | approximately ±1% | - | (hb p. 10) |
| Aerosol particle concentration | particles per cubic... | 0 to 100,000 cm-3 | - | - | (hb p. 10) |
| Relative humidity (RH) | dimensionless (%) | 2 to 93% | ±4% | - | (hb p. 10) |
| Growth factor | dimensionless | - | - | - | (hb p. 10) |
| Hygroscopicity parameter kappa | - | - | - | - | (hb p. 8) |
| Sample temperature | - | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Particle size range | 20 to 2,500 nm | (hb p. 10) |
| Particle concentration range | 0 to 100,000 cm-3 | (hb p. 10) |
| RH range | 2 to 93% | (hb p. 10) |
| Particle sizing accuracy | 10 nm (based on NIST traceable monodisperse PSL calibration aerosols) | (hb p. 10) |
| Humidification system accuracy | 1% | (hb p. 10) |
| Particle concentration measurement accuracy (CPC flow set... | 3% | (hb p. 10) |
| Particle sizing repeatability | within 10 nm between each successive particle size measurement | (hb p. 11) |
| Humidification system repeatability | within 0.8% between each successive RH measurement | (hb p. 11) |
| Particle concentration measurement repeatability | within 1% between successive concentration measurements | (hb p. 11) |
| Particle sizing uncertainty | approximately ±1% | (hb p. 11) |
| RH measurement uncertainty | ±4% | (hb p. 11) |
| Vacuum source requirement | 20 lpm, 15'' Hg | (hb p. 13) |
| Compressed dry-air source requirement | 20 lpm max, 15 psig | (hb p. 13) |
| SEMS/HSEMS weight | more than 50 kg or 110 lbs each | (hb p. 15) |


## The data

Verified example: **`enaaoshtdmaC1.b1`**, file `enaaoshtdmaC1.b1.20230521.000413.nc`
(0.62 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=231, `bound`=2, `bin`=60 |
| Data variables | 53 |
| QC variables | 13 (`qc_` companions) |
| Median time step | 374 s |
| File time span | 2023-05-21T00:04:13 to 2023-05-21T23:57:38 |
| dod version | aoshtdma-b1-1.0 |
| process version | ingest-aoshtdmacorr-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `dma_rh_avg` | % | time | yes | Average relative humidity in DMA2 (HSEMS) during humid scan |
| `dry_diameter_setting` | nm | time | yes | Dry aerosol diameter size instrument setting |
| `dry_pressure` | hPa | time | yes | Dry sample pressure |
| `dry_rh` | % | time | yes | Dry aerosol particle relative humidity |
| `dry_temperature` | degC | time | yes | Dry sample temperature |
| `excess_flow_avg` | L/min | time | yes | Average excess sheath flow in DMA2 (HSEMS) during humid scan |
| `hd_rh_avg` | % | time | yes | Average relative humidity in the humidifier during humid scan |
| `humid_sheath_flow_avg` | L/min | time | yes | Average sheath flow in DMA2 (HSEMS) during humid scan |
| `pressure_avg` | hPa | time | yes | Average sample pressure in DMA2 (HSEMS) during humid scan |
| `temperature_avg` | degC | time | yes | Average sample temperature in DMA2 (HSEMS) during humid scan |
| `total_concentration` | 1/cm^3 | time | yes | Total scan concentration over all bins |
| `upstream_excess_flow_avg` | L/min | time | yes | Average excess sheath flow in DMA1 (SEMS) during humid scan |
| `upstream_sheath_flow_avg` | L/min | time | yes | Average sheath flow in DMA1 (SEMS) during humid scan |
| `aerosol_concentration` | 1/cm^3 | time,bin | - | Concentration of aerosol |
| `bin_center` | nm | time,bin | - | Bin center value |
| `cpc_b_avg` | 1/cm^3 | time | - | Average particle concentration measured by external MCPC during humid... |
| `cpc_b_std` | 1/cm^3 | time | - | Standard deviation of the particle concentration measured by external... |
| `dma_rh_std` | % | time | - | Standard deviation of the relative humidity in DMA2 (HSEMS) during... |
| `excess_flow_std` | L/min | time | - | Standard deviation of the excess sheath flow in DMA2 (HSEMS) during... |
| `growth_factor` | 1 | time,bin | - | Hygroscopic growth factor |
| `hd_rh_std` | % | time | - | Standard deviation of the relative humidity in the humidifier during... |
| `humid_sheath_flow_std` | L/min | time | - | Standard deviation of the sheath flow in DMA2 (HSEMS) during humid... |
| `kappa` | 1 | time,bin | - | Hygroscopicity parameter kappa |
| `num_bins` | 1 | time | - | Number of distribution bins |
| `pressure_std` | hPa | time | - | Standard deviation of the sample pressure in DMA2 (HSEMS) during... |
| `scan_max_diameter_setting` | nm | time | - | Maximum aerosol particle diameter instrument setting |
| `scan_min_diameter_setting` | nm | time | - | Minimum aerosol particle diameter instrument setting |
| `scan_time_setting` | s | time | - | Humidified DMA scanning time instrument setting |
| `temperature_std` | degC | time | - | Standard deviation of the sample temperature in DMA2 (HSEMS) during... |
| `time` | - | time | - | Time offset from midnight |


_2 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaoshtdmaC1.b1", "2023-05-21", "2023-05-21")
ds = armlive_open("enaaoshtdmaC1.b1", "2023-05-21", "2023-05-21", cleanup_qc=True)
```

This datastream carries 53 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enaaoshtdmaC1.b1", start, end,
                  keep_variables=["dma_rh_avg", "dry_diameter_setting", "dry_pressure", "qc_dma_rh_avg", "qc_dry_diameter_setting", "qc_dry_pressure"])
```

## Quality control in this datastream

13 `qc_` companion variables cover 13 of the
53 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaoshtdmaC1.b1.20230521.000413.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `total_concentration` | Value is less than warn_min. | 136 | 58.8745 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaoshtdmaC1.b1", "20121116", "20260923")
```

The handbook's own note on data quality: Data quality evaluation involves automatic generation of plots, in collaboration with the ARM Data Quality Office: (1) humidified aerosol total particle concentrations (per ambient aerosol selection size) over time should be above 0, follow the same general trend, and not fluctuate erratically, indicating internal CPC is not out of butanol or flooded and air flows/pressures are stable; (2) humidifier RH should be close to 90%, with values below 85% indicating an issue with water level, temperature, or air flows.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sensitivity to temperature fluctuations | Instability or drift in RH/growth factor measurements when ambient temperature changes | Operate the instrument in an air-conditioned enclosure and minimize temperature changes | (hb p. 10) |
| Low RH of ambient aerosol sample (e.g., arctic conditions) | Degraded HTDMA operation/measurement quality in very low ambient RH environments | - | (hb p. 10) |
| Particle coincidence at higher concentrations | Undercounting or nonlinearity in particle concentration measurements at high particle concentrations | Accounted for in instrument software based on manufacturer comparison experiments with an aerosol electrometer and commercial CPCs | (hb p. 10) |
| Limited particle growth from condensation at lower particle sizes | Reduced counting efficiency/sensitivity for smaller particle sizes in the CPC | Accounted for in instrument software based on manufacturer comparison experiments | (hb p. 10) |
| Insufficient butanol in internal CPC (HSEMS) | Humidified aerosol total particle concentrations drop to or near 0 in time series | Data quality plots monitor that concentrations stay above 0; refill butanol bottle when below 50% | (hb p. 9) |
| Flooded internal CPC or unstable air flows/pressures | Erratic fluctuation in humidified aerosol total particle concentrations that does not follow expected general trend | Monitored via automatically generated data quality plots in collaboration with ARM Data Quality Office | (hb p. 9) |
| Humidifier RH deviation from setpoint | Humidifier RH reading below 85% (target is close to 90%) | Indicates an issue with water level, temperature, or air flows; should be checked/corrected | (hb p. 10) |
| Growth factor deviation from theoretical Kohler model curve | Measured growth factor curve for calibration aerosol (ammonium sulfate/nitrate) differs from theoretical Kohler model curve by more than manufacturer-specified accuracy value | Investigated on a case-by-case basis and corrected by instrument mentors | (hb p. 14) |
| Intermittent appearance of size distributions in plots | Visibly intermittent nature of the size distributions in time-series plots | This is due to different ambient aerosol selection sizes being repeated periodically, not an instrument fault | (hb p. 8) |
| Butanol is flammable and toxic if inhaled (internal CPC working fluid) | Safety hazard rather than data artifact; relevant to instrument handling | Follow safety precautions when handling butanol | (hb p. 15) |
| SEMS impactor fouling | Impactor status light in main software window turns red | Clean the SEMS impactor when status light turns red | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Manufacturer's calibration includes measuring the size distribution of a NIST traceable monodisperse calibration aerosol (PSL) to validate DMA operation, measuring growth factor of generated aerosol particles with known chemical composition (ammonium sulfate or ammonium nitrate) as a function of RH and comparing to... (hb p. 14) |
| Calibration interval | every six or twelve months (by instrument mentors); also calibrated/validated by manufacturer prior to delivery and during routine maintenance at manufacturing facilities (hb p. 14) |
| Traceability | NIST traceable monodisperse calibration aerosols (PSL); NIST traceable factory calibrations of built-in hygrometers; DryCal calibration standard for flows (hb p. 14) |
| Routine maintenance | Fill the water bottle when water level is below 50%; fill the butanol bottle when butanol level is below 50%; empty the drain bottle when the butanol bottle is filled or if liquid level exceeds 50%; clean the SEMS impactor when the impactor status light in the main software window turns red. (hb p. 15) |
| Maintenance interval | As needed based on level/status indicators (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: TDMA, SEMS, HSEMS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AC` | alternating current |
| `ARM` | Atmospheric Radiation Measurement |
| `BMI` | Brechtel Manufacturing, Inc. |
| `CPC` | condensation particle counter |
| `DMA` | differential mobility analyzer |
| `HSEMS` | Humidified Scanning Electrical Mobility System |
| `HTDMA` | humidified tandem differential mobility analyzer |
| `NIST` | National Institute of Standards and Technology |
| `PSL` | polystyrene latex |
| `RH` | relative humidity |
| `SEMS` | Scanning Electrical Mobility System |
| `UTC` | Coordinated Universal Time |


### References the handbook cites

- Brechtel FJ, and SM Kreidenweis. 2000a. "Predicting particle critical supersaturation from hygroscopic growth measurements in the humidified TDMA. Part I: Theory and sensitivity studies." Journal of the Atmospheric...
- Brechtel FJ, and SM Kreidenweis. 2000b. "Predicting particle critical supersaturation from hygroscopic growth measurements in the humidified TDMA. Part II: Laboratory and ambient studies." Journal of the Atmospheric...
- Hennig, T, A Massling, FJ Brechtel, and A Wiedensohler. 2005. "A tandem DMA for highly temperature-stabilized hygroscopic particle growth measurements between 90% and 98% relative humidity." Journal of Aerosol Science...
- Knutson, EO, and KT Whitby. 1975. "Aerosol classification by electric mobility: Apparatus, theory, and applications." Journal of Aerosol Science 6(6):443-451
- Lopez-Yglesias, XF, MC Yeung, SE Dey, FJ Brechtel, and CK Chan. 2014. "Performance evaluation of the Brechtel Mfg. Humidified Tandem Differential Mobility Analyzer (BMI HTDMA) for studying hygroscopic properties of...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/htdma_handbook.pdf (17 pages, DOE/SC-ARM-TR-161, by J Uin)
- Catalog record: ARM data-source index, `instrument_class_code=htdma`, read 2026-09-23
- Example file: `enaaoshtdmaC1.b1.20230521.000413.nc` from `enaaoshtdmaC1.b1`, 0.62 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
