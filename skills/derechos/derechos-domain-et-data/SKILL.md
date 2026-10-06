---
name: derechos-domain-et-data
description: "Tested access recipes for evapotranspiration and surface-flux data over the DERECHOS domain (Ames IA to Chicago IL), plus the DERECHOS ET map results built from them. Ranks 31 candidate sources - OpenET, ECOSTRESS ECO_L3T_JET, MOD16A2GF/A3GF, NLDAS-2 Noah, SSEBop, SMAP L4, HRRR, gridMET, Landsat C2 L2 surface temperature, AmeriFlux, ARM SGP ECOR/SEBS, IEM ISUSM - with auth maps, allowlist hosts, and the traps that silently return wrong ET: the MOD16 missing fill-value, ECOSTRESS night and near-empty granules, stale Planetary Computer mirrors, and naming errors that return success with no data. Load before fetching ET or flux data over the Midwest, building a domain ET product, or picking a validation tower. Triggers - DERECHOS, evapotranspiration, ET map, domain ET, latent heat flux, OpenET, ECOSTRESS, ECO_L3T_JET, MOD16, MOD16A2GF, NLDAS, SSEBop, SMAP L4, gridMET, reference ET, Landsat surface temperature, AmeriFlux, amfcdn, ARM ECOR, SEBS, EBBR, ISUSM, Muscatine, SERF, Cropland Data Layer."
---

# DERECHOS domain ET data

Getting bytes for an evapotranspiration map over the Ames-to-Chicago domain, and what a
first such map actually showed. Load `derechos-campaign` for the science case,
`cropland-et-measurement` for the tower side, `domain-et-inference` for method choice.
This skill is the data layer plus one measured result.

`derechos_et_sources()` returns the bundled 31-row source table
(`derechos_et_sources.csv`); `derechos_flux_towers()` returns the 68-row AmeriFlux
candidate table (`derechos_ameriflux_cropland_sites.csv`).

## Two corrections to sibling skills

- **AmeriFlux IS reachable.** `derechos-data-sources` records it as unreachable on the
  basis of `amfcdata.lbl.gov` (502) and `ameriflux.lbl.gov` (403). Both still fail, but
  **`amfcdn.lbl.gov` works anonymously** and returns all 844 sites. See the AmeriFlux
  section below.
- **The ISUSM data endpoint is `/cgi-bin/request/isusm.py`**, not `/agclimate/isusm.py`,
  which returns a PNG plot when handed data parameters.

## The measured result, 3 July - 3 August 2024

A domain ET map was built from MOD16A2GF (tiles h10v04 + h11v04, DOY 185-216 summed,
reprojected from MODIS sinusoidal to EPSG:4326) and stratified by USDA CDL 2021
fractional cover per 500 m cell. Artifacts: `derechos_domain_et_jul2024.tif` (5 bands),
`derechos_domain_et_metrics.csv`, `derechos_domain_et_map.png`,
`derechos_et_error_assessment.png`.

| Quantity | Value |
|---|---|
| Domain median ET | **4.24 mm day-1** (mean 4.30, 91 % of domain retrieved) |
| Domain median ET/PET | 0.70 |
| Corn-dominant pixels, mean ET | 4.43 mm day-1 |
| Soybean-dominant pixels, mean ET | 4.48 mm day-1 |
| Developed-dominant pixels, mean ET | 3.45 mm day-1 |
| 500 m pixels >= 80 % one CDL class | **13.4 %** |
| Domain >50 % corn+soy | 63.9 %, median minority-crop share 0.22 |
| Median ET spread within one 490 m block (70 m ECOSTRESS) | **16 % of the block mean** |
| MOD16 spread across the same scene | 0.88 mm day-1 |
| MOD16 vs ECOSTRESS spatial correlation | **Pearson r = 0.17**, n = 34,795 blocks |
| MOD16 ET / ISUSM reference ET | 0.85 at S1, **1.34 at M1** |

