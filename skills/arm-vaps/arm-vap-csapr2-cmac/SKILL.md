---
name: arm-vap-csapr2-cmac
description: ARM C-SAPR2 Corrected Moments in Antenna Coordinates (csapr2-cmac) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (copol_correlation_coeff, differential_phase, differential_reflectivity, mean_doppler_velocity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (houcsapr2cmacS2.c1) and the variable inventory of a real file. Use when working with csapr2-cmac data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Derived Quantities and Models. Triggers - csapr2-cmac, C-SAPR2 Corrected Moments in Antenna Coordinates, houcsapr2cmacS2.c1, copol_correlation_coeff, differential_phase, differential_reflectivity, Cloud Properties, Derived Quantities and Models.
---

# CSAPR2-CMAC - C-SAPR2 Corrected Moments in Antenna Coordinates

CMAC is an ARM value-added product that applies dealiasing, attenuation correction, multi-trip and clutter identification, and other corrections to the raw moments from the ARM X-band and C-band Scanning Precipitation Radars (including CSAPR2), producing corrected radar moments in antenna (Cf/Radial) coordinates.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 35 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `csapr2-cmac` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-327 / SM Collis, JJ Helmus, ZS Sherman, RC Jackson, B Raut, J O’Brien, M Grover, Y Feng, A Theisen / April 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-327.pdf) |
| Category | Cloud Properties; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2018-10-12 to 2025-06-26 (retired) |
| Datastreams with data | 4 across 3 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/csapr2-cmac |


## Credit

Everything this skill knows about the retrieval is the work of **SM Collis, JJ Helmus, ZS Sherman, RC Jackson, B Raut, J O’Brien, M Grover, Y Feng, A Theisen** -
the ARM developers and mentors who wrote the technical report it derives from:

> SM Collis, JJ Helmus, ZS Sherman, RC Jackson, B Raut, J O’Brien, M Grover, Y Feng, A Theisen. *Corrected Moments in Antenna Coordinates (CMAC) Technical Report*, DOE/SC-ARM-TR-327, April 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-327.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

CMAC first performs a gate-ID step on pre-corrected radar moments (reflectivity, texture of radial velocity, rhoHV, NCP, interpolated sounding temperature) using fuzzy logic membership functions to classify each gate as rain, melting layer, ice/snow, second trip, terrain blockage, clutter, or no significant scatterer, since raw measurements alone cannot constrain the problem, especially multiple-trip identification. Based on this classification, an application chain conditionally applies algorithms: region-based Doppler velocity dealiasing, linear-programming-based filtering of the measured differential phase (PsiDP) into propagation phase (PhiDP) plus non-uniform beam filling and backscatter phase terms, calculation of specific differential phase (KDP) by convolving PhiDP with a 20-point linear ramp, retrieval of specific attenuation via an iterative hotspot method, and Zdr bias/differential attenuation correction. Texture of radial velocity is computed using directional (circular) statistics, projecting velocities onto a unit circle to avoid false texture at Doppler folds, and a valley-finding algorithm on the resulting bimodal histogram sets the significant-return threshold. The output moments (dealiased velocity, corrected PhiDP/KDP, corrected reflectivity, corrected Zdr) represent an attempt to recover the 'intrinsic' value of each measurement corrected for propagation and processing artifacts.

## Inputs

