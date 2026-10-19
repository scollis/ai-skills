---
name: utqiagvik-research-assets
description: "Inventory of the non-ARM research and observing assets around Utqiagvik (formerly Barrow), Alaska, with sourced coordinates - NOAA GML Barrow Atmospheric Baseline Observatory (BRW), BSRN BAR, USCRN 27516, NWS ASOS PABR and the WMO 70026 upper-air site, NSF NEON BARR (tower, hut, megapit, soil plots, 93 observational plots), NGEE Arctic intensive sites A-D, CALM U1, the Barrow Environmental Observatory (BEO), BARC/UIC Science, historic NARL, UAF sea-ice radar and mass-balance site, SIZONet moorings, NOAA CO-OPS gauges, AERONET, EarthScope GNSS, the USGS magnetic observatory and Point Barrow/Nuvuk. Use for site maps, co-location questions, picking a comparison dataset near the ARM NSA site, or citing the networks."
---

# Research assets around Utqiagvik (non-ARM)

Everything here is outside the DOE ARM program; the ARM facilities are in `arm-nsa-site`, and
map layers and the figure builder are in `utqiagvik-site-map`. The table ships as
`utqiagvik_assets.csv` (37 rows, compiled 2026-10-19), and every row records its source URL,
coordinate precision and access date. `utqiagvik_assets(network=..., operator=...)` filters it,
`assets_near(lat, lon, km)` finds co-located assets, and `neon_barr_plots()` returns all 515 NEON
plot-protocol locations (93 plot IDs; `neon_barr_plots.csv`, each row's source being the NEON
locations endpoint for its `neon_location`).

## Credit

The table credits the networks that operate these assets: NOAA GML, NWS, NCEI/USCRN, NOAA CO-OPS,
NSF NEON (operated by Battelle), DOE NGEE Arctic (ORNL-led) with the UAF Permafrost Laboratory,
CALM/GTN-P, the UAF Geophysical Institute Sea Ice Group, Hokkaido University, USGS Geomagnetism,
EarthScope (formerly UNAVCO), NASA AERONET, and UIC Science (Ukpeagvik Inupiat Corporation).
Cite the network papers below and the data DOIs each network issues.

## Setting

- **Utqiagvik** is the North Slope Borough seat. It was incorporated as Barrow in 1958, and voters
  approved restoring the Inupiaq name in October 2016, effective 2016-12-01. The 2020 Census
  counted 4,927 residents, a figure taken from secondary sources because the Census API needs a
  key. The Census internal point (71.2539, -156.7982) lies about 4 km south of downtown, so do
  not use it as the town marker.
- **Point Barrow / Nuvuk** (71.3889, -156.4792) is the northernmost point of the USA. Nuvuk,
  the Thule-era settlement and archaeological site on the spit, was occupied into the 1940s. The
  spit migrates, so that coordinate is good to about 100 m.

## What each asset is

- **NOAA GML BRW, 1973-.** 71.3230, -156.6114, 11 m, about 8 km northeast of town and upwind of it
  in the prevailing ENE flow. It is one of four NOAA baseline observatories, measuring greenhouse
  gases (flasks from 1971, in situ from 1973), halocarbons, aerosols (from 1976), broadband and
  spectral radiation, Dobson ozone, surface ozone and meteorology. The radiation record was BSRN
  station BAR from 1992 until it left BSRN in 2016. ARM serves BRW aerosol data as facility X3,
  and ARM's E30 instruments sit in the new BRW building.
- **NWS.** The Wiley Post-Will Rogers Memorial Airport ASOS (PABR, WBAN 27502) is at 71.28703,
  -156.73938 per the HOMR survey. Twice-daily radiosondes (WMO 70026, IGRA2 USM00070026, from
  1932) launch from the Weather Service Office in town (71.2889, -156.7833). **HOMR attaches WMO
  70026 to the airport station, but the launch site is about 1.6 km away**, so map them as two
  points. ARM re-serves the soundings as `nsanwsupa1sX10.b1` with a third Release_Location
  (71.281, -156.789).
