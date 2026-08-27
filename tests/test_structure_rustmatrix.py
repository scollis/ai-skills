"""Offline documentation-vs-code checks for the rustmatrix-* tranche.

The repo rule is that a numeric or factual claim in a SKILL.md must be traceable
to something a test can check. These two skills are unusually claim-dense — they
exist because rustmatrix has several traps that produce *silently wrong numbers*
rather than errors, and the magnitude of each trap is the payload. So the checks
here are grouped as:

1.  Internal consistency — a value stated in two places, or in both a document
    and its sidecar, must agree. This class of drift shipped twice while these
    skills were being written: an "exact to floating point" claim that the
    document's own reproduced table contradicted (the zeros were five-decimal
    display of a 3.0e-07 residual), and a cache-poisoning description that named
    the wrong PSD as the victim.
2.  Physical and mathematical invariants — relations that hold whatever machine
    measured them: the drop-shape zero crossings are roots of published
    polynomials, the axis-ratio convention has a definite sign, the size-parameter
    envelope must shrink as particles get more elongated, and beam broadening has
    a closed form.
3.  Provenance and separation of concerns — measured values must be attributed to
    a named version and date, machine-specific numbers must be flagged as such,
    and every helper the prose tells the reader to call must exist in kernel.py.

No network and no rustmatrix install required: the invariant checks that need the
library are skipped when it is absent, so this suite runs in seconds on every
push. Where rustmatrix *is* installed, the invariants are re-derived rather than
trusted. Measurements came from rustmatrix 2.2.0 (PyPI ABI3 wheel) on CPython
3.13, macOS arm64, 14 cores; each skill names that in its provenance section.

rustmatrix is by Prof. Stephen W. Nesbitt (University of Illinois
Urbana-Champaign); these skills document it, they do not vendor it.
"""
import ast
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
RM_SKILLS = sorted(p for p in (ROOT / "skills").iterdir()
                   if p.is_dir() and p.name.startswith("rustmatrix-"))
RM_NAMES = [p.name for p in RM_SKILLS]

# Radar wavelengths in mm, as rustmatrix.tmatrix_aux defines them. Any skill
# quoting a band wavelength must quote one of these.
BANDS_MM = {"S": 111.0, "C": 53.5, "X": 33.3, "Ku": 22.0, "Ka": 8.43, "W": 3.19}

# Measured drop-shape zero crossings (mm). These are roots of published
# polynomial fits, so they are library properties, not machine properties.
DSR_ZEROS = {"thurai": 13.6186, "bc": 12.5118, "pb": 16.6129}

# The reference case for the axis-ratio convention: dsr_thurai_2007(3.0) is v/h.
THURAI_AT_3MM = 0.8590
ZDR_AT_3MM_DB = 1.569

# Solver caps inherited from the Fortran core.
NPN1 = 200
NPNG1 = 300

pytestmark = pytest.mark.skipif(not RM_SKILLS,
                                reason="rustmatrix tranche not in this repo")


def read(skill, name="SKILL.md"):
    p = skill / name
    return p.read_text() if p.exists() else ""


def sidecar_ns(skill):
    """Exec a skill's kernel.py the way the loader does, returning its namespace."""
    src = read(skill, "kernel.py")
    if not src:
        return {}
    ns = {}
    exec(compile(src, str(skill / "kernel.py"), "exec"), ns)
    return ns


def numbers_near(text, pattern, group=1):
    return [float(m.group(group)) for m in re.finditer(pattern, text)]


def have_rustmatrix():
    try:
        import rustmatrix  # noqa: F401
    except Exception:
        return False
    return True


# ---------------------------------------------------------------- provenance

@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_provenance_names_version_and_date(skill):
    """A measured claim needs a named library version and an ISO date.

    Without provenance a reader cannot tell whether a number still applies. Both
    skills state the wheel, interpreter, and platform up front.
    """
    text = read(skill)
    assert re.search(r"rustmatrix\s+2\.2\.0", text), \
        f"{skill.name}: no rustmatrix version named"
    assert re.search(r"\b20\d\d-\d\d-\d\d\b", text), \
        f"{skill.name}: no ISO date for the measurements"


