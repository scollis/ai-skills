---
name: derechos-soil-properties
description: Soil moisture, soil temperature and static soil properties for the DERECHOS Iowa-Illinois domain. Live-tested recipes for the Iowa Environmental Mesonet ISU Soil Moisture Network (ISUSM) in full - all temporal endpoints, the complete variable set including SoilVue multi-depth profiles and QC flags - plus a re-runnable network-wide sensor health audit, USDA AWDB/SCAN as an independent network, and NRCS SSURGO properties via Soil Data Access. Use when fetching or QCing Iowa mesonet soil data, interpreting a soil moisture or temperature series, or needing texture, bulk density, available water capacity, Ksat, drainage class or hydrologic soil group at a site. Triggers - Iowa mesonet, ISUSM, soil moisture, soil temperature, VWC, SoilVue, SCAN, AWDB, SSURGO, Soil Data Access, mukey, map unit, horizon, texture, bulk density, available water capacity, ksat, drainage class, hydrologic soil group, H2, SQ1, FRUI4, CRFI4, Muscatine Island, SERF, Illinois Climate Network, WARM.
---

# DERECHOS soil properties

Everything below was exercised against the live service on **2026-09-05** from this
sandbox. `kernel.py` auto-loads the helpers.

Load `derechos-campaign` for the science case (H2, SQ1) and `derechos-data-sources`
for the rest of the regional access layer - ASOS/RAOB, NEXRAD, CropScape CDL,
Sentinel-2, mPING, HRRR, ARM Live. **That skill already covers the ISUSM basics**
(the `iem_isusm` daily/hourly wrapper, the timezone-aware-timestamp HTTP 422 gotcha,
the seven legacy soil columns). This skill is the deep version: the endpoints and
variables that wrapper does not reach, a network-wide health audit, and the static
soil properties without which a moisture series is uninterpretable. Do not
re-document CDL, Sentinel-2, NEXRAD, mPING or HRRR here.

## Source to science question

| Source | What it provides | Serves | Status |
|---|---|---|---|
| **IEM ISUSM** (`mesonet.agron.iastate.edu`) | Soil moisture + soil temperature at 4-52 in, daily / hourly / **1-minute**, 29 stations, 2013- | SQ1, SQ2, SQ7 | verified |
| **IEM ISUSM SoilVue** (same CGI, `vars=sv`) | 15-depth VWC + temperature profile, 8 stations incl. **M1 since 2025-08-15** | SQ1, SQ2 | verified |
| **IEM AgClimate live CSV** | Today's per-station sensor depth inventory, SI units | operations | verified |
| **IEM `/api/1/isusm/daily`** | Network-wide daily ET / GDD / solar / precip - **no soil columns** | SQ1 | verified (no soil) |
| **USDA AWDB / SCAN** (`wcc.sc.egov.usda.gov`) | Independent soil moisture + temperature at 2-40 in from **2001**; 1 station in domain | SQ1 | verified |
| **NRCS SSURGO via Soil Data Access** (`sdmdataaccess.nrcs.usda.gov`) | Texture, bulk density, AWC, Ksat, drainage class, hydrologic soil group, taxonomy per horizon | SQ1, SQ2 | verified |
| **Illinois WARM / ICN** (`warm.isws.illinois.edu`) | East-domain soil moisture + temperature | SQ1, SQ2, SQ3 | **login required** |

The single most consequential geographic fact: **ISUSM stops at the Mississippi.**
The easternmost of the 29 stations is BNKI4 at **-90.914**, so the entire Illinois
half of the DERECHOS domain - NIU/DeKalb, Nachusa Grasslands, Chicago - has **no
ISUSM soil coverage at all**. East-domain soil moisture depends on WARM/ICN, which
is behind a login (S6), or on new instrumentation.

## 1. ISUSM in full - the complete endpoint and variable map

One CGI, `/cgi-bin/request/isusm.py`, carries everything. Three parameters the
existing wrapper does not pass are where the extra data lives: **`vars`**,
**`timeres`** and **`qcflags`**.

### 1.1 The three modes, and how to discover them

