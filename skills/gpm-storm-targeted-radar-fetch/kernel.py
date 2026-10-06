"""Helpers for GPM DPR overpass screening and ARM Live radar fetching.

Workflow this supports: use the GPM DPR swath as the storm detector over a ground
radar domain (surface gauges cannot do this job -- see SKILL.md), then fetch only the
few ground-radar volumes that bracket each precipitating overpass.

Built for ARM C-SAPR2 at BNF but the geometry and ARM Live calls are site-agnostic.
Method follows the ERAD2026 GPM-API short-course notebook on spaceborne-ground radar
calibration (Ghiggi et al.); see SKILL.md for full citations.
"""
import json
import os
import urllib.parse
import urllib.request

import numpy as np

CMR_GRANULES = "https://cmr.earthdata.nasa.gov/search/granules.json"
ARMLIVE = "https://adc.arm.gov/armlive/livedata"
EARTH_R = 6371000.0


def cmr_overpasses(site_lat, site_lon, start, end, short_name="GPM_2AKu",
                   version="08", page_size=200, timeout=90):
    """Granules whose swath contains a point, via a NASA CMR point query.

    CMR is authoritative for overpass screening. Do NOT propagate a TLE for this: at
    ~7.3 km/s a 60 s epoch error displaces the ground track ~440 km.

    NOTE the version string matters and fails SILENTLY -- an unavailable version
    returns zero granules with HTTP 200. GPM 2AKu is currently '08' (files are V08A);
    '07' returns nothing. Pass version=None to let CMR choose.
    """
    out = []
    for a, b in month_chunks(start, end):
        v = f"&version={version}" if version else ""
        q = (f"{CMR_GRANULES}?short_name={short_name}{v}"
             f"&point={site_lon},{site_lat}&temporal={a}T00:00:00Z,{b}T00:00:00Z"
             f"&page_size={page_size}")
        with urllib.request.urlopen(q, timeout=timeout) as r:
            d = json.load(r)
        for e in d.get("feed", {}).get("entry", []):
            gid = e.get("producer_granule_id", "")
            out.append(dict(granule=gid, time_start=e.get("time_start", ""),
                            time_end=e.get("time_end", ""),
                            orbit=gid.split(".")[-3] if gid.count(".") >= 3 else ""))
    out.sort(key=lambda r: r["time_start"])
    return out


def month_chunks(start, end):
    """Split a date range into <=15-day spans to stay inside CMR paging limits."""
    import datetime as dt
    a = dt.date.fromisoformat(str(start)[:10])
    b = dt.date.fromisoformat(str(end)[:10])
    cur = a
    while cur < b:
        nxt = min(b, cur + dt.timedelta(days=15))
        yield cur.isoformat(), nxt.isoformat()
        cur = nxt


def dpr_domain_crossing(ds, site_lat, site_lon, domain_km=115.0):
    """True crossing time and in-domain footprint counts for one DPR granule.

    Two traps this guards:

    1. The granule MIDPOINT is not the crossing time. A granule spans a full ~93 min
       orbit; the domain crossing is a ~30 s moment that can sit anywhere inside it
       (13.5 min from the midpoint in a verified BNF case).
    2. lat/lon are (cross_track, along_track) while `time` is indexed ALONG-TRACK
       only. np.unravel_index(argmin(dist)) returns (i_cross, j_along), so the time
       must be read with the ALONG-track index. Using the cross-track index gave a
       33-minute error that looked plausible because it fell inside the granule.
    """
    lat = np.asarray(ds["lat"].values)
    lon = np.asarray(ds["lon"].values)
    t = np.asarray(ds["time"].values)
    if lat.ndim != 2:
        raise ValueError("expected 2-D (cross_track, along_track) lat/lon")
    ax_along = 1 if lat.shape[1] == t.shape[0] else 0
    d = np.hypot((lat - site_lat) * 111.0,
                 (lon - site_lon) * 111.0 * np.cos(np.radians(site_lat)))
    i, j = np.unravel_index(np.nanargmin(d), d.shape)
    j_along = j if ax_along == 1 else i
    inr = d < domain_km
    jj = np.where(inr.any(axis=0 if ax_along == 1 else 1))[0]
    fp = np.asarray(ds["flagPrecip"].values) if "flagPrecip" in ds else None
    prec = (fp > 0) & inr if fp is not None else np.zeros_like(inr)
    return dict(cross_time=str(t[j_along])[:19], min_dist_km=float(d[i, j]),
                idx_along=int(j_along), idx_cross=int(i if ax_along == 1 else j),
                n_footprints_domain=int(inr.sum()), n_precip_domain=int(prec.sum()),
                cross_start=str(t[jj.min()])[:19] if jj.size else "",
                cross_end=str(t[jj.max()])[:19] if jj.size else "",
                frac_precip=float(prec.sum() / max(inr.sum(), 1)))


