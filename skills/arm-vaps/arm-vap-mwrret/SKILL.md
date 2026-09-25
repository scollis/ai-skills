---
name: arm-vap-mwrret
description: ARM MWR Retrievals (mwrret) - value-added product reference from its technical report. Derived from mwr. The retrieval algorithm, reported quantities (Precipitable water vapor, Liquid water path), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpmwrret1liljclouC1.c1) and the variable inventory of a real file. Use when working with mwrret data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties; Derived Quantities and Models; Radiometric. Triggers - mwrret, MWR Retrievals, sgpmwrret1liljclouC1.c1, mwr VAP, Precipitable water vapor, Liquid water path, Cloud Properties, Derived Quantities and Models, Radiometric.
---

# MWRRET - MWR Retrievals

The MWRRET VAP derives best-estimate precipitable water vapor (PWV) and liquid water path (LWP) from two-channel (23.8 and 31.4 GHz) microwave radiometer brightness temperature observations at ARM sites, using a physical retrieval method and brightness temperature offset corrections applied to MWR instrument data.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 19 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `mwrret` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM/TR-081.2 / KL Gaustad, DD Turner, SA McFarlane / July 2011](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-081.2.pdf) |
| Category | Cloud Properties; Derived Quantities and Models; Radiometric |
| Input instruments | `mwr` |
| Record | 1996-09-01 to 2026-09-18 (active) |
| Datastreams with data | 77 across 27 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/mwrret |


## Credit

Everything this skill knows about the retrieval is the work of **KL Gaustad, DD Turner, SA McFarlane** -
the ARM developers and mentors who wrote the technical report it derives from:

> KL Gaustad, DD Turner, SA McFarlane. *MWRRET Value-Added Product: The Retrieval of Liquid Water Path and Precipitable Water Vapor from Microwave Radiometer (MWR) Data Sets*, DOE/SC-ARM/TR-081.2, July 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-081.2.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The ARM microwave radiometers (MWR) observe downwelling radiation at 23.8 and 31.4 GHz. The instrument-resident 'orig' retrieval uses a statistical methodology based on site-dependent monthly retrieval coefficients (Liljegren and Lesht 1996) to convert brightness temperatures into PWV and LWP. The MWRRET VAP instead applies a physical/iterative retrieval algorithm that produces the most accurate retrievals when the atmospheric temperature profile and an estimate of the distribution of water vapor and liquid water are known. The VAP also applies brightness temperature offsets (static offsets at 23.8 GHz determined annually per site, and variable offsets at 31.4 GHz computed from a rolling database of cases) to reduce systematic clear-sky biases so that a LWP of zero in clear skies is statistically achieved. The output combines the 'orig', 'stat2', and 'phys' method retrievals with surface meteorology and MWR input data to produce best-estimate be_pwv and be_lwp values.

**Cadence.** output every One output file created per day; averaging Ensemble averages (mean_pwv_mwr, mean_lwp_mwr, mean_tbsky23_mwr, mean_tbsky31_mwr) computed over a window centered upon the current sample (hb p. 8).

## Inputs

ARM's catalog declares these input instrument classes: `mwr`.

The report names these instruments and sibling products: mwr (microwave radiometer), ARSCL VAP, Belfort laser ceilometer (BLC), Vaisala ceilometer (VCEIL).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Precipitable water vapor (best estimate) | cm | - | - | (hb p. 15) |
| Liquid water path (best estimate) | g/m^2 | - | - | (hb p. 15) |
| Sky brightness temperature at 23.8 GHz | K | - | - | (hb p. 15) |
| Sky brightness temperature at 31.4 GHz | K | - | - | (hb p. 15) |
| PWV retrieved using physical/iterative approach | cm | - | 1-sigma uncertainty reported as... | (hb p. 16) |
| Cloud liquid water path retrieved using physical/iterative... | g/m^2 | - | 1-sigma uncertainty reported as... | (hb p. 16) |
| Total water vapor along LOS path (orig) | cm | - | - | (hb p. 15) |
| Total liquid water along LOS path (orig) | g/m^2 | - | - | (hb p. 16) |
| Cloud base height | km AGL | - | - | (hb p. 15) |
| Cloud temperature used in the retrieval | K | - | - | (hb p. 15) |
| Surface temperature | K | - | - | (hb p. 15) |
| Surface vapor pressure | kPa | - | - | (hb p. 15) |
| Surface pressure | kPa | - | - | (hb p. 15) |
| Surface relative humidity | % | - | - | (hb p. 15) |
| Radiosonde-integrated PWV | cm | - | - | (hb p. 17) |


## The data