- **USCRN Utqiagvik 4 ENE (WBAN 27516).** 71.3213, -156.611, a climate-reference station: triple
  air temperature, precipitation, wind, radiation and soil temperature. HOMR record from
  2002-08-10, commissioned 2013-07-22 per the USCRN list.
- **NSF NEON BARR (Domain D18 Tundra), 2016-.** The NEON API returned 519 child locations: the
  tower (71.282425, -156.619319, 7.9 m tall with 4 levels), the instrument hut, megapit MP1
  (sampled May 2016), soil plots SP1-SP5 (pinned at polygon centroids) and 93 observational plots
  for vegetation, soils, birds, small mammals, mosquitoes, ticks and phenology. The tower carries
  eddy covariance (from 2017-09), meteorology, soil sensors and a phenocam. All of it lies inside
  the BEO; the tower is 1.16 km NE (042°) of ARM E12.
- **BARC / UIC Science.** The Barrow Arctic Research Center, built in 2007 on the former NARL
  campus (71.32495, -156.66741). UIC Science runs logistics and the BEO; the Barrow Arctic Science
  Consortium (BASC) did so earlier. The ARM X-SAPR is on this building.
- **Barrow Environmental Observatory (BEO), 1992-.** 7,466 acres set aside by UIC, designated a
  Scientific Research District by the North Slope Borough in 2003. The public BAID layer extent is
  71.2565-71.3291 N, 156.6664-156.4078 W. As of 2026-10-19 the polygon query failed with a server
  licence error (9027) and the polygon is not in OSM, so only that bounding box is available. The
  polygon itself is in NSF NCAR EOL dataset 106.ARCSS400, which needs an EOL account.
- **NARL, 1947-1981 (historic).** Founded by the Office of Naval Research in 1947, run by the
  University of Alaska from 1954, and named NARL in 1967. The campus passed to UIC after the Navy
  left in 1980-81 and now hosts Ilisagvik College and BARC.
- **NGEE Arctic.** Intensive Study Site 1 on the BEO, with polygon-type areas A (low-centred),
  B and C (flat-centred or transitional) and D (inundated low-centred). UAF Permafrost Lab soil
  stations at A-D have thermistor transects and 2.5-3 m boreholes.
- **CALM U1.** A 1 km grid, 11 x 11 nodes at 100 m, with GTN-P reference 71.316807,
  -156.604036, installed in the early 1990s, with thaw depth probed every year. CALM U2, the CRREL
  plots measured since 1962, lies in its SE corner.
- **Sea ice and coast.** The UAF coastal X-band ice radar and webcam are on a downtown building
  (71.2925, -156.7883; antenna 22.5 m ASL; range about 10 km). The landfast-ice mass-balance site
  (near 71.366, -156.542) is relocated every season. The SIZONet moorings are B1 (71.32535,
  -156.88404, 40 m) and B2. B2 is at 71 14.2 N, 157 39.2 W (71.2367, -157.6533) per Fukamachi et
  al. (2017); the ADC metadata lists 156.6571 W, which falls on land and is treated as a typo.
- **Tide gauges.** No NOAA water-level gauge operates now. CO-OPS 9494935 "Barrow Offshore"
  ran 2008-08-13 to 2010-08-20, and 9495048 Point Barrow is a subordinate prediction point only.
- **Other networks.** AERONET "Barrow" (records 1997-2026, site PI at DOE BNL) is listed at
  71.3122, -156.665, about 2 km WSW of BRW. ARM's C1 Cimel file carries the same coordinate.
  As of 2026-10-19 the MPLNET site list names no Barrow site; the micropulse lidar there is ARM's.
  EarthScope GNSS: SG27 (PBO/NOTA, 2002-) at BRW, BARO on the BARC roof (2014-2023), BASC
  (2011-2015). The USGS Barrow magnetic observatory (from 1949) is 0.42 km W of BRW.

## Asset table

