---
name: arm-instrument-ozone-air
description: ARM Ozone Monitor aboard Aircraft (ozone-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Ozone, Pres, Bench Temp, O3 Lamp Temp, Flow A, Flow B, Noise A, Noise B), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafo3F1.c1) and the variable inventory of a real file. Use when working with ozone-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Other. Triggers - ozone-air, Ozone Monitor aboard Aircraft, sgpaafo3F1.c1, Ozone, Pres, Bench Temp, O3 Lamp Temp, Flow A, Flow B, Airborne Observations, Other, Thermo Fisher Scientific Ozone Analyzer, Model 49i, DQPR, NIST, NYS DEC, o.d..
---

# OZONE-AIR - Ozone Monitor aboard Aircraft

The Ozone Monitor measures atmospheric ozone (O3) mixing ratio by UV photometry (254 nm) in a dual-cell configuration, deployed in-situ aboard the ARM Aerial Facility aircraft and at fixed/mobile ARM ground sites (AMF1, AMF2, AMF3, SGP, ENA) sampling from a trace-gas inlet.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ozone-air` |
| Handbook | [DOE/SC-ARM-TR-179 / SR Springston, R Trojanowski, C Hayes / April 2025](https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf) |
| Measurement category | Airborne Observations; Other |
| Manufacturer / model | Thermo Fisher Scientific Ozone Analyzer, Model 49i |
| Primary measurements | Ozone Concentration |
| Record | 2013-06-30 to 2024-01-27 (retired) |
| Datastreams with data | 14 across 6 sites |
| Sites | acx, cor, ena, mao, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/ozone-air |


## Credit

Everything this skill knows about the instrument is the work of **SR Springston, R Trojanowski, C Hayes** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SR Springston, R Trojanowski, C Hayes. *Ozone Monitor (OZONE) Instrument Handbook*, DOE/SC-ARM-TR-179, April 2025.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `ozone` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `ozone-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The ozone monitor measures ozone based on absorbance of ultraviolet (UV) light at a wavelength of 254 nm by ozone molecules, with absorbance related to ozone concentration through the Beer-Lambert Law: I/I0 = e^-KLC, where K is the molecular absorption coefficient (308 cm-1 at 0C and 1 atm), L is the cell length (38 cm), and C is ozone concentration in ppm. The dual-cell configuration with selective removal of ozone in the reference cell reduces response from interfering species. Following each 4-s measurement cycle, the reference and sample cells are reversed so optical effects (change in lamp output, detector gain, cell cleanliness) are rejected. The instrument also contains an ozone source (photolysis cell using filtered ambient air) that measures response stability over time via periodic automatic span checks.

**Siting.** Samples from a trace gas inlet, typically high-flow 1/2-inch o.d. PFA tubing sampling from under the aerosol inlet rain hat at ~10 m above ground level (or on the starboard side of the fuselage for aircraft deployment per ARM catalog); air pulled in at 30 LPM controlled by rotometer; residence time to back of instrument ~1-2 s; a 47-mm x 5-um Teflon/PFA filter is installed on the inlet line ahead of the instrument.

