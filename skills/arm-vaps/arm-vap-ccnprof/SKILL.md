---
name: arm-vap-ccnprof
description: ARM Cloud Condensation Nuclei Profile (ccnprof) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (CCN concentration profile, Dry extinction, Aerosol extinction coefficient, Relative humidity, Temperature, Pressure), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgprlccnprof1ghanC1.c1) and the variable inventory of a real file. Use when working with ccnprof data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Derived Quantities and Models. Triggers - ccnprof, Cloud Condensation Nuclei Profile, sgprlccnprof1ghanC1.c1, CCN concentration profile, Dry extinction, Aerosol extinction coefficient, Relative humidity, Temperature, Aerosols, Derived Quantities and Models.
---

# CCNPROF - Cloud Condensation Nuclei Profile

CCNPROF is an ARM value-added product that retrieves vertical profiles of cloud condensation nuclei (CCN) concentration at seven supersaturation values by scaling surface CCN measurements with a dry-extinction profile derived from lidar extinction/backscatter, relative humidity, and aerosol hygroscopic growth data, currently implemented for the Raman lidar at the SGP site.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 37 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ccnprof` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-103 / S McFarlane, C Sivaraman, S Ghan / October 2012](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-103.pdf) |
| Category | Aerosols; Derived Quantities and Models |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2006-09-15 to 2014-06-24 (retired) |
| Datastreams with data | 2 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ccnprof |


## Credit

Everything this skill knows about the retrieval is the work of **S McFarlane, C Sivaraman, S Ghan** -
the ARM developers and mentors who wrote the technical report it derives from:

> S McFarlane, C Sivaraman, S Ghan. *Cloud Condensation Nuclei Profile Value-Added Product*, DOE/SC-ARM/TR-103, October 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-103.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The 180-degree extinction (or backscatter) profile E(z) measured by a lidar is corrected to dry conditions, Ed(z), using a vertical profile of relative humidity RH and surface measurements of the dependence of scattering on relative humidity, f[RH(z)]: Ed(z) = E(z)/f[RH(z)]. Surface measurements of CCN concentration at a given supersaturation, CCN(S,0), are then scaled by the ratio of the dry extinction profile Ed(z) to the dry extinction near the surface Ed(0): CCN(S,z) = CCN(S,0)Ed(z)/Ed(0). The method assumes the humidification factor is independent of altitude and that the vertical structure of CCN concentration is identical to that of dry extinction/backscatter, which holds if aerosol size distribution shape and composition are independent of altitude. Dry extinction is computed as Ed(z,t) = E(z,t)*[(100.-40.)/(100-RH(z,t))]^(-gamma(t)), where 40 is the reference relative humidity and gamma(t) is the aerosol humidification fit parameter for that time. The CCN profile at each %ss step is then CCN(z,t,s) = CCN(0,t,s) * Ed(z,t)/Ed(0,s).

**Cadence.** input rate 10-minute (RL extinction), 5-minute per %ss step (AOS CCN, 30-minute full cycle), 20-second (ceilometer); output every one-hour; averaging All input datastreams averaged to one-hour temporal resolution corresponding to the aerosol humidification factor (f(RH)) measurement resolution; only last 4 minutes of each 5-minute %ss step used for CCN averaging (hb p. 5).

## Inputs

The report names these instruments and sibling products: Raman lidar (RL), Micropulse lidar (MPL), High spectral resolution lidar (HSRL), Aerosol Observing System (AOS) CCN counter, Aerosol Intensive Properties (AIP) VAP, Micropulse Lidar Cloud Mask (MPLCMASK) VAP, Merged Sounding VAP, Ceilometer (vceil25k), Raman Lidar Profiles Best Estimate VAP (RLPROFBE).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| CCN concentration profile (7 supersaturation steps) | cm^-3 | - | - | (hb p. 10) |
| Dry extinction (ext_dry_mean) | km^(-1) | valid_min 0.f, valid_max 2.5f | - | (hb p. 25) |
| Aerosol extinction coefficient (ext_mean) | km^(-1) | valid_min 0.f, valid_max 1.f | - | (hb p. 21) |
| Relative humidity (rh_mean) | % | valid_min 0.f, valid_max 100.f | - | (hb p. 21) |
| Temperature (temperature_mean) | K | valid_min 235.f, valid_max 320.f | - | (hb p. 23) |
| Pressure (pressure_mean) | Pa | valid_min 100.f, valid_max... | - | (hb p. 24) |
| Water vapor mixing ratio | g/kg | valid_min 0.f, valid_max 30.f | - | (hb p. 23) |
| AOS CCN number concentration (N_CCN_1..7) | 1/cm^3 | - | - | (hb p. 32) |
| Hygroscopic growth/humidification fit coefficients... | unitless | valid_min 0.f, valid_max 2.f | - | (hb p. 29) |
| Cloud base height (cbh) | km | valid_min 0.f, valid_max 25.f | - | (hb p. 35) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Temporal resolution of all input data averaging | one-hour | (hb p. 5) |
| Vertical resolution of input extinction (RL) | 7.5-meter non-uniform grid | (hb p. 6) |
| Vertical resolution of input extinction (MPL) | 15-meter vertical grid | (hb p. 10) |
| Native temporal resolution of RL input extinction profiles | 10-minute | (hb p. 6) |
| Maximum output altitude | cloud base or maximum altitude of 4 kilometers | (hb p. 10) |
| AOS CCN supersaturation steps | 7 intervals every 30 minutes, 5 minutes each; nominal %ss settings 0.15, 0.2, 04 [0.4], 0.6, 0.8, 1.0, 1.15 | (hb p. 7) |
| Reference relative humidity in dry extinction formula | 40 % | (hb p. 8) |
| f(RH) second fit parameter limits | min 0, max 2 | (hb p. 7) |
| CCN_dT_TEC3_TEC1_StdDev unstable-temperature threshold | greater than  .05 | (hb p. 7) |
| aosccn required samples per day for VAP to run | exactly 1440 samples | (hb p. 4) |
| Extinction std dev QC threshold (bit_13) | greater than  0.06 km^-1 sets value to -9999 | (hb p. 22) |
| ext_mean valid range | 0.f to 1.f km^-1 | (hb p. 22) |
| ext_dry_mean valid range | 0.f to 2.5f km^-1 | (hb p. 25) |
| rh_mean valid range | 0.f to 100.f % | (hb p. 21) |
| temperature_mean valid range | 235.f to 320.f K | (hb p. 23) |
| pressure_mean valid range | 100.f to 110000.f Pa | (hb p. 24) |
| water_vapor_mixing_ratio_mean valid range | 0.f to 30.f g/kg | (hb p. 23) |
| fRH_Bs_B_10um_2p valid range | 0.f to 2.f | (hb p. 29) |
| cbh valid range | 0.f to 25.f km | (hb p. 35) |
| Output file dimensions example (2009-07-20) | time=24 (unlimited), height=52, param2=2, ss_step=7 | (hb p. 20) |
| Ceilometer resolution | 20-second resolution | (hb p. 8) |


## The data

Verified example: **`sgprlccnprof1ghanC1.c1`**, file `sgprlccnprof1ghanC1.c1.20140624.000000.cdf`
(0.2 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=24, `height`=52, `param2`=2, `ss_step`=7 |
| Data variables | 62 |
| QC variables | 25 (`qc_` companions) |
| Median time step | 3584 s |
| File time span | 2014-06-24T00:00:00 to 2014-06-24T23:00:16 |
| dod version | rlccnprof1ghan-c1-0.5 |
| process version | v1.2 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `CCN_ss_calc` | % | time,ss_step | yes | AOS CCN sample supersaturation calculated by model |
| `CCN_ss_set` | % | time,ss_step | yes | AOS CCN sample saturation setpoint value reported by instrument |
| `N_CCN_1` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 1 |
| `N_CCN_2` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 2 |
| `N_CCN_3` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 3 |
| `N_CCN_4` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 4 |
| `N_CCN_5` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 5 |
| `N_CCN_6` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 6 |
| `N_CCN_7` | 1/cm^3 | time | yes | AOS number concentration of CCN at supersaturation step 7 |
| `be_ccn_ss` | % | time,ss_step | yes | The best estimate value of CCN_calc and CCN_ss |
| `ccn_1` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 1 |
| `ccn_2` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 2 |
| `ccn_3` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 3 |
| `ccn_4` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 4 |
| `ccn_5` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 5 |
| `ccn_6` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 6 |
| `ccn_7` | cm^(-3) | time,height | yes | Cloud condensation nuclei at supersaturation step 7 |
| `ext_dry_mean` | km^(-1) | time,height | yes | Aerosol extinction coefficient that is corrected to dry conditions... |
| `ext_mean` | km^(-1) | time,height | yes | Aerosol extinction coefficient |
| `fRH_Bs_B_10um_2p` | unitless | time,param2 | yes | Coefficients for 2 parameter fit of Bs_B_10um hygroscopic growth as a... |
| `pressure_mean` | Pa | time,height | yes | Pressure |
| `rh_mean` | % | time,height | yes | Relative humidity observed by the Raman lidar |
| `temperature_mean` | K | time,height | yes | Air temperature |
| `time` | - | time | yes | Time offset from midnight |
| `water_vapor_mixing_ratio_mean` | g/kg | time,height | yes | Water vapor mixing ratio observed by the Raman lidar |
| `CCN_ss_calc_std_dev` | % | time,ss_step | - | Standard deviation of AOS CCN sample supersaturation calculated by... |
| `CCN_ss_set_std_dev` | % | time,ss_step | - | Standard Deviation of AOS CCN sample saturation setpoint value... |
| `cbh` | km | time | - | Lowest cloud base height from Raman Lidar and/or ceilometer in... |
| `ext_err` | km^(-1) | time,height | - | Aerosol extinction coefficient uncertainty |
| `ext_std_dev` | km^(-1) | time,height | - | Standard deviation of aerosol extinction coefficient |


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
                     params={"user": f"{user}:{token}", "ds": "sgprlccnprof1ghanC1.c1",
                             "start": "2014-06-24", "end": "2014-06-24", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgprlccnprof1ghanC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgprlccnprof1ghanC1.c1", "2014-06-24", "2014-06-24")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgprlccnprof1ghanC1.c1", "2014-06-24", "2014-06-24"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cbh")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 62 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgprlccnprof1ghanC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["rh_mean", "ext_mean", "water_vapor_mixing_ratio_mean", "qc_rh_mean", "qc_ext_mean", "qc_water_vapor_mixing_ratio_mean"],
                                cleanup_qc=True)
```

