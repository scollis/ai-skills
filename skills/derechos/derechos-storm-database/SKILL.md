---
name: derechos-storm-database
description: Tested access to the severe-storm and derecho report databases over the DERECHOS Iowa-Illinois domain - NCEI Storm Events (bulk CSV and the search-events REST API), the SPC WCM severe database, SPC daily report CSVs, the SPC derecho archive of Squitieri et al. 2025, IEM Local Storm Reports and the NWS warning/storm-based-warning archive, NWS Damage Assessment Toolkit damage paths, NCEI SWDI radar-derived mesocyclone detections, and NCEI Billion-Dollar Disasters. Use when asked about derechos, QLCS or bow-echo climatology, severe wind or hail or tornado reports, storm report databases, local storm reports, warning polygons, damage surveys, EF-scale damage paths, wind gust records, storm case selection, high-impact storm catalogues, or report population bias. Carries an objective derecho/wind-swath day screening function calibrated against SPC's vetted archive.
---

# DERECHOS storm and derecho databases

Report-based and survey-based severe-storm archives over the DERECHOS domain, plus the
objective wind-swath screen that turns them into a case list. Everything below was
exercised against the live service on **2026-09-05** from this sandbox.

Load `derechos-campaign` for the science case (H1-H4, SQ1-SQ7) and `derechos-data-sources`
for the *in-situ and gridded* regional access recipes (ARM Live, IEM ASOS/ISUSM/RAOB,
NEXRAD Level II listing, CropScape CDL, Sentinel-2, mPING, HRRR). This skill does **not**
repeat those; it is the report/catalogue layer that sits on top of them. Where they touch -
IEM in particular - cross-reference rather than re-derive: `derechos-data-sources` §2 covers
ASOS gust retrieval and station discovery, this skill covers the LSR, warning and AFOS
archives on the same host.

The derecho definition underlying SPC's archive is:
Squitieri, B. J., A. R. Wade, and I. L. Jirak, 2025: On a Modified Definition of a Derecho. Part I: Construction of the Definition and Quantitative Analysis, Bull. Amer. Meteor. Soc., doi:10.1175/bams-d-24-0015.1; Part II: An Updated Spatial Climatology of Derechos, doi:10.1175/bams-d-24-0140.1. Author list and DOIs confirmed against Crossref 2026-09-05.

`kernel.py` auto-loads 27 helpers. Bounding box throughout:
`DERECHOS_BOX = (-94.2, 40.7, -87.4, 42.6)`.

## Source to science question

`storm_sources()` returns this as data; `storm_sources(sq="SQ6")` filters it.

| Source | What it provides over the domain | Basis | Serves | Status |
|---|---|---|---|---|
| **SPC derecho archive** (Squitieri et al. 2025) | The canonical, machine-readable derecho event list. 96 definitive NEXRAD-era events; **50 touch this box** | curated from reports + radar | SQ1, SQ2, SQ6, SQ7 | verified |
| **SPC WCM severe database** | Full 1955-2025 wind/hail (1950-2025 tornado) report record. 20,108 wind / 12,333 hail / 2,707 tornado in box | report | SQ2, SQ6 | verified |
| **NCEI Storm Events** bulk CSV | Same reports plus narratives, damage $, injuries, episode grouping, 51 event types | report | SQ2, SQ3, SQ6 | verified |
| **NCEI Storm Events** `search-events` REST | Ad-hoc state/date/type queries without downloading a year | report | SQ2, SQ6 | verified (1000-row cap) |
| **SPC daily report CSVs** | Same-day / next-day preliminary reports; `today`/`yesterday` aliases | report | SQ6 | verified |
| **IEM Local Storm Reports** | The raw LSRs *with* a measured/estimated qualifier and a source field - 28,694 severe reports in box 2006-2025 | report | SQ2, SQ3, SQ6 | verified |
| **IEM warning / SBW archive** | Warning polygons with wind/hail/tornado/damage tags; forecaster-side ground truth | operational | SQ6, SQ7 | verified |
| **IEM AFOS text archive** | The only machine route to NWS **DVN and LOT damage-survey narratives** | narrative | SQ2, SQ6 | verified |
| **NWS Damage Assessment Toolkit** | Surveyed damage points/paths/polygons with EF scale and estimated wind. 13,001 points in box | survey | SQ2, SQ6 | verified |
| **NCEI SWDI** (`nx3mda`, `nx3hail`, `nx3tvs`) | Radar-derived mesocyclone / hail / TVS detections - a *measurement* proxy independent of population | radar algorithm | SQ2, SQ6 | verified |
| **NCEI Billion-Dollar Disasters** | The cost of record for high-impact events | impact | SQ6 | partial - frozen at 2024 |

**Report-based (population-biased): SPC WCM, NCEI Storm Events, SPC daily reports, IEM LSR.
Measurement-based: the `MG`/`MS` subset of WCM and Storm Events, the `QUALIFIER == 'M'`
subset of IEM LSR, and SWDI radar detections. Survey-based: the DAT.** The quantified size
of the population bias is in §11.

