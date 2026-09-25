---
name: arm-vap-acsmcdce
description: ARM ACSM, corrected for composition-dependent collection efficiency (acsmcdce) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (acsm_vol_conc_cdce, ammonium_cdce, CDCE, CDCE_equation, chloride_CDCE, nitrate_CDCE), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpacsmcdceC1.c1) and the variable inventory of a real file. Use when working with acsmcdce data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Derived Quantities and Models. Triggers - acsmcdce, sgpacsmcdceC1.c1, acsm_vol_conc_cdce, ammonium_cdce, CDCE, CDCE_equation, chloride_CDCE, Aerosols, Derived Quantities and Models.
---

# ACSMCDCE - ACSM, corrected for composition-dependent collection efficiency

The ACSMCDCE VAP is a daily Python-based algorithm that takes ARM b-1-level Aerodyne ACSM chemical speciation data (organics, sulfate, nitrate, ammonium, chloride mass concentrations) and applies the Middlebrook et al. (2012) composition-dependent collection efficiency correction to produce CDCE-corrected species mass concentrations and diagnostic QC flags.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 15 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `acsmcdce` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-271 / JE Shilling, MS Levin / August 2021](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-271.pdf) |
| Category | Aerosols; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2010-11-18 to 2026-09-24 (active) |
| Datastreams with data | 26 across 13 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/acsmcdce |


## Credit

Everything this skill knows about the retrieval is the work of **JE Shilling, MS Levin** -
the ARM developers and mentors who wrote the technical report it derives from:

