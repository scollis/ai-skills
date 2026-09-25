---
name: arm-vap-radclss
description: ARM Extracted Radar Columns and In-Situ Sensors (RadCLss) (radclss) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Radial Doppler Velocity, Spectral Width, Differential Reflectivity, Differential Phase, Cross-Polar Correlation Ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (bnfcsapr2radclssS3.c2) and the variable inventory of a real file. Use when working with radclss data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - radclss, Extracted Radar Columns and In-Situ Sensors (RadCLss), bnfcsapr2radclssS3.c2, Radial Doppler Velocity, Spectral Width, Differential Reflectivity, Differential Phase, Cloud Properties.
---

# RADCLSS - Extracted Radar Columns and In-Situ Sensors (RadCLss)

RadCLss is an ARM value-added product that extracts CMAC-processed scanning-radar columns above instrumented surface sites and spatiotemporally merges them with co-located in-situ surface sensors (rain gauges, disdrometers, met stations, soundings, wind profilers, ceilometers) to validate radar-based precipitation retrievals.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 44 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `radclss` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-312 / JR O'Brien, RC Jackson, BA Raut, SM Collis, A Theisen, ZS Sherman, M Grover, M Tuftedal, D Feldman / November 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-312.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2021-11-02 to 2025-06-23 (retired) |
| Datastreams with data | 2 across 2 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/radclss |


## Credit

Everything this skill knows about the retrieval is the work of **JR O'Brien, RC Jackson, BA Raut, SM Collis, A Theisen, ZS Sherman, M Grover, M Tuftedal, D Feldman** -
the ARM developers and mentors who wrote the technical report it derives from:

> JR O'Brien, RC Jackson, BA Raut, SM Collis, A Theisen, ZS Sherman, M Grover, M Tuftedal, D Feldman. *Extracted Radar Columns and In Situ Sensors (RadCLss) Value-Added Product Report*, DOE/SC-ARM-TR-312, November 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-312.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

RadCLss builds on CMAC (Corrected Moments to Antenna Coordinates), which uses the Py-ART GateFilter to classify the scattering medium in each radar gate (gate-ID: rain, melting layer, snow, second trip, terrain blockage, no significant scatterer) and applies corrections for attenuation, specific differential phase, and Doppler velocity dealiasing. From these corrected radar moments, CMAC computes quantitative precipitation estimates using empirical power-law relationships based on equivalent reflectivity factor (Z), specific differential phase (KDP), and specific attenuation (AH). RadCLss then uses the Py-ART column_vertical_profile utility to compute the great-circle distance (haversine formula) and forward azimuth from the radar to each surface site, and subsets each radar elevation scan above that location. Following Murphy et al. (2020) and Bukovcic et al. (2020), three individual range gates from three azimuths spanning the in situ location are extracted and averaged for each CMAC field, with the lowest valid range gate (per CMAC gate-ID) chosen for collocation. The extracted radar columns are then matched in time with in situ surface observations (resampled to five-minute intervals and linearly interpolated to the column timestamps) using the Atmospheric data Community Toolkit (ACT), producing daily time series for direct comparison of radar parameters with surface precipitation observations.

**Cadence.** input rate Varies by radar scan strategy and by in situ sensor sampling frequency; output every Daily time series (matched columns and sensors collated for all scans in a day); averaging In situ sensors resampled to five-minute intervals and linearly interpolated to match extracted radar column timestamps; radar field averaged from three range gates across three azimuths per site (hb p. 12).

## Inputs

