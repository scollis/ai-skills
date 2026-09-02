"""Offline checks for the arm-netcdf-standards skill. No network, no credentials.

Three kinds of check, in order of what they protect:

1. **Drift guards** (stdlib only, always run). Every rule id and section number
   cited in SKILL.md must exist in the engine, and the check count the document
   claims must equal the number of checks here. This is the guard CONTRIBUTING
   asks for: the prose is not allowed to disagree with the code.
2. **Sidecar resolution** (stdlib only). kernel.py is exec'd without
   `__file__`, so the engine must still be found -- including from an unrelated
   working directory, which is the installed-skill case.
3. **Round trips** (need netCDF4, skipped when absent). A file written by
   `arm_skeleton` must come out with zero errors, and a file seeded with
   specific deviations must raise the specific rules. If the writer and the
   checker disagree, one of them is wrong.

The corpus numbers in SKILL.md (how many released ARM datastreams carry which
global attribute, which deviations recur) are *not* checkable here -- the ARM
files are not in this repo. They are written as dated observations, and the
suite asserts only that they carry a date.
"""
import ast
import datetime
import os
import pathlib
import re
import subprocess
import sys
import tempfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "arm-netcdf-standards"
KERNEL = SKILL / "kernel.py"
ENGINE = SKILL / "arm_standards_check.py"

pytestmark = pytest.mark.skipif(not SKILL.exists(),
                                reason="arm-netcdf-standards not in this repo")

TIMES = [datetime.datetime(2025, 5, 3) + datetime.timedelta(seconds=60 * i)
         for i in range(10)]
SITE, INST, FAC, LVL = "bnf", "demovap", "M1", "c1"


def sidecar():
    ns = {}
    exec(compile(KERNEL.read_text(), str(KERNEL), "exec"), ns)
    return ns


def doc():
    return (SKILL / "SKILL.md").read_text()


def skeleton(ns, tmp):
    return ns["arm_skeleton"](
        tmp, SITE, INST, FAC, LVL, TIMES,
        lat=34.34, lon=-87.34, alt=190.0,
        location_description="Bankhead National Forest (BNF), Courtland, Alabama",
        dod_version="demovap-c1-1.0", process_version="demo-1.0",
        command_line="python make_demo.py -d 20250503", doi="10.5439/0000000")


def rules_of(rep):
    return {f.rule for f in rep.findings}


# ------------------------------------------------------------ drift guards

def test_every_rule_cited_in_doc_exists_in_the_engine():
    """A rule id in the prose must be one the engine can actually emit.

    Cited ids are the reader's index into the checker's output; one that no
    longer fires (renamed, merged, dropped) sends them looking for a finding
    that cannot appear.
    """
    src = ENGINE.read_text()
    emitted = set(re.findall(r'self\.add\(\s*"([A-Z]+-[0-9a-z]+)"', src))
    cited = set(re.findall(r"`([A-Z]{3,4}-[0-9]{3}[a-z]?)`", doc()))
    assert cited, "SKILL.md cites no rule ids at all"
    missing = sorted(cited - emitted)
    assert not missing, (f"SKILL.md cites rules the engine never emits: {missing}\n"
                         f"engine emits {len(emitted)} rules")


def test_documented_section_numbers_exist_in_the_engine():
    """Section numbers in the prose must be ones the engine cites too."""
    src = ENGINE.read_text()
    engine_sections = set()
    for chunk in re.findall(r'self\.add\([^,]+,[^,]+,\s*"([^"]+)"', src):
        engine_sections.update(re.findall(r"\d+(?:\.\d+)*", chunk))
    cited = set(re.findall(r"§(\d+\.\d+(?:\.\d+)?)", doc()))
    unknown = sorted(s for s in cited if s not in engine_sections)
    # A section may legitimately be discussed in prose without a rule attached
    # (the exception process, for instance), so this is a budget, not a ban.
    assert len(unknown) <= 12, (
        f"{len(unknown)} sections cited in SKILL.md have no rule in the engine: "
        f"{unknown}")


def test_claimed_check_count_matches_this_suite():
    """"N checks pass" in SKILL.md must equal the number of tests here."""
    n_tests = sum(1 for name, obj in globals().items()
                  if name.startswith("test_") and callable(obj))
    claimed = {int(m) for m in re.findall(r"(\d+)\s+checks? in [`']?"
                                          r"test_arm_standards", doc())}
    assert claimed, ("SKILL.md's 'Verified against' section should state how many "
                     "checks in test_arm_standards.py pass")
    assert claimed == {n_tests}, (f"SKILL.md claims {sorted(claimed)} checks, "
                                  f"this file defines {n_tests}")


