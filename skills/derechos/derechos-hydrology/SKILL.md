---
name: derechos-hydrology
description: Verified access recipes for flooding, stream gauges, river stage and streamflow over the DERECHOS Iowa-Illinois domain - USGS NWIS legacy waterservices and the api.waterdata.usgs.gov OGC API (site discovery by bounding box, instantaneous and daily discharge and gage height, annual peak flows, parameter codes 00060/00065/00045), NOAA National Water Prediction Service NWPS gauges with action/minor/moderate/major flood-category thresholds, observed and forecast river stage, Iowa Flood Center IFIS bridge stream-stage sensors and hydrostations, HADS/DCP river and precipitation reports, and National Water Model channel_rt streamflow from noaa-nwm-pds and the v3.0 retrospective Zarr including USGS-site to NWM feature_id/COMID reach mapping. Use when fetching hydrographs, flood stage, crest data, drainage areas, gauge inventories or modelled streamflow for the DERECHOS campaign.
---

# DERECHOS hydrology - flooding, stream gauges, streamflow

Every recipe below was exercised against the live service from this sandbox on
**2026-09-04/05**. The `## What is verified` section states exactly what passed;
`## Not verified` records what did not, and why.

Load `derechos-campaign` first for the science case (H1-H4, SQ1-SQ7). This skill
complements **`derechos-data-sources`** and does not repeat it: soil moisture at
the core sites (IEM ISUSM), ASOS gust peaks, KDVN/KLOT soundings and Level II,
CropScape CDL, Sentinel-2, mPING and HRRR all live there. What is here is the
water side: who is gauging the rivers, what the flood thresholds are, and how to
get a hydrograph.

`kernel.py` auto-loads its helpers. Bounding box used throughout:
`BOX = (-94.2, 40.7, -87.4, 42.6)`.

## Source to science question

| Source | What it provides over the domain | Serves | Status |
|---|---|---|---|
| **USGS OGC API** (`api.waterdata.usgs.gov`) | The durable path: site inventory, daily/continuous values, annual peaks | SQ1, SQ2, SQ6, SQ7 | verified |
| **USGS legacy waterservices** | Same data, simpler grammar, **decommissioned early 2027** | SQ1, SQ2, SQ6, SQ7 | verified, sunsetting |
| **NOAA NWPS** (`api.water.noaa.gov`) | Flood-category thresholds, historic crests, observed + forecast stage, NWM reach forecasts | SQ1, SQ6, SQ7 | verified |
| **Iowa Flood Center IFIS** | Iowa's own dense bridge-mounted stream-stage network - 222 IFC-native sensors in the box | SQ1, SQ2, SQ7 | partial - no documented API |
| **HADS / DCP** via **IEM** | 15-minute SHEF river stage + precipitation from every DCP gauge | SQ1, SQ2, SQ6 | verified via IEM |
| **HADS** direct (`hads.ncep.noaa.gov`) | National DCP station definition table | - | metadata only |
| **NWM operational** (`noaa-nwm-pds`) | channel_rt streamflow, ~20-month rolling window | SQ1, SQ7 | verified |
| **NWM v3.0 retrospective** (Zarr) | Hourly modelled streamflow 1979-2023, 2.78 M reaches | SQ1, SQ2, SQ7 | verified |
| **NWM v2.1 retrospective** | Older Zarr/NetCDF retrospective | SQ1, SQ2 | reachable, not read |

Why this matters for DERECHOS: H2 is a two-way soil-moisture / convection
coupling hypothesis, and SQ1 asks explicitly about the **runoff versus recharge**
partition of storm rainfall. `derechos-campaign` already records a measured
pre-campaign recharge baseline at M1 (median 0.295 of event rainfall into
0-75 cm). The stream side of that same water balance is what this skill gets at:
the runoff limb, gauged, at 15-minute resolution, with a 100-year record.

## The domain, measured

