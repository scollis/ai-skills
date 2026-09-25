---
name: arm-instrument-irt-air
description: ARM Infrared Thermometer - Airborne (irt-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Sky infrared temperature, Surface infrared temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafirtU2.b1) and the variable inventory of a real file. Use when working with irt-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Radiometric. Triggers - irt-air, Infrared Thermometer - Airborne, bnfaafirtU2.b1, Sky infrared temperature, Surface infrared temperature, Airborne Observations, Radiometric, vendor Wintronics, AERI, ASTM, GNDRAD, IRTSST.
---

# IRT-AIR - Infrared Thermometer - Airborne

The IRT is a ground-based (and, for the ARM Aerial Facility variant, aircraft-mounted) radiation pyrometer that measures the equivalent blackbody brightness temperature of the sky (downwelling) or ground surface (upwelling) in its field of view, reported in Kelvins.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 31 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `irt-air` |
| Handbook | [DOE/SC-ARM-TR-015 / VR Morris / January 2018](https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf) |
| Measurement category | Airborne Observations; Radiometric |
| Manufacturer / model | Heitronics GmbH KT19.85 Infrared Radiation Pyrometer (Type I and Type II); vendor Wintronics, Inc. |
| Primary measurements | Longwave narrowband brightness temperature |
| Record | 2021-03-03 to 2026-09-14 (active) |
| Datastreams with data | 6 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/irt-air |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Infrared Thermometer (IRT) Instrument Handbook*, DOE/SC-ARM-TR-015, January 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `irt-air`, ARM links no handbook to this class. The facts below come from the **Infrared Thermometer** (`irt`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `irt-air` until checked against that document's own section for it.

## How it measures

The IRT is a radiation pyrometer that intercepts infrared radiation emitted by a target and, using an optical chopper, alternately exposes the pyroelectric detector to the target radiation and to an internal blackbody reference source of known temperature; this "chopped radiation" method eliminates thermal drift from the housing. Because the detector output is linear and proportional to the measured radiance, and radiance is related to temperature via Planck's law once the relative spectral response of the optical system and detector is known, the output signal can be calibrated directly in temperature units (Kelvins). Each unit is characterized against blackbody radiation at multiple temperatures to compensate for individual deviations in filters, detector sensitivity, and lenses (linearization). The downwelling IRT reports the effective blackbody temperature of the sky, dominated by atmospheric water vapor in clear conditions and increased by clouds in the field of view; the upwelling IRT reports a narrowband radiating temperature very close to the physical temperature of the ground/vegetation in its field of view, using an assumed emissivity.

**Siting.** The downwelling IRT is mounted at a height of 1-2 m above the ground inside a ventilated enclosure (Hoffman CSD16126SS6), oriented so the zenith view of the sky is reflected into the lens by a protected gold mirror (Edmund Optics 45-617). The upwelling IRT is mounted at a height of 2-25 m above the ground inside a small enclosure, oriented so the mounting platform is not in the field of view and to ensure the ground and vegetation cover are representative of the local area. For the ARM Aerial Facility (AAF), IRTs (SN 2326, 2327 upwelling) are deployed on the aerial facility platform (listed as located at PNNL, spare status as of Jan 2018); the handbook also notes downwelling/upwelling IRT...

**Sampling.** native rate 5-Hz instantaneous (irt200ms); 1-sec instantaneous (irtsst); reported every irt200ms: 5 Hz; irt/gndirt/irt10m/irt25m: 1-min-averaged; irtsst: 1-sec instantaneous; averaging 1-minute averaging for irt, gndirt, irt10m, irt25m datastreams (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sky infrared temperature (downwelling) | K | 173 to 473 K (Type II); 213 to 673 K... | ±0.5 K + 0.7% of temperature difference | ±1.85 K at 223 K; ±0.70 K... | (hb p. 20) |
| Surface infrared temperature (upwelling) | K | 173 to 473 K (Type II); 213 to 673 K... | ±0.5 K + 0.7% of temperature difference | ±1.85 K at 223 K; ±0.70 K... | (hb p. 20) |
| Internal reference infrared temperature | K | - | - | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Spectral Sensitivity | 9.6 to 11.5 µm (both Type I and Type II) | (hb p. 20) |
| Temperature Measuring Range | Type I (SNless than 2000): 213 to 673 K; Type II: 173 to 473 K | (hb p. 20) |
| Temperature Resolution (emissivity=1) | Type I: ±1.10 K at 223 K; ±0.45 K at 293 K (response time 1.0 s); Type II: ±1.85 K at 223 K; ±0.70 K at 293 K (response time 0.1 s) | (hb p. 20) |
| Accuracy | ±0.5 K + 0.7% of temperature difference (both types) | (hb p. 20) |
| Operational Ambient Temperature | Type I: 0° to 60°C; Type II: -20° to +60°C | (hb p. 20) |
| Storage Temperature | -20° to +70°C (both types) | (hb p. 20) |
| Weight | Type I: 1.5 kg; Type II: 2.4 kg | (hb p. 20) |
| Analog Output Resolution | 12 bit (both types) | (hb p. 20) |
| Optical Field of View (at 3 m) | Type I: downwelling (S921 lens, f=120mm) 2.64°; upwelling (M6 lens, f=20mm) 30.51°. Type II: downwelling (S921 lens, f=120mm) 2.64° | (hb p. 20) |
| Operating Voltages | 24 V AC (±10%) at 48 to 400 Hz or 26 V DC (±15%) (both types) | (hb p. 20) |
| Current Consumption | 80 mA (both types) | (hb p. 20) |
| Target emissivity (EMI) - Downwelling | 0.987 | (hb p. 18) |
| Target emissivity (EMI) - Upwelling | 1.000 | (hb p. 18) |
| Temperature span (ANALOG) - Downwelling | 173-303 K | (hb p. 18) |
| Temperature span (ANALOG) - Upwelling | 223-323 K | (hb p. 18) |
| Analog output (ANALOG) | 0-1 volt | (hb p. 18) |
| Digital output (COM) | 9.6Kb/8NP/1S/LF | (hb p. 18) |
| Response time (RESP) - Downwelling | 0.3 second | (hb p. 18) |
| Response time (RESP) - Upwelling | 3.0 seconds | (hb p. 18) |


## The data

Verified example: **`bnfaafirtU2.b1`**, file `bnfaafirtU2.b1.20260910.163628.nc`
(4.5 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=74864 |
| Data variables | 10 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2026-09-10T16:36:28 to 2026-09-10T20:17:27 |
| dod version | aafirt-b1-2.0 |
| process version | ingest-aafirtcorr-1.0-2.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `sky_ir_temp` | degC | time | yes | Sky/cloud infrared temperature |
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
                     params={"user": f"{user}:{token}", "ds": "bnfaafirtU2.b1",
                             "start": "2026-09-10", "end": "2026-09-10", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaafirtU2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaafirtU2.b1", "2026-09-10", "2026-09-10")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaafirtU2.b1", "2026-09-10", "2026-09-10"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("sky_ir_temp", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
10 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_sky_ir_temp"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("sky_ir_temp", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["sky_ir_temp", "lat", "lon"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (bnfaafirtU2.b1.20260910.163628.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `lat` | Value is equal to missing_value. | 54 | 0.0721 |
| `lon` | Value is equal to missing_value. | 54 | 0.0721 |
| `alt` | Value is equal to missing_value. | 54 | 0.0721 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("bnfaafirtU2.b1", "20210303", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Most datastream fields have a corresponding automated QC field qc_less than fieldnamegreater than  in b1-level datastreams, with flag values 0-15 indicating missing/min/max/delta check failures (Table 7). Minimum/maximum/delta thresholds differ for downwelling (sky_ir_temp: 173-303K, delta 50K; ref_ir_temp: 253-333K, delta 10K) and upwelling (sfc_ir_temp: 223-323K, delta 50K; ref_ir_temp: 253-333K, delta 10K) datastreams (Tables 8-9). A separate qc_time field flags duplicate samples, missing samples, or time offset problems relative to per-datastream lower/upper Dt limits (Table 10-11:...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Positive spikes from daily maintenance cleaning | Positive spikes in sky temperature measurements coincide with daily preventative maintenance times, due to water/alcohol used to clean the gold mirror | Recognize as maintenance artifact; not a data quality note beyond identification | (hb p. 20) |
| Solar intrusion spikes near local solar noon | Positive spikes in sky temperature measurements near local solar noon, especially at tropical sites near equinoxes, due to sun entering the IRT field of view | - | (hb p. 20) |
| Warm bias in upwelling surface temperature vs PIR at tower-mounted sites | Upwelling IRT surface temperature reads warmer than PIR at sites where instrument mounted 10 m above ground, especially in summer/daytime (e.g., TWP/CF3: IRT ~51°C vs PIR ~10°C cooler while... | - | (hb p. 20) |
| Negative bias of sky temperature vs MWRP/MWR3C | Downwelling IRT sky temperature reads lower than MWRP/MWR3C by ~10°C due to differing fields of view (IRT 2.6° vs MWRP/MWR3C 30°) | - | (hb p. 20) |
| Positive bias vs AERI at very cold/clear sky temperatures | Downwelling IRT reads warmer than AERI during clear-sky conditions when sky temperature is below ~180K; effect worsens with hot ambient temperature and inaccurate calibration at the 223K... | Accurate calibration at the lower limit (223K) recommended | (hb p. 20) |
| Internal reference temperature below measurable minimum in winter at AMF3/OLI | Internal reference temperature of downwelling and upwelling IRTs at AMF3 (OLI/M1) frequently falls below the minimum measurable value of -20°C in winter | - | (hb p. 20) |
| Water vapor contribution to cloud-base temperature retrieval | Sky temperature measured is influenced by atmospheric water vapor above the instrument, not solely cloud base temperature; effect significant in summer at SGP and year-round at tropical AMF... | AERI data could be used to determine corrections for water vapor contribution | (hb p. 10) |
| Individual unit-to-unit variation in spectral/detector characteristics | Each IRT shows small deviations due to differences in filters, detector sensitivity, and lenses | Compensated by comparing instrument reading with blackbody radiation at several temperatures and adapting linearization | (hb p. 19) |
| Data acquisition system reconfiguration discontinuities | Step changes/discontinuities in datastream lineage when IRT signals moved from SKYRAD/GNDRAD datalogger to dedicated data acquisition system (e.g., AMF2 on 5/25/2017, ENA/C1 on 6/5/2017) | - | (hb p. 20) |
| Instrument/model upgrades (Type I to Type II) changing measurement range and response time | Step changes in data characteristics (range, resolution, response time) at dates of Type I to Type II upgrades (e.g., SGP/C1 10m 9/17/2013, 25m 9/19/2013, TWP/C3 10/28/2013, TWP/C1... | - | (hb p. 20) |
| Mounting/enclosure configuration changes | Discontinuities in data due to changes in mounting hardware (e.g., SKYRAD IRT moved from Radiometrics case/saddle and elliptical mirror to Hoffman enclosure and round gold mirror at various... | - | (hb p. 21) |
| Datastream/instrument reassignment history (MWR, MFR removal) | Historical breaks in datastream continuity when IRTs were removed from MWR or MFR dataloggers and associated datastreams | - | (hb p. 21) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Factory calibration per ASTM E1256-88 using a blackbody calibration source at high temperature (80-100°C); calibration factor adjusted via device menu until display matches blackbody temperature. Mentor calibration recommends collocating upward-looking instruments with AERI, computing narrowband radiance LIRT =... (hb p. 9) |
| Calibration interval | Calibration/repair checks performed periodically (varies by unit, see calibration history table); not a fixed interval stated. (hb p. 9) |
| Traceability | ASTM Standard Test Methods for Radiation Thermometers (Single Waveband Type) E1256-88; cross-comparison with AERI spectrometer and blackbody (BB) sources (hb p. 9) |
| Routine maintenance | Fine dust removed from lens with compressed air or fine lens brush; heavily soiled or greasy lens cleaned with paper tissues, cotton swabs, and lens-cleaning solution (alcohol or water). (hb p. 19) |
| Maintenance interval | Daily preventative maintenance (implied by note about daily cleaning producing spikes) (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AERI, PIR, MWR, MWRP, MWR3C, GNDRAD, SKYRAD, IRTSST.

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

- Morris V, L Rihimaki, and M Ritsche. 2013. Measuring Sea-surface Temperature for the MAGIC Field Campaign. Presented at 4th Atmospheric System Research (ASR) Science Team Meeting. Potomac, Maryland.
- Morris V, C Long, and D Nelson. 2006. Deployment of an infrared thermometer network at the Atmospheric Radiation Measurement Program Southern Great Plains Climate Research Facility. In Proceedings of the Sixteenth...
- ASTM E1256-88 Standard Test Methods for Radiation Thermometers (Single Waveband Type)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/irt_handbook.pdf (31 pages, DOE/SC-ARM-TR-015, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=irt-air`, read 2026-09-24
- Example file: `bnfaafirtU2.b1.20260910.163628.nc` from `bnfaafirtU2.b1`, 4.5 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
