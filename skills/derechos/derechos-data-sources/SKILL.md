---
name: derechos-data-sources
description: >
  Tested access recipes for the regional data sources the DERECHOS campaign (DOE ARM AMF2,
  Ames IA to Chicago IL) depends on. Use when fetching or discovering data over the DERECHOS
  or Midwest domain, or building a DERECHOS pipeline. Covers ARM Data Center / ARM Live via
  ACT, Iowa Environmental Mesonet (IEM ASOS/AWOS, ISUSM soil moisture, RAOB soundings),
  Illinois Climate Network / WARM (ISWS), NEXRAD Level II KDVN and KLOT, USDA Cropland Data
  Layer via CropScape, AmeriFlux, Sentinel-2 via Element84 STAC and Copernicus CDSE, mPING
  precipitation type, and the HRRR archive via Herbie. Carries verified S1 (Muscatine Island)
  and M1 (SERF) coordinates, KDVN geometry, and gotchas that silently return wrong answers:
  mPING in_bbox-not-bbox, CropScape invalid JSON, dead S1 soil sensors. Triggers - DERECHOS,
  Muscatine, Crawfordsville, SERF, MIRF, KDVN, KLOT, DeKalb, NIU, Nachusa, IEM, mesonet,
  ISUSM, ICN, WARM, ISWS, CropScape, CDL, AmeriFlux, Sentinel-2, mPING, HRRR, Herbie,
  ARM Live, soil moisture, land use.
---

# DERECHOS data sources

Working access patterns for the non-ARM regional data DERECHOS leans on, plus ARM's own
archive. Everything below was exercised against the live service on **2026-09-01** from
this sandbox; §"What is verified" states exactly what passed and what did not.

Load `derechos-campaign` for the science case (H1-H4, SQ1-SQ7, the traceability matrix,
site concept). This skill is only about getting bytes.

`kernel.py` auto-loads its helpers into the python kernel. `derechos_stations.json` ships
alongside it and carries the site/radar/station reference.

## Source to science question

`derechos_sources()` returns this table as data; `derechos_sources(sq=3)` filters it.

| Source | What it provides over the domain | Serves | Status |
|---|---|---|---|
| **ARM Data Center / ARM Live** | The campaign's own S1/M1/R1 instrument data | SQ1-SQ7 | tested |
| **IEM - ASOS/AWOS** | Surface met, gust peaks, precip; densest network in the western domain | SQ2, SQ6, SQ7 | tested |
| **IEM - ISUSM** | Soil moisture + soil temperature profiles, **including at S1 and M1** | SQ1, SQ2 | tested |
| **IEM - RAOB** | KDVN sounding archive (00Z/12Z) | SQ3, SQ6, SQ7 | tested |
| **Illinois Climate Network / WARM** | Soil moisture + soil temperature, eastern domain | SQ1, SQ2, SQ3 | **login required** |
| **NEXRAD Level II** (KDVN, KLOT) | Convective organization, wind extremes | SQ1, SQ2, SQ6, SQ7 | tested |
| **USDA CDL / CropScape** | Crop type per 30 m pixel - land-use stratification | SQ1, SQ2, SQ4, SQ5 | tested |
| **AmeriFlux** | Flux-tower ET comparison (ATMOS, downtown Chicago) | SQ1, SQ2 | catalogue tested (`amfcdn.lbl.gov`); download needs an account |
| **Sentinel-2 L2A** (Element84) | Land-surface state, greenness, snow, standing water | SQ1-SQ5 | tested |
| **Sentinel-2** (Copernicus CDSE) | Native SAFE products | SQ1, SQ2, SQ3 | search only |
| **mPING** | Crowdsourced precipitation type, hail size, wind damage | SQ2, SQ3, SQ6 | tested |
| **HRRR archive** (AWS) | SCREAM IC/BC; the IOP forecast scorecard's input | SQ1, SQ6, SQ7 | tested |

## The domain, with verified geometry

