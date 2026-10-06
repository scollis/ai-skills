---
name: arm-vap-arealavealb
description: ARM Areal-Averaged Surface Albedo (arealavealb) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Areal-averaged surface albedo), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparealavealbC1.c1) and the variable inventory of a real file. Use when working with arealavealb data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface/Subsurface Properties. Triggers - arealavealb, Areal-Averaged Surface Albedo, sgparealavealbC1.c1, Areal-averaged surface albedo, Surface/Subsurface Properties.
---

# AREALAVEALB - Areal-Averaged Surface Albedo

The ArealAveAlb VAP estimates areal-averaged, spectrally-resolved surface albedo at four wavelengths (500, 615, 673/675, and 870 nm) from ground-based MFRSR transmission measurements combined with tower-based spectral surface albedo, cloud type, and cloud base height information at ARM sites such as SGP and ENA.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `arealavealb` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-309 / E Kassianov, D Zhang, K Gaustad, G Gibler, J Barnard / October 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-309.pdf) |
| Category | Surface/Subsurface Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2004-01-01 to 2024-02-14 (retired) |
| Datastreams with data | 4 across 4 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/arealavealb |


## Credit

Everything this skill knows about the retrieval is the work of **E Kassianov, D Zhang, K Gaustad, G Gibler, J Barnard** -
the ARM developers and mentors who wrote the technical report it derives from:

> E Kassianov, D Zhang, K Gaustad, G Gibler, J Barnard. *Areal-Averaged Surface Albedo (ArealAveAlb) Value-Added Product*, DOE/SC-ARM-TR-309, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-309.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Surface albedo is the ratio of irradiance reflected from a surface to the downwelling irradiance reaching it, and estimating it over large areas is challenging because towers only measure local albedo while aircraft/satellite methods lack direct incident/reflected radiation measurements. Barnard et al. (2008) introduced a simple analytic expression linking cloud optical depth (tau), surface albedo (A), and asymmetry factor (g) to measured atmospheric transmission under overcast conditions, using MFRSR-measured transmittance at five wavelengths (415, 500, 615, 675, 870 nm). The normalized atmospheric transmission is r_lambda = T_lambda/mu^1.5, where T_lambda is measured atmospheric transmission and mu is the cosine of solar zenith angle. The method first estimates cloud optical depth at 415 nm using Equation (1), assuming or measuring A_415 and g_415, then uses Equation (2) to estimate spectral surface albedo at other wavelengths, assuming cloud optical depth and asymmetry factor are nearly wavelength-independent across 415-870 nm (tau_lambda = tau_415 * c_lambda, with c_lambda close to one; g_lambda = g_415).

**Cadence.** output every 1 min (mfrsrcldod1min.c1, surfspecalb1mlawer.c1) (hb p. 9).

## Inputs

The report names these instruments and sibling products: MFRSR, MFRSRCLDOD, SURFSPECALB, cldtype, TSI.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Areal-averaged surface albedo | unitless (ratio) | - | - | (hb p. 10) |
| Cloud optical depth at 415-nm wavelength | unitless | - | - | (hb p. 10) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| MFRSR wavelengths (input) | 415, 500, 615, 675, 870 nm | (hb p. 4) |
| Output wavelengths (areal-averaged surface albedo) | 500, 615, 673, 870 nm | (hb p. 10) |
| Assumed A_415 (if tower measurement unavailable) | 0.04 (snow-free landscapes) | (hb p. 8) |
| Assumed g_415 for liquid water clouds | 0.87 | (hb p. 10) |
| Typical g_415 for ice clouds | 0.80 | (hb p. 10) |
| Coefficient c_lambda at 415 nm | 1.0 | (hb p. 11) |
| Coefficient c_lambda at 500 nm | 0.99 | (hb p. 11) |
| Coefficient c_lambda at 615 nm | 1.005 | (hb p. 11) |
| Coefficient c_lambda at 675 nm | 0.96 | (hb p. 11) |
| Coefficient c_lambda at 870 nm | 0.96 | (hb p. 11) |
| Cloud optical depth threshold for MFRSRCLDOD applicability | optical depths greater than 7 for snow-free locations | (hb p. 9) |


## The data

