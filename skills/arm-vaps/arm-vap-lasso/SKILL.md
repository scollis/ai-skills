---
name: arm-vap-lasso
description: ARM LES ARM Symbiotic Simulation and Observation (LASSO) (lasso) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (In-cloud liquid water path, 1D boundary-layer cloud fraction, Surface temperature, Surface water vapor mixing ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with lasso data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - lasso, LES ARM Symbiotic Simulation and Observation (LASSO), sgplassohighfreqobsC1.c1, In-cloud liquid water path, 1D boundary-layer cloud fraction, Surface temperature, Derived Quantities and Models.
---

# LASSO - LES ARM Symbiotic Simulation and Observation (LASSO)

LASSO produces bundled large-eddy simulation (LES) model output, input forcing files, co-registered ARM observations, and skill scores for shallow convection cases at the SGP site, packaged as per-simulation 'data bundles' for research and model evaluation.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 171 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `lasso` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-216 / WI Gustafson, A Vogelmann, X Cheng, KK Dumas, S Endo, KL Johnson, B Krishna, Z Li, T Fairless, H Xiao / September 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-216.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1989-12-31 to 2026-09-24 (active) |
| Datastreams with data | 110 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/lasso |


## Credit

Everything this skill knows about the retrieval is the work of **WI Gustafson, A Vogelmann, X Cheng, KK Dumas, S Endo, KL Johnson, B Krishna, Z Li, T Fairless, H Xiao** -
the ARM developers and mentors who wrote the technical report it derives from:

> WI Gustafson, A Vogelmann, X Cheng, KK Dumas, S Endo, KL Johnson, B Krishna, Z Li, T Fairless, H Xiao. *Description of the LASSO Data Bundles Product*, DOE/SC-ARM-TR-216, September 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-216.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Extraction coverage.** the report is 171 pages and the extractor reads at most 110,000 characters, so 60 pages were passed - cover, the full 27-page main body, Appendix A release history and Appendix C sub-VAP summaries - and 112 pages of netCDF header dumps were not read. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

LASSO drives the WRF-FASTER LES model (or, for earlier alpha releases, SAM) with large-scale forcing derived from three independent methodologies (VARANAL, ECMWF/DDH, and MSDA) plus radiosonde-based initial profiles, producing high-resolution (100-m grid, 226 vertical levels) simulations of shallow convection. Model output is co-registered in space and time with ARM ground-based observations (MWR, AERI, ARSCL, TSI, Doppler lidar, Raman lidar, radiosondes, surface MET) to allow apples-to-apples comparison between simulated and observed quantities such as LWP, cloud fraction, LCL, boundary-layer thermodynamics, and cloud-base height. Diagnostic plots (time series, Taylor diagrams, regressions, 2D cloud masks) and skill scores (Taylor skill, relative-mean skill, equitable threat score, frequency bias) are computed to quantify agreement between simulation and observation for each case day and simulation ensemble member. Skill scores are combined via geometric-mean formulas into single- and multi-variable net skill scores ranging from 0 (no skill) to 1 (perfect agreement) to help users identify better-performing simulations for their application. The resulting data bundles, browsable via the LASSO Bundle Browser, provide reproducible LES inputs/outputs, evaluation datasets, and quantitative skill metrics rather than raw instrument measurements.

**Cadence.** input rate Raw model output/statistics: 10-minute averaging with 1-minute sampling; high-frequency observations at near-native resolution; output every LASSO output provides 1-hour averages for model-observation comparisons unless otherwise noted; averaging 1-h averages for standard evaluation; high-frequency observation files at near-native resolution for 2018 and 2019 cases (hb p. 17).

## Inputs

The report names these instruments and sibling products: WRF model (LES), SAM model, VARANAL, AERI/AERIoe, MWR/MWRRet, TSI (Total Sky Imager), ARSCL VAP, KAZR (Ka-band ARM Zenith Radar), Micropulse lidar, Raman lidar, Doppler lidar, Radar Wind Profiler (RWP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| In-cloud liquid water path (LWP) | g m-2 | 1 less than  LWP less than  40 g... | - | (hb p. 17) |
| 1D boundary-layer cloud fraction (CF) | fraction | - | - | (hb p. 17) |
| 2D time-height cloud mask/cloud fraction | binary mask / fraction | below 5 km treated; lowest ARSCL... | - | (hb p. 18) |
| Regional lifting condensation level height (LCL, LCL_domain) | m | within 60 km of Central Facility... | standard deviation quantifies regional... | (hb p. 18) |
| Surface temperature (Tsurface) | K | - | - | (hb p. 19) |
| Surface water vapor mixing ratio (QVsurface) | g kg-1 | - | - | (hb p. 19) |
| Surface relative humidity (RHsurface) | % | - | - | (hb p. 19) |
| Boundary-layer thermodynamic profiles (T, water vapor... | K, g kg-1 | lowest 5 km | - | (hb p. 19) |
| Mid-boundary-layer moisture and temperature... | g kg-1, K, % | 0.5-0.7 km layer average | - | (hb p. 19) |
| Regional boundary-layer cloud-base height | m | from 5 Doppler lidars ~45 km from... | standard deviation for regional variability | (hb p. 19) |
| Taylor skill score, relative mean skill score, net skill... | dimensionless (0-1) | 0 (no skill) to 1 (perfect) | - | (hb p. 24) |
| 2D cloud mask skill scores (ETS/Gilbert skill score,... | dimensionless | ETS: -1/3 to 1, truncated to [0,1] | - | (hb p. 25) |
| 2D Time-Height Cloud Mask | cloud/no-cloud mask | clouds at or above 160 m; cloud... | - | (hb p. 18) |
| Regional Lifting Condensation Level Height (LCL) | m | - | - | (hb p. 18) |
| Surface Temperature | K | - | - | (hb p. 19) |
| Mid-Boundary-Layer Moisture (QVboundary_layer) | g kg-1 | 0.5-0.7 km layer average | - | (hb p. 19) |
| Mid-Boundary-Layer Temperature (Tboundary_layer) | K | 0.5-0.7 km layer average | - | (hb p. 19) |
| Mid-Boundary-Layer Relative Humidity (RHboundary_layer) | % | 0.5-0.7 km layer average | - | (hb p. 19) |
| Taylor skill score (ST) | unitless (0-1) | 0 to 1 | - | (hb p. 23) |
| Relative mean skill score (SRM) | unitless (0-1) | 0 to 1 | - | (hb p. 23) |
| Net single-variable skill score (S) | unitless (0-1) | 0 to 1 | - | (hb p. 24) |
| Equitable Threat Score (ETS) / truncated ETS skill score... | unitless | -1/3 to 1 (truncated to 0 to 1) | - | (hb p. 25) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| LES model | WRF version 3.8.1 with WRF-FASTER modifications | (hb p. 13) |
| Grid spacing | 100-m horizontal grid spacing | (hb p. 13) |
| Domain size | 25 km across | (hb p. 13) |
| Vertical levels | 226 levels, surface to 14.7 km | (hb p. 13) |
| Vertical grid spacing | 30 m up to 5 km, stretching to 300 m near model top | (hb p. 13) |
| Microphysics scheme | Thompson microphysics scheme | (hb p. 13) |
| Radiation scheme | RRTMG shortwave and longwave | (hb p. 13) |
| Turbulence scheme | 1.5 order TKE approach (Deardorff 1980) | (hb p. 13) |
| Initial profiles source | 12 UTC radiosonde soundings from Central Facility (2017+ cases) | (hb p. 13) |
| VARANAL forcing region | 300-km region | (hb p. 14) |
| ECMWF DDH forcing scales (2016+) | 413 km, 114 km, 9 km (single IFS column) | (hb p. 14) |
| ECMWF DDH forcing scale (2015 Alpha 1) | 16 km for smallest scale | (hb p. 14) |
| MSDA finest grid spacing | 2 km for SGP region | (hb p. 15) |
| MSDA forcing area sizes | 75 km, 150 km, 300 km | (hb p. 15) |
| Output averaging for evaluation | 1-h averages for model-observation comparisons unless otherwise noted | (hb p. 17) |
| WRF/SAM statistics averaging | time-averaged over 10-minute period with sampling every minute | (hb p. 22) |
| Cloud mask hydrometeor threshold (simulation) | total hydrometeor mixing ratio greater than  10-7 kg kg-1 | (hb p. 18) |
| ARSCL lowest cloud mask height | 160 m above ground | (hb p. 18) |
| 2D cloud mask evaluation height limit | below 5 km | (hb p. 18) |
| ETS skill score range | -1/3 to 1, truncated at 0 (SETS) | (hb p. 25) |
| Number of shallow-convection case days (2015-2019) | 95 case days | (hb p. 11) |
| v1 2019 release | 136 data bundles for 17 days | (hb p. 37) |
| v1 2018 release | 240 data bundles for 30 days | (hb p. 38) |
| v1 2017 release | 240 data bundles for 30 days | (hb p. 39) |
| Alpha 2 2016 release | 544 data bundles for 13 days | (hb p. 40) |
| Alpha 1 2015 release | 192 data bundles for 5 days | (hb p. 41) |


_32 further rows in the report._

## The data

**No example file was verified for this instrument.** the datastream serves a tar bundle that arrived truncated on repeated download attempts.

ARM's catalog lists 110 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "sgplassohighfreqobsC1.c1", "start": start, "end": end,
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
                     params={"user": f"{user}:{token}", "ds": "sgplassohighfreqobsC1.c1",
                             "start": "2026-09-24", "end": "2026-09-24", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgplassohighfreqobsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgplassohighfreqobsC1.c1", "2026-09-24", "2026-09-24")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgplassohighfreqobsC1.c1", "2026-09-24", "2026-09-24"))   # cite what you pulled
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you have a
file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgplassohighfreqobsC1.c1", "19891231", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The complete_flag field (0=all data available, 1=incomplete) and observation_data_availability_comments field in the sgplassostat file (renamed sgplassoscore in v1 2019) flag whether all input data needed to calculate skill scores was available for a given simulation, with comments providing additional detail (e.g., Raman lidar outages). LWP retrievals (MWRRet, AERIoe) are noted to have passed only preliminary QC, with more rigorous QC still needed. Ancillary QC variables (e.g., qc_aerioe_lwp, qc_mwrret_lwp, qc_temperature, qc_water_vapor_mixing_ratio, qc_relative_humidity, qc_pressure)...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Range of simulation behavior/quality varies | Comparisons to observations show a range of simulation skill; some simulations perform much better than others for a given case | Contact the LASSO team to ensure simulation details are understood and used appropriately for a given application | (hb p. 11) |
| Shallow-convection data bundle production hiatus | No new SGP shallow-convection case days after 2019 in this release; gap in temporal coverage | Resources redirected to deep convection and maritime scenarios; may resume shallow-convection processing when resources permit | (hb p. 11) |
| COVID-19 impact on 2020 data availability | Missing radiosonde launches and instrument outages in part of 2020 season | None stated beyond noting the cause | (hb p. 11) |
| LWP retrieval preliminary QC only | LWP values from MWRRet/AERIoe have passed only preliminary QC, not final rigorous QC | Additional work ongoing to improve LWP observations; AERIoe expected to improve | (hb p. 17) |
| LWP domain averaging mismatch | LWP in wrfstat file is an all-sky, domain-averaged value, whereas sgplassodiagobsmod file LWP is clear-sky-screened, in-cloud only; direct comparison of these two without accounting for the... | Use consistent clear-sky screening between obs and model as done in sgplassodiagobsmod files | (hb p. 17) |
| Single-site LWP retrieval | LWP retrievals only available from the single SGP Central Facility site, not regionally representative | None stated | (hb p. 17) |
| Insect contamination of radar-based cloud mask | Pronounced regions of apparent cloud fraction in ARSCL 2D cloud mask (e.g., 30 June 2017 example) that are actually insects, inflating cloud fraction/frequency of occurrence | Methodology being investigated to identify and account for insects in the 2D cloud mask; not yet implemented | (hb p. 18) |
| Frozen turbulence assumption in cloud mask comparison | Narrow-column ARSCL cloud sampling may not represent the broader cloud field, especially problematic at lower 1D CF values | None stated beyond caution to not over-interpret results | (hb p. 18) |
| Cirrus cloud mask threshold sensitivity | Presence of simulated cirrus clouds is highly sensitive to the hydrometeor mixing-ratio threshold (10-7 kg kg-1), unlike liquid clouds which are relatively insensitive | Only clouds below 5 km treated in 2D metric to avoid cirrus sensitivity issues | (hb p. 18) |
| Simulated clouds below 160 m not compared | Simulated cloud below 160 m AGL is excluded from 2D cloud mask plots since ARSCL cloud mask begins at 160 m | None stated | (hb p. 21) |
| Nudging profiles provided but unused | TH_RLX, QV_RLX relaxation/nudging profiles and their tendencies are present in forcing files but nudging is NOT actually performed in LASSO simulations; users should not assume nudging... | None stated; noted as NOT USED in Table 1 | (hb p. 13) |
| WRF-to-SAM surface pressure inconsistency | Surface pressure from spatially averaged forcing data source (MSDA/ECMWF/VARANAL) can be inconsistent with point-based radiosonde surface pressure used to initialize the model, causing... | Sample conversion script uses initial offset between the two surface pressures to adjust subsequent values, assuming the bias changes only slightly... | (hb p. 15) |
| Surface flux handling differs between WRF-LES and single-column model implementations | Differences noted by Angevine et al. (2018) in coupling of skin/surface layer between WRF LES mode and single-column WRF | Users converting inputs must account for model-specific assumptions | (hb p. 15) |
| Ensemble spread from three forcing methodologies | Simulations driven by VARANAL, ECMWF, and MSDA forcings can diverge substantially, especially on days with strong spatial variability around SGP not captured by a single regional-average... | Multiple forcing methods and scales provided to give a vetted ensemble; users should examine spread | (hb p. 14) |
| ECMWF forcing large-scale vertical velocity processing error (2015-2018 bundles) | Large-scale vertical velocity field for ECMWF forcing needs multiplying by factor of 10 for data bundle cases from 2015 to 2018; affects LES output and ECMWF forcing use in these older... | Reprocessing of all impacted cases was underway as of August 2020; will be re-released when ready | (hb p. 37) |
| ECMWF forcing methodology change in 2019 cases | Change in ECMWF data source (archived ARM ECMWF datastreams vs. direct ECMWF IFS access) alters forcing-tendency calculation methodology starting with 2019 cases; no systematic bias found... | Users comparing model behavior across time with ECMWF forcing should be aware of this methodological discontinuity | (hb p. 37) |
| Raman lidar hardware failure gap (Aug-Sep 2018) | Missing mid-boundary-layer temperature/moisture skill scores for specific 2018 case dates (11-Aug, 1-Sep, 2-Sep, 9-Sep, 11-Sep, 14-Sep, 16-Sep, 17-Sep, 18-Sep-2018); complete_flag=1 in... | complete_flag and observation_data_availability_comments metadata fields added to flag incomplete data | (hb p. 38) |
| sgpmet sensor replacement introduces warm bias (Jan 2018) | New C1 temperature sensor shows warm bias greater than 1 K vs previous cold bias, which manifests as a spurious apparent dry bias in model vs sgpmet water-vapor comparisons even though... | Surface meteorological values for skill-score calculations switched from sgpmet to sgpmaws data set until further notice | (hb p. 38) |
| LWP source switching and offset changes across versions | LWP source and offset correction method differs by release: 2017 cases use AERIoe for LWPless than 50 g/m2 and MWRRet1 offset by -3.5 g/m2 for LWPgreater than 50 g/m2; 2018+ cases use... | Documented in Appendix A change log; check version used | (hb p. 38) |
| Statistics output averaging bugs in Alpha 1 | Many bugs related to averaging in WRF statistics output in Alpha 1 release produce erroneous stat variables | Fixed in Alpha 2; recommend avoiding using statistics variables from Alpha 1 release | (hb p. 40) |
| SAM Alpha 1 uninitialized variable error | Uninitialized array related to background aerosol in Morrison microphysics caused erroneous SAM statistical output in Alpha 1 | Fixed in Alpha 2; recommend using newer 2015 (Alpha 2 supplement) runs; contact LASSO team if Alpha 1 data specifically needed | (hb p. 41) |
| sam_input_generation.py script errors (pre-2018 fix) | Latent/sensible heat fluxes transposed and a missing-value column absent in SAM-formatted sounding file for versions before the 2018-case fix | Fixed in updated script for 2018 cases release | (hb p. 38) |
| TSI outage substitution | Cloud-fraction time series shows data from site E42 substituted for C1 during periods when the C1 TSI was down (2017 cases onward) | E42 site is less than 1 km from C1 and sees nearly identical cloud field, used as substitute | (hb p. 39) |
| Mid-boundary-layer height definition changed across versions | Mid-boundary-layer moisture/temperature averaging height range changed from a case-specific fixed value (Alpha 2) to a constant 0.5-0.7 km range (2017 v1 cases onward); values not directly... | Documented in change log; users should note version differences when comparing across years | (hb p. 39) |


_29 further items in the report._

## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Gustafson et al. 2020 BAMS 101(4):E462-E479
- Gustafson et al. 2016 DOE/SC-ARM-TR-194 (Alpha 1)
- Gustafson et al. 2017 DOE/SC-ARM-17-031 (Recommendations)
- Gustafson et al. 2018 DOE/SC-ARM-TR-199 (Alpha 2)
- Xie et al. 2004 JGR 109:D01104 (VARANAL)
- Zhang and Lin 1997 JAS 54(11):1503-1524
- Zhang et al. 2001 MWR 129(2):295-311
- Li et al. 2015a JGR 120:654-666 (MSDA)
- Li et al. 2015b MWR 143(9):3804-3822
- Li et al. 2016 IJNMF 82:1035-1048

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-216.pdf (171 pages, DOE/SC-ARM-TR-216, by WI Gustafson, A Vogelmann, X Cheng, KK Dumas, S Endo, KL Johnson, B Krishna, Z Li, T Fairless, H Xiao)
- Catalog record: ARM data-source index, `instrument_class_code=lasso`, read 2026-09-24
- Example file: none - the datastream serves a tar bundle that arrived truncated on repeated download attempts
- Extraction coverage: the report is 171 pages and the extractor reads at most 110,000 characters, so 60 pages were passed - cover, the full 27-page main body, Appendix A release history and Appendix C sub-VAP summaries - and 112 pages of netCDF header dumps were not read
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
