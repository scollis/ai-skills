"""Offline checks on the ARM per-instrument handbook skills.

The claim each of these skills makes is that its prose agrees with two artifacts
shipped beside it: `catalog.csv` (ARM's own data-source record) and
`example_inventory.json` (what was actually in the file that was opened). These
tests are what make that claim checkable, so documentation drift fails a push
rather than misleading a reader months later.

No network, no credentials. The live counterpart is test_live_arm_instruments.py.
"""
import csv
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANCHE = ROOT / "skills" / "arm-instruments"
SKILLS = sorted(p for p in TRANCHE.glob("arm-instrument-*") if (p / "SKILL.md").exists())
IDS = [p.name for p in SKILLS]

pytestmark = pytest.mark.skipif(not TRANCHE.exists(),
                                reason="arm-instruments tranche not in this repo")


def catalog():
    with open(TRANCHE / "catalog.csv", newline="") as fh:
        return {r["code"]: r for r in csv.DictReader(fh)}


def code_of(skill):
    return skill.name[len("arm-instrument-"):]


def inventory(skill):
    return json.loads((skill / "example_inventory.json").read_text())


def test_tranche_index_exists():
    assert (TRANCHE / "SKILL.md").exists(), "arm-instruments needs its own index SKILL.md"
    assert (TRANCHE / "kernel.py").exists()
    assert (TRANCHE / "catalog.csv").exists()
    assert SKILLS, "no per-instrument skills found in the tranche"


def unverified(skill):
    """True when this skill deliberately ships without a measured data example."""
    return "**No example file was verified for this instrument.**" in (skill / "SKILL.md").read_text()


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_ships_its_inventory_or_says_why_not(skill):
    """Either the data claims are backed by a file, or the skill states no file was opened.

    The failure this prevents: a data section that reads as measured when nothing was.
    """
    has_inv = (skill / "example_inventory.json").exists()
    if has_inv:
        assert not unverified(skill), \
            f"{skill.name}: ships an inventory but also claims no example was verified"
        return
    text = (skill / "SKILL.md").read_text()
    assert unverified(skill), \
        f"{skill.name}: no example_inventory.json and no statement that none was verified"
    cat = catalog()[code_of(skill)]
    assert cat["no_example_reason"], \
        f"{skill.name}: catalog.csv carries no reason for the missing example"
    assert cat["example_verified"] in ("False", "false"), \
        f"{skill.name}: catalog says example_verified={cat['example_verified']!r} but no inventory shipped"
    for claim in ("### Variables in that file", "Measured on the example file"):
        assert claim not in text, f"{skill.name}: claims {claim!r} with no verified example"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_credits_the_handbook_authors(skill):
    """Every skill credits the instrument mentors who wrote its handbook, or states
    explicitly that the cover names none. A derived reference that drops the attribution
    is the one defect here that is not merely inaccurate.
    """
    text = (skill / "SKILL.md").read_text()
    assert "## Credit" in text, f"{skill.name}: no Credit section"
    m = re.search(r"## Credit\n(.*?)(?:\n## )", text, re.S)
    assert m, f"{skill.name}: Credit section is empty"
    block = m.group(1)
    authors = [a.strip() for a in (catalog()[code_of(skill)]["authors"] or "").split(";") if a.strip()]
    if authors:
        missing = [a for a in authors if a not in block]
        assert not missing, f"{skill.name}: Credit section omits {missing}"
        assert "instrument mentor" in block, \
            f"{skill.name}: Credit names authors but not their role"
    else:
        assert "names no individual author" in block, (
            f"{skill.name}: no authors in catalog.csv and no statement that the handbook "
            f"cover names none")
    assert "Cite the handbook, not this skill" in block, \
        f"{skill.name}: Credit section does not tell the reader what to cite"


