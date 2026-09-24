"""Helpers for the arm-instruments skill: ARM's data-source catalog, handbook
discovery, and the per-instrument example datastream.

The catalog endpoint is ARM's own Elasticsearch proxy behind arm.gov's instrument
pages. It is the only complete enumeration of ARM instrument classes - there is no
sitemap and /capabilities/instruments is a JavaScript shell.
"""
import ast
import csv
import json
import os
import pathlib
import urllib.request

ARM_ES_URL = "https://www.arm.gov/api/es/{index}/_search"
ARM_HANDBOOK_DIR = "https://www.arm.gov/publications/tech_reports/handbooks/"
ARM_INSTRUMENT_PAGE = "https://www.arm.gov/capabilities/instruments/{code}"
ARM_ES_INDEXES = ["ds", "measurements"]


def skill_dir():
    """Directory holding this sidecar. The loader execs the file, so there is no
    __file__ to read; recover it from a function's code object instead."""
    return pathlib.Path(skill_dir.__code__.co_filename).resolve().parent


def arm_es_query(index="ds", body=None, timeout=90):
    """POST a raw Elasticsearch query to ARM's public search proxy.

    index: 'ds' (741 data sources: instrument classes, VAPs, PI products, external)
           or 'measurements' (129 primary measurement types, each with the
           instruments that supply it).
    """
    payload = json.dumps(body or {"size": 1000, "query": {"match_all": {}}}).encode()
    req = urllib.request.Request(ARM_ES_URL.format(index=index), data=payload,
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def arm_parse_field(value):
    """Nested fields in the ds index come back as Python-repr strings, not JSON."""
    if value in (None, "", "None"):
        return []
    if isinstance(value, (list, dict)):
        return value
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []


def arm_fetch_catalog(timeout=120):
    """Live fetch: every ARM instrument class as a list of dicts.

    Instrument classes are the ds-index records with no 'type' field, where the
    document id equals the instrument_class_code. The typed records are VAPs, PI
    products and externally funded datasets.
    """
    hits = arm_es_query("ds", {"size": 1000, "query": {"match_all": {}}},
                        timeout=timeout)["hits"]["hits"]
    out = []
    for h in hits:
        s = h["_source"]
        if s.get("type") is not None:
            continue
        streams = arm_parse_field(s.get("datastreams"))
        hb = s.get("url_techreport")
        out.append({
            "code": s.get("instrument_class_code"),
            "name": s.get("instrument_class_name"),
            "description": s.get("instrument_class_desc"),
            "categories": [c.get("instrument_category_name")
                           for c in arm_parse_field(s.get("categories"))],
            "measurements": [m.get("primary_meas_type_name")
                             for m in arm_parse_field(s.get("measurements"))],
            "source_classes": [c.get("source_class_code")
                               for c in arm_parse_field(s.get("source_classes"))],
            "handbook": None if hb in (None, "", "None") else hb,
            "active": s.get("active"),
            "start_date": s.get("start_date"),
            "end_date": s.get("end_date"),
            "datastreams": streams,
            "n_datastreams_with_data": sum(1 for d in streams if d.get("data_available")),
        })
    return out


def arm_catalog_path():
    """Locate the shipped catalog.csv.

    The loader execs this file, and depending on how it was compiled co_filename may
    be a bare name rather than a path - so skill_dir() can land on the working
    directory. Check there first, then the conventional repo location, then the
    directory of any arm-instruments copy on sys.path.
    """
    here = skill_dir()
    candidates = [here / "catalog.csv",
                  here / "skills" / "arm-instruments" / "catalog.csv",
                  pathlib.Path.cwd() / "skills" / "arm-instruments" / "catalog.csv"]
    for parent in list(here.parents)[:4]:
        candidates.append(parent / "arm-instruments" / "catalog.csv")
        candidates.append(parent / "skills" / "arm-instruments" / "catalog.csv")
    for c in candidates:
        if c.exists():
            return c
    return None


def arm_catalog(live=False):
    """The shipped catalog (fast, offline) or a live fetch.

    The shipped copy is catalog.csv beside this file: one row per instrument class,
    with the handbook URL and the example datastream each instrument skill was
    verified against. Pass live=True to re-read ARM's index instead. Falls back to
    the live fetch when the CSV cannot be located.
    """
    if live:
        return arm_fetch_catalog()
    path = arm_catalog_path()
    if path is None:
        return arm_fetch_catalog()
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def arm_instrument(code, live=False):
    """One catalog record by instrument class code, or None."""
    for row in arm_catalog(live=live):
        if str(row.get("code", "")).lower() == code.lower():
            return row
    return None


def arm_find_instruments(text, live=False):
    """Instruments whose code, name, measurements or category mention `text`."""
    t = text.lower()
    out = []
    for row in arm_catalog(live=live):
        blob = " ".join(str(row.get(k, "")) for k in
                        ("code", "name", "measurements", "categories", "description")).lower()
        if t in blob:
            out.append(row)
    return out


def arm_handbook_candidates(code):
    """The two URL patterns ARM files instrument handbooks under."""
    row = arm_instrument(code)
    urls = [ARM_HANDBOOK_DIR + code + "_handbook.pdf"]
    if row and row.get("pdf"):
        urls.append(row["pdf"])
    if row and row.get("handbook"):
        urls.append(row["handbook"])
    seen = []
    for u in urls:
        u = u.replace("http://", "https://").replace("https://arm.gov", "https://www.arm.gov")
        if u not in seen:
            seen.append(u)
    return seen


def arm_handbook_url(code, check=True, timeout=30):
    """First handbook URL for this instrument that actually resolves to a PDF."""
    for u in arm_handbook_candidates(code):
        if not check:
            return u
        try:
            req = urllib.request.Request(u, method="HEAD")
            with urllib.request.urlopen(req, timeout=timeout) as r:
                if r.status == 200 and "pdf" in r.headers.get("Content-Type", ""):
                    return u
        except Exception:
            continue
    return None


def arm_handbook_download(code, outdir="handbooks", timeout=120):
    """Download the handbook PDF; returns the local path or None."""
    url = arm_handbook_url(code, timeout=timeout)
    if not url:
        return None
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, code + "_handbook.pdf")
    if not os.path.exists(path):
        urllib.request.urlretrieve(url, path)
    return path


