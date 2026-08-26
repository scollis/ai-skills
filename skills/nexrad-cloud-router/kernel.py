"""Router for NEXRAD-in-the-cloud work: characterise a task, cost each access
path, and emit an execution plan naming which sibling skill to load per step.

The cost constants are MEASURED (see SKILL.md "Calibration"), not guessed.
`measure_throughput()` re-calibrates the one that varies most by environment
(raw download bandwidth), which is what sets the raw-vs-ARCO crossover.
"""

import datetime as dt

# --------------------------------------------------------------------------
# Measured cost constants (KLOT, 2026-08-25, sandbox link ~1.2 MB/s).
# --------------------------------------------------------------------------
COST = {
    # Volume size is BIMODAL and is the constant the crossover is most
    # sensitive to. Measured on KLOT: quiet 3h window mean 7.67 MB
    # (5.21-8.46), convective 3h window mean 13.29 MB (7.96-16.95). The
    # default is the quiet/mixed figure; pass volume_MB= or call
    # measure_throughput() for a convective case.
    "raw_volume_MB": 8.4,           # KLOT mixed/quiet mean (see VOLUME_MB_BY_REGIME)
    "raw_MB_per_s": 1.2,            # sandbox link; re-measure elsewhere
    "raw_decode_full_s": 1.0,       # pyart full read, 17 sweeps x 7 fields
    "raw_decode_lazy_s": 0.8,       # delay_field_loading=True
    "arco_open_s": 4.9,             # icechunk repo open (once per session)
    "arco_time_axis_s": 1.4,        # whole vcp_time for one VCP (one chunk)
    "arco_chunk_s": 0.47,           # bare (sweep x field) chunk read, mean of 8
    "arco_chunk_in_loop_s": 0.60,   # same read inside a reassembly loop
    "arco_probe_s": 0.066,          # one (sweep, index) recorded-or-not probe
    "arco_chunk_wire_MB": 1.2,      # zstd, ~4.3x smaller than decoded
    "arco_chunk_decoded_MB": 5.3,   # 720 x 1832 float32
    "lowsweeps_open_s": 5.6,        # open + whole 1.0M-scan time axis
    "lowsweeps_scan_s": 0.36,       # one base-tilt scan, one field
}

# Mean Level II volume size by regime (KLOT, measured). Convective volumes are
# ~1.7x larger because more gates carry echo and compress less.
VOLUME_MB_BY_REGIME = {"quiet": 7.7, "mixed": 8.4, "convective": 13.3}

SKILL_ACCESS = "nexrad-aws-2025"
SKILL_ARCO = "nexrad-arco"
SKILL_GCS = "nexrad-radar-gcs"
SKILL_RAINFALL = "nexrad-site-rainfall"
SKILL_AREA = "nexrad-area-over-threshold"

ARCHETYPES = ("case_study", "base_tilt_series", "volume_series", "site_rainfall",
              "areal_stats", "realtime")


def volume_MB(regime=None):
    """Mean Level II volume size for a regime ('quiet'/'mixed'/'convective')."""
    if regime is None:
        return COST["raw_volume_MB"]
    return VOLUME_MB_BY_REGIME.get(str(regime).lower(), COST["raw_volume_MB"])


def raw_volume_cost(n_volumes, lazy=False, regime=None):
    """Wall-time and wire bytes for n raw Level II volumes (download + decode).

    `regime` selects the measured mean volume size ('quiet' 7.7 MB / 'mixed'
    8.4 / 'convective' 13.3); volume size drives the crossover, so set it when
    you know the weather.
    """
    mb = n_volumes * volume_MB(regime)
    dl = mb / COST["raw_MB_per_s"]
    dec = n_volumes * (COST["raw_decode_lazy_s"] if lazy else COST["raw_decode_full_s"])
    return {"path": "raw Level II", "n_volumes": n_volumes,
            "wire_MB": round(mb, 1), "wall_s": round(dl + dec, 1),
            "download_s": round(dl, 1), "decode_s": round(dec, 1),
            "regime": regime or "default",
            "gets": "every sweep, every field, true per-ray geometry"}


