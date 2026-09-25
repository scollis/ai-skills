---
name: arm-vap-lclheight
description: ARM Lifting Condensation Level Height (lclheight) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Lifting condensation level height, Temperature, Relative humidity, Pressure), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgplclC1.c1) and the variable inventory of a real file. Use when working with lclheight data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - lclheight, Lifting Condensation Level Height, sgplclC1.c1, Lifting condensation level height, Temperature, Relative humidity, Pressure, Derived Quantities and Models.
---

# LCLHEIGHT - Lifting Condensation Level Height

The LCL Height VAP is a value-added product that computes lifting condensation level height (in meters) at 16 ARM SGP facilities and 133 Oklahoma Mesonet stations from continuous surface meteorological observations of temperature, relative humidity, and pressure.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 11 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `lclheight` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-242 / T Toto, A Vogelmann, S Endo, K Gaustad, S Giangrande / April 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-242.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2017-01-01 to 2023-06-01 (retired) |
| Datastreams with data | 1 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/lclheight |


## Credit

Everything this skill knows about the retrieval is the work of **T Toto, A Vogelmann, S Endo, K Gaustad, S Giangrande** -
the ARM developers and mentors who wrote the technical report it derives from:

> T Toto, A Vogelmann, S Endo, K Gaustad, S Giangrande. *Lifting Condensation Level Height (LCL Height) Value-Added Product Report*, DOE/SC-ARM-TR-242, April 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-242.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The LCL is determined using a parcel method: the height at which the parcel water vapor mixing ratio qv reaches the parcel saturation water vapor mixing ratio qvs, i.e., z_LCL = z(qv = qvs). In an adiabatic air parcel, the initial water vapor mixing ratio is conserved while temperature T and pressure p decrease following the dry adiabatic lapse rate (dT/dz = -g/cp) and hydrostatic equilibrium (dp/dz = -ρg). Saturation water vapor mixing ratio is calculated from a variation of Teten's approximation for saturation vapor pressure as a function of temperature. The algorithm updates the parcel's thermodynamic state (T, p, ρ) for each 0.5 m increment in z and evaluates parcel qvs against qv until qvs becomes smaller than qv, at which point the LCL height is determined.

**Cadence.** input rate 1-min observations from MET; 5-min time resolution from OKM stations; output every 1-min time resolution LCL estimates for SGP facilities; effective 5-min time resolution for OKM stations (hb p. 6).

## Inputs

The report names these instruments and sibling products: ARM Surface Meteorology Systems (MET), Meteorological Automatic Weather Station (MAWS), Oklahoma Mesonet (OKM).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Lifting condensation level height | m | - | - | (hb p. 6) |
| Temperature | - | - | - | (hb p. 6) |
| Relative humidity | - | - | - | (hb p. 6) |
| Pressure | - | - | - | (hb p. 6) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Vertical increment for parcel ascent calculation | 0.5 m | (hb p. 8) |
| Number of ARM SGP facilities | 16 | (hb p. 6) |
| Number of OKM stations | 133 | (hb p. 6) |


## The data

Verified example: **`sgplclC1.c1`**, file `sgplclC1.c1.20230601.000000.nc`
(5.61 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2, `stations`=136 |
| Data variables | 14 |
| QC variables | 3 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2023-06-01T00:00:00 to 2023-06-01T23:59:00 |
| dod version | lcl-c1-1.4 |
| process version | vap-lassolcl-1.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `pressure` | kPa | time,stations | yes | Atmospheric Pressure |
| `relative_humidity` | % | time,stations | yes | Relative humidity |
| `temperature` | K | time,stations | yes | Atmospheric Temperature |
| `lcl` | m | time,stations | - | Lifting condensation level |
| `stations_name` | 1 | stations | - | Station names |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgplclC1.c1",
                             "start": "2023-06-01", "end": "2023-06-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgplclC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgplclC1.c1", "2023-06-01", "2023-06-01")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgplclC1.c1", "2023-06-01", "2023-06-01"))   # cite what you pulled
