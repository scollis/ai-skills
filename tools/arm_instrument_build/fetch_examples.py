"""Pull one real ARM Live file per instrument and measure what is in it.

Nothing here reads the handbook: the point is an independent check on what the
archive currently serves, so a skill can say where each number came from.
"""
import datetime as dt
import json
import os
import pathlib
import warnings

import numpy as np
import requests

QUERY = "https://adc.arm.gov/armlive/livedata/query"
SAVE = "https://adc.arm.gov/armlive/livedata/saveData"
MAX_FILE_MB = 150.0
LEVEL_RANK = {"c1": 0, "b1": 1, "c2": 2, "b2": 3, "a1": 4, "s1": 5, "a0": 9, "00": 9}
FAC_RANK = {"C1": 0, "M1": 1, "S40": 2, "E13": 3, "S1": 4}
SITE_RANK = {"sgp": 0, "bnf": 0, "ena": 2, "nsa": 1, "osc": 3}
RADAR_HINTS = ("radar", "sacr", "sapr", "kazr", "mmcr", "rwp", "acr")


def pick_datastream(record):
    """Best example datastream: processed level, permanent facility, recent, active."""
    ds = [d for d in record.get("datastreams", []) if d.get("data_available")]
    ds = [d for d in ds if (d.get("data_level_code") or "") not in ("00", "", "a0")] or ds
    if not ds:
        return None
    ds.sort(key=lambda e: (not e.get("active"),
                           LEVEL_RANK.get(e.get("data_level_code"), 7),
                           FAC_RANK.get(e.get("facility_code"), 6),
                           SITE_RANK.get(e.get("site_code"), 8),
                           -int(str(e.get("end_date") or "0")[:4] or 0)))
    return ds[0]


def list_files(user, token, datastream, start, end, timeout=90):
    r = requests.get(QUERY, params={"user": f"{user}:{token}", "ds": datastream,
                                    "start": start, "end": end, "wt": "json"}, timeout=timeout)
    r.raise_for_status()
    return r.json()


def find_example_file(user, token, datastream, end_date, windows=(6, 45, 400)):
    """Widen the window until the archive returns something. Retired instruments need
    the wide pass; active ones hit on the first."""
    end = dt.date.fromisoformat(str(end_date)[:10])
    for back in windows:
        out = list_files(user, token, datastream, (end - dt.timedelta(days=back)).isoformat(),
                         end.isoformat())
        files = out.get("files") or []
        if files:
            n, tot = out.get("num_found", len(files)), out.get("total_size", 0) or 0
            per_mb = (tot / n) / 1e6 if n else 0.0
            return {"files": sorted(files), "num_found": n, "per_file_mb": round(per_mb, 2),
                    "window_days": back}
    return None


def download(user, token, filename, datastream, root="arm_build/data", timeout=600):
    d = pathlib.Path(root) / datastream
    d.mkdir(parents=True, exist_ok=True)
    p = d / filename
    if p.exists() and p.stat().st_size > 0:
        return p
    r = requests.get(SAVE, params={"user": f"{user}:{token}", "file": filename},
                     timeout=timeout, stream=True)
    r.raise_for_status()
    with open(p, "wb") as fh:
        for chunk in r.iter_content(1 << 20):
            fh.write(chunk)
    return p


