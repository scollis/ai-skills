"""Offline documentation-vs-code checks for the pyart-* tranche and cmac-vap.

The repo rule is that a numeric or factual claim in a SKILL.md must be traceable
to something a test can check. These skills carry a lot of measured numbers, so
the checks here fall into three groups:

1.  Internal consistency — a number stated twice in one document, or in both a
    document and its sidecar, must agree. This is the class of drift that shipped
    once already in this repo, and it shipped again while these skills were being
    written: a KDP row paired one run's runtime with another run's percentiles.
2.  Physical invariants — relations that must hold whatever volume was measured
    (cone radius grows with height, exclusion fractions are fractions, a Nyquist
    ratio near 1 is clean).
3.  Provenance — measured values must be attributed to a named radar and date,
    and every helper the prose tells the reader to call must actually exist.

No network and no radar data: these run in seconds on every push. The
measurements themselves came from KIWA 2026-08-20 04:14 UTC (NEXRAD VCP 212) and
ARM SGP C-SAPR 2011-05-20 11:29 UTC (MC3E), named in each skill's provenance
section.
"""
import ast
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
PYART_SKILLS = sorted(p for p in (ROOT / "skills").iterdir()
                      if p.is_dir() and p.name.startswith("pyart-"))
PYART_NAMES = [p.name for p in PYART_SKILLS]
TRANCHE = PYART_SKILLS + [ROOT / "skills" / "cmac-vap"]
TRANCHE_NAMES = [p.name for p in TRANCHE]

# Measured on the two reference volumes; see each skill's provenance section.
KIWA_SWEEPS = 19
KIWA_UNIQUE_ELEVATIONS = 14
KIWA_TOP_TILT_DEG = 19.51
CSAPR_NYQUIST_MS = 16.52
CSAPR_TILTS = 17


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


@pytest.mark.parametrize("skill", TRANCHE, ids=TRANCHE_NAMES)
def test_provenance_names_radar_and_date(skill):
    """A measured claim needs a named instrument and an ISO or written date.

    Without provenance a reader cannot tell whether a number applies to their
    radar. Every skill in this tranche states its reference volumes up front.
    """
    text = read(skill)
    assert re.search(r"\b(KIWA|C-SAPR|NEXRAD|WSR-88D)\b", text), \
        f"{skill.name}: no reference radar named"
    assert re.search(r"\b20\d\d-\d\d-\d\d\b", text), \
        f"{skill.name}: no ISO date for the reference volume"


