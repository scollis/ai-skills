---
name: arm-vap-aafmerged
description: ARM ARM Aerial Facility (AAF) Merged VAP for Historical AAF G1 Field Campaigns (aafmerged) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Cloud particle size distribution, Cloud particle size distribution), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaafmergedF1.c1) and the variable inventory of a real file. Use when working with aafmerged data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Airborne Observations. Triggers - aafmerged, sgpaafmergedF1.c1, Cloud particle size distribution, Airborne Observations.
---

# AAFMERGED - ARM Aerial Facility (AAF) Merged VAP for Historical AAF G1 Field Campaigns

The AAFMERGED VAP is a value-added data product that merges up to 23 ARM Aerial Facility G-1 aircraft instrument datastreams (aerosol, cloud, trace gas, meteorological, and navigation measurements) onto a single common time grid to produce one consolidated netCDF file per G-1 flight for the historical 2013-2018 field campaigns.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 18 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aafmerged` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-299 / F Mei, K Gaustad / March 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-299.pdf) |
| Category | Airborne Observations |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2013-07-15 to 2024-03-01 (retired) |
| Datastreams with data | 7 across 7 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aafmerged |


## Credit

Everything this skill knows about the retrieval is the work of **F Mei, K Gaustad** -
the ARM developers and mentors who wrote the technical report it derives from:

> F Mei, K Gaustad. *ARM Aerial Facility (AAF) Merged Value-Added Product Report for Historical G-1 Field Campaigns*, DOE/SC-ARM-TR-299, March 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-299.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The AAFMERGED VAP does not apply any special algorithms or perform scientific analysis on the data retrieved and transformed; its sole purpose is to consolidate existing ARM G-1 airborne data products into a single file. It is produced using the ARM Data Integrator (ADI), a framework that automates data retrieval, integration, and creation of time-series netCDF data products, allowing users to combine data products, extract specific variables, and transform them into user-defined coordinate systems. The time dimension of the merged product aligns with the input aafnaviwg.c1 (navigation/met) datastream, and all other instrument data are mapped onto the aafnaviwg.c1 sampling period using ADI's nearest-neighbor transformation method. The nearest-neighbor method supports a range transformation parameter specifying a time window within which the next 'good' sample will be used if the closest sample to the target output time is bad or missing; this range is up to 30 minutes for all input datastreams except aafams.b1, for which the maximum range is 14s.

**Cadence.** output every Output time stamps match the aafnaviwg.c1 input file sample times; an aafmerged file is produced for each G-1 aircraft flight, and more than one flight per day produces multiple output files.; averaging Nearest-neighbor transformation with a range parameter of up to 30 minutes for all input datastreams except aafams.b1, which uses a maximum range of 14s. (hb p. 4).

## Inputs

The report names these instruments and sibling products: aafnaviwg, aaf2dsh, aaf2dsv, aafams, aafccn2cola, aafccn2colb, aafcpcfcvi, aafcpcfiso, aafcpcu, aafcdp, aaffims, aafhvps.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Cloud particle size distribution (2D stereo probe,... | μm | 10 to 3,000 μm | - | (hb p. 7) |
| Cloud particle size distribution (2D stereo probe, vertical) | μm | 10 to 3,000 μm | - | (hb p. 7) |
| Particle chemical composition/trace gas measurements (AMS) | - | - | - | (hb p. 7) |
| Cloud condensation nuclei concentration (dual column,... | - | - | - | (hb p. 8) |
| Cloud condensation nuclei concentration (dual column,... | - | - | - | (hb p. 8) |
| Total aerosol concentration via CVI inlet | μm | greater than 0.010 μm | - | (hb p. 8) |
| Total aerosol concentration via isokinetic inlet | μm | greater than 0.010 μm | - | (hb p. 8) |
| Total aerosol concentration (ultrafine CPC) | μm | greater than 0.003 μm | - | (hb p. 8) |
| Aerosol concentration (cloud droplet probe) | - | - | - | (hb p. 8) |
| Aerosol size distribution (FIMS) | μm | 0.010 to 0.450 μm | - | (hb p. 8) |
| Cloud particle size distribution (HVPS) | μm | 150 to 19,600 μm | - | (hb p. 8) |
| Aerosol particle size distribution (merged) | - | - | - | (hb p. 8) |
| Cloud particle size distribution/number concentration... | - | - | - | (hb p. 8) |
| Meteorological properties and geophysical location | - | - | - | (hb p. 8) |
| Aerosol scattering coefficient (nephelometer) | nm wavelengths | 450, 550, 700 nm | - | (hb p. 8) |
| Ozone concentration | - | - | - | (hb p. 8) |
| Size distribution (PCASP) | μm | 0.10 to 3 μm | - | (hb p. 8) |
| Aerosol absorption coefficient (PSAP) | nm wavelengths | 462, 523, 648 nm | - | (hb p. 8) |
| Sulfur dioxide concentration | - | - | - | (hb p. 8) |
| Soot spectrometry (SP2 refractory black carbon) | - | - | - | (hb p. 8) |
| Aerosol size distribution (UHSAS) | µm | 0.060 to 1 µm | - | (hb p. 8) |


## The data

Verified example: **`sgpaafmergedF1.c1`**, file `sgpaafmergedF1.c1.20160920.202755.nc`
(19.64 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=5104, `aaf2dsh_optical_diameter`=61, `bound`=2, `aaf2dsv_optical_diameter`=61, `cdp_optical_diameter`=21, `fims_geometric_diameter`=30, `hvps_optical_diameter`=37, `aerosolsd_geometric_diameter`=55, `pcasp_optical_diameter`=30, `uhsas_bin_number`=99 |
| Data variables | 193 |
| QC variables | 76 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aafmerged-c1-1.7 |
| process version | aafmerged-1.1.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `aerosolsd_alt` | m | time | yes | Altitude above mean sea level from merged aerosol size distribution |
| `aerosolsd_cas_flag` | 1 | time | yes | CAS flag from merged aerosol size distribution |
| `aerosolsd_cloud_flag` | 1 | time | yes | Cloud flag from merged aerosol size distribution |
| `aerosolsd_cvi_flag` | 1 | time | yes | CVI flag from merged aerosol size distribution |
| `aerosolsd_fcdp_flag` | 1 | time | yes | FCDP flag from merged aerosol size distribution |
| `aerosolsd_fims_flag` | 1 | time | yes | FIMS flag from merged aerosol size distribution |
| `aerosolsd_lat` | degree_N | time | yes | North latitude from merged aerosol size distribution |
| `aerosolsd_lon` | degree_E | time | yes | East longitude from merged aerosol size distribution |
| `aerosolsd_number_concentration` | 1/cm^3 | time,aerosolsd_geometric_diameter | yes | Number concentration from merged aerosol size distribution |
| `aerosolsd_pcasp_flag` | 1 | time | yes | PCASP flag from merged aerosol size distribution |
| `ams_CVI_enhancement_factor` | 1 | time | yes | CVI enhancement factor from time-of-flight aerosol mass spectrometer |
| `ams_Chl` | ug/m^3 | time | yes | Chloride mass concentration from time-of-flight aerosol mass... |
| `ams_Chl_err` | ug/m^3 | time | yes | Chloride mass concentration error from time-of-flight aerosol mass... |
| `ams_NH4` | ug/m^3 | time | yes | Ammonium mass concentration from time-of-flight aerosol mass... |
| `ams_NH4_err` | ug/m^3 | time | yes | Ammonium mass concentration error from time-of-flight aerosol mass... |
| `ams_NO3` | ug/m^3 | time | yes | Nitrate mass concentration from time-of-flight aerosol mass... |
| `ams_NO3_err` | ug/m^3 | time | yes | Nitrate mass concentration error from time-of-flight aerosol mass... |
| `ams_Org` | ug/m^3 | time | yes | Organic mass concentration from time-of-flight aerosol mass... |
| `ams_Org_err` | ug/m^3 | time | yes | Organic mass concentration error from time-of-flight aerosol mass... |
| `ams_SO4` | ug/m^3 | time | yes | Sulfate mass concentration from time-of-flight aerosol mass... |
| `ams_SO4_err` | ug/m^3 | time | yes | Sulfate mass concentration error from time-of-flight aerosol mass... |
| `ams_alt` | m | time | yes | Altitude above mean sea level from time-of-flight aerosol mass... |
| `ams_flag` | 1 | time | yes | Flag from time-of-flight aerosol mass spectrometer |
| `ams_lat` | degree_N | time | yes | North latitude from time-of-flight aerosol mass spectrometer |
| `ams_lon` | degree_E | time | yes | East longitude from time-of-flight aerosol mass spectrometer |
| `ccna_N_CCN` | 1/cm^3 | time | yes | Number concentration of CCN from cloud condensation nuclei counter a |
| `ccna_P_sample` | hPa | time | yes | Sample pressure of CCN from cloud condensation nuclei counter a |
| `ccna_T_inlet` | degC | time | yes | Temperature read of sample air at entrance to instrument from cloud... |
| `ccna_T_sample` | degC | time | yes | Temperature read of sample air entering the column from cloud... |
| `ccna_supersaturation_calculated` | % | time | yes | Sample supersaturation calculated via Lance/Rose method from cloud... |


_83 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaafmergedF1.c1", "2016-09-20", "2016-09-20")
ds = armlive_open("sgpaafmergedF1.c1", "2016-09-20", "2016-09-20", cleanup_qc=True)
```

