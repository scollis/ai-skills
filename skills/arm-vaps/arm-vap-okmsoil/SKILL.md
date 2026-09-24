---
name: arm-vap-okmsoil
description: ARM Oklahoma Mesonet Soil Moisture (okmsoil) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Volumetric water content, Matric potential, Sensor temperature rise, Fractional Water Index), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. No data file could be verified for this product, and the skill says so in place of a variable inventory. Use when working with okmsoil data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface/Subsurface Properties. Triggers - okmsoil, Oklahoma Mesonet Soil Moisture, sgpokmsoilX1.c1, Volumetric water content, Matric potential, Sensor temperature rise, Fractional Water Index, Surface/Subsurface Properties.
---

# OKMSOIL - Oklahoma Mesonet Soil Moisture

The OKMSOIL VAP derives volumetric water content and related soil moisture quantities at over 100 Oklahoma Mesonet surface stations surrounding the ARM SGP Central Facility, from measurements of soil matric potential inferred from sensor temperature rise.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 11 pages)
or ARM's data-source catalog. No data file could be verified; see **The data**.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `okmsoil` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-230 / L Gregory, A Cialella, SE Giangrande / October 2019](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-230.pdf) |
| Category | Surface/Subsurface Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-01-01 to 2020-10-22 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/okmsoil |


## Credit

Everything this skill knows about the retrieval is the work of **L Gregory, A Cialella, SE Giangrande** -
the ARM developers and mentors who wrote the technical report it derives from:

> L Gregory, A Cialella, SE Giangrande. *Oklahoma Mesonet Soil Moisture (OKMSOIL) Value-Added Product Report*, DOE/SC-ARM-TR-230, October 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-230.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP converts a sensor's normalized temperature rise into soil matric potential, ψm (kPa), using ψm = -c exp(a ΔTref), where ΔTref is the normalized temperature rise (K) and c and a are calibration constants (0.717 kPa and 1.7880 K-1); a linear regression normalizes each sensor to an idealized reference sensor to remove sensor-to-sensor variability (following Illston et al. 2008). The matric potential is then converted to volumetric water content, θ (m3/m3), via the van Genuchten (1980) equation θ = θr + (θs − θr)/[1 + (−αψm)^n]^m, using site- and depth-specific soil water retention curve parameters θr, θs, α, and n from the Meso-Soil Database (version 1.1), estimated via the Rosetta pedotransfer function (an artificial neural network model, Schaap et al. 2001). The parameter m is computed with a simplified expression following Scott et al. (2013): m = 1 - 1/n. This approach follows algorithms introduced by previous Oklahoma Mesonet activities (e.g., Scott et al. 2013) and requires a comprehensive field soil sampling survey for each OKM station to establish the site-specific retention curve.

**Cadence.** output every 30-minute intervals (time offset from midnight) (hb p. 7).

## Inputs

The report names these instruments and sibling products: sgp30okm.b1 (Oklahoma Mesonet input datastream), Meso-Soil Database.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Volumetric water content | cm3/cm3 (also given as... | - | - | (hb p. 6) |
| Matric potential | kPa | - | - | (hb p. 7) |
| Sensor temperature rise | - | - | - | (hb p. 7) |
| Fractional Water Index | - | - | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Calibration constant c | 0.717 kPa | (hb p. 7) |
| Calibration constant a | 1.7880 K-1 | (hb p. 7) |
| m (fitting parameter) | m = 1 - 1/n | (hb p. 7) |
| Meso-Soil Database version | version 1.1 | (hb p. 7) |
| Output file frequency | daily NetCDF file | (hb p. 7) |
| Primary output temporal resolution | 30-minute temporal resolution | (hb p. 7) |


## The data

**No example file was verified for this instrument.** ARM Live refused every query for this product, which is served only at level a0.

ARM's catalog lists 1 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
files = armlive_list_files("sgpokmsoilX1.c1", start, end)
```

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpokmsoilX1.c1", "2020-10-22", "2020-10-22")
ds = armlive_open("sgpokmsoilX1.c1", "2020-10-22", "2020-10-22", cleanup_qc=True)
```

## Quality control in this product

Not measured - no file was opened, so this skill cannot say which `qc_` variables this
product carries. Confirm with `act_qc_variables(ds)` once you have a file, and read
`act-qc` for the assessment-vocabulary trap before filtering.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpokmsoilX1.c1", "19980101", "20260924")
```

The report's own note on quality: Input data includes a QC flag for sensor temperature rise (qc_trise) from the sgp30okm.b1 datastream. Output variables each have a corresponding QC field: qc_sensor_temperature_rise, qc_matric_potential, qc_volumetric_water_content, and qc_fractional_water_index. The report states that the VAP was validated using "the latest revision of the OKM quality-assured input data."

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Sensor-to-sensor variability in temperature rise measurement | Inconsistent matric potential/water content estimates between sensors at different sites or depths if not corrected | A linear regression normalization is applied to normalize each sensor to that of an idealized reference sensor, following Illston et al. (2008) | (hb p. 7) |
| Small differences between OKMSOIL VAP output and previously published Illston et al.... | Minor discrepancies visible when comparing 1998 Butler station Soil Water Content plots to published Illston et al. (2008) values | Attributed to small improvements in the input data quality of the current OKMSOIL VAP | (hb p. 8) |
| Dependence on Meso-Soil Database soil hydraulic parameter estimates (Rosetta PTF) | Retrieved volumetric water content accuracy is tied to the quality of the pedotransfer-function-estimated van Genuchten parameters (θr, θs, α, n) for each station/depth | Requires a comprehensive field soil sampling survey for each OKM station (Scott et al. 2013) | (hb p. 6) |
| Reliance on QC flag of input sensor temperature rise data | Output volumetric_water_content quality depends on qc_trise flag from the sgp30okm.b1 input datastream | - | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Brock, FV, KC Crawford, RL Elliott, GW Cuperus, SJ Stadler, HL Johnson, and MD Eilts. 1995. "The Oklahoma Mesonet: A technical overview." Journal of Atmospheric and Oceanic Technology 12(1): 5-19
- Illston, BG, JB Basara, CA Fiebrich, KC Crawford, E Hunt, DK Fisher, R Elliott, and K Humes. 2008. "Mesoscale monitoring of soil moisture across a statewide network." Journal of Atmospheric and Oceanic Technology 25(2):...
- Schaap, MG, FJ Leij, and MT van Genuchten. 2001. "ROSETTA: a computer program for estimating soil hydraulic parameters with hierarchical pedotransfer functions." Journal of Hydrology 251(3-4): 163-176
- Scott, BL, TE Ochsner, BG Illston, CA Fiebrich, JB Basara, and AJ Sutherland. 2013. "New soil property database improves Oklahoma Mesonet soil moisture estimates." Journal of Atmospheric and Oceanic Technology 30(11):...
- Van Genuchten, MT. 1980. "A closed-form equation for predicting the hydraulic conductivity of unsaturated soils." Soil Science Society of America Journal 44(5): 892-898

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-230.pdf (11 pages, DOE/SC-ARM-TR-230, by L Gregory, A Cialella, SE Giangrande)
- Catalog record: ARM data-source index, `instrument_class_code=okmsoil`, read 2026-09-24
- Example file: none - ARM Live refused every query for this product, which is served only at level a0
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
