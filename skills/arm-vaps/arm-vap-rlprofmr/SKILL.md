---
name: arm-vap-rlprofmr
description: ARM Raman Lidar Mixing Ratio (rlprofmr) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Water vapor mixing ratio, Temperature, RR signal ratio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgp10rlprofmr1turnC1.c1) and the variable inventory of a real file. Use when working with rlprofmr data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols; Atmospheric Profiling. Triggers - rlprofmr, Raman Lidar Mixing Ratio, sgp10rlprofmr1turnC1.c1, Water vapor mixing ratio, Temperature, RR signal ratio, Aerosols, Atmospheric Profiling.
---

# RLPROFMR - Raman Lidar Mixing Ratio

This VAP derives profiles of water vapor mixing ratio (WVMR) and temperature from ARM Raman lidar photon-counting measurements of H2O, N2, and rotational Raman channels, calibrated against collocated radiosonde soundings, and produced from three deployed ARM Raman lidars (SGP, ENA, AMF3/Oliktok Point).

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 39 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `rlprofmr` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-218 / R Newsom, C Sivaraman / November 2018](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf) |
| Category | Aerosols; Atmospheric Profiling |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-03-01 to 2026-05-05 (retired) |
| Datastreams with data | 11 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/rlprofmr |


## Credit

Everything this skill knows about the retrieval is the work of **R Newsom, C Sivaraman** -
the ARM developers and mentors who wrote the technical report it derives from:

> R Newsom, C Sivaraman. *Raman Lidar Water Vapor Mixing Ratio and Temperature Value-Added Products*, DOE/SC-ARM-TR-218, November 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

Water vapor mixing ratio is retrieved from the ratio of Raman-shifted backscatter photon counts from atmospheric H2O (407.5 nm) to N2 (386.7 nm), which is proportional to the number density ratio of H2O to N2 after accounting for molecular transmission (computed from radiosonde temperature/pressure via Rayleigh scattering theory) while aerosol transmission effects are neglected; the uncalibrated ratio is scaled by an empirically-determined, time-dependent calibration profile derived from collocated radiosonde comparisons. Temperature is retrieved from the ratio Q of two pure rotational Raman (RR) channel signals (RR1/RR2), which depends nonlinearly on temperature via calibration coefficients a and b and a height-dependent overlap function, following T = (300 K b)/(ln(Q/O(z)) - a); calibration coefficients are obtained by linear regression against radiosonde temperature above the full-overlap height (4 km), and the overlap function is derived from residuals below that height. A separate CAL VAP computes 30-minute-averaged profiles of uncalibrated WVMR and the RR signal ratio at radiosonde launch times from the MERGE VAP (raw photon-count data), providing the inputs MR and TEMP use for their independent calibration procedures. Uncertainties in both WVMR and temperature are propagated from Poisson (shot-noise) statistics of the photon counts through the retrieval equations.

**Cadence.** input rate Raw RL data: 10s pulse accumulation time, 7.5m range resolution (rl.a0 / MERGE datastream); output every MR and TEMP typically run with finer temporal resolution (10 min or less); CAL uses 30-minute averages centered on radiosonde launch times; averaging CAL: 30-minute average centered on radiosonde launch time with 60-m range bin; MR/TEMP process one 24-hour period at a time (hb p. 20).

## Inputs