`mode` is validated with a regex, and the HTTP 422 body prints it - which is how the
mode list was established rather than guessed:

```
mode=inst -> 422  "String should match pattern 'hourly|daily|inversion'"
```

| `mode` | `timeres` | cadence | soil content |
|---|---|---|---|
| `daily` | - | 1/day | legacy depths + min/max temps + all SoilVue depths |
| `hourly` | - | 1/hour | legacy depths + all SoilVue depths |
| `hourly` | `minute` | **1/minute** | same variables at 1-minute resolution |
| `inversion` | - | 1/minute | **air** temperature at 1.5 / 5 / 10 ft + wind. **No soil.** |

`mode=inversion` is the network's inversion-tower product (`tair_15 tair_5 tair_10
speed gust`); useful for nocturnal stability and the SQ7 low-level-jet work, not for
soil. Verified at CRFI4 and BOOI4, 1440 rows/day each.

```python
d = isusm_soil("CRFI4", "2024-07-01", "2024-07-02", mode="daily")
h = isusm_soil("CRFI4", "2024-07-01", "2024-07-02", mode="hourly")
m = isusm_soil("CRFI4", "2024-07-01", "2024-07-01T02:00:00Z",
               mode="hourly", timeres="minute")   # 120 rows, soil04t + soil12vwc
```

### 1.2 The complete soil variable set

**Without `vars=`, the CGI returns a fixed legacy subset** - `soil04t soil12t
soil24t soil50t soil12vwc soil24vwc soil50vwc` - *even at a station with a
15-depth SoilVue installed*. Verified at BOOI4: the default header is identical to
CRFI4's. This is the most expensive gotcha in the service, because nothing tells you
the extra depths exist.

`isusm_soil_varlist(mode)` returns the codes. Soil-bearing members:

- **daily**: `soil{04,12,24,50}{tn,t,tx}` (min/mean/max temperature), `soil{12,24,50}vwc`, `sv`
- **hourly / minute**: `soil{04,12,24,50}t`, `soil{12,24,50}vwc`, `sv`
- **non-soil but co-located and useful**: `et`, `precip`, `solar`/`solar_mj`, `gdd50`,
  `chillhours`, `speed`, `gust`, `rh*`, `bpres_avg`/`bp_mb`, `cci`/`cci_shade`
  (crop canopy index), and two leaf-wetness sensors `lwmv_1 lwmv_2` with
  dry/condensation/wet minute totals `lwm{dry,con,wet}_{1,2}_tot`.

**`vars=sv` expands to the SoilVue family** - 15 depths in inches, each with a
temperature and a VWC column: `sv_t{D}` / `sv_vwc{D}` for
D in 2, 4, 8, 12, 14, 16, 20, 24, 28, 30, 32, 36, 40, 42, 52
(5, 10, 20, 30, 36, 41, 51, 61, 71, 76, 81, 91, 102, 107, 132 cm).

### 1.3 Units - and a factor-of-100 trap inside a single row

Soil temperature is **degrees F** and legacy VWC is **percent** at *all three*
cadences; the endpoints agree, which was the specific thing to check.

But `sv_vwc*` is a **fraction**, not a percent. Verified at BOOI4, 2024-07-01,
in the same CSV row at all three cadences:

| | `soil12vwc` (12 in) | `sv_vwc14` (14 in) |
|---|---|---|
| daily | 37.07 | 0.2832 |
| hourly | 37.20 | 0.2870 |
| minute | 37.20 | 0.2870 |

Two soil-moisture columns two inches apart in the same row, differing by 100x in
unit. `isusm_soil(..., sv_to_percent=True)` normalises. AgClimate's live CSV uses
a third convention again (K and percent).

### 1.4 `-99` is the missing sentinel and `na=blank` does not touch it

`na=blank` blanks *some* missing values but `-99` comes through as a number, so
`notna()` and `df.mean()` both silently accept it. This is not confined to SoilVue
columns. `isusm_soil(sentinel_to_nan=True)` (the default) masks `< -90`.

### 1.5 QC flags exist, are off by default, and reveal estimated data

`qcflags=1` adds a `<var>_f` column per requested variable: `-99` when unflagged, a
letter otherwise. Verified at CRFI4 for 2024-07-01, daily:

```
soil04tn 62.3  soil04tn_f E
soil04t  67.25 soil04t_f  E
soil04tx 72.2  soil04tx_f E
```

`E` = **estimated**. The default download hands you infilled soil temperature with
no indication. Note the flag columns are not universal - in the hourly response
`soil12vwc_f` and `soil04t_f` appeared but `soil24vwc` and `soil50vwc` had none.
Always request `qcflags=1` for any analysis that will be published.

### 1.6 Station and depth inventory

29 stations, **16 inside the DERECHOS box**, elevations 168-481 m, records from
2012-09-18 (CAMI4) onward. Two are retired: MCSI4 (ends 2024-04-24) and REFI4
(ends 2018-11-15); both return an empty soil frame.

```python
isusm_live_depths()      # today's reporting depths per station, from /agclimate/isusm.csv
```

That CSV embeds the depth list in its header (`depth [m]#SOILT [K]#SOILMP [%]`,
`;`-separated within each `#` block) and gives a *live* snapshot in SI units (K, m).