```

## Quality control in this product

3 `qc_` companion variables cover 3 of the
14 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_temperature"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("temperature", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["temperature", "relative_humidity", "pressure"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgplclC1.c1.20230601.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `relative_humidity` | QC_BAD: Transformation could not finish, value set to... | 12982 | 6.6289 |
| `temperature` | QC_BAD: Transformation could not finish, value set to... | 12962 | 6.6187 |
| `pressure` | QC_BAD: Transformation could not finish, value set to... | 12962 | 6.6187 |
| `relative_humidity` | QC_OUTSIDE_RANGE: No input samples exist in the transformation... | 8662 | 4.423 |
| `temperature` | QC_OUTSIDE_RANGE: No input samples exist in the transformation... | 8642 | 4.4128 |
| `pressure` | QC_OUTSIDE_RANGE: No input samples exist in the transformation... | 8642 | 4.4128 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgplclC1.c1", "20170101", "20260924")
```

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| MET data file unavailable for SGP E13 | For SGP E13, LCL computed from substituted MAWS C1 datastream instead of MET; users comparing E13-labeled LCL time series to E13 site conditions may actually be seeing C1 station data on... | MAWS data (maws.b1) at SGP C1 is used as a substitute when metE13.b1 is not available for a day | (hb p. 6) |
| Discretized parcel ascent algorithm resolution | LCL height values are quantized to 0.5 m increments since the parcel state is updated stepwise every 0.5 m in z until qvs falls below qv | - | (hb p. 8) |
| Approximate saturation vapor pressure formula (Teten's approximation variant) | Small systematic differences from other saturation vapor pressure formulations may appear in computed qvs and thus LCL height, since the VAP uses a specific variation of Teten's... | - | (hb p. 8) |
| Mixed input temporal resolution across networks | SGP facility LCL time series are reported at 1-min resolution while OKM station LCL time series are reported at effective 5-min resolution within the same daily output file, so users... | - | (hb p. 8) |
| LCL heights reported relative to SGP C1 altitude, not each station's own elevation datum | Time series of LCL in quicklook plots are expressed in meters above ground level with respect to the height of SGP C1, so stations at different elevations could show offset LCL values if... | - | (hb p. 9) |
| Quicklook time series limited to stations within 60 km of SGP C1 | Although LCL is computed for all colored and black dots on the Oklahoma map (16 SGP facilities and 133 OKM stations), the quicklook time series plot only displays stations/facilities within... | - | (hb p. 9) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- MT Ritsche. 2011. ARM Surface Meteorology Systems Handbook. DOE/SC-ARM/TR-086.
- Brock, FV, KC Crawford, RL Elliott, GW Cuperus, SJ Stadler, HL Johnson, and MD Eilts. 1995. "The Oklahoma Mesonet: A Technical Overview." Journal of Atmospheric and Oceanic Technology 12(1): 5-19.
- Gustafson, WI, et al. 2016. Description of the LASSO Alpha 1 Release. DOE/SC-ARM-TR-194.
- Gustafson, WI, et al. 2017. Description of the LASSO Alpha 2 Release. DOE/SC-ARM-TR-199.
- Gustafson, WI, et al. 2018. Description of the LASSO Data Bundles Product. DOE/SC-ARM-TR-216.
- Gustafson, WI, et al. 2020. "The Large-Eddy Simulation (LES) Atmospheric Radiation Measurement (ARM) Symbiotic Simulation and Observation (LASSO) Activity for Continental Shallow Convection." Bulletin of the American...
- Holdridge, DJ, and JA Kyrouac. 2017. Meteorological Automatic Weather Station (MAWS) Instrument Handbook. DOE/SC-ARM-TR-195.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-242.pdf (11 pages, DOE/SC-ARM-TR-242, by T Toto, A Vogelmann, S Endo, K Gaustad, S Giangrande)
- Catalog record: ARM data-source index, `instrument_class_code=lclheight`, read 2026-09-24
- Example file: `sgplclC1.c1.20230601.000000.nc` from `sgplclC1.c1`, 5.61 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
