"""Offline checks for skills/bnf/bnf-site-map.

The facility table, distances, panel layout and asset counts stated in
SKILL.md are compared with the kernel and its frozen CSVs. Geo-stack checks
skip where pandas, pyproj or cartopy are absent.
"""
import csv
import math
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = ROOT / "skills" / "bnf" / "bnf-site-map"
CAP = 65_536


def load():
    ns = {}
    path = MAP / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def rows(name):
    with open((MAP / name).resolve()) as f:
        return list(csv.DictReader(f))


def md_table(text, header):
    lines = text.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith(header))
    out = []
    for ln in lines[i + 2:]:
        if not ln.startswith("|"):
            break
        out.append([c.strip() for c in ln.strip("|").split("|")])
    return out


@pytest.fixture(scope="module")
def k():
    return load()


@pytest.fixture(scope="module")
def text():
    return (MAP / "SKILL.md").read_text()


def test_files_present_and_under_registry_cap():
    for name in ("SKILL.md", "kernel.py", "site_map_assets.csv",
                 "bnf_locations_page.csv"):
        path = MAP / name
        assert path.exists(), name
        assert len(path.read_text()) <= CAP, name


def test_facility_table_matches_page_csv(text):
    page = {r["facility"]: r for r in rows("bnf_locations_page.csv")}
    table = md_table(text, "| facility | role |")
    assert {r[0] for r in table} == set(page)
    for fac, _, lat, lon in table:
        assert float(lat) == pytest.approx(float(page[fac]["lat"]), abs=1e-6)
        assert float(lon) == pytest.approx(float(page[fac]["lon"]), abs=1e-6)
    assert page["S11"]["lat"] in ("0", "0.0")


def test_asset_count_stated(text):
    data = [r for r in rows("site_map_assets.csv") if r["group"] != "anchor"]
    m = re.search(r"`site_map_assets.csv` \((\d+) mapped assets: (\d+) ARM "
                  r"file positions and (\d+) non-ARM", text)
    arm = sum(r["group"] == "ARM" for r in data)
    assert tuple(map(int, m.groups())) == (len(data), arm, len(data) - arm)


def test_assets_and_config_agree(k):
    cfg = k["map_config"]()
    data = {r["key"]: r for r in rows("site_map_assets.csv")}
    for lab in ("lab_main", "lab_region", "lab_inset"):
        assert set(cfg[lab]) <= set(data), lab
    assert {c[0] for c in cfg["closeups"].values()} <= set(data)
    assert {x for leg in cfg["legs"] for x in leg[:2]} <= set(data)
    w, e, s, n = cfg["main"]
    iw, ie, i_s, i_n = cfg["inset"]
    for key, r in data.items():
        lat, lon = float(r["lat"]), float(r["lon"])
        if r["layer"] == "inset":
            assert iw <= lon <= ie and i_s <= lat <= i_n, key
            assert not (w <= lon <= e and s <= lat <= n), key
        else:
            assert w <= lon <= e and s <= lat <= n, key
    assert {r["group"] for r in data.values()} <= set(cfg["col"]) | {"anchor"}
    assert {r["marker"] for r in data.values()} <= set(cfg["size"]) | {""}
    assert {r["layer"] for r in data.values()} <= {"main", "detail", "inset",
                                                   "none"}


def test_arm_markers_are_file_positions_only():
    pos = {r["key"]: r for r in rows("../arm-bnf-site/"
                                     "bnf_instrument_positions.csv")}
    arm = [r for r in rows("site_map_assets.csv") if r["group"] == "ARM"]
    assert {r["key"] for r in arm} == set(pos)
    for r in arm:
        assert float(r["lat"]) == pytest.approx(float(pos[r["key"]]["lat"]))
    assert {r["key"] for r in arm if r["precise"] == "False"} == {
        "sonde_launch"}


def test_main_map_clusters_collapsed(k):
    main = [r for r in rows("site_map_assets.csv")
            if r["group"] == "ARM" and r["layer"] == "main"]
    for i, a in enumerate(main):
        for b in main[i + 1:]:
            d = k["haversine_m"](float(a["lat"]), float(a["lon"]),
                                 float(b["lat"]), float(b["lon"]))
            assert d >= 100, (a["key"], b["key"])


def test_no_census_or_ameriflux_duplicates():
    for r in rows("site_map_assets.csv"):
        assert "AmeriFlux US-" not in r["source"], r["key"]
        assert "County, Alabama" not in r["source"], r["key"]
        assert not r["source"].endswith(", Alabama"), r["key"]


def test_closeups_fit_layout_and_hold_their_site(k):
    pd = pytest.importorskip("pandas")
    cfg = k["map_config"]()
    main, inset, close = k["panel_rects"]()
    assert len(close) == len(cfg["closeups"])
    for r in [main, inset] + close:
        assert 0 <= r[0] and r[0] + r[2] <= 1
        assert 0 <= r[1] and r[1] + r[3] <= 1
    A = pd.read_csv(MAP / "site_map_assets.csv")
    boxes = k["closeup_boxes"](A)
    w, e, s, n = cfg["main"]
    for letter, (key, *_) in cfg["closeups"].items():
        b = boxes[letter]
        r = A[A.key == key].iloc[0]
        assert b[0] < r.lon < b[1] and b[2] < r.lat < b[3], letter
        assert w < b[0] and b[1] < e and s < b[2] and b[3] < n, letter
    tower = A[A.key.isin(["s10_tower", "s13", "s13_ecor", "s14", "s14_ecor"])]
    assert len(tower) == 5 and k["inside"](tower, boxes["c"]).all()
    for key, letter in (("improve_sips1", "b"), ("scan_2179", "h"),
                        ("1m4", "i"), ("sonde_launch", "b")):
        assert k["inside"](A[A.key == key], boxes[letter]).all(), key


