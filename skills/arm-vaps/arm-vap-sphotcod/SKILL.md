---
name: arm-vap-sphotcod
description: ARM Cloud optical depth retrieved from multi-channel sunphotometer (sphotcod) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Cloud optical depth, Cloud droplet effective radius, Liquid water path, Zenith sky radiance, Solar zenith angle, MODIS white sky albedo), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpsphotcod2chiuC1.c1) and the variable inventory of a real file. Use when working with sphotcod data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - sphotcod, sgpsphotcod2chiuC1.c1, Cloud optical depth, Cloud droplet effective radius, Liquid water path, Zenith sky radiance, Solar zenith angle, Cloud Properties.
---

# SPHOTCOD - Cloud optical depth retrieved from multi-channel sunphotometer

Retrieves cloud optical depth (and cloud droplet effective radius and liquid water path) from zenith radiance measurements made by a three-channel (440, 870, 1640-nm) Cimel sunphotometer operated in 'cloud mode' at ARM fixed and mobile facility sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 16 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `sphotcod` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-317 / LL Ma, SE Giangrande, JD Rausch, D Wang, C Chiu / June 2025](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-317.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2014-01-01 to 2024-02-13 (retired) |
| Datastreams with data | 4 across 4 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/sphotcod |


## Credit

Everything this skill knows about the retrieval is the work of **LL Ma, SE Giangrande, JD Rausch, D Wang, C Chiu** -
the ARM developers and mentors who wrote the technical report it derives from:

> LL Ma, SE Giangrande, JD Rausch, D Wang, C Chiu. *Three-Channel Sunphotometer Cloud Mode Value-Added Product Report*, DOE/SC-ARM-TR-317, June 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-317.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

During 'cloud mode' the Cimel sunphotometer points to zenith and obtains high-gain, sky-mode zenith radiance observations in at least six of its nine channels; the automated VAP retrieval uses the 440, 870, and 1640-nm channels. The ground-based zenith radiance at a given wavelength can be expressed as a function of the incoming radiance, the cloud effective radius and optical depth, and the albedo of the underlying surface. Including the 1640-nm water-absorbing channel enables simultaneous retrieval of cloud optical depth (tau) and effective radius (re) since 1640-nm radiance decreases with droplet size due to absorption while 870-nm radiance increases due to forward scattering. Perturbed zenith radiances (5-10% normally distributed uncertainty in radiance and surface albedo) are compared against a look-up table computed from the DISORT discrete-ordinate-method radiative transfer model; solutions agreeing with the LUT within 10% at 440 and 870 nm are deemed 'viable,' the five best (smallest 1640-nm error) are averaged, and this is repeated 40 times with random perturbations, with the reported tau and re being the mean of the 40 repetitions. LWP is then computed from the retrieved tau and re assuming vertically constant liquid water content (Stephens 1978).

**Cadence.** input rate cloud-mode channel cycle less than 5 minutes; output every 15-minute intervals in earlier record (prior to Oct 2017 SGP, Feb 2021 ENA); up to 5-minute updates for newer models; averaging mean of 40 repetitions of randomly perturbed retrievals, each averaging the five best of viable solutions (hb p. 7).

## Inputs

The report names these instruments and sibling products: MFRSR, KAZR, MICROBASE, MWRRET, TROPoe, MODIS.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Cloud optical depth | unitless | - | average reported uncertainty 1.19 (unitless)... | (hb p. 8) |
| Cloud droplet effective radius | um | - | average reported uncertainty 2.1 um at ENA;... | (hb p. 8) |
| Liquid water path | g m-2 | - | errors of the order of 50 g m-2 in... | (hb p. 6) |
| Zenith sky radiance (440, 870, 1640 nm) | unitless (normalized... | - | - | (hb p. 14) |
| Solar zenith angle | degree | - | - | (hb p. 14) |
| MODIS white sky albedo | unitless | - | - | (hb p. 14) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Field of view (FOV) | 1.2° | (hb p. 6) |
| Channels used for retrieval | 440, 870, 1640 nm | (hb p. 6) |
| Full cloud-mode channel set | at least six of nine channels: 380 (newer CE318T models), 440, 500, 675, 870, 1020, 1640 nm | (hb p. 7) |
| Time to cycle channels | less than five minutes | (hb p. 7) |
| Retrieval interval (older data) | 15-minute intervals (prior to October 2017 at SGP, February 2021 at ENA) | (hb p. 7) |
| Retrieval interval (newer models) | five-minute updates when not operating in other observing modes | (hb p. 7) |
| MODIS albedo spatial resolution | 500-m | (hb p. 9) |
| MODIS albedo temporal window | 16-day period, computed daily for the ninth day within the window | (hb p. 9) |


## The data

Verified example: **`sgpsphotcod2chiuC1.c1`**, file `sgpsphotcod2chiuC1.c1.20191227.143730.nc`
(0.03 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=95, `bound`=2, `modis_channel`=7, `channel`=6, `gain`=3 |
| Data variables | 23 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 300 s |
| File time span | 2019-12-27T14:37:30 to 2019-12-27T22:27:30 |
| dod version | sphotcod2chiu-c1-2.0 |
| process version | vap-sphotcod2chiu-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `modis_white_sky_albedo` | 1 | modis_channel | yes | Area average of white sky albedo for modis_channel |
| `channel` | nm | channel | - | Nominal wavelength for channel |
| `cloud_optical_depth` | 1 | time,gain | - | Cloud Optical Depth |
| `cloud_optical_depth_std` | 1 | time,gain | - | Standard deviation of cloud optical depth |
| `effective_radius` | um | time,gain | - | Effective radius |
| `effective_radius_std` | um | time,gain | - | Standard deviation of effective radius |
| `gain` | 1 | gain | - | Coordinate variable for gain |
| `liquid_water_path` | g/m2 | time,gain | - | Liquid Water Path |
| `liquid_water_path_std` | g/m2 | time,gain | - | Standard deviation of liquid water path |
| `modis_channel` | 1 | modis_channel | - | Coordinate variable for modis_channel |
| `modis_wavelength` | nm | modis_channel | - | Central wavelength of modis_channel |
| `number_of_solutions` | count | time,gain | - | Number of Solutions |
| `radiance_0440` | 1 | time,gain | - | Normalized zenith radiance at 440nm |
| `radiance_0870` | 1 | time,gain | - | Normalized zenith radiance at 870nm |
| `radiance_1640` | 1 | time,gain | - | Normalized zenith radiance at 1640nm |
| `retrieval_flag` | 1 | time,gain | - | Quality check results |
| `solar_zenith_angle` | degree | time | - | Solar zenith angle |
| `spectral_irradiance_at_toa` | W m-2 um-1 | channel | - | Spectral Irradiance at TOA |
| `time` | - | time | - | Time offset from midnight |
| `wavelength` | um | channel | - | Effective Wavelength |


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
                     params={"user": f"{user}:{token}", "ds": "sgpsphotcod2chiuC1.c1",
                             "start": "2019-12-27", "end": "2019-12-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpsphotcod2chiuC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpsphotcod2chiuC1.c1", "2019-12-27", "2019-12-27")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpsphotcod2chiuC1.c1", "2019-12-27", "2019-12-27"))   # cite what you pulled
```

## Quality control in this product

1 `qc_` companion variables cover 1 of the
23 data variables. Assessments present in the example file: `Acceptable`, `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_modis_white_sky_albedo"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("modis_white_sky_albedo", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["modis_white_sky_albedo"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpsphotcod2chiuC1.c1", "20140101", "20260924")
```

The report's own note on quality: Retrieval quality is captured via output variables number_of_solutions (count of viable solutions used) and retrieval_flag (quality check results), plus ancillary quality variable aqc_modis_white_sky_albedo for the MODIS albedo input and MODIS BRDF_Albedo_Band_Quality/Mandatory_Quality bands per band. Reported cloud_optical_depth_std, liquid_water_path_std, and effective_radius_std give the standard deviation from the 40-repetition perturbation ensemble as instantaneous retrieval uncertainty. Validation (Sookdar et al. 2025) reports correlation and bias statistics against MFRSR, MICROBASE,...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Cloud mode scheduling limited by solar zenith angle, instrument model, and overall... | Gaps or reduced frequency of cloud-mode retrievals depending on time of day/year and instrument model | None stated beyond noting availability depends on conditions; newer models improve availability to five-minute updates | (hb p. 7) |
| Intentional deactivation of cloud mode during winter and early spring in earlier... | Earlier VAP data (prior to 2017) only available from early March to October, with data gaps in winter/early spring | None stated; user should expect data availability limited to March-October for pre-2017 records | (hb p. 9) |
| Reduced usefulness of third (1640 nm) channel for effective radius retrievals | Retrieval sensitivity of zenith radiance to larger droplet sizes diminishes; re retrievals may be less reliable, especially for larger droplets | Chiu et al. (2012) implemented multi-step perturbation approach (5-10% uncertainty, 40 repetitions, LUT comparison) to assess and average out this... | (hb p. 7) |
| High (relative) bias in photometer tau retrievals compared to shadowband radiometer... | Correlation of ~0.81 between photometer tau and MFRSR tau, with photometer values biased high relative to MFRSR | None stated beyond noting the bias; consult Sookdar et al. (2025) for further detail | (hb p. 10) |
| Retrieval variability larger than perturbation-based uncertainty estimates | Intercomparison variability between ARM retrievals can be as high as a factor of three larger than errors reported from individual retrieval input perturbation tests | None stated; consult Sookdar et al. (2025) for error characterization | (hb p. 10) |
| Poor performance of effective radius retrievals against MICROBASE reference | Low correlations (less than 0.1) and standard deviation ~3 mm (as printed) when compared to ARM baseline multi-sensor radar/radiometer (MICROBASE) re references | None stated | (hb p. 10) |
| LWP bias in drizzling conditions | LWP calculations remain relatively unbiased only in non-drizzling conditions; in drizzling conditions bias/error behavior not characterized as good | Restrict comparisons/interpretation to non-drizzling conditions; consult Sookdar et al. (2025) | (hb p. 10) |
| Dependence on MODIS surface albedo product accuracy | Retrieval quality tied to accuracy/availability of MODIS MCD43A2/MCD43A3 albedo product (500-m, 16-day composite); quality flags provided via BRDF_Albedo_Band_Quality and... | Ancillary quality check variable (aqc_modis_white_sky_albedo) and MODIS QC bands provided for filtering | (hb p. 12) |
| Input measurement/albedo uncertainty propagation | 5-10% assumed uncertainty in zenith radiance and surface albedo inputs propagates into retrieved tau/re uncertainty (reported as standard error/instantaneous retrieval uncertainty) | Perturbation approach (40 repetitions) used to estimate and report uncertainty alongside retrieved values | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Chiu et al. 2006, J. Geophys. Res. Atmos. 111(D16): D16201
- Chiu et al. 2010, J. Geophys. Res. Atmos. 115(D14): D14202
- Chiu et al. 2012, Atmos. Chem. Phys. 12(21): 10313-10329
- Chiu, Gregory, Wagener 2016, DOE/SC-ARM-15-029
- Fairless et al. 2020, AGU Fall Meeting abstract #A174-0000
- Holben et al. 1998, Remote Sensing of Environment 66(1): 1-16
- Mather and Voyles 2013, BAMS 94(3): 377-392
- Schaaf et al. 2002, Remote Sensing of Environment 83(1-2): 135-148
- Sookdar et al. 2025, EGUsphere, https://doi.org/10.5194/egusphere-2025-694
- Stamnes et al. 1988, Applied Optics 27(12): 2502-2509

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-317.pdf (16 pages, DOE/SC-ARM-TR-317, by LL Ma, SE Giangrande, JD Rausch, D Wang, C Chiu)
- Catalog record: ARM data-source index, `instrument_class_code=sphotcod`, read 2026-09-24
- Example file: `sgpsphotcod2chiuC1.c1.20191227.143730.nc` from `sgpsphotcod2chiuC1.c1`, 0.03 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
