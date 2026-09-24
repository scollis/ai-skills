---
name: arm-vap-rlproftemp
description: ARM Raman Lidar Temperature VAP (rlproftemp) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Temperature, RR signal ratio, Overlap function estimate), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgprlproftemp2news10mC1.c0) and the variable inventory of a real file. Use when working with rlproftemp data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Atmospheric Profiling. Triggers - rlproftemp, Raman Lidar Temperature VAP, sgprlproftemp2news10mC1.c0, Temperature, RR signal ratio, Overlap function estimate, Aerosols, Atmospheric Profiling.
---

# RLPROFTEMP - Raman Lidar Temperature VAP

This value-added product retrieves height- and time-resolved profiles of atmospheric temperature (and water vapor mixing ratio, in the companion MR VAP) from the ratio of two pure rotational Raman channels measured by ARM's ground-based, semi-autonomous Raman lidar systems deployed at SGP, ENA, and AMF3.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 39 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `rlproftemp` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-218 / R Newsom, C Sivaraman / November 2018](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf) |
| Category | Aerosols; Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2009-01-01 to 2026-09-23 (active) |
| Datastreams with data | 11 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/rlproftemp |


## Credit

Everything this skill knows about the retrieval is the work of **R Newsom, C Sivaraman** -
the ARM developers and mentors who wrote the technical report it derives from:

