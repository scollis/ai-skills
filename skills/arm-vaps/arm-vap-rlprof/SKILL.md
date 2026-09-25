---
name: arm-vap-rlprof
description: ARM Raman LIDAR Vertical Profiles (rlprof) - value-added product reference from its technical report. Derived from rl. The retrieval algorithm, reported quantities (Photon counting rate, Analog voltage, Cloud base height, Dark current, Glue coefficients - analog offset, Height), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgp10rlprofbe1newsC1.c1) and the variable inventory of a real file. Use when working with rlprof data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Atmospheric Profiling; Cloud Properties. Triggers - rlprof, Raman LIDAR Vertical Profiles, sgp10rlprofbe1newsC1.c1, rl VAP, Photon counting rate, Analog voltage, Cloud base height, Dark current, Glue coefficients - analog offset, Aerosols.
---

# RLPROF - Raman LIDAR Vertical Profiles

The MERGE VAP combines simultaneously recorded analog and photon-counting signals from each channel of the ARM Raman lidar into a single "glued" photon counting rate profile with improved dynamic range, which serves as input to higher-level Raman lidar water vapor, temperature, aerosol backscatter, extinction, and depolarization VAPs.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 22 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `rlprof` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-189 / RK Newsom, J Goldsmith, C Sivaraman / April 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-189.pdf) |
| Category | Aerosols; Atmospheric Profiling; Cloud Properties |
| Input instruments | `rl` |
| Record | 1998-03-01 to 2026-09-23 (active) |
| Datastreams with data | 34 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/rlprof |


## Credit

Everything this skill knows about the retrieval is the work of **RK Newsom, J Goldsmith, C Sivaraman** -
the ARM developers and mentors who wrote the technical report it derives from:

> RK Newsom, J Goldsmith, C Sivaraman. *Raman Lidar MERGE Value-Added Product*, DOE/SC-ARM-TR-189, April 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-189.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-189 documents the Raman Lidar MERGE product specifically, not the wider `rlprof*` family, so facts here describe that member.

## How it is produced

For each detection channel the MERGE VAP reads raw photon counts and analog voltages from the raw RL datastream, converts them to photon counting rate (MHz) and analog voltage (mV), applies an analog delay shift and a pulse pile-up (dead-time) correction to the photon counting rate, and identifies cloud base heights to exclude cloud-affected data from calibration. It then performs a linear regression between the corrected photon counting rate and analog voltage (using bin-averaged data over a 24-hour period, restricted to Cminless than Cless than Cmax and heights below cloud base) to determine "glue" coefficients: the analog offset (Ao) and scale factor (s). These coefficients define a "virtual" photon counting rate extrapolated from the analog signal, which is spliced with the corrected photon counting rate above Cmax to produce a merged profile with extended dynamic range and improved linearity. Random uncertainty in the photon counting rate is derived from Poisson counting statistics.

**Cadence.** input rate 10 s per profile (accumulated laser shots at 30 Hz); output every twice-daily netCDF files; MERGE VAP processes one 24-hour period at a time; averaging Glue coefficients (Ao, s) computed once per day per channel using all 10-s profiles from that 24-hour period, via linear regression on photon-counting-rate-binned (0.2 MHz bins) analog data (hb p. 10).

## Inputs

ARM's catalog declares these input instrument classes: `rl`.

