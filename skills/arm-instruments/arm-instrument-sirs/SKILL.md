---
name: arm-instrument-sirs
description: ARM Solar and Infrared Radiation Station for Downwelling and Upwelling Radiation (sirs) - handbook-derived instrument reference. Measurement principle, reported quantities (Direct normal, Diffuse horizontal, Total hemispheric, Total hemispheric, Reflected solar, Upwelling longwave), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpsirsC1.b1) and the variable inventory of a real file. Use when working with sirs data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - sirs, sgpsirsC1.b1, Direct normal, Diffuse horizontal, Total hemispheric, Reflected solar, Upwelling longwave, Radiometric, The Eppley Laboratory, Inc. - NIP (pyrheliometer), SIRS, SKYRAD, GNDRAD, BORCAL.
---

# SIRS - Solar and Infrared Radiation Station for Downwelling and Upwelling Radiation

The SIRS provides continuous 1-minute measurements of broadband shortwave (solar) and longwave (atmospheric/infrared) irradiances for downwelling and upwelling components using a network of commercially available thermopile-based radiometers (pyrheliometer, pyranometers, and pyrgeometers) deployed on solar trackers and stands at ARM fixed and mobile facility sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 58 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sirs` |
| Handbook | [DOE/SC-ARM-TR-025 / A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta / April 2018](https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | The Eppley Laboratory, Inc. - NIP (pyrheliometer), PSP (Precision Spectral Pyranometer), Model 8-48 (Black & White pyranometer), PIR (Precision Infrared Radiometer, pyrgeometer); Kipp & Zonen Model... |
| Primary measurements | Longwave broadband downwelling irradiance; Longwave broadband upwelling irradiance; Shortwave broadband diffuse downwelling irradiance; Shortwave broadband direct normal irradiance; Shortwave broadband total downwelling irradiance; Shortwave broadband total upwelling irradiance |
| Record | 1997-03-04 to 2026-09-23 (active) |
| Datastreams with data | 183 across 7 sites |
| Sites | bnf, crg, dst, ena, kcg, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/sirs |


## Credit

Everything this skill knows about the instrument is the work of **A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta. *Solar Infrared Radiation Station (SIRS), Sky Radiation (SKYRAD), Ground Radiation (GNDRAD), and Broadband Radiometer Station (BRS) Instrument Handbook*, DOE/SC-ARM-TR-025, April 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `brs` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `sirs`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

Commercially available thermopile-based radiometers measure six broadband irradiance components: direct normal (beam), diffuse horizontal (sky), global horizontal (total hemispheric) shortwave, upwelling (reflected) shortwave, downwelling (atmospheric) longwave, and upwelling (terrestrial) longwave. Shortwave is measured with pyrheliometers (NIP) and pyranometers (PSP or 8-48) with spectral response 295-3000 nm (0.3-3.0 microns), while longwave is measured with pyrgeometers (PIR) with spectral response 3.5-50 microns. The thermopile detector produces a voltage output proportional to net irradiance exchanged with the surroundings; for pyrgeometers, the incoming infrared radiation is computed from thermopile voltage plus case and dome thermistor temperatures using the equation Win = K0 + K1*VTP + K2*Wr + K3*(Wd-Wr). Shortwave global irradiance follows the three-component relationship DS = DNI*Cos(Z) + DD, allowing measured versus derived comparisons for quality checks. Calibrations are traceable to the World Radiometric Reference (WRR) for shortwave and the Interim World Infrared Standard Group (WISG) for longwave.

**Siting.** Radiometers mounted on automatic solar tracker (direct normal, diffuse, downwelling longwave) or stationary/horizontal surface (global shortwave); upwelling shortwave and longwave mounted inverted on a custom stainless steel sun shade atop a 10 m tower (some AMF stations use shorter towers); ventilators used on shaded/global instruments to reduce dust, dew, frost accumulation and thermal offsets; siting affects albedo interpretation (typical 0.2 for vegetation, 0.8 for fresh snow).

**Sampling.** native rate Scanned every 2 seconds (CR10X) or once per second (CR3000, WMO recommended rate); reported every 1-minute (60-second) averages, with instantaneous values appended at 20s, 40s, 60s within the minute; averaging 1-minute average, standard deviation, minimum, and maximum computed from sub-minute scans (hb p. 26).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Direct normal (beam) solar irradiance | Wm-2 | 0.0 to 1100 Wm-2 | ±3.0% (greater than 700Wm-2) [WRR]; calibration... | - | (hb p. 29) |
| Diffuse horizontal (sky) solar irradiance | Wm-2 | 0.0 to 600 Wm-2 | 8-48: +4.0% to -(4%+2 Wm-2) [WRR]; PSP: +4.0%... | - | (hb p. 29) |
| Total hemispheric (global) solar irradiance | Wm-2 | 0.0 to 1400 Wm-2 | ±4.0% to -(4%+20 Wm-2) Zenithless than 80°... | - | (hb p. 29) |
| Total hemispheric (atmospheric) infrared/downwelling... | Wm-2 | 50 to 800 Wm-2 | ±(5.0%+4 Wm-2) [WISG]; calibration ±2% or 2 Wm-2 | - | (hb p. 29) |
| Reflected solar (upwelling shortwave) irradiance | Wm-2 | 0.0 to 1100 Wm-2 | ±2.0% or 10 Wm-2 [WRR]; calibration ±3.0% or 10... | - | (hb p. 29) |
| Upwelling longwave (terrestrial) irradiance | Wm-2 | 100 to 800 Wm-2 | ±2.0 Wm-2 or 2 Wm-2 [WISG]; calibration ±2% or... | - | (hb p. 29) |


## Specifications

| parameter | value | source |
|---|---|---|
| Direct Normal field of view | 5.7° | (hb p. 37) |
| Diffuse Horizontal field of view | 2π sr | (hb p. 37) |
| Downwelling Shortwave field of view | 2π sr | (hb p. 37) |
| Downwelling Longwave field of view | 2π sr | (hb p. 37) |
| Upwelling Shortwave field of view | 2π sr | (hb p. 37) |
| Upwelling Longwave field of view | 2π sr | (hb p. 37) |
| Shortwave wavelength range | 0.3 to 3.0 microns (295 nm-3000 nm) | (hb p. 10) |
| Longwave wavelength range | 3.5 to 50 microns (3.5 µm–50 µm) | (hb p. 10) |
| Direct Normal typical responsivity | 8.0 μV/Wm-2 | (hb p. 25) |
| Diffuse Horizontal (8-48) typical responsivity | 9.0 μV/Wm-2 | (hb p. 25) |
| Downwelling Shortwave (PSP) typical responsivity | 9.0 μV/Wm-2 | (hb p. 25) |
| Downwelling Longwave (PIR) typical responsivity | 4.0 μV/Wm-2 | (hb p. 25) |
| Upwelling Shortwave (PSP) typical responsivity | 9.0 μV/Wm-2 | (hb p. 25) |
| Upwelling Longwave (PIR) typical responsivity | 4.0 μV/Wm-2 | (hb p. 25) |
| Battery/logger voltage nominal | 13 VDC (acceptable range 10-16 VDC) | (hb p. 22) |
| Extraterrestrial Radiation Normal (ETRN) | 1366 ±5 Wm-2 | (hb p. 42) |


## The data

Verified example: **`sgpsirsC1.b1`**, file `sgpsirsC1.b1.20200523.000000.cdf`
(0.48 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 74 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2020-05-23T00:00:00 to 2020-05-23T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 60 seconds |
| dod version | sirs-b1-3.0 |
| process version | ingest-sirs-12.6-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `down_long_hemisp1_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_long_hemisp2_shaded` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer 2 |
| `down_long_hemisp2_shaded_max` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer 2,... |
| `down_long_hemisp2_shaded_min` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer 2,... |
| `down_long_hemisp2_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_long_hemisp_shaded` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer |
| `down_long_hemisp_shaded_max` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer,... |
| `down_long_hemisp_shaded_min` | W/m^2 | time | yes | Downwelling longwave hemispheric irradiance, shaded pyrgeometer,... |
| `down_short_diffuse_hemisp` | W/m^2 | time | yes | Downwelling shortwave diffuse hemispheric irradiance, pyranometer |
| `down_short_diffuse_hemisp_max` | W/m^2 | time | yes | Downwelling shortwave diffuse hemispheric irradiance, pyranometer,... |
| `down_short_diffuse_hemisp_min` | W/m^2 | time | yes | Downwelling shortwave diffuse hemispheric irradiance, pyranometer,... |
| `down_short_diffuse_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Diffuse Hemispheric... |
| `down_short_hemisp` | W/m^2 | time | yes | Downwelling shortwave hemispheric irradiance, pyranometer |
| `down_short_hemisp_max` | W/m^2 | time | yes | Downwelling shortwave hemispheric irradiance, pyranometer, maxima |
| `down_short_hemisp_min` | W/m^2 | time | yes | Downwelling shortwave hemispheric irradiance, pyranometer, minima |
| `down_short_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Hemispheric... |
| `short_direct_normal` | W/m^2 | time | yes | Shortwave direct normal irradiance, pyrheliometer |
| `short_direct_normal_max` | W/m^2 | time | yes | Shortwave direct normal irradiance, pyrheliometer, maxima |
| `short_direct_normal_min` | W/m^2 | time | yes | Shortwave direct normal irradiance, pyrheliometer, minima |
| `up_long_hemisp` | W/m^2 | time | yes | Upwelling longwave hemispheric irradiance, pyrgeometer |
| `up_long_hemisp_max` | W/m^2 | time | yes | Upwelling longwave hemispheric irradiance, pyrgeometer, maxima |
| `up_long_hemisp_min` | W/m^2 | time | yes | Upwelling longwave hemispheric irradiance, pyrgeometer, minima |
| `up_short_hemisp` | W/m^2 | time | yes | Upwelling shortwave hemispheric irradiance, pyranometer |
| `up_short_hemisp_max` | W/m^2 | time | yes | Upwelling shortwave hemispheric irradiance, pyranometer, maxima |
| `up_short_hemisp_min` | W/m^2 | time | yes | Upwelling shortwave hemispheric irradiance, pyranometer, minima |
| `down_long2_netir` | W/m^2 | time | - | Downwelling longwave hemispheric 2 net infrared |
| `down_long_hemisp2_shaded_std` | W/m^2 | time | - | Downwelling longwave hemispheric irradiance, shaded pyrgeometer 2,... |
| `down_long_hemisp_shaded_std` | W/m^2 | time | - | Downwelling longwave hemispheric irradiance, shaded pyrgeometer,... |
| `down_long_netir` | W/m^2 | time | - | Downwelling longwave hemispheric net infrared |
| `down_short_diffuse_hemisp_std` | W/m^2 | time | - | Downwelling shortwave diffuse hemispheric irradiance, pyranometer,... |


_14 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpsirsC1.b1", "2020-05-23", "2020-05-23")
ds = armlive_open("sgpsirsC1.b1", "2020-05-23", "2020-05-23", cleanup_qc=True)
```

