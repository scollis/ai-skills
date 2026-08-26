---
name: cmac-vap
description: Run and understand the ARM CMAC 2.0 VAP (Corrected Moments in Antenna Coordinates) for scanning radar - its per-radar config system and fuzzy membership functions, do_my_fuzz gate classification into no_scatter/multi_trip/rain/snow/melting/clutter, snr_and_sounding profile ingest, get_texture, the CSU Bringi FIR KDP path, clutter retrieval and beam blockage, gate_id-derived GateFilters, and the VAP call order and field-naming conventions. Separate from the pyart-* skills - CMAC is a consumer of Py-ART, not part of it. Triggers - CMAC, cmac2.0, corrected moments antenna coordinates, ARM VAP, gate_id, do_my_fuzz, fuzzy gate classification, radar clutter retrieval, beam blockage, csu_kdp, Bringi KDP, ARM radar processing, cacti csapr2, cmac config.
---

# CMAC 2.0 — the ARM corrected-moments VAP

CMAC 2.0 is ARM's production quality-control and retrieval VAP for scanning
precipitation radars. It **consumes** Py-ART; it is not part of it. For the underlying
Py-ART algorithms load the `pyart-*` skills — this skill covers CMAC's own machinery.

Verified against `github.com/ARM-Development/cmac` (note the org: there is no
`ARM-DOE/CMAC2.0`) on ARM SGP C-SAPR, MC3E 2011-05-20 11:29 UTC.

## 1. Install

```bash
git clone https://github.com/ARM-Development/cmac.git
```

Runtime dependencies beyond Py-ART: `scikit-fuzzy`, `wradlib`, `pyyaml`, `cython`,
`coincbc`. There is a Cython extension (`cmac/calc_kdp_ray_fir.pyx`) that must be
built, so an editable install is required — a plain `sys.path` insert will import the
package but fail at the KDP call:

```bash
pip install -e . --no-build-isolation --no-deps
```

## 2. Public surface

| Module | Key entry points |
|---|---|
| `cmac_radar.py` | `cmac(radar, sonde, config, ...)` — the whole VAP |
| `cmac_processing.py` | `do_my_fuzz`, `snr_and_sounding`, `get_texture`, `get_melt`, `return_csu_kdp`, `fix_phase_fields`, `retrieve_qvp`, `cum_score_fuzzy_logic` |
| `gate_id.py` | `get_gate_id_categories`, `gate_id_has_category` |
| `radar_clutter.py` | `gen_clutter_field_from_refl`, `beam_block`, `tall_clutter` |
| `config.py` / `default_config.py` | per-radar config lookup |
| `csu_kdp.py` | `calc_kdp_bringi` — FIR KDP |

## 3. The config system

`default_config.py` holds six top-level dictionaries keyed by a **radar config name**
(e.g. `cacti_csapr2_ppi`, `bnf_csapr2_ppi`, `sgpxsaprI4`):

| Dict | Contents |
|---|---|
| `_DEFAULT_METADATA` | VAP-level netCDF metadata |
| `_DEFAULT_FIELD_NAMES` | mapping from CMAC's internal names to the radar's actual field names |
| `_DEFAULT_CMAC_VALUES` | per-radar thresholds, `save_name`, sounding stream, ranges |
| `_DEFAULT_PLOT_VALUES` | quicklook field lists and limits |
| `_DEFAULT_ZS_RELATIONSHIPS` | Z-S coefficients |
| `_DEFAULT_PROCESSING_TUNABLES` | texture windows, fuzzy break points |

Plus standalone membership-function dicts, one per radar/scan combination:
`cacti_csapr2_ppi_mbfs`, `cacti_csapr2_ppi_hard_const`, and siblings.

**Adding a radar means adding a key to each dict**, not editing code. That is the
design worth copying if you build your own VAP.

## 4. The fuzzy gate classifier

`do_my_fuzz` is CMAC's distinguishing feature: rather than thresholding, it scores each
gate's membership in physical categories and takes the argmax.

```python
gid, cats = cmac.do_my_fuzz(radar, rhv_field, ncp_field,
                            tex_start=2.0, tex_end=2.1, verbose=False)
radar.add_field("gate_id", gid, replace_existing=True)
cats_map = cmac.gate_id.get_gate_id_categories(radar.fields["gate_id"])
```

Measured on the C-SAPR volume (2.7 s, 6.0M gates):

| Category | Gates |
|---|---|
| `no_scatter` | 2,225,646 |
| `snow` | 1,832,541 |
| `rain` | 1,566,861 |
| `multi_trip` | 252,320 |
| `melting` | 138,592 |

