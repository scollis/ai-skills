---
name: arm-vap-radfluxanal
description: ARM Radiative Flux Analysis (radfluxanal) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (downwelling_shortwave, clearsky_downwelling_shortwave, clearsky_downwelling_longwave, clearsky_upwelling_shortwave, clearsky_upwelling_longwave), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpradfluxbrs1longC1.c1) and the variable inventory of a real file. Use when working with radfluxanal data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models; Radiometric. Triggers - radfluxanal, Radiative Flux Analysis, sgpradfluxbrs1longC1.c1, downwelling_shortwave, clearsky_downwelling_shortwave, clearsky_downwelling_longwave, clearsky_upwelling_shortwave.
---

# RADFLUXANAL - Radiative Flux Analysis

RADFLUXANAL is an ARM value-added product that analyzes surface broadband shortwave and longwave radiometer measurements to detect clear-sky periods, estimate continuous clear-sky irradiances, and derive fractional sky cover, cloud optical depth, cloud radiative forcing and related cloud macrophysical properties.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 23 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `radfluxanal` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-228 / LD Riihimaki, KL Gaustad, CN Long / September 2019](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-228.pdf) |
| Category | Derived Quantities and Models; Radiometric |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1994-01-07 to 2025-11-29 (retired) |
| Datastreams with data | 79 across 21 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/radfluxanal |


## Credit

Everything this skill knows about the retrieval is the work of **LD Riihimaki, KL Gaustad, CN Long** -
the ARM developers and mentors who wrote the technical report it derives from:

> LD Riihimaki, KL Gaustad, CN Long. *Radiative Flux Analysis (RADFLUXANAL) Value-Added Product: Retrieval of Clear-Sky Broadband Radiative Fluxes and Other Derived Values*, DOE/SC-ARM-TR-228, September 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-228.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The Radiative Flux Analysis technique uses surface broadband SW and LW radiation measurements to detect periods of clear (cloudless) sky, based on magnitude and variability tests on total and diffuse irradiance normalized by the cosine of the solar zenith angle. Empirical least-squares fits of the form Y = a*mu_o^b are made to the identified clear-sky data and interpolated through cloudy periods to produce continuous clear-sky estimates of downwelling and upwelling SW. For LW, effective clear-sky periods are identified from smoothly varying downwelling LW and sky brightness temperature colder than ambient air temperature, and a Brutsaert (1975) formula is fit to derive clear-sky effective emissivity and downwelling LW, again interpolated through cloudy periods. Comparing measured to clear-sky-estimated fluxes then yields derived cloud properties such as fractional sky cover (from the Normalized Diffuse Cloud Effect for SW, and from a Durr and Philipona (2004) look-up table of standard deviation and cloud-free index for LW), cloud optical depth, and cloud radiating temperature.

**Cadence.** input rate 1-minute resolution data used by ARM; output every 1 min; averaging various (11-minute, 21-minute, 7-minute running windows depending on parameter) (hb p. 11).

## Inputs

