---
name: arm-nsa-site
description: "Reference for the DOE ARM North Slope of Alaska (NSA) observatory at Utqiagvik (formerly Barrow) - site history from 1997, every facility code (C1 Barrow, C2 Atqasuk, E10, E11 Point Barrow, E12 snow array on the BEO, E30 in the NOAA building, S01/S02 sondes, SALVO S10/S11, external X1/X3/X10) with coordinates and which ones to trust, the X-band precipitation radar offset 1.9 km west of C1 on the BARC building, C1-E12-X-SAPR distances, instrument classes per facility with active status, campaigns (SHEBA, M-PACE, ISDAC, ACME V, RIVAL, SALVO), the Kollias 2019 cloud-radar calibration offsets, and ARM data DOIs crediting the mentors. Use for any NSA data request, site map, instrument location, datastream lookup or citation."
---

# ARM North Slope of Alaska (NSA) observatory, Utqiagvik

The NSA observatory is ARM's high-Arctic fixed site. Its main facility, C1, sits on coastal
tundra about 8 km northeast of the town of Utqiagvik, beside NOAA's Barrow Atmospheric
Baseline Observatory (BRW). Companion skills: `utqiagvik-research-assets` (NOAA, NEON,
NGEE Arctic and the other non-ARM assets nearby) and `utqiagvik-site-map` (map layers,
imagery and the figure builder). For instrument physics and per-datastream QC load the
instrument skills, for example `arm-instrument-xsapr`, `arm-instrument-kazr`,
`arm-instrument-kasacr`, `arm-instrument-wsacr`, `arm-instrument-sonde`,
`arm-instrument-maws`, `arm-instrument-ldis` and `arm-instrument-wb`.

At NSA the main facility is **C1**, not M1. M1 is the AMF convention; the Oliktok Point AMF3
deployment used site code `oli` with facility M1, and it is a separate site, not an NSA facility.

## Credit