| Network | In the box | Notes |
|---|---|---|
| USGS sites with 00060 or 00065 | **429** | 408 with drainage area, 323 with annual peaks, 245 still active in 2026 |
| USGS sites with precipitation (00045) | **42** | see the gotcha below - no soil moisture at any of them |
| NWPS gauges | **353** | 246 carry a `usgsId`, 282 carry a `reachId`, only **234** have flood thresholds |
| NWPS gauges that are IFC sensors | **65** | name contains `--IFC`; these have NWS LIDs and thresholds |
| IFIS map objects | **901** | 270 on stream-gauge panels, 474 rain, 105 well, 34 hydrostation |
| IFIS stream-type objects fetched | **322** | 260 reporting a stage in the last 30 days; 222 IFC-native, 100 USGS-relayed |
| NWM reaches | **50,631** | of 2,776,734 CONUS reaches |

Nearest large gauge to the core sites: **Iowa River at Wapello, 05465500 /
WAPI4**, 41.178 N 91.182 W - about 20 km south of S1, on the same river system.
Its record runs to 1914 for daily discharge and holds 123 annual peaks from 1903
to 2025. Record crest 32.15 ft / 188,000 cfs on 2008-06-14.

Full 871-row inventory (USGS + IFIS + NWPS-only, with drainage area, period of
record, parameters and flood thresholds): `derechos_flood_gauge_inventory.csv`
in the project artifacts.

## 1. USGS - which API, and when it dies

**Both work today. The OGC API is the durable one.**
`https://waterservices.usgs.gov/` carries an explicit banner: WaterServices will
be decommissioned in **early 2027**, with migration to
`https://api.waterdata.usgs.gov`. That is *before* the requested July 2027 AMF2
start, so any DERECHOS operational tooling should be written against the OGC API
from the outset. No `Sunset` or `Deprecation` HTTP header is served - the notice
is only on the landing page.

### 1a. Legacy waterservices (still returning data 2026-09-04)

```python
sites = usgs_sites_box()                      # 694 rows x 42 cols, expanded metadata
cat   = usgs_series_catalog()                 # 2923 series rows, one call, whole box
iv    = usgs_iv("05465500", "2024-06-20", "2024-06-30")     # 1054 pts x 2 params
dv    = usgs_dv(sites="05465500", start="2024-01-01", end="2024-12-31",
                parameter_cd="00060", stat_cd="00003")       # 366 daily means
pk    = usgs_peaks_legacy("05465500")         # 123 peaks, 1903-2025, max 188000 cfs
```

`usgs_series_catalog()` is the cheap way to get period of record and parameter
availability for every site in the box in a single request - `begin_date`,
`end_date`, `count_nu` per `(site, data_type_cd, parm_cd, stat_cd)`.

**Host gotchas.** `waterservices.usgs.gov/nwis/iv/` HTTP-redirects to
`nwis.waterservices.usgs.gov`, and the annual-peak service lives only on
`nwis.waterdata.usgs.gov`. Both hosts need their own allowlist entries; the
requests fail at the proxy, not at USGS.

### 1b. OGC API - the replacement grammar

Anonymous, no key. 37 collections at `GET /ogcapi/v0/collections`. The ones that
matter: `monitoring-locations`, `time-series-metadata`, `daily`, `continuous`,
`latest-continuous`, `peaks`, `field-measurements`, `parameter-codes`.

```python
loc  = usgs_ogc_locations_box()                                  # 2331 USGS stream locations
meta = usgs_ogc_timeseries_meta("05465500")                      # begin/end per series
day  = usgs_ogc_series("daily", "05465500", parameter_code="00060",
                       datetime_range="2024-01-01/2024-12-31")
cont = usgs_ogc_series("continuous", "05465500", parameter_code="00065",
                       datetime_range="2024-06-20T00:00:00Z/2024-06-30T00:00:00Z")
peak = usgs_ogc_series("peaks", "05465500", parameter_code="00065", sortby="-time")
```

Grammar notes, all measured:

- `monitoring_location_id` **must** carry the `USGS-` prefix, and a
  comma-joined list of them works (tested to 20 per call).
