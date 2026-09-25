---
name: arm-vap-arscl
description: ARM Active Remote Sensing of CLouds (arscl) - value-added product reference from its technical report. Derived from mmcr, mpl. The retrieval algorithm, reported quantities (Reflectivity, ReflectivityNoClutter, ReflectivityBestEstimate, MeanDopplerVelocity, SpectralWidth, SignaltoNoiseRatio), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgparsclcbh1clothC1.c1) and the variable inventory of a real file. Use when working with arscl data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - arscl, Active Remote Sensing of CLouds, sgparsclcbh1clothC1.c1, mmcr VAP, mpl VAP, Reflectivity, ReflectivityNoClutter, ReflectivityBestEstimate, MeanDopplerVelocity, SpectralWidth, Cloud Properties.
---

# ARSCL - Active Remote Sensing of CLouds

ARSCL is an ARM value-added product that combines vertically pointing 35-GHz Millimeter Wave Cloud Radar (MMCR) Doppler moments with laser ceilometer, micropulse lidar (MPL), and microwave radiometer (MWR) data to produce best-estimate time-height maps of hydrometeor reflectivity, Doppler velocity, spectral width, and cloud boundary heights above fixed ARM ground sites.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 56 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `arscl` |
| Product type | value-added product (VAP) |
| Technical report | [Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold / March 2001](https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf) |
| Category | Cloud Properties |
| Input instruments | `mmcr`, `mpl` |
| Record | 1996-11-07 to 2011-03-23 (retired) |
| Datastreams with data | 27 across 3 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/arscl |


## Credit

Everything this skill knows about the retrieval is the work of **Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold** -
the ARM developers and mentors who wrote the technical report it derives from:

> Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold. *The ARM Millimeter Wave Cloud Radars (MMCRs) and the Active Remote Sensing of Clouds (ARSCL) Value Added Product (VAP)*, March 2001.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** ARM VAP-002.1 (2001) is the MMCR-era ARSCL report, so it describes no KAZR-era behaviour; for the KAZR implementation see `arm-vap-kazrarscl`, which shares this document.

## How it is produced

The MMCR transmits pulses of 34.86-GHz electromagnetic energy vertically and records the backscattered in-phase (I) and quadrature (Q) voltage time series for each range gate; a complex FFT applied to I/Q produces a Doppler power density spectrum whose moments give radar reflectivity (0th moment), mean Doppler velocity (1st moment), and spectral width (2nd moment). Because no single set of radar operating parameters can cover the full -50 to +20 dBZ reflectivity range of atmospheric hydrometeors, the MMCR cycles through four operational modes (robust, general, cirrus, boundary-layer stratus) with different pulse coding, coherent/incoherent averaging, and range/velocity resolution trade-offs; ARSCL merges the mode data using a Cloud Mask Code and Merge Modes Code algorithm to build a single best-estimate hydrometeor field. Because many significant radar returns are due to non-hydrometeor clutter (insects, biological particles), ARSCL uses collocated laser ceilometer and micropulse lidar cloud-mask/cloud-base-height retrievals (Clothiaux et al. 1998; Campbell et al. 1998; Scott and Spinhirne algorithms) to identify and filter clutter from the merged radar field via a Clutter Profile Code and Remove Clutter Code. During heavy precipitation, when laser retrievals fail, an MWR wet-window flag or optical rain-gauge precipitation indicator is used to flag surface precipitation periods, and cloud base height is set to 0 m if all laser systems fail during such an event.

**Cadence.** input rate MMCR pulses at interpulse period tau_ipp with mode-dependent coherent/incoherent averaging; spectra acquired over about 10 s per mode; output every arscl1cloth merged product on 10 s time grid, 45 m height grid; current MMCR temporal resolution ~9 s per mode; averaging Coherent integration (time-domain averaging of I/Q, Ncoh) and incoherent integration (averaging of Nspec consecutive power spectra) used to reduce noise, mode-dependent (hb p. 20).

## Inputs

ARM's catalog declares these input instrument classes: `mmcr`, `mpl`.

