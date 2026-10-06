---
name: derechos-landuse-imagery
description: "Land use, land-cover change and satellite imagery over the DERECHOS domain (Ames IA to Chicago IL): Planet Labs Data API v1 plus the free NASA CSDA and Planet Education & Research routes; NASA Earthdata land products (authenticated HLS download via LP DAAC, CMR discovery for MOD16 evapotranspiration, MCD12Q1 land cover, LAI, land surface temperature, ECOSTRESS, SMAP, and AppEEARS); USDA NASS Quick Stats county crop statistics; USDA Cropland Data Layer annual crop type and crop-frequency layers; NLCD land cover, impervious and tree-canopy fraction from the MRLC GeoServer WCS; USGS LCMAP annual 30 m land cover 1985-2021. Triggers - Planet Labs, PlanetScope, SkySat, NASA CSDA, HLS, HLSS30, LP DAAC, AppEEARS, MOD16, MCD12Q1, LAI, evapotranspiration, ECOSTRESS, NASS Quick Stats, quickstats, county acreage, crop yield, CDL, Cropland Data Layer, crop frequency, corn soybean rotation, CropScape, NLCD, MRLC, impervious surface, tree canopy, LCMAP, land cover change, land use change."
---

# DERECHOS land use, land-cover change and imagery

Access recipes for crop type, land cover, land-cover change and imagery over the
DERECHOS domain. Every recipe below was exercised against the live service on
**2026-09-05** from this sandbox. The closing sections state exactly what passed,
what did not, and which network grants were needed.

Load `derechos-campaign` for the science case (H1-H4, SQ1-SQ7). Load
**`derechos-data-sources`** first for the sources this skill deliberately does not
re-document: **CropScape CDL point/stat/clip queries, Sentinel-2 L2A via Element84
and Copernicus CDSE, IEM ASOS/ISUSM/RAOB, NEXRAD listing, mPING and HRRR**. This
skill is everything around those.

`kernel.py` auto-loads its helpers. `derechos_landuse_sources()` returns the table
below as data; `derechos_landuse_sources(sq=1)` filters it.

## Source to science question

| Source | Host | What it provides over the domain | Serves | Status |
|---|---|---|---|---|
| **Planet Data API v1** | `api.planet.com` | PlanetScope 3 m near-daily, SkySat, basemaps | SQ1, SQ2, SQ4 | **key required** |
| **NASA HLS** HLSS30/HLSL30 | `data.lpdaac.earthdatacloud.nasa.gov` | 30 m harmonized Landsat+Sentinel-2, ~2-3 day revisit | SQ1, SQ2, SQ4, SQ5 | **verified incl. download** |
| **NASA CMR** | `cmr.earthdata.nasa.gov` | Granule discovery: MOD16 ET, MCD12Q1, LAI, LST, ECOSTRESS, SMAP | SQ1, SQ2, SQ3 | verified |
| **NASA AppEEARS** | `appeears.earthdatacloud.nasa.gov` | Point/area extraction for 187 products | SQ1, SQ2 | **password required** |
| **USDA NASS Quick Stats** | `quickstats.nass.usda.gov` | County corn/soy acreage, yield, planting progress | SQ1, SQ4 | **key required** |
| **USDA CDL** (Planetary Computer) | `planetarycomputer.microsoft.com` | Annual 30 m crop type 2008-2021 + crop-frequency + cultivated | SQ1, SQ2, SQ4, SQ5 | verified |
| **USDA CropScape** | `nassgeodata.gmu.edu` | CDL point/stat/clip 1999-2024, the only path to 2022-2024 | SQ1, SQ2 | **degraded** |
| **NLCD / MRLC GeoServer** | `www.mrlc.gov` | 30 m land cover, impervious %, tree-canopy % | SQ1, SQ2, SQ4 | verified |
| **USGS LCMAP CONUS v1.3** | `planetarycomputer.microsoft.com` | Annual 30 m land cover + change magnitude/date, 1985-2021 | SQ1, SQ2 | verified |

