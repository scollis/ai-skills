---
name: derechos-iowa-dot
description: Iowa DOT road-weather and transport data for the DERECHOS campaign - RWIS road-surface temperature and pavement condition (live services plus the 26-year IEM archive), Iowa 511 winter road conditions, historic road-condition archives by winter season, snowplow AVL and dashcam imagery, plow-photo ML classifications, crash records with weather and surface-condition codes, AADT traffic counts, the RAMS road network and bridges. Use when fetching or discovering Iowa DOT / gis.iowadot.gov / data.iowadot.gov / IA_RWIS data, when working the ArcGIS REST query grammar for these servers, or when building freezing-rain, winter-precipitation-type, derecho-wind or flood road-impact analyses over the Iowa-Illinois domain.
---

# DERECHOS - Iowa DOT road weather and transport

Working access patterns for Iowa Department of Transportation data. Everything below was
exercised against the live service on **2026-09-05** from this sandbox; the closing
sections state exactly what passed and what did not.

Load `derechos-campaign` for the science case (H1-H4, SQ1-SQ7, traceability matrix) and
`derechos-data-sources` for the regional non-DOT sources. **This skill complements
`derechos-data-sources`, it does not repeat it** - CropScape CDL point queries, Sentinel-2
via Element84, IEM ASOS/ISUSM/RAOB basics, NEXRAD listing, mPING and HRRR all live there.
The one overlap is deliberate: `derechos-data-sources` covers IEM's ASOS and ISUSM
services; this skill adds IEM's **RWIS** service, which it does not cover at all.

`kernel.py` auto-loads the helpers named below.

## Why the DOT matters to DERECHOS

Two reasons, and the second is the one that gets forgotten.

1. **Impact ground truth.** H3/SQ3 is about freezing-rain severity and winter
   precipitation-type transitions; SQ6 is about grid- and infrastructure-impacting wind.
   Iowa DOT holds the only quantified, spatially resolved record of what those events did
   to surface transport in this domain: road-condition change records, crash records coded
   by weather *and* pavement surface condition, and salt/plow effort per road segment.
2. **RWIS is a dense surface met network that measures a variable nobody else does.**
   52 RWIS stations sit inside the DERECHOS box reporting air temperature, dew point and
   wind at 10-20 minute cadence, and 120 pavement sensors report **road-surface
   temperature**. No ARM instrument, no ASOS, no ISUSM station in the domain measures
   pavement temperature. For the freezing-rain problem it is the controlling variable:
   ice accretes when the *surface* is sub-freezing, which is not the same question as
   whether the air is.

Measured example of exactly that divergence, Burlington RWIS (`RBUI4`) through the whole
freezing-rain window of 14 Dec 2024: **air 32.0-32.4 degF while the pavement held
31.3-31.8 degF**. An air-temperature-only analysis calls that event non-freezing.

## Source to science question

`derechos_iadot_sources()` returns this as data; `derechos_iadot_sources(sq=3)` filters it.

| Source | What it provides over the domain | Serves | Status |
|---|---|---|---|
| **RWIS atmospheric** (live) | 94 stations statewide / **52 in box**; air T, Td, RH, wind avg+max, precip type/intensity/rate/accum, visibility | SQ2, SQ3, SQ6 | verified |
| **RWIS surface** (live) | 203 pavement sensors / **120 in box**; pavement T, surface condition, ice %, freeze point, friction index | SQ3 | verified |
| **RWIS archive via IEM** | 59 IA stations in box, record from **2000-02-08**; the only historical road-surface temperature | SQ2, SQ3 | verified |
| **RWIS cameras** | 68 sites / 305 positions, **146 positions in box**, 10 rolling images each | SQ3 | verified |
| **Iowa 511 winter road conditions** | 1014 CARS segments / 563 in box, current condition + pavement phrase | SQ3 | verified |
| **Historic road conditions** | Road-condition change records per winter season, 2019-2026 | SQ3, SQ6 | partial (1 season token-gated) |
| **Crash records** | **452,586 in box**, 2015-01-01 to 2026-09-02, coded weather + surface condition + severity | SQ3, SQ6 | verified |
| **Snowplow AVL** (live) | Per-truck **road temp + air temp**, plow state, material rate - a mobile road-weather platform | SQ3 | partial (off-season empty, no archive) |
| **Plow dashcam images** | Rolling 1 h of geolocated forward-view JPEGs | SQ3, and the §4.2.4 CV thrust | verified |
| **Plow photo ML classifications** | Road-surface class + confidence + model version on plow imagery | SQ3 | partial (off-season empty) |
| **Winter storm analysis 48 h** | Salt/liquid quantity, passes, mean road+air T, cost per segment | SQ3, SQ6 | partial (off-season empty) |
| **AADT / traffic log book** | 4299 segments in box with truck/bus split - exposure weighting | SQ6 | verified |
| **RAMS road network** | 208,314 LRS segments in box, 122 attributes | SQ3, SQ6 | verified |
| **Bridges / structures** | 11,018 bridge points in box + historic inspection table | SQ6 | verified |
| **Iowa 511 native API** | - | SQ3 | **dead** (502 on CONNECT after grant) |
| **Flood Images** | 687 photos, **all in western Iowa - none in the box** | - | verified empty |