| name | operator | lat | lon | years | coordinate precision |
|---|---|---|---|---|---|
| Barrow Atmospheric Baseline Observatory (BRW) | NOAA Global Monitoring Laboratory | 71.323 | -156.6114 | 1973– | 4 dp (~10 m) |
| BSRN station BAR (Barrow) | NOAA Global Monitoring Laboratory | 71.323 | -156.607 | 1992–2016 | 3 dp (~100 m) |
| USGS Barrow Magnetic Observatory (BRW) | USGS Geomagnetism Program | 71.3225 | -156.6231 | 1949– | 4 dp (~10 m) |
| USCRN Utqiagvik (formerly Barrow) 4 ENE (WBAN 27516) | NOAA NCEI | 71.3213 | -156.611 | 2002– | 4 dp (~10 m) |
| NWS ASOS Wiley Post-Will Rogers Memorial Airport (PABR) | NOAA National Weather Service / FAA | 71.28703 | -156.73938 | 1901– | 5 dp (~1 m), ASOS CM survey, WGS84 |
| NWS Utqiagvik Weather Service Office upper-air site (WMO 70026) | NOAA National Weather Service | 71.2889 | -156.7833 | 1932– | 4 dp (~10 m) |
| NEON Utqiagvik site BARR (site reference point) | NSF NEON (Battelle) | 71.28241 | -156.61936 | 2016– | 5 dp (~1 m) |
| NEON BARR tower (TOWER104688) | NSF NEON (Battelle) | 71.282425 | -156.619319 | 2017– | 6 dp (~0.1 m), WGS84 |
| NEON BARR instrument hut (HUT104647) | NSF NEON (Battelle) | 71.28255 | -156.6196 | 2017– | 6 dp (~0.1 m) |
| NEON BARR megapit MP1 (MEGAPT100964) | NSF NEON (Battelle) | 71.281711 | -156.650219 | 2016–2016 | 6 dp (~0.1 m) |
| NEON BARR Soil Plot, SP1 (SOILPL104735) | NSF NEON (Battelle) | 71.282368 | -156.6189 | 2017– | polygon centroid, 6 dp |
| NEON BARR Soil Plot, SP2 (SOILPL104764) | NSF NEON (Battelle) | 71.281912 | -156.617746 | 2017– | polygon centroid, 6 dp |
| NEON BARR Soil Plot, SP3 (SOILPL104791) | NSF NEON (Battelle) | 71.282133 | -156.61662 | 2017– | polygon centroid, 6 dp |
| NEON BARR Soil Plot, SP4 (SOILPL104823) | NSF NEON (Battelle) | 71.282086 | -156.615361 | 2017– | polygon centroid, 6 dp |
| NEON BARR Soil Plot, SP5 (SOILPL104850) | NSF NEON (Battelle) | 71.282031 | -156.613847 | 2017– | polygon centroid, 6 dp |
| NEON BARR observational sampling plots (summary of 93 plots) | NSF NEON (Battelle) | 71.26797 | -156.55109 | 2016– | mean of plot centres |
| Barrow Arctic Research Center (BARC) | UIC Science LLC (Ukpeagvik Inupiat Corporation) | 71.32495278 | -156.66741111 | 2007– | 8 dp listed (building-level) |
| Naval Arctic Research Laboratory (NARL), historic | U.S. Office of Naval Research (contract operators incl. University of Alaska from 1954) | 71.325 | -156.68056 | 1947–1981 | ~arc-second (Wikipedia, GNIS-style) |
| Barrow Environmental Observatory (BEO), extent centre | UIC Science LLC (Ukpeagvik Inupiat Corporation) | 71.29282 | -156.53708 | 1992– | centre of layer bounding box |
| NGEE Arctic Barrow intensive site A soil station | DOE NGEE Arctic (ORNL-led); UAF Permafrost Lab station | 71.28145 | -156.61104 | 2012– | 6 dp listed |
| NGEE Arctic Barrow intensive site B soil station | DOE NGEE Arctic (ORNL-led); UAF Permafrost Lab station | 71.27976 | -156.60348 | 2012– | 6 dp listed |
| NGEE Arctic Barrow intensive site C soil station | DOE NGEE Arctic (ORNL-led); UAF Permafrost Lab station | 71.28013 | -156.60117 | 2012– | 6 dp listed |
| NGEE Arctic Barrow intensive site D soil station | DOE NGEE Arctic (ORNL-led); UAF Permafrost Lab station | 71.28214 | -156.60078 | 2012– | 6 dp listed |
| CALM grid U1 Barrow (1 km ARCSS/CALM grid) | CALM (G. Washington Univ.) | 71.316807 | -156.604036 |  | 6 dp listed (grid reference) |
| UAF Utqiagvik coastal sea-ice radar and webcam | UAF Geophysical Institute Sea Ice Group | 71.2925 | -156.78833 | 1973– | arc-second (~30 m) |
| UAF Barrow sea-ice mass-balance site (SIZONet MBS) | UAF Geophysical Institute Sea Ice Group | 71.366 | -156.542 | 2007– | approximate (3 dp); relocated every season |
| SIZONet mooring B1 (nearshore) | UAF / Hokkaido University | 71.32535 | -156.88404 | 2009– | 5 dp (deployment fix) |
| SIZONet mooring B2 (offshore) | UAF / Hokkaido University | 71.2367 | -157.6533 | 2009– | 0.1 arc-minute (~200 m) |
| NOAA CO-OPS 9494935 Barrow Offshore (water level) | NOAA CO-OPS | 71.36011 | -156.72986 | 2008–2010 | 5 dp |
| NOAA CO-OPS 9495048 Point Barrow (tide predictions) | NOAA CO-OPS | 71.36 | -156.353 |  | 2-3 dp |
| AERONET Barrow sun photometer | NASA GSFC AERONET; site PI at DOE Brookhaven National Laboratory | 71.3122 | -156.665 | 1997– | 4 dp listed |
| EarthScope GNSS SG27 (NOTA/PBO) | EarthScope Consortium (formerly UNAVCO) | 71.3229 | -156.6103 | 2002– | 4 dp |
| EarthScope GNSS BARO (Barrow Arctic Research Center roof) | EarthScope Consortium (formerly UNAVCO) | 71.325 | -156.6677 | 2014–2023 | 4 dp |
| EarthScope GNSS BASC (Barrow community base station) | EarthScope Consortium (formerly UNAVCO) | 71.3249 | -156.6779 | 2011–2015 | 4 dp |
| Utqiagvik (formerly Barrow), city | City of Utqiagvik / North Slope Borough seat | 71.253861 | -156.798246 | 1958– | 6 dp (Census internal point, not downtown) |
| Point Barrow (Nuvuk) | n/a (geographic feature; archaeological site) | 71.38889 | -156.47917 |  | arc-second (GNIS via Wikipedia) |
| Point Barrow Long Range Radar Site (DEW Line POW-Main, LRR A-17) | U.S. Air Force | 71.32722 | -156.63611 | 1955– | arc-second (Wikipedia) |

