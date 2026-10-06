
"""Helpers for DERECHOS soil-property work: IEM ISUSM, USDA AWDB/SCAN, NRCS SSURGO."""
import io
import json

IEM = "https://mesonet.agron.iastate.edu"
AWDB = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"
SDA = "https://sdmdataaccess.nrcs.usda.gov/Tabular/post.rest"

SOILVUE_DEPTHS_IN = (2, 4, 8, 12, 14, 16, 20, 24, 28, 30, 32, 36, 40, 42, 52)
LEGACY_T_DEPTHS_IN = (4, 12, 24, 50)
LEGACY_VWC_DEPTHS_IN = (12, 24, 50)
ISUSM_MODES = ("hourly", "daily", "inversion")
DEPTH_IN_TO_CM = {2: 5, 4: 10, 8: 20, 12: 30, 14: 36, 16: 41, 20: 51, 24: 61,
                  28: 71, 30: 76, 32: 81, 36: 91, 40: 102, 42: 107, 50: 127, 52: 132}


def isusm_soil_varlist(mode=None):
    """Every soil-bearing `vars=` code the IEM isusm.py CGI accepts, per mode."""
    if mode is None:
        mode = "daily"
    sv = ["sv"]
    if mode == "daily":
        base = []
        for d in LEGACY_T_DEPTHS_IN:
            base += ["soil%02dtn" % d, "soil%02dt" % d, "soil%02dtx" % d]
        base += ["soil%02dvwc" % d for d in LEGACY_VWC_DEPTHS_IN]
        return base + sv
    base = ["soil%02dt" % d for d in LEGACY_T_DEPTHS_IN]
    base += ["soil%02dvwc" % d for d in LEGACY_VWC_DEPTHS_IN]
    return base + sv


def isusm_soil(stations, start, end, mode=None, soil_vars=None, timeres=None,
               qcflags=False, tz="UTC", sentinel_to_nan=True, sv_to_percent=False,
               timeout=1800):
    """Fetch ISU Soil Moisture Network soil data from the IEM isusm.py CGI.

    mode: 'daily' | 'hourly' | 'inversion' (the service validates against exactly
    these three). timeres='minute' with mode='hourly' yields 1-minute data.
    soil_vars=None asks for the full soil set for that mode (see
    isusm_soil_varlist) - omitting `vars` entirely gets you only the legacy
    4/12/24/50 in temperature and 12/24/50 in VWC columns even at a SoilVue station.

    Units, unchanged across all three cadences: soil*t / sv_t* deg F,
    soil*vwc PERCENT, sv_vwc* FRACTION (0-1). -99 is the missing sentinel and
    na=blank does NOT convert it; sentinel_to_nan does.
    """
    import requests
    import pandas as pd
    if isinstance(stations, str):
        stations = [stations]
    if mode is None:
        mode = "daily"
    if soil_vars is None and mode != "inversion":
        soil_vars = isusm_soil_varlist(mode)

    def stamp(v):
        v = str(v)
        return v if "T" in v else v + "T00:00:00Z"

    p = {"station": stations, "format": "comma", "mode": mode, "tz": tz,
         "na": "blank", "sts": stamp(start), "ets": stamp(end)}
    if soil_vars:
        p["vars"] = list(soil_vars)
    if timeres:
        p["timeres"] = timeres
    if qcflags:
        p["qcflags"] = "1"
    r = requests.get(IEM + "/cgi-bin/request/isusm.py", params=p, timeout=timeout)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    if sentinel_to_nan:
        for c in df.columns:
            if c in ("station", "valid"):
                continue
            v = pd.to_numeric(df[c], errors="coerce")
            df[c] = v.mask(v < -90)
    if sv_to_percent:
        for c in [c for c in df.columns if c.startswith("sv_vwc")]:
            df[c] = pd.to_numeric(df[c], errors="coerce") * 100.0
    return df


