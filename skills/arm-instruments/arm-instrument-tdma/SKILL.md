---
name: arm-instrument-tdma
description: ARM Tandem Differential Mobility Analyzer (tdma) - handbook-derived instrument reference. Measurement principle, reported quantities (DMA-only size distribution, APS-only size distribution, DMA+APS size distribution), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptdmaapssizeC1.c1) and the variable inventory of a real file. Use when working with tdma data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - tdma, Tandem Differential Mobility Analyzer, sgptdmaapssizeC1.c1, DMA-only size distribution, APS-only size distribution, DMA+APS size distribution, Aerosols, TSI, Inc. model 3321 Aerodynamic Particle Sizer (APS), TDMA, AS-DMA, NaCl, TAMU.
---

# TDMA - Tandem Differential Mobility Analyzer

The TDMA/APS system measures size-resolved submicron and supermicron aerosol particle number size distributions and size-resolved hygroscopic growth (and intermittently volatility and ambient hydration state) of dry particles, deployed as a ground-based instrument at the ARM SGP/C1 site.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `tdma` |
| Handbook | [DOE/SC-ARM-TR-090 / Don Collins / June 2010](https://www.arm.gov/publications/tech_reports/handbooks/tdma_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | TSI, Inc. model 3321 Aerodynamic Particle Sizer (APS); Texas A&M University-developed Tandem Differential Mobility Analyzer (TDMA) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution; Hygroscopic growth; Particle number concentration |
| Record | 2005-10-07 to 2014-11-20 (retired) |
| Datastreams with data | 3 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tdma |


## Credit

Everything this skill knows about the instrument is the work of **Don Collins** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> Don Collins. *Tandem Differential Mobility Analyzer/Aerodynamic Particle Sizer (APS) Handbook*, DOE/SC-ARM-TR-090, June 2010.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tdma_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The TDMA operates as a scanning DMA to measure dry submicron size distributions and as a tandem DMA to measure size-resolved hygroscopic growth: sample aerosol is dried, brought to a bipolar charge equilibrium, size-selected by voltage-scanning through a first DMA, then either measured directly (size distribution mode) or exposed to controlled 90% RH before a second DMA scans the humidified size distribution (hygroscopicity mode), with a CPC counting the size-selected particles. Particle mobility diameter selected by the DMA is a function of the ratio of applied high voltage to sheath flow rate, with voltage ramped exponentially from ~7V to over 8000V. The APS extends the size range into the supermicron range by accelerating the sample flow through a nozzle so that particle aerodynamic size determines acceleration (larger particles accelerate less due to inertia); particles are sized from the time-of-flight between two overlapping laser beams downstream of the nozzle. A data inversion algorithm combines the DMA and APS number size distributions into a single distribution spanning both ranges.

**Siting.** TDMA/APS deployed at ARM Southern Great Plains (SGP) site, C1 facility; TDMA in AOS trailer since 2005/10/01, APS added 2008/07/01. For ambient state operation, sample enters an upstream DMA (AS-DMA) located outside the AOS trailer in a weatherproof and reflective enclosure; ambient hydration state measurements are only made when outside temperature and RH are within acceptable ranges.

**Sampling.** reported every Approximately 45 minutes for a complete normal measurement sequence (size distribution + hygroscopic growth distributions); APS sample time (current configuration) 600 s; averaging Each recorded size distribution is the average of an up-scan and down-scan pair; hygroscopic growth measurements repeated at a given size until a minimum number of particles are detected or a maximum number of measurements are made (up to ~10 minutes for smallest/largest sizes) (hb p. 17).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| DMA-only size distribution (dry particle number size... | cm-3 | 0.012-0.74 µm diameter | - | 1201 size bins | (hb p. 3) |
| APS-only size distribution (dry particle number size... | cm-3 | 0.4- ~15 µm diameter | - | 2151 size bins | (hb p. 3) |
| DMA+APS size distribution (dry particle number size... | cm-3 | 0.012- ~15 µm diameter | - | 2151 size bins | (hb p. 3) |
| Hygroscopic growth factor distribution (size-resolved... | cm-3 (normalized) | - | - | 1201 growth factor bins | (hb p. 3) |


## Specifications

| parameter | value | source |
|---|---|---|
| APS Particle size range | 0.5 to 20 mm aerodynamic diameter | (hb p. 17) |
| APS Size resolution | 0.02 mm at 1.0 mm, 0.03 mm at 10 mm | (hb p. 17) |
| APS Size bins in distribution | 52 | (hb p. 17) |
| APS Upper concentration limit | 10,000 cm-3 with coincidence correction | (hb p. 17) |
| APS Sample time (current configuration) | 600 s | (hb p. 17) |
| APS Aerosol flow rate | 1 L/min | (hb p. 17) |
| APS Sheath flow rate | 4 L/min | (hb p. 17) |
| TDMA Particle size range | 0.013 to 0.75 mm electric mobility diameter | (hb p. 17) |
| TDMA Size resolution | 0.0026 mm at 0.05 mm, 0.013 mm at 0.2 mm | (hb p. 17) |
| TDMA Size bins in distribution | 75 | (hb p. 17) |
| TDMA Sample time | Approximately 45 minutes for complete sequence | (hb p. 17) |
| TDMA Aerosol flow rate | 1.2-2.8 L/min, dependent upon measured size | (hb p. 17) |
| TDMA Sheath flow rate | 10 x aerosol flow rate | (hb p. 17) |
| TDMA sample flow rate (normal operation) | 3 liters per minute | (hb p. 15) |
| Inter-DMA relative humidity setpoint | 90% | (hb p. 11) |


## The data

Verified example: **`sgptdmaapssizeC1.c1`**, file `sgptdmaapssizeC1.c1.20141117.001000.cdf`
(0.03 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=15, `diameter`=215, `aqc_test`=7 |
| Data variables | 15 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 4935 s |
| File time span | 2014-11-17T00:10:00 to 2014-11-17T23:00:09 |
| dod version | tdmaapssize-c1-1.0 |
| process version | $State: xdc-tdmaapssize-1.1-6 $ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `number_concentration_DMA_APS` | 1/cm^3 | time,diameter | yes | Size-resolved particle number concentration (dN/dlogDP) from... |
| `aqc_number_concentration_DMA_APS` | unitless | time,aqc_test | - | Auxiliary quality check results on field: Size-resolved particle... |
| `correlation_up_down_DMA` | unitless | time | - | Correlation coefficient between up and down scan distributions from... |
| `diameter` | um | diameter | - | Particle diameter |
| `integrated_number_concentration_DMA` | 1/cm^3 | time | - | Integrated number concentration from differential mobility analyzer |
| `integrated_volume_concentration_APS` | um^3/cm^3 | time | - | Integrated volume concentration from aerosol particle sizer |
| `integrated_volume_concentration_DMA` | um^3/cm^3 | time | - | Integrated volume concentration from differential mobility analyzer |
| `ratio_volume_conc_6to5_DMA` | unitless | time | - | Ratio of the amplitude (dV/dlogDp) of the volume concentration at... |
| `ratio_volume_concentration_12to10_APS` | unitless | time | - | Ratio of the amplitude (dV/dlogDp) of the volume concentration at... |
| `size_range_residual_DMA_and_APS` | unitless | time | - | Average residual ([(dN/dlogDp)DMA - (dN/dlogDP)APS]/(dN/dlogDp)DMA)... |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgptdmaapssizeC1.c1", "2014-11-17", "2014-11-17")
ds = armlive_open("sgptdmaapssizeC1.c1", "2014-11-17", "2014-11-17", cleanup_qc=True)
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
15 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgptdmaapssizeC1.c1.20141117.001000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `number_concentration_DMA_APS` | (DMA only) Number Concentration less than 100 cm^-3 OR greater... | 15 | 100.0 |
| `number_concentration_DMA_APS` | (DMA only) Volume Concentration less than 0.2 um^3/cm^3 OR... | 15 | 100.0 |
| `number_concentration_DMA_APS` | (DMA only) Unexpected volume concentration distribution slope... | 15 | 100.0 |
| `number_concentration_DMA_APS` | (Both DMA, APS) Average residual between the measured DMA and... | 15 | 100.0 |
| `number_concentration_DMA_APS` | (APS only) Volume Concentration less than 0.5 um^3/cm^3 OR... | 12 | 80.0 |
| `number_concentration_DMA_APS` | (APS only) Volume Concentration less than 0.2 um^3/cm^3 OR... | 3 | 20.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgptdmaapssizeC1.c1", "20051007", "20260923")
```

The handbook's own note on data quality: Data quality flags (value 0 = no flag) are applied per distribution. For size distributions: number concentration out-of-range (col 2), volume concentration out-of-range (col 3), unexpected volume concentration distribution slope (col 4), poor correlation between up/down scan distributions (col 5) - flag value 1 = somewhat unusual/possibly inaccurate but still used in calculated products, flag value 2 = highly unusual/likely inaccurate and excluded from calculated products. For hygroscopic growth factor distributions: relative humidity out of range (col 2), excessive number of peaks (col 3),...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| False count rate / leak in DMA | Positive bias in the slope of the retrieved volume distribution near the upper size limit (0.5-0.6 µm); ratio of dV/dlogDp at 0.6 µm to 0.5 µm elevated, flagged by column 4 of size... | Flag distributions with unexpected volume concentration slope; a leak rate of 1% of total flow gives ~1000 false counts/s, monitored via nightly leak... | (hb p. 9) |
| Number concentration out of range | Integrated number concentration less than 300 or greater than 30,000 cm-3 (flag 1); less than 100 or greater than 100,000 cm-3 (flag 2); often indicates instrumentation problem such as... | Flagged in column 2 of size distribution flags; distributions with flag 2 excluded from calculated products | (hb p. 9) |
| Volume concentration out of range | Integrated volume concentration less than 0.5 or greater than 40 µm3/cm3 (flag1); less than 0.2 or greater than 80 µm3/cm3 (flag2); can result from nearby fires (high) or long rainy periods... | Flagged in column 3 of size distribution flags | (hb p. 9) |
| Poor correlation between up and down scan distributions (size distribution) | Correlation between up-scan and down-scan distributions less than 0.9 (flag1) or less than 0.3 (flag2); instrumentation problems or abrupt aerosol changes cause differences | Flagged in column 5 of size distribution flags | (hb p. 10) |
| Inter-DMA relative humidity out of range | Inter-DMA RH less than 83% or greater than 93% (flag1), less than 78% or greater than 96% (flag2); RH may not fully stabilize after size distribution scan when there is no flow between DMAs | Correction applied to adjust distributions to 90% RH equivalent; two-minute wait after size distribution scan before hygroscopic growth measurement... | (hb p. 10) |
| Excessive number of peaks in hygroscopic growth factor distribution | More than six peaks (flag1) or more than nine peaks (flag2) in growth factor distribution, indicating noisy/inaccurate raw data despite smoothing by inversion algorithm | Flagged in column 3 of hygroscopic growth flags | (hb p. 11) |
| Tails of hygroscopic growth distribution too high | dN/dlogDp at first or last growth factor bin greater than 5% of max (flag1) or greater than 15% of max (flag2); typically result of false counts; most common at smallest (0.013 µm) and... | Flagged in column 4 of hygroscopic growth flags; several steps taken to minimize but impact still sometimes observed | (hb p. 12) |
| Poor correlation between up and down scan distributions (hygroscopic growth) | Correlation less than 0.4 (flag1) or less than 0.0 (flag2); far more hygroscopicity distributions flagged for this than size distribution measurements due to lower count rates | Flagged in column 5 of hygroscopic growth flags | (hb p. 12) |
| Location of peak in growth factor distribution out of range | Peak growth factor less than 0.98 or greater than 2.1 (flag1); less than 0.93 or greater than 2.3 (flag2); peaks left of 1.0 suggest particle shrinkage or right of ~2 could reflect... | Checks follow application of zero and span corrections from nightly calibration, so drift should not displace peaks outside expected range; flagged... | (hb p. 12) |
| Insufficient number of particles counted | Fewer than 15 particles detected during measurement (flag1) or fewer than 5 (flag2); occurs especially at 0.013 and 0.6 µm sizes even after up to 10 minutes of repeated measurement | Software repeats measurement at a given size until minimum particle count or maximum number of scans reached; flagged in column 7; exceedingly low... | (hb p. 13) |
| High voltage offset error | Offset error in applied high voltage biases sizing more at small diameter end (near 0.012 µm, ~7V) than large diameter end (near 0.75 µm, ~8000V); shifts dry diameters at which hygroscopic... | High voltage monitored and correction applied in data inversion; cause of offsets not determined, adjustments made when observed | (hb p. 11) |
| Non-exponential high voltage ramp assumption error | Error introduced in HV offset correction because actual high voltage ramp is not exponential as assumed in data inversion | None beyond noting the limitation | (hb p. 11) |
| Noisy calibration at size distribution extremes | Calibration aerosol (NaCl, peak just under 0.1 µm) has very low concentration at smallest and largest TDMA sizes, producing noisy calibration distributions and unreliable growth factor... | Several steps taken to minimize the problem, but impact still sometimes observed | (hb p. 11) |
| Persistent spike/dip on right-hand side of supermicron mode (APS) | A persistent point/spike appears on the right-hand side of the mode in the supermicron size distribution | Errors in size-dependent slope of time-of-flight-to-size relationship cause wider/narrower than assumed bin boundaries; a thorough APS calibration is... | (hb p. 12) |
| APS sizing uncertainty at size range tails | Greater sizing uncertainty near the tails of the 0.5-20 µm APS range | - | (hb p. 19) |
| Missing combined DMA+APS size distribution data at time of writing | Only TDMA-only size distribution data available in archive; combined product not yet available | Handbook states it will be available soon; refer to tdmasize datastream and Data Object Design documentation in the meantime | (hb p. 7) |
| Housekeeping data not archived | Instrument RH probes (5), temperature, flow rates, and high voltages recorded continuously but not uploaded to ARM Data Archive | Archived with instrument mentor instead; available upon request | (hb p. 12) |
| Values of -999 outside instrument range | Size bins outside the measurement range of the instrument(s) are filled with -999 in the fixed diameter/growth factor arrays | - | (hb p. 8) |
| Gaps in measurement sequence each morning | Data time series show hour(s)-long gaps in normal size distribution/hygroscopicity cycle each morning due to nightly calibration (up to 2 hours), RH-dependent hygroscopicity measurements... | - | (hb p. 12) |
| Variable total measurement sequence duration | Total time for normal measurement sequence (size distribution + hygroscopicity distributions) varies day to day because software extends scans at sizes with low particle counts | - | (hb p. 13) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | TDMA calibrated nightly at midnight by injecting polydisperse pure ammonium sulfate (per General Overview) / sodium chloride (NaCl) aerosol (per System Configuration) of known hygroscopicity generated by a TSI atomizer; CPC drained and replenished with butanol, flow meters tared, system checked for leaks via normal... (hb p. 11) |
| Calibration interval | Every night shortly after midnight (hb p. 11) |
| Traceability | Calibration data available from TAMU upon request (hb p. 11) |
| Routine maintenance | Daily: check butanol reservoir level and refill if 1/4 drained; check humidifier water level above heater and refill; check waste butanol container and empty if full; check excess water container and empty if full. Weekly: none needed if daily maintenance followed. Monthly: replace atomizer solution at least once a... (hb p. 18) |
| Maintenance interval | Daily checks; atomizer solution monthly; vacuum pump rebuild every 6-8 months; filter/pump replacement annually (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Aerosol Observing System (AOS), OPC (optical particle counter, replaced by APS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `TDMA` | tandem differential mobility analyzer |
| `APS` | aerodynamic particle sizer |
| `AOS` | aerosol observing system |
| `AS-DMA` | ambient state differential mobility analyzer |
| `CPC` | condensation particle counter |
| `DMA` | differential mobility analyzer |
| `NaCl` | sodium chloride |
| `TAMU` | Texas A&M University |
| `dN/dlogDp` | concentration (dN; cm-3) of particles in a size bin divided by the difference in log10 of... |
| `dV/dlogDp` | volume size distribution, calculated as the product of dN/dlogDp in each bin and the... |
| `RMSE` | root-mean-square error, defined as the vector sum of bias error B and random error... |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tdma_handbook.pdf (26 pages, DOE/SC-ARM-TR-090, by Don Collins)
- Catalog record: ARM data-source index, `instrument_class_code=tdma`, read 2026-09-23
- Example file: `sgptdmaapssizeC1.c1.20141117.001000.cdf` from `sgptdmaapssizeC1.c1`, 0.03 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
