"""Helpers for rustmatrix (Stephen W. Nesbitt, UIUC).

Thin, tested conveniences around the patterns in SKILL.md. Every function
here mirrors a recipe that was executed and validated against the library.
"""

import numpy as np

RUSTMATRIX_CITATION = (
    "Nesbitt, S. W. rustmatrix: Rust-backed T-matrix scattering for "
    "nonspherical hydrometeors, v2.2.0. doi:10.5281/zenodo.20077529"
)

# Measured single-particle cost model: t ~ COST_MS_AT_X1 * x**COST_EXPONENT
COST_EXPONENT = 2.72
COST_MS_AT_X1 = 2.44


def rain_axis_ratio(relation="thurai"):
    """Return a correctly-inverted axis_ratio_func for rain.

    The drop-shape relations return v/h (<1 oblate) while
    Scatterer(axis_ratio=) wants h/v (>1 oblate), so this inverts them.
    Pass the result straight to PSDIntegrator.axis_ratio_func.
    """
    from rustmatrix import tmatrix_aux
    fns = {"thurai": tmatrix_aux.dsr_thurai_2007,
           "pb": tmatrix_aux.dsr_pb,
           "bc": tmatrix_aux.dsr_bc}
    if relation not in fns:
        raise ValueError(f"relation must be one of {sorted(fns)}")
    fn = fns[relation]

    def axis_ratio_func(D):
        return 1.0 / fn(D)

    return axis_ratio_func


def estimate_tmatrix_seconds(radius_mm, wavelength_mm, n_particles=1):
    """Predict single-particle T-matrix cost from the measured x^2.72 law.

    Returns seconds. Use before launching a large table to avoid surprises
    (W-band hail is ~1 s per particle).
    """
    x = 2.0 * np.pi * float(radius_mm) / float(wavelength_mm)
    return COST_MS_AT_X1 * 1e-3 * x ** COST_EXPONENT * int(n_particles)


def check_mie_limit(wavelength_mm, radius_mm=1.0, m=None, tol=0.0001):
    """Run the Mie parity gate: T-matrix at axis_ratio=1 vs closed-form Mie.

    Returns dict with sca/ext cross sections and relative errors. Measured
    ~1e-8 across all six bands for x = 0.1 to 15 at default ddelt/ndgs.
    Raises AssertionError above `tol` (default 1e-4), which means the solver
    is not converging — pass tol=None to inspect the numbers without the gate.
    """
    from rustmatrix import Scatterer, mie_qsca, mie_qext, scatter
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import geom_horiz_back
    if m is None:
        m = m_w_10C[wavelength_mm]
    s = Scatterer(radius=radius_mm, wavelength=wavelength_mm, m=m, axis_ratio=1.0)
    s.set_geometry(geom_horiz_back)
    x = 2.0 * np.pi * radius_mm / wavelength_mm
    geo = np.pi * radius_mm ** 2
    sca_mie = mie_qsca(x, m.real, m.imag) * geo
    ext_mie = mie_qext(x, m.real, m.imag) * geo
    sca_tm = scatter.sca_xsect(s)
    ext_tm = scatter.ext_xsect(s)
    out = {"x": x, "sca_tmatrix": sca_tm, "sca_mie": sca_mie,
           "ext_tmatrix": ext_tm, "ext_mie": ext_mie,
           "relerr_sca": abs(sca_tm - sca_mie) / sca_mie,
           "relerr_ext": abs(ext_tm - ext_mie) / ext_mie}
    if tol is not None:
        worst = max(out["relerr_sca"], out["relerr_ext"])
        assert worst <= tol, (
            f"Mie parity failed at wavelength {wavelength_mm} mm, x={x:.3f}: "
            f"relative error {worst:.3e} exceeds {tol:.1e}. The T-matrix solve "
            "is not converging to the sphere limit — check radius/wavelength "
            "units (both mm) and the refractive index."
        )
    return out


