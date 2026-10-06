"""Helpers for kdp-physics-anchor: non-circular structure measurement and
verified drop-shape relations. numpy only; rustmatrix imported lazily."""
import numpy as np

BRANDES_2002 = (0.9951, 0.02510, -0.03644, 0.005030, -0.0002492)
THURAI_BRINGI_2005 = (0.9707, 4.26e-2, -4.29e-2, 6.5e-3, -3.0e-4)
BEARD_CHUANG_1987 = (1.0048, 5.7e-4, -2.628e-2, 3.682e-3, -1.677e-4)
PREDICTED_WIDTH_RATIO_CBAND = 1.18


def axis_ratio_vh(D, relation="brandes2002"):
    """Published drop-shape polynomials. Returns b/a = VERTICAL/HORIZONTAL
    (< 1 for an oblate drop), exactly as published.

    relation: 'brandes2002' | 'thurai_bringi2005' | 'beard_chuang1987'
    D in mm. NOTE rustmatrix's dsr_bc is beard_chuang1987, NOT Brandes.
    """
    tab = {"brandes2002": BRANDES_2002,
           "thurai_bringi2005": THURAI_BRINGI_2005,
           "beard_chuang1987": BEARD_CHUANG_1987}
    if relation not in tab:
        raise KeyError(f"unknown relation {relation!r}; choose from {sorted(tab)}")
    c = tab[relation]
    d = np.asarray(D, dtype=float)
    return c[0] + c[1]*d + c[2]*d**2 + c[3]*d**3 + c[4]*d**4


def to_tmatrix_axis_ratio(D, relation="brandes2002", clamp_mm=8.0):
    """Convert a published v/h drop-shape relation to the h/v (>1 oblate) that
    rustmatrix's Scatterer(axis_ratio=...) expects, with the extrapolation clamp.

    Passing a v/h value straight to Scatterer yields a PROLATE particle,
    negative Zdr, and no error raised. Always route through this.
    """
    d = np.minimum(np.asarray(D, dtype=float), float(clamp_mm))
    r = axis_ratio_vh(d, relation)
    if np.any(r <= 0):
        raise ValueError("drop-shape polynomial non-positive; lower clamp_mm")
    out = 1.0 / r
    return float(out) if np.isscalar(D) or np.ndim(D) == 0 else out


def contiguous_runs(mask, minlen=1):
    """[(start, stop), ...] index pairs of contiguous True runs."""
    m = np.asarray(mask, dtype=bool)
    if m.size == 0:
        return []
    e = np.diff(m.astype(np.int8))
    s = list(np.flatnonzero(e == 1) + 1)
    f = list(np.flatnonzero(e == -1) + 1)
    if m[0]:
        s = [0] + s
    if m[-1]:
        f = f + [m.size]
    return [(a, b) for a, b in zip(s, f) if b - a >= minlen]


def pooled_acf(rows, maxlag):
    num = np.zeros(maxlag + 1)
    cnt = np.zeros(maxlag + 1)
    for a in rows:
        a = np.asarray(a, dtype=float)
        if a.size < 8 or not np.all(np.isfinite(a)):
            continue
        a = a - a.mean()
        n = a.size
        for L in range(min(maxlag, n - 3) + 1):
            num[L] += float(np.dot(a[:n-L], a[L:]))
            cnt[L] += n - L
    c = num / np.maximum(cnt, 1)
    return c / c[0] if c[0] > 0 else np.full_like(c, np.nan)


def resolution_floor_acf(field, noise_mask, maxlag=8, min_run=40):
    """Instrumental range correlation measured from NOISE gates.

    Gate spacing is not range resolution. If lag-1 is ~0 the gates are not
    oversampled and any structure above one gate is atmosphere.
    """
    F = np.atleast_2d(np.asarray(field, dtype=float))
    M = np.atleast_2d(np.asarray(noise_mask, dtype=bool))
    rows = [F[i, a:b] for i in range(F.shape[0])
            for a, b in contiguous_runs(M[i], min_run)]
    if not rows:
        return {"n_runs": 0, "valid": False, "reason": "no noise runs found"}
    c = pooled_acf(rows, maxlag)
    lag1 = float(c[1]) if c.size > 1 else float("nan")
    verdict = ("gates effectively independent - not oversampled"
               if abs(lag1) < 0.1 else
               f"lag-1 = {lag1:.3f}: range-correlated, resolution coarser than the gate")
    return {"n_runs": len(rows), "acf": c, "lag1": lag1,
            "valid": True, "verdict": verdict}


def decorrelation_km_noise_corrected(rows, dr_km, lo=1, hi=12):
    """Noise-corrected 1/e decorrelation length from mean-removed runs.

    White noise sits only at lag 0 and biases the raw 1/e length SHORT. Fits
    c(L) = f0 * exp(-L*dr/L0) to lags >= `lo` and reports both.

    Guard: f0 > 1.05 is impossible and means the exponential model does not
    describe this field - the signature of a FILTERED field. Returns
    valid=False rather than a misleading number.
    """
    c = pooled_acf(list(rows), hi + 2)
    L = np.arange(lo, hi + 1)
    y = c[lo:hi+1]
    ok = np.isfinite(y) & (y > 0)
    if ok.sum() < 3:
        return {"valid": False, "reason": "too few positive lags to fit", "acf": c}
    b, a = np.polyfit(L[ok] * float(dr_km), np.log(y[ok]), 1)
    f0 = float(np.exp(a))
    L0 = float(-1.0 / b) if b < 0 else float("nan")
    below = np.flatnonzero(c < 1.0 / np.e)
    raw = float((below[0] - 1) * dr_km) if below.size else float("nan")
    if f0 > 1.05:
        return {"valid": False, "signal_fraction": f0, "raw_1e_km": raw, "acf": c,
                "reason": ("signal_fraction > 1 is impossible - exponential model "
                           "does not fit; field is filtered, not noisy. Do not quote "
                           "a decorrelation length for it.")}
    if not np.isfinite(L0) or L0 <= 0:
        return {"valid": False, "signal_fraction": f0, "raw_1e_km": raw, "acf": c,
                "reason": "non-decaying fit"}
    return {"valid": True, "signal_fraction": f0, "L_km": L0,
            "raw_1e_km": raw, "noise_variance_frac": max(0.0, 1.0 - f0), "acf": c}