This product carries 193 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaafmergedF1.c1", start, end,
                  keep_variables=['aerosolsd_alt', 'aerosolsd_cas_flag', 'aerosolsd_cloud_flag', 'qc_aerosolsd_alt', 'qc_aerosolsd_cas_flag', 'qc_aerosolsd_cloud_flag'])
```

## Quality control in this product

76 `qc_` companion variables cover 75 of the
193 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpaafmergedF1.c1.20160920.202755.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `ccna_T_sample` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |
| `cpcfcvi_concentration` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |
| `ccnb_supersaturation_calculated` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |
| `ccnb_P_sample` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |
| `ccnb_N_CCN` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |
| `ccnb_T_sample` | Transformation could not finish (all values bad or outside... | 5104 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaafmergedF1.c1", "20130715", "20260924")
```

The report's own note on quality: Quality controls can be applied during processing to create b1-level data files; additional mentor-edited processing with quality improvement/calibration produces 'c'-level data products. Variables carry supporting attributes (long_name, units, missing_value, and CF standard_name where applicable) to aid interpretation. Instrument-specific flags are propagated into the merged product (e.g., ams_flag, aerosolsd_cas_flag, aerosolsd_cloud_flag, aerosolsd_cvi_flag, aerosolsd_fcdp_flag, aerosolsd_fims_flag, aerosolsd_pcasp_flag, fims_heated_flag, ccna_temp_unstable, ccnb_temp_unstable) so users...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Missing or bad aafnaviwg.c1 navigation/met data | No aafmerged output data exists for periods where aafnaviwg.c1 data is unavailable, since output time stamps are tied directly to aafnaviwg.c1 sample times. | - | (hb p. 6) |
| Nearest-neighbor transformation range limits | For most input datastreams, a data value up to 30 minutes away in time from the target output time may be substituted if the closest sample is bad or missing, which can introduce temporal... | - | (hb p. 4) |
| Datastream availability varies by campaign | Not all of the up to 23 possible input datastreams/variables are present in every aafmerged.c1 file; some output variables listed in Table 2 may be absent depending on which instruments... | - | (hb p. 6) |
| No scientific analysis or bias correction applied by the VAP | Merged variables reflect the source datastream values unchanged (no additional algorithm or correction), so any artifacts or biases already present in the individual instrument-level... | - | (hb p. 4) |
| CCN instrument thermal stabilization flag | ccna_temp_unstable and ccnb_temp_unstable logical variables indicate when the CCN counter has not reached thermal gradient stabilization (within 0.4 degrees C of set point), meaning CCN... | - | (hb p. 8) |
| Multiple quality/contamination flags in merged aerosol size distribution | aerosolsd_cas_flag, aerosolsd_cloud_flag, aerosolsd_cvi_flag, aerosolsd_fcdp_flag, aerosolsd_fims_flag, and aerosolsd_pcasp_flag variables mark periods potentially affected by cloud... | - | (hb p. 9) |
| FIMS heated/unheated sampling mode | fims_heated_flag indicates whether FIMS data was collected in heated or unheated sampling mode, which can shift measured aerosol size distributions depending on mode. | - | (hb p. 8) |
| CVI inlet selector and dilution factor affect interpretation of CVI-derived data | inletcvi_inlet_selector records valve position and inletcvi_inlet_dilution_factor records the dilution factor for under-kinetic mode; users must account for these to correctly interpret... | - | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Prakash, G, J Kumar, E Rush, R Records, A Clodfelter, and J Voyles. 2016. "HPC infrastructure to support the next-generation ARM facility data operations." 2016 IEEE International Conference on Big Data (Big Data),...
- Berg, LK, et al. 2020. "Fine-Scale Variability of Observed and Simulated Surface Albedo over the Southern Great Plains." JGR-Atmospheres 125(7): e2019JD030559
- Creamean, JM, et al. 2018. "The influence of local oil exploration and regional wildfires on summer 2015 aerosol over the North Slope of Alaska." ACP 18(2): 555-570
- Fast, JD, et al. 2019. "Overview of the HI-SCALE Field Campaign: A New Perspective on Shallow Convective Clouds." BAMS 100(5): 821-840
- Gu, D, et al. 2017. "Airborne observations reveal elevational gradient in tropical forest isoprene emissions." Nature Communications 8: 15541
- Shrivastava, M, et al. 2019. "Urban pollution greatly enhances formation of natural aerosols over the Amazon rainforest." Nature Communications 10: 1046
- Wang, J, et al. 2022. "Aerosol and Cloud Experiments in the Eastern North Atlantic (ACE-ENA)." BAMS 103(2): E619-E641
- Wang, Y, et al. 2023. "Examining the vertical heterogeneity of aerosols over the Southern Great Plains." ACP 23(24): 15671-15691
- Yeom, JM, et al. 2021. "Vertical Variations of Cloud Microphysical Relationships in Marine Stratocumulus Clouds Observed during the ACE-ENA Campaign." JGR-Atmospheres 126(24): e2021JD034700
- Zhang, D, et al. 2023. "Evaluation of four ground-based retrievals of cloud droplet number concentration in marine stratocumulus with aircraft in situ measurements." AMT 16(23): 5827-5846

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-299.pdf (18 pages, DOE/SC-ARM-TR-299, by F Mei, K Gaustad)
- Catalog record: ARM data-source index, `instrument_class_code=aafmerged`, read 2026-09-24
- Example file: `sgpaafmergedF1.c1.20160920.202755.nc` from `sgpaafmergedF1.c1`, 19.64 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
