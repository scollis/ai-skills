---
name: arm-vap-interpsonde
description: ARM Interpolated Sonde (interpsonde) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Precipitation, Temperature, Relative humidity, Vapor pressure, Barometric pressure, Wind speed), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpinterpolatedsondeC1.c1) and the variable inventory of a real file. Use when working with interpsonde data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling; Derived Quantities and Models. Triggers - interpsonde, Interpolated Sonde, sgpinterpolatedsondeC1.c1, Precipitation, Temperature, Relative humidity, Vapor pressure, Barometric pressure, Atmospheric Profiling, Derived Quantities and Models.
---

# INTERPSONDE - Interpolated Sonde

INTERPSONDE is an ARM value-added product that transforms radiosonde sounding data (via the intermediate GRIDDEDSONDE product) into continuous daily time-height fields of atmospheric state variables at 1-minute time resolution on a fixed 332-level vertical grid, with relative humidity additionally scaled to microwave radiometer precipitable water vapor observations.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 13 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `interpsonde` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-183 / T Fairless, M Jensen, A Zhou, SE Giangrande / September 2021](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-183.pdf) |
| Category | Atmospheric Profiling; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-10-21 to 2026-09-21 (active) |
| Datastreams with data | 29 across 23 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/interpsonde |


## Credit

Everything this skill knows about the retrieval is the work of **T Fairless, M Jensen, A Zhou, SE Giangrande** -
the ARM developers and mentors who wrote the technical report it derives from:

> T Fairless, M Jensen, A Zhou, SE Giangrande. *Interpolated Sonde and Gridded Sonde Value-Added Products*, DOE/SC-ARM-TR-183, September 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-183.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-183 documents the interpolated-sonde and gridded-sonde products together, so it is shared with `sondegrid`.

## How it is produced

GRIDDEDSONDE first transforms one-dimensional (time- and height-increasing) ARM sounding files (sondeadjust.c1 for older data, sondewnpn.b1 for newer data) onto a fixed time-height grid, with each sounding value interpolated onto the grid extending ±7.5 minutes (a 15-minute-wide bar). INTERPSONDE then takes GRIDDEDSONDE output and, between soundings, linearly interpolates atmospheric state variables in time for each height level to produce a continuous daily file at 1-minute resolution on 332 vertical levels from the surface to approximately 40 km. When processing a day of INTERPSONDE, ±2 days of input data are retrieved, allowing interpolation across gaps between soundings of up to 5 days. INTERPSONDE additionally constrains/scales relative humidity using precipitable water vapor (PWV) estimates from microwave radiometer (MWR) measurements, drawn preferentially from the MWRRET VAP (mwrret1liljclou) and, if unavailable, from MWRLOS, following the retrieval approach of Turner et al. 2007.

**Cadence.** input rate Sounding launches (discrete, per-launch, non-fixed interval); output every 1-minute time resolution on continuous daily files; averaging Linear interpolation in time between soundings for each height level; GRIDDEDSONDE interpolates each sounding value onto grid over a ±7.5 minute window (hb p. 6).

## Inputs

The report names these instruments and sibling products: GRIDDEDSONDE, SONDEADJUST, sondewnpn (ARM balloon-borne sounding system), MWRRET, MWRLOS, MERGESONDE, KAZRCOR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Precipitation | Mm | - | - | (hb p. 11) |
| Temperature | oC | - | - | (hb p. 11) |
| Relative humidity | % | - | - | (hb p. 11) |
| Vapor pressure | kPa | - | - | (hb p. 11) |
| Barometric pressure | kPa | - | - | (hb p. 11) |
| Wind speed | m/s | - | - | (hb p. 11) |
| Wind direction | degree | - | - | (hb p. 11) |
| Eastward wind component | m/s | - | - | (hb p. 11) |
| Northward wind component | m/s | - | - | (hb p. 11) |
| Dew-point temperature | oC | - | - | (hb p. 11) |
| Potential temperature | K | - | - | (hb p. 11) |
| Specific humidity | g/g | - | - | (hb p. 11) |
| Relative humidity scaled using MWR | % | - | - | (hb p. 11) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Time resolution | 1-minute time resolution | (hb p. 6) |
| Vertical levels | 332 levels | (hb p. 6) |
| Vertical extent | from the surface up to a limit of approximately 40 km | (hb p. 6) |
| Typical sounding termination altitude | between 25 and 30 km, above which no data are provided | (hb p. 6) |
| GRIDDEDSONDE sounding interpolation window | ±7.5 minutes (15 minutes wide) | (hb p. 8) |
| Input data retrieval window | ±2 days' worth of input data retrieved when processing a day of INTERPSONDE | (hb p. 9) |
| Maximum sounding gap interpolated | up to 5 days | (hb p. 9) |
| Vertical resolution 0-3.5 km | 20 m | (hb p. 11) |
| Vertical resolution 3.5-5 km | 50 m | (hb p. 11) |
| Vertical resolution 5-7 km | 100 m | (hb p. 11) |
| Vertical resolution 7-20 km | 200 m | (hb p. 11) |
| Vertical resolution 20-~40 km | 500 m | (hb p. 11) |