@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_machine_specific_numbers_are_flagged(skill):
    """Timing claims must be marked machine-specific somewhere in the document.

    Accuracy claims port; timings do not. A reader planning a large run needs to
    know which is which, so any skill quoting seconds or a speedup must say so.
    """
    text = read(skill)
    quotes_timing = bool(re.search(r"\b\d+(?:\.\d+)?\s*(?:ms|s)\b", text) or
                         re.search(r"\b\d+(?:\.\d+)?\s*[x\u00d7]\b", text))
    if not quotes_timing:
        pytest.skip("no timing or speedup claims")
    assert re.search(r"machine-specific|machine specific|Re-measure|re-measure",
                     text), \
        (f"{skill.name}: quotes timings or speedups but never flags them as "
         "machine-specific")


@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_credits_the_author(skill):
    """rustmatrix is Nesbitt's work; a skill documenting it must say so.

    Not decoration: a reader who hits a solver limit needs to know whose issue
    tracker to open, and the library asks to be cited.
    """
    text = read(skill)
    assert "Nesbitt" in text, f"{skill.name}: does not credit the author"
    assert re.search(r"10\.5281/zenodo\.\d+", text), \
        f"{skill.name}: no DOI for citation"


# ------------------------------------------------------- internal consistency

@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_band_wavelengths_consistent(skill):
    """A quoted band wavelength must match tmatrix_aux, within rounding."""
    text = read(skill)
    bad = []
    for band, mm in BANDS_MM.items():
        for v in numbers_near(text, rf"wl_{band}\s*=\s*([\d.]+)"):
            if abs(v - mm) > 0.005:
                bad.append(f"{skill.name}: wl_{band}={v}, expected {mm}")
    assert not bad, "band wavelengths misquoted:\n  " + "\n  ".join(bad)


@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_dsr_zero_crossings_consistent(skill):
    """The drop-shape zero crossings anchor the clamping advice.

    These are the values that tell a user where 1/dsr(D) flips sign and panics
    the core, so a wrong one here is actively dangerous.
    """
    text = read(skill)
    bad = []
    for name, expected in DSR_ZEROS.items():
        pat = rf"{name}[^\n]{{0,40}}?(\d\d\.\d{{3,4}})"
        for v in numbers_near(text, pat):
            if abs(v - expected) > 0.001 and v not in DSR_ZEROS.values():
                bad.append(f"{skill.name}: {name} crossing {v}, expected {expected}")
    assert not bad, "drop-shape zero crossings misquoted:\n  " + "\n  ".join(bad)


def test_no_unqualified_exactness_claims():
    """"Exact to floating point" must not be claimed where a residual was measured.

    This exact drift shipped: the n_alpha parity table printed 0.00000 at five
    decimals, was read as zero, and became an "exact to floating point" headline
    that the table's own n_alpha=3 row (1.8e-04) contradicted. Any exactness
    claim must either cite a ulp/residual figure or say "bitwise".
    """
    offenders = []
    for skill in RM_SKILLS:
        for fname in ("SKILL.md", "kernel.py"):
            text = read(skill, fname)
            for m in re.finditer(r"exact(?:ly)?\s+to\s+floating[- ]point|"
                                 r"floating[- ]point\s+exact(?:ness)?", text, re.I):
                ctx = text[max(0, m.start() - 200):m.end() + 200]
                qualified = re.search(r"ulp|bitwise|bit-identical|\d\.?\d*e-\d\d|"
                                      r"0\.0000000|residual", ctx, re.I)
                if not qualified:
                    offenders.append(
                        f"{skill.name}/{fname}: unqualified exactness claim near "
                        f"...{text[max(0, m.start() - 60):m.end() + 60].strip()}...")
    assert not offenders, ("exactness claimed without a residual figure:\n  " +
                           "\n  ".join(offenders))


