"""Offline checks on the ARM value-added-product skills.

Same contract as the instrument tranche: the prose must agree with the two artifacts
shipped beside it - the shared catalog record and, where one exists,
`example_inventory.json`. The VAP-specific additions are the honesty markers, because a
derived product has two extra ways to mislead: a report that documents a sibling product
rather than this one, and a report too long for the extractor to read whole. Both must be
declared in the skill, not just known to whoever built it.

No network, no credentials.
"""
import csv
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANCHE = ROOT / "skills" / "arm-vaps"
CATALOG = ROOT / "skills" / "arm-instruments" / "catalog.csv"
SKILLS = sorted(p for p in TRANCHE.glob("arm-vap-*") if (p / "SKILL.md").exists())
IDS = [p.name for p in SKILLS]

pytestmark = pytest.mark.skipif(not SKILLS, reason="arm-vaps tranche not in this repo")


def catalog():
    with open(CATALOG, newline="") as fh:
        return {r["code"]: r for r in csv.DictReader(fh)}


def code_of(skill):
    return skill.name[len("arm-vap-"):]


def inventory(skill):
    return json.loads((skill / "example_inventory.json").read_text())


def unverified(skill):
    return "**No example file was verified for this instrument.**" in (skill / "SKILL.md").read_text()


def test_index_and_catalog_exist():
    assert (TRANCHE / "SKILL.md").exists(), "arm-vaps needs its own index SKILL.md"
    assert CATALOG.exists(), "the shared catalog lives in arm-instruments and must be present"
    assert SKILLS


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_code_is_a_vap_in_the_catalog(skill):
    cat, code = catalog(), code_of(skill)
    assert code in cat, f"{skill.name}: {code!r} is not an ARM class code"
    assert cat[code]["skill"] == skill.name, \
        f"catalog says {cat[code]['skill']!r} for {code}"
    assert cat[code]["product_type"] == "vap", \
        f"{skill.name}: catalog product_type is {cat[code]['product_type']!r}, not 'vap'"


