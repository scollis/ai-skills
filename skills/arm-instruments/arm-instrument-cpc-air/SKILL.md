---
name: arm-instrument-cpc-air
description: ARM Condensation particle counter aboard aircraft (cpc-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Particle number concentration, Instrument error code, Saturator temperature, Condenser temperature, Optics temperature, Cabinet temperature, Ambient pressure, Orifice pressure), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafmcpcU2.b1) and the variable inventory of a real file. Use when working with cpc-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - cpc-air, Condensation particle counter aboard aircraft, bnfaafmcpcU2.b1, Particle number concentration, Instrument error code, Saturator temperature, Condenser temperature, Optics temperature, Cabinet temperature, Aerosols.
---

# CPC-AIR - Condensation particle counter aboard aircraft

The Model 3772 condensation particle counter detects airborne particles down to 10 nm in diameter by growing them via butanol condensation and optically counting them, deployed aboard the G-1 aircraft aft of an iso-kinetic inlet and/or a counterflow virtual impactor (CVI) inlet.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cpc-air` |
| Handbook | [DOE/SC-ARM-TR-227 / C Kuang, F Mei / September 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-227.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | TSI Incorporated, Model 3772 (also class includes cpc3025-air Model 3025A, cpc3010-air Model 3010) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution; Navigation variables |
| Record | 2013-06-24 to 2026-09-23 (active) |
| Datastreams with data | 44 across 8 sites |
| Sites | acx, bnf, cor, ena, mao, nsa, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/cpc-air |


## Credit

Everything this skill knows about the instrument is the work of **C Kuang, F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> C Kuang, F Mei. *Condensation Particle Counter (CPC) Instrument Handbook – Airborne Version*, DOE/SC-ARM-TR-227, September 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-227.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The essential feature of the CPC is growth of sampled particles through working fluid (butanol) condensation, followed by optical counting. Laminar aerosol flow enters the saturator where butanol liquid is evaporated from a heated wick, saturating the aerosol flow with butanol vapor; this combined flow then enters the thermoelectrically cooled condenser where the butanol vapor becomes supersaturated and condenses onto aerosol particles to form larger droplets. These droplets pass through a nozzle into an optical detector (laser diode, focusing/collecting lenses, photodiode), where they scatter light that is converted into electrical pulses, which are counted and, at high concentrations, corrected for particle coincidence. When vapor supersaturation reaches a certain degree it condenses onto particles (heterogeneous nucleation); if supersaturation is too high, vapor can condense without particles present (homogeneous nucleation), producing noise. Optimal performance is achieved operating at a supersaturation level just below the homogeneous nucleation limit, and particle size detection limit is a strong function of the operating supersaturation ratio.

**Siting.** Typically two CPCs are aboard the G-1 aircraft: one aft of the iso-kinetic inlet (with an installed dilution flow system for high concentrations greater than 1x10^4 #/cc requiring dilution correction), and the other aft of the counterflow virtual impactor (CVI) inlet. During AAF deployments, the 3772 CPC samples within an environmentally controlled cabin per manufacturer's environmental requirements. CPC should be placed on a level surface with the cooling fan exposed to ambient air.

**Sampling.** native rate 1 second; reported every text files spanning an interval of one hour; averaging typical sampling time of one second used for accuracy/repeatability statistics (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle number concentration | #/cc | 0 to 1x10^4 #/cc | 2.5% at ~100 #/cc; 0.3% at ~5000 #/cc... | 1 second | (hb p. 8) |
| Instrument error code | hexadecimal code | - | - | - | (hb p. 8) |
| Saturator temperature | °C | nominal 38.5-39.5°C | - | - | (hb p. 9) |
| Condenser temperature | °C | nominal 21.5-22.5°C | - | - | (hb p. 10) |
| Optics temperature | °C | nominal 38.0-42.0°C | - | - | (hb p. 10) |
| Cabinet temperature | °C | - | - | - | (hb p. 8) |
| Ambient pressure | kPa | - | - | - | (hb p. 8) |
| Orifice pressure | kPa | minimum 50 kPa | - | - | (hb p. 9) |
| Nozzle pressure | kPa | maximum 3 kPa | - | - | (hb p. 9) |
| Laser current | mA | minimum 35 mA | - | - | (hb p. 10) |
| Liquid level (butanol) | full/not full and fraction... | minimum fraction 0.5 | - | - | (hb p. 10) |
| Valve position | open/closed | - | - | - | (hb p. 8) |
| Dilution flow set point | sccm | - | - | - | (hb p. 8) |
| Dilution flow measured | sccm | - | - | - | (hb p. 8) |
| Aerosol flow rate | lpm (empty field in output) | 1.0 lpm nominal | ±5% variability | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Particle size detection limit | down to 10 nm in diameter (nominal D50 = 10 nm) | (hb p. 8) |
| Aerosol flow rate | 1.0 lpm | (hb p. 8) |
| Concentration range | 0 to 1x10^4 #/cc | (hb p. 10) |
| Input voltage | 100-240 VAC, 50/60 Hz, 210 W maximum | (hb p. 13) |
| Warm-up time | approximately 10 minutes | (hb p. 13) |
| External vacuum source requirement | at least 60 kPa (18 in. Hg) | (hb p. 13) |
| Altitude | Up to 4000 m (14,000 ft) | (hb p. 14) |
| Inlet pressure | 75 to 105 kPa (0.74 to 1.05 atm) | (hb p. 14) |
| Operating temperature | 10 to 35°C | (hb p. 14) |
| Ambient humidity | 0 to 90% RH non-condensing | (hb p. 14) |
| Inlet flow rate variability | ±5% | (hb p. 14) |
| Nozzle pressure (nominal, per TSI technician) | 2-3 | (hb p. 18) |


## The data

Verified example: **`bnfaafmcpcU2.b1`**, file `bnfaafmcpcU2.b1.20260911.144346.nc`
(1.35 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=7717 |
| Data variables | 38 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-11T14:43:46 to 2026-09-11T16:52:26 |
| dod version | aafmcpc-b1-1.0 |
| process version | ingest-aafmcpccorr-1.0-2.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `concentration_ave` | 1/cm^3 | time | yes | Average concentration for save interval |
| `condenser_power` | 1 | time | yes | Condenser cooler power |
| `exhaust_pump_power` | 1 | time | yes | Exhaust vacuum pump power |
| `inlet_temperature` | degC | time | yes | Inlet temperature |
| `optics_power` | 1 | time | yes | Optics block heater power |
| `saturator_bottom_power` | 1 | time | yes | Saturator bottom heater power |
| `saturator_flow_power` | 1 | time | yes | Saturator flow pump power |
| `saturator_top_power` | 1 | time | yes | Saturator top heater power |
| `concentration_corrected` | 1/cm^3 | time | - | Coincidence Corrected concentration |
| `concentration_raw` | 1/cm^3 | time | - | Raw uncorrected concentration |
| `condenser_temperature` | degC | time | - | Condenser temperature |
| `count` | count/s | time | - | Particle counts per second |
| `error_number` | 1 | time | - | Bit packed error codes |
| `fill_count` | count | time | - | Butanol fill attempts |
| `flow_rate` | cm^3/min | time | - | Sample flow rate |
| `inlet_pressure` | hPa | time | - | Ambient pressure at inlet |
| `mcpc_power` | 1 | time | - | MCPC master power indicator |
| `mcpc_pump` | 1 | time | - | Mixing cpc pump |
| `optics_temperature` | degC | time | - | Optics block temperature |
| `saturator_bottom_temperature` | degC | time | - | Saturator bottom temperature |
| `saturator_flow_rate` | cm^3/min | time | - | Saturator flow rate |
| `saturator_top_temperature` | degC | time | - | Saturator top temperature |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("bnfaafmcpcU2.b1", "2026-09-11", "2026-09-11")
ds = armlive_open("bnfaafmcpcU2.b1", "2026-09-11", "2026-09-11", cleanup_qc=True)
```

