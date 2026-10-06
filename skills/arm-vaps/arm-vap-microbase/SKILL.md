---
name: arm-vap-microbase
description: ARM Continuous Baseline Microphysical Retrieval (microbase) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Liquid water content, Ice water content, MWR scale factor, Retrieval flag), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmicrobasepiavgC1.c1) and the variable inventory of a real file. Use when working with microbase data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - microbase, Continuous Baseline Microphysical Retrieval, sgpmicrobasepiavgC1.c1, Liquid water content, Ice water content, MWR scale factor, Cloud Properties.
---

# MICROBASE - Continuous Baseline Microphysical Retrieval

MICROBASE is an ARM value-added product that produces continuous vertical profiles of cloud liquid and ice water content and effective particle radius at ARM fixed and mobile observatories by combining cloud radar reflectivity, microwave radiometer liquid water path, and radiosonde temperature profiles.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 25 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `microbase` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-095 / M Wang, K Johnson, A Zhou, SE Giangrande, M Jensen / November 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-095.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1996-11-08 to 2026-06-21 (retired) |
| Datastreams with data | 28 across 12 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/microbase |


## Credit

Everything this skill knows about the retrieval is the work of **M Wang, K Johnson, A Zhou, SE Giangrande, M Jensen** -
the ARM developers and mentors who wrote the technical report it derives from:

> M Wang, K Johnson, A Zhou, SE Giangrande, M Jensen. *Continuous Baseline Microphysical Retrieval (MICROBASE) Value-Added Product Report*, DOE/SC-ARM-TR-095, November 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-095.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

MICROBASE partitions total measured radar reflectivity (Ztotal) into liquid and ice contributions based on sounding-derived ambient temperature: all ice below -16C, all liquid above 0C, and a linear ice/liquid fraction in between. Ice water content is computed from an empirical Z-IWC relationship (Liu and Illingworth 2000) applicable to 35-GHz reflectivity, and ice effective radius is parameterized as a function of temperature (Ivanova et al. 2001). Liquid water content is computed from reflectivity using a Z-LWC relationship (Liao and Sassen 1994) assuming a reference droplet number concentration, then vertically integrated to a liquid water path and scaled to match the microwave radiometer (MWRRET)-retrieved LWP when the MWR reports greater liquid water than the radar-derived estimate. Liquid effective radius is computed assuming a log-normal droplet size distribution with fixed width and an assumed droplet number concentration (Frisch et al. 1995). The algorithm is coded in Python using ARM Data Integrator (ADI) libraries and outputs NetCDF on the same time-height grid as the ARSCL input VAP.

**Cadence.** input rate ARSCL/KAZR native processed to 4-second time intervals, 30-meter height intervals; output every 4-second time intervals, 30-meter height intervals (KAZR input); daily output files; averaging LWP compared/integrated at each 10 second time point via trapezoid rule vertical integration across cloud layers (hb p. 8).

## Inputs

The report names these instruments and sibling products: ARSCL, MWRRET, INTERPSONDE, KAZR, WACR, MMCR, micropulse lidar (MPL), ceilometer, microwave radiometer (MWR), balloon-borne radiosonde, BBHRP, RIPBE.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Liquid water content (LWC) | g m-3 | min 0.0018 g/m3 (set to 0.0); max... | random uncertainty reported via... | (hb p. 11) |
| Ice water content (IWC) | g m-3 | min 1.55e-05 g/m3 (set to 0.0);... | random uncertainty reported via... | (hb p. 11) |
| Liquid cloud particle effective radius (LiqRe) | um | min 1.46 um; max 16.0 um | random uncertainty reported via... | (hb p. 11) |
| Ice cloud particle effective radius (IceRe) | um | min 14.0 um; max 38.0 um | random uncertainty reported via... | (hb p. 11) |
| MWR scale factor | unitless | - | - | (hb p. 12) |
| Retrieval flag | unitless | - | - | (hb p. 12) |
| Clear/cloudy flag | unitless | - | - | (hb p. 12) |
| Precipitation flag | unitless | - | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Output time-height grid (KAZR input) | 4-second time intervals, 30-meter height intervals, 596 vertical levels total | (hb p. 11) |
| Cloud phase temperature thresholds | T less than = -16C: all ice; T greater than = 0C: all liquid; -16Cless than Tless than 0C: mixed-phase linear fractionation | (hb p. 14) |
| Z-IWC relationship coefficients (Liu and Illingworth 2000) | IWC = 0.097 * Zice^0.59 (g/m3) | (hb p. 14) |
| Ice effective radius relationship (Ivanova et al. 2001) | r_ei = 75.3 + 0.5895*T^2 (um, T in degC) | (hb p. 14) |
| Z-LWC relationship (Liao and Sassen 1994) | LWC = (Z/N0)^(1/1.8) * 3.6, N0 assumed 100 cm-3 | (hb p. 15) |
| Liquid effective radius droplet distribution | log-normal, sigma=0.35, Nd assumed 200 cm-3, r_e = 1.358*r_mode (Frisch et al. 1995) | (hb p. 16) |
| Perturbation parameter values and ranges (Table 5) | a=0.097 (range 0.03-0.22), b=0.59 (fixed), c=75.3 (fixed), d=0.5895 (range 0.23-0.82), g=0.5556 (range 0.5-0.6), sigma=0.35 (range 0.2-0.6) | (hb p. 17) |
| MWR-radar time matching window | nearest-in-time positive stat2_lwp value within 5-minute window of MICROBASE profile time | (hb p. 15) |


