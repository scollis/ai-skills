---
name: arm-instrument-co-analyzer
description: ARM Carbon Monoxide Analyzer (co-analyzer) - handbook-derived instrument reference. Measurement principle, reported quantities (Carbon monoxide, Water vapor, Nitrous oxide, CO corrected for water vapor, N2O corrected for water vapor, Gas pressure in sample cell, Gas temperature in sample cell), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaoscoC1.b1) and the variable inventory of a real file. Use when working with co-analyzer data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Atmospheric Carbon. Triggers - co-analyzer, Carbon Monoxide Analyzer, enaaoscoC1.b1, Carbon monoxide, Water vapor, Nitrous oxide, CO corrected for water vapor, N2O corrected for water vapor, Gas pressure in sample cell, Aerosols, Atmospheric Carbon, Los Gatos Research (LGR).
---

# CO-ANALYZER - Carbon Monoxide Analyzer

The LGR CO/H2O/N2O Analyzer uses off-axis integrated cavity output spectroscopy to measure carbon monoxide, water vapor, and nitrous oxide mixing ratios in ambient air, permanently installed in ARM Aerosol Observing Systems and mobile facilities.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 25 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `co-analyzer` |
| Handbook | [DOE/SC-ARM-TR-159 / SR Springston, R Trojanowski, C Hayes / April 2025](https://www.arm.gov/publications/tech_reports/handbooks/co-analyzer_handbook.pdf) |
| Measurement category | Aerosols; Atmospheric Carbon |
| Manufacturer / model | Los Gatos Research (LGR); Model 907-0015 (AAF, AMF1, AMF3, ENA) and Model 098-0014 (AMF2) |
| Primary measurements | Atmospheric moisture; Carbon monoxide (CO) Concentration; Nitrogen oxides |
| Record | 2012-06-24 to 2026-09-23 (active) |
| Datastreams with data | 33 across 16 sites |
| Sites | anx, asi, bnf, cor, crg, dst, ena, epc, guc, hou, mao, mar, mos, oli |
| ARM page | https://www.arm.gov/capabilities/instruments/co-analyzer |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston, R Trojanowski, C Hayes** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston, R Trojanowski, C Hayes. *CO/H2O/N2O Analyzer Instrument Handbook*, DOE/SC-ARM-TR-159, April 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/co-analyzer_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Off-Axis ICOS utilizes a high-finesse optical cavity as an absorption cell, trapping laser photons so they make thousands of passes before leaving the cell, giving an effective optical path length of several thousand meters (e.g., 2500 meters for two 99.99% reflectivity mirrors spaced 25 cm apart). Because the path length depends on optical losses in the cavity rather than a unique beam trajectory, optical alignment is robust and reliable in the field, unlike conventional multi-pass cells or cavity-ring-down systems. The effective optical path length is determined by switching the laser off and measuring the time for light to leave the cavity (tens of microseconds). The laser wavelength is tuned over a selected absorption feature of the target species; measured absorption spectra combined with gas temperature, pressure, effective path length, and known line strength yield a quantitative mixing ratio directly without external calibration.

**Siting.** Permanently installed in shock-isolated 19-inch instrument rack within AOS systems; sample line plumbed into fast-flow ½-inch PFA trace gas manifold line with 47-mm PFA filter and filter holder; manifold line runs up the aerosol stack to under the 14-inch rain hat; deployed in ARM Aerial Facility (AAF), AMF1, AMF2, AMF3, and AOS at East North Atlantic (ENA).

**Sampling.** native rate 1 second (instrument frequency); reported every 1-second resolution, reported at beginning of period, average of all points less than or equal to the time and less than the next time; averaging CO_se/N2O_se/H2O_se etc. are standard deviation over averaging period; since data recorded at 1s instrument frequency, this error is 0 (hb p. 10).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Carbon monoxide (CO) | ppbv (raw datastream... | instrument will not operate below ~30... | ±2 ppbv or ±2%, whichever is greater;... | 1-second | (hb p. 10) |
| Water vapor (H2O) | ppmv | approximately less than 2000 to 5000... | not regularly calibrated against a water vapor... | 1-second | (hb p. 10) |
| Nitrous oxide (N2O) | ppbv (raw datastream... | varies very little in troposphere;... | ±2 ppbv or ±2%, whichever is greater;... | 1-second | (hb p. 10) |
| CO corrected for water vapor (CO_dry) | ppmv | - | includes combined imprecision of both analyte... | 1-second | (hb p. 5) |
| N2O corrected for water vapor (N2O_dry) | ppmv | - | includes combined imprecision of both analyte... | 1-second | (hb p. 5) |
| Gas pressure in sample cell (GasP) | torr | - | - | 1-second | (hb p. 5) |
| Gas temperature in sample cell (GasT) | C | - | - | 1-second | (hb p. 5) |
| Ambient/instrument interior temperature (AmbT) | C | - | - | 1-second | (hb p. 5) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | mixing volume of analyte, reported in parts per million by the instrument (raw); processed data in ppbv | (hb p. 11) |
| Range - CO | ambient CO never below ~50 to 60 ppbv; linearity better than 0.5% to 5 ppm and above; instrument will not operate below ~30 to 40 ppbv CO | (hb p. 12) |
| Range - N2O | varies very little in troposphere; linearity and range not an issue | (hb p. 12) |
| Range - H2O | approximately less than 2000 to 5000 ppm to saturated (non-condensing) | (hb p. 12) |
| Accuracy | ±2 ppbv or ±2% (whichever is greater) for CO and N2O; approaching ±1% under ideal circumstances | (hb p. 12) |
| Repeatability (1-sec noise, CO) | [CO] s = 0.05 ppbv | (hb p. 12) |
| Repeatability (1-sec noise, H2O) | [H2O] s = 150 ppmv | (hb p. 12) |
| Repeatability (1-sec noise, N2O) | [N2O] s = 0.08 ppbv | (hb p. 12) |
| 95% confidence interval CO | ± 0.1 ppbv | (hb p. 12) |
| 95% confidence interval H2O | ± 300 ppmv | (hb p. 12) |
| 95% confidence interval N2O | ± 0.2 ppbv | (hb p. 12) |
| Sensitivity - H2O bottoms out | below ~500 ppmv (arctic dry conditions) | (hb p. 12) |
| Zero-point y-intercept (lab tests, CO) | within ±0.2 to 0.3 ppbv | (hb p. 11) |
| AAF instrument final accuracy | within 1 to 2% (worst case) | (hb p. 11) |
| Optical cell effective path length (example) | 2500 meters (two 99.99% reflectivity mirrors spaced 25 cm) | (hb p. 15) |
| Flow calibration fluctuation | ~1% | (hb p. 11) |
| MAOS-C inlet calibration accuracy | uncertain to ±5 to 10% | (hb p. 13) |


## The data

Verified example: **`enaaoscoC1.b1`**, file `enaaoscoC1.b1.20260919.000000.nc`
(8.84 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=88135 |
| Data variables | 25 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:59 |
| sampling interval | 1 second |
| dod version | aosco-b1-2.4 |
| process version | ingest-aoscocorr-0.4-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `co` | ppmv | time | yes | Carbon monoxide (CO) mixing ratio calculated with nominal sensitivity... |
| `co_dry` | ppmv | time | yes | Carbon monoxide (CO) mixing ratio corrected for water vapor... |
| `h2o` | ppmv | time | yes | Water vapor mixing ratio calculated with nominal sensitivity... |
| `n2o` | ppmv | time | yes | Nitrous oxide (N2O) mixing ratio calculated with nominal sensitivity... |
| `n2o_dry` | ppmv | time | yes | Nitrous oxide (N2O) mixing ratio corrected for water vapor... |
| `ambient_temperature` | degC | time | - | Ambient temperature of instrument |
| `gas_pressure` | torr | time | - | Cell sample pressure |
| `gas_temperature` | degC | time | - | Cell sample temperature |
| `mass_flow_through_MFC_1` | cm^3/min | time | - | Actual mass flow through mass flow controller 1 |
| `mass_flow_through_MFC_2` | cm^3/min | time | - | Actual mass flow through mass flow controller 2 |
| `seconds_after_calibration` | s | time | - | Seconds after last calibration |
| `set_point_for_MFC_1` | cm^3/min | time | - | Set point for mass flow controller 1 |
| `set_point_for_MFC_2` | cm^3/min | time | - | Set point for mass flow controller 2 |
| `time` | - | time | - | Time offset from midnight |
| `valve_position_MFC_1` | unitless | time | - | Valve position for mass flow controller 1 |
| `valve_position_MFC_2` | unitless | time | - | Valve position mass flow controller 2 |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

The `act-arm-live` and `act-qc` skills wrap these calls in shorter helpers
(`armlive_open`, `armlive_list_files`, `act_qc_table`, `act_qc_apply`). Those are helpers
those skills define, **not** ACT functions - nothing below uses them, so every block here
runs against a bare `act-atmos` install.

```python
import os, requests, act

user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]

# ACT has no list-only call, so size the request against ARM Live's query endpoint
# before transferring anything.
avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f"{user}:{token}", "ds": "enaaoscoC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enaaoscoC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enaaoscoC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enaaoscoC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("h2o", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
25 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_co"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("co", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["co", "n2o", "h2o"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (enaaoscoC1.b1.20260919.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `co` | seconds_after_calibration less than ... | 275 | 0.312 |
| `n2o` | seconds_after_calibration less than ... | 275 | 0.312 |
| `h2o` | seconds_after_calibration less than ... | 275 | 0.312 |
| `co_dry` | seconds_after_calibration less than ... | 275 | 0.312 |
| `n2o_dry` | seconds_after_calibration less than ... | 275 | 0.312 |
| `co` | valve_position_MFC_1 = 0 or valve_position_MFC_2 = 0,... | 184 | 0.2088 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("enaaoscoC1.b1", "20120624", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: First level of QC is automatic flagging of data when chamber pressure deviates greater than 5 mb from nominal. Second level is inspection of daily standard addition and weekly replacement gas calibrations; standard addition responses nominally within ~10% of expected value (deviations from drift), weekly replacement calibration usually within 1-2% of nominal. Comparison of AAF CO instrument with post-program flask samples indicates accuracy for CO and N2O better than 5% of nominal; final accuracy of aircraft instrument judged within 1-2% (worst case). At "a" level processing, data quality...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Instrument cannot measure true zero concentration | Reports missing value of -999 when sample is scrubbed of CO, N2O, or H2O and instrument loses spectroscopic lock on absorbance line | Not an issue for ambient measurements since these analytes never reach zero in ambient air except arctic H2O; vendor claims zero determined by... | (hb p. 21) |
| Instrument will not operate below ~30-40 ppbv CO | No valid CO reading below this threshold; blind range at low concentrations | Manufacturer considers this a first-principles measurement for zero point; not an issue for ambient air which never reaches this low | (hb p. 11) |
| H2O 'bottoms out' under arctic dry conditions | H2O readings unreliable/invalid below ~500 ppmv | None stated beyond noting it as exception for arctic sampling | (hb p. 18) |
| Standard addition calibration accuracy affected by flow rate drift | Standard addition response deviates from 1, nominally within ~10% of expected value | Deviations explained by gradual drift of instrument flow rate or MFC calibrations; weekly replacement gas calibration is more precise (independent of... | (hb p. 11) |
| Chamber pressure deviation flagging | Data automatically flagged when chamber pressure deviates greater than 5 mb from nominal | First level of automatic data quality flagging | (hb p. 11) |
| Uncalibrated MFC flow readouts | Flow 1 read/Flow 2 read fields are raw uncalibrated MFC output | True flow computed as a + Flow_read * b using intercept/slope from configuration file calibration | (hb p. 6) |
| Calibration/standard addition periods not removed from data | MFC_1 and MFC_2 fields indicate when a standard addition or displacement calibration occurs within the datastream | No standard additions or displacement calibrations are removed from the data streams; users should be aware of this when analyzing data | (hb p. 7) |
| Non-standardized output channels across instrument generations | Unused channels (Gnd, LTCO, AIN5, AIN6, AIN7) appear in raw data with no meaning; LGR modified outputs across models | None; documentation complicated, standardization impossible | (hb p. 6) |
| Clock/timing dithering | Minor irregularities in output datastream timing because neither instrument clock nor instrument computer clock are perfect | Processing must handle more than one record per second and periods with no data or only timestamp | (hb p. 7) |
| Missing/empty data records | Instrument computer may output empty-field records if instrument does not produce a number | Processing must accommodate these; all non-operational periods removed as empty field or NAN in processed data | (hb p. 7) |
| Water vapor not a primary calibrated measurement | H2O values not regularly checked against a calibration standard | Lab tests against dew-point hygrometer show excellent correspondence, used as indirect validation | (hb p. 11) |
| Uncertain nominal response calibration on AAF instrument | Nominal instrument response questioned as being 5% off in comparisons with flask samples | Final accuracy judged within 1-2% worst case after adjustment | (hb p. 11) |
| MAOS-C calibration uncertainty | Standard addition to hi-flow PFA inlet depends on rotometer-measured flow, less accurate | Accuracy uncertain to ±5 to 10%; planned upgrade to system similar to ENA | (hb p. 13) |
| Dry air (H2O-corrected) mixing ratio not typically reported | co_dry/n2o_dry fields present but generally not reported/used | Because it includes combined imprecision of both the analyte and water measurements | (hb p. 11) |
| Displacement calibration cannot account for ambient air matrix effects | Weekly displacement calibration reading differs slightly from standard addition, though calibrations agree to within less than 2 to 5% | None specific; noted as limitation of the displacement method | (hb p. 13) |
| Security risk of instrument's Linux operating system | Ethernet connection possible but underlying OS does not support modern updates | None stated beyond noting risk; direct Ethernet communication avoided/limited | (hb p. 3) |
| Zero test not repeatable across units | One unit tested showed zero within ±0.5 ppbv, but not reproducible across other LGR analyzers | None; noted as limitation of lab testing | (hb p. 21) |
| Class IIIb laser hazard | N/A to data, but instrument must not be operated with cover off | Do not operate with cover off; see LGR manual laser safety warning | (hb p. 18) |
| Filter contamination/clogging | Visible dark circle of trapped dirt on removed filter indicates inadequate filter change frequency | Change filter every two weeks; increase frequency and notify mentor if dirt circle visibly dark; use white filter, not blue spacer | (hb p. 17) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Daily standard addition (~10-20 sccm via MFC, or ~40 sccm ~100 ppmv CO at MAOS-C) and weekly 1 SLPM replacement/displacement calibration using shared mixed gas standard; span check daily 30 seconds after midnight UTC for three minutes, weekly displacement calibration 10 minutes after midnight UTC for three minutes;... (hb p. 16) |
| Calibration interval | Daily standard addition; weekly (7-day) replacement/displacement calibration; instrument and MFC flow rates calibrated prior to campaign and on 6-month to 1-year schedule (hb p. 16) |
| Traceability | NIST-traceable commercial standards or shared CO/N2O standard from Sebastien Biraud of LBNL; flows measured by Gilibrator (calibrated against primary standard soap-bubble flow meter) or Defender Dry Gas Calibrator (calibrated annually against primary standard soap-bubble flow meter at Brookhaven National Laboratory) (hb p. 16) |
| Routine maintenance | Change inlet particle filter (47-mm diam. 5-µm PFA membrane filter Type LS, Millipore Catalog # LSWPO4700); use white filter not blue spacer; inspect old filter for dirt buildup and increase change frequency/notify mentor if dark (hb p. 17) |
| Maintenance interval | every two weeks (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Picarro CO2/CH4 instrument (Greenhouse Gas Analyzer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AMF` | ARM Mobile Facility |
| `AMF1` | first ARM Mobile Facility |
| `AMF2` | second ARM Mobile Facility |
| `AMF3` | third ARM Mobile Facility |
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `CO` | carbon monoxide |
| `ENA` | East North Atlantic |
| `GUI` | graphical user interface |
| `H2O` | water |
| `ICOS` | integrated cavity output spectroscopy |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `LGR` | Los Gatos Research |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/co-analyzer_handbook.pdf (25 pages, DOE/SC-ARM-TR-159, by SR Springston, R Trojanowski, C Hayes)
- Catalog record: ARM data-source index, `instrument_class_code=co-analyzer`, read 2026-09-23
- Example file: `enaaoscoC1.b1.20260919.000000.nc` from `enaaoscoC1.b1`, 8.84 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
