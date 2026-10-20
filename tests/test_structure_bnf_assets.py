"""Offline checks for skills/bnf/bnf-research-assets.

Every table, count and quoted distance in SKILL.md is recomputed from the
shipped CSV and the kernel, so prose, data and code cannot drift apart.
"""
import csv
import gzip
import pathlib
import re
from collections import Counter

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "bnf" / "bnf-research-assets"
TEXT = (SKILL / "SKILL.md").read_text()
CAP = 65536


def load():
    ns = {}
    path = SKILL / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def md_table(header):
    lines = TEXT.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.strip().startswith(header))
    out = []
    for ln in lines[i + 2:]:
        if not ln.strip().startswith("|"):
            break
        out.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return out


@pytest.fixture(scope="module")
def k():
    return load()


@pytest.fixture(scope="module")
def raw():
    with open(SKILL / "bnf_region_assets.csv", newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def by_name(k):
    return {r["name"]: r for r in k["bnf_assets"]()}


def test_files_and_caps():
    for name in ("SKILL.md", "kernel.py", "bnf_region_assets.csv"):
        assert (SKILL / name).stat().st_size < CAP, name
    front = TEXT.split("---")[1]
    assert "name: bnf-research-assets" in front
    desc = re.search(r'description: "(.*)"', front).group(1)
    assert "<" not in desc and ">" not in desc


def test_row_count_matches_prose(k, raw):
    n = int(re.search(r"\((\d+) rows, compiled 2026-10-20\)", TEXT).group(1))
    assert n == len(raw) == len(k["bnf_assets"]())
    assert int(re.search(r"all (\d+) rows from the sources", TEXT).group(1)) == n


def test_rows_are_sourced(raw):
    assert len({r["name"] for r in raw}) == len(raw), "duplicate names"
    for r in raw:
        assert r["source_url"].startswith("https://"), r["name"]
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["accessed"]), r["name"]
        assert 31.0 < float(r["lat"]) < 37.5 and -90.5 < float(r["lon"]) < -84.0
        assert r["coord_precision"] and r["operator"] and r["agency"]


def test_m1_reference(k):
    m1 = k["bnf_m1"]()
    assert (m1["lat"], m1["lon"]) == (34.342481, -87.338177)
    assert "(34.342481, -87.338177" in TEXT


def test_distances_match_kernel(k, raw):
    for r in raw:
        d, b = k["from_m1"](float(r["lat"]), float(r["lon"]))
        assert float(r["distance_km"]) == d, r["name"]
        assert int(float(r["bearing_deg"])) == b, r["name"]
        fac, km = k["nearest_arm"](float(r["lat"]), float(r["lon"]))
        assert (r["nearest_arm"], float(r["nearest_arm_km"])) == (fac, km), r["name"]


def test_vincenty_matches_pyproj(k):
    pyproj = pytest.importorskip("pyproj")
    geod = pyproj.Geod(ellps="WGS84")
    for lat1, lon1, lat2, lon2 in [(34.342481, -87.338177, 34.93055, -86.08361),
                                   (34.342481, -87.338177, 32.950461, -87.393269),
                                   (34.342481, -87.338177, 34.3429, -87.3397)]:
        d, az = k["geodesic_inverse"](lat1, lon1, lat2, lon2)
        az_ref, _, d_ref = geod.inv(lon1, lat1, lon2, lat2)
        assert d == pytest.approx(d_ref, abs=0.01)
        assert az == pytest.approx(az_ref % 360, abs=1e-6)
    assert k["geodesic_inverse"](34.3, -87.3, 34.3, -87.3) == (0.0, 0.0)


def test_filters(k):
    rows = k["bnf_assets"](operator="noaa", within_km=80)
    assert rows and all("noaa" in r["operator"].lower() and r["distance_km"] <= 80
                        for r in rows)
    dist = [r["distance_km"] for r in k["bnf_assets"]()]
    assert dist == sorted(dist)
    near = k["assets_near"](34.342481, -87.338177, km=0.2)
    assert near[0]["name"].startswith("IMPROVE Sipsey")


def test_agency_table(raw):
    got = Counter(r["agency"] for r in raw)
    table = md_table("| agency | rows |")
    assert {a: int(n) for a, n in table} == dict(got)


CLASSES = {"WSR-88D radar": ("network", "NEXRAD WSR-88D"),
           "TDWR": ("network", "TDWR"),
           "NWS ASOS": ("asset_type", "surface station (ASOS)"),
           "AWOS": ("asset_type", "surface station (AWOS)"),
           "NWS COOP": ("network", "NWS COOP"),
           "USRCRN": ("network", "USRCRN (Alabama)"),
           "USCRN": ("network", "USCRN"),
           "radiosonde (active)": ("network", "IGRA2 radiosonde"),
           "NEON site": ("network", "NEON Domain 08 Ozarks Complex"),
           "NALMA station": ("network", "North Alabama Lightning Mapping Array"),
           "AERONET": ("network", "AERONET"),
           "NRCS SCAN": ("network", "SCAN"),
           "USGS IV gauge": ("network", "USGS NWIS stream gauges"),
           "IMPROVE": ("network", "IMPROVE"),
           "CASTNET": ("network", "CASTNET"),
           "NOAA PSL site": ("network", "NOAA PSL observing sites")}


def test_nearest_class_table(k):
    table = md_table("| class | nearest asset |")
    assert [t[0] for t in table] == list(CLASSES)
    for cls, name, dist, bearing in table:
        col, val = CLASSES[cls]
        pool = [r for r in k["bnf_assets"]() if r[col] == val
                and (cls != "radiosonde (active)" or r["status"] == "active")]
        best = pool[0]
        assert best["name"] == name, cls
        assert dist == f"{best['distance_km']:.2f} km", cls
        assert bearing == f"{int(best['bearing_deg'])}°", cls


