---
name: arm-vap-aerosolbe
description: ARM Aerosol Best Estimate (aerosolbe) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Best estimate Angström exponent, Single scattering albedo profile, Asymmetry parameter profile), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaerosolbe1turnC1.c1) and the variable inventory of a real file. Use when working with aerosolbe data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - aerosolbe, Aerosol Best Estimate, sgpaerosolbe1turnC1.c1, Best estimate Angström exponent, Single scattering albedo profile, Aerosols.
---

# AEROSOLBE - Aerosol Best Estimate

AEROSOLBE is a value-added product that combines multiple ARM instrument datastreams to provide nearly continuous best-estimate time/height profiles of aerosol extinction, optical depth, single-scattering albedo, asymmetry parameter and Angström exponent above the SGP Central Facility.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 29 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aerosolbe` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-115 / C Flynn, D Turner, A Koontz, D Chand, C Sivaraman / July 2012](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-115.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2001-01-01 to 2021-04-30 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aerosolbe |


## Credit

Everything this skill knows about the retrieval is the work of **C Flynn, D Turner, A Koontz, D Chand, C Sivaraman** -
the ARM developers and mentors who wrote the technical report it derives from:

> C Flynn, D Turner, A Koontz, D Chand, C Sivaraman. *Aerosol Best Estimate (AEROSOLBE) Value-Added Product (VAP)*, DOE/SC-ARM/TR-115, July 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-115.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP screens direct AOD measurements from NIMFR and MFRSR for clouds and quality, then produces a nearly continuous AOD time series at 500 nm and 355 nm and Angström exponent via interpolation over short gaps and multivariate regression (using surface RH, surface total scattering, and boundary-layer average RH) over longer gaps. The corresponding aerosol extinction profile is selected from a Raman lidar (RL) seasonal climatology of extinction profiles as a function of column AOD (Turner et al. 2001). Single scattering albedo and asymmetry parameter profiles are derived by assuming the dry aerosol scattering properties measured at the surface by the AOS are well-mixed with height, with no humidity dependence assumed for absorption. These dry properties are then modulated with height using the vertical RH profile from MERGESONDE and the AOS-derived two-parameter f(RH) = a(1-u)^-b hygroscopic growth relationship to yield ambient aerosol optical properties as a function of height.

**Cadence.** output every 10 minutes; averaging Data from each input source are averaged to achieve the 10-minute temporal resolution (hb p. 6).

## Inputs

The report names these instruments and sibling products: Normal incidence multifilter radiometer (NIMFR), Multifilter rotating shadowband radiometer (MFRSR), Aerosol observing system (AOS), Aerosol Intensive Properties (AIP) VAP, Merged Sounding (MERGESONDE) VAP, Surface meteorological instrumentation (MET), Raman lidar (RL), Broadband Heating Rate Profile (BBHRP) VAP, Microwave radiometer profiler (MWRP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Best estimate aerosol optical depth at 500 nm | unitless | - | - | (hb p. 24) |
| Best estimate aerosol optical depth at 355 nm | unitless | - | - | (hb p. 24) |
| Best estimate Angström exponent | unitless | - | - | (hb p. 24) |
| Aerosol extinction profile at 500 nm | 1/km | - | - | (hb p. 24) |
| Single scattering albedo profile (red/green/blue) | unitless | - | - | (hb p. 24) |
| Asymmetry parameter profile (red/green/blue) | unitless | - | - | (hb p. 24) |
| Total scatter coefficient (red/green/blue) | 1/km | - | - | (hb p. 24) |
| Backscatter coefficient (red/green/blue) | 1/km | - | - | (hb p. 24) |
| Absorption coefficient (red/green/blue) | 1/km | - | - | (hb p. 24) |
| Relative humidity profile | % | - | - | (hb p. 25) |
| Height above ground level | km | - | - | (hb p. 24) |
| Boundary layer mixing height | km | - | - | (hb p. 27) |
| Solar zenith angle | degree | - | - | (hb p. 27) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Time resolution | 10 minutes | (hb p. 6) |
| Cloudy Angström exponent threshold (lower) | 0.5 | (hb p. 13) |
| Cloudy Angström exponent threshold (upper) | 4.0 | (hb p. 13) |
| Tolerance test rolling window | 90 samples before and after sample of interest | (hb p. 13) |
| Tolerance test standard deviation threshold | 0.05 | (hb p. 13) |
| Dry Angström exponent valid range (aip1ogren) | 0 to 3 | (hb p. 14) |
| Minimum mergesonde profile height | 7 km | (hb p. 14) |
| SONDE RH minimum value if below zero | 50% | (hb p. 14) |
| MET RH maximum cap | 99% | (hb p. 14) |
| f(RH) max RH range check (red/blue/green) | greater than 70% | (hb p. 14) |
| f(RH) min RH range check (red/blue/green) | less than 50% | (hb p. 14) |
| f(RH) parameter a and b valid range | 0.2 to 1.4 | (hb p. 14) |
| f(RH) Green parameter a | 0.8043 | (hb p. 14) |
| f(RH) Green parameter b | 0.4436 | (hb p. 14) |
| f(RH) Blue parameter a | 0.8345 | (hb p. 14) |
| f(RH) Blue parameter b | 0.3920 | (hb p. 14) |
| f(RH) Red parameter a | 0.7619 | (hb p. 14) |
| f(RH) Red parameter b | 0.4878 | (hb p. 14) |
| Interpolation gap - Best estimate Angström exponent | 3 days | (hb p. 15) |
| Interpolation gap - Best estimate AOD at 355nm | 3 hours | (hb p. 15) |
| Interpolation gap - Best estimate AOD at 500nm before... | 3 hours | (hb p. 15) |
| Interpolation gap - Best estimate AOD at 500nm after... | 8 hours | (hb p. 15) |
| Interpolation gap - All dry coefficients from aip1ogren | 3 hours | (hb p. 15) |
| Interpolation gap - f(RH) correction coefficients | 3 days | (hb p. 15) |
| Interpolation gap - Humidified total scattering and... | 3 hours | (hb p. 15) |
| Interpolation gap - Angström exponent using humidified Red... | 3 days | (hb p. 15) |


_7 further rows in the report._

## The data

Verified example: **`sgpaerosolbe1turnC1.c1`**, file `sgpaerosolbe1turnC1.c1.20210401.000000.cdf`
(87.78 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4320, `height`=177, `height_rl`=192, `parameter`=2 |
| Data variables | 129 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2021-04-01T00:00:00 to 2021-04-30T23:50:00 |
| dod version | aerosolbe1turn-c1-1.2 |
| process version | Exp |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `absorption_coefficient_mean_blue` | 1/km | time | yes | Aerosol absorption coefficient, blue wavelength, low RH, 1 um size cut |
| `absorption_coefficient_mean_green` | 1/km | time | yes | Aerosol absorption coefficient, green wavelength, low RH, 1 um size... |
| `absorption_coefficient_mean_red` | 1/km | time | yes | Aerosol absorption coefficient, red wavelength, low RH, 1 um size cut |
| `backscatter_coefficient_blue` | 1/km | time | yes | Aerosol backscatter coefficient, blue wavelength, low RH, 1 um size... |
| `backscatter_coefficient_green` | 1/km | time | yes | Aerosol backscatter coefficient, green wavelength, low RH, 1 um size... |
| `backscatter_coefficient_red` | 1/km | time | yes | Aerosol backscatter coefficient, red wavelength, low RH, 1 um size cut |
| `be_angstrom_exponent` | unitless | time | yes | Best estimate Angstrom exponent |
| `be_aod_355` | unitless | time | yes | Best estimate aerosol optical depth at 355nm |
| `be_aod_500` | unitless | time | yes | Best estimate aerosol optical depth at 500 nm |
| `mean_angstrom_exponent_mfrsr` | unitless | time | yes | Mean angstrom exponent from MFRSR observations, wavelengths used by... |
| `mean_angstrom_exponent_nimfr` | unitless | time | yes | Mean angstrom exponent from NIMFR observations, wavelengths used by... |
| `mean_aod_mfrsr_filter1` | unitless | time | yes | Mean aerosol optical depth at 415 nm from MFRSR |
| `mean_aod_mfrsr_filter2` | unitless | time | yes | Mean aerosol optical depth at 500 nm from MFRSR |
| `mean_aod_mfrsr_filter3` | unitless | time | yes | Mean aerosol optical depth at 615 nm from MFRSR |
| `mean_aod_mfrsr_filter4` | unitless | time | yes | Mean aerosol optical depth at 673 nm from MFRSR |
| `mean_aod_mfrsr_filter5` | unitless | time | yes | Mean aerosol optical depth at 870 nm from MFRSR |
| `mean_aod_nimfr_filter1` | unitless | time | yes | Mean aerosol optical depth at 415 nm from NIMFR |
| `mean_aod_nimfr_filter2` | unitless | time | yes | Mean aerosol optical depth at 500 nm from NIMFR |
| `mean_aod_nimfr_filter3` | unitless | time | yes | Mean aerosol optical depth at 615 nm from NIMFR |
| `mean_aod_nimfr_filter4` | unitless | time | yes | Mean aerosol optical depth at 673 nm from NIMFR |
| `mean_aod_nimfr_filter5` | unitless | time | yes | Mean aerosol optical depth at 870 nm from NIMFR |
| `time` | - | time | yes | Time offset from midnight |
| `total_scatter_coefficient_blue` | 1/km | time | yes | Aerosol total scatter coefficient, blue wavelength, low RH, 1 um size... |
| `total_scatter_coefficient_green` | 1/km | time | yes | Aerosol total scatter coefficient, green wavelength, low RH, 1 um... |
| `total_scatter_coefficient_red` | 1/km | time | yes | Aerosol total scattering coefficient, red wavelength, low RH, 1 um... |
| `BluBscat_humidified` | 1/km | time,height | - | Humidified backscatter coefficient at 450 nm for 1 um size cut |
| `BluTscat_humidified` | 1/km | time,height | - | Humidified total scatter coefficient at 450 nm for 1 um size cut |
| `GrnBscat_humidified` | 1/km | time,height | - | Humidified backscatter coefficient at 500 nm for 1 um size cut |
| `GrnTscat_humidified` | 1/km | time,height | - | Humidified total scatter coefficient at 500 nm for 1 um size cut |
| `RH_NephVol_Dry` | % | time | - | Relative humidity inside dry nephelometer |


_73 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaerosolbe1turnC1.c1", "2021-04-01", "2021-04-01")
ds = armlive_open("sgpaerosolbe1turnC1.c1", "2021-04-01", "2021-04-01", cleanup_qc=True)
```