## 1. Is there a derecho database? Yes, since 2025 - and this is the headline

For years the correct answer was "no canonical derecho catalogue exists, screen the wind
reports yourself". That changed. SPC now publishes a derecho archive built on the modified
definition of Squitieri et al. (2025a,b), reachable at
`https://www.spc.noaa.gov/about/derechos/archive/` and linked from the older
`/misc/AbtDerechos/derechofacts.htm` page (whose own text warns that the definition was
revised and that the "About Derechos" pages are stale). It is **eight plain CSVs**, no API,
no key, no landing-page scraping needed once you know the filenames.

```python
arch = spc_derecho_archive()          # downloads and parses all eight
{k: v.shape for k, v in arch["events"].items()}
# {'definitive_nexrad': (96, 11), 'likely_nexrad': (13, 11),
#  'likely_prenexrad': (48, 11), 'possible_prenexrad': (16, 11)}
box = spc_derechos_in_box(arch)       # 50 rows: 26 definitive, 3 likely (NEXRAD),
                                      # 17 likely + 4 possible (pre-NEXRAD)
```

Event tables carry `Event #`, start/end UTC time, start/end lat/lon, `Duration (Hours)`,
`Track Length (Kilometers)`. Definitive NEXRAD-era events span **1996-05-05 to 2025-07-29**,
track length 417-2210 km (median 868), duration 5-23 h (median 10). The four companion
report files give every wind report attributed to each event, with a
**`Report Type` of `Estimated` (11,906), `Measured` (3,669) or `Damage` (692)** - which is
better provenance than the WCM database offers before 2006.

**26 of the 96 definitive derechos (27 %) put at least one wind report inside the DERECHOS
box - 0.87 per year over 1996-2025.** All classes together: 50 events, 1960-2025.

### The number that matters for the campaign

The white paper motivates a two-year deployment with Li et al. (2025)'s ~**4 derechos/year**
in the hot spot. That figure is for ML-detected **bow echoes**. Against SPC's vetted
definition the domain sees **0.87 definitive derechos/year** (26 events 1997-2025 over the
1996-2025 NEXRAD era; 0.97/yr if `likely_nexrad` is included). The archive's two
pre-NEXRAD classes add 17 `likely` (1960-1995) and 4 `possible` (1963-1983), so all 50
box-crossing events span 1960-2025 at 0.76/yr - but pre- and post-NEXRAD rates are not
comparable because detection capability differs, so quote 0.87-0.97/yr for the NEXRAD era.. Both numbers are right for what they measure; quote the one that matches
the claim. If the case library is meant to be derechos *sensu* SPC, two seasons buys
~2 events, and the §5 swath screen (2.2 organized-wind-swath days/year) is what actually
fills an IOP scorecard.

Gotchas: the report CSVs are **latin-1**, not UTF-8 (`pd.read_csv` raises
`UnicodeDecodeError` at byte 154638 of the definitive file otherwise); `Report Type` has one
stray `'Measured '` with a trailing space; 4 of 16,269 reports have an unparseable
timestamp; and event time windows **overlap** (two derechos can be running at once), so
`IntervalIndex.get_indexer` raises `InvalidIndexError` - assign reports to events with an
explicit loop, as `spc_derechos_in_box` does.

## 2. SPC WCM severe report database

The full report record, three files, no key.

```python
w = spc_wcm("wind")     # (562088, 31)   1955-2025
h = spc_wcm("hail")     # (414481, 30)   1955-2025
t = spc_wcm("torn")     # ( 74956, 31)   1950-2025
wb = spc_box(w)         # 20108 reports in the DERECHOS box
```

The current aggregates are **zipped** (`1955-2025_wind.csv.zip`,
`1955-2025_hail.csv.zip`, `1950-2025_torn.csv.zip`). The unzipped
`1955-2025_wind.csv` path 404s; only `1950-2025_all_tornadoes.csv` and
`1950-2025_actual_tornadoes.csv` are served bare. Per-year (`2025_wind.csv`) and per-era
(`90-99_wind.csv`, `55-59_hail.csv`) files also exist. There is no directory index -
`/wcm/data/` returns the ordinary SPC page, so parse the links out of `/wcm/` itself.

Units and conventions, measured on the live files:

- **Wind `mag` is KNOTS.** Hail `mag` is inches (0.13-9.99). The SPC *daily* report CSVs
  (§4) and IEM LSR (§6) use **mph** for the same reports - see §10.
- **`tz == 3` for every one of the 562,088 wind rows**: all times are converted to CST
  (UTC-6, no DST) regardless of the report's own state. Add 6 h for UTC.
- **`mag == 0` on 20.1 % of wind rows** means "magnitude not reported", not calm. It is a
  damage report. Do not let it into a mean.
- **`mt` (magnitude type) exists only from 2006.** Coverage by decade: 0.000 for the 1950s
  through the 1990s, 0.445 in the 2000s, 1.000 from 2010. Values: `EG` 289,631 estimated
  gust, `MG` 44,715 measured gust, `ES` 206, `MS` 42, NaN 227,494. **Before 2006 there is no
  way to tell a measurement from an eyeball estimate in this database.**
