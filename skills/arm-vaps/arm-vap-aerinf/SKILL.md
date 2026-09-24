---
name: arm-vap-aerinf
description: ARM AERI Noise Filtered (aerinf) - value-added product reference from its technical report. Derived from aeri. The retrieval algorithm, reported quantities (Noise-equivalent spectral radiance, Eigenvalues from PCA decomposition), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaerich2nf1turnC1.c1) and the variable inventory of a real file. Use when working with aerinf data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Radiometric. Triggers - aerinf, AERI Noise Filtered, sgpaerich2nf1turnC1.c1, aeri VAP, Noise-equivalent spectral radiance, Eigenvalues from PCA decomposition, Radiometric.
---

# AERINF - AERI Noise Filtered

The AERINF VAP applies principal component analysis to ground-based AERI downwelling spectral radiance observations at the SGP, NSA, and TWP ACRF locales to remove uncorrelated random noise while preserving the atmospheric radiance signal.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 11 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aerinf` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-071 / C. Lo, D. D. Turner, R. O. Knuteson / January 2006](https://www.arm.gov/publications/tech_reports/arm-tr-071.pdf) |
| Category | Radiometric |
| Input instruments | `aeri` |
| Record | 2005-03-23 to 2026-09-20 (active) |
| Datastreams with data | 68 across 27 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aerinf |


## Credit

Everything this skill knows about the retrieval is the work of **C. Lo, D. D. Turner, R. O. Knuteson** -
the ARM developers and mentors who wrote the technical report it derives from:

> C. Lo, D. D. Turner, R. O. Knuteson. *A Principal Component Analysis Noise Filter Value-Added Procedure to Remove Uncorrelated Noise from Atmospheric Emitted Radiance Interferometer (AERI) Observations*, DOE/SC-ARM/TR-071, January 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-tr-071.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Principal Component Analysis (PCA) is a statistical technique that compresses data into an orthogonal factor space, decomposing the AERI radiance data into a set of orthogonal vectors (principal components), each of which explains some fraction of the total variance in the dataset. Because many AERI spectral channels are well correlated with each other, PCA can be used to filter out uncorrelated random error without introducing significant artifacts such as loss of atmospheric information. The VAP automatically determines the appropriate number of principal components to retain, using an empirical function, and reconstructs the radiance spectrum from only those components. Principal components with small eigenvalues are typically associated with random error and are removed before reconstruction, so the reconstructed (noise-filtered) data has a smaller random error component than the original observations.

**Cadence.** output every 8 minutes (nominal, 3-minute average every 8 minutes) or 15-30 seconds / 20-second data (rapid-sample, RS mode); averaging three-minute average of sky radiance (nominal mode) (hb p. 4).

## Inputs

ARM's catalog declares these input instrument classes: `aeri`.

The report names these instruments and sibling products: AERI, AERI-01.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Downwelling emitted spectral radiance (mean_rad) | mW/(m2 sr cm-1) | 500-3000 cm-1 (AERI); Channel 1:... | - | (hb p. 4) |
| Noise-equivalent spectral radiance (NESR) -... | mW/(m2 sr cm-1) | - | - | (hb p. 5) |
| Longwave sky noise-equivalent radiance (LWskyNEN) | mW/(m2 sr cm-1) | - | - | (hb p. 5) |
| Eigenvalues from PCA decomposition (output field, not in... | - | - | - | (hb p. 6) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| AERI spectral coverage | 500-3000 cm-1 | (hb p. 4) |
| AERI spectral resolution | 1 cm-1 | (hb p. 4) |
| Original temporal sampling | three-minute average of sky radiance every eight minutes | (hb p. 4) |
| Rapid-sample (RS) temporal resolution | sky spectrum every 15-30 seconds | (hb p. 4) |
| RS data file interval | 20-second data | (hb p. 5) |
| Channel 1 spectral sensitivity | 5-25 micron | (hb p. 5) |
| Channel 2 spectral sensitivity | 3-5 micron | (hb p. 5) |
| Summary file spectral resolution | 25 cm-1 | (hb p. 5) |
| Minimum temporal samples for filtering | at least 5000 (each channel has 2500 spectral elements) | (hb p. 7) |
| Recommended processing period, nominal data | one-month periods | (hb p. 7) |
| Recommended processing period, RS data | ten-day periods | (hb p. 7) |
| Bad spectra threshold, 900 cm-1 radiance | less than -5 mW/(m2 ster cm-1) or above 170 mW/(m2 ster cm-1) (~55 degC brightness temperature) | (hb p. 8) |
| Bad sample threshold, LWskyNEN nominal data | larger than 7 mW/(m2 ster cm-1) | (hb p. 8) |
| Bad sample threshold, LWskyNEN RS data | larger than 25 mW/(m2 ster cm-1) | (hb p. 8) |


## The data

Verified example: **`sgpaerich2nf1turnC1.c1`**, file `sgpaerich2nf1turnC1.c1.20260916.000409.nc`
(79.91 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=3927, `wnum`=2532, `wnum2`=2531 |
| Data variables | 25 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 16 s |
| File time span | 2026-09-16T00:04:09 to 2026-09-16T23:54:22 |
| dod version | aerich2nf1turn-c1-1.1 |
| process version | vap-aerinoisefilter-3.1-5.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `AERIunitNumber` | 1 | time | - | AERI instrument unit serial number |
| `BBsupportStructureTemp` | K | time | - | Temperature of the AERI blackbody support structure |
| `atmosphericPressure` | hPa | time | - | Observation atmospheric pressure in AERI electronics |
| `atmosphericRelativeHumidity` | % | time | - | Relative humidity measured near Blackbodies. Use with Air Temperature... |
| `calibratedSceneID` | 1 | time | - | Calibrated Scene Type Identification |
| `calibrationAmbientTemp` | K | time | - | Ambient temperature used in calibration |
| `calibrationCBBtemp` | K | time | - | Cold blackbody temperature used in calibration |
| `calibrationHBBtemp` | K | time | - | Hot blackbody temperature used in calibration |
| `channelNumber` | 1 | time | - | AERI instrument data channel number |
| `eigenvalues` | 1 | wnum | - | Eigenvalues used to reconstruct radiance derived from principal... |
| `hatchOpen` | 1 | time | - | Hatch Open Flag |
| `instrumentUnitNumber` | 1 | time | - | Character string containing instrument name |
| `mean_rad` | mW/(m^2 sr cm^-1) | time,wnum | - | Downwelling radiance interpolated to standard wavenumber scale |
| `missingDataFlag` | 1 | time | - | Logical flag indicating that a data record is missing (true/false) |
| `outsideAirTemp` | K | time | - | Ambient air temperature at hatch opening |
| `sceneMirPosEncoderMaxDrift` | count | time | - | Scene Mirror Position Encoder Maximum Drift |
| `sceneMirrorAngle` | degree | time | - | Scene mirror view angle in non-negative degrees, measured clockwise... |
| `sceneViewDuration` | s | time | - | Duration of scene view |
| `standard_dev_mean_rad` | (mW/(m^2 sr cm^-1))^2 | time,wnum2 | - | Difference between the sky view's radiance variance and the hot black... |
| `systemReleaseNumber` | 1 | time | - | Version number of Operational Software |
| `time` | - | time | - | Time offset from midnight |
| `wnum` | cm^-1 | wnum | - | Wave number in reciprocal centimeters |
| `wnum2` | cm^-1 | wnum2 | - | Wave number 2 in reciprocal centimeters |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaerich2nf1turnC1.c1", "2026-09-16", "2026-09-16")
ds = armlive_open("sgpaerich2nf1turnC1.c1", "2026-09-16", "2026-09-16", cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaerich2nf1turnC1.c1", "20050323", "20260924")
```

