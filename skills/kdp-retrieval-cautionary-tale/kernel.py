"""Physical acceptance tests for retrieved KDP fields.

Each returns a dict with a `passed` flag and the numbers behind it, so a caller can
report the evidence rather than the verdict alone. None needs a truth field or a
reference product.
"""
import numpy as np

Z_BINS = ((5, 20), (20, 30), (30, 40), (40, 50), (50, 70))


def kdp_amplitude_vs_z(kdp, z, rain_mask=None, z_bins=None, kdp_thresh=1.0):
    """Test 1: KDP median must rise monotonically with Z, and be small in light rain.

    The cheapest real check available on a KDP field. A non-monotonic Z-KDP median is
    decisive on its own -- no DSD-driven quantity can do that. In the source failure the
    median went 0.581 -> 0.432 (falling) -> 2.08 -> 2.66 -> 2.74 with 36.3% of 5-20 dBZ
    gates above 1 deg/km.

    Returns rows of (z_lo, z_hi, n, median, p90, frac_above_thresh) plus `monotonic`,
    `frac_light_rain_above_thresh` and `corr_kdp_z`.
    """
    if z_bins is None:
        z_bins = Z_BINS
    kdp = np.asarray(kdp, dtype=float)
    z = np.asarray(z, dtype=float)
    m = np.isfinite(kdp) & np.isfinite(z)
    if rain_mask is not None:
        m = m & np.asarray(rain_mask, dtype=bool)
    rows = []
    for lo, hi in z_bins:
        b = m & (z >= lo) & (z < hi)
        n = int(b.sum())
        if n < 30:
            rows.append(dict(z_lo=lo, z_hi=hi, n=n, median=float("nan"),
                             p90=float("nan"), frac_above=float("nan")))
            continue
        v = kdp[b]
        rows.append(dict(z_lo=lo, z_hi=hi, n=n, median=float(np.median(v)),
                         p90=float(np.percentile(v, 90)),
                         frac_above=float((v > kdp_thresh).mean())))
    meds = [r["median"] for r in rows if np.isfinite(r["median"])]
    monotonic = bool(all(b >= a for a, b in zip(meds, meds[1:]))) if len(meds) > 1 else None
    light = [r for r in rows if r["z_hi"] <= 20 and np.isfinite(r["frac_above"])]
    frac_light = float(light[0]["frac_above"]) if light else float("nan")
    corr = float(np.corrcoef(kdp[m], z[m])[0, 1]) if m.sum() > 30 else float("nan")
    return dict(rows=rows, monotonic=monotonic, frac_light_rain_above_thresh=frac_light,
                corr_kdp_z=corr, n_total=int(m.sum()),
                passed=bool(monotonic) and frac_light < 0.10)