Four things to carry forward:

1. **The 500 m pixel is a crop mixture almost everywhere.** Only 13 % of pixels are
   80 % one class. Any corn-versus-soybean ET contrast read off MOD16 is reading a
   mixture, which is the white-paper section 4.2.2 heterogeneity claim, quantified.
2. **Corn and soybean ET are indistinguishable at this scale** (4.43 vs 4.48 mm day-1),
   independently reproducing the tower-based literature result. Do not expect a crop-type
   ET signal in the *level*; look for it in timing.
3. **The two products agree on the domain mean far better than on the pattern.** Daily
   totals across MOD16, ECOSTRESS and NLDAS agree to about 15 %, but the spatial
   correlation between MOD16 and ECOSTRESS is r = 0.17. A product validated only on
   domain-mean bias will look fine and still be useless for a heterogeneity hypothesis.
4. **MOD16 exceeds reference ET at M1 by 34 %**, above the FAO-56 mid-season Kc ceiling
   for maize, while running 15 % low at the mixed S1 pixel - the wrong way round if
   cropland fraction were the control.

Caveat on the ECOSTRESS comparison: the 2024-07-23 granule used sits at **15.5 h local
solar time**, outside the 9-15 h usable window below, so its -1.2 mm day-1 mean offset
against MOD16 is partly late-afternoon daily-upscaling bias and must not be quoted as a
product bias. The r = 0.17 spatial disagreement and the within-pixel spread are not
affected by a scene-level scale error.


# DERECHOS domain ET data sources - operational guidance

Domain box: 40.4-42.7 N, 94.6-87.0 W. Core sites S1 (Muscatine Island Research Farm,
41.356, -91.136, ISUSM station FRUI4) and M1 (SERF Crawfordsville, 41.1933, -91.4839,
ISUSM CRFI4). All statements below were measured live on 2026-09-25/26 from a
network-sandboxed environment with NASA Earthdata and ARM Live credentials but no
OpenET, CDS, Planet or NASS key.

## Decision rule: which product for which job

- Need 30 m field-scale ET with an ensemble spread you can quote as uncertainty ->
  OpenET (requires a free key). Second choice ECOSTRESS ECO_L3T_JET, which is also an
  ensemble but is temporally sparse and irregular.
- Need a gap-free daily or hourly field -> NLDAS-2 Noah. It is the only source here that
  is complete in space and time over 1979-present, and the only one carrying the ET
  partition (TVeg / ESoil / ECanop) and canopy-conductance diagnostics.
- Need thermal and reflectance to run your own energy balance -> Landsat C2 L2 through
  Microsoft Planetary Computer (anonymous), not through USGS.
- Need a zero-credential independent check -> SSEBop CONUS monthly from USGS EROS.
- Need the reference-ET denominator -> gridMET pet (grass) / etr (alfalfa) from
  northwestknowledge.net, and IEM ISUSM `et` at the two core sites.
- Need near-real-time for IOP support -> HRRR surface LHTFL/SHTFL only; everything else
  lags weeks to a year.

## Auth map

- NASA Earthdata bearer token (env NASAEDTOKEN) works directly against
  data.lpdaac.earthdatacloud.nasa.gov, hydro1.gesdisc.eosdis.nasa.gov,
  data.nsidc.earthdatacloud.nasa.gov and opendap.earthdata.nasa.gov. Pattern for DAAC
  downloads: GET with `allow_redirects=False`, read `Location`, then fetch the presigned
  CloudFront URL WITHOUT the Authorization header.
- AppEEARS is the exception: `POST /api/login` needs HTTP basic with the Earthdata
  PASSWORD. A bearer token returns 401. Its `/api/product`, `/api/product/<id>` and
  `/api/quality/<id>` are fully public.
- ARM Live takes a single `user=USER:TOKEN` query parameter (ARMUSER, ARMTOKEN).
- Planetary Computer, USGS EROS FEWS, LandsatLook search, gridMET, IEM and CMR need no
  credential at all.
