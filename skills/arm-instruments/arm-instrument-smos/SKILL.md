---
name: arm-instrument-smos
description: ARM Surface Meteorological Observation System Instruments for SGP (smos) - handbook-derived instrument reference. Measurement principle, reported quantities (Wind Speed, Vector Average Wind Speed, Wind Direction, Temperature, RH, Vapor Pressure, Barometric Pressure), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgp30smosA5.a1) and the variable inventory of a real file. Use when working with smos data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Radiometric; Surface Meteorology. Triggers - smos, sgp30smosA5.a1, Wind Speed, Vector Average Wind Speed, Wind Direction, Temperature, RH, Radiometric, Surface Meteorology, Campbell Scientific (data logger CR10, storage module SM716, RMSE, SMOS, T/RH, Precipitation.
---

# SMOS - Surface Meteorological Observation System Instruments for SGP

SMOS uses conventional in-situ sensors on a 10-m (or 20-m at the forested E21 site) tower to obtain 1-, 30-, and 1440-minute averages of wind speed/direction, air temperature, relative humidity, barometric pressure, precipitation, and (formerly) snow depth at the Central Facility and many extended facilities of the SGP climate research site.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 34 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `smos` |
| Handbook | [DOE/SC-ARM/TR-031 / M.T. Ritsche / March 2008](https://www.arm.gov/publications/tech_reports/handbooks/smos_handbook.pdf) |
| Measurement category | Radiometric; Surface Meteorology |
| Manufacturer / model | Campbell Scientific (data logger CR10, storage module SM716, T/RH probe HMP35C); R.M. Young Company (Wind Monitor Model 05103, radiation shields Model 41002 and Model 43408); Vaisala (barometer Model... |
| Primary measurements | Atmospheric moisture; Atmospheric pressure; Atmospheric temperature; Atmospheric turbulence; Horizontal wind; Precipitation |
| Record | 1997-04-22 to 2004-04-01 (retired) |
| Datastreams with data | 10 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/smos |


## Credit

Everything this skill knows about the instrument is the work of **M.T. Ritsche** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> M.T. Ritsche. *Surface Meteorological Observation System (SMOS) Handbook*, DOE/SC-ARM/TR-031, March 2008.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/smos_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The wind monitor propeller anemometer produces a magnetically controlled AC output whose frequency is proportional to wind speed, while the wind vane drives a potentiometer forming part of a resistance bridge to sense direction. The T-RH probe thermistor is part of a resistance bridge for temperature, and the Vaisala RH circuitry produces a voltage proportional to the capacitance of a water-vapor-absorbing thin polymer film. The barometric pressure sensor uses a silicon capacitive pressure sensor. The snow depth sensor (when in service) determined distance to the surface by measuring the travel time of ultrasonic pulses. The tipping-bucket rain/snow gauge funnels heated, melted precipitation to a tipping bucket that triggers a magnetic reed switch, with pulses counted by the data logger. Vapor pressure is computed from air temperature and RH; vector-averaged wind speed and direction are computed from orthogonal u and v components of one-second wind samples.

**Siting.** SMOS sensors mounted on a 10-m triangular tower at most sites: Wind Monitor at 10 m on a cross-arm, T-RH probe in radiation shield at 2 m on southwestern leg, snow depth sensor at ~1.5 m boom, barometric sensor/data logger enclosure at 1 m, rain-snow gauge near tower with 12-in orifice and Alter Shield. Central Facility (E13) uses an aspirated radiation shield (Model 43408) instead of the naturally aspirated multi-plate shield (Model 41002) used elsewhere. At E21 (Okmulgee, OK, forested site) sensors are on a 20-m tower extending above the canopy (~14.3 m canopy height): T/RH at 17.0 m (2.7 m above canopy) facing north, wind sensor at 18 m (3.7 m above canopy) facing north, barometric...

**Sampling.** native rate Each input measured once per second, except barometric pressure (once per minute) and snow depth (every 3 min); reported every 1 min, 30 min, and 1440 min (daily); averaging 1-min and 30-min averages computed from 1-second samples (except barometric pressure measured once per minute, snow depth measured every 3 min); vector averaging used for wind speed and direction (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Wind Speed | m/s | - | +/- 2% for 2.5 to 30 m/s | 0.01 | (hb p. 6) |
| Vector Average Wind Speed | m/s | - | - | 0.01 | (hb p. 6) |
| Wind Direction | deg | - | +/- 5 deg | 0.1 | (hb p. 6) |
| Standard Deviation of Wind Direction | deg | - | - | 0.1 | (hb p. 6) |
| Temperature | C | - | a function of wind speed | 0.01 | (hb p. 6) |
| RH | % | - | +/- 2.06% RH (0% to 90% RH), +/- 3.04% RH (90%... | 0.1 | (hb p. 7) |
| Vapor Pressure | kPa | - | - | 0.001 | (hb p. 7) |
| Barometric Pressure | kPa | - | +/- 0.035 kPa | 0.1 | (hb p. 7) |
| Snow Depth | mm | - | +/- 10 mm plus any offset error | 0.1 | (hb p. 7) |
| Precipitation Total | mm | - | +/- 0.254 mm (unknown during strong winds and... | 0.001 | (hb p. 7) |
| Maximum Wind Speed | m/s | - | - | 0.01 | (hb p. 7) |
| Minimum Wind Speed | m/s | - | - | 0.01 | (hb p. 7) |
| Maximum Temperature | C | - | - | 0.01 | (hb p. 7) |
| Minimum Temperature | C | - | - | 0.01 | (hb p. 7) |
| Maximum RH | % | - | - | 0.1 | (hb p. 7) |
| Minimum RH | % | - | - | 0.1 | (hb p. 7) |
| Maximum Vapor Pressure | kPa | - | - | 0.001 | (hb p. 7) |
| Minimum Vapor Pressure | kPa | - | - | 0.001 | (hb p. 7) |
| Maximum Barometric Pressure | kPa | - | - | 0.01 | (hb p. 7) |
| Minimum Barometric Pressure | kPa | - | - | 0.01 | (hb p. 8) |
| Maximum Snow Depth | mm | - | - | 0.1 | (hb p. 8) |
| Minimum Snow Depth | mm | - | - | 0.1 | (hb p. 8) |


## Specifications

| parameter | value | source |
|---|---|---|
| Wind speed at 10 m | Precision: 0.01 m/s; Uncertainty: +/- 2% for 2.5 to 30 m/s | (hb p. 13) |
| Wind direction at 10 m | Precision: 0.1 deg; Uncertainty: +/- 5 deg | (hb p. 13) |
| Air temperature at 2 m | Precision: 0.01 degC; Uncertainty: a function of wind speed | (hb p. 13) |
| Relative humidity at 2 m | Precision: 0.1% RH; Uncertainty: +/- 2.06% RH (0% to 90% RH), +/- 3.04% RH (90% to 100% RH) | (hb p. 13) |
| Barometric pressure at 1 m | Precision: 0.01 kPa; Uncertainty: +/- 0.035 kPa | (hb p. 13) |
| Precipitation | Precision: 0.254 mm; Uncertainty: +/- 0.254 mm (unknown during strong winds and for snow) | (hb p. 13) |
| Snow depth | Precision: 0.1 mm; Uncertainty: +/- 10 mm plus any offset error. Removed from service August 2002 | (hb p. 13) |
| Data Acquisition (A/D converter) accuracy | +/- 0.2% of full-scale range | (hb p. 13) |
| Data logger time base accuracy | +/- 1 min per month, or about 23 ppm | (hb p. 13) |
| Wind speed sensor threshold | 1 m/s | (hb p. 16) |
| Wind speed NIST calibration uncertainty | +/- 2% for wind speeds from sensor threshold to 30 m/s | (hb p. 16) |
| Wind direction sensor accuracy | +/- 3 deg | (hb p. 16) |
| Wind direction A/D conversion accuracy | +/- 0.7 deg over 0 to 40 degC for one year | (hb p. 16) |
| Wind direction sensor alignment to true north | estimated accurate within +/- 3 deg | (hb p. 16) |
| Temperature sensor accuracy | +/- 0.4 degC | (hb p. 16) |
| Naturally aspirated shield radiation error | +/- 0.4 degC rms at 3 m/s, +/- 0.7 degC rms at 2 m/s, +/- 1.5 degC rms at 1 m/s | (hb p. 16) |
| Aspirated shield (Central Facility) radiation error | +/- 0.2 degC rms | (hb p. 17) |
| RH sensor accuracy | +/- 2% RH for 0 to 90% RH, +/- 3% RH for 90 to 100% RH | (hb p. 17) |
| RH A/D conversion accuracy | +/- 0.5% RH | (hb p. 17) |
| Barometric pressure uncertainty | +/- 0.035 kPa (95% confidence) | (hb p. 17) |
| Precipitation gauge collection efficiency | 99% to 100% for rain rates less than 75 mm per hour with light to moderate winds | (hb p. 17) |
| Data logger | Campbell Scientific Model CR10 Measurement & Control Module and Model SM716 Storage Module; Precision: function of input type and range; Uncertainty:... | (hb p. 13) |


## The data

Verified example: **`sgp30smosA5.a1`**, file `sgp30smosA5.a1.20040329.000000.cdf`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

**Reading note.** read with use_base_time=True: the file time units string is not CF-decodable.

|  |  |
|---|---|
| Dimensions | `time`=48 |
| Data variables | 35 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1800 s |
| File time span | 2004-03-29T00:30:00 to 2004-03-30T00:00:00 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `albedo` | - | time | - | surface albedo |
| `bar_pres` | kPa | time | - | Barometric Pressure |
| `down_solar_rad` | W/m**2 | time | - | downwelling, hemispheric solar radiation |
| `max_bar_pres` | kPa | time | - | Maximum Barometric Pressure |
| `max_rh` | % | time | - | Maximum Relative Humidity |
| `max_temp` | C | time | - | Maximum Temperature |
| `max_vap_pres` | kPa | time | - | Maximum Vapor Pressure |
| `max_wspd` | m/s | time | - | Maximum of Wind speed |
| `min_bar_pres` | kPa | time | - | Minimum Barometric Pressure |
| `min_rh` | % | time | - | Minimum Relative Humidity |
| `min_temp` | C | time | - | Minimum Temperature |
| `min_vap_pres` | kPa | time | - | Minimum Vapor Pressure |
| `min_wspd` | m/s | time | - | Minimum of Wind speed |
| `par` | W/m**2 | time | - | photosynthetic active radiation |
| `precip` | mm | time | - | Precipitation Total |
| `rh` | % | time | - | Relative Humidity |
| `rn` | W/m**2 | time | - | net radiation |
| `sd_bar_pres` | kPa | time | - | Standard deviation of Barometric Pressure |
| `sd_deg` | m/s | time | - | Standard Deviation of Wind Direction |
| `sd_rh` | % | time | - | Standard deviation of Relative Humidity |
| `sd_temp` | C | time | - | Standard deviation of Temperature |
| `sd_vap_pres` | kPa | time | - | Standard deviation of Vapor Pressure |
| `sd_wspd` | m/s | time | - | Standard Deviation of Wind Speed |
| `temp` | C | time | - | Temperature |
| `up_solar_rad` | W/m**2 | time | - | upwelling, hemispheric solar radiation |
| `vap-pres` | kPa | time | - | Vapor Pressure |
| `vbat` | volts | time | - | battery voltage |
| `wdir` | deg | time | - | Wind Direction |
| `wspd` | m/s | time | - | Wind Speed |
| `wspd_va` | m/s | time | - | Wind Speed (vector averaged) |


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
                     params={"user": f"{user}:{token}", "ds": "sgp30smosA5.a1",
                             "start": "2004-03-29", "end": "2004-03-29", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp30smosA5.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp30smosA5.a1", "2004-03-29", "2004-03-29")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"

# this datastream's time units are not CF-decodable, so read base_time instead
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True, use_base_time=True)
print(act.discovery.get_arm_doi("sgp30smosA5.a1", "2004-03-29", "2004-03-29"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("wspd")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgp30smosA5.a1", "19970422", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Quality check results are output as qc_ variables with defined Min/Max/Delta bounds for each quantity (Table 4). Data Quality Health and Status (DQ HandS) and NCVweb tools at http://dq.arm.gov provide interactive review. The ARM Data Quality Office performs routine DQA assessments on recently collected data via weekly reports (http://dq.arm.gov/weekly_reports/weekly_reports.html) and tracks problem resolution via Data Quality Problem reports. VAPs and QMEs (Quality Measurement Experiments) provide continuous assessment of input data quality via internal consistency checks, comparisons between...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Incorrect alignment of towers to true north | Wind direction values offset by a fixed number of degrees during specific date ranges at sites EF3, EF4, EF6, EF7, EF27; improperly corrected data still in archive pending reprocessing... | Offsets determined and corrections applied to data logger programs; a request for reprocessing of improperly corrected data has been made; Table 7... | (hb p. 10) |
| Tower deviation from true north (uncorrected) | Systematic wind direction bias of a few degrees (e.g. -3 to +6 degrees) depending on site, not currently corrected in data | Data users are encouraged to correct the data on their own as necessary; no corrections currently made | (hb p. 11) |
| Snow depth sensors removed from service | snow, max_snow, min_snow, snow_sen variables remain in datastream as placeholders and should read -9999 after Summer 2002 | None; sensors permanently removed, variable retained as placeholder | (hb p. 11) |
| Error/placeholder flags during routine maintenance | Positive values of 6999 or 99999 (or high-resolution 99999) output when intermediate processing disabled during maintenance; negative -6999/-99999 output when sensor problem (overranging/no... | Differentiate maintenance-disabled state (positive flag values) from sensor-error state (negative flag values); recognize partial averaging periods... | (hb p. 8) |
| RH sensor upward drift over time | RH values reported by probe normally drift slowly upward over time; probe may report values exceeding 104% RH | Six-month sensor verification; probe replaced with recently calibrated one if outside uncertainty range or reporting greater than 104% RH; data... | (hb p. 9) |
| Snow depth data noisiness from ground clutter | Noisy snow depth data caused by sonic echoes from waving grass below the sensor; single reading taken every 30 min initially | PIF P951219.2 issued; data logger program changed in spring 1996 to average readings every 3 min | (hb p. 9) |
| Snow depth averaging program error | Program change in 1996 contained an error not discovered until summer 2001, affecting snow depth data quality for years before correction | Program corrected; snow depth data collected during winter 2001/2002 after fix | (hb p. 9) |
| Snow depth sensor instability leading to removal | Snow depth sensors found not very stable even after program correction | Sensors removed from service in August 2002 | (hb p. 9) |
| Wind speed underestimation near sensor threshold | Reported wind speeds near/below 2.5 m/s show a low bias; e.g., reported 0.5 m/s implies ~0.5 m/s underestimate, reported 1.0 m/s implies 0.19-0.30 m/s underestimate, reported 1.5 m/s... | None beyond noting propeller anemometer threshold of 1 m/s; uncertainty ranges provided by wind speed bin | (hb p. 16) |
| Wind speed sensor threshold (stall speed) | Anemometer does not respond below threshold of 1 m/s, causing systematic underestimation of low wind speeds assuming normal distribution about the mean | None stated beyond quantified underestimate ranges | (hb p. 16) |
| Temperature uncertainty degrades at low wind speed (radiation shield error) | Naturally aspirated multi-plate radiation shield radiation error increases as wind speed decreases: +/-0.4 degC rms at 3 m/s, +/-0.7 degC rms at 2 m/s, +/-1.5 degC rms at 1 m/s; 95%... | Central Facility uses aspirated radiation shield instead, giving lower and more uniform uncertainty (+/-0.2 degC rms, +/-0.57 degC at 95% confidence) | (hb p. 16) |
| Precipitation gauge collection efficiency reduced during heavy rain or strong/gusty winds | Precipitation totals underestimate true precipitation during high rain rates (greater than 75 mm/hr) or strong gusty winds; manufacturer has not specified accuracy for these conditions | None stated; use with caution | (hb p. 17) |
| Snow/frozen precipitation measurement unreliable | Water-equivalent estimates for snowfall are unreliable; heater does not melt snow below -10 degC, so precipitation may show zero or delayed/incorrect timing of precipitation if snow... | Data user should treat water-equivalent snowfall estimates with a great deal of skepticism; readings only a rough indicator that snow occurred above... | (hb p. 17) |
| Snow depth sensor height entry bias error | Snow depth computed by subtracting sensor reading from manually entered sensor height in logger program; error in that entered height produces a persistent bias in reported snow depth | None beyond calibration check with known-height object and offset adjustment | (hb p. 17) |
| T/RH check bias from earlier uncalibrated aspirated shield procedure | Six-month calibration checks done without an aspirated shield before 2000 showed many spurious T/RH sensor failures due to solar radiation heating and hot-vehicle effects during the check | Newer procedures enacted in 2000 along with an aspirated shield reduced incorrect failure determinations | (hb p. 15) |
| Wind Monitor 2-year factory recalibration not always performed | Gaps in the calibration history logs where wind monitors are not returned to manufacturer for 2-year recalibration in some years due to funding | Handbook states this should not lead to a problem overall since sensors rarely go out of calibration and are checked every 6 months in the field | (hb p. 15) |
| Data interruption during field calibration checks | Data flow interrupted and gaps appear in record because 10-m tower must be lowered for 6-month calibration checks | A Data Quality Report (DQR) is usually issued to note the loss of data | (hb p. 16) |
| SMOS not co-located with existing surface met networks | No SMOS installed at extended facilities within about 10 km of existing surface meteorological stations such as Oklahoma Mesonet, creating spatial data gaps in that radius | Users can obtain data from Oklahoma Mesonet, Kansas State network, or NOAA 404-MHz radar wind profiler surface stations as external data | (hb p. 4) |
| E21 Okmulgee site canopy/forest influence and boom reconfiguration | Sensor heights/orientations at E21 changed (wind sensor orientation changed from north to west facing on July 16, 2002 18:44 GMT; T/RH probe height and orientation changed July 15, 2002... | New booms installed July 2002; dates of changes documented for data users | (hb p. 15) |
| Lat/lon/alt refer to tower ground location, not sensor height | Dimension variables lat/lon/alt in data files represent the ground siting location, not the actual measurement height of a given sensor | Note included in Table 5 documentation to prevent misinterpretation | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Sensors and data logger (including A/D converter) calibrated separately, not as a system; wind speed checked via R.M. Young Model 18810 Anemometer Drive at fixed rpm's; wind direction checked via R.M. Young Model 18212 vane angle fixture; temperature/RH checked against reference Vaisala HMI31 Digital RH and... (hb p. 15) |
| Calibration interval | Every six months in the field by SGP site operations personnel; Wind Monitors returned to manufacturer for recalibration after two years of use per manufacturer suggestion (funding-dependent) (hb p. 15) |
| Traceability | Comparison to calibrated references; NIST calibration uncertainty specified for wind speed sensor (hb p. 15) |
| Routine maintenance | Field calibration checks every six months comparing sensors against calibrated references; sensor/probe replacement when out of tolerance; details at http://www.ops.sgp.arm.gov/pm_proc/smospm.htm (hb p. 15) |
| Maintenance interval | Six-month field calibration checks; Wind Monitors returned for 2-year factory PM and calibration (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Oklahoma Mesonet, Kansas State network, NOAA 404-MHz radar wind profiler surface meteorological stations.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `A/D` | analog-to-digital converter |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `DQA` | Data Quality Assessment |
| `RH` | relative humidity |
| `RMSE` | root-mean-square error |
| `SGP` | Southern Great Plains |
| `SMOS` | Surface Meteorological Observation System |
| `T/RH` | Temperature/Relative Humidity |
| `Barometric pressure` | Local station pressure measured at the SMOS station at a height of 1 m |
| `Precipitation` | All forms of water meteors |
| `Relative humidity` | Percentage of saturated vapor pressure at the specified temperature |
| `Vector-averaged wind...` | Wind speed computed as the vector sum of the orthogonal u and v components, which are... |
| `Wind Monitor` | Trade name for R. M. Young propeller anemometer and wind vane |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/smos_handbook.pdf (34 pages, DOE/SC-ARM/TR-031, by M.T. Ritsche)
- Catalog record: ARM data-source index, `instrument_class_code=smos`, read 2026-09-23
- Example file: `sgp30smosA5.a1.20040329.000000.cdf` from `sgp30smosA5.a1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
