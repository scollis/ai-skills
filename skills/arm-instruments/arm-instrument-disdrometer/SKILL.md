---
name: arm-instrument-disdrometer
description: ARM Impact Disdrometer (disdrometer) - handbook-derived instrument reference. Measurement principle, reported quantities (Precipitation, Number of drops, Average diameter of drop class, Rain rate, Largest drop, Number density N, Fall velocity v), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpdisdrometerC1.b1) and the variable inventory of a real file. Use when working with disdrometer data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - disdrometer, Impact Disdrometer, sgpdisdrometerC1.b1, Precipitation, Number of drops, Average diameter of drop class, Rain rate, Largest drop, Number density N, Surface Meteorology, Distromet LTD, RD-80 impact disdrometer, VDIS.
---

# DISDROMETER - Impact Disdrometer

The impact disdrometer measures the drop size spectra (and derived rainfall properties) of falling raindrops by converting the mechanical momentum of impacting drops into electric pulses, and is deployed outdoors at ARM sites alongside a rain gauge for continuous 1-minute surface meteorology observations.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 19 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `disdrometer` |
| Handbook | [DOE/SC-ARM-TR-111 / MJ Bartholomew / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/disdrometer_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Distromet LTD, RD-80 impact disdrometer |
| Primary measurements | Precipitation; Radar reflectivity |
| Record | 2006-01-11 to 2025-04-08 (retired) |
| Datastreams with data | 3 across 2 sites |
| Sites | sgp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/disdrometer |


## Credit

Everything this skill knows about the instrument is the work of **MJ Bartholomew** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> MJ Bartholomew. *Impact Disdrometer Instrument Handbook*, DOE/SC-ARM-TR-111, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/disdrometer_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `vdis` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `disdrometer`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The sensor transforms the mechanical momentum of an impacting drop into an electric pulse, with the amplitude of the pulse roughly proportional to the mechanical momentum. The sensor consists of a cylindrical metal housing containing an electromechanical transducer and an amplifier module. The processor contains circuitry to eliminate unwanted signals, resulting mainly from acoustic noise, and produces a 7-bit code at the output for every drop that hits the sensitive surface of the sensor. Drop diameters are grouped into 20 discrete drop-size classes, each with an average diameter, associated terminal fall velocity, and diameter interval, from which quantities such as rainfall rate, liquid water content, radar reflectivity factor, and distribution slope/intercept are calculated over a standard 60 s time interval using a sensitive surface area F = 0.005 m2.

**Siting.** The impact disdrometer needs a level, firm base and a quiet environment because acoustic noise can be detected by the sensor. Strong winds that produce turbulence at the edges of the sensor are a source of error; mounting the top of the sensor flush with its surroundings minimizes the wind problem. The sensor must not be flooded, and the top of the sensor needs to be clear of snow. External sources of electromagnetic fields and power surges can interrupt and influence the measurements made by the disdrometer.

**Sampling.** native rate per-drop 7-bit code output for every drop hitting sensor; reported every 1 min; averaging Time interval for measurement t = 60 s (standard value) (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Precipitation (rain amount) | millimeters | - | - | - | (hb p. 8) |
| Number of drops | integer | - | - | - | (hb p. 8) |
| Average diameter of drop class | millimeters | 0.3 mm to 5.4 mm | 3% of drop diameter (center of sensor); ±5%... | - | (hb p. 9) |
| Rain rate | millimeters/hr | - | - | - | (hb p. 8) |
| Largest drop (Dmax) | millimeters | - | - | - | (hb p. 8) |
| Number density N(D) | 1/(m3 · m) | - | - | - | (hb p. 8) |
| Fall velocity v(D) | m/s | - | - | - | (hb p. 8) |
| Diameter interval between drop size classes | millimeters | - | - | - | (hb p. 8) |
| Liquid water content | grams/meter3 | - | - | - | (hb p. 8) |
| Radar reflectivity factor (ZdB) | dB | - | - | - | (hb p. 8) |
| Energy flux | joules/(meter2 hour) | - | - | - | (hb p. 8) |
| Distribution slope (lambda) | 1/millimeter | - | - | - | (hb p. 8) |
| Distribution intercept (N0) | 1/(meters3 millimeters) | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Drop size measurement range | 0.3 mm to 5.4 mm | (hb p. 9) |
| Accuracy (drop diameter, center of sensor) | 3% of drop diameter | (hb p. 9) |
| Accuracy (standard deviation over sensitive surface) | approximately ±5% | (hb p. 9) |
| Sensitive surface area (F) | 0.005 m2 | (hb p. 18) |
| Standard measurement time interval (t) | 60 s | (hb p. 18) |
| Video disdrometer bin width | 0.2 mm | (hb p. 10) |


## The data

Verified example: **`sgpdisdrometerC1.b1`**, file `sgpdisdrometerC1.b1.20250405.000000.cdf`
(0.44 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `drop_class`=20 |
| Data variables | 22 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2025-04-05T00:00:00 to 2025-04-05T23:59:00 |
| sampling interval | 60 seconds |
| averaging interval | None |
| dod version | disdrometer-b1-1.2 |
| process version | ingest-disdrometer-2.5-1.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `num_drop` | none | time,drop_class | yes | Number of drops |
| `precip_dis` | mm | time | yes | Precipitation |
| `rain_rate` | mm/hr | time | yes | Rain rate |
| `time` | - | time | yes | Time offset from midnight |
| `delta_diam` | mm | drop_class | - | Diameter interval between drop size classes |
| `diam_max` | mm | time | - | Diameter of largest drop |
| `distribution_intercept` | 1/(m^3-mm) | time | - | Distribution intercept |
| `distribution_slope` | 1/mm | time | - | Distribution slope |
| `drop_class` | unitless | drop_class | - | Drop class |
| `energy_flux` | J/(m^2-hr) | time | - | Energy flux |
| `fall_velocity` | m/s | drop_class | - | Fall velocity |
| `liq_water` | gm/m^3 | time | - | Liquid water content |
| `mean_diam_drop_class` | mm | drop_class | - | Diameter of drop size class |
| `number_density` | 1/(m^3-mm) | time,drop_class | - | Number density |
| `radar_reflectivity` | dB | time | - | Radar reflectivity |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpdisdrometerC1.b1", "2025-04-05", "2025-04-05")
ds = armlive_open("sgpdisdrometerC1.b1", "2025-04-05", "2025-04-05", cleanup_qc=True)
```

## Quality control in this datastream

4 `qc_` companion variables cover 3 of the
22 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

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
act.qc.print_dqr("sgpdisdrometerC1.b1", "20060111", "20260923")
```

The handbook's own note on data quality: If data are missing for a sample time, a "missing_value" of -999 is assigned to that field. Data-quality variables (qc_time, qc_precip_dis, qc_numdrop, qc_rain_rate, plus qc for d_max, ef, liq_water) are provided with minimum/maximum bounds (e.g., qc_precip_dis: 0-10, d_max: 0-10, ef: 0-4000, liq_water: 0-100). Instrument mentor reviews occur once or twice a week, three days behind the current day, using DSview plots for instrument operation status and DQ HandS diagnostic plots; outputs are Data Quality Problem Reports and Data Quality Reports as needed. Best indicators of instrument health...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Routine processor/sensor self-testing | A few hundred drops typically appear in drop class 7 (1 mm) when little or no drops occur in other classes; testing occurs once a week (not raining), usually between 15:00 and 18:00 UTC | These observations should be ignored | (hb p. 11) |
| Wind-induced sensor vibration / false small-drop detection | False detection of small drops usually in the 0.3-mm drop class, visible as spurious counts during windy periods | Mounting the top of the sensor flush with its surroundings minimizes the wind problem | (hb p. 11) |
| Acoustic noise sensitivity | Spurious pulses attributed to acoustic noise; processor circuitry attempts to eliminate unwanted signals from this source | Site the instrument in a quiet environment on a level, firm base | (hb p. 8) |
| Sensor location dependence of pulse amplitude | Pulse amplitudes for drops of equal diameter form a distribution around the average amplitude (approx ±5% std dev in diameter) depending on where on the sensitive cone the drop lands | - | (hb p. 9) |
| Turbulence/wind at sensor edges | Errors in drop measurements coincide with strong wind periods | Mount sensor top flush with surroundings | (hb p. 8) |
| Flooding of sensor | Data outages or anomalies during standing water conditions | Sensor must not be flooded | (hb p. 8) |
| Snow cover on sensor | Loss of valid drop detections when top of sensor is obstructed | Top of sensor needs to be clear of snow | (hb p. 8) |
| Electromagnetic interference / power surges | Interruptions or influenced (corrupted) measurements from external EMF sources or power surges | - | (hb p. 8) |
| Missing data | Field populated with missing_value of -999 for a sample time | - | (hb p. 10) |
| Disdrometer vs. rain gauge disagreement | When rainfall rate is between 1 and 10 mm/hr for several hours, total rain amounts collected over the event should agree between disdrometer and gauge to within 15%; larger disagreement... | Monitor quality-control flags for instrument health/performance | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Disdrometer sensor and processor sent to Distromet for calibration (hb p. 9) |
| Calibration interval | Once a year (hb p. 9) |
| Traceability | Should be done during the winter at the Southern Great Plains site and during the driest time of the year for the Darwin site (hb p. 9) |
| Routine maintenance | Inspect site grounds for hazards; visually inspect conduit, cables, and connectors for damage/tightness/water intrusion; check status of power LED on disdrometer processor; keep sensor free of leaves/debris; test internal processor/sensor circuit via test button and LED #4/10000-Hz sound check (hb p. 9) |
| Maintenance interval | Weekly (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Video disdrometer (VDIS), Tipping bucket rain gauge, Weighing bucket rain gauge.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `DOE` | U.S. Department of Energy |
| `LED` | light-emitting diode |
| `PM` | planned maintenance |
| `QC` | quality control |
| `QME` | Quality Measurement Experiment |
| `UTC` | Coordinated Universal Time |
| `VAP` | Value-Added Product |
| `VDIS` | video disdrometer |


### References the handbook cites

- Joss, J and A Waldvogel. 1967. "In spektrograph fuer niederschlagstropfen mit automatischer auswertung." Pure Applied Geophysics 68(1): 240-246, doi:10.1007/BF00874898.
- Joss, J and A Waldvogel. 1969. "Raindrop size distribution and sampling size errors." Journal of Atmospheric Science 26: 566-569, doi:10.1175/1520-0469(1969)026-0566:RSDASSgreater than 2.0.CO;2.
- Gunn, R and GD Kinzer. 1949. "The terminal velocity of fall for water droplets in stagnant air." Journal of Meteorology 6: 243-248, doi:10.1175/1520-0469(1949)006less than 0243:TTVOFFgreater than 2.0.CO;2.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/disdrometer_handbook.pdf (19 pages, DOE/SC-ARM-TR-111, by MJ Bartholomew)
- Catalog record: ARM data-source index, `instrument_class_code=disdrometer`, read 2026-09-23
- Example file: `sgpdisdrometerC1.b1.20250405.000000.cdf` from `sgpdisdrometerC1.b1`, 0.44 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