**Sampling.** native rate instrument makes an independent measurement every 4 seconds due to internal pneumatic switching limitations; reported every 1-s resolution (same concentration number repeated ~4 times at the uniform, monotonic 1-s time base); averaging Avg Time field: reported as 10 s when actual averaging time is 4 s (fast response default for AOS); centroid average ~30 seconds for zero/span (hb p. 3).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Ozone (O3) mixing ratio | ppbv (reported); ppm... | Linearity demonstrated up to 1500 ppbv;... | Initial calibration within 1-2% accuracy; field... | 1-s reported (actual... | (hb p. 3) |
| Pres | mm Hg | - | - | - | (hb p. 5) |
| Bench Temp | degC | - | - | - | (hb p. 5) |
| O3 Lamp Temp | degC | - | - | - | (hb p. 5) |
| Flow A | SLPM | - | not calibrated | - | (hb p. 5) |
| Flow B | SLPM | - | not calibrated | - | (hb p. 5) |
| Noise A | - | normally less than  10 | - | - | (hb p. 5) |
| Noise B | - | normally less than  10 | - | - | (hb p. 5) |
| Cell A Int (lamp intensity) | Hz | - | raised by mentor to 110-120,000 Hz when below... | - | (hb p. 6) |
| Cell B Int (lamp intensity) | Hz | - | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Units (measured quantity) | reported in ppm by instrument (ppbv in ARM data) | (hb p. 13) |
| Range | Full range extends well past conceivable ambient levels; linearity up to 1500 ppbv demonstrated with automatic span checks done twice daily | (hb p. 14) |
| Accuracy | Initial (on receipt) calibration within 1-2% accuracy; field variation from original measurement standard ~5% | (hb p. 14) |
| Repeatability | [O3] sigma = 2 ppbv; [O3] 95% Confidence Interval = ± 4 ppbv | (hb p. 14) |
| Manufacturer zero noise | 0.25 ppb RMS (for a 60-s average) | (hb p. 14) |
| Sensitivity | 4 ppbv (95% CI above baseline, as reported to ARM); manufacturer 'Lower detectable limit' = 1.0 ppb | (hb p. 14) |
| Molecular absorption coefficient K | 308 cm-1 (at 0degC and 1 atmosphere) | (hb p. 8) |
| Cell length L | 38 cm | (hb p. 8) |
| Cell A/B Int lamp intensity threshold | less than  ~60,000 Hz triggers lamp voltage increase or replacement; raised to 110-120,000 Hz | (hb p. 6) |
| Noise A/B normal value | less than  10 | (hb p. 5) |
| Measurement cycle | reference and sample cells switch every 10 seconds (as reported, actual 4 s in fast-response mode) | (hb p. 6) |
| Pump life | 2-3 years under continuous operation | (hb p. 13) |
| Filter change interval | every two weeks | (hb p. 13) |
| Zero/span check timing | Every midnight and noon (00:00:00 and 12:00:00), lasting 4 minutes | (hb p. 8) |
| Zero flag exclusion | first 105 seconds after zero actuated excluded | (hb p. 12) |
| Span flag exclusion | first 30 seconds after each span level excluded | (hb p. 12) |
| Centroid averaging | ~30 seconds once stable level achieved | (hb p. 12) |
| Zero/span drift threshold (monthly) | less than 1-2% relative standard deviation and minimal drift (less than 2%) typical; greater values indicate need for recalibration | (hb p. 12) |
| Long-term drift threshold | drifts of more than 5% indicate need for recalibration at NYS DEC laboratory | (hb p. 11) |


## The data

Verified example: **`sgpaafo3F1.c1`**, file `sgpaafo3F1.c1.20160920.202755.nc`
(0.17 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5104 |
| Data variables | 6 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aafo3-c1-1.0 |
| process version | ingest-aafo3me-1.3-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `o3` | ppbv | time | - | Ozone concentration at STP |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgpaafo3F1.c1",
                             "start": "2016-09-20", "end": "2016-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaafo3F1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaafo3F1.c1", "2016-09-20", "2016-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaafo3F1.c1", "2016-09-20", "2016-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("o3")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaafo3F1.c1", "20130630", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Automatic flagging of data occurs when the instrument changes states during zero and span checks: first 105 seconds after zero actuation and first 30 seconds after each span level are excluded; centroid of each state is an average of ~30 seconds once stable. Second level of QC is inspection of 2x daily zero/span checks, typically showing less than 1-2% relative standard deviation and less than 2% drift; larger values indicate need for recalibration at NYS DEC. Third level is visual inspection of the output data stream for periods of instrument/inlet failure, which are flagged; failures are...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Interfering species response | Would appear as spurious ozone signal not corresponding to actual ozone; mitigated by design | Dual cell configuration with selective removal of ozone in reference cell reduces response from interfering species | (hb p. 2) |
| Optical drift (lamp output, detector gain, cell cleanliness changes) | Would appear as slow baseline drift in signal if uncorrected | Reference and sample cells are reversed after each 4-s measurement cycle so optical effects are rejected | (hb p. 3) |
| 1-s data repeats same value ~4 times | Apparent step-like/staircase pattern in 1-s time series because instrument only makes an independent measurement every 4 seconds | - | (hb p. 3) |
| No water vapor correction | Reported O3 mixing ratio has no correction for water vapor interference | - | (hb p. 7) |
| Spans and zeros not removed from data stream | Zero/span check periods appear embedded within a/b-level data streams as distinct value excursions | Users should be aware spans and zeros are NOT removed from the data streams when utilizing the data | (hb p. 7) |
| Twice-daily negative pressure spikes | Momentary negative spikes in cell pressure housekeeping data at zero/span check times | Due to flow interruptions proximate to zero/span checks; understood artifact, not an error | (hb p. 10) |
| Lamp intensity decline | Cell A/B Int (raw detector Hz value) decreasing below ~60,000 Hz | Mentor raises lamp voltage to bring intensity to 110-120,000 Hz (intensity does not affect instrument response) | (hb p. 10) |
| Excess electronic noise (Noise A/B) | Noise A/B values exceeding normal level of less than 10 | Indicates need to clean the cell or replace the lamp | (hb p. 5) |
| Span source (photolysis lamp) drift/instability | Difference between measured span and calibrated span value, usually less than 5%, seen in zero/span check time series relative to NYS DEC reference dotted lines | Judged to be instability/drift in the photolysis lamp, not the measurement cell; drift greater than 5% over greater than 1 year indicates need for... | (hb p. 11) |
| Dirty or blocked inlet filter affecting flow | Reduced Flow A / Flow B (SLPM) values in housekeeping data | Flow rates do not directly affect instrument response but do affect span check values; two-week filter change schedule prevents flow reduction from... | (hb p. 5) |
| Diaphragm pump degradation | Gradual change/decline in instrument flow rate over time | Pump life under continuous operation is 2-3 years; replace as needed | (hb p. 13) |
| Instrument or inlet failure causing nonsensical values | Periods of instrument in-operation with anomalous/nonsensical values in output data stream | Identified via visual inspection by mentor using full housekeeping record; documented in DQPR/DQR; unique individual events not algorithmically... | (hb p. 13) |
| Impermeable filter spacer mistakenly used instead of filter | Instrument failure pattern documented separately; likely zero/blocked flow signature | DO NOT USE THE SPACER! USE THE WHITE FILTER (error made multiple times); use white 47-mm PFA membrane filter only | (hb p. 13) |
| Short instrumental spikes (4-s duration) | 20-40 ppbv positive or negative spikes of ~4-s duration (one measurement cycle) that can dramatically affect daily max/min readings; physically nonsensical given inlet/sample... | Flagged for deletion after visual inspection | (hb p. 13) |
| Real ambient ozone titration by local NO sources | Negative peaks of 30-s to 10-min duration, distinguishable from instrumental spikes; can be correlated with wind direction | Not flagged, as they represent real ambient ozone changes; distinguishing from instrumental spikes requires experience and judgment; local source... | (hb p. 13) |
| Filter/ozone destruction buildup on inlet filter | Would be obvious in span check values if filter buildup caused ozone destruction | All zero and span checks pass through ambient inlet filter so this effect would be detectable | (hb p. 14) |
| Span check source pressure dependence | Ozone generator output concentration variable with atmospheric pressure and residence time (varies with inverse square of ambient pressure) | Supplied pressure regulator provides only consistent gauge (not absolute) pressure; effect is similar | (hb p. 16) |
| Extended shutdown warm-up period | Instrument does not output valid data for 10 minutes or more after power-on following an extended shutdown | - | (hb p. 17) |
| Clock/timestamp irregularities | Minor irregularities (dithering) in output data stream timing; more than 1 record per second, or records with only date/time stamp and no data possible | Processing of raw data must handle these irregularities | (hb p. 7) |
| No field capability to deliver calibration source remotely | Drift beyond thresholds cannot be corrected in the field; instrument must be sent to NYS DEC | At present, there is no capability within ARM to deliver a calibration source for ozone to remote field sites | (hb p. 12) |
| PFA tubing abrasion inside instrument | Potential leaks or flow anomalies from tubing wear | All tubing must be strain-relieved with tie wraps to prevent rubbing | (hb p. 19) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Thermo Scientific ozone monitors calibrated for response upon receipt from manufacturer by the mentor at the NYS DEC testing laboratory in Albany, NY; internal automatic 2x daily zero and 5-level span checks (L1-L5) using an internal ozonizer/photolysis source with filtered ambient air; zero checked via proprietary... (hb p. 13) |
| Calibration interval | 2x daily (midnight and noon) automatic zero/span checks; recalibration at NYS DEC when drift exceeds 5% over periods greater than 1 year (hb p. 13) |
| Traceability | NYS DEC reference standard certified by U.S. EPA with NIST-traceable reference; used only for calibration of ozone instruments (hb p. 13) |
| Routine maintenance | Change inlet particle filter (47-mm diam. 5-um PFA membrane filter Type LS, Millipore Catalog # LSWPO4700, white filter - do NOT use blue plastic spacer); inspect old filter for dirt buildup; strain-relieve internal PFA tubing with tie wraps to prevent abrasion; lamp voltage increased or lamp replaced when Cell Int... (hb p. 17) |
| Maintenance interval | Filter change every two weeks; pump life 2-3 years under continuous operation (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: ARM Aerial Facility (AAF), AMF1 AOS, AMF2 AOS, AMF3 AOS, SGP atmospheric observatory, Eastern North Atlantic (ENA).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `AMF` | ARM Mobile Facility |
| `AMF1` | first ARM Mobile Facility |
| `AMF2` | second ARM Mobile Facility |
| `AMF3` | third ARM Mobile Facility |
| `AOS` | Aerosol Observing System |
| `ARM` | Atmospheric Radiation Measurement |
| `ENA` | Eastern North Atlantic |
| `DQPR` | Data Quality Problem Report |
| `DQR` | Data Quality Report |
| `NI` | National Instruments |
| `NIST` | National Institute of Standards and Technology |
| `NTP` | Network Time Protocol |
| `NYS DEC` | New York State Department of Environmental Conservation |


## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ozone_handbook.pdf (26 pages, DOE/SC-ARM-TR-179, by SR Springston, R Trojanowski, C Hayes)
- Catalog record: ARM data-source index, `instrument_class_code=ozone-air`, read 2026-09-23
- Example file: `sgpaafo3F1.c1.20160920.202755.nc` from `sgpaafo3F1.c1`, 0.17 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