def test_corpus_numbers_are_dated_observations():
    """Corpus measurements are not reproducible here, so they must carry a date.

    CONTRIBUTING: "If it cannot be checked, phrase it as an observation with a
    date rather than a fact."
    """
    text = doc()
    section = text.split("## What released ARM files actually get wrong")[-1]
    assert re.search(r"\b20\d\d-\d\d-\d\d\b", section), \
        "the released-file deviation counts must name the date they were measured"
    assert re.search(r"\b20\d\d-\d\d-\d\d\b",
                     text.split("## The global attribute question")[-1]), \
        "the global-attribute presence table must name the date it was measured"


def test_profiles_documented_match_the_engine():
    """Both profile names in the prose must be accepted by the engine."""
    src = ENGINE.read_text()
    assert 'choices=("adc", "doc")' in src
    assert "--profile doc" in doc() and "`adc`" in doc()


def test_core_global_attribute_list_matches_the_doc():
    """The twelve attributes the default profile requires must be the twelve
    the prose says are present in 97-100% of released files."""
    ns = {}
    exec(compile(ENGINE.read_text(), str(ENGINE), "exec"), ns)
    core = set(ns["CORE_GLOBAL_ATTRS"])
    assert len(core) == 12, sorted(core)
    table = doc().split("## The global attribute question")[-1].split("##")[0]
    listed = {a for a in core if f"`{a}`" in table}
    assert listed == core, f"not named in the presence table: {sorted(core - listed)}"


# ------------------------------------------------------ sidecar resolution

def test_sidecar_defines_helpers_without_dunder_file():
    ns = sidecar()
    for fn in ("arm_check", "arm_print", "arm_check_tree", "arm_findings_df",
               "arm_filename", "arm_write_time", "arm_skeleton", "arm_engine"):
        assert callable(ns.get(fn)), f"{fn} missing from kernel.py"


def test_engine_resolves_from_an_unrelated_cwd():
    """The installed-skill case: exec'd from /tmp, the engine is still found."""
    probe = ("src=open(%r).read();ns={};exec(compile(src,%r,'exec'),ns);"
             "print(ns['engine_script_path']())" % (str(KERNEL), str(KERNEL)))
    r = subprocess.run([sys.executable, "-c", probe], capture_output=True,
                       text=True, cwd=tempfile.gettempdir())
    assert r.returncode == 0, (r.stdout or r.stderr)[-400:]
    assert r.stdout.strip().endswith("arm_standards_check.py")


def test_engine_env_override_is_honoured():
    probe = ("src=open(%r).read();ns={};exec(compile(src,'<anon>','exec'),ns);"
             "print(ns['engine_script_path']())" % str(KERNEL))
    r = subprocess.run([sys.executable, "-c", probe], capture_output=True,
                       text=True, cwd=tempfile.gettempdir(),
                       env={**os.environ, "ARM_STANDARDS_CHECKER": str(ENGINE)})
    assert r.returncode == 0, (r.stdout or r.stderr)[-400:]
    assert r.stdout.strip() == str(ENGINE)


def test_cf_standard_name_table_is_bundled():
    """standard_name validation must work offline, so the table ships here."""
    table = SKILL / "cf_standard_names.txt"
    assert table.exists(), "cf_standard_names.txt is not bundled"
    names = [ln.strip() for ln in table.read_text().splitlines()
             if ln.strip() and not ln.startswith("#")]
    assert len(names) > 4000, f"only {len(names)} CF names bundled"
    assert "air_temperature" in names and "quality_flag" in names


def test_udunits_subset_accepts_arm_units_and_rejects_nonsense():
    ns = {}
    exec(compile(ENGINE.read_text(), str(ENGINE), "exec"), ns)
    check = ns["check_units_string"]
    for good in ("1", "W/m^2", "degC", "m/s", "g/kg", "degree_N", "%", "mm",
                 "count", "dB", "m^3/m^3", "1/(sr*km*10000)",
                 "counts/microsecond", "seconds since 2025-05-03 00:00:00"):
        assert check(good) == [], f"{good!r} should be recognised"
    for bad in ("hhmmss", "yymmdd", "steps"):
        assert check(bad) == [bad], f"{bad!r} should not be recognised"


# --------------------------------------------------------------- round trips

