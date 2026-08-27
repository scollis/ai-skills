"""Helpers for rustmatrix.spectra (Stephen W. Nesbitt, UIUC).

Each helper encodes a measured result from characterizing the spectra
engine — see SKILL.md for the numbers behind them.
"""

import numpy as np

GRAVITY = 9.81


def up_looking(fall_speed_fn, w, v_bins):
    """Correct up-looking (profiler) sign conversion.

    The documented 'flip w and v_bins' recipe keeps only 16.4% of the
    spectral power, because v_exp = v_t(D) + w is not even in v. The fall
    speed must be negated too. Returns (fall_speed, w, v_bins).
    """
    def neg_vt(D):
        return -np.asarray(fall_speed_fn(D), dtype=float)

    vb = np.asarray(v_bins, dtype=float)
    return neg_vt, -float(w), -vb[::-1]


def project_to_elevation(fall_speed_fn, elevation_deg):
    """Scale fall speed onto the beam — SpectralIntegrator does NOT do this.

    The velocity axis is v_t(D) + w regardless of geometry_backscatter, so
    a non-vertical geometry needs this explicitly. Do NOT use with
    BeamIntegrator, which applies cos(theta) itself.
    """
    sin_e = float(np.sin(np.deg2rad(float(elevation_deg))))

    def projected(D):
        return sin_e * np.asarray(fall_speed_fn(D), dtype=float)

    return projected


def safe_rain_fall_speed(clip_negative=True):
    """atlas_srivastava_sekhon_1973, clamped non-negative.

    Bounded and monotone to 20 mm (9.65 m/s), unlike the Brandes-based
    presets which turn over at 5.98 mm and reach 0.0 at 20 mm. Its only
    defect is a negative branch below D=0.1086 mm, which this clamps.
    """
    from rustmatrix import spectra

    base = spectra.fall_speed.atlas_srivastava_sekhon_1973

    def vt(D):
        v = np.asarray(base(D), dtype=float)
        if clip_negative:
            v = np.maximum(v, 0.0)
        # The presets return shape-(1,) arrays even for scalar input, which
        # breaks float() under numpy 2. Preserve the caller's rank.
        return v.reshape(()) [()] if np.isscalar(D) or np.ndim(D) == 0 else v

    return vt


def inertial_L_o(v_t_at_D, eps):
    """Eddy outer scale L_o giving Stokes number ~1 at a given fall speed.

    InertialZeng2023's default L_o=100 m keeps St < 0.021 for all rain,
    degenerating the model to GaussianTurbulence. L_o = sqrt(tau_p^3 * eps),
    which is centimetres for rain.
    """
    tau_p = float(v_t_at_D) / GRAVITY
    return float(np.sqrt(tau_p ** 3 * float(eps)))


def sigma_beam(u_h, beamwidth_rad):
    """Closed-form beam-broadening width [m/s]. beamwidth is RADIANS.

    Verified against measured spectral width to 7.7e-06 relative error.
    """
    return float(u_h) * float(beamwidth_rad) / (2.0 * np.sqrt(2.0 * np.log(2.0)))


def suggest_v_bins(fall_speed_fn, D_grid, sigma_eff, n_bins=512, n_sigma=4.0):
    """Velocity grid guaranteed to contain the spectrum.

    The library's own check uses 3 sigma; at 3.37 sigma the measured width
    is already 0.5% low, so this defaults to 4. A too-narrow grid can lose
    99.75% of the power with only a UserWarning.
    """
    v = np.asarray(fall_speed_fn(np.asarray(D_grid, dtype=float)), dtype=float)
    lo = float(np.min(v)) - float(n_sigma) * float(sigma_eff)
    hi = float(np.max(v)) + float(n_sigma) * float(sigma_eff)
    return np.linspace(lo, hi, int(n_bins))


def spectral_moments(v, sZ):
    """Zeroth/first/second/third moments of a Doppler spectrum.

    Returns dict with power (integral), v_mean, width (sigma) and skewness
    — skewness is the fingerprint that distinguishes inertial from Gaussian
    turbulence (-0.51 vs -0.35 on a matched case).
    """
    v = np.asarray(v, dtype=float)
    s = np.asarray(sZ, dtype=float)
    p = np.trapezoid(s, v)
    if p <= 0:
        return {"power": float(p), "v_mean": np.nan, "width": np.nan,
                "skewness": np.nan}
    vm = float(np.trapezoid(s * v, v) / p)
    var = float(np.trapezoid(s * (v - vm) ** 2, v) / p)
    sd = float(np.sqrt(var)) if var > 0 else 0.0
    skew = (float(np.trapezoid(s * (v - vm) ** 3, v) / p) / sd ** 3
            if sd > 0 else np.nan)
    return {"power": float(p), "v_mean": vm, "width": sd, "skewness": skew}


def assert_spectrum_contained(result, tol_frac=0.01):
    """Assert the spectrum's power is not clipped by the v_bins edges.

    Checks the outermost bins carry a negligible fraction of the peak. A
    clipped grid still returns a plausible-looking spectrum.
    """
    s = np.asarray(result.sZ_h, dtype=float)
    peak = float(np.max(s))
    if peak <= 0:
        raise AssertionError("spectrum has no power at all")
    edge = max(float(s[0]), float(s[-1])) / peak
    assert edge < float(tol_frac), (
        f"edge bins carry {edge:.3%} of the peak (> {tol_frac:.1%}): v_bins "
        "is clipping the spectrum. Widen it with suggest_v_bins()."
    )
    return edge


def assert_noise_free(result):
    """Assert noise is disabled — required before trusting a bulk round-trip.

    noise= never enters S_spec/Z_spec, so collapse_to_bulk round-trips
    exactly even with noise on and CANNOT detect it.
    """
    nh = float(getattr(result, "noise_h", 0.0))
    nv = float(getattr(result, "noise_v", 0.0))
    assert nh == 0.0 and nv == 0.0, (
        f"noise is enabled (noise_h={nh}, noise_v={nv}); sZ_dr / srho_hv / "
        "sLDR are biased by per-bin SNR. Use noise=None for validation."
    )
    return True


def validation_geometry(elevation_deg=60.0):
    """A slant BACKSCATTER geometry tuple for validating polarimetry.

    geom_vert_back forces Zdr=0 and rho_hv=1 identically, so it cannot
    detect a polarimetric error. Note the backscatter branch is phi=180.
    """
    thet0 = 90.0 - float(elevation_deg)
    return (thet0, 180.0 - thet0, 0.0, 180.0, 0.0, 0.0)