## The data

Verified example: **`sgpmicrobasepiavgC1.c1`**, file `sgpmicrobasepiavgC1.c1.20101227.001000.cdf`
(0.48 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=72, `nheights`=233 |
| Data variables | 17 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1200 s |
| File time span | 2010-12-27T00:10:00 to 2010-12-27T23:50:00 |
| process version | $State: vap-microbasepi-1.2-1.sol5_10 $ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Avg_CloudFraction` | unitless | time,nheights | - | Cloud Fraction Averaged over 1200 seconds |
| `Avg_IceEffectiveRadius` | micron | time,nheights | - | Ice Effective Radius in-cloud Averaged over 1200 seconds |
| `Avg_LiqEffectiveRadius` | micron | time,nheights | - | Liquid Effective Radius in-cloud Averaged over 1200 seconds |
| `Avg_Retrieved_IWC` | mg m-3 | time,nheights | - | Retrieved Ice Water Concentration in-cloud Averaged over 1200 seconds |
| `Avg_Retrieved_LWC` | g m-3 | time,nheights | - | Retrieved, MWR-Scaled, Liquid Water Concentration in-cloud Averaged... |
| `Heights` | m ASL | nheights | - | Height of Computed Value |
| `Integrated_CloudFraction` | unitless | time | - | Maximum of Column Cloud Fraction Averaged over 1200 Seconds |
| `MWR_Missing_Percentage` | unitless | time | - | Percentage of profiles with liquid for which MWR data were... |
| `Missing_Ice_Percentage` | unitless | time,nheights | - | Percentage of points where presence of ice could not be determined in... |
| `Missing_Liquid_Percentage` | unitless | time,nheights | - | Percentage of points where presence of liquid could not be determined... |
| `aqc_CloudFraction` | unitless | time | - | Fraction of averaging period time profiles that contain cloud (at any... |
| `aqc_CloudMissing` | unitless | time | - | Fraction of averaging period time profiles for which clear/cloudy... |
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
                     params={"user": f"{user}:{token}", "ds": "sgpmicrobasepiavgC1.c1",
                             "start": "2010-12-27", "end": "2010-12-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmicrobasepiavgC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmicrobasepiavgC1.c1", "2010-12-27", "2010-12-27")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmicrobasepiavgC1.c1", "2010-12-27", "2010-12-27"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("MWR_Missing_Percentage")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpmicrobasepiavgC1.c1", "19961108", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: MICROBASE QC uses a combination statistical-technical method to set min/max allowable value flags per variable (Table 6), transfers/adapts QC flags from antecedent VAPs (e.g., MWRRET qc_stat2_lwp becomes aqc_stat2_lwp, ARSCL qc_ReflectivityClutterFlag feeds retrieval_flag), and reports per-variable bit-packed QC flags (qc_liquid_water_content, qc_ice_water_content, qc_liquid_effective_radius, qc_ice_effective_radius) with bits for out-of-detection-range radar signal, possible clutter, out-of-min/max-range values, bad/questionable MWR LWP input, precipitation indication, and bad/missing radar...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Missing ARSCL or INTERPSONDE data at a time step | No microphysical quantities calculated at that time step (gap in output) | MICROBASE retrieval will not calculate microphysical quantities at any time step that either ARSCL or INTERPSONDE data are missing | (hb p. 2) |
| Missing MWRRET data | Liquid variables not calculated for that time step | Retrieval flag set to '3: MWR not available for LWC scaling'; liquid variables not calculated if MWRRET data missing | (hb p. 2) |
| Dependence on upstream VAPs (ARSCL, MWRRET, INTERPSONDE) | MICROBASE availability is contingent on availability of those input VAPs/instrument streams at a given site | - | (hb p. 2) |
| Empirical Z-IWC relationship validity limits | Errors introduced when ice particles do not match assumed unaggregated midlatitude-cirrus crystal size/shape/density; relationship calibrated for 35-GHz radar signal | - | (hb p. 7) |
| Ice effective radius parameterization assumptions | Assumes constant mass-dimension relationship and bimodal ice PSD typical of midlatitude cirrus; may not represent other cloud regimes | - | (hb p. 7) |
| Radar clutter contamination | ARSCL qc_ReflectivityClutterFlag identifies reflectivity possibly from non-hydrometeor scatterers; retrieval_flag set to '2: Cloud and possible clutter contribution' | Flag reported so users can filter/assess | (hb p. 12) |
| No radar reflectivity data available (instrument malfunction or out-of-range target) | retrieval_flag set to '10: No Reflectivity Data Available' | - | (hb p. 12) |
| MWR-radar liquid water disagreement (MWR sees no liquid but radar reflectivity-derived... | Phase fractionation reevaluated using dry-air temperature; LWCscaled set to 0 under various temperature conditions, or ice_fraction reset to 1.0 | Algorithm reassigns reflectivity to ice or zeroes LWCscaled per temperature thresholds (see Section 4.2.4) | (hb p. 8) |
| Radar sees no cloud but MWR sees liquid | Radar reflectivity-derived LWC is neither scaled nor modified in this case, potentially underestimating LWC relative to MWR | - | (hb p. 9) |
| MWR scaling window miss (no stat2_lwp value within 5-min window) | mwr_scale_factor and LWCscaled set to MISSING for all heights | - | (hb p. 8) |
| Minimum detectable LWC/IWC varies with height | Instrument sensitivity changes with height; minimum detectable value calculated only at lowest height bin and applied as single estimate, though true minimum varies by height | Value may be set to zero | (hb p. 11) |
| Empirical retrievals invalid outside derivation conditions | Retrieved values outside expected physical range (e.g., effective radius of 0.02 um) despite being mathematically possible outputs | All calculated quality flags should be used as guides; min/max allowable value QC flags applied | (hb p. 11) |
| Drizzle contamination of LWC maximum | LWC values up to 25 g/m3 observed but usually attributed to drizzle rather than valid cloud LWC; max valid cutoff set at 2.5 g/m3 | Values above 2.5 g/m3 cutoff flagged as out of min/max range | (hb p. 11) |
| Radar signal out of detection range or clutter (per-variable QC bits) | bit_1 (possible out of detection range) or bit_2 (possible clutter) set on primary variable QC fields, assessment 'Indeterminate' | - | (hb p. 13) |
| Calculated value out of min/max range | bit_3 set on primary variable QC field | Assessment 'Indeterminate' | (hb p. 13) |
| Bad or questionable MWR liquid water path input | bit_4 set on primary variable QC field | Assessment 'Indeterminate' | (hb p. 13) |
| Liquid precipitation present | bit_5 set (precip_flag indicated), assessment 'Indeterminate' | - | (hb p. 13) |
| Bad or missing radar signal | bit_6 set on primary variable QC field, assessment 'Bad' | - | (hb p. 13) |
| Product naming/versioning fragmentation across 20+ year history (MICROBASEPI,... | Different product names and algorithm versions used at different sites/times, complicating cross-site/time comparison | Existing MICROBASEKA and MICROBASEKAPLUS data planned to be reprocessed in 2026 under unified naming as microbase.c1/c0 | (hb p. 2) |
| Different radar frequency inputs (KAZR 35-GHz vs WACR 95-GHz) | Z-IWC and other empirical relationships derived for 35-GHz signal; MICROBASEW uses WACR 95-GHz data with same algorithm framework | - | (hb p. 9) |
| Legacy MMCR-based products lack QC flags or uncertainty estimates | microbasepi and pre-2011 evaluation products at NSA/SGP/TWP have no QC flag or uncertainty fields | - | (hb p. 22) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Clothiaux, EE, TP Ackerman, GG Mace, KP Moran, RT Marchand, MA Miller, and BE Martner. 2000. Journal of Applied Meteorology 39(5): 645–665.
- Frisch, AS, CW Fairall, and JB Snider. 1995. Journal of Atmospheric Science 52(16): 2788–2799.
- Ivanova, D, DL Mitchell, WP Arnott, and M Poellot. 2001. Atmospheric Research 59-60: 89–113.
- Liao, L, and K Sassen. 1994. Atmospheric Research 34(1-4): 231–248.
- Liljegren, JC, EE Clothiaux, GC Mace, S Kato, and X Dong. 2001. Journal of Geophysical Research – Atmospheres 106(D13): 14485–14500.
- Liu, C-L, and AJ Illingworth. 2000. Journal of Applied Meteorology 39(7): 1130–1146.
- Miller, MA, KL Johnson, DT Troyan, EE Clothiaux, EJ Mlawer, and GG Mace. 2003. Proceedings of the Thirteenth ARM Science Team Meeting.
- Turner, DD, SA Clough, JC Liljegren, EE Clothiaux, K Cady-Pereira, and KL Gaustad. 2007. IEEE Transactions on Geoscience and Remote Sensing 45(11): 3680–3690.
- Zhao, C, S Xie, X Chen, MP Jensen, and M Dunn. 2014. Journal of Geophysical Research – Atmospheres 119(9): 5375–5385.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-095.pdf (25 pages, DOE/SC-ARM-TR-095, by M Wang, K Johnson, A Zhou, SE Giangrande, M Jensen)
- Catalog record: ARM data-source index, `instrument_class_code=microbase`, read 2026-09-24
- Example file: `sgpmicrobasepiavgC1.c1.20101227.001000.cdf` from `sgpmicrobasepiavgC1.c1`, 0.48 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
