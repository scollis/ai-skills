---
name: arm-instrument-tbswind
description: ARM Anemometers aboard Tethered Balloon System (tbswind) - handbook-derived instrument reference. Measurement principle, reported quantities (Horizontal wind speed, Vertical wind speed, Wind Direction, GPS Position, 3D Sonic Wind Speed, Wind gust speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbswindC1.b1) and the variable inventory of a real file. Use when working with tbswind data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Profiling. Triggers - tbswind, Anemometers aboard Tethered Balloon System, sgptbswindC1.b1, Horizontal wind speed, Vertical wind speed, Wind Direction, GPS Position, 3D Sonic Wind Speed, Wind gust speed, Airborne Observations, Atmospheric Profiling, NRG Systems 40H Anemometer (cup, horizontal), ADS-B.
---

# TBSWIND - Anemometers aboard Tethered Balloon System

The tbswind anemometers (NRG Systems 40H cup anemometer and RM Young 27106T vertical propeller anemometer, with wind direction from Tallysman HC872 helical antennas and a Hemisphere GNSS Vega 28 compass board) are mounted on a wind sensor boom flown aboard the ARM Tethered Balloon System to measure horizontal wind speed, vertical wind speed, and wind direction at 1 Hz at variable altitudes below cloud base.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbswind` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling |
| Manufacturer / model | NRG Systems 40H Anemometer (cup, horizontal); RM Young 27106T Vertical Anemometer (propeller); Tallysman HC872 Helical Antennas; Hemisphere GNSS Vega 28 compass board; LI-COR LI-560 Trisonica Sphere... |
| Primary measurements | Horizontal wind; Vertical velocity |
| Record | 2018-07-02 to 2026-09-24 (active) |
| Datastreams with data | 22 across 6 sites |
| Sites | bnf, crg, guc, hou, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbswind |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbswind`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbsins`, `tbslws`, `tbsmet`, `tbspops`, `tbsslwc`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbswind` until checked against that document's own section for it.

## How it measures

The tbswind datastream measures horizontal wind speed and gust speed using an NRG 40H cup anemometer and vertical wind speed using an RM Young 27106T propeller anemometer, both sampled at 1 Hz. Wind direction is derived from two Tallysman HC872 helical antennas separated by 1 m combined with a Hemisphere GNSS Vega 28 compass board, which also provides IMU (pitch, roll) data. Because the wind sensor boom itself ascends and descends on the balloon tether, the vertical_wind variable is corrected by subtracting an offset for the boom's own ascent/descent rate, calculated from the altitude change reported by the Vega 28 compass board. Each wind sensor boom is co-located with an iMet XQ2 sensor to provide simultaneous temperature, relative humidity, and pressure at the same altitude as the wind measurement. This cup/propeller-based tbswind system (1 Hz) is distinguished from the sonic-based tbsmet/tbswind3d system, which reports 3D sonic wind speed at 60 Hz and IMU/wind-direction data at 50 Hz for higher-frequency turbulence estimates.

**Siting.** Wind sensor booms are mounted on the TBS tether and may be operated at different altitudes with multiple booms on the same flight; each boom is paired with an iMet XQ2 sensor for co-located temperature, relative humidity, and pressure. Tether angle from zenith is not allowed to exceed 45 degrees in flight, and deviation from zenith increases with wind speed, which affects the true altitude/position of the wind sensor relative to the ground track. Flights are generally conducted 152 m (500') below cloud base, in 3 sm or greater visibility, to a maximum altitude of 1.5 km (4,921') agl unless otherwise authorized; aerostats are not launched in sustained surface winds above 10 m/s and flights...

