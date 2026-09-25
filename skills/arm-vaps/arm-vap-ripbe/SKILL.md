---
name: arm-vap-ripbe
description: ARM Radiatively Important Parameters Best Estimate (ripbe) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (temperature, pressure, water vapor mixing ratio, relative humidity, air density, cloud liquid water path), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpripbe1mcfarlaneC1.c1) and the variable inventory of a real file. Use when working with ripbe data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Cloud Properties; Derived Quantities and Models; Radiometric. Triggers - ripbe, Radiatively Important Parameters Best Estimate, sgpripbe1mcfarlaneC1.c1, temperature, pressure, water vapor mixing ratio, relative humidity, air density, Aerosols.
---

# RIPBE - Radiatively Important Parameters Best Estimate

RIPBE is an ARM value-added product that combines multiple ARM instrument/VAP datastreams (cloud, temperature/humidity, aerosol, gas, surface albedo, surface radiating temperature, and measured fluxes) onto a uniform vertical and temporal grid at the SGP site to serve as a complete input data set for radiative transfer model calculations.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 27 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ripbe` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-097 / S McFarlane, T Shippert, J Mather / June 2011](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-097.pdf) |
| Category | Aerosols; Cloud Properties; Derived Quantities and Models; Radiometric |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2002-03-01 to 2011-06-05 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ripbe |


## Credit

Everything this skill knows about the retrieval is the work of **S McFarlane, T Shippert, J Mather** -
the ARM developers and mentors who wrote the technical report it derives from:

> S McFarlane, T Shippert, J Mather. *Radiatively Important Parameters Best Estimate (RIPBE): An ARM Value-Added Product*, DOE/SC-ARM-TR-097, June 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-097.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

RIPBE does not measure a physical quantity directly with a sensor; instead it is a data-fusion VAP that grids and interpolates radiatively important parameters (water vapor, ozone, temperature profiles, surface albedo, aerosol properties, cloud properties) from multiple ARM instrument datastreams and VAPs onto a common height/time grid for use as input to radiative transfer models such as RRTM. The procedure first sub-samples or interpolates each input profile in time then interpolates in height, filling missing/bad data where possible, with cloud properties treated as critical inputs that are never interpolated over due to their high variability and radiative impact. For non-cloud variables, if gridded data remain bad, they are replaced with secondary datastreams, climatology, or fixed values, with source flags tracking the origin of each value. Bit-packed qc flags mark test failures (critical failures replace data with -9999; non-critical failures flag issues like interpolation) and a 1D 'aqc_summary' flag reduces the 2D qc information to a single good/indeterminate/bad value per time column.

**Cadence.** input rate varies by input datastream (e.g., 1-min surface fluxes, MERGESONDE soundings, MICROBASE layers); output every 1-min time resolution; time stamps represent the center of the time bin, every minute on the half minute; averaging monthly climatological values calculated in pre-processing from existing data at the site; a 1-hour averaged RIPBE file and a 30-min averaged file are planned as future products (hb p. 12).

## Inputs

The report names these instruments and sibling products: MERGESONDE, MICROBASE, AEROSOLBE, SURFSPECALB, SWFLUXANAL, BBHRP, CMBE, QCRad, IRT (irt10mC1.b1), MFRSR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| temperature | K | - | - | (hb p. 23) |
| pressure | hPa | - | - | (hb p. 23) |
| water vapor mixing ratio | kg/kg | - | - | (hb p. 23) |
| relative humidity | % | - | - | (hb p. 23) |
| air density | g/m3 | - | - | (hb p. 24) |
| cloud liquid water path (cld_lwp) | g/m2 | - | - | (hb p. 24) |
| cloud ice water path (cld_iwp) | g/m2 | - | - | (hb p. 24) |
| cloud liquid effective radius (cld_reliq) | um | - | - | (hb p. 24) |
| cloud generalized ice effective diameter (cld_dgeice) | um | - | - | (hb p. 24) |
| aerosol Angstrom parameter | unitless | - | - | (hb p. 24) |
| aerosol optical depth at 500 nm (AOD_500) | unitless | - | - | (hb p. 24) |
| aerosol extinction at 500 nm | km-1 | - | - | (hb p. 24) |
| aerosol single scattering albedo at 500 nm | unitless | - | - | (hb p. 24) |
| aerosol asymmetry parameter at 500 nm | unitless | - | - | (hb p. 24) |
| ozone volume mixing ratio | ppmv | - | - | (hb p. 24) |
| total column ozone | DU | - | - | (hb p. 24) |
| surface albedo (RRTM, Fu-Liou, GCM2, Edwards-Slingo bands) | unitless | - | - | (hb p. 25) |
| CO2, CH4, N2O, CCl4, CFC11, CFC12 mixing ratios | ppmv | - | - | (hb p. 25) |
| surface radiating temperature | K | - | - | (hb p. 25) |
| measured longwave/shortwave surface fluxes... | W/m2 | - | - | (hb p. 25) |
| solar zenith angle | degrees | - | - | (hb p. 23) |
| solar distance factor | unitless | - | - | (hb p. 23) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Standard time grid | every minute on the half minute | (hb p. 2) |
| Height grid extent | extends to 68 km | (hb p. 2) |
| Cloud sub-sampling time interval | 30 seconds | (hb p. 3) |
| Non-cloud variable sub-sampling/interpolation time interval | 30 minutes | (hb p. 3) |
| Height interpolation limit (non-cloud) | within 20 km of target point (basically no limit) | (hb p. 3) |
| Extrapolation limit | up to half a bin beyond the min/max input height values | (hb p. 3) |
| MICROBASE layer depth | fixed at 45 m | (hb p. 5) |
| SURFSPECALB cutoff | cosine of solar zenith angle less than  0.15 produces no values | (hb p. 11) |
| Nighttime albedo fill exclusion | solar zenith angle greater than = 86 degrees not filled | (hb p. 11) |
| Output file time resolution | 1-min time resolution | (hb p. 12) |
| Output file naming convention | SSSripbe1mcfarlane.c1.YYYYMMDD.hhmmss | (hb p. 12) |
| Source flag range - observed | 0-19 Observed variable | (hb p. 4) |
| Source flag range - climatological | 20-29 Climatological value based on ARM observations at given site | (hb p. 4) |
| Source flag range - model derived | 30-39 Value derived from model values or climatology not based on site observations | (hb p. 4) |
| Source flag - out of range | 50 Data outside of measurement range or detection limit | (hb p. 4) |
| MERGESONDE v2 vertical extent | up to 60 km | (hb p. 7) |
| MERGESONDE v1 vertical extent | up to ~20 km | (hb p. 7) |


## The data

Verified example: **`sgpripbe1mcfarlaneC1.c1`**, file `sgpripbe1mcfarlaneC1.c1.20110603.000030.cdf`
(196.1 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `level`=628, `layer`=627, `rrtm_band`=14, `fu_liou_band`=6, `gcm2_band`=2, `edwards_slingo_band`=5 |
| Data variables | 172 |
| QC variables | 39 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2011-06-03T00:00:30 to 2011-06-03T23:59:30 |
| dod version | ripbe1mcfarlane-c1-0.2 |
| process version | $ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `aerosol_angstrom` | unitless | time | yes | Aerosol angstrom parameter |
| `aerosol_aod_500` | unitless | time | yes | Aerosol optical depth at 500nm |
| `aerosol_ext_500` | km-1 | time,layer | yes | Aerosol extinction profile at 500 nm |
| `aerosol_g_500` | unitless | time,layer | yes | Aerosol asymmetry parameter at 500nm |
| `aerosol_ssa_500` | unitless | time,layer | yes | Aerosol single scattering albedo at 500 nm |
| `airdensity_layer` | g/m3 | time,layer | yes | Density of air at each layer |
| `airdensity_level` | g/m3 | time,level | yes | Density of air at each level |
| `ccl4_mr` | ppmv | time | yes | Volume mixing ratio for CCL4 |
| `ch4_mr` | ppmv | time | yes | Volume mixing ratio for CH4 |
| `cld_dgeice` | um | time,layer | yes | Cloud generalized ice effective diameter (Fu) in layer |
| `cld_iwp` | g/m2 | time,layer | yes | Cloud ice water path across layer |
| `cld_lwp` | g/m2 | time,layer | yes | Cloud liquid water path across layer |
| `cld_reliq` | um | time,layer | yes | Cloud liquid effective radius in each layer |
| `clear_sky_flag` | unitless | time | yes | Clear sky flag from shortwave flux analysis (swfanal) |
| `co2_mr` | ppmv | time | yes | Volume mixing ratio for CO2; assumed constant with height |
| `column_ozone` | DU | time | yes | Total column ozone |
| `f11_mr` | ppmv | time | yes | Volume mixing ratio for CFC11 |
| `f12_mr` | ppmv | time | yes | Volume mixing ratio for CFC12 |
| `meas_down_long_hemisp` | W/m2 | time | yes | Measured longwave flux at surface |
| `meas_down_short_diffuse_hemisp` | W/m2 | time | yes | Measured shortwave diffuse flux at surface |
| `meas_down_short_hemisp` | W/m2 | time | yes | Measure shortwave total flux at surface |
| `meas_short_direct_normal` | W/m2 | time | yes | Measured shortwave direct normal flux at surface |
| `meas_up_long_hemisp` | W/m2 | time | yes | Measured upwelling longwave flux at surface |
| `n2o_mr` | ppmv | time | yes | Volume mixing ratio for N2O |
| `ozone_mr` | ppmv | time,level | yes | Ozone volume mixing ratio at level heights |
| `precip` | mm | time | yes | Total precipitation |
| `pressure_layer` | hPa | time,layer | yes | Pressure at midpoint of each layer |
| `pressure_level` | hPa | time,level | yes | Pressure at each level |
| `surface_albedo_edwards_slingo` | unitless | time,edwards_slingo_band | yes | Surface albedo in edwards_slingo wavenumber bands |
| `surface_albedo_fu_liou` | unitless | time,fu_liou_band | yes | Surface albedo in fu_liou wavenumber bands |


_101 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpripbe1mcfarlaneC1.c1",
                             "start": "2011-06-03", "end": "2011-06-03", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpripbe1mcfarlaneC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpripbe1mcfarlaneC1.c1", "2011-06-03", "2011-06-03")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpripbe1mcfarlaneC1.c1", "2011-06-03", "2011-06-03"))   # cite what you pulled
```

