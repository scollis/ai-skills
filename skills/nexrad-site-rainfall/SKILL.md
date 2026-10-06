---
name: nexrad-site-rainfall
description: "Detect and quantify rainfall events over a fixed ground site (e.g. an ARM deployment) from NEXRAD Level II radar using Py-ART. Use when the task is to survey a WSR-88D radar over weeks-to-months for rain over specific coordinates, convert reflectivity to rain rate via Marshall-Palmer Z-R, tabulate events (timing, peak dBZ, accumulation), or render colorblind-safe PPI reflectivity / rain-rate maps centered on a site. Triggers: NEXRAD, Level II, WSR-88D, Py-ART, KIWA, ARM site rainfall, radar rain rate, Z-R, reflectivity map, ChaseSpectral."
---

# NEXRAD site-rainfall analysis

Two-pass workflow to find and quantify rain over a fixed point from a NEXRAD
radar, without downloading the whole (tens-of-GB) archive. Helpers are loaded
into the kernel from `kernel.py`.

## Environment

Needs `arm_pyart, boto3, numpy, pandas, cartopy, cmweather` (and `netcdf4`,
`scipy`). Create a dedicated env, e.g.
`manage_environments(mode="create", name="radar", packages=["arm_pyart","boto3","cartopy","netcdf4","scipy","cmweather"], channels=["conda-forge"])`.

Data is streamed anonymously from the **`unidata-nexrad-level2`** S3 bucket
(LIST + GET both work UNSIGNED; the NOAA `noaa-nexrad-level2` bucket denies
anonymous LIST). Grant network access to
`unidata-nexrad-level2.s3.amazonaws.com` and `naturalearth.s3.amazonaws.com`
(cartopy shapefiles) when prompted.

## Site geometry & caveats (always state these)

- These are **radar Z-R estimates, not gauge-calibrated** rainfall.
- At long range the 0.5° beam is elevated (e.g. ~1 km AGL at 57 km); low-level
  growth/evaporation below the beam is not captured. Hail inflates high dBZ.
- Report **both** disk-mean accumulation (averaged over the analysis disk) and
  **conditional** (point-like) accumulation = disk-mean / rainy-fraction; the
  latter approximates a gauge directly under the cell.

## One-call pipeline

For a standard run, `run_site_rainfall()` chains the whole workflow below and
returns a dict `{events, survey, drilldown, catalog, figures, totals}`, writing
`scan_catalog.csv`, `survey_timeseries.csv`, `event_timeseries.csv`,
`rainfall_events.csv`, and `event_E##_ppi.png` maps to `outdir`:

```python
import cartopy; cartopy.config['data_dir'] = "cartopy_data"
res = run_site_rainfall("KIWA", 33.608, -112.153,
                        "2026-06-16 20:00", "2026-06-17 04:00",
                        outdir="run1", survey_every_h=1, workers=14)
print(res["events"])      # per-event table
print(res["totals"])      # n_events, n_significant, total accum (mm)
```

Key params: `radius_km=10` (analysis disk), `detect_dbz=35` (event threshold),
`event_gap_h=2` (merge scans <2 h apart into one event), `accum_gap_min=20`
(skip time-integration across gaps > this), `survey_every_h=1` (coarse-pass
cadence), `workers` (threads), `make_maps=True`. For long windows (months),
the coarse survey runs first and only event days are drilled to full
resolution, so cost scales with rain, not with archive size. The steps below
document what each stage does and how to run them manually.

## Workflow

1. **Catalog** — `keys = list_scan_keys("KIWA", start, end)` → list of
   `{key, timestamp}`. Save as CSV. Cadence (~100-300 scans/day) rises in
   precipitation-mode VCPs — a scans-per-day bar chart already flags storm days.
2. **Coarse survey** — subsample ~1 scan/hour; for each,
   `extract_site_stats(path, site_lat, site_lon, radius_km=10)` after
   downloading with `nexrad_s3_client()`. Download → read → **delete** each
   file; checkpoint results to CSV. Use `ThreadPoolExecutor` (the sandbox
   blocks `ProcessPoolExecutor` semaphores), ~12-16 workers.
3. **Detect events** — group hours with `max_dbz`/`mean_rr` above background
   into candidate windows.
4. **Drill-down** — re-process every scan (not just hourly) on event days for
   full-resolution rain-rate series.
5. **Accumulate** — trapezoidally integrate `mean_rr` in time (skip gaps
   >20 min) for disk-mean mm; divide by rainy-fraction for conditional mm.
6. **Maps** — find each event's peak scan; render
   `ppi_map(path, out, site_lat, site_lon, event_id=..., when=..., metrics=...)`
   and, for the largest event, `rainrate_map(...)`. Both default to the
   colorblind-safe **ChaseSpectral** colormap (cmweather).

## QC (baked into the helpers)

Lowest sweep only; Py-ART `GateFilter` excludes transition gates, invalid
reflectivity, cross-correlation ratio < 0.85 (clutter/biology), and
reflectivity < 5 dBZ. Analysis disk = `radius_km` around the site;
"rainy" gate = >= 20 dBZ.

## Key functions (from kernel.py)

- `nexrad_s3_client()` — UNSIGNED boto3 client for the Unidata bucket.
- `list_scan_keys(radar_id, start, end, client=None)` — enumerate Level II keys.
- `zr_rate(dbz, a=200, b=1.6)` — Marshall-Palmer rain rate (mm/hr).
- `extract_site_stats(path, site_lat, site_lon, radius_km=10, rainy_dbz=20)` —
  per-scan QC + disk stats (`max_dbz, p95_dbz, rainy_frac, mean_rr, ngate`).
- `ppi_map(...)` / `rainrate_map(...)` — ChaseSpectral PPI maps centered on the
  radar with site marker, dashed analysis disk, and range rings.

Cartopy note: before rendering maps set a writable cache —
`import cartopy; cartopy.config['data_dir']="cartopy_data"`. In some builds the
NWS colormap is registered as `'NWSRef'` (not `'pyart_NWSRef'`); this skill uses
ChaseSpectral to avoid that and for colorblind safety.
