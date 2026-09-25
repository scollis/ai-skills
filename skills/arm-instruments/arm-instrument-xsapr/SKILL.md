---
name: arm-instrument-xsapr
description: ARM X-Band Scanning ARM Precipitation Radar (xsapr) - handbook-derived instrument reference. Measurement principle, reported quantities (ZT, ZDR, φDP, KDP, ρHV), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsaxsaprcfrqcC1.b1) and the variable inventory of a real file. Use when working with xsapr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - xsapr, X-Band Scanning ARM Precipitation Radar, nsaxsaprcfrqcC1.b1, ZT, ZDR, φDP, Cloud Properties, Radtec Engineering, Inc. (transmitter/pedestal/radar control processor), CCDB, Ka band, W band, X band.
---

# XSAPR - X-Band Scanning ARM Precipitation Radar

X-SAPR is a full-hemispherical scanning polarimetric Doppler radar operating in X-band that simultaneously transmits H and V polarizations to measure cloud and precipitation reflectivity, Doppler velocity, and dual-polarization variables, deployed in a scanning array around ARM SGP and NSA sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `xsapr` |
| Handbook | [DOE/SC-ARM/TR-117 / K Widener, N Bharadwaj / October 2012](https://www.arm.gov/publications/tech_reports/handbooks/xsapr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Radtec Engineering, Inc. (transmitter/pedestal/radar control processor); Vaisala Sigmet RVP-900/RVP901 (receiver/processor) |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2010-12-14 to 2026-09-23 (active) |
| Datastreams with data | 69 across 3 sites |
| Sites | ena, nsa, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/xsapr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj. *X-band Scanning ARM Precipitation Radar (X-SAPR)*, DOE/SC-ARM/TR-117, October 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/xsapr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The X-SAPR measures the equivalent radar reflectivity factor via the meteorological radar range equation, relating received power to transmitted power, range, antenna gain, pulse width, beamwidth, system/atmospheric losses, and the dielectric factor of water (Kw2). Because it transmits and receives simultaneously in both horizontal (H) and vertical (V) polarizations, it can exploit the fact that raindrops are oblate spheroids (more oblate as they grow larger) to derive dual-polarization variables: differential reflectivity (ZDR), differential propagation phase shift (φDP), specific differential phase (KDP), and co-polar correlation coefficient magnitude (ρHV). These dual-pol variables allow hydrometeor type discrimination and improved rainfall estimation compared to single-polarization radars, which rely on empirically derived parametric models. The receiver operates in a coherent-on-receive mode (Vaisala Sigmet RVP-900) to also derive Doppler mean velocity and spectrum width from the linear channel signals.

**Siting.** Three X-SAPRs are deployed around the SGP Central Facility in a triangular array (at Billings OK/SGP I4, Garber OK/SGP I5, and Lamont OK/SGP I6). A fourth X-SAPR is deployed near Barrow, Alaska (NSA/C1) on top of the Barrow Arctic Research Center. Scan strategies (RHI, PPI, vertical pointing, sector scan, calibration) are defined per site and alternate during operation; sector scans perpendicular to prevailing wind direction are typical, though parallel sector scans can be manually configured by the instrument mentor.

**Sampling.** native rate Sampling rate 80 MHz (receiver digitization); PRF 200 Hz–2.7 kHz (example header shows PRF: 2222Hz); averaging Example header: Samples: 90 (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| V (linear channel Doppler mean velocity) | - | - | - | - | (hb p. 8) |
| W (linear channel Doppler spectrum width) | - | - | - | - | (hb p. 8) |
| Z (log channel reflectivity corrected for clutter) | dBZ | - | - | - | (hb p. 8) |
| ZT (log channel total reflectivity including clutter) | dBZ | - | - | - | (hb p. 8) |
| ZDR (differential reflectivity) | dB | - | - | - | (hb p. 8) |
| φDP (differential phase) | degrees | - | - | - | (hb p. 8) |
| KDP (specific differential phase) | - | - | - | - | (hb p. 9) |
| ρHV (dual polarization correlation magnitude) | - | - | - | - | (hb p. 9) |
| SQI (signal quality index) | - | - | - | - | (hb p. 9) |


## Specifications

| parameter | value | source |
|---|---|---|
| Transmitter Type | Magnetron | (hb p. 9) |
| Center frequency | 9.35–9.45 GHz | (hb p. 9) |
| Peak power output | 200 kW | (hb p. 9) |
| Pulse width | 200 ns–2 µs | (hb p. 9) |
| Polarization | dual-polarization, simultaneous H and V | (hb p. 9) |
| Maximum duty cycle | 0.1% | (hb p. 9) |
| PRF | 200 Hz–2.7 kHz | (hb p. 9) |
| Transmitter Manufacturer | Radtec | (hb p. 9) |
| Receiver Type | coherent-on-receive, dual channel digital Vaisala RVP-900 | (hb p. 9) |
| Dynamic range (receiver) | greater than  80 dB | (hb p. 9) |
| Noise figure | 3.0 dB | (hb p. 9) |
| Sampling rate | 80 MHz | (hb p. 9) |
| Decimation factor | Adjustable | (hb p. 9) |
| Video bandwidth | Adjustable | (hb p. 9) |
| Processing software | IRIS | (hb p. 9) |
| Receiver Manufacturer | Vaisala | (hb p. 9) |
| Antenna Type | offset feed parabolic reflector | (hb p. 10) |
| Antenna Diameter | 2.4 m | (hb p. 10) |
| 3 dB beam width | 1.0° | (hb p. 10) |
| Gain | 45.0 dBi | (hb p. 10) |
| Cross polarization isolation | -32 dB | (hb p. 10) |
| 2-way radome loss | less than 1.0 dB | (hb p. 10) |
| Pedestal Type | azimuth over elevation | (hb p. 10) |
| Azimuth scan rate | up to 36°/s | (hb p. 10) |
| Elevation scan rate | up to 30°/s | (hb p. 10) |
| Pedestal manufacturer | Radtec | (hb p. 10) |


_13 further specification rows are in the handbook._

## The data

Verified example: **`nsaxsaprcfrqcC1.b1`**, file `nsaxsaprcfrqcC1.b1.20260109.110010.nc`
(14.41 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=2592, `range`=401, `sweep`=4, `r_calib`=1, `frequency`=1 |
| Data variables | 41 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2026-01-09T11:00:10 to 2026-01-09T11:04:33 |
| dod version | xsaprcfrqc-b1-1.1 |
| process version | ingest-saprcfrqc-0.0-0.dev0.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `attenuation_corrected_differential_reflectivity` | dB | time,range | - | Rainfall attenuation-corrected differential reflectivity |
| `attenuation_corrected_reflectivity_h` | dBZ | time,range | - | Rainfall attenuation-corrected reflectivity, horizontal channel |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `cross_correlation_ratio_hv` | 1 | time,range | - | Cross-polar correlation ratio |
| `differential_phase` | degree | time,range | - | Differential propagation phase shift |
| `differential_reflectivity` | dB | time,range | - | Differential reflectivity |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `frequency` | Hz | frequency | - | Transmit center frequency |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `n_samples` | 1 | time | - | Number of samples used to compute moments |
| `normalized_coherent_power` | 1 | time,range | - | Normalized coherent power, also known as SQI |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |
| `prt` | s | time | - | Pulse repetition time |
| `prt_mode` | 1 | sweep | - | Transmit pulse mode |
| `r_calib_radar_constant_h` | dB | r_calib | - | Calibrated radar constant horizontal channel |
| `r_calib_radar_constant_v` | dB | r_calib | - | Calibrated radar constant vertical channel |
| `radar_echo_classification` | 1 | time,range | - | Radar echo classification |
| `radar_measured_transmit_power` | dBm | time | - | Radar measured transmit peak power |
| `radar_receiver_bandwidth` | Hz | - | - | Radar receiver bandwidth |
| `range` | m | range | - | Range to measurement volume |
| `reflectivity` | dBZ | time,range | - | Equivalent reflectivity factor |
| `reflectivity_enhanced` | dBZ | time,range | - | Equivalent reflectivity factor enhanced |
| `reflectivity_v` | dBZ | time,range | - | Equivalent reflectivity factor, vertical channel |
| `signal_to_noise_ratio` | dB | time,range | - | Signal-to-noise ratio, horizontal channel |
| `specific_differential_phase` | degree/km | time,range | - | Specific differential phase (KDP) |
| `spectral_width` | m/s | time,range | - | Spectral width |
| `sweep_end_ray_index` | 1 | sweep | - | Index of last ray in sweep |
| `sweep_mode` | 1 | sweep | - | Scan mode for sweep |


_8 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "nsaxsaprcfrqcC1.b1",
                             "start": "2026-01-09", "end": "2026-01-09", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./nsaxsaprcfrqcC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "nsaxsaprcfrqcC1.b1", "2026-01-09", "2026-01-09")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("nsaxsaprcfrqcC1.b1", "2026-01-09", "2026-01-09"))   # cite what you pulled
```

This datastream carries 41 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "nsaxsaprcfrqcC1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["attenuation_corrected_differential_reflectivity", "attenuation_corrected_reflectivity_h", "azimuth"],
                                cleanup_qc=True)
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 4 sweep, 2592 rays x 401 gates, `scan_type='rhi'`, fixed angle 51.998291015625 deg.

```python
import pyart
radar = pyart.io.read("nsaxsaprcfrqcC1.b1.20260109.110010.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `attenuation_corrected_differential_reflectivity`, `attenuation_corrected_reflectivity_h`, `censor_mask`, `cross_correlation_ratio_hv`, `differential_phase`, `differential_reflectivity`, `mean_doppler_velocity`, `normalized_coherent_power`, `radar_echo_classification`, `reflectivity`, `reflectivity_enhanced`, `reflectivity_v`, `signal_to_noise_ratio`, `specific_differential_phase`, `spectral_width`, `total_power`, `total_power_enhanced`, `total_power_v`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsaxsaprcfrqcC1.b1", "20101214", "20260923")
```

The handbook's own note on data quality: The Data Quality Office website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting and assessing X-SAPR data quality. Plots of reflectivity, Doppler radial velocity, and dual-polarization variables provide a good indicator of whether the system is operational. Instrument mentors review X-SAPR data routinely (usually daily Monday-Friday), upon request from Site Operations, site scientist team, ARM data translator, or data user, and when automatically notified by the X-SAPR's built-in-test (BIT) email messages. Data Assessments by Site Scientist/Data Quality Office section...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Ground clutter contamination in reflectivity | Elevated total reflectivity (ZT) near ground/near-range gates compared to clutter-corrected reflectivity (Z); IRIS header flags such as block_zc, attn_zc, target_zc indicate clutter... | Reflectivity flags include clutter correction (block_zc, attn_zc, target_zc, DPATTEN_ZC, dpatten_z) applied to produce Z (clutter-corrected) vs ZT... | (hb p. 14) |
| Velocity aliasing/folding | Doppler velocity field shows sudden sign reversals or discontinuities (unfolding); IRIS VFlags include unfold_vc and fall_vc indicating velocity unfolding processing | VFlags such as unfold_vc, fall_vc, ship_v, storm_vc are applied in processing to correct/unfold velocity | (hb p. 14) |
| Attenuation of radar signal by liquid water | Reduced reflectivity/differential phase behind heavy precipitation cells; dielectric factor of water depends on frequency and temperature, affecting derived Z accuracy | A value of dielectric factor Kw2 = 0.93 is used for X-SAPR computations; planned 'corrected moments' VAP will include water vapor attenuation... | (hb p. 15) |
| No netCDF ingestion / proprietary IRIS format | Data files are in Vaisala IRIS binary format rather than netCDF, requiring specialized software (IRIS viewer) to read | A free version of IRIS software for viewing data is available from Vaisala (Fee Display License) | (hb p. 8) |
| No value-added products currently available | Absence of corrected/gridded moments products; users must work with raw IRIS moments | Plans exist to produce a 'corrected moments' product including velocity/range dealiasing and water vapor attenuation correction, followed by a... | (hb p. 13) |
| Threshold/quality filtering of moments | Data below threshold settings (e.g., T Threshold LOG = 0.8 dB, Z Threshold SIG = 5.0 dB, V Threshold CSR = 18.0 dB, W Threshold SQI = 0.40) may be flagged or excluded depending on scan... | Header lists threshold settings per scan (e.g., 'All Pass' in example) that determine data acceptance | (hb p. 14) |
| Manual sector scan setup required for non-standard geometries | Sector scans parallel to wind direction do not occur automatically; absence of such data unless manually configured | These sector scans must be set up manually by the radar instrument mentor | (hb p. 7) |
| Single-polarization ambiguity in hydrometeor type/rainfall estimation (contextual... | Without dual-pol variables, reflectivity alone cannot distinguish hydrometeor type and rainfall rate estimates rely on empirically derived parametric models that vary by climatic regime | Dual-polarization variables (ZDR, φDP, KDP, ρHV) are used to alleviate these shortcomings | (hb p. 10) |
| System operational status issues detected via built-in test | X-SAPR's built-in-test (BIT) email messages notify of anomalies | Instrument mentors are notified automatically by BIT email messages and perform review | (hb p. 12) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Points at a predetermined fixed azimuth and elevation to view a fixed corner-reflector target of known radar cross-section to provide an absolute calibration point (scanning radar with narrow beamwidth). (hb p. 7) |
| Traceability | To be included in manufacturer's documentation and the ARM Common Calibration (CCDB) database. (hb p. 7) |
| Routine maintenance | Instrument mentors review data for nominal operation; operation and maintenance information available in manufacturer's documentation; contact instrument mentor for information. (hb p. 18) |
| Maintenance interval | Routine review usually daily Monday–Friday (hb p. 18) |


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

Instruments the handbook names as complements or predecessors: Ka-band ARM zenith radar, W-band ARM cloud radar.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `φDP` | differential phase |
| `φHH` | horizontal signal |
| `φVV` | vertical signal |
| `ρHV` | dual-polarization correlation magnitude |
| `3D` | three-dimensional |
| `ARM` | Atmospheric Radiation Measurement (Climate Research Facility) |
| `BIT` | built-in-test (messages) |
| `CCDB` | Common Calibration Database |
| `dB` | decibel |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `GHz` | gigahertz (10^9 Hz) |
| `Hz` | hertz |


### References the handbook cites

- Bharadwaj N, K Widener, A Koontz, and K Johnson. "Data Specification for ARM Scanning Radars." In progress.
- Bringi VN and V Chandrasekar. 2001. Polarimetric Doppler Weather Radar. Cambridge University Press, Cambridge, United Kingdom.
- Doviak RJ and DS Zrnic. 1993. Doppler Radar and Weather Observations. 2nd Edition, Academic Press, San Diego, California.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/xsapr_handbook.pdf (22 pages, DOE/SC-ARM/TR-117, by K Widener, N Bharadwaj)
- Catalog record: ARM data-source index, `instrument_class_code=xsapr`, read 2026-09-23
- Example file: `nsaxsaprcfrqcC1.b1.20260109.110010.nc` from `nsaxsaprcfrqcC1.b1`, 14.41 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