## 1. Where the data actually lives - three hosts, and only two matter

`data.iowadot.gov` is an **ArcGIS Hub site**, not a data server. Its useful surface is an
OGC API Records endpoint that indexes 162 datasets (2026-09-05):

```python
cat = iadot_catalogue()                 # 162 rows: title, type, url, tags
iadot_catalogue(match="rwis|winter|plow")
```

Every one of the 162 items is type `Feature Service`; **145 point at
`services.arcgis.com/8lRhdTsQyJpO52F1` (ArcGIS Online) and 16 at `gis.iowadot.gov`.**
That split is the important structural fact: the DOT's real-time and derived winter
products are AGOL hosted feature views, while the authoritative enterprise layers
(crash, road network, bridges, historic road conditions) are on their own server.

`gis.iowadot.gov` is an **IIS root that 404s** - it is not the REST directory. The public
ArcGIS Server instance is `agshost`; `private` returns HTTP 401.

```python
sv = iadot_services()      # ArcGIS Server 11.3, 42 folders, 112 services
sv.groupby("folder").size()
```

Folders that exist and are non-empty: `Bridges_Structures Environmental Exevision Hosted
IADOT_Utilities Maintenance PPMS RAMS Right_of_Way Survey Systems_Planning Test Traffic
Traffic_Operations Traffic_Safety Utilities Winter_Operations`. The folders
**`RWIS`, `Emergency`, `Imagery`, `LiDAR`, `Pavement_Management`, `Construction`** and 19
others are listed by the directory but contain **zero public services** - the folder name
is not evidence that data is there. The RWIS folder being empty is why RWIS access goes
through AGOL, not `agshost`.

### Gotcha: the directory lists services you cannot read

Of 109 public FeatureServer/MapServer endpoints on `agshost`, **107 are open and 2 return
`{"error":{"code":499,"message":"Token Required"}}` with HTTP 200** - specifically
`Winter_Operations/Historic_Iowa_Road_Conditions_2024_2025` (both Feature and Map server).
A `requests` call to it succeeds, `r.status_code == 200`, and `r.json()` has no `layers`
key. `ags_layers()` surfaces the error rather than raising. There is no anonymous route to
the 2024-2025 winter season; the other six seasons are open.

## 2. ArcGIS REST query grammar, verified

All against `.../<service>/<Feature|Map>Server/<layerId>/query`.

```python
ags_layers(url)                       # ids, names, geometry types, maxRecordCount
ags_fields(url, 0)                    # field names/types + coded-value domains
ags_count(url, 0, where, bbox=DERECHOS_BOX)
df = ags_query(url, 0, where="...", bbox=DERECHOS_BOX, out_fields="A,B")
```

| Parameter | Verified behaviour |
|---|---|
| `where` | Standard SQL. Date literals as `FIELD >= TIMESTAMP 'YYYY-MM-DD HH:MM:SS'` - confirmed on `CRASH_DATE` and `CONDITION_CHANGE_START` |
| `geometry` + `geometryType=esriGeometryEnvelope` + **`inSR=4326`** | Envelope as `lon_min,lat_min,lon_max,lat_max` |
| `outFields` | Comma string; `*` for all |
| `f` | `json` and **`geojson`** both work (`geojson` returns a real `FeatureCollection`, attributes under `properties`) |
| `resultOffset` / `resultRecordCount` | Paging. Requests are clamped to the service `maxRecordCount` |
| `returnCountOnly=true` | Cheap; honours the envelope |
| `returnDistinctValues=true` | Works with `returnGeometry=false` - e.g. `ROAD_CONDITION` distinct = `Completely Covered, Impassable, Partially Covered, Seasonal, Travel Not Advised` |
| `orderByFields` | e.g. `AADT DESC` - top AADT segment in box is I-235 at 130,800 |
| `outStatistics` | min/max for date-range discovery, JSON-encoded list |
| `outSR=4326` | Returns lat/lon geometry; the layers are natively Web Mercator |

