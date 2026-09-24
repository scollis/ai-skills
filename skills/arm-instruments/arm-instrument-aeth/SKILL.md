---
name: arm-instrument-aeth
description: ARM Aethalometer (aeth) - handbook-derived instrument reference. Measurement principle, reported quantities (Black/Elemental Carbon, Optical Attenuation, Sample air flow rate), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (dstaosaeth2spot1mM1.b1) and the variable inventory of a real file. Use when working with aeth data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - aeth, Aethalometer, dstaosaeth2spot1mM1.b1, Black/Elemental Carbon, Optical Attenuation, Sample air flow rate, Aerosols, Magee Scientific Aethalometer (models include AE-16, AE1x 'Standard', SG (sigma), PCMCIA, SLPM.
---

# AETH - Aethalometer

The Aethalometer provides a real-time readout of the concentration of black/elemental carbon aerosol particles by measuring the rate of change of optical transmission through a filter spot on which aerosol is continuously collected as sample air is drawn through it.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 36 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `aeth` |
| Handbook | [DOE/SC-ARM-TR-156 / AJ Sedlacek / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/aeth_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Magee Scientific Aethalometer (models include AE-16, AE1x 'Standard', AE2x 'UV + LED', AE3x '7 x LED', AE4x 'Portable' series) |
| Primary measurements | Aerosol absorption; Black carbon concentration |
| Record | 2012-06-29 to 2026-09-23 (active) |
| Datastreams with data | 31 across 10 sites |
| Sites | anx, asi, cor, crg, dst, epc, hou, mao, nsa, pvc |
| ARM page | https://www.arm.gov/capabilities/instruments/aeth |


## Credit

Everything this skill knows about the instrument is the work of **AJ Sedlacek** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> AJ Sedlacek. *Aethalometer™ Instrument Handbook*, DOE/SC-ARM-TR-156, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/aeth_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The Aethalometer measures the attenuation of a beam of light transmitted through a filter while the filter continuously collects an aerosol sample, at successive regular intervals of a time base period. Optical Attenuation (ATN) is defined as 100*ln(I0/I), where I0 is the intensity through a blank filter portion and I is the intensity through the aerosol-loaded portion. The increase in ATN from one period to the next is proportional to the increment of black carbon collected on the filter, using a wavelength-dependent 'specific attenuation' (sigma) coefficient relating ATN to BC mass loading. Dividing the BC mass increment by the volume of air sampled (flow rate times time) during the period yields the mean BC concentration in the air stream. The measurement uses ratios of Sensing Beam and Reference Beam detector outputs (with lamps on and off to remove zero offsets) so results do not depend on absolute photodetector calibration, only on linearity of response.

**Sampling.** native rate Timebase usually set to 1 to 5 minutes, depending on need; suggested initial 5-minute time base; reported every ARM LabVIEW shell program saves data to an hourly file every 5 minutes when a new set of measurements is available; averaging Mean BC concentration calculated over each time-base period T from the increase in surface loading divided by sampled air volume (hb p. 19).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Black/Elemental Carbon (BC) aerosol concentration | µg/m3 (also ng/m3) | 0 to 500 µg/m3 (detection range 0.1 to... | 10% | 0.1 µg/m3 (dependent on... | (hb p. 12) |
| Optical Attenuation (ATN) | unitless (log ratio x100) | advisory limit 75 to 125; max settable... | - | - | (hb p. 12) |
| Sample air flow rate | liters per minute (LPM/SLPM) | 2 to 6 standard liters per minute... | - | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Measurement range | 0 to 500 µg/m3 | (hb p. 12) |
| Resolution | 0.1 µg/m3 (dependent on dynamic range setting) | (hb p. 12) |
| Time Response | 5 minutes | (hb p. 12) |
| Baseline drift | automatically corrected by use of a reference filter | (hb p. 12) |
| Dimensions | 19 inches wide, 11 inches high, 12 inches deep | (hb p. 12) |
| Weight | less than 40 pounds | (hb p. 12) |
| Power requirements | 85 to 250 VAC/50 to 400 Hz | (hb p. 12) |
| Power consumption | less than 55 W | (hb p. 12) |
| Detection range | 0.1 to ~100 µg/m3 | (hb p. 12) |
| Advisory ATN limit | 75 to 125 (optical absorption depth 0.75 to 1.25); max settable value 150 | (hb p. 12) |
| Accuracy | 10% | (hb p. 12) |
| Repeatability | reference beam repeatability better than 1 part in 10,000 from one cycle to the next | (hb p. 13) |
| Sensitivity | less than 0.1 µg/m3 | (hb p. 13) |
| HS sampling head spot area | 0.5 cm² | (hb p. 13) |
| ER sampling head spot area | 1.67 cm² (3.3x larger than HS) | (hb p. 13) |
| Optimal sampling flow rate | 2 to 6 standard liters per minute | (hb p. 13) |
| Input voltage | 85 to 250 V AC, 50 to 400 Hz | (hb p. 13) |
| Tape roll capacity | 1500 sampling spot locations | (hb p. 13) |
| Analog output voltage range | 0 to +5 V | (hb p. 3) |
| Default output scale factor | 1 mV = 10 ng/m3 BC (i.e., 1 = 10 µg/m3 BC) | (hb p. 3) |
| Onboard computer | embedded 486-class single-board computer, 4-MB dynamic RAM, 2-MB solid-state disk | (hb p. 15) |


## The data

Verified example: **`dstaosaeth2spot1mM1.b1`**, file `dstaosaeth2spot1mM1.b1.20260919.000030.nc`
(0.22 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2, `wavelength`=7 |
| Data variables | 11 |
| QC variables | 2 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:30 to 2026-09-19T23:59:30 |
| sampling interval | 1 second |
| averaging interval | 1 minute |
| dod version | aosaeth2spot1m-b1-4.0 |
| process version | ingest-aosaeth2spot1m-1.1-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Babs` | 1/Mm | time,wavelength | yes | Absorption Coefficient |
| `equivalent_black_carbon` | ng/m^3 | time,wavelength | yes | Equivalent black carbon concentration corrected for loading factors |
| `impactor_state` | 1 | time | - | Impactor state in terms of aerodynamic diameter cut off |
| `time` | - | time | - | Time offset from midnight |
| `wavelength` | nm | wavelength | - | Wavelength of aethelometer optical filter |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("dstaosaeth2spot1mM1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("dstaosaeth2spot1mM1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

## Quality control in this datastream

2 `qc_` companion variables cover 2 of the
11 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (dstaosaeth2spot1mM1.b1.20260919.000030.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `equivalent_black_carbon` | Input source assessment is Indeterminate | 1436 | 14.246 |
| `Babs` | qc_equivalent_black_carbon assessment is Indeterminate | 1342 | 13.3135 |
| `Babs` | Value is equal to missing_value. | 686 | 6.8056 |
| `Babs` | qc_equivalent_black_carbon assessment is Bad, value set to... | 686 | 6.8056 |
| `equivalent_black_carbon` | Value is equal to missing_value. | 686 | 6.8056 |
| `equivalent_black_carbon` | less than  after_impactor_change_alarm seconds after an... | 420 | 4.1667 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("dstaosaeth2spot1mM1.b1", "20120629", "20260923")
```

The handbook's own note on data quality: On a monthly basis, Aethalometer data are checked for quality assurance/quality control during data reduction by the mentor. The message (MF) file logs run summaries per filter spot (total BC collected, running time, sampled air volume, mean BC concentration, standard deviation of BC measurements) and posts warnings for serious problems (pump failure, blockage, lamp failure) as well as each tape advance event, providing a QC record.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Filter-based measurement bias (light scattering, absorption enhancement 'shadowing'... | Systematic bias in BC concentration compared to reference method; affects precision of measurement | Algorithms are available to correct for this bias, but none of them are ideal | (hb p. 13) |
| Optical saturation at high attenuation | Non-linearity in attenuation vs. BC mass above ATN ~150; loss of linear relationship between attenuation and BC mass | Limit measured optical attenuation to values of approximately 150 or less; instrument automatically advances tape before loading becomes too large | (hb p. 9) |
| Filter tape advance / reinitialization | Data gaps of a few minutes during tape advance; analog output forced to -5V ('data not valid') during tape advance/initialization; RUN lamp flashes instead of steady | Program halts temporarily, advances tape, and reinitializes automatically before resuming; blank filler lines with valid date/time but null data... | (hb p. 12) |
| Trade-off between sensitivity and filter change frequency (HS vs ER head, flow rate) | More frequent filter changes and data-collection interruptions/data gaps when using small HS spot at high flow in high-BC-concentration air; noisier data at low flow | Use ER head at lower flow in urban/high-concentration areas for less frequent filter changes; use HS head at higher flow in remote/low-concentration... | (hb p. 13) |
| Tape Remaining percentage inaccuracy | Software-based estimate of tape remaining can become inaccurate and reach zero even though more tape remains on supply spool; yellow Check lamp lights below 10% | Instrument continues to provide valid data even if Check lamp is lit and estimate is low; must use Install New Tape procedure to properly reset... | (hb p. 13) |
| Air flow reporting error due to leaks or blockages (independent of flowmeter calibration) | Internally reported flow (e.g., 4.0 LPM) may differ from true sample flow entering rear-panel port (e.g., 3.8 LPM) due to internal leaks, causing simple scaling bias in reported BC... | Perform periodic external flow audit at inlet port, compare to internal flowmeter signal in 'Signals + Flow' mode; correct by numerical scaling... | (hb p. 27) |
| Disconnected/broken sample inlet hose | Flowmeter reports normal flow (e.g., 4 SLPM) but there is actually no external sample flow at all (air drawn from inside instrument chassis instead) | Verify sampling flow rate via flow audit at inlet port | (hb p. 27) |
| Bypass filter cartridge loading | Cartridge becomes visibly dark, especially when 'Tape Saver' mode used (more air passes through cartridge) | Does not affect analytical operation or data validity unless completely blocked; replace during routine cleaning if visibly dark; low flow resistance... | (hb p. 26) |
| Lack of spectral differentiation from local wood-smoke vs urban ambient sources | Multi-wavelength data show lack of spectral differentiation during the day but a distinct signature of UV-absorbing organics during evening wood-smoke episodes | - | (hb p. 11) |
| Wavelength-dependence of specific attenuation (sigma) is not a physical constant | Sigma value differs by instrument model/wavelength; using wrong sigma value biases BC concentration | Always use the appropriate specific attenuation value for the wavelength of measurement; value must be related to a chemical or other standard... | (hb p. 10) |
| Automatic instrument restart/timeout during operator interaction | Beeping after 10-30 seconds of inactivity, escalating; automatic restart after 10 minutes of no response, potentially interrupting a setup/calibration in progress | Respond to prompts promptly; timer disabled only for SERIOUS fault conditions requiring acknowledgment | (hb p. 15) |
| Serious instrument faults (pump failure, plumbing blockage, lamp failure) | Measurements halt, ERROR lamp flashes red, warning message displayed on screen and logged to message file | Operator attention required to clear fault before measurements resume | (hb p. 22) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Absolute measurement based on sample flow, spot size, and optical attenuation; only periodic checks of the air flowmeter response are required (flowmeter zero and span/scale factor determined using an external flow calibrator) (hb p. 23) |
| Calibration interval | Sample flow checked annually; flow audit recommended at least once per year and before/after any critical study period (hb p. 23) |
| Traceability | External standard flow calibrator/meter reading compared to internal flowmeter signal (hb p. 23) |
| Routine maintenance | Disassembly and cleaning of optical sampling/analysis cylinder; replacement of bypass filter cartridge; filter tape roll replacement (hb p. 25) |
| Maintenance interval | Cleaning once every year or two, or every second tape roll installation (accelerated under high aerosol loading); tape roll lasts hours to months depending on location (hb p. 25) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: PSAP.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ATN` | attenuation |
| `BC` | black carbon |
| `EC` | elemental carbon |
| `SB` | Sensing beam detector output with lamps on |
| `SZ` | Sensing beam detector zero offset output with lamps off |
| `RB` | Reference beam detector output with lamps on |
| `RZ` | Reference beam detector zero output with lamps off |
| `A` | aerosol collecting spot area of filter, [cm²] |
| `F` | flow rate of air through filter, liters per minute |
| `T` | sampling time-base period, minutes |
| `SG (sigma)` | specific attenuation cross section for the aerosol black carbon deposit on filter using... |
| `HS` | High Sensitivity sampling head |
| `ER` | Extended Range sampling head |
| `PCMCIA` | Personal Computer Memory Card International Association |


### References the handbook cites

- Hansen, ADA. 2007. "Operating Manual for the AE31/22/42 Aethalometers." Magee Scientific, Berkeley, California.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/aeth_handbook.pdf (36 pages, DOE/SC-ARM-TR-156, by AJ Sedlacek)
- Catalog record: ARM data-source index, `instrument_class_code=aeth`, read 2026-09-23
- Example file: `dstaosaeth2spot1mM1.b1.20260919.000030.nc` from `dstaosaeth2spot1mM1.b1`, 0.22 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
