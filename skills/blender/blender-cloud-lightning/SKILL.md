---
name: blender-cloud-lightning
description: Use when adding lightning to a CM1/VDB storm in Blender Cycles — choosing flash sites from model physics, in-cloud glow, cloud-to-ground bolts, flash timing, and keeping render cost down.
---

# Lightning in Blender (CM1 storms)

Builds on a storm already in the scene with the `phys2` material (`cm1-clouds-to-blender`). Files: `~/Documents/blender/farm_amf2/cm1/lightning/` (experiments) and `mirf_s1/add_lightning_s1.py` (production version, S1 tour).

## 1. Pick flash sites from the model
`lightning_sites.py <cm1out.nc> <out.json> [n]` (CM1 env python):
- Score = graupel × √(cloud ice + snow + 0.05) × max(w, 0) inside the −10 to −30 °C layer (non-inductive charging zone).
- Take the top N columns with a 3 km exclusion radius; write VDB-local x, y (m from domain centre), z, T, w, graupel, ice, qc.
- Expect two clusters: the main updraft (w 45–66 m/s, −25 °C, ~8.5 km) and secondary cells near the precip core.
- World position = `storm.matrix_world @ local` (the storm object is usually rotated, e.g. −120°).

## 2. Why point lights don't work
A 1e9–1e11 W point light inside the core changes the image by ~3/255. Cloud-water extinction 0.15 m⁻¹ per g m⁻³ → ~10 m mean free path; even 64 bounces carry light only a few hundred metres. Real flashes rely on thousands of scatterings (Dobashi et al. precompute them).

## 3. In-cloud flash = emission in the storm's own material
Add an Emission (volume) via Add Shader onto the phys2 output (node `LTG_Add`):
```
strength = GLOW · skin(q) · Σ aᵢ · exp(−dᵢ² / 2σ²)
q    = cloud + cice + snow + graup
skin = ramp(q, 0.02→0.08) · (1 − ramp(q, 0.8→1.6))   # the cloud's outer layer, where light escapes
dᵢ   = |Geometry.Position (world) − siteᵢ (world)|
```
- Use world-space Geometry Position. Texture Coordinate Object space on a VDB is not metres (first-batch bug).
- Emitting at the sites (core) gets absorbed; emitting in all condensate floods storm and haze. The skin mask is what makes it read.
- Each aᵢ is a Value node `LTG_s<i>` keyframed with CONSTANT interpolation (flash on/off, a few frames, with flicker).
- **Never** a second overlapping emission-only VDB object — the storm renders in rectangular blocks (Cycles GPU bug). One object, one material; no closure-limit warning appeared even with phys2 at 64 slots.
- Starting values: σ 1.8–3 km, GLOW 0.01 (close test) to 0.12 (34 km away in daylight).

## 4. Cloud-to-ground strikes
- `LTG_Bolt<n>`: branching emissive curve from cloud base to ground, a few km from the precip core toward the camera, plus a faint fat `_Halo` copy.
- Point light `LTG_Flash` ~900 m up over the bolt lights the cloud base and rain shaft.
- Key visibility, emission and light power together; 1–3 return strokes with flicker over ~6 frames.
- S1 production settings: `GLOW=0.12 SIGMA=1800 BOLT_W=40 BOLT_E=20000 HALO_E=80 HALO_X=4 PL_W=1e10`; `BOLT_OFF1/2` move strikes.

## 5. Timing and rendering
- Flash script example (S1 tour, frames 1446–1552): in-cloud bursts at 1446, 1474–1478, 1530; strikes 1506–1512 and 1546–1551. Shift keys as a block when retiming into another shot (KAWG used +174 frames).
- Emission nodes slow every storm sample: the render script connects `LTG_Add` **only on frames where some aᵢ > 0**; other frames render plain phys2.
- Check lightning at **full resolution** — at half res a 1–3 px bolt becomes a smudge. At ~34 km a bolt reads as a bright burst lighting the rain shaft, not a crisp line; haze and the denoiser soften it (close to real daylight viewing).
- Dusk sells it: sun 2°, energy ×0.15, exposure −0.5.
- Cost: ~27 min per 1080p 16 spp lightning frame on the Air.
- Keep a no-lightning backup (`*_nolt.blend`) and always re-apply `add_lightning_*.py` to the backup when retuning — never stack it on a scene that already has lightning.

## Next steps (not yet done)
- Physical in-cloud flash: solve steady diffusion from a point/line source through the CM1 optical grid in numpy (D = 1/(3 σ_s (1 − g))), write fluence as a `flash` grid in the VDB, emit ∝ σ_s · fluence in the same single material.
- Anvil "spider" flashes as emissive filaments in the anvil skin.
- Per-site flash sequences in the timelapse once the look is settled.