**But it is an incomplete inventory - do not use it to decide what a station
measures.** Measured 2026-09-05: it reported 27 of the 29 stations, and per station
only the legacy shallow depths. `FRUI4` and `CRFI4` both showed
`[0.102, 0.305, 0.61]` m (4/12/24 in) - it never lists the 1.27 m (50 in) sensor
that both stations do report through the CGI, and at `CRFI4` it omits the entire
9-depth SoilVue. `BOOI4` showed 6 depths (adding 0.406 and 0.508 m) and `AKCI4`,
which is SoilVue-only, showed **none at all**. Use it for "is this station alive
this minute"; use a `vars=sv` CGI pull plus the audit for what actually exists.
`isusm_station_soil_inventory.csv` (this session) is the record-wide version.

Depth availability is **not uniform**, and the 50 in (127 cm) sensor - the one H2
cares about - is the scarce one: a usable 50 in VWC record exists at **15 of 29**
stations network-wide and **7 of 16** in the DERECHOS box.

### 1.7 `/api/1/isusm/daily` has no soil columns

The modern JSON API endpoint is real, needs no station parameter (it returns the
whole network for a date range), and its columns are
`station et sgdd gdd srad precip lon lat name city climo_gdd climo_precip`. Despite
the name it carries **no soil moisture or soil temperature**. Use the CGI.

## 2. Network-wide sensor health audit

The earlier two-station, one-year finding generalises badly: the network's soil
sensors fail in at least four distinct ways and **every one of them passes a
completeness check**.

The whole archive fits in **one request**. Measured: 29 stations x
2013-12-01..2026-09-03, `mode=daily` with all soil vars = **109,322 station-days,
26.1 MB, 864 s**. Keep concurrency at 1 - this is a single free CGI on university
hardware, and 864 s is the price of being polite once rather than 29 times.

```python
raw = isusm_soil(all_stations, "2013-12-01", "2026-09-04", mode="daily", timeout=1800)
aud = isusm_soil_audit(raw)          # 1073 rows, one per (station, variable)
aud[aud.verdict != "ok"]
```

Verdict distribution over the **203 legacy** station-variable records:
145 `ok`, 43 `sentinel_only` (no such sensor at that station), 8 `intermittent`,
4 `pinned_flatlined`, 2 `impossible_values`, 1 `some_impossible`. Of the 870
SoilVue records, 718 are `sentinel_only` - i.e. the station has no SoilVue.

### The four failure modes, with the stations that show them

1. **Pinned at a constant.** `FRUI4` (= S1) `soil24vwc` and `soil50vwc` sit at
   exactly **1.00 %** on 70.9 % and 79.6 % of days respectively, with
   `n_sentinel = 0` - so `notna()` counts 4533/4533 for both. Re-measured
   2026-09-05: still pinned through 2026-09-03; `soil50vwc` has min = max = 1.00
   for all of 2025 and 2026. **Not repaired.**
