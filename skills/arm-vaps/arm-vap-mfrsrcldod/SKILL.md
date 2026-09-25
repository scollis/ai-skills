---
name: arm-vap-mfrsrcldod
description: ARM Cloud Optical Properties from MFRSR Using Min Algorithm (mfrsrcldod) - value-added product reference from its technical report. Derived from mfrsr. The retrieval algorithm, reported quantities (Cloud optical depth, Cloud effective radius, Liquid water path), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmfrsrcldod1minC1.c1) and the variable inventory of a real file. Use when working with mfrsrcldod data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Radiometric. Triggers - mfrsrcldod, Cloud Optical Properties from MFRSR Using Min Algorithm, sgpmfrsrcldod1minC1.c1, mfrsr VAP, Cloud optical depth, Cloud effective radius, Liquid water path, Aerosols, Radiometric.
---

# MFRSRCLDOD - Cloud Optical Properties from MFRSR Using Min Algorithm

MFRSRCLDOD is an ARM value-added product that retrieves cloud optical depth and, when MWR liquid water path is available, effective radius of warm liquid-water clouds from diffuse transmission at 415 nm measured by a surface-based Multifilter Rotating Shadowband Radiometer.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 23 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mfrsrcldod` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-047 / DD Turner, C Lo, Q Min, D Zhang, K Gaustad / July 2021](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-047.pdf) |
| Category | Aerosols; Radiometric |
| Input instruments | `mfrsr` |
| Record | 1997-01-09 to 2026-09-24 (retired) |
| Datastreams with data | 51 across 17 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mfrsrcldod |


## Credit

Everything this skill knows about the retrieval is the work of **DD Turner, C Lo, Q Min, D Zhang, K Gaustad** -
the ARM developers and mentors who wrote the technical report it derives from:

> DD Turner, C Lo, Q Min, D Zhang, K Gaustad. *Cloud Optical Properties from the Multifilter Shadowband Radiometer (MFRSRCLDOD): An ARM Value-Added Product*, DOE/SC-ARM-TR-047, July 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-047.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP applies the Min and Harrison (1996) Nonlinear Least Squares retrieval algorithm to the atmospheric transmittance at 415 nm, computed as the ratio of observed irradiance (I) from the MFRSR to a top-of-atmosphere irradiance (I0) derived from Langley regressions on nearby clear days. The algorithm parameterizes scattering properties at 415 nm as a function of effective radius and liquid water path using Mie theory, and uses an adjoint formulation of radiative transfer for accuracy and speed. It iteratively retrieves both cloud optical depth and effective radius when an LWP estimate from a microwave radiometer is provided; otherwise it assumes an effective radius of 8.0 microns and returns only optical depth. Because both I and I0 come from the same MFRSR, absolute calibration of the instrument is not required to obtain accurate transmittance, and the wavelength 415 nm is chosen for its lack of gaseous absorption and relatively constant surface albedo.

**Cadence.** input rate 20 s (MFRSR irradiance); output every 20 s output file; averaging 5-minute running average also provided, centered on output sample time; ancillary inputs interpolated to 20 s, LWP interpolated across gaps up to 5 min (hb p. 9).

## Inputs

ARM's catalog declares these input instrument classes: `mfrsr`.

The report names these instruments and sibling products: MFRSR, MWR, MWRRET, ARSCL, Shortwave Flux VAP, Surface Spectral Albedo VAP, Total Sky Imager, Langley VAP (mfrsrcal/mfrsrlangley).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Cloud optical depth | unitless | valid for optical depths larger... | 1-sigma uncertainty propagated from I, I0,... | (hb p. 6) |
| Cloud effective radius | microns | - | 1-sigma uncertainty propagated from I, I0,... | (hb p. 6) |
| Liquid water path (derived, if no MWR) | mm | - | large due to natural variability in assumed... | (hb p. 10) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Wavelength used for retrieval | 415 nm | (hb p. 6) |
| Optical depth validity threshold | greater than  approximately 7 | (hb p. 6) |
| Default effective radius (no MWR LWP) | 8.0 μm | (hb p. 6) |
| MFRSR irradiance temporal resolution | 20 s | (hb p. 9) |
| Averaged retrieval window | 5 min centered on output sample time | (hb p. 9) |
| Uncertainty in observed irradiance (I) | 1% | (hb p. 10) |
| Surface albedo (non-snow, 415 nm) | 0.036 | (hb p. 10) |
| Surface albedo uncertainty | ±0.01 | (hb p. 10) |
| MWR LWP uncertainty | approximately 20 g m-2 (Westwater et al. 2001) | (hb p. 9) |
| LWP threshold below which MWR LWP not used | 20 g m2 (i.e., below the ~20 g m-2 uncertainty threshold) | (hb p. 9) |
| LWP interpolation gap maximum | 5 min | (hb p. 9) |
| Number of I0 points selected for calibration | 20 closest in time, best 10 of 20 used for mean | (hb p. 4) |
| Langley I0 search window | 3 months before and after processing day | (hb p. 4) |
| MWR brightness temperature rain/cosmic-background QC... | below cosmic background or above 100 K | (hb p. 4) |
| Output file temporal resolution | 20 s data | (hb p. 3) |
| Criteria for valid cloud data used in example analysis | cloud fraction greater than  90%, infrared temperature greater than  268 K (-50°C... note as printed), cloud base height less than  4 km, optical... | (hb p. 12) |


## The data

Verified example: **`sgpmfrsrcldod1minC1.c1`**, file `sgpmfrsrcldod1minC1.c1.20260503.000000.nc`
(1.61 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4320, `n_Io`=181 |
| Data variables | 106 |
| QC variables | 47 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-05-03T00:00:00 to 2026-05-03T23:59:40 |
| dod version | mfrsrcldod1min-c1-3.1 |
| process version | mfrsrcldod1min-3.19.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Io_filter1` | count | n_Io | yes | Solar constant corrected for solar distance for the Direct Narrowband... |
| `Io_filter2` | count | n_Io | yes | Solar constant corrected for solar distance for the Direct Narrowband... |
| `Io_filter3` | count | n_Io | yes | Solar constant corrected for solar distance for the Direct Narrowband... |
| `Io_filter4` | count | n_Io | yes | Solar constant corrected for solar distance for the Direct Narrowband... |
| `Io_filter5` | count | n_Io | yes | Solar constant corrected for solar distance for the Direct Narrowband... |
| `cldtaua_error1` | 1 | time | yes | Average Cloud Tau Error1 (1% uncertainty in total irradiance) |
| `cldtaua_error2` | 1 | time | yes | Average Cloud Tau Error2 (uncertainty is standard deviation of... |
| `cldtaua_error3` | 1 | time | yes | Average Cloud Tau Error3 (uncertainty in liquid water path (lwp)... |
| `cldtaua_error4` | 1 | time | yes | Average Cloud Tau Error4 (uncertainty is 0.01 in surface albedo) |
| `cldtaua_toterror` | 1 | time | yes | Average Cloud Tau Total Uncertainty |
| `cldtaui_error1` | 1 | time | yes | Instantaneous Cloud Tau Error1 (1% uncertainty in total irradiance) |
| `cldtaui_error2` | 1 | time | yes | Instantaneous Cloud Tau Error2 (uncertainty is standard deviation of... |
| `cldtaui_error3` | 1 | time | yes | Instantaneous Cloud Tau Error3 (uncertainty in liquid water path... |
| `cldtaui_error4` | 1 | time | yes | Instantaneous Cloud Tau Error4 (uncertainty is 0.01 in surface albedo) |
| `cldtaui_error5` | 1 | time | yes | Instantaneous Cloud Tau Error5 (uncertainty in 3um higher of... |
| `cldtaui_toterror` | 1 | time | yes | Instantaneous Cloud Tau Total Uncertainty |
| `cloudbasebestestimate` | m | time | yes | LASER Cloud Base Height Best Estimate |
| `cloudfraction` | 1 | time | yes | Estimated Average Fractional Sky Cover over the Hemispheric Dome (cf) |
| `cosine_solar_zenith_angle` | 1 | time | yes | Cosine Solar Zenith Angle |
| `direct_transmittance_filter1` | 1 | time | yes | Direct transmittance of Narrowband Direct Normal Irradiance, Filter 1 |
| `direct_transmittance_filter2` | 1 | time | yes | Direct transmittance of Narrowband Direct Normal Irradiance, Filter 2 |
| `direct_transmittance_filter3` | 1 | time | yes | Direct transmittance of Narrowband Direct Normal Irradiance, Filter 3 |
| `direct_transmittance_filter4` | 1 | time | yes | Direct transmittance of Narrowband Direct Normal Irradiance, Filter 4 |
| `direct_transmittance_filter5` | 1 | time | yes | Direct transmittance of Narrowband Direct Normal Irradiance, Filter 5 |
| `effective_radius_average` | um | time | yes | Five-Minute Running Average of Effective Radius |
| `effective_radius_instantaneous` | um | time | yes | Effective Radius (Instantaneous) |
| `ir_temp` | K | time | yes | IR Brightness Temperature |
| `lwp` | mm | time | yes | Total liquid water along LOS path |
| `lwp_uncertainty` | mm | time | yes | lwp uncertainty if derived from mfrsr.b1 |
| `optical_depth_average` | 1 | time | yes | Five-Minute Running Average of Cloud Optical Depth |


_25 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpmfrsrcldod1minC1.c1",
                             "start": "2026-05-03", "end": "2026-05-03", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmfrsrcldod1minC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmfrsrcldod1minC1.c1", "2026-05-03", "2026-05-03")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmfrsrcldod1minC1.c1", "2026-05-03", "2026-05-03"))   # cite what you pulled
```

This product carries 106 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpmfrsrcldod1minC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['Io_filter1', 'Io_filter2', 'Io_filter3', 'qc_Io_filter1', 'qc_Io_filter2', 'qc_Io_filter3'],
                                cleanup_qc=True)
```

## Quality control in this product

47 `qc_` companion variables cover 47 of the
106 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_optical_depth_instantaneous"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("optical_depth_instantaneous", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["optical_depth_instantaneous", "effective_radius_instantaneous", "optical_depth_average"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpmfrsrcldod1minC1.c1.20260503.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `reffi_error3` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |
| `reffa_error3` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |
| `reffa_error1` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |
| `reffi_toterror` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |
| `reffi_error4` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |
| `reffa_error4` | Error calculation could not be performed, data value set to... | 4320 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmfrsrcldod1minC1.c1", "19970109", "20260924")
```

The report's own note on quality: The VAP applies simple quality control to MWR LWP: brightness temperature below cosmic background or above 100 K (indicative of rain) causes LWP to be rejected; LWP below the ~20 g m-2 MWR retrieval uncertainty threshold is also not used. Output NetCDF includes qc_ fields for essentially every primary and error variable (e.g., qc_optical_depth_instantaneous, qc_effective_radius_instantaneous, qc_lwp, qc_cloudfraction, qc_cloudbasebestestimate, qc_surface_albedo, qc_Io_filter1-5, etc.) plus a lwp_source flag indicating whether LWP came from MWR or from the MFRSR-derived calculation. For...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Validity restricted to overcast, single-layer or multi-layer liquid water clouds only | Retrieved optical depth/effective radius values are unreliable or meaningless outside overcast liquid-cloud scenes; user must screen using cloud fraction, IR temperature, and cloud base... | Use ancillary fields (cloud fraction from shortwave flux VAP, cloud base height from ARSCL VAP, IR brightness temperature) to select proper cases;... | (hb p. 10) |
| Optical depth retrieval only valid above ~7 | Optical depths below approximately 7 fall outside the valid retrieval regime and should not be trusted | Filter data to optical depth greater than  7 as done in example analysis | (hb p. 6) |
| Default effective radius used when MWR LWP unavailable | effective_radius fields pinned exactly at 8.0 microns whenever MWR LWP is missing/bad, and optical depth retrieval loses the slight re-dependence correction | Flag re = 8.00 μm cases and exclude when analyzing genuine effective radius retrievals; a flag in the output indicates whether LWP is from MWR or... | (hb p. 6) |
| MWR brightness temperature contamination (rain or cosmic background anomalies) | LWP values dropped/unused; corresponds to brightness temperature below cosmic background or above 100 K, usually indicative of rain | VAP applies QC to discard LWP from MWR under these conditions and instead runs without LWP input | (hb p. 4) |
| MWR LWP retrieval uncertainty threshold | LWP values below ~20 g m-2 are not used because they are within the MWR retrieval uncertainty, so re retrievals absent in low-LWP conditions | VAP does not use MWR-observed LWP below this threshold; defaults to assumed re = 8 μm | (hb p. 4) |
| LWP interpolation gap limit | For temporal gaps in MWR LWP larger than 5 minutes, retrieval reverts to no-LWP mode (re assumed 8 μm) for affected MFRSR samples | LWP interpolated only across gaps up to 5 min; beyond that gap the retrieval runs without LWP | (hb p. 9) |
| Biases in MWR LWP propagate to effective radius bias | Especially at small optical depths, systematic offsets in MWR LWP produce corresponding biases in retrieved effective radius | None specified beyond awareness; listed as a known caveat | (hb p. 14) |
| Snow/ice covered surface violates constant-albedo assumption | Surface albedo assumption of 0.036 at 415 nm breaks down with snow/ice cover, biasing optical depth and effective radius retrievals | Algorithm assumes non-snow-covered surface; no correction provided for snow/ice conditions | (hb p. 14) |
| I0 (calibration) uncertainty dominates optical depth uncertainty | Total uncertainty in retrieved optical depth tracks closely with the standard deviation of the 10-point mean I0 value shown in the I0 calibration quicklook | I0 uncertainty computed as standard deviation about the mean of the best 10 of 20 nearby Langley points and propagated into total tau uncertainty | (hb p. 10) |
| LWP uncertainty dominates effective radius uncertainty | Effective radius uncertainty plot shows largest contribution from LWP uncertainty term (assumed ~20 g m-2) | None beyond quantifying propagated uncertainty | (hb p. 10) |
| Spatial inhomogeneity of clouds affecting instantaneous diffuse irradiance | 20-s instantaneous retrievals show more scatter/noise than 5-min averaged retrievals due to sensitivity to cloud spatial inhomogeneities | Use the 5-min averaged retrieval product, which is less sensitive to spatial inhomogeneities | (hb p. 9) |
| Derived LWP (when MWR unavailable) has large uncertainty | LWP estimated via LWP=(2/3)ρτre at MWR-less sites shows large scatter/uncertainty due to natural variability in assumed re | A flag in the output file indicates whether LWP is from MWR or from this calculation; user should treat calculated LWP with caution | (hb p. 10) |
| Missing/bad LWP source fallback chain | LWP source variable (lwp_source flag) changes among be_lwp, phys_lwp, stat2_lwp, or default depending on data quality/availability, so effective radius provenance is inconsistent across... | VAP preference order: be_lwp, then phys_lwp if good/indeterminate, then stat2_lwp if good/indeterminate, then default re=8.0 μm if all missing/bad | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `mfrsr`: load `arm-instrument-mfrsr` for its handbook facts and artifacts

### References the report cites

- Clothiaux, EE, MA Miller, RC Perez, DD Turner, et al. 2001. The ARM millimeter wave cloud radars (MMCRs) and the active remote sensing of clouds (ARSCL) Value Added Product (VAP). ARM VAP-002-1.
- Harrison, LC, JJ Michalsky, and J Berndt. 1994. Automated multi-filter rotating shadowband radiometer: an instrument for optical depth and radiation measurements. Applied Optics 33(22): 5118-5125.
- Long, CN, and KL Gaustad. 2004. The shortwave (SW) clear-sky detection and fitting algorithm. DOE/SC-ARM-TR-004-1.
- Michalsky, JJ, JA Schlemmer, WE Berkheiser, et al. 2001. Multiyear measurements of aerosol optical depth in the ARM and Quantitative Links programs. JGR-Atmospheres 106(D11): 12099-12107.
- Min, Q, and LC Harrison. 1996. Cloud properties derived from surface MFRSR measurements and comparison with GOES results at the ARM SGP site. Geophysical Research Letters 23(13):1641-1644.
- Min, Q, M Duan, and R Marchand. 2003. Validation of surface retrieved cloud optical properties with in situ measurements at the ARM SGP site. JGR-Atmospheres 108(D17): 4547.
- Westwater, ER, Y Han, MD Shupe, and SY Matrosov. 2001. Analysis of integrated cloud liquid and precipitable water vapor retrievals from MWRs during SHEBA. JGR-Atmospheres 106(D23): 32,019-32,030.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-047.pdf (23 pages, DOE/SC-ARM-TR-047, by DD Turner, C Lo, Q Min, D Zhang, K Gaustad)
- Catalog record: ARM data-source index, `instrument_class_code=mfrsrcldod`, read 2026-09-24
- Example file: `sgpmfrsrcldod1minC1.c1.20260503.000000.nc` from `sgpmfrsrcldod1minC1.c1`, 1.61 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