- County FIPS arrive split as `stf` (state) + `f1..f4` (up to four counties); build a GEOID
  with `stf.zfill(2) + f1.zfill(3)`.

## 3. NCEI Storm Events Database

### Bulk CSV archive

`https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/` - three families
(`details`, `fatalities`, `locations`), **77 years each, 1950-2026**, all `v1.0`.

```python
ix = ncei_index("details")        # {1950: ('1.0','20260323'), ..., 2026: ('1.0','20260901')}
d  = ncei_fetch([2020])           # (61281, 51)
db = ncei_box(d)                  # 1617 rows with coordinates inside the box
```

**The `_cYYYYMMDD` suffix is a per-year publication stamp and cannot be guessed.** On
2026-09-05 the stamps ranged from `20260323` (most historical years) to `20260901` (the
2026 file); `locations` and `fatalities` carry *different* stamps from `details` for the
same year (2020: details `c20260323`, locations `c20260707`, fatalities `c20260323`).
Always list the directory first. Format documentation sits alongside as
`Storm-Data-Bulk-csv-Format.pdf` and `Storm-Data-Export-Format.pdf`.

### The pre-1996 caveat, stated exactly

Counted from the live files: **1950-1995 details files contain exactly three
`EVENT_TYPE` values - `Tornado`, `Thunderstorm Wind`, `Hail`.** The 1996 file jumps to
**34** types and the 2020 file to **51** (2024: 50, 2025: 48). So any query for High Wind,
Winter Storm, Ice Storm, Flash Flood, Heat or Drought silently returns nothing before 1996 -
not because the weather did not happen but because Storm Data did not tabulate it. For
DERECHOS this bites hardest on **H3/SQ3 freezing rain**: the freezing-rain record starts in
1996, full stop.

### The coordinate trap

`BEGIN_LAT`/`BEGIN_LON` are non-null on only ~60-65 % of modern rows, and the split is not
random - it is exactly the county-vs-zone coding:

| 2020 EVENT_TYPE | rows | with lat/lon |
|---|---|---|
| Thunderstorm Wind | 19,315 | 100 % |
| Hail | 7,677 | 100 % |
| Flash Flood | 3,569 | 100 % |
| Tornado | 1,253 | 100 % |
| **High Wind** | **3,682** | **0 %** |
| **Winter Weather** | **2,910** | **0 %** |
| **Winter Storm** | 2,102 | 0 % |
| **Heavy Snow** | 1,792 | 0 % |
| **Blizzard** | 515 | 0 % |

Every zone-coded (`CZ_TYPE == 'Z'`) event has **no coordinates at all**. A lon/lat box
filter therefore discards 100 % of the High Wind and winter-weather record, which is
precisely the SQ3/SQ6 material. `ncei_box(df, keep_zone=True)` retains them for a separate
`STATE`/`CZ_NAME`/UGC-based filter. 1995 has coordinates on just 3.7 % of rows; 1955 on
100 % (all three legacy types are point events).

### Do not use DAMAGE_PROPERTY as an impact metric

For 2020-08-10 across Iowa and Illinois, Storm Events records **$1.75 M property +
$0.13 M crops = $1.88 M**, with only 51 of 445 rows carrying any dollar figure at all.
NCEI's own Billion-Dollar Disasters entry for the same event -
*"Central Severe Weather - Derecho (August 2020)"* - is **$11.027 B unadjusted, $13.453 B
CPI-adjusted, 4 deaths**. Storm Events captures **0.017 %** of the cost of record. Storm
Events damage is a per-segment NWS field estimate; it is not, and was never meant to be, a
loss total.

```python
bd = ncei_billion_dollar_events()   # (403, 7), 1980-04-10 .. 2024-10-09
```

The Billion-Dollar file is `events-US-1980-2026.csv` but its own title line reads
*"...from 1980-2024"* and the last event is 2024-10-09: **the product is frozen**. Treat it
as a historical reference, not a live feed.

### The `search-events` REST API

The old `/stormevents/csv?...` CGI is **gone** - it 301s to
`/access/storm-events-database/`, a client-side app. Its backend is a small REST API,
undocumented but open:

`https://www.ncei.noaa.gov/access/storm-events-database/api/` with
`state-list` (GET), and `search-events`, `state-counties`, `polygon-counties`,
`csv-results`, `pdf-latex`, `certify` (POST, JSON).

```python
r = ncei_search_events(["Iowa", "Illinois"], "2020-08-10", "2020-08-10",
                       ["Thunderstorm Wind"])
len(r["data"]), r["truncated"]        # 391, False
```

Payload keys: `activeTab`, `stateList` (**title case** - `"Iowa"`, not `"IOWA"`),
`beginDate`/`endDate` as `YYYY-MM-DD`, `eventList`, `countyList`, `hailFilter`,
`tornFilter`, `windFilter`. A malformed payload returns HTTP 200 with
`{"data": [], "error": {"title": "Unable to Retrieve Results"}}`.

