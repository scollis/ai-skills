---
name: arm-vap-aop
description: ARM Aerosol Optical Properties (aop) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Angstrom exponent for scattering), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaoppsap1flynn1mC1.c1) and the variable inventory of a real file. Use when working with aop data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - aop, Aerosol Optical Properties, sgpaoppsap1flynn1mC1.c1, Aerosols.
---

# AOP - Aerosol Optical Properties

The AOP VAP applies published corrections (Bond/Ogren and Virkkula) to filter-based PSAP/CLAP aerosol absorption measurements combined with nephelometer scattering measurements to derive corrected aerosol absorption/scattering coefficients and intensive optical properties (SSA, angstrom exponents, backscatter fraction, asymmetry parameter) at ARM AOS sites worldwide.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 21 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aop` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-211 / C Flynn, D Chand, B Ermold, A Koontz / August 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-211.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-01-21 to 2026-09-24 (active) |
| Datastreams with data | 58 across 17 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aop |


## Credit

Everything this skill knows about the retrieval is the work of **C Flynn, D Chand, B Ermold, A Koontz** -
the ARM developers and mentors who wrote the technical report it derives from:

> C Flynn, D Chand, B Ermold, A Koontz. *The ARM Aerosol Optical Properties (AOP) Value-Added Product*, DOE/SC-ARM-TR-211, August 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-211.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The AOP VAP computes raw "uncorrected" absorption coefficients from Beer's Law using the filter spot area, aerosol sample flow rate, and light intensity transmitted through a particulate filter (PSAP or CLAP) over a sampling interval. Two independent published corrections are applied to these raw absorption coefficients to account for filter-loading (shadowing) amplification and light-scattering artifacts inherent to the filter-based technique: the Bond1999/Ogren2010 correction (using scattering coefficients corrected to STP but without truncation correction) and the Virkkula2010 iterative correction (using fully truncation-corrected scattering coefficients and retrieving single-scattering albedo iteratively). A combined absorption product is computed as the arithmetic mean of the Bond-Ogren and Virkkula corrected values. The combined absorption coefficients, together with scattering properties spectrally adjusted to match the absorption measurement wavelengths via angstrom-exponent relationships, are used to derive intensive aerosol optical properties: single-scattering albedo, absorption/scattering angstrom exponents, hemispheric backscatter fraction, and asymmetry parameter (the latter parameterized from backscatter fraction per Andrews et al. 2006). All quantities are computed as 1-minute averages, and a follow-on process (aoppsapavg, aopclapavg) generates hourly averages segregated by impactor state (1 micron vs 10 micron cutoff) with more stringent quality checks.

**Cadence.** input rate PSAP raw hexadecimal data packets; 60-second sliding window smoothing applied per Springston and Sedlacek 2007; output every 1-minute (60-second) averages in aoppsap1flynn1m.c1/aopclap1flynn1m.c1; hourly averages in follow-on aoppsapavg/aopclapavg (1flynn1h) files; averaging 1-minute averages computed over 60 seconds from start of minute (inclusive) to start of next (exclusive); hourly averages segregate 1-minute values by impactor state (1um vs 10um) excluding those flagged bad (hb p. 3).

## Inputs

The report names these instruments and sibling products: PSAP (particle soot absorption photometer), CLAP (continuous light absorption photometer), TAP (tricolor absorption photometer), Nephelometer (aosnephdry), AOS (Aerosol Observing System), AIP1OGREN (Aerosol Observing Station Intensive Properties VAP), CAPS (cavity-attenuated phase shift extinction monitor).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Uncorrected aerosol light absorption coefficient (Ba_B_raw,... | - | - | - | (hb p. 9) |
| Aerosol light absorption coefficient, Weiss-corrected... | - | - | - | (hb p. 9) |
| Transmittance, blue/green/red channel | - | - | - | (hb p. 9) |
| Aerosol total light-scattering coefficient (Bs_B, Bs_G,... | - | - | - | (hb p. 9) |
| Aerosol back-hemispheric light-scattering coefficient... | - | - | - | (hb p. 10) |
| Angstrom exponent for scattering (AE_BG, AE_BR, AE_GR) and... | - | - | - | (hb p. 10) |
| Backscattering fraction (bsf_B, bsf_G, bsf_R) | - | - | - | (hb p. 10) |
| Asymmetry parameter (g_B, g_G, g_R) | - | - | - | (hb p. 10) |
| Pressure inside reference nephelometer (P_Neph_Dry) | - | - | - | (hb p. 10) |
| Temperature inside reference nephelometer (T_Neph_Dry) | - | - | - | (hb p. 10) |
| Absorption coefficient, Virkkula-corrected (Ba_R_Virkkula,... | - | - | - | (hb p. 11) |
| Single-scattering albedo, Virkkula (ssa_R_Virkkula,... | - | SSAgreater than 0.98 flagged as... | - | (hb p. 11) |
| Absorption coefficient, Bond-Ogren corrected... | - | - | - | (hb p. 11) |
| Combined absorption coefficient (Ba_B_combined,... | - | - | - | (hb p. 11) |
| Absorption angstrom exponent (AAE_BG, AAE_BR, AAE_GR) | - | - | - | (hb p. 11) |
| impactor_state (PM1/PM10 mode indicator) | - | 1 um or 10 um | - | (hb p. 11) |
| Submicron scattering fraction / supermicron Bs (hourly) | - | - | - | (hb p. 12) |
| Submicron absorption fraction / supermicron Ba, SSA, AAE... | - | - | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Absorption measurement bands (nominal RGB) | ~650 nm (red), 530 nm (green), 465 nm (blue); exact wavelengths reported per-instrument in 'wavelength' attribute | (hb p. 9) |
| Scattering measurement wavelengths (nephelometer) | 450 nm (blue), 550 nm (green), 700 nm (red) | (hb p. 9) |
| 1-minute averaging window | 60 seconds from start of one minute (inclusive) to start of next (exclusive) | (hb p. 3) |
| PSAP transmittance smoothing window | 60-second sliding window applied to full-precision transmittances and calibrated flow rate | (hb p. 9) |
| PSAP green wavelength used in Bond correction | 574 nm (converted to nephelometer green 550 nm) | (hb p. 6) |
| K1 proportionality constant for PM1 (impactor_state==1) | 0.02 (2% of uncorrected scattering coefficient), per Bond 1999 | (hb p. 6) |
| K1_B for PM10 (impactor_state==10), blue | K1_B = 0.00668 for AE_Bs_BG_uncorrected less than  0.2; K1_B = 0.02 for AE_Bs_BG_raw greater than  0.6; K1_B = 0.0334 * AE_Bs_BG_uncorrected otherwise | (hb p. 6) |
| EMFAB filter scale factor | non-scattering component of Bond-Ogren and Virkkula corrections multiplied by factor of 1.3 when PSAP uses EMFAB filter | (hb p. 2) |
| Weiss filter-loading correction factor f_w | f_w = 1/1.22 * ((0.97*0.873)/(1.0796 Tr + 0.71)) = 1 / (1.5557Tr + 1.0227) | (hb p. 6) |
| Asymmetry parameter parameterization | g = 0.9893 - 3.9636 bsf + 7.4644 bsf^2 - 7.1439 bsf^3 | (hb p. 3) |
| STP reference conditions | 0 degC, 1013.25 hPa | (hb p. 3) |
| SSA display threshold | SSAgreater than 0.98 not shown in plots due to large uncertainty | (hb p. 12) |


## The data

Verified example: **`sgpaoppsap1flynn1mC1.c1`**, file `sgpaoppsap1flynn1mC1.c1.20170926.000030.nc`
(0.89 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 132 |
| QC variables | 58 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2017-09-26T00:00:30 to 2017-09-26T23:59:30 |
| dod version | aoppsap1flynn1m-c1-1.2 |
| process version | vap-aosaop-1.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `AAE_BG` | unitless | time | yes | Angstrom exponent computed from blue and green combined absorption... |
| `AAE_BR` | unitless | time | yes | Angstrom exponent computed from blue and red combined absorption... |
| `AAE_GR` | unitless | time | yes | Angstrom exponent computed from green and red combined absorption... |
| `AE_BG` | unitless | time | yes | Angstrom exponent computed from blue/green total scattering with... |
| `AE_BR` | unitless | time | yes | Angstrom exponent computed from blue/red total scattering with... |
| `AE_Bbs_BG` | unitless | time | yes | Angstrom exponent computed from blue/green hemispheric back... |
| `AE_Bbs_BR` | unitless | time | yes | Angstrom exponent computed from blue/red hemispheric back scattering... |
| `AE_Bbs_GR` | unitless | time | yes | Angstrom exponent computed from green/red hemispheric back scattering... |
| `AE_GR` | unitless | time | yes | Angstrom exponent computed from green/red total scattering with... |
| `Ba_B_BondOgren` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel, corrected... |
| `Ba_B_Virkkula` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel, using... |
| `Ba_B_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel, corrected... |
| `Ba_B_combined` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue channel |
| `Ba_B_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, blue channel at dry... |
| `Ba_G_BondOgren` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel,... |
| `Ba_G_Virkkula` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel, sing... |
| `Ba_G_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel,... |
| `Ba_G_combined` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green channel |
| `Ba_G_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, green channel at... |
| `Ba_R_BondOgren` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel, corrected... |
| `Ba_R_Virkkula` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel, using... |
| `Ba_R_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel, corrected... |
| `Ba_R_combined` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red channel |
| `Ba_R_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, red channel at dry... |
| `Bbs_B` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, truncation... |
| `Bbs_B_Dry_Neph3W` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal blue... |
| `Bbs_G` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, truncation... |
| `Bbs_G_Dry_Neph3W` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal green... |
| `Bbs_R` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, truncation... |
| `Bbs_R_Dry_Neph3W` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal red... |


_39 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaoppsap1flynn1mC1.c1", "2017-09-26", "2017-09-26")
ds = armlive_open("sgpaoppsap1flynn1mC1.c1", "2017-09-26", "2017-09-26", cleanup_qc=True)
```

