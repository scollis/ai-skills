---
name: arm-instrument-ins
description: ARM Ice Nucleation Spectrometer for INP measurement (ins) - handbook-derived instrument reference: measurement principle, reported quantities (Freezing temperature, INP number concentration), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpinpC1.a1) and the variable inventory of a real file. Use when working with ins data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - ins, Ice Nucleation Spectrometer for INP measurement, sgpinpC1.a1, Freezing temperature, INP number concentration, Aerosols, TSI Mass Flow Meter 5200-1, TRAPS, CACTI, SAIL.
---

# INS - Ice Nucleation Spectrometer for INP measurement

The Ice Nucleation Spectrometer (INS) is an offline analytical instrument that processes filter samples collected at ARM facilities (and via tethered balloon system) to measure immersion-mode ice nucleating particle (INP) freezing temperature spectra and number concentrations in aerosols.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ins` |
| Handbook | [DOE/SC-ARM-TR-278 / JM Creamean, TCJ Hill, CC Hume, T Devadoss / March 2024](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-278.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Filter units: Nalgene Sterile Analytical Filter Units (modified) with Whatman Nuclepore Track-Etched Membrane filters; TSI Mass Flow Meter 5200-1; Thomas 2688CE44 Oil-less Piston Compressor/Vacuum... |
| Primary measurements | Ice Nucleating Particle (INP) Concentration |
| Record | 2020-08-20 to 2026-09-23 (retired) |
| Datastreams with data | 22 across 9 sites |
| Sites | bnf, crg, epc, guc, hou, kcg, nsa, oli, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/ins |


## Credit

Everything this skill knows about the instrument is the work of **JM Creamean, TCJ Hill, CC Hume, T Devadoss** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> JM Creamean, TCJ Hill, CC Hume, T Devadoss. *Ice Nucleation Spectrometer (INS) Instrument Handbook*, DOE/SC-ARM-TR-278, March 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-278.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The INS mimics immersion freezing of cloud ice, whereby an INP first serves as a cloud condensation nucleus and then freezes at temperatures above homogeneous freezing (-38 degC), via heterogeneous ice nucleation. Aerosol particles collected on filters are resuspended in filtered deionized water, and 50-uL aliquots of serial dilutions are dispensed into 96-well PCR trays that are cooled at 0.33 degC per minute in aluminum incubation blocks. Freezing events in each well are detected automatically every 0.5 degC via a CCD camera/LabVIEW interface, and the fraction of frozen droplets at each temperature is used with the known volume of air filtered to calculate INP number concentration using the Vali (1971) equation. Thermal and peroxide-digestion treatments of sub-samples are used to partition the total INP spectrum into heat-labile (biological), bio-organic, and inorganic/mineral INP components.

**Siting.** Filter units are open-faced, secured outside to the ARM Aerosol Observing System (AOS) railing, and shielded from precipitation. Filters are collected at select ARM facilities and transferred to CSU for offline analysis. INP sampling is also occasionally conducted on the ARM tethered balloon system (TBS) at select sites.

**Sampling.** native rate Camera images every 20 seconds (~0.1 degC); freezing recorded every 0.5 degC; reported every Filter collection typically 24 hours (range 2-72 hours); TBS samples 30 min to 2 hours; averaging For each set of double blocks, readings from two thermocouples are averaged (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Freezing temperature | degC | 0 to approximately -27 to -29 degC | +/- 0.2 degC | 0.5 degC intervals... | (hb p. 9) |
| INP number concentration | L-1 STP (STP = 0 degC and... | detection limit 0.0002 INPs L-1 (24-hr... | 95% CI via binomial sampling (Agresti and Coull... | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Cooling rate | 0.33 degC min-1 | (hb p. 8) |
| Freezing detection interval | every 0.5 degC | (hb p. 8) |
| Aliquot volume | 50 uL | (hb p. 8) |
| Wells per PCR tray | 96-well trays, four trays per run | (hb p. 8) |
| Total aliquots per run | 384 x 50 uL aliquots | (hb p. 8) |
| Aliquots per dilution level | typically 32 | (hb p. 9) |
| Serial dilutions | up to five, 11- to 15-fold serial dilutions | (hb p. 9) |
| Headspace purge gas flow | 750 mL min-1 cooled, HEPA-filtered N2 | (hb p. 9) |
| Filter pore size | 0.2-um polycarbonate filters backed with 10-um polycarbonate filters, 47-mm diameter Whatman Nuclepore Track-Etched Membranes | (hb p. 6) |
| Filter collection duration | typically 24 hours (option 2 to 72 hours) | (hb p. 7) |
| Mass flow meter accuracy | TSI 5200-1, +/-2% | (hb p. 12) |
| Reference mass flow meter accuracy | TSI 5230, 1.7% accuracy | (hb p. 12) |
| Temperature uncertainty | +/- 0.2 degC | (hb p. 13) |
| Heat treatment | 95 degC for 20 min on 2.5 mL sample suspension | (hb p. 9) |
| Peroxide digestion | 2 mL suspension in 10% H2O2 solution, heated to 95 degC for 20 min with UV-B illumination | (hb p. 9) |
| TBS filter flow rate | typically 0.5-1 Slpm | (hb p. 11) |
| TBS sample duration | 30 minutes to 2 hours per sample | (hb p. 11) |
| Pump vacuum capability | 0.5 kPa vacuum (Thomas 2688CE44 pump, when operating efficiently) | (hb p. 16) |


## The data

Verified example: **`sgpinpC1.a1`**, file `sgpinpC1.a1.20250203.142700.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1, `temperature`=106 |
| Data variables | 12 |
| QC variables | 0 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2025-02-03T14:27:00 to 2025-02-03T14:27:00 |
| dod version | inp-a1-1.2 |
| process version | ingest-inp-1.4-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `lower_ci` | count/L | time,temperature | - | 95% lower confidence limit for number of ice nucleating particles per... |
| `n_inp_stp` | count/L | time,temperature | - | Number of ice nucleating particles per L of air at STP |
| `start_utc` | - | time | - | Filter collection start time |
| `stop_utc` | - | time | - | Filter collection end time |
| `temperature` | degC | temperature | - | Freezing temperature |
| `time` | - | time | - | Time offset from midnight |
| `total_volume` | L | time | - | Total volume of air passed through filter at STP |
| `treatment_flag` | 1 | time,temperature | - | Treatment flag |
| `upper_ci` | count/L | time,temperature | - | 95% upper confidence limit for number of ice nucleating particles per... |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpinpC1.a1", "2025-02-03", "2025-02-03")
ds = armlive_open("sgpinpC1.a1", "2025-02-03", "2025-02-03", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `treatment_flag`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpinpC1.a1", "20200820", "20260923")
```

The handbook's own note on data quality: A QA/QC flow diagram governs protocols for INP measurement (Figure 5): quality assurance ensures requirements are fulfilled for ARM management and end users, while quality control maintains requirements via inspection and testing against pre-specified performance characteristics. QC includes monitoring in-line pressure and flow rate during filter collection, use of DI water and H2O2/catalase blanks in every INS run, thermocouple calibration/averaging, checking camera images against automated freezing detection on every run, use of binomial 95% confidence intervals (Agresti and Coull 1998) for...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Limit of measurement / temperature range boundary | INP spectra truncated between -27 and -29 degC depending on background INPs in the DI water used for resuspension | Baseline (DI water blank) INP concentration is subtracted before subsequent calculations | (hb p. 9) |
| Leaks in filter unit, tubing, or connections during sample collection | Significant change in pressure and/or flow rate between start and end of filter collection | Monitor in-line pressure and flow rate at start and end of collection to determine if sampling errors occurred | (hb p. 12) |
| Flow rate decrease over sampling period | Total volume filtered would be inaccurate if flow rate change not accounted for | Use totalizing mass flow meter (TSI 5200-1) updating every second to accurately measure total volumes filtered | (hb p. 12) |
| Mass flow meter drift | TSI 5200 unit reading differs from TSI 5230 reference by more than 5% | Units more than 5% adrift are returned to TSI for servicing and calibration | (hb p. 12) |
| Contamination of filters/samples with INPs from laboratory surfaces or consumables... | Elevated background INP concentration in blank samples | Comprehensive cleanliness protocol during sample preparation (Barry et al. 2021); pipets calibrated annually | (hb p. 13) |
| INP contamination in DI water used for resuspension | Non-zero freezing signal in DI water blank run | A 0.1-um filtered DI water blank is included in each INS run to correct for INPs present in PCR trays and DI water | (hb p. 13) |
| INP contamination in hydrogen peroxide/catalase used for digestion | Non-zero freezing signal in H2O2 blank (DI water in place of sample) | Blanks are run for H2O2 digestions to check for contamination | (hb p. 13) |
| Temperature measurement uncertainty across PCR blocks | Variation in freezing temperature readings across blocks due to cooling gradients | Thermocouple placed just below wells in each of four PCR blocks; readings from two thermocouples per double block are averaged; combined uncertainty... | (hb p. 13) |
| N2 purge gas warming aliquots | Aliquots could be warmed by incoming purge gas, biasing freezing temperature | HEPA-filtered N2 purging headspace is precooled to a few degrees above block temperature to prevent warming the aliquots | (hb p. 13) |
| Program/automated detection errors during freezing runs | Discrepancy between automated freezing detection output and camera images | Camera images taken every 20 seconds (~0.1 degC) are checked against automated detection output on every run | (hb p. 13) |
| Statistical uncertainty from small numbers of frozen wells (binomial sampling) | Wide 95% confidence intervals when few wells are frozen, e.g., ~0.2 to ~5.5x estimated concentration for 1/32 wells frozen vs ~0.6 to ~1.6x for 16/32 wells frozen | Binomial sampling confidence intervals (95% CI) derived following Agresti and Coull (1998) are reported alongside INP concentration | (hb p. 13) |
| Sample degradation or change during frozen storage | Differences between INP spectra measured immediately after resuspension versus after frozen storage of the suspension | Repeatability confirmed via re-testing suspensions after frozen storage (pulse-vortexed after thawing); results shown to be within method's inherent... | (hb p. 13) |
| Filter-to-filter variability | Differences in INP spectra between replicate filters taken at the same site | Replicate filters tested to confirm comparability of INP spectra | (hb p. 14) |
| Field/background contamination during filter collection and handling | Elevated INP concentration on field/handling blank filters relative to true ambient | Field filter unit blanks prepared identically to sampling filters and exposed briefly at sampling position to monitor contamination; used to obtain... | (hb p. 14) |
| TBS/IcePuck flow rate reduction in cold temperatures | Lower measured flow rates through sample and backing filters at colder ambient temperatures | None specified beyond noting the effect; flow typically 0.5-1 Slpm | (hb p. 11) |
| TBS ascent sample not representative | First sample collected during balloon ascent (less than 30 minutes) shows different/unusable characteristics | First (ascent) sample is not used for analysis | (hb p. 11) |
| Flammable/toxic chemicals used in processing | Not a data artifact but a handling hazard: 30% H2O2, catalase, methanol, SYLTHERM XLT are used during collection and processing | Handle chemicals with appropriate safety precautions (flammable and/or toxic) | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | TSI 5200 mass flow meters checked against TSI 5230 meter (enhanced 1.7% accuracy, reserved for this purpose); pipets calibrated annually (hb p. 12) |
| Calibration interval | Mass flow meters checked annually; pipets calibrated annually (hb p. 12) |
| Traceability | TSI 5230 reference meter used as calibration standard for TSI 5200-1 field meters (hb p. 12) |
| Routine maintenance | Check in-line temperature, pressure, and flow rate at start and end of sample collection; clean precipitation shields as needed; check for leaks in filter units and vacuum tubing; check TSI 5200 mass flow meters against TSI 5230; check pump performance (should produce 0.5 kPa vacuum); clean plexiglass lids with Windex... (hb p. 16) |
| Maintenance interval | Plexiglass lids cleaned every two weeks; lab space deep-cleaned once per month; mass flow meters checked annually; other checks as needed or at start/end of each sample collection (hb p. 16) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Colorado State University (CSU) Ice Spectrometer (IS), ARM Aerosol Observing System (AOS), ARM tethered balloon system (TBS), IcePuck (Handix Scientific, Inc.), Time-Resolved Aerosol Particle Sampler (TRAPS), Continuous Light Absorption Photometer.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `INP` | ice nucleating particle |
| `IN` | ice nuclei (used interchangeably with INP) |
| `INS` | ice nucleation spectrometer |
| `IS` | Ice Spectrometer (CSU design nearly identical to the INS) |
| `CCN` | cloud condensation nuclei |
| `STP` | standard temperature and pressure (0 degC and 101.32 kPa) |
| `TBS` | tethered balloon system |
| `TRAPS` | Time-Resolved Aerosol Particle Sampler |
| `AOS` | Aerosol Observing System |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions (ARM field campaign) |
| `SAIL` | Surface Atmosphere Integrated Field Laboratory |
| `AMF` | ARM Mobile Facility |
| `CI` | confidence interval |
| `QA` | quality assurance |


### References the handbook cites

- Vali, G. 1971. Quantitative Evaluation of Experimental Results and the Heterogeneous Freezing Nucleation of Supercooled Liquids. J. Atmos. Sci. 28(3): 402-409
- Agresti, A, and BA Coull. 1998. Approximate Is Better than 'Exact' for Interval Estimation of Binomial Proportions. The American Statistician 52(2): 119-126
- Barry, KR, TCJ Hill, C Jentzsch, BF Moffett, F Stratmann, and PJ DeMott. 2021. Pragmatic protocols for working cleanly when measuring ice nucleating particles. Atmospheric Research 250: 105419
- DeMott, PJ, et al. 2017. Comparative measurements of ambient atmospheric concentrations of ice nucleating particles using multiple immersion freezing methods and a continuous flow diffusion chamber. ACP 17(18):...
- DeMott, PJ, et al. 2018b. The Fifth International Workshop on Ice Nucleation phase 2 (FIN-02): laboratory intercomparison of ice nucleation measurements. AMT 11(11): 6231-6257
- McCluskey, CS, et al. 2018. Observations of Ice Nucleating Particles over Southern Ocean Waters. GRL 45(21): 11,989-11,997
- Suski, KJ, et al. 2018. Activation of intact bacteria and bacterial fragments mixed with agar as cloud droplets and ice crystals in cloud chamber experiments. ACP 18(23): 17497-17513
- Testa, B, et al. 2021. Ice Nucleating Particle Connections to Regional Argentinian Land Surface Emissions and Weather during CACTI. JGR-Atmospheres 126(23): e2021JD035186
- Beall, CM, et al. 2017. Automation and heat transfer characterization of immersion mode spectroscopy for analysis of ice nucleating particles. AMT 10(7): 2613-2626
- Ogren, JA, J Wendell, E Andrews, and PJ Sheridan. 2017. Continuous light absorption photometer for long-term studies. AMT 10(12): 4805-4818

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-278.pdf (21 pages, DOE/SC-ARM-TR-278, by JM Creamean, TCJ Hill, CC Hume, T Devadoss)
- Catalog record: ARM data-source index, `instrument_class_code=ins`, read 2026-09-23
- Example file: `sgpinpC1.a1.20250203.142700.nc` from `sgpinpC1.a1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