`derechos_stations()` / `derechos_site("S1")` (also `"M1"`, `"NIU"`, `"ATMOS"`).
Bounding box used throughout:
`[-94.2, 40.7, -87.4, 42.6]`.

The core-site coordinates are **not** guesses - both DERECHOS core sites already carry an
IEM ISUSM soil station, and those station coordinates are the sites:

| Site | Lat, Lon | ISUSM | Range / azimuth from KDVN |
|---|---|---|---|
| **S1** Muscatine Island Research Farm | 41.356, -91.136 | `FRUI4` | 54.4 km / 33.8 mi, **238.7 deg** |
| **M1** South East Research Farm (SERF) | 41.1933, -91.4839 | `CRFI4` | 88.7 km / 55.1 mi, **238.7 deg** |

Both azimuths agree to 0.1 deg, so the white paper's "same WSR-88D radial" is literally
true. Separation is **34.3 km**, matching the abstract's 35 km. Two numbers to correct
when quoting the draft: M1 is **55 mi** from Davenport, not 51; and the "~29 km implied"
S1-M1 separation in the `derechos-campaign` errata was an artefact of that 51 mi figure -
use 34-35 km.

Radars: **KDVN** 41.6117, -90.5808 (read from a Level II header). **KLOT** 41.6044,
-88.0847 - 67.6 km from NIU/DeKalb, 133 km from Nachusa Grasslands, **13.1 km from
ATMOS**.

The eastern sites are not ISUSM-backed, and their coordinates differ in quality:

| Site | Lat, Lon | Source | Range / azimuth from KLOT |
|---|---|---|---|
| **ATMOS** Argonne Testbed for Multiscale Observational Science | 41.7018, -87.9963 | AmeriFlux registry, `US-AMS` | 13.1 km, **34.2 deg** |
| **NIU** DeKalb (Argonne Deployable Mast) | 41.9339, -88.7679 | campus centroid, **approximate** | 67.6 km, **303.0 deg** |

ATMOS is the one to be careful about: the `CHICAGO` entry in the station file is a **city
centroid** (41.8781, -87.6298), about 35 km northeast of the actual tower, so it is not a
substitute for the ATMOS coordinate. Being only 13 km from KLOT, ATMOS sits well inside
that radar's usable annulus - handy as a ground-truth anchor - but a constant-altitude
radar product above ~4 km is in the cone of silence there. The NIU coordinate is a campus
centroid and is fine for mapping, not for siting.

## 1. ARM Data Center / ARM Live

The campaign's own data lands here. Discovery and download by datastream and date.

```python
arm_query("sgpmetE13.b1", "2024-07-01", "2024-07-02")
# {'files': [...], 'status': 'success', 'num_found': 2, 'total_size': 665152.0}
arm_download("sgpmetE13.b1", "2024-07-01", "2024-07-01", output="arm_data")
```

**`gpm-storm-targeted-radar-fetch` is the reference for ARM Live's failure modes** - load
it before any long or bulk fetch. It documents, from measured experience: `Content-Length`
verification (a dropped connection returns EOF rather than raising, so truncated volumes
look clean and only fail hours later at read time), `.part`-then-`os.replace` writes, HEAD
sizing to classify interleaved scan types before downloading, and the archive's
degradation pattern (throughput collapsing to ~0.3 MB/s, `IncompleteRead`, and a fixed
30 s HTTP 500 from the listing endpoint that is *not* your credentials). Do not re-derive
any of that here.

Credentials: `ARMUSER` + `ARMTOKEN`, passed as a single `user=USER:TOKEN` parameter. A bad
credential returns **HTTP 401 with the body `Invalid username.`** - not a JSON error.

Prefer ACT (`act.discovery.download_arm_data`), which prints the DOI citation text; capture
it, because ARM asks that it appear in publications. `act.discovery.get_arm_doi` takes 3
positional arguments in ACT 2.3.4, not 4.

## 2. Iowa Environmental Mesonet (IEM)

Iowa State; run by white-paper co-author Daryl Herzmann. No credentials, no key. The
densest in-situ network in the western half of the domain, and the single most useful
non-ARM source here.

