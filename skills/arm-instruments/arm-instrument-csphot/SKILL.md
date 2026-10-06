---
name: arm-instrument-csphot
description: ARM Sunphotometer (csphot) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol optical thickness, Sky radiance, Precipitable water, Aerosol absorption, Aerosol concentration, Aerosol extinction, Aerosol optical properties, Particle number concentration), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpcsphotzenradv3C1.a1) and the variable inventory of a real file. Use when working with csphot data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Radiometric. Triggers - csphot, Sunphotometer, sgpcsphotzenradv3C1.a1, Aerosol optical thickness, Sky radiance, Precipitable water, Aerosol absorption, Aerosol concentration, Aerosol extinction, Aerosols, Radiometric, CIMEL Electronique (France).
---

# CSPHOT - Sunphotometer

The Cimel sunphotometer (CSPHOT) is a multi-channel, automatic sun-and-sky scanning radiometer that measures direct solar irradiance and sky radiance at the Earth's surface at pre-determined discrete wavelengths, deployed outdoors at ARM sites to derive aerosol and water vapor properties.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `csphot` |
| Handbook | [DOE/SC-ARM/TR-056 / L Gregory / January 2011](https://www.arm.gov/publications/tech_reports/handbooks/csphot_handbook.pdf) |
| Measurement category | Aerosols; Radiometric |
| Manufacturer / model | CIMEL Electronique (France); Cimel CE318 (per user manual filename man_ce318_us.pdf) |
| Primary measurements | Aerosol optical depth; Aerosol optical properties; Particle number concentration; Particle size distribution; Precipitable water; Shortwave narrowband radiance |
| Record | 1994-04-06 to 2026-09-23 (active) |
| Datastreams with data | 440 across 28 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc |
| ARM page | https://www.arm.gov/capabilities/instruments/csphot |


## Credit

Everything this skill knows about the instrument is the work of **L Gregory** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Gregory. *Cimel Sunphotometer (CSPHOT) Handbook*, DOE/SC-ARM/TR-056, January 2011.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/csphot_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Direct Normal Solar Irradiance E (W/m^2) at the surface at a given wavelength is given by Bouguer's law: E=(E_0/R^2)exp(-m*tau), where E_0 is the extra-terrestrial solar irradiance at 1 AU, R is the sun-earth distance in AU, m is the airmass, and tau is the total vertical optical thickness. If instrument voltage V corresponds to irradiance E, this becomes V=(V_0/R^2)exp(-m*tau), where V_0 is the calibration coefficient obtained by measuring voltage as a function of airmass and extrapolating to zero airmass. The total optical thickness is composed of molecular (Rayleigh) scattering, trace gas absorption (e.g., ozone), and aerosol extinction; by estimating molecular contributions, aerosol optical thickness can be derived. For the 940-nm water vapor channel, Bouguer's law is not strictly valid due to band (not monochromatic) attenuation, so transmission is modeled as T=exp(-a*w^b), a two-parameter expression, allowing derivation of precipitable water once calibration constants are known. Sky radiance is measured via almucantar and principal plane scans, and the sky brightness data are inverted by radiative transfer routines to derive aerosol size distribution and phase function.

**Siting.** The instrument is located at a height of about five feet from the surface to minimize accidental obstruction of the field of view of the collimators. The location should allow an unobstructed view of the sky above five degrees of elevation, especially in the general region of sunset and sunrise at the ARM sites. Instrument must be mounted on a level surface via the base plate mounting holes.

**Sampling.** native rate A measurement sequence takes about 10 seconds; three sequences (a triplet) lasting about 35 seconds are performed; reported every Direct solar irradiance: every 0.5 airmasses above airmass of 2, and every 15 minutes otherwise. Almucantar: twice daily (also stated as 4 times daily in spec table) at solar zenith angle ~60 degrees. Principal plane: 4 times daily. Cloud mode zenith radiance: frequent intervals between other observing schedules, every 10 min when not in other modes.; averaging Triplet of three measurement sequences performed to discriminate against non-uniform thin cirrus clouds; measured voltages compared to eliminate non-uniform scenes (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol optical thickness (AOT/AOD) | unitless (optical depth) | - | approximately 0.01-0.02 for field operated... | - | (hb p. 9) |
| Sky radiance | W/m2/sr/um | - | +/- 5% | - | (hb p. 9) |
| Precipitable water (PW) | cm | - | - | - | (hb p. 10) |
| Aerosol absorption | - | - | - | - | (hb p. 9) |
| Aerosol concentration | - | - | - | - | (hb p. 9) |
| Aerosol extinction | - | - | - | - | (hb p. 9) |
| Aerosol optical properties | - | - | - | - | (hb p. 9) |
| Particle number concentration | - | - | - | - | (hb p. 9) |
| Particle size distribution | - | - | - | - | (hb p. 9) |
| Shortwave narrowband radiance | - | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Detector | Silicon | (hb p. 13) |
| Number of Filters | 5 to 8 | (hb p. 13) |
| Number of collimators | 2 | (hb p. 13) |
| Field of View/Aperture | 1.2°; One has 10 times the aperture of the other. | (hb p. 13) |
| Solar Scanning | 4-quadrant detector | (hb p. 13) |
| Sky scanning | Azimuth and Zenith motors | (hb p. 13) |
| Frequency of Sun acquisition | 0.5 airmass intervals for airmass greater than  2. Otherwise, 15 minutes apart. | (hb p. 13) |
| Frequency of Almucantar | At airmass of 4 and 2; 4 times daily | (hb p. 13) |
| Frequency of Principal Plane Obs | 4 per day | (hb p. 13) |
| Frequency of Zenith Radiance Obs | Every 10 min, when not in any of the other observing modes. | (hb p. 13) |
| AOT measurement wavelengths | 340, 380, 440, 500, 675, 870, 1020, and 1640 nm | (hb p. 18) |
| Filter bandwidth | narrow bandwidth of about 10 nm | (hb p. 18) |
| Collimator field of view | 1.2 degree | (hb p. 15) |


## The data

Verified example: **`sgpcsphotzenradv3C1.a1`**, file `sgpcsphotzenradv3C1.a1.20260919.224833.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=119, `bound`=2, `nominal_wavelength`=7 |
| Data variables | 11 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 20 s |
| File time span | 2026-09-19T22:48:33 to 2026-09-19T23:53:12 |
| dod version | csphotzenradv3-a1-1.0 |
| process version | ingest-csphotzenradv3-1.1-2.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `exact_wavelength` | um | time,nominal_wavelength | - | Exact radiation wavelength |
| `instrument_number` | 1 | time | - | AERONET instrument number |
| `nominal_wavelength` | nm | nominal_wavelength | - | Nominal radiation wavelength |
| `time` | - | time | - | Time offset from midnight |
| `zenith` | degree | time | - | Solar zenith angle |
| `zenith_sky_radiance_A` | uW/(cm^2 sr nm) | time,nominal_wavelength | - | Sky radiance at zenith (Aureole gain) |
| `zenith_sky_radiance_K` | uW/(cm^2 sr nm) | time,nominal_wavelength | - | Sky radiance at zenith (sKy gain) |


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
                     params={"user": f"{user}:{token}", "ds": "sgpcsphotzenradv3C1.a1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpcsphotzenradv3C1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpcsphotzenradv3C1.a1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpcsphotzenradv3C1.a1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

A 2-D field over time, so pcolormesh rather than a line.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4.5))
disp.plot("zenith_sky_radiance_A")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpcsphotzenradv3C1.a1", "19940406", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data transmitted to AERONET hourly via internet; plotted and basic Q/C checks performed including cloud screening. ARM mentors at XDC check data daily and weekly for availability and to report problems. Annually, data reviewed post-deployment by AERONET to produce level 2 (cloud-screened and quality assured) data. QC frequency: daily and weekly checks for level 1.0 and level 1.5 (cloud-screened) data. QC delay: plots/error messages available at AERONET with 1-hour delay; Level 2 analysis delayed 1-2 years. QC type: comparisons with normal standards; cloud screening for level 1.5 data;...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Cloud contamination of aerosol optical thickness data | Presence of clouds distorts AOT data; visible as inconsistent triplet measurements or Angstrom exponent less than 0.5 | Clouds removed by inspection of triplet measurement in level 1.5 (csphotaotfilt) data and by eliminating all data showing an Angstrom exponent of... | (hb p. 9) |
| Thin, non-uniform cirrus cloud contamination during a measurement sequence | Measured voltages across the three sequences in a triplet disagree, indicating non-uniform scene | Three measurement sequences (triplet) are performed and compared; non-uniform scenes are eliminated during data analysis | (hb p. 12) |
| No measurement during nighttime or sun-below-horizon conditions | Data gaps outside daylight hours | - | (hb p. 6) |
| Filter optical degradation / calibration drift | Decrease in calibration coefficient stability over time, on average 1 to 10% per year, limiting factor being optical interference filters | Instruments calibrated on a 6- to 12-month rotation and filters changed when needed | (hb p. 10) |
| Precipitation shutdown | Data gaps during rain events; sensor head parked in fail-safe 'down' position pointing toward base | Wet sensor connected to instrument control box shuts down scanning during precipitation | (hb p. 12) |
| Wet sensor does not detect snow | Cloud mode data collected during snow season may be contaminated by snow in collimator tube, risking calibration accuracy | Instrument (particularly cloud mode) should not be operated during the snow season; AERONET suggests cloud mode be turned off during snow conditions | (hb p. 12) |
| Large calibration coefficient changes between pre- and post-deployment calibrations | Large uncertainties in derived measurements; data flagged and not processed to quality-assured level 2 | If the AERONET analyst deems the change too large, the data will not be processed to the quality assured level 2 | (hb p. 15) |
| 940-nm channel band attenuation saturation | Standard Bouguer's law exponential attenuation does not hold; preferential attenuation at line centers causes quick saturation | Transmission modeled with two-parameter expression T=exp(-a*w^b) using narrow 940-nm bandwidth to remove atmosphere sensitivity | (hb p. 13) |
| Airmass practical upper limit for Langley calibration | Calibration measurements above airmass of six or seven are unreliable due to inability to account for refractive index effects in the atmosphere | Practical upper limit for airmass of six or seven used in Langley calibration | (hb p. 14) |
| Cloud Mode Zenith Radiance data still developmental / provisional | Provisional cloud optical depth data only available at AERONET's website, not in standard ARM archive | Algorithm still in developmental stage; view via AERONET cloud mode web page | (hb p. 7) |
| Delay in Level 2 (quality-assured) data availability | Level 2 cloud-screened and quality-assured data delayed from 1-2 years from original date of data collection | Level 2 data processed during post-calibration; available within a few months of end of deployment | (hb p. 9) |
| Instrument obstruction of field of view | Blocked or reduced solar/sky signal near horizon if siting requirements not met | Location should allow unobstructed view of sky above five degrees of elevation, especially near sunset/sunrise; mount at height of about five feet | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Langley method for non-water absorbing channels (logarithm of DN vs airmass between 5 and 2, intercept = calibration coefficient, slope = optical depth); modified-Langley method for the 940-nm water vapor channel using a two-parameter transmission model (a, b constants from radiative transfer modeling e.g. MODTRAN-3).... (hb p. 10) |
| Calibration interval | Field instruments generally returned to GSFC for intercomparison approximately every 6 to 12 months; instruments swapped out and sent to AERONET on an annual basis; NSA CSPHOT calibrated during winter months November through March; AERONET reference instruments recalibrated at Mauna Loa Observatory every 2-3 months (hb p. 10) |
| Traceability | GSFC reference Cimels calibrated by the Langley technique at Mauna Loa Observatory, Hawaii; zero air mass voltages inferred to accuracy of approximately 0.2 to 0.5% for MLO calibrated reference instruments (Holben et al., 1998); calibration coefficients linearly interpolated between pre- and post-deployment... (hb p. 10) |
| Routine maintenance | Weekly checks including battery connections, wet sensor, instrument clocks, level of robot and parked sensor head, and clear collimator tubes. When cloud mode is in operation, wet sensor must be checked weekly to ensure it works properly and rain does not get into collimator tubes. (hb p. 15) |
| Maintenance interval | Weekly (hb p. 15) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: MFRSR, TSI, radiosonde, microwave radiometer.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AOT` | Aerosol Optical Thickness |
| `AOD` | Aerosol Optical Depth |
| `PW` | Precipitable Water |
| `DN` | Digital Number (instrument output) |
| `AERONET` | Aerosol Robotic Network |
| `XDC` | ARM External Data Center |
| `VAP` | Value-Added Product |
| `QME` | Quality Measurement Experiment |
| `MLO` | Mauna Loa Observatory |
| `DQR` | Data Quality Report |
| `DQPR` | Data Quality Problem Report (implied) |
| `Almucantar` | Sky scan at constant solar zenith angle but varying azimuth angles to obtain angular... |
| `Principal Plane` | Sky scan in a plane containing the sun and instrument, normal to the surface |


### References the handbook cites

- Halthore, RN, TF Eck, BN Holben, and BL Markham. 1997. "Sunphotometric measurements of atmospheric water vapor column abundance in the 940-nm band." Journal of Geophysical Research 102: 4343-4352.
- Holben, BN, TF Eck, I Slutsker, D Tanre, JP Buis, A Setzer, E Vermote, J Reagan, Y Kaufman, T Nakajima, F Lavenu, and I Jankowiak. 1997. "Automatic sun and sky scanning radiometer system for network aerosol monitoring."...
- Nakajima, T, M Tanaka, and T Yamauchi. 1983. "Retrieval of the optical properties of aerosols from aureole and extinction data." Applied Optics 22: 2951-2959.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/csphot_handbook.pdf (22 pages, DOE/SC-ARM/TR-056, by L Gregory)
- Catalog record: ARM data-source index, `instrument_class_code=csphot`, read 2026-09-23
- Example file: `sgpcsphotzenradv3C1.a1.20260919.224833.nc` from `sgpcsphotzenradv3C1.a1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
