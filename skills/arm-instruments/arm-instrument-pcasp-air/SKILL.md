---
name: arm-instrument-pcasp-air
description: ARM Passive cavity aerosol spectrometer aboard aircraft (pcasp-air) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafpcaspF1.b1) and the variable inventory of a real file. Use when working with pcasp-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - pcasp-air, Passive cavity aerosol spectrometer aboard aircraft, sgpaafpcaspF1.b1, Aerosols, Airborne Observations, Droplet Measurement Technologies (DMT), PCASP-100X with Signal Processing Package 200 (SPP-200), netcdf, PADS, PCASP.
---

# PCASP-AIR - Passive cavity aerosol spectrometer aboard aircraft

The PCASP-AIR is an airborne optical spectrometer, mounted in a canister under the aircraft wing, that uses scattered laser light intensity to measure aerosol particle size distribution and number concentration over 0.1-3.0 µm.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `pcasp-air` |
| Handbook | [DOE/SC-ARM-TR-241 / L Goldberger / April 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-241.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Droplet Measurement Technologies (DMT), PCASP-100X with Signal Processing Package 200 (SPP-200) |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution |
| Record | 2013-06-24 to 2018-12-10 (retired) |
| Datastreams with data | 14 across 7 sites |
| Sites | acx, cor, ena, mao, nsa, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pcasp-air |


## Credit

Everything this skill knows about the instrument is the work of **L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Goldberger. *Passive Cavity Aerosol Spectrometer Probe Aboard Aircraft (PCASP-AIR) with Signal Processing Package 200 Instrument Handbook*, DOE/SC-ARM-TR-241, April 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-241.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The PCASP has two parts: an optical bench and signal processing electronics. The optical bench collects light scattered by individual particles passing through a laser beam and converts the photon pulses to an electron voltage pulse via an avalanche photodetector. The SPP-200 amplifies, filters, digitizes, and categorizes this voltage pulse before transmitting the digital value for processing by an external data system. Because scattered light intensity over the 0.1-3.0 µm range covers more than six orders of magnitude, amplification is divided into high-gain, mid-gain, and low-gain stages, with the processor automatically stepping down to lower gain stages as higher stages saturate. Particle size is measured using Mie scattering theory to relate the scattered light intensity to particle size, assuming the particle is spherical with a known refractive index.

**Siting.** The PCASP probe is mounted in a gray Particle Measuring Systems (PMS) canister positioned on the starboard side of the aircraft under the wing, attached to a pylon.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle number concentration | #/cc | 0.1-3.0 µm | ±16% (Concentration) | - | (hb p. 8) |
| Aerosol particle size distribution / Optical diameter | µm (bins) | 0.1-3.0 µm | ±20% (Diameter) | 32 size channels | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units - Optical_diameter | bins, µm | (hb p. 11) |
| Units - Gain_Signals | dimensionless | (hb p. 11) |
| Units - Sample_flow_rate | cm3/s | (hb p. 11) |
| Units - Laser_ref | V | (hb p. 11) |
| Units - Sheath_flow_rate | cm3/s | (hb p. 11) |
| Units - Instrument_temperature | C | (hb p. 11) |
| Range | 0.1-3.0 µm | (hb p. 11) |
| Accuracy | ±20% (Diameter); ±16% (Concentration) | (hb p. 11) |
| Repeatability | Extremely stable, drifts minimally between calibrations | (hb p. 11) |
| Sensitivity - Laser reference voltage | 6 to 10 volts for good operation | (hb p. 11) |
| Probe power requirements | 115 VAC, specified on ordering; 50-60 Hz; less than  120 W | (hb p. 12) |
| Anti-ice power requirements | 28 VDC, 215 W | (hb p. 12) |
| Number of size channels | 32 | (hb p. 12) |
| Volumetric flow (factory set) | 1 cm3/sec at standard pressure and temperature | (hb p. 14) |
| Weight | 40 pounds | (hb p. 16) |
| Dimensions | 40" long by 7" in diameter | (hb p. 16) |
| Laser type | HeNe multi-mode classical passive cavity, wavelength 0.6328 µm, classified as class II laser | (hb p. 16) |


## The data

Verified example: **`sgpaafpcaspF1.b1`**, file `sgpaafpcaspF1.b1.20160920.202755.nc`
(1.54 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5104, `optical_diameter`=30, `bound`=2 |
| Data variables | 16 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aafpcasp-b1-1.0 |
| process version | ingest-aafpcaspme-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `size_distribution` | 1/cm^3 | time,optical_diameter | yes | Particle size distribution |
| `total_area_concentration` | um^2/cm^3 | time | yes | Total surface area concentration |
| `total_number_concentration` | 1/cm^3 | time | yes | Total number concentration |
| `total_volume_concentration` | um^3/cm^3 | time | yes | Total volume concentration |
| `cloud_flag` | 1 | time | - | Cloud flag |
| `data_flag` | 1 | time | - | Data flag |
| `optical_diameter` | um | optical_diameter | - | Optical diameter |
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
                     params={"user": f"{user}:{token}", "ds": "sgpaafpcaspF1.b1",
                             "start": "2016-09-20", "end": "2016-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaafpcaspF1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaafpcaspF1.b1", "2016-09-20", "2016-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaafpcaspF1.b1", "2016-09-20", "2016-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("total_area_concentration", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
16 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_size_distribution"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("size_distribution", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["size_distribution", "total_number_concentration", "total_area_concentration"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaafpcaspF1.b1", "20130624", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: There are no current data quality reports at this time. Good data quality is ensured by comparison with other measurements: total number concentration from PCASP should not be greater than that measured by the in-cabin condensation particle counter 3772 and the in-cabin ultra-high-sensitivity aerosol spectrometer. Measurements should not be used when aircraft is 'in cloud' due to hydrometeor shattering; use the cloud flag in the met-air/IWG data set or WCM-2000 liquid water content greater than 0.1 g/m3 as an in-cloud indicator. Instrument is regularly calibrated in the field and laser power...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Shattering of hydrometeors on PCASP inlet when aircraft is 'in cloud' | Anomalous/elevated aerosol counts during in-cloud periods that do not reflect true ambient aerosol | Do not use PCASP measurements when aircraft is 'in cloud'; use the 'cloud flag' in the met-air/IWG data set, or WCM-2000 total liquid water content... | (hb p. 10) |
| Assumption of spherical particle shape and fixed refractive index (1.58) | Increased uncertainty in size distributions when sampling mixed composition or non-spherical aerosols; particles mis-sized | None stated beyond noting the assumption | (hb p. 12) |
| Coincidence error at high particle concentrations (multiple particles in beam... | Undercounting or miscounting of particles at high concentrations; concentration values may be biased low | Corrections are applied to account for these losses but still lead to concentration uncertainties | (hb p. 12) |
| Root-sum-squared amplification of size uncertainty in derived surface area and volume | Surface area and volume uncertainties appear a factor of two and three higher, respectively, than the underlying size uncertainty | None stated | (hb p. 12) |
| Laser power degradation / contamination of optics | Laser reference voltage in housekeeping data drops below the 6-10 volt healthy range | Clean the optics (laser output coupler and 45-degree mirror) when laser reference voltage drops below threshold; if cleaning/alignment does not... | (hb p. 11) |
| Gain-stage saturation across high/mid/low gain amplification | When all gain stages saturate, counts appear in the 'ADC Overflow' counter rather than a sized channel | Processor automatically steps down to mid-gain then low-gain when higher stages saturate; overflow counted separately | (hb p. 13) |
| Pump/flow failure | Volumetric flow deviates from the factory-set 1 cm3/sec value regardless of ambient conditions | If flow is not at set value, the pump has likely failed | (hb p. 14) |
| Plumbing leaks or electronic noise | Significant counts registering in channels during a zero-flow/filtered-air 'zero count' test when there should be few or none | Tighten plumbing connections for simple leaks; use a leak detector and pressurize optics chamber for serious leaks | (hb p. 15) |
| Moisture/humidity clogging of drying material | Reduced desiccant effectiveness, potential clogging of sample line | Replace desiccant and filter periodically (every other year) and before campaigns in humid locales | (hb p. 16) |
| Instrument in storage / no data being collected | Data gap during period aircraft undergoes modifications | None stated (informational mentor summary) | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibrated using monodispersed polystyrene latex spheres (PSLs) with refractive index 1.58, nebulized via an aerosol generator; also requires aligning the 45-degree mirror. Probe is sent to the vendor for calibration and laser alignment. (hb p. 13) |
| Calibration interval | Required post-shipping and at the start of each deployment; during campaigns generally only PSL aerosol calibrations are necessary; instrument is regularly calibrated in the field and laser power monitored during each flight. (hb p. 13) |
| Traceability | Calibration results tracked by the AAF's director of engineering; instrument returned with calibration histograms for comparison with later calibration verifications. (hb p. 13) |
| Routine maintenance | Cleaning and aligning the laser output coupler and 45-degree mirror using an acetone-dampened Q-tip; leak checks with sample flow valve closed to check for zero counts; replacing desiccant and filter in the drying tube. (hb p. 15) |
| Maintenance interval | Desiccant and filter should be replaced periodically or once every other year to reduce clogging; recommended to replace desiccant before campaigns in humid locales. (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: in-cabin condensation particle counter 3772, in-cabin ultra-high-sensitivity aerosol spectrometer, WCM-2000 (Water Content Measurement) multi-element water content....

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ADC` | ARM Data Center |
| `ARM` | Atmospheric Radiation Measurement |
| `DMT` | Droplet Measurement Technologies |
| `ID` | inside diameter |
| `IWG` | interagency working group |
| `netcdf` | Network Common Data Form |
| `PADS` | Particle Analysis and Display System |
| `PCASP` | passive cavity aerosol spectrometer probe |
| `PMS` | Particle Measuring Systems |
| `PSL` | polystyrene latex sphere |
| `SPP` | signal processing package |
| `WCM` | Water Content Measurement |


### References the handbook cites

- Cai, Y, JR Snider, and P Wechsler. 2013. "Calibration of the passive cavity aerosol spectrometer probe for airborne determination of the size distribution." Atmospheric Measurement Techniques 6(9): 2349–2358,...
- Droplet Measurement Technologies. 2012. Passive Cavity Aerosol Spectrometer Probe (PCASP-100X) Operator Manual. DOC-0228, Rev C.
- Vendor's website: https://www.dropletmeasurement.com/product/passive-cavity-aerosol-spectrometer-probe/

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-241.pdf (17 pages, DOE/SC-ARM-TR-241, by L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=pcasp-air`, read 2026-09-23
- Example file: `sgpaafpcaspF1.b1.20160920.202755.nc` from `sgpaafpcaspF1.b1`, 1.54 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
