---
name: arm-vap-mwrretv2
description: ARM MWR Retrievals with MWRRET Version 2 (mwrretv2) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Liquid Water Path, Precipitable Water Vapor), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmwrret2turnC1.c1) and the variable inventory of a real file. Use when working with mwrretv2 data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Derived Quantities and Models; Radiometric. Triggers - mwrretv2, MWR Retrievals with MWRRET Version 2, sgpmwrret2turnC1.c1, Liquid Water Path, Precipitable Water Vapor, Cloud Properties, Derived Quantities and Models, Radiometric.
---

# MWRRETV2 - MWR Retrievals with MWRRET Version 2

MWRRETV2 is an ARM value-added product that retrieves liquid water path (LWP) and precipitable water vapor (PWV) from 3-channel microwave radiometer (MWR3C) brightness temperature measurements at 23.8, 30, and 89 GHz, combined with atmospheric profile data, and is run routinely on MWR3C data at ARM sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 17 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mwrretv2` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-245 / D Zhang, LD Riihimaki, KL Gaustad, DD Turner / May 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-245.pdf) |
| Category | Cloud Properties; Derived Quantities and Models; Radiometric |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-10-01 to 2026-09-24 (retired) |
| Datastreams with data | 15 across 9 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mwrretv2 |


## Credit

Everything this skill knows about the retrieval is the work of **D Zhang, LD Riihimaki, KL Gaustad, DD Turner** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Zhang, LD Riihimaki, KL Gaustad, DD Turner. *MWRRETV2 Value-Added Product Report: The Retrieval of Liquid Water Path and Precipitable Water Vapor from Microwave Radiometer – 3-Channel (MWR3C) Data Sets*, DOE/SC-ARM-TR-245, May 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-245.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

MWRRETV2 extends the physical-iterative retrieval algorithm of MWRRET (Turner et al. 2007) to work with any set of two or more microwave frequencies, applying it to 3-channel (23.8, 30, 89 GHz) MWR3C brightness temperatures rather than only the original 2-channel (23.8/31.4 GHz) systems. The retrieval uses a radiative transfer model (MonoRTM v4.2) to compute expected clear-sky brightness temperatures and iteratively adjusts profiles of PWV and LWP so that calculated Tb matches observed Tb, using input atmospheric temperature, pressure, and humidity profiles from radiosondes. The 89-GHz channel has approximately three times the sensitivity to liquid water of the 31-GHz channel, improving LWP retrieval accuracy particularly when LWP is less than 100 g/m2. Brightness temperature offsets (biases) are determined automatically from clear-sky residuals (observed minus calculated Tb) over a rolling window (60 or 90 days depending on site) and subtracted from the Tb values prior to retrieval to correct for instrument drift. Both a physical-iterative retrieval method ('phys') and a statistical retrieval method ('stat') are computed and output for comparison.

**Cadence.** input rate MWR sample time (per-sample retrieval at MWR3C measurement times); output every one output file per day; averaging Tb bias determined as mean over rolling 60-day (SGP, Oliktok) or 90-day (ENA) window; clear-sky Tb standard deviation computed over ~20 minute temporal window (hb p. 3).

## Inputs

The report names these instruments and sibling products: MWRRET, MWR3C, ARSCL, ceilometer, radiosonde.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Liquid Water Path (LWP) | g/m2 | - | - | (hb p. 4) |
| Precipitable Water Vapor (PWV) | - | - | - | (hb p. 4) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Rolling window for Tb bias correction (SGP sites, Oliktok... | 60 days (or longer depending on available clear-sky measurements) | (hb p. 3) |
| Rolling window for Tb bias correction (ENA site) | 90 days | (hb p. 3) |
| Clear-sky condition 1 | no cloud detected by active remote-sensing measurements (cbh_detected less than /= 0) | (hb p. 4) |
| Clear-sky condition 2 | standard deviation of Tb over a defined temporal window (usually 20 minutes) below a predetermined threshold, function of PWV | (hb p. 4) |
| Threshold equation | threshold = c + a*(PWV)^1 + b*(PWV)^2 | (hb p. 4) |
| Threshold constants c, a, b (SGP sites and ENA site) | 0.3, -0.01, 0.004 respectively | (hb p. 4) |
| Threshold constants c, a, b (Oliktok point) | 0.6, 0.0, 0.0 respectively | (hb p. 4) |
| MWR3C channel frequencies | 23.8, 30, 89 GHz | (hb p. 8) |
| Original 2-channel MWR frequencies | 23.8 and 31.4 GHz | (hb p. 1) |
| 2-channel MWR LWP uncertainty (historical, Turner et al.... | approximately 25 g/m2 | (hb p. 8) |
| 89-GHz sensitivity to liquid water relative to 31-GHz... | approximately three times | (hb p. 4) |
| LWP threshold below which 89-GHz channel markedly improves... | less than 100 g/m2 | (hb p. 4) |
| Radiative transfer model version | MonoRTM v4.2 | (hb p. 1) |
| Default cloud thickness assumption source order | ARSCL preferred; else ceilometer cloud base height with default thickness; else high-RH layer in profile; else default cloud base of 1 km AGL | (hb p. 9) |
| Output filename convention | XXXmwrret2turnFF.c1.YYYYMMDD.hhmmss | (hb p. 6) |
| Quicklook filename convention | XXXmwrret2turnFF.YYYYMMDD.png and XXXmwrret2turnFF.YYYYMMDD.dynamic.png | (hb p. 6) |


## The data

Verified example: **`sgpmwrret2turnC1.c1`**, file `sgpmwrret2turnC1.c1.20250328.000000.nc`
(12.35 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=67032, `freq`=3 |
| Data variables | 39 |
| QC variables | 2 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2025-03-28T00:00:00 to 2025-03-28T23:59:59 |
| dod version | mwrret2turn-c1-2.17 |
| process version | vap-mwrret2turn-1.35-0.dev7.dirty.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `phys_lwp` | g/m^2 | time | yes | Physically-retrieved liquid water path |
| `phys_pwv` | cm | time | yes | Physically-retrieved precipitable water vapor |
| `assumed_frequency_noise_level` | K | freq | - | Assumed radiometric random noise level for each frequency |
| `cbh_detected` | km | time | - | Cloud base height detected by ceilometer/radar |
| `cbh_used` | km | time | - | Cloud base height used in the retrieval |
| `clearsky_flag` | 1 | time | - | Flag to indicate if the sky is apparently clear |
| `cloud_temp` | K | time | - | Estimated cloud temperature (from "used" fields) |
| `converged` | 1 | time | - | Flag indicating if the retrieval converged |
| `cth_detected` | km | time | - | Cloud top height detected by ceilometer/radar |
| `cth_used` | km | time | - | Cloud top height used in the retrieval |
| `detection_status` | 1 | time | - | Detection status from ceil |
| `elevation_angle` | degree | time | - | Angle of Elevation |
| `freq` | GHz | freq | - | Frequency |
| `num_iteration` | 1 | time | - | Number of iterations performed by the retrieval |
| `observation_static_offset` | K | freq | - | The static (time-independent) offset applied to the observed... |
| `phys_lwp_uncertainty` | g/m^2 | time | - | Uncertainty (1-sigma) in physically retrieved liquid water path |
| `phys_pwv_lwp_error_correlation` | 1 | time | - | Correlation between uncertainties in physically-retrieved PWV and LWP |
| `phys_pwv_uncertainty` | cm | time | - | Uncertainty (1-sigma) in physically-retrieved precipitable water vapor |
| `phys_qc_flag` | 1 | time | - | Quality control flag indicating if the physical retrieval should be... |
| `ptu_flag` | 1 | time | - | Flag indicating if this is the true PTU profile |
| `ptu_pwv` | cm | time | - | Precipitable water vapor from the temporally interpolated PTU data... |
| `rain_intensity` | mm/s | time | - | Rain intensity |
| `rms` | K | time | - | Root mean square difference between observed and computed (from final... |
| `stat_lwp` | g/m^2 | time | - | Statistically-retrieved liquid water path |
| `stat_lwp_uncertainty` | g/m^2 | time | - | Estimated 1-sigma uncertainty in statistically-retrieved lwp |
| `stat_pwv` | cm | time | - | Statistically-retrieved precipitable water vapor |
| `stat_pwv_uncertainty` | cm | time | - | Estimated 1-sigma uncertainty in statistically-retrieved pwv |
| `surface_temperature` | degC | time | - | Surface temperature |
| `tbsky_calc` | K | time,freq | - | Calculated brightness temperature from final iteration |
| `tbsky_calc_cs` | K | time,freq | - | Clear-sky calculated brightness temperature |


_4 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpmwrret2turnC1.c1", "2025-03-28", "2025-03-28")
ds = armlive_open("sgpmwrret2turnC1.c1", "2025-03-28", "2025-03-28", cleanup_qc=True)
```

