---
name: arm-vap-varanal
description: ARM Constrained Variational Analysis (varanal) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Temperature, Water vapor mixing ratio, Horizontal wind U component, Horizontal wind V component, Vertical velocity, Horizontal wind divergence), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgp60varanarapC1.c1) and the variable inventory of a real file. Use when working with varanal data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - varanal, Constrained Variational Analysis, sgp60varanarapC1.c1, Temperature, Water vapor mixing ratio, Horizontal wind U component, Horizontal wind V component, Vertical velocity.
---

# VARANAL - Constrained Variational Analysis

VARANAL is an ARM value-added product that derives large-scale forcing data (vertical velocity, advective tendencies, and related atmospheric/surface variables) by constrained variational analysis of sounding, NWP/reanalysis, and surface/satellite observations over an atmospheric column, used to drive and evaluate single-column models, cloud-resolving models, and large-eddy simulations.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 33 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `varanal` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-222 / S Tang, C Tao, S Xie, M Zhang / August 2019](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-222.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1997-04-02 to 2026-01-31 (retired) |
| Datastreams with data | 82 across 18 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/varanal |


## Credit

Everything this skill knows about the retrieval is the work of **S Tang, C Tao, S Xie, M Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> S Tang, C Tao, S Xie, M Zhang. *Description of the ARM Large-Scale Forcing Data from the Constrained Variational Analysis (VARANAL) Version 2*, DOE/SC-ARM-TR-222, August 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-222.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The constrained variational analysis method integrates the column-integrated equations of mass, moisture, dry static energy, and momentum over an atmospheric column between the surface and top of atmosphere, using measurements of winds, temperature, and water vapor mixing ratio from a network of stations. The analyzed state variables (u, v, q, s) are adjusted with minimum deviation from a first guess (radiosonde or NWP analysis) subject to these four equations as strong constraints, by minimizing a cost function weighted by estimated observational error variances. The system is solved numerically using Lagrange multipliers in an iterative scheme, performed simultaneously across all time levels (monthly for continuous forcing). Surface vertical velocity is assumed zero, and geopotential height is derived from virtual temperature via hydrostatic balance. The output large-scale vertical velocity and advective tendencies are constrained to be consistent with observed surface fluxes, TOA/surface radiation, and precipitation.

**Cadence.** input rate Continuous forcing processed monthly (iteration carried out every month); output every 1-hour output (e.g., 'VarAna 1hr RAP_Based v2') for continuous forcing; time dimension example shows 744 records for a 31-day month; averaging Surface station measurements interpolated to 0.5°x0.5° GOES grid boxes and arithmetically averaged; domain averaging over VARANAL dodecagon domain; missing grid boxes filled via Barnes scheme (Lx=50km, Ly=50km, Lt=6hr) (hb p. 10).

## Inputs

The report names these instruments and sibling products: ECOR, EBBR, QCECOR, BAEBBR, MWR, SIROS, GOES VISST, varanal3d (3DCVA product).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Temperature | K | - | - | (hb p. 24) |
| Water vapor mixing ratio | g/kg | - | - | (hb p. 24) |
| Horizontal wind U component | m/s | - | - | (hb p. 24) |
| Horizontal wind V component | m/s | - | - | (hb p. 24) |
| Vertical velocity (omega) | mb/hour | - | climatologically ~20% uncertainty due to... | (hb p. 24) |
| Horizontal wind divergence | 1/s | - | - | (hb p. 25) |
| Horizontal temperature advection | K/hour | - | - | (hb p. 25) |
| Vertical temperature advection | K/hour | - | - | (hb p. 25) |
| Horizontal q advection | g/kg/hour | - | - | (hb p. 25) |
| Vertical q advection | g/kg/hour | - | - | (hb p. 25) |
| Dry static energy/Cp | K | - | - | (hb p. 25) |
| d(dry static energy)/dt/Cp | K/hour | - | - | (hb p. 26) |
| d(temperature)/dt | K/hour | - | - | (hb p. 26) |
| d(water vapor mixing ratio)/dt | g/kg/hour | - | - | (hb p. 26) |
| Apparent heat source Q1 | K/hour | - | - | (hb p. 26) |
| Apparent moisture sink Q2 | K/hour | - | - | (hb p. 26) |
| Surface precipitation | mm/hour | - | - | (hb p. 26) |
| Surface latent heat flux | W/m2 | - | - | (hb p. 27) |
| Surface sensible heat flux | W/m2 | - | - | (hb p. 27) |
| Surface pressure (domain averaged and center) | mb | - | - | (hb p. 27) |
| Surface air temperature | C | - | - | (hb p. 27) |
| Soil temperature | C | - | - | (hb p. 27) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Pressure levels (lev) | 37 levels, units mb | (hb p. 23) |
| Barnes scheme length/time scale | Lx=50km, Ly=50km, Lt=6hr | (hb p. 16) |
| Horizontal interpolation grid | 0.5°×0.5° GOES grid resolution | (hb p. 16) |


## The data

Verified example: **`sgp60varanarapC1.c1`**, file `sgp60varanarapC1.c1.20190801.000000.cdf`
(2.12 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=744, `lev`=37 |
| Data variables | 62 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2019-08-01T00:00:00 to 2019-08-31T23:05:26 |
| dod version | v1.0 |
| process version | N/A |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `LH` | W/m2 | time | - | Surface latent heat flux, upward positive |
| `LH_col` | W/m2 | time | - | Column latent heating |
| `LWP` | cm | time | - | Cloud liquid water path |
| `PWV` | cm | time | - | Column precipitable water |
| `RH_srf` | % | time | - | Surface air relative humidity |
| `SH` | W/m2 | time | - | Surface sensible heat flux, upward positive |
| `T` | K | time,lev | - | Temperature |
| `T_adv_h` | K/hr | time,lev | - | Horizontal Temperature advection |
| `T_adv_v` | K/hr | time,lev | - | Vertical Temperature advection |
| `T_skin` | degC | time | - | Surface skin temperature |
| `T_soil` | degC | time | - | Soil temperature |
| `T_srf` | degC | time | - | Surface air temperature |
| `cld_high` | % | time | - | Satellite-measured high level cloud |
| `cld_low` | % | time | - | Satellite-measured low level cloud |
| `cld_mid` | % | time | - | Satellite-measured middle level cloud |
| `cld_thick` | km | time | - | Satellite-measured cloud thickness |
| `cld_top` | km | time | - | Satellite-measured cloud top |
| `cld_tot` | % | time | - | Satellite-measured total cloud |
| `dTdt` | K/hr | time,lev | - | Derivative of air temperature with respect to time |
| `dh2odt_col` | mm/hr | time | - | Column-integrated derivative of H2O with respect to time |
| `div` | 1/s | time,lev | - | Horizontal wind divergence |
| `dqdt` | g/kg/hr | time,lev | - | Derivative of water vapor mixing ratio with respect to time |
| `dsdt` | K/hr | time,lev | - | Derivative of dry static energy/Cp with respect to time |
| `dsdt_col` | W/m2 | time | - | Column derivative of dry static energy/Cp with respect to time |
| `evap_srf` | mm/hr | time | - | Surface evaporation |
| `h2o_adv_col` | mm/hr | time | - | Column-integrated H2O advection |
| `lev` | hPa | lev | - | Pressure levels |
| `lw_dn_srf` | W/m2 | time | - | Surface downwelling longwave |
| `lw_net_toa` | W/m2 | time | - | Satellite-measured TOA longwave flux, upward positive |
| `lw_up_srf` | W/m2 | time | - | Surface upwelling longwave |


_29 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgp60varanarapC1.c1",
                             "start": "2019-08-01", "end": "2019-08-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp60varanarapC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp60varanarapC1.c1", "2019-08-01", "2019-08-01")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgp60varanarapC1.c1", "2019-08-01", "2019-08-01"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("prec_srf")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 62 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgp60varanarapC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['LH', 'LH_col', 'LWP'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgp60varanarapC1.c1", "19970402", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Step 2 of the workflow (preprocess) includes major quality control of input data, averaging within the domain, filling missing measurements, interpolating to a consistent observation time step, and visual checking; the visual-check step was re-coded from interactive to offline iterative mode. Output large-scale forcing data go through a visual check and SCM/CRM test cycle with user feedback; if a problem is found the process loops back to preprocessing, otherwise the product is finalized ('Everything good').

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Divergence between ECOR and EBBR surface turbulent flux measurements | BAEBBR shows larger latent heat (LH) and smaller sensible heat (SH) compared to QCECOR during summer, seen as offset seasonal cycles in LH/SH plots (Figure 2); leads to considerable... | Version 2 uses merged fluxes from EBBR and ECOR (QCECOR and BAEBBR VAPs) weighted by quality to better represent various surface types within the... | (hb p. 13) |
| Missing RUC/RAP analysis data | Gaps greater than  6 hr in RUC/RAP input data during specific time periods (listed in Table 1, e.g., Dec 2014, May 2016, Feb/Apr/May 2018) that propagate into the continuous forcing output... | Gaps greater than  6 hr are filled with RUC/RAP data from another time period of the same month; gaps less than  6 hr are filled by linear... | (hb p. 16) |
| Overweighting problem from uneven spatial distribution of surface stations | Without correction, domain averages would be biased toward areas with denser station coverage | Surface station measurements are first interpolated onto the GOES 0.5°x0.5° grid before domain averaging | (hb p. 10) |
| Missing measurements in grid boxes with no station coverage | Grid boxes without actual measurements would otherwise be blank/undefined in the merged surface field | Barnes scheme (Barnes 1964) used to fill missing grid boxes with length scale Lx=50km, Ly=50km, Lt=6hr | (hb p. 10) |
| Changing station numbers/locations and datastream names over time | Number and location of contributing surface stations (e.g., KAM mesonet) changes across years, e.g., KAM data only available before September 2013 and thus not shown in later domain maps;... | Analysts should check README files accompanying each version/campaign for the specific input datastreams and station configuration used | (hb p. 9) |
| Neglect of ice processes and cloud hydrometeor advection | Column budget equations do not include ice-phase terms or advection of cloud hydrometeors, so derived forcing may not capture these processes explicitly | - | (hb p. 3) |
| Assumption of zero surface vertical velocity | omega_srf variable is set to zero by construction (source: 'set to zero'), not an independent measurement | - | (hb p. 30) |
| Below-surface data extrapolation | Data below the surface (below-ground pressure levels in the fixed 37-level grid) are set to the lowest available level data rather than physically meaningful values | - | (hb p. 32) |
| Use of NWP/reanalysis substitution when radiosonde or other input unavailable | Field campaign forcing datasets vary in whether upper-level variables come from radiosonde network vs. NWP/reanalysis (RUC, ECMWF, ERA-Interim, MERRA), producing differing... | Xie et al. (2004) found NWP-based forcing agreed well with sounding-based forcing, especially during precipitation periods when the constraint is... | (hb p. 6) |
| Considerable uncertainty in derived large-scale vertical velocity (omega) due to surface... | Climatologically ~20% uncertainty in vertical velocity magnitude, visible as spread between QCECOR, BAEBBR, and merged omega profiles in Figure 2 | See Tang et al. (2019) for details; use merged flux product to reduce bias | (hb p. 13) |
| Version 1 vs Version 2 discontinuity in continuous forcing methodology | Step change in flux inputs and derived forcing fields when moving from version 1 period (1999-2011, EBBR-only) to version 2 period (2004-Oct 2018, merged EBBR+ECOR) | Users should note version differences (fixed bugs, updated input data version, optimized workflow) when comparing across versions or splicing datasets | (hb p. 7) |
| Field-campaign forcing products rely on heterogeneous, campaign-specific input data... | Data provenance and quality vary by campaign; some fields derived purely from reanalysis (e.g., ISDAC) while others blend radiosonde, radar, and surface stations | Consult README files with each field-campaign dataset for specific VARANAL setup, input sources, and version information | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Zhang, M, and J Lin. 1997. Journal of the Atmospheric Sciences 54(11): 1503-1524
- Zhang, M, S Xie, RT Cederwall, and JJ Yio. 2001a. DOE/SC-ARM-TR-005
- Zhang, M, J Lin, RT Cederwall, JJ Yio, and SC Xie. 2001b. Monthly Weather Review 129(2): 295-311
- Xie, S, RT Cederwall, and M Zhang. 2004. Journal of Geophysical Research - Atmospheres 109(D1): D01104
- Tang, S, S Xie, M Zhang, Q Tang, Y Zhang, SA Klein, DR Cook, and RC Sullivan. 2019. Journal of Geophysical Research - Atmospheres 124(6): 3301-3318
- Tang, S, and M Zhang. 2015. Journal of Geophysical Research - Atmospheres 120(15): 7283-7299
- Tang, S, M Zhang, and S Xie. 2016a. Journal of Geophysical Research - Atmospheres 121(1): 33-48
- Cressman, GP. 1959. Monthly Weather Review 87(10): 367-374
- Barnes, SL. 1964. Journal of Applied Meteorology 3(4): 396-409
- Cook, DR. 2019a. ECOR Instrument Handbook, DOE/SC-ARM/TR-052

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-222.pdf (33 pages, DOE/SC-ARM-TR-222, by S Tang, C Tao, S Xie, M Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=varanal`, read 2026-09-24
- Example file: `sgp60varanarapC1.c1.20190801.000000.cdf` from `sgp60varanarapC1.c1`, 2.12 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