def decorrelation_length_km(field, mask, dr_km, max_lag=80):
    """Along-range 1/e decorrelation length, averaged over rays."""
    field = np.asarray(field, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    acc = np.zeros(max_lag)
    cnt = np.zeros(max_lag)
    for i in range(field.shape[0]):
        m = mask[i]
        if m.sum() < 120:
            continue
        v = field[i][m]
        v = v - np.nanmean(v)
        s = np.nanstd(v)
        if not np.isfinite(s) or s < 1e-9:
            continue
        v = v / s
        for lag in range(max_lag):
            if v.size - lag > 30:
                acc[lag] += np.nanmean(v[: v.size - lag] * v[lag:])
                cnt[lag] += 1
    ac = acc / np.maximum(cnt, 1)
    below = np.where(ac < np.exp(-1.0))[0]
    length = (below[0] * dr_km) if below.size else (max_lag * dr_km)
    return dict(length_km=float(length), acf=ac, n_rays=int(cnt[0]))


def kdp_scale_vs_z(kdp, z, mask, dr_km, max_lag=80):
    """Test 2: KDP spatial scale should match Z's -- same DSD, same scale.

    Ratio near 1 passes. The source failure gave KDP 3.78 km vs Z 1.62 km (ratio 2.33),
    traced to a smoothness scale of 4.66 km = 43 gates at 108 m spacing.

    CAUTION: this metric has given opposite answers on different radar configurations
    (an earlier campaign put filter estimators at 0.49-0.57, i.e. too rough). Always
    report gate spacing and scan type with the value; never carry a target across
    campaigns.
    """
    mask = np.asarray(mask, dtype=bool)
    k = decorrelation_length_km(np.where(mask, kdp, np.nan), mask, dr_km, max_lag)
    zz = decorrelation_length_km(np.where(mask, z, np.nan), mask, dr_km, max_lag)
    ratio = k["length_km"] / zz["length_km"] if zz["length_km"] > 0 else float("nan")
    return dict(kdp_length_km=k["length_km"], z_length_km=zz["length_km"],
                ratio=float(ratio), dr_km=float(dr_km), n_rays=k["n_rays"],
                passed=bool(0.7 <= ratio <= 1.4) if np.isfinite(ratio) else None,
                note="report dr_km and scan type alongside; not portable across campaigns")


def steplikeness(kdp, mask=None):
    """Test 3: staircase signature. Compare against truth or peers -- CLOSER is better.

    A total-variation penalty on KDP has a piecewise-constant solution family, so it
    PREFERS staircases. One shipped config produced frac_repeat 0.847 with flat runs to
    9.7 km through a supercell. Note that plateau-length metrics do NOT discriminate
    between prior families; d2_over_d1, frac_repeat and n_distinct_frac do.
    """
    kdp = np.asarray(kdp, dtype=float)
    rows_d2, rows_d1, rep, dist, tot = [], [], 0, set(), 0
    arr = kdp if kdp.ndim == 2 else kdp[None, :]
    msk = None if mask is None else (np.asarray(mask, dtype=bool)
                                     if np.ndim(mask) == 2 else np.asarray(mask)[None, :])
    for i in range(arr.shape[0]):
        v = arr[i]
        if msk is not None:
            v = np.where(msk[i], v, np.nan)
        v = v[np.isfinite(v)]
        if v.size < 20:
            continue
        d1 = np.abs(np.diff(v))
        d2 = np.abs(np.diff(v, n=2))
        rows_d1.append(np.mean(d1))
        rows_d2.append(np.mean(d2))
        rep += int(np.sum(np.diff(v) == 0.0))
        tot += v.size - 1
        dist.update(np.round(v, 6).tolist())
    md1 = float(np.mean(rows_d1)) if rows_d1 else float("nan")
    md2 = float(np.mean(rows_d2)) if rows_d2 else float("nan")
    return dict(d2_over_d1=float(md2 / md1) if md1 > 0 else float("nan"),
                frac_repeat=float(rep / tot) if tot else float("nan"),
                n_distinct_frac=float(len(dist) / tot) if tot else float("nan"),
                n_rays=len(rows_d1),
                note="closer to truth/peer value is better, NOT lower")


def sign_by_altitude(kdp, height_km, iso0_km, blend_km=0.75, bin_km=1.0, top_km=14.0):
    """Test 4: KDP must be non-negative at and below the 0 C level, signed above.

    Pass is EXACTLY 0.0000% negative below the isotherm. A soft self-consistency floor
    alone makes non-negativity economic (buyable by paying a slack price), not structural
    -- that omission left 0.21-0.49% of rain gates negative in the source session.
    """
    kdp = np.asarray(kdp, dtype=float)
    h = np.asarray(height_km, dtype=float)
    fin = np.isfinite(kdp) & np.isfinite(h)
    below = fin & (h <= iso0_km)
    aloft = fin & (h > iso0_km + blend_km)
    edges = np.arange(0.0, top_km + bin_km, bin_km)
    prof = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        b = fin & (h >= lo) & (h < hi)
        if b.sum() > 20:
            prof.append(dict(h_lo=float(lo), h_hi=float(hi), n=int(b.sum()),
                             frac_neg=float((kdp[b] < 0).mean()),
                             median=float(np.median(kdp[b]))))
    fb = float((kdp[below] < 0).mean()) if below.sum() else float("nan")
    return dict(n_below=int(below.sum()), frac_neg_below=fb,
                min_below=float(kdp[below].min()) if below.sum() else float("nan"),
                n_aloft=int(aloft.sum()),
                frac_neg_aloft=float((kdp[aloft] < 0).mean()) if aloft.sum() else float("nan"),
                profile=prof, iso0_km=float(iso0_km),
                passed=bool(np.isfinite(fb) and fb == 0.0))


def check_offset_invariance(solve_fn, psi, offsets=None, tol=1e-6):
    """A KDP retrieval MUST be invariant to an additive constant on input phase.

    `solve_fn(psi) -> kdp array`. Zero-filling masked gates breaks this: 0 lands inside
    the data range and those gates still enter the phase-KDP link even at zero weight.
    Measured symptom in the source session: a constant offset moved frac_negative from
    39% to 76%, and psi+1000 pinned KDP at the ceiling everywhere.
    """
    if offsets is None:
        offsets = [0.0, -14.56, 1000.0]
    psi = np.asarray(psi, dtype=float)
    ref = None
    out = []
    for off in offsets:
        k = np.asarray(solve_fn(psi + off), dtype=float)
        if ref is None:
            ref = k
            dev = 0.0
        else:
            both = np.isfinite(ref) & np.isfinite(k)
            dev = float(np.nanmax(np.abs(ref[both] - k[both]))) if both.any() else float("nan")
        out.append(dict(offset=float(off), max_abs_dev=dev,
                        median_kdp=float(np.nanmedian(k))))
    worst = max((r["max_abs_dev"] for r in out if np.isfinite(r["max_abs_dev"])), default=float("nan"))
    return dict(results=out, worst_dev=worst,
                passed=bool(np.isfinite(worst) and worst <= tol))


def report(results, name="KDP acceptance tests"):
    """Format a dict of test-name -> result dict into a compact text block."""
    lines = [name, "=" * len(name)]
    for key, res in results.items():
        if not isinstance(res, dict):
            continue
        flag = res.get("passed")
        tag = "PASS" if flag is True else ("FAIL" if flag is False else "----")
        lines.append("[%s] %s" % (tag, key))
        for k, v in res.items():
            if k in ("rows", "profile", "results", "acf", "passed"):
                continue
            if isinstance(v, float):
                lines.append("        %-32s %.4f" % (k, v))
            elif isinstance(v, (int, str, bool, type(None))):
                lines.append("        %-32s %s" % (k, v))
        for row in res.get("rows", []) or []:
            lines.append("        Z %2.0f-%2.0f  n=%6d  med %8.3f  p90 %8.3f  frac> %6.3f"
                         % (row["z_lo"], row["z_hi"], row["n"], row["median"],
                            row["p90"], row["frac_above"]))
        for row in res.get("profile", []) or []:
            lines.append("        h %4.1f-%4.1f km  n=%6d  frac_neg %7.4f  med %7.3f"
                         % (row["h_lo"], row["h_hi"], row["n"], row["frac_neg"], row["median"]))
    return "\n".join(lines)