### Gotcha: omitting `inSR` silently returns zero

A lat/lon envelope **without** `inSR=4326` returns `{"count": 0}` with **HTTP 200 and no
warning** - the server interprets the coordinates in the layer's own spatial reference
(Web Mercator), where `-94.2, 40.7` is a few hundred metres from the origin off West
Africa. Measured on the AADT layer: with `inSR=4326`, 4299 features; without it, 0. This
is the single most dangerous failure mode on these services, because "no features in my
study area" is a plausible-looking answer. `ags_count`/`ags_query` always send `inSR`.

### Gotcha: `maxRecordCount` is not what you asked for

`maxRecordCount` is **1000 on the AGOL views** and **2000 on `agshost`**. Asking for
`resultRecordCount=3000` on Crash_Data returns exactly 2000 features with
`exceededTransferLimit: true`. Page on `resultOffset` and trust the flag, not the row
count, to decide whether to continue.

### Gotcha: string fields carry trailing whitespace

The AADT layer has both `'US 218'` and `'US 218 '` as `ROUTE_NAME` values. Any
`where="ROUTE_NAME='US 218'"` silently drops the trailing-space rows. Use `LIKE 'US 218%'`
or normalise after retrieval.

### Gotcha: layer names are misspelled inconsistently

Four of the six open historic-road-condition seasons name their layer
`Histoic Road Conditions` (2020_2021, 2021_2022, 2022_2023, 2023_2024); the other two
spell it `Historic Road Conditions`. Address layers by **id**, never by name.

## 3. RWIS - the road-weather network

### Live conditions and station metadata (Iowa DOT, AGOL)

```python
atm = iadot_rwis_sites("atmos")     # 94 rows, one per station
srf = iadot_rwis_sites("surface")   # 203 rows, one per pavement sensor
```

These are **current-conditions services**: one row per station or sensor carrying the
latest value plus full site metadata (`LATITUDE LONGITUDE GPS_ALTITUDE ROUTE_NAME
MILE_POST COUNTY_NAME GARAGE_NAME DISTRICT_NO COST_CENTER DATA_LAST_UPDATED`). There is
**no Iowa DOT-hosted RWIS archive** anywhere in the catalogue - the live services are the
whole of what the DOT publishes, and the archive is IEM's.

Atmospheric fields: `AIR_TEMP RELATIVE_HUMIDITY DEW_POINT AVG_WINDSPEED_MPH
MAX_WINDSPEED_MPH AVG/MAX_WINDSPEED_KNOTS WIND_DIRECTION_DEG PRECIPITATION_TYPE
PRECIPITATION_INTENSITY PRECIPITATION_RATE PRECIPITATION_ACCUMULATION VISIBILITY`.

Surface fields: `SENSOR_NAME SURFACE_TEMP SURFACE_CONDITION FREEZE_TEMP ICE_PERCENTAGE
FrictionIndex SENSOR_PRIORITY`. `SENSOR_NAME` names the physical location - e.g.
`US-20 WB Deck (1)`, `I-29 S/B Approach D/L (2)`, `I-380 Driving Ln / Deck (3)` - so a
bridge-deck sensor and a driving-lane sensor at the same site are different rows and
genuinely different measurements. Do not average them blindly.

**`NWS_ID` (e.g. `RBUI4`, `RDVI4`, `RMCI4`) is the IEM `IA_RWIS` station id.** That is the
join key between the live DOT service (which has route, milepost, sensor names, garage)
and the IEM archive (which has the time series).

#### Gotcha: 9999 is the missing sentinel in the surface table

`SURFACE_TEMP`, `FREEZE_TEMP`, `ICE_PERCENTAGE` and `FrictionIndex` return **9999** when
the sensor has nothing to report, not null. `SURFACE_CONDITION` returns the string `NA`.
A mean over the raw column is meaningless. On the 2026-09-05 pull, `FREEZE_TEMP`,
`ICE_PERCENTAGE` and `FrictionIndex` were 9999 at **every** sensor - those three fields
appear to be populated only during active winter chemical treatment.

### The archive: IEM `IA_RWIS`

```python
sta = iem_rwis_network("IA")                      # 106 stations, with archive_begin/end
df  = iem_rwis(["RTPI4","RDVI4"], "2024-12-13", "2024-12-16")
```

