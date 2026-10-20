---
name: bnf-research-assets
description: "Inventory of the non-ARM observing and context assets around the DOE ARM Bankhead National Forest (BNF) site in northern Alabama, with operator-sourced coordinates and geodesic distance/bearing from M1 - NWS WFO Huntsville, WSR-88Ds KGWX KHTX KBMX KOHX KMXX KNQA KHPX and TDWRs, ASOS/AWOS (KDCU, KMSL, KHSV, 1M4, 9A4, KCMD, KJFX), COOP, USRCRN/USCRN, BMX and OHX radiosondes, NSF NEON Domain 08 (TALL, MAYF, DELA, LENO, BLWA, TOMB), the 14 NALMA lightning stations, UAH ARMOR, NOAA PSL Courtland profiler, IMPROVE SIPS1 (co-located with M1), EPA AQS and CASTNET, AERONET, AmeriFlux, NRCS SCAN, USGS stream gauges, USFS Bankhead Ranger District and Sipsey Wilderness, Wheeler NWR, TVA and Alabama Power reservoirs, and Census GEOIDs for host counties and towns. Use for co-location questions, picking a comparison dataset near BNF, site maps, or crediting the networks."
---

# Research assets around ARM BNF (non-ARM)

Everything here lies outside the DOE ARM program. The ARM facilities themselves are covered by
`arm-bnf-site`, and the map layers by `bnf-site-map`. The table ships as `bnf_region_assets.csv`
(104 rows, compiled 2026-10-20). Each row carries the operator, network, ids, status, coordinate
precision, source URL and access date, plus the WGS84 geodesic distance and initial bearing from M1
(34.342481, -87.338177, the ARM locations-page point) and the nearest ARM BNF facility.

```python
bnf_assets(operator="NOAA", within_km=80)   # substring filters, nearest first
bnf_assets(network="NEXRAD")                # also asset_type=...
assets_near(34.653784, -87.292676, km=6)    # anything within 6 km of a point (here ARM S20)
from_m1(lat, lon)                           # (km, deg), as rounded in the CSV
nearest_arm(lat, lon)                       # (facility, km) over M1 S3 S4 S10 S20 S30 S40 U2
nws_radar_live("KHTX"); homr_station_live("ICAO:KDCU"); neon_location_live("TOWER100876")
nalma_stations("NALMA_261016_235000_0600.dat.gz")   # Sta_info table from any NALMA L1 file
```

`geodesic_inverse` is a stdlib Vincenty solver, tested against pyproj. The `agency` column groups
operators (NOAA covers NWS, NCEI and PSL; FAA covers AWOS; USDA covers NRCS and USFS).

| agency | rows |
|---|---|
| NOAA | 27 |
| Census | 17 |
| NASA | 17 |
| USDA | 11 |
| FAA | 6 |
| NSF | 6 |
| USGS | 5 |
| DOE | 4 |
| EPA | 4 |
| Alabama Power | 2 |
| NPS | 1 |
| FWS | 1 |
| TVA | 1 |
| UAH | 1 |
| DoD | 1 |

## Setting

- **M1 shares a compound with two long-running records.** IMPROVE SIPS1 (AQS 01-079-0002, established
  1992-03-07 at the USFS Black Warrior Work Center on Hwy 33, north of Grayson) is 0.15 km from M1.
  The HADS station BHFA1 "Bankhead National Forest" is 0.19 km from M1. BHFA1 is probably the USFS
  fire-weather RAWS, but RAWS metadata was not checked. M1 is inside the Bankhead Ranger District
  boundary and 1.48 km outside the Sipsey Wilderness, so SIPS1 represents the wilderness from outside
  it.
- **ARM S40 (Double Springs) is at NRCS SCAN 2179 Sudduth Farms** (0.23 km), which gives S40 a soil
  moisture and temperature record from 2010.
- **The Courtland airfield is a cluster:** Courtland AWOS 9A4, USRCRN Courtland 2 WSW, NALMA station K
  and NOAA PSL `ctd` all lie 4.7-5.3 km W of ARM S20.
- The ARM facilities fall in Lawrence County (M1, S3, S4, S10, S20), Morgan (S30) and Winston (S40, U2),
  per TIGERweb point-in-polygon on 2026-10-20. U2 is inside Haleyville city limits; S20 and S30 are
  outside Courtland and Falkville town limits.

| asset | ARM facility | separation |
|---|---|---|
| IMPROVE Sipsey Wilderness (SIPS1) | M1 | 0.15 km |
| HADS DCP Bankhead National Forest (BHFA1) | M1 | 0.19 km |
| NRCS SCAN Sudduth Farms (2179) | S40 | 0.23 km |
| USGS Flint Creek Near Falkville Al (03576500) | S30 | 1.39 km |
| Posey Field AWOS (1M4), Haleyville | U2 | 1.47 km |

