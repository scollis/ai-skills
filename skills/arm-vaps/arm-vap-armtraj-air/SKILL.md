---
name: arm-vap-armtraj-air
description: ARM Airmass trajectories to support studies using ARM Aerial Facility (AAF) data. (armtraj-air) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Airmass latitude, Airmass longitude, Airmass height above ground level, Airmass pressure, Airmass temperature), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparmtrajtbsC1.c1) and the variable inventory of a real file. Use when working with armtraj-air data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Airborne Observations; Atmospheric Profiling. Triggers - armtraj-air, sgparmtrajtbsC1.c1, Airmass latitude, Airmass longitude, Airmass height above ground level, Airmass pressure, Airborne Observations, Atmospheric Profiling.
---

# ARMTRAJ-AIR - Airmass trajectories to support studies using ARM Aerial Facility (AAF) data.  

ARMTRAJ is a value-added product that computes HYSPLIT-based ensemble airmass back/forward trajectories initialized at ARM deployment coordinates (surface, cloud layers, PBL, cloud decks, AAF aircraft/UAS, TBS, and marine boundary layer isobaric levels) to support aerosol, cloud, PBL, and AAF/TBS-related research.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 176 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `armtraj-air` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-314 / I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei / August 2026](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf) |
| Category | Airborne Observations; Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2013-10-01 to 2026-09-10 (active) |
| Datastreams with data | 12 across 7 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/armtraj-air |


## Credit

Everything this skill knows about the retrieval is the work of **I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei** -
the ARM developers and mentors who wrote the technical report it derives from:

> I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei. *ARM Trajectories Data Set Value-Added Product Report*, DOE/SC-ARM-TR-314, August 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Extraction coverage.** the report is 176 pages and only about a quarter was read - body pages 1-21 plus the ARMTRAJ-AAF output listing in Appendix E - so the specification and variable lists here are partial. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

Trajectory calculations use the Hybrid Single-Particle Lagrangian Integrated Trajectory (HYSPLIT) model informed by the ECMWF fifth-generation atmospheric reanalysis (ERA5) data set at its highest spatial resolution (0.25 degrees; ~31 km). HYSPLIT runs at multiple initial starting locations surrounding ARM deployments (in latitude/longitude and/or vertical coordinates), forming an ensemble for each sample. All ARMTRAJ data sets include ensemble runs initialized at relatively small horizontal and vertical offsets from ARM site coordinates; except for the isobaric, AAF, and TBS data sets, horizontal offsets are fixed at ±7.5 km east-west and north-south, defining a 3x3 horizontal grid. For ARMTRAJ-ISOBAR, trajectories are calculated using only horizontal winds while following isobaric (constant pressure) surfaces rather than vertical wind reanalysis data, assuming quasi-horizontal air movement. ARMTRAJ reports the mean and standard deviation of all airmass coordinate and thermodynamic variables, with ensemble means increasing fidelity and the standard deviation serving as a measure of trajectory estimated uncertainty.

**Cadence.** output every Varies by data set: ARMTRAJ-SFC/ARSCL/ISOBAR every 3 hours (00,03,06,09,12,15,18,21 UTC); ARMTRAJ-CLD/PBL at SONDE release times rounded to nearest hour; ARMTRAJ-AAF/TBS at facility operation times in 1-hour increments; averaging 1-hour mean and standard deviation values of surface/instrument observations included, starting at trajectory initialization time (hb p. 9).

## Inputs

