---
name: pyart-velocity-dealias
description: Unfold aliased Doppler velocity in Py-ART - why region-growing dealiasing amplifies a few leaked QC gates into a whole-region error (measured 22x Nyquist from one missing criterion), choosing between dealias_region_based and dealias_unwrap_phase and why dealias_fourdd is a dead end, calculate_velocity_texture settings and the check_nyq_uniform requirement on split-cut volumes, Nyquist handling for NEXRAD versus uniform-Nyquist research radars, reference velocity from a sounding wind profile and masking its unbounded extrapolation above profile top, and verifying with a max|v|/Nyquist ratio. Triggers - dealias, dealiasing, velocity unfolding, aliasing, folded velocity, dealias_region_based, dealias_unwrap_phase, dealias_fourdd, corrected_velocity, Nyquist, velocity_texture, calculate_velocity_texture, ref_vel_field, simulated_vel_from_profile, HorizontalWindProfile, Doppler velocity QC, radial velocity.
---

# Velocity dealiasing in Py-ART

Measured against **Py-ART 2.2.5** on a NEXRAD VCP-212 volume (KIWA 2026-08-20
04:14 UTC, 19 sweeps with SAILSx1 and split cuts, per-sweep Nyquist 25.0-34.7 m/s,
no `normalized_coherent_power`) and an ARM SGP C-SAPR MDV volume (MC3E 2011-05-20
11:29 UTC, 17 tilts, one sweep per elevation, 120 m gates to 118 km, uniform
Nyquist 16.52 m/s, NCP present). `kernel.py` auto-loads.

---

## 1. The headline: dealiasing amplifies QC leakage

`dealias_region_based` segments the velocity field into connected regions of
similar velocity and assigns each region an integer number of Nyquist intervals.
The unfolding decision is made **per region, not per gate**. A thin bridge of
noisy gates connecting two genuinely aliased regions merges them into one region,
and one wrong integer is then applied to every gate in it.

Same volume, same call, same algorithm on C-SAPR. Only the gate filter changed:

| Gate filter fed to the dealiaser | Resulting `corrected_velocity` range | Ratio to 16.52 m/s Nyquist | Runtime |
|---|---|---|---|
| Echo classification only | -366.6 to +182.4 m/s | **22x** | 1.1 s |
| Same, plus `velocity_texture < 3` | -33.5 to +48.1 m/s | 2.9x | 0.9 s |

The texture criterion excluded **0.7 percentage points** more gates than the
classification-only filter. That 0.7 points is the difference between a usable
wind field and one with 22x-Nyquist garbage smeared across whole regions.

**Velocity QC has a far lower tolerance for leaked gates than dual-pol QC does.**
A filter that leaves 1% non-meteorological echo is fine for a KDP or rain-rate
retrieval - the bad gates stay local and mostly average out. In region-based
dealiasing they are connectivity, and connectivity is global. Never reuse a
reflectivity-grade gate filter for velocity work without adding a
velocity-derived criterion.

Corollary on the API: `gatefilter=None` (**not** the default) makes the dealiaser
build its own `moment_based_gate_filter`. That filter has no velocity-texture
criterion, so it is exactly the failure mode above. Pass your own `GateFilter`
explicitly. `gatefilter=False`, the default, applies no filtering at all.

---

## 2. Choosing a dealiaser

| Function | Measured on KIWA (14 sweeps) | Behaviour |
|---|---|---|
| `pyart.correct.dealias_region_based` | 1.69 s; changed 0.44% of gates; range -34.1 to +27.5 m/s (1.0x Nyquist) | Region growing. Conservative when fed clean gates; catastrophic when not (section 1). Default choice. |
| `pyart.correct.dealias_unwrap_phase` | 0.76 s; changed 4.54% of gates; produced 62.6 m/s (**2.2x Nyquist**) | 2D/3D phase unwrapping. Roughly twice as fast, markedly less conservative - it unfolded 10x as many gates and pushed the maximum past 2x Nyquist on the same volume region-based kept at 1.0x. Inspect before trusting. |
| `pyart.correct.dealias_fourdd` | not runnable | **Deprecated in Py-ART 2.0** and requires the TRMM RSL library, which is not conda-installable. Do not route users here, do not write recipes around it, and do not suggest building RSL from source as a workaround - the two functions above supersede it. |

