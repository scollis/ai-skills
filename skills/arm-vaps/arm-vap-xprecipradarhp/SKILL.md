---
name: arm-vap-xprecipradarhp
description: ARM Surface Hydrometeor Phase (xprecipradarhp) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Unique Phase ID), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (gucxprecipradarhpS2.c1) and the variable inventory of a real file. Use when working with xprecipradarhp data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Surface Meteorology. Triggers - xprecipradarhp, Surface Hydrometeor Phase, gucxprecipradarhpS2.c1, Unique Phase ID, Cloud Properties, Surface Meteorology.
---

# XPRECIPRADARHP - Surface Hydrometeor Phase

This value-added product classifies the phase (liquid, snow, graupel/hail, or mixed melting) of near-surface precipitation over the SAIL/UCRB site by combining semi-supervised and fuzzy-logic hydrometeor classifications derived from CMAC-corrected CSU X-band polarimetric radar fields and sounding-based temperature profiles.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 19 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `xprecipradarhp` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-334 / BA Raut, JR O'Brien, ZS Sherman, RC Jackson, MA Grover, ME Tuftedal, SM Collis, DR Feldman / April 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-334.pdf) |
| Category | Cloud Properties; Surface Meteorology |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2021-11-02 to 2023-06-16 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/xprecipradarhp |


## Credit

Everything this skill knows about the retrieval is the work of **BA Raut, JR O'Brien, ZS Sherman, RC Jackson, MA Grover, ME Tuftedal, SM Collis, DR Feldman** -
the ARM developers and mentors who wrote the technical report it derives from:

> BA Raut, JR O'Brien, ZS Sherman, RC Jackson, MA Grover, ME Tuftedal, SM Collis, DR Feldman. *SAIL Field Campaign X-Band Precipitation Radar Seasonal Surface Hydrometeor Phase Classification Value-Added Product Report*, DOE/SC-ARM-TR-334, April 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-334.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm ingests Corrected Moments in Antenna Coordinates (CMAC) fields—corrected reflectivity (Zc), specific differential phase (KDP), and differential reflectivity (ZDR)—from the CSU X-band precipitation radar, which have already been corrected for nonmeteorological echoes, attenuation, and beam blockage, and appends environmental temperature profiles from nearby soundings. Two classification methods are then applied to these polarimetric fields: Py-ART's semi-supervised classification (SSC), which uses model-based clustering of polarimetric signatures, and CSURadartools' fuzzy-logic hydrometeor classification (FHC), run with separate summer and winter configurations (winter for DJF, summer for all other months) that yield physically interpretable fuzzy membership classes. SSC uses Zc, ZDR, KDP, copolar correlation coefficient (rhoHV), and temperature; FHC summer uses Zc, ZDR, KDP, rhoHV, and temperature, while FHC winter additionally uses signal-to-noise ratio (SNR). Both classifier outputs (each with their own granular hydrometeor classes) are then mapped into a unified five-category Unique Phase ID (UHID) schema: 0 Unclassified, 1 Liquid, 2 LD_Frozen (Snow), 3 HD_Frozen (Graupel/hail), 4 Mixed (wet snow/melting hail). SQUIRE grid projections are used to select near-surface gates per beam, mitigating beam-blockage issues and making the product directly usable for QPE.

**Cadence.** input rate Per radar volume (native radar grid from gucxprecipradarcmacppiS2.c1); output every One output NetCDF file per input volume (hb p. 12).

## Inputs

