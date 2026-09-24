---
name: arm-instrument-mwr
description: ARM Microwave Radiometer (mwr) - handbook-derived instrument reference: measurement principle, reported quantities (Total water vapor along LOS path, Total liquid water along LOS path, IR brightness temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpmwrlosC1.b1) and the variable inventory of a real file. Use when working with mwr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Atmospheric Profiling; Cloud Properties; Radiometric. Triggers - mwr, Microwave Radiometer, sgpmwrlosC1.b1, Total water vapor along LOS path, Total liquid water along LOS path, IR brightness temperature, Atmospheric Profiling, Cloud Properties, Radiometric, Radiometrics Corporation WVR-1100 radiometer, AARM, ASCII, BBSS, netCDF.
---

# MWR - Microwave Radiometer

The MWR is a ground-based, zenith-pointing (and tip-curve scanning) microwave receiver deployed at ARM sites that provides time-series measurements of column-integrated water vapor and liquid water by detecting microwave emissions of vapor and liquid water molecules at 23.8 and 31.4 GHz.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mwr` |
| Handbook | [DOE/SC-ARM-TR-016 / VR Morris / April 2019](https://www.arm.gov/publications/tech_reports/handbooks/mwr_handbook.pdf) |
| Measurement category | Atmospheric Profiling; Cloud Properties; Radiometric |
| Manufacturer / model | Radiometrics Corporation WVR-1100 radiometer |
| Primary measurements | Liquid water path; Microwave narrowband brightness temperature; Precipitable water |
| Record | 1993-07-21 to 2026-09-22 (active) |
| Datastreams with data | 115 across 31 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, epc, fkb, gan, grw, guc, hfe, hou |
| ARM page | https://www.arm.gov/capabilities/instruments/mwr |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Microwave Radiometer Handbook*, DOE/SC-ARM-TR-016, April 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mwr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrument is a sensitive microwave receiver tuned to measure sky brightness temperature at 23.8 GHz (a water-vapor-sensitive 'hinge point' frequency insensitive to pressure/altitude) and 31.4 GHz (a liquid-water-sensitive continuum frequency), allowing simultaneous separation of vapor and liquid signals. Observed radiance is related to brightness temperature TB via the radiative transfer equation, combining attenuated cosmic background radiation and atmospheric emission along the line of sight, characterized by optical thickness tau and mean radiating temperature TMR. TB is related to total absorption tau, which is partitioned into dry-air (O2), vapor, and liquid components; observations at the two frequencies yield two equations solved for total vapor (V) and liquid (L) via linear regression coefficients derived from climatology. Calibration uses an internal blackbody target and a noise diode injected into the waveguide to determine gain and offset, removing receiver drift; the receiving cone is steered by a rotating flat mirror and signals are counted via a voltage-to-frequency converter.

**Siting.** Deployed at ARM Central Facility and other sites; instrument observes along a selected line-of-sight path (zenith or scanning) and via tipping-curve air masses at multiple elevation angles (19.5, 23.6, 30.0, 41.8, 90.0, 138.2, 150.0, 156.4, 160.5, 90.0 degrees) on both sides of zenith to assess horizontal homogeneity; anomalies occur near local solar noon at TWP (sun in field of view near equinoxes) and near sunrise/sunset at SGP in east-west tip curve data.

**Sampling.** native rate Standard LOS observations acquired at 15-second intervals (post Oct 1998 upgrade; previously 20-second intervals); sky samples can be acquired at intervals of 2.67 seconds (up to 1024 samples per gain update); reported every Nominally 20 s in LOS mode, 58 s in TIP mode (user selectable); averaging Standard LOS cycle comprises one sky sample per blackbody sample and gain update (hb p. 14).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| 23.8 GHz sky brightness temperature (tbsky23) | K | - | - | - | (hb p. 8) |
| 31.4 GHz sky brightness temperature (tbsky31) | K | - | - | - | (hb p. 8) |
| Total water vapor along LOS path (vap) | cm | - | vapor_retrieval_rms_accuracy = 0.057881 cm... | - | (hb p. 8) |
| Total liquid water along LOS path (liq) | cm | - | liquid_retrieval_rms_accuracy = 0.003083 cm... | - | (hb p. 8) |
| IR brightness temperature (sky_ir_temp) | K | - | - | - | (hb p. 8) |
| 23.8 GHz sky brightness temperature derived from tip curve... | K | - | - | - | (hb p. 8) |
| 31.4 GHz sky brightness temperature derived from tip curve... | K | - | - | - | (hb p. 8) |
| Total water vapor along zenith path using tip-derived... | cm | - | - | - | (hb p. 8) |
| Total liquid water along zenith path using tip-derived... | cm | - | - | - | (hb p. 8) |
| Radiometric brightness temperature (general) | K | 0 to 700 K | 0.3 K | 0.25 K | (hb p. 17) |


## Specifications

| parameter | value | source |
|---|---|---|
| Sample time | User selectable; nominally 20 s in LOS mode, 58 s in TIP mode | (hb p. 17) |
| Accuracy | 0.3 K | (hb p. 17) |
| Resolution | 0.25 K | (hb p. 17) |
| Radiometric range | 0 to 700 K | (hb p. 17) |
| Operating range | -20 to +50°C | (hb p. 17) |
| Power requirements | 120W maximum | (hb p. 17) |
| Voltage requirements | 90 to 130 or 180 to 260 VAC; 50 to 440 Hz | (hb p. 17) |
| Output | ASCII data files to laptop computer via RS-232 at 9600 baud | (hb p. 17) |
| Dimensions | 50 x 28 x 76 cm | (hb p. 18) |
| Weight | 17 kg | (hb p. 18) |
| Angular coverage | all sky | (hb p. 18) |
| Pointing slew rate | 3°/second, azimuth; greater than 90°/second, elevation | (hb p. 18) |
| Field of view | 5.9° at 23 GHz, 4.5° at 31.4 GHz (full width at half maximum) | (hb p. 18) |
| Sky measurement uncertainty | 0.018 K | (hb p. 8) |
| Blackbody measurement uncertainty | 0.12 K | (hb p. 8) |
| Blackbody+noise measurement uncertainty | ~0.15 K | (hb p. 8) |
| Gain reference measurement uncertainty | ~0.02 K | (hb p. 8) |
| Receiver gain measurement uncertainty | ~0.09 K | (hb p. 8) |
| Receiver offset measurement uncertainty | 0.035 K | (hb p. 8) |


## The data

Verified example: **`sgpmwrlosC1.b1`**, file `sgpmwrlosC1.b1.20260922.000000.cdf`
(0.62 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=3797 |
| Data variables | 41 |
| QC variables | 15 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-09-22T00:00:00 to 2026-09-22T23:59:41 |
| sampling interval | 20 seconds |
| dod version | mwrlos-b1-2.3 |
| process version | ingest-mwr-2.3-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bb23` | count | time | yes | 23.8 GHz Blackbody signal |
| `bb31` | count | time | yes | 31.4 GHz Blackbody signal |
| `bbn23` | count | time | yes | 23.8 GHz blackbody+noise injection signal |
| `bbn31` | count | time | yes | 31.4 GHz blackbody+noise injection signal |
| `liq` | cm | time | yes | Total liquid water along LOS path |
| `sky23` | count | time | yes | 23.8 GHz sky signal |
| `sky31` | count | time | yes | 31.4 GHz sky signal |
| `tbsky23` | K | time | yes | 23.8 GHz sky brightness temperature |
| `tbsky31` | K | time | yes | 31.4 GHz sky brightness temperature |
| `time` | - | time | yes | Time offset from midnight |
| `tkair` | K | time | yes | Ambient temperature |
| `tkbb` | K | time | yes | Blackbody kinetic temperature |
| `tknd` | K | time | yes | Noise diode mount temperature |
| `tkxc` | K | time | yes | Mixer kinetic (physical) temperature |
| `vap` | cm | time | yes | Total water vapor along LOS path |
| `tc23` | K/K | time | - | Temperature correction coefficient at 23.8 GHz |
| `tc31` | K/K | time | - | Temperature correction coefficient at 31.4 GHz |
| `tnd23` | K | time | - | Noise injection temp at 23.8 GHz adjusted to tkbb |
| `tnd31` | K | time | - | Noise injection temp at 31.4 GHz adjusted to tkbb |
| `tnd_nom23` | K | time | - | Noise injection temp at nominal temperature at 23.8 GHz |
| `tnd_nom31` | K | time | - | Noise injection temp at nominal temperature at 31.4 GHz |
| `wet_window` | unitless | time | - | Water on Teflon window (1=WET, 0=DRY) |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmwrlosC1.b1", "2026-09-22", "2026-09-22")
ds = armlive_open("sgpmwrlosC1.b1", "2026-09-22", "2026-09-22", cleanup_qc=True)
```

This datastream carries 41 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpmwrlosC1.b1", start, end,
                  keep_variables=["bb23", "bb31", "bbn23", "qc_bb23", "qc_bb31", "qc_bbn23"])
```

