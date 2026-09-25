---
name: arm-vap-sacradvvad
description: ARM SACR Advance Velocity Azimuth Display (sacradvvad) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (vad_fit_rmsd, number_az_angles), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpkasacradvvadC1.c1) and the variable inventory of a real file. Use when working with sacradvvad data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - sacradvvad, SACR Advance Velocity Azimuth Display, sgpkasacradvvadC1.c1, vad_fit_rmsd, number_az_angles, Cloud Properties.
---

# SACRADVVAD - SACR Advance Velocity Azimuth Display

The SACR-ADV-VAD VAP derives time series of vertical profiles of in-cloud horizontal wind speed and direction by applying the Velocity-Azimuth Display technique to mean Doppler velocity measurements collected during horizon-to-horizon range height indicator (HSRHI) scans from the Ka-band Scanning ARM Cloud Radar.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 12 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sacradvvad` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-209 / EE Clothiaux, K Johnson, T Toto, P Kollias, K Lamer, SE Giangrande, M Oue / January 2018](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-209.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2012-08-01 to 2017-11-17 (retired) |
| Datastreams with data | 6 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sacradvvad |


## Credit

Everything this skill knows about the retrieval is the work of **EE Clothiaux, K Johnson, T Toto, P Kollias, K Lamer, SE Giangrande, M Oue** -
the ARM developers and mentors who wrote the technical report it derives from:

> EE Clothiaux, K Johnson, T Toto, P Kollias, K Lamer, SE Giangrande, M Oue. *Scanning ARM Cloud Radar—Advanced—Velocity Azimuth Display Value-Added Product*, DOE/SC-ARM-TR-209, January 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-209.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The traditional VAD technique uses radial velocity measurements at a constant elevation angle and constant range through azimuth from 0° to 360°; in a region of homogeneous wind flow, the observed radial velocity exhibits a sinusoidal pattern when plotted versus azimuth at a fixed elevation and constant height above the ground. The sinusoid's maximum amplitude equals the horizontal wind speed and its phase location indicates the wind direction, while the offset of the sinusoid from zero velocity measures vertical hydrometeor motion. The SACR HSRHI scan strategy consists of six horizon-to-horizon scans spaced by 30 degrees in azimuth, providing at most 12 azimuth points contributing data to the algorithm from the endpoints of the six scans. The SACR-ADV-VAD algorithm pulls in a full day of HSRHI scan input files, and each HSRHI scan file provides the measurements needed to produce a single time profile of in-cloud horizontal wind speed and direction as a function of height. The VAP outputs the product in a single file for each day, with one output time profile produced for each input HSRHI file.

**Cadence.** output every temporal resolution of the product will be ~30-60 min (hb p. 6).

## Inputs

The report names these instruments and sibling products: Scanning ARM Cloud Radar (SACR), soundings.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| horizontal_wind_magnitude_at_cloud_level | - | - | - | (hb p. 9) |
| horizontal_wind_direction_at_cloud_level | - | - | - | (hb p. 9) |
| vad_fit_rmsd | - | - | - | (hb p. 9) |
| number_az_angles | - | - | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Height resolution | 50 m | (hb p. 9) |
| Height range | 100m to 15000m AGL | (hb p. 9) |
| HSRHI scan repeat interval | every 30-60 min | (hb p. 6) |
| HSRHI scan azimuth spacing | 30 degrees | (hb p. 6) |
| Number of scans per HSRHI strategy | six horizon-to-horizon scans | (hb p. 6) |
| Maximum azimuth points contributing to algorithm | at most 12 azimuth points | (hb p. 7) |


## The data

Verified example: **`sgpkasacradvvadC1.c1`**, file `sgpkasacradvvadC1.c1.20120828.002308.nc`
(0.19 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=37, `bound`=2, `height`=299 |
| Data variables | 13 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 2548.5 s |
| File time span | 2012-08-28T00:23:08 to 2012-08-28T23:49:23 |
| dod version | kasacradvvad-c1-1.0 |
| process version | vap-sacradvvad-5.1-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `height` | m | height | - | Height above ground level |
| `horizontal_wind_direction_at_cloud_level` | degree | time,height | - | Horizontal wind from direction at cloud level |
| `horizontal_wind_magnitude_at_cloud_level` | m/s | time,height | - | Horizontal wind magnitude at cloud level |
| `number_az_angles` | count | time,height | - | Number of azimuth angles |
| `nyquist_velocity` | m/s | time | - | Unambiguous Doppler velocity |
| `radar_beam_width_h` | degree | time | - | Radar beam width, horizontal channel |
| `time` | - | time | - | time in seconds since volume start |
| `vad_fit_rmsd` | unitless | time,height | - | VAD fit RMSD |


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
                     params={"user": f"{user}:{token}", "ds": "sgpkasacradvvadC1.c1",
                             "start": "2012-08-28", "end": "2012-08-28", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpkasacradvvadC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpkasacradvvadC1.c1", "2012-08-28", "2012-08-28")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpkasacradvvadC1.c1", "2012-08-28", "2012-08-28"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpkasacradvvadC1.c1", "20120801", "20260924")
```