The report names these instruments and sibling products: Raman Lidar MERGE VAP (rlprofmerge2news.c0), Raman Lidar raw datastream (rl.a0), radiosonde (sondewnpn.b1), Raman Lidar Aerosol/Backscatter/Extinction/Depolarization products.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Water vapor mixing ratio (merged WFOV/NFOV) | g kg-1 | - | propagated shot-noise uncertainty... | (hb p. 22) |
| WFOV calibrated water vapor mixing ratio (mr_lo) | g kg-1 | - | mr_lo_err | (hb p. 23) |
| NFOV calibrated water vapor mixing ratio (mr_hi) | g kg-1 | - | mr_hi_err | (hb p. 23) |
| Temperature | K | - | temperature_error; recommended QC threshold... | (hb p. 24) |
| RR signal ratio (RR1/RR2) | unitless | - | rot_raman_ratio_error | (hb p. 24) |
| One-way molecular transmission due to N2 | unitless | - | - | (hb p. 23) |
| One-way molecular transmission due to H2O | unitless | - | - | (hb p. 23) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Laser | Continuum model 9030, frequency-Tripled Nd:YAG | (hb p. 8) |
| Transmit wavelength | 354.7 nm | (hb p. 8) |
| Pulse energy | ~300 mJ | (hb p. 8) |
| Pulse width | ~5 ns | (hb p. 8) |
| Pulse repetition frequency | 30 Hz | (hb p. 8) |
| Telescope diameter | 61 cm | (hb p. 8) |
| WFOV | 2 mrad | (hb p. 8) |
| NFOV | 0.3 mrad | (hb p. 8) |
| PMTs | Electron Tube 9954B | (hb p. 8) |
| Data acquisition | Licel transient data recorders | (hb p. 8) |
| Pulse accumulation time | 10s | (hb p. 8) |
| Range resolution | 7.5m | (hb p. 8) |
| WFOV & NFOV H2O filter center wavelength / FWHM | 407.5 nm / 0.27 nm | (hb p. 8) |
| WFOV & NFOV N2 filter center wavelength / FWHM | 386.7 nm / 0.31 nm | (hb p. 8) |
| NFOV RR1 filter center wavelength / FWHM | 354.27 nm / 0.22 nm | (hb p. 8) |
| NFOV RR2 filter center wavelength / FWHM | 353.27 nm / 0.21 nm | (hb p. 8) |
| WFOV overlap complete altitude | 800 m | (hb p. 10) |
| NFOV overlap complete altitude | 4 km | (hb p. 10) |
| MR processing interval | one 24-hour period at a time | (hb p. 10) |
| CAL averaging window | 30-minute time period centered on radiosonde launch time, 60-m range bin | (hb p. 20) |
| MR NFOV calibration height range (z_min, z_max) | (0.5 km, 4.0 km) | (hb p. 13) |
| MR WFOV calibration height range (z_min, z_max) | (0.3 km, 2.0 km) | (hb p. 13) |
| MR calibration relative error rejection threshold | 0.25 (25%) | (hb p. 13) |
| MR scale-factor QC threshold on mean percent difference | Delta(t_s) less than = 0.2 | (hb p. 13) |
| FOV merge height range (typical) | z_WFOV=0 km, z_NFOV=1.2 km | (hb p. 14) |
| TEMP calibration coefficient fit height range | 4 km to 10 km (full overlap to upper limit) | (hb p. 16) |


_9 further rows in the report._

## The data

