---
name: arm-vap-thermocldphase
description: ARM Thermodynamic Cloud Phase (thermocldphase) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (cloud_phase_hsrl, cloud_phase_mplgr, cloud_phase_layer_hsrl, cloud_phase_layer_mplgr, qc_cloud_phase_hsrl, qc_cloud_phase_mplgr), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpthermocldphaseC1.c1) and the variable inventory of a real file. Use when working with thermocldphase data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - thermocldphase, Thermodynamic Cloud Phase, sgpthermocldphaseC1.c1, cloud_phase_hsrl, cloud_phase_mplgr, cloud_phase_layer_hsrl, cloud_phase_layer_mplgr, qc_cloud_phase_hsrl, Cloud Properties.
---

# THERMOCLDPHASE - Thermodynamic Cloud Phase

The THERMOCLDPHASE VAP provides vertically resolved thermodynamic cloud phase classifications (liquid, drizzle, liquid+drizzle, rain, ice, snow, or mixed-phase at pixel level, and liquid/mixed-phase/ice at cloud-layer level) derived from combined ARM lidar, radar, microwave radiometer and radiosonde datastreams at ARM fixed and mobile facility sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `thermocldphase` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-325 / D Zhang, MS Levin, MD Shupe, L Goldberger / October 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-325.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-01-18 to 2026-06-30 (retired) |
| Datastreams with data | 20 across 15 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/thermocldphase |


## Credit

Everything this skill knows about the retrieval is the work of **D Zhang, MS Levin, MD Shupe, L Goldberger** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Zhang, MS Levin, MD Shupe, L Goldberger. *ARM Thermodynamic Cloud Phase (THERMOCLDPHASE) Value-Added Product Report*, DOE/SC-ARM-TR-325, October 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-325.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm applies the multi-sensor methodology of Shupe (2007), combining lidar backscatter intensity (beta) and depolarization ratio (delta) from either HSRL or MPL, radar reflectivity (Ze), Doppler velocity (VD) and Doppler spectral width (WD) from KAZR/ARSCL, liquid water path (LWP) from MWR retrieval VAPs, and temperature (T) profiles from radiosonde-based INTERPSONDE, applying a sequence of threshold-based decision steps to each cloudy pixel identified by the ARSCL VAP to assign a hydrometeor phase category. Lidar backscatter is highly sensitive to small, high-concentration particles such as liquid droplets, while lidar depolarization helps identify nonspherical ice particles, though lidar signals attenuate rapidly in cloud. Radar reflectivity is dominated by larger particles such as ice crystals and is generally unaffected by attenuation except in strong precipitation. LWP from MWR further constrains the presence of liquid layers. The VAP also aggregates pixel-level phase over each of up to 10 ARSCL-identified cloud layers to classify the whole layer as liquid, mixed-phase, or ice based on the fraction of ice-containing pixels (frcice).

**Cadence.** output every 30 seconds temporal, 30 meters vertical (hb p. 9).

## Inputs

The report names these instruments and sibling products: MPLCMASK, HSRL, KAZRARSCL, INTERPSONDE, MWRRET, MWRRETv2, ARSCL.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| cloud_phase_hsrl | - | - | - | (hb p. 11) |
| cloud_phase_mplgr | - | - | - | (hb p. 11) |
| cloud_phase_layer_hsrl | - | liquid, mixed-phase, or ice per... | - | (hb p. 11) |
| cloud_phase_layer_mplgr | - | liquid, mixed-phase, or ice per... | - | (hb p. 11) |
| qc_cloud_phase_hsrl | bit-packed flag | - | - | (hb p. 11) |
| qc_cloud_phase_mplgr | bit-packed flag | - | - | (hb p. 11) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Temporal resolution | 30 seconds | (hb p. 9) |
| Vertical resolution | 30 meters | (hb p. 9) |
| Number of cloud layers identified | up to 10 distinct cloud layers | (hb p. 10) |
| Cloud layer phase thresholds (frcice) | Liquid: frcice less than  0.1; Mixed-phase: 0.1 less than = frcice less than = 0.9; Ice: frcice greater than  0.9 | (hb p. 10) |


## The data