The report's own note on quality: Select velocity dealiasing and associated retrieval quality control measures to ensure accurate VAD estimates are only available within the 'c1' product streams (processed from calibrated kasacrcorhsrhi*.c1 input). The 'c0' versions, based on uncorrected SACR data, are available on an expedited timetable but may reflect additional noisiness and velocity aliasing in faster wind speeds. The output field vad_fit_rmsd provides a measure of the goodness of the VAD sinusoidal fit, and number_az_angles indicates how many azimuth points contributed to each retrieval.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Uncalibrated input data (c0 product stream) lacking velocity dealiasing and retrieval... | kasacradvvad*.c0 output products (based on uncorrected SACR kasacrhsrhi*.a1 data) may show additional noisiness and velocity aliasing, particularly in faster wind speeds, compared to c1... | Use the calibrated kasacrcorhsrhi*.c1 input stream to obtain kasacradvvad*.c1 output, which includes velocity dealiasing and quality control... | (hb p. 7) |
| Relative calibration offsets in SACR data | Not expected to visibly affect VAD product quality | Handbook notes relative calibration offsets do not impact the quality of the VAD products | (hb p. 7) |
| Irregular time stamps in output | Time profiles in the daily NetCDF output are only produced when an HSRHI scan sequence is performed, so the time dimension may not be evenly spaced | - | (hb p. 9) |
| Limited azimuth sampling for VAD fit | Algorithm has at most 12 azimuth points (from endpoints of six HSRHI scans) contributing to each wind retrieval, fewer than a full 360-degree azimuth scan; number_az_angles output variable... | - | (hb p. 7) |
| Sounding comparison limitation motivating VAP | Standard sounding observations are only conducted 1-4 times per day, which may not resolve detailed in-cloud wind structure; SACR-ADV-VAD is intended to augment/complement these infrequent... | Use SACR-ADV-VAD VAP wind profiles to augment sounding wind measurements | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Kollias, P, N Bharadwaj, K Widener, I Jo, and K Johnson. 2014. "Scanning ARM cloud radars. Part I: Operational Sampling Strategies." Journal of Atmospheric and Oceanic Technology 31(3): 569-582,...
- Lhermitte, RM, and DA Atlas. 1961. "Precipitation motion by pulse Doppler." Proceedings of the 9th Weather Radar Conference, Boston, American Meteorological Society, Boston, Massachusetts, 498-503.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-209.pdf (12 pages, DOE/SC-ARM-TR-209, by EE Clothiaux, K Johnson, T Toto, P Kollias, K Lamer, SE Giangrande, M Oue)
- Catalog record: ARM data-source index, `instrument_class_code=sacradvvad`, read 2026-09-24
- Example file: `sgpkasacradvvadC1.c1.20120828.002308.nc` from `sgpkasacradvvadC1.c1`, 0.19 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
