---
name: arm-vap-aeriprof
description: ARM AERI Profiles of Water Vapor and Temperature (aeriprof) - value-added product reference from its technical report. Derived from aeri. The retrieval algorithm, reported quantities (Temperature profile, Water vapor mixing ratio profile, Precipitable water vapor), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaeriprof3feltzC1.c1) and the variable inventory of a real file. Use when working with aeriprof data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models; Radiometric. Triggers - aeriprof, AERI Profiles of Water Vapor and Temperature, sgpaeriprof3feltzC1.c1, aeri VAP, Temperature profile, Water vapor mixing ratio profile, Precipitable water vapor, Derived Quantities and Models, Radiometric.
---

# AERIPROF - AERI Profiles of Water Vapor and Temperature

The AERIPROF VAP retrieves vertical profiles of temperature and water vapor mixing ratio in the lower-to-mid troposphere from ground-based AERI infrared radiance observations, using RUC model data as an upper-air first guess, and is run operationally at ARM sites such as SGP, NSA, and TWP.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 35 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aeriprof` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-066.1 / W.F. Feltz, D.D. Turner, H.B. Howell, W.L. Smith, R.O. Knuteson, H.M. Woolf, J. Comstock, C. Sivaraman, R. Mahon, T. Halter / April 2007](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-066.1.pdf) |
| Category | Derived Quantities and Models; Radiometric |
| Input instruments | `aeri` |
| Record | 1996-06-14 to 2025-06-28 (retired) |
| Datastreams with data | 15 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aeriprof |


## Credit

Everything this skill knows about the retrieval is the work of **W.F. Feltz, D.D. Turner, H.B. Howell, W.L. Smith, R.O. Knuteson, H.M. Woolf, J. Comstock, C. Sivaraman, R. Mahon, T. Halter** -
the ARM developers and mentors who wrote the technical report it derives from:

> W.F. Feltz, D.D. Turner, H.B. Howell, W.L. Smith, R.O. Knuteson, H.M. Woolf, J. Comstock, C. Sivaraman, R. Mahon, T. Halter. *Retrieving Temperature and Moisture Profiles from AERI Radiance Observations: AERIPROF Value-Added Product Technical Description*, DOE/SC-ARM/TR-066.1, April 2007.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-066.1.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

AERIPROF uses a physical retrieval approach in which downwelling infrared radiance is computed from an assumed atmospheric temperature/moisture (T/q) state using a fast radiative transfer forward model (a variant of RTTOV built from LBLRTM/FASCODE line-by-line calculations), and the computed radiance is compared to the AERI-observed radiance. Differences between observed and calculated radiance are propagated backward using an 'onion-peeling' technique to adjust the T/q profile starting at the surface and progressing upward, iterating until the residual meets a convergence threshold. Only spectral regions near the CO2 absorption bands (15 micron and 4 micron) are used for temperature, and spectral regions on the wings of water vapor absorption bands are used for moisture, because these regions carry the most vertical structure information with least interference. A first-guess profile (statistical retrieval from AERI radiance, blended with RUC model or GOES retrievals) is required to constrain this otherwise ill-posed inversion, since information content decreases with height and the AERI-only weighting functions peak near the surface.

**Cadence.** input rate per AERI radiance sample/record (AERI scene-view duration 195.03 seconds); output every algorithm processes one day at a time, producing profiles per AERI sample; averaging First-guess profile smoothed with up to 100 smoothing passes between 1000-600 mb; RUC model profiles computed hourly and used as background/first-guess above boundary layer (hb p. 13).

## Inputs

ARM's catalog declares these input instrument classes: `aeri`.

The report names these instruments and sibling products: AERI (Atmospheric Emitted Radiance Interferometer), RUC (Rapid Update Cycle numerical weather prediction model), GOES sounder retrievals, Microwave Radiometer (MWR), Vaisala ceilometer, Micropulse lidar (MPL), Belfort laser ceilometer, Raman lidar, Radiosonde (balloon-borne sonde), LSSONDE VAP, Best Estimate atmospheric state VAP.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Temperature profile | K (implied) | surface to ~14 km (RUC-blended);... | RMS differences less than 1,000 in the first... | (hb p. 10) |
| Water vapor mixing ratio profile | - | surface to ~14 km (RUC-blended);... | agreement within 5% RMS vs MWR-scaled... | (hb p. 10) |
| Precipitable water vapor (PWV) derived from retrieved q... | cm | - | - | (hb p. 11) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| AERI channel 1 spectral range | 500-1800 cm-1 | (hb p. 17) |
| AERI channel 2 spectral range | 1800-3000 cm-1 | (hb p. 17) |
| TempSpectralRegion(1) | 612 618 cm-1 | (hb p. 28) |
| TempSpectralRegion(2) | 624 660 cm-1 | (hb p. 28) |
| TempSpectralRegion(3) | 674 713 cm-1 | (hb p. 28) |
| TempSpectralRegion(4) | 2223 2260 cm-1 | (hb p. 28) |
| WaterVaporSpectralRegion(1) | 538 588 cm-1 | (hb p. 28) |
| WaterVaporSpectralRegion(2) | 1250 1350 cm-1 | (hb p. 29) |
| RetrievalTopPressure (PTOP) | 700 mb | (hb p. 29) |
| CloudSearchMinimumPressure (PCLD) | 500 mb | (hb p. 29) |
| CloudSearchMaximumPressure (PCMIN) | 800 mb | (hb p. 29) |
| CloudSearchMinimumAmount (ACLD) | 0.001 | (hb p. 29) |
| CloudSearchMaximumAmount (AMTMX) | 0.4 | (hb p. 29) |
| MaximumIterationNumber (MITER) | 5 | (hb p. 28) |
| MaxResidualBrTemp (RTSQLMX) | 0.8 | (hb p. 30) |
| SurfacePressureLoLimit | 900.0 mb | (hb p. 29) |
| SurfacePressureHiLimit | 1020.0 mb | (hb p. 29) |
| SurfacePressureNominal | 1000.0 mb | (hb p. 29) |
| AERIsceneViewDuration (SVDUR) | 195.03 seconds | (hb p. 29) |
| MinTempDiffHatchOpen (TDHTCH) | 6.0 K (implied) | (hb p. 30) |
| MinTempDiffClearSky (TDVRFY) | 40.0 K (implied) | (hb p. 30) |
| tempBlendHeightBottom (GTBHBTM) | 0.8 km | (hb p. 30) |
| tempBlendHeightTop (GTBHTOP) | 1.3 km | (hb p. 30) |
| dewptBlendHeightBottom (GDBHBTM) | 1.0 km | (hb p. 30) |
| dewptBlendHeightTop (GDBHBTM) | 2.0 km | (hb p. 30) |
| RetrievalConditioningParameter (GAMMA) | .001 | (hb p. 29) |


_4 further rows in the report._

## The data

Verified example: **`sgpaeriprof3feltzC1.c1`**, file `sgpaeriprof3feltzC1.c1.20250625.001039.cdf`
(0.48 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=94, `height`=58, `CPL`=60 |
| Data variables | 34 |
| QC variables | 14 (`qc_` companions) |
| Median time step | 917 s |
| File time span | 2025-06-25T00:10:39 to 2025-06-25T23:51:00 |
| dod version | aeriprof3feltz-c1-2.1 |
| process version | Exp |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `CPL_ambientTemp` | K | time,CPL | yes | CPL retrieval of ambient temperature |
| `CPL_dewpointTemp` | K | time,CPL | yes | CPL retrieval of dewpoint temperature |
| `CPL_height` | meters above ground... | time,CPL | yes | CPL height array for the profile |
| `CPL_pressure` | kPa | time,CPL | yes | CPL retrieval of atmospheric pressure |
| `CPL_waterVaporMixingRatio` | g/kg | time,CPL | yes | CPL retrieval of water vapor mixing ratio |
| `auxDataFlagsNow` | unitless | time | yes | Auxiliary inputs used for this retrieval |
| `auxDataFlagsToday` | unitless | - | yes | Auxiliary inputs used today |
| `cloudBaseHeight` | meters above ground... | time | yes | Cloud base height |
| `dewpointTemperature` | K | time,height | yes | Interpolated dewpoint temperature |
| `pressure` | kPa | time,height | yes | Interpolated atmospheric pressure |
| `profile_source_flag` | unitless | time,CPL | yes | Profile source flag |
| `temperature` | K | time,height | yes | Interpolated ambient temperature |
| `totalPrecipitableWater` | cm | time | yes | Total precipitable water vapor, from microwave radiometer |
| `waterVaporMixingRatio` | g/kg | time,height | yes | Interpolated water vapor mixing ratio |
| `CPL` | count | CPL | - | Constant pressure level |
| `aqc_retrievalRejectionFlag` | unitless | time | - | Retrieval rejection flag |
| `height` | meters above ground... | height | - | Height array for the profile |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgpaeriprof3feltzC1.c1",
                             "start": "2025-06-25", "end": "2025-06-25", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaeriprof3feltzC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaeriprof3feltzC1.c1", "2025-06-25", "2025-06-25")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaeriprof3feltzC1.c1", "2025-06-25", "2025-06-25"))   # cite what you pulled
```