Verified example: **`sgp10rlprofmr1turnC1.c1`**, file `sgp10rlprofmr1turnC1.c1.20040103.000000.cdf`
(0.88 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=144, `height_low`=25, `height_high`=102, `height`=104 |
| Data variables | 38 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2004-01-03T00:00:00 to 2004-01-03T23:50:00 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `average_energy` | mJ | time | - | Average laser energy of the ensemble shots |
| `calib_factor` | unitless | time | - | Calibration factor for entire profile |
| `calib_high_low` | unitless | time | - | Calibration factor used to match the high channel mixing ratio to the... |
| `cloud_base_height_other` | km AGL | time | - | Cloud base height |
| `diff_trans_aerosol_corr` | unitless | time,height_high | - | Differential transmission correction for aerosols |
| `height` | km AGL | height | - | Height range of the merged water vapor mixing ratio profile |
| `height_high` | km AGL | height_high | - | Height range of the high channel water vapor mixing ratio profile |
| `height_low` | km AGL | height_low | - | Height range of the low channel water vapor mixing ratio profile |
| `liq_mwr` | cm | time | - | Cloud liquid water vapor by the microwave radiometer |
| `mixing_ratio_1` | g/kg | time,height_high | - | Water vapor mixing ratio profile created by merging the two channels |
| `mixing_ratio_1_error` | g/kg | time,height_high | - | Uncertainty of the water vapor mixing ratio profile created by... |
| `mixing_ratio_2` | g/kg | time,height_high | - | Water vapor mixing ratio profile created by merging the two... |
| `mixing_ratio_2_error` | g/kg | time,height_high | - | Uncertainty of the water vapor mixing ratio profile created by... |
| `mixing_ratio_3` | g/kg | time,height | - | Water vapor mixing ratio profile created by merging the two... |
| `mixing_ratio_3_error` | g/kg | time,height | - | Uncertainty of the water vapor mixing ratio profile created by... |
| `mixing_ratio_error_high` | g/kg | time,height_high | - | Uncertainty of the water vapor mixing ratio profile from the high... |
| `mixing_ratio_error_low` | g/kg | time,height_low | - | Uncertainty of the water vapor mixing ratio profile from the low... |
| `mixing_ratio_high` | g/kg | time,height_high | - | Water vapor mixing ratio profile from the high channel |
| `mixing_ratio_low` | g/kg | time,height_low | - | Water vapor mixing ratio profile from the low channel |
| `mixing_ratio_other` | g/kg | time,height | - | Water vapor mixing ratio |
| `mode` | unitless | time | - | Mode of the dataset (as defined by the filter arrangement of the... |
| `pressure` | mb | time,height | - | Pressure |
| `pwv_mwr` | cm | time | - | Precipitable water vapor observed by the microwave radiometer |
| `pwv_rl` | cm | time | - | Precipitable water vapor observed by the Raman lidar |
| `pwv_rl_err` | cm | time | - | Random error in the precipitable water vapor observed by the Raman... |
| `pwv_rl_fraction` | unitless | time | - | Fraction of the total column amount of water vapor the Raman lidar... |
| `relative_humidity` | % | time,height | - | Relative humidity calculated from the merged water vapor mixing ratio... |
| `relative_humidity_over_ice` | % | time,height | - | Relative humidity over ice calculated from the merged water vapor... |
| `sample_times_other` | unitless | time | - | Flag indicating whether or not there was a sample from the... |
| `shots_summed` | counts | time | - | Number of laser shots in the ensemble |


_6 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgp10rlprofmr1turnC1.c1",
                             "start": "2004-01-03", "end": "2004-01-03", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgp10rlprofmr1turnC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgp10rlprofmr1turnC1.c1", "2004-01-03", "2004-01-03")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgp10rlprofmr1turnC1.c1", "2004-01-03", "2004-01-03"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("liq_mwr")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

1 `qc_` companion variables cover 0 of the
38 data variables. Assessments present in the example file: .

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# This file carries one QC variable, `qc_flag`, not a per-variable `qc_<name>`
# companion - so the qcfilter methods that key off that naming have nothing to
# match. Read it directly and work out the encoding from its own attributes.
print(ds["qc_flag"].attrs)
print(ds["qc_flag"].to_series().value_counts().head())
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgp10rlprofmr1turnC1.c1", "19980301", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: MR and TEMP algorithms perform no quality control on the final output; it is the end user's responsibility to perform QC using provided uncertainty estimates. Recommended QC: reject WVMR samples where mr_merged_err/mr_merged greater than  0.25 (25%); reject temperature samples where temperature_err/temperature greater than  0.05 (5%). These thresholds are user-adjustable ('relative_uncertainty_threshold') based on need. Example day (21 Aug 2017, SGP) shows QC removes noisiest data, reducing valid WVMR height from ~8km at night to ~4km in daytime.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Incomplete overlap between outgoing laser beam and receiver field of view | Signal roll-off and biased/noisy retrievals below the overlap-complete altitude: WFOV below 800 m, NFOV below 4 km; overlap function departs from unity at low altitude | Use an overlap function/correction; NFOV temperature calibration coefficients determined only above 4 km where overlap is assumed unity, with overlap... | (hb p. 10) |
| Overlap function temporal drift due to beam alignment changes | Overlap function and calibration coefficients show diurnal/temporal variability in plots (Figure 8); WFOV overlap generally more stable than NFOV | Independent overlap function and calibration coefficient estimates computed at each radiosonde launch time within a 24-hour period and interpolated... | (hb p. 4) |
| Daytime solar contamination increasing measurement noise | WVMR uncertainty increases significantly during daytime; maximum valid-measurement height drops from ~8km at night to ~4km during day (Figure 10); WFOV H2O channel most solar-sensitive, RR... | None specific beyond uncertainty-based QC filtering | (hb p. 4) |
| Neglect of aerosol transmission in WVMR retrieval | Under very hazy conditions (AOD=1) aerosol transmission ratio can bias WVMR by up to ~5% from surface to 7km AGL; under typical AOD=0.2 conditions bias is ~1% | Aerosol transmission effects are ignored in the MR algorithm because retrieved aerosol extinction (via Ansmann et al. 1990 technique on N2 channel)... | (hb p. 10) |
| No quality control performed by the algorithms themselves | Output datastreams contain a mix of good- and poor-quality measurements without flags | End user must filter using relative uncertainty thresholds: mr_merged_err/mr_merged greater than  0.25 rejected for WVMR; temperature_err/temperature... | (hb p. 22) |
| TEMP calibration fit failure/rejection | Samples outside height range (4-10km) or with relative RR-ratio uncertainty delta_ygreater than 0.1 shown as light gray (excluded) points in regression plots; fit deemed invalid if... | Reject bad samples from regression; require RMSless than 0.1 and correlationgreater than 0.7 for valid coefficient estimates | (hb p. 17) |
| MR calibration scale factor rejection | Scale factor alpha(t_s) excluded from interpolation if mean percent difference Delta(t_s) greater than  0.2 relative to sonde | Interpolate scale factor to RL time grid using only alpha(t_s) values with Delta(t_s)less than =0.2 | (hb p. 13) |
| Missing baseline calibration profile for run date | MR VAP will not run/produce output for that date | Ensure configuration file contains a baseline calibration profile covering the specified run date | (hb p. 21) |
| Reliance on radiosonde availability and quality for calibration | Calibration coefficients, scale factors, and overlap functions are only updated at radiosonde launch times (2-4 times/day); gaps or bad soundings limit calibration accuracy between launches | CAL run several days/weeks/months ahead of MR/TEMP to allow offline analysis; independent calibration per radiosonde launch interpolated to RL grid | (hb p. 20) |
| Algorithms run independently of each other with sequencing dependency | MR and TEMP calibration will be degraded or fail if CAL has not been run sufficiently ahead of time | CAL must run at least a couple of days ahead of MR and TEMP | (hb p. 7) |
| No WFOV rotational Raman channels for temperature | TEMP output contains only NFOV temperature data; no FOV merging step for TEMP | None - stated as a design limitation | (hb p. 23) |
| Hand-drawn baseline calibration profile introduces subjectivity | Baseline calibration profile (red curve in Figure 9) obtained by hand-drawing a smooth curve through median sonde/uncalibrated-ratio values rather than an automated fit | None stated beyond using median profiles over 2-6 month periods | (hb p. 21) |
| Uncertainty estimates exclude calibration-profile and transmission-term uncertainty | Reported WVMR uncertainty (mr_merged_err) reflects only shot-noise propagation, not full calibration/transmission error budget, potentially underestimating true uncertainty | None stated | (hb p. 11) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Albert A, M Riebesell, and C Weitkamp. 1990. Measurement of atmospheric aerosol extinction profiles with a Raman lidar. Optics Letters 15(13): 746-748
- Behrendt, A, and J Reichardt. 2000. Atmospheric temperature profiling in the presence of clouds with a pure rotational Raman lidar. Applied Optics 39(9): 1372-1378
- Bucholtz A. 1995. Rayleigh-scattering calculations for the terrestrial atmosphere. Applied Optics 34(15): 2765-2773
- Goldsmith JEM, FH Blair, SE Bisson, and DD Turner. 1998. Turn-key Raman lidar for profiling atmospheric water vapor, clouds and aerosols. Applied Optics 37(21): 4979-4990
- Newsom RK, J Goldsmith, and C Sivaraman. 2017. Raman Lidar MERGE Value-Added Product. DOE/SC-ARM-TR-189
- Newsom, RK, DD Turner, and JEM Goldsmith. 2013. Long-term evaluation of temperature profiles measured by an operational Raman lidar. JTECH 30(8): 1616-1634
- Turner DD, RA Ferrare, LA Heilman Brasseur, WF Feltz, and TP Tooman. 2002. Automated retrievals of water vapor and aerosol profiles from an operational Raman lidar. JTECH 19(1): 37-49
- Turner, DD, JEM Goldsmith, and RA Ferrare. 2016. Development and applications of the ARM Raman lidar.
- Whiteman, DN, SH Melfi, and RA Ferrare. 1992. Raman lidar system for the measurement of water vapor and aerosols in the Earth's atmosphere. Applied Optics 31(16): 3068-3082

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-218.pdf (39 pages, DOE/SC-ARM-TR-218, by R Newsom, C Sivaraman)
- Catalog record: ARM data-source index, `instrument_class_code=rlprofmr`, read 2026-09-24
- Example file: `sgp10rlprofmr1turnC1.c1.20040103.000000.cdf` from `sgp10rlprofmr1turnC1.c1`, 0.88 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
