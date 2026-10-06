---
name: arm-instrument-mwrhf
description: ARM Microwave Radiometer - High Frequency (mwrhf) - handbook-derived instrument reference. Measurement principle, reported quantities (temp - ambient temperature, pressure), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmwrhfC1.b1) and the variable inventory of a real file. Use when working with mwrhf data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - mwrhf, Microwave Radiometer - High Frequency, sgpmwrhfC1.b1, Radiometric, Radiometer Physics, GmbH, Uncertainty, TndI, Tndmed.
---

# MWRHF - Microwave Radiometer - High Frequency

The MWRHF (90/150-GHz Vapor Radiometer) measures time-series sky brightness temperatures at 90 and 150 GHz, sensitive to cloud liquid water and precipitable water vapor, deployed at fixed and mobile ARM sites such as SGP/C1 and AMF1.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mwrhf` |
| Handbook | [DOE/SC-ARM-TR-080 / MP Cadeddu / March 2011](https://www.arm.gov/publications/tech_reports/handbooks/mwrhf_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Radiometer Physics, GmbH; RF section: Radiometer RPG-150-90 |
| Primary measurements | Microwave narrowband brightness temperature |
| Record | 2006-11-03 to 2024-02-14 (retired) |
| Datastreams with data | 31 across 12 sites |
| Sites | asi, cor, epc, fkb, grw, hfe, hou, mao, nsa, pgh, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/mwrhf |


## Credit

Everything this skill knows about the instrument is the work of **MP Cadeddu** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MP Cadeddu. *Microwave Radiometer – High Frequency (MWRHF) Handbook*, DOE/SC-ARM-TR-080, March 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mwrhf_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The MWRHF measures sky radiances at two frequencies, 90 and 150 GHz, located in the window region of the microwave spectrum, and converts these radiances to equivalent brightness temperatures through a calibration procedure. An off-axis paraboloid mirror focuses microwave radiation onto a corrugated feed horn, and a wire-grid beam splitter decomposes the incoming radiation into two beams, each directed to a feed horn producing a beam of ~3° HPBW. A Dicke Switch periodically switches each receiver input to an internal black body of known brightness temperature to continuously determine system noise temperature. The receivers use direct detection: the signal is amplified (40-dB LNA, then 20-dB amplifier), filtered, and detected/integrated simultaneously for both channels. Since cloud liquid water contribution to the microwave signal increases roughly with the square of frequency, the window regions above 90 GHz are more sensitive to cloud liquid than the region below 45 GHz, and combining MWRHF with lower-frequency MWR channels (23.8/31 GHz) can reduce retrieved liquid water path RMSE by about 50%.

**Siting.** The instrument located at the SGP does not have the noise diode after the Dicke switch and relies on the Dicke switch for calibration, unlike other deployments; deployment locations include SGP/C1 and AMF1 (mobile facility, e.g. GRW, FKB).

**Sampling.** native rate 1 s integration time at each frequency (greater than =1 s per specifications) (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Tbsky90 - 90 GHz sky brightness temperature | K | - | 1 K | - | (hb p. 7) |
| Tbsky150 - 150 GHz sky brightness temperature (filtered) | K | - | 1 K | - | (hb p. 7) |
| tnd90med - 90 GHz median noise diode temperature from tip... | K | - | 5 K | - | (hb p. 7) |
| tnd150med - 150 GHz median noise diode temperature from tip... | K | - | 5 K | - | (hb p. 7) |
| tnd90i - 90 GHz instantaneous noise diode temperature from... | K | - | 1.5 K | - | (hb p. 7) |
| tnd150i - 150 GHz instantaneous noise diode temperature... | K | - | 2.5 K | - | (hb p. 7) |
| temp - ambient temperature | C | - | 0.5 | - | (hb p. 7) |
| pressure | KPa | - | 2 | - | (hb p. 7) |
| rh - relative humidity | % | - | 5 | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Receiver noise temperature 90 GHz | less than  750 K | (hb p. 12) |
| Receiver noise temperature 150 GHz | less than  1650 K | (hb p. 12) |
| Channel bandwidth | 2000 MHz | (hb p. 12) |
| Absolute system stability | 1 K | (hb p. 12) |
| Radiometric resolution | 0.2-0.4 K RMS@1 s integration time | (hb p. 12) |
| Receiver and antenna thermal stabilization | less than  0.05 K | (hb p. 12) |
| Integration time | greater than =1 s | (hb p. 12) |
| HPBW 90-GHz channel | 1.8° | (hb p. 12) |
| HPBW 150-GHz channel | 1.5° | (hb p. 12) |
| Temperature range | -30 to +45 C (Environmental Chamber tested) | (hb p. 12) |
| Power consumption | less than  150 W, Max 350 W without dew blower | (hb p. 12) |


## The data

Verified example: **`sgpmwrhfC1.b1`**, file `sgpmwrhfC1.b1.20131123.000000.cdf`
(5.47 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=56876 |
| Data variables | 25 |
| QC variables | 10 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2013-11-23T00:00:00 to 2013-11-23T23:59:57 |
| sampling interval | 2 seconds |
| averaging interval | not averaged |
| dod version | mwrhf-b1-2.1 |
| process version | ingest-mwrhf-3.1-0.el5 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `surface_pressure` | kPa | time | yes | Ambient surface pressure |
| `surface_relative_humidity` | % | time | yes | Ambient surface relative humidity |
| `surface_temperature` | degC | time | yes | Ambient surface temperature |
| `tbsky150` | K | time | yes | Sky brightness temperature (150 GHz) |
| `tbsky90` | K | time | yes | Sky brightness temperature (90 GHz) |
| `time` | - | time | yes | Time offset from midnight |
| `tnd150i` | K | time | yes | 150 GHz last instantaneous noise diode temperature from tip curves |
| `tnd150med` | K | time | yes | 150 GHz median noise diode temperature from tip curves |
| `tnd90i` | K | time | yes | 90 GHz last instantaneous noise diode temperature from tip curves |
| `tnd90med` | K | time | yes | 90 GHz median noise diode temperature from tip curves |
| `surface_rain_flag` | None | time | - | Rain flag |


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
                     params={"user": f"{user}:{token}", "ds": "sgpmwrhfC1.b1",
                             "start": "2013-11-23", "end": "2013-11-23", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmwrhfC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmwrhfC1.b1", "2013-11-23", "2013-11-23")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmwrhfC1.b1", "2013-11-23", "2013-11-23"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("tbsky90", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

10 `qc_` companion variables cover 9 of the
25 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_tbsky90"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("tbsky90", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["tbsky90", "tbsky150", "tnd90med"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpmwrhfC1.b1", "20061103", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags are named qc_'fieldname' (e.g., qc_tbsky90) with possible values 0 (within range), 1 (missing), 2 (below minimum), 4 (above maximum), 8 (failed valid delta check); thresholds given in Table 5. The instrument mentor submits a monthly summary report (IMMS) and performs checks including smoothness/noise of brightness temperature time series, physical bounds (2.75-310 K), agreement with tower temp/pressure/rh within specified tolerances, and comparison with model computations. Daily quality checks and site scientist/DQ office assessments are available via the DQHands system...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Calibration algorithm rewritten from vendor software | Calibrated brightness temperatures produced with ARM's own algorithm, not vendor software, so results may differ from vendor-processed data; effective for SGP data starting September 2008... | Description of the calibration algorithm is provided in the handbook; users should be aware which calibration version applies to which time period | (hb p. 9) |
| Tip curve quality threshold | A tip curve is only considered good (used for calibration update) if the correlation coefficient of the regression exceeds 0.999; poor tip curves are effectively rejected | Software checks correlation threshold of 0.999 before accepting new TndI value; if not found, gain calibration continues using old Tndmed | (hb p. 9) |
| Instantaneous TndI variability/noise | Instantaneous TndI values (from individual tip curves) show scatter (e.g., standard deviation ~5 K at 90 GHz and ~8 K at 150 GHz) and are not directly usable in calibration due to... | A circular array of 50 (or more) points is maintained and the median value (Tndmed) is used instead of instantaneous values | (hb p. 9) |
| Calibration error budget / drift | Estimated uncertainty in slope of tip-curve regression (~0.002) propagates to ~0.4 K error in Tsky, ~1.5 K uncertainty in TndI, and ~1 K calibration uncertainty in Tsky at both frequencies;... | Routine hourly tip curves and running median approach account for gradual drift in noise diode injection temperature | (hb p. 10) |
| SGP unit lacks noise diode after Dicke switch | SGP instrument relies solely on Dicke switch for calibration rather than a noise diode, a configuration difference from other units that could affect calibration behavior/comparability... | - | (hb p. 6) |
| Data quality flag thresholds | qc_ flags indicate missing values (1), values below minimum (2), above maximum (4), or failed delta check (8) for fields such as Tbsky90 (0-310 K), Tbsky150 (0-310 K), pressure (80-110... | Use qc_ fields to filter/flag data outside specified min/max ranges | (hb p. 8) |
| Brightness temperature physical bounds check | Mentor checks that brightness temperatures should be greater than 2.75 K and less than approximately 310 K; deviations indicate instrument or calibration problems | Instrument mentor performs this check as part of monthly review | (hb p. 10) |
| Ancillary sensor agreement with tower measurements | External temperature, pressure, and relative humidity readings may disagree with tower measurements beyond expected tolerances (+/- 2 K, +/- 5 KPa, +/- 5% respectively) | Mentor compares external temp/pressure/rh readings to tower measurements as a data quality check | (hb p. 10) |
| Model comparison discrepancy | Measured brightness temperatures compared with model computations; discrepancies indicate potential calibration or instrument issues (illustrated in Figure 1 comparison, N=197 points) | Used as a general quality check by instrument mentor | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Absolute calibration using two calibration targets (occasionally a cryogenic/LN2 reference target); routine calibration relies on hourly tip curves and gain calibrations every 5 minutes using the radiometer equation Tsky = Tbb + (Vsky-Vbb)/G, with gain G and noise diode temperature Tnd determined from black body and... (hb p. 8) |
| Calibration interval | Tip curves collected hourly; gain calibrations every 5 minutes; LN2 calibrations performed at start of new deployment or after out-of-service/move, and additional LN2 calibrations as necessary (hb p. 8) |
| Traceability | Liquid nitrogen (cryogenic) reference target calibration used to determine equivalent noise diode temperature (hb p. 8) |
| Routine maintenance | Routine and corrective maintenance documentation available at the site operation web pages (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MWR (microwave dual-channel radiometer, 23.8 and 31 GHz).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Uncertainty` | The range of probable maximum deviation of a measured value from the true value within a... |
| `Tnd` | Noise diode injection temperature, determined via Tnd = [(Tsky - Tbb)/(Vsky - Vbb)] *... |
| `TndI` | Instantaneous value of Tnd derived from a single tip curve measurement. |
| `Tndmed` | Median value of the circular array of TndI values (50 or more points), used as the... |


### References the handbook cites

- RPG-150-90 High Sensitivity LWP radiometers-Operating Manual, by T. Rose and H. Czekala.
- T Rose, S Crewell, U Lonhert, and C Simmer. 2005. "A network suitable microwave radiometer for operational monitoring of the cloudy atmosphere." Atmospheric Research 75: 183–200.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mwrhf_handbook.pdf (20 pages, DOE/SC-ARM-TR-080, by MP Cadeddu)
- Catalog record: ARM data-source index, `instrument_class_code=mwrhf`, read 2026-09-23
- Example file: `sgpmwrhfC1.b1.20131123.000000.cdf` from `sgpmwrhfC1.b1`, 5.47 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