def isusm_soil_audit(df, flat_run=7):
    """Per-station, per-depth sensor health audit of an ISUSM daily frame.

    Input: isusm_soil(..., mode='daily') output (sentinel_to_nan either way).
    Returns one row per (station, variable) with completeness plus the failure
    modes that masquerade as valid data: sentinel counts, physically impossible
    values, longest constant run, modal-value fraction, and step-change counts.
    verdict: ok | some_impossible | impossible_values | pinned_flatlined |
    intermittent | sentinel_only | absent.
    """
    import numpy as np
    import pandas as pd
    soilcols = [c for c in df.columns if c.startswith(("soil", "sv_"))]
    out = []
    for stn, g in df.groupby("station"):
        g = g.sort_values("valid")
        dates = pd.to_datetime(g["valid"])
        span = (dates.max() - dates.min()).days + 1
        for c in soilcols:
            v = pd.to_numeric(g[c], errors="coerce")
            sent = v.notna() & (v < -90)
            vv = v.where(~sent)
            is_frac = c.startswith("sv_vwc")
            is_vwc = "vwc" in c
            hi = 1.0 if is_frac else (100.0 if is_vwc else 200.0)
            lo = 0.0 if is_vwc else -60.0
            bad = vv.notna() & ((vv < lo) | (vv > hi))
            ok = vv.notna() & ~bad
            nv = int(ok.sum())
            row = dict(station=stn, variable=c, kind=("vwc" if is_vwc else "temp"),
                       sensor=("soilvue" if c.startswith("sv_") else "legacy"),
                       depth_in=int("".join(ch for ch in c if ch.isdigit()) or 0),
                       days_returned=len(g), span_days=span,
                       n_present=int(v.notna().sum()), n_sentinel=int(sent.sum()),
                       n_impossible=int(bad.sum()), n_valid=nv)
            if nv:
                s = vv.where(ok).dropna()
                runs = s.groupby((s != s.shift()).cumsum()).size()
                modal = s.round(4).value_counts()
                step = 15.0 if (is_vwc and not is_frac) else (0.15 if is_frac else 10.0)
                row.update(first_valid=str(dates[ok].min().date()),
                           last_valid=str(dates[ok].max().date()),
                           completeness=round(nv / span, 4),
                           median=round(float(s.median()), 3),
                           p05=round(float(s.quantile(.05)), 3),
                           p95=round(float(s.quantile(.95)), 3),
                           max_run=int(runs.max()),
                           flat_frac=round(float(runs[runs >= flat_run].sum() / nv), 4),
                           modal_value=float(modal.index[0]),
                           modal_frac=round(float(modal.iloc[0] / nv), 4),
                           n_steps=int((s.diff().abs() > step).sum()))
            else:
                row.update(first_valid=None, last_valid=None, completeness=0.0,
                           median=np.nan, p05=np.nan, p95=np.nan, max_run=0,
                           flat_frac=np.nan, modal_value=np.nan, modal_frac=np.nan,
                           n_steps=0)
            if nv == 0:
                vd = "absent" if row["n_present"] == 0 else "sentinel_only"
            elif row["n_impossible"] > 0.10 * nv:
                vd = "impossible_values"
            elif row["modal_frac"] > 0.5 or row["flat_frac"] > 0.5:
                vd = "pinned_flatlined"
            elif row["completeness"] < 0.5:
                vd = "intermittent"
            elif row["n_impossible"] > 0.02 * nv:
                vd = "some_impossible"
            else:
                vd = "ok"
            row["verdict"] = vd
            out.append(row)
    return pd.DataFrame(out)


def isusm_live_depths():
    """Per-station sensor depth inventory from IEM's live AgClimate CSV (SI units).

    /agclimate/isusm.csv reports current values with depth lists embedded in the
    header: 'depth [m]#SOILT [K]#SOILMP [%]' with ';'-separated values per block.
    This is the cheapest way to see which depths a station is reporting TODAY.
    """
    import requests
    import pandas as pd
    r = requests.get(IEM + "/agclimate/isusm.csv", timeout=180)
    r.raise_for_status()
    rows = list(io.StringIO(r.text))
    hdr = rows[0].rstrip("\n").split(",")
    icol = [i for i, h in enumerate(hdr) if h.startswith("depth [m]")][0]
    out = []
    for line in rows[1:]:
        f = line.rstrip("\n").split(",")
        if len(f) <= icol:
            continue
        blk = f[icol].split("#")
        depths = [float(x) for x in blk[0].split(";") if x] if blk[0] else []
        temps = [x for x in blk[1].split(";")] if len(blk) > 1 else []
        vwcs = [x for x in blk[2].split(";")] if len(blk) > 2 else []
        out.append(dict(station=f[0], lat=float(f[1]), lon=float(f[2]), valid=f[3],
                        elev_m=float(f[4]), depths_m=depths, soilt_K=temps, vwc_pct=vwcs,
                        n_depths=len(depths)))
    return pd.DataFrame(out)