Endpoint `https://mesonet.agron.iastate.edu/cgi-bin/request/rwis.py`. The station
parameter is **`stations` (plural)** - `station=` returns HTTP 422 with a pydantic
validation body. Variables (from the live form, verified): `tmpf dwpf feel relh sknt drct
gust tfs0 tfs0_text tfs1 tfs1_text tfs2 tfs2_text tfs3 tfs3_text subf`. `tfsN` are the
pavement-sensor temperatures in degF and `tfsN_text` their condition strings
(`Dry`, `Wet`, `Trace Moisture`, `Ice Warning`, `NA`, ...). Timestamps come back as
`obtime`; cadence is irregular, roughly every 10-20 minutes (~155 obs/station/day).

Etiquette: request the whole range in **one** call; do not loop days.

#### Gotcha: the CGI streams chunked and truncates

A multi-station, multi-week request will occasionally die with
`http.client.IncompleteRead` / `requests.exceptions.ChunkedEncodingError` mid-stream.
Observed once in eight calls. `iem_rwis()` retries four times with backoff. A partial read
raises rather than returning short data, so you cannot silently get a truncated frame -
but do not write a pipeline that treats one attempt as authoritative.

#### Gotcha: `subf` is documented, offered, and empty

`subf` (subsurface temperature) is a selectable variable in IEM's own download form. Over
46 in-box stations across 19,909 observations it is **non-null 0.0 % of the time**. No
Iowa RWIS station reports subsurface temperature. If you want soil temperature in this
domain, use ISUSM (see `derechos-data-sources`).

#### Gotcha: two ingest paths, different precision, no pavement on one

About 3 % of rows (14 of 464 at `RDVI4` over three days) carry air temperature at
sub-0.1 degF precision - `12.000202` rather than `12.4` - a Celsius-converted feed. **12
of those 14 rows have every pavement column blank.** The other 450 rows, at clean 0.1 degF
precision, have pavement data on 100 % of rows. So blank `tfsN` is usually *not* a sensor
outage; it is the other ingest path. Two consequences: do not compute pavement-sensor
uptime from null fraction without splitting on precision, and do not join the two feeds
on temperature equality.

#### Gotcha: `online: true` does not mean data in your window

Four in-box stations flagged `online: true` with `archive_end: null` returned **zero
rows** for 2024-12-13/16: `RCRI4` (Anamosa), `RDEI4` (De Soto), `RMQI4` (Maquoketa),
`RWBI4` (Williamsburg). Three of them returned data for January 2025, so they were simply
gappy; `RDEI4` returned nothing in either window and is effectively stale. Probe the
window you actually need.

### Station geography, measured

59 `IA_RWIS` stations fall inside the DERECHOS box, 48 flagged online, with the original
cohort's record beginning **2000-02-08/21** - a 26-year pre-campaign baseline. 40 of them
have at least one working pavement sensor.

**But the pavement network does not reach the core sites.** The two RWIS stations
physically closest to M1 (SERF) - `ROUI4` Olds at **7.4 km** and `RAII4` Ainsworth at
**11.7 km** - report air temperature and dew point only, no pavement sensors at all. The
nearest station with a pavement sensor is `RTPI4` Tipton (I-80) at **32.1 km from S1**, and
`RIAI4` Iowa City (US 218) at **52.5 km from M1**. Pavement sensors live on the interstate
and primary-highway network; the 2024-vintage rural additions are atmospheric-only. Any
site-scale road-surface analysis at S1/M1 needs either a campaign-deployed surface
sensor or an acceptance that the nearest pavement observation is 30-50 km away.

### Gotcha: Illinois RWIS is effectively gone

The eastern half of the DERECHOS box has almost no road-weather coverage. `IL_RWIS` on IEM
has 117 stations, **52 inside the box, and only 5 online** - `IMC01`-`IMC05`, a McHenry
County highway-department feed in far north-east Illinois (42.18-42.47 N), all beginning
2019. The IDOT cohort (`IL002`-`IL049` and the older `CL15xx` ids) has `archive_end`
clustered on **2016-08-17**; the feed to IEM stopped then. So the NIU/DeKalb and Chicago
anchors have no RWIS pavement temperature, historic or current, and Iowa DOT RWIS is a
western-domain asset only.

### RWIS cameras

```python
cam = iadot_rwis_sites("camera")   # 305 positions across 68 sites; 146 in box
```

