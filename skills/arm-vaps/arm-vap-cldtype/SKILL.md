---
name: arm-vap-cldtype
description: ARM Cloud Type Classification (cldtype) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Cloud type, Cloud base best estimate, Cloud layer top height, Cloud layer base height, Precipitation, Reflectivity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpcldtypeC1.c1) and the variable inventory of a real file. Use when working with cldtype data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - cldtype, Cloud Type Classification, sgpcldtypeC1.c1, Cloud type, Cloud base best estimate, Cloud layer top height, Cloud layer base height, Precipitation, Cloud Properties.
---

# CLDTYPE - Cloud Type Classification

The cldtype VAP is a value-added product that classifies up to 10 cloud layers into seven cloud types using cloud base/top/thickness derived from combined ground-based lidar and radar (ARSCL) and surface meteorological (rain rate) data at fixed ARM sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 16 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `cldtype` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-200 / D Flynn, Y Shi, K-S Lim, L Riihimaki / August 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-200.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1996-11-08 to 2026-06-30 (retired) |
| Datastreams with data | 19 across 13 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/cldtype |


## Credit

Everything this skill knows about the retrieval is the work of **D Flynn, Y Shi, K-S Lim, L Riihimaki** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Flynn, Y Shi, K-S Lim, L Riihimaki. *Cloud Type Classification (cldtype) Value-Added Product*, DOE/SC-ARM-TR-200, August 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-200.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The cldtype VAP derives cloud macrophysical quantities (cloud top, base, and thickness) from the ARSCL data product, which merges vertically pointing lidar and radar cloud boundary retrievals into a single composite cloud mask at 1-minute time and 30-m vertical resolution. Lidar detects low- and most mid/high-level clouds but can be limited by strong optical attenuation in dense hydrometeor layers, while radar effectively detects mid/high clouds through lidar-attenuating layers but misses layers with small particles. To ensure completeness, lidar cloud boundaries below 3.5 km that are missing from the ARSCL cloud mask are added in a preliminary step. Cloud layers are screened (removing layers ≤120 m thick, merging layers separated by ≤120 m) before each of up to 10 layers is assigned one of seven cloud types based on predetermined, site-specific thresholds of cloud top, base, and thickness (Tables 1 and 2), following Burleyson et al. 2015 and McFarlane et al. 2013.

**Cadence.** input rate 1 minute / 30 m (matches ARSCL resolution); output every 1 minute; averaging time_bounds offsets of -30, 30 seconds around each 1-minute time step (hb p. 6).

## Inputs

The report names these instruments and sibling products: ARSCL (Active Remotely Sensed Cloud Location), Ka-band ARM Zenith Radar (KAZR), micro pulse lidar (MPL), ceilometer, Surface Meteorological System (MET), Shallow Cumulus VAP, LASSO.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Cloud type | unitless | flag_values 1-7 | - | (hb p. 8) |
| Cloud base best estimate | m | valid_range 0, 25000; flag_values... | - | (hb p. 9) |
| Cloud layer top height | m | - | - | (hb p. 9) |
| Cloud layer base height | m | - | - | (hb p. 10) |
| Precipitation (mean precipitation rate) | mm/min | valid_min 0, valid_max 10 | - | (hb p. 11) |
| Reflectivity (best estimate) | dBZ | valid_min -90, valid_max 50 | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Temporal resolution | 1 minute | (hb p. 6) |
| Vertical resolution | 30 m | (hb p. 6) |
| Number of cloud layers classified | up to 10 layers | (hb p. 6) |
| Number of cloud types | 7 cloud types | (hb p. 6) |
| Minimum cloud layer thickness retained | greater than  120 m (layers ≤ 120 m removed) | (hb p. 7) |
| Minimum separation between layers before merging | ≤ 120 m merged into single layer | (hb p. 7) |
| Rain rate threshold for excluding data (radar attenuation) | greater than  1 mm hr-1 | (hb p. 7) |
| SGP Low clouds thresholds | base less than  3.5 km, top less than  3.5 km, thickness less than  3.5 km | (hb p. 6) |
| SGP Congestus thresholds | base less than  3.5 km, top 3.5-6.5 km, thickness ≥ 1.5 km | (hb p. 6) |
| SGP Deep convection thresholds | base less than  3.5 km, top greater than  6.5 km, thickness ≥ 1.5 km | (hb p. 6) |
| SGP Altocumulus thresholds | base 3.5-6.5 km, top 3.5-6.5 km, thickness less than  1.5 km | (hb p. 6) |
| SGP Altostratus thresholds | base 3.5-6.5 km, top 3.5-6.5 km, thickness ≥ 1.5 km | (hb p. 6) |
| SGP Cirrostratus/Anvil thresholds | base 3.5-6.5 km, top greater than  6.5 km, thickness ≥ 1.5 km | (hb p. 6) |
| SGP Cirrus thresholds | base greater than  6.5 km, top greater than  6.5 km, no thickness restriction | (hb p. 6) |
| TWP Low clouds thresholds | base less than  4 km, top less than  4 km, thickness less than  4 km | (hb p. 6) |
| TWP Congestus thresholds | base less than  4 km, top 4-8 km, thickness ≥ 1.5 km | (hb p. 6) |
| TWP Deep convection thresholds | base less than  4 km, top greater than  8 km, thickness ≥ 1.5 km | (hb p. 6) |
| TWP Altocumulus thresholds | base 4-8 km, top 4-8 km, thickness less than  1.5 km | (hb p. 6) |
| TWP Altostratus thresholds | base 4-8 km, top 4-8 km, thickness ≥ 1.5 km | (hb p. 6) |
| TWP Cirrostratus/Anvil thresholds | base 4-8 km, top greater than  8 km, thickness ≥ 1.5 km | (hb p. 6) |
| TWP Cirrus thresholds | base greater than  8 km, top greater than  8 km, no thickness restriction | (hb p. 6) |


