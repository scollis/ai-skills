---
name: arm-bnf-site
description: "Reference for the DOE ARM Bankhead National Forest (BNF) observatory in northern Alabama, the AMF3 deployment that followed Oliktok Point - why the southeastern US and the forest were chosen, the 2021-2024 timeline, science themes, partners, every facility code (M1 main site, S1/S2 collocated, S3 C-SAPR2, S4 Ka/X-SACR, S10 tower, S13/S14 soil plots, S20 Courtland, S30 Falkville, S40 Double Springs, U2 ArcticShark) with page coordinates, an instrument-by-instrument position audit read from the most recent a-level files, distinct instrument positions for site maps, S3-M1 and S4-M1 geodesics, radar outage epochs from the file record and DQRs, the BNF field campaigns with PIs, and datastream DOIs crediting the mentors. Use for any BNF data request, site map, instrument location, radar geometry or citation."
---

# ARM Bankhead National Forest (BNF) observatory, Alabama

BNF is the third ARM Mobile Facility (AMF3) on a long-term deployment in the William B. Bankhead
National Forest, north-west Alabama. The main site (M1) is in a forest clearing at the US Forest
Service Black Warrior Work Center, south-west of Moulton. For instrument physics and per-datastream QC
load the instrument skills (for example `arm-instrument-csapr`, `arm-instrument-kazr`,
`arm-instrument-sonde`); for data access load `act-arm-live`.

## Credit