Verified example: **`sgparealavealbC1.c1`**, file `sgparealavealbC1.c1.20220625.060000.nc`
(23.05 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4320, `bound`=2, `layer`=10, `height`=596, `filter`=5 |
| Data variables | 58 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2022-06-25T06:00:00 to 2022-06-26T05:59:40 |
| dod version | arealavealb-c1-1.5 |
| process version | not_specified |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `areal_ave_surface_albedo` | 1 | time,filter | yes | Areal average surface albedo |
| `areal_daily_ave_surface_albedo` | 1 | filter | yes | Areal daily average surface albedo |
| `cloud_base_best_estimate` | m | time | yes | Cloud base best estimate, based on ceilometer and micropulse lidar |
| `cloud_layer_base_height` | m | time,layer | yes | Cloud base height (AGL) |
| `cloud_layer_top_height` | m | time,layer | yes | Top height (AGL) of hydrometeor layers, based on combined radar and... |
| `cloud_optical_depth` | 1 | time,filter | yes | Cloud Optical Depth |
| `cloudfraction` | 1 | time | yes | Estimated Average Fractional Sky Cover over the Hemispheric Dome (cf) |
| `cloudtype` | 1 | time,layer | yes | Cloud type |
| `cosine_solar_zenith_angle` | 1 | time | yes | Cosine Solar Zenith Angle |
| `ir_temp` | K | time | yes | IR Brightness Temperature |
| `lwp` | mm | time | yes | Total liquid water along LOS path, it could come from either MWR or... |
| `normalized_transmittance` | 1 | time,filter | yes | Normalized transmittance |
| `optical_depth_average` | 1 | time | yes | Five-Minute Running Average of Cloud Optical Depth |
| `percent_opaque` | % | time | yes | Percent opaque cloud |
| `percent_thin` | % | time | yes | Percent thin cloud |
| `precipitation` | mm/min | time | yes | Mean precipitation rate |
| `reflectivity` | dBZ | time,height | yes | Best estimate reflectivity from ARSCL product |
| `screened_areal_ave_surface_albedo` | 1 | time,filter | yes | Screened areal average surface albedo |
| `screened_areal_daily_ave_surface_albedo` | 1 | filter | yes | Screened areal daily average surface albedo |
| `surface_albedo415` | 1 | time | yes | Surface albedo at 415nm |
| `total_transmittance_filter1` | 1 | time | yes | Total transmittance of Narrowband Hemispheric Irradiance, Filter 1 |
| `total_transmittance_filter2` | 1 | time | yes | Total transmittance of Narrowband Hemispheric Irradiance, Filter 2 |
| `total_transmittance_filter3` | 1 | time | yes | Total transmittance of Narrowband Hemispheric Irradiance, Filter 3 |
| `total_transmittance_filter4` | 1 | time | yes | Total transmittance of Narrowband Hemispheric Irradiance, Filter 4 |
| `total_transmittance_filter5` | 1 | time | yes | Total transmittance of Narrowband Hemispheric Irradiance, Filter 5 |
| `areal_daily_ave_surface_albedo_nsamples` | 1 | filter | - | Number of samples available to determine... |
| `filter` | nm | filter | - | Wavelength of each of the 5 filters measured by the MFR radiometers |
| `height` | m | height | - | Height above ground level |
| `layer` | 1 | layer | - | Cloud layer number |
| `source_surface_albedo415` | 1 | time | - | Source for variable: Surface albedo at 415nm |


_1 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgparealavealbC1.c1",
                             "start": "2022-06-25", "end": "2022-06-25", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgparealavealbC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgparealavealbC1.c1", "2022-06-25", "2022-06-25")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgparealavealbC1.c1", "2022-06-25", "2022-06-25"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cloudfraction", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 58 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgparealavealbC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["cosine_solar_zenith_angle", "cloudfraction", "lwp", "qc_cosine_solar_zenith_angle", "qc_cloudfraction", "qc_lwp"],
                                cleanup_qc=True)