def test_skeleton_is_compliant():
    pytest.importorskip("netCDF4")
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        assert os.path.basename(path) == "bnfdemovapM1.c1.20250503.000000.nc"
        rep = ns["arm_check"](path)
        assert rep.compliant, "\n".join(str(f) for f in rep.by_severity("error"))


def test_skeleton_plus_data_and_qc_variable_is_compliant():
    """The realistic case: skeleton, then a data variable with bit-packed QC."""
    netCDF4 = pytest.importorskip("netCDF4")
    import numpy as np
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        with netCDF4.Dataset(path, "a") as nc:
            v = nc.createVariable("atmospheric_temperature", "f4", ("time",))
            v.long_name = "Atmospheric temperature"
            v.units = "degC"
            v.standard_name = "air_temperature"
            v.missing_value = np.float32(-9999.0)
            v.ancillary_variables = "qc_atmospheric_temperature"
            v.cell_methods = "time: mean"
            v[:] = np.linspace(10, 12, len(TIMES)).astype("f4")

            q = nc.createVariable("qc_atmospheric_temperature", "i4", ("time",))
            q.long_name = ("Quality check results on variable: "
                           "Atmospheric temperature")
            q.units = "1"
            q.flag_method = "bit"
            q.standard_name = "quality_flag"
            q.description = (
                "This variable contains bit packed integer values, where each bit "
                "represents a QC test on the data. Non-zero bits indicate the QC "
                "condition given in the description for those bits; a value of 0 "
                "(no bits set) indicates the data has not failed any QC tests.")
            q.fail_min = np.float32(-40.0)
            q.fail_max = np.float32(50.0)
            q.bit_1_description = "Value is equal to missing_value"
            q.bit_1_assessment = "Bad"
            q.bit_2_description = "Value is less than fail_min"
            q.bit_2_assessment = "Bad"
            q.bit_3_description = "Value is greater than fail_max"
            q.bit_3_assessment = "Bad"
            q[:] = 0
        rep = ns["arm_check"](path)
        assert rep.compliant, "\n".join(str(f) for f in rep.by_severity("error"))


def test_filename_builder_rejects_bad_identifiers():
    ns = sidecar()
    for kwargs in (
        dict(site="bnfx", inst="met", facility="M1", level="b1"),
        dict(site="bnf", inst="met_avg", facility="M1", level="b1"),
        dict(site="bnf", inst="met", facility="m1", level="b1"),
        dict(site="bnf", inst="met", facility="M1", level="bb"),
        dict(site="bnf", inst="a" * 30, facility="M1", level="b1"),
    ):
        with pytest.raises(ValueError):
            ns["arm_filename"](start=datetime.datetime(2025, 1, 1), **kwargs)
    assert (ns["arm_filename"]("bnf", "met", "M1", "b1",
                               datetime.datetime(2025, 1, 1))
            == "bnfmetM1.b1.20250101.000000.nc")


def test_detects_seeded_variable_and_qc_deviations():
    """Each seeded deviation must raise its rule.

    netCDF4-python silently coerces missing_value/_FillValue to the variable's
    type, so ATT-007 cannot be produced from this library at all -- the type
    mismatch is seeded on valid_min (ATT-009) instead.
    """
    netCDF4 = pytest.importorskip("netCDF4")
    import numpy as np
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        with netCDF4.Dataset(path, "a") as nc:
            a = nc.createVariable("bad_units", "f4", ("time",))    # ATT-001/004
            a.units = "unitless"
            a[:] = 1.0
            b = nc.createVariable("bad_std_name", "f4", ("time",))
            b.long_name = "North latitude"                          # ATT-018
            b.units = "m"
            b.standard_name = "not_a_cf_standard_name"              # ATT-006
            b[:] = 1.0
            c = nc.createVariable("bad_limits", "f4", ("time",))
            c.long_name = "Bad valid_min type"
            c.units = "m"
            c.setncattr("valid_min", np.float64(-9999.0))           # ATT-009/010
            c[:] = 1.0
            q = nc.createVariable("qc_bad_limits", "i4", ("time",))
            q.long_name = "Quality check results on variable: Bad valid_min type"
            q.units = "unitless"                                    # QC-004
            q.description = "x"
            q.bit_1_description = "Value is bad"                    # QC-008
            q.bit_1_assessment = "Terrible"                         # QC-019
            q[:] = 0
            s = nc.createVariable("hatch_status", "i4", ("time",))
            s.long_name = "Hatch status"
            s.units = "1"
            s.flag_values = "[0 1 2]"                               # STA-008
            s.flag_meanings = "open closed in_transition"
            s[:] = 0
            m = nc.createVariable("sensor_status", "i4", ("time",))
            m.long_name = "Sensor status"
            m.units = "1"
            m.flag_masks = np.array([1, 2, 3], dtype="i4")          # STA-005
            m.flag_meanings = "a b c"
            m[:] = 0
        with netCDF4.Dataset(path, "a") as nc:
            nc.variables["bad_units"].sensor_height = "10 m"        # ATT-020
        rep = ns["arm_check"](path)
        got = rules_of(rep)
        for rule in ("ATT-001", "ATT-004", "ATT-006", "ATT-009", "ATT-010",
                     "ATT-018", "ATT-020", "QC-004", "QC-008", "QC-019",
                     "STA-005", "STA-008"):
            assert rule in got, f"{rule} not detected; got {sorted(got)}"
        assert not rep.compliant


