"""Every function a skill snippet calls must exist.

The defect this catches shipped once, in all 230 ARM skills: the "Getting the data" and
"Quality control" sections opened with `import act` and then called `armlive_open`,
`armlive_list_files`, `act_qc_table` and `act_qc_apply`. Those are kernel helpers defined
by the `act-arm-live` and `act-qc` skills, not ACT functions, so a reader with a bare
`act-atmos` install got a NameError from a snippet that looked like ACT's own API.

Two rules follow, and this module enforces both for every skill in the repo:

1. A dotted call into a third-party package (`act.*`, `pyart.*`) must resolve in the
   installed package.
2. A bare call to a known skill kernel helper must not appear inside a code block at all.
   Naming one in prose, labelled as a helper, is fine and is how the skills point at the
   convenience wrappers.

Rule 1 needs the packages installed, so it skips where they are not.
"""
import ast
import builtins
import importlib
import importlib.util
import pathlib
import textwrap
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = sorted(p for p in (ROOT / "skills").rglob("*")
                if p.is_dir() and (p / "SKILL.md").exists())
IDS = [p.name for p in SKILLS]

# helpers defined by act-arm-live, act-qc and arm-instruments kernel.py sidecars
KERNEL_HELPERS = {
    "armlive_credentials", "armlive_list_files", "armlive_download", "armlive_open",
    "armlive_subset", "arm_datastream_parts", "arm_facility_latlon",
    "act_qc_variables", "act_qc_assessments", "act_qc_table", "act_qc_apply",
    "act_qc_masked", "act_qc_with_dqr",
}
def code_blocks(skill):
    return re.findall(r"```python\n(.*?)```", (skill / "SKILL.md").read_text(), re.S)


def called_symbols(block):
    """Names being called. The lookbehind matters: `\\b` also matches just after a dot,
    so a plain `\\b` pattern reports `np.arange` *and* a phantom bare `arange`."""
    return {m.group(1) for m in
            re.finditer(r"(?<![\w.])([A-Za-z_][A-Za-z0-9_.]*)\s*\(", block)}


def kernel_defs(skill):
    k = skill / "kernel.py"
    return set(re.findall(r"^def\s+([A-Za-z_][A-Za-z0-9_]*)", k.read_text(), re.M)) \
        if k.exists() else set()


def own_helpers(skill):
    """Helpers in scope for this skill: its own kernel.py sidecar, plus the sidecar of any
    sibling skill the document explicitly tells the reader to load (that is how the nested
    ARM skills reach `arm_instrument` and friends from `arm-instruments/kernel.py`)."""
    helpers = kernel_defs(skill)
    text = (skill / "SKILL.md").read_text()
    for other in SKILLS:
        if other != skill and re.search(rf"\b{re.escape(other.name)}\b", text):
            helpers |= kernel_defs(other)
    return helpers


def resolve(dotted):
    parts = dotted.split(".")
    try:
        obj = importlib.import_module(parts[0])
    except ImportError:
        return None  # package not installed: caller skips
    for i, p in enumerate(parts[1:], 1):
        try:
            obj = getattr(obj, p)
        except AttributeError:
            try:
                obj = importlib.import_module(".".join(parts[: i + 1]))
            except Exception:
                return False
    return True


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_no_kernel_helper_called_in_a_snippet(skill):
    """A snippet must run against a bare install, not silently need a skill loaded."""
    offenders = sorted({s for b in code_blocks(skill) for s in called_symbols(b)
                        if s in KERNEL_HELPERS})
    assert not offenders, (
        f"{skill.name}: code block calls skill kernel helper(s) {offenders}. These are not "
        f"ACT functions; use ACT's own API in snippets and name the helpers in prose only.")


# Calls that do not exist in the installed package. Recorded, not excused - same ratchet.
# `pyart.util.fetch_radar_time_profile` was removed from Py-ART before 2.1.1; the snippet in
# pyart-retrievals still calls it.
KNOWN_ABSENT = {"pyart-retrievals": {"pyart.util.fetch_radar_time_profile"}}


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_package_calls_resolve(skill):
    """act.* / pyart.* calls must exist in the installed package."""
    syms = {s for b in code_blocks(skill) for s in called_symbols(b)
            if s.split(".")[0] in ("act", "pyart") and "." in s}
    if not syms:
        pytest.skip("no package calls in this skill")
    broken = []
    for s in sorted(syms):
        r = resolve(s)
        if r is None:
            pytest.skip(f"{s.split('.')[0]} not installed")
        if r is False:
            broken.append(s)
    recorded = KNOWN_ABSENT.get(skill.name, set())
    new = set(broken) - recorded
    assert not new, (
        f"{skill.name}: snippet calls names absent from the installed package: {sorted(new)}")
    assert not recorded - set(broken), (
        f"{skill.name}: {sorted(recorded - set(broken))} resolves now - delete from KNOWN_ABSENT")


