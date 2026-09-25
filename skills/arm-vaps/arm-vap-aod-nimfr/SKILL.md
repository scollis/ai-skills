---
name: arm-vap-aod-nimfr
description: ARM Aerosol Optical Depth (AOD) derived from NIMFR measurements (aod-nimfr) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Total optical depth, Aerosol optical depth, Ångström exponent, Vo, Rayleigh optical depth, Ozone optical depth), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpnimfr7nchaod1michC1.c1) and the variable inventory of a real file. Use when working with aod-nimfr data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Derived Quantities and Models; Radiometric. Triggers - aod-nimfr, sgpnimfr7nchaod1michC1.c1, Total optical depth, Aerosol optical depth, Ångström exponent, Vo, Rayleigh optical depth, Aerosols, Derived Quantities and Models.
---

# AOD-NIMFR - Aerosol Optical Depth (AOD) derived from NIMFR measurements 

This value-added product retrieves aerosol optical depth (AOD) at several wavelengths from ground-based multifilter rotating shadowband radiometer (MFRSR/MFRSR7nch) and normal incidence multifilter radiometer (NIMFR/NIMFR7nch) direct-normal irradiance measurements at ARM ground-based observatories.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 32 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aod-nimfr` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-129 / A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov / December 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf) |
| Category | Aerosols; Derived Quantities and Models; Radiometric |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-04-28 to 2026-09-23 (active) |
| Datastreams with data | 8 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aod-nimfr |


## Credit

Everything this skill knows about the retrieval is the work of **A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov** -
the ARM developers and mentors who wrote the technical report it derives from:

> A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov. *Aerosol Optical Depth Value-Added Product Report*, DOE/SC-ARM-TR-129, December 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-129 documents the same AOD algorithm applied to both MFRSR and NIMFR inputs, so it is shared with `aod-mfrsr` and is not specific to the NIMFR class.

## How it is produced

The algorithm computes Langley regressions (linear regression of log measured direct-normal irradiance versus airmass) twice daily to derive first-order top-of-atmosphere calibration values (Vo) at each wavelength channel. A robust daily calibration time series (Vo,f) is produced by ratioing Vo at 415 and 870 nm, applying a two-month sliding-window quartile pruning filter to remove outliers, then smoothing with a 30-day Gaussian filter (the Forgan technique), except at AMF sites where manually-derived Vo values from a text file may be substituted. Using the daily Vo,f, total optical depth (TOD) is computed from the ratio of measured irradiance to Vo,f and airmass; aerosol optical depth (AOD) is then obtained as the residual of TOD minus the pressure-corrected Rayleigh optical depth and a satellite-derived (TOMS or OMI) ozone optical depth. An autonomous cloud-screening algorithm (Alexandrov et al. 2004), based on the temporal variability of the AOD time series, flags/removes cloud-contaminated retrievals. For the MFRSR7nch/NIMFR7nch 1625-nm channel, additional filter-envelope-averaged gas absorption corrections for CO2, CH4, and H2O (via LBLRTM-derived look-up tables parameterized as second-order polynomials in airmass or precipitable water) are applied to both the Langley calibration and the AOD retrieval.

**Cadence.** averaging Langley regressions computed twice daily (morning and afternoon); daily Vo,f derived via 2-month sliding window + 30-day Gaussian smoothing (hb p. 9).

## Inputs

The report names these instruments and sibling products: MFRSR (multifilter rotating shadowband radiometer), MFRSR7nch, NIMFR7nch, Langley VAP, AERONET Cimel sunphotometer (CSPHOT).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Total optical depth (TOD) | unitless | - | - | (hb p. 2) |
| Aerosol optical depth (AOD) | unitless | - | +/- 0.01 (estimated error) | (hb p. 11) |
| Ångström exponent | unitless | - | - | (hb p. 11) |
| Vo (top-of-atmosphere calibration irradiance, 'V-naught') | counts | - | noise ~ +/-10% for good Langley events | (hb p. 2) |
| Rayleigh optical depth | unitless | - | - | (hb p. 5) |
| Ozone optical depth (τozone) | unitless | - | - | (hb p. 5) |
| Columnar ozone amount | atm-cm (Dobson Unit/1000) | - | - | (hb p. 5) |
| Direct normal irradiance | W/m^2 (broadband);... | - | - | (hb p. 26) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| AOD retrieval wavelengths (5-channel) | 415, 500, 615, 673, 870 nm | (hb p. 8) |
| 7th channel wavelength (MFRSR7nch/NIMFR7nch) | nominal 1625 nm, passband ~20 nm (measures ~1605-1645 nm) | (hb p. 12) |
| 500 nm nominal filter passband | ~10 nm (495-505 nm) | (hb p. 8) |
| 500 nm TOA irradiance (Gueymard spectrum) | 1.963 W/m2/nm | (hb p. 8) |
| Morning Langley airmass range | airmass 6 to 2 | (hb p. 9) |
| Afternoon Langley airmass range | airmass 2 to 6 | (hb p. 9) |
| Processing window for stable calibration | two-month window required at most ARM sites | (hb p. 8) |
| Target statistical variability of stable calibration | below 1% per day | (hb p. 8) |
| Ratio-Langley wavelength pair (Forgan technique) | 415 nm / 870 nm ratio | (hb p. 10) |
| Sliding window length for Vo,f pruning | two-month length (approximately 60-day width across hardware-change boundaries) | (hb p. 10) |
| Quartile pruning | remove upper and lower 25% quartiles, retaining 50% of points | (hb p. 10) |
| Smoothing filter | Gaussian filter of 30-day width | (hb p. 10) |
| Ångström exponent wavelength pair | 415 nm and 870 nm | (hb p. 11) |
| Airmass range for gas absorption LUT (CO2, CH4) | am = 1 to 6 | (hb p. 19) |
| Precipitable water vapor range for LUT (H2O) | pw = 1 to 10 cm | (hb p. 19) |
| Gas absorption polynomial form | second-order polynomial: A + B*am + C*am^2 (CO2, CH4); exp(A + B*pw + C*pw^2) (H2O) | (hb p. 19) |
| Ozone data source period | TOMS/OMI (gecomiX1.a1 datastream) stored from July 25, 1996 to present | (hb p. 6) |
| Airmass formula | Kasten and Young (1989): am = 1.0 / [cos(Z) + 0.50572 × (96.07995 - Z)^-1.6364] | (hb p. 8) |


## The data

Verified example: **`sgpnimfr7nchaod1michC1.c1`**, file `sgpnimfr7nchaod1michC1.c1.20260919.000000.nc`
(29.91 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=86400, `wavelength`=750, `Io_interquartile_time`=62, `Io_wavelength`=6, `Io_gauss_time`=61 |
| Data variables | 160 |
| QC variables | 53 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:59 |
| dod version | nimfr7nchaod1mich-c1-1.1 |
| process version | vap-mfraod-2.17-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Io_filter1` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter2` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter3` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter4` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter5` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Io_filter7` | count | - | yes | TOA direct normal irradiance corrected for earth-sun distance from... |
| `Ozone_column_amount` | DU | - | yes | Ozone column amount from satellite |
| `aerosol_optical_depth_filter1` | 1 | time | yes | Aerosol optical depth filter 1 |
| `aerosol_optical_depth_filter2` | 1 | time | yes | Aerosol optical depth filter 2 |
| `aerosol_optical_depth_filter3` | 1 | time | yes | Aerosol optical depth filter 3 |
| `aerosol_optical_depth_filter4` | 1 | time | yes | Aerosol optical depth filter 4 |
| `aerosol_optical_depth_filter5` | 1 | time | yes | Aerosol optical depth filter 5 |
| `aerosol_optical_depth_filter7` | 1 | time | yes | Aerosol optical depth filter 7 |
| `airmass` | 1 | time | yes | Airmass |
| `angstrom_exponent` | 1 | time | yes | Angstrom exponent |
| `direct_horizontal_narrowband_filter1` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 1 |
| `direct_horizontal_narrowband_filter2` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 2 |
| `direct_horizontal_narrowband_filter3` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 3 |
| `direct_horizontal_narrowband_filter4` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 4 |
| `direct_horizontal_narrowband_filter5` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 5 |
| `direct_horizontal_narrowband_filter6` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 6 |
| `direct_horizontal_narrowband_filter7` | W/(m^2 nm) | time | yes | Narrowband direct horizontal irradiance, filter 7 |
| `direct_normal_narrowband_filter1` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 1 |
| `direct_normal_narrowband_filter2` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 2 |
| `direct_normal_narrowband_filter3` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 3 |
| `direct_normal_narrowband_filter4` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 4 |
| `direct_normal_narrowband_filter5` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 5 |
| `direct_normal_narrowband_filter6` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 6 |
| `direct_normal_narrowband_filter7` | W/(m^2 nm) | time | yes | Narrowband direct normal irradiance, filter 7 |
| `head_temp` | degC | time | yes | Detector temperature |


_76 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpnimfr7nchaod1michC1.c1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpnimfr7nchaod1michC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpnimfr7nchaod1michC1.c1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpnimfr7nchaod1michC1.c1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("direct_normal_narrowband_filter1_raw")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 160 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpnimfr7nchaod1michC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["direct_normal_narrowband_filter1", "direct_normal_narrowband_filter2", "direct_normal_narrowband_filter3", "qc_direct_normal_narrowband_filter1", "qc_direct_normal_narrowband_filter2", "qc_direct_normal_narrowband_filter3"],
                                cleanup_qc=True)
```

