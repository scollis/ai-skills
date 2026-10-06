---
name: mrms-hourly-conus
description: Access the NOAA MRMS CONUS hourly analysis as analysis-ready Zarr - the dynamical.org Icechunk store on AWS Open Data, 2014-11-01 to present, hourly, 0.01 degree (~1 km) over the contiguous US. Gauge-corrected and radar-only quantitative precipitation estimates (QPE), a categorical precipitation type flag, and the FLASH QPE-to-flash-flood-guidance ratio. Load for MRMS, MultiSensor QPE, RadarOnly or GaugeCorr QPE, PrecipFlag or precipitation type, radar-derived rainfall accumulation, flash flood guidance, gridded US precipitation climatology, or when you need precipitation coverage that is spatially uniform rather than following gauges and human storm reports. Covers anonymous Icechunk access, per-variable availability boundaries, chunk-aware subsetting for point series versus spatial boxes, kg m-2 s-1 unit conversion, the descending-latitude gotcha, and why the precipitation-type flag cannot represent freezing rain or ice pellets.
---

# MRMS CONUS hourly analysis (dynamical.org Icechunk store)

Analysis-ready hourly MRMS over the CONUS, repackaged by dynamical.org from NOAA
NODD/NCEP and Iowa Mesonet archives. Anonymous access, no credentials.

**Everything below was verified against the live store on 2026-09-01.**

## Facts

| | |
|---|---|
| Store | `s3://dynamical-noaa-mrms/noaa-mrms-conus-analysis-hourly/v0.3.0.icechunk` (us-west-2) |
| Time | 2014-11-01 00:00 UTC to present, hourly (103,750 steps as of 2026-09-01 21:00) |
| Grid | 3500 lat x 7000 lon, 0.01 deg (~1 km); lat 54.995 -> 20.005, lon -129.995 -> -60.005 |
| Chunks / shards | `(648, 100, 100)` / `(648, 700, 1400)` |
| Licence | CC BY 4.0 |
| Citation | "NOAA NWS NCEP MRMS data processed by dynamical.org from NOAA NCEP, NOAA Open Data Dissemination and Iowa Mesonet archives" |

## Opening it

`icechunk >= 2` is required (the store is Icechunk **v2** format) and that wheel needs
**Python >= 3.12**. On Python 3.11 you get `icechunk 1.1.21`, which fails with
"this repository uses Icechunk v2 format, please upgrade the icechunk library". Use a
3.12+ environment.

```python
ds = mrms_open()          # anonymous S3, read-only session on "main"
```

Equivalent by hand:

```python
import icechunk, xarray as xr
storage = icechunk.s3_storage(bucket="dynamical-noaa-mrms",
                              prefix="noaa-mrms-conus-analysis-hourly/v0.3.0.icechunk",
                              region="us-west-2", anonymous=True)
repo = icechunk.Repository.open(storage)
ds = xr.open_zarr(repo.readonly_session("main").store, chunks=None, consolidated=False)
```

There is also a `dynamical_catalog.open("noaa-mrms-conus-analysis-hourly")` convenience
path (`dynamical-catalog >= 0.8.0`, also Python >= 3.12). It resolves the store through
`stac.dynamical.org`, so it needs that host reachable as well as the bucket; the direct
call above needs only the bucket. Version 0.3.0 of that client does **not** work - it
raises `STAC Collection noaa-gfs-analysis is missing a 'zarr' asset` on an unrelated
collection while walking the catalog.

## Variables and availability

Not everything reaches back to 2014. Verified by reading both sides of the boundary:

| Variable | Meaning | Available |
|---|---|---|
| `categorical_precipitation_type_surface` | Precipitation type flag | 2014-11-01 onward |
| `precipitation_surface` | Blended hourly QPE rate | 2014-11-01 onward, **source switches 2020-10-15** |
| `precipitation_radar_only_surface` | Radar-only QPE rate, no gauge correction | 2014-11-01 onward |
| `precipitation_pass_1_surface` | MultiSensor Pass 1 (low latency, fewer gauges) | 2020-10-15 onward, NaN before |
| `precipitation_pass_2_surface` | MultiSensor Pass 2 (higher latency, more gauges) | 2020-10-15 onward, NaN before |
| `flash_qpe_ffg_max_surface` | Max QPE-to-flash-flood-guidance percentage | 2020-10 onward, NaN before |

`mrms_availability()` returns this table.

## Verified coverage: the record does not really begin in 2014

The time axis starts 2014-11-01, and the catalog says so - but that is a statement about
the coordinate, not about data existing. Measured at two Iowa grid points over the whole
record (103 753 hours each), the fraction of hours with a finite value is:

| Period | Valid hours |
|---|---|
| 2014-11 | 10 % |
| 2014-12 | 4 % |
| 2015-01 | 7 % |
| 2015-02 | 42 % |
| **2015-03 onward** | **99.93 %** |

By year: 2014 is 7 % valid, 2015 is 87 % (dragged down by Jan-Feb), and every year from
2016 is >= 99.9 %. In November-December 2014 the valid hours are scattered singletons -
1 to 11 hours on 22 separate days - and the first day with >= 20 valid hours anywhere in
the first four months is 2015-02-01.

