---
name: arm-instrument-mpl
description: ARM Micropulse Lidar (mpl) - handbook-derived instrument reference. Measurement principle, reported quantities (Lowest detected cloud base height, Normalized Relative Backscatter, Linear depolarization ratio), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpminimplC1.b1) and the variable inventory of a real file. Use when working with mpl data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Cloud Properties. Triggers - mpl, Micropulse Lidar, sgpminimplC1.b1, Lowest detected cloud base height, Normalized Relative Backscatter, Linear depolarization ratio, Aerosols, Cloud Properties, Micro Pulse LiDAR, part of Hexagon, ARSCL, AWARE, COMBLE, ICECAPS.
---

# MPL - Micropulse Lidar

The MPL is a ground-based, autonomous, eye-safe lidar operating at 532 nm that transmits short laser pulses and measures the time-resolved backscattered signal to detect the altitude of clouds and, with post-processing, characterize atmospheric aerosols.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `mpl` |
| Handbook | [DOE/SC-ARM-TR-019 / P Muradyan, R Coulter / March 2020](https://www.arm.gov/publications/tech_reports/handbooks/mpl_handbook.pdf) |
| Measurement category | Aerosols; Cloud Properties |
| Manufacturer / model | Micro Pulse LiDAR, part of Hexagon, sold through Leica Geosystems, Inc.; laser systems originally Spectra Physics (model 7300 or "R-Series"), later supplied by Photonics, Inc.; lidar control system... |
| Primary measurements | Aerosol concentration; Aerosol extinction; Aerosol optical depth; Backscatter depolarization ratio; Backscattered radiation; Cloud base height |
| Record | 1996-03-12 to 2026-09-23 (active) |
| Datastreams with data | 58 across 34 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc |
| ARM page | https://www.arm.gov/capabilities/instruments/mpl |


## Credit

Everything this skill knows about the instrument is the work of **P Muradyan, R Coulter** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> P Muradyan, R Coulter. *Micropulse Lidar (MPL) Instrument Handbook*, DOE/SC-ARM-TR-019, March 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/mpl_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

A short pulse of laser light is transmitted from the telescope; as it travels, part of it is scattered by molecules, water droplets, or other atmospheric objects, with greater numbers of scatterers producing greater scattered fraction. A small portion of the scattered light returns toward the instrument, is collected by the telescope, and detected. The detected signal is stored in range bins according to elapsed time since pulse transmission, which relates directly to distance to the scatterer. The collection of bins for each pulse is called a profile, and a cloud appears as a spike/increase in the backscattered signal profile because cloud water droplets produce strong backscatter.

**Siting.** The MPL is configured to operate autonomously in an unattended manner 24 hours a day. Standard ARM deployments orient the MPL vertically (or slightly off vertical).

**Sampling.** native rate 2500 Hz laser pulse rate; fast-switching polarization switches on every pulse (2500 Hz rate) for FS systems; averaging 10-second averaging time (hb p. 16).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Co-pol and cross-pol backscatter signal | - | up to 20+ km | - | - | (hb p. 12) |
| Lowest detected cloud base height | m | - | ±2% (timing calibration) plus ±1/2 range... | - | (hb p. 12) |
| Normalized Relative Backscatter (NRB) profile | arbitrary units | - | - | - | (hb p. 12) |
| Linear depolarization ratio | - | - | - | - | (hb p. 17) |
| Aerosol extinction and backscatter profiles | - | - | - | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wavelength of laser pulse | 532 nm | (hb p. 16) |
| Length of laser pulse | ~10 ns = 3 m | (hb p. 16) |
| Range resolution (height interval) | 15 m | (hb p. 16) |
| Maximum range for cloud base height | 18 km | (hb p. 16) |
| Typical averaging | 10 sec | (hb p. 16) |
| Laser pulse rate | 2500 Hz | (hb p. 15) |
| Laser output power (green, 532 nm) | about 25 mW pulses | (hb p. 15) |
| Infrared CW pump radiation power | approximately 1.0 watt | (hb p. 15) |
| Narrow-band interference filter bandwidth | 0.27 nm fwhm | (hb p. 16) |
| Telescope aperture | 8" Celestron telescope | (hb p. 15) |
| Laser current (normal operation) | 0.5 to 1.0 amp | (hb p. 18) |
| Laser energy (normal operation) | 2 to 7 µJ | (hb p. 18) |
| Early SGP/TWP C1 range resolution | 300 meters | (hb p. 12) |


## The data

Verified example: **`sgpminimplC1.b1`**, file `sgpminimplC1.b1.20260724.000003.nc`
(139.22 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=8638, `range_bins`=2000, `num_darkcount_corr`=2000, `num_deadtime_corr`=20, `num_overlap_corr`=668 |
| Data variables | 46 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 10 s |
| File time span | 2026-07-24T00:00:03 to 2026-07-24T23:59:52 |
| sampling interval | 0.000400 |
| averaging interval | 10.000000 |
| dod version | minimpl-b1-1.0 |
| process version | ingest-mplpolfs-1.24-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `detector_temp` | degC | time | yes | Detector temperature |
| `energy_monitor` | uJ | time | yes | Energy output per pulse of transmitted laser beam at 532 nm (Doubled... |
| `laser_temp` | degC | time | yes | Laser temperature |
| `range_offset` | km | time | yes | Distance between initial range_bin and the laser flash |
| `scope_temp` | degC | time | yes | Telescope temperature |
| `signal_return_co_pol` | count/us | time,range_bins | yes | Attenuated backscatter, copol |
| `signal_return_cross_pol` | count/us | time,range_bins | yes | Attenuated backscatter, cross pol |
| `afterpulse_correction_co_pol` | count/us | range_bins | - | Afterpulse correction factor co_pol |
| `afterpulse_correction_cross_pol` | count/us | range_bins | - | Afterpulse correction factor cross_pol |
| `background_signal_co_pol` | count/us | time | - | Background signal, copol data |
| `background_signal_cross_pol` | count/us | time | - | Background signal, cross pol data |
| `background_signal_std_co_pol` | count/us | time | - | Background signal standard deviation, copol data |
| `background_signal_std_cross_pol` | count/us | time | - | Background signal standard deviation, cross pol data |
| `darkcount_correction_co_pol` | count/us | num_darkcount_corr | - | Darkcount correction factor co_pol |
| `darkcount_correction_cross_pol` | count/us | num_darkcount_corr | - | Darkcount correction factor cross_pol |
| `dead_time_corrected` | 1 | time | - | Dead time correction flag |
| `deadtime_correction` | 1 | num_deadtime_corr | - | Deadtime correction factor |
| `deadtime_correction_counts` | count/us | num_deadtime_corr | - | Laboratory measured counts used to calculate the deadtime correction... |
| `first_data_bin` | 1 | time | - | Bin number of first data. Tells where pretrigger timing ends and end... |
| `height` | km | range_bins | - | Height above ground of the center of corresponding range_bin |
| `laser_fire_bin` | 1 | time | - | Bin number associated with zero height and time where laser transmit... |
| `max_altitude` | km | - | - | Maximum altitude retrieved from multichannel scalar card. |
| `mcs_mode` | 1 | - | - | MCS mode register. |
| `num_bins` | count | - | - | Number of bins stored in data block |
| `num_channels` | count | - | - | Number of detector channels |
| `overlap_correction` | 1 | num_overlap_corr | - | Overlap correction factor |
| `overlap_correction_heights` | km | num_overlap_corr | - | Heights for overlap correction |
| `polarization_control` | 1 | time | - | Polarization control enabled flag |
| `polarization_control_voltage` | V | time | - | Polarization control voltage setting |
| `pulse_rep` | Hz | - | - | Repetition rate, or Trigger Frequency of the laser |


_6 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpminimplC1.b1",
                             "start": "2026-07-24", "end": "2026-07-24", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpminimplC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpminimplC1.b1", "2026-07-24", "2026-07-24")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpminimplC1.b1", "2026-07-24", "2026-07-24"))   # cite what you pulled
```

This datastream carries 46 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpminimplC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["detector_temp", "energy_monitor", "laser_temp", "qc_detector_temp", "qc_energy_monitor", "qc_laser_temp"],
                                cleanup_qc=True)
```

Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

7 `qc_` companion variables cover 7 of the
46 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_range_offset"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("range_offset", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["range_offset", "energy_monitor", "detector_temp"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpminimplC1.b1", "19960312", "20260923")
```

The handbook's own note on data quality: QC frequency: Monthly; QC delay: 1 week; QC type: Graphical plots; Inputs: Raw data; Outputs: Processed backscatter profiles. Daily data quality monitoring of the MPL at all ARM sites mainly consists of visual inspection of vertical time sections of backscattered signal. DQO website provides DQ-Explorer, DQ-Plotbrowser, DQ-Zoom, and NCVweb tools for inspecting and assessing MPL data quality; most site scientist checking techniques are incorporated within DQ-Explorer.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Detector saturation / dead-time effect at high count rates | Non-linear detector response during strong signal return, unique for each lidar/detector | Apply dead-time correction using vendor-supplied lookup table | (hb p. 11) |
| Afterpulse (detector noise induced by laser firing) | Near-field blind zone at the beginning of each sampling period; includes detector dark counts/dark noise related to thermal effects; minimum detection height on the order of 150 m, below... | Afterpulse correction performed quarterly by site operators, validated and uploaded for ingest by mentor | (hb p. 13) |
| Background noise from sunlight | Elevated background at 532 nm reducing signal-to-noise, especially during daytime | Background subtraction correction applied | (hb p. 11) |
| Near-field receiver efficiency loss (overlap) | Reduced or distorted signal at close range due to incomplete overlap between laser beam and telescope field of view | Overlap correction as function of range; historically performed by vendor, horizontal overlap calibration at SGP, in-field overlap calibration for... | (hb p. 11) |
| Low signal-to-noise for high, thin clouds during daytime | Difficulty detecting high thin clouds in daytime data due to low-power laser (less than ~25 mW) combined with solar background noise and atmospheric attenuation/extinction of beam | - | (hb p. 6) |
| Laser system degradation over time | Decreasing pulse power/sensitivity over the lifetime of the laser system, affecting detection sensitivity | - | (hb p. 7) |
| Cloud definition / algorithm sensitivity | Different cloud-detection algorithms may identify or miss the same atmospheric structure as a 'cloud', producing biases in reported cloud base height between products | - | (hb p. 7) |
| Minimum detectable cloud height limitation | Cannot reliably detect clouds below ~150 m due to afterpulse swamping the signal | - | (hb p. 13) |
| Timing/calibration uncertainty | ±2% uncertainty applied uniformly to all reported distances due to timing electronics calibration | - | (hb p. 12) |
| Range-bin quantization uncertainty | Cloud base heights centered within discrete range bins carry ±1/2 range resolution uncertainty (currently ±7.5 m at 15-m resolution; historically ±150 m at 300-m resolution) | - | (hb p. 12) |
| Aerosol retrieval products not operationally available | No standard ARM MPL aerosol retrieval datastream; users must rely on qualitative NRB (MPLNOR) profiles or limited NASA MPLNET products for aerosol layers | Use MPLNOR normalized backscatter profiles for qualitative aerosol indication; for b1-level data ensure overlap, dead-time, and afterpulse... | (hb p. 13) |
| Polarizer malfunction | Little/no difference between co-pol and cross-pol signal returns at all heights over several days | Notify mentor | (hb p. 18) |
| High depolarization value problems observed in field | Abnormally high depolarization ratio values recorded at specific deployments (e.g., MPL106, MPL4103 at MARCUS) | Instrument sent for evaluation/repair at Sigma Space | (hb p. 11) |
| Low laser output / degraded laser diode | Reduced laser output power (e.g., swap events showing low output in µJ or W in deployment log), unrealistic corrected signal peaks at nighttime, frequent energy level drops | Laser diode replacement, laser controller replacement, or return to vendor for repair | (hb p. 8) |
| Water intrusion damage | Instrument malfunction following extreme water intrusion event, requiring shipment to vendor for repair | Ship unit to Sigma Space for repair | (hb p. 9) |
| Liquid crystal (LC) module degradation | Switching between co-pol/cross-pol channels affected or not functioning; degraded LC performance noted during beta tests | LC replacement and alignment at vendor (Sigma Space) | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Distance-scale calibration uses a calibrated-pulse generator producing a trigger pulse and a delayed pulse with known time lag to mimic transmitted/backscattered pulses. Absolute signal magnitude calibration requires instrument-level corrections: dead-time correction, afterpulse correction, background subtraction,... (hb p. 11) |
| Calibration interval | Afterpulse and dark count correction procedures performed quarterly by site operators; overlap calibration historically performed by vendor after instrument evaluation/repair, occasionally performed at SGP by mentor/site operators; in-field overlap calibration for AMF deployments performed on an as-needed basis using... (hb p. 11) |
| Traceability | Dead-time correction lookup table provided by vendor with every new detector, unique to each lidar/detector (hb p. 11) |
| Routine maintenance | Routine cleaning of the viewport window and gentle cleaning of dust from the telescope; visual confirmation that the program is operating, that the clock is updating, and that displayed measurement agrees with reality. Co-pol and cross-pol signals should be compared: little cross-polarized signal expected from... (hb p. 18) |
| Maintenance interval | Daily and monthly preventative maintenance procedures designed by mentor (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ceilometer, radar, ARSCL (composite lidar+radar+ceilometer product).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM mobile facility |
| `ANL` | Argonne National Laboratory |
| `APD` | avalanche photodiode |
| `ARM` | Atmospheric Radiation Measurement |
| `ARSCL` | Active Remotely Sensed Cloud Locations |
| `ASI` | Ascension Island |
| `AWARE` | ARM West Antarctic Radiation Experiment |
| `CF` | Central Facility |
| `COMBLE` | Cold-Air Outbreaks in the Marine Boundary Layer Experiment |
| `CW` | continuous wave |
| `DQO` | Data Quality Office |
| `ENA` | Eastern North Atlantic |
| `FS` | fast switching |
| `ICECAPS` | Integrated Characterization of Energy, Clouds, Atmospheric State, and Precipitation over... |


### References the handbook cites

- Campbell, JR, DL Hlavka, EJ Welton, CJ Flynn, DD Turner, JD Spinhirne, and VS Scott. 2002. "Full-time Eye-Safe Cloud and Aerosol Lidar Observation at Atmospheric Radiation Measurement Program Sites: Instruments and Data...
- Spinhirne, JD. 1993. "Micro pulse lidar." IEEE Transactions on Geoscience and Remote Sensing 31(1): 48-55, https://doi.org/10.1109/36.210443
- Spinhirne, JD, JAR Rall, and VS Scott. 1995. "Compact eye safe lidar systems." Review of Laser Engineering 23(2): 112-118.
- Welton, EJ, JR Campbell, JD Spinhirne, and VS Scott. 2001. "Global monitoring of clouds and aerosols using a network of micropulse lidar systems." In Lidar Remote Sensing for Industry and Environment Monitoring 4153:...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/mpl_handbook.pdf (20 pages, DOE/SC-ARM-TR-019, by P Muradyan, R Coulter)
- Catalog record: ARM data-source index, `instrument_class_code=mpl`, read 2026-09-23
- Example file: `sgpminimplC1.b1.20260724.000003.nc` from `sgpminimplC1.b1`, 139.22 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
