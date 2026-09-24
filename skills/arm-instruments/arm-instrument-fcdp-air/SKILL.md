---
name: arm-instrument-fcdp-air
description: ARM Fast Cloud Droplet Probe aboard aircraft (fcdp-air) - handbook-derived instrument reference: measurement principle, reported quantities (Cloud particle size distribution, Liquid water content), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaaffcdpF1.c1) and the variable inventory of a real file. Use when working with fcdp-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Airborne Observations; Cloud Properties. Triggers - fcdp-air, Fast Cloud Droplet Probe aboard aircraft, sgpaaffcdpF1.c1, Cloud particle size distribution, Liquid water content, Airborne Observations, Cloud Properties, SPEC Inc. (Stratton Park Engineering) FCDP, 2D-S, ACE-ENA, CACTI, FCDP.
---

# FCDP-AIR - Fast Cloud Droplet Probe aboard aircraft

The FCDP is an open-path aircraft-mounted instrument (typically below the wing) that uses forward light scattering from a laser to detect and size cloud droplets in the 1.5-50 µm diameter range, yielding cloud particle number concentration, size distribution, and liquid water content.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 16 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `fcdp-air` |
| Handbook | [DOE/SC-ARM-TR-238 / S Glienke, F Mei / January 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-238.pdf) |
| Measurement category | Airborne Observations; Cloud Properties |
| Manufacturer / model | SPEC Inc. (Stratton Park Engineering) FCDP |
| Primary measurements | Cloud particle number concentration; Cloud particle size distribution |
| Record | 2014-02-22 to 2023-08-12 (retired) |
| Datastreams with data | 6 across 6 sites |
| Sites | acx, cor, ena, mao, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/fcdp-air |


## Credit

Everything this skill knows about the instrument is the work of **S Glienke, F Mei** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> S Glienke, F Mei. *Fast Cloud Droplet Probe (FCDP) Instrument Handbook*, DOE/SC-ARM-TR-238, January 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-238.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The FCDP is an open-path instrument mounted on the outside of the aircraft, with a sample volume lying between its two forward-pointing arms. A laser is focused on the sample volume, which is continuously monitored along the flight path, and when a droplet passes through it the laser light is scattered, which is used to detect and size the droplet. Within the probe there are two detectors, the "sizer" and the "qualifier," both of which measure light scattered at ca. 4-12 degrees in a forward direction, but the qualifier is masked whereas the sizer is not. In a regular droplet event the qualifier measures a higher signal than the sizer, which is the criterion for accepting and counting the droplet; if the droplet is out of focus, the scattered light is more diffuse and the qualifier signal will be less than the sizer signal, rejecting the event. Only single droplets at a time are detected, and sizes measured over one second must be averaged to obtain a size distribution; the method assumes spherical particles, so it does not yield useful information for ice clouds.

**Siting.** The FCDP is an open-path instrument mounted on the outside of the aircraft, typically below the wing; an air speed greater than 10 m/s is necessary to define the sample volume, which is given for ARM aircraft. It can be mounted with a collar provided by the vendor in conjunction with the two-dimensional stereo (2D-S) probe.

**Sampling.** native rate continuous monitoring along flight path; single droplets detected individually; reported every sizes measured over one second are averaged to obtain a size distribution; averaging 1 second averaging for size distribution (hb p. 7).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Cloud particle number concentration | #/liter | - | ±sqrt(N) Poisson counting statistics in most... | - | (hb p. 11) |
| Cloud particle size distribution | #/liter/µm for each bin (22... | 1.5-50 µm | roughly 3 µm for size measurements | 22 bins, higher resolution... | (hb p. 11) |
| Liquid water content | g/m^3 | - | - | - | (hb p. 11) |


## Specifications

| parameter | value | source |
|---|---|---|
| Droplet size range | 1.5-50 µm | (hb p. 11) |
| Air speed operating range | 10-200 m/s | (hb p. 11) |
| Minimum air speed for correct sample volume | greater than 10 m/s | (hb p. 13) |
| Size measurement uncertainty | roughly 3 µm | (hb p. 12) |
| Calibration bead sizes | 8, 15, 20, 30, 40, 50 µm | (hb p. 14) |
| Forward scattering angle measured | ca. 4-12 degrees | (hb p. 13) |


## The data

