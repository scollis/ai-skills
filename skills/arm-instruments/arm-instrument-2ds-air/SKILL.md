---
name: arm-instrument-2ds-air
description: ARM 2 Dimensional Stereo Probe aboard aircraft (2ds-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Cloud particle size distribution, Ice and liquid water content), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaaf2dsvF1.c1) and the variable inventory of a real file. Use when working with 2ds-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations; Cloud Properties. Triggers - 2ds-air, 2 Dimensional Stereo Probe aboard aircraft, sgpaaf2dsvF1.c1, Cloud particle size distribution, Ice and liquid water content, Airborne Observations, Cloud Properties, SPECInc (Stratton Park Engineering), Two-Dimensional Stereo (2D-S) Probe, 2D-S, ACE-ENA, CACTI.
---

# 2DS-AIR - 2 Dimensional Stereo Probe aboard aircraft

The 2D-S is an open-path airborne optical imaging probe mounted below an aircraft wing that measures the concentration, size, and stereo shadowgraph images of cloud droplets and ice crystals in the 25-3000 µm range.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `2ds-air` |
| Handbook | [DOE/SC-ARM-TR-233 / S Glienke, F Mei / November 2019](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-233.pdf) |
| Measurement category | Airborne Observations; Cloud Properties |
| Manufacturer / model | SPECInc (Stratton Park Engineering), Two-Dimensional Stereo (2D-S) Probe |
| Primary measurements | Cloud particle number concentration; Cloud particle size distribution |
| Record | 2014-02-15 to 2023-08-12 (retired) |
| Datastreams with data | 12 across 6 sites |
| Sites | acx, cor, ena, mao, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/2ds-air |


## Credit

Everything this skill knows about the instrument is the work of **S Glienke, F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Glienke, F Mei. *Two-Dimensional Stereo (2D-S) Probe Instrument Handbook*, DOE/SC-ARM-TR-233, November 2019.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-233.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The 2D-S uses two laser beams mounted perpendicular to each other, each casting a shadowgraph image of a hydrometeor onto a photodiode array as the particle moves through the sample volume. If the hydrometeor passes through the cross-section of both beams, both optical arrays record it, producing a stereo image; if it only shadows one beam, only that channel records the image, labeled "horizontal" or "vertical." As the particle moves through the beam, the optical array continuously records the moving shadow, building a two-dimensional image. Sizing along the direction of flight relies on knowing the aircraft's air speed, which becomes the sole basis for sizing particles larger than 1280 µm since they exceed the full array width. Post-processing must distinguish liquid from ice water because liquid droplets form round/near-spherical shapes enabling easier size and mass determination, while ice particles have irregular shapes requiring shape assumptions and an assumed (variable) ice density for water content derivation.

**Siting.** The probe is mounted in a standard Particle Measuring Systems (PMS) can below the wing of the aircraft. It has two independently sampling channels labeled "horizontal" (H) and "vertical" (V) with an overlap region in the center; these labels are arbitrary and depend on the exact orientation of the probe. An air speed greater than 0 m/s is necessary to define the sample volume correctly.

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Cloud particle number concentration | #/liter | - | Poisson counting statistics, ±sqrt(N) | - | (hb p. 12) |
| Cloud particle size distribution | #/liter/µm for each bin (61... | 25-1280 µm fully resolved at 10 µm... | ±10 µm (pixel size) | 10 µm | (hb p. 12) |
| Ice and liquid water content | g/m^3 | depends on size range of hydrometeors... | - | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Number of diodes per array | 128 diodes | (hb p. 12) |
| Effective pixel size | 10 µm | (hb p. 12) |
| Fully resolved particle size range | 25-1280 µm at 10 µm resolution | (hb p. 12) |
| Maximum particle size (flight-direction sizing only) | up to 3000 µm | (hb p. 12) |
| Size uncertainty | ±10 µm | (hb p. 13) |
| Number concentration uncertainty | ±sqrt(N) | (hb p. 13) |


## The data

