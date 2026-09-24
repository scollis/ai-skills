"""Live checks on the ARM VAP skills: the report is still served, and ARM Live still
serves the verified example. The catalog-API check lives in test_live_arm_instruments.py;
both tranches read the same index, so it is not repeated here.

Run on a schedule, not on every push. The ARM Live test needs ARMUSER / ARMTOKEN.
"""
import csv
import datetime
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
TRANCHE = ROOT / "skills" / "arm-vaps"
CATALOG = ROOT / "skills" / "arm-instruments" / "catalog.csv"
SKILLS = sorted(p for p in TRANCHE.glob("arm-vap-*") if (p / "SKILL.md").exists())
IDS = [p.name for p in SKILLS]
ARMLIVE_QUERY = "https://adc.arm.gov/armlive/livedata/query"

pytestmark = pytest.mark.skipif(not SKILLS, reason="arm-vaps tranche not in this repo")


def catalog():
    with open(CATALOG, newline="") as fh:
        return {r["code"]: r for r in csv.DictReader(fh)}


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_report_pdf_still_resolves(skill):
    url = catalog()[skill.name[len("arm-vap-"):]]["pdf"]
    assert url == url.strip(), "catalog URL carries whitespace; strip it before requesting"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=60) as r:
            assert r.status == 200
            assert "pdf" in r.headers.get("Content-Type", ""), f"{url} no longer served as a PDF"
    except urllib.error.HTTPError as e:
        pytest.fail(f"{skill.name}: report {url} returned HTTP {e.code}")


@pytest.mark.parametrize("skill", SKILLS, ids=IDS)
def test_armlive_still_serves_the_example(skill):
    user, token = os.environ.get("ARMUSER"), os.environ.get("ARMTOKEN")
    if not (user and token):
        pytest.skip("ARMUSER / ARMTOKEN not set")
    inv_path = skill / "example_inventory.json"
    if not inv_path.exists():
        pytest.skip("no verified example for this product; see the skill's data section")
    inv = json.loads(inv_path.read_text())
    day = inv["filename"].split(".")[2]
    date = datetime.date(int(day[:4]), int(day[4:6]), int(day[6:8]))
    # ARM Live expands a single-date query to cover a whole day, and for some datastreams
    # that window lands on the neighbouring day, so ask for a +/- 1 day span.
    q = urllib.parse.urlencode({"user": f"{user}:{token}", "ds": inv["datastream"],
                                "start": (date - datetime.timedelta(days=1)).isoformat(),
                                "end": (date + datetime.timedelta(days=1)).isoformat(),
                                "wt": "json"})
    with urllib.request.urlopen(f"{ARMLIVE_QUERY}?{q}", timeout=90) as r:
        out = json.loads(r.read())
    assert out.get("status") == "success", f"{inv['datastream']}: status {out.get('status')!r}"
    assert inv["filename"] in out.get("files", []), (
        f"{inv['datastream']}: verified file {inv['filename']} no longer listed around {date}; "
        f"archive returned {out.get('num_found')} files")
