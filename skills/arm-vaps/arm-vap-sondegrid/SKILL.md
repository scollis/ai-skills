---
name: arm-vap-sondegrid
description: ARM Gridded Sonde VAP Product (sondegrid) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Barometric pressure, Dew-point temperature, Relative humidity, Temperature, Eastward wind component, Northward wind component), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpgriddedsondeC1.c0) and the variable inventory of a real file. Use when working with sondegrid data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - sondegrid, Gridded Sonde VAP Product, sgpgriddedsondeC1.c0, Barometric pressure, Dew-point temperature, Relative humidity, Temperature, Eastward wind component, Atmospheric Profiling.
---

# SONDEGRID - Gridded Sonde VAP Product

The Gridded Sonde VAP (GRIDDEDSONDE) transforms one-dimensional ARM balloon sounding files into a two-dimensional time-height grid (identical to the INTERPSONDE grid) at ARM sites, serving as the intermediate input to the INTERPSONDE Value-Added Product.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 13 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sondegrid` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-183 / T Fairless, M Jensen, A Zhou, SE Giangrande / September 2021](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-183.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1999-07-20 to 2026-09-23 (active) |
| Datastreams with data | 28 across 22 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sondegrid |


## Credit

Everything this skill knows about the retrieval is the work of **T Fairless, M Jensen, A Zhou, SE Giangrande** -
the ARM developers and mentors who wrote the technical report it derives from:

> T Fairless, M Jensen, A Zhou, SE Giangrande. *Interpolated Sonde and Gridded Sonde Value-Added Products*, DOE/SC-ARM-TR-183, September 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-183.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-183 documents the interpolated-sonde and gridded-sonde products together, so it is shared with `interpsonde`; the gridded algorithm is described as reusing the interpolated time-height grid.

## How it is produced

GRIDDEDSONDE takes standard ARM-format radiosonde sounding files, which report atmospheric state (pressure, dewpoint, relative humidity, temperature, u/v wind) as a one-dimensional series increasing in time and height per launch, and interpolates each sounding value onto a fixed two-dimensional time-height grid identical to the INTERPSONDE grid. Each sounding value is placed on the grid extending +/-7.5 minutes around the launch time, so each sounding occupies a 15-minute-wide vertical bar on the time-height grid. GRIDDEDSONDE ingests corrected soundings from the SONDEADJUST VAP (sondeadjust.c1) for older data, which corrects Vaisala radiosonde observations for known humidity biases, and original ARM sounding files (sondewnpn.b1) for newer, already-improved soundings that used Vaisala software correcting for these biases (adopted by ARM beginning in 2001). The GRIDDEDSONDE output is not itself distributed as an ARM datastream but is used directly as input to INTERPSONDE, from which its data can be recovered via the source variables.

**Cadence.** input rate per sonde launch; output every 1-minute time resolution on fixed time-height grid; each sounding occupies a 15-minute-wide window (+/-7.5 minutes); averaging linear interpolation in time between soundings for each height level; gaps of up to 5 days may be interpolated (using +/-2 days of input data) (hb p. 6).

## Inputs

The report names these instruments and sibling products: INTERPSONDE, SONDEADJUST, MWRRET, MWRLOS, MERGESONDE, KAZRCOR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Barometric pressure (bar_pres, from pres) | - | - | - | (hb p. 8) |
| Dew-point temperature (dp) | - | - | - | (hb p. 8) |
| Relative humidity (rh) | - | - | - | (hb p. 8) |
| Temperature (temp) | - | - | - | (hb p. 8) |
| Eastward wind component (u_wind) | - | - | - | (hb p. 8) |
| Northward wind component (v_wind) | - | - | - | (hb p. 8) |
| Altitude (alt) | - | - | - | (hb p. 8) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Time resolution of grid | 1-minute time resolution | (hb p. 6) |
| Number of vertical levels | 332 levels | (hb p. 6) |
| Vertical extent | surface up to a limit of approximately 40 km | (hb p. 6) |
| Sounding sample width on grid | each sounding value interpolated onto the fixed grid extends +/-7.5 minutes, i.e. 15 minutes wide | (hb p. 8) |
| Vertical resolution 0-3.5 km | 20 m | (hb p. 11) |
| Vertical resolution 3.5-5 km | 50 m | (hb p. 11) |
| Vertical resolution 5-7 km | 100 m | (hb p. 11) |
| Vertical resolution 7-20 km | 200 m | (hb p. 11) |
| Vertical resolution 20-~40 km | 500 m | (hb p. 11) |


## The data

Verified example: **`sgpgriddedsondeC1.c0`**, file `sgpgriddedsondeC1.c0.20260918.000030.nc`
(30.63 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `height`=332 |
| Data variables | 21 |
| QC variables | 8 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-18T00:00:30 to 2026-09-18T23:59:30 |
| dod version | griddedsonde-c0-1.3 |
| process version | vap-griddedsonde-3.3-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bar_pres` | kPa | time,height | yes | Barometric pressure |
| `dp` | degC | time,height | yes | Dewpoint temperature |
| `rh` | % | time,height | yes | Relative humidity |
| `temp` | degC | time,height | yes | Temperature |
| `u_wind` | m s-1 | time,height | yes | Eastward wind component |
| `v_wind` | m s-1 | time,height | yes | Northward wind component |
| `wdir` | degree | time,height | yes | Wind direction |
| `wspd` | m s-1 | time,height | yes | Wind speed |
| `height` | km | height | - | Height |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpgriddedsondeC1.c0", "2026-09-18", "2026-09-18")
ds = armlive_open("sgpgriddedsondeC1.c0", "2026-09-18", "2026-09-18", cleanup_qc=True)
```

## Quality control in this product

8 `qc_` companion variables cover 8 of the
21 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpgriddedsondeC1.c0.20260918.000030.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `temp` | Data value not available in input file, data value has been set... | 468815 | 98.062 |
| `rh` | Data value not available in input file, data value has been set... | 468815 | 98.062 |
| `bar_pres` | Data value not available in input file, data value has been set... | 468815 | 98.062 |
| `wspd` | Data value not available in input file, data value has been set... | 468815 | 98.062 |
| `wdir` | Data value not available in input file, data value has been set... | 468815 | 98.062 |
| `u_wind` | Data value not available in input file, data value has been set... | 468815 | 98.062 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpgriddedsondeC1.c0", "19990720", "20260924")
```