## Access that worked (2026-10-19)

- NEON API v0, no key: `https://data.neonscience.org/api/v0/sites/BARR` and `.../locations/<name>`
  (`neon_site_live`, `neon_location_live`).
- NCEI HOMR and IGRA2 station lists (NWS and USCRN), the USCRN `stations.tsv`, the NOAA CO-OPS
  MDAPI, the EarthScope GNSS metadata service, the AERONET site list and the Census Gazetteer.
- The UAF Permafrost Lab and UTEP BAID servers serve incomplete TLS chains; bsrn.awi.de and
  arcticdata.io returned proxy 502, so BSRN metadata came from the PANGAEA wiki.

## Traps

- WMO 70026 means two places, the airport ASOS in HOMR and the launch site in IGRA2. ARM adds a third.
- Lower-confidence coordinates (about 100 m): NARL, Point Barrow and the DEW Line site, from
  Wikipedia/GNIS-style points. The sea-ice mass-balance site is approximate and moves yearly.
- NEON soil plots are pinned at polygon centroids, not sensor positions.
- The BRW cluster (BRW, BSRN, USCRN, USGS magnetic, GNSS SG27, CALM U1 reference point) lies within 0.74 km and
  overlaps ARM C1/E10/E30, so a map at town scale needs a close-up inset.

## Verified against

2026-10-19: 37 assets pinned (13 from APIs), 519 NEON BARR locations from the NEON API, and 21
literature DOIs checked on Crossref. `tests/test_structure_nsa.py` checks the asset table here
against `utqiagvik_assets.csv`, and `tests/test_live_nsa.py` re-reads the NEON tower coordinate.

