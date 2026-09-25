---
name: arm-instrument-mwr3c
description: ARM Microwave Radiometer, 3 Channel (mwr3c) - handbook-derived instrument reference. Measurement principle, reported quantities (30 GHz sky brightness temperature, 89 GHz sky brightness temperature, 31 GHz sky brightness temperature, 90 GHz sky brightness temperature, Liquid water path, Precipitable water vapor), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmwr3cC1.b1) and the variable inventory of a real file. Use when working with mwr3c data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties; Radiometric. Triggers - mwr3c, Microwave Radiometer, 3 Channel, sgpmwr3cC1.b1, 30 GHz sky brightness temperature, 89 GHz sky brightness temperature, 31 GHz sky brightness temperature, 90 GHz sky brightness temperature, Cloud Properties, Radiometric.
---

# MWR3C - Microwave Radiometer, 3 Channel

The MWR3C is a ground-based, zenith-pointing three-channel microwave radiometer (23.834, 30, and 89 GHz) deployed at fixed ARM sites and mobile facilities that measures sky brightness temperatures used to retrieve precipitable water vapor and liquid water path.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 24 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mwr3c` |
| Handbook | [DOE/SC-ARM-TR-108 / MP Cadeddu / February 2021](https://www.arm.gov/publications/tech_reports/handbooks/mwr3c_handbook.pdf) |
| Measurement category | Cloud Properties; Radiometric |
| Manufacturer / model | Radiometrics Corporation PR2289C (PR2230 K-band receiver, PR8900 W-band receiver); also RPG systems (including RPG G5) |
| Primary measurements | Liquid water path; Microwave narrowband brightness temperature; Precipitable water |
| Record | 2011-01-11 to 2026-09-23 (active) |
| Datastreams with data | 53 across 23 sites |
| Sites | acx, anx, asi, bnf, crg, dst, ena, epc, gan, guc, hou, kcg, mag, mao |
| ARM page | https://www.arm.gov/capabilities/instruments/mwr3c |


## Credit

Everything this skill knows about the instrument is the work of **MP Cadeddu** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MP Cadeddu. *Microwave Radiometer – 3-Channel (MWR3C) Instrument Handbook*, DOE/SC-ARM-TR-108, February 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mwr3c_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The MWR3C measures sky radiances at three frequencies (23.834, 30, and 89 GHz for Radiometrics systems; 23.8, 31, and 90 GHz for RPG systems), converting them to "equivalent brightness temperatures" through a calibration procedure. Radiation entering the lens passes through a feedhorn to a PIN switch that alternately views the sky, an internal reference load held at a precisely monitored temperature, and a calibrated noise diode injection for gain monitoring. Absolute calibration is performed in the field via tip curves, in which optical thickness is regressed against air mass and extrapolated to zero air mass to determine system noise temperature; RPG systems additionally perform frequent gain calibrations against a black body target. By relating the observed radiances to atmospheric water vapor and liquid water absorption/emission, precipitable water vapor (PWV) and liquid water path (LWP) are derived from the three-frequency brightness temperature measurements using neural network (real-time) and physical (VAP) retrieval algorithms.

**Siting.** In normal operation mode the radiometers observe the sky in zenith position; zenith measurements are interrupted approximately every 15 minutes for scanning tip-curve calibration measurements.

**Sampling.** native rate Integration time greater than =1 s; radiometric resolution 0.4 K RMS@1 s integration time; averaging Zenith measurements interrupted approximately every 15 minutes to collect scanning measurements for absolute calibration (Radiometrics); tip curves collected every 15 minutes (Radiometrics) or every hour with gain calibrations every 5 minutes (RPG non-G5) (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| 23.834 GHz sky brightness temperature (Radiometrics/Tbsky23) | K | - | 0.5 K | - | (hb p. 8) |
| 30 GHz sky brightness temperature (Radiometrics/Tbsky30) | K | - | 0.5 K | - | (hb p. 8) |
| 89 GHz sky brightness temperature (Radiometrics/Tbsky89) | K | - | 1.5 K | - | (hb p. 8) |
| 23.8 GHz sky brightness temperature (RPG/Tbsky23) | K | - | 0.5 K | - | (hb p. 8) |
| 31 GHz sky brightness temperature (RPG/Tbsky31) | K | - | 0.5 K | - | (hb p. 8) |
| 90 GHz sky brightness temperature (RPG/Tbsky90) | K | - | 1.5 K | - | (hb p. 8) |
| Liquid water path (lwp) | mm | - | ~0.015 mm | - | (hb p. 8) |
| Precipitable water vapor (pwv) | cm | - | ~0.05 cm | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Radiometrics/Receiver noise temperature 23.834 GHz | less than  500 K | (hb p. 17) |
| Radiometrics/Receiver noise temperature 30 GHz | less than  500 K | (hb p. 17) |
| Radiometrics/Receiver noise temperature 89 GHz | less than 1100 | (hb p. 17) |
| Radiometrics/Channel bandwidth K-band | 300 MHz | (hb p. 17) |
| Radiometrics/Channel bandwidth W-band | 1900 MHz | (hb p. 17) |
| Radiometrics/Radiometric resolution | 0.4 K RMS@1 s integration time | (hb p. 17) |
| Radiometrics/Receiver and antenna thermal stabilization | less than  30 mK (excluded external lens) | (hb p. 17) |
| Radiometrics/Integration time | greater than =1 s | (hb p. 17) |
| Radiometrics/HPBW K-band channels | ~3.0o | (hb p. 17) |
| Radiometrics/HPBW W-band channel | ~3.5o | (hb p. 17) |
| Radiometrics/Temperature range | -40 to +45 C (environmental chamber tested) | (hb p. 17) |
| RPG/Receiver noise temperature 23.8 GHz | less than  400 K | (hb p. 17) |
| RPG/Receiver noise temperature 31 GHz | less than  400 K | (hb p. 17) |
| RPG/Receiver noise temperature 90 GHz | less than 800 | (hb p. 18) |
| RPG/Channel bandwidth K-band | 230 MHz | (hb p. 18) |
| RPG/Channel bandwidth W-band | 2000 MHz | (hb p. 18) |
| RPG/Radiometric resolution | 0.4 K RMS@1 s integration time | (hb p. 18) |
| RPG/Receiver and antenna thermal stabilization | less than  30 mK (excluded external lens) | (hb p. 18) |
| RPG/Integration time | greater than =1 s | (hb p. 18) |
| RPG/HPBW K-band channels | ~3.0o | (hb p. 18) |
| RPG/HPBW W-band channel | ~1.6 | (hb p. 18) |
| RPG/Temperature range | -40 to +45 C (environmental chamber tested) | (hb p. 18) |


## The data

Verified example: **`sgpmwr3cC1.b1`**, file `sgpmwr3cC1.b1.20260919.000000.nc`
(21.49 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=67021, `frequency`=3, `infrared_wavelength`=1 |
| Data variables | 92 |
| QC variables | 34 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:59 |
| dod version | mwr3c-b1-3.6 |
| process version | ingest-mwr3c-5.9-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ambient_target_sensor_1_temperature` | K | time | yes | Ambient target sensor 1 temperature |
| `ambient_target_sensor_2_temperature` | K | time | yes | Ambient target sensor 2 temperature |
| `azimuth` | degree | time | yes | Azimuth |
| `be_calibrated_gain23` | V / K | time | yes | Best estimate calibrated 23.84 GHz channel gain (sensitivity) |
| `be_calibrated_gain31` | V / K | time | yes | Best estimate calibrated 31.4 GHz channel gain (sensitivity) |
| `be_calibrated_gain90` | V / K | time | yes | Best estimate calibrated 90.0 GHz channel gain (sensitivity) |
| `be_calibrated_trec23` | K | time | yes | Best estimate calibrated 23.84 GHz receiver power scaled to... |
| `be_calibrated_trec31` | K | time | yes | Best estimate calibrated 31.4 GHz receiver power scaled to... |
| `be_calibrated_trec90` | K | time | yes | Best estimate calibrated 90.0 GHz receiver power scaled to... |
| `detector_voltage23` | V | time | yes | 23.84 GHz channel detector voltage |
| `detector_voltage31` | V | time | yes | 31.4 GHz channel detector voltage |
| `detector_voltage90` | V | time | yes | 90.0 GHz channel detector voltage |
| `elevation` | degree | time | yes | Elevation |
| `gain23` | V / K | time | yes | 23.84 GHz channel gain (sensitivity), from LV0 file |
| `gain31` | V / K | time | yes | 31.4 GHz channel gain (sensitivity), from LV0 file |
| `gain90` | V / K | time | yes | 90.0 GHz channel gain (sensitivity), from LV0 file |
| `infrared_temperature` | K | time | yes | Zenith-pointing infrared temperature at 10.5 um |
| `rain_intensity` | mm/s | time | yes | Rain intensity |
| `receiver_1_temperature` | K | time | yes | Receiver 1 temperature |
| `receiver_1_temperature_stability` | K | time | yes | Receiver 1 temperature stability |
| `receiver_2_temperature` | K | time | yes | Receiver 2 temperature |
| `receiver_2_temperature_stability` | K | time | yes | Receiver 2 temperature stability |
| `surface_pressure` | kPa | time | yes | Ambient surface pressure |
| `surface_relative_humidity` | % | time | yes | Ambient surface relative humidity |
| `surface_temperature` | degC | time | yes | Ambient surface temperature |
| `tb_black_body` | K | time | yes | Ambient black body target temperature, from LV0 file |
| `tbsky23` | K | time | yes | 23.84 GHz sky brightness temperature |
| `tbsky31` | K | time | yes | 31.4 GHz sky brightness temperature |
| `tbsky90` | K | time | yes | 90.0 GHz sky brightness temperature |
| `trec23` | K | time | yes | 23.84 GHz receiver power scaled to temperature units, from LV0 file |


