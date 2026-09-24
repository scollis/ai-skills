---
name: arm-instrument-hvps-air
description: ARM High Volume Precipitation Spectrometer aboard aircraft (hvps-air) - handbook-derived instrument reference: measurement principle, reported quantities (Hydrometeor number concentration, Hydrometeor size distribution, Ice and liquid water content, Hydrometeor size), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafhvpsF1.c1) and the variable inventory of a real file. Use when working with hvps-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations; Cloud Properties. Triggers - hvps-air, High Volume Precipitation Spectrometer aboard aircraft, sgpaafhvpsF1.c1, Hydrometeor number concentration, Hydrometeor size distribution, Ice and liquid water content, Hydrometeor size, Airborne Observations, Cloud Properties, SPEC Inc. (Stratton Park Engineering) HVPS (HVPS V3), 2D-S, ACAPEX, ACE-ENA, CACTI.
---

# HVPS-AIR - High Volume Precipitation Spectrometer aboard aircraft

The HVPS is an open-path airborne optical instrument mounted below the wing of a research aircraft that measures the size, shape, and concentration of cloud droplets and ice crystals (hydrometeors larger than 150 µm) by recording two-dimensional shadowgraph images as particles cross a laser sample volume.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `hvps-air` |
| Handbook | [DOE/SC-ARM-TR-239 / S Glienke, F Mei / January 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-239.pdf) |
| Measurement category | Airborne Observations; Cloud Properties |
| Manufacturer / model | SPEC Inc. (Stratton Park Engineering) HVPS (HVPS V3) |
| Primary measurements | Hydrometeor Size Distribution; Hydrometeor concentration |
| Record | 2014-02-25 to 2023-08-15 (retired) |
| Datastreams with data | 7 across 6 sites |
| Sites | acx, cor, ena, mao, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/hvps-air |


## Credit

Everything this skill knows about the instrument is the work of **S Glienke, F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Glienke, F Mei. *High-Volume Precipitation Spectrometer (HVPS) Instrument Handbook*, DOE/SC-ARM-TR-239, January 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-239.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

A laser sheet throws a shadowgraph image of the hydrometeor (cloud droplets or ice crystals) in the sample volume onto a photodiode array. As the hydrometeor moves through the sample volume, the optical array continuously records the moving shadow, producing a two-dimensional image. The HVPS has 128 diodes in each array with an effective pixel size of 150 µm, so hydrometeors in the range 0.3-19.2 mm can be fully recorded at 150 µm resolution; larger particles can only be sized along the direction of flight using the air speed. Liquid water forms round or slightly deformed spherical droplets, allowing size and mass determination even from half-imaged droplets, while ice crystals have irregular shapes requiring assumptions about the third-dimension shape and ice density for water content derivation. At an air speed of 100 m/s, the sample volume is 310 l/s.

**Siting.** Open-path instrument located on the outside of the aircraft, typically below the wing, mounted in a standard particle measuring system (PMS) housing. An air speed greater than 10 m/s is necessary for correct sample volume determination (given for ARM aircraft). Often co-mounted with several other ARM cloud probes (e.g., during CACTI campaign).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Hydrometeor number concentration | #/liter | - | - | - | (hb p. 11) |
| Hydrometeor size distribution | #/liter/µm for each bin (61... | 0.3−19.2 mm fully recorded at 150 µm... | ±150 µm (pixel size) | 150 µm | (hb p. 11) |
| Ice and liquid water content | g/m^3 | - | - | - | (hb p. 11) |
| Hydrometeor size (two-dimensional images) | µm/mm | 150 µm to 19.2 mm fully imaged; larger... | ±150 µm | 150 µm | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Measurement range (full 2D imaging) | 0.3−19.2 mm at 150 µm resolution | (hb p. 7) |
| Minimum detectable particle size threshold | 150 µm | (hb p. 1) |
| Number of diodes per array | 128 | (hb p. 12) |
| Effective pixel size | 150 µm | (hb p. 12) |
| Sample volume (at 100 m/s air speed) | 310 l/s | (hb p. 1) |
| Size uncertainty | ±150 µm | (hb p. 12) |
| Number concentration uncertainty | ±sqrt(N), N = number of particles (Poisson counting statistics) | (hb p. 12) |
| Number of size bins | 61 bins | (hb p. 11) |


## The data

