---
name: arm-instrument-cip-air
description: ARM Cloud Imaging Probe aboard aircraft (cip-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Number Concentration, Area Concentration, Volume Concentration), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaafcipF1.b1) and the variable inventory of a real file. Use when working with cip-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Cloud Properties. Triggers - cip-air, Cloud Imaging Probe aboard aircraft, enaaafcipF1.b1, Number Concentration, Area Concentration, Volume Concentration, Airborne Observations, Cloud Properties, Droplet Measurement Technologies (DMT), Cloud, CAPS, 2DS-AIR, DPOL, PADS.
---

# CIP-AIR - Cloud Imaging Probe aboard aircraft

The cloud imaging probe (CIP), part of the aircraft-mounted Cloud, Aerosol, and Precipitation Spectrometer (CAPS), uses shadow images from a linear photo-detector array to measure the size, shape, and concentration of larger cloud/aerosol particles and hydrometeors from an aircraft wing pylon.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cip-air` |
| Handbook | [DOE/SC-ARM-TR-246 / L Goldberger / June 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf) |
| Measurement category | Airborne Observations; Cloud Properties |
| Manufacturer / model | Droplet Measurement Technologies (DMT), Cloud, Aerosol, and Precipitation Spectrometer (CAPS) - Cloud Imaging Probe (CIP) component |
| Primary measurements | Cloud particle size distribution |
| Record | 2017-03-08 to 2026-09-23 (retired) |
| Datastreams with data | 4 across 2 sites |
| Sites | cor, ena |
| ARM page | https://www.arm.gov/capabilities/instruments/cip-air |


## Credit

Everything this skill knows about the instrument is the work of **L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Goldberger. *Cloud, Aerosol, and Precipitation Spectrometer Instrument Handbook*, DOE/SC-ARM-TR-246, June 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `cas-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `cip-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The CIP operates by projecting shadow images of particles passing through a collimated 658 nm, 30 mW laser beam onto a linear array of 64 photodetectors with 200-um pitch. The presence of a particle is registered as a change in light level on each diode, with "On" registered when light level decreases below 50%. Particle images are reconstructed from individual "slices," where a slice is the state of the 64-element linear array at a given moment, stored each time interval the particle advances through the beam by a distance equal to the probe's size resolution. The CIP determines particle size based on how many diodes in the array its shadow obscures; particles shadowing an end diode (number one or sixty-four) are rejected from sizing but still generate a 2D image. The probe has Korolev tips installed with a 70mm beam opening to prevent ice shattering.

**Siting.** The CAPS instrument (including CIP) is installed in a wing pylon on the aircraft with access to power controlled from a switch inside the aircraft; probe is controlled via vendor-provided GUI once power is applied. If temperatures reach 0 deg C, anti-ice heaters need to be turned on manually.

**Sampling.** native rate 0.1 to 10 Hz (possible 1d histogram data sampling frequency); reported every 1 Hz (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle, precipitation, and hydrometeor size... | #/CC (concentration), um... | 25 to 1550 µm (reported); 12.5 to 1550... | - | - | (hb p. 11) |
| Number Concentration (CIP) | #/CC | - | up to 500 particles/cm3 for standard tips and... | - | (hb p. 12) |
| Area Concentration (CIP) | um^2/cm^3 | - | - | - | (hb p. 9) |
| Volume Concentration (CIP) | um^3/cm^3 | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| CIP measurement range (Section 5.0) | 12.5 um–1.55 mm (standard) at 1 Hz time resolution | (hb p. 8) |
| CIP reported range (Section 7.2.2) | 25 to 1550 µm | (hb p. 11) |
| CIP sampling frequency capability | 0.1 to 10 Hz (reported at 1 Hz) | (hb p. 11) |
| CIP sample area (diode array) | 10 cm x 1.55 mm | (hb p. 11) |
| CIP airspeed valid range | 10−300 m/s | (hb p. 11) |
| CIP laser | 658 nm, 30 mW, DMT-manufactured laser with Arima Lasers Corporation diode | (hb p. 13) |
| CIP diode array | 200-um pitch, 64-element photo-diode array | (hb p. 14) |
| CIP theoretical size range (Section 9.0) | 12.5 to 1550 μm | (hb p. 14) |
| Korolev tips beam opening | 70mm | (hb p. 11) |
| CIP upper concentration range | up to 500 particles/cm3 for CIP with standard tips and arm width | (hb p. 12) |
| 2D image data storage interval | variable interval, when buffer fills | (hb p. 12) |
| 2D CIP data input voltage/interface | RS-422, High Speed, 4 Mb/sec Baud rate | (hb p. 12) |
| CIP System data input voltage/interface | RS-232 or RS-422, 56.6 kb/sec Baud rate | (hb p. 13) |
| Proper operating range - Temperature | -50–50°C | (hb p. 11) |
| Proper operating range - Humidity | 0–100%, non-condensing | (hb p. 11) |
| Proper operating range - Altitude | 50,000 ft | (hb p. 11) |


## The data

Verified example: **`enaaafcipF1.b1`**, file `enaaafcipF1.b1.20180218.122850.nc`
(9.66 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=15168, `bound`=2, `particle_diameter`=62 |
| Data variables | 31 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2018-02-18T12:28:50 to 2018-02-18T16:41:37 |
| dod version | aafcip-b1-1.0 |
| process version | ingest-aafcipcorr-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `counts` | count | time,particle_diameter | yes | Particle counts |
| `diode_1` | V | time | yes | Diode 1 voltage |
| `diode_32` | V | time | yes | Diode 32 voltage |
| `diode_64` | V | time | yes | Diode 64 voltage |
| `laser_current` | mA | time | yes | Laser current through the CIP’s laser diode |
| `laser_power` | V | time | yes | Relative laser power as measured by the onboard laser power monitor |
| `lwc_hw` | g/m^3 | time | - | Liquid water content hotwire |
| `lwc_slave_volt` | V | time | - | Voltage used by the end sections or “slaves” of the liquid water... |
| `lwc_volt` | V | time | - | Voltage required to maintain the liquid water content hotwire’s fixed... |
| `p_pitot` | 1 | time | - | Pitot pressure raw measurement counts |
| `p_static` | 1 | time | - | Static pressure raw measurement counts |
| `particle_diameter` | um | particle_diameter | - | Coordinate variable for particle_diameter |
| `particle_surface_area` | mm^2 | particle_diameter | - | Particle surface area |
| `spare_volt` | V | time | - | Spare voltage |
| `temp_dsp` | degC | time | - | Temperature at the Digital Signal Processing Board |
| `temperature` | degC | time | - | Ambient temperature |
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
                     params={"user": f"{user}:{token}", "ds": "enaaafcipF1.b1",
                             "start": "2018-02-18", "end": "2018-02-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enaaafcipF1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enaaafcipF1.b1", "2018-02-18", "2018-02-18")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enaaafcipF1.b1", "2018-02-18", "2018-02-18"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("p_pitot")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
31 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_diode_1"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("diode_1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["diode_1", "diode_32", "diode_64"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (enaaafcipF1.b1.20180218.122850.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `diode_64` | Value is greater than warn_max. | 14880 | 98.1013 |
| `counts` | diode_64 is outside of warn limits | 15051 | 1.6005 |
| `laser_power` | Value is greater than warn_max. | 238 | 1.5691 |
| `diode_32` | Value is less than warn_min. | 207 | 1.3647 |
| `diode_32` | Value is less than fail_min. | 174 | 1.1472 |
| `diode_64` | Value is less than warn_min. | 171 | 1.1274 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("enaaafcipF1.b1", "20170308", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data Flag and Cloud Flag columns are included in both CAS and CIP ICARTT-format data files (Col 34/35 for CAS; Col 66/67 for CIP). No links to a dedicated Data Quality (DQ) page were found for these data sets; an example DQ plot from the DQ plot browser (from ARM's TCAP campaign) is shown in Figure 3. Calibration/QC results are currently tracked by AAF's director of engineering rather than in a public ARM database.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Large discrepancies between 2DS-AIR and CIP at sizes greater than 150 µm | CIP-reported sizes/concentrations for particles greater than 150 µm diverge noticeably from 2DS-AIR probe measurements | It is recommended one uses the two-dimensional stereo probe aboard aircraft (2DS-AIR) data over the CIP data for particles greater than 150 µm | (hb p. 11) |
| Pre-2019 data processing used aircraft true airspeed rather than CAPS probe's own... | Potential distortion (elongation or squashing) of particle images, leading to under-sizing of droplets, more pronounced at larger particle sizes | For droplets larger than 150 μm, use data from the 2DS-AIR probe for data sets from 2019 and earlier | (hb p. 15) |
| End-diode shadowing rejection | Particles shadowing diode number one or sixty-four are rejected from the sizing routine (excluded from size distribution) although a 2D image is still generated | - | (hb p. 14) |
| Ice shattering on probe tips | Spurious small-particle counts/artificial concentration spikes from shattered ice fragments impacting probe | Korolev tips installed with 70mm beam opening to prevent ice shattering (Korolev 2013) | (hb p. 14) |
| Buffer fill / variable 2D image data storage interval | 2D image data recorded at variable intervals when buffer fills, potentially causing irregular temporal sampling of images | - | (hb p. 12) |
| Concentration-dependent uncertainty at high particle concentrations (CAS, buffer/data... | Uncertainty in concentration increases at high particle loads; CAS concentration uncertainty cited as +/-15% (Baumgardner et al. 2001); CIP upper concentration range limited to up to 500... | - | (hb p. 12) |
| CAS particle out-of-focus sizing error | If a particle is not perfectly between the sapphire windows, the amount of light bounced back does not correspond to true particle size, causing size misassignment; detected via anomalous... | S&P data used to determine if particle is in focus; qualifier criterion (0.5*Sizer less than  Qualifier) rejects particles not in focus | (hb p. 6) |
| Low-gain-stage noise threshold | Values in lower gain stage below 150 are ignored as noise, potentially causing small real signals to be dropped | - | (hb p. 8) |
| Missing/incomplete data quality (DQ) webpage link | No dedicated DQ page found for these data sets, limiting ability to check flagged quality issues online | - | (hb p. 4) |
| CAS aerosol refractive index correction needed | CAS is processed with a refractive index of 1.33 (liquid water); sizing of aerosols using this default index would be inaccurate | A correction will need to be made to use for aerosols | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field/lab calibration uses a spinning disk attachment (provided by DMT) that recreates images of perfectly spherical drops (four different sizes); operator aligns spinning disk with photo-detector array and adjusts airspeed via PADS software until drops appear spherical, then compares known diameter of drops to live... (hb p. 17) |
| Calibration interval | In the field, CAPS is calibrated before and after the first and last research flights; one day a week dedicated to calibrations, generally calibrated every other week. Between campaigns, probe shipped to vendor for in-depth calibration. Latest vendor calibration was October 2019; previous one was August 2016. (hb p. 17) |
| Traceability | Vendor calibrations supply updated values for calibration curves and constants used in signal-to-output conversions; results tracked by AAF's director of engineering (contact Jason Tomlinson); AAF is working to incorporate calibrations into ARM's databases. (hb p. 17) |
| Routine maintenance | Use acetone on Q-tips to clean the CIP window before every flight. Clean any insects or residue from the surface of the probe if visible. (hb p. 18) |
| Maintenance interval | Before every flight (CIP window); CAS windows cleaned only on calibration days (once per week) (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: 2DS-AIR (two-dimensional stereo probe aboard aircraft), FCDP (fast cloud droplet probe), WCM (water content meter), Gerber PVM-100a liquid water probe, CAS (cloud and aerosol spectrometer, co-located component of CAPS), HW (hotwire LWC sensor, co-located component of CAPS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `CIP` | Cloud imaging probe |
| `CAPS` | Cloud, aerosol, and precipitation spectrometer |
| `CAS` | Cloud and aerosol spectrometer |
| `HW` | Hotwire (liquid water content sensor using platinum resistance temperature detector wire) |
| `2DS-AIR` | Two-dimensional stereo probe aboard aircraft |
| `DPOL` | Dual polarization |
| `PBP` | Particle by particle |
| `MVD` | Median volume diameter |
| `ED` | Effective diameter |
| `LWC` | Liquid water content |
| `PADS` | Particle Analysis and Display System (vendor software) |
| `AAF` | ARM Aerial Facility |
| `PSL` | Polystyrene latex |
| `RTD` | Resistance temperature detector |


### References the handbook cites

- Baumgardner, D, H Jonsson, W Dawson, D O'Connor, and R Newton. 2001. "The cloud, aerosol and precipitation spectrometer: a new instrument for cloud investigations." Atmospheric Research 59-60: 251-264,...
- Korolev, Alexi. 2013. "Modification and Tests of Particle Probe Tips to Mitigate Effects of Ice Shattering." Journal of Atmospheric and Oceanic Technology 30(4): 690-708, https://doi.org/10.1175/JTECH-D-12-00142.1
- CAPS Manual: CAPS operator Manual 2010 w wiring schematics.pdf
- Cloud Aerosol Spectrometer with Particle by Particle Manual
- The Cloud Aerosol Spectrometer Depolarization Option

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf (20 pages, DOE/SC-ARM-TR-246, by L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=cip-air`, read 2026-09-23
- Example file: `enaaafcipF1.b1.20180218.122850.nc` from `enaaafcipF1.b1`, 9.66 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