## The data

Verified example: **`sgpcldtypeC1.c1`**, file `sgpcldtypeC1.c1.20260627.000000.nc`
(9.08 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2, `layer`=10, `height`=596 |
| Data variables | 22 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-06-27T00:00:00 to 2026-06-27T23:59:00 |
| dod version | cldtype-c1-1.3 |
| process version | cldtype-1.14.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cloud_layer_base_height` | m | time,layer | yes | Cloud base height (AGL) for up to 10 layers |
| `cloud_layer_top_height` | m | time,layer | yes | Top height (AGL) of hydrometeor layers for up to 10 layers, based on... |
| `cloudtype` | 1 | time,layer | yes | Cloud type |
| `precipitation` | mm/min | time | yes | Mean precipitation rate |
| `reflectivity` | dBZ | time,height | yes | Best estimate reflectivity from ARSCL product |
| `cloud_base_best_estimate` | m | time | - | Cloud base best estimate, based on ceilometer and ARSCL lidar |
| `cloud_base_best_estimate_status` | 1 | time | - | Cloud base best estimate status |
| `cloud_source_flag` | 1 | time,height | - | Instrument source flag for cloud (hydrometeor) detections |
| `cloudtop_instrument` | 1 | time,layer | - | Instrument that detected layer top height |
| `height` | m | height | - | Height above ground level |
| `instrument_availability_status` | 1 | time | - | Indicates instrument data used in the radar retrieved data |
| `layer` | 1 | layer | - | Cloud layer number |
| `source_precipitation` | 1 | time | - | Source for variable: Mean precipitation rate |
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
                     params={"user": f"{user}:{token}", "ds": "sgpcldtypeC1.c1",
                             "start": "2026-06-27", "end": "2026-06-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpcldtypeC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpcldtypeC1.c1", "2026-06-27", "2026-06-27")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpcldtypeC1.c1", "2026-06-27", "2026-06-27"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cloud_base_best_estimate")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

5 `qc_` companion variables cover 5 of the
22 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_cloudtype"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("cloudtype", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["cloudtype", "cloud_layer_top_height", "cloud_layer_base_height"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpcldtypeC1.c1.20260627.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cloudtype` | Cloud layer cannot be determined | 13085 | 90.8681 |
| `cloud_layer_top_height` | Minimum cloud thickness less than  cdepth | 12968 | 90.0556 |
| `cloud_layer_base_height` | Minimum cloud thickness less than  cdepth | 12968 | 90.0556 |
| `reflectivity` | Data value not available in input file, data value has been set... | 602499 | 70.2017 |
| `cloud_base_best_estimate` | valid_cloud_base_height, | 898 | 62.3611 |
| `cloud_base_best_estimate` | clear_sky, | 542 | 37.6389 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpcldtypeC1.c1", "19961108", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The qc_cloudtype, qc_cloud_layer_top_height, qc_cloud_layer_base_height, and qc_precipitation fields contain bit-packed integer QC values where each bit represents a specific QC test; non-zero bits indicate the QC condition described for that bit, and a value of 0 (no bits set) indicates the data passed all QC tests. Bit assessments are labeled either "Bad" or "Indeterminate" depending on severity (e.g., cloud layer cannot be determined = Bad; MMCR/MPL/precipitation data unavailable = Indeterminate; precipitation exceeding threshold = Bad). The qc fields contain information about what input...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Radar signal attenuation during precipitation | Time periods with rain rate greater than  1 mm hr-1 are excluded from cloud-type classification; qc_cloudtype bit_7 (Precipitation greater than  th_precip) flagged as Bad, potentially... | These time periods are not included in classification due to potential cloud-top underestimation or failure to detect some high-level clouds | (hb p. 7) |
| Lidar undetected by radar clouds below 3.5 km | Sensitivity studies at SGP suggest 27% of clouds detected by lidar below 3.5 km are not detected by radar, which could cause missing low-cloud layers in radar-only cloud mask | If lidar cloud boundaries at or below this level are available but not found in the ARSCL cloud mask, the boundaries are added in a preliminary step... | (hb p. 7) |
| Lidar optical attenuation in dense hydrometeor layers | Lidar-detected cloud boundaries may be truncated or missing above a layer with high hydrometeor concentration, limiting detection of clouds above that layer | - | (hb p. 7) |
| Radar failure to detect small-particle cloud layers | Cloud layers with small particles may be absent from radar reflectivity data even though lidar detects them | - | (hb p. 7) |
| Thin/noisy cloud layers filtered out | Cloud layers with thickness ≤ 120 m do not appear as separate classified layers; they are removed prior to classification | Layers with thickness ≤ 120 m are removed as a filtering step to reduce noise | (hb p. 7) |
| Adjacent thin-layer merging | Two distinct cloud layers separated by ≤ 120 m appear merged into a single layer in the output rather than as separate layers | Adjacent cloud layers separated by 120 m or less are merged into a single cloud layer | (hb p. 7) |
| Cloud layer cannot be determined | qc_cloudtype bit_1 set (Bad assessment) indicating cloud layer type could not be determined | - | (hb p. 9) |
| MMCR (radar) unavailability | qc_cloudtype bit_2 and qc_cloud_layer_top/base_height bit_3 set (Indeterminate) when MMCR data not available | - | (hb p. 9) |
| MMCR clutter contamination | qc_cloudtype bit_3 and related qc fields set (Indeterminate) when MMCR clutter detected | - | (hb p. 9) |
| MPL not available | qc_cloudtype bit_4 and related qc fields set (Indeterminate) when MPL data missing | - | (hb p. 9) |
| MPL beam blocked or attenuated | qc_cloudtype bit_5 and related qc fields set (Indeterminate) when MPL beam is blocked or attenuated, potentially truncating detected cloud tops | - | (hb p. 9) |
| Precipitation data not available | qc_cloudtype bit_6 and related qc fields set (Indeterminate) when precipitation data is missing, preventing attenuation screening | - | (hb p. 9) |
| Minimum cloud thickness below cdepth threshold | qc_cloud_layer_top_height/base_height bit_2 set (Bad) when minimum cloud thickness less than  cdepth global attribute value | - | (hb p. 9) |
| cloudtop_instrument reliability ordering | cloudtop_instrument flag values 0-5 indicate which instrument (MMCR best, then MPL layers 1st-5th) detected cloud top; lower numbers indicate higher reliability, so higher flag values... | - | (hb p. 10) |
| cloudtop_instrument and cloud_source_flag unavailable when input datastream missing | cloudtop_instrument only set when arscl1cloth.c1 datastream available (else -9999); cloud_source_flag only set when arsclkazr1kollias.c1 datastream available (else -9999) | - | (hb p. 10) |
| Missing data represented by fill value | Fields such as cloudtype, cloud_base_best_estimate, cloud_layer_top_height, cloud_layer_base_height, precipitation, reflectivity use missing_value = -9999 | - | (hb p. 8) |
| Reflectivity out-of-range values | qc_reflectivity bit_2/bit_3 set (Bad) when reflectivity value is less than valid_min (-90 dBZ) or greater than valid_max (50 dBZ) | - | (hb p. 12) |
| Precipitation out-of-range values | qc_precipitation bit_2/bit_3 set (Bad) when precipitation value is less than valid_min (0) or greater than valid_max (10 mm/min) | - | (hb p. 12) |
| Site-specific threshold applicability | Cloud-type base/top/thickness thresholds differ between SGP (3.5/6.5 km) and TWP (4/8 km) sites; applying wrong site's table would misclassify cloud types | Use the site-specific threshold table (Table 1 for SGP, Table 2 for TWP) | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Burleyson, CD, CN Long, and JM Comstock. 2015. "Quantifying diurnal cloud radiative effects by cloud type in the Tropical Western Pacific." Journal of Applied Meteorology and Climatology 54(6): 1297-1312,...
- McFarlane, SA, CN Long, and J Flaherty. 2013. "A climatology of surface cloud radiative effects at the ARM Tropical Western Pacific sites." Journal of Applied Meteorology and Climatology 52(4): 996-1013,...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-200.pdf (16 pages, DOE/SC-ARM-TR-200, by D Flynn, Y Shi, K-S Lim, L Riihimaki)
- Catalog record: ARM data-source index, `instrument_class_code=cldtype`, read 2026-09-24
- Example file: `sgpcldtypeC1.c1.20260627.000000.nc` from `sgpcldtypeC1.c1`, 9.08 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
