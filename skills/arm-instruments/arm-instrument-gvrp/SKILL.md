---
name: arm-instrument-gvrp
description: ARM G-band (183 GHz) Vapor Radiometer Profiler (gvrp) - handbook-derived instrument reference. Measurement principle, reported quantities (Brightness temperature, Frequency, Elevation, surfacePressure, surfaceTemperature, surfaceRelativeHumidity, surfaceRainFlag, blackBodyTemperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsagvrpC1.b1) and the variable inventory of a real file. Use when working with gvrp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - gvrp, G-band (183 GHz) Vapor Radiometer Profiler, nsagvrpC1.b1, Brightness temperature, Frequency, Elevation, surfacePressure, surfaceTemperature, surfaceRelativeHumidity, Radiometric, Radiometrics Corporation, MP-3000A series (MP3000A, Uncertainty, IMMS.
---

# GVRP - G-band (183 GHz) Vapor Radiometer Profiler

The GVRP measures time-series brightness temperatures at 15 channels between 170 and 183.31 GHz to derive water vapor and liquid water information, deployed as a ground-based zenith/elevation-scanning microwave radiometer at fixed ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gvrp` |
| Handbook | [DOE/SC-ARM/TR-091 / MP Cadeddu / June 2010](https://www.arm.gov/publications/tech_reports/handbooks/gvrp_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Radiometrics Corporation, MP-3000A series (MP3000A, model 183-2) |
| Primary measurements | Microwave narrowband brightness temperature |
| Record | 2008-04-01 to 2026-07-14 (retired) |
| Datastreams with data | 6 across 2 sites |
| Sites | awr, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/gvrp |


## Credit

Everything this skill knows about the instrument is the work of **MP Cadeddu** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MP Cadeddu. *G-Band Vapor Radiometer Profiler (GVRP) Handbook*, DOE/SC-ARM/TR-091, June 2010.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/gvrp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Downwelling atmospheric radiation passes through the instrument radome and is reflected by a parabolic mirror into the receiver feed-horn. Microwave channels are selected using a frequency synthesizer, and the input power is down-converted to an intermediate frequency, then amplified, filtered, and detected. Atmospheric emission in this spectral region is primarily due to water vapor, with some influence from liquid water; channels between 170.0 and 176.0 GHz are particularly sensitive to liquid water. The receiver has a noise source (noise diode) used to calibrate the gain, and the instrument scans eleven elevation angles at each observing cycle. The 183.31-GHz line sensitivity to water vapor is approximately 30 times higher than the two-channel MWR for PWV less than 2.5 mm, making the GVRP especially useful in low-humidity conditions and capable of providing low-resolution vertical profiles of water vapor in very dry conditions.

**Siting.** Deployed at NSA/C1 (North Slope of Alaska); instrument uses a parabolic mirror to reflect downwelling atmospheric radiation into the receiver feed-horn, with elevation-scanning capability (eleven elevation angles per observing cycle) and a super-blower activated when the rain sensor detects rain to keep the radome clear of rain or snow.

**Sampling.** native rate ~ 1/20 s; averaging 0.25 K radiometric noise at 250 ms averaging time (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Brightness temperature | K | - | 2 K | - | (hb p. 7) |
| Frequency | GHz | 170.0, 171.0, 172.0, 173.0, 174.0,... | - | - | (hb p. 7) |
| Elevation | Degrees | 90=zenith viewing | - | - | (hb p. 7) |
| surfacePressure | kPa | - | 2.0 | - | (hb p. 7) |
| surfaceTemperature | K | - | 1.0 | - | (hb p. 7) |
| surfaceRelativeHumidity | % | - | 5.0 | - | (hb p. 7) |
| surfaceRainFlag | count | - | - | - | (hb p. 7) |
| blackBodyTemperature | K | - | 0.25 K | - | (hb p. 8) |
| noiseDiodePhysicalTemp | K | - | 0.25 K | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Data interface Primary computer port | RS422 57600 kb/s 8N1 | (hb p. 10) |
| Data interface Auxiliary computer port | RS422 1.2—57600 kb/s 8N1 | (hb p. 10) |
| Power requirement (100 to 250 VAC / 50–60 Hz) | ~ 200 W (400 W at cold start) | (hb p. 10) |
| Weight | 27 kg | (hb p. 10) |
| Size | 50 X 28 X 76 cm | (hb p. 10) |
| Radiometric noise | 0.25 K (250 ms averaging time) | (hb p. 10) |
| Long term stability | less than  1 K over 1 yr | (hb p. 10) |
| Measurement rate | ~ 1/20 s | (hb p. 10) |
| Antenna beamwidth | 1.0° | (hb p. 10) |
| Temperature range | -50° to 50°C | (hb p. 10) |
| Output | ASCII data files | (hb p. 10) |


## The data

Verified example: **`nsagvrpC1.b1`**, file `nsagvrpC1.b1.20260711.000524.cdf`
(0.58 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=3106, `frequency`=15 |
| Data variables | 19 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 25 s |
| File time span | 2026-07-11T00:05:24 to 2026-07-11T23:56:13 |
| sampling interval | 22 seconds |
| averaging interval | None |
| dod version | gvrp-b1-1.3 |
| process version | ingest-gvrp-2.6-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `blackBodyTemperature` | K | time | yes | Internal blackbody reference temperature |
| `brightnessTemperature` | K | time,frequency | yes | Microwave brightness temperature |
| `surfacePressure` | kPa | time | yes | Ambient surface pressure |
| `surfaceRainFlag` | None | time | yes | Rain flag |
| `surfaceRelativeHumidity` | % | time | yes | Ambient surface relative humidity |
| `surfaceTemperature` | K | time | yes | Ambient surface absolute temperature |
| `time` | - | time | yes | Time offset from midnight |
| `elevation` | degrees | time | - | Elevation angle |
| `frequency` | GHz | frequency | - | Frequency |


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
                     params={"user": f"{user}:{token}", "ds": "nsagvrpC1.b1",
                             "start": "2026-07-11", "end": "2026-07-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsagvrpC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsagvrpC1.b1", "2026-07-11", "2026-07-11")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsagvrpC1.b1", "2026-07-11", "2026-07-11"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("blackBodyTemperature", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

7 `qc_` companion variables cover 6 of the
19 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_blackBodyTemperature"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("blackBodyTemperature", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["blackBodyTemperature", "brightnessTemperature", "surfacePressure"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("nsagvrpC1.b1", "20080401", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are named qc_'fieldname'. Possible values: 0 (within specified range), 1 (missing value), 2 (less than specified minimum), 4 (greater than specified maximum), 8 (failed valid delta check). Thresholds given in Table 5 for BrightnessTemperature (3-320), surfacePressure (80-110 kPa), surfaceTemperature (223.15-323 K), surfaceRelativeHumidity (1-110%), blackBodyTemperature (243-320 K). Instrument mentor submits a monthly IMMS summary report performing checks: brightness temperature time series should be smooth with low noise; brightness temperatures should be between 2.75 K and...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Instrument does not perform tip curves | No tip-curve-derived calibration checks available; calibration relies solely on black body/noise diode/LN2 methods | Not applicable - GVRP channels are too opaque for tip curves | (hb p. 6) |
| Liquid water sensitivity in wing channels | Channels between 170.0 and 176.0 GHz show enhanced brightness temperature response during liquid water presence (e.g., clouds), potentially confounding pure water vapor retrievals | - | (hb p. 6) |
| Nonlinear response to PWV | Brightness temperature response to precipitable water vapor is nonlinear, especially at high sensitivity channels near 183.31 GHz | - | (hb p. 6) |
| Low utility at high humidity | Measurements are most useful/valid during low-humidity conditions (PWV less than  5 mm); at higher PWV the 183.31 GHz channels may saturate or lose sensitivity | Use GVRP data preferentially during low-humidity (PWV less than  5 mm) conditions | (hb p. 6) |
| Rain/snow contamination of radome | Brightness temperature readings become unreliable during precipitation due to water/snow on radome | Super-blower activates automatically when rain sensor detects rain to keep radome clear of rain or snow | (hb p. 10) |
| Data quality flag thresholds exceeded | qc_ flags set to 1 (missing), 2 (below minimum), 4 (above maximum), or 8 (failed delta check) for fields such as BrightnessTemperature, surfacePressure, surfaceTemperature,... | Consult qc_'fieldname' flags and thresholds in Table 5 | (hb p. 8) |
| Brightness temperature out-of-physical-range | Values below 2.75 K or above ~310 K flagged as suspect by mentor review; ambient temperature in Barrow not expected to exceed 30°C | Mentor performs monthly review comparing to expected physical bounds | (hb p. 9) |
| Surface meteorological sensor disagreement with tower measurements | Surface temperature, pressure, or relative humidity readings differing from tower measurements beyond +/- 2 K (temperature), ~5 kPa (pressure), or 5% (relative humidity) | Compare routinely to tower measurements as a quality check | (hb p. 9) |
| Discrepancy with model computations | Measured brightness temperatures deviating from model-computed brightness temperatures | Routine comparison with model computations as a general quality check | (hb p. 9) |
| Noise diode temperature dependence drift | Systematic bias in calibrated brightness temperature if noise diode temperature correction (Tc) is inaccurate | Field calibration of effective noise diode temperature; factory-determined temperature correction coefficients (K1-K4) applied | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Each channel is factory-calibrated to determine seven parameters used in the calibration algorithm (linearity correction exponent α, 1/f noise suppression coefficient dTdG, four temperature correction coefficients for noise diode temperature dependence Ki, and the effective noise diode temperature at T=290 K Tnd290).... (hb p. 6) |
| Calibration interval | LN2 calibration every 3–4 months (also stated as every three months) (hb p. 6) |
| Traceability | Calibration information available in the calibration database and upon request to the instrument mentor (hb p. 6) |
| Routine maintenance | Routine and corrective maintenance documentation not available for this instrument system. Super-blower activates automatically when rain sensor detects rain to keep radome clear. (hb p. 9) |
| Maintenance interval | LN2 calibration every 3-4 months (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: two-channel microwave radiometer (MWR).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Uncertainty` | The range of probable maximum deviation of a measured value from the true value within a... |
| `PWV` | Precipitable water vapor amount |
| `MWR` | Two-channel microwave radiometer |
| `IMMS` | Monthly summary report submitted by the instrument mentor |


### References the handbook cites

- Radiometrics MP-183 User's Manual, REV. A.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/gvrp_handbook.pdf (14 pages, DOE/SC-ARM/TR-091, by MP Cadeddu)
- Catalog record: ARM data-source index, `instrument_class_code=gvrp`, read 2026-09-23
- Example file: `nsagvrpC1.b1.20260711.000524.cdf` from `nsagvrpC1.b1`, 0.58 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
