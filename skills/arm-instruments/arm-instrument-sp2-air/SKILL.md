---
name: arm-instrument-sp2-air
description: ARM Single Particle Soot Photometer aboard aircraft (sp2-air) - handbook-derived instrument reference. Measurement principle, reported quantities (rBC mass loading, Measurement range, Sensitivity, Sensitivity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaaafsp2rbc10sF1.c1) and the variable inventory of a real file. Use when working with sp2-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations. Triggers - sp2-air, Single Particle Soot Photometer aboard aircraft, nsaaafsp2rbc10sF1.c1, rBC mass loading, Measurement range, Sensitivity, Aerosols, Airborne Observations, Droplet Measurement Technologies (DMT), Single Particle Soot Photometer (SP2), ACME-V, Fullerene soot, Incandescence, Nd:YAG.
---

# SP2-AIR - Single Particle Soot Photometer aboard aircraft

The SP2 measures, in situ aboard aircraft, the time-dependent light scattering and laser-induced incandescence signals of individual refractory black carbon (rBC)-containing particles to derive their mass concentration and size distribution.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 24 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `sp2-air` |
| Handbook | [DOE/SC-ARM-TR-169 / AJ Sedlacek / February 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf) |
| Measurement category | Aerosols; Airborne Observations |
| Manufacturer / model | Droplet Measurement Technologies (DMT), Single Particle Soot Photometer (SP2); Revision "C" and Revision "D" |
| Primary measurements | Black carbon concentration |
| Record | 2015-06-04 to 2019-04-29 (retired) |
| Datastreams with data | 4 across 3 sites |
| Sites | cor, ena, nsa |
| ARM page | https://www.arm.gov/capabilities/instruments/sp2-air |


## Credit

Everything this skill knows about the instrument is the work of **AJ Sedlacek** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> AJ Sedlacek. *Single-Particle Soot Photometer (SP2) Instrument Handbook*, DOE/SC-ARM-TR-169, February 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `sp2` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `sp2-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The SP2 uses the high intra-cavity optical power of a continuous-wave Nd:YAG laser through which individual particles pass. Light-absorbing particles (mainly black or elemental carbon) absorb laser energy until heated to the point of incandescence, and the amplitude of this incandescence signal is related to the amount of refractory material in the particle, giving a mass measurement independent of particle mixing state. All particles, whether absorbing or not, scatter light, and a scattering detector detects single-particle scattering at 1064 nm, which can indicate black carbon mixing state at the single-particle level. Because the SP2 detects single particles, it can measure both black carbon mass concentration and number concentration. The full scattering and/or incandescence response of each particle is completely digitized for detailed analysis.

**Sampling.** native rate Each individual channel is made up of 100 points of data with a time resolution of 400 ns/pt; reported every 10 seconds for aircraft-based deployments and 60-seconds for ground deployments; averaging rBC mass loading and size distribution binned per unit time; per unit sample volume for mass concentration (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| rBC mass loading (mixing ratio) | ng/m3 | - | - | - | (hb p. 8) |
| rBC volume equivalent size distribution | dN/dlogDVED | - | - | - | (hb p. 8) |
| Measurement range (particle concentration) | particles/cc | 1-12,500 particles/cc at 120 vccm... | - | particle-resolved | (hb p. 12) |
| Sensitivity (mass concentration) | ng/m3 | - | 10 ng/m3 | - | (hb p. 12) |
| Sensitivity (per particle mass) | fg/particle | - | 0.3 fg/particle | - | (hb p. 13) |


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
| Time response | 10 seconds for aircraft-based deployments and 60-seconds for ground deployments. | (hb p. 12) |
| Span drift | negligible | (hb p. 12) |
| Accuracy | less than  10%: Calibration dependent. Fullerene soot used (Laborde et al., 2012; Gysel et al., 2011) | (hb p. 12) |
| Precision | 30%; goes as sqrt(N), where N is the number of detected particles. | (hb p. 12) |
| Sensitivity | 10 ng/m3; 0.3 fg/particle | (hb p. 12) |
| Uncertainty | ~25% (May et al., 2014) | (hb p. 13) |
| Input Voltage | ~350 W; 100-250 VAC (50-60 Hz) | (hb p. 13) |
| Number of raw data channels | 8 channels: high- and low-gain broadband incandescence (~350-800 nm), high- and low-gain narrowband incandescence (~630-800 nm), high- and low-gain... | (hb p. 8) |
| Time resolution per channel point | 400 ns/pt (100 points per channel) | (hb p. 8) |
| Optics reflectivity | 99.97% or better | (hb p. 16) |


## The data

Verified example: **`nsaaafsp2rbc10sF1.c1`**, file `nsaaafsp2rbc10sF1.c1.20150827.213000.nc`
(1.27 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1487, `bound`=2, `diameter_geo`=200 |
| Data variables | 10 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 10 s |
| File time span | 2015-08-27T21:30:00 to 2015-08-28T01:37:40 |
| averaging interval | 10 sec |
| dod version | aafsp2rbc10s-c1-1.0 |
| process version | ingest-aafsp2rbcme-1.0-2.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `rBC` | ng / m^3 | time | yes | Refractory black carbon concentration |
| `N_dN_rBC` | count / cm^3 | time,diameter_geo | - | Number density of particles containing refractory black carbon |
| `diameter_geo` | um | diameter_geo | - | Mean volume-equivalent geometric diameter |
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
                     params={"user": f"{user}:{token}", "ds": "nsaaafsp2rbc10sF1.c1",
                             "start": "2015-08-27", "end": "2015-08-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsaaafsp2rbc10sF1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsaaafsp2rbc10sF1.c1", "2015-08-27", "2015-08-27")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsaaafsp2rbc10sF1.c1", "2015-08-27", "2015-08-27"))   # cite what you pulled
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
10 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_rBC"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("rBC", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["rBC"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (nsaaafsp2rbc10sF1.c1.20150827.213000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `rBC` | Value is less than rBC_min_alarm | 202 | 13.5844 |
| `rBC` | Value is equal to missing_value | 191 | 12.8447 |
| `rBC` | Value is less than rBC_min_warning | 72 | 4.842 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsaaafsp2rbc10sF1.c1", "20150604", "20260923")
```

