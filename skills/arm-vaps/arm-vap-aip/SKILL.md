---
name: arm-vap-aip
description: ARM Aerosol Intensive Properties (aip) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Absorption coefficient, Total scattering coefficient, Aerosol single scattering albedo, Hemispheric backscatter fraction, Average upscatter fraction), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpaipavg1ogrenC1.c1) and the variable inventory of a real file. Use when working with aip data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - aip, Aerosol Intensive Properties, sgpaipavg1ogrenC1.c1, Absorption coefficient, Total scattering coefficient, Aerosol single scattering albedo, Hemispheric backscatter fraction, Aerosols.
---

# AIP - Aerosol Intensive Properties

Value-added product that computes aerosol intensive optical properties (single-scattering albedo, backscatter fraction, asymmetry parameter, Angstrom exponent, submicron scattering/absorption fractions, forcing efficiency) from calibrated, quality-controlled AOS nephelometer scattering/backscattering and PSAP absorption coefficient data, produced as 1-minute and hourly-averaged netCDF files at ARM sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 31 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `aip` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-201 / A Koontz, C Flynn / September 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-201.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1996-07-02 to 2017-03-30 (retired) |
| Datastreams with data | 60 across 10 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/aip |


## Credit

Everything this skill knows about the retrieval is the work of **A Koontz, C Flynn** -
the ARM developers and mentors who wrote the technical report it derives from:

> A Koontz, C Flynn. *AIP1OGREN: Aerosol Observing Station Intensive Properties Value-Added Product*, DOE/SC-ARM-TR-201, September 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-201.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The aip1ogren VAP computes several aerosol intensive properties as ratios of measured extensive properties (scattering and absorption coefficients) obtained from the Aerosol Observing Station (AOS), which measures absorption via a filter-based particle soot absorption photometer (PSAP) and total/backscattering via nephelometer at red, green and blue wavelengths and at 1 um and 10 um particle size cuts. Single-scattering albedo is computed as sigma_sp/(sigma_sp+sigma_ap); hemispheric backscatter fraction b as sigma_bsp/sigma_sp; average upscatter fraction and asymmetry parameter g are empirical parameterizations of b; the Angstrom exponent is computed from the log-ratio of scattering (or absorption) coefficients at two wavelengths divided by the log-ratio of the wavelengths. Submicron scattering and absorption fractions are computed as the ratio of the 1 um to 10 um size-cut coefficients, and aerosol forcing efficiency is computed from a parameterized radiative transfer expression (Sheridan and Ogren, 1999) using ozone/atmosphere constants and the derived single-scattering albedo and backscatter fraction. Because the AOS alternates between 1 um and 10 um size cuts at intervals, submicron fraction and size-cut dependent products are constrained to the hourly-averaged output file.

**Cadence.** output every 1-minute (sssaip1ogrenFn.c1) and hourly (sssaipavg1ogrenFn.c1); averaging Hourly file is not a simple average of the 1-minute file; it contains additional intensive properties depending on/relating to the size cut which alternates through a typical 1-hour interval (hb p. 10).

## Inputs