The report names these instruments and sibling products: CSU X-Band Precipitation Radar (gucxprecipradarcmacppiS2.c1), CMAC (Corrected Moments in Antenna Coordinates) Value-Added Product, SQUIRE (Surface Quantitative Precipitation Estimation) Value-Added..., Py-ART semi-supervised classifier, CSURadartools fuzzy-logic hydrometeor classifier.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Unique Phase ID (UHID) - unified hydrometeor phase... | categorical ID | 0-4 (0: Unclassified, 1: Liquid,... | - | (hb p. 10) |
| Py-ART SSC hydrometeor classification | categorical ID | 0-9 (see Table 3) | - | (hb p. 9) |
| CSU FHC summer hydrometeor classification | categorical ID | 1-10 (see Table 1) | - | (hb p. 8) |
| CSU FHC winter hydrometeor classification | categorical ID | 0-7 (see Table 2) | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Input datastream | gucxprecipradarcmacppiS2.c1 (CMAC corrected fields on native radar grid) | (hb p. 10) |
| FHC configuration selection | Winter configuration used for December, January, February; summer configuration used for all other months | (hb p. 10) |
| Unique Phase ID (UHID) schema | 0: Unclassified, 1: Liquid, 2: LD_Frozen, 3: HD_Frozen, 4: Melting/Mixed | (hb p. 10) |
| Evaluation data availability | November 2021 to June 2023 | (hb p. 12) |
| Output file format | ARM-compliant NetCDF file per input volume | (hb p. 12) |
| SSC classification inputs | Zc, ZDR, KDP, copolar correlation coefficient (rhoHV), temperature | (hb p. 10) |
| FHC summer classification inputs | Zc, ZDR, KDP, rhoHV, temperature | (hb p. 10) |
| FHC winter classification inputs | Zc, ZDR, KDP, rhoHV, temperature, SNR | (hb p. 10) |


## The data

Verified example: **`gucxprecipradarhpS2.c1`**, file `gucxprecipradarhpS2.c1.20230613.083408.nc`
(0.98 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1, `y`=160, `x`=160 |
| Data variables | 9 |
| QC variables | 0 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2023-06-13T08:34:08 to 2023-06-13T08:34:08 |
| dod version | xprecipradarhp-c1-1.3 |
| process version | HP-v1.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `corrected_reflectivity` | dBZ | time,y,x | - | Corrected equivalent_reflectivity_factor |
| `hp_fhc` | 1 | time,y,x | - | Near surface hydrometeor phase using fuzzy-logic method |
| `hp_ssc` | 1 | time,y,x | - | Near surface hydrometeor phase using semi-supervised method |
| `lowest_height` | m | time,y,x | - | Height of the lowest radar gate |
| `radar_alt` | m | - | - | Altitude of location of the radar |
| `radar_lat` | degree_north | - | - | Latitude of location of the radar |
| `radar_lon` | degree_east | - | - | Longitude of location of the radar |
| `time` | - | time | - | Time offset from midnight |
| `x` | m | x | - | X distance on the projection plane from the origin |
| `y` | m | y | - | Y distance on the projection plane from the origin |


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
                     params={"user": f"{user}:{token}", "ds": "gucxprecipradarhpS2.c1",
                             "start": "2023-06-13", "end": "2023-06-13", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./gucxprecipradarhpS2.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "gucxprecipradarhpS2.c1", "2023-06-13", "2023-06-13")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("gucxprecipradarhpS2.c1", "2023-06-13", "2023-06-13"))   # cite what you pulled
```
### First look

A gridded or multi-dimensional product, so one axis is fixed to plot it.

```python
import matplotlib.pyplot as plt

# This field is 3-D ('time', 'y', 'x'), so a first look has to fix an axis.
fig, ax = plt.subplots(figsize=(8, 4))
ds["corrected_reflectivity"].isel(x=0).plot(ax=ax)
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("gucxprecipradarhpS2.c1", "20211102", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The product combines outputs from Py-ART semi-supervised classification and CSU fuzzy-logic classifiers into a unified, quality-controlled set of phase labels (Unique Phase ID/UHID) for near-surface precipitation. The handbook notes generally good agreement between SSC and FHC for liquid and low-density frozen classes in both seasons, but large discrepancies in the mixed/melting class, and states that further ground comparison and statistical analysis are needed to evaluate these differences.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Disagreement between SSC and FHC classifiers in the mixed/melting class | SSC tends to classify more points as liquid than FHC does in the mixed/melting hydrometeor class, visible as large discrepancies between the two classification panels in event plots | Further ground comparison and statistical analysis are needed to evaluate these differences | (hb p. 12) |
| SSC overestimation of rain and low-density frozen classes | SSC method shows higher total frequency counts for rain and low-density frozen classes compared to FHC across summer (JJA) and winter (DJF) months in frequency histograms | - | (hb p. 13) |
| SSC underestimation of mix/melting and high-density frozen classes | SSC shows lower total frequency counts for mix/melting and high-density frozen classes relative to FHC in seasonal frequency comparisons | - | (hb p. 13) |
| Varying number and definition of hydrometeor classes between classifiers | Py-ART SSC and CSURadartools FHC produce different numbers of classes with different definitions, making raw outputs not directly comparable | Classes are combined/mapped into four simplified phase categories (Table 4) for comparability | (hb p. 8) |
| Beam blockage at the X-band radar site | Would appear as gaps or reduced returns along blocked beam paths if not corrected | CMAC fields are corrected for beam blockage; SQUIRE grid projections used to select near-surface gates per beam to mitigate this issue | (hb p. 4) |
| Attenuation at X-band | Would show reduced reflectivity/phase fidelity along propagation path if uncorrected | CMAC corrections are used to maintain phase fidelity and correct attenuation before computing KDP and other polarimetric-derived features | (hb p. 10) |
| Increased uncertainty in more granular hydrometeor classes | Fine-grained classes (e.g., the 8-10 category CSU/Py-ART schemes) show more variability/uncertainty than needed for QPE and hydrologic applications | Classes combined into four practical phase categories (Table 4) to reduce uncertainty for QPE/hydrology use | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Besic, N, et al. 2016. Atmospheric Measurement Techniques 9(9): 4425-4445, https://doi.org/10.5194/amt-9-4425-2016
- Collis, SM, et al. 2022. Corrected Moments in Antenna Coordinates (CMAC) X-SAPR Technical Report. DOE/SC-ARM-TR-283.
- Dolan, B, and SA Rutledge. 2009. Journal of Atmospheric and Oceanic Technology 26(10): 2071-2088, https://doi.org/10.1175/2009JTECHA1208.1
- Feldman, DR, et al. 2023. Bulletin of the American Meteorological Society 104(12): E2192-E2222, https://doi.org/10.1175/BAMS-D-22-0049.1
- Grover, MA, et al. 2023. SAIL Field Campaign X-Band Precipitation Radar Surface Quantitative Precipitation Estimation (SQUIRE) Value-Added Product Report. DOE/SC-ARM-TR-287.
- Helmus, JJ, and SM Collis. 2016. Journal of Open Research Software 4(1): e25, https://doi.org./10.5334/jors.119
- Jackson, R, et al. 2025. Journal of Atmospheric and Oceanic Technology 43(1): 77-93, https://doi.org/10.1175/JTECH-D-25-0023.1
- O'Brien, JR, et al. 2024. CSU X-Band Precipitation Radar PPI Data Processed with CMAC Value-Added Product Report. DOE/SC-ARM-TR-313.
- Thompson, EJ, et al. 2014. Journal of Atmospheric and Oceanic Technology 31(7): 1457-1481, https://doi.org/10.1175/JTECH-D-13-00119.1

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-334.pdf (19 pages, DOE/SC-ARM-TR-334, by BA Raut, JR O'Brien, ZS Sherman, RC Jackson, MA Grover, ME Tuftedal, SM Collis, DR Feldman)
- Catalog record: ARM data-source index, `instrument_class_code=xprecipradarhp`, read 2026-09-24
- Example file: `gucxprecipradarhpS2.c1.20230613.083408.nc` from `gucxprecipradarhpS2.c1`, 0.98 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