def fetch_one(user, token, code, record, root="arm_build/data"):
    """Resolve, size-check and download one example file. Network only - no reading."""
    pick = pick_datastream(record)
    if not pick:
        return {"code": code, "error": "no datastream with data"}
    ds = pick["datastream"]
    try:
        found = find_example_file(user, token, ds, pick.get("end_date"))
    except Exception as e:
        return {"code": code, "datastream": ds, "error": f"query failed: {type(e).__name__}: {e}"[:150]}
    if not found:
        return {"code": code, "datastream": ds, "error": "ARM Live returned no files in 400 days"}
    if found["per_file_mb"] > MAX_FILE_MB:
        return {"code": code, "datastream": ds,
                "error": f"files average {found['per_file_mb']} MB, over the {MAX_FILE_MB} MB cap"}
    # middle of the list: avoids a truncated first-day or last-day file
    fname = found["files"][len(found["files"]) // 2]
    try:
        p = download(user, token, fname, ds, root=root)
    except Exception as e:
        return {"code": code, "datastream": ds, "filename": fname,
                "error": f"download failed: {type(e).__name__}: {e}"[:150]}
    return {"code": code, "datastream": ds, "filename": fname, "path": str(p),
            "size_mb": round(p.stat().st_size / 1e6, 2), "site": pick.get("site_code"),
            "facility": pick.get("facility_code"), "level": pick.get("data_level_code"),
            "start": str(pick.get("start_date"))[:10], "end": str(pick.get("end_date"))[:10],
            "active": bool(pick.get("active")), "n_files_in_window": found["num_found"],
            "window_days": found["window_days"]}


def inventory(path):
    """Open with ACT and record what is actually in the file."""
    import act
    warnings.filterwarnings("ignore")
    ds = act.io.arm.read_arm_netcdf(str(path), cleanup_qc=True)
    try:
        va = {}
        for v, da in ds.variables.items():
            a = da.attrs
            va[v] = {"dims": list(da.dims), "shape": [int(s) for s in da.shape],
                     "dtype": str(da.dtype), "units": a.get("units"),
                     "long_name": a.get("long_name"), "has_qc": f"qc_{v}" in ds.variables}
        tres = None
        if "time" in ds and ds.time.size > 2:
            tres = float(np.median(np.diff(ds.time.values).astype("timedelta64[s]").astype(float)))
        keep = ("command_line", "process_version", "ingest_software", "dod_version",
                "input_source", "site_id", "facility_id", "data_level", "location_description",
                "datastream", "sampling_interval", "averaging_interval", "serial_number", "doi")
        return {"n_vars": len(ds.data_vars), "dims": {k: int(v) for k, v in ds.sizes.items()},
                "n_qc_vars": sum(1 for v in ds.variables if v.startswith("qc_")),
                "time_resolution_s": tres,
                "time_span": [str(ds.time.values[0])[:19], str(ds.time.values[-1])[:19]]
                              if "time" in ds else None,
                "global_attrs": {k: str(v)[:200] for k, v in ds.attrs.items() if k in keep},
                "variables": va}
    finally:
        ds.close()


def qc_profile(path, qc_table_fn):
    """Which embedded tests actually fire on this file, and how hard."""
    import act
    ds = act.io.arm.read_arm_netcdf(str(path), cleanup_qc=True)
    try:
        qcv = sorted(v for v in ds.variables if v.startswith("qc_"))
        covered = sorted(v for v in ds.data_vars if f"qc_{v}" in ds.variables)
        assess = sorted({str(a) for v in qcv for a in ds[v].attrs.get("flag_assessments", [])})
        rows = []
        if qcv:
            try:
                tb = qc_table_fn(ds)
                if tb is not None and len(tb):
                    rows = (tb[tb.n_flagged > 0].sort_values("percent", ascending=False)
                            .head(6).to_dict("records"))
            except Exception as e:
                rows = [{"error": f"{type(e).__name__}: {e}"[:120]}]
        return {"n_qc_vars": len(qcv), "qc_covered": covered, "assessments": assess,
                "flagged_top": rows}
    finally:
        ds.close()


def pyart_probe(path):
    """Can Py-ART read it as a Radar object, and what is in it if so."""
    try:
        import pyart
    except ImportError:
        return None
    for mod, fn in ((getattr(__import__("pyart.aux_io", fromlist=["x"]), "read_kazr", None), "read_kazr"),
                    (getattr(__import__("pyart.io", fromlist=["x"]), "read", None), "read")):
        if mod is None:
            continue
        try:
            radar = mod(str(path))
            out = {"reader": fn, "ok": True, "fields": sorted(radar.fields),
                   "nsweeps": int(radar.nsweeps), "ngates": int(radar.ngates),
                   "nrays": int(radar.nrays), "scan_type": radar.scan_type,
                   "fixed_angle": float(radar.fixed_angle["data"][0])}
            del radar
            return out
        except Exception:
            continue
    return {"ok": False}


def looks_like_radar(code, name):
    blob = f"{code} {name}".lower()
    return any(h in blob for h in RADAR_HINTS)
