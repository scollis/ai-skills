---
name: arm-instrument-wsacr
description: ARM W-band Scanning ARM Cloud Radar (wsacr) - handbook-derived instrument reference. Measurement principle, reported quantities (reflectivity, mean_doppler_velocity, spectral_width, snr, linear_depolarization_ratio, reflectivity_copol, reflectivity_xpol, mean_doppler_velocity_copol), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (anxwsacrcfrqcM1.b1) and the variable inventory of a real file. Use when working with wsacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - wsacr, W-band Scanning ARM Cloud Radar, anxwsacrcfrqcM1.b1, reflectivity, mean_doppler_velocity, spectral_width, snr, linear_depolarization_ratio, reflectivity_copol, Cloud Properties, ProSensing, Inc. (vendor/instrument developer), SACR, X-SACR, KA-SACR, W-SACR.
---

# WSACR - W-band Scanning ARM Cloud Radar

The W-band Scanning ARM Cloud Radar (W-SACR) is a 94 GHz polarimetric Doppler cloud radar mounted on a shared pedestal with a Ka-band SACR, deployed at fixed ARM sites to scan clouds via RHI, PPI, vertical-pointing, sector, and calibration scan strategies to characterize cloud reflectivity, Doppler velocity, and spectrum width.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 37 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `wsacr` |
| Handbook | [DOE/SC-ARM/TR-113 / K Widener, N Bharadwaj, K Johnson / June 2012](https://www.arm.gov/publications/tech_reports/handbooks/wsacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. (vendor/instrument developer); transmitter by CPI Canada with CPI Beverly modulator |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2011-04-06 to 2026-09-23 (active) |
| Datastreams with data | 145 across 8 sites |
| Sites | anx, asi, ena, epc, nsa, oli, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/wsacr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj, K Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj, K Johnson. *Scanning ARM Cloud Radar (X/Ka/W-SACR)*, DOE/SC-ARM/TR-113, June 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/wsacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `kasacr`, `xsacr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `wsacr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The SACR is a polarimetric Doppler radar that transmits pulses at its operating frequency (94.0 GHz for W-band) and measures the backscattered power, phase, and polarization state from cloud and precipitation targets to derive reflectivity, Doppler velocity, and spectrum width. Equivalent reflectivity factor (dBZ) is computed from the meteorological radar range equation using received power, range, system losses, antenna gain, pulse width, beamwidth, transmit power, and the dielectric factor of water (Kw^2), with the W-SACR using a dielectric factor of 0.70 at 0°C. A narrow-beamwidth antenna on a scanning pedestal allows the SACR to point at a fixed trihedral corner reflector of known radar cross-section for absolute calibration. The instrument can be operated in scanning modes (RHI, PPI, sector) or in vertical-pointing mode to obtain zenith cloud profiles similar to KAZR and WACR, which serves as a calibration reference between systems.

**Siting.** There are two SACRs on a single pedestal at each deployment site; the choice of operating frequency pair (X/Ka vs Ka/W) is determined predominantly by atmospheric attenuation at the site, with Ka/W-band pairs used at SGP, NSA, and AMF1, and X/Ka-band pairs used at TWP sites and AMF2 due to higher water vapor attenuation in the tropics. Scan strategies (RHI, PPI, vertical-pointing, sector, calibration) are defined per site and alternate during operation.

**Sampling.** native rate Sampling rate: 120 MHz (receiver); averaging n_samples: Number of samples used to compute moments (variable, per ray) (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| reflectivity (equivalent reflectivity factor) | dBZ | - | - | - | (hb p. 11) |
| mean_doppler_velocity | meters per second | - | - | - | (hb p. 11) |
| spectral_width (spectrum width) | meters per second | - | - | - | (hb p. 11) |
| snr (signal-to-noise-ratio) | dB | - | - | - | (hb p. 12) |
| linear_depolarization_ratio (Linear depolarization ratio H) | dB | - | - | - | (hb p. 12) |
| reflectivity_copol | dBZ | - | 3 dBZ | - | (hb p. 24) |
| reflectivity_xpol | dBZ | - | 3 dBZ | - | (hb p. 24) |
| mean_doppler_velocity_copol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| mean_doppler_velocity_xpol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| spectral_width_copol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| spectral_width_xpol | m/s | - | 0.1 m/s | - | (hb p. 24) |


## Specifications

| parameter | value | source |
|---|---|---|
| Transmitter Type (W-band) | EIKA | (hb p. 9) |
| Center frequency (W-band) | 94.0 GHz | (hb p. 9) |
| Peak power output (W-band) | 1.7 kW | (hb p. 9) |
| Pulse width (W-band) | 50 ns–2 µs | (hb p. 9) |
| Polarization (W-band transmitter) | transmit horizontal linear | (hb p. 9) |
| Maximum duty cycle (W-band) | 1% | (hb p. 9) |
| PRF (W-band) | up to 20 kHz | (hb p. 9) |
| Manufacturer (W-band transmitter) | CPI Canada with CPI Beverly modulator | (hb p. 9) |
| Receiver Type (W-band) | dual-channel receiver | (hb p. 9) |
| Dynamic range (W-band receiver) | greater than 80 dB | (hb p. 9) |
| Noise figure (W-band receiver) | 6.0 dB | (hb p. 9) |
| Sampling rate (W-band receiver) | 120 MHz | (hb p. 9) |
| Decimation factor (W-band receiver) | adjustable | (hb p. 9) |
| Video bandwidth (W-band receiver) | adjustable | (hb p. 9) |
| Antenna Type (W-band) | Cassegrain parabolic reflector | (hb p. 10) |
| Antenna diameter (W-band) | 0.9 m | (hb p. 10) |
| 3 dB beam width (W-band) | 0.33° | (hb p. 10) |
| Gain (W-band) | 53.5 dBi | (hb p. 10) |
| Cross polarization isolation (W-band) | -27 dB | (hb p. 10) |
| 2-way radome loss (W-band) | 1.5 dB | (hb p. 10) |
| Pedestal type (W-band) | elevation over azimuth | (hb p. 10) |
| Azimuth scan rate (W-band) | up to 36°/s | (hb p. 10) |
| Elevation scan rate (W-band) | up to 20°/s | (hb p. 10) |
| range:meters_to_center_of_first_gate | 549.620 m | (hb p. 16) |
| range:meters_between_gates | 24.982 m | (hb p. 16) |


## The data

Verified example: **`anxwsacrcfrqcM1.b1`**, file `anxwsacrcfrqcM1.b1.20200529.035028.nc`
(7.79 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=681, `range`=755, `sweep`=4, `group_pulse_number`=3, `r_calib`=1, `frequency`=1 |
| Data variables | 59 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 0 s |
| File time span | 2020-05-29T03:50:28 to 2020-05-29T03:52:47 |
| dod version | wsacrcfrqc-b1-1.1 |
| process version | ingest-sacrcfrqc-1.0-0.dev1.dirty.el8 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_agl` | m | - | - | Altitude above ground level |
| `antenna_transition` | 1 | time | - | Antenna is in transition between sweeps |
| `azimuth` | degree | time | - | Azimuth angle from true north |
| `censor_mask` | 1 | time,range | - | Censor Mask |
| `clutter_mask` | 1 | time,range | - | Clutter Mask |
| `co_to_crosspol_correlation_coeff` | 1 | time,range | - | Copolar to cross-polar correlation coefficient (also known as rhoxh) |
| `crosspolar_differential_phase` | degree | time,range | - | Cross-polar propagation phase shift |
| `elevation` | degree | time | - | Elevation angle from horizontal plane |
| `fixed_angle` | degree | sweep | - | Ray target fixed angle |
| `frequency` | Hz | frequency | - | Transmit center frequency |
| `group_intra_pulse_prt` | s | group_pulse_number | - | Prt between group pulses |
| `instrument_type` | 1 | - | - | Type of instrument |
| `linear_depolarization_ratio_v` | dB | time,range | - | Linear depolarization ratio, vertical channel |
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
| `r_calib_radar_constant_v` | dB | r_calib | - | Calibrated radar constant vertical channel |


_26 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("anxwsacrcfrqcM1.b1", "2020-05-29", "2020-05-29")
ds = armlive_open("anxwsacrcfrqcM1.b1", "2020-05-29", "2020-05-29", cleanup_qc=True)
```

This datastream carries 59 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("anxwsacrcfrqcM1.b1", start, end,
                  keep_variables=["altitude_agl", "antenna_transition", "azimuth"])
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 4 sweep, 681 rays x 755 gates, `scan_type='rhi'`, fixed angle 359.9877014160156 deg.

```python
import pyart
radar = pyart.io.read("anxwsacrcfrqcM1.b1.20200529.035028.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `censor_mask`, `clutter_mask`, `co_to_crosspol_correlation_coeff`, `crosspolar_differential_phase`, `linear_depolarization_ratio_v`, `mean_doppler_velocity`, `reflectivity`, `signal_to_noise_ratio_copolar_h`, `signal_to_noise_ratio_crosspolar_v`, `spectral_width`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `censor_mask`, `clutter_mask`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("anxwsacrcfrqcM1.b1", "20110406", "20260923")
```

The handbook's own note on data quality: The qc_time variable contains bit-packed QC flags for time regularity (zero delta-time, delta-time below 0.01 s lower limit, or above 30 s upper limit), with all bits unset indicating good data and set bits given "Indeterminate" assessment. The Data Quality Office (DQO) website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting SACR data quality; plots of reflectivity, Doppler radial velocity, and spectral width serve as indicators of whether the system is operational. Instrument mentors perform routine data reviews (daily Monday-Friday) plus reviews triggered by site...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Atmospheric attenuation dependence on water vapor | Reduced signal/increased attenuation at higher-frequency bands in high water-vapor environments, affecting reflectivity accuracy; frequency pairing differs by site (X/Ka for humid tropical... | Site frequency pair selection (Ka/W at SGP/NSA/AMF1, X/Ka at TWP/AMF2) chosen based on atmospheric attenuation at each site | (hb p. 7) |
| Water vapor attenuation of radar signal | Underestimated reflectivity or biased Doppler moments in moist atmosphere, not yet corrected in released data | Planned future 'corrected moments' VAP will include water vapor attenuation correction | (hb p. 26) |
| Velocity aliasing / range ambiguity | Doppler velocity wrapping (aliasing) beyond the nyquist_velocity, or range ambiguity beyond unambiguous_range in the data | Planned future 'corrected moments' VAP will include velocity and range dealiasing | (hb p. 26) |
| No value-added products (VAPs) currently available for SACR | Only raw/moments-level data available in the archive; no dealiased, attenuation-corrected, or gridded cloud-boundary products in this data description period | Plans exist to produce a 'corrected moments' product and later a gridded moments product with cloud boundaries | (hb p. 26) |
| X-SACR dual-polarization products (ZDR, RHOHV, PHIDP, KDP) not yet included in data files | Absence of differential reflectivity, correlation coefficient, differential phase, and specific differential phase fields in the initial X-SACR data release despite simultaneous H/V... | These parameters will be included in a future release of the ingested X-SACR data file | (hb p. 24) |
| Doppler uncertainty only characterized for zenith-pointing mode | Table 2 uncertainties (e.g., 0.1 m/s for velocity/spectral width) apply only to vertical/zenith-pointing mode; scanning-mode uncertainty not yet quantified | Uncertainty for scanning mode is to be determined at each frequency band | (hb p. 24) |
| qc_time flags for irregular sample timing | qc_time bit flags set when delta time between current and previous samples is zero, less than delta_t_lower_limit (0.01 s), or greater than delta_t_upper_limit (30 s) | No bits set (zero) represents good data; flagged values are indeterminate assessment | (hb p. 10) |
| Manual azimuth selection for sector scans | Sector scan azimuth (cross-wind or along-wind) not automatically determined; incorrect or stale manual entry could misalign scan geometry relative to actual wind direction | Azimuth directions must be entered manually | (hb p. 8) |
| Antenna transition periods between sweeps | antenna_transition flag = 1 indicates ray data collected while antenna is between sweeps, which may be unreliable or should be excluded from analysis | - | (hb p. 11) |
| Dielectric factor assumption for reflectivity computation | Reflectivity values depend on an assumed dielectric factor of water at 0°C (Kw^2 = 0.70 for W-SACR); this differs by band (0.93 X-SACR, 0.88 Ka-SACR) and does not account for varying... | - | (hb p. 31) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Pointing at a fixed trihedral corner reflector of known radar cross-section at a predetermined azimuth and elevation to provide an absolute calibration point; a single corner reflector is used for Ka/W-SACR installations. (hb p. 29) |
| Traceability | Additional calibration information available in the ARM Common Calibration Database (CCDB), access limited to ARM Facility personnel; detailed calibration procedures to be listed in the forthcoming SACR Operations Manual. (hb p. 29) |
| Routine maintenance | Instrument mentors review SACR data routinely (usually daily Monday-Friday), and additionally when requested by site operations, site scientist team, ARM data translator, data user, or when notified automatically by the SACR's built-in test (BIT) email messages. Operation and maintenance details are to be listed in... (hb p. 26) |
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

Instruments the handbook names as complements or predecessors: KAZR (Ka-band ARM Zenith Radar), WACR (W-band ARM cloud radar), X-SACR, Ka-SACR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `SACR` | scanning ARM cloud radar |
| `X-SACR` | X-band scanning ARM cloud radar |
| `KA-SACR` | Ka-band scanning ARM cloud radar |
| `W-SACR` | W-band scanning ARM cloud radar |
| `KAZR` | Ka-band ARM Zenith Radar |
| `WACR` | W-band ARM cloud radar |
| `RHI` | Range Height Indicator (type of radar scan) |
| `PPI` | Plan Position Indicator (type of radar scan) |
| `ZDR` | differential reflectivity |
| `ρHV (RHOHV)` | correlation coefficient between H and V polarizations |
| `φDP (PHIDP)` | differential phase |
| `KDP` | specific differential phase |
| `EIKA` | Extended Interaction Klystron Amplifier |
| `TWTA` | Traveling Wave Tube Amplifier |


### References the handbook cites

- Bharadwaj, N, K Widener, A Koontz, and K Johnson. 'Data Specification for ARM Scanning Radars', Draft ARM Technical Report May 2010
- Bringi, VN and V Chandrasekar. 2001. 'Polarimetric Doppler Weather Radar.' Cambridge University Press.
- Doviak, RJ and DS Zrnic. 1993. 'Doppler Radar and Weather Observations.' 2nd Edition, Academic Press.
- Mead, J. 'Scanning ARM Cloud Radar (SACR) System Description and Operations Manual.' In process.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/wsacr_handbook.pdf (37 pages, DOE/SC-ARM/TR-113, by K Widener, N Bharadwaj, K Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=wsacr`, read 2026-09-23
- Example file: `anxwsacrcfrqcM1.b1.20200529.035028.nc` from `anxwsacrcfrqcM1.b1`, 7.79 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