The report names these instruments and sibling products: QCRAD, SWCLRID, SIRS, BRS, SKYRAD, GNDRAD, MET, IRT.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| downwelling_shortwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_downwelling_shortwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_downwelling_longwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_upwelling_shortwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_upwelling_longwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_diffuse_downwelling_shortwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_direct_downwelling_shortwave | W/m^2 | - | - | (hb p. 9) |
| clearsky_status | Flag--none | 0-9 (1 if SW detected clear sky,... | - | (hb p. 9) |
| cloudfraction_longwave | unitless | - | - | (hb p. 9) |
| cloudfraction_shortwave | unitless | - | - | (hb p. 9) |
| visible_cloud_optical_depth | unitless | only for SWScvgreater than 0.95 | - | (hb p. 9) |
| brightness_temperature | K | - | - | (hb p. 9) |
| cloud_radiating_temperature | K | - | - | (hb p. 9) |
| cloud_transmissivity_shortwave | unitless | - | - | (hb p. 9) |
| clearsky_emissivity_longwave | unitless | - | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Normalized Diffuse Ratio Variability Test Limit | generally 0.0012 for an 11-minute period | (hb p. 11) |
| Minimum clear points for 'clear enough day' | usually set to 110 | (hb p. 11) |
| LW estimate agreement with clear-sky measured LW | about 80% within 4 W/m2 | (hb p. 16) |
| LW estimate agreement with radiative transfer calculations... | within 8 W/m2 (RT itself agrees with clear-sky measurements at 4 W/m2 level) | (hb p. 16) |
| Ice cloud asymmetry parameter | 0.8 (Fu 1996) | (hb p. 15) |
| Liquid water cloud asymmetry parameter | 0.87 (standard) | (hb p. 15) |
| Tice (ice cloudy sky brightness temperature) | 248 K | (hb p. 15) |
| Brutsaert C constant (U.S. standard atmosphere) | 1.24 | (hb p. 17) |
| High-humidity threshold for lapse-rate power-law term | RHgreater than 75-80%, depending on the site | (hb p. 17) |
| LW standard deviation window | 21 minutes | (hb p. 18) |
| LW fractional sky cover smoothing window | 7-minute running mean | (hb p. 18) |
| Cloud optical depth validity | only for sky cover greater than  0.90 (officially valid for overcast skies) | (hb p. 15) |
| Cloud radiating temperature validity | limited to times when LW sky cover is greater than  50% | (hb p. 19) |
| Fractional sky cover solar elevation limit | valid for solar elevation angles greater than 10 degrees | (hb p. 14) |
| SW sky cover field of view | effective 160 degree field of view | (hb p. 14) |


## The data

Verified example: **`sgpradfluxbrs1longC1.c1`**, file `sgpradfluxbrs1longC1.c1.20250819.060000.nc`
(0.36 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 54 |
| QC variables | 12 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2025-08-19T06:00:00 to 2025-08-20T05:59:00 |
| dod version | radfluxbrs1long-c1-1.6 |
| process version | radflux1long-3.17.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `air_temperature` | K | time | yes | Air temperature |
| `diffuse_downwelling_shortwave` | W/m^2 | time | yes | Measured broadband diffuse downwelling shortwave irradiance |
| `direct_downwelling_shortwave` | W/m^2 | time | yes | Measured direct downwelling shortwave irradiance |
| `downwelling_longwave` | W/m^2 | time | yes | Downwelling longwave irradiance from pyrgeometer |
| `downwelling_shortwave` | W/m^2 | time | yes | Broadband downwelling shortwave irradiance from sum or global... |
| `precipitation` | mm | time | yes | Precipitation |
| `pressure` | kPa | time | yes | Atmospheric pressure |
| `relative_humidity` | % | time | yes | Relative humidity |
| `upwelling_longwave` | W/m^2 | time | yes | Upwelling longwave irradiance from pyrgeometer |
| `upwelling_shortwave` | W/m^2 | time | yes | Upwelling shortwave irradiance from pyranometer |
| `wind_direction` | degree | time | yes | Wind direction |
| `wind_speed` | m/s | time | yes | Wind speed |
| `brightness_temperature` | K | time | - | Sky brightness temperature from downwelling_longwave |
| `clearsky_diffuse_downwelling_shortwave` | W/m^2 | time | - | Estimated clear-sky diffuse downwelling shortwave irradiance |
| `clearsky_direct_downwelling_shortwave` | W/m^2 | time | - | Estimated clear-sky direct downwelling shortwave irradiance |
| `clearsky_downwelling_longwave` | W/m^2 | time | - | Estimated clear-sky downwelling longwave irradiance |
| `clearsky_downwelling_shortwave` | W/m^2 | time | - | Estimated clear-sky broadband downwelling shorwave irradiance |
| `clearsky_emissivity_longwave` | 1 | time | - | Effective clear-sky longwave emissivity |
| `clearsky_status` | 1 | time | - | Clear-sky status |
| `clearsky_upwelling_longwave` | W/m^2 | time | - | Estimated clear-sky upwelling longwave irradiance |
| `clearsky_upwelling_shortwave` | W/m^2 | time | - | Estimated clear-sky upwelling shortwave irradiance |
| `cloud_radiating_temperature` | K | time | - | Estimated effective cloud radiating temperature |
| `cloud_transmissivity_shortwave` | 1 | time | - | Shortwave cloud transmissivity |
| `cloudfraction_longwave` | 1 | time | - | Estimated effective longwave fractional sky cover |
| `cloudfraction_shortwave` | 1 | time | - | Estimated shortwave fractional sky cover |
| `cloudfraction_shortwave_status` | 1 | time | - | Status for field: Estimated shortwave fractional sky cover |
| `cosine_zenith` | 1 | time | - | Cosine of solar zenith angle |
| `ice_cloud_temperature_limit` | K | time | - | Temperature limit defined as ice cloud |
| `rh_adjustment_to_clearsky_emissivity_longwave` | 1 | time | - | Fraction of clear sky emissivity due to relative humidity correction |
| `source_diffuse_downwelling_shortwave` | 1 | time | - | Source for variable: Measured broadband diffuse downwelling shortwave... |


_7 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpradfluxbrs1longC1.c1",
                             "start": "2025-08-19", "end": "2025-08-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpradfluxbrs1longC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpradfluxbrs1longC1.c1", "2025-08-19", "2025-08-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpradfluxbrs1longC1.c1", "2025-08-19", "2025-08-19"))   # cite what you pulled
