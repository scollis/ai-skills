---
name: arm-vap-rnccn
description: ARM Retrieved Number concentration of CCN (rnccn) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (RH corrected, Relative humidity, Temperature, Potential temperature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgprnccnprof1kulkarniC1.c1) and the variable inventory of a real file. Use when working with rnccn data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - rnccn, Retrieved Number concentration of CCN, sgprnccnprof1kulkarniC1.c1, RH corrected, Relative humidity, Temperature, Cloud Properties.
---

# RNCCN - Retrieved Number concentration of CCN

RNCCN is a value-added product that retrieves the vertical profile of cloud condensation nuclei (CCN) number concentration at multiple supersaturation set points, up to cloud base, by combining Raman lidar extinction and relative humidity profiles with surface CCN spectrum and aerosol humidification factor measurements at the SGP observatory.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 24 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `rnccn` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-292 / G Kulkarni, C Sivaraman, J Shilling / November 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-292.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2015-09-04 to 2023-10-31 (retired) |
| Datastreams with data | 4 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/rnccn |


## Credit

Everything this skill knows about the retrieval is the work of **G Kulkarni, C Sivaraman, J Shilling** -
the ARM developers and mentors who wrote the technical report it derives from:

> G Kulkarni, C Sivaraman, J Shilling. *Retrieved Number Concentration of Cloud Condensation Nuclei (RNCCN) Profile Value-Added Product Report*, DOE/SC-ARM-TR-292, November 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-292.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The 180-degree extinction (or backscatter) profile E(z) measured by a lidar is corrected to dry conditions, Ed(z), using a vertical profile of relative humidity (RH) and surface measurements of the dependence of scattering on relative humidity, f[RH(z)]: Ed(z) = E(z)/f[RH(z)]. Surface measurements of the CCN concentration at a given supersaturation, CCN(S,0), are then scaled by the ratio of the 180-degree extinction profile Ed(z) to the 180-degree extinction at or near the surface, Ed(0): CCN(S,z) = CCN(S,0)Ed(z)/Ed(0). The method rests on three assumptions: 1) aerosol composition and shape are independent of altitude, 2) the vertical structure of CCN concentration is identical to the vertical structure of dry extinction or backscatter, and 3) the largest particles (greater than 100 nm) that significantly contribute to extinction activate first. The dry extinction is computed as Ed(z,t) = E(z,t)*[(100-40)/(100-RH(z,t))]^(-gamma(t)), using a reference RH of 40% because ambient particles do not show enhancement in aerosol extinction below 40% RH, and gamma(t) is the aerosol humidification fit parameter (gamma coefficient) for the given time.

**Cadence.** output every one-hour resolution; averaging All input data are averaged to one-hour temporal resolution, corresponding to the temporal resolution of the aerosol humidification factor measurements. (hb p. 6).

## Inputs

The report names these instruments and sibling products: Raman lidar (RL), AOS (surface CCN spectrometer), ceilometer (cloud base height), rlproffex1thor VAP, rlprofmr2news10m datastream.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Retrieved number concentration of CCN (ccn_1...ccn_7) | cm-3 | - | - | (hb p. 8) |
| RH corrected (dry) extinction (ext_dry_mean) | km-1 | - | - | (hb p. 16) |
| Best-estimate particulate extinction coefficient... | 1/km | - | random and systematic uncertainty variables... | (hb p. 15) |
| Relative humidity (rh) | % | - | - | (hb p. 16) |
| Temperature | K | - | - | (hb p. 16) |
| Potential temperature | K | - | - | (hb p. 21) |
| AOS surface number concentration of CCN (N_CCN_1...N_CCN_7) | cm-3 | - | - | (hb p. 21) |
| Cloud base height (cbh) | km | valid_min 0 | - | (hb p. 22) |
| Calculated f(RH) (calculated_frh) | 1 | - | - | (hb p. 22) |
| Supersaturation set point | % | - | - | (hb p. 22) |
| Lifting condensation level (lcl) | km | - | - | (hb p. 16) |
| Aerosol linear depolarization ratio | 1 | - | - | (hb p. 15) |
| Best-estimate lidar ratio (lidar_ratio_be) | sr | - | - | (hb p. 15) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Temporal resolution of input data | one-hour | (hb p. 6) |
| Output vertical resolution | 60 meter (input lidar data resolution) | (hb p. 8) |
| Output temporal resolution | one-hour resolution | (hb p. 8) |
| Vertical extent of CCN profile | calculated up to cloud base (or maximum altitude) | (hb p. 8) |
| Number of supersaturation steps | seven values of percent supersaturation | (hb p. 8) |
| Reference relative humidity for f(RH) | RH_0 = 40% | (hb p. 7) |
| Gamma coefficient validity threshold | if gamma value exceeds 5 then the calculations are not performed | (hb p. 8) |
| Temperature validity threshold | if the temperature exceeds 273.15K | (hb p. 8) |
| Cloud-layer RH screening threshold | RH below first cloud layer above 85% and RH above 99% | (hb p. 8) |
| VAP processing unit | operates on one day (UTC) of data at a time | (hb p. 7) |
| DoD class name | rnccnprof1kulkarni.c1 | (hb p. 8) |
| Output file naming | SSSrnccnprof1kulkarniC1.c1.YYYYMMDD.hhmmss.nc | (hb p. 8) |
| Header version | version: 1.3 | (hb p. 14) |
| DOI | 10.5439/1813858 | (hb p. 23) |


