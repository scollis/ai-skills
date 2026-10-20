"""Helpers for the ARM Bankhead National Forest (BNF, AMF3) observatory.

The shipped CSVs were generated on 2026-10-20 from the ARM locations page,
the ARM catalog index and one opened ARM Live file per instrument class and
facility; the ``*_live`` helpers re-read those sources so drift can be seen.
"""
import csv
import json
import math
import os
import re
import urllib.parse
import urllib.request

BNF_FILES = ("bnf_facilities.csv", "bnf_instruments.csv",
             "bnf_instrument_audit.csv", "bnf_instrument_positions.csv",
             "bnf_dois.csv", "bnf_campaigns.csv", "bnf_radar_daily_files.csv",
             "bnf_radar_dqrs.csv")


def bnf_table(name):
    """Rows of one shipped CSV (name with or without .csv) as dicts of str."""
    here = os.path.dirname(bnf_table.__code__.co_filename)
    fn = name if name.endswith(".csv") else name + ".csv"
    with open(os.path.join(here, fn), newline="") as f:
        return list(csv.DictReader(f))


def num(value):
    """float(value), or None for an empty CSV cell."""
    return float(value) if value not in ("", None) else None


def bnf_facilities(code=None):
    """Facility records from the ARM locations page, keyed by code.

    lat/lon/alt_m are None where the page holds 0,0 (S11). n_classes and
    n_active count instrument classes in bnf_instrument_audit.csv.
    """
    out = {}
    for r in bnf_table("bnf_facilities"):
        for k in ("lat", "lon", "alt_m"):
            r[k] = num(r[k])
        r["n_classes"], r["n_active"] = int(r["n_classes"]), int(r["n_active"])
        r["page_is_active"] = r["page_is_active"] == "True"
        out[r["code"]] = r
    return out if code is None else out[code]


def bnf_instruments(facility=None, active=None):
    """Instrument class x facility rows with every datastream the catalog
    lists. active means an ARM Live file dated on or after 2026-08-01."""
    rows = bnf_table("bnf_instruments")
    for r in rows:
        r["active"] = r["active"] == "True"
    return [r for r in rows
            if (facility is None or r["facility"] == facility)
            and (active is None or r["active"] == active)]


def bnf_instrument_audit(flag=None, facility=None):
    """Position audit (2026-10-20): one row per instrument class x facility,
    read from the most recent a-level file (b-level where a-level is not
    served or holds no position). flag filters by prefix."""
    return [r for r in bnf_table("bnf_instrument_audit")
            if (flag is None or r["flag"].startswith(flag))
            and (facility is None or r["facility_code"] == facility)]


def bnf_positions(key=None):
    """Distinct file positions keyed by name (m1, s3_csapr2, s4_sacr, ...).

    kind 'fixed' rows group every instrument whose file stores the same
    position to 1e-5 deg; 'first fix' rows are launch or take-off points.
    """
    out = {}
    for r in bnf_table("bnf_instrument_positions"):
        for k in ("lat", "lon", "alt_m", "dist_m1_km", "bearing_from_m1_deg",
                  "offset_from_page_m"):
            r[k] = num(r[k])
        r["n_instruments"] = int(r["n_instruments"])
        out[r["key"]] = r
    return out if key is None else out[key]


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


def bnf_point(p):
    """(lat, lon) for a position key, a facility code (page value) or a pair."""
    if isinstance(p, (tuple, list)):
        return float(p[0]), float(p[1])
    pos = bnf_positions()
    if p in pos:
        return pos[p]["lat"], pos[p]["lon"]
    f = bnf_facilities(p)
    if f["lat"] is None:
        raise ValueError(f"{p}: the locations page holds no position")
    return f["lat"], f["lon"]


def bnf_distance(a, b):
    """Geodesic distance (km) and bearing (deg) from a to b; each is a
    bnf_positions() key, a facility code or a (lat, lon) pair."""
    d, az = geodesic_inverse(*bnf_point(a), *bnf_point(b))
    return dict(km=d / 1000, bearing_deg=az)