This product carries 172 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpripbe1mcfarlaneC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['aerosol_angstrom', 'aerosol_aod_500', 'aerosol_ext_500', 'qc_aerosol_angstrom', 'qc_aerosol_aod_500', 'qc_aerosol_ext_500'],
                                cleanup_qc=True)
```

## Quality control in this product

39 `qc_` companion variables cover 39 of the
172 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_clear_sky_flag"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("clear_sky_flag", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["clear_sky_flag", "pressure_level", "pressure_layer"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpripbe1mcfarlaneC1.c1.20110603.000030.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `surface_albedo_fu_liou` | Input data flagged as indeterminate, and used | 4962 | 57.4306 |
| `surface_albedo_edwards_slingo` | Input data flagged as indeterminate, and used | 4135 | 57.4306 |
| `surface_albedo_gcm2` | Input data flagged as indeterminate, and used | 1654 | 57.4306 |
| `surface_albedo_rrtm` | Input data flagged as indeterminate, and used | 10751 | 53.3284 |
| `surface_albedo_rrtm` | Input data included bad values in integration range; bad values... | 8582 | 42.5694 |
| `surface_albedo_edwards_slingo` | All input values bad for grid value | 3065 | 42.5694 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpripbe1mcfarlaneC1.c1", "20020301", "20260924")
```

