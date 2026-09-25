---
name: arm-instrument-inletcvi-air
description: ARM Inlet for Counterflow Virtual Impactor aboard aircraft (inletcvi-air) - handbook-derived instrument reference. Measurement principle, reported quantities (CVI cut size, CVI enhancement factor, Dilution factor, CVI mode flag, CVI QC flag, Aircraft attitude warning flags, Large droplet warning flag, Inlet selector valve position), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafinletcviF1.c1) and the variable inventory of a real file. Use when working with inletcvi-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations. Triggers - inletcvi-air, Inlet for Counterflow Virtual Impactor aboard aircraft, sgpaafinletcviF1.c1, CVI cut size, CVI enhancement factor, Dilution factor, CVI mode flag, CVI QC flag, Aircraft attitude warning flags.
---

# INLETCVI-AIR - Inlet for Counterflow Virtual Impactor aboard aircraft

The CVI inlet, mounted on the ARM Aerial Facility's Gulfstream-1 aircraft, extracts cloud droplet and ice crystal residuals from the free air stream via inertial impaction against a counterflow of dry air so that in-cabin instruments can sample cloud element residues and coarse-mode aerosol separately from interstitial aerosol.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `inletcvi-air` |
| Handbook | [DOE/SC-ARM-TR-254 / LA Goldberger, MS Pekour, JM Hubbe / September 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-254.pdf) |
| Measurement category | Airborne Observations |
| Manufacturer / model | Brechtel Manufacturing, Inc. (BMI), Hayward, California - Counterflow Virtual Impactor Inlet System |
| Primary measurements | Hydrometeor size |
| Record | 2015-01-16 to 2026-09-23 (retired) |
| Datastreams with data | 8 across 4 sites |
| Sites | acx, cor, ena, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/inletcvi-air |


## Credit

Everything this skill knows about the instrument is the work of **LA Goldberger, MS Pekour, JM Hubbe** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> LA Goldberger, MS Pekour, JM Hubbe. *Counterflow Virtual Impactor (CVI) Inlet Aboard Aircraft (INLETCVI-AIR) Instrument Handbook*, DOE/SC-ARM-TR-254, September 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-254.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Warm, dry, particle-free carrier gas of known composition is pumped to the tip of the inlet in the direction opposite the incoming free-stream air, splitting the flow lines of that air. Larger droplets and ice crystals suspended in the sample air have enough inertia to penetrate this counterflow and enter the sample flow, while smaller, unactivated particles follow the streamlines of air flowing around the inlet's tip. The instrument samples cloud elements as a function of cut size by adjusting the counterflow velocity at the probe tip (F3 = F1 - F2, where F1 is the flow pumped to the tip, F2 returns with the sample air, and F3 exits the tip), with the cut size defined as the diameter at which penetration rate is 50%. The dry heated carrier gas also evaporates water from the hydrometeor, leaving residuals for sampling by in-cabin aerosol instrumentation. The CVI's performance as a concentrator is described via an enhancement factor relating ambient volumetric concentration to the concentration in the CVI sample line.

**Siting.** Mounted on the right-hand side window #1 of the G-1 aircraft (Gulfstream-159), below the isokinetic inlet, with probe pylon tall enough to sample in the free stream; mounting angle set to 9.7° down since 31 December 2012 to align the CVI tip with local flow; CVI head equipped with heating elements and gold-plated fairing cone/tip, and thermo-insulated body to improve low-temperature performance.

