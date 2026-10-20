"""Helpers for the non-ARM observing and context assets around ARM BNF."""
import csv
import gzip
import json
import math
import os
import urllib.parse
import urllib.request

M1_LAT = 34.342481
M1_LON_WEST = 87.338177
CSV_NAME = "bnf_region_assets.csv"
NUMERIC = ("lat", "lon", "alt_m", "distance_km", "bearing_deg", "nearest_arm_km")
# ARM BNF facility points from the locations page, (lat, west longitude);
# S1/S2 sit at M1, S11 is collocated with S10.
ARM_FACILITIES = {"M1": (34.342481, 87.338177), "S3": (34.630806, 87.133118),
                  "S4": (34.464279, 87.236001), "S10": (34.3437276, 87.35044401),
                  "S20": (34.653784, 87.292676), "S30": (34.384829, 86.927905),
                  "S40": (34.178796, 87.453905), "U2": (34.280111, 87.597858)}


def nearest_arm(lat, lon):
    """(facility, km) of the ARM BNF facility closest to a point."""
    best = None
    for code, (la, lo_w) in ARM_FACILITIES.items():
        d = geodesic_inverse(la, -lo_w, lat, lon)[0] / 1000
        if best is None or d < best[1]:
            best = (code, round(d, 2))
    return best


def bnf_m1():
    """ARM BNF M1 reference point (locations page) used for every distance."""
    return {"lat": M1_LAT, "lon": -M1_LON_WEST}


def geodesic_inverse(lat1, lon1, lat2, lon2):
    """WGS84 distance (m) and initial bearing (deg) by Vincenty's formula."""
    a, f = 6378137.0, 1 / 298.257223563
    b = a * (1 - f)
    big_l = math.radians(lon2 - lon1)
    u1 = math.atan((1 - f) * math.tan(math.radians(lat1)))
    u2 = math.atan((1 - f) * math.tan(math.radians(lat2)))
    su1, cu1, su2, cu2 = math.sin(u1), math.cos(u1), math.sin(u2), math.cos(u2)
    lam = big_l
    for _ in range(200):
        sl, cl = math.sin(lam), math.cos(lam)
        ss = math.hypot(cu2 * sl, cu1 * su2 - su1 * cu2 * cl)
        if ss == 0:
            return 0.0, 0.0
        cs = su1 * su2 + cu1 * cu2 * cl
        sig = math.atan2(ss, cs)
        sa = cu1 * cu2 * sl / ss
        c2a = 1 - sa * sa
        c2sm = cs - 2 * su1 * su2 / c2a if c2a else 0.0
        c = f / 16 * c2a * (4 + f * (4 - 3 * c2a))
        prev = lam
        lam = big_l + (1 - c) * f * sa * (
            sig + c * ss * (c2sm + c * cs * (2 * c2sm * c2sm - 1)))
        if abs(lam - prev) < 1e-12:
            break
    usq = c2a * (a * a - b * b) / (b * b)
    ka = 1 + usq / 16384 * (4096 + usq * (usq * (320 - 175 * usq) - 768))
    kb = usq / 1024 * (256 + usq * (usq * (74 - 47 * usq) - 128))
    ds = kb * ss * (c2sm + kb / 4 * (cs * (2 * c2sm * c2sm - 1) - kb / 6 * c2sm
                                     * (4 * ss * ss - 3) * (4 * c2sm * c2sm - 3)))
    az = math.degrees(math.atan2(cu2 * math.sin(lam),
                                 cu1 * su2 - su1 * cu2 * math.cos(lam)))
    return b * ka * (sig - ds), az % 360


def from_m1(lat, lon):
    """(distance_km, bearing_deg) from M1, rounded as stored in the CSV."""
    d, az = geodesic_inverse(M1_LAT, -M1_LON_WEST, lat, lon)
    return round(d / 1000, 2), round(az) % 360


def bnf_assets(operator=None, within_km=None, network=None, asset_type=None):
    """Rows of bnf_region_assets.csv, nearest first.

    operator, network and asset_type are case-insensitive substring filters;
    within_km keeps rows no farther than that from M1.
    """
    here = os.path.dirname(bnf_assets.__code__.co_filename)
    with open(os.path.join(here, CSV_NAME), newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in NUMERIC:
            r[k] = float(r[k]) if r[k] else None
    keep = []
    for r in rows:
        if operator and operator.lower() not in r["operator"].lower():
            continue
        if network and network.lower() not in r["network"].lower():
            continue
        if asset_type and asset_type.lower() not in r["asset_type"].lower():
            continue
        if within_km is not None and r["distance_km"] > within_km:
            continue
        keep.append(r)
    return sorted(keep, key=lambda r: r["distance_km"])


def assets_near(lat, lon, km=1.0):
    """Assets within km of any point, nearest first, with sep_km added."""
    out = []
    for r in bnf_assets():
        d = geodesic_inverse(lat, lon, r["lat"], r["lon"])[0] / 1000
        if d <= km:
            out.append(dict(r, sep_km=round(d, 3)))
    return sorted(out, key=lambda r: r["sep_km"])


def get_json(url, params=None, timeout=60):
    """GET a JSON document (plain urllib, no key)."""
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def nws_radar_live(station="KHTX"):
    """NWS API radar station record: (lat, lon, elevation_m, name)."""
    p = get_json("https://api.weather.gov/radar/stations/" + station)
    lon, lat = p["geometry"]["coordinates"][:2]
    return lat, lon, p["properties"]["elevation"]["value"], p["properties"]["name"]


def homr_station_live(qid="ICAO:KDCU"):
    """NCEI HOMR header for a station id: (name, lat, lon, por)."""
    base = "https://www.ncei.noaa.gov/access/homr/services/station/"
    hit = get_json(base + "search", {"qid": qid})["stationCollection"]["stations"]
    st = get_json(base + hit[0]["ncdcStnId"])["stationCollection"]["stations"][0]
    h = st["header"]
    return h["preferredName"], float(h["latitude_dec"]), float(h["longitude_dec"]), h["por"]


def neon_location_live(name="TOWER100876"):
    """One NEON named location (site, tower, met station) from the v0 API."""
    return get_json("https://data.neonscience.org/api/v0/locations/" + name)["data"]


def nalma_stations(path):
    """Station table from a NALMA level-1 .dat.gz header.

    Returns dicts with id, name, lat, lon, alt_m and active (True/False).
    """
    sta, act = [], {}
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("*** data ***"):
                break
            p = line.split()
            if line.startswith("Sta_info:"):
                sta.append(dict(id=p[1], name=p[2], lat=float(p[3]),
                                lon=float(p[4]), alt_m=float(p[5])))
            elif line.startswith("Sta_data:"):
                act[p[1]] = p[-1] == "A"
    for s in sta:
        s["active"] = act.get(s["id"])
    return sta