## The data

Verified example: **`sgprnccnprof1kulkarniC1.c1`**, file `sgprnccnprof1kulkarniC1.c1.20231014.000500.nc`
(4.69 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=144, `bound`=2, `height`=299, `supersaturation_setpoint`=6 |
| Data variables | 44 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2023-10-14T00:05:00 to 2023-10-14T23:55:00 |
| dod version | rnccnprof1kulkarni-c1-1.3 |
| process version | vap-rnccnprof-0.0-0.dev0.dirty.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ccn_1` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 1 |
| `ccn_2` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 2 |
| `ccn_3` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 3 |
| `ccn_4` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 4 |
| `ccn_5` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 5 |
| `ccn_6` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 6 |
| `ccn_7` | cm-3 | time,height | yes | Retrieved number concentration of CCN at supersaturation step 7 |
| `N_CCN_1` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 1 |
| `N_CCN_2` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 2 |
| `N_CCN_3` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 3 |
| `N_CCN_4` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 4 |
| `N_CCN_5` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 5 |
| `N_CCN_6` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 6 |
| `N_CCN_7` | cm-3 | time | - | AOS surface number concentration of CCN at supersaturation step 7 |
| `calculated_frh` | 1 | time,height | - | Calculated f(RH) using equation f(RH) = C1(1-RH)^gamma, where C1 = (1... |
| `cbh` | km | time | - | Cloud base height |
| `depolarization_ratio` | 1 | time,height | - | Aerosol linear depolarization ratio |
| `ext_dry_mean` | km-1 | time,height | - | RH corrected extinction |
| `extinction_be` | 1/km | time,height | - | Best-estimate of the particulate extinction coefficient |
| `extinction_be_uncertainty_random` | 1/km | time,height | - | Random uncertainty in extinction_be |
| `extinction_be_uncertainty_systematic` | 1/km | time,height | - | Maximum systematic uncertainty in extinction_be |
| `feature_mask` | 1 | time,height | - | Feature mask |
| `height` | km | height | - | Height above ground level |
| `lcl` | km | time | - | Lifting condensation level |
| `lidar_ratio_be` | sr | time,height | - | Best-estimate of the lidar ratio |
| `mr_merged` | g/kg | time,height | - | High and Low merged water vapor mixing ratio |
| `mr_sonde` | g/kg | time,height | - | Water vapor mixing ratio from radiosondes |
| `potential_temperature` | K | time,height | - | Potential temperature |
| `pres_sonde` | mb | time,height | - | Pressure from radiosondes |
| `rh` | % | time,height | - | Relative humidity observed by the Raman lidar |


_3 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

The `act-arm-live` and `act-qc` skills wrap these calls in shorter helpers
(`armlive_open`, `armlive_list_files`, `act_qc_table`, `act_qc_apply`). Those are helpers
those skills define, **not** ACT functions - nothing below uses them, so every block here
runs against a bare `act-atmos` install.

```python
import os, requests, act

user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]

# ACT has no list-only call, so size the request against ARM Live's query endpoint
# before transferring anything.
avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f"{user}:{token}", "ds": "sgprnccnprof1kulkarniC1.c1",
                             "start": "2023-10-14", "end": "2023-10-14", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgprnccnprof1kulkarniC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgprnccnprof1kulkarniC1.c1", "2023-10-14", "2023-10-14")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgprnccnprof1kulkarniC1.c1", "2023-10-14", "2023-10-14"))   # cite what you pulled
```

This product carries 44 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgprnccnprof1kulkarniC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['ccn_1', 'ccn_2', 'ccn_3', 'qc_ccn_1', 'qc_ccn_2', 'qc_ccn_3'],
                                cleanup_qc=True)
```

## Quality control in this product

