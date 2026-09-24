---
name: arm-instrument-sebs
description: ARM Surface Energy Balance System (sebs) - handbook-derived instrument reference: measurement principle, reported quantities (surface_energy_balance, surface_soil_heat_flux_avg, net radiation, wetness, down_short_hemisp, up_short_hemisp, down_long, up_long), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enasebsC1.b1) and the variable inventory of a real file. Use when working with sebs data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface/Subsurface Properties. Triggers - sebs, Surface Energy Balance System, enasebsC1.b1, surface_energy_balance, surface_soil_heat_flux_avg, net radiation, wetness, down_short_hemisp, up_short_hemisp, Surface/Subsurface Properties, Net Radiometer: CNR4/CNF4 by Kipp & Zonen, Wetness: DRD11A Rain Detector by Vaisala, EBBR, ECOR, IMMS, NetCDF.
---

# SEBS - Surface Energy Balance System

The SEBS measures the surface radiation and soil energy balance—via upwelling/downwelling solar and infrared radiation, wetness, and soil heat flux/moisture/temperature—deployed collocated with eddy correlation flux measurement systems (ECOR) at ARM observatories to compare with ECOR sensible and latent heat fluxes.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sebs` |
| Handbook | [DOE/SC-ARM-TR-092 / DR Cook, RC Sullivan / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/sebs_handbook.pdf) |
| Measurement category | Surface/Subsurface Properties |
| Manufacturer / model | Net Radiometer: CNR4/CNF4 by Kipp & Zonen; Wetness: DRD11A Rain Detector by Vaisala, Inc.; Soil Heat Flow: HFT-3 by Radiation and Energy Balance Systems, Inc. (HFP01 by Hukseflux at AMF1 beginning at... |
| Primary measurements | Longwave broadband downwelling irradiance; Longwave broadband upwelling irradiance; Net broadband total irradiance; Shortwave broadband total downwelling irradiance; Shortwave broadband total upwelling irradiance; Soil heat flux |
| Record | 2010-10-01 to 2026-09-23 (active) |
| Datastreams with data | 43 across 19 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mao, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/sebs |


## Credit

Everything this skill knows about the instrument is the work of **DR Cook, RC Sullivan** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> DR Cook, RC Sullivan. *Surface Energy Balance System (SEBS) Instrument Handbook*, DOE/SC-ARM-TR-092, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sebs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The surface energy balance is determined from the net radiometer and soil sensor measurements. Upwelling and downwelling solar and infrared radiation measurements are combined to determine net radiation, with net radiometer measurements adjusted to compensate for the temperature of the net radiometer body. Soil measurements are performed by three sets of soil heat flow (5 cm depth), soil temperature (0-5 cm average, 2.5 cm at AMF1 beginning at CRG and AMF3 beginning at BNF), and soil moisture (centered at 2.5 cm) probes; soil heat flow is adjusted for the effect of soil moisture above the soil heat flow plate (not at AMF1 beginning at CRG and AMF3 beginning at BNF). The storage of energy in the soil above the soil heat flow plate is determined from the change in soil temperature with time. Measurements from the three sets of soil probes are combined to give an average soil surface heat flux, which is combined with net radiation to produce an estimate of the surface energy balance.

**Siting.** In a typical arrangement, the ECOR/SEBS system is placed on the north side of a crop field; the net radiometer is attached to the end of the ECOR boom, beneath the mount that holds the sonic and CO2/H2O sensor heads, at approximately 3 m above ground level (15 m height at SGP site EF21 forest). The wetness sensor is mounted on the top of the boom, midway between the two ends of the boom. The soil sensors are buried in the soil under the sonic and CO2/H2O sensor heads. The net radiometer is pointed due south. The sign convention for radiometer, net radiation, change of energy storage, and soil heat flux measurements is: positive towards the soil surface and negative away from the surface.

**Sampling.** reported every 30 minutes; averaging Thirty-minute average measurements are stored within the CR1000 data logger; the SEBS timestamp is the end of the half hour. (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| surface_energy_balance | - | - | 5% | - | (hb p. 8) |
| surface_soil_heat_flux_avg | - | - | 10% | - | (hb p. 8) |
| net radiation | - | - | 5% | - | (hb p. 8) |
| wetness | - | - | 5% | - | (hb p. 8) |
| down_short_hemisp | - | - | - | - | (hb p. 9) |
| up_short_hemisp | - | - | - | - | (hb p. 9) |
| down_long | - | - | - | - | (hb p. 9) |
| up_long | - | - | - | - | (hb p. 9) |
| surface_soil_heat_flux_1/2/3 | - | - | - | - | (hb p. 9) |
| soil_moisture_1/2/3 | - | - | - | - | (hb p. 9) |
| soil_temp_1/2/3 | - | - | - | - | (hb p. 9) |
| soil_heat_flow_1/2/3 | - | - | - | - | (hb p. 9) |
| corr_soil_heat_flow_1/2/3 | - | - | - | - | (hb p. 9) |
| soil_heat_capacity_1/2/3 | - | - | - | - | (hb p. 9) |
| energy_storage_change_1/2/3 | - | - | - | - | (hb p. 9) |
| albedo | - | - | - | - | (hb p. 9) |
| temp_net_radiometer | - | - | - | - | (hb p. 9) |
| battery_voltage | - | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Net Radiometer Spectral range (shortwave) | 300 to 2800 nm | (hb p. 13) |
| Net Radiometer Spectral range (longwave) | 4500 to 42000 nm | (hb p. 13) |
| Net Radiometer Sensitivity | 5 to 20 µV/W/m² | (hb p. 13) |
| Net Radiometer Temperature dependence of sensitivity (-10... | less than  4% | (hb p. 13) |
| Net Radiometer Response time | less than  18 s | (hb p. 13) |
| Net Radiometer Non-linearity | less than  1 % | (hb p. 13) |
| Net Radiometer Operating temperature | -40 to 80 °C | (hb p. 13) |
| Net Radiometer International standards (WMO) | Good Quality WMO | (hb p. 13) |
| Net Radiometer Ventilation power | 10 W | (hb p. 13) |
| Wetness Range | 1 to 3 V DC (3 V dry, 1 V wet) | (hb p. 13) |
| Soil Heat Flow Range (HFT-3) | +/- 10 mV | (hb p. 13) |


## The data

Verified example: **`enasebsC1.b1`**, file `enasebsC1.b1.20260919.000000.cdf`
(0.04 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=48, `bound`=2 |
| Data variables | 70 |
| QC variables | 32 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:30:00 |
| sampling interval | 5 seconds |
| averaging interval | 30 minutes |
| dod version | sebs-b1-1.6 |
| process version | ingest-sebs-1.10-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `albedo` | 1 | time | yes | Albedo |
| `battery_voltage` | V | time | yes | Battery voltage |
| `corr_soil_heat_flow_1` | W/m^2 | time | yes | Soil heat flow 1, corrected for soil moisture |
| `corr_soil_heat_flow_2` | W/m^2 | time | yes | Soil heat flow 2, corrected for soil moisture |
| `corr_soil_heat_flow_3` | W/m^2 | time | yes | Soil heat flow 3, corrected for soil moisture |
| `down_long` | W/m^2 | time | yes | Sky longwave irradiance |
| `down_short_hemisp` | W/m^2 | time | yes | Downwelling shortwave hemispheric irradiance |
| `energy_storage_change_1` | W/m^2 | time | yes | Change in energy storage 1, 0-5 cm soil layer |
| `energy_storage_change_2` | W/m^2 | time | yes | Change in energy storage 2, 0-5 cm soil layer |
| `energy_storage_change_3` | W/m^2 | time | yes | Change in energy storage 3, 0-5 cm soil layer |
| `net_radiation` | W/m^2 | time | yes | Net radiation |
| `soil_heat_capacity_1` | MJ/m^3/degC | time | yes | Soil heat capacity 1 |
| `soil_heat_capacity_2` | MJ/m^3/degC | time | yes | Soil heat capacity 2 |
| `soil_heat_capacity_3` | MJ/m^3/degC | time | yes | Soil heat capacity 3 |
| `soil_heat_flow_1` | W/m^2 | time | yes | Soil heat flow 1 |
| `soil_heat_flow_2` | W/m^2 | time | yes | Soil heat flow 2 |
| `soil_heat_flow_3` | W/m^2 | time | yes | Soil heat flow 3 |
| `soil_moisture_1` | % | time | yes | Soil moisture 1, volumetric |
| `soil_moisture_2` | % | time | yes | Soil moisture 2, volumetric |
| `soil_moisture_3` | % | time | yes | Soil moisture 3, volumetric |
| `soil_temp_1` | degC | time | yes | Soil temperature 1 |
| `soil_temp_2` | degC | time | yes | Soil temperature 2 |
| `soil_temp_3` | degC | time | yes | Soil temperature 3 |
| `surface_energy_balance` | W/m^2 | time | yes | Surface energy balance |
| `surface_soil_heat_flux_1` | W/m^2 | time | yes | Surface soil heat flux 1 |
| `surface_soil_heat_flux_2` | W/m^2 | time | yes | Surface soil heat flux 2 |
| `surface_soil_heat_flux_3` | W/m^2 | time | yes | Surface soil heat flux 3 |
| `surface_soil_heat_flux_avg` | W/m^2 | time | yes | Surface soil heat flux, average of fluxes 1-3 |
| `temp_net_radiometer` | degC | time | yes | Net radiometer temperature |
| `up_long` | W/m^2 | time | yes | Surface longwave irradiance |


_3 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enasebsC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("enasebsC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

This datastream carries 70 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enasebsC1.b1", start, end,
                  keep_variables=["albedo", "battery_voltage", "corr_soil_heat_flow_1", "qc_albedo", "qc_battery_voltage", "qc_corr_soil_heat_flow_1"])
```