The report names these instruments and sibling products: Micropulse Lidar (MPL), Belfort laser ceilometer, Vaisala laser ceilometer, Microwave Radiometer (MWR), Surface meteorology station (smetstd) optical rain gauge, MMCR (millimeter wave cloud radar), micropulse lidar, ceilometer.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Reflectivity | dBZe | - | - | (hb p. 27) |
| ReflectivityNoClutter | dBZe | - | - | (hb p. 27) |
| ReflectivityBestEstimate | dBZe | - | - | (hb p. 27) |
| MeanDopplerVelocity (1st Moment) | m s-1 | - | - | (hb p. 27) |
| SpectralWidth (2nd Moment) | m s-1 | - | - | (hb p. 27) |
| SignaltoNoiseRatio | dB | - | - | (hb p. 28) |
| RadarFirstTop | m | - | - | (hb p. 28) |
| ModeId | - | 1-4 | - | (hb p. 28) |
| CloudBaseBestEstimate | m | - | - | (hb p. 28) |
| CloudBaseCeilometerStd | m | - | - | (hb p. 28) |
| CloudBaseMplScott | m | - | - | (hb p. 28) |
| CloudBaseMplCamp | m | - | - | (hb p. 29) |
| CloudBaseMplCloth | m | - | - | (hb p. 29) |
| CloudLayerBottomHeightMplCamp/Cloth | m | - | - | (hb p. 29) |
| CloudLayerTopHeightMplCamp/Cloth | m | - | - | (hb p. 29) |
| CloudMaskMplCamp / CloudMaskMplCloth | - | - | - | (hb p. 29) |
| Radar reflectivity Z (theoretical definition) | mm6 m-3 (dBZ) | -50 to +20 dBZ (full hydrometeor... | - | (hb p. 7) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| MMCR operating frequency | 34.86 GHz | (hb p. 7) |
| Radar wavelength | approximately 8.6 mm | (hb p. 7) |
| Required detectable reflectivity range | -50 to +20 dBZ (70 dB dynamic range) | (hb p. 8) |
| SGP antenna diameter/gain/beamwidth | 10-foot diameter, 57.2 dB gain, 0.19 degree beamwidth | (hb p. 11) |
| NSA/TWP antenna diameter/gain/beamwidth | 6-foot diameter, ~53.4 dB gain, 0.29 degree beamwidth | (hb p. 11) |
| First sidelobe levels | typically better than 18 dB | (hb p. 11) |
| SGP sample volume beamwidth (SGP note) | 0.2-degree beam width; sample volume at 5 km approx. cylinder 17.5 m diameter, height 45 m or 90 m | (hb p. 8) |
| TWTA peak RF power | 100 W | (hb p. 10) |
| TWTA maximum duty cycle | 25% (for long pulse width phase-coded waveforms) | (hb p. 10) |
| Range resolution/spacing, Modes 4,3,2 (SGP) | 90 m | (hb p. 21) |
| Range resolution/spacing, Mode 1 (SGP, boundary layer... | 45 m | (hb p. 21) |
| Minimum usable range Rmin, SGP Modes 4 and 3 | 105 m | (hb p. 21) |
| Minimum usable range Rmin, SGP Mode 2 | 2985 m | (hb p. 21) |
| Minimum usable range Rmin, SGP Mode 1 | 465 m | (hb p. 21) |
| Maximum range Rmax, SGP Modes 4,3,2 | 15.045 km | (hb p. 22) |
| Maximum range Rmax, SGP Mode 1 | 5.010 km | (hb p. 22) |
| Temporal resolution Ts of MMCR data (current) | 9 s | (hb p. 22) |
| Unambiguous velocity Vu, SGP Mode 4 | +/- 20.28 m s-1 | (hb p. 22) |
| Unambiguous velocity Vu, SGP Mode 3 | +/- 3.38 m s-1 | (hb p. 22) |
| Coherent averages Ncoh, SGP Mode 4 | 1 (no coherent averaging) | (hb p. 22) |
| Coded bits Nbits, SGP Mode 4 | 0 | (hb p. 22) |
| Coherent averages Ncoh, SGP Mode 3 | 6 | (hb p. 22) |
| Spectra averaged Nspec, SGP Mode 3 | 60 | (hb p. 22) |
| Sensitivity gain, SGP Mode 3 vs Mode 4 | approximately 5 dB more sensitive | (hb p. 22) |
| Coded bits Nbits, SGP Mode 2 (cirrus) | 32 | (hb p. 22) |
| Sensitivity, SGP Mode 2 between 3-15 km | between -55 and -45 dBZ | (hb p. 22) |


_7 further rows in the report._

## The data

Verified example: **`sgparsclcbh1clothC1.c1`**, file `sgparsclcbh1clothC1.c1.20110101.000000.cdf`
(0.21 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=8640 |
| Data variables | 6 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 10 s |
| File time span | 0.0 to 86390.0 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `CloudBaseCeilometerCloth` | m AGL | time | - | BLC/VCEIL Clothiaux et al. Algorithm Cloud Base Height |
| `CloudBaseCeilometerStd` | m AGL | time | - | BLC/VCEIL Standard Algorithm Cloud Base Height |
| `CloudBaseMplZwang` | m AGL | time | - | MPL Wang and Sassen Algorithm Cloud Base Height |
| `CloudBasePrecipitation` | m AGL | time | - | Microwave Radiometer Wet Window/Optical Rain Gauge Cloud Base Height |
| `time` | seconds | time | - | Time Offset from base_time |


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
                     params={"user": f"{user}:{token}", "ds": "sgparsclcbh1clothC1.c1",
                             "start": "2011-01-01", "end": "2011-01-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgparsclcbh1clothC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgparsclcbh1clothC1.c1", "2011-01-01", "2011-01-01")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgparsclcbh1clothC1.c1", "2011-01-01", "2011-01-01"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgparsclcbh1clothC1.c1", "19961107", "20260924")
```

The report's own note on quality: The most useful QC flag in arscl1cloth is qc_ReflectivityClutterFlag: value 10 = no data present; value 0 (with reflectivity outside -100 to 30 after scaling) = data exist but no significant detection (no cloud); values 1/2/3 (with reflectivity in valid range) indicate significant detection, with 1 = hydrometeor only, 2 = hydrometeor+clutter mixed (cloud top uncertain but within flagged region), 3 = clutter/insects only. In the mode-level datastream, qc_ReflectivityClutterFlag additionally uses value 4 to indicate a significant detection exists in arscl1cloth merged product at that range/time...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Radar cannot conclusively identify hydrometeor-free regions | Absence of significant radar detection does not guarantee absence of small cloud drops (e.g., 4 micron radius drops far from radar go undetected) | Use combination of significant radar detections with lidar and passive radiation measurements to estimate cloud boundaries | (hb p. 2) |
| Heavy rain attenuation of 35-GHz beam | Millimeter wavelength beam does not fully penetrate during periods of heavy rain; reflectivity/Doppler fields degraded or contaminated during precipitation | None specific beyond noting the limitation; combined four-mode data still cannot resolve heavy rain periods | (hb p. 1) |
| Insect and biological particulate clutter contaminating radar returns | Significant power returns in MMCR data that are not from hydrometeors but from low-density airborne particulates/insects, especially below ~4 km | Use ceilometer and MPL cloud masks (which do not detect these particles) to filter MMCR data via Clutter Profile Code and Remove Clutter Code;... | (hb p. 24) |
| Pulse-coding partial decoding near minimum range | First Nbits-1 radar sample volumes contain inaccurate/limited-value reflectivity estimates due to partial decoding | Data flagged as such in qc fields; e.g., SGP Mode 2 unusable below 2985 m, Mode 1 below 465 m | (hb p. 13) |
| Range sidelobe leakage from pulse coding | Regions with strong reflectivity gradients and large Doppler velocities can contaminate weaker/slower regions within Nbits-1 sample volumes in either direction | None beyond noting limitation; contributes to Rmin values for coded modes | (hb p. 13) |
| Velocity aliasing (folding) from coherent integration | Particles with Doppler velocity exceeding Vu appear at incorrect velocity Vu minus offset on opposite side; affects Mode 3, 2, 1 more than Mode 4 | Use SGP Mode 4 (no coherent averaging, higher Vu) to identify/flag problems in Mode 3 data; reduce Ncoh to increase Vu at cost of sensitivity | (hb p. 13) |
| Spectral (velocity) weighting from coherent integration | Steep roll-off (3.9 dB / 60% loss) near spectral ends biases estimated mean velocity toward smaller values and lowers reflectivity estimates for broad, high-velocity spectra | Reduce Ncoh (increase Vu) or set Ncoh=1 to remove weighting, at cost of increased noise/reduced sensitivity | (hb p. 13) |
| Range aliasing (second trip echoes) | Backscattered power from a distant cloud arrives simultaneously with power from a pulse aimed at a nearer cloud, causing I/Q voltages from two different ranges to be superimposed | tau_ipp set sufficiently large to ensure prior pulse energy has returned before next pulse transmitted | (hb p. 14) |
| Trade-off in mode design (sensitivity vs artifacts/resolution) | No single MMCR operating parameter set can satisfy full -50 to +20 dBZ range without either lower sensitivity or velocity aliasing/range sidelobe artifacts; requires compositing 4 modes | Merge four operational modes (robust, general, cirrus, boundary layer stratus) in ARSCL processing | (hb p. 14) |
| qc_RadarArtifacts flagged data in modes 1-3 | Each mode except Mode 4 may have artifacts entering the final merged reflectivity field; flagged as problems in qc_RadarArtifacts, notably in pre-mid-October-1999 data using older mode set | Data flagged; problem occurs mainly for data collected before mid-October 1999 | (hb p. 24) |
| Laser (ceilometer/MPL) retrieval failure during heavy precipitation | Laser-based cloud base height retrievals fail during periods of heavier precipitation | Use MWR wet window flag or smetstd rain gauge precipitation rate to flag precipitation periods; cloud base assigned 0 m if all laser retrievals fail... | (hb p. 24) |
| Uncertain cloud top height when clutter and hydrometeors co-occur | qc_ReflectivityClutterFlag value of 2 indicates both hydrometeors and insects contribute; top of flagged region may not represent true cloud top, though true cloud top falls within the... | Use qc_ReflectivityClutterFlag interpretation guidance; cloud top uncertain but bounded | (hb p. 24) |
| Radar cannot conclusively establish true cloud top | qc_CloudLayerTopHeightMplCamp/Cloth variables note there is no way to conclusively establish cloud top from radar returns alone | Must be set/verified by analysis of MPL data | (hb p. 24) |
| Interpolation of arscl1cloth onto uniform grid may misrepresent time series | Data on interpolated 10 s/45 m grid; handbook states uncertainty about usefulness for time series analysis; laser-derived cloud base heights are not interpolated to this grid since doing so... | Use mmcrmode__v___ datastream (raw, uninterpolated) for time-series applications instead | (hb p. 20) |
| MMCR near-field reflectivity correction error | Below about 1 km, near-field correction applied to ARM MMCR data is off by about 2 to 3 dB near the surface, dropping to a few tenths of a dB by ~1 km | Correction factor being developed; will be incorporated when data are reprocessed | (hb p. 34) |
| SGP Belfort ceilometer height offset | From start of record until 3 Feb 2000, Belfort ceilometer heights (and hence ARSCL cloud base heights) are too high by 122 m | Offset removed from raw data starting 4 Feb 2000; historical data to be reprocessed | (hb p. 35) |
| NSA Micropulse Lidar height offset | Starting 16 June 1999 when NSA MPL was reactivated, backscatter profile heights (and cloud base heights) were 30 m too high, continuing until an unspecified later date | Raw MPL data and ARSCL VAP data for affected period will need reprocessing | (hb p. 35) |
| CloudBaseCeilometerCloth algorithm not yet implemented | Variable exists in datastream but algorithm applying Clothiaux et al. (1998) detection to Belfort/Vaisala ceilometer backscatter has not been implemented; field may be absent/unpopulated | None stated; noted as future work | (hb p. 23) |
| In-house lidar cloud mask algorithm not yet applied to blc/vceil25k raw backscatter | blccloth/vceil25kcloth products depend on algorithm not yet run on ceilometer datastreams; will only be implemented if pressing need arises and backscatter data become available | None stated beyond conditional future implementation | (hb p. 18) |
| Fields requiring further development / caution | CloudLayerBottomHeightMplCamp/Cloth and CloudLayerTopHeightMplCamp/Cloth variables flagged repeatedly with 'More work may need to be done here, so be very careful with this variable' | None stated beyond caution to the user | (hb p. 23) |
| Radar signal processor limits temporal resolution | Only 4% to 31% of data the radar hardware could generate is actually processed for SGP Modes 4 through 1, limiting temporal resolution to ~9 s | Planned processor upgrade could improve resolution to ~0.45 s without sacrificing sensitivity | (hb p. 42) |
| Power density spectra not saved at full resolution | Only first three moments (reflectivity, mean velocity, spectral width) saved at full temporal resolution; raw spectra saved only at selected times due to memory constraints | Radar can be remotely reconfigured to save spectra during interesting cloud events | (hb p. 42) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

- input instrument `mmcr`: load `arm-instrument-mmcr` for its handbook facts and artifacts
- input instrument `mpl`: load `arm-instrument-mpl` for its handbook facts and artifacts

### References the report cites

- Moran et al. (1998)
- Clothiaux et al. (1999)
- Clothiaux et al. (2000)
- Clothiaux et al. (1998)
- Campbell et al. (1998)
- Frisch et al. (1995)
- Fox and Illingworth (1997)
- Noonkester (1984)
- Heymsfield et al. (1991)
- Clothiaux et al. (1995)

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/arm-vap-002-1.pdf (56 pages, by Eugene E. Clothiaux, Mark A. Miller, Robin C. Perez, David D. Turner, Kenneth P. Moran, Brooks E. Martner, Thomas P. Ackerman, Gerald G. Mace, Roger T. Marchand, Kevin B. Widener, Daniel J. Rodriguez, Taneil Uttal, James H. Mather, Connor J. Flynn, Krista L. Gaustad, Brian Ermold)
- Catalog record: ARM data-source index, `instrument_class_code=arscl`, read 2026-09-24
- Example file: `sgparsclcbh1clothC1.c1.20110101.000000.cdf` from `sgparsclcbh1clothC1.c1`, 0.21 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