## Quality control in this product

25 `qc_` companion variables cover 24 of the
62 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_rh_mean"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("rh_mean", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["rh_mean", "ext_mean", "water_vapor_mixing_ratio_mean"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgprlccnprof1ghanC1.c1.20140624.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `ccn_3` | Data value not available in input file, data value set to -9999... | 1248 | 100.0 |
| `ccn_1` | Extinction dry data value outside the minimum or maximum range,... | 1248 | 100.0 |
| `ccn_6` | Data value not available in input file, data value set to -9999... | 1248 | 100.0 |
| `ccn_5` | Extinction dry data value outside the minimum or maximum range,... | 1248 | 100.0 |
| `ccn_5` | Data value not available in input file, data value set to -9999... | 1248 | 100.0 |
| `ccn_4` | Extinction dry data value outside the minimum or maximum range,... | 1248 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgprlccnprof1ghanC1.c1", "20060915", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Quality control flags are applied at multiple stages: on the input extinction, temperature, water vapor, and RH profiles (based on gridding, interpolation, extrapolation, valid_min/max, and missing-data bits); on the averaged (hourly) extinction, RH, temperature, and pressure fields (including a std-dev threshold bit for extinction); on the f(RH) fit parameters (multiple bad/indeterminate bits related to RH range coverage, r-square, sample count, and ratio validity); on the dry extinction and CCN profile outputs (bad/indeterminate bits tied to input QC and valid-range violations); and on the...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Humidification influence on extinction near cloud base | Raw aerosol extinction profiles show enhanced scattering near cloud base that does not correspond to actual CCN structure; must be removed via dry-extinction correction before use | Correct extinction to dry conditions using RH profile and surface f(RH) before relating to CCN (Ed(z)=E(z)/f[RH(z)]) | (hb p. 5) |
| Assumption that humidification factor f(RH) is altitude-independent | Retrieved CCN/dry-extinction profile error grows if actual aerosol composition/size distribution varies with height, since surface f(RH) is applied at all heights | Handbook notes validity depends on aerosol size distribution shape and composition/shape being independent of altitude | (hb p. 5) |
| Assumption that CCN vertical structure equals dry extinction/backscatter vertical... | Any divergence between aerosol optical and CCN-active size distributions with height causes retrieval error not visible in the extinction data alone | None stated beyond noting the assumption | (hb p. 5) |
| RL cannot directly measure extinction below 800 m | Extinction (and Sa) below 800 m is not directly retrieved; profile relies on extrapolated Sa to the surface | Extinction-to-backscatter ratio Sa is smoothed over all times/heights and extrapolated to the surface | (hb p. 6) |
| RL cloud mask insufficient to mask clouds | Spikes in retrieved CCN values aloft when relying on RL cloud mask alone | Use ceilometer 'first_cbh' lowest cloud base height variable in addition to lidar cloud mask | (hb p. 4) |
| MPL cloud mask only valid above 1 km | Cloud contamination below 1 km not flagged by MPL cloud mask | Supplement with ceilometer cbh data | (hb p. 4) |
| Conservative cloud-masking from ceilometer at 20-second resolution vs 10-minute lidar | A single ceilometer cbhgreater than 0 reading within a 10-minute lidar averaging interval flags the entire interval, potentially over-flagging otherwise valid data | Handbook notes this is a fairly conservative approach, applied intentionally | (hb p. 4) |
| AOS CCN instrument step transition instability | First minute of each %ss step shows anomalous/unstable CCN readings | Only the last four minutes of each 5-minute %ss step are used | (hb p. 3) |
| Unstable column temperature in CCN counter | CCN_dT_TEC3_TEC1_StdDev greater than  .05 indicates instability between top and bottom of instrument column | Data flagged and not used when threshold exceeded | (hb p. 3) |
| Wavelength dependence of f(RH) not fully resolved | f(RH) measured only at blue wavelength rather than extrapolated via Angstrom exponent to lidar wavelength; could introduce bias for aerosols with different size distributions | Blue wavelength chosen because it is expected to have larger, more robust aerosol signal; full 3-wavelength extrapolation not implemented due to... | (hb p. 3) |
| f(RH) second parameter out-of-range rejection | Both f(RH) fit parameters set to missing when second parameter falls outside 0-2 limits, causing gaps in dry-extinction and CCN profile retrieval for that hour | Min/max limits of 0 and 2 applied; values outside range set to missing | (hb p. 3) |
| Missing AIP or incomplete aosccn data causes VAP not to run for the day | No output file produced for days when AIP data file unavailable or aosccn file lacks exactly 1440 samples | None; VAP simply does not run for that day | (hb p. 4) |
| Negative or excessively high extinction values after averaging | Negative extinction values from low signal-to-noise, or extremely high values likely from cloud contamination, appear in averaged extinction profile | Min/max valid range checks applied to remove/flag these after averaging | (hb p. 4) |
| Extinction standard deviation exceeding threshold | Bit 13 QC flag trips and ext_mean set to -9999 when std dev of extinction mean greater than  0.06 km^-1, indicating high within-hour variability | Flagged as bad in qc_ext_mean | (hb p. 22) |
| Rapidly changing aerosol or boundary-layer meteorology within averaging hour | High standard deviation values reported alongside hourly means for extinction, temperature, humidity, and surface CCN | Handbook suggests standard deviations could be used to identify/exclude such times, and average/std dev of surface CCN and profiles are output for... | (hb p. 6) |
| Cloud contamination above cloud base | Extinction/backscatter values above detected cloud base height set to -9999 with qc flag set | Values above cbh (from lidar cloud mask or ceilometer first_cbh) are masked to -9999 | (hb p. 4) |
| Propagated QC flags through retrieval chain | qc_ext_dry_mean and qc_ccn_1..7 flags encode bad/indeterminate status inherited from extinction, RH, f(RH), and surface CCN input QC as well as valid-range violations | Analysts should check bit-packed qc variables described in netCDF header before using output values | (hb p. 25) |
| MPL and HSRL implementations still under development at time of report | Only RL/SGP output files (sgprlccnprof1ghanC1.c1...) are currently produced; MPL and HSRL datastreams not yet available | Planned future work | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Ghan, SJ and DR Collins. 2004. Use of in situ data to test a Raman lidar-based cloud condensation nuclei remote sensing method. Journal of Atmospheric and Ocean Technology 21: 387-394.
- Ghan, SJ, TA Rissman, R Elleman, RA Ferrare, D Turner, C Flynn, J Wang, J Ogren, J Hudson, HH Johnsson, T VanReken, RC Flagan, and JH Seinfeld. 2006. Use of in situ cloud condensation nuclei, extinction, and aerosol...
- Jefferson, A. 2011. Aerosol Observing System Instrument Handbook. DOE/SC-ARM/TR-014.
- Newsom, R. 2012. Raman Lidar Profiles Best Estimate Value-Added Product Technical Report. DOE/SC-ARM/TR-100.
- Sivaraman, C, and J Comstock. 2011. Micropulse Lidar Cloud Mask Value-Added Product Technical Report. DOE/SC-ARM/TR-098.
- Troyan, D. 2010. Merged Sounding Value-Added Product. DOE/SC-ARM/TR-087.
- Turner et al. 2002 (extinction/backscatter/Sa calculation method for Raman lidar)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-103.pdf (37 pages, DOE/SC-ARM/TR-103, by S McFarlane, C Sivaraman, S Ghan)
- Catalog record: ARM data-source index, `instrument_class_code=ccnprof`, read 2026-09-24
- Example file: `sgprlccnprof1ghanC1.c1.20140624.000000.cdf` from `sgprlccnprof1ghanC1.c1`, 0.2 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
