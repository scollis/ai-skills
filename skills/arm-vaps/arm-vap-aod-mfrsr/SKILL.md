---
name: arm-vap-aod-mfrsr
description: ARM Aerosol Optical Depth (AOD) derived from MFRSR measurements (aod-mfrsr) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Aerosol optical depth, Total optical depth, Angstrom exponent, Vo, Rayleigh optical depth, Ozone optical depth), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmfrsr7nchcalC1.c1) and the variable inventory of a real file. Use when working with aod-mfrsr data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Radiometric. Triggers - aod-mfrsr, Aerosol Optical Depth (AOD) derived from MFRSR measurements, sgpmfrsr7nchcalC1.c1, Aerosol optical depth, Total optical depth, Angstrom exponent, Vo, Rayleigh optical depth, Aerosols, Radiometric.
---

# AOD-MFRSR - Aerosol Optical Depth (AOD) derived from MFRSR measurements

This VAP retrieves aerosol optical depth (AOD) at several wavelengths from ground-based multifilter rotating shadowband radiometers (MFRSR/MFRSR7nch) and normal incidence multifilter radiometers (NIMFR/NIMFR7nch) operated at ARM's fixed and mobile observatories.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 32 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aod-mfrsr` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-129 / A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov / December 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf) |
| Category | Aerosols; Radiometric |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1997-01-09 to 2026-09-24 (active) |
| Datastreams with data | 169 across 24 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aod-mfrsr |


## Credit

Everything this skill knows about the retrieval is the work of **A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov** -
the ARM developers and mentors who wrote the technical report it derives from:

> A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov. *Aerosol Optical Depth Value-Added Product Report*, DOE/SC-ARM-TR-129, December 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-129 documents the same AOD algorithm applied to both MFRSR and NIMFR inputs, so it is shared with `aod-nimfr` and is not specific to the MFRSR class.

## How it is produced

The uncalibrated direct normal irradiance V(lambda) measured by the MFRSR/NIMFR is related to the top-of-atmosphere irradiance Vo(lambda) via Beer's law, V(lambda)=Vo(lambda)exp[-(tauRayleigh+tauaerosol-tau(gas))am], where am is airmass computed from solar zenith angle. Taking the log of this equation gives a linear Langley regression of log[V(lambda)] versus airmass, whose slope is the total optical depth (TOD=tauRayleigh+tauaerosol+taugas) and whose intercept is log[Vo(lambda)]. Daily 'good' Langley Vo values (computed separately for morning airmass 6-2 and afternoon airmass 2-6) are filtered using a Forgan (1988,1994) three-step ratio/boxcar/Gaussian-smoothing technique to yield robust daily calibration values Vo,f. Applying Vo,f to the measured irradiance at any time of day yields TOD, from which AOD is obtained as the residual after subtracting the pressure-corrected Rayleigh optical depth and a satellite-derived (TOMS/OMI) ozone optical depth. An autonomous cloud-screening algorithm (Alexandrov et al. 2004) based on AOD time-series variability is then applied to flag/remove cloud-contaminated AOD retrievals.

**Cadence.** averaging Langley regressions computed twice-daily (morning and afternoon); daily Vo,f from two-month sliding window with 25% quartile trimming and 30-day Gaussian smoothing (hb p. 3).

## Inputs

The report names these instruments and sibling products: MFRSR, MFRSR7nch, NIMFR, NIMFR7nch, AERONET Cimel sunphotometer (CSPHOT), Langley VAP, TOMS, OMI.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Aerosol optical depth (AOD) | unitless | - | +/- 0.01 | (hb p. 12) |
| Total optical depth (TOD) | unitless | - | - | (hb p. 5) |
| Angstrom exponent | unitless | - | - | (hb p. 6) |
| Vo (top-of-atmosphere calibration irradiance) | counts | - | noise of about +/-10% | (hb p. 4) |
| Rayleigh optical depth | unitless | - | - | (hb p. 6) |
| Ozone optical depth | unitless | - | - | (hb p. 5) |
| Columnar ozone amount | atm-cm (Dobson Unit/1000) | - | - | (hb p. 6) |
| CO2/CH4/H2O average gas absorption (1625 nm channel) | unitless (optical depth) | airmass 1 to 6; precipitable... | - | (hb p. 19) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| MFRSR/NIMFR AOD wavelengths | 415, 500, 615, 673, and 870 nm | (hb p. 1) |
| Seventh channel (MFRSR7nch/NIMFR7nch) nominal wavelength | 1625 nm, passband about 20 nm (measures ~1605-1645 nm) | (hb p. 12) |
| 500 nm passband | about 10 nm (measures ~495-505 nm) | (hb p. 8) |
| 500 nm TOA irradiance | 1.963 W/m2/nm | (hb p. 8) |
| Estimated AOD error | +/- 0.01 | (hb p. 12) |
| Processing window required for stable calibration | two-month processing window at most ARM sites | (hb p. 2) |
| Daily calibration statistical variability target | below 1% per day | (hb p. 2) |
| Forgan ratio wavelengths | 415 and 870 nm | (hb p. 4) |
| Sliding window (boxcar) length | two-month length | (hb p. 4) |
| Gaussian smoothing filter width | 30-day width | (hb p. 4) |
| Hardware-change sliding window width | approximately 60-day width | (hb p. 10) |
| Earth orbit eccentricity irradiance variation | about +/- 3% | (hb p. 4) |
| Vo noise (good Langley events) | considerable noise of about +/-10% | (hb p. 4) |
| 2010 good Langley events (SGP E13) | 293 Langley events | (hb p. 4) |
| Airmass range for morning Vo | airmass values between 6 and 2 | (hb p. 3) |
| Airmass range for afternoon Vo | airmass values between 2 and 6 | (hb p. 3) |
| Ozone data record | stored in ARM Data Center from July 25, 1996 to present (datastream gecomiX1.a1) | (hb p. 6) |
| Example AOD at 500 nm (SGP E13, Oct 2, 2010) | average AOD about 0.04 | (hb p. 12) |