def arco_cost(n_scans, n_sweeps=1, n_fields=1, fragmented=False, opened=False):
    """Wall-time and wire bytes for an ARCO read of n_scans x n_sweeps x n_fields.

    `fragmented=True` accounts for the SAILS layout trap: one physical volume
    spans ~3 consecutive scan indices, so a whole-volume read costs 3x the
    index count (see nexrad-aws-2025 section 5b).
    """
    mult = 3 if fragmented else 1
    chunks = n_scans * mult * n_sweeps * n_fields
    setup = 0.0 if opened else COST["arco_open_s"] + COST["arco_time_axis_s"]
    # Reassembling a fragmented volume also probes every (sweep, index) pair to
    # find which sweeps were actually recorded -- a real cost the naive
    # chunks-only model missed (51 probes = 3.4 s on a 3-index KLOT volume).
    per = COST["arco_chunk_in_loop_s"] if fragmented else COST["arco_chunk_s"]
    probes = n_scans * mult * n_sweeps if fragmented else 0
    wall = setup + chunks * per + probes * COST["arco_probe_s"]
    return {"path": "ARCO per-VCP", "n_chunks": chunks, "n_probes": probes,
            "wire_MB": round(chunks * COST["arco_chunk_wire_MB"], 1),
            "wall_s": round(wall, 1), "setup_s": round(setup, 1),
            "gets": "exactly the sweeps/fields asked for; azimuth pre-regridded"}


def lowsweeps_cost(n_scans, n_fields=1, opened=False):
    """Wall-time and wire bytes for n base-tilt scans from the lowsweeps cube."""
    setup = 0.0 if opened else COST["lowsweeps_open_s"]
    chunks = n_scans * n_fields
    return {"path": "ARCO lowsweeps", "n_chunks": chunks,
            "wire_MB": round(chunks * COST["arco_chunk_wire_MB"], 1),
            "wall_s": round(setup + chunks * COST["lowsweeps_scan_s"], 1),
            "setup_s": round(setup, 1),
            "gets": "base tilt (0.48 deg) only, 2015->now, all VCPs in one axis"}


def crossover_chunks(regime=None):
    """(sweep x field) chunk count at which one raw volume becomes cheaper.

    Below this, ARCO wins because you pay only for what you read; above it the
    raw volume is one sequential transfer that carries everything. Scales with
    volume size and inversely with bandwidth: on a 1.2 MB/s link it is 15
    (quiet), 17 (mixed) and 25 (convective) chunks. Call it rather than quoting
    it -- the numbers move with COST["raw_MB_per_s"].
    """
    raw = volume_MB(regime) / COST["raw_MB_per_s"] + COST["raw_decode_lazy_s"]
    return int(round(raw / COST["arco_chunk_s"]))


def classify_task(text):
    """Guess the task archetype and routing-relevant features from a request.

    Keyword heuristic over the user's own words -- a starting point, not a
    substitute for reading the request. Returns dict(archetype, signals,
    needs_true_geometry, needs_upper_tilts, likely_long_series).
    """
    t = (text or "").lower()

    def hits(*words):
        return [w for w in words if w in t]

    sig = {
        "series": hits("time series", "timeseries", "climatolog", "month", "year",
                       "season", "long-term", "trend", "every scan", "week", "day",
                       "hourly", "daily", "over time", "evolution", "series"),
        "single": hits("case study", "this storm", "one volume", "snapshot",
                       "tornado", "outbreak", "single volume"),
        "geometry": hits("grid", "gridding", "nufft", "spectral", "azimuth", "jitter",
                         "per-ray", "interpolat", "cappi", "rhi", "cross-section",
                         "dealias"),
        "upper": hits("echo top", "echo-top", "storm top", "vil", "profile", "qvp",
                      "vertical", "hail", "melting layer", "column", "3d"),
        "rain": hits("rainfall", "rain rate", "accumulation", "precip", "marshall",
                     "z-r", "qpe"),
        "area": hits("area", "coverage", "extent", "km2", "km^2", "organiz"),
        "live": hits("real-time", "realtime", "live", "latest", "current", "nowcast",
                     "right now", "showing now", "at the moment", "most recent",
                     "up to the minute"),
        "dualpol": hits("zdr", "dual-pol", "dualpol", "rhohv", "polarimetric",
                        "differential"),
    }
    if sig["live"]:
        arch = "realtime"
    elif sig["rain"] and not sig["area"]:
        arch = "site_rainfall"
    elif sig["area"]:
        arch = "areal_stats"
    elif sig["series"] and not sig["upper"]:
        arch = "base_tilt_series"
    elif sig["series"]:
        arch = "volume_series"
    else:
        arch = "case_study"
    return {"archetype": arch,
            "signals": {k: v for k, v in sig.items() if v},
            "needs_true_geometry": bool(sig["geometry"]),
            "needs_upper_tilts": bool(sig["upper"] or sig["area"]),
            "likely_long_series": bool(sig["series"])}