def arm_handbook_pages(code, outdir="handbooks"):
    """Handbook text as a list of page strings (needs pypdfium2)."""
    import pypdfium2
    path = arm_handbook_download(code, outdir=outdir)
    if not path:
        return []
    pdf = pypdfium2.PdfDocument(path)
    return [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]


def arm_instrument_example(code):
    """The datastream this instrument's skill was verified against, plus its window."""
    row = arm_instrument(code)
    if not row:
        return None
    return {"datastream": row.get("ex_datastream"), "site": row.get("ex_site"),
            "facility": row.get("ex_facility"), "level": row.get("ex_level"),
            "start": row.get("ex_start"), "end": row.get("ex_end")}


def arm_instruments_for_measurement(measurement, timeout=90):
    """Which instrument classes supply a primary measurement type, from the live
    measurements index. `measurement` is matched case-insensitively against the
    measurement name, e.g. 'Cloud base height'."""
    hits = arm_es_query("measurements", {"size": 200, "query": {"match_all": {}}},
                        timeout=timeout)["hits"]["hits"]
    out = {}
    for h in hits:
        s = h["_source"]
        if measurement.lower() not in str(s.get("primary_meas_type_name", "")).lower():
            continue
        for ds in s.get("data_sources") or []:
            out.setdefault(ds.get("instrument_class_code"), ds.get("instrument_class_name"))
    return out


def arm_skill_for(code):
    """Name of the per-instrument skill for this code, if this repo ships one."""
    d = skill_dir() / ("arm-instrument-" + code.lower())
    return d.name if (d / "SKILL.md").exists() else None
