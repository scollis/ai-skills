---
name: pyart-foundations
description: Read, inspect and plot weather radar volumes with Py-ART - the Radar object, sweep and scan-strategy anatomy (NEXRAD split cuts, SAILS, VCP detection vs research-radar single-sweep tilts), field naming conventions, extract_sweeps and sweep_number pitfalls, cmweather colormaps, RadarDisplay/RadarMapDisplay/GridMapDisplay, CfRadial/MDV/NEXRAD/SIGMET IO, and xradar DataTree interop. The entry point and router for all Py-ART work. Triggers - Py-ART, pyart, radar volume, PPI, RHI, sweep, tilt, VCP, split cut, SAILS, CfRadial, MDV, Level II, cmweather, RadarDisplay, xradar, radar field names.
---

# Py-ART foundations

Measured against **Py-ART 2.2.5**. Every number here came from running the code on
real volumes, not from documentation. `kernel.py` auto-loads.

Two radar classes are referenced throughout, because they behave differently and
most Py-ART surprises come from assuming one when you have the other:

| | NEXRAD WSR-88D | Research radar (ARM C-SAPR / C-SAPR2 / X-SAPR) |
|---|---|---|
| Sweeps per elevation | **2 or more** (split cuts + SAILS repeats) | 1 |
| Fields per sweep | varies by sweep (5 or 3) | all fields, all sweeps |
| Nyquist | 25-35 m/s, varies per sweep | 16-17 m/s, uniform |
| `normalized_coherent_power` | **absent** | **present** |
| Range gate count | **varies per sweep** | constant |

## 1. Always read the scan anatomy first

A VCP 212 volume is not a stack of unique tilts. Measured on KIWA 2026-08-20 04:14 UTC:
19 sweeps over **14 unique elevations**.

```python
radar = pyart.io.read(path)
print(scan_anatomy(radar).to_string(index=False))   # kernel.py helper
```

```
 sweep  elev  nrays  kind  nfields  split_partner
     0  0.48    720  surv        5              1     <- Z, ZDR, RhoHV, PhiDP, (SW)
     1  0.48    720   dop        3              0     <- V, SW only
     2  0.88    720  surv        5              3
     3  0.88    720   dop        3              2
     ...
     9  0.48    720  surv        5             10     <- SAILS supplemental repeat
    11  4.00    360 batch        7             -1     <- all fields above the split-cut region
```

**Consequence.** Dual-pol algorithms belong on the surveillance members; velocity work
belongs on the Doppler members. Handing the raw volume to a KDP retrieval silently
processes Doppler tilts that carry no ZDR.

```python
surv = dedup_split_cuts(radar, prefer="surv")   # one index per unique elevation
dop  = dedup_split_cuts(radar, prefer="dop")
rs = radar.extract_sweeps(surv)     # dual-pol work
rd = radar.extract_sweeps(dop)      # velocity work
```

A research radar returns one index per tilt from either call — the helper is safe to
run unconditionally.

## 2. `extract_sweeps` does not renumber `sweep_number` — reset it

This is the single most common silent failure in the toolkit.

```python
radar.sweep_number["data"]   # [0 1 2 ... 18]
rs = radar.extract_sweeps([0, 2, 4, 6, 7, 8, 11, ...])
rs.sweep_number["data"]      # [0 2 4 6 7 8 11 ...]   <-- ORIGINAL numbers, 14 entries
```

Anything that loops `for sweep in radar.sweep_number["data"]` then calls
`radar.get_slice(sweep)` now indexes past the end:

```
IndexError: ('Sweep out of range: ', np.int32(14))
```

Confirmed to hit `composite_reflectivity` and `storm_relative_velocity`. Fix once,
immediately after extracting:

```python
rs = radar.extract_sweeps(surv)
renumber_sweeps(rs)      # kernel.py: sweep_number["data"] = arange(nsweeps)
```

## 3. Field names: check, don't assume

Py-ART's canonical names live in `pyart.default_config`. What a file actually
contains depends on the reader and the instrument.

```python
print(sorted(radar.fields))
field_report(radar)     # kernel.py: name, units, valid fraction, p1/p99 per field
```

NEXRAD Level II gives:
`reflectivity, velocity, spectrum_width, differential_reflectivity,
differential_phase, cross_correlation_ratio, clutter_filter_power_removed`

MC3E C-SAPR MDV gives the same core plus `normalized_coherent_power` and
**pre-computed** `specific_differential_phase`. A shipped KDP is not necessarily the
one you want — recomputing on C-SAPR gave a visibly different distribution
(see `pyart-dualpol-phase`).

Functions with field-name defaults that don't match your data fail with a bare
`KeyError: Field not available: <name>`. The worst offender:
`moment_and_texture_based_gate_filter` defaults to `uncorrected_differential_phase`.
Pass field names explicitly whenever a function accepts them.

## 4. Reading data

```python
radar = pyart.io.read(path)                    # sniffs format
radar = pyart.io.read_nexrad_archive(path)     # Level II
radar = pyart.io.read_mdv(path)                # MDV (181 MB -> 1.4 s)
radar = pyart.io.read_cfradial(path)
```