Verified example: **`sgpmwrret1liljclouC1.c1`**, file `sgpmwrret1liljclouC1.c1.20260915.000000.nc`
(1.25 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=3985, `nlevels`=54, `nvbias`=100 |
| Data variables | 81 |
| QC variables | 28 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-09-15T00:00:00 to 2026-09-15T23:59:29 |
| dod version | mwrret1liljclou-c1-1.6 |
| process version | vap-mwrret1liljclou-1.20-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `be_lwp` | g/m^2 | time | yes | Liquid water path best-estimate value |
| `be_pwv` | cm | time | yes | Precipitable water vapor best-estimate value |
| `cloud_base_height` | km | time | yes | Cloud base height |
| `cloud_temp` | K | time | yes | Cloud temperature used in the retrieval |
| `mean_tbsky23_mwr` | K | time | yes | Ensemble average for MWR 23.8 GHz sky brightness temperature in... |
| `mean_tbsky31_mwr` | K | time | yes | Ensemble average for MWR 31.4 GHz sky brightness temperature in... |
| `orig_lwp` | g/m^2 | time | yes | Total liquid water along LOS path |
| `orig_pwv` | cm | time | yes | Total water vapor along LOS path |
| `phys_converge` | 1 | time | yes | Convergence value for the physical retrieval |
| `phys_lwp` | g/m^2 | time | yes | Cloud liquid water path retrieved using a physical/iterative approach |
| `phys_lwp_uncertainty` | g/m^2 | time | yes | 1-sigma uncertainty in cloud liquid water path retrieved using a... |
| `phys_niter` | count | time | yes | Number of iterations needed by the physical retrieval for convergence |
| `phys_pwv` | cm | time | yes | Precipitable water vapor retrieved using a physical/iterative approach |
| `phys_pwv_uncertainty` | cm | time | yes | 1-sigma uncertainty in precipitable water vapor retrieved using a... |
| `phys_rms` | K | time | yes | Root mean square difference between the computed and observed... |
| `sdev_tbsky23_mwr` | K | time | yes | Standard deviation for ensemble average for MWR 23.8 GHz sky... |
| `sdev_tbsky31_mwr` | K | time | yes | Standard deviation for ensemble average for MWR 31.4 GHz sky... |
| `sonde_pwv` | cm | time | yes | Precipitable water vapor integrated from the radiosonde profile |
| `stat2_lwp` | g/m^2 | time | yes | Cloud liquid water path retrieved using predicted mean radiating... |
| `stat2_pwv` | cm | time | yes | Precipitable water vapor retrieved using predicted mean radiating... |
| `surface_pres` | kPa | time | yes | Surface pressure |
| `surface_rh` | % | time | yes | Surface relative humidity |
| `surface_temp` | K | time | yes | Surface temperature |
| `surface_vapor_pres` | kPa | time | yes | Surface vapor pressure |
| `tbsky23` | K | time | yes | Sky brightness temperature at 23.8 GHz |
| `tbsky23_calculated` | K | time | yes | Calculated sky brightness temperature at 23.8 GHz |
| `tbsky31` | K | time | yes | Sky brightness temperature at 31.4 GHz |
| `tbsky31_calculated` | K | time | yes | Calculated sky brightness temperature at 31.4 GHz |
| `be_retrieval_status` | 1 | time | - | Best-estimate retrieval status |
| `mean_lwp_mwr` | g/m^2 | time | - | Ensemble average for MWR liquid (orig_lwp) in window centered upon... |


_19 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpmwrret1liljclouC1.c1",
                             "start": "2026-09-15", "end": "2026-09-15", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpmwrret1liljclouC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpmwrret1liljclouC1.c1", "2026-09-15", "2026-09-15")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpmwrret1liljclouC1.c1", "2026-09-15", "2026-09-15"))   # cite what you pulled
```

This product carries 81 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpmwrret1liljclouC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['be_lwp', 'be_pwv', 'cloud_base_height', 'qc_be_lwp', 'qc_be_pwv', 'qc_cloud_base_height'],
                                cleanup_qc=True)
```

## Quality control in this product