def test_n_alpha_parity_rule_is_stated_with_both_residuals():
    """The parity finding must distinguish n_alpha=3 from n_alpha>=5.

    Both are "odd" and both are fine in practice, but they differ by ~600x in
    residual (1.8e-04 vs 3.0e-07 dB). Collapsing them is what produced the
    original wrong claim, so the document must keep them apart.
    """
    skill = ROOT / "skills" / "rustmatrix-scattering"
    if not skill.exists():
        pytest.skip("scattering skill not in this repo")
    text = read(skill)
    assert re.search(r"n_alpha", text), "parity rule absent"
    assert re.search(r"odd", text, re.I), "parity rule does not say 'odd'"
    # The two residual magnitudes must both appear, in either notation.
    has_small = re.search(r"1\.8e-0?4|0\.00018", text)
    has_tiny = re.search(r"3\.0e-0?7|2\.98\d*e-0?7", text)
    assert has_small and has_tiny, (
        "parity section must cite BOTH residuals (1.8e-04 dB at n_alpha=3 and "
        "3.0e-07 dB at n_alpha>=5) so they are not conflated as 'exact'")


def test_axis_ratio_convention_has_one_direction():
    """The axis-ratio recipe must be stated as 1/dsr, never bare dsr.

    Passing dsr(D) directly is the library's highest-traffic silent error: it
    flips the sign of Zdr with no exception. The document must not contain a
    code line that does it, even as a counter-example without a marker.
    """
    offenders = []
    for skill in RM_SKILLS:
        for fname in ("SKILL.md", "kernel.py"):
            text = read(skill, fname)
            for m in re.finditer(r"axis_ratio\s*=\s*(?!1\s*(?:\.0)?\s*/)"
                                 r"(?:dsr_|tmatrix_aux\.dsr_)", text):
                ctx = text[max(0, m.start() - 260):m.end() + 160]
                # A deliberately-wrong example is fine if it is marked wrong.
                if re.search(r"wrong|not\b|never|silently|prolate|incorrect|"
                             r"footgun|foot-gun|trap|bug|catch", ctx, re.I):
                    continue
                offenders.append(f"{skill.name}/{fname}: unmarked "
                                 f"axis_ratio=dsr_* at offset {m.start()}")
    assert not offenders, ("bare axis_ratio=dsr_*(D) with no warning "
                           "(should be 1.0/dsr_*(D)):\n  " + "\n  ".join(offenders))


def test_solver_caps_stated_consistently():
    """NPN1=200 and NPNG1=300 must be quoted correctly wherever they appear."""
    bad = []
    for skill in RM_SKILLS:
        text = read(skill)
        for v in numbers_near(text, r"NPN1\s*(?:=|\u2264|<=)?\s*(\d+)"):
            if v != NPN1:
                bad.append(f"{skill.name}: NPN1={v}, expected {NPN1}")
        for v in numbers_near(text, r"NPNG1\s*(?:=|\u2264|<=)?\s*(\d+)"):
            if v != NPNG1:
                bad.append(f"{skill.name}: NPNG1={v}, expected {NPNG1}")
    assert not bad, "solver caps misquoted:\n  " + "\n  ".join(bad)


def test_convergence_envelope_is_monotone():
    """The documented max size parameter must fall as axis ratio rises.

    Physical invariant: a more elongated particle needs a higher nmax at the same
    x, so it must hit the NPN1 cap sooner. A table that violates this is a
    transcription error whatever machine produced it.
    """
    skill = ROOT / "skills" / "rustmatrix-scattering"
    if not skill.exists():
        pytest.skip("scattering skill not in this repo")
    text = read(skill)
    m = re.search(r"\|\s*axis_ratio[^|]*\|(.+?)\n\|[-\s|]+\n\|\s*max x\s*\|(.+?)\n",
                  text, re.S)
    if not m:
        pytest.skip("no convergence-envelope table found")
    ars = [float(x) for x in re.findall(r"[\d.]+", m.group(1))]
    xs = [float(x) for x in re.findall(r"[\d.]+", m.group(2))]
    assert len(ars) == len(xs) >= 3, \
        f"envelope table malformed: {len(ars)} axis ratios, {len(xs)} x values"
    pairs = sorted(zip(ars, xs))
    for (a1, x1), (a2, x2) in zip(pairs, pairs[1:]):
        assert x2 <= x1, (f"envelope not monotone: axis_ratio {a1} allows x={x1} "
                          f"but {a2} allows x={x2} (should be <= {x1})")


