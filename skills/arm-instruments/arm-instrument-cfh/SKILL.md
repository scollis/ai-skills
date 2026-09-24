---
name: arm-instrument-cfh
description: ARM Cryogenic Frostpoint Hygrometer (cfh) - handbook-derived instrument reference: measurement principle, reported quantities (Frostpoint temperature, Water vapor mixing ratio, Relative humidity, Ambient temperature, Pressure, Altitude, Potential temperature, Wind speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpcfhC1.b1) and the variable inventory of a real file. Use when working with cfh data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling. Triggers - cfh, Cryogenic Frostpoint Hygrometer, sgpcfhC1.b1, Frostpoint temperature, Water vapor mixing ratio, Relative humidity, Ambient temperature, Pressure, Altitude, Atmospheric Profiling, EN-SCI Environmental Science (Boulder, Colorado), AIDA, ASCII, CART, CMDL.
---

# CFH - Cryogenic Frostpoint Hygrometer

The CFH is a small, balloon-borne chilled-mirror hygrometer that measures highly accurate frost/dewpoint temperature profiles of atmospheric water vapor from the surface to the stratosphere.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 31 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cfh` |
| Handbook | [DOE/SC-ARM-TR-210 / M Stuefer, T Gordon / March 2018](https://www.arm.gov/publications/tech_reports/handbooks/cfh_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | EN-SCI Environmental Science (Boulder, Colorado); CFH developed at University of Colorado by Holger Vömel; used with InterMet iMet-1-RSB radiosonde (2L CFH version) at ARM SGP; Vaisala RS-92 used for... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Horizontal wind |
| Record | 2014-09-11 to 2019-12-18 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/cfh |


## Credit

Everything this skill knows about the instrument is the work of **M Stuefer, T Gordon** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> M Stuefer, T Gordon. *Cryogenic Frostpoint Hygrometer (CFH) Instrument Handbook*, DOE/SC-ARM-TR-210, March 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/cfh_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The CFH measurement is based on the chilled-mirror principle, in which a small mirror is cooled by a cryogenic liquid (currently Trifluoromethane, CHF3) and heated by a heater coil so that it is maintained at the thermodynamic equilibrium temperature between the vapor and condensed phases of water. An LED emits infrared light that reflects off the mirror, and a pair of phase-sensitive photodiodes senses the reflected light, which varies with the formation of frost or dew; this signal is fed back to a controller that adjusts mirror temperature to maintain a constant thin condensate layer. The mirror temperature at this equilibrium condition equals the ambient frost or dew point temperature of the air passing the mirror. A force-freezing algorithm forces the condensate to freeze at -15degC to remove liquid/ice ambiguity. Frost/dewpoint profiles are converted to relative humidity and mixing ratios using the Clausius-Clapeyron equation variants: Hyland Wexler for saturation vapor pressure over liquid water (dewpoint) and Goff Gratch for saturation vapor pressure over ice (frostpoint).

**Siting.** The CFH-iMet package is combined with a radiosonde as data transmitter; at SGP a Vaisala RS-92 radiosonde is flown for reference comparison on the opposite side of a wooden rigging pole at a distance of typically 1.5 meters. Air inlet tubes (17 cm) extend above and below the foam box to enable clean sampling of ambient air, away from self-contamination. Mechanical shielding of sunlight is not necessary due to the phase-sensitive detector.

**Sampling.** native rate typically less than two seconds per mirror measurement; reported every continuous during balloon flight from surface to stratosphere; averaging mean mirror temperature averaged over a period of 10 seconds typically yields best results (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Frostpoint temperature (mirror temperature, TFp Hyg) | deg C | greater than  +25C to less than  -80C | better than 0.2 K (total); systematic errors... | - | (hb p. 10) |
| Water vapor mixing ratio (H2O Mr) | ppmv | greater than  25000 ppmv to less than ... | accuracies of only a few parts per million | - | (hb p. 14) |
| Relative humidity (RH FP, RH) | % | - | - | - | (hb p. 9) |
| Ambient temperature (Temp, Traw) | deg C | - | - | - | (hb p. 9) |
| Pressure (Press) | hPa | - | - | - | (hb p. 9) |
| Altitude (Alt, GPS alt) | km | 0-30 km | - | - | (hb p. 14) |
| Potential temperature (Theta) | K | - | - | - | (hb p. 9) |
| Wind speed (Wind) | m/s | - | - | - | (hb p. 10) |
| Wind direction (Wind Dir) | deg | - | - | - | (hb p. 10) |
| GPS latitude/longitude | deg | - | - | - | (hb p. 10) |
| CFH battery voltage (Batt) | V | - | - | - | (hb p. 10) |
| CFH detector signal (TP2) | V | - | - | - | (hb p. 10) |
| CFH detector/optics temperature (TOptic) | deg C | - | - | - | (hb p. 10) |
| Rise rate (RiseR) | m/s | - | - | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| CFH weight (without cryogen) | 400 g | (hb p. 14) |
| Mirror diameter | 7 mm | (hb p. 14) |
| Mirror thickness | 1.27 mm | (hb p. 14) |
| Max mirror temperature limit | 40C | (hb p. 14) |
| Altitude range | 0-30 km | (hb p. 14) |
| Dimensions (without tube) | 6.5'W x 12'L x 5'H | (hb p. 14) |
| Detection for dew or frostpoints | greater than  +25C to less than  -80C | (hb p. 14) |
| Mixing ratio detection | greater than  25000 ppmv to less than  0.8 ppmv | (hb p. 14) |
| Vertical resolution | less than  ~50m (troposphere) to less than  ~100m (stratosphere) | (hb p. 14) |
| Systematic errors | less than 0.1 K | (hb p. 16) |
| Total uncertainty (good conditions) | better than 0.2 K | (hb p. 16) |
| Air inlet tube length | 17 cm long, extending 12 cm beyond foam box in both directions | (hb p. 8) |
| Input voltage (batteries) | 12 V, drops to 11V under load, dips to 9V when heater active, brief 8V periods acceptable for a few seconds | (hb p. 11) |
| Battery configuration | 8 x 3V lithium CR123A batteries | (hb p. 14) |


## The data

Verified example: **`sgpcfhC1.b1`**, file `sgpcfhC1.b1.20191218.162850.nc`
(1.51 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=7539 |
| Data variables | 47 |
| QC variables | 21 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2019-12-18T16:28:50 to 2019-12-18T18:35:33 |
| dod version | cfh-b1-1.0 |
| process version | ingest-cfh-1.1-1.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cfh_battery_voltage` | V | time | yes | CFH Battery voltage |
| `cfh_frost_point_temperature` | degC | time | yes | Frost point temperature measured by the CFH |
| `data_frame_number` | unitless | time | yes | Data frame number |
| `detector_signal` | V | time | yes | CFH detector signal |
| `detector_temperature` | degC | time | yes | CFH detector temperature |
| `h2o_mixing_ratio` | ppmv | time | yes | Mixing ratio calculated from the CFH frost point temperature |
| `imet_temp_i` | degC | time | yes | Internal temperature of the Intermet radiosonde |
| `imet_temp_p` | degC | time | yes | Temperature near the pressure sensor of the Intermet radiosonde |
| `imet_temp_u` | degC | time | yes | Temperature near the humidity sensor of the Intermet radiosonde |
| `mixing_ratio` | ppmv | time | yes | Mixing ratio calculated from radiosonde pressure and CFH saturation... |
| `potential_temperature` | K | time | yes | Potential temperature |
| `pressure` | hPa | time | yes | Pressure from the radiosonde pressure sensor |
| `relative_humidity` | % | time | yes | Relative humidity over liquid from the radiosonde |
| `rs_battery_voltage` | V | time | yes | Battery voltage of the radiosonde battery |
| `rs_frost_point_temperature` | degC | time | yes | Frost point temperature calculated from radiosonde relative humidity |
| `saturation_vapor_pressure` | hPa | time | yes | Saturation vapor pressure calculated from CFH frost point temperature |
| `temperature` | degC | time | yes | Ambient temperature from the radiosonde |
| `temperature_raw` | degC | time | yes | Ambient temperature from the radiosonde without any corrections... |
| `wind_direction` | degree | time | yes | Wind direction calculated from GPS location measurements |
| `wind_speed` | m/s | time | yes | Wind speed calculated from GPS location measurements |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpcfhC1.b1", "2019-12-18", "2019-12-18")
ds = armlive_open("sgpcfhC1.b1", "2019-12-18", "2019-12-18", cleanup_qc=True)
```

This datastream carries 47 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpcfhC1.b1", start, end,
                  keep_variables=["cfh_battery_voltage", "cfh_frost_point_temperature", "data_frame_number", "qc_cfh_battery_voltage", "qc_cfh_frost_point_temperature", "qc_data_frame_number"])
```

