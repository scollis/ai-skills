"""Offline checks for skills/bnf/arm-bnf-site.

Every coordinate, distance, count and table in SKILL.md is compared with the
kernel helpers and shipped CSVs it came from, so prose and data cannot drift.
"""
import csv
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "skills" / "bnf" / "arm-bnf-site"
TEXT = (SITE / "SKILL.md").read_text()


def load():
    ns, path = {}, SITE / "kernel.py"
    exec(compile(path.read_text(), str(path), "exec"), ns)
    return ns


def rows(name):
    with open(SITE / name, newline="") as f:
        return list(csv.DictReader(f))


def md_table(header):
    """Rows of the markdown table whose header line starts with header."""
    lines = TEXT.splitlines()
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


def test_frontmatter_and_files(k):
    head = TEXT.split("---")[1]
    assert "name: arm-bnf-site" in head
    assert "<" not in head and ">" not in head
    for fn in k["BNF_FILES"]:
        assert (SITE / fn).exists(), fn
    for p in SITE.iterdir():
        assert p.stat().st_size < 65_536, p.name


def test_facility_table_matches_csv(k):
    fac = k["bnf_facilities"]()
    table = md_table("| code | what it is")
    assert [r[0] for r in table] == list(fac)
    for code, role, lat, lon, alt, period, n, act in table:
        f = fac[code]
        assert role == f["role"], code
        if f["lat"] is None:
            assert lat == lon == alt == "—", code
        else:
            assert float(lat) == f["lat"] and float(lon) == f["lon"], code
            assert float(alt) == f["alt_m"], code
        assert period == f"{f['start']} – {f['end']}", code
        assert int(n) == f["n_classes"] and int(act) == f["n_active"], code


def test_class_counts_match_audit(k):
    audit = rows("bnf_instrument_audit.csv")
    for code, f in k["bnf_facilities"]().items():
        got = [r for r in audit if r["facility_code"] == code]
        assert f["n_classes"] == len(got), code
        assert f["n_active"] == sum(r["active"] == "True" for r in got), code
    m = re.search(r"Active classes at M1 \((\d+)\): ([^.]+)\.", TEXT)
    m1 = sorted(r["instrument_class"] for r in audit
                if r["facility_code"] == "M1" and r["active"] == "True")
    assert int(m.group(1)) == len(m1)
    assert [s.strip() for s in m.group(2).split(",")] == m1
    inst = k["bnf_instruments"]()
    assert {(r["class"], r["facility"]) for r in inst} == {
        (r["instrument_class"], r["facility_code"]) for r in audit}


def test_audit_is_instruments_only():
    audit = rows("bnf_instrument_audit.csv")
    levels = {r["level"][:1] for r in audit if r["level"]}
    assert levels <= {"a", "b"}
    assert not {r["instrument_class"] for r in audit} & {
        "ceilpblht", "interpsonde", "mwrret", "qcrad", "csapr2-cmac", "tropoe"}
    for r in audit:
        if r["level"].startswith("b") and r["a_level_datastream"]:
            assert r["lat_src"] == "" or "-air" in r["instrument_class"], r


def test_audit_counts_in_prose():
    audit = rows("bnf_instrument_audit.csv")
    counts = {}
    for r in audit:
        counts[r["flag"]] = counts.get(r["flag"], 0) + 1
    assert {f: int(n) for f, n in md_table("| flag | rows |")} == counts
    m = re.search(r"Of (\d+) rows \((\d+) classes at (\d+) facilities\), (\d+) "
                  r"carry a position: (\d+) from a-level\s+and (\d+) from b-level "
                  r"files, (\d+) of the latter", TEXT)
    pos = [r for r in audit if r["lat"]]
    assert int(m.group(1)) == len(audit)
    assert int(m.group(2)) == len({r["instrument_class"] for r in audit})
    assert int(m.group(3)) == len({r["facility_code"] for r in audit})
    assert int(m.group(4)) == len(pos)
    assert int(m.group(5)) == sum(r["level"].startswith("a") for r in pos)
    assert int(m.group(6)) == sum(r["level"].startswith("b") for r in pos)
    assert int(m.group(7)) == sum(r["level"].startswith("b")
                                  and bool(r["a_level_datastream"]) for r in pos)
    page = [float(r["offset_from_page_m"]) for r in audit
            if r["flag"] == "page value"]
    assert max(page) <= 0.4


def test_quoted_offsets():
    by = {(r["instrument_class"], r["facility_code"]): r
          for r in rows("bnf_instrument_audit.csv")}
    assert round(float(by["dl", "S40"]["offset_from_page_m"])) == 92
    assert round(float(by["ecor", "S40"]["offset_from_page_m"])) == 52
    m1 = [float(by[c, "M1"]["offset_from_page_m"]) for c in ("aeri", "csphot", "dl")]
    assert round(min(m1)) == 33 and round(max(m1)) == 48
    assert by["dl", "S1"]["flag"] == "bad: 0,0"
    assert float(by["sonde", "M1"]["first_lat"]) == pytest.approx(34.35, abs=1e-5)


def test_positions_table_matches_csv(k):
    pos = k["bnf_positions"]()
    table = md_table("| key | lat | lon |")
    assert [r[0] for r in table] == list(pos)
    for key, lat, lon, alt, facs, ins, dist in table:
        p = pos[key]
        assert float(lat) == pytest.approx(p["lat"], abs=1e-6), key
        assert float(lon) == pytest.approx(p["lon"], abs=1e-6), key
        assert float(alt) == p["alt_m"], key
        km, brg = dist.split(" km, ")
        d = k["bnf_distance"]("m1", key)
        assert float(km) == round(d["km"], 3), key
        if d["km"] > 0:
            assert int(brg.rstrip("°")) == round(d["bearing_deg"]), key
        n = p["n_instruments"]
        assert ins == (f"{n} classes" if n > 6
                       else p["instruments"].replace(";", ", ")), key


