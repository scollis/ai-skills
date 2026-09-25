---
name: arm-instrument-nfov
description: ARM Narrow Field of View Zenith Radiometer (nfov) - handbook-derived instrument reference. Measurement principle, reported quantities (Zenith radiance at 673 nm, Zenith radiance at 870 nm), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpnfovC1.b1) and the variable inventory of a real file. Use when working with nfov data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties; Radiometric. Triggers - nfov, Narrow Field of View Zenith Radiometer, sgpnfovC1.b1, Zenith radiance at 673 nm, Zenith radiance at 870 nm, Cloud Properties, Radiometric, NFOV, NFOV2, REDvsNIR, DISORT.
---

# NFOV - Narrow Field of View Zenith Radiometer

The NFOV/NFOV2 is a ground-based, zenith-pointing radiometer with a narrow field of view that measures downwelling zenith spectral radiance (870 nm for NFOV; 673 and 870 nm for NFOV2) at 1-second time resolution, used to retrieve overhead cloud optical depth and, for NFOV2, effective cloud fraction.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 12 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nfov` |
| Handbook | [DOE/SC-ARM/TR-060 / C. Chiu, A. Marshak, G. Hodges, J.C. Barnard, J. Schmelzer / November 2008](https://www.arm.gov/publications/tech_reports/handbooks/nfov_handbook.pdf) |
| Measurement category | Cloud Properties; Radiometric |
| Primary measurements | Shortwave narrowband radiance; Shortwave spectral total downwelling irradiance |
| Record | 2000-03-08 to 2026-09-23 (active) |
| Datastreams with data | 18 across 15 sites |
| Sites | anx, asi, cor, crg, dst, epc, fkb, grw, hfe, hou, mao, pgh, pvc, pye |
| ARM page | https://www.arm.gov/capabilities/instruments/nfov |


## Credit

Everything this skill knows about the instrument is the work of **C. Chiu, A. Marshak, G. Hodges, J.C. Barnard, J. Schmelzer** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> C. Chiu, A. Marshak, G. Hodges, J.C. Barnard, J. Schmelzer. *Narrow Field-of-View Radiometer (NFOV) Handbook*, DOE/SC-ARM/TR-060, November 2008.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/nfov_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The NFOV radiometers point straight up, and a collimating tube restricts the instrument's field of view so that only photons traveling in the correct direction and entering the collimator reach the detector, an interference filter/Silicon diode detector. The head is held at a nearly constant temperature to minimize temperature effects on the measurement, since sensitivity to head temperature is about a 1% change in radiance per 1 K change in head temperature. Raw detector counts are converted to zenith radiance via a linear calibration relationship I = aV + b, where a is the calibration factor and b is an offset derived from nighttime measurements. For NFOV2, the two channels (673 nm RED and 870 nm NIR) exploit the fact that clouds have nearly identical optical properties at both wavelengths while vegetated surfaces reflect very differently, enabling the REDvsNIR method (using a DISORT-based lookup table) to retrieve cloud optical depth and effective cloud fraction even for broken-cloud (3D) sky conditions, which a single-channel monochromatic radiance measurement cannot unambiguously resolve.

**Siting.** The instrument points straight up (zenith-viewing). The NFOV2 field of view was initially 5.7 deg (same as NFOV) when deployed at SGP, but was reduced to 1.2 deg because incorrect cloud optical depths were retrieved when the FOV was filled with both clouds and clear sky; the 1.2 deg FOV also matches the fields of view of the ACRF shortwave spectrometer and the NASA AERONET sun photometers. Deployments include ACRF Southern Great Plains (SGP, from September 2004), and with the ARM Mobile Facility (AMF) at Point Reyes, California (June-September 2005), the Black Forest, Germany (2007), and China (for aerosol indirect effects study).

**Sampling.** native rate 1 Hz (sampling rate of 1 second); reported every 1 second (hb p. 3).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Zenith radiance at 673 nm | Wm-2sr-1nm-1 | - | - | - | (hb p. 5) |
| Zenith radiance at 870 nm | Wm-2sr-1nm-1 | - | - | - | (hb p. 5) |


## Specifications

| parameter | value | source |
|---|---|---|
| Radiometer types | NFOV: 1-channel narrow field-of-view radiometer with a filter 870 nm; NFOV2: 2-channel narrow field-of-view radiometer with filters 673 and 870 nm | (hb p. 8) |
| Components | NFOV comprised of a MFRSR head and a collimator that sits atop the head; the collimator restricts the field of view | (hb p. 9) |
| FOV | NFOV: 5.7 deg; NFOV2: 5.7 deg and 1.2 deg prior to and after 2004, respectively | (hb p. 9) |
| Bandwidth | 10 nm at full width at half maximum (response function data) | (hb p. 9) |
| Detector | Silicon diode detector | (hb p. 9) |
| Sampling rate | 1 Hz (one-second sampling time resolution) | (hb p. 3) |
| Head temperature output (Campbell logger column 8) | in mV, this value should be around 1450 | (hb p. 9) |
| Tube temperature output (Campbell logger column 9) | in mV, this value should be around 1400 | (hb p. 9) |


## The data

Verified example: **`sgpnfovC1.b1`**, file `sgpnfovC1.b1.20070611.181317.cdf`
(1.84 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=20803, `numfields`=6 |
| Data variables | 21 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2007-06-11T18:13:17 to 2007-06-11T23:59:59 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ambient_temp` | degC | time | yes | Ambient Temperature |
| `cosine_solar_zenith_angle` | unitless | time | yes | Cosine Solar Zenith Angle |
| `head_temp` | degC | time | yes | Detector Temperature |
| `radiance` | W/m2/nm/sr | time | yes | Calibrated Zenith Radiance |
| `radiance_temp_cor` | W/m2/nm/sr | time | yes | Calibrated zenith radiance data corrected for changes in head... |
| `raw_counts` | counts | time | yes | Raw counts from instrument before calibration |
| `time` | - | time | yes | Time offset from midnight |
| `tube_temp` | degC | time | yes | Tube Temperature |
| `callang_flags` | unitless | time,numfields | - | Fields flagged by callang |


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
                     params={"user": f"{user}:{token}", "ds": "sgpnfovC1.b1",
                             "start": "2007-06-11", "end": "2007-06-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpnfovC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpnfovC1.b1", "2007-06-11", "2007-06-11")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpnfovC1.b1", "2007-06-11", "2007-06-11"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("radiance", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

