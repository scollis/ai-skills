---
name: arm-instrument-brs
description: ARM Broadband Radiometer Station (brs) - handbook-derived instrument reference. Measurement principle, reported quantities (Direct normal, Diffuse horizontal, Total hemispheric, Total hemispheric, Reflected solar irradiance, Upwelling longwave irradiance), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpbrs60sC1.b1) and the variable inventory of a real file. Use when working with brs data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric. Triggers - brs, Broadband Radiometer Station, sgpbrs60sC1.b1, Direct normal, Diffuse horizontal, Total hemispheric, Reflected solar irradiance, Upwelling longwave irradiance, Radiometric, The Eppley Laboratory, Inc. models - NIP (pyrheliometer), SIRS, SKYRAD, GNDRAD, SIROS.
---

# BRS - Broadband Radiometer Station

The Broadband Radiometer Station (BRS) collection of radiometers provides continuous 1-minute measurements of downwelling broadband shortwave (solar) and longwave (infrared) irradiances at the ARM SGP Central Facility, operated in association with the WMO Baseline Surface Radiation Network (BSRN), with no upwelling measurements.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 58 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `brs` |
| Handbook | [DOE/SC-ARM-TR-025 / A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta](https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | The Eppley Laboratory, Inc. models: NIP (pyrheliometer), PSP (Precision Spectral Pyranometer), 8-48 (Black & White pyranometer), PIR (Precision Infrared Radiometer/pyrgeometer); tracker: Kipp & Zonen... |
| Primary measurements | Longwave broadband downwelling irradiance; Longwave broadband upwelling irradiance; Shortwave broadband diffuse downwelling irradiance; Shortwave broadband direct normal irradiance; Shortwave broadband total downwelling irradiance; Shortwave broadband total upwelling irradiance |
| Record | 2001-03-05 to 2026-09-22 (active) |
| Datastreams with data | 5 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/brs |


## Credit

Everything this skill knows about the instrument is the work of **A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta. *Solar Infrared Radiation Station (SIRS), Sky Radiation (SKYRAD), Ground Radiation (GNDRAD), and Broadband Radiometer Station (BRS) Instrument Handbook*, DOE/SC-ARM-TR-025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `sirs` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `brs`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

Downwelling shortwave (0.3-3.0 micron) irradiance is measured with thermopile-based pyrheliometers (direct normal beam, tracked to the sun) and pyranometers (diffuse horizontal, shaded and ventilated; and total hemispheric/global, unshaded and ventilated), all producing a voltage signal proportional to incident irradiance via a calibrated responsivity. Downwelling longwave (3.5-50 micron) irradiance is measured with a shaded, ventilated pyrgeometer whose thermopile output is combined with case and dome thermistor temperatures using the equation Win = K0 + K1*VTP + K2*Wr + K3*(Wd-Wr), where Wr and Wd are blackbody irradiances computed from case and dome temperatures via the Stefan-Boltzmann relation. Three-component shortwave irradiance measurements are cross-checked via DS = DNI*Cos(Z) + DD, providing an internal consistency test. All commercial thermopile pyranometers exhibit a non-zero "thermal offset" signal at night and during the day due to thermal gradients between the detector and instrument body/domes, which must be corrected. Calibration of shortwave radiometers is traceable to the World Radiometric Reference (WRR) via component summation method calibration against absolute cavity radiometers; longwave radiometers are calibrated outdoors overnight against reference pyrgeometers using linear regression to derive K0-K3 coefficients.

**Siting.** BRS is located at the ARM SGP Central Facility, near the SIRS C1 station, and collects downwelling-only measurements (no upwelling measurements at this station). It is part of the WMO Baseline Surface Radiation Network (BSRN) global network. Like C1 and E13, the BRS station is cleaned daily, as opposed to the biweekly cleaning at Extended Facility sites. Pyranometers must be properly leveled; an unleveled global horizontal PSP causes asymmetry artifacts. Ventilator/sun-shield/tracker mounting geometry (even circumferential spacing between sun shield and dome, correct ventilator height on tracker plates) affects shading and airflow and thus data quality.

**Sampling.** native rate sampled once per second (CR3000) or once every two seconds (legacy CR10X); reported every 1-minute data (average, std dev, min, max), with instantaneous values appended at 20s, 40s, 60s within each minute; averaging 1-minute averages computed from 1-second (or 2-second) scans; 20-second data are raw/unaveraged values (hb p. 26).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Direct normal (beam) solar irradiance | Wm-2 | 0.0 to 1100 Wm-2 (typical); ETRN limit | ±3.0% (greater than 700 Wm-2), WRR uncertainty;... | - | (hb p. 20) |
| Diffuse horizontal (sky) solar irradiance | Wm-2 | 0.0 to 600 Wm-2 (typical) | 8-48: +4.0% to -(4%+2 Wm-2); PSP: +4.0% to... | - | (hb p. 20) |
| Total hemispheric (global) solar irradiance | Wm-2 | 0.0 to 1400 Wm-2 (typical); ETR limit | ±4.0% to -(4%+20 Wm-2), Zenith less than 80... | - | (hb p. 20) |
| Total hemispheric (atmospheric) infrared irradiance... | Wm-2 | 50 to 800 Wm-2 (typical) | ±(5.0%+4 Wm-2), WISG uncertainty; calibration... | - | (hb p. 20) |
| Reflected solar irradiance (upwelling shortwave) | Wm-2 | 0.0 to 1100 Wm-2 (typical) | ±2.0% or 10 Wm-2, WRR; calibration uncertainty... | - | (hb p. 20) |
| Upwelling longwave irradiance | Wm-2 | 100 to 800 Wm-2 (typical) | ±2.0 Wm-2 or 2 Wm-2, WISG; calibration... | - | (hb p. 20) |


## Specifications

| parameter | value | source |
|---|---|---|
| Direct Normal (beam) [DNI] Field of View / Wavelength Range | 5.7 deg / 0.3 to 3.0 microns | (hb p. 37) |
| Diffuse Horizontal (sky) [DD] Field of View / Wavelength... | 2π sr / 0.3 to 3.0 microns | (hb p. 37) |
| Downwelling Shortwave (global) [DS] Field of View /... | 2π sr / 0.3 to 3.0 microns | (hb p. 37) |
| Downwelling Longwave (atmospheric) [DIR] Field of View /... | 2π sr / 3.5 to 50 microns | (hb p. 37) |
| Upwelling Shortwave (reflected) [US] Field of View /... | 2π sr / 0.3 to 3.0 microns | (hb p. 37) |
| Upwelling Longwave (terrestrial) [UIR] Field of View /... | 2π sr / 3.5 to 50 microns | (hb p. 37) |
| Direct Normal NIP Typical Responsivity / Calibration... | 8.0 microV/Wm-2 / ±2.5% or 2 Wm-2 | (hb p. 33) |
| Diffuse Horizontal 8-48 Typical Responsivity / Calibration... | 9.0 microV/Wm-2 / ±3.0% or 10 Wm-2 | (hb p. 33) |
| Downwelling Shortwave PSP Typical Responsivity /... | 9.0 microV/Wm-2 / ±3.0% or 10 Wm-2 | (hb p. 33) |
| Downwelling Longwave PIR Typical Responsivity / Calibration... | 4.0 microV/Wm-2 / ±2% or 2 Wm-2 | (hb p. 33) |
| Upwelling Shortwave PSP Typical Responsivity / Calibration... | 9.0 microV/Wm-2 / ±3.0% or 10 Wm-2 | (hb p. 33) |
| Upwelling Longwave PIR Typical Responsivity / Calibration... | 4.0 microV/Wm-2 / ±2% or 2 Wm-2 | (hb p. 34) |
| Extraterrestrial Radiation Normal (ETRN) | 1366 ±5 Wm-2 | (hb p. 42) |
| Data logger acceptable voltage range | 10-16 VDC (nominally 13 VDC) | (hb p. 22) |
| Ventilator housing to mounting plate spacing | minimum 1 cm | (hb p. 56) |
| Shortwave (solar) radiometer spectral response | 295 nm-3000 nm | (hb p. 10) |
| Longwave (infrared) radiometer spectral response | 3.5 micron-50 micron | (hb p. 10) |
| NIP field of view design basis | 0.5 deg solar disc at earth's surface, per WMO circa 1960 design requirements | (hb p. 38) |


## The data

Verified example: **`sgpbrs60sC1.b1`**, file `sgpbrs60sC1.b1.20260919.000000.nc`
(0.43 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 65 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| sampling interval | 1 second |
| averaging interval | 60 seconds |
| dod version | brs60s-b1-5.0 |
| process version | ingest-skyrad-1.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `down_long_hemisp1` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1 |
| `down_long_hemisp1_max` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Maxima |
| `down_long_hemisp1_min` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Minima |
| `down_long_hemisp1_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_long_hemisp2` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2 |
| `down_long_hemisp2_max` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Maxima |
| `down_long_hemisp2_min` | W/m^2 | time | yes | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Minima |
| `down_long_hemisp2_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Longwave Hemispheric... |
| `down_short_diffuse_hemisp` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer |
| `down_short_diffuse_hemisp_corrected` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_corrected_max` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_corrected_min` | W/m^2 | time | yes | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_max` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_diffuse_hemisp_min` | W/m^2 | time | yes | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_diffuse_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Diffuse Hemispheric... |
| `down_short_hemisp` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `down_short_hemisp_corrected` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer |
| `down_short_hemisp_corrected_max` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_corrected_min` | W/m^2 | time | yes | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_max` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer, Maxima |
| `down_short_hemisp_min` | W/m^2 | time | yes | Downwelling Shortwave Hemispheric Irradiance, Pyranometer, Minima |
| `down_short_hemisp_vent_tachometer` | rpm | time | yes | Ventilation tachometer for Downwelling Shortwave Hemispheric... |
| `short_direct_normal` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer |
| `short_direct_normal_max` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer, Maxima |
| `short_direct_normal_min` | W/m^2 | time | yes | Shortwave Direct Normal Irradiance, Pyrheliometer, Minima |
| `down_long_hemisp1_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer1, Standard... |
| `down_long_hemisp2_std` | W/m^2 | time | - | Downwelling Longwave Hemispheric Irradiance, Pyrgeometer2, Standard... |
| `down_short_diffuse_hemisp_corrected_std` | W/m^2 | time | - | Corrected Downwelling Shortwave Diffuse Hemispheric Irradiance,... |
| `down_short_diffuse_hemisp_std` | W/m^2 | time | - | Downwelling Shortwave Diffuse Hemispheric Irradiance, Pyranometer,... |
| `down_short_hemisp_corrected_std` | W/m^2 | time | - | Corrected Downwelling Shortwave Hemispheric Irradiance, Pyranometer,... |


_5 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpbrs60sC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("sgpbrs60sC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

This datastream carries 65 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpbrs60sC1.b1", start, end,
                  keep_variables=["down_long_hemisp1", "down_long_hemisp1_max", "down_long_hemisp1_min", "qc_down_long_hemisp1", "qc_down_long_hemisp1_max", "qc_down_long_hemisp1_min"])
```

## Quality control in this datastream

25 `qc_` companion variables cover 25 of the
65 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpbrs60sC1.b1", "20010305", "20260923")
```

The handbook's own note on data quality: Until early 2012, each 1-minute irradiance value was assigned a two-digit SERI_QC/DQMS-3 data quality flag (00-99, see Appendix A) based on automated K-space (Kt, Kn, Kd) consistency tests (one-, two-, and three-component tests against Gompertz boundaries and physical limits). After the Linux port in early 2012, this was replaced with a simplified max/min/delta QC flag system. Users are now directed to the QCRAD Value-Added Product (VAP), which assesses data quality and enhances data continuity for ARM radiation data at all Central and Extended Facilities, and includes QC flags indicating...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Pyranometer thermal (zero) offsets | Negative nighttime shortwave irradiance values (typically less than 15 W/m2 but can be as much as 30 W/m2 under clear-sky nighttime conditions); diffuse irradiance below the physical... | Treat small (less than 15 W/m2) nighttime shortwave irradiances as 0.0 when computing daily totals; apply Dutton et al. (2001) correction method... | (hb p. 29) |
| Three-component shortwave mismatch (measured vs. derived DS) | Derived minus measured downwelling shortwave time series shows a symmetric valley in summer / mountain in winter under proper operation; a mismatch as high as -80 W/m2 seen when... | Replace all three shortwave instruments (global, diffuse, direct) if mismatch persists after installation | (hb p. 14) |
| Asymmetry between three-component instruments | Time series of measured minus derived DS shows two mountains with a valley in between instead of the expected single mountain or valley; visible asymmetry between direct and global... | Often caused by an unleveled PSP global horizontal instrument; releveling the instrument | (hb p. 17) |
| Infrared measurement deviation between IRT (infrared thermometer) and PIR (pyrgeometer) | Large difference between measured longwave from pyrgeometer versus calculated longwave from infrared thermometer | Indicates one of the two devices is not operating correctly; investigate instrument | (hb p. 17) |
| Clogged ventilator fan filter | Increased noise in longwave measurement from the affected 'shaded' instrument compared to a redundant instrument; daytime gap and noise reduced after cleaning | Clean ventilator filter | (hb p. 18) |
| Dirty PSP dome | Measured vs. derived DS relationship in time series shows sharp changes throughout the day instead of expected smooth mountain/valley shape; asymmetry in global measurement | Clean the dome; time series returns to expected valley shape after cleaning | (hb p. 19) |
| Pyrheliometer window contamination (dust) | Direct normal irradiance decreases before cleaning and jumps after cleaning (e.g., 947.81 vs 963.25 Wm-2, ~1.6% decrease due to dust) | Regular window cleaning (daily at BRS/C1/E13, biweekly at EF sites) | (hb p. 17) |
| Incorrect/stale metadata for calibration coefficients and serial numbers | Up to nearly 24 hours of partially incorrect metadata in the 60-second data after a sensor swap, because the metadata table (Table 214) is only updated once daily at 23:59 GMT even though... | Not corrected operationally (would require turning off ingest); consult SIRS OMIS or TWP OMIS for correction info; future logging via ARM OSS | (hb p. 20) |
| UTC time convention causes apparent late sunset / date-boundary confusion | Local sunset can appear to occur after 24:00 UTC in summer in daily data files; nighttime negative shortwave values throughout night depending on cloud cover | Be aware data are recorded in UTC (00:00-23:59); treat small nighttime negative values as zero | (hb p. 29) |
| Exceeding acceptable measured vs. derived (three-component) limits | Difference between measured and derived DS exceeds empirical limit of -10 W/m2 at night; during day differences of 20-30 W/m2 (occasionally near 50 W/m2) | Attributed to cosine response artifact of installed PSP and typical radiometer uncertainties; also affected by pyranometer responsivity variation... | (hb p. 31) |
| Non-linear pyranometer angular (cosine) response with solar zenith/azimuth | Variable PSP responsivity affecting three-component calculations; calibration results show Rs varying with SZA and local time (Figure 16) | Determined/verified via calibration; major contributor to estimated measurement uncertainty | (hb p. 30) |
| Ventilator airflow leakage (cable slot gap, sun shield/housing gap) | Reduced ventilation flow over dome; increased noise/offset in shaded pyrgeometer/pyranometer measurements | Plug cable slot with vinyl foam tape; inspect and correct gap between sun shield and ventilator housing; replace deformed sun shields | (hb p. 52) |
| Ventilator airflow restriction (dirty fan filter, inadequate housing-to-mounting-plate... | Reduced ventilator output airflow detectable by hand-check against reference flow; increased thermal offset/noise | Clean fan filter (quarterly or more often), maintain minimum 1 cm spacing between ventilator housing base and mounting plate | (hb p. 53) |
| AC fan-induced nighttime thermal offset (pre-2014/2015) | Larger negative nighttime PSP/8-48 offsets prior to fan upgrade (average before change -7.2 W/m2 for PSP, -0.7 W/m2 for 8-48 across sites) | Transition from AC to DC fans under ECO-00991 reduced average nighttime offset (to -2.3 W/m2 for PSP, -0.3 W/m2 for 8-48) | (hb p. 31) |
| Pyrgeometer calibration coefficients historically not directly measured | Historical SIRS pyrgeometer IR computed using theoretical K0-K4 values and Eppley responsiveness rather than measured coefficients (K0=0, K1=1/Responsiveness, K2=1, K3=-4, K4=0) | New outdoor calibration method (post-2015, ECO-00781) measures actual K0-K3 coefficients via linear regression against reference pyrgeometers | (hb p. 35) |
| SERI_QC / DQMS-3 flagging artifacts and physically impossible K-space regions | Two-digit QC flag (00-99) per 1-minute value; flags 94-97 indicate physically impossible region where Kn greater than  Kt by increasing K-space distance | Use QCRAD VAP for best-estimate quality-controlled data; SERI_QC discontinued in early 2012 in favor of simplified max/min/delta flags for archived... | (hb p. 49) |
| Snow and frost accumulation on domes/ventilators at cold-climate sites | Obstruction of measurement noticeable in data during winter; addressed at NSA, OLI, AMF cold-climate deployments with heated ventilators | Ventilated (and heated at NSA/OLI/SBS/TMP) radiometers; remove snow accumulations during site visits | (hb p. 25) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Component Summation Method (modified ASTM E913-82 shading method) for shortwave radiometers using absolute cavity radiometers and shaded reference pyranometers (BORCAL events at SGP Radiometer Calibration Facility); longwave pyrgeometers calibrated outdoors overnight (zenith greater than 96 deg) collocated with two... (hb p. 35) |
| Calibration interval | Pyranometers and pyrheliometers recalibrated annually at the SGP Radiometer Calibration Facility (RCF); existing radiometer inventory allows for 50% spares to reduce station downtime during calibration (hb p. 35) |
| Traceability | Shortwave: traceable to World Radiometric Reference (WRR) maintained by World Radiation Center (WRC) for WMO, via NREL-maintained group of three electrically self-calibrating absolute cavity radiometers, with traceability maintained via International Pyrheliometer Comparisons (IPC, every 5 years) and NREL... (hb p. 35) |
| Routine maintenance | Cleaning, preventive maintenance, corrective maintenance during site visits; ventilator fan filter cleaning (quarterly best practice, more often in dusty conditions); flow checks against a 'reference flow' each inspection; check/plug cable slot leaks; check for gaps under sun shield; confirm 1 cm minimum... (hb p. 6) |
| Maintenance interval | BRS/C1/E13 cleaned daily; Extended Facility sites cleaned bi-weekly; ventilator filter cleaning quarterly (best practice, site-dependent); radiometers recalibrated annually (hb p. 6) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SIRS (Solar Infrared Radiation Station), SKYRAD (Sky Radiometers on stand for downwelling radiation), GNDRAD (Ground Radiometers on stand for upwelling radiation), SIROS (Solar and Infrared Radiation Observation Station, predecessor..., MFRSR (multi-filter rotating shadowband radiometer), QCRAD VAP.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `BRS` | broadband radiometer station |
| `SIRS` | solar infrared radiation station |
| `SKYRAD` | sky radiometers on stand for downwelling radiation |
| `GNDRAD` | ground radiometers on stand for upwelling radiation |
| `SIROS` | solar and infrared radiation observation station |
| `DNI` | Direct Normal Shortwave (Beam) Irradiance |
| `DD` | downwelling diffuse (shortwave sky irradiance) |
| `DS` | downwelling shortwave (global/total hemispheric) irradiance |
| `DIR` | downwelling infrared (atmospheric) irradiance |
| `US` | upwelling shortwave (reflected) irradiance |
| `UIR` | upwelling infrared (terrestrial) irradiance |
| `BORCAL` | Broadband Outdoor Radiometer CALibration |
| `WRR` | World Radiometric Reference |
| `WISG` | Interim World Infrared Standard Group |


### References the handbook cites

- BIPM. 1995. Guide to the Expression of Uncertainty in Measurement.
- Dutton, EG, et al. 2001. Measurement of Broadband Diffuse Solar Irradiance Using Current Commercial Instrumentation with a Correction for Thermal Offset Errors. J. Atmos. Oceanic Technol. 18(3): 297-314.
- Gulbrandsen, A. 1978. On the Use of Pyranometers in the Study of Spectral Solar Radiation and Atmospheric Aerosols. J. Appl. Meteorol. 17(6): 899-904.
- Cess, RD, T Qian, and M Sun. 1999/2000. Consistency Tests Applied to the Measurement of Total, Direct, and Diffuse Shortwave Radiation at the Surface. JGR-Atmospheres 105(D20): 24881-24887.
- Myers, DR, KA Emery, and TL Stoffel. 1989. Uncertainty estimates of global solar irradiance measurements used to evaluate PV device performance. Solar Cells 27(1-4): 455-464.
- Taylor, BN, and CE Kuyatt. 1993. Guidelines for Evaluation and Expressing the Uncertainty of NIST Measurement Results. NIST Technical Note 1297.
- Reda, I. 2011. Method to Calculate Uncertainty Estimate of Measuring Shortwave Solar Irradiance using Thermopile and Semiconductor Solar Radiometers. NREL Report TP-3B10-52194.
- Reda, I, et al. 2012. An absolute cavity pyrgeometer to measure the absolute outdoor longwave irradiance with traceability to SI. J. Atmos. Solar-Terrestrial Physics 77: 132-143.
- Reda, I. 1999. Improving the Shade/Unshade Method to Calculate the Responsivities of Solar Pyranometers. NREL Report TR-26483.
- Michalsky, J, M Kutchenreiter, and C Long. 2017. Significant improvements in pyranometer nighttime offsets using high-flow DC ventilation. J. Atmos. Oceanic Technol. 34(6): 1323-1332.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/sirs_handbook.pdf (58 pages, DOE/SC-ARM-TR-025, by A Andreas, M Dooraghi, A Habte, M Kutchenreiter, I Reda, M Sengupta)
- Catalog record: ARM data-source index, `instrument_class_code=brs`, read 2026-09-23
- Example file: `sgpbrs60sC1.b1.20260919.000000.nc` from `sgpbrs60sC1.b1`, 0.43 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