7 `qc_` companion variables cover 7 of the
44 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_ccn_1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("ccn_1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["ccn_1", "ccn_2", "ccn_3"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgprnccnprof1kulkarniC1.c1.20231014.000500.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `ccn_7` | Some of the input parameters were missing, no calculation is... | 43056 | 100.0 |
| `ccn_6` | The feature mask was detected as not aerosol and the extinction... | 38689 | 89.8574 |
| `ccn_1` | The feature mask was detected as not aerosol and the extinction... | 38689 | 89.8574 |
| `ccn_5` | The feature mask was detected as not aerosol and the extinction... | 38689 | 89.8574 |
| `ccn_4` | The feature mask was detected as not aerosol and the extinction... | 38689 | 89.8574 |
| `ccn_3` | The feature mask was detected as not aerosol and the extinction... | 38689 | 89.8574 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgprnccnprof1kulkarniC1.c1", "20150904", "20260924")
```

The report's own note on quality: Input variables are screened per Table 2 (rh, rh_ground, extinction_be, feature_mask, rh cloud, gamma_coefficient, potential temperature, temperature) before VAP calculation. Each output CCN variable (ccn_1...ccn_7) has a companion bit-packed qc_ccn_n variable where non-zero bits indicate specific QC conditions (assessed as Bad or Indeterminate) and a value of 0 indicates no failed QC tests. Bit assessments: bit_1 (RH missing, no calc) = Bad; bit_2 (surface RH missing, replaced) = Indeterminate; bit_3 (surface extinction missing, replaced) = Indeterminate; bit_4 (feature mask not aerosol,...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Missing relative humidity input | rh missing -greater than  no calculation performed for that profile; qc_ccn bit_1 set (assessment: Bad) | If the relative humidity from input data is missing, no calculation is performed. | (hb p. 7) |
| Missing surface relative humidity | surface RH gap filled from next height bin; qc_ccn bit_2 set (assessment: Indeterminate) | If the surface relative humidity value is missing, it is replaced with a value from the next height bin. | (hb p. 7) |
| Missing surface extinction value | surface extinction gap filled from next height bin; qc_ccn bit_3 set (assessment: Indeterminate) | If the surface extinction value is missing, it is replaced with a value from the next height bin. | (hb p. 7) |
| Non-aerosol feature mask contamination | extinction values set to missing where feature_mask indicates not-aerosol (e.g., cloud, rain/virga, ice); qc_ccn bit_4 set (assessment: Bad) | The feature mask was detected as not aerosol, then the extinction values were replaced as missing value. | (hb p. 8) |
| High humidity near cloud layer biasing f(RH)/extinction | RH below first cloud layer above 85% or RH above 99%; qc_ccn bit_5 and bit_7 set (assessment: Indeterminate) | Screened via rh cloud test in Table 2. | (hb p. 8) |
| Gamma coefficient out of valid range | gamma_coefficient exceeds 5; calculation not performed for that period | If gamma value exceeds 5 then the calculations are not performed. | (hb p. 8) |
| Atmospheric stability test failure using temperature/potential temperature profile | flagged via qc_ccn bit_6 (assessment: Bad) where the stability test fails | The atmospheric stability test using temperature profile failed leads to screening/flagging. | (hb p. 8) |
| Temperature exceeding freezing threshold | temperature exceeds 273.15K triggers screening condition per Table 2 | Screened per Table 2 variable list. | (hb p. 8) |
| Missing input parameters generally | qc_ccn bit_8 set (assessment: Bad) when some input parameters missing, no calculation performed | None specified beyond flagging as Bad. | (hb p. 17) |
| Retrieval limited to below cloud base | CCN profile output only extends up to cloud base (or maximum altitude); no values above cbh | None; inherent limitation of the retrieval method. | (hb p. 8) |
| Method assumptions may not hold | Retrieved profile may disagree with in-situ/aircraft CCN measurements when aerosol composition/shape varies with altitude, vertical CCN structure differs from dry extinction/backscatter... | None specified; inherent assumption of Ghan and Collins (2004) / Ghan et al. (2006) method. | (hb p. 6) |
| Implementation currently limited to one lidar type and one site | Data only available for SGP with Raman lidar input; not available at other ARM sites until future implementation | Future work will extend VAP to ENA and BNF observatories once RL data become available. | (hb p. 6) |
| Dependence on humidification factor f(RH) measurement quality | Errors or gaps in calculated_frh or gamma_coefficient propagate directly into ext_dry_mean and ccn_1...ccn_7 via Ed(z,t) correction | gamma_coefficient screening (values greater than 5 excluded) as noted in Table 2. | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Ghan, SJ, and DR Collins. 2004. "Use of in situ data to test a Raman lidar-based cloud condensation nuclei remote sensing method." Journal of Atmospheric and Oceanic Technology 21(2): 387–394.
- Ghan, SJ, TA Rissman, R Elleman, RA Ferrare, D Turner, C Flynn, J Wang, J Ogren, J Hudson, HH Johnsson, T VanReken, RC Flagan, and JH Seinfeld. 2006. "Use of in situ cloud condensation nuclei, extinction, and aerosol...
- Dawson, KW, RA Ferrare, RH Moore, MB Clayton, TJ Thorsen, and EW Eloranta. 2020. "Ambient aerosol hygroscopic growth from combined Raman lidar and HSRL." Journal of Geophysical Research – Atmospheres 125(7):...
- Newsom, R. 2022. Raman Lidar (RL) Instrument Handbook. DOE/SC-ARM/TR-038.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-292.pdf (24 pages, DOE/SC-ARM-TR-292, by G Kulkarni, C Sivaraman, J Shilling)
- Catalog record: ARM data-source index, `instrument_class_code=rnccn`, read 2026-09-24
- Example file: `sgprnccnprof1kulkarniC1.c1.20231014.000500.nc` from `sgprnccnprof1kulkarniC1.c1`, 4.69 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
