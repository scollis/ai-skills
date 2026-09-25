---
name: arm-instrument-tbsins
description: ARM Ice Nucleation Spectrometer for INP measurements aboard Tethered Balloon System (tbsins) - handbook-derived instrument reference. Measurement principle, reported quantities (Ice-nucleating particle), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgptbsinpC1.a1) and the variable inventory of a real file. Use when working with tbsins data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations; Cloud Properties. Triggers - tbsins, sgptbsinpC1.a1, Ice-nucleating particle, Aerosols, Airborne Observations, Cloud Properties, PUFIN sampler (ARM/SNL design, OLAF DaQ INS, PUFIN.
---

# TBSINS - Ice Nucleation Spectrometer for INP measurements aboard Tethered Balloon System

The Tethered Balloon System Ice Nucleation Spectrometer (TBSINS) reports ice-nucleating particle concentrations derived by offline freezing-assay processing (at Colorado State University using the OLAF DaQ INS) of filter samples collected at up to three altitudes by the PUFIN sampler flown on ARM's helium-filled Tethered Balloon System.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbsins` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Aerosols; Airborne Observations; Cloud Properties |
| Manufacturer / model | PUFIN sampler (ARM/SNL design; schematic/parts list at https://github.com/ARM-Development/TBS-INP-Design); offline processing via Colorado State University OLAF DaQ INS... |
| Primary measurements | Ice Nucleating Particle (INP) Concentration |
| Record | 2022-04-10 to 2026-09-24 (retired) |
| Datastreams with data | 9 across 4 sites |
| Sites | bnf, crg, guc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/tbsins |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbsins`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbslws`, `tbsmet`, `tbspops`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbsins` until checked against that document's own section for it.

## How it measures

PUFIN, a lightweight INP sampler flown on the TBS tether, draws air through pre-cleaned 47-mm-diameter Whatman Nuclepore Track-Etched Membrane filters at up to three altitudes per flight, typically over one-hour sampling periods, while monitoring flow, power consumption, and atmospheric conditions in real time. These loaded filters are returned to the surface and undergo offline processing with the ice nucleation spectrometer (INS) at Colorado State University, in which the filters are presumably subjected to a freezing assay (per Creamean et al. 2024) to determine the temperature at which particles on the filter nucleate ice. INP concentrations at each temperature interval are generated using the Open-source Library for Automating Freezing Data acQuisition from Ice Nucleation Spectrometer (OLAF DaQ INS). The technique can resolve INP concentrations down to ~10^-3 L^-1 given sufficient aerosol loading, achievable in as little as 28 minutes of sampling.

**Siting.** PUFIN is flown on the ARM Tethered Balloon System tether and collects multiple filter samples per flight at up to three altitudes; TBS flights are generally conducted 152 m (500') below cloud base, in 3 sm or greater visibility, to a maximum altitude of 1.5 km (4,921') agl, with in-cloud flights generally conducted within Restricted Airspace; tether angle from zenith is not allowed to exceed 45° in flight, which affects true sampling altitude/position relative to nominal tether length.

**Sampling.** reported every typically one hour per filter sample; as little as 28 minutes achievable; averaging integrated filter sample over sampling duration; offline INS analysis at discrete temperature intervals (hb p. 25).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Ice-nucleating particle (INP) concentration | L-1 | down to ~10-3 L-1 (detection limit with... | - | - | (hb p. 25) |


## Specifications

| parameter | value | source |
|---|---|---|
| Filter type | Whatman Nuclepore Track-Etched Membrane, 47-mm-diameter, pre-cleaned | (hb p. 25) |
| Sampling duration (typical) | typically collected over one hour | (hb p. 25) |
| Minimum sampling duration achieved | 28 minutes | (hb p. 25) |
| Sampling altitudes per flight | up to three altitudes | (hb p. 25) |
| Detection limit | ~10-3 L-1 | (hb p. 25) |


## The data

Verified example: **`sgptbsinpC1.a1`**, file `sgptbsinpC1.a1.20220426.142826.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1, `temperature`=27 |
| Data variables | 14 |
| QC variables | 0 (`qc_` companions) |
| Median time step | n/a |
| File time span | 2022-04-26T14:28:26 to 2022-04-26T14:28:26 |
| dod version | tbsinp-a1-1.0 |
| process version | ingest-tbsinp-1.0-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `lower_ci` | count/L | time,temperature | - | 95% lower confidence limit for number of ice nucleating particles per... |
| `lower_height` | m | time | - | Lower height AGL |
| `n_inp_stp` | count/L | time,temperature | - | Number of ice nucleating particles per L of air at STP |
| `start_utc` | - | time | - | Filter collection start time |
| `stop_utc` | - | time | - | Filter collection end time |
| `temperature` | degC | temperature | - | Freezing temperature |
| `time` | - | time | - | Time offset from midnight |
| `total_volume` | L | time | - | Total volume of air passed through filter at STP |
| `treatment_flag` | 1 | time,temperature | - | Treatment flag |
| `upper_ci` | count/L | time,temperature | - | 95% upper confidence limit for number of ice nucleating particles per... |
| `upper_height` | m | time | - | Upper height AGL |


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
                     params={"user": f"{user}:{token}", "ds": "sgptbsinpC1.a1",
                             "start": "2022-04-26", "end": "2022-04-26", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgptbsinpC1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgptbsinpC1.a1", "2022-04-26", "2022-04-26")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"

# a day's files will not concatenate on a shared index, so concatenate along time
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True, combine='nested', concat_dim='time')
print(act.discovery.get_arm_doi("sgptbsinpC1.a1", "2022-04-26", "2022-04-26"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("lower_height")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `treatment_flag`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgptbsinpC1.a1", "20220410", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The handbook states that each TBS datastream includes quality control variables for each scientific variable, but no PUFIN/INS-specific QC flag details are given beyond real-time monitoring of flow, power consumption, and atmospheric conditions during sampling.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Offline processing delay between filter collection and INS analysis | Gap between TBS flight date and INP concentration data availability; PUFIN data products are publicly released on the ARM Data Center within six months of each TBS campaign | None stated beyond the six-month release timeline | (hb p. 25) |
| Sample loading / detection limit dependency on sampling duration | Very low or noisy INP concentration estimates for short sampling durations; detection limit of ~10-3 L-1 requires sufficient aerosol loading, achieved in as little as 28 minutes under... | Samples typically collected over one hour to ensure sufficient aerosol loading | (hb p. 25) |
| Tether angle deviation from zenith with wind speed | Actual sampling altitude/position of PUFIN filters may differ from nominal tether length under windy conditions since tether angle increases with wind speed (not allowed to exceed 45°) | Flights suspended/balloon retrieved if winds aloft exceed 14 m/s; tether angle capped at 45° | (hb p. 9) |
| Restricted flight envelope limiting sampling conditions | No PUFIN/INS data available above 1.5 km agl or in-cloud outside Restricted Airspace, or in visibility less than 3 sm, or above cloud-base-relative altitude limits | Flights conducted under FAA Certificate of Authorization with specified operational limits | (hb p. 9) |
| Data product not yet released within campaign timeframe | Absence of TBSINS/PUFIN data in ARM archive for recent campaigns until up to six months post-campaign | None stated beyond noting the six-month release window | (hb p. 25) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | PUFIN uses pre-cleaned filters; calibration mode listed as ARM TBS staff (hb p. 30) |
| Calibration interval | Prior to each campaign (hb p. 30) |
| Routine maintenance | PUFIN calibration/check prior to each campaign, performed by ARM TBS staff (as for EMSL instruments STAC, TBAC, TRAVIS) (hb p. 30) |
| Maintenance interval | Prior to each campaign (hb p. 30) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: PUFIN, TBS (parent platform), Ice Nucleation Spectrometer (INS) Instrument Handbook,....

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `INP` | ice nucleating particle |
| `INS` | ice nucleation spectrometer |
| `OLAF DaQ INS` | Open-source Library for Automating Freezing Data acQuisition from Ice Nucleation... |
| `PUFIN` | Profiling Upper Altitudes for Ice Nucleation |
| `TBS` | tethered balloon system |
| `CSU` | Colorado State University |


### References the handbook cites

- Creamean, JM, T Hill, CC Hume, and T Devadoss. 2024. Ice Nucleation Spectrometer (INS) Instrument Handbook. DOE/SC-ARM-TR-278.
- Creamean, JM, D Dexheimer, CC Hume, M Vazquez, BTM Hess, CM Longbottom, CA Ruiz, and AK Theisen. 2025. "Reaching new heights: A vertically-resolved ice nucleating particle sampler operating on Atmospheric Radiation...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbsins`, read 2026-09-24
- Example file: `sgptbsinpC1.a1.20220426.142826.nc` from `sgptbsinpC1.a1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
