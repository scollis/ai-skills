---
name: arm-instrument-mwrp
description: ARM Microwave Radiometer Profiler (mwrp) - handbook-derived instrument reference. Measurement principle, reported quantities (brightnessTemperature, totalPrecipitableWater, totalPrecipitableWater2, liquidWaterPath, liquidWaterPath2, Temperature, waterVaporDensity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsamwrpC1.b1) and the variable inventory of a real file. Use when working with mwrp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Profiling; Cloud Properties; Radiometric. Triggers - mwrp, Microwave Radiometer Profiler, nsamwrpC1.b1, brightnessTemperature, totalPrecipitableWater, totalPrecipitableWater2, liquidWaterPath, liquidWaterPath2, Temperature, Atmospheric Profiling, Cloud Properties, Radiometric.
---

# MWRP - Microwave Radiometer Profiler

The MWRP measures sky brightness temperatures at 12 microwave frequencies (22.235-58.80 GHz) from a fixed zenith-pointing ground-based location to retrieve vertical profiles of temperature, humidity, and cloud liquid water content along with precipitable water vapor and liquid water path at approximately 5-minute intervals.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mwrp` |
| Handbook | [DOE/SC-ARM-TR-057 / MP Cadeddu, J Liljegren / March 2018](https://www.arm.gov/publications/tech_reports/handbooks/mwrp_handbook.pdf) |
| Measurement category | Atmospheric Profiling; Cloud Properties; Radiometric |
| Manufacturer / model | Radiometrics Corporation MWRP (serial numbers MP3002, MP3015, MP3156A) |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Cloud base height; Convection; Liquid water content |
| Record | 2004-02-19 to 2025-07-12 (retired) |
| Datastreams with data | 14 across 12 sites |
| Sites | asi, cor, ena, fkb, grw, hfe, mao, nim, nsa, pgh, pvc, pye |
| ARM page | https://www.arm.gov/capabilities/instruments/mwrp |


## Credit

Everything this skill knows about the instrument is the work of **MP Cadeddu, J Liljegren** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MP Cadeddu, J Liljegren. *Microwave Radiometer Profiler (MWRP) Instrument Handbook*, DOE/SC-ARM-TR-057, March 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mwrp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Absorption and emission of microwave radiation in the range 10-80 GHz are dominated by molecular water vapor and oxygen, as well as cloud liquid water. Because the mixing ratio of oxygen is invariant with altitude, the emission at each altitude depends on the local temperature, and the variation of emission with frequency permits radiation from a range of altitudes to reach the instrument, thereby permitting the vertical temperature distribution to be retrieved. The emission due to water vapor varies in proportion to the water vapor density and also depends on altitude due to pressure broadening of the line shape, permitting the vertical distribution of water vapor density to be retrieved. The variation of liquid water absorption approximately as the square of frequency permits a coarsely resolved vertical distribution of liquid water retrieval. The MWRP measures microwave radiance, expressed as brightness temperature, at five frequencies near the water vapor resonance centered at 22.235 GHz and seven frequencies in the band of oxygen resonances between 51 and 59 GHz, with retrievals of physical variables derived using a statistical algorithm.

**Siting.** In normal operation mode the radiometers observe the sky in zenith position; zenith measurements are interrupted to collect scanning measurements used to perform the absolute calibration (tip curve). Deployed at fixed ARM sites: NSA/C1, AMF1/M1, ENA/C1.

**Sampling.** native rate Integration time greater than =1 s; reported every approximately 5-minute intervals (per ARM catalog); tipping curve calibration measurements acquired continuously at about 15-minute intervals (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| brightnessTemperature | K | - | ~1 K | - | (hb p. 8) |
| totalPrecipitableWater | cm | - | ~0.05 mm | - | (hb p. 8) |
| totalPrecipitableWater2 | cm | - | ~0.05 cm | - | (hb p. 8) |
| liquidWaterPath | mm | - | ~0.015 mm | - | (hb p. 8) |
| liquidWaterPath2 | mm | - | ~0.015 cm | - | (hb p. 8) |
| Temperature (retrieved profile) | K | - | 1-2K through the profile | - | (hb p. 8) |
| waterVaporDensity (retrieved profile) | g/m3 | - | ~20% through the profile | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Receiver noise temperature K-band | less than  500 K | (hb p. 12) |
| Receiver noise temperature V-band | less than  500 K | (hb p. 12) |
| Channel bandwidth K band | 300 MHz | (hb p. 12) |
| Channel bandwidth V band | 300 MHz | (hb p. 12) |
| Radiometric resolution | 0.1-1 K | (hb p. 12) |
| HPBW K band channels | ~4.9o-6.3o | (hb p. 12) |
| HPBW W band channel | ~2.4o-2.5o | (hb p. 12) |
| Integration time | greater than =1 s | (hb p. 12) |
| Operating temperature range | -50 to +50 C (Environmental Chamber tested) | (hb p. 12) |
| Operating altitude range | 0 to +3000 m | (hb p. 12) |


## The data

Verified example: **`nsamwrpC1.b1`**, file `nsamwrpC1.b1.20230926.000814.cdf`
(4.77 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=2639, `frequency`=12, `height`=47 |
| Data variables | 45 |
| QC variables | 15 (`qc_` companions) |
| Median time step | 25 s |
| File time span | 2023-09-26T00:08:14 to 2023-09-26T23:58:08 |
| sampling interval | varies |
| averaging interval | 500 ms |
| dod version | mwrp-b1-3.1 |
| process version | ingest-mwrp-13.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `blackbodyTemperature` | K | time | yes | Internal blackbody reference temperature |
| `brightnessTemperature` | K | time,frequency | yes | Microwave brightness temperature |
| `infraredTemperature` | K | time | yes | Zenith-pointing infrared temperature at 10um |
| `liquidWaterPath` | mm | time | yes | Retrieved liquid water path |
| `liquidWaterPath2` | mm | time | yes | Retrieved liquid water path using only 23.835 and 30.0 GHz |
| `pressure` | hPa | time,height | yes | Derived pressure |
| `relativeHumidity` | % | time,height | yes | Derived relative humidity |
| `surfacePressure` | hPa | time | yes | Surface pressure at instrument |
| `surfaceRelativeHumidity` | % | time | yes | Surface relative humidity at instrument |
| `surfaceTemperature` | K | time | yes | Surface absolute temperature at instrument |
| `surfaceWaterVaporDensity` | g/m^3 | time | yes | Surface water vapor density at instrument |
| `temperature` | K | time,height | yes | Retrieved absolute temperature |
| `totalPrecipitableWater` | cm | time | yes | Retrieved total precipitable water vapor |
| `totalPrecipitableWater2` | cm | time | yes | Retrieved total precipitable water vapor using only 23.835 and 30.0... |
| `waterVaporDensity` | g/m^3 | time,height | yes | Retrieved water vapor density |
| `azimuth` | degree | - | - | Azimuth angle |
| `dataQualityFlags` | 1 | time,height | - | Data quality flags |
| `elevation` | degree | time | - | Elevation angle |
| `frequency` | GHz | frequency | - | Frequency |
| `height` | m | height | - | Height above ground level |
| `liquidWaterPath2RmsError` | mm | - | - | Expected root-mean-square error in liquid water path retrieval using... |
| `liquidWaterPathRmsError` | mm | - | - | Expected root-mean-square error in liquid water path retrieval |
| `temperatureRmsError` | K | height | - | Expected root-mean-square error in temperature retrieval |
| `time` | - | time | - | Time offset from midnight |
| `totalPrecipitableWater2RmsError` | cm | - | - | Expected root-mean-square error in precipitable water retrieval using... |
| `totalPrecipitableWaterRmsError` | cm | - | - | Expected root-mean-square error in precipitable water retrieval |
| `waterVaporDensityRmsError` | g/m^3 | height | - | Expected root-mean-square error in water vapor density retrieval |
| `wetWindowFlag` | 1 | time | - | Flag indicating moisture sensor status |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "nsamwrpC1.b1",
                             "start": "2023-09-26", "end": "2023-09-26", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsamwrpC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsamwrpC1.b1", "2023-09-26", "2023-09-26")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsamwrpC1.b1", "2023-09-26", "2023-09-26"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("surfacePressure", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This datastream carries 45 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "nsamwrpC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["surfacePressure", "surfaceTemperature", "surfaceRelativeHumidity", "qc_surfacePressure", "qc_surfaceTemperature", "qc_surfaceRelativeHumidity"],
                                cleanup_qc=True)
```