- OpenET needs an API key in a bare `Authorization` header (not `Bearer`). AmeriFlux bulk
  download needs a registered account user_id plus email.

## Network hosts that must be allowlisted

openet-api.org, hydro1.gesdisc.eosdis.nasa.gov, edcintl.cr.usgs.gov,
landsatlook.usgs.gov, amfcdn.lbl.gov, data.nsidc.earthdatacloud.nasa.gov,
opendap.earthdata.nasa.gov, modiseuwest.blob.core.windows.net,
landsateuwest.blob.core.windows.net, www.northwestknowledge.net, and (from earlier work)
d1nklfio7vscoe.cloudfront.net for LP DAAC presigned downloads.
n5eil01u.ecs.nsidc.org is dead even once granted - do not request it.
www.gleam.eu and cds.climate.copernicus.eu were never granted and remain untested.

## Source-by-source operational notes

### OpenET (openet-api.org, API v3.2)
Public `/openapi.json` (35.6 kB) documents 20 paths. Request models: Point, Polygon,
Multipolygon, Stack_Export, Metadata. Required Point fields: date_range, interval,
geometry [lon, lat], model, variable, reference_et, file_format; defaults version=2.1,
units='mm'. `/raster/export/stack` is the domain-map endpoint (adds resample, cog,
drive_folder). The spec declares no enums, so read valid model/variable strings from the
OpenET docs, not from the spec. Auth scheme is `APIKeyHeader` named `Authorization`.
NO key -> 403 {"detail":"Not authenticated"}. INVALID key -> HTTP 500 Internal Server
Error. That asymmetry is the single most useful debugging fact: if you see 500, suspect
the key, not the server. Coverage: OpenET launched in 2021 with 17 western states, went
to 23 in 2023, and only reached all 48 contiguous states in December 2025, with data
back to 2016. Any documentation describing OpenET as "western US" predates the DERECHOS
domain being covered. Field-boundary (polygon) products for the eastern half were
scheduled for early 2026 - verify before relying on them.

### ECOSTRESS ECO_L3T_JET v002
The richest single product for this campaign: a 70 m ET ensemble. Per-granule assets are
ETdaily, ETinstUncertainty, PTJPLSMinst, PTJPLSMcanopy, PTJPLSMsoil, PTJPLSMinterception,
STICinst, STICcanopy, BESSinst, MOD16inst, cloud, water. 28,233 granules over the domain
box since 2018-07-29; newest 2026-09-15, so the instrument is still producing and will
plausibly be flying during the 2027-2029 deployment. Tiles are MGRS in the local UTM zone
(15TXF -> EPSG:32615, 16TBK -> EPSG:32616), 1568x1568 at 70 m, float32, nodata NaN.

Three measured traps:
1. ISS precession means overpass local solar time is uncontrolled. Over tile 15TXF for
   June-August 2024, 16 granules spanned LST 5.2 h to 17.9 h; only 7 fell in 9-15 LST.
2. A nighttime granule is nearly fully valid and nearly all zero. The 05:13 LST granule
   was 99.9% valid with median ETdaily 0.00 mm/day. Averaging granules without an LST
   filter pulls the domain mean toward zero silently.
3. Valid fraction is unrelated to file success. The 2024-07-31 midday granule downloads
   as a clean 19 kB GeoTIFF containing 161 valid pixels out of 2,458,624 (0.007%). Mean
   valid fraction across the 16 granules was 28.6%; only 8 exceeded 10%; only 2 were both
   daytime and >10% valid.
Screening rule: keep granules with LST in [9, 15] AND valid fraction above 10%, and
expect roughly 2 per tile per summer month before cloud screening.
CMR bounding-box matching also returns tiles that merely graze the domain - a domain-wide
query's first hit was 16TBK, spanning 39.6-40.6 N, almost entirely south of the box.
ECO_L3T_ET_ALEXI v002 (disALEXI, 24-hour, CONUS) has 10,308 granules but its newest is
2026-02-05 against JET's 2026-09-15; treat disALEXI production as possibly stalled.