**Silent 1000-row cap.** A full-year Iowa+Illinois all-types query returns **exactly 1000**
records with `error: None` and no pagination field, offset parameter or total count. There
is no way to tell a complete 1000-row answer from a truncated one except by narrowing the
query - `ncei_search_events` sets `truncated=True` at the boundary for you. The response
also carries **no coordinates and no magnitude type** (`magnitude` is a display string like
`"65 kts. EG"`). Use the API for reconnaissance; use the bulk CSVs for analysis.
`csv-results` returns `{"data": []}` for the same payload - it needs an event-id list this
skill did not reverse-engineer.

## 4. SPC daily report CSVs

`https://www.spc.noaa.gov/climo/reports/YYMMDD_rpts_{wind,hail,torn,filtered}.csv`, plus
`today_wind.csv` / `yesterday_wind.csv` aliases (both verified 200).

```python
spc_daily_reports("2020-08-10", "wind").shape    # (910, 8)
spc_daily_reports("yesterday", "wind").shape     # (403, 8) on 2026-09-05
```

Columns `Time, Speed, Location, County, State, Lat, Lon, Comments`. Two traps:
**`Speed` is MPH here** (max 130 in box on 2020-08-10, versus 126 *knots* for the same event
in WCM), and it is the literal string **`UNK` on 661 of 910 rows** - damage-only reports -
so the column is `object` dtype and any `.mean()` fails or silently coerces. `Time` is
`HHMM` UTC. These are the *preliminary* reports; the WCM database is the vetted version and
the two will differ.

## 5. The wind-swath screen - and what it can and cannot do

`screen_derecho_days` implements an objective criterion in the spirit of Johns & Hirt
(1987), Coniglio & Stensrud (2004) and Squitieri et al. (2025). It is a **documented,
reusable function, not a hand-picked list.**

Reports are linked into swaths by **single linkage at 100 km in a space-time metric where
one hour counts as 60 km** (a typical MCS translation speed), so a swath is a coherent
moving cluster rather than everything that happened that day. Each swath of each convective
day (12Z-12Z) is then tested:

1. `n_reports >= 30` severe wind reports in the swath;
2. `n_strong >= 3` of them at `>= 65 kt`;
3. no gap `> 3 h` between successive reports in the swath;
4. robust major axis `>= 400 km` - the 2.5-97.5 percentile span along the first principal
   axis, so a handful of outliers cannot inflate it;
5. at least one report of the swath inside the target box.

```python
w = spc_wcm("wind")
wide = w[(w.slon.between(-100, -83)) & (w.slat.between(37, 46))]
passed, cand = screen_derecho_days(wide, box=DERECHOS_BOX)
len(passed)          # 157 days, 1955-2025 -> 2.21 per year
passed[passed.conv_day == "2020-08-10"]
# n_reports 583, n_strong 153, max_gap_h 0.33, major_km 909.2, minor_km 480.7,
# axis_deg 96.7, max_kt 126.0, duration_h 12.2
```

**Screen over a window wider than the box, not the box itself.** The DERECHOS box is only
~565 km across at 41.6 N, so a 400 km major axis measured *inside* it is barely attainable:
the box-only screen finds 32 days and recovers just **8 of 26** SPC-archived definitive
derechos. Screening a -100/-83 lon, 37/46 lat window and then requiring a report in the box
recovers **24 of 26 (92 %)**. The 400 km threshold did not need relaxing to 250 km on the
wider window.

**Precision is the honest limitation.** Calibrated against SPC's 26 box-crossing definitive
derechos (1996-2025):

| `min_major_km` | `min_strong` | screened days 1996-2025 | recall | precision |
|---|---|---|---|---|
| 400 | 3 | 143 | 24/26 | 0.17 |
| 400 | 10 | 85 | 24/26 | 0.28 |
| 400 | 20 | 45 | 19/26 | 0.42 |
| 600 | 10 | 42 | 15/26 | 0.36 |
| 700 | 20 | 18 | 7/26 | 0.39 |

Precision never exceeds ~0.42 at any threshold combination. That is not a tuning failure:
report geometry cannot test the continuously-observed bow-echo structure the published
definitions require, so a report-only screen can be a high-recall **candidate generator**
and nothing more. Use it that way - to build an IOP case pool or to extend the record back
before 1996, where SPC's archive only offers the weaker pre-NEXRAD classes - and use
`spc_derecho_archive()` when you need the vetted label.

## 6. IEM Local Storm Report archive

`derechos-data-sources` §2 covers ASOS/ISUSM/RAOB on this host; this is the LSR layer. Free
CGI on university hardware: **request whole date ranges in one call**, keep concurrency to
1-2, use generous timeouts. A 20-year, 5-WFO pull took ~55 s per year.

```python
L = iem_lsr("2020-08-10T00:00Z", "2020-08-11T00:00Z", wfos=["DVN", "LOT"])
# (318, 18); QUALIFIER: '' 207, 'M' 78, 'E' 33
```

Columns `VALID VALID2 LAT LON MAG WFO TYPECODE TYPETEXT CITY COUNTY STATE SOURCE REMARK UGC
UGCNAME QUALIFIER`. This is the **only** report archive that ships a per-report
measured/estimated flag *and* a source, which is why it is worth the bytes.

