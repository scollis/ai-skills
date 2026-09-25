---
name: arm-vap-armtraj
description: ARM Airmass trajectories to support studies using ARM data (armtraj) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Airmass latitude, Airmass longitude, Airmass height above ground level, Airmass pressure, Airmass temperature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparmtrajpblC1.c1) and the variable inventory of a real file. Use when working with armtraj data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - armtraj, Airmass trajectories to support studies using ARM data, sgparmtrajpblC1.c1, Airmass latitude, Airmass longitude, Airmass height above ground level, Airmass pressure, Atmospheric Profiling.
---

# ARMTRAJ - Airmass trajectories to support studies using ARM data

The ARMTRAJ VAP provides seven ensemble airmass trajectory data sets (HYSPLIT driven by ERA5 reanalysis) initialized at ARM deployment coordinates to support aerosol, cloud, planetary boundary layer, AAF, and TBS studies using ARM data.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 176 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `armtraj` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-314 / I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei / August 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2013-10-01 to 2026-09-14 (active) |
| Datastreams with data | 50 across 12 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/armtraj |


## Credit

Everything this skill knows about the retrieval is the work of **I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei** -
the ARM developers and mentors who wrote the technical report it derives from:

> I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei. *ARM Trajectories Data Set Value-Added Product Report*, DOE/SC-ARM-TR-314, August 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Extraction coverage.** the report is 176 pages; pages 1-46 plus two appendix opening pages were read, and the repeating per-data-set variable appendices were not, so the specification and variable lists here are partial. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

Trajectory calculations use the Hybrid Single-Particle Lagrangian Integrated Trajectory (HYSPLIT) model informed by the ECMWF ERA5 reanalysis data set at its highest spatial resolution (0.25 degrees; ~31 km). HYSPLIT runs at multiple initial starting locations surrounding ARM deployments (in latitude/longitude and/or vertical coordinates), forming an ensemble for each sample. All ARMTRAJ data sets include ensemble runs initialized at relatively small horizontal and vertical offsets from ARM site coordinates, with horizontal offsets fixed at +/- 7.5 km (east-west and north-south) for most data sets, defining a 3x3 horizontal grid. ARMTRAJ reports the mean and standard deviation of all airmass coordinate and thermodynamic variables and most surface attribute variables; the ensemble mean increases fidelity while the standard deviation is treated as a measure of trajectory estimated uncertainty. The ARMTRAJ-ISOBAR data set instead calculates trajectories using only horizontal winds while following isobaric (constant pressure) surfaces, assuming quasi-horizontal air movement rather than using reanalysis vertical motion.

**Cadence.** output every Varies by data set: ARMTRAJ-SFC every 3 hours; ARMTRAJ-CLD and ARMTRAJ-PBL at SONDE release times rounded to nearest hour; ARMTRAJ-ARSCL and ARMTRAJ-ISOBAR every 3 hours; ARMTRAJ-AAF/TBS at 1-hour increments during system operation; averaging 1-hour mean and standard deviation values for surface/auxiliary observations (e.g., MET, ARSCL fields) starting at trajectory initialization time (hb p. 2).

## Inputs