2. **Physically impossible values.** The same two columns report **negative**
   volumetric water content on 2419 and 2569 days. Combined with (1), S1 has no
   usable deep soil moisture anywhere in its 12.4-year record.
3. **Flatlined at a station-wide freeze.** `OSTI4` (Oskaloosa) is a failure mode
   not previously documented: `soil24t`/`soil24vwc` returned a constant
   71.672 F / 39.6 % from **2020-07-31**, and `soil12t`/`soil12vwc` a constant
   73.202 F / 39.3 % from **2020-08-10** - the day the 2020 Midwest derecho crossed
   the domain. 2216 pinned days and counting. The 12-inch freeze is coincident with
   the reference event; that is an association, not a demonstrated cause.
4. **Intermittent / retired mid-record.** `CNAI4` soil50 ends 2018-11-27 while
   soil04/12/24 continue to 2026; `DOCI4` legacy soil ends 2021-06-02; `MCSI4`
   ends 2022-2023 by depth. A whole-archive fetch plus `first_valid`/`last_valid`
   is the only way to see this - `archive_end` in the station metadata is null for
   all of them.

The audit also emits `n_steps` (day-over-day jumps beyond 15 pp VWC / 10 F soil
temperature), which flags sensor swaps. FRUI4 and CRFI4 show 48 and 39 steps in
`soil04t`, all at the surface where large diurnal-scale jumps are real - treat
`n_steps` at 4 in as expected and at 24-50 in as suspicious.

**Operational headline:** of the 16 ISUSM stations in the DERECHOS box, only **10**
had at least one physically plausible, non-pinned VWC depth reporting in the 30 days
to 2026-09-03 (20 of 29 network-wide). Budget for that.

### SoilVue deployment - and M1 already has one

Eight stations have a real SoilVue record. Five arrived in a 2025 expansion:

| station | depths (in) | first valid |
|---|---|---|
| `BOOI4` Ames AEA | 2,4,8,12,14,16,20,24,28,30,32,36,40,42,52 | 2016-08-09 |
| `DOCI4` Jefferson | 2,4,8,12,16,20 | 2019-06-05 |
| `AKCI4` Ames Kitchen Farm | 2,4,8,12,16,20,24,30,40 | 2021-12-17 |
| `AHDI4` Ames Hinds Farm | 14,16,20,24,28,32 | 2023-06-21 |
| `CNAI4` Castana | 14,16,20,24,28,32,36,42,52 | 2025-06-02 |
| `CAMI4` Sutherland | " | 2025-06-19 |
| `KNAI4` Kanawha | " | 2025-06-19 |
| **`CRFI4` = M1 SERF** | **14,16,20,24,28,32,36,42,52** | **2025-08-15** |

So **M1 has carried a 9-depth soil profile to 132 cm since 2025-08-15**, ~2 years
before the requested deployment start - a pre-campaign deep-soil baseline the white
paper did not know about. `FRUI4` = S1 has **no** SoilVue, which is the sharpest
possible statement of the §3.1 SoilVue10 request: at S1 it is not an upgrade, it is
the only route to deep soil moisture.

**Gotcha on the new installs.** At CRFI4 the three shallowest SoilVue VWC channels
disagree with everything around them. Medians over the 385-day overlap
2025-08-15..2026-09-03:

| depth | 36 cm | 41 cm | 51 cm | 61 cm | 71 cm | 81 cm | 91 cm | 107 cm | 132 cm |
|---|---|---|---|---|---|---|---|---|---|
| `sv_vwc` (%) | **7.1** | **8.4** | **8.0** | 44.5 | 45.9 | 46.9 | 44.5 | 44.0 | 43.4 |

The co-located legacy sensors read 41.4 / 42.1 / 40.2 % at 30 / 61 / 127 cm, and
`sv_vwc24` (61 cm) matches `soil24vwc` (61 cm) to 2.4 pp. So depths 4-9 are good and
**depths 14, 16 and 20 in are not usable** - consistent with poor probe-soil contact
in a smectitic clay, a known SoilVue installation failure. `isusm_soil_audit` does
not catch this (the values are in-range and varying); it took the co-located
comparison. **Always cross-check a new profile probe against the legacy point
sensors in the overlap window.**

