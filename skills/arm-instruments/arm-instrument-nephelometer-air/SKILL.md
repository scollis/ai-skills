---
name: arm-instrument-nephelometer-air
description: ARM 3-Wavelength integrating nephelometer aboard aircraft (nephelometer-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Sample air pressure, Sample relative humidity, Sample and inlet temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaaafneph10sF1.b1) and the variable inventory of a real file. Use when working with nephelometer-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - nephelometer-air, 3-Wavelength integrating nephelometer aboard aircraft, nsaaafneph10sF1.b1, Sample air pressure, Sample relative humidity, Sample and inlet temperature, Aerosols, Airborne Observations, TSI Incorporated, model 3563 integrating nephelometer, ACE-ENA, ASCII, HEPA, Netcdf.
---

# NEPHELOMETER-AIR - 3-Wavelength integrating nephelometer aboard aircraft

The TSI model 3563 integrating nephelometer measures aerosol particle light-scattering (total and backscatter) coefficients at three wavelengths (450, 550, 700 nm) while sampling directly from the isokinetic manifold aboard the ARM Aerial Facility's Gulfstream-159 aircraft.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `nephelometer-air` |
| Handbook | [DOE/SC-ARM-TR-248 / J Uin, L Goldberger / June 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-248.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | TSI Incorporated, model 3563 integrating nephelometer |
| Primary measurements | Aerosol backscattered radiation; Aerosol scattering |
| Record | 2013-06-26 to 2026-09-23 (active) |
| Datastreams with data | 17 across 6 sites |
| Sites | acx, cor, ena, mao, nsa, osc |
| ARM page | https://www.arm.gov/capabilities/instruments/nephelometer-air |


## Credit

Everything this skill knows about the instrument is the work of **J Uin, L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin, L Goldberger. *Nephelometer Aboard Aircraft Instrument Handbook*, DOE/SC-ARM-TR-248, June 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-248.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The instrument draws an aerosol sample through a large-diameter inlet into a measurement volume illuminated over an angle of 7 to 170° by a halogen lamp directed through an optical light pipe and opal glass diffuser. Three photomultiplier tubes view the sample volume through apertures, and dichroic filters split the scattered light into blue (450 nm), green (550 nm), and red (700 nm) bandpass channels. A rotating reference chopper alternately provides the aerosol scattering signal, a measure of PMT dark current (subtracted from the signal), and a measure of the light-source signal so that changes in lamp output or detector efficiency are compensated over time. In backscatter mode, a backscatter shutter blocks light in the 7 to 90° range so only backward-scattered light (90-170°) reaches the detectors, allowing forward-scatter to be derived by subtraction from the total signal. Periodically, an automated valve diverts the sample through a HEPA filter to measure the clean-air (zero) signal, which along with the dark-current signal is subtracted from the aerosol-scatter signal to isolate the true particle-scattering contribution.

**Siting.** On board the aircraft, the nephelometer samples directly from the isokinetic manifold with a designated heater mounted just upstream of the nephelometer inlet fitting. The internal relative humidity is controlled via temperature variation and is normally kept at or below 40%. The nephelometer onboard the G-1 was installed in the aerosol rack and controlled via the main aircraft data system, powered from an uninterruptible power supply via a designated switch to prevent electrical interruptions.

**Sampling.** native rate 1-Hz resolution with the M300 data acquisition system on the G-1; reported every Separate data files started for preflight tests and for each flight; averaging Particle-scattering parameters for all three wavelengths of total and backscatter signal are continuously averaged and passed to a computer for permanent storage; detection limit specified for 1-second average and for averaging times longer than ~60 seconds (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle optical scattering coefficient (total... | inverse meters (m-1) or... | Upper detection limit 2x10-2 m-1; lower... | ±10% (Anderson et al. 1996) | - | (hb p. 11) |
| Aerosol particle optical scattering coefficient... | inverse meters (m-1) or... | Angular integration 90 to 170° | ±10% (Anderson et al. 1996) | - | (hb p. 11) |
| Sample air pressure | hectoPascals (hPa) | - | - | - | (hb p. 11) |
| Sample relative humidity | percent (%) | normally kept at or below 40% | - | - | (hb p. 11) |
| Sample and inlet temperature | Kelvin (K) | - | - | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units - scattering coefficient | inverse meters (m-1) or inverse mega-meters (Mm-1) | (hb p. 11) |
| Units - relative humidity | percent (%) | (hb p. 11) |
| Units - air pressure | hectoPascals (hPa) | (hb p. 11) |
| Units - temperature | Kelvin (K) | (hb p. 11) |
| Upper detection limit (scattering coefficient) | 2x10-2 m-1 | (hb p. 11) |
| Lower limit (sensitivity, 1-second measurement) | about 1x10-6 | (hb p. 11) |
| Angular integration - total scatter mode | 7 to 170° | (hb p. 11) |
| Angular integration - backscatter mode | 90 to 170° | (hb p. 11) |
| Accuracy | within ±10% (Anderson et al. 1996) | (hb p. 11) |
| Truncation error - submicron particles | 5-10% | (hb p. 11) |
| Truncation error - particles 1-10 μm | 30-50% | (hb p. 11) |
| Repeatability | within ±1% (Anderson and Ogren 1998) | (hb p. 11) |
| Detection limit (1-second average, typical aircraft... | about 1x10-6 m-1 | (hb p. 12) |
| Gas calibration uncertainty contribution | about ±1% | (hb p. 12) |
| Systematic uncertainty (wavelength/angular non-idealities) | within ±10% (Anderson et al. 1998) | (hb p. 12) |


## The data

Verified example: **`nsaaafneph10sF1.b1`**, file `nsaaafneph10sF1.b1.20150930.180955.nc`
(0.44 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=2107, `bound`=2 |
| Data variables | 41 |
| QC variables | 19 (`qc_` companions) |
| Median time step | 10 s |
| File time span | 2015-09-30T18:09:55 to 2015-10-01T00:00:55 |
| sampling interval | 1 second |
| averaging interval | 10 s |
| dod version | aafneph10s-b1-1.0 |
| process version | ingest-aafneph10s-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Bbs_B` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal blue... |
| `Bbs_B_raw` | 1/Mm | time | yes | Uncorrected aerosol back-hemispheric light scattering coefficient,... |
| `Bbs_G` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal green... |
| `Bbs_G_raw` | 1/Mm | time | yes | Uncorrected aerosol back-hemispheric light scattering coefficient,... |
| `Bbs_R` | 1/Mm | time | yes | Aerosol back-hemispheric light scattering coefficient, nominal red... |
| `Bbs_R_raw` | 1/Mm | time | yes | Uncorrected aerosol back-hemispheric light scattering coefficient,... |
| `Bs_B` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal blue wavelength |
| `Bs_B_raw` | 1/Mm | time | yes | Uncorrected aerosol total light scattering coefficient, nominal blue... |
| `Bs_G` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal green wavelength |
| `Bs_G_raw` | 1/Mm | time | yes | Uncorrected aerosol total light scattering coefficient, nominal green... |
| `Bs_R` | 1/Mm | time | yes | Aerosol total light scattering coefficient, nominal red wavelength |
| `Bs_R_raw` | 1/Mm | time | yes | Uncorrected aerosol total light scattering coefficient, nominal red... |
| `P_sample` | hPa | time | yes | Pressure inside nephelometer |
| `RH_sample` | % | time | yes | Relative humidity inside nephelometer |
| `T_inlet` | degC | time | yes | Temperature at nephelometer inlet |
| `T_sample` | degC | time | yes | Sample temperature inside nephelometer |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsaaafneph10sF1.b1", "2015-09-30", "2015-09-30")
ds = armlive_open("nsaaafneph10sF1.b1", "2015-09-30", "2015-09-30", cleanup_qc=True)
```

This datastream carries 41 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("nsaaafneph10sF1.b1", start, end,
                  keep_variables=["Bbs_B", "Bbs_B_raw", "Bbs_G", "qc_Bbs_B", "qc_Bbs_B_raw", "qc_Bbs_G"])
```

## Quality control in this datastream

19 `qc_` companion variables cover 19 of the
41 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (nsaaafneph10sF1.b1.20150930.180955.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Bs_G_raw` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |
| `Bs_R_raw` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |
| `Bbs_B_raw` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |
| `Bbs_G_raw` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |
| `Bbs_R_raw` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |
| `Bs_G` | Transformation resulted in an indeterminate outcome. | 757 | 35.9279 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsaaafneph10sF1.b1", "20130626", "20260923")
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging of data based on criteria developed by instrument mentors, plus automatic generation of plots in collaboration with the ARM Data Quality Office. Automatic checks include monitoring the "mode" variable to determine operating mode (normal, zeroing) and flagging data accordingly, and ensuring RH levels inside the nephelometer are maintained below 40%. Plots are available via the ARM Facility Data Quality Diagnostic Plot Browser.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Angular truncation error | Scattering coefficients biased low relative to true values; error magnitude varies with particle size - 5-10% for submicron particles, 30-50% for particles 1-10 μm, due to limited 7-170°... | Consider as additional source of measurement error for certain applications (Anderson and Ogren 1998) | (hb p. 11) |
| Sensitivity to sample pressure and humidity | Scattering coefficient measurements vary with sample pressure and RH conditions; no automatic correction applied so values from different times/locations may not be directly comparable | No automatic corrections are applied by the instrument; care should be taken when comparing measurement results from different times and locations | (hb p. 12) |
| Random noise dominant at low concentration / short averaging | At low particle concentrations or short (e.g., 1-second) sampling times, measured scattering coefficient shows increased scatter/noise near the detection limit (~1x10-6 m-1) | - | (hb p. 12) |
| Systematic uncertainty from gas calibration and wavelength/angular non-idealities | For scattering coefficients above ~10-6 m-1 and averaging times longer than ~60 s, a systematic offset (within ±10%) dominates over random noise; gas calibration alone contributes ~±1% | - | (hb p. 12) |
| Upper detection limit / saturation | Scattering coefficient readings clip or become unreliable above 2x10-2 m-1 | - | (hb p. 11) |
| Lower detection limit set by sensitivity | Below about 1x10-6 m-1 (for 1-second measurement) signal is indistinguishable from noise floor | - | (hb p. 11) |
| Zero/background subtraction requirement (wall, gas, dark current scatter) | Raw signal includes contributions from carrier gas, instrument walls, and detector background noise unless zeroed; periodic HEPA-filtered 'zero' periods appear as flat/low baseline segments... | Zeroing performed during preflight for each research flight; automated HEPA valve diverts sample periodically to measure clean-air signal, which is... | (hb p. 7) |
| Operating mode changes (normal vs. zeroing) | 'mode' variable switches between normal and zeroing states; data during zeroing should not be treated as ambient scattering measurement | Automatic QC checks flag data according to which operating mode the instrument is in | (hb p. 10) |
| Internal RH control excursions | If internal RH rises above 40%, measured optical properties may be affected by hygroscopic growth artifacts; flagged in QC | Internal RH is controlled via temperature variation and normally kept at or below 40%; automatic QC checks ensure RH levels inside nephelometer are... | (hb p. 7) |
| Lamp failure/degradation | Visual inspection or software status indicates lamp failure; scattering signal intensity/light-source signal channel may drop or become unstable | Replace halogen lamp when visual inspection or software status indicates failure, and before each field campaign | (hb p. 14) |
| HEPA filter degradation | Clean-air (zero) signal measurement may drift if internal HEPA filter is not replaced regularly | Replace internal HEPA filter before each field campaign | (hb p. 14) |
| No automatic ambient-condition correction applied | Reported scattering coefficients are at instrument's internal sample conditions (pressure, RH, temperature), not corrected to standard conditions, so cross-comparison across... | Care should be taken when comparing measurement results from different times and locations | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Measuring scattering coefficients of dry test gas (CO2, SF6, or freon) introduced into the system and comparing them with known values from literature adjusted for calibration conditions (temperature, RH, air pressure); calibration coefficients recorded into internal nephelometer memory and applied to raw measurement... (hb p. 11) |
| Calibration interval | Calibrated by manufacturer before delivery and during instrument maintenance; instrument mentors perform calibration as needed; span-checked with CO2 before each deployment; 'zero' test run during preflight preparation before each flight (hb p. 11) |
| Traceability | Anderson et al. 1996 (hb p. 11) |
| Routine maintenance | Replacing the halogen lamp (when visual inspection or software status indicates lamp failure and before each field campaign); replacing the internal HEPA filter before each field campaign (hb p. 14) |
| Maintenance interval | Before each field campaign / as needed (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `ASCII` | American Standard Code for Information Interchange |
| `G-1` | Gulfstream 159 |
| `HEPA` | high-efficiency particulate air |
| `Netcdf` | Network Common Data Form |
| `PMT` | photomultiplier tube |
| `RH` | relative humidity |
| `UTC` | Coordinated Universal Time |


### References the handbook cites

- Anderson, TL, and JA Ogren. 1998. "Determining aerosol radiative properties using the TSI 3563 Integrating Nephelometer." Aerosol Science and Technology 29(1): 57-69.
- Anderson, TL, DS Covert, SF Marshall, ML Laucks, RJ Charlson, AP Waggoner, JA Ogren, R Caldow, RL Holm, FR Quant, GJ Sem, A Wiedensohler, NA Ahlquist, and TS Bates. 1996. "Performance characteristics of a...
- Heintzenberg, J, and RJ Charlson. 1996. "Design and applications of the integrating nephelometer: A review." Journal of Atmospheric and Oceanic Technology 13(5): 987-1000.
- TSI 3563 Nephelometer description by NOAA Earth System Research Laboratory Global Monitoring Division. 2015.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-248.pdf (16 pages, DOE/SC-ARM-TR-248, by J Uin, L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=nephelometer-air`, read 2026-09-23
- Example file: `nsaaafneph10sF1.b1.20150930.180955.nc` from `nsaaafneph10sF1.b1`, 0.44 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
