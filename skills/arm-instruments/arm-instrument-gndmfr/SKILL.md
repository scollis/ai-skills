---
name: arm-instrument-gndmfr
description: ARM Ground Multifilter Radiometer (gndmfr) - handbook-derived instrument reference. Measurement principle, reported quantities (Direct beam irradiance, Measurement voltage output), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (shbgndmfrC1.b1) and the variable inventory of a real file. Use when working with gndmfr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric; Surface/Subsurface Properties. Triggers - gndmfr, Ground Multifilter Radiometer, shbgndmfrC1.b1, Direct beam irradiance, Measurement voltage output, Radiometric, Surface/Subsurface Properties, Yankee Environmental Systems, Inc. MFRSR head (used for MFR), MFRSR, NIMFR, cordif, cordirhor.
---

# GNDMFR - Ground Multifilter Radiometer

The Multifilter Radiometer (MFR), a derivative of the MFRSR consisting of an MFRSR head mounted on a tower and pointed at the surface, measures upwelling (reflected) irradiance at six narrowband channels (415, 500, 615, 673, 870, 940 nm) and one broadband channel, deployed at ARM tower sites to characterize surface reflected radiation.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `gndmfr` |
| Handbook | [DOE/SC-ARM-TR-144 / GB Hodges, JJ Michalsky / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf) |
| Measurement category | Radiometric; Surface/Subsurface Properties |
| Manufacturer / model | Yankee Environmental Systems, Inc. MFRSR head (used for MFR); Campbell Scientific CR1000 data logger |
| Primary measurements |  |
| Record | 1997-10-26 to 1998-09-30 (retired) |
| Datastreams with data | 3 across 1 sites |
| Sites | shb |
| ARM page | https://www.arm.gov/capabilities/instruments/gndmfr |


## Credit

Everything this skill knows about the instrument is the work of **GB Hodges, JJ Michalsky** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> GB Hodges, JJ Michalsky. *Multifilter Rotating Shadowband Radiometer Instrument Handbook, With subsections for derivative instruments: Multifilter Radiometer (MFR), Normal Incidence Multifilter Radiometer (NIMFR)*, DOE/SC-ARM-TR-144, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `mfrsr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `gndmfr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The instrument (MFRSR/MFR) is a passive radiometer measuring solar energy in six narrowband channels and one broadband channel; for the ground-viewing MFR configuration it is simply the MFRSR head mounted on a tower and pointed at the surface to measure reflected irradiance at the same nominal wavelengths as the MFRSR. In the standard MFRSR configuration, four measurements are taken per sample cycle using a rotating shadowband: an unblocked (nadir/home) measurement, two side-band measurements (used to correct for sky obscured by the shadowband), and a sun-blocked measurement, from which global, diffuse, and calculated direct-beam irradiance are derived. Corrections applied include a cosine correction (for angular response, determined on a laboratory cosine bench), a diffuse correction (modeled using a Rayleigh sky with input from the cosine response file), and an offset correction (derived from averaged nighttime data). For the MFR mounted on a tower viewing the surface, the same internal electronics and sensors are used, in some cases housed in custom insulated enclosures for tower or aircraft mounting.

