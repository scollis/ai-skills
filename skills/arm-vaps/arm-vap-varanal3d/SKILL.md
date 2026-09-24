---
name: arm-vap-varanal3d
description: ARM Three-dimensional Constrained Variational Analysis (varanal3d) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (U wind, V wind, dry static energy/Cpd, geopotential height, divergence of wind), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgp180varanal3drucC1.c1) and the variable inventory of a real file. Use when working with varanal3d data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Derived Quantities and Models. Triggers - varanal3d, Three-dimensional Constrained Variational Analysis, sgp180varanal3drucC1.c1, U wind, V wind, dry static energy/Cpd, geopotential height, Derived Quantities and Models.
---

# VARANAL3D - Three-dimensional Constrained Variational Analysis

VARANAL3D is a derived ARM value-added product providing three-dimensional large-scale forcing data (adjusted state variables, vertical velocity, advections, budget terms) over a multi-column analysis domain at the SGP site, produced by variationally adjusting reanalysis background fields to satisfy column-integrated mass, moisture, heat, and radiative constraint equations using ARM surface and TOA observations.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 31 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `varanal3d` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-253 / S Tang, S Xie, M Zhang / August 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-253.pdf) |
| Category | Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2000-03-01 to 2011-06-06 (retired) |
| Datastreams with data | 9 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/varanal3d |


## Credit

Everything this skill knows about the retrieval is the work of **S Tang, S Xie, M Zhang** -
the ARM developers and mentors who wrote the technical report it derives from:

