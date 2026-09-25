---
name: arm-vap-ppihyd
description: ARM hydrometeor field statistics dataset derived from radar PPI scans (ppihyd) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Equivalent reflectivity factor, Doppler spectral width, V_D standard deviation per feature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with ppihyd data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - ppihyd, anxkasacrppihydmaskM1.c1, Equivalent reflectivity factor, Doppler spectral width, V_D standard deviation per feature, Cloud Properties.
---

# PPIHYD - hydrometeor field statistics dataset derived from radar PPI scans

PPIHYD is an evaluation data product that derives per-feature hydrometeor field statistics (reflectivity and Doppler spectral width percentiles/moments, morphology, water content and precipitation rate estimates, and interpolated thermodynamic properties) from ARM scanning radar plan position indicator (PPI) scans.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 43 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ppihyd` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-307 / I Silber, JM Comstock / August 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-307.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2019-12-01 to 2020-05-31 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ppihyd |


## Credit

Everything this skill knows about the retrieval is the work of **I Silber, JM Comstock** -
the ARM developers and mentors who wrote the technical report it derives from:

> I Silber, JM Comstock. *Plan Position Indicator Hydrometeor Field Statistics (PPIHYD) Evaluation Data Product Version 1.0*, DOE/SC-ARM-TR-307, August 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-307.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

PPIHYD processes quality-controlled, partially corrected PPI scan files (b1 or c1 datastreams) from ARM scanning radars, applying Doppler velocity dealiasing, beam blockage removal, Cartesian gridding via Py-ART with a modified Barnes weighting function, and non-meteorological/second-trip echo mitigation. Hydrometeor field 'features' (clustered hydrometeor fields) are identified from the equivalent reflectivity factor (Ze) field using tobac's feature detection and segmentation methods with three deployment-dependent Ze thresholds spaced by 0.5 dBZ increments. For each identified feature, statistics are computed including percentiles, min/max, and first four moments (mean, standard deviation, skewness, kurtosis) of Ze and Doppler spectral width, morphological properties (area, maximum Feret diameter, solidity, fill percent, ellipse fit parameters), water content and precipitation rate estimates from literature parameterizations, and thermodynamic properties (temperature, relative humidity, pressure) interpolated from the INTERPSONDE VAP. The output is organized as tabular per-feature statistics files accompanied by indexed feature mask arrays.

**Cadence.** input rate PPI scan sweeps at low-elevation angles (up to a few degrees), processed per sweep for a full given day; output every Daily output files; averaging Per-feature statistics computed over pixels comprising each detected hydrometeor feature within a sweep (hb p. 9).

## Inputs

The report names these instruments and sibling products: INTERPSONDE VAP, KASACR, KAZR, Scanning ARM Cloud Radar (SACR/XSACR/WSACR), XSAPR, CSAPR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Equivalent reflectivity factor (Ze) percentiles, min/max,... | dBZ | - | - | (hb p. 8) |
| Doppler spectral width (sigma_D) percentiles, min/max, and... | m/s | - | - | (hb p. 8) |
| V_D standard deviation per feature (mean Doppler velocity... | m/s | - | - | (hb p. 22) |
| Number of Ze peaks per feature with prominence of 2, 5, 10... | 1 | - | - | (hb p. 8) |
| Mean, min, max of interpolated sounding fields... | degC, %, kPa | - | - | (hb p. 8) |
| Morphological properties: area, maximum dimension,... | km^2, km, m, degree, 1, % | - | - | (hb p. 9) |
| Warm rain and ice precipitation rate estimates (RR, SR) per... | mm/h | - | - | (hb p. 9) |
| Ice water content (IWC) estimates per feature | g/m^3 | - | - | (hb p. 9) |
| Estimated height (alt) per feature | m | - | - | (hb p. 36) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Radius of influence (RoI) virtual beam width | 2° | (hb p. 11) |
| Weighting function | modified Barnes weighting function | (hb p. 11) |
| Dealiasing trigger threshold | VD exceeding 0.9 of Nyquist velocity in at least one sampled voxel | (hb p. 10) |
| Feature identification thresholds | three deployment-dependent Ze thresholds differentiated by 0.5 dBZ increments (e.g., COMBLE: -12.5, -12.0, -11.5 dBZ) | (hb p. 13) |
| Second-trip 'suspect' flag thresholds | orientation angle deviates less than 15° from centroid-radar angle and ellipse aspect ratio less than 0.3 | (hb p. 7) |
| Second-trip 'likely' flag thresholds | orientation angle deviates less than 7.5° from centroid-radar angle and ellipse aspect ratio less than 0.15 | (hb p. 7) |
| Artifact fraction flag threshold | artificially filled fraction of voxels exceeds 0.10 | (hb p. 6) |
| feature_num dimension (example file) | 9791 | (hb p. 21) |
| Mask grid dimensions (example file) | y = 1601, x = 1601 | (hb p. 41) |


## The data

**No example file was verified for this instrument.** the only datastream serves 2.4 GB files, past the download cap used for these examples.

ARM's catalog lists 2 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "anxkasacrppihydmaskM1.c1", "start": start, "end": end,
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
                     params={"user": f"{user}:{token}", "ds": "anxkasacrppihydmaskM1.c1",
                             "start": "2020-05-31", "end": "2020-05-31", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./anxkasacrppihydmaskM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "anxkasacrppihydmaskM1.c1", "2020-05-31", "2020-05-31")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("anxkasacrppihydmaskM1.c1", "2020-05-31", "2020-05-31"))   # cite what you pulled
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you have a
file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("anxkasacrppihydmaskM1.c1", "20191201", "20260924")
```

