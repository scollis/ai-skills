"""Offline checks on every skill in the repo. No network, no credentials.

These encode the constraints that a skill must satisfy to publish and load
cleanly, plus the documentation-drift guards that caught real errors while
these skills were being written. Runs in seconds on every push; the live
suites (test_live_*.py) go to the buckets and run on a schedule instead.
"""
import ast
import os
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


def discover(root):
    """Every skill directory under skills/, at any depth.

    A skill is a directory holding a SKILL.md. Tranches may nest one level - the
    ARM instrument skills live in skills/arm-instruments/arm-instrument-<code>/,
    with skills/arm-instruments/ itself the index skill - so a flat iterdir()
    would both miss them and treat the tranche directory as a broken skill.
    """
    return sorted((p for p in root.rglob("*") if p.is_dir() and (p / "SKILL.md").exists()),
                  key=lambda p: str(p))


SKILLS = discover(ROOT / "skills")
NAMES = [p.name for p in SKILLS]
DEAD_BUCKET = "noaa-nexrad-level2"


def test_no_skill_dir_without_skill_md():
    """A directory under skills/ is either a skill or a tranche of skills."""
    orphans = []
    for p in (ROOT / "skills").rglob("*"):
        if not p.is_dir() or p.name == "__pycache__":
            continue
        if (p / "SKILL.md").exists():
            continue
        if any(c.is_dir() and (c / "SKILL.md").exists() for c in p.iterdir()):
            continue
        orphans.append(str(p.relative_to(ROOT)))
    assert not orphans, f"directories under skills/ that are neither: {orphans}"


def sidecars():
    return [(p.name, p / "kernel.py") for p in SKILLS if (p / "kernel.py").exists()]


def frontmatter(skill_dir):
    text = (skill_dir / "SKILL.md").read_text()
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta, key = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_][\w-]*:", line):
            key, v = line.split(":", 1)
            key = key.strip()
            meta[key] = v.strip()
        elif key and line.strip():
            meta[key] += " " + line.strip()   # YAML folded continuation
    return meta, text[m.end():]


@pytest.mark.parametrize("skill", SKILLS, ids=NAMES)
def test_has_skill_md(skill):
    assert (skill / "SKILL.md").exists(), f"{skill.name} has no SKILL.md"


@pytest.mark.parametrize("skill", SKILLS, ids=NAMES)
def test_frontmatter_valid(skill):
    meta, _ = frontmatter(skill)
    assert meta.get("name") == skill.name, \
        f"frontmatter name {meta.get('name')!r} != directory {skill.name!r}"
    desc = meta.get("description", "")
    assert len(desc) > 80, f"{skill.name}: description too thin to route on"
    # the registry rejects anything it reads as markup
    assert not re.search(r"<[^>]+>", desc), \
        f"{skill.name}: description contains angle-bracket text"


@pytest.mark.parametrize("name,path", sidecars(),
                         ids=[n for n, _ in sidecars()])
