---
name: arm-vap-xprecipcmac
description: ARM CSU X-Band Precip Radar (XPRECIPRADAR) PPI Corrected Moments to Antenna Coord (xprecipcmac) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Radial Doppler Velocity, Spectral Width, Differential Reflectivity, Differential Phase, Cross-Polar Correlation Ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (gucxprecipradarcmacppiS2.c1) and the variable inventory of a real file. Use when working with xprecipcmac data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - xprecipcmac, gucxprecipradarcmacppiS2.c1, Radial Doppler Velocity, Spectral Width, Differential Reflectivity, Differential Phase, Cloud Properties.
---

# XPRECIPCMAC - CSU X-Band Precip Radar (XPRECIPRADAR) PPI Corrected Moments to Antenna Coord

The CMAC value-added product applies gate-level scatterer identification, dealiasing, phase/attenuation correction, and rainfall/snowfall retrievals to Plan Position Indicator (PPI) scans from the CSU X-Band Precipitation Radar (XPRECIPRADAR) deployed during the SAIL field campaign to produce corrected moments in antenna coordinates.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 34 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `xprecipcmac` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR 313 / JR O'Brien, M Grover, RC Jackson, ZS Sherman, SM Collis, A Theisen, BA Raut, M Tuftedal, D Feldman / December 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-313.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2021-11-02 to 2023-06-16 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/xprecipcmac |


## Credit

Everything this skill knows about the retrieval is the work of **JR O'Brien, M Grover, RC Jackson, ZS Sherman, SM Collis, A Theisen, BA Raut, M Tuftedal, D Feldman** -
the ARM developers and mentors who wrote the technical report it derives from:

> JR O'Brien, M Grover, RC Jackson, ZS Sherman, SM Collis, A Theisen, BA Raut, M Tuftedal, D Feldman. *Colorado State University (CSU) X-Band Precipitation Radar Plan Position Indicator Data Processed with Corrected Moments in Antenna Coordinates (CMAC) Value-Added Product Report*, DOE/SC-ARM-TR 313, December 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-313.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

CMAC first performs a pre-correction "gate-ID" that classifies each radar gate (rain, melting layer, ice/snow, second/multi-trip, terrain blockage, no significant scatterer) using fuzzy logic membership functions built from texture of radial velocity (computed via directional/circular statistics to avoid false texture on Doppler folds), co-polar correlation coefficient (rho_HV), normalized coherent power (NCP/SQI), interpolated sounding temperature, height, and SNR. This classification, done before any corrections are applied, is used to construct Py-ART Gatefilter objects that determine which downstream algorithms run on which gates (e.g., dealiasing on all but no-significant-return; specific attenuation retrieval only on rain). Doppler velocities are dealiased using region-based (or fringe/phase-based) unfolding, with a secondary step fitting integer multiples of the Nyquist velocity to rawinsonde wind profiles via a cost-function minimization. Raw differential phase (PsiDP = PhiDP + delta + NBF) is filtered using a Linear Programming (LP) technique to retrieve a monotonically increasing PhiDP, from which specific differential phase (KDP) is derived via a Sobel-filter convolution; specific attenuation and specific differential attenuation are retrieved using an iterative "hotspot" method, and applied to correct reflectivity and Zdr for two-way liquid water path attenuation.

**Cadence.** averaging 3x3 kernel commonly used for texture moving filter (hb p. 12).

## Inputs

