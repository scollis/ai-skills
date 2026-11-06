---
name: c850-blender-aircraft
description: Use when building, modifying, verifying or placing the ARM AAF Challenger 850 (N850RJ) research aircraft model in Blender, or modelling another aircraft the same way.
---

# The ARM Challenger 850 (N850RJ) in Blender

General method (MB bmesh builder, hinge empties, surface-conforming decals, silhouette overlay) is in `blender-engineering-asset`; this skill holds the aircraft-specific numbers and decisions so they don't have to be re-derived.

## Files (Mac `~/Documents/blender/farm_amf2/`)
- Asset: `assets/aircraft/C850_ARM/c850_arm.blend` (collection with `C850_root`).
- Builder: `airport_awg/build_c850.py` (v3), headless `Blender -b --factory-startup --python build_c850.py`.
- Renders: `airport_awg/render_c850.py` → `C850_ARM/renders/c3_*.jpg`.
- Reference: Bombardier CRJ100/200/440 **Airport Planning Manual** (CSP A-020 rev 8), `C850_ARM/ref/CRJ200APMR8.pdf`; Figure 2 "General Airplane Dimensions (Metric)" on page 25. The CL-850 shares the CRJ200 airframe. Newspaper/magazine 3-views were ~5 % inconsistent — use the APM.

## Frame and verified dimensions
+Y to the nose, +X to the right wing, Z up; nose tip at y = +14.6. Stations below are metres aft of the nose tip.

| Item | Value |
|---|---|
| Span / overall length / height | 21.23 / 26.77 / 6.22 m |
| Fuselage nose → tail cone | 24.38 m (fin and stab tips reach 26.77) |
| Wing LE | 10.03 at fuselage side, 12.05 at kink (x 4.02, ~37° inboard), 15.22 at tip (~27° outboard) |
| Wing TE | unswept inboard at 14.34, 16.62 at tip; root chord 4.27, tip ~1.4; tip at x 10.19 + winglet |
| Fin | LE sweep 46.5°, root LE ~20.66 on fuselage top |
| Stabiliser | root LE 23.62, span 6.20, tip chord 0.95, z 5.93; bullet fairing ends 26.77 |
| Nacelles | inlet 17.03, length 3.75, Ø 1.45, centre x ±2.43, z 2.86 |
| Gear | nose 2.10, mains 13.45 (wheelbase 11.4), track ±1.57; nose pivot z 1.35 so it folds into the nose |
| Doors / windows | L entry door 4.25–5.15 (0.91 m); cabin windows 6.15–14.55 |

## Nose, glazing, livery
- Short blunt CRJ radome; crown line = monotone cubic (Fritsch–Carlson) through points traced from photos and the 3-view.
- Glazing is a level band z 2.60–3.01: main windscreen (centre post), corner pane, side and DV windows at 2.90–3.88. Panes are grids mapped point-by-point onto the skin, with silver frames.
- Corner-pane posts have constant on-skin width (6 cm, solved by bisection), and each pane's rear edge is tied to the next post. Constant-angle edges diverge on the tapering nose and leave slivers (the v2 bug).
- Livery: white, navy + gold swept stripes, navy pinstripe, `N850RJ` on both nacelles. Windows, stripes and door seams are separate geometry offset 2–5 mm along the normal, never face-material paint.

## Instruments (Scott's rules)
- Wing pods and probes are **gold**, pylons grey. Pylons at ±4.6 m and ±7.0 m semispan: L outboard HVPS-3, L inboard FSSP-100, R inboard PIP, R outboard King LWC.
- Fuselage sensors only around the nose, below/behind the glazing, never in the pilots' view: droplet inlet R 3.45, aerosol inlet L 3.45, trace-gas inlet R chin 4.35, TAT housings, pitots, AoA vanes.
- Shapes are generic PMS/DMT/SPEC; real ARM probe stations are unconfirmed — keep that in the root note.

## Animation
Custom props on `C850_root`: `gear`, `flap_deg`, `aileron_deg`, `elevator_deg`, `rudder_deg`, `fan_rps`, driven by SINGLE_PROP drivers onto hinge empties placed on the true hinge lines. Sweep each DOF (gear 0/1, flaps 0/max) and look for parts poking through before saving.

## Verify (do this after any geometry change)
1. Extents from evaluated geometry vs span / length / height above.
2. Silhouette overlay on APM Figure 2 at 300 dpi = **49.55 px/m** (derive from the 26.77 m dimension line, cross-check a second one): export world triangles, rasterize plan/side/front with PIL, register nose / centreline / ground line, paint the model translucent red over the figure, read the differences. Scripts: `ortho_sil.py`, `overlay_apm.py` (cloud container).
3. True orthographic Cycles 3-view (`ortho_scale = px / px_per_m`, transparent film) with a metric ruler for Scott.
- Errors this caught before: fuselage drawn to overall length, wing too far aft, missing inboard LE kink, wrong fin sweep, nacelle height, gear and door stations.

## Workflow
- Develop in the cloud container: `pip install bpy --break-system-packages` gives Blender 5.2.3 (same as the Mac). Debug-render there.
- Push to the Mac as a line-diff patch with md5 checks before and after (see `blender-remote-mcp`). The container proxy blocks bombardier.com: download on the Mac, pull across in base64 chunks.

## Placing it in a scene (KAWG/S2)
- Append only the aircraft collection. Set yaw from the OSM taxiway/apron, z and pitch/roll from the DEM under the three gear contact points; set `gear` = 1 on the ground.
- Report clearances (wingtip to the radar compound, to hangars). It appears in the KAWG fly-throughs on the apron.
