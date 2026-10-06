---
name: arm-vap-dlprof-wind
description: ARM Doppler Lidar Wind (dlprof-wind) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Eastward wind component, Northward wind component, Vertical wind component, Wind speed, Wind direction, Fit residual), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpdlprofwind4newsC1.c1) and the variable inventory of a real file. Use when working with dlprof-wind data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - dlprof-wind, Doppler Lidar Wind, sgpdlprofwind4newsC1.c1, Eastward wind component, Northward wind component, Vertical wind component, Wind speed, Wind direction, Atmospheric Profiling.
---

# DLPROF-WIND - Doppler Lidar Wind

The DLPROF-WIND VAP retrieves time- and height-resolved profiles of horizontal wind speed and direction (and vertical velocity) from scanning coherent Doppler lidar PPI (plan-position-indicator) scans using a velocity-azimuth-display (VAD)-based fitting method.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 18 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `dlprof-wind` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-148 / RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki / May 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-148.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2010-11-02 to 2026-09-13 (active) |
| Datastreams with data | 29 across 17 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/dlprof-wind |


## Credit

Everything this skill knows about the retrieval is the work of **RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki** -
the ARM developers and mentors who wrote the technical report it derives from:

> RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki. *Doppler Lidar Wind Value-Added Product*, DOE/SC-ARM-TR-148, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-148.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The ARM Doppler lidars operate in the near infrared (1.5 microns) and provide range-resolved measurements of radial velocity, attenuated aerosol backscatter, and SNR by performing PPI scans (scanning the beam in azimuth at fixed elevation angle) several times per hour. At a fixed range, the conical PPI scan traces a circle centered above the lidar, and as the beam scans in azimuth the radial velocity varies sinusoidally. The u, v, and w wind components are retrieved by fitting a sinusoid to the radial velocity data via a least-squares cost function minimization, where amplitude, phase, and offset of the sinusoid determine wind speed, wind direction, and vertical velocity respectively. Uncertainty estimates for u, v, and w are derived from the diagonal elements of the inverted coefficient matrix (A^-1), and fit quality is assessed via the fit residual and linear correlation coefficient. The derived winds represent averages over the circumference of the scan circle and over the time to complete a full PPI scan.

**Cadence.** input rate PPI scans performed several times per hour; output every one 8-beam PPI scan every 15 minutes (typical), nominally 96 profiles per day; averaging each profile represents a 40 second average taken every 15 minutes (typical); derived winds are averages over the circumference of the scan circle and over the time to complete a full PPI scan (30 seconds to a couple of minutes) (hb p. 11).

## Inputs

The report names these instruments and sibling products: Doppler lidar (dlppi datastream), surface meteorological instrumentation (MET).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Eastward wind component (u) | m/s | - | - | (hb p. 11) |
| Northward wind component (v) | m/s | - | - | (hb p. 11) |
| Vertical wind component (w) | m/s | - | - | (hb p. 14) |
| Wind speed | m/s | - | - | (hb p. 11) |
| Wind direction | degree | - | - | (hb p. 11) |
| Fit residual | m/s | - | - | (hb p. 10) |
| Fit correlation coefficient | unitless | - | - | (hb p. 10) |
| Mean SNR (averaged over nbeams) | unitless | - | - | (hb p. 15) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Wavelength | near infrared (1.5 microns) | (hb p. 6) |
| Typical range gate size | 30-m | (hb p. 10) |
| Typical PPI scan elevation angle | 60o | (hb p. 10) |
| Typical number of beams (azimuth angles) | N=8 evenly spaced beams | (hb p. 10) |
| Typical height resolution | 30sin(60o)=26m | (hb p. 10) |
| Minimum range for Doppler lidar | approximately 100 m | (hb p. 10) |
| Minimum height (for 60o PPI scan) | about 87m | (hb p. 10) |
| Maximum processing height | 3 km | (hb p. 10) |
| SNR threshold value used in QC | about 0.008 | (hb p. 10) |
| Typical PPI scan interval | one 8-beam PPI scan every 15 minutes | (hb p. 11) |
| Typical PPI scan elapse time | roughly 40 seconds | (hb p. 11) |
| Nominal daily profile count | 4x24=96 wind profiles | (hb p. 11) |
| PPI scan duration range | typically anywhere from about 30 seconds to a couple of minutes | (hb p. 7) |


## The data