def test_positions_come_from_audit_rows(k):
    audit = rows("bnf_instrument_audit.csv")
    for key, p in k["bnf_positions"]().items():
        if p["kind"] != "fixed":
            continue
        here = [r for r in audit if r["lat"]
                and abs(float(r["lat"]) - p["lat"]) < 1e-5
                and abs(float(r["lon"]) - p["lon"]) < 1e-5]
        assert len(here) == p["n_instruments"], key
        assert sorted(r["instrument_class"] for r in here) == sorted(
            p["instruments"].split(";")), key


LEGS = {"S3 C-SAPR2 → M1": ("s3_csapr2", "m1"), "S4 SACR → M1": ("s4_sacr", "m1"),
        "S3 C-SAPR2 → S4 SACR": ("s3_csapr2", "s4_sacr"),
        "M1 → S10 tower": ("m1", "s10_tower"), "M1 → S20 Courtland": ("m1", "s20"),
        "M1 → S30 Falkville": ("m1", "s30"),
        "M1 → S40 Double Springs": ("m1", "s40"),
        "M1 → U2 take-off": ("m1", "u2_takeoff"), "S20 → S30": ("s20", "s30"),
        "S30 → S40": ("s30", "s40"), "S40 → S20": ("s40", "s20")}


def test_distance_table_recomputes(k):
    table = md_table("| leg | distance |")
    assert [r[0] for r in table] == list(LEGS)
    for leg, dist, bearing in table:
        d = k["bnf_distance"](*LEGS[leg])
        assert float(dist.split()[0]) == round(d["km"], 2), leg
        assert int(bearing.rstrip("°")) == round(d["bearing_deg"]), leg
    s4 = k["bnf_distance"]("s4_sacr", "m1")["km"]
    assert round(s4, 1) == 16.5 and "16.4 km" in TEXT


def test_distances_match_pyproj(k):
    pyproj = pytest.importorskip("pyproj")
    geod = pyproj.Geod(ellps="WGS84")
    pos = k["bnf_positions"]()
    for a, b in LEGS.values():
        p, q = pos[a], pos[b]
        az, _, d = geod.inv(p["lon"], p["lat"], q["lon"], q["lat"])
        got = k["bnf_distance"](a, b)
        assert got["km"] * 1000 == pytest.approx(d, abs=0.01)
        assert got["bearing_deg"] == pytest.approx(az % 360, abs=1e-6)
    assert k["geodesic_inverse"](34.3, -87.3, 34.3, -87.3) == (0.0, 0.0)


def test_quoted_u2_and_sonde_distances(k):
    posey = (34.28027778, -87.60055556)
    assert round(k["bnf_distance"]("U2", posey)["km"] * 1000) == 249
    assert round(k["bnf_distance"]("u2_takeoff", "U2")["km"] * 1000) == 203
    assert "249 m" in TEXT and "203 m" in TEXT
    d = k["bnf_distance"]("m1", "sonde_launch")
    assert round(d["km"], 2) == 0.85 and 337.5 <= d["bearing_deg"] < 360
    sides = [k["bnf_distance"](a, b)["km"] for a, b in
             (("s20", "s30"), ("s30", "s40"), ("s40", "s20"))]
    assert round(min(sides)) == 45 and round(max(sides)) == 55


def test_radar_gap_table(k):
    table = md_table("| radar datastream |")
    data = rows("bnf_radar_daily_files.csv")
    for ds, first, last, gaps in table:
        ds = ds.strip("`")
        on = [r["date"] for r in data if int(r[ds]) > 0]
        assert (first, last) == (on[0], on[-1]), ds
        want = "; ".join(f"{a} – {b} ({n} d)" for a, b, n in k["bnf_radar_gaps"](ds))
        assert gaps == want, ds
    cs = k["bnf_radar_gaps"]("bnfcsapr2cfrS3.a1")
    assert cs[0][2] == 209 and cs[1][2] == 124


def test_radar_dqrs_quoted():
    dq = {r["dqr"] for r in rows("bnf_radar_dqrs.csv")}
    for num in re.findall(r"D\d{6}\.\d+", TEXT):
        assert num in dq, num


def test_doi_table_matches_csv(k):
    table = md_table("| datastream | DOI |")
    assert len(table) >= 25
    for ds, doi, creators in table:
        r = k["bnf_dois"](ds.strip("`"))
        assert re.fullmatch(r"\[10\.5439/\d+\]\(https://doi\.org/10\.5439/\d+\)", doi)
        assert r["doi"] in doi
        names = r["creators"].split("; ")
        assert creators == ", ".join(names[:4]) + (" et al." if len(names) > 4 else "")
    assert len(rows("bnf_dois.csv")) == sum(
        1 for r in rows("bnf_instrument_audit.csv") if r["datastream"])


def test_campaign_table_matches_csv(k):
    table = md_table("| campaign | title |")
    camp = k["bnf_campaigns"]()
    assert len(table) == len(camp)
    for t, r in zip(table, camp):
        assert t[0] == r["acronym"] and t[3] == r["lead"]
        assert t[2] == f"{r['start']} – {r['end']}"
    assert not any("@" in v for r in camp for v in r.values())


def test_kernel_reads_csv_relative_to_itself(k, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert k["bnf_facilities"]("M1")["alt_m"] == 293.0
    assert k["bnf_positions"]("s3_csapr2")["facilities"] == "S3"
    assert len(k["bnf_instrument_audit"](facility="S4")) == 3
