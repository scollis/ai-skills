---
name: arm-vap-kazrcor
description: ARM KAZR Corrected Data (kazrcor) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (reflectivity, mean Doppler velocity, signal_to_noise_ratio, significant_detection_mask, gaseous_attenuation_correction, temp, rh, bar_pres), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with kazrcor data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - kazrcor, KAZR Corrected Data, sgpkazrcormdC1.c1, reflectivity, mean Doppler velocity, signal_to_noise_ratio, significant_detection_mask, gaseous_attenuation_correction, Cloud Properties.
---

# KAZRCOR - KAZR Corrected Data

KAZRCOR/KAZRCFRCOR is a value-added product that applies gaseous attenuation correction, velocity dealiasing, minimum-usable-range masking, and significant-detection masking to Ka-Band ARM Zenith Radar (KAZR) moment data (reflectivity, mean Doppler velocity, SNR) on a mode-by-mode, day-by-day basis at ARM fixed and mobile sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 18 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `kazrcor` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-203 / K Johnson, T Fairless, S Giangrande / August 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-203.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-01-18 to 2019-12-20 (retired) |
| Datastreams with data | 31 across 9 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/kazrcor |


## Credit

Everything this skill knows about the retrieval is the work of **K Johnson, T Fairless, S Giangrande** -
the ARM developers and mentors who wrote the technical report it derives from:

> K Johnson, T Fairless, S Giangrande. *Ka-Band ARM Zenith Radar Corrections (KAZRCOR, KAZRCFRCOR) Value-Added Products*, DOE/SC-ARM-TR-203, August 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-203.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP differentiates significant radar returns from background noise by applying the Hildebrand and Sekhon (1974) technique to the KAZR signal-to-noise-ratio field profile by profile, taking the noise value plus 1.5 standard deviations as the minimum SNR for a significant detection, then applying a 5x5 point majority filter. Atmospheric gaseous attenuation due to water vapor and oxygen is computed for each time profile following Ulaby et al. 1981, using temperature, pressure, and relative humidity from the INTERPOLATEDSONDE product, and this attenuation is added back to measured reflectivity to produce corrected reflectivity. Mean Doppler velocity is dealiased in a two-step process: first profile-by-profile using gate-to-gate velocity differences (for SNR greater than  -5 dB) from cloud top downward, identifying folds when the absolute gate-to-gate difference exceeds 1.5 times the Nyquist velocity and correcting by adding/subtracting twice the Nyquist velocity; second, dealiasing in time for ranges up to 6 km using 2-, 4-, and 10-minute moving velocity averages. Data below the minimum valid usable range (where the radar is still transmitting and lacks full power) are marked MISSING.

**Cadence.** averaging KAZRCOR VAP processes one day of data at a time, producing daily output files, on the original KAZR time and range grids (hb p. 6).

## Inputs

The report names these instruments and sibling products: KAZR, KAZR2, KAZR-ARSCL, INTERPOLATEDSONDE.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| reflectivity (corrected for gaseous attenuation) | - | - | - | (hb p. 10) |
| mean Doppler velocity (dealiased) | m s-1 | - | - | (hb p. 10) |
| signal_to_noise_ratio (copol/xpol) | dB | - | - | (hb p. 2) |
| significant_detection_mask | - | - | - | (hb p. 8) |
| gaseous_attenuation_correction | - | - | - | (hb p. 8) |
| temp, rh, bar_pres (passed from INTERPOLATEDSONDE) | - | - | - | (hb p. 8) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| KAZR Nyquist velocity (example, SGP-C1) | 5.96 m s-1 | (hb p. 15) |
| High-SNR threshold for profile-by-profile dealiasing | greater than -5 dB | (hb p. 11) |
| Velocity fold detection threshold | gate-to-gate velocity difference exceeds 1.5 times the Nyquist velocity | (hb p. 11) |
| Significant detection SNR threshold | noise value plus 1.5 standard deviations of the noise values | (hb p. 9) |
| Majority filter for significant detection mask | 5x5 point majority filter | (hb p. 9) |
| Time dealiasing moving-average windows | 2-minute, 4-minute, and 10-minute moving velocity averages, for radar ranges up to 6 km | (hb p. 11) |


## The data

**No example file was verified for this instrument.** every datastream serves files of 800 MB or more, past the download cap used for these examples.