The site was planned by the AMF3 Site Science Team led from Brookhaven National Laboratory
(Kuang, Giangrande, Serbin and co-authors, science plan DOE/SC-ARM-23-035,
[10.2172/2280575](https://doi.org/10.2172/2280575)); the overview paper is Kuang et al. (2026, BAMS,
[10.1175/BAMS-D-25-0072.1](https://doi.org/10.1175/BAMS-D-25-0072.1)). The science plan thanks
Andy Scott and Shane Hoskins (USFS) for siting at the Black Warrior Work Center and UAH staff
(Knupp, Mecikalski, Lee, Carey, Freeman and others) for regional data and site visits. Each datastream
has a DOI whose creators are the instrument mentors and data developers; the "Data DOIs" table names
them and `bnf_dois.csv` covers every audited datastream. Cite the DOI for every datastream used, and
acknowledge: "Data were obtained from the Atmospheric Radiation Measurement (ARM) User Facility, a
U.S. Department of Energy (DOE) Office of Science user facility managed by the Biological and
Environmental Research program."

## History

- **AMF3 before BNF.** AMF3 ran at Oliktok Point, Alaska (site `oli`), from September 2013 to June
  2021, then was packed out June-September 2021 (ARM BNF science page).
- **Siting, 2021-2022.** ARM's timeline: a southeastern-US short list in March 2021, logistics
  analysis and site choice March-September 2021, approvals, leases and contracts September 2021 to
  September 2022. The USFS special-use permit for the forest site was approved in December 2022
  (ASR news, 2024).
- **Why northern Alabama.** The site science team recommended N. Alabama "from among several
  candidate regions" (science plan §1), weighing complex terrain, coastal proximity, representative
  forest cover and land-use diversity, aerosol sources, cloud frequency and severity, air space for
  aerial work and partner facilities. The forest, agricultural valley and Huntsville urban area give a
  heterogeneous contrast to the ARM SGP; the region is a maximum for high-impact weather. The main site
  sits in intact forest for "canopy to the clouds" studies, with a 43 m (140 ft) walk-up tower.
- **Science themes.** Land-atmosphere interactions over a heterogeneous forest and farm landscape;
  biogenic VOC emissions, secondary organic aerosol and new particle formation; aerosol-cloud
  interactions; convective onset and the shallow-to-deep transition, mesoscale convective systems
  and severe weather (science plan; BAMS 2026).
- **Opening.** Construction delays (weather, staffing, electrical parts) pushed instrument
  installation to August-September 2024; M1 and the three supplemental sites opened on 2024-10-01
  (BNL news; locations page start 2024-10-01 06:00 UTC). The planned duration is
  five years (science plan §3.1; FY2025 radar plan lists 2024-2029).
- **Phase 2.** The C-SAPR2 (S3) and Ka/X-SACR (S4) sites needed state and tribal historic
  preservation review; the first C-SAPR2 a1 file is 2025-02-16 and the first SACR files 2024-11-24.
  The tethered balloon system began at M1 in spring 2025.
- **ArcticShark (U2).** The AAF ArcticShark flew BNF engineering and science flights from
  Cullman Regional Airport, 2024-07-24 to 08-07 (ARM news), then from Posey Field (FAA 1M4,
  Haleyville) on 2025-03-10 to 03-24 and 2025-05-28 to 06-23 (CHELAX-BNF dataset records, OSTI
  2997211). The U2 page coordinate is 249 m from the Posey Field reference point (34.28027778,
  -87.60055556); the first navigation fix of the 2026-09-16 flight is 203 m from the page point.
- **Partners.** USFS Bankhead Ranger District (Black Warrior Work Center), UAH, Alabama A&M and the
  Alabama Mesonet, NWS Huntsville/Birmingham/Nashville and KHTX/KGWX/KBMX NEXRADs, the North Alabama
  LMA, NASA MSFC GPM-GV, IMPROVE, EPA CSN and ASCENT (science plan §3.5.1).

## Facilities

From the ARM locations page, read 2026-10-20 (`const locations` JSON); an end date of 2026-10-20 is
the open-ended placeholder. Classes counts instrument classes per facility in
`bnf_instrument_audit.csv`; active means an ARM Live file dated on or after 2026-08-01.

| code | what it is | lat | lon | alt (m) | period (page) | classes | active |
|---|---|---|---|---|---|---|---|
| M1 | Main site in the forest clearing at the USFS Black Warrior Work Center: AMF3 core, KAZR, lidars, AOS, sondes | 34.342481 | -87.338177 | 293 | 2024-10-01 – 2026-10-20 | 52 | 36 |
| S1 | Collocated with M1: tethered balloon system (TBS) payloads and a second Doppler lidar | 34.342481 | -87.338177 | 293 | 2024-10-01 – 2026-10-20 | 7 | 0 |
| S2 | Collocated with M1: reserved code, no datastreams | 34.342481 | -87.338177 | 293 | 2024-10-01 – 2026-10-20 | 0 | 0 |
| S3 | C-SAPR2 C-band scanning precipitation radar site, north of the forest | 34.630806 | -87.133118 | 180 | 2024-10-01 – 2026-10-20 | 2 | 2 |
| S4 | Ka/X-band scanning cloud radar (KASACR/XSACR) site near Moulton | 34.464279 | -87.236001 | 197 | 2024-10-01 – 2026-10-20 | 3 | 3 |
| S10 | 43 m walk-up tower in the canopy about 1.1 km west of M1 | 34.3437276 | -87.35044401 | 284 | 2024-10-01 – 2026-10-20 | 16 | 16 |
| S11 | Collocated with the tower: page holds 0,0, no datastreams | — | — | — | 2024-10-01 – 2026-10-20 | 0 | 0 |
| S13 | STAMP2 soil profile and SEBS/ECOR plot beside the tower | 34.344015 | -87.35062209 | 286 | 2024-10-01 – 2026-10-20 | 6 | 6 |
| S14 | STAMP3 soil profile and SEBS/ECOR plot beside the tower | 34.343399 | -87.350858 | 282 | 2024-10-01 – 2026-10-20 | 6 | 6 |
| S20 | Supplemental site at Courtland (north, agricultural valley) | 34.653784 | -87.292676 | 178 | 2024-10-01 – 2026-10-20 | 15 | 14 |
| S30 | Supplemental site at Falkville (east) | 34.384829 | -86.927905 | 183 | 2024-10-01 – 2026-10-20 | 11 | 10 |
| S40 | Supplemental site at Double Springs (south-west) | 34.178796 | -87.453905 | 236 | 2024-10-01 – 2026-10-20 | 13 | 11 |
| U2 | ARM Aerial Facility ArcticShark UAS; page point is Posey Field (1M4), Haleyville | 34.280111 | -87.597858 | 279 | 2024-07-15 – 2026-10-20 | 13 | 10 |

Active classes at M1 (36): acsm, aeri, aos, aosmet, aps, asi, caminst, ccn, ceil, co-analyzer, cpc, csphot, dl, gndrad, hsrl, kazr, ldis, maws, met, mfrsr, monitorinst, mpl, mwr3c, nephelometer, psap, rwp, sirs, skyrad, smps, so2, sonde, sp2, tbsground, uhsas, vdis, wb.

S1 is the TBS and second-Doppler-lidar code; S2 and S11 carry no datastreams. U2 is not a ground
site.

## Instrument position audit (2026-10-20)

`bnf_instrument_audit.csv` (`bnf_instrument_audit()`) holds one row per instrument class x facility.
Instrument means an `armobs` datastream in the catalog (VAPs and `ceilpblht` excluded). For each row
the datastream with the most recent ARM Live file was chosen (within 30 days of the newest), a-level
first and the smallest file among equals; the position was read from that file's `lat`/`lon`/`alt`
variables. The b-level file is used where ARM serves no a-level or the a-level holds no position.
Of 144 rows (82 classes at 11 facilities), 134 carry a position: 56 from a-level
and 78 from b-level files, 9 of the latter because the a-level file holds no position (all
ArcticShark payloads). Offsets are geodesic from the facility's page coordinate.

| flag | rows |
|---|---|
| page value | 102 |
| moving platform (median of track) | 16 |
| within 50 m of page | 10 |
| no position: no served a/b-level datastream (a0 only or data_available false) | 6 |
| no position: no netCDF file (images, movies or tar only) | 4 |
| differs from page by more than 50 m | 2 |
| moving platform; bad: track holds spurious GPS fixes | 2 |
| bad: 0,0 | 1 |
| moving platform; launch point rounded to 0.01 deg | 1 |

Findings:

- **File and page agree for most instruments.** 102 rows store the page coordinate itself (as
  float32, within 0.4 m). Radars included: C-SAPR2, KASACR, XSACR and KAZR store the S3, S4 and M1
  page values, so the files do not place the radar pedestal more precisely than the page.
- **Instruments with their own coordinate.** AERI, Cimel and Doppler lidar at M1 sit 33-48 m from the
  page point; at S20, S40, S13, S14 and S30 the ECOR, DL and AERI do too. Two exceed 50 m: the S40
  Doppler lidar (92 m) and the S40 ECOR (52 m).
- **Bad metadata.** Both S1 Doppler lidar datastreams (`bnfdlppiS1.b1`, `bnfdlfptS1.b1`) store 0,0.
  The S1 TBS CPC and POPS tracks hold spurious GPS fixes (latitudes 2-67 N). The sonde stores its
  launch point to 0.01 deg (34.35, -87.34), 0.85 km NNW of M1, so the true launch pad is not
  recoverable from the file.
- **No position.** Cameras, stereo cameras and the Raman lidar (a0 only) cannot be placed from files.

## Distinct instrument positions

`bnf_instrument_positions.csv` (`bnf_positions()`) has one row per distinct file position (to
1e-5 deg) with the instruments there; this is what the site map draws. `first fix` rows are the
sonde, TBS and ArcticShark starting points.

| key | lat | lon | alt (m) | facilities | instruments | from M1 |
|---|---|---|---|---|---|---|
| m1 | 34.342480 | -87.338181 | 293 | M1, S1 | 42 classes | 0.000 km, 0° |
| m1_aeri | 34.342083 | -87.337982 | 295 | M1 | aeri | 0.048 km, 157° |
| m1_csphot | 34.342201 | -87.337997 | 293 | M1 | csphot | 0.035 km, 151° |
| m1_dl | 34.342338 | -87.337860 | 297 | M1 | dl | 0.033 km, 118° |
| s10_tower | 34.343727 | -87.350441 | 284 | S10 | 14 classes | 1.137 km, 277° |
| s13 | 34.344013 | -87.350624 | 286 | S13 | irt, metwxt, par, sebs, stamp | 1.157 km, 278° |
| s13_ecor | 34.344002 | -87.350578 | 290 | S13 | ecor | 1.153 km, 278° |
| s14 | 34.343399 | -87.350861 | 282 | S14 | irt, metwxt, par, sebs, stamp | 1.171 km, 275° |
| s14_ecor | 34.343380 | -87.350853 | 286 | S14 | ecor | 1.170 km, 275° |
| s20 | 34.653786 | -87.292679 | 178 | S20 | 11 classes | 34.786 km, 7° |
| s20_ecor | 34.653671 | -87.292671 | 178 | S20 | ecor | 34.773 km, 7° |
| s20_dl | 34.653994 | -87.292464 | 178 | S20 | dl | 34.811 km, 7° |
| s20_aeri | 34.653793 | -87.292770 | 180 | S20 | aeri | 34.785 km, 7° |
| s3_csapr2 | 34.630806 | -87.133118 | 180 | S3 | csapr, ldis | 37.119 km, 30° |
| s30 | 34.384830 | -86.927902 | 183 | S30 | 10 classes | 38.032 km, 83° |
| s30_ecor | 34.384460 | -86.927841 | 183.8 | S30 | ecor | 38.033 km, 83° |
| s4_sacr | 34.464279 | -87.236000 | 197 | S4 | kasacr, ldis, xsacr | 16.457 km, 35° |
| s40 | 34.178795 | -87.453903 | 236 | S40 | 10 classes | 21.054 km, 210° |
| s40_dl | 34.179543 | -87.453466 | 231 | S40 | dl | 20.962 km, 210° |
| s40_ecor | 34.179150 | -87.453537 | 232 | S40 | ecor | 21.003 km, 210° |
| s40_aeri | 34.178970 | -87.453651 | 230 | S40 | aeri | 21.026 km, 210° |
| sonde_launch | 34.349998 | -87.339996 | 306.1 | M1 | sonde | 0.851 km, 349° |
| tbs_launch | 34.341717 | -87.338264 | 295.2 | M1 | tbswind | 0.085 km, 185° |
| u2_takeoff | 34.278336 | -87.598404 | 298 | U2 | nav-air | 24.987 km, 254° |

## Distances

From file positions, WGS84 geodesic (`bnf_distance()`, Vincenty, agrees with pyproj to 1 cm):

| leg | distance | bearing |
|---|---|---|
| S3 C-SAPR2 → M1 | 37.12 km | 211° |
| S4 SACR → M1 | 16.46 km | 215° |
| S3 C-SAPR2 → S4 SACR | 20.75 km | 207° |
| M1 → S10 tower | 1.14 km | 277° |
| M1 → S20 Courtland | 34.79 km | 7° |
| M1 → S30 Falkville | 38.03 km | 83° |
| M1 → S40 Double Springs | 21.05 km | 210° |
| M1 → U2 take-off | 24.99 km | 254° |
| S20 → S30 | 44.86 km | 132° |
| S30 → S40 | 53.55 km | 245° |
| S40 → S20 | 54.74 km | 16° |

ARM's gridded-SACR announcement quotes 16.4 km from S4 to the main site, consistent with the
table. The supplemental triangle sides are 45-55 km, not the "about 50 km" each that ARM news gives.

## Radar operating epochs

Daily ARM Live file counts from 2024-09-01 to 2026-10-20 ship as `bnf_radar_daily_files.csv`;
`bnf_radar_gaps()` finds runs of empty days. DQRs (`bnf_radar_dqrs.csv`, ARM DQR service, read
2026-10-20) give the cause.

| radar datastream | first day | last day | gaps of 3+ days with no file |
|---|---|---|---|
| `bnfcsapr2cfrS3.a1` | 2025-02-16 | 2026-10-15 | 2025-06-24 – 2026-01-18 (209 d); 2026-01-29 – 2026-06-01 (124 d); 2026-08-09 – 2026-08-17 (9 d) |
| `bnfxsacrcfrS4.a1` | 2024-11-24 | 2026-10-19 | 2025-06-14 – 2025-06-25 (12 d); 2025-07-26 – 2025-08-07 (13 d); 2026-07-03 – 2026-07-05 (3 d); 2026-08-09 – 2026-08-11 (3 d) |
| `bnfkasacrcfrS4.a1` | 2024-11-24 | 2026-10-19 | 2025-06-14 – 2025-06-25 (12 d); 2025-07-26 – 2025-08-07 (13 d); 2026-07-03 – 2026-07-05 (3 d); 2026-09-06 – 2026-09-08 (3 d); 2026-09-26 – 2026-09-30 (5 d) |
| `bnfkazr2cfrgeM1.a1` | 2024-11-08 | 2026-10-19 | 2025-02-13 – 2025-02-17 (5 d); 2026-08-05 – 2026-08-10 (6 d); 2026-09-06 – 2026-09-16 (11 d) |

- **C-SAPR2.** Offline 2025-06-23 to 2026-01-19 "due to serious mechanical issues" (D250710.5) and
  again 2026-01-28 to 2026-06-02 (D260210.2), which records a new pedestal installed in May 2026.
  Since 2026-06-02 differential phase is suspect and the vendor phase products (KDP, PhiDP) are
  flagged incorrect (D260709.9, D260901.43, the latter open-ended). The QC b1 stream
  `bnfcsapr2cfrqcS3.b1` covers only 2025-04-01 to 2025-06-23. The per-scan a1 names in the catalog
  (`bnfcsapr2cfrppiS3.a1`, `...rhiS3.a1` and others) have no data; all scans are in `bnfcsapr2cfrS3.a1`.
- **SACR.** Both bands share 2025 gaps of 12-13 days (June and July-August, DQR D250627.2 and
  D250812.6). The HSRHIs from 2025-01-06 to 2025-04-01 show tilted clouds (D250402.2, suspect).
- **KAZR.** Chiller hardware work 2025-02-12 to 02-18 (D250224.5), not transmitting
  2025-09-14 to 09-18 (D251104.1).

## Campaigns

ARM field campaigns that list BNF, from the ARM campaign index (`POST /api/es/fc/_search`, 2026-10-20);
`bnf_campaigns.csv` adds co-PIs and AAF platform.

| campaign | title | period | lead |
|---|---|---|---|
| JPSSVAL | ARM Radiosondes for JPSS Validation | 2024-02-01 – 2027-12-31 | Borg, Lori |
| APMS-AMF3 | Aerosol mixing state and composition at AMF3 | 2024-10-01 – 2026-07-31 | OBrien, Rachel |
| 2025FICUS10266 | FICUS: Chemical Characterization of SOA | 2024-10-01 – 2026-09-30 | Surratt, Jason |
| 2025FICUS10271 | FICUS: Acquiring Vertical Profiles | 2024-10-01 – 2025-09-30 | Knopf, Daniel |
| 2025FICUS | FICUS: Quantifying the integrated terrestrial | 2024-10-01 – 2026-09-30 | Kuang, Chongai |
| SSNPF | Seasonal/spatial vertical NPF variation study | 2025-03-01 – 2025-11-30 | Zhang, Jie |
| B2NF | Bioaerosol in the Bankhead National Forest | 2025-03-03 – 2025-06-30 | China, Swarup |
| CSSF | Cross-scale Study of Southeastern Forests with UAS | 2025-04-01 – 2028-03-31 | Cushman, KC |
| CONVECT | Radar Studies of Convective Dynamics | 2025-05-01 – 2026-10-30 | Kollias, Pavlos |
| CAFE-BNF | CAnopy Fluxes Experiment - BNF | 2025-05-01 – 2027-12-31 | Liu, Heping |
| FOREST-BIO | Field Observations of Real-time Emissions of Soil and Tree BIOaerosols | 2025-05-07 – 2025-11-28 | China, Swarup |
| CHELAX-BNF | Characterizing HEterogeneous Land-Atmosphere eXchanges at BNF | 2025-06-01 – 2025-06-30 | Juliano, Timothy |
| HAMBAEX | Holographic Aerosol Monitor for Biological Aerosol Experiment | 2025-06-01 – 2026-12-31 | Kuang, Chongai |
| HAIIC | High Altitude Infrared Image Collection | 2025-06-01 – 2026-12-31 | Deng, Xintong |
| ADLO25 | Alternative Doppler Lidar Operations | 2025-06-02 – 2025-06-27 | Juliano, Timothy |
| SHINE | Spatial Heterogeneity in cloud condensation NuclEi | 2025-06-02 – 2025-08-30 | Kulkarni, Gourihar |
| MONET-TAP | Molecular Observation Network- Study Terrestrial-Atmospheric Processes | 2025-08-04 – 2027-09-30 | China, Swarup |
| LASTT-BNF | LAnd-Surface Temperature Transitions at the BNF | 2025-08-06 – 2025-08-25 | Kuang, Chongai |
| MPFCS | Mixed Precursor and Future Climate in SE-US | 2025-08-18 – 2025-09-19 | Salvador, Christian Mark |
| RAPID | Rapid SACR Observations of Convection at BNF | 2025-08-25 – 2026-09-30 | Oue, Mariko |
| IVPFSTIRC | Investigating Vertical Profiles of composition and abundance of Fungal Spores and Their Impacts on Regional Climate | 2025-10-01 – 2026-09-30 | Steiner, Allison |
| CM-BIN | Continuous Measurements of Biological Ice Nuclei | 2025-10-01 – 2028-09-30 | Cornwell, Gavin |
| UFLUX-BNF | Understory Flux Experiment at Bankhead National Forest (UFLUX-BNF) | 2026-02-16 – 2027-02-16 | Liu, Heping |
| EXAER-BNF | Examining AERosols from Bankhead National Forest | 2026-03-01 – 2026-08-31 | Hiranuma, Naruki (seonggi) |
| POLBNF | Pollen Monitoring at BNF | 2026-03-01 – 2026-11-01 | Steiner, Allison |
| VNPF-BNF | Vertical Structure of New Particle Formation and Mixing at the BNF Site | 2026-03-15 – 2026-07-29 | Zhang, Jie |
| COBON | Columnar Bioaerosol and NPF Observations at BNF | 2026-03-15 – 2026-07-28 | Subba, Tamanna |
| MRR-VMIP | MRR Vertical Motion Intercomparison Project | 2026-06-01 – 2027-07-31 | Schumacher, Courtney |
| LEAFF-BNF | Lidar Experiments for Assessing Flow over Forests at BNF | 2026-06-01 – 2027-06-30 | Wharton, Sonia |
| IGNITE | Investigating Gradients of Near-storm Instability and Thermodynamic Evolution | 2026-07-01 – 2027-08-01 | Schiro, Kathleen |
| SOAFA-BVOC | Summer Organic Aerosol Formation Assessment from Biogenic Volatile Organic Compounds | 2026-08-01 – 2026-09-29 | Thornton, Joel |
| SOACAVE | SE U.S. Organic Aerosol Composition and Volatility | 2026-08-01 – 2026-09-25 | Thornton, Joel |
| VIBES | Volatility-resolved Investigation of Bankhead aerosol Evolution and regional Simulation | 2026-09-07 – 2026-09-16 | Laskin, Alexander |
| BNF-WIN | BNF Wintertime Investigation of New Particle Formation | 2026-12-01 – 2027-01-31 | Kuang, Chongai |
| CROPSPEC | Cropland spectral irradiance campaign | 2027-01-04 – 2028-01-07 | OHalloran, Thomas |
| NPF-SEUS | New Particle Formation in the Southeast U.S. | 2027-02-15 – 2027-02-15 | Wang, Jian |
| BINT-BNF | Biological Ice Nuclei Typing at BNF | 2027-03-15 – 2027-08-31 | Cornwell, Gavin |

Field campaign reports with DOIs: APMS-AMF3 interim ([10.2172/2574224](https://doi.org/10.2172/2574224)),
RAPID ([10.2172/3003126](https://doi.org/10.2172/3003126)), LASTT-BNF
([10.2172/3374715](https://doi.org/10.2172/3374715)) and CAFE-BNF interim
([10.2172/3816364](https://doi.org/10.2172/3816364)).

## Getting the data

Datastream names follow `bnf<class><facility>.<level>`, for example `bnfmetM1.b1`. Use
`act.discovery.download_arm_data` with ARM Live credentials (see `act-arm-live`); BNF files mix
`.cdf` and `.nc`. `bnf_datastreams_live(facility="S4")` lists what the catalog holds now, with the
per-datastream source class and `data_available`. Filter on `data_available`: many catalog entries
(the per-scan C-SAPR2 a1 streams, `bnftbsdts*S1.b1`, `bnfcamsceneM1.a1`) are placeholders with end
date equal to the query day and no files. ARM Live queries return at most 10,000 files, so list
SACR days (about 1,250 files per day) a few days at a time. `bnf_file_position(path)` reads the
stored position of any file.

Package notes: ACT 2.3.4 served the downloads; its `get_arm_doi` and the `act-arm-live`
listing helper send a browser user-agent string, so this skill calls the ARM citation service and
ARM Live REST endpoints directly with the default client header. ACT has no file-size or byte-range
probe; ARM Live `saveData` answers `Range` requests, which is how the audit sized files first.

## Data DOIs

Creators as returned by the ARM citation service (spelling as returned).

| datastream | DOI | creators |
|---|---|---|
| `bnfmetM1.b1` | [10.5439/1786358](https://doi.org/10.5439/1786358) | Kyrouac, Shi, Tuftedal |
| `bnfkazr2cfrspcprxpolM1.a1` | [10.5439/1961310](https://doi.org/10.5439/1961310) | Lindenmaier, Matthews, Wendler, Melo de Castro et al. |
| `bnfcsapr2cfrS3.a1` | [10.5439/1467901](https://doi.org/10.5439/1467901) | Bharadwaj, Collis, Hardin, Isom et al. |
| `bnfxsacrcfrS4.a1` | [10.5439/1469303](https://doi.org/10.5439/1469303) | Bharadwaj, Hardin, Isom, Johnson et al. |
| `bnfkasacrcfrspcxpolS4.a1` | [10.5439/1889619](https://doi.org/10.5439/1889619) | Lindenmaier, Matthews, Wendler, Melo de Castro et al. |
| `bnfdlppiM1.b1` | [10.5439/1025186](https://doi.org/10.5439/1025186) | Newsom, Shi, Krishnamurthy |
| `bnfceilM1.b1` | [10.5439/1181954](https://doi.org/10.5439/1181954) | Zhang, Ermold, Morris |
| `bnfmplpolfsextM1.a1` | [10.5439/3402545](https://doi.org/10.5439/3402545) | Muradyan, OBrien, Flynn, Ermold et al. |
| `bnfhsrlscanM1.a1` | [10.5439/2281582](https://doi.org/10.5439/2281582) | Cromwell, Garcia, Bambha |
| `bnfaeriengineerM1.b1` | [10.5439/1989301](https://doi.org/10.5439/1989301) | Gero, Garcia, Hackel, Ermold et al. |
| `bnfmwr3ctipM1.a1` | [10.5439/1973372](https://doi.org/10.5439/1973372) | Cadeddu, Tuftedal |
| `bnfsondewnpnM1.b1` | [10.5439/1595321](https://doi.org/10.5439/1595321) | Keeler, Burk, Kyrouac |
| `bnfsirsS20.b1` | [10.5439/1475460](https://doi.org/10.5439/1475460) | Sengupta, Xie, Jaker, Yang et al. |
| `bnfsebsS10.b1` | [10.5439/1984921](https://doi.org/10.5439/1984921) | Sullivan, Keeler, Pal, Kyrouac |
| `bnftowermet43mS10.a1` | [10.5439/2570718](https://doi.org/10.5439/2570718) | Kyrouac, Tuftedal |
| `bnfldM1.b1` | [10.5439/1973058](https://doi.org/10.5439/1973058) | zhu, Wang, Goncalves Morais, Shi |
| `bnfvdisdropsM1.b1` | [10.5439/1984593](https://doi.org/10.5439/1984593) | zhu, Wang, Goncalves Morais |
| `bnf915rwpwindavgM1.a1` | [10.5439/1572183](https://doi.org/10.5439/1572183) | Muradyan, Ermold |
| `bnfmetS20.b1` | [10.5439/1786358](https://doi.org/10.5439/1786358) | Kyrouac, Shi, Tuftedal |
| `bnfecorsfwindS20.a1` | [10.5439/3375191](https://doi.org/10.5439/3375191) | Sullivan, Cook, Ermold, Keeler et al. |
| `bnfstampS10.b1` | [10.5439/1238260](https://doi.org/10.5439/1238260) | Kyrouac, Cook, Ermold, Pal et al. |
| `bnfaosacsmtofspecM1.a1` | [10.5439/1822138](https://doi.org/10.5439/1822138) | Shilling, Anna, Shippert, Hayes et al. |
| `bnftbswindM1.a1` | [10.5439/1483631](https://doi.org/10.5439/1483631) | Cromwell, Dexheumer, Shi, Whitson |
| `bnfaafnavaimsU2.a1` | [10.5439/1238157](https://doi.org/10.5439/1238157) | Cristina, Mei, Ermold, Mehta |
| `bnfaosccn200M1.a1` | [10.5439/1223287](https://doi.org/10.5439/1223287) | Enekwizu, Koontz, Senum, Andrews et al. |
| `bnfaossmpsM1.a1` | [10.5439/1225453](https://doi.org/10.5439/1225453) | Kuang, Singh, Salwen, Hayes |
| `bnfminiaosmsemsS20.a1` | [10.5439/3006854](https://doi.org/10.5439/3006854) | Singh, Campos |
| `bnfwbpluvio2M1.a1` | [10.5439/1338194](https://doi.org/10.5439/1338194) | Zhu, Wang, Jane, Cromwell et al. |
| `bnfsirsM1.b1` | [10.5439/1475460](https://doi.org/10.5439/1475460) | Sengupta, Xie, Jaker, Yang et al. |

## Verified against

2026-10-20: ARM locations page (13 BNF facility records), ARM catalog index (743 records, 636 BNF
datastreams in 129 classes, 512 of them `armobs`), 145 ARM Live files opened for positions, 4 radar
file records listed day by day, the DQR service, 134 citations from the ARM citation service, and the
ARM campaign index. `tests/test_structure_bnf_site.py` pins every table here to `kernel.py` and the
shipped CSVs; `tests/test_live_bnf.py` re-reads the locations page, the catalog and one file.

## References

- Kuang, C., Giangrande, S. E., Serbin, S. P., Campbell, P., Elsaesser, G. S., Gentine, P., Heus, T., Hickmon, N. L., Oue, M., Peters, J. M., Raghunathan, G. N., Ritsche, M. T., Smith, J. N., Spychala, M., Steiner, A. L., Theisen, A. (2026). The U.S. DOE ARM User Facility Establishes a New Site for Studies of Land-Aerosol-Cloud Interactions in the Southeastern United States. BAMS 107(1). https://doi.org/10.1175/BAMS-D-25-0072.1
- Kuang, C., Giangrande, S., Serbin, S., Elsaesser, G., Gentine, P., Heus, T., Oue, M., Peters, J., Smith, J., Steiner, A., McComiskey, A., Jensen, M., Sedlacek, A., Kollias, P., Vogelmann, A., Morrison, H., Petters, M., Turner, D. (2023). Science Plan for the Deployment of the Third ARM Mobile Facility to the Southeastern United States at the Bankhead National Forest, Alabama (AMF3 BNF). DOE/SC-ARM-23-035. https://doi.org/10.2172/2280575
- Miller, M. A., Nitschke, K., Ackerman, T. P., Ferrell, W. R., Hickmon, N., Ivey, M. (2016). The ARM Mobile Facilities. Meteorological Monographs 57. https://doi.org/10.1175/AMSMONOGRAPHS-D-15-0051.1
- Feng, Y.-C., Theisen, A., Lindenmaier, I., Collis, S., et al. (2023). ARM FY2024 Radar Plan. DOE/SC-ARM-TR-291. https://doi.org/10.2172/2217102
- Feng, Y.-C., Lindenmaier, I., Theisen, A., Wang, D., Collis, S., et al. (2024). ARM FY2025 Radar Plan. DOE/SC-ARM-TR-308. https://doi.org/10.2172/2482518
- Theisen, A., Mayol-Bracero, O., Uin, J., et al. (2023). ARM FY2024 Aerosol Operations Plan. DOE/SC-ARM-TR-289. https://doi.org/10.2172/2008425
- O'Brien, R., Ault, A. (2025). Aerosol Particle Mixing State and Composition at AMF3, Interim Field Campaign Report. https://doi.org/10.2172/2574224
- Oue, M., Freeman, S., Gatlin, P., Kollias, P., et al. (2025). Rapid SACR Observations of Convection at Bankhead National Forest (RAPID) Field Campaign Report. https://doi.org/10.2172/3003126
- Kuang, C., Dexheimer, D., Longbottom, C., et al. (2026). Land-Surface Temperature Transitions at the BNF (LASTT-BNF) Field Campaign Report. https://doi.org/10.2172/3374715
- Liu, H., et al. (2026). Canopy Flux Experiment Bankhead National Forest (CAFE-BNF) Interim Field Campaign Report. https://doi.org/10.2172/3816364
- Pekour, M. CHELAX-BNF: Turbulent Parameters by airborne measurements (dataset), OSTI 2997211. https://www.osti.gov/dataexplorer/biblio/dataset/2997211
- ARM BNF pages: https://www.arm.gov/capabilities/observatories/bnf (science, locations); ARM news posts 99364 (2024 opening approaches), 104580 (2025 operations), 106336 (BNF after one year); BNL news, "Atmospheric Observatory Opens for Operation in Bankhead National Forest" (2024).