Verified domain climatology, 2006-2025, WFOs DVN/LOT/DMX/ILX/ARX: 242,344 rows, 118,127
inside the box, of which **28,694 are severe** (`TYPECODE` in `G` gust 5,800, `D` wind
damage 9,414, `H` hail 11,958, `T` tornado 1,522). `QUALIFIER`: `M` measured 7,553,
`E` estimated 9,957, blank 10,941, `U` 243. **53.7 % of wind-gust reports are flagged
measured** - far better provenance than WCM's pre-2006 blank. Sources, after
case-normalising: TRAINED SPOTTER 11,120, PUBLIC 5,569, EMERGENCY MNGR 3,236, LAW
ENFORCEMENT 2,145, BROADCAST MEDIA 947, ASOS 721, AMATEUR RADIO 716, NWS EMPLOYEE 640,
NWS STORM SURVEY 635, MESONET 612.

### Gotchas

- **The `type` filter silently returns nothing.** `type[]=G&type[]=D` *and* `type=G&type=D`
  both return **HTTP 200 with a header row and zero data rows**; `typetext=TSTM+WND+GST` is
  ignored and returns the full unfiltered set. There is no working server-side type filter
  on this endpoint. Request everything and filter `TYPECODE` client-side - `iem_lsr` takes
  no type argument for exactly this reason.
- **3 of 242,344 rows break pandas' C parser** (`Expected 16 fields ... saw 17`) - an
  unescaped delimiter inside `REMARK`. `iem_lsr` reads with the `csv` module and truncates
  to the header width.
- **`MAG` is MPH** for gusts (inches for hail), unlike WCM's knots.
- **`SOURCE` case is inconsistent across the archive** ("PUBLIC" 3,970 and "Public" 1,599 are
  the same source). `iem_lsr` adds a normalised `SRC` column.
- **Magnitudes are not sanity-checked upstream.** 2011-06-04 21:40 at Manteno IL carries
  `MAG = 620` with `QUALIFIER = 'M'` and a `REMARK` that reads *"62 MPH MEASURED GUSTS"* - an
  uncaught factor-of-ten typo, still in the archive. Assert plausibility before you take a
  domain maximum.

## 7. IEM NWS warning and storm-based-warning archive

```python
ww = iem_warnings("2020-08-10T00:00Z", "2020-08-11T00:00Z", wfos=["DVN", "LOT"])
# (34, 27): SV 25, TO 6, MA 2, FA 1; every row gtype 'P' (polygon)
# windtag 49-90 kt, median polygon area2d 3285 km^2
gj = iem_sbw_geojson("2020-08-10T12:00Z", "2020-08-11T00:00Z", wfos=["DVN", "LOT"])
len(gj["features"])   # 34 MultiPolygon features - agrees with the CSV exactly
```

The CSV route (`/cgi-bin/request/gis/watchwarn.py`, `accept=csv|shapefile|geojson`) carries
`windtag`, `hailtag`, `tornadotag`, `damagetag`, `is_emergency`, `area2d` (km2), `gtype`
(`P` polygon / `C` county-zone segment), `utc_polygon_begin/end` and the AFOS `product_id`.
`limit1=yes` keeps only the initial NEW statement of each VTEC event; drop it to get every
SVS follow-up. The polygon tags are the forecaster's real-time expectation and make a clean
independent axis against which to score a nowcast or an IOP trigger.

**Gotcha, and a bad one:** `/api/1/vtec/sbw_interval.geojson` takes **`begints`/`endts`**.
Pass `sts`/`ets` (the spelling every other IEM endpoint uses) and it returns **HTTP 200 with
the current day's warnings** - on 2026-09-05 a query for 2020-08-10 came back with one
2026-09-05 Delaware County SV.W. No error, no warning, plausible-looking output. Always
assert on `utc_issue`.

## 8. Damage surveys - the DAT has a fully public FeatureServer

`apps.dat.noaa.gov` is a static CloudFront/S3 host serving an ArcGIS Experience Builder
app; every path that is not a shipped asset returns S3 `AccessDenied`, and there is no
ArcGIS server there. The app config at
`/StormDamage/DamageViewer/cdn/28/config.json` (readable; `config.json` at the app root is
403) names the real service host:

```
https://services.dat.noaa.gov/arcgis/rest/services/nws_damageassessmenttoolkit/DamageViewer/FeatureServer
  /0  Damage Points SDE     (point)    stormdate surveydate event_id damage damage_txt
                                       dod_txt efscale windspeed injuries deaths comments
                                       lat lon office image qc surveytype path_guid
  /1  Damage Lines SDE      (polyline) wfo stormdate starttime endtime start/end lat/lon
                                       length width injuries fatalities efscale efnum
                                       maxwind cropdamage propdamage comments
  /2  Damage Polygons SDE   (polygon)  efscale event_id stormdate length width ...
```

Anonymous, `Query,ChangeTracking`, `maxRecordCount` 2000, ArcGIS 11.5.

