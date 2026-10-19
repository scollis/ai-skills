"""Helpers for the non-ARM research assets around Utqiagvik (Barrow), Alaska."""
import csv
import json
import math
import os
import sys
import urllib.request


def utqiagvik_assets(network=None, operator=None):
    """The shipped asset table (37 rows, compiled 2026-10-19).

    Columns: name, operator, network, asset_type, lat, lon, elev_m, start_year,
    end_year, source_url, notes, coord_precision, accessed. Substring filters.
    """
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    with open(os.path.join(here, "utqiagvik_assets.csv")) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["lat"], r["lon"] = float(r["lat"]), float(r["lon"])
    return [r for r in rows
            if (network is None or network.lower() in r["network"].lower())
            and (operator is None or operator.lower() in r["operator"].lower())]


def neon_barr_plots():
    """All 515 NEON BARR observational plot-protocol locations (93 plot IDs).

    Read from the NEON API on 2026-10-19; each row's source is
    https://data.neonscience.org/api/v0/locations/<neon_location>.
    """
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    with open(os.path.join(here, "neon_barr_plots.csv")) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["lat"], r["lon"] = float(r["lat"]), float(r["lon"])
    return rows


def haversine_km(lat1, lon1, lat2, lon2):
    """Great-circle distance on a 6371 km sphere (about 0.3 percent accuracy)."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def assets_near(lat, lon, km=1.0):
    """Assets within km of a point, nearest first, with distance_km added."""
    out = []
    for r in utqiagvik_assets():
        d = haversine_km(lat, lon, r["lat"], r["lon"])
        if d <= km:
            out.append(dict(r, distance_km=round(d, 3)))
    return sorted(out, key=lambda r: r["distance_km"])


def neon_site_live(site="BARR"):
    """NEON site record from the public v0 API (no key needed)."""
    url = f"https://data.neonscience.org/api/v0/sites/{site}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["data"]


def neon_location_live(name):
    """One NEON named location, e.g. a tower or plot, with its coordinates."""
    url = f"https://data.neonscience.org/api/v0/locations/{name}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.load(r)["data"]
