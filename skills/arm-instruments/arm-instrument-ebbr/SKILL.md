---
name: arm-instrument-ebbr
description: ARM Energy Balance Bowen Ratio Station (ebbr) - handbook-derived instrument reference. Measurement principle, reported quantities (Sensible Heat Flux, Latent Heat Flux, Net Radiation, Average Soil Surface Heat Flux, Air temperature, Temperature/RH Probe - Temperature, Temperature/RH Probe - RH, Soil Temperature), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgp5ebbrE13.b1) and the variable inventory of a real file. Use when working with ebbr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric; Surface/Subsurface Properties. Triggers - ebbr, Energy Balance Bowen Ratio Station, sgp5ebbrE13.b1, Sensible Heat Flux, Latent Heat Flux, Net Radiation, Average Soil Surface Heat Flux, Air temperature, Temperature/RH Probe - Temperature, Radiometric.
---

# EBBR - Energy Balance Bowen Ratio Station

The EBBR system produces 30-minute estimates of the vertical fluxes of sensible and latent heat at the local surface, deployed at ARM Southern Great Plains extended facilities including the Central Facility.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 28 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ebbr` |
| Handbook | [DOE/SC-ARM-TR-037 / DR Cook, RC Sullivan / May 2025](https://www.arm.gov/publications/tech_reports/handbooks/ebbr_handbook.pdf) |
| Measurement category | Radiometric; Surface/Subsurface Properties |
| Manufacturer / model | Radiation and Energy Balance Systems, Inc. (REBS) - system called SEBS (surface energy balance system); components include REBS Q*7.1 Net Radiometer, REBS SMP-2 Soil Moisture Probes, REBS HFT-3 Soil... |
| Primary measurements | Latent heat flux; Net broadband total irradiance; Sensible heat flux; Soil heat flux |
| Record | 1993-07-04 to 2026-09-23 (active) |
| Datastreams with data | 66 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/ebbr |


## Credit

Everything this skill knows about the instrument is the work of **DR Cook, RC Sullivan** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> DR Cook, RC Sullivan. *Energy Balance Bowen Ratio (EBBR) Instrument Handbook*, DOE/SC-ARM-TR-037, May 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ebbr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The EBBR uses a standard Bowen ratio approach in which the surface energy balance equation q + ave_shf + h + e = 0 is solved using measurements of net radiation, soil surface heat flux, and the vertical gradients of temperature and vapor pressure (derived from RH and temperature) at two fixed heights within three meters of the surface. The Bowen ratio B = h/e is computed from these gradients assuming the transfer coefficients of heat and water vapor are the same, and then e = -(q + ave_shf)/(1 + B) and h = B*e are calculated. The automatic exchange mechanism (AEM) periodically swaps the gradient-measuring instrumentation between top and bottom positions every 15 minutes to reduce errors from instrument offset drift. Soil heat flow is measured with heat flow plates at 5 cm combined with soil energy storage from temperature probes in the 0-5 cm layer, averaged over five sensor sets to obtain ave_shf.

**Siting.** EBBR data are collected only at ARM SGP extended facilities where the local surface is not tilled; sensors mounted on triangular pipe framework on soil surface; net radiometer at south end, AEM (with aspirated shields) at north end facing north to reduce radiation error; local area of influence is approximately 20 times the height of the top aspirated radiation shield on the AEM; heights of AEM aspirators vary by facility depending on max vegetation height with 1 m vertical separation between the two; data are only useful for particular wind directions at each facility due to insufficient fetch outside those ranges (minimum fetch of 120 m based on 1/40 height-to-fetch ratio); surface...

**Sampling.** native rate 5 minutes (base sampling for some variables); reported every 30 minutes (primary variables); also 15 minute and 5 minute secondary/diagnostic data available; averaging AEM switches gradient measuring instrumentation between top and bottom positions every 15 minutes; 30-minute values are computed from these (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sensible Heat Flux (h) | W/m^2 | - | 10% | - | (hb p. 8) |
| Latent Heat Flux (e) | W/m^2 | - | 10% | - | (hb p. 8) |
| Net Radiation (q) | W/m^2 | - | 5% | - | (hb p. 8) |
| Average Soil Surface Heat Flux (ave_shf) | W/m^2 | - | 10% | - | (hb p. 8) |
| Air temperature (thermocouple) | degC | -30 to 40°C | +/- 0.5°C | - | (hb p. 23) |
| Temperature/RH Probe - Temperature (PRTD) | degC | -30 to 40°C | +/- 0.2°C | - | (hb p. 23) |
| Temperature/RH Probe - RH | % RH | 0% to 100% | +/- 2% (0-90% RH), +/- 3% (90-100%);... | - | (hb p. 23) |
| Soil Temperature (PRTD) | degC | -30 to 40°C | +/- 0.5°C | - | (hb p. 23) |
| Soil Moisture | % by volume | approximately 1% to 50% by volume (SGP... | not specified by manufacturer | - | (hb p. 23) |
| Soil Heat Flow | - | - | not specified by manufacturer | - | (hb p. 24) |
| Barometric Pressure | kPa | 24 to 30 kPa (090C-24/30-1); 26 to 32... | +/- 0.14 kPa | - | (hb p. 24) |
| Net Radiation (radiometer) | - | - | +/- 5% of full-scale reading | - | (hb p. 24) |
| Wind Direction | degrees | 0 to 360° physical (for greater than... | +/- 3° | - | (hb p. 24) |
| Wind Speed | ms-1 | 0.27 to 50 ms-1; Operational Limit 60... | +/- 1% of reading | - | (hb p. 24) |
| Data Logger accuracy | - | varies by voltage range selected | +/- 0.1% of full-scale reading | - | (hb p. 24) |


## Specifications

| parameter | value | source |
|---|---|---|
| Air temperatures sensor | Chromel-constantan thermocouple, Omega Engineering Inc., REBS Model # ATP-1, Detection Limits -30 to 40°C, Accuracy +/- 0.5°C | (hb p. 23) |
| Temperature/RH Probe | Operating Temperature Range -20 to 60°C; Temperature: PRTD, Detection Limits -30 to 40°C, Accuracy +/- 0.2°C; RH: Capacitive element, Vaisala Inc.,... | (hb p. 23) |
| Soil Temperature sensor | Platinum Resistance Temperature Detector, MINCO Products, Inc., REBS Model # STP-1, MINCO Model # XS11PA40T260X36(D), Detection Limits -30 to 40°C,... | (hb p. 23) |
| Soil Moisture sensor | Soil Moisture Probe (fiberglass and stainless steel screen mesh sandwich), REBS Model # SMP-1, accuracy not specified; detection limits approximately... | (hb p. 23) |
| Soil Heat Flow sensor | Soil Heat Flow Probes, Radiation & Energy Balance Systems, Inc., Model #s HFT-3, HFT3.1, Accuracy not specified by manufacturer | (hb p. 24) |
| Barometric Pressure sensor | Met One Instruments, Model #s 090C-24/30-1 (24-30 kPa), 090C-26/32-1 (26-32 kPa), 090D-26/32-1 (26-32 kPa), Accuracy +/- 0.14 kPa | (hb p. 24) |
| Net Radiometer | Radiation & Energy Balance Systems, Inc., Model Q*6.1 or Q*7.1, Accuracy +/- 5% of full-scale reading | (hb p. 24) |
| Wind Direction Sensor | Met One Instruments, Model #s 5470, 020C, Detection Limits 0 to 360° physical (greater than 0.3 ms-1), 0 to 356° electrical, Accuracy +/- 3° | (hb p. 24) |
| Wind Speed Sensor | Met One Instruments, model #s 010B and 010C, Operating Temperature Range -50 to 85°C, Detection Limits 0.27 to 50 ms-1, Accuracy +/- 1% of reading,... | (hb p. 24) |
| Data Logger | Campbell Scientific, Inc., Model CR10, Detection Limits vary by voltage range selected, Accuracy +/- 0.1% of full-scale reading | (hb p. 24) |


## The data

Verified example: **`sgp5ebbrE13.b1`**, file `sgp5ebbrE13.b1.20231215.000000.nc`
(0.06 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=288, `bound`=2 |
| Data variables | 38 |
| QC variables | 16 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2023-12-15T00:00:00 to 2023-12-15T23:55:00 |
| sampling interval | 30 seconds |
| averaging interval | 3 minutes averages for outputs at 0,15,30 and 45 minutes. 5 minutes averages for all... |
| dod version | 5ebbr-b1-4.0 |
| process version | ingest-ebbr-10.1-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `atmos_pressure` | kPa | time | yes | Atmospheric pressure |
| `home_signal` | mV | time | yes | AEM position indicator |
| `net_radiation` | W/m^2 | time | yes | Net radiation |
| `rh_bottom_fraction` | 1 | time | yes | Bottom relative humidity (fractional) |
| `rh_top_fraction` | 1 | time | yes | Top relative humidity (fractional) |
| `temp_air_bottom` | degC | time | yes | Bottom air temperature |
| `temp_air_top` | degC | time | yes | Top air temperature |
| `temp_reference` | degC | time | yes | Reference temperature in enclosure |
| `temp_trh_bottom` | degC | time | yes | Bottom T/RH sensor temperature |
| `temp_trh_top` | degC | time | yes | Top T/RH sensor temperature |
| `vapor_pressure_bottom` | kPa | time | yes | Bottom vapor pressure |
| `vapor_pressure_top` | kPa | time | yes | Top vapor pressure |
| `wdir_vec_mean` | degree | time | yes | Wind direction vector mean |
| `wdir_vec_std` | degree | time | yes | Wind direction vector mean standard deviation |
| `wspd_arith_mean` | m/s | time | yes | Wind speed arithmetic mean |
| `wspd_vec_mean` | m/s | time | yes | Wind speed vector mean |
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
                     params={"user": f"{user}:{token}", "ds": "sgp5ebbrE13.b1",
                             "start": "2023-12-15", "end": "2023-12-15", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp5ebbrE13.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp5ebbrE13.b1", "2023-12-15", "2023-12-15")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgp5ebbrE13.b1", "2023-12-15", "2023-12-15"))   # cite what you pulled
```