The report names these instruments and sibling products: Aerosol Observing Station (AOS), nephelometer (Neph3W), particle soot absorption photometer (PSAP1W, PSAP3W).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Absorption coefficient | 1/Mm | - | - | (hb p. 8) |
| Total scattering coefficient | 1/Mm | 450, 550, 700 nm; RH less than ... | - | (hb p. 8) |
| Hemispheric backscattering coefficient | 1/Mm | 450, 550, 700 nm; RH less than ... | - | (hb p. 8) |
| Aerosol single scattering albedo | unitless | - | - | (hb p. 9) |
| Hemispheric backscatter fraction | unitless | - | - | (hb p. 9) |
| Average upscatter fraction | unitless | - | - | (hb p. 9) |
| Asymmetry parameter | unitless | - | - | (hb p. 9) |
| Angstrom exponent | unitless | - | - | (hb p. 9) |
| Submicron scattering fraction | unitless | - | - | (hb p. 9) |
| Submicron absorption fraction | unitless | - | - | (hb p. 9) |
| Aerosol forcing efficiency | unitless (Wm-2 per unit... | - | - | (hb p. 9) |
| TSI Low RH Nephelometer relative humidity | % | - | - | (hb p. 13) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Absorption coefficient input wavelength | 545 nm (PSAP) | (hb p. 8) |
| Total scattering coefficient input wavelengths / RH | 450, 550, 700 nm, RH less than  40% | (hb p. 8) |
| Hemispheric backscattering coefficient input wavelengths /... | 450, 550, 700 nm, RH less than  40% | (hb p. 8) |
| Single scattering albedo equation | omega_o = sigma_sp/(sigma_sp+sigma_ap); computed for PSAP1W and PSAP3W depending on data availability | (hb p. 8) |
| Hemispheric backscatter fraction equation | b = sigma_bsp/sigma_sp | (hb p. 8) |
| Average upscatter fraction equation | b_bar = 0.0817 + 1.8495b - 2.9682b^2 | (hb p. 8) |
| Asymmetry parameter equation | g = 1.011 - 1.036b - 2.005b^2 | (hb p. 8) |
| Angstrom exponent equation | a = -log[sigma_sp(lambda1)/sigma_sp(lambda2)]/log[lambda1/lambda2]; computed for PSAP3W (absorption), Neph3W (backscatter and total scatter) when... | (hb p. 8) |
| Submicron scattering fraction equation | Rsp = sigma_sp(1 um)/sigma_sp(10 um) | (hb p. 8) |
| Submicron absorption fraction equation | Rap = sigma_ap(1 um)/sigma_ap(10 um) | (hb p. 8) |
| Aerosol forcing efficiency equation and constants | dF/delta = -D*So*Tat^2*(1-Ac)*omega_o*b*[(1-Rs)^2 - (2Rs/b)((1/omega_o)-1)]; D=0.5 (fractional day length), So=1370 Wm-2 (solar constant), Tat=0.76... | (hb p. 9) |
| AOS size cuts | 1 um and 10 um particle size cuts, measured at alternating intervals | (hb p. 6) |
| Size cut interval (varies by site/period) | 6 minutes or 30 minutes depending on site and time period (Table 3) | (hb p. 10) |
| 1-minute file averaging | 1-minute averaging for extensive/intensive properties | (hb p. 6) |
| Hourly file averaging | Hourly averaged file produced from 1-minute files; includes submicron scattering and absorption fractions | (hb p. 6) |


## The data

Verified example: **`sgpaipavg1ogrenC1.c1`**, file `sgpaipavg1ogrenC1.c1.20170327.000000.cdf`
(0.12 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=24 |
| Data variables | 147 |
| QC variables | 71 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2017-03-27T00:00:00 to 2017-03-27T23:00:00 |
| dod version | aipavg1ogren-c1-1.1 |
| process version | vap-aip1ogren-4.3-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Ba_B_Dry_10um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, blue wavelength, 3 wavelength PSAP, low RH,... |
| `Ba_B_Dry_1um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, blue wavelength, 3 wavelength PSAP, low RH, 1... |
| `Ba_G_Dry_10um_PSAP1W_1` | 1/Mm | time | yes | Absorption coefficient, green wavelength, low RH, 10 um size cut |
| `Ba_G_Dry_10um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, green wavelength, 3 wavelength PSAP, low RH,... |
| `Ba_G_Dry_1um_PSAP1W_1` | 1/Mm | time | yes | Absorption coefficient, green wavelength, low RH, 1 um size cut |
| `Ba_G_Dry_1um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, green wavelength, 3 wavelength PSAP, low RH,... |
| `Ba_R_Dry_10um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, red wavelength, 3 wavelength PSAP, low RH, 10... |
| `Ba_R_Dry_1um_PSAP3W_1` | 1/Mm | time | yes | Absorption coefficient, red wavelength, 3 wavelength PSAP, low RH, 1... |
| `Ba_angstrom_exponent_BG_Dry_10um` | unitless | time | yes | Angstrom exponent computed from blue/green ratio, 10 um size cut,... |
| `Ba_angstrom_exponent_BG_Dry_1um` | unitless | time | yes | Angstrom exponent computed from blue/green ratio, 1 um size cut,... |
| `Ba_angstrom_exponent_BR_Dry_10um` | unitless | time | yes | Angstrom exponent computed from blue/red ratio, 10 um size cut,... |
| `Ba_angstrom_exponent_BR_Dry_1um` | unitless | time | yes | Angstrom exponent computed from blue/red ratio, 1 um size cut, PSAP3W... |
| `Ba_angstrom_exponent_GR_Dry_10um` | unitless | time | yes | Angstrom exponent computed from green/red ratio, 10 um size cut,... |
| `Ba_angstrom_exponent_GR_Dry_1um` | unitless | time | yes | Angstrom exponent computed from green/red ratio, 1 um size cut,... |
| `Bbs_B_Dry_10um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, blue wavelength, low RH, 10 um size cut |
| `Bbs_B_Dry_1um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, blue wavelength, low RH, 1 um size cut |
| `Bbs_G_Dry_10um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, green wavelength, low RH, 10 um size cut |
| `Bbs_G_Dry_1um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, green wavelength, low RH, 1 um size cut |
| `Bbs_R_Dry_10um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, red wavelength, low RH, 10 um size cut |
| `Bbs_R_Dry_1um_Neph3W_1` | 1/Mm | time | yes | Back-scattering coefficient, red wavelength, low RH, 1 um size cut |
| `Bbs_angstrom_exponent_BG_Dry_10um` | unitless | time | yes | Angstrom exponent computed from blue/green ratio, 10 um size cut,... |
| `Bbs_angstrom_exponent_BG_Dry_1um` | unitless | time | yes | Angstrom exponent computed from blue/green ratio, 1 um size cut,... |
| `Bbs_angstrom_exponent_BR_Dry_10um` | unitless | time | yes | Angstrom exponent computed from blue/red ratio, 10 um size cut,... |
| `Bbs_angstrom_exponent_BR_Dry_1um` | unitless | time | yes | Angstrom exponent computed from blue/red ratio, 1 um size cut, Neph3W... |
| `Bbs_angstrom_exponent_GR_Dry_10um` | unitless | time | yes | Angstrom exponent computed from green/red ratio, 10 um size cut,... |
| `Bbs_angstrom_exponent_GR_Dry_1um` | unitless | time | yes | Angstrom exponent computed from green/red ratio, 1 um size cut,... |
| `Bs_B_Dry_10um_Neph3W_1` | 1/Mm | time | yes | Total scattering coefficient, blue wavelength, low RH, 10 um size cut |
| `Bs_B_Dry_1um_Neph3W_1` | 1/Mm | time | yes | Total scattering coefficient, blue wavelength, low RH, 1 um size cut |
| `Bs_G_Dry_10um_Neph3W_1` | 1/Mm | time | yes | Total scattering coefficient, green wavelength, low RH, 10 um size cut |
| `Bs_G_Dry_1um_Neph3W_1` | 1/Mm | time | yes | Total scattering coefficient, green wavelength, low RH, 1 um size cut |


_42 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpaipavg1ogrenC1.c1",
                             "start": "2017-03-27", "end": "2017-03-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaipavg1ogrenC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaipavg1ogrenC1.c1", "2017-03-27", "2017-03-27")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaipavg1ogrenC1.c1", "2017-03-27", "2017-03-27"))   # cite what you pulled
```

This product carries 147 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpaipavg1ogrenC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['Ba_B_Dry_10um_PSAP3W_1', 'Ba_B_Dry_1um_PSAP3W_1', 'Ba_G_Dry_10um_PSAP1W_1', 'qc_Ba_B_Dry_10um_PSAP3W_1', 'qc_Ba_B_Dry_1um_PSAP3W_1', 'qc_Ba_G_Dry_10um_PSAP1W_1'],
                                cleanup_qc=True)
```

## Quality control in this product

71 `qc_` companion variables cover 71 of the
147 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_Ba_G_Dry_1um_PSAP1W_1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("Ba_G_Dry_1um_PSAP1W_1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["Ba_G_Dry_1um_PSAP1W_1", "Ba_G_Dry_10um_PSAP1W_1", "Ba_R_Dry_10um_PSAP3W_1"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaipavg1ogrenC1.c1.20170327.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ba_angstrom_exponent_BG_Dry_10um` | Data value for Ba_B_Dry_10um_PSAP3W_1 is not available in input... | 24 | 100.0 |
| `ssa_B_Dry_1um` | Data value for Ba_B_Dry_1um_PSAP3W_1 is not available in input... | 24 | 100.0 |
| `submicron_fraction_absorption_R` | Data value cannot be computed, data value set to missing_value... | 24 | 100.0 |
| `Ba_angstrom_exponent_GR_Dry_1um` | Data value for Ba_R_Dry_1um_PSAP3W_1 is not available in input... | 24 | 100.0 |
| `Ba_angstrom_exponent_GR_Dry_1um` | Data value for Ba_G_Dry_1um_PSAP3W_1 is not available in input... | 24 | 100.0 |
| `Ba_angstrom_exponent_BR_Dry_1um` | Data value for Ba_R_Dry_1um_PSAP3W_1 is not available in input... | 24 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpaipavg1ogrenC1.c1", "19960702", "20260924")
```

The report's own note on quality: Explicit QC flags (qc_ fields) are included for every reported field in both the 1-minute and hourly datastreams. Input AOS data have undergone extensive QC at NOAA prior to use in the VAP, and specific QC tests are reported for each aerosol property (both extensive and intensive). The Data Quality Office does not independently conduct data quality assessment of VAPs.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Low signal-to-noise ratio under clean/low aerosol burden conditions | Ratios of measured extensive properties (used to compute intensive properties) become noisy; flagged conditions appear as questionable/bad QC values during low-aerosol periods | Conditions are flagged; user is advised to treat such data with caution | (hb p. 10) |
| PSAP filter loading bias on absorption and single-scattering albedo | As the PSAP filter becomes more heavily loaded with aerosol, filter transmittance and measurement sensitivity decrease, biasing absorption coefficient and derived single-scattering albedo... | These conditions are flagged as questionable | (hb p. 10) |
| Submicron fraction errors from interleaved size-cut sampling under rapidly changing... | Submicron scattering/absorption fraction ratios computed from interleaved (alternating 1um/10um) samples can show spurious variability or spikes during rapidly changing aerosol conditions;... | Constrained to hourly-averaged product; reduced to some extent by hourly averaging, but user should be particularly attentive when using these... | (hb p. 10) |
| Parameterized (not strictly derived) quantities | Average upscatter fraction, asymmetry parameter, and forcing efficiency are computed via empirical parameterizations rather than direct derivations, so may show systematic offsets/errors... | None specified beyond noting possible systematic errors | (hb p. 10) |
| Difficulty distinguishing transient atmospheric spikes from spurious noise | Under low-aerosol conditions it can be hard to tell whether a spike in the ratio-based intensive properties is a real transient event or instrument noise | User advised to treat such data with caution | (hb p. 25) |
| Input data dependency on AOS/NOAA quality control and delivery schedule | VAP output generation is gated on receipt of quarterly quality-checked AOS data batches from NOAA/CMDL; delays in AOS QC data propagate to aip1ogren availability | VAP runs periodically after receipt of new sgpcmdlaos/AOS data | (hb p. 28) |
| Alternating size-cut measurement limits temporal resolution of size-dependent products | Submicron scattering/absorption fractions and other size-cut-dependent quantities are unavailable at 1-minute resolution because the AOS alternates between 1 um and 10 um cuts over 6- or... | These products are only reported in the hourly-averaged (aipavg) datastream | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Delene, DJ, and JA Ogren. 2002. "Variability of Aerosol Optical Properties at Four North American Surface Monitoring Sites." Journal of the Atmospheric Sciences 59: 1135-1150, doi:10.1175/1520-0469(2002)059less than...
- Sheridan, PJ, and JA Ogren. 1999. "Observations of the vertical and regional variability of aerosol optical properties over central and eastern North America." Journal of Geophysical Research – Atmospheres 104(D14):...
- Sheridan, PJ, DJ Delene, and JA Ogren. 2001. "Four years of continuous surface aerosol measurements from the Department of Energy's Atmospheric Radiation Measurement Program Southern Great Plains Cloud and Radiation...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-201.pdf (31 pages, DOE/SC-ARM-TR-201, by A Koontz, C Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=aip`, read 2026-09-24
- Example file: `sgpaipavg1ogrenC1.c1.20170327.000000.cdf` from `sgpaipavg1ogrenC1.c1`, 0.12 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
