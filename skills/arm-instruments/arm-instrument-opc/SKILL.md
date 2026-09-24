---
name: arm-instrument-opc
description: ARM Optical Particle Counter (opc) - handbook-derived instrument reference. Measurement principle, reported quantities (Number concentration, Light-scattering intensity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfminiaosopcM1.b1) and the variable inventory of a real file. Use when working with opc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Cloud Properties. Triggers - opc, Optical Particle Counter, bnfminiaosopcM1.b1, Number concentration, Light-scattering intensity, Aerosols, Cloud Properties, TSI Incorporated, Aerodynamic Particle Sizer (APS) Model 3321, ACTRIS, DUSTIEAIM, HEPA, NetCDF.
---

# OPC - Optical Particle Counter

The TSI Aerodynamic Particle Sizer (APS) Model 3321 measures the aerodynamic diameter and light-scattering intensity of airborne solid and non-volatile liquid particles from 0.5 to 20 µm via time-of-flight, and is deployed within the ARM Aerosol Observing System (AOS) sampling from a common inlet manifold to characterize coarse-mode aerosol size distributions.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 28 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `opc` |
| Handbook | [DOE/SC-ARM-TR-343 / A Singh, D Campos, T Subba / August 2026](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf) |
| Measurement category | Aerosols; Cloud Properties |
| Manufacturer / model | TSI Incorporated, Aerodynamic Particle Sizer (APS) Model 3321 |
| Primary measurements | Aerosol concentration; Aerosol particle size distribution |
| Record | 2021-09-01 to 2026-09-23 (active) |
| Datastreams with data | 19 across 7 sites |
| Sites | bnf, crg, epc, guc, hou, kcg, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/opc |


## Credit

Everything this skill knows about the instrument is the work of **A Singh, D Campos, T Subba** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> A Singh, D Campos, T Subba. *Aerodynamic Particle Sizer (APS) Instrument Handbook*, DOE/SC-ARM-TR-343, August 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `aps` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `opc`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The APS 3321 measures aerodynamic particle size using a time-of-flight principle: the aerosol sample is accelerated through a nozzle, and particles pass through two partially overlapping laser beams that create a double-crested beam profile. Larger particles accelerate more slowly due to inertia, producing a longer peak-to-peak time of flight — resolved at 4 ns resolution — which is mapped to aerodynamic diameter via an internal calibration curve. A valid single-particle event generates a signal with exactly two crests ("event 2"); signals with only one crest (phantom particles, "event 1") or more than two crests (coincidence events, "event 3") are excluded from size distribution calculations but logged separately for post-analysis correction. Because coincidence increases with particle concentration, the manufacturer provides maximum recommended concentration limits and coincidence thresholds to ensure reported number and mass size distributions reflect only well-characterized single-particle events. Sheath flow precisely aligns and accelerates particles through the measurement region, minimizing particle recirculation.

**Siting.** The APS draws from the main AOS inlet manifold via a vertical, dedicated sample line, with horizontal runs and bends kept to a minimum to limit gravitational and inertial particle losses. A Perma Pure MD-700 nafion dryer (24-inch active length with crossflow purge) sits upstream of the APS, holding sample RH at ≤40% consistent with ACTRIS/GAW guidance. RH and temperature can be monitored just upstream of the APS to verify dryer performance. Sampling configuration is site-specific and constrained by available rack space; bends observed at ENA and BNF may result in more losses than the configuration at AMF1 and SGP, but only AMF1 transmission loss has been characterized. The SGP APS currently...