## Quality control in this datastream

21 `qc_` companion variables cover 21 of the
47 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpcfhC1.b1.20191218.162850.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `rs_battery_voltage` | Value is greater than the fail_max. | 7477 | 99.1776 |
| `imet_temp_p` | Value is less than the fail_min. | 6397 | 84.8521 |
| `imet_temp_i` | Value is less than the fail_min. | 6375 | 84.5603 |
| `altitude` | Value is equal to missing_value. | 6374 | 84.547 |
| `potential_temperature` | Value is equal to missing_value. | 6374 | 84.547 |
| `mixing_ratio` | Value is equal to missing_value. | 6275 | 83.2339 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpcfhC1.b1", "20140911", "20260923")
```

The handbook's own note on data quality: Data Quality Reports (DQRs) flag data as "questionable," "unreliable," or "missing," accessible via the ARM Data Quality Explorer or indicated with a color bar on the ARM Data Discovery browser. Faulty frostpoint data are mostly caused by mirror contamination. The Strato software's flight data file (FLT.DAT) contains a data quality flag 'FI': a value of 1 indicates usable CFH frostpoint data, while 0 indicates unreliable data.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Mirror contamination | Faulty/unreliable frostpoint data, flagged by FI=0 in flight data file | Visual inspection during post-processing to eliminate affected data; mirror cleaning with cotton swabs and methanol before flight | (hb p. 7) |
| Mixed-phase (liquid/ice) mirror contamination | Ambiguous frostpoint readings when supercooled water drops and ice both cover mirror surface | CFH controller forces condensate to freeze at -15C, eliminating liquid/ice ambiguity; supercooled water assumed to exist between 0C and -15C | (hb p. 11) |
| Outgassing from balloon, strings, intake tubes, or parachute | Inaccurate frostpoint readings, especially when balloon passes through liquid water clouds | Eliminated during post-processing by visual inspection of the data | (hb p. 11) |
| Frost-layer morphology / phase change uncertainty | Unknown/unquantified additional uncertainty (listed as 0 K in table but flagged with caveat) | None specified beyond noting unknown phase changes from supercooled water to ice | (hb p. 10) |
| Mirror temperature oscillation around equilibrium | Individual mirror temperature readings measured at less than 2 s intervals oscillate around the true equilibrium frostpoint temperature rather than reading it directly | Average mirror temperature over a 10-second period for best results | (hb p. 10) |
| Manufacturing bias in thermistor placement (older models) | Measurement bias observed for older CFH models due to small manufacturing variation of thermistor location on mirror | Recently eliminated in current models | (hb p. 11) |
| Low detector signal triggers heater | If detector signal falls below 2.5 V, mirror heater turns on and mirror temperature increases | - | (hb p. 11) |
| Low battery voltage | Battery voltage drops to 11V under load, dips to 9V when heater active, brief 8V periods; visible as low Batt (V) values in plot browser diagnostic plots | Diagnostic plots used to detect low battery voltage; short 8V dips should not last more than a few seconds | (hb p. 11) |
| Data gaps | Detectable via ARM diagnostic plot browser graphics designed to quickly detect data gaps | Use plot browser diagnostic plots for detection | (hb p. 10) |
| Trace gas interference | Contributes to measurement uncertainty (listed as negligible in uncertainty table) | None specified (negligible) | (hb p. 10) |
| Calibration miscalibration/out-of-range values | CFH.setup window shows red field for 'CFH instrument' if calibration coefficients missing or out-of-range; instrument without calibration will not report proper mirror temperature | Recheck/recalibrate instrument before flight | (hb p. 22) |
| Reflectivity setpoint drift from nominal | Reflectivity measurement not exactly at 88% (screw difficult to turn due to Loctite) | Values between 85% and 90% acceptable if noted; add note to metadata for that sounding | (hb p. 20) |
| Mirror temperature ceiling | Mirror temperature cannot surpass 40C | Built-in limit prevents accidental burnout of mirror heater | (hb p. 7) |
| Cooling liquid safety hazard (not a data artifact but operational limitation) |  | Use gloves and eye protection; store/use outdoors or in well-ventilated area to avoid oxygen displacement/suffocation risk | (hb p. 23) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Individually calibrated (to a NIST-traceable standard) thermistor attached to mirror; calibration coefficients (A, B, C, D) saved within *.DE1 file via Strato software; CFH.setup program used to clean mirror and set reflectivity setpoint (near 88%, acceptable range 85-90%) as part of calibration procedure (hb p. 7) |
| Calibration interval | performed prior to each flight (as part of setup) (hb p. 7) |
| Traceability | NIST-traceable standard (hb p. 7) |
| Routine maintenance | Visual inspection for fractures in CFH housing and cracks in cooling-liquid compartment; steel air inlet tubes carefully removed, CFH mirror cleaned, and new tubes inserted with epoxy glue before re-use; foam housing rebuilt in rare cases (hb p. 23) |
| Maintenance interval | after each flight, before re-use (hb p. 23) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: NOAA/CMDL frostpoint hygrometer (FPH), Vaisala RS-92 radiosonde, InterMet iMet-1-RSB radiosonde, Vaisala RS-41 radiosonde (anticipated replacement), Aura MLS instrument, Russian Fluorescent Lyman Alpha Stratospheric Hygrometer, NOAA/CSD frostpoint hygrometer, Harvard Lyman-alpha hygrometer.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AIDA` | Aerosols Interaction and Dynamics in the Atmosphere |
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `CART` | Cloud and Radiation Testbed |
| `CFH` | cryogenic frostpoint hygrometer |
| `CMDL` | Climate Monitoring and Diagnostic Laboratory (NOAA) |
| `DOE` | U.S. Department of Energy |
| `DQR` | Data Quality Report |
| `FPH` | frostpoint hygrometer |
| `GMT` | Greenwich Mean Time |
| `GPS` | Global Positioning System |
| `IMet` | InterMet (International Met Systems) |
| `LED` | light-emitting diode |
| `MLS` | Microwave Limb Sounder |


### References the handbook cites

- Vömel, H, DE David, and K Smith. 2007. "Accuracy of tropospheric and stratospheric water vapor measurements by the cryogenic frost point hygrometer: Instrumental details and observations." Journal of Geophysical...
- Vömel, H, "Cryogenic Frostpoint Hygrometer Operations Manual," Version 1.9, 11 July 2012.
- Vömel, H, "Strato/Balloon Data Output Guide," Version 1.2, 14 October 2015.
- Vömel, H, T Naebert, R Dirksen, and M Sommer, 2016. "An update on the uncertainties of water vapor measurements using cryogenic frost point hygrometers." Atmospheric Measurement Techniques 9(8): 3755-3768,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/cfh_handbook.pdf (31 pages, DOE/SC-ARM-TR-210, by M Stuefer, T Gordon)
- Catalog record: ARM data-source index, `instrument_class_code=cfh`, read 2026-09-23
- Example file: `sgpcfhC1.b1.20191218.162850.nc` from `sgpcfhC1.b1`, 1.51 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
