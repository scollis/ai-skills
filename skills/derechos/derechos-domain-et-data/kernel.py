"""Helpers for DERECHOS domain ET data sources."""
import os
import sys

DERECHOS_ET_BBOX = (-94.6, 40.4, -87.0, 42.7)
ECOSTRESS_LST_WINDOW = (9.0, 15.0)
ECOSTRESS_MIN_VALID_FRAC = 0.10
MOD16_VALID_MAX = 32700
DOMAIN_MEDIAN_ET_JUL2024 = 4.24


def derechos_et_skill_dir():
    """Directory this skill was loaded from, or None if unresolvable."""
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    return here or None


def derechos_et_sources(verified=None, source=None):
    """Bundled 31-row table of candidate ET/flux sources over the domain.

    verified: filter on the 'verified' column ('yes', 'no', 'blocked', ...).
    source: case-insensitive substring on 'source'.
    """
    import pandas as pd
    here = derechos_et_skill_dir()
    if here is None:
        raise RuntimeError("skill directory unavailable in this runtime")
    df = pd.read_csv(os.path.join(here, "derechos_et_sources.csv"))
    if verified:
        df = df[df["verified"].str.contains(verified, case=False, na=False)]
    if source:
        df = df[df["source"].str.contains(source, case=False, na=False)]
    return df.reset_index(drop=True)


def derechos_flux_towers(igbp=None, state=None, has_le=None, near=None):
    """Bundled 68-row AmeriFlux candidate table for the Midwest.

    igbp: e.g. 'CRO' for cropland. state: two-letter code ('IA', not 'Iowa').
    has_le: True keeps only sites with LE in the BASE product.
    near: (lat, lon, km) adds a 'km' column and keeps sites within that range.
    """
    import numpy as np
    import pandas as pd
    here = derechos_et_skill_dir()
    if here is None:
        raise RuntimeError("skill directory unavailable in this runtime")
    df = pd.read_csv(os.path.join(here, "derechos_ameriflux_cropland_sites.csv"))
    if igbp:
        df = df[df["igbp"].astype(str).str.upper() == igbp.upper()]
    if state:
        df = df[df["state"].astype(str).str.upper() == state.upper()]
    if has_le and "le_in_base" in df.columns:
        df = df[df["le_in_base"].astype(str).str.lower().isin(["true", "yes", "1"])]
    if near:
        la, lo, km = near
        dlat = np.radians(df["lat"].values - la)
        dlon = np.radians(df["lon"].values - lo)
        mlat = np.radians((df["lat"].values + la) / 2.0)
        df = df.assign(km=6371.0 * np.hypot(dlat, dlon * np.cos(mlat)))
        df = df[df["km"] <= km].sort_values("km")
    return df.reset_index(drop=True)


def ecostress_usable(utc_hour, lon_deg, valid_frac):
    """Screen an ECOSTRESS granule on local solar time and valid fraction.

    ISS precession makes overpass time uncontrolled: a 05:13 LST granule is
    99.9% valid and almost all zero, and a clean-downloading midday granule
    held 161 valid pixels out of 2.46 million. Expect ~2 usable granules per
    tile per summer month.
    """
    lst = (utc_hour + lon_deg / 15.0) % 24.0
    lo, hi = ECOSTRESS_LST_WINDOW
    return {"local_solar_time_h": lst,
            "in_time_window": bool(lo <= lst <= hi),
            "valid_frac_ok": bool(valid_frac >= ECOSTRESS_MIN_VALID_FRAC),
            "usable": bool(lo <= lst <= hi and valid_frac >= ECOSTRESS_MIN_VALID_FRAC)}


def mod16_mask(array, scale_factor=0.1):
    """Mask MOD16 ET/PET/LE/PLE fill codes and apply the scale factor.

    ET_500m carries valid_range [-32767, 32700] and NO _FillValue, so xarray
    scales 32767 to 3276.7 and keeps it. Measured unmasked-vs-masked: 55.5 vs
    3.60 mm/day for an 8-day block; 1279 vs 606 mm/yr annual. Pass the raw
    integer DN array.
    """
    import numpy as np
    out = np.asarray(array, dtype="float32").copy()
    out[out > MOD16_VALID_MAX] = np.nan
    out[out < 0] = np.nan
    return out * scale_factor