The report names these instruments and sibling products: CSAPR, CSAPR2, XSAPR, KAZR, MMCR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| attenuation_corrected_differential_reflectivity | dB | - | - | (hb p. 21) |
| attenuation_corrected_reflectivity_h | dBZ | - | - | (hb p. 21) |
| copol_correlation_coeff (rhohv) | 1 | - | - | (hb p. 22) |
| differential_phase | degree | - | - | (hb p. 22) |
| differential_reflectivity | dB | - | - | (hb p. 22) |
| mean_doppler_velocity | m/s | - | - | (hb p. 22) |
| normalized_coherent_power (SQI) | 1 | - | - | (hb p. 23) |
| reflectivity | dBZ | - | - | (hb p. 23) |
| signal_to_noise_ratio_copolar_h | dB | - | - | (hb p. 23) |
| specific_attenuation | dB/km | valid_min 0.0 to valid_max 1.0 | - | (hb p. 24) |
| specific_differential_attenuation | dB/km | - | - | (hb p. 24) |
| specific_differential_phase (KDP) | degree/km | - | - | (hb p. 24) |
| spectral_width | m/s | - | - | (hb p. 24) |
| corrected_velocity | m/s | valid_min -49.476 to valid_max... | - | (hb p. 27) |
| corrected_differential_phase | degree | valid_min 0.0 to valid_max 400.0 | - | (hb p. 27) |
| corrected_specific_diff_phase (KDP) | degree/km | - | - | (hb p. 28) |
| corrected_differential_reflectivity | dB | - | - | (hb p. 28) |
| corrected_reflectivity | dBZ | - | - | (hb p. 28) |
| rain_rate_A | mm/hr | valid_min 0.0 to valid_max 400.0 | - | (hb p. 28) |
| path_integrated_attenuation | dB | - | - | (hb p. 28) |
| path_integrated_differential_attenuation | dB | - | - | (hb p. 28) |
| gate_id | 1 | valid_min 0 to valid_max 6 | - | (hb p. 27) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| nsweeps | 15 | (hb p. 29) |
| ngates | 1100 | (hb p. 29) |
| nrays | 76 | (hb p. 29) |
| meters_between_gates | 100.0 | (hb p. 29) |
| meters_to_center_of_first_gate | 50.0 | (hb p. 29) |
| scan_type | rhi | (hb p. 30) |
| gate_id valid range | valid_min 0, valid_max 6 | (hb p. 27) |
| corrected_velocity valid range | valid_min -49.476, valid_max 49.476 m/s | (hb p. 27) |
| corrected_differential_phase valid range | valid_min 0.0, valid_max 400.0 degree | (hb p. 27) |
| rain_rate_A valid range | valid_min 0.0, valid_max 400.0 mm/hr | (hb p. 28) |
| specific_attenuation valid range | valid_min 0.0, valid_max 1.0 dB/km | (hb p. 24) |
| XSAPR/CSAPR baseline aliasing velocity | 12.4 and 16.52 m s-1 | (hb p. 9) |
| KDP clutter filter threshold | filter out all Kdp greater than 15 deg km-1 | (hb p. 17) |


## The data