def bnf_dois(datastream=None):
    """ARM DOI, creators (mentors and developers) and title per datastream."""
    rows = bnf_table("bnf_dois")
    return rows if datastream is None else next(
        r for r in rows if r["datastream"] == datastream)


def bnf_campaigns(lead=None):
    """ARM field campaigns that list BNF (ARM campaign index, 2026-10-20)."""
    return [r for r in bnf_table("bnf_campaigns")
            if lead is None or lead.lower() in r["lead"].lower()]


def bnf_radar_gaps(datastream="bnfcsapr2cfrS3.a1", min_days=3):
    """Runs of at least min_days days with no ARM Live file, between the
    first and last day with data, as (first_day, last_day, n_days)."""
    rows = bnf_table("bnf_radar_daily_files")
    days = [(r["date"][:10], int(r[datastream])) for r in rows]
    on = [i for i, (_, n) in enumerate(days) if n > 0]
    gaps, start = [], None
    for i in range(on[0], on[-1] + 1):
        if days[i][1] == 0 and start is None:
            start = i
        elif days[i][1] > 0 and start is not None:
            if i - start >= min_days:
                gaps.append((days[start][0], days[i - 1][0], i - start))
            start = None
    return gaps


def bnf_file_position(path):
    """lat, lon, alt and the source name stored in one ARM netCDF file.

    Looks at variables first, then global attributes. A time series (moving
    platform) returns its first finite fix and n_fixes.
    """
    import numpy as np
    import xarray as xr
    names = (("lat", ("lat", "latitude")), ("lon", ("lon", "longitude")),
             ("alt", ("alt", "altitude")))
    out = {}
    with xr.open_dataset(path, decode_times=False) as ds:
        for key, cands in names:
            for n in cands:
                if n in ds.variables:
                    v = np.asarray(ds[n].values, dtype=float).ravel()
                    v = v[np.isfinite(v)]
                    if v.size:
                        out[key], out[key + "_src"] = float(v[0]), f"var:{n}"
                        out["n_fixes"] = int(v.size)
                        break
                if n in ds.attrs:
                    out[key], out[key + "_src"] = ds.attrs[n], f"attr:{n}"
                    break
    return out


def bnf_locations_live(site="bnf"):
    """Re-read the facility records embedded in the ARM locations page."""
    url = f"https://www.arm.gov/capabilities/observatories/{site}/locations"
    with urllib.request.urlopen(url, timeout=60) as r:
        html = r.read().decode("utf-8", "replace")
    m = re.search(r"const\s+locations\s*=\s*(\[.*?\]);", html, re.S)
    return json.loads(m.group(1)) if m else []


def bnf_datastreams_live(site="bnf", facility=None, instrument_class=None):
    """Datastreams for a site from ARM's public catalog index, with the
    per-datastream source class (armobs = instrument) and data_available."""
    query = ({"term": {"instrument_class_code": instrument_class}}
             if instrument_class else {"match_all": {}})
    body = json.dumps({"size": 3000, "query": query}).encode()
    req = urllib.request.Request("https://www.arm.gov/api/es/ds/_search",
                                 data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        hits = json.load(r)["hits"]["hits"]
    out = []
    for h in hits:
        s = h["_source"]
        for d in s.get("datastreams") or []:
            if d.get("site_code") != site:
                continue
            if facility and d.get("facility_code") != facility:
                continue
            out.append(dict(datastream=d.get("datastream"),
                            instrument_class=s.get("instrument_class_code"),
                            facility_code=d.get("facility_code"),
                            source_class=d.get("source_class_code"),
                            level=d.get("data_level_code"),
                            start_date=d.get("start_date"),
                            end_date=d.get("end_date"),
                            data_available=d.get("data_available")))
    return out


def bnf_citation_live(datastream, start="2024-10-01", end="2026-10-19"):
    """APA citation with DOI from the ARM citation service."""
    q = urllib.parse.urlencode(dict(id=datastream, citationType="apa",
                                    startDate=start, endDate=end))
    url = f"https://adc.arm.gov/citationservice/citation/datastream?{q}"
    with urllib.request.urlopen(url, timeout=60) as r:
        text = r.read().decode()
    return json.loads(text)["citation"].strip() if text.strip() else None