Ten rolling image slots per position (`IMAGE_URL_1..10`, `IMAGE_DATE_1..10`), on
`cloud.iowadot.gov`. Verified fetch: HTTP 200, `image/jpeg`, 800x450, with the site,
route, milepost and timestamp burned into the frame - e.g.
`South US 34 @ MM 263.5 near Burlington (RWIS07) 09/04/2026 20:09:12`. Note the image
table grew from 298 to 305 rows during a 90-minute session; it is a live table, not a
fixed station list.

## 4. Winter operations

### Iowa 511 current road conditions

```python
ags_query(IADOT_AGOL + "/511_IA_Road_Conditions_View/FeatureServer", 0, page=1000)
```

1014 CARS road segments statewide, 563 in box, as polylines with `ROAD_CONDITION`,
`HL_PAVEMENT_CONDITION` (a human phrase), `CONDITION_CHANGE_START/END` and
`SEGMENT_LENGTH_MI`. On 2026-09-05 all 1014 read `Seasonal` and the most recent condition
change was **2026-04-07** - the feed is live but it says nothing between April and
November. `511_IA_Road_Conditions_Change_View` (2-hour change) and
`CARS511_Iowa_Critical_View` (critical closures, 0 features on test day) are the same
family.

### Historic road conditions - the impact archive

```python
rc = iadot_road_conditions("2019_2020",
        where="CONDITION_CHANGE_START >= TIMESTAMP '2020-01-18 00:00:00' "
              "AND CONDITION_CHANGE_START <  TIMESTAMP '2020-01-19 12:00:00'",
        bbox=DERECHOS_BOX)
```

One FeatureServer per winter season on `agshost`. Measured feature counts: **2019_2020
58,746 / 2020_2021 67,184 / 2021_2022 52,124 / 2022_2023 54,398 / 2023_2024 39,849 /
2025_2026 28,280**, and 2024_2025 token-gated. Each row is a *condition change* on a road
segment, with `ROAD_CONDITION`, `PREVIOUS_ROAD_CONDITION`, `HL_PAVEMENT_CONDITION`,
`CONDITION_CHANGE_START/END`, `CONDITION_NOT_NORMAL_START/END/ELAPSED`, `SEGMENT_LENGTH_MI`
and district/cost-centre. `PRIMARY_LATITTUDE` (sic) and `SECONDARY_LATITUDE` give segment
endpoints in the older seasons.

The AGOL `Historic_Iowa_Road_Conditions_View` (304,686 features) is a **frozen snapshot**
covering only **2016-10-14 to 2021-04-21** - `hasStaticData: true`. It is the only route to
2016-2019, and it is useless for anything after April 2021. For a recent season use the
per-season `agshost` service.

### Snowplow AVL and dashcams - a mobile road-weather platform

`AVL_Direct_View` carries, per truck: `AIRTEMP`, **`ROADTEMP`**, `VELOCITY`, `HEADING`,
`FRONTPLOWSTATE`, `LEFT/RIGHT/UNDERBELLY` plow states, `SOLIDMATERIAL`/`LIQUIDMATERIAL`
and application rates, `GARAGE_NAME`, `LOGDT`. That is an infrared road-temperature
transect along every plowed route - conceptually the densest road-surface sampling in the
domain. **It had 0 features on 2026-09-05** (no plows running in September) and there is
**no archive service**. To use it the campaign must poll and store it through a winter.

```python
img = iadot_plowcam(bbox=DERECHOS_BOX, fetch=1)   # rolling 1 h
```

`AVL_Images_Past_1HR_View` runs year-round: 85 images statewide over a 2.7-hour window on
test day, 16 inside the box, each with `PHOTO_LATITUDE/LONGITUDE`, `PHOTO_SPEED`,
`PHOTO_BEARING`, `ROUTE_NAME`, `GARAGE_NAME` and a `SECURE_PHOTO_URL`. Verified fetch:
HTTP 200, `image/jpeg`, 640x360, forward view down the travel lane. Two sibling services
exist - `AVL_Images_By_Region_View` and `AVL_Plow_Cam_Images_Minnesota_View` (MnDOT
imagery, useful for the northern edge). Rolling window only; nothing older than an hour.

`Winter_Operations/Plow_Photo_Classifications` (3 layers: past 1 h / 24 h / 7 d) carries
`CLASSIFICATION`, `CONFIDENCE`, `MODEL_VERSION`, `MODEL_TIMESTAMP` on those photos - the
DOT is already running an ML road-surface classifier on plow imagery. That is directly
adjacent to the campaign's §4.2.4 computer-vision thrust and worth talking to them about.
**All three layers had 0 features on 2026-09-05**, so the class vocabulary is unknown -
re-inspect in January.

