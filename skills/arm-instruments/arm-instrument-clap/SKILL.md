---
name: arm-instrument-clap
description: ARM Continuous Light Absorption Photometer (clap) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (pvcaosclap3wM1.c1) and the variable inventory of a real file. Use when working with clap data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - clap, Continuous Light Absorption Photometer, pvcaosclap3wM1.c1, Aerosols.
---

# CLAP - Continuous Light Absorption Photometer

Continuous Light Absorption Photometer

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 35 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `clap` |
| Handbook | [E Andrews](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-280.pdf) |
| Measurement category | Aerosols |
| Primary measurements | Aerosol absorption; Aerosol extinction; Aerosol optical properties |
| Record | 2011-03-01 to 2026-09-21 (active) |
| Datastreams with data | 14 across 5 sites |
| Sites | mao, nsa, pgh, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/clap |


## Credit

Everything this skill knows about the instrument is the work of **E Andrews** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> E Andrews. *clap Instrument Handbook*.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-280.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures



## The data

Verified example: **`pvcaosclap3wM1.c1`**, file `pvcaosclap3wM1.c1.20130621.000000.cdf`
(0.1 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 16 |
| QC variables | 3 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2013-06-21T00:00:00 to 2013-06-21T23:59:00 |
| sampling interval | 1 second |
| averaging interval | not averaged |
| dod version | aosclap3w-c1-1.3 |
| process version | ingest-aosmqc-1.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Ba_B_CLAP3W_1` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal blue wavelength at dry... |
| `Ba_G_CLAP3W_1` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal green wavelength at dry... |
| `Ba_R_CLAP3W_1` | 1/Mm | time | yes | Aerosol light absorption coefficient, nominal red wavelength at dry... |
| `impactor_setting` | um | time | - | Impactor setting in terms of aerodynamic diameter cut off |
| `sample_length` | m | time | - | AOS Ba_B_CLAP3W_1 (NOAA) sample length, needed to calculate Beers Law |
| `time` | - | time | - | Time offset from midnight |
| `transmittance_B` | unitless | time | - | AOS Ba_B_CLAP3W_1 transmittance, blue channel |
| `transmittance_G` | unitless | time | - | AOS Ba_G_CLAP3W_1 transmittance, green channel |
| `transmittance_R` | unitless | time | - | AOS Ba_R_CLAP3W_1 transmittance, red channel |


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
                     params={"user": f"{user}:{token}", "ds": "pvcaosclap3wM1.c1",
                             "start": "2013-06-21", "end": "2013-06-21", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./pvcaosclap3wM1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "pvcaosclap3wM1.c1", "2013-06-21", "2013-06-21")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("pvcaosclap3wM1.c1", "2013-06-21", "2013-06-21"))   # cite what you pulled
```

## Quality control in this datastream

3 `qc_` companion variables cover 3 of the
16 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_Ba_B_CLAP3W_1"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("Ba_B_CLAP3W_1", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["Ba_B_CLAP3W_1", "Ba_G_CLAP3W_1", "Ba_R_CLAP3W_1"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (pvcaosclap3wM1.c1.20130621.000000.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `Ba_B_CLAP3W_1` | Value is equal to missing_value. | 239 | 16.5972 |
| `Ba_G_CLAP3W_1` | Value is equal to missing_value. | 239 | 16.5972 |
| `Ba_R_CLAP3W_1` | Value is equal to missing_value. | 239 | 16.5972 |
| `Ba_B_CLAP3W_1` | transmittance_B less than  transmittance_minimum_warning | 183 | 12.7083 |
| `Ba_G_CLAP3W_1` | transmittance_G less than  transmittance_minimum_warning | 183 | 12.7083 |
| `Ba_R_CLAP3W_1` | transmittance_R less than  transmittance_minimum_warning | 183 | 12.7083 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("pvcaosclap3wM1.c1", "20110301", "20260923")
```

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Filter loading / multiple scattering artifact | Absorption coefficient changes systematically as transmittance (Tr) decreases from 1.0 toward 0.7, requiring correction of raw signal | Use optical configuration and filter media comparable to PSAP to allow use of the Bond et al. (1999) correction scheme for errors caused by filter... | (hb p. 7) |
| High ambient dewpoint / humidity effect on filter | Cellulose fiber backing of filter takes up water under high humidity, altering transmittance/absorption readings | CLAP has internal heater to lower sample relative humidity inside the instrument | (hb p. 8) |
| Vacuum source oscillations/disruptions | Filter oscillates physically, causing noisy or erratic transmittance/absorption measurements | Use a stable vacuum source; note oscillations may affect measurements | (hb p. 10) |
| Filter material contamination inside instrument (fibers stuck to CLAP top/holes) | Obstructed flow paths or spurious optical readings after filter change | Clean with ethanol and lintless tissue; blow out holes gently with compressed air during filter change | (hb p. 12) |
| Lamp error / LED problem | Flags bit 0x0100 set; blinking red indicator lamp; flag value shown as nonzero hex (e.g., 0100) in CPD status window | Error condition must be corrected before continuing sampling | (hb p. 9) |
| Low transmittance warning (Tr below 0.7) | Flags variable non-zero, warning condition noted in CPD Client screen; transmittance flag bits 0x0040,0x0010,0x0004 set | Investigate; spot should be advanced/filter changed when Tr reaches 0.7 (SpotAdvanceTR) | (hb p. 9) |
| Very low transmittance (Tr less than  0.5) - severe filter loading | Flags bits 0x0080, 0x0020, 0x0008 set (transmittance below 0.5 for R, G, B channels) | None specified beyond flag reporting | (hb p. 24) |
| Case temperature unstable | Flag bit 0x0400 set; case temperature deviates outside setpoint +/-1.0 C window | See Appendix B troubleshooting: raise setpoint, expand acceptable deviation, remove side panels for cooling, or add external insulation (e.g.,... | (hb p. 24) |
| Temperature error (inlet or block) | Flag bit 0x0200 set | None specified beyond flag reporting | (hb p. 24) |
| Flow error | Flag bit 0x0002 set; flowrate reading anomalous or zero | None specified beyond flag reporting | (hb p. 24) |
| Flow disabled due to system bypass or other condition | Status line shows 'FLOW DISABLED ON SPOT X' or 'FLOW DISABLED WITH PENDING SPOT X'; no flow through active spot | Override using 'Set Flow Override' CLAP menu option once condition passes | (hb p. 18) |
| Filter deformation/flexing after filter change or flow onset | Normalized intensities distort away from 1.0 on unsampled spots for even/odd channels depending on reference in use; visible via Intensity Filter Start Ratio deviating from 1.0 | Instrument waits through stabilization period before recording initial intensities and beginning normal sampling | (hb p. 15) |
| Two filters stuck together during filter change | Flowrate after filter change lower than before the change | Repeat the filter change to check for two stuck filters if flow is lower than prior exposed filter | (hb p. 13) |
| Non-linear flowmeter response requiring dual calibration | Discrepancy between internal calibration flow reading and true flow rate, especially away from nominal 1.0 slpm operating point; residual fit error (e.g., 0.012 slpm at 1.0 slpm) | Apply internal third-degree polynomial calibration plus a 'trimming' multiplier in cpd.conf to correct residual error at nominal flow | (hb p. 31) |
| High-altitude station volumetric vs mass flow discrepancy | Mass flow reading well below 1.0 slpm at high-altitude sites even though volumetric flow is correct at 1.0 lpm | Calculate proper standard flow (Vstd) using station T and P via ideal gas law to achieve true 1.0 lpm volumetric flow | (hb p. 8) |
| No real-time clock in CLAP | Data records lack instrument-generated timestamps | Logging computer must add timestamp to data reports | (hb p. 16) |
| Loss of intensity/filter baseline data after power interruption | CLAP does not store intensity readings when a new filter is installed after power loss; resumed sampling on old spot could use stale reference | Recommended procedure for manual operation is always to start a new spot after a power interruption | (hb p. 15) |
| O-ring-induced diffuse/variable spot edge (early design issue, resolved) | Filter spot edges would appear diffuse and variable in area if o-rings were used | O-rings eliminated from final design; precisely defined filter spot areas used instead | (hb p. 8) |
| Improper top/bottom seal torque causing leaks | Incomplete sealing of two assemblies leading to flow leakage past filter | Use torque driver (clicks at correct torque, 2.5 N-m) rather than thumbscrews | (hb p. 8) |
| Blower block orientation error | Incorrect sampling flow characteristics if nephelometer blower bypass block is not oriented with pick-off fitting closer to nephelometer sampling volume | Match orientation to figure showing correct pick-off fitting placement | (hb p. 9) |
| Reserved/undefined flag bits | Five most-significant bits of 16-bit flag value always shown as zero; reserved for future correction flags (CTS, Bond, Weiss corrections) | None specified; reserved for later data processing | (hb p. 24) |


## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-280.pdf (35 pages, by E Andrews)
- Catalog record: ARM data-source index, `instrument_class_code=clap`, read 2026-09-23
- Example file: `pvcaosclap3wM1.c1.20130621.000000.cdf` from `pvcaosclap3wM1.c1`, 0.1 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