The report names these instruments and sibling products: CMAC (Corrected Moments in Antenna Coordinates), XSAPR (X-Band Scanning ARM Precipitation Radar), CSAPR (C-Band Scanning ARM Precipitation Radar), KAZR (Ka-Band ARM Zenith Radar), MMCR (millimeter wavelength cloud radar), Laser Disdrometer (LD), LDQUANTS, VDISQUANTS, Pluvio weighing bucket precipitation gauge (WBPLUVIO2), Surface Meteorological Instrumentation (MET), METWXT, Balloon-Borne Sounding System (SONDEWNPN).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Equivalent Radar Reflectivity Factor (DBZ /... | dBZ | - | - | (hb p. 19) |
| Radial Doppler Velocity (VEL / corrected_velocity) | m/s | valid_min -47.7 to valid_max 47.7... | - | (hb p. 19) |
| Spectral Width (WIDTH) | m/s | - | - | (hb p. 20) |
| Differential Reflectivity (ZDR /... | dB | - | - | (hb p. 20) |
| Differential Phase (PHIDP / corrected_differential_phase /... | degree | valid_min 0.0 to valid_max 400.0 | - | (hb p. 20) |
| Cross-Polar Correlation Ratio (RHOHV) | 1 | - | - | (hb p. 20) |
| Normalized Coherent Power (NCP) | 1 | - | - | (hb p. 20) |
| Specific Differential Phase (corrected_specific_diff_phase... | degree/km | - | - | (hb p. 22) |
| Specific Attenuation | dB/km | valid_min 0.0 to valid_max 1.0 | - | (hb p. 23) |
| Path Integrated Attenuation | dB | - | - | (hb p. 23) |
| Rain Rate from Specific Attenuation (rain_rate_A) | mm/hr | valid_min 0.0 to valid_max 400.0 | - | (hb p. 23) |
| Rain Rate from Reflectivity (rain_rate_Z, BNF) | mm/hr | valid_min 0.0 to valid_max 400.0 | - | (hb p. 36) |
| Rain Rate from KDP (rain_rate_Kdp, BNF) | mm/hr | valid_min 0.0 to valid_max 400.0 | - | (hb p. 36) |
| Snowfall Rate (snow_rate_ws2012, snow_rate_ws88diw,... | mm/h | valid_min 0 to valid_max 500 | - | (hb p. 23) |
| Height of radar beam over freezing level | m | - | - | (hb p. 22) |
| Precipitation accumulation and rates (Pluvio: intensity_rt,... | mm, mm/hr | varies by field, see... | absolute_accuracy plus/minus 6... | (hb p. 24) |
| Surface meteorological quantities (temp, RH, pressure,... | degC, %, kPa, m/s,... | - | - | (hb p. 25) |
| Drop size distribution / disdrometer quantities... | mm/hr, mm, mm^3/m^3,... | - | - | (hb p. 28) |
| Balloon-borne sounding profiles (pressure, temperature,... | hPa, degC, m/s, degree | e.g. sonde_pres 0.0-1100.0 hPa;... | - | (hb p. 30) |
| Cloud base height / vertical visibility / backscatter... | m, log(1/(sr*km*10000)) | valid_min 0.00 to valid_max... | - | (hb p. 32) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Radar column extraction geometry | Three individual range gates from three azimuths spanning the in situ location are extracted and averaged for each CMAC field; lowest valid range... | (hb p. 12) |
| Lowest valid gate constraint above instrumented site | within 1.5 km of the surface | (hb p. 10) |
| In situ resampling interval | 5-minute intervals, linearly interpolated to extracted column timestamps | (hb p. 12) |
| SAIL RadCLss dimensions | time = UNLIMITED, height = 138, station = 6, particle_size = 32, raw_fall_velocity = 32 | (hb p. 19) |
| BNF RadCLss dimensions | time = UNLIMITED, height = 32, station = 6 | (hb p. 35) |
| SAIL RadCLss class/level/version | class: xprecipradarradclss, level: c2, version: 1.4 | (hb p. 19) |
| BNF RadCLss class/level/version | class: csapr2radclss, level: c2, version: 1.0 | (hb p. 35) |
| Snowfall Z(S) empirical relationships (SAIL) | Wolfe and Snider (2012): Z=110S^2 (A=110,B=2,S-band); WSR-88D High Plains: Z=130S^2 (A=130,B=2,S-band); Braham(1990)1: Z=67S^1.28... | (hb p. 17) |
| BNF precipitation rate empirical relationships | Attenuation: R=294*AH^0.89 (A=294,B=0.89); Reflectivity: R=0.017*Z^0.714 (A=0.017,B=0.714); Specific differential phase: R=25.1*KDP^0.777... | (hb p. 18) |
| rain_rate_A comment (SAIL) | R=43.5*specific_attenuation^0.79 | (hb p. 23) |
| rain_rate_A coefficients (BNF) | A_coefficient=51.3, B_exponent=0.81 | (hb p. 37) |
| rain_rate_Z coefficients (BNF) | A_coefficient=0.017, B_exponent=0.714 | (hb p. 37) |
| rain_rate_Kdp coefficients (BNF) | A_coefficient=294, B_exponent=0.89 | (hb p. 37) |
| gate_id classification scheme | 0:multi_trip,1:rain,2:snow,3:no_scatter,4:melting,5:clutter,6:terrain_blockage | (hb p. 21) |
| corrected_velocity valid range (SAIL) | valid_min=-47.7, valid_max=47.7 m/s | (hb p. 21) |
| corrected_velocity valid range (BNF) | valid_min=-49.476, valid_max=49.476 m/s | (hb p. 36) |
| attenuation_corrected_differential_reflectivity applied... | -0.4732 dB | (hb p. 36) |
| attenuation_corrected_reflectivity_h applied bias... | 2.2 dBZ | (hb p. 36) |


## The data

Verified example: **`bnfcsapr2radclssS3.c2`**, file `bnfcsapr2radclssS3.c2.20250619.000000.nc`
(3.5 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=142, `station`=6, `height`=32 |
| Data variables | 65 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 603 s |
| File time span | 2025-06-19T00:04:16 to 2025-06-19T23:50:25 |
| dod version | csapr2radclss-c2-1.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `accum_nrt` | mm | time,station | - | Accumulated precipitation over the sampling interval filtered and... |
| `accum_rtnrt` | mm | time,station | - | Accumulated amounts of precipitation over the sampling interval... |
| `atmos_pressure` | kPa | time,station | - | Atmospheric pressure |
| `attenuation_corrected_differential_reflectivity` | dB | time,height,station | - | Rainfall attenuation-corrected differential reflectivity |
| `attenuation_corrected_differential_reflectivity_lag_1` | dB | time,height,station | - | Differential reflectivity estimated at lag 1 corrected for rainfall... |
| `attenuation_corrected_reflectivity_h` | dBZ | time,height,station | - | Rainfall attenuation-corrected reflectivity, horizontal channel |
| `bucket_nrt` | mm | time,station | - | The currently measured, filtered bucket contents since last reset |
| `copol_correlation_coeff` | 1 | time,height,station | - | Copolar correlation coefficient (also known as rhohv) |
| `corrected_differential_phase` | degree | time,height,station | - | Corrected Differential Phase |
| `corrected_differential_reflectivity` | dB | time,height,station | - | Corrected differential reflectivity |
| `corrected_reflectivity` | dBZ | time,height,station | - | Corrected reflectivity |
| `corrected_specific_diff_phase` | degree/km | time,height,station | - | Corrected Specific differential phase (KDP) |
| `corrected_velocity` | m/s | time,height,station | - | Corrected mean doppler velocity |
| `filtered_corrected_differential_phase` | degree | time,height,station | - | Filtered Corrected Differential Phase |
| `filtered_corrected_specific_diff_phase` | degree/km | time,height,station | - | Filtered Corrected Specific differential phase (KDP) |
| `gate_time` | - | time,station | - | Time in Seconds that Cooresponds to the Start of each Individual... |
| `height` | m | height | - | Height of Radar Beam |
| `intensity_rt` | mm/hr | time,station | - | Heavy precipitation alarm |
| `intensity_rtnrt` | mm/hr | time,station | - | Rain intensity based upon accum_rtnrt |
| `ldquants_differential_reflectivity_cband20c` | dB | time,station | - | Estimated Differential Radar Reflectivity (H, V) from Drop Size... |
| `ldquants_lwc` | g/m^3 | time,station | - | Liquid Water Content |
| `ldquants_mass_weighted_mean_diameter` | mm | time,station | - | Mean Drop Diameter |
| `ldquants_med_diameter` | mm | time,station | - | Median Drop Diameter |
| `ldquants_rain_rate` | mm/hour | time,station | - | Instantaneous Rainfall Rate of Water Flux |
| `ldquants_reflectivity_factor_cband20c` | dBZ | time,station | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `ldquants_specific_attenuation_cband20c` | dB/km | time,station | - | Specific Attenuation C-Band when temperature is 20 degree C |
| `ldquants_specific_differential_attenuation_cband20c` | dB/km | time,station | - | Specific Differential Attenuation C-Band when temperature is 20... |
| `ldquants_specific_differential_phase_cband20c` | degree/km | time,station | - | Specific Differential Phase from Drop Size Distribution C-Band when... |
| `ldquants_total_droplet_concentration` | 1/m^3 | time,station | - | Total Droplet Concentration |
| `rain_rate_A` | mm/hr | time,height,station | - | Rainfall rate from specific attenuation |


_33 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "bnfcsapr2radclssS3.c2",
                             "start": "2025-06-19", "end": "2025-06-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfcsapr2radclssS3.c2/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfcsapr2radclssS3.c2", "2025-06-19", "2025-06-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfcsapr2radclssS3.c2", "2025-06-19", "2025-06-19"))   # cite what you pulled
```

This product carries 65 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "bnfcsapr2radclssS3.c2", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['accum_nrt', 'accum_rtnrt', 'atmos_pressure'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("bnfcsapr2radclssS3.c2", "20211102", "20260924")
```

The report's own note on quality: In situ sensors are downloaded, opened, and quality controlled using ACT modules before being resampled to five-minute intervals and linearly interpolated to the radar column timestamps for collocation.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Terrain blockage precluding valid radar column extraction | Requested surface site (e.g., SAIL Brush Creek) shows no valid gates within CMAC Gate-ID; no extracted column is produced for that site | Sites are inspected in advance to verify valid radar returns exist within CMAC before including them in RadCLss | (hb p. 10) |
| Lowest valid gate too far above surface due to distance from radar or scan strategy | Lowest valid radar gate above a site (e.g., BNF S40) is far from the surface, exceeding practical comparison height; requires additional checks | Additional checks are performed to verify the lowest valid radar gate is within 1.5 km of the surface; scan strategy changes during IOPs are monitored | (hb p. 10) |
| Duplicate/indistinguishable columns from closely spaced sites | Multiple nearby instrument sites (e.g., BNF meteorological tower sites S10, S13, S14) produce identical or non-unique radar columns from the radar's perspective | Only an average column above the site was extracted for these locations | (hb p. 10) |
| Beam blockage precluding use of lowest physical gate | PPI scan shows rays used by column_vertical_profile do not reach the lowest physical range gate at some sites; extracted lowest gate is higher than the true lowest possible gate | The lowest valid range gate, as defined by CMAC gate-ID, is chosen instead of the lowest physical gate | (hb p. 12) |
| Radar sampling volume far above the surface in complex terrain (SAIL) | For most SAIL sites, the lowest valid radar gate is hundreds of meters above ground; boundary-layer processes below the beam are not captured, causing discrepancies between radar-retrieved... | - | (hb p. 13) |
| Inability to distinguish precipitation from lofted/blowing snow within a radar gate | Radar-derived precipitation totals may be systematically higher than surface accumulation during blowing/lofted snow events | - | (hb p. 14) |
| Empirical Z-S and QPE relationship uncertainty/regional dependence | Multiple empirical coefficient sets (ensemble of a/b values) yield different snowfall/rain rate estimates for the same reflectivity, reflectivity spread indicates estimate uncertainty | An ensemble approach with multiple a and b coefficients is used (e.g., four snowfall relationships for SAIL) to represent estimate spread instead of... | (hb p. 17) |
| Known experimental/unresolved processing issues | Global attribute 'known_issues' states data are 'highly experimental and initial'; PHIDP shows jumps in insect-contaminated regions | Handbook notes 'known_issues = False phidp jumps in insect regions. Still uses old Giangrande code. Issues with some s[ites]' - users cautioned data... | (hb p. 34) |
| Fill values and thresholds on Pluvio and MET fields can suppress small measurements | Only measurements exceeding a stated threshold (e.g., 6 mm/hr for intensity_rt, 0.05 mm for accum fields, 0.01 mm for bucket fields) are recorded; values below threshold appear as no... | - | (hb p. 24) |
| Radar scan strategy changes during IOPs affect site inclusion | Sites present in RadCLss for part of a deployment may drop out or change validity as the scan strategy is modified for select Intensive Operational Periods | Additional checks are required each time scan strategy changes to re-verify lowest valid gate | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Al-Sakka et al. 2013, J. Appl. Meteor. Climatol. 52(10):2328-2344
- Bukovcic et al. 2020, J. Appl. Meteor. Climatol. 59(5):991-1009
- Dolan and Rutledge 2009, J. Atmos. Oceanic Technol. 26(10):2071-2088
- Giangrande et al. 2014, J. Appl. Meteor. Climatol. 53(9):2130-2147
- Helmus and Collis 2016, J. Open Research Software 4:e25
- Murphy et al. 2020, J. Atmos. Oceanic Technol. 37(9):1623-1642
- Wen et al. 2015, J. Atmos. Oceanic Technol. 32(7):1320-1340
- Mather and Voyles 2012/2013, BAMS 94(3):377-392
- Theisen et al. 2023/2025, ACT Release, Zenodo

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-312.pdf (44 pages, DOE/SC-ARM-TR-312, by JR O'Brien, RC Jackson, BA Raut, SM Collis, A Theisen, ZS Sherman, M Grover, M Tuftedal, D Feldman)
- Catalog record: ARM data-source index, `instrument_class_code=radclss`, read 2026-09-24
- Example file: `bnfcsapr2radclssS3.c2.20250619.000000.nc` from `bnfcsapr2radclssS3.c2`, 3.5 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
