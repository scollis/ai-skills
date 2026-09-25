---
name: arm-instrument-ldis
description: ARM Laser Disdrometer (ldis) - handbook-derived instrument reference. Measurement principle, reported quantities (Particle/drop diameter, Fall velocity, Precipitation intensity, Weather code, Equivalent radar reflectivity, Equivalent radar reflectivity, Number of detected particles), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpldC1.b1) and the variable inventory of a real file. Use when working with ldis data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface Meteorology. Triggers - ldis, Laser Disdrometer, sgpldC1.b1, Particle/drop diameter, Fall velocity, Precipitation intensity, Weather code, Equivalent radar reflectivity, Surface Meteorology, OTT Hydromet GmbH, Kempten, LDIS, LDQUANTS, NetCDF, TRACER.
---

# LDIS - Laser Disdrometer

The Laser Disdrometer (LDIS, an OTT Parsivel2 instrument) measures the size, fall velocity, and type of falling hydrometeors by detecting the shadowing of a horizontal laser beam, and is deployed at ARM fixed sites and mobile facilities to characterize precipitation.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 15 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ldis` |
| Handbook | [DOE/SC-ARM-TR-137 / Z Zhu, D Wang / September 2025](https://www.arm.gov/publications/tech_reports/handbooks/ldis_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | OTT Hydromet GmbH, Kempten, Germany - OTT Parsivel2 (second-generation particle size velocity disdrometer) |
| Primary measurements | Hydrometeor Size Distribution; Hydrometeor fall velocity; Hydrometeor size; Liquid water content; Precipitation; Snow depth |
| Record | 2014-01-01 to 2026-09-23 (active) |
| Datastreams with data | 47 across 19 sites |
| Sites | anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mao, mar |
| ARM page | https://www.arm.gov/capabilities/instruments/ldis |


## Credit

Everything this skill knows about the instrument is the work of **Z Zhu, D Wang** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> Z Zhu, D Wang. *Laser Disdrometer (LDIS) Instrument Handbook*, DOE/SC-ARM-TR-137, September 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ldis_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The OTT Parsivel2 (LDIS) operates on the principle of extinction, quantifying precipitation particles through the shadowing effect they induce as they traverse a laser band. The transmitter unit emits a flat, horizontally oriented beam of light, which is converted into an electrical signal by the receiver unit, and this signal changes whenever a hydrometeor passes through the beam within the measuring area. The extent of signal attenuation indicates the hydrometeor's size, and fall velocity is derived from the duration of the extinction signal. A fast signal processor provided by the vendor classifies particles into 32 size/velocity classes and calculates precipitation type, amount, intensity, kinetic energy, visibility, and equivalent radar reflectivity. The ratiometric process inherently accounts for temperature characteristics and laser diode aging, ensuring sustained accuracy.

**Siting.** LDIS deployed at ARM fixed-site observatories (SGP, ENA) and mobile facilities (AMFs) across various field campaigns; instrument uses a horizontally oriented laser beam requiring an unobstructed light pathway free of leaves, branches, or spider webs.

**Sampling.** reported every 1-minute intervals (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Particle/drop diameter (volume-equivalent) | mm | 0.06 to 24.5 mm | - | 32 unevenly spaced bins,... | (hb p. 7) |
| Fall velocity | m/s | 0.05 to 20.8 m/s | - | 32 unevenly spaced bins,... | (hb p. 7) |
| Precipitation intensity (precip_rate) | mm/hr | - | - | - | (hb p. 9) |
| Weather code (SYNOP WaWa Table 4680) | 1 | - | - | - | (hb p. 9) |
| Equivalent radar reflectivity (manufacturer, OTT) | dBZ | - | - | - | (hb p. 9) |
| Equivalent radar reflectivity (ARM-calculated) | dBZ | - | - | - | (hb p. 10) |
| Number of detected particles | count | - | - | - | (hb p. 9) |
| Meteorological optical range visibility (mor_visibility) | m | - | - | - | (hb p. 9) |
| Snow height (snow_depth_intensity) | mm/hr | - | - | - | (hb p. 9) |
| Liquid water content | mm3/m3 | - | - | - | (hb p. 10) |
| Intercept parameter (Marshall-Palmer type) | 1(m3 mm) | - | - | - | (hb p. 10) |
| Slope parameter (Marshall-Palmer type) | 1/mm | - | - | - | (hb p. 10) |
| Median volume diameter (Marshall-Palmer type) | mm | - | - | - | (hb p. 10) |
| Number density of drops | 1(m3 mm) | - | - | - | (hb p. 10) |
| Moments 1-6 of observed distribution | mm/m3 through mm6/m3 | - | - | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Nominal measuring area | 54 cm2 | (hb p. 7) |
| Effective sampling cross-section | 180 x (30 - L/2), where L is the size parameter | (hb p. 7) |
| Number of size/velocity bins | 32 unevenly spaced bins for both drop size and fall velocity | (hb p. 7) |
| Diameter measurement range | 0.06 to 24.5 mm | (hb p. 7) |
| Fall velocity measurement range | 0.05 to 20.8 m/s | (hb p. 7) |
| Precipitation type classes | 8 classes: drizzle, drizzle with rain, rain, rain and drizzle with snow, snow, snow grains, freezing rain, and hail | (hb p. 7) |


## The data

Verified example: **`sgpldC1.b1`**, file `sgpldC1.b1.20260919.000000.cdf`
(6.31 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `particle_size`=32, `raw_fall_velocity`=32 |
| Data variables | 42 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| sampling interval | 1 minute |
| dod version | ld-b1-2.0 |
| process version | ingest-ld-1.6-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `equivalent_radar_reflectivity_ott` | dBZ | time | yes | Radar reflectivity from the manufacturer's software |
| `heating_current` | A | time | yes | Heating current |
| `laserband_amplitude` | count | time | yes | Laserband amplitude |
| `mor_visibility` | m | time | yes | Meteorological optical range visibility |
| `number_detected_particles` | count | time | yes | Number of particles detected |
| `precip_rate` | mm/hr | time | yes | Precipitation intensity |
| `sensor_voltage` | V | time | yes | Sensor voltage |
| `snow_depth_intensity` | mm/hr | time | yes | New snow height |
| `weather_code` | 1 | time | yes | SYNOP WaWa Table 4680 |
| `class_size_width` | mm | particle_size | - | Class size width |
| `diameter_max` | mm | time | - | Diameter of largest drop observed |
| `diameter_min` | mm | time | - | Diameter of smallest drop observed |
| `equivalent_radar_reflectivity` | dBZ | time | - | Radar reflectivity calculated by the ingest |
| `fall_velocity_calculated` | m/s | raw_fall_velocity | - | Fall velocity calculated after Lhermite |
| `intercept_parameter` | 1/(m^3 mm) | time | - | Intercept parameter, assuming an ideal Marshall-Palmer type... |
| `liquid_water_content` | mm^3/m^3 | time | - | Liquid water content |
| `liquid_water_distribution_mean` | mm | time | - | Liquid water distribution mean, assuming an ideal Marshall-Palmer... |
| `median_volume_diameter` | mm | time | - | Median volume diameter, assuming an ideal Marshall-Palmer type... |
| `moment1` | mm/m^3 | time | - | Moment 1 from the observed distribution |
| `moment2` | mm^2/m^3 | time | - | Moment 2 from the observed distribution |
| `moment3` | mm^3/m^3 | time | - | Moment 3 from the observed distribution |
| `moment4` | mm^4/m^3 | time | - | Moment 4 from the observed distribution |
| `moment5` | mm^5/m^3 | time | - | Moment 5 from the observed distribution |
| `moment6` | mm^6/m^3 | time | - | Moment 6 from the observed distribution |
| `number_density_drops` | 1/(m^3 mm) | time,particle_size | - | Number density of drops of the diameter corresponding to a particular... |
| `particle_size` | mm | particle_size | - | Particle class size average |
| `raw_fall_velocity` | m/s | raw_fall_velocity | - | Fall velocity classes observed by Parsivel2 |
| `raw_spectrum` | count | time,particle_size,raw_fall_velocity | - | Raw drop size distribution |
| `sensor_temperature` | degC | time | - | Temperature in sensor |
| `slope_parameter` | 1/mm | time | - | Slope parameter, assuming an ideal Marshall-Palmer type distribution |


_1 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpldC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpldC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpldC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpldC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("precip_rate", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This datastream carries 42 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpldC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["precip_rate", "weather_code", "equivalent_radar_reflectivity_ott", "qc_precip_rate", "qc_weather_code", "qc_equivalent_radar_reflectivity_ott"],
                                cleanup_qc=True)
```

## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
42 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_precip_rate"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("precip_rate", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["precip_rate", "weather_code", "equivalent_radar_reflectivity_ott"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpldC1.b1.20260919.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `equivalent_radar_reflectivity_ott` | Value is equal to missing_value. | 1440 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpldC1.b1", "20140101", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: ARM undertakes post-processing of LDIS b-1 level data by implementing fall-speed filters (removing data points with fall speeds exceeding or falling below 50% of Tokay et al. 2013 terminal fall speeds for raindrops) to enhance data quality and consistency; results are made available as c-1 level data called LDQUANTS (Laser Disdrometer Quantities Value-Added Product), which also computes DSD microphysical properties (e.g., liquid water path) assuming gamma or exponential drop size distributions, and radar-equivalent quantities including dual-polarization parameters (Reflectivity Factor Z,...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Edge-of-field-of-view effects producing spuriously small drops with anomalously high... | Small drops exhibiting velocities exceeding their anticipated terminal fall rates in the raw b-1 data | Filter using +/-50% of Tokay et al. (2013) terminal fall speed relationship; post-processed into c-1 LDQUANTS | (hb p. 12) |
| Hydrometeors entering field of view after impacting the device | Larger drops observed with fall velocities that deviate from expected terminal values | Filter using +/-50% of Tokay et al. (2013) terminal fall speed relationship; post-processed into c-1 LDQUANTS | (hb p. 12) |
| Spurious measurements from non-hydrometeor objects (insects, leaves, spider webs) | Anomalous particle counts/sizes/velocities not consistent with precipitation physics | Removed via post-processing filters into LDQUANTS c-1 product; keep light pathway clear during maintenance | (hb p. 13) |
| Coincident hydrometeor undercounting | Multiple drops passing through the beam simultaneously reported as a single entity, causing underestimation of drop counts | None stated beyond noting the effect (Yuter et al. 2006) | (hb p. 13) |
| Uncertainty measuring frozen particles (snowflakes) due to axial ratio/tilt variation | Reported particle width and fall velocity can significantly differ from actual values; e.g., for 2-mm frozen particles, measured/true width ratio ranges 0.6-1.6 and observed/actual fall... | None specific stated beyond noting the uncertainty (Battaglia et al. 2010) | (hb p. 13) |
| Amplified errors in higher radar moments (e.g., Z) due to particle size uncertainty | Significant errors in derived DSD properties such as precipitation intensity (R) and radar reflectivity, especially pronounced for reflectivity because calculation involves sixth power of... | None stated | (hb p. 14) |
| Missing data represented by fill value | Fields show a value of -999 when data unavailable for a specific sample time | Recognize -999 as missing_value flag | (hb p. 8) |
| Classes 1 and 2 not evaluated by OTT | Boundary size/velocity classes 1 and 2 fall beyond device measurement range and are not populated in OTT measurements | None stated | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Instrument is calibrated by the vendor; no calibration activities are conducted at ARM sites. Prior to each deployment, particle size measurement verification is performed using reference spheres of known diameters released through the center of the laser strip during a 60-second measurement interval from a height of... (hb p. 12) |
| Calibration interval | Prior to each deployment (hb p. 12) |
| Traceability | Verification method provides only an approximate assessment; in cases of uncertainty, the instrument is returned to OTT for further inspection. (hb p. 12) |
| Routine maintenance | Visual inspection for physical damage; cleaning of laser protective lenses with soft lint-free cloth or cleaning solution; keeping light pathway clear of leaves, branches, spider webs; cleaning splash protection unit by removing hex screws, brushing and washing under running water; software/firmware updates;... (hb p. 12) |
| Maintenance interval | Lens cleaning performed at least semiannually; other tasks at regular intervals (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `CSV` | comma-separated values |
| `DOE` | U.S. Department of Energy |
| `DSD` | drop size distribution |
| `LDIS` | laser disdrometer |
| `LDQUANTS` | Laser Disdrometer Quantities Value-Added Product |
| `LWC` | liquid water content |
| `NetCDF` | Network Common Data Form |
| `TRACER` | Tracking Aerosol Convection Interactions Experiment |
| `Z` | reflectivity factor |
| `ZDR` | differential reflectivity |


### References the handbook cites

- Battaglia, A, E Rustemeier, A Tokay, U Blahak, and C Simmer. 2010. "Parsivel snow observations: A critical assessment." Journal of Atmospheric and Oceanic Technology 27(2): 333-344
- Giangrande, SE, D Wang, MJ Bartholomew, MP Jensen, DB Mechem, JC Hardin, and R Wood. 2019. "Midlatitude Oceanic Cloud and Precipitation Properties as Sampled by the ARM Eastern North Atlantic Observatory."...
- Jackson, R, S Collis, V Louf, A Protat, D Wang, S Giangrande, EJ Thompson, B Dolan, SW Powell, 2021. "The development of rainfall retrievals from radar at Darwin." Atmospheric Measurement Techniques 14(1): 53-69
- Loffler-Mang, M, and J Joss. 2000. "An optical disdrometer for measuring size and velocity of hydrometeors." Journal of Atmospheric and Oceanic Technology 17(2): 130-139
- Tokay, A, W Peterson, P Gatlin, and M Wingo. 2013. "Comparison of raindrop size distribution measurements by collocated disdrometers." Journal of Atmospheric and Oceanic Technology 30(8): 1672-1690
- Wang, D, SE Giangrande, MJ Bartholomew, JC Hardin, Z Feng, R Thalman, and LAT Machado. 2018. "The Green Ocean: precipitation insights from the GoAmazon2014/5 experiment." Atmospheric Chemistry and Physics 18(12):...
- Wang, D, MJ Bartholomew, SE Giangrande, and JC Hardin. 2021. "Analysis of Three Types of Collocated Disdrometer Measurements at the ARM Southern Great Plains Observatory." DOE/SC-ARM-TR-275
- Yuter, SE, DE Kingsmill, LB Nance, and M Loffler-Mang. 2006. "Observations of precipitation size and fall speed characteristics within coexisting rain and wet snow." Journal of Applied Meteorology and Climatology...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ldis_handbook.pdf (15 pages, DOE/SC-ARM-TR-137, by Z Zhu, D Wang)
- Catalog record: ARM data-source index, `instrument_class_code=ldis`, read 2026-09-23
- Example file: `sgpldC1.b1.20260919.000000.cdf` from `sgpldC1.b1`, 6.31 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
