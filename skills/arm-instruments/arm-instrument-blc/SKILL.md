---
name: arm-instrument-blc
description: ARM Belfort Laser Ceilometer (blc) - handbook-derived instrument reference. Measurement principle, reported quantities (Visibility, Backscattering profile, Extinction coefficient), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpblcprofC1.a1) and the variable inventory of a real file. Use when working with blc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - blc, Belfort Laser Ceilometer, sgpblcprofC1.a1, Visibility, Backscattering profile, Extinction coefficient, Cloud Properties, Belfort Instruments, Model 7013C (field unit), Ceilometer, Field Unit, ASOS, BBSS.
---

# BLC - Belfort Laser Ceilometer

The Belfort Laser Ceilometer (BLC) Model 7013C is a self-contained, ground-based, active optical remote sensing instrument deployed at the SGP central facility that transmits vertical infrared laser pulses to detect cloud base height (up to three layers), extinction coefficient, and vertical visibility.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 23 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `blc` |
| Handbook | [ARM TR-040 / C. Flynn / January 2005](https://www.arm.gov/publications/tech_reports/handbooks/blc_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Belfort Instruments, Model 7013C (field unit); primary display unit included in system |
| Primary measurements | Cloud base height |
| Record | 1994-08-11 to 2000-05-23 (retired) |
| Datastreams with data | 2 across 1 sites |
| Sites | sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/blc |


## Credit

Everything this skill knows about the instrument is the work of **C. Flynn** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> C. Flynn. *Belfort Laser Ceilometer (BLC) Handbook*, ARM TR-040, January 2005.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/blc_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The ceilometer system detects clouds by transmitting pulses of near-infrared light (910 nm) vertically into the atmosphere from a Gallium Arsenide laser diode routed through a Newtonian transmitter telescope. The receiver telescope, aligned with the transmitter, detects scattered light from clouds and precipitation via an Avalanche Photo-Diode (APD). Each data acquisition cycle fires 5120 laser pulses (150 ns wide, at 1.024-ms intervals), and the receiver samples backscatter at a 20-MHz rate (50 ns) into range cells representing 7.6-m increments, yielding four accumulated phase arrays (Phase 0-3) used to extract signal from noise and breakthrough. The processed received power data is input to a Klett LIDAR inversion program to determine backscatter as a function of range, from which cloud base heights and extinction are computed. Elapsed time between transmitted and backscattered pulses establishes distance to the reflecting object (cloud layer), analogous to radar but using light energy instead of radio frequencies.

**Siting.** The field unit should be located in an area where collection of weather information is desired or needed, and the ground beneath and surrounding it should be leveled. The primary display unit is placed in a location convenient for system operators.

**Sampling.** native rate 5120 laser pulses per data acquisition cycle, pulses 150 ns wide at 1.024-millisecond intervals; receiver samples at 20-MHz (50 ns); reported every Default data acquisition cycle every 30 seconds; user-selectable 30 to 3600 seconds in 1-second increments; averaging Adaptive window filter applies averaging window based on S/N ratio per range cell; squelch rejects low S/N range cells (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Base height of lowest cloud detected | m | 15 to 7350 m AGL | - | 7.6 m | (hb p. 5) |
| Base height of second-lowest cloud detected | m | 15 to 7350 m AGL | may be optically obscured by lower clouds | 7.6 m | (hb p. 5) |
| Base height of third-lowest cloud detected | m | 15 to 7350 m AGL | may be optically obscured by lower clouds | 7.6 m | (hb p. 5) |
| Visibility (vertical) | - | - | qualitative indication; precise interpretation... | - | (hb p. 5) |
| Backscattering profile | - | 15 to 7350 m | - | 7.6 m | (hb p. 6) |
| Extinction coefficient | - | - | +/- 3 dB (extinction coefficient variation) | - | (hb p. 17) |


## Specifications

| parameter | value | source |
|---|---|---|
| Dimensions | 152 H X 72.4 W X 65.4 D centimeters | (hb p. 17) |
| Weight - Field Unit | 56.5 kg (125 lbs) | (hb p. 17) |
| Weight - Shipping | 105 kg (230 lbs) | (hb p. 17) |
| Supply voltage | 115VAC/60Hz (U.S. Model) | (hb p. 17) |
| Power Consumption | 930 W Total (800 W Heaters, 130 W Electronics) | (hb p. 17) |
| Height Range | 15 to 7350 meters | (hb p. 17) |
| Height Resolution | 7.6 meters | (hb p. 17) |
| Optical Source | Gallium Arsenide Laser-Diode | (hb p. 17) |
| Wavelength | 910 nm (near-infrared) | (hb p. 17) |
| Peak Optical Output | 15 W (nominal) | (hb p. 17) |
| Optical Pulse Length | 150 ns (nominal) | (hb p. 17) |
| Optical Pulse Repetition Frequency | 976.6 Hz | (hb p. 17) |
| Receiver Optical Detector | APD | (hb p. 17) |
| Extinction coefficient variation | +/- 3 dB | (hb p. 17) |
| Update Period | 30 seconds to 3600 seconds in 1-second increments | (hb p. 17) |
| Temperature Range (storage) | -50 to 65°Celsius | (hb p. 17) |
| Temperature Range (Operational) | -30 to 40°Celsius | (hb p. 17) |
| Relative Humidity | 0-100% | (hb p. 17) |
| Wind Speed | Max operational 50 m/s, Max survival on concrete base 75 m/s | (hb p. 17) |
| Beam divergence (both telescopes) | less than 3 milliradians | (hb p. 12) |
| Telescope tube diameter | 21.6-cm-diameter tube case | (hb p. 14) |
| Telescope mirror diameter | 20.3-cm-diameter concave mirror | (hb p. 14) |
| Sampling rate | 20-MHz rate (50 ns) | (hb p. 14) |
| Laser diode reduced voltage (over-temp safety) | 70 V | (hb p. 14) |
| TMPLD_FAIL threshold | 2 less than = TMPLD_FAIL less than = 5 degrees Celsius | (hb p. 8) |
| TX_DPSUC_status tolerance | /target-actual/ less than = 30 V | (hb p. 9) |


_3 further specification rows are in the handbook._

## The data

Verified example: **`sgpblcprofC1.a1`**, file `sgpblcprofC1.a1.20000520.000000.cdf`
(23.39 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=2835, `range`=1022 |
| Data variables | 28 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 30 s |
| File time span | 2000-05-20T00:00:00 to 2000-05-20T23:59:20 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `Klett_min_ext_coef` | unitless | - | - | Klett minimum extinction coefficient threshold |
| `Klett_squelch` | unitless | - | - | Klett algorithm signal squelch |
| `Klett_window` | unitless | - | - | Klett algorithm adaptive filter window |
| `actual_laser_temp` | degC | time | - | Actual laser diode temperature |
| `ambient_temp` | degC | time | - | Ceilometer ambient temperature |
| `apd_volts` | Volts | time | - | Avalanche Photo-Diode volts |
| `cloud1` | m above ground level | time | - | Base height of lowest cloud detected with threshold algorithm |
| `cloud2` | m above ground level | time | - | Base height of second cloud detected with threshold algorithm |
| `cloud3` | m above ground level | time | - | Base height of third cloud detected with threshold algorithm |
| `kcloud1` | m above ground level | time | - | Base height of lowest cloud detected with Klett algorithm |
| `kcloud2` | m above ground level | time | - | Base height of second cloud detected with Klett algorithm |
| `kcloud3` | m above ground level | time | - | Base height of third cloud detected with Klett algorithm |
| `laser_energy` | unitless | time | - | Laser Energy |
| `laser_volts` | volts | time | - | Laser Volts |
| `lidar_Klett` | counts per bin | time,range | - | Klett algorithm input |
| `lidar_amplitude` | counts per bin | time,range | - | threshold algorithm input |
| `range` | meters | range | - | distance to center of range bin after correcting for offset in sync |
| `range_offset` | meters | - | - | effective range offset due to poor sync between laser firing and A/D... |
| `receiver_temp` | degC | time | - | Receiver temperature |
| `status_flags` | 16 bit field packed... | time | - | Diagnostic flags from data packet |
| `target_laser_temp` | degC | time | - | Target laser diode temperature |
| `threshold_filter` | unitless | - | - | relative filter strength applied during threshold algorithm |
| `threshold_mincloudsig` | unitless | - | - | minimum cloud signal required for threshold algorithm. |
| `time` | - | time | - | Time offset from base_time |
| `visibility` | m | time | - | Vertical visibility |


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
                     params={"user": f"{user}:{token}", "ds": "sgpblcprofC1.a1",
                             "start": "2000-05-20", "end": "2000-05-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpblcprofC1.a1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpblcprofC1.a1", "2000-05-20", "2000-05-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpblcprofC1.a1", "2000-05-20", "2000-05-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("cloud1")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods
have nothing to act on. Screening has to come from the fields the product provides
itself and from Data Quality Reports.

Mask/flag fields in the verified file: `status_flags`.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpblcprofC1.a1", "19940811", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: QC frequency: once or twice a week; QC delay: three days behind current day; QC type: 'quick-view' plots. Inputs: operational_state variable in netcdf file sgpblcC1.*.cdf, and status_flags variable. Mentor examines operational_state to detect garbled data packets - this bit-packed field is produced by the SGP site data system collection module (not present in raw BLC data) and is zero unless a condition makes data suspect; excluding operational_stateless than greater than 0 data makes outliers very rare. status_flags is generated by the instrument itself (bit-packed) and is useful for...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Missed isolated clouds due to duty cycle | Gaps or missing cloud detections in periods when clouds are transient, since the instrument only actively collects backscattered photons for about 5 seconds of every 30-second measurement... | None stated beyond user awareness | (hb p. 6) |
| Optical obscuration of upper cloud layers | Second- and third-lowest cloud base heights frequently missing or absent from data even when upper clouds are present | None; first layer considered most accurate | (hb p. 6) |
| Inverse-square law signal attenuation at height | Higher clouds under harsh sky conditions are more likely to be missed (reduced detection probability with altitude) | None stated | (hb p. 6) |
| False clear-sky reports | Ceilometer indicates clear skies when clouds are actually present, especially in very thin clouds with sunlight, scattered/broken cloud layers, or heavy fog/rain/precipitation that blinds... | Users should be aware of these factors when interpreting cloud-clear periods | (hb p. 6) |
| Spurious extreme cloud-height values | BLC data contaminated by cloud-height values above 100,000 m in comparison dataset | Ignore/filter spurious BLC cloud heights above 100,000 m | (hb p. 6) |
| Cloud height bias vs. Vaisala VCEIL | BLC cloud heights read 100 to 120 m higher than co-located VCEIL after accounting for ~5-hour time offset | Window/align data in time before comparison | (hb p. 6) |
| Missing data flag | Field value of -999 assigned when data missing for a sample time | Treat -999 as missing_value | (hb p. 7) |
| Operational state / status flags indicating suspect data | Non-zero operational_state field (status_0x1000 Maintenance, status_0x2000 Comm Status data unavailable, status_0x4000 Packet Error possibly erroneous data, status_0x8000 garbled data... | Exclude data with operational_state less than greater than  0 from consideration; post-processing can recover some garbled data | (hb p. 7) |
| Garbled data packets in SGP SDS ingest | Outliers rare once operational_stateless than greater than 0 data excluded, but garbled packets present in files from SGP site data system at higher rate than seen on dedicated instrument PC | A 'smarter' ingest could identify and adjust for garbled packets; mentor manually post-processed limited chunks to recover data | (hb p. 8) |
| Multiplier breakthrough contamination | Contamination from swept gain waveform identical in Phase 0 and Phase 3, appearing as a low-frequency artifact in raw phase arrays | Filter extracts low-noise estimate of breakthrough curve and subtracts it from Phase 0 (direct subtraction would double noise) | (hb p. 12) |
| Electrical/ringing breakthrough in first range cells | Ringing appears in the first few range cells of Phase 0 due to electrical coupling of laser firing energy into receiver preamplifier | Ring calibration procedure stores stable ring signal in EPROM; subtracted from present data during normal operation | (hb p. 12) |
| Low S/N range cells | Range cells with low signal-to-noise ratio after adaptive window averaging | Squelch applied to reject low S/N range cells before Klett LIDAR inversion | (hb p. 13) |
| No recalibration performed | Calibration coefficients static from original 1993 factory calibration; no re-calibration events in data history | None; System Gain Calibration Unit never purchased by ARM Program | (hb p. 16) |
| Data loss during calibration procedure | Cloud base height data unavailable while System Gain Calibration Unit is placed over ceilometer | None stated beyond noting the gap | (hb p. 19) |
| Data unavailable during maintenance | Gaps in data during maintenance procedures | Documented in Site Operations Log | (hb p. 21) |
| Dirty transmitter/receiver windows | Degraded/reduced backscatter signal if windows not cleaned | Clean windows at least every three weeks with Windex or Glass-Plus; corrected on the spot if noticed dirty | (hb p. 21) |
| Instrument retirement / discontinuity | No data after March 24, 2000 (mid-day); instrument removed for repair and never returned to service | Replaced by Vaisala 25K ceilometer (VCEIL) | (hb p. 4) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Factory calibration using proprietary procedures; two field procedures 'SGAINCAL' and 'RINGCAL' require the Belfort-manufactured System Gain Calibration Unit ('Dog House'); ring signal calibration data stored in EPROM and subtracted during normal operation to remove breakthrough ringing (hb p. 15) |
| Calibration interval | Manufacturer recommends calibration upon delivery and every 6 months thereafter; however the BLC has never been recalibrated since original factory purchase because the System Gain Calibration Unit was never purchased by the ARM Program (hb p. 15) |
| Traceability | Original factory calibration by Belfort Instruments; proprietary, description of calibration theory not available (hb p. 15) |
| Routine maintenance | Ceilometer transmitter and receiver windows should be cleaned at least every three weeks using Windex or Glass-Plus; corrective maintenance performed at board level (replacing defective circuit board) (hb p. 21) |
| Maintenance interval | Every three weeks (window cleaning); other maintenance as needed (hb p. 21) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Vaisala 25K ceilometer (VCEIL).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `Ceilometer` | An instrument that detects cloud base height |
| `Field Unit` | The ceilometer itself |
| `APD` | Avalanche Photo-Diode |
| `ASOS` | Automatic Surface Observing System |
| `BBSS` | Balloon-Borne Sonde System |
| `BLC` | Belfort Laser Ceilometer |
| `CPU` | Central Processing Unit |
| `DC` | Direct Current |
| `DSP` | Digital Signal Processor |
| `EPROM` | Electrically Programmable Read Only Memory |
| `I/O` | Input/Output |
| `LED` | light-emitting diode |
| `LIDAR` | Light Detection And Ranging |
| `LLNL` | Lawrence Livermore National Laboratory |


### References the handbook cites

- Belfort Model 7013C Laser Ceilometer: Operating and Maintenance Procedures, T.J. Peters, May 1995, Pacific Northwest National Laboratory
- Belfort Model 7013C Ceilometer Technical Manual

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/blc_handbook.pdf (23 pages, ARM TR-040, by C. Flynn)
- Catalog record: ARM data-source index, `instrument_class_code=blc`, read 2026-09-23
- Example file: `sgpblcprofC1.a1.20000520.000000.cdf` from `sgpblcprofC1.a1`, 23.39 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
