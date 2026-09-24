---
name: arm-instrument-tap
description: ARM Tricolor Absorption Photometer (tap) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaostapE13.b1) and the variable inventory of a real file. Use when working with tap data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - tap, Tricolor Absorption Photometer, sgpaostapE13.b1, Aerosols, AOS07, PSAP, CAPS, Neph, Dry.
---

# TAP - Tricolor Absorption Photometer

The Tricolor Absorption Photometer (TAP), part of the SGP Aerosol Observing System (AOS07), measures three-wavelength aerosol light absorption on sample air drawn from the aerosol inlet stack and distributed through the AOS sample distribution system.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `tap` |
| Handbook | [DOE/SC-ARM-TR-267 / J Uin, S Smith, O Mayol-Bracero, D De Oliveira / April 2025](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Brechtel Manufacturing Inc. (TAP: tricolor absorption photometer) |
| Primary measurements |  |
| Record | 2016-03-21 to 2018-04-17 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tap |


## Credit

Everything this skill knows about the instrument is the work of **J Uin, S Smith, O Mayol-Bracero, D De Oliveira** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin, S Smith, O Mayol-Bracero, D De Oliveira. *Southern Great Plains (SGP) Aerosol Observing System (AOS) Instrument Handbook*, DOE/SC-ARM-TR-267, April 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tap`, the handbook ARM links for this instrument class is the SGP Aerosol Observing System handbook, which mentions TAP only in passing; the facts below are AOS-system-level and no TAP-specific handbook exists on arm.gov.

## How it measures

The handbook states that the instruments downstream of the impactor are selected because of the measurements they make: the nephelometers measure light scattering, and the PSAP and TAP measure light absorption, while the CAPS measures light extinction (the sum of scattering and absorption). These radiative parameters (scattering, absorption, extinction) are used to quantify how aerosols affect visibility and radiation transfer in the atmosphere and depend on aerosol particle size, with larger particles scattering much more light than smaller ones. The impactor upstream (one-micrometer or ten-micrometer cutoff, switchable) helps determine whether the measured light effect is due to a large number of small particles or a small number of large particles. No further TAP-specific optical or physical principle details are given in this handbook, which focuses on the AOS system as a whole rather than individual instruments.

**Siting.** The TAP is installed inside the AOS07 mobile laboratory shelter and receives sample air via the aerosol inlet stack (two 10-foot sections of 8-inch aluminum irrigation pipe, 20 feet tall) and the flow distributor/sample distribution system. Sample air passes through a switchable impactor (1 micrometer or 10 micrometer cutoff) before reaching the TAP and other optical instruments (nephelometers, PSAP, CAPS). Sample lines and the flow distributor are insulated to prevent water condensation in the lines. Placement of any guest instruments in the sample distribution system is coordinated with the AOS mentor to ensure no bias is introduced to standard measurements.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Three-wavelength aerosol light absorption | - | - | - | - | (hb p. 12) |


## The data

Verified example: **`sgpaostapE13.b1`**, file `sgpaostapE13.b1.20180414.000000.nc`
(63.78 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86170, `spot`=10 |
| Data variables | 42 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2018-04-14T00:00:00 to 2018-04-14T23:59:59 |
| sampling interval | 1 second |
| dod version | aostap-b1-1.1 |
| process version | ingest-aostapcorr-1.0-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `impactor_state` | unitless | time | yes | Impactor state in terms of aerodynamic diameter cut off |
| `transmittance_blue` | unitless | time | yes | Transmittance, blue channel, for valid active_spot_number |
| `transmittance_green` | unitless | time | yes | Transmittance, green channel, for valid active_spot_number |
| `transmittance_red` | unitless | time | yes | Transmittance, red channel, for valid active_spot_number |
| `active_spot_number` | count | time | - | Active spot number |
| `case_temperature` | degC | time | - | Case temperature |
| `change_time` | - | time | - | Time of either an active_spot_number or filter_id change |
| `clean_blue` | unitless | time,spot | - | Signal from blue LED at start of filter or spot change |
| `clean_green` | unitless | time,spot | - | Signal from green LED at start of filter or spot change |
| `clean_red` | unitless | time,spot | - | Signal from red LED at the start of filter or spot change |
| `elapsed_time` | second | time | - | Elapsed time as shown in the raw data |
| `filter_id` | count | time | - | Filter ID, increments for each new filter |
| `minimum_active_spot_duration` | second | - | - | Minimum active spot duration |
| `normalized_blue` | unitless | time,spot | - | Signal from blue LED through each filter spot normalized at start of... |
| `normalized_green` | unitless | time,spot | - | Signal from green LED through each filter spot normalized at start of... |
| `normalized_red` | unitless | time,spot | - | Signal from red LED through each filter spot normalized to start of... |
| `normalized_spot_transmittance_blue` | unitless | time,spot | - | Transmittance of blue LED through each filter spot normalized against... |
| `normalized_spot_transmittance_green` | unitless | time,spot | - | Transmittance of green LED through each filter spot normalized... |
| `normalized_spot_transmittance_red` | unitless | time,spot | - | Transmittance of red LED through each filter spot normalized against... |
| `record_type` | unitless | time | - | Record type shown in the raw data |
| `sample_air_temperature` | degC | time | - | Sample air temperature |
| `sample_volume` | m^3 | time | - | Sample volume |
| `seconds_after_transition` | second | time | - | Seconds since last impactor transition |
| `signal_blue` | unitless | time,spot | - | Signal from blue LED through each filter spot |
| `signal_blue_raw` | unitless | time,spot | - | Signal blue raw measurements |
| `signal_dark` | unitless | time,spot | - | Dark signal from detector below each filter spot |
| `signal_green` | unitless | time,spot | - | Signal from green LED through each filter spot |
| `signal_green_raw` | unitless | time,spot | - | Signal green raw measurements |
| `signal_red` | unitless | time,spot | - | Signal from red LED through each filter spot |
| `signal_red_raw` | unitless | time,spot | - | Signal red raw measurements |


_4 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaostapE13.b1", "2018-04-14", "2018-04-14")
ds = armlive_open("sgpaostapE13.b1", "2018-04-14", "2018-04-14", cleanup_qc=True)
```

This datastream carries 42 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaostapE13.b1", start, end,
                  keep_variables=["impactor_state", "transmittance_blue", "transmittance_green", "qc_impactor_state", "qc_transmittance_blue", "qc_transmittance_green"])
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
42 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpaostapE13.b1.20180414.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `impactor_state` | (seconds_after_transition less than  seconds_after_1um_warning)... | 5162 | 5.9905 |
| `impactor_state` | (seconds_after_transition less than  seconds_after_1um_alarm)... | 4515 | 5.2396 |
| `impactor_state` | (seconds_after_transition less than ... | 4475 | 5.1932 |
| `impactor_state` | (seconds_after_transition less than  seconds_after_10um_alarm)... | 3828 | 4.4424 |
| `impactor_state` | qc_impactor_state from impactor datastream is indeterminate | 1259 | 1.4611 |
| `impactor_state` | qc_impactor_state from impactor datastream is bad | 1215 | 1.41 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaostapE13.b1", "20160321", "20260923")
```

The handbook's own note on data quality: The handbook describes sample line integrity checks as a QC process: remove the sample line from the stack, cap the stack end with a HEPA filter, and confirm each connected instrument reads zero; further investigation is required if not. Every connection on the sample line is treated as a potential single point of failure. A future goal is to automate this using a zero-air purge system (as used during MOSAIC) that fills the AOS sampling system with particle-free air. Housekeeping data (temperatures, pressures, voltages, flows) are continuously logged and displayed via a virtual...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sample line leaks | Instrument readings not at zero when sample line is disconnected from the stack and capped with a HEPA filter | Perform sample line integrity checks: remove sample line from stack, place HEPA filter on stack end, confirm each instrument reads zero; investigate... | (hb p. 21) |
| Temperature/RH change of sample air in inlet lines | Some change in temperature and thus relative humidity of sample air is inevitable even though lines are insulated, monitored via dedicated T/RH port on flow distributor | Lines insulated; T/RH monitored using an Omega temperature/RH sensor and PID to display and log data | (hb p. 9) |
| Condensation in sample lines | Water condensing in sample lines could affect optical/aerosol measurements | Flow distributor and conductive tubing used to transport sample air is insulated to prevent water from condensing in the sample lines | (hb p. 7) |
| Ice buildup at inlet edge | Ice forming around edge of aerosol inlet hat could obstruct or bias sample flow | Thermistor and 175-watt band heater around rain cover edge, controlled to 5°C via Omega PID controller, prevents ice buildup | (hb p. 3) |
| Aerosol particle size bias in scattering/absorption/extinction measurements | Larger particles scatter much more light than smaller ones, so light-absorption/extinction/scattering readings can be biased by particle size distribution | Use of switchable impactor (1 micrometer or 10 micrometer cutoff) upstream to determine whether large numbers of small particles or small numbers of... | (hb p. 12) |
| Power interruption/bumps at SGP site | Instrument power loss or brief power bumps could interrupt data collection | UPS absorbs expected power bumps and keeps all instruments on for about 30 minutes after a power loss | (hb p. 12) |
| Enclosure overheating from pumps/blowers/air drier | Elevated cabinet or pump temperatures recorded in housekeeping data | Temperature sensors mounted on each pump and near top of air drier as part of housekeeping measurements; four 10-inch fans circulate air into and out... | (hb p. 5) |
| Guest instrument sampling bias | Addition of guest instruments to the sample distribution system could alter flow rates or bias standard measurements | Instrument mentors coordinate placement of guest instruments with AOS mentor; flow rate in modified sample line adjusted to compensate for additional... | (hb p. 7) |
| Structural corrosion (rust) of AOS shelter | Visible rust on outside of structure during monthly inspection | Scrape, clean, and apply touch-up paint as needed on a monthly basis | (hb p. 21) |
| Guy wire tension loss over time | Cables feel loose compared to others; cables stretch over time | Check guy wires for rubbing/frayed wires, confirm similar tension, adjust tension as needed | (hb p. 22) |


## Calibration and maintenance

|  |  |
|---|---|
| Routine maintenance | Setup and operation information for individual instruments (including TAP) is found in separate handbooks and the AOS Procedures Manual; operators fill out daily log sheets covering each instrument and AOS systems as provided by mentors. Sample line integrity checks (removing the sample line from the stack, placing a... (hb p. 15) |
| Maintenance interval | Sample line integrity checks: before deployment (prior to AOS leaving the facility), on-site before any disruptions/modifications to sample lines, on-site after field activities once work is completed, and as needed whenever a significant change occurs (e.g., replacing a tube or adding/removing a component). (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ACSM, APS, CAPS, CCN-200, CPCf, CPCu, Neph, Dry, n-SMPS, PSAP, SMPS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOS` | Aerosol Observing System |
| `AOS07` | SGP AOS (designation for this specific Aerosol Observing System unit) |
| `TAP` | tricolor absorption photometer (Brechtel Manufacturing Inc.) |
| `PSAP` | particle soot absorption photometer (Radiance Research) |
| `CAPS` | cavity attenuated phase shift monitor (Aerodyne Research Inc.) |
| `Neph, Dry` | nephelometer, ambient RH (TSI Inc.) |
| `Neph, Wet` | nephelometer, controlled RH (TSI Inc.) |
| `PID` | proportional, integral, derivative controller |
| `RTD` | resistance temperature detector |
| `DAQ` | data acquisition board |
| `VI` | virtual instrumentation |
| `VM` | virtual machine (computer) |
| `IOP` | intensive operational period |
| `SCFD` | standard cubic feet per day |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf (23 pages, DOE/SC-ARM-TR-267, by J Uin, S Smith, O Mayol-Bracero, D De Oliveira)
- Catalog record: ARM data-source index, `instrument_class_code=tap`, read 2026-09-23
- Example file: `sgpaostapE13.b1.20180414.000000.nc` from `sgpaostapE13.b1`, 63.78 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
