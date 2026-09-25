---
name: arm-instrument-cas-air
description: ARM Cloud and Aerosol Spectrometer aboard aircraft (cas-air) - handbook-derived instrument reference. Measurement principle, reported quantities (Number Concentration, Area Concentration, Volume Concentration, Particle optical properties, Inter-arrival time), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enaaafcasF1.b1) and the variable inventory of a real file. Use when working with cas-air data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Aerosols; Airborne Observations; Cloud Properties. Triggers - cas-air, Cloud and Aerosol Spectrometer aboard aircraft, enaaafcasF1.b1, Number Concentration, Area Concentration, Volume Concentration, Particle optical properties, Aerosols, Airborne Observations, Cloud Properties, Droplet Measurement Technologies (DMT) Cloud, Aerosol.
---

# CAS-AIR - Cloud and Aerosol Spectrometer aboard aircraft

The CAS (part of the CAPS instrument suite) measures aerosol particle and cloud droplet size distributions from 0.51 to 50 µm and optical/depolarization properties using forward- and back-scattered laser light, mounted in a wing pylon on the ARM Aerial Facility research aircraft.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 20 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `cas-air` |
| Handbook | [DOE/SC-ARM-TR-246 / L Goldberger / June 2020](https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf) |
| Measurement category | Aerosols; Airborne Observations; Cloud Properties |
| Manufacturer / model | Droplet Measurement Technologies (DMT) Cloud, Aerosol, and Precipitation Spectrometer (CAPS), comprising CAS, CIP, and HW sensors |
| Primary measurements | Cloud particle size distribution |
| Record | 2017-03-08 to 2026-09-23 (retired) |
| Datastreams with data | 4 across 2 sites |
| Sites | cor, ena |
| ARM page | https://www.arm.gov/capabilities/instruments/cas-air |


## Credit

Everything this skill knows about the instrument is the work of **L Goldberger** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> L Goldberger. *Cloud, Aerosol, and Precipitation Spectrometer Instrument Handbook*, DOE/SC-ARM-TR-246, June 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `cip-air` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `cas-air`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The CAS relies on light-scattering rather than imaging techniques to measure smaller particles: particles scatter light from an incident laser, and collecting optics guide light scattered in the 4 to 12 degree range into a forward-sizing photodetector, which is measured and used to infer particle size. Backscatter optics also measure light in the 168 to 176 degree range. The CAS polarization feature (S-state and P-state polarizations measured by two backscatter detectors) allows it to differentiate between water and ice particles in the 0.5-50 µm range; for spherical droplets the polarization of incident light is retained and the crossed polarization in the backscatter generates no signal, while aspherical particles increase signal in the crossed-polarizer backscatter detector. The CAS probe assigns each sizer signal to a bin via high and low gain stages, with a roll-over value of 14336, gain added value of 16384 (2^14), and gain multiplier of 128; the resulting size value is placed in a bin according to a threshold table corresponding to the index of refraction used (processed with refractive index 1.33 for liquid water). Particle inter-arrival time and S&P qualifier data are used to determine if a particle is in focus (if 0.5*Sizer less than  Qualifier, the particle is rejected) and to limit coincidence errors and mask ice-shattering artifacts.

**Siting.** The CAPS instrument is installed in a wing pylon with power controlled from a switch inside the aircraft; once power is applied, the probe is controlled via the vendor-provided GUI. If temperatures reach 0 deg C, anti-ice heaters must be turned on manually. When grounded (before flight, calibration days) a bright orange traffic cone must be placed in front of the probe to prevent contact with the probe tips, and safety caps must be on the CIP's ice-shattering-prevention tips when not in use.

