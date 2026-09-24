"""Live checks on the ARM per-instrument skills: the three external facts each one
depends on are still true.

1. ARM's data-source catalog API still answers, and still knows the instrument.
2. The handbook PDF is still where the skill says it is.
3. ARM Live still serves the verified example datastream.

Run on a schedule, not on every push - each test hits arm.gov or adc.arm.gov.
The ARM Live test needs ARMUSER / ARMTOKEN and skips without them.
"""
import csv
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANCHE = ROOT / "skills" / "arm-instruments"
SKILLS = sorted(p for p in TRANCHE.glob("arm-instrument-*") if (p / "SKILL.md").exists())
IDS = [p.name for p in SKILLS]

ES_URL = "https://www.arm.gov/api/es/ds/_search"
ARMLIVE_QUERY = "https://adc.arm.gov/armlive/livedata/query"

pytestmark = pytest.mark.skipif(not SKILLS, reason="arm-instruments tranche not in this repo")


def catalog():
    with open(TRANCHE / "catalog.csv", newline="") as fh:
        return {r["code"]: r for r in csv.DictReader(fh)}


def inventory(skill):
    return json.loads((skill / "example_inventory.json").read_text())


def es_search(body, timeout=90):
    req = urllib.request.Request(ES_URL, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def test_catalog_api_still_answers():
    """The endpoint the whole tranche was built from."""
    out = es_search({"size": 1, "query": {"match_all": {}}})
    total = out["hits"]["total"]["value"]
    assert total > 600, f"ds index returned only {total} records; the index may have changed"


def test_catalog_still_enumerates_instrument_classes():
    """Instrument classes are the records with no 'type' field. If ARM starts typing
    them, every code in catalog.csv still has to resolve - that is the real invariant."""
    hits = es_search({"size": 1000, "query": {"match_all": {}}})["hits"]["hits"]
    live = {h["_source"].get("instrument_class_code") for h in hits
            if h["_source"].get("type") is None}
    assert len(live) > 400, f"only {len(live)} instrument classes in the live index"
    shipped = {p.name[len("arm-instrument-"):] for p in SKILLS}
    assert shipped <= live, f"codes no longer in ARM's index: {sorted(shipped - live)}"


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_handbook_pdf_still_resolves(skill):
    url = catalog()[skill.name[len("arm-instrument-"):]]["pdf"]
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            assert r.status == 200
            assert "pdf" in r.headers.get("Content-Type", ""), \
                f"{url} is no longer served as a PDF"
    except urllib.error.HTTPError as e:
        pytest.fail(f"{skill.name}: handbook {url} returned HTTP {e.code}")


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_armlive_still_serves_the_example(skill):
    user, token = os.environ.get("ARMUSER"), os.environ.get("ARMTOKEN")
    if not (user and token):
        pytest.skip("ARMUSER / ARMTOKEN not set")
    if not (skill / "example_inventory.json").exists():
        pytest.skip("no verified example for this instrument; see the skill's data section")
    inv = inventory(skill)
    ds = inv["datastream"]
    day = inv["filename"].split(".")[2]
    date = f"{day[:4]}-{day[4:6]}-{day[6:8]}"
    q = urllib.parse.urlencode({"user": f"{user}:{token}", "ds": ds,
                                "start": date, "end": date, "wt": "json"})
    with urllib.request.urlopen(f"{ARMLIVE_QUERY}?{q}", timeout=90) as r:
        out = json.loads(r.read())
    assert out.get("status") == "success", f"{ds}: ARM Live returned {out.get('status')!r}"
    assert inv["filename"] in out.get("files", []), (
        f"{ds}: the verified file {inv['filename']} is no longer listed for {date}; "
        f"archive returned {out.get('num_found')} files")
