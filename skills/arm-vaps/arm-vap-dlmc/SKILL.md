---
name: arm-vap-dlmc
description: ARM Doppler Lidar Mentor Corrected for Ship Motion (dlmc) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (range, azimuth, elevation, radial_velocity, intensity, attenuated_backscatter), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (mosdlmcusrM1.c1) and the variable inventory of a real file. Use when working with dlmc data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - dlmc, Doppler Lidar Mentor Corrected for Ship Motion, mosdlmcusrM1.c1, range, azimuth, elevation, radial_velocity, intensity, Cloud Properties.
---

# DLMC - Doppler Lidar Mentor Corrected for Ship Motion

The DLMC VAP combines raw Doppler lidar (DL) beam and radial velocity data with simultaneous ARM Navigation (NAV) system attitude and velocity measurements to transform ship-based Doppler lidar beam angles into an Earth-fixed coordinate system and remove the contribution of platform (ship) motion from the lidar's radial velocity measurements.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 16 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `dlmc` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-296 / R Newsom, G Gibler, K Gaustad, D Zhang / February 2024](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-296.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2019-10-11 to 2020-09-20 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/dlmc |


## Credit

Everything this skill knows about the retrieval is the work of **R Newsom, G Gibler, K Gaustad, D Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> R Newsom, G Gibler, K Gaustad, D Zhang. *Doppler Lidar Motion-Correction (DLMC) Value-Added Product Report*, DOE/SC-ARM-TR-296, February 2024.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-296.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

In ship-based Doppler lidar deployments the lidar's heading and tilt are constantly changing and its radial velocity measurements are contaminated by ship motion, so beam directions reported relative to the instrument's own frame of reference must be transformed to an Earth-fixed frame before higher-order products like wind speed and direction can be derived. The DLMC VAP uses a prescribed displacement vector and roll/pitch/yaw offsets between the DL and NAV coordinate systems to rotate the DL beam vector into the NAV frame (matrix B), and then uses NAV-measured yaw, pitch, and roll (and their rates) to rotate the NAV frame into the Earth frame (matrix A). The velocity of the DL in the Earth frame is computed from the NAV's linear velocity (from surge, sway, heave) plus the linear velocity due to rotation about the NAV origin. The along-beam (radial) component of this platform velocity is subtracted from the observed radial velocity to yield the motion-corrected radial (air) velocity, while the beam vector expressed in the Earth frame yields the true-north-referenced azimuth and local-horizon-referenced elevation angles.

**Cadence.** input rate NAV provides 10 Hz measurements of surge, sway, and heave velocity components; averaging NAV data (roll, pitch, yaw, roll rate, pitch rate, yaw rate, surge velocity, sway velocity, heave velocity) are averaged over the pulse integration time of the DL beam for each DL profile; vector averaging is used for yaw to avoid problems from its cyclic nature (hb p. 8).

## Inputs

The report names these instruments and sibling products: Doppler lidar (DL), Navigational Location and Attitude instrument (NAV).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| range | m | - | - | (hb p. 9) |
| azimuth | deg | - | - | (hb p. 9) |
| elevation | deg | - | - | (hb p. 9) |
| radial_velocity (motion-corrected) | m s-1 | - | - | (hb p. 9) |
| intensity (SNR + 1) | unitless | - | - | (hb p. 9) |
| attenuated_backscatter | m-1 sr-1 | - | - | (hb p. 9) |
| lidar_velocity_west | m s-1 | - | - | (hb p. 9) |
| lidar_velocity_north | m s-1 | - | - | (hb p. 9) |
| lidar_velocity_z | m s-1 | - | - | (hb p. 9) |
| lidar_velocity_radial | m s-1 | - | - | (hb p. 9) |
| nav_roll | deg | - | - | (hb p. 9) |
| nav_pitch | deg | - | - | (hb p. 9) |
| nav_yaw | deg | - | - | (hb p. 9) |
| lidar_roll | deg | - | - | (hb p. 9) |
| lidar_pitch | deg | - | - | (hb p. 9) |
| lat | deg | - | - | (hb p. 9) |
| lon | deg | - | - | (hb p. 9) |
| alt | m | - | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Displacement vector Δr (DL relative to NAV, NAV frame) -... | [1.52 m, 4.11 m, 1.68 m] | (hb p. 7) |
| Mean pitch offset Δβ (NAV−DL) | -0.27° | (hb p. 7) |
| Mean roll offset Δγ (NAV−DL) | -1.77° | (hb p. 7) |
| Yaw offset Δα | 0 (assumed negligible) | (hb p. 7) |
| NAV velocity data rate | 10 Hz (surge, sway, heave) | (hb p. 5) |


## The data