This datastream carries 74 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpsirsC1.b1", start, end,
                  keep_variables=["down_long_hemisp1_vent_tachometer", "down_long_hemisp2_shaded", "down_long_hemisp2_shaded_max", "qc_down_long_hemisp1_vent_tachometer", "qc_down_long_hemisp2_shaded", "qc_down_long_hemisp2_shaded_max"])
```

## Quality control in this datastream

25 `qc_` companion variables cover 25 of the
74 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpsirsC1.b1.20200523.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `up_short_hemisp_min` | Value is less than the fail_min. | 556 | 38.6111 |
| `up_short_hemisp` | Value is less than the fail_min. | 544 | 37.7778 |
| `up_short_hemisp_max` | Value is less than the fail_min. | 528 | 36.6667 |
| `down_short_hemisp_min` | Value is less than the fail_min. | 513 | 35.625 |
| `down_short_hemisp` | Value is less than the fail_min. | 499 | 34.6528 |
| `down_short_hemisp_max` | Value is less than the fail_min. | 491 | 34.0972 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpsirsC1.b1", "19970304", "20260923")
```

The handbook's own note on data quality: Until early 2012, each 1-minute irradiance value was assigned a two-digit SERI QC data quality flag (00-99) based on automated K-space (Kt, Kn, Kd) consistency tests (one-, two-, and three-component tests against Gompertz boundaries and physical limits), described in Appendix A (DQMS-3). After the 2012 Linux port, this was replaced with a simplified max/min/delta QC flag system. Users are directed to the QCRAD Value-Added Product (VAP) for best quality-controlled estimates of short- and longwave radiation across SIRS, SKYRAD, GNDRAD, and BRS; QCRAD flags indicate pass/fail and reason. Data...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Three-component mismatch between measured and derived downwelling shortwave | Difference between measured and derived DS as high as -80 W/m2 seen as time-series deviation instead of expected symmetric valley/mountain shape | Replace all three shortwave instruments (global, diffuse, direct) if difference is large and instruments recently installed | (hb p. 15) |
| Infrared measurement deviation between IRT and PIR | Large difference between measured longwave from pyrgeometer versus calculated longwave from infrared thermometer | Indicates one of the two devices is not operating correctly; investigate | (hb p. 17) |
| Asymmetry between three-component instruments | Time series shows two mountains with a valley in between instead of expected single mountain or valley in measured-minus-derived DS plot; also visible in relationship between direct and... | Often caused by an unleveled PSP global horizontal instrument; relevel instrument | (hb p. 17) |
| Clogged ventilator fan | Increased noise in longwave measurement for one shaded instrument compared to a second shaded instrument; daytime gap between the two instruments | Clean the ventilator filter to reduce noise and daytime gap | (hb p. 18) |
| Dirty PSP dome | Measured-vs-derived DS relationship shows sharp changes throughout the day and asymmetry in global measurement instead of expected smooth mountain/valley | Clean the dome; time series returns to expected valley shape for summer | (hb p. 19) |
| Incorrect/stale metadata after instrument swap | Up to nearly 24 hours of partially incorrect metadata (serial numbers/calibration coefficients) in 60-second data following sensor replacement, since metadata only updates via a special... | Cross-check SIRS Operations Management Information System (OMIS) or OSS logs for actual calibration change times; no automated correction implemented | (hb p. 20) |
| UTC/local time offset causing apparent negative nighttime values | Local sunset occurs after 24:00 UTC in summer; negative shortwave irradiance values appear after sunset/through the night due to single black thermopile detector thermal offset | Treat small (less than 15 W/m2) nighttime shortwave irradiance values as 0.0 when computing daily totals | (hb p. 21) |
| Pyranometer thermal offsets (zero offsets) | Generally negative bias in shaded pyranometer output at night and during day due to longwave exchange between thermopile detector, domes, and atmosphere; diffuse irradiance under very clear... | Correction method developed (Dutton et al. 2001) applied via VAP for SIRS data (not applied to pre-conversion SIROS data); replacement of PSP with... | (hb p. 21) |
| Exceeding acceptable measured versus derived (3-component) limits | Difference between measured and derived DS outside empirical limit (-10 W/m2) at night; during day differs by about 20-30 W/m2 (occasionally near 50 W/m2) | Attributed to cosine response artifact of installed PSP coupled with typical radiometer uncertainties and pyranometer responsivity variation with... | (hb p. 23) |
| Pyranometer angular/cosine response non-linearity | Derived-minus-measured DS time series forms symmetric valley (summer) or mountain (winter) shape due to non-linear PSP responsiveness to solar zenith and azimuth position | Characterized via calibration (Rs vs SZA curves); expected pattern used as diagnostic baseline | (hb p. 14) |
| Nighttime thermal offset from AC ventilator fans | Nighttime offset of up to ~-7.2 W/m2 average (PSP) before fan upgrade, seen as negative baseline in irradiance signal at night | Transition from AC to DC fans (ECO-00991) reduced average nighttime offset (PSP from -7.2 to -2.3 W/m2; 8-48 from -0.7 to -0.3 W/m2) | (hb p. 31) |
| Direct normal pyrheliometer window contamination (dust) | Decrease in direct normal irradiance measurement (e.g., 1.6% decrease observed comparing 947.81 vs 963.25 Wm-2 before/after cleaning) | Clean pyrheliometer window regularly | (hb p. 17) |
| Ventilator airflow leakage | Reduced flow over dome; increased thermal offset/noise | Plug cable slot with vinyl foam tape; inspect and correct gaps between sun shield and ventilator housing; replace deformed sun shields | (hb p. 52) |
| Ventilator airflow restriction from dust/filter buildup or inadequate housing spacing | Reduced airflow over dome noticeable in hand-check 'reference flow' test; increased thermal offset noise | Clean fan filter (quarterly best practice, more often in dusty sites); maintain minimum 1 cm spacing between ventilator housing base and mounting... | (hb p. 54) |
| Circumsolar (forward scatter) radiation included in pyrheliometer field of view | NIP field of view (5.7°) wider than solar disc (~0.5°), admitting additional circumsolar radiation into direct normal measurement | Inherent to WMO-specified geometry circa 1960 for tracker alignment tolerance; no correction described | (hb p. 30) |
| Data quality flag system transition (SERI QC to max/min/delta) | Pre-2012 data have two-digit SERI QC flags (00-99); post-2012 (Linux ingest) data use simplified max/min/delta QC flags instead | Users directed to QCRAD VAP for best-estimate quality-controlled data across both eras | (hb p. 14) |
| Physically impossible K-space region (Kn greater than  Kt) | SERI QC flags 94-97 indicate direct normal exceeding total hemispheric by 0.05-≥0.20 K-units, a physically impossible condition | Flagged by DQMS-3 automated assessment for investigation | (hb p. 51) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Component Summation Method (modified ASTM E913-82 shading method) for shortwave using absolute cavity radiometers and shaded reference pyranometers at the SGP Radiometer Calibration Facility (BORCAL); longwave calibration performed outdoors collocated with two reference pyrgeometers using linear regression to... (hb p. 35) |
| Calibration interval | Recalibrated annually (hb p. 35) |
| Traceability | Shortwave traceable to World Radiometric Reference (WRR) via NREL absolute cavity radiometers, maintained through International Pyrheliometer Comparisons (IPC, every 5 years) and annual NREL Pyrheliometer Comparisons (NPC); longwave traceable to the Interim World Infrared Standard Group (WISG) (hb p. 35) |
| Routine maintenance | Cleaning, preventive and corrective maintenance performed during site visits; ventilator filter cleaning (quarterly best practice, more frequent in dusty conditions); flow checks each site inspection; radiometer inventory allows 50% spares to reduce downtime during calibration (hb p. 38) |
| Maintenance interval | Biweekly visits at SGP Extended Facility sites; daily cleaning at C1, E13, and BRS sites (hb p. 38) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SKYRAD, GNDRAD, BRS, MFRSR (multi-filter rotating shadowband radiometer), SIROS.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `SIRS` | solar infrared radiation station |
| `SKYRAD` | sky radiometers on stand for downwelling radiation |
| `GNDRAD` | ground radiometers on stand for upwelling radiation |
| `BRS` | broadband radiometer station |
| `DNI` | Direct Normal Shortwave (Beam) Irradiance |
| `DD` | downwelling diffuse (sky) shortwave irradiance |
| `DS` | downwelling shortwave (global) irradiance |
| `DIR` | downwelling infrared (atmospheric) irradiance |
| `US` | upwelling shortwave (reflected) irradiance |
| `UIR` | upwelling infrared (terrestrial) irradiance |
| `NIP` | Normal Incidence Pyrheliometer |
| `PSP` | Precision Spectral Pyranometer |
| `PIR` | Precision Infrared Radiometer (pyrgeometer) |
| `BORCAL` | Broadband Outdoor Radiometer CALibration |


