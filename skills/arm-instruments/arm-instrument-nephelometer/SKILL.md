---
name: arm-instrument-nephelometer
description: ARM Nephelometer (nephelometer) - handbook-derived instrument reference. Measurement principle, reported quantities (Sample RH, Sample air pressure, Sample temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (pvcaosnephwetM1.c1) and the variable inventory of a real file. Use when working with nephelometer data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - nephelometer, Nephelometer, pvcaosnephwetM1.c1, Sample RH, Sample air pressure, Sample temperature, Aerosols, TSI model 3563 integrating nephelometer, HEPA, MAOS.
---

# NEPHELOMETER - Nephelometer

A nephelometer measures aerosol particle light-scattering coefficients (total scatter and backscatter) at three wavelengths by detecting light scattered from an aerosol sample drawn through the instrument, and is deployed at ARM sites to characterize aerosol optical scattering properties, formerly paired with a second nephelometer and RH conditioner as a humidigraph.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nephelometer` |
| Handbook | [J Uin](https://www.arm.gov/publications/tech_reports/handbooks/nephelometer_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | TSI model 3563 integrating nephelometer |
| Primary measurements | Aerosol backscattered radiation; Aerosol scattering |
| Record | 2010-10-04 to 2026-09-23 (active) |
| Datastreams with data | 123 across 23 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, mag, mao |
| ARM page | https://www.arm.gov/capabilities/instruments/nephelometer |


## Credit

Everything this skill knows about the instrument is the work of **J Uin** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin. *Nephelometer Instrument Handbook*.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/nephelometer_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

An internal blower or external flow system draws an aerosol sample through a large-diameter inlet into the measurement volume, where it is illuminated over an angle of 7 to 170 degrees by a halogen lamp directed through an optical light pipe and opal glass diffuser. Three photomultiplier tubes view the sample volume through apertures, with dichroic filters and bandpass filters splitting the scattered light into blue (450 nm), green (550 nm), and red (700 nm) wavelengths. A constantly rotating reference chopper provides three types of signal detection: the aerosol light scattering signal, the PMT dark current (with all light blocked), and the light-source signal (via a translucent chopper area), compensating for changes in light source or detector efficiency over time. In backscatter mode, a backscatter shutter rotates under the lamp to block light in the 7 to 90 degree range so only backward-scattered light reaches the detectors, and this backscatter signal can be subtracted from the total signal to derive forward scattering. Periodically, an automated valve diverts the entire sample through a HEPA filter to measure the clean-air signal, which along with PMT dark current is subtracted from the aerosol-scatter signal to isolate the sample aerosol's scattering signal.

**Siting.** Deployed with an external sampling system drawing 7.5 lpm through the instrument; previously two identical nephelometers were run in series with a sample RH conditioner between them (humidigraph setup), labeled "wet" and "dry" (names switched at the MAOS site due to high ambient RH). Since 2024, humidigraph instruments were removed from service and only single nephelometers are retained without active RH conditioning (except drying sample flow before the AOS impactor).

**Sampling.** reported every every five seconds (typical, depends on averaging time); averaging 30-second averaging time referenced for detection limits; 60-second averaging referenced for systematic uncertainty dominance (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle optical scattering coefficient (total... | m-1 | upper detection limit 2x10-2 m-1; lower... | within ±10% (accuracy); systematic uncertainty... | - | (hb p. 11) |
| Aerosol particle optical scattering coefficient... | m-1 | angular integration 90 to 170° | within ±10% | - | (hb p. 11) |
| Sample RH | % (dimensionless) | - | - | - | (hb p. 11) |
| Sample air pressure | hectopascals (hPa) | - | - | - | (hb p. 11) |
| Sample temperature | kelvins (K) | - | - | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units - scattering coefficient | inverse meters (m-1) | (hb p. 11) |
| Units - RH | % (dimensionless) | (hb p. 11) |
| Units - air pressure | hectopascals (hPa) | (hb p. 11) |
| Units - temperature | kelvins (K) | (hb p. 11) |
| Upper detection limit (scattering coefficient) | 2x10-2 m-1 | (hb p. 11) |
| Lower detection limit (30-second averaging) | between 1x10-7 and 3x10-7 m-1 (depending on wavelength) | (hb p. 11) |
| Angular integration - total scatter mode | 7 to 170° | (hb p. 11) |
| Angular integration - backscatter mode | 90 to 170° | (hb p. 11) |
| Accuracy | within ±10% | (hb p. 11) |
| Angular truncation error - submicron particles | 5-10% | (hb p. 11) |
| Angular truncation error - particles 1-10 μm | 30-50% | (hb p. 11) |
| Repeatability | within ±1% | (hb p. 11) |
| Gas calibration uncertainty contribution | ±1% | (hb p. 12) |
| Systematic uncertainty (wavelength/angular non-idealities) | within ±10% | (hb p. 12) |
| Sample flow rate | 7.5 lpm | (hb p. 14) |
| Wavelengths | 700 nm (red), 550 nm (green), 450 nm (blue) | (hb p. 7) |


## The data

Verified example: **`pvcaosnephwetM1.c1`**, file `pvcaosnephwetM1.c1.20130621.000000.cdf`
(0.19 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 29 |
| QC variables | 12 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2013-06-21T00:00:00 to 2013-06-21T23:59:00 |
| sampling interval | 1 second |
| averaging interval | not averaged |
| dod version | aosnephwet-c1-1.3 |
| process version | ingest-aosmqc-1.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Bbs_B_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal blue... |
| `Bbs_G_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol back-emispheric light scattering coefficient, nominal green... |
| `Bbs_R_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal red... |
| `Bs_B_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal blue wavelength... |
| `Bs_G_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal green wavelength... |
| `Bs_R_Wet_Neph3W_2` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal red wavelength at... |
| `P_Neph_Wet` | hPa | time | yes | Pressure inside reference nephelometer |
| `RH_Neph_Inlet_Wet` | % | time | yes | Relative humidity, reference nephelometer inlet |
| `RH_Neph_Vol_Wet` | % | time | yes | Relative humidity, inside reference nephelometer |
| `T_Neph_Inlet_Wet` | degC | time | yes | Temperature, reference nephelometer inlet |
| `T_Neph_Vol_Wet` | degC | time | yes | Temperature, inside nephelometer |
| `impactor_setting` | um | time | yes | Impactor setting in terms of aerodynamic diameter cut off |
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
                     params={"user": f"{user}:{token}", "ds": "pvcaosnephwetM1.c1",
                             "start": "2013-06-21", "end": "2013-06-21", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./pvcaosnephwetM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "pvcaosnephwetM1.c1", "2013-06-21", "2013-06-21")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("pvcaosnephwetM1.c1", "2013-06-21", "2013-06-21"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("Bs_B_Wet_Neph3W_2", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

12 `qc_` companion variables cover 12 of the
29 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_Bs_B_Wet_Neph3W_2"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("Bs_B_Wet_Neph3W_2", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["Bs_B_Wet_Neph3W_2", "Bs_G_Wet_Neph3W_2", "Bs_R_Wet_Neph3W_2"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (pvcaosnephwetM1.c1.20130621.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Bs_B_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |
| `Bs_R_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |
| `Bbs_R_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |
| `Bbs_B_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |
| `Bbs_G_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |
| `Bs_G_Wet_Neph3W_2` | Value is equal to missing_value. | 168 | 11.6667 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("pvcaosnephwetM1.c1", "20101004", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging of data based on criteria developed by instrument mentors and automatic generation of plots in collaboration with the ARM Data Quality Office. Automatic checks include checking the "mode" variable to determine operating mode (normal, zeroing) and flagging accordingly. Automatically generated plots include scattering coefficients and sample pressure, which should show periodic high/low values from external impactor state changes; scattering should usually be highest for blue (450 nm) and lowest for red (700 nm), with noted exceptions at...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Angular truncation error due to limited angular integration range (7 to 170°) | Scattering coefficients for larger particles read low relative to true value; error magnitude depends on particle size | Consider correction for certain applications (Anderson and Ogren 1998); error is 5-10% for submicron particles and 30-50% for particles 1-10 μm | (hb p. 11) |
| Sensitivity to sample pressure and humidity | Scattering coefficient measurements vary with sample RH and pressure changes not related to actual aerosol changes | No automatic corrections are applied by the instrument; care should be taken when comparing measurement results from different times and locations | (hb p. 12) |
| Random noise dominance at low particle concentrations or short sampling times | Noisy scattering coefficient signal near the detection limit (1x10-7 to 3x10-7 m-1 for 30-s averages) | - | (hb p. 12) |
| Systematic uncertainty dominance at higher concentrations/longer averaging | For scattering coefficients above ~10-6 m-1 and averaging times greater than ~60 s, bias from gas-calibration and wavelength/angular non-idealities dominates over random noise | - | (hb p. 12) |
| Impactor state switching on external sampling system | ~10 hPa 'jumps' in ambient/sample pressure and periodic high/low values in scattering coefficients corresponding to different impactor states | Can be used to verify proper operation of the external impactor valve | (hb p. 9) |
| Wavelength-dependent scattering ordering anomaly at marine sites | Normally scattering is highest for blue (450 nm) and lowest for red (700 nm); at marine-influenced sites the red scattering coefficient can instead be highest at 10 μm external impactor cut... | - | (hb p. 10) |
| Zeroing/HEPA filter periods | Data flagged as zeroing mode; typically for five minutes every day at midnight UTC when clean-air (HEPA-filtered) signal is measured instead of ambient aerosol | Automatic flagging of the 'mode' variable distinguishes normal vs zeroing operation | (hb p. 7) |
| Lamp failure | Visual inspection or software status indicates lamp failure | Replace the halogen lamp | (hb p. 14) |
| Water intrusion into internal HEPA filter system | Discoloration in tubes connected to the HEPA filter, especially in humid measurement locations | Replace the internal HEPA filter | (hb p. 14) |
| High-voltage source for PMTs / hot lamp housing | Not a data artifact but a safety hazard: user not exposed during normal operation, but lamp housing can reach burn-causing temperatures | Disconnect power and allow lamp/housing to cool before handling | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Measuring the scattering coefficients of dry CO2 gas introduced into the system and comparing them with known values from literature adjusted for calibration conditions (temperature, RH, air pressure) (Anderson et al. 1996). Calibration coefficients can be applied to raw measurement data. (hb p. 5) |
| Calibration interval | typically at least once every 12 months and as needed (e.g., before a new deployment) (hb p. 5) |
| Traceability | Calibrated by manufacturer before delivery and during instrument maintenance at manufacturer's facilities; calibration coefficients recorded by ARM. (hb p. 5) |
| Routine maintenance | Replacing the halogen lamp (when visual inspection or software status indicates lamp failure); replacing the internal HEPA filter (when discoloration in tubes connected to the HEPA filter indicates water in the system, especially relevant in humid measurement locations). (hb p. 14) |
| Maintenance interval | as needed / when failure indicated (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Aerosol Observing System (AOS), ARM impactor, humidigraph instrument.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `HEPA` | high-efficiency particulate air |
| `MAOS` | Mobile Aerosol Observing System |
| `PMT` | photomultiplier tubes |
| `RH` | relative humidity |
| `UTC` | Coordinated Universal Time |


### References the handbook cites

- Anderson, TL, DS Covert, SF Marshalll, ML Laucks, RJ Charlson, AP Waggoner, JA Ogren, R Caldow, RL Holm, FR Quant, GJ Sem, A Wiedensohler, NA Ahlquist, and TS Bates. 1996. "Performance characteristics of a...
- Anderson, TL, and JA Ogren. 1998. "Determining aerosol radiative properties using the TSI 3563 Integrating Nephelometer." Aerosol Science and Technology 29(1): 57-69
- Heintzenberg, J, and RJ Charlson. 1996. "Design and applications of the integrating nephelometer: A review." Journal of Atmospheric and Oceanic Technology 13(5): 987-1000
- TSI 3563 Three-Wavelength Integrating Nephelometer description by NOAA Earth System Research Laboratory Global Monitoring Division. 2015

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/nephelometer_handbook.pdf (16 pages, by J Uin)
- Catalog record: ARM data-source index, `instrument_class_code=nephelometer`, read 2026-09-23
- Example file: `pvcaosnephwetM1.c1.20130621.000000.cdf` from `pvcaosnephwetM1.c1`, 0.19 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
