---
name: arm-instrument-xsacr
description: ARM X-Band Scanning ARM Cloud Radar (xsacr) - handbook-derived instrument reference. Measurement principle, reported quantities (reflectivity_copol, reflectivity_xpol, mean_doppler_velocity_copol, mean_doppler_velocity_xpol, spectral_width_copol, spectral_width_xpol, reflectivity, mean_doppler_velocity), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (houxsacrcfrqcM1.b1) and the variable inventory of a real file. Use when working with xsacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - xsacr, X-Band Scanning ARM Cloud Radar, houxsacrcfrqcM1.b1, reflectivity_copol, reflectivity_xpol, mean_doppler_velocity_copol, mean_doppler_velocity_xpol, spectral_width_copol, spectral_width_xpol, Cloud Properties, ProSensing, Inc. (instrument developer).
---

# XSACR - X-Band Scanning ARM  Cloud Radar

The Scanning ARM Cloud Radar (SACR) is a polarimetric Doppler radar (X-, Ka-, and W-band variants) mounted on a scanning pedestal to observe the 3D structure, reflectivity, and Doppler motion of clouds via RHI, PPI, sector, vertical-pointing, and calibration scans at ARM fixed and mobile sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 37 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `xsacr` |
| Handbook | [DOE/SC-ARM/TR-113 / K Widener, N Bharadwaj, K Johnson / June 2012](https://www.arm.gov/publications/tech_reports/handbooks/xsacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. (instrument developer); transmitter manufacturer CPI (X-band) / CPI Canada with CPI Beverly modulator (Ka/W-band); receiver processing by Mercury Computers; pedestal by Orbit... |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2011-09-14 to 2026-09-23 (active) |
| Datastreams with data | 117 across 7 sites |
| Sites | awr, bnf, cor, gan, hou, tmp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/xsacr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj, K Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj, K Johnson. *Scanning ARM Cloud Radar (X/Ka/W-SACR)*, DOE/SC-ARM/TR-113, June 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/xsacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `kasacr`, `wsacr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `xsacr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The SACR transmits pulsed microwave radiation at X-, Ka-, or W-band frequencies and receives the backscattered power from cloud and precipitation particles to compute the equivalent reflectivity factor via the meteorological radar range equation, which depends on wavelength, range, received power, atmospheric and system losses, pulse width, antenna gain and beamwidth, transmit power, and the dielectric factor of water (Kw^2). Doppler processing of the returned signal yields mean Doppler velocity and spectral width, representing the radial velocity and velocity dispersion of scatterers. The X-SACR transmits both H and V polarizations simultaneously, enabling dual-polarization parameters (ZDR, RHOHV, PHIDP, KDP) that provide information on particle shape, phase mixture, and size. The narrow antenna beamwidths on the scanning pedestal also permit absolute calibration by pointing at a fixed trihedral corner reflector of known radar cross-section.

**Siting.** Two SACRs share a single pedestal at each deployment site. Frequency pair selection is driven by atmospheric water vapor attenuation at the site: TWP sites use the X-/Ka-band pair; SGP and NSA sites use the Ka-/W-band pair; AMF1 has Ka/W-SACR and AMF2 has X/Ka-SACR. Deployed at SGP/C1 (Billings, OK), NSA/C1 (Barrow, AK), TWP/C1 (Manus, PNG), TWP/C3 (Darwin, AUS), AMF1 (Cape Cod, MA), and AMF2 (TBD).

**Sampling.** native rate Receiver sampling rate 120 MHz (all bands); averaging n_samples: Number of samples used to compute moments (per ray, variable) (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| reflectivity_copol | dBZ | - | 3 dBZ | - | (hb p. 30) |
| reflectivity_xpol | dBZ | - | 3 dBZ | - | (hb p. 30) |
| mean_doppler_velocity_copol | m/s | - | 0.1 m/s | - | (hb p. 30) |
| mean_doppler_velocity_xpol | m/s | - | 0.1 m/s | - | (hb p. 30) |
| spectral_width_copol | m/s | - | 0.1 m/s | - | (hb p. 30) |
| spectral_width_xpol | m/s | - | 0.1 m/s | - | (hb p. 30) |
| reflectivity (raw datastream field) | dBZ | - | - | scale_factor 0.002766339... | (hb p. 17) |
| mean_doppler_velocity (raw datastream field) | meters per second | - | - | scale_factor 0.0006447607 | (hb p. 17) |
| spectral_width (raw datastream field) | meters per second | - | - | scale_factor 0.0002320935... | (hb p. 17) |
| snr | dB | - | - | scale_factor 0.00305341... | (hb p. 17) |
| linear_depolarization_ratio | dB | - | - | scale_factor 0.001795543... | (hb p. 17) |
| Differential Reflectivity (ZDR) | - | - | - | - | (hb p. 29) |
| Correlation Coefficient (rhoHV / RHOHV) | - | near 1 indicates homogeneous... | - | - | (hb p. 29) |
| Differential Phase (phiDP / PHIDP) | - | - | - | - | (hb p. 30) |
| Specific Differential Phase (KDP) | - | - | - | - | (hb p. 30) |


## Specifications

| parameter | value | source |
|---|---|---|
| X-band SACR Center frequency | 9.710 GHz | (hb p. 7) |
| X-band SACR Peak power output | 20.0 kW | (hb p. 7) |
| X-band SACR Pulse width | 100 ns–40 µs | (hb p. 7) |
| X-band SACR Polarization | dual-polarization, simultaneous H and V | (hb p. 8) |
| X-band SACR Maximum duty cycle | 1% | (hb p. 8) |
| X-band SACR PRF | maximum 10 kHz | (hb p. 8) |
| X-band SACR Receiver dynamic range | greater than  80 dB | (hb p. 8) |
| X-band SACR Receiver noise figure | 4.5 dB | (hb p. 8) |
| X-band SACR Receiver sampling rate | 120 MHz | (hb p. 8) |
| X-band SACR Antenna diameter | 1.82 m | (hb p. 8) |
| X-band SACR 3 dB beam width | 1.40° | (hb p. 8) |
| X-band SACR Gain | 42.0 dBi | (hb p. 8) |
| X-band SACR Cross polarization isolation | -30 dB | (hb p. 8) |
| X-band SACR 2-way radome loss | less than 0.2 dB | (hb p. 8) |
| X-band SACR Azimuth scan rate | up to 36°/s | (hb p. 8) |
| X-band SACR Elevation scan rate | up to 20°/s | (hb p. 8) |
| Ka-band SACR Center frequency | 35.3 GHZ | (hb p. 8) |
| Ka-band SACR Peak power output | 2.0 kW | (hb p. 8) |
| Ka-band SACR Pulse width | 50 ns–13 µs | (hb p. 8) |
| Ka-band SACR Polarization | transmit horizontal linear | (hb p. 8) |
| Ka-band SACR Maximum duty cycle | 5% | (hb p. 8) |
| Ka-band SACR PRF | up to 10 kHz | (hb p. 8) |
| Ka-band SACR Receiver dynamic range | greater than  80 dB | (hb p. 9) |
| Ka-band SACR Receiver noise figure | 3.5 dB | (hb p. 9) |
| Ka-band SACR Antenna diameter | 1.82 m | (hb p. 9) |
| Ka-band SACR 3 dB beam width | 0.33° | (hb p. 9) |


_21 further specification rows are in the handbook._

## The data

Verified example: **`houxsacrcfrqcM1.b1`**, file `houxsacrcfrqcM1.b1.20220918.194606.nc`
(31.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=1254, `range`=1539, `sweep`=6, `group_pulse_number`=3, `r_calib`=1, `frequency`=1 |
| Data variables | 63 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2022-09-18T19:46:06 to 2022-09-18T19:49:33 |
| dod version | xsacrcfrqc-b1-1.1 |
| process version | ingest-sacrcfrqc-1.0-0.dev18.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_agl` | m | - | - | Altitude above ground level |
| `antenna_transition` | 1 | time | - | Antenna is in transition between sweeps |
| `attenuation_corrected_differential_reflectivity` | dB | time,range | - | Rainfall attenuation-corrected differential reflectivity |
| `attenuation_corrected_reflectivity_h` | dBZ | time,range | - | Rainfall attenuation-corrected reflectivity, horizontal channel |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `copol_correlation_coeff` | 1 | time,range | - | Copolar correlation coefficient (also known as rhohv) |
| `differential_phase` | degree | time,range | - | Differential propagation phase shift |
| `differential_reflectivity` | dB | time,range | - | Differential reflectivity |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `frequency` | Hz | frequency | - | Transmit center frequency |
| `group_intra_pulse_prt` | s | group_pulse_number | - | Prt between group pulses |
| `instrument_type` | 1 | - | - | Type of instrument |
| `mean_doppler_velocity` | m/s | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `n_samples` | 1 | time | - | Number of Samples used to compute moments |
| `nyquist_velocity` | m/s | time | - | Unambiguous doppler velocity |
| `platform_type` | 1 | - | - | Platform type |
| `polarization_mode` | 1 | sweep | - | Polarization mode for sweep |
| `primary_axis` | 1 | - | - | Primary axis of rotation |
| `prt` | s | time | - | Pulse repetition time |
| `prt_mode` | 1 | sweep | - | Transmit pulse mode |
| `pulse_width` | s | time | - | Transmitter pulse width |
| `r_calib_index` | 1 | time | - | Calibration data array index per ray |
| `r_calib_noise_hc` | dBm | r_calib | - | Measured noise level horizontal copolar channel |
| `r_calib_noise_source_power_h` | dBm | r_calib | - | Noise source power horizontal channel |
| `r_calib_noise_source_power_v` | dBm | r_calib | - | Noise source power vertical channel |
| `r_calib_noise_vc` | dBm | r_calib | - | Measured noise level vertical copolar channel |
| `r_calib_pulse_width` | s | r_calib | - | Calibrated Pulse Width |
| `r_calib_radar_constant_h` | dB | r_calib | - | Calibrated radar constant horizontal channel |


_30 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "houxsacrcfrqcM1.b1",
                             "start": "2022-09-18", "end": "2022-09-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./houxsacrcfrqcM1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "houxsacrcfrqcM1.b1", "2022-09-18", "2022-09-18")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("houxsacrcfrqcM1.b1", "2022-09-18", "2022-09-18"))   # cite what you pulled
```

This datastream carries 63 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "houxsacrcfrqcM1.b1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=["altitude_agl", "antenna_transition", "attenuation_corrected_differential_reflectivity"],
                                cleanup_qc=True)
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 6 sweep, 1254 rays x 1539 gates, `scan_type='rhi'`, fixed angle -0.0 deg.

```python
import pyart
radar = pyart.io.read("houxsacrcfrqcM1.b1.20220918.194606.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `attenuation_corrected_differential_reflectivity`, `attenuation_corrected_reflectivity_h`, `censor_mask`, `copol_correlation_coeff`, `differential_phase`, `differential_reflectivity`, `mean_doppler_velocity`, `reflectivity`, `signal_to_noise_ratio_copolar_h`, `signal_to_noise_ratio_copolar_v`, `specific_attenuation`, `specific_differential_attenuation`, `specific_differential_phase`, `spectral_width`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

### First look

The verified sweep is an RHI - fixed azimuth, elevation varying - so range-height it is.

```python
import matplotlib.pyplot as plt

# A fixed-azimuth elevation sweep: range-height, not a plan view.
disp = pyart.graph.RadarDisplay(radar)
fig, ax = plt.subplots(figsize=(8, 4))
disp.plot_rhi("reflectivity", sweep=0, ax=ax)
fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("houxsacrcfrqcM1.b1", "20110914", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The reported qc_time field contains bit-packed QC results (bit 1: delta time between current and previous samples is zero; bit 2: delta time less than delta_t_lower_limit; bit 3: delta time greater than delta_t_upper_limit), all assessed as 'Indeterminate', with no bits set representing good data. The DQO website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting SACR data quality; plots of reflectivity, Doppler radial velocity, and Doppler spectral width provide a good indicator of whether the system is operational. Instrument mentors review data routinely (daily M-F) and...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| No value-added products (VAPs) currently exist for SACR | Only raw moments datastreams are available; no dealiased velocity, attenuation-corrected reflectivity, or gridded cloud-boundary product exists yet | Plans exist to produce a 'corrected moments' product (velocity and range dealiasing, water vapor attenuation correction) and later a gridded moments... | (hb p. 26) |
| X-SACR dual-polarization products (ZDR, RHOHV, PHIDP, KDP) not yet in released data files | Initial X-SACR data files contain the same fields as Ka/W-SACR files; dual-pol variables are absent despite X-SACR transmitting simultaneous H/V | These parameters will be included in a future release of the ingested X-SACR data file | (hb p. 24) |
| Doppler variable uncertainty only characterized for zenith-pointing (vertical mode) | Uncertainty values of 0.1 m/s for Doppler velocity/spectral width in Table 2 apply to vertical-pointing mode only; scanning-mode uncertainty may differ | Uncertainty for scanning mode is to be determined at each frequency band | (hb p. 24) |
| RF attenuation by atmospheric water vapor drives frequency-pair siting choice | Signal attenuation differs by site/band combination; TWP (humid) sites use lower-attenuation X-/Ka-band pair while drier SGP/NSA sites use Ka-/W-band pair, affecting comparability of... | Frequency pair selected per site based on atmospheric water vapor content | (hb p. 7) |
| Antenna transition between sweeps produces non-representative rays | antenna_transition flag = 1 during transition periods between sweeps, indicating antenna is not in a stable pointing position | Field is provided so these rays can be identified/excluded | (hb p. 11) |
| qc_time bit flags for anomalous sample timing | Bit 1: zero delta time between samples; Bit 2: delta time below delta_t_lower_limit (0.01s); Bit 3: delta time above delta_t_upper_limit (30s); all flagged as 'Indeterminate' assessment | No bits set (zero) represents good data; users should check qc_time before using data | (hb p. 10) |
| Manually entered azimuth for sector (cross-wind/along-wind) scans | Sector scan azimuth directions not automatically determined; could be stale or mis-set if not manually updated to correspond to current wind direction at the target altitude | Azimuth directions must be entered manually | (hb p. 14) |
| Dielectric factor of water (Kw^2) is temperature- and frequency-dependent but a fixed 0°C... | Reflectivity values computed using a constant Kw^2 (0.93 X-band, 0.88 Ka-band, 0.70 W-band) assuming 0°C liquid water; may not represent actual hydrometeor phase/temperature | - | (hb p. 31) |
| Radar system and two-way radome losses reduce received power / affect calibration | 2-way radome loss (less than 0.2 dB X-band; 1.5 dB Ka- and W-band) enters into the radar range equation as Lsys and can bias reflectivity if not accounted for | Radome loss parameters (r_calib_two_way_radome_loss_h) stored per calibration record for correction | (hb p. 8) |
| Instrument details, theory of operation, calibration procedures, and... | Sections 7.1-7.4 defer to a 'SACR Operations Manual' that is 'currently in progress'; annotated examples, user notes/known problems, and data quality assessment sections all marked 'To be... | Refer to forthcoming SACR Operations Manual for full instrument, calibration, and maintenance details | (hb p. 27) |
| Data quality assessment (Section 6.0) largely undocumented at time of writing | Data Quality Health and Status, Data Assessments by Site Scientist/DQO sections state 'To be determined'; only routine mentor review cadence and BIT email alerts are described | - | (hb p. 26) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Pointing the narrow-beamwidth antenna at a fixed trihedral corner reflector of known radar cross-section at a predetermined azimuth/elevation to provide an absolute calibration point. For Ka/W-SACRs a single corner reflector is used; X/Ka-SACR installations require a separate corner reflector for each radar band. (hb p. 29) |
| Traceability | Additional calibration information available in the ARM Common Calibration Database (CCDB); access limited to ARM Facility personnel. Detailed calibration procedures to be listed in the forthcoming SACR Operations Manual. (hb p. 29) |
| Routine maintenance | Instrument mentors perform routine review for nominal operation, usually daily Monday-Friday, plus reviews on request from site operations, site scientist team, ARM data translator, or data user, and when notified automatically by the SACR's built-in test (BIT) email messages. (hb p. 26) |
| Maintenance interval | daily (Monday-Friday) routine review (hb p. 26) |


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

Instruments the handbook names as complements or predecessors: KAZR, WACR, Ka-SACR, W-SACR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AGL` | above ground level |
| `ARM` | Atmospheric Radiation Measurement (Climate Research Facility) |
| `C band` | frequencies between 4 GHz and 8 GHz |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `DMF` | Data Management Facility |
| `DQO` | Data Quality Office (ARM) |
| `EIKA` | Extended Interaction Klystron Amplifier |
| `Ka band` | frequencies between 26.5 GHz and 40 GHz |
| `KA-SACR` | Ka-band scanning ARM cloud radar |
| `KAZR` | Ka-band ARM Zenith Radar |
| `KDP` | specific differential phase |
| `NSA` | North Slope of Alaska |


### References the handbook cites

- Bharadwaj, N, K Widener, A Koontz, and K Johnson. "Data Specification for ARM Scanning Radars", Draft ARM Technical Report May 2010
- Bringi, VN and V Chandrasekar. 2001. "Polarimetric Doppler Weather Radar." Cambridge University Press.
- Doviak, RJ and DS Zrnic. 1993. "Doppler Radar and Weather Observations." 2nd Edition, Academic Press.
- Mead, J. "Scanning ARM Cloud Radar (SACR) System Description and Operations Manual.". In process.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/xsacr_handbook.pdf (37 pages, DOE/SC-ARM/TR-113, by K Widener, N Bharadwaj, K Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=xsacr`, read 2026-09-23
- Example file: `houxsacrcfrqcM1.b1.20220918.194606.nc` from `houxsacrcfrqcM1.b1`, 31.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
