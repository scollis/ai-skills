---
name: arm-instrument-stereocam
description: ARM Stereo Cameras for Clouds (stereocam) - handbook-derived instrument reference. Measurement principle, reported quantities (JPEG cloud images, Battery voltage, Load voltage, Load current, Battery temperature, Ambient temperature, Remote temperature, Charger output power), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with stereocam data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - stereocam, Stereo Cameras for Clouds, bnfstereocambmovieS10.a1, JPEG cloud images, Battery voltage, Load voltage, Load current, Battery temperature, Ambient temperature, Cloud Properties, Moxa V2201 minicomputer, CACTI, COGS, JPEG, PCCP.
---

# STEREOCAM - Stereo Cameras for Clouds

The stereo camera setups acquire synchronized, stereo-calibrated JPEG image time series from paired ground-based cameras surrounding ARM facilities, enabling 3D triangulation of cloud features from the paired images.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 17 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `stereocam` |
| Handbook | [DOE/SC-ARM-TR-204 / DM Romps, R Öktem / May 2026](https://www.arm.gov/publications/tech_reports/handbooks/stereocam_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | StarDot Technologies SD500BN Netcam camera with StarDot 5MV4513CS lens; Moxa V2201 minicomputer; CradlePoint IBR 600LPE modem; Garmin 18x PC GPS puck; Morningstar MPPT 25A charge controller |
| Primary measurements | Images of Clouds; Instrument monitoring non-geophysical variables |
| Record | 2014-01-02 to 2026-09-22 (active) |
| Datastreams with data | 32 across 4 sites |
| Sites | bnf, cor, hou, sgp |
| ARM page | https://www.arm.gov/capabilities/instruments/stereocam |


## Credit

Everything this skill knows about the instrument is the work of **DM Romps, R Öktem** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> DM Romps, R Öktem. *Stereo Camera for Clouds (STEREOCAM) Instrument Handbook*, DOE/SC-ARM-TR-204, May 2026.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/stereocam_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

Two cameras of a stereo pair, separated by a known baseline and precisely time-synchronized, capture images of the same sky/cloud scene from different viewpoints. Matching cloud points identified in both images can be triangulated to obtain 3D positions of cloud features, producing the Point Cloud of Cloud Points (PCCP) Value-Added Product. When multiple stereo pairs (a "ring") surrounding a site observe the same cloud synchronously, their PCCP point clouds can be combined to reconstruct the full cloud surface and generate a 4D map of cloudiness (COGS VAP). Camera intrinsic parameters (lens distortion) are obtained via checkerboard calibration, while extrinsic parameters (orientation) are obtained using nighttime images of bright stellar objects to accurately determine each camera's azimuth, elevation, and roll.

**Siting.** Stereo camera pairs are sited in a ring configuration with each pair positioned to view clouds; cameras must be pitched 16o-20o up from the ground as a trade-off between avoiding nearby low clouds, capturing horizon landmarks, minimizing distortion at image center, and maximizing observed sky area. Baseline separation between paired cameras is chosen to be about an order of magnitude shorter than distance to observed objects (e.g., 500-600 m at SGP for clouds ~6 km away; 1.2 km at HOU for clouds ≥10 km away). Cameras of a pair should face roughly perpendicular to the baseline, typically tilted 3°-5° inward to maximize common field of view. Stability (minimum vibration) and clear FoV are...

**Sampling.** native rate 20-second intervals during the daytime and six minutes during the nighttime; reported every Images: 20 s (day) / 6 min (night); Auxiliary measurements: hourly; Movie: one-frame-per-two-minutes (hb p. 9).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| JPEG cloud images | pixels | 2592x1944 pixel resolution | - | 2592x1944 pixels | (hb p. 9) |
| Battery voltage | V | - | - | - | (hb p. 12) |
| Load voltage | V | - | - | - | (hb p. 12) |
| Load current | A | - | - | - | (hb p. 12) |
| Battery temperature | C | - | - | - | (hb p. 12) |
| Ambient temperature | C | - | - | - | (hb p. 12) |
| Remote temperature | C | - | - | - | (hb p. 12) |
| Charger output power | W | - | - | - | (hb p. 12) |
| Enclosure temperature | C | - | - | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Camera model | 5MP StarDot SD500BN Netcam, outdoor rated | (hb p. 7) |
| Lens | 4.5-13 mm varifocal StarDot 5MV4513CS lenses | (hb p. 7) |
| Image resolution | 2592x1944 pixels | (hb p. 7) |
| Horizontal field of view | 65o-75o | (hb p. 7) |
| Minicomputer | Moxa V2201 | (hb p. 7) |
| Cellular modem | CradlePoint IBR 600LPE | (hb p. 7) |
| GPS | Garmin 18x PC GPS puck | (hb p. 7) |
| Solar panels | two 145 W panels | (hb p. 7) |
| Battery | 12V 200Ah battery | (hb p. 7) |
| Charge controller | Morningstar MPPT 25A charge controller | (hb p. 7) |
| Camera pitch angle | 16o-20o up from the ground | (hb p. 7) |
| SGP baseline | 500-600-m baseline | (hb p. 7) |
| HOU baseline | 1.2-km baseline | (hb p. 7) |
| Camera yaw tilt | 3°-5° inward from perpendicular to the baseline | (hb p. 9) |
| Camera orientation accuracy after readjustment | within a ±2 degree accuracy | (hb p. 14) |


## The data

**No example file was verified for this instrument.** the product is MPEG video, not a dataset.

ARM's catalog lists 32 datastreams with data across 4 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
import os, requests

avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}',
                             "ds": "bnfstereocambmovieS10.a1", "start": start, "end": end,
                             "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])
