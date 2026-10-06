---
name: arm-vap-mergedsmpsaps
description: ARM merged size distribution from SMPS and APS (mergedsmpsaps) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (aps_dN_dlogDp, smps_dN_dlogDp, merged_dN_dlogDp, effective_density, merged_total_N_conc, merged_total_SA_conc), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (enamergedsmpsapsC1.c1) and the variable inventory of a real file. Use when working with mergedsmpsaps data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Aerosols. Triggers - mergedsmpsaps, merged size distribution from SMPS and APS, enamergedsmpsapsC1.c1, aps_dN_dlogDp, smps_dN_dlogDp, merged_dN_dlogDp, effective_density, merged_total_N_conc, Aerosols.
---

# MERGEDSMPSAPS - merged size distribution from SMPS and APS

The mergedsmpsaps VAP merges submicron mobility-diameter size distributions from the SMPS with sub- and super-micron aerodynamic-diameter size distributions from the APS into a single continuous aerosol number size distribution spanning approximately 10-20,000 nm mobility diameter, deployed as part of ARM's Aerosol Observing System (AOS).

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 15 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mergedsmpsaps` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-294 / JE Shilling, MS Levin / December 2023](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-294.pdf) |
| Category | Aerosols |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2016-11-15 to 2026-09-23 (active) |
| Datastreams with data | 7 across 7 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mergedsmpsaps |


## Credit

Everything this skill knows about the retrieval is the work of **JE Shilling, MS Levin** -
the ARM developers and mentors who wrote the technical report it derives from:

> JE Shilling, MS Levin. *Scanning Mobility Particle Sizer (SMPS)-Aerodynamic Particle Sizer (APS) Merged Size Distribution (mergedsmpsaps) Value-Added Product Report*, DOE/SC-ARM-TR-294, December 2023.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-294.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The SMPS measures submicron particle size distributions by charging particles to an equilibrium distribution with an aerosol neutralizer, selecting a narrow size cut according to electric mobility diameter with a differential mobility analyzer (DMA), and counting particles with a condensation particle counter (CPC). The APS measures sub- and super-micron particle size distributions by accelerating particles through an expansion nozzle and measuring particle time of flight between two downstream laser beams, converting time of flight to an aerodynamic diameter (larger particles take longer to transit). Because SMPS mobility diameter and APS aerodynamic diameter are not equivalent, the VAP iteratively shifts the APS diameter (via an effective density) until a minimum residual is obtained between SMPS and APS particle counts in the overlap region, following Beddows et al. (2010). The APS aerodynamic diameter is then converted to mobility diameter using the derived effective density (assuming a shape factor of unity) and re-binned onto the native SMPS bin structure (64 bins/decade, constant dlogDp) so the two distributions can be concatenated into one merged dN/dlogDp distribution.

**Cadence.** output every 1 hour; averaging Data are averaged to a 1-hour time resolution to improve signal at low particle counts and improve VAP performance; if more than half of the average period is missing data from either instrument, data are excluded and a merged size distribution is not calculated (hb p. 4).

## Inputs

The report names these instruments and sibling products: SMPS (scanning mobility particle sizer), APS (aerodynamic particle sizer).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| aps_dN_dlogDp (APS aerosol number size distribution) | 1/cm3 | aerodynamic diameters 523 to... | - | (hb p. 9) |
| smps_dN_dlogDp (SMPS aerosol number size distribution) | 1/cm3 | mobility diameters 10.6 to 514 nm | - | (hb p. 9) |
| merged_dN_dlogDp (merged aerosol number size distribution) | 1/cm3 | merged mobility diameters 10.6 to... | - | (hb p. 10) |
| effective_density | g/cm3 | valid range approximately 1.5-3... | - | (hb p. 10) |
| merged_total_N_conc (total number concentration) | 1/cm3 | - | - | (hb p. 10) |
| merged_total_SA_conc (total surface area concentration) | nm2/cm3 | - | - | (hb p. 11) |
| merged_total_V_conc (total volume concentration) | nm3/cm3 | - | - | (hb p. 11) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| SMPS mobility diameter range | 10.6 to 514 nm | (hb p. 6) |
| APS aerodynamic diameter range | 523 to 20,536 nm | (hb p. 6) |
| Merged mobility diameter range (midpoint diameters) | 10.555 to 20,909.234 nm | (hb p. 7) |
| Merged bin structure | 64 bins per decade, constant dlogDp | (hb p. 7) |
| Minimum effective density resolvable | approximately 1.5 g/cm3 | (hb p. 8) |
| Effective density minimum QC threshold | 1.4 g/cm3 | (hb p. 10) |
| Effective density maximum QC threshold | 3.0 g/cm3 | (hb p. 10) |
| Time resolution | 1-hour averaging | (hb p. 6) |


## The data

Verified example: **`enamergedsmpsapsC1.c1`**, file `enamergedsmpsapsC1.c1.20260920.000000.nc`
(0.09 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=24, `bound`=2, `merged_diameter_mobility`=212, `diameter_aerodynamic`=51, `diameter_mobility`=192 |
| Data variables | 32 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2026-09-20T00:00:00 to 2026-09-20T23:00:00 |
| dod version | mergedsmpsaps-c1-1.3 |
| process version | mergedsmpsaps-0.4.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `effective_density` | g/cm^3 | time | yes | Aerosol particle effective density |
| `merged_dN_dlogDp` | 1/cm^3 | time,merged_diameter_mobility | yes | Number size distribution, merged |
| `merged_total_N_conc` | 1/cm^3 | time | yes | Total aerosol number concentration, merged |
| `merged_total_SA_conc` | nm^2/cm^3 | time | yes | Total aerosol surface area, merged |
| `merged_total_V_conc` | nm^3/cm^3 | time | yes | Total aerosol volume, merged |
| `DA_num_density` | g/cm^3 | time | - | Dual Annealing Number Solution Effective Density |
| `DA_vol_density` | g/cm^3 | time | - | Dual Annealing Volume Solution Effective Density |
| `DE_num_density` | g/cm^3 | time | - | Differential Evolution Number Solution Effective Density |
| `DE_vol_density` | g/cm^3 | time | - | Differential Evolution Volume Solution Effective Density |
| `aps_dN_dlogDp` | 1/cm^3 | time,diameter_aerodynamic | - | Number size distribution, aerodynamic diameter |
| `aps_total_N_conc` | 1/cm^3 | time | - | Aerosol number concentration from integrated size distribution, APS |
| `diameter_aerodynamic` | nm | diameter_aerodynamic | - | Midpoint of geometric mean aerodynamic diameter |
| `diameter_mobility` | nm | diameter_mobility | - | Midpoint of geometric mean mobility diameter |
| `effective_density_solution_strength` | 1 | time | - | Strength of effective density solution |
| `merged_diameter_mobility` | nm | merged_diameter_mobility | - | Merged midpoint of geometric mean mobility diameter |
| `resid_DA_num` | 1 | time | - | Dual Annealing Number Solution Residual |
| `resid_DA_vol` | 1 | time | - | Dual Annealing Volume Solution Residual |
| `resid_DE_num` | 1 | time | - | Differential Evolution Number Solution Residual |
| `resid_DE_vol` | 1 | time | - | Differential Evolution Volume Solution Residual |
| `smps_dN_dlogDp` | 1/cm^3 | time,diameter_mobility | - | Number size distribution, electrical mobility diameter |
| `smps_total_N_conc` | 1/cm^3 | time | - | Aerosol number concentration from integrated size distribution, SMPS |
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
                     params={"user": f"{user}:{token}", "ds": "enamergedsmpsapsC1.c1",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enamergedsmpsapsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enamergedsmpsapsC1.c1", "2026-09-20", "2026-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enamergedsmpsapsC1.c1", "2026-09-20", "2026-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("effective_density", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

5 `qc_` companion variables cover 5 of the
32 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_effective_density"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("effective_density", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["effective_density", "merged_dN_dlogDp", "merged_total_N_conc"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired, so the machinery is present but unexercised
there - not a guarantee for other days.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("enamergedsmpsapsC1.c1", "20161115", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The VAP applies bit-packed QA/QC flags (qc_effective_density, qc_merged_dN_dlogDp, qc_merged_total_N_conc, qc_merged_total_SA_conc, qc_merged_total_V_conc). Checks include: (1) bad quality input smps_dN_dlogDp, (2) bad quality input aps_dN_dlogDp, (3) effective density below 1.4 g/cm3 or merged_total_N_conc exceeding sum of component concentrations, (4) effective density above 3.0 g/cm3 or effective_density failing limit QC. Data flagged bad are not to be used; check 3 failures are flagged indeterminate rather than bad. A solution_strength variable (0-3) tracks confidence in the effective...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Non-equivalence of SMPS mobility diameter and APS aerodynamic diameter | Raw APS and SMPS distributions do not align at the same diameter axis; requires diameter conversion via effective density before merging | VAP iteratively shifts APS diameter and converts aerodynamic diameter to mobility diameter using a derived effective density (Beddows et al. 2010... | (hb p. 6) |
| Minimum resolvable effective density limited to ~1.5 g/cm3 | Effective density solutions below ~1.5 g/cm3 cannot be produced by the algorithm; low-density aerosol cases may show anomalously high or flagged density values | Caused by requirement of a minimum of three overlapping size bins between APS and SMPS (step 9.b.i); if overlap is less than 3 bins, an artificially... | (hb p. 8) |
| Effective density outside valid range (1.5-3 g/cm3) or failing solution-agreement criteria | Data flagged as bad; no merged size distribution calculated for that period | Algorithm requires 3+ of 4 density solutions to agree (rounded to nearest tenth) or all four within one standard deviation of the mean; otherwise... | (hb p. 8) |
| Local minima / noise-driven spread in effective density solution space | Multiple candidate effective density values from different solvers scatter widely, especially in low-count or overlap regions; visible as noisy effective_density time series (Figure 1) and... | Use of two global solvers (dual_annealing and differential_evolution, scipy.optimize) instead of least-squares solvers to minimize spread; four... | (hb p. 8) |
| Largest measurement error in the SMPS-APS overlap region | Increased scatter/uncertainty in merged distribution near the transition zone between SMPS upper range and APS lower range (upper end of SMPS scan range, lower end of APS range) | Advise users to pay close attention to QA/QC flags and not use flagged-bad data; future plan to apply machine learning filtering and to consider... | (hb p. 9) |
| Missing/zero/NaN-filled size distributions in APS or SMPS input | Bins or time periods with all-zero or NaN dN/dlogDp values | Algorithm removes such size distributions and flags the data (step 6) | (hb p. 7) |
| Insufficient input data availability in averaging window | Merged size distribution not produced for that hour; missing values in output | If more than half of the 1-hour average period is missing data from either instrument, the period is excluded from the VAP | (hb p. 4) |
| DQR timing lag relative to VAP processing | Bad/problematic data flagged in a Data Quality Report (DQR) filed after VAP processing may still appear as valid (unflagged) in the VAP output | Users encouraged to examine DQRs for both SMPS and APS data for periods of interest; DQRs filed at time of processing are excluded, but later DQRs... | (hb p. 4) |
| First APS bin (4-bin-per-decade spacing, centered on 514 nm) removed | No data reported at the theoretical 514 nm APS bin; slight discontinuity/gap possible at the SMPS-APS boundary | Bin is deliberately excluded from algorithm and output per methodology step 3 | (hb p. 7) |
| Rounding differences in midpoint diameters between SMPS b1 text file and merged product | Slight numerical differences in midpoint diameter values reported in SMPS vs. merged size files despite being theoretically identical bins | Contact the translator for more information regarding these differences | (hb p. 7) |
| merged_total_N_conc exceeding sum of smps_total_N_conc and aps_total_N_conc | QC check 3 fails; merged_total_N_conc, merged_dN_dlogDp, SA and V concentrations flagged as indeterminate | Flagged via qc_merged_total_N_conc / qc_merged_dN_dlogDp etc.; do not use without checking flag | (hb p. 10) |
| Bad quality input SMPS or APS dN/dlogDp data | effective_density and merged variables set to missing at affected timestamps | QC checks 1 and 2 catch bad input data quality and propagate missing values downstream | (hb p. 10) |
| Algorithm degradation with poor data quality or low particle counts in overlap region | Erroneous or highly variable effective density and merged distribution outputs during periods of instrument issues or low aerosol loading | Strongly advise attention to QA/QC flags; plan to use machine learning to further filter problematic data in the future | (hb p. 9) |
| Custom diameter-range integration by users | User-calculated integrated quantities over non-standard diameter ranges may not match VAP's pre-calculated number/SA/volume if bin spacing (64 bins/decade, dN/dlogDp units) is not accounted... | Note that bin spacing is 64 bins/decade and size distributions are reported in dN/dlogDp units when calculating custom integrated quantities | (hb p. 8) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Beddows, DCS, M Dall'osto, and RM Harrison. 2010. "An Enhanced Procedure for the Merging of Atmospheric Particle Size Distribution Data Measured Using Electrical Mobility and Time-of-Flight Analysers." Aerosol Science...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-294.pdf (15 pages, DOE/SC-ARM-TR-294, by JE Shilling, MS Levin)
- Catalog record: ARM data-source index, `instrument_class_code=mergedsmpsaps`, read 2026-09-24
- Example file: `enamergedsmpsapsC1.c1.20260920.000000.nc` from `enamergedsmpsapsC1.c1`, 0.09 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
