"""Helpers for the ARM North Slope of Alaska (NSA) observatory, Utqiagvik.

Facility and position literals were generated on 2026-10-19 from the ARM
locations page and from one opened ARM Live file per datastream; the
``*_live`` helpers re-read the sources so drift can be detected.
"""
import csv
import json
import math
import os
import re
import sys
import urllib.request


def nsa_facilities(code=None):
    """NSA facility records as the ARM locations page published them.

    lat/lon are None where the page carries null or 0,0 (S1, S2, S10, S11, X1).
    X1, X3 and X10 are external-data facilities taken from the ARM catalog.
    """
    fac = {'C1': {'name': 'Central Facility, Barrow AK',
            'lat': 71.323,
            'lon': -156.615,
            'alt_m': 8.0,
            'start': '1997-12-11',
            'end': '2026-10-19',
            'source': 'ARM locations page '
                      '(arm.gov/capabilities/observatories/nsa/locations)'},
     'C2': {'name': 'Central Facility, Atqasuk AK',
            'lat': 70.4718,
            'lon': -157.407,
            'alt_m': 20.0,
            'start': '1999-08-21',
            'end': '2011-01-17',
            'source': 'ARM locations page '
                      '(arm.gov/capabilities/observatories/nsa/locations)'},
     'E10': {'name': 'Barrow, Alaska, extended facility colocated at main site',
             'lat': 71.323,
             'lon': -156.615,
             'alt_m': 8.0,
             'start': '2011-01-01',
             'end': '2026-10-19',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'E11': {'name': 'Point Barrow, Alaska (71.393, -156.422, 0)',
             'lat': 71.393,
             'lon': -156.422,
             'alt_m': 0.0,
             'start': '2011-01-01',
             'end': '2026-10-19',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'E12': {'name': 'Barrow, Alaska (Extended) at BEO',
             'lat': 71.27473611,
             'lon': -156.64119444,
             'alt_m': 10.0,
             'start': '2022-01-25',
             'end': '2026-10-19',
             'source': 'ARM locations page = nsamawsE12.b1 file (71.27473,-156.64119,10 '
                       'm); separation confirmed by Sturm et al. 2025 (10.2172/2569396), '
                       'which gives no numeric coordinates'},
     'E30': {'name': 'Barrow, Alaska, ARM instruments at NOAA facility in new building '
                     '(NAD83)',
             'lat': 71.32312,
             'lon': -156.61143,
             'alt_m': 11.0,
             'start': '2024-07-01',
             'end': '2026-10-19',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'F1': {'name': 'Barrow, Alaska: Gulfstream 159 Aircraft',
            'lat': 71.323,
            'lon': -156.615,
            'alt_m': 8.0,
            'start': '2015-06-01',
            'end': '2015-09-15',
            'source': 'ARM locations page '
                      '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S01': {'name': 'Supplemental 1',
             'lat': 71.323,
             'lon': -156.615,
             'alt_m': 8.0,
             'start': '2015-02-04',
             'end': '2026-10-19',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S02': {'name': 'Barrow, Alaska, supplement to NSA C1 for sonde launches (i.e. RIVAL '
                     'IOP)',
             'lat': 71.323,
             'lon': -156.609,
             'alt_m': 8.0,
             'start': '2017-06-01',
             'end': '2026-10-19',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S1': {'name': 'Supplemental 1, Barrow AK [temporary for IOP]',
            'lat': None,
            'lon': None,
            'alt_m': None,
            'start': '1999-01-28',
            'end': '1999-04-09',
            'source': 'ARM locations page '
                      '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S2': {'name': 'Supplemental 2, Atqasuk AK [temporary for IOP]',
            'lat': None,
            'lon': None,
            'alt_m': None,
            'start': '1999-05-20',
            'end': '1999-10-18',
            'source': 'ARM locations page '
                      '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S10': {'name': 'SALVO facility on tundra, 2km south of NSA',
             'lat': None,
             'lon': None,
             'alt_m': None,
             'start': '2019-05-01',
             'end': '2021-07-20',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'S11': {'name': 'SALVO facility on ice, 2km north of NSA',
             'lat': None,
             'lon': None,
             'alt_m': None,
             'start': '2019-05-01',
             'end': '2021-07-20',
             'source': 'ARM locations page '
                       '(arm.gov/capabilities/observatories/nsa/locations)'},
     'X1': {'name': 'External data (satellites, NOAA, models)',
            'lat': None,
            'lon': None,
            'alt_m': None,
            'start': '2011-09-01',
            'end': '2021-09-01',
            'source': 'ES ds index (no coords)'},
     'X3': {'name': 'NOAA BRW aerosol (AOS) data, new building (NAD83)',
            'lat': 71.32312,
            'lon': -156.61143,
            'alt_m': 11.0,
            'start': '2020-10-22',
            'end': '2026-10-17',
            'source': 'ARM file nsaaosnephdryX3.b1'},
     'X10': {'name': 'NWS Utqiagvik upper-air (PABR/70026)',
             'lat': 71.281,
             'lon': -156.789,
             'alt_m': 15.0,
             'start': '1996-03-31',
             'end': '2016-07-31',
             'source': 'ARM file nsanwsupa1sX10.b1 Release_Location attr'}}
    return fac if code is None else fac[code]


def nsa_positions(key=None):
    """Reference positions, each from a named source (file or page).

    c1_page is the facility coordinate on the locations page; c1_file is the
    site-nominal value most C1 datastreams store. Only dl, aeri, e10_ecor,
    e30_aos, xsapr and e12 are instrument-specific.
    """
    pos = {'c1_page': {'lat': 71.323,
                 'lon': -156.615,
                 'alt_m': 8.0,
                 'source': 'ARM locations page',
                 'datastream': None},
     'c1_file': {'lat': 71.323,
                 'lon': -156.609,
                 'alt_m': 8.0,
                 'source': 'ARM file nsametC1.b1.20250715.000000.cdf',
                 'datastream': 'nsametC1.b1'},
     'xsapr': {'lat': 71.324745,
               'lon': -156.66774,
               'alt_m': 17.0,
               'source': 'ARM file nsaxsaprcfrC1.a1.20250715.000008.nc',
               'datastream': 'nsaxsaprcfrC1.a1'},
     'e12': {'lat': 71.274734,
             'lon': -156.64119,
             'alt_m': 10.0,
             'source': 'ARM file nsamawsE12.b1.20250715.000006.nc',
             'datastream': 'nsamawsE12.b1'},
     'e11': {'lat': 71.393,
             'lon': -156.422,
             'alt_m': 0.0,
             'source': 'ARM file nsasebsE11.b1.20150217.000000.cdf',
             'datastream': 'nsasebsE11.b1'},
     'e10_sebs': {'lat': 71.325,
                  'lon': -156.608,
                  'alt_m': 5.0,
                  'source': 'ARM file nsasebsE10.b1.20250715.000000.cdf',
                  'datastream': 'nsasebsE10.b1'},
     'e10_ecor': {'lat': 71.32436,
                  'lon': -156.61482,
                  'alt_m': 4.0,
                  'source': 'ARM file nsaecorsfE10.b1.20260925.000000.nc',
                  'datastream': 'nsaecorsfE10.b1'},
     'e30_aos': {'lat': 71.32312,
                 'lon': -156.61143,
                 'alt_m': 11.0,
                 'source': 'ARM file nsaaosapsE30.b1.20250715.000000.nc',
                 'datastream': 'nsaaosapsE30.b1'},
     'dl': {'lat': 71.322947,
            'lon': -156.61609,
            'alt_m': 8.0,
            'source': 'ARM file nsadlppiC1.b1.20260925.120022.cdf',
            'datastream': 'nsadlppiC1.b1'},
     'aeri': {'lat': 71.32326,
              'lon': -156.60805,
              'alt_m': 28.0,
              'source': 'ARM file nsaaerisummaryC1.b1.20260925.001032.nc',
              'datastream': 'nsaaerisummaryC1.b1'},
     'sonde': {'lat': 71.32,
               'lon': -156.62,
               'alt_m': 13.9,
               'source': 'ARM file nsasondewnpnC1.b1.20250715.052900.cdf',
               'datastream': 'nsasondewnpnC1.b1'},
     'cimel': {'lat': 71.3122,
               'lon': -156.665,
               'alt_m': 8.0,
               'source': 'ARM file nsacsphotsdalunarfiltv3C1.a1.20260925.083546.nc',
               'datastream': 'nsacsphotsdalunarfiltv3C1.a1'},
     'nws_x10': {'lat': 71.281,
                 'lon': -156.789,
                 'alt_m': 15.0,
                 'source': 'ARM file nsanwsupa1sX10.b1.20150715.110002.cdf',
                 'datastream': 'nsanwsupa1sX10.b1'},
     'c2': {'lat': 70.4718,
            'lon': -157.407,
            'alt_m': 20.0,
            'source': 'ARM file nsametC2.b1.20100715.000000.cdf',
            'datastream': 'nsametC2.b1'}}
    return pos if key is None else pos[key]


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


def nsa_distance(a, b):
    """Distance (km) and bearing (deg) between two nsa_positions() keys."""
    p, q = nsa_positions(a), nsa_positions(b)
    d, az = geodesic_inverse(p["lat"], p["lon"], q["lat"], q["lon"])
    return dict(km=d / 1000, bearing_deg=az)


def nsa_instruments(facility=None, active=None):
    """Instrument class x facility table shipped with this skill.

    Columns: class, name, facility, datastreams, start, end, active. active
    means catalog end date on or after 2026-08-01 (catalog end dates equal to
    the query day are open-ended placeholders).
    """
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    with open(os.path.join(here, "nsa_instruments.csv")) as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["active"] = r["active"] == "True"
    return [r for r in rows
            if (facility is None or r["facility"] == facility)
            and (active is None or r["active"] == active)]


def nsa_locations_live(site="nsa"):
    """Re-read the facility records embedded in the ARM locations page."""
    url = f"https://www.arm.gov/capabilities/observatories/{site}/locations"
    with urllib.request.urlopen(url, timeout=60) as r:
        html = r.read().decode("utf-8", "replace")
    m = re.search(r"const\s+locations\s*=\s*(\[.*?\]);", html, re.S)
    return json.loads(m.group(1)) if m else []


def nsa_datastreams_live(site="nsa", facility=None, instrument_class=None):
    """Datastreams for a site from ARM's public catalog index.

    Returns dicts with datastream, instrument_class, facility_code, start_date,
    end_date, active and data_available.
    """
    query = ({"term": {"instrument_class_code": instrument_class}}
             if instrument_class else {"match_all": {}})
    body = json.dumps({"size": 1000, "query": query}).encode()
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
                            start_date=d.get("start_date"),
                            end_date=d.get("end_date"),
                            active=d.get("active"),
                            data_available=d.get("data_available")))
    return out


def nsa_file_position(path):
    """lat, lon, alt as stored in one ARM netCDF file (variables or attrs)."""
    import xarray as xr
    with xr.open_dataset(path, decode_times=False) as ds:
        out = {}
        for key, names in (("lat", ("lat", "latitude")),
                           ("lon", ("lon", "longitude")),
                           ("alt", ("alt", "altitude"))):
            for n in names:
                if n in ds.variables:
                    out[key] = float(ds[n].values.ravel()[0])
                    break
                if n in ds.attrs:
                    out[key] = ds.attrs[n]
                    break
        return out


def nsa_location_audit(flag=None, facility=None):
    """Most-recent-file position audit (2026-10-19), one row per datastream.

    Columns: instrument_class, facility_code, datastream, file, file_date,
    lat, lon, alt, lat_src, lat_dtype, mb, offset_from_page_m, flag.
    flag values include 'C1 nominal', 'rounded to 0.01 deg',
    'instrument-specific or facility value', 'bad: ...' and 'no position: ...'.
    """
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    with open(os.path.join(here, "nsa_location_audit.csv")) as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows
            if (flag is None or r["flag"].startswith(flag))
            and (facility is None or r["facility_code"] == facility)]


def nsa_instrument_audit(flag=None, facility=None):
    """Instrument-only position audit (2026-10-19): most recent a-level
    file, b-level where a-level is unserved or holds no better position.
    Columns as nsa_location_audit() plus level and a_level_datastream.
    """
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    with open(os.path.join(here, "nsa_instrument_audit.csv")) as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows
            if (flag is None or r["flag"].startswith(flag))
            and (facility is None or r["facility_code"] == facility)]
