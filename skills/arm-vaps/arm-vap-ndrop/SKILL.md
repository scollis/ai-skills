---
name: arm-vap-ndrop
description: ARM Droplet number concentration (ndrop) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Droplet number concentration, Adiabaticity parameter, Measured liquid water path), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpndropmfrsrC1.c1) and the variable inventory of a real file. Use when working with ndrop data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - ndrop, Droplet number concentration, sgpndropmfrsrC1.c1, Adiabaticity parameter, Cloud Properties.
---

# NDROP - Droplet number concentration

The NDROP VAP estimates cloud droplet number concentration of overcast water clouds by combining cloud optical depth from the MFRSR with liquid water path from the MWR, along with adiabatic LWP and adiabaticity (beta) estimates when cloud boundary data are available, deployed as a ground-based ARM value-added product.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 29 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ndrop` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-140 / L Riihimaki, S McFarlane, C Sivaraman / March 2021](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-140.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 1998-01-01 to 2026-05-06 (retired) |
| Datastreams with data | 6 across 5 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ndrop |


## Credit

Everything this skill knows about the retrieval is the work of **L Riihimaki, S McFarlane, C Sivaraman** -
the ARM developers and mentors who wrote the technical report it derives from:

> L Riihimaki, S McFarlane, C Sivaraman. *Droplet Number Concentration Value-Added Product*, DOE/SC-ARM-TR-140, March 2021.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-140.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The retrieval follows McComiskey et al. (2009), based on Boers and Mitchell (1994), assuming an adiabatic cloud model in which liquid water path LWP = 1/2 (1-beta) Cw H^2, where H is cloud thickness, beta is a mixing parameter (0 for adiabatic, 0less than betaless than 1 for sub-adiabatic), and Cw is the adiabatic condensation rate depending on cloud base temperature and pressure. Comparing measured MWR LWP to the calculated adiabatic LWP allows beta to be solved for and constrained to the physically valid range 0-1. The visible cloud optical depth is related to LWP, droplet number concentration N, cloud thickness H, and a droplet size distribution parameter k, and combining the optical depth and LWP equations yields N = C1 * k^-1 * rho_l^2 * tau^3 * LWP^-2.5 * [(1-beta)Cw]^0.5, with C1=0.05789 assuming Qext=2 and k=0.74 (Brenguier et al. 2011). Two variables are output: drop_number_conc (uses best-estimate beta when cloud thickness available) and drop_number_conc_adiabatic (assumes beta=0).

**Cadence.** output every gridded onto a common temporal grid using ADI functions (hb p. 8).

## Inputs

The report names these instruments and sibling products: multi-filter rotating shadowband radiometer (MFRSR), microwave radiometer (MWR), Active Remote Sensing of Clouds (ARSCL) product, ceilometer (vceil25k), Merged Sounding product, narrow field-of-view (NFOV2) instrument, micropulse lidar (MPL).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Droplet number concentration (drop_number_conc) | m-3 | valid_min = 0; qc_max = 1.e+10 | see drop_number_conc_toterror (propagated... | (hb p. 24) |
| Droplet number concentration total error... | m-3 | valid_min = 0 | - | (hb p. 25) |
| Droplet number concentration, adiabatic... | m-3 | valid_min = 0; qc_max = 1.e+10 | - | (hb p. 26) |
| Adiabaticity parameter (beta) | unitless | constrained to 0-1 | delta_beta = 10% | (hb p. 23) |
| Calculated adiabatic liquid water path (lwp_adiabatic) | kg m-2 | valid_min = 0 | - | (hb p. 27) |
| Measured liquid water path (lwp_meas) | kg m-2 | valid_min = -50 | +/- 20 g/m2 (MWR assumed error) | (hb p. 20) |
| Cloud optical depth, instantaneous... | unitless | valid_min = 0 | relative error from cldtaui_toterror / tau | (hb p. 18) |
| Cloud base height (cloud_base_height) | m | - | - | (hb p. 20) |
| Cloud top height (cloud_top_height) | m | - | - | (hb p. 21) |
| Cloud thickness (cloud_thickness) | m | - | - | (hb p. 21) |
| Cloud base temperature (cloud_base_temperature) | K | valid_min = 183.15; valid_max =... | - | (hb p. 22) |
| Cloud base pressure (cloud_base_pressure) | Pa | valid_min = 1000; valid_max =... | - | (hb p. 22) |
| Barometric pressure (bar_pres) | Pa | valid_min = 1000; valid_max =... | - | (hb p. 19) |
| Temperature (temp) | K | valid_min = 183.15; valid_max =... | - | (hb p. 20) |
| Condensation rate (condensation_rate) | kg m-4 | - | - | (hb p. 25) |
| Saturated water vapor pressure... | Pa | - | - | (hb p. 27) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| C1 constant (Qext=2 assumed) | 0.05789 (unitless) | (hb p. 10) |
| k (droplet spectral shape parameter) | 0.74 (Brenguier et al. 2011) | (hb p. 10) |
| delta_k (assumed uncertainty in k) | 10% | (hb p. 10) |
| delta_beta (assumed uncertainty in beta) | 10% | (hb p. 10) |
| delta_cw (assumed uncertainty in Cw) | 5% | (hb p. 10) |
| LWP error assumption for MWR | +/- 20 g/m2 | (hb p. 10) |
| LWP retrieval lower limit for processing | LWP greater than  0.02 kg/m2 | (hb p. 11) |
| Droplet number concentration QC max threshold | 1e10 drops per cubic meter (10,000 drops per cubic centimeter) | (hb p. 11) |
| Default cloud base height (when unavailable) | 1000 m (cloud_base_height_default) | (hb p. 28) |
| Cloud base temperature threshold for retrieval | warmer than 260 K | (hb p. 11) |
| Optional stricter ice-cloud screening threshold | warmer than 273 K | (hb p. 11) |
| height dimension | 266 levels | (hb p. 18) |
| delta_c2 (global attribute) | 0.05 | (hb p. 28) |


## The data

Verified example: **`sgpndropmfrsrC1.c1`**, file `sgpndropmfrsrC1.c1.20260504.000000.nc`
(2.12 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=4320, `height`=332 |
| Data variables | 36 |
| QC variables | 13 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-05-04T00:00:00 to 2026-05-04T23:59:40 |
| dod version | ndropmfrsr-c1-1.1 |
| process version | vap-ndrop_mfrsr-1.1-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bar_pres` | Pa | time,height | yes | Barometric pressure |
| `beta` | 1 | time | yes | Adiabaticity parameter |
| `cloud_base_height` | m | time | yes | Altitude of cloud base used in retrieval |
| `cloud_base_pressure` | Pa | time | yes | Air pressure of cloud base used in retrieval |
| `cloud_base_temperature` | K | time | yes | Temperature of cloud base used in retrieval |
| `cloud_top_height` | m | time | yes | Altitude of cloud top used in retrieval |
| `drop_number_conc` | m-3 | time | yes | Calculated droplet number concentration |
| `drop_number_conc_adiabatic` | m-3 | time | yes | Droplet number concentration calculated assuming adiabatic cloud layer |
| `drop_number_conc_toterror` | m-3 | time | yes | Total error on calculated droplet number concentration |
| `lwp_adiabatic` | kg m-2 | time | yes | Calculated adiabatic liquid water path |
| `lwp_meas` | kg m-2 | time | yes | Measured liquid water path |
| `optical_depth_instantaneous` | 1 | time | yes | Cloud optical depth instantaneous |
| `temp` | K | time,height | yes | Temperature |
| `cloud_base_type` | 1 | time | - | Type of cloud at cloud base |
| `cloud_thickness` | m | time | - | Cloud thickness |
| `condensation_rate` | kg m-4 | time | - | Condensation rate |
| `height` | m | height | - | Height above mean sea level |
| `saturated_water_vapor_pressure` | Pa | time | - | Saturated water vapor pressure |
| `source_cloud_base` | 1 | time | - | Source for variable:cloud_base_height |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpndropmfrsrC1.c1", "2026-05-04", "2026-05-04")
ds = armlive_open("sgpndropmfrsrC1.c1", "2026-05-04", "2026-05-04", cleanup_qc=True)
```

## Quality control in this product

13 `qc_` companion variables cover 13 of the
36 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may
mean the algorithm refused to converge, or that an input was missing, rather than that
the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgpndropmfrsrC1.c1.20260504.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cloud_base_pressure` | no_source_available | 4320 | 100.0 |
| `drop_number_conc` | Data value for optical_depth_instantaneous not available in... | 4320 | 100.0 |
| `lwp_adiabatic` | Data value for optical_depth_instantaneous not available in... | 4320 | 100.0 |
| `drop_number_conc_adiabatic` | Data value for optical depth not available in input file, data... | 4320 | 100.0 |
| `cloud_base_height` | no_source_available | 4320 | 100.0 |
| `cloud_top_height` | Data value for optical_depth_instantaneous not available in... | 4320 | 100.0 |


Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpndropmfrsrC1.c1", "19980101", "20260924")
```

The report's own note on quality: QC is provided via bit-packed QC flags (e.g., qc_drop_number_conc, qc_beta, qc_cloud_base_height, qc_cloud_base_temperature, qc_cloud_base_pressure, qc_lwp_adiabatic, qc_drop_number_conc_adiabatic, qc_drop_number_conc_toterror), each with per-bit descriptions and Bad/Indeterminate assessments. Key indicators include: qc_drop_number_conc flags absence of observed cloud top or base, out-of-range cloud base temperature/pressure, unrealistically high computed values (greater than 1e10 m-3), and negative beta reset to zero. An uncertainty estimate variable drop_number_conc_toterror and a...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Retrieval restricted to overcast liquid water clouds only | No retrieval output (missing values) during broken-cloud or partly-cloudy periods; optical depth QC bit 5 sets value to missing when cloudfraction less than  0.7 | A retrieval of optical depth from the NFOV2 instrument for broken clouds is planned but not yet available. | (hb p. 7) |
| LWP retrieval only valid for two-channel MWR (mwrret1lilj) | VAP currently only ingests mwrret1lilj datastream; low-LWP cloud accuracy limited | A new mwrret2turner retrieval using a different absorption model for three-channel MWRs is planned for increased accuracy at low LWP, with some... | (hb p. 7) |
| Default cloud base temperature and pressure used when measurements unavailable | Retrieval is less accurate for these time steps; may be flagged via qc_cloud_base_height/temperature bit 5 (no observed cloud base, default used) | Retrieval is more accurate with good measurement-based estimates of cloud base temperature and pressure. | (hb p. 7) |
| Missing cloud top height | beta cannot be calculated; qc_beta bit 3 and qc_drop_number_conc bit 3 set to Indeterminate; adiabatic cloud (beta=0) assumed instead | Adiabatic cloud (beta=0) is assumed when cloud top is unavailable. | (hb p. 11) |
| Missing cloud base height | Both adiabaticity and cloud height must be assumed default (1000 m); qc_cloud_base_height/qc_beta/qc_drop_number_conc bit 5 (or bit4/5) set to Indeterminate | Default cloud_base_height_default = 1000 m is used. | (hb p. 11) |
| Unphysically high droplet number concentration values | drop_number_conc greater than  1e10 m-3 (10,000 cm-3); qc_drop_number_conc bit 9 set to Indeterminate | Flagged as likely an error in observations or retrieval rather than a physically observed value; associated with LWP values near the MWR detection... | (hb p. 11) |
| Low LWP near MWR measurement limit | Unrealistically high drop_number_conc values often correspond to small measured LWP close to instrument sensitivity limit | Retrieval restricted to LWP greater than  0.02 kg/m2. | (hb p. 11) |
| Multiple liquid cloud layers in column | cloud_base_type = 3 (multiple_liquid_layers); retrieval assumes single layer but MWR LWP and MFRSR optical depth integrate over all layers, increasing uncertainty | Users can restrict analysis to cloud_base_type = 1 (single liquid layer) to eliminate these cases. | (hb p. 11) |
| Ice or mixed-phase/supercooled clouds included in retrieval | Retrieval run for all clouds with base temperature warmer than 260 K, an arbitrary threshold that can admit supercooled liquid or ice cloud cases;... | Users can screen for cloud_base_temperature warmer than 273 K to impose a stricter threshold excluding potential ice clouds. | (hb p. 11) |
| Negative beta values from measurement/retrieval uncertainty | Calculated beta less than  0 reset to zero; qc_beta bit 10 and qc_drop_number_conc_adiabatic bit 10 set to Indeterminate | Beta values are constrained to physically valid range 0 to 1 (reset to 0 if negative, reset to 1 if greater than 1). | (hb p. 9) |
| Beta greater than 1 due to measurement mismatch | Calculated beta greater than  1, indicating uncertainties in measurements or mismatch between what different instruments observe | Beta is capped at 1. | (hb p. 9) |
| Missing optical depth input data | qc_cloud_base_height/qc_cloud_top_height/qc_beta/qc_drop_number_conc bit 1 set to Bad; data value set to missing_value | - | (hb p. 20) |
| Ceilometer-based cloud base used when ARSCL unavailable | source_cloud_base flag = 2 (vceil25k first_cbh) instead of ARSCL-based flag = 1; may differ in accuracy from ARSCL cloud boundaries | Cloud base height determined from vceil25k datastream if ARSCL not available. | (hb p. 7) |
| NFOV2-based broken-cloud optical depth retrieval not yet available at all sites | No broken-cloud aerosol-cloud interaction retrieval possible; instrument/data absent at many sites | Capability to use NFOV optical depth datastream will be added when available; NFOV2 instrument does not exist at all sites. | (hb p. 7) |
| Errors in most model inputs (k, beta, Cw) not well constrained | Uncertainty estimate relies on fixed assumed relative errors rather than measured uncertainties for k, beta, Cw | Simple fixed assumptions used: delta_k=10%, delta_beta=10%, delta_cw=5%, following Bennartz (2007). | (hb p. 10) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Bennartz, R. 2007. Global assessment of marine boundary layer cloud droplet number concentration from satellite. JGR-Atmospheres 112(D2): D02201, https://doi.org/10.1029/2006JD007547
- Brenguier, J-L, F Burnet, and O Geoffroy. 2011. Cloud optical thickness and liquid water path – does the k coefficient vary with droplet concentration? ACP 11(18): 9771-9786, https://doi.org/10.5194/acp-11-9771-2011
- Boers, R, and RM Mitchell. 1994. Absorption feedback in stratocumulus clouds: Influence on cloud top albedo. Tellus A 46(3): 229-241, https://doi.org/10.3402/tellusa.v46i3.15476
- McComiskey, A, G Feingold, AS Frisch, DD Turner, MA Miller, JC Chiu, Q Min, and JA Ogren. 2009. An assessment of aerosol-cloud interactions in marine stratus clouds based on surface remote sensing. JGR-Atmospheres...
- Twomey 1977 (cited for aerosol-droplet relationship)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-140.pdf (29 pages, DOE/SC-ARM-TR-140, by L Riihimaki, S McFarlane, C Sivaraman)
- Catalog record: ARM data-source index, `instrument_class_code=ndrop`, read 2026-09-24
- Example file: `sgpndropmfrsrC1.c1.20260504.000000.nc` from `sgpndropmfrsrC1.c1`, 2.12 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