The report names these instruments and sibling products: X-Band and C-Band Scanning ARM Precipitation Radars (X/CSAPRs), Ka-Band ARM Zenith Radar (KAZR), millimeter wavelength cloud radar (MMCR), Laser Disdrometer Quantities Value-Added Product (LDQUANTS), Pluvio2 weighing bucket rain gauge, interpolated sonde product.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Equivalent radar reflectivity factor (DBZ) | dBZ | - | - | (hb p. 26) |
| Radial Doppler Velocity (VEL) | m/s | - | - | (hb p. 26) |
| Spectral Width (WIDTH) | m/s | - | - | (hb p. 27) |
| Differential Reflectivity (ZDR) | dB | - | - | (hb p. 27) |
| Differential Phase (PHIDP) | degree | - | - | (hb p. 27) |
| Cross-Polar Correlation Ratio (RHOHV) | 1 | - | - | (hb p. 27) |
| Normalized Coherent Power (NCP/SQI) | 1 | - | - | (hb p. 27) |
| Equivalent Reflectivity Factor HV (DBZhv) | dBZ | - | - | (hb p. 27) |
| Cumulative Beam Block Fraction Flag (cbb_flag) | 1 | - | - | (hb p. 27) |
| Interpolated sounding temperature | degC | - | - | (hb p. 27) |
| Height of radar beam | m | - | - | (hb p. 28) |
| Signal to Noise Ratio | dB | - | - | (hb p. 28) |
| Velocity texture (mean doppler velocity variance metric) | m/s | - | - | (hb p. 28) |
| Gate classification of dominant scatterer (gate_id) | 1 | valid_min 0, valid_max 6 | - | (hb p. 28) |
| Simulated mean doppler velocity | m/s | - | - | (hb p. 28) |
| Corrected mean doppler velocity | m/s | valid_min -79.5, valid_max 79.5 | - | (hb p. 28) |
| Unfolded differential propagation phase shift | degree | - | - | (hb p. 28) |
| Corrected differential propagation phase shift | degree | valid_min 0.0, valid_max 400.0 | - | (hb p. 29) |
| Filtered Corrected Differential Phase | degree | valid_min 0.0, valid_max 400.0 | - | (hb p. 29) |
| Specific differential phase (KDP) | degrees/km | - | - | (hb p. 29) |
| Filtered Corrected Specific differential phase (KDP) | degrees/km | - | - | (hb p. 29) |
| Corrected differential reflectivity | dB | - | - | (hb p. 29) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| meters_to_center_of_first_gate | -112.6891 | (hb p. 26) |
| meters_between_gates | 59.94095 | (hb p. 26) |
| range dimension | 668 | (hb p. 26) |
| sweep dimension | 8 | (hb p. 26) |
| KDP filter threshold for clutter mitigation | filter out all Kdp greater than 15 degree/km-1 | (hb p. 18) |
| Beam blockage classification threshold | gates with more than 30% beam blockage flagged as terrain blockage | (hb p. 20) |
| XSAPR/CSAPR aliasing velocities (baseline mode) | 12.4 and 16.52 m/s | (hb p. 9) |
| swe_ratio (snow rate variables) | 13.699 | (hb p. 30) |


## The data