`Winter_Storm_Analysis_48HR_View` aggregates per road segment over a rolling 48 h:
`TOTAL_SALT_QUANTITY`, `QUANTITY_LIQUID/PREWET`, `NUMBER_PASSES`, `AVERAGE_AIR_TEMP`,
**`AVERAGE_ROAD_TEMP`**, `NUMBER_OF_PINGS`, `LABOR_HOURS` and a full cost breakdown.
0 features off-season; no archive.

### Gotcha: everything winter is empty in summer

Five services central to this skill returned **0 features** on 2026-09-05:
`AVL_Direct_View`, `Winter_Storm_Analysis_48HR_View`, all three
`Plow_Photo_Classifications` layers, and `CARS511_Iowa_Critical_View`. Their schemas are
verified; their content is not. Do not conclude a feed is broken from a September test,
and do not build an analysis that assumes these are populated without checking the month.

## 5. Crash records as a weather-impact metric

```python
c = iadot_crashes("2024-12-14", "2024-12-15", bbox=DERECHOS_BOX)
c.WEATHER_label.value_counts()
```

`Traffic_Safety/Crash_Data` holds **630,409 records statewide, 452,586 inside the box**,
spanning **2015-01-01 to 2026-09-02** - a rolling ~10-year window updated to within days.
Companion services `Crash_Vehicle_Data` and `Crash_Person_Data` join on `CRASH_KEY`.

The fields that make this a weather dataset: `WEATHER` (domain `CRASH_WEATHER`), `CSRFCND`
(`CRASH_SURF_COND`), `LIGHT`, `CSEV` (`CRASH_SEVERITY`), plus `FATALITIES`, `INJURIES`,
`PROPDMG`, `VEHICLES`. **18 of the 48 fields carry coded-value domains** and the raw
values are bare integers - `WEATHER=4` means nothing until decoded. `ags_query(...,
decode=True)` (the default) appends `<FIELD>_label` columns from the domain; `ags_fields()`
returns the maps. `CSEV`: 1 Fatal, 2 Major Injury, 3 Minor Injury, 4 Possible/Unknown,
5 Property Damage Only. Note both `CRASH_DATE` (midnight-truncated) and `CRASH_DATETIME` /
`CRASH_DATETIME_UTC` exist - use `CRASH_DATE` for whole-day windows and the datetime
fields for sub-daily.

## 6. Traffic, network and structures

```python
ags_query(IADOT_AGOL + "/Traffic_Log_Book_AADT_View/FeatureServer", 0,
          bbox=DERECHOS_BOX, page=1000)
```

- **AADT** (`Traffic_Log_Book_AADT_View`): 7437 route sections statewide, **4299 in box**,
  with `AADT`, `TOTALTRUCKBUS`, per-axle-class counts, `ALLVEHICLEMILES`. Within 10 km of
  S1: 27 sections, busiest US 61 at 13,900 AADT (1779 truck/bus). Within 10 km of M1:
  25 sections, busiest US 218 at 11,900 AADT (2267 truck/bus). Useful for weighting an
  impact metric by exposure rather than by segment count.
- **Automatic Traffic Recorders** (`Automatic_Traffic_Recorders_View`): 174 continuous
  count sites, 96 in box - **site metadata only** (`ATR_NUMBER`, factors, speed limit,
  functional class). The count time series is not in this service.
- **RAMS road network** (`RAMS/Road_Network`, agshost): 359,066 segments statewide,
  **208,314 in box**, 122 attributes - the LRS the road-condition and AADT services key
  against. `RAMS/All_Routes`, `RAMS/Reference_Posts` and `RAMS/RAMS_Analysis_Segments` are
  the rest of that family.
- **Bridges** (`Bridges_Structures/Bridges_Structures`, agshost): 23,643 bridge points
  statewide, **11,018 in box**, plus a `Bridge Line` layer and a `Bridge Historic Data`
  table. A parallel `Bridges_Structures_SNBI` service carries the newer national
  bridge-inventory schema. Relevant to SQ6 wind loading and to flood scour.
- **Closure gates** (`Closure_Gate_View`): 37 physical gates statewide, 8 in box, with
  `ACTIVATION_TYPE` and route/milepost.
- **Flood Images** (`Flood_Images_View`): 687 attachment-bearing photo records, and every
  one of them is in **western Iowa** (longitude -95.9 to -95.7, the Missouri River valley).
  **Zero inside the DERECHOS box.** The in-box count of 0 is real, not a query error.