## Quality control in this datastream

11 `qc_` companion variables cover 11 of the
38 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (bnfaafmcpcU2.b1.20260911.144346.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `concentration_ave` | Value is less than fail_min. | 44 | 0.5702 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfaafmcpcU2.b1", "20130624", "20260923")
```

The handbook's own note on data quality: First level: automated data flagging by ARM's Data Quality Office based on mentor-supplied thresholds (nozzle pressure, orifice pressure, saturator/condenser/optics temperatures, butanol level, laser current - see artifacts). Second level: automatic generation of plots including nozzle pressure vs. time (to detect clogging) and comparison of co-located 3772 and 3776 particle number concentration measurements vs. time (3772 concentration should always be ≤ 3776 concentration since 3772 detection limit is 10 nm vs. 3 nm for 3776); this comparison provides a quick assessment of relative CPC...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Nozzle clogging by debris | Steady increase in nozzle pressure over time; nozzle pressure exceeding 3 kPa generates a warning | Clean clogged nozzle per Appendix B nozzle-cleaning procedure | (hb p. 9) |
| Insufficient vacuum / low orifice pressure | Orifice pressure below 50 kPa generates an alarm, indicating insufficient vacuum to produce 1 lpm flow | Ensure external vacuum source provides at least 60 kPa (18 in. Hg) | (hb p. 9) |
| Saturator temperature deviation | Saturator temperature outside 38.5-39.5°C generates an alarm; deviation causes altered butanol vapor pressure and resulting particle size detection limit (nominally 10 nm) | - | (hb p. 9) |
| Condenser temperature deviation | Condenser temperature outside 21.5-22.5°C generates an alarm; deviation causes altered vapor saturation ratio and resulting particle size detection limit | - | (hb p. 10) |
| Optics temperature deviation / vapor condensation on optics (flooding) | Optics temperature outside 38.0-42.0°C generates an alarm; could lead to vapor condensation on optics surface (flooded optics) | Correct flooded optics whenever there is indication flooding has occurred | (hb p. 10) |
| Low butanol (working fluid) level | Butanol fraction full below 0.5 generates an alarm; may prevent sufficient butanol vapor from reaching expected vapor saturation ratio and particle size detection limit | Re-fill butanol reservoir before each flight | (hb p. 10) |
| Declining laser health | Laser current below 35 mA generates an alarm | - | (hb p. 10) |
| Coincidence error at high concentration | Particle concentrations above range require correction for concentration-dependent counting coincidence, corrected up to 1x10^4 #/cc | Signal-processing electronics correct for coincidence; use dilution flow system for concentrations greater than 1x10^4 #/cc with dilution correction... | (hb p. 11) |
| High concentration saturation (greater than 1x10^4 #/cc) | Measured concentration exceeds instrument's nominal range without dilution | Installed dilution flow system provides user-set dilution flow; apply dilution correction formula: Nambient = Nmeasured / (1 - Qdilution/1000) | (hb p. 8) |
| Statistical counting noise (concentration-dependent) | Accuracy/repeatability varies with concentration: ~2.5% at ~100 #/cc, ~0.3% at ~5000 #/cc using 1 s sampling | - | (hb p. 11) |
| Inlet flow rate variability | Inlet flow rate (not an online measurement) typically varies up to 5%, primary contributor to measurement accuracy and repeatability | Verify flow rate weekly with bubble flow meter | (hb p. 11) |
| Homogeneous nucleation noise | Particle counts from droplets generated through homogeneous nucleation of working fluid appear as instrument noise, without real sampled particles present | Operate at supersaturation level just below the homogeneous nucleation limit | (hb p. 13) |
| Particle size detection limit sensitivity to operating conditions | Detection limit (nominally 10 nm) shifts with supersaturation ratio, which depends on saturator/condenser temperatures | - | (hb p. 13) |
| Counting efficiency depends on particle composition and diameter | Counting efficiency curve differs for silver vs. sodium chloride particles near D50 (10 nm) | Determine via calibration protocol in Hermann et al. (2007) | (hb p. 14) |
| Flammable/toxic working fluid (butanol) | N/A - safety hazard rather than data artifact | Handle with care; drain before shipment; Class I laser instrument, no laser exposure during normal operation | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Inlet flow rate verified with low-pressure drop-bubble flow meter; dilution flow system calibrated against mass flow controller set point using bubble flow meter; size-dependent particle counting efficiency determined per Hermann et al. (2007) using tube furnace evaporation-condensation aerosol generation,... (hb p. 14) |
| Calibration interval | Calibrated prior to instrument installation and deployment (hb p. 14) |
| Traceability | CPC calibration data collected and maintained by the instrument mentor (hb p. 14) |
| Routine maintenance | Re-fill butanol reservoir before each flight; drain butanol from reservoir prior to instrument shipment; verify flow rate once a week using low-pressure drop-bubble flowmeter (average of three measurements, should be 1.0 lpm ±5%); correct flooded optics whenever flooding indicated; clean clogged nozzle when nozzle... (hb p. 16) |
| Maintenance interval | weekly flow verification; before each flight refill; as-needed nozzle cleaning and optics correction (hb p. 16) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: TSI Model 3776 CPC (co-located comparison, 3 nm detection limit), cpc3025-air Ultrafine Condensation Particle Counter (UCPC), Model..., cpc3010-air Condensation Particle Counter (CPC), Model 3010.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AC` | alternating current |
| `ADC` | analog data collection |
| `ARM` | Atmospheric Radiation Measurement |
| `BNC` | Bayonet Neill–Concelman (coaxial cable connector) |
| `CPC` | condensation particle counter |
| `CVI` | counterflow virtual impactor |
| `DAS` | data acquisition system |
| `G-1` | Gulfstream-159 aircraft |
| `GoAmazon 2014/15` | Green Ocean Amazon 2014/15 field campaign |
| `MAOS` | Mobile Aerosol Observing System |
| `RH` | relative humidity |
| `SDC` | serial data collection |
| `SEA` | Science Engineering Associates |


### References the handbook cites

- Hermann, M, B Wehner, O Bischof, HS Han, T Krinke., W Liu, A Zerrath, and A Wiedensohler. 2007. "Particle counting efficiencies of new TSI condensation particle counters." Journal of Aerosol Science 38(a6): 674–682,...
- Mordas, G, H Manninen, T Petäjä, P Aalto, K Hämeri, and M Kulmala. 2008. "On operation of the ultra-fine water-based CPC TSI 3786 and comparison with other TSI models (TSI 3776, TSI 3772, TSI 3025, TSI 3010, TSI 3007)."...
- Ahn, KH, and BYH Liu. 1990. "Particle activation and droplet growth processes in condensation nucleus counter I. Theoretical background." Journal of Aerosol Science 21(2): 249–261,...
- Stolzenburg, MR, and PH McMurry. 1991. "An ultrafine aerosol condensation nucleus counter." Aerosol Science and Technology 14(1): 48–65, https://doi.org/10.1080/02786829108959470

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-227.pdf (22 pages, DOE/SC-ARM-TR-227, by C Kuang, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=cpc-air`, read 2026-09-23
- Example file: `bnfaafmcpcU2.b1.20260911.144346.nc` from `bnfaafmcpcU2.b1`, 1.35 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
