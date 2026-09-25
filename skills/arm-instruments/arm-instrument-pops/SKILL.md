---
name: arm-instrument-pops
description: ARM portable or printed optical particle spectrometer (pops) - handbook-derived instrument reference. Measurement principle, reported quantities (Aerosol size distribution, Total particle concentration, Temperature, Relative humidity, Sample flow rate), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (dstpops1mM1.b1) and the variable inventory of a real file. Use when working with pops data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols. Triggers - pops, portable or printed optical particle spectrometer, dstpops1mM1.b1, Aerosol size distribution, Total particle concentration, Temperature, Relative humidity, Sample flow rate, Aerosols, NOAA-developed POPS, licensed/distributed by Handix Scientific (model 1120), CoURAGE, HEPA, NetCDF, NOAA.
---

# POPS - portable or printed optical particle spectrometer

The POPS is a laser-based optical particle spectrometer that measures aerosol size distribution (150 nm - 5 um, 16 bins) and total number concentration, deployed as a network of up to four weatherproof, tripod-mounted units with co-located temperature and RH sensors.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 18 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `pops` |
| Handbook | [DOE/SC-ARM-TR-328 / SS Petters, MD Petters / January 2026](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-328.pdf) |
| Measurement category | Aerosols |
| Manufacturer / model | NOAA-developed POPS, licensed/distributed by Handix Scientific (model 1120); modified by University of California, Riverside (UCR) |
| Primary measurements | Aerosol concentration; Aerosol particle size; Aerosol particle size distribution |
| Record | 2019-09-15 to 2026-09-23 (active) |
| Datastreams with data | 11 across 3 sites |
| Sites | crg, dst, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/pops |


## Credit

Everything this skill knows about the instrument is the work of **SS Petters, MD Petters** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> SS Petters, MD Petters. *Network of Modified Portable Optical Particle Spectrometers Instrument Handbook*, DOE/SC-ARM-TR-328, January 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-328.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The POPS records the passage of particles through a continuous-flow detector and assigns a size to each particle, building a size distribution with high time resolution; particle size and number concentration are both assessed optically, with no high-voltage power supply and no diameter scanning. Particle-laden air passes through a blue-violet 405-nm, 100-mW diode laser beam; when a particle passes through the beam, the flash of scattered light is reflected by a cupped mirror below (capturing light over 38 to 142 degrees) into a photomultiplier tube above. The PMT converts incident photons into electrons via the photoelectric effect and the observed current is proportional to the brightness of scattered light. The amplitude of collected light is not a linear function of particle size, depending on refractive index, diameter relative to the 405-nm wavelength, and collection angle/breadth; calibration matches instrument response to size-selected particles of known refractive index against Mie theory predictions to map instrument output to diameter bin boundaries.

**Siting.** Each unit sits in a weatherproof enclosure mounted on a tripod; the 1/16-inch steel inlet protrudes about 2 cm from the base of the enclosure, unencumbered by netting or rain covers, hovering about 1 m above the grass; up to four matching POPS deployed across a network (e.g., urban, rural, coastal sites). Sample stream is not dried before measurement.