## The data

Verified example: **`sgpinterpolatedsondeC1.c1`**, file `sgpinterpolatedsondeC1.c1.20260916.000030.nc`
(61.25 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `height`=332 |
| Data variables | 39 |
| QC variables | 13 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-16T00:00:30 to 2026-09-16T23:59:30 |
| dod version | interpolatedsonde-c1-4.2 |
| process version | vap-interpolatedsonde-7.1-4.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bar_pres` | kPa | time,height | yes | Barometric pressure |
| `dp` | degC | time,height | yes | Dewpoint temperature |
| `potential_temp` | K | time,height | yes | Potential temperature |
| `precip` | mm | time | yes | Precipitation |
| `rh` | % | time,height | yes | Relative humidity |
| `rh_scaled` | % | time,height | yes | Relative humidity scaled using MWR |
| `sh` | g/g | time,height | yes | Specific humidity |
| `temp` | degC | time,height | yes | Temperature |
| `u_wind` | m s-1 | time,height | yes | Eastward wind component |
| `v_wind` | m s-1 | time,height | yes | Northward wind component |
| `vap_pres` | kPa | time,height | yes | Vapor pressure |
| `wdir` | degree | time,height | yes | Wind direction |
| `wspd` | m s-1 | time,height | yes | Wind speed |
| `aqc_rh_scaled` | 1 | time,height | - | Quality check results |
| `height` | km | height | - | Height |
| `source_bar_pres` | 1 | time,height | - | Source for variable:Barometric pressure |
| `source_dp` | 1 | time,height | - | Source for variable:Dewpoint temperature |
| `source_rh` | 1 | time,height | - | Source for variable:Relative humidity |
| `source_temp` | 1 | time,height | - | Source for variable:Temperature |
| `source_u_wind` | 1 | time,height | - | Source for variable:Eastward wind component |
| `source_v_wind` | 1 | time,height | - | Source for variable:Northward wind component |
| `time` | - | time | - | Time offset from midnight |
| `vapor_source` | 1 | time,height | - | Source of the MWR data used to produce: rh_scaled |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpinterpolatedsondeC1.c1", "2026-09-16", "2026-09-16")
ds = armlive_open("sgpinterpolatedsondeC1.c1", "2026-09-16", "2026-09-16", cleanup_qc=True)
```

## Quality control in this product

13 `qc_` companion variables cover 13 of the
39 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpinterpolatedsondeC1.c1.20260916.000030.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `temp` | Data value not available in input file, data value has been set... | 63054 | 13.189 |
| `rh` | Data value not available in input file, data value has been set... | 63054 | 13.189 |
| `vap_pres` | Data value not available in input file, data value has been set... | 63054 | 13.189 |
| `bar_pres` | Data value not available in input file, data value has been set... | 63054 | 13.189 |
| `wspd` | Data value not available in input file, data value has been set... | 63054 | 13.189 |
| `wdir` | Data value not available in input file, data value has been set... | 63054 | 13.189 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpinterpolatedsondeC1.c1", "19981021", "20260924")
```

The report's own note on quality: Tests to ensure values are within a valid range are provided for variables interpolated from GRIDDEDSONDE, as well as for the scaled relative humidity. Computed values (specific humidity, wind speed, wind direction, potential temperature) do not require QC tests. The rh_scaled variable has, in addition to general valid range QC, an ancillary QC variable aqc_rh_scaled describing the quality of computed scale factors. The vapor_source variable provides the source of the PWV used for scaling relative humidity. Table 4 indicates per-variable whether QC data exists and whether a source field is...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Interpolation gaps between soundings | Red contour regions in time-height plots (as opposed to blue vertical lines at actual sounding times) representing linearly interpolated rather than observed data | Linear interpolation in time for each height level between available soundings | (hb p. 6) |
| Data blind zone above typical sounding termination | No data above the altitude where soundings terminate (typically 25-30 km) even though the output grid extends to ~40 km | Grid extends to ~40 km only to capture full height of soundings that reach higher; no data provided above actual sounding termination altitude | (hb p. 6) |
| Long interpolation gaps up to 5 days | Extended stretches of interpolated (non-observed) values in the time-height field when soundings are missing for multiple days, since ±2 days of input data are retrieved per processing day | None specified beyond the ±2 day retrieval window design | (hb p. 9) |
| Known humidity biases in Vaisala radiosonde observations | Systematic offset in relative humidity from older radiosondes prior to bias correction | Corrected via the SONDEADJUST VAP (rh_adjust) for older soundings; new Vaisala software adopted by ARM beginning in 2001 accounts for these biases... | (hb p. 8) |
| Site-dependent transition date from SONDEADJUST to sondewnpn | Discontinuity or change in RH data source/processing at a date that varies by site (e.g., SGP.C1 August 32, 2012; TWP.C1 September 8, 2011; NSA.C1 July 16, 2012) | Refer to Table 1 dates of last SONDEADJUST per site.facility | (hb p. 8) |
| GRIDDEDSONDE not distributed as its own datastream | Users cannot directly retrieve GRIDDEDSONDE data as a standalone product | Data contained in GRIDDEDSONDE can be gleaned from INTERPSONDE by using the source variables | (hb p. 8) |
| PWV source substitution for RH scaling | Relative humidity scaling factor quality/behavior may differ depending on whether PWV came from MWRRET or fallback MWRLOS | Process first attempts PWV from MWRRET VAP (mwrret1liljclou/mwrretliljclou), then falls back to MWRLOS if unavailable; vapor_source variable records... | (hb p. 9) |
| Static/no-QC precipitation field | Precipitation variable listed with QC flag 'yes' but marked as having a static source (not measured/interpolated like other variables) | None specified | (hb p. 11) |
| Computed variables lack independent QC | Vapor pressure, wind speed, wind direction, potential temperature, and specific humidity show QC flags but are derived/computed rather than sourced, so their quality reflects the input... | Tests for valid range are provided only for variables interpolated from GRIDDEDSONDE and for scaled RH; computed values do not require separate QC... | (hb p. 10) |
| Ancillary QC needed to interpret rh_scaled quality | General valid-range QC alone does not describe quality of computed scale factors used for rh_scaled | Consult aqc_rh_scaled ancillary QC variable for additional information on the quality of computed scale factors | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Gaustad, KL, DD Turner, and SA McFarlane. 2011. MWRRET Value-Added Product: The Retrieval of Liquid Water Path and Precipitable Water Vapor from Microwave Radiometer (MWR) Data Sets. DOE/SC-ARM-TR-081.2.
- Miloshevich, LM, H Vomel, DN Whiteman, and T Leblanc. 2009. Accuracy assessment and correction of Vaisala RS92 radiosonde water vapor measurements. Journal of Geophysical Research - Atmospheres 114(D11): D11305.
- Troyan, D. 2012. Merged Sounding Value-Added Product. DOE/SC-ARM-TR-087.
- Troyan, D. 2011. Sonde Adjust Value-Added Product Technical Report. DOE/SC-ARM-TR-102.
- Turner, DD, SA Clough, JC Liljegren, EE Clothiaux, KE Cady-Pereira, and KL Gaustad. 2007. Retrieving Liquid Water Path and Precipitable Water Vapor from Atmospheric Radiation Measurement (ARM) Microwave Radiometers....

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-183.pdf (13 pages, DOE/SC-ARM-TR-183, by T Fairless, M Jensen, A Zhou, SE Giangrande)
- Catalog record: ARM data-source index, `instrument_class_code=interpsonde`, read 2026-09-24
- Example file: `sgpinterpolatedsondeC1.c1.20260916.000030.nc` from `sgpinterpolatedsondeC1.c1`, 61.25 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