def test_thurai_recipe_arithmetic():
    """1/dsr_thurai_2007(8.0) must equal the axis ratio the docs blame for W-band
    panics, and the D=3mm reference case must invert consistently."""
    text = read(ROOT / "skills" / "rustmatrix-scattering")
    cited = numbers_near(text, r"1\.0/dsr_thurai_2007\(8\.0\)\s*=\s*([\d.]+)")
    if cited:
        for v in cited:
            assert 1.5 < v < 2.5, f"implausible axis ratio at D=8mm: {v}"
    at3 = numbers_near(text, r"dsr_thurai_2007\(3\.0\)`?\s*returns?\s*\*?\*?([\d.]+)")
    for v in at3:
        assert abs(v - THURAI_AT_3MM) < 0.001, \
            f"dsr_thurai_2007(3.0)={v}, expected {THURAI_AT_3MM}"
        assert v < 1.0, ("the whole point is that dsr returns v/h (<1 for oblate); "
                         f"{v} would be h/v")


# ------------------------------------------------------------ sidecar / prose

@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_documented_helpers_exist(skill):
    """Every helper named as a call in the prose must be defined in kernel.py.

    Catches prose describing a renamed or dropped helper.
    """
    ns = sidecar_ns(skill)
    if not ns:
        pytest.skip(f"{skill.name} ships no kernel.py")
    tree = ast.parse(read(skill, "kernel.py"))
    defined = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    defined |= {k for k, v in ns.items() if callable(v)}
    text = read(skill)
    called = set(re.findall(r"`([a-z][a-z0-9_]{3,})\(", text))
    # rustmatrix's own API and numpy/stdlib are not our sidecar's job.
    external = {
        "dsr_thurai_2007", "dsr_pb", "dsr_bc", "init_scatter_table",
        "save_scatter_table", "load_scatter_table", "set_geometry", "get_SZ",
        "collapse_to_bulk", "orient_single", "orient_averaged_fixed",
        "orient_averaged_adaptive", "gaussian_pdf", "uniform_pdf", "mie_qsca",
        "mie_qext", "radar_xsect", "sca_xsect", "ext_xsect", "refl", "Zdr",
        "Kdp", "rho_hv", "delta_hv", "ldr", "calctmat", "calcampl", "sarea",
        "sareac", "drop", "from_np", "build_state", "get_angular_integrated",
        "realistic_noise_floor", "from_params", "power_law", "sample",
        "atlas_srivastava_sekhon_1973", "brandes_et_al_2002", "beard_1976",
        "locatelli_hobbs_1974_aggregates", "locatelli_hobbs_1974_graupel_hex",
        "marshall_palmer_psd_factory", "spherical_jn", "trapezoid",
        "mg_refractive", "bruggeman_refractive", "ice_refractive", "sigma_t",
        # numpy / stdlib
        "linspace", "maximum", "asarray", "reshape", "isscalar", "ndim",
        "array_equal", "deg2rad", "isfinite", "sqrt", "log10", "sin", "exp",
        "min", "max", "float", "int", "print", "range", "help", "skill",
        "type", "array", "abs", "sum", "trapz",
    }
    missing = sorted(n for n in called - external if n not in defined)
    assert not missing, (f"{skill.name}/SKILL.md calls helpers that kernel.py "
                        f"does not define: {missing}")


@pytest.mark.parametrize("skill", RM_SKILLS, ids=RM_NAMES)
def test_guard_helpers_actually_guard(skill):
    """Helpers named assert_*/check_*/verify_* must be able to fail.

    A guard rail that cannot raise is worse than none: it reads as verification
    while asserting nothing. Each must contain an assert, a raise, or both.
    """
    src = read(skill, "kernel.py")
    if not src:
        pytest.skip(f"{skill.name} ships no kernel.py")
    tree = ast.parse(src)
    toothless = []
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not re.match(r"^(assert|check|verify)_", node.name):
            continue
        can_fail = any(isinstance(n, (ast.Assert, ast.Raise))
                       for n in ast.walk(node))
        if not can_fail:
            toothless.append(node.name)
    assert not toothless, (f"{skill.name}/kernel.py: guard helpers with no "
                           f"assert or raise: {toothless}")


