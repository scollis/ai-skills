---
name: arm-vap-mplcmaskml
description: ARM Micropulse Lidar Cloud Mask Machine Learning VAP (mplcmaskml) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (backscatter, range_corrected_backscatter, preprocess_backscatter, linear_depol_ratio, preprocess_linear_depol_ratio, cloud_mask_dl), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmplcmaskmlC1.c1) and the variable inventory of a real file. Use when working with mplcmaskml data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - mplcmaskml, Micropulse Lidar Cloud Mask Machine Learning VAP, sgpmplcmaskmlC1.c1, backscatter, range_corrected_backscatter, preprocess_backscatter, linear_depol_ratio, preprocess_linear_depol_ratio.
---

# MPLCMASKML - Micropulse Lidar Cloud Mask Machine Learning VAP

The MPLCMASKML VAP applies a machine-learning (deep learning) model to two-channel (NRB and LDR) micropulse lidar data from ARM fast-switching polarized MPL systems to produce a pixel-level cloud mask, confidence rating, cloud base/top heights, and number of cloud layers.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mplcmaskml` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-274 / D Flynn, E Cromwell, D Zhang / March 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-274.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2010-07-10 to 2026-09-23 (active) |
| Datastreams with data | 12 across 11 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mplcmaskml |


## Credit

Everything this skill knows about the retrieval is the work of **D Flynn, E Cromwell, D Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Flynn, E Cromwell, D Zhang. *Micropulse Lidar Cloud Mask Machine-Learning Value-Added Product Report*, DOE/SC-ARM-TR-274, March 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-274.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The machine-learning model is trained to identify cloud pixels from MPL lidar images using two-channel input: the MPL normalized relative backscatter (NRB) as one channel and the corresponding linear depolarization ratio (LDR) as the other, allowing simultaneous assessment of lidar backscatter/attenuation behavior and cloud phase/clear-sky/aerosol indication. The model was trained through a three-stage semi-supervised process: (1) cloud/no-cloud classification, (2) pre-training for cloud location using MPLCMASK VAP-derived cloud masks, and (3) final fine-tuning using hand-labeled cloud masks created from visual inspection of the two-channel imagery. The trained model is run on quarter-day segments of preprocessed log(NRB) and LDR data to estimate a cloud mask, which is then merged across quarter days, clustered to remove small false clouds/clutter, and merged spatially/temporally to produce cloud base, cloud top, and number of cloud layers. The cloud mask definition used for hand-labeling closely follows Wang et al. (2001), excluding liquid precipitation and virga while including other radiatively important suspended cloud particles.

**Cadence.** averaging Quarter-day processing: First quarter time bins 0-800 (00:00:00-06:40:00 UTC); Second quarter time bins 680-1480 (05:40:00-12:20:00 UTC); Third quarter time bins 1400-2200 (11:40:00-18:20:00 UTC); Fourth quarter time bins 2080-2880 (17:20:00-24:00:00 UTC); overlapping periods merged (hb p. 8).

## Inputs

The report names these instruments and sibling products: MPLCMASK (Micropulse Lidar Cloud Mask VAP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| backscatter | - | - | - | (hb p. 10) |
| range_corrected_backscatter | - | - | - | (hb p. 10) |
| preprocess_backscatter | - | - | - | (hb p. 10) |
| linear_depol_ratio | - | 0 to 1 (valid data range) | - | (hb p. 10) |
| preprocess_linear_depol_ratio | - | - | - | (hb p. 10) |
| cloud_mask_dl | - | - | - | (hb p. 10) |
| cloud_mask_confidence | 0 to 1 | 0 to 1, where 1 is highly... | - | (hb p. 10) |
| cloud_mask | - | - | - | (hb p. 10) |
| cloud_base | AGL | - | - | (hb p. 10) |
| cloud_top | AGL | - | - | (hb p. 10) |
| num_cloud_layers | - | - | - | (hb p. 10) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Pre-training VAP time resolution | 30 seconds averaged | (hb p. 2) |
| Pre-training VAP vertical height resolution | 30 meters averaged | (hb p. 2) |
| Classification pre-training data | 1780 quarter days (890 with cloud, 890 without cloud) | (hb p. 2) |
| Cloud location pre-training data | more than 4200 quarter days (2010-2015) | (hb p. 2) |
| Final training data | over 100 days hand-labeled cloud masks, mostly Jan 1-March 30 2015 plus supplementary April-December 2015 data | (hb p. 2) |
| Hold-out evaluation data | 66 quarter days | (hb p. 8) |
| March 2015 evaluation data | 27 days (108 quarter-days) from SGP C1 | (hb p. 8) |
| OLI evaluation data | 14 days (56 quarter-days) of hand-labeled data from May 2016 | (hb p. 9) |
| MPLCMASKML F1-Score (Hold-Out) | 0.8790 | (hb p. 8) |
| MPLCMASKML Precision (Hold-Out) | 0.8505 | (hb p. 8) |
| MPLCMASKML Recall (Hold-Out) | 0.9094 | (hb p. 8) |
| MPLCMASKML F1-Score (March) | 0.8626 | (hb p. 8) |
| MPLCMASKML Precision (March) | 0.8432 | (hb p. 8) |
| MPLCMASKML Recall (March) | 0.8829 | (hb p. 8) |
| MPLCMASK F1-Score (Hold-Out) | 0.5892 | (hb p. 8) |
| MPLCMASK Precision (Hold-Out) | 0.4423 | (hb p. 8) |
| MPLCMASK Recall (Hold-Out) | 0.8795 | (hb p. 8) |
| MPLCMASK F1-Score (March) | 0.65 | (hb p. 8) |
| MPLCMASK Precision (March) | 0.5072 | (hb p. 8) |
| MPLCMASK Recall (March) | 0.9049 | (hb p. 8) |
| MPLCMASKML F1-Score (OLI) | 0.7530 | (hb p. 9) |
| MPLCMASKML Precision (OLI) | 0.7438 | (hb p. 9) |
| MPLCMASKML Recall (OLI) | 0.7643 | (hb p. 9) |
| MPLCMASK F1-Score (OLI) | 0.4185 | (hb p. 9) |
| MPLCMASK Precision (OLI) | 0.371 | (hb p. 9) |
| MPLCMASK Recall (OLI) | 0.48 | (hb p. 9) |


## The data

Verified example: **`sgpmplcmaskmlC1.c1`**, file `sgpmplcmaskmlC1.c1.20260920.000003.nc`
(105.91 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=2880, `bound`=2, `height`=667 |
| Data variables | 26 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2026-09-20T00:00:03 to 2026-09-20T00:00:00 |
| dod version | mplcmaskml-c1-1.1 |
| process version | mplcmaskml-1.4.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `backscatter` | count/us | time,height | yes | Total attenuated backscatter |
| `cloud_mask` | 1 | time,height | yes | Cloud mask from deep learning model with clustering and merging... |
| `cloud_mask_zwang` | 1 | time,height | yes | Cloud mask from 30smplcmask1zwang.c1 |
| `linear_depol_ratio` | 1 | time,height | yes | Linear depolarization ratio |
| `num_cloud_layers` | 1 | time | yes | Number of cloud layers |
| `preprocess_backscatter` | 1 | time,height | yes | Preprocessed range-corrected total attenuated backscatter for model |
| `preprocess_linear_depol_ratio` | 1 | time,height | yes | Preprocessed linear depolarization ratio for model |
| `cloud_base` | km | time | - | Lowest cloud base height above ground level (AGL) |
| `cloud_mask_confidence` | 1 | time,height | - | Model confidence in cloud prediction |
| `cloud_mask_dl` | 1 | time,height | - | Cloud mask from deep learning model |
| `cloud_top` | km | time | - | Highest cloud top height above ground level (AGL) |
| `height` | km | height | - | Vertical height above ground level (AGL) corresponding to the bottom... |
| `range_corrected_backscatter` | km^2*count/us | time,height | - | Range-corrected total attenuated backscatter |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmplcmaskmlC1.c1", "2026-09-20", "2026-09-20")
ds = armlive_open("sgpmplcmaskmlC1.c1", "2026-09-20", "2026-09-20", cleanup_qc=True)
```

