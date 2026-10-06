---
name: arm-instrument-acsm
description: ARM Aerosol Chemical Speciation Monitor (acsm) - handbook-derived instrument reference. Measurement principle, reported quantities (Organics, Sulfate, Nitrate, Ammonium, Chloride, Aerosol size, Mass range), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaosacsmC1.b1) and the variable inventory of a real file. Use when working with acsm data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - acsm, Aerosol Chemical Speciation Monitor, sgpaosacsmC1.b1, Organics, Sulfate, Nitrate, Ammonium, Chloride, Aerosol size, Aerosols, Non-refractory, ACSM, HR-ToF-AMS, PILS.
---

# ACSM - Aerosol Chemical Speciation Monitor

The Aerosol Chemical Speciation Monitor is a thermal vaporization, electron impact ionization quadrupole mass spectrometer that measures real-time mass loading and chemical composition (organics, sulfate, nitrate, ammonium, chloride) of non-refractory sub-micron aerosol particles, deployed for long-term unattended monitoring at ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `acsm` |
| Handbook | [DOE/SC-ARM-TR-196 / TB Watson / August 2017](https://www.arm.gov/publications/tech_reports/handbooks/acsm_handbook.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | Aerodyne Research Aerosol Chemical Speciation Monitor (ACSM), built around the Pfeiffer Vacuum Prisma Residual Gas Analyzer (RGA) with Prisma Plus electronics |
| Primary measurements | Inorganic chemical composition; Organic Material Concentration |
| Record | 2010-11-18 to 2026-09-23 (active) |
| Datastreams with data | 40 across 16 sites |
| Sites | anx, asi, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mao, mos, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/acsm |


## Credit

Everything this skill knows about the instrument is the work of **TB Watson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> TB Watson. *Aerosol Chemical Speciation Monitor (ACSM) Instrument Handbook*, DOE/SC-ARM-TR-196, August 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/acsm_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The aerodynamic lens creates a ~1 mm diameter particle beam directed at a resistively heated particle vaporization source typically operated at 600 degC, mounted inside an electron impact ionization source that ionizes any vaporized particulate material. The ions formed are analyzed by a quadrupole mass spectrometer providing composition information. Three turbo molecular pumps provide differential pumping to separate gas from the particle beam, backed by an oil-free diaphragm pump. Because the ion source operates continuously, a background mass spectrum is always present and must be subtracted; this is done by alternating a 3-way valve between a filter position and a sample position at the completion of each full mass scan, yielding a "particle" spectrum and a "particle-free" spectrum whose difference contains the particle composition information. A small effusive naphthalene source mounted in the detection region provides a reference for mass-to-charge calibration, instrument stability, and ion transmission through the quadrupole mass filter.

**Siting.** Ambient aerosol-laden air is brought to the instruments through an 8\"-diameter external stack nominally 10 m above the roof of the enclosure at 800 lpm. Inside the stack, sample air flows through a 2\"-diameter stainless steel pipe at 120 lpm, split into four 30-lpm sample lines, one supplying the ACSM. The ACSM pulls sample through insulated 3/8-inch OD copper tubing; the line is insulated to prevent condensation in the air-conditioned enclosure interior. A water trap removes condensed liquid water, and the sample stream is dried with a Nafion dryer before entering the ACSM at 0.1 lpm through a 100 \u00b5m critical orifice.

**Sampling.** native rate 28 scans of aerosol sample and 28 scans of filtered background per averaging period; reported every 30 minutes; averaging 30 minutes averaging (results from 28 scans of aerosol sample and 28 scans of filtered background) (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Organics (total organic mass concentration) | µg m-3 | - | ± 30% | - | (hb p. 8) |
| Sulfate | µg m-3 | - | ± 30% | - | (hb p. 8) |
| Nitrate | µg m-3 | - | ± 30% | - | (hb p. 8) |
| Ammonium (NH4) | µg m-3 | - | ± 30% | - | (hb p. 8) |
| Chloride | µg m-3 | - | ± 30% | - | (hb p. 8) |
| Aerosol size (vacuum aerodynamic diameter) | - | 40 nm to 1 µm | - | - | (hb p. 9) |
| Mass range (m/z) | amu | 10 to 200 amu | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Data Rate | 30 minutes averaging | (hb p. 9) |
| Sample Flow | 85 cc min-1 (volumetric flow) | (hb p. 9) |
| Operating Pressure | Ambient | (hb p. 9) |
| Data Acquisition (DAQ) Control | Ethernet based | (hb p. 9) |
| Size/Weight | Bench top, 21” x 19.5” x 34”, 140 lbs [53.34 cm x 49.53 cm x 86.36 cm, 64 kg] | (hb p. 9) |
| Electric Power | 300 W; 85-264 VAC, 47-63 Hz | (hb p. 9) |
| Aerosol Size range | 40 nm to 1 µm (vacuum aerodynamic diameter) | (hb p. 9) |
| Mass range (m/z) | 10 to 200 amu | (hb p. 9) |
| Accuracy | ± 30% | (hb p. 9) |
| Sensitivity - Organic | 0.3 µg m-3 (30 minute, 3σ) | (hb p. 12) |
| Sensitivity - Sulfate | 0.4 µg m-3 (30 minute, 3σ) | (hb p. 12) |
| Sensitivity - Nitrate | 0.2 µg m-3 (30 minute, 3σ) | (hb p. 12) |
| Sensitivity - NH4 | 0.5 µg m-3 (30 minute, 3σ) | (hb p. 12) |
| Sensitivity - Chloride | 0.2 µg m-3 (30 minute, 3σ) | (hb p. 12) |
| Detection limit | less than 0.2 µg/m3 for 30 min of signal averaging | (hb p. 2) |
| Particle lens flow | ~0.1 LPM fixed by a 100 um-diameter critical aperture | (hb p. 6) |
| Main aerosol inlet system flow | 3 LPM for near isokinetic sampling conditions | (hb p. 6) |
| SEM gain (nominal) | 20,000 | (hb p. 5) |
| Vaporizer temperature (nominal) | 600 °C | (hb p. 2) |
| Emission current (nominal) | 1 mA | (hb p. 2) |
| Flow rate (nominal) | 1.4 cc sec-1 | (hb p. 2) |
| Inlet pressure closed (nominal) | 0.03 torr | (hb p. 2) |
| Inlet pressure open (nominal) | 1.3 torr | (hb p. 2) |


## The data

Verified example: **`sgpaosacsmC1.b1`**, file `sgpaosacsmC1.b1.20161222.001505.cdf`
(0.1 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=45, `bound`=2, `amus`=121 |
| Data variables | 20 |
| QC variables | 7 (`qc_` companions) |
| Median time step | 1727 s |
| File time span | 2016-12-22T00:15:05 to 2016-12-22T23:46:18 |
| sampling interval | 1 second |
| averaging interval | 30 minutes |
| dod version | aosacsm-b1-1.4 |
| process version | ingest-aosacsmcal-1.2-1.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `ammonium` | ug/m^3 | time | yes | Mass concentration of ammonium, ambient aerosol in air |
| `chloride` | ug/m^3 | time | yes | Mass concentration of chloride, ambient aerosol in air |
| `nitrate` | ug/m^3 | time | yes | Mass concentration of nitrate, ambient aerosol in air |
| `org_mx` | ug/m^3 | time,amus | yes | Organic mass spectral matrix |
| `org_mx_err` | ug/m^3 | time,amus | yes | Organic mass spectral error matrix |
| `sulfate` | ug/m^3 | time | yes | Mass concentration of sulfate, ambient aerosol in air |
| `total_organics` | ug/m^3 | time | yes | Mass concentration of total organics, ambient aerosol in air |
| `amus` | unitless | amus | - | Mass number to charge number ratio of ion fragments (m/z) |
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
                     params={"user": f"{user}:{token}", "ds": "sgpaosacsmC1.b1",
                             "start": "2016-12-22", "end": "2016-12-22", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaosacsmC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaosacsmC1.b1", "2016-12-22", "2016-12-22")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaosacsmC1.b1", "2016-12-22", "2016-12-22"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("total_organics", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

7 `qc_` companion variables cover 7 of the
20 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_total_organics"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("total_organics", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["total_organics", "ammonium", "sulfate"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpaosacsmC1.b1.20161222.001505.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `chloride` | Value is less than the fail_min. | 7 | 15.5556 |
| `ammonium` | Value is less than the fail_min. | 3 | 6.6667 |
| `org_mx` | Value is less than the fail_min. | 306 | 5.6198 |
| `chloride` | Value is greater than the fail_max. | 1 | 2.2222 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpaosacsmC1.b1", "20101118", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The handbook describes diagnostics based on monitoring the air beam signal (m/z 28, from nitrogen) present in all measurements, used to adjust mass concentrations for changes in detector sensitivity caused by aging; recalibration is suggested when the air peak decreases by 10%. ARM is developing procedures to evaluate instrument performance using this and other diagnostics going forward.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Critical orifice clogging with particulate material | Inlet pressure (displayed in ACSM Configuration and Control window) drops from the nominal value of 1.3 torr | Install a new orifice or clean the old orifice in an ultrasonic bath with distilled water and reinstall; use a 10µ cyclone impactor in the inlet... | (hb p. 18) |
| Turbo pump failure | Loss of vacuum and shutdown of the vacuum system; usually the small turbo pump (pump 3) fails, which shuts down the other pumps | Diagnose by restarting the backing pump (MD1) and starting turbo pumps individually; install a new turbo pump | (hb p. 19) |
| Ionizer element burnout | Ionizer element failure error message appears and the element 'on' check box becomes unchecked in the Vaporizer and Ionizer Control window; rechecking the box shuts the ionizer down | Switch to the second ionizer filament (Filament 2) by clicking the button so the green dot appears; Emiss mA and Max amps values should increase if... | (hb p. 19) |
| Prisma computer lockup | Loss of active status of the ACSM Configuration and Control window; failure to update filament amperage readings and Inlet (torr) reading | Reboot Prisma computer via software configuration menu and wait 5 minutes to reconnect; if failure to connect persists, perform hard reboot by... | (hb p. 19) |
| Continuous ion source background signal | A background mass spectrum is always present even absent particles, which would bias mass concentrations if not removed | Alternate 3-way valve between filter and sample position at completion of each mass scan and subtract the particle-free spectrum from the particle... | (hb p. 6) |
| Detector sensitivity aging/drift | Air beam signal (m/z 28, from nitrogen) decreases over time, indicating declining detector sensitivity | Monitor the air beam signal; recalibration suggested when the air peak decreases by 10% | (hb p. 9) |
| Impractical monthly calibration schedule due to shared/limited SMPS resources across... | Calibration intervals longer than the manufacturer-recommended monthly frequency, potentially larger drift in response factors between calibrations | ARM developing a calibration schedule to maximize frequency across instruments and evaluating air beam monitoring as a diagnostic | (hb p. 9) |
| Counting statistics error in mass spectra dependent on averaging time and counts | Error in mass signal (in counts) scales as a*sqrt(S); error increases at low signal/low averaging time, visible as larger scatter in low-concentration data | Use quadrature sum of open/closed signal errors and convert via measured NO3 calibration to estimate concentration uncertainty | (hb p. 10) |
| Non-refractory limitation | Any particulate material that cannot be vaporized at 600°C (refractory material such as black carbon, dust, sea salt) is not measured/detected by the ACSM | - | (hb p. 8) |
| Discrepancy with other instruments (slope deviation from unity) | Correlation slopes vs HR-ToF-AMS range from 0.76 (Organic) to 1.01 (Nitrate) with r2 from 0.81-0.91; slope vs PILS and SPA sulfate measurements both 0.69 with r2 0.77 and 0.85 respectively,... | - | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Sample Flow Rate Calibration (measuring sample flow rate versus inlet pressure with a Gilibrator or similar device); NO3 Response Factor (RF) calibration and NH4/SO4 Relative Ionization Efficiency (RIE) calibration using an aerosol generator, SMPS (DMA selecting 300 nm particles), dilution system, and CPC to generate... (hb p. 7) |
| Calibration interval | Manufacturer-recommended ideal calibration frequency is once a month, but monthly calibrations are not practical given shared SMPS resources across global deployment sites; recalibration suggested when air beam (m/z 28) peak decreases by 10% (hb p. 7) |
| Routine maintenance | Critical orifice replacement/cleaning (ultrasonic bath with distilled water); turbo pump replacement upon failure (commonly pump 3); switching ionizer filament (Filament 1/Filament 2) upon burnout; rebooting Prisma computer upon lockup (soft reboot via software menu, or hard reboot by unplugging power to Prisma... (hb p. 12) |
| Maintenance interval | Turbo pumps can fail after months of continuous operation; ionizer element burns out after several years of continuous operation (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: High-Resolution Time-of-Flight Aerosol Mass Spectrometer (HR-ToF-AMS), Particle-into-Liquid Sampler (PILS), Sulfate Particulate Analyzer (SPA), Scanning Mobility Particle Sizer (SMPS).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Non-refractory` | any particulate material that cannot be vaporized at 600 °C |
| `ACSM` | Aerosol Chemical Speciation Monitor |
| `AOS` | Aerosol Observing System |
| `DMA` | differential mobility analyzer |
| `HR-ToF-AMS` | High-Resolution Time-of-Flight Aerosol Mass Spectrometer |
| `PILS` | particle-into-liquid sampler |
| `PMF` | positive matrix factorization |
| `RF` | response factor |
| `RGA` | residual gas analyzer |
| `RIE` | relative ionization efficiency |
| `SEM` | secondary electron multiplier |
| `SMPS` | scanning mobility particle sizer |
| `SPA` | Sulfate Particulate Analyzer |
| `OPC` | Openness, Productivity, Collaboration (formerly Windows OLE for Process Control) |


### References the handbook cites

- Ng, NL, SC Herndon, A Trimborn, MR Canagaratna, PL Croteau, TB Onasch, D Sueper, DR Worsnop, Q Zhang, YL Sun, and JT Jayne. 2011. "An aerosol chemical speciation monitor (ACSM) for routine Monitoring of the composition...
- Budisulistiorini, SH, MR Canagaratna, PL Croteau, WJ Marth, K Baumann, ES Edgerton, SL Shaw, EM Knipping, DR Worsnop, JT Jayne, A Gold, and JD Surratt. 2013. "Real-time continuous characterization of secondary organic...
- Sun, Y, Z Wang, H Dong, T Yang, J Li, X Pan, P Chen, and JT Jayne. 2012. "Characterization of summer organic and inorganic aerosols in Beijing, China with an Aerosol Chemical Speciation Monitor." Atmospheric Environment...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/acsm_handbook.pdf (21 pages, DOE/SC-ARM-TR-196, by TB Watson)
- Catalog record: ARM data-source index, `instrument_class_code=acsm`, read 2026-09-23
- Example file: `sgpaosacsmC1.b1.20161222.001505.cdf` from `sgpaosacsmC1.b1`, 0.1 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
