---
name: arm-vap-dlmcprof-wind
description: ARM Doppler Lidar Motion Correction (DLMC) Wind Profiles (dlmcprof-wind) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Eastward wind component, Northward wind component, Vertical wind component, Wind speed, Wind direction, Fit residual), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (mosdlmcprofwindnewsM1.c1) and the variable inventory of a real file. Use when working with dlmcprof-wind data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - dlmcprof-wind, Doppler Lidar Motion Correction (DLMC) Wind Profiles, mosdlmcprofwindnewsM1.c1, Eastward wind component, Northward wind component, Vertical wind component, Wind speed, Wind direction.
---

# DLMCPROF-WIND - Doppler Lidar Motion Correction (DLMC) Wind Profiles 

DLMCPROF-WIND is a value-added product that derives motion-corrected, height-resolved horizontal (and vertical) wind profiles from scanning coherent Doppler lidar radial velocity data collected on a moving platform (e.g., the icebreaker Polarstern during MOSAiC), using platform motion correction and a least-squares wind retrieval.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 12 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `dlmcprof-wind` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-295 / R Newsom, G Gibler / January 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-295.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2019-10-11 to 2020-09-20 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/dlmcprof-wind |


## Credit

Everything this skill knows about the retrieval is the work of **R Newsom, G Gibler** -
the ARM developers and mentors who wrote the technical report it derives from:

> R Newsom, G Gibler. *Doppler Lidar Motion-Correction Wind Profiles (DLMCPROF-WIND) Value-Added Product Report*, DOE/SC-ARM-TR-295, January 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-295.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The Doppler lidar performs DBS scans consisting of six slant-path beams (73 degree elevation) plus one vertical beam, providing motion-corrected radial velocity, attenuated backscatter, and SNR along each beam. Because the platform is moving, the scan surface is tilted rather than flat, so the DLMCPROF-WIND algorithm first interpolates the radial velocities from each beam onto a predefined uniform vertical grid at each height. Then, assuming horizontal homogeneity, the three-dimensional wind vector (u, v, w) at each height level is obtained by solving a least-squares linear system relating the interpolated motion-corrected radial velocities from all beams to the along-beam projection coefficients (functions of true azimuth and elevation angles). This retrieval technique is adapted directly from the least-squares method used in the ground-based DLPROF-WIND VAP, with the beam-to-grid interpolation as the key additional preprocessing step for moving-platform operation.

**Cadence.** input rate DBS scan consisting of six slant-path beams (73 deg elevation) plus one vertical beam; each mosdlmcusrM1.b1 file contains 16 DBS scans with total elapsed time just over 6 minutes; output every Single netCDF output file produced per day; averaging Wind vector computed per scan cycle via least-squares fit over all beams in the scan; mean_snr averaged over nbeams (hb p. 6).

## Inputs

The report names these instruments and sibling products: DLPROF-WIND (Doppler Lidar Horizontal Wind Profiles VAP), DLMC VAP, Doppler Lidar (DL) instrument.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Eastward wind component (u) | m s-1 | - | u_error reported per-profile | (hb p. 8) |
| Northward wind component (v) | m s-1 | - | v_error reported per-profile | (hb p. 8) |
| Vertical wind component (w) | m s-1 | - | w_error reported per-profile | (hb p. 9) |
| Wind speed | m s-1 | - | wind_speed_error reported per-profile; slow... | (hb p. 9) |
| Wind direction | deg | - | wind_direction_error reported per-profile;... | (hb p. 9) |
| Fit residual | m s-1 | - | - | (hb p. 9) |
| Fit correlation coefficient | unitless | - | - | (hb p. 9) |
| Chi squared (chisq) | unitless | - | - | (hb p. 9) |
| Mean signal-to-noise ratio (mean_snr) | unitless | - | - | (hb p. 9) |
| Height above ground level | m | 100 m to 3 km | - | (hb p. 8) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| DBS scan configuration | six slant-path beams with an elevation angle of 73 deg, plus one vertical beam | (hb p. 6) |
| Scans per file | 16 DBS scans per mosdlmcusrM1.b1 file | (hb p. 6) |
| Elapsed time per file | just over 6 minutes | (hb p. 6) |
| SNR threshold | about 0.008 (radial velocity estimates with SNR below this are not used) | (hb p. 6) |
| Range gate size | 30-m range gates | (hb p. 8) |
| Nominal height resolution | 30sin(73deg) = 28.7 m | (hb p. 8) |
| Processing height range | from 100 m up to a maximum height of 3 km | (hb p. 8) |
| Vertical grid spacing | 28.7 m | (hb p. 8) |
| Output file frequency | single netCDF file per day | (hb p. 8) |


## The data