def awdb_stations(state_codes=None, network="SCAN", with_elements=True):
    """USDA AWDB station metadata. Filtering is via stationTriplets wildcards only.

    There is NO stateCds/state parameter: an unrecognised query parameter is
    silently IGNORED and the full national list comes back with HTTP 200.
    """
    import requests
    import pandas as pd
    if state_codes is None:
        state_codes = ["IA", "IL"]
    trip = ",".join("*:%s:%s" % (s, network) for s in state_codes)
    p = {"stationTriplets": trip, "activeOnly": "false"}
    if with_elements:
        p["returnStationElements"] = "true"
    r = requests.get(AWDB + "/stations", params=p, timeout=300)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def awdb_soil_series(triplet, begin, end, elements=None, duration="DAILY"):
    """SCAN/AWDB soil moisture (SMS, percent) and soil temperature (STO, degF).

    Depths arrive as negative INCHES in stationElement.heightDepth. endDate
    2100-01-01 in metadata means 'active', not a real end date.
    """
    import requests
    import pandas as pd
    if elements is None:
        elements = "SMS:*,STO:*"
    r = requests.get(AWDB + "/data", params={"stationTriplets": triplet,
                     "elements": elements, "duration": duration,
                     "beginDate": begin, "endDate": end, "returnFlags": "true"},
                     timeout=600)
    r.raise_for_status()
    rows = []
    for stn in r.json():
        for blk in stn.get("data", []):
            se = blk["stationElement"]
            for v in blk.get("values", []):
                rows.append(dict(station=stn["stationTriplet"],
                                 element=se["elementCode"],
                                 depth_in=abs(se.get("heightDepth") or 0),
                                 date=v.get("date"), value=v.get("value"),
                                 qc_flag=v.get("qcFlag")))
    return pd.DataFrame(rows)


def sda_query(sql, timeout=600):
    """Run SQL against the NRCS Soil Data Access tabular service; returns a DataFrame."""
    import requests
    import pandas as pd
    r = requests.post(SDA, json={"query": sql, "format": "JSON+COLUMNNAME"},
                      timeout=timeout)
    r.raise_for_status()
    j = r.json()
    if "Table" not in j:
        raise RuntimeError("SDA returned no Table: %s" % str(j)[:300])
    t = j["Table"]
    return pd.DataFrame(t[1:], columns=t[0])