```

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
files = act.discovery.download_arm_data(user, token, "bnfstereocambmovieS10.a1", start, end)

# These files are an MPEG program stream (magic 00 00 01 ba), not netCDF - `read_arm_netcdf` fails with
# "did not find a match in any of xarray's currently installed IO backends".
# Decode frames with an MPEG reader (ffmpeg/imageio); xarray has no backend for video.
print(os.path.getsize(files[0]) / 1e6, "MB of video")
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `[v for v in ds.data_vars if v.startswith("qc_")]` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("bnfstereocambmovieS10.a1", "20140102", "20260923")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: The image data quality is judged subjectively by the sharpness of images and metadata information collected with the images. Environmental factors such as rain, sun (when in FoV), or insufficient daylight may temporarily impact data quality during the day depending on season. Rain drops on the camera screen may distort images; heavy rain or fog may cause complete loss of visibility; dust or debris accumulation on the camera enclosure screen may also affect image quality. Movies and system monitoring plots can be accessed via DQ-Plotbrowser.

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Rain drops on camera screen | Distorted images visible during rainy weather conditions | None specified beyond noting the effect on data quality | (hb p. 11) |
| Heavy rain or fog | Complete loss of visibility in images | None specified | (hb p. 11) |
| Dust or debris accumulation on camera enclosure screen | Reduced image quality/sharpness | None specified beyond periodic inspection | (hb p. 11) |
| Sun in field of view / insufficient daylight | Temporary impact on image data quality depending on season and time of day | None specified | (hb p. 11) |
| Lens distortion at wide FoV | Highly noticeable geometric distortion in raw images, especially away from image center | Images stored as captured without correction; use intrinsic camera parameters (Table 3) with tools like OpenCV to correct for lens distortion | (hb p. 13) |
| Camera orientation shift from external incidents (bird landing, vehicle strike, ground... | Significant shift in camera's field of view; misalignment between paired camera views | Camera orientation manually readjusted by field operations team to maintain azimuth/pitch within ±2 degree accuracy; new extrinsic calibration... | (hb p. 14) |
| PCCP VAP gaps during FoV misalignment | Missing PCCP VAP data during periods when camera's FoV is out of adjustment | PCCP VAP is not produced during any periods when the camera's FoV is out of adjustment | (hb p. 15) |
| Camera replacement changes intrinsic parameters | Step change in intrinsic calibration parameters (k1,k2,k3,fx,fy,px,py) coincident with documented replacement dates | Camera intrinsic parameters must be recalibrated/updated at each camera replacement | (hb p. 12) |
| Spider webs on camera enclosure screen | Visible obstruction or blur in image videos | Checked daily via inspection of image videos | (hb p. 14) |
| Time synchronization drift between paired cameras | Images from stereo pair not properly time-aligned (must be within one second) | GPS puck resets minicomputer time daily at midnight to ensure synchronization within one second | (hb p. 9) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Intrinsic calibration using a checkerboard pattern (OpenCV, Bradski and Kaehler 2008; Hartley and Zisserman 2004) to correct lens distortion; extrinsic calibration using nighttime images and positions of bright stellar objects to determine camera orientation (azimuth, elevation, roll) for stereo reconstruction... (hb p. 13) |
| Calibration interval | Performed at initial deployment and then as required by camera mentors; intrinsic parameters updated only if camera is changed or zoom/focus readjusted; extrinsic parameters updated whenever camera positions/headings change or after incidents altering orientation (hb p. 13) |
| Routine maintenance | Inspect image videos for camera focus/heading/view change and spider webs in front of camera enclosure screen (daily); inspect battery for cracked/bulging cases and corroding terminals (monthly); inspect all wiring (annually); inspect enclosures for nesting insects (annually) (hb p. 14) |
| Maintenance interval | daily/monthly/annually as specified per task (hb p. 14) |


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
| `3D` | three-dimensional |
| `4D` | four-dimensional |
| `AMF1` | First ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement |
| `CACTI` | Cloud, Aerosol, and Complex Terrain Interactions |
| `COGS` | Clouds Optically Gridded by Stereo Value-Added Product |
| `COR` | Córdoba, Argentina CACTI site code |
| `DOE` | U.S. Department of Energy |
| `DQ` | Data Quality |
| `EF` | extended facility |
| `FoV` | field of view |
| `GPS` | Global Positioning System |
| `HOU` | Houston, Texas TRACER site code |
| `JPEG` | Joint Photographic Experts Group |


### References the handbook cites

- Bradski, G, and A Kaehler. 2008. Learning OpenCV: Computer Vision with the OpenCV Library. O'Reilly Media, Sebastopol, California.
- Hartley, RI, and A Zisserman. 2004. Multiple View Geometry in Computer Vision. Cambridge University Press, Cambridge, England.
- Öktem, R, Prabhat, J Lee, A Thomas, P Zuidema, and DM Romps. 2014. Stereophotogrammetry of Oceanic Clouds. Journal of Atmospheric and Oceanic Technology 31(7): 1482–1501.
- Romps, DM, and R Öktem. 2018. Observing Clouds in 4D with Multiview Stereophotogrammetry. Bulletin of the American Meteorological Society 99(12): 2575–2586.
- Romps, DM, and R Öktem. 2023. Retrieving Point Cloud of Cloud Points (PCCP) Value-Added Product from Stereo Cameras. DOE/SC-ARM-TR-252.
- Romps, DM. 2024. Principles of stereo reconstruction of aerial objects using stationary cameras. Remote Sensing Letters 15(11): 1118–1131.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/stereocam_handbook.pdf (17 pages, DOE/SC-ARM-TR-204, by DM Romps, R Öktem)
- Catalog record: ARM data-source index, `instrument_class_code=stereocam`, read 2026-09-23
- Example file: none - the product is MPEG video, not a dataset
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