`dealias_unwrap_phase` has an `unwrap_unit` argument (`'sweep'`, `'ray'`,
`'volume'`). It is a reasonable second opinion: if the two dealiasers disagree
about a region, the region is ambiguous and neither answer is trustworthy.

---

## 3. The velocity texture gate

`pyart.retrieve.calculate_velocity_texture` computes the standard deviation of
velocity in a moving window and is the criterion that saves region-based
dealiasing.

```python
vt = pyart.retrieve.calculate_velocity_texture(
    radar,
    vel_field="velocity",
    wind_size=3,               # measured setting; 3x3 gate window
    check_nyq_uniform=False,   # REQUIRED on split-cut volumes
)
radar.add_field("velocity_texture", vt, replace_existing=True)
gatefilter.exclude_above("velocity_texture", 3.0)
```

- `wind_size=3` on a 14-sweep NEXRAD volume: **0.92 s**. Cheap relative to
  everything downstream (`despeckle_field` at `size=20` costs 15.02 s on the
  same volume).
- `check_nyq_uniform=False` is **required** on any volume whose per-sweep Nyquist
  varies - i.e. every NEXRAD split-cut volume, where the surveillance and Doppler
  cuts differ (25.0-34.7 m/s on KIWA). Leaving it `True` raises on the
  non-uniformity instead of computing texture.
- Watch the spelling. Texture takes `check_nyq_uniform`; the dealiasers take
  `check_nyquist_uniform`. They are not interchangeable and a typo lands in
  `**kwargs`-free signatures as a `TypeError`.
- The threshold of 3 m/s is what was measured to work at 16.52 m/s Nyquist. Scale
  it with Nyquist rather than transplanting the literal: a research C-band radar
  at 16.52 m/s and a WSR-88D at 34.7 m/s do not have the same texture floor for
  the same physical turbulence.

See `pyart-gatefilter-qc` for how texture composes with the rest of a filter and
what each additional criterion costs.

---

## 4. Nyquist handling - the two radar classes

This is the most common source of user error and it splits cleanly by radar class.

| | NEXRAD WSR-88D (KIWA) | Research radar (ARM C-SAPR) |
|---|---|---|
| Nyquist structure | Varies by sweep, 25.0-34.7 m/s (split cuts, dual-PRF) | Uniform 16.52 m/s across all 17 tilts |
| Dealias call | `nyquist_vel=None, check_nyquist_uniform=False` - let Py-ART read per-sweep values from `instrument_parameters` and stop it from asserting uniformity | Pass the scalar: `nyquist_vel=radar.instrument_parameters["nyquist_velocity"]["data"][0]` |
| Texture call | `check_nyq_uniform=False` | default `True` is fine |

Passing a single scalar `nyquist_vel` on a split-cut NEXRAD volume applies one
sweep's Nyquist to all of them, which mis-scales the unfolding intervals on every
other sweep. Passing `None` on a research radar is harmless but pointless.

Check before you assume:

```python
nyq = radar.instrument_parameters["nyquist_velocity"]["data"]
uniform = float(nyq.min()) == float(nyq.max())
```

---

## 5. Sweep selection - run on the Doppler cuts

On a NEXRAD split-cut VCP the lowest elevations are scanned twice: a long-PRT
surveillance cut carrying reflectivity, and a short-PRT Doppler cut carrying
velocity and spectrum width. Velocity work belongs on the **Doppler members**.
The surveillance members either carry no velocity or carry it at a Nyquist that
does not correspond to the reflectivity you are plotting alongside it.