Etiquette: these are free CGI services on university hardware. Request whole date ranges
in one call rather than looping days, and keep concurrency to 1-2.

### Station discovery, and the documented API

`https://mesonet.agron.iastate.edu/api/` is the landing page and **`/api/1/openapi.json`
documents 50 endpoints**. Prefer the API over the legacy `cgi-bin/request/*.py` scripts
wherever an endpoint exists; read parameter names off the spec rather than guessing.

```python
iem_network("IA_ASOS")   # 62 stations
iem_network("ISUSM")     # 29 stations
```

**`/api/1/networks.json` is the authoritative network list - 600 networks.** Measured
2026-09-28 over the DERECHOS box, the ten that matter (online / registered in box):

| IEM code(s) | Network | online / registered |
|---|---|---|
| `IA_ASOS` `IL_ASOS` | ASOS / AWOS | 53 / 54 |
| `IA_COOP` `IL_COOP` | NWS COOP | 156 / 226 |
| `IA_DCP` `IL_DCP` | HADS / DCP river+precip telemetry | 529 / 679 |
| `IA_COCORAHS` `IL_COCORAHS` | CoCoRaHS volunteer precipitation | **1597 / 3035** |
| `IACLIMATE` `ILCLIMATE` | Long-term climate sites (from 1836 IL, 1867 IA) | 122 / 507 |
| `IA_RWIS` | Iowa DOT RWIS | 50 / 59 |
| `IL_RWIS` | Illinois DOT RWIS | **5 / 52** (IDOT feed ended 2016-08-17) |
| `IA_HPD` | Hourly precipitation | 27 / 27 |
| `ISUSM` | ISU Soil Moisture | 15 / 16 |
| `RAOB` | Radiosonde sites | **1 / 3** - only KDVN is active; KCID and KJOT are historical |

Station rows carry an `online` boolean plus `archive_begin`/`archive_end`; filter on it or
a third of what you plot is defunct. CoCoRaHS is by far the largest network here and its
density follows population, so it is dense around Chicago and thin over the farm sites.

### Two silent-failure traps, both HTTP 200

1. **An unrecognised network code returns an empty feature list, not an error.**
   `IACOCORAHS` (no underscore) returns 0 stations; the real code is `IA_COCORAHS` with
   1,030 registered in the box. A guessed code reads as "this network has nothing here" -
   always resolve codes against `networks.json`.
2. **An unrecognised query parameter is ignored.** `nws/lsrs_by_point` takes
   `begints`/`endts` and `radius_miles`/`radius_degrees`; passing `sdate`/`edate` returns
   **38,281 rows spanning 2004-2026** instead of the 220 for the day asked for - 174x too
   many, no warning. Same failure family as mPING's `bbox`-vs-`in_bbox`.

### API endpoints the CGI scripts do not cover

| Endpoint | What it gives |
|---|---|
| `iowa_winter_roadcond.geojson?valid=` | **Iowa winter road conditions, openly** - 1,006 segments at 2024-12-14T12Z, labels `PC Ice` 510, `CC Ice` 231, `PC Mixed` 62, `Normal` 174. This is the 2024-25 season that Iowa DOT's own ArcGIS service **token-gates**, so it closes that open action in `derechos-iowa-dot`. |
| `last_shef.json?station=` , `shef_currents` | DCP/SHEF observations - the working path, since `hads.ncep.noaa.gov`'s DecodedData servlet returns zero-byte bodies |
| `idot_rwiscam` , `idot_dashcam` | RWIS and snowplow camera imagery indices |
| `drydown.json?lat=&lon=` | Soil-moisture drydown climatology by point, 1980-present |
| `iemre/daily|hourly|multiday?date=&lon=&lat=` | IEM Reanalysis gridded analysis over the domain |
| `nws/lsrs_by_point` , `vtec/*` , `nws/sbw_by_line` | Local storm reports, VTEC events, storm-based warning polygons |
| `ffg_bypoint.json` , `usdm_bypoint.json` | Flash-flood guidance, US Drought Monitor by point |
| `network/{id}.json` , `station/{id}.json` | Station metadata as pandas table-schema JSON |
| `asos_interval_summary` , `obhistory` , `currents` , `daily` | ASOS summaries and current/historical observations |