`pyart.io.read` handles CfRadial, MDV, SIGMET, UF, NEXRAD archive/CDM, GAMIC, ODIM,
Rainbow, CHL. Writing: `write_cfradial` (3.5 s for a 14-sweep volume),
`Grid.write`, `write_grid_geotiff` (**needs GDAL**, absent from a plain conda env —
`MissingOptionalDependency`).

### xradar interop and the NEXRAD alignment trap

```python
import xradar
dtree = xradar.io.open_nexradlevel2_datatree(path)     # 2.2 s
xr_radar = pyart.xradar.Xradar(dtree)                  # AlignmentError on NEXRAD
```

```
AlignmentError: cannot reindex or align along dimension 'range'
because of conflicting dimension sizes: {1832, 1712, 1536, ...}
```

Each NEXRAD sweep has its own gate count — 19 sweeps, 19 different `range` sizes
(1832, 1192, 1832, 1192, 1712, ... 240). The `Xradar` accessor needs a common range
axis. Subset to sweeps that share one, or stay in the native Py-ART `Radar` object.
Research-radar CfRadial usually aligns fine.

## 5. Plotting

House convention: **cmweather colormaps** for colour-mapped geophysical quantities.
`import cmweather` registers them with matplotlib. Names are case-sensitive:

| Available | Use for |
|---|---|
| `ChaseSpectral` | reflectivity, KDP, attenuation, rain rate |
| `balance` | velocity (diverging, zero-centred) |
| `plasmidis` | RhoHV, correlation-type quantities — note the spelling, **not** `plasmidic` |
| `HomeyerRainbow`, `LangRainbow12`, `SpectralExtended` | alternatives for Z |

The three display classes:

- `RadarDisplay` — native coordinates: `plot_ppi`, `plot_rhi`, `plot_vpt`,
  `plot_azimuth_to_rhi`, `plot_cr_raster`, `plot_range_rings`
- `RadarMapDisplay` — georeferenced PPI: `plot_ppi_map` plus map annotations
- `GridMapDisplay` — gridded output: `plot_grid`, `plot_latitude_slice`,
  `plot_cross_section`, `plot_maxcappi`

A minimal georeferenced PPI:

```python
import cmweather                                     # registers, no direct calls
setup_cartopy_cache("cartopy_data")                  # kernel.py — REQUIRED first
disp = pyart.graph.RadarMapDisplay(radar)
disp.plot_ppi_map("reflectivity", sweep=0, ax=ax, vmin=-10, vmax=65,
                  cmap="ChaseSpectral", gatefilter=gf)
```

**Anything beyond that minimal call belongs to `pyart-mapping`** — projection choice,
the `PlateCarree` vs `Geodetic` datum trap that displaces data by 21 km, verifying
georeferencing against the cone of silence, geodesic range rings, `grid_origin`,
multi-panel composition, and the annotation methods that don't take an `ax` kwarg.
Load it before writing any figure you intend to keep.

## 6. Where to go next

| Task | Skill |
|---|---|
| Maps, projections, range rings, georeferencing checks | `pyart-mapping` |
| Masking clutter, noise, non-meteorological gates | `pyart-gatefilter-qc` |
| Unfolding aliased velocity | `pyart-velocity-dealias` |
| KDP, PhiDP, attenuation correction | `pyart-dualpol-phase` |
| Cartesian grids, radius of influence, multi-radar | `pyart-gridding` |
| Rain rate, echo classification, hydrometeor ID, CAPPI/QVP/CFAD | `pyart-retrievals` |
| The ARM CMAC VAP specifically | `cmac-vap` |

Start with `pyart-gatefilter-qc` regardless of the eventual goal. Gate filtering
drives the numbers every later step produces: across six QC recipes on one volume,
mean rain rate spanned 2.28-4.39 mm/h.

## 7. Utility inventory

Measured on a 14-sweep NEXRAD surveillance volume.

| Function | Runtime | Note |
|---|---|---|
| `pyart.util.subset_radar` | fast | range/azimuth/elevation subsetting |
| `pyart.util.cross_section_ppi` | <0.1 s | pseudo-RHI from PPI azimuths |
| `pyart.util.column_vertical_profile` | 0.02 s | profile over a lat/lon — the ARM-site tool |
| `pyart.util.get_field_location` | 1.05 s | all fields at one lat/lon |
| `pyart.util.join_radar` | — | concatenate two volumes |
| `pyart.util.image_mute_radar` | — | non-meteorological masking for display |
| `pyart.util.texture_along_ray` | — | generic along-ray texture |
| `pyart.util.determine_sweeps` | fails | `TypeError: NoneType does not support item assignment` |

## Verified against

Py-ART 2.2.5. Scan anatomy, split-cut dedup and sweep renumbering re-run on KIWA 2026-08-20 04:14 UTC (19 sweeps, 14 unique elevations) and ARM SGP C-SAPR MC3E 2011-05-20 11:29 UTC (17 tilts).

Last re-run: 2026-08-26.
