---
name: arm-instrument-inletisok-air
description: ARM Isokinetic Inlet aboard aircraft (inletisok-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Cabin Temperature, Inlet Temperature, Inlet Pressure, Inlet Relative Humidity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpaafinletisokF1.a1) and the variable inventory of a real file. Use when working with inletisok-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Airborne Observations. Triggers - inletisok-air, Isokinetic Inlet aboard aircraft, sgpaafinletisokF1.a1, Cabin Temperature, Inlet Temperature, Inlet Pressure, Inlet Relative Humidity, Airborne Observations, Brechtel (Hayward, California) Isokinetic Inlet System, CACTI, ISOK, PNNL, SBIR.
---

# INLETISOK-AIR - Isokinetic Inlet aboard aircraft

The isokinetic inlet samples external free-stream air aboard the ARM Aerial Facility aircraft at matched velocity to avoid distorting the aerosol size distribution, delivering sample flow to cabin instrumentation while reporting cabin/inlet temperature, pressure, and relative humidity housekeeping data.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 14 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `inletisok-air` |
| Handbook | [DOE/SC-ARM-TR-251 / L Goldberger / July 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-251.pdf) |
| Measurement category | Airborne Observations |
| Manufacturer / model | Brechtel (Hayward, California) Isokinetic Inlet System, modified by Pacific Northwest National Laboratory (PNNL) |
| Primary measurements |  |
| Record | 2013-06-24 to 2026-09-23 (retired) |
| Datastreams with data | 7 across 7 sites |
| Sites | acx, cor, ena, mao, nsa, osc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/inletisok-air |


## Credit

Everything this skill knows about the instrument is the work of **L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Goldberger. *Isokinetic Inlet Aboard Aircraft (INLETISOK-AIR) Instrument Handbook*, DOE/SC-ARM-TR-251, July 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-251.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

An isokinetic inlet samples particles from the free stream at the same velocity as the free stream entering the tip so streamlines and particle trajectories remain straight and undistorted; super- or sub-isokinetic sampling skews concentrations due to inertial effects around the tip. Sampling efficiency is determined by the inlet's aspiration, entrance, and transmission properties: aspiration efficiency is the ratio of particle concentrations inside the inlet versus the free stream and depends on matching nozzle velocity to free-stream velocity; entrance bluntness can generate flow separation and turbulence causing disproportionate loss of larger, higher-inertia particles; transmission efficiency describes particle loss within the inlet from sedimentation, turbulent deposition, inertial deposition from bends, and diffusion. Within the inlet, sample air is slowed in two stages via an aerodynamic twin-diffuser (a duct that increases area in the flow direction, allowing the compressible air/aerosol to increase in temperature, pressure, and density while decreasing velocity) to a velocity suitable for cabin instrumentation, aided by passive pumping to remove diffuser turbulent boundary layer and a low-power blower actively controlling sample flow. A large flow is passed through the subsampling tube with most exhausted downstream and only a small fraction sampled, minimizing transmission loss and residence time.

**Siting.** Inlet nozzle must be a suitable distance from the aircraft fuselage skin to sample true free-stream air and avoid surface drag/turbulent eddy contamination, yet close enough to the fuselage that the air stream is unaffected by propeller prop wash; on the G-1 this distance was 8 inches from the fuselage. The inlet's angle of attack must be aligned with the directional flow of air so streamlines are unimpeded entering the nozzle. After the nozzle and two diffusers, the probe has a shallow (less than 90°) bend to be inserted through a window plate on the right (starboard) side of the aircraft. Inlets undergo extensive testing after installation to ensure proper sampling.