The report's own note on quality: RIPBE includes bit-packed qc values for each output variable; each bit corresponds to a test, and if the test fails the bit is set (qc=0 means no tests failed). Tests are critical or non-critical: critical test failures mean data are 'bad' and are replaced with -9999, while non-critical failures flag issues (e.g., interpolation) for user awareness without removing data. Cloud variables are not interpolated over, so failing min/max or other qc checks flags them as bad rather than replacing them. QC bit descriptions are stored as global attributes, though some fields have additional...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Cloud properties not interpolated/filled | Missing or bad cloud values remain flagged as bad (not interpolated over); iwp/lwc/iwc show gaps or -9999 rather than smoothed/climatological fill | Cloud parameters are designated critical inputs; missing/bad values are indicated as such and not interpolated or replaced with climatology | (hb p. 7) |
| Cloud edge indeterminate values | Numerous cyan qc bit=7 values at the lower edge of cloud in iwp quicklook plots, causing 1D summary aqc flag to be 'indeterminate' for much of the day | None specified beyond flagging as indeterminate; likely due to valid_min/valid_max failures from cloud edge effects | (hb p. 11) |
| Cloud/aerosol grid points outside sensor detection range | Cloud or aerosol variables set to 0 with source flag = 50 at heights outside range of remote sensors/AEROSOLBE product | Values set to 0 and flagged with source flag 50 to indicate no information known | (hb p. 5) |
| Relative humidity supersaturation clipping | RH values in input data above 100% are set to 100% in gridding/interpolation, visible as white patches in RH quicklook and qc bit=13 set; summary qc flags RH/water vapor as indeterminate at... | Field-specific qc bit (13) flags these clipped values so users are aware | (hb p. 7) |
| Small negative aerosol extinction values | Aerosol extinction profile occasionally contains small negative values (less than  -0.01) | These are set to 0 and source flag modified to indicate the change; values still considered 'good' | (hb p. 9) |
| Missing/near-zero aerosol extinction, SSA, or asymmetry parameter at profile top | Small values of extinction and/or -9999 reported near top of AEROSOLBE profile; qc bit 4 (gold points, 'Data interpolated while gridding') or qc bit 6 (hot pink points, 'Not using closest... | Gridder interpolates over missing values or uses closest good value up to 30 minutes away; if gap too large, monthly climatological SSA/g values... | (hb p. 9) |
| MERGESONDE version limitation / grid top extrapolation | Above 60 km (v2) or ~20 km (v1) values are extrapolated or filled from standard atmosphere; potential discontinuity/jump at top of MERGESONDE input grid when v1 used | Values extrapolated from 60 to 68 km for v2; standard atmosphere used above ~20 km for v1, with a smoothing procedure implemented to avoid large... | (hb p. 7) |
| MERGESONDE missing/bad data | Entire temperature/humidity/pressure/density profile shows climatological values instead of sounding-derived data, flagged via source flag | Entire profile replaced with monthly climatological profile (based on existing MERGESONDE data) to avoid height discontinuities | (hb p. 7) |
| Surface radiating temperature unavailable | surface_rad_temp = -9999 when neither IRT nor pyrgeometer-derived estimate is available | Preferred source is IRT (irt10mC1.b1); if unavailable/bad, calculated from measured longwave upwelling assuming emissivity=1.0; if both unavailable,... | (hb p. 11) |
| Pyrgeometer-based surface radiating temperature bias | Surface radiative temperature biased on warm days when derived from upwelling longwave measured by pyrgeometer | Pyrgeometer reacts strongly to air temperature causing bias; future versions will preferentially use downward-looking IRT with additional backup... | (hb p. 12) |
| Measured surface fluxes and clear-sky flag not filled when missing/bad | meas_down_long_hemisp, meas_down_short_hemisp, etc., and flag_clearsky_detection show -9999 rather than interpolated/climatological values | These fields (measured radiative fluxes, clear sky detection flag) are exceptions to the fill/climatology replacement process and are simply given... | (hb p. 11) |
| SURFSPECALB unavailable at low sun angle | No surface albedo values produced when cosine of solar zenith angle less than  0.15; gap in surface_albedo_* fields near sunrise/sunset | Interpolated or filled with monthly climatological values, except nighttime data (SZA greater than = 86 deg) which are not filled | (hb p. 11) |
| Spectral discontinuity risk in surface albedo | If albedo at any single wavelength is bad, without correction the spectrum would show discontinuities | If albedo at any wavelength is bad, the entire shortwave spectrum is replaced with climatological value to avoid spectral discontinuities | (hb p. 11) |
| CO2 data set temporal limitation | CO2 mixing ratio values after 2008 are extrapolated rather than directly observed | Extrapolated using an algorithm developed by Dave Turner that includes annual increases and seasonal variability (predict_co2.pro); requires yearly... | (hb p. 9) |
| Trace gases fixed at constant values | CH4, N2O, CCl4, CFC11, CFC12 mixing ratios show no time variation despite being nominally time-varying fields, since currently set at fixed values for all times | None specified; assumes well-mixed gases | (hb p. 9) |
| Ozone profile not scaled when satellite data unavailable | column_ozone / ozone_mr reflect unscaled default/standard BBHRP ozone profile rather than satellite-observed values on days without TOMS/OMI coverage | If TOMS/OMI values are not available, the ozone profile is not scaled | (hb p. 9) |
| Hard-coded/site-specific layering | Height/layer grid definitions are currently fixed based on site and MICROBASE file rather than dynamically generated | For the testbed, layering will be modified to be developed automatically from an input cloud file | (hb p. 2) |
| Single-site limitation | RIPBE output only exists for SGP; datastreams like SURFSPECALB and AEROSOLBE not available at other ARM sites | Extension to other sites planned depending on resource availability; alternative aerosol/albedo estimation approaches under consideration | (hb p. 13) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Clough, SA, MW Shephard, E Mlawer, JS Delamere, M Iacono, K Cady-Pereira, S Boukabara, PD Brown. 2005. 'Atmospheric radiative transfer modeling: A summary of the AER codes.' Journal of Quantitative Spectroscopy and...
- Edwards, JM and A Slingo. 1996. 'Studies with a flexible new radiation code. Part 1: Choosing a configuration for a large-scale model.' Quarterly Journal of the Royal Meteorological Society 122: 689-719.
- Fu, Q and KN Liou. 1992. 'On the correlated k-distribution method for radiative transfer in nonhomogeneous atmospheres.' Journal of the Atmospheric Sciences 49: 2139-2156.
- Fu, Q. 1996. 'An accurate parameterization of the solar radiative properties of cirrus clouds for climate models.' Journal of Climate 9: 2058-2082.
- Gaustad, K, SA McFarlane, CN Long, and E Mlawer. 2011. Spectral Surface Albedo Value-Added Product. DOE/SC-ARM/TR-096, in preparation.
- Long, CN and Y Shi. 2006. The QCRad Value Added Product: Surface Radiation Measurement Quality Control Testing, Including Climatology Configurable Limits. DOE/SC-ARM/TR-074.
- Long, CN and K Gaustad. 2004. The Shortwave (SW) Clear-Sky Detection and Fitting Algorithm: Algorithm Operational Details and Explanations. DOE/SC-ARM/TR-004.1.
- Sivaraman, C, DD Turner, and CJ Flynn. 2006. ABE - Aerosol Best Estimate Value Added Product: Algorithm Operational Details and Explanations.
- Troyan, D. 2010. Merged Sounding Value Added Product. DOE/SC-ARM/TR-087.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-097.pdf (27 pages, DOE/SC-ARM-TR-097, by S McFarlane, T Shippert, J Mather)
- Catalog record: ARM data-source index, `instrument_class_code=ripbe`, read 2026-09-24
- Example file: `sgpripbe1mcfarlaneC1.c1.20110603.000030.cdf` from `sgpripbe1mcfarlaneC1.c1`, 196.1 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
