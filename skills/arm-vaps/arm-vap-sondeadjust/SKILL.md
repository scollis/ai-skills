---
name: arm-vap-sondeadjust
description: ARM Sonde Adjust (sondeadjust) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Barometric pressure, Dry bulb temperature, Dewpoint temperature, Wind speed, Wind direction, Relative humidity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpsondeadjustC1.c1) and the variable inventory of a real file. Use when working with sondeadjust data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - sondeadjust, Sonde Adjust, sgpsondeadjustC1.c1, Barometric pressure, Dry bulb temperature, Dewpoint temperature, Wind speed, Wind direction, Atmospheric Profiling.
---

# SONDEADJUST - Sonde Adjust

Sonde Adjust is an ARM value-added product (software algorithm, not a physical sensor) that applies documented Vaisala RS-80/RS-90/RS-92 humidity bias, time-lag and solar-heating corrections plus an MWR-precipitable-water-vapor scaling to ARM balloon-borne radiosonde soundings launched at ARM fixed and mobile facility sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 19 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sondeadjust` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-102 / D Troyan / "December 2011"](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-102.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1997-08-28 to 2019-03-05 (retired) |
| Datastreams with data | 14 across 12 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sondeadjust |


## Credit

Everything this skill knows about the retrieval is the work of **D Troyan** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Troyan. *Sonde Adjust Value-Added Product Technical Report*, DOE/SC-ARM-TR-102, "December 2011".
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-102.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Vaisala radiosonde humidity sensors exhibit well-documented dry biases and response time-lags that prevent accurate ambient RH from being directly measured, as detailed in the cited literature (Miloshevich et al., Wang et al., Turner et al., Vomel et al., Xie et al.). Sonde Adjust corrects the raw RH profile in sequential steps: it first smooths the coarse-resolution original RH using a Derivative-Based Smoothing Algorithm to produce rh_smooth, then applies a dry-bias correction (based on Wang et al. 2002, addressing chemical contamination, temperature dependence, calibration, sensor-arm heating, and ground-check errors) to produce rh_biased, and finally corrects for sensor time-lag and solar warming (per Miloshevich et al. 2004/2009) using rh_biased as input to produce the final ambient RH field rh_adjust. A further rh_scaled field is derived by integrating rh_adjust, computing a scale factor from the microwave radiometer's retrieved precipitable water vapor (PWV), and applying that factor across the humidity profile. The algorithm also determines whether the sonde launch occurred during day or night to apply diurnal-dependent corrections.

## Inputs

The report names these instruments and sibling products: sgpsondecorr1miloC1.c1 (discontinued PI product), LSSONDE (Liebe Scaled Sonde VAP, planned to be replaced by Sonde..., MWR Retrievals VAP (mwrret1liljclouC1 datastream), ARM balloon-borne radiosonde system (sondewnpn datastreams).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Barometric pressure | hPa | 0.f to 1100.f | - | (hb p. 10) |
| Dry bulb temperature | C | -80.f to 50.f | - | (hb p. 11) |
| Dewpoint temperature | C | -110.f to 50.f | - | (hb p. 11) |
| Wind speed | m/s | 0.f to 100.f | - | (hb p. 12) |
| Wind direction | deg | 0.f to 360.f | - | (hb p. 12) |
| Relative humidity (original) | % | 0.f to 105.f | - | (hb p. 12) |
| Eastward wind component | m/s | -75.f to 75.f | - | (hb p. 13) |
| Northward wind component | m/s | -75.f to 75.f | - | (hb p. 13) |
| Ascent rate | m/s | -10.f to 20.f | - | (hb p. 13) |
| Relative humidity smoothed (rh_smooth) | % | 0.f to 100.f | - | (hb p. 10) |
| Relative humidity dry-bias corrected (rh_biased) | % | 0.f to 100.f | - | (hb p. 10) |
| Relative humidity ambient/adjusted (rh_adjust) | % | 0.f to 100.f | - | (hb p. 11) |
| Relative humidity scaled by MWR (rh_scaled) | % | 0.f to 100.f | - | (hb p. 11) |
| Latitude | degrees | -90.f to 90.f | - | (hb p. 11) |
| Longitude | degrees | -180.f to 180.f | - | (hb p. 11) |
| Altitude above mean sea level | m | - | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| pres valid_min/valid_max | 0.f to 1100.f hPa | (hb p. 10) |
| tdry valid_min/valid_max | -80.f to 50.f C | (hb p. 11) |
| dp valid_min/valid_max | -110.f to 50.f C | (hb p. 11) |
| wspd valid_min/valid_max | 0.f to 100.f m/s | (hb p. 12) |
| deg valid_min/valid_max | 0.f to 360.f deg | (hb p. 12) |
| rh valid_min/valid_max | 0.f to 105.f % | (hb p. 12) |
| u_wind valid_min/valid_max | -75.f to 75.f m/s | (hb p. 13) |
| v_wind valid_min/valid_max | -75.f to 75.f m/s | (hb p. 13) |
| asc valid_min/valid_max | -10.f to 20.f m/s | (hb p. 13) |
| rh_smooth valid_min/valid_max | 0.f to 100.f % | (hb p. 10) |
| rh_biased valid_min/valid_max | 0.f to 100.f % | (hb p. 10) |
| rh_adjust valid_min/valid_max | 0.f to 100.f % | (hb p. 11) |
| rh_scaled valid_min/valid_max | 0.f to 100.f % | (hb p. 11) |
| lat valid_min/valid_max | -90.f to 90.f degrees | (hb p. 11) |
| lon valid_min/valid_max | -180.f to 180.f degrees | (hb p. 11) |
| qc_time delta_t_lower_limit | 20. | (hb p. 10) |
| qc_time delta_t_upper_limit | 20. | (hb p. 10) |


## The data

Verified example: **`sgpsondeadjustC1.c1`**, file `sgpsondeadjustC1.c1.20120829.053200.cdf`
(0.5 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=3288 |
| Data variables | 35 |
| QC variables | 15 (`qc_` companions) |
| Median time step | 2 s |
| File time span | 2012-08-29T05:32:00 to 2012-08-29T07:21:34 |
| dod version | 5.0 |
| process version | $State: vap-sonde_adjust-7.0-0.sol5_10$ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `asc` | m/s | time | yes | Ascent rate |
| `deg` | deg | time | yes | Wind direction |
| `dp` | C | time | yes | Dewpoint temperature |
| `dp_scaled` | C | time | yes | Scaled dewpoint temperature |
| `pres` | hPa | time | yes | Barometric pressure |
| `rh` | % | time | yes | Relative humidity |
| `rh_adjust` | % | time | yes | Final corrected ambient relative humidity |
| `rh_biased` | % | time | yes | Dry bias corrected relative humidity |
| `rh_scaled` | % | time | yes | Scaled final corrected ambient relative humidity |
| `rh_smooth` | % | time | yes | Smoothed original relative humidity |
| `tdry` | C | time | yes | Dry bulb temperature |
| `time` | - | time | yes | Time offset from midnight |
| `u_wind` | m/s | time | yes | Eastward wind component |
| `v_wind` | m/s | time | yes | Northward wind component |
| `wspd` | m/s | time | yes | Wind speed |
| `wstat` | unitless | time | - | Wind status |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpsondeadjustC1.c1", "2012-08-29", "2012-08-29")
ds = armlive_open("sgpsondeadjustC1.c1", "2012-08-29", "2012-08-29", cleanup_qc=True)
```