Verified example: **`houcsapr2cmacS2.c1`**, file `houcsapr2cmacS2.c1.20220928.074553.nc`
(336.58 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1081, `range`=1100, `sweep`=15 |
| Data variables | 75 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2022-09-28T07:45:53 to 2022-09-28T07:47:42 |
| dod version | csapr2cmac-c1-1.1 |
| process version | vap-cmaccsapr2-0.0-0.dev0.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `attenuation_corrected_differential_reflectivity` | dB | time,range | - | Rainfall attenuation-corrected differential reflectivity |
| `attenuation_corrected_differential_reflectivity_lag_1` | dB | time,range | - | Differential reflectivity estimated at lag 1 corrected for rainfall... |
| `attenuation_corrected_reflectivity_h` | dBZ | time,range | - | Rainfall attenuation-corrected reflectivity, horizontal channel |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `classification_mask` | 1 | time,range | - | Classification Mask |
| `clutter_masked_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `copol_correlation_coeff` | 1 | time,range | - | Copolar correlation coefficient (also known as rhohv) |
| `corrected_differential_phase` | degree | time,range | - | Corrected Differential Phase |
| `corrected_differential_reflectivity` | dB | time,range | - | Corrected differential reflectivity |
| `corrected_reflectivity` | dBZ | time,range | - | Corrected reflectivity |
| `corrected_specific_diff_phase` | degree/km | time,range | - | Corrected Specific differential phase (KDP) |
| `corrected_velocity` | m/s | time,range | - | Corrected mean doppler velocity |
| `cumulative_beam_blockage` | 1 | time,range | - | Cumulative Beam Block Fraction |
| `differential_phase` | degree | time,range | - | Differential propagation phase shift |
| `differential_reflectivity` | dB | time,range | - | Differential reflectivity |
| `differential_reflectivity_lag_1` | dB | time,range | - | Differential reflectivity estimated at lag 1 |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `filtered_corrected_differential_phase` | degree | time,range | - | Filtered Corrected Differential Phase |
| `filtered_corrected_specific_diff_phase` | degree/km | time,range | - | Filtered Corrected Specific differential phase (KDP) |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `gate_id` | 1 | time,range | - | Classification of dominant scatterer |
| `ground_clutter` | 1 | time,range | - | Ground Clutter |
| `height` | m | time,range | - | Height of radar beam |
| `height_over_iso0` | m | time,range | - | Height of radar beam over freezing level |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `mean_doppler_velocity_v` | m/s | time,range | - | Doppler velocity, vertical channel |
| `normalized_coherent_power` | 1 | time,range | - | Normalized coherent power, also known as SQI. |
| `normalized_coherent_power_v` | 1 | time,range | - | Normalized coherent power, also known as SQI, Vertical Channel |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |


_41 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "houcsapr2cmacS2.c1",
                             "start": "2022-09-28", "end": "2022-09-28", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./houcsapr2cmacS2.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "houcsapr2cmacS2.c1", "2022-09-28", "2022-09-28")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("houcsapr2cmacS2.c1", "2022-09-28", "2022-09-28"))   # cite what you pulled
```

This product carries 75 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "houcsapr2cmacS2.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['attenuation_corrected_differential_reflectivity', 'attenuation_corrected_differential_reflectivity_lag_1', 'attenuation_corrected_reflectivity_h'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `censor_mask`, `classification_mask`, `clutter_masked_velocity`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("houcsapr2cmacS2.c1", "20181012", "20260924")
```

The report's own note on quality: CMAC output includes a censor_mask (flag_masks/flag_meanings covering horizontal/vertical SNR below noise threshold, ccor below threshold, SQI below thresholds, sigpow below threshold, unfiltered rhoHV below threshold, and censored_by_clutter_micro_suppression) and a classification_mask (second_trip, third_trip, interference, clutter, sunspoke flags), plus a gate_id field (flag_values 0-6: multi_trip, rain, snow, no_scatter, melting, clutter, terrain_blockage) used to determine where corrections are applied. Rain rate (rain_rate_A) is set to 0.0 where normalized coherent power less than  0.4...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Doppler velocity aliasing (folding) | Radial velocities show sharp jumps/discontinuities near +/- Nyquist velocity; XSAPR and CSAPR alias at 12.4 and 16.52 m/s in baseline mode | Dealiasing performed using region-based (or fringe/phase-based) unfolding technique, with a secondary step minimizing a cost function against... | (hb p. 9) |
| Multi-trip (second/third trip) echoes | Low or flat normalized coherent power (NCP) and structureless Doppler spectra away from first-trip returns, appearing as spurious 'multi-trip' or 'no scatterer' regions on gate-ID maps | Gate-ID classification using texture of radial velocity plus rhoHV, NCP, temperature, height, SNR membership functions rather than NCP alone;... | (hb p. 1) |
| False low-NCP flagging in regions of high spectral width | NCP decreases even in purely first-trip regions of high convergence/divergence in convective storms, causing false flagging as multi-trip | Use gate-ID with multiple discriminants (texture, rhoHV, temperature, height, SNR) rather than relying on NCP alone | (hb p. 1) |
| Doppler folding contaminating texture calculation | Purely radial-velocity-based texture shows spurious high-texture signal at fold boundaries | Project radial velocity onto unit circle and use circular/directional statistics to compute texture, avoiding false texture at folds | (hb p. 3) |
| Liquid water path (attenuation) affecting reflectivity and Zdr at C-band/X-band | Reflectivity and Zdr are progressively reduced along the propagation path through liquid water, worse than at S-band | Specific attenuation retrieved via iterative hotspot method (Gu et al. 2011) and integrated/applied to correct reflectivity; specific differential... | (hb p. 9) |
| Ground clutter and pipeline clutter near radar | Persistent high-reflectivity/high-texture returns close to the radar location, tagged in classification_mask and ground_clutter fields | Most pipeline clutter returns near the radar were removed; clutter identification/tagging is an ongoing area of work, with some clutter returns... | (hb p. 11) |
| Non-hydrometeor / precipitation misclassification by membership functions | Gate-ID incorrectly tags some precipitation gates as non-hydrometeor classes | Further refinement of membership functions required for future deployments (e.g., BNF) | (hb p. 11) |
| LP PhiDP retrieval underperformance in extended differential backscatter phase (delta_dp)... | KDP and specific attenuation fields show anomalies/erroneous values in regions of extended delta_dp | Authors have a proposed solution but it is difficult to implement with currently supported LP packages; actively being worked on | (hb p. 11) |
| Clutter contamination of PhiDP/KDP/specific attenuation calculation | Occasional spurious spikes apparent in the Kdp and specific attenuation fields caused by clutter throwing off the PhiDP calculation | Filter out all Kdp greater than 15 deg/km | (hb p. 9) |
| Unresolved/undetected hail contamination | Radial paths passing through hail are not currently flagged; attenuation retrieval assumes ice attenuation is negligible and mixed-phase is intractable | Work is proceeding on determining if a radial is hail-contaminated; currently attenuation only calculated in regions identified as liquid... | (hb p. 9) |
| Zdr calibration bias at SGP XSAPR radars (May-Sep 2018) | Significant Zdr biases observed that vary scan-to-scan, preventing a confident Zdr calibration | All corrected Zdr data for the ARM SGP site during this period are masked and not available; raw Zdr included for analysis but users are urged to use... | (hb p. 10) |
| Non-uniform beam filling (NBF) and phase shift on backscatter (delta) contaminating... | Raw PsiDP contains contributions beyond propagation phase (PhiDP), causing non-monotonic or noisy differential phase profiles | Linear programming (LP) technique retrieves a strictly increasing, unbiased PhiDP from PsiDP, weighted by local reflectivity as a constraint | (hb p. 8) |
| 4DD (Four-Dimensional Dealiasing) implementation issues | Discussion of implementation issues in the original 4DD/RSL-wrapped dealiasing code led to persistent dealiasing errors | Switched to region-based (and fringe/phase-based) dealiasing techniques in Py-ART instead of 4DD | (hb p. 7) |
| Fringe/phase-based dealiasing technique underperformance | Early tests of the fringe-pattern dealiasing technique were sub-par | Technique remains available in Py-ART but is rarely used; region-based technique preferred | (hb p. 7) |
| Radar wavelength choice (no S-band) increases attenuation susceptibility | C-band/X-band reflectivity and Zdr show stronger attenuation signatures than would be seen at S-band, especially in severe storms | Necessitated development of robust attenuation and differential attenuation correction code within CMAC | (hb p. 9) |


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
- Giangrande, McGraw, and Lei 2013 (LP for differential phase processing)
- Giangrande and Ryzhkov 2008 (rainfall estimation via polarimetric echo classification)
- Gu, Ryzhkov, Zhang, Neilley, Knight, Wolf, and Lee 2011 (polarimetric attenuation correction in heavy rain at C band)
- Bringi, Huang, Chandrasekar, and Gorgucci 2002 (gamma raindrop size distribution parameter estimation)
- Gourley, Tabary, and Parent du Chatelet 2007 (fuzzy logic separation of precipitating/nonprecipitating echoes)
- Dolan and Rutledge 2009 (X-band hydrometeor ID algorithm)
- Wen, Protat, May, Wang, and Moran 2015 (cluster-based hydrometeor classification)
- Al-Sakka, Boumahmoud, Fradon, Frasier, and Tabary 2013 (fuzzy logic hydrometeor classification for French radars)
- Heistermann et al. 2014 (open source software for weather radar community)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-327.pdf (35 pages, DOE/SC-ARM-TR-327, by SM Collis, JJ Helmus, ZS Sherman, RC Jackson, B Raut, J O’Brien, M Grover, Y Feng, A Theisen)
- Catalog record: ARM data-source index, `instrument_class_code=csapr2-cmac`, read 2026-09-24
- Example file: `houcsapr2cmacS2.c1.20220928.074553.nc` from `houcsapr2cmacS2.c1`, 336.58 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
