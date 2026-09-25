---
name: arm-vap-pblht
description: ARM Planetary Boundary Layer Height (pblht) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (PBL height, PBL height, PBL height, PBL height, PBL regime type, Potential temperature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgppblhtsonde1mcfarlC1.c1) and the variable inventory of a real file. Use when working with pblht data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - pblht, Planetary Boundary Layer Height, sgppblhtsonde1mcfarlC1.c1, PBL height, PBL regime type, Atmospheric Profiling.
---

# PBLHT - Planetary Boundary Layer Height

The PBLHeightSonde VAP derives planetary boundary layer (mixing layer) height estimates from ARM balloon-borne radiosonde profiles (sondewnpn.b1/a1) using three independent algorithms (Heffter, Liu-Liang, bulk Richardson number), producing per-sonde and yearly output files at ARM fixed and mobile facility sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 36 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `pblht` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-132 / C Sivaraman, S McFarlane, E Chapman, M Jensen, T Toto, S Liu, M Fischer / August 2013](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-132.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2001-04-01 to 2026-09-24 (active) |
| Datastreams with data | 119 across 31 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/pblht |


## Credit

Everything this skill knows about the retrieval is the work of **C Sivaraman, S McFarlane, E Chapman, M Jensen, T Toto, S Liu, M Fischer** -
the ARM developers and mentors who wrote the technical report it derives from:

> C Sivaraman, S McFarlane, E Chapman, M Jensen, T Toto, S Liu, M Fischer. *Planetary Boundary Layer (PBL) Height Value Added Product (VAP): Radiosonde Retrievals*, DOE/SC-ARM/TR-132, August 2013.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-132.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP uses vertical profiles of pressure, temperature, relative humidity, wind speed and wind direction from radiosonde soundings to compute potential temperature (and virtual potential temperature) at each level, then subsamples the profile onto a 5 mb pressure grid to reduce noise. Boundary layer regime (convective CBL, stable SBL, or neutral residual layer NRL) is classified from the near-surface potential temperature gradient between the 2nd and 5th subsampled levels relative to a site-dependent stability threshold. Three physically distinct methods are then applied to the same profile: the Liu-Liang (2010) method finds the height where a rising air parcel becomes neutrally buoyant (CBL/NRL) or searches for stability/wind-shear-based inversions and low-level jets (SBL); the Heffter (1980) method identifies inversion layers where the potential temperature lapse rate exceeds 0.005 K/m and locates the lowest layer where the potential temperature difference across the inversion reaches 2 K; and the bulk Richardson number method locates the height at which the ratio of buoyant to shear-generated turbulence (Rib) first exceeds a critical threshold (0.25 or 0.5). Because PBL height has no independently verifiable 'truth' and its definition is somewhat subjective, multiple methods are retained so that the spread between them serves as a partial estimate of uncertainty.

**Cadence.** input rate per radiosonde launch (as scheduled at each ARM site); output every daily output file per sonde launch; yearly aggregate file per site; averaging radiosonde profile subsampled to 5 mb pressure resolution; Heffter method further smoothed via three-point moving average to 15 mb (hb p. 8).

## Inputs

The report names these instruments and sibling products: radiosonde (sondewnpn), ceilometer, backscatter lidar, Doppler wind lidar, sodar, radar wind profiler.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| PBL height (Heffter method) | m above mean sea level | - | - | (hb p. 21) |
| PBL height (Liu-Liang method) | m above mean sea level | - | - | (hb p. 21) |
| PBL height (bulk Richardson, threshold 0.25) | m above mean sea level | - | - | (hb p. 21) |
| PBL height (bulk Richardson, threshold 0.5) | m above mean sea level | - | - | (hb p. 21) |
| PBL regime type (Liu-Liang) | categorical (-2=CBL,... | - | - | (hb p. 9) |
| Potential temperature (theta) | K | - | - | (hb p. 8) |
| Virtual potential temperature | K | - | - | (hb p. 12) |
| Bulk Richardson number | dimensionless | - | - | (hb p. 12) |
| Potential temperature lapse rate | K/m (also expressed K/km) | - | - | (hb p. 21) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Subsampling resolution | 5 mb pressure grid | (hb p. 8) |
| Heffter smoothing resolution | 15 mb (three-point moving average) | (hb p. 11) |
| Inversion lapse rate threshold (Heffter) | 0.005 K/m (also stated as greater than  5 K/km) | (hb p. 11) |
| Inversion potential temperature difference threshold... | 2 K | (hb p. 11) |
| Max inversion AGL for valid Heffter PBL height | 4 km AGL | (hb p. 11) |
| Max PBL height (Liu-Liang / bulk Richardson) before flagged... | 4 km AGL | (hb p. 13) |
| Bulk Richardson critical thresholds | 0.25 and 0.5 | (hb p. 12) |
| delta_s (inversion_strength_threshold) Land | 1.0 K | (hb p. 10) |
| delta_s (inversion_strength_threshold) Ocean/Ice | 0.2 K | (hb p. 10) |
| delta_u (instability_threshold) Land | 0.5 K | (hb p. 10) |
| delta_u (instability_threshold) Ocean/Ice | 0.1 K | (hb p. 10) |
| theta_r_dot (overshoot_threshold) Land | 4.0 K/km | (hb p. 10) |
| theta_r_dot (overshoot_threshold) Ocean/Ice | 0.5 K/km | (hb p. 10) |
| Local peak curvature threshold (SBL stability criterion) | less than  -40 K/km | (hb p. 9) |
| LLJ nose wind speed excess | at least 2 m/s stronger than layers immediately above and below | (hb p. 9) |
| Near-surface wind speed QC threshold | 33.5 m/s (below 50 m AGL) | (hb p. 13) |
| R/cpd (dry air) | 0.286 | (hb p. 8) |
| Reference pressure p0 | 1000 hPa | (hb p. 8) |
| epsilon (water vapor/dry air molecular weight ratio) | 0.622 | (hb p. 12) |
| Reference temperature T1 | 273.15 K | (hb p. 12) |
| Reference saturation vapor pressure es1 | 6.11 hPa | (hb p. 12) |
| Max number of inversion layers identified (Heffter) | up to five | (hb p. 11) |
| Search height floor for Liu-Liang CBL/NRL criteria | above 150 m AGL | (hb p. 9) |


## The data

Verified example: **`sgppblhtsonde1mcfarlC1.c1`**, file `sgppblhtsonde1mcfarlC1.c1.20260917.185609.nc`
(0.19 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4957, `height_ss`=190, `layer`=5 |
| Data variables | 33 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-17T18:56:09 to 2026-09-17T20:18:44 |
| dod version | pblhtsonde1mcfarl-c1-2.1 |
| process version | pblhtsonde-2.1.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pbl_height_bulk_richardson_pt25` | m | - | yes | Planetary boundary layer height above mean sea level calculated from... |
| `pbl_height_bulk_richardson_pt5` | m | - | yes | Planetary boundary layer height above mean sea level calculated from... |
| `pbl_height_heffter` | m | - | yes | Planetary boundary layer height above mean sea level calculated using... |
| `pbl_height_liu_liang` | m | - | yes | Planetary boundary layer height above mean sea level calculated by... |
| `pbl_regime_type_liu_liang` | 1 | - | yes | Planetary boundary layer regime type determined by Liu and Liang... |
| `air_temp` | degC | time | - | Dry bulb ambient air temperature |
| `atm_pres` | hPa | time | - | Atmospheric pressure |
| `atm_pres_ss` | hPa | height_ss | - | Sonde-measured pressure closest to the bottom of the 5 mb subsampling... |
| `bottom_inversion` | m | layer | - | Height above mean sea level at bottom of inversion layer from Heffter... |
| `delta_theta_max` | K | layer | - | The maximum difference in potential temperature across inversion... |
| `height_ss` | m | height_ss | - | Height above mean sea level subsampled at 5 mb resolution |
| `lapserate_max` | K/m | layer | - | Maximum lapse rate in inversion layer from Heffter (1980) method |
| `lapserate_theta_smoothed` | K/m | height_ss | - | Potential temperature lapse rate subsampled at 5 mb resolution and... |
| `lapserate_theta_ss` | K/m | height_ss | - | Potential temperature lapse rate subsampled at 5 mb resolution |
| `layer` | 1 | layer | - | Inversion layer number for Heffter (1980) method |
| `level_1_liu_liang` | m | - | - | Level 1 height above mean sea level calculated by the Liu and Liang... |
| `level_2_liu_liang` | m | - | - | Level 2 height above mean sea level calculated by the Liu and Liang... |
| `pressure_gridded` | hPa | height_ss | - | Pressure grid for 5 mb subsampling |
| `rh` | % | time | - | Relative humidity |
| `richardson_number` | 1 | height_ss | - | Bulk Richardson number |
| `theta_ss` | K | height_ss | - | Potential temperature subsampled at 5 mb resolution |
| `time` | - | time | - | Time offset from midnight |
| `top_inversion` | m | layer | - | Height above mean sea level at top of inversion layer from Heffter... |
| `virtual_theta_ss` | K | height_ss | - | Virtual potential temperature |
| `wspd` | m/s | time | - | Wind speed |
| `wspd_ss` | m/s | height_ss | - | Wind speed subsampled at 5 mb resolution |


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
                     params={"user": f"{user}:{token}", "ds": "sgppblhtsonde1mcfarlC1.c1",
                             "start": "2026-09-17", "end": "2026-09-17", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgppblhtsonde1mcfarlC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgppblhtsonde1mcfarlC1.c1", "2026-09-17", "2026-09-17")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgppblhtsonde1mcfarlC1.c1", "2026-09-17", "2026-09-17"))   # cite what you pulled
```
### First look

Plotted through xarray: the field's layout defeats ACT's 2-D path.

```python
import matplotlib.pyplot as plt

# Plotted through xarray rather than ACT: this field is not time-major, or its
# second dimension has a non-numeric coordinate, either of which sends ACT's
# 2-D path into a dtype error.
fig, ax = plt.subplots(figsize=(10, 4))
ds["air_temp"].plot(x="time", ax=ax)
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```

## Quality control in this product

5 `qc_` companion variables cover 5 of the
33 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_pbl_height_heffter"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("pbl_height_heffter", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["pbl_height_heffter", "pbl_regime_type_liu_liang", "pbl_height_liu_liang"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgppblhtsonde1mcfarlC1.c1.20260917.185609.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `pbl_height_heffter` | Normally calculated PBL height was greater than  4 km or... | 1 | 100.0 |
| `level_1_liu_liang` | neutral_boundary_layer | 1 | 100.0 |
| `level_2_liu_liang` | neutral_boundary_layer | 1 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgppblhtsonde1mcfarlC1.c1", "20010401", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Radiosonde pre-processing performs whole-sonde QC checks (data count, altitude, pressure, temperature jump/extremes, missing pressure) that reject an entire sonde if failed, producing no PBL estimates. Passing sondes still have individual point-level QC against valid min/max criteria, with failing values set missing and qc flags set (no interpolation/fill). Near-surface (less than 50 m AGL) wind speeds greater than 33.5 m/s are treated as missing. Output PBL heights carry per-method qc flags (qc_pbl_height_heffter, qc_pbl_height_liu_liang, qc_pbl_height_bulk_richardson_pt25/pt5,...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Whole-sonde rejection due to failed pre-processing QC | No PBL height estimates produced for that sonde launch; missing record in daily/yearly output | Radiosonde is labeled bad and excluded if any of: less than 1 data points, max altitude less than 1000 m, max pressure less than =200 hPa,... | (hb p. 7) |
| Individual bad/missing sonde data points | Missing values in individual variables within an otherwise valid sonde file; qc flags set | Values failing valid min/max criteria set to missing and qc flags set; no interpolation or fill performed over bad points | (hb p. 8) |
| No independent 'truth' for PBL height / subjective definition | Different methods (Heffter, Liu-Liang, bulk Richardson) disagree, sometimes substantially, for the same sounding | Multiple methods implemented; spread between methods used as a partial uncertainty estimate; users must use judgment on which estimate is appropriate | (hb p. 6) |
| Liu-Liang PBL height undetermined (CBL/NRL) | Value of -9999 reported for pbl_height_liu_liang | Reported as -9999 when criteria in Eq 5/6 not met | (hb p. 9) |
| Liu-Liang PBL height undetermined (SBL) | Value of -9999 reported for pbl_height_liu_liang when neither stability nor wind-shear criteria found | Reported as -9999 | (hb p. 10) |
| Liu-Liang or bulk Richardson PBL height exceeding 4 km AGL | PBL height flagged bad and set to -9999 | QC flag set to bad, value replaced with -9999 | (hb p. 13) |
| Heffter PBL height indeterminate / inversion greater than 4 km AGL or no layer meets 2K... | PBL height set to height of maximum potential temperature gradient rather than the 2K-difference criterion; QC flag set to indeterminate | Falls back to inversion layer with largest max potential temperature gradient below 4 km; flagged indeterminate | (hb p. 11) |
| Criteria not met for any method (Table 1 thresholds, Heffter lapse rate/difference... | PBL height flagged bad and set to -9999 for that method | Flag as bad, set to -9999 | (hb p. 13) |
| Noisy near-surface sonde readings | Spurious shallow layers/height estimates near the surface | Liu-Liang searches restricted to above 150 m AGL; 5 mb pressure subsampling and (for Heffter) 15 mb smoothing applied to reduce identification of... | (hb p. 8) |
| Erroneously high near-surface wind speeds | Wind speed values below 50 m AGL exceeding 33.5 m/s | Windspeed data in that region treated as missing if threshold exceeded | (hb p. 13) |
| Island site land/ocean classification uncertainty | PBL height regime/threshold behavior at Nauru, Manus, Azores, Gan may not reflect true surface forcing if island heating drives PBL depth | Currently classified as oceanic; further analysis flagged as needed | (hb p. 9) |
| Outlier disagreement between VAP Liu-Liang and independent Dr. Liu implementation | Mean absolute difference 137 m, median absolute difference 61 m, correlation 0.86 for April 2004 SGP; larger outliers mainly in SBL regime | Attributed to differences in pre-processing/subsampling; further analysis planned | (hb p. 15) |
| Outlier disagreement between VAP Heffter and independent Dr. Fischer implementation | Mean absolute difference 288 m, median absolute difference 29 m, correlation 0.66 overall (0.44 under neutral conditions); VAP tends to produce higher PBL heights under... | Attributed to automated selection of a higher inversion layer than manual implementation; further analysis planned | (hb p. 15) |
| Systematic differences between intra-VAP methods | Heffter method tends to produce higher PBL heights than Liu-Liang (corr 0.69, mean/median abs diff 440/185 m) and than bulk Richardson (corr 0.71, mean/median abs diff 407/124 m); bulk... | No correction applied; documented as expected inter-method variability | (hb p. 15) |
| Sensitivity of bulk Richardson PBL height to critical threshold choice | Raising bulk Richardson critical threshold from 0.25 to 0.5 uniformly raises estimated PBL heights and shifts mean/median absolute differences versus other methods (e.g., 394/165 m vs... | Both 0.25 and 0.5 threshold outputs provided due to literature ambiguity on appropriate critical value | (hb p. 13) |
| Bulk Richardson method performance limited to certain conditions | Method known to perform best only for SBLs with low wind speeds; potential inaccuracy otherwise | Vogelezang and Holtslag (1996) surface-friction modification suggested but not implemented in current VAP version | (hb p. 13) |
| No gap-filling for missing/failed sonde launches in yearly files | Yearly time series shows gaps rather than interpolated/filled values | Yearly file process explicitly does not fill in gaps due to missing or failed sonde launches | (hb p. 15) |
| No bad-point interpolation | Individual missing/bad sonde values remain as missing in output rather than being interpolated | Handbook states bad sonde points are not filled in or interpolated over at this time | (hb p. 13) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Heffter JL. 1980. Transport Layer Depth Calculations.
- Liu S and XZ Liang. 2010. Observed Diurnal Cycle Climatology of Planetary Boundary Layer Height. Journal of Climate 23:5790-5807.
- Seibert P, F Beyrich, SE Gryning, S Joffre, A Rasmussen, and P Tercier. 2000. Review and Intercomparison of Operational Methods for the Determination of the Mixing Height. Atmospheric Environment 34(7):1001-1027.
- Sorensen JH, A Rasmussen, T Ellermann, and E Lyck. 1998. Mesoscale Influence on Long-range Transport - Evidence From ETEX Modeling and Observations. Atmospheric Environment 32(24):4207-4217.
- Vogelezang DHP and AAM Holtslag. 1996. Evolution and Model Impacts of Alternative Boundary Layer Formulations. Boundary Layer Meteorology 81:245-269.
- Stull RB 1988.
- Curry JA and PJ Webster 1999.
- Delle Monache L, KD Perry, RT Cederwall, and JA Ogren. 2004. In situ Aerosol Profiles Over the Southern Great Plains Cloud and Radiation Test Bed Site: 2. Effects of Mixing Height on Aerosol Properties. JGR 109:D06209.
- Marsik FJ, KW Fischer, TD McDonald, and PJ Samson. 1995. Comparison of Methods for Estimating Mixing Height Used During the 1992 Atlanta Field Intensive. Journal of Applied Meteorology 34(8):1802-1814.
- Snyder BJ and KB Strawbridge. 2004. Meteorological Analysis of the Pacific 2001 Air Quality Field Study. Atmospheric Environment 38:5733-5743.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-132.pdf (36 pages, DOE/SC-ARM/TR-132, by C Sivaraman, S McFarlane, E Chapman, M Jensen, T Toto, S Liu, M Fischer)
- Catalog record: ARM data-source index, `instrument_class_code=pblht`, read 2026-09-24
- Example file: `sgppblhtsonde1mcfarlC1.c1.20260917.185609.nc` from `sgppblhtsonde1mcfarlC1.c1`, 0.19 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