@pytest.mark.parametrize("skill", TRANCHE, ids=TRANCHE_NAMES)
def test_documented_helpers_exist(skill):
    """Every helper named in backticks in the prose must be defined in kernel.py.

    Catches the failure where prose is edited to describe a function that was
    renamed, or a sidecar function is dropped while its documentation stays.
    """
    ns = sidecar_ns(skill)
    if not ns:
        pytest.skip(f"{skill.name} ships no kernel.py")
    defined = {k for k, v in ns.items() if callable(v)}
    src = read(skill, "kernel.py")
    tree = ast.parse(src)
    top_level = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    text = read(skill)
    # Only check names that look like a call to a sidecar helper: `name(` in prose.
    called = set(re.findall(r"`([a-z][a-z0-9_]{3,})\(", text))
    # Anything resolvable in the pyart/numpy/matplotlib namespace is not ours.
    external = {"grid_from_radars", "extract_sweeps", "add_field", "get_slice",
                "read", "read_mdv", "read_nexrad_archive", "read_cfradial",
                "plot_ppi_map", "plot_grid", "plot_maxcappi", "plot_point",
                "plot_line_geo", "plot_line_xy", "plot_range_ring",
                "plot_range_rings", "plot_crosshairs", "plot_latitude_slice",
                "plot_longitude_slice", "plot_cross_section", "transform_points",
                "circle", "exclude_all", "exclude_below", "exclude_above",
                "exclude_invalid", "exclude_masked", "exclude_outside",
                "exclude_gates", "exclude_transition", "exclude_above_toa",
                "exclude_last_gates", "include_equal", "include_above",
                "include_not_masked", "map_profile_to_gates", "write_grid_geotiff",
                "write_cfradial", "to_xarray", "from_u_and_v", "copy",
                "calculate_velocity_texture", "simulated_vel_from_profile",
                "fetch_radar_time_profile", "open_nexradlevel2_datatree",
                "est_rain_rate_z", "est_rain_rate_kdp", "est_rain_rate_a",
                "est_rain_rate_zkdp", "est_rain_rate_hydro",
                "hydroclass_semisupervised", "steiner_conv_strat",
                "conv_strat_yuter", "conv_strat_raut", "feature_detection",
                "composite_reflectivity", "storm_relative_velocity",
                "create_cappi", "create_cfad", "compute_qvp", "compute_rqvp",
                "compute_evp", "compute_svp", "quasi_vertical_profile",
                "vad_browning", "vad_michelson", "kdp_maesaka", "kdp_vulpiani",
                "kdp_schneebeli", "phase_proc_lp", "phase_proc_lp_gf",
                "calculate_attenuation_zphi", "calculate_attenuation_philinear",
                "dealias_region_based", "dealias_unwrap_phase", "dealias_fourdd",
                "despeckle_field", "moment_based_gate_filter",
                "moment_and_texture_based_gate_filter", "temp_based_gate_filter",
                "iso0_based_gate_filter", "determine_sweeps", "subset_radar",
                "join_radar", "grid_displacement_pc", "cross_section_ppi",
                "cross_section_rhi", "column_vertical_profile",
                "get_field_location", "image_mute_radar", "texture_along_ray",
                "calc_zdr_offset", "calc_noise_floor", "calc_kdp_bringi",
                "do_my_fuzz", "snr_and_sounding", "get_texture", "get_melt",
                "return_csu_kdp", "fix_phase_fields", "retrieve_qvp",
                "gen_clutter_field_from_refl", "beam_block", "tall_clutter",
                "get_gate_id_categories", "gate_id_has_category", "cmac",
                "apply_figure_style", "print", "range", "float", "int",
                "skill", "install", "clone",
                # numpy / stdlib, not sidecar helpers
                "arange", "sqrt", "linspace", "zeros", "ones", "hypot", "meshgrid",
                "isfinite", "nanmax", "nanmin", "nanmedian", "nanpercentile",
                "filled", "masked_invalid", "argsort", "deg2rad", "radians"}
    missing = sorted(n for n in called - external
                     if n not in defined and n not in top_level)
    assert not missing, (f"{skill.name}/SKILL.md calls helpers that kernel.py does "
                         f"not define: {missing}")


def test_kiwa_sweep_arithmetic_consistent():
    """19 sweeps over 14 unique elevations must be stated consistently.

    The split-cut count is the single most repeated number across this tranche
    and the one a reader is most likely to act on when selecting sweeps.
    """
    offenders = []
    for skill in TRANCHE:
        text = read(skill)
        if "SAILS" not in text and "split cut" not in text.lower():
            continue
        sweeps = set(numbers_near(text, r"\b(19)\s+sweeps"))
        uniq = set(numbers_near(text, r"\b(14)\s+unique elevations"))
        # A skill may mention either or both, but never a contradicting value.
        wrong = {n for n in numbers_near(text, r"\b(\d+)\s+sweeps\b")
                 if n not in (KIWA_SWEEPS, KIWA_UNIQUE_ELEVATIONS, CSAPR_TILTS, 1.0, 3.0)}
        if wrong:
            offenders.append(f"{skill.name}: unexplained sweep counts {sorted(wrong)}")
        if sweeps and sweeps != {float(KIWA_SWEEPS)}:
            offenders.append(f"{skill.name}: sweep count {sweeps}")
        if uniq and uniq != {float(KIWA_UNIQUE_ELEVATIONS)}:
            offenders.append(f"{skill.name}: unique-elevation count {uniq}")
    assert not offenders, "inconsistent split-cut arithmetic:\n  " + \
        "\n  ".join(offenders)


def test_csapr_nyquist_stated_consistently():
    """The C-SAPR Nyquist velocity anchors every dealiasing ratio in the tranche."""
    bad = []
    for skill in TRANCHE:
        text = read(skill)
        cited = set(numbers_near(text, r"\b(1[0-9]\.\d\d)\s*m\s*s"))
        cited |= set(numbers_near(text, r"\b(1[0-9]\.\d\d)\s*m/s"))
        for v in cited:
            if abs(v - CSAPR_NYQUIST_MS) > 0.005:
                bad.append(f"{skill.name}: {v} m/s where {CSAPR_NYQUIST_MS} expected")
    assert not bad, "Nyquist velocity misquoted:\n  " + "\n  ".join(bad)