Bounding box used throughout: `LANDUSE_BBOX = [-94.2, 40.7, -87.4, 42.6]` (named so it does not collide with `derechos-data-sources`'s `DERECHOS_BBOX`). Sites:
**S1** 41.356, -91.136 (Muscatine Island Research Farm); **M1** 41.1933, -91.4839
(SERF). In EPSG:5070 (CONUS Albers, which every USDA/USGS raster here uses) those
are **S1 (403655.16, 2049179.73)** and **M1 (375671.32, 2029561.58)** -
`albers5070(lat, lon)` does the conversion.

---

## 1. Planet Labs

There is **no Planet credential in this sandbox**, so nothing past the unauthenticated
surface was exercised. What that surface tells you is still worth recording.

```python
planet_probe()
```

Measured 2026-09-05:

| Endpoint | No credential |
|---|---|
| `GET /data/v1/` | **200** - a HAL index of `asset-types`, `item-types`, `spec` |
| `GET /data/v1/spec` | **200** - the full Swagger 2.0 document, 41 kB, *public* |
| `GET /data/v1/item-types` | 401 `{"message": "Please provide valid credentials...", "errors": []}` |
| `GET /data/v1/asset-types/` | 401, same body |
| `POST /data/v1/quick-search` | 401, same body |
| `GET /basemaps/v1/mosaics` | 401 `{"message":"Credentials Required"}` |
| `GET /subscriptions/v1/` | 401, empty body |
| `GET /compute/ops/orders/v2` | 401, empty body |
| `GET /analytics/` | 401 `{"code":401,"message":"unauthenticated for invalid credentials"}` |

Two useful facts fall out of that:

- **The Data API spec is public.** `GET https://api.planet.com/data/v1/spec` returns
  `Planet Data API 1.0.0`, `basePath: /data/v1`, `host: api.planet.com`, and
  `securityDefinitions: {"basic": {"type": "basic"}}` with `security: [{"basic": []}]`.
  So the authoritative statement of the auth scheme is **HTTP basic**, and you can
  read the whole filter grammar with no account. Paths: `/item-types`,
  `/item-types/{id}`, `/item-types/{id}/items/{id}` (+ `/assets`, `/coverage`,
  `/versions`), `/asset-types`, `/quick-search`, `/searches`, `/searches/{id}/results`,
  `/stats`. Filter definitions in the spec: `AndFilter`, `OrFilter`, `NotFilter`,
  `GeometryFilter` (`field_name` fixed to `geometry`), `DateRangeFilter`
  (`gt/gte/lt/lte`, RFC-3339), `RangeFilter` (numeric `gt/gte/lt/lte`),
  `StringInFilter`, `NumberInFilter`, `UpdateFilter`, `AssetFilter`,
  `PermissionFilter` (enum of `assets.<type>:download` strings). `_page_size`
  maxes at **250**; default sort `published desc`.
- **Every auth form returns the identical 401 body.** Basic auth with the key as
  username, `Authorization: api-key <KEY>`, `Authorization: Bearer <KEY>` and no
  header at all are indistinguishable from the response. You therefore **cannot
  tell a wrong-header mistake from a bad key**. Use HTTP basic - that is what the
  spec declares - and debug key problems on a `GET /data/v1/item-types`, which is
  the cheapest authenticated call.

Ready to run the moment a key exists:

```python
planet_search_payload()                       # the request body, no network
planet_quick_search(os.environ["PLANET_API_KEY"],
                    bbox=[-94.2, 40.7, -87.4, 42.6],
                    start="2020-08-09T00:00:00Z", end="2020-08-12T00:00:00Z",
                    item_types=["PSScene"], max_cloud=0.2)
```

That default window is the 2020-08-10 derecho. The payload includes a
`PermissionFilter` on `assets:download` so the search returns only what the
account can actually order - without it a search over a research quota looks far
more productive than it is.

Item-type names could **not** be verified: `/item-types` is behind the 401 and the
spec carries no enum. Read the list from `/data/v1/item-types` on first
authenticated use rather than trusting a remembered name.

### The two free research routes

Both are real; they grant different things and the difference matters here.

**NASA CSDA (Commercial SmallSat Data Acquisition)** - the right route for a
DOE national-lab PI. NASA buys the archive under an end-user licence and
redistributes it to federally funded researchers, so it is free to the user, and
the licence is unusually permissive: NASA has negotiated terms under which
CSDA-provided Planet data can be shared and published without the usual
commercial restrictions. Eligibility is NASA-defined and covers US federal
civil-servant researchers and federally funded researchers (grantees and
contractors) - a DOE laboratory appointment qualifies on the "federally funded"
limb, not the NASA-employee limb. Access is per-user, requires a NASA Earthdata
login plus CSDA approval, and the archive available is PlanetScope and RapidEye;
**Planet Basemaps and SkySat are excluded**, and the initial per-user download
quota is large (order 10^6 km^2) rather than unlimited. Apply through the
CSDA programme, not through Planet.

**Planet Education & Research (E&R) Basic** - the university route, and the one
a national-lab appointment does **not** get. It requires a verifiable academic
email at a degree-granting institution; **government employees are not
eligible**, and neither is commercial or operational use. The Basic plan grants
roughly **3,000 km^2 per month** of PlanetScope quota, and PlanetScope imagery is
released to E&R users on a **30-day delay**, so it cannot support nowcasting or
near-real-time IOP support. Clipping does not save you quota below a floor:
each intersecting scene is charged at a minimum area (order 100 km^2), so a
handful of small AOIs scattered across the domain burns the monthly allowance
much faster than the AOI areas suggest.

**Consequence for DERECHOS.** The 3,000 km^2/month E&R quota is about **2 %** of
the 139,000 km^2 DERECHOS box - it buys per-site field-scale imagery at S1/M1/R1,
not domain coverage, and never on the day of an IOP. CSDA is the route to plan
around for anything domain-wide or for publication. Verify current terms at
application time; the numbers above were read from the programmes' own pages on
2026-09-05 and both programmes revise quotas.

---

## 2. NASA Earthdata

Credentials: `NASAEDNAME` / `NASAEDTOKEN`. **`NASAEDTOKEN` is an Earthdata Login
bearer token, not a password** - that distinction decides which NASA services you
can reach (see §2.3).

### 2.1 HLS granule download - the gap `derechos-data-sources` left open

`derechos-data-sources` verified the CMR search but not the download. Closed here.

```python
n, ents = cmr_granules("HLSS30", bbox=[-91.19, 41.31, -91.09, 41.41],
                       start="2024-08-01T00:00:00Z", end="2024-08-15T00:00:00Z")
# 5 granules; HLSL30 over the same box/window: 2
hls_download([l["href"] for l in ents[0]["links"] if l["href"].endswith("Fmask.tif")][0],
             "Fmask.tif")                       # 615603 bytes
hls_ndvi(ents[0], 41.1933, -91.4839, half_m=300)
# {'granule': 'HLS.S30.T15TXF.2024216T165849', 'nir_band': 'B08',
#  'red_mean_dn': 335.0, 'nir_mean_dn': 4081.4, 'ndvi': 0.8425, 'n_valid': 400}
```

**The token works as a bearer token directly against the DAAC.** The redirect chain
is short and does not need a URS round trip:

- No `Authorization` header: **302** to
  `https://urs.earthdata.nasa.gov/oauth/authorize?client_id=...&app_type=401` -
  the interactive login. Follow that and you get HTML, not data.
- `Authorization: Bearer $NASAEDTOKEN`: **303** straight to a **presigned CloudFront
  URL** on `d1nklfio7vscoe.cloudfront.net` (plus an `asf-urs` session cookie), with
  `Expires` about 50 minutes out. No URS hop at all.

So the recipe is: one authenticated request with `allow_redirects=False`, read
`Location`, then fetch that URL **without** the `Authorization` header.
`hls_presign()` / `hls_download()` do exactly this. Following redirects naively
also worked here (CloudFront tolerated the re-sent header), but that is
distribution-dependent - do not rely on it.

Gotchas:

- **The presigned host must be allowlisted separately.** `data.lpdaac.earthdatacloud.nasa.gov`
  is reachable but the bytes come from `d1nklfio7vscoe.cloudfront.net`; without a grant
  for that host the download fails at the second hop with a proxy 403 and looks like
  an auth failure.
- **`/vsicurl` with `GDAL_HTTP_HEADERS` does not work** against the protected DAAC
  URL - GDAL reports `not recognized as being in a supported file format` because it
  reads the redirect body, not the TIFF. Presign first, then open
  `/vsicurl/<presigned>` with no headers. `hls_window()` does this and reads a
  20x20-pixel window instead of the whole 3660x3660 tile.
- **S30 granules are frequently partial within the MGRS tile.** On
  `HLS.S30.T15TXF.2024216T165849` the M1 window returned real reflectance while the
  **S1 window was entirely fill** - the Sentinel-2 swath edge cuts between two sites
  34 km apart. Always check `n_valid` before believing a mean; a `nanmean` over an
  all-fill window returns NaN silently (numpy emits only a RuntimeWarning).
- Fill value is `-9999`, reflectance scale `0.0001`, CRS is the UTM zone of the
  MGRS tile (**EPSG:32615** for T15TXF), 30 m, `Fmask` nodata 255.
- The NIR band differs between products: **B08 for S30, B05 for L30**. Using B08 on
  an L30 granule silently gives you a different wavelength.

### 2.2 What else NASA covers over this domain - CMR granule counts

Measured 2026-09-05 over the full DERECHOS box. MODIS/VIIRS tile is **h11v04**;
HLS tiles are T15TUH / T15TXF / T16TCL / T16TDL.

| Collection | Product | Window queried | Granules |
|---|---|---|---|
| `MCD12Q1` | MODIS 500 m annual land cover type | 2001-2025 | **48** |
| `MOD16A2GF` | Terra 500 m 8-day gap-filled ET/LE | 2024 | **92** |
| `MOD16A3GF` | Terra 500 m annual gap-filled ET | 2001-2025 | **50** |
| `MCD15A3H` | 500 m 4-day LAI/FPAR | Jul 2024 | **18** |
| `MOD11A2` | Terra 1 km 8-day LST | Jul 2024 | **10** |
| `VNP21A2` | VIIRS 1 km 8-day LST | Jul 2024 | **10** |
| `ECO_L3T_JET` | ECOSTRESS **70 m** tiled ET | Jun-Aug 2024 | **287** |
| `ECO_L4T_ESI` | ECOSTRESS 70 m evaporative stress index | Jun-Aug 2024 | **288** |
| `ECO_L2T_LSTE` | ECOSTRESS 70 m tiled LST | 1-15 Aug 2024 | **149** |
| `HLSS30` | 30 m Sentinel-2 harmonized | 2024 | **2383** |
| `HLSL30` | 30 m Landsat harmonized | 2024 | **1899** |
| `SPL4SMGP` | SMAP L4 9 km surface + root-zone soil moisture | 1-5 Aug 2024 | **34** |
| `LCMAP_CU_ANNUAL_LAND_COVER` | - | 1985-2022 | **0** |
| `NLCD_LAND_COVER_L48` | - | 2001-2022 | **0** |

**ECOSTRESS is the headline for the campaign's ET hypotheses.** At 70 m it resolves
individual fields, where MOD16's 500 m pixel averages a corn field, a soybean
field and a farmstead together - exactly the heterogeneity the white paper's
§4.2.2 says MOD16-class products miss at SGP. Nearly 300 ET granules over one
warm season is a usable sample; the cost is the ISS-dependent, irregular overpass
schedule, so it cannot give you a fixed-time-of-day series.

**Neither LCMAP nor NLCD is discoverable through CMR** - both return 0 hits.
Get them from §4 and §5 instead. Do not conclude from a 0-hit CMR search that a
land-cover product does not cover the domain.

MODIS/VIIRS granules are **HDF-EOS2 (`.hdf`)**, and the rasterio/GDAL build in
this sandbox has **no HDF4 driver** (`rasterio 1.5.1 / GDAL 3.13.3`;
`HDF4`/`HDF4Image` absent). Install `pyhdf` (conda-forge) to read them, or take
the point/area extraction route in §2.3 instead. ECOSTRESS `*_L3T_*` / `*_L2T_*`
tiled products are cloud-optimized GeoTIFF and need none of that.

### 2.3 AppEEARS - catalogue is public, task submission is not

```python
appeears_products(r"MOD16|MCD12Q1|MCD15|MOD11|VNP21|ECO_L3T")
appeears_layers("MOD16A2GF.061")
```

`GET /api/product` returns **187 products** with no credential at all, each carrying
`ProductAndVersion`, `Resolution`, `TemporalGranularity`, `TemporalExtentStart/End`,
`DOI` and `Available`. `GET /api/product/<id>` (layer names) and
`GET /api/quality/<id>` are also public. That is enough to plan a request
precisely. Products relevant here include `MCD12Q1.061` (500 m yearly land cover),
`MOD16A2GF.061` / `MOD16A3GF.061` / `MYD16*` (ET), `MCD15A2H.061` / `MCD15A3H.061`
/ `MOD15A2H.061` / `VNP15A2H.002` (LAI/FPAR), `MOD11A1/A2` + `MYD11A1/A2` +
`VNP21A1D/A1N/A2` (LST), `MCD43A1-A4` (BRDF/albedo), `MOD13*` / `VNP13*` (NDVI/EVI),
`SPL3SMP_E.006` / `SPL4SMGP.008` / `SPL3FTP.004` (soil moisture, freeze/thaw),
`L04-L09.002` (Landsat 4-9 ARD 30 m), `HLSS30/HLSL30.020` and their `_VI` vegetation-index
variants, and the ECOSTRESS `ECO_*` family including `ECO_L3T_ET_ALEXI.002`.
There is **no CDL, NLCD or LCMAP product in AppEEARS**.

**Task submission was not completed, and cannot be with the credentials configured.**
Measured 2026-09-05:

| Call | Result |
|---|---|
| `GET /api/task` with `Authorization: Bearer $NASAEDTOKEN` | **403** "You don't have the permission to access the requested resource" |
| `GET /api/task` with no auth | 403, identical body |
| `POST /api/login` with `Authorization: Bearer $NASAEDTOKEN` | **403**, identical body |
| `POST /api/login` HTTP basic (`NASAEDNAME`, `NASAEDTOKEN` as password) | **401** "could not verify that you are authorized" |
| `GET /api/bundle` with bearer | **500** HTML error page |

AppEEARS mints **its own** session token from `POST /api/login` under HTTP basic
with the Earthdata **username and password**; it does not accept an EDL bearer
token, and the 401 confirms the token is not usable as a password. The
distinction between the 403 (no AppEEARS session) and the 401 (bad basic
credentials) is the diagnostic.

The submit/poll/download shape - `POST /api/login` -> `token`, then
`POST /api/task` with `Authorization: Bearer <appeears token>` and a
`{"task_type": "point", "params": {"coordinates": [...], "layers": [...]}}`
body, then `GET /api/status/<task_id>` and `GET /api/bundle/<task_id>` -
is **documented, not verified**. The point request at S1 and M1 was **not run**.
Action for the campaign lead: an Earthdata *password* (or a service account) is
what unlocks this; the token alone is not enough.

---

## 3. USDA NASS Quick Stats

County-level corn and soybean acreage, yield and planting progress - the
statistical complement to the CDL's per-pixel view, and the only source here for
*planting date* progress, which matters for stratifying IOPs by crop stage.

**No key is configured, and nothing works without one.** Measured 2026-09-05:
`get_param_values`, `api_GET` and `get_counts`, with `key` absent, `key=` empty, or
`key=BADKEY`, all return **HTTP 401 `{"error":["unauthorized"]}`** - one identical
26-byte body, so a malformed query is indistinguishable from a missing key. The
root `https://quickstats.nass.usda.gov/api` page (200, HTML) *is* the registration
form.

```python
nass_key_help()
# register at https://quickstats.nass.usda.gov/api  -- POST fields: name, email, agree
# the key is emailed immediately; 50,000-record cap per api_GET call
```

Once a key exists (grammar read off the live docs page, so the field names are
authoritative even though no query was executed):

```python
nass_count(key, commodity_desc="CORN", statisticcat_desc="AREA HARVESTED",
           agg_level_desc="COUNTY", state_alpha="IA", year__GE=2008)
nass_query(key, commodity_desc="CORN", statisticcat_desc="YIELD",
           agg_level_desc="COUNTY", state_fips_code="19", county_ansi="139",
           year__GE=2008, format="CSV")
```

Three resources: **`/api/api_GET`** (data, 50 k records max),
**`/api/get_counts`** (record count for the same filter - call it first),
**`/api/get_param_values?param=<field>`** (valid values for one field).
`format` is `JSON` (default), `CSV` or `XML`; `callback` only for JSONP.

Parameters are grouped *what* / *where* / *when*. The **35 returned fields** are, in
CSV column order: `source_desc, sector_desc, group_desc, commodity_desc, class_desc,
util_practice_desc, prodn_practice_desc, statisticcat_desc, unit_desc, short_desc,
domain_desc, domaincat_desc, agg_level_desc, state_ansi, state_alpha, state_name,
asd_code, asd_desc, county_ansi, county_name, region_desc, zip_5, watershed_code,
watershed_desc, congr_district_code, country_code, country_name, year, freq_desc,
begin_code, end_code, reference_period_desc, week_ending, load_time, Value`.
Any of them can be used as a filter.

For the DERECHOS counties: `agg_level_desc="COUNTY"` with
`state_fips_code="19"` (Iowa) or `"17"` (Illinois) and a `county_ansi` list;
`commodity_desc="CORN"` / `"SOYBEANS"`; `statisticcat_desc` in
`"AREA PLANTED"` / `"AREA HARVESTED"` / `"YIELD"` / `"PRODUCTION"`;
`source_desc="SURVEY"` for the annual estimates and `"CENSUS"` for the
five-yearly Census of Agriculture. Planting progress lives under
`freq_desc="WEEKLY"` with `statisticcat_desc="PROGRESS"` and is published at
**state and agricultural-district level, not county**.

Gotchas verified from the docs and the sample output:

- **Range operators are suffixes on the field name**: `year__GE=2012` is the form
  shown in the service's own example. The full operator list
  (`__LE __LT __GT __NE __LIKE __NOT_LIKE`) lives on the `param_define` page,
  which renders client-side and could not be scraped - treat anything beyond
  `__GE` as unconfirmed until you run it.
- **`Value` is a comma-grouped string**, e.g. `"510,000"`. Strip commas before
  casting or every acreage silently becomes NaN.
- **One `short_desc` returns several rows per year** distinguished only by
  `reference_period_desc` - the sample output shows `YEAR` alongside
  `YEAR - MAR FORECAST` for the same 2012 Virginia corn record, with different
  values and `load_time`. Filter `reference_period_desc="YEAR"` or you will
  average forecasts into the final estimate.
- Over the 50 k cap the API does not paginate; narrow the filter or use the bulk
  file downloads.

---

## 4. USDA Cropland Data Layer - use the Planetary Computer, not CropScape

`derechos-data-sources` documents CropScape's `GetCDLValue` / `GetCDLStat` /
`GetCDLFile` and their gotchas (EPSG:5070 coordinates, `format=json` returning a
JavaScript object literal with unquoted keys, the two-step `<returnURL>`). All of
that still holds. What has changed is that **CropScape is badly degraded**.

Measured 2026-09-05:

- `https://nassgeodata.gmu.edu/CropScape/` now **302-redirects to
  `https://cat.csiss.gmu.edu/CropSmart/signin`** - the interactive tool is behind
  a sign-in on a different host.
- The `axis2` SOAP/REST service still answers, but **2 of 3 `GetCDLValue` calls
  timed out past 200 s**; the third returned in 43 s. A 56-call harvest with three
  retries per call and 5 s backoff did complete (52/56 succeeded) but took over an
  hour.
- `GetCDLStat` is worse than `GetCDLValue`: a 1 x 1 km bbox request for S1 2022
  failed on **all four attempts** at a 180 s timeout, so the two-step
  `<returnURL>` path could not be exercised at all on 2026-09-05.
- `cropland.usda.gov` **does not resolve at all** (immediate connection failure,
  not a proxy block).

So: for anything more than a handful of points, read the CDL from the
**Planetary Computer STAC** collection `usda-cdl`, which serves it as
cloud-optimized GeoTIFFs in EPSG:5070 at 30 m.

```python
items = pc_search("usda-cdl", query={"usda_cdl:type": {"eq": "cropland"}})   # 406 items
sas   = pc_sas("usda-cdl")                                                   # anonymous
names = cdl_class_names()                                                    # 133 classes
cdl_field_crop(41.1933, -91.4839, 2021)
# {'year': 2021, 'code': 1, 'crop': 'Corn', 'dominant_frac': 0.550,
#  'crop_frac': 0.927, 'n_px': 1156}
c = cdl_domain_counts(2021)          # exact 30 m pixel counts over the whole box, ~25 s
cdl_frequency(41.1933, -91.4839, "corn")
# {'band': 'corn', 'point_years': 7, 'window_mean_years': 6.83, 'nodata_px': 72, ...}
```

Structure of the collection, as measured:

- `usda_cdl:type` takes **`cropland`**, **`frequency`** and **`cultivated`**.
- **Coverage is 2008-2021 only** - 29 90-km tiles per year x 14 years over the
  DERECHOS box. 2022-2024 are **not** here; CropScape is still the only path to
  them.
- `cropland` items carry a `cropland` and a `confidence` asset;
  `frequency` items carry **`corn`, `soybeans`, `wheat`, `cotton`** - these are the
  CDL **crop-frequency derivative layers**, giving the number of years each pixel
  was planted to that crop over 2008-2021. `cultivated` items carry a `cultivated`
  asset (the cultivated/non-cultivated mask). There is **no crop-rotation
  (sequence) layer** in this collection; a rotation has to be reconstructed from
  the annual `cropland` rasters, which is what `cdl_field_crop()` over a year
  range does.
- Class names come from the STAC `classification:classes` extension on the
  `cropland` asset - **133 entries**, so you never need a hard-coded CDL legend.

### Gotchas that will give you the wrong answer quietly

- **A single 30 m pixel is not a field label.** At S1's exact coordinate the CDL
  reads *Developed/Open Space* (121) every year from 2008 to 2018, *Barren* (131)
  in 2019, then Corn in 2020 and Soybeans in 2021. `derechos-data-sources`
  reports "S1 -> Soybeans, 2024" from a point query - that is true of that pixel
  in that year and is **not** the site's crop history. Use `cdl_field_crop()`
  (dominant crop in a 1 km window, non-crop classes masked) and read the
  `crop_frac` it returns: S1's window is only **44-49 %** crop, against **86-93 %**
  at M1.
- **Frequency-layer 255 is nodata, not "255 years".** The raw 1 km window mean at
  S1 is 105.8 for corn because 465 of 1156 pixels are 255; masked it is **5.38**.
  `cdl_frequency()` masks it and reports `nodata_px` so you can see how much of
  the window was never cropland.
- **The CDL's non-crop classes are not temporally consistent.** Over this box,
  Grassland/Pasture (176) drops from 22,633 km^2 in 2010 to **13,180 km^2** in 2011
  while Other Hay/Non Alfalfa (37) rises from 444 to 3,432 and Alfalfa (36) from
  1,067 to 2,634 - a classifier artefact, not land-use change. Similarly the
  *total* developed area is flat (15,897 -> 15,515 km^2 over 2008-2021) while
  Developed/Medium Intensity alone appears to grow 64 % and Developed/Open Space
  to shrink 38 %: internal reshuffling between the four developed classes. **Only
  the corn and soybean classes are trustworthy for interannual change**; group
  everything else before differencing.
- Code **0 is background**, a constant 3,832 km^2 of the box (the mosaic's
  outside-footprint area). Exclude it from any percentage denominator.
- **Do not use cartopy to place lat/lon on these EPSG:5070 rasters.** Measured
  2026-09-08 with cartopy 0.25.0 / pyproj: both `ccrs.AlbersEqualArea(central_longitude=-96,
  central_latitude=23.0, standard_parallels=(29.5, 45.5))` and `ccrs.epsg(5070)` place a
  lat/lon point about **23.8 km too far north** (and 1.2-1.4 km west) of where
  `albers5070()` puts it. Settled against the data, not by argument: a point in the
  Mississippi channel at 41.52, -90.57 reads **111 Open Water** through
  pyproj/`rasterio.warp.transform` and **5 Soybeans** through cartopy's `transform_point`;
  farmland at 41.356, -91.25 reads 1 Corn vs 176 Grassland/Pasture. `albers5070()` (a plain
  `Transformer.from_crs("EPSG:4326","EPSG:5070")`) is the correct one.
  The failure is quiet and symmetric: an `imshow` with `extent=albers5070_bbox(...)` lands at
  true EPSG:5070 coordinates, but every marker, graticule line and box drawn through cartopy
  lands 24 km north of it, so the map looks internally consistent while every annotated
  position is wrong by most of a CDL tile. Keep coordinates in pyproj and draw on plain
  matplotlib axes in EPSG:5070 metres; `plotmap.py` (saved as a project artifact) carries
  `ll2a`, a pyproj `graticule`, `radial` and `scalebar` for this.
- The SAS token expires (about an hour). Re-mint with `pc_sas()` inside long loops;
  an expired token surfaces as a rasterio open failure, not an auth message.

---

## 5. NLCD and the MRLC GeoServer

`www.mrlc.gov` runs a GeoServer with **both** WMS 1.3.0 and **WCS 2.0.1**; the WCS
is what you want, because it returns real GeoTIFF. No credentials.

```python
mrlc_coverages(r"NLCD_2021|Impervious_L48|tcc_conus_2021|Annual_NLCD")
mrlc_wcs_geotiff("mrlc_download__NLCD_2021_Land_Cover_L48", "m1_lc2021.tif",
                 centre=(41.356, -91.136), half_m=5000)      # 333x333 uint8, 30 m
mrlc_wcs_geotiff("mrlc_download__NLCD_2021_Land_Cover_L48", "domain_lc2021.tif",
                 scalefactor=0.1)                             # 300 m over the whole box
```

Measured: GetCapabilities returns **1764 WMS layer names** and **446 WCS coverage
ids**. Every coverage is **EPSG:5070**, 30 m, `axisLabels="X Y"`, CONUS extent
`(-2493045, 177285)` to `(2342655, 3310005)`, grid `161190 x 104424`.

Epochs available for change analysis over the L48, from the WCS coverage list:

| Product | Coverage id pattern | Epochs |
|---|---|---|
| Land cover | `mrlc_download__NLCD_<YEAR>_Land_Cover_L48` | 2001, 2004, 2006, 2008, 2011, 2013, 2016, 2019, 2021 |
| Land cover (science product) | `..._Land_Cover_Science_Product_L48` | same nine |
| Impervious % | `mrlc_download__NLCD_<YEAR>_Impervious_L48` | 2001, 2004, 2006, 2008, 2011, 2013, 2016, 2019, 2021 |
| Impervious descriptor | `..._Impervious_descriptor_L48` | same nine |
| Tree canopy % | `mrlc_download__nlcd_tcc_conus_<YEAR>_v2021-4` | 2011-2021, **annual** |
| 2001-2021 change | `mrlc_download__NLCD_2001_2021_Land_Cover_Change_Index_L48` | one layer |
| 2001-2021 change count / first disturbance | `mrlc_download__NLCD_01_21_Land_Cover_Change_Count`, `..._First_Disturbance_Date` | one each |
| Annual NLCD 1985-2023 summary | `mrlc_download__Annual_NLCD_Smy_LndCov_ChgCnt_1985_2023_CU_C1V0`, `..._ChgIdx_...` | one each |

### Gotchas

- **Annual NLCD's per-year land cover is NOT on this GeoServer.** Only the two
  1985-2023 *summary* layers (change count, change index) are published. Searching
  WMS and WCS for `LndCov` returns exactly five names, all summaries. For the
  annual 1985-2023 land-cover rasters use the MRLC bulk download or **LCMAP
  (§6)**, which is annual, 30 m and directly readable.
- **A full-domain 30 m GetCoverage silently drops the connection.** The DERECHOS
  box at 30 m is 19100 x 8097 px; the request ran 152 s and then raised
  `ChunkedEncodingError: Response ended prematurely` - no HTTP error, no partial
  TIFF. Use `scalefactor<=0.1` for domain-wide work (11 s, 2.1 MB) and full
  resolution only for site-scale windows (10x10 km in about 1 s).
- **`scalefactor` resamples a categorical raster.** Fine for an overview image;
  never take class-area statistics off a scaled request. Take them at native
  resolution over a window.
- **The 2001-2021 Change Index uses 1 for "no change", not 0.** A naive `>0`
  test says 100 % of pixels changed. Measured in the 10x10 km windows: value 1
  covers 104,021/110,889 px at S1 and 107,861/110,889 at M1, so the real
  changed fractions are **6.2 %** and **2.7 %**.
- Tree-canopy coverage ids carry the `v2021-4` version suffix, and the AK/HI/PR
  variants sit next to the CONUS ones in the same list - match on
  `tcc_conus_<year>` or you will fetch Hawaii.

Measured at the two core sites (10x10 km windows, 30 m, native resolution):

| | S1 | M1 |
|---|---|---|
| NLCD 2021 / 2001 at the site pixel | **71 Herbaceous** (both years) | **82 Cultivated Crops** (both years) |
| Cultivated Crops, % of window | 51.8 (2001) -> 52.4 (2021) | 74.2 -> 75.4 |
| Impervious %, window mean | **6.28** | 1.86 |
| Tree canopy %, window mean | **11.80** | 4.09 |
| Annual NLCD 1985-2023 change count, mean / max | 0.25 / 21 | 0.19 / 20 |
| Pixels with >= 1 change, 1985-2023 | 14.9 % | 12.9 % |

That is the paired-site contrast in one table: S1 sits in a mixed, partly
developed, partly wooded mosaic (6.3 % impervious, 11.8 % canopy) while M1 is
near-monoculture row crop (1.9 %, 4.1 %). For H1 and SQ2 - land-use heterogeneity
controlling PBL stability - S1 is the heterogeneous member and M1 the homogeneous
one, which is a stronger framing than "sandy vs loam".

---

## 6. USGS LCMAP CONUS v1.3 - annual 30 m land cover back to 1985

The 30 m land-cover-change product the task asked for. **Not in CMR** (0 hits);
it is in the Planetary Computer as `usgs-lcmap-conus-v13`.

```python
lcmap_point_history(41.356, -91.136)
# {1985: {'code': 3, 'class': 'Grass/Shrub'}, ... 2021: {'code': 3, 'class': 'Grass/Shrub'}}
lcmap_point_history(41.1933, -91.4839)
# {1985: {'code': 2, 'class': 'Cropland'}, ... 2021: {'code': 2, 'class': 'Cropland'}}
```

Measured: **296 items over the DERECHOS box**, 8 ARD tiles x 37 years,
**1985-2021**, ids of the form `LCMAP_CU_021008_2021_V13_CCDC`. Assets per item:
`lcpri` (primary land cover), `lcsec` (secondary), `lcpconf` / `lcsconf`
(confidence), `lcachg` (annual change), `scmag` / `scmqa` / `sclast` / `scstab` /
`sctime` (spectral change magnitude, QA, last change, stability, time), `dates`,
`browse`, plus a `*_metadata` sidecar per band.

`lcpri` legend from the STAC classification extension:
`0 No Data, 1 Developed, 2 Cropland, 3 Grass/Shrub, 4 Tree Cover, 5 Water,
6 Wetlands, 7 Snow/Ice, 8 Barren`.

**Cross-product agreement at the site pixels is the useful result.** LCMAP calls
S1 *Grass/Shrub* in every year 1985-2021, NLCD calls it *Herbaceous* in 2001 and
2021, and the CDL calls it *Developed/Open Space* 2008-2018. Three independent
30 m products agree that the exact S1 station coordinate is **not** a cropped
pixel; M1's is *Cropland* / *Cultivated Crops* / corn-or-soy in all three. Any
analysis that reads the crop at S1 from a single pixel is reading the research
farm's yard, not its fields.

---

## 7. Worked result - multi-year land-use change over the domain and at the sites

Artifacts: `derechos_cdl_site_history.csv`, `derechos_cdl_domain_area_by_class.csv`,
`derechos_cdl_domain_area_grouped.csv`, `derechos_nlcd_site_stats.csv`,
`derechos_landuse_change.png`.

### Domain-wide crop area, 2008-2021, exact 30 m counts

150,917,528 pixels per year (135,826 km^2, of which 3,832 km^2 is background),
identical across all 14 years - so the year-to-year differences are real
reclassification, not a changing footprint.

| | 2008 | 2021 | change |
|---|---|---|---|
| Corn | 44,572 km^2 | 43,138 km^2 | **-3.2 %** |
| Soybeans | 27,342 km^2 | 33,442 km^2 | **+22.3 %** |
| Corn + soybeans | 71,914 km^2 | 76,580 km^2 | **+6.5 %** |
| Corn : soybean ratio | **1.630** | **1.290** | -21 % |
| Grass / hay / fallow | 25,043 km^2 | 18,843 km^2 | -24.8 % (**see the CDL caveat in §4**) |
| Developed, all four classes | 15,897 km^2 | 15,515 km^2 | -2.4 % |
| Forest | 13,211 km^2 | 13,569 km^2 | +2.7 % |

The domain is **intensifying into row crop and shifting toward soybeans**: nearly
5,000 km^2 of additional corn-or-soybean area in 13 years, taken mostly from
grass/hay/fallow, with essentially no urban expansion. Corn peaks at 49,274 km^2
in 2011 (the ethanol-price year) and 2019 shows the flood signature - Fallow/Idle
Cropland jumps from 18 to **4,263 km^2**, corn and soybeans both fall.

Since the corn-soybean *fraction* of the domain grows while soybeans replace part
of the corn, the campaign's H4 (crop type controlling BL turbulence and clouds)
has a real trend to work against rather than a static land surface: the domain's
mean growing-season canopy has been drifting toward the lower-LAI, earlier-senescing
member of the rotation.

### Do S1 and M1 stay out of phase? No.

This is the question the paired-site design turns on, and the answer is
disappointing. Field-scale dominant crop in a 1 km window at each site:

| Years | S1 | M1 | Phase |
|---|---|---|---|
| 2008-2012 | corn, soy, corn, soy, corn | soy, corn, soy, corn, soy | **opposite** |
| 2013-2021 | corn, soy, corn, soy, corn, soy, corn, soy, corn | identical | **same crop** |

The two sites were cleanly anti-phased for five years, then locked into the same
phase from 2013 onward and stayed there for nine. At the *pixel* level CropScape
reports S1 in soybeans and M1 in corn for 2024 - opposite again - but S1's pixel
is the farmyard (§4), so that is not evidence about the fields.

**Consequence:** DERECHOS cannot assume a corn-versus-soybean contrast between S1
and M1 in any given season. Either confirm the planted crop with the ISU farm
managers each spring and treat the contrast as a measured covariate rather than a
design feature, or lean on the contrast that *is* stable - S1's mixed,
partly-developed, 6.3 %-impervious mosaic against M1's 75 %-row-crop homogeneity
(§5), which has held since at least 1985 in LCMAP.

Supporting numbers: over 2008-2021 the CDL crop-frequency layers give M1
**7 years of corn and 7 of soybeans** out of 14 at its station pixel - a textbook
alternation - against 1 and 1 at S1's (because that pixel is not cropland).
M1's 1 km window is 86-93 % crop in every year; S1's is 37-49 %.

### Cross-validation

The CropScape point history (1999-2024, 52 of 56 requests succeeded; 1997 and
1998 failed at both sites, 1999-2000 return "No Data" so the usable record starts
**2001**) and the Planetary Computer COGs agree on the class code at **28 of 28**
site-years where both have data - including the awkward ones, S1's
Developed/Open Space run 2008-2018 and its Barren 2019. Two independent
distributions of the same USDA product, one slow and one fast, give the same
answer; use the fast one.

---

## What is verified

Exercised against the live service on **2026-09-05** from this sandbox:

- **Planet** - the nine unauthenticated endpoint responses in §1 and the public
  Swagger 2.0 document (parsed: `securityDefinitions`, all 13 paths, all 13 filter
  definitions, `_page_size` max 250).
- **NASA HLS** - CMR search (HLSS30 5 granules, HLSL30 2 over a 0.1-degree box
  around S1 for 1-15 Aug 2024); **authenticated download** of
  `HLS.S30.T15TXF.2024216T165849.v2.0.Fmask.tif` (615,603 bytes) with the bearer
  token, opened with rasterio (EPSG:32615, 3660x3660, uint8, 30 m, nodata 255);
  the 302-vs-303 redirect comparison; a presigned windowed two-band read giving
  NDVI **0.8425** at M1 and an all-fill window at S1 on the same granule.
- **NASA CMR** - the 14-collection granule-count survey in §2.2.
- **NASA AppEEARS** - `/api/product` (187 products), `/api/product/<id>`,
  `/api/quality/<id>` public; the five auth attempts in §2.3.
- **NASS Quick Stats** - the 401 behaviour on five endpoint/key combinations, the
  registration form fields, and the 35-field record schema and operator example
  from the live docs page.
- **USDA CDL via Planetary Computer** - 406 `cropland` + 29 `frequency` + 29
  `cultivated` items; 133-entry class legend; exact 30 m domain counts for all 14
  years; 1 km field-scale dominant crop for both sites x 14 years; corn/soybean
  frequency at both sites; SAS minting.
- **CropScape** - the CropSmart redirect, the timeout rate, and a 56-call
  `GetCDLValue` harvest for 1997-2024 at both sites (52 succeeded).
- **MRLC** - WMS and WCS GetCapabilities (1764 layers / 446 coverages),
  `DescribeCoverage`, the full-domain 30 m connection drop, a `scalefactor=0.1`
  domain retrieval, and twelve native-resolution 10x10 km site retrievals (land
  cover 2001 and 2021, impervious 2021, tree canopy 2021, change index,
  Annual NLCD change count) opened and tabulated.
- **LCMAP** - 296 items over the box, asset and legend enumeration, and `lcpri`
  point history at both sites for 1985/1995/2005/2015/2021.

## Not verified

- **Planet, anything authenticated.** No key exists in this sandbox. The search
  payload in §1 is schema-checked against the public spec but has never received a
  200. The item-type names, asset names and quota behaviour are unverified.
  `docs.planet.com` is not allowlisted and was not requested.
- **NASA CSDA and Planet E&R terms** were read from the programmes' own web pages
  on 2026-09-05, not from a contract. Re-check at application time.
- **AppEEARS task submission, status polling and bundle download.** Needs an
  Earthdata password; only the public catalogue endpoints were exercised. The S1/M1
  point request was **not** run.
- **NASS Quick Stats queries.** No key. Field names and the `__GE` operator come
  from the live docs page; the operator suffixes beyond `__GE` were not confirmed,
  and no query has been executed. A key was deliberately **not** registered - that
  requires submitting the user's email address.
- **MODIS/VIIRS HDF-EOS reads.** Granule counts were confirmed through CMR; no
  `.hdf` was downloaded or opened (no HDF4 driver in the sandbox GDAL). MOD16 and
  MCD12Q1 values at S1/M1 are **not** measured here.
- **ECOSTRESS granule download.** Counts confirmed through CMR; no ECOSTRESS COG
  was fetched.
- **CDL 2022-2024 at field scale.** The Planetary Computer collection stops at
  2021 and CropScape's `GetCDLStat` was too slow to complete during the session;
  only single-pixel CropScape values exist for 2022-2024.
- **NLCD Annual (1985-2023) per-year land cover.** Only the two summary layers are
  on the GeoServer; the annual rasters were not retrieved from any source.
- **`cropland.usda.gov`** was allowlisted on request and then found not to resolve
  at all. **`www.nass.usda.gov`** is not allowlisted; the bulk CDL national raster
  download path was therefore not tested.

## Network grants this skill depends on

Granted while building it: **`api.planet.com`**, **`quickstats.nass.usda.gov`**,
**`appeears.earthdatacloud.nasa.gov`** (all three pre-granted for this work),
**`d1nklfio7vscoe.cloudfront.net`** (the LP DAAC presigned-download host - HLS
downloads fail at the second hop without it), **`planetarycomputer.microsoft.com`**,
**`landcoverdata.blob.core.windows.net`** (the Azure host behind the CDL and LCMAP
COGs), and **`cropland.usda.gov`** (granted, then found dead).
Already default-reachable: `cmr.earthdata.nasa.gov`,
`data.lpdaac.earthdatacloud.nasa.gov`, `www.mrlc.gov`, `nassgeodata.gmu.edu`.
Blocked and not needed: `docs.planet.com`. Not requested:
`www.nass.usda.gov`.

## Helper coverage

All **28** functions in `kernel.py` were enumerated with `ast` and called in a
single pass after publication: 28 defined, 28 called, 0 missed. The pass ran the
remote-raster paths at **NIU/DeKalb (41.93, -88.77)** rather than S1/M1, so the
recipes are not tuned to one point - and it caught the L30-versus-S30 NIR-band
difference (`hls_ndvi` on `HLS.L30.T16TCM.2024221T164025` returned NDVI 0.546
from B05, over a pixel all three land-cover products call developed).

## Related skills

`derechos-campaign` (science case, traceability matrix - load first),
`derechos-data-sources` (CropScape CDL basics, Sentinel-2 via Element84 and CDSE,
IEM, NEXRAD, mPING, HRRR - **load it too; this skill assumes it**).