- `properties.value` is a **string**. Cast before comparing.
- `time_series_id` is an opaque 32-hex id, not a parameter code.
- Pagination is by **cursor** (`links[rel=next]`); `offset` also shifts
  correctly (verified: page 2 shares zero ids with page 1). `limit` is not
  capped at 1000 - `limit=10001` returned 10001 features.
- `numberMatched` is **never populated**. There is no total count; page until
  `next` disappears.
- The `peaks` collection publishes annual peaks only after water-year approval:
  as of 2026-09-04 the latest peak at 05465500 was **2025-08-02**, so the
  2026 water year is absent.

### Gotchas where the service silently returns the wrong answer

**`monitoring-locations` is the site *inventory*, not the gauge network.** The
box returns **2360** stream locations, against **248** from the legacy site
service filtered to active sites with an instantaneous 00060/00065 series - a
factor of ten. It also mixes agencies: 2331 USGS, 16 Indiana DNR (`IN033`),
12 USACE (`USCE`), 1 Illinois DOT (`IL004`). Filter by `agency_code` and join
against `time-series-metadata` or you will report a ten-times-too-large network.

**`datetime` is silently ignored by the `peaks` collection.** `datetime=` on
`daily` and `continuous` works. On `peaks`, the same parameter returns HTTP 200
with **zero** features and no warning. Fetch the whole record and filter locally,
or use `sortby=-time`.

**Daily gage height is a MEAN, not a maximum.** Over the DERECHOS box, 00065
daily series exist at 183 sites - and 182 of them publish only `statCd=00003`
(daily mean). `statCd=00001` (daily max) exists at exactly **one** site. A
domain flood scan built on daily values therefore understates every crest;
the `dv` request will succeed and return plausible numbers. Use `continuous` /
`iv` (00065) or the annual-peak record for peak stage. The coverage hole is
worse than that: a whole-box 00065 `dv` pull returned series at only **158**
sites, and **none** of the eight gauges in the §6 event case has one. Daily
gage height is not a usable domain flood screen in this domain at all - the
Iowa half of the §6 event had to be found through the annual-peak record.

### Parameter codes present in the domain

47 distinct codes across 2923 series. Site counts for the ones you will want:
**00060** discharge 373 sites, **00065** gage height 286, **00010** water
temperature, **00045** precipitation total **42 sites**, 00095 specific
conductance, 00300 dissolved oxygen, 63680 turbidity, 99133 nitrate.

**There is no soil-moisture parameter at any USGS site in the DERECHOS box.**
Checked explicitly against the full 47-code list for 74207, 99968 and the
72180-72189 block: none present. USGS gives you the runoff side of H2's water
balance and nothing of the storage side - that stays with IEM ISUSM
(`derechos-data-sources` §2) and the proposed SoilVue10 installs.

## 2. NOAA National Water Prediction Service (NWPS)

`https://api.water.noaa.gov/nwps/v1`. Anonymous. This is where the **flood
categories** live, and they are not in USGS.

```python
g   = nwps_gauges_box()                 # 353 gauges, with current status
th  = nwps_flood_categories("WAPI4")    # thresholds + reachId + historic crests
obs, fcst = nwps_stageflow("WAPI4")     # 2724 observed pts, 28 forecast pts
q, reach  = nwps_reach_streamflow("11919825", "short_range")   # NWM, no S3
flood_category(21.95, th)               # -> 'minor'
```

`nwps_flood_categories("WAPI4")` returns, verified: `usgsId` 05465500,
`reachId` 11919825, action 18.5 / minor 21 / moderate 25 / major 27.5 ft, and a
historic-crest list whose top entry is **32.15 ft, 188,000 cfs, 2008-06-14** -
identical to the USGS annual-peak record for the same site, so the two datums
agree at this gauge.

`/gauges/{lid}` also carries `pedts` (SHEF physical element for the observed and
forecast series), the `rfc` and `wfo`, and `lro` long-range outlook
probabilities. `/reaches/{reachId}/streamflow` returns the operational NWM
analysis-assimilation, short-, medium- and long-range series plus
`route.upstream` / `route.downstream` reach ids - real-time NWM without touching
S3 at all.

### The trap: `bbox` without `srid` returns zero, and a typo returns everything

