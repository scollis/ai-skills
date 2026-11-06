---
name: cm1-clouds-to-blender
description: Use when converting CM1 (or LES) output into OpenVDB volumes and rendering the clouds physically in the Blender site scenes — species grids, per-species optics, placement, cameras, timelapses and performance.
---

# Getting CM1 clouds into Blender

Runs come from `cm1-cloud-simulation`. Scene look and haze from `blender-landscape-realism`; remote/headless mechanics from `blender-remote-mcp`.

## Standing conventions (Scott)
1. **No noise on the storm**: render the model condensate as-is — no shader noise, billows or erosion (`NOISE=0` default; `NOISE=1` only for comparison).
2. **Physically based optics at full density** (`OPTICS=phys2 OPT_SCALE=1.0`), species kept separate.
3. **Golden standard light**: sun az 105, el 15, `SUNPHYS=1 AOD=0.2 SKYAER=2 HAZE=0.3`.
4. **`max_bounces` ≥ volume bounces + 4**. farm_v4/v5 ship with `max_bounces = 4`, which silently capped all volume scattering and made storms grey. Every render script must set it.
5. GPU (Metal) on the M3 Max is faster than CPU for storms. LES fields with many tiles (UCLA) render on CPU on the Air/laptop to avoid Metal memory spikes.

## Conversion pipeline (`cm1/`)
1. `cm1_to_npz.py <cm1out_N.nc> <out.npz> [dz_m]` (env python): resample the stretched vertical grid to uniform dz; grids in g m⁻³, (x,y,z): `cloud` (qc), `cice` (qi), `snow` (qs), `graup` (qg+qhl), `rain` (qr), legacy `ice` (qi+qs), `dbz`. dz: 25 m BOMEX, 50 m TCu, 100 m for 100 m runs, 250 m otherwise.
   - Stretched horizontal grid: `cm1_to_npz_stretch.py <nc> <base> [dz_in 100] [dx_out 500] [dz_out 250]` → `_in.npz` (uniform inner) + `_out.npz` (whole domain at 500 m, **zeroed inside the inner box** so they don't double up). Prints CORE_LOCAL and outer extent.
2. `npz_to_vdb.py` (Blender python: `Blender -b --factory-startup --python npz_to_vdb.py -- in.npz out.vdb [min_gm3]`): one FloatGrid per field, voxel = dx/dz in metres, origin at domain centre at ground (z = 0).
   - **Skip empty grids.** A grid with 0 active voxels has a ±2³¹ bbox and Cycles crawls (a frame sat 95 min). `vdb_drop_empty.py` cleans old files; `vdbinfo.py` prints per-grid counts and bboxes.
3. Batch scripts convert every output minute in parallel (3 at a time), delete the npz, log core and extent (`conv_t*.log`), then copy VDBs to Drive.
4. Periodic LES fields: `tile_vdb.py -- in.npz out.vdb n` tiles n×n into ONE VDB (never linked object copies — seams and slow). `CLEAR="az1:az2:rmin"` empties a compass wedge to keep a sight line to a distant storm.
- In Blender, `volume.grids` reads empty until `grids.load()`.

## Optics (`phys2`)
Per-species extinction per mass from effective radius, β/q ≈ 3/(2ρ r_e):
| Species | β/q (m⁻¹ per g m⁻³) | Phase |
|---|---|---|
| cloud water | 0.15 (r_e ~10 µm) | Mie, 20 µm |
| cloud ice | 0.04 | HG g 0.75 |
| snow | 0.01 | HG g 0.88 |
| graupel/hail | 0.004 | HG g 0.90 |
| rain | 0.0015 | HG g 0.90 |
- Cycles reserves 32 slots per volume closure, cap 64. So `phys2` = 2 closures: (1) cloud water Mie; (2) all ice + rain in one HG with density Σβᵢ and extinction-weighted mean g. Within 3/255 of the 5-closure version, which exceeds the limit.
- BOMEX cumulus (`CM1_Cu_phys2`): cloud Mie 20 µm β/q 0.15, rain HG g 0.9 β/q 0.0015. "Look C": volume step rate 4, haze ×0.4, `EDGE=0.02:0.15` smoothstep on cloud water to remove 50 m-grid edge fuzz (slightly alters the field; use haze-only if it must stay untouched).
- Volume step rate 1 vs 4 made no visible difference and doubled time.

## Placement and cameras (`build_serf_storm.py` / `run_serf_storm.sh <res%> <spp>`)
- Env: `STORM_VDB`, `STORM_VDB_OUT` (outer grid, same transform), `EXTRA_VDB`/`EXTRA_LOC`/`EXTRA_ROT` (second field sharing the material), `CORE="x,y"` (precip core in VDB-local m), `DIST` (core distance), `CAZ` (core azimuth from camera), `AA` (anvil azimuth → storm rotation), `CAMXYZ` (z is AGL by ray cast when `CAM_AGL=1`), `VAZ`, `PITCH`, `LENS`, `SUNS="az:el,..."`, `CLEARSKY=1`, `NOUCLA=1`, `VB`, `VS`, `DEVICE`, `DRYRUN=1` (save blend only).
- Standard wide view: camera (1237, −129, 300), CAZ 282, DIST 45 km, AA 210, 16 mm, pitch 3. Pad view: (64, 98, 4 AGL), VAZ 281–285, 20 mm, pitch 6.
- Lessons: at 10–15 km the storm fills the sky and reads as overcast; use ≥25–45 km (65–95 km for late, wide anvils). An anvil toward the camera shades the site; one along the view axis renders pathologically slowly. The farm ground ends ~15–20 km out — aerials must look down steeply. A dense TCu field near the camera hides a distant storm unless a corridor is cleared.
- Sky: Sky Texture MULTIPLE_SCATTERING, `sun_rotation = 180° − compass az`. `SUNPHYS` sets sun colour/energy from Rayleigh + aerosol transmission (15° sun → (1.00, 0.86, 0.58), exposure +0.78).
- Other scenes: the same storm and material are reused at S1 (`add_storm_s1.py`) and S2 (`make_storm_fly.py`, `PLACE=m1view` reproduces the M1 geometry; true geographic placement put S2 under the anvil and was rejected).

## Timelapses and fly-throughs
- Storm-relative: place every frame with one core so the storm grows in place. Camera can pull back over time (run E: 35 → 95 km, 24 → 16 mm).
- Skip existing frames; each frame waits for other storm renders (`pgrep -f build_serf_storm.py`).
- Encode with Blender's VSE (`encode_seq.py`, `tl_encode.py` with cross-fades) — no ffmpeg on the Macs.
- QC: per-frame mean brightness and frame-difference spikes.

## Cost guide (1080p, 64 spp, VB 64, GPU M3 Max)
500 m storm 1–5 min; 250 m 3–8 min; 100 m 15–20 min; run E inner+outer 15–60 min at 128 spp; timelapse 32 spp ~4.6 min/frame. Always run a memory watchdog whose pattern matches the render script's name.

## Never
- Never put a second **overlapping** VDB volume object over the storm (e.g. an emission-only copy): Cycles GPU renders the whole storm in rectangular blocks (known bug, still in 4.x/5.x). Non-overlapping inner/outer grids are fine.
- Never `ls`/`du` Google Drive inside a Blender MCP call.