This product carries 132 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaoppsap1flynn1mC1.c1", start, end,
                  keep_variables=['AAE_BG', 'AAE_BR', 'AAE_GR', 'qc_AAE_BG', 'qc_AAE_BR', 'qc_AAE_GR'])
```

## Quality control in this product

58 `qc_` companion variables cover 58 of the
132 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpaoppsap1flynn1mC1.c1.20170926.000030.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `AE_Bbs_GR` | One or more source fields were flagged "Bad" | 941 | 65.3472 |
| `Bbs_R` | One or more source fields were flagged "Bad" | 941 | 65.3472 |
| `AE_Bbs_BR` | One or more source fields were flagged "Bad" | 941 | 65.3472 |
| `bsf_R` | One or more source fields were flagged "Bad" | 941 | 65.3472 |
| `g_R` | One or more source fields were flagged "Bad" | 941 | 65.3472 |
| `g_B` | One or more source fields were flagged "Bad" | 532 | 36.9444 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaoppsap1flynn1mC1.c1", "20110121", "20260924")
```

The report's own note on quality: The AOP datastream applies automated quality checks (QC) for each primary field and many auxiliary fields, captured in bit-mapped/bit-packed integer "qc" fields named after the field of interest. Each bit represents a true/false quality test; ARM convention is that a "true"/1 value represents a failure condition, so a qc value of 0 means "good" data. Quality tests can characterize data as "bad" or "indeterminate" (suspect); test definitions and assessments are stored as NetCDF metadata attributes "bit_N_description" and "bit_N_assessment" under each qc field. Example:...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Filter-based absorption measurement artifacts (amplification/shadowing/filter-loading... | Raw absorption coefficients from PSAP/CLAP show artifacts comparable in magnitude or even larger than the actual absorption signal | Apply published corrections (Weiss filter-loading correction, Bond/Ogren correction, Virkkula correction) to raw absorption coefficients | (hb p. 1) |
| Two independent, non-reconciled absorption correction schemes (Bond/Ogren vs Virkkula)... | Ba_{RGB}_BondOgren and Ba_{RGB}_Virkkula differ for the same raw measurement | No explicit preference is given; VAP reports arithmetic mean as Ba_{RGB}_combined for use in derived products | (hb p. 6) |
| PSAP filter medium change (PallFlex E70 to Pall EMFAB) alters correction scale factor | Step change/discontinuity in corrected absorption coefficients coincident with filter medium change | Non-scattering component of corrections multiplied by factor of 1.3 for EMFAB filter | (hb p. 1) |
| Bond correction wavelength conversion artifact (implicit conversion from PSAP green 574... | Wavelength-dependent bias in Ba_BondOgren unless Ogren-adjusted correction applied | Ogren 2010 removes the implicit wavelength conversion using an assumed angstrom exponent for the nigrosin suspension used in Bond 1999 | (hb p. 6) |
| Virkkula 5-parameter correction has only 4 linearly independent parameters | Redundant/non-unique parameter fit if all 5 parameters treated as independent | Retained as-published 5-parameter form for consistency with literature | (hb p. 6) |
| Bond/Ogren correction uses non-truncation-corrected scattering while Virkkula uses... | Systematic offset between Ba_BondOgren and Ba_Virkkula traceable to different scattering inputs | None specified beyond noting the difference; combined product averages both | (hb p. 6) |
| Low aerosol loading / low signal-to-noise for extensive properties | Larger scatter/uncertainty in intensive properties (SSA, AAE, SAE, BSF, g) near instrument detection limit | Such conditions are flagged; user advised to treat data with caution | (hb p. 12) |
| Filter-based SSA measurement scattering artifacts from particle deposits on filter surface | Anomalously high or noisy SSA values, especially SSAgreater than 0.98 | Data with SSAgreater than 0.98 not shown in plots (Figure 3 middle panel) due to large uncertainty | (hb p. 12) |
| Very low absorption coefficient and/or high scattering coefficient increases uncertainty... | Increased scatter/noise in Ba_combined and ssa fields under low-absorption/high-scattering conditions | None specified beyond caution advisory | (hb p. 12) |
| Asymmetry parameter is a parameterization (fit), not a strict derivation | Systematic errors possible in g fields relative to true asymmetry parameter | None specified | (hb p. 12) |
| Data gaps / limited processing periods per site | AOP datastreams only available for specific date ranges per site (e.g., ASI M1 May 2016-Oct 2017, ENA C1 Oct 2013-Jan 2018); MAO S1 and MAO M1 not processed yet | Expected reprocessing efforts planned starting with GoAmazon2014/15 MAO facilities | (hb p. 12) |
| CAPS-based version and constrained two-stream correction approach still under evaluation,... | Not yet reflected in current data product; results using nephelometer-based scattering may differ from a future CAPS-based version | Under evaluation for possible future addition | (hb p. 13) |
| TAP instrument not yet supported | aostap1m.b1 input datastream mentioned as planned ('and soon TAP') but not yet processed | Anticipate extending AOP to process TAP data | (hb p. 12) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Anderson, TL, and JA Ogren. 1998. Determining aerosol radiative properties using the TSI-3563 integrating nephelometer. Aerosol Science and Technology 29(1): 57-69
- Andrews, E, et al. 2006. Comparison of methods for deriving aerosol asymmetry parameter. JGR Atmospheres 111(D5): D05S04
- Bond, TC, TL Anderson, and D Campbell. 1999. Calibration and inter-comparison of filter-based measurements of visible light absorption by aerosols. Aerosol Science and Technology 30(6): 582-600
- Collins, AM, WD Dick, and FJ Romay. 2013. A new coincidence correction method for condensation particle counters. Aerosol Science and Technology 47(2): 177-182
- Jaenicke, R. 1972. The optical particle counter: Cross-sensitivity and coincidence. Journal of Aerosol Science 3(2): 95-111
- Jefferson, A. 2011. Aerosol Observing System (AOS) Handbook. DOE/SC-ARM-TR-014
- Koontz, A, and C Flynn. 2017. AIP1OGREN: Aerosol Observing Station Intensive Properties Value-Added Product. DOE/SC-ARM-TR-201
- McMurry, PH. 2000. A review of atmospheric aerosol measurements. Atmospheric Environment 34(12-14): 1959-1999
- Ogren, JA. 2010. Comment on Calibration and intercomparison of filter-based measurements of visible light absorption by aerosols. Aerosol Science and Technology 44(8): 589-591
- Springston, SR, and AJ Sedlacek. 2007. Noise characteristics of an instrumental particle absorbance technique. Aerosol Science and Technology 41(12): 1110-1116

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-211.pdf (21 pages, DOE/SC-ARM-TR-211, by C Flynn, D Chand, B Ermold, A Koontz)
- Catalog record: ARM data-source index, `instrument_class_code=aop`, read 2026-09-24
- Example file: `sgpaoppsap1flynn1mC1.c1.20170926.000030.nc` from `sgpaoppsap1flynn1mC1.c1`, 0.89 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