Measured over a small test box:

| parameters | HTTP | gauges returned |
|---|---|---|
| `bbox.xmin/ymin/xmax/ymax` + **`srid=EPSG_4326`** | 200 | **6** (correct) |
| `bbox.xmin/ymin/xmax/ymax` alone | 200 | **0** |
| `bbox=csv` | 400 | - (honest error) |
| `xmin/ymin/xmax/ymax` (flat) | 200 | **12873** (whole nation) |
| `state=IA` | 200 | **12873** |
| `wfo=DVN` | 200 | **12873** |

So the spatial filter has two silent failure modes in opposite directions:
forget `srid` and you conclude there are no gauges; misspell the parameter and
you silently get the national list with HTTP 200. `nwps_gauges_box` asserts the
returned longitudes lie inside the requested box. Note also that `state` and
`wfo` are **not** supported filters despite being obvious - do the filtering
client-side.

### Other NWPS gotchas

- **`-9999` is the missing sentinel** for a flood threshold, not `null`. 119 of
  353 gauges in the box have `minor.stage = -9999`; the `flow` thresholds are
  `-9999` at essentially every stage-based gauge. Treating -9999 as a stage puts
  every gauge in major flood.
- **The observed series is a ~30-day rolling window, not an archive.** Measured
  at WAPI4 on 2026-09-05: observed spans 2026-08-06 to 2026-09-05 (2724 points
  at 15 min); forecast spans 6.75 days (28 points, 6-hourly). For any historical
  event go to USGS `continuous`/`iv` or the IEM HADS archive.
- `status.observed.floodCategory` in the box: 237 `no_flooding`, 86
  `not_defined`, 19 `out_of_service`, 6 `obs_not_current`, 5 `low_threshold`.
  `not_defined` means no threshold, not "no flood".
- `/gauges/{lid}` 404s with `code: 5, "[X] could not find gauge ID"` for a
  plausible-looking LID (`DVNI4` does not exist). A bare `/gauges` with no
  spatial filter downloads the whole national list and took **~4 minutes** from
  this sandbox - do not do it by accident.
- No OpenAPI document is served: `/openapi.json` and `/swagger.json` 404 and
  `/docs` returns a Swagger UI shell whose static assets are missing. The user
  guide at `water.noaa.gov/about/api` is the only reference.

## 3. Iowa Flood Center IFIS - a real regional asset with no real API

The IFC operates its own bridge-mounted stream-stage network across Iowa, which
is genuinely distinctive: it instruments small and mid-size streams that USGS
does not gauge, which is exactly the scale at which convective-rainfall runoff
is generated. **In the DERECHOS box: 222 IFC-native sensors, 260 of 322
stream-type objects reporting a stage within the last 30 days.**

There is **no documented JSON web service**. `ifis.iowafloodcenter.org/api/`,
`/ws/`, `/sensors/` and `/ifc/` all 404; `/hlm-plus/api/` and `/ifis/layers/...`
are 403. What works are endpoints reverse-engineered from the app bundles:

```python
obj  = ifis_objects()                      # 1951 objects statewide, JS array-of-arrays
s    = ifis_sensor(747, obj_type=4)        # Ioway Creek | Stange RD | Ames, SQWCR02
hs   = ifis_hydrostations()                # 59 IFC hydrostations, real JSON
```

- `inc/inc_get_object.php?id=0` (legacy app) returns the statewide object list as
  a **JavaScript** array-of-arrays: `[[html],['rainmetadata'],[[id,lat,lon,type,..],...]]`.
  `json.loads` fails on it. `id` with no value returns HTTP 500.
- `obj_type` is the IFIS data **panel** type, not a sensor class: 2/3/4 stream
  gauge, 8 outlet graph, 11 rain calendar, 15 hydrostation, 17 well.
- `chart/chart-bridge.php?id=&type=` renders for **any** id and always labels
  itself `Stream Sensor (IFC)`, so the panel header is not a classifier. What is
  real is `Sensor ID`, `Water Elevation` and `Last Reported`. A dead or
  non-stream sensor returns `no data available` and `Dec 31, 1969 6:00 pm`
  (epoch zero) rather than an error.