### NLDAS-2 Noah (NLDAS_NOAH0125_H.2.0)
Files are netCDF4, not GRIB, at
hydro1.gesdisc.eosdis.nasa.gov/data/NLDAS/NLDAS_NOAH0125_H.2.0/<YYYY>/<DOY>/. 7.35 MB per
hour, 4.8 s each; a whole day is 169 MB in 206 s. The directory index itself requires the
bearer token. 54 variables; domain subset is 19x61 cells at 0.125 deg. Evap is
kg m-2 per hour, so summing 24 files gives mm/day directly. Measured 2024-07-31 domain
mean: 4.20 mm/day (p5-p95 1.35-5.12), day-mean Qle 127 W m-2, 18Z Qle 375 W m-2, and a
partition of TVeg 79% / ECanop 17% / ESoil 4%. Structural caveat: Noah's GVEG and LAI are
a MODIS climatology, so NLDAS cannot express interannual crop variability or a cover-crop
signal. Use it as a spatially complete backbone, never as an arbiter of vegetation
control.

### MOD16A2GF / MOD16A3GF
Two routes. OPeNDAP at opendap.earthdata.nasa.gov gives cheap spatial subsets but needs
the DAP4 group path `/MOD_Grid_MOD16A2/Data_Fields/ET_500m` - a bare `/ET_500m`
constraint expression returns Hyrax 400 "referenced a variable that was not found".
A 301x301 block of ET+PET+QC came back as 238 kB in 4.2 s. Planetary Computer collection
`modis-16A3GF-061` serves the annual product as COGs; sign with
`/api/sas/v1/sign?href=...` (manually appending the `/api/sas/v1/token/<coll>` string
produced 403).
THE FILL TRAP: ET_500m carries valid_range [-32767, 32700] and NO _FillValue. xarray
scales 32767 to 3276.7 and includes it everywhere. Measured: naive 8-day mean 55.5 mm/day
vs 3.60 mm/day masked (87.2% valid); naive annual 1279 mm/yr vs 606 mm/yr median masked
(88.5% valid). Always mask on valid_range.
SECOND TRAP: the PC `modis-16A3GF-061` collection mixes Terra (MOD) and Aqua (MYD)
granules - a 2022 domain query returned two of each. Filter on the id prefix.
LATENCY: the gap-filled products lag about a year (MOD16A2GF newest 2025-12-27;
MOD16A3GF newest 2025-01-01). Use MOD16A2.061 (newest 2026-09-06, about three weeks) for
recent dates. VNP16A2 returns zero CMR hits - that short name does not exist.

### Landsat Collection 2 Level-2
Use Planetary Computer collection `landsat-c2-l2`. Assets lwir11, atran, emis, red,
nir08, qa_pixel. A 418x579 windowed read of lwir11 took 2.4 s. Scale to kelvin with
DN*0.00341802 + 149.0; DN 0 is fill. Ten scenes with cloud<15% over the S1 box for
June-September 2024; mean ST at S1 on 2024-09-09 was 28.4 C. The USGS LandsatLook STAC
(landsatlook.usgs.gov/stac-server) is excellent for discovery - 14 collections including
landsat-c2l2-st and the ARD variants, 22 ST scenes over S1 for July-August 2024 - but its
https asset hrefs 302 to ers.cr.usgs.gov (interactive login) and the s3://usgs-landsat
alternate is requester-pays. Discover on USGS, read pixels on Planetary Computer.