8 `qc_` companion variables cover 7 of the
21 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_raw_counts"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("raw_counts", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["raw_counts", "radiance", "head_temp"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpnfovC1.b1.20070611.181317.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `radiance_temp_cor` | Value is less than the fail_min. | 20803 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpnfovC1.b1", "20000308", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Calibrations are performed to produce a calibration factor converting raw detector counts to zenith radiance; values of a and b are stored in the data file header. Data quality is monitored via DQ HandS (Data Quality Health and Status) and NCVweb for interactive data plotting, using techniques employed by ARM's data quality analysts, instrument mentors, and site scientists. Section 6.2 (Data Reviews by Instrument Mentor) states "This section is not applicable to this instrument." All DQ Office and most Site Scientist checking techniques have been incorporated within DQ HandS. Redundant...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Non-unique relationship between zenith radiance and cloud optical depth (1D... | For a single-channel (monochromatic) radiometer, the same observed radiance value corresponds to multiple possible optical depth values in DISORT-calculated curves, making optical depth... | Use two-channel NFOV2 with REDvsNIR retrieval method instead of single-channel NFOV | (hb p. 4) |
| 3D radiative transfer effects exceeding 1D model bounds | Histogram of actual NFOV observations shows some radiance values exceeding those permitted by 1D DISORT models, so cloud optical depth is irretrievable for those zenith radiances | None specific stated for single-channel NFOV; addressed partly by NFOV2's broken-cloud-capable REDvsNIR method | (hb p. 4) |
| Clear-sky contamination when FOV filled with both cloud and clear sky | Incorrect (biased) cloud optical depth retrievals when the wide 5.7 deg FOV captured a mixed cloud/clear-sky scene | FOV was reduced from 5.7 deg to 1.2 deg to lower the amount of clear-sky contamination | (hb p. 4) |
| Head temperature sensitivity | About a 1% change in radiance for every 1 K change in head temperature | Head is kept at a constant temperature (insofar as possible) using a head/tube heater controller to prevent temperature effects from influencing... | (hb p. 7) |
| Lens contamination (raindrops, sea salt, dust, bird droppings) | Inaccurate/inconsistent radiance measurements relative to calibration performed with a clean lens | Use linear combinations of calibration factors obtained from pre- and post-experiment calibrations, or use redundant measurements of the AMF sun... | (hb p. 5) |
| Instrument damage/decommissioning (single-channel NFOV) | Data gap/discontinuity: NFOV was damaged during a storm in June 2002 and was decommissioned in June 2007 | Replaced operationally by the two-channel NFOV2 | (hb p. 4) |
| FOV change over instrument history affecting comparability | NFOV2 FOV was 5.7 deg prior to 2004 and 1.2 deg after 2004, so data collected before and after this change are not directly comparable in terms of clear-sky contamination susceptibility | Be aware of the FOV change date (2004) when comparing datasets across time | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration factor derived from linear regression between NFOV2 signals and radiances of a calibrated integrating sphere; dark counts and signals for 4, 8, 12, and 16 lamps of the sphere are measured; final zenith radiance I = aV + b, where a is the calibration factor, b is the offset based on nighttime measurements,... (hb p. 7) |
| Calibration interval | Sphere calibrated several times a year (hb p. 7) |
| Traceability | Calibrated at the NASA Goddard Space Flight Center Calibration Facility using the 36-inch integrating Teflon sphere, calibrated using a spectroradiometer and a secondary lamp standard; same sphere used to calibrate all sun photometers of the NASA AERONET; uncertainties in radiances of the sphere at 673 and 870 nm are... (hb p. 7) |
| Routine maintenance | This section is under development (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: radars, lidars, microwave radiometers, ACRF shortwave spectrometer, NASA AERONET sun photometers.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `NFOV` | One-channel narrow field-of-view radiometer with a filter at 870 nm |
| `NFOV2` | Two-channel narrow field-of-view radiometer with filters at 673 nm (RED) and 870 nm (NIR) |
| `FOV` | Field of view |
| `SZA` | Solar zenith angle |
| `REDvsNIR` | Retrieval method using normalized zenith radiances at RED (673 nm) and NIR (870 nm)... |
| `DISORT` | Discrete-Ordinate-method radiative transfer model |
| `AMF` | ARM Mobile Facility |
| `ACRF` | ARM Climate Research Facility |
| `AERONET` | NASA Aerosol Robotic Network |
| `VAP` | Value-added product |
| `QME` | Quality Measurement Experiment |
| `COPS` | Convective and Orographically-induced Precipitation Study |


### References the handbook cites

- Chiu, JC, A Marshak, Y Knyazikhin, WJ Wiscombe, HW Barker, JC Barnard, and Y Luo. 2006. "Remote sensing of cloud properties using ground-based measurements of zenith radiance." Journal of Geophysical Research 111:...
- Marshak, A, Y Knyazikhin, KD Evans, and WJ Wiscombe. 2004. "The 'RED versus NIR' plane to retrieve broken-cloud optical depth from ground-based measurements, cloud-vegetation interaction: Use of normalized difference...
- Stamnes, K, S-C Tsay, WJ Wiscombe, and K Jayaweera. 1988. "Numerically stable algorithm for discrete-ordinate-method radiative transfer in multiple scattering and emitting layered media." Applied Optics 27: 2502-2512.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/nfov_handbook.pdf (12 pages, DOE/SC-ARM/TR-060, by C. Chiu, A. Marshak, G. Hodges, J.C. Barnard, J. Schmelzer)
- Catalog record: ARM data-source index, `instrument_class_code=nfov`, read 2026-09-23
- Example file: `sgpnfovC1.b1.20070611.181317.cdf` from `sgpnfovC1.b1`, 1.84 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
