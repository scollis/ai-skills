"""Live checks for the NSA tranche: the external facts the skills rest on.

Hits arm.gov, the NEON API and (with ARMUSER/ARMTOKEN set) ARM Live. Run
weekly; a failure means a source changed and the skill text needs a look.
"""
import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
NSA = ROOT / "skills" / "nsa"


def load(name):
    ns, path = {}, NSA / name / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


@pytest.fixture(scope="module")
def site():
    return load("arm-nsa-site")


def test_locations_page_still_matches(site):
    live = {r["facility_code"]: r for r in site["nsa_locations_live"]()}
    for code in ("C1", "C2", "E11", "E12", "E30"):
        f = site["nsa_facilities"](code)
        assert float(live[code]["latitude"]) == pytest.approx(f["lat"], abs=1e-6)
        assert float(live[code]["longitude"]) == pytest.approx(f["lon"], abs=1e-6)


def test_catalog_lists_xsapr_and_e12(site):
    xs = {d["datastream"] for d in
          site["nsa_datastreams_live"](instrument_class="xsapr")}
    assert "nsaxsaprcfrC1.a1" in xs
    e12 = {d["instrument_class"] for d in
           site["nsa_datastreams_live"](facility="E12")}
    assert {"srs", "spmf", "maws", "wb"} <= e12


def test_neon_barr_tower_position():
    k = load("utqiagvik-research-assets")
    tower = k["neon_location_live"]("TOWER104688")
    row = next(r for r in k["utqiagvik_assets"]() if "TOWER104688" in r["name"])
    assert tower["locationDecimalLatitude"] == pytest.approx(row["lat"], abs=1e-5)
    assert tower["locationDecimalLongitude"] == pytest.approx(row["lon"], abs=1e-5)


@pytest.mark.skipif(not (os.environ.get("ARMUSER") and os.environ.get("ARMTOKEN")),
                    reason="needs ARM Live credentials")
def test_xsapr_file_position(site, tmp_path):
    """One 15 MB X-SAPR file: the radar is on BARC, 1.9 km west of C1."""
    act = pytest.importorskip("act")
    files = act.discovery.download_arm_data(
        os.environ["ARMUSER"], os.environ["ARMTOKEN"], "nsaxsaprcfrC1.a1",
        "2025-07-15", "2025-07-15", time="000008", output=str(tmp_path))
    assert files, "ARM Live returned no file"
    got = site["nsa_file_position"](files[0])
    ref = site["nsa_positions"]("xsapr")
    assert got["lat"] == pytest.approx(ref["lat"], abs=1e-5)
    assert got["lon"] == pytest.approx(ref["lon"], abs=1e-5)
