---
name: arm-instrument-irt
description: ARM Infrared Thermometer (irt) - handbook-derived instrument reference. Measurement principle, reported quantities (Sky infrared temperature, Surface infrared temperature, Overall reported measuring range), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpirt25mC1.b1) and the variable inventory of a real file. Use when working with irt data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric; Surface/Subsurface Properties. Triggers - irt, Infrared Thermometer, sgpirt25mC1.b1, Sky infrared temperature, Surface infrared temperature, Overall reported measuring range, Radiometric, Surface/Subsurface Properties, vendor Wintronics, AERI, ASTM, GNDRAD, IRTSST.
---

# IRT - Infrared Thermometer

The IRT is a ground-based radiation pyrometer deployed downwelling (narrow field of view) to measure sky/cloud-base brightness temperature and upwelling (wide field of view) to measure ground-surface brightness temperature, reported as equivalent blackbody temperature in Kelvins.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 31 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `irt` |
| Handbook | [VR Morris](https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf) |
| Measurement category | Radiometric; Surface/Subsurface Properties |
| Manufacturer / model | Heitronics GmbH KT19.85 Infrared Radiation Pyrometer (Type I and Type II); vendor Wintronics, Inc. |
| Primary measurements | Longwave broadband upwelling irradiance; Longwave narrowband brightness temperature; Surface skin temperature |
| Record | 1996-04-16 to 2026-09-23 (active) |
| Datastreams with data | 148 across 24 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, grw, guc, hou, kcg |
| ARM page | https://www.arm.gov/capabilities/instruments/irt |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Infrared Thermometer (IRT) Instrument Handbook*.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Temperature radiation emitted by all objects above absolute zero is sensed by the IRT's infrared detector; a radiation thermometer measures the radiance power from the target area, which by Planck's law is related to temperature given the known relative spectral response of the optical system and detector. The output signal of a linear detector is proportional to measured radiance, so the indicating meter can be calibrated in temperature units (Kelvins). The KT19.85 uses an optical chopper that periodically interrupts incident radiation from the target, exposing the detector alternately to the target and to an internal blackbody reference source of defined temperature; because pyroelectric detectors respond to radiation differences rather than absolute intensities, this "chopped radiation" method eliminates thermal drift of the housing and provides a modulated signal at a precise frequency. Each IRT's individual characteristics (filters, detector sensitivity, lenses) are compensated by comparing instrument readings against blackbody radiation at several temperatures and adjusting the linearization/calibration factor.

**Siting.** The downwelling IRT is mounted at a height of 1-2 m above the ground inside a ventilated enclosure (Hoffman CSD16126SS6), oriented so the zenith view of the sky is reflected into the lens by a protected gold mirror (Edmund Optics 45-617). The upwelling IRT is mounted at a height of 2-25 m above the ground inside a small enclosure, oriented so the mounting platform is not in the field of view and to ensure the ground and vegetation cover are representative of the local area.