The site is run by the ARM NSA site operations team. Its design is documented by Stamnes et
al. (1999) and its history reviewed by Verlinde, Zak, Shupe, Ivey and Stamnes (2016). The E12
array and its relationship to C1 are documented by Sturm, Barndt, Delamere and Irving (2025,
DOE/SC-ARM-24-025, [10.2172/2569396](https://doi.org/10.2172/2569396)), UAF Geophysical
Institute. Each ARM datastream has a DOI whose creators are the instrument mentors and data
developers; the table under "Data DOIs" names them. Cite the DOI for every datastream used, and
acknowledge: "Data were obtained from the Atmospheric Radiation Measurement (ARM) User Facility,
a U.S. Department of Energy (DOE) Office of Science user facility managed by the Biological and
Environmental Research program."

## History

- **Concept.** NSA was designed as the North Slope of Alaska and Adjacent Arctic Ocean
  (NSA/AAO) Cloud and Radiation Testbed (Stamnes et al. 1999).
- **Barrow C1, 1997.** The ARM page gives installation in July 1997 and establishment on
  1997-12-11; the first C1 data (ceilometer) start that day. The Adjacent Arctic Ocean
  component was the SHEBA ice camp, October 1997 to October 1998 (Uttal et al. 2002).
- **Atqasuk C2, 1999-2011.** Established 1999-08-21 and removed 2011-01-17, about 99 km SSW
  of C1. It is often quoted as starting in 2000, but the page and the first C2 files
  (nsaceilC2.b1 from 1999-08-22) say 1999.
- **Land.** C1 lies east of the former Naval Arctic Research Laboratory (NARL, 1947-1981),
  whose campus passed to the Ukpeagvik Inupiat Corporation (UIC). UIC set aside the 7,466-acre
  Barrow Environmental Observatory (BEO) in 1992; E12 is "at BEO".
- **ARRA upgrades, 2010-2011.** Ivey et al. (2011, ASR poster) list the X-SAPR on the Barrow
  Arctic Research Center (BARC) mezzanine, the KAZR (a modified MMCR), the SACRs, the HSRL, an
  ER-AERI, and a remote ECOR at Point Barrow (E11). Catalog start dates are KAZR 2011-05-12,
  KaSACR/WSACR 2011-06, X-SAPR 2011-06-24 and E11 SEBS 2011-03-03.
- **Radar generations.** MMCR 1998-03 to 2011-03. KAZR from 2011, with KAZR2 datastreams
  (nsakazr2cfr*) from 2019-12. The first SACRs ran 2011-2015, then KaSACR2/WSACR2 from
  2022-10-07. The legacy X-SAPR PPIs run 2011-2016, with raw data to 2020-02. XSAPR-1 in CF/Radial
  mode (nsaxsaprcfrC1.a1) runs from 2023-05-30.
- **NOAA co-location.** BRW was established in 1973 next to the site. NOAA aerosol data enter
  ARM as external facility X3 (from 2020-10-22). ARM's own aerosol instruments (ACSM, APS) went
  into the new NOAA building as E30 in mid-2024.
- **E12, 2022.** The snow-monitoring array that ran at Oliktok Point from April 2017 to June
  2021 was moved to E12 (Sturm et al. 2025). The page gives E12 as established 2022-01-25.

## Facilities

From the ARM locations page and the ARM catalog, read 2026-10-19. The class counts are
instrument classes in the shipped `nsa_instruments.csv`, which also lists the datastreams.
"Active" means the catalog end date is on or after 2026-08-01. An end date of 2026-10-19 (the
query day) is an open-ended placeholder.

| code | what it is | lat | lon | period (page) | classes | active |
|---|---|---|---|---|---|---|
| C1 | Central Facility, Barrow - the main site on the tundra east of the former NARL campus | 71.323 | -156.615 | 1997-12-11 – 2026-10-19 | 95 | 46 |
| C2 | Central Facility, Atqasuk - about 99 km SSW of C1, near the Atqasuk airport and Meade River | 70.4718 | -157.407 | 1999-08-21 – 2011-01-17 | 22 | 0 |
| E10 | Not a site: a catch-all code for C1-area instruments that are not co-located (SEBS/LPM and ECOR-SF sit about 250 m apart); the page repeats the C1 coordinate | 71.323 | -156.615 | 2011-01-01 – 2026-10-19 | 5 | 4 |
| E11 | Point Barrow remote ECOR/SEBS on the spit | 71.393 | -156.422 | 2011-01-01 – 2026-10-19 | 3 | 1 |
| E12 | Snow-monitoring array on the Barrow Environmental Observatory, along Cake Eater Road | 71.27473611 | -156.64119444 | 2022-01-25 – 2026-10-19 | 9 | 9 |
| E30 | ARM aerosol instruments in the new NOAA GML BRW building | 71.32312 | -156.61143 | 2024-07-01 – 2026-10-19 | 4 | 3 |
| F1 | ARM-ACME V Gulfstream-159 aircraft campaign; coordinate is a C1 placeholder | 71.323 | -156.615 | 2015-06-01 – 2015-09-15 | 15 | 0 |
| S01 | Supplemental sonde launches and a sky-radiometer stand at C1 | 71.323 | -156.615 | 2015-02-04 – 2026-10-19 | 2 | 2 |
| S02 | RIVAL radiosonde intercomparison | 71.323 | -156.609 | 2017-06-01 – 2026-10-19 | 1 | 0 |
| S1 | 1999 IOP, Barrow | — | — | 1999-01-28 – 1999-04-09 | 0 | 0 |
| S2 | 1999 IOP, Atqasuk | — | — | 1999-05-20 – 1999-10-18 | 0 | 0 |
| S10 | SALVO tundra site, about 2 km south of C1 | — | — | 2019-05-01 – 2021-07-20 | 0 | 0 |
| S11 | SALVO sea-ice site, about 2 km north of C1 | — | — | 2019-05-01 – 2021-07-20 | 0 | 0 |
| X1 | External data: satellites, NOAA products, models | — | — | 2011-09-01 – 2021-09-01 | 22 | 4 |
| X3 | NOAA GML BRW aerosol system (external) | 71.32312 | -156.61143 | 2020-10-22 – 2026-10-17 | 6 | 6 |
| X10 | NWS Utqiagvik upper-air soundings (external) | 71.281 | -156.789 | 1996-03-31 – 2016-07-31 | 1 | 0 |

Active classes at C1 (46): aeri, aerinf, aod-mfrsr, aod-nimfr, armtraj, asi, caminst, camsite, ceil, ceilpblht, cloudradarcor, csphot, dl, dlprof-wind, dlprof-wstats, gndrad, hsrl, interpsonde, irt, kasacr, kazr, ldis, masc, maws, met, mfr, mfrsr, mfrsrcip, mpl, mwr, mwr3c, mwrret, nimfr, pblht, precipbe, precipip, qcrad, sirs, skyrad, sonde, sonicwind, spmf, srs, twr, wsacr, xsapr.

E12 (all 9 active): caminst, camsite, ldis, maws, metwxt, sonicwind, spmf, srs, wb. E30: acsm,
acsmcdce, aps. E10: caminst, ecor, ldis, sebs.

`nsa_facilities()` returns these records, and `nsa_instruments(facility, active)` filters the
table.

## Coordinates: which to trust

ARM publishes more than one position for the same thing, and most C1 files cannot place an
individual instrument. Positions used by `nsa_positions()`:

| key | lat | lon | source | what it is |
|---|---|---|---|---|
| c1_page | 71.323 | -156.615 | locations page | the C1 facility coordinate |
| c1_file | 71.323 | -156.609 | 26 C1 datastreams | site-nominal value most C1 files store, 215 m east of c1_page |
| dl | 71.322947 | -156.61609 | nsadlppiC1.b1 (float64) | Doppler lidar, 39 m from c1_page |
| aeri | 71.32326 | -156.60805 | nsaaerisummaryC1.b1 | AERI, alt 28 m |
| e10_ecor | 71.32436 | -156.61482 | nsaecorsfE10.b1 | ECOR smart-flux, 152 m north of c1_page |
| e10_sebs | 71.325 | -156.608 | nsasebsE10.b1 | SEBS, 3 decimal places |
| e30_aos | 71.32312 | -156.61143 | nsaaosapsE30.b1 | NOAA GML BRW building (NAD83) |
| xsapr | 71.324745 | -156.66774 | nsaxsaprcfrC1.a1 | X-SAPR on the BARC building, alt 17 m |
| e12 | 71.274734 | -156.64119 | nsamawsE12.b1 (float32) | E12 snow array; the page gives 71.27473611, -156.64119444 |
| e11 | 71.393 | -156.422 | nsasebsE11.b1 | Point Barrow; equals the page value |
| sonde | 71.32 | -156.62 | nsasondewnpnC1.b1 | launch point stored to 0.01 degrees only |
| cimel | 71.3122 | -156.665 | nsacsphotsdalunarfiltv3C1.a1 | carries the AERONET "Barrow" coordinate, 2.16 km WSW of c1_page |
| nws_x10 | 71.281 | -156.789 | nsanwsupa1sX10.b1 | NWS release location attribute |
| c2 | 70.4718 | -157.407 | nsametC2.b1 | Atqasuk C2 met, equals the page value |

Distances by `nsa_distance()` (WGS84 Vincenty, which agrees with pyproj to the metre):

| leg | distance | bearing |
|---|---|---|
| C1 → E12 | 5.47 km | 190° |
| C1 → X-SAPR | 1.90 km | 276° |
| E12 → X-SAPR | 5.66 km | 350° |
| C1 → E11 | 10.41 km | 41° |
| C1 → C2 | 99.28 km | 197° |

C1 here means c1_page. Measured from c1_file instead, every leg moves by up to 215 m.

**The X-band precipitation radar is not at C1.** XSAPR-1 is filed under facility C1, but its
files put it on the BARC/UIC-NARL building, 1.9 km west, about 30 m from the INTERACT BARC
station coordinate (71.32495, -156.66741). Any range-azimuth geometry over C1, E12 or the
town must use the file's lat/lon/alt, not the facility coordinate. The legacy (2011-2016)
X-SAPR files return HTTP 404 from ARM Live, so their position is unverified; the ARRA poster
places that radar on the same BARC mezzanine. Read the position from one file:

```python
import os

import act
import xarray as xr

files = act.discovery.download_arm_data(
    os.environ["ARMUSER"], os.environ["ARMTOKEN"], "nsaxsaprcfrC1.a1",
    "2025-07-15", "2025-07-15", time="000008")
assert files, "ARM Live returned no file"
with xr.open_dataset(files[0]) as ds:
    print(float(ds["lat"]), float(ds["lon"]), float(ds["alt"]))
# 71.32474517822266 -156.66773986816406 17.0   (float32; one 15 MB file, run 2026-10-19)
```

`nsa_file_position(path)` does the same for any ARM file, looking in variables and then in
global attributes.

**E12.** Sturm et al. (2025) place E12 "5.4 km south along Cake Eater Road" from C1 and say
its layout is similar to the C1 array (nine sonic sounders on swing sets within about 15 m,
shielded and unshielded laser precipitation monitors about 16 m apart, an SPMF blowing-snow
sensor, a heated 3-D sonic, steerable cameras, plus a heated Geonor in a double-Alter shield
at E12 only). **The report gives no numeric coordinates, and the sub-array positions are not
published.** All five E12 files opened carry the same coordinate, so no public source places
the individual E12 instruments.

## Location audit (2026-10-19)

The most recent file of one datastream per instrument class per facility was opened through ARM
Live (b1 preferred, then a1/c1; a0, 00 and the F1 aircraft skipped), and its lat/lon/alt was read
from variables or global attributes. The result ships as `nsa_location_audit.csv`
(`nsa_location_audit()`), one row per datastream with file, date, position, dtype, offset from the
facility's page coordinate and a flag. Of 162 datastreams, 137 files carry a position:

| flag | datastreams |
|---|---|
| C1 nominal | 66 |
| instrument-specific or facility value | 59 |
| rounded to 0.01 deg | 10 |
| no position: not netCDF (movie, image or tar) | 8 |
| no position: file over 250 MB cap | 5 |
| no position: netCDF4-python cannot open the file | 5 |
| no position: no lat/lon in file | 4 |
| no position: ARM Live refuses the datastream (HTTP 403) | 2 |
| bad: 0,0 | 1 |
| bad: longitude sign (east) | 1 |
| no position: no files in the last year of record | 1 |

"C1 nominal" files cannot place an instrument. The positions table above lists the ones that can.
The 250 MB per-file cap excluded the HSRL, whose last a1 files date from 2019-07-11.

## Campaigns

| campaign | period | facility | reference |
|---|---|---|---|
| SHEBA (AAO component) | Oct 1997 – Oct 1998 | ice camp | Uttal et al. 2002 |
| IOPs | 1999-01-28 – 04-09 / 1999-05-20 – 10-18 | S1 Barrow / S2 Atqasuk | locations page |
| M-PACE | autumn 2004 | C1, C2 | Verlinde et al. 2007 |
| ISDAC | April 2008 | C1 | McFarquhar et al. 2011 |
| ARM-ACME V | 2015-06-01 – 09-15 | F1 | Biraud 2016 |
| RIVAL | 2018-02-27 – 2019-10-20 | S02 | Borg et al. 2022 |
| SALVO | 2019-05 – 2021-07 | S10 tundra, S11 sea ice | Delamere et al. 2025 |
| POPEYE | 2016 – 2018 | Oliktok (`oli`), not NSA | de Boer et al. 2018, 2019 |

The ARM campaign index is client-rendered and was not parsed, so this list is not exhaustive.

## Cloud-radar calibration at NSA

Kollias, Puigdomenech Treserras and Protat (2019) calibrated the 2007-2017 ARM cloud-radar record
against CloudSat. At NSA they found that the MMCR mode 2 needed -4.4 to -8.4 dB in 2008-2009,
which they attribute to waveguide corrosion at the antenna feed. The KAZR MD mode was within 1 dB
in 2012-2013, then offset +3 to +6 dB over 2014-2017, with GE minus MD about -1.7 dB.
The correction is operationalised in the KAZR-ARSCL CloudSat VAP (`arm-vap-kazrarsclcloudsat`,
Johnson et al. 2022). Any multi-year NSA reflectivity statistic needs it.

## Getting the data

Datastream names follow `nsa<class><facility>.<level>`, for example `nsametC1.b1`,
`nsamawsE12.b1` and `nsaxsaprcfrqcC1.b1`. Use `act.discovery.download_arm_data` with ARM Live
credentials (see `act-arm-live`). `nsa_datastreams_live(facility="E12")` lists what the catalog
holds now. Day sizes vary a lot: X-SAPR runs about 1.2 GB per day, so fetch a single file with
`time=` when only the header is needed.

## Traps

- Do not plot instruments at the C1 facility coordinate. Most C1 files store the nominal
  71.323, -156.609; only the instruments in the positions table carry their own coordinate.
- E10 is not a site. It is a catch-all code for instruments around C1 that are not co-located,
  so never draw or label it as one place. Its files put SEBS/LPM at 71.325, -156.608 and the
  ECOR-SF at 71.32436, -156.61482, about 250 m apart, while the page repeats the C1 coordinate.
- S10 and S11 are 0,0 on the page and S1, S2 and X1 are null. Treat these as missing, never as
  a position.
- Sonde files store the launch point to 0.01 degrees (about 380 m from C1), and the C1 sonde
  class start date in the catalog is a 1970-01-01 placeholder.
- The page flags E11 and S02 is_active although their data ended (E11 SEBS 2016-10-07, the
  RIVAL sondes 2019). Check the datastream end dates.
- The Cimel sun-photometer file carries the AERONET "Barrow" coordinate, 2.16 km WSW of C1.
  Do not take it as where the ARM photometer sits without checking.
- Bad position metadata found by the audit: `isssonde` (C1, to 2002) stores 0,0, and `varanal`
  stores longitude +156.4 (east, wrong sign).
- E11's last files are from 2016-12 even though the catalog lists `nsaecorwindE11.a1` to
  2026-08-15.
- `X10` is the NWS upper-air record (WMO 70026) re-served by ARM; it has no ARM DOI.

## Data DOIs

DataCite creators are the instrument mentors, translators and developers; credit them.

| datastream | DOI | creators |
|---|---|---|
| `nsa30ecorE11.b1` | [10.5439/1025039](https://doi.org/10.5439/1025039) | Sullivan, Billesbach, Keeler, Ermold et al. |
| `nsaaerisummaryC1.b1` | [10.5439/1989300](https://doi.org/10.5439/1989300) | Gero, Gaustad, Ermold, Hackel et al. |
| `nsaaosapsE30.b1` | [10.5439/1407135](https://doi.org/10.5439/1407135) | Singh, Oliveira, Koontz, Sedlacek et al. |
| `nsaaosnephdryX3.b1` | [10.5439/1228051](https://doi.org/10.5439/1228051) | Koontz, Flynn, Uin, Jefferson et al. |
| `nsaasicldmaskC1.b1` | [10.5439/3005849](https://doi.org/10.5439/3005849) | Silber, Flynn, Cromwell, Ermold |
| `nsaceil10mC1.b1` | [10.5439/1497398](https://doi.org/10.5439/1497398) | Zhang, Morris, Ermold |
| `nsaceilpblhtC1.b1` | [10.5439/1888170](https://doi.org/10.5439/1888170) | Zhang, Morris, Shi, Ermold |
| `nsacsphotsdalunarfiltv3C1.a1` | [10.5439/2202682](https://doi.org/10.5439/2202682) | Ma |
| `nsadlppiC1.b1` | [10.5439/1963410](https://doi.org/10.5439/1963410) | Shi, Newsom |
| `nsaecorsfE10.b1` | [10.5439/1494128](https://doi.org/10.5439/1494128) | Sullivan, Cook, Shi, Keeler et al. |
| `nsagndirtC1.b1` | [10.5439/1366509](https://doi.org/10.5439/1366509) | Howie, Shi, Goldberger, Morris |
| `nsagndrad60sC1.b1` | [10.5439/1377837](https://doi.org/10.5439/1377837) | Sengupta, Habte, Andreas, Reda et al. |
| `nsakasacr2cfrC1.a1` | [10.5439/1890472](https://doi.org/10.5439/1890472) | Feng, (Andrei), Nelson, Johnson et al. |
| `nsakazrcfrgeC1.a1` | [10.5439/1498936](https://doi.org/10.5439/1498936) | Isom, Nelson, (Andrei), Hardin et al. |
| `nsalpmC1.b1` | [10.5439/3008898](https://doi.org/10.5439/3008898) | Sturm, Delamere, Cromwell, Wang et al. |
| `nsamascC1.b1` | [10.5439/1234550](https://doi.org/10.5439/1234550) | Stuefer, Ermold, Shkurko, Wong |
| `nsamawsC1.b1` | [10.5439/1162061](https://doi.org/10.5439/1162061) | Keeler, Kyrouac, Ermold |
| `nsametC1.b1` | [10.5439/1786358](https://doi.org/10.5439/1786358) | Kyrouac, Shi, Tuftedal |
| `nsamfr7nch10mC1.b1` | [10.5439/1773175](https://doi.org/10.5439/1773175) | Hodges, Sheffer, Herrera, Ermold |
| `nsamfrsr7nchC1.b1` | [10.5439/1429369](https://doi.org/10.5439/1429369) | Hodges, Sheffer, Herrera, Ermold |
| `nsaminimplC1.b1` | [10.5439/2401652](https://doi.org/10.5439/2401652) | Flynn, Muradyan, Ermold, OBrien |
| `nsamwr3cC1.b1` | [10.5439/1025248](https://doi.org/10.5439/1025248) | Cadeddu, Gibler, Koontz, Tuftedal |
| `nsamwrlosC1.b1` | [10.5439/1999490](https://doi.org/10.5439/1999490) | Cadeddu, Tuftedal |
| `nsanimfr7nchC1.b1` | [10.5439/1827212](https://doi.org/10.5439/1827212) | Hodges, Herrera, Ermold |
| `nsaprecipipmpC1.a1` | [10.5439/1489525](https://doi.org/10.5439/1489525) | Cromwell, Wong, Bliven, Stuefer et al. |
| `nsasebsE10.b1` | [10.5439/1984921](https://doi.org/10.5439/1984921) | Sullivan, Keeler, Pal, Kyrouac |
| `nsasirsC1.b1` | [10.5439/1475460](https://doi.org/10.5439/1475460) | Sengupta, Xie, Jaker, Yang et al. |
| `nsaskyrad60sC1.b1` | [10.5439/1377836](https://doi.org/10.5439/1377836) | Sengupta, Habte, Andreas, Reda et al. |
| `nsasondewnpnC1.b1` | [10.5439/1595321](https://doi.org/10.5439/1595321) | Keeler, Burk, Kyrouac |
| `nsasonicwind3dC1.b1` | [10.5439/3008892](https://doi.org/10.5439/3008892) | Sturm, Delamere, Cromwell, Irving et al. |
| `nsaspmfC1.b1` | [10.5439/3008879](https://doi.org/10.5439/3008879) | Sturm, Delamere, Cromwell, Irving et al. |
| `nsasrsC1.a1` | [10.5439/1374062](https://doi.org/10.5439/1374062) | Cromwell, Delamere, Sturm, Irving et al. |
| `nsatwrC1.b1` | [10.5439/1989297](https://doi.org/10.5439/1989297) | Kyrouac, Tuftedal |
| `nsawbgeonorE12.a1` | [10.5439/1393925](https://doi.org/10.5439/1393925) | Cromwell, Delamere, Wang, Sturm et al. |
| `nsawsacr2cfrC1.a1` | [10.5439/1890470](https://doi.org/10.5439/1890470) | Feng, (Andrei), Nelson, Johnson et al. |
| `nsaxsaprcfrC1.a1` | [10.5439/1463663](https://doi.org/10.5439/1463663) | Bharadwaj, Hardin, Isom, Johnson et al. |
| `nsaxsaprcfrqcC1.b1` | [10.5439/3013114](https://doi.org/10.5439/3013114) | Rocque, Schuman, Feng, Matthews et al. |

## Verified against

2026-10-19: ARM locations page (13 NSA facility records), ARM catalog index (743 records,
1099 NSA datastreams), 49 ARM Live files opened for coordinates and a 162-datastream
most-recent-file location audit, 37 DataCite DOIs resolved, and
20 literature DOIs checked on Crossref. `tests/test_structure_nsa.py` pins the facility table,
the positions, the distance table and the class counts to `kernel.py` and `nsa_instruments.csv`.
`tests/test_live_nsa.py` re-reads the locations page and the catalog.

## References

- Ackerman, Thomas P.; Cress, Ted S.; Ferrell, Wanda R.; Mather, James H.; Turner, David D. (2016). The Programmatic Maturation of the ARM Program. Meteorological Monographs. https://doi.org/10.1175/amsmonographs-d-15-0054.1
- Ackerman, Thomas P.; Stokes, Gerald M. (2003). The Atmospheric Radiation Measurement Program. Physics Today. https://doi.org/10.1063/1.1554135
- Biraud, Sebastien (2016). ARM-ACME V: ARM Airborne Carbon Measurements V on the North Slope of Alaska Field Campaign Report. DOE/OSTI report. https://doi.org/10.2172/1253896
- Borg, Lori; Dirksen, Ruud; Fasso, Alessandro; Gardiner, Tom; Jauhiainen, Hannu; Querel, Richard; Reale, Tony; Thorne, Peter; Tobin, David; Wang, June (2022). Radiosonde Intercomparison and Validation (RIVAL) Field Campaign Report. DOE/OSTI report. https://doi.org/10.2172/1894500
- de Boer, Gijs (2018). Profiling at Oliktok Point to Enhance Year of Polar Prediction Experiments (POPEYE) Science Plan. DOE/OSTI report. https://doi.org/10.2172/1439593
- de Boer, Gijs; Dexheimer, Darielle; Mei, Fan; Hubbe, John; Longbottom, Casey; Carroll, Peter J.; Apple, Monty; Goldberger, Lexie; Oaks, David; Lapierre, Justin; Crume, Michael; Bernard, Nathan; Shupe, Matthew D.; Solomon, Amy; Intrieri, Janet; Lawrence, Dale; Doddi, Abhiram; Holdridge, Donna J.; Hubbell, Michael; Ivey, Mark D.; Schmid, Beat (2019). Atmospheric observations made at Oliktok Point, Alaska, as part of the Profiling at Oliktok Point to Enhance YOPP Experiments (POPEYE) campaign. Earth System Science Data. https://doi.org/10.5194/essd-11-1349-2019
- Delamere, J.; Sturm, M.; Perovich, D.; Webster, M.; Pinzer, A.; Wilson, P.; Oggier, M.; Clemens-Sewall, D.; Chapman-Dutton, H; Espinosa, Z.; Grams, T.; Larson, O.; Mayo, E.; Wesen, S.; Shean, D.; Warren, S. (2025). The Snow Albedo Evolution (SALVO) Campaign at the North Slope of Alaska Field Campaign Report. DOE/OSTI report. https://doi.org/10.2172/3018052
- Desilets, Darin; Helsel, Fred; Bendure, Al; Lucero, Daniel; Ivey, Mark; Dexheimer, Danielle (2016). Visitor’s Guide to Oliktok Point Atmospheric Radiation Measurement Climate Research Facility, North Slope of Alaska. DOE/OSTI report. https://doi.org/10.2172/1253899
- Johnson, Karen; Giangrande, Scott; Zhou, Aifang (2022). Ka-Band ARM Zenith Radar (KAZR) Active Remote Sensing of Clouds (ARSCL) CloudSat Calibration (KAZRARSCL-CLOUDSAT) (Value-Added Product Report). DOE/OSTI report. https://doi.org/10.2172/1847644
- Kollias, Pavlos; Bharadwaj, Nitin; Widener, Kevin; Jo, Ieng; Johnson, Karen (2014). Scanning ARM Cloud Radars. Part I: Operational Sampling Strategies. Journal of Atmospheric and Oceanic Technology. https://doi.org/10.1175/jtech-d-13-00044.1
- Kollias, Pavlos; Puigdomènech Treserras, Bernat; Protat, Alain (2019). Calibration of the 2007–2017 record of Atmospheric Radiation Measurements cloud radar observations using CloudSat. Atmospheric Measurement Techniques. https://doi.org/10.5194/amt-12-4949-2019
- Mather, James H.; Voyles, Jimmy W. (2013). The Arm Climate Research Facility: A Review of Structure and Capabilities. Bulletin of the American Meteorological Society. https://doi.org/10.1175/bams-d-11-00218.1
- McFarquhar, Greg M.; Ghan, Steven; Verlinde, Johannes; Korolev, Alexei; Strapp, J. Walter; Schmid, Beat; Tomlinson, Jason M.; Wolde, Mengistu; Brooks, Sarah D.; Cziczo, Dan; Dubey, Manvendra K.; Fan, Jiwen; Flynn, Connor; Gultepe, Ismail; Hubbe, John; Gilles, Mary K.; Laskin, Alexander; Lawson, Paul; Leaitch, W. Richard; Liu, Peter; Liu, Xiaohong; Lubin, Dan; Mazzoleni, Claudio; Macdonald, Ann-Marie; Moffet, Ryan C.; Morrison, Hugh; Ovchinnikov, Mikhail; Shupe, Matthew D.; Turner, David D.; Xie, Shaocheng; Zelenyuk, Alla; Bae, Kenny; Freer, Matt; Glen, Andrew (2011). Indirect and Semi-direct Aerosol Campaign. Bulletin of the American Meteorological Society. https://doi.org/10.1175/2010bams2935.1
- Stamnes, K.; Ellingson, R. G.; Curry, J. A.; Walsh, J. E.; Zak, B. D. (1999). Review of Science Issues, Deployment Strategy, and Status for the ARM North Slope of Alaska–Adjacent Arctic Ocean Climate Research Site. Journal of Climate. https://doi.org/10.1175/1520-0442-12.1.46
- Sturm, Matthew; Barndt, William; Delamere, Jenifer; Irving, Ken (2025). Assessment of North Slope of Alaska (NSA) Snow Monitoring Arrays. DOE/OSTI report. https://doi.org/10.2172/2569396
- Turner, D. D.; Ellingson, R. G. (2016). Introduction. Meteorological Monographs. https://doi.org/10.1175/amsmonographs-d-16-0001.1
- Uttal, Taneil; Curry, Judith A.; Mcphee, Miles G.; Perovich, Donald K.; Moritz, Richard E.; Maslanik, James A.; Guest, Peter S.; Stern, Harry L.; Moore, James A.; Turenne, Rene; Heiberg, Andreas; Serreze, Mark C.; Wylie, Donald P.; Persson, Ola G.; Paulson, Clayton A.; Halle, Christopher; Morison, James H.; Wheeler, Patricia A.; Makshtas, Alexander; Welch, Harold; Shupe, Matthew D.; Intrieri, Janet M.; Stamnes, Knut; Lindsey, Ronald W.; Pinkel, Robert; Pegau, W. Scott; Stanton, Timothy P.; Grenfeld, Thomas C. (2002). Surface Heat Budget of the Arctic Ocean. Bulletin of the American Meteorological Society. https://doi.org/10.1175/1520-0477(2002)083<0255:shbota>2.3.co;2
- Verlinde, J.; Harrington, J. Y.; McFarquhar, G. M.; Yannuzzi, V. T.; Avramov, A.; Greenberg, S.; Johnson, N.; Zhang, G.; Poellot, M. R.; Mather, J. H.; Turner, D. D.; Eloranta, E. W.; Zak, B. D.; Prenni, A. J.; Daniel, J. S.; Kok, G. L.; Tobin, D. C.; Holz, R.; Sassen, K.; Spangenberg, D.; Minnis, P.; Tooman, T. P.; Ivey, M. D.; Richardson, S. J.; Bahrmann, C. P.; Shupe, M.; DeMott, P. J.; Heymsfield, A. J.; Schofield, R. (2007). The Mixed-Phase Arctic Cloud Experiment. Bulletin of the American Meteorological Society. https://doi.org/10.1175/bams-88-2-205
- Verlinde, J.; Zak, B. D.; Shupe, M. D.; Ivey, M. D.; Stamnes, K. (2016). The ARM North Slope of Alaska (NSA) Sites. Meteorological Monographs. https://doi.org/10.1175/amsmonographs-d-15-0023.1
- Ivey, M., J. Zirzow, F. Helsel, V. Sparks, J. Verlinde, S. Richardson, M. Stuefer, J. Cherry (2011). ARRA Upgrades on the North Slope of Alaska – Barrow. ASR Science Team Meeting poster P000281 (no DOI).
