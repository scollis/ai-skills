---
name: arm-instrument-prp
description: ARM Portable Radiation Package (prp) - handbook-derived instrument reference. Measurement principle, reported quantities (Pitch and roll, Total, Shortwave irradiance, Longwave irradiance, FRSR global and sweep voltages, Head temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (acxprptcmM1.b1) and the variable inventory of a real file. Use when working with prp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - prp, Portable Radiation Package, acxprptcmM1.b1, Pitch and roll, Total, Shortwave irradiance, Longwave irradiance, FRSR global and sweep voltages, Radiometric, Remote Measurements & Research Co. PRP2 system, components - Garman GPS17X/GPS16X (GPS), FRSR, MFRSR, SPN1.
---

# PRP - Portable Radiation Package

The Portable Radiation Package (PRP/PRP2) is a modular suite of a Precision Spectral Pyranometer (PSP), Precision Infrared Radiometer (PIR), SPN1 total/diffuse sensor, GPS, tilt-compass, and a continuously rotating fast-rotating shadowband radiometer (FRSR) deployed on moving platforms such as ships to measure shortwave and longwave broadband irradiance, spectral direct/diffuse/global irradiance, and aerosol optical depth.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 90 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `prp` |
| Handbook | [DOE/SC-ARM-TR-198 / RM Reynolds / August 2017](https://www.arm.gov/publications/tech_reports/handbooks/prp_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Remote Measurements & Research Co. PRP2 system; components: Garman GPS17X/GPS16X (GPS), Precision Navigation Inc. TCM2.5 (tilt-compass), RMR Co. RAD Model 200 (radiometer analog-to-digital... |
| Primary measurements | Longwave broadband downwelling irradiance; Navigation variables; Shortwave broadband diffuse downwelling irradiance; Shortwave broadband direct normal irradiance; Shortwave broadband total downwelling irradiance; Shortwave narrowband total downwelling irradiance |
| Record | 2012-11-02 to 2020-10-30 (retired) |
| Datastreams with data | 31 across 4 sites |
| Sites | acx, mag, mar, mos |
| ARM page | https://www.arm.gov/capabilities/instruments/prp |


## Credit

Everything this skill knows about the instrument is the work of **RM Reynolds** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> RM Reynolds. *Portable Radiation Package (PRP) Instrument Handbook*, DOE/SC-ARM-TR-198, August 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/prp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The FRSR follows the multi-frequency rotating shadowband radiometer (MFRSR) principle: a continuously rotating shadowband sweeps across the sky so that global, shadow, and edge voltages are measured for each of seven channels in a fraction of a second, and the direct-beam irradiance is derived by subtracting a corrected diffuse component from the global irradiance while automatically correcting for the portion of sky blocked by the shadowband and removing electronic bias. Because the platform (e.g., a ship) is unlevel and unaligned in azimuth, the measured angles must be transformed from the plane of the instrument head to Earth-based geographic coordinates using externally measured pitch, roll, and heading (from the TCM and GPS) via coordinate rotation matrices. The extinction of solar radiation through the atmosphere is treated via the Beer-Bouguer-Lambert law, with the total extinction coefficient decomposed into aerosol, Rayleigh, ozone, and NO2 contributions as a function of wavelength and air mass; optical depths are derived from Langley calibration of the extraterrestrial voltage V0. The PSP and PIR thermopile radiometers' microvolt analog signals are converted by the RAD interface (amplified and digitized) into calibrated shortwave and longwave irradiance in physical units (Wm-2), while the SPN1 uses an array of seven thermopile sensors under a computer-generated shading pattern to directly measure global and diffuse irradiance without a moving shadowband.

**Siting.** Deployment requires an exposed location, ideally as high as possible, free of nuisance shadows from masts, antennas, or structures; clear horizons toward sunrise/sunset are important. On ships, the FRSR plate should be aligned so north points to north (or aligned to the bow), to an accuracy of approximately +/-5 degrees; RAD radiometers should be mounted at the same height as the FRSR head diffuser so none significantly shades another down to the horizon; GPS antenna needs greater than 80% sky coverage; RS232 serial connections to the CDU should be less than 200 ft, and network cable runs less than 100 m; minimal RF interference/radar exposure is required; because ship obstacles inevitably...

**Sampling.** native rate GPS 1 Hz NMEA0183 (4800 bps); TCM 1 Hz (RS232 0600/9600 bps); RAD1 serial 19200 bps; FRSR serial 38400 bps; RAD2 serial 38400 bps; SPN1 serial 9600 bps; ADC 8-channel 16-bit; reported every 1-minute averaged files (AVG-i.txt); raw data files accumulated hourly/daily; averaging Primary data product is a one-minute time series (1-min averages); shadow sweep cycle occurs every 3.4 sec with 250 measurements per channel per sweep; first and last 10 samples per channel averaged for global measurement; tilt sensor read twice per shadowband cycle (hb p. 31).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Latitude/Longitude/Speed over ground/Course over ground | per NMEA0183 GPRMC | Defined by GPRMC specification | Typically +/- 10 m | - | (hb p. 16) |
| Pitch and roll (tilt) of MFR head | degrees | Tilt range +/-50 deg | Sensor tilt accuracy 0.2 deg RMS; At-sea... | - | (hb p. 17) |
| Total (global) and diffuse solar irradiance (SPN1/SPN2) | Wm-2 | 0-2000 Wm-2 | currently under evaluation | 0.6 Wm-2 | (hb p. 19) |
| Shortwave irradiance (PSP via RAD) | Wm-2 (analog millivolts... | Analog input +/-8 millivolts | Computed irradiance accuracy less than  1%;... | - | (hb p. 18) |
| Longwave irradiance (PIR via RAD) | Wm-2 (analog millivolts... | Analog input +/-2 millivolts | Computed irradiance accuracy less than  1%;... | - | (hb p. 18) |
| FRSR global and sweep voltages (six 10 nm shortwave bands:... | millivolts | 0-3500 mv after FRSR preamp, depending... | +/- 1 mv | Approx. 2 mv | (hb p. 20) |
| Direct beam radiance, diffuse and global irradiance,... | Wm-2 / optical depth... | - | - | - | (hb p. 11) |
| Head temperature (thermistor) | degC | 0-50 degC (thermistor); head maintained... | Head temp maintained 40 +/- 0.2 degC | - | (hb p. 65) |


## Specifications

| parameter | value | source |
|---|---|---|
| Power (system) | 10-18 VDC; Current = 200mA normal with 3-sec pulses to 2 A when MFR head heater is on | (hb p. 6) |
| Communication (system) | Ethernet connection to host LAN | (hb p. 6) |
| Components (system) | Four main components: FRSR plate, RAD1 (with SPN1), RAD2 (with SPN2), and the Control Data Unit (CDU) | (hb p. 6) |
| Temperature (system) Storage | -20 to 80 degC | (hb p. 6) |
| Temperature (system) Operating | 5 to 50 degC | (hb p. 6) |
| GPS Model | Garman model GPS17X or GPS 16X | (hb p. 7) |
| GPS Physical | Size: 96.1mm diam. x 49.5mm height; Weight: 201 g; Case: white molded plastic, waterproof to IEC 60529 IPX7 | (hb p. 7) |
| GPS Power | 8-33 VDC, 40 mA 12 VDC | (hb p. 7) |
| GPS Communication | RS232, 4800 bps, 8-n-1 | (hb p. 7) |
| GPS Operating Temperature | 20 to 80 degC | (hb p. 7) |
| GPS Accuracy/Uncertainty | Typically +/- 10 m | (hb p. 7) |
| GPS Sensitivity | Typically 2 m | (hb p. 7) |
| TCM Model | Precision Navigation Inc. model TCM2.5 | (hb p. 8) |
| TCM Physical | Circuit board lwh = 50.8 x 63.5 x 10.7 mm, weight=20 g; Enclosure: lwh = 125 x 80 x 57 mm | (hb p. 8) |
| TCM Power | 6-18 VDC typ less than  20 mA | (hb p. 8) |
| TCM Communication | RS232, 0600 bps, 8-n-1 | (hb p. 8) |
| TCM Tilt range | +/-50 deg | (hb p. 8) |
| TCM Sensor tilt accuracy | 0.2 deg RMS | (hb p. 8) |
| TCM Operating temperature | -20 to 70 degC | (hb p. 8) |
| TCM At-sea uncertainty | Typically 1-min mean +/-0.2 deg | (hb p. 8) |
| RAD Model | Radiation analog-to-digital (RAD) interface, Model 200 | (hb p. 9) |
| RAD Physical | Enclosure: lwh = 160 x 100 x 81 mm | (hb p. 9) |
| RAD Power | 9-16 VDC, Typ less than  10 ma | (hb p. 9) |
| RAD Communication | RS232, 19200 bps, 8-n-1 | (hb p. 9) |
| RAD Analog inputs Shortwave | +/-8 millivolts | (hb p. 9) |
| RAD Analog inputs Longwave | +/-2 millivolts | (hb p. 9) |


_23 further specification rows are in the handbook._

## The data

Verified example: **`acxprptcmM1.b1`**, file `acxprptcmM1.b1.20150208.000000.cdf`
(0.11 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 17 |
| QC variables | 2 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2015-02-08T00:00:00 to 2015-02-08T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 1 minute |
| dod version | prptcm-b1-1.1 |
| process version | ingest-prp-1.12-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pitch` | degree | time | yes | Pitch angle |
| `roll` | degree | time | yes | Roll angle |
| `circuit_board_temperature` | degC | time | - | Circuit (interior) temperature |
| `compass_heading` | degree | time | - | Flux-gate compass heading, errors from ship magnetism |
| `pitch_std` | degree | time | - | Pitch angle, standard deviation |
| `roll_std` | degrees | time | - | Roll angle, standard deviation |
| `time` | - | time | - | Time offset from midnight |
| `xmag` | microTorr | time | - | Magnetometer field, x component, +/- 80 microTorr |
| `ymag` | microTorr | time | - | Magnetometer field, y component, +/- 80 microTorr |
| `zmag` | microTorr | time | - | Magnetometer field, z component, +/- 80 microTorr |


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
                     params={"user": f"{user}:{token}", "ds": "acxprptcmM1.b1",
                             "start": "2015-02-08", "end": "2015-02-08", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./acxprptcmM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "acxprptcmM1.b1", "2015-02-08", "2015-02-08")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("acxprptcmM1.b1", "2015-02-08", "2015-02-08"))   # cite what you pulled
```

## Quality control in this datastream

2 `qc_` companion variables cover 2 of the
17 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_pitch"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("pitch", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["pitch", "roll"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("acxprptcmM1.b1", "20121102", "20260923")
```

The handbook's own note on data quality: Data quality health and status results are posted at http://dq.arm.gov/, containing techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality; however, as of the handbook date the PRP2 is not yet a certified ARM instrument, so no real-time graphical data presentation site exists, and the calibration/QA database is still in development. Grounding quality is checked operationally by monitoring the standard deviation of one-minute mean FRSR global measurements (displayed by the PRPRX program) and of ADC channel readings; elevated...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Grounding problems / noise contamination | FRSR global measurement standard deviation much larger than normal (on order of 100 mv vs normal 5 mv on clear bright days); ADC channel standard deviations of 10-20 mv normally, much... | Verify resistance between all components (including FRSR head and preamp box) is less than one ohm; investigate grounding; try alternate grounding... | (hb p. 23) |
| Shading from ship structures (masts, antennas, obstacles) | Radiometer irradiance readings show unexpected dips/drops when ship obstacles cast shadows on sensors | Deploy a second RAD/SPN combination (RAD2/SPN2) at a second location so at least one radiometer is fully exposed; choose most exposed location for... | (hb p. 9) |
| MFR head cable/connector fragility and water intrusion | Intermittent or lost signal from MFR head; connector corrosion or water damage evident on inspection | Handle cable carefully, avoid twisting/bending; seal plug backshells with self-sealing tape and Scotch 88 tape; use silicone grease in receptacle;... | (hb p. 21) |
| Cold-weather difficulty with Impulse connectors | Connectors become very difficult to disconnect below 0degC | Use a hot air gun to warm connectors before removal | (hb p. 22) |
| Head temperature out-of-range causes data processing to stop | Measured head temperature falls outside 37-43degC range; corresponding measurements are marked missing | Check thermistor circuit continuity and voltage at TP22; head calibrations valid only around 40degC | (hb p. 85) |
| Open thermistor circuit disables heater | TP22 reads zero volts; heater does not actuate; head temperature drifts outside valid range | Check cable continuity, open plug backshells for bad solder joints, verify with 10K ohm test resistor giving 25degC reading | (hb p. 85) |
| Platform tilt / wave-induced horizontal accelerations contaminating tilt measurements | 1 Hz TCM pitch/roll data show sinusoidal wave-induced motion mixed with true tilt | Use 1-minute averages to remove sinusoidal wave-induced horizontal accelerations; final processing focuses on 1-min averages considered accurate | (hb p. 8) |
| Shadowband sky-blocking bias (occulting band blocks portion of diffuse sky) | Direct-beam irradiance derived by simple global-minus-diffuse subtraction is biased low without edge correction | Use edge irradiance (VE) measurement, average of two edge values, to correct for blocked sky and remove electronic bias via subtraction | (hb p. 16) |
| Dissimilar metal galvanic corrosion in RAD/PRP hardware | Lid screws and backplate hardware corroded/frozen in place, sometimes requiring lid to be cut off | Use nylon washers/insulators, anti-seize compound, sealing compound in mounting holes, silicone grease on o-rings | (hb p. 86) |
| Radiometer dome contamination (dust, salt spray) | Visible dust/salt deposit accumulation on PSP/PIR domes reducing measured irradiance accuracy | Regular fresh-water rinse and cleaning with wet then dry lintless optical wipes; frequency depends on environment | (hb p. 87) |
| O-ring/seal failure leading to water intrusion into enclosures | Severe water damage inside enclosure; corrosion of internal electronics after prolonged exposure | Ensure o-rings are perfect, use sealant on connector holes, inspect and grease regularly | (hb p. 88) |
| RF/radar interference near shipboard installation | Severe electronic noise in radiometer/FRSR data when near radar beams | Select exposed location with minimal RF interference and radar exposure | (hb p. 64) |
| Ground loop from FRSR head cable shield | Elevated noise if shield connected at both ends | Shield connected only at CDU end (marked with tape), not connected at head end, to prevent ground loops | (hb p. 22) |
| Low solar flux nighttime mode transition | Data packets switch to 'Low Mode' (~17 characters) when solar flux falls below approximately 5 Wm-2; shadowband parked at nadir | Recognize Low Mode packets as nighttime operation, not instrument fault | (hb p. 67) |
| No shadow detected mode (High, No Shadow Mode) | Packet contains only global information (~400 characters), no valid shadow-derived direct-beam data | None specified beyond recognizing packet mode | (hb p. 67) |
| SPN1 sensor uncertainty not yet established | No stated uncertainty value for SPN1 total/diffuse irradiance in specification table | Sensor currently under evaluation | (hb p. 19) |
| PRP2 not a certified ARM instrument / no real-time QC site | No real-time data graphical presentation available; calibration/QA database still in development | PRP data available only via field project data reports; check http://dq.arm.gov/ for data quality health and status when available | (hb p. 14) |
| Motor/shaft o-ring wear and set screw loosening from vibration | Shadowband motor sticking, misalignment, or shaft slipping over time on ship deployments | Periodic disassembly, replace shaft o-rings, tighten set screws, use blue LokTite on set screws (24 hr cure) | (hb p. 40) |
| GPS sky-view obstruction reduces position/time accuracy | Degraded GPS fix or dropouts if sky coverage is poor | Mount GPS with greater than 80% sky coverage in exposed location | (hb p. 21) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Electronic gains calibrated end-to-end with precision millivolt reference source; FRSR head calibrated via lamp calibration (mv per Wm-2), bandpass spectral response calibration, and zenith angle calibration on two planes using collimated beam tilting fixture; Langley determination used to derive V0 for seven channels (hb p. 36) |
| Calibration interval | Lab calibration prior to deployment; MFR head recalibrated at SGP calibration facility; Langley calibrations performed using multiple clear days (hb p. 36) |
| Traceability | MFR head calibration procedure same as used for MFRSR heads; calibration files: Lamp file, Angular response file, Specular response file (hb p. 36) |
| Routine maintenance | MFR head calibration at SGP facility producing lamp, angular response, and specular response files; shadowband motor disassembly to replace shaft o-rings and tighten set screws; use of silicone grease, blue LokTite, and anti-seize on hardware; radiometer dome rinsing and cleaning with lintless wipes; ground strap... (hb p. 39) |
| Maintenance interval | Pre-deployment, daily, and long-term service checklists; grounding joint checked typically every six months; shadowband motor assembly serviced on a regular basis (hb p. 39) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR, FRSR (predecessor PRP versions).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOD` | aerosol optical depth |
| `CDU` | Control Data Unit |
| `FRSR` | fast-rotating shadowband radiometer |
| `MFR` | multifilter radiometer (head) |
| `MFRSR` | multi-frequency rotating shadowband radiometer |
| `PIR` | precision infrared radiometer |
| `PSP` | precision spectral pyranometer |
| `RAD` | radiometer analog-to-digital converter/interface |
| `SPN1` | Delta-T SPN1 sensor measuring global and diffuse solar irradiance |
| `TCM` | tilt compass sensor |
| `GPS` | Global Positioning System |
| `AOT` | atmospheric optical thickness |


### References the handbook cites

- Harrison et al. 1994 (MFRSR design)
- Liou 1980
- Paltridge and Platt 1977
- Colina et al. 1996 (reference solar spectrum)
- Kasten and Young 1989 (air mass formulation)
- Michalsky 1988; Spencer 1989 (ephemeris algorithm)
- Penndorf 1957 (Rayleigh scattering coefficients)
- Long 1996 (radiative budget from shadowband technique)
- 2000: Design, Operation, and Calibration of a Shipboard Fast-Rotating Shadowband Spectral Radiometer, Jtech (rmrco.com pub00)
- 2003: The Accuracy of Marine Shadow-band Sun Photometer Measurements of Aerosol Optical Thickness and Angstrom Exponent, Jtech (rmrco.com pub03)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/prp_handbook.pdf (90 pages, DOE/SC-ARM-TR-198, by RM Reynolds)
- Catalog record: ARM data-source index, `instrument_class_code=prp`, read 2026-09-23
- Example file: `acxprptcmM1.b1.20150208.000000.cdf` from `acxprptcmM1.b1`, 0.11 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