KIWA VCP 212 with SAILSx1 has 19 sweeps over 14 unique elevations, so the
deduplicated Doppler set used for the dealiasing measurements in this skill is 14
sweeps, and the deduplicated surveillance set is a separate 14. Use
`pyart-foundations` (`dedup_split_cuts`, VCP detection, `extract_sweeps`
renumbering) to select the right subset - and note the `extract_sweeps` trap
documented there and in `pyart-gatefilter-qc`: a `GateFilter` built on the full
volume is silently the wrong shape for an extracted sub-volume.

The C-SAPR volume has no split cuts at all - one sweep per elevation, 0.75-42.0
degrees in 17 tilts. Nothing to deduplicate; do not apply split-cut logic to it.

---

## 6. Reference velocity from a sounding

Both dealiasers accept `ref_vel_field=`: the name of a field holding an expected
radial velocity, used to anchor the unfolding of the first region. The
environmental-wind route:

```python
profile = pyart.core.HorizontalWindProfile.from_u_and_v(height_m, u_ms, v_ms)
sim = pyart.util.simulated_vel_from_profile(radar, profile)   # 0.2 s
radar.add_field("simulated_velocity", sim, replace_existing=True)
```

### The extrapolation trap

**`simulated_vel_from_profile` extrapolates without bound above the top of the
profile you gave it.** On C-SAPR, 38.9% of gates sat above the 10.2 km sounding
top and were assigned simulated velocities of up to **14,080 m/s**. Nothing warns
you; the field is returned looking normal.

Mask it before use:

```python
top = float(profile.height.max())
sim["data"] = numpy.ma.masked_where(radar.gate_altitude["data"] > top, sim["data"])
```

`kernel.py` provides `mask_above_profile_top` for this.

Two further notes on the sounding side, from the ARM streams:

- Interpolated sonde (`sgpinterpolatedsondeC1.c1`) gave 227 valid levels to
  10.2 km. The gridded sonde stream was unusable at that timestamp - `-9999`
  fill on all 332 levels.
- `pyart.util.fetch_radar_time_profile` returns the raw fill values. Mask
  anything below -500 before building the profile, or the whole downstream chain
  inherits `-9999` as a wind speed.

### Report honestly: it may buy you nothing

On the C-SAPR volume, passing `ref_vel_field` produced **no change** in the
dealiased output relative to omitting it - the interval-splitting path dominated
the solution. Build the reference field when you have a trustworthy contemporaneous
sounding and the volume is genuinely ambiguous, not as routine hygiene. Verify
that it changed something (compare `corrected_velocity` with and without) before
claiming it helped.

A radar-derived alternative when no sounding exists: `pyart.retrieve.vad_browning`
or `vad_michelson` (0.43 s, Doppler sweeps only) give a wind profile from the
volume itself, which can be fed back through `HorizontalWindProfile`. That is
circular if the velocities are badly folded, so it only works when the low tilts
are already clean.

---

## 7. Recommended recipe

Order matters: texture is computed on the **raw** velocity field, the filter is
built from it, and only then does the dealiaser run.

```python
import numpy
import pyart

radar = pyart.io.read(path)                      # or read_mdv for C-SAPR MDV

# 1. Doppler sweep subset (NEXRAD split cuts only) - see pyart-foundations.

# 2. Nyquist inspection drives the kwargs.
nyq = radar.instrument_parameters["nyquist_velocity"]["data"]
uniform = float(nyq.min()) == float(nyq.max())

# 3. Texture on the RAW velocity field.
vt = pyart.retrieve.calculate_velocity_texture(
    radar, vel_field="velocity", wind_size=3, check_nyq_uniform=uniform
)
radar.add_field("velocity_texture", vt, replace_existing=True)

# 4. Filter: reflectivity-grade criteria PLUS the velocity criterion.
gf = pyart.filters.GateFilter(radar)
gf.exclude_invalid("velocity")
gf.exclude_invalid("reflectivity")
gf.exclude_masked("reflectivity")
gf.exclude_above("velocity_texture", 3.0)        # scale with Nyquist
# research radars only - NCP does not exist on NEXRAD:
if "normalized_coherent_power" in radar.fields:
    gf.exclude_below("normalized_coherent_power", 0.4)

# 5. Dealias with an EXPLICIT filter, never gatefilter=None.
dealiased = pyart.correct.dealias_region_based(
    radar,
    gatefilter=gf,
    vel_field="velocity",
    nyquist_vel=None if not uniform else float(nyq[0]),
    check_nyquist_uniform=uniform,
    centered=True,
)
radar.add_field("corrected_velocity", dealiased, replace_existing=True)

# 6. Verify before plotting (section 8).
```

