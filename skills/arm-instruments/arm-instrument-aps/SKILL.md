---
name: arm-instrument-aps
description: ARM Aerodynamic Particle Sizer (aps) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerodynamic diameter, Optical diameter, Number size distribution, Total number concentration, Surface-area concentration, Volume concentration), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaosapsC1.b1) and the variable inventory of a real file. Use when working with aps data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - aps, Aerodynamic Particle Sizer, enaaosapsC1.b1, Aerodynamic diameter, Optical diameter, Number size distribution, Total number concentration, Surface-area concentration, Volume concentration, Aerosols, TSI Aerodynamic Particle Sizer (APS) Model 3321, ACTRIS, DUSTIEAIM, HEPA, NetCDF.
---

# APS - Aerodynamic Particle Sizer

The APS is a TSI Model 3321 time-of-flight aerodynamic particle spectrometer deployed within the ARM Aerosol Observing System (AOS) to measure coarse-mode aerosol number size distributions from 0.5-20 µm aerodynamic diameter (0.3-20 µm optical) by sampling from a common inlet manifold.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 28 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `aps` |
| Handbook | [DOE/SC-ARM-TR-343 / A Singh, D Campos, T Subba / August 2026](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | TSI Aerodynamic Particle Sizer (APS) Model 3321 |
| Primary measurements | Aerosol concentration; Aerosol particle size; Aerosol particle size distribution |
| Record | 2016-04-01 to 2026-09-23 (active) |
| Datastreams with data | 12 across 10 sites |
| Sites | bnf, cor, crg, dst, ena, epc, hou, kcg, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/aps |


## Credit

Everything this skill knows about the instrument is the work of **A Singh, D Campos, T Subba** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Singh, D Campos, T Subba. *Aerodynamic Particle Sizer (APS) Instrument Handbook*, DOE/SC-ARM-TR-343, August 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `opc` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `aps`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The APS 3321 measures aerodynamic particle size using a time-of-flight principle: the aerosol sample is accelerated through a nozzle, and particles pass through two partially overlapping laser beams that create a double-crested beam profile. Larger particles accelerate more slowly due to inertia, producing a longer peak-to-peak time of flight - resolved at 4 ns resolution - which is mapped to aerodynamic diameter via an internal calibration curve. A valid single-particle event generates a signal with exactly two crests; signals with only one crest (phantom particles) or more than two crests (coincidence events) are excluded from size distribution calculations but logged separately for post-analysis correction. Because coincidence increases with particle concentration, the manufacturer provides maximum recommended concentration limits and coincidence thresholds; adherence to these limits is necessary to ensure that reported number and mass size distributions reflect only well-characterized single-particle events.

**Siting.** The APS draws from the main AOS inlet manifold via a vertical, dedicated sample line, with horizontal runs and bends kept to a minimum to limit gravitational and inertial particle losses. A Perma Pure MD-700 nafion dryer (24-inch active length with a crossflow purge) sits upstream of the APS, holding sample RH at ≤ 40% consistent with ACTRIS/GAW guidance. RH and temperature can be monitored just upstream of the APS to verify dryer performance. Site-specific bends/configuration (e.g., ENA, BNF vs AMF1, SGP) may result in different transmission losses, and only AMF1 transmission loss has been characterized; the SGP APS currently operates without a dryer (to be added in FY27); NSA APS...

**Sampling.** native rate 1 Hz; reported every 1 s (programmable) (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerodynamic diameter | µm | 0.5-20 µm | - | 0.02 µm at 1.0 µm; 0.03 µm... | (hb p. 7) |
| Optical diameter (PSL equivalent) | µm | 0.3-20 µm | - | - | (hb p. 7) |
| Number size distribution (dN/dlogDp) | 1/cm³ | - | - | 51 size bins at b1 level... | (hb p. 10) |
| Total number concentration | 1/cm³ | usable to 10,000 pt/cm³ | ±10% of reading plus variation from counting... | - | (hb p. 7) |
| Surface-area concentration | nm²/cm³ | - | - | - | (hb p. 10) |
| Volume concentration | nm³/cm³ | - | - | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Technique | Time-of-flight, double-crested optical system, single high-speed timing processor | (hb p. 7) |
| Particle type | Airborne solids and non-volatile liquids | (hb p. 7) |
| Size range | 0.5-20 µm aerodynamic; 0.3-20 µm optical (PSL equivalent) | (hb p. 7) |
| Resolution | 0.02 µm at 1.0 µm; 0.03 µm at 10 µm — 32 ch/decade, 52 total channels | (hb p. 7) |
| Max concentration | 1,000 #/cm³ at 0.5 µm (less than 5% coincidence); 1,000 pt/cm³ at 10 µm (less than 10%); usable to 10,000 pt/cm³ | (hb p. 7) |
| Flow rates | Total 5.0 L/min ±1%, sheath 4.0 L/min ±1%, aerosol 1.0 L/min ±10% (feedback controlled) | (hb p. 7) |
| Sampling time | 1 s (programmable) | (hb p. 7) |
| Pressure correction | Automatic 400-1030 mbar; full correction 700-1030 mbar | (hb p. 7) |
| Temperature | 10-40 °C (50-104 °F) | (hb p. 7) |
| Humidity | 10-90% RH, non-condensing | (hb p. 7) |
| Concentration accuracy | ±10% of reading plus variation from counting statistics | (hb p. 7) |
| Laser | 30 mW, 655 nm diode | (hb p. 7) |
| Detector | Avalanche photodetector (APD) | (hb p. 7) |
| Power | 100-240 VAC, 50-60 Hz, 100 W; or 24 VDC | (hb p. 7) |
| Communications | RS232 (9-pin), 7-bit even parity, 9600/19200/38400 baud | (hb p. 8) |
| I/O | Digital: 15-pin (3 in/3 out); analog and digital pulse via BNC (configurable) | (hb p. 8) |
| Dimensions (H×W×D) | 18 × 30 × 38 cm (7 × 12 × 15 in) | (hb p. 8) |
| Weight | 10 kg (22 lbs) | (hb p. 8) |


## The data

Verified example: **`enaaosapsC1.b1`**, file `enaaosapsC1.b1.20260919.000000.nc`
(48.05 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86399, `bound`=2, `diameter_aerodynamic`=51 |
| Data variables | 38 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:59 |
| dod version | aosaps-b1-1.2 |
| process version | ingest-aosapscorr-1.7-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `dN_dlogDp` | 1/cm^3 | time,diameter_aerodynamic | yes | Number size distribution, aerodynamic diameter |
| `total_N_conc` | 1/cm^3 | time | yes | Aerosol number concentration from integrated size distribution, APS |
| `total_SA_conc` | nm^2/cm^3 | time | yes | Total surface area concentration from integrated size distribution,... |
| `total_V_conc` | nm^3/cm^3 | time | yes | Total volume concentration from integrated size distribution, APS |
| `analog_input_voltage_0` | V | time | - | Analog input voltage 0 |
| `analog_input_voltage_1` | V | time | - | Analog input voltage 1 |
| `avalanche_photodiode_temperature` | degC | time | - | Avalanche photodiode temperature |
| `avalanche_photodiode_voltage` | V | time | - | Avalanche photodiode voltage |
| `box_temperature` | degC | time | - | Box temperature |
| `dD_to_dSA` | um^2 | diameter_aerodynamic | - | Surface area of one particle |
| `dD_to_dV` | um^3 | diameter_aerodynamic | - | Volume of one particle |
| `dead_time` | ms | time | - | Dead time |
| `diameter_aerodynamic` | um | diameter_aerodynamic | - | Midpoint of geometric mean aerodynamic diameter. |
| `digital_input_level_0` | 1 | time | - | Digital input level 0 |
| `digital_input_level_1` | 1 | time | - | Digital input level 1 |
| `digital_input_level_2` | 1 | time | - | Digital input level 2 |
| `event_1` | count | time | - | Single crossing event |
| `event_3` | count | time | - | Coincidence event |
| `event_4` | count | time | - | Over range event |
| `inlet_pressure` | hPa | time | - | Inlet pressure |
| `inlet_temperature` | degC | time | - | Inlet temperature |
| `laser_current` | mA | time | - | Laser current |
| `laser_power` | % | time | - | Laser power |
| `sheath_flow_rate` | L/min | time | - | Sheath flow rate |
| `sheath_pump_voltage` | V | time | - | Sheath pump voltage |
| `status_flags` | 1 | time | - | Status flags |
| `time` | - | time | - | Time offset from midnight |
| `total_flow_rate` | L/min | time | - | Total flow rate |
| `total_pump_voltage` | V | time | - | Total pump voltage |


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
                     params={"user": f"{user}:{token}", "ds": "enaaosapsC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enaaosapsC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enaaosapsC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enaaosapsC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("total_N_conc", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
38 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_dN_dlogDp"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("dN_dlogDp", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["dN_dlogDp", "total_N_conc", "total_SA_conc"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("enaaosapsC1.b1", "20160401", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The b1 processor (aosapscorr) produces a bit-packed qc_ companion variable for each reported quantity (e.g., qc_dN_dlogDp, qc_total_N_conc), following ARM's standard convention: zero means the sample passed every applied test, non-zero means one or more test bits are set, mapped to Indeterminate or Bad assessments. Data Quality Reports (DQRs) issued by the ARM Data Quality Office are a separate, higher-level assessment applied to both a0 and b1 datastreams at time of retrieval, flagging periods identified as suspect or incorrect. Guidance: screen qc_flags to exclude samples flagged Bad, treat...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Coincidence events at high concentration | Events with more than two crests (event 3) are tallied as counts but not sized; increases above ~1,000 particles/cm³, causing undercounting/bias in reported size distribution at high... | Manufacturer maximum recommended concentration limits and coincidence thresholds must be adhered to; coincident events are flagged in the datastream... | (hb p. 8) |
| Phantom particle (single-crest) events | Signals with only one crest (event 1, smallest particles) carry no time-of-flight and fall into the lowest channel rather than being properly sized | Excluded from size distribution calculations but logged separately for post-analysis correction | (hb p. 8) |
| Timer over-range events | Event 4 signals tallied as counts but not sized | - | (hb p. 10) |
| Lowest size bin exclusion at b1 | b1-level distribution has 51 bins instead of 52; the 0.505 µm bin is removed so the distribution begins at 0.542 µm, affecting integrated number/surface/volume concentrations | - | (hb p. 11) |
| No inlet-loss correction applied at b1 | b1 size distributions are not corrected for inlet losses since site-specific inlet-stack transmission efficiencies are unavailable | Users should consult Sections 3.1/3.2 (transmission loss discussion) and be aware inter-site comparisons carry uncertainty | (hb p. 11) |
| Unit-to-unit variability | Reported number size distributions differ measurably between individual APS units even after calibration; variability 10-20% for 0.9-3 µm particles, growing to as much as 60% below 0.9 µm | Considered acceptable for atmospheric measurements in 0.9-3 µm range; users should be aware variability increases outside this window; unit-specific... | (hb p. 6) |
| Reduced counting efficiency near lower size limit (less than 1 µm) | Measurement consistency declines significantly approaching the nominal 0.523 µm lower detection limit; counting efficiencies 85-99% across 0.8-10 µm per Volckens and Peters (2005) | - | (hb p. 18) |
| Flow deviations from nominal | Deviations in aerosol (1.0 ± 0.05 L/min) or sheath (4.0 ± 0.05 L/min) flow from nominal introduce systematic biases in both reported concentrations and aerodynamic diameters | Weekly flow verification against a NIST-traceable flow standard; adjust RA3 (sheath) and RA4 (aerosol) potentiometers per flow-calibration procedure... | (hb p. 6) |
| Sample-line RH/temperature conditioning effects | Sample RH not maintained below 40% (nafion dryer underperformance) can bias sizing/counting; expected slight exceedance (5-10%) in very humid climates | Perma Pure MD-700 nafion dryer maintains sample RH ≤ 40%; RH/T monitored upstream of APS to verify dryer performance | (hb p. 15) |
| Inlet impactor clogging | Sample pressure deviates from expected (1000±30 hPa), indicating impactor being clogged by debris | Monitored via DQ Explorer thresholds | (hb p. 14) |
| Site-specific inlet/sample-line transmission losses (super-micron) | Coarse-mode data differ across sites due to differing tubing length, diameter, bend count, and orientation; roll-off in transmission efficiency at smallest (~0.016 µm) and largest (~6.2 µm)... | Site-specific transmission efficiency measurements needed comparing near-inlet and post-manifold size distributions against a collocated APS or OPC... | (hb p. 17) |
| Laser degradation over operational lifetime | Laser power trends downward over 4,500-7,000 hours of continuous operation, degrading below threshold for reliable particle detection | Proactive monitoring and spare laser inventory management; schedule laser replacement before particle counting degrades (approx. 6-10 month... | (hb p. 19) |
| Pump wear/flow drift | Pump wear, filter loading, and ambient pressure/temperature changes cause flow drift affecting sizing accuracy | Weekly flow verification against NIST-traceable flow standard; inspect Parker Balston pump filter if pump voltages are noisy | (hb p. 19) |
| DAQ/communication failures | Intermittent data gaps documented at multiple AOS sites from DAQ communication failures between APS and site data system | Implement fail-safe watchdog protocols and automated data integrity checks; check serial communications and restart VI, escalate to mentor if... | (hb p. 19) |
| Merging APS aerodynamic sizing with SMPS/OPC data requires assumptions | Discrepancies appear when comparing APS aerodynamic-diameter distributions to SMPS mobility-diameter or OPC optical-equivalent-diameter distributions without accounting for particle density... | Requires assumptions about particle density and dynamic shape factor when merging datastreams | (hb p. 9) |
| Instrument status flags indicating fault conditions | Nine-bit status_flags indicate laser fault, total/sheath flow out of range, excessive sample concentration, accumulator clipped, autocal failed, internal temperature below 10°C or above... | Preserved at both a0 and b1 levels for screening | (hb p. 10) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Three-tier program: Tier 1 verifies instrument status, flows, optics, and zero-count baseline; Tier 2 verifies sizing accuracy with PSL spheres (modal diameter from lognormal fit within ±3-5% of certified size); Tier 3 performs full characterization and size-distribution closure against co-located SMPS and reference... (hb p. 21) |
| Calibration interval | Onsite calibration/validation scheduled per routine-check timetable; mentor onsite calibration/validation quarterly and 6-monthly; remote calibration/validation weekly; system zero-check quarterly, 6-monthly, and annually; factory service evaluated annually. (hb p. 21) |
| Traceability | NIST-traceable volumetric flow standard (e.g., Sensidyne Gilibrator 2.0); PSL spheres with certified sizes (hb p. 21) |
| Routine maintenance | Daily: confirm status lights and VI running; check sheath/total flow, sample/inlet pressure, pump voltages, error flags, laser current/power. Weekly: inner-nozzle cleaning, HEPA zero check, inlet flow verification. As needed: inspect/clean nafion dryer orifice and replace filter, inspect pump filter if voltages noisy.... (hb p. 19) |
| Maintenance interval | Daily and weekly preventive maintenance; quarterly/6-monthly/annual service per Table 6 (hb p. 19) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Scanning Mobility Particle Sizer (SMPS, TSI 3938), Optical Particle Counter (OPC, Grimm Model 11 D).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ACTRIS` | Aerosol, Clouds and Trace Gases Research Infrastructure |
| `AMF` | ARM Mobile Facility |
| `AOS` | Aerosol Observing System |
| `APD` | avalanche photodetector |
| `APS` | aerodynamic particle sizer |
| `BNC` | Bayonet Neill-Concelman coaxial cable connector |
| `BNF` | Bankhead National Forest |
| `DAQ` | data acquisition |
| `DQ` | data quality |
| `DQR` | Data Quality Report |
| `DST` | ARM site code for DUSTIEAIM campaign |
| `DUSTIEAIM` | Desert-Urban System Integrated Atmospheric Monsoon |
| `ENA` | Eastern North Atlantic |
| `FY` | fiscal year |


### References the handbook cites

- Bullard, RL, C Kuang, J Uin, S Smith, and SR Springston. 2017. Characterization of the ARM Aerosol Inlet and Sampling Losses. DOE/SC-ARM-TR-191.
- Kuang, C, and A Singh. 2024. Characterization of Transmission Losses of Particles with Dp greater than  1 µm in the Aerosol Observing System Inlet Stack. DOE/SC-ARM-TR-305.
- Pfeifer, S, T Müller, K Weinhold, N Zikova, S Martins dos Santos, A Marinoni, OF Bischof, C Kykal, L Ries, F Meinhardt, P Aalto, N Mihalopoulos, and A Wiedensohler. 2016. “Intercomparison of 15 aerodynamic particle...
- TSI Incorporated. Model 3321 Aerodynamic Particle Sizer (APS) Spectrometer Operation and Service Manual.
- Volckens, J, and TM Peters. 2005. “Counting and particle transmission efficiency of the Aerodynamic Particle Sizer.” Journal of Aerosol Science 36(12): 1400-1408.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf (28 pages, DOE/SC-ARM-TR-343, by A Singh, D Campos, T Subba)
- Catalog record: ARM data-source index, `instrument_class_code=aps`, read 2026-09-23
- Example file: `enaaosapsC1.b1.20260919.000000.nc` from `enaaosapsC1.b1`, 48.05 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