def test_radar_table(k):
    table = md_table("| radar | distance |")
    want = [r for r in k["bnf_assets"]() if r["network"] in ("NEXRAD WSR-88D", "TDWR")]
    assert [t[0] for t in table] == [r["name"] for r in want]
    for (name, dist, bearing, elev), r in zip(table, want):
        assert dist == f"{r['distance_km']:.2f} km" and bearing == f"{int(r['bearing_deg'])}°"
        assert elev == f"{r['alt_m']:g} m"
    assert "KPAH is 329 km away" in TEXT


def test_colocation_table(k, by_name):
    table = md_table("| asset | ARM facility |")
    want = [r for r in k["bnf_assets"]() if r["nearest_arm_km"] <= 1.5
            and r["agency"] not in ("Census", "DOE")]
    assert sorted(t[0] for t in table) == sorted(r["name"] for r in want)
    for name, fac, sep in table:
        r = by_name[name]
        assert (fac, sep) == (r["nearest_arm"], f"{r['nearest_arm_km']:.2f} km")


def test_census_table(by_name):
    table = md_table("| Census geography | GEOID |")
    assert len(table) == 17
    for place, geoid, dist in table:
        r = by_name[place + ", Alabama"]
        assert r["ids"] == f"GEOID {geoid}"
        assert dist == f"{r['distance_km']:.2f} km"
        assert len(geoid) == (5 if place.endswith("County") else 7)


def sep(k, name, fac):
    r = k["bnf_assets"]()
    r = next(x for x in r if x["name"].startswith(name))
    la, lo_w = k["ARM_FACILITIES"][fac]
    return round(k["geodesic_inverse"](la, -lo_w, r["lat"], r["lon"])[0] / 1000, 2)


def test_quoted_distances(k, by_name):
    assert "SIPS1 (AQS 01-079-0002" in TEXT and "is 0.15 km from M1" in TEXT
    assert by_name["IMPROVE Sipsey Wilderness (SIPS1)"]["distance_km"] == 0.15
    assert "\"Bankhead National Forest\" is 0.19 km from M1" in TEXT
    assert by_name["HADS DCP Bankhead National Forest (BHFA1)"]["distance_km"] == 0.19
    assert sep(k, "NRCS SCAN Sudduth", "S40") == 0.23
    assert sep(k, "USGS Flint Creek Near Falkville", "S30") == 1.39
    assert "Falkville is 1.39 km from S30" in TEXT
    assert sep(k, "USGS Big Nance Creek", "S20") == 2.89
    assert "Courtland is 2.89 km from S20" in TEXT
    assert sep(k, "Posey Field AWOS", "U2") == 1.47
    seps = [sep(k, n, "S20") for n in ("Courtland Airport AWOS", "USRCRN Courtland",
                                       "NALMA station K", "NOAA PSL Courtland")]
    assert "4.7-5.3 km W of ARM S20" in TEXT
    assert round(min(seps), 1) == 4.7 and round(max(seps), 1) == 5.3
    wild = by_name["Sipsey Wilderness"]["notes"]
    assert "M1 is 1.48 km outside" in wild and "1.48 km outside the Sipsey" in TEXT


def test_quoted_counts(k):
    nalma = k["bnf_assets"](network="Lightning Mapping")
    assert len(nalma) == 14 and "NALMA has 14 VHF stations" in TEXT
    assert sum(r["status"] == "active" for r in nalma) == 9
    assert "9 were active" in TEXT
    rcrn = k["bnf_assets"](network="USRCRN")
    assert len(rcrn) == 4 and max(r["distance_km"] for r in rcrn) < 56
    gauges = k["bnf_assets"](network="USGS NWIS")
    assert len(gauges) == 5 and "(5 gauges as of 2026-10-20)" in TEXT
    neon = k["bnf_assets"](network="NEON")
    assert len(neon) == 6 and min(r["distance_km"] for r in neon) > 150
    sipsey = k["bnf_assets"](network="Wilderness")[0]
    assert "gis_acres 25851" in sipsey["notes"] and "25,851 GIS acres" in TEXT


def test_arm_rows_flagged(k):
    for r in k["bnf_assets"](network="AmeriFlux"):
        assert r["agency"] == "DOE" and r["nearest_arm_km"] < 0.05, r["name"]


def test_nalma_parser(k, tmp_path):
    body = ("Number of stations: 2\n"
            "Sta_info: A  firetower 34.8092586 -87.0357225 207.62 720 5 3\n"
            "Sta_info: K  courtland 34.6578669 -87.3436469 157.25 22 3 5\n"
            "Sta_data: A  firetower 80 12 70 2 100.0 24.33  A\n"
            "Sta_data: K  courtland 0 0 70 0 0.0 0.00  NA\n"
            "*** data ***\n1.0 34.5 -87.0 5000 0.5 10.0 0x3\n")
    path = tmp_path / "NALMA_test.dat.gz"
    with gzip.open(path, "wt") as f:
        f.write(body)
    sta = k["nalma_stations"](str(path))
    assert [s["id"] for s in sta] == ["A", "K"]
    assert sta[0]["active"] is True and sta[1]["active"] is False
    csv_k = k["bnf_assets"](network="Lightning Mapping")
    csv_k = next(r for r in csv_k if r["name"].startswith("NALMA station K"))
    assert (csv_k["lat"], csv_k["lon"]) == (sta[1]["lat"], sta[1]["lon"])
