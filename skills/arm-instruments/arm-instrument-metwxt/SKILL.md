---
name: arm-instrument-metwxt
description: ARM WXT520/530 Meteorological Instrument System (metwxt) - handbook-derived instrument reference. Measurement principle, reported quantities (Atmospheric pressure, Relative humidity, Temperature, Relative humidity, Temperature, Wind speed, Wind direction, Wind speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (crgmetwxtM1.b1) and the variable inventory of a real file. Use when working with metwxt data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - metwxt, WXT520/530 Meteorological Instrument System, crgmetwxtM1.b1, Atmospheric pressure, Relative humidity, Temperature, Wind speed, Surface Meteorology, Vaisala PTB330 Barometer, Vaisala HMP155 Humidity and Temperature Probe, AOSMET, TBRG.
---

# METWXT - WXT520/530 Meteorological Instrument System

The Surface Meteorological System (MET) is a set of ground-based instruments deployed at ARM fixed and mobile facility sites that records standard surface meteorological variables—temperature, relative humidity, pressure, wind speed and direction, precipitation, and (at most sites) visibility and present weather—once per minute at standard heights following WMO guidelines.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `metwxt` |
| Handbook | [DOE/SC-ARM-TR-086 / J Kyrouac, M Tuftedal / June 2024](https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Vaisala PTB330 Barometer; Vaisala HMP155 Humidity and Temperature Probe; Vaisala HMT337 Humidity and Temperature Transmitter; RM Young 43502 Aspirated Radiation Shield; RM Young 05103/05106 Wind... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind; Precipitation |
| Record | 2018-10-01 to 2026-09-24 (active) |
| Datastreams with data | 9 across 5 sites |
| Sites | anx, bnf, cor, crg, dst |
| ARM page | https://www.arm.gov/capabilities/instruments/metwxt |


## Credit

Everything this skill knows about the instrument is the work of **J Kyrouac, M Tuftedal** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Kyrouac, M Tuftedal. *Surface Meteorological System (MET) Instrument Handbook*, DOE/SC-ARM-TR-086, June 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `metwxt`, ARM links no handbook to this class. The facts below come from the **Surface Meteorological Instrumentation** (`met`) handbook, which documents the parent system. The same document also covers `marinemet`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `metwxt` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

Pressure is measured by a Vaisala PTB330 barometer using a BAROCAP silicon capacitive absolute sensor with microprocessor correction for linearity and temperature dependence. Temperature and relative humidity are measured using a Pt100 resistive platinum sensor and a HUMICAP capacitive thin film polymer sensor (HMP155), or via a warmed-probe technique that prevents saturation at high humidity by heating the sensor above ambient temperature (HMT337). Wind speed and direction are measured either mechanically, using a helicoid four-blade propeller producing an AC sine wave signal proportional to speed and a potentiometer producing a voltage proportional to vane position (RM Young 05103/05106), or acoustically, by measuring transit time of pulses between three transducers with no moving parts (Vaisala WMT700). Visibility and present weather are determined using light-scattering principles and a capacitive RAINCAP rain sensor that analyzes signal amplitude changes to infer precipitation intensity and type (PWD22). Precipitation is measured by a heated tipping bucket mechanism with a magnetic reed switch (each tip = 0.254 mm) or by an optical rain gauge that translates scintillation intensity of a transmitted infrared beam into precipitation rate and type.

**Siting.** Measurements are taken once a minute at standard heights following WMO guidelines: barometer at 1 meter inside electronics enclosure; temperature/humidity probe at 2 meters in an aspirated radiation shield on a crossarm; wind sensor at standard 10 meters (with historical exceptions at 3m, 6m, or 12m at some AMF1/ENA deployments); PWD22 and optical rain gauge mounted on tripod or crossarm at 2-3 meters. Slight variations in instrumentation exist depending on site or mobile facility deployment. Pressure is reported as station pressure (not corrected to sea level).

**Sampling.** native rate once a minute; reported every 1 min raw data, processed into daily quality-flagged files (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Atmospheric pressure | hPa | 500-1100 hPa | ± 0.15 hPa (total accuracy) | - | (hb p. 7) |
| Relative humidity (HMP155) | % RH | 0-100% | ± (1.0 + 0.008 x reading) % RH (at -20-40°C) | - | (hb p. 7) |
| Temperature (HMP155) | °C | -80-60°C | ± (0.1 + 0.00167 x /temperature/) °C | - | (hb p. 7) |
| Relative humidity (HMT337) | % RH | 0-100% | ± 1 % RH (at 0-90 % RH, 15-25°C); ± 1.7 % RH... | - | (hb p. 7) |
| Temperature (HMT337) | °C | -70-180°C | ± 0.1°C | - | (hb p. 7) |
| Wind speed (RM Young 05103/05106) | m/s | 0-100 m/s | ± 0.3 m/s, or 1% of reading, whichever is... | - | (hb p. 8) |
| Wind direction (RM Young 05103/05106) | degrees | 0°-360° | ± 3° | - | (hb p. 8) |
| Wind speed (Vaisala WMT700) | m/s | 0-75 m/s | ± 0.1 m/s or 2% of reading, whichever is greater | - | (hb p. 8) |
| Wind direction (Vaisala WMT700) | degrees | 0-360° | ± 2° | - | (hb p. 8) |
| Visibility (PWD22) | m | 0-20000 m | ± 10% (at 10-10000 m); ± 20% (at 10000-20000 m) | - | (hb p. 8) |
| Precipitation intensity (PWD22) | mm | 0-999.99 mm | none listed | - | (hb p. 8) |
| Precipitation amount (PWD22) | mm | 0-99.99 mm | none listed | - | (hb p. 8) |
| Snow (PWD22) | mm | 0-999 mm | none listed | - | (hb p. 8) |
| Precipitation (Novalynx TBRG) | in/hr | - | ± 1% (at 1-3 in/hr); ± 3% (at 0-6 in/hr) | one tip = 0.254 mm... | (hb p. 8) |
| Precipitation intensity (ORG-815-DS) | mm/hr | 0.1-500 mm/hr | ± 5% accumulation | - | (hb p. 8) |
| Precipitation accumulation (ORG-815-DS) | mm | 0.001-999.999 mm | ± 5% accumulation | - | (hb p. 8) |
| Snow intensity (ORG-815-DS) | mm/hr, liquid equivalent | 0.01-50 mm/hr | ± 10% | - | (hb p. 8) |
| Snow accumulation (ORG-815-DS) | mm, liquid equivalent | 0.001-999.999 mm | ± 10% | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Pressure Range (PTB330) | 500-1100 hPa | (hb p. 7) |
| Pressure Total accuracy (PTB330) | ± 0.15 hPa | (hb p. 7) |
| RH range (HMP155) | 0-100% | (hb p. 7) |
| RH accuracy (HMP155, at -20-40°C) | ± (1.0 + 0.008 x reading) % RH | (hb p. 7) |
| Temperature range (HMP155) | -80-60°C | (hb p. 7) |
| Temperature accuracy (HMP155) | ± (0.1 + 0.00167 x /temperature/) °C | (hb p. 7) |
| RH range (HMT337) | 0-100% | (hb p. 7) |
| RH accuracy (HMT337, 15-25°C, 0-90% RH) | ± 1 % RH | (hb p. 7) |
| RH accuracy (HMT337, 15-25°C, 90-100% RH) | ± 1.7 % RH | (hb p. 7) |
| RH accuracy (HMT337, -20-40°C) | ± (1.0 + 0.008 x reading) % RH | (hb p. 7) |
| Temperature range (HMT337) | -70-180°C | (hb p. 7) |
| Temperature accuracy (HMT337) | ± 0.1°C | (hb p. 7) |
| Radiation error (RM Young 43502 shield) | 0.2°C RMS at 1000 W/m2 intensity | (hb p. 7) |
| Wind speed range (RM Young 05103/05106) | 0-100 m/s | (hb p. 8) |
| Wind speed accuracy (RM Young 05103/05106) | ± 0.3 m/s, or 1% of reading, whichever is greater | (hb p. 8) |
| Wind direction range (RM Young 05103/05106) | 0°-360° | (hb p. 8) |
| Wind direction accuracy (RM Young 05103/05106) | ± 3° | (hb p. 8) |
| Wind speed range (WMT700) | 0-75 m/s | (hb p. 8) |
| Wind speed accuracy (WMT700) | ± 0.1 m/s or 2% of reading, whichever is greater | (hb p. 8) |
| Wind direction range (WMT700) | 0-360° | (hb p. 8) |
| Wind direction accuracy (WMT700) | ± 2° | (hb p. 8) |
| Visibility range (PWD22) | 0-20000 m | (hb p. 8) |
| Visibility accuracy (PWD22, 10-10000 m) | ± 10% | (hb p. 8) |
| Visibility accuracy (PWD22, 10000-20000 m) | ± 20% | (hb p. 8) |
| Precipitation intensity range (PWD22) | 0-999.99 mm | (hb p. 8) |
| Precipitation amount range (PWD22) | 0-99.99 mm | (hb p. 8) |


_10 further specification rows are in the handbook._

## The data

Verified example: **`crgmetwxtM1.b1`**, file `crgmetwxtM1.b1.20251128.000000.nc`
(0.19 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 29 |
| QC variables | 10 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2025-11-28T00:00:00 to 2025-11-28T23:59:00 |
| dod version | metwxt-b1-1.2 |
| process version | ingest-metwxt-1.2-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `atmos_pressure` | kPa | time | yes | Atmospheric pressure |
| `logger_temp` | degC | time | yes | Logger temperature |
| `logger_volt` | V | time | yes | Logger voltage |
| `rh_mean` | % | time | yes | Relative humidity mean |
| `temp_mean` | degC | time | yes | Temperature mean |
| `wdir_vec_mean` | degree | time | yes | Wind direction vector mean |
| `wspd_arith_mean` | m/s | time | yes | Wind speed arithmetic mean |
| `wspd_vec_mean` | m/s | time | yes | Wind speed vector mean |
| `wxt_cumul_precip` | mm | time | yes | WXT cumulative precipitation |
| `wxt_precip_rate_mean` | mm/hr | time | yes | WXT mean precipitation rate |
| `rh_std` | % | time | - | Relative humidity standard deviation |
| `temp_std` | degC | time | - | Temperature standard deviation |
| `time` | - | time | - | Time offset from midnight |
| `wdir_vec_std` | degree | time | - | Wind direction vector mean standard deviation |


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
                     params={"user": f"{user}:{token}", "ds": "crgmetwxtM1.b1",
                             "start": "2025-11-28", "end": "2025-11-28", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./crgmetwxtM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "crgmetwxtM1.b1", "2025-11-28", "2025-11-28")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("crgmetwxtM1.b1", "2025-11-28", "2025-11-28"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("temp_mean", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

10 `qc_` companion variables cover 10 of the
29 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_temp_mean"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("temp_mean", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["temp_mean", "rh_mean", "atmos_pressure"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("crgmetwxtM1.b1", "20181001", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data Quality Reports (DQRs) are provided with MET data downloads for specified times/variables where data quality may have been compromised (e.g., instrument problems, power outages, calibration issues, environmental events); these events are not necessarily flagged by automated QC variables, so DQRs should be reviewed before use, and suggestions for use are often included. PWD communication interruption values are flagged by QC and should be removed from study. Raw data are processed into daily quality-flagged files; information on variables and QC flags is in file headers.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Vaisala PWD22 precipitation accuracy not listed | No stated uncertainty for precipitation intensity/amount/snow values from PWD22 | PWD precipitation data should only be used as a supplemental means of verification unless all other precipitation data are unavailable | (hb p. 8) |
| Optical rain gauge not suited for solid precipitation / snow performance issues | Snow events poorly captured or missed by ORG-815-DS | Use heated tipping bucket or present weather detector precipitation data for snow; this instrument not typically used for snow | (hb p. 8) |
| Optical rain gauge overestimation of precipitation, especially light/transitional rain | Small precipitation events reported that may be spurious, sensitive to fog or high humidity | Cross-reference precipitation data with other sensors (TBRG, PWD, etc.) to verify validity | (hb p. 10) |
| HMP45 cold bias in high humidity and RH drift (SGP ~2007-2018) | Cold bias apparent in temperature during high humidity periods; RH readings may show drift over time | See technical report DOE/SC-ARM-TR-192 for details | (hb p. 10) |
| Ultrasonic wind sensor dropouts/spikes due to transducer interference | Wind data dropouts or spikes visible in time series, typically during heavy wet snow, ice conditions, or bird interference | none stated beyond noting cause | (hb p. 10) |
| CMH (chilled mirror hygrometer) daily self-check artifact | Spike/drop in relative humidity and dew point data at regular daily interval (see Figure 4) | Compare with HMT337 data to verify readings are similar | (hb p. 10) |
| CMH delayed operating temperature after self-check | Mirror takes longer than typical few minutes to reach normal operating temperature, visible as extended anomaly (Figure 5) | Compare with HMT337 data to verify readings are similar; usually obvious on a time series plot | (hb p. 10) |
| PWD communication interruption | Sensor serial number momentarily reported as rain rate (Figure 6) | These values are flagged by QC and should be removed from study | (hb p. 10) |
| Chilled mirror hygrometer (TSL-1088) poor performance in arctic conditions | Degraded/unreliable humidity data at NSA and AMF3-OLI leading to removal of instrument | Instrument removed from deployment (late 2019) | (hb p. 7) |
| Optical rain gauge removed from NSA due to poor arctic performance | No optical rain gauge data present in NSA MET datastream after late 2003 | Instrument removed | (hb p. 8) |
| Pressure not corrected to sea level | Reported pressure values represent station pressure at 1m above ground level, not sea-level-adjusted values | None; station pressure is the reported quantity by design | (hb p. 12) |
| Wind sensor mounting height deviations at some AMF1/ENA deployments | Wind speed/direction values reflect non-standard mounting heights (3m, 6m, or 12m) rather than standard 10m during specific site/time periods | Refer to Section 3.0 historical background for site/time-specific heights | (hb p. 6) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field-checked using transfer standard equipment or field calibration kit; instrument replaced/adjusted if out of tolerance and sent to manufacturer for calibration when applicable (hb p. 9) |
| Calibration interval | Varies by instrument: PTB330 barometer every 6 months (also at install/removal); HMP155 every 6 months (also at install/removal); HMT337 yearly (also at installation); RM Young 05103/05106 wind monitor every 6 months; WMT700 none required; PWD22 yearly (also at installation); Novalynx TBRG every 6 months (also at... (hb p. 9) |
| Routine maintenance | Daily: live data checked on remote display to verify communications, updating data, and no errors/dropouts/flatlines. Biweekly: instruments, cabling, mountings, electronics inspected for physical damage, obstructions, cleanliness; tip test performed on tipping bucket rain gauges; mentor notified of problems for... (hb p. 14) |
| Maintenance interval | Daily and biweekly checks (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AOSMET.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `MET` | surface meteorological system |
| `AMF1` | ARM Mobile Facility 1 |
| `AMF2` | ARM Mobile Facility 2 |
| `AMF3` | ARM Mobile Facility 3 |
| `AOSMET` | Aerosol Observing System Meteorological Sensor |
| `ARM` | Atmospheric Radiation Measurement |
| `CMH` | chilled mirror hygrothermometer |
| `DQO` | Data Quality Office |
| `DQR` | Data Quality Report |
| `ENA` | Eastern North Atlantic |
| `NSA` | North Slope of Alaska |
| `ORG` | optical rain gauge |
| `PWD` | present weather gauge |
| `QC` | quality control |


### References the handbook cites

- Kyrouac, J, and A Theisen. 2018. Biases of the MET Temperature and Relative Humidity Sensor (HMP45) Report. ARM Climate Research Facility. DOE/SC-ARM-TR-192, https://doi.org/10.2172/1366737
- World Meteorological Organization. 2008. Guide to Meteorological Instruments and Methods of Observation (Seventh Edition). WMO-No. 8.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/met_handbook.pdf (20 pages, DOE/SC-ARM-TR-086, by J Kyrouac, M Tuftedal)
- Catalog record: ARM data-source index, `instrument_class_code=metwxt`, read 2026-09-24
- Example file: `crgmetwxtM1.b1.20251128.000000.nc` from `crgmetwxtM1.b1`, 0.19 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
