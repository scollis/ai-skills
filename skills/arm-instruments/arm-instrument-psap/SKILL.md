---
name: arm-instrument-psap
description: ARM Particle Soot Absorption Photometer (psap) - handbook-derived instrument reference. Measurement principle, reported quantities (Optical absorbance of aerosols, Filter transmittance, Dark current, Instrument mass flow), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (pvcaospsap3wM1.c1) and the variable inventory of a real file. Use when working with psap data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - psap, Particle Soot Absorption Photometer, pvcaospsap3wM1.c1, Optical absorbance of aerosols, Filter transmittance, Dark current, Instrument mass flow, Aerosols, Radiance Research, 3-λ Particle Soot Absorption Photometer (PSAP), CAPS, EPROM, HEPA, MAOS.
---

# PSAP - Particle Soot Absorption Photometer

The PSAP determines the optical extinction coefficient for absorption at three wavelengths by measuring the change in light transmittance through a filter as ambient particles are deposited on it, deployed within ARM Aerosol Observing System (AOS) racks at fixed and mobile ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `psap` |
| Handbook | [DOE/SC-ARM-TR-176 / SR Springston, R Trojanowski, C Hayes, C Flynn / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/psap_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Radiance Research, 3-λ Particle Soot Absorption Photometer (PSAP) |
| Primary measurements | Aerosol absorption |
| Record | 2010-09-20 to 2026-09-23 (active) |
| Datastreams with data | 98 across 23 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, mag, mao |
| ARM page | https://www.arm.gov/capabilities/instruments/psap |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston, R Trojanowski, C Hayes, C Flynn** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston, R Trojanowski, C Hayes, C Flynn. *Particle Soot Absorption Photometer (PSAP) Instrument Handbook*, DOE/SC-ARM-TR-176, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/psap_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The PSAP technique measures the particle absorption coefficient (σAP) as a function of the decrease in filter transmittance (Tr) over time as particles accumulate on a glass/cellulose (Emfab) filter, using Beer's law with the simplification that the change in Tr over the averaging interval Δt is much less than 1. Filter transmittance is calculated from the ratio of the summed signal and reference detector outputs, normalized to the value of a new filter; the reference channel uses an identical filter exposed to the same aerosol-free air to remove common-mode noise such as humidity. A single three-LED assembly illuminates both the sample and reference filters simultaneously, alternating between three nominal wavelengths (470, 522, 660 nm, though actual measured wavelengths differ slightly). The absorption coefficient is calculated from Beer's law using Tr, the flow rate through the optical cell, and the area of the deposited particle spot on the filter; an experimentally determined transfer function (Fr) corrects transmittance to the actual transmittance of the sampled air column.

**Siting.** Deployed within ARM Aerosol Observing System (AOS) racks at AMF1 (formerly MAOS-A), AMF2, AMF3, ENA, SGP, and other mobile campaign AOS sites; an earlier PSAP version is operated on the ARM Aerial Facility. Air is sampled from the AOS high-flow aerosol inlet through a 1-/10-µm impactor and a PermaPure Nafion drier upstream of the instrument (using counterflow of PSAP exhaust at low pressure); the heater shown in the flow schematic is NOT used in AOS sampling because of drier effectiveness. The impactor output is shared with nephelometers and, where present, CAPS and PASS3 systems on a switching schedule coordinated with other ARM instruments.

**Sampling.** native rate 1-second (native resolution); reported every 1-minute (aospsap3w1m.b1) and 1-hour (aoppsap1h.c1) final products; averaging Springston-Sedlacek sliding boxcar average with a 60-second fullwidth applied to 1-s data (aospsap3w1s.b1); a final 60-second average yields aospsap3w1m.b1 (hb p. 5).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Optical absorbance of aerosols (absorption coefficient, σAP) | Mm-1 (reciprocal megameters) | 0-50 Mm-1 in non-urban locations (can... | ill-defined absent a true reference absorbance... | - | (hb p. 15) |
| Filter transmittance (Tr) | ratio (dimensionless) | 1.0 (new filter) down to less than 0.7... | - | - | (hb p. 8) |
| Light intensity at three wavelengths (sample and reference) | 20-bit resolution counts | - | - | 20-bit, 1-s resolution | (hb p. 11) |
| Dark current (sample and reference light paths) | - | - | - | 1-s resolution | (hb p. 11) |
| Instrument mass flow | slpm | nominal 1.0 slpm | 1.000 ± 0.001 slpm (with modified micrometer... | - | (hb p. 11) |
| Dilution MFC set point and read point | slpm | 0-2 slpm | - | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | reciprocal megameters (Mm-1) | (hb p. 15) |
| Range | 0-50 Mm-1 in non-urban locations; higher during biomass burn or local contamination | (hb p. 15) |
| Accuracy | not generally agreed on in the community; scattering correction can be up to 50% of original PSAP measurement for high single-scattering albedo... | (hb p. 15) |
| Repeatability (Precision) | Absorbance σ ~ 0.1 Mm-1 without dilution for 60-s averaged intensity data | (hb p. 15) |
| Repeatability with dilution | 0.5 dilution factor increases standard deviation of signal by ~2-3X | (hb p. 16) |
| Sensitivity | 3 X σ or 0.3 Mm-1 for 60-s averaging of intensities, no dilution | (hb p. 16) |
| Uncertainty | ill-defined; combined measure of accuracy and precision, absent true reference absorbance measurement | (hb p. 16) |
| Nominal flow rate | 1.0 slpm | (hb p. 10) |
| Modified flow rate precision | 1.000 ± 0.001 slpm | (hb p. 11) |
| Dilution MFC range | 0-2 slpm | (hb p. 11) |
| Filter change threshold | Tr less than  0.7 | (hb p. 8) |
| LED nominal wavelengths | 470, 522, and 660 nm | (hb p. 10) |
| EPROM version | 2.03 | (hb p. 11) |
| Detector resolution | full 20-bit resolution measurement at 1-s resolution | (hb p. 11) |


## The data

Verified example: **`pvcaospsap3wM1.c1`**, file `pvcaospsap3wM1.c1.20130621.000000.cdf`
(0.13 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 21 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2013-06-21T00:00:00 to 2013-06-21T23:59:00 |
| sampling interval | variable, contact mentor for details |
| averaging interval | 1 minute |
| dod version | aospsap3w-c1-1.3 |
| process version | ingest-aosmqc-1.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Ba_B_PSAP3W` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue wavelength at dry... |
| `Ba_G_PSAP3W` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green wavelength at dry... |
| `Ba_R_PSAP3W` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red wavelength at dry... |
| `impactor_setting` | um | time | yes | Impactor setting in terms of aerodynamic diameter cut off |
| `sample_length` | m | time | yes | AOS PSAP3W (NOAA) sample length, needed to calculate Beers Law |
| `transmittance_B` | unitless | time | yes | AOS PSAP3W transmittance, blue channel |
| `transmittance_G` | unitless | time | yes | AOS PSAP3W transmittance, green channel |
| `transmittance_R` | unitless | time | yes | AOS PSAP3W transmittance, red channel |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "pvcaospsap3wM1.c1",
                             "start": "2013-06-21", "end": "2013-06-21", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./pvcaospsap3wM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "pvcaospsap3wM1.c1", "2013-06-21", "2013-06-21")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("pvcaospsap3wM1.c1", "2013-06-21", "2013-06-21"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("Ba_B_PSAP3W", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

8 `qc_` companion variables cover 8 of the
21 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_Ba_B_PSAP3W"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("Ba_B_PSAP3W", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["Ba_B_PSAP3W", "Ba_G_PSAP3W", "Ba_R_PSAP3W"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (pvcaospsap3wM1.c1.20130621.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ba_B_PSAP3W` | Value is equal to missing_value. | 428 | 29.7222 |
| `Ba_G_PSAP3W` | Value is equal to missing_value. | 428 | 29.7222 |
| `Ba_R_PSAP3W` | Value is equal to missing_value. | 428 | 29.7222 |
| `Ba_R_PSAP3W` | Ba_R_PSAP3W less than  absorption_minimum_warning | 1 | 0.0694 |
| `transmittance_B` | Value is greater than the fail_max. | 1 | 0.0694 |
| `transmittance_G` | Value is greater than the fail_max. | 1 | 0.0694 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("pvcaospsap3wM1.c1", "20100920", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: First level of data quality is automatic flagging when transmittance decreases below 0.7, pumps are off, or filters are being changed; most events identified algorithmically but not all. Final level of data quality is visual inspection of plots for wild excursions (ringing) caused by momentary (~1s) intensity changes, which are obvious due to their symmetrical nature about zero; these occur near filter changes and power failures/resumptions. Automatic processing has conservative (wide) invalid-data bands around such events, but excursions can occur outside even these wide bands due to line...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Filter loading effect / departure from Beer's law | Nonlinear response and drift in absorbance as filter transmittance decreases; flagged when Tr not within bounds (1 to 0.7) | Filter changed when Tr less than  0.7; Weiss filter-loading correction applied in processing | (hb p. 6) |
| Scattering contamination of absorption signal (extinction vs absorption) | PSAP measures extinction (absorption + scattering); for high single-scattering-albedo aerosols, scattering can be up to 50% of the original PSAP measurement | Bond/Sheridan/Ogren and Virkkula corrections using co-located nephelometry data applied in AOP VAP processing | (hb p. 15) |
| Artificial AAE (absorption Angström exponent) dependence on filter transmittance | Both Bond/Sheridan/Ogren and Virkkula correction approaches individually show an artificial dependence of AAE on transmittance | AOP process takes arithmetic mean of the two corrections (similar magnitude, opposite sign) to yield negligible AAE dependence on transmittance | (hb p. 6) |
| Filter media discontinuation / change (PALL E70-2075W to Pallflex Emfab) | Step change or discontinuity in correction factors/data around filter change dates per site | Emfab (TX40HI20-WW) selected as best replacement; correction factors recalibrated; changeover dates documented per site (e.g., AOS07-SGP March 1... | (hb p. 9) |
| Flow excursions during filter changes | Instrument flow spikes greater than greater than  1.0 slpm during filter changes when filter holder is opened | Periods flagged as not valid | (hb p. 6) |
| Power failures/interruptions | Pump off periods visible as flow drop to zero, usually due to site power failures; ~5-min period around each interruption flagged | Instrument backed up with UPS; data flagged as not valid around interruptions | (hb p. 6) |
| Impactor malfunction | Absence of normal ±0.03 slpm fine-structure oscillation in instrument flow indicative of impactor switching state; visible as anomalous flat flow over multi-day periods (e.g., two-day... | Can be algorithmically flagged | (hb p. 6) |
| Dilution air source failure (Pentras Drier failure) | Gaps in dilution flow trace | Dilution factor automatically set to 1 (no dilution) if dilution flow not functioning | (hb p. 6) |
| Momentary signal excursions/ringing | Wild excursions (~1 s) in intensity, symmetrical about zero, occurring near/just after filter changes and accompanying power failures/resumptions | Conservative wide flagging bands around these events; mentor judgment used for excursions outside the automatic bands | (hb p. 8) |
| Line voltage instability / HVAC excursions / undocumented inlet changes | Excursions in data outside normal automatic flagging bands | Mentor judgment exercised in identifying and flagging these periods | (hb p. 8) |
| Native 1-second data noise | Absorption values quite noisy at native 1-s resolution before boxcar averaging | 60-second sliding boxcar average (Springston-Sedlacek) applied to improve signal-to-noise ratio | (hb p. 5) |
| Dilution increases measurement noise | Standard deviation of signal increases ~2-3X with 0.5 dilution factor; additional uncertainty from drift in dilution MFC calibration | none stated beyond noting the effect | (hb p. 16) |
| Local contamination from on-site generator or biomass burning | Absorbance values much higher than typical 0-50 Mm-1 non-urban range | none stated | (hb p. 15) |
| No absolute calibration standard for absorbance | Uncertainty is ill-defined; no way to independently verify accuracy against a reference | Treated as first-principles measurement; flow, spot size, and dilution rates calibrated instead | (hb p. 8) |
| Garbled display after storage/transport | PSAP display comes up garbled after extended storage or transportation | Reseating of all internal boards is the best remedy | (hb p. 19) |
| Local interference from transportation | Visible spike/interference in GUI time series plot (e.g., evident at 15:10 in example) | none stated beyond visual identification via GUI | (hb p. 14) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | No effective way to calibrate PSAP using a realistic absorbance standard; absorbance is considered a first-principles measurement. Spot size measured upon receipt of instrument. Flow calibrated using a first-principles bubble flowmeter (with corrections for temperature, pressure, and water vapor concentration) or a... (hb p. 14) |
| Calibration interval | Flows calibrated at the beginning of each deployment and generally at 6-12 month intervals in the field; MFM calibrated annually or more frequently if circumstances change; MFC calibrations performed during mentor visits. (hb p. 14) |
| Traceability | First-principles bubble flowmeter or dry gas meter standardized against the bubble flowmeter (hb p. 14) |
| Routine maintenance | Filter changes (sample and reference) performed when blue transmittance decreases below 0.7; after filter change, transmittance is reset to 1.00 and flow adjusted to nominal 1.00 slpm. Procedure given in AOS Operating Procedures. (hb p. 21) |
| Maintenance interval | As needed, when Tr less than  0.7 (varies with aerosol loading) (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: nephelometer, cloud aerosol and precipitation spectrometer (CAPS), three-wavelength photoacoustic soot spectrometer (PASS3).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAE` | absorption Angström exponent |
| `AMF` | ARM Mobile Facility |
| `AOP` | Aerosol Optical Properties |
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `CAPS` | cloud aerosol and precipitation spectrometer |
| `EPROM` | erasable programmable read-only memory |
| `HEPA` | high-efficiency particulate air |
| `LED` | light-emitting diodes |
| `MAOS` | Mobile Aerosol Observing System |
| `MFC` | mass flow controller |
| `MFM` | mass flow meter |
| `PASS3` | three-wavelength photoacoustic soot spectrometer |
| `PSAP` | particle soot absorption photometer |


### References the handbook cites

- Schmid et al. 2006
- Virkkula et al. 2005
- Anderson et al. 2003
- Anderson et al. 1999
- Bond et al. 1999
- Springston, SR, and AJ Sedlacek. 2007. Noise characteristics of an instrumental particle absorbance technique
- Springston, S. 2019. Filter Aerosol Measurements for ARM

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/psap_handbook.pdf (22 pages, DOE/SC-ARM-TR-176, by SR Springston, R Trojanowski, C Hayes, C Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=psap`, read 2026-09-23
- Example file: `pvcaospsap3wM1.c1.20130621.000000.cdf` from `pvcaospsap3wM1.c1`, 0.13 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