The report names these instruments and sibling products: Raman lidar (RL), Water vapor mixing ratio VAP, Temperature VAP, Aerosol backscatter VAP, Extinction VAP, Depolarization ratio VAP.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Photon counting rate (uncorrected, corrected, merged) | MHz | - | - | (hb p. 10) |
| Analog voltage | mV | Amax = 20 mV | - | (hb p. 10) |
| Cloud base height (CBH) | - | - | - | (hb p. 7) |
| Dark current (background photon counting rate) | MHz (rate) | - | - | (hb p. 8) |
| Glue coefficients: analog offset (Ao) and scale factor (s) | mV / (MHz per mV) | - | Ao relative std dev 0.18%, s relative std dev... | (hb p. 12) |
| Height | m | ~200 m to greater than 10 km AGL | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Transmit wavelength | 355 nm | (hb p. 7) |
| Pulse energy | 300 mJ | (hb p. 7) |
| Pulse duration | ~5 ns | (hb p. 7) |
| Pulse repetition frequency | 30 Hz | (hb p. 7) |
| Number of detection channels | 9 (2 water vapor 408 nm, 2 nitrogen 387 nm, 3 elastic, 2 rotational Raman 354/353 nm) | (hb p. 7) |
| NFOV field of view | 0.3 mrad | (hb p. 7) |
| WFOV field of view | 2 mrad | (hb p. 7) |
| Height resolution (range gate size, Δr) | 7.5 m | (hb p. 7) |
| Time resolution (native) | 10 s | (hb p. 7) |
| NFOV range bins per profile | 4,000 | (hb p. 8) |
| WFOV range bins per profile | 1,500 | (hb p. 8) |
| Digitizer resolution (β) | 12 bits | (hb p. 10) |
| Analog gain setting (Amax) | 20 mV | (hb p. 10) |
| Analog range bin offset (noffset) | typically 3 to 10 | (hb p. 11) |
| Dead-time coefficient (τ, response time) | typically ~3 to 8 ns | (hb p. 12) |
| Fit lower threshold (Cmin) | 1 MHz | (hb p. 15) |
| Fit upper threshold (Cmax) | 15 MHz | (hb p. 15) |
| Photon counting rate bin size for regression | 0.2 MHz | (hb p. 16) |
| Fit success residual threshold | less than  0.01 mV RMS difference | (hb p. 16) |
| Fit success correlation threshold | Pearson correlation coefficient greater than  0.95 | (hb p. 16) |
| CBH derivative peak magnitude threshold | greater than  0.1 mV km | (hb p. 13) |
| CBH peak separation range | 2 to 15 range bins | (hb p. 13) |
| CBH temporal isolation rejection threshold | greater than  1 km difference from adjacent profiles | (hb p. 13) |
| PMT model | Electron Tubes 9954B | (hb p. 7) |
| Data recorder | Licel GbR transient data recorders | (hb p. 7) |


## The data