def test_panic_guard_uses_base_exception():
    """Any helper that wraps a rustmatrix call must catch BaseException.

    Solver panics surface as pyo3_runtime.PanicException, which subclasses
    BaseException — `except Exception` misses it and the worker dies. A helper
    advertised as making a call safe must not use the narrower form.
    """
    skill = ROOT / "skills" / "rustmatrix-scattering"
    if not skill.exists():
        pytest.skip("scattering skill not in this repo")
    src = read(skill, "kernel.py")
    tree = ast.parse(src)
    target = next((n for n in tree.body
                   if isinstance(n, ast.FunctionDef) and n.name == "safe_solve"),
                  None)
    assert target is not None, "kernel.py defines no safe_solve helper"
    caught = set()
    for node in ast.walk(target):
        if isinstance(node, ast.ExceptHandler) and node.type is not None:
            for nm in ast.walk(node.type):
                if isinstance(nm, ast.Name):
                    caught.add(nm.id)
    assert "BaseException" in caught, (
        "safe_solve must catch BaseException — PanicException does not subclass "
        f"Exception. Currently catches: {sorted(caught)}")
    # And it must not swallow interrupts.
    assert "KeyboardInterrupt" in caught or "KeyboardInterrupt" in src, \
        "safe_solve catches BaseException but does not re-raise KeyboardInterrupt"


def test_up_looking_helper_negates_fall_speed():
    """The up-looking helper must negate the fall speed, not just w and v_bins.

    The upstream docs' recipe (flip w and v_bins only) loses most of the spectral
    power because v_exp = v_t(D) + w is not even in v. Both skills ship a helper
    for this; neither may regress to the documented-but-wrong form.
    """
    checked = 0
    for skill in RM_SKILLS:
        src = read(skill, "kernel.py")
        tree = ast.parse(src) if src else None
        if tree is None:
            continue
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            if "up_looking" not in node.name:
                continue
            checked += 1
            body = ast.unparse(node)
            assert re.search(r"-\s*np\.asarray|-\s*float\(|\[::-1\]", body), \
                f"{skill.name}/{node.name}: no negation visible"
            # the fall-speed callable itself must be negated
            assert re.search(r"def\s+\w+\(D\):\s*\n\s*return\s+-", body) or \
                   re.search(r"-\s*np\.asarray\(\s*fall_speed", body), \
                f"{skill.name}/{node.name}: negates w/v_bins but not the fall speed"
    assert checked, "no up_looking helper found in either skill"


# -------------------------------------------------- live invariants (optional)

@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_dsr_zero_crossings():
    """Re-derive the drop-shape zero crossings from the library itself.

    Plain bisection so the offline suite keeps needing only pytest.
    """
    from rustmatrix import tmatrix_aux as aux
    fns = {"thurai": aux.dsr_thurai_2007, "bc": aux.dsr_bc, "pb": aux.dsr_pb}
    for name, expected in DSR_ZEROS.items():
        lo, hi = expected - 2.0, expected + 2.0
        f_lo, f_hi = float(fns[name](lo)), float(fns[name](hi))
        assert f_lo > 0 > f_hi, (
            f"{name}: no sign change bracketing {expected} mm "
            f"(f({lo})={f_lo:.4f}, f({hi})={f_hi:.4f}) — the polynomial or the "
            "documented crossing has changed")
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if float(fns[name](mid)) > 0:
                lo = mid
            else:
                hi = mid
        root = 0.5 * (lo + hi)
        assert abs(root - expected) < 0.01, \
            f"{name} zero crossing is {root:.4f}, document says {expected}"


@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_axis_ratio_sign_convention():
    """The recipe must give positive Zdr and the bare relation negative.

    This is the claim the whole scattering skill is built around, so it is worth
    re-running rather than trusting prose.
    """
    import numpy as np

    from rustmatrix import Scatterer, radar
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import (K_w_sqr, dsr_thurai_2007,
                                        geom_horiz_back, wl_C)
    vh = float(dsr_thurai_2007(3.0))
    assert abs(vh - THURAI_AT_3MM) < 0.001, \
        f"dsr_thurai_2007(3.0)={vh:.4f}, document says {THURAI_AT_3MM}"

    def zdr(ar):
        s = Scatterer(radius=1.5, wavelength=wl_C, m=m_w_10C[wl_C],
                      axis_ratio=ar, Kw_sqr=K_w_sqr[wl_C])
        s.set_geometry(geom_horiz_back)
        return 10.0 * np.log10(radar.Zdr(s))

    good, bad = zdr(1.0 / vh), zdr(vh)
    assert good > 0, f"1/dsr gave Zdr={good:.3f} dB; rain must be positive"
    assert bad < 0, f"bare dsr gave Zdr={bad:.3f} dB; the trap should be negative"
    assert abs(good - ZDR_AT_3MM_DB) < 0.05, \
        f"Zdr={good:.3f} dB, document says {ZDR_AT_3MM_DB}"


