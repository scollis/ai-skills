---
name: radar-advection-interpolation
description: Temporally interpolate weather-radar volumes - reconstruct an intermediate volume between two scans (or tween many frames for a smooth animation) by optical-flow advection morphing on native radar gate geometry. Estimates a spatially varying, height-resolved motion field with TV-L1 optical flow, then advects and blends per gate so the output is a true CfRadial volume, not a grid. Use for radar time interpolation, gap-filling between scan volumes, matching a radar to a faster instrument, or smooth PPI/CAPPI animations. Built and validated on ARM C-SAPR (MC3E) but works on any Py-ART Radar with reflectivity. Helpers auto-load into the python kernel.
---

# Radar volume advection interpolation

Reconstruct a radar volume at a time **between** two observed scans. Naive averaging
smears fast-moving convection into a ghost; this method estimates how the echo is moving
and pushes the neighbours to the target time before blending.

**Environment:** the `radar` conda env (Py-ART >= 2.0, scikit-image, scipy). The helper
functions below auto-load into the python kernel when this skill is loaded (`kernel.py`).

## Method summary

1. **Motion** - dense TV-L1 optical flow, estimated **per height level**. A single rigid
   advection vector fails for an MCS: the broad stratiform region pins whole-domain
   cross-correlation to zero shift while convective cells move at ~20 m/s. Motion also
   varies with height (strong low-level, weak aloft), so grid a z-stack and flow each level.
2. **Morph** - semi-Lagrangian forward/backward warp + time blend. For fractional time
   alpha in (0,1): forward-warp the earlier volume (sample at **+alpha*D**), backward-warp
   the later one (sample at **-(1-alpha)*D**), blend `(1-alpha)*earlier + alpha*later`.
3. **Native geometry** - do the morph per gate in the radar's own (azimuth, slant-range,
   elevation) coordinates so the output is an ordinary CfRadial volume.

> **The sign trap.** The single easiest thing to get wrong is the warp sign - flip it and
> the reconstruction is *worse* than a naive average. The reliable check is **end-to-end**:
> warp t1 by the *full* +D and confirm it reproduces t3 (it does; -D does not). The forward
> warp samples the source at **+alpha*D**. Get the sign from validation, not intuition.

## Helper functions (auto-loaded from kernel.py)

- `fetch_arm_volume(stamp, user, token, datastream, datadir)` -> Py-ART Radar. `stamp` is
  `'YYYYMMDD.HHMMSS'` (volume END time, as in the ARM filename). Needs an ARM Live token
  (https://adc.arm.gov/armlive/); adc.arm.gov must be network-allowlisted. For a non-ARM
  radar, skip this and read your volumes with `pyart.io.read_*` directly.
- `volume_midtime(radar)` -> representative UTC datetime (mean ray time).
- `grid_volume(radar, grid_shape, grid_limits, field)` -> Py-ART Grid (Barnes2/dist_beam;
  defaults: 8 levels 1-8 km, +-120 km, 241x241).
- `level_displacements(Za, Zb, y_m, x_m)` -> (U_east, V_north), each (z,y,x); TOTAL echo
  displacement in **meters** over the Za->Zb interval. `Za,Zb` are gridded reflectivity
  stacks (fill NaN for non-echo); `y_m,x_m` are the grid axes.
- `build_flow_interpolators(U, V, echo_mask, zlev_m, y_m, x_m)` -> (fU, fV)
  RegularGridInterpolators over (z,y,x).
- `interp_native_volume(rA, rB, fU, fV, alpha, zlev_m, field)` -> (nrays, ngates) array:
  the reconstructed field on rA's native geometry at fractional time alpha.
- `resample_to_geometry(rSrc, rTgt, field)` -> rSrc sampled onto rTgt geometry with NO
  advection (fair no-motion baseline).
- `score_reconstruction(pred, truth, thresh)` -> {rmse, mae, bias, cc, n} over echo.
- `sweep_sampler` / `sample_native` - low-level (az,range) bilinear sampling with azimuth
  wrap; used internally, exposed for custom work.

## Workflow

```python
# 1. Load three volumes (t1 earliest, t2 middle = held-out truth, t3 latest)
stamps = ["20110520.112734", "20110520.113434", "20110520.114134"]
radars = {k: fetch_arm_volume(s, user, token) for k, s in zip(["t1","t2","t3"], stamps)}
midt = {k: volume_midtime(v) for k, v in radars.items()}
dt12 = (midt["t2"]-midt["t1"]).total_seconds()
alpha = dt12 / (midt["t3"]-midt["t1"]).total_seconds()

# 2. Grid t1,t3 to a z-stack; build the height-resolved flow field
import numpy as np
g1, g3 = grid_volume(radars["t1"]), grid_volume(radars["t3"])
zlev_m, y_m, x_m = g1.z["data"], g1.y["data"], g1.x["data"]
Z1 = np.ma.filled(g1.fields["reflectivity"]["data"], np.nan)
Z3 = np.ma.filled(g3.fields["reflectivity"]["data"], np.nan)
U, V = level_displacements(Z1, Z3, y_m, x_m)
fU, fV = build_flow_interpolators(U, V, (Z1 > 5) | (Z3 > 5), zlev_m, y_m, x_m)

# 3. Reconstruct the intermediate volume on native geometry
R2 = interp_native_volume(radars["t1"], radars["t3"], fU, fV, alpha, zlev_m)

# 4. Validate against held-out real t2 (fair baselines resample with zero motion)
truth = np.ma.filled(radars["t2"].fields["reflectivity"]["data"].astype(float), np.nan)
print("morph  ", score_reconstruction(R2, truth))
lin = np.nanmean([resample_to_geometry(radars["t1"], radars["t2"]),
                  resample_to_geometry(radars["t3"], radars["t2"])], axis=0)
print("lin-avg", score_reconstruction(lin, truth))
```

## Animation (gap-filling)

To fill the gaps between real volumes with N tweens each, compute flow **pairwise** on
consecutive volumes (shorter interval -> cleaner flow than spanning the full span), then
`interp_native_volume(rA, rB, fU_ab, fV_ab, a, zlev_m)` for `a` in `[(i+1)/(N+1) ...]`.
Assemble real keyframes + tweens and render one sweep with matplotlib `pcolormesh` over
`gate_x/gate_y` (native PPI) or the CAPPI plane. **Label observed vs interpolated frames**
so the animation stays honest about what's reconstructed.

## Notes and gotchas

- **ARM access:** `sgpcsaprsurI7.00` (raw MDV surveillance) downloads from ARM Live;
  processed CMAC variants (`...cmac...c0`) are catalogued but order-only (404 on saveData).
- **Advection margin is modest at near range** and largest at far range - near-range gates
  are small and the storm barely moves relative to gate spacing. Expect a few % RMSE gain
  over linear-avg, concentrated in large far-range gates.
- **Residual error localizes at cell edges** - storm growth/decay, which a purely kinematic
  morph cannot represent. It gets position right, not intensity change.
- **Other moments:** the same morph applies to ZDR/KDP/rhov; velocity needs care (it is a
  vector component, not a passive scalar).
- Py-ART 2.x reflectivity colormap is `'ChaseSpectral'` (no `pyart_` prefix).