## Nearest asset of each class

| class | nearest asset | distance | bearing |
|---|---|---|---|
| WSR-88D radar | WSR-88D KGWX (Columbus AFB) | 103.93 km | 242° |
| TDWR | TDWR TBNA (Nashville) | 191.83 km | 19° |
| NWS ASOS | Decatur Pryor Field ASOS (KDCU) | 50.39 km | 46° |
| AWOS | Posey Field AWOS (1M4), Haleyville | 25.51 km | 251° |
| NWS COOP | NWS COOP Moulton 2 (MOUA1) | 16.58 km | 13° |
| USRCRN | USRCRN Courtland 2 WSW (WBAN 63868) | 35.25 km | 359° |
| USCRN | USCRN Gadsden 19 N (WBAN 63857) | 126.82 km | 92° |
| radiosonde (active) | NWS Birmingham (BMX) upper-air site (WMO 72230) | 138.96 km | 158° |
| NEON site | NEON Mayfield Creek (MAYF) met station | 153.43 km | 182° |
| NALMA station | NALMA station K (courtland) | 34.99 km | 359° |
| AERONET | AERONET UAHuntsville | 76.53 km | 56° |
| NRCS SCAN | NRCS SCAN Sudduth Farms (2179) | 21.07 km | 211° |
| USGS IV gauge | USGS Sipsey Fork Near Grayson Al (02450250) | 8.45 km | 221° |
| IMPROVE | IMPROVE Sipsey Wilderness (SIPS1) | 0.15 km | 288° |
| CASTNET | CASTNET Sand Mountain (SND152) | 126.06 km | 92° |
| NOAA PSL site | NOAA PSL Courtland profiler site (ctd) | 35.24 km | 358° |

## What each asset is and how to get its data

- **NWS.** WFO Huntsville (HUN) serves the whole network from the NSSTC building at UAH. Radars:

| radar | distance | bearing | elevation |
|---|---|---|---|
| WSR-88D KGWX (Columbus AFB) | 103.93 km | 242° | 155 m |
| WSR-88D KHTX (Northeast Alabama) | 132.24 km | 60° | 537.1 m |
| WSR-88D KBMX (Birmingham) | 140.11 km | 158° | 196.6 m |
| TDWR TBNA (Nashville) | 191.83 km | 19° | 249 m |
| WSR-88D KOHX (Nashville) | 222.79 km | 18° | 176.5 m |
| WSR-88D KMXX (Maxwell AFB) | 246.66 km | 144° | 136 m |
| TDWR TMEM (Memphis) | 251.09 km | 285° | 147.2 m |
| WSR-88D KNQA (Memphis) | 257.14 km | 296° | 103 m |
| WSR-88D KHPX (Ft Campbell) | 265.68 km | 1° | 172 m |

  KHTX (Hytop) is the HUN radar; KPAH is 329 km away and was left out. Level II data are on the
  `unidata-nexrad-level2` bucket (see the `nexrad-*` skills). ASOS/AWOS within 80 km come from HOMR
  station records (`homr_station_live`); minute and hourly data come from IEM
  (`mesonet.agron.iastate.edu/cgi-bin/request/asos.py`) or NCEI ISD/GHCNh. COOP rows are IEM
  `AL_COOP` stations within 40 km, excluding two that are USRCRN stations. As of 2026-10-20 IEM `AL_DCP`
  listed 81 HADS DCPs within 80 km of M1, 70 of them online. Only BHFA1 is tabulated; the rest are
  mostly TVA, USGS and Alabama Power river and rain gauges.
- **NCEI climate networks.** Four Alabama USRCRN pilot stations lie within 56 km. They are listed as
  "Experimental/Operational" in `uscrn/products/stations.tsv`, which gives 2-dp coordinates (HOMR gives
  4 dp). The nearest commissioned USCRN station is Gadsden 19 N. USRCRN/USCRN subhourly data:
  `https://www.ncei.noaa.gov/pub/data/uscrn/products/`.
- **Upper air.** BMX (WMO 72230) and OHX (72327) launch twice a day (IGRA2 `USM00072230`,
  `USM00072327`). Redstone Arsenal 74001 is historic (IGRA2 1992-2014).
- **NOAA PSL Courtland (`ctd`)** went in for VORTEX-SE on 2019-11-22 and stayed through PERiLS. It is
  still active, with a 449 MHz profiler, RASS, Parsivel, GPS, radiation and met. Its 915 MHz profiler
  ran 2021-2023. PSL gives only 2-dp coordinates (about 1 km). PSL `win` (Winfield) is in the PSL site
  table with end "TBD". Data: `https://downloads.psl.noaa.gov/psd2/data/realtime/` (for example `Radar449/WwWind/ctd/`).
