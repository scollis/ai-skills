---
name: blender-arm-instruments
description: Use when modelling an ARM instrument (KAZR, AERI, MPL, MFRSR, ECOR, SIRS, MET...) as a standalone Blender asset from its ARM handbook, photos and specs, and dropping it into the farm/site scenes.
---

# ARM instruments in Blender from the handbooks

One `.blend` per instrument, built by a deterministic headless script, then appended into the site scenes (M1 SERF, S1 MIRF, S2 KAWG, AMF LiDAR sites). Built so far: AERI, AOSMET, ASI, CEIL, CSPHOT, DL, ECOR, IRT, KAZR, LDIS, MAWS, MET, MFR, MFRSR, MPL, MWR3C, RWP, SEBS, SIRS, SONDE, VDIS, WB (plus C-SAPR2 and AWOS as one-offs). Pairs with `blender-engineering-asset` (dimension verification) and `blender-remote-mcp` (headless mechanics on the Mac).

## Layout on the Mac (`~/Documents/blender/farm_amf2/`)
- `handbooks/` — PDFs, `text/*.txt`, `figures/<inst>/`, `figures/_index.json`, contact sheets `figures/_sheet_*.jpg`, `refphotos/`.
- `scripts/instr/` — `inst_common.py` (harness), `build_<id>.py` (one per instrument), `queue_runner.py`, `render_orbit.py`, `encode_orbit.py`, `_bb.py`.
- `assets/instruments/<ID>/` — `<ID>.blend`, `build_report.json`, `preview/`, `orbit/`, `<ID>_orbit.mp4`, `render_report.json`; shared `_tex/` (ambientCG sets + DaySkyHDRI069A), `_contact/`, `_logs/build_<ID>.txt`.

## 1. Gather the sources
- Handbooks: `https://www.arm.gov/publications/tech_reports/handbooks/<name>.pdf`. Some are filed by TR number: WB Pluvio = `doe-sc-arm-tr-232`, MWR3C = `-300`, SEBS = `-332`, ECOR = `-333`, AOS = `-343`. Download **on the Mac** (`handbooks/_dl.py`, `User-Agent: Mozilla/5.0`, skip files already > 10 kB); the cloud container's proxy blocks many sites.
- Text: `scripts/pdftext.swift` via `run_text.sh` (PDFKit; there is no poppler on the Mac) → `handbooks/text/`. Grep it for dimensions, mount heights, weights, antenna/aperture sizes, "mounted on", "height above".
- Figures: `scripts/pdfimg.py` is a pure-Python PDF image-XObject extractor (MAP of pdf → short name). Output `figures/<inst>/<inst>_obj<N>_<w>x<h>.{jpg,png}`. 1275×1650 images are scanned full pages. `sheet.swift` makes contact sheets so a whole handbook's figures can be reviewed in one image.
- Photos beat handbook drawings for "what it looks like at an AMF": ARM Flickr albums (`flickr_album.py`, slow and polite, Safari UA + Referer) and Scott's own photos. Ask Scott for photos of the actual installation before detailing.
- Decide early what is generic (sensor make, mount, enclosure) and write it in the build script docstring and `meta()`.

## 2. Build script pattern
```python
"""KAZR - <what is modelled, what is not>. Refs: DOE/SC-ARM/TR-106 (antenna 2 m Cassegrain...), handbook photos of <sites>."""
import sys; sys.path.insert(0, '<farm_amf2>/scripts/instr')
from inst_common import *
ID = 'KAZR'; root = reset(ID); M = lib()
fibre = pbr('fibreglass_white', 'Plastic013A', tint=(0.86,0.85,0.80), tint_mix=0.85, scale=1.2, metallic=0.0)
box(...); cyl(...); rod(...); lathe(...); cable(...)
meta(source='TR-106', generic=['blower'], height_m=1.89)
finish(stage_kw={...}, cam_kw={...}, preview_kw=[{}, {'tag':'close','zoom':0.5}])
```
Run: `Blender -b --factory-startup --python build_<id>.py -- preview` (~1 min incl. previews). Every log ends with `BUILD_REPORT {...}`; key on it.