def choose_source(archetype="case_study", n_volumes=1, needs_true_geometry=False,
                  needs_upper_tilts=False, site="KLOT", n_fields=1,
                  arco_sites=("KLOT",), n_sweeps=None, regime=None):
    """Pick the access path, with the reason, the cost, and the runner-up.

    Hard constraints apply BEFORE cost: ARCO cannot serve true per-ray geometry
    (its azimuth axis is pre-regridded onto an exact grid), and it only covers
    the sites actually published in the bucket.

    `n_sweeps` is how many sweeps per volume you actually need -- the single
    biggest lever on the decision, since ARCO bills per (sweep x field) chunk.
    Pass 1 for a base-tilt PPI; leave None to infer 17 (whole volume) when
    upper tilts are needed and 6 (the low cuts) otherwise. `regime`
    ('quiet'/'mixed'/'convective') sets the raw volume size.
    """
    site = (site or "").upper()
    in_arco = site in {s.upper() for s in arco_sites}

    if archetype == "realtime":
        return {"source": "chunks bucket", "skill": SKILL_ACCESS,
                "reason": "sub-minute latency; archive lags ~7 min and ARCO ~8 min",
                "alternatives": ["archive bucket if a few minutes is acceptable"],
                "notes": ["reassemble S/I/E chunk messages into a volume"]}

    if needs_true_geometry:
        return {"source": "raw Level II", "skill": SKILL_ACCESS,
                "reason": ("ARCO azimuth is pre-regridded to an exact 0.5/1.0 deg grid, "
                           "so it cannot exercise anything sensitive to ray jitter"),
                "alternatives": [],
                "notes": ["raw KLOT jitter reaches 0.19 of nominal ray spacing"]}

    if not in_arco:
        return {"source": "raw Level II", "skill": SKILL_ACCESS,
                "reason": f"{site} is not published in the ARCO bucket",
                "alternatives": [f"GCS mirror ({SKILL_GCS}) if AWS is blocked"],
                "notes": ["verify ARCO coverage before assuming a site exists"]}

    if archetype == "base_tilt_series" and not needs_upper_tilts:
        c_low = lowsweeps_cost(n_volumes, n_fields)
        c_raw = raw_volume_cost(n_volumes, lazy=True, regime=regime)
        ratio = c_raw["wall_s"] / max(c_low["wall_s"], 0.1)
        return {"source": "ARCO lowsweeps", "skill": SKILL_ARCO,
                "reason": (f"base tilt only over {n_volumes} scans: {c_low['wall_s']}s "
                           f"vs {c_raw['wall_s']}s raw ({ratio:.0f}x)"),
                "alternatives": ["raw Level II if you later need upper tilts"],
                "notes": ["one flat cube spanning 2015->now across every VCP"],
                "cost": c_low, "runner_up": c_raw}

    if n_sweeps is None:
        n_sweeps = 17 if needs_upper_tilts else 6
    # A single-sweep read needs no volume reassembly, so it skips the
    # fragmentation multiplier and the per-(sweep, index) probes.
    frag = n_sweeps > 1
    c_arco = arco_cost(n_volumes, n_sweeps=n_sweeps, n_fields=n_fields, fragmented=frag)
    c_raw = raw_volume_cost(n_volumes, lazy=True, regime=regime)
    notes = []
    if c_arco["wall_s"] <= c_raw["wall_s"]:
        src, skill, other = "ARCO per-VCP", SKILL_ARCO, c_raw
        why = (f"{n_sweeps} sweep(s) x {n_fields} field(s) = {c_arco['n_chunks']} chunks "
               f"({c_arco['wall_s']}s) beats {n_volumes} raw volumes ({c_raw['wall_s']}s)")
        if frag:
            notes.append("mind SAILS fragmentation: one volume spans ~3 scan indices")
        cost = c_arco
    else:
        src, skill, other = "raw Level II", SKILL_ACCESS, c_arco
        why = (f"{c_arco['n_chunks']} chunks would cost {c_arco['wall_s']}s; one "
               f"sequential volume transfer is {c_raw['wall_s']}s and carries every "
               f"sweep and field (crossover ~{crossover_chunks(regime)} chunks at "
               f"{volume_MB(regime)} MB volumes)")
        cost = c_raw
    return {"source": src, "skill": skill, "reason": why,
            "alternatives": [other["path"]], "notes": notes,
            "cost": cost, "runner_up": other}