## 3. USDA AWDB / SCAN - the independent comparison network

`wcc.sc.egov.usda.gov/awdbRestApi`, no credentials, OpenAPI at `/v3/api-docs`
(4 paths: `stations`, `data`, `reference-data`, `forecasts`).

### The trap: there is no state filter and a bad parameter is silently ignored

Adding `stateCds=IA` and `networkCds=SCAN` to the stations call returns **HTTP 200 and the full national SCAN list**
(1.6 MB, first record in Alabama). Neither parameter exists. Filtering is
`stationTriplets` with `*` wildcards:

```python
awdb_stations(["IA", "IL"], network="SCAN")     # -> 3 stations
awdb_soil_series("2031:IA:SCAN", "2020-06-01", "2020-09-01")
```

**Every SCAN station in Iowa and Illinois - all three of them:**

| triplet | name | lat, lon | elev (ft) | begins |
|---|---|---|---|---|
| `2031:IA:SCAN` | Ames | 42.0136, -93.72977 | 1060 | 2001-09-19 |
| `2068:IA:SCAN` | Shagbark Hills | 42.44481, -95.76793 | 1360 | 2002-06-19 |
| `2004:IL:SCAN` | Mason #1 | 40.31314, -89.90187 | 490 | 1993-10-01 |

Only **Ames is inside the DERECHOS box**; Shagbark Hills is 1.6 deg west of it and
Mason #1 0.4 deg south. Ames is also 22 km from ISUSM `BOOI4`/`AKCI4`, so it is a
usable independent check on the Ames ISUSM cluster - and its record starts **12
years before ISUSM**, which matters for any decadal soil-moisture trend argument.

Ames soil elements: `SMS` (soil moisture, **percent**) and `STO` (soil temperature,
**deg F**) at **2, 4, 8, 20, 40 inches**, at HOURLY, DAILY, SEMIMONTHLY and MONTHLY
durations. Also `SAL` (salinity), `RDC` (real dielectric constant), plus full met.
Verified retrieval: 93 daily values per depth for Jun-Aug 2020, every point
`qcFlag: 'V'`.

Gotchas: depths are **negative inches** in `heightDepth`; `endDate` is
**`2100-01-01`** for active elements, so do not read it as a real end date; the
response is `[{stationTriplet, data:[{stationElement, values:[...]}]}]` - one block
per element x depth x duration, so `elements=SMS:*` at `duration=DAILY` still
returns five blocks.

## 4. NRCS SSURGO via Soil Data Access - what makes a moisture series interpretable

`sdmdataaccess.nrcs.usda.gov/Tabular/post.rest`, no credentials. **SQL over HTTP**:
POST `{"query": "<T-SQL>", "format": "JSON+COLUMNNAME"}`, response
`{"Table": [[colnames], [row], ...]}`. `sdmdataaccess.sc.egov.usda.gov` also
responds; prefer the short host.

```python
sda_point_profile(41.356, -91.136)          # S1
sda_grid_components(points)                 # a whole domain grid in ONE request
sda_query("SELECT mukey, muname FROM mapunit WHERE mukey = '410028'")
```

### The join, and the aggregation trap

The hierarchy is `legend -> mapunit -> component -> chorizon`. A point resolves to a
`mukey` via the spatial helper function:

```sql
SELECT mu.mukey, mu.muname, c.compname, c.comppct_r, c.drainagecl, c.hydgrp,
       c.taxclname, ch.hzname, ch.hzdept_r, ch.hzdepb_r, ch.sandtotal_r,
       ch.silttotal_r, ch.claytotal_r, ch.dbthirdbar_r, ch.awc_r, ch.ksat_r, ch.om_r
FROM legend l
INNER JOIN mapunit  mu ON mu.lkey = l.lkey
INNER JOIN component c ON c.mukey = mu.mukey
LEFT OUTER JOIN chorizon ch ON ch.cokey = c.cokey
WHERE mu.mukey IN (SELECT * FROM
      SDA_Get_Mukey_from_intersection_with_WktWgs84('point(-91.136 41.356)'))
ORDER BY c.comppct_r DESC, ch.hzdept_r
```

