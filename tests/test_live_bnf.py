"""Live checks for skills/bnf/arm-bnf-site: the external facts it rests on.

Hits arm.gov and (with ARMUSER/ARMTOKEN set) ARM Live. Run weekly; a failure
means a source changed and the skill text needs a look.
"""
import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "skills" / "bnf" / "arm-bnf-site"
LIVE = bool(os.environ.get("ARMUSER") and os.environ.get("ARMTOKEN"))


@pytest.fixture(scope="module")
def k():
    ns, path = {}, SITE / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def test_locations_page_still_matches(k):
    live = {r["facility_code"]: r for r in k["bnf_locations_live"]()}
    for code, f in k["bnf_facilities"]().items():
        if f["lat"] is None:
            continue
        assert float(live[code]["latitude"]) == pytest.approx(f["lat"], abs=1e-6)
        assert float(live[code]["longitude"]) == pytest.approx(f["lon"], abs=1e-6)


def test_catalog_lists_radars(k):
    cs = {d["datastream"]: d for d in
          k["bnf_datastreams_live"](instrument_class="csapr")}
    assert cs["bnfcsapr2cfrS3.a1"]["data_available"]
    s4 = {d["instrument_class"] for d in k["bnf_datastreams_live"](facility="S4")}
    assert {"kasacr", "xsacr", "ldis"} <= s4


def test_citation_service_doi(k):
    cit = k["bnf_citation_live"]("bnfmetM1.b1")
    assert k["bnf_dois"]("bnfmetM1.b1")["doi"] in cit


@pytest.mark.skipif(not LIVE, reason="needs ARM Live credentials")
@pytest.mark.parametrize("ds,date,time,key", [
    ("bnfmetM1.b1", "2026-10-19", "000000", "m1"),
    ("bnfkasacrcfrspcxpolS4.a1", "2026-10-10", "235633", "s4_sacr")])
def test_file_position(k, tmp_path, ds, date, time, key):
    """One small file each (0.3 MB and 2 MB, sizes on 2026-10-20)."""
    act = pytest.importorskip("act")
    files = act.discovery.download_arm_data(
        os.environ["ARMUSER"], os.environ["ARMTOKEN"], ds, date, date,
        time=time, output=str(tmp_path))
    assert files, "ARM Live returned no file"
    got = k["bnf_file_position"](files[0])
    ref = k["bnf_positions"](key)
    assert got["lat"] == pytest.approx(ref["lat"], abs=1e-5)
    assert got["lon"] == pytest.approx(ref["lon"], abs=1e-5)
