---
name: arm-vap-surfspecalb
description: ARM Surface Spectral Albedo (surfspecalb) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Downwelling broadband irradiance, Upwelling broadband irradiance, Broadband surface albedo, Narrowband spectral surface albedo), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpsurfspecalb7nch1mlawerC1.c1) and the variable inventory of a real file. Use when working with surfspecalb data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface/Subsurface Properties. Triggers - surfspecalb, Surface Spectral Albedo, sgpsurfspecalb7nch1mlawerC1.c1, Downwelling broadband irradiance, Upwelling broadband irradiance, Broadband surface albedo, Surface/Subsurface Properties.
---

# SURFSPECALB - Surface Spectral Albedo

SURFSPECALB is an ARM value-added product that combines MFRSR downwelling and MFR upwelling shortwave irradiance measurements at SGP (and NSA) towers to produce best-estimate narrowband spectral surface albedo and, for non-snow surfaces, an extrapolated high-spectral-resolution albedo.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 43 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `surfspecalb` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-096 / S McFarlane, K Gaustad, C Long / November 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-096.pdf) |
| Category | Surface/Subsurface Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-04-07 to 2026-08-01 (active) |
| Datastreams with data | 4 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/surfspecalb |


## Credit

Everything this skill knows about the retrieval is the work of **S McFarlane, K Gaustad, C Long** -
the ARM developers and mentors who wrote the technical report it derives from:

> S McFarlane, K Gaustad, C Long. *Spectral Surface Albedo Value-Added Product Report*, DOE/SC-ARM-TR-096, November 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-096.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP uses multifilter radiometers (MFRs) facing downward and multifilter rotating shadowband radiometers (MFRSRs) facing upward, which measure spectral irradiance in 10-nm-wide filters centered at 415, 500, 615, 870, 940, and (post-2021) 1625 nm, plus (pre-2021) an uncalibrated broadband 'open' channel; the MFRSR's rotating shadowband periodically shades the instrument to allow separation of diffuse and total downwelling irradiance, with direct irradiance derived as the difference. Narrowband and broadband albedo are calculated as the ratio of upwelling to downwelling irradiance after screening and best-estimate backfilling of the irradiance measurements. Best-estimate narrowband albedos are then used to determine daily surface type (snow, vegetation, partial vegetation, or 0% vegetation/brown) via albedo thresholds and a version of NDVI computed from the 673-nm and 870-nm channels. For non-snow surfaces, piecewise continuous functions derived from spectral albedo libraries extrapolate the narrowband measurements to high-spectral-resolution albedo (820 to 50,000 cm-1 at 10 cm-1 resolution, 60-s temporal resolution), scaled by the daily surface type/vegetation fraction and the best-estimate narrowband albedos at each time.

**Cadence.** input rate 60-s common time grid; 5-minute moving window averaging applied; output every 60-s (1-min) output; averaging irradiances averaged over a 5-minute moving window to address data logger drift (hb p. 6).

## Inputs

