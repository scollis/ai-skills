---
name: nexrad-radar-gcs
description: >
  Analyze NEXRAD Level II weather-radar data with Py-ART, pulling volume scans
  from the Google Cloud public bucket (gcp-public-data-nexrad-l2) as a fallback
  when the AWS NEXRAD bucket is blocked. Use for reflectivity / dual-pol PPI maps,
  rainfall events, Marshall-Palmer rain-rate time series over a site (e.g. an ARM
  facility), corrupt-scan-safe volume reading, dual-pol gate filtering, and
  cmweather colormaps. Ships kernel.py helpers: nexrad_gcs_keys, download_nexrad,
  scan_time, read_radar_safe, dualpol_gatefilter, extract_site_rainrate,
  plot_ppi_map, add_context_features, setup_cmweather.
---

# NEXRAD radar via Google Cloud + Py-ART

Workflow for weather-radar analysis over a fixed ground site. Handles the common
snag that the AWS NEXRAD bucket is unreachable from the sandbox, and standardises
the dual-pol filtering, Marshall-Palmer Z-R conversion, and cmweather styling.

Environment: needs `pyart` (arm-pyart), `cmweather`, `cartopy`, `numpy`,
`pandas`, `matplotlib`. The `radar` conda env in this project has them.

## kernel.py helpers (auto-loaded when this skill loads)

- `scan_time(path)` -> datetime parsed from `SITEyyyymmdd_HHMMSS` in the key/filename.
- `nexrad_gcs_keys(site, year, month, day)` -> sorted list of Level-II volume keys
  for one radar on one UTC day (drops supplemental `_MDM` volumes).
- `download_nexrad(keys, dest_dir="nexrad_scans")` -> local paths, sorted by scan time.
- `read_radar_safe(path)` -> pyart Radar, or **None** if the volume is corrupt (skip it).
- `setup_cmweather()` -> registers cmweather colormaps AND resets `savefig.bbox`
  to `'standard'` (see gotcha below). Call once before plotting.
- `dualpol_gatefilter(radar, rhohv_min=0.85, dbz_min=5.0)` -> Py-ART GateFilter.
- `extract_site_rainrate(radar, site_lat, site_lon, radius_km=2.0)` ->
  `{mean_dbz, rain_rate_mmph, n_gates}` from the lowest sweep, averaged in linear Z.
- `make_radar_geoaxes(fig, radar, rect=[l,b,w,h], extent=[...], tiler=None)`
  -> a correctly-georeferenced **Mercator** GeoAxes. Use this to build the PPI axes;
  pass `tiler=cimgt.OSM(cache=True)` for a tiled street basemap. Do NOT use a cartopy
  AzimuthalEquidistant axes here -- see the georeferencing note below.
- `add_context_features(ax, extent)` -> overlay interstates (labeled), airports, and
  state borders from Natural Earth 10m. Call after plot_ppi_map (or pass context=True).
- `plot_ppi_map(radar, ax, fig, extent=[lonmin,lonmax,latmin,latmax], site=(lat,lon))`
  -> filtered PPI map on the GeoAxes with ChaseSpectral cmap + site/radar markers.

## Network access

The GCS bucket host is not on the default allowlist. Before the first fetch:
`request_network_access("gcp-public-data-nexrad-l2.storage.googleapis.com")`.
Cartopy's `resolution='10m'` state boundaries also fetch from
`naturalearth.s3.amazonaws.com` on first use -- grant that too if maps are drawn.
Prefer AWS first: the archive is `unidata-nexrad-level2` (see the
`nexrad-aws-2025` skill). The old `noaa-nexrad-level2` bucket is DEPRECATED
and returns a genuine S3 AccessDenied -- never fall back to it. Use this GCS
mirror when AWS is blocked by a proxy 403, or for the plotting helpers below.

## Choosing the radar

Pick the WSR-88D nearest the site. For the ASU West Valley ARM site
(33.606726 N, -112.166912 W) that is **KIWA** (Phoenix / Williams Gateway),
~50 km SE. Reflectivity directly over a site can be light even when nearby
convective cores are strong -- report the site footprint, not the scene max.

## Typical run

```python
skill({"skill": "nexrad-radar-gcs"})   # loads kernel.py helpers
# after request_network_access(...) for the bucket host:
keys  = nexrad_gcs_keys("KIWA", 2026, 6, 17)
# optionally clip to an event window using scan_time(k)
paths = download_nexrad(keys)

setup_cmweather()
rows = []
for p in paths:
    radar = read_radar_safe(p)
    if radar is None:            # corrupt volume -- skip
        continue
    r = extract_site_rainrate(radar, 33.606726, -112.166912, radius_km=2.0)
    r["time_utc"] = scan_time(p)
    rows.append(r)
```

## Marshall-Palmer Z-R

`Z = 200 * R**1.6` (Z linear). `extract_site_rainrate` averages reflectivity in
**linear** units over the footprint, then inverts:
`R = (Z_lin / 200)**(1/1.6)`. Override with `zr_a=`, `zr_b=` for other relations.

## Plotting gotcha (important)

`figure-style`'s `apply_figure_style()` sets `savefig.bbox='tight'`, which
**collapses a cartopy GeoAxes to a sliver on save**. Always call
`setup_cmweather()` (or `mpl.rcParams['savefig.bbox']='standard'`) AFTER
`apply_figure_style()` and before saving map figures. Use `fig.savefig(...)`
(never `plt.savefig`). **Build the PPI axes with `make_radar_geoaxes(fig, radar, ...)`** (a **Mercator** axes) and draw the field with `plot_ppi_map`, which plots Py-ART's **own** `radar.gate_longitude`/`gate_latitude` (spherical geometry, correct to ~6 decimals) via `pcolormesh(..., transform=ccrs.PlateCarree())`. **Do NOT** route the data through `RadarMapDisplay.plot_ppi_map` on a cartopy `AzimuthalEquidistant` axes: cartopy's aeqd transform is inaccurate at the origin for a non-zero `central_latitude` and maps the radar's own lon/lat to ~(0, +21 km), shifting the gate field ~21 km **south** of the radar marker. The visible symptom is a radar triangle sitting **north** of the cone-of-silence blind zone. Mercator + Py-ART gate lat/lon avoids any aeqd round-trip, so data, markers, roads, and basemap all share correct geodesy. Draw markers with `transform=ccrs.PlateCarree()`. Pass `context=True` to overlay interstates + airports (Natural Earth 10m), or give `make_radar_geoaxes` a `tiler=cimgt.OSM(cache=True)` for a tiled street basemap (needs network access to `a/b/c.tile.openstreetmap.org`).

## Two-panel animation (map + site time series)

Render one PNG per volume scan (left = `plot_ppi_map`; right = the rain-rate
series with the event window shaded and a moving vertical cursor at the current
frame's time), then assemble with Pillow: `img0.save("out.gif", save_all=True,
append_images=imgs[1:], duration=450, loop=0)`. ffmpeg may be absent; Pillow GIF
is the reliable path.