## The data

Verified example: **`sgpmfrsr7nchcalC1.c1`**, file `sgpmfrsr7nchcalC1.c1.20260920.000000.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1, `Io_interquartile_time`=62, `Io_wavelength`=6, `Io_gauss_time`=61 |
| Data variables | 35 |
| QC variables | 7 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2026-09-20T00:00:00 to 2026-09-20T00:00:00 |
| dod version | mfrsr7nchcal-c1-1.3 |
| process version | vap-mfraod-2.17-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Io_filter1` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter2` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter3` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter4` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter5` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter7` | count | time | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Ozone_column_amount` | DU | time | yes | Ozone column amount from satellite |
| `Io_gauss_time` | - | Io_gauss_time | - | Time for Ios after gaussian filter |
| `Io_gauss_values` | count | Io_gauss_time,Io_wavelength | - | Io values after gaussian filter |
| `Io_interquartile_time` | - | Io_interquartile_time | - | Time for interquartile Io sample times |
| `Io_interquartile_values` | count | Io_interquartile_time,Io_wavelength | - | Interquartile Io values |
| `Ozone_optical_depth_filter1` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Ozone_optical_depth_filter2` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Ozone_optical_depth_filter3` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Ozone_optical_depth_filter4` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Ozone_optical_depth_filter5` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Ozone_optical_depth_filter7` | 1 | time | - | Ozone optical depth, computed from ozone_absorption coefficient,... |
| `Rayleigh_optical_depth_filter1` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 1 |
| `Rayleigh_optical_depth_filter2` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 2 |
| `Rayleigh_optical_depth_filter3` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 3 |
| `Rayleigh_optical_depth_filter4` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 4 |
| `Rayleigh_optical_depth_filter5` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 5 |
| `Rayleigh_optical_depth_filter7` | 1 | time | - | Rayleigh optical depth adjusted for surface pressure for filter 7 |
| `sun_to_earth_distance` | astronomical_unit | time | - | Sun to earth distance |
| `surface_pressure` | kPa | time | - | Surface pressure |
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
                     params={"user": f"{user}:{token}", "ds": "sgpmfrsr7nchcalC1.c1",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmfrsr7nchcalC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmfrsr7nchcalC1.c1", "2026-09-20", "2026-09-20")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmfrsr7nchcalC1.c1", "2026-09-20", "2026-09-20"))   # cite what you pulled
```

## Quality control in this product

