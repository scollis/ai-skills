---
name: arm-vap-mergesonde
description: ARM Merged Sounding (mergesonde) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Barometric Pressure, Temperature, Relative Humidity, Wind Speed, Wind Direction, U- and V-Wind), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmergesonde1maceC1.c1) and the variable inventory of a real file. Use when working with mergesonde data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - mergesonde, Merged Sounding, sgpmergesonde1maceC1.c1, Barometric Pressure, Temperature, Relative Humidity, Wind Speed, Wind Direction, Atmospheric Profiling.
---

# MERGESONDE - Merged Sounding

The Merged Sounding (MERGESONDE) VAP produces continuous atmospheric thermodynamic and wind profiles from the surface to ~20 km (v1) or ~60 km (v2) AGL at one-minute time resolution, merging radiosonde, microwave radiometer, surface meteorology, and ECMWF model data at fixed ARM Climate Research Facility and ARM Mobile Facility sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 19 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mergesonde` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-087 / D Troyan / March 2012](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-087.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1996-07-15 to 2015-06-29 (retired) |
| Datastreams with data | 15 across 9 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mergesonde |


## Credit

Everything this skill knows about the retrieval is the work of **D Troyan** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Troyan. *Merged Sounding Value-Added Product*, DOE/SC-ARM/TR-087, March 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-087.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

MERGESONDE builds two temporary profiles on a common grid: one using only radiosonde data with interpolation/extrapolation, and one using ECMWF model output with the same techniques. These two profiles are merged using a double-sigmoid weighting function of temporal distance from the nearest radiosonde observation, so that actual radiosonde observations receive 100% weight and the model contribution grows as time from an observation increases. Surface meteorology and tower instruments provide boundary conditions for the lowest levels since ECMWF data does not reach ground level, and ECMWF pressure levels are converted to meters AGL via the hypsometric equation using surface data. MWR retrievals (MWRRET) constrain total column water vapor and scale relative humidity in the one-minute profiles. A box-car smoothing (average of four nearest neighbors, replacing the center point with a five-point average if it differs by more than 20%) is applied, followed by a check to ensure no physically impossible situations exist.

**Cadence.** output every one-minute temporal intervals; averaging box-car average of four nearest neighbors, replaced by five-point average if greater than 20% different from center (hb p. 6).

## Inputs

The report names these instruments and sibling products: Radiosonde (sondewnpn, SONDEADJUST), Microwave Radiometer (MWR, MWRRET, MWR-LOS), Surface Meteorological Instruments / Meteorological Tower, ECMWF model output, Sonde Adjust VAP (DOE/SC-ARM-TR-102).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Barometric Pressure | - | - | - | (hb p. 12) |
| Temperature | C | - | - | (hb p. 6) |
| Relative Humidity | % | - | - | (hb p. 6) |
| Wind Speed | m/s | - | - | (hb p. 7) |
| Wind Direction | deg | - | - | (hb p. 6) |
| U- and V-Wind | - | - | - | (hb p. 12) |
| Dew Point | - | - | - | (hb p. 12) |
| Vapor Pressure | - | - | - | (hb p. 12) |
| Specific Humidity | - | - | - | (hb p. 12) |
| Precipitation | - | - | - | (hb p. 12) |
| Potential Temperature | - | - | - | (hb p. 12) |
| Scaled Relative Humidity (RH scaled using MWR PWV) | % | - | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Temporal resolution | 1-minute | (hb p. 6) |
| Altitude levels (v1) | at least 266 altitude levels | (hb p. 6) |
| Altitude levels (v2) | 316 altitude levels | (hb p. 6) |
| Maximum height (v1) | 20 km above ground level | (hb p. 6) |
| Maximum height (v2) | 60 km above ground level | (hb p. 6) |
| Altitude resolution 0-3 km AGL | 20 m | (hb p. 7) |
| Altitude resolution 3-13 km AGL | 50 m | (hb p. 7) |
| Altitude resolution 13-16 km AGL | 100 m | (hb p. 7) |
| Altitude resolution 16-20 km AGL | 200 m | (hb p. 7) |
| Altitude resolution 20-60 km AGL (v2 only) | 200 m | (hb p. 7) |
| Double sigmoid parameter SGP | Slope 1.50, Half Width-Half Mean 4.00 | (hb p. 9) |
| Double sigmoid parameter NSA | Slope 0.75, Half Width-Half Mean 8.00 | (hb p. 9) |
| Double sigmoid parameter TWP Manus | Slope 1.10, Half Width-Half Mean 6.00 | (hb p. 9) |
| Double sigmoid parameter TWP Nauru | Slope 1.10, Half Width-Half Mean 6.00 | (hb p. 9) |
| Double sigmoid parameter TWP Darwin | Slope 1.50, Half Width-Half Mean 4.00 | (hb p. 9) |
| Double sigmoid parameter Mobile Facility (All Sites) | Slope 1.10, Half Width-Half Mean 6.00 | (hb p. 9) |
| Smoothing box-car threshold | average of four nearest neighbors; if relative average differs from center point by more than 20%, replace center with five-point average | (hb p. 9) |
| qc_time delta_t_lower_limit | 20. | (hb p. 13) |
| qc_time delta_t_upper_limit | 20. | (hb p. 13) |


## The data

Verified example: **`sgpmergesonde1maceC1.c1`**, file `sgpmergesonde1maceC1.c1.20150626.000000.cdf`
(41.42 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `height`=266 |
| Data variables | 35 |
| QC variables | 14 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2015-06-26T00:00:00 to 2015-06-26T23:59:00 |
| process version | $State: vap-mergesondemace-8.0-0.sol5_10$ |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bar_pres` | kPa | time,height | yes | Barometric pressure |
| `dp` | C | time,height | yes | Dewpoint temperature |
| `potential_temp` | K | time,height | yes | Potential temperature |
| `precip` | mm | time | yes | Precipitation |
| `rh` | % | time,height | yes | Relative humidity |
| `rh_scaled` | % | time,height | yes | Relative humidity scaled using MWR |
| `sh` | g/g | time,height | yes | Specific humidity |
| `temp` | C | time,height | yes | Temperature |
| `time` | - | time | yes | Time offset from midnight |
| `u_wind` | m/s | time,height | yes | Eastward wind component |
| `v_wind` | m/s | time,height | yes | Northward wind component |
| `vap_pres` | kPa | time,height | yes | Vapor pressure |
| `wdir` | deg | time,height | yes | Wind direction |
| `wspd` | m/s | time,height | yes | Wind speed |
| `height` | km above MSL | height | - | Height |
| `sonde_fraction` | fraction | time,height | - | Sonde contribution to the new data point |
| `sonde_fraction_rh` | fraction | time,height | - | Sonde contribution to the new rh |
| `vapor_source` | unitless | time,height | - | Source of the MWR Data used to Produce Scaled RH Field |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmergesonde1maceC1.c1", "2015-06-26", "2015-06-26")
ds = armlive_open("sgpmergesonde1maceC1.c1", "2015-06-26", "2015-06-26", cleanup_qc=True)
```

## Quality control in this product

14 `qc_` companion variables cover 13 of the
35 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmergesonde1maceC1.c1", "19960715", "20260924")
```

