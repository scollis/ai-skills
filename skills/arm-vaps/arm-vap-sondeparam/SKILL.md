---
name: arm-vap-sondeparam
description: ARM convective parameters derived from radiosonde data (sondeparam) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (CAPE, CIN, LCL, LFC, LNB, rh), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpsondeparamC1.c1) and the variable inventory of a real file. Use when working with sondeparam data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Atmospheric Profiling. Triggers - sondeparam, convective parameters derived from radiosonde data, sgpsondeparamC1.c1, CAPE, CIN, LCL, LFC, LNB, Atmospheric Profiling.
---

# SONDEPARAM - convective parameters derived from radiosonde data

The SONDEPARAM VAP computes convective cloud parameters such as CAPE, CIN, LCL, LFC, and LNB from ARM radiosonde (sondewnpn.b1) profile data at ARM sites prone to convective cloud formation.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 14 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sondeparam` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-284 / A Zhou, SE Giangrande, D Wang, M Jensen / December 2022](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-284.pdf) |
| Category | Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2001-04-01 to 2026-09-24 (active) |
| Datastreams with data | 12 across 10 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sondeparam |


## Credit

Everything this skill knows about the retrieval is the work of **A Zhou, SE Giangrande, D Wang, M Jensen** -
the ARM developers and mentors who wrote the technical report it derives from:

> A Zhou, SE Giangrande, D Wang, M Jensen. *Convective Parameters Derived from Radiosonde Data (SONDEPARAM) Value-Added Product Report*, DOE/SC-ARM-TR-284, December 2022.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-284.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The VAP takes vertical profiles of pressure, temperature, dewpoint, relative humidity, and winds from the sondewnpn.b1 radiosonde datastream and applies algorithms from Wang et al. (2020), Jensen et al. (2016), and Giangrande et al. (2020) to compute convective cloud parameters for several parcel assumptions (surface-based, most unstable, mixed-layer). Parcel ascent is treated as pseudo-adiabatic/irreversible saturated adiabatic, with condensed water immediately removed, considering both liquid and ice phases so that latent heat release from freezing adds positive buoyancy above the melting level; hydrometeor loading is neglected under undiluted ascent. Buoyancy at each layer k is computed as B[k] = g*((tv_p - tv_e[k])/tv_e[k]) using virtual potential temperatures of parcel and environment, and LCL, LFC, and LNB are derived from altitude minima/maxima relative to buoyancy sign changes. CAPE and CIN are obtained by summing positive and negative buoyancy-weighted altitude increments (p[k] and c[k]) between the LFC/LNB and LFC/surface layers respectively.

## Inputs

The report names these instruments and sibling products: sondewnpn.b1 (ARM balloon-borne sounding system radiosonde datastream).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| CAPE | J kg-1 | - | - | (hb p. 7) |
| CIN | J kg-1 | - | - | (hb p. 7) |
| LCL | km | - | - | (hb p. 7) |
| LFC | km | - | - | (hb p. 7) |
| LNB | km | - | - | (hb p. 7) |
| rh (low-level relative humidity 0-5km) | % | 0km to 5km | - | (hb p. 7) |
| elr3 (environmental temperature lapse rate 0-3km) | degC km-1 | 0km to 3km | - | (hb p. 7) |
| elr6 (environmental temperature lapse rate 3-6km) | degC km-1 | 3km to 6km | - | (hb p. 7) |
| wind_shear (0-5km) | s-1 | 0km to 5km | - | (hb p. 7) |
| parcel_type | 1 | - | - | (hb p. 7) |
| parcel_layer | km | - | - | (hb p. 7) |
| sonde_height | km | - | - | (hb p. 7) |
| time_highest_level | seconds since 1970-1-1... | - | - | (hb p. 7) |
| data_quality | 1 | - | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| depth of mixed-layer | 482 meters | (hb p. 8) |
| depth of most-unstable-layer | 700 hPa | (hb p. 8) |
| Most Unstable Parcel definition | parcel with greatest virtual temperature in lowest 700mb above surface | (hb p. 8) |
| Surface-Based Parcel definition | parcel at the lowest sounding data level | (hb p. 8) |
| Mixed-Layer Parcel definition | parcel with properties of the mean of the boundary layer | (hb p. 8) |
| Filter 1 threshold - dewpoint jump | abs(dp[0]-dp[1]) greater than  2.5 | (hb p. 11) |
| Filter 1 threshold - tdry jump | abs(tdry[0]-tdry[1]) greater than  2.5 | (hb p. 11) |
| Filter 1 threshold - surface pressure/dp/tdry | pres[0] less than  700; dp less than  -20; tdry less than  -25 | (hb p. 11) |
| Filter 1 MAO-specific threshold | dp less than  0 C or tdry less than  0 C marked bad | (hb p. 11) |
| Filter 2 threshold - sonde max height | height above surface greater than  10km | (hb p. 11) |


## The data

Verified example: **`sgpsondeparamC1.c1`**, file `sgpsondeparamC1.c1.20260917.185609.nc`
(0.62 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4956, `parcel_type`=3 |
| Data variables | 19 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-17T18:56:09 to 2026-09-17T20:18:44 |
| dod version | sondeparam-c1-1.2 |
| process version | sondeparam-1.2.6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cape` | J kg-1 | time,parcel_type | - | Convective available potential energy |
| `cin` | J kg-1 | time,parcel_type | - | Convective inhibition |
| `data_quality` | 1 | time | - | Flag indicating quality of the input data |
| `elr_3` | degC km-1 | time | - | Environmental temperature lapse rates from 0km to 3km |
| `elr_6` | degC km-1 | time | - | Environmental temperature lapse rates from 3km to 6km |
| `lcl` | km | time,parcel_type | - | Lifting condensation level |
| `lcl_lfc_flag` | 1 | time | - | Warning flag when LCL equals to LFC |
| `lfc` | km | time,parcel_type | - | Level of free convection |
| `lnb` | km | time,parcel_type | - | Level of neutral buoyancy |
| `parcel_layer` | km | time,parcel_type | - | The height of the parcel for a given parcel type |
| `parcel_type` | 1 | parcel_type | - | Types of parcel |
| `rh` | % | time | - | Low-level relative humidity from 0km to 5km |
| `sonde_height` | km | time | - | The highest level of radiosonde |
| `time` | - | time | - | Time offset from midnight |
| `time_highest_level` | - | time | - | The time when radiosonde reaches the highest level |
| `wind_shear` | s-1 | time | - | Wind shear from 0km to 5km |


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
                     params={"user": f"{user}:{token}", "ds": "sgpsondeparamC1.c1",
                             "start": "2026-09-17", "end": "2026-09-17", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsondeparamC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsondeparamC1.c1", "2026-09-17", "2026-09-17")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsondeparamC1.c1", "2026-09-17", "2026-09-17"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `data_quality`, `lcl_lfc_flag`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpsondeparamC1.c1", "20010401", "20260924")
```

The report's own note on quality: The output variable 'data_quality' is a flag composed of [sfc_delta_dp, sfc_delta_tdry, bad_dp, bad_tdry, bad_pres, bad_rh, bad_deg, bad_u_wind, bad_v_wind], with threshold values defined by Filter 1 and Filter 2 in Appendix A. These are sanity checks added by the VAP developers because ARM's Data Quality Office QC checks are not currently implemented for these issues. Appendix B further notes that some non-convective cases (e.g., low-level negative lapse rates, elr3 less than  0) are allowable VAP failures outside the intended convective assumptions.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Problematic radiosondes with unusual parameter estimates during initial testing | Subsequent unusual/aberrant convective parameter estimates flagged after VAP processing | Sanity checks (Filter 1 and Filter 2) added into VAP processing to allow processing with fewer failures, since ARM Data Quality Office QC checks are... | (hb p. 11) |
| Large near-surface dewpoint or dry-bulb temperature jumps between first two levels | abs(dp[0]-dp[1]) greater than  2.5 or abs(tdry[0]-tdry[1]) greater than  2.5 triggers 'bad' flag in data_quality | Marked as 'bad' data in flag variable data_quality (Filter 1) | (hb p. 11) |
| Unphysical surface pressure/dewpoint/temperature values | pres[0] less than  700 hPa; dp less than  -20; tdry less than  -25 triggers bad flag | Marked as 'bad' data in data_quality flag (Filter 1) | (hb p. 11) |
| MAO site-specific cold dewpoint/temperature anomaly | dp less than  0 C or tdry less than  0 C at MAO site | Suggested to be marked as 'bad' data in data_quality flag | (hb p. 11) |
| Sonde failing to reach sufficient altitude | Sonde height above surface does not exceed 10km threshold; fraction of sondes exceeding 10km varies by site (e.g., COR/M1 0.0, SGP/C1 0.97, MAO/M1 0.96) | Filter 2 flags/filters based on the 10km height threshold, determined empirically from fraction of sondes reaching that height across sites | (hb p. 11) |
| Low-level negative lapse rates (temperature inversions) in non-convective wintertime cases | elr3 less than  0, indicating tdry increases with height in a deep inversion; occurs a handful of times annually at sites like SGP | Noted by developer as allowable instances for VAP failure since these fall outside intended convective environment assumptions; example... | (hb p. 13) |
| Sensitivity of convective parameters to initial parcel assumption | CAPE, CIN, LNB, etc. vary substantially depending on whether surface-based, most-unstable, or mixed-layer parcel is chosen | VAP baseline implementation includes a variety of parcel options to let users compare/choose | (hb p. 7) |
| Neglect of hydrometeor loading in parcel ascent | CAPE/CIN may be overestimated relative to reality since condensed water loading on parcel buoyancy is not accounted for | None stated beyond noting the assumption of undiluted pseudo-adiabatic ascent | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Giangrande, SE, D Wang, and DB Mechem. 2020. "Cloud regimes over the Amazon Basin: perspectives from the GoAmazon2014/5 campaign." Atmospheric Chemistry and Physics 20(12):7489–7507,...
- Jensen, MP, DJ Holdridge, P Survo, R Lehtinen, S Baxter, T Toto, and KL Johnson. 2016. "Comparison of Vaisala radiosondes RS41 and RS92 at the ARM Southern Great Plains site." Atmospheric Measurement Techniques 9(7):...
- Wang, D, MP Jensen, JA D'Iorio, G Jozef, SE Giangrande, KL Johnson, ZJ Luo, M Starzec, and GL Mullendore. 2020. "An Observational Comparison of Level of Neutral Buoyancy and Level of Maximum Detrainment in Tropical Deep...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-284.pdf (14 pages, DOE/SC-ARM-TR-284, by A Zhou, SE Giangrande, D Wang, M Jensen)
- Catalog record: ARM data-source index, `instrument_class_code=sondeparam`, read 2026-09-24
- Example file: `sgpsondeparamC1.c1.20260917.185609.nc` from `sgpsondeparamC1.c1`, 0.62 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