```

This product carries 54 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpradfluxbrs1longC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['air_temperature', 'diffuse_downwelling_shortwave', 'direct_downwelling_shortwave', 'qc_air_temperature', 'qc_diffuse_downwelling_shortwave', 'qc_direct_downwelling_shortwave'],
                                cleanup_qc=True)
```

## Quality control in this product

12 `qc_` companion variables cover 12 of the
54 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_downwelling_shortwave"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("downwelling_shortwave", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["downwelling_shortwave", "downwelling_longwave", "upwelling_shortwave"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpradfluxbrs1longC1.c1.20250819.060000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cloudfraction_shortwave` | no_retrieval | 762 | 52.9167 |
| `cloudfraction_shortwave` | cloudfrac_diffuse | 343 | 23.8194 |
| `cloudfraction_shortwave` | anomalous_clear | 112 | 7.7778 |
| `cloudfraction_shortwave` | cloudeffect_less | 83 | 5.7639 |
| `cloudfraction_shortwave` | anomalous_overcast | 71 | 4.9306 |
| `cloudfraction_shortwave` | overcast_medium | 47 | 3.2639 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpradfluxbrs1longC1.c1", "19940107", "20260924")
```

The report's own note on quality: All input data for RADFLUXANAL are taken from the QCRAD datastream, which applies automated quality control (Long and Shi 2006, 2008) using climatological and data comparison tests on SW/LW fluxes, surface air temperature, humidity, wind speed and IRT data to identify common measurement errors; QCRAD also computes the WMO BSRN-recommended best-estimate total downwelling SW (sum of direct+diffuse with PSP backup, corrected for infrared loss per Dutton et al. 2001 and Younkin and Long 2003). The clearsky_status flag in RADFLUXANAL output (1, 2, 3, 9, or 0) indicates which detection method...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Poor upwelling SW clear-sky fit during and after snow events | Large error in clearsky_upwelling_shortwave during snow accumulation and snow melt periods until next 'clear enough' fitting day | Use daily average of 1100-1300 LST data and a second-pass function vs cosine of solar zenith angle for data with greater than =25% direct SW... | (hb p. 13) |
| Erratic measured albedo (SWup/SWdn) | Albedo ratio behaves erratically through time depending on whether direct sun is blocked by cloud | Use the fitted clear-sky upwelling SW technique instead of raw measured albedo times clear-sky SWdn | (hb p. 13) |
| Clear-sky upwelling LW not fully implemented | clearsky_upwelling_longwave field only contains measured upwelling LW values when downwelling LW is determined clear; otherwise missing | Only measured upwelling clear-sky values used when LW is effectively clear; experimental interpolation method in original code not included in VAP | (hb p. 3) |
| Cloud height estimates not included | No cloud base height variable in output | Excluded from VAP as still very preliminary and often incorrect | (hb p. 3) |
| Cloud radiating temperature is experimental/unpublished | cloud_radiating_temperature shows discrepancies vs IRT especially at low LW sky cover; degraded agreement for LW sky cover less than 50% | Use with caution; retrievals limited to times when LW sky cover greater than 50%; not peer reviewed | (hb p. 3) |
| Cloud optical depth restricted to overcast | visible_cloud_optical_depth reported only when sky cover greater than  0.90 (SWScvgreater than 0.95 per Table 1) | Output limited to overcast cases only | (hb p. 15) |
| Min and Harrison technique overestimates optical depth for thin clouds | Cloud optical depth (Tau) biased high for Tauless than 5 | Use total (global) SW instead of diffuse in formulation to compensate for thin-cloud overestimation (Barnard et al. 2008) | (hb p. 15) |
| One-fit-for-all mode degraded for diffuse/direct components | Diffuse and direct component clear-sky estimates do not fare as well as total SW when only one set of coefficients used for entire run | Use Daily fit mode where climate allows; one-fit mode reserved for infrequently-clear sites/seasons | (hb p. 11) |
| LW clear-sky error during abrupt atmospheric changes | clearsky_downwelling_longwave shows greater error during cold front passages or abrupt temperature/humidity profile changes differing from data used to fit lapse rate coefficients | None specific; noted these conditions occur infrequently | (hb p. 16) |
| LW fractional sky cover limited resolution from oktas-based lookup | cloudfraction_longwave shows discretized jumps consistent with human-observer-derived oktas resolution (inherent uncertainty at least 1/8 of sky cover) | 7-minute running mean smoothing applied to reduce artificial jumps between oktas; future work planned using infrared sky imager | (hb p. 18) |
| LW sky cover insensitive to high, thin clouds | cloudfraction_longwave ("effective LW sky cover") under-represents high/thin cloud amount, representing mainly low and mid-level cloudiness | Termed 'effective LW sky cover' to flag this limitation | (hb p. 18) |
| Clear-sky upwelling LW does not work over water, snow, or ice | Preliminary clear-sky upwelling LW algorithm fails over water, snow, or ice surfaces due to long thermal response time | Not included in VAP; considered still in development | (hb p. 20) |
| Threshold-based artificial variation near clear/overcast boundaries in SW sky cover | Retrieved fractional sky cover can vary artificially compared to actual atmospheric change timescale near clear-sky and overcast thresholds | Additional 11-minute nearly-clear/nearly-overcast smoothing tests applied (MEDFIT fit substitution or running average) | (hb p. 15) |
| Negative Dn ambiguity (clear vs optically thick overcast) | Normalized Diffuse Cloud Effect (Dn) can be negative both for clear skies and for optically thick overcast conditions | Separated using effective transmissivity threshold of 0.4 (SWdn/CSWdn) | (hb p. 14) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Long, CN, and TP Ackerman. 2000. Journal of Geophysical Research – Atmospheres 105(D12) 15609–15626
- Brutsaert, W. 1975. Water Resources Research 11(3): 742–744
- Long, CN, and DD Turner. 2008. Journal of Geophysical Research – Atmospheres 113(D18): D18206
- Durr, B, and R Philipona. 2004. Journal of Geophysical Research – Atmospheres 109(D5): D05201
- Long, CN, TP Ackerman, KL Gaustad, and JNS Cole. 2006. Journal of Geophysical Research – Atmospheres 111(D11): D11204
- Barnard, JC, CN Long, EI Kassianov, SA McFarlane, JM Comstock, M Freer, and GM McFarquhar. 2008. The Open Atmospheric Science Journal 2(1): 46–55
- Barnard, JC, and CN Long. 2004. Journal of Applied Meteorology and Climatology 43(7): 1057–1066
- Long, CN, and Y Shi. 2006. DOE/SC-ARM-TR-074
- Long, CN, and Y Shi. 2008. The Open Atmosphere Science Journal 2: 23–37
- Long, CN, and KL Gaustad. 2004. DOE/SC-ARM-TR-004.1

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-228.pdf (23 pages, DOE/SC-ARM-TR-228, by LD Riihimaki, KL Gaustad, CN Long)
- Catalog record: ARM data-source index, `instrument_class_code=radfluxanal`, read 2026-09-24
- Example file: `sgpradfluxbrs1longC1.c1.20250819.060000.nc` from `sgpradfluxbrs1longC1.c1`, 0.36 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