Verified example: **`sgpaaf2dsvF1.c1`**, file `sgpaaf2dsvF1.c1.20160920.202755.nc`
(1.33 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4805, `optical_diameter`=61, `bound`=2 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:47:59 |
| dod version | aaf2dsv-c1-1.1 |
| process version | ingest-aaf2dsme-1.2-0.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `number_concentration` | count/L/um | time,optical_diameter | - | Number concentration |
| `optical_diameter` | um | optical_diameter | - | Optical diameter |
| `time` | - | time | - | Time offset from midnight |
| `total_number_concentration` | count/L | time | - | Total number concentration |


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
                     params={"user": f"{user}:{token}", "ds": "sgpaaf2dsvF1.c1",
                             "start": "2016-09-20", "end": "2016-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpaaf2dsvF1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpaaf2dsvF1.c1", "2016-09-20", "2016-09-20")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpaaf2dsvF1.c1", "2016-09-20", "2016-09-20"))   # cite what you pulled
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaaf2dsvF1.c1", "20140215", "20260923")
```

The handbook's own note on data quality: Good data quality is ensured by comparison with other measurements. During sections of flight known not to contain clouds or precipitation, the 2D-S should also not record any images. Number concentrations and sizes should be comparable to other cloud probe measurements, and deviations should be investigated. Plots are generated using the ARM Data Quality Diagnostic Plot Browser (https://dq.arm.gov/dq-plotbrowser/).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Undersized particles below 25 µm | Shadowgraph image covers only one or two pixels, sizing not considered reliable for particles smaller than 25 µm | Not considered reliable; effectively excluded from range | (hb p. 12) |
| Particles larger than 1280 µm sized only along flight direction | Particle size for objects greater than 1280 µm relies solely on air-speed-based sizing rather than full 2D image | Requires accurate air speed determination | (hb p. 12) |
| Inaccurate liquid/ice water content for small droplets | Water content values appear inaccurate when mostly very small cloud droplets are present below 2D-S detection range, or when ice crystal mass assumptions are inaccurate | None stated beyond noting the limitation | (hb p. 12) |
| Diffraction/ring patterns from out-of-focus particles | Small hydrometeors outside the depth of field produce diffraction patterns (rings) larger than their true size with a bright area in the middle; rings often appear broken due to individual... | Patterns can still be recorded; repeatability tested regularly during calibration | (hb p. 12) |
| Location-dependent diffraction pattern variability | The diffraction pattern of the same object looks different depending on its exact location relative to the photodiode array pixels | None stated | (hb p. 12) |
| Edge-of-array undersizing | Hydrometeors near the edge of the optical array may be undersized because only part of the shadowgraph image is recorded | None stated | (hb p. 12) |
| Air-speed dependent sizing error | Errors in flight-path sizing arise from inaccurate air speed determination, especially critical for particles greater than 1280 µm | Accurate air speed determination needed | (hb p. 12) |
| Out-of-focus particles produce diffraction rather than in-focus shadowgraph | Hydrometeors outside the depth of field show diffraction patterns instead of clear shadowgraph images | Can be a source of uncertainty if not accounted for in post-processing | (hb p. 12) |
| Shattering of hydrometeors on probe housing | A multitude of smaller particles appear, leading to overestimate of small particle concentrations | Sharp leading edges on the 2D-S minimize shattering into the sample volume | (hb p. 13) |
| Coincidence effects | Underestimate of number concentration when multiple particles are present simultaneously | None stated beyond noting Poisson-based uncertainty is affected | (hb p. 13) |
| Ice water content uncertainty from assumed ice density | Ice water content derivation depends on assumed ice density value, which is highly variable, leading to uncertainty | None stated beyond noting the assumption | (hb p. 15) |
| Out-of-cloud gaps in data | Gaps in number concentration data during periods outside clouds; highest and lowest altitudes above/below cloud show no cloud droplet concentration | Expected behavior, used as a data quality check (should show zero concentration outside cloud) | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration and laser alignment performed by sending the probe to the vendor; can be done using sized glass beads. (hb p. 11) |
| Calibration interval | No calibration typically needed during deployment. (hb p. 11) |
| Routine maintenance | Cleaning the probe windows to remove dirt before each flight. (hb p. 11) |
| Maintenance interval | Before each flight (hb p. 11) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: FCDP, HVPS, CPI.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `2D-S` | two-dimensional stereo probe |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `DOE` | U.S. Department of Energy |
| `IDL` | Interactive Data Language |
| `PMS` | Particle Measurements Systems |


### References the handbook cites

- Lawson, RP, D O'Connor, P Zmarzly, K Weaver, B Baker, Q Mo, and H Jonsson, 2006. "The 2D-S (Stereo) Probe: Design and Preliminary Tests of a New Airborne, High-Speed, High-Resolution Particle Imaging Probe." Journal of...
- SPEC 2D-S Technical Manual (Rev.3.1), February 2011.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-233.pdf (18 pages, DOE/SC-ARM-TR-233, by S Glienke, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=2ds-air`, read 2026-09-23
- Example file: `sgpaaf2dsvF1.c1.20160920.202755.nc` from `sgpaaf2dsvF1.c1`, 1.33 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
