---
name: arm-instrument-sp2
description: ARM Single Particle Soot Photometer (sp2) - handbook-derived instrument reference. Measurement principle, reported quantities (rBC mass loading, Measurement range, Sensitivity, Sensitivity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (bnfaossp2xrM1.b1) and the variable inventory of a real file. Use when working with sp2 data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Atmospheric Carbon. Triggers - sp2, Single Particle Soot Photometer, bnfaossp2xrM1.b1, rBC mass loading, Measurement range, Sensitivity, Aerosols, Atmospheric Carbon, Revision "C" and Revision "D" units referenced, ACME-V, Fullerene soot, Incandescence, Nd:YAG.
---

# SP2 - Single Particle Soot Photometer

The SP2 measures, in situ at the single-particle level, the time-dependent light-scattering and laser-induced incandescence signals of individual BC-containing (refractory black carbon, rBC) particles as they pass through a continuous-wave Nd:YAG laser beam, deployed as a rack-mounted instrument for ground or aircraft-based sampling of ambient aerosol.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 24 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sp2` |
| Handbook | [DOE/SC-ARM-TR-169 / AJ Sedlacek / February 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf) |
| Measurement category | Aerosols; Atmospheric Carbon |
| Manufacturer / model | Droplet Measurement Technologies (DMT) Single Particle Soot Photometer (SP2); Revision "C" and Revision "D" units referenced |
| Primary measurements | Black carbon concentration |
| Record | 2012-11-14 to 2026-09-23 (active) |
| Datastreams with data | 17 across 10 sites |
| Sites | blr, bnf, crg, dst, epc, guc, hou, kcg, mos, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/sp2 |


## Credit

Everything this skill knows about the instrument is the work of **AJ Sedlacek** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> AJ Sedlacek. *Single-Particle Soot Photometer (SP2) Instrument Handbook*, DOE/SC-ARM-TR-169, February 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `sp2-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `sp2`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The SP2 uses the high intra-cavity optical power of a continuous-wave Nd:YAG laser; particles traversing the beam scatter light, and any light-absorbing (black or elemental carbon) material in the particle absorbs laser energy until it is heated to incandescence. The incandescence signal amplitude is related to the amount of refractory black carbon (rBC) material in the particle, and binning individual incandescence signals per sample volume yields the rBC mass concentration (ng/m3), while binning by volume equivalent diameter (VED) yields the size distribution (dN/dlogDVED) per unit time. Because the SP2 detects and sizes single particles, it also yields black carbon number concentration, and this mass measurement is independent of particle mixing state. A separate scattering detector detects single-particle scattering at 1064 nm and can be used to infer BC mixing state and to detect non-BC-containing aerosol number/mass concentrations. The full scattering and/or incandescence response of each particle is fully digitized (100 points per channel at 400 ns/pt) for detailed offline analysis.

**Siting.** Not explicitly specified beyond deployment context; instrument is rack-mounted (19" rack, 5U, 24" deep) and has been deployed both in ground-based settings (e.g., MAOS) and aircraft (e.g., ACME-V field campaign).

**Sampling.** native rate Each channel: 100 points of data at 400 ns/pt time resolution; raw data recorded per particle event; reported every Time series of raw incandescence and scattering signal counts displayed every second (units counts/cc); averaging Time response: 10 seconds for aircraft-based deployments and 60-seconds for ground deployments (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| rBC mass loading (mass concentration) | ng/m3 | - | - | - | (hb p. 8) |
| rBC volume equivalent size distribution | dN/dlogDVED | - | - | particle-resolved | (hb p. 8) |
| Measurement range (particle concentration) | particles/cc | 1-12,500 particles/cc at 120 vccm... | - | - | (hb p. 12) |
| Sensitivity (mass concentration) | ng/m3 | - | - | 10 ng/m3 | (hb p. 12) |
| Sensitivity (per-particle mass) | fg/particle | - | - | 0.3 fg/particle | (hb p. 13) |


## Specifications

| parameter | value | source |
|---|---|---|
| Sample flow rate | 0.120 liters per minute (default; can be changed as necessary for loading conditions) | (hb p. 11) |
| Purge flow | provided internally | (hb p. 11) |
| Cell pressure | ambient | (hb p. 11) |
| Power usage | ~ 300 watts (@120 VAC) | (hb p. 11) |
| Weight | ~190 kg | (hb p. 11) |
| Size | ~65 cm x 43 cm x 23 cm (length x width x height) (19" rack mount, 5U, 24" deep) | (hb p. 12) |
| Measurement range | 1-12,500 particles/cc at 120 vccm (0 – 25,000 particles/sec; concentrations increases until particles become coincident) | (hb p. 12) |
| Resolution | particle-resolved | (hb p. 12) |
| Precision (measurement spec) | less than  20% | (hb p. 12) |
| Time response | 10 seconds for aircraft-based deployments and 60-seconds for ground deployments | (hb p. 12) |
| Span drift | negligible | (hb p. 12) |
| Accuracy | less than  10%: Calibration dependent. Fullerene soot used (Laborde et al., 2012; Gysel et al., 2011) | (hb p. 12) |
| Precision | 30%; goes as sqrt(N), where N is the number of detected particles | (hb p. 12) |
| Sensitivity | 10 ng/m3; 0.3 fg/particle | (hb p. 12) |
| Uncertainty | ~25% (May et al., 2014) | (hb p. 13) |
| Input Voltage | ~350 W; 100-250 VAC (50-60 Hz) | (hb p. 13) |


## The data

Verified example: **`bnfaossp2xrM1.b1`**, file `bnfaossp2xrM1.b1.20260919.000001.nc`
(8.46 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=86398, `rBC_mass_bin`=100, `bound`=2, `scatter_diam_bin`=100 |
| Data variables | 16 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2026-09-19T00:00:01 to 2026-09-19T23:59:59 |
| dod version | aossp2xr-b1-1.0 |
| process version | ingest-aossp2xr-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cavity_pressure` | hPa | time | - | Air pressure in cavity |
| `inlet_air_temp` | degC | time | - | Air temperature at the inlet to the case |
| `rBC_bins` | count | time,rBC_mass_bin | - | Number of particles in incandescence bins |
| `rBC_mass_bin` | fg | rBC_mass_bin | - | Incandescent particle mass bin midpoint (geometric mean) |
| `rBC_mass_conc` | ng/m^3 | time | - | Number of incandescent particles multiplied by the size information... |
| `rBC_particle_conc` | count/cm^3 | time | - | Concentration of all particles showing an incandescent signal, with... |
| `sample_flow_read_mass` | cm^3/min | time | - | Mass flow reading from the sample flow controllers in sccm |
| `sample_flow_read_volume` | cm^3/min | time | - | Volumetric flow reading from the sample flow controller |
| `scatter_bins` | count | time,scatter_diam_bin | - | Number of particles in scattering bins |
| `scatter_diam_bin` | nm | scatter_diam_bin | - | Scattering particle diameter bin midpoint (geometric mean) |
| `scattering_particle_conc` | count/cm^3 | time | - | Concentration of particles showing only a scattering signal,... |
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
                     params={"user": f"{user}:{token}", "ds": "bnfaossp2xrM1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./bnfaossp2xrM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "bnfaossp2xrM1.b1", "2026-09-19", "2026-09-19")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("bnfaossp2xrM1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("bnfaossp2xrM1.b1", "20121114", "20260923")
```

The handbook's own note on data quality: Data is Quality-Controlled (QCd) by the instrument mentor after an IOP-based field deployment before submission to the ARM Archive. The housekeeping, log, and initialization files are used to monitor instrument health status but are only relevant to the SP2 mentor and are not provided as user data products.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Particle coincidence at high concentration | Measured particle concentration deviates from linear response and appears to saturate/roll off as true concentration increases beyond ~12,500 particles/cc (25,000 particles/sec), since... | Stay within stated measurement range (1-12,500 particles/cc at 120 vccm) | (hb p. 12) |
| Non-rBC incandescence signals (interferents such as dust, metals, or spurious signals) | Incandescence signal appears in broadband channel without corresponding expected narrowband signature, or vice versa, indicating a non-BC source | Use narrowband channel in combination with broadband channel to filter out non-rBC incandescence signals (e.g., from dust, metals, or spurious... | (hb p. 2) |
| Calibration material mismatch/uncertainty (Fullerene soot vs. ambient BC) | Derived rBC mass may carry calibration-dependent bias since no mono-dispersed black carbon particles exist for direct calibration; requires assumed particle density as function of mobility... | Use Fullerene soot (preferred over manufacturer-recommended Aquadag) because its morphology more closely mimics ambient BC; estimate particle mass... | (hb p. 14) |
| Desiccant saturation in purge line under humid conditions | Condensation build-up in purge line; potential contamination/failure of flow controllers | Periodically refresh or replace desiccant in the drying cartridge on the purge line | (hb p. 15) |
| Non-zero particle counts during zero check | Instrument records more than an occasional particle when sampling through a HEPA/high-efficiency filter, indicating a fault | If not near-zero, contact DMT for support | (hb p. 15) |
| Laminar flow element (LFE) calibration drift in particle-laden environments | Sample flow reading (Sample Flow LFE) deviates from expected ~120 vccm or from linear voltage-flow relationship | Check/recalibrate the LFE using bubble flow meter procedure described in Section 13.1 if operated in a highly particle-laden environment | (hb p. 15) |
| Laser optical power degradation / contamination of laser optics | Laser power drops and cannot be recovered by minor alignment | Attempt cleaning of optics (coupler surface first); replace coupler if cleaning fails; consult DOC-0229 SP2 Laser Alignment Manual; keep a... | (hb p. 16) |
| Charge-multiplet peaks in DMA calibration | Calibration histograms show several peaks corresponding to particles with charge 1, 2, 3, etc., which can confuse mass-vs-peak-height calibration if not properly identified | Conduct first data analysis with mid-range-size particles so the charge-1 aerosol peak is seen clearly | (hb p. 15) |
| Mixing-state data product requires additional QC/QA | Scattering-channel-derived mixing-state data product not available as a standard output; requires special processing | Produced only on a requested basis since additional detailed analysis and QC/QA must be conducted | (hb p. 1) |
| Precision scales with number of detected particles (counting statistics) | Precision degrades (approaches 30%) at low particle counts, improving as sqrt(N) with increasing N | None stated beyond noting the sqrt(N) dependence | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Incandescence channel calibrated using commercially available Fullerene soot; scattering channel calibrated using five different PSL (polystyrene latex) standards; calibration also performed using an aerosol generator and classifier (DMA) providing particles in the 50-500 nm size range, taking ~10 data points between... (hb p. 14) |
| Calibration interval | Routinely calibrated at the beginning, during, and at the end of a field campaign; if deployment is longer than 12 months, calibrated approximately every 6 months (hb p. 14) |
| Traceability | ARM uses fullerene soot rather than manufacturer-recommended Aquadag because fullerene soot particle morphology more closely mimics ambient BC; requires knowledge of particle density as function of mobility size to estimate actual particle mass; no known mono-dispersed black carbon particles currently available for... (hb p. 14) |
| Routine maintenance | Periodically refresh or replace desiccant in the drying cartridge on the purge line; perform occasional particle zero check using a HEPA or other high-efficiency filter on the SP2 inlet; if operated in a highly particle-laden environment, may need to check calibration of the laminar flow element (LFE) on the sample... (hb p. 15) |
| Maintenance interval | Occasional/periodic (as needed); routine desiccant check; particle zero check occasional (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ACME-V` | ARM Airborne Carbon Measurements V Field Campaign |
| `AI` | analog input |
| `DMA` | differential mobility analyzer |
| `DMT` | Droplet Measurement Technologies (manufacturer of SP2) |
| `DVM` | digital volt meter |
| `fg` | Femtogram (10-9) |
| `Fullerene soot` | Calibration standard for the SP2 incandescence channel |
| `Incandescence` | laser-induced black body emission from rBC particle |
| `Nd:YAG` | Neodymium-doped yttrium aluminium garnet—crystal used as a lasing medium |
| `NIR` | near-infrared |
| `PSL` | PolyStyrene Latex spheres—calibration standard for particle scattering |
| `QC` | Quality Control |
| `QA` | Quality Assurance |
| `rBC` | Refractory Black Carbon |


### References the handbook cites

- Baumgardner, D, G Kok, and G Raga. 2004. Geophysical Research Letters 31(6): L06117.
- Gao, RS, et al. 2007. Aerosol Science and Technology 41(2): 125-135.
- Gysel, M, M Laborde, JS Olfert, R Subramanian, and AJ Grohn. 2011. Atmospheric Measurement Techniques 4(12): 2851-2858.
- Laborde, M, et al. 2012. Atmospheric Measurement Techniques 5(12): 3077-3097.
- May, AA, et al. 2014. Journal of Geophysical Research - Atmospheres 119(20): 11,826-11,849.
- Moteki, N, and Y Kondo. 2007. Aerosol Science and Technology 41(4): 398-417.
- Schwarz, JP, et al. 2010. Aerosol Science and Technology 44(8): 612-628.
- Schwarz, JP, et al. 2006. Journal of Geophysical Research – Atmospheres 111: D16207.
- Schwarz, JP, AE Perring, MZ Markovic, RS Gao, S Ohata, J Langridge, D Law, R McLaughlin, and DW Fahey. 2015. Journal of Aerosol Science 81: 110-126.
- Sedlacek, AJ, ER Lewis, L Kleinman, J Xu, and Q Zhang. 2012. Geophysical Research Letters 39(6).

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf (24 pages, DOE/SC-ARM-TR-169, by AJ Sedlacek)
- Catalog record: ARM data-source index, `instrument_class_code=sp2`, read 2026-09-23
- Example file: `bnfaossp2xrM1.b1.20260919.000001.nc` from `bnfaossp2xrM1.b1`, 8.46 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