def test_detects_seeded_time_filename_and_global_deviations():
    """The locally-written-product failure mode, end to end."""
    netCDF4 = pytest.importorskip("netCDF4")
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "my_product_20250503.nc")
        with netCDF4.Dataset(path, "w", format="NETCDF4") as nc:
            nc.createDimension("time", len(TIMES))          # not unlimited
            t = nc.createVariable("time", "f8", ("time",))
            t.units = "seconds since 2025-05-03 00:00:00"
            t[:] = [0, 60, 60, 30, 240, 300, 360, 420, 480, 540]
        rep = ns["arm_check"](path)
        got = rules_of(rep)
        for rule in ("FILE-002", "FILE-004", "DIM-002", "TIM-001", "TIM-014",
                     "TIM-018", "TIM-019", "LOC-001", "GLB-001", "FMT-002"):
            assert rule in got, f"{rule} not detected; got {sorted(got)}"


def test_bounds_variable_needs_no_units():
    """6.1.4 makes units not recommended on a bounds variable.

    This fired on 55 released ARM files before the exemption was added, which
    is what a rule read off the document without checking it looks like.
    """
    netCDF4 = pytest.importorskip("netCDF4")
    import numpy as np
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        with netCDF4.Dataset(path, "a") as nc:
            nc.createDimension("bound", 2)
            nc.variables["time"].bounds = "time_bounds"
            tb = nc.createVariable("time_bounds", "f8", ("time", "bound"))
            tb.long_name = "Time cell bounds"
            base = np.asarray(nc.variables["time"][:])
            tb[:, 0] = base - 30
            tb[:, 1] = base + 30
        rep = ns["arm_check"](path)
        assert rep.compliant, "\n".join(str(f) for f in rep.by_severity("error"))
        assert "BND-001" not in rules_of(rep)


def test_facility_id_with_a_description_is_a_warning_not_an_error():
    """Released ARM files carry facility_id = "M1: Bankhead National Forest".

    The documented value is the identifier alone, so this is a deviation -- but
    calling it an error would fail files ARM itself publishes, and would also
    fire a bogus filename-disagreement error on top.
    """
    netCDF4 = pytest.importorskip("netCDF4")
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        with netCDF4.Dataset(path, "a") as nc:
            nc.facility_id = "M1: Bankhead National Forest, Alabama"
        rep = ns["arm_check"](path)
        assert "GLB-009b" in rules_of(rep)
        assert "GLB-013" not in rules_of(rep), "facility code compared as text"
        assert rep.compliant, "\n".join(str(f) for f in rep.by_severity("error"))


def test_profile_doc_is_stricter_than_profile_adc():
    netCDF4 = pytest.importorskip("netCDF4")
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        assert ns["arm_check"](path, profile="adc").compliant
        strict = ns["arm_check"](path, profile="doc")
        assert not strict.compliant
        assert "GLB-002" in {f.rule for f in strict.by_severity("error")}


def test_engine_cli_exit_status_tracks_compliance():
    pytest.importorskip("netCDF4")
    ns = sidecar()
    with tempfile.TemporaryDirectory() as tmp:
        path = skeleton(ns, tmp)
        ok = subprocess.run([sys.executable, str(ENGINE), path, "--quiet"],
                            capture_output=True, text=True)
        assert ok.returncode == 0, ok.stdout[-400:]
        bad = subprocess.run([sys.executable, str(ENGINE), path, "--quiet",
                              "--profile", "doc"], capture_output=True, text=True)
        assert bad.returncode == 1