```python
dat_count(0), dat_count(1), dat_count(2)     # 13001, 1000, 761  in the DERECHOS box
p = dat_query(0, where="stormdate >= DATE '2020-08-10' AND stormdate < DATE '2020-08-11'",
              out_fields="objectid,stormdate,efscale,windspeed,office")
len(p)                                       # 297 surveyed damage points
dat_query(1, where="stormdate >= DATE '2020-08-10' AND stormdate < DATE '2020-08-11'")
# 18 damage paths: 16 from LOT (EF0-EF1, maxwind 70-110 mph, up to 14.5 km long)
# and 2 from DVN with efscale 'UNKNOWN' and maxwind -99
```

### Gotchas

- **`resultRecordCount` is mandatory.** A query with `where` + envelope + `outFields` and no
  `resultRecordCount` returns HTTP 200 carrying only
  `{"error": {"code": 400, "message": "Unable to complete operation.", "details": []}}`.
  `dat_query` always sends it and paginates.
- **`returnCountOnly=true` lies.** It returned 2000 for layer 0 and 761 for layer 2; the true
  counts from a server-side statistic are **13001** and 761. The count is clipped at
  `maxRecordCount`. Use `dat_count()`, which issues an `outStatistics` count. Paginating
  layer 0 to exhaustion returned 13,002 attribute rows against the statistic's 13,001 - a
  one-row disagreement, presumably a live edit between the two calls; treat either as
  "about 13,000" and re-count rather than assuming a fixed total.
- **`maxwind` uses `-99` as its missing sentinel**, and `surveytype` is **NULL on all 13,002
  points** - it looks like a usable field and is not.
- **This is not a continuous archive.** Points per year in the box: 2 (2004), 38 (2008),
  126 (2013), 863 (2014), 956 (2015), 388 (2020), 1744 (2023), 2337 (2024), 561 (2025),
  3104 (2026 to 21 Aug) - plus retrospective historical entries dated 1855, 1928, 1965,
  1967 and 1976. Operational coverage effectively starts 2013-2014. Never read a DAT trend
  as a hazard trend.
- **Survey effort is office-dependent**, which is a bias on top of the population bias:
  LOT 8,474 points, DVN 2,242, DMX 1,066, ILX 671, MKX 510. Chicago surveys far more
  densely than Quad Cities. Damage-path counts are closer (LOT 333, DVN 321, DMX 261).
- `noaa.maps.arcgis.com` (the webmap item the app also references) is **not reachable** from
  this sandbox and was not granted; the FeatureServer makes it unnecessary.

### What DVN and LOT publish as text

The survey *narratives* are AFOS Public Information Statements, and IEM archives them:

```python
al  = iem_afos_list("PNSLOT", "2020-08-11")        # 1 product
txt = iem_afos_text("202008120018-KLOT-NOUS43-PNSLOT")
# "...NWS DAMAGE SURVEY FOR 08/10/2020 DERECHO AND TORNADO EVENT..."
# "...consistent with 60 to 80 mph wind gusts, with pockets of enhanced winds
#     likely in excess of 90 mph."
```

`PNSDVN` and `PNSLOT` also carry ordinary pre-event public statements, so filter on the
text, not the PIL. Nine PNS products existed across DVN+LOT for 11-14 Aug 2020. There is
**no structured DVN/LOT survey product** beyond the DAT geometry - the narrative is prose.

## 9. NCEI SWDI - radar-derived detections, population-bias-free

`https://www.ncei.noaa.gov/swdiws/csv/<product>/<YYYYMMDD>:<YYYYMMDD>?bbox=...`

```python
swdi_query("nx3mda", "20200810", "20200811").shape   # (2409, 20) mesocyclone detections
swdi_query("nx3hail", "20200810", "20200811")        # hail-signature cells
swdi_query("nx3tvs",  "20200810", "20200811")        # tornado vortex signatures
```

`nx3mda` gives `LL_ROT_VEL`, `LL_DV`, `DEPTH_KFT`, `MAX_RV_KTS`, `MSI` and a `TVS` flag per
detection - a genuinely independent, algorithmic view of the mesovortices in a QLCS, with no
dependence on who was watching. Appending `&stat=count` returns a bare count.

Gotchas: the accepted product list is `nx3structure`, `nx3hail`, `nx3meso`, `nx3mda`,
`nx3tvs`, `nldn` (each also `:inv` and some `_all`) - **`plsr` (storm reports) is no longer
a SWDI product**, so this is not a route to reports. **`nx3meso` returns zero rows** for
modern dates; `nx3mda` is its live replacement. **`nldn` (lightning) returns HTTP 400 with
an empty body** - it is licence-restricted (Vaisala), not broken. Bare `/swdiws/` returns
400. Detections carry `-999` sentinels (`MOTION_DEG`, `MOTION_KTS`).

## 10. The unit traps, and one outright error in the record

Four archives carry the *same* reports in *different* units:

| Archive | Wind field | Unit | Missing/unknown |
|---|---|---|---|
| SPC WCM | `mag` | **knots** | `0` |
| NCEI Storm Events | `MAGNITUDE` | **knots** | NaN |
| SPC daily reports | `Speed` | **mph** | string `UNK` |
| IEM LSR | `MAG` | **mph** | `0` |
| DAT | `windspeed`, `maxwind` | **mph** | `-99` |