Verified example: **`mosdlmcusrM1.c1`**, file `mosdlmcusrM1.c1.20200917.042722.nc`
(0.61 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=112, `range`=320 |
| Data variables | 40 |
| QC variables | 12 (`qc_` companions) |
| Median time step | 3 s |
| File time span | 2020-09-17T04:27:22 to 2020-09-17T04:33:28 |
| dod version | dlmcusr-c1-1.0 |
| process version | vap-dlmc-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `azimuth` | degree | time | yes | Beam azimuth relative to true north |
| `elevation` | degree | time | yes | Beam elevation angle measured from the horizon |
| `nav_pitch` | degree | time | yes | Platform pitch angle from the NAV |
| `nav_pitch_rate` | degree/s | time | yes | Platform pitch rate from the NAV |
| `nav_roll` | degree | time | yes | Platform roll angle from the NAV |
| `nav_roll_rate` | degree/s | time | yes | Platform roll rate from the NAV |
| `nav_yaw` | degree | time | yes | Platform yaw angle from the NAV |
| `nav_yaw_rate` | degree/s | time | yes | Platform yaw rate from the NAV |
| `radial_velocity` | m/s | time,range | yes | Radial air velocity corrected for platform motion |
| `attenuated_backscatter` | 1/(m sr) | time,range | - | Attenuated backscatter |
| `intensity` | 1 | time,range | - | Intensity (signal to noise ratio + 1) |
| `lidar_nav_displacement_bow` | m | - | - | Bow-ward component of the lidar-nav displacement vector |
| `lidar_nav_displacement_port` | m | - | - | Port-ward component of the lidar-nav displacement vector |
| `lidar_nav_displacement_up` | m | - | - | Up-ward (normal to ship deck) component of the lidar-nav displacement... |
| `lidar_nav_pitch_offset` | degree | - | - | The lidar-nav pitch angle offset |
| `lidar_nav_roll_offset` | degree | - | - | The lidar-nav roll angle offset |
| `lidar_nav_yaw_offset` | degree | - | - | The lidar-nav yaw angle offset |
| `lidar_pitch` | degree | time | - | Platform pitch angle from the lidar's low quality tilt sensor |
| `lidar_roll` | degree | time | - | Platform roll angle from the lidar's low quality tilt sensor |
| `lidar_velocity_north` | m/s | time | - | North-ward component of the lidar's velocity |
| `lidar_velocity_radial` | m/s | time | - | Along-beam component of the lidar's velocity |
| `lidar_velocity_west` | m/s | time | - | West-ward component of the lidar's velocity |
| `lidar_velocity_z` | m/s | time | - | Z-component (aligned with gravity) of the lidar's velocity |
| `range` | m | range | - | Distance from Lidar to center of range gate |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("mosdlmcusrM1.c1", "2020-09-17", "2020-09-17")
ds = armlive_open("mosdlmcusrM1.c1", "2020-09-17", "2020-09-17", cleanup_qc=True)
```

## Quality control in this product

12 `qc_` companion variables cover 12 of the
40 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("mosdlmcusrM1.c1", "20191011", "20260924")
```

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Ship motion contamination of radial velocity | Observed (uncorrected) radial velocity measurements from the DL include a spurious contribution from the ship's linear and rotational motion, distorting apparent wind/air velocity until... | DLMC VAP subtracts the along-beam component of the DL's Earth-frame velocity (lidar_velocity_radial) from the observed radial velocity to produce the... | (hb p. 6) |
| Changing lidar heading and tilt on a moving ship | Beam azimuth/elevation reported relative to the instrument frame drift relative to true north/horizon as the ship's heading and tilt change, unlike stationary land-based deployments | DLMC transforms beam angles from the DL frame to NAV frame and then to an Earth-fixed frame using NAV attitude data so azimuth is relative to true... | (hb p. 6) |
| Noisy DL internal tilt sensor | DL pitch/roll readings from its internal tilt sensor show significant noise compared to NAV pitch/roll data (see Figure 3 comparison for 20200331) | Sufficient averaging over the deployment was adequate for estimating the pitch and roll offset despite the noise | (hb p. 7) |
| Misalignment of DL and NAV coordinate axes (non-coalignment) | Non-zero pitch/roll/yaw offsets required between DL and NAV frames; if unaccounted for, transformed beam angles and velocities would be biased | Offsets (Δα, Δβ, Δγ) and displacement vector Δr must be prescribed ahead of time; handbook recommends ensuring coalignment of DL and NAV x-axes in... | (hb p. 7) |
| Yaw offset assumption | Yaw offset between DL and NAV is assumed to be exactly zero based on by-eye alignment during installation rather than measured; any real yaw misalignment would not be corrected | Assumed negligible because DL's 1-axis was oriented facing the front of the ship during setup | (hb p. 7) |
| Cyclic nature of yaw angle in averaging | Naive scalar averaging of yaw angle across the pulse integration window could produce erroneous results near the 0/360 degree wrap | Vector averaging is used for the yaw angle to avoid problems caused by its cyclic nature | (hb p. 8) |
| Limited scan types during MOSAiC | Only 'fpt' and 'usr' scan-type datastreams are available/processed for the MOSAiC deployment, limiting the scan geometries in the output data | - | (hb p. 3) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Newsom, RK, and R Krishnamurthy. 2020. Doppler Lidar Handbook. U.S. Department of Energy, Atmospheric Radiation Measurement User Facility, Richland, Washington. DOE/SC-ARM/TR-101.
- Walton, SM. 2019. Navigational Location and Attitude (NAV) Instrument Handbook. U.S. Department of Energy, Atmospheric Radiation Measurement User Facility, Richland, Washington. DOE/SC-ARM/TR-226.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-296.pdf (16 pages, DOE/SC-ARM-TR-296, by R Newsom, G Gibler, K Gaustad, D Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=dlmc`, read 2026-09-24
- Example file: `mosdlmcusrM1.c1.20200917.042722.nc` from `mosdlmcusrM1.c1`, 0.61 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
