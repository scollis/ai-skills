---
name: arm-vap-aerioe
description: ARM AERIoe Thermodynamic Profile and Cloud Retrieval (aerioe) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (temperature, waterVapor, lwp, lReff, relative humidity, potential temperature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaerioe1turnC1.c1) and the variable inventory of a real file. Use when working with aerioe data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - aerioe, AERIoe Thermodynamic Profile and Cloud Retrieval, sgpaerioe1turnC1.c1, temperature, waterVapor, lwp, lReff, relative humidity, Derived Quantities and Models.
---

# AERIOE - AERIoe Thermodynamic Profile and Cloud Retrieval

AERIoe is an ARM value-added product that retrieves boundary-layer profiles of temperature and water vapor mixing ratio together with single-layer liquid cloud properties (liquid water path, effective radius) from AERI downwelling infrared radiance spectra combined with microwave radiometer, surface meteorology, model, and cloud-base-height inputs, using an optimal estimation physical-iterative retrieval, and is currently run operationally at the ARM SGP site.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 23 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aerioe` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-234 / LD Riihimaki, T Shippert, DD Turner / November 2019](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-234.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2016-01-01 to 2023-06-13 (retired) |
| Datastreams with data | 8 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aerioe |


## Credit

Everything this skill knows about the retrieval is the work of **LD Riihimaki, T Shippert, DD Turner** -
the ARM developers and mentors who wrote the technical report it derives from:

> LD Riihimaki, T Shippert, DD Turner. *Atmospheric Emitted Radiance Interferometer Optimal Estimation (AERIoe) Value-Added Product Report*, DOE/SC-ARM-TR-234, November 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-234.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm uses an optimal estimation (physical-iterative) framework (Rodgers 2000) to simultaneously retrieve profiles of temperature and water vapor mixing ratio plus liquid cloud LWP and effective radius from AERI infrared radiance spectra in specific wavenumber bands (Table 2), constrained by additional inputs including surface MET temperature/RH, microwave radiometer brightness temperatures at 23.8 and 30.0 GHz, cloud base height, and Rapid Refresh (RAP) NWP model output above the boundary layer. A priori (prior) profiles come from monthly radiosonde climatologies at the site, with level-to-level covariance computed from ~2000 historical radiosondes per month at SGP; cloud property priors are fixed at LWP=0+/-50 g m-2 and Reff=8+/-4 microns. The forward model uses LBLRTM (v12.1) for infrared radiances and MonoRTM (v5.2) for microwave frequencies, both from AER, simulating only absorption (no scattering). Because it is an iterative optimal-estimation retrieval, each solution comes with a full error covariance matrix, degrees of freedom for signal (information content), and averaging-kernel-derived vertical resolution estimates.

**Cadence.** input rate approximately 20 s (native AERI resolution); output every VAP run at native resolution of the AERI, ~20 s; averaging Monthly a priori climatologies use 3 months centered on desired month, averaged over ~2000 radiosondes per month at SGP; prior profiles average all times of day and cloud conditions together (hb p. 16).

## Inputs

The report names these instruments and sibling products: AERI, AERIPROF VAP, MWR (MWRLOS, MWR3C), MWRRET VAP, MET, ceilometer, Doppler lidar, KAZR, MPL, CLDTYPE VAP, TSI, RAP NWP model.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| temperature | degC | - | sigma_temperature (from error covariance... | (hb p. 10) |
| waterVapor | g kg-1 | - | sigma_waterVapor (from error covariance... | (hb p. 10) |
| lwp | g m-2 | - | sigma_lwp; less than 20% uncertainty over... | (hb p. 10) |
| lReff | microns | - | sigma_lReff (from error covariance matrix) | (hb p. 10) |
| relative humidity | - | - | - | (hb p. 9) |
| potential temperature | - | - | - | (hb p. 9) |
| equivalent potential temperature | - | - | - | (hb p. 9) |
| dew point temperature | - | - | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| AERI spectral range | 3.3-19.2 microns (520-3020 cm-1 wavenumbers) | (hb p. 8) |
| Wavenumber band 538-588 cm-1 | Water vapor sensitivity | (hb p. 11) |
| Wavenumber band 612-618 cm-1 | Temperature sensitivity | (hb p. 11) |
| Wavenumber band 624-660 cm-1 | Temperature sensitivity | (hb p. 11) |
| Wavenumber band 674-722 cm-1 | Temperature sensitivity | (hb p. 11) |
| Wavenumber band 828-835 cm-1 | Clouds sensitivity | (hb p. 11) |
| Wavenumber band 843-848 cm-1 | Clouds sensitivity | (hb p. 11) |
| Wavenumber band 860.1-864 cm-1 | Clouds sensitivity | (hb p. 11) |
| Wavenumber band 872.2-877.5 cm-1 | Clouds sensitivity | (hb p. 11) |
| Wavenumber band 898.2-905.4 cm-1 | Clouds sensitivity | (hb p. 11) |
| Prior cloud LWP | 0 +/-50 g m-2 | (hb p. 11) |
| Prior cloud effective radius | 8 +/-4 microns | (hb p. 11) |
| Assumed CH4 concentration | 1.793 +/-0.0538 ppm | (hb p. 11) |
| Assumed N2O concentration | 0.310 +/-0.0093 ppm | (hb p. 11) |
| Algorithm version used in VAP | version 2.8 of David Turner's code | (hb p. 8) |
| Current version being run by developer (not yet in ARM VAP) | version 2.11 | (hb p. 19) |
| LBLRTM version used | version 12.1 | (hb p. 12) |
| MonoRTM version used | version 5.2 | (hb p. 12) |
| Cloud base height search interval (primary) | 20-minute interval from ceilometer | (hb p. 11) |
| Cloud base height search interval (expanded) | 180-minute interval if no cloud base found in 20-min window | (hb p. 11) |
| Default cloud base height | 2 km (used if no measured cloud base height found) | (hb p. 11) |
| RAP model output altitude range used to constrain upper... | 4 km to 20 km | (hb p. 9) |
| rmsr threshold for valid samples | less than 5 | (hb p. 12) |
| converged_flag valid range | greater than 0 and less than 9 | (hb p. 12) |
| Native AERI temporal resolution used in VAP | approximately 20 s frequency | (hb p. 16) |


## The data

Verified example: **`sgpaerioe1turnC1.c1`**, file `sgpaerioe1turnC1.c1.20230611.000348.nc`
(562.49 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=2976, `bound`=2, `height`=55, `gas_dim`=3, `dfs_dim`=16, `index_dim`=5, `obs_dim`=350, `arb`=123, `arb2`=123 |
| Data variables | 58 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 18 s |
| File time span | 2023-06-11T00:03:48 to 2023-06-11T21:59:43 |
| dod version | aerioe1turn-c1-1.0 |
| process version | $ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Akernal` | 1 | time,arb,arb2 | - | Averaging kernal |
| `Sa` | 1 | arb,arb2 | - | Prior covariance |
| `Sop` | 1 | time,arb,arb2 | - | Covariance matrix of the solution |
| `Xa` | 1 | arb | - | Prior mean state |
| `Xop` | 1 | time,arb | - | Optimal solution |
| `aqc_flag` | 1 | time | - | Manual QC flag |
| `arb` | 1 | arb | - | Arbitrary dimension |
| `cbh` | km | time | - | Cloud base height above ground level |
| `cbh_flag` | 1 | time | - | Flag indicating the source of the cloud base height |
| `ch4` | ppm | time,gas_dim | - | Methane concentration |
| `chi2` | 1 | time | - | Chi-square statistic of Y vs. F(Xn) |
| `co2` | ppm | time,gas_dim | - | Carbon dioxide concentration |
| `converged_flag` | 1 | time | - | Convergence flag |
| `convergence_criteria` | 1 | time | - | Convergence criteria di^2 |
| `dewpt` | degC | time,height | - | Dew point temperature |
| `dfs` | 1 | time,dfs_dim | - | Degrees of freedom of signal |
| `dindices` | 1 | time,index_dim | - | Derived indices |
| `forward_calc` | 1 | time,obs_dim | - | Forward calculation from state vector (i.e., F(Xn)) |
| `gamma` | 1 | time | - | Gamma parameter |
| `hatchOpen` | 1 | time | - | Flag indicating if the AERIs hatch was open |
| `height` | km | height | - | Height |
| `hour` | - | time | - | Time |
| `iReff` | um | time | - | Ice effective radius |
| `iTau` | 1 | time | - | Ice cloud optical depth (geometric limit) |
| `index_dim` | 1 | index_dim | - | Index dimension for derived indeces |
| `lReff` | um | time | - | Liquid water effective radius |
| `lwp` | g/m2 | time | - | Liquid water path |
| `n2o` | ppm | time,gas_dim | - | Nitrous oxide concentration |
| `n_iter` | 1 | time | - | Number of iterations performed |
| `obs_dim` | 1 | obs_dim | - | Dimension of the observation vector |