**Sampling.** native rate 1-Hz resolution (recorded with M300 data acquisition system and CVI controller/embedded PC); reported every 1 Hz raw; separate data files started for preflight tests and each flight; averaging Post-campaign processing averages all data over 1 min; missed data filled with NaNs (hb p. 4).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| CVI cut size | µm | minimum diameter of cloud element... | - | - | (hb p. 6) |
| CVI enhancement factor | unitless | - | - | - | (hb p. 6) |
| Dilution factor | unitless | applies in sub-isokinetic mode | - | - | (hb p. 3) |
| CVI mode flag | - | - | - | - | (hb p. 2) |
| CVI QC flag | 4-digit binary | 0000 = no errors/warnings | - | - | (hb p. 4) |
| Aircraft attitude warning flags (total speed, roll, pitch... | - | roll ±5°, pitch ±3°, speed 90-110 m/s... | - | - | (hb p. 4) |
| Large droplet warning flag | - | - | - | - | (hb p. 2) |
| Inlet selector valve position | - | - | - | - | (hb p. 2) |


## Specifications

| parameter | value | source |
|---|---|---|
| CVI cut size (typical) | ~13 microns for G-1 aircraft's CVI inlet | (hb p. 7) |
| Cut sharpness (sigma) | 1.28 to 1.34 (Shingler et al. 2012, for similar CVI) | (hb p. 6) |
| Mounting angle | 9.7° down (since 31 December 2012) | (hb p. 7) |
| Roll angle warning threshold | ±5° | (hb p. 4) |
| Pitch angle warning threshold | ±3° | (hb p. 4) |
| Normal sampling total air speed range | 90 to 110 m/s | (hb p. 4) |
| Post-processing nominal airspeed test range | greater than 90 and less than 105 m/s | (hb p. 10) |
| Input voltage (mains) | 110 VAC | (hb p. 9) |
| Input voltage (heater power) | 28 VDC round 16 pins, black-and-red wires | (hb p. 9) |
| Max anti-ice power | 725 watts at 28 VDC | (hb p. 9) |
| Total Sample Flow (Brechtel default) | 15 LPM | (hb p. 10) |
| Total Sample Flow (AAF setting) | 7.5 LPM | (hb p. 10) |
| Cloud droplet concentration flag threshold | total CAS counts less than  300 | (hb p. 10) |
| Large droplet test threshold | droplets outside CAS range greater than  5% of total CIP counts | (hb p. 10) |
| CAS laser beam cross-section area (S_L) | 0.24 mm^2 | (hb p. 11) |
| CAS measuring time interval (Δt) | 1 s | (hb p. 11) |
| Reynolds number range for stopping distance estimate | 0.5 less than  Re less than  500 | (hb p. 6) |
| First deployment | March 2010, CalWater field study | (hb p. 8) |


## The data

Verified example: **`sgpaafinletcviF1.c1`**, file `sgpaafinletcviF1.c1.20160920.202755.nc`
(0.35 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5104 |
| Data variables | 15 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aafinletcvi-c1-1.1 |
| process version | ingest-aafinletcvime-1.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cvi_cut_size` | um | time | yes | CVI cut size |
| `cvi_mode` | 1 | time | - | Inlet mode state |
| `enhancement_factor` | 1 | time | - | CVI enhancement factor |
| `inlet_dilution_factor` | 1 | time | - | Inlet dilution factor for under-kinetic mode |
| `inlet_selector` | 1 | time | - | Inlet selector valve position |
| `large_droplet_warning` | 1 | time | - | Large droplet warning. Probability of sampling a large size droplet |
| `pitch_warning` | 1 | time | - | Pitch angle warning (angle of attack) |
| `roll_warning` | 1 | time | - | Roll angle warning |
| `time` | - | time | - | Time offset from midnight |
| `total_air_speed_warning` | 1 | time | - | Total air speed warning |


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
                     params={"user": f"{user}:{token}", "ds": "sgpaafinletcviF1.c1",
                             "start": "2016-09-20", "end": "2016-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaafinletcviF1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaafinletcviF1.c1", "2016-09-20", "2016-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaafinletcviF1.c1", "2016-09-20", "2016-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cvi_cut_size", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
15 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_cvi_cut_size"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("cvi_cut_size", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["cvi_cut_size"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaafinletcviF1.c1.20160920.202755.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `cvi_cut_size` | Transition between CVI modes | 85 | 1.6654 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaafinletcviF1.c1", "20150116", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging based on mentor-developed criteria: a 4-digit binary QC flag reports CVI controller errors (cut size bad), roll angle beyond ±5°, pitch angle beyond ±3°, and total air speed outside 90-110 m/s. Large droplet entry into the sample flow is separately flagged due to possible break-up in the inlet. The handbook recommends using data from aerosol inlets only during level flight. Bad or missing-value placeholder is -9999.0. Post-processing also applies additional tests: level-flight masking (GPS rollgreater than 5°/pitchgreater than 3°), aircraft...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Droplet break-up in inlet for large droplets | Large droplet warning flag set true; possible spikes/inconsistency in cloud residual concentrations when large droplets enter sample flow | Times when large droplets enter sample flow are noted/flagged | (hb p. 11) |
| Aircraft attitude disturbance of airflow around inlet | Aircraft roll beyond ±5° or pitch beyond ±3° flagged; biased aerosol sample during maneuvers | Use data from aerosol inlets only during level flight; roll/pitch warning flags included | (hb p. 11) |
| CVI controller problem | First bit of 4-digit binary QC flag set; cut size reported as bad | Flagged as error, cut size marked bad | (hb p. 4) |
| Total air speed out of normal sampling range (90-110 m/s, or 90-105 m/s in... | Fourth bit of QC flag set; data flagged out during speed test | Flag data with speed outside nominal operational range | (hb p. 4) |
| No real-time monitoring of CVI cut size | Cut size field appears constant or unavailable in real-time stream; only available after post-processing | Cut size determined during post-processing | (hb p. 3) |
| Time frame not adjusted for CVI internal residence time/delay in lines | Apparent timing offset between CVI-derived variables and cloud probe data unless corrected | Data reported in cloud probe time frame with no adjustment; post-processing sequence introduces ~10 s time shift for sensors behind CVI (CVI CPC,... | (hb p. 3) |
| Particle loss in CVI inlet and sample lines | Cloud droplet residue concentration in CVI line lower than expected relative to cloud probe measured concentration; cut size estimates shift when loss accounted for | Shingler et al. (2012) provides transmission efficiency curves; described as 'worst case' since they ignore droplet evaporation effects that would... | (hb p. 8) |
| Droplet/ice crystal shattering near CVI probe, pylon, aircraft body, wings, propellers | Anomalously high concentrations of small particles/interstitial aerosol appearing in CVI sample, complicating cut-size determination | None specified beyond acknowledging complication | (hb p. 9) |
| Interstitial aerosol penetration ('piggyback' in wake of cloud droplets) | Unwanted small aerosol particles appear in CVI sample alongside droplet residues | None specified | (hb p. 9) |
| Cut sharpness resolution limited by particle sizing instrument resolution | Measured cut sharpness (sigma) estimates have a natural low limit; sigma reported as 1.28-1.34 by Shingler et al. 2012 | None specified; noted as inherent limitation | (hb p. 6) |
| Icing on CVI inlet | Ice accumulation on CVI structures observed in test flights, potential flow line distortion | Inlet outfitted with heating elements to prevent icing; icing tests performed with plastic tube accumulation surface | (hb p. 7) |
| Low cloud droplet concentration causing unreliable cut-size estimate | Data flagged out when total CAS counts less than  300 | Cloud droplet concentration test flags out low concentration data | (hb p. 10) |
| Wide cloud droplet spectrum / large droplet test | Data flagged when number of droplets outside CAS range is above 5% of total CIP counts | Large droplet test flags such data | (hb p. 10) |
| Add Flow instability affecting counterflow calculation | Counterflow (Addflow minus Sample flow) set to NaN when Add flow not stable within averaging period | Averaged value of counterflow set to NaN if Add Flow unstable | (hb p. 10) |
| Sub-isokinetic mode dilution requiring correction | Particle number concentration in CVI lines needs multiplier (dilution factor) to restore ambient concentration | Apply dilution factor as multiplier to restore ambient concentration | (hb p. 3) |
| Historical inconsistency in dataset naming/formats across campaigns | Different datastream names (aafinletcvi, inleticvi-air, cvi-air) and formats (netCDF, ICARTT, CSV) depending on campaign/year | Check campaign-specific readme file in IOP archive | (hb p. 3) |
| Missing/bad data placeholder | Values of -9999.0 appear in data fields | Recognize -9999.0 as bad or missing-value placeholder | (hb p. 5) |
| No real-time cut size / configuration flow mismatch | Incorrect setting of Total Sample Flow vs Instrument Sample Flow in configuration file leads to incorrect counterflow and thus incorrect CVI cut size | Set Total Sample Flow and Instrument Sample Flow correctly in configuration file before runtime; AAF uses 7.5 LPM vs Brechtel default of 15 LPM | (hb p. 14) |
| Contamination from Add Flow gas source (compressed air bottles) or heater | Particle concentration detected at test ports upstream/downstream of Add Flow heater indicating contamination | Two HEPA capsules in series to remove particulates; verified with CPC (TSI 3010) at test ports | (hb p. 14) |
| Heavy aerosol loading (e.g., smoke) contaminating inlet faster than normal cleaning... | Increased particle loading or fouling requiring more frequent cleaning | Accelerated cleaning schedule recommended for environments with heavy aerosol loadings such as smoke | (hb p. 15) |
| Instrument currently not in use / no monthly summaries | No monthly summary reports generated; dataset not actively produced during Challenger 850 modification period | None; simply noted as not routinely used | (hb p. 5) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Characterized against cloud droplet distribution from cloud and aerosol spectrometer (CAS); mounting angle and flow distortion verified using a Rosemount 5-port gust probe on loan from CIRPAS; CVI positioning validated by location/orientation of ice accumulation on CVI structures (hb p. 15) |
| Calibration interval | Flow angle estimated on 11 November 2012, 30 November 2012, and 30 November 2012; mounting angle unchanged since 31 December 2012 (hb p. 15) |
| Traceability | Calibration procedures and records maintained by the instrument mentor; calibration database maintained by AAF's Director of Engineering (hb p. 15) |
| Routine maintenance | Inlet should be cleaned before every campaign; two test ports (upstream/downstream of Add Flow heater) used to check for leaks and verify no aerosol particles introduced into Add Flow from heater or gas bottles (via CPC measurement); ports made of standard Swagelok Ts (hb p. 15) |
| Maintenance interval | Before every campaign, with accelerated cleaning schedule recommended for heavy aerosol loading environments (e.g., flying through smoke) (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: OPC-AIR (optical particle counter, inlet housekeeping data), isokinetic aerosol inlet, cloud and aerosol spectrometer (CAS), cloud droplet probe (CDP), condensation particle counter (CPC, TSI 3010).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `CVI` | Counterflow virtual impactor |
| `AAF` | ARM Aerial Facility |
| `G-1` | Gulfstream-159 aircraft |
| `C50` | CVI cut size, diameter of smallest particle for which penetration rate is 50% |
| `Enhancement factor...` | Atip*Vplane / qSample, describing CVI performance as a concentrator |
| `Dilution factor` | Multiplier applied to particle number concentration measured in CVI lines during... |
| `CAS` | Cloud and aerosol spectrometer |
| `CDP` | Cloud droplet probe |
| `CPC` | Condensation particle counter |
| `OPC` | Optical particle counter |
| `MFC` | Mass flow controller |
| `TANS` | Tactical Air Navigation System |
| `ICARTT` | International Consortium for Atmospheric Research on Transport and Transformation |


### References the handbook cites

- Anderson, TL, RJ Charlson, and DS Covert. 1993. Calibration of a Counterflow Virtual Impactor at aerodynamic diameters from 1 to 15 µm. Aerosol Science and Technology 19(3): 317-329.
- Hinds, WC. 1999. Aerosol Technology: Properties, Behavior, and Measurement of Airborne Particles. 2nd ed. Wiley-Interscience, New York.
- Noone, KJ, JA Ogren, J Heintzenberg, RJ Charlson, and DS Covert. 1988. Design and calibration of a counterflow virtual impactor for sampling of atmospheric fog and cloud droplets. Aerosol Science and Technology 8(3):...
- Noone, KJ, H-C Hansson, and RKAM Mallant. 1992. Droplet Sampling from Crosswinds: An Inlet Efficiency Calibration. Journal of Aerosol Science 23(2): 153-164.
- Shingler, T, S Dey, A Sorooshian, FJ Brechtel, Z Wang, A Metcalf, M Coggon, J Mülmenstädt, LM Russell, HH Jonsson, and JH Seinfeld. 2012. Characterization and airborne deployment of a new counterflow virtual impactor...
- Willeke, K, and P Baron. 2001. Aerosol Measurement: Principles, Techniques, and Applications. Van Nostrand Reinhold, New York.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-254.pdf (22 pages, DOE/SC-ARM-TR-254, by LA Goldberger, MS Pekour, JM Hubbe)
- Catalog record: ARM data-source index, `instrument_class_code=inletcvi-air`, read 2026-09-23
- Example file: `sgpaafinletcviF1.c1.20160920.202755.nc` from `sgpaafinletcviF1.c1`, 0.35 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