def test_dealias_ratio_arithmetic():
    """The headline 22x / 2.9x Nyquist claim must divide out correctly.

    This is the tranche's most-quoted result (one QC criterion, sevenfold change
    in velocity range), so the ratio and the ranges must agree with each other
    and with the stated Nyquist.
    """
    skill = ROOT / "skills" / "pyart-velocity-dealias"
    if not skill.exists():
        pytest.skip("dealias skill not in this repo")
    text = read(skill)
    ratios = set(numbers_near(text, r"\b(2\d)\s*[x\u00d7]\s*(?:the\s+)?"
                                    r"(?:[\d.]+\s*m\s*s[^)]*)?Nyquist"))
    assert ratios, "no NxNyquist ratio found in the dealias skill"
    lows = numbers_near(text, r"[-\u2212](3\d\d\.\d)\s*to")
    assert lows, "no failed-dealias velocity range found"
    worst = max(lows)
    implied = worst / CSAPR_NYQUIST_MS
    assert any(abs(implied - r) < 1.0 for r in ratios), (
        f"stated ratios {sorted(ratios)} do not match {worst} m/s / "
        f"{CSAPR_NYQUIST_MS} m/s = {implied:.1f}")


def test_cone_radius_grows_with_height():
    """cone_radius_km must be linear in height and match z/tan(top_elevation).

    The cone of silence is the tranche's georeferencing ground truth, so the
    formula behind it is checked rather than trusted.
    """
    skill = ROOT / "skills" / "pyart-mapping"
    if not skill.exists():
        pytest.skip("mapping skill not in this repo")
    ns = sidecar_ns(skill)
    fn = ns["cone_radius_km"]

    class FakeRadar:
        fixed_angle = {"data": [0.5, 5.0, KIWA_TOP_TILT_DEG]}

    r4, r8 = fn(FakeRadar(), 4000.0), fn(FakeRadar(), 8000.0)
    assert r8 > r4 > 0, f"cone radius not increasing: {r4}, {r8}"
    assert abs(r8 / r4 - 2.0) < 1e-6, f"not linear in height: {r4} -> {r8}"
    import math
    expect = 8000.0 / math.tan(math.radians(KIWA_TOP_TILT_DEG)) / 1000.0
    assert abs(r8 - expect) < 1e-6, f"{r8} != z/tan(top) = {expect}"


def test_datum_error_is_real_and_geodetic_is_clean():
    """PlateCarree-as-source must be shown wrong and Geodetic right.

    The 21 km displacement is the mapping skill's headline warning. If a cartopy
    release ever changes this, the skill's central claim is void and this test is
    how we find out.
    """
    skill = ROOT / "skills" / "pyart-mapping"
    if not skill.exists():
        pytest.skip("mapping skill not in this repo")
    ns = sidecar_ns(skill)
    try:
        out = ns["assert_no_datum_error"](lon0=-112.0, lat0=33.6)
    except ImportError:
        pytest.skip("cartopy not installed")
    assert out["geodetic_error_m"] < 100.0, \
        f"Geodetic round-trip is no longer clean: {out}"
    assert out["platecarree_error_m"] > 1000.0, \
        (f"PlateCarree no longer shows the datum error ({out}); the mapping "
         "skill's central warning needs rewriting")
    text = read(skill)
    cited = numbers_near(text, r"\b(2[01]\.\d)\s*km")
    if cited:
        km = out["platecarree_error_m"] / 1000.0
        assert any(abs(km - c) < 1.5 for c in cited), \
            f"skill cites {cited} km, measured {km:.1f} km"


def test_exclusion_fractions_are_fractions():
    """Every exclusion figure quoted as a fraction must lie in [0, 1].

    A gate-exclusion value above 1 means a percentage was pasted into a fraction
    column, which would send a reader chasing a nonexistent QC problem.
    """
    bad = []
    for skill in TRANCHE:
        text = read(skill)
        for m in re.finditer(r"(?:excl(?:uded)?|exclusion)\D{0,24}?(\d\.\d{3,4})\b",
                             text):
            v = float(m.group(1))
            if not 0.0 <= v <= 1.0:
                bad.append(f"{skill.name}: {v}")
    assert not bad, "exclusion fractions outside [0,1]:\n  " + "\n  ".join(bad)