`kernel.py`'s `texture_and_dealias` is this sequence with the guards baked in.

Plot with the house colormap: `cmweather` `balance` for velocity, symmetric limits
at the Nyquist you expect (`vmin=-nyq_max, vmax=+nyq_max`), so a folded or
over-unfolded region saturates visibly instead of hiding inside an autoscaled
range. `ChaseSpectral` for reflectivity in the companion panel. See
`pyart-mapping` for `plot_ppi_map` and georeferencing.

---

## 8. Verification - how to know it worked

The single most useful diagnostic is the ratio of the dealiased maximum absolute
velocity to the Nyquist velocity.

```python
ratio = numpy.abs(radar.fields["corrected_velocity"]["data"]).max() / float(nyq.max())
```

Interpreting it, against the measured cases:

| Ratio | Interpretation | Measured example |
|---|---|---|
| ~1.0 | Nothing unfolded, or only single-interval folds. Normal for a weak-wind volume. | KIWA, region-based, clean filter: -34.1 to +27.5 m/s at 34.7 m/s Nyquist |
| 1.5-3 | Plausible for real deep shear or a strong jet, but inspect the PPI before trusting. | KIWA, unwrap-phase: 62.6 m/s (2.2x). C-SAPR with texture: 48.1 m/s (2.9x) |
| >3 | **QC leaked.** Region growing bridged noise. Add or tighten a velocity criterion and re-run; do not post-process the output. | C-SAPR without texture: 366.6 m/s (22x) |

`kernel.py`'s `nyquist_ratio` returns this with the supporting numbers.

Three further checks, in increasing cost:

1. **Fraction of gates changed.** Region-based changed 0.44% on KIWA;
   unwrap-phase changed 4.54% on the same volume. A change fraction in the tens
   of percent on a volume without obvious folding means the algorithm is
   unfolding noise.
2. **Visual continuity across the zero-isodop.** Real velocity is continuous
   through the zero line and across azimuth. A region boundary that coincides
   with a sharp jump of exactly one Nyquist interval is a dealiasing error, not
   weather.
3. **Independent wind profile.** Compare a VAD from the dealiased field against
   the contemporaneous sounding. Disagreement of a full Nyquist interval at some
   altitude localises the failed region.

Report the QC recipe alongside any dealiased product. As with reflectivity QC,
the number is not reproducible without it.

---

## 9. Related skills

| Need | Skill |
|---|---|
| Sweep anatomy, split cuts, `dedup_split_cuts`, `extract_sweeps` renumbering, field naming | `pyart-foundations` |
| GateFilter method semantics, criterion costs, canned filters, despeckle | `pyart-gatefilter-qc` |
| PPI/map plotting, projections, range rings | `pyart-mapping` |
| PhiDP unfolding and KDP - a different unfolding problem with different failure modes | `pyart-dualpol-phase` |
| Gridding dealiased velocity to Cartesian, dual-Doppler prep | `pyart-gridding` |
| VAD, QVP, rain rate and other retrievals downstream of velocity | `pyart-retrievals` |
| The ARM corrected-moments VAP as a product | `cmac-vap` |

## Verified against

Py-ART 2.2.5. Dealiaser comparison re-run on KIWA 2026-08-20 04:14 UTC (Doppler members) and the 22x-Nyquist QC-leakage case on ARM SGP C-SAPR MC3E 2011-05-20 11:29 UTC.

Last re-run: 2026-08-26.