**Sampling.** native rate high time resolution (optical, particle-by-particle); reported every one-minute averages; averaging one-minute averages of aerosol size and number spectrum, temperature, RH, total concentration, flow rate (hb p. 6).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol size distribution (particles per bin) | cm-3 (normalized by bin... | 150 nm to 5 um, 16 logarithmically... | +/-(3-5)% | 16 bins (PSL calibration)... | (hb p. 6) |
| Total particle concentration | cm-3 | 0 to 4000 cm-3 (upper limit of... | - | - | (hb p. 9) |
| Temperature | degC | - | accurate to 0.1 degC | - | (hb p. 4) |
| Relative humidity | %RH | - | 1% near saturation, 0.5% near 40% RH | - | (hb p. 4) |
| Sample flow rate | L/min | nominal 0.18 L/min (3 cm3/s) | less than  5% margin of error irrespective of... | - | (hb p. 5) |


## Specifications

| parameter | value | source |
|---|---|---|
| Size distribution range | 150 nm to 5 um, 16 logarithmically spaced bins | (hb p. 6) |
| Accuracy of size distributions | +/-(3-5)% | (hb p. 3) |
| Temperature sensor accuracy | 0.1 degC | (hb p. 4) |
| RH sensor accuracy | 1% near saturation and 0.5% near 40% RH | (hb p. 4) |
| Upper limit of linearity | ~2000 cm-3 | (hb p. 4) |
| Upper limit of quantification | 4000 cm-3 | (hb p. 4) |
| Saturation range | between 4000 and 5000 cm-3 | (hb p. 4) |
| D50 (ammonium sulfate, Mei et al. 2020) | 135 nm | (hb p. 4) |
| D50 (PSL, Handix 2020 assessment) | 129 +/- 6 nm | (hb p. 5) |
| Power consumption | ~15-20 W: 5 (POPS) + 6.5-10.5 (Computer) + 0.25 LabJack + 3.5 (power supply original specification) | (hb p. 5) |
| Enclosure size and material | 20 x 16 x 8'' enclosure of 1.5-mm steel | (hb p. 5) |
| PSL calibration bin boundaries (16 bins) | 115, 125, 135, 150, 165, 185, 210, 250, 350, 475, 575, 855, 1220, 1530, 1990, 2585, 3370 nm | (hb p. 10) |
| Ammonium sulfate calibration bin boundaries (16 bins) | 156, 172, 190, 210, 232, 269, 357, 469, 540, 690, 1068, 1534, 1910, 2538, 3288, 4331, 5415 nm | (hb p. 10) |
| Nominal flow rate | 0.18 L/min (3 cm3/s) | (hb p. 5) |
| Laser | blue-violet 405-nm, 100-mW diode laser | (hb p. 5) |
| Mirror collection angle | 38 deg to 142 deg, 90 deg relative to beam | (hb p. 6) |
| PMT peak sensitivity | near 400 nm | (hb p. 6) |
| PMT dark current | typical 1 nA (max 10 nA) | (hb p. 6) |
| PMT rise time | 0.57 ns | (hb p. 6) |
| PMT signal from particles | uA range | (hb p. 6) |
| Flow measurement error | less than  5% irrespective of absolute pressure | (hb p. 7) |


## The data

Verified example: **`dstpops1mM1.b1`**, file `dstpops1mM1.b1.20260817.000030.nc`
(0.55 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1440, `bound`=2, `diameter_optical`=16, `diameter_optical_AS`=16 |
| Data variables | 35 |
| QC variables | 4 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-08-17T00:00:30 to 2026-08-17T23:59:30 |
| sampling interval | 1 second |
| averaging interval | 1 minute |
| dod version | pops1m-b1-1.0 |
| process version | ingest-pops1m-1.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `sample_flow_rate` | cm^3/s | time | yes | Sample flow rate |
| `sample_relative_humidity` | % | time | yes | Relative humidity |
| `sample_temperature` | degC | time | yes | Sample temperature |
| `total_N_conc` | 1/cm^3 | time | yes | Total number concentration |
| `dD_to_dSA` | nm^2 | diameter_optical | - | Particle surface area (PSL) |
| `dD_to_dSA_AS` | nm^2 | diameter_optical_AS | - | Particle surface area (AS) |
| `dD_to_dV` | nm^3 | diameter_optical | - | Particle volume (PSL) |
| `dD_to_dV_AS` | nm^3 | diameter_optical_AS | - | Particle volume (AS) |
| `dN_dlogDp` | 1/cm^3 | time,diameter_optical | - | Particle size distribution (PSL) |
| `dN_dlogDp_AS` | 1/cm^3 | time,diameter_optical_AS | - | Particle size distribution (AS) |
| `diameter_optical` | nm | diameter_optical | - | Optical diameter bin midpoints (PSL) |
| `diameter_optical_AS` | nm | diameter_optical_AS | - | Optical diameter bin midpoints (AS) |
| `diameter_optical_bounds_AS` | nm | diameter_optical_AS,bound | - | Optical diameter bin boundaries (AS) |
| `dlogDp` | 1 | diameter_optical | - | Relative width of bins (PSL) |
| `dlogDp_AS` | 1 | diameter_optical_AS | - | Relative width of bins (AS) |
| `raw_bin_counts` | count/s | time,diameter_optical | - | Raw counts in each bin |
| `raw_bin_counts_std` | count/s | time,diameter_optical | - | Standard deviation of raw counts in each bin |
| `sample_flow_rate_std` | cm^3/s | time | - | Standard deviation of sample flow rate |
| `sample_relative_humidity_std` | % | time | - | Standard deviation of relative humidity |
| `sample_temperature_std` | degC | time | - | Standard deviation of sample temperature |
| `time` | - | time | - | Time offset from midnight |
| `total_SA_conc` | nm^2/cm^3 | time | - | Total surface area concentration from integrated size distribution... |
| `total_SA_conc_AS` | nm^2/cm^3 | time | - | Total surface area concentration from integrated size distribution... |
| `total_V_conc` | nm^3/cm^3 | time | - | Total volume concentration from integrated size distribution (PSL) |
| `total_V_conc_AS` | nm^3/cm^3 | time | - | Total volume concentration from integrated size distribution (AS) |
| `total_count` | count/s | time | - | Total number of raw counts |
| `total_count_std` | count/s | time | - | Standard deviation of total number of raw counts |


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
                     params={"user": f"{user}:{token}", "ds": "dstpops1mM1.b1",
                             "start": "2026-08-17", "end": "2026-08-17", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./dstpops1mM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "dstpops1mM1.b1", "2026-08-17", "2026-08-17")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("dstpops1mM1.b1", "2026-08-17", "2026-08-17"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("sample_temperature", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

4 `qc_` companion variables cover 4 of the
35 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_total_N_conc"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("total_N_conc", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["total_N_conc", "sample_temperature", "sample_relative_humidity"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("dstpops1mM1.b1", "20190915", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Data become suspect or unusable under certain circumstances (laser power drop, pump control failure, need for cleaning); these incidents and associated time periods are flagged by ARM and instrument mentors and archived as Data Quality Reports (DQRs). Data are flagged when concentration is outside 0 to 4000 cm-3 or when flow deviates beyond a set acceptable range; these flags have thus far been lagging indicators of issues that already arose.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Upper limit of linearity / undercounting at high concentration | POPS reported concentration begins to deviate from CPC reference below the 1:1 line for concentrations exceeding 2000 cm-3 | Recognize as instrument limitation; use MCA pulse height distribution comparison for correction context | (hb p. 4) |
| Saturation at high concentration | Signal saturates between 4000 and 5000 cm-3; concentration values plateau despite higher true concentration | None given beyond flagging data outside 0-4000 cm-3 range | (hb p. 9) |
| Digitizer speed limitation causing bias | Serial stream concentration diverges from MCA-derived concentration and from CPC reference at high number concentrations | None stated beyond characterization via MCA comparison | (hb p. 4) |
| RH sensor saturation/wetting bias in enclosure at high ambient RH | When outdoor RH reaches 100%, reported RH within enclosure remains ~20% lower and becomes constant with time because interior is warmer than exterior | Apply an exterior temperature about 2.25 degC lower than interior and adjust the guess until calculated RH is 100% at the point of saturation | (hb p. 4) |
| Laser power failure | Steady and widening gap develops between the failing instrument and other POPS in the network; failing instrument becomes slowly silent; signs are initially subtle | Requires replacement laser, laser realignment, and instrument recalibration | (hb p. 6) |
| Pump control failure | Erratic signal (board failing) or loud screeching noted by onsite technicians (pump failing) | Does not necessarily render data useless; flow, particle spectra, and concentration measurement should remain accurate barring catastrophic pump... | (hb p. 6) |
| Instrument needs cleaning (optics contamination) | Instrument does not report zero particles when sampling through a filter (or instrument leaks) | Airtight, below-ambient-pressure POPS chamber must be dismantled to clean optics | (hb p. 7) |
| Data flags lag real issues | Flags applied when concentration outside 0-4000 cm-3 or flow deviates beyond acceptable range, but these have thus far been lagging indicators of issues already present | Archived as Data Quality Reports (DQRs) by ARM and mentors | (hb p. 6) |
| T/RH sensor stuck value | Temperature or RH holding the same value for excessively long | Could indicate a problem; if sensor becomes wet it reaches 100% RH and remains there for a protracted period before fully recovering | (hb p. 7) |
| Counting uncertainty from lower size cutoff and flow rate | Uncertainty in total number concentration reported | Flow margin of error determined to be less than 5% irrespective of absolute pressure (Gao et al. 2016) | (hb p. 7) |
| Size uncertainty from refractive index variability | Calibration curve can shift upwards or downwards; ambient particle population may be internally or externally mixed adding uncertainty | Two calibrations provided (PSL and ammonium sulfate) to bound uncertainty | (hb p. 7) |
| Mie scattering resonance ambiguity above ~600 nm | Scattered light is not a monotonic function of particle size above about 600 nm (405-nm laser), causing regions of ambiguity in the unsmoothed model response | Calibration curve uses a smoothing algorithm to assign diameter | (hb p. 7) |
| Non-linear amplitude-to-size relationship | Amplitude of collected light is not a linear function of particle size | Calibration via Mie theory matching to size-selected particles of known refractive index | (hb p. 6) |
| Sample not dried | Reported size distribution reflects ambient (hydrated) particle sizes, not dry sizes | None stated (noted as FAQ: aerosols are not dried) | (hb p. 6) |
| Smallest size bin higher uncertainty | Data in the smallest bin does not align as well with co-located SMPS instruments | None stated beyond noting the elevated uncertainty in lower cutoff of detection | (hb p. 10) |
| Flow rate deviation from nominal | Flow rate reading departs from nominal 0.18 L/min | Does not necessarily indicate corrupt data since flow measurement and control are separate circuits; but should be carefully investigated for... | (hb p. 5) |
| Backup pump / critical orifice flow oscillation | Switching to backup pump results in an oscillating flow rate that does not precisely match PID-controlled flow rate of default pump/circuit; choked flow through critical orifice varies with... | None beyond noting the backup exists as contingency | (hb p. 5) |
| Enclosure heating from closed box / external vacuum pump | Interior temperature elevated relative to outside temperature due to power dissipation, radiative heating by sun, or added external vacuum pump heat | External vacuum pump housed in a separate enclosure at base of tripod to mitigate excess heating; box has two fans to keep interior temperature... | (hb p. 3) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field calibration with PSL using a portable atomizer, matching instrument response to size-selected particles of known refractive index to Mie theory predictions; also calibrated with size-selected dry ammonium sulfate aerosol following Kasparoglu et al. (2022) (hb p. 10) |
| Calibration interval | At time of service (every few months) the instruments should be recalibrated (hb p. 10) |
| Traceability | Vendor calibration (Mie scattering theory) and Mei et al. 2020; PSL and ammonium sulfate size-selected aerosol standards (hb p. 10) |
| Routine maintenance | Service and sometimes repair; recalibration and optics cleaning at time of service (hb p. 9) |
| Maintenance interval | every few months (hb p. 9) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: CPC (condensation particle counter), SMPS (scanning mobility particle sizer), UHSAS (ultra-high-sensitivity aerosol spectrometer), SP2 (single-particle soot photometer), OPC (optical particle spectrometer, Grimm 11-D), POPS-AIR (Portable Optical Particle Spectrometer aboard an Airborne....

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ARM` | Atmospheric Radiation Measurement |
| `CoURAGE` | Coast-Urban-Rural Atmospheric Gradient Experiment |
| `CPC` | condensation particle counter |
| `DQR` | Data Quality Report |
| `HEPA` | high-efficiency particulate air |
| `MCA` | multi-channel analyzer |
| `NetCDF` | Network Common Data Form |
| `NOAA` | National Oceanic and Atmospheric Administration |
| `OPC` | optical particle spectrometer [sic] |
| `PH` | pulse height |
| `PID` | proportional-integral-derivative |
| `PMT` | photomultiplier tube |
| `POPS` | portable optical particle spectrometer |
| `PSL` | polystyrene latex spheres |


### References the handbook cites

- Gao et al. 2013, 2016
- Watts 2017
- Telg et al. 2017
- Asher et al. 2021/2022
- Mei and Pekour 2026
- Mei et al. 2020
- Kasparoglu et al. 2022
- Kasparoglu et al. 2024
- Cai et al. 2008
- Suda and Petters 2013

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-328.pdf (18 pages, DOE/SC-ARM-TR-328, by SS Petters, MD Petters)
- Catalog record: ARM data-source index, `instrument_class_code=pops`, read 2026-09-23
- Example file: `dstpops1mM1.b1.20260817.000030.nc` from `dstpops1mM1.b1`, 0.55 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
