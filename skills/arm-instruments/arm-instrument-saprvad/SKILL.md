---
name: arm-instrument-saprvad
description: ARM Scanning ARM Precipitation Radar (SAPR) Velocity Azimuth Display (saprvad) - handbook-derived instrument reference. Measurement principle, reported quantities (ZDR, phiDP, KDP, rhoHV, NCP), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpxsaprvadI6.c1) and the variable inventory of a real file. Use when working with saprvad data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties; Derived Quantities and Models. Triggers - saprvad, sgpxsaprvadI6.c1, ZDR, phiDP, KDP, Cloud Properties, Derived Quantities and Models, Advanced Radar Corporation (ARC) pedestal, Pulse Systems Technology transmitter, rhoHV, C band, Ka band.
---

# SAPRVAD - Scanning ARM Precipitation Radar (SAPR) Velocity Azimuth Display

C-SAPR is a scanning polarimetric Doppler weather radar operating at C band (6.25 GHz) that transmits simultaneous H and V polarizations to measure reflectivity, polarimetric variables, and Doppler mean velocity/spectrum width via RHI, PPI, and vertical-pointing scans, from which VAD wind profiles can be derived.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 19 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `saprvad` |
| Handbook | [DOE/SC-ARM/TR-121 / K Widener, N Bharadwaj / November 2012](https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf) |
| Measurement category | Cloud Properties; Derived Quantities and Models |
| Manufacturer / model | Advanced Radar Corporation (ARC) pedestal; Pulse Systems Technology transmitter; NCAR Hi-Q receiver; TITAN processing software |
| Primary measurements | Horizontal wind |
| Record | 2010-12-14 to 2019-02-26 (retired) |
| Datastreams with data | 4 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/saprvad |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj. *C-Band Scanning ARM Precipitation Radar (C-SAPR) Handbook*, DOE/SC-ARM/TR-121, November 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `saprvad`, ARM links no handbook to this class. The facts below come from the **C-Band Scanning ARM Precipitation Radar** (`csapr`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `saprvad` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

C-SAPR is a coherent-on-receive dual-polarization Doppler radar that transmits pulses simultaneously in horizontal (H) and vertical (V) polarization from a 350-kW magnetron transmitter and measures the returned power and phase to derive reflectivity and polarimetric variables. The Doppler mean velocity (V) and spectrum width (W) are computed from the linear channel using the coherent-on-receive NCAR Hi-Q receiver processed with TITAN software. Reflectivity (Z) is computed from the meteorological radar range equation using system parameters such as wavelength, range, received power, losses, antenna gain, the dielectric factor of water (Kw^2), and antenna beamwidth. Dual-polarization measurements (ZDR, phiDP, KDP, rhoHV) exploit the oblate shape of raindrops to characterize hydrometeor type and estimate rainfall independent of purely reflectivity-based empirical models. Scan strategies alternate between RHI, PPI (360-degree azimuth sweeps at incrementing elevations), and vertical pointing modes to build volumetric or profile views of the atmosphere.

**Siting.** Deployed at ARM SGP Central Facility near Nardin, OK (near the triangular array of X-SAPRs) and at ARM TWP site on Manus Island, Papua New Guinea (Lombrum). The C-SAPR is limited to scanning 92 degrees in elevation for RHI scans; PPI scans sweep 360 degrees in azimuth at incrementing elevations; vertical pointing mode is used during part of the measurement period to obtain zenith cloud profiles.

**Sampling.** native rate Receiver sampling rate 40 MHz; PRF 200 Hz–2.7 kHz (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| V (Doppler mean velocity) | - | - | - | - | (hb p. 6) |
| W (Doppler spectrum width) | - | - | - | - | (hb p. 6) |
| Z (log channel reflectivity corrected for clutter) | dBZ | - | - | - | (hb p. 6) |
| ZDR (differential reflectivity) | dB | - | - | - | (hb p. 6) |
| phiDP (differential phase) | degrees | - | - | - | (hb p. 6) |
| KDP (specific differential phase) | deg/km | - | - | - | (hb p. 6) |
| rhoHV (dual-polarization correlation magnitude) | - | - | - | - | (hb p. 6) |
| NCP (normalized coherent power) | - | - | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Transmitter type | Magnetron | (hb p. 9) |
| Center frequency | 6.25 GHz | (hb p. 9) |
| Peak power output | 350 kW | (hb p. 9) |
| Pulse width | 200 ns–2 µs | (hb p. 9) |
| Polarization | dual polarization, simultaneous H and V | (hb p. 9) |
| Maximum duty cycle | 0.1% | (hb p. 9) |
| PRF | 200 Hz–2.7 kHz | (hb p. 9) |
| Transmitter manufacturer | Pulse Systems Technology | (hb p. 9) |
| Receiver type | coherent-on-receive, dual channel digital Hi-Q | (hb p. 9) |
| Receiver dynamic range | greater than  80 dB | (hb p. 9) |
| Receiver noise figure | 2.8 dB | (hb p. 9) |
| Receiver sampling rate | 40 MHz | (hb p. 9) |
| Decimation factor | Adjustable | (hb p. 9) |
| Video bandwidth | Adjustable | (hb p. 9) |
| Processing software | TITAN | (hb p. 9) |
| Receiver manufacturer | NCAR | (hb p. 9) |
| Antenna type | direct feed parabolic reflector | (hb p. 10) |
| Antenna diameter | 2.4 m | (hb p. 10) |
| 3 dB beam width | 0.9° | (hb p. 10) |
| Antenna gain | 45.1 dBi | (hb p. 10) |
| Cross polarization isolation | -32 dB | (hb p. 10) |
| 2-way radome loss | less than 1.0 dB | (hb p. 10) |
| Pedestal type | azimuth over elevation | (hb p. 10) |
| Azimuth scan rate | up to 36°/s | (hb p. 10) |
| Elevation scan rate | up to 30°/s | (hb p. 10) |
| Pedestal manufacturer | ARC | (hb p. 10) |


## The data

Verified example: **`sgpxsaprvadI6.c1`**, file `sgpxsaprvadI6.c1.20190223.000000.nc`
(0.35 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=91, `height`=101 |
| Data variables | 9 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 600 s |
| File time span | 2019-02-23T00:00:04 to 2019-02-23T17:30:04 |
| dod version | v1.0 |
| process version | EVAl-0.5 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `direction` | degree | time,height | - | Horizontal wind direction |
| `height` | meter | height | - | Height above ground |
| `speed` | m/s | time,height | - | Horizontal wind speed |
| `time` | - | time | - | Time offset from midnight |
| `u_wind` | m/s | time,height | - | Eastward wind component |
| `v_wind` | m/s | time,height | - | Northward wind component |


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
                     params={"user": f"{user}:{token}", "ds": "sgpxsaprvadI6.c1",
                             "start": "2019-02-23", "end": "2019-02-23", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpxsaprvadI6.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpxsaprvadI6.c1", "2019-02-23", "2019-02-23")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpxsaprvadI6.c1", "2019-02-23", "2019-02-23"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpxsaprvadI6.c1", "20101214", "20260924")
```

The handbook's own note on data quality: Data Quality Office provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting C-SAPR data quality. Plots of reflectivity, Doppler radial velocity, and dual-polarization variables serve as indicators of whether the system is operational. Instrument mentors review data routinely (daily Monday-Friday) and on request from Site Operations, site scientist team, ARM data translator, data user, or automated built-in test email notifications. Site scientist/Data Quality Office assessments were 'to be determined' at time of writing.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Elevation scan limitation for RHI | RHI scans truncated; cannot cover full 180-degree horizon-to-horizon elevation range, limited to 92 degrees | - | (hb p. 11) |
| No netCDF ingestion / proprietary MDV format | Data files are in NCAR TITAN MDV format rather than netCDF, requiring TITAN's PrintMdv program to read/dump data | Retrieve sample file from ARM Data Archive and run TITAN 'PrintMdv' program | (hb p. 12) |
| Reflectivity requires clutter correction | Log channel reflectivity (Z) reported is already 'corrected for clutter', implying raw returns are contaminated by ground clutter | - | (hb p. 12) |
| Dielectric factor assumption for reflectivity computation | Reflectivity values depend on an assumed water dielectric factor (Kw^2 = 0.93 at 0°C) which varies with frequency and temperature; using an incorrect assumption biases dBZ | - | (hb p. 14) |
| Single-polarization ambiguity resolved partly by dual-pol variables | Without dual-pol variables, hydrometeor type and rainfall rate estimates rely on empirically derived models that differ by climatic regime, introducing regional bias | Use dual-polarization variables (ZDR, phiDP, KDP, rhoHV) to better characterize hydrometeor type/rainfall | (hb p. 14) |
| Velocity/range aliasing not yet corrected | Raw C-SAPR moments are not yet dealiased for velocity or range; observed Doppler velocity field may show folding/aliasing artifacts | Planned 'corrected moments' value-added product will include velocity and range dealiasing and water vapor attenuation correction (not yet available) | (hb p. 16) |
| Water vapor attenuation not yet corrected | Reflectivity/received power may be biased low along path due to uncorrected water vapor attenuation | Planned corrected-moments VAP will include water vapor attenuation correction | (hb p. 16) |
| No value-added products currently available | Users must work with raw MDV moments; no gridded or corrected product exists yet at time of writing | Planned VAPs (corrected moments, then gridded moments with cloud boundaries) are in development | (hb p. 16) |
| System operational status indicator via visual inspection | Operational health assessed by inspecting plots of reflectivity, Doppler radial velocity, and dual-polarization variables; anomalies would appear as discontinuities or missing structure in... | Routine instrument mentor review, DQ Explorer, DQ Plot Browser, NCVweb tools | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | To be included in manufacturer's documentation and the ARM Common Calibration database; contact instrument mentor for information (hb p. 17) |
| Routine maintenance | See NCAR TITAN documentation for operation and maintenance (hb p. 17) |
| Maintenance interval | Routine mentor review of data usually daily Monday–Friday (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: X-SAPR, Ka-band ARM zenith radar, W-band ARM cloud radar.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `phiDP` | differential phase |
| `rhoHV` | correlation coefficient between H and V polarizations |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `C band` | frequencies between 4 GHz and 8 GHz |
| `dB` | decibel |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `DQ` | Data Quality |
| `GHz` | gigahertz (10^9 Hz) |
| `Hz` | hertz |
| `Ka band` | frequencies between 26.5 GHz and 40 GHz |
| `KDP` | specific differential phase |
| `kW` | kilowatt |


### References the handbook cites

- Bharadwaj N, K Widener, A Koontz, and K Johnson. "Data Specification for ARM Scanning Radars." In progress.
- Bringi VN, and V Chandrasekar. 2001. Polarimetric Doppler Weather Radar. Cambridge University Press, Cambridge, United Kingdom.
- Doviak RJ, and DS Zrnic. 1993. Doppler Radar and Weather Observations. 2nd Edition, Academic Press, San Diego, California

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf (19 pages, DOE/SC-ARM/TR-121, by K Widener, N Bharadwaj)
- Catalog record: ARM data-source index, `instrument_class_code=saprvad`, read 2026-09-24
- Example file: `sgpxsaprvadI6.c1.20190223.000000.nc` from `sgpxsaprvadI6.c1`, 0.35 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
