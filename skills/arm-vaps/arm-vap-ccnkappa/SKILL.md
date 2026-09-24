---
name: arm-vap-ccnkappa
description: ARM CCN Counter derived hygroscopicity parameter kappa (ccnkappa) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (kappa, critical_diameter, supersaturation_calculated, N_CCN, aerosol number size distribution), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (enaaosccnsmpskappaC1.c1) and the variable inventory of a real file. Use when working with ccnkappa data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Derived Quantities and Models. Triggers - ccnkappa, CCN Counter derived hygroscopicity parameter kappa, enaaosccnsmpskappaC1.c1, kappa, critical_diameter, supersaturation_calculated, N_CCN, aerosol number size distribution, Aerosols.
---

# CCNKAPPA - CCN Counter derived hygroscopicity parameter kappa

This value-added product calculates the aerosol hygroscopicity parameter kappa from collocated CCN counter and aerosol particle sizer (SMPS or UHSAS) data at ARM observatories, quantifying the ability of aerosols to activate into cloud droplets.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ccnkappa` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-272 / G Kulkarni, MS Levin, JE Shilling / November 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-272.pdf) |
| Category | Aerosols; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2016-05-20 to 2026-09-23 (active) |
| Datastreams with data | 13 across 11 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ccnkappa |


## Credit

Everything this skill knows about the retrieval is the work of **G Kulkarni, MS Levin, JE Shilling** -
the ARM developers and mentors who wrote the technical report it derives from:

> G Kulkarni, MS Levin, JE Shilling. *Cloud Condensation Nuclei Hygroscopicity Value-Added Product Report*, DOE/SC-ARM-TR-272, November 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-272.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-272 covers both output variants of this class, the CCN+SMPS and CCN+UHSAS combinations.

## How it is produced

Kappa-Köhler theory (Petters and Kreidenweis 2007) is used to calculate kappa from aerosol particle size and supersaturation measurements, ignoring the influence of mixing state and individual chemical composition and assuming particles are internally mixed with bulk chemical composition. The overall kappa is calculated from the particle number size distribution (from SMPS or UHSAS) and CCN concentrations at a defined instrument supersaturation as a function of time. Backward stepwise integration from the upper size limit of the size distribution measurements is performed until the total particle concentration matches the measured CCN concentration, and the corresponding particle diameter is assumed to be the critical diameter required for activation. Particles greater than this critical diameter are assumed to activate into CCN, and this critical diameter is used with the measured supersaturation to calculate kappa via the rearranged kappa-Köhler equation. Surface tension for all droplets is assumed to be that of water (0.072 J m-2), and particles are assumed to have uniform chemical composition and mixing state, with larger particles preferentially activating over smaller ones independent of composition at a given supersaturation.

**Cadence.** input rate SMPS: one complete scan per 300 seconds; UHSAS: aerosol size distribution recorded every 10 seconds; CCNC: 10 minutes per supersaturation setpoint, 60-minute complete scan cycle; output every Daily netCDF output files, each spanning a 24-hour interval beginning at midnight (UTC); averaging Temporal spacing between data points can vary due to different time-grids used by CCN and SMPS/UHSAS input datastreams (hb p. 15).

## Inputs

The report names these instruments and sibling products: SMPS (scanning mobility particle sizer), UHSAS (ultra-high-sensitivity aerosol spectrometer), CCNC (cloud condensation nuclei counter), CPC (condensation particle counter).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| kappa (hygroscopicity parameter) | dimensionless | - | - | (hb p. 11) |
| critical_diameter | nm (implied) | - | - | (hb p. 11) |
| supersaturation_calculated | % | 0.0 to 1.0% | - | (hb p. 7) |
| N_CCN (CCN number concentration) | #/cc (implied) | - | - | (hb p. 9) |
| aerosol number size distribution (dN_dlogDp) | - | SMPS: 10-515 nm; UHSAS: 60 to... | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Kappa range for highly hygroscopic aerosols | 0.5 to 1.4 | (hb p. 6) |
| Kappa range for organic compounds | 0.01 to 0.5 | (hb p. 6) |
| Kappa for non-hygroscopic aerosols (e.g., soot) | very close to zero | (hb p. 6) |
| Kappa range for ambient aerosols | 0.05 to 0.9 | (hb p. 6) |
| SMPS size range | 10-515 nm | (hb p. 7) |
| SMPS scan time | 300 seconds (complete scan across 109 size bins) | (hb p. 7) |
| CCNC supersaturation steps | 0, 0.1, 0.2, 0.4, 0.8, and 1% | (hb p. 7) |
| CCNC data recording time per SS value | 10 minutes | (hb p. 7) |
| CCNC complete scan cycle | 60 minutes | (hb p. 7) |
| UHSAS detection size range | 60 to 1000 nm | (hb p. 7) |
| UHSAS size range used in kappa calculation | 70 to 700 nm | (hb p. 7) |
| UHSAS data recording interval | every 10 seconds | (hb p. 7) |
| UHSAS supersaturation limit for kappa calc | Sc less than  0.5% | (hb p. 7) |
| Assumed droplet surface tension | 0.072 Jm-2 | (hb p. 7) |
| UHSAS optical scattering wavelength | 1054 nm | (hb p. 10) |
| UHSAS QC total number concentration threshold | less than  3600 #/cc | (hb p. 10) |


## The data

Verified example: **`enaaosccnsmpskappaC1.c1`**, file `enaaosccnsmpskappaC1.c1.20260920.000826.nc`
(0.19 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=96, `bound`=2, `diameter_mobility`=192, `droplet_size`=20, `setpoint`=7 |
| Data variables | 24 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 640 s |
| File time span | 2026-09-20T00:08:26 to 2026-09-20T23:52:41 |
| dod version | aosccnsmpskappa-c1-1.3 |
| process version | aosccnsmpskappa-1.7.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `N_CCN` | 1/cm^3 | time | yes | Mean number concentration of N_CCN |
| `N_CCN_dN` | count/s | time,droplet_size | yes | Droplet count by bin size |
| `aerosol_number_concentration` | 1/cm^3 | time | yes | Aerosol particle number concentration |
| `critical_diameter` | nm | time | yes | Critical diameter |
| `dN_dlogDp` | 1/cm^3 | time,diameter_mobility | yes | Number size distribution, electrical mobility diameter |
| `kappa` | 1 | time | yes | Hygroscopicity parameter kappa |
| `supersaturation_calculated` | % | time | yes | Mean calculated supersaturation values for a fixed supersaturation... |
| `temperature` | degC | time | yes | Temperature read at top of column |
| `diameter_mobility` | nm | diameter_mobility | - | Midpoint of geometric mean mobility diameter |
| `droplet_size` | um | droplet_size | - | Size bins for CCN droplets |
| `setpoint` | % | setpoint | - | Supersaturation set point values |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaosccnsmpskappaC1.c1", "2026-09-20", "2026-09-20")
ds = armlive_open("enaaosccnsmpskappaC1.c1", "2026-09-20", "2026-09-20", cleanup_qc=True)
```

