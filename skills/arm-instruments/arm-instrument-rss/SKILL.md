---
name: arm-instrument-rss
description: ARM Rotating Shadowband Spectroradiometer (rss) - handbook-derived instrument reference: measurement principle, reported quantities (), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgprssC1.b1) and the variable inventory of a real file. Use when working with rss data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Radiometric. Triggers - rss, Rotating Shadowband Spectroradiometer, sgprssC1.b1, Radiometric, Yankee Environmental Systems (RSS105), ASRC, FWHM, MFRS, NIST.
---

# RSS - Rotating Shadowband Spectroradiometer

The RSS measures spectrally resolved direct-normal, diffuse-horizontal, and total-horizontal solar irradiance from 360-1050 nm using an automated shadowbanding technique, deployed at the SGP site (and formerly NSA) from sunrise to sunset.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 22 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `rss` |
| Handbook | [ARM TR-051 / P. Kiedron, J. Schlemmer, M. Klassen / May 2006](https://www.arm.gov/publications/tech_reports/handbooks/rss_handbook.pdf) |
| Measurement category | Radiometric |
| Manufacturer / model | Yankee Environmental Systems (RSS105); ASRC, SUNY at Albany (RSS102 & RSS103) |
| Primary measurements | Shortwave spectral diffuse downwelling irradiance; Shortwave spectral direct normal irradiance; Shortwave spectral total downwelling irradiance |
| Record | 2003-05-10 to 2007-12-05 (retired) |
| Datastreams with data | 1 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/rss |


## Credit

Everything this skill knows about the instrument is the work of **P. Kiedron, J. Schlemmer, M. Klassen** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> P. Kiedron, J. Schlemmer, M. Klassen. *Rotating Shadowband Spectroradiometer (RSS) Handbook*, ARM TR-051, May 2006.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/rss_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The RSS implements the automated shadowbanding technique used by the MFRSR: a rotating shadowband periodically shades a diffuser, allowing measurement of total horizontal diffuse radiation, then the diffuser is fully exposed to measure total horizontal downward radiation; the difference gives the downward component of the direct beam, from which direct beam solar irradiance is calculated. Irradiance spectra are measured simultaneously at all spectral elements (pixels) via a spectrograph imaging onto a CCD, with light passing through collimating lens, prisms, and camera lens onto the CCD detector. Measurements are corrected for cosine response of the diffuser/sensor assembly and for "excess sky" obscured by the shadowband during diffuse measurement. In one shadowbanding cycle, five measurements (including dark signal) are performed at different shadowband positions (Unblocked, CorrMinus, CorrPlus, Blocked, Dark) to derive DiffHor, DirHor, TotHor, and DirNorm via algebraic combination.

**Siting.** Shadowband axis angle for RSS105 is 45°; for RSS102 and RSS103 it is parallel with Earth axis. Shadowband center is on diffuser. Deployed at Southern Great Plains (SGP) site; RSS103 was also deployed at North Slope of Alaska (NSA) from 03/04/1999 to 08/16/1999.

**Sampling.** native rate 1 shadowbanding cycle per min; reported every From sunrise to sunset; averaging 5 measurements (including dark signal) per shadowbanding cycle at different shadowband positions (hb p. 5).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Direct normal solar spectral irradiance | W/m2/nm | 360-1050 nm | better than ±5% (including calibration and... | pixel-dependent, FWHM... | (hb p. 6) |
| Total horizontal solar spectral irradiance | W/m2/nm | 360-1050 nm | better than ±5% | pixel-dependent | (hb p. 6) |
| Diffuse horizontal solar spectral irradiance | W/m2/nm | 360-1050 nm | better than ±5% | pixel-dependent | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Number of pixels (RSS105) | 1024 | (hb p. 6) |
| Nominal Spectral Range (NSR) (RSS105) | 360-1050 nm | (hb p. 6) |
| Number of Pixels within NSR (RSS105) | 1001 | (hb p. 6) |
| Resolution (FWHM) @400nm (RSS105) | 0.37/1.56 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @500nm (RSS105) | 0.62/1.36 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @600nm (RSS105) | 1.05/1.40 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @700nm (RSS105) | 1.57/1.44 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @800nm (RSS105) | 2.16/1.52 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @900nm (RSS105) | 2.79/1.63 nm/pixels | (hb p. 7) |
| Resolution (FWHM) @1000nm (RSS105) | 3.42/1.78 nm/pixels | (hb p. 7) |
| Diffuser aperture | 0.25" | (hb p. 15) |
| Shadowband width | 8.1° | (hb p. 15) |
| Shadowband radius | 3.50" | (hb p. 15) |
| Shadowband length | 135° | (hb p. 15) |
| Shadowband position at corrections | ±9° | (hb p. 15) |
| Shadowband axis angle (RSS105) | 45° | (hb p. 15) |
| Field of view (FOV) | 8.1° | (hb p. 14) |
| Measurement rate | 1 shadowbanding cycle per min | (hb p. 5) |
| Number of spectra per day | From 570 spectra in Winter to 870 spectra in Summer | (hb p. 5) |
| Exposure time | 0.2-5 seconds | (hb p. 10) |
| Readout | 16-bit readout row capacity, 20+ bits combined dynamic range | (hb p. 10) |


## The data

Verified example: **`sgprssC1.b1`**, file `sgprssC1.b1.20071202.132900.cdf`
(31.51 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=582, `scan`=1040 |
| Data variables | 26 |
| QC variables | 9 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2007-12-02T13:29:00 to 2007-12-02T23:09:59 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `az` | degree | time | yes | azimuth |
| `diffuse` | W/m2/nm | time,scan | yes | Radiation, Shortwave, Downwelling, Diffuse |
| `directnormal` | W/m2/nm | time,scan | yes | Radiation, Shortwave, Direct normal |
| `el` | degree | time | yes | elevation |
| `exposure` | second | time | yes | scan exposure |
| `sdf_diff` | unitless | time,scan | yes | 1 sigma std. dev, fraction of diffuse |
| `sdf_dn` | unitless | time,scan | yes | 1 sigma std. dev, fraction of direct normal |
| `sdf_th` | unitless | time,scan | yes | 1 sigma std. dev, fraction of total horizontal |
| `totalhorizontal` | W/m2/nm | time,scan | yes | Radiation, Shortwave, Downwelling, Global |
| `blue_shift` | unitless | time | - | scan pixel shift in blue |
| `red_shift` | unitless | time | - | scan pixel shift in red |
| `time` | - | time | - | Time offset from midnight |
| `wavelength` | nm | time,scan | - | wavelength associated with CCD pixel |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgprssC1.b1", "2007-12-02", "2007-12-02")
ds = armlive_open("sgprssC1.b1", "2007-12-02", "2007-12-02", cleanup_qc=True)
```

## Quality control in this datastream

9 `qc_` companion variables cover 9 of the
26 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

Measured on the example file (sgprssC1.b1.20071202.132900.cdf), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `totalhorizontal` | Value is equal to missing_value. | 19206 | 3.1731 |
| `sdf_th` | Value is equal to missing_value. | 19206 | 3.1731 |
| `diffuse` | Value is equal to missing_value. | 19206 | 3.1731 |
| `sdf_diff` | Value is equal to missing_value. | 19206 | 3.1731 |
| `directnormal` | Value is equal to missing_value. | 19206 | 3.1731 |
| `sdf_dn` | Value is equal to missing_value. | 19206 | 3.1731 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgprssC1.b1", "20030510", "20260923")
```

The handbook's own note on data quality: Automated Quality Control/flagging is contained within netCDF files. Instrument Mentor Quality Control Checks: QC frequency Daily, QC delay Day+2, QC type Graphical plots, Inputs Raw data, Outputs Summary reports. Site Scientist/Data Quality Office Quality Control Checks: Not implemented yet. No value-added products implemented yet. Data Quick Looks/Near Realtime: Not available yet. Data Quality Health and Status: No routine implementation.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Photon and read noise | Standard deviation of noise calculated for every pixel of every scan; relative noise larger in absorption bands, strong Fraunhofer lines, and near 360 nm and 1050 nm edges | Noise parameters verified from calibration event data; noise value submitted with calibrated data (RSS105) | (hb p. 6) |
| Radiometric calibration error | Calibration transfer errors estimated at less than ±2% for each individual calibration | - | (hb p. 6) |
| Absolute radiometric scale error | NIST FEL lamp accuracy as large as ±4%; RSS-derived extraterrestrial spectrum differs less than 4% from accepted standard for wavelengths larger than 450 nm | - | (hb p. 6) |
| Nonlinearity | Detected and characterized from calibration data; errors up to ±1% in regions where signal is strong; growth of nonlinearity detected during first three months since deployment | Corrected in each scan of RSS105 via nonlinearity accounting algorithm; all data since deployment recalculated after September 2004 discovery | (hb p. 7) |
| Wavelength shift/error | Slight spectral shift during daily measurement due to temperature changes of optics and mechanical stress, less than 0.5 pixels | Detected in each scan via correlation technique with Fraunhofer spectrum and applied to responsivity | (hb p. 7) |
| Responsivity drift/stability | RSS105 exhibited strong responsivity drift during first several months of operation; RSS102 showed ±5% semiannual drift | Drift rate declined steadily; as of November 2004 drift less than 1% per month; bimonthly calibrations and interpolated responsivity used; RSS102... | (hb p. 7) |
| Stray light | Discrepancies appear in absorption bands when comparing RSS to modeled irradiance if truncated filter functions are used, appearing as residual stray light | Calculate modeled spectra using exact RSS filter functions, or remove stray light via deconvolution method (Kiedron et al. 2002) | (hb p. 7) |
| Dead pixel | Pixel 523 (approximately 503 nm) in RSS105 is dead | Average of pixel 522 and 524 reported instead, resulting in increased resolution at this pixel | (hb p. 6) |
| 8.1° field-of-view bias in shadowbanding correction | Equations overestimate direct and underestimate diffuse irradiance because correction (CorrMinus+CorrPlus)/2 does not eliminate all errors from 8.1° FOV; larger bias for aerosol size... | Estimation of these errors for RSS geometry not completed; correction scheme used in RSS expected to result in significantly smaller errors than... | (hb p. 12) |
| Color glass filter contribution to instability | Sandwich of two color glass filters located between slit and collimating lens reduces dynamic range and increases out-of-band rejection in UV and NIR, but hypothesized to contribute to... | Hypothesis not yet confirmed | (hb p. 10) |
| Embedded Linux computer malfunctioning | Frequent downtime due to embedded Linux computer malfunctions prior to February 2004 | BCR 00776 implemented removing embedded Linux computer; new xtty software launched to acquire and parse data | (hb p. 15) |
| Shadowbanding mechanical failure (September 2004) | Shadowbanding does not shadow correctly; only total horizontal spectra available for September 2004 | Combo board replacement cured the problem after 3 weeks of troubleshooting | (hb p. 15) |
| Shadowbanding mechanical failure (April-June 2005) | Shadowbanding does not shadow correctly in afternoons; specific date ranges with all-day bad shading or bad shading from 1h before noon during which no direct nor diffuse data reported:... | Motor replacement fixes the problem | (hb p. 15) |
| PortCal/PROM failure and calibrator gaps | Calibration event frequency plot (Figure 7) shows gaps annotated with I/O Modification, PortCal sent to NREL, PROM failure, Total Horizontal Only | - | (hb p. 14) |
| Missing data flagging | Missing data denoted as -999 in data files (netCDF files of processed/calibrated data not yet produced at time of writing) | - | (hb p. 8) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Radiometrically calibrated with a Licor calibrator (once a month) and a Portable Calibrator (twice a month); wavelength calibration with HgCd Oriel Calibrator discontinued March 2004; can also be calibrated in situ via Langley regression (hb p. 13) |
| Calibration interval | Two Portable Calibrator calibrations per month and one Licor calibration per month expected (best case); since November 2005, calibrations performed once every two weeks (hb p. 13) |
| Traceability | Licor irradiance is traceable to NIST irradiance standards (hb p. 13) |
| Routine maintenance | RSS band movement and shading when direct sun is available is checked daily; diffuser is wiped with distilled water; malfunctions reported to mentor who initiates corrective actions (except power recycling) (hb p. 14) |
| Maintenance interval | Daily (hb p. 14) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: multifilter rotating shadowband radiometer (MFRSR), UV-RSS104.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `ASRC` | Atmospheric Sciences Research Center |
| `BCR` | baseline change request |
| `CCD` | charge-coupled device |
| `DQ` | Data Quality |
| `FOV` | field-of-view |
| `FWHM` | Full Width at Half Maximum |
| `MFRS` | muti-filter rotating shadowband radiometer |
| `NIST` | National Institute of Standards and Technology |
| `NSA` | North Slope of Alaska |
| `RSS` | rotating shawdowband spectroradiometer |
| `SGP` | Southern Great Plains |
| `SZA` | Sun Zenith Angle |
| `UV` | ultraviolet |


### References the handbook cites

- Harrison and Michalsky (1994) Automated Multifilter Rotating Shadow-Band Radiometer: An Instrument for Optical Depth and Radiation Measurements, Appl. Optics 33:5118-5125
- Harrison and Michalsky (1994) Objective Algorithms for the Retrieval of Optical Depths from Ground-Based Measurements, Appl. Optics 33:5126-5132
- Kiedron et al. (2002) Data and Signal Processing of Rotating Shadowband Spectroradiometer (RSS) Data, Proc. SPIE 4815:58-72
- Kiedron et al. (1999) Comparison of Spectral Irradiance Standards Used to Calibrate Shortwave Radiometers and Spectroradiometers, Appl. Optics 38:2432-2439
- Harrison et al. (2003) Extraterrestrial Solar Spectrum 360-1050 nm from Rotating Shadowband Spectroradiometer Measurements at SGP, J. Geophys. Res. 108:4424

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/rss_handbook.pdf (22 pages, ARM TR-051, by P. Kiedron, J. Schlemmer, M. Klassen)
- Catalog record: ARM data-source index, `instrument_class_code=rss`, read 2026-09-23
- Example file: `sgprssC1.b1.20071202.132900.cdf` from `sgprssC1.b1`, 31.51 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