## Quality control in this datastream

32 `qc_` companion variables cover 32 of the
70 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enasebsC1.b1.20260919.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `corr_soil_heat_flow_1` | Value is equal to missing_value. | 48 | 100.0 |
| `corr_soil_heat_flow_2` | Value is equal to missing_value. | 48 | 100.0 |
| `corr_soil_heat_flow_3` | Value is equal to missing_value. | 48 | 100.0 |
| `down_short_hemisp` | Value is less than the fail_min. | 23 | 47.9167 |
| `up_short_hemisp` | Value is less than the fail_min. | 23 | 47.9167 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enasebsC1.b1", "20101001", "20260923")
```

The handbook's own note on data quality: The b1 data file contains basic data quality flags for most important variables (bit values: 0x0=within range, 0x1=missing_value, 0x2=less than valid_min, 0x4=greater than valid_max, 0x8=failed valid_delta check). Visual QC frequency is daily to weekly, with a typical QC delay of 1-3 days. Instrument mentor routinely views graphic displays including day-course plots of all calculated quantities and comparison plots with collocated ECOR, SEBS, EBBR, and MET data. Monthly reviews were prepared by the mentor and submitted to the IMMS report database until late 2014. DQRs are not written for...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Nighttime negative solar radiation offsets | Upwelling and downwelling solar radiation measurements often exhibit small negative values at night; these values are not physically real (instrument offsets). | These are known instrument offsets; no DQR is written for this condition. | (hb p. 4) |
| Wetness sensor icing artifact | The wetness values go below the lower limit when icing occurs, and spike above the upper limit after the ice melts; most frequent at NSA and Oliktok Point, Alaska (OLI), but can occur... | - | (hb p. 4) |
| Nuisance QC flags from solar radiation offsets | Upwelling/downwelling minimum solar radiation flags are frequently tripped at night, exhibiting small negative values that are not physically real. | - | (hb p. 5) |
| Legitimate values falling outside QC limits | Times when legitimate values fall outside the QC limits, particularly for upwelling and downwelling solar radiation. | - | (hb p. 5) |
| Vegetation/surface differences limit cross-site comparison | Upwelling radiometer and surface soil heat flux measurements from two adjacent sites may not be similar unless the ground is snow-covered; comparisons at SGP E21 (forest) versus other SGP... | Use caution comparing sites with different vegetation surfaces; only downwelling radiation and wetness are generally comparable. | (hb p. 5) |
| EBBR vs SEBS comparison limitations | Net radiation and surface soil heat flux measurements from EBBR and SEBS at E13/E14 will probably not be similar unless the ground is snow-covered. | Use caution due to differing vegetation surfaces seen by the two systems. | (hb p. 6) |
| Net radiometer temperature discrepancy vs MET/ECOR | SEBS net radiometer temperature (body temperature) is normally expected to be higher than MET temperature and ECOR sonic temperature, but may be lower than the LI-7500 CO2/H2O analyzer... | No direct measurement comparison possible between systems. | (hb p. 6) |
| Flat-lined/unchanging measurements | Measurements that do not change at all over several hours (particularly if flat-lined) may not be correct. | Check QC flags in the SEBS data. | (hb p. 6) |
| Water/precipitation/dew/frost obstruction on radiometer domes | Periods of precipitation, fog, and dew (frost) cause water lying on the upper domes of the net radiometer, obstructing shortwave and longwave radiation passage; offscale or spiked readings... | No DQRs written for this wetting condition; user should check SEBS wetness measurement, collocated/nearby MET rain gauges, or DQ Explorer ECOR plots... | (hb p. 6) |
| Spikes during heavy precipitation | Large spikes (positive and negative) in surface_energy_balance and surface_soil_heat_flux_avg can occur when precipitation is heavy, caused by temperature of water flowing into soil and... | - | (hb p. 6) |
| Canopy underestimation of heat flux | Under vegetation canopies (particularly tall vegetation), the soil surface heat flux probably underestimates the heat flux from the top of the canopy. | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | All sensors are factory calibrated. Periodic in situ checks of the net radiometer calibrations are possible, but are not normally needed for years. All sensors would be returned to the vendor for factory calibration, if needed. (hb p. 8) |
| Calibration interval | Not normally needed for years (hb p. 8) |
| Traceability | Vendor factory calibration (hb p. 8) |
| Routine maintenance | No single comprehensive user manual for the SEBS system is available for general use; vendor-supplied documentation on sensors and a collection of procedures prepared by the mentor are provided for internal use by Site Operations. (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ECOR, EBBR, MET.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `BNF` | Bankhead National Forest |
| `CF` | Central Facility |
| `CRG` | Coast-Urban-Rural Atmospheric Gradient Experiment (CoURAGE) |
| `DC` | direct current |
| `DOE` | U.S. Department of Energy |
| `DQR` | Data Quality Report |
| `EBBR` | energy balance Bowen ratio system |
| `ECOR` | eddy correlation flux measurement system |
| `EF` | extended facility |
| `ENA` | Eastern North Atlantic |
| `IMMS` | Instrument Mentor Monthly Summary |
| `MET` | surface meteorological instrumentation |


### References the handbook cites

- Cook, DR, ML Fischer, and DJ Holdridge. 2006. "Comparison of ECOR, EBBR, and CO2FLX System Fluxes." Sixteenth ARM Science Team Meeting, Albuquerque, New Mexico.
- Kyrouac, J, and Y Hamada. 2018. "Comparison between co-located soil moisture measurements at the ARM Southern Great Plains (SGP) Central Facility." Poster, 2018 ARM/ASR PI Meeting, Vienna, Virginia, 19-24 March.
- Webb, EK, GI Pearman, and R Leuning. 1980. "Correction of flux measurements for density effects due to heat and water vapour transfer." Quarterly Journal of the Royal Meteorology Society 106(44): 85-100,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sebs_handbook.pdf (16 pages, DOE/SC-ARM-TR-092, by DR Cook, RC Sullivan)
- Catalog record: ARM data-source index, `instrument_class_code=sebs`, read 2026-09-23
- Example file: `enasebsC1.b1.20260919.000000.cdf` from `enasebsC1.b1`, 0.04 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
