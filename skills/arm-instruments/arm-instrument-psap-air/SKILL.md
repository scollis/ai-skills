---
name: arm-instrument-psap-air
description: ARM Particle soot absorption photometer aboard aircraft (psap-air) - handbook-derived instrument reference: measurement principle, reported quantities (Particle absorption coefficient, Particle absorption coefficient, Particle absorption coefficient, Absorbance of aerosols, Instrument mass flow, Transmittance), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaafpsap1sF1.b1) and the variable inventory of a real file. Use when working with psap-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols; Airborne Observations. Triggers - psap-air, Particle soot absorption photometer aboard aircraft, enaaafpsap1sF1.b1, Particle absorption coefficient, Absorbance of aerosols, Instrument mass flow, Transmittance, Aerosols, Airborne Observations, Brechtel Manufacturing, Inc., ACCESS, ASCII, CACTI, HEPA.
---

# PSAP-AIR - Particle soot absorption photometer aboard aircraft

The STAP measures the particle light absorption coefficient at three wavelengths by tracking the decrease in optical transmittance through a filter as aerosol particles are deposited on it, deployed aboard ARM Aerial Facility unmanned aerial systems (e.g., ArcticShark) and aircraft as part of the ACCESS aerosol instrument suite.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `psap-air` |
| Handbook | [DOE/SC-ARM-TR-262 / F Mei, LA Goldberger, C Flynn, M Pekour / November 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-262.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Brechtel Manufacturing, Inc., STAP Model 9406 (part of ACCESS system: base module 9400, filter sampler 9401, MCPC 9403, MOPC 9405, STAP 9406) |
| Primary measurements | Aerosol absorption |
| Record | 2017-06-21 to 2026-09-23 (retired) |
| Datastreams with data | 7 across 2 sites |
| Sites | cor, ena |
| ARM page | https://www.arm.gov/capabilities/instruments/psap-air |


## Credit

Everything this skill knows about the instrument is the work of **F Mei, LA Goldberger, C Flynn, M Pekour** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> F Mei, LA Goldberger, C Flynn, M Pekour. *Single-Channel Tricolor Absorption Photometer (STAP) Instrument Handbook*, DOE/SC-ARM-TR-262, November 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-262.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The STAP uses the same measurement technique as the ARM particle soot absorption photometer (PSAP), based on optical transmittance measurement through a filter over time as aerosol particles are deposited on the filter. The particle absorption coefficient is determined as a function of the decrease in transmittance with increasing aerosol particle loading. The absorption coefficient, sigma_ap, is calculated from Beer's Law using the transmittance ratio (Tr), the flow rate, the area of the deposited spot on the filter, and a Tr correction function, Fr. The 'uncorrected' absorbance coefficients computed via Beer's Law are then processed via the Bond/Ogren algorithm, which uses the normalized filter transmittance and the aerosol scattering coefficient to account for apparent absorption from aerosol scattering. Field data processing must consider filter material differences, aerosol flow fluctuation, and artifacts from aerosol deposition, so an empirically determined filter-loading correction factor is applied.

**Siting.** Deployed on the ARM Aerial Facility's Gulfstream-159 (G-1) after the aircraft's isokinetic inlet inside the cabin (as in CACTI campaign), or installed on the multiple instruments stackable tower (MIST) in the main payload bay of the ArcticShark UAS, connected by four vibration isolators to reduce noise, with outside air brought in via a universal inlet on the nose of the UAS, pumped actively via a scroll pump and controlled with a mass flow controller.

**Sampling.** native rate 1-s signal (noise given as 1-s signal); averaging 60-s averaged intensity data used for repeatability/sensitivity best-case scenario (hb p. 15).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle absorption coefficient (red) | Mm-1 | - | - | - | (hb p. 9) |
| Particle absorption coefficient (green) | Mm-1 | - | - | - | (hb p. 9) |
| Particle absorption coefficient (blue) | Mm-1 | - | - | - | (hb p. 9) |
| Absorbance of aerosols (optical absorbance) | Mm-1 | 0-50 Mm-1 (ambient, non-urban; can be... | - | - | (hb p. 14) |
| Instrument mass flow | - | 0.5 to 1.7 lpm (sample flow) | - | - | (hb p. 14) |
| Transmittance (sample/reference light intensity ratio) | - | - | - | - | (hb p. 14) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavelengths | 450, 525, 624 nm | (hb p. 14) |
| Sample flow | 0.5 to 1.7 lpm | (hb p. 14) |
| Noise level (1 sigma) | +/- 0.2 Mm-1 (0.02 μg/m³ black carbon mass) | (hb p. 14) |
| Filter | Glass fiber, 10-mm dia | (hb p. 14) |
| Size | 5.3 x 4.3 x 3.9 in/13.5 x 10.9 x 9.9 cm | (hb p. 14) |
| Weight | 1.45 lbs/0.66 kg | (hb p. 14) |
| Supply voltage | 12 VDC | (hb p. 14) |
| Power | 10 Watts | (hb p. 14) |
| Mounting | Multiple hard mounting points through metal body brackets | (hb p. 14) |


## The data

Verified example: **`enaaafpsap1sF1.b1`**, file `enaaafpsap1sF1.b1.20180218.122850.nc`
(2.45 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=15167, `bound`=2 |
| Data variables | 33 |
| QC variables | 14 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2018-02-18T12:28:50 to 2018-02-18T16:41:36 |
| sampling interval | 1 second |
| averaging interval | 10 second rolling average for transmittances |
| dod version | aafpsap1s-b1-1.0 |
| process version | ingest-aafpsap10s-1.1-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Ba_B_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, blue channel at dry or... |
| `Ba_B_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, blue channel at dry... |
| `Ba_G_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, green channel at dry or... |
| `Ba_G_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, green channel at... |
| `Ba_R_Weiss` | 1/Mm | time | yes | Aerosol light absorption coefficient, red channel at dry or reference... |
| `Ba_R_raw` | 1/Mm | time | yes | Uncorrected aerosol light absorption coefficient, red channel at dry... |
| `sample_flow_rate` | L/min | time | yes | Mass flow |
| `sample_volume` | L | time | yes | Volume of air through each filter |
| `transmittance_blue` | 1 | time | yes | Transmittance, blue channel |
| `transmittance_green` | 1 | time | yes | Transmittance, green channel |
| `transmittance_red` | 1 | time | yes | Transmittance, red channel |
| `filter_unstable` | 1 | time | - | Filter state |
| `spot_size_area` | mm^2 | - | - | Spot size area |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enaaafpsap1sF1.b1", "2018-02-18", "2018-02-18")
ds = armlive_open("enaaafpsap1sF1.b1", "2018-02-18", "2018-02-18", cleanup_qc=True)
```

## Quality control in this datastream

14 `qc_` companion variables cover 14 of the
33 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (enaaafpsap1sF1.b1.20180218.122850.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ba_G_raw` | Value is less than fail_min | 319 | 2.1033 |
| `Ba_B_raw` | Value is less than fail_min | 291 | 1.9186 |
| `Ba_R_raw` | Value is less than fail_min | 289 | 1.9055 |
| `Ba_G_Weiss` | Value is less than fail_min | 76 | 0.5011 |
| `Ba_R_Weiss` | Value is less than fail_min | 74 | 0.4879 |
| `Ba_B_Weiss` | Value is less than fail_min | 62 | 0.4088 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaafpsap1sF1.b1", "20170621", "20260923")
```

The handbook's own note on data quality: STAP data compared against co-located PSAP data during CACTI campaign using MATLAB processing routines for both instruments. "Level" flight legs (altitude within ±40-m variation) showed good correlation between PSAP and STAP absorption coefficients in cloud-free air; flight average altitude did not significantly affect STAP performance. Ambient temperature, static pressure, differential pressure (ascent/descent rates), and vertical wind speed were analyzed and found not to significantly affect PSAP/STAP differences. Comparison during ascending/descending flight maneuvers also showed similar...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Firmware real-time absorption coefficient higher uncertainty | Onboard STAP firmware particle absorption coefficient values calculated in real time show higher uncertainties (15%) compared to post-processed values | Post-processing of raw data is recommended using Igor-based (Brechtel) or MATLAB-based (Connor Flynn, ARM) software routines | (hb p. 10) |
| Filter material difference between PSAP and STAP | Discrepancies in absorption coefficient comparisons between PSAP and STAP due to different filter media | Data processing considers filter material difference; empirically determined filter-loading correction factor applied | (hb p. 8) |
| Aerosol flow fluctuation | Variability/noise in absorption coefficient signal due to sample flow rate changes | Filter-loading correction factor applied empirically; flow rate correction included in processing | (hb p. 8) |
| Artifact from aerosol deposition (filter loading) | Apparent absorption changes as filter loading increases, not solely due to true aerosol absorption | Bond/Ogren algorithm applied to correct absorbance coefficients using normalized filter transmittance and aerosol scattering coefficient | (hb p. 10) |
| Scattering artifact (apparent absorption from aerosol scattering) | STAP absorbance measurement includes contribution from aerosol scattering, inflating apparent absorption particularly for high single-scattering-albedo aerosols (up to 50% of original... | Bond Corrections: infer scattering on STAP filter based on co-located nephelometry data and correct accordingly | (hb p. 15) |
| Dilution-induced signal degradation | A factor of 0.5 dilution (dilution air set to 50% of sample inlet flow) increases the standard deviation of the signal by ~2-3X; signal measured by instrument reduced proportional to... | Account for dilution ratio and calibration drift of dilution MFC in processing; additional uncertainty introduced by drift in dilution MFC calibration | (hb p. 15) |
| No absolute calibration standard / first-principles measurement limitation | No reference absorbance standard exists to validate STAP readings against | Treated as first-principles measurement; flow rates and spot size calibrated instead | (hb p. 14) |
| Day-to-day and month-to-month repeatability degradation | Confidence intervals for repeatability are larger over longer time periods than short-period repeatability estimates | None stated beyond noting the larger confidence interval | (hb p. 15) |
| Local contamination affecting ambient range | Absorbance values much higher than typical 0-50 Mm-1 range during biomass burn events or local contamination from onsite generator | None stated | (hb p. 14) |
| STAP data plot visualization not yet available | DQ-Zoom Plotter tool example currently shown is from PSAP data, not STAP; STAP plot under development | None stated (in development) | (hb p. 12) |
| Filter transmittance degradation requiring replacement | Blue transmittance channel value decreases below 0.7 over time as filter loads | Change sample and reference filters when blue transmittance less than  0.7, reset transmittance to 1.00, adjust flow to nominal 1.00 slpm | (hb p. 17) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | No effective way to calibrate STAP using a realistic absorbance standard; absorbance is considered a first-principles measurement. Instrument and dilution flow rates and spot size are calibrated and used to process resultant data. Spot size measured upon receipt of instrument. Zero checks not considered appropriate;... (hb p. 14) |
| Calibration interval | Flows calibrated at the beginning of each deployment and generally at 6-12 month intervals in the field. (hb p. 14) |
| Routine maintenance | Filter changes (sample and reference) done when the blue transmittance decreases below 0.7. After filter change, transmittance is reset to 1.00, and flow is adjusted to a nominal 1.00 slpm. (hb p. 17) |
| Maintenance interval | As needed when blue transmittance less than  0.7 (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Particle soot absorption photometer (PSAP), aerosol counting, composition, extinction, and sizing system (ACCESS)..., MCPC, MOPC, filter sampler.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ACCESS` | aerosol counting, composition, extinction, and sizing system |
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `DAQ` | data acquisition |
| `DQ` | data quality |
| `G-1` | Gulfstream-159 |
| `GUI` | graphical user interface |
| `HEPA` | high-efficiency particulate air |
| `MCPC` | mixing condensation particle counter |
| `MFC` | mass flow controller |
| `MIST` | multiple instruments stackable tower |
| `MOPC` | miniaturized optical particle counter |


### References the handbook cites

- Bond, TC, TL Anderson, and D Campbell. 1999. "Calibration and intercomparison of filter-based measurements of visible light absorption by aerosols." Aerosol Science and Technology 30(6): 582-600.
- Lin, C-I, M Baker, and RJ Charlson. 1973. "Absorption coefficient of the atmospheric aerosol: a method for measurement." Applied Optics 12(6): 1356-1363.
- Ogren, JA. 2010. "Comment on 'Calibration and intercomparison of filter-based measurements of visible light absorption by aerosols'." Aerosol Science and Technology 44(8): 589-591.
- Springston, SR. 2018. Particle Soot Absorption Photometer (PSAP) Instrument Handbook. DOE/SC-ARM-TR-176.
- STAP Brochure. Brechtel_Model_9406_STAP_Brochure1.pdf
- STAP 9406 Instrument Manual Ver. 3.4. Brechtel. October, 2020.
- Pikridas, M et al. 2019. "On-flight Intercomparison of three miniature aerosol absorption sensors using unmanned aerial systems (UASs)." Atmospheric Measurement Techniques 12(12): 6425-6447.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-262.pdf (18 pages, DOE/SC-ARM-TR-262, by F Mei, LA Goldberger, C Flynn, M Pekour)
- Catalog record: ARM data-source index, `instrument_class_code=psap-air`, read 2026-09-23
- Example file: `enaaafpsap1sF1.b1.20180218.122850.nc` from `enaaafpsap1sF1.b1`, 2.45 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