Verified example: **`mosdlmcprofwindnewsM1.c1`**, file `mosdlmcprofwindnewsM1.c1.20200917.001508.nc`
(0.56 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=96, `bound`=2, `height`=103 |
| Data variables | 22 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 901 s |
| File time span | 2020-09-17T00:15:08 to 2020-09-18T00:01:46 |
| dod version | dlmcprofwindnews-c1-1.0 |
| process version | dlmcprof_wind-1.0.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `chisq` | 1 | time,height | - | Chi squared |
| `correlation` | 1 | time,height | - | Fit correlation coefficient |
| `height` | m | height | - | Height above ground level |
| `mean_snr` | 1 | time,height | - | Signal-to-noise ratio averaged over nbeams |
| `nbeams` | 1 | time | - | Number of beams (azimuth angles) used in wind vector estimation |
| `residual` | m/s | time,height | - | Fit residual |
| `scan_duration` | second | time | - | MCUSR scan duration |
| `time` | - | time | - | Time offset from midnight |
| `u` | m/s | time,height | - | Eastward component of wind vector |
| `u_error` | m/s | time,height | - | Estimated error in eastward component of wind vector |
| `v` | m/s | time,height | - | Northward component of wind vector |
| `v_error` | m/s | time,height | - | Estimated error in northward component of wind vector |
| `w` | m/s | time,height | - | Vertical component of wind vector |
| `w_error` | m/s | time,height | - | Estimated error in vertical component of wind vector |
| `wind_direction` | degree | time,height | - | Wind direction |
| `wind_direction_error` | degree | time,height | - | Wind direction error |
| `wind_speed` | m/s | time,height | - | Wind speed |
| `wind_speed_error` | m/s | time,height | - | Wind speed error |


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
                     params={"user": f"{user}:{token}", "ds": "mosdlmcprofwindnewsM1.c1",
                             "start": "2020-09-17", "end": "2020-09-17", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./mosdlmcprofwindnewsM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "mosdlmcprofwindnewsM1.c1", "2020-09-17", "2020-09-17")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("mosdlmcprofwindnewsM1.c1", "2020-09-17", "2020-09-17"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("nbeams")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("mosdlmcprofwindnewsM1.c1", "20191011", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Primary output variables contain missing values where SNR is below the processing threshold (~0.008). Users can apply additional QC by filtering wind estimates with large fit residuals and/or small linear correlation coefficients, by QC based on relative wind speed uncertainty (wspd_error/wspd), and/or by applying a higher SNR threshold than used in the original processing.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| SNR thresholding | Missing values / gaps in wind speed fields in regions where SNR is below the threshold (e.g., SNRless than 0.008), visible as blank/masked regions in time-height plots | Use a threshold value of about 0.008 to reject poor-quality radial velocity data; users can apply a higher SNR threshold than used in original... | (hb p. 6) |
| Platform tilt (moving platform scans) | Wind profile scans are tilted relative to a stationary reference, so radial velocity beams intersect a given height at different horizontal/vertical offsets rather than a common plane | Interpolate radial velocities from each beam to a predefined uniform vertical grid before computing the wind vector (the key modification vs.... | (hb p. 7) |
| Assumption of horizontal homogeneity | Wind vector retrieval at a given height relies on solving a least-squares linear system assuming the wind field is horizontally uniform across the beams; violations would appear as... | - | (hb p. 7) |
| Poor fit quality (large residuals / low correlation) | Large values in the 'residual' variable and/or small values in the 'correlation' variable indicate unreliable wind retrievals | Users can apply additional QC by filtering out wind estimates corresponding to large fit residuals and/or small linear correlation coefficients | (hb p. 9) |
| High relative wind speed uncertainty | Large ratio of wspd_error/wspd indicates unreliable wind speed estimates | Users can perform QC based on the relative wind speed uncertainty (wspd_error/wspd) | (hb p. 9) |
| Slow bias relative to radiosonde | Doppler lidar wind speed shows a slight slow bias of 39 cm s-1 relative to collocated radiosonde observations; wind direction is essentially unbiased | - | (hb p. 10) |
| Fixed vertical grid / height range limitation | Wind profiles are only produced from 100 m up to a maximum height of 3 km with grid spacing of 28.7 m; no retrieval outside this range | - | (hb p. 8) |
| Dependence on number of beams used | Metadata field 'nbeams' records number of beams used in the result; fewer beams (e.g., due to SNR rejection) could reduce retrieval robustness | - | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Newsom, RK, WA Brewer, JM Wilczak, DE Wolfe, SP Oncley, and JK Lundquist. 2017. "Validating Precision Estimates in Horizontal Wind Measurements from a Doppler Lidar." Atmospheric Measurement Techniques 10(3): 1229-1240,...
- Newsom, RK, and R Krishnamurthy. 2022. Doppler Lidar (DL) Instrument Handbook. U.S. Department of Energy, Atmospheric Radiation User Facility, Richland, Washington. DOE/SC-ARM-TR-101.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-295.pdf (12 pages, DOE/SC-ARM-TR-295, by R Newsom, G Gibler)
- Catalog record: ARM data-source index, `instrument_class_code=dlmcprof-wind`, read 2026-09-24
- Example file: `mosdlmcprofwindnewsM1.c1.20200917.001508.nc` from `mosdlmcprofwindnewsM1.c1`, 0.56 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
