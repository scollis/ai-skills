"""Helpers for kdp-structure-priors: measure the shape and size of KDP features."""
import numpy as np


def kdp_regime_priors(regime=None):
    """Published amplitude / depth / sign priors for named KDP structures.

    Returns the whole table as a dict, or one entry when `regime` is given.
    Values are what the cited papers report; they are priors for sanity checks,
    not universal constants. See SKILL.md for the citations in full.
    """
    table = {
        "convective_column": {
            "kdp_deg_km": "positive; scales with updraft, no fixed value",
            "extent": "several km above environmental 0 degC level; depth AND width scale "
                      "with updraft size/intensity (Snyder et al. 2017)",
            "sign": "+",
            "notes": "composed largely of rain lofted above 0 degC; companion ZDR column "
                     ">3 km above 0 degC (Kumjian et al. 2014)",
        },
        "melting_layer_core": {
            "kdp_deg_km": ">= 1.0 (threshold used by Kuster et al. 2021 at S band)",
            "extent": "at or within ~3 km below the environmental melting layer",
            "sign": "+",
            "notes": "evolves slowly, typically > 15 min; vertical gradient is as "
                     "diagnostic as the peak; descending cores in 85% of tracked downbursts",
        },
        "hail_core": {
            "kdp_deg_km": "large positive; R(KDP) still usable in rain-hail mixtures",
            "extent": "convective core scale",
            "sign": "+",
            "notes": "a rain-fitted Z-KDP self-consistency constraint is OUT OF SCOPE here "
                     "and will suppress the true core",
        },
        "dgl_band": {
            "kdp_deg_km": "0.15-0.4 local maxima near -15 degC; organised regions "
                          "> 0.1-0.2 are diagnostic (Kennedy and Rutledge 2011)",
            "extent": "horizontally extensive thin layer",
            "sign": "+",
            "notes": "marks onset of aggregation; offset in height from the ZDR band "
                     "(Moisseev et al. 2015). A convective-tuned noise floor erases it.",
        },
        "ice_alignment": {
            "kdp_deg_km": "|KDP| up to 0.8 in BOTH signs with ZDR near 0 dB "
                          "(Hubbert et al. 2014)",
            "extent": "layer ~20 km in range, ~3 km deep (Caylor and Chandrasekar 1996)",
            "sign": "-/+ (negative is the measurement)",
            "notes": "reorients on ~10 s with lightning; canting flips ~7 min before the "
                     "first IC flash. A global non-negativity prior deletes this.",
        },
        "overshooting_top": {
            "kdp_deg_km": "negative, weak",
            "extent": "storm top above the tropopause",
            "sign": "-",
            "notes": "ZH 15-30 dBZ with near-zero ZDR; small hail / conical graupel",
        },
    }
    if regime is None:
        return table
    if regime not in table:
        raise KeyError(f"unknown regime {regime!r}; choose from {sorted(table)}")
    return table[regime]


def kdp_smoothing_budget(dr_km, window_gates, feature_km):
    """Turn a filter window into the physical claim it makes.

    dr_km        gate spacing in km
    window_gates smoothing window length in gates (e.g. Py-ART window_len)
    feature_km   smallest real structure you intend to resolve, in km
    """
    window_km = float(dr_km) * float(window_gates)
    gpf = float(feature_km) / float(dr_km)
    ratio = window_km / float(feature_km)
    if ratio <= 0.5:
        verdict = f"window is {ratio:.2f}x the feature - undersmoothed, expect noise-dominated KDP"
    elif ratio <= 1.5:
        verdict = f"window is {ratio:.2f}x the feature - matched"
    else:
        verdict = (f"window is {ratio:.1f}x the feature you claim to resolve - oversmoothed")
    return {"window_km": window_km, "gates_per_feature": gpf,
            "window_over_feature": ratio, "verdict": verdict}


