---
name: arm-vap-squire
description: ARM Surface QUantitatIve pRecipitation Estimation (SQUIRE) (squire) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Corrected reflectivity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (bnfcsapr2squireS3.c1) and the variable inventory of a real file. Use when working with squire data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - squire, Surface QUantitatIve pRecipitation Estimation (SQUIRE), bnfcsapr2squireS3.c1, Corrected reflectivity, Cloud Properties.
---

# SQUIRE - Surface QUantitatIve pRecipitation Estimation (SQUIRE)

SQUIRE is a value-added product that grids CMAC-corrected X-band precipitation radar moments and snow QPE fields from the SAIL campaign near Crested Butte, Colorado onto a Cartesian grid, selecting the lowest terrain-unblocked vertical level at each grid cell to produce surface estimates of reflectivity and liquid/snow precipitation rate.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 21 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `squire` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-287 / MA Grover, JR O'Brien, RC Jackson, ZS Sherman, SM Collis, BA Raut, A Theisen, M Tuftedal, D Feldman / April 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-287.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2021-12-01 to 2025-06-23 (retired) |
| Datastreams with data | 2 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/squire |


## Credit

Everything this skill knows about the retrieval is the work of **MA Grover, JR O'Brien, RC Jackson, ZS Sherman, SM Collis, BA Raut, A Theisen, M Tuftedal, D Feldman** -
the ARM developers and mentors who wrote the technical report it derives from:

> MA Grover, JR O'Brien, RC Jackson, ZS Sherman, SM Collis, BA Raut, A Theisen, M Tuftedal, D Feldman. *SAIL Field Campaign X-Band Precipitation Radar Surface Quantitative Precipitation Estimation (SQUIRE) Value-Added Product Report*, DOE/SC-ARM-TR-287, April 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-287.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

SQUIRE takes as input the Corrected Moments in Antenna Coordinates (CMAC) value-added product, which provides horizontal reflectivity corrected for attenuation and beam blockage along with liquid-equivalent snowfall rate estimates computed from empirical Ze = aS^b relationships between equivalent radar reflectivity factor and snowfall rate. These antenna-coordinate fields are transformed to a Cartesian grid using nearest-neighbor interpolation. Because terrain around the radar blocks or enhances the beam at different elevations, SQUIRE reduces the three-dimensional (height, latitude, longitude) grid to two dimensions by selecting, at each horizontal grid cell, the lowest vertical level not blocked by terrain (as determined by the CMAC fuzzy logic gate-identification algorithm). The corrected horizontal reflectivity, QPE fields, and the lowest valid vertical level (height) are then output at that lowest level for each grid cell, without further correction for the change of reflectivity factor with height between that level and the true surface.

## Inputs

The report names these instruments and sibling products: CMAC (Corrected Moments in Antenna Coordinates), XPRECIPRADAR (CSU X-Band Precipitation Radar), Ka-band ARM Zenith Radar (KAZR).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Equivalent Radar Reflectivity Factor (DBZ) | dBZ | - | - | (hb p. 16) |
| Corrected reflectivity | dBZ | - | - | (hb p. 16) |
| Rainfall Rate from Specific Attenuation (rain_rate_A) | mm/hr | valid_min 0.0 to valid_max 400.0 | - | (hb p. 16) |
| Snowfall rate from Z using WSR 88D High Plains... | mm/h | valid_min 0 to valid_max 500 | - | (hb p. 16) |
| Snowfall rate from Z using Matrosov et al.(2009)... | mm/h | valid_min 0 to valid_max 500 | - | (hb p. 17) |
| Snowfall rate from Z using Matrosov et al.(2009)... | mm/h | valid_min 0 to valid_max 500 | - | (hb p. 17) |
| Snowfall rate from Z using Wolf and Snider (2012)... | mm/h | valid_min 0 to valid_max 500 | - | (hb p. 18) |
| Height of the lowest Radar Gate (lowest_height) | m | - | - | (hb p. 18) |
| North latitude (lat) | degree_N | valid_min -90 to valid_max 90 | - | (hb p. 18) |
| East longitude (lon) | degree_E | valid_min -180 to valid_max 180 | - | (hb p. 19) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Domain horizontal extent (x direction by y direction) | 40 km x 40 km | (hb p. 10) |
| Domain vertical extent | 5 km | (hb p. 10) |
| Horizontal resolution | 250 m | (hb p. 10) |
| Vertical resolution | 250 m | (hb p. 10) |
| Gridding routine | Nearest neighbor | (hb p. 10) |
| Radius of influence | 250 m | (hb p. 10) |
| Lowest vertical level (above ground level) | 250 meters above ground level | (hb p. 10) |
| Z(S) relationship - Wolfe and Snider (2012) | Z = 110S^2, A=110, B=2, S band | (hb p. 9) |
| Z(S) relationship - WSR-88D High Plains | Z = 130S^2, A=130, B=2, S band | (hb p. 9) |
| Z(S) relationship - Braham (1990) 1 | Z = 67S^1.28, A=67, B=1.28, X band | (hb p. 9) |
| Z(S) relationship - Braham (1990) 2 | Z = 114S^1.39, A=114, B=1.39, X band | (hb p. 9) |
| swe_ratio (all snow rate fields) | 13.699 | (hb p. 16) |
| Grid dimensions | time = 1, y = 161, x = 161 | (hb p. 15) |
| Conventions | ARM-1.3 CF/Radial instrument_parameters | (hb p. 19) |
| DOI | 10.5439/1884979 | (hb p. 20) |