Verified example: **`sgp10rlprofbe1newsC1.c1`**, file `sgp10rlprofbe1newsC1.c1.20150918.000500.cdf`
(2.77 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=144, `height`=198 |
| Data variables | 43 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2015-09-18T00:05:00 to 2015-09-18T23:55:00 |
| dod version | 0.1 |
| process version | $State: vap-rlprof_be-0.5-0.el6$ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `aod` | unitless | time | yes | Aerosol optical depth |
| `aod_profile` | unitless | time,height | yes | Aerosol optical depth profile |
| `asr` | unitless | time,height | yes | Aerosol scattering ratio |
| `bscat` | 1/(ster km) | time,height | yes | Aerosol backscatter coefficient |
| `cmask` | unitless | time,height | yes | Cloud mask from depolarization VAP |
| `cot` | unitless | time | yes | Cloud optical depth from elastic data |
| `dep` | % | time,height | yes | Linear depolarization ratio profile |
| `ext` | km^(-1) | time,height | yes | Aerosol extinction coefficient |
| `mr` | g/km | time,height | yes | Water vapor mixing ratio observed by the Raman lidar |
| `pwv` | cm | time | yes | Precipitable water vapor observed by the Raman lidar |
| `rh` | % | time,height | yes | Relative humidity observed by the Raman lidar |
| `aod_err` | unitless | time | - | Aerosol optical depth uncertainty |
| `aod_max_height` | km | time | - | Maximum height for aod |
| `asr_err` | unitless | time,height | - | Aerosol scattering ratio uncertainty |
| `bscat_err` | 1/(ster km) | time,height | - | Aerosol backscatter coefficient uncertainty |
| `cot_err` | unitless | time | - | Uncertainty in cloud optical depth from elastic data |
| `dep_err` | % | time,height | - | Linear depolarization ratio uncertainty |
| `ext_err` | km^(-1) | time,height | - | Aerosol extinction coefficient uncertainty |
| `height` | km | height | - | Height above ground level |
| `mr_err` | g/km | time,height | - | Uncertainty in water vapor mixing ratio observed by the Raman lidar |
| `mr_max_height` | km | time | - | Suggested maximum altitude to use the water vapor from the Raman lidar |
| `mr_sonde` | g/kg | time,height | - | Sonde mixing ratio |
| `pressure` | mb | time,height | - | Pressure from sgpaeriprof3feltzC1.c1 |
| `pwv_err` | cm | time | - | Uncertainty in precipitable water vapor observed by the Raman lidar |
| `pwv_fraction` | unitless | time | - | Fraction of the total column amount of water vapor the Raman lidar... |
| `pwv_mwr` | cm | time | - | Precipitable water vapor from microwave radiometer |
| `sample_times_sonde` | unitless | time | - | Sonde sample times |
| `temperature` | C | time,height | - | Temperature from sgpaeriprof3feltzC1.c1 |
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
                     params={"user": f"{user}:{token}", "ds": "sgp10rlprofbe1newsC1.c1",
                             "start": "2015-09-18", "end": "2015-09-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp10rlprofbe1newsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp10rlprofbe1newsC1.c1", "2015-09-18", "2015-09-18")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgp10rlprofbe1newsC1.c1", "2015-09-18", "2015-09-18"))   # cite what you pulled
```

This product carries 43 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgp10rlprofbe1newsC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['aod', 'aod_profile', 'asr', 'qc_aod', 'qc_aod_profile', 'qc_asr'],
                                cleanup_qc=True)
```

## Quality control in this product

11 `qc_` companion variables cover 11 of the
43 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_asr"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("asr", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["asr", "bscat", "ext"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgp10rlprofbe1newsC1.c1.20150918.000500.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cot` | Data quality suspect | 104 | 72.2222 |
| `cot` | Data value not available in input file, data value set to -9999... | 99 | 68.75 |
| `bscat` | Error exceeds 25% | 17948 | 62.9489 |
| `ext` | Error exceeds 25% | 17590 | 61.6933 |
| `rh` | Data quality suspect | 16689 | 58.5332 |
| `asr` | Data quality suspect | 16329 | 57.2706 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgp10rlprofbe1newsC1.c1", "19980301", "20260924")
```

The report's own note on quality: The MERGE VAP produces per-channel, per-time fit_status flags (1=success, 0=failure) indicating whether the daily linear regression met the residual (less than 0.01 mV RMS) and correlation (Pearson rgreater than 0.95) thresholds; when it fails, default glue coefficients from the configuration file are used instead. A merge_flag variable (per channel, time, height) indicates whether each sample is corrected photon counting data (0), virtual/extrapolated photon counting data (1), or saturated/clipped signal (2). Cloud base height estimates undergo a temporal-isolation rejection check to...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Analog signal poor sensitivity at low signal levels; photon counting signal strongly... | Analog voltage profile noisy/flat at low return, photon counting rate curves away from linear (pulse pile-up curve) at high count rates | Combine (glue) both signals into a merged profile with improved dynamic range | (hb p. 7) |
| Analog signal timing delay relative to photon counting data | Misalignment between analog and photon-count profiles in range if uncorrected | Shift analog profile by a fixed range-bin offset (noffset, typically 3-10 bins) determined offline per Licel unit | (hb p. 11) |
| Electronic background/offset in analog signal superimposed on ambient signal | Nonzero analog voltage baseline even absent atmospheric or background light, visible below z=0 | - | (hb p. 11) |
| Ground spike | Sharp spike in both analog voltage and photon counting rate signals at z=0 (pulse leaving the lidar) | - | (hb p. 11) |
| Pulse pile-up (dead-time) nonlinearity in photon counting rate | Photon counting rate vs analog voltage plot shows distinct curved (nonlinear) relationship at higher count rates instead of a straight line | Apply dead-time correction using per-channel response time τ (typically 3-8 ns) from Whiteman et al. (2006) formula | (hb p. 12) |
| Residual nonlinearity in corrected photon counting rate above ~15 MHz | Corrected photon counting rate (blue curve) deviates from virtual/extrapolated rate above Cmax=15 MHz in profile comparison plots | Splice in virtual photon counting rate (derived from analog signal via glue coefficients) above Cmax to restore linearity in merged profile | (hb p. 16) |
| Cloud contamination of glue-coefficient regression | Spikes in analog voltage profile at cloud base height that would bias the linear regression if included | Detect cloud base height via first-derivative method and exclude data above CBH from the regression used to compute glue coefficients | (hb p. 13) |
| False cloud base height detections | Isolated CBH estimates in time that differ by more than 1 km from CBH in adjacent profiles | Reject temporally isolated CBH estimates where absolute difference from both neighboring profiles exceeds 1 km | (hb p. 13) |
| Saturated/clipped signal | White regions in merge-flag time-height cross-section (Figure 9c) indicating clipped/saturated samples | Flagged via *_counts_high_merge_flag / *_counts_low_merge_flag value of 2 | (hb p. 12) |
| Failed glue regression (poor fit) | fit_status flag = 0 for a given day/channel; occurs when fit residual exceeds 0.01 mV or Pearson correlation below 0.95 | Default glue coefficients from rlprof_merge_glue.conf configuration file are substituted | (hb p. 16) |
| Dark current / inherent PMT noise floor | Nonzero photon counting rate during 'mode 0' (filter wheel blocked) periods | Computed daily per channel from mode-0 profiles and reported as *_counts_high/low_background; useful for characterizing PMT noise limit | (hb p. 8) |
| Random (Poisson) uncertainty in photon counting rate not explicitly output | No explicit uncertainty variable in MERGE output; must be derived by user | Uncertainty can be computed by converting counting rate back to counts, taking square root (Poisson statistics), then reconverting to rate per Eq. 13 | (hb p. 19) |
| Ambient background recorded before ground bin | Nonzero signal for jless than no or zless than 0 (negative height) representing ambient light background rather than atmospheric return | - | (hb p. 10) |
| Glue coefficient temporal variability | Analog offset (Ao) relative standard deviation ~0.18% and scale factor (s) relative standard deviation ~3.3% over ~14 months for NFOV N2 channel; scale factor shows small long-term drift | Daily (24-hr) recomputation of glue coefficients rather than per-profile regression, since per-profile regression was found to produce poorer water... | (hb p. 18) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `rl`: load `arm-instrument-rl` for its handbook facts and artifacts

### References the report cites

- Newsom, RK, DD Turner, B Mielke, MF Clayton, R Ferrare, and C Sivaraman. 2009. "Simultaneous analog and photon counting detection for Raman lidar." Applied Optics 48(20): 3903-3914, doi:10.1364/AO.48.003903.
- Turner, DD, RA Ferrare, LA Heilman Brasseur, WF Feltz, and TP Tooman, 2002. "Automated retrievals of water vapor and aerosol profiles from an operational Raman lidar." Journal of Atmospheric and Oceanic Technology 19:...
- Whiteman, DN, B Demoz, P Di Girolamo, J Comer, I Veselovskii, K Evans, Z Wang, M Cadirola, K Rush, G Schwemmer, B Gentry, SH Melfi, B Mielke, D Venable, and T Van Hove. 2006. "Raman Water Vapor Lidar Measurements during...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-189.pdf (22 pages, DOE/SC-ARM-TR-189, by RK Newsom, J Goldsmith, C Sivaraman)
- Catalog record: ARM data-source index, `instrument_class_code=rlprof`, read 2026-09-24
- Example file: `sgp10rlprofbe1newsC1.c1.20150918.000500.cdf` from `sgp10rlprofbe1newsC1.c1`, 2.77 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