Verified by matching distributions on 2020-08-10 in the box: WCM median 61, LSR median 70,
ratio **0.871** against the exact conversion 0.869.

### The 126 kt that is really 126 mph

The largest measured gust in the SPC WCM database over the DERECHOS domain across the whole
1955-2025 record is **126 kt (145 mph), 2020-08-10 11:00 CST at 41.899 N, 92.320 W**,
flagged `MG`. The SPC derecho archive's re-vetted entry for the **same report** - same
17:00 UTC time, same 41.90/-92.32 location, Benton County Iowa - reads **109 kt, Measured** -
**125.4 mph**, i.e. the underlying 126 mph measurement rounded to whole knots
(126 mph = 109.5 kt). The IEM LSR for that event is exactly that: a 126 **mph**
home-weather-station measurement near Atkins. The WCM row stores the mph figure in a knots column, inflating it
by 15.6 %. The second-largest measured gust in WCM over this box is 93 kt (2006-03-12, IL),
so the artefact is a clear outlier - see `derechos_domain_largest_measured_gusts.csv`.

**Cross-checks against the ASOS gusts in `derechos-data-sources` §2 both hold.** At ORD the
WCM database has a **measured 54 kt at 41.98/-87.90, 3.3 km from the airport, 14:49 CST** -
identical to the 54 kt ASOS peak that skill records. At **MUT there is no measured report at
all**: the nearest WCM entries are 70 kt *estimated* 10 km away, against the 50 kt the
Muscatine ASOS actually measured. The report database is 40 % high there. Take domain maxima
from the `MG`/`MS` subset, and expect estimates to run hot.

## 11. Population bias, quantified

Report databases record who was watching. Over the 80 counties whose centroid falls inside
the DERECHOS box (45 Iowa, 33 Illinois, 1 Indiana, 1 Wisconsin), with severe-wind reports
from SPC WCM 1996-2025 and 2024 Census county population:

- **Spearman rho = 0.865 (p = 4.5e-25, n = 80)** between county population density and wind
  reports per 1000 km2 per decade.
- Log-log slope **0.383**: report density scales as (population density)^0.38, so a decade
  of population density buys 2.4x the reports.
- By population-density quartile, median wind reports per 1000 km2 per decade:
  **21.4 (Q1 rural, 8.8 people/km2) -> 29.3 -> 38.9 -> 72.2 (Q4 urban, 160 people/km2)**.
  An **18.3x** population contrast produces a **3.4x** report-density contrast.

Sub-linear, but real and large. Two consequences for DERECHOS: an apparent east-west gradient
in wind-report density across the domain is partly the Chicago metro, not the land-use
gradient H1 is about; and the DAT's office-dependent survey effort (§8) compounds it. The
population-independent alternatives are SWDI radar detections (§9), the `MG`/`MS` measured
subset, and the ASOS/mesonet networks in `derechos-data-sources`.

Temporal bias is larger still. Mean severe-wind reports per year inside the box:
**62.6 (1955-1975) -> 129.1 (1976-1995) -> 489.5 (1996-2010) -> 591.3 (2011-2025)**.
Comparing the record's first and last decades rather than these unequal eras, the rise is
larger still: wind **29.1 (1955-1964) -> 620.9 (2016-2025) = 21.3x**, hail
**14.5 -> 308.4 = 21.3x**, tornado **15.7 -> 71.2 = 4.5x**. Quote the decade figures - the
era means understate it because the 1955-1975 window already contains part of the growth.
None of it is meteorological: it is NWS reporting practice, spotter networks, mobile phones
and social media. **Never fit a trend to raw report counts.** Screened swath-days show the same
artefact (0.10 -> 0.60 -> 5.13 -> 4.40 per year), so the §5 screen is a case-selection tool,
not a climate-change diagnostic.

## Worked result: the domain catalogue

Three artifacts in this project, built entirely from the recipes above:

- `derechos_domain_derecho_catalogue.csv` - **173 rows**: 157 screened wind-swath days
  (1955-2025) plus 16 SPC-archive events the screen missed, with swath geometry
  (`major_km`, `minor_km`, `aspect`, `axis_deg`), report counts, in-box counts, gust maxima,
  the SPC archive class where one matched (50 rows), and a `qc_note` on the 126 kt artefact.
- `derechos_domain_report_climatology.csv` - per-year 1955-2025 wind/hail/tornado counts in
  box, largest measured and largest reported gust, screened swath-days, SPC archive counts.
- `derechos_domain_largest_measured_gusts.csv` - the 25 largest `MG`/`MS` gusts in box, in
  both knots and mph.
- `derechos_domain_storm_climatology.png` - the four-panel climatology figure.

## What is verified

Exercised against the live service on **2026-09-05** from this sandbox:

- **NCEI Storm Events** - directory index (77 years x 3 families, with the differing `_c`
  stamps); `details` downloaded and parsed for 1955, 1995, 1996, 2020, 2024, 2025;
  `locations` (62,421 rows) and `fatalities` (905 rows) for 2020; the pre/post-1996 event-type
  count and the zone-vs-county coordinate split measured; damage parsing;
  `search-events` POST for one state, two states and a full year (the 1000-row cap
  reproduced); `state-list` GET.
- **SPC WCM** - all three zipped aggregates downloaded and parsed; magnitude-type coverage by
  decade; `tz == 3` on all 562,088 wind rows; box clip.
- **SPC daily reports** - `200810_rpts_{wind,hail,torn,filtered}.csv` and the
  `today_`/`yesterday_` aliases.
- **SPC derecho archive** - all eight CSVs plus `WindReportMethodology.pdf` downloaded and
  parsed; box intersection for all four classes; the screen calibrated against it.
- **IEM** - LSR for 2006-2025 over DVN/LOT/DMX/ILX/ARX (242,344 rows) and a single day;
  the broken `type` filter reproduced three ways; `watchwarn.py` CSV and shapefile;
  `sbw_interval.geojson` with both correct and incorrect parameter spellings;
  `afos/list.json` and `nwstext/<id>` retrieving the KLOT derecho damage survey.
- **NWS DAT** - FeatureServer root, folder, all three layer metadata documents, paginated
  full pulls (13,002 points / 1,000 lines / 761 polygons), `outStatistics` counts, the
  mandatory-`resultRecordCount` failure, the clipped `returnCountOnly`.
- **NCEI SWDI** - `nx3mda`, `nx3hail`, `nx3tvs`, `nx3structure` (0 rows), `nx3meso` (0 rows),
  `nldn` (HTTP 400), `&stat=count`.
- **NCEI Billion-Dollar Disasters** - `events-US-1980-2026.csv` (403 events, frozen 2024).
- **Census** - 2024 county population estimates and the 2024 county gazetteer, from
  `www2.census.gov`.

All **27** helpers in `kernel.py` were enumerated with `ast` and called in a single pass with
coverage tracked programmatically: **27 defined, 27 called, 0 missed**.

### Not verified

- **`api.census.gov`** - granted and reachable, but every query now returns a
  *"Missing Key"* page. No API key is configured. The keyless bulk files on
  `www2.census.gov` were used instead and are what `§11` rests on.
- **`noaa.maps.arcgis.com`** - blocked by the allowlist, not granted, not needed once the DAT
  FeatureServer was found. The ArcGIS Online item id in the DAT app config is
  `36d695d869a94664a74d919cfbe8813f`, untested.
- **`storage.googleapis.com`** - the Storm Events app fetches a `graphql.json` from there for
  its CMS content. Denylisted and not grantable. Irrelevant to the data path.
- **NCEI SWDI `nldn`** lightning - HTTP 400; licence-restricted. Not a sandbox artefact.
- **`csv-results`** on the Storm Events API - returns `{"data": []}`; its payload shape was
  not reverse-engineered.
- **`pdf-latex`, `certify`, `polygon-counties`** on the same API - seen in the bundle, not
  called.
- **SPC derecho archive completeness beyond 2025-07-29** - SPC's own page says the archive
  was recently "initiated" and that further definition work is under way. Re-download before
  quoting counts.
- **DAT damage-path counts of exactly 1000** for layer 1 - confirmed by an `outStatistics`
  count and by exhausting pagination at three page sizes, so it is a real 1000, but the round
  number is worth re-checking on a future pull.

### Network grants this skill depends on

Granted while building it: **`api.census.gov`** (subsequently found to require a key) and
**`www2.census.gov`**. Already default-reachable: `www.ncei.noaa.gov`, `www.spc.noaa.gov`,
`mesonet.agron.iastate.edu`, `apps.dat.noaa.gov`, `services.dat.noaa.gov`. Blocked and *not*
granted: `noaa.maps.arcgis.com`, `storage.googleapis.com`.

## Related skills

`derechos-campaign` (science case, SQ1-SQ7 - load first),
`derechos-data-sources` (ARM Live, IEM ASOS/ISUSM/RAOB, NEXRAD listing, CDL, Sentinel-2,
mPING, HRRR - the in-situ and gridded layer this skill complements),
`nexrad-cloud-router` and `nexrad-aws-2025` (turning a screened case day into radar volumes).

## Key references

- **Squitieri et al. 2025a,b** - the modified derecho definition and its updated CONUS
  climatology; the basis of the SPC archive in §1. A companion BAMS paper documents the
  archive itself. `WindReportMethodology.pdf` ships with the archive.
- **Johns & Hirt 1987** - the original derecho criteria (report swath, continuity).
- **Coniglio & Stensrud 2004** - derecho climatology and environments.
- **Li et al. 2025** - ML bow-echo climatology 2004-2021, doi:10.5194/essd-17-3721-2025;
  the source of the white paper's ~4/year. Bow echoes, not derechos - see §1.
- **Wagner et al. 2025** - wind damage in the 10 Aug 2020 derecho from UAS, satellite and
  radar, doi:10.1175/WAF-D-24-0198.1.