Verified example: **`gucxprecipradarcmacppiS2.c1`**, file `gucxprecipradarcmacppiS2.c1.20230613.083408.nc`
(334.27 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=9232, `range`=668, `sweep`=8 |
| Data variables | 46 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2023-06-13T08:34:08 to 2023-06-13T08:38:23 |
| dod version | xprecipradarcmacppi-c1-2.0 |
| process version | CMAC |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `DBZ` | dBZ | time,range | - | Equaivalent_radar_reflectiivity_factor |
| `DBZhv` | dBZ | time,range | - | Equivalent Reflectivity Factor HV |
| `NCP` | 1 | time,range | - | Normalized Coherent Power, also known as SQI |
| `PHIDP` | degree | time,range | - | Differential Phase |
| `RHOHV` | 1 | time,range | - | Cross-Polar Correlation Ratio |
| `VEL` | m/s | time,range | - | Radial Doppler Velocity, Positive for Motion Away from Instrument |
| `WIDTH` | m/s | time,range | - | Spectral Width |
| `ZDR` | dB | time,range | - | Differential Reflectivity |
| `azimuth` | degree | time | - | Azimuth Angle from True North |
| `cbb_flag` | 1 | time,range | - | Cumulative Beam Block Fraction Flag |
| `corrected_differential_phase` | degree | time,range | - | Corrected differential propagation phase shift |
| `corrected_differential_reflectivity` | dB | time,range | - | Corrected differential reflectivity |
| `corrected_reflectivity` | dBZ | time,range | - | Corrected reflectivity |
| `corrected_specific_diff_phase` | degrees/km | time,range | - | Specific differential phase (KDP) |
| `corrected_velocity` | m/s | time,range | - | Corrected mean doppler velocity |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `filtered_corrected_differential_phase` | degree | time,range | - | Filtered Corrected Differential Phase |
| `filtered_corrected_specific_diff_phase` | degrees/km | time,range | - | Filtered Corrected Specific differential phase (KDP) |
| `fixed_angle` | degree | sweep | - | Ray Target Fixed Angle |
| `gate_id` | 1 | time,range | - | Classification of dominant scatterer |
| `height` | m | time,range | - | Height of radar beam |
| `height_over_iso0` | m | time,range | - | Height of radar beam over freezing level |
| `nyquist_velocity` | m/s | time | - | Nyquist velocity |
| `path_integrated_attenuation` | dB | time,range | - | Path Integrated Attenuation |
| `path_integrated_differential_attenuation` | dB | time,range | - | Path Integrated Differential Attenuation |
| `rain_rate_A` | mm/hr | time,range | - | Rainfall Rate from Specific Attenuation |
| `range` | meter | range | - | Range to measurement volume |
| `signal_to_noise_ratio` | dB | time,range | - | Signal to Noise Ratio |
| `simulated_velocity` | m/s | time,range | - | Simulated mean doppler velocity |
| `snow_rate_m2009_1` | mm/h | time,range | - | Snowfall rate from Z using Matrosov et al.(2009) Braham(1990) 1 |


_17 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("gucxprecipradarcmacppiS2.c1", "2023-06-13", "2023-06-13")
ds = armlive_open("gucxprecipradarcmacppiS2.c1", "2023-06-13", "2023-06-13", cleanup_qc=True)
```

This product carries 46 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("gucxprecipradarcmacppiS2.c1", start, end,
                  keep_variables=['DBZ', 'DBZhv', 'NCP'])
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `cbb_flag`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("gucxprecipradarcmacppiS2.c1", "20211102", "20260924")
```

The report's own note on quality: Gate-ID (scatterer classification: multi_trip, rain, snow, no_scatter, melting, clutter, terrain_blockage) is computed pre-correction using fuzzy logic membership functions (Table 1) on texture of radial velocity, rho_HV, NCP, sounding temperature, height, and SNR, and is used to build Py-ART Gatefilter objects controlling which correction algorithms run on which gates. The gate_id variable has flag_values 0-6 with flag_meanings multi_trip, rain, snow, no_scatter, melting, clutter, terrain_blockage. Global attribute "known_issues" states: "False phidp jumps in insect regions. Still uses old...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Second/multiple-trip echoes (range aliasing) due to magnetron pulse-to-pulse phase... | Flat, low-NCP Doppler spectrum and randomly varying radial velocity gate-to-gate/azimuth-to-azimuth between -Vnyq and Vnyq in regions dominated by second-trip returns; visible as high... | Use gate-ID (fuzzy logic classification using texture, rho_HV, NCP, temperature, height, SNR) to flag multi-trip gates before applying corrections | (hb p. 9) |
| NCP alone unreliable for second-trip detection in high spectral width regions | NCP decreases even in purely first-trip regions of high convergence/divergence in convective storms, causing false flagging as multi-trip/no-scatter | Do not rely on NCP alone; use combined fuzzy-logic gate-ID with multiple inputs (texture, rho_HV, NCP, temperature, height, SNR) | (hb p. 9) |
| Doppler velocity aliasing/folding | Radial velocity wraps at +/- Nyquist velocity (12.4 or 16.52 m/s in baseline mode for XSAPR/CSAPR); raw velocity field shows discontinuous jumps at fold boundaries | Region-based (or fringe/phase-based) dealiasing; secondary step minimizes a cost function fitting integer multiples of Vnyq to rawinsonde wind field | (hb p. 9) |
| False texture signal from Doppler folding if computed directly on radial velocity | Spurious high-texture values along fold boundaries when texture calculated on raw (non-circular) velocity values | Project radial velocity onto unit circle (directional/circular statistics) before computing texture (standard deviation via R and S formulas) | (hb p. 12) |
| Choice of texture cutoff threshold depends on many site/instrument factors | Histogram of texture values shows two distinct populations (significant vs. non-significant) whose separation point can shift with number of samples and SNR | Use continuous wavelet transform-based peak-finding (Du et al. 2006) to locate left/right peaks and choose the valley/minimum between them as cutoff | (hb p. 13) |
| Fringe/phase-based dealiasing technique underperformance | Early tests were sub-par compared to region-based approach | Technique retained in Py-ART but rarely used; region-based technique preferred | (hb p. 8) |
| Residual Nyquist-interval offset after initial dealiasing | Some velocities remain off by an integer factor of the Nyquist velocity after unfolding/merging regions | Second step minimizes cost function J comparing regional mean velocity to rawinsonde wind field to find correct integer offset | (hb p. 8) |
| Non-uniform beam filling (NBF) and phase shift on backscatter (delta) contaminate... | Raw PsiDP includes NBF and delta components on top of true propagation phase PhiDP, causing non-monotonic or noisy phase profiles | Linear Programming (LP) technique fits a piecewise increasing, non-biased PhiDP through the base of short-term variations, weighted weakly by local... | (hb p. 9) |
| Clutter contamination of PhiDP calculation | Occasional clutter throws off phi_dp calculation, apparent as anomalous spikes in Kdp and specific attenuation (A) fields | Filter out all Kdp greater than 15 degree km-1 | (hb p. 10) |
| Attenuation due to ice/mixed-phase not accounted for in specific attenuation retrieval | Specific attenuation (A) only calculated in liquid precipitation gates; ice-phase attenuation assumed negligible, mixed-phase considered intractable | Gate filter restricts A calculation to gates classified as rain | (hb p. 10) |
| Uncalibrated reflectivity bias requiring offset correction | Raw radar reflectivity differs from disdrometer-derived reference, visible as a systematic offset before correction | Apply reflectivity offset via comparison to disdrometer measurement (interim solution); future plan is end-to-end calibrated data | (hb p. 10) |
| Differential attenuation affecting Zdr at C- and X-band | Uncorrected Zdr shows bias/attenuation artifacts across a PPI scan, especially through heavy precipitation cores | Retrieve specific differential attenuation using Gu et al. (2011) method (code contributed by J. Figueras e Ventura) and correct Zdr for bias and... | (hb p. 11) |
| Beam blockage from complex terrain (mountains south of radar during SAIL) | Reduced power return, underestimated reflectivity, or blind spots at low elevation angles in southern coverage sector; cumulative beam blockage fraction map shows values approaching 1.0... | Generate beam-blockage maps per elevation angle with wradlib; flag gates with greater than 30% cumulative beam blockage as terrain_blockage class in... | (hb p. 11) |
| Uncertainty in snowfall rate retrievals due to hydrometeor diversity | Spread among four different Ze-S empirical relationship curves applied to the same reflectivity field, producing a range of snowfall rate estimates for the same event | Apply an ensemble of four empirical Ze=aS^b relationships (Wolfe & Snider 2012, WSR-88D High Plains, Braham 1990 x2) rather than a single... | (hb p. 12) |
| Attenuation-based rainfall estimates (R(A)) underestimate rainfall in drizzle/warm-phase... | CMAC attenuation-based rain rate systematically lower than Pluvio2 weighing bucket gauge and LDQUANTS accumulations for 15-min/30-min/1-hr comparisons in August 2022, especially during... | Use CMAC reflectivity-based (R(Z)) rainfall estimates instead of attenuation-based for warm-phase precipitation during SAIL | (hb p. 21) |
| Clutter detection and tagging incomplete / anomalous propagation exacerbates clutter | Residual clutter returns not fully flagged, especially as convective systems cool and moisten the boundary layer (ducting/anomalous propagation) | Ongoing work using mean/variance of reflectivity in non-precipitating regions to diagnose clutter; not yet resolved | (hb p. 15) |
| LP technique underperformance in regions of extended differential phase on backscatter... | Retrieved PhiDP/KDP degrade in quality in regions with extended delta_dp | Authors have a theoretical solution but it is difficult to implement with currently supported LP packages; actively being worked on | (hb p. 15) |
| False PhiDP jumps in insect-contaminated regions | Sudden jumps in differential phase field co-located with biological/insect scatterer regions | None specified beyond noting the known issue | (hb p. 33) |
| Data uses old Giangrande LP code with known issues in some snow below the melting layer | Snow classification/retrieval below melting layer may be inaccurate | None specified; flagged as known issue | (hb p. 33) |
| Product labeled highly experimental with many known and unknown issues | Data quality inconsistent across cases; global attribute explicitly warns users | Contact the Translator (scollis@anl.gov) before use | (hb p. 33) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- James and Houze 2001 (4DD dealiasing)
- Giangrande and Ryzhkov 2008 (rainfall estimation via polarimetric echo classification / phase filtering)
- Giangrande, McGraw, and Lei 2013 (Linear Programming for differential phase processing)
- Gu et al. 2011 (Polarimetric Attenuation Correction in Heavy Rain at C Band)
- Bukovčić et al. 2018 (Polarimetric Radar Relations for Quantification of Snow)
- Gourley et al. 2007 (Fuzzy logic separation of precipitating from nonprecipitating echoes)
- Bringi et al. 2002 (Gamma raindrop size distribution parameter estimation)
- Helmus and Collis 2016 (Py-ART)
- Heistermann et al. 2014 (Open source software for weather radar community)
- Kollias et al. 2013 (Scanning ARM Cloud Radars Part II)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-313.pdf (34 pages, DOE/SC-ARM-TR 313, by JR O'Brien, M Grover, RC Jackson, ZS Sherman, SM Collis, A Theisen, BA Raut, M Tuftedal, D Feldman)
- Catalog record: ARM data-source index, `instrument_class_code=xprecipcmac`, read 2026-09-24
- Example file: `gucxprecipradarcmacppiS2.c1.20230613.083408.nc` from `gucxprecipradarcmacppiS2.c1`, 334.27 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