**The gap is CONUS-wide, not regional.** Spot-checking single hours: 2014-12-15 18Z has
9 % of CONUS cells valid, 2015-01-15 18Z has 7 %, and 2015-03-15 18Z has 90 % (the
residual 10 % being outside radar coverage, as expected). So this is an ingest gap in the
archive rather than a local radar outage, and it will look the same wherever you sample.

**Practical rule: treat the usable record as starting 2015-03-01** (~11.5 years), and if
you need earlier data, verify coverage in your own domain first rather than trusting the
time axis. Anything computed over 2014-11 to 2015-02 - a trend fit, a climatological
mean, a monthly total - is being computed on a few per cent of the hours and will be
wrong without warning, because the missing hours are NaN rather than absent rows.

Post-2015-03 the only months below 99 % at these points are 2015-04 (98.9 %),
2015-08 (98.1 %) and 2020-10 (98.5 %); everything else is essentially complete.

One corollary worth stating: coverage gaps in this store are **not** diurnally biased once
the record is established. Over 94 942 hours in 2015-2025 the count of valid hours per UTC
hour-of-day varies by 0.7 % (max/min = 1.007), so diurnal-cycle work is safe - but check
this yourself if you include the sparse early months, where it is not true.

**The `precipitation_surface` discontinuity matters.** It is MultiSensor Pass 2 from
2020-10-15 and GaugeCorr QPE before, falling back to Pass 1 then radar-only when the
primary is missing. That is a change of instrument mid-record, so it will corrupt a
naive trend fit or a return-period estimate spanning 2020. Either restrict to one side
of the boundary or use `precipitation_radar_only_surface`, which is homogeneous across
the whole record (at the cost of no gauge correction).

Radar-only and precipitation-type variables are NaN beyond US radar range; the Pass
variables extend further offshore but are NaN in the southeast corner over the Atlantic.
Early hours in the record contain NaNs where source data is missing.

## Precipitation type - read this before using it

```python
mrms_ptype_labels(da.values)   # codes present -> labels
mrms_ptype_counts(da)          # labelled histogram
```

| Code | Meaning |
|---|---|
| -3 | no coverage |
| 0 | no precipitation |
| 1 | warm stratiform rain |
| 3 | snow |
| 6 | convective rain |
| 7 | rain mixed with hail |
| 10 | cold stratiform rain |
| 91 / 96 | tropical stratiform / convective rain mix |

**There is no freezing-rain category and no ice-pellet category.** This is inherent to
MRMS PrecipFlag, not a packaging choice: freezing rain freezes on contact with the
surface, so the radar aloft sees liquid and the flag reports rain.

Demonstrated: on 22 February 2023, a well-observed freezing-rain day in eastern Iowa,
the flag at 41.356 N, 91.136 W reports only code 10 (cold stratiform rain, 9 hours),
code 3 (snow, 1 hour) and code 0. Across the whole 2020-11 to 2021-03 cold season at
that point, the only codes that ever appear are 0, 1, 3 and 10.

So this field can verify a **snow-versus-rain** call across a whole domain, including
the gaps between airports, and is **structurally blind** to freezing rain versus rain.
For that distinction use mPING reports or ASOS present-weather sensors. Do not present
an MRMS-based winter-precipitation climatology as covering freezing rain.

Code 7 ("rain mixed with hail") is a coarse convective indicator, not a hail-size
product. **This store carries no MESH**, so it cannot give a population-bias-free hail
climatology; for hail size use MRMS MESH from another source, or storm reports.

## Reading efficiently

Chunks are `(648, 100, 100)`: 648 hours deep, 100 x 100 cells wide. The store is built
for **time series at points and small boxes**, not for single-timestep CONUS maps.

Measured on a warm cache:

| Read | Cost |
|---|---|
| Point, 25 hours | 1.1 s |
| Point, full 5-month cold season (3,624 hours) | 2.0 s |
| Box 220 x 290 cells, 12 hours | 9.8 s |

A point time series is nearly free regardless of length, because one chunk already
holds 27 days. A spatial box is expensive *per unit time* because every chunk it
touches drags in 648 hours whether you want them or not. Pull long series at points
cheaply; keep box reads to short windows.

```python
ds  = mrms_open()
ts  = mrms_point(ds, 41.356, -91.136, "precipitation_surface", "2023-02-22", "2023-02-23")
box = mrms_box(ds, 41.356, -91.136, radius_km=120, var="categorical_precipitation_type_surface",
               start="2023-02-22T12", end="2023-02-22T23")
```

**Latitude is stored descending** (54.995 -> 20.005), so a `.sel(latitude=slice(...))`
must run high to low or it returns an empty array. `mrms_box` handles this.

## Units

Every precipitation variable is a **rate in `kg m-2 s-1`**, numerically equal to mm/s.

```python
mrms_mm_per_hour(da)     # -> mm/h
mrms_accumulate_mm(da)   # -> total mm over the time axis
```

Forgetting the 3600 factor is the easiest way to be wrong by three orders of magnitude.

## When to reach for this

Good for: gridded precipitation over a region with uniform coverage; storm-total
accumulation; snow-versus-rain discrimination; flash-flood context; anything where
gauge networks or human storm reports are too sparse or too population-biased.

Not for: hail size (no MESH), freezing rain or ice pellets (no category), sub-hourly
timing (hourly only), pre-2014 climatology, anything outside CONUS radar coverage.