The handbook's own note on data quality: Data is Quality-Controlled (QCd) by the instrument mentor after an IOP-based field deployment before submission to the ARM Archive. The scattering-channel-derived mixing-state data product is produced only on a requested basis since additional detailed analysis and QC/QA must be conducted.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Particle coincidence at high concentration | Measured particle concentration plateaus or deviates from linearity as true concentration increases until particles become coincident within the laser beam, biasing counts low at high... | - | (hb p. 12) |
| Unknown particle density for Fullerene soot calibration standard | Derived rBC mass calibration depends on assumed particle density as a function of mobility size; errors in this assumption propagate to mass accuracy | Determine particle density as a function of mobility size to derive a good estimate of actual particle mass; no known mono-dispersed black carbon... | (hb p. 14) |
| Non-rBC incandescence signals (e.g., dust, metals, spurious signals) | Incandescence signal detected in broadband channel without corresponding expected narrowband signature, or anomalous incandescence events not matching rBC signal shape | Narrowband channel used in combination with broadband channel to filter out non-rBC incandescence signals | (hb p. 8) |
| Desiccant saturation in purge line drying cartridge | Condensation build-up in purge line; potential flow controller malfunction/failure visible as flow instability or dropout in housekeeping flow data | Periodically refresh or replace the desiccant in the drying cartridge on the purge line | (hb p. 21) |
| Non-zero particle counts on HEPA-filtered zero check | Instrument records more than an occasional particle when sampling through a HEPA filter, indicating contamination or instrument fault | If zero check fails, contact DMT for support | (hb p. 21) |
| Laminar flow element (LFE) calibration drift in particle-laden environments | Sample flow rate readings (Sample Flow LFE) deviate from expected ~120 vccm or from linear voltage-to-flow relationship | Check and recalibrate the LFE per the SP2-D procedure (linear regression of flow rate vs. voltage, update Offset and Linear parameters in AI Channels... | (hb p. 21) |
| Laser optics contamination/degradation | Drop in laser power that cannot be recovered by minor alignment | Verify other parameters (e.g., pump laser power); attempt cleaning of optics (likely contamination on coupler surface first); replace coupler if... | (hb p. 22) |
| Additional QC/QA needed for mixing-state data product from scattering channel | Mixing-state-derived data product not available by default; only produced on request due to need for additional detailed analysis | Data product produced on a requested-basis since additional detailed analysis and QC/QA must be conducted | (hb p. 7) |
| Precision degrades with low particle counts | Precision (~30%) scales as sqrt(N); statistical uncertainty larger when detected particle number N is small (e.g., low concentration periods) | - | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Incandescence calibration accomplished using commercially available Fullerene soot; scattering channel calibrated using five different PSL standards. Calibration via DMA-classified particles (50-500 nm size range) with mass vs. peak height polynomial fit. (hb p. 14) |
| Calibration interval | Routinely calibrated at the beginning, during, and at the end of a field campaign; if campaign/deployment is longer than 12 months, calibrated approximately every 6 months. (hb p. 14) |
| Traceability | Fullerene soot preferred over manufacturer-recommended Aquadag because particle morphology more closely mimics ambient BC; particle density as function of mobility size must be known to estimate actual particle mass. Efforts underway to transfer calibrations into the Operations Status System (OSS) database. (hb p. 14) |
| Routine maintenance | Periodically refresh or replace the desiccant in the drying cartridge on the purge line. Occasional particle zero check using a HEPA or high-efficiency filter on the SP2 inlet. If operated in a highly particle-laden environment, may need to check calibration of the laminar flow element (LFE) on the sample inlet. (hb p. 21) |
| Maintenance interval | periodic/occasional (not further specified) (hb p. 21) |


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
| `rBC` | Refractory Black Carbon |
| `SP2` | single-particle soot photometer |
| `VED` | volume equivalent diameter—a void-free sphere |


### References the handbook cites

- Baumgardner, D, G Kok, and G Raga. 2004. Warming of the Arctic lower stratosphere by light absorbing particles. Geophysical Research Letters 31(6): L06117.
- Gao, RS, et al. 2007. A novel method for estimating light-scattering properties of soot aerosols using a modified Single-Particle Soot Photometer. Aerosol Science and Technology 41(2): 125-135.
- Gysel, M, M Laborde, JS Olfert, R Subramanian, and AJ Grohn. 2011. Effective density of Aquadag and fullerene soot black carbon reference materials used for SP2 calibration. Atmospheric Measurement Techniques 4(12):...
- Laborde, M, et al. 2012. Single Particle Soot Photometer intercomparison at the AIDA chamber. Atmospheric Measurement Techniques 5(12): 3077-3097.
- May, AA, et al. 2014. Aerosol emissions from prescribed fires in the United States. Journal of Geophysical Research - Atmospheres 119(20): 11,826-11,849.
- Moteki, N, and Y Kondo. 2007. Effects of mixing state on black carbon measurements by laser-induced incandescence. Aerosol Science and Technology 41(4): 398-417.
- Schwarz, JP, et al. 2010. The detection efficiency of the Single Particle Soot Photometer. Aerosol Science and Technology 44(8): 612-628.
- Schwarz, JP, et al. 2006. Single-particle measurements of midlatitude black carbon and light-scattering aerosols from the boundary layer to the lower stratosphere. Journal of Geophysical Research – Atmospheres 111:...
- Schwarz, JP, et al. 2015. Technique and theoretical approach for quantifying the hygroscopicity of black-carbon-containing aerosol using a single particle soot photometer. Journal of Aerosol Science 81: 110-126.
- Sedlacek, AJ, et al. 2012. Determination of and evidence for non-core-shell structure of particles containing black carbon using the Single-Particle Soot Photometer (SP2). Geophysical Research Letters 39(6).

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-169.pdf (24 pages, DOE/SC-ARM-TR-169, by AJ Sedlacek)
- Catalog record: ARM data-source index, `instrument_class_code=sp2-air`, read 2026-09-23
- Example file: `nsaaafsp2rbc10sF1.c1.20150827.213000.nc` from `nsaaafsp2rbc10sF1.c1`, 1.27 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