### References the handbook cites

- BIPM. 1995. Guide to the Expression of Uncertainty in Measurement.
- Cess, RD, T Qian, and M Sun. 2000. Consistency tests applied to the measurement of total, direct, and diffuse shortwave radiation at the surface. JGR-Atmospheres 105(D20): 24881-24887.
- Coulson, KL. 1975. Solar and Terrestrial Radiation Methods and Measurements.
- Dutton, EG, et al. 2001. Measurement of Broadband Diffuse Solar Irradiance Using Current Commercial Instrumentation with a Correction for Thermal Offset Errors. J. Atmos. Oceanic Technol. 18(3): 297-314.
- Gulbrandsen, A. 1978. On the Use of Pyranometers in the Study of Spectral Solar Radiation and Atmospheric Aerosols. J. Appl. Meteorol. 17(6): 899-904.
- Hickey, JR, and AR Karoli. 1974. Radiometer Calibrations for the Earth Radiation Budget Experiment. Applied Optics 13(3): 523-533.
- Myers, DR, KA Emery, and TL Stoffel. 1989. Uncertainty estimates of global solar irradiance measurements used to evaluate PV device performance. Solar Cells 27(1-4): 455-464.
- Reda, I. 2011. Method to Calculate Uncertainty Estimate of Measuring Shortwave Solar Irradiance using Thermopile and Semiconductor Solar Radiometers. NREL Report No. TP-3B10-52194.
- Reda, I, et al. 2012. An absolute cavity pyrgeometer to measure the absolute outdoor longwave irradiance with traceability to SI. J. Atmos. Solar-Terrestrial Physics 77: 132-143.
- Taylor, BN, and CE Kuyatt. 1993. Guidelines for Evaluation and Expressing the Uncertainty of NIST Measurement Results. NIST Technical Note 1297.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf (58 pages, DOE/SC-ARM-TR-025, by A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta)
- Catalog record: ARM data-source index, `instrument_class_code=sirs`, read 2026-09-23
- Example file: `sgpsirsC1.b1.20200523.000000.cdf` from `sgpsirsC1.b1`, 0.48 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
