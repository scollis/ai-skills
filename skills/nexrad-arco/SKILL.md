---
name: nexrad-arco
description: Read WSR-88D NEXRAD Level II radar from the analysis-ready NEXRAD ARCO Icechunk/Zarr store on AWS (s3://nexrad-arco) as Py-ART radar objects, and plot reflectivity / dual-pol PPI maps, time-height QVPs, and animations. Use for cloud-native NEXRAD ARCO access (icechunk + rustytree engine), the anonymous-S3 TLS/CA fix, the split-cut and 0-based-sweep_number gotchas, and surface METAR station overlays from the Iowa Environmental Mesonet. Complements nexrad-radar-gcs (raw Level II from the GCS bucket).
---

# NEXRAD ARCO (cloud-native Level II)

The NEXRAD ARCO store (`s3://nexrad-arco`, https://registry.opendata.aws/nexrad-arco/)
is an **Icechunk**-managed **Zarr v3** archive, one repo per WSR-88D radar. Inside a
radar the data is grouped by **VCP** (volume coverage pattern) then **sweep**; each
`/VCP-xxx/sweep_N` group is a single **time-stacked cube** with a `vcp_time` axis
spanning 2015 → near-real-time (~30 min lag behind the live feed). Only one VCP scans
at a time, so the freshest volume lives in whichever VCP the radar is currently running.

Fields use **ODIM names** (`DBZH`, `ZDR`, `RHOHV`, `PHIDP`, `VRADH`, `WRADH`).

This skill ships `kernel.py`, auto-loaded into the python kernel when the skill is
loaded. It pairs with **`nexrad-radar-gcs`** (raw Level II volumes from the GCS bucket),
whose helpers you use for plotting: `setup_cmweather`, `make_radar_geoaxes`,
`plot_ppi_map`, `add_context_features`. Load both when making maps.

## Environment

Needs an env with `arm-pyart`, `xradar>=0.12`, `xarray>=2026.4`, `zarr>=3`, `icechunk`,
**`rustytree-xarray>=0.3`** (the `rustytree` xarray engine — NOT importable as bare
`rustytree`, and NOT on PyPI as `rustytree`), `cmweather`, `cartopy`, `metpy`, and
`requests`. In this project that env is `radar`.

## The one hard gotcha: TLS/CA trust for the native S3 client

`icechunk`'s Rust `object_store` client does **not** read Python's certifi bundle by
default and fails the S3 handshake with `invalid peer certificate: UnknownIssuer`. The
native trust store initializes **once per process and is cached** — `importlib.reload`
does not reset it, and a kernel that has already imported icechunk without the fix
cannot recover. The fix: set the CA env vars **before the first `import icechunk`**.

`kernel.py` does this correctly: it does **not** import icechunk at module scope, and
`connect()` calls `ensure_ca()` (which points `SSL_CERT_FILE` / `AWS_CA_BUNDLE` /
`REQUESTS_CA_BUNDLE` / `CURL_CA_BUNDLE` at `certifi.where()`) before the lazy
`import icechunk`. So as long as your **first** icechunk touch in the kernel goes
through `connect()`, TLS just works. Do NOT `import icechunk` yourself in an earlier
cell — that taints the process and you must restart the kernel.

## Network access

The icechunk client addresses the bucket at the **virtual-hosted regional host**
`nexrad-arco.s3.us-east-1.amazonaws.com` — grant network access to that host. The
path-style `s3.amazonaws.com` is on the denylist and cannot be granted. (boto3
path-style reaches it via the grantable `nexrad-arco.s3.amazonaws.com`.)

## Workflow

```python
from kernel import (connect, latest_scan, vcp_time_bounds, to_pyart,
                    fetch_asos, obs_for_time, add_stations)  # auto-loaded

session = connect("KLOT")                 # anonymous, read-only
bounds  = vcp_time_bounds(session)        # per-VCP first/last, newest first
scan, meta = latest_scan(session)         # georeferenced sweep_0 + meta{vcp,time,bounds}
radar = to_pyart(session, meta, nsweeps=2)  # Py-ART Radar (0-based sweep fix applied)
```

To pull a specific time, build `meta = {"vcp": "VCP-212", "time": pd.Timestamp("...")}`
and call `to_pyart(session, meta)`. Get the available timestamps from
`vcp_time_bounds` or by opening the sweep_0 cube's `vcp_time` axis directly.

### to_pyart gotchas (handled by kernel.py — know them if you diverge)

- **sweep_number**: the store stores it as **1-based float32**; Py-ART's Xradar
  accessor indexes sweeps by 0-based sequential int64 matching group order. Each
  sweep's `sweep_number` is rebuilt as `np.int64(i)` or you get `KeyError: 0.0`.
- **Standard field aliases**: ODIM fields are deep-copied to Py-ART standard names
  (`reflectivity`←`DBZH`, `cross_correlation_ratio`←`RHOHV`,
  `differential_reflectivity`←`ZDR`, `velocity`←`VRADH`, …) with units set, so
  `radar.get_field(0, "reflectivity")` works.

### Split-cut structure (dual-pol vs Doppler)

Low tilts are **split cuts**: `sweep_0` (surveillance, ~0.5°) carries
reflectivity + ZDR + RHOHV but **no velocity**; `sweep_1` (the Doppler cut at the same
elevation) carries **velocity** but no ZDR/RHOHV. So plot dual-pol fields from sweep 0
and **velocity from sweep 1**, and threshold the gatefilter on reflectivity+RHOHV — not
on the field being plotted (thresholding ZDR on a dBZ floor wrongly nulls it).

### Gatefilter and the reflectivity floor

`plot_ppi_map` (from `nexrad-radar-gcs`) applies a dual-pol gatefilter that excludes
RHOHV < `rhohv_min` and dBZ < `dbz_min`. To lower the *displayed* floor you must drop
**both** the colorbar `vmin` **and** `dbz_min` — the gatefilter masks weak echo before
it reaches the plot, so changing only `vmin` leaves it white. To show **all** low-level
/ clear-air structure, disable the filter entirely: `rhohv_min=-1.0, dbz_min=-1000.0`
(RHOHV ≥ 0 always, so nothing but invalid gates is excluded). Use colorblind-friendly
`ChaseSpectral` for reflectivity and `balance` for velocity.

## Surface METAR overlay

`fetch_asos(extent, start, end)` pulls ASOS/METAR obs (temp/dewpoint/wind) from the
Iowa Environmental Mesonet for the map `extent` `[W, E, S, N]` and time window, clipped
to extent across the IL/WI/IN/IA/MI networks. `obs_for_time(obs, t)` picks the nearest
ob per station to a frame time; `add_stations(ax, df)` draws station models on a cartopy
axes (temp NW red, dewpoint SW blue, wind barbs), thinned with MetPy's
`reduce_point_density`.

**MetPy note**: MetPy's `StationPlot` text artist is broken under matplotlib >= 3.11
(tuple-unpack error in `_get_layout`). `add_stations` places the temp/dewpoint numbers
with plain `ax.annotate` and uses MetPy only for wind-barb geometry — same look, avoids
the broken path.

## Animations

Build one Py-ART radar per timestamp (`to_pyart(session, meta, nsweeps=1)` for speed),
render each frame with `make_radar_geoaxes` + `plot_ppi_map` (+ `add_stations` for METAR),
`fig.savefig` per frame, `plt.close(fig)` and `gc.collect()` between frames, then
assemble with Pillow (`save_all=True, loop=0, optimize=True`, hold the last frame longer).

## cartopy cache

`~/.local/share` is not writable here. Before drawing context features set
`os.environ["CARTOPY_DATA_DIR"]` and `cartopy.config["data_dir"]` /
`["pre_existing_data_dir"]` to a writable workspace path (e.g. `./cartopy_cache`).


## QVP (quasi-vertical profile)

`qvp(session, vcp, times, sweep, fields=("DBZH","ZDR","RHOHV"), rho_min=0.80,
min_az=15, hmax_m=None)` builds a time-height QVP by azimuthally averaging each
field on one **high tilt** across a list of `vcp_time` timestamps, mapping slant
range to height AGL (4/3-earth beam). Returns `{times, height(m), elev, <field>:
(time x range) ...}`.

**Pick a populated high tilt.** A QVP wants the steepest available cut (more
height per range). Probe first — VCP-212 stores up to ~19.5°, but its higher
cuts (sweep_10+) are **empty at many archived times**, and at some events even
4° is unpopulated. Confirm `ray_elevation_angle` is finite and DBZH has coverage
at your target times before committing a sweep. sweep_9 (~4°) is a reliable
fallback that still resolves the melting layer (~3–4 km).

**QC is essential.** The function keeps only gates with `RHOHV > rho_min`
(≈0.80) and requires ≥`min_az` valid azimuths per range gate *before*
averaging. Skipping this is a real bug: low-SNR noise has random-low but finite
ρHV, so a naive azimuthal mean of ρHV aloft collapses to the floor (~0.7) and Z
is biased low. With QC, ρHV aloft in meteorological echo reads ~0.99 as it
should.

Plot as stacked `pcolormesh` time-height panels (`ChaseSpectral` for Z,
`balance` for ZDR, `plasma`/`magma` for ρHV), cap the y-axis at ~10 km, mark the
0 °C level. Example: KLOT 2022-08-29/30 convective event, sweep_9, gives clean
warm-rain ZDR (>3 dB below 3.5 km → ~0 aloft) and ρHV~1.