**A map unit is not a soil.** It holds several components with `comppct_r`
percentages, and the query above returns all of them interleaved by horizon. The M1
map unit `408753` returns **22 rows spanning three components** - Taintor 90 %
(poorly drained, HSG D), Sperry 5 % (very poorly drained, D) and Mahaska 5 %
(somewhat poorly drained, **C/D**). Take the first row and you may get the 5 %
component and the wrong hydrologic group. Either filter `c.majcompflag='Yes'` and
keep `max(comppct_r)` (the *dominant condition*), or area-weight by `comppct_r` (the
*weighted average*) - and say which you did. `sda_point_profile(major_only=True)`
does the former.

Units: horizon depths **cm**; sand/silt/clay **%**; `dbthirdbar_r` **g/cm3**;
`awc_r` **cm/cm**; `ksat_r` **um/s**; `om_r` **%**. Every property has `_l`/`_r`/`_h`
(low / representative / high) variants - `_r` is the one to use.

### Domain-wide in one request

`SDA_Get_Mukey_from_intersection_with_WktWgs84` accepts a **multipoint** WKT, so a
whole-domain survey is a single query. Verified: a 108-point 0.4 deg x 0.38 deg grid
over `[-94.2, 40.7, -87.4, 42.6]` returned **103 distinct map units** in one call.
Dominant-component surface horizons (n = 120): sand median **9.5 %** (p10 4.0,
p90 41.0), clay median **24 %**, bulk density median **1.36 g/cm3**, AWC median
**0.21 cm/cm** (min 0.11), Ksat median **9 um/s** (max 92). Drainage class:
37 well, 27 poorly, 20 moderately well, 14 somewhat poorly, **3 excessively**.
Hydrologic group: 32 C, 23 C/D, 21 B, 14 B/D, 6 D, **4 A**.
Do **not** attempt a polygon covering the whole box - the grid is what makes this
one fast query instead of a timeout.

## 5. Worked result - the DERECHOS core sites are soil end-members

`derechos_soil_sites()` returns this as data. Both sites resolve to a single
dominant component covering >= 90 % of the map unit, so the aggregation trap does
not bite here.

| | **S1** Muscatine Island (`FRUI4`) | **M1** SERF Crawfordsville (`CRFI4`) |
|---|---|---|
| map unit | 410028 Fruitfield coarse sand, 0-2 % | 408753 Taintor silty clay loam, 0-2 % |
| dominant component | Fruitfield, **95 %** | Taintor, **90 %** |
| taxonomy | Entic Hapludolls, sandy, mixed, mesic | Fine, smectitic, mesic **Vertic Argiaquolls** |
| drainage class | **Excessively drained** | **Poorly drained** |
| hydrologic soil group | **A** | **D** |
| sand / clay, 0-20 cm | **90.6 / 3.0 %** | **2.0 / 30.0 %** |
| bulk density | 1.55 g/cm3 | 1.35 g/cm3 |
| AWC | **0.05 cm/cm** | **0.22 cm/cm** |
| Ksat | **200 um/s** | **3 um/s** |
| organic matter, surface | 2.0 % | 4.0 % |
| profile | uniform sand to 152 cm (Ap-A-AC-C) | Ap-A1-A2-Btg1..4-Cg, clay peaks 41 % at 51-61 cm |

**Yes, S1 and M1 differ in a way that matters for the paired-site design, and by
more than "different soils".** AWC differs **4.4x**, Ksat **67x**, and the two sites
sit at opposite ends of the hydrologic-group scale (A vs D) and the drainage-class
scale (excessively vs poorly). Against the 103-map-unit domain survey in S4, **M1 is
typical and S1 is an outlier**: S1's surface sand (90.6 %) exceeds the domain
maximum (87 %), its AWC (0.05) falls below the domain minimum (0.11), and its Ksat
(200) exceeds the domain maximum (92); only 4 of 103 domain map units are HSG A and
only 3 are excessively drained. M1's values (sand 2 %, clay 30 %, AWC 0.22,
Ksat 3) sit at or near the domain median throughout.