- Water elevation comes back as a **string in feet and inches**
  (`888 ft 1 in`), referenced to the sensor datum - usually absolute elevation
  for IFC sensors and stage for USGS-relayed ones. Do not mix the two in one
  plot.
- The 2025 app's only working object endpoint is
  `hlm-plus/api/getObjectList/?otype=15` (59 IFC hydrostations). Every other
  `otype` from 0 to 40 returns HTTP 200 with a zero-length body.
- `chart-bridge.php` also embeds a 120-hour hourly stage series as two JS arrays
  (`data1`, `data2`) that abut at the current hour, with `0.0` as the fill for
  the unpopulated half. It is a chart payload, not a data product; treat it as
  fragile.

**The durable path to IFC data is NWPS, not IFIS.** 65 of the 353 NWPS gauges in
the box are IFC sensors - their names end `--IFC` and they carry NWS LIDs,
flood-category thresholds and the same 30-day observed series as any other
gauge. Coordinate match is exact: IFIS object 747 at 42.036626, -93.645004 is
NWPS `AMQI4` at the identical coordinates. 180 of the 322 IFIS objects matched an
NWPS gauge to within 0.002 deg. So:

- want a **hydrograph** or a flood threshold for an IFC sensor -> use NWPS by LID;
- want the **full sensor inventory** including sensors not relayed to NWS -> use
  `ifis_objects` + `ifis_sensor`;
- want an **archive** -> there is no good one. **IFC sensors are not in HADS**:
  zero of the 65 IFC LIDs in the box appear in `all_dcp_defs.txt` (against 241
  of the 353 NWPS box LIDs overall), so the IEM `IA_DCP` archive does not cover
  them. NWPS gives you 30 days, IFIS gives you 5, and past that the record is
  only obtainable from IFC directly.

Etiquette: `ifis_sensor` is one HTTP request per sensor against a university
server. A 322-object pass at 0.12 s spacing took 75 s. Keep concurrency at 1.

**Action for the campaign lead:** ask IFC/IIHR (University of Iowa) directly for
a bulk sensor export and archive access. Everything above is scraping and will
break when the 2025 app fully replaces the legacy one.

## 4. HADS / DCP

**`hads.ncep.noaa.gov`'s own data servlet is effectively dead for programmatic
use.** `nexhads2/servlet/DecodedData` returns **HTTP 200 with a zero-byte body**
for every parameter combination tried (`state`, `hsa`, `of`, `sinceday`,
`nesdis_ids`, `extraids`, GET and POST, with and without `data=Get+Data`). With
no parameters at all it returns a 4.9 kB page whose form and JavaScript assets
are 404. `/USGS/ALL_DCP.shefs`, `/dcp_defs/`, `/hads/DCP_data/` and
`/hads/USGS/` are all 403.

What does work:

```python
d = hads_dcp_defs(states=["IA", "IL"])                  # national defs, filtered
h = hads_via_iem("WAPI4", "2024-06-20", "2024-06-30")   # 887 rows, 15-min SHEF
```

- `compressed_defs/all_dcp_defs.txt` is a **23 MB** pipe-delimited national
  station-definition table: NESDIS id, NWS LID, owner, state, HSA, lat/lon in
  degrees-minutes-seconds, elevation, **transmission interval**, name, flag, then
  repeating SHEF physical-element blocks (`HG`, `PC`, `US`, `UD`, `UP`, `TA`,
  ...). Field 8 is the interval and field **9** is the name - offsetting by one
  silently puts `60` in your station-name column. This is the authoritative DCP
  metadata. Filtered to IA + IL it gives **534** DCPs, **295** of them inside the
  DERECHOS box, each with its owner code (`USGS01`, `CEMVR1`, `NWSARH`, ...).