def test_sidecar_gate(name, path):
    """The loader accepts only functions, imports, and literal assignments."""
    tree = ast.parse(path.read_text())
    problems = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            if not isinstance(node.value, (ast.Constant, ast.Tuple, ast.List,
                                           ast.Dict)):
                problems.append(f"line {node.lineno}: computed top-level assignment "
                                f"({type(node.value).__name__})")
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.startswith("_"):
                    problems.append(f"line {node.lineno}: reserved name {t.id}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                problems.append(f"line {node.lineno}: reserved name {node.name}")
            if node.decorator_list:
                problems.append(f"line {node.lineno}: decorated top-level function")
            for d in node.args.defaults + [x for x in node.args.kw_defaults if x]:
                if not isinstance(d, (ast.Constant, ast.Tuple, ast.List, ast.Dict)):
                    problems.append(f"line {node.lineno}: computed default in "
                                    f"{node.name}")
        elif not isinstance(node, (ast.Import, ast.ImportFrom, ast.Expr)):
            problems.append(f"line {node.lineno}: {type(node).__name__} at top level")
    assert not problems, f"{name}/kernel.py violates the sidecar gate:\n  " + \
        "\n  ".join(problems)


@pytest.mark.parametrize("name,path", sidecars(),
                         ids=[n for n, _ in sidecars()])
def test_sidecar_execs_without_dunder_file(name, path):
    """Sidecars are exec'd, not imported, so __file__ is undefined."""
    ns = {}
    exec(compile(path.read_text(), str(path), "exec"), ns)
    assert any(callable(v) for v in ns.values()), f"{name} defined no helpers"


@pytest.mark.parametrize("skill", SKILLS, ids=NAMES)
def test_no_dead_bucket_recommendation(skill):
    """The deprecated bucket may be named, but never as something to try."""
    for f in skill.iterdir():
        if not f.is_file() or f.suffix not in (".md", ".py"):
            continue
        for m in re.finditer(rf".{{0,90}}{DEAD_BUCKET}.{{0,90}}", f.read_text(), re.S):
            ctx = m.group(0)
            # A prohibition ("never fall back to X") is the desired text; only a
            # recommendation is a defect.
            if re.search(r"(never|not|don'?t|no)\b[^.]{0,40}(fall\s*back|try|use)",
                         ctx, re.I):
                continue
            if re.search(r"try\s+aws|fall\s*back\s+to\s+`?" + DEAD_BUCKET,
                         ctx, re.I):
                pytest.fail(f"{skill.name}/{f.name} recommends the dead bucket:\n"
                            f"  ...{ctx.strip()}...")


@pytest.mark.parametrize("skill", SKILLS, ids=NAMES)
def test_no_embedded_secrets(skill):
    """No tokens, keys, or account names committed with a skill."""
    pattern = re.compile(
        r"(gh[pousr]_[A-Za-z0-9]{16,}|AKIA[0-9A-Z]{12,}|"
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----|"
        r"(?:api[_-]?key|secret|password|token)\s*=\s*['\"][A-Za-z0-9/+_-]{16,}['\"])",
        re.I)
    for f in skill.iterdir():
        if f.is_file() and f.suffix in (".md", ".py", ".json"):
            hit = pattern.search(f.read_text())
            assert not hit, f"{skill.name}/{f.name} looks like it embeds a secret: " \
                            f"{hit.group(0)[:24]}..."


# Skills referenced by this tranche that live elsewhere (a later tranche, or a
# PyPI package that merely looks like a skill name). Listed explicitly so a NEW
# dangling reference fails while known-external ones stay quiet.
KNOWN_EXTERNAL = {
    "arm-pyart",                  # the Py-ART package, not a skill
    "nexrad-site-rainfall",       # category 2, not yet published here
    "nexrad-area-over-threshold",
}


def test_cross_references_resolve():
    """A skill naming a sibling must name one that exists, here or in KNOWN_EXTERNAL."""
    known = set(NAMES) | KNOWN_EXTERNAL
    missing = []
    for skill in SKILLS:
        text = (skill / "SKILL.md").read_text()
        for ref in set(re.findall(r"`(nexrad-[a-z0-9-]+|arm-[a-z0-9-]+)`", text)):
            if ref not in known and ref != skill.name:
                missing.append(f"{skill.name} -> {ref}")
    assert not missing, ("cross-references to unknown skills (publish them "
                         "together, reword, or add to KNOWN_EXTERNAL):\n  " +
                         "\n  ".join(sorted(set(missing))))


def test_external_references_are_flagged_in_readme():
    """If a shipped skill points outside the repo, the README must say so."""
    referenced = set()
    for skill in SKILLS:
        text = (skill / "SKILL.md").read_text()
        for ref in re.findall(r"`(nexrad-[a-z0-9-]+|arm-[a-z0-9-]+)`", text):
            if ref not in set(NAMES) and ref in KNOWN_EXTERNAL and ref != "arm-pyart":
                referenced.add(ref)
    if not referenced:
        pytest.skip("no external skill references")
    readme = (ROOT / "README.md").read_text()
    unlisted = [r for r in referenced if r not in readme]
    assert not unlisted, ("skills referenced but not shipped, and not explained "
                          f"in README.md: {sorted(unlisted)}")


def test_router_documented_crossovers_match_code():
    """Documented crossover numbers must equal what the function returns.

    This exact drift shipped once: a docstring kept a value from a superseded
    constant. The doc is not allowed to disagree with the code.
    """
    router = ROOT / "skills" / "nexrad-cloud-router"
    if not router.exists():
        pytest.skip("router not in this repo")
    ns = {}
    exec(compile((router / "kernel.py").read_text(), "kernel.py", "exec"), ns)
    doc = (router / "SKILL.md").read_text()
    code = (router / "kernel.py").read_text()
    for regime in ("quiet", "mixed", "convective"):
        actual = ns["crossover_chunks"](regime)
        cited = set()
        for src in (doc, code):
            cited |= {int(m.group(1)) for m in
                      re.finditer(rf'crossover_chunks\("{regime}"\)\s*#\s*(\d+)', src)}
            cited |= {int(m.group(1)) for m in
                      re.finditer(rf"\b(\d+)\s*\({regime}\)", src)}
        assert not cited or cited == {actual}, \
            f"{regime}: docs cite {sorted(cited)}, code returns {actual}"


@pytest.mark.parametrize("skill", SKILLS, ids=NAMES)
def test_verified_section_is_dated(skill):
    """A 'Verified against' claim must carry a date a reader can judge."""
    text = (skill / "SKILL.md").read_text()
    m = re.search(r"^##+\s*Verified against\s*$", text, re.M)
    if not m:
        pytest.skip("no verification section")
    tail = text[m.end():]
    assert re.search(r"\d{4}-\d{2}-\d{2}", tail[:600]), \
        f"{skill.name}: 'Verified against' section carries no ISO date"