## Quality control in this datastream

15 `qc_` companion variables cover 15 of the
45 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_surfacePressure"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("surfacePressure", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["surfacePressure", "surfaceTemperature", "surfaceRelativeHumidity"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsamwrpC1.b1.20230926.000814.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `temperature` | Value is equal to missing_value. | 25380 | 20.4623 |
| `waterVaporDensity` | Value is equal to missing_value. | 25380 | 20.4623 |
| `totalPrecipitableWater` | Value is equal to missing_value. | 540 | 20.4623 |
| `totalPrecipitableWater2` | Value is equal to missing_value. | 540 | 20.4623 |
| `liquidWaterPath` | Value is equal to missing_value. | 540 | 20.4623 |
| `liquidWaterPath2` | Value is equal to missing_value. | 540 | 20.4623 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("nsamwrpC1.b1", "20040219", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are named qc_'fieldname' (e.g., qc_temperature) with possible values: 0 (within specified range), 1 (missing value), 2 (less than specified minimum), 4 (greater than specified maximum), 8 (failed valid delta check). Table 5 provides min/max thresholds for brightnessTemperature, temperature, waterVaporDensity, surface_temperature, surface_pressure, surface_relative_humidity, surfaceWaterVaporDensity, totalPrecipitableWater, and liquidWaterPath. A daily quality check is available via the DQ Explorer system (http://dq.arm.gov/). The instrument mentor submits a monthly IMMS...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Non-linear optical thickness/absorber relationship in V-band (51-59 GHz oxygen resonances) | Tipping curve calibration method cannot be applied to V-band channels; requires separate LN2 target calibration | Use liquid-nitrogen-filled external target to provide ~77 K cold reference for V-band calibration | (hb p. 8) |
| Tipping curve screening for invalid sky conditions | Tip curve measurements with liquid water clouds or strong horizontal water vapor gradients violate the linear optical thickness/path length relationship | Screen tip curves by requiring correlation coefficient of regression exceed 0.99 | (hb p. 8) |
| LN2 target brightness temperature bias effects | Brightness temperature measured when viewing LN2 target is elevated ~2K above the boiling point of LN2 due to reflection at Styrofoam/LN2 interface (~1.7K), absorption of Styrofoam (~0.2K),... | Corrections for these effects are included in the calibration process | (hb p. 8) |
| Condensation formation on LN2 target during calibration | Calibration measurement session limited/interrupted when condensation forms on bottom of Styrofoam container | Blower activated to delay condensation formation; alternating measurements performed for up to an hour or until condensation forms | (hb p. 8) |
| Noise diode injection temperature drift | Effective noise diode injection temperature (Tnd) determined from tip curves shows drift over a period of a few months even though noise diodes are stable | Calibration algorithm accounts for this via periodic tip curve determination of Tnd | (hb p. 9) |
| Residual receiver temperature dependence | Small deviations in brightness temperature correlate with receiver physical temperature despite thermal stabilization to within 0.5 C | Residual temperature dependences are corrected in the calibration procedure with additional temperature coefficients (K1-K4, dTdG) | (hb p. 12) |
| Rain/wet radome contamination | wetWindowFlag variable indicates presence of rain (1=yes, 0=no), signaling potentially degraded brightness temperature measurements | Dewblower keeps radome free of dew and water drops in drizzle conditions; data from rain detection system routinely checked against other similar... | (hb p. 3) |
| Data quality flag thresholds exceeded | qc_ fields (e.g., qc_temperature) flagged with values 1 (missing), 2 (below minimum), 4 (above maximum), 8 (failed valid delta check) per Table 5 thresholds | Use qc_ flags to filter data; refer to Table 5 for specified min/max per field | (hb p. 4) |
| External temperature/pressure/relative humidity sensor disagreement with tower... | External temperature readings differ from tower measurements by more than +/-2K, pressure differs by more than +/-5 KPa, or relative humidity differs by more than +/-5% during mentor review | Instrument mentor routinely compares external readings to tower measurements as a quality check | (hb p. 11) |
| Brightness temperature physical bounds violation | Brightness temperatures observed below 2.75 K or above approximately 330 K | Mentor checks that brightness temperatures are greater than 2.75 K and less than approximately 330 K | (hb p. 11) |
| Noise/roughness in brightness temperature time series | Brightness temperature time series shows non-smooth, high-noise-level behavior | Mentor reviews time series for smoothness and low noise as a general check | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Tipping curve method used to provide cold reference temperatures (10-90 K range) for K-band channel calibration, exploiting the linear relationship between optical thickness and atmospheric path length when sky is free of liquid water clouds and strong horizontal water vapor gradients; screened by requiring... (hb p. 8) |
| Calibration interval | Tipping curve measurements acquired continuously at about 15-minute intervals; LN2 target calibration performed periodically (as shown, e.g., September 2000 at Barrow) (hb p. 8) |
| Traceability | Calibration algorithm assumes noise diodes are stable over time, but effective noise diode injection temperature as determined from tip curves will eventually show drift over a period of a few months; radiometer equations use factory calibrated temperature coefficients K1-K4 and hardware-specific parameter dTdG (hb p. 8) |
| Routine maintenance | Dewblower keeps radome free of dew and water drops in drizzle conditions; blower normally used to prevent dew condensation on window is activated during LN2 calibration to delay condensation on the bottom of the Styrofoam container (hb p. 12) |
| Maintenance interval | N/A (Routine and Corrective Maintenance Documentation section states N/A) (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `MWRP` | microwave radiometer profiler |
| `PWV` | precipitable water vapor |
| `LWP` | liquid water path |
| `RMSE` | root-mean-square error |
| `IMMS` | Instrument Mentor Monthly Summary |
| `QC` | quality control |
| `AMF` | ARM Mobile Facility |
| `NSA` | North Slope of Alaska |
| `SGP` | Southern Great Plains |
| `ENA` | Eastern North Atlantic |
| `Uncertainty` | the range of probable maximum deviation of a measured value from the true value within a... |


### References the handbook cites

- Cadeddu, MP, JC Liljegren, and DD Turner. 2013. "The atmospheric radiation measurement (ARM) program network of microwave radiometers: Instrumentation, data, and retrievals," Atmospheric Measurement Techniques 6(9):...
- Radiometrics Corporation, "Profiler operator's manual," available upon request.
- Liljegren, JC. 2002, "Evaluation of a New Multi-Frequency Microwave Radiometer for Measuring the Vertical Distribution of Temperature, Water Vapor, and Cloud Liquid Water," U.S. Department of Energy, technical report...
- Solheim, FS, JR Godwin, ER Westwater, Y Han, SJ Keihm, K March, and R Ware. 1998. "Radiometric profiling of temperature, water vapor, and cloud liquid water using various inversion methods." Radio Science 33: 393-404,...
- Solheim, FS. 1993. Use of pointed water vapor radiometer observations to improve vertical GPS surveying accuracy. Ph.D. Thesis, University of Colorado, 128 pp.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mwrp_handbook.pdf (18 pages, DOE/SC-ARM-TR-057, by MP Cadeddu, J Liljegren)
- Catalog record: ARM data-source index, `instrument_class_code=mwrp`, read 2026-09-23
- Example file: `nsamwrpC1.b1.20230926.000814.cdf` from `nsamwrpC1.b1`, 4.77 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
