---
name: arm-instrument-kasacr
description: ARM Ka-Band Scanning ARM Cloud Radar (kasacr) - handbook-derived instrument reference. Measurement principle, reported quantities (Equivalent reflectivity factor, Mean Doppler velocity, Spectrum width, Signal-to-noise ratio, Linear depolarization ratio H, reflectivity_copol, reflectivity_xpol, mean_doppler_velocity_copol), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (enakasacrvpthrcC1.b1) and the variable inventory of a real file. Use when working with kasacr data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - kasacr, Ka-Band Scanning ARM Cloud Radar, enakasacrvpthrcC1.b1, Equivalent reflectivity factor, Mean Doppler velocity, Spectrum width, Signal-to-noise ratio, Linear depolarization ratio H, reflectivity_copol, Cloud Properties.
---

# KASACR - Ka-Band Scanning ARM Cloud Radar

The SACR is a polarimetric Doppler scanning cloud radar, deployed as a Ka/W-band or X/Ka-band pair on a common pedestal at ARM sites, that scans clouds in RHI, PPI, sector, vertical-pointing and calibration modes to measure reflectivity, Doppler velocity, spectral width and depolarization ratio.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 37 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `kasacr` |
| Handbook | [DOE/SC-ARM/TR-113 / K Widener, N Bharadwaj, K Johnson / June 2012](https://www.arm.gov/publications/tech_reports/handbooks/kasacr_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | ProSensing, Inc. (vendor/instrument developer); transmitters by CPI/CPI Canada; receivers by Mercury Computers; X-SACR pedestal by Orbit Industries |
| Primary measurements | Radar Doppler; Radar polarization; Radar reflectivity |
| Record | 2011-04-03 to 2026-09-23 (active) |
| Datastreams with data | 279 across 16 sites |
| Sites | anx, asi, awr, bnf, cor, ena, epc, gan, hou, mos, nsa, oli, pvc, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/kasacr |


## Credit

Everything this skill knows about the instrument is the work of **K Widener, N Bharadwaj, K Johnson** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> K Widener, N Bharadwaj, K Johnson. *Scanning ARM Cloud Radar (X/Ka/W-SACR)*, DOE/SC-ARM/TR-113, June 2012.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/kasacr_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** The same document covers `wsacr`, `xsacr` as well as
> this instrument, so much of what follows is family- or system-level rather than
> specific to `kasacr`. Where a number has to be per-instrument - a frequency, a
> detection limit, a serial number - check it against the handbook section for this
> class before using it.

## How it measures

The SACR is a polarimetric Doppler radar that transmits pulses at X-, Ka-, or W-band frequencies and measures the returned power, phase, and polarization state of backscattered signals from cloud and precipitation particles to derive equivalent reflectivity factor, mean Doppler velocity, and spectrum width. Reflectivity is computed from the meteorological radar range equation using received power, range, system losses, antenna gain, pulse width, beamwidth, transmit power, and the dielectric factor of water (Kw^2), which is frequency- and temperature-dependent. The Ka- and W-band SACRs transmit horizontal linear polarization only, while the X-SACR transmits both H and V polarizations simultaneously, enabling dual-polarization parameters such as differential reflectivity (ZDR), correlation coefficient (rhoHV), differential phase (phiDP), and specific differential phase (KDP). A narrow-beamwidth antenna on a scanning pedestal allows the radar to point at a fixed trihedral corner-reflector target of known radar cross-section to provide an absolute calibration reference. Vertical-pointing mode obtains zenith cloud profiles analogous to KAZR and WACR, providing a calibration cross-check between these instruments.

**Siting.** Two SACRs share a common pedestal at each site; frequency pair chosen based on atmospheric attenuation at the site: TWP sites use X-/Ka-band (high water vapor attenuation), SGP and NSA sites use Ka-/W-band; AMF1 has Ka/W-SACR and AMF2 has X/Ka-SACR. A fixed trihedral corner-reflector calibration target must be sited at a known azimuth/elevation near the radar; X/Ka-SACR installations require a separate corner reflector for each band.

**Sampling.** native rate Receiver sampling rate 120 MHz (all bands); reported every Varies by scan strategy (RHI, PPI, VPT, sector) per site; time recorded per ray; averaging n_samples: Number of samples used to compute moments (per ray) (hb p. 8).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Equivalent reflectivity factor | dBZ | - | - | - | (hb p. 11) |
| Mean Doppler velocity | meters per second | - | - | - | (hb p. 11) |
| Spectrum width | meters per second | - | - | - | (hb p. 11) |
| Signal-to-noise ratio | dB | - | - | - | (hb p. 11) |
| Linear depolarization ratio H | dB | - | - | - | (hb p. 11) |
| reflectivity_copol | dBZ | - | 3 dBZ | - | (hb p. 24) |
| reflectivity_xpol | dBZ | - | 3 dBZ | - | (hb p. 24) |
| mean_doppler_velocity_copol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| mean_doppler_velocity_xpol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| spectral_width_copol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| spectral_width_xpol | m/s | - | 0.1 m/s | - | (hb p. 24) |
| Differential Reflectivity (ZDR) | - | - | - | - | (hb p. 23) |
| Correlation Coefficient (rhoHV/RHOHV) | - | - | - | - | (hb p. 23) |
| Differential Phase (phiDP/PHIDP) | - | - | - | - | (hb p. 24) |
| Specific Differential Phase (KDP) | - | - | - | - | (hb p. 24) |


## Specifications

| parameter | value | source |
|---|---|---|
| X-SACR Transmitter Type | TWTA | (hb p. 7) |
| X-SACR Center frequency | 9.710 GHz | (hb p. 7) |
| X-SACR Peak power output | 20.0 kW | (hb p. 7) |
| X-SACR Pulse width | 100 ns–40 µs | (hb p. 7) |
| X-SACR Polarization | dual-polarization, simultaneous H and V | (hb p. 8) |
| X-SACR Maximum duty cycle | 1% | (hb p. 8) |
| X-SACR PRF | maximum 10 kHz | (hb p. 8) |
| X-SACR Transmitter Manufacturer | CPI | (hb p. 8) |
| X-SACR Receiver Type | dual-channel digital | (hb p. 8) |
| X-SACR Receiver Dynamic range | greater than  80 dB | (hb p. 8) |
| X-SACR Receiver Noise figure | 4.5 dB | (hb p. 8) |
| X-SACR Receiver Sampling rate | 120 MHz | (hb p. 8) |
| X-SACR Receiver Manufacturer | Mercury Computers | (hb p. 8) |
| X-SACR Antenna Diameter | 1.82 m | (hb p. 8) |
| X-SACR 3 dB beam width | 1.40° | (hb p. 8) |
| X-SACR Antenna Gain | 42.0 dBi | (hb p. 8) |
| X-SACR Cross polarization isolation | -30 dB | (hb p. 8) |
| X-SACR 2-way radome loss | less than 0.2 dB | (hb p. 8) |
| X-SACR Pedestal Type | azimuth over elevation | (hb p. 8) |
| X-SACR Azimuth scan rate | up to 36°/s | (hb p. 8) |
| X-SACR Elevation scan rate | up to 20°/s | (hb p. 8) |
| X-SACR Pedestal manufacturer | Orbit Industries | (hb p. 8) |
| Ka-SACR Transmitter Type | EIKA | (hb p. 8) |
| Ka-SACR Center frequency | 35.3 GHZ | (hb p. 8) |
| Ka-SACR Peak power output | 2.0 kW | (hb p. 8) |
| Ka-SACR Pulse width | 50 ns–13 µs | (hb p. 8) |


_44 further specification rows are in the handbook._

## The data

Verified example: **`enakasacrvpthrcC1.b1`**, file `enakasacrvpthrcC1.b1.20170728.223026.nc`
(9.99 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=223, `range`=480, `sweep`=1, `group_pulse_number`=5, `r_calib`=1, `frequency`=1 |
| Data variables | 73 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2017-07-28T22:30:26 to 2017-07-28T22:45:17 |
| dod version | kasacrvpthrc-a1-3.6 |
| process version | ingest-sacr3-1.10-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `altitude_agl` | meters | - | - | altitude_above_ground_level |
| `antenna_transition` | unitless | time | - | antenna_is_in_transition_between_sweeps |
| `azimuth` | degrees | time | - | azimuth_angle_from_true_north |
| `co_to_crosspol_correlation_coeff_h` | unitless | time,range | - | Copol to cross-polar correlation coefficient (also known as rhoxh) |
| `co_to_crosspol_correlation_coeff_v` | unitless | time,range | - | Copol to cross-polar correlation coefficient (also known as rhoxv) |
| `copol_correlation_coeff` | unitless | time,range | - | Copolar correlation coefficient (also known as rhohv) |
| `cross_polar_differential_phase_h` | degrees | time,range | - | Cross-polar propagation phase shift |
| `cross_polar_differential_phase_v` | degrees | time,range | - | Cross-polar propagation phase shift |
| `differential_phase` | degrees | time,range | - | Differential propagation phase shift |
| `differential_reflectivity` | dB | time,range | - | Differential reflectivity |
| `elevation` | degrees | time | - | elevation_angle_from_horizontal_plane |
| `fixed_angle` | degrees | sweep | - | ray_target_fixed_angle |
| `frequency` | s-1 | frequency | - | radiation_frequency |
| `group_intra_pulse_prt` | seconds | group_pulse_number | - | Prt between group pulses |
| `instrument_type` | unitless | - | - | type_of_instrument |
| `linear_depolarization_ratio_h` | dB | time,range | - | Linear depolarization ratio, horizontal channel |
| `linear_depolarization_ratio_v` | dB | time,range | - | Linear depolarization ratio, vertical channel |
| `mask_blanking_copolar_variables` | unitless | time,range | - | transmitter blanking mask |
| `mask_blockage_copolar_variables` | unitless | time,range | - | beam blockage mask |
| `mask_clutter_copolar_variables` | unitless | time,range | - | ground clutter mask |
| `mask_copolar_variables` | unitless | time,range | - | significant polarimeric variable mask |
| `mask_significant_echo` | unitless | time,range | - | significant echo detections mask |
| `mean_doppler_velocity` | m s-1 | time,range | - | Radial mean Doppler velocity, positive for motion away from the... |
| `nyquist_velocity` | meters per second | time | - | unambiguous_doppler_velocity |
| `platform_type` | unitless | - | - | platform_type |
| `polarization_mode` | unitless | sweep | - | polarization_mode_for_sweep |
| `prt` | seconds | time | - | pulse_repetition_frequency |
| `prt_mode` | unitless | sweep | - | transmit_pulse_mode |
| `pulse_width` | seconds | time | - | transmitter_pulse_width |
| `r_calib_dielectric_constant` | unitless | r_calib | - | calibrated_radar_dielectric_constant_in_use |


_40 more variables; the full inventory is in `example_inventory.json` beside this file._

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("enakasacrvpthrcC1.b1", "2017-07-28", "2017-07-28")
ds = armlive_open("enakasacrvpthrcC1.b1", "2017-07-28", "2017-07-28", cleanup_qc=True)
```

This datastream carries 73 variables. On any window longer than a day,
read only what you need - and ask for the QC companion at the same time:

```python
ds = armlive_open("enakasacrvpthrcC1.b1", start, end,
                  keep_variables=["altitude_agl", "antenna_transition", "azimuth"])
```

### Reading it as a radar object

This datastream is CfRadial, so Py-ART reads it directly - verified 1 sweep, 223 rays x 480 gates, `scan_type='vpt'`, fixed angle 89.99333953857422 deg.

```python
import pyart
radar = pyart.io.read("enakasacrvpthrcC1.b1.20170728.223026.nc")        # or pyart.aux_io.read_kazr
print(sorted(radar.fields))
```

Fields present in the verified file: `co_to_crosspol_correlation_coeff_h`, `co_to_crosspol_correlation_coeff_v`, `copol_correlation_coeff`, `cross_polar_differential_phase_h`, `cross_polar_differential_phase_v`, `differential_phase`, `differential_reflectivity`, `linear_depolarization_ratio_h`, `linear_depolarization_ratio_v`, `mask_blanking_copolar_variables`, `mask_blockage_copolar_variables`, `mask_clutter_copolar_variables`, `mask_copolar_variables`, `mask_significant_echo`, `mean_doppler_velocity`, `reflectivity`, `signal_to_noise_ratio_co_polar_h`, `signal_to_noise_ratio_co_polar_v`, `signal_to_noise_ratio_cross_polar_h`, `signal_to_noise_ratio_cross_polar_v`, `spectral_width`, `uncorrected_mean_doppler_velocity_h`, `uncorrected_mean_doppler_velocity_v`, `unthresholded_power_co_polar_h`, `unthresholded_power_co_polar_v`, `unthresholded_power_cross_polar_h`, `unthresholded_power_cross_polar_v`.

For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load
`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing
profilers have one sweep and no split cuts, so the scan-strategy machinery in those
skills is mostly inapplicable - the time-height view is the useful one.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `mask_significant_echo`, `mask_copolar_variables`, `mask_blanking_copolar_variables`, `mask_clutter_copolar_variables`, `mask_blockage_copolar_variables`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("enakasacrvpthrcC1.b1", "20110403", "20260923")
```

The handbook's own note on data quality: Data Quality Office (DQO) website provides DQ Explorer, DQ Plot Browser, and NCVweb tools for inspecting SACR data quality. Plots of reflectivity, Doppler radial velocity, and Doppler spectral width are used as indicators of whether the system is operational. Instrument mentors perform routine review (usually daily Mon-Fri) plus ad hoc reviews triggered by site operations, site scientist team, ARM data translator, data user requests, or automatic built-in-test (BIT) email notifications. Data files include a bit-packed qc_time field flagging anomalous sample timing (zero delta, below 0.01 s...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Uncertainty for scanning-mode Doppler variables not yet determined | Table 2 uncertainties (0.1 m/s for velocity/spectral width, 3 dBZ for reflectivity) apply only to zenith-pointing mode; scanning-mode uncertainty is undefined, so users cannot assume the... | To be determined at each frequency band per handbook | (hb p. 24) |
| X-SACR dual-pol products not yet in data files | ZDR, RHOHV, PHIDP, KDP are described conceptually but are not present in the initial released X-SACR data files; only the same fields as Ka/W-SACR are provided | Handbook states these will be included in a future release of the ingested X-SACR data file | (hb p. 23) |
| No value-added products (VAPs) currently available for SACR | Raw/moments data only; no dealiased or attenuation-corrected products, no gridded cloud-boundary product in the archive at time of writing | Plans exist to produce a 'corrected moments' product (velocity/range dealiasing, water-vapor attenuation correction) and later a gridded moments... | (hb p. 26) |
| Water-vapor attenuation not corrected in current data | Reflectivity/SNR may show frequency-dependent attenuation bias (especially Ka/W-band) that is not corrected in the moments data | Planned correction in future 'corrected moments' VAP | (hb p. 26) |
| Velocity/range aliasing not corrected | Mean Doppler velocity may show folding/wrap-around near the Nyquist velocity, and range may show ambiguity beyond the unambiguous range, uncorrected in current files | Planned dealiasing in future 'corrected moments' VAP | (hb p. 26) |
| Dielectric factor (Kw^2) is temperature- and frequency-dependent | Reflectivity values (dBZ) depend on an assumed Kw^2 (0.93 X-band, 0.88 Ka-band, 0.70 W-band at 0°C); if actual hydrometeor temperature/phase differs from 0°C liquid water assumption,... | Handbook notes the dielectric factor of water at 0°C is used for computing equivalent reflectivity factor; see Figure 11 for the... | (hb p. 31) |
| Differing antenna beamwidths and radome losses across bands | X-SACR has broader 1.40° beamwidth vs 0.33° for Ka/W-SACR, and near-zero (less than 0.2 dB) radome loss vs 1.5 dB for Ka/W-SACR, affecting spatial resolution and sensitivity comparisons... | None stated; noted only as a specification difference | (hb p. 8) |
| Manual sector-scan azimuth selection | Cross-wind/along-wind sector scan azimuths are not automatically computed; incorrect or stale manual entry could misalign scan with intended wind-relative geometry | Azimuth directions must be entered manually per handbook | (hb p. 8) |
| Antenna transition periods between sweeps | antenna_transition flag =1 indicates data collected while antenna is between sweeps (in transition), which may be less reliable/should be treated differently than in-sweep data | Field is provided so users can identify/exclude transition-period rays | (hb p. 11) |
| qc_time bit-packed flags indicate timing anomalies | qc_time bits set (nonzero) flag delta-time between samples that is zero, below the lower limit (0.01 s), or above the upper limit (30 s), indicating potential timing irregularities in the... | All bits documented as 'Indeterminate' assessment; no explicit corrective action stated beyond flagging | (hb p. 10) |
| X-SACR dual-polarization data file fields not finalized | Initial release X-SACR files contain essentially the same fields as Ka/W-SACR (no distinct copol/xpol dual-pol variables), which could mislead a user expecting ZDR/PHIDP/KDP fields | Future release planned to include full dual-pol parameters | (hb p. 24) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Radar points at a predetermined fixed azimuth and elevation to view a trihedral corner reflector of known radar cross-section, providing an absolute calibration point; vertical-pointing mode also used as a calibration reference against KAZR/WACR. (hb p. 29) |
| Calibration interval | Not specified (calibration information to be listed in forthcoming SACR Operations Manual) (hb p. 29) |
| Traceability | ARM Common Calibration Database (CCDB); access limited to ARM Facility personnel (hb p. 29) |
| Routine maintenance | Instrument mentors perform routine review of data for nominal operation, and the SACR has a built-in test (BIT) that sends automatic email notifications on issues (hb p. 26) |
| Maintenance interval | Routine review usually daily Monday–Friday (hb p. 26) |


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

Instruments the handbook names as complements or predecessors: KAZR (Ka-band ARM Zenith Radar), WACR (W-band ARM cloud radar), X-SACR, W-SACR.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AGL` | above ground level |
| `ARM` | Atmospheric Radiation Measurement (Climate Research Facility) |
| `C band` | frequencies between 4 GHz and 8 GHz |
| `dB` | decibel |
| `dBi` | antenna gain referenced to isotropic radiator |
| `dBm` | decibel referenced to 1 mW |
| `dBZ` | reflectivity |
| `DMF` | Data Management Facility |
| `DQO` | Data Quality Office (ARM) |
| `EIKA` | Extended Interaction Klystron Amplifier |
| `GHz` | gigahertz (10^9 Hz) |
| `Hz` | hertz |
| `Ka band` | frequencies between 26.5 GHz and 40 GHz |
| `KA-SACR` | Ka-band scanning ARM cloud radar |


### References the handbook cites

- Bharadwaj, N, K Widener, A Koontz, and K Johnson. "Data Specification for ARM Scanning Radars", Draft ARM Technical Report May 2010
- Bringi, VN and V Chandrasekar. 2001. "Polarimetric Doppler Weather Radar." Cambridge University Press.
- Doviak, RJ and DS Zrnic. 1993. "Doppler Radar and Weather Observations." 2nd Edition, Academic Press.
- Mead, J. "Scanning ARM Cloud Radar (SACR) System Description and Operations Manual." In process.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/kasacr_handbook.pdf (37 pages, DOE/SC-ARM/TR-113, by K Widener, N Bharadwaj, K Johnson)
- Catalog record: ARM data-source index, `instrument_class_code=kasacr`, read 2026-09-23
- Example file: `enakasacrvpthrcC1.b1.20170728.223026.nc` from `enakasacrvpthrcC1.b1`, 9.99 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
