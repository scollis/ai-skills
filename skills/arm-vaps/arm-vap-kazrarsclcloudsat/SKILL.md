---
name: arm-vap-kazrarsclcloudsat
description: ARM KAZR-ARSCL, reflectivities aligned with CloudSat Cloud Profiling Radar (kazrarsclcloudsat) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Reflectivity, Best-estimate reflectivity, Mean Doppler velocity, Spectral width, Linear depolarization ratio, Signal-to-noise ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparsclkazrcloudsatC1.c1) and the variable inventory of a real file. Use when working with kazrarsclcloudsat data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - kazrarsclcloudsat, sgparsclkazrcloudsatC1.c1, Reflectivity, Best-estimate reflectivity, Mean Doppler velocity, Spectral width, Linear depolarization ratio.
---

# KAZRARSCLCLOUDSAT - KAZR-ARSCL, reflectivities aligned with CloudSat Cloud Profiling Radar

This value-added product applies monthly, CloudSat-derived reflectivity offsets to KAZRARSCL merged cloud-radar reflectivity fields at fixed and mobile ARM sites, aligning KAZR reflectivity with the well-characterized 95-GHz CloudSat Cloud-Profiling Radar record.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 23 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `kazrarsclcloudsat` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-279 / KL Johnson, SE Giangrande, A Zhou / February 2022](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-279.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2012-03-01 to 2017-11-29 (retired) |
| Datastreams with data | 4 across 4 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/kazrarsclcloudsat |


## Credit

Everything this skill knows about the retrieval is the work of **KL Johnson, SE Giangrande, A Zhou** -
the ARM developers and mentors who wrote the technical report it derives from:

> KL Johnson, SE Giangrande, A Zhou. *Ka-Band ARM Zenith Radar (KAZR) Active Remote Sensing of Clouds (ARSCL) CloudSat Calibration (KAZRARSCL-CLOUDSAT) Value-Added Product Report*, DOE/SC-ARM-TR-279, February 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-279.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm ingests the full KAZRARSCL VAP output (reflectivity, reflectivity_best_estimate, radar_mode_flag) and a netCDF configuration file of monthly CloudSat-KAZR reflectivity offsets derived by Kollias et al. (2019) from statistical comparisons of CloudSat's 95-GHz CPR with zenith-pointing ARM cloud radars within 200-300 km and a 2-hour overpass window. For each time-height point, the KAZRARSCL radar_mode_flag is used to select the correct per-mode CloudSat offset (one value per mode per month, representing a six-month averaging window), which is then added to both the reflectivity and reflectivity_best_estimate fields. The offsets themselves were derived by degrading ARM radar sensitivity to CloudSat's MDS, correcting both platforms for gaseous attenuation and ice-scattering differences, retaining only non-precipitating profiles, and testing 301 candidate offsets (-15 to +15 dBZ in 0.1 dB steps) against CFAD-derived mean reflectivity profiles to find the offset with lowest RMSE per six-month window. The VAP outputs the applied offset, its RMSE, and the number of CloudSat-ARM samples used, alongside all pass-through KAZRARSCL fields.

**Cadence.** output every daily netCDF output file; averaging CloudSat offsets represent six-month averaged reflectivity comparisons, reported monthly (hb p. 6).

## Inputs

The report names these instruments and sibling products: KAZR (Ka-Band ARM Zenith Radar), KAZRARSCL VAP, MMCR (millimeter wavelength cloud radar), WACR (W-Band ARM Cloud Radar), CloudSat 95-GHz Cloud-Profiling Radar (CPR), micropulse lidar (MPL), microwave radiometer (MWR), ceilometer, rain gauge.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Reflectivity (statistically aligned with CloudSat) | dBZ | valid_min -90 to valid_max 50 | - | (hb p. 14) |
| Best-estimate reflectivity (statistically aligned with... | dBZ | valid_min -90 to valid_max 50 | - | (hb p. 14) |
| Mean Doppler velocity | m/s | valid_min -25 to valid_max 25 | - | (hb p. 15) |
| Spectral width | m/s | valid_min 0 to valid_max 10 | - | (hb p. 16) |
| Linear depolarization ratio | dBZ | valid_min -50 to valid_max 50 | - | (hb p. 17) |
| Signal-to-noise ratio | dB | - | - | (hb p. 17) |
| Statistically-derived reflectivity offset between KAZR and... | dBZ | -15 to +15 dBZ (candidate offsets... | - | (hb p. 12) |
| cloudsat_rmse (RMSE of statistically derived offset) | dBZ | - | - | (hb p. 8) |
| cloudsat_num_samples (number of CloudSat-ARM samples used) | 1 | - | - | (hb p. 8) |
| radar_first_top (top height of lowest significant detection... | m | valid_range 0, 25000; flag_values... | - | (hb p. 18) |
| Precipitation mean from rain gauge | mm/hr | - | - | (hb p. 19) |
| Liquid water path best-estimate from microwave radiometer | g/m^2 | - | - | (hb p. 20) |
| Cloud base best estimate | m | valid_range 0, 25000; flag_values... | - | (hb p. 20) |
| Cloud layer base/top height (up to 10 layers) | m | valid_range 0, 25000; flag_values... | - | (hb p. 21) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| height dimension size | 596 | (hb p. 13) |
| layer dimension size | 10 | (hb p. 13) |
| radar_mode dimension size | 4 | (hb p. 13) |
| Offset search range in derivation | -15 to +15 dBZ in intervals of 0.1 dB (301 separate data sets) | (hb p. 12) |
| CloudSat inclusion radius from ARM site | 200-300 km | (hb p. 12) |
| ARM radar time window around CloudSat overpass | two-hour window centered on overpass | (hb p. 12) |
| CloudSat minimum altitude used | observations below 500 m above Earth's surface omitted | (hb p. 12) |
| CloudSat SNR/quality threshold | CPR Cloud mask less than  20 omitted | (hb p. 12) |
| ARM radar SNR threshold | SNR less than  -15 dB omitted | (hb p. 12) |
| ARM radar MDS degradation threshold | returns with MDS less than approximately -30 dBZ omitted | (hb p. 12) |
| Matched data resolution | 1-minute time samples at 250 m vertical resolution | (hb p. 12) |
| Offset averaging window | six-month time window; offset labeled by first month of window | (hb p. 12) |
| reflectivity_best_estimate valid_min/valid_max | -90 to 50 dBZ | (hb p. 14) |
| mean_doppler_velocity valid_min/valid_max | -25 to 25 m/s | (hb p. 15) |
| spectral_width valid_min/valid_max | 0 to 10 m/s | (hb p. 16) |
| linear_depolarization_ratio valid_min/valid_max | -50 to 50 dBZ | (hb p. 17) |
| radar_first_top valid_range | 0, 25000 m | (hb p. 18) |
| cloud_base_best_estimate valid_range | 0, 25000 m | (hb p. 20) |


## The data

Verified example: **`sgparsclkazrcloudsatC1.c1`**, file `sgparsclkazrcloudsatC1.c1.20170828.000000.nc`
(68.5 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=21600, `height`=596, `radar_mode`=4, `layer`=10 |
| Data variables | 33 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2017-08-28T00:00:00 to 2017-08-28T23:59:56 |
| dod version | arsclkazrcloudsat-c1-1.1 |
| process version | vap-kazrarsclcloudsat-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `linear_depolarization_ratio` | dBZ | time,height | yes | Linear depolarization ratio |
| `mean_doppler_velocity` | m/s | time,height | yes | Mean Doppler velocity |
| `mwr_lwp` | g/m^2 | time | yes | Liquid water path best-estimate from microwave radiometer |
| `precip_mean` | mm/hr | time | yes | Precipitation mean from rain gauge |
| `reflectivity` | dBZ | time,height | yes | Reflectivity statistically aligned with CloudSat |
| `reflectivity_best_estimate` | dBZ | time,height | yes | Best-estimate reflectivity statistically aligned with CloudSat |
| `spectral_width` | m/s | time,height | yes | Spectral width |
| `cloud_base_best_estimate` | m | time | - | Cloud base best estimate, based on ceilometer and micropulse lidar |
| `cloud_layer_base_height` | m | time,layer | - | Base height of hydrometeor layers for up to 10 layers, based on... |
| `cloud_layer_top_height` | m | time,layer | - | Top height of hydrometeor layers for up to 10 layers, based on... |
| `cloud_mask_mpl` | 1 | time,height | - | Cloud mask from 30smplcmask1zwang |
| `cloud_source_flag` | 1 | time,height | - | Instrument source flag for cloud (hydrometeor) detections |
| `cloudsat_num_samples` | 1 | radar_mode | - | Number of available CloudSat and KAZR samples used to estimate... |
| `cloudsat_reflectivity_offset_applied` | dBZ | radar_mode | - | Statistically-derived reflectivity offset between KAZR and CloudSat |
| `cloudsat_rmse` | dBZ | radar_mode | - | Root mean square error of statistically-derived reflectivity offset... |
| `height` | m | height | - | Height above ground level |
| `instrument_availability_flag` | 1 | time | - | Indicates which instruments have data available |
| `layer` | 1 | layer | - | Cloud layer number |
| `mean_doppler_velocity_dealias_flag` | 1 | time,height | - | Indication of whether or not dealiasing was performed on the... |
| `radar_first_top` | m | time | - | KAZR top height of lowest significant detection layer, before clutter... |
| `radar_mode` | 1 | radar_mode | - | Radar mode names |
| `radar_mode_flag` | 1 | time,height | - | Radar mode flag |
| `reflectivity_clutter_flag` | 1 | time,height | - | Reflectivity clutter flag |
| `signal_to_noise_ratio` | dB | time,height | - | Signal-to-noise ratio |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgparsclkazrcloudsatC1.c1", "2017-08-28", "2017-08-28")
ds = armlive_open("sgparsclkazrcloudsatC1.c1", "2017-08-28", "2017-08-28", cleanup_qc=True)
```

## Quality control in this product

7 `qc_` companion variables cover 7 of the
33 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgparsclkazrcloudsatC1.c1.20170828.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `reflectivity_best_estimate` | Data value not available in input file, data value has been set... | 12763360 | 99.1437 |
| `linear_depolarization_ratio` | Data value not available in input file, data value has been set... | 11376865 | 88.3736 |
| `reflectivity` | Data value not available in input file, data value has been set... | 10997633 | 85.4278 |
| `mean_doppler_velocity` | Data value not available in input file, data value has been set... | 10997633 | 85.4278 |
| `spectral_width` | Data value not available in input file, data value has been set... | 10997633 | 85.4278 |
| `precip_mean` | Data value not available in input file, data value has been set... | 7 | 0.0324 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgparsclkazrcloudsatC1.c1", "20120301", "20260924")
```

The report's own note on quality: Each science variable (reflectivity, reflectivity_best_estimate, mean_doppler_velocity, spectral_width, linear_depolarization_ratio, precip_mean, mwr_lwp) has a companion bit-packed qc_ variable: bit_1 = value less than valid_min (Bad), bit_2 = value greater than valid_max (Bad), bit_3 = data value not available in input file, set to missing_value (Bad); a value of 0 (no bits set) indicates the data has not failed any QC tests. reflectivity_clutter_flag distinguishes no detection, hydrometeor-only, hydrometeor+clutter, clutter-only, bad data, and missing data. instrument_availability_flag is...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| No output produced for a day | Missing daily netCDF files in the archive for certain dates | Occurs when cloud radar observations are unavailable or flagged 'bad' in KAZRARSCL input for the entire day, or when no CloudSat offset is available... | (hb p. 10) |
| Statistical, non-instantaneous offset | Applied offset is a six-month statistical average, not representative of any single event's true reflectivity bias/drift | Handbook notes this explicitly; treat offsets as long-term calibration correction, not event-specific truth | (hb p. 6) |
| Missing CloudSat offset for Precipitation (PR) mode at Oliktok Point (OLI) | OLI site output produced even though no CloudSat offset exists for PR mode; PR-mode reflectivity at OLI left uncorrected | A Data Quality Report (DQR) has been issued to notify users | (hb p. 10) |
| Only one offset per mode per month | Within a given day/month, only a single scalar CloudSat offset value per radar operating mode is applied, even though the underlying derivation used a six-month window | - | (hb p. 6) |
| Limited site/time coverage | Gaps in Table 3 availability periods for NSA, SGP, AWR, and OLI; no data outside listed date ranges | - | (hb p. 9) |
| Only KAZR-based ARSCL processed | No KAZRARSCL-CLOUDSAT output for MMCR- or WACR-based ARSCL records even though CloudSat offsets exist for those radar generations too | - | (hb p. 11) |
| CloudSat ground clutter near surface | CloudSat comparison data excludes observations below 500 m above Earth's surface | Omitted in offset derivation due to excessive ground clutter | (hb p. 12) |
| Low SNR / poor data quality exclusion in offset derivation | CloudSat profiles with CPR Cloud mask less than  20 and ARM radar profiles with SNR less than  -15 dB excluded from the offset-fitting dataset | Excluded during Kollias et al. offset derivation | (hb p. 12) |
| Sensitivity mismatch between ARM radars and CloudSat | More sensitive ARM radar detects hydrometeors CloudSat cannot; requires degrading ARM data to CloudSat's MDS (~-30 dBZ) before comparison | ARM radar returns below approximate CloudSat MDS of -30 dBZ are omitted when deriving offsets | (hb p. 12) |
| Precipitating profiles excluded from offset derivation | Only 'non-precipitating' radar profiles used to derive offsets, to minimize hydrometeor attenuation bias | - | (hb p. 12) |
| Frequency/scattering differences between Ka-band ARM radars and 95-GHz CloudSat CPR | Reflectivity offsets partly reflect systematic conversion between Ka-band and 95-GHz equivalent values, plus gaseous attenuation and ice-crystal scattering corrections | Corrections applied for gaseous attenuation and ice-crystal scattering differences, and Ka-band reflectivities converted to 95-GHz equivalents before... | (hb p. 12) |
| Offset month labeling can mislead | The reported offset for a given month actually derives from a six-month window starting at that month, not centered on or ending at it | Handbook explicitly notes the month associated with an offset is the first month of the six-month window used to derive it | (hb p. 12) |
| Not all months/sites have available offsets | For many months at most sites, Kollias et al. offsets are not available, resulting in VAP non-production for those days | - | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Kollias, P, B Puigdomènech Treserras, and A Protat. 2019. "Calibration of the 2007–2017 record of ARM Cloud Radar Observations using CloudSat." Atmospheric Measurement Techniques 12(9): 4949
- Tanelli et al. 2008 (CloudSat CPR characterization)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-279.pdf (23 pages, DOE/SC-ARM-TR-279, by KL Johnson, SE Giangrande, A Zhou)
- Catalog record: ARM data-source index, `instrument_class_code=kazrarsclcloudsat`, read 2026-09-24
- Example file: `sgparsclkazrcloudsatC1.c1.20170828.000000.nc` from `sgparsclkazrcloudsatC1.c1`, 68.5 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