The report's own note on quality: PPIHYD reports several per-feature QC flags: a dealiasing flag (V_D_dealiased_flag/V_D_dealiased) indicating a dealiasing routine was applied; a radar FOV edge flag (edge_flag) for hydrometeor fields extending beyond the radar FOV; a large artifact fraction flag (artifact_frac_flag) for hydrometeor fields with a significant fraction of narrow-beam-blockage artifact pixels (threshold 0.10); and a second-trip flag (second_trip_flag, 1=suspect, 2=likely if not removed) denoting second-trip echo suspicion. Second-trip 'likely' features are removed from the final output dataset. Complete variable...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Doppler velocity aliasing/folding | Mean Doppler velocity (VD) exceeds 0.9 of the Nyquist velocity in at least one sampled voxel in the sweep; flagged sweeps show a dealiasing flag (V_D_dealiased_flag) set to 1 | A Py-ART region-based dealiasing procedure is applied automatically after filtering VD field texture values exceeding an automatically determined... | (hb p. 10) |
| Extended (terrain) beam blockage | Persistent loss of spatial continuity in scan sectors, typically near azimuth range limits, appearing as greyscale/excluded sectors in PPI plots | Entire affected scan sectors are excluded from processing after manual, once-per-deployment characterization of blockage-free sectors | (hb p. 3) |
| Narrow beam blockage from nearby obstacles (buildings, antenna towers, etc.) | Localized regions of Ze deviation from median-filtered Ze value revealed by time-averaged deviation analysis; appears as narrow masked/brighter regions in the beam blockage mask | Detected via time-averaged deviation of Ze from median-filtered value, mask expanded to include partially affected voxels, then filled using... | (hb p. 4) |
| Lack of certain fields in SACR measurements (e.g., normalized coherent power) | Absence of standard artifact-removal fields makes narrow beam blockage and data artifact identification more challenging | Narrow beam blockage identification method described is still experimental | (hb p. 4) |
| Non-meteorological echoes (insects, birds, etc.) | Spurious echoes in Ze field not associated with hydrometeors | Dedicated detection/interpolation processing step planned for future PPIHYD versions; not yet implemented | (hb p. 6) |
| Second-trip echoes | Elongated, narrow features whose ellipse-fit orientation angle nearly matches the angle from feature centroid to radar origin and whose ellipse aspect ratio is small (less than 0.3 suspect,... | Features flagged 'second-trip likely' are removed from the final output dataset; 'second-trip suspect' features are flagged (second_trip_flag) but... | (hb p. 6) |
| Truncation of Ze data due to feature-identification thresholds | Reported statistical moments (Ze_mean, Ze_std, Ze_skewness, Ze_kurtosis), especially higher moments (skewness, kurtosis), are biased because low-Ze values outside the threshold set are... | None specified beyond noting the effect; users should be aware moments are influenced by truncated data | (hb p. 8) |
| Feature extending beyond radar field of view | edge_flag = 1 for features that extend beyond the radar FOV, visible in mask/edge_flag plots at scan sector boundaries | Flagged via edge_flag variable so users can identify/exclude incomplete features | (hb p. 9) |
| Radial-wind-component limitation of V_D standard deviation field | Reported V_D_cld_std_std reflects only the radial wind component, which may not represent full wind variability, especially in dealiased sweeps | Handbook advises this output field 'should be used with caution, especially in dealiased sweeps' | (hb p. 10) |
| Parameterization-based precipitation rate/water content estimates applied irrespective of... | RR/SR/IWC estimates are calculated for all detected features regardless of temperature suggested by INTERPSONDE, so warm-rain parameterizations may be reported for features that are... | Calculated for all features due to long sounding release intervals and horizontal heterogeneity of thermodynamic fields; selection of which... | (hb p. 9) |
| No feature tracking across scans | Output lacks temporal tracking linkage between features in successive PPI scans, though tobac tracking-related fields are retained | Current PPIHYD processing does not include feature tracking owing to reduced value given short radar range and low PPI scan repetition frequency;... | (hb p. 6) |
| Elevation-angle dependence of hydrometeor field properties at high angles | Hydrometeor field properties change significantly at higher elevation-angle scans (e.g., crossing the melting level), especially over large radial distances | PPIHYD processing and output limited to low-elevation-angle sweeps (up to a few degrees) to support straightforward analysis of mostly precipitating... | (hb p. 2) |
| Ground clutter at some elevation configurations | Persistent clutter contamination in certain 0° elevation PPI scans | Such scans are excluded from PPIHYD processing entirely | (hb p. 2) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Barnes, SL. 1964. Journal of Applied Meteorology and Climatology 3(4): 396-409
- Covert, JA, DB Mechem, and Z Zhang. 2022. Atmospheric Chemistry and Physics 22(2): 1159-1174
- Feingold, G, T Goren, and T Yamaguchi. 2022. Atmospheric Chemistry and Physics 22(5): 3303-3319
- Geerts, B, et al. 2022. Bulletin of the American Meteorological Society 103(5): E1371-E1389
- Heikenfeld, M, et al. 2019. Geoscientific Model Development 12(11): 4551-4570
- Helmus, J, and SM Collis. 2016. Journal of Open Research Software 4(1): e25
- Fairless, T, M Jensen, A Zhou, and SE Giandrande. 2021. DOE/SC-ARM-TR-183
- Jensen, MP, et al. 2023. DOE/SC-ARM-23-038
- Kay, JE, et al. 2018. Journal of Geophysical Research - Atmospheres 123(8): 4294-4309
- McCoy, DT, et al. 2015. Journal of Geophysical Research - Atmospheres 120(18): 9539-9554

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-307.pdf (43 pages, DOE/SC-ARM-TR-307, by I Silber, JM Comstock)
- Catalog record: ARM data-source index, `instrument_class_code=ppihyd`, read 2026-09-24
- Example file: none - the only datastream serves 2.4 GB files, past the download cap used for these examples
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