The report's own note on quality: Standard bit-packed quality control variables (qc_xxxx) follow each physical variable per ARM QC Standards, with no bits set (zero) representing good data; assessments are 'Bad' (missing data, set to -9999) or 'Indeterminate' (out of valid_min/valid_max range). Additional status fields sonde_fraction and sonde_fraction_rh report the 0-1 weighting of sonde vs. model contribution to each merged value, and vapor_source reports which MWR datastream (Turner/MWRRET or MWR-LOS) was used and whether it had problems (values 0-4, with 4 meaning no MWR vapor data at all).

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Radiosonde dry bias (RS92) | Systematic low bias in humidity/water vapor values from ARM radiosondes prior to correction; corrected values differ from raw sondewnpn-based profiles | Version 2 incorporates the Miloshevich dry bias correction applied to all ARM radiosondes, using the new SONDEADJUST datastream in place of sondewnpn... | (hb p. 6) |
| ECMWF RH bias | Discrepancy between ECMWF-derived relative humidity profiles and observed/stratospheric temperature-consistent values | Version 2 applies the Revercomb ECMWF RH correction (see Wang et al. 2005) | (hb p. 6) |
| ECMWF model does not reach ground level | Missing/undefined model profile values at lowest altitudes without surface data | Surface meteorology and meteorological tower instruments are used as boundary conditions for the lowest levels; ECMWF pressure levels are converted... | (hb p. 8) |
| Sparse/discrete radiosonde sampling | Radiosonde observations only occur at a limited number of launch times/day depending on site, day of week, and balloon ascent; gaps between launches show declining sonde_fraction and... | Merged product fills gaps via double-sigmoid weighted blend between radiosonde and ECMWF profiles, with linear interpolation used to fill gaps... | (hb p. 8) |
| NWS radiosonde RH field unusable | Relative humidity field from the NWS radiosonde (nsa06snwsupabrwX1) input is not used in the merged product | Field excluded from processing; only temperature and pressure readings used from this input | (hb p. 10) |
| MWR-LOS used only as fallback | vapor_source flag values 2 or 3 indicate MWR-LOS datastream was used instead of the physical/statistical retrieval | MWR-LOS (mwrlosC1) is used only when the mwrret1liljclouC1 datastream is not available | (hb p. 10) |
| MWR data quality problems affecting scaled RH | vapor_source flag values 1 or 3 indicate vapor data used had problems; value 4 indicates no MWR vapor data available, meaning scaled RH may be unscaled or degraded | Tracked via vapor_source status field: 0=Turner Datastream without problems, 1=Turner Datastream with problems, 2=MWRLOS without problems, 3=MWRLOS... | (hb p. 17) |
| Missing input data | Output value set to -9999 with corresponding qc bit_1 (precip, vap_pres, bar_pres) or bit_3 (temp, rh, wspd, wdir, u_wind, v_wind, dp, potential_temp, sh, rh_scaled) flagged 'Bad' when data... | Flagged via qc_xxxx bit-packed QC variable associated with each field | (hb p. 8) |
| Value out of valid range | qc_xxxx bit_1 set (Indeterminate) when value less than valid_min; bit_2 set (Indeterminate) when value greater than valid_max, for temp, rh, vap_pres (bar_pres), wspd, wdir, u_wind, v_wind,... | Flagged via bit-packed qc_xxxx variables with Indeterminate assessment | (hb p. 9) |
| qc_time delta anomalies | qc_time bit_1 set when delta time between current and previous samples is zero; bit_2 set when delta time is less than delta_t_lower_limit (20); bit_3 set when delta time is greater than... | Bit-packed qc_time flags with 'Bad' assessment; prior_sample_flag attribute controls whether first sample of a new raw file is compared to previous... | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Miloshevich, LM, et al. 2009. "Accuracy assessment and correction of Vaisala RS92 radiosonde water vapor measurements." Journal of Geophysical Research 114: D11305, doi:10.1029/2008JD011565.2009.
- Troyan, D. 2011. Sonde Adjust Value-Added Product Technical Report. U.S. Department of Energy. DOE/SC-ARM-TR-102.
- Wang, DY, et al. 2005. "Validation of stratospheric temperatures measured by Michelson Interferometer for Passive Atmospheric Sounding (MIPAS) on Envisat." Journal of Geophysical Research 110(D8): D08301.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-087.pdf (19 pages, DOE/SC-ARM/TR-087, by D Troyan)
- Catalog record: ARM data-source index, `instrument_class_code=mergesonde`, read 2026-09-24
- Example file: `sgpmergesonde1maceC1.c1.20150626.000000.cdf` from `sgpmergesonde1maceC1.c1`, 41.42 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
