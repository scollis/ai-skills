---
name: arm-instrument-wsi
description: ARM Whole Sky Imager (wsi) - handbook-derived instrument reference: measurement principle, reported quantities (Sky radiance, Sector cloud cover fraction, Number of clouds), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. No data file could be verified for this instrument, and the skill says so in place of a variable inventory. Use when working with wsi data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category: Cloud Properties. Triggers - wsi, Whole Sky Imager, sgp02wsipartradmpgC1.b1, Sky radiance, Sector cloud cover fraction, Number of clouds, Cloud Properties, Marine Physical Lab / EO System 6 (E/O Camera System 6), Camera: Photometrics 16-bit CCD (Thomson TH7895B, AdaM, ARCS, NIST, SHEBA.
---

# WSI - Whole Sky Imager

The Whole Sky Imager is a ground-based, passive electronic camera system that acquires filtered images of the entire sky dome to detect and characterize cloud presence, distribution, and radiance under daylight, moonlight, and starlight conditions at fixed ARM sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 21 pages) or ARM's data-source catalog. No data file could
be opened for this instrument - see **The data**. Compiled 2026-09-23.

|  |  |
|---|---|
| ARM class code | `wsi` |
| Handbook | [ARM TR-043 / January 2005](https://www.arm.gov/publications/tech_reports/handbooks/wsi_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Marine Physical Lab / EO System 6 (E/O Camera System 6); Camera: Photometrics 16-bit CCD (Thomson TH7895B, Grade 1); Lens: Fisheye-Nikkor 8mm f/2.8 |
| Primary measurements | Cloud fraction |
| Record | 1995-09-20 to 2004-01-10 (retired) |
| Datastreams with data | 46 across 3 sites |
| Sites | nsa, sgp, twp |
| ARM page | https://www.arm.gov/capabilities/instruments/wsi |


## Credit

The handbook this skill derives from names no individual author on its cover;
it is issued by the ARM facility. The instrument knowledge in it is still the
mentor programme's work, not this file's:

> ARM Climate Research Facility. *Whole-Sky Imager (WSI) Handbook*, ARM TR-043, January 2005.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/wsi_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The WSI acquires images of the sky dome through a 180-degree fisheye lens onto a 16-bit CCD, using neutral density and spectral (red 650 nm, blue 450 nm) filters to cover an approximately 9-decade range of lighting conditions from full sun to starlight. Sky radiances are captured as two 16-bit images at the red and blue passbands, and a red/blue ratio image is computed and calibrated against a site-specific library of clear-sky ratio images (indexed by solar/lunar zenith angle) to distinguish opaque clouds (by whiteness/ratio threshold) from thin clouds (ratio exceeding background by 20%) and clear sky. A solar/lunar occultor with two degrees of freedom (arc and trolley) is positioned automatically to shade the lens and dome from direct sun/moon, preventing scattering artifacts. From the pixel-by-pixel cloud decision image, sector cloud cover fractions and Kegelmeyer statistical quantities (cloud cover fraction, path lengths, per-cloud area/perimeter/circularity) are derived.

**Siting.** The WSI must be shadowed from extraneous bright lights so the night sky is imaged properly (site responsibility). Occultor design differs by site: SGP and TWP use a different occultor design than NSA sites (Barrow/Atqasuk); TWP uses a larger shade fixed N-S, moving only E-W, obscuring 6% of the sky; NSA/SHEBA sites use a fixed shade covering the full 180 degrees to block the sun as it moves around the horizon; standard design shade is 24" from the dome obscuring less than 1% of sky. Requires accurate site location input for solar/lunar position calculations, and clear-sky ratio calibration library is site-dependent (depends on site altitude) and can only be determined after the imager has...

**Sampling.** native rate image sets as often as once a minute possible; reported every normally 10 minutes for the ARM Program (hb p. 12).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Sky radiance | - | - | net accuracy 5% (lamp calibration ~3% accurate) | - | (hb p. 7) |
| Sector cloud cover fraction (full sky and 9 sectors) | fraction | - | - | - | (hb p. 6) |
| Cloud path length mean and standard deviation | pixels or cloud-height units | - | - | - | (hb p. 6) |
| Clear path length mean and standard deviation | pixels or cloud-height units | - | - | - | (hb p. 6) |
| Number of clouds | count | - | - | - | (hb p. 6) |
| Cloud area mean and standard deviation | pixels or cloud-height units | - | - | - | (hb p. 6) |
| Cloud perimeter mean and standard deviation | pixels or cloud-height units | - | - | - | (hb p. 6) |
| Cloud circularity mean and standard deviation | ratio | - | - | - | (hb p. 6) |
| Positioning accuracy | degrees | - | generally 1 degree with experienced teams | 1/3 degree precision | (hb p. 7) |


## Specifications

| parameter | value | source |
|---|---|---|
| Sensor Dimensions | 28" W x 36" D x 36" H | (hb p. 13) |
| Sensor Weight | 410 lb | (hb p. 13) |
| Sensor Power | 614 watts (79 must be on UPS) | (hb p. 13) |
| Controller Dimensions | 26" W x 26" D x 52" H | (hb p. 13) |
| Controller Weight | 450 lb | (hb p. 13) |
| Controller Power | 150 watts (must be on UPS) | (hb p. 13) |
| Spectral Filters | 450 nm and 650 nm and open hole | (hb p. 14) |
| Spectral passband width | 70 nm | (hb p. 14) |
| Neutral Density Filters | 0, 2, and 3 logs (decades) neutral density | (hb p. 14) |
| Lens | Fisheye-Nikkor 8mm f/2.8 | (hb p. 14) |
| Angular resolution | 1/3 degree | (hb p. 14) |
| Field of view | 180 degrees (typically 181) | (hb p. 14) |
| CCD | Thomson TH7895B, Grade 1 | (hb p. 14) |
| Pixel array | 512 x 512 pixels | (hb p. 14) |
| A/D readout | 16 bit A/D readout at 40,000 pixels/second | (hb p. 14) |
| Fiber optic reducer | 25 mm to 11 mm fiber optic reducer | (hb p. 14) |
| CCD cooling | cooled to -35 C via 3-stage Peltier and liquid water/alcohol coolant | (hb p. 14) |
| Environmental Housing temperature | held at 60 F via thermo-electric air cooler | (hb p. 14) |
| Camera electronics temperature | 60 F (including A/D and pre-amp) | (hb p. 14) |
| Dynamic Range (overall) | 10.6 log or 40000000000:1 | (hb p. 14) |
| Dynamic Range (single image) | 45800:1 | (hb p. 14) |
| Readout Noise | 1.6 counts out of 65,536 grey levels | (hb p. 14) |
| Uniformity (Spatial Variation) | 1.6% (correctable) | (hb p. 14) |
| Precision (Temporal Variation) | 0.2% | (hb p. 14) |
| Nonlinearity | less than = 1% up to signal 10k, less than = 3% up to signal 50k (correctable) | (hb p. 14) |
| Pixel Resolution | 0.36 degrees | (hb p. 14) |


_8 further specification rows are in the handbook._

## The data

**No example file was verified for this instrument.** products are imagery (mpg/jpg) or summary files that ARM Live listed but would not serve.

ARM's catalog lists 46 datastreams with data across 3 sites, so data exist - but nothing in this skill's data,
variable or QC sections was measured, because nothing could be opened. Treat the
handbook facts above as the only verified content here, and check the variable names
yourself against a file before writing code against them:

```python
files = armlive_list_files("sgp02wsipartradmpgC1.b1", start, end)
```

## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

```python
import act
files = armlive_list_files("sgp02wsipartradmpgC1.b1", "2003-10-20", "2003-10-20")
ds = armlive_open("sgp02wsipartradmpgC1.b1", "2003-10-20", "2003-10-20", cleanup_qc=True)
```

## Quality control in this datastream

Not measured - no file was opened, so this skill cannot say which `qc_` variables
this datastream carries or which tests fire. ARM b1-level files usually ship a
`qc_` companion for most measurements; confirm with `act_qc_variables(ds)` once you
have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgp02wsipartradmpgC1.b1", "19950920", "20260923")
```

The handbook's own note on data quality: QC frequency is limited; QC delay N/A; QC type N/A; inputs are WSI images; outputs not specified; reference N/A. Data quality control beyond visual inspection of images is very limited at present. Comparison of cloud retrievals with Belfort laser ceilometer (BLC), Marine Physical Laboratory (MPL), or VCEIL data would require considerable effort. A contract with Mission Research Corporation is being set up to produce night and thin cloud retrieval algorithms, and instrument mentor Tim Tooman is trying to develop a calibrated radiance retrieval. Data Quality Health and Status (DQ HandS) and...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Calibration lamp uncertainty limits radiometric accuracy | Net accuracy of radiometric data limited to about 5% due to ~3% lamp calibration uncertainty | Use lamps accurate to about 3%; net accuracies of 5% normally achievable | (hb p. 7) |
| Positioning/pointing inaccuracy | Systematic offset between expected and measured pixel position corresponding to sun location | Can be checked and corrected for using measured sun positions | (hb p. 7) |
| Thin cloud vs haze ambiguity | Difficulty distinguishing a very thin cloud from a fairly thick haze in cloud decision output; thin cloud algorithm may misclassify haze | In near-real-time code, only opaque cloud results are presented until thin cloud algorithm is verified/improved for autonomous mode | (hb p. 7) |
| Visual misinterpretation of windowed 16-bit-to-8-bit images | Data appearing offscale bright or dark in displayed image may actually just be outside the selected display range, not truly offscale; dim features may appear invisible | Select a narrower/different display range; check image time and lighting condition (sun/moon/star) when interpreting | (hb p. 7) |
| Extraneous bright light contamination at night | Night sky images corrupted or improperly exposed due to stray lighting | Site responsibility to shadow instrument from extraneous bright lights | (hb p. 7) |
| CCD chip temperature excursion | CCD chip temp reading above -30 C (yellow) or above 0 C (red) flag codes 1 | Flagged via data quality flag table | (hb p. 8) |
| Environmental/camera housing overtemperature | Housing temperature above 32 C (yellow) or 49 C (red), flag codes 2/4 | Flagged via data quality flag table | (hb p. 8) |
| Coolant flow reduction | Coolant flow through camera below 0.125 gpm (yellow) or 0.09 gpm (red), flag codes 3 | Flagged via data quality flag table | (hb p. 8) |
| Camera non-response | Camera fails to respond for a grab, red flag code 5 | Red flag set | (hb p. 8) |
| Occultor positioning errors (arc/trolley timeout or off-position) | Occultor fails to reach or is not in specified position in greater than 10% (yellow) or greater than 90% (red) of images | Flag codes assigned (5-9) distinguishing arc vs trolley and timeout vs off-position | (hb p. 8) |
| Neutral density and spectral filter wheel errors | Filter unable to reach specified position in greater than 10% (yellow, codes 9/10) or greater than 90% (red, codes 10/11) of images | Flagged | (hb p. 8) |
| Exabyte tape write error | Unable to write to Exabyte in greater than 10% of attempts, yellow flag code 11 | Flagged | (hb p. 8) |
| Low nitrogen pressure in camera housing | Pressure below 2 psi triggers yellow/red flag code 12 | Flagged | (hb p. 8) |
| Loss of WWV time source | Time stamp on images not sourced from WWV signal, yellow flag code 13 proportional to number of images grabbed | Flagged | (hb p. 8) |
| Occultor obscuration of sky | Small solid angle of sky permanently blocked by occultor shade (less than 1% for standard design, 6% for TWP fixed shade) | Accepted as design tradeoff for reliability | (hb p. 6) |
| Clouds touching field-of-view/occultor edge excluded from per-cloud statistics | Number of clouds, cloud area/perimeter/circularity statistics undercount clouds that are only partially visible | Clouds touching edge of field of view or occultor/occultor arm are excluded from per-cloud statistics | (hb p. 6) |
| Opaque cloud misclassification near sun | Thin clouds near the sun sometimes incorrectly labeled as opaque clouds | Noted as an area for future algorithm improvement | (hb p. 7) |
| High aerosol/haze load causing indeterminate pixels | On very hazy days, clear-sky ratio may exceed opaque cloud ratio in some pixels (e.g., aureole), leading to pixels labeled indeterminate | Pixels labeled indeterminate | (hb p. 12) |
| Site-dependent clear-sky ratio calibration library requirement | Cloud decision algorithm cannot be fully validated until sufficient site-specific clear-sky ratio data (function of solar zenith angle, altitude, aerosol) has been collected | Library built up after imager has been at the site for a reasonable period | (hb p. 12) |
| Limited automated data quality control | Beyond image inspection, little cross-validation with independent cloud sensors is routinely performed | Considerable effort recommended to compare cloud retrievals with Belfort laser ceilometer (BLC), MPL, or VCEIL data; contract in progress for... | (hb p. 8) |
| Fiber-optic taper flat-fielding difficulty | Non-uniform pixel sensitivity artifacts specific to the fiber-optic taper complicate absolute radiance extraction | Unique technique developed using a 1-meter integrating sphere with numerical corrections to remove sphere artifacts | (hb p. 17) |
| Non-linearity of CCD response at high signal | Signal deviates from linear response, especially near saturation (less than =1% up to signal 10k, less than =3% up to signal 50k) | Correctable via radiometric linearity calibration | (hb p. 14) |
| Geometric/equi-distant projection deviation | Zenith angle vs pixel position deviates from ideal equi-distant projection by average 1.2 degrees | Correctable via geometric calibration | (hb p. 14) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration occurs at Marine Physical Lab prior to fielding, using a 2-meter precision calibration bar with a 1000W FEL lamp and a lambertian reflectance plaque; includes dark level vs exposure, dark level repeats, short/long exposure calibration, radiometric linearity, precision and uniformity, filter passband,... (hb p. 16) |
| Calibration interval | Performed prior to fielding; e.g., WSI01 calibrated Sept-Nov 94 with additional calibrations Dec 94 and Mar 95; WSI02 calibrated Aug 95 (hb p. 16) |
| Traceability | 1000W FEL lamp traceable to National Institute of Standards and Technology (NIST); high-accuracy resistance shunt monitors lamp current (hb p. 16) |
| Routine maintenance | See the SGP Preventative Maintenance Procedures (not detailed in handbook); system performs self-checks for proper readouts and data acquisition, automated self-shutdown under pre-defined conditions, and automated recovery from power down when power returns. (hb p. 18) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Belfort laser ceilometer (BLC), Marine Physical Laboratory (MPL) instrument, VCEIL.

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AdaM` | ARCS Data Management |
| `ARCS` | Atmospheric Radiation and Cloud Stations |
| `ARM` | Atmospheric Radiation Measurement (Program) |
| `CCD` | charge-coupled device |
| `CID` | CEPEX integrated data system |
| `DQ` | Data Quality |
| `IR` | infrared |
| `MPL` | Marine Physical Laboratory |
| `ND` | neutral density |
| `NIST` | National Institute of Standards and Technology |
| `NSA` | North Slope of Alaska |
| `QC` | quality control |
| `QME` | Quality Measurement Experiment |
| `SDS` | site data system |


### References the handbook cites

- Johnson, R.W., W.S. Hering, and J.E. Shields. 1989. Automated Visibility and Cloud Cover Measurements with a Solid-State Imaging System. SIO 89-7, GL-TR-89-0061, NTIS No. ADA216906.
- Johnson, R.W., J.E. Shields, and T.L. Koehler. 1991. Analysis and Interpretation of Simultaneous Multi-Station Whole Sky Imagery. SIO 91-33, PL-TR-91-2214.
- Shields, J.E., R.W. Johnson, and M.E. Karr. 1992. An Automated Observing System for Passive Evaluation of Cloud Cover and Visibility. SIO 92-22, PL-TR-92-2202, NTIS No. ADA216906.
- Sun, C.-H., and L.R. Thorne. Inferring Spatial Cloud Statistics from Limited Field-of-View Zenith Observations. To be submitted to J. Appl. Meteor.
- Buch, K.A., and C.-H. Sun. 1995. Cloud Classification Using Whole-Sky Imager Data. Ninth Symposium on Meteorological Observations and Instrumentation, Paper 7.5.
- Johnson, R.W., W.S. Hering, and J.E. Shields. 1986. Imagery Assessment for the Determination of Cloud Free Intervals. Atmospheric Visibility Technical Note No. 200.
- Shields, J.E., T.L. Koehler, M.E. Karr, and R.W. Johnson. 1990. Automated Cloud Cover and Visibility Systems for Real Time Applications. Optical Systems Group Technical Note No. 217.
- Shields, J.E., R.W. Johnson, and T.L. Koehler. 1991. Imaging Systems for Automated 24-Hour Whole Sky Cloud Assessment and Visibility Determination. Proceedings of the Cloud Impacts on DoD Operations and Systems.
- Shields, J.E., R.W. Johnson, and R.L. Koehler. 1993. Automated Whole Sky Imaging Systems for Cloud Field Assessment. Fourth Symposium on Global Change Studies.
- Shields, J.E., R.W. Johnson, M.E. Karr, B.J. Kroeger, D.R. Sauer, and J.R. Varah. 1994. Operations Manual: Day/Night Whole Sky Imager (E/O Camera System 6). Optical Systems Group Technical Note No. 236.

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/wsi_handbook.pdf (21 pages, ARM TR-043, no individual author named on the cover)
- Catalog record: ARM data-source index, `instrument_class_code=wsi`, read 2026-09-23
- Example file: none - products are imagery (mpg/jpg) or summary files that ARM Live listed but would not serve
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