## Quality control in this datastream

15 `qc_` companion variables cover 14 of the
41 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

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
act.qc.print_dqr("sgpmwrlosC1.b1", "19930721", "20260923")
```

The handbook's own note on data quality: Most fields have a corresponding automated quality check field named qc_less than fieldnamegreater than  in the b1 level datastreams, with flag values 0-15 encoding combinations of missing-data, minimum, maximum, and delta check failures (Table 5). Minimum/maximum/delta thresholds for each field are defined in Table 6 (e.g., tbsky23 min 2.73 K, max 100 K, delta 0.01 K; liq min -3*rms). PWV/LWP exceeding maximum should be eliminated as usually indicating rain; negative LWP within RMS uncertainty of the retrieval is acceptable and may be treated as zero. Data quality control procedures are...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Water/rain on Teflon window causing invalid data | Retrieved liquid water path (LWP) exceeds 1 cm (qcmax flag raised); PWV and LWP exceed maximum thresholds, usually indicating rain; PWV goes below zero (unphysical) during rain due to... | Eliminate PWV/LWP values exceeding the maximum; use wet_window flag to identify heater-on periods | (hb p. 11) |
| Preventive maintenance window cleaning spikes | Positive 'spikes' produced in the measurements during preventative maintenance due to water used to clean the Teflon window | - | (hb p. 5) |
| Standing water on window after rain stops (lag between rain end and evaporation) | qcmax flags for liquid not completely coincident with weather log reports of rain; instrument continues reporting invalid data after operators report rain has stopped | - | (hb p. 5) |
| Dew/fog formation on window | Distinct smooth 'hump' signature in retrieved vapor and liquid and in underlying brightness temperatures, often near/before dawn; e.g., instrument showed 85-90 microns of liquid coincident... | Anti-dew system (continuous fan + 500-750W heater controlled by moisture sensor) turns on during condensing/precipitating conditions; condition... | (hb p. 6) |
| Heater false triggering on cold nights | wet_window variable indicates heater ON even absent rain/dew/fog, causing confusion when using wet_window as rain/dew/fog indicator (though PWV/LWP measurements themselves unaffected) | MWRs retrofitted with new blowers with greater air flow and heater circuitry less sensitive to ambient temperature | (hb p. 6) |
| Retrieval residual/theoretical uncertainty causing apparent non-zero LWP in clear sky | Significant (+/- 30 g/m3 = +/- 0.03 mm) positive/negative LWP values seen when sky is clear according to ceilometer; noise level itself is much lower (0.003 mm = 0.0003 cm RMS) | Recognize LWP within +/- 0.03 mm of zero could be clear sky; negative LWP within RMS-accuracy of zero may be considered equal to zero (physically... | (hb p. 12) |
| Diurnal variation of mean radiating temperature (Tmr) not accounted for by retrieval... | Zero LWP appears to vary within the uncertainty bounds of the retrieval in an 'annoying fashion' over the diurnal cycle | - | (hb p. 12) |
| Retrieval coefficients based on climatological mean conditions | Clear-sky LWP has larger uncertainty than cloudy-sky LWP (which is closer to climatological mean); apparent offset in LWP under clear-sky conditions | Do not simply subtract clear-sky offset from all LWP values, since cloudy-sky LWP may already be close to correct; reprocess data to fix brightness... | (hb p. 13) |
| Calibration error affecting slope (gain) of calibration rather than offset | Error in noise injection temperature calibration appears as an apparent offset in LWP for clear-sky conditions because retrieved values result from a weighted difference of two channels | Reprocess data to fix brightness temperatures then reapply retrievals | (hb p. 13) |
| Occasional spikes in LWP over 3 mm | LWP spikes exceeding 1 mm or 3 mm, associated with rain, melting snow, or condensation (dew) on window; brightness temperatures over 100 K considered unreliable | Flag set in netCDF data file when brightness temperature exceeds 100 K (used as upper limit rule of thumb) | (hb p. 13) |
| Radiosonde dependency of retrievals (historical) | Retrieval coefficients based on NWS radiosonde data from 1994-1999, so MWR retrievals are not entirely independent of radiosondes | - | (hb p. 14) |
| Tuning function discontinuation / historical inconsistency | Data before 6 April 1996 had tuning functions applied/removed differently; awareness needed when comparing pre- and post-1996 data at SGP CF | Tuning functions discontinued 6 April 1996; removed from SGP CF MWR data collected 950101-960409 by Jim Liljegren; data after this were never tuned,... | (hb p. 8) |
| Sun in field of view near local solar noon | Anomalies in the data near local solar noon; occurs near equinoxes at TWP site in both TIP and LOS modes, and at SGP near sunrise/sunset in east-west tip curve data | - | (hb p. 9) |
| Windows98/DOS software conflict causing spurious spikes (Nov 1999-Jul 2002) | Intermittent spikes in LWP and PWV data caused by blackbody signal counts at half the expected value, yielding negative sky brightness temperatures | Corrected by upgrading MWR software with a new Windows-compatible program | (hb p. 9) |
| Tip-curve calibration invalid in cloudy conditions | Poor linear fit (low R^2) between optical thickness and air mass during tip-curve procedure when clouds present, since absorption is not linearly related to air mass | Regression must account for at least 99.8% of observed variance (R2 = 0.998) to be considered a valid tip-curve calibration; angles on both sides of... | (hb p. 15) |
| Gain sensitivity to component temperature | Slight temperature variations in receiver components (feed horn, waveguides, mixer, local oscillators) cause slope (gain) variations in the calibration curve, producing significant errors... | Microwave hardware mounted on thick aluminum plate in insulated enclosure, thermally stabilized to ±0.25 K; tip-curve data used to derive linear... | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated noise diode injects a known temperature into the antenna waveguide to determine gain; offset determined by observing the internal blackbody target with the radiometer antenna. Tip-curve procedure measures optical thickness at multiple elevation angles/air masses and fits a straight line to derive true... (hb p. 14) |
| Calibration interval | Results of many (greater than 500) tip curves used to compute gain, Vnd, and Tnd; automatic self-calibration can be updated at specified intervals or continuously (hb p. 14) |
| Traceability | Noise injection temperature Tnd is calibrated from tip-curve-derived gain; regression for tip curve must account for at least 99.8% of observed variance (R2 = 0.998) to be considered valid (hb p. 14) |
| Routine maintenance | Preventative maintenance includes cleaning of the Teflon window with water; anti-dew system with continuous fan and 500-750 W heater controlled by moisture sensor keeps window clear of dust and prevents dew/fog/rain accumulation; heater sensitivity needs periodic maintenance; MWRs retrofitted with new blowers with... (hb p. 11) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: balloon-borne sounding system (BBSS), millimeter cloud radar, radiosondes.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `BBSS` | balloon-borne sounding system |
| `CF` | Central Facility |
| `DOS` | Disk Operating System |
| `DQR` | Data Quality Report |
| `ETL` | Environmental Technology Laboratory |
| `GMT` | Greenwich Mean Time |
| `IF` | intermediate frequency |
| `IR` | infrared |
| `LOS` | line-of-sight |
| `LWP` | liquid water path |
| `MWR` | microwave radiometer |
| `netCDF` | Network Common Data Form |


### References the handbook cites

- Liljegren, JC. 1999. Automatic self-calibration of ARM microwave radiometers. Microwave Radiometry and Remote Sensing of the Earth's Surface and Atmosphere, eds. P Pampaloni and S Paloscia, pp. 433-443. VSP Press.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mwr_handbook.pdf (23 pages, DOE/SC-ARM-TR-016, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=mwr`, read 2026-09-23
- Example file: `sgpmwrlosC1.b1.20260922.000000.cdf` from `sgpmwrlosC1.b1`, 0.62 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