## Quality control in this product

7 `qc_` companion variables cover 7 of the
26 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpmplcmaskmlC1.c1.20260920.000003.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `linear_depol_ratio` | The value of signal is zero in the denominator causing the... | 691665 | 36.0062 |
| `preprocess_linear_depol_ratio` | Value is less than 0 | 691665 | 36.0062 |
| `cloud_mask_dl` | qc_linear_depol_ratio is Bad | 691416 | 35.9933 |
| `cloud_mask` | qc_linear_depol_ratio is Bad | 691416 | 35.9933 |
| `cloud_mask_zwang` | Unable to determine the cloud mask, data value set to... | 42272 | 2.2006 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmplcmaskmlC1.c1", "20100710", "20260924")
```

The report's own note on quality: Model performance is assessed via precision (percentage of predicted clouds that are actual clouds), recall (percentage of actual clouds predicted as clouds), and F1-score (harmonic mean of precision and recall), computed against hand-labeled ground-truth hold-out data (66 quarter days) and an independent March 2015 SGP data set (27 days/108 quarter-days), as well as an OLI arctic transfer-learning evaluation (14 days/56 quarter-days). The output variable cloud_mask_confidence provides a per-pixel model confidence rating (0 to 1) for the cloud prediction.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Polarization degradation of the source MPL instrument | If the polarization behavior of the specific MPL degrades significantly, LDR values increase, and the model struggles to accurately distinguish clouds from clear air or aerosol | - | (hb p. 8) |
| Transfer learning site/climate mismatch | A model trained on data from a mid-latitude site (SGP) may not perform as well on data from a different MPL operating at an arctic location due to differing dominant cloud types (cirrus at... | - | (hb p. 8) |
| MPLCMASK (predecessor VAP) exaggerated/oversampled cloud boundaries | MPLCMASK tends to oversample both the cloud top and bottom boundaries and can detect false edges compared to MPLCMASKML | Use MPLCMASKML which shows less exaggerated cloud boundaries and improved cloud layer separation | (hb p. 12) |
| Aerosol loading interference in boundary layer for MPLCMASK | Moderate aerosol loading likely interferes with accurate cloud boundary identification for the MPLCMASK algorithm in the boundary layer (example: 10-14 UTC on Dec 24, 2017), while... | - | (hb p. 11) |
| Missing/invalid NRB values (NaN, infinite) | Missing, infinite, or NaN values in NRB show up as anomalies before preprocessing | Missing, infinite, or NaN NRB values are set to the daily minimum during preprocessing | (hb p. 8) |
| LDR out-of-range values | LDR values outside the valid 0-1 range appear as extreme/invalid values | Missing values and NaNs are set to 0; values greater than 1 are set to 1; values less than 0 are set to 0 | (hb p. 8) |
| Small false clouds or clutter above 10 km | Spurious isolated cloud-flagged bins appear above 10 km altitude | Cluster test from MPLCMASK VAP is run on all bins identified as cloud above 10 km to detect and attempt to eliminate small false clouds or clutter | (hb p. 8) |
| Fragmented cloud layers in time and height | Cloud mask shows closely spaced but disconnected cloud segments in time or height | Cloud bins are merged time-wise if less than 2 time bins (1 minute) apart, and height-wise if less than 4 bins (120 m) apart | (hb p. 9) |
| Degraded signal-to-noise ratio near sunrise/with thin cirrus | Background noise increases with time near sunrise; MPLCMASKML identifies most cirrus cloud but misses some thinner cloud edges when NRB and LDR SNR are degraded | - | (hb p. 12) |
| Attenuating low cloud near surface historically missed by MPLCMASK | MPLCMASK fails to identify attenuating cloud below 500 m (e.g., between 10-11 UTC on Dec 24, 2017), while MPLCMASKML successfully identifies it - important at sites like OLI where sub-500m... | MPLCMASKML model identifies clouds below 500 m | (hb p. 11) |
| Model trained on site-, date-, and instrument-specific data (SGP winter/spring 2015) | Performance metrics differ between the SGP hold-out/March 2015 evaluation (higher F1/precision/recall) and the OLI arctic evaluation (lower F1/precision/recall), reflecting... | - | (hb p. 6) |
| Only fast-switching polarized MPL data supported | Older single-wavelength non-polarized or non-fast-switching polarized MPL data sets are not processed by current MPLCMASKML version | Alternative versions of the VAP could be developed to handle older MPL data sets | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Cromwell E, and DM Flynn. 2019. "Lidar Cloud Detection with Fully Convolutional Networks." IEEE Winter Conference on Applications of Computer Vision 2019: 619-627. PNNL-SA-138402. https://doi.org/10.1109/WACV.2019.00071
- Flynn, D, C Sivaraman, J Comstock, and D Zhang. 2020. Micropulse Lidar Cloud Mask (MPLCMASK) Value-Added Product for the Fast-Switching Polarized Micropulse Lidar Technical Report. ARM user facility. DOE/SC-ARM/TR-098.
- Lim K-S S, LD Riihimaki, Y Shi, D Flynn, JM Kleiss, LK Berg, WI Gustafson Jr., Y Zhang, and KL Johnson. 2019. "Long-Term Retrievals of Cloud Type and Fair-Weather Shallow Cumulus Events at the ARM SGP Site." Journal of...
- Przybylak, R. 2003. The Climate of the Arctic. 1st ed. Kluwer Academic.
- Serreze, MC, and RG Barry. 2005. The Arctic Climate System. Cambridge University Press.
- Wang, Z, and K Sassen. 2001. "Cloud Type and Macrophysical Property Retrieval Using Multiple Remote Sensors." Journal of Applied Meteorology 40(10): 1665-1682, https://doi.org/10.1175/1520-0450(2001)040less than...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-274.pdf (17 pages, DOE/SC-ARM-TR-274, by D Flynn, E Cromwell, D Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=mplcmaskml`, read 2026-09-24
- Example file: `sgpmplcmaskmlC1.c1.20260920.000003.nc` from `sgpmplcmaskmlC1.c1`, 105.91 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