Verified example: **`sgpthermocldphaseC1.c1`**, file `sgpthermocldphaseC1.c1.20140312.000000.nc`
(32.61 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=2880, `bound`=2, `layer`=10, `height`=596 |
| Data variables | 65 |
| QC variables | 26 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2014-03-12T00:00:00 to 2014-03-12T23:59:30 |
| dod version | thermocldphase-c1-4.3 |
| process version | thermocldphase-1.2.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cloud_phase_hsrl` | 1 | time,height | yes | Thermodynamic Cloud Phase (HSRL) |
| `cloud_phase_mplgr` | 1 | time,height | yes | Thermodynamic Cloud Phase (MPL Gradient) |
| `hsrl_atten_beta_r_backscatter` | 1/(m sr) | time,height | yes | HSRL Attenuated Molecular Return |
| `hsrl_b` | 1/(m sr) | time,height | yes | HSRL Particulate Backscatter Cross Section Per Unit Volume |
| `hsrl_beta_a` | 1/m | time,height | yes | HSRL Particulate Extinction Cross Section Per Unit Volume |
| `hsrl_depol` | 1 | time,height | yes | HSRL Circular Depolarization Ratio for Particulate |
| `mpl_b` | count/us | time,height | yes | MPL Total Attenuated Backscatter |
| `mpl_b_snr` | 1 | time,height | yes | MPL Signal to Noise Ratio of Backscatter |
| `mpl_background_signal` | count/us | time | yes | MPL Background Signal |
| `mpl_ldr` | 1 | time,height | yes | MPL Linear Depolarization Ratio |
| `mpl_ldr_snr` | 1 | time,height | yes | MPL Signal to Noise Ratio of Linear Depolarization Ratio |
| `mpl_overlap_correction` | 1 | height | yes | MPL Overlap Correction |
| `mwr_lwp_be` | g/m^2 | time | yes | MWR Best-Estimate Liquid Water Path |
| `mwr_pwv_be` | cm | time | yes | MWR Best-Estimate Precipitable Water Vapor |
| `radar_cloud_source_flag` | 1 | time,height | yes | Instrument source flag for cloud (hydrometeor) detections |
| `radar_ldr` | dBZ | time,height | yes | Radar Linear Depolarization Ratio |
| `radar_mdv` | m/s | time,height | yes | Radar Mean Doppler Velocity |
| `radar_precip_mean` | mm/hr | time | yes | Radar Precipitation Mean |
| `radar_snr` | dB | time,height | yes | Radar Signal-to-Noise Ratio |
| `radar_w` | m/s | time,height | yes | Radar Spectral Width |
| `radar_ze` | dBZ | time,height | yes | Radar Best-Estimate Reflectivity |
| `sonde_bar_pres` | kPa | time,height | yes | Sonde Barometric Pressure |
| `sonde_rh` | % | time,height | yes | Sonde Relative Humidity |
| `sonde_temp` | degC | time,height | yes | Sonde Temperature |
| `sonde_wdir` | degree | time,height | yes | Sonde Wind Direction |
| `sonde_wspd` | m s-1 | time,height | yes | Sonde Wind Speed |
| `cloud_layer_heights` | km | time,layer,bound | - | Base and top heights of hydrometeor layers for up to 10 layers, based... |
| `cloud_mask` | 1 | time,height | - | Cloud Mask |
| `cloud_phase_layer_hsrl` | 1 | time,layer | - | Thermodynamic Cloud Phase Layer (HSRL) |
| `cloud_phase_layer_mplgr` | 1 | time,layer | - | Thermodynamic Cloud Phase Layer (MPL Gradient) |


_6 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "sgpthermocldphaseC1.c1",
                             "start": "2014-03-12", "end": "2014-03-12", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpthermocldphaseC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpthermocldphaseC1.c1", "2014-03-12", "2014-03-12")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpthermocldphaseC1.c1", "2014-03-12", "2014-03-12"))   # cite what you pulled
```

This product carries 65 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpthermocldphaseC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['cloud_phase_hsrl', 'cloud_phase_mplgr', 'hsrl_atten_beta_r_backscatter', 'qc_cloud_phase_hsrl', 'qc_cloud_phase_mplgr', 'qc_hsrl_atten_beta_r_backscatter'],
                                cleanup_qc=True)