**Sampling.** native rate 1 Hz (raw, unpolled records over RS-232); reported every 1 s (programmable sampling time); averaging b1 level integrates size-distribution into total number, surface-area, and volume concentrations from the 51-bin (a0: 52-bin) distribution (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerodynamic particle diameter / number size distribution | µm (size); dN/dlogDp in... | 0.5-20 µm aerodynamic; 0.3-20 µm... | ±10% of reading plus variation from counting... | 0.02 µm at 1.0 µm; 0.03 µm... | (hb p. 7) |
| Number concentration | #/cm³ | up to 1,000 #/cm³ at 0.5 µm (less than... | ±10% of reading plus variation from counting... | - | (hb p. 7) |
| Total/surface-area/volume concentration (derived, b1) | 1/cm³, nm²/cm³, nm³/cm³ | - | - | - | (hb p. 11) |
| Light-scattering intensity (side-scatter) | counts across channels | 64 side-scatter channels (accumulator);... | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Measurement Technique | Time-of-flight, double-crested optical system, single high-speed timing processor | (hb p. 7) |
| Particle type | Airborne solids and non-volatile liquids | (hb p. 7) |
| Size range | 0.5-20 µm aerodynamic; 0.3–20 µm optical (PSL equivalent) | (hb p. 7) |
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

Verified example: **`bnfminiaosopcM1.b1`**, file `bnfminiaosopcM1.b1.20260629.000002.nc`
(7.1 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=14393, `bound`=2, `diameter_midpoint`=32 |
| Data variables | 36 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 6 s |
| File time span | 2026-06-29T00:00:02 to 2026-06-29T23:59:57 |
| sampling interval | 6 second |
| dod version | miniaosopc-b1-1.0 |
| process version | ingest-miniaosopccorr-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `calc_dust_weight` | ug | time | yes | Calculated dust weight that has passed the measuring cell since the... |
| `pump_current_consumption` | % | time | yes | Pump current consumption |
| `sample_relative_humidity` | % | time | yes | Calculated relative humidity of the sample air in the measuring cell |
| `sample_temperature` | degC | time | yes | Measured temperature at the measuring cell |
| `air_pressure` | hPa | time | - | Air pressure |
| `air_volume` | L | time | - | Volume of air that has passed the measuring cell since the last... |
| `dD_to_dSA` | um^2 | diameter_midpoint | - | Surface area of one particle |
| `dD_to_dV` | um^3 | diameter_midpoint | - | Volume of one particle |
| `dN_dlogDp` | 1/cm^3 | time,diameter_midpoint | - | Number size distribution |
| `diameter_midpoint` | um | diameter_midpoint | - | Diameter midpoint of aerosol particles |
| `error_code` | 1 | time | - | Error code |
| `flow_rate_percent` | % | time | - | Flow rate |
| `flow_sensor` | L/min | time | - | Flow sensor volume |
| `gravimetric_factor` | 1 | time | - | Gravimetric factor |
| `high_laser_current` | mA | - | - | High laser current |
| `low_laser_current` | mA | - | - | Low laser current |
| `particle_count` | 1/cm^3 | time,diameter_midpoint | - | Particle counts |
| `photodiode_dark_voltage` | mV | - | - | Photodiode voltage when the laser diode is switched off |
| `photodiode_high_voltage` | mV | - | - | Photodiode voltage when the laser diode is switched on |
| `preamplifier_voltage` | mV | - | - | DC voltage of the preamplifier without bias |
| `sum_particle_count` | 1/cm^3 | time,diameter_midpoint | - | Raw summed particle counts |
| `time` | - | time | - | Time offset from midnight |
| `total_N_conc` | 1/cm^3 | time | - | Total number concentration from size distribution, OPC |
| `total_SA_conc` | um^2/cm^3 | time | - | Total surface area concentration from size distribution, OPC |
| `total_V_conc` | um^3/cm^3 | time | - | Total volume concentration from size distribution, OPC |
| `zero_count_dark` | count | - | - | Counts without particles or zero count with the laser switched off |
| `zero_count_high` | count | - | - | Counts without particles or zero count with the laser switched on |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("bnfminiaosopcM1.b1", "2026-06-29", "2026-06-29")
ds = armlive_open("bnfminiaosopcM1.b1", "2026-06-29", "2026-06-29", cleanup_qc=True)
```

## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
36 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfminiaosopcM1.b1", "20210901", "20260923")
```

The handbook's own note on data quality: The instrument status_flags (nine-bit) are preserved at both a0 and b1 levels: laser fault; total flow out of range; sheath flow out of range; excessive sample concentration; accumulator clipped; autocal failed; internal temperature below 10°C; internal temperature above 40°C; detector voltage beyond ±10% of Vb. B1 additionally carries a bit-packed qc_ companion variable for each reported quantity (e.g., qc_dN_dlogDp, qc_total_N_conc) following ARM's standard convention: zero means the sample passed every applied test, non-zero means one or more test bits are set, mapped to Indeterminate or...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Discrepancy with target instrument | The provided handbook text is titled 'Aerodynamic Particle Sizer (APS) Instrument Handbook' (DOE/SC-ARM-TR-343) and describes a TSI APS 3321, not the requested 'Optical Particle Counter... | - | (hb p. 1) |
| Phantom particles (single-crest events) | Event 1 signals with only one crest carry no time-of-flight and fall into the lowest channel; excluded from sized channels but logged separately | Excluded from size distribution calculations but logged separately for post-analysis correction | (hb p. 8) |
| Coincidence events | Signals with more than two crests (event 3, three or more crests) are tallied as counts but not sized; increases with particle concentration, typically above 1,000 particles/cm3 | Manufacturer provides maximum recommended concentration limits and coincidence thresholds; flagged in datastream and can be used to apply... | (hb p. 8) |
| Timer over-range events | Event 4 signals tallied as counts but not sized | - | (hb p. 10) |
| Lowest channel exclusion at b1 level | First size bin (0.505 um) removed going from a0 (52 channels) to b1 (51 channels); distribution begins at 0.542 um | Integrated number, surface, and volume concentrations at b1 are based on 51 size bins | (hb p. 11) |
| No inlet-loss correction at b1 | b1 size distributions not corrected for inlet losses because site-specific inlet-stack transmission efficiencies are unavailable | See Sections 3.1/3.2 (transmission efficiency characterization) for more details | (hb p. 11) |
| Unit-to-unit variability | Reported number size distributions differ by 10-20% between 0.9-3 um and up to 60% below 0.9 um across different APS units (Pfeifer et al. 2016); complicates inter-site comparisons | Awareness that variability increases outside 0.9-3 um window; systematic intercomparison campaigns recommended | (hb p. 6) |
| Reduced counting efficiency near lower size limit | Measurement consistency declines significantly approaching nominal lower detection limit of 0.523 um; counting efficiencies of 85-99% found across 0.8-10 um range (Volckens and Peters 2005) | - | (hb p. 18) |
| High concentration coincidence bias | Above ~1,000 particles/cm3, coincident events detected but not sized, biasing counting accuracy | Flagged in datastream and can be used to apply concentration corrections in post-processing | (hb p. 6) |
| Flow deviations bias sizing and concentration | Deviations in aerosol (1.0 L/min) or sheath (4.0 L/min) flow from nominal introduce systematic biases in reported concentrations and aerodynamic diameters | Weekly flow verification against NIST-traceable flow standard; adjust RA3/RA4 potentiometers per flow-calibration procedure | (hb p. 6) |
| Site-specific transmission losses uncharacterized | Only AMF1 inlet-stack transmission efficiency has been characterized; other sites (ENA, BNF, SGP, NSA, AMF2) not quantified, so applying uniform corrections or comparing coarse-mode data... | Site-specific transmission efficiency measurements needed comparing near-inlet and post-manifold size distributions against collocated reference | (hb p. 16) |
| Transmission efficiency roll-off at size limits | TE approaches unity (+/-10-15% daily std dev) from ~0.02 to 4.0 um; TE50 at 0.016 um (lower) and 6.2 um (upper); roll-off indicates stack losses from diffusion at smallest sizes and... | - | (hb p. 17) |
| Sample RH excursions | Sample RH maintained below 40% via nafion dryer; in very humid climates slight exceedance (5-10%) is expected, which can bias sizing (hygroscopic growth) | Single-tube nafion dryer (Perma Pure MD-700, 24-inch drying length); RH/temperature monitored upstream of APS to verify dryer performance | (hb p. 9) |
| Sample pressure / impactor clogging | Sample pressure deviating from 1000+/-30 hPa downstream of inlet impactor indicates degree of impactor clogging by debris | Monitored via DQ Explorer thresholds | (hb p. 8) |
| Laser degradation | Laser power trends downward over 4,500-7,000 hours of continuous operation before degrading below threshold for reliable particle detection | Monitor trend and schedule laser replacement proactively; keep spare laser inventory | (hb p. 19) |
| Flow/pump drift | Pump wear, filter loading, and ambient pressure/temperature changes cause flow drift affecting sizing accuracy | Weekly flow verification against NIST-traceable flow standard | (hb p. 19) |
| DAQ communication failures | Intermittent data gaps documented at multiple AOS sites from DAQ communication failures between APS and site data system | Implement fail-safe watchdog protocols and automated data integrity checks | (hb p. 19) |
| Merging with SMPS/OPC diameters requires assumptions | APS reports aerodynamic diameter; merging with SMPS (mobility diameter) or OPC (optical-equivalent diameter) requires assumptions about particle density and dynamic shape factor, seen as... | - | (hb p. 9) |
| Failed HEPA zero check | Non-zero background counts on HEPA-filtered air | Reclean inner nozzle, confirm inlet tube seated and knurled ring hand tight, rerun zero; persistent counts may indicate leak or contaminated optics | (hb p. 20) |
| Status flag faults | Nine-bit status_flags may indicate laser fault, total/sheath flow out of range, excessive sample concentration, accumulator clipped, autocal failed, internal temperature below 10C or above... | - | (hb p. 10) |
| Repeated/persistent flags or VI gaps | Gaps in the VI/data ingest or repeated flags | Check serial communications and restart the VI; escalate to mentor if unresolved | (hb p. 20) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Three-tier program: Tier 1 verifies instrument status, flows, optics, zero-count baseline; Tier 2 verifies sizing accuracy with PSL standards (700, 1,000, and 2,500 nm) using lognormal-fit modal diameter within +/-3-5% of certified size; Tier 3 performs full characterization and size-distribution closure against... (hb p. 21) |
| Calibration interval | Onsite calibration/validation scheduled per routine-check timetable: remote calibration/validation weekly-ish (per Table 6, listed under a recurring column), mentor onsite calibration/validation quarterly and 6-monthly, system zero-check quarterly/6-monthly/annual, factory service evaluated annually (hb p. 21) |
| Traceability | NIST-traceable volumetric flow standard (e.g., Sensidyne Gilibrator 2.0); PSL spheres of certified size (hb p. 21) |
| Routine maintenance | Daily: confirm Power/Flow/Laser/Particle status lights ON, VI running and updating every second; check sheath flow 4.0+/-0.05 LPM and total flow 5.0+/-0.05 LPM; sample/inlet pressure (bpress) 1000+/-30 hPa; sheath-pump and total-pump voltages 2.8+/-0.3 V; error flags = 00; laser current 47-55 mA and laser power... (hb p. 13) |
| Maintenance interval | Daily, Weekly, Quarterly, 6-Monthly, Annual (per Table 6 schedule) (hb p. 13) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: scanning mobility particle sizer (SMPS, TSI 3938), optical particle counter (OPC, Grimm Model 11 D).

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
- Pfeifer, S, et al. 2016. Intercomparison of 15 aerodynamic particle sizers (APS 3321): uncertainties in particle sizing and number size distributions. Atmospheric Measurement Techniques 9(4): 1545-1551.
- TSI Incorporated. Model 3321 Aerodynamic Particle Sizer (APS) Spectrometer Operation and Service Manual.
- Volckens, J, and TM Peters. 2005. Counting and particle transmission efficiency of the Aerodynamic Particle Sizer. Journal of Aerosol Science 36(12): 1400-1408.
- Wiedensohler, A, et al. 2012. Mobility particle size spectrometers: harmonization of technical standards and data structure. Atmospheric Measurement Techniques 5(3): 657-685.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-343.pdf (28 pages, DOE/SC-ARM-TR-343, by A Singh, D Campos, T Subba)
- Catalog record: ARM data-source index, `instrument_class_code=opc`, read 2026-09-23
- Example file: `bnfminiaosopcM1.b1.20260629.000002.nc` from `bnfminiaosopcM1.b1`, 7.1 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
