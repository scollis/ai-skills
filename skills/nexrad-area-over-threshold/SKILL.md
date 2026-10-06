---
name: nexrad-area-over-threshold
description: "Compute the AREA (km^2) of a radar domain exceeding rain-rate intensity thresholds from NEXRAD Level II data with Py-ART, using a Marshall-Palmer Z-R relation. Use to measure storm COVERAGE and organization over time (not point intensity): area over imperial rainfall bins (0.25/0.5/1/2/3 in/hr), area-over-threshold time series, stacked intensity-band partition, and a discrete intensity-band map at the peak-coverage timestep. Complements point/site rain-rate analyses. Pairs with nexrad-radar-gcs for data access and georeferenced PPI plotting. Ships kernel.py helpers: area_over_thresholds, sweep_rain_rate_capped, rainfall_band_cmap. Triggers: NEXRAD, Py-ART, Marshall-Palmer, Z-R, rain rate, area over threshold, areal coverage, in/hr, mm/hr, intensity bands, hail cap, WSR-88D."
---

# NEXRAD area-over-threshold rainfall

Measure the **area of a radar domain** whose rain rate exceeds each of a set of
intensity thresholds, volume by volume. Where a point/site series answers *how
hard is it raining here*, this answers *how much of the domain is under heavy
rain, and how is that coverage organized* — the two peak at different times in a
multi-round event.

## Method

For each Level II volume, on the base (0.5 deg) sweep:

1. **Z -> R** with Marshall-Palmer `Z = zr_a * R**zr_b` (default 200, 1.6).
2. **Dual-pol QC**: keep gates with rhoHV >= `rhohv_min` (0.85) and
   Z >= `dbz_min` (5 dBZ) — removes non-meteorological echo.
3. **Hail cap**: clip reflectivity at `hail_cap` (53 dBZ) before the Z->R
   inversion so hail cores do not inflate rainfall. Both capped and uncapped
   areas are returned. A 53 dBZ cap limits M-P rain rate to ~75 mm/hr, just
   below the 3 in/hr = 76.2 mm/hr bin, so the capped >=3 in/hr area is zero by
   construction — that bin is diagnostic of hail contamination (compare
   `area_raw_3.0` vs `area_cap_3.0`).
4. **Polar-geometry area**: each gate cell area is `dr * (r * dphi)` (range-gate
   depth x arc length). These cells tile the sweep without overlap, so summing
   the areas of gates above a threshold inside the lon/lat `extent` gives the
   true covered area — no Cartesian regridding or interpolation.

Thresholds default to the imperial rainfall bins **0.25, 0.5, 1, 2, 3 in/hr**
(6.35, 12.7, 25.4, 50.8, 76.2 mm/hr).

## Helpers (kernel.py, auto-loaded)

- `area_over_thresholds(radar, extent, thresholds_in=None, rhohv_min=0.85, dbz_min=5.0, hail_cap=53.0, zr_a=200.0, zr_b=1.6)`
  -> dict with `area_cap_<t>` / `area_raw_<t>` (km^2) per threshold and
  `domain_area_km2` (total raining area). Keys use `str(t)`, e.g.
  `area_cap_1.0`. `extent = [lon_min, lon_max, lat_min, lat_max]`.
- `sweep_rain_rate_capped(radar, ...)` -> `(gate_lon, gate_lat, rain_rate)` for
  the base sweep (hail-capped, QC-masked) — pcolormesh straight onto a
  georeferenced axes.
- `rainfall_band_cmap(edges_in=None)` -> `(cmap, norm, edges_mm)`, a discrete
  colormap + BoundaryNorm for imperial intensity bands (below the first edge is
  transparent). Default edges `[0.1, 0.25, 0.5, 1, 2, 3]` in/hr.
- Module constants `RAIN_THRESHOLDS_IN`, `MM_PER_IN`.

## Workflow

1. **Get data + a georeferenced axes** from the `nexrad-radar-gcs` skill
   (`nexrad_gcs_keys`, `download_nexrad`, `read_radar_safe`, `make_radar_geoaxes`,
   `add_context_features`, `setup_cmweather`). This skill assumes those are
   available; load `nexrad-radar-gcs` alongside it.
2. **Sweep the engine** over every volume, collecting one row per scan into a
   DataFrame; save a CSV.

   ```python
   rows = []
   for p in volume_paths:                      # from nexrad-radar-gcs
       r = read_radar_safe(p)
       if r is None: continue
       a = area_over_thresholds(r, extent)
       a["time_utc"] = scan_time(p)
       rows.append(a)
       del r
   adf = pd.DataFrame(rows).sort_values("time_utc")
   ```
3. **Time series**: plot `area_cap_<t>` for each threshold vs time — nesting
   curves show coverage of each intensity growing/shrinking through the event.
4. **Stacked bands**: difference the cumulative areas
   (`area_cap_0.25 - area_cap_0.5`, ...) and `stackplot` them to partition the
   raining area by intensity through time.
5. **Peak-coverage map**: at `adf.area_cap_1.0.idxmax()`, read that volume, call
   `sweep_rain_rate_capped` + `rainfall_band_cmap`, and pcolormesh the discrete
   intensity bands over the basemap (`transform=PlateCarree`).

## Notes

- Use the **capped** areas as the defensible rainfall product; carry uncapped
  alongside to flag hail.
- Georeference via Py-ART gate lon/lat on a Mercator GeoAxes with
  `transform=PlateCarree()` (from `nexrad-radar-gcs`) — never a radar-centered
  azimuthal-equidistant axes.
- Reflectivity maps use cmweather `ChaseSpectral`; rainfall-band maps use the
  discrete `rainfall_band_cmap`.
- `extent` should be well inside the ~230 km unambiguous range of the base
  sweep so gate coverage is complete across the domain.