## The data

Verified example: **`bnfcsapr2squireS3.c1`**, file `bnfcsapr2squireS3.c1.20250619.000416.nc`
(59.77 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=142, `y`=171, `x`=141 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 603 s |
| File time span | 2025-06-19T00:04:16 to 2025-06-19T00:00:00 |
| dod version | csapr2squire-c1-1.1 |
| process version | vap-squire-0.0-0.dev0.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `corrected_reflectivity` | dBZ | time,y,x | - | Corrected reflectivity |
| `lowest_height` | m | time,y,x | - | Height of the lowest radar gate |
| `rain_rate_A` | mm hr-1 | time,y,x | - | Rainfall rate calculated from specific attenuation |
| `rain_rate_Z` | mm hr-1 | time,y,x | - | Rainfall rate calculated from reflectivity |
| `rain_rate_combined` | mm hr-1 | time,y,x | - | Rainfall rate calculated from a blend of rainfall rate estimates from... |
| `time` | - | time | - | Time offset from midnight |
| `x` | m | x | - | X distance on the projection plane to the origin |
| `y` | m | y | - | Y distance on the projection plane to the origin |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("bnfcsapr2squireS3.c1", "2025-06-19", "2025-06-19")
ds = armlive_open("bnfcsapr2squireS3.c1", "2025-06-19", "2025-06-19", cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("bnfcsapr2squireS3.c1", "20211201", "20260924")
```

The report's own note on quality: Global attribute 'comment' states the data are highly experimental/initial with many known and unknown issues and instructs users not to use the data before contacting the responsible Translator (scollis@anl.gov). Global attribute 'known_issues' lists: false phidp jumps in insect regions, continued use of old Giangrande code, and issues with some snow below the melting layer. rain_rate_A is explicitly set to 0.0 where normalized coherent power less than  0.4 or rhohv less than  0.8.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Beam blockage by terrain (mountains) | Missing or reduced reflectivity at low elevations near high terrain; lowest usable vertical level increases with terrain height and distance from radar (Figure 4) | SQUIRE selects, at each grid cell, the lowest vertical level not blocked by terrain rather than using a fixed lowest level | (hb p. 10) |
| Excluded terrain-enhanced/blocked regions if using a fixed lowest vertical level | Gaps or unrealistic values in the 250 m above-ground-level lowest level product over blocked terrain | Use the terrain-aware lowest-valid-level selection implemented in SQUIRE instead of a single fixed vertical level | (hb p. 10) |
| No correction for change of reflectivity factor with height | Reflectivity and snowfall rates projected from the lowest valid elevation to the surface may be biased where that elevation is well above ground | Future work will use Ka-band ARM Zenith Radar to characterize and correct for reflectivity change with height | (hb p. 12) |
| High uncertainty in liquid-equivalent estimates from snow | Disagreement among the four different empirical Z(S) snowfall-rate fields (snow_rate_ws88diw, snow_rate_m2009_1, snow_rate_m2009_2, snow_rate_ws2012) for the same reflectivity input | Product reports multiple empirical relationships (Table 1) rather than a single one; see CMAC technical document for further discussion | (hb p. 12) |
| Rain rate set to zero under low correlation/coherence conditions | rain_rate_A forced to 0.0 where normalized coherent power less than  0.4 or rhohv less than  0.8 | - | (hb p. 16) |
| False phidp jumps in insect regions (inherited from CMAC/LP code) | Spurious phase jumps and downstream artifacts in corrected fields in regions with insect contamination | Noted as a known issue; still uses old Giangrande LP code | (hb p. 20) |
| Issues with snow below the melting layer | Unreliable or inconsistent snow rate values in melting-layer-affected gates | - | (hb p. 20) |
| Experimental/initial data status | Data flagged with global comment as highly experimental with many known and unknown issues | Contact the Translator (scollis@anl.gov) before use | (hb p. 20) |
| Best-estimate nature of terrain-based gate selection | Output represents a best estimate combining terrain, precipitation, and available scientific information rather than a verified ground-truth surface value | - | (hb p. 12) |
| CMAC gate-ID algorithm changes affect SQUIRE outputs over time | Discontinuities or version-dependent differences in gate identification and hence lowest_height/QPE fields as CMAC improves | SQUIRE will be updated to reflect CMAC gate-ID improvements | (hb p. 12) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- O'Brien, JR, et al. 2023. CSU X-Band Precipitation Radar PPI Data Processed with CMAC Technical Report. U.S. DOE.
- Helmus, JJ, and SM Collis. 2016. The Python ARM Radar Toolkit (Py-ART). Journal of Open Research Software 4(1): e25.
- Braham, RR. 1990 (Z(S) relationships as cited in Table 1).
- Wolfe and Snider. 2012 (Z(S) relationship as cited in Table 1).
- Varble, A, et al. 2019. CACTI Field Campaign Report. DOE/SC-ARM-19-028.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-287.pdf (21 pages, DOE/SC-ARM-TR-287, by MA Grover, JR O'Brien, RC Jackson, ZS Sherman, SM Collis, BA Raut, A Theisen, M Tuftedal, D Feldman)
- Catalog record: ARM data-source index, `instrument_class_code=squire`, read 2026-09-24
- Example file: `bnfcsapr2squireS3.c1.20250619.000416.nc` from `bnfcsapr2squireS3.c1`, 59.77 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
