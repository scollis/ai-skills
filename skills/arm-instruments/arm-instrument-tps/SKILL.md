---
name: arm-instrument-tps
description: ARM Total Precipitation Sensor (tps) - handbook-derived instrument reference. Measurement principle, reported quantities (Precipitation rate, Wind speed, Ambient Temperature, Atmospheric Pressure, Relative Humidity, Solar Radiation, Net Thermal Infrared Radiation, Accumulated liquid precipitation), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsatpsauxC1.b1) and the variable inventory of a real file. Use when working with tps data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - tps, Total Precipitation Sensor, nsatpsauxC1.b1, Precipitation rate, Wind speed, Ambient Temperature, Atmospheric Pressure, Relative Humidity, Solar Radiation, Surface Meteorology, "Yankee Environmental Systems, Inc., TB.DELTA, TBIN.DELTA.
---

# TPS - Total Precipitation Sensor

The TPS-3100 Total Precipitation Sensor uses a heated hotplate technique to measure instantaneous liquid equivalent precipitation rate, wind speed and ambient meteorological parameters, deployed unattended outdoors on a mounting post (e.g., at the ARM North Slope of Alaska site) without need for a wind shield.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 91 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `tps` |
| Handbook | [DOE/SC-ARM/TR-094 / "February 2011"](https://www.arm.gov/publications/tech_reports/handbooks/tps_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | "Yankee Environmental Systems, Inc., Model TPS-3100 Total Precipitation Sensor" |
| Primary measurements | Atmospheric temperature; Horizontal wind; Precipitation |
| Record | 2006-08-23 to 2014-05-21 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/tps |


## Credit

The handbook this skill derives from names no individual author on its cover;
it is issued by the ARM facility. The instrument knowledge in it is still the
mentor programme's work, not this file's:

> ARM Climate Research Facility. *Total Precipitation Sensor (TPS) Handbook*, DOE/SC-ARM/TR-094, "February 2011".
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tps_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The Hotplate sensor consists of two individually heated 5-inch diameter plates maintained at the same elevated temperature by precisely controlled electrical heaters; the top plate is exposed to precipitation while the shaded lower plate is not. By measuring the difference in power required to maintain both plates at the same elevated temperature, the instantaneous liquid equivalent precipitation rate (LER) is calculated, since the difference reflects the thermal energy needed to evaporate incident rain or snow off the top plate. Power delivered to the lower plate is used to factor out wind cooling effects, yielding a measurement of wind speed at the same location as the precipitation measurement. The instantaneous precipitation rate is thus derived from the power difference between the two plates after correction for both ambient temperature and wind speed. Auxiliary sensors for solar radiation, infrared radiation, pressure and humidity (added in 2010) provide internal corrections for edge-case conditions such as direct solar heating or nighttime radiative cooling of the top plate.

**Siting.** Requires an open, flat field with largely laminar wind flow; must not be installed near hills, earthen berms, stockade fences, buildings, stone walls, bushes, trees, or other tall structures, as these create wind turbulence for distances of about ten times their height, biasing the plates and creating false precipitation signals. Avoid mountain sides (anabatic/katabatic diurnal winds). Mount atop a vertical post secured in a concrete foundation poured below the local frost line, kept plumb and level; orient the sensor arm into the least likely prevailing wind direction (arm downwind) to minimize turbulence from the mount itself, and avoid rotating the sensor head more than 90 degrees about...

**Sampling.** native rate Continuous internal measurement; example drip test used 1 Hz data acquisition rate; reported every Configurable streaming interval 0-9999 seconds (0 disables streaming, returns to interactive/on-demand mode); interactive mode returns one record per 'T' command; averaging Internal algorithm uses both 1-minute and 5-minute running averages; onset of precipitation based on 5-minute average exceeding 0.25 mm/hr threshold, then output switches to 1-minute average with same threshold; wind speed and ambient temperature reported as 1-minute averages of instantaneous values; enclosure temperature is not averaged (hb p. 58).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Precipitation rate (Liquid Equivalent Rate, LER) | mm hr-1 | 0-50 mm hr-1 | ±0.5 mm hr-1 | 0.1 mm-hr-1 | (hb p. 21) |
| Wind speed | meter-sec-1 | 0-25 meter-sec-1 | ≈1 meter-sec-1 | - | (hb p. 21) |
| Ambient Temperature | °C | -50 to +50°C (per fault code... | 2% FS accuracy | - | (hb p. 21) |
| Atmospheric Pressure | milliBar | - | 2% FS accuracy | - | (hb p. 21) |
| Relative Humidity | % | - | 5% FS accuracy | - | (hb p. 21) |
| Solar Radiation | Watts-m2 | - | 5% FS accuracy | - | (hb p. 21) |
| Net Thermal Infrared Radiation (Tambient-to-sky) | Watts-m2 | - | 10% FS accuracy | - | (hb p. 21) |
| Accumulated liquid precipitation | mm | - | - | - | (hb p. 54) |
| Instrument enclosure temperature | °C | -50 to +100°C | - | - | (hb p. 66) |


## Specifications

| parameter | value | source |
|---|---|---|
| Power Required | 100/250 Vac, 50/60Hz, 1Φ; 100W typ, 680W max | (hb p. 21) |
| Weight | 17 lbs. (8 kg), not including mounting post | (hb p. 21) |
| Size | 72" (183cm) H; 22" (55cm) D; 8" (20cm) W | (hb p. 21) |
| Materials | Aluminum | (hb p. 21) |
| Digital I/O | RS-232, 9600 baud 8-N-1 ASCII | (hb p. 21) |
| Analog output | Simulated tipping bucket rain gauge output, Open Collector | (hb p. 21) |
| Measurement range | 0-50 mm hr-1 | (hb p. 21) |
| Liquid Equivalent Rate accuracy | ±0.5 mm hr-1 | (hb p. 21) |
| Time Constant | 1 minute | (hb p. 21) |
| Slew rate | ≈0.5 mm s-1 | (hb p. 21) |
| Repeatability | ±0.25 mm hr-1 | (hb p. 21) |
| Hysteresis |  | (hb p. 21) |
| Resolution | 0.1 mm-hr-1 | (hb p. 21) |
| Wind Speed | 0-25 meter-sec-1; accuracy ≈1 meter-sec-1 | (hb p. 21) |
| Auxiliary Met Measurements - Ambient Temperature | 2% FS accuracy (°C) | (hb p. 21) |
| Auxiliary Met Measurements - Atmospheric Pressure | 2% FS accuracy (milliBar) | (hb p. 21) |
| Auxiliary Met Measurements - Relative Humidity | 5% FS accuracy (%) | (hb p. 21) |
| Auxiliary Met Measurements - Solar Radiation | 5% FS accuracy (Watts-m2) | (hb p. 21) |
| Auxiliary Met Measurements - Net Thermal Infrared Radiation | 10% FS accuracy (Watts-m2), Tambient-to-sky | (hb p. 21) |
| Operating Temp range | ±50°C | (hb p. 21) |
| Initial Power on delay | 10 minutes (permits thermal stabilization) | (hb p. 21) |
| Running average period | 5 minutes, 1 minute | (hb p. 21) |
| Electrical Connections | Internal DB9 pin Female (DCE) RS-232, separate pulse output simulates tipping bucket sensor for data loggers with counter inputs. 6' (1.8m), AC line... | (hb p. 21) |


## The data

Verified example: **`nsatpsauxC1.b1`**, file `nsatpsauxC1.b1.20140518.000000.cdf`
(0.12 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 21 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2014-05-18T00:00:00 to 2014-05-18T23:59:00 |
| dod version | tpsaux-b1-1.1 |
| process version | ingest-tps-2.4-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `amps_max` | A | time | yes | Maximum current measured by the sensor |
| `amps_mean` | A | time | yes | Mean current measured by the sensor |
| `batt_volt_max` | V | time | yes | Battery voltage, maximum |
| `batt_volt_mean` | V | time | yes | Battery voltage, mean |
| `batt_volt_min` | V | time | yes | Battery voltage, minimum |
| `inst_batt_volt` | V | time | yes | Battery voltage, instantaneous |
| `inst_logger_temp` | degC | time | yes | Logger temperature, instantaneous |
| `logger_temp_mean` | degC | time | yes | Logger temperature, mean |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsatpsauxC1.b1", "2014-05-18", "2014-05-18")
ds = armlive_open("nsatpsauxC1.b1", "2014-05-18", "2014-05-18", cleanup_qc=True)
```

## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
21 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (nsatpsauxC1.b1.20140518.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `inst_logger_temp` | Value is equal to missing_value. | 1440 | 100.0 |
| `logger_temp_mean` | Value is equal to missing_value. | 1440 | 100.0 |
| `inst_batt_volt` | Value is equal to missing_value. | 1440 | 100.0 |
| `batt_volt_mean` | Value is equal to missing_value. | 1440 | 100.0 |
| `batt_volt_max` | Value is equal to missing_value. | 1440 | 100.0 |
| `batt_volt_min` | Value is equal to missing_value. | 1440 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsatpsauxC1.b1", "20060823", "20260923")
```

The handbook's own note on data quality: The electronics continuously monitor system status; a seven-digit binary Fault Indicator field in each output record flags critical faults (top plate, bottom plate, current, voltage, resistance, maximum/minimum value exceeded); a string of seven zeros indicates normal operation, seven ones indicates the 10-minute warm-up period. Critical faults disable the normal heater control algorithm and reduce power duty cycle to 1.5%, but still allow auxiliary A/D measurements for remote diagnosis. Non-critical faults (ambient temperature sensor fault) force precipitation rate and wind speed outputs to...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Heavy rain saturation / underreporting at high LER | During heavy hail or when liquid precipitation rate exceeds ~4" per hour, LER output data flat lines (saturates), an unnatural, visually obvious cue of out-of-range measurement; LER is... | Co-locate a conventional tipping bucket gauge with the system to capture high rain rate events | (hb p. 16) |
| Large hail underreporting | During heavy hail, larger particles ballistically bounce off the top plate and LER will be underreported | - | (hb p. 16) |
| High wind / blowing snow measurement error | If wind is blowing at gale force and snow is blowing horizontally, measurement accuracy suffers; wind cooling of lower plate misinterpreted | Use dual TPS systems at different heights with independent wind sensors to detect and correct for blowing snow | (hb p. 16) |
| Blowing snow contaminating lower (reference) plate | Lower plate power (used for wind correction) is affected by blowing snow contact, rendering wind correction inaccurate; wind speed retrieval biased | Deploy two TPS-3100 units at different heights (e.g., 2m and 10m) with independent calibrated wind sensors to detect and quantify blowing snow | (hb p. 18) |
| Daytime solar heating of top plate reduces sensitivity | During clear daytime precipitation events, direct sunlight heats top plate reducing measurement sensitivity | Auxiliary solar radiation sensor added in 2010 to provide internal correction | (hb p. 19) |
| Nighttime radiative cooling false precipitation signal | During cold cloudless nighttime periods, thermal emission from top plate to ~2.7K cosmic background cools top plate, causing system to falsely indicate light snow when none is occurring | Auxiliary net infrared radiation sensor added in 2010 to filter this edge case | (hb p. 19) |
| Site turbulence from nearby obstacles | Imbalance between plates misinterpreted as precipitation when it is really wind turbulence from buildings, walls, hills, vegetation, or towers | Site in open flat area away from buildings, walls, fences, vegetation, hills/slopes, berms, tall structures; avoid mountain sides due to... | (hb p. 27) |
| Turbulence from sensor's own support arm/mast | Wind arriving from the direction of the sensor arm creates turbulence artifacts | Orient sensor head arm into the least likely prevailing wind direction (arm downwind) | (hb p. 27) |
| Tilt/leveling error | Physical movement or tilt of the mounted sensor leads to measurement errors even though not damaging | Verify system remains level using bubble level; adjust mounting screws/flange bolts | (hb p. 31) |
| Nearby towers/structures dropping accumulated precipitation | Nearby towers create complex downwind turbulence and drop accumulated precipitation in random complex patterns around their bases, contaminating catch | Keep such structures far from sensor site | (hb p. 30) |
| Lightning-induced electrical damage | Sudden permanent system failure/data dropout after nearby lightning strike; semiconductor breakdown | Use optical isolation (fiber optic serial/Ethernet), metallic conduit, surge protection (MOV, spark gap), proper grounding with ground rods/mesh,... | (hb p. 35) |
| RTC battery discharge causing clock stoppage | If AC power lost and internal lithium coin battery discharged, real-time clock stops and requires reset; timestamps become invalid/frozen | Replace CR-2032 lithium battery every 5 years | (hb p. 56) |
| Ambient temperature sensor fault | Ambient temperature field reads fixed -50°C (disconnected) or +50°C (short-circuited); precipitation rate forced to zero, accumulated precipitation frozen at last valid value, wind speed... | Check wiring connection of external ambient temperature thermistor | (hb p. 65) |
| Top/bottom plate or electrical faults | Fault Indicator 7-digit binary code (e.g., 1010001) nonzero; flashing red LED (green off); system power duty cycle drops to 1.5% | Diagnose using fault code bit definitions (top plate, bottom plate, current, voltage, resistance, max/min value exceeded); repair or contact YES... | (hb p. 65) |
| Warm-up period after power-on/reset | Status/fault code reads all ones (1111111) for 10 minutes after power-up; no precipitation measured or output regardless of actual conditions; steady red LED | Wait for 10-minute warm-up to elapse before trusting data; can be used to detect unintended power cycling | (hb p. 53) |
| Enclosure temperature sensor out-of-range (non-critical) | Enclosure temperature reads -50°C (disconnected) or 100°C (short-circuited) but does not trigger a fault condition; can occur briefly in arctic winter after power restoration | Power supply has thermal cutout that fully shuts down system if interior overheats | (hb p. 66) |
| Internal averaging (boxcar) delay/bias at onset and cessation of precipitation | ~1 minute delay before non-zero precipitation rate reported after event onset for long-duration events; initial reported rate can slightly exceed true delivered rate; short-duration events... | - | (hb p. 76) |
| Repeated system resets increasing calibration uncertainty | Frequent thermal expansion/contraction from repeated warm-up cycles may eventually cause material failure, increasing calibration drift | Avoid issuing reset command repeatedly; leave system powered on continuously for highest calibration stability | (hb p. 64) |
| Streaming mode lockup with dialup/cellular modems | Modem misinterprets streaming data as escape command and never answers incoming calls again, even after power cycling | Use interactive mode with modems, or physically visit site and reset via terminal emulator to interactive mode; avoid streaming intervals less than... | (hb p. 58) |
| Pulse accumulator output limited information | Pulse output only provides accumulated precipitation, not instantaneous rate, ambient temp, wind, or diagnostics; masks underlying system problems | Use RS-232 serial interface instead for most accurate, information-rich measurements | (hb p. 27) |
| Cable/connector reversal at sensor head | If blue (top/sky) and brown (bottom/earth) sensor cables are swapped during reassembly, system data will be invalid | Carefully verify color-coded cable positions during reassembly (blue=top/sky, brown=bottom/earth) | (hb p. 71) |
| Water infiltration into electronics enclosure | Evidence of water inside enclosure; erratic or failed operation; voids warranty | Keep enclosure sealed; only open when absolutely necessary and never during precipitation; properly reseat O-ring gasket on reassembly | (hb p. 24) |
| Wild/domestic animal damage to cabling or enclosure | Chewed/damaged cables from wolves, coyotes, or overturning forces from bear/elk/deer/livestock scratching on enclosure | Use armored Seal-tite conduit for cables; fence in system in open range areas | (hb p. 39) |
| GFCI false tripping from lightning noise | Power loss to system apparently unrelated to actual electrical fault, coincides with nearby lightning | Avoid GFCIs; use traditional circuit breaker plus MOV/spark gap surge suppression | (hb p. 39) |


_5 further items in the handbook._

## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Factory calibration via measurement of current, voltage and temperature of each sensor head under a variety of conditions, verified in a well-controlled environment in a small wind tunnel; NCAR has compared systems against reference precipitation gauges at a well-controlled field site to arrive at final calibration of... (hb p. 69) |
| Calibration interval | Preferably yearly, at least every two years (per Routine Maintenance: 'Periodic Calibration') (hb p. 69) |
| Traceability | Each sensor head is individually calibrated at the factory; comparisons against NCAR reference precipitation gauges (hb p. 69) |
| Routine maintenance | Seasonally: check plates for debris (grey oxidation is normal, do not use abrasives). Yearly: clean plates with mild solution (e.g., Windex) and soft cloth; inspect AC and data cables for wind-wear or animal damage. Every 5 years: replace 3V lithium CR-2032 coin battery on main PCB. Periodic factory calibration... (hb p. 68) |
| Maintenance interval | Seasonal/yearly/5-yearly as itemized; calibration yearly to biennially (hb p. 68) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Double Fenced Intercomparison Rain gauge (DFIR), YES TSI Total Sky Imager, YESDAS-2 Data Acquisition System, YES Opti-Grid switch, conventional tipping bucket rain gauge, weighing-type rain gauge.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `LER` | Liquid Equivalent Rate - instantaneous rate of precipitation expressed as equivalent... |
| `TPS` | Total Precipitation Sensor |
| `RTC` | Real-time clock, used to timestamp data records and periodically reset accumulated... |
| `DMS` | Data Management System |
| `PLC` | Programmable Logic Controller |
| `CRC` | Cyclical Redundancy Check, a checksum appended to each data record to verify data... |
| `DCE` | Data Communications Equipment (the system's serial port configuration) |
| `DTE` | Data Terminal Equipment (typical PC serial port configuration) |
| `TB.DELTA` | Parameter setting the amount of precipitation (in micrometers) represented by each... |
| `TBIN.DELTA` | Parameter multiplying tipping bucket input contact closures to yield precipitation amount... |


### References the handbook cites

- Numerical Recipes in C, Cambridge University Press (CRC-16 algorithm reference)
- AMS Glossary of Meteorology (p.695) (snow density/specific density reference)
- Horowitz & Hill's The Art of Electronics, ISBN: 0521370957, 3rd edition (RS-232 tutorial reference)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tps_handbook.pdf (91 pages, DOE/SC-ARM/TR-094, no individual author named on the cover)
- Catalog record: ARM data-source index, `instrument_class_code=tps`, read 2026-09-23
- Example file: `nsatpsauxC1.b1.20140518.000000.cdf` from `nsatpsauxC1.b1`, 0.12 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