Read for the campaign: the pair spans the *physical* end-members of the Corn Belt
soil-moisture reservoir, which is exactly what H2 needs - but M1 is the site that
represents the domain, and S1 is a deliberate dry-limb extreme, not a second sample
of the same population. Any domain-scale inference (the §4.2.2 ET digital twin, the
SCREAM benchmark) should weight accordingly.

### What the 12.4-year ISUSM record adds

Monthly medians over the full record, dead sensors excluded per the S2 audit:

| | S1 30 cm VWC | M1 30 / 61 / 127 cm VWC |
|---|---|---|
| range across the year | **3.4 - 4.7 %** | 42.0-48.3 / 42.5-49.0 / 38.0-42.7 % |

S1's usable moisture sensor shows **no seasonal cycle at all** - a 1.3 pp annual
range - because a coarse sand with AWC 0.05 drains to residual water content and
stays there. M1 shows a clear spring-summer wetting to ~48 % and never dries below
~38 %. That last point is a real limitation on the pre-campaign baseline: **the dry
limb H2 cares about is unsampled at M1 and unmeasurable at S1.**

Soil temperature is measurable and clean at all four depths at **both** sites, and
it separates them:

| annual amplitude of monthly medians | 10 cm | 30 cm | 61 cm | 127 cm |
|---|---|---|---|---|
| S1 (sand) | 25.2 K | 27.8 K | 25.1 K | **21.8 K** |
| M1 (silty clay loam) | 25.2 K | 22.2 K | 19.5 K | **14.2 K** |

Identical at the surface, and by 127 cm the annual wave is damped to 0.87 of the
surface amplitude at S1 versus 0.56 at M1. A 21.8 K amplitude at 1.27 m is large
enough to be worth checking against an independent probe before it is published -
either the sand's thermal regime genuinely propagates that deep, or S1's 50 in
temperature sensor is shallower than labelled. Treat it as provisional.

Artifacts from this session: `derechos_core_site_soil_profile.csv` (18 rows, SSURGO
horizon properties joined to the observed climatology per sensor depth),
`derechos_core_site_soil_climatology.png`, `isusm_soil_sensor_audit.csv` (1073
rows), `isusm_station_soil_inventory.csv` (29 stations),
`ssurgo_derechos_domain_context.csv` (103 map units).

## 6. Illinois WARM / ICN - re-checked, still shut

Re-verified **2026-09-05**, unchanged from the 2026-09-01 finding in
`derechos-data-sources`:

```python
warm_icn_soil_status()
# station_metadata: 200, title "Illinois Climate Network: Station Metadata..."
# bulk_data_list:   200, title "Access WARM Data - Login"
```

`warm.isws.illinois.edu/warm/climnet/stnmetadata.asp` serves the 21 station codes
publicly; `/warm/cdflist.asp` is a login page; `/warm/datadownload.asp` is an IIS
404. Station lat/lon remains non-machine-readable. **This is the binding constraint
on east-domain soil science**, because ISUSM does not cross the Mississippi (see the
table at the top). Action for the campaign lead: an ISWS/WARM account, or a direct
transfer through co-author Trent Ford (Illinois State Climatologist, ISWS).

## What is verified

Live, from this sandbox, on **2026-09-05**:

- **ISUSM station list** - 29 stations via `/geojson/network/ISUSM.geojson`, with
  coordinates, elevation and `archive_begin`.
- **ISUSM endpoints** - `mode=daily`, `mode=hourly`, `mode=hourly&timeres=minute`
  (120 one-minute rows), `mode=inversion` (1440 rows/day, air temperature only),
  and the 422 body that enumerates the legal modes.
- **ISUSM variables** - `vars=` with the full daily and hourly soil lists;
  `vars=sv` expanding to 15 SoilVue depths x (temperature, VWC) at BOOI4;
  `qcflags=1` returning `_f` columns with an `E` (estimated) flag at CRFI4; the
  fixed default column set at a SoilVue station.
