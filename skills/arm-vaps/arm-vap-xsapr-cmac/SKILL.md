---
name: arm-vap-xsapr-cmac
description: ARM X-SAPR Corrected Moments in Antenna Coordinates (xsapr-cmac) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Total power, Reflectivity, Mean Doppler velocity, Doppler spectrum width, Differential reflectivity, Specific differential phase), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with xsapr-cmac data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Derived Quantities and Models. Triggers - xsapr-cmac, X-SAPR Corrected Moments in Antenna Coordinates, nsaxsaprcmacppiC1.c1, Total power, Reflectivity, Mean Doppler velocity, Doppler spectrum width.
---

# XSAPR-CMAC - X-SAPR Corrected Moments in Antenna Coordinates

CMAC is an ARM value-added product that applies a chain of gate-classification, dealiasing, phase-filtering, and attenuation-correction algorithms to raw moments and polarimetric measurements from the X-band and C-band Scanning ARM Precipitation Radars (X/CSAPR) to produce corrected, geophysically meaningful radar moments in antenna (range/azimuth/elevation) coordinates.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 38 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `xsapr-cmac` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-283 / SM Collis, JJ Helmus, ZS Sherman, RC Jackson / November 2022](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-283.pdf) |
| Category | Cloud Properties; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2017-07-31 to 2020-09-24 (retired) |
| Datastreams with data | 8 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/xsapr-cmac |


## Credit

Everything this skill knows about the retrieval is the work of **SM Collis, JJ Helmus, ZS Sherman, RC Jackson** -
the ARM developers and mentors who wrote the technical report it derives from:

> SM Collis, JJ Helmus, ZS Sherman, RC Jackson. *Corrected Moments in Antenna Coordinates (CMAC) X-SAPR Technical Report*, DOE/SC-ARM-TR-283, November 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-283.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The application chain first performs pre-identification calculations, mapping interpolated sounding temperature to radar gates and computing the texture (variance) of radial velocity using circular/directional statistics to avoid false texture from Doppler folding. A fuzzy-logic scheme with trapezoidal membership functions then scores each range gate against classes (melting layer, multi-trip, rain, snow, no significant scatterer) using texture, cross-correlation ratio (rhoHV), normalized coherent power (NCP/SQI), temperature, height, and SNR, producing a gate ID used to build a Py-ART Gatefilter that conditionally routes subsequent corrections. Doppler velocities are dealiased using region-based (or fringe-pattern) unfolding followed by an integer-Nyquist correction minimized against sounding winds. Measured differential phase (PsiDP = PhiDP + delta + NBF) is filtered using a linear-programming (LP) technique to retrieve a monotonically increasing PhiDP, from which specific differential phase (KDP) is derived via a Sobel-like linear ramp convolution; specific attenuation and specific differential attenuation are retrieved via an iterative hotspot method and applied to correct reflectivity and differential reflectivity for two-way liquid water path attenuation.

**Cadence.** averaging 3x3 kernel commonly used for texture calculation over range gates of adjacent rays (hb p. 11).

## Inputs

The report names these instruments and sibling products: CSAPR (C-band Scanning ARM Precipitation Radar), KAZR (Ka-band ARM Zenith Radar), MMCR (millimeter wavelength cloud radar), INTERPSONDE (Interpolated Sonde Value-Added Product).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Total power | dBZ | - | - | (hb p. 22) |
| Reflectivity | dBZ | - | - | (hb p. 23) |
| Mean Doppler velocity | m/s | - | - | (hb p. 23) |
| Doppler spectrum width | m/s | - | - | (hb p. 23) |
| Differential reflectivity (Zdr) | dB | - | - | (hb p. 23) |
| Specific differential phase (KDP) | degrees/km | - | - | (hb p. 24) |
| Cross correlation ratio (RHOHV) | 1 | valid_min 0. to valid_max 1. | - | (hb p. 24) |
| Normalized coherent power (SQI) | 1 | valid_min 0. to valid_max 1. | - | (hb p. 24) |
| Differential phase (PhiDP) | degrees | valid_min -180. to valid_max 180. | - | (hb p. 25) |
| Ground clutter flag | 1 | 0 or 1 | - | (hb p. 25) |
| Sounding temperature (interpolated profile) | degC | - | - | (hb p. 25) |
| Height of radar beam | m | - | - | (hb p. 25) |
| Signal to noise ratio | dB | - | - | (hb p. 25) |
| Velocity texture | m/s | - | - | (hb p. 26) |
| Gate ID (classification of dominant scatterer) | 1 | flag values 0-5 | - | (hb p. 26) |
| Simulated mean Doppler velocity | m/s | - | - | (hb p. 26) |
| Corrected mean Doppler velocity | m/s | valid_min -32.085 to valid_max... | - | (hb p. 27) |
| Unfolded differential propagation phase shift | degree | valid_min -180. to valid_max 180. | - | (hb p. 27) |
| Corrected differential propagation phase shift | degree | valid_min 0. to valid_max 400. | - | (hb p. 27) |
| Filtered corrected differential phase | - | valid_min 0. to valid_max 400. | - | (hb p. 27) |
| Corrected specific differential phase (KDP) | degrees/km | - | - | (hb p. 28) |
| Filtered corrected specific differential phase (KDP) | degrees/km | - | - | (hb p. 28) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| range dimension | 1001 gates | (hb p. 21) |
| sweep dimension | 12 | (hb p. 21) |
| range:meters_to_center_of_first_gate | 0.f | (hb p. 22) |
| range:meters_between_gates | 100.f | (hb p. 22) |
| XSAPR/CSAPR Doppler aliasing velocity (baseline mode) | 12.4 and 16.52 m/s (X and C band respectively) | (hb p. 9) |
| KDP clutter filter threshold | filter out all Kdp greater than 15 deg/km-1 | (hb p. 16) |
| corrected_velocity valid range | -32.085 to 32.085 (units 'm/s') | (hb p. 27) |
| differential_phase valid range | -180. to 180. (degrees) | (hb p. 25) |
| corrected_differential_phase valid range | 0. to 400. (degrees) | (hb p. 27) |
| specific_attenuation valid range | 0. to 1. (dB/km) | (hb p. 29) |
| rain_rate_A valid range | 0. to 400. (mm/hr) | (hb p. 30) |
| Conventions | CF/Radial 1.4 | (hb p. 35) |
| DOI | 10.5439/1573362 | (hb p. 35) |