def test_every_skill_with_authors_is_credited_in_the_catalog():
    """catalog.csv is the machine-readable copy of the attribution; it must not be thinner
    than the prose."""
    cat = catalog()
    thin = []
    for skill in SKILLS:
        row = cat[code_of(skill)]
        block = re.search(r"## Credit\n(.*?)(?:\n## )", (skill / "SKILL.md").read_text(), re.S)
        named = bool(block and "names no individual author" not in block.group(1))
        if named and not (row["authors"] or "").strip():
            thin.append(skill.name)
    assert not thin, f"skills crediting authors that catalog.csv does not record: {thin}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_shared_handbook_carries_a_scope_note(skill):
    """When one handbook covers several instrument classes, the skill must say so - or it
    is quietly presenting family-level numbers as instrument-specific."""
    row = catalog()[code_of(skill)]
    siblings = [s for s in (row["shared_handbook_with"] or "").split(",") if s]
    if not siblings:
        return
    text = (skill / "SKILL.md").read_text()
    assert "Scope of this handbook" in text, \
        f"{skill.name}: shares its handbook with {siblings} but carries no scope note"
    for s in siblings:
        assert f"`{s}`" in text, f"{skill.name}: scope note does not name sibling {s}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_code_is_in_catalog(skill):
    cat = catalog()
    code = code_of(skill)
    assert code in cat, f"{skill.name}: {code!r} is not an ARM instrument class code"
    assert cat[code]["skill"] == skill.name, \
        f"catalog.csv skill column says {cat[code]['skill']!r} for {code}"


