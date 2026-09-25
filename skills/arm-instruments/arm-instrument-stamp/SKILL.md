---
name: arm-instrument-stamp
description: ARM Soil Temperature and Moisture Profiles (stamp) - handbook-derived instrument reference. Measurement principle, reported quantities (soil_specific_water_content, plant_water_availability, total_plant_water_availability, soil_temperature, loam_soil_water_content, soil_conductivity, real_dielectric_permittivity, precip), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfstamppcpS40.b1) and the variable inventory of a real file. Use when working with stamp data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Surface/Subsurface Properties. Triggers - stamp, Soil Temperature and Moisture Profiles, bnfstamppcpS40.b1, soil_specific_water_content, plant_water_availability, total_plant_water_availability, soil_temperature, loam_soil_water_content, soil_conductivity.
---

# STAMP - Soil Temperature and Moisture Profiles

STAMP provides vertical profiles of soil temperature, soil water content (soil-type specific and loam type), plant water availability, soil conductivity, and real dielectric permittivity as a function of depth via in situ HydraProbe sensors installed at all SGP extended facilities, plus precipitation measured at the surface.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `stamp` |
| Handbook | [DOE/SC-ARM-TR-186 / DR Cook / April 2018](https://www.arm.gov/publications/tech_reports/handbooks/stamp_handbook.pdf) |
| Measurement category | Surface/Subsurface Properties |
| Manufacturer / model | Stevens Water Monitoring Systems, Inc. HydraProbe; Texas Electronics, Inc. Model TR-525M Metric Heated Rain Gauge; Campbell Scientific, Inc. Model CR800 data logger; Campbell Scientific, Inc. Model... |
| Primary measurements | Precipitation; Soil moisture; Soil temperature |
| Record | 2016-02-22 to 2026-09-22 (active) |
| Datastreams with data | 46 across 2 sites |
| Sites | bnf, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/stamp |


## Credit

Everything this skill knows about the instrument is the work of **DR Cook** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> DR Cook. *Soil Temperature and Moisture Profile (STAMP) System Instrument Handbook*, DOE/SC-ARM-TR-186, April 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/stamp_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The HydraProbe soil temperature and moisture sensor measures soil temperature, bulk electrical conductivity, and real dielectric permittivity based on the reflectance of an electrical signal transmitted through the soil between the center and three perimeter tines. An internal microprocessor calculates soil moisture based on the loam soil texture calibration. The Campbell CR800 program calculates soil moisture and plant water availability based on the physically measured soil-specific texture at each measurement depth and calibration coefficients determined by Stevens Water Monitoring Systems, Inc. Two soil-specific texture calibration equations are used depending on whether the soil is sand/silt/clay versus other soil textures, relating soil moisture (Θ) to the real dielectric permittivity (εR) via coefficients A, B, C, D. Plant water availability per soil section is estimated from soil moisture, the crop lower limit (wilting point) for the soil texture, and the height of the soil section.

**Siting.** Measurements are made in three soil profiles (west, south, east) at generally 5, 10, 20, 50, and 100 cm depths (lowest depth varies at three EFs). Three sensor profiles are located approximately 1 m apart, for a total of 15 HydraProbes per site. Installation performed manually with a powered auger to minimize disturbance; HydraProbes placed in sides of holes to provide a relatively undisturbed soil profile. The electronics enclosure is mounted on poles in concrete foundations, placed at a reasonable distance from the HydraProbes to minimize the influence of the equipment on the HydraProbe measurements. Soil type varies with depth and by site (see soil texture triangle and Table 5),...

**Sampling.** reported every half hourly intervals for soil profile variables (dimension time = 48); precipitation at one-minute intervals (dimension time = 1440) (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| soil_specific_water_content (west/south/east) | % (100 x m3/m3) | 0 to 100 % | 3% | - | (hb p. 9) |
| plant_water_availability (west/south/east) | mm | -200 to 400 mm | 1% | - | (hb p. 9) |
| total_plant_water_availability (west/south/east) | mm | -800 to 1200 mm | 1% | - | (hb p. 9) |
| soil_temperature (west/south/east) | oC | -40 to 50 oC | 0.3 oC | - | (hb p. 9) |
| loam_soil_water_content (west/south/east) | % (100 x m3/m3) | 0 to 100 % | 3% | - | (hb p. 9) |
| soil_conductivity (west/south/east) | Siemens/m | 0 to 2 S/m | 2% | - | (hb p. 10) |
| real_dielectric_permittivity (west/south/east) | unitless | 0 to 650 | 1.5% | - | (hb p. 10) |
| precip | mm | 0 to 10 mm | 1 % | 0.1 mm Metric | (hb p. 10) |
| battery_voltage | VDC | 0 to 15 V | - | - | (hb p. 10) |
| Real dielectric permittivity (isolated) [HydraProbe factory... | unitless | 1 to 80 where 1 = air, 80 = distilled... | ± 1.5% or 0.2 whichever is typically greater | - | (hb p. 16) |
| Soil moisture for inorganic & mineral soil [HydraProbe... | WFV | From completely dry to fully saturated | ± 0.01 WFV for most soils, ± 0.03 max for fine... | - | (hb p. 16) |
| Bulk electrical conductivity [HydraProbe factory spec] | S/m | 0.01 to 1.5 S/m | ± 2.0% or 0.02 S/m whichever is typically... | - | (hb p. 16) |
| Temperature [HydraProbe factory spec] | °C | -10°C to +55°C | ± 0.3°C | - | (hb p. 16) |
| Inter-sensor variability [HydraProbe factory spec] | WFV (θ m3 m-3) | - | less than  ± 0.012 WFV | - | (hb p. 16) |


## Specifications

| parameter | value | source |
|---|---|---|
| TR-525M Resolution | 0.1 mm Metric | (hb p. 15) |
| TR-525M Accuracy | 1.0% up to 2"/hr (50 mm/hr) | (hb p. 16) |
| TR-525M Collector Diameter | 9.66" (245 mm) with knife-edge | (hb p. 16) |
| TR-525M Funnel Depth | 7.2" (183 mm) | (hb p. 16) |
| TR-525M Splash out Protection | greater than 2" (50 mm) | (hb p. 16) |
| TR-525M Operating Temp | 32 to 125°F (0 to 50°C) | (hb p. 16) |
| TR-525M Storage Temp | -40 to 160°F (-40 to 70°C) | (hb p. 16) |
| TR-525M Humidity Limits | 0 to 100% | (hb p. 16) |
| TR-525M Weight | 2.5 lbs. (1.2 kg) 6 lbs. (2.7 kg) shipping | (hb p. 16) |
| TR-525M Height | 12" (305 mm) | (hb p. 16) |
| TR-525M Cable | 25', 24-gauge 2-conductor | (hb p. 16) |
| TR-525M Switch | Momentary potted reed switch | (hb p. 16) |
| TR-525M Switch Rating | 30 VDC @ 2 A, 115 VAC @ 1 A | (hb p. 16) |
| TR-525M Switch Closure Time | 135 ms | (hb p. 16) |
| TR-525M Bounce Setting Time | 0.75 ms | (hb p. 16) |
| TR-525M Pivot | Hardened SS Jewel & Pivot | (hb p. 16) |
| TR-525M Bucket | Black ABS injection molded | (hb p. 16) |
| TR-525M Level | Integral Bubble Level | (hb p. 16) |
| TR-525M Power | 120 VAC | (hb p. 16) |
| TR-525M Current | 1.65 A | (hb p. 16) |
| TR-525M Starting Temperature | 45°F (7.2°C) | (hb p. 16) |
| TR-525M Minimum Temperature | -65°F (-54°C) | (hb p. 16) |
| HydraProbe Electrical - Power supply | 9-20 VDC | (hb p. 16) |
| HydraProbe Electrical - Power consumption | less than 1 mA idle / 10 mA active for 2 seconds during duty cycle | (hb p. 16) |
| HydraProbe Electrical - Cable | 3-wire: power, ground, data | (hb p. 16) |
| HydraProbe Electrical - Max. cable length | 60 m (197 ft) | (hb p. 16) |


_13 further specification rows are in the handbook._

## The data

Verified example: **`bnfstamppcpS40.b1`**, file `bnfstamppcpS40.b1.20260919.000000.nc`
(0.06 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2 |
| Data variables | 8 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:00 |
| dod version | stamppcp-b1-1.0 |
| process version | ingest-stamp-1.2-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `precip` | mm | time | yes | Precipitation total |
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
                     params={"user": f"{user}:{token}", "ds": "bnfstamppcpS40.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfstamppcpS40.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfstamppcpS40.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfstamppcpS40.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("precip", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
8 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_precip"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("precip", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["precip"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("bnfstamppcpS40.b1", "20160222", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality flags alert users to bad or questionable data. -9999 means sensor not installed or data missing; 9999 indicates an offscale value beyond data logger capability. netCDF files contain flags: Flag=0 (within specified range), Flag=1 (missing, recorded as -9999), Flag=2 (less than acceptable minimum), Flag=4 (greater than acceptable maximum), Flag=8 (failed delta check). QC variables (e.g., qc_precip) are the sum of applicable flags, decoded via base-2 conversion; there are QC variables for all measurement variables. Acceptable minimums/maximums per variable are given in Table 4....

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Lightning sensitivity of HydraProbe microprocessor | Sudden sensor failure or dropout, particularly at deeper depths, following lightning activity; several HydraProbes already replaced | Replace affected HydraProbes | (hb p. 13) |
| Missing data / sensor not installed | Value of -9999 in the datastream | Interpret -9999 as sensor not installed or data missing; check for failed probe, non-functioning multiplexer channel, loose/broken leads, or... | (hb p. 10) |
| Offscale value | Value of 9999 in the datastream | Interpret as beyond capability of data logger to measure | (hb p. 10) |
| Out-of-range values flagged | QC flag=2 (less than acceptable minimum) or flag=4 (greater than acceptable maximum) set per Table 4 min/max bounds | Use qc_ variables (sum of flags, decode via base-2) to identify range violations | (hb p. 11) |
| Failed delta check | QC flag=8 set when value differs too greatly from previous value | None specified beyond flagging | (hb p. 11) |
| Soil conductivity and real dielectric permittivity not temperature corrected | Values reflect raw sensor response without temperature correction, may show apparent variability tied to soil temperature | None specified | (hb p. 10) |
| Depth/soil type variability across profile | Soil-specific water content computations vary by depth and by extended facility due to differing soil texture (see Table 5 and soil texture triangle) | Soil textural classification determined via OSU lab analysis used to select the correct calibration equation for soil-specific water content | (hb p. 12) |
| Shallow soil/rock limiting sensor installation depth | Some EFs have different (shallower) deepest sensor depth (e.g., E13 75/100 cm, E31 80 cm) rather than standard 100 cm | Consult Table 1 for actual installed depths at each EF | (hb p. 8) |
| Precipitation gauge funnel blockage by debris or ice/snow | Precipitation readings artificially low or zero; heater malfunction suspected | Disconnect gauge lead, remove funnel, clear blockage, check heaters by hand feel, replace gauge or funnel if heater not working, perform tip test... | (hb p. 20) |
| Rain gauge calibration drift | Tipping bucket count deviates from vendor calibration device reference | Perform six-month calibration check using vendor calibration device and adjust tipping bucket as needed | (hb p. 21) |
| Battery/power issues | battery_voltage diagnostic variable outside 0-15V acceptable range | Remove charging power, measure battery voltage, reconnect charging power as part of preventative maintenance | (hb p. 20) |
| SWATS-to-STAMP transition discontinuity | Data record shows system change from SWATS to STAMP in early 2016; SWATS retained at EF13 for ~1 year for comparison, creating overlapping but distinct datastreams | Compare SWATS and STAMP records at EF13 during overlap period | (hb p. 7) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Sensors factory calibrated by Stevens Water Monitoring Systems, Inc. to yield accurate soil temperature for any soil texture and volumetric soil moisture for the loam soil texture; calibration coefficients also provided for soil-specific texture calculation using two calibration equations (sand/silt/clay vs other soil... (hb p. 11) |
| Calibration interval | Precipitation gauge: bi-weekly tip test checks; calibration performed every six months using calibration device from precipitation gauge vendor. (hb p. 11) |
| Traceability | Uncertainties determined by the manufacturer of the HydraProbe (Stevens Water Monitoring Systems, Inc.). (hb p. 11) |
| Routine maintenance | Preventative maintenance checks include: testing battery voltage; checking for reasonable values in measurements (soil water content, temperature, PWA, conductivity, permittivity ranges); checking for -9999 values indicating failed probe, non-functioning multiplexer channel, loose/broken leads, or broken/chewed cable;... (hb p. 20) |
| Maintenance interval | Bi-weekly tip test checks on precipitation gauge; six-month calibration of precipitation gauge. (hb p. 20) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: SWATS (Soil Water and Temperature System).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ABS` | acrylonitrile butadiene styrene |
| `ARM` | Atmospheric Radiation Measurement |
| `CLL` | crop lower limit |
| `DOE` | U.S. Department of Energy |
| `DQ Explorer` | Data Quality Explorer |
| `DQO` | Data Quality Office |
| `DQPR` | Data Quality Problem Reports |
| `DQR` | Data Quality Report |
| `EF` | extended facility |
| `OSU` | Oklahoma State University |
| `PVC` | polyvinyl chloride |
| `PWA` | plant water availability |
| `QC` | quality control |
| `RMSE` | root-mean-square error |


### References the handbook cites

- Stevens Water Monitoring Systems, Inc. HydraProbe website, http://www.stevenswater.com/products/sensors/soil/hydraprobe/
- Stevens Water Monitoring Systems, Inc., "HydraProbe User's Manual," https://www.fondriest.com/pdf/stevens_hydra_manual.pdf
- Stevens Water Monitoring Systems, Inc., "The Parameters of the HydraProbe," http://www.btnode.ethz.ch/pub/uploads/Internal/hydraprobe.pdf
- Bellingham, K. (Stevens Water Monitoring Systems, Inc.), "The Stevens Hydra Probe Inorganic Soil Calibrations," http://www.soilsensor.com/articles/The%20Stevens%20Hydra%20Probe%20Inorganic%20Soil%20Calibrations.pdf
- White, B. (Cropfacts Pty Ltd for Birchip Cropping Group Inc.(BCG)), "BCG Soil Test Interpretation Workshop Notes," http://www.bcg.org.au/cb_pages/HealthySoils.php
- Better Soils Module 2, Soil & Nutrition: Crops, 2.1 Soil Holding Capacity, http://www.soilwater.com.au/bettersoils/module2/2_1.htm#wilting%20point

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/stamp_handbook.pdf (23 pages, DOE/SC-ARM-TR-186, by DR Cook)
- Catalog record: ARM data-source index, `instrument_class_code=stamp`, read 2026-09-23
- Example file: `bnfstamppcpS40.b1.20260919.000000.nc` from `bnfstamppcpS40.b1`, 0.06 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
