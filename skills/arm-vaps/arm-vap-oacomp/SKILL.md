---
name: arm-vap-oacomp
description: ARM Organic Aerosol Component (oacomp) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (time_series_MOOOA, time_series_LOOOA, time_series_BBOA, mass_spectrum_MOOOA, mass_spectrum_LOOOA, mass_spectrum_BBOA), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpoacomp1zhangC1.c1) and the variable inventory of a real file. Use when working with oacomp data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - oacomp, Organic Aerosol Component, sgpoacomp1zhangC1.c1, time_series_MOOOA, time_series_LOOOA, time_series_BBOA, mass_spectrum_MOOOA, mass_spectrum_LOOOA, Aerosols.
---

# OACOMP - Organic Aerosol Component

OACOMP is an ARM value-added product that derives quantitative organic aerosol source/process components (LOOOA, MOOOA, BBOA) from ACSM aerosol chemical speciation monitor mass spectral data collected at fixed ARM sites such as SGP.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 18 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `oacomp` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-131 / J Fast, T Shippert, Q Zhang, C Parworth, A Tilp, F Mei / August 2013](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-131.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-01-08 to 2012-03-24 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/oacomp |


## Credit

Everything this skill knows about the retrieval is the work of **J Fast, T Shippert, Q Zhang, C Parworth, A Tilp, F Mei** -
the ARM developers and mentors who wrote the technical report it derives from:

> J Fast, T Shippert, Q Zhang, C Parworth, A Tilp, F Mei. *Organic Aerosol Component (OACOMP): An ARM Value-Added Product*, DOE/SC-ARM-TR-131, August 2013.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-131.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

OACOMP is primarily based on multivariate analysis (positive matrix factorization, PMF) of the measured organic mass spectral matrix reported by the ACSM. The ACSM measures mass concentrations and chemical composition of non-refractory submicron aerosol particles by vaporizing particles and ionizing them for mass spectral analysis, similar to but a low-maintenance 'mini' version of the aerosol mass spectrometer (AMS). PMF is run for 2- and 3-factor solutions over a fifteen-day rolling window centered on each analysis day, producing a mass spectrum matrix F for each factor and a time series matrix G for each factor, normalized such that X ~ GF. Factors are identified with physical processes (biomass burning via AMU 60 fraction, MOOA vs LOOA via AMU 44 fraction) and averaged across the 15 overlapping PMF runs to produce final component time series and mass spectra summing to ~100% of total OA mass.

**Cadence.** input rate ACSM sampling interval generally 30 minutes (vs 2-5 min for fixed-site AMS, 30 sec or less for mobile AMS); output every ~30-min increments (OACOMP output at same time intervals as original ACSM data); averaging PMF run on a fifteen-day rolling window centered on each day of analysis; 15 overlapping PMF runs averaged per day (hb p. 7).

## Inputs

The report names these instruments and sibling products: ACSM (aerosol chemical speciation monitor), AMS (aerosol mass spectrometer), HR-AMS (high-resolution aerosol mass spectrometer), MAOS (Mobile Aerosol Observing System).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| time_series_MOOOA (more-oxidized oxygenated organic aerosol) | - | - | - | (hb p. 7) |
| time_series_LOOOA (less-oxidized oxygenated organic aerosol) | - | - | - | (hb p. 7) |
| time_series_BBOA (biomass burning organic aerosol) | - | - | - | (hb p. 7) |
| mass_spectrum_MOOOA | - | - | - | (hb p. 7) |
| mass_spectrum_LOOOA | - | - | - | (hb p. 7) |
| mass_spectrum_BBOA | - | - | - | (hb p. 8) |
| total_organics | µg m-3 | - | - | (hb p. 8) |
| ammonium | µg m-3 | - | - | (hb p. 8) |
| sulfate | µg m-3 | - | - | (hb p. 8) |
| nitrate | µg m-3 | - | - | (hb p. 8) |
| chloride | µg m-3 | - | - | (hb p. 8) |
| organic matter (OM) detection limit (ACSM, input data) | g m-3 | - | 0.3 | (hb p. 7) |
| sulfate (SO4) detection limit (ACSM, input data) | g m-3 | - | 0.4 | (hb p. 7) |
| nitrate (NO3) detection limit (ACSM, input data) | g m-3 | - | 0.2 | (hb p. 7) |
| ammonium (NH4) detection limit (ACSM, input data) | g m-3 | - | 0.5 | (hb p. 7) |
| chloride (Cl) detection limit (ACSM, input data) | g m-3 | - | 0.2 | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| valid_min threshold (output) | 0.0 for all output fields | (hb p. 5) |
| valid_max threshold (output) | 300.0 | (hb p. 6) |
| PMF factors computed | 2 and 3 factors, fpeak = 0.0 | (hb p. 5) |
| PMF rolling window | fifteen-day rolling window centered on each day of analysis (15 PMFs per day) | (hb p. 5) |
| Biomass burning identification threshold | AMU 60 to sum-of-all-AMUs mass spec ratio greater than  0.008 | (hb p. 5) |
| Spike removal threshold (preprocessing) | X_t,a / (X_t-1,a + X_t+1,a) greater than  3 | (hb p. 4) |
| Bad m/z down-weighting criterion | R_mean_a less than  0.2 or R_median_a less than  0.0 =greater than  X_t,a = X_t,a/20, E_t,a = mean_t,a(E_t,a) | (hb p. 3) |


## The data

Verified example: **`sgpoacomp1zhangC1.c1`**, file `sgpoacomp1zhangC1.c1.20120321.002128.cdf`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=44, `amus`=121 |
| Data variables | 28 |
| QC variables | 6 (`qc_` companions) |
| Median time step | 1910 s |
| File time span | 2012-03-21T00:21:28 to 2012-03-21T23:32:16 |
| dod version | oacomp1zhang-c1-0.9 |
| process version | $ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `mass_spectrum_BBOA` | unitless | amus | yes | mass spectra for biomass organic aerosol component, unnormalized |
| `mass_spectrum_LOOOA` | unitless | amus | yes | mass spectra for less oxidized oxygenated organic aerosol component |
| `mass_spectrum_MOOOA` | unitless | amus | yes | mass spectra for more oxidized oxygenated organic aerosol component |
| `time_series_BBOA` | ug/m3 | time | yes | time series for biomass burning organic aerosol component |
| `time_series_LOOOA` | ug/m3 | time | yes | time series for less oxidized oxygenated organic aerosol component |
| `time_series_MOOOA` | ug/m3 | time | yes | time series for more oxidized oxygenated organic aerosol component |
| `ammonium` | ug/m3 | time | - | Mass concentration of ammonium, ambient aerosol in air |
| `amus` | amus | amus | - | Mass to charge ratios of ion fragments |
| `chloride` | ug/m3 | time | - | Mass concentration of chloride, ambient aerosol in air |
| `mass_spectrum_BBOA_std` | unitless | amus | - | standard deviation of mass spectra for biomass organic aerosol... |
| `mass_spectrum_LOOOA_std` | unitless | amus | - | standard deviation of mass spectra for less oxidized oxygenated... |
| `mass_spectrum_MOOOA_std` | unitless | amus | - | standard deviation of mass spectra for more oxidized oxygenated... |
| `nitrate` | ug/m3 | time | - | Mass concentration of nitrate, ambient aerosol in air |
| `sulfate` | ug/m3 | time | - | Mass concentration of sulfate, ambient aerosol in air |
| `time` | - | time | - | Time offset from midnight |
| `time_series_BBOA_std` | ug/m3 | time | - | standard deviation of time series for biomass burning organic aerosol... |
| `time_series_LOOOA_std` | ug/m3 | time | - | standard deviation of time series for less oxidized oxygenated... |
| `time_series_MOOOA_std` | ug/m3 | time | - | standard deviation of time series for more oxidized oxygenated... |
| `total_organics` | ug/m3 | time | - | Mass concentration of total organics, ambient aerosol in air |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpoacomp1zhangC1.c1", "2012-03-21", "2012-03-21")
ds = armlive_open("sgpoacomp1zhangC1.c1", "2012-03-21", "2012-03-21", cleanup_qc=True)
```

## Quality control in this product

6 `qc_` companion variables cover 6 of the
28 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpoacomp1zhangC1.c1.20120321.002128.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `time_series_MOOOA` | Three or fewer days used in fifteen day rolling PMF window | 44 | 100.0 |
| `time_series_LOOOA` | At least one PMF in rolling window had at least one factor with... | 44 | 100.0 |
| `mass_spectrum_BBOA` | At least one PMF in rolling window had at least one factor with... | 121 | 100.0 |
| `time_series_BBOA` | No biomass burning factor for this window; BBOA fields set to... | 44 | 100.0 |
| `time_series_BBOA` | At least one PMF in rolling window had at least one factor with... | 44 | 100.0 |
| `mass_spectrum_LOOOA` | At least one PMF in rolling window had at least one factor with... | 121 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpoacomp1zhangC1.c1", "20110108", "20260924")
```

The report's own note on quality: Flags are assigned to each data point to indicate data quality. 'Bad' flags: Bit1 OACOMP could not be performed (missing data), Bit2 value below valid_min (0.0), Bit3 value above valid_max (300.0), Bit4 three or fewer valid PMF runs used. 'Indeterminate' flags (data probably usable but caveated): Bit5 fewer than 15 valid PMF runs used, Bit6 a PMF had a factor with AMU44 mass_spec fraction greater than 0.3 (unphysical), Bit7 a PMF had AMU43/AMU44 ratio less than 0.01 or greater than 10, Bit8 ratio of summed time-series factors to total_organics greater than 1.4 or less than 0.7 (when...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Noisy input ACSM data | Spikes and noisy samples in org_mx and org_mx_err matrices before preprocessing | Preprocessing steps remove spikes, down-weight noisy samples, and fix other problem areas before running PMF analysis | (hb p. 4) |
| Zero values in input error matrix | Zeros detected in org_mx_err error matrix | Zeros are replaced with the maximum error value in that matrix | (hb p. 4) |
| Large spikes in mass spectral time series | X_t,a / (X_t-1,a + X_t+1,a) greater than  3 in org_mx or org_mx_err matrices | Replace X_t,a with an average of the two bracketing points; same process applied to org_mx_err | (hb p. 4) |
| Low vaporizer temperature instrument malfunction | Very low (less than 550 C) vaporizer temperatures in diagnostics plots | Instrument mentor marks and removes affected data points | (hb p. 2) |
| Bad m/z (weak/unreliable variable) | Mean error ratio R_mean_a less than  0.2 or median error ratio R_median_a less than  0.0 for a given m/z | Set X_t,a = X_t,a/20 and E_t,a = mean_t,a(E_t,a), forcing PMF to put little signal in that species (effectively removing it) | (hb p. 3) |
| m/z 44-related interferences (m/z 44, 16, 17) | Elevated signal at m/z 44, 16, 17 potentially confounding PMF factor separation | Down-weight m/z 44 related m/z's as part of PMF exporting tools procedure | (hb p. 2) |
| PMF factor swapping/ambiguity across rolling window runs | Factor 1 may be MOOOA in one 15-day PMF run and LOOOA in the next run | Identify each factor with its physical process each run: biomass burning via AMU60 ratio greater than 0.008, then correlate non-biomass factor time... | (hb p. 5) |
| Insufficient valid PMF runs / data gaps (Bit 4, Bit 1) | Bit 1: OACOMP unable to be performed, data filled with missing; Bit 4: three or fewer valid PMF runs used for the day | Flagged as 'bad'; usually indicates gap in ACSM data | (hb p. 5) |
| Output values outside loose valid_min/valid_max bounds | Bit 2: output value below valid_min (0.0); Bit 3: output value above valid_max (300.0) | Flagged as 'bad'; intended mainly to catch processing bugs rather than identify reasonable scientific values (no data failed these tests in test runs) | (hb p. 5) |
| Fewer than full 15 valid PMF runs in final averaging (Bit 5) | Fewer than 15 valid PMF runs used in final averaging | Flagged as 'indeterminate'; data can probably still be used but user should be aware | (hb p. 6) |
| Unphysical PMF mass spectrum at AMU 44 (Bit 6) | At least one PMF in the 15-day rolling window has a factor with AMU 44 mass_spec fraction greater than  0.3, which does not make physical sense | Any PMF with this condition is excluded from the final average (co-occurs with Bit 5) | (hb p. 6) |
| Anomalous AMU 43/44 ratio in PMF output (Bit 7) | Ratio of AMU 43 to AMU 44 less than  0.01 or greater than  10 in at least one PMF in the rolling window | Such PMF excluded from final average; handbook notes this had not occurred in initial test runs and limits may need tightening | (hb p. 6) |
| Mismatch between summed OA factors and total_organics field (Bit 8) | /ts_factor_sum/total_organics/ greater than  1.4 or less than  0.7 while total_organics greater than  1.0 µg m-3 | Flagged; indicates discrepancy between PMF-derived component sum and measured total organics | (hb p. 6) |
| Low total organics precludes reliable factor-sum comparison (Bit 9) | total_organics less than  1.0 µg m-3, causing the comparison ratio to blow up | Bit set instead of Bit 8 to indicate comparison could not be made | (hb p. 6) |
| No biomass burning detected for a given day | BBOA fields all set to 0.0 by definition; Bit 10 set | Not an error; bit included simply to flag when this occurs | (hb p. 6) |
| Primary organic aerosol (POA) undetectable at SGP | Primary OAs are very small and cannot be detected by the ACSM at SGP | Attributed to SGP's distance from large primary anthropogenic emission sources; no specific mitigation given | (hb p. 8) |
| Semi-automated XDC-to-DMF data transfer process | Manual/semi-automated packaging and shipping of QCed data introduces potential for delay or human error in B1 product generation | Process is nearly ready to be fully automated (future plan) | (hb p. 3) |
| Non-fully-automated initial QA (Step 1) | Manual instrument mentor review of diagnostics plots and calibration inputs required monthly | Instrument mentor investigating automation, dependent on ACSM manufacturer software updates | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Canagaratna et al. 2007, Mass Spectrometry Reviews 26: 185-222
- DeCarlo et al. 2006, Analytical Chemistry 78: 8281-8289
- Jimenez et al. 2009, Science 326: 1525-1529
- Ng et al. 2011a, Environmental Science and Technology 45(3): 910-916
- Ng et al. 2011b, Aerosol Science and Technology 45(7): 770-784
- Paatero and Tapper 1994, Environmetrics 5: 111-126
- Sun et al. 2011, Atmospheric Chemistry and Physics 11: 1581-1602
- Ulbrich et al. 2009, Atmospheric Chemical Physics 9: 2891-2918
- Zhang et al. 2005, Environmental Science & Technology 39(13): 4938-4952
- Zhang et al. 2011, Analytical and Bioanalytical Chemistry 401(10): 3045-3067

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-131.pdf (18 pages, DOE/SC-ARM-TR-131, by J Fast, T Shippert, Q Zhang, C Parworth, A Tilp, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=oacomp`, read 2026-09-24
- Example file: `sgpoacomp1zhangC1.c1.20120321.002128.cdf` from `sgpoacomp1zhangC1.c1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