ARM's catalog lists 31 datastreams with data across 9 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "sgpkazrcormdC1.c1", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
                     params={"user": f"{user}:{token}", "ds": "sgpkazrcormdC1.c1",
                             "start": "2019-12-20", "end": "2019-12-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpkazrcormdC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpkazrcormdC1.c1", "2019-12-20", "2019-12-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpkazrcormdC1.c1", "2019-12-20", "2019-12-20"))   # cite what you pulled
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you have a
file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpkazrcormdC1.c1", "20110118", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Output datastreams include multiple quality control fields alongside corrected moments: qc_reflectivity_copol/xpol, qc_mean_doppler_velocity_copol/xpol, qc_spectral_width_copol/xpol (KAZRCOR), and qc_reflectivity, qc_mean_doppler_velocity, qc_mean_doppler_velocity_crosspolar_v, qc_spectral_width, qc_spectral_width_crosspolar_v, qc_gaseous_attenuation_correction, qc_temp, qc_rh, qc_bar_pres (KAZRCFRCOR). A mean_doppler_velocity_dealias_flag (and copol/xpol/crosspolar_v variants) indicates time-height points where dealiasing was performed. A significant_detection_mask flags significant radar...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Velocity aliasing/folding | Red and magenta-colored areas in the Mean Doppler Velocity image (e.g., below 4 km from approximately 0130-0830Z in example) where absolute value of actual hydrometeor velocities exceed the... | Two-step dealiasing algorithm: profile-by-profile correction using gate-to-gate velocity differences (SNR greater than  -5 dB) from cloud top... | (hb p. 11) |
| Gaseous (water vapor and oxygen) attenuation of reflectivity | Reduced measured reflectivity values relative to true reflectivity, though correction magnitude can be very small and difficult to detect visually for some dates/times. | Attenuation computed per time profile from INTERPOLATEDSONDE temperature, pressure, and relative humidity following Ulaby et al. 1981, and added back... | (hb p. 5) |
| Minimum usable range / near-radar blind zone | Data at ranges below the minimum valid range appear as MISSING, since the radar is still transmitting and does not have full power at these close ranges. | KAZRCOR VAP marks all data below this minimum radar range as MISSING. | (hb p. 7) |
| Background noise contaminating significant detections | Isolated, scattered spurious 'detections' surrounded by non-detections in the time-height field. | Apply Hildebrand and Sekhon (1974) noise-floor technique per profile plus 1.5 standard deviations threshold, followed by a 5x5 point majority filter... | (hb p. 9) |
| Missing INTERPOLATEDSONDE input | Gaseous attenuation correction not applied to reflectivity for periods when INTERPOLATEDSONDE data unavailable. | Correction is only applied when INTERPOLATEDSONDE is available. | (hb p. 2) |
| Uncalibrated vs calibrated reflectivity inputs | kazrcor*.c0 (or kazrcfrcor*.c0) products derived from uncalibrated a1-level KAZR data will have reflectivity values not on the calibrated scale, unlike kazrcor*.c1 products from b1-level... | Use c0 products only as interim input for KAZR-ARSCL VAP processing prior to KAZR calibration; use c1 (calibrated) products as archived standard. | (hb p. 9) |
| Not all KAZR modes always present | Number and type of output datastreams (kazrcorge, kazrcormd, kazrcorhi, kazrcorpr) varies by day depending on which input KAZR mode datastreams exist; generally not all modes exist. | VAP can run without all KAZR modes existing; output datastream created only for each input mode present. | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Hildebrand, PH, and RS Sekhon. 1974. "Objective determination of the noise level in Doppler spectra." Journal of Applied Meteorology 13(7): 808-811, http://doi.org/10.1175/1520-0450(1974)013less than 0808:ODOTNLgreater...
- Ulaby, FT, RK Moore, and AK Fung. 1981. Microwave Remote Sensing: Active and Passive, Vol. I -- Microwave Remote Sensing Fundamentals and Radiometry. Addison-Wesley, Advanced Book Program, Reading, Massachusetts.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-203.pdf (18 pages, DOE/SC-ARM-TR-203, by K Johnson, T Fairless, S Giangrande)
- Catalog record: ARM data-source index, `instrument_class_code=kazrcor`, read 2026-09-24
- Example file: none - every datastream serves files of 800 MB or more, past the download cap used for these examples
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