**Field-name trap.** The shipped MBF dicts key on CMAC's *internal* names
(e.g. `copol_correlation_coeff`), but `do_my_fuzz` renames those to the radar's actual
field names as it builds the membership functions. Passing a shipped dict straight
through as `custom_mbfs=` therefore raises a `KeyError`:

```python
# WRONG - KeyError on the internal name
cmac.do_my_fuzz(radar, ..., custom_mbfs=cmac.default_config.cacti_csapr2_ppi_mbfs)

# RIGHT - let it build the MBFs, and tell it your field names
cmac.do_my_fuzz(radar, "cross_correlation_ratio", "normalized_coherent_power",
                tex_start=2.0, tex_end=2.1)
```

To genuinely customise, re-key the dict to your radar's field names first.

**`normalized_coherent_power` is required and NEXRAD does not have it.** CMAC targets
ARM research radars. On a WSR-88D you must substitute a different confidence field or
drop the NCP term.

### gate_id → GateFilter

The idiomatic conversion, and the reason CMAC's output is useful downstream:

```python
gf = pyart.filters.GateFilter(radar)
gf.exclude_all()
gf.include_equal("gate_id", cats_map["rain"])
gf.include_equal("gate_id", cats_map["melting"])
gf.include_equal("gate_id", cats_map["snow"])
```

`exclude_all()` then `include_equal(...)` is the correct include-based idiom — see
`pyart-gatefilter-qc` for why mixing in an `exclude_*` call here would undo it.

**This filter alone is not sufficient for velocity dealiasing.** On the C-SAPR volume
it produced ±366 m/s (22× the 16.52 m/s Nyquist) from region-based dealiasing; adding
a single velocity-texture criterion brought it to ±48 m/s. Full treatment in
`pyart-velocity-dealias`.

## 5. Sounding ingest

```python
z_dict, temp_dict, snr_dict = cmac.snr_and_sounding(radar, sonde_dir,
                                                    override_file=path, verbose=False)
```

Two things measured on the MC3E case, both of which will bite:

1. **The stream CMAC expects by filename pattern may be unusable at your radar time.**
   `sgpgriddedsondeC1.c0` was −9999 across all 332 levels at 11:29 UTC, which crashes
   the profile mapping with `ValueError: cannot reshape array of size 0`.
   `sgpinterpolatedsondeC1.c1` had 227 valid levels to 10.2 km with 0 °C at 4.02 km.
   **Verify coverage at the radar time before running the VAP.**
2. Fill values propagate. `pyart.retrieve.fetch_radar_time_profile` returns raw
   `-9999`; mask below −500 before `map_profile_to_gates`.

## 6. Texture and KDP

```python
tex = cmac.get_texture(radar, "velocity", window=4, median_size=(4, 4))
kdp, phidp, _ = cmac.return_csu_kdp(radar)     # 1.6 s, full 17-sweep volume
```

`return_csu_kdp` wraps `calc_kdp_bringi` (FIR). Measured: 54.3% valid gates, median
0.150, p99 1.75 deg/km — physically plausible and roughly 100× faster than Py-ART's
Kalman-filter method. It expects PhiDP unfolded first (`fix_phase_fields`); values
below 0 need +360 on this volume.

CMAC does **not** use `pyart.correct.phase_proc_lp_gf`, and that is the right call —
that function is broken upstream. See `pyart-dualpol-phase`.

## 7. Clutter and blockage

`gen_clutter_field_from_refl` builds a clutter field from a long-term reflectivity
composite; `tall_clutter` targets tall ground targets; `beam_block` uses `wradlib`
terrain data for partial beam blockage. These need auxiliary inputs (a clutter
climatology, a DEM) and are the part of CMAC least portable to a new site.

## 8. Reading CMAC as a Py-ART reference implementation

CMAC's value beyond running it is that it is a **production VAP whose call order has
been debugged against years of real data**. What it demonstrates:

- Sounding-derived temperature and height fields are added to the radar object
  *before* any classification.
- Texture is computed once and reused, not recomputed per algorithm.
- Gate classification happens before dealiasing, attenuation and QPE — everything
  downstream consumes one authoritative gate mask.
- A fast FIR KDP is preferred over the variational and LP methods for operational
  throughput.
- Every field name is configuration, never a literal.

Those lessons are folded into the `pyart-*` skills. This skill is the only place
CMAC's own machinery is documented.

## Verified against

CMAC 2.0 at github.com/ARM-Development/cmac, run against ARM SGP C-SAPR MC3E 2011-05-20 11:29 UTC with sgpinterpolatedsondeC1.c1. Gate-ID category counts and the FIR KDP distribution are from that volume.

Last re-run: 2026-08-26.
