---
name: arm-instrument-tap-air
description: ARM Tricolor Absorption Photometer aboard aircraft (tap-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol light absorption), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafstapU2.b1) and the variable inventory of a real file. Use when working with tap-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - tap-air, Tricolor Absorption Photometer aboard aircraft, bnfaafstapU2.b1, Aerosol light absorption, Aerosols, Airborne Observations, AOS07, PSAP, CAPS, Neph, Dry.
---

# TAP-AIR - Tricolor Absorption Photometer aboard aircraft

This handbook documents the SGP Aerosol Observing System (AOS07), a shipping-container-based ground aerosol sampling facility; the tricolor absorption photometer (TAP), described here in its ground TAP form, measures three-wavelength aerosol light absorption from an aerosol sample drawn through the AOS inlet, and no TAP-air (aircraft) specific content is present in this parent handbook.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tap-air` |
| Handbook | [DOE/SC-ARM-TR-267 / J Uin, S Smith, O Mayol-Bracero, D De Oliveira / April 2025](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | TAP = tricolor absorption photometer (Brechtel Manufacturing Inc.) |
| Primary measurements | Aerosol absorption |
| Record | 2021-03-03 to 2026-09-16 (active) |
| Datastreams with data | 5 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tap-air |


## Credit

Everything this skill knows about the instrument is the work of **J Uin, S Smith, O Mayol-Bracero, D De Oliveira** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin, S Smith, O Mayol-Bracero, D De Oliveira. *Southern Great Plains (SGP) Aerosol Observing System (AOS) Instrument Handbook*, DOE/SC-ARM-TR-267, April 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tap-air`, ARM links no handbook to this class. The facts below come from the **Tricolor Absorption Photometer** (`tap`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tap-air` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

The handbook states that the PSAP and TAP measure light absorption, while the nephelometers measure light scattering and the CAPS measures light extinction (the sum of scattering and absorption); these three radiative parameters are used to quantify how aerosols affect visibility and radiation transfer in the atmosphere and depend on aerosol particle size, with larger particles scattering more light than smaller ones. Sample air enters via the aerosol inlet stack, is drawn through a polished 2-inch center pipe to a five-port flow distributor, and is conditioned (e.g., via an impactor selecting 1-micrometer or 10-micrometer size cuts) before reaching instruments such as the TAP. No aircraft-specific (tap-air) measurement principle, deployment description, or distinguishing detail is given anywhere in this parent handbook; all TAP-related text describes the ground-based AOS07 configuration only.

**Siting.** The handbook describes only the ground-based SGP AOS07 aerosol inlet and sample distribution siting: an 8-inch aluminum irrigation-pipe stack ~20 feet tall with a heated rain hat and WXT520 weather station on top, feeding a five-port flow distributor with an impactor (1 or 10 micrometer size cut) upstream of instruments such as the TAP; downstream instrument placement (including guest instruments) is coordinated with the AOS mentor to avoid biasing standard measurements. No aircraft-platform siting or orientation requirements for tap-air are stated in this handbook.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol light absorption (TAP) | - | - | - | - | (hb p. 7) |


## The data

Verified example: **`bnfaafstapU2.b1`**, file `bnfaafstapU2.b1.20260911.144750.nc`
(1.09 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=7477 |
| Data variables | 40 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-11T14:47:50 to 2026-09-11T16:52:26 |
| dod version | aafstap-b1-1.0 |
| process version | ingest-aafstapcorr-1.0-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `sample_flow` | L/min | time | yes | Sample flow rate, volumetric |
| `temperature` | degC | time | yes | Ambient sample flow temperature |
| `Ba_B` | 1/Mm | time | - | Aerosol light absorption coefficient, nominal blue wavelength at... |
| `Ba_G` | 1/Mm | time | - | Aerosol light absorption coefficient, nominal green wavelength at... |
| `Ba_R` | 1/Mm | time | - | Aerosol light absorption coefficient, nominal red wavelength at... |
| `Ba_calculation_interval` | s | time | - | Time interval used by the instrument to calculate the nominal aerosol... |
| `blue_intensity_reference` | 1 | time | - | Raw intensity, blue minus dark, reference |
| `blue_intensity_sample` | 1 | time | - | Raw intensity, blue minus dark, sample |
| `dark_intensity_reference` | 1 | time | - | Raw intensity, LEDs off (dark), reference |
| `dark_intensity_sample` | 1 | time | - | Raw intensity, LEDs off (dark), sample |
| `filter_size_area` | mm^2 | - | - | Filter size area |
| `filter_state` | 1 | time | - | Filter state |
| `flow_setpoint` | L/min | time | - | Flow setpoint |
| `green_intensity_reference` | 1 | time | - | Raw intensity, green minus dark, reference |
| `green_intensity_sample` | 1 | time | - | Raw intensity, green minus dark, sample |
| `initial_blue_intensity_reference` | 1 | - | - | Initial intensity reading through white filter, blue minus dark,... |
| `initial_blue_intensity_sample` | 1 | - | - | Initial intensity reading through white filter, blue minus dark,... |
| `initial_dark_intensity_reference` | 1 | - | - | Initial intensity reading through white filter, LEDs off (dark),... |
| `initial_dark_intensity_sample` | 1 | - | - | Initial intensity reading through white filter, LEDs off (dark),... |
| `initial_green_intensity_reference` | 1 | - | - | Initial intensity reading through white filter, green minus dark,... |
| `initial_green_intensity_sample` | 1 | - | - | Initial intensity reading through white filter, green minus dark,... |
| `initial_red_intensity_reference` | 1 | - | - | Initial intensity reading through white filter, red minus dark,... |
| `initial_red_intensity_sample` | 1 | - | - | Initial intensity reading through white filter, red minus dark, sample |
| `power_supply` | V | time | - | Power supply voltage |
| `pressure` | hPa | time | - | Ambient sample flow pressure |
| `pump_power` | 1 | time | - | Pump power, duty cycle |
| `red_intensity_reference` | 1 | time | - | Raw intensity, red minus dark, reference |
| `red_intensity_sample` | 1 | time | - | Raw intensity, red minus dark, sample |
| `stap_errors` | 1 | time | - | Bit-packed error codes |
| `stap_state` | 1 | time | - | STAP on/off state (STAP control) |


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
                     params={"user": f"{user}:{token}", "ds": "bnfaafstapU2.b1",
                             "start": "2026-09-11", "end": "2026-09-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaafstapU2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaafstapU2.b1", "2026-09-11", "2026-09-11")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaafstapU2.b1", "2026-09-11", "2026-09-11"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("Ba_R")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
40 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_sample_flow"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("sample_flow", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["sample_flow", "temperature", "lat"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (bnfaafstapU2.b1.20260911.144750.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sample_flow` | Value is greater than fail_max. | 6 | 0.0802 |
| `sample_flow` | Value is less than fail_min. | 1 | 0.0134 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("bnfaafstapU2.b1", "20210303", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Operators fill out daily log sheets covering each instrument and AOS systems as provided by mentors. Sample line integrity checks (HEPA-filter zero check) are performed at defined intervals to catch leaks; every connection is treated as a potential single point of failure. Housekeeping data (temperature, RH, pressure, voltage, vacuum) are recorded and displayed via a virtual instrumentation (VI) display on the AOS personal computer for system monitoring.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sample line leaks | Instrument readings deviate from zero when sample line is capped with a HEPA filter during an integrity check; potential single point of failure at every connection | Perform sample line integrity checks: remove sample line from stack, place HEPA filter on stack end, confirm each connected instrument reads zero;... | (hb p. 21) |
| Temperature/RH change of sample air in inlet lines | Measured T/RH of inlet sample air deviates from ambient despite insulation, monitored via Omega T/RH sensor and PID | Lines are insulated to prevent water condensation in sample lines; T/RH is monitored and logged via PID | (hb p. 9) |
| Ice buildup around inlet edge | Would appear as flow restriction or blockage at inlet rain cover edge in cold conditions | 1-inch wide, 175-watt band heater around rain cover edge, controlled to 5 degC via Omega PID, prevents ice buildup | (hb p. 3) |
| Water condensation in sample lines | Would appear as unexpected moisture/flow anomalies in sample lines | Flow distributor and conductive tubing are insulated to prevent water condensation | (hb p. 7) |
| Particle size bias in absorption/scattering/extinction measurements | Radiative parameters (scattering, absorption, extinction) vary depending on whether light is affected by a large number of small particles or a small number of large particles | An impactor (1 micrometer or 10 micrometer cut) upstream of instruments including TAP helps determine size-dependent contribution | (hb p. 7) |
| Guest instrument sample line bias | Addition of guest instruments into the sample distribution system could bias standard measurements if not properly flow-balanced | Instrument mentors coordinate placement with AOS mentor; flow rate in modified sample line adjusted to compensate for additional instrumentation | (hb p. 7) |
| Power interruption/bumps at SGP site | Instrument power loss or brief outages visible as gaps in data during power bumps | UPS absorbs expected power bumps and keeps instruments on for about 30 minutes | (hb p. 12) |
| Overheating of pumps/blowers/air drier in blower enclosure | Elevated temperature readings from pump/blower/air-drier temperature sensors in housekeeping data | Four 10-inch fans circulate air into/out of enclosure; temperatures monitored as part of housekeeping measurements | (hb p. 5) |
| Rust/corrosion of structure and hardware | Visible rust on exterior structure, door hinges, door knob mechanism | Monthly inspection; scrape, clean, and apply touch-up paint as needed; grease/oil hinges every three months | (hb p. 16) |
| Guy wire tension loss over time | Uneven cable tension compared to other guy wires supporting the aerosol inlet stack | Check cables for rubbing/frayed wires and confirm similar tension; adjust turnbuckles as needed | (hb p. 17) |


## Calibration and maintenance

|  |  |
|---|---|
| Routine maintenance | Monthly: check exterior of structure for rust and touch up paint as needed; check door hinges for wear/rust and grease/oil every three months; inspect door knob mechanism and clean/oil/tighten as needed; inspect roof railing bolts and pins for tightness and wear; check railing gate swings freely and latch engages... (hb p. 16) |
| Maintenance interval | Monthly (structure/rust check); every three months (door hinges) (hb p. 16) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: PSAP (particle soot absorption photometer), CAPS (cavity attenuated phase shift monitor), Neph, Dry (nephelometer), Neph, Wet (nephelometer), ACSM, APS, CCN-200, CPCf, CPCu, n-SMPS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOS` | Aerosol Observing System |
| `AOS07` | SGP AOS (designation for this specific system) |
| `TAP` | tricolor absorption photometer (Brechtel Manufacturing Inc.) |
| `PSAP` | particle soot absorption photometer (Radiance Research) |
| `CAPS` | cavity attenuated phase shift monitor (Aerodyne Research Inc.) |
| `Neph, Dry` | nephelometer, ambient RH (TSI Inc.) |
| `PID` | proportional, integral, derivative controller |
| `VI` | virtual instrumentation |
| `VM` | virtual machine (computer) |
| `IOP` | intensive operational period |
| `SCFD` | standard cubic feet per day |
| `PDU` | power distribution unit |
| `RTD` | resistance temperature detector |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-267.pdf (23 pages, DOE/SC-ARM-TR-267, by J Uin, S Smith, O Mayol-Bracero, D De Oliveira)
- Catalog record: ARM data-source index, `instrument_class_code=tap-air`, read 2026-09-24
- Example file: `bnfaafstapU2.b1.20260911.144750.nc` from `bnfaafstapU2.b1`, 1.09 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