> R Newsom, C Sivaraman. *Raman Lidar Water Vapor Mixing Ratio and Temperature Value-Added Products*, DOE/SC-ARM-TR-218, November 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The ratio of the signals from two narrow-bandwidth pure rotational Raman (RR) detection channels, Q = P'RR1/P'RR2, depends nonlinearly on atmospheric temperature because the positions and strengths of rotational Raman lines are temperature sensitive, with the ratio well approximated by Q(z) = O(z)(a + b*exp(T'/... )) type relation involving an overlap function O(z) and height-independent calibration coefficients a and b, where T' = T(K)/300 is non-dimensional temperature. Temperature is then obtained by inverting this relation: T(z) = 300*b / (ln(Q(z)/O(z)) - a). The calibration coefficients a and b are determined via linear regression against radiosonde temperature profiles at heights above complete overlap (zgreater than =4 km, using y=ln(Q), x=300/Tsonde), and the overlap function is estimated from the residual ratio once a and b are known, then smoothed and forced to unity at large z. Differential transmission effects between the two RR channels are negligible because the wavelength difference is small, so the retrieval is comparatively insensitive to aerosol/molecular transmission uncertainties (unlike the water vapor mixing ratio retrieval).

**Cadence.** input rate 10s pulse accumulation, 7.5m range resolution (raw RL/MERGE); output every MR and TEMP are typically run with a finer temporal resolution (10 min or less); CAL computes 30-minute-averaged profiles centered on radiosonde launch times; averaging 30-minute averaging interval centered on radiosonde launch times (CAL); 5-point boxcar average applied to overlap function estimate with height (hb p. 20).

## Inputs

The report names these instruments and sibling products: Raman lidar (RL) raw instrument, Raman Lidar MERGE VAP (rlprofmerge), Raman Lidar Water Vapor Mixing Ratio VAP (MR, rlprofmr), sondewnpn (radiosonde).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Temperature | K | - | computed via error propagation from RR signal... | (hb p. 29) |
| RR signal ratio (RR1/RR2) | unitless | - | rot_raman_ratio_error reported | (hb p. 29) |
| Calibration coefficients a_coef, b_coef | unitless | - | - | (hb p. 29) |
| Overlap function estimate (olap_function) | unitless | - | - | (hb p. 29) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Laser | Continuum model 9030, frequency-Tripled Nd:YAG | (hb p. 8) |
| Transmit wavelength | 354.7 nm | (hb p. 8) |
| Pulse energy | ~300 mJ | (hb p. 8) |
| Pulse width | ~5 ns | (hb p. 8) |
| Pulse repetition frequency | 30 Hz | (hb p. 8) |
| Telescope diameter | 61 cm | (hb p. 8) |
| WFOV | 2 mrad | (hb p. 8) |
| NFOV | 0.3 mrad | (hb p. 8) |
| PMTs | Electron Tube 9954B | (hb p. 8) |
| Data acquisition | Licel transient data recorders | (hb p. 8) |
| Pulse accumulation time | 10s | (hb p. 8) |
| Range resolution | 7.5m | (hb p. 8) |
| NFOV RR1 Center Wavelength | 354.27 nm, FWHM 0.22 nm | (hb p. 8) |
| NFOV RR2 Center Wavelength | 353.27 nm, FWHM 0.21 nm | (hb p. 8) |
| WFOV & NFOV H2O Center Wavelength | 407.5 nm, FWHM 0.27 nm | (hb p. 8) |
| WFOV & NFOV N2 Center Wavelength | 386.7 nm, FWHM 0.31 nm | (hb p. 8) |


## The data

Verified example: **`sgprlproftemp2news10mC1.c0`**, file `sgprlproftemp2news10mC1.c0.20260918.000500.nc`
(0.86 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=144, `bound`=2, `height`=299 |
| Data variables | 19 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2026-09-18T00:05:00 to 2026-09-18T23:55:00 |
| dod version | rlproftemp2news10m-c0-1.0 |
| process version | vap-rlprof2_temp-1.1-3.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `a_coef` | 1 | time | - | Calibration coefficient a |
| `b_coef` | 1 | time | - | Calibration coefficient b |
| `cbh` | km | time | - | Median cloud base height |
| `height` | km | height | - | Height above ground level |
| `mr_sonde` | g/kg | time,height | - | Water vapor mixing ratio from radiosondes |
| `olap_function` | 1 | time,height | - | Overlap function |
| `pres_sonde` | mb | time,height | - | Pressure from radiosondes |
| `rot_raman_ratio` | 1 | time,height | - | Raw ratio, R1/R2 |
| `rot_raman_ratio_error` | 1 | time,height | - | Precision of the raw ratio, R1/R2 |
| `temp_sonde` | K | time,height | - | Temperature from radiosondes |
| `temperature` | K | time,height | - | Calibrated temperature from the rotational Raman channels |
| `temperature_error` | K | time,height | - | Uncertainty of calibrated temperature from the rotational Raman... |
| `time` | - | time | - | Time offset from midnight |
| `time_sonde` | 1 | time | - | Flag indicating sonde launch |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgprlproftemp2news10mC1.c0", "2026-09-18", "2026-09-18")
ds = armlive_open("sgprlproftemp2news10mC1.c0", "2026-09-18", "2026-09-18", cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgprlproftemp2news10mC1.c0", "20090101", "20260924")
```

The report's own note on quality: The MR and TEMP algorithms perform no quality control on the final output; it is the end user's responsibility to QC the data using the provided uncertainty estimates. Recommended QC is to reject samples where the relative uncertainty exceeds a threshold: temperature_error/temperature greater than  0.05 (5%) for TEMP, and mr_merged_err/mr_merged greater than  0.25 (25%) for MR. This threshold can be adjusted based on user needs. Figures 10 and 12 illustrate the effect of this filtering, showing that valid measurement height decreases during daytime for WVMR but is much less affected for...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Incomplete overlap between outgoing laser beam and receiver field of view | Overlap function departs from unity at low altitudes; NFOV reaches complete overlap only at 4km AGL (WFOV at 800m), causing biased/erratic temperature or ratio values below that height... | Overlap function O(z) is estimated from radiosonde-anchored ratio residuals, smoothed with a 5-point boxcar, and forced to 1 at large z using a... | (hb p. 10) |
| Temporal drift of overlap function and calibration coefficients due to beam alignment... | Diurnal and longer-term variability seen in plotted overlap function and a_coef/b_coef time series (Figure 8); WFOV overlap tends to be more stable than NFOV | Independent estimates of calibration coefficients and overlap function are computed for each radiosonde launch time within a 24-hour period and... | (hb p. 4) |
| Daytime solar background increasing random uncertainty | WVMR uncertainty increases significantly during daytime, with maximum valid height dropping from ~8km at night to ~4km during day (Figure 10); temperature is far less affected because RR... | None specific beyond standard QC filtering by relative uncertainty threshold; noted that RR/temperature channels are inherently less solar-sensitive... | (hb p. 10) |
| No built-in quality control performed by the algorithm on final output | Output variables (mr_merged, temperature) contain a mix of good- and poor-quality data with no QC flags pre-applied; noisy/erroneous values appear at low SNR ranges or heights without... | End user must filter data using provided uncertainty estimates; recommended relative uncertainty threshold of 5% for temperature... | (hb p. 22) |
| Aerosol transmission effects ignored in WVMR (MR) retrieval | Under hazy conditions (AOD=1) aerosol transmission ratio can decrease ~5% from surface to 7km, introducing unmodeled bias in uncalibrated WVMR profile | Effects of aerosol transmission are deliberately ignored in the MR algorithm due to difficulty of accurate aerosol extinction estimation and because... | (hb p. 10) |
| Noisy retrieved aerosol extinction from N2 channel if attempted (Ansmann-type retrieval) | Extinction profiles from N2 channel are often quite noisy and strongly affected by overlap, introducing artifacts if used for transmission correction | MR does not use retrieved aerosol extinction; effects of aerosol transmission are ignored entirely | (hb p. 10) |
| Random noise in initial overlap function estimate | Initial overlap function estimate (Eq 3.2.2.2.1) exhibits significant height-to-height variability due to measurement/shot noise, seen as scatter in Figure 7 red dots | Smoothed using a 5-point boxcar average and forced to asymptote to 1 at large z | (hb p. 18) |
| Calibration fit rejection due to poor linear regression quality | Some radiosonde-based calibration attempts fail QC criteria (RMSgreater than =0.1 or correlationless than =0.7), visible as light gray (excluded) points in calibration regression plot... | Calibration coefficients from a given radiosonde are deemed invalid and excluded if RMSgreater than =0.1 or correlationless than =0.7; only valid... | (hb p. 17) |
| Requirement that CAL VAP run ahead of MR/TEMP | If CAL has not been run for the relevant dates, MR and TEMP cannot calibrate; missing calibration data would show as unresolved or default calibration in output | CAL must run at least a couple of days ahead of MR and TEMP; CAL can run days, weeks, or months ahead since it is independent | (hb p. 7) |
| Missing baseline calibration profile in configuration file for MR | MR will not run for a given date if the configuration file lacks a corresponding baseline calibration profile | Baseline calibration profiles must be periodically generated via offline analysis (over 2-6 month periods) and hand-drawn through median... | (hb p. 21) |
| No WFOV rotational Raman channel exists | TEMP output contains only NFOV-derived temperature; no WFOV/NFOV merging step is present (unlike MR), so temperature data availability is limited to the NFOV overlap-corrected range | Not applicable / no merging needed, noted explicitly in handbook | (hb p. 23) |
| Uncertainty estimate excludes calibration profile and transmission term uncertainties... | Reported uncertainty may underestimate true total uncertainty since systematic calibration-profile or transmission uncertainties are not propagated | None stated beyond acknowledging exclusion | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Behrendt A, and J Reichardt. 2000. Applied Optics 39(9): 1372-1378
- Bucholtz A. 1995. Applied Optics 34(15): 2765-2773
- Goldsmith JEM, FH Blair, SE Bisson, and DD Turner. 1998. Applied Optics 37(21): 4979-4990
- Newsom RK, J Goldsmith, and C Sivaraman. 2017. Raman Lidar MERGE Value-Added Product. DOE/SC-ARM-TR-189
- Newsom, RK, DD Turner, and JEM Goldsmith. 2013. Journal of Atmospheric and Oceanic Technology 30(8): 1616-1634
- Turner DD, RA Ferrare, LA Heilman Brasseur, WF Feltz, and TP Tooman. 2002. Journal of Atmospheric and Oceanic Technology 19(1): 37-49
- Turner, DD, JEM Goldsmith, and RA Ferrare. 2016. Development and applications of the ARM Raman lidar.
- Whiteman, DN, SH Melfi, and RA Ferrare. 1992. Applied Optics 31(16): 3068-3082
- Weitkamp, Claus. 2005. Lidar, Range-Resolved Optical Remote Sensing of the Atmosphere.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf (39 pages, DOE/SC-ARM-TR-218, by R Newsom, C Sivaraman)
- Catalog record: ARM data-source index, `instrument_class_code=rlproftemp`, read 2026-09-24
- Example file: `sgprlproftemp2news10mC1.c0.20260918.000500.nc` from `sgprlproftemp2news10mC1.c0`, 0.86 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