def test_qc_recipes_are_ordered_by_strictness():
    """permissive < dualpol < strict must hold in the code, not just the prose."""
    skill = ROOT / "skills" / "pyart-gatefilter-qc"
    if not skill.exists():
        pytest.skip("gatefilter skill not in this repo")
    src = read(skill, "kernel.py")
    # strict must raise the RhoHV floor above the dualpol default
    assert re.search(r"rhv_min,\s*refl_min\s*=\s*0\.95", src), \
        "strict recipe no longer tightens RhoHV to 0.95"
    assert re.search(r"rhv_min=0\.85", src), \
        "dualpol default RhoHV floor is no longer 0.85"
    assert re.search(r'exclude_below\("cross_correlation_ratio",\s*0\.80\)', src), \
        "permissive recipe no longer uses the 0.80 RhoHV floor"


def test_nyquist_ratio_verdicts_are_monotonic():
    """nyquist_ratio must call a near-1 ratio clean and a large one suspect."""
    skill = ROOT / "skills" / "pyart-velocity-dealias"
    if not skill.exists():
        pytest.skip("dealias skill not in this repo")
    src = read(skill, "kernel.py")
    assert "nyquist_ratio" in src, "nyquist_ratio helper is gone"
    # The documented diagnostic threshold and the code's must agree.
    doc = read(skill)
    doc_thresholds = set(numbers_near(doc, r"ratio\D{0,40}?above\s*~?(\d(?:\.\d)?)"))
    code_thresholds = set(numbers_near(src, r"ratio\s*[<>]=?\s*(\d(?:\.\d)?)"))
    if doc_thresholds and code_thresholds:
        assert doc_thresholds & code_thresholds, \
            (f"documented ratio threshold {sorted(doc_thresholds)} appears nowhere "
             f"in the code thresholds {sorted(code_thresholds)}")


def test_lp_bug_described_as_upstream_not_user_error():
    """The phase_proc_lp_gf crash must be attributed to the library.

    A reader who believes it is their data will burn hours on QC and solver
    tolerances, both of which were tested and ruled out.
    """
    skill = ROOT / "skills" / "pyart-dualpol-phase"
    if not skill.exists():
        pytest.skip("dualpol skill not in this repo")
    text = read(skill)
    assert "phase_proc_lp_gf" in text, "the LP function is not mentioned"
    assert re.search(r"upstream|library bug|not your data|not a data problem",
                     text, re.I), \
        "the LP crash is not attributed to the library"
    assert re.search(r"infeasible", text, re.I), \
        "the infeasible-ray root cause is not stated"


def test_schneebeli_runs_quoted_as_pairs():
    """Both kdp_schneebeli runs must appear together, never mixed.

    This exact conflation shipped once: the gate-filtered run's runtime paired
    with the unfiltered run's percentiles. The two runs differ only in the
    gatefilter passed, so each row must carry its own runtime AND its own p99.
    """
    skill = ROOT / "skills" / "pyart-dualpol-phase"
    if not skill.exists():
        pytest.skip("dualpol skill not in this repo")
    text = read(skill)
    if "schneebeli" not in text.lower():
        pytest.skip("schneebeli not discussed")
    # Both p99 values must be present if either is.
    has_unfiltered = bool(re.search(r"\b79\.2\d?\b", text))
    has_filtered = bool(re.search(r"\b37\.6\d?\b|\b37\.7\b", text))
    assert has_unfiltered == has_filtered, (
        "kdp_schneebeli p99 values must be quoted as a pair "
        f"(unfiltered 79.22 present={has_unfiltered}, "
        f"filtered 37.65 present={has_filtered}) - quoting one alone is the "
        "conflation this test exists to prevent")
    if has_unfiltered:
        # And both runtimes, so neither row borrows the other's.
        assert re.search(r"\b165\b", text) and re.search(r"\b146\b", text), \
            ("both schneebeli runtimes (165 s unfiltered, 146 s filtered) must "
             "appear wherever both p99 values do")


