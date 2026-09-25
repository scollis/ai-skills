---
name: arm-vap-rlprof-fex
description: ARM Raman Lidar Vertical Profiles Feature Detection and Extinction (rlprof-fex) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Particulate extinction coefficient, Lidar ratio, Scattering ratio, Scattering ratio, Scattering ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgprlproffexext1thorC1.c0) and the variable inventory of a real file. Use when working with rlprof-fex data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Atmospheric Profiling; Cloud Properties. Triggers - rlprof-fex, sgprlproffexext1thorC1.c0, Particulate extinction coefficient, Lidar ratio, Scattering ratio, Aerosols, Atmospheric Profiling, Cloud Properties.
---

# RLPROF-FEX - Raman Lidar Vertical Profiles Feature Detection and Extinction

The RLPROF-FEX VAP processes Raman lidar elastic and nitrogen-Raman backscatter signals from ARM's ground-based Raman lidars at fixed sites (SGP, ENA, formerly OLI) to produce height-resolved, time-continuous best estimates of particulate extinction, backscatter, lidar ratio, depolarization ratio, and feature (aerosol/cloud/precipitation) masks.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 35 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `rlprof-fex` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-224 / D Chand, R Newsom, R Bambha, E Cromwell, T Thorsen, J Comstock / October 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-224.pdf) |
| Category | Aerosols; Atmospheric Profiling; Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2015-02-25 to 2026-09-23 (active) |
| Datastreams with data | 12 across 3 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/rlprof-fex |


## Credit

Everything this skill knows about the retrieval is the work of **D Chand, R Newsom, R Bambha, E Cromwell, T Thorsen, J Comstock** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Chand, R Newsom, R Bambha, E Cromwell, T Thorsen, J Comstock. *Aerosol and Cloud Optical Properties from the ARM Raman Lidars: The Feature Detection and Extinction (FEX) Value-Added Product*, DOE/SC-ARM-TR-224, October 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-224.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The FEX algorithm uses return signals from elastic backscatter at 355 nm and Raman-shifted backscatter from atmospheric nitrogen at 387 nm, measured through wide and narrow field-of-view receiver channels. It computes scattering ratios using both the observed nitrogen signal and a modeled nitrogen signal, plus the total volume depolarization ratio from co- and cross-polarized elastic channels. Range-dependent detection thresholds are applied to these ratios to identify aerosol, cloud (liquid vs. ice), and precipitation features, with consistency checks across the various ratios to construct a best feature mask. The algorithm iterates, refining scattering ratios, feature mask, depolarization ratio, backscatter, and extinction coefficients (adjusting overlap functions, calibration constants, and detection limits each iteration) until the feature mask converges below a prescribed threshold. Final outputs are corrected for multiple scattering effects and combine WFOV/NFOV Raman-method solutions and Fernald-solution elastic retrievals depending on data quality.

**Cadence.** input rate 10 sec pulse integration time; 30 Hz laser pulse repetition frequency; averaging Inputs from 2-5 days prior are used to initiate processing to produce output for a desired day; algorithm iterates until feature mask converges (hb p. 7).

## Inputs