- **NSF NEON D08.** No NEON site lies inside the BNF network. The nearest is the core pair MAYF (stream)
  and TALL (Talladega tower), about 154 km S. API: `data.neonscience.org/api/v0` (no key). TALL and DELA
  towers are also AmeriFlux US-xTA and US-xDL.
- **NSF campaigns.** VORTEX-SE (2016-2019) and PERiLS (2022-2023) left one fixed asset in the BNF
  footprint, PSL `ctd`. Their mobile north-Alabama deployments (UAH MAX and MoDLS, CLAMPS-2 at Courtland,
  NOAA ATDD flux towers at Belle Mina and Cullman in 2017) are archived at NSF NCAR EOL
  (`data.eol.ucar.edu`), not tabulated here. UAH's NSF-funded MAPNet facility is mobile (four platforms and
  a scanning X-band radar, per the UAH ESSC SWIRLL page) and is based at SWIRLL.
- **NASA / UAH.** NALMA has 14 VHF stations; 9 were active in `NALMA_261016_235000_0600.dat.gz`, and
  the network centre is 34.72461, -86.64533. The nearest stations to BNF are K (courtland), N (landfill)
  and J (hospital), and BNF lies on the network's western edge. Data: CMR collection
  `C2683433889-GHRC_DAAC` (short name `nalma`), Earthdata login required; the station table is in every
  file header (`nalma_stations`). ARMOR (C-band dual-pol, Huntsville International Airport) is cited from
  Wikidata, because the UAH pages returned 404. AERONET `UAHuntsville` is at NSSTC; AERONET also lists
  `ARM_BNF`, which is ARM's own Cimel and is excluded here.
- **Air quality and deposition.** EPA AQS bulk files (`aqs.epa.gov/aqsweb/airdata/aqs_sites.zip`,
  `aqs_monitors.zip`, extract 2026-06-26) need no key. Monitors within 80 km with a sample since 2025-07-01: SIPS1, Decatur
  (O3, PM2.5) and two Huntsville sites. CASTNET SND152 (Sand Mountain, co-located NADP AL99) is the
  nearest dry-deposition site, from `gaftp.epa.gov/castnet/CASTNET_Outgoing/data/site.zip`.
- **Flux.** AmeriFlux registers ARM's own towers as US-BNF (the S10 tower), US-A20, US-A30 and US-A40;
  these are ARM instruments, flagged `DOE`. No non-ARM AmeriFlux site lies within 150 km.
  Site list: `amfcdn.lbl.gov/api/v1/site_display/AmeriFlux`.
- **Soil and water.** NRCS SCAN stations come from the AWDB REST API (elevation in feet, converted).
  USGS IV gauges come from `waterservices.usgs.gov/nwis/site/?bBox=-87.75,34.05,-86.85,34.75&siteType=ST&siteStatus=active&hasDataTypeCd=iv`
  (5 gauges as of 2026-10-20). Flint Creek near Falkville is 1.39 km from S30, and Big Nance Creek at
  Courtland is 2.89 km from S20.
- **Land management.** USFS EDW ArcGIS services give the Bankhead Ranger District polygon (org 080101)
  and the Sipsey Wilderness polygon (25,851 GIS acres). The district office address comes from the USFS
  office page and was geocoded with the Census geocoder. Wheeler NWR, Wheeler Dam (TVA) and Lewis Smith
  Lake and Dam are OSM feature points via Nominatim. **Lewis Smith Lake is an Alabama Power reservoir,
  not TVA.**
- **Census.** TIGERweb current layers (State_County/1, Places/4) give GEOIDs and internal points:

| Census geography | GEOID | distance from M1 |
|---|---|---|
| Addison town | 0100484 | 21.40 km |
| Colbert County | 01033 | 58.39 km |
| Cullman County | 01043 | 49.11 km |
| Franklin County | 01059 | 47.70 km |
| Lauderdale County | 01077 | 68.60 km |
| Lawrence County | 01079 | 20.83 km |
| Limestone County | 01083 | 61.35 km |
| Morgan County | 01103 | 46.90 km |
| Winston County | 01133 | 20.99 km |
| Courtland town | 0118040 | 36.34 km |
| Decatur city | 0120104 | 40.96 km |
| Double Springs town | 0121280 | 21.91 km |
| Falkville town | 0125648 | 39.62 km |
| Haleyville city | 0132704 | 28.41 km |
| Hartselle city | 0133448 | 38.16 km |
| Moulton city | 0151600 | 16.97 km |
| Russellville city | 0167056 | 40.16 km |

## Access record (2026-10-20)

- **Worked by default:** api.weather.gov, NCEI HOMR, IGRA2 and USCRN lists, IEM geojson, NEON, AERONET,
  NRCS AWDB, USGS waterservices, TIGERweb, the Census geocoder, USFS EDW, EPA AQS bulk files, CMR,
  amfcdn.lbl.gov, psl.noaa.gov, Nominatim and Crossref.
