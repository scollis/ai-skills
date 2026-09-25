---
name: arm-vap-mplcmask
description: ARM Cloud mask from Micropulse Lidar (mplcmask) - value-added product reference from its technical report. Derived from mpl. The retrieval algorithm, reported quantities (cloud_mask, cloud_base, cloud_top, num_cloud_layers, linear_depol_ratio, linear_depol_snr), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgp30smplcmask1zwangC1.c1) and the variable inventory of a real file. Use when working with mplcmask data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - mplcmask, Cloud mask from Micropulse Lidar, sgp30smplcmask1zwangC1.c1, mpl VAP, cloud_mask, cloud_base, cloud_top, num_cloud_layers, linear_depol_ratio, Cloud Properties.
---

# MPLCMASK - Cloud mask from Micropulse Lidar

MPLCMASK is a value-added product that retrieves cloud mask, cloud boundaries (base, top, number of layers) and linear depolarization ratio from fast-switching polarized micropulse lidar (MPL) backscatter, providing a lidar-based cloud product used as input to the ARSCL VAP at ARM fixed and mobile sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 25 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mplcmask` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-098 / D Flynn, C Sivaraman, J Comstock, D Zhang / December 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-098.pdf) |
| Category | Cloud Properties |
| Input instruments | `mpl` |
| Record | 1998-05-22 to 2026-09-23 (active) |
| Datastreams with data | 31 across 27 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mplcmask |


## Credit

Everything this skill knows about the retrieval is the work of **D Flynn, C Sivaraman, J Comstock, D Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Flynn, C Sivaraman, J Comstock, D Zhang. *Micropulse Lidar Cloud Mask (MPLCMASK) Value-Added Product for the Fast-Switching Polarized Micropulse Lidar Technical Report*, DOE/SC-ARM-TR-098, December 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-098.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

MPLCMASK applies instrument corrections (dead-time, afterpulse, background, overlap, energy normalization) to raw MPL photon-count profiles from the fast-switching polarized MPL to compute normalized relative backscatter (NRB) and linear depolarization ratio (LDR), following Campbell et al. (2002) and Flynn et al. (2007) methodology. The cloud detection algorithm of Wang and Sassen (2001) then examines the slope of the range-uncorrected backscattered lidar signal as a function of height to identify potential layers, distinguishes cloud from aerosol or noise using a peak-to-base backscatter ratio threshold (4 below 5 km, 1.5 above 5 km), determines whether a cloud top is actual or attenuation-limited (effective), and distinguishes cloud base from virga/drizzle using the signal slope below the layer base. Additional steps apply range correction for subcloud interference, extend cloud base/top regions, and merge nearby layers, followed by a cluster (point-density) test above 10 km to remove noise-driven false clouds. Output is generated at 30-second temporal and 30-meter vertical resolution, with SONDE temperature/pressure profiles (or a static standard-atmosphere molecular backscatter profile if unavailable) used to compute Rayleigh scattering for calibration/normalization of the signal.

**Cadence.** input rate mplpolfs input at 10-second/15-meter resolution (1-second for ship deployments); output every 30-second, 30-meter output resolution; averaging instrument corrections applied at full resolution then averaged/combined to 30-second/30-meter resolution; 2880 time bins per daily output file (hb p. 9).

## Inputs

ARM's catalog declares these input instrument classes: `mpl`.

The report names these instruments and sibling products: ARSCL VAP, MPL (fast-switching polarized micropulse lidar, mplpolfs datastream), MPLPOLFSSHIPCOR VAP, SONDE (balloon-borne sounding system), MPLCMASKML (planned machine-learning successor VAP), ceilometer (via ARSCL).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| cloud_mask | unitless (0=clear,1=cloud) | 0.5 km to 20 km AGL (algorithm... | - | (hb p. 6) |
| cloud_base | km AGL | - | - | (hb p. 22) |
| cloud_top | km AGL (implied) | - | - | (hb p. 17) |
| num_cloud_layers | count | up to 50 layers... | - | (hb p. 17) |
| linear_depol_ratio (LDR) | unitless ratio | - | - | (hb p. 17) |
| linear_depol_snr | unitless | - | - | (hb p. 17) |
| backscatter (NRB) | - | - | - | (hb p. 17) |
| backscatter_snr | - | - | - | (hb p. 17) |
| cloud_top_attenuation_flag | flag (0/1) | - | - | (hb p. 17) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Output temporal resolution | 30-second time-averaged | (hb p. 6) |
| Output vertical resolution | 30-meter vertical height resolution | (hb p. 6) |
| Algorithm vertical extent | surface to 20 km AGL | (hb p. 6) |
| Reported cloud product range | 0.5 km to 20 km | (hb p. 6) |
| Peak-to-base backscatter ratio threshold (less than =5 km) | 4 | (hb p. 7) |
| Peak-to-base backscatter ratio threshold (greater than 5 km) | 1.5 | (hb p. 7) |
| Actual cloud top slope range | -0.2 to -1.2 | (hb p. 7) |
| Cloud-base extension region | 300 meters below identified base (for base 1-5 km) | (hb p. 8) |
| Cloud-base extension threshold | ratio greater than  3 or slope less than  -4 | (hb p. 8) |
| Cloud-top extension threshold | ratio greater than  1.4 or slope less than  -3.5 | (hb p. 8) |
| Layer merge distance (weak above strong) | within 60 m | (hb p. 8) |
| Layer merge distance (top-to-base gap) | within 500 meters | (hb p. 8) |
| Cluster test grid | 5x5 grid of bins, applied above 10 km | (hb p. 8) |
| Cluster test cloud-bin condition 1 | less than 7 of 24 surrounding bins are cloud | (hb p. 8) |
| Cluster test cloud-bin condition 2 | less than 4 of those 7 cloud bins at different time/height | (hb p. 8) |
| Scene variability window (attenuation test) | 13 time steps | (hb p. 4) |
| Scene variability threshold (attenuated flag) | less than 1 above cloud top | (hb p. 4) |
| Backscatter SNR attenuation flag threshold | below 1.0 between cloud top and 30 m below cloud top | (hb p. 16) |
| MPL laser pulse energy | ~10 microJ | (hb p. 9) |
| MPL pulse rate | 2500 Hz | (hb p. 9) |
| Input mplpolfs native resolution (typical fixed site) | 10-second and 15-meter | (hb p. 9) |
| Input mplpolfs native resolution (ship deployment) | 1-second (processed by MPLPOLFSSHIPCOR to standard resolution) | (hb p. 9) |
| Background correction averaging region | 7 km of the last 10-km region (highest altitude), last 3 km of highest altitude ignored | (hb p. 11) |
| Backscatter SNR rolling window | 3 minutes, no vertical averaging | (hb p. 11) |
| Height dimension of output | 667 range bins | (hb p. 18) |
| Time dimension of output | 2880 time bins per day (30-s resolution) | (hb p. 18) |


_2 further rows in the report._

## The data

Verified example: **`sgp30smplcmask1zwangC1.c1`**, file `sgp30smplcmask1zwangC1.c1.20260920.000003.nc`
(24.16 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=2880, `bound`=2, `height`=667, `layer`=50, `num_deadtime_corr`=18 |
| Data variables | 30 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2026-09-20T00:00:03 to 2026-09-20T23:59:36 |
| dod version | 30smplcmask1zwang-c1-1.3 |
| process version | vap-mplcmask-1.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `backscatter` | count/us | time,height | yes | Total attenuated backscatter |
| `backscatter_snr` | 1 | time,height | yes | Signal to noise ratio of backscatter |
| `cloud_mask` | 1 | time,height | yes | Cloud mask |
| `linear_depol_ratio` | 1 | time,height | yes | Linear depolarization ratio |
| `linear_depol_snr` | 1 | time,height | yes | Signal to noise ratio for the linear depolarization ratio |
| `afterpulse_correction_copol` | count/us | height | - | Detector afterpulse (copol) from laser flash that has been degraded |
| `afterpulse_correction_cross` | count/us | height | - | Detector afterpulse (cross) from laser flash that has been degraded |
| `background_signal` | count/us | time | - | Background signal |
| `cloud_base` | km | time | - | Lowest cloud base height above ground level (AGL) |
| `cloud_base_layer` | km | time,layer | - | Cloud base for each layer |
| `cloud_top` | km | time | - | Highest cloud top height above ground level (AGL) |
| `cloud_top_attenuation_flag` | 1 | time | - | Flag indicating whether the beam was extinguished at indicated cloud... |
| `cloud_top_layer` | km | time,layer | - | Cloud top for each layer above ground level (AGL) |
| `deadtime_correction` | 1 | num_deadtime_corr | - | Deadtime correction factor |
| `deadtime_correction_counts` | count/us | num_deadtime_corr | - | Laboratory measured counts used to calculate the deadtime correction... |
| `height` | km | height | - | Vertical height above ground level (AGL) corresponding to the bottom... |
| `num_cloud_layers` | 1 | time | - | Number of cloud layers |
| `overlap_correction` | 1 | height | - | Overlap correction |
| `shots_summed` | 1 | time | - | Number of lidar pulses summed |
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
                     params={"user": f"{user}:{token}", "ds": "sgp30smplcmask1zwangC1.c1",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp30smplcmask1zwangC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp30smplcmask1zwangC1.c1", "2026-09-20", "2026-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgp30smplcmask1zwangC1.c1", "2026-09-20", "2026-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cloud_base")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

5 `qc_` companion variables cover 5 of the
30 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_linear_depol_ratio"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("linear_depol_ratio", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["linear_depol_ratio", "linear_depol_snr", "cloud_mask"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgp30smplcmask1zwangC1.c1.20260920.000003.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `linear_depol_ratio` | The value of signal is zero in the denominator causing the... | 748150 | 38.9467 |
| `linear_depol_snr` | The value of signal is zero in the denominator causing the... | 748150 | 38.9467 |
| `cloud_mask` | Unable to determine the cloud mask, data value set to... | 46080 | 2.3988 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgp30smplcmask1zwangC1.c1", "19980522", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Quality checks are applied to five variables (linear depolarization ratio, cloud_mask, linear depolarization signal-to-noise ratio, backscatter, backscatter signal-to-noise ratio); each has a corresponding qc_ variable in the output. NaNs arising from division by zero (since raw MPL signal can be legitimately zero) are set to missing with appropriate QC bits set. Beam-blocked periods, invalid backscatter, and bad lidar times identified by mentor/translator are flagged with missing values and QC bits. cloud_top_attenuation_flag is set when the backscatter SNR is below 1.0 between cloud top and...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Optically thick cloud attenuation / effective vs actual cloud top | Lidar signal above cloud top drops to near-minimum reliable signal with zero mean slope and strong negative slope within the cloud; reported cloud top is an 'effective' top rather than the... | Algorithm flags whether a top is 'actual' (slope between -0.2 and -1.2) or 'effective'; cloud_top_attenuation_flag set when scene-variability ratio... | (hb p. 6) |
| Near-range instrument correction uncertainty | Cloud detection below 500 m is unreliable/omitted even though algorithm technically runs from the surface | VAP output truncated to above 0.5 km; overlap correction accuracy would need careful assessment before pursuing detection in first several hundred... | (hb p. 6) |
| False cloud / noise clutter above 10 km | Isolated cloud bins above 10 km consisting of only a few range/time bins, often when SNR is poor near the cloud/non-cloud threshold | Cluster (point-density) test using 5x5 grid reassigns isolated bins to clear if fewer than 7/24 surrounding bins are cloud and fewer than 4 of those... | (hb p. 8) |
| Virga/drizzle misidentified as cloud base | Below-cloud signal with smaller-magnitude slope than true cloud signal could otherwise be mistaken for cloud base | Algorithm examines slope below layer base to distinguish virga/drizzle from actual cloud base; range correction applied for subcloud interference in... | (hb p. 7) |
| Beam-blocked conditions near solar noon | Corrected MPL signal set to missing during a window around solar noon; background signal during 4-hour noon window falls below nighttime average background | Beam-blocked periods detected via solar zenith angle and background-signal comparison and set to missing value; QC flags for LDR, backscatter, and... | (hb p. 10) |
| Afterpulse correction unavailability/inaccuracy | Nonphysical negative lidar signal, or slope errors that interfere with distinguishing clear-sky, cloud, and attenuated signal | Default mode applies no afterpulse correction; correction only included if it can be demonstrated to accurately characterize system afterpulse;... | (hb p. 9) |
| Dead-time correction table exceeded by high raw counts | MPL raw counts on a given day exceed the manufacturer's maximum table value | Correction table extended by fitting last three points to a second-order polynomial and extrapolating to the daily maximum observed raw signal | (hb p. 9) |
| Division-by-zero NaNs in backscatter/LDR | Calculated backscatter or LDR fields contain NaNs because raw MPL signal can validly be zero | NaNs are set to missing value and appropriate QC bits are set | (hb p. 12) |
| Invalid backscatter signal | Backscatter values replaced with missing value -9999.0 | QC bit set whenever backscatter signal is not valid | (hb p. 11) |
| Bad lidar times from raw datastream | Specific time periods with known instrument/data problems identified by mentor or translator | Flagged as missing based on mentor/translator input; cloud boundaries recalculated after flagging | (hb p. 11) |
| Ship-tilt correction missing data in background region | Lidar signal represented as missing (-999) in the last 3 km of the highest-altitude background-correction region for ship deployment data corrected for ship tilt | Last 3 km of highest-altitude region is ignored when computing the background correction constant | (hb p. 11) |
| Version-to-version disagreement (v1.0.0 vs v0.6) due to correction-order changes | Clear-sky agreement only ~93% (yearly)/90% (daily average) between versions; cloud base height agreement within 60 m only ~81% daily/91% yearly; disagreements greater than 120 m occur ~18%... | Attributed to correct ordering of lidar corrections in v1.0.0 vs v0.6; recommend further evaluation of instrument correction accuracy and algorithm... | (hb p. 22) |
| Instrument swap impact on boundary-layer cloud detection | Performance of new vs old VAP version reversed after MPL serial 107 was swapped for 4212 at SGP on Nov 21, 2018 - new version missed more low boundary-layer clouds after swap while... | Not resolved by handbook; noted as an open question requiring further investigation of instrument-specific corrections | (hb p. 23) |
| Threshold fixed across sites/instruments | Single set of thresholds used regardless of site or instrument, which may reduce boundary-layer cloud detection accuracy at some deployments | Fixed thresholds retained for autonomous, robust operation across sites; future work may test site/instrument-specific threshold tuning | (hb p. 19) |
| Polarization channel separation issues | Full separation of polarization channels has been imperfect in some MPL deployments, affecting LDR quality | Cloud detection algorithm does not depend on LDR, so cloud detection remains possible even when LDR is compromised | (hb p. 19) |
| Lidar signal attenuation in optically thick clouds (general strengths/weaknesses vs radar) | Lidar may fail to detect cloud layers above an optically thick cloud that a co-located radar would detect | ARSCL VAP combines lidar (MPLCMASK) with radar and ceilometer data for a more complete cloud mask | (hb p. 6) |
| Aborted processing when input MPL data unavailable | No MPLCMASK output file generated for that period | VAP aborts if MPL data are not available | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `mpl`: load `arm-instrument-mpl` for its handbook facts and artifacts

### References the report cites

- Campbell, JR, DL Hlavka, EJ Welton, CJ Flynn, DD Turner, JD Spinhirne, VS Scott, and IH Hwang. 2002. Full-Time, Eye-Safe Cloud and Aerosol Lidar Observation at Atmospheric Radiation Measurement Program Sites:...
- Clothiaux, EE, GG Mace, TP Ackerman, TJ Kane, JD Spinhirne, and VS Scott. 1998. An Automated Algorithm for Detection of Hydrometeor Returns in Micropulse Lidar Data. Journal of Atmospheric and Oceanic Technology 15(4):...
- Cromwell E, and DM Flynn. 2019. Lidar Cloud Detection with Fully Convolutional Networks. IEEE WACV 2019, 619-627.
- Flynn CJ, A Mendoza, Y Zheng, and S Mathur. 2007. Novel Polarization-Sensitive Micropulse Lidar Measurement Technique. Optics Express 15(6): 2785-2790.
- Wang, Z, and K Sassen. 2001. Cloud Type and Macrophysical Property Retrieval Using Multiple Remote Sensors. Journal of Applied Meteorology and Climatology 40(10): 1665-1682.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-098.pdf (25 pages, DOE/SC-ARM-TR-098, by D Flynn, C Sivaraman, J Comstock, D Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=mplcmask`, read 2026-09-24
- Example file: `sgp30smplcmask1zwangC1.c1.20260920.000003.nc` from `sgp30smplcmask1zwangC1.c1`, 24.16 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