def test_closeup_letters_on_main_labels(k):
    cfg = k["map_config"]()
    labels = {key: v[0] for key, v in cfg["lab_main"].items()}
    for letter, (key, *_) in cfg["closeups"].items():
        key = {"M1_S10": "m1"}.get(key, key)
        tags = re.search(r"\(([a-i, ]+)\)$", labels[key]).group(1)
        assert letter in tags.split(", "), letter


def test_asset_table_regenerates(k):
    pytest.importorskip("pandas")
    built = k["build_asset_table"]()
    data = rows("site_map_assets.csv")
    assert list(built.key) == [r["key"] for r in data]
    assert list(built.layer) == [r["layer"] for r in data]
    for (_, b), r in zip(built.iterrows(), data):
        assert b.lat == pytest.approx(float(r["lat"]), abs=1e-7)
        assert b.lon == pytest.approx(float(r["lon"]), abs=1e-7)


def test_distance_table_matches_geodesic(k, text):
    """Recomputed from the arm-bnf-site positions CSV, not the kernel."""
    pyproj = pytest.importorskip("pyproj")
    pos = {r["key"]: r for r in rows("../arm-bnf-site/"
                                     "bnf_instrument_positions.csv")}
    geod = pyproj.Geod(ellps="WGS84")
    table = md_table(text, "| leg | distance | bearing |")
    legs = k["map_config"]()["legs"]
    assert len(table) == len(legs)
    for (a, b, name, *_), (tname, dist, bear) in zip(legs, table):
        p, q = pos[a], pos[b]
        az, _, d = geod.inv(float(p["lon"]), float(p["lat"]),
                            float(q["lon"]), float(q["lat"]))
        assert tname == name
        assert dist == f"{d / 1000:.2f} km"
        assert bear == f"{az % 360:.0f}°"


def test_xyz_tile_arithmetic(k):
    assert k["xyz_tile"](0.0, 0.0, 1) == (1, 1)
    x, y = k["xyz_tile"](34.342481, -87.338177, 16)
    assert (x, y) == (16868, 26104)


def test_route_shield(k):
    f = k["route_shield"]
    assert f("US Hwy 278") == "US 278"
    assert f("State Hwy 33") == "AL 33"
    assert f("State Rte 157") == "AL 157"
    assert f("I- 65") == "I-65"
    assert f("Co Rd 23") is None


def test_platecarree_trap_at_bnf(k, text):
    """PROJ 9.8 ellipsoidal eqc drifts ~24 km near 34 N; lonlat_crs and
    Geodetic do not."""
    ccrs = pytest.importorskip("cartopy.crs")
    pyproj = pytest.importorskip("pyproj")
    lon, lat = -87.338177, 34.342481
    tm = k["local_tm"](k["map_config"]()["main"])
    truth = pyproj.Transformer.from_crs(4326, pyproj.CRS(tm.proj4_init),
                                        always_xy=True).transform(lon, lat)
    for crs in (k["lonlat_crs"](), ccrs.Geodetic()):
        x, y = tm.transform_point(lon, lat, crs)
        assert math.hypot(x - truth[0], y - truth[1]) < 0.01
    y_pc = tm.transform_point(lon, lat, ccrs.PlateCarree())[1]
    if abs(y_pc - truth[1]) < 1:
        pytest.skip("this PROJ build has linear eqc; the trap is absent")
    err = abs(y_pc - truth[1]) / 1000
    m = re.search(r"y error was ([\d.]+) km at M1", text)
    assert float(m.group(1)) == pytest.approx(err, abs=0.05)


def test_variant_table_matches_themes(k, text):
    table = md_table(text, "| variant | main map |")
    assert [r[0] for r in table] == list(k["map_themes"]())


def test_no_vap_classes_in_assets():
    vaps = {"ceilpblht", "interpsonde", "mwrret", "qcrad", "armbe",
            "sondeadjust", "aerioe", "pblhtsonde", "mfrsrcldod"}
    for r in rows("site_map_assets.csv"):
        assert not set(r["classes"].split(";")) & vaps, r["key"]


def test_fixed_closeup_slots_point_inside_their_panel(k):
    pd = pytest.importorskip("pandas")
    cfg = k["map_config"]()
    A = pd.read_csv(MAP / "site_map_assets.csv")
    boxes = k["closeup_boxes"](A)
    for letter, slots in cfg["lab_detail"].items():
        for key, (_, x, y, ha) in slots.items():
            assert k["inside"](A[A.key == key], boxes[letter]).all(), key
            assert 0 < x <= 1 and 0 < y < 1 and ha in ("left", "right")