7 `qc_` companion variables cover 7 of the
35 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_Io_filter1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("Io_filter1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["Io_filter1", "Io_filter2", "Io_filter3"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpmfrsr7nchcalC1.c1.20260920.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ozone_column_amount` | Value unavailable from input, default_value used | 1 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmfrsr7nchcalC1.c1", "19970109", "20260924")
```

The report's own note on quality: A 'variability_flag' field is near zero during times of relatively stable optical depth (sliding-window algorithm checked temporal stability); it is set to one (1) when optical depths vary widely from one sample to the next, which may indicate cloud presence. Most measured variables are accompanied by QC flags/bits based on criteria such as being far outside physically plausible limits; a non-zero QC bit indicates a possible data problem, and users are advised to carefully examine QC values and underlying causes.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Cloud contamination of Langley regressions | Poor/noisy linear fit in log(V) vs airmass Langley plot; regression deemed 'bad' and discarded; on completely overcast days no Langley regression is possible | Algorithm attempts to remove cloud contamination; if uncertainty of fit too large the Langley event is discarded as 'bad' | (hb p. 3) |
| Random noise in daily Vo from AOD variation during Langley regression period | Vo time series (Figure 2) shows about +/-10% scatter even among 'good' Langley events; a Langley plot can look linear/'good' even with significant aerosol variation | Obtain many Langley Vo values before/after date of interest and filter with Forgan technique (ratio + boxcar quartile trimming + Gaussian smoothing)... | (hb p. 3) |
| Earth orbit eccentricity effect on irradiance | Sine-wave pattern in Vo time series with one-year period, peaking in winter and troughing in summer, about +/-3% amplitude | Vo values are corrected for Earth-sun distance eccentricity before further processing | (hb p. 4) |
| Hardware change discontinuity | Abrupt step up or step down in Vo time series precisely at the time of instrument/sensor change | Sliding window is not applied across the boundary; one edge of the ~60-day window is butted against the step change and the smoothed value at window... | (hb p. 10) |
| 940-nm channel unusable for Langley/AOD retrieval | No AOD values reported at 940 nm; channel data instead used for water vapor retrieval | 940-nm channel calibrated only via standard lamp, not TOA/Langley method; used for columnar water vapor instead of AOD | (hb p. 12) |
| Ozone absorption contaminating certain AOD channels | 500-, 615-, and 673-nm channels show wavelength-dependent bias if ozone not subtracted, especially strong at 615 nm (Chappuis band) | Subtract satellite-derived (TOMS/OMI) ozone optical depth using columnar ozone amount and wavelength-specific absorption coefficients (Appendix A) | (hb p. 5) |
| Missing satellite ozone data for a given day | Gaps in the ozone column dataset (gecomiX1.a1) for certain days | A site-specific default ozone value is used when no ozone data are available | (hb p. 6) |
| Residual cloud contamination in AOD time series | Sharp upward spikes/turns in AOD time series (e.g., Figure 3 around 1400 LST) inconsistent with smooth aerosol variation | Autonomous cloud screen (Alexandrov et al. 2004) examines AOD variability over a time interval and flags/removes AODs exceeding a conservative... | (hb p. 7) |
| Cloud screen threshold conservatism / false positives | Some good (non-cloud) AODs are flagged/removed along with contaminated ones | Threshold intentionally set conservative, erring toward removing some good data rather than allowing cloud-contaminated data through | (hb p. 7) |
| AMF (ARM Mobile Facility) short-deployment Vo determination difficulty | Insufficient Langley events accumulate during short mobile deployments to run the standard Forgan/sliding-window calibration | Vo values manually determined per day and supplied via site-specific text file using the -Z command line option instead of the standard Forgan... | (hb p. 11) |
| 1625-nm (7th channel) gas absorption from CO2, CH4, H2O | Non-uniform filter envelope and strong wavelength-dependent gas absorption spectra within 1605-1645 nm passband bias raw optical depth if uncorrected | Average gas transmittances (CO2, CH4 via airmass-based LUT; H2O via precipitable-water-based LUT) computed with LBLRTM, convolved with filter... | (hb p. 12) |
| QC flags indicating physically implausible or problematic values | Non-zero qc_* bits accompanying most measured variables | User advised to carefully examine QC values and underlying reasons for a non-zero QC bit before use | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Alexandrov, M, A Marshak, B Cairns, A Lacis, and B Carlson. 2004. Automated cloud screening algorithm for MFRSR data. Geophysical Research Letters 31(4): L04118
- Clough, SA, MW Shephard, EJ Mlawer, JS Delamere, MJ Iacono, K Cady-Pereira, S Boukabara, and PD Brown. 2005. Atmospheric radiative transfer modeling: A summary of the AER codes. JQSRT 91(2): 233-244
- Forgan, BW. 1986. Sun photometer calibration by the ratio-Langley method.
- Forgan, BW. 1994. General method for calibrating Sun photometers. Applied Optics 33(21): 4841-4850
- Giles, DM, et al. 2019. Advancements in the Aerosol Robotic Network (AERONET) Version 3 database. Atmospheric Measurement Techniques 12(1): 169-209
- Goody, RM and YL Yung. 1989. Atmospheric Radiation: Theoretical Basis.
- Gueymard, C. 2004. The Sun's total and spectral irradiance for solar energy applications and solar radiation models. Solar Energy 76(4): 423-453
- Hansen, J, and L Travis. 1974. Light scattering in planetary atmospheres. Space Science Reviews 16: 527-610
- Harrison, L, and J Michalsky. 1994. Objective algorithms for the retrieval of optical depths from ground-based measurements. Applied Optics 33(22): 5126-5132
- Kasten, F, and A Young. 1989. Revised optical air mass tables and approximation formula. Applied Optics 28(22): 4735-4738

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf (32 pages, DOE/SC-ARM-TR-129, by A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov)
- Catalog record: ARM data-source index, `instrument_class_code=aod-mfrsr`, read 2026-09-24
- Example file: `sgpmfrsr7nchcalC1.c1.20260920.000000.nc` from `sgpmfrsr7nchcalC1.c1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
