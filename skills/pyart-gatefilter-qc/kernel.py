"""Helpers for pyart-gatefilter-qc: named QC recipes, marginal cost, shape assertions."""


def assert_filter_matches(gatefilter, radar):
    """Raise ValueError if a GateFilter's shape doesn't match the radar it will be used on.

    Py-ART SILENTLY accepts a parent-radar filter on an extract_sweeps child and shifts
    gridded means to a plausible-looking wrong value (18.40 -> 13.04 dBZ measured).
    Call before every grid_from_radars / retrieval that takes a gatefilter.
    """
    want = (radar.nrays, radar.ngates)
    got = tuple(gatefilter.gate_excluded.shape)
    if got != want:
        raise ValueError(
            f"gatefilter shape {got} != radar shape {want}. "
            "Build the filter on the radar object you actually pass "
            "(extract_sweeps children need their own filter)."
        )
    return True


def qc_recipe(radar, name="dualpol", rhv_min=0.85, refl_min=0.0,
              texture_max=3.0, ncp_min=None):
    """Return a named GateFilter recipe. name: permissive|dualpol|strict|velocity.

    'permissive' - invalid + rhoHV 0.80. Keeps weak echo; use when coverage matters.
    'dualpol'    - invalid + rhoHV + Z floor + ZDR sanity. General-purpose default.
    'strict'     - dualpol with rhoHV 0.95 and a higher Z floor.
    'velocity'   - invalid velocity + velocity_texture ceiling; REQUIRED before
                   region-based dealiasing (see pyart-velocity-dealias).

    ncp_min applies only on radars carrying normalized_coherent_power (research
    radars); it is silently skipped on NEXRAD, which has no such field.
    """
    import pyart
    gf = pyart.filters.GateFilter(radar)
    if name == "velocity":
        gf.exclude_invalid("velocity")
        if "velocity_texture" in radar.fields:
            gf.exclude_above("velocity_texture", texture_max)
        return gf
    gf.exclude_invalid("reflectivity")
    if name == "permissive":
        gf.exclude_below("cross_correlation_ratio", 0.80)
        return gf
    if name == "strict":
        rhv_min, refl_min = 0.95, max(refl_min, 5.0)
    gf.exclude_below("cross_correlation_ratio", rhv_min)
    gf.exclude_below("reflectivity", refl_min)
    if "differential_reflectivity" in radar.fields:
        gf.exclude_outside("differential_reflectivity", -4, 6)
    if ncp_min is not None and "normalized_coherent_power" in radar.fields:
        gf.exclude_below("normalized_coherent_power", ncp_min)
    return gf


def marginal_cost(radar, criteria=None):
    """DataFrame of solo / cumulative / marginal exclusion fraction per criterion.

    Shows which criteria actually do work on YOUR volume. On NEXRAD the no-echo mask
    dominates (0.838 measured) and everything after is a few points; exclude_transition
    is a silent no-op there (no antenna_transition field).
    """
    import pandas as pd
    import pyart
    if criteria is None:
        criteria = [
            ("exclude_invalid(Z)", lambda g: g.exclude_invalid("reflectivity")),
            ("exclude_below(rhoHV,0.85)",
             lambda g: g.exclude_below("cross_correlation_ratio", 0.85)),
            ("exclude_below(Z,0)", lambda g: g.exclude_below("reflectivity", 0)),
            ("exclude_outside(ZDR,-4,6)",
             lambda g: g.exclude_outside("differential_reflectivity", -4, 6)),
            ("exclude_transition()", lambda g: g.exclude_transition()),
            ("exclude_above_toa(15km)", lambda g: g.exclude_above_toa(15000.0)),
        ]
    rows = []
    cum = pyart.filters.GateFilter(radar)
    prev = float(cum.gate_excluded.mean())
    for label, fn in criteria:
        solo = pyart.filters.GateFilter(radar)
        fn(solo)
        fn(cum)
        now = float(cum.gate_excluded.mean())
        rows.append(dict(criterion=label,
                         solo=round(float(solo.gate_excluded.mean()), 4),
                         cumulative=round(now, 4),
                         marginal=round(now - prev, 4)))
        prev = now
    return pd.DataFrame(rows)


def sector_ring_mask(radar, az_ranges=(), range_ranges_m=()):
    """Boolean (nrays, ngates) mask for exclude_gates: sector blanking + range rings.

    az_ranges: [(az_start_deg, az_end_deg), ...] blanks whole azimuth sectors and
    handles wrap-around when start > end. range_ranges_m: [(r_min, r_max), ...] removes
    range rings (test-signal artefacts, second-trip rings). Pass the result to
    gatefilter.exclude_gates(mask).
    """
    import numpy as np
    az = radar.azimuth["data"]
    rng = radar.range["data"]
    mask = np.zeros((radar.nrays, radar.ngates), dtype=bool)
    for a0, a1 in az_ranges:
        sel = (az >= a0) & (az <= a1) if a0 <= a1 else (az >= a0) | (az <= a1)
        mask |= sel[:, None]
    for r0, r1 in range_ranges_m:
        mask |= ((rng > r0) & (rng < r1))[None, :]
    return mask


def add_lapse_rate_temperature(radar, surface_temp_c=20.0, lapse_c_per_km=6.5,
                               field_name="temperature"):
    """Add a crude standard-atmosphere temperature field on gate altitudes, in place.

    For TESTING the thermal gate filters and classification chains only. Real work
    needs a sounding - see pyart-retrievals for map_profile_to_gates and the
    fill-value trap.
    """
    import numpy as np
    z = radar.gate_altitude["data"]
    alt0 = float(radar.altitude["data"][0])
    t = surface_temp_c - lapse_c_per_km * (z - alt0) / 1000.0
    radar.add_field(field_name,
                    {"data": np.ma.masked_invalid(t), "units": "degC",
                     "standard_name": "temperature", "long_name": "temperature"},
                    replace_existing=True)
    return radar


def qc_sensitivity(radar, recipes=("permissive", "dualpol", "strict")):
    """DataFrame of excluded fraction and kept-gate count per named recipe.

    The spread is what you must report alongside any mean. Measured across six recipes
    on one NEXRAD volume: mean rain rate 2.28-4.39 mm/h, gridded mean Z 8.37-12.40 dBZ,
    while grid MAXIMUM was 58.4 dBZ in all six. Peaks are QC-robust, means are not.
    """
    import pandas as pd
    rows = []
    for name in recipes:
        gf = qc_recipe(radar, name)
        rows.append(dict(recipe=name,
                         excluded=round(float(gf.gate_excluded.mean()), 4),
                         kept_gates=int((~gf.gate_excluded).sum())))
    return pd.DataFrame(rows)
