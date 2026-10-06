"""Helpers for the DERECHOS campaign knowledge skill."""
import os
import sys
import json

DERECHOS_CACHE = {}


def derechos_data():
    """Load and cache the DERECHOS structured white-paper record (dict)."""
    if "data" in DERECHOS_CACHE:
        return DERECHOS_CACHE["data"]
    here = os.path.dirname(sys._getframe().f_code.co_filename)
    if not here:
        raise RuntimeError("skill dir unavailable in this runtime")
    with open(os.path.join(here, "derechos_stm.json")) as f:
        DERECHOS_CACHE["data"] = json.load(f)
    return DERECHOS_CACHE["data"]


def derechos_instruments(sq=None, site=None, min_priority=None, table=1):
    """Query the DERECHOS science traceability matrix.

    sq            int or "SQ3" -> only instruments supporting that science question
    site          "M1" | "S1" | "R1" (table 1 only)
    min_priority  1..3 (3 = critical/core)
    table         1 = requested AMF matrix, 2 = additional M1 instruments,
                  3 = ANL guest instruments at NIU, 4 = ATMOS capabilities
    Returns a pandas DataFrame.
    """
    import pandas as pd
    d = derechos_data()
    rows = d["table%d" % int(table)]
    if int(table) == 4:
        return pd.DataFrame(rows)
    if int(table) == 3:
        return pd.DataFrame(rows)
    out = []
    for r in rows:
        if sq is not None:
            n = int(str(sq).upper().replace("SQ", ""))
            if n not in r["sqs"]:
                continue
        if site is not None and site.upper() not in r.get("sites", []):
            continue
        if min_priority is not None and r["priority"] < int(min_priority):
            continue
        out.append(r)
    df = pd.DataFrame(out)
    if "sqs" in df:
        df["sqs"] = df["sqs"].apply(lambda v: " ".join("SQ%d" % i for i in v))
    if "sites" in df:
        df["sites"] = df["sites"].apply(" ".join)
    return df


def derechos_sq(n=None):
    """Full text of science question(s). n=None returns all seven as a dict."""
    d = derechos_data()["science_questions"]
    if n is None:
        return d
    return d["SQ%d" % int(str(n).upper().replace("SQ", ""))]


def derechos_hypotheses(n=None):
    """Full text of hypothesis H1-H4. n=None returns all four as a dict."""
    d = derechos_data()["hypotheses"]
    if n is None:
        return d
    return d["H%d" % int(str(n).upper().replace("H", ""))]


def derechos_sites(key=None):
    """Site descriptions: M1, S1, R1, NIU, CHICAGO, MOBILE."""
    d = derechos_data()["site_key"]
    if key is None:
        return d
    return d[key.upper()]


def derechos_traceability(sq=None):
    """Print a compact SQ -> instrument traceability listing for tables 1 and 2."""
    d = derechos_data()
    sqs = ["SQ%d" % i for i in range(1, 8)] if sq is None else ["SQ%d" % int(str(sq).upper().replace("SQ", ""))]
    for s in sqs:
        n = int(s[2:])
        t1 = [r["instrument"] for r in d["table1"] if n in r["sqs"]]
        t2 = [r["instrument"] for r in d["table2"] if n in r["sqs"]]
        meta = d["science_questions"][s]
        print("%s (%s | %s)" % (s, "/".join(meta["hypotheses"]), "/".join(meta["topics"])))
        print("   requested : " + ", ".join(t1))
        print("   additional: " + ", ".join(t2))
