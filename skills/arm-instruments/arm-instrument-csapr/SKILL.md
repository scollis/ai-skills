---
name: arm-instrument-csapr
description: ARM C-Band Scanning ARM Precipitation Radar (csapr) - handbook-derived instrument reference. Measurement principle, reported quantities (ZDR, φDP, KDP, ρHV, NCP), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (corcsapr2cfrzppiqcM1.b1) and the variable inventory of a real file. Use when working with csapr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - csapr, C-Band Scanning ARM Precipitation Radar, corcsapr2cfrzppiqcM1.b1, ZDR, φDP, KDP, Cloud Properties, Transmitter - Pulse Systems Technology, Receiver - NCAR Hi-Q, C band, Ka band, L band, NCAR.
---

# CSAPR - C-Band Scanning ARM Precipitation Radar

The C-SAPR is a scanning polarimetric Doppler weather radar that transmits simultaneously in both H and V polarization to measure precipitation reflectivity, velocity, and hydrometeor properties, deployed at fixed sites (SGP and TWP) performing RHI, PPI, and vertical-pointing scans.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 19 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `csapr` |
| Handbook | [DOE/SC-ARM/TR-121 / K Widener, N Bharadwaj / November 2012](https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Transmitter: Pulse Systems Technology; Receiver: NCAR Hi-Q; Pedestal/Antenna: Advanced Radar Corporation (ARC) |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2011-03-25 to 2026-09-23 (active) |
| Datastreams with data | 78 across 6 sites |
| Sites | bnf, cor, dst, hou, sgp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/csapr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj. *C-Band Scanning ARM Precipitation Radar (C-SAPR) Handbook*, DOE/SC-ARM/TR-121, November 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The C-SAPR is a scanning polarimetric Doppler radar transmitting simultaneously in both H and V polarizations, with a 350-kW magnetron transmitter putting 125 kW of transmitted power on each polarization. The receiver operates in a coherent-on-receive mode using an NCAR-developed Hi-Q system. Reflectivity is computed from the meteorological radar range equation relating received power, range, system losses, antenna gain, pulse width, beamwidth, and the dielectric factor of water. Dual-polarization measurements exploit the oblate-spheroid shape of raindrops: larger drops are more oblate (larger horizontal axis relative to vertical), producing differences between horizontal and vertical reflectivity, differential reflectivity (ZDR), differential phase (φDP), specific differential phase (KDP), and correlation coefficient (ρHV), which together aid hydrometeor type discrimination and rainfall estimation beyond what single-polarization radars can provide.

**Siting.** One C-SAPR is deployed near the SGP Central Facility (Nardin, OK) near the triangular array of X-SAPRs; the second is deployed at the TWP site on Manus Island, Papua New Guinea (Lombrum). The C-SAPR performs RHI, PPI, and vertical-pointing scans depending on the site scan strategy; the C-SAPR is limited to scanning 92 degrees in elevation for RHI scans.

**Sampling.** native rate Sampling rate: 40 MHz (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| V (Doppler mean velocity) | - | - | - | - | (hb p. 6) |
| W (Doppler spectrum width) | - | - | - | - | (hb p. 6) |
| Z (Log channel reflectivity corrected for clutter) | dBZ | - | - | - | (hb p. 6) |
| ZDR (Differential reflectivity) | dB | - | - | - | (hb p. 6) |
| φDP (Differential phase) | degrees | - | - | - | (hb p. 6) |
| KDP (Specific differential phase) | deg/km | - | - | - | (hb p. 6) |
| ρHV (Dual-polarization correlation magnitude) | - | - | - | - | (hb p. 6) |
| NCP (Normalized coherent power) | - | - | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Transmitter Type | Magnetron | (hb p. 9) |
| Center frequency | 6.25 GHz | (hb p. 9) |
| Peak power output | 350 kW | (hb p. 9) |
| Pulse width | 200 ns–2 µs | (hb p. 9) |
| Polarization | dual polarization, simultaneous H and V | (hb p. 9) |
| Maximum duty cycle | 0.1% | (hb p. 9) |
| PRF | 200 Hz–2.7 kHz | (hb p. 9) |
| Transmitter Manufacturer | Pulse Systems Technology | (hb p. 9) |
| Receiver Type | coherent-on-receive, dual channel digital Hi-Q | (hb p. 9) |
| Dynamic range | greater than  80 dB | (hb p. 9) |
| Noise figure | 2.8 dB | (hb p. 9) |
| Sampling rate | 40 MHz | (hb p. 9) |
| Decimation factor | Adjustable | (hb p. 9) |
| Video bandwidth | Adjustable | (hb p. 9) |
| Processing software | TITAN | (hb p. 9) |
| Receiver Manufacturer | NCAR | (hb p. 9) |
| Antenna Type | direct feed parabolic reflector | (hb p. 10) |
| Diameter | 2.4 m | (hb p. 10) |
| 3 dB beam width | 0.9° | (hb p. 10) |
| Gain | 45.1 dBi | (hb p. 10) |
| Cross polarization isolation | - 32 dB | (hb p. 10) |
| 2-way radome loss | less than 1.0 dB | (hb p. 10) |
| Pedestal Type | azimuth over elevation | (hb p. 10) |
| Azimuth scan rate | up to 36°/s | (hb p. 10) |
| Elevation scan rate | up to 30°/s | (hb p. 10) |
| Pedestal manufacturer | ARC | (hb p. 10) |


## The data

Verified example: **`corcsapr2cfrzppiqcM1.b1`**, file `corcsapr2cfrzppiqcM1.b1.20190227.230933.nc`
(3.83 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=360, `range`=200, `sweep`=1 |
| Data variables | 52 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2019-02-27T23:09:33 to 2019-02-27T23:10:08 |
| dod version | csapr2cfrzppiqc-b1-1.0 |
| process version | ingest-sapr2cfrqc-0.0-0.dev0.dirty.el7 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `attenuation_corrected_differential_reflectivity` | dB | time,range | - | Rainfall attenuation-corrected differential reflectivity |
| `attenuation_corrected_differential_reflectivity_lag_1` | dB | time,range | - | Differential reflectivity estimated at lag 1 corrected for rainfall... |
| `attenuation_corrected_reflectivity_h` | dBZ | time,range | - | Rainfall attenuation-corrected reflectivity, horizontal channel |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `classification_mask` | 1 | time,range | - | Classification Mask |
| `copol_correlation_coeff` | 1 | time,range | - | Copolar correlation coefficient (also known as rhohv) |
| `differential_phase` | degree | time,range | - | Differential propagation phase shift |
| `differential_reflectivity` | dB | time,range | - | Differential reflectivity |
| `differential_reflectivity_lag_1` | dB | time,range | - | Differential reflectivity estimated at lag 1 |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `mean_doppler_velocity_v` | m/s | time,range | - | Doppler velocity, vertical channel |
| `normalized_coherent_power` | 1 | time,range | - | Normalized coherent power, also known as SQI. |
| `normalized_coherent_power_v` | 1 | time,range | - | Normalized coherent power, also known as SQI, Vertical Channel |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |
| `prt` | s | time | - | Pulse repetition time |
| `range` | m | range | - | Range to measurement volume |
| `reflectivity` | dBZ | time,range | - | Equivalent reflectivity factor |
| `reflectivity_v` | dBZ | time,range | - | Equivalent reflectivity factor, vertical channel |
| `signal_to_noise_ratio_copolar_h` | dB | time,range | - | Signal-to-noise ratio, horizontal channel |
| `signal_to_noise_ratio_copolar_v` | dB | time,range | - | Signal-to-noise ratio, vertical channel |
| `specific_attenuation` | db/km | time,range | - | Specific attenuation |
| `specific_differential_attenuation` | db/km | time,range | - | Specific differential attenuation |
| `specific_differential_phase` | degree/km | time,range | - | Specific differential phase (KDP) |
| `spectral_width` | m/s | time,range | - | Spectral width |
| `spectral_width_v` | m/s | time,range | - | Spectral Width, Vertical Channel |
| `sweep_end_ray_index` | 1 | sweep | - | Index of last ray in sweep |
| `sweep_mode` | 1 | sweep | - | Scan mode for sweep |


_18 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "corcsapr2cfrzppiqcM1.b1",
                             "start": "2019-02-27", "end": "2019-02-27", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./corcsapr2cfrzppiqcM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "corcsapr2cfrzppiqcM1.b1", "2019-02-27", "2019-02-27")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("corcsapr2cfrzppiqcM1.b1", "2019-02-27", "2019-02-27"))   # cite what you pulled
```

This datastream carries 52 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "corcsapr2cfrzppiqcM1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["attenuation_corrected_differential_reflectivity", "attenuation_corrected_differential_reflectivity_lag_1", "attenuation_corrected_reflectivity_h"],
                                cleanup_qc=True)
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 1 sweep, 360 rays x 200 gates, `scan_type='sector'`, fixed angle 90.0 deg.

```python
import pyart
radar = pyart.io.read("corcsapr2cfrzppiqcM1.b1.20190227.230933.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `attenuation_corrected_differential_reflectivity`, `attenuation_corrected_differential_reflectivity_lag_1`, `attenuation_corrected_reflectivity_h`, `censor_mask`, `classification_mask`, `copol_correlation_coeff`, `differential_phase`, `differential_reflectivity`, `differential_reflectivity_lag_1`, `mean_doppler_velocity`, `mean_doppler_velocity_v`, `normalized_coherent_power`, `normalized_coherent_power_v`, `reflectivity`, `reflectivity_v`, `signal_to_noise_ratio_copolar_h`, `signal_to_noise_ratio_copolar_v`, `specific_attenuation`, `specific_differential_attenuation`, `specific_differential_phase`, `spectral_width`, `spectral_width_v`, `uncorrected_copol_correlation_coeff`, `uncorrected_differential_phase`, `uncorrected_differential_reflectivity`, `uncorrected_differential_reflectivity_lag_1`, `uncorrected_mean_doppler_velocity_h`, `uncorrected_mean_doppler_velocity_v`, `uncorrected_reflectivity_h`, `uncorrected_reflectivity_v`, `uncorrected_spectral_width_h`, `uncorrected_spectral_width_v`, `unthresholded_power_copolar_h`, `unthresholded_power_copolar_v`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

### First look

The verified sweep points at zenith, so neither a plan view nor a time-height applies.

```python
import matplotlib.pyplot as plt

# An azimuth sweep at 90 deg elevation (a birdbath scan, used for ZDR
# calibration). Every ray points at zenith, so a plan view is meaningless -
# one ray is a vertical profile, and the spread across rays is the signal.
disp = pyart.graph.RadarDisplay(radar)
fig, ax = plt.subplots(figsize=(6, 4))
disp.plot_ray("reflectivity", 0, ax=ax)
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`, `classification_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("corcsapr2cfrzppiqcM1.b1", "20110325", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The Data Quality Office website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting and assessing (X-SAPR/C-SAPR) data quality. Plots of reflectivity, Doppler radial velocity, and dual-polarization variables provide a good indicator of whether the system is operational. Instrument mentors review C-SAPR data via routine review (usually daily Monday-Friday), upon request by Site Operations, the site scientist team, an ARM data translator, or a data user, and when notified automatically by built-in test email messages. Data Assessments by Site Scientist/Data Quality Office: To...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| RHI elevation scan limitation | RHI scans truncated/incomplete near zenith or nadir; cannot reach full horizon-to-horizon 180 degrees | C-SAPR is limited to scanning 92 degrees in elevation | (hb p. 11) |
| Non-netCDF data format (MDV) | Standard netCDF tools cannot read C-SAPR files directly; files appear in NCAR TITAN MDV format instead | Use NCAR's TITAN 'PrintMdv' program to get a text dump of an MDV file; consult TITAN documentation | (hb p. 12) |
| Clutter contamination in reflectivity | Elevated or anomalous reflectivity values near ground clutter/obstructions | Z variable is described as 'Log channel reflectivity corrected for clutter', implying a clutter correction is applied | (hb p. 12) |
| Dielectric factor temperature/frequency dependence | Reflectivity (Z) values can be biased if the assumed dielectric factor does not match actual drop temperature | A fixed dielectric factor of 0.93 (water at 0°C) is used for C-SAPR reflectivity computation | (hb p. 13) |
| Single-polarization ambiguity in hydrometeor type/rainfall estimation (context for why... | Rainfall-rate estimates from reflectivity alone vary by climatic regime and cannot distinguish hydrometeor type | Dual-polarization variables (ZDR, φDP, KDP, ρHV) are used to alleviate these shortcomings | (hb p. 14) |
| KDP insensitivity to received power / tumbling hail | KDP measurements unaffected by spherical particles like tumbling hail, unlike reflectivity-based estimates | Use KDP, a propagation variable independent of received power, for rainfall estimation in mixed rain-ice | (hb p. 15) |
| No value-added products currently available | No corrected-moments or gridded-moments products exist yet; users must work with raw MDV moments data | Plans exist to produce a 'corrected moments' product (velocity/range dealiasing, water vapor attenuation correction) and later a gridded moments... | (hb p. 16) |
| Water vapor attenuation (implied, uncorrected) | Potential underestimation of reflectivity due to uncorrected atmospheric/water vapor attenuation | Planned future 'corrected moments' product will include water vapor attenuation correction | (hb p. 16) |
| Velocity/range aliasing (implied, uncorrected) | Doppler velocity or range ambiguities/aliasing not yet corrected in current data | Planned future 'corrected moments' product will include velocity and range dealiasing | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | To be included in manufacturer's documentation and the ARM Common Calibration database. Contact the instrument mentor for information. (hb p. 17) |
| Routine maintenance | See the NCAR TITAN documentation. (hb p. 17) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |
| `pyart-foundations` | the `Radar` object, fields, sweeps, IO, cmweather |
| `pyart-gatefilter-qc` | gate filtering for radar moments |

Instruments the handbook names as complements or predecessors: X-SAPR, Ka-band ARM zenith radar, W-band ARM cloud radar.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `φDP` | differential phase |
| `ρHV` | correlation coefficient between H and V polarizations |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `C band` | frequencies between 4 GHz and 8 GHz |
| `dB` | decibel |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `DQ` | Data Quality |
| `GHz` | gigahertz (10^9 Hz) |
| `Hz` | hertz |
| `Ka band` | frequencies between 26.5 GHz and 40 GHz |
| `KDP` | specific differential phase |
| `kW` | kilowatt |


### References the handbook cites

- Bharadwaj N, K Widener, A Koontz, and K Johnson. "Data Specification for ARM Scanning Radars." In progress.
- Bringi VN, and V Chandrasekar. 2001. Polarimetric Doppler Weather Radar. Cambridge University Press, Cambridge, United Kingdom.
- Doviak RJ, and DS Zrnic. 1993. Doppler Radar and Weather Observations. 2nd Edition, Academic Press, San Diego, California

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/csapr_handbook.pdf (19 pages, DOE/SC-ARM/TR-121, by K Widener, N Bharadwaj)
- Catalog record: ARM data-source index, `instrument_class_code=csapr`, read 2026-09-23
- Example file: `corcsapr2cfrzppiqcM1.b1.20190227.230933.nc` from `corcsapr2cfrzppiqcM1.b1`, 3.83 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
