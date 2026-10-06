"""Helpers for cropland ET measurement and interpretation."""
import os
import sys

LAMBDA_MJ_PER_KG = 2.45
MM_PER_DAY_IN_W_PER_M2 = 28.4
ARM_FETCH_RATIOS = (("ecor", 70.0), ("ebbr", 40.0))


def et_skill_dir():
    """Directory this skill was loaded from, or None if unresolvable."""
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    return here or None


def et_units(value, frm="W/m2", to="mm/day", lam=None):
    """Convert between LE energy flux and ET water flux.

    Units: 'W/m2', 'mm/day', 'MJ/m2/day', 'mm/hour', 'kg/m2/s'.
    lam defaults to the FAO-56 latent heat of vaporisation, 2.45 MJ/kg.
    """
    if lam is None:
        lam = LAMBDA_MJ_PER_KG
    to_wm2 = {
        "W/m2": 1.0,
        "mm/day": (lam * 1e6) / 86400.0,
        "MJ/m2/day": 1e6 / 86400.0,
        "mm/hour": (lam * 1e6) / 3600.0,
        "kg/m2/s": lam * 1e6,
    }
    for unit in (frm, to):
        if unit not in to_wm2:
            raise ValueError("unknown unit %r; use one of %s"
                             % (unit, sorted(to_wm2)))
    return value * to_wm2[frm] / to_wm2[to]


def closure_variants(h, le, rn, g):
    """Return H and LE under all four energy-balance closure conventions.

    Keys: 'none', 'bowen' (Twine 2000), 'buoyancy' (Charuchittipan 2014),
    'residual_le'. Also returns the residual and the energy balance ratio.
    Scalars or numpy arrays. See SKILL.md for when each is defensible.
    """
    available = rn - g
    residual = available - (h + le)
    out = {"residual": residual,
           "ebr": (h + le) / available,
           "none": {"H": h, "LE": le}}
    scale = available / (h + le)
    out["bowen"] = {"H": h * scale, "LE": le * scale}
    # Buoyancy weighting f = Hb/(H+LE) with Hb ~ H + 0.07*LE (Charuchittipan 2014)
    fb = (h + 0.07 * le) / (h + le)
    out["buoyancy"] = {"H": h + fb * residual, "LE": le + (1.0 - fb) * residual}
    out["residual_le"] = {"H": h, "LE": available - h}
    return out


def footprint_geometry(canopy_height_m, meas_height_m):
    """Roughness geometry and ARM fetch requirements over a crop canopy.

    d = 0.67 h, z0 = 0.1 h. Returns effective height above the displacement
    plane and the fetch each ARM siting ratio demands. Recompute at least
    biweekly through the growing season - a fixed d is wrong by ~2x between
    bare soil and tasselling maize.
    """
    d = 0.67 * canopy_height_m
    z0 = 0.1 * canopy_height_m
    zeff = meas_height_m - d
    out = {"canopy_height_m": canopy_height_m, "meas_height_m": meas_height_m,
           "displacement_height_m": d, "roughness_length_m": z0,
           "effective_height_m": zeff}
    for name, ratio in ARM_FETCH_RATIOS:
        out["fetch_%s_m" % name] = ratio * meas_height_m
    if zeff <= 0:
        out["warning"] = "measurement height is below the displacement plane"
    return out


def et_magnitudes(quantity=None, crop=None, site=None):
    """Bundled table of measured Midwest cropland ET and flux magnitudes.

    Case-insensitive substring filters on the quantity, crop_or_cover and
    site columns. Every row carries source_doi - quote it.
    """
    import pandas as pd
    here = et_skill_dir()
    if here is None:
        raise RuntimeError("skill directory unavailable in this runtime")
    df = pd.read_csv(os.path.join(here, "midwest_cropland_et_magnitudes.csv"))
    for col, val in (("quantity", quantity), ("crop_or_cover", crop),
                     ("site", site)):
        if val:
            df = df[df[col].str.contains(val, case=False, na=False)]
    return df.reset_index(drop=True)
