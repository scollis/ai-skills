---
name: arm-vap-dlprof-wstats
description: ARM Doppler Lidar Vertical Velocity Statistics (dlprof-wstats) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Vertical velocity variance, Vertical velocity skewness, Vertical velocity kurtosis, Median vertical velocity, 25th percentile vertical velocity, 75th percentile vertical velocity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpdlprofwstats4newsC1.c1) and the variable inventory of a real file. Use when working with dlprof-wstats data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - dlprof-wstats, Doppler Lidar Vertical Velocity Statistics, sgpdlprofwstats4newsC1.c1, Vertical velocity variance, Vertical velocity skewness.
---

# DLPROF-WSTATS - Doppler Lidar Vertical Velocity Statistics

The DLPROF-WSTATS VAP derives height- and time-resolved clear-air vertical velocity variance, skewness, kurtosis, and cloud-base statistics from ARM ground-based Doppler lidar vertical-staring measurements.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 22 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `dlprof-wstats` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-149 / RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki / May 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-149.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2010-10-22 to 2026-09-23 (active) |
| Datastreams with data | 27 across 17 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/dlprof-wstats |


## Credit

Everything this skill knows about the retrieval is the work of **RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki** -
the ARM developers and mentors who wrote the technical report it derives from:

> RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki. *Doppler Lidar Vertical Velocity Statistics Value-Added Product*, DOE/SC-ARM-TR-149, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-149.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The ARM Doppler lidars operate in the near infrared and are sensitive to aerosol scattering, providing range-resolved radial velocity, signal-to-noise ratio (SNR), and attenuated backscatter measurements while staring vertically most of the time between periodic PPI scans. From 30-minute time series of vertical velocity at each range gate, the algorithm computes the total observed variance, then estimates and removes the noise variance using the autocovariance function (ACF) technique of Lenschow et al. (2000) and Pearson et al. (2009), in which random uncorrelated noise appears as a delta-function spike at the zeroth lag while atmospheric variance is obtained by extrapolating lags 1-5 to lag zero via a straight-line fit. Skewness and kurtosis are computed as normalized third- and fourth-order moments of vertical velocity after filtering out low-SNR data. Cloud-base height is located by finding sharp spikes (via the first derivative) in the range-corrected SNR profile, with the cloud-base vertical velocity taken from the vertical velocity at that height.

**Cadence.** input rate 1 second (vertical staring), 30 m height resolution; output every 10-minute intervals; averaging 30-minute averaging interval (hb p. 9).

## Inputs

