---
name: arm-vap-mergedaerosol
description: ARM Merged Aerosol VAP (mergedaerosol) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (acsm_total_organics_CDCE, acsm_sulfate_CDCE, acsm_ammonium_CDCE, acsm_nitrate_CDCE, acsm_chloride_CDCE, acsm_vol_conc), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (epcmergedaerosolM1.c1) and the variable inventory of a real file. Use when working with mergedaerosol data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - mergedaerosol, Merged Aerosol VAP, epcmergedaerosolM1.c1, acsm_total_organics_CDCE, acsm_sulfate_CDCE, acsm_ammonium_CDCE, acsm_nitrate_CDCE, acsm_chloride_CDCE, Aerosols.
---

# MERGEDAEROSOL - Merged Aerosol VAP

The Merged Aerosol VAP consolidates multiple ARM aerosol instrument datastreams (chemical composition, optical properties, size distributions, particle number, CCN, hygroscopicity, trace gases, and aerosol optical depth) onto a single common one-hour timestamp file to streamline aerosol data analysis.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 10 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mergedaerosol` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-338 / JE Shilling, BE Ermold / May 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-338.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2016-11-14 to 2025-06-30 (retired) |
| Datastreams with data | 3 across 3 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mergedaerosol |


## Credit

Everything this skill knows about the retrieval is the work of **JE Shilling, BE Ermold** -
the ARM developers and mentors who wrote the technical report it derives from:

> JE Shilling, BE Ermold. *Merged Aerosol Value-Added Product Report*, DOE/SC-ARM-TR-338, May 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-338.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Extraction coverage.** the report is 10 pages and contains no retrieval-specification table, so that section is absent rather than omitted. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

The VAP does not measure a physical quantity itself but merges data from multiple existing ARM aerosol instruments. It uses the ARM Data Integration (ADI) tool to average all input datastreams to a common one-hour time resolution, matching the time resolution of the slowest instrument (the CCNC). The timestamp in the output files represents the midpoint of the time-averaging window. The VAP identifies the best available data when multiple datastreams exist for a single geophysical quantity, and reads QA/QC variables and DQRs to mark data with known issues as missing, indeterminate, or good.

**Cadence.** input rate varies by input instrument; output every one-hour; averaging Instruments with faster sampling rates than one measurement per hour are averaged over the time interval; timestamp represents the midpoint of the time-averaging window (hb p. 6).

## Inputs

The report names these instruments and sibling products: aerosol chemical speciation monitor (ACSM), cloud condensation nuclei counter (CCNC), SMPS, APS, UHSAS, CPC, SAP, MFRSR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| acsm_total_organics_CDCE | - | - | - | (hb p. 7) |
| acsm_sulfate_CDCE | - | - | - | (hb p. 8) |
| acsm_ammonium_CDCE | - | - | - | (hb p. 8) |
| acsm_nitrate_CDCE | - | - | - | (hb p. 8) |
| acsm_chloride_CDCE | - | - | - | (hb p. 8) |
| acsm_vol_conc | - | - | - | (hb p. 8) |
| aoppsap_Bs_B_1um | - | - | - | (hb p. 8) |
| aoppsap_Bs_G_1um | - | - | - | (hb p. 8) |
| aoppsap_Bs_R_1um | - | - | - | (hb p. 8) |
| aoppsap_Ba_B_Virkkula_1um | - | - | - | (hb p. 8) |
| aoppsap_Ba_G_Virkkula_1um | - | - | - | (hb p. 8) |
| aoppsap_Ba_R_Virkkula_1um | - | - | - | (hb p. 8) |
| aoppsap_ssa_B_1um | - | - | - | (hb p. 8) |
| aoppsap_ssa_G_1um | - | - | - | (hb p. 8) |
| aoppsap_ssa_R_1um | - | - | - | (hb p. 8) |
| aoppsap_Bs_B_10um | - | - | - | (hb p. 8) |
| aoppsap_Bs_G_10um | - | - | - | (hb p. 8) |
| aoppsap_Bs_R_10um | - | - | - | (hb p. 8) |
| aoppsap_Ba_B_Virkkula_10um | - | - | - | (hb p. 8) |
| aoppsap_Ba_G_Virkkula_10um | - | - | - | (hb p. 8) |
| aoppsap_Ba_R_Virkkula_10um | - | - | - | (hb p. 8) |
| aoppsap_ssa_B_10um | - | - | - | (hb p. 8) |


## The data

Verified example: **`epcmergedaerosolM1.c1`**, file `epcmergedaerosolM1.c1.20240211.003000.nc`
(0.13 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=24, `bound`=2, `mergedsmpsaps_diameter_mobility`=212, `ccnsmpskappa_setpoint`=7 |
| Data variables | 99 |
| QC variables | 46 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2024-02-11T00:30:00 to 2024-02-11T23:30:00 |
| dod version | mergedaerosol-c1-1.0 |
| process version | vap-mergedaerosol-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `N_CCN` | 1/cm^3 | time | yes | Mean number concentration of activated condensation nuclei |
| `acsm_ammonium_CDCE` | ug/m^3 | time | yes | Mass concentration of ammonium corrected for the CDCE, ambient... |
| `acsm_chloride_CDCE` | ug/m^3 | time | yes | Mass concentration of chloride corrected for the CDCE, ambient... |
| `acsm_nitrate_CDCE` | ug/m^3 | time | yes | Mass concentration of nitrate corrected for the CDCE, ambient aerosol... |
| `acsm_sulfate_CDCE` | ug/m^3 | time | yes | Mass concentration of sulfate corrected for the CDCE, ambient aerosol... |
| `acsm_total_organics_CDCE` | ug/m^3 | time | yes | Mass concentration of total organics corrected for the CDCE, ambient... |
| `acsm_vol_conc` | um^3/cm^3 | time | yes | ACSM volume concentration |
| `aoppsap_Ba_B_Virkkula_10um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel, 10 micron... |
| `aoppsap_Ba_B_Virkkula_1um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel, 1 micron... |
| `aoppsap_Ba_G_Virkkula_10um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel, 10... |
| `aoppsap_Ba_G_Virkkula_1um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel, 1 micron... |
| `aoppsap_Ba_R_Virkkula_10um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel, 10 micron... |
| `aoppsap_Ba_R_Virkkula_1um` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel, 1 micron... |
| `aoppsap_Bs_B_10um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 10 micron impactor,... |
| `aoppsap_Bs_B_1um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 1 micron impactor,... |
| `aoppsap_Bs_G_10um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 10 micron impactor,... |
| `aoppsap_Bs_G_1um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 1 micron impactor,... |
| `aoppsap_Bs_R_10um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 10 micron impactor,... |
| `aoppsap_Bs_R_1um` | 1/Mm | time | yes | Aerosol total light scattering coefficient, 1 micron impactor,... |
| `aoppsap_ssa_B_10um` | 1 | time | yes | Single scattering albedo at measured blue absorption wavelength, 10... |
| `aoppsap_ssa_B_1um` | 1 | time | yes | Single scattering albedo at measured blue absorption wavelength, 1... |
| `aoppsap_ssa_G_10um` | 1 | time | yes | Single scattering albedo at measured green absorption wavelength, 10... |
| `aoppsap_ssa_G_1um` | 1 | time | yes | Single scattering albedo at measured green absorption wavelength, 1... |
| `aoppsap_ssa_R_10um` | 1 | time | yes | Single scattering albedo at measured red absorption wavelength, 10... |
| `aoppsap_ssa_R_1um` | 1 | time | yes | Single scattering albedo at measured red absorption wavelength, 1... |
| `ccn_aerosol_number_concentration` | 1/cm^3 | time | yes | Aerosol particle number concentration |
| `ccn_supersaturation_calculated` | % | time | yes | Mean calculated supersaturation values for a fixed supersaturation... |
| `ccnsmps_kappa` | 1 | time | yes | Hygroscopicity parameter kappa |
| `ccnsmpskappa_critical_diameter` | nm | time | yes | Critical diameter |
| `co_dry` | ppmv | time | yes | Carbon monoxide (CO) mixing ratio corrected for water vapor... |


_19 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "epcmergedaerosolM1.c1",
                             "start": "2024-02-11", "end": "2024-02-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./epcmergedaerosolM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "epcmergedaerosolM1.c1", "2024-02-11", "2024-02-11")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("epcmergedaerosolM1.c1", "2024-02-11", "2024-02-11"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("acsm_total_organics_CDCE", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 99 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "epcmergedaerosolM1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["acsm_total_organics_CDCE", "acsm_sulfate_CDCE", "acsm_ammonium_CDCE", "qc_acsm_total_organics_CDCE", "qc_acsm_sulfate_CDCE", "qc_acsm_ammonium_CDCE"],
                                cleanup_qc=True)
```