### SSEBop (USGS EROS FEWS NET)
CONUS monthly at
edcintl.cr.usgs.gov/downloads/sciweb1/shared/uswem/web/conus/eta/modis_eta/monthly/downloads/
- 640 files, m<YYYYMM>.zip = actual ET, ma<YYYYMM>.zip = anomaly, 2000-01 to 2026-08,
about one month of latency, no credentials. m202407.zip is 10.9 MB in 9.8 s and contains
one GeoTIFF. The directory index is plain HTML; regex the hrefs. Only the exact monthly
path works: the annual/downloads sibling 404s and the edcintl root is 403. A global
monthly sibling exists under .../fews/web/global/monthly/eta/downloads/ (222 files).

### SMAP L4
SPL4SMGP.008 via OPeNDAP, group `/Geophysical_Data`, variables heat_flux_latent,
heat_flux_sensible, land_evapotranspiration_flux, sm_surface, sm_rootzone. A DAP4
constraint with no index range returns the WHOLE global 1624x3856 EASE2 grid - 24 MB in
6.2 s for five variables. Add [y0:y1][x0:x1]. The domain holds 1,944 9 km cells.
land_evapotranspiration_flux is kg m-2 s-1: 1.05e-4 -> 9.04 mm/day at 22:30 UTC, matching
heat_flux_latent 258 W m-2. SPL4CMDL.008 carries carbon, not LE.

### HRRR
Herbie with priority=["aws"], model='hrrr', product='sfc'. Search string
":(LHTFL|SHTFL|GFLUX|VEG):surface:anl:" pulls four fields by byte range in 6.5 s instead
of a 130 MB GRIB2. cfgrib renames them: LHTFL->slhtf, SHTFL->ishf, GFLUX->gflux,
VEG->veg. 18,028 domain cells at 3 km; longitudes are 0-360. At 18Z 2024-07-31 HRRR
LHTFL was 216 W m-2 against NLDAS-2 Qle 375 W m-2 - a factor of 1.7 between the two
candidate forcings at the same timestamp, which is a result in its own right.

### gridMET
https://www.northwestknowledge.net/metdata/data/. NAMING TRAP: grass reference ET is
pet_<YYYY>.nc, NOT eto_<YYYY>.nc, which 404s; alfalfa is etr_<YYYY>.nc. pet_2024.nc is
70.3 MB (49.7 s), etr_2024.nc 93.1 MB. The internal variable is
potential_evapotranspiration; latitude DESCENDS so use sel(lat=slice(42.7, 40.4)). The
server honours byte ranges, so /vsicurl or h5netcdf range reads avoid the full download
and the thredds host is unnecessary. 10,248 domain cells; 2024-07-31 domain mean ETo
4.61 mm/day.
DO NOT use the Planetary Computer `gridmet` Zarr mirror: it opens cleanly and stops at
2020-12-31. Same for PC `terraclimate` (ends 2021-12). Both silently return nothing for
campaign years.

### AmeriFlux
amfcdata.lbl.gov and ameriflux-data.lbl.gov still fail, but **amfcdn.lbl.gov works**.
Three endpoints: /api/v1/site_display/AmeriFlux (844 sites, 299 kB),
/api/v1/site_availability/AmeriFlux (policy tiers per product), and the far richer
/api/v2/site_info_display/AmeriFlux (1.69 MB, wrapped in a top-level "values" key).
The v2 record carries base_variables (test `"LE" in ...` directly), grp_publish_base (the
exact published BASE years), publish_ameriflux_policy (CCBY4.0 vs LEGACY), status, the
AmeriFlux and FLUXNET DOIs, and planting/harvest dates in grp_igbp.igbp_comment.
FILTER TRAP: country is "USA" and state is a two-letter code; matching "United States" or
"Iowa" silently returns an empty frame.
Bulk data: POST https://amfcdn.lbl.gov/api/v2/data_download. An empty body returns 422
naming exactly user_id, user_email, data_policy, data_product as required;
agree_policy is client-side only and the server rejects it as an unknown field. Do not
call it without a real registered account - downloads are logged against a user id.

