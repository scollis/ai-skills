---
name: arm-vap-qcecor
description: ARM Quality Controlled Eddy Correlation Flux Measurement (qcecor) - value-added product reference from its technical report. Derived from ecor. The retrieval algorithm, reported quantities (Corrected CO2 flux, Uncorrected CO2 flux), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (ena30qcecorC1.c1) and the variable inventory of a real file. Use when working with qcecor data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface/Subsurface Properties. Triggers - qcecor, Quality Controlled Eddy Correlation Flux Measurement, ena30qcecorC1.c1, ecor VAP, Corrected CO2 flux, Surface/Subsurface Properties.
---

# QCECOR - Quality Controlled Eddy Correlation Flux Measurement

QCECOR is a value-added product that applies eddy-correlation corrections and stringent quality control to raw ECOR data to produce corrected, quality-flagged surface latent heat, sensible heat, and CO2 turbulent flux measurements at ARM sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 19 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `qcecor` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-223 / C Tao, S Xie, RC Sullivan, S Tang, Y Zhang, DR Cook, KL Gaustad / August 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-223.pdf) |
| Category | Surface/Subsurface Properties |
| Input instruments | `ecor` |
| Record | 2003-09-09 to 2025-11-30 (retired) |
| Datastreams with data | 66 across 17 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/qcecor |


## Credit

Everything this skill knows about the retrieval is the work of **C Tao, S Xie, RC Sullivan, S Tang, Y Zhang, DR Cook, KL Gaustad** -
the ARM developers and mentors who wrote the technical report it derives from:

> C Tao, S Xie, RC Sullivan, S Tang, Y Zhang, DR Cook, KL Gaustad. *The QCECOR Value-Added Product: Quality-Controlled Eddy Correlation Flux Measurements*, DOE/SC-ARM-TR-223, August 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-223.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

QCECOR takes the original 30-minute ECOR eddy covariance data (and SEBS wetness data) as input and applies a series of eddy correlation corrections: stability correction, Webb-Pearman-Leuning (WPL) correction, frequency correction, sensor separation correction, filtering correction, line-averaging correction, and volume-averaging correction. These corrections generally increase latent heat flux by 10-30% and sensible heat flux by 10% relative to the uncorrected data, especially during daytime, while CO2 flux corrections (dominated by the WPL correction) can range from 0-50%, with total correction sometimes exceeding 50%. After correction, LLNL applies additional quality control: a data range check on maximum/minimum values, an outlier check using standard deviation departures from the day/night mean, and a temporal variability check using a moving ±3-hour window comparing variability with and without each data point. Data failing any of the original ECOR QC or the LLNL QC checks are flagged qc_flag = 1 (bad) and the corresponding flux value is set to missing (-9999); qc_flag = 0 indicates good data.

**Cadence.** output every 30-min time resolution (one output file per day); averaging bound_offsets -1800., 0. (30-minute averaging window ending at reported time) (hb p. 9).

## Inputs

ARM's catalog declares these input instrument classes: `ecor`.