def test_catalog_skill_column_matches_directories():
    cat = catalog()
    claimed = {r["skill"] for r in cat.values() if r.get("skill")}
    assert claimed == set(IDS), (
        "catalog.csv disagrees with the shipped skills; "
        f"only in csv: {sorted(claimed - set(IDS))}, only on disk: {sorted(set(IDS) - claimed)}")


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_handbook_url_matches_catalog(skill):
    """The handbook a skill links must be the one the catalog resolved for that code."""
    text = (skill / "SKILL.md").read_text()
    urls = set(re.findall(r"https://www\.arm\.gov/publications/tech_reports/[^\s)\]]+", text))
    expected = catalog()[code_of(skill)]["pdf"]
    assert expected, f"{skill.name}: catalog has no handbook PDF for this code"
    assert expected in urls, f"{skill.name}: links {sorted(urls)}, catalog says {expected}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_example_datastream_is_consistent(skill):
    """SKILL.md, catalog.csv and the inventory must all name the same datastream."""
    if unverified(skill):
        pytest.skip("no verified example; covered by test_ships_its_inventory_or_says_why_not")
    text = (skill / "SKILL.md").read_text()
    inv = inventory(skill)
    ds = inv["datastream"]
    assert catalog()[code_of(skill)]["ex_datastream"] == ds, \
        f"{skill.name}: catalog.csv example disagrees with the inventory ({ds})"
    assert ds in text, f"{skill.name}: SKILL.md never names the verified datastream {ds}"
    assert inv["filename"] in text, \
        f"{skill.name}: SKILL.md does not name the verified file {inv['filename']}"
    assert inv["filename"].startswith(ds.split(".")[0]), \
        f"{skill.name}: file {inv['filename']} is not from datastream {ds}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_variables_cited_exist_in_the_file(skill):
    """Every variable named in the inventory table was in the file that was opened.

    An invented or drifted variable name is the failure mode that would waste a
    reader's time most directly, so it is the one pinned hardest here.
    """
    if unverified(skill):
        pytest.skip("no verified example; nothing is cited from a file")
    text = (skill / "SKILL.md").read_text()
    inv = inventory(skill)
    present = set(inv["variables"])
    m = re.search(r"### Variables in that file\n(.*?)(?:\n## |\Z)", text, re.S)
    if not m:
        pytest.skip("no variable table in this skill")
    cited = set(re.findall(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|", m.group(1), re.M))
    assert cited, f"{skill.name}: variable table present but no variables parsed"
    missing = sorted(cited - present)
    assert not missing, f"{skill.name}: SKILL.md cites variables absent from the file: {missing}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_variable_and_qc_counts_match_inventory(skill):
    if unverified(skill):
        pytest.skip("no verified example; no counts are claimed")
    text = (skill / "SKILL.md").read_text()
    inv = inventory(skill)
    for label, key in [("Data variables", "n_vars"), ("QC variables", "n_qc_vars")]:
        m = re.search(rf"\|\s*{label}\s*\|\s*(\d+)", text)
        assert m, f"{skill.name}: no '{label}' row in the data table"
        assert int(m.group(1)) == inv[key], \
            f"{skill.name}: SKILL.md says {label}={m.group(1)}, inventory says {inv[key]}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_page_citations_are_within_the_handbook(skill):
    """`hb p. N` must point at a page the handbook actually has."""
    text = (skill / "SKILL.md").read_text()
    m = re.search(r"`hb p\. N`,\s*(\d+)\s*pages", text)
    assert m, f"{skill.name}: header does not state the handbook page count"
    n_pages = int(m.group(1))
    cited = [int(x) for x in re.findall(r"hb p\.\s*(\d+)", text)]
    bad = sorted({p for p in cited if p < 1 or p > n_pages})
    assert not bad, f"{skill.name}: page citations outside 1-{n_pages}: {bad}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_has_the_sections_that_earn_the_skill(skill):
    """A per-instrument skill without artifacts or QC is a datastream listing."""
    text = (skill / "SKILL.md").read_text()
    for heading in ("## How it measures", "## The data", "## Getting the data",
                    "## Quality control in this datastream",
                    "## Known artifacts and failure modes", "## Verified against"):
        assert heading in text, f"{skill.name}: missing section {heading!r}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_no_unsourced_artifact_rows(skill):
    """Artifact rows carry either a page citation or an explicit dash, never a bare
    claim - the whole point of the section is that it is the mentor's text, not ours."""
    text = (skill / "SKILL.md").read_text()
    m = re.search(r"## Known artifacts and failure modes\n(.*?)(?:\n## |\Z)", text, re.S)
    if not m or "|" not in m.group(1):
        pytest.skip("no artifact table")
    rows = [r for r in m.group(1).splitlines()
            if r.startswith("|") and not r.startswith("|---") and "how it shows up" not in r]
    unsourced = [r[:70] for r in rows if not re.search(r"(hb p\.\s*\d+|\|\s*-\s*\|)", r)]
    assert not unsourced, f"{skill.name}: artifact rows with no source: {unsourced}"


def test_kernel_resolves_every_shipped_skill():
    ns = {}
    path = TRANCHE / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    assert ns["arm_catalog_path"] is not None
    rows = ns["arm_catalog"]()
    assert len(rows) > 400, f"catalog.csv looks truncated: {len(rows)} rows"
    for skill in SKILLS:
        code = code_of(skill)
        assert ns["arm_skill_for"](code) == skill.name
        rec = ns["arm_instrument"](code)
        assert rec and rec["name"], f"arm_instrument({code!r}) returned nothing"
        if not unverified(skill):
            ex = ns["arm_instrument_example"](code)
            assert ex["datastream"] == inventory(skill)["datastream"], \
                f"arm_instrument_example({code!r}) disagrees with the shipped inventory"


def test_index_lists_every_shipped_skill():
    text = (TRANCHE / "SKILL.md").read_text()
    missing = [n for n in IDS if n not in text]
    assert not missing, f"arm-instruments/SKILL.md does not list: {missing}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_parent_handbook_is_declared(skill):
    """A class with no handbook of its own must say whose handbook it is using.

    21 of these skills are documented only inside a parent system's handbook, and for 9
    of those the document never names the class at all. Publishing either without saying
    so would present another instrument's facts as this one's - the exact misattribution
    this tranche exists to avoid.
    """
    row = catalog()[code_of(skill)]
    if row.get("handbook_is_parent", "") != "True":
        return
    text = (skill / "SKILL.md").read_text()
    assert "ARM links no handbook to this class" in text, \
        f"{skill.name}: uses a parent handbook but does not declare it"
    if row.get("handbook_coverage") == "parent-system-level":
        assert "every fact in this skill is" in text and "parent-system-level" in text, \
            f"{skill.name}: handbook never names this class, but the skill does not say so"


def test_rejected_classes_ship_no_skill():
    """Classes whose linked handbook turned out to describe a different instrument were
    rejected. The reason is recorded, and no skill may claim them."""
    cat = catalog()
    rejected = {c: r["no_handbook_reason"] for c, r in cat.items() if r.get("no_handbook_reason")}
    assert rejected, "catalog.csv records no rejected classes; the audit trail is missing"
    for code, reason in rejected.items():
        assert len(reason) > 30, f"{code}: rejection reason too thin to judge"
        assert not (TRANCHE / f"arm-instrument-{code}").exists(), \
            f"{code} was rejected ({reason[:60]}...) but a skill directory exists"


def test_coverage_is_classified_for_every_skill():
    """Every skill states how its handbook relates to it, so a reader never has to guess."""
    cat = catalog()
    allowed = {"own handbook", "class-specific", "parent-system-level",
               "different instrument (APS handbook)", ""}
    bad = {code_of(s): cat[code_of(s)].get("handbook_coverage") for s in SKILLS
           if cat[code_of(s)].get("handbook_coverage") not in allowed}
    assert not bad, f"unrecognised handbook_coverage values: {bad}"
