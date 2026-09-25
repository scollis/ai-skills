---
name: arm-instrument-pops-air
description: ARM portable optical particle spectrometer aboard an airborne platform (pops-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol particle size distribution), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaafpopsU2.b1) and the variable inventory of a real file. Use when working with pops-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - pops-air, bnfaafpopsU2.b1, Aerosol particle size distribution, Aerosols, Airborne Observations, Handix Scientific Inc., HEPA, NIST, NOAA, POPEYE.
---

# POPS-AIR - portable optical particle spectrometer aboard an airborne platform

POPS-AIR is a lightweight optical particle spectrometer that measures aerosol particle size distribution (~0.13-3 µm) and total number concentration, deployed aboard ARM Aerial Facility unmanned aerial systems and tethered balloon systems.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `pops-air` |
| Handbook | [DOE/SC-ARM-TR-259 / F Mei, M Pekour / January 2026](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-259.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Handix Scientific Inc., POPS-AIR (portable optical particle spectrometer aboard an airborne platform); original design described in Gao et al. 2016 |
| Primary measurements | Aerosol particle size distribution; Aerosol concentration |
| Record | 2020-09-30 to 2026-09-16 (active) |
| Datastreams with data | 8 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pops-air |


## Credit

Everything this skill knows about the instrument is the work of **F Mei, M Pekour** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> F Mei, M Pekour. *Portable Optical Particle Spectrometer aboard an Airborne Platform (POPS-AIR) Instrument Handbook*, DOE/SC-ARM-TR-259, January 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-259.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Sample particles, sheathed in clean air to maintain laminar flow and avoid biased sizing at the fringe of the sampling volume, transit a 405-nm laser diode beam inside the optical chamber. Light scattered by the particles is collected by a spherical mirror at the bottom of the optical chamber and focused onto the detection region of a photomultiplier tube. The pulse height of the scattered light signal is scaled to particle diameter using a theory-based calibration response function derived from a size look-up table calibrated with monodisperse PSL aerosols. A laser heater maintains the laser diode at a minimum operating temperature of 35 degC, which is essential for cold-weather applications.

**Siting.** Deployed aboard ARM Aerial Facility unmanned aerial systems (UAS) and tethered balloon systems (TBS). On aircraft/UAS platforms, sample and sheath inlets must be connected to the same inlet manifold to minimize flow distortions caused by differing inlet-line pressures relative to cabin/ambient pressure; exhaust line must be balanced with similar pressure to the inlet line to reduce pump load. In icy environments, an insulated enclosure keeps internal temperature around 15 degC.

**Sampling.** native rate Output data recorded after every sample, typically every second; reported every 1 second; averaging A new data file is started every time the system is restarted or the file size reaches a threshold (hb p. 4).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle size distribution | nanometers (nm) | approximately 0.13 to 3 µm (130 to 3000... | manufacturer specifies within 2.5% of particle... | 12 size bins | (hb p. 7) |
| Total particle number concentration | particles per cubic... | 0 to 3000 s-1 (4000 cm-3 with 25%... | 25% at upper concentration limit (4000 cm-3) | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units | aerosol particle size in nanometers (nm); aerosol particle number concentration in particles per cubic centimeter (cm3), or raw counts (dimensionless) | (hb p. 7) |
| Range - particle size | 130 to 3000 nm | (hb p. 7) |
| Range - total particle number concentration | 0 to 3000 s-1 (4000 cm-3 with 25% uncertainty) | (hb p. 7) |
| Accuracy | within 5% (per SMPS comparison), for total particle counts below 3000 s-1 with no significant coincidence | (hb p. 7) |
| Repeatability | within 1%, for total particle counts below 4000 cm-3 with no significant coincidence | (hb p. 7) |
| Sensitivity - upper concentration limit for reliable... | around 4000 cm-3 | (hb p. 7) |
| Uncertainty - particle sizing (manufacturer specified) | within 2.5% of particle size | (hb p. 8) |
| Nominal sample flow (on ground) | 3 cm3/s | (hb p. 1) |
| Nominal sheath flow (on ground) | 9 cm3/s | (hb p. 1) |
| Laser wavelength | 405 nm | (hb p. 1) |
| Minimum laser operating temperature | 35 degC | (hb p. 1) |
| Laser temperature normal operating range | 25-65 degC | (hb p. 5) |
| Insulated enclosure internal temperature (icy environments) | around 15 degC | (hb p. 2) |
| Number of size bins (processed data) | 12 size bins | (hb p. 3) |
| Warm-up time (Daily Zero check) | approximately 600 seconds | (hb p. 9) |
| Zero response time (HEPA filter attached) | particle concentration goes to zero in approximately 5 to 10 seconds; leave attached 30 seconds to ensure stable zero | (hb p. 9) |
| Laser Class | Class I Laser Product | (hb p. 15) |


## The data

Verified example: **`bnfaafpopsU2.b1`**, file `bnfaafpopsU2.b1.20260911.144213.nc`
(10.64 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=7838, `optical_diameter`=100, `bound`=2 |
| Data variables | 38 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-11T14:42:13 to 2026-09-11T16:52:50 |
| dod version | aafpops-b1-1.1 |
| process version | ingest-aafpopscorr-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `size_distribution` | 1/cm^3 | time,optical_diameter | yes | Particle size distribution in dN |
| `total_number_concentration` | 1/cm^3 | time | yes | Total number concentration |
| `aerosol_temperature` | degC | time | - | Aerosol temperature |
| `atm_pressure` | hPa | time | - | Ambient atmospheric pressure |
| `baseline` | 1 | time | - | Measured signal in optical cavity in absence of light |
| `baseline_start_value` | 1 | time | - | Starting value of baseline |
| `baseline_std` | 1 | time | - | Standard deviation of noise on baseline signal |
| `baseline_threshold` | 1 | time | - | Threshold above baseline for values to be counted as valid particles |
| `baseline_threshold_multiplier` | 1 | time | - | Threshold multiplier * std |
| `battery_voltage` | V | time | - | Input power supply voltage |
| `flow_setting` | V | time | - | Voltage of flow set point |
| `laser_current` | mA | time | - | Laser diode current |
| `laser_feedback` | mV | time | - | Feedback on laser diode circuit |
| `laser_monitor` | 1 | time | - | Output laser power |
| `laser_temp` | degC | time | - | Temperature of laser diode |
| `log_max` | 1 | time | - | Log10 of maximum bin size in nm |
| `log_min` | 1 | time | - | Log10 of minimum bin size in nm |
| `max_peak_points` | 1 | time | - | Maximum points to be counted as a valid peak |
| `min_peak_points` | 1 | time | - | Minimum points to be counted as a valid peak |
| `optical_diameter` | nm | optical_diameter | - | Optical diameter |
| `pump_feedback` | mV | time | - | Pump feedback control voltage |
| `pump_hours` | hour | time | - | Pump life-time hours |
| `raw_bin_counts` | count | time,optical_diameter | - | Raw counts in each bin |
| `raw_points` | 1 | time | - | Number of raw points to output for randomized background analysis |
| `sample_flow_rate` | cm^3/s | time | - | POPS sample flow rate measured through the entrant tubing |
| `sample_flow_rate_smoothed` | cm^3/s | time | - | Smoothed sample flow rate |
| `temp_board` | degC | time | - | Temperature of POPS electronics board |
| `time` | - | time | - | Time offset from midnight |
| `total_count_rate` | 1/s | time | - | Total number of particles per second including outside the size range |


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
                     params={"user": f"{user}:{token}", "ds": "bnfaafpopsU2.b1",
                             "start": "2026-09-11", "end": "2026-09-11", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaafpopsU2.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaafpopsU2.b1", "2026-09-11", "2026-09-11")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaafpopsU2.b1", "2026-09-11", "2026-09-11"))   # cite what you pulled
```

## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
38 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_size_distribution"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("size_distribution", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["size_distribution", "total_number_concentration", "lat"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfaafpopsU2.b1", "20200930", "20260924")
```

The handbook's own note on data quality: Data quality evaluation involves automatic generation of housekeeping plots by a mentor, examining: aerosol particle size distribution vs. time (low counts or noisy signal may indicate optics block misalignment/contamination or unstable sample flow); comparison of particle number concentration with co-located instruments (UHSAS, SMPS) which should show the same general trend if integrated over the same size ranges; sample flow rate (low/unstable flow indicates blockage or failing pump); and laser temperature (values outside 25-65 degC cause considerable uncertainty in size determination)....

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sample flow/pressure distortion on aircraft/UAS platform | Unstable or inaccurate sample flow rate readings; possible sizing errors due to inlet/cabin/ambient pressure differential | Connect POPS-AIR sample and sheath inlets to the same inlet manifold; balance exhaust line pressure similarly to reduce pump load | (hb p. 7) |
| Cold-weather laser temperature drop | Laser temperature falling below normal range causing increased sizing uncertainty | Laser heater added to maintain laser operating temperature at a minimum of 35 degC; insulated enclosure used in icy environments to keep internal... | (hb p. 7) |
| Optics block contamination or misalignment | Low counts or noisy signal in aerosol particle size distribution vs. time plots | Housekeeping plots monitored by mentor; replacement of 3D-printed mounts with machined aluminum parts to reduce outgassing contamination of optical... | (hb p. 4) |
| Low or unstable sample flow / blockage or failing pump | Low or unstable sample flow rate in housekeeping plot | Monitor flow rate in housekeeping plots; check for blockage in sample line or failing pump | (hb p. 5) |
| Laser temperature out of range | Laser temperature outside 25-65 degC in housekeeping plot | None specified beyond monitoring; causes considerable uncertainty in size determination | (hb p. 5) |
| Particle coincidence at high concentration | Undercounting/mis-sizing when total particle counts approach or exceed ~3000 s-1 / 4000 cm-3; concentration measurements above 4000 cm-3 have 25% uncertainty | No corrections made by instrument for coincidence; use a dilution system when sampling above the upper concentration limit | (hb p. 13) |
| Non-PSL refractive index / non-spherical particle shape bias | Sized incorrectly compared to true diameter when ambient aerosol differs from PSL calibration aerosol in refractive index or shape | Apply corrections if ambient particle refractive index is known [2,3] | (hb p. 13) |
| Optical surface contamination from 3D-printed plastic outgassing (older design) | Degraded optics performance, noisy or low signal | Replaced 3D-printed components for laser/optics mounting with machined aluminum parts | (hb p. 8) |
| Instrument sizing resolution limit from optics geometry | Inherent uncertainty in particle sizing manifesting as scatter around true size | Manufacturer specifies uncertainty within 2.5% of particle size | (hb p. 14) |
| Data object description subject to change | Variation in recorded data fields/format across software revisions | Note that description is subject to change with future instrument software revisions | (hb p. 4) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Manufacturer calibration measures size distribution of NIST-traceable PSL calibration aerosols, calibrates gain of four internal pulse-height measurement ranges, calibrates inlet flow rate with a precision flow meter, and performs zero counts verification with a HEPA filter attached to the inlet; instrument mentors... (hb p. 15) |
| Calibration interval | Full calibration typically once every 12 months or as needed, e.g., before deployment (hb p. 15) |
| Traceability | NIST-traceable PSL calibration aerosols (hb p. 15) |
| Routine maintenance | Consult the manufacturer's manual for cleaning the laser optics, cleaning the mirror, and laser alignment (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: UHSAS (ultra-high-sensitivity aerosol spectrometer), SMPS (scanning mobility particle sizer), DMA (differential mobility analyzer), POPS (portable optical particle spectrometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AMF3` | third ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `DAQ` | data acquisition |
| `DMA` | differential mobility analyzer |
| `DQ` | Data Quality |
| `HEPA` | high-efficiency particulate air |
| `NIST` | National Institute of Standards and Technology |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `POPEYE` | Profiling at Oliktok Point to Enhance YOPP Experiments |
| `POPS` | portable optical particle spectrometer |
| `POPS-AIR` | portable optical particle spectrometer aboard an airborne platform |
| `SMPS` | scanning mobility particle sizer |
| `TBS` | tethered balloon system |


### References the handbook cites

- Mei, F, G McMeeking, M Pekour, R-S Gao, G Kulkarni, S China, H Telg, D Dexheimer, J Tomlinson, and B Schmid. 2020. "Performance Assessment of Portable Optical Particle Spectrometer (POPS)." Sensors 20(21): 6294,...
- Cai, Y, D Montague, W Mooiweer-Bryan, and T Deshler. 2008. "Performance characteristics of the ultra-high-sensitivity aerosol spectrometer for particles between 55 and 800 nm: Laboratory and field studies." Journal of...
- Ames, RB, JL Hand, SM Kreidenweis, DE Day, and WC Malm. 2000. "Optical measurements of aerosol size distributions in Great Smoky Mountains National Park: Dry aerosol characterization." Journal of the Air and Waste...
- Gao, RS, H Telg, RJ McLaughlin, SJ Ciciora, LA Watts, MS Richardson, JP Schwarz, AE Perring, TD Thornberry, AW Rollins, MZ Markovic, TS Bates, JE Johnson, and DW Fahey. 2016. "A light-weight, high-sensitivity particle...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-259.pdf (17 pages, DOE/SC-ARM-TR-259, by F Mei, M Pekour)
- Catalog record: ARM data-source index, `instrument_class_code=pops-air`, read 2026-09-24
- Example file: `bnfaafpopsU2.b1.20260911.144213.nc` from `bnfaafpopsU2.b1`, 10.64 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