## The data

**No example file was verified for this instrument.** two separate files from this product both failed to open with an HDF error, so nothing could be inventoried.

ARM's catalog lists 8 datastreams with data across 2 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "nsaxsaprcmacppiC1.c1", "start": start, "end": end,
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
                     params={"user": f"{user}:{token}", "ds": "nsaxsaprcmacppiC1.c1",
                             "start": "2020-09-24", "end": "2020-09-24", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsaxsaprcmacppiC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsaxsaprcmacppiC1.c1", "2020-09-24", "2020-09-24")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsaxsaprcmacppiC1.c1", "2020-09-24", "2020-09-24"))   # cite what you pulled
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you have a
file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("nsaxsaprcmacppiC1.c1", "20170731", "20260924")
```

The report's own note on quality: Gate ID (scatterer classification: rain, melting layer, ice/snow, second trip, terrain blockage, no significant scatterer, clutter) is computed on pre-corrected data using fuzzy-logic membership functions (Table 1) on texture, rhoHV, NCP, temperature, height, and SNR, and is used to build a Py-ART Gatefilter that conditionally gates which correction/retrieval algorithms are applied at each range gate. A ground_clutter flag (0=No Clutter,1=Clutter) is also provided. The output file's global 'comment' attribute states the data is 'highly experimental and initial data' with 'many known and...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Second-trip (multiple-trip) echo contamination | Flat, low normalized coherent power (NCP) in second-trip regions from magnetron pulse-to-pulse phase randomization; appears as a distinct 'multi_trip' class in gate_id and can corrupt... | Gate ID (fuzzy logic classification using texture, rhoHV, NCP, temperature, height, SNR) run before corrections to flag and exclude multi-trip gates... | (hb p. 9) |
| NCP breakdown in high spectral-width regions | NCP falsely decreases (approaching second-trip-like low values) in regions of high convergence/divergence in convective storms even though returns are first-trip, causing false flagging | Use gate ID scheme combining multiple discriminants (texture, rhoHV, temperature, height, SNR) rather than NCP alone | (hb p. 9) |
| Doppler velocity aliasing (folding) | Raw radial velocity shows abrupt jumps/wraps between +/-Vnyq (12.4 m/s for X-band, 16.52 m/s for C-band in baseline mode), especially in intense convection | Region-based dealiasing algorithm implemented in Py-ART; secondary integer-Nyquist correction minimizes cost function against sounding wind field | (hb p. 9) |
| Doppler fringe-based dealiasing underperformance | Sub-par results when applying the fringe/phase-based image analysis dealiasing technique | Rarely used in practice; region-based technique preferred | (hb p. 7) |
| False texture on Doppler folds if computed naively | Spurious high-texture values appear at velocity fold boundaries in the velocity-texture field | Project radial velocity onto unit circle using circular/directional statistics before computing texture | (hb p. 3) |
| Ambiguity in texture threshold for significant-return discrimination | Histogram of texture values shows two populations (significant vs. noise) whose separation point varies with sample number and SNR | Use continuous wavelet transform-based peak-finding to locate left/right peaks and set cutoff at the valley minimum between them | (hb p. 4) |
| Non-uniform beam filling (NBF) and backscatter phase shift contamination of PhiDP | Measured PsiDP includes NBF and backscatter differential phase (delta) components superimposed on the true propagation phase signal, causing noisy or non-monotonic raw PhiDP | Linear programming (LP) technique retrieves a piecewise-increasing, unbiased PhiDP that fits through the base of short-term variation rather than... | (hb p. 15) |
| LP technique underperformance in regions of extended differential backscatter phase... | KDP and PhiDP retrievals degrade in quality where delta_dp is extended, as identified by Giangrande and Ryzhkov (2008) | Authors note a solution exists but is difficult to implement with currently supported LP packages; actively being worked on | (hb p. 21) |
| Clutter contamination affecting PhiDP, KDP, and specific attenuation | Clutter can throw off phi_dp calculation, visible as anomalies in the KDP and specific-attenuation (A) fields | Filter out all KDP values greater than 15 deg/km-1 | (hb p. 16) |
| Ground clutter near and beyond the radar | Elevated/erroneous reflectivity and velocity near the radar and at some ranges further out, flagged in ground_clutter variable (0=no clutter,1=clutter) | Pipeline clutter near the radar largely removed; clutter identification/tagging further out from radar is still an active challenge (work in progress) | (hb p. 12) |
| Attenuation of X- and C-band signal by liquid water path | Reflectivity and Zdr are systematically reduced/biased with increasing range through precipitation because ARM opted not to use attenuation-robust S-band; visible as underestimated... | Specific attenuation retrieved via iterative hotspot method (Gu et al. 2011) and applied cumulatively to correct reflectivity; specific differential... | (hb p. 9) |
| Zdr calibration bias at ARM SGP XSAPR radars (May-Sept 2018) | Significant Zdr biases observed across all XSAPR radars at SGP during May-Sept 2018 period, varying between individual scans with no stable offset | No confident Zdr calibration could be applied; all corrected Zdr data for this period/site are masked and unavailable; raw Zdr included but users... | (hb p. 18) |
| Scan-strategy inconsistency between files | At NSA, scan configuration changed between every other file, causing every-other-file's gate identification to be incorrect | Affected data was identified, rerun, and fixed; future work planned to better handle differing scan strategies within CMAC | (hb p. 21) |
| Sea ice and stationary ground objects (e.g., oil pipelines) misclassified as scatterers | Spurious 'no scatter'/clutter or false returns at NSA site associated with sea ice or pipeline infrastructure | Improved filtering identified as future work; not yet fully resolved | (hb p. 21) |
| Fuzzy-logic scheme confusion between noise and second-trip echoes | Gate ID misclassification between 'no_scatter' and 'multi_trip' classes in ambiguous SNR/texture regimes | Adjustments to the fuzzy logic algorithm identified as needed future work | (hb p. 21) |
| Hail contamination of polarimetric propagation path (not yet handled) | Gates along a radial contaminated by hail are not currently flagged as a distinct class, potentially degrading KDP/attenuation retrievals in hail cores | Future plans to include hail-contaminated gate classification; work in progress at time of writing | (hb p. 5) |
| Experimental/preliminary data quality | Output files self-describe processing as highly experimental with many known and unknown issues | Handbook advises contacting the Translator responsible (scollis@anl.gov) before use | (hb p. 27) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Giangrande, SE, and AV Ryzhkov. 2008. Journal of Applied Meteorology and Climatology 47(9): 2445-2462.
- Giangrande, SE, R McGraw, and L Lei. 2013. Journal of Atmospheric and Oceanic Technology 30(8): 1716-1729.
- Gu, JY, A Ryzhkov, P Zhang, P Neilley, M Knight, B Wolf, and DI Lee. 2011. Journal of Applied Meteorology and Climatology 50(1): 39-58.
- James, CN, and RA Houze. 2001. Journal of Atmospheric and Oceanic Technology 18(10): 1674-1683.
- Bringi, VN, GJ Huang, V Chandrasekar, and E Gorgucci. 2002. Journal of Atmospheric and Oceanic Technology 19(5): 633-645.
- Gourley, JJ, P Tabary, and J Parent du Chatelet. 2007. Journal of Atmospheric and Oceanic Technology 24(8): 1439-1451.
- Helmus, JJ, and SM Collis. 2016. Journal of Open Research Software 4(1): e25.
- Kollias, P, et al. 2013. Journal of Atmospheric and Oceanic Technology 31(3): 583-598.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-283.pdf (38 pages, DOE/SC-ARM-TR-283, by SM Collis, JJ Helmus, ZS Sherman, RC Jackson)
- Catalog record: ARM data-source index, `instrument_class_code=xsapr-cmac`, read 2026-09-24
- Example file: none - two separate files from this product both failed to open with an HDF error, so nothing could be inventoried
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