### Harness conventions (`inst_common.py`) — keep them so every asset drops in the same way
- Metres, Z up, instrument base on Z = 0 centred on the origin. Roof-mounted kit (KAZR, MWR3C, radiometers on a container): Z = 0 is the roof surface.
- +Y = north / the face toward the sun tracker or the front panel.
- Everything in collection `INST_<ID>`, parented to empty `<ID>_root`. Presentation (ground disc, sky, sun, `OrbitPivot`, `OrbitCam`) lives in `_Stage_<ID>` and is never appended.
- Primitives: `box, cyl, tube, sphere, rod(p0,p1,r), cable(pts, sag), lathe(profile), extrude_poly, text, array_ring, group, lattice_mast`. Pass `mat=`, `bevel=`, `parent=`.
- Materials: `pbr(name, tex_id, tint, tint_mix, scale, metallic, rough_mul...)` box-projects an ambientCG set on Object coords (no UVs needed). `lib()` gives the palette: white/beige/grey/black/arm_blue/yellow/red/green paint, aluminum, anodized, stainless, galvanized, corrugated, chrome, brass, gold_foil, plastics, rubber; `glass()` for domes and windows. Dielectrics metallic 0, metals 1.
- `meta(**kw)` stores provenance and dimensions on the root (bbox is added on save).
- `finish()` = stage (physical sky + sun over mown grass with a gravel apron) → render settings (Cycles, adaptive, OIDN, AgX Medium High Contrast) → orbit camera framed from the bbox → save → previews at 4 azimuths → `build_report.json`.

## 3. Check before calling it done
- Read `build_report.json`: bbox vs the handbook dimension (height, footprint), object count.
- Look at the previews (prev_325/055/145/235 plus close/rim). Make a contact sheet of several instruments at once (`_contact/<ID>_0001/0045/0090.jpg`) to compare scale and paint.
- `_bb.py`-style sweep: list objects whose evaluated bbox falls below z −0.05 or outside the expected envelope — catches floating or sunk parts.
- Compare with at least one real photo from the same viewpoint; fix shape errors before adding bolts.

## 4. Orbit videos (serial, never in parallel)
- Queue line in `assets/instruments/_render_queue.txt`: `<ID> <spp> <w> <h> [frames]`. Start the runner (idempotent, PID lock): `Blender -b --factory-startup --python queue_runner.py`. It runs `render_orbit.py` (resumable: overwrite off + placeholders) then `encode_orbit.py` → `<ID>_orbit.mp4`. Exits after ~30 min idle.
- Typical cost: 120 frames, 96 spp, 1080p, ~24 min (KAZR) on the M3 Max GPU.

## 5. Putting instruments into a site scene
- Append only `INST_<ID>`; place `<ID>_root` from the site layout (lidar/DEM height under the footprint, yaw from the real alignment).
- Edit (lift, rotate) only while the appended collection is in the view layer. Under an excluded `_AssetLib` the world matrices are stale (an ECOR tower read as 1.6 m instead of 3.2 m).
- Site rules from Scott: 30 m clear of trees around sensors; ECOR raised to 4 m and placed in the crop (clear crop points within ~2.2 m); no SACR at M1 (it lives at S2); check container orientation and order against photos at full resolution before laying out a row.
- Sharing: assets go to the `ablemodels` repo (clone `~/general_repos/ablemodels`), stratified by asset type with previews, self-contained via linked assets; PRs from a work branch to upstream.

## Pitfalls
- Handbooks show several generations of hardware; date the photo and pick the AMF version.
- Don't invent fine detail the sources don't show; say what is generic.
- Long builds in the GUI session time out the MCP call (~60 s) — always headless, see `blender-remote-mcp`.
