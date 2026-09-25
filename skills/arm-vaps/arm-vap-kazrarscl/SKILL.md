---
name: arm-vap-kazrarscl
description: ARM Active Remote Sensing of CLouds (ARSCL) product using Ka-band ARM Zenith Radars (kazrarscl) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Radar reflectivity, ReflectivityNoClutter, ReflectivityBestEstimate, MeanDopplerVelocity, SpectralWidth, SignaltoNoiseRatio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparsclkazrbnd1kolliasC1.c1) and the variable inventory of a real file. Use when working with kazrarscl data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - kazrarscl, sgparsclkazrbnd1kolliasC1.c1, Radar reflectivity, ReflectivityNoClutter, ReflectivityBestEstimate, MeanDopplerVelocity, SpectralWidth, Cloud Properties.
---

# KAZRARSCL - Active Remote Sensing of CLouds (ARSCL) product using Ka-band ARM Zenith Radars

ARSCL is an ARM value-added product that combines vertically-pointing 35-GHz Millimeter Wave Cloud Radar (MMCR) reflectivity, Doppler velocity, and spectral width data with laser ceilometer and Micropulse Lidar (MPL) cloud-base-height estimates to produce continuous time-height best-estimate maps of cloud hydrometeor location and radar moments above fixed ARM ground sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 56 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `kazrarscl` |
| Product type | value-added product (VAP) |
| Technical report | [DOE Tech. Memo. ARM VAP-002.1 / Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold / March 4, 2001](https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-01-18 to 2026-06-30 (retired) |
| Datastreams with data | 60 across 18 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/kazrarscl |


## Credit

Everything this skill knows about the retrieval is the work of **Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold** -
the ARM developers and mentors who wrote the technical report it derives from:

> Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold. *The ARM Millimeter Wave Cloud Radars (MMCRs) and the Active Remote Sensing of Clouds (ARSCL) Value Added Product (VAP)*, DOE Tech. Memo. ARM VAP-002.1, March 4, 2001.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** the linked report, ARM VAP-002.1 (2001), is the MMCR-era ARSCL document shared with `arm-vap-arscl`; it predates the KAZR implementation this class serves, so treat its algorithm detail as the lineage rather than the current processor.

## How it is produced

The MMCR transmits pulses of electromagnetic energy at 34.86 GHz vertically into the atmosphere and receives backscattered energy as in-phase (I) and quadrature (Q) voltage time series for each range gate; a complex FFT of I and Q produces a power density spectrum (Doppler spectrum) of backscatter cross section versus vertical particle velocity, from which the moments reflectivity (0th), mean Doppler velocity (1st), and spectral width (2nd) are derived. The ARSCL VAP applies a "Cloud Mask Code" algorithm to MMCR power returns on a mode-by-mode basis to identify significant returns, merges data from four operational MMCR modes (differing in sensitivity, range resolution, and velocity ambiguity) into a best-estimate reflectivity field, and uses ceilometer and MPL cloud-base-height retrievals (which are less susceptible to insect/clutter contamination) to filter clutter from the merged radar hydrometeor field. The final merged products represent the best-estimate vertical distribution of hydrometeors combining active radar and lidar/ceilometer detections.

**Cadence.** input rate radar samples every pulse; radar task collects data every half hour and FTPs to data management computer; output every 9 s temporal resolution per mode (current); arscl1cloth merged product on 10 s time grid; averaging coherent integration (Ncoh) and incoherent/spectral averaging (Nspec) per mode; moments (reflectivity, mean velocity, spectral width) acquired over spectra spanning about 10 s (hb p. 15).

## Inputs

The report names these instruments and sibling products: Belfort laser ceilometer, Vaisala laser ceilometer, Micropulse Lidar (MPL), Microwave Radiometer (MWR), surface meteorology station (smetstd) / optical rain gauge.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Radar reflectivity (Reflectivity, 0th Moment) | dBZe | -50 to +20 dBZ (combined mode... | good to at least 1 dB | (hb p. 21) |
| ReflectivityNoClutter | dBZe | - | - | (hb p. 21) |
| ReflectivityBestEstimate | dBZe | - | - | (hb p. 21) |
| MeanDopplerVelocity (1st Moment) | m s-1 | - | - | (hb p. 21) |
| SpectralWidth (2nd Moment, Doppler width) | m s-1 | - | - | (hb p. 21) |
| SignaltoNoiseRatio | dB | - | - | (hb p. 22) |
| CloudBaseBestEstimate (cloud base height) | m | - | - | (hb p. 23) |
| CloudLayerBottomHeight / CloudLayerTopHeight (MplCamp,... | m | - | - | (hb p. 23) |
| ModeId | unitless flag (1-4) | 1 to 4 | - | (hb p. 22) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Radar operating frequency | 34.86 GHz | (hb p. 7) |
| Radar wavelength | approximately 8.6 mm | (hb p. 13) |
| Peak transmitter (TWTA) RF power | 100 W, max duty cycle 25% | (hb p. 10) |
| SGP antenna diameter | 10-foot diameter | (hb p. 11) |
| SGP antenna gain | 57.2 dB | (hb p. 11) |
| SGP antenna beam width | 0.19° | (hb p. 11) |
| NSA/TWP antenna diameter | 6-foot diameter | (hb p. 11) |
| NSA/TWP antenna gain | about 53.4 dB | (hb p. 11) |
| NSA/TWP antenna beam width | 0.29° | (hb p. 11) |
| First sidelobe levels | typically better than 18 dB | (hb p. 11) |
| SGP beam width (Section 1 reference) | 0.2-degree beam width | (hb p. 8) |
| Sample volume length (SGP) | typically 45 m or 90 m | (hb p. 8) |
| Range resolution/spacing, SGP Modes 4,3,2 | 90 m | (hb p. 21) |
| Range resolution/spacing, SGP Mode 1 (boundary layer... | 45 m | (hb p. 21) |
| Minimum usable range, SGP Modes 4 and 3 | 105 m | (hb p. 21) |
| Minimum usable range, SGP Mode 2 | 2985 m | (hb p. 21) |
| Minimum usable range, SGP Mode 1 | 465 m | (hb p. 21) |
| Maximum range, SGP Modes 4, 3, 2 | 15.045 km | (hb p. 22) |
| Maximum range, SGP Mode 1 | 5.010 km | (hb p. 22) |
| Temporal resolution (current, all modes) | 9 s | (hb p. 22) |
| Unambiguous velocity, SGP Mode 4 | ±20.28 m s-1 | (hb p. 22) |
| Unambiguous velocity, SGP Mode 3 | ±3.38 m s-1 | (hb p. 22) |
| arscl1cloth merged product grid | 10 s time grid, 45 m height grid | (hb p. 26) |
| MMCR full dynamic range requirement | -50 to +20 dBZ (70 dB dynamic range) | (hb p. 15) |
| UPS power output | up to 12 amps of 12-volt AC power at 60 Hz for 20 minutes | (hb p. 4) |
| LNA gain | 33 dB | (hb p. 11) |


_4 further rows in the report._

## The data

Verified example: **`sgparsclkazrbnd1kolliasC1.c1`**, file `sgparsclkazrbnd1kolliasC1.c1.20140312.000000.nc`
(2.34 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=21600, `layer`=10 |
| Data variables | 10 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2014-03-12T00:00:00 to 2014-03-12T23:59:56 |
| dod version | arsclkazrbnd1kollias-c1-1.2 |
| process version | vap-kazrarscl-0.5-0.el6 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `cloud_base_best_estimate` | m | time | - | Cloud base best estimate, based on ceilometer and micropulse lidar |
| `cloud_layer_base_height` | m | time,layer | - | Base height of hydrometeor layers for up to 10 layers, based on... |
| `cloud_layer_top_height` | m | time,layer | - | Top height of hydrometeor layers for up to 10 layers, based on... |
| `instrument_availability_flag` | unitless | time | - | Flag indicating which instruments have data available |
| `layer` | unitless | layer | - | Cloud layer number |
| `radar_first_top` | m | time | - | KAZR top height of lowest significant detection layer, before clutter... |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "sgparsclkazrbnd1kolliasC1.c1",
                             "start": "2014-03-12", "end": "2014-03-12", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgparsclkazrbnd1kolliasC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgparsclkazrbnd1kolliasC1.c1", "2014-03-12", "2014-03-12")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgparsclkazrbnd1kolliasC1.c1", "2014-03-12", "2014-03-12"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cloud_base_best_estimate")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `instrument_availability_flag`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgparsclkazrbnd1kolliasC1.c1", "20110118", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: The most useful QC flag in arscl1cloth is qc_ReflectivityClutterFlag, used together with Reflectivity, ReflectivityNoClutter, and ReflectivityBestEstimate to sort data: value 10 means no data exist; if flag != 10 and reflectivity (after dividing file value by 100) is less than -100 or greater than 30, data exist but no significant detection (no cloud); otherwise data exist, there is a significant detection, and the flag value indicates the likely source of the power return (0=no detection, 1=hydrometeor only, 2=hydrometeor+insects mixed/uncertain cloud top, 3=all clutter/insects,...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Range sidelobe leakage from pulse coding | Contaminated/inaccurate reflectivity estimates within the first Nbits-1 range gates near strong reflectivity gradients or large Doppler velocities; elevated minimum usable range (e.g., 2985... | Data in these near-range regions flagged; higher minimum usable range values enforced for pulse-coded modes | (hb p. 15) |
| Velocity aliasing (velocity folding) from coherent integration | Particle contributions to power density spectrum appear at incorrect (folded) velocity when true Doppler velocity exceeds unambiguous velocity Vu; reflectivities/velocities from that mode... | Use SGP Mode 4 (Vu=±20.28 m/s, no coherent averaging) to identify and validate/replace problem data from lower-Vu modes | (hb p. 13) |
| Spectral weighting from coherent integration near unambiguous velocity ends | Steep roll-off (3.9 dB / 60% loss) at spectral ends near Vu, shifting estimated mean velocity toward smaller values and biasing reflectivity low when hydrometeor velocities are near Vu with... | Reduce number of coherent integrations (Ncoh) to increase Vu, or set Ncoh=1 to remove weighting entirely (at cost of more noise/reduced sensitivity) | (hb p. 13) |
| Range aliasing (second trip echoes) | Backscattered power from a distant cloud beyond the unambiguous range Ru arrives superimposed on I/Q voltages from a pulse originating from a closer cloud, contaminating apparent returns at... | Ensure interpulse period (tau_ipp) sufficiently large so radar does not transmit before backscattered energy from previous pulse returns | (hb p. 14) |
| Receiver noise limiting minimum detectable signal | As cloud reflectivity decreases, receiver noise contribution to I and Q voltages eventually makes atmospheric signal undetectable; noise floor visible as variability/standard deviation in... | Use coherent/incoherent averaging (Ncoh, Nspec) and pulse coding to enhance sensitivity, at cost of resolution/velocity range trade-offs | (hb p. 12) |
| Insect/biological clutter contamination of radar returns | Significant power returns below about 4 km not attributable to hydrometeors, visible as spurious reflectivity in clear-sky or near-surface layers, especially evident in Mode 4 results below... | Use ceilometer and MPL cloud-base-height data (which do not detect these airborne particles) combined with Clutter Profile Code / Remove Clutter Code... | (hb p. 15) |
| Radar beam attenuation/failure during heavy precipitation | Laser-based cloud base height retrievals fail during periods of heavier precipitation; radar reflectivity may be affected by attenuation of 35-GHz beam during heavy rain | Use MWR wet-window flag (mwrloslilj) or precipitation rate from surface meteorology station (smetstd) to identify precipitation periods; if all laser... | (hb p. 24) |
| Lidar/laser beam complete attenuation or blockage | MPL/ceilometer signal shows no cloud detected beyond attenuation point; qc_BeamAttenuationMplCamp flag values indicate missing data (-9), blocked beam (-2), attenuated beam (-1), no cloud... | qc_BeamAttenuationMplCamp/Cloth variables flag attenuation state; use combined active sensor suite to compensate for lidar-only blind spots | (hb p. 24) |
| Radar artifacts in individual MMCR operational modes (pre-October 1999 mode set) | qc_RadarArtifacts flag set when artifacts from an individual mode enter merged reflectivity field; more common in data collected before mid-October 1999 when original mode set was in use | Flagged via qc_RadarArtifacts; current mode configuration (post mid-Oct 1999) should not exhibit this problem | (hb p. 24) |
| MMCR near-field reflectivity correction error | Reflectivities below about 1 km are off by about 2 to 3 dB near the surface, dropping to a few tenths of a dB error by about 1 km above the radar | Correction factor being developed (as of March 2001) to be incorporated when MMCR data are next reprocessed | (hb p. 40) |
| SGP Belfort laser ceilometer height offset | From start of record until 3 February 2000, Belfort ceilometer heights read 122 m too high, affecting CloudBaseCeilometerStd and related fields | Offset removed from raw data starting 4 February 2000; historical data to be corrected upon reprocessing of BLC raw data files and ARSCL VAP products | (hb p. 41) |
| NSA Micropulse Lidar height offset | Starting 16 June 1999 when NSA MPL was reactivated, backscatter profile heights were 30 m too high, persisting until an unspecified removal date | Raw MPL data and ARSCL VAP data for the affected period will need to be reprocessed | (hb p. 41) |
| CloudBaseCeilometerCloth algorithm not yet implemented | Variable present in datastream schema but not populated with real cloud detection algorithm output for Belfort/Vaisala backscatter profiles | Noted as future work; algorithm 'has not yet been implemented' | (hb p. 22) |
| Radar cannot conclusively identify clear-sky (absence of hydrometeors) | Small/distant cloud drops (e.g., 4 µm radius drops far from radar) may be present but undetected; radar can identify presence of hydrometeors but not conclusively rule out their absence | None stated beyond combining with lidar/passive measurements for estimating boundaries | (hb p. 2) |
| Uncertain cloud top height when clutter flag = 2 (hydrometeors + insects both present) | qc_ReflectivityClutterFlag value of 2 in arscl1cloth/mmcrmode datastreams indicates region where both hydrometeors and insects may contribute; top of flagged region may not equal true cloud... | Use qc_ReflectivityClutterFlag together with Reflectivity/ReflectivityNoClutter/ReflectivityBestEstimate to interpret; flagged as uncertain rather... | (hb p. 24) |
| CloudLayerBottom/TopHeight (MplCamp/MplCloth) variables flagged as immature/unreliable | Handbook repeatedly cautions 'More work may need to be done here, so be very careful with this variable' for these layer boundary fields | None beyond caution to the user; qc_CloudLayerTopHeightMplCamp/Cloth flags provided but require manual MPL data analysis since radar alone cannot... | (hb p. 23) |
| arscl1cloth interpolation to fixed 10 s/45 m grid may not be meaningful for time series... | Data from four MMCR modes with different native temporal/spatial resolutions interpolated onto common grid; handbook states 'We are not sure if the data contained in this datastream are... | Laser-derived cloud base heights deliberately NOT interpolated to this grid since such interpolation would be meaningless; use mmcrmode__v___... | (hb p. 20) |
| Radar signal processor cannot process all generated data (low processing efficiency) | Radar signal processor efficiency ranges from only 4% to 31% for SGP Modes 4 through 1, meaning most raw radar-generated data are discarded / not processed | Planned processor upgrade would allow full processing at ~0.45 s resolution without sensitivity loss | (hb p. 42) |
| Power density spectra saved only at selected times | Full Doppler spectra (Figure 4e-type data) not archived continuously due to large memory requirements; only the first three moments (reflectivity, mean velocity, spectral width) saved at... | Radar can be reconfigured remotely to save spectra during interesting cloud events | (hb p. 42) |
| Attenuation of 35-GHz beam during heavy rain | Combining four modes gives accurate cloud coverage description except during periods when insects present and during rain when 35-GHz beam attenuation becomes significant | None stated beyond noting the limitation | (hb p. 42) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Moran et al. (1998)
- Clothiaux et al. (1999)
- Clothiaux et al. (2000)
- Clothiaux et al. (1998)
- Clothiaux et al. (1995)
- Campbell et al. (1998)
- Scott and Spinhirne
- Frisch et al. (1995)
- Fox and Illingworth (1997)
- Noonkester (1984)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf (56 pages, DOE Tech. Memo. ARM VAP-002.1, by Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold)
- Catalog record: ARM data-source index, `instrument_class_code=kazrarscl`, read 2026-09-24
- Example file: `sgparsclkazrbnd1kolliasC1.c1.20140312.000000.nc` from `sgparsclkazrbnd1kolliasC1.c1`, 2.34 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