The report names these instruments and sibling products: BEFLUX (Best-Estimate Flux VAP), BBHRP (Broadband Heating Rate Profiles VAP), RSS (rotating shadowband spectroradiometer), SWS (shortwave spectroradiometer), TSI (total sky imager), MFRSR, MFR, PSP (precision spectral pyranometer).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Downwelling broadband irradiance (best estimate) | W/m^2 | - | - | (hb p. 6) |
| Downwelling narrowband spectral irradiance | W/m^2 (implied) | - | - | (hb p. 7) |
| Upwelling broadband irradiance (MFR10M_BB, MFR25M_BB) | W/m^2 | - | - | (hb p. 14) |
| Upwelling narrowband spectral irradiance (MFR10M_NB,... | W/m^2 (implied) | - | - | (hb p. 14) |
| Broadband surface albedo | unitless (ratio) | - | - | (hb p. 17) |
| Narrowband spectral surface albedo | unitless (ratio) | - | - | (hb p. 17) |
| High-spectral-resolution surface albedo | unitless (ratio) | 820 to 50,000 cm-1 | standard deviation less than 0.015 vs PSP... | (hb p. 28) |
| NDVI (Normalized Difference Vegetation Index, MFR-derived) | unitless | -1 to +1 | - | (hb p. 35) |
| Surface type / vegetation fraction | categorical / percent | 0-100% vegetation, or snow | - | (hb p. 29) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| MFR/MFRSR filter bands | 10-nm-wide filters centered at 415 nm, 500 nm, 615 nm, 870 nm, 940 nm, and (7-channel period) 1625 nm | (hb p. 7) |
| Output temporal resolution | 60-s | (hb p. 3) |
| High-resolution spectral albedo resolution | 1-min temporal, 10 cm-1 spectral resolution, 820 to 50,000 cm-1 | (hb p. 32) |
| MFRSR to 6-to-7 channel transition (SGP) | January 13, 2021 | (hb p. 7) |
| MFRSR to 6-to-7 channel transition (NSA) | June 23, 2021 | (hb p. 7) |
| Inter-MFRSR broadband ratio limit | narrower limits (unspecified numeric) for inter-MFRSR test | (hb p. 6) |
| Overcast threshold (BEFlux_DOWN) | less than  200 W/m^2 | (hb p. 6) |
| Downwelling narrowband inter-instrument ratio limit | 0.9 to 1.1 | (hb p. 10) |
| Upwelling irradiance ratio limits (MFR10M vs BEFlux_UP;... | 0.75 to 1.75 | (hb p. 14) |
| Upwelling standard deviation of percent difference cutoff | 0.03 | (hb p. 15) |
| Cosine solar zenith angle removal limit (upwelling... | cos(SZA) less than  0.15 removed | (hb p. 15) |
| Maximum upwelling broadband limit (counts) | decreased from 5000 to 1000 counts | (hb p. 15) |
| MFR10M/MFR25M/PSP25M broadband minimum | 0 W/m^2 | (hb p. 15) |
| Albedo calculation filter threshold | downwelling broadband BEFlux1long less than  greater of 50 W/m^2 and cos(SZA at solar noon) x 100 is filtered out | (hb p. 17) |
| Direct/diffuse sky condition threshold | direct/total irradiance ratio 15% | (hb p. 18) |
| Direct albedo fit inclusion threshold | direct/total irradiance ratio greater than  20% | (hb p. 21) |
| Albedo noon minimum sample count | 50 good diffuse (or combined) points | (hb p. 18) |
| Bad data correction limit | not corrected if continuous bad data greater than  30 minutes | (hb p. 13) |
| End-of-bad-period good data requirement | 5 or more minutes of good data | (hb p. 13) |
| Anomalous albedo morning/evening threshold | difference greater than = 0.05 | (hb p. 25) |
| Anomalous albedo near-noon threshold | difference greater than = 0.03 | (hb p. 25) |
| Morning/evening solar zenith test range | mu0 falling from 20 to 35% of available mu0 range | (hb p. 25) |
| Near-noon solar zenith test range | mu0 falling from 65 to 80% of available mu0 range | (hb p. 25) |
| Snow surface criteria | alpha(415) greater than  0.17 && alpha(615)/alpha(870) greater than  0.65 | (hb p. 30) |
| 100% vegetation criteria | NDVI greater than = 0.58 | (hb p. 30) |
| Partial vegetation criteria | 0.25 less than  NDVI less than  0.58 | (hb p. 30) |


_2 further rows in the report._

## The data

Verified example: **`sgpsurfspecalb7nch1mlawerC1.c1`**, file `sgpsurfspecalb7nch1mlawerC1.c1.20260729.060000.nc`
(58.23 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2, `filter`=7, `wavenumber`=4918 |
| Data variables | 65 |
| QC variables | 28 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-07-29T06:00:00 to 2026-07-30T05:59:00 |
| dod version | surfspecalb7nch1mlawer-c1-1.2 |
| process version | vap-surfspecalb1mlawer-2.17-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `be_hemisp_narrowband_mfrsr` | W/m^2 | time,filter | yes | Best estimate Best measured hemispheric narrowband irradiance from... |
| `be_surface_albedo_mfr_narrowband_10m` | 1 | time,filter | yes | Best estimate Narrowband surface albedo at the 10m tower |
| `be_surface_albedo_mfr_narrowband_25m` | 1 | time,filter | yes | Best estimate Narrowband surface albedo at 25m on the 60m tower |
| `be_surface_albedo_psp_broadband_10m` | 1 | time | yes | PSP broadband surface albedo at the 10m tower... |
| `be_surface_albedo_psp_broadband_25m` | 1 | time | yes | PSP broadband surface albedo at 25m on the 60m tower... |
| `be_up_hemisp_narrowband_mfr10mC1` | W/(m^2 nm) | time,filter | yes | Best estimate 10 meter narrowband upwelling hemispheric irradiance |
| `be_up_hemisp_narrowband_mfr25mC1` | W/(m^2 nm) | time,filter | yes | Best estimate 25 meter narrowband hemispheric irradiance |
| `broadband_from_spectral_albedo_10m` | 1 | time | yes | Broadband albedo at 10m tower estimated from integrating spectral... |
| `broadband_from_spectral_albedo_25m` | 1 | time | yes | Broadband albedo at 25m tower estimated from integrating spectral... |
| `cosine_solar_zenith_angle_mfr10mC1` | 1 | time | yes | 10 meter Cosine Solar Zenith Angle |
| `cosine_solar_zenith_angle_mfr25mC1` | 1 | time | yes | 25 meter Cosine Solar Zenith Angle |
| `diffuse_hemisp_narrowband_mfrsrC1` | W/(m^2 nm) | time,filter | yes | Narrowband Diffuse Hemispheric Irradiance for mfrsrC1 |
| `diffuse_hemisp_narrowband_mfrsrE13` | W/(m^2 nm) | time,filter | yes | Narrowband Diffuse Hemispheric Irradiance for mfrsrE13 |
| `direct_normal_narrowband_mfrsrC1` | W/(m^2 nm) | time,filter | yes | Narrowband Direct Normal Irradiance for mfrsrC1 |
| `direct_normal_narrowband_mfrsrE13` | W/(m^2 nm) | time,filter | yes | Narrowband Direct Normal Irradiance for mfrsrE13 |
| `down_short_hemisp_beflux1longC1` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance for beflux1longC1 |
| `estimated_spectral_albedo_10m` | 1 | time,wavenumber | yes | Spectral albedo estimated from mfr albedos using surface type and... |
| `estimated_spectral_albedo_25m` | 1 | time,wavenumber | yes | Spectral albedo estimated from mfr albedos using surface type and... |
| `hemisp_narrowband_mfrsr` | W/m^2 | time,filter | yes | Best measured hemispheric narrowband irradiance from mfrsrC1 and/or... |
| `hemisp_narrowband_mfrsrC1` | W/(m^2 nm) | time,filter | yes | Narrowband Hemispheric Irradiance for mfrsrC1 |
| `hemisp_narrowband_mfrsrE13` | W/(m^2 nm) | time,filter | yes | Narrowband Hemispheric Irradiance for mfrsrE13 |
| `short_direct_normal_beflux1longC1` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance for beflux1longC1 |
| `surface_albedo_mfr_narrowband_10m` | 1 | time,filter | yes | Narrowband surface albedo at the 10m tower |
| `surface_albedo_mfr_narrowband_25m` | 1 | time,filter | yes | Narrowband surface albedo at 25m on the 60m tower |
| `up_hemisp_narrowband_mfr10mC1` | W/(m^2 nm) | time,filter | yes | 10 meter Narrowband Upwelling Hemispheric Irradiance |
| `up_hemisp_narrowband_mfr25mC1` | W/(m^2 nm) | time,filter | yes | 25 meter Upwelling Hemispheric Irradiance |
| `up_short_hemisp_beflux1longC1` | W/m^2 | time | yes | Upwelling (10 meter) Shortwave Hemispheric Irradiance for... |
| `up_short_hemisp_irt25mC1` | W/m^2 | time | yes | Upwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `filter` | nm | filter | - | Wavelength of each of the filters measured by the MFR radiometers |
| `source_hemisp_narrowband_mfrsr` | 1 | time,filter | - | Source for variable: Best measured hemispheric narrowband irradiance... |


_4 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpsurfspecalb7nch1mlawerC1.c1",
                             "start": "2026-07-29", "end": "2026-07-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsurfspecalb7nch1mlawerC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsurfspecalb7nch1mlawerC1.c1", "2026-07-29", "2026-07-29")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsurfspecalb7nch1mlawerC1.c1", "2026-07-29", "2026-07-29"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("down_short_hemisp_beflux1longC1", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 65 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpsurfspecalb7nch1mlawerC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["hemisp_narrowband_mfrsrC1", "diffuse_hemisp_narrowband_mfrsrC1", "direct_normal_narrowband_mfrsrC1", "qc_hemisp_narrowband_mfrsrC1", "qc_diffuse_hemisp_narrowband_mfrsrC1", "qc_direct_normal_narrowband_mfrsrC1"],
                                cleanup_qc=True)
```

## Quality control in this product

28 `qc_` companion variables cover 28 of the
65 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_hemisp_narrowband_mfrsrC1"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("hemisp_narrowband_mfrsrC1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["hemisp_narrowband_mfrsrC1", "diffuse_hemisp_narrowband_mfrsrC1", "direct_normal_narrowband_mfrsrC1"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpsurfspecalb7nch1mlawerC1.c1.20260729.060000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `broadband_from_spectral_albedo_25m` | be_surface_albedo_mfr_narrowband_25m for one or more of the... | 984 | 68.3333 |
| `estimated_spectral_albedo_25m` | be_surface_albedo_mfr_narrowband_25m for one or more of the... | 984 | 68.3333 |
| `up_hemisp_narrowband_mfr25mC1` | down_short_hemisp_beflux1longC1 is less than 200 W/m^2 | 5957 | 59.0972 |
| `up_hemisp_narrowband_mfr10mC1` | down_short_hemisp_beflux1longC1 is less than 200 W/m^2 | 5957 | 59.0972 |
| `surface_albedo_mfr_narrowband_25m` | down_short_hemisp_beflux1longC1 is less than 200 W/m^2 | 5957 | 59.0972 |
| `be_surface_albedo_psp_broadband_10m` | down_short_hemisp_beflux1longC1 is less than 200 W/m^2 | 851 | 59.0972 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpsurfspecalb7nch1mlawerC1.c1", "19980407", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The .c1 output includes bit-packed QC flags for gridded irradiance values, best-estimate irradiances with QC/status flags, best-estimate albedos with QC flags, and estimated surface type/high-spectral-resolution albedo with QC flags, plus integrated broadband albedo from spectral integration. The .s1 output uses a simple four-state QC representation: good, bad, indeterminate, or missing. Status flags indicate whether irradiance values are measured or estimated. Values where albedo was estimated rather than directly calculated are flagged so users can restrict analysis to directly-calculated...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Loss of broadband channel after 7th-channel MFRSR upgrade | After January 13, 2021 (SGP) / June 23, 2021 (NSA), only narrowband best-estimate values equal to raw measurements are reported; broadband channel, best-estimate estimation logic, surface... | Best-estimate methodology (Sections 5.1-5.4, 5.5.3) is only applicable prior to the transition dates; no estimation of irradiance or albedo is made... | (hb p. 5) |
| Data logger time drift | Small timing errors in irradiance time series | Irradiances averaged over a 5-minute moving window | (hb p. 6) |
| Overcast periods skew ratio tests | Small downwelling irradiance values (BEFlux_DOWN less than  200 W/m^2) cause noisy/unreliable ratio comparisons for albedo estimation | Only ratio test of each MFRSR to BEFlux_DOWN is performed during overcast periods; below 200 W/m^2 with poor agreement, irradiance cannot be estimated | (hb p. 6) |
| Instrument divergence near sunset/sunrise | MFRSRC1 diverges from MFRSRE13 and BEFlux near sunset, visible as a departure in the ratio test plot | The other instrument (e.g., E13) is chosen as best value during this time | (hb p. 7) |
| Broken cloudiness cross-instrument disagreement | Ratio of the two MFRSR values frequently outside the 5% limit during clear-to-overcast transitions | Overcast cross-instrument ratio tests applied; individual instrument (C1 or E13) selected rather than averaging | (hb p. 8) |
| Narrowband filter drift / cross-instrument ratio misbehavior | Narrowband ratios between MFRSRC1 and MFRSRE13 are broader than broadband ratios; 499-nm channel ratio is consistently outside limits, with temporally varying behavior between 18-22 UTC | Broadened inter-instrument ratio limit (0.9-1.1) applied for narrowband; possible filter problem noted but not corrected specifically | (hb p. 11) |
| Possible filter degradation in 499-nm channel | Consistently high ratio in 499-nm channel across multiple sky conditions (clear, overcast, broken cloud) | - | (hb p. 11) |
| Uncorrectable bad/missing data due to insufficient good-data context | Gaps exceeding 30 minutes of continuous bad data, or too few good samples before/after, remain flagged as bad/missing rather than estimated | Estimation limited to periods with continuous bad data less than =30 min and sufficient good samples (greater than =5 min or equal number to bad... | (hb p. 13) |
| Estimation excluded at low downwelling irradiance | No irradiance estimates made when BEFlux1Long downwelling broadband is less than  200 W/m^2 or missing | Estimations skipped under this condition; data left missing/bad | (hb p. 13) |
| Geographic separation of upwelling instruments causes surface-dependent irradiance ratio... | Ratio of MFR10M_BB to MFR25M_BB shows large variation over the year due to differing vegetation under each tower | Use BEFlux1long and PSP as comparison references instead of cross-comparing the two MFRs directly | (hb p. 14) |
| Low sun-angle noise in upwelling standard-deviation test | Large standard deviation of percent difference values concentrated at low sun angles (sunrise/sunset) | Remove samples with cosine solar zenith angle less than  0.15 in preprocessing | (hb p. 15) |
| Anomalous albedo changes (snow, plowing, snowmelt) | Sudden changes in albedo not explained by solar zenith angle; large morning-to-evening or near-noon albedo differences exceeding thresholds (0.05, 0.03) | Best estimates are not determined during these periods; data flagged and albedo set to -9999 if anomaly detected on both tests | (hb p. 25) |
| Snow surface albedo spectral extrapolation not performed | Snow-flagged days show no high-spectral-resolution albedo output | Spectral extrapolation withheld for snow-flagged days due to limited validation cases | (hb p. 29) |
| Snowmelt masking underlying surface | Six MFR spectral channels may fail to detect transition as snow melts and underlying surface becomes visible | Extrapolated albedos for several days after an identified snow case should be treated with caution | (hb p. 29) |
| NDVI threshold dependence on surface/instrument specifics | Vegetated/non-vegetated classification boundaries are empirically tuned and not universal | Thresholds derived from visual inspection of several years of MFR albedo plots; using different channels or FOV may require different thresholds | (hb p. 29) |
| Outlier residuals in integrated vs. measured broadband albedo comparison | Some data points show residuals greater than 0.1 between integrated spectral albedo and PSP-measured broadband albedo, traced to unflagged input data problems | Comparison used as an additional QC check; residuals 0.05-0.1 flagged indeterminate, residuals greater than =0.1 flagged bad and set to -9999 | (hb p. 34) |
| No correction for spatial heterogeneity or cloud cover | Albedo values may not represent broader spatial footprint or account for cloud-induced spectral shifts | Not implemented in current work; noted as needed for accurate radiative flux calculations | (hb p. 35) |
| Systematic tower bias in integrated vs PSP broadband albedo | 10-m MFR integrated values slightly overestimate PSP broadband albedo; opposite (underestimate) true for 25-m MFR | - | (hb p. 34) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Clough et al. 2005, Journal of Quantitative Spectroscopy and Radiative Transfer 91(2): 233-244
- Kiedron, Schlemmer, and Klassen 2006, Rotating Shadowband Spectrometer (RSS) Handbook, DOE/SC-ARM-TR-051
- Pilewskie and Pommier 2007, Shortwave Spectrometer (SWS) Handbook, DOE/SC-ARM-TR-062
- Shi and Long 2002, Best Estimate Radiation Flux Value-Added Procedure, DOE/SC-ARM/TR-008
- McFarlane, Gaustad, Mlawer, Long, and Delamere 2011, Atmospheric Measurement Techniques 4(9): 1713-1733
- Bowker, Davis, Myrick, Stacy, and Jones 1985, NASA Reference Publication 1139
- ASTER Spectral Library 1999
- Myneni, Hall, Sellers, and Marshak 1995, IEEE Transactions on Geoscience and Remote Sensing 33(2): 481-486
- Kustas, Schmugge, Jumes, Jackson, Parry, and Weltz 1993, Journal of Applied Meteorology 32(12): 1781-1790
- Wittich and Hansing 1995, International Journal of Biometeorology 38: 209-215

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-096.pdf (43 pages, DOE/SC-ARM-TR-096, by S McFarlane, K Gaustad, C Long)
- Catalog record: ARM data-source index, `instrument_class_code=surfspecalb`, read 2026-09-24
- Example file: `sgpsurfspecalb7nch1mlawerC1.c1.20260729.060000.nc` from `sgpsurfspecalb7nch1mlawerC1.c1`, 58.23 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