## Quality control in this product

46 `qc_` companion variables cover 46 of the
99 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_acsm_total_organics_CDCE"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("acsm_total_organics_CDCE", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["acsm_total_organics_CDCE", "acsm_sulfate_CDCE", "acsm_ammonium_CDCE"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (epcmergedaerosolM1.c1.20240211.003000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `co_dry` | Transformation resulted in an indeterminate outcome. | 24 | 100.0 |
| `ccnsmps_kappa` | Transformation could not finish, or resulted in bad value (good... | 24 | 100.0 |
| `ccnsmpskappa_critical_diameter` | Transformation could not finish, or resulted in bad value (good... | 24 | 100.0 |
| `n2o_dry` | Transformation resulted in an indeterminate outcome. | 24 | 100.0 |
| `so2` | Transformation could not finish, or resulted in bad value (good... | 24 | 100.0 |
| `o3` | Transformation could not finish, or resulted in bad value (good... | 24 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("epcmergedaerosolM1.c1", "20161114", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: QA/QC variables in the input data are evaluated and simplified into three reporting options: good, indeterminate, and bad. For c1 processing, the VAP searches for applicable DQRs and applies them prior to averaging: data flagged 'suspect' are included in averages but output flagged indeterminate; data flagged 'incorrect' are excluded from averaging (with missing/indeterminate flags applied based on the fraction excluded, using the same 50%/75% thresholds as for generic bad/missing data). The c0 version does not include DQR checks; the c1 version does.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Data marked missing due to excessive bad/missing input data | If more than 75% of an input datastream is bad or missing in a given one-hour time block, the entire one-hour period is marked as missing in the output | Data for that one-hour period are marked as missing for the entire one-hour time period | (hb p. 6) |
| Indeterminate data due to partial bad/missing input data | If between 50% and 75% of the input data are bad or missing, the data are averaged and reported but flagged as indeterminate | Data are averaged and reported, but marked as indeterminate by the VAP code so users can decide whether to use it | (hb p. 6) |
| c0 (near-real-time) version lacks final input data | c0 files will not have final versions of some input data (e.g., ACSM CDCE) and will have missing values for data evaluated at campaign end (e.g., AOD at some sites) or otherwise unavailable... | Use the c1 version, generated after final input data become available (typically after campaign end or approximately yearly), for DQR-checked,... | (hb p. 6) |
| DQR 'suspect' flagged data included but marked indeterminate | Input data flagged as 'suspect' by a DQR are included in the average but the output is flagged as indeterminate | ARM data users can decide whether they would like to use these data, based on the QA/QC flags associated with that data variable | (hb p. 6) |
| DQR 'incorrect' flagged data excluded from averaging | Input data flagged as 'incorrect' by a DQR are excluded from the calculated average over that time period; if more than 75% of the data in a time block are excluded, the whole hour is... | Excluded from average if flagged incorrect; missing or indeterminate flag applied depending on exclusion fraction | (hb p. 7) |
| ACSM CDCE not finalized in near-real-time processing | acsmcdce.c1 or acsmtofcdce.c1 used for c0 output represents non-final composition-dependent collection efficiency; final version (acsmcdce.c2) only used for c1 output | Use c1 output for final CDCE-corrected values | (hb p. 7) |
| Merged size distribution unavailability fallback | When mergedsmpsaps.c1 is not available, size distribution instead comes from separate aosaps.b1, aossmps.b1, and aosuhsas.b1 datastreams, which may not be fully consistent with the merged... | aosaps.b1, aossmps.b1, aosuhsas.b1 used when merged size distribution not available | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-338.pdf (10 pages, DOE/SC-ARM-TR-338, by JE Shilling, BE Ermold)
- Catalog record: ARM data-source index, `instrument_class_code=mergedaerosol`, read 2026-09-24
- Example file: `epcmergedaerosolM1.c1.20240211.003000.nc` from `epcmergedaerosolM1.c1`, 0.13 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 10 pages and contains no retrieval-specification table, so that section is absent rather than omitted
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
