"""Measure NEXRAD access-path costs on THIS machine and link.

Run as a FRESH PROCESS -- that is not optional. The icechunk Rust client
caches its TLS trust store on first import, so the CA environment variables
must be set before `import icechunk` anywhere in the process. A kernel that
has already imported icechunk cannot be fixed in place.

    python measure.py --site KLOT --out calibration.json [--quick] [--window ISO,ISO]

Emits a JSON calibration document with the same keys as the
nexrad-cloud-router COST dict, plus provenance (site, timestamps, sample
sizes, and the raw observations behind each constant).
"""
import argparse
import datetime as dt
import json
import os
import statistics
import sys
import time


def ensure_ca():
    """Point every TLS-consuming client at certifi's bundle. Call FIRST."""
    import certifi
    ca = certifi.where()
    for var in ("SSL_CERT_FILE", "AWS_CA_BUNDLE", "REQUESTS_CA_BUNDLE",
                "CURL_CA_BUNDLE"):
        os.environ[var] = ca
    return ca


def find_access_helpers():
    """Locate and load the nexrad-aws-2025 kernel (bucket access primitives).

    Searched in order: NEXRAD_AWS_2025_KERNEL, beside this script's parent, the
    working directory, then the installed skills tree.
    """
    import importlib.util
    here = os.path.dirname(os.path.abspath(__file__))
    home = os.path.expanduser("~")
    candidates = [
        os.environ.get("NEXRAD_AWS_2025_KERNEL", ""),
        os.path.join(here, "..", "nexrad-aws-2025", "kernel.py"),
        os.path.join(os.getcwd(), "nexrad-aws-2025", "kernel.py"),
    ]
    # When installed, sibling skills live beside this one in the skills tree.
    candidates.append(os.path.join(os.path.dirname(here), "nexrad-aws-2025",
                                   "kernel.py"))
    for base in (os.path.join(home, ".claude-science"),):
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            if os.path.basename(root) == "nexrad-aws-2025" and "kernel.py" in files:
                candidates.append(os.path.join(root, "kernel.py"))
            if root.count(os.sep) - base.count(os.sep) > 4:
                dirs[:] = []
    for path in candidates:
        if path and os.path.exists(path):
            spec = importlib.util.spec_from_file_location("nexrad_access", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            print(f"[0/5] access helpers: {path}", flush=True)
            return mod
    raise SystemExit(
        "Could not find nexrad-aws-2025/kernel.py. Set NEXRAD_AWS_2025_KERNEL "
        "to its path, or run from a directory containing nexrad-aws-2025/."
    )


def busy_window(K, site, client, hours=3, lookback_days=40):
    """Find a recent window with the most volumes -- a proxy for active weather.

    Calibrating on a quiet day understates volume size by ~40%, which is the
    single biggest error source in the cost model.
    """
    best = None
    now = dt.datetime.now(dt.timezone.utc)
    for back in (1, 3, 7, 14, 30, lookback_days):
        end = now - dt.timedelta(days=back)
        start = end - dt.timedelta(hours=hours)
        try:
            keys = K.nexrad_keys(site, start, end, client=client)
        except Exception:
            continue
        if not keys:
            continue
        mean_mb = statistics.fmean(k["size"] for k in keys) / 1e6
        if best is None or mean_mb > best[0]:
            best = (mean_mb, start, end, keys)
    if best is None:
        raise SystemExit(f"no volumes found for {site} in the last {lookback_days} days")
    return best


def measure_raw(K, client, keys, n, workdir):
    """Download n volumes for BANDWIDTH; take volume SIZE from the full listing.

    These are deliberately different samples. Bandwidth needs real transfers,
    so it is measured over n downloads. Volume size must not be: n is small (2
    in quick mode) and the few volumes at the end of a window are not
    representative of it -- a 13.5 MB convective window can easily hand you two
    8.5 MB volumes. Sizes come free from the LIST call, so use all of them.
    """
    os.makedirs(workdir, exist_ok=True)
    use = keys[-n:] if len(keys) >= n else keys
    mb_total, paths = 0.0, []
    t0 = time.time()
    for k in use:
        p = K.download_volume(k["key"], workdir, client=client, overwrite=True)
        mb_total += os.path.getsize(p) / 1e6
        paths.append(p)
    dl_s = time.time() - t0

    import pyart
    t0 = time.time()
    pyart.io.read_nexrad_archive(paths[0])
    full_s = time.time() - t0
    t0 = time.time()
    pyart.io.read_nexrad_archive(paths[0], delay_field_loading=True)
    lazy_s = time.time() - t0

    listed_mb = [k["size"] / 1e6 for k in keys]
    return {
        "raw_volume_MB": round(statistics.fmean(listed_mb), 2),
        "raw_MB_per_s": round(mb_total / dl_s, 2),
        "raw_decode_full_s": round(full_s, 2),
        "raw_decode_lazy_s": round(lazy_s, 2),
        "_n_downloaded": len(use),
        "_n_listed": len(keys),
        "_downloaded_mean_MB": round(mb_total / len(use), 2),
        "_download_s": round(dl_s, 1),
        "_downloaded_total_MB": round(mb_total, 1),
    }


def measure_volume_regimes(K, client, site, hours=3):
    """Mean volume size in a busy vs a calm window -- volume size is bimodal."""
    now = dt.datetime.now(dt.timezone.utc)
    sizes = {}
    for back in (1, 2, 3, 5, 7, 10, 14, 21, 30):
        end = now - dt.timedelta(days=back)
        try:
            keys = K.nexrad_keys(site, end - dt.timedelta(hours=hours), end,
                                 client=client)
        except Exception:
            continue
        if len(keys) >= 8:
            sizes[back] = statistics.fmean(k["size"] for k in keys) / 1e6
    if not sizes:
        return {}
    vals = sorted(sizes.values())
    return {
        "quiet": round(vals[0], 1),
        "mixed": round(statistics.fmean(vals), 1),
        "convective": round(vals[-1], 1),
        "_windows_sampled": len(vals),
        "_spread_MB": [round(v, 2) for v in vals],
    }


def measure_arco(K, site, when):
    """Open cost, time-axis cost, bare chunk, in-loop chunk, and probe cost."""
    out = {}
    t0 = time.time()
    root = K.arco_open(site)
    out["arco_open_s"] = round(time.time() - t0, 2)

    inv = K.arco_vcps(root)
    groups = list(inv["group"]) if hasattr(inv, "__getitem__") else []
    group = "VCP-212" if "VCP-212" in groups else (groups[0] if groups else None)
    if group is None:
        raise SystemExit(f"no VCP groups in the {site} ARCO repo")
    out["_group"] = group

    t0 = time.time()
    times = K.arco_times(root, group)
    out["arco_time_axis_s"] = round(time.time() - t0, 2)
    out["_n_scans"] = int(times.size)

    idx, _ = K.arco_nearest(root, group, when)
    g = root[group]
    sweeps = sorted((k for k, _ in g.groups()),
                    key=lambda s: int("".join(c for c in s if c.isdigit()) or 0))

    import numpy as np
    fields = [k for k, _ in g[sweeps[0]].arrays()]
    field = "DBZH" if "DBZH" in fields else next(
        (f for f in fields if g[sweeps[0]][f].ndim == 3), None)
    out["_field"] = field

    bare = []
    for sw in sweeps[:4]:
        if field in [k for k, _ in g[sw].arrays()]:
            t0 = time.time()
            arr = g[sw][field][idx]
            bare.append(time.time() - t0)
            out["arco_chunk_decoded_MB"] = round(arr.nbytes / 1e6, 2)
    out["arco_chunk_s"] = round(statistics.fmean(bare), 3)
    out["_bare_samples"] = len(bare)

    t0 = time.time()
    for sw in sweeps:
        int(np.int64(g[sw]["time"][idx, 0]))
    probe_s = (time.time() - t0) / len(sweeps)
    out["arco_probe_s"] = round(probe_s, 3)

    vol = K.arco_volume_indices(root, group, idx)
    t0 = time.time()
    reads = 0
    for k in vol:
        for sw in sweeps:
            if np.int64(g[sw]["time"][k, 0]) <= 0:
                continue
            g[sw][field][k]
            reads += 1
    loop_s = time.time() - t0
    n_probes = len(vol) * len(sweeps)
    out["arco_chunk_in_loop_s"] = round(
        max((loop_s - n_probes * probe_s) / max(reads, 1), out["arco_chunk_s"]), 3)
    out["_reassembly_s"] = round(loop_s, 2)
    out["_reassembly_indices"] = len(vol)
    out["_reassembly_reads"] = reads
    return out


def measure_lowsweeps(K, site, when):
    """Open + whole time axis, and per-scan read cost for the base-tilt cube."""
    out = {}
    t0 = time.time()
    root = K.arco_open(site, lowsweeps=True)
    times = K.arco_times(root, "sweep_0")
    out["lowsweeps_open_s"] = round(time.time() - t0, 2)
    out["_n_scans"] = int(times.size)

    import numpy as np
    j = int(np.searchsorted(times, np.datetime64(when)))
    j = max(0, min(j, times.size - 9))
    g = root["sweep_0"]
    fields = [k for k, _ in g.arrays()]
    field = "DBZH" if "DBZH" in fields else None
    if field is None:
        return out
    t0 = time.time()
    for k in range(j, j + 8):
        g[field][k]
    out["lowsweeps_scan_s"] = round((time.time() - t0) / 8, 3)
    out["_scans_sampled"] = 8
    return out


def measure_wire(K, client, site, n_objects=3000):
    """Compressed on-the-wire chunk size, from the icechunk chunk objects."""
    pag = client.get_paginator("list_objects_v2")
    sizes = []
    for page in pag.paginate(Bucket="nexrad-arco", Prefix=f"{site}/chunks/",
                             PaginationConfig={"MaxItems": n_objects}):
        sizes += [o["Size"] for o in page.get("Contents", [])]
    if not sizes:
        return {}
    big = sorted(s for s in sizes if s > 1e6)
    if not big:
        big = sorted(sizes)[-max(1, len(sizes) // 100):]
    return {"arco_chunk_wire_MB": round(statistics.median(big) / 1e6, 2),
            "_chunk_objects_sampled": len(sizes)}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--site", default="KLOT")
    ap.add_argument("--out", default="calibration.json")
    ap.add_argument("--quick", action="store_true",
                    help="2 volumes instead of 8; skip the wire-size sampling")
    ap.add_argument("--workdir", default="calib_tmp")
    ap.add_argument("--window", default="",
                    help="ISO start,end to force a specific window")
    args = ap.parse_args()

    ensure_ca()
    K = find_access_helpers()
    client = K.s3_anon()
    site = args.site.upper()

    if args.window:
        a, b = args.window.split(",")
        start = dt.datetime.fromisoformat(a).replace(tzinfo=dt.timezone.utc)
        end = dt.datetime.fromisoformat(b).replace(tzinfo=dt.timezone.utc)
        keys = K.nexrad_keys(site, start, end, client=client)
        if not keys:
            raise SystemExit(f"no volumes for {site} in {args.window}")
        mean_mb = statistics.fmean(k["size"] for k in keys) / 1e6
    else:
        mean_mb, start, end, keys = busy_window(K, site, client)

    print(f"[1/5] window {start:%Y-%m-%d %H:%M} -> {end:%H:%M}Z, "
          f"{len(keys)} volumes, mean {mean_mb:.2f} MB", flush=True)

    cost = {}
    n = 2 if args.quick else 8
    cost.update(measure_raw(K, client, keys, n, args.workdir))
    print(f"[2/5] raw: {cost['raw_volume_MB']} MB/vol at "
          f"{cost['raw_MB_per_s']} MB/s", flush=True)

    regimes = measure_volume_regimes(K, client, site)
    print(f"[3/5] volume regimes: {regimes.get('quiet')} / {regimes.get('mixed')} "
          f"/ {regimes.get('convective')} MB", flush=True)

    when = (start + (end - start) / 2).replace(tzinfo=None).isoformat(
        timespec="seconds")
    arco, low, wire = {}, {}, {}
    try:
        arco = measure_arco(K, site, when)
        print(f"[4/5] ARCO: chunk {arco.get('arco_chunk_s')}s, "
              f"probe {arco.get('arco_probe_s')}s", flush=True)
        low = measure_lowsweeps(K, site, when)
        if not args.quick:
            wire = measure_wire(K, client, site)
        print(f"[5/5] lowsweeps: {low.get('lowsweeps_scan_s')}s per scan", flush=True)
    except Exception as exc:
        print(f"[!] ARCO measurement skipped: {type(exc).__name__}: "
              f"{str(exc)[:160]}", flush=True)

    cost.update(arco)
    cost.update(low)
    cost.update(wire)

    doc = {
        "COST": {k: v for k, v in cost.items() if not k.startswith("_")},
        "VOLUME_MB_BY_REGIME": {k: v for k, v in regimes.items()
                                if not k.startswith("_")},
        "provenance": {
            "site": site,
            "measured_at": dt.datetime.now(dt.timezone.utc).isoformat(
                timespec="seconds"),
            "window": [start.isoformat(timespec="seconds"),
                       end.isoformat(timespec="seconds")],
            "window_mean_volume_MB": round(mean_mb, 2),
            "quick": bool(args.quick),
            "python": sys.version.split()[0],
            "observations": {k: v for k, v in
                             list(cost.items()) + list(regimes.items())
                             if k.startswith("_")},
        },
    }
    with open(args.out, "w") as fh:
        json.dump(doc, fh, indent=1)
    print(f"\nwrote {args.out}")
    print(json.dumps(doc["COST"], indent=1))
    return doc


if __name__ == "__main__":
    main()