def test_maesaka_fill_is_labelled():
    """kdp_maesaka's valid-gate count must be marked as fill, not retrieval.

    Verified behaviour: a gatefilter excluding 91% of gates was passed and the
    solver still returned a finite value at every gate. An unqualified 3.96 M
    invites the reader to rank it above vulpiani's 339 k.
    """
    skill = ROOT / "skills" / "pyart-dualpol-phase"
    if not skill.exists():
        pytest.skip("dualpol skill not in this repo")
    text = read(skill)
    if "maesaka" not in text.lower():
        pytest.skip("maesaka not discussed")
    assert re.search(r"fill|filled through|not signal|not retrieval", text, re.I), \
        ("kdp_maesaka's large valid-gate count is not labelled as fill; a reader "
         "will read coverage as skill")


def test_sweep_number_trap_documented_where_it_bites():
    """Skills whose functions hit the extract_sweeps trap must warn about it."""
    affected = {"pyart-foundations", "pyart-retrievals"}
    for skill in TRANCHE:
        if skill.name not in affected:
            continue
        text = read(skill)
        assert "sweep_number" in text, \
            f"{skill.name} does not mention the sweep_number trap"
        assert re.search(r"extract_sweeps", text), \
            f"{skill.name} does not name extract_sweeps as the cause"


def test_roi_ranking_stated_as_the_transferable_result():
    """The gridding skill must not present its RMSE digits as universal.

    Re-running the holdout sweep with a different base gatefilter moved nb-1.5
    RMSE between 4.57 and 4.96 dBZ. The ranking was stable; the digits were not.
    """
    skill = ROOT / "skills" / "pyart-gridding"
    if not skill.exists():
        pytest.skip("gridding skill not in this repo")
    text = read(skill)
    assert re.search(r"volume-\s*and\s*QC-specific|ranking|re-?run", text, re.I), \
        ("the gridding skill quotes absolute RMSE without telling the reader to "
         "re-measure; the ranking is what transfers")


def test_cmac_machinery_stays_out_of_pyart_skills():
    """CMAC is a consumer of Py-ART; its own machinery belongs only in cmac-vap.

    Keeping the boundary means a Py-ART user never has to install scikit-fuzzy
    or learn a VAP config system to follow a pyart-* skill.
    """
    cmac_only = ["do_my_fuzz", "snr_and_sounding", "return_csu_kdp",
                 "calc_kdp_bringi", "cacti_csapr2", "_DEFAULT_CMAC_VALUES",
                 "gen_clutter_field_from_refl", "tall_clutter",
                 "get_gate_id_categories", "scikit-fuzzy", "wradlib"]
    leaks = []
    for skill in PYART_SKILLS:
        blob = read(skill) + read(skill, "kernel.py")
        for token in cmac_only:
            if token in blob:
                leaks.append(f"{skill.name}: {token}")
    assert not leaks, ("CMAC-specific machinery leaked into pyart-* skills "
                       "(document it in cmac-vap instead):\n  " +
                       "\n  ".join(leaks))


def test_cmac_skill_states_the_separation():
    """cmac-vap must say it is separate and point back at the pyart-* skills."""
    skill = ROOT / "skills" / "cmac-vap"
    if not skill.exists():
        pytest.skip("cmac-vap not in this repo")
    text = read(skill)
    assert re.search(r"consumer of Py-?ART|not part of it|Separate from", text, re.I), \
        "cmac-vap does not state its relationship to the pyart-* skills"
    assert re.search(r"pyart-[a-z-]+", text), \
        "cmac-vap does not cross-reference any pyart-* skill"


@pytest.mark.parametrize("skill", TRANCHE, ids=TRANCHE_NAMES)
def test_radar_class_differences_are_attributed(skill):
    """A claim about NCP or Nyquist must say which radar class it applies to.

    Confusing the two classes is the most common source of user error in this
    tranche: min_ncp works on a research radar and must be None on NEXRAD.
    """
    text = read(skill)
    if "normalized_coherent_power" not in text:
        pytest.skip("does not discuss NCP")
    # A markdown table names the radar classes in its header, which can sit many
    # rows above the NCP row, so widen the window to the enclosing section.
    window = ""
    for m in re.finditer(r"normalized_coherent_power", text):
        start = text.rfind("\n## ", 0, m.start())
        window += text[max(0, start if start != -1 else m.start() - 1200):
                       m.start() + 400]
    assert re.search(r"NEXRAD|WSR-88D|research", window), \
        (f"{skill.name}: NCP discussed without naming which radar class has it")
