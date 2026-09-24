---
name: arm-instrument-cpc
description: ARM Condensation Particle Counter (cpc) - handbook-derived instrument reference: measurement principle, reported quantities (Particle number concentration, Instrument error code, Saturator temperature, Condenser temperature, Optics temperature, Cabinet temperature, Ambient pressure, Orifice pressure), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaoscpcC1.b1) and the variable inventory of a real file. Use when working with cpc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - cpc, Condensation Particle Counter, sgpaoscpcC1.b1, Particle number concentration, Instrument error code, Saturator temperature, Condenser temperature, Optics temperature, Cabinet temperature, Aerosols, TSI Incorporated, Model 3772 condensation particle counter, CPCf, CPCu, EPCAPE, HEPA.
---

# CPC - Condensation Particle Counter

The Model 3772 CPC measures airborne particle number concentration (down to 10 nm diameter, 0-1x10^4 #/cc) at a fixed 1.0 lpm sample flow, deployed as part of ARM's Aerosol Observing System (AOS)/Mobile Aerosol Observing System (MAOS) to continuously sample ambient aerosol.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 24 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cpc` |
| Handbook | [DOE/SC-ARM-TR-145 / A Singh, C Kuang / April 2024](https://www.arm.gov/publications/tech_reports/handbooks/cpc_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | TSI Incorporated, Model 3772 condensation particle counter |
| Primary measurements | Aerosol concentration |
| Record | 2010-10-14 to 2026-09-23 (active) |
| Datastreams with data | 114 across 24 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mag |
| ARM page | https://www.arm.gov/capabilities/instruments/cpc |


## Credit

Everything this skill knows about the instrument is the work of **A Singh, C Kuang** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Singh, C Kuang. *Condensation Particle Counter (CPC) Instrument Handbook*, DOE/SC-ARM-TR-145, April 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/cpc_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The CPC grows sampled particles into larger droplets through condensation of a working fluid (n-butyl alcohol/butanol) followed by optical counting. Aerosol flow enters a heated saturator where butanol evaporates from a wick and saturates the flow with vapor, then passes into a thermoelectrically cooled condenser where the vapor becomes supersaturated and condenses onto particles to form droplets. These droplets pass through a nozzle into an optical detector (laser diode, lenses, photodiode) where they scatter laser light, generating electrical pulses that are counted and corrected for coincidence at high concentrations. Vapor condensation onto particles is heterogeneous nucleation; if supersaturation is too high, homogeneous nucleation of the working fluid vapor itself can occur, producing spurious counts/noise, so the instrument is operated at a supersaturation level just below the homogeneous nucleation limit. The particle size detection limit (D50, nominally 10 nm) is a strong function of the operating supersaturation ratio.

**Siting.** Place the CPC on a level surface with the cooling fan on the back panel exposed to ambient air; requires an external vacuum source (at least 60 kPa) connected to the vacuum port to produce fixed 1.0 lpm critical flow. During ARM deployments, the 3772 CPC samples within an environmentally controlled measurement container per manufacturer's environmental requirements (operating temperature 10-35°C, altitude up to 2000 m, inlet pressure 75-105 kPa, ambient humidity 0-90% RH non-condensing).

**Sampling.** native rate 1 second; reported every 1 second, written to hour-long text files; averaging typical sampling time of one second used for accuracy/repeatability calculations (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle number concentration | #/cc | 0 to 1x10^4 #/cc | 2.5% at ~100 #/cc; 0.3% at ~5000 #/cc... | 1 second | (hb p. 12) |
| Instrument error code | hexadecimal code | - | - | - | (hb p. 8) |
| Saturator temperature | °C | nominal 38.5-39.5°C | - | - | (hb p. 9) |
| Condenser temperature | °C | nominal 21.5-22.5°C | - | - | (hb p. 9) |
| Optics temperature | °C | nominal 38.0-42.0°C | - | - | (hb p. 9) |
| Cabinet temperature | °C | 5-40 °C | - | - | (hb p. 9) |
| Ambient pressure | kPa | - | - | - | (hb p. 8) |
| Orifice pressure | kPa | minimum 50 kPa (or 50% of ambient... | - | - | (hb p. 9) |
| Nozzle pressure | kPa | maximum 3 kPa | - | - | (hb p. 9) |
| Laser current | mA | minimum 15 mA | - | - | (hb p. 9) |
| Working fluid liquid level | full/not full; fraction full | minimum fraction 0.5 | - | - | (hb p. 9) |
| Dilution flow set point | sccm | - | - | - | (hb p. 8) |
| Dilution flow measured | sccm | - | - | - | (hb p. 8) |
| Aerosol flow rate | lpm | 1.0 lpm nominal, ±5% variability | ±5% | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Detection size limit (D50) | 10 nm diameter | (hb p. 7) |
| Aerosol flow rate | 1.0 lpm | (hb p. 7) |
| Concentration range | 0 to 1x10^4 #/cc | (hb p. 7) |
| Input voltage | 100-240 VAC, 50/60 Hz, 210 W maximum | (hb p. 15) |
| Altitude (operating) | Up to 2000 m (6500 ft) | (hb p. 15) |
| Inlet Pressure (operating) | 75 to 105 kPa (0.74 to 1.05 atm) | (hb p. 15) |
| Operating Temperature | 10 to 35°C | (hb p. 15) |
| Ambient Humidity (operating) | 0 to 90% RH non-condensing | (hb p. 15) |
| External vacuum source requirement | at least 60 kPa (18 in. Hg) | (hb p. 15) |
| Warm-up time | approximately 10 minutes | (hb p. 15) |
| Working fluid | reagent-grade (greater than 99.9% purity) n-butyl alcohol (butanol) | (hb p. 15) |
| Maximum nozzle pressure threshold | 3 kPa | (hb p. 9) |
| Minimum orifice pressure threshold | 50 kPa (or 50% of ambient pressure) | (hb p. 9) |
| Nominal saturator temperature range | 38.5°C – 39.5°C | (hb p. 9) |
| Nominal condenser temperature range | 21.5°C – 22.5°C | (hb p. 9) |
| Nominal optics temperature range | 38.0°C-42.0°C | (hb p. 9) |
| Minimum butanol level (fraction) | 0.5 | (hb p. 9) |
| Minimum laser current | 15 mA | (hb p. 9) |
| Cabinet temperature range | 5-40 °C | (hb p. 9) |


## The data

Verified example: **`sgpaoscpcC1.b1`**, file `sgpaoscpcC1.b1.20170926.000000.nc`
(0.07 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 11 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2017-09-26T00:00:00 to 2017-09-26T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 1 minute |
| dod version | aoscpc-b1-1.7 |
| process version | ingest-aosdilutioncorr-1.7-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `concentration` | 1/cm^3 | time | yes | Particle concentration |
| `cpc_flow` | L/min | - | - | CPC flow rate |
| `dilution_correction_factor` | unitless | time | - | Dilution correction factor |
| `f2_flags` | unitless | time | - | CPC-specific flags |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaoscpcC1.b1", "2017-09-26", "2017-09-26")
ds = armlive_open("sgpaoscpcC1.b1", "2017-09-26", "2017-09-26", cleanup_qc=True)
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
11 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpaoscpcC1.b1.20170926.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `concentration` | f2_flags indicates "not_ready" | 569 | 39.5139 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaoscpcC1.b1", "20101014", "20260923")
```

The handbook's own note on data quality: Data quality is evaluated in two levels: (1) automated flagging by the Data Quality Office based on mentor-supplied thresholds on housekeeping variables (nozzle pressure, orifice pressure, saturator/condenser/optics temperature, butanol level, laser current, cabinet temperature) generating warnings or alarms; (2) automated diagnostic plots (via ARM Data Quality Diagnostic Plot Browser) showing housekeeping time series and comparisons with co-located instruments (CPCu/3776, SMPS, CCN) to assess stability and identify issues. Data processing levels: a1 (raw one-second serial data with firmware...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Statistical counting noise at low concentration | Higher relative uncertainty/scatter in concentration reading in clean environments (~2.5% at ~100 #/cc) vs polluted environments (~0.3% at ~5000 #/cc) | Accounted for via uncertainty propagation using relative statistical counting error sigma_r = sqrt(n)/n | (hb p. 12) |
| Inlet flow rate variability | Field inlet flow rate (not an online measurement) varies up to 5%, contributing primary error to concentration accuracy/repeatability | Weekly flow-rate verification with bubble flow meter; factory calibration | (hb p. 12) |
| Coincidence at high concentration | At high particle concentrations (above measurement range) counts undercounted unless corrected | Signal-processing electronics correct for concentration-dependent counting coincidence up to 1x10^4 #/cc; dilution flow system used for... | (hb p. 12) |
| Homogeneous nucleation of working fluid | Spurious particle counts/instrument noise not attributable to sampled aerosol, occurring when supersaturation too high | Operate at supersaturation level just below homogeneous nucleation limit | (hb p. 15) |
| Nozzle clogging | Nozzle pressure steadily increases over time, exceeding 3 kPa threshold, triggering warning flag | Clean nozzle per Appendix B procedure when pressure greater than 3 kPa and steadily increasing | (hb p. 12) |
| Insufficient vacuum/orifice pressure drop | Orifice pressure falls below 50 kPa (or 50% ambient pressure), indicating insufficient flow/vacuum | Warning generated; verify vacuum source provides at least 60 kPa | (hb p. 9) |
| Saturator temperature deviation | Saturator temperature outside 38.5-39.5°C causes deviation from expected butanol vapor pressure and shifts nominal 10 nm detection limit; triggers alarm | Alarm generated; monitor housekeeping temperature | (hb p. 9) |
| Condenser temperature deviation | Condenser temperature outside 21.5-22.5°C causes deviation in vapor saturation ratio and shifts detection limit; triggers alarm | Alarm generated | (hb p. 9) |
| Optics temperature deviation | Optics temperature outside 38.0-42.0°C could lead to vapor condensation on optics surface, triggers alarm | Alarm generated | (hb p. 9) |
| Low butanol/working fluid level | Butanol fill fraction below 0.5 may prevent sufficient vapor for proper particle growth/detection limit; triggers alarm | Refill butanol reservoir every 3 days; alarm generated below threshold | (hb p. 9) |
| Declining laser health | Laser current below 15 mA indicates degrading laser; triggers alarm | Alarm generated; monitor laser current housekeeping | (hb p. 9) |
| Cabinet temperature out of range | Cabinet temperature outside 5-40°C indicates abnormal CPC operation and may destabilize condenser/saturator/optics temperature control; triggers alarm | Alarm generated | (hb p. 9) |
| Zero check failure | CPC fails to read zero within 1 minute when sampling through HEPA filter | Indicates potential leaks, contamination in optical chamber, or dirty wick; perform weekly zero check | (hb p. 17) |
| Flooded optics | Indication of optics flooding (not detailed further) affecting particle detection | Correct flooded optics whenever indication occurs | (hb p. 17) |
| Wick degradation over time | Reduced butanol vapor delivery/dirty wick affecting particle growth and zero check performance | Replace CPC wick at campaign start and every 6-12 months during continuous usage | (hb p. 18) |
| Dilution correction not applied | High-concentration (greater than 1x10^4 #/cc) measurements recorded without dilution correction applied in current data, despite formula existing | Note: in recent years, dilution flow corrections have not been applied; currently no CPC uses any form of dilution correction | (hb p. 8) |
| Detection limit differs between co-located CPC models | 3772 (CPCf, 10 nm D50) concentration should always be equal to or smaller than co-located 3776/CPCu (3 nm D50) concentration; deviation from this relationship indicates a data quality issue | Compare co-located 3772 and 3776 time series as a quick assessment of relative CPC performance | (hb p. 12) |
| Counting efficiency dependent on particle composition and size | Counting efficiency curve varies with particle diameter and, to some extent, particle composition (e.g., silver vs sodium chloride) near the D50 detection limit | Determined via calibration protocol in Hermann et al. (2007) | (hb p. 16) |
| Butanol is flammable and toxic | Not a data artifact but a safety/handling caveat relevant to instrument operation | Handle with safety precautions; Class I laser, no exposure during normal operation | (hb p. 18) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated prior to installation: inlet flow rate verified with low-pressure drop-bubble flow meter; dilution flow system calibrated against mass flow controller set point using bubble flow meter; size-dependent particle counting efficiency determined per Hermann et al. (2007) protocol using tube-furnace-generated... (hb p. 16) |
| Calibration interval | Prior to installation/deployment; pre- and post-campaign comparisons in laboratory; regular factory service and calibration typically every 1 to 2 years; electrometer reference undergoes yearly calibration at TSI (hb p. 16) |
| Traceability | TSI Model 3068B Aerosol Electrometer serves as primary reference for characterizing CPC counting efficiency; electrometer calibrated yearly at TSI (hb p. 16) |
| Routine maintenance | Re-fill butanol reservoir every three days; drain butanol prior to shipment; verify flow rate weekly (should be 1.0 lpm ±5%); verify zero check weekly using HEPA capsule filter (should read zero within 1 minute); correct flooded optics when indicated; clean clogged nozzle when nozzle pressure greater than 3 kPa and... (hb p. 17) |
| Maintenance interval | Butanol refill: 3 days; flow/zero check: weekly; wick replacement: 6-12 months; factory service: 1-2 years (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Ultrafine condensation particle counter (CPCu, TSI Model 3776), Scanning Mobility Particle Sizer (SMPS), Cloud Condensation Nuclei counter (CCN), TSI Model 3068B Aerosol Electrometer, TSI Model 3080/82 Electrostatic Classifier, TSI Model 3085 Nano Differential Mobility Analyzer.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AC` | alternating current |
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `BNC` | Bayonet Neill–Concelman |
| `CCN` | cloud condensation nuclei |
| `CPC` | condensation particle counter |
| `CPCf` | fine-mode condensation particle counter |
| `CPCu` | ultrafine condensation particle counter |
| `EPCAPE` | Eastern Pacific Cloud Aerosol Precipitation Experiment |
| `HEPA` | high-efficiency particulate absorbing |
| `MAOS` | Mobile Aerosol Observing System |
| `RH` | relative humidity |
| `UTC` | Coordinated Universal Time |
| `VAC` | volts alternating current |


### References the handbook cites

- Hermann, M, B Wehner, O Bischof, HS Han, T Krinke, W Liu, A Zerrath, and A Wiedensohler. 2007. "Particle counting efficiencies of new TSI condensation particle counters." Journal of Aerosol Science 38(6): 674–682.
- Mordas, G, H Manninen, T Petäjä, P Aalto, K Hämeri, and M Kulmala. 2008. "On operation of the ultra-fine water-based CPC TSI 3786 and comparison with other TSI models (TSI 3776, TSI 3772, TSI 3025, TSI 3010, TSI 3007)."...
- Ahn, KH, and BYH Liu. 1990. "Particle activation and droplet growth processes in condensation nucleus counter I. Theoretical background." Journal of Aerosol Science 21(2): 249–261.
- Stolzenburg, MR, and PH McMurry. 1991. "An ultrafine aerosol condensation nucleus counter." Aerosol Science and Technology 14(1): 48–65.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/cpc_handbook.pdf (24 pages, DOE/SC-ARM-TR-145, by A Singh, C Kuang)
- Catalog record: ARM data-source index, `instrument_class_code=cpc`, read 2026-09-23
- Example file: `sgpaoscpcC1.b1.20170926.000000.nc` from `sgpaoscpcC1.b1`, 0.07 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
