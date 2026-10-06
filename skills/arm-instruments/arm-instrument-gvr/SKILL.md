---
name: arm-instrument-gvr
description: ARM G-band (183 GHz) Vapor Radiometer (gvr) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsagvrC1.c1) and the variable inventory of a real file. Use when working with gvr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - gvr, G-band (183 GHz) Vapor Radiometer, nsagvrC1.c1, Radiometric, ProSensing, Inc. (Amherst, Uncertainty, NEDT, IMMS.
---

# GVR - G-band (183 GHz) Vapor Radiometer

The G-Band Vapor Radiometer (GVR) provides time-series measurements of brightness temperatures from four double sideband channels centered around the 183.31-GHz water vapor line, deployed at a fixed ground site (NSA/C1) to characterize water vapor and liquid water especially in low-humidity conditions (PWV less than  5 mm).

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gvr` |
| Handbook | [DOE/SC-ARM/TR-076 / MP Cadeddu / March 2011](https://www.arm.gov/publications/tech_reports/handbooks/gvr_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | ProSensing, Inc. (Amherst, Massachusetts) G-Band Vapor Radiometer (GVR) |
| Primary measurements | Microwave narrowband brightness temperature; Precipitable water |
| Record | 2006-09-28 to 2024-07-07 (retired) |
| Datastreams with data | 4 across 1 sites |
| Sites | nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/gvr |


## Credit

Everything this skill knows about the instrument is the work of **MP Cadeddu** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MP Cadeddu. *GVR Radiometer Handbook*, DOE/SC-ARM/TR-076, March 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/gvr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The GVR measures brightness temperatures from four double-sideband channels centered at ±1, ±3, ±7, and ±14 GHz around the 183.31-GHz water-vapor line, where atmospheric emission is primarily due to water vapor with some influence from liquid water. Downwelling atmospheric radiation is captured by a 10-cm diameter, 1.7° beamwidth, 90-degree parabolic metal mirror and focused to a corrugated feed horn, where a sub-harmonically pumped mixer using a 91.655-GHz LO signal down-converts the sidebands to base-band. A broadband low-noise amplifier and power splitter divide the amplified signal among four channels before filtering, and the band-limited noise signals are square-law detected and converted to a TTL pulse-train via voltage-to-frequency converters, then frequency-counted using an FPGA processor, which effectively integrates and measures the noise power. Since no low-loss fast switches are available at G-band, external hot and warm calibration absorbers are used to track receiver gain and offset, with the mirror rotated by a stepper motor to point at the calibration loads. The 183.31±14-GHz channel is particularly sensitive to the presence of liquid water, and the sensitivity to water vapor of the 183.31-GHz line is approximately 30 times higher than the MWR frequencies for PWV less than 2.5 mm.

**Siting.** Deployed at NSA/C1 (North Slope of Alaska, Barrow), installed 2000/09/1, operational. The instrument points its beam via a rotating metal mirror between sky, warm load, and hot load calibration targets.

**Sampling.** native rate Measurement rate 10/min with continuous calibration; instrument calibrates once every 10 seconds; averaging A filter is applied to raw data (counts) and final brightness temperatures: for each data point, if the difference from the max/min of the first four neighbors exceeds 3 K, the point is replaced with the average of the four neighbors. (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| 183.3 ± 1 GHz sky brightness temperature (filtered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 3 GHz sky brightness temperature (filtered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 7 GHz sky brightness temperature (filtered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 14 GHz sky brightness temperature (unfiltered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 1 GHz sky brightness temperature (unfiltered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 3 GHz sky brightness temperature (unfiltered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 7 GHz sky brightness temperature (unfiltered) | K | - | 2 K | - | (hb p. 7) |
| 183.3 ± 14 GHz sky brightness temperature (filtered) | K | - | 2 K | - | (hb p. 7) |
| Precipitable Water Vapor (pwv, value-added product) | - | - | pw_error (associated uncertainty variable) | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Receiver noise temperature 1 GHz | 1750 K | (hb p. 12) |
| Receiver noise temperature 3 GHz | 1610 K | (hb p. 12) |
| Receiver noise temperature 7 GHz | 1600 K | (hb p. 12) |
| Receiver noise temperature 14 GHz | 2170 K | (hb p. 12) |
| Measurement precision, NEDT (Noise Equivalent Delta-T) | 0.2 K | (hb p. 12) |
| Measurement Stability (Allan STD) | less than  0.05 K over 1000 s | (hb p. 12) |
| Measurement rate | 10/min with continuous calibration | (hb p. 12) |
| Antenna aperture | 4" | (hb p. 12) |
| Antenna beamwidth | 1.5° | (hb p. 12) |
| Temperature range | -40 to 10 C | (hb p. 12) |
| Output | ASCII data files | (hb p. 12) |


## The data

Verified example: **`nsagvrC1.c1`**, file `nsagvrC1.c1.20240703.000011.nc`
(0.64 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4881 |
| Data variables | 33 |
| QC variables | 10 (`qc_` companions) |
| Median time step | 17 s |
| File time span | 2024-07-03T00:00:11 to 2024-07-03T23:59:51 |
| sampling interval | variable (approximately 6 to 12 seconds) |
| averaging interval | None |
| dod version | gvr-c1-1.1 |
| process version | vap-gvrpwv-4.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pwv` | mm | time | yes | Precipitable water vapor retrieved using a Neural Network algorithm |
| `pwv_error` | mm | time | yes | Estimated 1-sigma uncertainty in precipitable water vapor retrieval |
| `tbsky1` | K | time | yes | 183.3 +/- 1 GHz sky brightness temperature |
| `tbsky14` | K | time | yes | 183.3 +/- 14 GHz sky brightness temperature |
| `tbsky3` | K | time | yes | 183.3 +/- 3 GHz sky brightness temperature |
| `tbsky7` | K | time | yes | 183.3 +/- 7 GHz sky brightness temperature |
| `temp_hot1` | C | time | yes | Temperature of the hot absorber at the tip |
| `temp_hot2` | C | time | yes | Temperature of the hot absorber at the center |
| `temp_warm` | C | time | yes | Temperature of the warm absorber |
| `time` | - | time | yes | Time offset from midnight |
| `tbsky14u` | K | time | - | Unfiltered 183.3 +/- 14 GHz sky brightness temperature |
| `tbsky1u` | K | time | - | Unfiltered 183.3 +/- 1 GHz sky brightness temperature |
| `tbsky3u` | K | time | - | Unfiltered 183.3 +/- 3 GHz sky brightness temperature |
| `tbsky7u` | K | time | - | Unfiltered183.3 +/- 7 GHz sky brightness temperature |
| `temp_antenna_feed_horn` | C | time | - | Physical temperature of antenna feed horn |
| `temp_component_plate` | C | time | - | Physical temperature of component plate |
| `temp_ext` | C | time | - | Temperature of external sensor |
| `temp_noise_diode` | C | time | - | Physical temperature of noise diode |
| `temp_thermoelectric_cooling_plate` | C | time | - | Physical temperature of thermoelectric cooling plate |


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
                     params={"user": f"{user}:{token}", "ds": "nsagvrC1.c1",
                             "start": "2024-07-03", "end": "2024-07-03", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsagvrC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsagvrC1.c1", "2024-07-03", "2024-07-03")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsagvrC1.c1", "2024-07-03", "2024-07-03"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("tbsky1", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

10 `qc_` companion variables cover 9 of the
33 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_tbsky1"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("tbsky1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["tbsky1", "tbsky3", "tbsky7"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsagvrC1.c1.20240703.000011.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `tbsky1` | Value is greater than the fail_max. | 15 | 0.3073 |
| `pwv` | Value not computed because 183.3 +/- 1 GHz sky brightness... | 15 | 0.3073 |
| `pwv_error` | Value not computed because 183.3 +/- 1 GHz sky brightness... | 15 | 0.3073 |
| `tbsky3` | Value is greater than the fail_max. | 14 | 0.2868 |
| `tbsky7` | Value is greater than the fail_max. | 6 | 0.1229 |
| `tbsky14` | Value is greater than the fail_max. | 6 | 0.1229 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("nsagvrC1.c1", "20060928", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are named qc_'fieldname' with values 0 (within range), 1 (missing), 2 (below min), 4 (above max), 8 (failed delta check); thresholds given in Table 5 (tbsky1/3/7/14: min 3, max 310; temp_hot1/temp_hot2: min 45, max 75; temp_warm: min 10, max 20). Instrument mentor submits a monthly summary report (IMMS). Mentor checks include: filtered brightness temperature time series should be smooth with low noise; brightness temperatures should be greater than 2.75 K and less than ~310 K; external temperature readings should agree with tower measurements within +/- 2 K; difference...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Radar interference from nearby U.S. Air Force radar | Interference spikes appear in the raw/unfiltered brightness temperature time series | A filter is routinely applied to all data; users should use only filtered data (tbsky1, tbsky3, tbsky7, tbsky14) | (hb p. 7) |
| High noise in unfiltered data | Unfiltered variables (tbsky1u, tbsky3u, tbsky7u, tbsky14u) have high noise levels | Should be avoided; use filtered data instead | (hb p. 9) |
| Prototype-era elevated noise (4/12/2004 to 9/1/2006) | Segments of elevated noise due to slowly varying reduction of receiver sensitivity, noticeable during warmer days (surface temperatures greater than  ~255 K) | - | (hb p. 9) |
| Ice water path misinterpreted as liquid water | Presence of ice water path increases brightness temperature observed by the 183.3 ± 14 GHz channel, which would be interpreted as a contribution from liquid clouds | - | (hb p. 8) |
| Nonlinear channel response and saturation near line center | GVR-measured brightness temperatures show nonlinear response to PWV, with saturation of channels close to the 183.31-GHz line center, especially evident in ±1 and ±3 channels | - | (hb p. 8) |
| Calibration sensor error amplification at low sky brightness temperature | A +0.2 K error at the 333 K hot load and -0.2 K error at the 293 K warm load amplifies to a -2.8 K error at a 33 K sky brightness temperature | Temperature sensor accuracy is the most significant source of calibration error (~0.2 K) | (hb p. 9) |
| Calibration revision offset | Revised calibration (verified April 2006) produced a slight (~1 K) increase in brightness temperatures of the ±1 and ±3-GHz channels compared to originally obtained data, slightly improving... | Brightness temperatures used in the reference paper are the ones originally obtained from the instrument; calibration correction can be applied to... | (hb p. 9) |
| Receiver gain drift with temperature | Component plate temperature stability limits receiver-gain rate-of-change to below 100 K/Hr | System gain and offset calibrations performed a few times a minute (mirror cycles to loads every 10 s) to achieve sub-K measurement precision | (hb p. 7) |
| Negligible but nonzero sensitivity to ice scattering | Sensitivity to ice scattering is less than  0.6 K at GVR frequencies for typical winter ice clouds | - | (hb p. 8) |
| Data quality flag triggers | qc_ flags indicate 1 (missing value), 2 (value less than specified minimum), 4 (value greater than specified maximum), 8 (value failed valid delta check) for fields such as tbsky1/3/7/14,... | Check qc_'fieldname' flags against thresholds in Table 5 | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated using a warm (~293 K) and a hot (~333 K) FIRAM-160 absorber, tilted about 10 degrees for better than -60 dB reflectivity (0.999999 emissivity). Brightness temperature computed as Tsky = Twarm + G(Vsky - Vwarm), with gain G = (Thot - Twarm)/(Vhot + Vwarm), Thot = average of temp_hot1 and temp_hot2, and Mylar... (hb p. 8) |
| Calibration interval | Mirror continuously cycles between warm load, hot load, and sky, calibrating the instrument once every 10 seconds. (hb p. 8) |
| Traceability | Operational calibration independently verified in spring 2006 with an external calibration load; larger insulated hot-load convection chamber built with higher precision temperature meter and sensors calibrated with a NIST-traceable voltmeter and temperature probe with 0.05 K absolute accuracy. Measured absolute error... (hb p. 8) |
| Routine maintenance | Not available (hb p. 10) |
| Maintenance interval | Not available (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MWR (two-channel microwave radiometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Uncertainty` | The range of probable maximum deviation of a measured value from the true value within a... |
| `PWV` | Precipitable water vapor |
| `NEDT` | Noise Equivalent Delta-T |
| `IMMS` | Instrument mentor monthly summary report |
| `MWR` | Microwave radiometer (two-channel) |


### References the handbook cites

- Cadeddu, MP, DD Turner, and JC Liljegren. 2009. "A Neural Network for Real-Time Retrievals of PWV and LWP From Arctic Millimeter-Wave Ground-Based Observations." IEEE Transactions on Geoscience and Remote Sensing 47(7):...
- Pazmany, AL. 2007. "A compact 183 GHz radiometer for water vapor and liquid sensing." IEEE Transactions on Geoscience and Remote Sensing 45(7): 2202-2207.
- Cadeddu, MP, JC Liljegren, and AL Pazmany. 2007. "Measurements and retrievals from a new 183-GHz water-vapor radiometer in the arctic." IEEE Transactions on Geoscience and Remote Sensing 45(7): 2207-2215.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/gvr_handbook.pdf (17 pages, DOE/SC-ARM/TR-076, by MP Cadeddu)
- Catalog record: ARM data-source index, `instrument_class_code=gvr`, read 2026-09-23
- Example file: `nsagvrC1.c1.20240703.000011.nc` from `nsagvrC1.c1`, 0.64 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