Inventory result for the campaign: 21 AmeriFlux sites inside the domain box, 68 candidates
including all cropland (CRO) sites in IA/IL/MN/NE/MO/WI/IN, 54 of them with LE in BASE.
US-AMS is ATMOS (GRA, CC-BY-4.0, BASE 2022-2023); US-CU1 is the downtown-Chicago UIC
tower (URB, CC-BY-4.0, BASE 2024); US-CU2, US-CU3 and US-CU4 are registered with no
published BASE years yet. Longest cropland record in the box is US-IB1 (Fermilab Batavia,
2005-2018, 14 years); the active cluster is US-IAB/IAC/IAM at Iowa State (2019-2024,
CC-BY-4.0). CRITICAL GEOGRAPHIC FACT: the nearest in-box cropland tower is 224 km from
S1 and the nearest tower of any kind is 181 km. Every in-box tower is at the Ames end or
the Chicago end; the middle of the gradient, where S1 and M1 sit, has none.

### ARM SGP flux
DATASTREAM NAME TRAP: the ECOR b1 stream is `sgpecorsfE33.b1` (with "sf"), not
`sgpecorE33.b1` - the latter returns status "success" with zero files and no error.
Active ECOR facilities E33, E37, E39 (2019-10-22 to 2026-09-24); a day is 87.6 kB in
0.7 s. SEBS `sgpsebs<FAC>.b1` is active at E12, E14, E32, E33, E37, E39. EBBR
`sgp{5,15,30}ebbr<FAC>.b1` ran 1993-07-06 to 2024-12-10 and is RETIRED - E12 and E32
ended 2024-12-05/10 and SEBS started there 2024-12-09/11. Any "SGP training analogue"
built on EBBR is historical, not concurrent with 2027-2029.
Datastream coverage is best enumerated from the ARM instrument catalogue:
POST https://www.arm.gov/api/es/ds/_search with {"size": 800, "query": {"match_all": {}}}
returns 742 instrument classes, each with locations[].datastreams[] carrying
datastream, start_date, end_date and facility lat/lon. Filtering by
instrument_class_code fails (0 hits); pull all 742 and filter client-side.

### IEM ISUSM
ENDPOINT CORRECTION: /agclimate/isusm.py returns a PNG plot for data parameters. The data
endpoint is https://mesonet.agron.iastate.edu/cgi-bin/request/isusm.py with
mode=daily&format=comma&tz=UTC and RFC-3339 Z-suffixed sts/ets. A full 2024 at FRUI4 and
CRFI4 is 732 rows, 119 kB, no gaps and no -99 sentinels in the `et` column. `et` is in
INCHES per day. JJA 2024 means: FRUI4 (S1) 5.02 mm/day, CRFI4 (M1) 4.82 mm/day; annual
maxima 11.2-11.4 mm/day. Those maxima are reference-ET magnitude, so treat `et` as a
reference/potential ET diagnostic - it is NOT an eddy-covariance constraint and must not
be used to validate actual ET. It is still the best decade-plus daily atmospheric-demand
record at the exact core-site coordinates.

## Cross-product consistency, 2024-07-31, domain mean
NLDAS-2 Noah 24 h sum 4.20 mm/day; ECOSTRESS ETdaily 3.85; MOD16A2GF (8-day/8, DOY 177)
3.60; gridMET ETo 4.61; ISUSM reference ET 4.28 (S1) and 3.51 (M1). Daily totals agree to
about 15% across three independent actual-ET products. Instantaneous fluxes do not: at
18Z, NLDAS Qle 375 vs HRRR LHTFL 216 W m-2; SMAP L4 258 W m-2 at 22:30Z; ECOSTRESS
PT-JPL-SM 346 W m-2 with a quoted 1-sigma of 240 W m-2 (70% of the retrieval).
Implication: build the product at daily or 8-day aggregation, use ARM eddy covariance to
constrain the diurnal shape rather than the daily total, and carry ECOSTRESS's own
per-pixel uncertainty forward - it exceeds the entire inter-product spread.