def core_width_threshold_sweep(field_a, field_b, mask, dr_km,
                               pcts=(85, 90, 95, 98, 99), min_gates=2,
                               label_a="A", label_b="B"):
    """Percentile-matched along-range core widths for two fields in the SAME
    gates, swept over threshold - because a single threshold is worthless.

    Rows where the median width of either field is <= 3 gates are flagged
    `floor_limited`: the ratio there is set by the resolution, not the fields.
    Read the ratio from the LOWEST percentiles that are not floor-limited.

    Thresholds are pooled over everything in `mask`. Computing them per-sweep
    instead shifts the ratios (measured: 3.00/2.33/1.33 per-file vs
    2.50/2.00/1.67 pooled at the 85th/90th/95th) without changing the verdict.
    Say which you used.
    """
    A = np.atleast_2d(np.asarray(field_a, dtype=float))
    B = np.atleast_2d(np.asarray(field_b, dtype=float))
    M = np.atleast_2d(np.asarray(mask, dtype=bool))
    floor = 3 * float(dr_km)   # <=3 gates leaves no dynamic range to compare
    out = []
    for q in pcts:
        ta = float(np.nanpercentile(A[M], q))
        tb = float(np.nanpercentile(B[M], q))
        wa, wb = [], []
        for i in range(A.shape[0]):
            for a, b in contiguous_runs(M[i] & (A[i] >= ta), min_gates):
                wa.append((b - a) * dr_km)
            for a, b in contiguous_runs(M[i] & (B[i] >= tb), min_gates):
                wb.append((b - a) * dr_km)
        if not wa or not wb:
            continue
        ma, mb = float(np.median(wa)), float(np.median(wb))
        out.append({"pct": q, f"thr_{label_a}": ta, f"thr_{label_b}": tb,
                    f"n_{label_a}": len(wa), f"n_{label_b}": len(wb),
                    f"median_{label_a}_km": ma, f"median_{label_b}_km": mb,
                    "ratio_b_over_a": mb / ma if ma > 0 else float("nan"),
                    "floor_limited": (ma <= floor + 1e-9) or (mb <= floor + 1e-9)})
    return out


def sensitivity_exponents(band="C", relation="brandes2002", temp="10C",
                          D0_range=(0.8, 3.2), n=25, Nw=1e4, mu=3,
                          D_max=8.0, num_points=64):
    """d log(field) / d log(D0) for Z, KDP and W, and the predicted
    KDP-core / Z-core width ratio. Requires rustmatrix.

    Returns {'Z':.., 'KDP':.., 'W':.., 'predicted_width_ratio':..}.
    C band / 10 degC / Brandes gives 7.37 / 6.23 / 4.00 -> 1.18.
    """
    from rustmatrix import Scatterer, radar, psd
    from rustmatrix import refractive as rfr
    from rustmatrix import tmatrix_aux as tax
    wl = {"S": tax.wl_S, "C": tax.wl_C, "X": tax.wl_X}[band]
    m = {"0C": rfr.m_w_0C, "10C": rfr.m_w_10C, "20C": rfr.m_w_20C}[temp][wl]
    sc = Scatterer(wavelength=wl, m=m, Kw_sqr=tax.K_w_sqr[wl])
    ig = psd.PSDIntegrator()
    ig.D_max = D_max
    ig.num_points = num_points
    ig.axis_ratio_func = lambda D: to_tmatrix_axis_ratio(D, relation, D_max)
    ig.geometries = (tax.geom_horiz_back, tax.geom_horiz_forw)
    sc.psd_integrator = ig
    ig.init_scatter_table(sc)
    D0s = np.linspace(D0_range[0], D0_range[1], n)
    Dg = np.linspace(0.05, D_max, 800)
    Z, K, W = [], [], []
    for D0 in D0s:
        p = psd.GammaPSD(D0=float(D0), Nw=Nw, mu=mu)
        sc.psd = p
        N = np.array([p(float(x)) for x in Dg])
        W.append((np.pi / 6) * 1e-3 * np.trapezoid(N * Dg**3, Dg))
        sc.set_geometry(tax.geom_horiz_back)
        Z.append(radar.refl(sc))
        sc.set_geometry(tax.geom_horiz_forw)
        K.append(radar.Kdp(sc))
    lg = np.log(D0s)
    eZ = float(np.polyfit(lg, np.log(Z), 1)[0])
    eK = float(np.polyfit(lg, np.log(K), 1)[0])
    eW = float(np.polyfit(lg, np.log(W), 1)[0])
    return {"Z": eZ, "KDP": eK, "W": eW, "predicted_width_ratio": eZ / eK,
            "band": band, "relation": relation, "temp": temp}