The report names these instruments and sibling products: Doppler lidar (dlfpt), Vaisala ceilometer (vceil25k/ceil25k), eddy correlation flux measurement system (ECOR, 30ecor), surface meteorological instrumentation (MET).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Vertical velocity variance (w_variance) | m2 s-2 (implied) | up to 4 km (clear-air) | - | (hb p. 15) |
| Vertical velocity skewness (w_skewness) | unitless | - | - | (hb p. 15) |
| Vertical velocity kurtosis (w_kurtosis) | unitless | - | - | (hb p. 15) |
| Median vertical velocity (w) | ms-1 (implied) | - | - | (hb p. 15) |
| 25th percentile vertical velocity (w_25) | - | - | - | (hb p. 15) |
| 75th percentile vertical velocity (w_75) | - | - | - | (hb p. 15) |
| Median cloud-base height (dl_cbh) | m (implied) | up to 10 km AGL (cloud base) | - | (hb p. 15) |
| 25th percentile cloud-base height (dl_cbh_25) | - | - | - | (hb p. 15) |
| 75th percentile cloud-base height (dl_cbh_75) | - | - | - | (hb p. 15) |
| Median cloud base vertical velocity (cbw) | - | - | - | (hb p. 15) |
| 25th percentile cbw (cbw_25) | - | - | - | (hb p. 15) |
| 75th percentile cbw (cbw_75) | - | - | - | (hb p. 15) |
| Cloud frequency (dl_cloud_frequency) | fraction | - | - | (hb p. 15) |
| Cloud base updraft fraction (cbw_up_fraction) | fraction | - | - | (hb p. 15) |
| Noise (standard deviation of random noise in vertical... | ms-1 (implied) | - | - | (hb p. 15) |
| SNR (snr) | unitless | - | - | (hb p. 15) |
| SNR threshold used in skewness/kurtosis calculation... | unitless | - | - | (hb p. 15) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| PPI scan interval | once every 10 or 15 minutes (depending on site), ~40 seconds to execute | (hb p. 7) |
| Vertical staring temporal resolution | about 1 second | (hb p. 7) |
| Vertical staring height resolution | 30 m | (hb p. 7) |
| VAP averaging interval | 30 minutes | (hb p. 9) |
| VAP reporting interval | 10 minutes (oversampled by factor of 3) | (hb p. 9) |
| Maximum height for clear-air vertical velocity statistics | 4 km | (hb p. 9) |
| Maximum sensing height for cloud-base vertical velocities | 10 km | (hb p. 9) |
| Beam elevation tolerance for vertical staring | within about 0.2 degrees of 90 degrees | (hb p. 9) |
| Number of ACF lags computed | first six lags | (hb p. 10) |
| SNR threshold (typical) for QC | SNRless than 0.008 | (hb p. 11) |
| Noise threshold (typical) for QC | noisegreater than 1 ms-1 | (hb p. 11) |
| Minimum height of lidar-derived vertical velocity statistics | approximately 100 m | (hb p. 16) |
| Typical maximum height (clear-sky, mid-latitude convective... | roughly equal to boundary layer depth (1 to 3 km AGL) | (hb p. 16) |
| Cloud detection peak magnitude threshold | 0.1 km | (hb p. 13) |
| Cloud detection peak vertical separation | between 2 and 15 range bins | (hb p. 13) |
| CBH isolated-value rejection threshold | 1 km (absolute difference with adjacent CBH values) | (hb p. 13) |


## The data

Verified example: **`sgpdlprofwstats4newsC1.c1`**, file `sgpdlprofwstats4newsC1.c1.20251215.000000.nc`
(0.8 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=144, `bound`=2, `height`=133 |
| Data variables | 57 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2025-12-15T00:00:00 to 2025-12-15T23:50:00 |
| dod version | dlprofwstats4news-c1-1.1 |
| process version | vap-dlprof_wstats-1.9-2.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `averaging_time` | s | - | - | Averaging time interval |
| `cbw` | m/s | time | - | Median cloud base vertical velocity from Doppler lidar |
| `cbw_25` | m/s | time | - | Cloud base vertical velocity 25th percentile from Doppler lidar |
| `cbw_75` | m/s | time | - | Cloud base vertical velocity 75th percentile from Doppler lidar |
| `cbw_up_fraction` | 1 | time | - | Cloud base vertical velocity updraft fraction from Doppler lidar |
| `ceil_alt` | m | - | - | Altitude above mean sea level from ceilometer |
| `ceil_cbh` | m | time | - | Median cloud base height from ceilometer |
| `ceil_cbh_25` | m | time | - | Cloud base height 25th percentile from ceilometer |
| `ceil_cbh_75` | m | time | - | Cloud base height 75th percentile from ceilometer |
| `ceil_cbh_zmax` | m | - | - | Maximum detection height for ceil_cbh |
| `ceil_cloud_frequency` | 1 | time | - | Fraction of time that a cloud is detected during averaging period... |
| `ceil_lat` | degree_N | - | - | North latitude from ceilometer |
| `ceil_lon` | degree_E | - | - | East longitude from ceilometer |
| `dl_cbh` | m | time | - | Median cloud base height from Doppler lidar |
| `dl_cbh_25` | m | time | - | Cloud base height 25th percentile from Doppler lidar |
| `dl_cbh_75` | m | time | - | Cloud base height 75th percentile from Doppler lidar |
| `dl_cbh_zmax` | m | - | - | Maximum detection height for dl_cbh |
| `dl_cloud_frequency` | 1 | time | - | Fraction of time that a cloud is detected during averaging period... |
| `ecor_alt` | m | - | - | Altitude above mean sea level from eddy correlation system |
| `ecor_h2o` | mmol/m^3 | time | - | Water vapor density from eddy correlation system |
| `ecor_lat` | degree_N | - | - | North latitude from eddy correlation system |
| `ecor_lon` | degree_E | - | - | East longitude from eddy correlation system |
| `ecor_temp` | K | time | - | Temperature from eddy correlation system |
| `ecor_tke` | m^2/s^2 | time | - | Turbulence kinetic energy from eddy correlation system |
| `ecor_ustar` | m/s | time | - | Friction velocity from eddy correlation system |
| `ecor_w_kurt` | 1 | time | - | Vertical velocity kurtosis from eddy correlation system |
| `ecor_w_skew` | 1 | time | - | Vertical velocity skewness from eddy correlation system |
| `ecor_w_var` | m^2/s^2 | time | - | Vertical velocity variance from eddy correlation system |
| `ecor_wq` | mmol/(s m^2) | time | - | Wq covariance from eddy correlation system |
| `ecor_wt` | K m/s | time | - | Wt covariance from eddy correlation system |


_23 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpdlprofwstats4newsC1.c1",
                             "start": "2025-12-15", "end": "2025-12-15", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpdlprofwstats4newsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpdlprofwstats4newsC1.c1", "2025-12-15", "2025-12-15")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpdlprofwstats4newsC1.c1", "2025-12-15", "2025-12-15"))   # cite what you pulled
```

This product carries 57 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpdlprofwstats4newsC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['averaging_time', 'cbw', 'cbw_25'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpdlprofwstats4newsC1.c1", "20101022", "20260924")
```

The report's own note on quality: The DLPROF-WSTATS VAP itself does not fully quality-control the variance, w, and noise fields; users must filter data using the included noise and median SNR fields. Typical thresholds are SNRless than 0.008 and/or noisegreater than 1 ms-1, which are effective at removing most poor-quality measurements. The skewness and kurtosis fields already have missing values applied wherever SNR is below the prescribed threshold (default 0.008, saved in the VAP as snr_threshold), but users can raise this threshold for further QC. Ancillary ECOR and MET data are included to help assess lidar-derived...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Random noise contamination of radial velocity/variance | Total variance field shows elevated values relative to true atmospheric variance, especially at low SNR or long range; noise appears as delta-function spike at zeroth lag of ACF | Apply noise correction procedure using ACF extrapolation (lags 1-5 fit to zeroth lag) to obtain noise-corrected atmospheric variance; VAP saves noise... | (hb p. 9) |
| Noise increases with increasing range and decreasing SNR | Radial velocity noise standard deviation rises as SNR decreases, up to receiver bandwidth limit | Filter data using SNR and/or noise thresholds | (hb p. 11) |
| Low SNR / high noise data quality degradation | Regions with SNRless than 0.008 and/or noisegreater than 1 ms-1 show poor-quality measurements, visible as anomalous spikes or unrealistic variance in time-height plots | Reject data with SNRless than 0.008 and/or noisegreater than 1.0 ms-1; VAP provides non-QC'd corrected variance so users must filter themselves | (hb p. 11) |
| Non-quality-controlled variance field | Raw w_variance, w, and noise fields in the VAP have no QC applied (see Figure 8 'no QC' panels), showing spurious high values | Users should filter corrected variances based on noise or median SNR fields | (hb p. 12) |
| Skewness and kurtosis missing values at low SNR | S and K fields contain missing values in regions where SNR is below the prescribed threshold (default 0.008) | Users can impose further QC by increasing the SNR threshold; actual threshold used is saved in VAP as snr_threshold | (hb p. 13) |
| Data gaps in vertical staring record due to periodic PPI scans | Uneven time sampling in the 30-minute vertical velocity time series | Gaps are filled with uniformly spaced NaN samples prior to computing ACF to preserve sample spacing | (hb p. 10) |
| Slant-path staring contamination | dlfpt datastream may occasionally contain slant-path staring data instead of vertical, which would bias vertical velocity statistics if not screened | Algorithm screens staring data to verify beam elevation is within about 0.2 degrees of 90 degrees | (hb p. 9) |
| Limited clear-air sensing height due to near-infrared aerosol dependence | Reliable clear-air radial velocity measurements constrained to lower troposphere; data sparse or unavailable above typical aerosol-laden boundary layer, up to a max processed height of 4 km | Algorithm configured to process clear-air vertical velocity statistics only up to 4 km; cloud-base velocities computed separately up to 10 km due to... | (hb p. 9) |
| False cloud-base detections | Isolated/spurious CBH estimates appearing at a single time step inconsistent with neighboring estimates | Additional checks reject temporally isolated CBH estimates where absolute CBH difference with both neighbors exceeds 1 km; magnitude of derivative... | (hb p. 13) |
| Precipitation bias on vertical velocity statistics | Vertical velocity statistics may be anomalous during precipitation events, coincident with elevated precipitation rate from MET station | VAP includes precipitation rate measurements from surface MET station (smet_spr_mean, mean/max/min) to allow users to identify and account for... | (hb p. 15) |
| Oversampling in reported profiles | Consecutive 10-minute reported profiles are correlated since computed from overlapping 30-minute windows; only every third sample is independent | Note in documentation that profiles are oversampled by a factor of 3 | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Hogan, RJ, ALM Grant, AJ Illingworth, GN Pearson, and EJ O'Connor. 2009. 'Vertical velocity variance and skewness in clear and cloud-topped boundary layers as revealed by Doppler lidar.' Quarterly Journal of the Royal...
- Lenschow, DH, V Wulfmeyer, and C Senff. 2000. 'Measuring Second- through Fourth-Order Moments in Noisy Data.' Journal of Atmospheric and Oceanic Technology 17(10): 1330-1347,...
- Pearson, G, F Davies, and C Collier. 2009. 'An Analysis of the Performance of the UFAM Pulsed Doppler Lidar for Observing the Boundary Layer.' Journal of Atmospheric and Oceanic Technology 26(2): 240-250,...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-149.pdf (22 pages, DOE/SC-ARM-TR-149, by RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki)
- Catalog record: ARM data-source index, `instrument_class_code=dlprof-wstats`, read 2026-09-24
- Example file: `sgpdlprofwstats4newsC1.c1.20251215.000000.nc` from `sgpdlprofwstats4newsC1.c1`, 0.8 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