def build_rain_integrator(wavelength_mm, num_points=64, D_max=8.0,
                          temperature="10C", relation="thurai",
                          both_geometries=True, orientation_averaged=False,
                          canting_std=10.0):
    """Build and tabulate a rain PSDIntegrator with validated defaults.

    Returns (scatterer, integrator) ready for `.psd = ...` assignment.
    num_points=64 puts Zdr within 0.002 dB of the 128-point value.
    """
    from rustmatrix import Scatterer, psd, orientation as _or
    from rustmatrix import refractive, tmatrix_aux
    tables = {"0C": refractive.m_w_0C, "10C": refractive.m_w_10C,
              "20C": refractive.m_w_20C}
    if temperature not in tables:
        raise ValueError(f"temperature must be one of {sorted(tables)}")
    m = tables[temperature][wavelength_mm]
    kw = tmatrix_aux.K_w_sqr[wavelength_mm]
    kwargs = {}
    if orientation_averaged:
        kwargs = {"orient": _or.orient_averaged_fixed,
                  "or_pdf": _or.gaussian_pdf(std=canting_std),
                  "n_alpha": 5, "n_beta": 10}
    s = Scatterer(wavelength=wavelength_mm, m=m, Kw_sqr=kw, **kwargs)
    ig = psd.PSDIntegrator()
    ig.D_max = float(D_max)
    ig.num_points = int(num_points)
    ig.axis_ratio_func = rain_axis_ratio(relation)
    ig.geometries = ((tmatrix_aux.geom_horiz_back, tmatrix_aux.geom_horiz_forw)
                     if both_geometries else (tmatrix_aux.geom_horiz_back,))
    s.psd_integrator = ig
    ig.init_scatter_table(s)
    return s, ig


def polarimetric_summary(scatterer, forward_geometry=True):
    """Evaluate the standard polarimetric set, switching geometry as needed.

    Returns dict with Zh/Zv in dBZ, Zdr in dB, rho_hv, delta_hv, and
    (if forward_geometry) Kdp and Ah. Assumes a PSD is attached if the
    scatterer has a psd_integrator.
    """
    from rustmatrix import radar
    from rustmatrix.tmatrix_aux import geom_horiz_back, geom_horiz_forw
    scatterer.set_geometry(geom_horiz_back)
    out = {"Zh_dBZ": 10.0 * np.log10(radar.refl(scatterer, h_pol=True)),
           "Zv_dBZ": 10.0 * np.log10(radar.refl(scatterer, h_pol=False)),
           "Zdr_dB": 10.0 * np.log10(radar.Zdr(scatterer)),
           "rho_hv": radar.rho_hv(scatterer),
           "delta_hv": radar.delta_hv(scatterer)}
    if forward_geometry:
        scatterer.set_geometry(geom_horiz_forw)
        out["Kdp_deg_km"] = radar.Kdp(scatterer)
        out["Ah_dB_km"] = radar.Ai(scatterer, h_pol=True)
        scatterer.set_geometry(geom_horiz_back)
    return out


def assert_rain_sanity(scatterer):
    """Assert Zdr > 0 for rain — catches an inverted axis ratio.

    Raises AssertionError with the measured value if the sign is wrong.
    """
    from rustmatrix import radar
    from rustmatrix.tmatrix_aux import geom_horiz_back
    scatterer.set_geometry(geom_horiz_back)
    zdr = 10.0 * np.log10(radar.Zdr(scatterer))
    assert zdr > 0, (
        f"Zdr={zdr:.3f} dB is negative for rain — axis_ratio is probably "
        "inverted. Use axis_ratio=1.0/dsr_thurai_2007(D), not dsr_thurai_2007(D)."
    )
    return zdr


def clamped_axis_ratio(relation="thurai", D_clamp=8.0, ar_cap=2.0):
    """Axis-ratio func that cannot panic the solver.

    The dsr_* polynomials cross zero (thurai 13.6186 mm, bc 12.5118,
    pb 16.6129), so 1/dsr diverges then flips sign and the Rust core dies
    with an UNCATCHABLE PanicException. This clamps the diameter and caps
    the axis ratio (real large hail is rounder than an extrapolated
    raindrop fit implies).
    """
    from rustmatrix import tmatrix_aux
    fns = {"thurai": tmatrix_aux.dsr_thurai_2007,
           "pb": tmatrix_aux.dsr_pb,
           "bc": tmatrix_aux.dsr_bc}
    if relation not in fns:
        raise ValueError(f"relation must be one of {sorted(fns)}")
    fn = fns[relation]

    def axis_ratio_func(D):
        d = min(float(D), float(D_clamp))
        return min(1.0 / fn(d), float(ar_cap))

    return axis_ratio_func


def safe_solve(fn, *args, **kwargs):
    """Call a rustmatrix entrypoint, turning a Rust panic into a return value.

    Solver non-convergence raises pyo3_runtime.PanicException, which
    subclasses BaseException — `except Exception` misses it and the worker
    dies. Returns (ok, result_or_message).
    """
    try:
        return True, fn(*args, **kwargs)
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException as e:            # noqa: BLE001 — deliberate
        return False, f"{type(e).__name__}: {e}"