**`isusm/daily.json` carries NO soil columns** - re-confirmed 2026-09-28, it returns 13
columns (`et sgdd gdd srad precip climo_gdd climo_precip` + station metadata). Soil moisture
and temperature must come from the `isusm.py` CGI with an explicit `vars=`; see
`derechos-soil-properties`.

### ASOS / AWOS surface observations

```python
a = iem_asos(["MUT","DVN","DKB","ORD"], "2020-08-10", "2020-08-11")
a.groupby("station")["gust"].max()   # MUT 50 kt, ORD 54 kt, DKB 42 kt (2020 derecho)
```

`report_type=[3,4]` (the helper's default) keeps **both** routine METARs and SPECIs -
drop the specials and you lose the gust peaks that matter for SQ6. Note the 2020-08-10
example: DVN's own ASOS reports only 15 kt while MUT 60 km away reports 50 kt. Peak-gust
coverage in this network is spatially patchy; do not read a single station as the domain
maximum.

### ISUSM - soil moisture and temperature, at the core sites

This is the find worth knowing about. The ISU Soil Moisture Network already instruments
**both** DERECHOS core sites, with records back to 2014-04-02 (S1) and 2013-12-17 (M1) -
a decade-plus pre-campaign baseline for H2/SQ1, and partial cover for the soil-moisture
row that is missing from the white paper's Table 1.

```python
iem_isusm(["FRUI4","CRFI4"], "2024-07-01", "2024-07-05", mode="daily")
iem_isusm("FRUI4", "2024-07-01", "2024-07-03", mode="hourly")
```

Columns: `soil04t soil12t soil24t soil50t` (deg **F**), `soil12vwc soil24vwc soil50vwc`
(percent), plus `et`, `precip` (inches), `solar`, `gdd50`.

**Timestamps must be timezone-aware** or the service returns HTTP 422 with a pydantic
validation body - a bare `2024-07-01` fails. The helper appends `T00:00:00Z`.

**Do not trust the VWC columns without QC.** Measured over all 366 days of 2024:

| | soil12vwc | soil24vwc | soil50vwc |
|---|---|---|---|
| `CRFI4` (M1) | 41.3-52.3 % | 41.9-52.2 % | 36.9-45.1 % |
| `FRUI4` (S1) | 2.6-8.3 % | **pinned at 1.00 on 97 % of days** | **pinned at 1.00 on 100 % of days** |

The deep sensors at S1 are dead, and they fail by returning a constant `1.0` rather than a
gap - `notna()` counts 366/366 for every column at both stations. So S1's existing deep
soil moisture is unusable, which sharpens the white paper's §3.1 SoilVue10 advocacy from a
preference into a requirement. `soil_sensor_health()` returns this. Re-measure before
relying on it; sensors get repaired.

### Soundings

```python
iem_raob("KDVN", "2020-08-10", "2020-08-11")   # 719 levels, 542 with temperature
```

Missing values arrive as the literal string `M`; the helper maps them to NaN. `levelcode`
distinguishes mandatory / significant / surface levels.

## 3. Illinois Climate Network / WARM (ISWS) - login required

The eastern-domain counterpart to ISUSM, run by the Illinois State Water Survey; carries
soil moisture and soil temperature, hourly, from the early 2000s. Co-author **Trent Ford**
is the Illinois State Climatologist at ISWS.

**Station metadata is public; bulk data is not.**

```python
icn_stations()   # 21 codes/names + the northern-Illinois subset + the access caveat
```

Verified live: 21 station codes at
`warm.isws.illinois.edu/warm/climnet/stnmetadata.asp`, per-station pages at
`stationmeta.asp?site=<CODE>`. The DERECHOS-relevant northern subset is **DEK (DeKalb -
co-located with the NIU guest cluster and the Argonne Deployable Mast), STC (St. Charles),
FRE (Freeport), MON (Monmouth)**.

Host gotchas: `www.isws.illinois.edu` 301-redirects to `isws.illinois.edu`, where every
`/warm/...` path is a 404 after the site redesign. Data pages live only on
**`warm.isws.illinois.edu`**. `/warm/cdflist.asp` returns a page titled *"Access WARM Data
- Login"*; `/warm/warmdb/warmdb.asp` is an IIS 404. Station lat/lon is not machine-readable
on the public pages, so `derechos_stations.json` deliberately omits ICN coordinates rather
than inventing them.

**Action for the campaign lead:** obtain an ISWS/WARM data account, or a direct data
transfer through Trent Ford, and record the resulting endpoint here.

## 4. NEXRAD Level II - KDVN and KLOT

Anonymous AWS, no credentials.

```python
k = derechos_nexrad_keys("KDVN", datetime(2020,8,10,16), datetime(2020,8,10,19))
# 30 volumes; KLOT 19-21Z on the same day: 22
```

Bucket is **`unidata-nexrad-level2`**. The legacy `noaa-nexrad-level2` is **dead** - it
returns a genuine S3 `AccessDenied` (confirmed again 2026-09-01), which is not a sandbox
artefact and has no fallback.

**`nexrad-aws-2025` is the reference for everything past listing** and should be loaded
before analysing volumes: split cuts (a 17-sweep VCP-212 volume holds 14 distinct
elevations, and picking a sweep by "first field present" silently flips which member you
get between processes), SAILS/MESO-SAILS/MRLE/AVSET detection per volume, the real-time
chunks bucket, and the ARCO Icechunk stores. A verified read of
`KDVN20200810_172407_V06`: 20 sweeps, VCP 212, max 70.5 dBZ.

## 5. USDA Cropland Data Layer via CropScape

30 m crop type per pixel - the land-use stratification H1 and H4 rest on. No credentials.

```python
cdl_point(41.356, -91.136, 2024)     # S1 -> {'value': 5,  'category': 'Soybeans'}
cdl_point(41.1933, -91.4839, 2024)   # M1 -> {'value': 1,  'category': 'Corn'}
cdl_stats(41.356, -91.136, 2024, half_km=5.0)
cdl_clip(41.356, -91.136, 2024, half_km=3.0)
```

That point query independently confirms the white paper's site rationale: S1 in soybeans,
M1 in corn, in the same year.

Within 5 km of S1 (2024): Corn 6453 ac, Soybeans 5892 ac, Grass/Pasture 3855 ac,
Deciduous Forest 2920 ac, Developed/Low 1231 ac - a genuine mosaic, not a monoculture.

Gotchas:

- **Coordinates are EPSG:5070** (CONUS Albers), not lat/lon. The helpers reproject.
- **`format=json` is not JSON.** It returns a JavaScript object literal with *unquoted*
  keys, so `json.loads` raises `Expecting property name enclosed in double quotes`.
  `cdl_parse()` quotes the keys first.
- `GetCDLStat` and `GetCDLFile` are two-step: the XML response carries a `<returnURL>`
  pointing at a cached artefact on the same host, which you then fetch. The cache path
  embeds a server-side timestamp, so URLs are not reusable.
- Clipped GeoTIFFs are `uint8` class codes with **no nodata set**, EPSG:5070, 30 m.

## 6. AmeriFlux - reachable, but on a third host

**CORRECTED 2026-09-26.** `amfcdata.lbl.gov` and `ameriflux-data.lbl.gov` both fail at
the sandbox network layer (`ProxyError`, max retries exceeded - a connection block, not an
HTTP status), and `ameriflux.lbl.gov` returns a real HTTP **403** from nginx. But
**`amfcdn.lbl.gov` works anonymously** and serves the whole site catalogue. The "not
reachable" conclusion below was drawn from the wrong hosts; note also that only the third
host produced an actual HTTP response, so the earlier "502" reading for the first two was
a misattribution of a network block.

```python
ameriflux_status()          # still reports the 502/403 hosts
```

Working endpoints on `amfcdn.lbl.gov`, no credential:
`/api/v1/site_display/AmeriFlux` (844 sites, 299 kB),
`/api/v1/site_availability/AmeriFlux` (policy tiers per product), and the richer
`/api/v2/site_info_display/AmeriFlux` (1.69 MB, wrapped in a top-level `"values"` key)
carrying `base_variables` (test `"LE" in ...`), `grp_publish_base` (exact published BASE
years), `publish_ameriflux_policy` (CCBY4.0 vs LEGACY), DOIs, and planting/harvest dates
in `grp_igbp.igbp_comment`. **Filter trap:** `country` is `"USA"` and `state` is a
two-letter code - matching `"United States"` or `"Iowa"` silently returns an empty frame.

Bulk data still needs an account: `POST /api/v2/data_download` with `user_id`,
`user_email`, `data_policy`, `data_product` (an empty body returns 422 naming exactly
those four; `agree_policy` is client-side and rejected as unknown). Downloads are logged
against a user id, so do not call it without a real registered account.

**Load `derechos-domain-et-data` for the resulting tower inventory** - 21 AmeriFlux sites
inside the domain box, 68 Midwest candidates, and the finding that the nearest in-box
cropland tower is 224 km from S1 with nothing in the middle of the land-use gradient. The
DERECHOS urban towers are registered: **US-AMS** is Argonne ATMOS, **US-CU1** the UIC
downtown-Chicago tower, both CC-BY-4.0. The `US-AMS` registry record is also the source
of the ATMOS coordinate in `derechos_site("ATMOS")` - 41.7018, -87.9963, 232 m.

The `ameriflux_status()` return records the API shape the `amerifluxr` client uses
(`/api/v1/site_display/AmeriFlux`, `/api/v1/data_availability/AmeriFlux/<SITE>`, and a
POST to `/api/v1/data_download` carrying user id, email, data product and policy
acceptance) as a **starting point, not a tested recipe**.

An AmeriFlux account is required regardless - downloads are logged against a user id and
the data policy must be accepted per request. The DERECHOS ATMOS and downtown-Chicago
towers are already AmeriFlux-registered, so their site IDs are the thing to look up first.

## 7. Sentinel-2

Two paths. **Use Element84 - it is the one that works end to end without credentials.**

```python
s2_search(41.356, -91.136, "2024-06-01", "2024-08-31", max_cloud=20)   # 3 items
s2_ndvi(41.356, -91.136, "2024-06-01", "2024-08-31")
# {'item_id': 'S2A_15TXF_20240606_0_L2A', 'cloud_cover': 0.038, 'ndvi_mean': 0.410, ...}
```

The domain sits on MGRS tile **T15TXF** (S1/M1 end). Assets are COGs in
`sentinel-cogs.s3.us-west-2.amazonaws.com`, so a windowed read costs a few MB rather than
a whole granule - `s2_ndvi` reads only the box you ask for. Reflectance is scaled by
10000.

Clear-sky availability varies sharply **across** the domain, so do not generalise from one
point: for June-August 2024 with cloud < 20 %, S1 (tile T15TXF) returned **3** scenes while
NIU/DeKalb returned **11**. Budget per-site, and for the §4.2.4 computer-vision or
greenness work lean on the site cameras and phenocams for temporal density at the sparse
end of the domain.

The **Copernicus CDSE** OData catalogue is queryable **anonymously**:

```python
cdse_search(41.356, -91.136, "2024-08-01", "2024-09-01", top=2)
```

but **product download needs a CDSE bearer token, and the configured `ESATOK` is not
one.** Its issuer is `https://iam.maap.eo.esa.int/realms/esa-maap` with `azp=offline-token`
- an ESA MAAP offline token, unexpired but for a different platform. Presented to CDSE
OData it returns HTTP 403, and a `refresh_token` exchange at the CDSE identity endpoint
returns `invalid_client`. **Action:** register a Copernicus Data Space account if native
SAFE products are needed; otherwise Element84 covers the L2A use case.

NASA Earthdata is a third route and its CMR search is reachable
(`cmr.earthdata.nasa.gov`, verified: HLSS30 granules returned over the S1 box). HLS gives
harmonized Landsat + Sentinel-2 at 30 m, which roughly doubles the revisit. Downloads go
through `data.lpdaac.earthdatacloud.nasa.gov` with `NASAEDNAME`/`NASAEDTOKEN`; the search
was verified but **the authenticated HLS download was not tested**.

## 8. mPING

Crowdsourced precipitation type - the observation automated stations are worst at, and
directly the H3/SQ3 snow / sleet / freezing-rain transition problem. Also carries hail
size and wind-damage reports, which serve SQ6.

**The API is on `mping.ou.edu`, not `mping.nssl.noaa.gov`.** The NSSL host serves only the
project web page and 404s on every API path; it *also* presents an incomplete TLS chain
(valid Sectigo leaf for `*.nssl.noaa.gov`, intermediate not served) so requests to it fail
certificate verification. Ignore that host.

```python
mping_reports("2025-01-01", "2025-04-01")                              # 5957 reports
mping_reports("2025-01-01", "2025-04-01", description="Freezing Rain") # 32
```

### The trap: `bbox` is silently ignored

The spatial parameter that works is **`in_bbox`**. Measured over 2025-01-05 to 01-06:

| parameter | HTTP | count | fraction inside the DERECHOS box |
|---|---|---|---|
| `in_bbox=...` | 200 | **20** | **1.000** |
| `bbox=...` | 200 | 5552 | 0.003 |
| no spatial parameter at all | 200 | 5552 | 0.003 |
| `lonmin/latmin/lonmax/latmax` | 200 | 5552 | 0.003 |
| `geom_within`, `lat`+`lon`+`radius`, `state` | 200 | 5552 | 0.003 |

Every spelling except `in_bbox` returns the **global** report set with HTTP 200 and no
warning - longitudes spanning -151 to +32. A `bbox` query looks like it worked, returns
plausible mid-latitude reports at the head of the list, and is wrong by three orders of
magnitude. Always assert on the returned coordinates.

Other notes: page size is 5000 and the `next` link comes back as **`http://`** (the helper
upgrades it and follows pagination). `Authorization: Token <key>` header, from `MPINGTOK`.
License tier governs latency - a **Research** licence sees only reports older than 48
hours, so this cannot drive real-time IOP nowcasting; General sees the last 4 hours only.
Early-record geometry is suspect: an id-123 report from 2008 carries `[97.26, 35.27]`, a
positive longitude.

Verified domain climatology, Jan-Mar 2025, 5957 reports, 100 % in box:
Snow and/or Graupel 1958, Rain 1064, `NULL` 834, hail "Pea (0.25 in.)" 452, Drizzle 273,
Freezing Drizzle 221, Mixed Rain and Snow 166, Ice Pellets/Sleet 74; 258 freezing-type
reports overall. The `NULL` description (id 2) is a real category in the feed - filter it.

## 9. HRRR archive on AWS

Initial and boundary conditions for the SCREAM testbed, and the input the IOP forecast
scorecard needs. Anonymous; use **Herbie**.

```python
hrrr_inventory("2020-08-10 12:00", ":(CAPE|CIN):")
hrrr_point("2020-08-10 12:00", ":CAPE:surface:anl:", 41.356, -91.136)
# {'variable': 'cape', 'value': 1810.0, 'grid_lat': 41.353, 'grid_lon': 268.852}
ds = hrrr_field("2020-08-10 12:00", ":CAPE:surface:anl:")
```

Bucket `noaa-hrrr-bdp-pds`; pass `priority=["aws"]` so Herbie does not try hosts that are
not allowlisted (`storage.googleapis.com` in particular is denylisted and cannot be
granted). Herbie's `.idx` sidecar lets you byte-range a single field out of a ~130 MB
file - always search rather than downloading whole GRIB2 files.

**HRRR longitudes are 0-360.** `-91.136` matches grid longitude `268.852`; `hrrr_point`
converts. Grid is 1799 x 1059 at 3 km on a Lambert conformal projection. Herbie warns it
cannot write a config file in this sandbox; harmless, defaults are used.

## What is verified

Exercised against the live service on **2026-09-01** from this sandbox:

- **ARM Live** - `query` for `sgpmetE13.b1` and `bnfmetM1.b1`; ACT download of a real file
  with citation text; the dataset opened in xarray.
- **IEM** - `IA_ASOS` (62) and `ISUSM` (29) station GeoJSON; ASOS for MUT/DVN/DKB/ORD over
  the 2020-08-10 derecho; ISUSM daily and hourly at `FRUI4`/`CRFI4`, plus a full-year 2024
  sensor-health pass; KDVN RAOB (719 levels).
- **NEXRAD** - KDVN and KLOT key listing from `unidata-nexrad-level2`; one volume
  downloaded and read with Py-ART; `noaa-nexrad-level2` re-confirmed dead.
- **CropScape** - `GetCDLValue` at S1 and M1, `GetCDLStat` (30 classes), `GetCDLFile`
  downloaded and opened with rasterio.
- **Sentinel-2 / Element84** - STAC search and a windowed two-band COG read producing real
  NDVI. **CDSE** - anonymous OData search returning named SAFE products.
- **mPING** - authenticated queries, the full `in_bbox` versus `bbox` comparison above,
  pagination, and a Jan-Mar 2025 domain pull.
- **HRRR** - Herbie inventory, field extraction and a point value at S1.
- **NASA CMR** - HLSS30 granule search over the S1 box.

All **27** helpers in `kernel.py` were enumerated from the published file with `ast` and
called in a single pass after the skill was published, with coverage tracked
programmatically: 27 defined, 27 called, 0 missed. That pass exercised the wrappers that
the worked examples above only reach indirectly - `arm_download` (downloaded a file and
surfaced its DOI), `cdl_parse`, `mping_stamp`, `hrrr_field`, `soil_sensor_health`,
`ameriflux_status`, `derechos_credential` - and re-ran the live paths against a second set
of locations (M1 and NIU rather than S1) so the recipes are not tuned to one point.

### Not verified

- **AmeriFlux bulk data download** - needs a registered account. The site catalogue on `amfcdn.lbl.gov` IS verified (see §6); only the POST to `/api/v2/data_download` is untested.
- **Illinois Climate Network / WARM bulk data** - behind a login. Only station metadata
  was retrieved.
- **Copernicus CDSE product download** - no valid CDSE credential; search only.
- **NASA Earthdata HLS download** - CMR search verified, the authenticated granule
  download through `data.lpdaac.earthdatacloud.nasa.gov` was not.
- **mPING real-time behaviour** - the licence tier attached to `MPINGTOK` was not
  determined; assume Research (48 h lag) until confirmed.

### Network grants this skill depends on

Non-default allowlist entries granted while building it: `mping.ou.edu`,
`nassgeodata.gmu.edu`, `catalogue.dataspace.copernicus.eu`,
`identity.dataspace.copernicus.eu`, `earth-search.aws.element84.com`,
`sentinel-cogs.s3.us-west-2.amazonaws.com`, `isws.illinois.edu`,
`www.isws.illinois.edu`, `warm.isws.illinois.edu`, `amfcdata.lbl.gov`,
`ameriflux.lbl.gov`. Already default-reachable: `adc.arm.gov`,
`mesonet.agron.iastate.edu`, `unidata-nexrad-level2.s3.amazonaws.com`,
`noaa-hrrr-bdp-pds.s3.amazonaws.com`, `cmr.earthdata.nasa.gov`.

## Related skills

`derechos-campaign` (science case, traceability matrix - load first),
`gpm-storm-targeted-radar-fetch` (ARM Live failure modes, bulk-fetch discipline),
`nexrad-aws-2025` (VCPs, split cuts, dynamic scanning, ARCO),
`nexrad-cloud-router` (choosing a NEXRAD access path),
`arm-site-week-survey` (ARM datastream discovery over a window).
