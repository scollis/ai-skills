---
name: arm-instrument-flask
description: ARM Flask Samplers for Carbon Cycle Gases and Isotopes (flask) - handbook-derived instrument reference. Measurement principle, reported quantities (CO2 mixing ratio, CH4 mixing ratio, N2O mixing ratio, CO mixing ratio, SF6 mixing ratio, H2 mixing ratio, delta13C of CO2, delta18O of CO2), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpghgisoflaskC1.b1) and the variable inventory of a real file. Use when working with flask data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Carbon. Triggers - flask, Flask Samplers for Carbon Cycle Gases and Isotopes, sgpghgisoflaskC1.b1, CO2 mixing ratio, CH4 mixing ratio, N2O mixing ratio, CO mixing ratio, SF6 mixing ratio, H2 mixing ratio, Atmospheric Carbon, Sherpa 70 (surface measurements).
---

# FLASK - Flask Samplers for Carbon Cycle Gases and Isotopes

FLASK collects discrete whole-air samples in flasks at a 60 m tower (surface, weekly) and from a chartered aircraft (approximately weekly, up to twelve elevations) at the ARM SGP site, which NOAA ESRL analyzes for CO2, CH4, CO, N2O, H2, SF6 mixing ratios and stable isotope ratios of CO2 and CH4.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `flask` |
| Handbook | [DOE/SC-ARM-TR-181 / S Biraud / March 2016](https://www.arm.gov/publications/tech_reports/handbooks/flask_handbook.pdf) |
| Measurement category | Atmospheric Carbon |
| Manufacturer / model | Sherpa 70 (surface measurements), Sherpa 90 and Sherpa 80 (aircraft measurements) |
| Primary measurements | Carbon dioxide (CO2) concentration; Carbon monoxide (CO) Concentration; Isotope ratio; Methane concentration; Nitrogen oxides; Trace gas concentration |
| Record | 2002-04-02 to 2024-09-01 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/flask |


## Credit

Everything this skill knows about the instrument is the work of **S Biraud** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Biraud. *Flask Samplers for Carbon Cycle Gases and Isotopes (FLASK) Instrument Handbook*, DOE/SC-ARM-TR-181, March 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/flask_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Air samples are collected into pressurized flasks (surface flasks from a 60 m tower inlet, aircraft flasks from a community inlet at multiple elevations) and shipped to NOAA ESRL for analysis. CO2 is measured by nondispersive infrared absorption; CH4 by gas chromatography with flame ionization detection; CO and H2 by gas chromatography with mercuric oxide reduction detection; N2O and SF6 by gas chromatography with electron capture detection. Stable isotopes (delta13C and delta18O of CO2, delta13C of CH4) are measured by dual inlet isotope-ratio mass spectrometry at the INSTAAR Stable Isotope Laboratory. Isotopic ratios are expressed as deviations (delta notation) from an agreed-upon reference standard (e.g., Pee Dee Belemnite for carbon/oxygen in CO2, VSMOW for water-referenced ratios), in per mil units. All mixing-ratio measurements are referenced to WMO standard scales maintained by the Central Calibration Laboratory at NOAA/ESRL.

**Siting.** Surface samples collected from one of two 60 m inlets in the PGS shed at the ARM SGP Central Facility, co-located with PGS (Precision Gas System) continuous CO2 measurements at 2 m, 4 m, 25 m, and 60 m, and eddy covariance flux measurements (CO2FLX) at 4 m. Aircraft samples collected from a community inlet at multiple elevations from a chartered aircraft, with collection flight path centered over the tower where surface samples are collected.

**Sampling.** native rate Surface: weekly (usually Thursdays at 2pm local time), each flask sampled for about 2 minutes; Aircraft: approximately weekly, sampled at up to twelve elevations, each flask sampled for about 2 minutes; reported every 1 minute; averaging reporting_interval_comment: The time assigned to each data point indicates the beginning of any period of averaging data. (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| CO2 mixing ratio | ppm | 250 - 520 ppm | 0.069 ppm (one-sigma) for primary standards;... | - | (hb p. 12) |
| CH4 mixing ratio | ppb | 300 - 5,000 ppb | 1 ppb (primary standards) | - | (hb p. 12) |
| N2O mixing ratio | ppb | 260 - 370 ppb | standard deviation of residuals is 0.33 ppb;... | - | (hb p. 12) |
| CO mixing ratio | ppb | 30 - 1000 ppb | 2.6 ppb (14 primary standards) | - | (hb p. 12) |
| SF6 mixing ratio | ppt | 2-20 ppt | analysis repeatability typically less than 0.3%... | - | (hb p. 12) |
| H2 mixing ratio | ppt | 140 - 1,200 ppt | bias of the scale of 2-3 ppb in the atmospheric... | - | (hb p. 12) |
| delta13C of CO2 | per mil (‰) | -7.5 to -9 per mil | - | - | (hb p. 13) |
| delta18O of CO2 | per mil (‰) | -2 to +2 per mil | - | - | (hb p. 13) |
| delta13C of CH4 | per mil (‰) | standardized isotopic calibration in... | - | - | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Reporting interval | 1 minute | (hb p. 7) |
| Surface flask volume | 2.5 liters | (hb p. 6) |
| Surface flask sampling duration | about 2 minutes | (hb p. 6) |
| Surface flask pressurization | 40 PSI | (hb p. 6) |
| Aircraft flask volume | 0.75 liters | (hb p. 6) |
| Aircraft flask sampling duration | about 2 minutes | (hb p. 6) |
| Aircraft flask pressurization | 40 PSI | (hb p. 6) |
| Input Voltage | 110-120V, at 50-60 Hz | (hb p. 14) |
| Input Current (Typical) | 500 mA | (hb p. 14) |
| Input Current (Max) | 2A | (hb p. 14) |
| CO2 range | 250 - 520 ppm | (hb p. 13) |
| CH4 range | 300 - 5,000 ppb | (hb p. 13) |
| N2O range | 260 - 370 ppb | (hb p. 13) |
| CO range | 30 - 1000 ppb | (hb p. 13) |
| SF6 range | 2-20 ppt | (hb p. 13) |
| H2 range | 140 - 1,200 ppt | (hb p. 13) |
| delta13C of CO2 range | -7.5 to -9 per mil | (hb p. 13) |
| delta18O of CO2 range | -2 to +2 per mil | (hb p. 13) |
| CO2 WMO scale currently used | X2007 | (hb p. 15) |
| CH4 WMO scale currently used | X2004A | (hb p. 15) |
| N2O WMO scale currently used | X2006A | (hb p. 15) |
| CO WMO scale currently used | X2014A | (hb p. 15) |
| SF6 WMO scale currently used | X2014 | (hb p. 15) |
| H2 WMO scale currently used | X2009 | (hb p. 15) |
| delta13C of CO2 scale | VPDB-CO2 | (hb p. 15) |
| delta18O of CO2 scale | VPDB-CO2 | (hb p. 15) |


_1 further specification rows are in the handbook._

## The data

Verified example: **`sgpghgisoflaskC1.b1`**, file `sgpghgisoflaskC1.b1.20240901.191758.nc`
(0.03 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1 |
| Data variables | 97 |
| QC variables | 44 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2024-09-01T19:17:58 to 2024-09-01T19:17:58 |
| dod version | ghgisoflask-b1-1.0 |
| process version | ingest-ghgisoflask-1.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `C2Br2F4` | ppt | time | yes | Dibromotetrafluoroethane (C2Br2F4) concentration |
| `C2Cl4` | ppt | time | yes | Tetrachloroethene (C2Cl4) concentration |
| `C2H2` | ppt | time | yes | Acetylene (C2H2) concentration |
| `C2H3Cl3` | ppt | time | yes | Methyl chloroform (C2H3Cl3) concentration |
| `C2H6` | ppt | time | yes | Ethane (C2H6) concentration |
| `C3H8` | ppt | time | yes | Propane (C3H8) concentration |
| `C4H10` | ppt | time | yes | N-Butane (C4H10) concentration |
| `C5H12` | ppt | time | yes | N-Pentane (C5H12) concentration |
| `C6H6` | ppt | time | yes | Benzene (C6H6) concentration |
| `CBrClF2` | ppt | time | yes | Bromochlorodifluoromethane (CBrClF2) concentration |
| `CBrF3` | ppt | time | yes | Bromotrifluoromethane (CBrF3) concentration |
| `CCl4` | ppt | time | yes | Carbon Tetrachloride (CCl4) concentration |
| `CFC_11` | ppt | time | yes | Trichlorofluoromethane (CCl3F) concentration |
| `CFC_113` | ppt | time | yes | Trichlorotrifluoroethane (C2Cl3F3) concentration |
| `CFC_115` | ppt | time | yes | Chloropentafluoroethane (C2ClF5) concentration |
| `CFC_12` | ppt | time | yes | Difluorodichloromethane (CCl2F2) concentration |
| `CH2Br2` | ppt | time | yes | Dibromomethane (CH2Br2) concentration |
| `CH2Cl2` | ppt | time | yes | Dichloromethane (CH2Cl2) concentration |
| `CH3Br` | ppt | time | yes | Methyl bromide (CH3Br) concentration |
| `CH3I` | ppt | time | yes | Methyl iodide (CH3I) concentration |
| `CH4` | ppb | time | yes | Methane (CH4) concentration |
| `CH4C13` | 1/1E6 | time | yes | Isotopic ratio of C13 in CH4 |
| `CHBr3` | ppt | time | yes | Bromoform (CHBr3) concentration |
| `CHCl3` | ppt | time | yes | Chloroform (CHCl3) concentration |
| `CO` | ppb | time | yes | Carbon monoxide (CO) concentration |
| `CO2` | ppm | time | yes | Carbon dioxide (CO2) concentration |
| `CO2C13` | 1/1E6 | time | yes | Isotopic ratio of C13 in CO2 |
| `CO2C14` | 1/1E6 | time | yes | Isotopic ratio of C14 in CO2 |
| `CO2O18` | 1/1E6 | time | yes | Isotopic ratio of O18 in CO2 |
| `COS` | ppt | time | yes | Carbonyl sulphide (COS) concentration |


_19 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "sgpghgisoflaskC1.b1",
                             "start": "2024-09-01", "end": "2024-09-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpghgisoflaskC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpghgisoflaskC1.b1", "2024-09-01", "2024-09-01")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpghgisoflaskC1.b1", "2024-09-01", "2024-09-01"))   # cite what you pulled
```

This datastream carries 97 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpghgisoflaskC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["C2Br2F4", "C2Cl4", "C2H2", "qc_C2Br2F4", "qc_C2Cl4", "qc_C2H2"],
                                cleanup_qc=True)
```

## Quality control in this datastream

44 `qc_` companion variables cover 44 of the
97 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_CO2"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("CO2", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["CO2", "CH4", "CO"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpghgisoflaskC1.b1.20240901.191758.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `SF6_hats` | Value is equal to missing_value. | 1 | 100.0 |
| `HFC_125` | Value is equal to missing_value. | 1 | 100.0 |
| `C6H6` | Value is equal to missing_value. | 1 | 100.0 |
| `CBrClF2` | There was a sample collection or measurement problem and the... | 1 | 100.0 |
| `CH2Br2` | Value is equal to missing_value. | 1 | 100.0 |
| `CHBr3` | Value is equal to missing_value. | 1 | 100.0 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpghgisoflaskC1.b1", "20020402", "20260923")
```

The handbook's own note on data quality: A 3-column quality control flag is used: column 1 is a REJECTION flag (alphanumeric other than a period indicates a sample with obvious problems, should not be interpreted); column 2 is a SELECTION flag (alphanumeric other than a period indicates a sample likely valid but not meeting selection criteria for a particular investigation); column 3 is an INFORMATION flag (alphanumeric other than a period provides additional information; a 'P' indicates preliminary, not yet examined by the PI, removed once quality determined). Samples are collected in pairs (surface, and aircraft prior to 2006);...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Bad pairs (surface/aircraft flask pair mismatch) | Pair difference greater than 0.5 ppm between two flasks collected together; flagged as high (+..) or low (-..) member of bad pair, rejected or retained depending on era | From 1989 to present both members of bad pairs automatically rejected; through 1988 one or both members sometimes retained if within +/- 3 residual... | (hb p. 11) |
| Outlier samples relative to fitted curve | Value deviates greater than 3 sigma from a fitted curve; flagged .X. (automatic) or .Z. (manual) | Flagged as outlier in SELECTED category; manual flagging (.Z.) used to prevent distortion of the curve used for automated data selection | (hb p. 11) |
| Off-scale or broken flask | Measurement rejected with * . . flag | Rejected; not used in data analysis | (hb p. 11) |
| Sampling or analysis error | Flagged N.. (sampling/analysis error) or A.. (analysis error) | Rejected | (hb p. 11) |
| Methods test samples | Flagged T.. for samples collected as part of a methods test | Not used in data analysis | (hb p. 11) |
| Preliminary/unreviewed data | 'P' in third column of QC flag indicates measurement result is preliminary and has not yet been carefully examined by the PI | P flag removed once quality of measurement has been determined | (hb p. 10) |
| b1 to c1 reprocessing / recalibration drift | b1-level annual files updated to c1-level based on recalibrations, typically midsummer of following year; mixing or isotopic ratios recalculated if reference gases found to be drifting | Discard previous b1 files once c1 update occurs; c1 data essentially final but may be occasionally reprocessed based on retrospective analyses of... | (hb p. 3) |
| H2 primary standard drift / scale bias | Growing H2 mole fraction detected in two of the primary standards, suggesting a bias of the scale of 2-3 ppb in the atmospheric range | Will induce a revision of the WMO scale in the next scale update | (hb p. 8) |
| delta13C of CH4 calibration not yet standardized | Range/uncertainty for delta13C of CH4 listed as 'standardized isotopic calibration in development'; WMO scale listed as TBD | - | (hb p. 13) |
| Measurement range limited by primary calibration standard range | Values outside the primary standard range (e.g., CO2 250-520 ppm, CH4 300-5000 ppb, etc.) fall outside optimum calibration range | Range is dictated by the range of primary calibration standard used for each species | (hb p. 7) |
| Manual triggering dependency | Gaps or irregular timing in weekly sampling record since sampling is triggered manually by technician (surface) or pilot (aircraft) rather than automated on fixed schedule | - | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Each species referenced to its respective WMO/NOAA ESRL or MPI-BGC calibration scale via analytical technique specific to species (NDIR for CO2, GC-FID for CH4, GC with mercuric oxide reduction for CO and H2, GC-ECD for N2O and SF6, dual inlet isotope-ratio mass spectrometry for stable isotopes); calibration results... (hb p. 10) |
| Calibration interval | Primary standards calibrated at regular intervals, between 1 and 2 years, by the ESRL manometric system (hb p. 10) |
| Traceability | Results are traceable to the SI unit "amount of substance fraction"; equipment traceable to national standards for mass, temperature, pressure, and amount of substance fraction (O2 in N2) (hb p. 10) |
| Routine maintenance | Pumps diaphragm is replaced when needed (hb p. 10) |
| Maintenance interval | as needed (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: AOS, AOSGHG, PGS, PGSISO, CO2FLX.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `CCL` | Central Calibration Laboratory |
| `CH4` | methane |
| `CO` | carbon monoxide |
| `CO2` | carbon dioxide |
| `ESRL` | Earth System Research Laboratory |
| `GAW` | Global Atmosphere Watch |
| `GHG` | greenhouse gas |
| `H2` | hydrogen |
| `INSTARR` | Institute of Arctic and Alpine Research |
| `LBNL` | Lawrence Berkeley National Laboratory |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `N2O` | nitrous oxide |
| `SF6` | sulfur hexafluoride |
| `SGP` | Southern Great Plains |


### References the handbook cites

- Biraud, S. C., Torn, M. S., Smith, J. R., Sweeney, C., Riley, W. J., and Tans, P. P.: A multiyear record of airborne CO2 observations in the US Southern Great Plains, Atmos. Meas. Tech., 6, 751-763,...
- Zhao, C., and P.P. Tans (2006), Estimating uncertainty of the WMO Mole Fraction Scale for carbon dioxide in air, J. Geophys. Res. 111, D08S09, doi: 10.1029/2005JD006003.
- Zhao, C., P.P. Tans and K.W. Thoning (1997), A high precision manometric system for absolute calibrations of CO2 in dry air. Journal of Geophysical Research 102(D5):5885-5894
- Dlugokencky, E. J., et al. (2005), Conversion of NOAA atmospheric dry air CH4 mole fractions to a gravimetrically prepared standard scale, J. Geophys. Res., 110, D18306, doi:10.1029/2005JD006035.
- Novelli et al., Development and evaluation of a gravimetric reference scale for measurements of atmospheric carbon monoxide, 1991, JGR, 96, 13109-13121, 1991.
- Hall et al., The NOAA nitrous oxide standard scale for atmospheric observations, JGR, 112, D09305, doi:10.1029/2006JD007954, 2007.
- Trolier, M., J.W.C. White, P.P. Tans, K.A. Masarie and P.A. Gemery, Monitoring the isotopic composition of atmospheric CO2: measurements from the NOAA Global Air Sampling Network, JGR 101, 25,897-25,916 (1996).

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/flask_handbook.pdf (17 pages, DOE/SC-ARM-TR-181, by S Biraud)
- Catalog record: ARM data-source index, `instrument_class_code=flask`, read 2026-09-23
- Example file: `sgpghgisoflaskC1.b1.20240901.191758.nc` from `sgpghgisoflaskC1.b1`, 0.03 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
