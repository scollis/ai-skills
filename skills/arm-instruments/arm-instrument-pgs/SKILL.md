---
name: arm-instrument-pgs
description: ARM Precision Carbon Dioxide Mixing Ratio System (pgs) - handbook-derived instrument reference. Measurement principle, reported quantities (CO2 mixing ratio, CH4 mixing ratio), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgppgscoeffC1.b1) and the variable inventory of a real file. Use when working with pgs data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Carbon. Triggers - pgs, Precision Carbon Dioxide Mixing Ratio System, sgppgscoeffC1.b1, CO2 mixing ratio, CH4 mixing ratio, Atmospheric Carbon, Licor LI-6252 CO2 Analyzer (2001-2011), Picarro G1301 CO2 and CH4 Analyzer (2010-2014), CRDS, IRGA, NDIR, NOAA.
---

# PGS - Precision Carbon Dioxide Mixing Ratio System

The PGS makes long-term, continuous, high-accuracy observations of CO2 and CH4 mixing ratios in air sampled sequentially from 2 m, 4 m, 25 m, and 60 m heights on a tower at the ARM SGP Central Facility (C1), using a tower gas processing system feeding a gas analyzer housed in an instrument shelter at the tower base.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `pgs` |
| Handbook | [DOE/SC-ARM-TR-049 / S Biraud, K Reichl / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/pgs_handbook.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Licor LI-6252 CO2 Analyzer (2001-2011); Picarro G1301 CO2 and CH4 Analyzer (2010-2014); Picarro G2301 CO2 and CH4 Analyzer (2015-present) |
| Primary measurements | Carbon dioxide (CO2) concentration; Methane concentration |
| Record | 2001-04-11 to 2025-09-23 (retired) |
| Datastreams with data | 5 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pgs |


## Credit

Everything this skill knows about the instrument is the work of **S Biraud, K Reichl** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Biraud, K Reichl. *Precise Gas System (PGS) Instrument Handbook*, DOE/SC-ARM-TR-049, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/pgs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

For data collected prior to October 2010, the Licor LI-6252, a differential, non-dispersive infrared (NDIR) gas analyzer, measured CO2 by comparing IR absorption between a reference cell (known CO2 concentration, ~360 ppm) and a sample cell (unknown concentration), with lead selenide detectors producing an output proportional to the difference in absorption between the two cells. For data collected after October 2010, a Picarro cavity ring-down spectrometer (CRDS) measures CO2 and CH4 by directing laser light into a high-finesse optical resonator cavity containing the analyte gas and determining the decay time ("ring-down") of light in the cavity; when the laser wavelength is resonant with a species' absorption feature, the decay time decreases as the reciprocal of that species' concentration. Digital signal processing determines the ring-down rate (optical loss) as a function of wavelength, allowing detection of multiple spectral features and species simultaneously. Prior to analysis, the tower gas sample is dried and treated to minimize dilution by water vapor and to prevent liquid water from entering the analyzer.

**Siting.** The instrument is located at the base of the 60-m tower at the ARM SGP Central Facility (C1), inside an instrument shelter, sampling continuously from tower sample heights of 2 m, 4 m, 25 m, and 60 m above ground level.

**Sampling.** reported every One measurement of each of four tower sample heights measured in sequence for 5 minutes (10 minutes for calibration tanks) [3 minutes measurement window / 0.5 min averaging window prior to 2010-10-06]; averaging latter one minute averaged [0.5 minute prior to 2010-10-06] (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| CO2 mixing ratio | ppm (dry air) | - | MEAN -0.03, STDERR 0.00, RMSE 0.06 ppm (Target... | - | (hb p. 10) |
| CH4 mixing ratio | ppb (dry air) | - | MEAN -0.06, STDERR 0.00, RMSE 0.34 ppb (Target... | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Sample air and calibration cylinder air pressure to analyzer | (800 +/- 1) Torr | (hb p. 8) |
| Condenser temperature (TGP drying) | 5 C | (hb p. 8) |
| Buffer volume (Prototype I) | 1-liter | (hb p. 8) |
| Reference gas concentration (Licor LI-6252 period) | ~360 ppm CO2 | (hb p. 7) |
| Gain/zero drift correction interval (Licor LI-6252 period) | every 15 minutes | (hb p. 7) |


## The data

Verified example: **`sgppgscoeffC1.b1`**, file `sgppgscoeffC1.b1.20250919.204000.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1, `bound`=2 |
| Data variables | 18 |
| QC variables | 4 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2025-09-19T20:40:00 to 2025-09-19T20:40:00 |
| dod version | pgscoeff-b1-1.0 |
| process version | ingest-pgsavg-1.2-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ch4_gain` | unitless | time | yes | Methane gain coefficient |
| `ch4_offset` | ppb | time | yes | Methane offset coefficient |
| `co2_gain` | unitless | time | yes | Carbon dioxide gain coefficient |
| `co2_offset` | ppm | time | yes | Carbon dioxide offset coefficient |
| `ch4_gain_err` | unitless | time | - | Methane gain coefficient error |
| `ch4_offset_err` | ppb | time | - | Methane offset coefficient error |
| `co2_gain_err` | unitless | time | - | Carbon dioxide gain coefficient error |
| `co2_offset_err` | ppm | time | - | Carbon dioxide offset coefficient error |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgppgscoeffC1.b1",
                             "start": "2025-09-19", "end": "2025-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgppgscoeffC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgppgscoeffC1.b1", "2025-09-19", "2025-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgppgscoeffC1.b1", "2025-09-19", "2025-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("co2_gain", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
18 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_co2_gain"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("co2_gain", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["co2_gain", "co2_offset", "ch4_gain"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgppgscoeffC1.b1", "20010411", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Best data are those with *_QC values of 0 for tower sample or Target measurements. QC uses a bit-flag method (flag_method = "bit") with 9 defined bits covering missing values, valid_min/valid_max violations, slope/slope_err missing or out-of-range, slope significance relative to zero, and auxiliary variable QC failures; bits 1, 2, 3, and 9 pertain to tower sample measurements while all bits pertain to calibration tank measurements. Data Quality Reports (DQRs) document confirmed or possible periods of instrument instability; a mentor-compiled machine-readable .csv of DQRs is used as a...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Liquid water entering sample stream damaging analyzer | During first Picarro deployment in 2014, liquid water entered the sample stream and damaged the analyzer, prompting redesign; would appear as analyzer failure or anomalous readings... | TGP (2015-present) equipped with a liquid water detector that stops pressurized flow from tower sample line to Picarro analyzer if liquid water is... | (hb p. 8) |
| Dilution of sample by water vapor | Would appear as bias in CO2/CH4 dry mixing ratio if not corrected via drying | Upgraded TGP system deployed in 2015 to optimize tower gas sample handling by minimizing dilution effects of water vapor | (hb p. 7) |
| Diurnal systematic bias in calibration | Would appear as time-of-day dependent drift in calibration coefficients if calibration always occurred at same time of day | Span cylinders measured every 11 hours 35 minutes (not exactly 12 hours) to prevent diurnal systematic bias | (hb p. 9) |
| Instrument instability periods not flagged by automated QC | Target calibration residuals outside mentor-defined standards, calibration coefficient outliers, or periods of systematic deviation from expected values | Mentor-compiled machine-readable DQR .csv documentation excludes these periods from statistics and reprocessing; QC state of affected coefficients... | (hb p. 11) |
| Missing or out-of-range values flagged by QC bits | QC_CO2_DRY_AVG_CORR / QC_CH4_DRY_AVG_CORR bit flags set (e.g., value equal to missing_value -9999, less than valid_min, greater than valid_max) | Use only data with *_QC values of 0 ("best data") for tower sample or Target measurements | (hb p. 12) |
| Calibration slope (gain) anomalies | *_dry_slope missing value, below valid_min, above valid_max, or dry_slope significant with respect to zero slope (abs(ch4_dry_slope) - ch4_dry_slope_err greater than  0), flagged via QC... | Flagged via QC bit definitions; excluded from best data | (hb p. 12) |
| Auxiliary variable QC failure | QC state for at least one mentor-defined auxiliary variable not equal to 0, flagged via bit 9 (value 256) | Flagged in QC bits; contributes to exclusion from best data | (hb p. 12) |
| Instrument/measurement method changes across the data record (analyzer transitions) | Step changes in measurement window (3 min to 5 min), averaging window (0.5 min to 1 min), calibration method (polynomial to linear to linear with Target check), and number of span... | Documented in Table 1, Table 2, and Table 3 of handbook for users to account for method changes when analyzing long-term record | (hb p. 6) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Low- and high-span cylinders measured every 11 hours 35 minutes with a Target cylinder measurement in the middle; each calibration cylinder measured for 10 minutes with the latter one minute averaged; linearly interpolated gain and offset coefficients applied to b0-level tower data and Target measurements to generate... (hb p. 9) |
| Calibration interval | Span cylinders every 11.58 hours (2015-present); calibration tank values updated by mentor about once every two years when tanks are changed out (hb p. 9) |
| Traceability | Traceable to World Meteorological Organization/Global Atmosphere Watch scales; calibration tank values provided by WMO's Central Calibration Laboratory (CCL) at NOAA's Earth System Research Laboratory. CO2 scale: WMO-CO2-X2019; CH4 scale: WMO-CH4-X2004A. (hb p. 9) |
| Routine maintenance | Calibration tanks changed out by the mentor (hb p. 12) |
| Maintenance interval | about once every two years (hb p. 12) |


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
| `ARM` | Atmospheric Radiation Measurement |
| `C1` | SGP Central Facility |
| `CCL` | Central Calibration Laboratory |
| `CRDS` | cavity ring-down spectroscopy |
| `DQR` | Data Quality Report |
| `IR` | infrared |
| `IRGA` | infrared gas analyzer |
| `NDIR` | non-dispersive, infrared |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `PGS` | precise gas system |
| `QC` | quality control |
| `RMSE` | root-mean-square error |
| `SGP` | Southern Great Plains |
| `TGP` | tower gas processing system |


### References the handbook cites

- Andrews et al. 2014, Atmospheric Measurement Techniques 7(2): 647-687, https://doi.org/10.5194/amt-7-647-2014
- Bakwin et al. 1995, Tellus B 47(5): 535-549, https://doi.org/10.3402/tellusb.v47i5.16070
- Bakwin et al. 1998, Tellus B 50(5): 401-415, https://doi.org/10.3402/tellusb.v50i5.16216
- Biraud et al. 2013, Atmospheric Measurement Techniques 6(3): 751-763, http://doi.org/10.5194/amt-6-751-2013
- Crosson 2008, Applied Physics B 92: 403-408, https://doi.org/10.1007/s00340-008-3135-y
- Tans, Bakwin, and Guenther 1996, Global Change Biology 2(3): 309-318, https://doi.org/10.1111/j.1365-2486.1996.tb00082.x
- WMO 2014, GAW Report No. 213

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/pgs_handbook.pdf (14 pages, DOE/SC-ARM-TR-049, by S Biraud, K Reichl)
- Catalog record: ARM data-source index, `instrument_class_code=pgs`, read 2026-09-23
- Example file: `sgppgscoeffC1.b1.20250919.204000.nc` from `sgppgscoeffC1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