_26 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaerioe1turnC1.c1", "2023-06-11", "2023-06-11")
ds = armlive_open("sgpaerioe1turnC1.c1", "2023-06-11", "2023-06-11", cleanup_qc=True)
```

This product carries 58 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaerioe1turnC1.c1", start, end,
                  keep_variables=['Akernal', 'Sa', 'Sop'])
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `aqc_flag`, `converged_flag`, `cbh_flag`, `obs_flag`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaerioe1turnC1.c1", "20160101", "20260924")
```

The report's own note on quality: There is an overall qc_flag field but its logic is still under development and should not be used at this time. Instead, use converged_flag (valid when greater than 0 and less than 9) to determine usable retrievals. Two RMS fields, rmsr (AERI+MWR radiance residual) and rmsa (full observation vector residual), compare observations to the forward calculation using final retrieved fields; generally only samples with rmsr less than  5 should be used, though values above this threshold may still contain useful information. Uncertainty (sigma_X) fields are provided per scientific variable from the...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Limited information content above ~3 km or cloud base | Degrees of freedom for signal (dfs field) drops off; retrieved profile values above this altitude are not physically meaningful | Retrieved data above 3 km or cloud base should not be used, or used with caution | (hb p. 12) |
| Vertical resolution much coarser than the reported height grid, decreasing rapidly with... | Actual resolution (vres_temperature, vres_watervapor fields, from averaging kernel) may be 1 km or more aloft even though profile is reported on a fine height grid; sharp... | Use vres_temperature and vres_watervapor fields to assess true vertical resolution rather than assuming the output height grid resolution | (hb p. 12) |
| Unreliable overall qc_flag | qc_flag field present in output but its logic is still under development | Do not use qc_flag at this time; instead use converged_flag (valid when greater than 0 and less than 9) to determine usable retrievals | (hb p. 12) |
| Poor convergence / high residual retrievals | rmsr (AERI+MWR radiance residual) and rmsa (full observation vector residual) fields are elevated | Generally use only samples with rmsr less than  5, though retrievals above this threshold may still contain useful information | (hb p. 12) |
| Uncertainty estimates are incomplete | Reported sigma_X uncertainty fields only include correlated error from the prior, random observation error, and forward-model sensitivity | None stated beyond noting the limitation | (hb p. 13) |
| Ice cloud contamination of liquid water path retrieval | LWP retrieval shows biased (typically high) values when ice water content is mistakenly retrieved as liquid water, since only liquid-cloud properties are retrieved | None stated (noted as a known systematic error source); future work aims to add scattering treatment to better distinguish liquid and ice | (hb p. 13) |
| Cannot resolve elevated inversions or localized humidity/temperature gradients aloft | AERIoe profile shows smoothed transition instead of a sharp inversion or humidity gradient seen in radiosonde (e.g., top-of-boundary-layer humidity drop in late afternoon, Figure 6) | Still captures average/integrated profile information adequately for bulk quantities like CAPE/CIN; use with awareness of coarse resolution aloft | (hb p. 13) |
| Forward model does not include scattering | 1250-1350 cm-1 band (used by AERIPROF) is excluded from AERIoe because it is strongly influenced by cloud-particle scattering, which the absorption-only forward model cannot represent | Band excluded from retrieval; future development may add first-order scattering treatment | (hb p. 12) |
| Cloud base height not adjusted by retrieval and its uncertainty is unaccounted for | Cloud base height taken from ceilometer/lidar or defaulted to 2 km is held fixed; any error in this input does not propagate into reported retrieval uncertainties | None stated beyond noting the limitation | (hb p. 11) |
| MWR sensitivity/bias limitations affecting comparison and complementary use | 2-channel MWR (MWRRET) retrieval shows noise and misses most shallow cumulus low-LWP clouds due to insufficient sensitivity at 23/30 GHz; 3-channel MWR (89 GHz channel) retrieval is not... | AERIoe combines AERI+MWR data to better capture low LWP (less than 60 g/m2) where MWR alone underperforms | (hb p. 6) |
| AERI has very little information content above the boundary layer | Upper-atmosphere thermodynamic structure in output profile is essentially driven by RAP NWP model output rather than AERI observations | RAP model output (4-20 km) used to constrain upper atmosphere | (hb p. 9) |
| Trace gas and ice-cloud/optical-depth variables present but disabled | Output files contain empty variables for ice cloud optical depth, ice effective radius, and CO2/CH4/N2O concentrations that are not actually retrieved in this implementation | Left in file format for potential future use; currently disabled due to research nature | (hb p. 9) |
| Algorithm/version discrepancy between operational VAP and developer's current code | ARM VAP runs version 2.8 while Dr. Turner is running version 2.11 with minor improvements, so results may differ from latest published evaluations | ARM plans to continue working with developer to incorporate new versions | (hb p. 19) |
| Only SGP site currently processed operationally despite algorithm being site-agnostic | Users cannot obtain operational AERIoe VAP output for non-SGP ARM sites even though AERI instruments exist elsewhere | Plan to implement AERIoe at all ARM sites with an AERI, including development of new a priori datasets per site | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Turner and Löhnert 2014, J. Appl. Meteorol. Climatol. 53(3): 752-771
- Turner and Blumberg 2019, IEEE JSTARS 12(5): 1339-1354
- Rodgers/Rogers CD 2000, Inverse Methods for Atmospheric Sounding: Theory and Practice
- Feltz et al. 2003, J. Appl. Meteorol. 42(5): 584-597
- Turner 2007, J. Geophys. Res. 112(D15): D15204
- Turner et al. 2006, J. Atmos. Oceanic Technol. 23(9): 1223-1238 (AERI noise reduction)
- Knuteson et al. 2004a, J. Atmos. Oceanic Technol. 21(12): 1763-1776 (AERI Part 1: Instrument Design)
- Knuteson et al. 2004b, J. Atmos. Oceanic Technol. 21(12): 1777-1789 (AERI Part 2: Instrument Performance)
- Clough and Iacono 1995, J. Geophys. Res. 100(D8): 16519-16535 (LBLRTM)
- Clough et al. 2005, J. Quant. Spectrosc. Radiat. Transfer 91(2): 233-244 (MonoRTM/AER codes)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-234.pdf (23 pages, DOE/SC-ARM-TR-234, by LD Riihimaki, T Shippert, DD Turner)
- Catalog record: ARM data-source index, `instrument_class_code=aerioe`, read 2026-09-24
- Example file: `sgpaerioe1turnC1.c1.20230611.000348.nc` from `sgpaerioe1turnC1.c1`, 562.49 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