## Quality control in this product

15 `qc_` companion variables cover 14 of the
35 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpsondeadjustC1.c1", "19970828", "20260924")
```

The report's own note on quality: Quality control flags copied from the original radiosonde datastream apply unchanged to fields such as pres, tdry, dp, wspd, deg, rh, u_wind, v_wind, and asc. The new value-added fields (rh_smooth, rh_biased, rh_adjust, rh_scaled) have newly created QC variables that are currently copied directly from the RH QC field of the original radiosonde data, per Data Quality office requirements; more detailed QC information will be assigned to these new fields as data move from the Evaluation area to the general area of the ARM Data Archive. QC variables are bit-packed: zero means good data. Bit 1 =...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Dry bias in Vaisala humidity sensors | Original relative humidity (rh) values read systematically lower than true ambient RH; corrected profiles (rh_biased, rh_adjust) shift RH upward relative to raw rh, as seen in Figure 1... | Apply dry-bias correction algorithm from Wang et al. (2002), fixing chemical contamination error, temperature dependence error, basic calibration... | (hb p. 9) |
| Sensor time-lag error | RH profile lags true atmospheric humidity changes, especially at low temperatures/high altitude, producing smeared or delayed transitions in the vertical RH profile | Apply time-lag correction algorithms from Miloshevich et al. (2004) for RS-80/RS-90 and Miloshevich et al. (2009) for RS-92 to produce rh_adjust field | (hb p. 9) |
| Solar (radiation) warming/heating of sensor | RH readings biased during daytime soundings due to solar heating of the sensor relative to nighttime; discrepancy correlates with day/night launch determination | Correct ambient RH for diurnal differences as part of producing final rh_adjust field; day/night launch is determined explicitly in algorithm step 3 | (hb p. 7) |
| Coarse instrument resolution (integer RH values) causing stairstep artifact | Raw RH profile shows a stairstep-like function due to integer-resolution reporting | Smooth original RH profile using Derivative-Based Smoothing Algorithm (Miloshevich et al. 2004, Appendix B) to produce rh_smooth field | (hb p. 10) |
| Diurnal variation dependence of RS-92 dry bias | Magnitude of dry bias varies between day and night soundings | Referenced in Xie et al. (2010); accounted for via diurnal correction step in algorithm | (hb p. 5) |
| MWR data unavailable or PWV below threshold | rh_scaled field contains only missing-data values (-9999) for the entire profile | Documented behavior: if MWR data are unavailable or PWV less than  0.8, rh_scaled is set to -9999; qc_rh_scaled bit_4 flags PWV below 0.8 threshold... | (hb p. 9) |
| rh_biased correction only applies to RS-80 sondes | For RS-90/RS-92 soundings, rh_biased field note indicates the dry-bias correction step is not the applicable correction pathway (per netCDF note1/note2 in header) | Handbook notes this restriction in the sample header file attributes for rh_biased | (hb p. 10) |
| Missing/unavailable data in input radiosonde file | Output value set to -9999 with qc bit_3 flagged as Bad for pres, tdry, dp, wspd, deg, rh, u_wind, v_wind, asc and other copied fields | QC bit_3 flag documents that data value was not available in input file and was set to -9999 in output | (hb p. 10) |
| Value outside valid_min/valid_max range | QC bit_1 (below valid_min) or bit_2 (above valid_max) set to Indeterminate for fields such as pres, tdry, dp, wspd, deg, rh, u_wind, v_wind, asc, rh_smooth, rh_biased, rh_adjust, rh_scaled | Flagged via bit-packed qc variables with Indeterminate assessment | (hb p. 11) |
| Discontinuation of predecessor PI product sgpsondecorr1miloC1.c1 | Legacy datastream no longer produced/updated; users relying on it will find no new data after Sonde Adjust VAP supersedes it | Sonde Adjust VAP improves upon and replaces sgpsondecorr1miloC1.c1 by covering all radiosonde classes (RS-80, RS-90, RS-92) | (hb p. 5) |
| QC fields for new value-added variables are placeholder/incomplete | qc_rh_smooth, qc_rh_biased, qc_rh_adjust, qc_rh_scaled are currently copied directly from the original RH QC field rather than independently derived, so QC may not fully reflect quality of... | Handbook states more detailed QC information will be assigned once data move from Evaluation area to general area of ARM Data Archive | (hb p. 9) |
| Time QC delta checks | qc_time bit_1/2/3 flag Bad when delta time between samples is zero, less than delta_t_lower_limit (20.), or greater than delta_t_upper_limit (20.) | Documented as bit-packed qc_time flags; prior_sample_flag setting affects how first sample of new raw file is checked | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Miloshevich, LM, H Vomel, A Paukkunen, AJ Heymsfield, SJ Oltmans. 2001. Journal of Atmospheric and Oceanic Technology 18: 135–156.
- Miloshevich, LM, A Paukkunen, H Vomel, SJ Oltmans. 2004. Journal of Atmospheric and Oceanic Technology 21: 1305–1327.
- Miloshevich, LM, H Vomel, DN Whiteman, BM Lesht, FJ Schmidlin, F Russo. 2006. Journal of Geophysical Research 111: D09S10, doi:10.1029/2005JD006083.
- Miloshevich, LM, H Vomel, DN Whiteman, T Leblanc. 2009. Journal of Geophysical Research 114: D11305, doi:10.1029/2008JD011565.
- Turner, DD, BM Lesht, SA Clough, JC Liljegren, HE Revecomb, DC Tobin. 2003. Journal of Atmospheric and Oceanic Technology 20: 117–132.
- Vömel, H, DE David, K Smith. 2007. Journal of Atmospheric and Oceanic Technology 24: 953–963.
- Wang, J, H Cole, DJ Carlson, ER Miller, K Beierle, A Paukkunen, TK Laine. 2002. Journal of Atmospheric and Oceanic Technology 19: 981–1002.
- Xie, S, T Hume, C Jakob, SA Klein, RB McCoy, MH Zhang. 2010. Journal of Climate 23: 57–79.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-102.pdf (19 pages, DOE/SC-ARM-TR-102, by D Troyan)
- Catalog record: ARM data-source index, `instrument_class_code=sondeadjust`, read 2026-09-24
- Example file: `sgpsondeadjustC1.c1.20120829.053200.cdf` from `sgpsondeadjustC1.c1`, 0.5 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