- **ISUSM units** - the percent/fraction mismatch measured in the same CSV row at
  all three cadences.
- **ISUSM whole-archive pull** - 29 stations x 2013-12-01..2026-09-03 in one
  request, 109,322 station-days, 26.1 MB, 864 s; audited into 1073 rows.
- **AgClimate** - `/agclimate/isusm.csv` live snapshot (27 stations, and its
  under-reporting of depths, measured against the CGI);
  `/agclimate/hist/daily.php` and `hourly.php` (the forms that document `vars`,
  `qcflags` and `timeres`, and post to the same CGI); `/api/1/openapi.json`;
  `/api/1/isusm/daily.json` returning 26 stations and no soil columns.
- **AWDB** - `/v3/api-docs`; the ignored-parameter behaviour; `*:IA:*,*:IL:*`
  returning 3 SCAN stations with 212-274 station elements each; Ames SMS+STO daily
  for Jun-Aug 2020 with QC flags.
- **SSURGO / SDA** - point mukey and full horizon join at S1 and M1; the
  three-component M1 map unit; a 108-point multipoint domain grid returning 103 map
  units and 120 surface horizons.
- **WARM/ICN** - metadata page 200, bulk-data page still a login.

### Not verified

- **ISUSM `sv` at 1-minute resolution over a long window** - a 5-row minute pull
  with `vars=sv` at BOOI4 succeeded; sustained multi-day minute-resolution SoilVue
  requests were not attempted and may be slow enough to need chunking.
- **AWDB `HOURLY` and `SEMIMONTHLY` durations** - advertised in the station
  elements, only `DAILY` was retrieved.
- **AWDB `/forecasts`** - not relevant to soil, not called.
- **SSURGO polygon (non-multipoint) queries and the `SDA_Get_*` mupolygon
  geometry helpers** - only the point and multipoint intersection helpers were
  exercised. `mapunit`/`component`/`chorizon` only; `Valu1`, `cosoilmoist` and the
  interpretation tables were not touched.
- **gSSURGO raster / Web Soil Survey downloads** - not attempted; SDA covered the
  need.
- **Illinois WARM bulk data** - login. **SCAN Mason #1 and Shagbark Hills series** -
  metadata only.
- **Whether the OSTI4 freeze was caused by the 2020-08-10 derecho** - the dates
  coincide for the 12 in sensors; no maintenance record was consulted.

### Network grants this skill depends on

Granted for this work: `wcc.sc.egov.usda.gov`, `sdmdataaccess.nrcs.usda.gov`.
Already reachable: `mesonet.agron.iastate.edu`. Carried over from
`derechos-data-sources`: `warm.isws.illinois.edu`. No credentials are needed by any
recipe in this skill.

## Helper coverage

All **11** functions and **8** module constants in `kernel.py` (counted with `ast`
over the published file) were enumerated and exercised in one pass after
publication on **2026-09-05**, against live services and against a second location
than the worked example where applicable:
`isusm_soil` (daily / minute+qcflags / inversion), `isusm_soil_varlist`,
`isusm_soil_audit`, `isusm_live_depths`, `awdb_stations`, `awdb_soil_series`,
`sda_query`, `sda_point_profile`, `sda_grid_components` (S1, M1 and NIU/DeKalb -
which resolves to the Wingate series), `derechos_soil_sites`,
`warm_icn_soil_status`. 11 functions defined, 11 called, 0 missed; all 8 constants
read (`IEM`, `AWDB`, `SDA`, `SOILVUE_DEPTHS_IN`, `LEGACY_T_DEPTHS_IN`,
`LEGACY_VWC_DEPTHS_IN`, `ISUSM_MODES`, `DEPTH_IN_TO_CM`).

## Related skills

`derechos-campaign` (H2/SQ1 science case, traceability matrix - load first),
`derechos-data-sources` (ASOS, RAOB, NEXRAD, CropScape CDL, Sentinel-2, mPING,
HRRR, ARM Live; the ISUSM basics this skill extends).
