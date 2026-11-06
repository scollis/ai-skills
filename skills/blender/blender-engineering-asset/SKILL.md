---
name: blender-engineering-asset
description: Use when building a dimensionally accurate procedural Blender asset of real hardware (radars, met stations, aircraft, probes) from photos, specs and drawings, and when verifying its proportions.
---

# Building and verifying engineering assets

Learned building the ARM C-SAPR2 (tower, radome, El-over-Az pedestal), the KAWG AWOS-III and the ARM Challenger 850 cloud-physics aircraft. Pairs with `blender-remote-mcp` (headless/remote mechanics).

## Research first, then model
- Get authoritative dimensions before shaping anything. For aircraft the manufacturer's **Airport Planning Manual** (general-arrangement figure, metric) beats magazine 3-views and Wikipedia: it gives fuselage vs overall length, root/tip chord, wheelbase, track, nacelle diameter, door positions. Newspaper 3-views can be internally inconsistent by ~5 %.
- Service-point tables (refuel adapter, overwing fillers) locate the wing root/LE when figures are images.
- Ask the user for photos of the real installation; note what is generic (probe models/stations, sensor makes) in the asset's root `note` and in the project doc.
- User rules seen so far: radome panels randomized and the inside renderable (dome transparency prop); transmitters may live in a container with waveguides routed through rotary joints; aircraft pods/probes are gold; fuselage research sensors go around the nose, below/behind the glazing, never in the pilots' view.

## Script structure (deterministic rebuilds)
- One `build_<asset>.py`, headless `--factory-startup`, writes `assets/<kind>/<NAME>/<name>.blend`. Collection `<NAME>` + preview-only collection (`*_Preview`: ground, sun, sky, cameras) that scenes never append.
- Helper class `MB` (bmesh builder): `box`, `beam(p0,p1,w,h,up)`, `cyl(p0,p1,r0,r1,seg)`, `sphere`, `loft(rings)`, `lathe(profile, axis_p, axis_d)`, `obj(name, mats, parent)`. Helpers `hexbolt`, `bolt_circle`, NURBS `cable(...)`, aerofoil `section(LE, chord_dir, thick_dir, c, t, u0, u1)` (NACA 4-digit) for wings, fins, pylons, struts and masts.
- Root empty with custom props for every animatable DOF (az/el, gear, flaps, ailerons, elevator, rudder, fan rps, wind dir, cup rps, mast tilt) driven by SINGLE_PROP drivers. Each moving part gets a pivot empty placed exactly on its hinge axis (`frame_from(origin, axis)`), with the mesh built in world coords then `mesh.transform(M.inverted())`. Choose the axis direction so + angle has the documented sense on both sides.
- Cables/waveguides that cross a rotation axis must meet at a point ON that axis (split into a part parented to each frame) or they detach when animated. Sweep the DOFs (e.g. el 0/45/90, az 3 values) and look before calling it done.

## Surfaces, decals and glazing
- Never paint windows/stripes by assigning face materials on a coarse mesh: they come out jagged. Build them as separate geometry that conforms to the analytic surface: parameterize the fuselage cross-section (`fus_sec(s) -> zmid, half_w, half_h`), write `surf_at(s, side, z, off)` / `surf_phi(s, side, phi, off)`, and build windows (fan of an ellipse in (s,z)), livery ribbons (two edges sampled along s) and door seams (polyline in (s,z)) offset 2-5 mm along the normal; windows slightly above stripes.
- Large curved panes (windscreens) need a grid over the pane mapped point-by-point onto the skin; fan triangles sag under the skin.
- Edges defined as constant-angle lines diverge on a tapering nose -> triangles of frame/skin between panes. Define posts with constant on-skin width (solve phi by bisection so the 3-D distance equals the post width) and tie a pane's rear edge to the next pane's post.
- Bisection solvers must clamp to reachable values (e.g. a z band not reached at that phi) or vertices run to the search limit and leave slivers; print the s/z ranges of new pane meshes to catch it.
- Shape lines (nose crown, radome) as monotone cubic (Fritsch-Carlson) splines through points traced from side photos/drawings; avoid piecewise power laws that leave creases.

## Verify proportions quantitatively
1. Overall extents from evaluated geometry (all mesh/curve/text objects, modifiers applied): span, length, height vs spec.
2. Orthographic silhouette overlay: export world triangles (`to_mesh()` + `loop_triangles`), rasterize plan/side/front with PIL at the drawing's own scale (derive px/m from a dimension line, e.g. 26.77 m extension lines; check the scale bar against a second dimension), register nose x / centreline / ground line, paint the model translucent red over the drawing, read the differences, fix, repeat. One rendering pass takes seconds locally.
3. Then render true orthographic Cycles views (ORTHO camera, `ortho_scale = pixels / px_per_m`, film transparent) and compose a 3-view sheet with a metric/imperial ruler at the same scale for the user.
- Typical errors this caught: fuselage drawn to overall length (tail cone should end earlier; fin/stab tips reach overall length), wing too far aft with wrong root chord / missing inboard LE kink, fin sweep, nacelle height/diameter, gear stations, door station.
- Re-check side effects after big moves: retracted gear poking out, pylons/probes relative to the new LE, decals on the new tail cone, registration text orientation.

## Placing assets in site scenes
- Append only the asset collection; set root location from the DEM, yaw from the real alignment (OSM taxiway segment, lidar mast position, NAIP pad), pitch/roll from ground under the contact points; add 2-3 dedicated cameras (ground, drone, context with neighbouring instruments).
- Keep clearance in mind (wingtip to radar compound, mast to pad edge) and report it.