**Sampling.** native rate 1 Hz (cup/propeller anemometers, tbswind); 60 Hz sonic wind speed and 50 Hz IMU/wind direction (tbsmet); reported every 1 second per sample; averaging 3-minute and 30-minute means of GPS position and acceleration used to provide motion-corrected turbulence estimates in tbswind3d; turbulent kinetic energy estimates generated from higher-frequency tbsmet wind speed data (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Horizontal wind speed | m/s | 1-96 | +/- 0.1 | 0.765 | (hb p. 13) |
| Vertical wind speed | m/s | 0-25 | +/- 1 % | 0.4 | (hb p. 13) |
| Wind Direction | degrees | 0-360 | +/- 0.08 | 0.1 | (hb p. 13) |
| GPS Position | - | - | ≥ 8 mm | 1 ppm | (hb p. 13) |
| 3D Sonic Wind Speed (tbsmet) | m/s | 0-50 | +/- 1 % | 0.01 m/s | (hb p. 13) |
| Wind gust speed (wind_gust) | m/s | - | - | - | (hb p. 19) |


## Specifications

| parameter | value | source |
|---|---|---|
| Horizontal wind speed (m/s) - Resolution | 0.765 | (hb p. 13) |
| Horizontal wind speed (m/s) - Accuracy | +/- 0.1 | (hb p. 13) |
| Horizontal wind speed (m/s) - Range | 1-96 | (hb p. 13) |
| Horizontal wind speed (m/s) - Response Time | less than 1 s | (hb p. 13) |
| Vertical wind speed (m/s) - Resolution | 0.4 | (hb p. 13) |
| Vertical wind speed (m/s) - Accuracy | +/- 1 % | (hb p. 13) |
| Vertical wind speed (m/s) - Range | 0-25 | (hb p. 13) |
| Vertical wind speed (m/s) - Response Time | less than 1 s | (hb p. 13) |
| Wind Direction (°) - Resolution | 0.1 | (hb p. 13) |
| Wind Direction (°) - Accuracy | +/- 0.08 | (hb p. 13) |
| Wind Direction (°) - Range | 0-360 | (hb p. 13) |
| Wind Direction (°) - Response Time | 0.1 s | (hb p. 13) |
| GPS Position - Resolution | 1 ppm | (hb p. 13) |
| GPS Position - Accuracy | ≥ 8 mm | (hb p. 13) |
| GPS Position - Response Time | 0.1 s | (hb p. 13) |
| 3D Sonic Wind Speed (m/s) - Resolution | 0.01 m/s | (hb p. 13) |
| 3D Sonic Wind Speed (m/s) - Accuracy | +/- 1 % | (hb p. 13) |
| 3D Sonic Wind Speed (m/s) - Range | 0-50 | (hb p. 13) |
| 3D Sonic Wind Speed (m/s) - Response Time | 0.02 s | (hb p. 13) |
| Number of wind sensor booms available | Thirteen | (hb p. 12) |
| tbswind sampling rate | 1 Hz | (hb p. 12) |
| tbsmet sonic wind sampling rate | 60 Hz | (hb p. 12) |
| tbsmet IMU and wind direction sampling rate | 50 Hz | (hb p. 12) |


## The data

Verified example: **`sgptbswindC1.b1`**, file `sgptbswindC1.b1.20241111.170031.nc`
(1.31 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=13467, `num_anem`=1 |
| Data variables | 24 |
| QC variables | 10 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2024-11-11T17:00:31 to 2024-11-11T20:44:58 |
| dod version | tbswind-b1-3.1 |
| process version | ingest-tbswindcorr-1.2-1.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pitch` | degree | time,num_anem | yes | Pitch from compass module |
| `pulse_count` | count | time,num_anem | yes | Pulse count |
| `roll` | degree | time,num_anem | yes | Roll from compass module |
| `vertical_wind` | m/s | time,num_anem | yes | Vertical wind component |
| `wind_direction` | degree | time,num_anem | yes | Wind direction |
| `wind_gust` | m/s | time,num_anem | yes | Wind gust |
| `wind_speed` | m/s | time,num_anem | yes | Wind speed |
| `anem_file_name` | 1 | num_anem | - | Anemometer file names |
| `serial_number` | 1 | num_anem | - | Serial number of anemometers |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgptbswindC1.b1", "2024-11-11", "2024-11-11")
ds = armlive_open("sgptbswindC1.b1", "2024-11-11", "2024-11-11", cleanup_qc=True)
```

## Quality control in this datastream

10 `qc_` companion variables cover 10 of the
24 data variables. Assessments present in the example file: `Bad`.

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
act.qc.print_dqr("sgptbswindC1.b1", "20180702", "20260924")
```

The handbook's own note on data quality: Each datastream includes quality control variables for each scientific variable, per the handbook's general Data section statement covering all TBS datastreams including tbswind.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Tether angle deviation from zenith with increasing wind speed | Reported wind sensor position/altitude deviates from vertical tether assumption; tether angle not allowed to exceed 45° in flight, so high-wind flights may show truncated altitude range or... | Flights constrained so tether angle does not exceed 45°; flights suspended if winds aloft exceed 14 m/s | (hb p. 9) |
| Boom ascent/descent motion contaminating vertical wind measurement | Raw vertical_wind values would be biased by the boom's own vertical motion during ascent/descent through the atmosphere | vertical_wind is corrected by applying an offset for the calculated change in altitude reported by the Vega 28 compass board | (hb p. 19) |
| Difference in temporal resolution between tbswind (cup/propeller, 1 Hz) and tbsmet... | Turbulence estimates and short-timescale gusts differ depending on which datastream (tbswind vs. tbswind3d/tbsmet) is used; direct comparison of the two datastreams may show discrepancies... | Use tbswind3d turbulent kinetic energy estimates (from 60 Hz sonic data) for turbulence; use tbswind for standard 1 Hz cup/propeller wind speed | (hb p. 12) |
| Wind speed sensor heading/calibration drift | Wind direction readings offset from true bearing if not checked | Heading checks performed against reference compass bearing at start of each field campaign | (hb p. 21) |
| Wind speed sensor calibration drift (NRG 40H cup anemometer) | Cup anemometer wind speed diverges from ground-truth tbsground sensor reading | Compared daily at start of flight day with tbsground reference output | (hb p. 21) |
| Variable payload/altitude range due to changing science payload and flight strategy | Data availability and sensor combinations on wind sensor booms vary by flight and campaign; not all variables present on every flight | Individual components of the system may change with each flight based on desired measurements, atmospheric conditions, operating location, and flight... | (hb p. 9) |
| Aerostat lift/tension change with altitude affecting tether/flight stability | Line tension decreases with altitude (~1% net lift loss per ~100 m above mean sea level during descent), potentially affecting boom stability and thus wind measurement quality at higher... | none stated | (hb p. 2) |
| Restricted flight envelope (cloud-relative altitude ceiling, visibility, wind limits) | No wind data collected above ~1.5 km agl or during high winds/low visibility; data gaps correspond to weather constraints | Flights conducted per FAA Certificate of Authorization constraints | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Vendor calibration; wind sensor booms undergo heading checks at the start of each field campaign against a reference compass bearing; at the start of each flight day, wind speed reported by each NRG 40H cup anemometer planned for flight is compared with the reference output reported by tbsground sensors (hb p. 21) |
| Calibration interval | Annually (NRG 40H cup anemometer, NRG IceFree3 anemometer, RM Young 27106T anemometer - vendor calibration); heading checks at start of each field campaign; daily comparison checks at start of each flight day (hb p. 21) |
| Traceability | Vendor calibration mode (hb p. 21) |
| Routine maintenance | Wind sensor booms undergo heading checks at the start of each field campaign against a reference compass bearing; NRG 40H cup anemometer wind speed compared daily against tbsground reference at start of each flight day (hb p. 21) |
| Maintenance interval | Start of each field campaign (heading check); start of each flight day (comparison check); Annually (vendor calibration) (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: tbsmet (sonic wind, LI-COR LI-560 Trisonica Sphere), tbswind3d, tbsground (NRG IceFree3 heated anemometer), tbsimetxq2 (iMet XQ2 co-located sensor), tbsmerged Value-Added Product, Ceilometer (surface-based, provides cloud base/mixing layer height..., Doppler lidar (operated independently but complementary).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `TBS` | tethered balloon system |
| `IMU` | inertial measurement unit |
| `agl` | above ground level |
| `GPS` | Global Positioning System |
| `ADS-B` | Automatic Dependent Surveillance-Broadcast |
| `FAA` | Federal Aviation Administration |
| `sm` | statute mile |


### References the handbook cites

- Dexheimer, D, K Gaustad, F Mei, and D Zhang. 2023. Tethered Balloon System Merged Data (TBSMERGED) Value-added Product Report. DOE/SC-ARM-TR-286. https://doi.org/10.2172/1958999

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbswind`, read 2026-09-24
- Example file: `sgptbswindC1.b1.20241111.170031.nc` from `sgptbswindC1.b1`, 1.31 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