> JE Shilling, MS Levin. *Aerosol Chemical Speciation Monitor (ACSM) Composition-Dependent Collection Efficiency (CDCE) Value-Added Product Report*, DOE/SC-ARM-TR-271, August 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-271.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm loads ACSM b-1-level netCDF files, removes 1-point anomalous spikes via a greater than 5x-difference filter and linear interpolation, then smooths the organic, ammonium, nitrate, sulfate, and chloride concentrations with a five-point first-order Savitsky-Golay filter (replacing Middlebrook's original binomial filter used in Igor). It calculates the ammonium nitrate mass fraction (ANMF) and the ammonium mass needed for full neutralization of measured nitrate, sulfate, and chloride (NH4pred), then forms the ratio NH4meas/NH4pred. A decision tree selects one of three CDCE formulas: CDCE=0.5 if NH4pred is below the 0.2 ug/m3 detection limit; CDCE=(0.0833+0.9167*ANMF) (Middlebrook Eq. 4) if the aerosol is largely neutralized (ratiogreater than 0.75); or CDCE=(1-0.73*(NH4meas/NH4pred)) (Middlebrook Eq. 6) if the aerosol is acidic. The resulting CDCE is clipped to the range 0.5-1.0, and each species concentration is corrected by dividing by CDCE (e.g., Org_CDCE = org*(1/CDCE)), after which QA/QC bits are computed and bitpacked.

**Cadence.** output every Daily output file; VAP expected to run daily and generate one file each day; averaging Five-point, first-order Savitsky-Golay smoothing filter applied to organic, ammonium, nitrate, sulfate, and chloride concentrations (hb p. 2).

## Inputs

The report names these instruments and sibling products: Aerodyne aerosol chemical speciation monitor (ACSM, input instrument), Aerosol Observing System (AOS), scanning mobility particle sizer (SMPS), ultra-high-sensitivity aerosol spectrometer (UHSAS).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| acsm_vol_conc_cdce (total particle volume concentration... | cm^3/m^3 (printed as... | - | - | (hb p. 10) |
| ammonium_cdce (mass concentration of ammonium corrected for... | ug/M3 | - | - | (hb p. 10) |
| CDCE (composition-dependent collection efficiency value) | unitless (fraction) | 0.5-1.0 (clipped) | - | (hb p. 10) |
| CDCE_equation (flag for which equation used) | categorical: 1,2,3 | 1-3 | - | (hb p. 10) |
| chloride_CDCE (mass concentration of chloride corrected for... | ug/M3 | - | - | (hb p. 10) |
| nitrate_CDCE (mass concentration of nitrate corrected for... | ug/M3 | - | - | (hb p. 10) |
| sulfate_CDCE (mass concentration of sulfate corrected for... | ug/M3 | - | - | (hb p. 11) |
| total_organics_CDCE (mass concentration of organics... | ug/M3 | - | - | (hb p. 11) |
| total_organics (input, mass concentration of total organics) | ug/m^3 | - | - | (hb p. 9) |
| ammonium (input, mass concentration of ammonium) | ug/m^3 | - | - | (hb p. 9) |
| ammonium_predicted (mass concentration of ammonium... | ug/m^3 | - | detection limit 0.2 ug/m3 | (hb p. 9) |
| sulfate (input, mass concentration of sulfate) | ug/m^3 | - | - | (hb p. 9) |
| nitrate (input, mass concentration of nitrate) | ug/m^3 | - | - | (hb p. 9) |
| chloride (input, mass concentration of chloride) | ug/m^3 | - | - | (hb p. 9) |
| acsm_vol_conc (input, ACSM volume concentration) | cm^3/m^3 | - | - | (hb p. 9) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Instrument detection limit for NH4pred | 0.2 ug/m3 | (hb p. 7) |
| CDCE clipping range | 0.5-1.0 | (hb p. 7) |
| Neutralization threshold for equation selection | NH4meas/NH4pred greater than  0.75 | (hb p. 7) |
| CDCE Equation 4 (neutralized aerosol) | CDCE = (0.0833 + 0.9167*ANMF) | (hb p. 7) |
| CDCE Equation 6 (acidic aerosol) | CDCE = (1 - 0.73*(NH4meas/NH4pred)) | (hb p. 7) |
| CDCE default when NH4pred below LOD | CDCE = 0.5 | (hb p. 7) |
| Spike detection threshold | datapoints more than 5x different than both the previous and next datapoint | (hb p. 7) |
| Smoothing filter | 5-point, first-order Savitsky-Golay filter (SciPy) | (hb p. 6) |
| Density assumptions for volume concentration calc | org = 1.2 g/cm^3; SO4 = 1.77 g/cm^3; NO3 = 1.72 g/cm^3; NH4 = 1.77 g/cm^3; Chl = 1.53 g/cm^3 | (hb p. 9) |


## The data

Verified example: **`sgpacsmcdceC1.c1`**, file `sgpacsmcdceC1.c1.20161222.001505.nc`
(0.04 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=45, `bound`=2 |
| Data variables | 53 |
| QC variables | 13 (`qc_` companions) |
| Median time step | 1727 s |
| File time span | 2016-12-22T00:15:05 to 2016-12-22T23:46:18 |
| dod version | acsmcdce-c1-1.1 |
| process version | acsmcdce-2.2.4 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `CDCE` | 1 | time | yes | Composition dependent collection efficiency |
| `acsm_vol_conc` | cm^3/m^3 | time | yes | ACSM volume concentration |
| `acsm_vol_conc_CDCE` | cm^3/m^3 | time | yes | ACSM volume concentration corrected for the CDCE, ambient aerosol in... |
| `ammonium` | ug/m^3 | time | yes | Mass concentration of ammonium, ambient aerosol in air |
| `ammonium_CDCE` | ug/m^3 | time | yes | Mass concentration of ammonium corrected for the CDCE, ambient... |
| `chloride` | ug/m^3 | time | yes | Mass concentration of chloride, ambient aerosol in air |
| `chloride_CDCE` | ug/m^3 | time | yes | Mass concentration of chloride corrected for the CDCE, ambient... |
| `nitrate` | ug/m^3 | time | yes | Mass concentration of nitrate, ambient aerosol in air |
| `nitrate_CDCE` | ug/m^3 | time | yes | Mass concentration of nitrate corrected for the CDCE, ambient aerosol... |
| `sulfate` | ug/m^3 | time | yes | Mass concentration of sulfate, ambient aerosol in air |
| `sulfate_CDCE` | ug/m^3 | time | yes | Mass concentration of sulfate corrected for the CDCE, ambient aerosol... |
| `total_organics` | ug/m^3 | time | yes | Mass concentration of total organics, ambient aerosol in air |
| `total_organics_CDCE` | ug/m^3 | time | yes | Mass concentration of total organics corrected for the CDCE, ambient... |
| `CDCE_equation` | 1 | time | - | Equation used to calculate the composition dependent collection... |
| `CE` | 1 | time | - | Collection efficiency assumed in b-level files |
| `DAQ_version` | 1 | - | - | Program version number |
| `RIE_CL` | 1 | time | - | Relative ionization efficiency chloride |
| `RIE_NH4` | 1 | time | - | Relative ionization efficiency ammonium |
| `RIE_NO3` | 1 | time | - | Relative ionization efficiency nitrate |
| `RIE_ORG` | 1 | time | - | Relative ionization efficiency organic |
| `RIE_SO4` | 1 | time | - | Relative ionization efficiency sulfate |
| `airbeam_normalization_factor` | 1 | time | - | Airbeam normalization factor |
| `ammonium_predicted` | ug/m^3 | time | - | Mass concentration of ammonium predicted for neutralization. |
| `instrument_serial_number` | 1 | time | - | Instrument serial number |
| `mz_delta` | amu | time | - | Delta m/z for scan mode |
| `mz_resolution` | amu | time | - | Channel m/z resolution |
| `mz_scan_width` | amu | time | - | Scan width for first scan range |
| `mz_start` | amu | time | - | Starting m/z for scan range |
| `new_start` | 1 | time | - | New start acquisition indicator |
| `number_of_sets` | 1 | time | - | Number of sets |


_5 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpacsmcdceC1.c1",
                             "start": "2016-12-22", "end": "2016-12-22", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpacsmcdceC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpacsmcdceC1.c1", "2016-12-22", "2016-12-22")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpacsmcdceC1.c1", "2016-12-22", "2016-12-22"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("total_organics", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 53 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpacsmcdceC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["total_organics", "ammonium", "sulfate", "qc_total_organics", "qc_ammonium", "qc_sulfate"],
                                cleanup_qc=True)
```

## Quality control in this product

13 `qc_` companion variables cover 13 of the
53 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_total_organics"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("total_organics", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["total_organics", "ammonium", "sulfate"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpacsmcdceC1.c1.20161222.001505.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `chloride_CDCE` | qc_chloride has Bad assessment | 8 | 17.7778 |
| `chloride` | Value is less than fail_min | 7 | 15.5556 |
| `ammonium` | Value is less than fail_min | 3 | 6.6667 |
| `ammonium_CDCE` | qc_ammonium has Bad assessment | 3 | 6.6667 |
| `chloride` | Value is greater than fail_max | 1 | 2.2222 |
| `acsm_vol_conc` | acsm_vol_conc failed quality check | 1 | 2.2222 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpacsmcdceC1.c1", "20101118", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: QA/QC tests trigger qc_CDCE bits: bit 1 for negative NH4meas/NH4pred, bit 2 for negative ANMF, bit 3 for ANMFgreater than 1, and bit 4 for NH4pred below the instrument LOD of 0.2 ug/m3. The handbook states these QC bits do not necessarily indicate the CDCE calculation is wrong and instead indicate caution should be used. Additional per-species QC variables (qc_ammonium_cdce, qc_chloride_cdce, qc_nitrate_cdce, qc_sulfate_cdce, qc_total_organics_cdce, qc_acsm_vol_conc_cdce) combine bits for qc_CDCE indeterminate assessment and the corresponding b-1 species QC (bad or indeterminate assessment)....

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| 1-point data spikes in ACSM species concentrations | anomalous positive and negative single-point spikes in organic and ammonium concentration time series, more than 5x different from neighboring points | Filter identifies spikes as datapoints greater than 5x different from both previous and next datapoint; replaced by simple linear interpolation for... | (hb p. 7) |
| NH4pred below instrument detection limit (0.2 ug/m3) | predicted ammonium mass concentration near zero/below 0.2 ug/m3; CDCE_equation flag = 1; qc_CDCE bit 4 set | CDCE defaults to 0.5 in this case | (hb p. 7) |
| CDCE value clipping | CDCE values below 0.5 or above 1.0 in the raw calculation are truncated to exactly 0.5 or 1.0 in the output, creating flat boundary values | Clip CDCE to 0.5-1.0 using NumPy clip function | (hb p. 7) |
| Negative value of (NH4meas/NH4pred) | non-physical negative ratio; qc_CDCE bit 1 set | Flag via QC bit 1; handbook notes QC bits do not necessarily indicate the CDCE calculation is wrong, caution should be used | (hb p. 7) |
| Negative ammonium nitrate mass fraction (ANMF) | non-physical negative ANMF value; qc_CDCE bit 2 set | Flag via QC bit 2 | (hb p. 7) |
| ANMF greater than 1 | non-physical ANMF value greater than 1; qc_CDCE bit 3 set | Flag via QC bit 3 | (hb p. 8) |
| Algorithm port from Igor to Python introduces methodological differences | Smoothing uses 5-point first-order Savitsky-Golay filter (SciPy) instead of Middlebrook's binomial filter (Igor); results may differ slightly from original Middlebrook implementation | Documented as a modification; no further correction given | (hb p. 6) |
| Requires data from preceding and following day for smoothing | VAP output lags b-1 file availability by at least one day; missing adjacent-day input data would prevent proper smoothing/processing | Production of VAP files will lag b-1 file availability by at least one day | (hb p. 9) |
| CE assumed constant (0.5) in underlying b-1 files vs. composition-dependent in VAP | b-1-level ACSM data using fixed CE=0.5 will disagree with CDCE-corrected values, especially for crystalline/solid aerosol compositions (e.g., deliquesced ammonium sulfate) which have lower... | Use CDCE VAP files preferentially over b-1-level files whenever available for improved accuracy | (hb p. 6) |
| Non-refractory limitation of ACSM measurement | Species that do not evaporate on the 600C vaporizer (refractory material, e.g., black carbon, dust, sea salt) are not detected/quantified | - | (hb p. 6) |
| Particle bounce/rebound off vaporizer reduces collection efficiency | Lower apparent mass concentrations than true ambient loading, especially for solid/crystalline particles; manifests as CEless than 1 | Composition-dependent collection efficiency correction (Middlebrook et al. 2012) applied by this VAP | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Alfarra, MR, et al. 2004. Atmospheric Environment 38(34): 5745-5758.
- Allan, JD, et al. 2004. Journal of Geophysical Research - Atmospheres 109(D23): D23S24.
- Drewnick, F, et al. 2003. Atmospheric Environment 37(24): 3335-3350.
- Hogrefe, O, et al. 2004. Journal of the Air & Waste Management Association 54(9): 1040-1060.
- Huffman, JA, et al. 2005. Aerosol Science and Technology 39(12): 1143-1163.
- Middlebrook, AM, R Bahreini, JL Jimenez, and MR Canagaratna. 2012. Aerosol Science and Technology 46(3): 258-271.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-271.pdf (15 pages, DOE/SC-ARM-TR-271, by JE Shilling, MS Levin)
- Catalog record: ARM data-source index, `instrument_class_code=acsmcdce`, read 2026-09-24
- Example file: `sgpacsmcdceC1.c1.20161222.001505.nc` from `sgpacsmcdceC1.c1`, 0.04 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
