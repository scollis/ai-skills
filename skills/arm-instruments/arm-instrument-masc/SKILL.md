---
name: arm-instrument-masc
description: ARM Multi-Angle Snowflake Camera (masc) - handbook-derived instrument reference: measurement principle, reported quantities (Hydrometeor stereographic images, Fall speed), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (nsamascC1.b1) and the variable inventory of a real file. Use when working with masc data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Surface Meteorology. Triggers - masc, Multi-Angle Snowflake Camera, nsamascC1.b1, Hydrometeor stereographic images, Fall speed, Surface Meteorology, Particle Flux Analytics / University of Utah MASC, cameras: Unibrain Fire-I 980b (Part number 4610), GUID, IEEE, IIDC, MASC.
---

# MASC - Multi-Angle Snowflake Camera

The MASC takes 9- to 37-micron resolution stereographic photographs of free-falling hydrometeors from three angles while simultaneously measuring their fall speed, deployed outdoors at ARM sites to characterize snow crystal size, shape, and fall behavior.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `masc` |
| Handbook | [DOE/SC-ARM-TR-158 / M Stuefer, J Bailey / July 2016](https://www.arm.gov/publications/tech_reports/handbooks/masc_handbook.pdf) |
| Measurement category | Surface Meteorology |
| Manufacturer / model | Particle Flux Analytics / University of Utah MASC; cameras: Unibrain Fire-I 980b (Part number 4610); former vendor Fallgatter Technologies (before January 2016) |
| Primary measurements | Hydrometeor fall velocity; Hydrometeor image |
| Record | 2015-10-25 to 2026-09-22 (active) |
| Datastreams with data | 4 across 2 sites |
| Sites | nsa, oli |
| ARM page | https://www.arm.gov/capabilities/instruments/masc |


## Credit

Everything this skill knows about the instrument is the work of **M Stuefer, J Bailey** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> M Stuefer, J Bailey. *Multi-Angle Snowflake Camera Instrument Handbook*, DOE/SC-ARM-TR-158, July 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/masc_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The MASC consists of three commercial cameras separated by angles of 36 degrees, each aligned to a common focus point about 10 cm away. A ring around the focal point houses two vertically stacked arrays of near-infrared emitter-detector pairs, separated vertically by 32 mm, that detect hydrometeor passage via IR pyroelectric motion sensors sensitive to infrared radiation from the falling particle. The lower emitter array triggers the three cameras and a bank of LED lights simultaneously, capturing an image triplet at exposure times as short as 1/25,000th of a second (up to 1/40,000th of a second per the theory of operations). Fall speed is derived from the time lag between successive triggers of the upper and lower IR motion sensor arrays as the hydrometeor traverses the 32 mm vertical separation. The electronics are designed to respond only to rapidly varying occultation of the IR beam, filtering out slow ambient light fluctuations from sunlight and shadows.

**Siting.** The MASC was deployed originally at NSA C-1 Barrow, Alaska (spring 2014), then relocated to AMF-3 Oliktok Point, Alaska (February 2015). Non-ARM deployments include Alta Ski Area Utah, Greenland Summit, and Mammoth Mountain California. RF interference from an adjacent radar instrument at AMF-3 caused false triggering, mitigated with RF chokes and new firmware.

**Sampling.** native rate Camera exposure ~1/25,000th of a second (up to 1/40,000th per theory of operations); capture interval can be as fast as hydrometeor inter-arrival times; reported every Typically set to once per second to limit excessive flashes; any number of images from zero to thousands per day (hb p. 11).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Hydrometeor stereographic images | png image | 9 to 37 micron resolution; snowflake... | - | 9-37 micron | (hb p. 7) |
| Fall speed | m/s | - | +/-10% of the fall speed in meters per second... | - | (hb p. 10) |


## Specifications

| parameter | value | source |
|---|---|---|
| Weight and size | 10kg, 43.5cm x 58cm x 21.5cm | (hb p. 21) |
| Cameras | 3 high-speed 5 Megapixel, 2/3" sensor, industrial cameras, each with C-mount 12.5mm lenses (swappable) | (hb p. 21) |
| Lights | Three 40W LEDs rated at 2700 lumens each | (hb p. 21) |
| Snowflake detection range | 40 micrometers to 3 centimeters | (hb p. 21) |
| Detection region | about 2.5 cm2 | (hb p. 21) |
| AC power receptacle rating | 13A | (hb p. 21) |
| Max power | 240W at 115-240VAC | (hb p. 21) |
| Power supplies | four 60W power supplies | (hb p. 21) |
| Anti-riming heat pads | two 50W heat pads and one 38W heat pad | (hb p. 21) |
| Heating system thermostat | turns on at 7C and off at 16C (hysteresis) | (hb p. 22) |
| Model | Unibrain Fire-I 980b | (hb p. 18) |
| Part number | 4610 | (hb p. 18) |
| Image Sensor | 2/3" progressive scan Sony ICX-625ALA 2/3" CCD | (hb p. 18) |
| Pixel size | 3.45 x 3.45 um | (hb p. 18) |
| Effective pixels | 5,054,448, 2456(H) x 2058(V) | (hb p. 18) |
| Picture sizes | 2448x2048, 1600x1200, 1280x960, 800x600, 640x480 | (hb p. 18) |
| Data path | 8 bit or 12 bit b/w | (hb p. 18) |
| CELL size | 3.45 um x 3.45 um | (hb p. 18) |
| Frame rates | 15, 7.5, 3.75, 1.875 fps | (hb p. 18) |
| Gain | 0-18 dB | (hb p. 18) |
| Multicamera sync | -144 us ~+144 us at 15, 7.5 frame rate | (hb p. 18) |
| Shutter speed | 5 usec - 3600 sec | (hb p. 18) |
| Gamma | 0.4-2.5 | (hb p. 18) |
| S/N ratio | 56 dB or better | (hb p. 18) |
| Power requirements | 310 mA max @+12V DC, 3.8 W | (hb p. 18) |
| Compact housing | 50 x 50 x 49 mm, weight 230 gram | (hb p. 18) |


_7 further specification rows are in the handbook._

## The data

Verified example: **`nsamascC1.b1`**, file `nsamascC1.b1.20260919.155142.nc`
(0.02 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=411, `camera`=3 |
| Data variables | 14 |
| QC variables | 1 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2026-09-19T15:51:42 to 2026-09-19T18:16:15 |
| dod version | masc-b1-1.0 |
| process version | ingest-masc-1.3-1.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `snowflake_fall_speed` | m/s | time | yes | Fall speed of the snowflake |
| `camera_id` | unitless | time,camera | - | Camera IDs of images taken |
| `crop_from_bottom` | unitless | camera | - | Number of pixels cropped from the bottom of the image |
| `crop_from_left` | unitless | camera | - | Number of pixels cropped from the left of the image |
| `crop_from_right` | unitless | camera | - | Number of pixels cropped from the right of the image |
| `crop_from_top` | unitless | camera | - | Number of pixels cropped from the top of the image |
| `field_of_view` | mm | camera | - | Horizontal field of view |
| `snowflake_id` | unitless | time | - | Snowflake ID number |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("nsamascC1.b1", "2026-09-19", "2026-09-19")
ds = armlive_open("nsamascC1.b1", "2026-09-19", "2026-09-19", cleanup_qc=True)
```

## Quality control in this datastream

1 `qc_` companion variables cover 1 of the
14 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable; then screen with the `act-qc`
helpers. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
act_qc_table(ds)                       # what each bit would remove, per variable
act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names
```

On the example file no test fired on any variable, so the flag machinery is
present but unexercised there - do not read that as a guarantee for other days.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("nsamascC1.b1", "20151025", "20260923")
```

The handbook's own note on data quality: The DQ-Explorer site includes quality control metrics and data-quality plots for visual inspection of MASC data. Weekly data quality assessment reports are disseminated by the ARM Data Quality Office at the University of Oklahoma. The MASC status output responds whenever image data is returned or during automatic status checks at regular intervals, reporting on microcontroller behavior, critical errors, power/software resets, and dropped images (rate exceeding disk write speed, or mis-formed/mis-transmitted image data). Image data itself is not flagged, but an image status file is generated...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| RF interference from adjacent radar causing false triggering | Trigger sensitivity issues / spurious triggers producing blank or distorted images | Installation of RF chokes to increase electromagnetic interference protection, and new firmware | (hb p. 14) |
| Blank or distorted images from false alarms or RF pollution | Blank images or distorted image data in the image dataset; image data itself not flagged but image status file may show errors | Images might be filtered based upon excessive fall speeds or image size information | (hb p. 13) |
| Dropped images due to image queue full | IMG_QFULL count in status log increments; missing images/snowflake IDs that do not repeat three times | Recorded in status log for diagnostic tracking | (hb p. 5) |
| Dropped images due to badly formed frames | IMG_BADFRAME count in status log; incomplete image triplets | - | (hb p. 6) |
| Dropped fall speeds due to speed queue full | FS_QFULL count in status log; missing fall speed records | - | (hb p. 6) |
| Camera bus resets | BUS_RST count increments in status log | - | (hb p. 5) |
| Microcontroller power/software resets or watchdog resets | MCR_PWR, MCR_BRWN, MCR_SFTWR, MCR_EXTR, MCR_WTCHDG flags set (X) in status log | - | (hb p. 5) |
| Only a fraction of triggered images are in sharp focus | Approximately 1 in 9 photographed images expected to be in focus given 11% overlap between camera depth of field and trigger depth of field for 35mm lens/10mm DOF setup | Physically block part of the lower emitter array (e.g., block two outermost emitters) to reduce trigger depth of field from 3100 to 1400 mm2,... | (hb p. 11) |
| Trade-off between lens focal length, resolution, and depth of field | Shorter lenses give lower resolution but larger depth of field/horizontal FOV; 35mm lens approximates 9cm object distance giving finer pixel resolution but constrained depth of field | Select lens according to desired balance of resolution vs depth of field; upgrades underway for higher-powered, more concentrated light to allow... | (hb p. 11) |
| Missing/dropped camera image in a triplet | A perfect acquisition run has each snowflake ID repeat three times (once per camera); if one is missing, that image has been dropped | - | (hb p. 8) |
| Fall speed uncertainty | Fall speed values carry an estimated uncertainty of about 10% | Verified via laboratory experiments measuring motion blur of photographed spherical metal beads at slow shutter speed for repeatability/accuracy | (hb p. 10) |
| Snow/frost/riming build-up on instrument | Blocked LED lights or obscured camera lenses leading to degraded or missing images | Anti-riming heating pads (100W collection plate pad plus additional housing pads) remove excess snow/ice from front of instrument; periodic manual... | (hb p. 19) |
| Scratch-prone polycarbonate windows on cameras/IR sensors | Scratches on windows degrade image/detector quality | Use soft cotton cloth for cleaning; do not use paper towels | (hb p. 18) |
| Dust/moisture ingress when lid removed | Contamination of internal electronics/optics | Lid should only be removed in dry, non-dusty conditions; inside of instrument must be clean and dry at all times | (hb p. 18) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration performed using a vendor-supplied calibration target; all cameras set to correct video mode; MASC typically connected to a portable laptop nearby for checking camera video stream in real time while performing camera adjustments; procedure described in MASC 'Getting Started Guide' (hb p. 17) |
| Calibration interval | Whenever new cameras are installed, or cameras are moved within the MASC housing (hb p. 17) |
| Routine maintenance | Periodic cleaning of camera and IR motion detector windows (polycarbonate, scratch easily - use soft cotton cloth, not paper towels); clean camera lens covers with soft cloth and glass cleaner; remove snow and frost build-up; anti-riming heat pads remove excess snow/ice from front of instrument; lid should only be... (hb p. 24) |
| Maintenance interval | as needed / periodic (hb p. 24) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AC` | alternating current |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `CCD` | change-coupled device |
| `DMF` | ARM Data Management Facility |
| `DOE` | U.S. Department of Energy |
| `DQ` | data quality |
| `Fps` | frames per second |
| `GUID` | A camera definition's unique identifier |
| `IEEE` | Institute of Electrical and Electronics Engineers |
| `IIDC` | Instrumentation & Industrial Digital Camera |
| `IR` | infrared |
| `LED` | light-emitting diode |
| `MASC` | Multi-Angle Snowflake Camera |


### References the handbook cites

- Garrett, TJ, C Fallgatter, K Shkurko, and D Howlett. 2012: "Fall speed measurement and high-resolution multi-angle photography of hydrometeors in freefall." Atmospheric Measurement Techniques 5: 2625-2633,...
- MASC technical specification at http://particleflux.net/data/MASC_Spec_Sheet.pdf
- Multi-Angle Snowflake Camera Getting Started Guide available through the vendor Particle Flux Analytics, University of Utah, UT 84112, Email: info@particleflux.net.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/masc_handbook.pdf (26 pages, DOE/SC-ARM-TR-158, by M Stuefer, J Bailey)
- Catalog record: ARM data-source index, `instrument_class_code=masc`, read 2026-09-23
- Example file: `nsamascC1.b1.20260919.155142.nc` from `nsamascC1.b1`, 0.02 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