## References

* Stone et al. (2002) Earlier spring snowmelt in northern Alaska as an indicator of climate change. Journal of Geophysical Research: Atmospheres. https://doi.org/10.1029/2000JD000286
* Driemel et al. (2018) Baseline Surface Radiation Network (BSRN): structure and data description (1992–2017). Earth System Science Data. https://doi.org/10.5194/essd-10-1491-2018
* Love (2013) An International Network of Magnetic Observatories. Eos, Transactions American Geophysical Union. https://doi.org/10.1002/2013EO420001
* Diamond et al. (2013) U.S. Climate Reference Network after One Decade of Operations: Status and Assessment. Bulletin of the American Meteorological Society. https://doi.org/10.1175/BAMS-D-12-00170.1
* Durre et al. (2006) Overview of the Integrated Global Radiosonde Archive. Journal of Climate. https://doi.org/10.1175/JCLI3594.1
* Keller et al. (2008) A continental strategy for the National Ecological Observatory Network. Frontiers in Ecology and the Environment. https://doi.org/10.1890/1540-9295(2008)6[282:ACSFTN]2.0.CO;2
* Hubbard et al. (2012) Quantifying and relating land-surface and subsurface variability in permafrost environments using LiDAR and surface geophysical datasets. Hydrogeology Journal. https://doi.org/10.1007/s10040-012-0939-y
* Brown et al. (2000) The circumpolar active layer monitoring (calm) program: Research designs and initial results. Polar Geography. https://doi.org/10.1080/10889370009377698
* Hinkel & Nelson (2003) Spatial and temporal patterns of active layer thickness at Circumpolar Active Layer Monitoring (CALM) sites in northern Alaska, 1995–2000. Journal of Geophysical Research: Atmospheres. https://doi.org/10.1029/2001JD000927
* Brown et al. (1980) An Arctic ecosystem : the coastal tundra at Barrow, Alaska. . https://doi.org/10.1575/1912/222
* Shelesnyak (1948) Arctic Research Laboratory, Office of Naval Research, Point Barrow, Alaska. Science. https://doi.org/10.1126/science.107.2777.283
* Reed (1969) The Story of the Naval Arctic Research Laboratory. Arctic. https://doi.org/10.14430/arctic3211
* Reed & Ronhovde (1971) Arctic Laboratory: a history (1947-1966) of NARL. DTIC/AINA. https://doi.org/10.21236/ad0733452
* Druckenmiller et al. (2009) Toward an integrated coastal sea-ice observatory: System components and a case study at Barrow, Alaska. Cold Regions Science and Technology. https://doi.org/10.1016/j.coldregions.2008.12.003
* Mahoney, Eicken & Shapiro (2007) How fast is landfast sea ice? Cold Reg. Sci. Technol. https://doi.org/10.1016/j.coldregions.2006.09.005
* Jones et al. (2016) Landfast sea ice breakouts ... at Barrow, Alaska. Cont. Shelf Res. https://doi.org/10.1016/j.csr.2016.07.015
* Mahoney et al. (2015) Taking a look at both sides of the ice ... near Barrow. Ann. Glaciol. https://doi.org/10.3189/2015aog69a565
* Polashenski et al. (2012) The mechanisms of sea ice melt pond formation and evolution. Journal of Geophysical Research: Oceans. https://doi.org/10.1029/2011JC007231
* Fukamachi et al. (2017) Sea-ice thickness in the coastal northeastern Chukchi Sea from moored ice-profiling sonar. J. Glaciol. https://doi.org/10.1017/jog.2017.56
* Richter et al. (2022) Accuracy and precision when deriving sea-ice thickness from thermistor strings. J. Glaciol. https://doi.org/10.1017/jog.2022.108
* Holben et al. (1998) AERONET—A Federated Instrument Network and Data Archive for Aerosol Characterization. Remote Sensing of Environment. https://doi.org/10.1016/S0034-4257(98)00031-5
* Dataset: Eicken, H. et al. (2009, updated 2012) Automated ice mass balance site (SIZONET). UCAR/NCAR EOL. https://doi.org/10.5065/D6MW2F2H