## Quality control in this product

2 `qc_` companion variables cover 2 of the
39 data variables. Assessments present in the example file: `Bad`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmwrret2turnC1.c1", "20111001", "20260924")
```

The report's own note on quality: All quality flags associated with input fields are propagated to the output. A QC flag is set for each retrieved variable (PWV, LWP) to indicate whether the retrieval is good or bad. QC tests include identification of unrealistic retrievals (PWV less than  0), number of iterations of retrievals, and standard deviations of outputs. A 'converged' variable indicates whether the physical-iterative retrieval converged; 'num_iteration' stores the number of iterations performed. Flags indicating clear-sky and precipitating periods are also included in the output, along with root-mean-square...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Systematic brightness temperature (Tb) biases/offsets causing nonzero retrieved LWP in... | Retrieved LWP is significantly nonzero during known clear-sky periods; upward trend in uncorrected Tb residuals over time (e.g., seen in 89-GHz channel data at ENA in 2017) | Determine and subtract Tb offsets via postprocessing using an automated rolling-window (60- or 90-day) clear-sky bias correction rather than a single... | (hb p. 9) |
| Annual (single, static) Tb bias correction insufficient to capture drift | Clear upward trend evident in uncorrected 89-GHz data persists even after annual correction; only resolved by monthly/rolling corrections | Use automated rolling-window (60-90 day) bias correction instead of annual/manual correction | (hb p. 9) |
| MWRRET (original) algorithm incompatible with 3-channel systems | Original 2-channel-specific adaptive Tb offset QC logic cannot be applied when a third (89 GHz) channel is present | Use MWRRETV2, which extends the physical-iterative algorithm to be flexible for any set of two or more frequencies | (hb p. 1) |
| Unrealistic PWV retrievals (negative PWV) | Retrieved PWV less than  0 | Flagged by QC test for unrealistic retrievals | (hb p. 5) |
| Non-convergence of physical-iterative retrieval | 'converged' flag set to false/not converged; example shown for 22 August 2019 SGP C1 case with significant amounts of non-converged retrievals plotted as red lines | Variable 'converged' output to indicate convergence status; 'num_iteration' records number of iterations performed | (hb p. 12) |
| Missing or unavailable cloud boundary information (ARSCL unavailable) | Cloud base/top source falls back to ceilometer or profile-derived estimate, changing retrieval assumptions | Falls back to ceilometer cloud base height with assumed default thickness; if that unavailable, search profile for high-RH layers; if none found,... | (hb p. 9) |
| Precipitation contamination of retrieval | Retrieval indeterminate or bad during precipitating periods, flagged via surface meteorological precipitation field gridded to radiometer time samples | Flag cases where retrieval is indeterminate or bad using surface met precipitation data; precipitating-period flag included in output | (hb p. 9) |
| Low-level marine stratocumulus reducing clear-sky sample availability (site-specific) | Fewer clear-sky periods available for Tb bias determination at ENA site | Use longer 90-day rolling window at ENA site instead of the 60-day window used elsewhere | (hb p. 3) |
| Discrepancy between statistical ('stat') and physical-iterative ('phys') retrieval methods | Differences between 'statpwv'/'statlwp' and 'physpwv'/'physlwp' lines in quicklook plots | Both methods computed and plotted for comparison in quicklook output | (hb p. 6) |
| Dependence on radiosonde profile availability and interpolation | Atmospheric profile input interpolated from radiosonde data of current, previous, and next days; retrieval quality depends on radiosonde data density/quality | Code performs basic QC checks on radiosonde data and interpolates to a common height grid, then to each MWR sample time | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Cadeddu, MP, and DD Turner. 2011. IEEE Transactions on Geoscience and Remote Sensing 49(8): 2999-3008
- Cadeddu, MP, JC Liljegren, and DD Turner. 2013. Atmospheric Measurement Techniques 6(9): 2359-2372
- Gaustad, KL, DD Turner, and SA McFarlane. 2011. MWRRET Value-Added Product Report. DOE/SC-ARM-TR-081.2
- Liljegren, JC, and BM Lesht. 1996. IGARSS '96 3: 1675-1677
- Löhnert, U, and S Crewell. 2003. Radio Science 38(3): 8041
- van Meijgaard, E and S Crewell. 2005. Atmospheric Research 75(3): 201-226
- Turner, DD, SA Clough, JC Liljegren, EE Clothiaux, KE Cady-Pereira, and KL Gaustad. 2007. IEEE Transactions on Geoscience and Remote Sensing 45(11): 3680-3690
- Turner, DD, U Loehnert, M Cadeddu, S Crewell, and A Vogelmann. 2009. IEEE Transactions on Geoscience and Remote Sensing 47(10): 3326-3337

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-245.pdf (17 pages, DOE/SC-ARM-TR-245, by D Zhang, LD Riihimaki, KL Gaustad, DD Turner)
- Catalog record: ARM data-source index, `instrument_class_code=mwrretv2`, read 2026-09-24
- Example file: `sgpmwrret2turnC1.c1.20250328.000000.nc` from `sgpmwrret2turnC1.c1`, 12.35 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
