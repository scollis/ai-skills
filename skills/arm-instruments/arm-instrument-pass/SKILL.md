---
name: arm-instrument-pass
description: ARM Photoacoustic Soot Spectrometer (pass) - handbook-derived instrument reference: measurement principle, reported quantities (Absorption coefficient, Scattering coefficient, Extinction coefficient, Sample air temperature, Sample air relative humidity, Sample air pressure, Dew point temperature, Laser power), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaospass3wC1.a1) and the variable inventory of a real file. Use when working with pass data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - pass, Photoacoustic Soot Spectrometer, sgpaospass3wC1.a1, Absorption coefficient, Scattering coefficient, Extinction coefficient, Sample air temperature, Sample air relative humidity, Sample air pressure, Aerosols, Droplet Measurement Technologies (DMT), PASS, Babs, Bscat, Bext.
---

# PASS - Photoacoustic Soot Spectrometer

The PASS measures light absorption (and, with the scattering option, light scattering at three wavelengths) by aerosol particles in situ as they are drawn through a laser beam inside an acoustic resonator, typically deployed as a ground-based, mobile-platform, or airborne rack-mounted instrument.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 55 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `pass` |
| Handbook | [DOE/SC-ARM-TR-123 / January 2013](https://www.arm.gov/publications/tech_reports/handbooks/pass_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Droplet Measurement Technologies (DMT), PASS-3100 / PASS-3 (Three-Wavelength Photoacoustic Soot Spectrometer) |
| Primary measurements | Aerosol absorption; Aerosol scattering |
| Record | 2009-02-19 to 2015-10-01 (retired) |
| Datastreams with data | 4 across 3 sites |
| Sites | mao, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pass |


## Credit

The handbook this skill derives from names no individual author on its cover;
it is issued by the ARM facility. The instrument knowledge in it is still the
mentor programme's work, not this file's:

> ARM Climate Research Facility. *Photoacoustic Soot Spectrometer (PASS) Handbook*, DOE/SC-ARM-TR-123, January 2013.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/pass_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Sample air is drawn through an acoustic resonator at about 1 lpm while a laser beam is square-wave modulated at the resonator's resonance acoustic frequency (fres). Aerosols in the air stream absorb light, periodically heating the surrounding gas, which expands and creates a sound-source pressure wave at frequency fres that is detected by a microphone at one end of the resonator. A piezo element at the other end of the resonator is used to find fres, and laser power is measured with an integrating sphere/photodetector; together these are used to calculate the absorption coefficient Babs. If the scattering option (photomultiplier tube detector) is installed, the instrument simultaneously measures the scattering coefficient Bscat, so absorption, scattering and (via calibration) extinction and single-scattering albedo can all be derived.

**Siting.** Rack-mountable instrument for ground-based, mobile-platform, or airborne applications; entire sampling system is sealed so it can be used on a pressurized aircraft as long as sample air inlet and outlet are at ambient pressure. Back of unit needs support when rack-mounted; vibration isolation kit available. Pump can be located any reasonable distance from the PASS unit.

**Sampling.** native rate Sampling instances normally two seconds apart; reported every 2 seconds (with data gaps during zeroing); averaging Auto Zero Interval and Auto Cal Interval set in number of measurements (200-1800 range); e.g. 450 measurements each = 900 seconds = 15 minutes between zeroing/calibration cycles. Manual or automatic run-averaging sessions also available (user-specified time interval in minutes). (hb p. 33).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Absorption coefficient (Babs) | 1/Mm | - | - | - | (hb p. 14) |
| Scattering coefficient (Bscat) | 1/Mm | - | - | - | (hb p. 14) |
| Extinction coefficient (Bext) | 1/Mm | - | - | - | (hb p. 20) |
| Sample air temperature | degC | 10-40 C operating limit | - | - | (hb p. 13) |
| Sample air relative humidity | % | non-condensing; degraded performance... | - | - | (hb p. 13) |
| Sample air pressure | mBar | - | - | - | (hb p. 53) |
| Dew point temperature | degC | - | - | - | (hb p. 13) |
| Laser power | mW | - | should not fluctuate by more than 5% in a short... | - | (hb p. 34) |


## Specifications

| parameter | value | source |
|---|---|---|
| Technique | Photoacoustic method for light absorption (Babs) and integrated nephelometry for light-scattering (Bscat) | (hb p. 13) |
| Sample Flow | 1 lpm | (hb p. 13) |
| Modulation Frequency | 1500 Hz, square wave | (hb p. 13) |
| Laser | 781 nm (2 W), 532 nm (0.4 W) and 405 nm (0.6 W) | (hb p. 13) |
| Auxiliary Parameters | Temperature, Pressure, Relative Humidity, Dew Point Temperature | (hb p. 13) |
| Calibration | Linear regressions applied to absorption, extinction and scattering coefficients | (hb p. 13) |
| Input Electrical Specifications | 105-125 V or 220-240 V (specify when ordering); 50-60 Hz | (hb p. 13) |
| Power Consumption | Electronics: 100 W; AC Pump: 250 W | (hb p. 13) |
| Weight | 33 kg, excluding pump | (hb p. 13) |
| Dimensions | 19" W x 24" L x 12" H / 48.3 cm W x 61 cm L x 30.5 cm H (7U) | (hb p. 13) |
| Operating Limits - Temperature | 10-40 C; temperatures above 40 C may damage the laser | (hb p. 13) |
| Operating Limits - Relative Humidity | Non-condensing; degraded performance above humidity level of 70% | (hb p. 13) |
| Laser wavelength/max power (Red) | 781 nm, 2 W | (hb p. 8) |
| Laser wavelength/max power (Green) | 532 nm, 0.4 W | (hb p. 8) |
| Laser wavelength/max power (Blue) | 405 nm, 0.6 W | (hb p. 8) |
| Laser classification (safety front matter) | Class I Laser Product | (hb p. 7) |
| Laser classification (maintenance section) | CLASS 4 Laser, rated up to 2 W | (hb p. 28) |
| Output file format | 38 comma-delimited columns, sampling instances normally two seconds apart | (hb p. 51) |
| AD range | 5 V (normally) | (hb p. 45) |
| Amp Gain | 200 (normally); AMP Max Gain should not exceed 200 | (hb p. 41) |
| Microphone Measuring Time | 2.0 sec (default) | (hb p. 46) |
| Df (Hz) | typically 5 Hz | (hb p. 46) |
| Number of zero averages | 16 (factory default) | (hb p. 46) |
| Q (resonator quality factor) | normally around 75 @ 1013 mBar | (hb p. 53) |


## The data

Verified example: **`sgpaospass3wC1.a1`**, file `sgpaospass3wC1.a1.20150928.000101.cdf`
(3.32 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=26732 |
| Data variables | 32 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 2 s |
| File time span | 2015-09-28T00:01:01 to 2015-09-28T23:59:58 |
| sampling interval | 2 seconds |
| averaging interval | None |
| dod version | aospass3w-a1-2.0 |
| process version | ingest-aospass3w-0.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `absorption_coefficient_405nm` | 1/Mm | time | - | Absorption coefficient, 405 nm wavelength |
| `absorption_coefficient_532nm` | 1/Mm | time | - | Absorption, 532 nm wavelength |
| `absorption_coefficient_781nm` | 1/Mm | time | - | Absorption coefficient, 781nm wavelength |
| `acoustic_pressure` | dB | time | - | Acoustic pressure at resonance |
| `avg_background_subtracted_absorp_coef_405nm` | 1/Mm | time | - | Average background subtracted from absorption coefficient, 405nm |
| `avg_background_subtracted_absorp_coef_532nm` | 1/Mm | time | - | Average background subtracted from absorption coefficient, 532nm |
| `avg_background_subtracted_absorp_coef_781nm` | 1/Mm | time | - | Average background subtracted from absorption coefficient, 781nm |
| `avg_background_subtracted_scat_coef_405nm` | 1/Mm | time | - | Average background subtracted from scattering coefficient, 405nm |
| `avg_background_subtracted_scat_coef_532nm` | 1/Mm | time | - | Average background subtracted from scattering coefficient, 532nm |
| `avg_background_subtracted_scat_coef_781nm` | 1/Mm | time | - | Average background subtracted from scattering coefficient, 781nm |
| `dew_point_temperature` | degC | time | - | Dew point temperature |
| `laser_power_405nm` | mW | time | - | Laser Power, 405 nm wavelength |
| `laser_power_532nm` | mW | time | - | Laser Power, 532 nm wavelength |
| `laser_power_781nm` | mW | time | - | Laser Power, 781 nm wavelength |
| `pressure` | hPa | time | - | Pressure |
| `resonance_frequency` | Hz | time | - | Resonance frequency |
| `rh` | % | time | - | Relative humidity |
| `running_average` | unitless | time | - | Running average indicator, 0=no, 1=yes |
| `sample_measurement_flag` | unitless | time | - | Indicates occurrence of background zero |
| `scattering_coefficient_405nm` | 1/Mm | time | - | Scattering coefficient, 405 nm wavelength |
| `scattering_coefficient_532nm` | 1/Mm | time | - | Scattering coefficient, 532 nm wavelength |
| `scattering_coefficient_781nm` | 1/Mm | time | - | Scattering coefficient, 781 nm wavelength |
| `temperature` | degC | time | - | Temperature |
| `temperature_laser` | degC | time | - | Laser temperature |
| `time` | - | time | - | Time offset from midnight |
| `uncertainty_estimate_405nm` | 1/Mm | time | - | Uncertainty estimate for absorption coefficient, 405 nm wavelength |
| `uncertainty_estimate_532nm` | 1/Mm | time | - | Uncertainty estimate for absorption coefficient, 532 nm wavelength |
| `uncertainty_estimate_781nm` | 1/Mm | time | - | Uncertainty estimate for absorption coefficient, 781nm wavelength |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaospass3wC1.a1", "2015-09-28", "2015-09-28")
ds = armlive_open("sgpaospass3wC1.a1", "2015-09-28", "2015-09-28", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `sample_measurement_flag`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaospass3wC1.a1", "20090219", "20260923")
```

The handbook's own note on data quality: Housekeeping channels are provided for QC purposes: P0_dB (peak acoustic pressure during acoustic calibration, should remain stable if microphone sensitivity is constant); Phase_deg (should be near zero with strong absorption signal, random -180 to 180 with no signal); AverageBackgroundSubtractedBabs_1/Mm and BscaBackGnd_1/Mm (background stability, should stay relatively constant during stable conditions, dramatic changes indicate a problem); NoiseEqBabs_1/Mm (uncertainty estimate for Babs, useful instrument-response metric); ADrange_v (amplification factor, should be ~200 and definitely...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| High relative humidity degrades performance | Degraded/erratic Babs or Bscat readings when sample RH exceeds ~70% | Keep sample air non-condensing and below 70% RH; RH_% housekeeping channel should stay below 70% for optimum performance | (hb p. 13) |
| High temperature can damage laser | Instrument shutdown or laser failure if operating temperature exceeds 40 C | Keep operating temperature in 10-40 C range; shutoff temp control can be set to auto-shutdown instrument above a threshold | (hb p. 13) |
| Background/zero drift with environmental conditions | AverageBackgroundSubtractedBabs_1/Mm and BscaBackGnd_1/Mm housekeeping channels change with variables like temperature; dramatic changes indicate a problem | Background is determined during instrument zero; monitor these channels for stability, shorten auto zero/cal interval if... | (hb p. 29) |
| Stray laser light causes background absorption signal | Non-zero Background[laser frequency] value on Babs tab representing background signal from stray laser light hitting the resonator | Background value is subtracted from raw signal (Babs = Babs,raw - Babs,bg) | (hb p. 34) |
| Dirty optics (window/prism) reduce measurement quality | Drop in laser-power readings (LaserPower_mW channel) | Clean window and prism periodically (every 3-12 months ambient, weekly for diesel exhaust); only clean when visibly dirty since excessive cleaning... | (hb p. 26) |
| Clogged inlet tubing | Pressure rises during a zero count | Open access panel, check small-diameter conductive tubing, replace if necessary | (hb p. 32) |
| Cabling/grounding problem in acoustic circuit | Raw and Fit curves on the Acoustic tab do not overlap | Ensure resonator is grounded and microphone cable is connected | (hb p. 32) |
| Phase indicates absence or presence of absorption signal | Phase_deg is random between -180 and 180 degrees when there is no signal (e.g., filter on inlet); approaches zero during high absorbing aerosol concentrations | Use Phase_deg as a diagnostic of signal validity; background phase calculated during auto-zeroing is used to correct raw phase | (hb p. 33) |
| Amplifier gain auto-reduction discards outlier measurements | Amp Gain Factor automatically lowered when measurement out of range, and the outlier measurement is thrown out | Amp Gain Factor will not rise above AMP Max Gain (should not exceed 200) | (hb p. 41) |
| Sample flow rate cannot be accurately measured at back-panel inlet | Flow reading at sample inlet includes resonator flow plus bypass flow through zero filter, giving an inflated/incorrect flow value | Measure sample flow through the resonator at the line immediately before the resonator | (hb p. 26) |
| Data gaps during zeroing and calibration cycles | Sampling instances normally two seconds apart but gaps appear in the output file when PASS-3 is zeroing | None specified beyond expected periodic zero/cal cycle (Auto Zero/Cal Interval) | (hb p. 48) |
| Calibration validity depends on scattering-negligible or estimated properly | Absorption calibration via black-carbon source requires additional correction term (Bscat - Bext) because scattering is not negligible, unlike NO2 method | Prefer NO2 gas calibration method since scattering is negligible and does not need to be estimated | (hb p. 21) |
| Single-laser operation required during calibration | Cross-talk or inaccurate calibration if more than one laser operating simultaneously during calibration | Calibrate PASS-3 with only one laser operating at a time | (hb p. 17) |
| Consumables not covered by warranty and require replacement | Degraded flow, filtration or humidification performance from worn tubing, filters, pump diaphragms, Nafion humidifier | Replace consumable components as part of routine maintenance (not covered by warranty) | (hb p. 6) |
| Tlaser_C channel is unused | Column present in output file but contains no meaningful data | None specified | (hb p. 54) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Scattering calibrated using highly scattering aerosol (e.g., PSL particles) by regressing calculated extinction (Bext) against measured Bscat; absorption calibrated preferably using NO2 gas (regressing Bext vs Babs, scattering negligible) or alternatively a black-carbon source (regressing [Bscat-Bext] vs Babs,... (hb p. 15) |
| Calibration interval | Bi-monthly (absorption and scattering calibration); routine auto-zero/auto-cal cycle every 200-1800 measurements during operation (e.g. every 15 minutes) (hb p. 15) |
| Traceability | NO2 gas calibration: each ppb of NO2 produces ~0.395 Mm-1 absorption at STP (0 C, 1013.25 mBar); recommended 200,000 ppb NO2 producing ~79,000 Mm-1 absorption at STP (hb p. 15) |
| Routine maintenance | Monthly: check/replace filter in front of Temperature/RH sensor and zero-air filter (McMaster part 4795K3, 99.99% efficiency at .01 micron); check DRIERITE color (blue to pink indicates replacement needed). Bi-monthly: calibrate absorption and scattering measurements; check sample flow rate at line immediately before... (hb p. 23) |
| Maintenance interval | Monthly / Bi-monthly / 3-12 months (optics) depending on aerosol type sampled (hb p. 23) |


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
| `PASS` | Photoacoustic Soot Spectrometer |
| `Babs` | Absorption coefficient measured photoacoustically |
| `Bscat` | Scattering coefficient measured via integrated nephelometry/PMT |
| `Bext` | Extinction coefficient, calculated from laser power attenuation; Bext = Babs + Bscat |
| `fres` | Resonance acoustic frequency of the resonator |
| `Q` | Resonator quality factor |
| `STP` | Standard temperature and pressure, 0 C and 1013.25 mBar |
| `PSL` | Polystyrene latex particles used for scattering calibration |
| `TTL` | Time-to-live, UDP parameter decremented by 1 at each router hop |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/pass_handbook.pdf (55 pages, DOE/SC-ARM-TR-123, no individual author named on the cover)
- Catalog record: ARM data-source index, `instrument_class_code=pass`, read 2026-09-23
- Example file: `sgpaospass3wC1.a1.20150928.000101.cdf` from `sgpaospass3wC1.a1`, 3.32 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