**Sampling.** native rate 0.1 to 10 Hz (CAS and CIP possible sampling frequency); reported every 1 Hz (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Aerosol particle and cloud hydrometeor size distribution... | µm; #/cc | 0.51 to 50 µm | +/- 15% in concentration | - | (hb p. 5) |
| Number Concentration | #/CC | up to 10,000 cm3 max concentration | - | - | (hb p. 9) |
| Area Concentration | um^2/cm^3 | - | - | - | (hb p. 9) |
| Volume Concentration | um^3/cm^3 | - | - | - | (hb p. 9) |
| Particle optical properties (refractive index) | - | 1.3-1.7 (non-absorbing samples) | - | - | (hb p. 5) |
| Particle shape/phase discrimination (depolarization, water... | unitless (S,P) | 0.5-50 µm particles | - | - | (hb p. 8) |
| Inter-arrival time (PBP) | - | - | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| CAS reported size distribution range | 0.51 to 50 µm | (hb p. 11) |
| CAS possible sampling frequency | 0.1 to 10 Hz | (hb p. 11) |
| CAS reported time resolution | 1 Hz | (hb p. 11) |
| CAS sample area (forward and back scattering) | 1.1 mm x 120 µm | (hb p. 11) |
| CAS valid airspeed range | 10-200 m/s | (hb p. 11) |
| CAS refractive index range (non-absorbing samples) | 1.3-1.7 | (hb p. 11) |
| CAS laser wavelength | 658 nm | (hb p. 11) |
| CAS maximum concentration sample | 10,000 cm3 | (hb p. 11) |
| CIP reported size range | 25 to 1550 µm | (hb p. 11) |
| CIP theoretical size range (measurement theory section) | 12.5 to 1550 µm | (hb p. 14) |
| CIP sampling frequency (histogram) | 0.1 to 10 Hz, reported at 1 Hz | (hb p. 11) |
| CIP sample area (diode array) | 10 cm x 1.55 mm | (hb p. 11) |
| CIP valid airspeed range | 10-300 m/s | (hb p. 11) |
| CIP laser | 658 nm, 30 mW | (hb p. 13) |
| CIP upper concentration range | up to 500 particles/cm3 for CIP with standard tips and arm width | (hb p. 12) |
| HW LWC range | 0.01 to 3 g/m3 | (hb p. 11) |
| HW valid airspeed range | 10-300 m/s | (hb p. 11) |
| HW sampling frequency | 0.1 to 10 Hz | (hb p. 11) |
| Operating temperature range | -50-50°C | (hb p. 11) |
| Operating humidity range | 0-100%, non-condensing | (hb p. 11) |
| Operating altitude | 50,000 ft | (hb p. 11) |
| CAS System data input voltage/comms | RS-232 or RS-422, 56.6 kb/sec Baud rate; Maximum packet size 8200 bits | (hb p. 12) |
| 2D CIP data comms | RS-422, High Speed, 4 Mb/sec Baud rate | (hb p. 12) |
| CIP System data comms | RS-232 or RS-422, 56.6 kb/sec Baud rate | (hb p. 13) |
| HW system comms | RS-232 or RS-422, 56.6 kb/sec Baud rate | (hb p. 13) |
| CIP probe tips | Korolev tips installed with a 70mm beam opening | (hb p. 11) |


_1 further specification rows are in the handbook._

## The data

Verified example: **`enaaafcasF1.b1`**, file `enaaafcasF1.b1.20180218.122850.nc`
(7.05 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=15168, `bound`=2, `particle_diameter`=30 |
| Data variables | 51 |
| QC variables | 5 (`qc_` companions) |
| Median time step | 1 s |
| File time span | 2018-02-18T12:28:50 to 2018-02-18T16:41:37 |
| dod version | aafcas-b1-1.0 |
| process version | ingest-aafcascorr-1.0-1.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `counts` | count | time,particle_diameter | yes | Particle counts |
| `laser_current` | mA | time | yes | Laser current |
| `back_block_temperature` | degC | time | - | Back block temperature |
| `forward_block_temperature` | degC | time | - | Forward block temperature |
| `laser_pd` | V | time | - | Laser photodiode |
| `num_pbp_packets` | count | time | - | Number of particle by particle packets |
| `p_apd_voltage` | V | time | - | P avalanche photodiode voltage |
| `p_back_tec_temperature` | degC | time | - | P back detector thermoelectric cooler temperature |
| `p_hi_bandwidth` | count | time | - | High bandwidth of intensity of light back scattered perpendicular to... |
| `p_hi_baseline` | count | time | - | High baseline of intensity of light back scattered perpendicular to... |
| `p_low_bandwidth` | count | time | - | Low baseline of intensity of light back scattered perpendicular to... |
| `p_low_baseline` | count | time | - | Low bandwidth of intensity of light back scattered perpendicular to... |
| `p_oversize` | count | time | - | Number of oversized particles based on intensity of light back... |
| `particle_diameter` | um | particle_diameter | - | Coordinate variable for particle_diameter |
| `qual_hi_bandwidth` | count | time | - | High bandwidth of qualified particles within the depth-of-field of... |
| `qual_hi_baseline` | count | time | - | High baseline of qualified particles within the depth-of-field of the... |
| `qual_low_bandwidth` | count | time | - | Low bandwidth of qualified particles within the depth-of-field of the... |
| `qual_low_baseline` | count | time | - | Low baseline of qualified particles within the depth-of-field of the... |
| `qual_oversize` | count | time | - | Number of oversized particles from the qualifier |
| `qualifer_apd_voltage` | V | time | - | Qualifier avalanche photodiode voltage |
| `qualifier_tec_temperature` | degC | time | - | Qualifier thermoelectric cooler temperature |
| `s_apd_voltage` | V | time | - | S avalanche photodiode voltage |
| `s_dpol_tec_temperature` | degC | time | - | S dual polarization thermoelectric cooler temperature |
| `s_hi_bandwidth` | count | time | - | High bandwidth of intensity of light back scattered parallel to laser... |
| `s_hi_baseline` | count | time | - | High baseline of intensity of light back scattered parallel to laser... |
| `s_low_bandwidth` | count | time | - | Low bandwidth of intensity of light back scattered parallel to laser... |
| `s_low_baseline` | count | time | - | Low baseline of intensity of light back scattered parallel to laser... |
| `s_oversize` | count | time | - | Number of oversized particles based on intensity of light back... |
| `sizer_apd_voltage` | V | time | - | Sizer avalanche photodiode voltage |
| `sizer_hi_bandwidth` | count | time | - | High bandwidth of light scattered from particles |


_11 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "enaaafcasF1.b1",
                             "start": "2018-02-18", "end": "2018-02-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./enaaafcasF1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "enaaafcasF1.b1", "2018-02-18", "2018-02-18")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("enaaafcasF1.b1", "2018-02-18", "2018-02-18"))   # cite what you pulled
```

This datastream carries 51 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "enaaafcasF1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["counts", "laser_current", "back_block_temperature", "qc_counts", "qc_laser_current"],
                                cleanup_qc=True)
```

## Quality control in this datastream

5 `qc_` companion variables cover 5 of the
51 data variables. Assessments present in the example file: `Bad`, `Indeterminate`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_laser_current"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("laser_current", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["laser_current", "counts", "lat"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enaaafcasF1.b1", "20170308", "20260923")
```

The handbook's own note on data quality: Data columns include a Data_Flag and a Cloud_Flag for both CAS and CIP output (ICARTT format). No links to a dedicated Data Quality (DQ) webpage were found for this instrument; an example DQ plot browser figure from the Two-Column Aerosol Project (TCAP) is shown. S&P (S high, S low, P high, P low) qualifier data are used on a particle-by-particle basis to assess whether size data are good (in focus) or should be rejected.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| CIP undersizing/discrepancy vs 2DS-AIR at larger sizes | Large discrepancies observed between the 2DS and CIP at sizes greater than 150 µm. | It is recommended one uses the 2DS-AIR data over the CIP data for particles greater than 150 µm. | (hb p. 11) |
| Particle out-of-focus sizing error in CAS | If the particle is not perfectly between the sapphire windows, the amount of light bounced back will not correspond to the true size of the particle, seen as anomalous sizer values relative... | Use S&P qualifier data to reject out-of-focus particles (if 0.5*Sizer less than  Qualifier, particle is rejected); if S&P data are good, size data... | (hb p. 6) |
| High-concentration buffer/data collection uncertainty (CAS) | Increased uncertainty in concentration values at high particle concentrations. | Baumgardner et al. 2001 suggest +/- 15% in concentration as the uncertainty bound. | (hb p. 6) |
| CIP upper concentration limit | Concentration measurements become unreliable or saturate above the upper concentration range. | Upper concentration range up to 500 particles/cm3 for CIP with standard tips and arm width; depends on particle size. | (hb p. 6) |
| 2D image data variable storage interval when buffer fills (CIP) | Irregular/variable time intervals between stored 2D images when buffer fills. | - | (hb p. 6) |
| Ice shattering at probe tips | Spurious counts of small fragments appearing as many small particles following a large ice particle impact. | Korolev tips with 70mm beam opening installed on CIP probe to prevent ice shattering (Korolev 2013); PBP data (inter-arrival time) used to mask... | (hb p. 8) |
| True airspeed source error affecting CIP image sizing (pre-2019 data) | Distorted (elongated or squashed) CIP shadow images, leading to under-sizing of droplets, more pronounced at larger sizes. | For campaigns before 2019, post-processing used aircraft true airspeed rather than the CAPS probe's own pitot-tube airspeed; recommend using 2DS-AIR... | (hb p. 15) |
| Coincidence errors (CAS) | Multiple particles detected simultaneously appearing as a single larger or anomalous particle signal. | Particle inter-arrival time (PBP data) is used to limit coincidence errors. | (hb p. 6) |
| Refractive index dependence / aerosol correction needed | Sizing is based on a Mie curve computed for a specific refractive index (processed with 1.33 for liquid water); using CAS data for aerosols without correction can misrepresent particle size. | To use CAS data for aerosols, a correction will need to be made; operations use the threshold table for water to match its Mie curve. | (hb p. 8) |
| End-diode particle rejection (CIP sizing bias) | Particles shadowing diode number one or sixty-four are rejected from the sizing routine (though still generate a 2D image), potentially undercounting particles at the edge of the array. | - | (hb p. 14) |
| Data quality (DQ) webpage not found | No accessible link/documentation for data quality information for this instrument. | - | (hb p. 4) |
| Calibration database not yet integrated into ARM systems | Calibration history not retrievable from ARM's standard calibration database. | Contact Jason Tomlinson directly for calibration information; AAF is currently working to incorporate calibrations into ARM's databases. | (hb p. 4) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Field/lab calibration uses a glass/PSL bead calibration system (guiding pipe with vial of calibration beads, puff of compressed air) for CAS, and a spinning disk attachment (recreating perfectly spherical drops of known diameters) for CIP; HW is tested by spraying water on the wire and comparing to WCM. Vendor... (hb p. 10) |
| Calibration interval | In the field, CAPS is calibrated before and after the first and last research flights; one day a week is dedicated to calibrations, generally every other week. Between campaigns the probe is shipped to the vendor for in-depth calibration. Latest vendor calibration was October 2019; previous one was August 2016. (hb p. 10) |
| Traceability | Results of field/laboratory and vendor calibrations are currently tracked by AAF's director of engineering; AAF is working to incorporate calibrations into ARM's databases. (hb p. 10) |
| Routine maintenance | Use acetone on Q-tips to clean the CIP window before every flight. Clean any insects or residue from the surface of the probe if visible. (hb p. 18) |
| Maintenance interval | CAS windows are cleaned only on calibration days (once per week); CIP window cleaned before every flight. (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: 2DS-AIR (two-dimensional stereo probe aboard aircraft), FCDP (fast cloud droplet probe), WCM (water content meter), Gerber PVM-100a liquid water probe.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `CAPS` | cloud, aerosol, and precipitation spectrometer |
| `CAS` | cloud and aerosol spectrometer |
| `CIP` | cloud imaging probe |
| `HW` | hotwire (liquid water content sensor) |
| `LWC` | liquid water content |
| `DPOL` | dual polarization |
| `PBP` | particle by particle |
| `MVD` | median volume diameter |
| `ED` | effective diameter |
| `PSL` | polystyrene latex |
| `PADS` | personal automated design solutions (Particle Analysis and Display System) |
| `RTD` | resistance temperature detector |
| `2DS-AIR` | two-dimensional stereo probe aboard aircraft |
| `FCDP` | fast cloud droplet probe |


### References the handbook cites

- Baumgardner, D, H Jonsson, W Dawson, D O'Connor, and R Newton. 2001. "The cloud, aerosol and precipitation spectrometer: a new instrument for cloud investigations." Atmospheric Research 59-60: 251-264,...
- Korolev, Alexi. 2013. "Modification and Tests of Particle Probe Tips to Mitigate Effects of Ice Shattering." Journal of Atmospheric and Oceanic Technology 30(4): 690-708, https://doi.org/10.1175/JTECH-D-12-00142.1
- CAPS Manual: CAPS operator Manual 2010 w wiring schematics.pdf
- Cloud Aerosol Spectrometer with Particle by Particle Manual
- The Cloud Aerosol Spectrometer Depolarization Option

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/doe-sc-arm-tr-246.pdf (20 pages, DOE/SC-ARM-TR-246, by L Goldberger)
- Catalog record: ARM data-source index, `instrument_class_code=cas-air`, read 2026-09-23
- Example file: `enaaafcasF1.b1.20180218.122850.nc` from `enaaafcasF1.b1`, 7.05 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