28 `qc_` companion variables cover 28 of the
81 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
# What each test would remove, one variable at a time
print(ds["qc_be_pwv"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("be_pwv", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["be_pwv", "be_lwp", "cloud_base_height"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpmwrret1liljclouC1.c1.20260915.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `sonde_pwv` | Data has bad quality, value set to missing_value. | 3983 | 99.9498 |
| `cloud_base_height` | Clear sky conditions, data value set to missing_value. | 3849 | 96.5872 |
| `stat2_lwp` | cloud_base_height field is missing. | 3849 | 96.5872 |
| `phys_lwp` | cloud_base_height field is missing. | 3849 | 96.5872 |
| `phys_pwv` | cloud_base_height field is missing. | 3849 | 96.5872 |
| `stat2_pwv` | cloud_base_height field is missing. | 3849 | 96.5872 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpmwrret1liljclouC1.c1", "19960901", "20260924")
```

The report's own note on quality: All quality flags associated with input fields are propagated to the output. Additional QC tests (developed by Jim Liljegren) are applied to MWR brightness temperatures to identify sudden abnormal instantaneous changes, covering thermal stabilization issues, spikes, and invalid optical depths. QC tests were also developed for the non-best-estimate PWV and LWP fields calculated by the VAP. In *c2 level output files, be_pwv and be_lwp samples with indeterminate QC assessments are set to the missing value -9999. Quicklook plots display colored bars along the bottom axis of the brightness...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Statistical 'orig' retrieval errors under atmospheric conditions unlike those used to... | Large retrieval errors in orig_pwv/orig_lwp during atmospheric conditions that differ significantly from conditions captured in the site's monthly retrieval coefficients | Use the MWRRET physical retrieval (phys_pwv, phys_lwp) instead of relying solely on the instrument-resident 'orig' statistical retrieval | (hb p. 6) |
| Site-specific statistical retrieval coefficients not transferable | orig retrieval coefficients cannot be applied to other locations; using them at a different site would produce invalid PWV/LWP | - | (hb p. 6) |
| Systematic clear-sky LWP bias in original algorithm | Retrieved LWP biased from +/- 5 to 30 g/m2 in clear-sky scenes when true LWP should be zero (within retrieval uncertainty) | Apply variable brightness temperature offsets at 31.4 GHz so that, statistically, a LWP of zero in clear skies is obtained | (hb p. 7) |
| Clear-sky LWP bias causing radiative transfer calculation errors | Significant error in radiative transfer calculations when biased LWP values are used (per Turner et al. 2007a) | Correct via variable Tb offset subtraction at 31.4 GHz | (hb p. 7) |
| Static Tb offsets not applied in real-time processing | Real-time production data (c1 level) will show unadjusted 23.8-GHz brightness temperatures/PWV until yearly reprocessing produces c2 level files | Use *c2 level files for final data; *c1 level files indicate additional processing is still expected | (hb p. 6) |
| Static offsets not calculated for certain sites | No static Tb offset correction applied for high-PWV tropical sites (Manus, Nauru) or for sites lacking radiosondes (NSA C2 and SGP extended facilities) | - | (hb p. 7) |
| Instrument health issues detected in brightness temperature data | Sudden abnormal instantaneous changes in brightness temperature values; QC flags such as 'possible spike' and 'spike simple' set for affected samples, shown as colored bars along bottom... | Additional QC tests applied (developed by Jim Liljegren) identify thermal stabilization issues, spikes, and invalid optical depths; flagged data... | (hb p. 4) |
| Indeterminate QC assessments in c2-level output | be_pwv and be_lwp samples with indeterminate QC assessments are set to missing value -9999 in *c2 level files | Check qc_be_pwv/qc_be_lwp fields and treat -9999 as missing | (hb p. 8) |
| Missing radiosonde profile input | VAP will run without balloon-borne sounding system profiles, but physical retrieval accuracy depends on having temperature/water vapor/liquid profile estimates | Use sonde profiles when available; VAP selects sonde platform based on a prioritized list (wnpn.b1, wrpn.a1, wrpn.b1, wnpn.a1, wrpr.a1) when multiple... | (hb p. 6) |
| Optional cloud base height source ambiguity | Cloud base height input may come from Belfort laser ceilometer (BLC), Vaisala ceilometer (VCEIL), or ARSCL VAP depending on operator choice, potentially affecting cloud_temp and retrieval... | Choice of cloud base height source is specified at the command line and left to VAP operator discretion | (hb p. 6) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `mwr`: load `arm-instrument-mwr` for its handbook facts and artifacts

### References the report cites

- Liljegren, JC, and BM Lesht. 1996. "Measurements of integrated water vapor and cloud liquid water from microwave radiometers at the DOE ARM cloud and radiation testbed in the U.S. Southern Great Plains." In Proceedings...
- Turner, DD, and KL Gaustad. 2004. "Improved PWV and LWP retrievals from the microwave radiometer for ARM." In Proceedings of the Fourteenth Atmospheric Radiation Measurement (ARM) Science Team Meeting, U.S. Department...
- Turner, DD, AM Vogelmann, R Austin, JC Barnard, K Cady-Pereira, C Chiu, SA Clough, CJ Flynn, MM Khaiyer, JC Liljegren, K Johnson, B Lin, CN Long, A Marshak, SY Matrosov, SA McFarlane, MA Miller, Q Min, P Minnis, W...
- Turner, DD, SA Clough, JC Liljegren, EE Clouthiaux, K Cady-Pereira, and KL Gaustad. 2007b. "Retrieving liquid water path and precipitable water vapor from the Atmospheric Radiation Measurement (ARM) microwave...

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-081.2.pdf (19 pages, DOE/SC-ARM/TR-081.2, by KL Gaustad, DD Turner, SA McFarlane)
- Catalog record: ARM data-source index, `instrument_class_code=mwrret`, read 2026-09-24
- Example file: `sgpmwrret1liljclouC1.c1.20260915.000000.nc` from `sgpmwrret1liljclouC1.c1`, 1.25 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