- **IEM is the data path.** `mesonet.agron.iastate.edu/cgi-bin/request/hads.py`
  with `network=IA_DCP` (or `IL_DCP`) returns 15-minute SHEF observations.
  Verified at WAPI4 for 2024-06-20 to 06-30: 887 rows, columns `HGIRGZZ` (stage,
  ft), `PCIRGZZ` (accumulated precipitation), `PPHRGZZ` (incremental
  precipitation), `VBIRGZZ` (battery volts). One network per call, one call per
  whole date range - see the IEM etiquette note in `derechos-data-sources`.

## 5. National Water Model

### 5a. Operational, `noaa-nwm-pds` (anonymous S3)

```python
k = nwm_pds_keys("20260901", "short_range", "t00z", "channel_rt")   # 18 keys
```

Layout: `nwm.YYYYMMDD/<configuration>/nwm.t{HH}z.<configuration>.<product>.{f###|tm##}.conus.nc`.
73 configurations per day (CONUS plus Alaska/Hawaii/PR/coastal variants);
products `channel_rt`, `land`, `terrain_rt`, `reservoir`, plus
`forcing_*` and `usgs_timeslices` (the streamflow observations fed to data
assimilation). One hourly CONUS `channel_rt` file is **12.2 MB**.

**This bucket is a rolling window, not an archive.** On 2026-09-05 it held
`nwm.20250101` through `nwm.20260905` - 613 day prefixes, about 20 months. For
anything older you need the retrospective.

Simplest real-time route: skip S3 entirely and use
`nwps_reach_streamflow(reach_id, "short_range")`.

### 5b. v3.0 retrospective Zarr - verified, and expensive in a specific way

```python
ds  = nwm_retro_open()                 # 14.6 s to open
m   = nwm_gage_map(ds)                 # 8660 gauged reaches, gage_id -> feature_id
idx = nwm_box_features(ds)             # 50,631 reaches in the DERECHOS box
```

`noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr`, anonymous, consolidated
metadata. **51 TB**, hourly **1979-02-01 to 2023-02-01** (385,704 steps),
**2,776,734** reaches. Variables: `streamflow`, `velocity`, `q_lateral`,
`qSfcLatRunoff`, `qBucket`, `qBtmVertRunoff`. Coordinates carry `latitude`,
`longitude`, `elevation`, `order` and `gage_id`.

**Reach to feature_id / COMID, two independent confirmations.** The `gage_id`
coordinate maps USGS site numbers straight onto `feature_id`: 05465500 (Iowa
River at Wapello) -> **11919825**, which is exactly the `reachId` NWPS returns
for `WAPI4`. 05454500 (Iowa River at Iowa City) -> 11916315. Only **8660** of
2.78 M reaches carry a gage_id, so for an ungauged reach you still need NHDPlus
or the NWPS `/reaches` route graph.

**Cost, measured from this sandbox.** Chunking is `(672 time, 30000 feature)` =
**161 MB decompressed per chunk**, and `feature_id` is **not spatially sorted**:

| request | wall time | output |
|---|---|---|
| 1 reach x 1 month (721 hourly steps) | **36 s** | 721 values |
| 1 reach x 1 year (8760 steps) | **98 s** | 8760 values |
| all 50,631 box reaches x 24 h | **152 s** | 9.7 MB |

The 50,631 DERECHOS-box reaches are spread across **21 of the 93 feature
chunks**, so a bounding-box subset reads ~3.4 GB to return 9.7 MB - only about
4x the cost of a single point for 50,000x the data. **Never loop reach-by-reach.
Pull a domain slab once, cache it, and slice locally.**

Sanity check that the archive is real: at 05465500 the retrospective's peak for
June 2008 is **5086.3 m3/s = 179,600 cfs on 2008-06-14 14:00Z**, against the
observed USGS annual peak of **188,000 cfs on 2008-06-14** - 4.5 % low, same day.

### Analysis-ready mirrors

`noaa-nwm-retrospective-3-0-pds` (`CONUS|Alaska|Hawaii|PR`, each with
`netcdf/` and `zarr/`) and `noaa-nwm-retrospective-2-1-pds`
(`forcing/`, `model_output/`) are both reachable anonymously. The v3.0 Zarr
above **is** the analysis-ready mirror; there is no Icechunk store in either
bucket. `ciroh-nwm-zarr` is not allowlisted and was not requested.