- **Needed allowlist grants:** nadp.slh.wisc.edu, gaftp.epa.gov (CASTNET), data.ghrc.earthdata.nasa.gov,
  and the GHRC CloudFront host `d1sd4up8kynpk2.cloudfront.net`. For NALMA, the EDL username/password
  pair was rejected (401) and the EDL bearer token worked.
- **Failed:** the NADP site list loads from an API keyed by a password embedded in page script, so it
  was not used, and NADP AL99 is located only through CASTNET's `NADP_ID`. vista.cira.colostate.edu
  (IMPROVE) serves an incomplete TLS chain. views.cira, www.epa.gov, carto.nationalmap.gov,
  nid.sec.usace.army.mil and api.openstreetmap.org are blocked and were not requested. The GNIS
  (edits.nationalmap.gov) app has no public JSON route. Overpass returned 502 (at capacity).
  `ameriflux-data.lbl.gov` returned 522. UAH SWIRLL pages returned 404.

## Credit

Cite NOAA NWS, NCEI (HOMR, USCRN, IGRA2) and PSL; NSF NEON (operated by Battelle); NASA GHRC with the
NALMA dataset citation (Lang, Blakeslee, Wingo, Rison, Rodeheffer and Krehbiel 2021,
doi:10.5067/NALMA/DATA101); UAH SWIRLL for ARMOR; IMPROVE (NPS and partner agencies, UC Davis
analysis) and EPA AQS/CASTNET; NASA AERONET with the site PI; USDA NRCS SCAN; USGS NWIS; USFS;
AmeriFlux; and the Census Bureau. Use each dataset's own DOI where one is issued.

## Traps

- HOMR puts KCMD at longitude -85.85802, a 1° typo that lands 136 km east. The CSV uses IEM -86.858.
- HOMR gives 1M4 and 9A4 at 3 dp. 1M4 is 1.47 km from U2 by HOMR but 0.24 km by IEM (34.2803, -87.6004).
- KHAB has a 2016-only HOMR record with no platform and is absent from IEM, so its status is unconfirmed.
- The IEM `JFX` name "Manchester" is the Walker County (Jasper) AWOS.
- Nominatim "Wheeler Lake, Alabama" resolves to a pond in Chambers County, and the "Wheeler Reservoir"
  node is in Limestone County; neither is TVA's Wheeler Lake.
- OSM, Wikidata and PSL coordinates are lower confidence (`coord_precision`). Census internal points
  are not town centres.

## Verified against

2026-10-20: all 104 rows from the sources named in `source_url`. `tests/test_structure_bnf_assets.py`
checks every table here against the CSV and the kernel.

## References

* Crum & Alberty (1993) The WSR-88D and the WSR-88D Operational Support Facility. BAMS. https://doi.org/10.1175/1520-0477(1993)074<1669:TWATWO>2.0.CO;2
* Diamond et al. (2013) U.S. Climate Reference Network after One Decade of Operations. BAMS. https://doi.org/10.1175/BAMS-D-12-00170.1
* Durre et al. (2006) Overview of the Integrated Global Radiosonde Archive. J. Climate. https://doi.org/10.1175/JCLI3594.1
* Keller et al. (2008) A continental strategy for the National Ecological Observatory Network. Front. Ecol. Environ. https://doi.org/10.1890/1540-9295(2008)6[282:ACSFTN]2.0.CO;2
* Rison et al. (1999) A GPS-based three-dimensional lightning mapping system. GRL. https://doi.org/10.1029/1999GL010856
* Goodman et al. (2005) The North Alabama Lightning Mapping Array. Atmos. Res. https://doi.org/10.1016/j.atmosres.2004.11.035
* Lang et al. (2021) North Alabama Lightning Mapping Array (LMA). NASA GHRC DAAC. https://doi.org/10.5067/NALMA/DATA101
* Holben et al. (1998) AERONET. Remote Sens. Environ. https://doi.org/10.1016/S0034-4257(98)00031-5
* Malm et al. (1994) Spatial and seasonal trends in particle concentration and optical extinction (IMPROVE). JGR. https://doi.org/10.1029/93JD02916
* Schaefer et al. (2007) The USDA NRCS Soil Climate Analysis Network (SCAN). JTECH. https://doi.org/10.1175/2007JTECHA930.1
* Novick et al. (2018) The AmeriFlux network: a coalition of the willing. Agric. For. Meteorol. https://doi.org/10.1016/j.agrformet.2017.10.009
* Kosiba et al. (2024) The Propagation, Evolution, and Rotation in Linear Storms (PERiLS) Project. BAMS. https://doi.org/10.1175/BAMS-D-22-0064.1