## 7. Worked result - the 14 December 2024 freezing-rain event

The event was **found from data, not assumed**. Scanning the IEM ASOS archive for
`FZRA|FZDZ` present-weather codes at BRL, IOW, CID, DVN, DBQ and MUT over
2019-10-01 to 2026-05-01 returned 742 freezing-precipitation reports; the largest single
day is **2024-12-14 with 106 reports across five stations**, progressing north-east from
Burlington (08Z) through Iowa City and Cedar Rapids (10-13Z) to Davenport (13-21Z) and
Dubuque (14Z-00Z).

What Iowa DOT data says about that day, inside the DERECHOS box:

- **Crashes: 161**, against a December-2024 in-box daily median of 111. Of those,
  **117 coded `Freezing rain/drizzle`** and **130 coded surface `Ice/frost`**; 44 injuries
  and 1 fatality.
- **RWIS pavement vs air**: within each station's own freezing-rain window, pavement
  tracked air to within **-1.0 to +2.9 degF** (median +1.6 to +1.9 at Iowa City, Tipton and
  Davenport; **-0.8 at Burlington**). The day before, under clear sky, the same sensors ran
  up to **+11.1 degF** above air. So the pavement-air offset is large and insolation-driven
  in dry conditions and collapses to near zero once precipitation wets the surface - which
  is exactly when the sign of the offset decides whether ice forms.
- **The Burlington case**: air 32.0-32.4 degF, pavement 31.3-31.8 degF, for the entire
  window. Air says rain; pavement says ice; the crash records for the county say ice.

For a road-condition retrieval the 2024-2025 season is token-gated, so the equivalent was
run on the next-largest event in an open season - **2020-01-18/19** (56 FZRA reports).
In-box: **1,647 road-condition change records**, of which `Partially Covered` 852,
`Seasonal` 495, `Completely Covered` 260 and `Travel Not Advised` 40. Decoding the pavement
phrase: **273 records of ice-covered pavement** (169 partially, 104 completely) and 40
travel-not-advised. That is a defensible, spatially resolved impact label for an H3/SQ3
case study.

Artifacts from this session: `derechos_rwis_station_inventory.csv` (111 stations, 59
IA_RWIS + 52 IL_RWIS in box, with per-station variable coverage and distances to S1/M1/KDVN),
`derechos_iowadot_service_inventory.csv` (20 verified services with measured counts),
`rwis_air_vs_road_20241214.png`.

## What is verified

Exercised against the live service on **2026-09-05** from this sandbox:

- **data.iowadot.gov** - full catalogue walk, 162 dataset records paged out of the OGC API
  Records endpoint.
- **gis.iowadot.gov/agshost** - directory walk (42 folders, 112 services), and a
  token-gating probe of all 109 FeatureServer/MapServer endpoints.
- **ArcGIS REST grammar** - `where` with TIMESTAMP literals, envelope + `inSR`, the
  `inSR`-omitted zero-count failure, `outFields`, `f=geojson`, `resultOffset` paging past
  `maxRecordCount`, `returnCountOnly`, `returnDistinctValues`, `orderByFields`,
  `outStatistics` min/max, coded-value-domain decoding.
- **RWIS live** - atmospheric (94), surface (203), traffic (58) and camera (305) tables
  pulled in full; the 9999 sentinel measured across all sensors.
- **RWIS cameras** - one JPEG fetched from `cloud.iowadot.gov` (800x450, HTTP 200).
- **RWIS archive via IEM** - `IA_RWIS` (106) and `IL_RWIS` (117) station GeoJSON; the
  download form's variable list read from the live page; 19,909 observations across 46
  stations for 2024-12-13/16; five further windows probed (Jan 2025, Feb 2014, Feb 2016,
  May 2010, and the Illinois cohorts); the `IncompleteRead` truncation observed and
  retried through.
- **Historic road conditions** - all seven season services probed; 1,647 in-box records
  retrieved and decoded for the 2020-01-18 event.
- **511** - current conditions pulled in full (1014 segments, all `Seasonal`).
- **Plow imagery** - `AVL_Images_Past_1HR_View` pulled and one JPEG fetched (640x360).
- **Crash data** - date range by `outStatistics`; 161 event-day in-box records with domains
  decoded; a December-2024 daily baseline built from 3,000+ records.
- **AADT / ATR / road network / bridges / closure gates / flood images** - schemas read and
  in-box counts measured.
