---
name: arm-instrument-cmh-air
description: ARM Chilled Mirror Hygrometer aboard aircraft (cmh-air) - handbook-derived instrument reference: measurement principle, reported quantities (Dew/frost point temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafdewpointF1.b1) and the variable inventory of a real file. Use when working with cmh-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations; Atmospheric Profiling. Triggers - cmh-air, Chilled Mirror Hygrometer aboard aircraft, sgpaafdewpointF1.b1, Dew/frost point temperature, Airborne Observations, Atmospheric Profiling, GE-1011B from General Eastern, ACE-ENA, AIMMS, CACTI, HI-SCALE.
---

# CMH-AIR - Chilled Mirror Hygrometer aboard aircraft

The CMH-AIR is an airborne hygrometer mounted on the ARM Aerial Facility's G-1 aircraft that detects dew or frost point by cooling a reflective mirror until condensation forms, sensed optically, to determine atmospheric moisture.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cmh-air` |
| Handbook | [DOE/SC-ARM-TR-235 / L Goldberger / December 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-235.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling |
| Manufacturer / model | GE-1011B from General Eastern; newest iteration from Buck Research Instruments LLC (Model 1011C) |
| Primary measurements | Atmospheric moisture |
| Record | 2016-04-25 to 2026-09-23 (retired) |
| Datastreams with data | 6 across 3 sites |
| Sites | cor, ena, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/cmh-air |


## Credit

Everything this skill knows about the instrument is the work of **L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Goldberger. *Chilled Mirror Hygrometer Aboard Aircraft (CMH-AIR) Instrument Handbook*, DOE/SC-ARM-TR-235, December 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-235.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Air is sampled via an inlet and flowed over a chilled mirror (polished hexagonal rhodium, stainless steel, or platinum) whose temperature is controlled by a Peltier cooling module. A servo controller applies current to the Peltier to cool the mirror, and an ultra-stable thermistor imbedded in the mirror measures its temperature. The mirror is illuminated with a regulated LED and reflected light is received by a photodiode; as water vapor condenses as water or frost, the light measured by the photodiode is reduced due to scattering. The servo and control system modulate mirror temperature to maintain a constant rate of condensation and evaporation so the mass of water on the mirror stays constant, at which point the mirror temperature equals, by definition, the dew or frost point temperature. The vapor pressure formulations used in the instrument's development are described in Buck et al. 1981.

**Siting.** The sensing unit comes with an inlet fitting including inlet, exhaust, and water drain ports, designed for either the left or right side of the aircraft. Shock mounts are not necessary for aircraft operations per the manufacturer. For initial setup, the inlet should be placed where the sensor pressure is near static pressure. An optional aspirating kit provides airflow through the sensor when the aircraft is not in flight or in the lab; a sampling pump can also be used.

**Sampling.** native rate RS-232 output at 9600 Baud with resolution 0.01 deg C (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Dew/frost point temperature | deg C | -75 to +50 deg C, dewpoint depression... | +/- 0.1 deg C | 0.01 deg C on RS-232 output | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | degrees Celsius | (hb p. 11) |
| Range | -75 to +50 deg C, dewpoint depression up to 85 deg C | (hb p. 11) |
| Sample pressure range | 0 to 1100 mb | (hb p. 11) |
| Required flow rate | 0.23 to 3 liters per minute (LPM) | (hb p. 11) |
| Calibration accuracy range | +/- 0.1 deg C | (hb p. 11) |
| Repeatability check standards (dewpoint temps) | 11.78, 5.19, -11.74, and -27.87 deg C | (hb p. 11) |
| Slew rate | typically 1 deg C/s | (hb p. 11) |
| Resolution | 0.01 deg C on RS-232 output | (hb p. 11) |
| Calibration uncertainty | +/- 0.1 deg C on analog and RS-232 outputs | (hb p. 12) |
| Input Voltage | 28 VDC | (hb p. 12) |
| Input Values |  | (hb p. 12) |
| Output Values | 0-10V and 4-20 mA scaleable analog outputs; dewpoint conversion 0.08 v/deg C, where 6v = 0 deg C | (hb p. 12) |
| Operating temperature range - Sensing unit | -80 to +60 °C | (hb p. 16) |
| Operating temperature range - Control/indicator unit | -40 to +60 °C | (hb p. 16) |
| Operating temperature range - Power unit | -40 to +60 °C | (hb p. 16) |
| Airspeed (nominal) | 450 knots | (hb p. 16) |
| Altitude (nominal) | 45,000 feet | (hb p. 16) |
| Pressure limit | 1.5 atmospheres | (hb p. 16) |
| Serial output | 9600 Baud | (hb p. 16) |


## The data

Verified example: **`sgpaafdewpointF1.b1`**, file `sgpaafdewpointF1.b1.20160920.202752.nc`
(0.31 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5108 |
| Data variables | 10 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:52 to 2016-09-20T21:52:59 |
| dod version | aafdewpoint-b1-1.0 |
| process version | ingest-aafdewpointcorr-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `dewpoint_temperature` | degC | time | yes | Dewpoint temperature |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaafdewpointF1.b1", "2016-09-20", "2016-09-20")
ds = armlive_open("sgpaafdewpointF1.b1", "2016-09-20", "2016-09-20", cleanup_qc=True)
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
10 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaafdewpointF1.b1", "20160425", "20260923")
```

The handbook's own note on data quality: Data is quality controlled (QCd) by the mentor after an IOP-based field deployment before submission to the ARM Data Center. The dataset is compared to and validated by auxiliary measurements (relative and specific humidity, vapor mixing ratio, water vapor density, vapor pressure, dewpoint) taken by the AIMMS probe onboard the aircraft. Generally during level flight, reported changes in dew/frost points should be accurate; however, responses under icing conditions, sudden transitions from low to high dewpoints, and aircraft descent into warm, moist air should be analyzed closely. Data quality...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Mirror contamination | Rebalanced LED does not shut off, indicating the mirror needs cleaning; Service Mirror LED flashes when mirror is too contaminated for operation and requires immediate cleaning | Clean the mirror per maintenance procedure using cotton swab with approved solvent (acetone followed by water); reduced flow rates used to minimize... | (hb p. 15) |
| Slow response at low dew points | Response (slew rate, typically 1 deg C/s) can be reduced to minutes when dew points are low and there is a greater difference between mirror temperature and housing temperature; reduced... | Maximize flow over the mirror and ensure sensor case temperature is kept as close to ambient temperature as possible | (hb p. 11) |
| Icing conditions | Reported changes in dew/frost points may not be accurate during icing conditions | Analyze responses under these conditions closely; compare to AIMMS auxiliary measurements | (hb p. 10) |
| Sudden transitions from low to high dewpoints | Reported changes in dew/frost point may lag or be inaccurate during rapid dewpoint transitions | Analyze responses under these conditions closely | (hb p. 10) |
| Aircraft descent into warm, moist air | Reported dew/frost point changes should be analyzed closely, as accuracy may be reduced compared to level flight | Compare to AIMMS auxiliary measurements; analyze closely | (hb p. 10) |
| Dewpoint depression limit / mirror cooling capability | Instrument cannot report dew point below the minimum achievable given ambient temperature; shown in depression capability figure | Reducing the CMH's temperature allows lower dew points to be measured | (hb p. 14) |
| Analog output drift | Analog electronics may be susceptible to drift over time affecting analog output values | Temperature is measured via ADC calibrated each time instrument is turned on, which is not susceptible to drift like the analog electronics | (hb p. 8) |
| Balance cycle interruption of data | During 'Balance' mode (heating mirror to 40 deg C to evaporate condensation) or initial balance cycle at power-up, no valid dew/frost point is output; serial line shows 0 in the third... | Wait for D/F Point LED to light up indicating stabilization on a dew or frost point before treating data as valid | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated by the vendor using four NIST-traceable standards; NIST-traceable calibration equipment checked humidity standard (DewPrime 1 by Edgetech and CR-3 Cryogenic Hygrometer by Buck Research Instruments), temperature standard (Platinum RTD by Logan), voltage standard (two 34401A voltage standards by Agilent and... (hb p. 16) |
| Calibration interval | Latest calibration by vendor was August 2019; return instrument to vendor for NIST calibrations (hb p. 16) |
| Traceability | NIST-traceable standards at dewpoint temperatures 11.78, 5.19, -11.74, and -27.87 deg C, resulting uncertainty of +/- 0.10 deg C (hb p. 16) |
| Routine maintenance | Perform periodic inspections of the system; check for damage on cables, connectors, o rings, gaskets, front panel switches, system optics, and mounting hardware; clean, lubricate, and replace damaged parts. Clean mirror using supplied cotton swab moistened with an approved solvent such as acetone followed by water;... (hb p. 17) |
| Maintenance interval | annually and before campaigns (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AIMMS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ADC` | analog-to-digital converter |
| `AIMMS` | aircraft-integrated meteorological measurement system |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `CMH` | chilled mirror hygrometer |
| `DP` | dew or frost point in deg C |
| `DQ` | data quality |
| `e` | vapor pressure in millibars |
| `es` | saturation vapor pressure in millibars |
| `G-1` | Gulfstream 159 aircraft |
| `HI-SCALE` | Holistic Interactions of Shallow Clouds, Aerosols, and Ecosystems |
| `IOP` | intensive operational period |


### References the handbook cites

- Buck, AL. 1981. "New equations for computing vapor pressure and enhancement factor." Journal of Applied Meteorology 20(12): 1527−1532, https://doi.org/10.1175/1520-0450(1981)020less than 1527:NEFCVPgreater than 2.0.CO;2
- Buck Research Instruments LLC. 2009. 1011C Chilled Mirror Aircraft Hygrometer Brochure.
- Buck Research Instruments LLC. 2009. Model 1011C Hygrometer Operating Manual.
- General Eastern Instruments. 1987. Model 1011B Dew Point Hygrometer for Aircraft Preliminary Operating Manual. Revision A.
- General Eastern Instruments. 2006. GE_Chilled_Mirror_Theory_Etc.pdf

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-235.pdf (18 pages, DOE/SC-ARM-TR-235, by L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=cmh-air`, read 2026-09-23
- Example file: `sgpaafdewpointF1.b1.20160920.202752.nc` from `sgpaafdewpointF1.b1`, 0.31 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