## 6. Worked result - the 30 July to 2 August 2025 eastern-Iowa flood

Event selection was data-driven, not assumed. Scanning USGS daily-mean gage
height for the whole box from 2024-01-01 to 2026-09-04 against NWPS minor flood
stage gave two clusters: 2026-04-17/25 (up to **23** sites at or above minor,
Rock/Des Plaines/Pecatonica - the eastern, Illinois half of the domain) and
2024-07-16/18 (13 sites, same basins). For eastern **Iowa** specifically,
annual peak stage against NWPS thresholds for the 71 Iowa gauges in the box
identified three events: May 2024 (Iowa River basin, major at Sigourney), late
June/early July 2024 (Cedar basin) and **30 July - 2 August 2025** - the most
recent multi-gauge flood, and the one closest to the DERECHOS core sites.

Independent confirmation: the NWS issued flood watches and warnings for
portions of the Cedar, Wapsipinicon, Iowa, North Skunk and English rivers over
that window, with closures in Iowa, Keokuk, Washington, Linn, Cedar, Jones and
Black Hawk counties.

Instantaneous 00065 crests, and their NWPS category:

| Gauge | Drainage (mi2) | Crest (ft, UTC) | action / minor / moderate / major | Category |
|---|---|---|---|---|
| English R at Kalona, 05455500 / KALI4 | 574 | **16.15**, 31 Jul 02:00 | 13 / 14 / 16 / 18 | **moderate** |
| Iowa R at Marengo, 05453100 / MROI4 | 2794 | **17.56**, 31 Jul 07:30 | 13 / 15 / 17 / 19 | **moderate** |
| N Skunk R nr Sigourney, 05472500 / SIGI4 | 730 | **18.47**, 30 Jul 17:15 | 14.5 / 16 / 18 / 21 | **moderate** |
| Iowa R nr Tama, 05451770 / TMAI4 | 1882 | **13.63**, 1 Aug 17:00 | 11 / 12.5 / 13 / 14 | **moderate** |
| Big Bear Ck at Ladora, 05453000 / LADI4 | 189 | **22.59**, 31 Jul 02:00 | 19 / 20 / - / - | minor |
| Iowa R at Wapello, 05465500 / WAPI4 | 12500 | **21.95**, 2 Aug 05:45 | 18.5 / 21 / 25 / 27.5 | minor |
| Iowa R at Oakville, 05465700 / OKVI4 | 12630 | **11.94**, 2 Aug 13:30 | 8 / 11 / 15 / 20 | minor |
| Cedar R at Cedar Rapids, 05464500 / CIDI4 | 6510 | **12.69**, 4 Aug 09:30 | 10 / 12 / 14 / 16 | minor |

Instantaneous crests reproduce the published annual peak stage exactly at all
eight gauges, which cross-validates the `continuous`/`iv` path against the
`peaks` collection.

Figure: `derechos_2025_flood_hydrographs.png` - four hydrographs with NWS
flood-category bands, each panel labelled with its own crest category (moderate
at Kalona, Marengo and Sigourney; **minor** at Wapello, whose 21.95 ft crest sits
between its minor 21 and moderate 25 thresholds). The shape is the
DERECHOS-relevant point, and it is
measured: English River at Kalona (574 mi2) rose **8.37 ft in 42 h** (7.78 ft on
29 Jul 08:00Z to 16.15 ft on 31 Jul 02:00Z) and was back below action stage
**55 h** after its crest; North Skunk at Sigourney (730 mi2) rose **9.11 ft in
33 h**. Iowa River at Wapello (12,500 mi2), 100 km downstream of Marengo, held
above minor flood stage for **211 h** - 8.8 days. A convective event's runoff
signature is only resolvable at the small-basin gauges, and those are exactly
the ones the IFC network densifies.

## What is verified

Exercised live on **2026-09-04/05** from this sandbox:

- **USGS legacy** - `site` (bbox, expanded, series catalog), `iv` (00060+00065,
  1054 points), `dv` (00060 366 daily means; a whole-box 00065 pull returning
  159 series / 145,795 rows), `peak` (123 annual peaks at 05465500).