Verified example: **`sgpaafhvpsF1.c1`**, file `sgpaafhvpsF1.c1.20160920.202755.nc`
(0.87 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=4804, `optical_diameter`=37, `bound`=2 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:47:58 |
| dod version | aafhvps-c1-1.1 |
| process version | ingest-aafhvpsme-1.1-0.el7 |


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

```python
import act
files = armlive_list_files("sgpaafhvpsF1.c1", "2016-09-20", "2016-09-20")
ds = armlive_open("sgpaafhvpsF1.c1", "2016-09-20", "2016-09-20", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaafhvpsF1.c1", "20140225", "20260923")
```

The handbook's own note on data quality: Good data quality is ensured by comparison with other measurements. During sections of the flight known not to contain clouds or precipitation, the HVPS should also not record any images. Number concentrations and sizes should be comparable to other cloud probe measurements, and deviations should be investigated. Plots are generated using the ARM Data Quality Diagnostic Plot Browser (https://dq.arm.gov/dq-plotbrowser/).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Undersized/unreliable measurement of very small particles (near 150 µm) | Particles smaller than 300 µm cover only one or two pixels in the shadowgraph, giving unreliable size estimates | - | (hb p. 6) |
| Blind range for cloud droplets below detection limit | Water content computations are inaccurate when mostly cloud droplets are present, which are below the HVPS detectable range | - | (hb p. 6) |
| Ice water content assumption uncertainty | Derived ice water content depends on an assumed, highly variable ice density value | - | (hb p. 9) |
| Out-of-focus diffraction patterns | Hydrometeors outside the depth of field produce diffraction rings larger than the true particle size, with a bright area in the middle; rings often appear broken due to individual pixels;... | Accounted for in post-processing (user specifies methods for sizing out-of-focus particles) | (hb p. 6) |
| Edge-of-array undersizing | Particles up to 19.2 mm near the edge of the optical array may be undersized because only part of the shadowgraph image is recorded | - | (hb p. 6) |
| Air-speed dependence for large particles | Sizing of particles greater than 19.2 mm relies solely on air speed measurement accuracy since they exceed the full array width | Accurate determination of flight air speed required | (hb p. 6) |
| Shattering of hydrometeors on probe housing | Produces a multitude of smaller spurious particles, causing overestimate of small-particle counts or loss of detection | Sharp leading edges (anti-shattering tips) minimize shattering into sample volume; shatter-removal algorithm applied during post-processing (Korolev... | (hb p. 6) |
| Coincidence of multiple particles in sample volume | Can lead to underestimate of number concentration | - | (hb p. 6) |
| Data gaps outside cloud | Gaps in the number concentration time series correspond to periods outside clouds (e.g., highest/lowest altitudes above/below cloud show zero concentration) | - | (hb p. 3) |
| Raw data requires vendor post-processing software | Raw .HVPS files are not directly usable; must be processed with Playback/HVPSview before producing size distribution, concentration, or water content products | Use SPEC 2D-S software in HVPS mode for acquisition/playback and IDL-based HVPSview for further processing | (hb p. 8) |
| Software mode misconfiguration | Software defaults to 2D-S probe settings and must be manually switched to HVPS mode, otherwise processing may be incorrect | Change software into HVPS mode before use | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Probe sent to vendor for calibration and laser alignment; a spinning disk with known hole sizes is used to check size resolution (hb p. 15) |
| Calibration interval | Routinely performed in the laboratory before and after a field campaign; no calibration typically needed during deployment (hb p. 15) |
| Routine maintenance | Cleaning the probe windows to remove dirt (hb p. 15) |
| Maintenance interval | Before each flight (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: 2D-S (two-dimensional stereo probe), FCDP (Fast Cloud Droplet Probe).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `2D-S` | two-dimensional stereo probe |
| `AC` | alternating current |
| `ACAPEX` | ARM Cloud Aerosol Precipitation Experiment |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `DC` | direct current |
| `DOE` | U.S. Department of Energy |
| `HVPS` | high-volume precipitation spectrometer |
| `ICARTT` | International Consortium for Atmospheric Research on Transport and Transformation |
| `IDL` | Interactive Data Language |
| `NetCDF` | Network Common Data Form |
| `PMS` | particle measuring system |


### References the handbook cites

- HVPS Post-Processing Using HVPSview Software, User Manual. 2010.
- SPEC HVPS V3 Technical Manual (Rev. 1.2). 2013.
- Korolev, A. 2007. "Reconstruction of the Sizes of Spherical Particles from Their Shadow Images. Part I: Theoretical Considerations." Journal of Atmospheric and Oceanic Technology 24(3): 376−389.
- McFarquhar, GM, et al. 2017. "Processing of ice cloud in situ data collected by bulk water, scattering, and imaging probes: fundamentals, uncertainties, and efforts toward consistency." AMS Monographs 58: 11.1−11.33.
- SPEC 2007 (probe manual)

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-239.pdf (17 pages, DOE/SC-ARM-TR-239, by S Glienke, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=hvps-air`, read 2026-09-23
- Example file: `sgpaafhvpsF1.c1.20160920.202755.nc` from `sgpaafhvpsF1.c1`, 0.87 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
