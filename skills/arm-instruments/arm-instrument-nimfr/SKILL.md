---
name: arm-instrument-nimfr
description: ARM Normal Incidence Multifilter Radiometer (nimfr) - handbook-derived instrument reference. Measurement principle, reported quantities (Direct normal irradiance, Instrument output signal), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpnimfr7nchlangplotC1.c1) and the variable inventory of a real file. Use when working with nimfr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Radiometric. Triggers - nimfr, Normal Incidence Multifilter Radiometer, sgpnimfr7nchlangplotC1.c1, Direct normal irradiance, Instrument output signal, Aerosols, Radiometric, Yankee Environmental Systems, Inc. (electronics cube/sensors shared with MFRSR), ESRL, IMMS, MFRSR, NIMFR.
---

# NIMFR - Normal Incidence Multifilter Radiometer

The NIMFR is a sunphotometer mounted on a solar tracking device that points directly at the sun to provide a time series of shortwave spectral direct normal irradiance at six narrowband channels and one broadband channel.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nimfr` |
| Handbook | [DOE/SC-ARM/TR-059 / GB Hodges, JJ Michalsky / January 2011](https://www.arm.gov/publications/tech_reports/handbooks/nimfr_handbook.pdf) |
| Measurement category | Aerosols; Radiometric |
| Manufacturer / model | Yankee Environmental Systems, Inc. (electronics cube/sensors shared with MFRSR); Campbell Scientific CR1000 data logger used for MFRSR (NIMFR uses older-style data loggers) |
| Primary measurements | Aerosol optical depth; Shortwave broadband direct normal irradiance; Shortwave narrowband direct normal irradiance |
| Record | 1997-10-16 to 2026-09-23 (active) |
| Datastreams with data | 15 across 3 sites |
| Sites | nsa, sgp, shb |
| ARM page | https://www.arm.gov/capabilities/instruments/nimfr |


## Credit

Everything this skill knows about the instrument is the work of **GB Hodges, JJ Michalsky** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> GB Hodges, JJ Michalsky. *Multifilter Rotating Shadowband Radiometer (MFRSR) Handbook, With subsections for the following derivative instruments: Multifilter Radiometer (MFR), Normal Incidence Multifilter Radiometer (NIMFR)*, DOE/SC-ARM/TR-059, January 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/nimfr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `mfr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `nimfr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The NIMFR uses the same electronics cube and sensors found in the MFRSR, but mounted in a collimating tube instead of the open head, and mounted on a solar tracking device so it can be pointed at the sun throughout the day. Because it points directly at the sun, it measures direct beam irradiance as a principal measurement rather than deriving it from global and diffuse measurements as the MFRSR does, and there is no need to determine and correct for instrument cosine errors. It measures solar energy in six narrowband channels (nominal wavelengths 415, 500, 615, 673, 870, and 940 nm) and one open/broadband channel, from which atmospheric aerosol optical depth at each wavelength can be inferred, and in turn column abundances of ozone and water vapor and other atmospheric constituents can be derived. There is no shadowband associated with the NIMFR, so it never has the shading issues common with MFRSRs, and it produces cleaner data at high solar zenith angles because it points at the sun.

**Siting.** The NIMFR must be mounted on a solar tracking device so that it can be pointed at the sun throughout the day. (General MFRSR siting guidance also applies: instrument should be mounted on a stable post or platform with as few obstructions as possible, ideally with no site obstructions casting a shadow over the instrument at any point during the day; ARM currently fields NIMFRs only at the SGP CF in Oklahoma and the NSA Barrow site; the NSA Atqasuk site also operated a NIMFR before being shut down in December 2010.)

**Sampling.** native rate Sampling intervals started at 20-second intervals (as described for MFRSR logging system); averaging Nighttime data averaged to produce offset correction for the following day (MFRSR); Langley calibration used for field calibration (hb p. 13).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Direct normal irradiance (narrowband channels) | millivolts (fundamental... | - | - | - | (hb p. 18) |
| Shortwave spectral direct normal irradiance | - | - | - | - | (hb p. 7) |
| Instrument output signal (shared spec with MFRSR head) | millivolts | ± 250 millivolts | 0.06% of 250 millivolts, i.e., 0.15 millivolts | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | millivolts (fundamental measurements) | (hb p. 13) |
| Range | ± 250 millivolts | (hb p. 13) |
| Accuracy | 0.06% of 250 millivolts, i.e., 0.15 millivolts | (hb p. 13) |
| Repeatability | 33.3 µvolts (if differential measurement) | (hb p. 13) |
| Uncertainty | 0.06% of 250 millivolts | (hb p. 14) |
| Input Voltage | Excitation voltage for thermistors is 5 volts | (hb p. 14) |
| Input Current | 1 nano-amperes (typical) | (hb p. 14) |
| Nominal narrowband wavelengths | 415, 500, 615, 673, 870, and 940 nm | (hb p. 7) |
| Half-step increment (motor) | 0.45 degrees per half-step; ~108 seconds for sun to move that amount | (hb p. 13) |


## The data

Verified example: **`sgpnimfr7nchlangplotC1.c1`**, file `sgpnimfr7nchlangplotC1.c1.20260918.215624.nc`
(0.89 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=6412 |
| Data variables | 35 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-18T21:56:24 to 2026-09-18T23:43:15 |
| dod version | nimfr7nchlangplot-c1-1.0 |
| process version | vap-langley-6.5-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `barnard_airmass` | 1 | time | - | Airmass, Barnard |
| `barnard_lnI_filter1` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter1, Barnard |
| `barnard_lnI_filter2` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter2, Barnard |
| `barnard_lnI_filter3` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter3, Barnard |
| `barnard_lnI_filter4` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter4, Barnard |
| `barnard_lnI_filter5` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter5, Barnard |
| `barnard_lnI_filter6` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter6, Barnard |
| `barnard_lnI_filter7` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter7, Barnard |
| `barnard_rejected_filter1` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter1,... |
| `barnard_rejected_filter2` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter2,... |
| `barnard_rejected_filter3` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter3,... |
| `barnard_rejected_filter4` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter4,... |
| `barnard_rejected_filter5` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter5,... |
| `barnard_rejected_filter6` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter6,... |
| `barnard_rejected_filter7` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter7,... |
| `michalsky_airmass` | 1 | time | - | Airmass, Michalsky |
| `michalsky_lnI_filter1` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter1, Michalsky |
| `michalsky_lnI_filter2` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter2, Michalsky |
| `michalsky_lnI_filter3` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter3, Michalsky |
| `michalsky_lnI_filter4` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter4, Michalsky |
| `michalsky_lnI_filter5` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter5, Michalsky |
| `michalsky_lnI_filter6` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter6, Michalsky |
| `michalsky_lnI_filter7` | ln(re W/(m^2 nm)) | time | - | Log(irradiance) for the Direct Narrowband Filter7, Michalsky |
| `michalsky_rejected_filter1` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter1,... |
| `michalsky_rejected_filter2` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter2,... |
| `michalsky_rejected_filter3` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter3,... |
| `michalsky_rejected_filter4` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter4,... |
| `michalsky_rejected_filter5` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter5,... |
| `michalsky_rejected_filter6` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter6,... |
| `michalsky_rejected_filter7` | 1 | time | - | Rejected points for the final fit for the Direct Narrowband Filter7,... |


_1 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpnimfr7nchlangplotC1.c1",
                             "start": "2026-09-18", "end": "2026-09-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpnimfr7nchlangplotC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpnimfr7nchlangplotC1.c1", "2026-09-18", "2026-09-18")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpnimfr7nchlangplotC1.c1", "2026-09-18", "2026-09-18"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("barnard_lnI_filter1")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpnimfr7nchlangplotC1.c1", "19971016", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Near real-time data plots accessible via ARM Data Quality Health and Status (DQ HandS) plot browser. Data quality health and status results, including techniques used by ARM's data quality analysts, instrument mentors, and site scientists to monitor and diagnose data quality, are available at http://dq.arm.gov/. Instrument Mentor Monthly Summary provides additional monitoring info.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Cosine response error (relevant to MFRSR, not NIMFR) | Varying instrument response depending on direction of solar disc; would show as systematic bias in irradiance vs solar zenith angle for cosine-corrected instruments, but NIMFR avoids this... | NIMFR eliminates the need for cosine error correction because it points at the sun; MFRSR uses a cosine response correction file built from cosine... | (hb p. 18) |
| Shading issues from shadowband motor coarse stepping (MFRSR only) | Shadowband only moves to a new position every five or six 20-second sampling intervals; if adjusted right after or just before a move, results in a shading issue in morning or afternoon data | Finer motor stepping (1/8 steps, 0.225 degrees) possible with new Campbell systems to reduce issue; NIMFR has no shadowband so never experiences this | (hb p. 13) |
| EMF interference from bang-on/bang-off head heater (older logger/NIMFR uses older-style... | Saw-tooth trace of head temperature; potential EMF interference with irradiance measurements during heater on/off cycling | Original logger gives irradiance measurements priority and stops heater during measurement; newer proportional heater controller (not used by NIMFR,... | (hb p. 12) |
| Langley calibration not possible for 940 nm channel | 940 nm channel calibration relies only on lamp (nominal) calibration, not Langley-calibrated data, due to highly variable atmospheric water vapor | Each head returned to SGP calibration facility annually for lamp calibration | (hb p. 18) |
| Sensor offset/bias inherent in each sensor | Non-zero nighttime signal indicating bias; affects total and diffuse irradiance measurements if uncorrected | Nighttime data averaged to produce offset correction for the following day, calculated on an ongoing basis rather than relying on a single... | (hb p. 16) |
| NIMFR does not provide total or diffuse irradiance | Absence of total/diffuse irradiance variables in NIMFR data output, unlike MFRSR | - | (hb p. 19) |
| NIMFR requires solar tracking device | Added mechanical complexity/expense; tracking errors could misalign instrument from sun, degrading direct beam measurement | - | (hb p. 19) |
| NIMFR is a custom-built instrument with very limited availability | Limited number of deployed NIMFR units (only SGP CF and NSA Barrow currently; NSA Atqasuk decommissioned December 2010) | - | (hb p. 19) |
| Side-band and sun-blocked measurement variability under rapidly changing sky conditions... | Side-band measurements taken just before/after sun-blocked measurement show impact of rapidly changing sky conditions on final derived values | Newer Campbell logging system records side-band and sun-blocked measurements plus both head thermistors for analysis | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Standard lamp calibration (nominal calibration), cosine response determination, and mapping of the spectral response function of each filter detector; once deployed and with enough data collected, the instrument is Langley-calibrated (hb p. 17) |
| Calibration interval | Each head is returned to the SGP calibration facility annually for lamp calibration (Langley calibration cannot be performed for the 940 channel due to highly variable water vapor) (hb p. 17) |
| Traceability | Nominal (lamp) calibration data found in .b1 data files; Langley-calibrated data contained in .c1 data files (hb p. 17) |
| Routine maintenance | Cleaning of the Spectralon diffuser; some heads include desiccant holders, desiccant should be checked monthly and replaced as necessary (hb p. 18) |
| Maintenance interval | Cleaning performed as frequently as reasonably possible, depending on site location from once daily to once every two weeks; desiccant checked monthly (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR (Multifilter Rotating Shadowband Radiometer), MFR (Multifilter Radiometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `EMF` | electromagnetic field |
| `ESRL` | Earth System Research Laboratory |
| `FOV` | field-of-view |
| `GMD` | Global Monitoring Division |
| `IMMS` | Instrument Mentor Monthly Summary |
| `MFR` | multifilter radiometer |
| `MFRSR` | multifilter rotating shadowband radiometer |
| `NIMFR` | normal incidence multifilter radiometer |
| `NOAA` | National Oceanic Atmospheric Administration |
| `NSA` | North Slope of Alaska |
| `SGP` | Southern Great Plains |
| `TWP` | Tropical Western Pacific |


### References the handbook cites

- Harrison, Lee, Joseph Michalsky, and Jerry Berndt. 1994. "Automated Multifilter Rotating Shadow-Band Radiometer: An Instrument for Optical Depth and Radiation Measurements." Applied Optics 33: 5118-5125.
- Harrison, Lee, and Joseph Michalsky. 1994. "Objective Algorithms for the Retrieval of Optical Depths from Ground-Based Measurements." Applied Optics 33: 5126-5132.
- Michalsky, J.J., J.C. Liljegren, and L.C. Harrison. 1995. "A Comparison of Sun Photometer Derivations of Total Column Water Vapor and Ozone to Standard Measures of Same at the Southern Great Plains Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/nimfr_handbook.pdf (20 pages, DOE/SC-ARM/TR-059, by GB Hodges, JJ Michalsky)
- Catalog record: ARM data-source index, `instrument_class_code=nimfr`, read 2026-09-23
- Example file: `sgpnimfr7nchlangplotC1.c1.20260918.215624.nc` from `sgpnimfr7nchlangplotC1.c1`, 0.89 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