The report names these instruments and sibling products: Raman lidar (RL) MERGE VAP, Radiosonde, AERONET, MODIS.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Particulate extinction coefficient (best estimate) | - | - | random and systematic uncertainty variables... | (hb p. 7) |
| Particulate backscatter coefficient (best estimate) | - | - | random and systematic uncertainty variables... | (hb p. 7) |
| Lidar ratio (best estimate) | - | - | random and systematic uncertainty variables... | (hb p. 7) |
| Scattering ratio (elastic + nitrogen, high channels) | - | - | random and systematic uncertainty variables... | (hb p. 6) |
| Scattering ratio (elastic + nitrogen, low channels) | - | - | random and systematic (maximum) uncertainty... | (hb p. 7) |
| Scattering ratio (elastic only, high channels) | - | - | random and systematic uncertainty variables... | (hb p. 7) |
| Volume linear depolarization ratio | - | - | random and systematic uncertainty variables... | (hb p. 6) |
| Pressure (from radiosonde) | - | - | - | (hb p. 6) |
| Temperature (from radiosonde) | - | - | - | (hb p. 6) |
| Wet bulb temperature | - | - | - | (hb p. 6) |
| Feature mask (bit-packed: aerosol, liquid cloud, ice cloud,... | - | - | - | (hb p. 8) |
| Detection confidence score (total and random) | - | 0 to 1 (-1 if beam fully... | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Laser | Nd:YAG, Third harmonic | (hb p. 7) |
| Transmitter wavelength | 355 nm | (hb p. 7) |
| Pulse energy | 300 mJ | (hb p. 7) |
| Pulse repetition frequency | 30 Hz | (hb p. 7) |
| Pulse width | 5 ns | (hb p. 7) |
| Telescope diameter | 61 cm | (hb p. 7) |
| FOV | 2 mrad (WFOV), 0.3 mrad (NFOV) | (hb p. 7) |
| Range resolution | 7.5 m | (hb p. 7) |
| Pulse integration time | 10 sec | (hb p. 7) |
| Data acquisition | simultaneous photon counting and analog voltage measurement | (hb p. 7) |
| Detectors | PMTs, Electron Tube 9954B | (hb p. 7) |
| Detection channels | Unpolarized WFOV elastic @ 355 nm; Co-polarized NFOV elastic @ 355 nm; Cross-polarized NFOV elastic at 355 nm; WFOV Nitrogen @ 387 nm; NFOV Nitrogen... | (hb p. 8) |


## The data

Verified example: **`sgprlproffexext1thorC1.c0`**, file `sgprlproffexext1thorC1.c0.20260920.000000.nc`
(48.14 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=720, `height_high`=667, `height_low`=290 |
| Data variables | 34 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 120 s |
| File time span | 2026-09-20T00:00:00 to 2026-09-20T23:58:00 |
| dod version | rlproffexext1thor-c0-1.0 |
| process version | 1.7-7.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `height_high` | km | height_high | - | Height above ground level for the high (NFOV) channels |
| `height_low` | km | height_low | - | Height above ground level for the low (WFOV) channels |
| `lidar_ratio_be_noMS` | sr | time,height_high | - | Best-estimate of the lidar ratio without accounting for multiple... |
| `lidar_ratio_e` | sr | time,height_high | - | Lidar ratio from the high elastic channels |
| `lidar_ratio_e_n2` | sr | time,height_high | - | Lidar ratio from the high nitrogen channel extinction and... |
| `lidar_ratio_e_n2_low` | sr | time,height_low | - | Lidar ratio from the low nitrogen channel extinction and... |
| `lidar_ratio_e_n2_low_noMS` | sr | time,height_low | - | Lidar ratio from the low nitrogen channel extinction and... |
| `lidar_ratio_e_n2_low_uncertainty_random` | sr | time,height_low | - | Random uncertainty in lidar_ratio_e_n2_low |
| `lidar_ratio_e_n2_noMS` | sr | time,height_high | - | Lidar ratio from the high nitrogen channel extinction and... |
| `lidar_ratio_e_n2_uncertainty_random` | sr | time,height_high | - | Random uncertainty in lidar_ratio_e_n2 |
| `lidar_ratio_e_noMS` | sr | time,height_high | - | Lidar ratio from the high elastic channels without accounting for... |
| `lidar_ratio_e_uncertainty_random` | sr | time,height_high | - | Random uncertainty in lidar_ratio_e |
| `lidar_ratio_e_uncertainty_systematic` | sr | time,height_high | - | Systematic uncertainty in lidar_ratio_e |
| `particulate_backscatter_be_noMS` | 1/(km*sr) | time,height_high | - | Best-estimate of the particulate backscatter coefficient without... |
| `particulate_backscatter_e` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient from the high elastic channels... |
| `particulate_backscatter_e_beS` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient from the high elastic channels... |
| `particulate_backscatter_e_beS_noMS` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient from the high elastic channels... |
| `particulate_backscatter_e_beS_uncertainty_random` | 1/(km*sr) | time,height_high | - | Random uncertainty in particulate_backscatter_e_beS |
| `particulate_backscatter_e_beS_uncertainty_systematic` | 1/(km*sr) | time,height_high | - | Systematic uncertainty in particulate_backscatter_e_beS |
| `particulate_backscatter_e_n2` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient calculated from the scattering... |
| `particulate_backscatter_e_n2_low` | 1/(km*sr) | time,height_low | - | Particulate backscatter coefficient calculated from the scattering... |
| `particulate_backscatter_e_n2_low_noMS` | 1/(km*sr) | time,height_low | - | Particulate backscatter coefficient calculated from... |
| `particulate_backscatter_e_n2_low_uncertainty_random` | 1/(km*sr) | time,height_low | - | Random uncertainty in particulate_backscatter_e_n2_low |
| `particulate_backscatter_e_n2_low_uncertainty_systematic` | 1/(km*sr) | time,height_low | - | Systematic uncertainty in particulate_backscatter_e_n2_low |
| `particulate_backscatter_e_n2_noMS` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient calculated from... |
| `particulate_backscatter_e_n2_uncertainty_random` | 1/(km*sr) | time,height_high | - | Random uncertainty in particulate_backscatter_e_n2 |
| `particulate_backscatter_e_n2_uncertainty_systematic` | 1/(km*sr) | time,height_high | - | Systematic uncertainty in particulate_backscatter_e_n2 |
| `particulate_backscatter_e_noMS` | 1/(km*sr) | time,height_high | - | Particulate backscatter coefficient from the high elastic channels... |
| `particulate_backscatter_e_uncertainty_random` | 1/(km*sr) | time,height_high | - | Random uncertainty in particulate_backscatter_e |
| `particulate_backscatter_e_uncertainty_systematic` | 1/(km*sr) | time,height_high | - | Systematic uncertainty in particulate_backscatter_e |


_2 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgprlproffexext1thorC1.c0",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgprlproffexext1thorC1.c0/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgprlproffexext1thorC1.c0", "2026-09-20", "2026-09-20")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgprlproffexext1thorC1.c0", "2026-09-20", "2026-09-20"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgprlproffexext1thorC1.c0", "20150225", "20260924")
```

The report's own note on quality: Estimates of random and systematic uncertainty are provided for all primary variables in rlproffex1thor.c0. Random uncertainties are derived from random noise in raw lidar signals (background noise from solar radiation, detector dark current, thermal noise, and shot noise) via standard error-propagation. Systematic uncertainties stem from errors in calibration constants, overlap corrections, and other configuration-file constants. detection_confidence_score_total and detection_confidence_score_random (0 to 1, with -1 for fully attenuated beam) indicate confidence that a bin is feature vs....

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Persistent low cloudiness frustrates accurate calibration | Poor or unstable calibration constants during extended low-cloud periods, degraded extinction/backscatter retrievals | Use feature mask, total confidence, QC bits and related flags to screen poor-quality data | (hb p. 17) |
| Poor system alignment reduces sensitivity | Lower signal-to-noise and reduced detection sensitivity in output profiles | None specified beyond general QC screening | (hb p. 17) |
| Changing alignment causes changing calibration that is difficult to track | Drifting or jumping calibration constants over time not attributable to a known cause | None specified | (hb p. 17) |
| Cloud and precipitation strong beam attenuation | High uncertainty values or low detection confidence scores below/within attenuating layers; detection_confidence_score_total set to -1 where beam completely attenuated | Use feature mask, confidence score, and QC flags to screen poor-quality data | (hb p. 17) |
| NFOV incomplete overlap at low altitude | NFOV channel signals strongly biased/unreliable below about 4 km due to incomplete beam-receiver FOV overlap | Use WFOV channels (complete overlap ~800 m) for lower-altitude retrievals; overlap functions estimated from raw RL data are applied | (hb p. 1) |
| WFOV higher sensitivity to solar background/radiation | Increased noise/background in WFOV channel signals, especially daytime; affects background_e/n2 and background_rms variables | None specified beyond noting NFOV has lower solar background sensitivity | (hb p. 1) |
| Feature mask value of 0 indicates invalid/no detection | feature_mask=0 samples should be treated as invalid rather than 'clear sky' | Treat zero feature_mask as invalid sample | (hb p. 8) |
| Overlapping/ambiguous source attribution in source_feature_mask | Some pixels show multiple bits set in source_feature_mask, indicating overlap between multiple detection sources | None specified beyond noting the overlap occurs | (hb p. 13) |
| Lack of independent validation | No direct ground-truth comparison; only limited comparisons to satellite observations available | Handbook states products are not validated directly with any observations because similar ground-based measurements are unavailable; will... | (hb p. 19) |
| Configuration files based on limited climatology (couple of years, annual only) | Systematic biases possible in extinction/backscatter under conditions not well represented by the short-term or annual-only climatology used for Angstrom exponent, aerosol size, cloud... | Plans to refine configuration files using long-term (greater than 10 years) data and seasonal climatology in future | (hb p. 18) |
| OLI (Oliktok Point) system stopped in 2019 and being updated for SEUS deployment | No FEX data available for OLI after October 2019; gap in that site's record | Instrument being updated for deployment at new SEUS site | (hb p. 1) |
| Historical pre-2015 SGP RL data collected with different system configurations | FEX VAP cannot currently be run on pre-2015 SGP data without additional processing effort | More resources and effort needed to process historical data; planned future work | (hb p. 18) |
| One-time calibration shift event at ENA (last week of December 2015) | Step change/discontinuity in long-term scattering ratio (elastic+N2) calibration constant time series in Dec 2015 | Attributed to known system update (voltage supply change); documented to have no impact on FEX outcomes | (hb p. 34) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Thorsen, TJ, Q Fu, RK Newsom, DD Turner, and JM Comstock. 2015. Automated retrieval of cloud and aerosol properties from the ARM Raman lidar. Part I: Feature detection. JTECH 32(11):1977-1998
- Thorsen, TJ, and Q Fu. 2015. Automated retrieval of cloud and aerosol properties from the ARM Raman lidar. Part II: Extinction. JTECH 32(11):1999-2023
- Whiteman, DN et al. 2006. Raman Water Vapor Lidar Measurements during the International H2O Project. I: Instrumentation and Analysis Techniques. JTECH 23(2):157-169
- Newsom, RK. 2009. Raman Lidar Handbook. DOE/SC-ARM/TR-038
- Newsom, RK. 2012. Raman Lidar Profiles Best Estimate Value-Added Products. DOE/SC-ARM/TR-100
- Newsom, RK, DD Turner, and JEM Goldsmith. 2013. Long-term evaluation of temperature profiles measured by an operational Raman lidar. JAOT 30(8):1616-1634
- Goldsmith JEM, FH Blair, SE Bisson, and DD Turner. 1998. Turn-key Raman lidar for profiling atmospheric water vapor, clouds and aerosols. Applied Optics 37(21):4979-4990
- Turner DD, RA Ferrare, LA Heilman Brasseur, WF Feltz, and TP Tooman. 2002. Automated retrievals of water vapor and aerosol profiles from an operational Raman lidar. JAOT 19(1):37-49
- Turner, DD, JEM Goldsmith, and RA Ferrare. 2016. Development and applications of the ARM Raman lidar. Meteorological Monograph 57
- Balmes, KA, Q Fu, and TJ Thorsen. 2019. Differences in ice cloud optical depth from CALIPSO and ground-based Raman lidar at the ARM SGP and TWP sites. JGR-Atmospheres 124(3):1755-1778

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-224.pdf (35 pages, DOE/SC-ARM-TR-224, by D Chand, R Newsom, R Bambha, E Cromwell, T Thorsen, J Comstock)
- Catalog record: ARM data-source index, `instrument_class_code=rlprof-fex`, read 2026-09-24
- Example file: `sgprlproffexext1thorC1.c0.20260920.000000.nc` from `sgprlproffexext1thorC1.c0`, 48.14 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