The report's own note on quality: The VAP applies quality control to input radiance spectra before PCA because bad spectra can significantly skew PCA results and make the noise-filtered data suboptimal. Two bad-data criteria are used: (1) mean observed radiance at 900 cm-1 outside -5 to 170 mW/(m2 ster cm-1), and (2) LWskyNEN exceeding 7 mW/(m2 ster cm-1) (nominal data) or 25 mW/(m2 ster cm-1) (RS data). Flagged bad samples are removed from the dataset prior to noise filtering. The output file's qc_time field is recalculated because time samples are synchronized among the three input files, and its attributes were rewritten...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Increased random noise from higher temporal resolution (RS mode) | Larger random fluctuations/uncorrelated noise component in rapid-sample (15-30 second) sky spectra compared to nominally sampled 8-minute data, due to reduced instrument averaging | Apply PCA noise filter VAP to reduce uncorrelated random error while preserving atmospheric signal | (hb p. 4) |
| Insufficient number of temporal samples relative to spectral elements | PCA filtering removes atmospheric signal along with noise rather than just uncorrelated random error if the number of time samples is not sufficiently larger than twice the number of... | Require number of time samples used in filtering be greater than two times number of spectral elements, preferably much larger; found little... | (hb p. 7) |
| Computer memory capacity limits processing window size | Limits on how large a window of AERI data can be noise-filtered in a single VAP run | Process in one-month periods (nominal) or ten-day periods (RS) | (hb p. 7) |
| Mismatched time samples among Channel 1, Channel 2, and summary input files | The three AERI input data files (ch1, ch2, summary) may not have the same number of samples due to how the AERI instrument operates | VAP performs time synchronization so only common time samples among the three files are kept | (hb p. 7) |
| Bad/anomalous radiance spectra skewing PCA results | Mean observed radiance at 900 cm-1 less than -5 mW/(m2 ster cm-1) or above 170 mW/(m2 ster cm-1) (approx. 55 degC brightness temperature) | Sample flagged as bad and removed from the dataset before the noise filter is applied | (hb p. 8) |
| Excessive longwave sky noise-equivalent radiance (poor instrument performance/noise... | LWskyNEN field exceeds 7 mW/(m2 ster cm-1) for nominally sampled data or 25 mW/(m2 ster cm-1) for RS data | Sample identified as bad and removed from the dataset before the noise filter is applied | (hb p. 8) |
| Real atmospheric signal spikes could be mistaken for noise | A spike in the radiance time series (e.g., at 18:55 UTC in example) that persists in the noise-filtered data is a real signal, not a noise artifact | Analyst should recognize such features are real atmospheric signal, not noise, since the filter is designed to remove only uncorrelated random error | (hb p. 5) |
| Residual differences between filtered and unfiltered spectra | Difference (residual) between noise-filtered and original radiance spectrum shows only random, Gaussian-distributed differences with no biases across the spectrum, confirming removed... | - | (hb p. 9) |


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

- Feltz, WF, WL Smith, HB Howell, RO Knuteson, H Woolf, and HE Revercomb. 2003. Journal of Applied Meteorology 42, 584-597.
- Knuteson, RO, et al. 2004a. Atmospheric emitted radiance interferometer. Part I: Instrument design. Journal of Atmospheric and Oceanic Technology 21, 1763-1776.
- Knuteson, RO, et al. 2004b. Atmospheric emitted radiance interferometer. Part II: Instrument performance. Journal of Atmospheric and Oceanic Technology 21, 1777-1789.
- Tobin, DC, et al. 1999. Downwelling spectral radiance observations at the SHEBA ice station. Journal of Geophysical Research 104, 2081-2092.
- Turner, DD, et al. 2004. The QME AERI LBLRTM: A closure experiment for downwelling high spectral resolution infrared radiance. Journal of Atmospheric Science 61, 2657-2675.
- Turner, DD. 2005. Arctic mixed-phase cloud properties from AERI-lidar observations: Algorithm and results from SHEBA. Journal of Applied Meteorology 44, 427-444.
- Turner, DD, RO Knuteson, HE Revercomb, C Lo, and RG Dedecker. 2006. Noise reduction of Atmospheric Emitted Radiance Interferometer (AERI) observations using principal component analysis. Journal of Atmospheric and...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-tr-071.pdf (11 pages, DOE/SC-ARM/TR-071, by C. Lo, D. D. Turner, R. O. Knuteson)
- Catalog record: ARM data-source index, `instrument_class_code=aerinf`, read 2026-09-24
- Example file: `sgpaerich2nf1turnC1.c1.20260916.000409.nc` from `sgpaerich2nf1turnC1.c1`, 79.91 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
