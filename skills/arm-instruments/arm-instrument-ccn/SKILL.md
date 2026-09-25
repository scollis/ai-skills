---
name: arm-instrument-ccn
description: ARM Cloud Condensation Nuclei Particle Counter (ccn) - handbook-derived instrument reference. Measurement principle, reported quantities (Activated aerosol particle size, Supersaturation, Sample flow rate, Sample air pressure, Sample temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaosccn1colspectraC1.b1) and the variable inventory of a real file. Use when working with ccn data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - ccn, Cloud Condensation Nuclei Particle Counter, sgpaosccn1colspectraC1.b1, Activated aerosol particle size, Supersaturation, Sample flow rate, Sample air pressure, Sample temperature, Aerosols, Droplet Measurement Technologies, Inc., NIST, SMPS.
---

# CCN - Cloud Condensation Nuclei Particle Counter

The CCN measures the number concentration and size of aerosol particles that activate into droplets as a function of controlled supersaturation, deployed as a continuous-flow thermal-gradient diffusion chamber at ARM ground and mobile sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ccn` |
| Handbook | [DOE/SC-ARM-TR-168 / J Uin, OY Enekwizu / April 2024](https://www.arm.gov/publications/tech_reports/handbooks/ccn_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Droplet Measurement Technologies, Inc.; Model CCN-100 or CCN-200 |
| Primary measurements | Aerosol concentration; Cloud condensation nuclei |
| Record | 2005-03-04 to 2026-09-23 (active) |
| Datastreams with data | 123 across 29 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/ccn |


## Credit

Everything this skill knows about the instrument is the work of **J Uin, OY Enekwizu** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> J Uin, OY Enekwizu. *Cloud Condensation Nuclei Particle Counter Instrument Handbook*, DOE/SC-ARM-TR-168, April 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ccn_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The CCN counter is a continuous-flow, thermal-gradient diffusion chamber for measuring aerosols that can act as cloud condensation nuclei. The CCN draws an aerosol sample into a column where a thermodynamically unstable, supersaturated water vapor condition is created by taking advantage of the difference in diffusion rates between water vapor and heat, with water vapor diffusing from the warm, wet column walls toward the centerline faster than heat. The wall temperature along the column gradually increases to create a well-controlled and quasi-uniform centerline supersaturation. Seeking equilibrium, the supersaturated water vapor condenses on the cloud condensation nuclei in the sample air to form droplets, just as cloud drops form in the atmosphere. An optical particle counter using side-scattering technology counts and sizes the activated droplets.

**Siting.** Coefficients from a calibration done at similar conditions (altitude) as the measurement location should be used, since the relationship between CCN column temperature gradient and supersaturation is sensitive to ambient pressure. The supersaturation scanning schedule is typically chosen to fit a particular measurement location because aerosol particle properties can vary by location and reach 100% activation at different supersaturation values.

**Sampling.** native rate typically every second; reported every new data file started every hour and every time system is restarted (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Activated aerosol particle size | micrometers (µm) | 0.75-10 µm | approximately ±0.25 µm | - | (hb p. 11) |
| Activated aerosol particle number concentration | particles per cubic... | up to 6000 s-1 at SS below 0.2%; up to... | within 4% for the operating ranges specified | - | (hb p. 11) |
| Supersaturation | % (dimensionless) | 0.07% to 2.0% | within 3% above 0.1% SS; as low as 40% below... | - | (hb p. 11) |
| Sample flow rate | - | - | - | - | (hb p. 8) |
| Sample air pressure | - | - | - | - | (hb p. 8) |
| Sample temperature | - | - | - | - | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Supersaturation range | 0.07% to 2.0% | (hb p. 11) |
| Particle size range (after activation) | 0.75-10 µm | (hb p. 11) |
| Particle number concentration range at SS below 0.2% | maximum 6000 s-1 | (hb p. 11) |
| Particle number concentration range at SS above 0.3% | maximum 20000 s-1 | (hb p. 11) |
| Accuracy of supersaturation control (above 0.1% SS) | within 3% | (hb p. 11) |
| Accuracy of supersaturation control (below 0.1% SS) | as low as 40% | (hb p. 11) |
| Accuracy of single-particle counting | within 4% | (hb p. 11) |
| Repeatability of supersaturation control (laboratory) | ±1% | (hb p. 11) |
| Repeatability of supersaturation control (field) | ±5% | (hb p. 11) |
| Uncertainty of activated particle sizing | approximately ±0.25 µm | (hb p. 12) |
| Sheath/sample flow rate ratio (QC criterion) | between 9.5 and 10.5 | (hb p. 10) |
| OPC first-stage voltage monitor reading (QC criterion) | below 0.2 V | (hb p. 10) |
| Laser safety classification | Class IIIb Laser Product | (hb p. 14) |


## The data

Verified example: **`sgpaosccn1colspectraC1.b1`**, file `sgpaosccn1colspectraC1.b1.20170813.000300.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=24, `bound`=2, `supersaturation_setpoint`=7, `polynomial_order`=3 |
| Data variables | 16 |
| QC variables | 2 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2017-08-13T00:03:00 to 2017-08-13T23:03:00 |
| sampling interval | 1 second |
| averaging interval | 1 minute |
| dod version | aosccn1colspectra-b1-1.2 |
| process version | ingest-aosccn1colspectra-1.3-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `N_CCN` | 1/cm^3 | time,supersaturation_setpoint | yes | Mean number concentration of activated condensation nuclei |
| `f_CCN` | unitless | time,supersaturation_setpoint | yes | Ratio of N_CCN to concentration |
| `N_CCN_fit_coefs` | unitless | time,polynomial_order | - | Coefficients for quadratic fit of N_CCN vs supersaturation |
| `N_CCN_fit_error` | 1/cm^3 | time,supersaturation_setpoint | - | Absolute relative error between N_CCN measurement and fit |
| `N_CCN_fit_value` | 1/cm^3 | time,supersaturation_setpoint | - | Fitted value of N_CCN versus calculated supersaturation |
| `concentration` | 1/cm^3 | time,supersaturation_setpoint | - | Aerosol concentration averaged over times to match N_CCN |
| `setpoint_time` | s | time,supersaturation_setpoint | - | Supersaturation setpoint start time, relative to midnight |
| `supersaturation_calculated` | % | time,supersaturation_setpoint | - | Mean supersaturation_calculated at times to match... |
| `supersaturation_setpoint` | % | supersaturation_setpoint | - | Supersaturation set point |
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
                     params={"user": f"{user}:{token}", "ds": "sgpaosccn1colspectraC1.b1",
                             "start": "2017-08-13", "end": "2017-08-13", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaosccn1colspectraC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaosccn1colspectraC1.b1", "2017-08-13", "2017-08-13")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaosccn1colspectraC1.b1", "2017-08-13", "2017-08-13"))   # cite what you pulled
