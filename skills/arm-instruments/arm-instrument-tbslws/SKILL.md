---
name: arm-instrument-tbslws
description: ARM Leaf Wetness Sensor aboard Tethered Balloon System (tbslws) - handbook-derived instrument reference. Measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with tbslws data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Atmospheric Profiling; Surface/Subsurface Properties. Triggers - tbslws, Leaf Wetness Sensor aboard Tethered Balloon System, olitbslwsM1.a0, Airborne Observations, Atmospheric Profiling, Surface/Subsurface Properties, POPS, SLWC, STAC, TBAC.
---

# TBSLWS - Leaf Wetness Sensor aboard Tethered Balloon System

The handbook does not mention a leaf wetness sensor; it documents the ARM Tethered Balloon System (TBS) platform-level components and the various sensor payloads (thermal/visible imagers, CPC, DTS, ground station meteorology, radiosondes, POPS, SLWC sonde, wind booms, aerosol/VOC collectors, and PUFIN INP sampler) flown on a helium-filled tethered aerostat/balloon controlled by a winch and tether from a ground command station.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 32 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `tbslws` |
| Handbook | [DOE/SC-ARM-TR-206 / D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom / February 2026](https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf) |
| Measurement category | Airborne Observations; Atmospheric Profiling; Surface/Subsurface Properties |
| Primary measurements |  |
| Record | 2016-04-18 to 2016-10-22 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | oli |
| ARM page | https://www.arm.gov/capabilities/instruments/tbslws |


## Credit

Everything this skill knows about the instrument is the work of **D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom. *Tethered Balloon System (TBS) Instrument Handbook*, DOE/SC-ARM-TR-206, February 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `tbslws`, ARM links no handbook to this class. The facts below come from the **Tethered Balloon System** (`tbs`) handbook, which documents the parent system. The same document also covers `tbscpc`, `tbsdts`, `tbsground`, `tbsins`, `tbsmet`, `tbspops`, `tbsslwc`, `tbswind`. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `tbslws` until checked against that document's own section for it. The handbook contains no text naming this class, so **every fact in this skill is parent-system-level**, established by a full-text search of the document rather than by a section about this instrument.

## How it measures

No leaf wetness sensing principle is described anywhere in this handbook; the document instead describes the TBS platform (balloon, winch, tether) and a series of independent payload instruments, each with its own measurement principle (e.g., condensation particle counting, Raman-scattering distributed temperature sensing, vibrating-wire ice accretion for supercooled liquid water content, sonic/cup/propeller anemometry, radiosonde thermodynamic sensors, and filter/impactor-based aerosol and VOC sampling).

**Siting.** TBS flights are conducted under an FAA Certificate of Authorization specific to each mission location; flights are generally 152 m (500') below cloud base, in 3 sm or greater visibility, to a maximum altitude of 1.5 km (4,921') agl; in-cloud flights are generally conducted within Restricted Airspace; night flights currently only at SGP with specific FAA authorization; tether angle from zenith increases with wind speed and may not exceed 45° in flight; missions are typically two weeks long with daily flights as conditions allow.

## Specifications