- **IEM ASOS** - 564,684 present-weather rows over 2019-2026 at six stations, used to find
  the event.

All **13** helpers in `kernel.py` were enumerated from the published file with `ast` and
called in a single pass after publication: 13 defined, 13 called, 0 missed. That pass
deliberately used a *different* event and different stations from the worked examples above
- the 22 Feb 2023 freezing-rain day (50 ASOS reports) at `RQCI4` Quad Cities - so the
recipes are not tuned to one case. Cross-check results: `iem_rwis` 261 obs with a minimum
air temperature of 31.0 degF; `iadot_road_conditions("2022_2023")` 737 in-box condition
changes (360 Partially Covered, 309 Seasonal, 68 Completely Covered); `iadot_crashes`
90 in-box crashes of which 36 coded surface `Ice/frost`. It also exercised
`ags_layers`/`ags_fields`/`ags_query` against services the worked examples never touch
(`Traffic_Operations/ATMS_Layers`, 118,544 rows over 42 fields in box, and
`Bridges_Structures` with 156 fields) - note ATMS_Layers includes a layer id 12 named
`Incompatible Layer` with a null geometry type, which `ags_query` cannot read.

### Not verified

- **`Winter_Operations/Historic_Iowa_Road_Conditions_2024_2025`** - token-gated (error 499).
  No anonymous route; the 2024-2025 winter is missing from the open archive.
- **`gis.iowadot.gov/private`** - HTTP 401. Not attempted further.
- **Snowplow AVL live truck feed, Winter Storm Analysis 48 h, Plow Photo Classifications,
  511 Critical Closures** - schemas verified, **content not**: 0 features in September.
  Their class vocabularies and value ranges are unknown until winter.
- **`api.iowaroadconditions.org`** - allowlisted on request, then **502 Bad Gateway on the
  CONNECT tunnel** on every attempt. Same signature `derechos-data-sources` records for
  AmeriFlux. `api.511ia.org` and `511ia.org` were never granted. No recipe here is tested;
  the AGOL CARS mirrors cover the same feed and are open, so this is a documented dead end
  rather than a gap.
- **ATR count time series** - only site metadata is in the service; where the actual
  continuous counts are published was not established.
- **Bridge attachment images and Flood Images attachments** - `hasAttachments: true` was
  read from the layer metadata, but no attachment was downloaded.
- **`Bridges_Structures_SNBI`, `Traffic_Operations/ATMS_Layers`, `Exevision_Data`,
  `Maintenance/*` (culverts, lighting, crossovers), `Systems_Planning/ICE`** - listed and
  open, but not queried.

### Network grants this skill depends on

Granted during this session: **`cloud.iowadot.gov`** (required - it hosts every RWIS and
plow-camera JPEG; the feature services only carry URLs) and
**`api.iowaroadconditions.org`** (granted but unreachable, see above). Already reachable:
`data.iowadot.gov`, `gis.iowadot.gov`, `services.arcgis.com`,
`mesonet.agron.iastate.edu`.

### Open actions for the campaign lead

1. **Ask Iowa DOT for a token, or for the 2024-2025 season export.** One winter is missing
   from the otherwise-open 2019-2026 historic road-condition archive, and it happens to
   contain the largest recent freezing-rain event in the domain.
2. **Arrange an AVL feed or archive.** Per-truck road temperature along every plowed route
   is the densest road-surface dataset that exists here, and the DOT publishes only a
   live snapshot. Either negotiate an archive or stand up a poller before the first winter.
3. **Talk to whoever owns `Plow_Photo_Classifications`.** They are already running an ML
   road-surface classifier on plow dashcam imagery - the same problem as the campaign's
   §4.2.4 computer-vision thrust, with a labelled operational stream behind it.
4. **Accept or fix the pavement gap at S1/M1.** Nearest pavement temperature is 32 km from
   S1 and 52 km from M1; the two RWIS stations within 12 km of M1 are atmospheric-only.
   A campaign surface-temperature sensor at the core sites has no substitute.
5. **Do not expect Illinois RWIS.** IDOT's feed to IEM ended 2016-08-17. If road-surface
   temperature matters in the eastern domain, it needs a direct IDOT request or a
   deployed sensor.

## Related skills

`derechos-campaign` (science case, traceability matrix - load first),
`derechos-data-sources` (ARM Live, IEM ASOS/ISUSM/RAOB, NEXRAD, CropScape, Sentinel-2,
mPING, HRRR - the non-DOT regional sources; load it rather than re-deriving any of them).