```

## Quality control in this product

26 `qc_` companion variables cover 26 of the
65 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_cloud_phase_mplgr"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("cloud_phase_mplgr", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["cloud_phase_mplgr", "cloud_phase_hsrl", "mpl_b"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpthermocldphaseC1.c1.20140312.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cloud_phase_hsrl` | Value is equal to missing_value | 1716480 | 100.0 |
| `hsrl_b` | Transformation could not finish (all values bad or outside... | 1716480 | 100.0 |
| `hsrl_atten_beta_r_backscatter` | Transformation could not finish (all values bad or outside... | 1716480 | 100.0 |
| `hsrl_depol` | Transformation could not finish (all values bad or outside... | 1716480 | 100.0 |
| `hsrl_beta_a` | Transformation could not finish (all values bad or outside... | 1716480 | 100.0 |
| `radar_ze` | Transformation could not finish (all values bad or outside... | 1695665 | 98.7873 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpthermocldphaseC1.c1", "20110118", "20260924")
```

The report's own note on quality: If any required input variables are flagged as missing_value, a QC flag is assigned and the affected pixels are classified as unknown. If LWP input data sets (from MWRRET or MWRRETv2) are unavailable, a QC flag is assigned indicating that no LWP constraint was applied. Output variables qc_cloud_phase_hsrl and qc_cloud_phase_mplgr are bit-packed quality checks: bit 1 = value equal to missing_value, bit 2 = temperature data not available, bit 3 = liquid water path data not available. If any required input data set is not available for the entire day, the VAP does not produce an output data set...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Lidar signal attenuation by cloud droplets | Lidar backscatter and depolarization signals rapidly attenuated, limiting phase information above liquid-dominated layers | Combine with radar, which is generally unaffected by attenuation except in strong precipitation | (hb p. 7) |
| Radar attenuation in strong precipitation | Reduced or missing reflectivity/Doppler signal during heavy precipitation events | - | (hb p. 7) |
| HSRL limited availability | cloud_phase_hsrl and cloud_phase_layer_hsrl variables absent from output when HSRL data are not available at a given site or during an AMF deployment | Use MPL-derived cloud_phase_mplgr classification instead, since ARM operates only three HSRL units at limited fixed sites or during AMF campaigns | (hb p. 10) |
| MPL provides only relative backscatter intensity (not absolutely calibrated) | cloud_phase_mplgr classification relies on vertical gradient strength in backscattered signal rather than absolute beta values, differing methodologically from HSRL-based classification | Differentiates liquid/ice by analyzing strength of vertical gradient in backscattered signal (Wang and Sassen 2001) | (hb p. 10) |
| Missing/unavailable input data flagged as missing_value | Affected pixels classified as "unknown" and a QC flag assigned | QC flag assigned to indicate missing input; pixel classified unknown | (hb p. 11) |
| Unavailable LWP data from MWRRET/MWRRETv2 | No liquid water path constraint applied to phase classification for affected periods | QC flag assigned to indicate that no LWP constraint was applied | (hb p. 11) |
| Missing input datastream for entire processing day | No THERMOCLDPHASE output file produced for that day | None stated beyond non-production of output | (hb p. 11) |
| "Unknown" phase classification when result is inconsistent with known cloud physics | Pixel labeled unknown despite non-missing inputs, when classification conflicts with established understanding of cloud structure/physics | - | (hb p. 7) |
| Threshold values derived from Arctic climatology | Classification thresholds may be inappropriate/inaccurate when applied outside middle/high-latitude Arctic conditions | Handbook states thresholds will need review and update according to local cloud climatology before extending VAP to low-latitude sites | (hb p. 10) |
| Full attenuation of both lidar and radar in deep convective clouds | Loss of phase classification capability (no usable signal) in strongly convective cloud columns | Noted as a challenge for this classification method; no specific mitigation given | (hb p. 10) |
| Radar reflectivity calibration offset at NSA | Slightly more snow pixels identified compared to original Shupe (2007) implementation | Applied radar reflectivity offset correction of ~4 dBZ recommended by Kollias et al. (2019) | (hb p. 12) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Shupe, MD. 2007. "A ground-based multisensor cloud phase classifier." Geophysical Research Letters 34(22): L22809
- Clothiaux et al. 2001. The ARM Millimeter Wave Cloud Radars (MMCRs) and the ARSCL VAP. ARM VAP-002.1
- Johnson, KL, SE Giangrande, and A Zhou. 2022. KAZR ARSCL CloudSat Calibration VAP Report. DOE/SC-ARM-TR-279
- Fairless, T, M Jensen, A Zhou, and SE Giangrande. 2021. Interpolated Sounding and Gridded Sounding VAPs. DOE/SC-ARM-TR-183
- Flynn, D, C Sivaraman, J Comstock, and D Zhang. 2020. MPLCMASK VAP Technical Report. DOE/SC-ARM-TR-098
- Gaustad, KL, DD Turner, and SA McFarlane. 2011. MWRRET VAP. DOE/SC-ARM-TR-081.2
- Zhang, D, LD Riihimaki, KL Gaustad, and DD Turner. 2020. MWRRETV2 VAP Report. DOE/SC-ARM-TR-245
- Bambha, R, J Garcia, I Razenkov, and E Eloranta. 2025. HSRL Instrument Handbook. DOE/SC-ARM-TR-157
- Kollias, P, B Puigdomenech Treserras, and A Protat. 2019. Calibration of the 2007-2017 record of ARM cloud radar observations using CloudSat. AMT 12(9): 4949-4964
- Wang, Z, and K Sassen. 2001. Cloud Type and Macrophysical Property Retrieval Using Multiple Remote Sensors. JAM 40(10): 1665-1682

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-325.pdf (17 pages, DOE/SC-ARM-TR-325, by D Zhang, MS Levin, MD Shupe, L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=thermocldphase`, read 2026-09-24
- Example file: `sgpthermocldphaseC1.c1.20140312.000000.nc` from `sgpthermocldphaseC1.c1`, 32.61 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