The report's own note on quality: Tests ensure values are within a valid range for variables interpolated from GRIDDEDSONDE, as well as for the scaled relative humidity (rh_scaled). Computed values (specific humidity, wind speed, wind direction, potential temperature) do not require QC tests. In addition to general valid-range QC for rh_scaled, ancillary QC in aqc_rh_scaled describes the quality of computed scale factors. The vapor_source variable indicates the source of PWV used for scaling relative humidity. Table 4 in the handbook indicates, per variable, whether QC data exists and whether source data (from GRIDDEDSONDE...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Most soundings terminate below the full 40 km grid height | No data provided above the sounding termination altitude, typically between 25 and 30 km, even though the grid extends to ~40 km | Grid extends to 40 km simply to capture the full height of soundings that do reach that high; no data exists above actual sounding termination... | (hb p. 6) |
| Interpolation gaps between soundings | Red contour regions in time-height plots (as opposed to blue vertical lines where actual sounding data exists) show linearly interpolated rather than measured atmospheric state values | INTERPSONDE linearly interpolates atmospheric state variables in time for each height level between soundings | (hb p. 6) |
| Known humidity bias in Vaisala radiosonde observations | Uncorrected relative humidity/dewpoint values from older soundings show systematic bias relative to true atmospheric humidity | SONDEADJUST VAP corrects for known humidity biases (Miloshevich et al. 2009) for older soundings; newer soundings use updated Vaisala software... | (hb p. 8) |
| Site-specific transition dates from SONDEADJUST to sondewnpn source data | Data provenance (rh source variable and adjustment method) changes at different calendar dates depending on site | Refer to Table 1 for date of last SONDEADJUST use per site | (hb p. 8) |
| Long interpolation gaps up to 5 days between soundings | Extended stretches of interpolated (non-measured) data in a given day's output when soundings are sparse | Processing retrieves +/-2 days of input data around each processed day to allow interpolation across gaps of up to 5 days | (hb p. 9) |
| GRIDDEDSONDE not distributed as a standalone ARM datastream | Users will not find a discrete GRIDDEDSONDE datastream in the ARM archive | GRIDDEDSONDE data can be gleaned from INTERPSONDE using the source variables | (hb p. 8) |
| Apparent data-entry error in Table 1 for SGP.C1 last SONDEADJUST date | Table lists SGP.C1 date of last SONDEADJUST as 'August 32, 2012', an invalid calendar date as printed in the handbook | - | (hb p. 8) |


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
- Catalog record: ARM data-source index, `instrument_class_code=sondegrid`, read 2026-09-24
- Example file: `sgpgriddedsondeC1.c0.20260918.000030.nc` from `sgpgriddedsondeC1.c0`, 30.63 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