The report names these instruments and sibling products: SONDE (Balloon-Borne Sounding System), MET (Surface Meteorological System), ARSCL (Active Remote Sensing of Clouds VAP), PBLHT (Planetary Boundary Layer Height VAP), AAF (ARM Aerial Facility, AAFNAVAIMS), TBS (Tethered Balloon System, TBSIMET), MWR (Microwave Radiometer).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Airmass latitude | degree_N | - | - | (hb p. 14) |
| Airmass longitude | degree_E | - | - | (hb p. 14) |
| Airmass height above ground level | m | - | - | (hb p. 14) |
| Airmass altitude above mean sea level | m | - | - | (hb p. 14) |
| Airmass pressure | hPa | - | - | (hb p. 14) |
| Airmass temperature | degC | - | - | (hb p. 14) |
| Airmass specific humidity | g/kg | - | - | (hb p. 14) |
| Airmass relative humidity | % | - | - | (hb p. 14) |
| Airmass relative humidity with respect to ice | % | - | - | (hb p. 14) |
| Airmass potential temperature | K | - | - | (hb p. 14) |
| Airmass equivalent potential temperature | K | - | - | (hb p. 14) |
| Airmass virtual potential temperature | K | - | - | (hb p. 14) |
| Mean hourly airmass ascent rate | m/s | - | - | (hb p. 14) |
| Planetary boundary-layer height in airmass column | m | - | - | (hb p. 14) |
| Surface altitude above mean sea level in airmass column | m | - | - | (hb p. 14) |
| Airmass height-to-PBLH ratio | 1 | - | - | (hb p. 14) |
| Land/sea cover | 1 | 0.0 (100% water) - 1.0 (100% land) | - | (hb p. 14) |
| Daily sea-ice cover | 1 | - | - | (hb p. 14) |
| Low vegetation type and cover | 1 | - | - | (hb p. 14) |
| High vegetation type and cover | 1 | - | - | (hb p. 14) |
| Soil type | 1 | - | - | (hb p. 14) |
| Subgrid-scale orography angle | radian | - | - | (hb p. 14) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| ERA5 spatial resolution used for HYSPLIT | 0.25 degrees (~31 km) | (hb p. 8) |
| Standard ensemble horizontal offset (most data sets) | ± 7.5 km east-west and north-south (3x3 grid) | (hb p. 8) |
| ARMTRAJ-SFC: back trajectory period | 240 hours (10 days) | (hb p. 2) |
| ARMTRAJ-SFC: ensemble members | 18 | (hb p. 2) |
| ARMTRAJ-SFC: initialization time | 00, 03, 06, 09, 12, 15, 18, 21 UTC | (hb p. 2) |
| ARMTRAJ-CLD: back/forward trajectory period | 120 hours (5 days) each | (hb p. 2) |
| ARMTRAJ-CLD: ensemble members | 27 per detected cloud layer | (hb p. 2) |
| ARMTRAJ-CLD: cloud detection RH threshold | 96% | (hb p. 10) |
| ARMTRAJ-CLD: layer concatenation distance | 50 m | (hb p. 10) |
| ARMTRAJ-CLD: minimum layer thickness | 25 m | (hb p. 10) |
| ARMTRAJ-PBL: back trajectory period | 120 hours (5 days) | (hb p. 2) |
| ARMTRAJ-PBL: ensemble members | 99 (PBL); 9 (free-tropospheric) | (hb p. 2) |
| ARMTRAJ-PBL: PBLH critical Richardson number | 0.25 | (hb p. 10) |
| ARMTRAJ-PBL: minimum PBLH set in HYSPLIT | 100 m AGL | (hb p. 11) |
| ARMTRAJ-PBL: free-tropospheric initialization height | 200 m above reported PBLH | (hb p. 10) |
| ARMTRAJ-ARSCL: back/forward trajectory period | 120 hours (5 days) each | (hb p. 2) |
| ARMTRAJ-ARSCL: ensemble members | 99 (cloud deck); 9 (free troposphere) | (hb p. 2) |
| ARMTRAJ-ARSCL: free-tropospheric height offset | 1-hour mean cloud top + 1-hour std + 200 m | (hb p. 11) |
| ARMTRAJ-AAF/TBS: back trajectory period | 120 hours (5 days) | (hb p. 2) |
| ARMTRAJ-AAF/TBS: ensemble members | 25 per flight altitude | (hb p. 2) |
| ARMTRAJ-AAF/TBS: ensemble grid configuration | 5x5 grid, dynamic spacing (max of 1-hour coordinate std or 3.75 km), capped at 50 km spacing (effective 15x15 to 100x100 km) | (hb p. 12) |
| ARMTRAJ-ISOBAR: back/forward trajectory period | 48 hours (2 days) each | (hb p. 2) |
| ARMTRAJ-ISOBAR: ensemble members | 25 per starting height | (hb p. 2) |
| ARMTRAJ-ISOBAR: starting altitudes | 15 equally distant altitudes between 200 and 1600 m AMSL (100 m increments) | (hb p. 12) |
| ARMTRAJ-ISOBAR: ensemble grid | 5x5 grid with 3.75 km increments | (hb p. 13) |
| ERA5 near-surface vertical resolution | ~250 m | (hb p. 11) |