## Quality control in this product

8 `qc_` companion variables cover 8 of the
24 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaosccnsmpskappaC1.c1.20260920.000826.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `dN_dlogDp` | Transformation could not finish (all values bad or outside... | 8064 | 43.75 |
| `kappa` | Value is greater than fail_max. Value set to missing_value. | 1 | 1.0417 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("enaaosccnsmpskappaC1.c1", "20160520", "20260924")
```

The report's own note on quality: The aosccn2colaavg.b1 datastream includes qc_N_CCN (quality check on mean N_CCN). The aossmps.b1 datastream includes qc_dN_dlogDp (quality check on number size distribution). The aosuhsas.b1 datastream includes qc_dN_dlogDp (quality check on number size distribution, optical diameter 70-700 nm) and qc_total_N_conc (quality check flagging total number concentration from integrated size distribution, threshold less than  3600 #/cc). Appendix A describes quality checks applied to aosccn2cola.b1: N_CCN concentrations marked as good (shown in green in plots) are used to develop the AVG and SPECTRA...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Kappa depends on instrument supersaturation and critical diameter due to assumption of... | A polydisperse size distribution of single-component aerosol particles would appear to have higher kappa at lower instrument supersaturation, an obvious error | Method works best for clean continental regions/sites with lesser heterogeneity in chemical composition across the size distribution | (hb p. 7) |
| Mixing state and individual chemical composition of particles are ignored in the... | Calculated kappa represents an overall bulk value rather than composition-resolved values | - | (hb p. 6) |
| UHSAS lower and upper detection limit uncertainty | Particles near 60 nm and 1000 nm edges have uncertain sizing | Only particles in size range 70 to 700 nm were used in the kappa calculation | (hb p. 7) |
| UHSAS lower size limit restricts kappa calculation to low supersaturation | For Sc greater than = 0.5%, critical diameter often falls below 70 nm and cannot be resolved | Kappa calculation restricted to supersaturation values below 0.5% (Sc less than  0.5%) | (hb p. 7) |
| Variable temporal spacing between data points | Irregular time grid in output files due to differing native time-grids of CCN and SMPS/UHSAS instruments | - | (hb p. 15) |
| Processing delay imposed on VAP | Data for a given day not available immediately; several-day lag before VAP output appears | A several-day delay on processing is imposed to allow for input data to become fully available before the VAP is run | (hb p. 15) |
| Assumption that larger particles preferentially activate over smaller particles... | Derived critical diameter/kappa may not reflect true composition-dependent activation behavior | - | (hb p. 7) |
| Uniform surface tension assumption (pure water value used for all droplets) | Kappa values may be biased if actual droplet surface tension differs from water due to surfactants or organics | - | (hb p. 7) |
| AOSCCNUHSASKAPPA developed only to fill gaps where AOSCCNSMPSKAPPA is missing | UHSAS-based kappa product only present at sites/times lacking SMPS-based kappa | - | (hb p. 6) |
| Quality-flagged N_CCN data in aosccn2cola.b1 | CCN concentration data points marked with quality assessments (good/bad) visible in plots; only data marked good (green) used in higher-level AVG/SPECTRA products | Only good-quality N_CCN data used to develop AVG and SPECTRA higher-level products | (hb p. 16) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Kuang, C. 2016. Scanning Mobility Particle Spectrometer Instrument Handbook. DOE/SC-ARM/TR-147.
- Petters, MD, and SM Kreidenweis. 2007. "A Single Parameter Representation of Hygroscopic Growth and Cloud Condensation Nucleus Activity." Atmospheric Chemistry and Physics 7(8): 1961-1971.
- Ren, J, et al. 2018. "Using different assumptions of aerosol mixing state and chemical composition to predict CCN concentrations based on field measurements in urban Beijing." Atmospheric Chemistry and Physics 18(9):...
- Uin, J. 2016. Ultra-High-Sensitivity Aerosol Spectrometer (UHSAS) Instrument Handbook. DOE/SC-ARM/TR-163.
- Uin, J. 2022. Cloud Condensation Nuclei Particle Counter Instrument Handbook. DOE/SC-ARM/TR-168.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-272.pdf (17 pages, DOE/SC-ARM-TR-272, by G Kulkarni, MS Levin, JE Shilling)
- Catalog record: ARM data-source index, `instrument_class_code=ccnkappa`, read 2026-09-24
- Example file: `enaaosccnsmpskappaC1.c1.20260920.000826.nc` from `enaaosccnsmpskappaC1.c1`, 0.19 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