**Sampling.** native rate 5-Hz instantaneous (irt200ms); 1-sec instantaneous (irtsst); reported every irt200ms: 5 Hz (0.2 s); irt/gndirt/irt10m/irt25m: 1-min averaged; irtsst: 1 sec instantaneous; averaging 1-minute averaging for irt, gndirt, irt10m, irt25m datastreams (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sky infrared temperature (sky_ir_temp) | K | - | - | - | (hb p. 12) |
| Surface infrared temperature (sfc_ir_temp) | K | - | - | - | (hb p. 12) |
| Internal reference infrared temperature (ref_ir_temp) | K | - | - | - | (hb p. 12) |
| Temperature Measuring Range - Type I (SNless than 2000) | K | 213 to 673 K | ±0.5 K + 0.7% of temperature difference | ±1.10 K at 223 K; ±0.45 K... | (hb p. 20) |
| Temperature Measuring Range - Type II | K | 173 to 473 K | ±0.5 K + 0.7% of temperature difference | ±1.85 K at 223 K; ±0.70 K... | (hb p. 20) |
| Overall reported measuring range | K | 173 to 473 K | - | - | (hb p. 21) |


## Specifications

| parameter | value | source |
|---|---|---|
| Spectral Sensitivity | 9.6 to 11.5 µm (both Type I and Type II) | (hb p. 20) |
| Temperature Measuring Range (Type I, SNless than 2000) | 213 to 673 K | (hb p. 20) |
| Temperature Measuring Range (Type II) | 173 to 473 K | (hb p. 20) |
| Temperature Resolution (Type I, emissivity=1) | ±1.10 K at 223 K; ±0.45 K at 293 K (response time = 1.0 s) | (hb p. 20) |
| Temperature Resolution (Type II, emissivity=1) | ±1.85 K at 223 K; ±0.70 K at 293 K (response time = 0.1 s) | (hb p. 20) |
| Accuracy | ±0.5 K + 0.7% of temperature difference (both types) | (hb p. 20) |
| Operational Ambient Temperature (Type I) | 0° to 60°C | (hb p. 20) |
| Operational Ambient Temperature (Type II) | -20° to +60°C | (hb p. 20) |
| Storage Temperature | -20° to +70°C (both types) | (hb p. 20) |
| Weight (Type I) | 1.5 kg | (hb p. 20) |
| Weight (Type II) | 2.4 kg | (hb p. 20) |
| Analog Output Resolution | 12 bit (both types) | (hb p. 20) |
| Optical Field of View (at 3 m) - downwelling (S921 lens,... | 2.64° | (hb p. 20) |
| Optical Field of View (at 3 m) - upwelling (M6 lens,... | 30.51° | (hb p. 20) |
| Operating Voltages | 24 V AC (±10%) at 48 to 400 Hz or 26 V DC (±15%) (both types) | (hb p. 20) |
| Current Consumption | 80 mA (both types) | (hb p. 20) |
| Target emissivity (EMI) - Downwelling | 0.987 | (hb p. 24) |
| Target emissivity (EMI) - Upwelling | 1.000 | (hb p. 24) |
| Temperature span (ANALOG) - Downwelling | 173-303 K | (hb p. 24) |
| Temperature span (ANALOG) - Upwelling | 223-323 K | (hb p. 24) |
| Analog output (ANALOG) | 0-1 volt (both) | (hb p. 24) |
| Digital output (COM) | 9.6Kb/8NP/1S/LF (both) | (hb p. 24) |
| Response time (RESP) - Downwelling | 0.3 second | (hb p. 24) |
| Response time (RESP) - Upwelling | 3.0 seconds | (hb p. 24) |


## The data

Verified example: **`sgpirt25mC1.b1`**, file `sgpirt25mC1.b1.20260919.000000.nc`
(0.14 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 21 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| dod version | irt25m-b1-4.0 |
| process version | ingest-irt25m-1.1-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `logger_libat` | V | time | yes | Internal datalogger Lithium battery voltage |
| `logger_temp` | degC | time | yes | Logger temperature |
| `logger_volt` | V | time | yes | Logger voltage |
| `ref_ir_temp` | K | time | yes | Internal reference temperature |
| `sfc_ir_temp` | K | time | yes | Surface infrared temperature |
| `sfc_ir_temp_max` | K | time | yes | Surface infrared temperature, maxima |
| `sfc_ir_temp_min` | K | time | yes | Surface infrared temperature, minimum |
| `sfc_ir_temp_std` | K | time | - | Surface infrared temperature, standard deviation |
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
                     params={"user": f"{user}:{token}", "ds": "sgpirt25mC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpirt25mC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpirt25mC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpirt25mC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("sfc_ir_temp", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

7 `qc_` companion variables cover 7 of the
21 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_sfc_ir_temp"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("sfc_ir_temp", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["sfc_ir_temp", "sfc_ir_temp_max", "sfc_ir_temp_min"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpirt25mC1.b1", "19960416", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Most datastream fields contain a corresponding sample-by-sample automated quality check field in the b1-level datastreams named qc_less than fieldnamegreater than  (e.g., qc_sky_ir_temp). Flags range from 0 (all QC checks passed) to combinations of missing-data, minimum, maximum, and delta-check failures (values 1-15 per Table 7). Minimum/maximum/delta thresholds differ for downwelling (sky_ir_temp: 173-303 K, delta 50 K; ref_ir_temp: 253-333 K, delta 10 K) versus upwelling (sfc_ir_temp: 223-323 K, delta 50 K; ref_ir_temp: 253-333 K, delta 10 K) datastreams. A qc_time field also flags...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Positive spikes from cleaning | Positive spikes in sky temperature measurements coincide with daily preventative maintenance times, caused by water and/or alcohol used to clean the gold mirror | - | (hb p. 20) |
| Solar intrusion spikes near local solar noon | Positive spikes in sky temperature measurements near local solar noon, especially at tropical sites near equinoxes, due to sun entering the IRT field of view | - | (hb p. 20) |
| Warm bias of upwelling IRT vs PIR on towers | Upwelling IRT reads warmer than PIR at sites where instrument is mounted 10 m above ground, especially in summer/daytime; bias shrinks at night or during rain/overcast (low solar); e.g., at... | - | (hb p. 20) |
| Negative bias of sky temperature vs MWRP/MWR3C | Downwelling IRT reads a negative bias relative to MWRP and MWR3C of roughly ~10°C, attributed to differing fields of view (IRT 2.6° vs MWRP/MWR3C 30°) | - | (hb p. 20) |
| Positive bias vs AERI in very cold/clear/dry conditions | Downwelling IRT reads warmer than AERI during clear-sky conditions when sky temperature is less than ~180K; greatest when sky is very clear, dry, cold and ambient is hot, especially if... | - | (hb p. 20) |
| Internal reference temperature below measurable minimum in winter at AMF3 | Internal reference temperature of downwelling and upwelling IRTs at AMF3 (OLI/M1) in winter is frequently less than the minimum measurable value of -20°C | - | (hb p. 20) |
| Data acquisition system migration | Discontinuity/change in datastream provenance: signals moved from SKYRAD/GNDRAD datalogger to a dedicated data acquisition system (ENG0000990) at AMF2 on 5/25/2017 and at ENA/C1 on 6/5/2017 | - | (hb p. 20) |
| Type I to Type II instrument upgrades | Step changes in calibration factor/specifications at specific sites and dates when Type I units were replaced with Type II (BCR-1958) at SGP/C1 10m 9/17/2013, 25m 9/19/2013, TWP/C3... | - | (hb p. 20) |
| Mounting configuration changes for SKYRAD IRT | Enclosure/mirror hardware change (Radiometrics MP3965/MP3964 with Edmund 32-089 mirror to Hoffman CSD16126SS6 enclosure with Edmund 45-617 mirror) at various sites/dates could shift... | - | (hb p. 21) |
| Extended-range IRT swap at SGP/CF1 | Downwelling IRT at SGP/CF1 replaced with extended-range IRT (ECO-345, BCR-1131) at SGP/E13 on 1/4/2006, causing a step change in range/behavior | - | (hb p. 21) |
| Datastream lineage changes for surface temperature at SGP | sfc_ir_temp historically appears under different datastream names over time (sgpmfr10mC1.a1/sgpmfr25mC1.a1 pre-2001, sgpmfrirt10mC1.a1/sgpmfrirt25mC1.a1 2001, sgpirt10mC1.a1/sgpirt25mC1.a1... | - | (hb p. 22) |
| Calibration factor drift/repairs over instrument lifetime | Calibration factor values change over time for individual serial numbers following repairs (see Calibration history Table 12), so applying a single static calibration factor across the full... | Consult calibration history table for date-specific calibration factor per serial number | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Factory: blackbody calibration source test at 80-100°C per ASTM E1256-88 Standard Test Methods for Radiation Thermometers (Single Waveband Type); calibration factor adjusted via device menu until display matches blackbody temperature. Mentor method: collocate IRT with AERI, compute narrowband radiance LIRT =... (hb p. 9) |
| Calibration interval | Documented in calibration history table (Table 12), varies by unit - recalibrations/checks occurring irregularly, e.g. after repairs, periodic BB checks, and AERI comparisons (hb p. 9) |
| Traceability | ASTM E1256-88; referenced to AERI (cryogenically cooled spectrometer) rather than absolute blackbody due to ASTM blackbody being far outside sky-temperature range (hb p. 9) |
| Routine maintenance | Fine dust removed from lens with compressed air or a fine lens brush; heavily soiled or greasy lens cleaned with paper tissues, cotton swabs, and lens-cleaning solution (alcohol or water can also be used). See Corrective Maintenance Reporting. (hb p. 19) |
| Maintenance interval | Daily preventative maintenance (implied by note about daily cleaning causing spikes) (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AERI (atmospheric emitted radiance interferometer), PIR (precision infrared radiometer), MWRP (microwave radiometer profiler), MWR3C (microwave radiometer, 3 channel), MWR (microwave radiometer), SKYRAD, GNDRAD.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AERI` | atmospheric emitted radiance interferometer |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `ASTM` | American Society for Testing and Materials |
| `DOE` | U.S. Department of Energy |
| `ENA` | Eastern North Atlantic |
| `GNDRAD` | ground radiometers on stand for upwelling radiation |
| `IRT` | infrared thermometer |
| `IRTSST` | infrared thermometer for sea-surface temperature |
| `MWR` | microwave radiometer |
| `MWRP` | microwave radiometer profiler |
| `MWR3C` | microwave radiometer, 3 channel |
| `NSA` | North Slope of Alaska |


### References the handbook cites

- ASTM E1256-88, Standard Test Methods for Radiation Thermometers (Single Waveband Type)
- Morris V, L Rihimaki, and M Ritsche. 2013. Measuring Sea-surface Temperature for the MAGIC Field Campaign. Presented at 4th Atmospheric System Research (ASR) Science Team Meeting. Potomac, Maryland.
- Morris V, C Long, and D Nelson. 2006. Deployment of an infrared thermometer network at the Atmospheric Radiation Measurement Program Southern Great Plains Climate Research Facility. In Proceedings of the Sixteenth...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf (31 pages, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=irt`, read 2026-09-23
- Example file: `sgpirt25mC1.b1.20260919.000000.nc` from `sgpirt25mC1.b1`, 0.14 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