_26 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpmwr3cC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmwr3cC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmwr3cC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmwr3cC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("lwp")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This datastream carries 92 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpmwr3cC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["azimuth", "elevation", "tbsky23", "qc_azimuth", "qc_elevation", "qc_tbsky23"],
                                cleanup_qc=True)
```

## Quality control in this datastream

34 `qc_` companion variables cover 34 of the
92 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_azimuth"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("azimuth", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["azimuth", "elevation", "tbsky23"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpmwr3cC1.b1.20260919.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `tbsky90` | Questionable calibration. Refer to instrument handbook. | 2982 | 4.4494 |
| `tbsky31` | Questionable calibration. Refer to instrument handbook. | 1903 | 2.8394 |
| `tbsky23` | Questionable calibration. Refer to instrument handbook. | 1851 | 2.7618 |
| `ambient_target_sensor_1_temperature` | Value is equal to missing_value. | 1104 | 1.6472 |
| `ambient_target_sensor_2_temperature` | Value is equal to missing_value. | 1104 | 1.6472 |
| `receiver_1_temperature` | Value is equal to missing_value. | 1104 | 1.6472 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpmwr3cC1.b1", "20110111", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are named qc_'fieldname' (e.g., qc_tbsky90) with possible values 0 (within specified range), 1 (missing value), 2 (below specified minimum), 4 (above specified maximum), 8 (failed valid delta check), with min/max thresholds listed per field in Table 5. The instrument mentor performs monthly checks (IMMS) including: brightness temperature time series should be smooth with low noise; brightness temperatures should be greater than 2.75 K and less than ~330 K; external temperature should agree with tower measurements within +/- 2 K; external pressure within +/- 5 KPa; external...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Rain and dew contamination of receiver lenses | Elevated/anomalous brightness temperatures during and shortly after rain events; MWR3C brightness temperatures take approximately 5-10 minutes after rain stops to return to normal levels | Rain Effect Mitigation (REM) system blows warm air across lenses when relative humidity exceeds a user-adjustable threshold, and at high speed during... | (hb p. 13) |
| Residual temperature dependence of K-band (23.834 GHz) channel calibration | Slightly higher RMS differences (0.7 K) between measured and modeled brightness temperatures at 23.834 GHz compared to 30 GHz (0.4 K) | Additional temperature correction coefficients (TndTC, c1, c2) applied in calibration procedure to correct residual temperature dependence due to... | (hb p. 12) |
| Noise diode injection temperature (Tnd) drift over time | Instantaneous Tnd values from tip curves show variability/scatter around a running median (see Figure 5) | Median value computed from a sufficiently large number of acceptable tip curves (user-selectable acceptance criterion) used in brightness temperature... | (hb p. 13) |
| Intermittent MET sensor data on E32 unit | Gaps or intermittent values in surface meteorological instrumentation (MET) variables starting June 2018 | Documented in DQPR 7158 | (hb p. 8) |
| Tip curve quality/misalignment errors (RPG) | Low correlation coefficient (R) for a tip curve regression | A tip curve is considered good only if the correlation coefficient of the regression exceeds a predefined threshold of 0.995; radiometer scans on... | (hb p. 15) |
| Data quality flag thresholds exceeded | qc_ fields flagged: 1 (missing value), 2 (value less than specified minimum), 4 (value greater than specified maximum), 8 (value failed valid delta check) | Compare qc_'fieldname' flags against thresholds in Table 5 | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field calibration exclusively via tip curves: linear regression of optical thickness versus air mass extrapolated to zero air mass to determine system noise temperature plus 2.7 K; gain monitored via periodic calibrated noise diode injection; RPG systems perform tip curves every hour and gain calibrations every 5... (hb p. 13) |
| Calibration interval | Tip curves every 15 minutes (Radiometrics); tip curves every hour and gain calibration every 5 minutes (RPG); continuous (RPG G5) (hb p. 13) |
| Traceability | Processing of tip curves designed to be consistent with the MWR's and MWRHF's calibration procedures (Liljegren 2000; Cadeddu et al. 2013) (hb p. 13) |
| Routine maintenance | To be written (hb p. 16) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MWR (microwave radiometer, 2-channel), MWRHF, MWRRET (value-added product).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `MWR3C` | microwave radiometer−3-channel |
| `PWV` | precipitable water vapor |
| `LWP` | liquid water path |
| `REM` | Rain Effect Mitigation |
| `MWRRET` | MWR Retrievals value-added product |
| `Tnd` | noise diode injection temperature |
| `Tmr` | atmospheric mean radiating temperature |
| `IMMS` | instrument mentor monthly summary |
| `DQPR` | Data Quality Problem Report |
| `LNA` | low-noise amplifier |
| `Uncertainty` | the range of probable maximum deviation of a measured value from the true value within a... |


### References the handbook cites

- Cadeddu, MP, JC Liljegren, and DD Turner. 2013. "The atmospheric radiation measurement (ARM) program network of microwave radiometers: Instrumentation, data, and retrievals." Atmospheric Measurement Techniques 6(9):...
- Cadeddu, MP, DD Turner, and JC Liljegren, 2009. "A neural network for real-time retrievals of PWV and LWP from arctic millimeter-wave ground-based observations." IEEE Transactions on Geoscience and Remote Sensing 47(7):...
- Liljegren, JC. 2000. "Automatic self-calibration of ARM microwave radiometers," in Microwave Radiometry and Remote Sensing of the Earth's Surface and Atmosphere, P. Pampaloni and S. Paloscia, Eds. VSP Book, Lorton,...
- RPG_MWR_STD_Technical_Manual_2015

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mwr3c_handbook.pdf (24 pages, DOE/SC-ARM-TR-108, by MP Cadeddu)
- Catalog record: ARM data-source index, `instrument_class_code=mwr3c`, read 2026-09-23
- Example file: `sgpmwr3cC1.b1.20260919.000000.nc` from `sgpmwr3cC1.b1`, 21.49 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