def bound_names(tree):
    """Every name the block itself binds: imports, assignments, args, loop and with targets."""
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            out |= {(a.asname or a.name).split(".")[0] for a in n.names}
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(n.name)
            args = getattr(n, "args", None)
            if args:
                out |= {a.arg for a in args.posonlyargs + args.args + args.kwonlyargs}
                out |= {a.arg for a in (args.vararg, args.kwarg) if a}
        elif isinstance(n, ast.Lambda):
            out |= {a.arg for a in n.args.posonlyargs + n.args.args + n.args.kwonlyargs}
        elif isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.For, ast.AsyncFor,
                            ast.comprehension, ast.withitem, ast.NamedExpr, ast.ExceptHandler)):
            targets = (n.targets if isinstance(n, ast.Assign) else
                       [n.target] if hasattr(n, "target") and n.target is not None else
                       [n.optional_vars] if isinstance(n, ast.withitem) else [])
            for tgt in filter(None, targets):
                out |= {x.id for x in ast.walk(tgt) if isinstance(x, ast.Name)}
            if isinstance(n, ast.ExceptHandler) and n.name:
                out.add(n.name)
    return out


# Skills that predate this rule and still have unreachable names in their snippets -
# mostly a missing `import numpy as np` or the `radar = pyart.io.read(...)` line that the
# narrative assumes. Recorded rather than excused: the test fails if a list grows or a new
# skill appears here, and fails telling you to delete the entry once a gap is fixed. New
# skills must be clean.
KNOWN_UNREACHABLE = {
    "cmac-vap": {"cmac.return_csu_kdp", "radar.add_field"},
    "nexrad-aws-2025": {"dt.datetime"},
    "nexrad-radar-gcs": {"skill"},
    "pyart-gatefilter-qc": {"np.ones", "radar.extract_sweeps"},
    "pyart-mapping": {"ax.add_feature", "ccrs.Geodetic", "cfeature.STATES.with_scale",
                      "disp.plot_line_xy", "plt.figure"},
    "pyart-retrievals": {"display.plot_ppi_map", "np.arange", "radar.add_field"},
    "pyart-velocity-dealias": {"gatefilter.exclude_above", "radar.add_field"},
    "rustmatrix-scattering": {"dsr_thurai_2007", "integ.init_scatter_table"},
    "rustmatrix-spectra": {"vt"},
}


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_snippet_symbols_are_accounted_for(skill):
    """No bare, unexplained call.

    Every function a snippet calls must be reachable by a reader: a builtin, an installed
    package, something the block binds itself, or a helper the skill's own kernel.py
    defines. A call to anything else is a NameError waiting to happen - which is exactly
    the defect that shipped in the ARM sections.
    """
    # A SKILL.md is a narrative: block 3 legitimately uses the `ds` that block 1 opened,
    # so scope accumulates down the document the way a reader working through it would.
    scope = set(dir(builtins)) | own_helpers(skill) | {p.stem for p in skill.glob("*.py")}
    unknown = {}
    for b in code_blocks(skill):
        try:
            tree = ast.parse(textwrap.dedent(b))
        except SyntaxError:
            continue  # illustrative fragment, not runnable code
        scope |= bound_names(tree)
        for n in ast.walk(tree):
            if not isinstance(n, ast.Call):
                continue
            f = n.func
            while isinstance(f, (ast.Attribute, ast.Subscript)):
                f = f.value
            if isinstance(f, ast.Name) and f.id not in scope:
                if importlib.util.find_spec(f.id) is None:
                    unknown[f.id] = ast.unparse(n.func)
    found = set(unknown.values())
    recorded = KNOWN_UNREACHABLE.get(skill.name, set())
    new = found - recorded
    assert not new, (
        f"{skill.name}: snippet calls {sorted(new)} with no import, assignment or known "
        f"source - a reader running the block gets a NameError")
    fixed = recorded - found
    assert not fixed, (
        f"{skill.name}: {sorted(fixed)} now reachable - delete from KNOWN_UNREACHABLE")