## Quality control in this product

14 `qc_` companion variables cover 14 of the
34 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_pressure"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("pressure", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["pressure", "temperature", "dewpointTemperature"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaeriprof3feltzC1.c1.20250625.001039.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cloudBaseHeight` | Clear sky conditions, original data value of -30; data value in... | 93 | 98.9362 |
| `waterVaporMixingRatio` | Relative humidity calculated from the waterVaporMixingRatio,... | 182 | 3.3382 |
| `pressure` | Valid data value not available in input file, data value in... | 174 | 3.1915 |
| `temperature` | Valid data value not available in input file, data value in... | 174 | 3.1915 |
| `dewpointTemperature` | Valid data value not available in input file, data value in... | 174 | 3.1915 |
| `waterVaporMixingRatio` | Valid data value not available in input file, data value in... | 174 | 3.1915 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaeriprof3feltzC1.c1", "19960614", "20260924")
```

The report's own note on quality: AERIPROF applies input-data QC flags for surface data (0=OK,1=dewpoint substituted from AERI RH due to bad surface station dewpoint,greater than 2=bad surface T/P/RH) and lidar data (0=OK,1=fog/condensation on window,2=no data in AERI time period,3=no valid data in file). Retrieval profile rejection flags (0-10) are assigned per AERI record and stored in the AERIPROF physical retrieval netCDF file, indicating reasons the physical retrieval was not output (double saturation, uncertain sky conditions, low cloud, cloud signal too large, residual too large, null input, negative radiances,...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Ill-posed inversion requiring a first-guess profile | Without a good first guess the retrieval can be unstable; retrieved profiles depend strongly on the quality of the first-guess source (statistical, GOES, or RUC) | Use an iterative physical retrieval constrained by a first-guess profile (statistical regression, GOES, or RUC), employing an onion-peeling approach... | (hb p. 5) |
| Diminishing information content with height | Retrieved profiles (statistical and physical) are only reliable below approximately 3 km; above this the AERI-only retrieval converges toward the mean atmospheric state | Blend with RUC (or previously GOES) mid/upper-tropospheric profiles above ~2-3 km to extend profiles through the troposphere. | (hb p. 6) |
| RUC model boundary-layer inaccuracy | RUC's 20-km horizontal resolution does not accurately portray boundary-layer thermodynamic structure; nocturnal temperature inversions often missed and moisture biases occur in RUC... | AERI physical retrieval modifies the merged first-guess profile in the boundary layer using AERI radiance to correct RUC boundary-layer state. | (hb p. 6) |
| Cloud contamination of retrieval | Spikes in retrieved temperature (warm spikes) and moistening of water vapor profile during cloud-contaminated but undetected conditions, especially high thin cirrus (greater than 5 km) not... | Compare PWV from AERIPROF retrieval to independent MWR PWV (MWR not used as constraint in retrieval) to identify cloud contamination; SIP file cloud... | (hb p. 11) |
| Retrieval not available or unstable during extensive/low cloud periods | Gaps in AERI-retrieved profile time series during heavy cloud cover (e.g., 1500-1800 UTC in example case); retrieval instabilities/warm spikes when clouds not detected by lidar but within... | When physical retrieval fails or is skipped due to low clouds (below CloudSearchMaximumPressure), RUC profile is substituted in the output with... | (hb p. 11) |
| Interpolation error from pressure-to-height conversion (hypsometric equation) | Small discrepancies introduced in height-gridded profiles relative to native pressure-grid retrieval, present in 1Feltz/2Feltz output | 3Feltz version outputs data on original pressure grid to preserve accuracy, while also providing an interpolated constant-height grid for downstream... | (hb p. 6) |
| Regression/spectroscopic bias errors in forward model | Systematic offset between observed and calculated AERI radiance spectra (non-zero mean spectral difference) | Apply an empirically-derived bias spectrum (subtracted from observed spectrum before retrieval); improvements in LBLRTM/HITRAN reduced bias magnitude... | (hb p. 3) |
| Radiosonde dry bias contaminating bias-spectrum calibration | If radiosonde profiles used to derive the bias spectrum have a dry bias in water vapor, that error is introduced into all subsequent AERIPROF retrievals | Use MWR-scaled radiosonde humidity profiles (shown to have less bias/variability) rather than unscaled radiosondes when deriving the bias spectrum. | (hb p. 3) |
| Retrieval convergence failure | Residual RMS between observed and calculated radiance does not fall below threshold within maximum iterations, or residual increases rather than decreases during iteration | Retrieval is aborted and flagged (QC flag 5, 'Residual too large'); RUC profile substituted in output. | (hb p. 12) |
| Double saturation in profile | Two levels in first-guess, iterated-guess, or physically retrieved profile reach 100% saturation | Flagged as QC flag 1; RUC profile substituted. | (hb p. 12) |
| Conflicting cloud information between lidar and AERI spectra | Sky-condition ambiguity flagged when lidar cloud detection disagrees with AERI spectral cloud signal | Flagged as QC flag 2 ('Sky conditions uncertain'); RUC profile substituted. | (hb p. 12) |
| Low cloud below maximum allowed pressure level | Retrieval skipped entirely for samples where cloud altitude is below (pressure above) the SIP-defined CloudSearchMaximumPressure (default 800 mb) | Flagged as QC flag 3 ('Low cloud'); RUC profile substituted. | (hb p. 12) |
| Cloud signal too large without lidar data | When lidar data unavailable, AERI brightness-temperature difference between opaque CO2 region and window region falls below SIP threshold, indicating strong cloud signal | Flagged as QC flag 4; retrieval skipped, RUC profile substituted. | (hb p. 12) |
| Missing/NULL AERI radiance input | AERI radiances absent from radiance netCDF file for a given time | Flagged as QC flag 6 ('NULL input'); RUC profile substituted. | (hb p. 12) |
| Negative radiances after apodization | Apodized AERI radiance spectrum contains negative values, indicating instrument/processing error | Flagged as QC flag 7 ('Negative radiances'); retrieval skipped. | (hb p. 12) |
| Gross-error check failure in radiance QC (aeriqc.f) | AERI radiance fails basic sanity/gross-error tests | Flagged as QC flag 8; retrieval skipped, RUC profile substituted. | (hb p. 12) |
| AERI hatch-open test failure (instrument view obstruction) | Brightness-temperature difference between opaque CO2 region and window region is less than SIP-defined threshold, indicating AERI hatch may not be open / view obstructed | Flagged as QC flag 9 ('Hatch-open test failed'); retrieval skipped, RUC profile substituted. | (hb p. 13) |
| No RUC data available for upper-level constraint | Retrieval performed using only regression (statistical) first guess, valid only from surface to 3 km, without RUC upper-air information | Flagged as QC flag 10 ('No RUC data'); retrieval limited to surface-3km using regression first guess. | (hb p. 13) |
| Radiosonde vertical resolution mismatch with AERI weighting functions | At times with rapid vertical transitions in water vapor gradient (e.g., 1130 UTC example), AERI retrieval smooths/misses fine structure resolved by radiosonde because infrared weighting... | None specific; noted as an inherent resolution limitation of the retrieval. | (hb p. 11) |
| GOES retrievals unavailable in cloudy (e.g., cirrus) conditions (2Feltz version) | In cloudy conditions the first guess for 2Feltz consisted solely of the statistical retrieval, lacking mid/upper-troposphere GOES information | 3Feltz version replaced GOES with RUC, which is available hourly regardless of cloud cover. | (hb p. 6) |
| MWR not used as retrieval constraint by ARM default | Statistical first-guess accuracy could be improved by using MWR PWV, but ARM default withholds MWR to preserve it as an independent QC check | ARM deliberately does not use MWR data in the retrieval so it can serve as an independent evaluation/QC source. | (hb p. 13) |
| Multiple simultaneous QC error conditions reported as single flag | Only the first-encountered error condition is reported per sample even if multiple QC issues exist, potentially masking additional problems | None stated beyond noting the limitation. | (hb p. 12) |
| Raman lidar water vapor input not available operationally | Research-mode-only option (temperature-only retrieval using Raman lidar q profile) not present in standard ARM output because Raman lidar data are not available away from SGP Central... | Not used operationally in ARM; restricted to research mode. | (hb p. 13) |
| First-guess/output files not retained | First-guess netCDF file (yyyymmddFG.cdf) and ascii log file are generated but not kept in the ARM data tree, so diagnostic first-guess profiles are unavailable to downstream users | None; only the physically retrieved AP.cdf-derived product (sgpAERIPROF3feltzC1.c1) is retained. | (hb p. 18) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `aeri`: load `arm-instrument-aeri` for its handbook facts and artifacts

### References the report cites

- Smith, WL et al. 1999. The retrieval of planetary boundary layer structure using ground-based infrared spectral radiance measurements. JAOT 16:323-333.
- Feltz, WF. 1994. Meteorological applications of AERI. M.S. thesis, University of Wisconsin-Madison.
- Feltz, WF et al. 1998. Meteorological applications of temperature and water vapor retrievals from AERI. J. Appl. Meteorol. 37:857-875.
- Turner, DD, WF Feltz, RA Ferrare. 2000. Continuous water profiles from operational ground-based active and passive remote sensors. BAMS 81:1301-1317.
- Feltz, WF, D Posselt, JR Mecikalski, GS Wade, TJ Schmit. 2003. Rapid boundary layer water vapor transitions. BAMS 84:29-30.
- Feltz, WF, HB Howell, RO Knuteson, HM Woolf, HE Revercomb. 2003. Near continuous profiling of temperature, moisture, and atmospheric stability using AERI. J. Appl. Meteorol. 42:584-597.
- Feltz, WF, JR Mecikalski. 2002. Monitoring high temporal resolution convective stability indices using AERI. Weather Forecasting 17:445-455.
- Schmit, TJ, WF Feltz, WP Menzel, J Jung, JP Nelson III, GS Wade. 2002. Validation and use of GOES sounder moisture information. Wea. Forecasting 17:139-154.
- Revercomb, HE et al. 2003. The ARM Water Vapor IOPs: Overview, accomplishments, and future challenges. BAMS 84:217-236.
- Turner, DD, BM Lesht, SA Clough, JC Liljegren, HE Revercomb, DC Tobin. 2003. Dry bias and variability in Vaisala RS80-H radiosondes: The ARM experience. JAOT 20:117-132.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-066.1.pdf (35 pages, DOE/SC-ARM/TR-066.1, by W.F. Feltz, D.D. Turner, H.B. Howell, W.L. Smith, R.O. Knuteson, H.M. Woolf, J. Comstock, C. Sivaraman, R. Mahon, T. Halter)
- Catalog record: ARM data-source index, `instrument_class_code=aeriprof`, read 2026-09-24
- Example file: `sgpaeriprof3feltzC1.c1.20250625.001039.cdf` from `sgpaeriprof3feltzC1.c1`, 0.48 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