Verified example: **`sgpdlprofwind4newsC1.c1`**, file `sgpdlprofwind4newsC1.c1.20260826.000224.nc`
(2.43 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=282, `bound`=2, `height`=164 |
| Data variables | 32 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2026-08-26T00:02:24 to 2026-08-26T23:57:08 |
| dod version | dlprofwind4news-c1-1.0 |
| process version | dlprof_wind-1.3.2 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `correlation` | unitless | time,height | - | Fit correlation coefficient |
| `elevation_angle` | degree | time | - | Beam elevation angle |
| `height` | m | height | - | Height above ground level |
| `mean_snr` | unitless | time,height | - | Signal to noise ratio averaged over nbeams |
| `met_alt` | m | - | - | MET altitude |
| `met_dt` | second | - | - | Averaging period length used for MET data |
| `met_lat` | degree_N | - | - | MET latitude |
| `met_lon` | degree_E | - | - | MET longitude |
| `met_spr` | mm/hr | time | - | Mean surface precipitation rate during averaging period from MET |
| `met_spr_max` | mm/hr | time | - | Maximum surface precipitation rate during averaging period from MET |
| `met_spr_min` | mm/hr | time | - | Minimum surface precipitation rate during averaging period from MET |
| `met_wdir` | degree | time | - | Vector mean surface wind direction from MET |
| `met_wspd` | m/s | time | - | Vector mean surface wind speed from MET |
| `nbeams` | unitless | time | - | Number of beams (azimuth angles) used in wind vector estimation |
| `residual` | m/s | time,height | - | Fit residual |
| `scan_duration` | second | time | - | PPI scan duration |
| `snr_threshold` | unitless | - | - | SNR threshold |
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
                     params={"user": f"{user}:{token}", "ds": "sgpdlprofwind4newsC1.c1",
                             "start": "2026-08-26", "end": "2026-08-26", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpdlprofwind4newsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpdlprofwind4newsC1.c1", "2026-08-26", "2026-08-26")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpdlprofwind4newsC1.c1", "2026-08-26", "2026-08-26"))   # cite what you pulled
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
    act.qc.print_dqr("sgpdlprofwind4newsC1.c1", "20101102", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The configuration file contains an SNR threshold (about 0.008) used to reject poor-quality radial velocity data before computing wind profiles. Primary output variables contain missing values where SNR is below threshold. The output also includes fit residual and linear correlation coefficient fields so users can apply additional QC by filtering out estimates with large residuals or small correlation coefficients, and the mean_snr field allows users to apply a higher SNR threshold than used in original processing. MET station variables (wind speed/direction, precipitation rate) are included...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Low SNR / poor backscatter above the boundary layer | Radial velocity data and derived wind profiles become missing (fill value -9999) above roughly 2-3 km as backscatter signal drops dramatically above the aerosol-laden boundary layer | Algorithm is configured to process data only up to a maximum height of 3 km; primary variables contain missing values in regions where SNR is below... | (hb p. 10) |
| Radial velocity estimates below SNR threshold | Missing values in u, v, w, wind_speed, wind_direction and related fields at range gates where SNR is low | Radial velocity estimates corresponding to SNR values below the configured threshold (about 0.008) are excluded from the wind profile computation;... | (hb p. 10) |
| Poor fit quality (large fit residual or low correlation) | Large residual field values or low correlation field values at certain heights/times, indicating unreliable sinusoid fit to radial velocity data | Users can apply additional QC by filtering out wind estimates corresponding to large fit residuals and/or small linear correlation coefficients | (hb p. 10) |
| Precipitation contamination of lidar measurements | Anomalous or degraded wind estimates coinciding with nonzero precipitation rate reported by the MET station | MET precipitation rate variables (met_spr, met_spr_min, met_spr_max) are included in the output to help determine when lidar measurements may be... | (hb p. 10) |
| Minimum range blind zone | No valid wind retrievals below about 87 m height (for a 60-degree elevation PPI scan) due to minimum lidar range of approximately 100 m | - | (hb p. 10) |
| Height resolution dependent on scan geometry | Vertical spacing between range gates in the profile varies with elevation angle and range gate size (e.g., 26 m for 30-m gates at 60-degree elevation), not fixed across all... | - | (hb p. 10) |
| Assumption of horizontally uniform and steady flow | Wind estimates at a given height represent spatial averages over the scan circle circumference and temporal averages over the scan duration; true small-scale or transient wind variability... | - | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Browning, KA, and R Wexler. 1968. "The determination of kinematic properties of a wind field using Doppler radar." Journal of Applied Meteorology 7(1): 105-113
- Newsom, RK, WA Brewer, JM Wilczak, DE Wolfe, SP Oncley, and JK Lundquist. 2017. "Validating Precision Estimates in Horizontal Wind Measurements from a Doppler Lidar." Atmospheric Measurement Techniques 10(3):1229-1240
- Press, WH, SA Teukolsky, WT Vetterling, and BP Flannery. 1988. Numerical Recipes in C. Cambridge University Press, pp. 528-534

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-148.pdf (18 pages, DOE/SC-ARM-TR-148, by RK Newsom, C Sivaraman, TR Shippert, LD Riihimaki)
- Catalog record: ARM data-source index, `instrument_class_code=dlprof-wind`, read 2026-09-24
- Example file: `sgpdlprofwind4newsC1.c1.20260826.000224.nc` from `sgpdlprofwind4newsC1.c1`, 2.43 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