def plan_analysis(task, site="KLOT", n_volumes=1, when=None, n_fields=1,
                  arco_sites=("KLOT",), n_sweeps=None, regime=None):
    """Full route: classify -> choose source -> ordered steps naming sibling skills.

    Returns dict(archetype, source, reason, cost, steps, skills_to_load,
    guardrails). Render it with format_plan().
    """
    feat = classify_task(task)
    arch = feat["archetype"]
    pick = choose_source(archetype=arch, n_volumes=n_volumes,
                         needs_true_geometry=feat["needs_true_geometry"],
                         needs_upper_tilts=feat["needs_upper_tilts"],
                         site=site, n_fields=n_fields, arco_sites=arco_sites,
                         n_sweeps=n_sweeps, regime=regime)

    # Locating data is always a nexrad-aws-2025 job -- it owns the bucket keys
    # and the ARCO open/time-axis primitives. pick["skill"] is where the
    # downstream WORKFLOW lives, which is a different thing.
    steps = [{"step": "locate data",
              "action": (f"list volumes for {site}"
                         + (f" around {when}" if when else "")
                         + f" via the {pick['source']} path"),
              "skill": SKILL_ACCESS}]

    if pick["source"] == "raw Level II":
        steps.append({"step": "filter",
                      "action": "drop *_V06_MDM sidecars by size floor "
                                "(0.65-0.7 MB vs 4-9 MB volumes)",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "read",
                      "action": "read_nexrad_volume(); delay_field_loading=True if you "
                                "only need one moment",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "resolve scan config",
                      "action": "classify_scan(fixed_angle, vcp) -> SAILS/MRLE/AVSET; "
                                "dedup_split_cuts() before any per-sweep indexing",
                      "skill": SKILL_ACCESS})
    elif pick["source"] == "ARCO lowsweeps":
        steps.append({"step": "open",
                      "action": "arco_open(site, lowsweeps=True); arco_times() reads the "
                                "whole time axis in one request",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "select",
                      "action": "np.searchsorted on that axis; never scan the per-ray "
                                "time array by column",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "mask",
                      "action": "arco_mask() -- the -999 sentinel is NOT auto-decoded "
                                "(~75% of gates in a low sweep)",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "workflow",
                      "action": "Py-ART conversion, QVPs, METAR overlays and animations "
                                "for ARCO data",
                      "skill": SKILL_ARCO})
    elif pick["source"] == "ARCO per-VCP":
        steps.append({"step": "open",
                      "action": "arco_open(site); arco_vcps() to see which VCP covers "
                                "your period",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "reassemble volume",
                      "action": "arco_volume_indices() -- under SAILS one volume spans "
                                "~3 consecutive indices; reading one loses upper tilts",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "load sweeps",
                      "action": "arco_sweep() (masks -999 and georeferences)",
                      "skill": SKILL_ACCESS})
        steps.append({"step": "workflow",
                      "action": "Py-ART conversion, QVPs, METAR overlays and animations "
                                "for ARCO data",
                      "skill": SKILL_ARCO})
    else:
        steps.append({"step": "assemble",
                      "action": "group chunk messages by volume, order S -> I -> E",
                      "skill": SKILL_ACCESS})

    if arch == "site_rainfall":
        steps.append({"step": "rain rate",
                      "action": "Marshall-Palmer Z-R with a hail cap; state the "
                                "beam-height caveat at range",
                      "skill": SKILL_RAINFALL})
    if arch == "areal_stats":
        steps.append({"step": "areal stats",
                      "action": "area_over_thresholds() on the lowest usable sweep",
                      "skill": SKILL_AREA})
    if arch in ("case_study", "volume_series"):
        steps.append({"step": "plot",
                      "action": "PPI / dual-pol maps with ChaseSpectral (cmweather) on "
                                "georeferenced GeoAxes",
                      "skill": SKILL_GCS})

    guards = [
        "Never fall back to noaa-nexrad-level2 -- deprecated, denies access.",
        "Sweep count is not fixed for a VCP: detect SAILS/MESO-SAILS/MRLE/AVSET "
        "per volume.",
        "Split cuts repeat the 3 lowest tilts; never select a sweep by "
        "field-iteration order.",
    ]
    if pick["source"].startswith("ARCO"):
        guards.append("ARCO -999 fill is base64-encoded in the attrs, so nothing "
                      "masks it for you.")
        guards.append("Fix the CA bundle before the first icechunk import "
                      "(once per process).")

    ordered, seen = [], set()
    for s in [SKILL_ACCESS] + [x["skill"] for x in steps]:
        if s not in seen:
            seen.add(s)
            ordered.append(s)
    return {"archetype": arch, "features": feat, "source": pick["source"],
            "reason": pick["reason"], "alternatives": pick.get("alternatives", []),
            "cost": pick.get("cost"), "runner_up": pick.get("runner_up"),
            "steps": steps, "skills_to_load": ordered,
            "guardrails": guards + pick.get("notes", [])}