def test_catalog_skill_column_matches_directories():
    cat = catalog()
    claimed = {r["skill"] for r in cat.values() if r["skill"].startswith("arm-vap-")}
    assert claimed == set(IDS), (f"only in csv: {sorted(claimed - set(IDS))}, "
                                 f"only on disk: {sorted(set(IDS) - claimed)}")


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_report_url_matches_catalog(skill):
    text = (skill / "SKILL.md").read_text()
    expected = catalog()[code_of(skill)]["pdf"]
    assert expected, f"{skill.name}: catalog has no report URL"
    assert expected in text, f"{skill.name}: does not link {expected}"
    assert expected == expected.strip(), \
        f"{skill.name}: catalog URL carries stray whitespace, which the server answers 404 for"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_credits_the_report_authors(skill):
    text = (skill / "SKILL.md").read_text()
    assert "## Credit" in text, f"{skill.name}: no Credit section"
    m = re.search(r"## Credit\n(.*?)\n## ", text, re.S)
    assert m, f"{skill.name}: Credit section is empty"
    block = m.group(1)
    authors = [a.strip() for a in (catalog()[code_of(skill)]["authors"] or "").split(";") if a.strip()]
    if authors:
        missing = [a for a in authors if a not in block]
        assert not missing, f"{skill.name}: Credit omits {missing}"
    else:
        assert "names no individual author" in block, \
            f"{skill.name}: no authors recorded and no statement that the cover names none"
    assert "Cite the technical report, not this skill" in block, \
        f"{skill.name}: Credit does not tell the reader what to cite"
    assert "handbook" not in block.lower(), \
        f"{skill.name}: Credit calls the source a handbook; a VAP cites a technical report"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_shared_report_is_declared(skill):
    """A report covering a sibling product must be declared, or the skill presents another
    product's algorithm as its own."""
    if catalog()[code_of(skill)].get("handbook_coverage") != "shared report":
        return
    assert "Scope of this report" in (skill / "SKILL.md").read_text(), \
        f"{skill.name}: catalog marks its report as shared but the skill carries no scope note"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_partial_extraction_is_declared(skill):
    """Where the report was too long to read whole, the skill must say so and must not
    present its lists as complete."""
    if catalog()[code_of(skill)].get("extraction_partial") != "True":
        return
    text = (skill / "SKILL.md").read_text()
    assert "Extraction coverage" in text, \
        f"{skill.name}: extraction was partial but the skill does not say so"
    assert "lower bounds" in text, \
        f"{skill.name}: coverage note does not tell the reader the lists are lower bounds"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_declares_its_inputs(skill):
    """A VAP skill that does not name its inputs is missing the thing that makes it a VAP."""
    text = (skill / "SKILL.md").read_text()
    assert "## Inputs" in text, f"{skill.name}: no Inputs section"
    for code in [i for i in (catalog()[code_of(skill)].get("vap_inputs") or "").split(",") if i]:
        assert f"`{code}`" in text, f"{skill.name}: catalog declares input {code} but the skill omits it"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_inventory_or_reason(skill):
    has_inv = (skill / "example_inventory.json").exists()
    cat = catalog()[code_of(skill)]
    if has_inv:
        assert not unverified(skill)
        assert cat["verified_file"] == inventory(skill)["filename"], \
            f"{skill.name}: catalog verified_file disagrees with the shipped inventory"
        return
    assert unverified(skill), f"{skill.name}: no inventory and no statement that none was verified"
    assert cat["no_example_reason"], f"{skill.name}: catalog carries no reason"
    for claim in ("### Variables in that file", "Measured on the example file"):
        assert claim not in (skill / "SKILL.md").read_text(), \
            f"{skill.name}: claims {claim!r} with no verified example"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_variables_cited_exist_in_the_file(skill):
    if unverified(skill):
        pytest.skip("no verified example")
    text = (skill / "SKILL.md").read_text()
    present = set(inventory(skill)["variables"])
    m = re.search(r"### Variables in that file\n(.*?)(?:\n## |\Z)", text, re.S)
    if not m:
        pytest.skip("no variable table")
    cited = set(re.findall(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|", m.group(1), re.M))
    assert cited
    assert not sorted(cited - present), \
        f"{skill.name}: cites variables absent from the file: {sorted(cited - present)}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_page_citations_are_within_the_report(skill):
    text = (skill / "SKILL.md").read_text()
    m = re.search(r"`tr p\. N`,\s*(\d+)\s*pages", text)
    assert m, f"{skill.name}: header does not state the report page count"
    n_pages = int(m.group(1))
    bad = sorted({p for p in (int(x) for x in re.findall(r"tr p\.\s*(\d+)", text))
                  if p < 1 or p > n_pages})
    assert not bad, f"{skill.name}: page citations outside 1-{n_pages}: {bad}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_has_the_vap_sections(skill):
    text = (skill / "SKILL.md").read_text()
    for heading in ("## How it is produced", "## Inputs", "## Getting the data",
                    "## Quality control in this product", "## Documented failure modes",
                    "## Verified against"):
        assert heading in text, f"{skill.name}: missing section {heading!r}"


def test_rejected_products_ship_no_skill():
    cat = catalog()
    for code, reason in {c: r["no_handbook_reason"] for c, r in cat.items() if r["no_handbook_reason"]}.items():
        assert not (TRANCHE / f"arm-vap-{code}").exists(), \
            f"{code} was rejected ({reason[:60]}...) but a VAP skill exists"


def test_index_lists_every_shipped_skill():
    text = (TRANCHE / "SKILL.md").read_text()
    missing = [n for n in IDS if n not in text]
    assert not missing, f"arm-vaps/SKILL.md does not list: {missing}"


def test_index_counts_match_the_shipped_tranche():
    """The index's own numbers must agree with what is on disk.

    This failed once: the verified-example count was computed over all VAP candidates
    including one that was later rejected, so the index claimed 75 verified and 5
    unverified while naming 6 unverified products in the same sentence.
    """
    text = (TRANCHE / "SKILL.md").read_text()
    n_skills = len(SKILLS)
    n_verified = sum(1 for s in SKILLS if (s / "example_inventory.json").exists())
    n_unverified = n_skills - n_verified

    m = re.search(r"(\d+) files opened with ACT", text)
    assert m, "index does not state how many files were opened"
    assert int(m.group(1)) == n_verified, \
        f"index claims {m.group(1)} files opened; {n_verified} skills ship an inventory"

    m = re.search(r"No example verified\*\* - (\d+) products could not be opened", text)
    assert m, "index does not state how many products lack an example"
    assert int(m.group(1)) == n_unverified, \
        f"index claims {m.group(1)} unverified; {n_unverified} skills ship no inventory"
    named = set(re.findall(r"`([a-z0-9-]+)`", text[m.end():m.end() + 700]))
    actual = {code_of(s) for s in SKILLS if not (s / "example_inventory.json").exists()}
    assert actual <= named, f"unverified products not named in the index: {sorted(actual - named)}"

    m = re.search(r"turns (\d+) of them into loadable skills", text)
    assert m and int(m.group(1)) == n_skills, \
        f"index claims {m.group(1) if m else '?'} skills; {n_skills} directories exist"
