"""Offline checks for the NSA site tranche (skills/nsa/).

Every coordinate, distance and count the three SKILL.md files state is
compared with the kernel literals and shipped CSVs it came from, so prose and
data cannot drift apart. The cartopy check is skipped where cartopy is absent.
"""
import csv
import math
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
NSA = ROOT / "skills" / "nsa"
SITE, ASSETS, MAP = (NSA / n for n in ("arm-nsa-site",
                                       "utqiagvik-research-assets",
                                       "utqiagvik-site-map"))


def load(skill):
    ns = {}
    path = skill / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def rows(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def md_table(text, header):
    """Rows of the markdown table whose header line starts with header."""
    lines = text.splitlines()
    i = next(k for k, ln in enumerate(lines) if ln.startswith(header))
    out = []
    for ln in lines[i + 2:]:
        if not ln.startswith("|"):
            break
        out.append([c.strip() for c in ln.strip("|").split("|")])
    return out


@pytest.fixture(scope="module")
def site():
    return load(SITE)


def test_tranche_present():
    for d in (SITE, ASSETS, MAP):
        assert (d / "SKILL.md").exists() and (d / "kernel.py").exists()


def test_facility_table_matches_kernel(site):
    fac = site["nsa_facilities"]()
    table = md_table((SITE / "SKILL.md").read_text(), "| code | what it is")
    assert [r[0] for r in table] == list(fac), "facility codes or order drifted"
    for code, _, lat, lon, period, *_ in table:
        f = fac[code]
        if f["lat"] is None:
            assert lat == "—" and lon == "—", code
        else:
            assert float(lat) == f["lat"] and float(lon) == f["lon"], code
        assert period == f"{f['start']} – {f['end']}", code


def test_class_counts_match_csv(site):
    table = md_table((SITE / "SKILL.md").read_text(), "| code | what it is")
    for code, *_, n, active in table:
        got = site["nsa_instruments"](code)
        assert int(n) == len(got), code
        assert int(active) == sum(r["active"] for r in got), code
    text = (SITE / "SKILL.md").read_text()
    m = re.search(r"Active classes at C1 \((\d+)\): ([^.]+)\.", text)
    c1 = sorted(r["class"] for r in site["nsa_instruments"]("C1", True))
    assert int(m.group(1)) == len(c1)
    assert [s.strip() for s in m.group(2).split(",")] == c1


def test_positions_table_matches_kernel(site):
    pos = site["nsa_positions"]()
    table = md_table((SITE / "SKILL.md").read_text(), "| key | lat | lon |")
    assert {r[0] for r in table} == set(pos)
    for key, lat, lon, *_ in table:
        assert float(lat) == pytest.approx(pos[key]["lat"], abs=1e-6), key
        assert float(lon) == pytest.approx(pos[key]["lon"], abs=1e-6), key


LEGS = {"C1 → E12": ("c1_page", "e12"), "C1 → X-SAPR": ("c1_page", "xsapr"),
        "E12 → X-SAPR": ("e12", "xsapr"), "C1 → E11": ("c1_page", "e11"),
        "C1 → C2": ("c1_page", "c2")}


@pytest.mark.parametrize("skill", [SITE, MAP], ids=lambda p: p.name)
def test_distance_tables_match_geodesic(site, skill):
    table = md_table((skill / "SKILL.md").read_text(), "| leg | distance |")
    assert table, f"{skill.name}: no distance table"
    for leg, dist, bearing in table:
        d = site["nsa_distance"](*LEGS[leg])
        assert float(dist.split()[0]) == round(d["km"], 2), leg
        assert int(bearing.rstrip("°")) == round(d["bearing_deg"]), leg


def test_vincenty_matches_pyproj(site):
    """geodesic_inverse is stdlib-only; check it against pyproj's Karney
    solver on legs from metres to ~100 km, and on a zero-length leg."""
    pyproj = pytest.importorskip("pyproj")
    geod = pyproj.Geod(ellps="WGS84")
    for lat1, lon1, lat2, lon2 in [(71.0, -156.6, 72.0, -156.6),
                                   (71.323, -156.615, 70.4718, -157.407),
                                   (71.323, -156.615, 71.3231, -156.6151)]:
        d, az = site["geodesic_inverse"](lat1, lon1, lat2, lon2)
        az_ref, _, d_ref = geod.inv(lon1, lat1, lon2, lat2)
        assert d == pytest.approx(d_ref, abs=0.01)
        assert az == pytest.approx(az_ref % 360, abs=1e-6)
    assert site["geodesic_inverse"](71.3, -156.6, 71.3, -156.6) == (0.0, 0.0)


def test_xsapr_is_offset_from_c1(site):
    d = site["nsa_distance"]("c1_page", "xsapr")
    assert 1.8 < d["km"] < 2.0 and 270 < d["bearing_deg"] < 280


def test_dois_are_arm_prefix():
    text = (SITE / "SKILL.md").read_text()
    table = md_table(text, "| datastream | DOI |")
    assert len(table) >= 30
    for ds, doi, _ in table:
        assert ds.strip("`").startswith("nsa"), ds
        assert re.search(r"\[10\.5439/\d+\]", doi), doi


def test_asset_table_matches_csv():
    data = rows(ASSETS / "utqiagvik_assets.csv")
    table = md_table((ASSETS / "SKILL.md").read_text(), "| name | operator |")
    assert len(table) == len(data) == 37
    for r, t in zip(data, table):
        assert t[0] == r["name"]
        assert float(t[2]) == float(r["lat"]) and float(t[3]) == float(r["lon"])


def test_assets_kernel_reads_csv():
    k = load(ASSETS)
    assert len(k["utqiagvik_assets"]()) == 37
    assert len(k["neon_barr_plots"]()) == 515
    near = k["assets_near"](71.3230, -156.6114, 0.75)
    assert near[0]["name"].startswith("Barrow Atmospheric Baseline")


def test_quoted_asset_distances():
    """Distances written into the assets prose."""
    k, text = load(ASSETS), (ASSETS / "SKILL.md").read_text()
    by = {r["name"]: r for r in k["utqiagvik_assets"]()}
    brw = by["Barrow Atmospheric Baseline Observatory (BRW)"]
    mag = by["USGS Barrow Magnetic Observatory (BRW)"]
    tower = by["NEON BARR tower (TOWER104688)"]
    d_mag = k["haversine_km"](brw["lat"], brw["lon"], mag["lat"], mag["lon"])
    assert f"{d_mag:.2f} km W of BRW" in text
    e12 = load(SITE)["nsa_positions"]("e12")
    d_t = k["haversine_km"](e12["lat"], e12["lon"], tower["lat"], tower["lon"])
    assert f"{d_t:.2f} km NE" in text


def test_map_assets_csv_and_config():
    k = load(MAP)
    cfg = k["map_config"]()
    data = rows(MAP / "site_map_assets.csv")
    assert len(data) == 37
    keys = {r["key"] for r in data}
    for lab in ("lab_main", "lab_c1", "lab_e12", "lab_e12_zoom"):
        assert set(cfg[lab]) <= keys, lab
    for a, b, *_ in cfg["triangle"]:
        assert {a, b} <= keys
    w, e, s, n = cfg["main"]
    for r in data:
        lat, lon = float(r["lat"]), float(r["lon"])
        assert s <= lat <= n and w <= lon <= e, r["key"]
    # every close-up label points at an asset inside that close-up
    for lab, box in (("lab_c1", cfg["c1_box"]), ("lab_e12", cfg["e12_box"])):
        for key in cfg[lab]:
            r = next(x for x in data if x["key"] == key)
            assert box[0] <= float(r["lon"]) <= box[1], key
            assert box[2] <= float(r["lat"]) <= box[3], key


def test_map_assets_agree_with_site_kernel(site):
    data = {r["key"]: r for r in rows(MAP / "site_map_assets.csv")}
    pos = site["nsa_positions"]()
    for key in ("c1_page", "xsapr", "e12", "aeri", "dl"):
        mk = {"c1_page": "c1_page"}.get(key, key)
        # audited float32 file values vs kernel literals: within float32 precision
        assert float(data[mk]["lat"]) == pytest.approx(pos[key]["lat"], abs=1e-5)
        assert float(data[mk]["lon"]) == pytest.approx(pos[key]["lon"], abs=1e-5)


def test_xyz_tile_arithmetic():
    k = load(MAP)
    assert k["xyz_tile"](0.0, 0.0, 1) == (1, 1)
    x, y = k["xyz_tile"](71.3265, -156.6265, 17)
    assert (x, y) == (8510, 27874)


def test_cartopy_platecarree_trap_is_real_and_avoided():
    """PROJ 9.8 made ellipsoidal eqc non-linear in latitude, so cartopy's
    PlateCarree drifts ~23 km at 71 N; lonlat_crs() and Geodetic do not."""
    ccrs = pytest.importorskip("cartopy.crs")
    pyproj = pytest.importorskip("pyproj")
    k = load(MAP)
    lon, lat = -156.6, 71.3225
    tm = ccrs.TransverseMercator(central_longitude=lon, central_latitude=lat)
    truth = pyproj.Transformer.from_crs(4326, pyproj.CRS(tm.proj4_init),
                                        always_xy=True).transform(lon, lat)
    for crs in (k["lonlat_crs"](), ccrs.Geodetic()):
        x, y = tm.transform_point(lon, lat, crs)
        assert math.hypot(x - truth[0], y - truth[1]) < 0.01
    y_pc = tm.transform_point(lon, lat, ccrs.PlateCarree())[1]
    if abs(y_pc - truth[1]) < 1:
        pytest.skip("this PROJ build has linear eqc; the trap is absent")
    assert abs(y_pc - truth[1]) > 10_000
    # Web Mercator is fine with true lon/lat input
    y3857 = pyproj.Transformer.from_crs(4326, 3857, always_xy=True).transform(
        lon, lat)[1]
    assert abs(ccrs.GOOGLE_MERCATOR.transform_point(lon, lat, ccrs.Geodetic())[1]
               - y3857) < 0.01
    # tiles_in puts a 3857 corner where lonlat_crs puts the same lon/lat
    proj = k["local_tm"]((-156.63, -156.62, 71.32, 71.33))
    x3, y3 = pyproj.Transformer.from_crs(4326, 3857, always_xy=True).transform(
        lon, lat)
    ext = k["tiles_in"](proj, (x3, x3 + 1, y3, y3 + 1))
    direct = proj.transform_point(lon, lat, k["lonlat_crs"]())
    assert math.hypot(ext[0] - direct[0], ext[2] - direct[1]) < 0.01


def test_location_audit_table_matches_csv():
    text = (SITE / "SKILL.md").read_text()
    data = rows(SITE / "nsa_location_audit.csv")
    table = md_table(text, "| flag | datastreams |")
    counts = {}
    for r in data:
        counts[r["flag"]] = counts.get(r["flag"], 0) + 1
    assert {f: int(n) for f, n in table} == counts
    m = re.search(r"Of (\d+) datastreams, (\d+) files carry a position", text)
    assert int(m.group(1)) == len(data)
    assert int(m.group(2)) == sum(1 for r in data if r["lat"])


def test_c1_nominal_label_count_matches_instrument_audit():
    data = rows(SITE / "nsa_instrument_audit.csv")
    n = sum(1 for r in data if r["flag"] == "C1 nominal")
    k = load(MAP)
    assert f"({n} instruments)" in k["map_config"]()["lab_c1"]["c1_file"][0]
    assets = {r["key"]: r for r in rows(MAP / "site_map_assets.csv")}
    assert assets["c1_file"]["label"] == f"C1 nominal ({n} instruments)"
    assert int(assets["c1_file"]["n"]) == n


def test_instrument_audit_has_no_vaps():
    data = rows(SITE / "nsa_instrument_audit.csv")
    assert {r["level"][0] for r in data} <= {"a", "b"}
    assert not {r["instrument_class"] for r in data} & {
        "ceilpblht", "interpsonde", "mwrret", "qcrad", "armbe", "sondeadjust"}
    assert sum(1 for r in data if r["lat"]) == int(re.search(
        r"Of (\d+) instrument rows,\s+(\d+) carry a position",
        (SITE / "SKILL.md").read_text()).group(2))


def test_e10_is_not_drawn_as_a_site():
    k = load(MAP)
    cfg = k["map_config"]()
    labels = [v[0] for lab in ("lab_main", "lab_c1", "lab_e12") for v in
              cfg[lab].values()]
    labels += [r["label"] for r in rows(MAP / "site_map_assets.csv")]
    assert not any("E10" in t for t in labels)


def test_variant_table_matches_themes():
    k = load(MAP)
    table = md_table((MAP / "SKILL.md").read_text(), "| variant | main map |")
    assert [r[0] for r in table] == list(k["map_themes"]())
    for r in table:
        has = bool(k["map_themes"]()[r[0]]["details"])
        assert has == (not r[2].startswith("none")), r[0]