The report names these instruments and sibling products: ECOR (Eddy Correlation Flux Measurement System), SEBS (Surface Energy Balance System), EBBR (Energy Balance Bowen Ratio), BAEBBR (Bulk Aerodynamic Technique EBBR VAP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Corrected sensible heat flux at surface | W/m^2 | valid_min -300, valid_max 1100 | - | (hb p. 12) |
| Corrected latent heat flux at surface | W/m^2 | valid_min -300, valid_max 1100 | - | (hb p. 13) |
| Corrected CO2 flux | umol/(s m^2) | valid_min -50, valid_max 35 | - | (hb p. 13) |
| Uncorrected sensible heat flux at surface | W/m^2 | valid_min -300, valid_max 1100 | - | (hb p. 14) |
| Uncorrected latent heat flux at surface | W/m^2 | valid_min -300, valid_max 1500 | - | (hb p. 14) |
| Uncorrected CO2 flux | umol/(s m^2) | valid_min -50, fail_max 35 | - | (hb p. 15) |
| Wetness, rain detector | V | - | - | (hb p. 16) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Data range check (night) | flag SH/LH if greater than  150 W/m2 or less than  -150 W/m2 during the night | (hb p. 7) |
| Data range check (day, high insolation) | flag SH/LH if less than  -100 W/m2 when solar insolation is greater than  300 W/m2 | (hb p. 7) |
| Outlier check threshold | flag as bad if departure from day/night mean greater than  4 standard deviations | (hb p. 7) |
| Temporal variability check window | moving window of ± 3 hours centered at the data point | (hb p. 7) |
| Temporal variability threshold (SH/LH) | 25 W/m2 | (hb p. 7) |
| Temporal variability threshold (CO2 flux) | 1.0 µmol/m2/s | (hb p. 7) |
| corrected_sensible_heat_flux valid range | valid_min -300 W/m^2, valid_max 1100 W/m^2 | (hb p. 12) |
| corrected_latent_heat_flux valid range | valid_min -300 W/m^2, valid_max 1100 W/m^2 | (hb p. 13) |
| corrected_co2_flux valid range | valid_min -50 umol/(s m^2), valid_max 35 umol/(s m^2) | (hb p. 13) |
| uncorrected_latent_heat_flux valid range | valid_min -300 W/m^2, valid_max 1500 W/m^2 | (hb p. 14) |
| uncorrected_co2_flux fail_max | 35 umol/(s m^2) | (hb p. 15) |
| Output time resolution | 30-min (30qcecor) | (hb p. 9) |
| Sensor mounting height | 3 m above ground level, except SGP E21 at 15 m above ground on a tall tower | (hb p. 17) |
| missing_value / _FillValue | -9999 | (hb p. 12) |


## The data

Verified example: **`ena30qcecorC1.c1`**, file `ena30qcecorC1.c1.20240907.000000.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=48, `bound`=2 |
| Data variables | 20 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2024-09-07T00:00:00 to 2024-09-07T23:30:00 |
| dod version | 30qcecor-c1-1.2 |
| process version | vap-qcecor-1.8-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `corrected_co2_flux` | umol/(s m^2) | time | yes | Corrected CO2 flux |
| `corrected_latent_heat_flux` | W/m^2 | time | yes | Corrected latent heat flux at surface |
| `corrected_sensible_heat_flux` | W/m^2 | time | yes | Corrected sensible heat flux at surface |
| `uncorrected_co2_flux` | umol/(s m^2) | time | yes | Uncorrected CO2 flux |
| `uncorrected_latent_heat_flux` | W/m^2 | time | yes | Uncorrected latent heat flux at surface |
| `uncorrected_sensible_heat_flux` | W/m^2 | time | yes | Uncorrected sensible heat flux at surface |
| `wetness` | V | time | yes | Wetness, rain detector |
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
                     params={"user": f"{user}:{token}", "ds": "ena30qcecorC1.c1",
                             "start": "2024-09-07", "end": "2024-09-07", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./ena30qcecorC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "ena30qcecorC1.c1", "2024-09-07", "2024-09-07")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("ena30qcecorC1.c1", "2024-09-07", "2024-09-07"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("corrected_sensible_heat_flux", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

7 `qc_` companion variables cover 7 of the
20 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_corrected_sensible_heat_flux"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("corrected_sensible_heat_flux", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["corrected_sensible_heat_flux", "corrected_latent_heat_flux", "corrected_co2_flux"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (ena30qcecorC1.c1.20240907.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `corrected_co2_flux` | Value not available or failed one or more quality control... | 9 | 18.75 |
| `corrected_latent_heat_flux` | Value not available or failed one or more quality control... | 8 | 16.6667 |
| `uncorrected_latent_heat_flux` | Value is equal to missing_value. | 5 | 10.4167 |
| `uncorrected_co2_flux` | Value is equal to missing_value. | 5 | 10.4167 |
| `uncorrected_co2_flux` | Value is less than the fail_min. | 1 | 2.0833 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("ena30qcecorC1.c1", "20030909", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Two QC flags are set for each corrected surface turbulent flux: qc_flag = 0 (good data), qc_flag = 1 (bad data, value set to missing). Data are flagged bad if they were identified as bad in the original ECOR data or failed any of the LLNL QC checks (data range check, outlier/standard-deviation check, temporal variability moving-window check). The qc_corrected_* variables use integer flag_method with flag_1_description "Value not available or failed one or more quality control tests, value set to missing_value" and flag_1_assessment "Bad". The qc_uncorrected_* variables use bit-packed flags...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Original (uncorrected) ECOR data not corrected for common eddy covariance effects and... | Discrepancies between uncorrected_* fields and corrected_* fields; gray line (original ECOR) diverges from black line (QCECOR) in time series plots | Apply eddy correlation corrections and LLNL QC to produce QCECOR product; users suggested to use corrected fluxes | (hb p. 6) |
| Systematic low bias in uncorrected fluxes | Corrections increase LH by 10-30% and SH by 10% relative to original data, especially during daytime; smaller increase at night | Use corrected LH/SH from QCECOR | (hb p. 7) |
| Large WPL/CO2 correction magnitude | CO2 flux corrections from WPL alone range 0-50% of original measured flux; total correction (all corrections combined) can exceed 50% | Corrected CO2 flux validated against community-vetted code EddyPro; use corrected_co2_flux | (hb p. 7) |
| Nighttime and high-insolation flux range failures | SH/LH values greater than  150 W/m2 or less than  -150 W/m2 at night, or less than  -100 W/m2 when insolation greater than  300 W/m2, are flagged bad and set to missing (-9999) | Data range check filters these values out; qc_flag set to 1 | (hb p. 7) |
| Statistical outliers relative to diurnal mean | Data departing more than 4 standard deviations from the day/night mean appear as spikes/discontinuities and are flagged bad | Outlier check using standard deviation removes these points | (hb p. 7) |
| Short-timescale anomalies / spurious spikes | Data point causing a change in local (±3 hr window) temporal variability exceeding 25 W/m2 (SH/LH) or 1.0 µmol/m2/s (CO2) appear as isolated spikes in time series, flagged bad | Temporal variability moving-window check flags and removes such points | (hb p. 7) |
| Disagreement between ECOR/QCECOR and BAEBBR (EBBR) fluxes | At SGP Central Facility, BAEBBR shows similar LH but larger SH than QCECOR in spring, and much larger LH but smaller SH in summer; seasonal divergence visible in Figure 2 | Attributed in part to differing upwind vegetation/fetch footprints between collocated ECOR and EBBR instruments; users should be aware of surface... | (hb p. 8) |
| Footprint/vegetation heterogeneity between collocated ECOR and EBBR | Flux comparisons vary with wind direction since ECOR and EBBR sample different upwind vegetation (cropland/grassland vs. grassland) | Consult site-specific vegetation documentation (Cook and Sullivan 2019, 2020) and Tang et al. 2019 comparison | (hb p. 8) |
| Precipitation/dew/frost contamination of ECOR sensors | SEBS wetness sensor analog voltage drops from 3 V (dry) toward 1 V (wet), indicating periods of potential sensor contamination | Wetness measurement included for user reference only; not applied in any QC procedure | (hb p. 6) |
| No quick plots currently available for this VAP | Users cannot rely on standard ARM quicklook plots to visually QC QCECOR output | None stated | (hb p. 9) |
| Missing/bad data set to fill value | corrected_* variables show -9999 where qc_flag = 1 (bad) | Check qc_flag / qc_corrected_* variables before using data | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `ecor`: load `arm-instrument-ecor` for its handbook facts and artifacts

### References the report cites

- Cook, DR, and RC Sullivan. 2019. Energy Balance Bowen Ratio (EBBR) Instrument Handbook. DOE/SC-ARM-TR-037.
- Cook, DR, and RC Sullivan. 2020. Eddy Correlation Flux Measurement System (ECOR) Instrument Handbook. DOE/SC-ARM-TR-052.
- Cook, DR, and RC Sullivan. 2024. Surface Energy Balance System (SEBS) Instrument Handbook. DOE/SC-ARM-TR-092.
- Burba, G. and Anderson, D. 2010. A Brief Practical Guide to Eddy Covariance Flux Measurements.
- Cook, DR, M Franklin, and DJ Holdridge. 2008. ECOR VAP Flux Corrections, Gap-Filling, and Results.
- Fuehrer, PL, and CA Friehe. 2002. Flux corrections revisited. Boundary-Layer Meteorology 102(3): 415-458.
- Massman, WJ. 2000. A simple method for estimating frequency response corrections for eddy covariance systems. Agricultural and Forest Meteorology 104(3): 185-198.
- Tang, S, et al. 2019. Differences in eddy-correlation and energy-balance surface turbulent heat flux measurements... JGR-Atmospheres 124(6): 3301-3318.
- Webb EK, GI Pearman, and R Leuning. 1980. Correction of flux measurements for density effects due to heat and water vapour transfer. QJRMS 106(447): 85-100.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-223.pdf (19 pages, DOE/SC-ARM-TR-223, by C Tao, S Xie, RC Sullivan, S Tang, Y Zhang, DR Cook, KL Gaustad)
- Catalog record: ARM data-source index, `instrument_class_code=qcecor`, read 2026-09-24
- Example file: `ena30qcecorC1.c1.20240907.000000.nc` from `ena30qcecorC1.c1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