| parameter | value | source |
|---|---|---|
| Aerostat volume | 74-128 m3 Skydoc aerostats | (hb p. 9) |
| Science payload weight (aerostats) | 8-45 kg | (hb p. 9) |
| Science payload weight (other balloon types) | under 8 kg | (hb p. 9) |
| Maximum sustained surface wind speed for launch | 10 m/s | (hb p. 9) |
| Wind speed aloft triggering flight suspension/retrieval | 14 m/s | (hb p. 9) |
| Maximum tether angle from zenith | 45° | (hb p. 9) |
| Maximum altitude (agl) | 1.5 km (4,921') | (hb p. 9) |
| Typical cloud clearance | 152 m (500') below cloud base | (hb p. 9) |
| Minimum visibility | 3 sm or greater | (hb p. 9) |
| Winch motor | 5 HP DC permanent magnet motor, 220 VAC 40 A shore power | (hb p. 10) |
| Winch gearbox ratio | 75:1 double-reduction planetary-to-worm gear | (hb p. 10) |
| Tether length | up to 10,000' of 3/16" OD plasma 12-strand rope | (hb p. 10) |
| Tether minimum breaking strength | 5,500 lbs | (hb p. 10) |
| Tether safety factor | 5.9x with 128 m3 aerostat at 15 m/s wind at sea level standard atmosphere | (hb p. 10) |


## The data

**No example file was verified for this instrument.** the only TBS liquid-water-sensor datastream is level a0, which ARM Live does not serve by policy.

ARM's catalog lists 1 datastreams with data across 1 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "olitbslwsM1.a0", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
                     params={"user": f"{user}:{token}", "ds": "olitbslwsM1.a0",
                             "start": "YYYY-MM-DD", "end": "YYYY-MM-DD", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./olitbslwsM1.a0/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "olitbslwsM1.a0", "YYYY-MM-DD", "YYYY-MM-DD")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("olitbslwsM1.a0", "YYYY-MM-DD", "YYYY-MM-DD"))   # cite what you pulled
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("olitbslwsM1.a0", "20160418", "20260924")
```

The handbook's own note on data quality: Each datastream includes quality control variables for each scientific variable.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| No leaf wetness sensor documented | No leaf wetness datastream, variable, or measurement range appears anywhere in the handbook's instrument list, data section, or specification tables | - | (hb p. 6) |
| Aerostat launch/flight restricted by wind speed | No flight data collected above 10 m/s surface wind at launch; flights terminated and balloon retrieved when winds aloft exceed 14 m/s, producing gaps in time series during high-wind periods | Aerostats not launched above 10 m/s surface wind; flights suspended and balloon retrieved above 14 m/s aloft | (hb p. 9) |
| Tether angle constraint with wind speed | Payload altitude/position deviates from vertical as tether angle increases with wind speed, altering true sample altitude versus assumed vertical profile | Tether angle not allowed to exceed 45° in flight | (hb p. 9) |
| Altitude decrease in line tension with elevation | Aerostat lift and line tension decrease roughly 1% per ~100 m operated above mean sea level during descent, affecting tension/altitude relationship | - | (hb p. 10) |
| CPC/POPS coincidence error at high concentrations | Particle concentration readings become biased low above the stated maximum concentration range due to greater than 10% coincidence error (CPC: greater than 100,000 #/cm3; POPS: greater than... | - | (hb p. 6) |
| POPS accuracy flow-rate dependence | Particle concentration accuracy of +/-10% specifically applies at less than 1000 #/cm3 at 0.1 LPM sample flow rate; deviations from this flow/concentration regime may show different accuracy | - | (hb p. 11) |
| DTS fiber optic rotary joint used only during ascent/motion | Ch2 fiber data only available when balloon is stationary aloft, since it does not operate through the fiber optic rotary joint | Deploy Ch1 fiber via rotary joint for continuous profiling; use Ch2 only for stationary aloft measurements | (hb p. 7) |
| DTS calibration baths as endpoint reference | DTS temperature retrieval relies on ice-water and heated calibration baths at the surface plus an iMet-4 RSB radiosonde endpoint reference; any drift in these references would bias the... | Two PT100 probes and 15-m fiber coils deployed in calibration baths; iMet-4 RSB radiosonde deployed at fiber end as calibration reference | (hb p. 7) |
| SLWC sonde restricted to in-cloud, restricted-airspace flights | tbsslwc / tbsmergedincloud data only exist for flights conducted inside clouds in restricted airspace; absent otherwise | - | (hb p. 11) |
| Ceilometer and Doppler lidar operated independently of TBS | Cloud base/mixing layer height and wind profile data merged into tbsmerged may not be time- or space-coincident with TBS payload measurements since these ancillary instruments are not... | TBS generally operated with a collocated ceilometer; if a Doppler lidar is dedicated to TBS flights it is run in 1-minute wind profile mode | (hb p. 8) |
| tbsground continuous vs. flight-only datastreams | tbsground is continuously collected at the surface, unlike other TBS datastreams which are only produced during flight, so time coverage differs between datastreams when merging | - | (hb p. 18) |
| Wind sensor boom heading and calibration checks needed | Wind direction measurements could show a heading offset if not checked against reference compass bearing at start of campaign | Heading checks performed against reference compass bearing at start of each field campaign | (hb p. 21) |
| Turbulence estimate frequency mismatch between tbswind and tbswind3d/tbsmet | Turbulence intensity/TKE estimates differ depending on whether based on 1 Hz cup/propeller (tbswind) or 60 Hz sonic (tbswind3d/tbsmet) data; users should not directly compare turbulence... | 3-minute and 30-minute means of GPS position and acceleration used to motion-correct turbulence estimates in tbswind3d | (hb p. 20) |
| Vertical wind speed requires ascent/descent correction | Raw vertical_wind values would be biased by boom ascent/descent rate if uncorrected | Ascent/descent speed corrected for in vertical_wind by applying offset for altitude change from Vega 28 compass board | (hb p. 19) |
| STAC/TRAVIS/TBAC data not on ARM Data Discovery | No STAC, TBAC, or TRAVIS datastream appears in ARM Data Discovery archive listing; must be requested separately | Datastreams available from PNNL EMSL directly | (hb p. 13) |
| FROST data not on ARM Data Discovery | No FROST datastream appears in ARM Data Discovery archive listing | Data available from SNL directly | (hb p. 16) |
| PUFIN data release delay | PUFIN INP data for a campaign will not appear in the ARM Data Center until up to six months after the campaign ends | PUFIN data products publicly released within six months of each TBS campaign | (hb p. 17) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Varies by instrument; see Table 15 (vendor calibration, instrument mentor calibration, or ARM TBS staff calibration prior to each campaign) (hb p. 29) |
| Calibration interval | Varies by instrument: prior to each campaign, annually, every two years, or every three years depending on instrument (Table 15) (hb p. 29) |
| Routine maintenance | Balloons: air leak/seam testing and rigging inspection; winches: annual one-minute deadlift testing; tethers: load tested to failure every 225 flight hours; instrumentation: CPC/POPS daily flow rate and zero filter checks during campaigns, wind sensor boom heading checks at start of each campaign, daily comparison of... (hb p. 20) |
| Maintenance interval | Varies: annual balloon air leak testing, annual winch deadlift testing, 225-flight-hour tether load testing, daily/per-campaign instrument checks (hb p. 20) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Ceilometer, Doppler lidar, Ice Nucleation Spectrometer (INS), Portable Optical Particle Spectrometer (POPS) standalone handbook.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `TBS` | tethered balloon system |
| `DTS` | distributed temperature sensing |
| `POPS` | portable optical particle spectrometer |
| `CPC` | condensation particle counter |
| `SLWC` | supercooled liquid water content |
| `STAC` | size- and time-resolved aerosol collector |
| `TBAC` | total bulk aerosol collector |
| `TRAVIS` | time-resolved automated volatile organic compounds sampling system |
| `FROST` | fielded remote organic sampling technology |
| `PUFIN` | profiling upper altitudes for ice nucleation |
| `INP` | ice nucleating particle |
| `INS` | ice nucleation spectrometer |
| `IMU` | inertial measurement unit |
| `ADS-B` | Automatic Dependent Surveillance-Broadcast |


### References the handbook cites

- Cheng et al. 2022, Environmental Science: Atmospheres
- Creamean et al. 2024, Ice Nucleation Spectrometer (INS) Instrument Handbook, DOE/SC-ARM-TR-278
- Creamean et al. 2025, EGUsphere
- Dexheimer et al. 2019, Atmospheric Measurement Techniques
- Dexheimer et al. 2023, TBSMERGED Value-added Product Report, DOE/SC-ARM-TR-286
- Lata et al. 2023, Environmental Science & Technology
- Lata et al. 2025, Environmental Science: Atmospheres
- Mei and Pekour 2020, POPS Instrument Handbook, DOE/SC-ARM-TR-259
- Serke et al. 2014, Atmospheric Research
- Vandergrift et al. 2022, ACS Earth and Space Chemistry

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/tbs_handbook.pdf (32 pages, DOE/SC-ARM-TR-206, by D Dexheimer, Z Cheng, J Creamean, J Sammon, K Gaustad, F Mei, C Longbottom)
- Catalog record: ARM data-source index, `instrument_class_code=tbslws`, read 2026-09-24
- Example file: none - the only TBS liquid-water-sensor datastream is level a0, which ARM Live does not serve by policy
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