## Quality control in this datastream

16 `qc_` companion variables cover 16 of the
38 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_temp_reference"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("temp_reference", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["temp_reference", "temp_air_top", "temp_air_bottom"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgp5ebbrE13.b1.20231215.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `rh_top_fraction` | Value is greater than fail_max | 160 | 55.5556 |
| `rh_bottom_fraction` | Value is greater than fail_max | 157 | 54.5139 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgp5ebbrE13.b1", "19930704", "20260923")
```

The handbook's own note on data quality: QC flags (qcmin#, qcmax#, qcdelta#) are provided in the 30-, 15-, and 5-minute data streams as 24-bit binary numbers; bits 6 and 7 of qcmin49-72/qcmax49-72 relate to home_15 and home_30 AEM signal checks. QC flags should routinely be used for all variables, but for some (e.g., ave_shf, e, h) flags were not set until late May 1998. The Bowen QC flag is frequently and legitimately tripped near sunrise/sunset due to near-zero temperature gradients and should not be reported as a data quality issue in DQO assessments. hum_top/hum_bot QC flags trip when RH exceeds a threshold, but since the RH...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Sunrise/sunset spikes in sensible and latent heat flux when Bowen ratio near -1 | Sharp spikes in h and e time series near sunrise/sunset, with Bowen ratio annotated near -1 on plots; Bowen QC flag frequently tripped at these times | Do not require DQR since occurs frequently; BA EBBR VAP replaces spiked data with bulk aerodynamic technique fluxes; when Bowen ratio is between -1.6... | (hb p. 6) |
| AEM (automatic exchange mechanism) malfunction | home_15 and home_30 values outside normal ranges (40-55 for home_15, 15-30 for home_30); if both home values are nearly identical in 30-minute data, at least one is incorrect; qcmin/qcmax... | Use QC flags to detect AEM state; sensible/latent heat flux unreliable and should not be used when AEM not functioning, even if flux estimates appear... | (hb p. 9) |
| AEM home signal limit checks not properly set prior to April 7, 1993 | qcmin#/qcmax# flags unreliable for data before this date | Inspect home_15 and home_30 directly rather than relying on qcmin#/qcmax# for data collected prior to April 7, 1993 | (hb p. 9) |
| AEM fuse blown | home_15 and/or home_30 values of zero (though an exception showed -2.0 at E15 Ringwood, OK in May 1994) | Usually caused by friction from freezing rain/snow, dirt buildup, or electrical/electronic failure; identified via DQRs | (hb p. 10) |
| AEM stuck at one position (usually right housing stuck down) | home_15 and home_30 signals both equal to the proper home_30 value (if fuse intact); exception noted at CF in late 1992 when both home signals were 35 | none stated beyond noting condition | (hb p. 10) |
| AEM stuck between 15- and 30-minute positions | Small negative home value for both home_15 and home_30 (e.g., -0.2) | none stated | (hb p. 10) |
| AEM removed for service | Home signals show anomalous values (e.g., 67-73) or float to the thousands when AEM circuitry absent | AEM replaced/refurbished and reinstalled, home signals return to normal | (hb p. 10) |
| RH probe offset drift | Gradual drift of about +2% per year in RH readings due to aging and dirt contamination of sensing element; also seen in Tower and MET RH probes | Does not significantly affect 30-minute vapor pressure difference since RH probes drift at similar rates and AEM exchanging reduces offset effects;... | (hb p. 9) |
| Battery/power supply degradation affecting AEM home signal | Home signal levels lower than normal, varying diurnally; can fall to unacceptable levels for 15-minute value | DQRs written to identify problems when low battery allows some sensors to function while others do not | (hb p. 8) |
| Condensation or frost on net radiometer upper polyethylene dome | Anomalous net radiation readings persisting into daylight hours | none stated beyond noting as common problem | (hb p. 6) |
| Net radiometer desiccant degradation | Degraded net radiometer performance/readings | none stated | (hb p. 6) |
| Holes in net radiometer top dome from bird claws | Water intrusion into net radiometer if dome not replaced before precipitation | Replace dome before precipitation occurs | (hb p. 6) |
| Soil sensors pulled from ground or chewed by animals | Missing or anomalous soil sensor readings (sm, ts, shf variables) | none stated beyond routine maintenance detection | (hb p. 6) |
| Blown fuse in AEM from belt/track binding | AEM stops switching; home signal anomalies | none specific stated | (hb p. 6) |
| Seized bearings in wind instruments | Erratic or stuck wind speed/direction readings | none stated | (hb p. 6) |
| Aging of sensors and electronic components | Gradual drift or degraded accuracy over time | Periodic recalibration program every two years | (hb p. 6) |
| Loosened electronic connections | Intermittent or erroneous data | Detected/corrected via preventative maintenance visits every two weeks | (hb p. 6) |
| Insufficient fetch for certain wind directions at each site | Data invalid/unreliable for wind directions outside the site-specific valid ranges listed in Section 6.3 | Use listed valid wind direction ranges per extended facility; required minimum fetch of 120 m (1/40 height-to-fetch ratio) | (hb p. 20) |
| EBBR net radiation disagreement with SIRS net radiation at low effective sky temperature | EBBR net radiometer sensitivity decreases rapidly below about -20°C effective sky temperature; nighttime sensible heat flux over/underestimated, nighttime latent heat flux overestimated... | Use IRT, AERI, or SIRS net radiation measurements instead under low effective sky temperature conditions; errors are within 10% system error of EBBR | (hb p. 13) |
| Longwave calibration of net radiometer not valid at very low temperatures | REBS longwave calibration not performed below about -30°C, causing inaccurate low effective sky temperature measurements | none stated beyond noting limitation | (hb p. 19) |
| EBBR atmospheric pressure insufficient accuracy for some applications | Pressure values less accurate/precise than MET pressure data | Use MET pressure data instead for applications like geostrophic wind calculations | (hb p. 7) |
| EBBR soil moisture/temperature inadequate for hydrological/land-surface models | Soil measurements represent only top 5 cm, not representative of root zone | Use SWATS soil moisture and temperature data instead for modeling efforts | (hb p. 11) |
| Surface soil heat flux term cannot be precisely recalculated from raw information | ave_shf recalculation from raw data introduces a few percent error in recomputed sensible/latent heat flux | Recompute sensible/latent heat flux using remaining working soil probe sets when some probes fail; error only a few percent | (hb p. 8) |
| QC flags not set for some variables until late May 1998 | Missing QC flags for ave_shf, e, h in older data records | Inspect data manually using knowledge of typical value ranges (e.g., Bowen ratio signs/magnitudes) when QC flags unavailable | (hb p. 9) |


_7 further items in the handbook._

## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Net Radiometer calibrated in temperature-controlled black-body cavity chamber against a transfer standard (tungsten-halide lamp source); transfer standard also calibrated by comparison to an Eppley precision pyranometer outdoors using a shading technique; wind speed effects considered by ventilating radiometers during... (hb p. 25) |
| Calibration interval | EBBR units returned to REBS approximately every two years for recalibration of all sensors and data logger equipment; RH probe recalibration after two years of use recommended; time between recalibrations has sometimes exceeded two years due to logistics (hb p. 25) |
| Traceability | Transfer standard traceable to NIST through the Eppley pyranometer using a shading technique (hb p. 25) |
| Routine maintenance | Preventative maintenance visits and instrument mentor quality assurance activities designed to detect and correct common instrumentation problems; SGP Site Operations personnel maintain preventative maintenance, corrective maintenance, and engineering logs per written procedures; six-month EBBR checks maintained on... (hb p. 13) |
| Maintenance interval | Preventative maintenance visits every two weeks; six-month checks; recalibration approximately every two years (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ECOR (eddy correlation flux measurement system), MET (surface meteorological instrumentation), SIRS (solar and infrared station), SWATS (soil water and temperature system), IRT (infrared thermometer), AERI (atmospheric emitted radiance interferometer), BA EBBR VAP.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AEM` | automatic exchange mechanism |
| `BA` | Bulk Aerodynamic Technique |
| `Bowen Ratio` | the ratio of the sensible heat flux to the latent heat flux |
| `Latent Heat Flux` | the transfer of latent heat (heat released or absorbed by water) between the surface and... |
| `Net Radiation` | the net difference in downwelling and upwelling solar plus terrestrial radiation |
| `Sensible Heat Flux` | the transfer of sensible heat (enthalpy) between the surface and the air, or vice versa |
| `Soil Heat Flow` | the transfer of sensible heat (enthalpy) in the soil, towards the surface or away from... |
| `SEBS` | surface energy balance system (manufacturer's name for the EBBR system) |
| `ECOR` | eddy correlation flux measurement system |
| `SWATS` | soil water and temperature system |
| `SIRS` | solar and infrared station |
| `MET` | surface meteorological instrumentation |


### References the handbook cites

- Brutsaert, WH. 1982. Evaporation in the Atmosphere. D. Reidel Publishing Company
- Wesely, MW, DR Cook, and RL Coulter. 1995. Surface Heat Flux Data from Energy Balance Bowen Ratio Systems.
- Fritschen, LJ, P Qian, ET Kanemasu, D Nie, EA Smith, JB Steward, SB Verma, and ML Wesely. 1992. Comparisons of surface flux measurement systems used in FIFE 1989. JGR 97(D17): 18,697-18,713
- Fritschen, LJ, and LW Gay. 1979. Environmental Instrumentation. Springer-Verlag
- Heilman, JL, and CL Brittin. 1989. Fetch requirements for Bowen ratio measurements of latent and sensible heat fluxes. Agricultural and Forest Meteorology 44(3-4): 261-273
- Lewis, JM. 1995. The story behind the Bowen ratio. BAMS 76(12): 2433-2443
- Halldin, S, and A Lindroth. 1992. Errors in net radiometry: Comparison and evaluation of six radiometer designs. JAOT 9(6): 762-783
- Field, RT, L Fritschen, ET Kanemasu, EA Smith, J Stewart, S Verma, and W Kustas. 1992. Calibration, comparison, and correction of net radiation instruments used during FIFE. JGR 97(D17): 18681-18695
- Fritschen, L, and JR Simpson. 1989. Surface energy and radiation balance systems: General description and improvements. Journal of Applied Meteorology 28(7): 680-689

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ebbr_handbook.pdf (28 pages, DOE/SC-ARM-TR-037, by DR Cook, RC Sullivan)
- Catalog record: ARM data-source index, `instrument_class_code=ebbr`, read 2026-09-23
- Example file: `sgp5ebbrE13.b1.20231215.000000.nc` from `sgp5ebbrE13.b1`, 0.06 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