The report names these instruments and sibling products: SONDE (Balloon-Borne Sounding System), MET (Surface Meteorological System), ARSCL (Active Remote Sensing of Clouds VAP), PBLHT VAP (Planetary Boundary Layer Height VAP), TBS (Tethered Balloon System), AAF systems (aircraft, UAS), Microwave Radiometer (MWR).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Airmass latitude | degree_N | - | - | (hb p. 14) |
| Airmass longitude | degree_E | - | - | (hb p. 14) |
| Airmass height above ground level (height) | m | - | - | (hb p. 14) |
| Airmass altitude above mean sea level (altitude) | m | - | - | (hb p. 14) |
| Airmass pressure (pres) | hPa | - | - | (hb p. 14) |
| Airmass temperature (temp) | degC | - | - | (hb p. 14) |
| Airmass specific humidity (qv) | g/kg | - | - | (hb p. 14) |
| Airmass relative humidity (rh) | % | - | - | (hb p. 14) |
| Airmass relative humidity with respect to ice (rhi) | % | - | - | (hb p. 14) |
| Airmass potential temperature (theta) | K | - | - | (hb p. 14) |
| Airmass equivalent potential temperature (theta_e) | K | - | - | (hb p. 14) |
| Airmass virtual potential temperature (theta_v) | K | - | - | (hb p. 14) |
| Mean hourly ascent rate (wvert) | m/s | - | - | (hb p. 14) |
| Planetary boundary-layer height (PBLH) in airmass column | m | - | - | (hb p. 14) |
| Surface altitude in airmass column (surf_altitude) | m | - | - | (hb p. 14) |
| Airmass height-to-PBLH ratio | 1 | - | - | (hb p. 14) |
| Land/sea cover (land_sea_mask) | 1 (0.0=100% water,... | 0.0-1.0 | - | (hb p. 14) |
| Daily sea-ice cover | 1 | - | - | (hb p. 14) |
| Low vegetation type and cover | 1 | - | - | (hb p. 14) |
| High vegetation type and cover | 1 | - | - | (hb p. 14) |
| Soil type | 1 | - | - | (hb p. 14) |
| Subgrid-scale orography angle | radian | - | - | (hb p. 14) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| ARMTRAJ-SFC initialization time | 00, 03, 06, 09, 12, 15, 18, and 21 UTC | (hb p. 9) |
| ARMTRAJ-SFC ensemble members | 18 | (hb p. 9) |
| ARMTRAJ-SFC back trajectory period | 240 hours | (hb p. 9) |
| ARMTRAJ-CLD initialization time | SONDE release rounded to the nearest hour | (hb p. 9) |
| ARMTRAJ-CLD ensemble members | 27 per detected cloud layer | (hb p. 9) |
| ARMTRAJ-CLD back trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-CLD forward trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-PBL initialization time | SONDE release rounded to the nearest hour | (hb p. 9) |
| ARMTRAJ-PBL ensemble members | 99 (ensemble size of 9 in free-tropospheric runs) | (hb p. 9) |
| ARMTRAJ-PBL back trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-ARSCL initialization time | 00, 03, 06, 09, 12, 15, 18, and 21 UTC | (hb p. 9) |
| ARMTRAJ-ARSCL ensemble members | 99 | (hb p. 9) |
| ARMTRAJ-ARSCL back trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-ARSCL forward trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-AAF initialization time | Hours during which AAF systems are operated | (hb p. 9) |
| ARMTRAJ-AAF ensemble members | 25 per flight altitude | (hb p. 9) |
| ARMTRAJ-AAF back trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-TBS initialization time | Hours during which a TBS is operated | (hb p. 9) |
| ARMTRAJ-TBS ensemble members | 25 per flight altitude | (hb p. 9) |
| ARMTRAJ-TBS back trajectory period | 120 hours | (hb p. 9) |
| ARMTRAJ-ISOBAR initialization time | 00, 03, 06, 09, 12, 15, 18, and 21 UTC | (hb p. 9) |
| ARMTRAJ-ISOBAR ensemble members | 25 per initial height | (hb p. 9) |
| ARMTRAJ-ISOBAR back trajectory period | 48 hours | (hb p. 9) |
| ARMTRAJ-ISOBAR forward trajectory period | 48 hours | (hb p. 9) |
| ERA5 spatial resolution | 0.25 degrees; ~31 km | (hb p. 8) |
| Standard ensemble horizontal offset | ± 7.5 km east-west and north-south (3x3 grid, multiples of nine) | (hb p. 8) |


_17 further rows in the report._

## The data

Verified example: **`sgparmtrajtbsC1.c1`**, file `sgparmtrajtbsC1.c1.20241111.130000.nc`
(14.54 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

**Reading note.** use_base_time=True (time units not CF-decodable).

|  |  |
|---|---|
| Dimensions | `time`=11, `trajectory_time`=121, `vert_layer`=11, `time_tbs`=45876, `trajectory_type`=1 |
| Data variables | 261 |
| QC variables | 17 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2024-11-11T13:00:00 to 2024-11-11T23:00:00 |
| dod version | armtrajtbs-c1-2.0 |
| process version | armtraj-1.10.14 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `alt_tbsimet` | m | time_tbs | yes | (TBS) Altitude above mean sea level from GPS |
| `lat_tbsimet` | degree_N | time_tbs | yes | (TBS) Latitude in decimal degrees from GPS |
| `lon_tbsimet` | degree_E | time_tbs | yes | (TBS) Longitude in decimal degrees from GPS |
| `sea_ice_cover` | 1 | time,trajectory_time,vert_layer | yes | Sea-ice cover fraction (based on daily means) in airmass column |
| `sea_ice_cover_ens_mean` | 1 | time,trajectory_time,vert_layer | yes | Sea-ice cover fraction (based on daily means) in airmass column... |
| `sea_ice_cover_sfc` | 1 | time,trajectory_time | yes | Sea-ice cover fraction (based on daily means) in airmass column... |
| `sea_ice_cover_sfc_ens_mean` | 1 | time,trajectory_time | yes | Sea-ice cover fraction (based on daily means) in airmass column... |
| `wvert` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate |
| `wvert_ens_max` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate ensemble max |
| `wvert_ens_mean` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate ensemble mean |
| `wvert_ens_min` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate ensemble min |
| `wvert_ens_std` | m/s | time,trajectory_time,vert_layer | yes | Mean hourly airmass ascent rate ensemble std |
| `wvert_sfc` | m/s | time,trajectory_time | yes | Surface (at initialization) mean hourly airmass ascent rate |
| `wvert_sfc_ens_max` | m/s | time,trajectory_time | yes | Surface (at initialization) mean hourly airmass ascent rate ensemble... |
| `wvert_sfc_ens_mean` | m/s | time,trajectory_time | yes | Surface (at initialization) mean hourly airmass ascent rate ensemble... |
| `wvert_sfc_ens_min` | m/s | time,trajectory_time | yes | Surface (at initialization) mean hourly airmass ascent rate ensemble... |
| `wvert_sfc_ens_std` | m/s | time,trajectory_time | yes | Surface (at initialization) mean hourly airmass ascent rate ensemble... |
| `alt_max_tbsimet` | m | time | - | Altitude above mean sea level from GPS, 1-hour max (averaging window... |
| `alt_mean_tbsimet` | m | time | - | Altitude above mean sea level from GPS, 1-hour mean (averaging window... |
| `alt_min_tbsimet` | m | time | - | Altitude above mean sea level from GPS, 1-hour min (averaging window... |
| `alt_std_tbsimet` | m | time | - | Altitude above mean sea level from GPS, 1-hour std (averaging window... |
| `altitude_ens_max` | m | time,trajectory_time,vert_layer | - | Airmass altitude above mean sea level ensemble max |
| `altitude_ens_mean` | m | time,trajectory_time,vert_layer | - | Airmass altitude above mean sea level ensemble mean |
| `altitude_ens_min` | m | time,trajectory_time,vert_layer | - | Airmass altitude above mean sea level ensemble min |
| `altitude_ens_std` | m | time,trajectory_time,vert_layer | - | Airmass altitude above mean sea level ensemble std |
| `altitude_sfc` | m | time,trajectory_time | - | Surface (at initialization) airmass altitude above mean sea level |
| `altitude_sfc_ens_max` | m | time,trajectory_time | - | Surface (at initialization) airmass altitude above mean sea level... |
| `altitude_sfc_ens_mean` | m | time,trajectory_time | - | Surface (at initialization) airmass altitude above mean sea level... |
| `altitude_sfc_ens_min` | m | time,trajectory_time | - | Surface (at initialization) airmass altitude above mean sea level... |
| `altitude_sfc_ens_std` | m | time,trajectory_time | - | Surface (at initialization) airmass altitude above mean sea level... |


_211 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgparmtrajtbsC1.c1", "2024-11-11", "2024-11-11")
ds = armlive_open("sgparmtrajtbsC1.c1", "2024-11-11", "2024-11-11", cleanup_qc=True)
```

This product carries 261 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgparmtrajtbsC1.c1", start, end,
                  keep_variables=['alt_tbsimet', 'lat_tbsimet', 'lon_tbsimet', 'qc_alt_tbsimet', 'qc_lat_tbsimet', 'qc_lon_tbsimet'])
```

## Quality control in this product

17 `qc_` companion variables cover 17 of the
261 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgparmtrajtbsC1.c1.20241111.130000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sea_ice_cover_sfc_ens_mean` | airmass over land, sea-ice cover is N/A | 1331 | 100.0 |
| `sea_ice_cover_sfc` | airmass over land, sea-ice cover is N/A | 1331 | 100.0 |
| `sea_ice_cover_ens_mean` | airmass over land, sea-ice cover is N/A | 14419 | 98.4837 |
| `sea_ice_cover` | airmass over land, sea-ice cover is N/A | 14362 | 98.0944 |
| `alt_tbsimet` | Input QC indicated a bad value | 8253 | 17.9898 |
| `lat_tbsimet` | Value is equal to _FillValue. | 3356 | 7.3154 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgparmtrajtbsC1.c1", "20131001", "20260924")
```

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Lack of explicit mixing in the ECMWF IFS model driving ERA5 | PBL trajectory ensemble spread may not fully capture true boundary-layer mixing variability; mitigated by extensive 99-member ensemble configuration | ARMTRAJ-PBL uses an extensive ensemble configuration (11 heights, 99 members) to ameliorate this limitation | (hb p. 11) |
| Limited near-surface resolution of ERA5 pressure level grid (~250 m) | Coarse vertical resolution near the surface may smear near-surface trajectory height/thermodynamic gradients | Addressed via the same extensive PBL ensemble configuration | (hb p. 11) |
| Lowest PBLH floor of 100 m AGL set in HYSPLIT calculations | Reported PBLH values will not go below 100 m AGL even if true PBL is shallower | Considered in the ensemble configuration design | (hb p. 11) |
| Cloud-top height variability over averaging window (ARMTRAJ-ARSCL) | First radar-top height used for cloud top can be fairly variable over the 1-hour averaging period, affecting free-tropospheric height determination | Free-tropospheric height set as 1-hour mean cloud top plus its 1-hour standard deviation plus 200 m to account for variability | (hb p. 11) |
| Sparse/incorrect altitude reports from AAF/TBS systems (e.g., due to GPS lock loss) | Outlier minimum/maximum altitude values in AAFNAVAIMS/TBSIMET data that could skew trajectory initialization altitudes | Use of 1st and 99th altitude percentiles instead of system minimum/maximum values to mitigate influence of sparse, incorrect altitude reports | (hb p. 12) |
| Moving nature of AAF aircraft/UAS during 1-hour averaging window | Ensemble grid shape can become rectangular rather than square, and dimensions can range from 15x15 km up to 100x100 km depending on flight path/speed | Dynamic ensemble grid distance calculated separately for latitude and longitude, based on coordinate standard deviation over the 1-hour period,... | (hb p. 12) |
| Quasi-horizontal air movement assumption in ARMTRAJ-ISOBAR | Trajectories influenced by meso- to synoptic-scale lifting or orographic forcing will violate the isobaric assumption, showing physically implausible constant-pressure paths under strong... | Advised to filter trajectories believed to be influenced by dynamical forcing (e.g., synoptic lifting, orographic forcing); can restrict to... | (hb p. 13) |
| Non-zero land_sea_mask fractional values near trajectory initialization over coastal/land... | In the first few hours of an ISOBAR trajectory, land_sea_mask can show fractional values greater than 0.0 even though the site is meant to represent marine boundary layer, because ARM... | Handbook states these near-zero non-zero values could be acceptable given ARM deployments are typically over land at the coast | (hb p. 13) |
| Radiosonde-based cloud detection RH threshold and instrument uncertainty (ARMTRAJ-CLD) | Liquid-bearing cloud layer detection depends on a 96% RH threshold accounting for a 4% RH uncertainty in the Vaisala RS-41; layers thinner than 25 m or separated by more than 50 m are... | Threshold and concatenation/removal rules (samples within 50 m concatenated; layers less than 25 m thick removed) applied consistently with prior... | (hb p. 10) |
| Clear-sky periods produce no data files (ARMTRAJ-CLD and ARMTRAJ-ARSCL) | Gaps in the data set time series corresponding to clear-sky periods, since files are not generated when no liquid-bearing cloud layer or cloud deck is detected | None stated beyond noting files are not generated for clear-sky periods | (hb p. 10) |
| Dependence on SONDE availability for ARMTRAJ-CLD and ARMTRAJ-PBL initialization | Only 2 to 4 trajectory starting times per day for ARMTRAJ-PBL depending on radiosonde launch schedule, producing sparser temporal coverage than the 3-hourly data sets | None stated beyond describing the resulting frequency | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Stein et al. 2015 (HYSPLIT)
- Hersbach et al. 2020 (ERA5)
- Holdridge 2020 (SONDE Instrument Handbook)
- Kyrouac and Tuftedal 2024/2011 (MET Instrument Handbook)
- Sivaraman et al. 2013 (PBLHT VAP)
- Clothiaux et al. 2001 (ARSCL VAP)
- Dexheimer et al. 2024 (TBS Instrument Handbook)
- Mei et al. 2022 (Uncrewed Systems SGP)
- Schmid and Ivey 2016 (ARM UAS Implementation Plan)
- Silber et al. 2025 (ARMTRAJ data article, ESSD)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-314.pdf (176 pages, DOE/SC-ARM-TR-314, by I Silber, JM Comstock, MR Kieburtz, KL Gaustad, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=armtraj-air`, read 2026-09-24
- Example file: `sgparmtrajtbsC1.c1.20241111.130000.nc` from `sgparmtrajtbsC1.c1`, 14.54 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 176 pages and only about a quarter was read - body pages 1-21 plus the ARMTRAJ-AAF output listing in Appendix E - so the specification and variable lists here are partial
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
