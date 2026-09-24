---
name: arm-instrument-aos
description: ARM Aerosol Observing System (aos) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpnoaaaosavgC1.b1) and the variable inventory of a real file. Use when working with aos data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Aerosols. Triggers - aos, Aerosol Observing System, sgpnoaaaosavgC1.b1, Aerosols.
---

# AOS - Aerosol Observing System

Aerosol Observing System

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `aos` |
| Handbook | [A. Jefferson](https://www.arm.gov/publications/tech_reports/handbooks/aos_handbook.pdf) |
| Measurement category | Aerosols |
| Primary measurements | Aerosol absorption; Aerosol backscattered radiation; Aerosol particle size; Aerosol scattering; Backscattered radiation; Cloud condensation nuclei |
| Record | 1995-11-03 to 2026-09-22 (active) |
| Datastreams with data | 101 across 27 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, grw, guc, hfe |
| ARM page | https://www.arm.gov/capabilities/instruments/aos |


## Credit

Everything this skill knows about the instrument is the work of **A. Jefferson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A. Jefferson. *aos Instrument Handbook*.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/aos_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures



## The data

Verified example: **`sgpnoaaaosavgC1.b1`**, file `sgpnoaaaosavgC1.b1.20170328.000000.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=24, `bound`=2 |
| Data variables | 55 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 3600 s |
| File time span | 2017-03-28T00:00:00 to 2017-03-28T23:00:00 |
| sampling interval | 1 second |
| averaging interval | 1 hour |
| dod version | noaaaosavg-b1-1.3 |
| process version | ingest-noaaaos-3.1-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Ba_G_Dry_10um_PSAP1W_1` | 1/Mm | time | - | Aerosol light absorption coefficient, green channel, 10 um particle... |
| `Ba_G_Dry_10um_PSAP1W_1_N` | count | time | - | Number of data points used in Ba_G_Dry_10um_PSAP1W_1 computation |
| `Ba_G_Dry_10um_PSAP1W_1_std` | 1/Mm | time | - | Standard deviation of Ba_G_Dry_10um_PSAP1W_1 data this period |
| `Ba_G_Dry_1um_PSAP1W_1` | 1/Mm | time | - | Aerosol light absorption coefficient, green channel, 1 um |
| `Ba_G_Dry_1um_PSAP1W_1_N` | count | time | - | Number of data points used in Ba_G_Dry_1um_PSAP1W_1 computation |
| `Ba_G_Dry_1um_PSAP1W_1_std` | 1/Mm | time | - | Standard deviation of Ba_G_Dry_1um_PSAP1W_1 data this period |
| `Bbs_B_Dry_10um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, blue... |
| `Bbs_B_Dry_10um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_B_Dry_10um_Neph3W_1 computation |
| `Bbs_B_Dry_10um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_B_Dry_10um_Neph3W_1 data this period |
| `Bbs_B_Dry_1um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, blue... |
| `Bbs_B_Dry_1um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_B_Dry_1um_Neph3W_1 computation |
| `Bbs_B_Dry_1um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_B_Dry_1um_Neph3W_1 data this period |
| `Bbs_G_Dry_10um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, green... |
| `Bbs_G_Dry_10um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_G_Dry_10um_Neph3W_1 computation |
| `Bbs_G_Dry_10um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_G_Dry_10um_Neph3W_1 data this period |
| `Bbs_G_Dry_1um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, green... |
| `Bbs_G_Dry_1um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_G_Dry_1um_Neph3W_1 computation |
| `Bbs_G_Dry_1um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_G_Dry_1um_Neph3W_1 data this period |
| `Bbs_R_Dry_10um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, red... |
| `Bbs_R_Dry_10um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_R_Dry_10um_Neph3W_1 computation |
| `Bbs_R_Dry_10um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_R_Dry_10um_Neph3W_1 data this period |
| `Bbs_R_Dry_1um_Neph3W_1` | 1/Mm | time | - | Aerosol backwards-hemispheric light scattering coefficient, red... |
| `Bbs_R_Dry_1um_Neph3W_1_N` | count | time | - | Number of data points used in Bbs_R_Dry_1um_Neph3W_1 computation |
| `Bbs_R_Dry_1um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bbs_R_Dry_1um_Neph3W_1 data this period |
| `Bs_B_Dry_10um_Neph3W_1` | 1/Mm | time | - | Aerosol total light scattering coefficient, blue channel, 10 um... |
| `Bs_B_Dry_10um_Neph3W_1_N` | count | time | - | Number of data points used in Bs_B_Dry_10um_Neph3W_1 computation |
| `Bs_B_Dry_10um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bs_B_Dry_10um_Neph3W_1 data this period |
| `Bs_B_Dry_1um_Neph3W_1` | 1/Mm | time | - | Aerosol total light scattering coefficient, blue channel, 1 um |
| `Bs_B_Dry_1um_Neph3W_1_N` | count | time | - | Number of data points used in Bs_B_Dry_1um_Neph3W_1 computation |
| `Bs_B_Dry_1um_Neph3W_1_std` | 1/Mm | time | - | Standard deviation of Bs_B_Dry_1um_Neph3W_1 data this period |


_20 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpnoaaaosavgC1.b1", "2017-03-28", "2017-03-28")
ds = armlive_open("sgpnoaaaosavgC1.b1", "2017-03-28", "2017-03-28", cleanup_qc=True)
```

This datastream carries 55 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("sgpnoaaaosavgC1.b1", start, end,
                  keep_variables=["Ba_G_Dry_10um_PSAP1W_1", "Ba_G_Dry_10um_PSAP1W_1_N", "Ba_G_Dry_10um_PSAP1W_1_std"])
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `flags_CMDL`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpnoaaaosavgC1.b1", "19951103", "20260923")
```

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
|  |  | - | - |


## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/aos_handbook.pdf (32 pages, by A. Jefferson)
- Catalog record: ARM data-source index, `instrument_class_code=aos`, read 2026-09-23
- Example file: `sgpnoaaaosavgC1.b1.20170328.000000.nc` from `sgpnoaaaosavgC1.b1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