def sda_point_profile(lat, lon, major_only=True):
    """SSURGO map unit / component / horizon profile at a lat-lon point.

    A map unit holds SEVERAL components with comppct_r percentages; a query that
    does not filter or aggregate returns all of them interleaved. major_only=True
    keeps majcompflag='Yes'; take the max comppct_r row for the dominant soil.
    Units: depths cm, sand/silt/clay %, dbthirdbar_r g/cm3, awc_r cm/cm,
    ksat_r um/s, om_r %.
    """
    flt = " AND c.majcompflag='Yes'" if major_only else ""
    sql = ("SELECT mu.mukey, mu.muname, c.cokey, c.compname, c.comppct_r, "
           "c.majcompflag, c.drainagecl, c.hydgrp, c.taxclname, c.slope_r, "
           "ch.hzname, ch.hzdept_r, ch.hzdepb_r, ch.sandtotal_r, ch.silttotal_r, "
           "ch.claytotal_r, ch.dbthirdbar_r, ch.awc_r, ch.ksat_r, ch.om_r, "
           "ch.ph1to1h2o_r FROM legend l "
           "INNER JOIN mapunit mu ON mu.lkey=l.lkey "
           "INNER JOIN component c ON c.mukey=mu.mukey "
           "LEFT OUTER JOIN chorizon ch ON ch.cokey=c.cokey "
           "WHERE mu.mukey IN (SELECT * FROM "
           "SDA_Get_Mukey_from_intersection_with_WktWgs84('point(%f %f)'))%s "
           "ORDER BY c.comppct_r DESC, ch.hzdept_r" % (lon, lat, flt))
    df = sda_query(sql)
    num = ["comppct_r", "slope_r", "hzdept_r", "hzdepb_r", "sandtotal_r",
           "silttotal_r", "claytotal_r", "dbthirdbar_r", "awc_r", "ksat_r",
           "om_r", "ph1to1h2o_r"]
    import pandas as pd
    for c in num:
        if c in df:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def sda_grid_components(points, surface_only=True):
    """Dominant-component soil properties over many lat-lon points in ONE SDA call.

    points: iterable of (lon, lat). Uses a WKT multipoint, which keeps a
    domain-wide survey to a single request. surface_only restricts to the
    0-cm-top horizon.
    """
    wkt = "multipoint(" + ", ".join("(%.4f %.4f)" % (lo, la) for lo, la in points) + ")"
    hz = " AND ch.hzdept_r=0" if surface_only else ""
    sql = ("SELECT mu.mukey, mu.muname, c.compname, c.comppct_r, c.drainagecl, "
           "c.hydgrp, ch.hzdept_r, ch.hzdepb_r, ch.sandtotal_r, ch.claytotal_r, "
           "ch.dbthirdbar_r, ch.awc_r, ch.ksat_r FROM mapunit mu "
           "INNER JOIN component c ON c.mukey=mu.mukey "
           "INNER JOIN chorizon ch ON ch.cokey=c.cokey "
           "WHERE mu.mukey IN (SELECT * FROM "
           "SDA_Get_Mukey_from_intersection_with_WktWgs84('%s')) "
           "AND c.majcompflag='Yes'%s" % (wkt, hz))
    return sda_query(sql)


def derechos_soil_sites():
    """Verified SSURGO identity of the two DERECHOS core sites (measured 2026-09-05)."""
    return {
        "S1": dict(name="Muscatine Island Research Farm", isusm="FRUI4",
                   lat=41.356, lon=-91.136, mukey="410028",
                   muname="Fruitfield coarse sand, 0 to 2 percent slopes",
                   component="Fruitfield", comppct=95, hydgrp="A",
                   drainage="Excessively drained", sand_pct=90.6, clay_pct=3.0,
                   awc_cm_per_cm=0.05, ksat_um_per_s=200.0,
                   taxclname="ENTIC HAPLUDOLLS, SANDY, MIXED, MESIC"),
        "M1": dict(name="South East Research Farm (SERF)", isusm="CRFI4",
                   lat=41.1933, lon=-91.4839, mukey="408753",
                   muname="Taintor silty clay loam, 0 to 2 percent slopes",
                   component="Taintor", comppct=90, hydgrp="D",
                   drainage="Poorly drained", sand_pct=2.0, clay_pct=30.0,
                   awc_cm_per_cm=0.22, ksat_um_per_s=3.0,
                   taxclname="Fine, smectitic, mesic Vertic Argiaquolls"),
    }


def warm_icn_soil_status():
    """Live re-check of the Illinois WARM / ICN access barrier for the east domain."""
    import re
    import requests
    out = {}
    for key, url in (("station_metadata",
                      "https://warm.isws.illinois.edu/warm/climnet/stnmetadata.asp"),
                     ("bulk_data_list",
                      "https://warm.isws.illinois.edu/warm/cdflist.asp")):
        try:
            r = requests.get(url, timeout=90)
            m = re.search(r"<title>(.*?)</title>", r.text, re.I | re.S)
            out[key] = dict(url=url, status=r.status_code,
                            title=(m.group(1).strip() if m else None))
        except Exception as e:
            out[key] = dict(url=url, error="%s: %s" % (type(e).__name__, str(e)[:120]))
    return out
