---
name: arm-vap-beflux
description: ARM Best-Estimate Radiative Flux (beflux) - value-added product reference from its technical report. Derived from brs, sirs. The retrieval algorithm, reported quantities (Shortwave Direct Normal Irradiance), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpqcflux1longC1.c1) and the variable inventory of a real file. Use when working with beflux data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Radiometric. Triggers - beflux, Best-Estimate Radiative Flux, sgpqcflux1longC1.c1, brs VAP, sirs VAP, Shortwave Direct Normal Irradiance, Radiometric.
---

# BEFLUX - Best-Estimate Radiative Flux

BEFLUX is an ARM value-added product that combines and quality-controls broadband radiometer measurements from three co-located surface radiometer platforms (SIRS E13, SIRS C1, and BSRN/BRS) at the SGP Central Facility to automatically produce a best-estimate 1-minute time series of downwelling/upwelling shortwave and longwave irradiances, net surface radiation, and albedo.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 55 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `beflux` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-008 / Y. Shi, C. N. Long / October 2002](https://www.arm.gov/publications/tech_reports/arm-tr-008.pdf) |
| Category | Radiometric |
| Input instruments | `brs`, `sirs` |
| Record | 1995-05-19 to 2026-09-23 (active) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/beflux |


## Credit

Everything this skill knows about the retrieval is the work of **Y. Shi, C. N. Long** -
the ARM developers and mentors who wrote the technical report it derives from:

> Y. Shi, C. N. Long. *Best Estimate Radiation Flux Value-Added Procedure: Algorithm Operational Details and Explanations*, DOE/SC-ARM/TR-008, October 2002.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-tr-008.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP uses redundant broadband radiometer measurements of the same irradiance quantities from multiple co-located instruments to statistically determine a best estimate. For fields measured by three instruments (diffuse SW, direct normal SW, downwelling LW), the two closest-agreeing measurements are averaged if they meet an empirically derived agreement criterion; disagreement beyond that criterion triggers a look-back through the past week's data to decide which instrument to trust. For fields measured by only two instruments (upwelling SW and LW), the same logic is applied under a two-measurement case, with upwelling LW additionally cross-checked against a downward-facing infrared thermometer (IRT) converted to flux via the Stefan-Boltzmann relation (flux = σTb^4). Agreement criteria (percent or absolute Wm-2 thresholds) were derived from statistical analysis of two years (1999-2000) of instrument-pair difference distributions, chosen to encompass the "good" data population identified from frequency distributions of agreement.

**Cadence.** input rate SIRS and BSRN/BRS data: 1-minute; MFR/IRT data: 20 second; output every 1-minute resolution output; averaging Best estimate is average of the two closest-agreeing instrument measurements when criteria are met; 15-minute running standard deviation used for upwelling LW quality check (hb p. 5).

## Inputs

ARM's catalog declares these input instrument classes: `brs`, `sirs`.

The report names these instruments and sibling products: SIRS (Solar Infrared Station), BSRN (Baseline Surface Radiation Network), BRS (Broadband Radiometer Station), MFR (Multi-Filter Radiometer), IRT (Infrared Thermometer), DiffCorr1Dutt VAP, BESW (Best Estimate ShortWave VAP, predecessor).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Downwelling Shortwave Diffuse Hemispheric Irradiance | Wm-2 | - | Data difference less than 10% or 5 Wm-2,... | (hb p. 7) |
| Shortwave Direct Normal Irradiance | Wm-2 | - | Data difference less than 5% or 5 Wm-2,... | (hb p. 7) |
| Downwelling Shortwave Hemispheric Irradiance | Wm-2 | - | - | (hb p. 3) |
| Downwelling Longwave Hemispheric Irradiance | Wm-2 | - | Data difference less than 2% or 5 Wm-2,... | (hb p. 7) |
| Upwelling Shortwave Hemispheric Irradiance | Wm-2 | - | For SZA less than 80°: abs(C1/E13-1) less... | (hb p. 7) |
| Upwelling Longwave Hemispheric Irradiance | Wm-2 | - | Data difference less than 4% or IRT flux-LW... | (hb p. 7) |
| Net Surface Radiation | Wm-2 | - | - | (hb p. 3) |
| Broadband Shortwave Surface Albedo | unitless | - | - | (hb p. 4) |
| Solar Zenith Angle | degrees | - | - | (hb p. 4) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Diffuse SW criteria | Data difference less than 10% or 5 Wm-2, whichever is greater | (hb p. 36) |
| Direct Normal SW criteria | Data difference less than 5% or 5 Wm-2, whichever is greater | (hb p. 36) |
| Downwelling LW criteria | Data difference less than 2% or 5 Wm-2, whichever is greater | (hb p. 36) |
| Upwelling SW criteria | For SZA less than 80°, abs(C1/E13-1) less than 0.2; for SZA greater than =80°, data difference less than 10% or 5 Wm-2, whichever is greater | (hb p. 36) |
| Upwelling LW criteria | Data difference less than 4% or IRT flux-LW ratio standard deviation less than 0.01 | (hb p. 36) |
| 95% Level Agreement - Diffuse SW (Best/Typical/Worst) | 4.0 ± 1.4 / 9.0 ± 3.1 / 12.0 ± 3.8 Wm-2 | (hb p. 54) |
| 95% Level Agreement - Direct Normal SW (Best/Typical/Worst) | 6.3 ± 3.3 / 13.6 ± 6.3 / 15.0 ± 6.7 Wm-2 | (hb p. 54) |
| 95% Level Agreement - Downwelling LW (Best/Typical/Worst) | 3.1 ± 0.4 / 5.1 ± 1.2 / 7.1 ± 1.4 Wm-2 | (hb p. 54) |
| 95% Level Agreement - Upwelling SW | 11.1 ± 2.8 Wm-2 | (hb p. 54) |
| 95% Level Agreement - Upwelling LW | 9.6 ± 3.0 Wm-2 | (hb p. 54) |
| Ohmura et al. Global irradiance accuracy requirement (1990)... | 5 Wm-2 requirement; 15 Wm-2 in 1990; 5 Wm-2 achieved by 1995 | (hb p. 53) |
| Ohmura et al. Direct solar irradiance accuracy requirement... | 2 Wm-2 requirement; 3 Wm-2 in 1990; 2 Wm-2 achieved by 1995 | (hb p. 53) |
| Ohmura et al. Diffuse sky irradiance accuracy requirement... | 5 Wm-2 requirement; 10 Wm-2 in 1990; 5 Wm-2 achieved by 1995 | (hb p. 53) |
| Ohmura et al. Longwave down irradiance accuracy requirement... | 20 Wm-2 requirement; 30 Wm-2 in 1990; 10 Wm-2 achieved by 1995 | (hb p. 53) |


## The data

Verified example: **`sgpqcflux1longC1.c1`**, file `sgpqcflux1longC1.c1.20260920.000000.nc`
(0.18 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 28 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-20T00:00:00 to 2026-09-20T23:59:00 |
| dod version | qcflux1long-c1-1.1 |
| process version | beflux1long-1.0.13 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `albedo` | 1 | time | - | Broadband Shortwave Surface Albedo |
| `down_long_hemisp` | W/m2 | time | - | Downwelling Longwave Hemispheric Irradiance |
| `down_short_diffuse_hemisp` | W/m2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance |
| `down_short_hemisp` | W/m2 | time | - | Downwelling Shortwave Hemispheric Irradiance |
| `net_surface_radiation` | W/m2 | time | - | Net Shortwave Surface Radiation |
| `qcdifbrs` | W/m2 | time | - | Difference between Best Estimate and BRS down_short_diffuse_hemisp |
| `qcdifsirsc` | W/m2 | time | - | Difference between Best Estimate and SIRS C1 down_short_diffuse_hemisp |
| `qcdifsirse` | W/m2 | time | - | Difference between Best Estimate and SIRS E13... |
| `qcdirbrs` | W/m2 | time | - | Difference between Best Estimate and BRS short_direct_normal |
| `qcdirsirsc` | W/m2 | time | - | Difference between Best Estimate and SIRS C1 short_direct_normal |
| `qcdirsirse` | W/m2 | time | - | Difference between Best Estimate and SIRS E13 short_direct_normal |
| `qcdlfbrs` | W/m2 | time | - | Difference between Best Estimate and BRS down_long_hemisp |
| `qcdlfsirsc` | W/m2 | time | - | Difference between Best Estimate and SIRS C1 down_long_hemisp |
| `qcdlfsirse` | W/m2 | time | - | Difference between Best Estimate and SIRS E13 down_long_hemisp |
| `qcuhfsirsc` | W/m2 | time | - | Difference between Best Estimate and SIRS C1 up_short_hemisp |
| `qcuhfsirse` | W/m2 | time | - | Difference between Best Estimate and SIRS E13 up_short_hemisp |
| `qculfsirsc` | W/m2 | time | - | Difference between Best Estimate and SIRS C1 up_long_hemisp |
| `qculfsirse` | W/m2 | time | - | Difference between Best Estimate and SIRS E13 up_long_hemisp |
| `short_direct_normal` | W/m2 | time | - | Shortwave Direct Normal Irradiance |
| `time` | - | time | - | Time offset from midnight |
| `up_long_hemisp` | W/m2 | time | - | Upwelling (10 meter) Longwave Hemispheric Irradiance |
| `up_short_hemisp` | W/m2 | time | - | Upwelling (10 meter) Shortwave Hemispheric Irradiance |
| `zenith` | degree | time | - | Solar Zenith Angle |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpqcflux1longC1.c1", "2026-09-20", "2026-09-20")
ds = armlive_open("sgpqcflux1longC1.c1", "2026-09-20", "2026-09-20", cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpqcflux1longC1.c1", "19950519", "20260924")
```

The report's own note on quality: The VAP applies automatic data QC by comparing redundant co-located instrument measurements against empirically derived agreement criteria (Section 5, Table 2) and assigns a QC flag to each best-estimate value. For direct normal SW, diffuse SW, and downwelling LW (three-instrument fields): Flag=2 (Average of E13 and C1), Flag=1 (Average of BRS and C1), Flag=0 (Average of BRS and E13), Flag=-1 (BRS only), Flag=-2 (E13 only), Flag=-3 (C1 only), Flag=4 (Not enough info), Flag=-4 (All instruments down). For upwelling SW and LW (two-instrument fields): Flag=0 (Average of E13 and C1), Flag=1 (E13...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Instrument disagreement beyond criteria (no clear 'good' measurement identifiable) | Two measurements physically possible but differ beyond expected accuracy; VAP checks back through past week's data to decide which to trust, or sets value to NULL if undecidable | Look back through past week of data to determine best estimate logic path; if unresolved, set to NULL | (hb p. 8) |
| SIRS C1 diffuse SW/direct normal SW sign switch (wiring fault) | SIRS C1 B/W diffuse data switched signs from April 24 ~2000h to May 9 ~1700h in year 2000; best-estimate difference plot shows large sign-flipped differences for SIRS C1 relative to best... | VAP automatically excludes/throws out SIRS C1 data during this period based on QC criteria; confirmed via DQR-D000919.1 (crossed wires) | (hb p. 41) |
| SIRS C1 downwelling LW anomaly | From 17:30 GMT May 9, 2000 to 16:30 GMT June 30, 2000, SIRS C1 LW data read well over 500 Wm-2 while SIRS E13 and BRS read ~400 Wm-2; larger differences shown in day 138-184 period of... | Treated as outlier; best-estimate uses SIRS E13/BRS agreement instead | (hb p. 15) |
| BRS direct normal SW instrument malfunction (day 207-213, year 2000) | BRS data significantly differs from SIRS E13 and SIRS C1 data (BRS lower before day 210, higher after day 210 relative to best estimate) | Best estimate algorithm detects and excludes BRS data from the calculation during this period | (hb p. 44) |
| SIRS C1 upwelling LW malfunction (day ~126-220, year 2000; specifically May 9-Aug 3, 2000... | Standard deviation of IRT flux/upwelling LW ratio for SIRS C1 rises (only 90.7% below 0.01 in 2000 vs 98.0% in 1999); large excursions in 15-min running std dev plot; SIRS C1 vs IRT flux... | IRT flux comparison (Stefan-Boltzmann converted brightness temperature) used as additional QC criterion to detect and exclude bad SIRS C1 periods | (hb p. 25) |
| Annual ground/vegetation event affecting upwelling LW | Sudden increase in upwelling LW instrument differences around day 220 followed by gradual decrease until day 280 returning to normal, in both 1999 and 2000; also seen as decrease in... | Attributed to seasonal fall 'browning' of plants; noted as expected phenomenon, not instrument fault | (hb p. 25) |
| Upwelling SW data quality dependent on solar zenith angle | Increased distribution/scatter in C1/E13 ratio at abs(C1/E13-1)=1 appears when including all data but disappears when restricted to SZA less than 80°, indicating SZAgreater than =80° data... | Use abs(C1/E13-1) less than 0.2 as criterion only for SZA less than 80°; use percent/absolute difference criteria for SZA greater than =80° | (hb p. 18) |
| Direct normal SW percent-difference criterion sensitive to low-magnitude values | Percent differences appear large when direct normal SW magnitude is small (5% of a small value is small in absolute terms), lowering the percent of data meeting less than 5% criterion (82%... | Combine percent criterion with absolute 5 Wm-2 floor (whichever is greater) | (hb p. 12) |
| Input data availability gaps varying by platform and year | Percent of possible daytime data available varies: SIRS E13 94.5%-99.7%, SIRS C1 93.9%-99.4%, BRS/BSRN lowest at 82.7%-98.7% across 1997-2001 | VAP fills gaps using available redundant platforms per the best-estimate logic flow; missing data flagged/set to NULL when all instruments down | (hb p. 38) |
| Case with only one working instrument (no cross-check possible) | Best estimate relies on single instrument with only physical-limit checks, no comparative quality assessment possible | Continue using it if it was previously used in best estimate; otherwise flagged as 'not enough info' (Flag=4) | (hb p. 8) |
| Undecidable best-estimate cases due to insufficient historical information | QC Flag = 4 ('Not enough info') assigned when look-back logic cannot resolve which instrument(s) to trust | Flagged as Flag=4; data user should treat these periods as lower confidence | (hb p. 39) |
| All instruments down | Best estimate value set to fill value / NULL (-9999) when no instrument data available | Set to NULL | (hb p. 39) |
| Instrument transition/discontinuity in diffuse SW instrumentation | In 2001, diffuse SW instruments switched from BSRN unshaded/corrected instruments to shaded B/W (BRS) instruments, and datastream/platform naming changed from BSRN to BRS, changing input... | VAP algorithm accounts for this by using different input datastreams before/after the transition dates listed in Section 2 | (hb p. 1) |
| Diffuse SW correction dependency (Dutton IR loss correction) | Prior to BRS switch, only corrected diffuse SW (fully corrected preferred, then Dutton corrected, then original) is used as input; uncorrected data may show IR loss bias if correction... | Use fully corrected diffuse SW field if it exists; else Dutton corrected; else original uncorrected data | (hb p. 2) |
| Operational field uncertainty substantially exceeds ideal calibration accuracy | 95% agreement level for diffuse and direct normal SW is about 4-6 times larger than Ohmura et al. calibration-based accuracy figures; downwelling LW operational uncertainty is about half of... | Users should treat Table 4 'Typical'/'Worst' values as realistic long-term field uncertainty rather than ideal calibration accuracy | (hb p. 50) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `brs`: load `arm-instrument-brs` for its handbook facts and artifacts
- input instrument `sirs`: load `arm-instrument-sirs` for its handbook facts and artifacts

### References the report cites

- Long, C. N., 2002: The ARM Southern Great Plains CF Best Estimate Radiative Flux CD. ARM TR-007.
- Long, C. N., K. Younkin, and D. M. Powell, 2002: Analysis of the Dutton et al. IR Loss Correction Technique Applied to ARM Diffuse SW Measurements.
- Ohmura, A. et al., 1998: Baseline Surface Radiation Network (BSRN/WCRP): New Precision Radiometry for Climate Research. Bull. Amer. Meteo. Soc., 79, No. 10, pp. 2115-2136.
- Shi, Y., and C. N. Long, 2002: Techniques and Methods Used to Determine the Best Estimate of Radiation Fluxes at SGP Central Facility.
- Younkin, K., and C. N. Long, 2002: Results of the Dutton et al. IR Loss Correction VAP: Statistical Analysis of Corrected and Uncorrected SW Measurements.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-tr-008.pdf (55 pages, DOE/SC-ARM/TR-008, by Y. Shi, C. N. Long)
- Catalog record: ARM data-source index, `instrument_class_code=beflux`, read 2026-09-24
- Example file: `sgpqcflux1longC1.c1.20260920.000000.nc` from `sgpqcflux1longC1.c1`, 0.18 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