## Quality control in this product

53 `qc_` companion variables cover 53 of the
160 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_direct_normal_narrowband_filter1"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("direct_normal_narrowband_filter1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["direct_normal_narrowband_filter1", "direct_normal_narrowband_filter2", "direct_normal_narrowband_filter3"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpnimfr7nchaod1michC1.c1.20260919.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ozone_column_amount` | Value unavailable from input, default value used | 1 | 100.0 |
| `aerosol_optical_depth_filter7` | variability_flag greater than  1e-5 | 85911 | 99.434 |
| `angstrom_exponent` | variability_flag greater than  1e-5 | 85911 | 99.434 |
| `aerosol_optical_depth_filter1` | variability_flag greater than  1e-5 | 85911 | 99.434 |
| `aerosol_optical_depth_filter2` | variability_flag greater than  1e-5 | 85911 | 99.434 |
| `aerosol_optical_depth_filter4` | variability_flag greater than  1e-5 | 85911 | 99.434 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpnimfr7nchaod1michC1.c1", "19980428", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: A 'variability_flag' field is near zero during stable optical depth periods (checked via the sliding-window algorithm) and set to one when optical depths vary widely sample-to-sample, potentially indicating cloud presence. Most measured variables have accompanying qc_ flags based on criteria such as physically plausible limits; a non-zero QC bit indicates a possible data problem, and users are advised to carefully examine QC values and underlying reasons before use.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Daily Langley regression noise from atmospheric variability | Daily Vo values scatter by about ±10% around the smooth calibration curve even for 'good' Langley events | Use a two-month processing window and Forgan ratio/quartile-pruning/Gaussian-smoothing technique to derive a robust Vo,f time series | (hb p. 8) |
| Cloud contamination of Langley regressions | Poor linear fit / high uncertainty in the log(V) vs airmass regression; regression flagged as 'bad' and discarded; no Langley possible on fully overcast days | Bad Langley events with uncertainty too large are discarded | (hb p. 9) |
| Aerosol variability during Langley regression period masquerading as good linear fit | A Langley regression can appear linear ('good') even when significant aerosol variation occurred, introducing hidden noise in the derived Vo | Obtain Langley Vo data before and after the date of interest and filter to reduce noise (Marenco 2007 cited) | (hb p. 9) |
| Earth-sun orbital eccentricity effect on irradiance | Sine-wave variation of about ±3% in raw Vo time series with a one-year period, peaking in winter | Vo values are corrected for orbital eccentricity before further processing | (hb p. 4) |
| Hardware change discontinuity in calibration | Abrupt step up or step down in Vo values precisely at the time of an MFRSR/NIMFR hardware change; sliding window cannot span the boundary | Allow the sliding window (~60-day width) to butt against the step change and use the smoothed value at the window's middle up to the... | (hb p. 10) |
| 940-nm channel unusable for AOD/Langley | 940-nm channel is contaminated by water vapor absorption and shows no valid Langley-derived AOD; instead used to retrieve columnar water vapor and relies on standard lamp calibration rather... | Excluded from AOD retrieval; calibrated via standard lamp instead of Langley/TOA method | (hb p. 11) |
| Cloud contamination of AOD time series | AOD time series shows sharp upward spikes / high short-term variability (e.g., after 1400 LST in example) | Apply autonomous cloud screen (Alexandrov et al. 2004) based on AOD variability threshold; conservative threshold errs toward removing some good data... | (hb p. 6) |
| Ozone data gaps | Missing TOMS/OMI ozone retrieval for a given day | Use a site-specific default ozone value when no satellite ozone data is available | (hb p. 6) |
| Ångström/AOD retrieval error | Estimated AOD error of about ±0.01 evident when comparing retrieved AOD across wavelengths/time | - | (hb p. 11) |
| 1625-nm (7th) channel gas absorption interference from CO2, CH4, H2O | Non-uniform filter envelope response and strong wavelength-dependent gas absorption across the ~1605-1645 nm passband bias raw TOD/AOD if uncorrected | Apply filter-envelope-averaged gas transmittance corrections (LBLRTM-derived LUTs parameterized as polynomials in airmass/precipitable water) to both... | (hb p. 12) |
| AMF site calibration difficulty | Insufficient good Vo Langley events accumulate at short-duration ARM Mobile Facility deployments, preventing automated Forgan-technique calibration | Manually derive Vo values per day and supply via site-specific text file using the -Z command line option instead of the automated technique | (hb p. 11) |
| Non-zero QC bits indicate data outside physically plausible limits or other problems | qc_ fields associated with most variables show non-zero values | Data user advised to carefully examine QC values and underlying reasons before use | (hb p. 12) |
| variability_flag indicating unstable/cloud-affected optical depth | variability_flag set to 1 when optical depths vary widely from one sample to the next (vs near 0 for stable conditions) | Use variability_flag to identify likely cloud-affected periods | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Alexandrov, M, A Marshak, B Cairns, A Lacis, and B Carlson. 2004. Geophysical Research Letters 31(4): L04118
- Clough, SA, MW Shephard, EJ Mlawer, JS Delamere, MJ Iacono, K Cady-Pereira, S Boukabara, and PD Brown. 2005. Journal of Quantitative Spectroscopy & Radiative Transfer 91(2): 233-244
- Forgan, BW. 1986. Sun photometer calibration by the ratio-Langley method
- Forgan, BW. 1994. General method for calibrating Sun photometers. Applied Optics 33(21): 4841-4850
- Giles, DM et al. 2019. Atmospheric Measurement Techniques 12(1): 169-209
- Goody, RM and YL Yung. 1989. Atmospheric Radiation: Theoretical Basis
- Gueymard, C. 2004. Solar Energy 76(4): 423-453
- Hansen, J, and L Travis. 1974. Space Science Reviews 16: 527-610
- Harrison, L, and J Michalsky. 1994. Applied Optics 33(22): 5126-5132
- Kasten, F, and A Young. 1989. Applied Optics 28(22): 4735-4738

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-129.pdf (32 pages, DOE/SC-ARM-TR-129, by A Koontz, C Flynn, G Hodges, J Michalsky, J Barnard, E Cromwell, E Kassianov)
- Catalog record: ARM data-source index, `instrument_class_code=aod-nimfr`, read 2026-09-24
- Example file: `sgpnimfr7nchaod1michC1.c1.20260919.000000.nc` from `sgpnimfr7nchaod1michC1.c1`, 29.91 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