```

## Quality control in this datastream

2 `qc_` companion variables cover 2 of the
16 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_N_CCN"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("N_CCN", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["N_CCN", "f_CCN"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaosccn1colspectraC1.b1.20170813.000300.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `f_CCN` | value is equal to missing_value | 168 | 100.0 |
| `N_CCN` | N_CCN_modeled_error value greater than  20% | 5 | 2.9762 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaosccn1colspectraC1.b1", "20050304", "20260923")
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging of data based on criteria developed by instrument mentors and automatic generation of plots in collaboration with the ARM Data Quality Office. Automatic checks include verifying sheath/sample flow rate ratio is between 9.5 and 10.5, and that the OPC first-stage voltage monitor reading is below 0.2 V. Particle number concentration data at 0% supersaturation set point are automatically flagged 'bad' to exclude from analysis (no meaningful information at 0% SS; not indicative of instrument problems). Automatically generated plots include...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Zero supersaturation data flagged as bad | Particle number concentration data at supersaturation set point of 0% are automatically flagged 'bad' in the data files | Flag excludes these data from further processing/analysis; this flag does not indicate any instrument operation issues | (hb p. 10) |
| Non-linear supersaturation dependence below 0.1% SS | Supersaturation accuracy can be as low as 40% at SS below 0.1% | Must be accounted for in instrument calibration and data interpretation; by default it is not accounted for | (hb p. 11) |
| Particle coincidence at high concentrations | Aerosol particle size and concentration measurements become inaccurate above growth-kinetics-limited counting rates (6000 s-1 below 0.2% SS, 20000 s-1 above 0.3% SS) | Growth kinetics of the particles in the CCN column set the upper limit of total particle counts for accurate single-particle detection | (hb p. 11) |
| Sensitivity of SS-to-ΔT relationship to ambient pressure | Reported supersaturation drifts from true value if calibration altitude differs from deployment altitude | Use calibration coefficients from a calibration done at similar conditions (altitude) as the measurement location; raw data can be corrected for... | (hb p. 11) |
| Field repeatability degradation | Repeatability of supersaturation control increases from ±1% (laboratory) to ±5% (field) | Attributed to fluctuations of ambient temperature | (hb p. 11) |
| OPC malfunction / low or noisy counts | Low counts or noisy signal in particle size distribution plot of activated aerosols vs time | May indicate issues with the OPC; checked via automatic QC plot | (hb p. 10) |
| CCN column malfunction | Lack of clear step-wise change in total activated particle number concentration with changing humidifier supersaturation | May indicate an issue with the CCN column | (hb p. 10) |
| Sample line blockage or failing pump | Low or unstable sample flow rate | Checked via automatic QC plot of sample flow rate | (hb p. 10) |
| Failing OPC (laser/reference voltage) | High laser current and reference voltage | Checked via automatic QC plot of laser current and reference voltage | (hb p. 10) |
| Algae contamination in water system | Green algae observed in wastewater upon inspection of drain bottle | Clean the CCN water system if algae is present | (hb p. 13) |
| Dry column startup delay | OPC does not register counts for 4 to 12 hours after dry startup while CCN column is being wetted | Perform dry startup procedure (Dry Start Up button) and wait for column to become properly wetted; green status light indicates proper function | (hb p. 7) |
| Improper water supply contamination | Use of tap water or purified water with added minerals instead of distilled water may affect column performance | Fill supply bottle with distilled water only; tap water or purified water with added minerals is not OK | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Generating and size-selecting ammonium sulfate particles and recording their total number concentration before and after activation in the CCN as a function of particle size, for several column temperature gradients (ΔT); 50% activation diameter (D50) is calculated for each ΔT and supersaturation (%SS) is calculated... (hb p. 10) |
| Calibration interval | Instrument mentors typically perform calibration before and after each deployment, and during deployment if more than a year has passed since the last calibration and the deployment is not yet ending; schedule is flexible depending on availability of calibration SMPS. (hb p. 10) |
| Traceability | NIST-traceable polystyrene latex (PSL) particles for OPC size calibration (hb p. 10) |
| Routine maintenance | Adding distilled water to the CCN fill bottle; emptying the CCN drain bottle and inspecting wastewater for presence of green algae (clean CCN water system if algae present); emptying the CCN water trap bottles as needed when water is present. (hb p. 13) |
| Maintenance interval | Fill bottle: every day; drain bottle: every time fill bottle is filled; water trap bottles: as needed (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SMPS (scanning mobility particle sizer, used for calibration).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `CCN` | cloud condensation nuclei counter |
| `DOE` | U.S. Department of Energy |
| `NIST` | National Institute of Standards and Technology |
| `OPC` | optical particle counter |
| `OSS` | Operation Status System |
| `PC` | personal computer |
| `PSL` | polystyrene latex |
| `SMPS` | scanning mobility particle sizer |
| `SS` | supersaturation |
| `USB` | universal serial bus |
| `VGA` | video graphics array |


### References the handbook cites

- Roberts, GC, and Nenes, A. 2005. "A Continuous-Flow Streamwise Thermal-Gradient CCN Chamber for Atmospheric Measurements." Aerosol Science and Technology 39(3): 206−221, http://doi.org/10.1080/027868290913988
- Rose, D, GP Frank, U Dusek, SS Gunthe, MO Andreae, and U Pöschl. 2007. "Calibration and measurement uncertainties of a continuous-flow cloud condensation nuclei counter (DMT-CCNC): CCN activation of ammonium sulfate and...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ccn_handbook.pdf (15 pages, DOE/SC-ARM-TR-168, by J Uin, OY Enekwizu)
- Catalog record: ARM data-source index, `instrument_class_code=ccn`, read 2026-09-23
- Example file: `sgpaosccn1colspectraC1.b1.20170813.000300.nc` from `sgpaosccn1colspectraC1.b1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
