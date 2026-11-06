---
name: blender-landscape-realism
description: >
  Use when building or reviewing a realistic outdoor/landscape scene in Blender Cycles (farms, field sites, instrument deployments): lighting, haze, materials, vegetation, terrain, animation.
---

# Realistic landscape recipe (Cycles)

Distilled from the SERF farm + ARM AMF2 scene and the KAWG (Washington IA) airport site scene. Pairs with `blender-remote-mcp` for the mechanics.

## Light and atmosphere
- Sun lamp ~5 W/m^2-equivalent at the real elevation for the date/site; physical sky (MULTIPLE_SCATTERING). Check balance with a gray card: sky diffuse share ~14 % on a horizontal surface.
- View transform AgX with "Medium High Contrast" look, exposure ~+0.35.
- Distance haze: ONE homogeneous volume box only (stacked boxes or height-falloff densities streak in Blender 5). Farm: +-80 km wide, 1 km tall, density ~1.3e-4. Airport scene: 160 km wide, 4 km tall, density 6e-5 (a short slab gives a hard band at the horizon). Anisotropy ~0.6, absorption 0.
- Clouds: shared GN cloud field + invisible shadow-only copy. Widen the world cloud fade (MapRange smoothstep, From Max ~0.22) or clouds streak at the horizon.

## Real-site scenes (geo-referenced)
- Frame: local metres in UTM, origin at a surveyed point (e.g. FAA ARP), Z = 0 at lidar ground there; store the frame as JSON in a scene custom prop.
- Data: NAIP 0.6 m via USGS ImageServer exportImage in 1000 px tiles (4000 px requests 502), 3DEP 1 m DEM, wide ring at 6 m/30 m, OSM for taxiways/roads (OSM building footprints can be ~8 m off; trace buildings on NAIP), 3DEP lidar EPT (laspy+lazrs) for heights, USDA CDL for crop rotation forecasts.
- Lidar answers "where is it really": published station coordinates are often rounded (the KAWG AWOS coordinate fell on a runway); search lidar returns 3-25 m HAG for isolated masts, confirm on NAIP (pads, mown circles). Filter lidar noise (HAG < 70 m with no structure beneath).
- Radar siting / blockage: per-azimuth max elevation angle from lidar with 4/3-earth refraction, 3rd-highest return per 0.5 deg bin; report degrees of azimuth blocked above the requirement (e.g. 1 deg). Check FAA Part 77 transitional surfaces near runways.
- Farmers' fields: don't put instruments in row crops; infields can be farmed (check CDL).

## Physically plausible materials
- Dielectrics metallic 0; bare metals metallic 1. Cap white albedo ~0.78. Gravel pads: NAIP shows them bright, but under scene lighting limestone gravel needs base ~0.3-0.4 or it reads as concrete.
- Pavement: NAIP colour x tiling concrete detail x ~0.56-0.7 darkening + noise stains.
- Gravel: displacement or bump; raise pads a few cm and cut the lawn mesh out at the pad edge.
- Fabric: roughness ~0.8 + sheen, mix ~20 % Translucent.
- Avoid z-fighting/floating decals on uneven pads (cable-trench strips cast hard black shadows); drop them rather than fake them.

## Vegetation and ground
- Crops/trees as GN Instance-on-Points; per-instance colour via Object Info Random; bake tree leaf GN into plain meshes (nested instancing explodes memory).
- Natural lawn: Poisson-distributed blades, random rotation/tilt, noise-driven patches and tufts; NO mowing stripes for airfield/site grass (stripes read as rows). Density-factor floor ~0.75.
- When adding a site inside a crop field, rebuild the crop point cloud without points in the mown area (numpy filter of the mesh + copy POINT attributes) and lay a lawn mesh there.

## Terrain
- One TerrainHeight node group shared by conform modifier and instancers (or return 0 when points already sit on lidar ground).
- Midwest roll: low-frequency noise (~2 km features, ~12 m relief) plus smaller noise; flat mask around the built area.
- Place assets with z from the DEM at their footprint (75th percentile under pads; average of gear contact points for vehicles, plus pitch/roll from the contact heights).

## Animation details that sell it
- Flags: procedural GN travelling wave; fly downwind consistent with crop/tree sway.
- People: posed figures swapped by visibility at the action frame.
- Key events happen while the camera is looking, against sky.

## Review checklist before a final render
- Close-up of every edge where two ground materials meet, and of every newly placed asset.
- One frame from the actual camera at the moment each feature is closest.
- Time one final-quality frame and give the user an ETA.