def armlive_query(user, token, datastream, start, end, timeout=120):
    """List ARM Live files for a datastream over a time range."""
    q = (f"{ARMLIVE}/query?user={user}:{token}&ds={urllib.parse.quote(datastream)}"
         f"&start={start}&end={end}&wt=json")
    with urllib.request.urlopen(q, timeout=timeout) as r:
        return json.load(r).get("files", []) or []


def armlive_file_size(user, token, filename, timeout=90):
    """Byte size of an ARM Live file via HTTP HEAD -- transfers no data.

    This is how you tell scan types apart when the filename carries no scan token.
    In bnfcsapr2cfrS3.a1, PPI volumes are ~200 MB and RHIs ~3 MB, interleaved on a
    ~16 min cycle; sizing first avoids downloading gigabytes of the wrong scan type.
    """
    url = (f"{ARMLIVE}/saveData?user={user}:{token}"
           f"&file={urllib.parse.quote(filename)}")
    try:
        with urllib.request.urlopen(
                urllib.request.Request(url, method="HEAD"), timeout=timeout) as r:
            return int(r.headers.get("Content-Length", 0))
    except Exception:
        return -1


def select_scans_by_size(user, token, filenames, min_bytes=20_000_000,
                         max_bytes=None, cache=None):
    """Filter an ARM Live file list to one scan class by size (HEAD only)."""
    keep = []
    cache = cache if cache is not None else {}
    for fn in sorted(filenames):
        if fn not in cache:
            cache[fn] = armlive_file_size(user, token, fn)
        n = cache[fn]
        if n >= min_bytes and (max_bytes is None or n <= max_bytes):
            keep.append(fn)
    return keep


def filename_time(filename):
    """Parse the ARM datastream timestamp from a filename -> numpy datetime64."""
    import re
    m = re.search(r"\.(\d{8})\.(\d{6})\.", filename)
    if not m:
        raise ValueError(f"no ARM timestamp in {filename}")
    d, t = m.groups()
    return np.datetime64(f"{d[:4]}-{d[4:6]}-{d[6:]}T{t[:2]}:{t[2:4]}:{t[4:]}")


def beam_height(range_m, elevation_deg, radar_alt_m=0.0):
    """4/3-earth beam-centre height in metres MSL."""
    r = np.asarray(range_m, dtype="f8")
    ke = 4.0 / 3.0 * EARTH_R
    return (np.sqrt(r ** 2 + ke ** 2
                    + 2.0 * r * ke * np.sin(np.radians(elevation_deg)))
            - ke + radar_alt_m)


def ground_range_azimuth(lat0, lon0, lat1, lon1):
    """Great-circle distance (m) and forward azimuth (deg) from point 0 to point 1."""
    p1, p2 = np.radians(lat0), np.radians(lat1)
    dl = np.radians(lon1 - lon0)
    d = 2.0 * EARTH_R * np.arcsin(np.sqrt(
        np.sin((p2 - p1) / 2.0) ** 2
        + np.cos(p1) * np.cos(p2) * np.sin(dl / 2.0) ** 2))
    brg = np.degrees(np.arctan2(
        np.sin(dl) * np.cos(p2),
        np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl))) % 360.0
    return float(d), float(brg)
