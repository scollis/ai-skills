"""Helpers for domain-wide ET and surface-flux inference."""
import os
import sys

CROPLAND_MONTHLY_MAE_PCT = (15.0, 20.0)
CROPLAND_DAILY_MAE_MM = (0.5, 1.2)
EC_CLOSURE_UNDERSTATEMENT = 0.12
CORNBELT_BENCHMARK = ("BESS-STAIR", 0.93, "mm/day", "10.5194/hess-24-1251-2020")


def et_inference_skill_dir():
    """Directory this skill was loaded from, or None if unresolvable."""
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    return here or None


def et_products(family=None, product=None):
    """Bundled table of gridded ET products and method families.

    Case-insensitive substring filters on method_family and product.
    Columns include inputs, native_resolution, cropland_rmse, cropland_bias,
    validation_doi and failure_mode.
    """
    import pandas as pd
    here = et_inference_skill_dir()
    if here is None:
        raise RuntimeError("skill directory unavailable in this runtime")
    df = pd.read_csv(os.path.join(here, "et_product_skill_table.csv"))
    for col, val in (("method_family", family), ("product", product)):
        if val:
            df = df[df[col].str.contains(val, case=False, na=False)]
    return df.reset_index(drop=True)


def et_error_floor(mean_et, timescale="monthly"):
    """Credible error range for a well-implemented cropland ET product.

    mean_et in mm/month for timescale='monthly', mm/day for 'daily'.
    Returns the absolute range implied by the documented relative floor.
    A product beating this is a developer self-assessment or one lucky site.
    """
    if timescale == "monthly":
        lo, hi = CROPLAND_MONTHLY_MAE_PCT
        return {"timescale": "monthly", "mae_pct": (lo, hi),
                "mae_mm_per_month": (mean_et * lo / 100.0, mean_et * hi / 100.0),
                "source": "10.1038/s44221-023-00181-7"}
    if timescale == "daily":
        lo, hi = CROPLAND_DAILY_MAE_MM
        return {"timescale": "daily", "mae_mm_per_day": (lo, hi),
                "mae_pct": (100.0 * lo / mean_et, 100.0 * hi / mean_et),
                "source": "10.1111/1752-1688.12956"}
    raise ValueError("timescale must be 'monthly' or 'daily'")


def closure_adjust_reference(le_uncorrected, factor=None):
    """Scale an uncorrected EC latent heat reference to closure-corrected.

    Default factor is the documented ~12% understatement across 194 CONUS
    stations (10.1016/j.agrformet.2023.109307). Apply BEFORE using towers as a
    validation target - a product validated against uncorrected towers shows a
    spurious positive bias of roughly this size.
    """
    if factor is None:
        factor = 1.0 / (1.0 - EC_CLOSURE_UNDERSTATEMENT)
    return le_uncorrected * factor