@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_n_alpha_parity():
    """uniform_pdf must give ~0 dB for odd n_alpha and fail badly for even.

    Re-derives the documented parity rule, including the residual magnitudes the
    document is required to distinguish.
    """
    import numpy as np

    from rustmatrix import Scatterer, orientation, radar
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import geom_horiz_back, wl_C

    def zdr(n_alpha, n_beta=8):
        s = Scatterer(radius=1.5, wavelength=wl_C, m=m_w_10C[wl_C],
                      axis_ratio=1.5, orient=orientation.orient_averaged_fixed,
                      or_pdf=orientation.uniform_pdf(),
                      n_alpha=n_alpha, n_beta=n_beta)
        s.set_geometry(geom_horiz_back)
        return abs(10.0 * np.log10(radar.Zdr(s)))

    assert zdr(3) < 1e-3, "n_alpha=3 residual larger than documented 1.8e-04 dB"
    assert zdr(5) < 1e-5, "n_alpha=5 residual larger than documented 3.0e-07 dB"
    assert zdr(5) < zdr(3), "n_alpha=5 should beat n_alpha=3, as documented"
    assert zdr(4) > 0.1, "even n_alpha should alias by >0.1 dB, as documented"


@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_panic_is_base_exception_not_exception():
    """Confirm the catchability claim that shapes all the error-handling advice."""
    from rustmatrix import Scatterer
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import wl_W

    def boom():
        s = Scatterer(radius=10.0, wavelength=wl_W, m=m_w_10C[wl_W],
                      axis_ratio=3.0)
        s.set_geometry((90.0, 90.0, 0.0, 180.0, 0.0, 0.0))
        return s.get_SZ()

    try:
        boom()
    except Exception:                                    # noqa: BLE001
        pytest.fail("solver limit raised an ordinary Exception — the skills' "
                    "BaseException advice would now be wrong (good news, but "
                    "the documents need updating)")
    except BaseException as e:                           # noqa: BLE001
        assert type(e).__name__ == "PanicException", \
            f"expected PanicException, got {type(e).__name__}"
    else:
        pytest.fail("expected the documented solver panic, got none — the "
                    "convergence-envelope table may be stale")


@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_clamped_axis_ratio_prevents_panic():
    """The shipped clamp must let a table build where the bare recipe panics."""
    from rustmatrix import Scatterer, psd
    from rustmatrix.refractive import m_w_10C
    from rustmatrix.tmatrix_aux import K_w_sqr, geom_vert_back, wl_Ka
    ns = sidecar_ns(ROOT / "skills" / "rustmatrix-scattering")
    clamp = ns.get("clamped_axis_ratio")
    assert clamp is not None, "kernel.py defines no clamped_axis_ratio"
    s = Scatterer(wavelength=wl_Ka, m=m_w_10C[wl_Ka], Kw_sqr=K_w_sqr[wl_Ka])
    ig = psd.PSDIntegrator()
    ig.D_max, ig.num_points = 20.0, 32
    ig.axis_ratio_func = clamp()
    ig.geometries = (geom_vert_back,)
    s.psd_integrator = ig
    ig.init_scatter_table(s)      # must not panic
    assert ig._S_table is not None


@pytest.mark.skipif(not have_rustmatrix(), reason="rustmatrix not installed")
def test_live_sigma_beam_closed_form():
    """The sidecar's beam-broadening helper must match the closed form."""
    import numpy as np
    ns = sidecar_ns(ROOT / "skills" / "rustmatrix-spectra")
    fn = ns.get("sigma_beam")
    if fn is None:
        pytest.skip("spectra sidecar ships no sigma_beam")
    u_h, theta = 10.0, np.deg2rad(3.0)
    expected = u_h * theta / (2.0 * np.sqrt(2.0 * np.log(2.0)))
    assert abs(fn(u_h, theta) - expected) < 1e-12
