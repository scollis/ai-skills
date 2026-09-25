---
name: arm-instrument-ghg
description: ARM Greenhouse Gas Monitor (ghg) - handbook-derived instrument reference. Measurement principle, reported quantities (CO2, CH4), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (oliaosghgcoeffM1.b1) and the variable inventory of a real file. Use when working with ghg data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Carbon. Triggers - ghg, Greenhouse Gas Monitor, oliaosghgcoeffM1.b1, CO2, CH4, Atmospheric Carbon, AOSGHG, CRDS, NOAA, RMSE.
---

# GHG - Greenhouse Gas Monitor

The GHG system continuously measures atmospheric CO2 and CH4 concentrations from air pulled from a 10 m sampling tower height, using a tower gas processing (TGP) rack to dry/pressurize the air followed by a Picarro G2301 series cavity ringdown spectrometer, deployed long-term at ARM's Oliktok Point (OLI) and Eastern North Atlantic (ENA) observatories.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 13 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ghg` |
| Handbook | [DOE/SC-ARM-TR-175 / S Biraud, K Reichl / October 2024](https://www.arm.gov/publications/tech_reports/handbooks/ghg_handbook.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Picarro model G2301 series cavity ringdown spectrometer (CRDS) |
| Primary measurements | Carbon dioxide (CO2) concentration; Methane concentration |
| Record | 2013-10-01 to 2021-06-15 (retired) |
| Datastreams with data | 10 across 2 sites |
| Sites | ena, oli |
| ARM page | https://www.arm.gov/capabilities/instruments/ghg |


## Credit

Everything this skill knows about the instrument is the work of **S Biraud, K Reichl** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Biraud, K Reichl. *Atmospheric Observation System for Greenhouse Gases (GHG) Instrument Handbook*, DOE/SC-ARM-TR-175, October 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ghg_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The essential CRDS measurement consists of determining the decay time of light in an optical cavity filled with the gas stream to be analyzed. Light from a semiconductor diode laser is directed into a high-finesse optical resonator cavity containing the analyte gas; when the optical frequency matches the cavity's resonance frequency, energy builds up in the cavity. When the build-up is complete, the laser is shut off and the light circulating in the cavity decays, or "rings down," with a characteristic decay time. When the injected light does not match an absorption feature of any gas in the cavity, the decay time is dominated by mirror loss; but when the wavelength is resonant with an absorption feature of a species in the cavity, the decay time decreases as the reciprocal of the species concentration. The instrument's electronics include a digital signal processing system for determination of the ring-down rate, or optical loss, as a function of wavelength, allowing rapid measurement of multiple spectral features to accurately detect multiple species.

**Siting.** The instrument is located at the base of the tower inside an instrument shelter, sampling air pulled from a single sample height of 10 m above ground level on an atmospheric sampling tower. Deployed at Oliktok Point, Alaska (OLI, as part of AMF3) and at the Eastern North Atlantic (ENA) site on Graciosa Island, Azores.

**Sampling.** native rate continuous sampling by analyzer; reported every one-minute average for tower sample measurements; averaging Tower sample: one-minute average of continuous measurements. Calibration/Target tanks: measured for 10 minutes, latter 1 minute averaged; the four minutes following calibration tank measurements are discarded before returning to tower sample measurements, to allow sufficient transition of air sample in the analyzer cavity. (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| CO2 (dry, corrected) | ppm | - | - | - | (hb p. 6) |
| CH4 (dry, corrected) | ppb | - | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Sample height above ground level | 10 m | (hb p. 6) |
| Analyzer | Picarro model G2301 series cavity ringdown spectrometer (CRDS) | (hb p. 6) |
| Condenser drying temperature | 5ºC | (hb p. 7) |
| Additional drying | Nafion and Drierite dryers | (hb p. 7) |
| Sample and calibration cylinder air pressure to analyzer | 800 ±1 Torr | (hb p. 7) |
| Datalogger | Campbell CR1000 | (hb p. 7) |
| Stream selection valve | Valco multi-port valve | (hb p. 7) |
| Calibration frequency | low- and high-span cylinders measured every 11 hours and 35 minutes, with a Target cylinder measurement in the middle | (hb p. 8) |
| Calibration/Target cylinder measurement duration | 10 minutes measured, latter 1 minute averaged | (hb p. 8) |
| CO2 calibration scale | WMO-CO2-X2019 | (hb p. 11) |
| CH4 calibration scale | WMO-CH4-X2004A | (hb p. 11) |


## The data

Verified example: **`oliaosghgcoeffM1.b1`**, file `oliaosghgcoeffM1.b1.20210612.053400.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1, `bound`=2 |
| Data variables | 18 |
| QC variables | 4 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2021-06-12T05:34:00 to 2021-06-12T05:34:00 |
| dod version | aosghgcoeff-b1-1.0 |
| process version | ingest-aosghgavg-1.2-0.el7 |


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
                     params={"user": f"{user}:{token}", "ds": "oliaosghgcoeffM1.b1",
                             "start": "2021-06-12", "end": "2021-06-12", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./oliaosghgcoeffM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "oliaosghgcoeffM1.b1", "2021-06-12", "2021-06-12")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("oliaosghgcoeffM1.b1", "2021-06-12", "2021-06-12"))   # cite what you pulled
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
print(ds["qc_co2_gain"].attrs["flag_meanings"])
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
act.qc.print_dqr("oliaosghgcoeffM1.b1", "20131001", "20260923")
```

The handbook's own note on data quality: Primary variables CO2_DRY_AVG_CORR and CH4_DRY_AVG_CORR each have associated QC variables (QC_CO2_DRY_AVG_CORR, QC_CH4_DRY_AVG_CORR) using a bit-flag method (flag_method = "bit") with 9 defined bits (see artifacts). "Best data" are those with QC_* values of 0 for tower sample or Target measurements. Tower sample data correspond to VALCOPOSITION variable equal to integer 1. Bits 1, 2, 3, and 9 pertain to tower sample measurements while all bits pertain to calibration tank measurements. Additionally, uncertainty/culling of Target tank statistics uses a mentor-compiled machine-readable .csv file...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Liquid water intrusion into sample stream | Flow from tower sample line to gas analyzer is stopped by the liquid water detector when liquid water is detected in the sample stream, resulting in data gaps | TGP is equipped with a cooler (M&C) and a liquid water detector that stops flow to prevent liquid water from entering the cell cavity of the gas... | (hb p. 7) |
| Post-calibration transition/carryover in analyzer cavity | Four minutes of data immediately following calibration tank measurements show transitional (non-representative) values | The four minutes following measurements of calibration tanks are discarded before returning to one-minute averaged continuous tower sample... | (hb p. 7) |
| Diurnal systematic bias in calibration timing | If calibration always occurred at the same time of day, residuals could show a diurnal-correlated systematic offset | Span cylinders measured every 11 hours and 35 minutes (an interval offset from 12 hours) specifically to prevent this possibility | (hb p. 8) |
| Instrument instability periods (systematic deviation) | Target calibration residuals outside mentor-defined standards for one or more gas species, or calibration coefficient outliers/periods of systematic deviation from expected values | Periods are excluded from uncertainty statistics using a mentor-compiled machine-readable .csv file of Data Quality Reports (DQRs) used as a... | (hb p. 9) |
| Calibration residual / measurement uncertainty (non-zero mean and RMSE) | Target cylinder comparisons show MEAN, STDERR, and RMSE offsets from known values (e.g., ENA CO2 MEAN 0.03 ppm RMSE 0.07 ppm; ENA CH4 MEAN -0.15 ppb RMSE 0.31 ppb; OLI CO2 MEAN 0.04 ppm... | Used by mentors as an uncertainty metric to assess instrument performance; is inherent overall instrument uncertainty encompassing systematic and/or... | (hb p. 9) |
| Missing/out-of-range values flagged by QC bit system | QC variable bits set: bit1 = value equals missing_value -9999; bit2 = value less than valid_min; bit3 = value greater than valid_max; bit4 = *_dry_slope missing; bit5 = *_dry_slope_err... | Best data are those with QC_* values of 0 for tower sample or Target measurements | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Low- and high-span calibration cylinders measured every 11 hours 35 minutes (to prevent diurnal systematic bias), with a Target cylinder measurement in between; each cylinder measured 10 minutes with latter 1-minute averaged. Linearly interpolated gain and offset coefficients from span cylinder pairs are applied to... (hb p. 8) |
| Calibration interval | Span cylinder calibration every 11 hours 35 minutes; calibration tanks physically changed out about once every two years (hb p. 8) |
| Traceability | Measurements traceable to World Meteorological Organization (WMO)/Global Atmosphere Watch scales; calibration tank values provided by the WMO's Central Calibration Laboratory (CCL) at NOAA's Earth System Research Laboratory (hb p. 8) |
| Routine maintenance | Calibration tanks are changed out periodically by the mentor, who updates the machine-readable configuration file of tank values each time (hb p. 11) |
| Maintenance interval | about once every two years (hb p. 11) |


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
| `AMF` | ARM Mobile Facility |
| `AOSGHG` | atmospheric observation system for greenhouse gases |
| `ARM` | Atmospheric Radiation Measurement |
| `CCL` | Central Calibration Laboratory |
| `CRDS` | cavity ringdown spectrometer |
| `DQR` | Data Quality Report |
| `ENA` | Eastern North Atlantic |
| `GHG` | atmospheric observation system for greenhouse gases |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `OLI` | Oliktok Point, Alaska |
| `QC` | quality control |
| `RMSE` | root-mean-square error |
| `TGP` | tower gas processing system |
| `WMO` | World Meteorological Organization |


### References the handbook cites

- Andrews et al. 2014. "CO2, CO, and CH4 measurements from tall towers in the NOAA Earth System Research Laboratory's Global Greenhouse Gas Reference Network: instrumentation, uncertainty analysis, and recommendations for...
- Bakwin, Tans, Zhao, Ussler, Quesnell. 1995. "Measurements of carbon dioxide on a very tall tower." Tellus B-Chemical and Physical Meteorology 47(5): 535–549
- Bakwin, Tans, Hurst, Zhao. 1998. "Measurements of carbon dioxide on very tall towers: results of the NOAA/CMDL program." Tellus B-Chemical and Physical Meteorology 50(5): 401–415
- Biraud, Torn, Smith, Sweeney, Riley, Tans. 2013. "A multi-year record of airborne CO2 observations in the US Southern Great Plains." Atmospheric Measurement Techniques 6(3): 751–763
- Crosson, ER. 2008. "A cavity ring-down analyzer for measuring atmospheric levels of methane, carbon dioxide, and water vapor." Applied Physics B 92: 403–408
- Tans, Bakwin, Guenther. 1996. "A Feasible global carbon cycle observing system: a plan to decipher today's carbon cycle based on observations." Global Change Biology 2(3): 309–318
- World Meteorological Organization (WMO). 2014. GAW Report No. 213.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ghg_handbook.pdf (13 pages, DOE/SC-ARM-TR-175, by S Biraud, K Reichl)
- Catalog record: ARM data-source index, `instrument_class_code=ghg`, read 2026-09-23
- Example file: `oliaosghgcoeffM1.b1.20210612.053400.nc` from `oliaosghgcoeffM1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
