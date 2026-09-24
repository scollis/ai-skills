---
name: arm-instrument-smps
description: ARM Scanning mobility particle sizer (smps) - handbook-derived instrument reference: measurement principle, reported quantities (Particle number-size distribution, Particle diameter, Sample Temperature, Sample Pressure, Mean Free Path, Gas Viscosity, Sheath Flow Rate, Aerosol Flow Rate), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaossmpsC1.b1) and the variable inventory of a real file. Use when working with smps data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - smps, Scanning mobility particle sizer, enaaossmpsC1.b1, Particle number-size distribution, Particle diameter, Sample Temperature, Sample Pressure, Mean Free Path, Gas Viscosity, Aerosols, TSI Incorporated, Model 3938 SMPS (long-column DMA, CFCf, EPCAPE, MAOS, nSMPS.
---

# SMPS - Scanning mobility particle sizer

The SMPS measures the ambient particle number-size distribution (dN/dlogDp) for aerosol particles from about 10 nm to 1000 nm mobility diameter by combining a differential mobility analyzer with a condensation particle counter, deployed in ARM's fixed and mobile Aerosol Observing System sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 25 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `smps` |
| Handbook | [DOE/SC-ARM-TR-147 / A Singh, C Kuang / April 2024](https://www.arm.gov/publications/tech_reports/handbooks/smps_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | TSI Incorporated, Model 3938 SMPS (long-column DMA, e.g. Model 3081/3083, with Model 3750/3772 CPC); nano-SMPS variant uses TSI Model 3085 DMA with TSI Model 3776 ultrafine CPC |
| Primary measurements | Aerosol concentration; Aerosol particle size; Aerosol particle size distribution; Hygroscopic growth |
| Record | 2012-06-27 to 2026-09-23 (active) |
| Datastreams with data | 40 across 14 sites |
| Sites | anx, asi, bnf, cor, crg, dst, ena, epc, guc, hou, mao, mos, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/smps |


## Credit

Everything this skill knows about the instrument is the work of **A Singh, C Kuang** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Singh, C Kuang. *Scanning Mobility Particle Sizer (SMPS) Instrument Handbook*, DOE/SC-ARM-TR-147, April 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/smps_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The SMPS neutralizes polydisperse aerosol to a known bipolar charge equilibrium using a Krypton-85 charger, then classifies particles by their electrical mobility in a long-column differential mobility analyzer (DMA) under a user-set electric field, selecting a known size fraction based on derived relationships between electrical mobility and DMA operating parameters such as applied voltage. The resulting monodisperse aerosol stream is passed to a condensation particle counter (CPC), which grows the particles by condensing supersaturated butanol vapor onto them so they can be optically detected and counted as they scatter laser light. By stepping the DMA voltage over a scan, the instrument builds up the full particle number-size distribution (dN/dlogDp), which is then inverted from raw counts and diameters assuming charge equilibrium was reached in the neutralizer. An inlet impactor upstream removes larger particles via inertial impaction before classification.

**Siting.** During ARM deployments, the 3938 SMPS samples within an environmentally controlled measurement container, in accordance with the manufacturer's environmental requirements. Nominal operating environmental conditions: altitude up to 2000 m (6500 ft), inlet pressure 75 to 105 kPa (0.74 to 1.05 atm), operating temperature 10 to 35°C, ambient humidity 0 to 90% relative humidity non-condensing; sample line humidity maintained below 40% using a multitube Nafion dryer (Perma Pure Model PD-070).

**Sampling.** native rate AIM data output imported at 5-min intervals at a1 level; reported every 5-min intervals (a1 level); averaging Scans per sample; each scan comprises a scan-up time and retrace time; data organized into hour-long text files (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle number-size distribution (dN/dlogDp) | #/cc | particle diameter 10 nm to 1000 nm... | - | - | (hb p. 7) |
| Particle diameter (mobility diameter) | nm | 8-10 nm (50% detection limit of... | ±2% sizing accuracy under typical operating... | - | (hb p. 8) |
| Sample Temperature | °C | - | - | - | (hb p. 8) |
| Sample Pressure | kPa | typical 97-102 kPa | - | - | (hb p. 8) |
| Mean Free Path | m | - | - | - | (hb p. 8) |
| Gas Viscosity | kg/(m*s) | - | - | - | (hb p. 8) |
| Sheath Flow Rate | lpm | nominally 5 lpm | ±2% variability | - | (hb p. 9) |
| Aerosol Flow Rate | lpm | nominally 1 lpm | ±5% variability | - | (hb p. 9) |
| CPC Inlet Flow Rate | lpm | nominally 1.0 lpm | ±5% | - | (hb p. 9) |
| Total integrated number concentration | #/cc | 1 to 1x10^7 #/cc | - | - | (hb p. 8) |
| DMA sheath flow temperature and relative humidity | °C / % | Sheath Flow RH maximum threshold 20% | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Particle diameter range (general/typical, 3750/3772 CPC) | 8-10 nm (50% detection limit of 3750/3772 CPC) to 500 nm (max applied voltage 10,000 volts, sheath flow rate 5 lpm) | (hb p. 8) |
| Particle number concentration range | 1 to 1x10^7 #/cc | (hb p. 8) |
| nSMPS particle diameter range (SGP site, 3085 DMA + 3776... | ~2.5 nm (50% detection limit of 3776 CPC) to ~65 nm (max applied voltage 10,000 volts, sheath flow rate 15 lpm) | (hb p. 8) |
| nSMPS particle number concentration range | 1 to 1x10^7 #/cc | (hb p. 8) |
| AMF3 BNF extended size range (3083 DMA + 3750 CPC) | 12-800 nm (extended from 10-500 nm) | (hb p. 8) |
| Charging efficiency accuracy | ±10% (Jiang et al. 2014) | (hb p. 8) |
| DMA sizing accuracy (5 lpm sheath flow, ±2% variability) | less than  ±2% | (hb p. 9) |
| Aerosol sample flow rate variability (assumed fixed 1 lpm) | ±5% | (hb p. 9) |
| Repeatability - CPC sample flow rate variability | ±5% | (hb p. 9) |
| Repeatability - DMA sheath flow rate variability | ±2% | (hb p. 9) |
| Counting uncertainty at ~100 #/cc (clean environment) | 2.5% | (hb p. 9) |
| Counting uncertainty at ~5000 #/cc (polluted environment) | 0.3% | (hb p. 9) |
| Sensitivity to particle size | ±2% under typical operating conditions | (hb p. 9) |
| Altitude (operating) | Up to 2000 m (6500 ft) | (hb p. 20) |
| Inlet Pressure (operating) | 75 to 105 kPa (0.74 to 1.05 atm) | (hb p. 20) |
| Operating Temperature | 10 to 35°C | (hb p. 20) |
| Ambient humidity (operating) | 0 to 90% relative humidity non-condensing | (hb p. 20) |
| Sheath flow rate (nominal, calibration) | nominally 5 lpm | (hb p. 21) |
| High-voltage probe range | capable of measuring up to 10,000 volts | (hb p. 21) |
| CPC inlet flow rate (nominal) | 1.0 lpm, with a variability of up to ±5% | (hb p. 21) |
| 3772 CPC nominal cut size | 10 nm (D50, particle diameter at 50% detection) | (hb p. 21) |
| Weekly flow rate check | 1.0 lpm ±5% for SMPS and 1.5 lpm ±5% | (hb p. 22) |
| Weekly zero check | less than 0.1 #/cm3 within two full scans (10 minutes) | (hb p. 22) |
| CPC wick replacement interval | beginning of campaign and every 6 to 12 months during continuous usage | (hb p. 23) |
| CPC factory service/calibration interval | typically every 1 to 2 years | (hb p. 23) |
| Nozzle cleaning threshold | nozzle pressure greater than  3 kPa and steadily increasing over time | (hb p. 23) |


## The data

Verified example: **`enaaossmpsC1.b1`**, file `enaaossmpsC1.b1.20260922.000000.nc`
(0.51 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=288, `bound`=2, `diameter_mobility`=192 |
| Data variables | 50 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2026-09-22T00:00:00 to 2026-09-22T23:55:00 |
| sampling interval | 5 minutes |
| dod version | aossmps-b1-2.1 |
| process version | ingest-aossmpscorr-1.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `dN_dlogDp` | 1/cm^3 | time,diameter_mobility | yes | Number size distribution, electrical mobility diameter |
| `total_N_conc` | 1/cm^3 | time | yes | Total number concentration from integrated size distribution, SMPS |
| `total_SA_conc` | nm^2/cm^3 | time | yes | Total surface area concentration from integrated size distribution,... |
| `total_V_conc` | nm^3/cm^3 | time | yes | Total volume concentration from integrated size distribution, SMPS |
| `DMA_characteristic_length` | cm | - | - | Characteristic length of DMA |
| `DMA_inner_radius` | cm | - | - | Inner radius of DMA |
| `DMA_outer_radius` | cm | - | - | Outer radius of DMA |
| `aerosol_flow` | L/min | time | - | Aerosol flow rate set point |
| `bypass_flow` | L/min | time | - | Bypass flow rate set point |
| `d50` | nm | time | - | 50 percent cut-point diameter of the impactor |
| `dD_to_dSA` | nm^2 | diameter_mobility | - | Surface area of one particle |
| `dD_to_dV` | nm^3 | diameter_mobility | - | Volume of one particle |
| `delay_time` | s | time | - | Time required for aerosol to flow from classifier exit to detector in... |
| `diameter_mobility` | nm | diameter_mobility | - | Midpoint of geometric mean mobility diameter |
| `diffusion_correction` | 1 | - | - | Diffusion correction |
| `gas_viscosity` | Pa*s | time | - | Gas viscosity |
| `geometric_mean` | nm | time | - | Mean diameter of size distribution using a geometric average |
| `geometric_std` | nm | time | - | Geometric standard deviation of lognormal function |
| `high_voltage` | V | time | - | High voltage reading |
| `hv_polarity` | 1 | - | - | HV polarity |
| `low_voltage` | V | time | - | Low voltage reading |
| `lower_size` | nm | time | - | Lower size limit |
| `mean` | nm | time | - | Number mean diameter of size distribution |
| `mean_free_path` | m | time | - | Mean free path |
| `median` | nm | time | - | Number median diameter of size distribution |
| `mode` | nm | time | - | Number mode diameter of size distribution |
| `multiple_charge_correction` | 1 | - | - | Multiple charge correction |
| `nanoparticle_agglomerate_mobility_analysis` | 1 | - | - | Nanoparticle agglomerate mobility analysis |
| `reference_gas_pressure` | kPa | - | - | Reference gas pressure |
| `reference_gas_temperature` | K | - | - | Reference gas temperature |


_11 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaossmpsC1.b1", "2026-09-22", "2026-09-22")
ds = armlive_open("enaaossmpsC1.b1", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

This datastream carries 50 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enaaossmpsC1.b1", start, end,
                  keep_variables=["dN_dlogDp", "total_N_conc", "total_SA_conc", "qc_dN_dlogDp", "qc_total_N_conc", "qc_total_SA_conc"])
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
50 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaossmpsC1.b1.20260922.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `dN_dlogDp` | Value is equal to missing_value. | 24192 | 43.75 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaossmpsC1.b1", "20120627", "20260923")
```

The handbook's own note on data quality: Data quality is evaluated at two levels. First, automated flagging by the Data Quality Office based on mentor-supplied thresholds, e.g., Sample Pressure 97-102 kPa, calibrated impactor flow 1.0±0.05 lpm, Status Flag (0=normal, 1=failed measurement due to CPC or classifier faults), Sheath Flow RH maximum 20%, and Sample RH less than 40% (maintained via Nafion dryer). CPC firmware also generates its own flags per manufacturer's manual. Second, automated diagnostic plots (via ARM's Data Quality Diagnostic Plot Browser) show housekeeping variable time series and comparisons/closure with...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Impactor clogging by debris | Sample pressure drifts outside the 97-102 kPa typical range | Monitor sample pressure; clean the impactor nozzle when there is indication of significant pressure drop | (hb p. 10) |
| Impactor flow deviation | Calibrated impactor flow deviates from 1.0 +/-0.05 lpm typical range | Monitor real-time calculated flow from pressure drop across impactor | (hb p. 10) |
| Instrument fault / failed measurement | Status Flag = 1 (failed scan) due to CPC faults (insufficient vacuum, saturator/condenser/optics temperature off set point) or classifier faults (sheath flow error, DMA voltage error,... | Flagged automatically; use Status Flag to exclude failed scans | (hb p. 10) |
| Wet aerosol / hygroscopic growth in sheath flow | Particles incorrectly mobility-classified (sized) due to diameter changes from ambient water uptake when sheath flow RH exceeds threshold | Sheath Flow Relative Humidity Maximum flag = 20%; sample RH maintained less than 40% using a multitube Nafion dryer (Perma Pure Model PD-070) | (hb p. 10) |
| CPC-triggered data quality flags | Flags triggered by CPC firmware errors | Refer to manufacturer's manual for CPC flag definitions | (hb p. 10) |
| Disagreement between co-located CPC and integrated SMPS concentration | Co-located 3772 CPC and integrated SMPS particle number concentration differ by more than ~±10% for particles between 10-500 nm | Use as quick assessment of SMPS performance versus 3772 CPC via automated comparison plots | (hb p. 10) |
| Statistical (Poisson) counting noise | Relative counting uncertainty of 1/sqrt(n): larger scatter/uncertainty in clean environments (~100 #/cc: 2.5% uncertainty) versus polluted environments (~5000 #/cc: 0.3% uncertainty) | - | (hb p. 14) |
| Aerosol sample flow rate not monitored online | Fixed assumed value of 1 lpm can vary by as much as ±5% in practice, biasing concentration/size accuracy | - | (hb p. 14) |
| Size-dependent aerosol charging efficiency uncertainty | Charging efficiency accuracy characterized as ±10% (Jiang et al. 2014), contributing to size distribution inaccuracy | - | (hb p. 14) |
| DMA sheath flow variability affecting sizing accuracy | Sheath flow variability of ±2% at 5 lpm results in particle sizing accuracy of less than ±2% | - | (hb p. 14) |
| Lower particle size detection limit set by CPC cut size | Particles below ~8-10 nm (3750/3772 CPC 50% detection limit) not counted, blind range at small end | Use nSMPS (3085 DMA + 3776 CPC) for ~2.5 nm lower limit if extended range needed | (hb p. 8) |
| Upper particle size limit set by max DMA voltage/sheath flow | Particles above 500 nm (at 10,000 V, 5 lpm sheath flow) not classified, blind range at large end | AMF3 BNF deployment extends range to 12-800 nm using 3083 DMA with 3750 CPC | (hb p. 8) |
| Homogeneous nucleation noise in CPC | Instrument noise from droplets formed without sampled particles present when super-saturation is too high | Operate CPC at super-saturation level just below the homogeneous nucleation limit | (hb p. 19) |
| Coincidence error at high particle concentration | Undercounting/bias at high particle concentrations due to multiple particles passing detector simultaneously | Electrical pulses corrected for particle coincidence at high concentrations | (hb p. 17) |
| Flooded CPC optics | Optical signal degraded or erroneous counts when optics are flooded with working fluid | Correct flooded optics when there is any indication of flooding | (hb p. 23) |
| Clogged CPC nozzle | Nozzle pressure greater than  3 kPa and steadily increasing over time | Clean clogged nozzle per manufacturer's manual procedure | (hb p. 23) |
| CPC wick degradation | Zero-check failure or counting anomalies related to CPC optics and wick | Replace CPC wick at beginning of campaign and every 6 to 12 months during continuous usage | (hb p. 22) |
| System leaks or CPC issues detected via zero check | SMPS fails to read near-zero (less than 0.1 #/cm3) within two full scans (10 minutes) during HEPA-filtered zero check | Weekly zero check with HEPA capsule filter at instrument inlet; investigate leaks or CPC optics/wick issues if failed | (hb p. 22) |
| Environmental operating range limits (temperature/humidity/altitude/pressure) | Data quality degrades or instrument may fault outside altitude up to 2000 m, inlet pressure 75-105 kPa, operating temperature 10-35°C, ambient humidity 0-90% RH non-condensing | Sample within environmentally controlled measurement container per manufacturer's environmental requirements | (hb p. 20) |
| Butanol working fluid handling | Not a data artifact but a safety/logistics issue: butanol is flammable and toxic if inhaled | Drain butanol from reservoir prior to instrument shipment | (hb p. 23) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Verify sheath flow rate with low-pressure drop-bubble flow meter; verify high-voltage power supply with high-voltage probe (up to 10,000 volts); verify mobility classifier particle sizing with NIST-certified polystyrene latex particle size standards (150 nm); determine CPC size-dependent counting efficiency using... (hb p. 21) |
| Calibration interval | Prior to installation/deployment; CPC factory service and calibration typically every 1 to 2 years (hb p. 21) |
| Traceability | NIST-certified polystyrene latex particle size standards (hb p. 21) |
| Routine maintenance | Clean impactor nozzle when significant pressure drop indicated; verify flow rate weekly with a low-pressure drop-bubble flowmeter (should read 1.0 lpm ±5% for SMPS and 1.5 lpm ±5%); verify zero check weekly using a HEPA capsule filter at instrument inlet (should read less than 0.1 #/cm3 within two full scans/10... (hb p. 22) |
| Maintenance interval | Weekly flow and zero checks; wick replacement every 6-12 months; CPC factory calibration every 1-2 years (hb p. 22) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: CPC, CFCf (fine-mode condensation particle counter), APS (aerodynamic particle sizer), UHSAS (ultra-high-sensitivity aerosol spectrometer), OPC (optical particle counter), nSMPS (nano-scanning mobility particle sizer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AIM` | Aerosol Instrument Manager |
| `AOS` | Aerosol Observing System |
| `APS` | aerodynamic particle sizer |
| `ARM` | Atmospheric Radiation Measurement |
| `BNF` | Bankhead National Forest |
| `CPC` | condensation particle counter |
| `CFCf` | fine-mode condensation particle counter |
| `DMA` | differential mobility analyzer |
| `EPCAPE` | Eastern Pacific Cloud Aerosol Precipitation Experiment |
| `MAOS` | Mobile Aerosol Observing System |
| `nSMPS` | nano-scanning mobility particle sizer |
| `OPC` | optical particle counter |
| `RH` | relative humidity |
| `SMPS` | scanning mobility particle sizer |


### References the handbook cites

- Ahn, K-H and BYH Liu. 1990. Journal of Aerosol Science 21(2): 249-261
- Friedlander, SK. 2000. Smoke, Dust, and Haze. Wiley, New York.
- Fuchs, NA. 1964. The Mechanics of Aerosols. Pergamon Press, New York.
- Hermann, M, B Wehner, O Bischof, HS Han, T Krinke, W Liu, A Zerrath, and A Wiedensohler. 2007. Journal of Aerosol Science 38(6): 674-682
- Hinds, WC. 2012. Aerosol Technology: Properties, Behavior, and Measurement of Airborne Particles. John Wiley and Sons, New York.
- Jiang, J, C Kim, X Wang, MR Stolzenburg, SL Kaufman, C Qi, GJ Sem, H Sakurai, N Hama, and PH McMurry. 2014. Aerosol Science and Technology 48(12): 1207-1216
- Knutson, EO, and KT Whitby. 1975. Journal of Aerosol Science 6(6):443-451
- Knutson, EO. 1976. In Fine Particles: Aerosol Generation, Measurement, Sampling, and Analysis. Academic Press, New York, pp. 739-762.
- Wiedensohler, A. 1988. Journal of Aerosol Science 19(3): 387-389

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/smps_handbook.pdf (25 pages, DOE/SC-ARM-TR-147, by A Singh, C Kuang)
- Catalog record: ARM data-source index, `instrument_class_code=smps`, read 2026-09-23
- Example file: `enaaossmpsC1.b1.20260922.000000.nc` from `enaaossmpsC1.b1`, 0.51 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