> S Tang, S Xie, M Zhang. *Description of the Three-Dimensional Large-Scale Forcing Data from the 3D Constrained Variational Analysis (VARANAL3D)*, DOE/SC-ARM-TR-253, August 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-253.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The 3DCVA algorithm extends the one-dimensional constrained variational analysis (1DCVA) to a three-dimensional domain of many interacting sub-columns on an adjusted C-grid, adjusting background reanalysis fields of wind, specific humidity, and dry static energy (u, v, q, s) within their uncertainties so that column-integrated conservation equations for mass, water vapor, heat, and (optionally) momentum are satisfied in each grid box, with surface/TOA fluxes and precipitation treated as constraint 'truth' variables. Above cloud top or 400 hPa (whichever is higher), an additional radiative heating constraint is imposed to remove spurious heating/cooling from vertical velocity errors amplified through vertical advection of dry static energy. To keep specific humidity physically positive, the algorithm adjusts ln(q) rather than q directly. The adjustment minimizes a cost function weighted by an error covariance matrix (via Lagrange multipliers and Newton's iteration, solved with the LSQR sparse least-squares method) that includes horizontal and vertical spatial correlations, using either time variance of background data or, in the ensemble framework, the covariance among multiple reanalysis background data sets as the error estimate. An ensemble product is formed by running 3DCVA separately on each of several reanalysis/analysis background data sets and averaging the resulting forcing fields, rather than assimilating an ensemble mean background.

**Cadence.** input rate 3-hour time resolution (ensemble background interpolation); output every example output time dimension = 168 (3-hourly over ~3 weeks for 0003 IOP based on file naming); averaging Users can run generate_forcing_3DCVA.m to average the 3D product into 1D forcing data at different spatial resolutions (hb p. 12).

## Inputs

The report names these instruments and sibling products: 1DCVA / VARANAL (1D constrained variational analysis, ARM..., VISST (cloud-top pressure input), RRTMG (radiative transfer model used for radiative heating constraint).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| U wind (grid center and staggered) | m/s | - | - | (hb p. 22) |
| V wind (grid center and staggered) | m/s | - | - | (hb p. 22) |
| water vapor mixing ratio / specific humidity (grid center... | kg/kg | - | - | (hb p. 22) |
| dry static energy/Cpd (T+g*z/Cpd) | K | - | - | (hb p. 22) |
| geopotential height | gpm | - | - | (hb p. 22) |
| divergence of wind | 1/s | - | - | (hb p. 23) |
| pressure vertical velocity (omega) | Pa/s | - | - | (hb p. 23) |
| time change of moisture (dq/dt) | kg/kg/s | - | - | (hb p. 23) |
| horizontal/vertical advection of q | kg/kg/s | - | - | (hb p. 23) |
| apparent moisture sink Q2 | K/s | - | - | (hb p. 23) |
| time tendency of dry static energy (ds/dt) | K/s | - | - | (hb p. 24) |
| horizontal/vertical advection of s | K/s | - | - | (hb p. 24) |
| apparent heat source Q1 | K/s | - | - | (hb p. 24) |
| temperature (T) | K | - | - | (hb p. 24) |
| time tendency of temperature (dT/dt) | K/s | - | - | (hb p. 25) |
| horizontal/vertical advection of T | K/s | - | - | (hb p. 25) |
| relative humidity (RH) | % | - | - | (hb p. 25) |
| surface downward latent heat flux | W/m^2 | - | - | (hb p. 25) |
| surface downward sensible heat flux | W/m^2 | - | - | (hb p. 25) |
| surface pressure | hPa | - | - | (hb p. 26) |
| surface temperature | degC | - | - | (hb p. 26) |
| surface relative humidity | % | - | - | (hb p. 26) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Typical background data resolution (0003 IOP ensemble) | 0.5°×0.5° horizontal resolution, 25 hPa vertical resolution, 3-hour time resolution | (hb p. 12) |
| Typical 3DCVA domain | ~10×10 horizontal grids | (hb p. 12) |
| Cost-function matrix size (typical domain) | A is a ~10^4 x 10^4 matrix | (hb p. 12) |
| Newton's iteration max iterations (default) | 20 | (hb p. 13) |
| Newton's iteration convergence threshold (default) | 0.01 | (hb p. 13) |
| Output grid (example file, 0003 IOP) | lon=10, lat=9, lev=37 (ensemble output), time=168 | (hb p. 22) |
| Radiative heating constraint layer | applied at each layer above observed cloud top or 400 hPa, whichever is higher | (hb p. 7) |
| 0003 IOP analysis period | 1 March to 22 March 2000 | (hb p. 15) |
| MC3E analysis period | 00Z April 22 to 21Z June 6, 2011 | (hb p. 16) |
| 0003 IOP background reanalyses (6) | RUC, ERA-Interim, CFSR, NARR, MERRA, JRA-55 | (hb p. 15) |
| MC3E background reanalyses (6) | RAP, ERA5, NCEP-2, NARR, MERRA-2, JRA-55 | (hb p. 16) |


## The data

Verified example: **`sgp180varanal3drucC1.c1`**, file `sgp180varanal3drucC1.c1.20110422.000000.nc`
(154.77 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=368, `lev`=38, `lat`=9, `lon`=10, `lon_stag`=11, `lat_stag`=10 |
| Data variables | 74 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 10800 s |
| File time span | 2011-04-22T00:00:00 to 2011-06-06T21:00:00 |
| dod version | 1.1 |
| process version | 1.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `KB` | 1 | time,lat,lon | - | bottom level index |
| `KT` | 1 | time,lat,lon | - | tropopause level index |
| `Lprecip` | kg*K/s/m^2 | time,lat,lon | - | latent heat by precipitation |
| `Q1` | K/s | time,lev,lat,lon | - | Apparent heat source (/cpd) from Yanai et al., (1973) |
| `Q2` | K/s | time,lev,lat,lon | - | Apparent moisture sink (/cpd) from Yanai et al., (1973) |
| `RH` | % | time,lev,lat,lon | - | relative humidity |
| `T` | K | time,lev,lat,lon | - | Temperature at grid center |
| `Ts` | degC | time,lat,lon | - | surface temperature |
| `clddz` | km | time,lat,lon | - | cloud depth |
| `cldhgh` | % | time,lat,lon | - | high cloud amount |
| `cldlow` | % | time,lat,lon | - | low cloud amount |
| `cldmid` | % | time,lat,lon | - | middle cloud amount |
| `cldtot` | % | time,lat,lon | - | total cloud amount |
| `cldtz` | km | time,lat,lon | - | cloud top height |
| `dT_dt` | K/s | time,lev,lat,lon | - | time tendency of temperature |
| `div` | 1/s | time,lev,lat,lon | - | Divergence of wind |
| `dq_dt` | kg/kg/s | time,lev,lat,lon | - | Time change of moisture |
| `ds_dt` | K/s | time,lev,lat,lon | - | time tendency of dry static energy (/cpd) |
| `evapor` | mm/hr | time,lat,lon | - | Surface evaporation |
| `h_advT` | K/s | time,lev,lat,lon | - | horizontal advection of T |
| `h_advq` | kg/kg/s | time,lev,lat,lon | - | horizontal advection of q |
| `h_advs` | K/s | time,lev,lat,lon | - | horizontal advection of s (/cpd) |
| `ins` | W/m^2 | time,lat,lon | - | TOA insolation |
| `lat_stag` | degrees_north | lat_stag | - | latitude at N-S boundary |
| `lev` | millibar | lev | - | levels |
| `lh` | W/m^2 | time,lat,lon | - | Downward surface latent heat |
| `liq` | cm | time,lat,lon | - | liquid water path |
| `lon_stag` | degrees_east | lon_stag | - | longitude at W-E boundary |
| `lwc` | W/m^2 | time,lat,lon | - | TOA clearsky longwave flux |
| `lwt` | W/m^2 | time,lat,lon | - | TOA net longwave flux |


_45 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgp180varanal3drucC1.c1", "2011-04-22", "2011-04-22")
ds = armlive_open("sgp180varanal3drucC1.c1", "2011-04-22", "2011-04-22", cleanup_qc=True)
```

This product carries 74 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
ds = armlive_open("sgp180varanal3drucC1.c1", start, end,
                  keep_variables=['KB', 'KT', 'Lprecip'])
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgp180varanal3drucC1.c1", "20000301", "20260924")
```

The report's own note on quality: Output variables carry a missing_value attribute (-9999. in the main product, 999.9 in the cloud-top pressure input) to flag unavailable data; residual budget terms (rsd_mass, rsd_water, rsd_heat) are provided in the output and can be examined to assess how well the constraint equations were satisfied after adjustment, effectively serving as a data-quality/convergence diagnostic, though the handbook does not describe a separate formal QC flag system.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Spurious heating/cooling centers near tropopause from vertical velocity error... | Large, unphysical Q1 heating or cooling spikes at upper layers near the tropopause when Q1 is computed directly from large-scale dynamics (left-hand side of Eq. 5), caused by amplification... | Impose radiative heating constraint (Eq. 7) at each layer above observed cloud top or 400 hPa, whichever is higher, to remove spurious... | (hb p. 7) |
| Unphysical negative specific humidity from Gaussian adjustment of q at upper levels | Adjusted q field can go negative in the upper troposphere where q values are small, if q itself (rather than ln q) is adjusted assuming Gaussian error distribution | Adjust ln(q) (as variable Q = ln q) instead of q directly, guaranteeing q remains positive regardless of adjustment magnitude | (hb p. 7) |
| Neglect of ice processes and cloud hydrometeor advection | Heating/drying and moisture budgets do not account for ice-phase processes or advection of cloud hydrometeors; apparent discrepancies in Q1/Q2 budgets in ice-cloud regimes | None stated; noted as a simplification | (hb p. 8) |
| Momentum constraint not currently incorporated | Wind fields (u,v) are adjusted only via mass/moisture/heat constraints; momentum/Coriolis constraint equation (4) is not enforced in current 3DCVA implementation | None stated | (hb p. 8) |
| Ill-conditioned error covariance and cost-function matrices | Error covariance matrix B and cost-function matrix A are large, sparse and can be ill-conditioned; condition number increases with number of grid points, number of constraints, and... | Pre-condition the equations before inversion; use LSQR iterative least-squares solver (Paige and Saunders 1982) tuned with normalization factors and... | (hb p. 10) |
| Iteration non-convergence / truncation | Newton's iteration solution may not fully converge within default settings, appearing as residual budget terms (rsd_mass, rsd_water, rsd_heat) not near zero | Loop continues until maximum iteration number (20 default) is reached or gradient norm falls below threshold (0.01 default); these defaults can be... | (hb p. 13) |
| Dependence of derived forcing on choice of background reanalysis/analysis data set | 3D forcing fields (u,v,q,s,Q1,Q2, etc.) differ noticeably between individual-reanalysis-based VARANAL3D products (e.g., cfsr, interim, jra55, merra, narr, ruc, era5, ncep) for the same... | Use the ensemble 3DCVA product (average of forcing derived from multiple background data sets) to characterize and reduce this uncertainty; both... | (hb p. 12) |
| No correlation assumed between different state variables or between different time steps... | Error covariance matrix B is block-diagonal across u, v, q, s (Eq. 15) and has no cross-time-step correlation, which may understate real correlated errors | None stated beyond noting the assumption; horizontal/vertical spatial correlations to neighboring grids are included instead | (hb p. 9) |
| Time-variance-based error covariance conflates natural variability with data uncertainty | When ensemble background data are unavailable and the time-variance method (as in 1DCVA) is used instead, the resulting error covariance includes natural atmospheric variability rather than... | Prefer ensemble covariance from multiple background data sets, which better reflects data uncertainty; time variance retained only as fallback option | (hb p. 11) |
| Missing/gap-filled cloud-top pressure | cldtoppres variable in cloudtop_pressure.nc input carries missing_value = 999.9 where VISST cloud-top pressure retrieval is unavailable, affecting placement of the radiative heating... | None stated beyond flagging missing_value | (hb p. 21) |
| Missing data flagged with sentinel value in output product | All major output variables (u, v, q, s, Q1, Q2, fluxes, etc.) use missing_value = -9999. to flag unavailable or unretrieved data points | None stated beyond using the missing_value attribute for filtering | (hb p. 22) |
| Product currently limited to specific field campaigns and SGP domain | Only two VARANAL3D data sets exist (March 2000 IOP and MC3E, both at SGP); data are not available for other periods or sites, and background reanalysis sets differ between the two campaigns... | None stated; users must use the appropriate reanalysis-specific or ensemble product for the campaign of interest | (hb p. 15) |
| Radiative heating rate for the constraint computed under clear-sky assumption above cloud... | main_rad.f90 (RRTMG) computes radiative heating rate under clear-sky condition using temperature/moisture from output_3d.nc; any residual cloud or aerosol radiative effects above the... | None stated | (hb p. 15) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Tang, S, and M Zhang. 2015. Journal of Geophysical Research – Atmospheres 120(15): 7283-7299, https://doi.org/10.1002/2015JD023621
- Tang, S, M Zhang, and S Xie. 2016. Journal of Geophysical Research – Atmospheres 121(1): 33-48, https://doi.org/10.1002/2015JD024167
- Tang, S, M Zhang, and S Xie. 2017. Journal of Geophysical Research – Atmospheres 122(16): 8724-8738, https://doi.org/10.1002/2017JD026565
- Tang, S, C Tao, S Xie, and M Zhang. 2019. DOE/SC-ARM-TR-222
- Zhang, M, and J Lin. 1997. Journal of the Atmospheric Sciences 54(11): 1503-1524
- Zhang, M, J Lin, RT Cederwall, JJ Yio, and SC Xie. 2001. Monthly Weather Review 129(2): 295-311
- Yanai, M, S Esbensen, and J-H Chu. 1973. Journal of the Atmospheric Sciences 30(4): 611-627
- Paige, CC, and MA Saunders. 1982. ACM Transactions on Mathematical Software 8(1): 43-71
- Xie, S, et al. 2005. Journal of Geophysical Research – Atmospheres 110(D15): D15S03
- Xie, S, Y Zhang, SE Giangrande, MP Jensen, R McCoy, and M Zhang. 2014. Journal of Geophysical Research – Atmospheres, 2014JD022011

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-253.pdf (31 pages, DOE/SC-ARM-TR-253, by S Tang, S Xie, M Zhang)
- Catalog record: ARM data-source index, `instrument_class_code=varanal3d`, read 2026-09-24
- Example file: `sgp180varanal3drucC1.c1.20110422.000000.nc` from `sgp180varanal3drucC1.c1`, 154.77 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