Verified example: **`sgpaaffcdpF1.c1`**, file `sgpaaffcdpF1.c1.20160920.202755.nc`
(0.6 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5104, `optical_diameter`=21, `bound`=2 |
| Data variables | 8 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-20T20:27:55 to 2016-09-20T21:52:58 |
| dod version | aaffcdp-c1-1.1 |
| process version | ingest-aaffcdpme-1.1-0.el7 |


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
files = armlive_list_files("sgpaaffcdpF1.c1", "2016-09-20", "2016-09-20")
ds = armlive_open("sgpaaffcdpF1.c1", "2016-09-20", "2016-09-20", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaaffcdpF1.c1", "20140222", "20260923")
```

The handbook's own note on data quality: Good data quality is ensured by comparison with other measurements. During sections of the flight known not to contain clouds, the FCDP should also not record data. Number concentrations and sizes should be comparable to other cloud probe measurements, and deviations should be investigated. Data plots are generated using the ARM Data Quality Diagnostic Plot Browser (https://dq.arm.gov/dq-plotbrowser/).

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Ice cloud measurement invalidity | Sizing/scattering results in ice clouds will not represent true particle size since the method assumes spherical particles, which is very different for ice crystals | None stated; handbook notes FCDP will not yield useful information for ice clouds | (hb p. 7) |
| Small droplet detection limit (less than 1.5 µm) | Droplets smaller than 1.5 µm will not scatter enough light to be detected, appearing as an artificial low cutoff in the size distribution | None stated | (hb p. 11) |
| Large droplet sizing unreliability (greater than 50 µm) | Larger droplets are not reliably sized due to change in scattering behavior and are typically found in lower concentrations for which the sample volume can be too small | None stated | (hb p. 11) |
| Coincidence of multiple droplets | Two droplets counted as one, producing wrong droplet number and incorrect sizing of the combined scattered signal; leads to underestimate of number concentration | Coincidence correction algorithm applied during post-processing using the mask on the qualifier optics to reject coincident particles | (hb p. 11) |
| Shattering of hydrometeors on probe housing | Overestimate of smaller droplets due to multitude of smaller particles produced by shattering; shattered particles show lower interarrival times than non-shattered particles | Sharp leading edges minimize shattering into sample volume; can be at least partially removed during post-processing by interarrival time analysis | (hb p. 11) |
| Non-monotonic Mie scattering vs. size | Same scattering intensity can correspond to more than one droplet size (bumps in Mie scattering curve), causing ambiguous size bin assignment | Bin sizes must be chosen carefully so bumps are narrower than chosen bin sizes to ensure unambiguous correlation of scattering intensity to bin size | (hb p. 12) |
| Air speed sensitivity | Sample volume calculation, and thus number concentration accuracy, depends strongly on air speed; incorrect air speed leads to wrong sample volume estimates | FCDP designed for air speeds of 10-200 m/s to correctly sample droplets | (hb p. 11) |
| Out-of-cloud gaps in data | Gaps in the data appear during periods outside clouds, e.g., at highest and lowest altitudes above and below cloud showing no cloud droplet concentration | Expected behavior; used as a data quality check (FCDP should not record data when known not to contain clouds) | (hb p. 9) |
| Window contamination/dirt on probe optics | Not explicitly described as a data signature, but contamination could degrade measurement | Cleaning of the probe windows to remove dirt before each flight | (hb p. 15) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Regular calibration of size measurements performed with six sizes of glass beads (8, 15, 20, 30, 40, 50 µm); laser alignment and estimation of sampling area performed by the vendor (hb p. 14) |
| Calibration interval | typically weekly during a field campaign (hb p. 14) |
| Routine maintenance | Cleaning of the probe windows to remove dirt before each flight; regular calibration with glass beads (hb p. 15) |
| Maintenance interval | cleaning before each flight; calibration about once a week (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: two-dimensional stereo probe (2D-S), high-volume precipitation spectrometer (HVPS), Cloud Particle Imager (CPI), Cloud Droplet Probe (CDP).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `2D-S` | two-dimensional stereo probe |
| `ACE-ENA` | Aerosol and Cloud Experiments in the Eastern North Atlantic |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `CPI` | Cloud Particle Imager |
| `DOE` | U.S. Department of Energy |
| `FCDP` | fast cloud droplet probe |
| `HVPS` | high-volume precipitation spectrometer |
| `ICARTT` | International Consortium for Atmospheric Research on Transport and Transformation |
| `NetCDF` | Network Common Data Form |


### References the handbook cites

- Lance, S, CA Brock, D Rogers, and JA Gordon. 2010. "Water droplet calibration of the Cloud Droplet Probe (CDP) and in-flight performance in liquid, ice and mixed-phase clouds during ARCPAC." Atmospheric Measurement...
- SPEC FCDP Technical Manual (Rev.1.0 - Preliminary). 2013.
- SPEC FCDP Technical Manual (Rev.2.0). 2019.
- McFarquhar, GM, et al. 2017. "Processing of ice cloud in situ data collected by bulk water, scattering, and imaging probes: fundamentals, uncertainties, and efforts toward consistency." AMS Monographs 58: 11.1-11.33,...
- Baumgardner, D, et al. 2017. "Cloud ice properties: In situ measurement challenges." AMS Monographs 58: 9.1-9.23, https://doi.org/10.1175/AMSMONOGRAPHS-D-16-0011.1

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-238.pdf (16 pages, DOE/SC-ARM-TR-238, by S Glienke, F Mei)
- Catalog record: ARM data-source index, `instrument_class_code=fcdp-air`, read 2026-09-23
- Example file: `sgpaaffcdpF1.c1.20160920.202755.nc` from `sgpaaffcdpF1.c1`, 0.6 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