**Siting.** The instrument should be mounted on a stable post or platform with as few obstructions as possible; ideally no site obstructions cast a shadow over the instrument at any time of day. It must be mounted with the motor toward the Equator and aligned north-south, with the shadowband motor angle set to the local latitude so the ephemeris calculation works properly; the shadowband must be adjusted, ideally at solar noon, so it shades the diffuser squarely at the sun-blocked stop. For the MFR derivative, the head is mounted on a tower pointed at the surface (e.g., at 25-meter and 10-meter levels of towers at SGP, or in custom housings at NSA Barrow and other Arctic/Azores sites, or on a Cessna...

**Sampling.** native rate sampling intervals started at 20-second intervals; shadowband moves to a new position only every five or six sampling intervals; averaging nighttime data averaged to produce offset correction for the following day (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Global/diffuse/reflected irradiance (narrowband channels) | - | - | - | - | (hb p. 7) |
| Direct beam irradiance (calculated) | - | - | - | - | (hb p. 7) |
| Measurement voltage output | millivolts | ± 250 millivolts | 0.06% of 250 millivolts, i.e., 0.15 millivolts | - | (hb p. 14) |


## The data

Verified example: **`shbgndmfrC1.b1`**, file `shbgndmfrC1.b1.19980927.000000.cdf`
(1.4 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4319, `channel`=6 |
| Data variables | 13 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 1998-09-27T00:00:00 to 1998-09-27T23:59:39 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `callang_flags` | None | time | - | Fields flagged by callang: 0 = no flag 1 = 2 = 3 = 4 = Night time 5 = |
| `cosine_solar_zenith_angle` | None | time | - | Cosine of Solar Zenith Angle |
| `logger_volt` | volts | time | - | Data Logger Supply Voltage |
| `mfr_temp` | deg C | time | - | Detector Temperature |
| `raw_file` | None | time | - | Source of raw data values for time step |
| `time` | - | time | - | Time offset from base_time |
| `up_hemisp_broadband` | Counts | time | - | Broadband Upwelling Hemispheric Irradiance, Uncalibrated Silicon... |
| `up_hemisp_narrowband` | W/m^2/nm | time,channel | - | Upwelling Hemispheric Irradiance, GNDMFR |


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
                     params={"user": f"{user}:{token}", "ds": "shbgndmfrC1.b1",
                             "start": "1998-09-27", "end": "1998-09-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./shbgndmfrC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "shbgndmfrC1.b1", "1998-09-27", "1998-09-27")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("shbgndmfrC1.b1", "1998-09-27", "1998-09-27"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("up_hemisp_broadband")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

1 `qc_` companion variables cover 0 of the
13 data variables. Assessments present in the example file: .

`cleanup_qc=True` on read normalises what QC there is; `qc_info` is not a per-variable
companion, so `qcfilter`'s variable-keyed methods do not apply here. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# This file carries one QC variable, `qc_info`, not a per-variable `qc_<name>`
# companion - so the qcfilter methods that key off that naming have nothing to
# match. Read it directly and work out the encoding from its own attributes.
print(ds["qc_info"].attrs)
print(ds["qc_info"].to_series().value_counts().head())
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("shbgndmfrC1.b1", "19971026", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality is monitored via the ARM Data Quality Health and Status (DQ HandS) system at http://dq.arm.gov/, which contains tables and graphs with techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality. Near-real-time data plots are available via the DQ HandS plot browser. An Instrument Mentor Monthly Summary is also produced.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Shading issue from coarse shadowband stepping | Anomalous or offset diffuse/direct/total irradiance values in morning or afternoon when shadowband is adjusted right before or after a step, due to 0.45-degree half-step increments causing... | Use finer stepping (e.g., 0.225-degree one-eighth steps) with the new Campbell motor controller to reduce the issue; consult careful adjustment... | (hb p. 8) |
| Electromagnetic frequency interference from bang-on/bang-off heater (older loggers) | Saw-tooth trace of head temperature; potential interference with irradiance measurements during heater on/off transitions | Original logger gives irradiance measurements priority and stops heater during a measurement; new proportional heater controller eliminates the... | (hb p. 13) |
| 940 nm channel cannot be Langley-calibrated | 940 nm channel calibration relies only on lamp (nominal) calibration rather than higher-accuracy Langley calibration, due to highly variable atmospheric water vapor | Each head is returned annually to the SGP calibration facility for lamp calibration | (hb p. 19) |
| Lamp calibration less accurate than Langley calibration | .b1 (lamp-calibrated) data show greater uncertainty than .c1 (Langley-calibrated) data | Use Langley-calibrated .c1 data once available; lamp calibration serves as nominal/backup estimate | (hb p. 18) |
| Sensor offset bias | Inherent bias in each sensor affecting total and diffuse irradiance measurements if uncorrected | Nighttime data averaged to compute an ongoing offset correction for the following day rather than relying on a single lamp-calibration-derived value;... | (hb p. 17) |
| Cosine response error | Instrument response varies with solar zenith/azimuth angle rather than following a true cosine law | Cosine correction determined in the laboratory using a cosine bench across ±90° in south-north and west-east directions to build a correction file | (hb p. 16) |
| Diffuse correction approximation | Diffuse irradiance correction based on modeled isotropic/Rayleigh sky, not actual instantaneous sky conditions | Handbook states isotropic sky assumption is within one percent of actual conditions and the diffuse correction is small enough not to warrant... | (hb p. 17) |
| Site obstructions casting shadows | Anomalous drops or artifacts in irradiance data at certain times of day due to trees, buildings, or other obstructions | Site should ideally have no obstructions that cast a shadow over the instrument at any time during the day; compromise siting often required | (hb p. 12) |
| SGP network degradation / missing instruments | Historical data gaps at SGP extended facilities where MFRSR was intended but not operational due to lack of spares/parts | Network was refurbished and restored to full capacity by end of 2008 | (hb p. 7) |
| Station decommissioning affecting record continuity | Discontinuities in the deployment history/datastream when SGP extended facilities were shut down in 2009-2010, particularly those farthest from the Central Facility | Closed stations were planned to be re-established at locations closer to the CF, though with different site names | (hb p. 9) |
| NIMFR shading issues avoided but other cons present | NIMFR (sun-tracking derivative) does not exhibit shading issues common to MFRSR/MFR, but does not provide total or diffuse irradiance and requires solar tracker | N/A - noted as inherent trade-off of NIMFR design | (hb p. 19) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Standard lamp calibration, cosine response determination, and mapping of the spectral response function (filter function) performed at the SGP calibration facility before deployment; Langley calibration performed once deployed in the field with sufficient data collected (except for the 940 nm channel, which cannot be... (hb p. 18) |
| Calibration interval | Each head is returned to the SGP calibration facility annually for lamp calibration (and cosine/spectral bench runs) (hb p. 18) |
| Traceability | Nominal (lamp) calibration data are found in .b1 data files; Langley-calibrated data are contained in .c1 data files (hb p. 18) |
| Routine maintenance | Cleaning the Spectralon diffuser; checking and replacing desiccant (in heads with desiccant holders) as necessary (hb p. 19) |
| Maintenance interval | Diffuser cleaned from once daily to once every two weeks depending on site location; desiccant checked monthly (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR (Multifilter Rotating Shadowband Radiometer), NIMFR (Normal Incidence Multifilter Radiometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `MFRSR` | Multifilter Rotating Shadowband Radiometer |
| `MFR` | Multifilter Radiometer |
| `NIMFR` | Normal Incidence Multifilter Radiometer |
| `blk` | sun-blocked measurement |
| `cordif` | cosine-corrected diffuse measurement |
| `cordirhor` | cosine-corrected direct horizontal |
| `corth` | corrected total horizontal calculated using cordirhor and cordif |
| `dif` | sideband-corrected sun-blocked measurement |
| `dirhor` | vertical component of the direct beam on a horizontal surface |
| `fsb` | first side-band |
| `ssb` | second side-band |
| `th` | total horizontal |
| `CF` | Central Facility |
| `SGP` | Southern Great Plains |


### References the handbook cites

- Harrison, L, J Michalsky, and J Berndt. 1994. "Automated multifilter rotating shadow-band radiometer: An instrument for optical depth and radiation measurements." Applied Optics 33(22):5118-5125,...
- Harrison, L, and J Michalsky. 1994. "Objective algorithms for the retrieval of optical depths from ground-based measurements." Applied Optics 33(22):5126-5132, doi:10.1364/AO.33.005126.
- Michalsky, JJ, JC Liljegren, and LC Harrison. 1995. "A comparison of sun photometer derivations of total column water vapor and ozone to standard measures of same at the Southern Great Plains Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mfrsr_handbook.pdf (21 pages, DOE/SC-ARM-TR-144, by GB Hodges, JJ Michalsky)
- Catalog record: ARM data-source index, `instrument_class_code=gndmfr`, read 2026-09-23
- Example file: `shbgndmfrC1.b1.19980927.000000.cdf` from `shbgndmfrC1.b1`, 1.4 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