def kdp_segment_widths(kdp, dr_km, thresh=1.0, min_len_km=0.0):
    """Along-beam widths of contiguous runs where kdp >= thresh.

    kdp   1-D ray or 2-D (ray, gate) array; non-finite gates break runs
    Use this to build the width distribution the literature does not report.
    """
    a = np.atleast_2d(np.asarray(kdp, dtype=float))
    widths, peaks, means = [], [], []
    minlen = max(1, int(np.ceil(float(min_len_km) / float(dr_km))))
    for ray in a:
        good = np.isfinite(ray) & (ray >= float(thresh))
        if not good.any():
            continue
        edges = np.diff(good.astype(np.int8))
        starts = list(np.flatnonzero(edges == 1) + 1)
        ends = list(np.flatnonzero(edges == -1) + 1)
        if good[0]:
            starts = [0] + starts
        if good[-1]:
            ends = ends + [good.size]
        for s, e in zip(starts, ends):
            n = e - s
            if n < minlen:
                continue
            widths.append(n * float(dr_km))
            seg = ray[s:e]
            peaks.append(float(np.nanmax(seg)))
            means.append(float(np.nanmean(seg)))
    w = np.asarray(widths, dtype=float)
    out = {"n": int(w.size), "widths_km": w,
           "peak": np.asarray(peaks, dtype=float),
           "mean": np.asarray(means, dtype=float),
           "thresh": float(thresh), "dr_km": float(dr_km)}
    if w.size:
        out.update(median_km=float(np.median(w)), p90_km=float(np.percentile(w, 90)),
                   max_km=float(w.max()))
    return out


def kdp_decorrelation_km(field, dr_km, mask=None, max_lag_gates=200):
    """Along-range 1/e decorrelation length in km (mean over rays).

    Run on KDP and on Z over the SAME gates and compare the two lengths; a KDP
    field much broader than Z in the same gates has been smeared by the estimator.
    """
    a = np.atleast_2d(np.asarray(field, dtype=float)).copy()
    if mask is not None:
        m = np.atleast_2d(np.asarray(mask, dtype=bool))
        a = np.where(m, a, np.nan)
    nlag = int(min(max_lag_gates, a.shape[1] - 1))
    if nlag < 2:
        return float("nan")
    corr = np.full(nlag + 1, np.nan)
    for lag in range(nlag + 1):
        x = a[:, : a.shape[1] - lag].ravel()
        y = a[:, lag:].ravel()
        ok = np.isfinite(x) & np.isfinite(y)
        if ok.sum() < 30:
            break
        xs, ys = x[ok], y[ok]
        sx, sy = xs.std(), ys.std()
        if sx == 0 or sy == 0:
            break
        corr[lag] = float(((xs - xs.mean()) * (ys - ys.mean())).mean() / (sx * sy))
    thr = 1.0 / np.e
    below = np.flatnonzero(np.isfinite(corr) & (corr < thr))
    if below.size == 0:
        return float("nan")
    k = int(below[0])
    if k == 0:
        return 0.0
    c0, c1 = corr[k - 1], corr[k]
    frac = (c0 - thr) / (c0 - c1) if c0 != c1 else 0.0
    return float((k - 1 + frac) * float(dr_km))


def kdp_column_depth(kdp_col, height_km, iso0_km, thresh=0.5):
    """Depth (km) of positive KDP above the 0 degC level for one vertical column.

    kdp_col, height_km  1-D arrays of equal length, ordered by height
    Returns depth above iso0_km spanned by gates with kdp >= thresh, plus the
    top height reached. Depth is the standard published column metric; pair it
    with kdp_segment_widths for the width, which the literature omits.
    """
    k = np.asarray(kdp_col, dtype=float)
    h = np.asarray(height_km, dtype=float)
    sel = np.isfinite(k) & np.isfinite(h) & (h >= float(iso0_km)) & (k >= float(thresh))
    if not sel.any():
        return {"depth_km": 0.0, "top_km": float("nan"), "n_gates": 0}
    top = float(h[sel].max())
    return {"depth_km": top - float(iso0_km), "top_km": top, "n_gates": int(sel.sum())}