This product carries 129 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaerosolbe1turnC1.c1", start, end,
                  keep_variables=['absorption_coefficient_mean_blue', 'absorption_coefficient_mean_green', 'absorption_coefficient_mean_red', 'qc_absorption_coefficient_mean_blue', 'qc_absorption_coefficient_mean_green', 'qc_absorption_coefficient_mean_red'])
```

## Quality control in this product

25 `qc_` companion variables cover 24 of the
129 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpaerosolbe1turnC1.c1.20210401.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `mean_aod_nimfr_filter1` | Data value is not available in input file, data value set to... | 4320 | 100.0 |
| `absorption_coefficient_mean_green` | Data value not available in input file, data value set to -9999... | 4320 | 100.0 |
| `mean_angstrom_exponent_nimfr` | Data value is not available in input file, data value set to... | 4320 | 100.0 |
| `mean_aod_nimfr_filter5` | Data value is not available in input file, data value set to... | 4320 | 100.0 |
| `mean_aod_nimfr_filter4` | Data value is not available in input file, data value set to... | 4320 | 100.0 |
| `mean_aod_nimfr_filter3` | Data value is not available in input file, data value set to... | 4320 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaerosolbe1turnC1.c1", "20010101", "20260924")
```

The report's own note on quality: Each input datastream undergoes quality checks before combination: (1) NIMFR/MFRSR AOD data pass a rolling-window (90 samples before/after) tolerance test on standard deviation (threshold 0.05), with flagged bad data replaced by missing value -9999.0; (2) cloud screening via Angström exponent thresholds (below 0.5 or above 4.0 flags all filter AODs as missing); (3) dry Angström exponent from aip1ogren screened to be within 0-3, else set to missing; (4) mergesonde profiles discarded if not reaching 7 km, and SONDE RH values below zero set to a minimum of 50%; (5) MET RH values above 99.0 set...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| NIMFR/MFRSR AOD anomalies flagged by rolling-window tolerance test | Samples where the standard deviation of a 90-sample rolling window exceeds 0.05 are flagged as bad data and replaced with missing value -9999.0 | Rolling window standard deviation test applied (originally combined with mean-difference test, later simplified to std-dev-only test after Oct 2004... | (hb p. 13) |
| Cloud contamination of AOD measurements | Angström exponent from NIMFR/MFRSR falls below 0.5 or above 4.0, indicating cloud-affected samples | AOD for all filters replaced with missing values -9999.0 when Angström exponent is outside 0.5-4.0 range | (hb p. 13) |
| Bad dry Angström exponent data from aip1ogren | Dry Angström exponent for total scattering, back scattering, or absorption coefficients falls outside 0-3 range | Values replaced with missing values -9999.0 | (hb p. 14) |
| Insufficient vertical extent of radiosonde profile | mergesonde1mace profile does not reach a minimum height of 7 km | Profile is discarded | (hb p. 14) |
| Unphysical negative RH from sonde | Relative humidity from SONDE data is less than zero | RH set to a minimum value of 50% | (hb p. 14) |
| MET RH exceeding sensor plausible max | Relative humidity from MET data above 99.0% | RH capped/set to 99% | (hb p. 14) |
| Bad f(RH) fit coefficients in aipfitrh1ogren | Max RH range for red/blue/green not greater than 70% or min RH range not less than 50%, or fit parameters a/b outside 0.2-1.4 range | Out-of-range parameters set to -9999 or reset to prescribed default values (Table 1) | (hb p. 14) |
| NIMFR lacks cosine correction | Discrepancy between NIMFR and MFRSR AOD estimates under certain sun-angle/instrument-response conditions | NIMFR is taken in preference over MFRSR despite this, per Harrison and Michalsky (1994) reference; algorithm still prioritizes NIMFR when available | (hb p. 7) |
| Data gaps in direct AOD measurements | Missing NIMFR/mfrsraod values for a given 10-minute sample | Short gaps filled by interpolation; longer gaps filled by multivariate regression using surface RH, surface total scattering, and boundary layer... | (hb p. 7) |
| Extinction profile derived from climatology rather than direct vertical measurement | Extinction profile assigned from a lookup table (RL seasonal climatology binned by season and AOD) rather than a real-time vertical measurement, so vertical structure reflects... | None stated beyond noting the climatology basis (Turner et al. 2001) | (hb p. 7) |
| Well-mixed aerosol assumption for SSA/g vertical profiles | Single scattering albedo and asymmetry parameter profiles assume dry aerosol optical properties are constant with altitude (well-mixed boundary layer), which may not hold under all... | None stated beyond describing the well-mixed assumption; ratios used to mitigate scale-height effects | (hb p. 7) |
| No humidity dependence applied to aerosol absorption | Absorption coefficient profile does not vary with RH even though scattering coefficients are humidity-corrected | None stated; assumption explicitly made | (hb p. 7) |
| Interpolation gap limits exceeded | Data gaps longer than the specified interval (e.g., 3 hours, 8 hours, 3 days depending on field, see Table 2) are not interpolated and remain missing | Values are not interpolated if gap exceeds the specified interval | (hb p. 15) |
| Discrepancy between v1.0 effective height and v1.1 regression-fit AOD prediction | Monthly distributions of observed minus predicted AOD show differences between v1.0 effective height and v1.1 regression fit methods for 2000 | None stated beyond illustrating the comparison in Figure 11 and Table 3 | (hb p. 19) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Andrews, E, et al. 2006. Comparison of methods for deriving aerosol asymmetry parameter. JGR 111: D05S04.
- Andrews, E, PJ Sheridan, JA Ogren, and R Ferrare. 2004. In situ aerosol profiles over the Southern Great Plains CART site, Part I. JGR 109: D06208.
- Daniel, JS, et al. 2002. Cloud liquid water and ice measurements from spectrally resolved near-infrared observations. JGR 107: 4599.
- Ferrare, RA, et al. 2004. Raman lidar measurements of aerosols and water vapor over the Southern Great Plains. ILRC 22.
- Flynn, CJ, A Mendoza, and J Christy. 2004. ARM Micropulse lidar: Configuration upgrades and new data products. 14th ARM Science Team Meeting.
- Goldsmith, JEM, FH Blair, SE Bisson, and DD Turner. 1998. Turn-key Raman lidar for profiling atmospheric water vapor, clouds, and aerosols. Applied Optics 37: 4979-4990.
- Harrison, LC, and JJ Michalsky. 1994. Objective algorithms for the retrieval of optical depths from ground-based measurements. Applied Optics 33: 5126.
- Koontz, AS, CJ Flynn, JA Ogren, E Andrews, and PJ Sheridan. 2003. ARM AOS processing status and aerosol intensive properties VAP. 13th ARM Science Team Meeting.
- Mlawer, EJ, et al. 2002. The broadband heating rate profile (BBHRP) VAP. 12th ARM Science Team Meeting.
- Mlawer, EJ, et al. 2004. Status of the broadband heating rate profile (BBHRP) VAP. 14th ARM Science Team Meeting.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-115.pdf (29 pages, DOE/SC-ARM/TR-115, by C Flynn, D Turner, A Koontz, D Chand, C Sivaraman)
- Catalog record: ARM data-source index, `instrument_class_code=aerosolbe`, read 2026-09-24
- Example file: `sgpaerosolbe1turnC1.c1.20210401.000000.cdf` from `sgpaerosolbe1turnC1.c1`, 87.78 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