## The data

Verified example: **`sgparmtrajpblC1.c1`**, file `sgparmtrajpblC1.c1.20260910.112307.nc`
(1.34 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=5, `trajectory_time`=121, `vert_layer`=3, `trajectory_type`=1 |
| Data variables | 231 |
| QC variables | 14 (`qc_` companions) |
| Median time step | 10799.5 s |
| File time span | 2026-09-10T11:23:07 to 2026-09-10T23:30:09 |
| dod version | armtrajpbl-c1-2.0 |
| process version | armtraj-1.12.3 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `sea_ice_cover` | 1 | time,trajectory_time,vert_layer | yes | Sea-ice cover fraction (based on monthly means) in airmass column |
| `sea_ice_cover_ens_mean` | 1 | time,trajectory_time | yes | Sea-ice cover fraction (based on monthly means) in airmass column... |
| `sea_ice_cover_ft` | 1 | time,trajectory_time | yes | Sea-ice cover fraction (based on monthly means) in airmass column... |
| `sea_ice_cover_ft_ens_mean` | 1 | time,trajectory_time | yes | Sea-ice cover fraction (based on monthly means) in airmass column... |
| `wvert` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate |
| `wvert_ens_max` | m/s | time,trajectory_time | yes | Mean hourly airmass ascent rate ensemble max |
| `wvert_ens_mean` | m/s | time,trajectory_time | yes | Mean hourly airmass ascent rate ensemble mean |
| `wvert_ens_min` | m/s | time,trajectory_time | yes | Mean hourly airmass ascent rate ensemble min |
| `wvert_ens_std` | m/s | time,trajectory_time | yes | Mean hourly airmass ascent rate ensemble std |
| `wvert_ft` | m/s | time,trajectory_time | yes | Free-troposphere mean hourly airmass ascent rate |
| `wvert_ft_ens_max` | m/s | time,trajectory_time | yes | Free-troposphere mean hourly airmass ascent rate ensemble max |
| `wvert_ft_ens_mean` | m/s | time,trajectory_time | yes | Free-troposphere mean hourly airmass ascent rate ensemble mean |
| `wvert_ft_ens_min` | m/s | time,trajectory_time | yes | Free-troposphere mean hourly airmass ascent rate ensemble min |
| `wvert_ft_ens_std` | m/s | time,trajectory_time | yes | Free-troposphere mean hourly airmass ascent rate ensemble std |
| `altitude_ens_max` | m | time,trajectory_time | - | Airmass altitude above mean sea level ensemble max |
| `altitude_ens_mean` | m | time,trajectory_time | - | Airmass altitude above mean sea level ensemble mean |
| `altitude_ens_min` | m | time,trajectory_time | - | Airmass altitude above mean sea level ensemble min |
| `altitude_ens_std` | m | time,trajectory_time | - | Airmass altitude above mean sea level ensemble std |
| `altitude_ft` | m | time,trajectory_time | - | Free-troposphere airmass altitude above mean sea level |
| `altitude_ft_ens_max` | m | time,trajectory_time | - | Free-troposphere airmass altitude above mean sea level ensemble max |
| `altitude_ft_ens_mean` | m | time,trajectory_time | - | Free-troposphere airmass altitude above mean sea level ensemble mean |
| `altitude_ft_ens_min` | m | time,trajectory_time | - | Free-troposphere airmass altitude above mean sea level ensemble min |
| `altitude_ft_ens_std` | m | time,trajectory_time | - | Free-troposphere airmass altitude above mean sea level ensemble std |
| `date` | - | time,trajectory_time | - | Trajectory date per trajectory type and time step |
| `height` | m | time,trajectory_time,vert_layer | - | Airmass height above ground level |
| `height_ens_max` | m | time,trajectory_time | - | Airmass height above ground level ensemble max |
| `height_ens_mean` | m | time,trajectory_time | - | Airmass height above ground level ensemble mean |
| `height_ens_min` | m | time,trajectory_time | - | Airmass height above ground level ensemble min |
| `height_ens_std` | m | time,trajectory_time | - | Airmass height above ground level ensemble std |
| `height_ft` | m | time,trajectory_time | - | Free-troposphere airmass height above ground level |


_183 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgparmtrajpblC1.c1",
                             "start": "2026-09-10", "end": "2026-09-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgparmtrajpblC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgparmtrajpblC1.c1", "2026-09-10", "2026-09-10")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgparmtrajpblC1.c1", "2026-09-10", "2026-09-10"))   # cite what you pulled