- **USGS OGC API** - `collections` (37), `monitoring-locations` bbox with cursor
  paging (2360 stream locations), `daily`, `continuous`, `peaks`,
  `time-series-metadata`, `latest-continuous`; the `datetime`-on-`peaks` failure
  and the `offset` vs cursor comparison.
- **NWPS** - `/gauges` bbox with and without `srid` and with four wrong
  spellings; `/gauges/{lid}` for all 353 box gauges (thresholds + crests);
  `/gauges/{lid}/stageflow` and its `/observed` and `/forecast` sub-paths;
  `/reaches/{reachId}/streamflow` returning an operational short-range series.
- **IFIS** - `inc_get_object.php?id=0` (1951 objects), `chart-bridge.php` for
  322 in-box objects, `chart-usgs.php`, `chart-raingauge.php`,
  `chart-hydrostation.php`, `getObjectList` for otype 0-40,
  `hlm-plus/api/alert`, `getQpeak/issueTime.php`, `getDroughtUSDM`.
- **HADS** - `compressed_defs/all_dcp_defs.txt` (23 MB) downloaded;
  `DecodedData` probed eight ways; IEM `hads.py` for WAPI4 (887 rows of 15-min
  SHEF).
- **NWM** - `noaa-nwm-pds` prefix listing and per-day configuration listing,
  one file HEAD-sized; v3.0 retrospective `chrtout.zarr` opened, `gage_id` map
  extracted, point and domain-subset timings measured, a 2008 peak compared
  against the observed record.

### Not verified

- **HADS `DecodedData` observations** - the servlet answers HTTP 200 with an
  empty body for every parameter set tried. No recipe. Use IEM.
- **IFIS time series as data** - the 120-hour `data1`/`data2` arrays inside
  `chart-bridge.php` were observed but not parsed into a validated product, and
  which array is observed versus forecast was not established.
- **IFIS forecast products** - `hlm-plus/api/getFlowHLM`, `getQpeak`,
  `getBasin`, `getInunTile`, `getVtilePbf` all respond but their outputs were
  not decoded (`getFlowHLM/refTime` returned `{"refTime": -1}`, i.e. no current
  forecast at fetch time).
- **NWM v2.1 retrospective** - bucket listed, no store opened.
- **NWM operational file contents** - keys and sizes verified; no `channel_rt`
  NetCDF was downloaded and read.
- **Datum consistency between USGS 00065 and NWS stage** - verified to agree at
  05465500/WAPI4 only (crest 32.15 ft matches both records). Not checked at the
  other 245 matched gauges. Check per gauge before comparing a USGS stage
  against an NWS threshold.
- **IFIS rain-gauge and well objects** - counted from the object list (474 rain,
  105 well in box) but not fetched or classified.
- **Any archive of IFC stream stage** - none was found. NWPS holds 30 days, the
  IFIS chart payload 5 days, and HADS/IEM does not carry IFC sensors at all.
- **NWM streamflow at the DERECHOS core sites** - only the Wapello reach was
  extracted.

### Network grants this skill depends on

Granted while building it: `nwis.waterservices.usgs.gov`,
`nwis.waterdata.usgs.gov`, `hads.ncep.noaa.gov`,
`noaa-nwm-retrospective-2-1-pds.s3.amazonaws.com`,
`noaa-nwm-retrospective-3-0-pds.s3.amazonaws.com`. Already allowlisted for this
work: `api.waterdata.usgs.gov`, `api.water.noaa.gov`,
`ifis.iowafloodcenter.org`, `noaa-nwm-pds.s3.amazonaws.com`. Default-reachable:
`waterservices.usgs.gov`, `mesonet.agron.iastate.edu`. No credentials are needed
by any recipe here.

## Related skills

`derechos-campaign` (science case - load first), `derechos-data-sources` (IEM
ISUSM soil moisture, ASOS, RAOB, NEXRAD, CDL, Sentinel-2, mPING, HRRR - do not
duplicate).