def format_plan(plan):
    """Render plan_analysis() output as readable text."""
    lines = [f"archetype : {plan['archetype']}",
             f"source    : {plan['source']}",
             f"reason    : {plan['reason']}"]
    if plan.get("cost"):
        c = plan["cost"]
        lines.append(f"est. cost : {c['wall_s']}s, {c['wire_MB']} MB wire "
                     f"({c['gets']})")
    if plan.get("runner_up"):
        r = plan["runner_up"]
        lines.append(f"runner-up : {r['path']} at {r['wall_s']}s, {r['wire_MB']} MB")
    lines.append(f"load      : {', '.join(plan['skills_to_load'])}")
    lines.append("steps:")
    for i, s in enumerate(plan["steps"], 1):
        lines.append(f"  {i}. [{s['step']}] {s['action']}   <- {s['skill']}")
    lines.append("guardrails:")
    for g in plan["guardrails"]:
        lines.append(f"  - {g}")
    return "\n".join(lines)


def arco_coverage(client=None):
    """Live list of sites published in the ARCO bucket, and which have lowsweeps.

    Coverage is still limited, so a router decision that assumes a site is in
    ARCO must check. Pass the result as `arco_sites=` to choose_source().
    """
    s3 = client
    if s3 is None:
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config
        s3 = boto3.client("s3", region_name="us-east-1",
                          config=Config(signature_version=UNSIGNED))
    r = s3.list_objects_v2(Bucket="nexrad-arco", Delimiter="/")
    prefixes = [p["Prefix"].rstrip("/") for p in r.get("CommonPrefixes", [])]
    sites = sorted({p.replace("-lowsweeps", "") for p in prefixes})
    return {"sites": sites,
            "lowsweeps": sorted(p.replace("-lowsweeps", "") for p in prefixes
                                if p.endswith("-lowsweeps")),
            "prefixes": sorted(prefixes)}


def measure_throughput(site="KLOT", when=None, client=None, workdir="bench_router",
                       n=2):
    """Re-measure raw download BANDWIDTH and update COST['raw_MB_per_s'] in place.

    Bandwidth varies most between environments and it sets the raw-vs-ARCO
    crossover, so call this when a routing decision is close. Deliberately does
    NOT touch the volume-size constants: one volume's size says more about the
    weather at that moment than about the archive, so regime stays explicit via
    VOLUME_MB_BY_REGIME. Requires the nexrad-aws-2025 helpers (s3_anon /
    nexrad_keys / download_volume) in the same kernel.
    """
    import os
    import time

    g = globals()
    need = ("s3_anon", "nexrad_keys", "download_volume")
    missing = [x for x in need if x not in g]
    if missing:
        raise RuntimeError("load the nexrad-aws-2025 skill first; missing: "
                           + ", ".join(missing))
    c = client or g["s3_anon"]()
    end = when or dt.datetime.now(dt.timezone.utc)
    keys = g["nexrad_keys"](site, end - dt.timedelta(hours=3), end, client=c)
    if not keys:
        raise RuntimeError(f"no volumes found for {site} before {end}")
    os.makedirs(workdir, exist_ok=True)
    mb_total, t0 = 0.0, time.time()
    used = keys[-int(max(1, n)):]
    for k in used:
        path = g["download_volume"](k["key"], workdir, client=c, overwrite=True)
        mb_total += os.path.getsize(path) / 1e6
    elapsed = time.time() - t0
    COST["raw_MB_per_s"] = round(mb_total / elapsed, 2)
    return {"n_volumes": len(used), "MB": round(mb_total, 2),
            "wall_s": round(elapsed, 2), "MB_per_s": COST["raw_MB_per_s"],
            "observed_mean_volume_MB": round(mb_total / len(used), 2),
            "crossover_now": crossover_chunks(),
            "note": "volume-size constants untouched; pass regime= to cost calls"}