**Sampling.** native rate 1 Hz; reported every 1-Hz resolution on the G-1 with the M300 data acquisition system (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Cabin Temperature | - | - | - | - | (hb p. 7) |
| Inlet Temperature | - | - | - | - | (hb p. 7) |
| Inlet Pressure | - | - | - | - | (hb p. 7) |
| Inlet Relative Humidity | - | - | - | - | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Particle aerodynamic diameter size range | 0.005-10 micron | (hb p. 9) |
| Sample flow at diffuser tip (at 100 m/s*) | 300 Liters per minute | (hb p. 9) |
| Sample flow to cabin | 150 Liters per minute | (hb p. 9) |
| Maximum sample flow to instruments | 100 Liters per minute | (hb p. 9) |
| Control and data acquisition frequency | 1 Hz | (hb p. 9) |
| Anti-icing power | 900 Watts @ 28 VDC | (hb p. 9) |
| Rack-mountable electronics chassis size | 19 x 6.5 x 12 (48.25 x 16.5 x 30.5) Inches (centimeters) | (hb p. 9) |
| Electronics chassis weight | 20 (9) Lb (kg) | (hb p. 9) |
| Total system weight | 70 (31.75) Lb (kg) | (hb p. 9) |
| Operating temperature range | -40 to 45 C | (hb p. 9) |
| Operating pressure range (absolute) | 200- 1000 mb | (hb p. 9) |


## The data

Verified example: **`sgpaafinletisokF1.a1`**, file `sgpaafinletisokF1.a1.20160921.162746.nc`
(0.31 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=9710 |
| Data variables | 9 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2016-09-21T16:27:46 to 2016-09-21T19:09:35 |
| dod version | aafinletisok-a1-1.0 |
| process version | ingest-aafinletisok-1.2-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cabin_temperature` | degC | time | - | Cabin temperature |
| `pressure_isok_inlet` | hPa | time | - | Pressure at isokinetic inlet manifold |
| `relative_humidity_isok_inlet` | % | time | - | Relative humidity at isokinetic inlet manifold |
| `temperature_isok_inlet` | degC | time | - | Temperature at isokinetic inlet manifold |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgpaafinletisokF1.a1", "2016-09-21", "2016-09-21")
ds = armlive_open("sgpaafinletisokF1.a1", "2016-09-21", "2016-09-21", cleanup_qc=True)
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpaafinletisokF1.a1", "20130624", "20260923")
```

The handbook's own note on data quality: Data quality evaluation involves automatic flagging based on criteria developed by instrument mentors. Automatic data quality checks performed by the ARM Data Quality Office (DQO) ensure temperature, pressure, and relative humidity are within normal levels. The instrument mentor performs a more vigorous data quality check before data publication to ensure particle transmission is not biased from cases such as transmission loss and dryer performance. No plots are available for these data on Data Discovery; however, these data can be used for data masking (e.g., using the CVI flag to identify...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Super-isokinetic sampling bias | Oversampling of smaller particles relative to larger particles in the reported size distribution because nearby streamlines curve inward toward the inlet when sample velocity exceeds... | Maintain isokinetic (matched velocity) sampling conditions via inlet flow control software | (hb p. 6) |
| Sub-isokinetic sampling bias | Undersampling of smaller particles (which follow streamlines away from the nozzle) while larger particles are oversampled relative to true concentration, occurring when sample velocity is... | Maintain isokinetic (matched velocity) sampling conditions via inlet flow control software | (hb p. 6) |
| Inlet installation/siting contamination effects | Anomalous or biased particle concentration readings if inlet is too close to fuselage (surface drag, turbulent eddies) or misaligned angle of attack disrupting streamlines | Install inlet at sufficient distance from aircraft skin (8 inches on G-1) and at the appropriate angle aligned with airflow; extensive... | (hb p. 6) |
| Entrance bluntness / flow separation and turbulence | Disproportionate loss of larger particles (higher inertia) in the sampled size distribution due to flow separation and turbulence generated at the probe tip | - | (hb p. 11) |
| Transmission losses within inlet | Particle loss from sedimentation, turbulent deposition, inertial deposition from bends, and diffusion, seen as reduced concentration or altered size distribution shape compared to... | Large flow through subsampling tube with most exhausted downstream and only small fraction sampled, minimizing residence time and transmission loss | (hb p. 11) |
| Particle size cutoff / limited transmission efficiency | Transmission efficiency drops below 90% for particle aerodynamic diameters greater than 10 microns; earlier prototype inlet had a 50% cutoff near 1.5 micron | - | (hb p. 7) |
| Dryer performance degradation | Variability in inlet relative humidity / dryer performance visible in housekeeping data during a campaign (e.g., as shown for CACTI campaign) | Instrument mentor performs vigorous data quality check before publication to ensure particle transmission is not biased by dryer performance | (hb p. 9) |
| Non-scientific housekeeping data | Cabin/inlet temperature, pressure, RH, and OPC-AIR coarse-mode size distribution data are not meant for direct scientific analysis but for assessing sample integrity/transmission | Use for data masking / QC assessment rather than direct scientific analysis; cross-reference with INLETCVI-AIR flag | (hb p. 7) |
| Manual inlet switching between ISOK and CVI | Sampling inlet flag (ISOK vs CVI) in INLETCVI-AIR dataset changes based on manual crew action, so data may reflect either inlet depending on switch state, requiring the CVI flag to... | Check the sampling inlet flag in the INLETCVI-AIR data set to determine which inlet was active | (hb p. 7) |
| Instrument currently not in use | No new data being produced while the Challenger 850 aircraft is being modified for research | - | (hb p. 9) |
| Heavy aerosol loading contamination (e.g., smoke) | Increased particle deposition/fouling in inlet after flights through heavy aerosol loadings such as smoke, potentially degrading transmission over time if not cleaned | Accelerated cleaning schedule recommended for heavy aerosol loading environments | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration procedures and records are maintained between Brechtel and the instrument mentor. (hb p. 12) |
| Routine maintenance | The inlet should be cleaned before every campaign; an accelerated cleaning schedule is recommended for environments with particularly heavy aerosol loadings, such as flying through smoke. (hb p. 12) |
| Maintenance interval | Before every campaign (accelerated in heavy aerosol loading environments) (hb p. 12) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: CVI inlet (counterflow virtual impactor, separate handbook), OPC-AIR, INLETCVI-AIR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AAF` | ARM Aerial Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `CAD` | computer-aided design |
| `CVI` | counterflow virtual impactor |
| `DOE` | U.S. Department of Energy |
| `DQO` | Data Quality Office |
| `G-1` | Gulfstream-159 |
| `GUI` | graphical user interface |
| `IOP` | intensive operational period |
| `ISOK` | isokinetic |
| `PC` | personal computer |
| `PNNL` | Pacific Northwest National Laboratory |
| `SBIR` | Small Business Innovation Research |


### References the handbook cites

- Hermann, M, F Stratmann, M Wilck, and A Wiedensohler. 2000. 'Sampling characteristics of an aircraft-borne aerosol inlet system.' Journal of Atmospheric and Oceanic Technology 18(1): 7–19
- Huebert, BJ, G Lee, and WL Warren. 1990. 'Airborne aerosol inlet passing efficiency measurement.' Journal of Geophysical Research − Atmospheres 95(D10): 16369–16381
- Baron, PA, and K Willeke. 2005. Aerosol Measurement: Principles, Techniques, and Applications. 2nd ed. John Wiley & Sons Inc.
- Zaveri, R, et al. 2009. 'Nighttime chemical evolution of aerosol and trace gases in a power plant plume.' Journal of Geophysical Research − Atmospheres 115(D12): D12304
- Brechtel, FJ. 2003. Description and Assessment of a New Aerosol Inlet for the DOE G-1 Research Aircraft. Final Technical Report, BMI contract #0000058843 to Brookhaven National Laboratory

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-251.pdf (14 pages, DOE/SC-ARM-TR-251, by L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=inletisok-air`, read 2026-09-23
- Example file: `sgpaafinletisokF1.a1.20160921.162746.nc` from `sgpaafinletisokF1.a1`, 0.31 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
