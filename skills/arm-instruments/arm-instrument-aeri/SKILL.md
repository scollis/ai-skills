---
name: arm-instrument-aeri
description: ARM Atmospheric Emitted Radiance Interferometer (aeri) - handbook-derived instrument reference: measurement principle, reported quantities (Calibrated spectral radiance, Spectral blackbody radiance, Blackbody temperature, Front-end ambient temperature, Hatch status, Ambient air temperature, Ambient pressure, Ambient humidity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaerisummaryC1.b1) and the variable inventory of a real file. Use when working with aeri data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Radiometric. Triggers - aeri, Atmospheric Emitted Radiance Interferometer, sgpaerisummaryC1.b1, Calibrated spectral radiance, Spectral blackbody radiance, Blackbody temperature, Front-end ambient temperature, Hatch status, Ambient air temperature, Radiometric, ABB Inc. (current manufacturer of hardware, licensed from University of Wisconsin), AERI, AERI QC, ER-AERI, FTSW.
---

# AERI - Atmospheric Emitted Radiance Interferometer

The AERI is a ground-based Fourier transform spectrometer that measures downwelling infrared radiance from the atmosphere, typically deployed in a thru-wall configuration with the front-end outside and the back-end in a temperature-controlled indoor environment.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `aeri` |
| Handbook | [DOE/SC-ARM-TR-054 / J Gero, D Hackel / March 2025](https://www.arm.gov/publications/tech_reports/handbooks/aeri_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | ABB Inc. (current manufacturer of hardware, licensed from University of Wisconsin); originally built by University of Wisconsin (V1, V2) |
| Primary measurements | Longwave spectral brightness temperature; Longwave spectral radiance |
| Record | 1994-01-10 to 2026-09-21 (active) |
| Datastreams with data | 209 across 31 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/aeri |


## Credit

Everything this skill knows about the instrument is the work of **J Gero, D Hackel** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Gero, D Hackel. *Atmospheric Emitted Radiance Interferometer (AERI) Instrument Handbook*, DOE/SC-ARM-TR-054, March 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/aeri_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The AERI is a Fourier transform interferometer of Michelson design, with cube corners mounted on a voice-coil actuated wishbone structure. Broadband downwelling radiation enters the aperture, is split into two beams by a beamsplitter, recombined, and focused by aft-optics onto two broadband single pixel thermal detectors cooled to cryogenic temperatures, producing an interferogram as a function of optical path difference (-1 to +1 cm). A HeNe metrology laser samples the interferogram at evenly spaced intervals via its sinusoidal signal. The digitized, coadded interferogram is Fourier transformed into a raw spectrum, then converted to a calibrated spectrum using the calibration equation (Revercomb et al. 1988) referencing two blackbody targets with traceable temperature and emissivity, with additional corrections for instrument effects (Knuteson et al. 2004b).

**Siting.** Typically mounted in a thru-wall configuration with the front-end outside and the back-end in a temperature-controlled indoor environment; a protective enclosure shields the front-end from sun, rain, snow, wind, sand; a hatch actuated by precipitation sensors closes to protect the scene mirror and front-end optics during precipitation, and the AERI does not acquire sky data during precipitation events.

**Sampling.** native rate Interferometer scan from -1 to +1 cm optical path difference per scan; reported every Sky/blackbody views averaged over 17 second interval; calibration views every 3 minutes in standard rapid sample mode; averaging Sky and blackbody views averaged over a 17 second interval (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Calibrated spectral radiance | Radiance Units (RU = mW m-2... | Channel 1: 520-1800 cm-1; Channel 2:... | less than 1% of ambient blackbody radiance | 0.5 cm-1 unapodized (max... | (hb p. 9) |
| Spectral blackbody radiance | RU | - | - | - | (hb p. 9) |
| Blackbody temperature | K | HBB controlled to 333 K; ABB passively... | - | - | (hb p. 7) |
| Front-end ambient temperature | - | - | - | - | (hb p. 9) |
| Hatch status | - | open/closed | - | - | (hb p. 9) |
| Ambient air temperature (secondary) | - | - | not rigorously calibrated | - | (hb p. 9) |
| Ambient pressure (secondary) | - | - | not rigorously calibrated | - | (hb p. 9) |
| Ambient humidity (secondary) | - | - | not rigorously calibrated | - | (hb p. 9) |
| Noise-equivalent radiance (NEN) | RU | AERI: less than 0.2 RU 670-1400 cm-1,... | - | - | (hb p. 12) |
| Repeatability | % of ambient blackbody... | - | less than 0.2% | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Spectral range (standard AERI) | 3.3-19.2 µm (520-3020 cm-1) | (hb p. 7) |
| Spectral range (ER-AERI) | 3.3-25.0 µm (400-3020 cm-1) | (hb p. 7) |
| Unapodized resolution | 0.5 cm-1 (max optical path difference of 1 cm) | (hb p. 7) |
| Detectors | HgCdTe and InSb, cooled to cryogenic temperatures with a Stirling cycle cooler | (hb p. 7) |
| Field of view | 46 mrad full angle, zenith angular | (hb p. 7) |
| Absolute radiometric accuracy | less than 1% of the radiance of a blackbody at surface ambient temperature | (hb p. 7) |
| Hot Blackbody (HBB) temperature | 333 K, temperature controlled | (hb p. 7) |
| Ambient Blackbody (ABB) temperature | passively follows ambient temperature | (hb p. 7) |
| Scan sequence | eight sky views and two calibration blackbody views, averaged over a 17 second interval, repeating continuously | (hb p. 7) |
| Repeatability | less than 0.2% of ambient blackbody radiance | (hb p. 12) |
| Noise (AERI) | less than 0.2 RU for 670-1400 cm-1; less than 0.015 RU for 2000-2600 cm-1 (except 667 cm-1 and 2300-2400 cm-1 where CO2 reduces responsivity) | (hb p. 12) |
| Noise (ER-AERI) | less than 0.4 RU for 420-1400 cm-1; less than 0.015 RU for 2000-2600 cm-1 (except 667 cm-1 and 2300-2400 cm-1 where CO2 reduces responsivity) | (hb p. 12) |
| Laser | 632.8 nm, 1 mW red HeNe metrology laser, Class 1 instrument | (hb p. 18) |
| Calibration view interval (standard rapid sample mode) | every 3 minutes | (hb p. 10) |


## The data

Verified example: **`sgpaerisummaryC1.b1`**, file `sgpaerisummaryC1.b1.20260921.000405.nc`
(13.48 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=3847, `wnumsum1`=71, `wnumsum2`=56, `wnumsum3`=58, `wnumsum4`=48, `wnumsum5`=71, `wnumsum6`=56, `wnumsum7`=71, `wnumsum8`=56, `wnumsum9`=71, `wnumsum10`=56, `wnumsum11`=50, `wnumsum12`=48, `wnumsum13`=50, `wnumsum14`=48 |
| Data variables | 79 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 16 s |
| File time span | 2026-09-21T00:04:05 to 2026-09-21T23:53:28 |
| sampling interval | about 16 seconds |
| averaging interval | Use sceneViewDuration |
| dod version | aerisummary-b1-2.2 |
| process version | ingest-aeri-12.2-4.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `time` | - | time | yes | Time offset from midnight |
| `ABBmaxTempDiff` | K | time | - | Maximum temperature difference between ABB thermistors |
| `AERIunitNumber` | unitless | time | - | AERI instrument unit serial number |
| `Altitude` | m | time | - | Observation altitude |
| `HBB2minNENestimateNo1Ch1` | mW/(m^2 sr cm^-1) | time,wnumsum7 | - | AERI LW HBB 2min NESR estimate #1 derived from variance during HBB... |
| `HBB2minNENestimateNo1Ch2` | mW/(m^2 sr cm^-1) | time,wnumsum8 | - | AERI SW HBB 2min NESR estimate #1 derived from variance during HBB... |
| `HBB2minNENestimateNo2Ch1` | mW/(m^2 sr cm^-1) | time,wnumsum9 | - | AERI LW HBB 2min NESR estimate #2 derived from sequential HBB views... |
| `HBB2minNENestimateNo2Ch2` | mW/(m^2 sr cm^-1) | time,wnumsum10 | - | AERI SW HBB 2min NESR estimate #2 derived from sequential HBB views... |
| `HBBmaxTempDiff` | K | time | - | Maximum temperature difference between HBB thermistors |
| `HBBstable` | unitless | time | - | Logical flag indicating whether HBB temperature is stable (true) or... |
| `HBBtempDrift` | K | time | - | The maximum excursion of hot-blackbody temperature over 5 consecutive... |
| `JulianDay` | days | time | - | Julian day including day and fraction of day |
| `LW_HBB_NEN` | mW/(m^2 sr cm^-1) | time | - | Longwave HBB noise-equivalent radiance |
| `LWresponsivity` | counts/[mW/(m^2 sr... | time | - | Characteristic value representing overall longwave channel... |
| `LWskyNEN` | mW/(m^2 sr cm^-1) | time | - | The noise equivalent radiance observed in the longwave channel during... |
| `LWskyNENacceptable` | unitless | time | - | Logical flag indicating whether longwave channel noise equivalent... |
| `Latitude` | degrees | time | - | Observation latitude |
| `Longitude` | degrees | time | - | Observation longitude |
| `ResponsivitySpectralAveragesCh1` | counts/[mW/(m^2 sr... | time,wnumsum1 | - | AERI LW responsivity spectral averages (ch1) |
| `ResponsivitySpectralAveragesCh2` | counts/[mW/(m^2 sr... | time,wnumsum2 | - | AERI SW responsivity spectral averages (ch2) |
| `SW_HBB_NEN` | mW/(m^2 sr cm^-1) | time | - | Shortwave HBB noise-equivalent radiance |
| `SWresponsivity` | counts/[mW/(m^2 sr... | time | - | Characteristic value representing overall shortwave channel... |
| `SWskyNEN` | mW/(m^2 sr cm^-1) | time | - | The noise equivalent radiance observed in the shortwave channel... |
| `SWskyNENacceptable` | unitless | time | - | Logical flag indicating whether shortwave channel noise equivalent... |
| `SkyBrightnessTempSpectralAveragesCh1` | K | time,wnumsum13 | - | AERI LW scene brightness temp spectral averages (ch1) |
| `SkyBrightnessTempSpectralAveragesCh2` | K | time,wnumsum14 | - | AERI SW scene brightness temp spectral averages (ch2) |
| `SkyNENCh1` | mW/(m^2 sr cm^-1) | time,wnumsum5 | - | AERI LW scene NESR spectral averages (ch1) |
| `SkyNENCh2` | mW/(m^2 sr cm^-1) | time,wnumsum6 | - | AERI SW scene NESR spectral averages (ch2) |
| `SkyRadianceSpectralAveragesCh1` | mW/(m^2 sr cm^-1) | time,wnumsum11 | - | AERI LW Scene radiance spectral averages (ch1) |
| `SkyRadianceSpectralAveragesCh2` | mW/(m^2 sr cm^-1) | time,wnumsum12 | - | AERI SW scene radiance spectral averages (ch2) |


_58 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaerisummaryC1.b1", "2026-09-21", "2026-09-21")
ds = armlive_open("sgpaerisummaryC1.b1", "2026-09-21", "2026-09-21", cleanup_qc=True)
```

This datastream carries 79 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpaerisummaryC1.b1", start, end,
                  keep_variables=["time", "ABBmaxTempDiff", "AERIunitNumber", "qc_time"])
```

## Quality control in this datastream

1 `qc_` companion variables cover 0 of the
79 data variables. Assessments present in the example file: `Indeterminate`.

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
act.qc.print_dqr("sgpaerisummaryC1.b1", "19940110", "20260923")
```

The handbook's own note on data quality: The AERI software performs real-time QC checks with problem conditions flagged in the FTSW display window and stored with the data. ARM Data Quality Reports (DQRs) flag periods greater than 24 hours where data may be suspect, incorrect, or missing. Basic user-level QC parameters include Hatch Open, LW HBB NEN, SW HBB NEN, LW Responsivity, and SW Responsivity. A mentor product, AERI QC (part of the AERI ARMORY software package), algorithmically calculates data quality flags using about 20 different quality control tests; it requires raw AERI data obtained directly from the instrument or via...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Precipitation blocks valid sky data | During rain/snow the hatch closes and 'sky' views actually look at the inside of the closed hatch, which resembles an ambient temperature blackbody spectrum; Hatch Open flag = 0 | Remove data using the Hatch Open flag (only Hatch Open = 1 is valid atmospheric data) | (hb p. 18) |
| CO2 absorption reduces responsivity at specific bands | Elevated noise/reduced responsivity at 667 cm-1 and 2300-2400 cm-1 bands compared to surrounding spectral regions | - | (hb p. 12) |
| Instrument back-end temperature drift between calibration cycles | Errors induced if ambient back-end temperature changes rapidly relative to the calibration cycle, since uncooled back-end optics are sensitive to thermal radiation including its own emission | High duty-cycle calibration with blackbody views every 3 minutes keeps this error negligible as long as ambient temperature changes slowly relative... | (hb p. 10) |
| Single event upsets, particularly on Version 4 systems | Recurring instrument upsets that can corrupt or degrade data; requires QC checks to catch | Perform quality control as outlined in section 2.2 | (hb p. 17) |
| High LW HBB NEN (longwave detector noise) | High values of LW HBB NEN indicate degraded data | Use LW HBB NEN parameter for basic QC screening | (hb p. 13) |
| High SW HBB NEN (shortwave detector noise) | High values of SW HBB NEN indicate degraded data | Use SW HBB NEN parameter for basic QC screening | (hb p. 13) |
| Low LW Responsivity | Low values indicate degraded longwave channel/detector sensitivity | Use LW Responsivity parameter for basic QC screening | (hb p. 13) |
| Low SW Responsivity | Low values indicate degraded shortwave channel/detector sensitivity | Use SW Responsivity parameter for basic QC screening | (hb p. 13) |
| Ancillary meteorological sensors not rigorously calibrated | Temperature, pressure, relative humidity, rain/sun sensor values may be diagnostically useful but not accurate enough for scientific analysis | Use nearby ARM MET sensors for calibrated ambient measurements instead | (hb p. 9) |
| AERIPROF retrieval discontinued | Older AERIPROF-derived profile products are no longer produced/updated | Use TROPoe (formerly AERIoe) instead, which has superseded AERIPROF | (hb p. 6) |
| TROPoe processing incomplete for all historical data | TROPoe VAP may not be available for a specific site/time period of interest | Contact the mentor if TROPoe retrievals are not available for a specific dataset | (hb p. 6) |
| Instrument/version differences in noise performance | Instrument noise properties may vary across different AERI units and versions (V1, V2, V4) deployed at a given site over time, visible as step changes in NEN/responsivity time series | Use instrumentUnitNumber parameter to identify instrument changes; radiometric uncertainties are otherwise uniform and constant across versions | (hb p. 15) |
| Fixed Resistor secular drift | Built-in Fixed Resistor values show a drift over time, indicating multimeter/electronics measurement path issues | Perform resistance validation and consider multimeter recalibration/swap | (hb p. 11) |
| Raw data retention limited on site VM | Only ~30 days of raw data stored on site VM before automatic deletion of oldest files | Raw AERI data needed for AERI QC must be obtained directly from the instrument or via special request from the ARM Archive | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Views of two accurately characterized and calibrated blackbodies (Hot Blackbody controlled to 333 K, Ambient Blackbody following ambient temperature) using the calibration equation of Revercomb et al. 1988; also 3rd blackbody calibration validation, resistance validation of multimeter/electronics path, multimeter... (hb p. 11) |
| Calibration interval | Operational: every 3 minutes (standard rapid sample mode). 3rd blackbody validation: once a year at fixed sites, and at start/end of mobile deployments, and before/after major configuration changes. Multimeter recalibration: every 1-2 years. Blackbody thermistor recalibration: every 3-5 years. (hb p. 11) |
| Traceability | Traceable to the original instrument certification, which is itself traceable to NIST standards. (hb p. 11) |
| Routine maintenance | Daily: physical inspection, software inspection (Ingest operational, FTSW housekeeping nominal). Monthly: replace outside air filter, replace desiccant as needed, inspect/clean/replace scene mirror as needed, clean rain sensors as needed. Yearly: replace inside air HEPA filter, replace laser as needed (typical... (hb p. 16) |
| Maintenance interval | Daily, monthly, yearly as detailed (hb p. 16) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ARM MET sensors, TROPoe (formerly AERIoe), AERIPROF (discontinued, superseded by TROPoe), Marine-AERI (M-AERI), Extended range AERI (ER-AERI).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ABB` | Ambient Blackbody |
| `AERI` | Atmospheric Emitted Radiance Interferometer |
| `AERI QC` | AERI quality control algorithm, part of AERI ARMORY |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `AWR` | AWARE AMF2 deployment |
| `DQR` | ARM Data Quality Report |
| `ER-AERI` | Extended range Atmospheric Emitted Radiance Interferometer |
| `FTS` | Fourier Transform Spectrometer |
| `FTSW` | GUI for AERI operating system |
| `GUI` | Graphical user interface |
| `HBB` | Hot blackbody |
| `M-AERI` | Marine-AERI |
| `NIST` | National Institute of Standards and Technology |


### References the handbook cites

- Knuteson, R.O., et al. 2004. 'Atmospheric Emitted Radiance Interferometer. Part I: Instrument Design.' Journal of Atmospheric and Oceanic Technology 21:1763-1776.
- Knuteson, R.O., et al. 2004. 'Atmospheric Emitted Radiance Interferometer. Part II: Instrument Performance.' Journal of Atmospheric and Oceanic Technology 21:1777-1789.
- Revercomb, H.E., et al. 1988. 'Radiometric Calibration of IR Fourier Transform Spectrometers: Solution to a Problem with the High-Resolution Interferometer Sounder.' Applied Optics 27(15):3210-3218.
- Brown, P.D., et al. 1995. 'Initial Analyses of Surface Spectral Radiance Between Observations and Line-by-Line Calculations.' Proceedings of the Fifth ARM Science Team Meeting.
- Minnett, P.J., et al. 2001. 'The Marine-Atmospheric Emitted Radiance Interferometer.' JAOT 18:994-1013.
- Turner, D. D., and U. Löhnert. 2014. 'Information content and uncertainties in thermodynamic profiles...' JAMC 53, 752-771.
- Turner, D. D. and W. G. Blumberg, 2018. 'Improvements to the AERIoe Thermodynamic Profile Retrieval Algorithm.' IEEE J-STARS 12, 1339-1354.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/aeri_handbook.pdf (22 pages, DOE/SC-ARM-TR-054, by J Gero, D Hackel)
- Catalog record: ARM data-source index, `instrument_class_code=aeri`, read 2026-09-23
- Example file: `sgpaerisummaryC1.b1.20260921.000405.nc` from `sgpaerisummaryC1.b1`, 13.48 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