```

## Quality control in this product

25 `qc_` companion variables cover 25 of the
58 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_cosine_solar_zenith_angle"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("cosine_solar_zenith_angle", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["cosine_solar_zenith_angle", "cloudfraction", "lwp"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgparealavealbC1.c1.20220625.060000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `screened_areal_daily_ave_surface_albedo` | areal_ave_surface_albedo had 50 or fewer good samples, data set... | 5 | 100.0 |
| `areal_daily_ave_surface_albedo` | areal_ave_surface_albedo had 50 or fewer good samples, data set... | 5 | 100.0 |
| `optical_depth_average` | Transformation could not finish (all values bad or outside... | 4286 | 99.213 |
| `reflectivity` | Transformation could not finish (all values bad or outside... | 2476673 | 96.1919 |
| `cloudtype` | Transformation could not finish (all values bad or outside... | 40548 | 93.8611 |
| `cloud_layer_top_height` | Transformation could not finish (all values bad or outside... | 40540 | 93.8426 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgparealavealbC1.c1", "20040101", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Unavailable tower-based 415-nm surface albedo measurement | VAP defaults A_415 to assumed value of 0.04; retrieval only applicable to snow-free environments in this case | If tower-based measurements unavailable, VAP assumes surface albedo of 0.04 at 415 nm representing snow-free landscapes; without these measurements... | (hb p. 8) |
| Assumption failure for snow, ice, and sand surfaces | Assumed A_415=0.04 default is inaccurate for these surface types, leading to biased albedo retrievals | Use measured surface albedo when available rather than the 0.04 default | (hb p. 10) |
| Cloud optical depth threshold requirement | Input MFRSRCLDOD data represent only horizontally homogeneous stratiform clouds with optical depths greater than 7; retrieval not valid for thin or inhomogeneous clouds | - | (hb p. 9) |
| Asymmetry factor (g) dependence on cloud phase | Fixed g_415 assumption (0.87 for liquid, 0.80 for ice) may misrepresent actual cloud asymmetry if cloud type is misclassified | Use cldtype VAP cloud type classification (e.g., liquid vs ice clouds) to help specify asymmetry factor properly | (hb p. 8) |
| Wavelength-independence assumptions for cloud optical depth and asymmetry factor | Retrieved spectral albedo at 500-870 nm relies on assumption that tau and g vary only slightly with wavelength (415-870 nm); any real spectral variation in these cloud parameters not... | Coefficient c_lambda (Table 2) applied to adjust tau_415 to other wavelengths, values kept close to one based on literature (Hu and Stamnes 1993,... | (hb p. 11) |
| Spectral albedo differences between snow-covered and vegetation/soil surfaces | Snow albedo decreases moderately (about 10-20%) with increasing wavelength in 415-870 nm range, while vegetation/soil albedo increases substantially (up to several times) in same range,... | - | (hb p. 11) |
| Surface wetness/soil moisture effect on albedo | Albedo values across all wavelengths show noticeable reduction on wet/precipitating days compared to dry days due to enhanced soil moisture darkening surface | - | (hb p. 11) |
| Ocean surface albedo characteristics | Ocean albedo is relatively low (~0.06 at 500 nm) and decreases slightly (about 10-20%) with increasing wavelength, contributing to differences in areal-averaged albedo estimates between... | - | (hb p. 12) |
| Areal representativeness scale tied to cloud base height | Estimated areal-averaged surface albedo represents a large area with radius more than three times greater than CBH; diurnal changes in retrieved albedo can be driven by CBH variability... | Use CBH information (from input VAPs) to estimate the area represented by the retrieved areal-averaged surface albedo | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Barnard JC, CN Long, EI Kassianov, SA McFarlane, JM Comstock, M Freer, and G McFarquhar. 2008. "Development and evaluation of a simple algorithm to find cloud optical depth with emphasis on thin ice clouds." Open...
- Flynn, D, Y Shi, K-S Lim, and L Riihimaki. 2017. Cloud Type Classification (cldtype) Value-Added Product. DOE/SC-ARM-TR-200.
- Hu, YX, and K Stamnes. 1993. "An accurate parameterization of the radiative properties of water clouds suitable for use in climate models." Journal of Climate 6(4): 728-742
- Jäkel, E, et al. 2024. "Observations and modeling of areal surface albedo and surface types in the Arctic." The Cryosphere 18(3): 1185-1205
- Kassianov, EI, JC Barnard, CJ Flynn, LD Riihimaki, J Michalsky, and GB Hodges. 2014. "Areal-averaged and spectrally-resolved surface albedo from ground-based transmission data alone: Toward an operational retrieval."...
- Kassianov, EI, JC Barnard, CM Flynn, LD Riihimaki, LK Berg, and DA Rutan. 2017. "Areal-averaged spectral surface albedo in an Atlantic coastal area: Estimation from ground-based transmission." Atmosphere 8(7): 123
- Kokhanovsky, AA. 2004. "Optical properties of terrestrial clouds." Earth-Science Reviews 64(3-4): 189-241
- McFarlane, SA, KL Gaustad, EJ Mlawer, CN Long, and J Delamere. 2011. "Development of a high spectral resolution surface albedo product for the ARM Southern Great Plains central facility." Atmospheric Measurement...
- Michalsky, J, Q Min, J Barnard, R Marchand, and P Pilewski. 2003. "Simultaneous spectral albedo measurements near the ARM SGP central facility." JGR-Atmospheres 108(D8): D4254
- Miller, SD, F Wang, AB Burgess, SM Skiles, M Rogers, and TH Painter. 2016. "Satellite-based estimation of temporally resolved dust radiative forcing in snow cover." Hydrometeorology 17(7): 1999-2011

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-309.pdf (17 pages, DOE/SC-ARM-TR-309, by E Kassianov, D Zhang, K Gaustad, G Gibler, J Barnard)
- Catalog record: ARM data-source index, `instrument_class_code=arealavealb`, read 2026-09-24
- Example file: `sgparealavealbC1.c1.20220625.060000.nc` from `sgparealavealbC1.c1`, 23.05 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