def assert_converged(scatterer, nmax_limit=190):
    """Assert a solve converged rather than hitting the NPN1=200 ceiling.

    ndgs=1 reports success while pinning nmax at 199 — the refinement loop
    exhausted the cap and fell through with best-effort state, no error.
    """
    h = getattr(scatterer, "_handle", None)
    if h is None:
        scatterer.get_SZ()
        h = getattr(scatterer, "_handle", None)
    if h is None:
        raise RuntimeError("no T-matrix handle available on this scatterer")
    nmax = h.nmax
    assert nmax < nmax_limit, (
        f"nmax={nmax} >= {nmax_limit}: the solver hit the NPN1=200 ceiling "
        "and returned unconverged best-effort state. Reduce the size "
        "parameter or moderate the axis ratio; do NOT 'fix' this with ndgs=1."
    )
    return nmax


def check_orientation_parity(n_alpha):
    """Reject even n_alpha, which aliases cos(2*alpha) by up to 2.3 dB.

    The alpha grid is linspace(0,360,n_alpha+1)[:-1]; even n_alpha samples
    pairs 180 deg apart. The error does NOT shrink with refinement.
    """
    n = int(n_alpha)
    if n % 2 == 0:
        raise ValueError(
            f"n_alpha={n} is even, which aliases the cos(2*alpha) dependence "
            "(1.0-2.3 dB errors in Zdr that do not shrink with refinement). "
            "Use an odd n_alpha >= 3; (n_alpha=3, n_beta=4) is the cheapest "
            "rule good to 0.01 dB."
        )
    return n


def verify_uniform_pdf_zero(wavelength_mm, n_alpha=3, n_beta=8,
                            axis_ratio=1.5, radius_mm=1.5, tol_dB=0.01):
    """Self-test orientation averaging: uniform_pdf must give Zdr ~ 0 dB.

    Full random orientation has an exact answer of 0 dB, so this catches
    even-n_alpha aliasing or a mis-wired PDF immediately. Measured residuals
    with odd n_alpha: 1.8e-04 dB at n_alpha=3, 3.0e-07 dB at n_alpha>=5
    (n_beta>=8). Even n_alpha misses by 0.4-2.3 dB, hence the 0.01 dB default
    tolerance.
    """
    from rustmatrix import Scatterer, radar, orientation
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import geom_horiz_back
    check_orientation_parity(n_alpha)
    s = Scatterer(radius=radius_mm, wavelength=wavelength_mm,
                  m=m_w_10C[wavelength_mm], axis_ratio=axis_ratio,
                  orient=orientation.orient_averaged_fixed,
                  or_pdf=orientation.uniform_pdf(),
                  n_alpha=int(n_alpha), n_beta=int(n_beta))
    s.set_geometry(geom_horiz_back)
    zdr = 10.0 * np.log10(radar.Zdr(s))
    assert abs(zdr) < tol_dB, (
        f"uniform_pdf gave Zdr={zdr:.4f} dB, expected ~0. Orientation "
        "averaging is mis-configured (check that n_alpha is odd)."
    )
    return zdr


def assert_mixture_consistent(mix):
    """Assert HydroMix components share D_max and num_points.

    HydroMix checks wavelength but NOT D_max — a truncated component gets
    summed with a full one silently (measured 0.91 dB under-report).
    """
    dmax, npts, missing = set(), set(), []
    for c in mix.components:
        ig = getattr(c.scatterer, "psd_integrator", None)
        if ig is None or not callable(getattr(c, "psd", None)):
            missing.append(c.label)
            continue
        dmax.add(ig.D_max)
        npts.add(ig.num_points)
    assert not missing, f"components with missing psd/psd_integrator: {missing}"
    assert len(dmax) == 1, f"components disagree on D_max: {sorted(dmax)}"
    assert len(npts) == 1, f"components disagree on num_points: {sorted(npts)}"
    return {"D_max": dmax.pop(), "num_points": npts.pop(),
            "n_components": len(mix.components)}


def up_looking_kinematics(fall_speed_fn, w, v_bins):
    """Correct sign conversion for an up-looking profiler.

    The documented 'flip w and v_bins' recipe retains only 16.4% of the
    spectral power — v_exp = v_t(D) + w is not even in v, so the FALL SPEED
    must be negated too. Returns (fall_speed, w, v_bins) for
    SpectralIntegrator.
    """
    def neg_vt(D):
        return -np.asarray(fall_speed_fn(D), dtype=float)

    vb = np.asarray(v_bins, dtype=float)
    return neg_vt, -float(w), -vb[::-1]
