---
name: arm-vap-armlagtraj
description: ARM Lagrangian large-scale forcing data following a trajectory (armlagtraj) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Domain-mean temperature, Trajectory-centered temperature, Domain-mean vertical velocity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with armlagtraj data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - armlagtraj, Lagrangian large-scale forcing data following a trajectory , mos60armlagtrajecmwfM1.c1, Domain-mean temperature, Trajectory-centered temperature, Atmospheric Profiling.
---

# ARMLAGTRAJ - Lagrangian large-scale forcing data following a trajectory 

ARMLAGTRAJ is a value-added product that generates Lagrangian (and Eulerian) large-scale forcing data along an air-mass trajectory (e.g., following a ship-based moving observational platform) by extracting ERA5 reanalysis profiles and fluxes along the trajectory and combining them with co-located ARM observations for use as SCM/CRM/LES model input and evaluation data.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 18 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `armlagtraj` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-306 / C Tao, M Zhang, S Xie / August 2024](https://www.arm.gov/publications/tech_reports/DOE-SC-ARM-TR-306.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2012-09-20 to 2020-01-31 (retired) |
| Datastreams with data | 3 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/armlagtraj |


## Credit

Everything this skill knows about the retrieval is the work of **C Tao, M Zhang, S Xie** -
the ARM developers and mentors who wrote the technical report it derives from:

> C Tao, M Zhang, S Xie. *Development of the ARM Lagrangian Large-Scale Forcing Data (ARMLAGTRAJ) Value-Added Product Based on the lagtraj Framework*, DOE/SC-ARM-TR-306, August 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/DOE-SC-ARM-TR-306.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm, based on the open-source lagtraj framework, first downloads ERA5 reanalysis data for the domain and time period of interest. It then produces a trajectory file using winds at either a single height/pressure level or a weighted average between two levels, or, as a new ARMLAGTRAJ feature, uses trajectory information from an existing trajectory data set (e.g., ship locations for MOSAiC). Forcing profiles (domain-mean and trajectory-centered/"local") are then extracted along the trajectory, with flexibility to choose output levels, averaging width for means and gradients, and optional land/ocean masking. The derived forcing profiles are converted to an ARM-type format similar to VARANAL, and available ARM observational variables are appended to the output for direct comparison with the ERA5-derived quantities.

**Cadence.** output every 60 minutes (hourly); averaging 60 minutes (hb p. 8).

## Inputs

The report names these instruments and sibling products: VARANAL, ARMBE, lagtraj, mosarmbecldradM1, mossondewnpnM1.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Domain-mean temperature (T) | K | - | - | (hb p. 10) |
| Trajectory-centered temperature (T_local) | K | - | - | (hb p. 10) |
| Domain-mean water vapor mixing ratio (q) | g/kg | - | - | (hb p. 11) |
| Domain-mean horizontal wind U component (u) | m/s | - | - | (hb p. 11) |
| Domain-mean horizontal wind V component (v) | m/s | - | - | (hb p. 11) |
| Domain-mean vertical velocity (omega) | mb/hr | - | - | (hb p. 11) |
| Domain-mean horizontal wind divergence (div) | 1/s | - | - | (hb p. 11) |
| Domain-mean horizontal temperature advection (T_adv_h) | K/hr | - | - | (hb p. 11) |
| Domain-mean horizontal q advection (q_adv_h) | g/kg/hr | - | - | (hb p. 12) |
| Domain-mean derivative of air temperature w.r.t. time (dTdt) | K/hr | - | - | (hb p. 12) |
| Domain-mean derivative of water vapor mixing ratio w.r.t.... | g/kg/hr | - | - | (hb p. 12) |
| Domain-mean surface latent heat flux (LH) | W/m2 | - | - | (hb p. 12) |
| Domain-mean surface sensible heat flux (SH) | W/m2 | - | - | (hb p. 12) |
| Domain-mean surface pressure averaged over domain... | mb | - | - | (hb p. 12) |
| Domain-mean surface pressure at center of domain... | mb | - | - | (hb p. 12) |
| Surface U component (u_srf) | m/s | - | - | (hb p. 12) |
| Surface V component (v_srf) | m/s | - | - | (hb p. 13) |
| Domain-mean TOA LW flux (lw_net_toa) | W/m2 | - | - | (hb p. 13) |
| Domain-mean TOA net SW flux (sw_net_toa) | W/m2 | - | - | (hb p. 13) |
| Domain-mean TOA solar insolation (sw_dn_toa) | W/m2 | - | - | (hb p. 13) |
| Domain-mean total cloud (cld_tot) | % | - | - | (hb p. 13) |
| Liquid water path (LWP) | g/m2 | - | - | (hb p. 13) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Trajectory domain size | about 111x111 km2 | (hb p. 17) |
| Vertical levels (lev dimension) | 211 | (hb p. 10) |
| Time resolution | 60-min (hourly) | (hb p. 8) |
| averaging_interval (global attribute) | 60 minutes | (hb p. 17) |
| dod_version | 60armlagtrajecmwf-c1-1.0 | (hb p. 17) |
| Input reanalysis data set | ERA5 (ECMWF Reanalysis 5) | (hb p. 6) |
| Output file convention | XXX60armlagtrajecmwfFF.c1.YYYYMMDD.hhmmss.cdf | (hb p. 8) |


## The data

**No example file was verified for this instrument.** ARM Live refused every query for this product, which is served only at level a0.

ARM's catalog lists 3 datastreams with data across 2 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "mos60armlagtrajecmwfM1.c1", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
                     params={"user": f"{user}:{token}", "ds": "mos60armlagtrajecmwfM1.c1",
                             "start": "2020-01-31", "end": "2020-01-31", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./mos60armlagtrajecmwfM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "mos60armlagtrajecmwfM1.c1", "2020-01-31", "2020-01-31")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("mos60armlagtrajecmwfM1.c1", "2020-01-31", "2020-01-31"))   # cite what you pulled
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you have a
file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("mos60armlagtrajecmwfM1.c1", "20120920", "20260924")
```

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Dependence on ERA5 reanalysis fidelity | ERA5-derived quantities (e.g., column precipitable water, surface downward longwave radiation) broadly but not exactly match ARM observed values in comparison time series; discrepancies... | Both ERA5 and ARM observation variables are included in the output file so users can directly compare and choose which to use when driving model... | (hb p. 7) |
| Forcing extraction settings dependence | Extracted forcing profiles can vary depending on chosen output levels, averaging width for mean calculations and gradients, and whether land/ocean masking is applied, so results are... | Handbook notes flexibility to select output levels, averaging width, and masking, implying users should be aware these choices affect the forcing | (hb p. 6) |
| Trajectory type dependence (domain-mean vs. trajectory-centered/local) | Output includes both domain-mean (e.g., T, q, u, v) and trajectory-centered/local (e.g., T_local, cld_tot_local, PW_local) versions of similar quantities, which can differ from each other... | - | (hb p. 10) |
| Traditional VARANAL forcing limited to fixed locations | Legacy ARM large-scale forcing data (VARANAL) does not support moving/ship-based platforms; motivated the need for the new Lagrangian product | ARMLAGTRAJ developed based on the lagtraj framework to extend forcing to moving platforms | (hb p. 6) |
| New trajectory type derived from existing trajectory dataset | For MOSAiC, the trajectory follows recorded ship locations rather than being computed purely from wind fields; if the external trajectory dataset has gaps or errors, they would propagate... | - | (hb p. 7) |
| Version/process attributes left blank in output | Global attributes such as process_version, platform_id, data_level, site_id, facility_id, and location_description are empty strings in the example file header | - | (hb p. 17) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Boeing, S, L Denby, PN Blossey, R Neggers, Z Cui, R Burton, and L Saffin. 2020. Sensitivity of EUREC4A/ATOMIC LES to large-scale tendencies.
- Hersbach, H, et al. 2020. The ERA5 global reanalysis. QJRMS 146(730): 1999-2049.
- Tang, S, C Tao, S Xie, and M Zhang. 2019. Description of the ARM Large-Scale Forcing Data from the Constrained Variational Analysis (VARANAL) Version 2. DOE/SC-ARM-TR-222.
- Xie, S, RT Cederwall, and M Zhang. 2004. Developing long-term single-column model/cloud system-resolving model forcing data. JGR-Atmospheres 109(D1): D01104.
- Xie, S, RB McCoy, SA Klein, et al. 2010. ARM climate modeling best estimate data. BAMS 91(1): 13-20.
- Zhang, M, and J Lin. 1997. Constrained Variational Analysis of Sounding Data. J Atmos Sci 54(11): 1503-1524.
- Zhang, M, J Lin, RT Cederwall, JJ Yio, and SC Xie. 2001. Objective Analysis of ARM IOP Data. Mon Wea Rev 129(2): 295-311.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/DOE-SC-ARM-TR-306.pdf (18 pages, DOE/SC-ARM-TR-306, by C Tao, M Zhang, S Xie)
- Catalog record: ARM data-source index, `instrument_class_code=armlagtraj`, read 2026-09-24
- Example file: none - ARM Live refused every query for this product, which is served only at level a0
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