```

This product carries 231 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgparmtrajpblC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['sea_ice_cover', 'sea_ice_cover_ens_mean', 'sea_ice_cover_ft', 'qc_sea_ice_cover', 'qc_sea_ice_cover_ens_mean', 'qc_sea_ice_cover_ft'],
                                cleanup_qc=True)
```

## Quality control in this product

14 `qc_` companion variables cover 14 of the
231 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_wvert"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("wvert", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["wvert", "wvert_ft", "wvert_ens_mean"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgparmtrajpblC1.c1.20260910.112307.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `pbl_height_liu_liang` | neutral_boundary_layer | 5 | 100.0 |
| `sea_ice_cover` | airmass over land, sea-ice cover is N/A | 1371 | 75.5372 |
| `sea_ice_cover_ens_mean` | airmass over land, sea-ice cover is N/A | 359 | 59.3388 |
| `sea_ice_cover_ft_ens_mean` | airmass over land, sea-ice cover is N/A | 358 | 59.1736 |
| `sea_ice_cover_ft` | airmass over land, sea-ice cover is N/A | 351 | 58.0165 |
| `wvert` | Ascent rate missing due to final trajectory sample | 15 | 0.8264 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgparmtrajpblC1.c1", "20131001", "20260924")
```

The report's own note on quality: ARMTRAJ reports the mean and standard deviation of all airmass coordinate and thermodynamic variables and most surface attribute variables; the ensemble standard deviation can be treated as a measure of trajectory estimated uncertainty. Users are advised to filter ARMTRAJ-ISOBAR trajectories affected by dynamical forcing (e.g., using land_sea_mask to identify trajectories over open water) since the isobaric quasi-horizontal assumption is critical to validity.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Lack of explicit mixing in ECMWF IFS model driving ERA5 | PBL trajectory ensemble spread may not capture true near-surface turbulent mixing; addressed via extensive 99-member PBL ensemble | Extensive ensemble configuration (11 equally distant heights, 99 members) is used to ameliorate this limitation | (hb p. 11) |
| Limited near-surface resolution of ERA5 pressure level grid (~250 m) | Coarse vertical resolution near the surface reduces fidelity of low-altitude trajectory initialization/height | Minimum PBLH of 100 m AGL is set in HYSPLIT calculations; large ensemble used | (hb p. 11) |
| Lowest PBLH floor of 100 m AGL set in HYSPLIT | Reported PBL trajectory base heights cannot go below 100 m AGL even if true PBLH is lower | Ensemble configuration ameliorates the effect | (hb p. 11) |
| Sparse or incorrectly reported AAF/TBS altitudes (e.g., due to lack of GPS lock) | Spurious minimum/maximum altitude values in AAFNAVAIMS/TBSIMET data that could bias trajectory initialization heights | Use of 1st and 99th altitude percentiles instead of min/max values to set initialization altitudes | (hb p. 5) |
| Cloud top variability over 1-hour averaging window in ARMTRAJ-ARSCL | Free-tropospheric height sample may not represent instantaneous cloud top; large 1-hour standard deviation of cloud top height | Free-tropospheric height is set as 1-hour mean cloud top plus its 1-hour standard deviation plus 200 m | (hb p. 11) |
| Radiosonde RH sensor uncertainty affecting cloud detection | Cloud layer detection from SONDE RH profiles may misclassify borderline humid layers as cloud or clear-sky | RH threshold of 96% set considering Vaisala RS-41 4% RH uncertainty, consistent with prior comparisons to other cloud detection instruments | (hb p. 10) |
| Clear-sky periods excluded from ARMTRAJ-CLD and ARMTRAJ-ARSCL | No data set files/records generated for periods without detected liquid-bearing cloud or without a cloud deck | - | (hb p. 10) |
| Dependence of ARMTRAJ-PBL and ARMTRAJ-CLD on SONDE availability | Trajectory initialization only at radiosonde release times (rounded to nearest hour), resulting in only two to four starting times per day rather than continuous coverage | - | (hb p. 3) |
| Violation of quasi-horizontal air movement assumption in ARMTRAJ-ISOBAR | Isobaric trajectories become unreliable when significant vertical motion occurs, e.g., during meso- to synoptic-scale lifting or orographic forcing | Advised to filter trajectories believed to be influenced by dynamical forcing (e.g., using land_sea_mask to restrict to trajectories advected over... | (hb p. 6) |
| Non-zero land_sea_mask fractions near trajectory initialization in ARMTRAJ-ISOBAR | Fractional land_sea_mask values greater than 0.0 in the first few hours of a trajectory even for coastal/land-based ARM deployments (e.g., ENA, EPCAPE) | Those non-zero near-initialization values can be considered acceptable since ARM deployments are typically over land, not ship-borne | (hb p. 6) |
| Interpolation and numerical errors from reanalysis vertical motion field | Potential errors in trajectory vertical displacement when using full 3-D wind fields | ARMTRAJ-ISOBAR avoids this by using only horizontal winds along isobaric surfaces, applicable mainly in subtropical MBL regimes where vertical motion... | (hb p. 5) |
| Dynamic, non-fixed ensemble grid spacing for AAF trajectories | Ensemble grid shape can be rectangular rather than square and vary in size (15x15 km to 100x100 km) depending on AAF flight path, complicating direct comparison across flights | Grid point distance capped at 50 km to bound ensemble dimensions | (hb p. 5) |
| Limited applicability of full ensemble grid dynamics to TBS | For TBS, the dynamic grid spacing calculation is practically irrelevant given limited TBS drift; effectively fixed at 3.75 km | - | (hb p. 5) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Stein, AF, RR Draxler, GD Rolph, BJB Stunder, MD Cohen, and F Ngan. 2015. NOAA's HYSPLIT Atmospheric Transport and Dispersion Modeling System. BAMS 96(12): 2059-2077.
- Hersbach, H, et al. 2020. The ERA5 Global Reanalysis. QJRMS 146(730): 1999-2049.
- Holdridge, D. 2020. Balloon-Borne Sounding System (SONDE) Instrument Handbook. DOE/SC-ARM-TR-029.
- Kyrouac, J, and M Tuftedal. 2011. Surface Meteorological System (MET) Instrument Handbook. DOE/SC-ARM-TR-086.
- Sivaraman, C, et al. 2013. Planetary Boundary Layer Height (PBL) VAP: Radiosonde Retrievals. DOE/SC-ARM-TR-132.
- Clothiaux, EE, et al. 2001. The ARM Millimeter Wave Cloud Radars (MMCRs) and the ARSCL VAP. ARM VAP-002.1.
- Silber, I, JM Comstock, MR Kieburtz, and LM Russell. 2025. ARMTRAJ: A Set of Multipurpose Trajectory Datasets Augmenting ARM Measurements. Earth System Science Data 17(1): 29-42.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf (176 pages, DOE/SC-ARM-TR-314, by I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=armtraj`, read 2026-09-24
- Example file: `sgparmtrajpblC1.c1.20260910.112307.nc` from `sgparmtrajpblC1.c1`, 1.34 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 176 pages; pages 1-46 plus two appendix opening pages were read, and the repeating per-data-set variable appendices were not, so the specification and variable lists here are partial
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
