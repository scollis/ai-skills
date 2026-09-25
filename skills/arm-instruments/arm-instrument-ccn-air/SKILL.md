---
name: arm-instrument-ccn-air
description: ARM Cloud Condensation Nuclei Particle Counter aboard Aircraft (ccn-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol particle size, Supersaturation, Sample flow rate, Sample air pressure, Sample temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafccn2colbF1.b1) and the variable inventory of a real file. Use when working with ccn-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - ccn-air, Cloud Condensation Nuclei Particle Counter aboard Aircraft, sgpaafccn2colbF1.b1, Aerosol particle size, Supersaturation, Sample flow rate, Sample air pressure, Sample temperature, Aerosols, Airborne Observations, Droplet Measurement Technologies, Inc., ACE-ENA, NIST, SMPS.
---

# CCN-AIR - Cloud Condensation Nuclei Particle Counter aboard Aircraft

The CCN Counter is a continuous-flow thermal-gradient diffusion chamber that measures the concentration and size of aerosol particles activated as cloud condensation nuclei as a function of supersaturation, deployed aboard research aircraft.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ccn-air` |
| Handbook | [DOE/SC-ARM-TR-225 / J Uin, F Mei / September 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-225.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Droplet Measurement Technologies, Inc.; Model CCN-100 or CCN-200 |
| Primary measurements | Cloud condensation nuclei; Navigation variables |
| Record | 2013-07-10 to 2026-09-23 (retired) |
| Datastreams with data | 18 across 6 sites |
| Sites | acx, cor, ena, mao, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/ccn-air |


## Credit

Everything this skill knows about the instrument is the work of **J Uin, F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin, F Mei. *Cloud Condensation Nuclei Particle Counter Instrument Handbook – Airborne Version*, DOE/SC-ARM-TR-225, September 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-225.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The CCN counter is a continuous-flow, thermal-gradient diffusion chamber for measuring aerosols that can act as cloud condensation nuclei. The CCN draws an aerosol sample into a column, where a thermodynamically unstable, supersaturated water vapor condition is created by taking advantage of the difference in diffusion rates between water vapor and heat, since water vapor diffuses from the warm, wet column walls toward the centerline faster than heat. The wall temperature along the column gradually increases to create a well-controlled and quasi-uniform centerline supersaturation. Seeking equilibrium, the supersaturated water vapor condenses on the cloud condensation nuclei in the sample air to form droplets, just as cloud drops form in the atmosphere. An OPC using side-scattering technology counts and sizes the activated droplets.

**Sampling.** native rate typically every second; reported every new data file started every hour and every time the system is restarted (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle size (activated/humidified) | micrometers (μm) | 0.75-10 μm | approximately ±0.25 μm (sizing resolution of... | - | (hb p. 13) |
| Aerosol particle number concentration | particles per cubic... | max 6000 s-1 at SS below 0.2%; max... | within 4% for the operating ranges specified | - | (hb p. 13) |
| Supersaturation (SS) | % (dimensionless) | 0.07% to 2.0% | within 3% above SS 0.1%; as low as 40% below SS... | - | (hb p. 13) |
| Sample flow rate | - | - | - | - | (hb p. 8) |
| Sample air pressure | - | - | - | - | (hb p. 8) |
| Sample temperature | - | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Aerosol particle size units | micrometers (μm) | (hb p. 13) |
| Aerosol particle number concentration units | particles per cubic centimeter (cm-3) or raw number of counts (dimensionless) | (hb p. 13) |
| Supersaturation units | % (dimensionless) | (hb p. 13) |
| Supersaturation range | 0.07% to 2.0% | (hb p. 13) |
| Particle size range (after humidification) | 0.75-10 μm | (hb p. 13) |
| Particle number concentration max (SS below 0.2%) | 6000 s-1 | (hb p. 13) |
| Particle number concentration max (SS above 0.3%) | 20000 s-1 | (hb p. 13) |
| Accuracy of supersaturation (SS above 0.1%) | within 3% | (hb p. 13) |
| Accuracy of supersaturation (SS below 0.1%, not corrected) | as low as 40% | (hb p. 13) |
| Accuracy of single particle counting | within 4% | (hb p. 13) |
| Repeatability of supersaturation control (laboratory) | ±1% | (hb p. 13) |
| Repeatability of supersaturation control (field) | ±5% | (hb p. 13) |
| Uncertainty of activated particle sizing | approximately ±0.25 μm | (hb p. 14) |
| Laser safety classification | Class IIIb Laser Products | (hb p. 17) |


## The data

Verified example: **`sgpaafccn2colbF1.b1`**, file `sgpaafccn2colbF1.b1.20160921.163352.nc`
(2.05 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=7949, `droplet_size`=20, `bound`=2, `n_lookup`=100 |
| Data variables | 42 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-21T16:33:52 to 2016-09-21T19:04:42 |
| sampling interval | 1 second |
| dod version | aafccn2colb-b1-1.1 |
| process version | ingest-aafccn200corr-2.0-4.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `N_CCN` | 1/cm^3 | time | yes | Number concentration of CCN |
| `N_CCN_dN` | count/s | time,droplet_size | - | Droplet count by bin size |
| `P_sample` | hPa | time | - | Sample pressure |
| `Q_sample` | cm^3/min | time | - | Volumetric flow rate of sample air |
| `Q_sheath` | cm^3/min | time | - | Volumetric flow rate of sheath air |
| `T_OPC` | degC | time | - | Temperature read of the optical particle counter |
| `T_inlet` | degC | time | - | Temperature read of sample air at entrance to instrument |
| `T_nafion` | degC | time | - | Nafion temperature |
| `T_read_TEC1` | degC | time | - | Temperature read at top of column |
| `T_read_TEC2` | degC | time | - | Temperature read at middle of column |
| `T_read_TEC3` | degC | time | - | Temperature read at bottom of column |
| `T_read_gradient` | degC | time | - | Temperature difference between T_read_TEC3 and T_read_TEC1 |
| `T_sample` | degC | time | - | Temperature read of sample air entering the column |
| `T_set_TEC1` | degC | time | - | Temperature set point at top of column |
| `T_set_TEC2` | degC | time | - | Temperature set point at middle of column |
| `T_set_TEC3` | degC | time | - | Temperature set point at bottom of column |
| `T_set_gradient` | degC | time | - | Temperature difference between T_set_TEC3 and T_set_TEC1 |
| `dT_OPC` | degC | time | - | T_OPC - T_read_TEC3 temperature difference |
| `dT_target_estimated` | degC | time | - | Estimated target thermal gradient under current operating conditions |
| `droplet_size` | um | droplet_size | - | Size bins for CCN droplet count |
| `eta` | unitless | time | - | Eta factor used in calculation of supersaturation_calculated |
| `eta_lookup_table` | unitless | n_lookup,bound | - | Lookup table for eta computation |
| `eta_target` | unitless | time | - | Eta factor used in calculation of... |
| `first_bin_used` | unitless | time | - | First bin used in N_CCN calculation |
| `first_stage_monitor_voltage` | V | time | - | First stage monitor voltage |
| `laser_current` | mA | time | - | OPC laser current |
| `overflow` | count | time | - | Number of particles that are larger than 10um |
| `proportional_valve_voltage` | V | time | - | CCN Proportional valve voltage |
| `reported_temperature_gradient` | degC | time | - | Reported temperature difference between T_set_TEC3 and T_set_TEC1 |
| `supersaturation_calculated` | % | time | - | Sample supersaturation calculated via Lance/Rose method |


_4 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpaafccn2colbF1.b1",
                             "start": "2016-09-21", "end": "2016-09-21", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaafccn2colbF1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaafccn2colbF1.b1", "2016-09-21", "2016-09-21")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaafccn2colbF1.b1", "2016-09-21", "2016-09-21"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("reported_temperature_gradient")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This datastream carries 42 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpaafccn2colbF1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["N_CCN", "lat", "lon", "qc_N_CCN", "qc_lat", "qc_lon"],
                                cleanup_qc=True)
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
42 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_N_CCN"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("N_CCN", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["N_CCN", "lat", "lon"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaafccn2colbF1.b1.20160921.163352.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `N_CCN` | abs(supersaturation_calculated_target -... | 1949 | 24.5188 |
| `N_CCN` | first_stage_monitor_voltage less than ... | 420 | 5.2837 |
| `N_CCN` | first_stage_monitor_voltage greater than ... | 403 | 5.0698 |
| `N_CCN` | dT_OPC less than  dT_OPC_min_alarm OR dT_OPC greater than ... | 380 | 4.7805 |
| `N_CCN` | temperature_std greater than  temperature_std_alarm | 379 | 4.7679 |
| `N_CCN` | Value is less than the fail_min. | 135 | 1.6983 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaafccn2colbF1.b1", "20130710", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging of data based on criteria developed by instrument mentors and automatic generation of plots in collaboration with the ARM Data Quality Office. Automatic checks include verifying sheath/sample flow rate ratio is between 9.5 and 10.5, and that the OPC first-stage voltage monitor reading is below 0.5 V. Automatically generated plots include aerosol particle size distribution vs time, total number concentration of humidified particles vs time, sample flow rate, and laser current/reference voltage, each used to flag potential instrument issues as...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Non-linear supersaturation dependence below 0.1% SS | Supersaturation accuracy can be as low as 40% at SS below 0.1% if the non-linear dependence on humidifier column temperature gradient is not accounted for in calibration/data interpretation... | Account for non-linearity in instrument calibration and data interpretation (not done by default) | (hb p. 13) |
| Particle coincidence at high concentrations | Aerosol particle size and concentration measurements become inaccurate at higher particle concentrations due to particle coincidence during counting; upper limit for accurate... | Stay within stated concentration limits for accurate single-particle detection | (hb p. 13) |
| Pressure sensitivity of supersaturation-temperature gradient relationship | Relationship between humidifier column temperature gradient and supersaturation % varies with ambient pressure (altitude), leading to inaccurate supersaturation reporting if wrong... | Use calibration coefficients obtained at similar conditions (altitude) to the measurement location | (hb p. 13) |
| OPC sizing resolution limit | Activated particle sizing shows uncertainty of approximately ±0.25 μm due to OPC sizing resolution | - | (hb p. 14) |
| Sheath/sample flow ratio out of range | Sheath/sample flow rate ratio deviates from the 9.5-10.5 acceptable range, flagged in automatic QC | Automatic flagging by data quality checks; investigate flow system | (hb p. 12) |
| OPC first-stage voltage monitor high reading | OPC first-stage voltage monitor reading exceeds 0.5 V, indicating improper OPC operation | Automatic flagging by data quality checks | (hb p. 12) |
| OPC malfunction / noisy signal | Low counts or noisy signal in aerosol particle size distribution vs time plot may indicate issues with the OPC | Reviewed via automatically generated plots by ARM Data Quality Office | (hb p. 12) |
| Humidifier column issue | Lack of clear step-wise change in particle concentration with changing humidifier supersaturation in total number concentration plot may indicate an issue with the humidifier column | Reviewed via automatically generated plots by ARM Data Quality Office | (hb p. 12) |
| Sample line blockage or failing pump | Low or unstable sample flow rate | Reviewed via automatically generated flow rate plots | (hb p. 12) |
| Failing OPC (laser/reference issue) | High laser current and reference voltage indicate a failing OPC | Reviewed via automatically generated plots | (hb p. 12) |
| Algae contamination in water system | Presence of green algae observed in waste water from drain bottle inspection | Clean the CCN water system if algae is present | (hb p. 17) |
| Dry column startup delay | After dry startup, it may take 4 to 12 hours for the CCN to become properly humidified and count particles; OPC will not be counting properly during this period | Perform dry startup procedure and wait for humidifier column to be fully wetted (status light turns green when functioning properly) | (hb p. 16) |
| Improper water supply contamination | Use of tap water or purified water with added minerals instead of distilled water could affect humidifier column performance | Fill supply bottle with distilled water only, not tap water or mineral-added purified water | (hb p. 16) |
| Calibration drift over time / long-term eta changes | Monitoring long-term thermal efficiency (eta) values reveals drifts in overall CCN column performance | Real-time calibration approach corrects for pressure, flow, and supersaturation drifts using mentor-provided calibrations during data ingest;... | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Manufacturer calibration includes supersaturation calibration with ammonium sulfate aerosol particles, size calibration of the OPC with NIST-traceable polystyrene latex (PSL) particles, and flow calibrations with a precision flow meter. Mentor calibration involves generating and size-selecting ammonium sulfate... (hb p. 16) |
| Calibration interval | Calibrated by manufacturer before delivery and during instrument maintenance; instrument mentors typically perform calibration before and after each deployment at conditions (altitude) similar to the measurement site, and during deployment if more than a year since the last calibration and deployment is not yet... (hb p. 16) |
| Traceability | NIST-traceable polystyrene latex (PSL) particles for OPC size calibration (hb p. 16) |
| Routine maintenance | Adding distilled water to the CCN fill bottle; emptying the CCN drain bottle and inspecting waste water for green algae (clean water system if algae present); emptying the CCN water trap bottles as needed when water is present. (hb p. 17) |
| Maintenance interval | Fill bottle: every day. Drain bottle: every time the fill bottle is filled. Water trap bottles: as needed. (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Ground version of CCN counter (DOE/SC-ARM-TR-168), SMPS (calibration scanning mobility particle sizer spectrometer).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `CCN` | cloud condensation nuclei counter |
| `DOE` | U.S. Department of Energy |
| `NIST` | National Institute of Standards and Technology |
| `OPC` | optical particle counter |
| `OSS` | Operation Status System |
| `PC` | personal computer |
| `SMPS` | scanning mobility particle sizer spectrometer |
| `SS` | supersaturation |
| `USB` | Universal Serial Bus |
| `UTC` | Coordinated Universal Time |
| `VGA` | video graphics array |


### References the handbook cites

- Roberts, GC, and Nenes, A. 2005. "A Continuous-Flow Streamwise Thermal-Gradient CCN Chamber for Atmospheric Measurements." Aerosol Science and Technology 39(3): 206–221, http://doi.org/10.1080/027868290913988
- Rose, D, GP Frank, U Dusek, SS Gunthe, MO Andreae, and U Pöschl, 2007. "Calibration and measurement uncertainties of a continuous-flow cloud condensation nuclei counter (DMT-CCNC): CCN activation of ammonium sulfate and...
- Raatikainen, T, JJ Lin, KM Cerully, TL Lathem, RH Moore, and A Nenes. 2014. "CCN data interpretation under dynamic operation conditions." Aerosol Science and Technology 48(5): 552–561,...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-225.pdf (18 pages, DOE/SC-ARM-TR-225, by J Uin, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=ccn-air`, read 2026-09-23
- Example file: `sgpaafccn2colbF1.b1.20160921.163352.nc` from `sgpaafccn2colbF1.b1`, 2.05 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
