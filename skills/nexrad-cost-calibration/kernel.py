"""Recalibrate the NEXRAD access-path cost model for THIS machine and link.

The router (nexrad-cloud-router) ships constants measured on one sandbox. They
travel badly: bandwidth is environment-specific, and volume size depends on the
weather in the window you sampled. These helpers re-measure and apply.

The measurement itself runs in a SUBPROCESS (measure.py) on purpose -- the
icechunk Rust client caches its TLS trust store on first import, so a kernel
that has already touched icechunk cannot be corrected in place.
"""

import json
import os
import subprocess
import sys

CALIBRATION_FILENAME = "calibration.json"

# Constants worth re-measuring, and how far they travel between environments.
# "link" = set by network path; "weather" = set by what the radar was seeing;
# "machine" = set by local CPU/disk.
CONSTANT_SENSITIVITY = {
    "raw_MB_per_s": "link",
    "arco_chunk_s": "link",
    "arco_chunk_in_loop_s": "link",
    "arco_probe_s": "link",
    "lowsweeps_scan_s": "link",
    "arco_open_s": "link",
    "arco_time_axis_s": "link",
    "lowsweeps_open_s": "link",
    "raw_volume_MB": "weather",
    "arco_chunk_wire_MB": "weather",
    "arco_chunk_decoded_MB": "fixed",
    "raw_decode_full_s": "machine",
    "raw_decode_lazy_s": "machine",
}


SKILL_DIRNAME = "nexrad-cost-calibration"


def measure_script_path():
    """Absolute path to measure.py, which must run as its own process.

    The sidecar is exec'd into the kernel rather than imported, so `__file__`
    is not defined here -- resolve by searching the installed skill directory,
    the working directory, and NEXRAD_CALIBRATION_MEASURE.
    """
    override = os.environ.get("NEXRAD_CALIBRATION_MEASURE", "")
    candidates = [override] if override else []
    # The loader compiles this sidecar with its real path, so the code object
    # knows where it lives even though `__file__` is absent.
    own = measure_script_path.__code__.co_filename
    if own and os.path.sep in own:
        candidates.append(os.path.join(os.path.dirname(own), "measure.py"))
    candidates += [
        os.path.join(os.getcwd(), SKILL_DIRNAME, "measure.py"),
        os.path.join(os.getcwd(), "measure.py"),
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return os.path.abspath(path)
    raise FileNotFoundError(
        "measure.py not found. Set NEXRAD_CALIBRATION_MEASURE to its path, or "
        f"run from a directory containing {SKILL_DIRNAME}/measure.py."
    )


def run_calibration(site="KLOT", out=None, quick=False, window=None,
                    access_kernel=None, timeout=1800, echo=True):
    """Run the measurement subprocess and return the calibration document.

    `quick=True` uses 2 volumes instead of 8 and skips wire-size sampling --
    about a third of the runtime, enough to refresh bandwidth. `window` is
    "ISO,ISO" to force a specific period; by default the script searches recent
    days for the busiest window, since calibrating on a quiet day understates
    volume size.

    `access_kernel` is the path to nexrad-aws-2025/kernel.py if it is not
    beside this skill or under the working directory.
    """
    out = out or CALIBRATION_FILENAME
    cmd = [sys.executable, measure_script_path(), "--site", site, "--out", out]
    if quick:
        cmd.append("--quick")
    if window:
        cmd += ["--window", window]
    env = dict(os.environ)
    if access_kernel:
        env["NEXRAD_AWS_2025_KERNEL"] = access_kernel
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                          env=env)
    if echo and proc.stdout:
        print(proc.stdout.rstrip())
    if proc.returncode != 0:
        raise RuntimeError(f"calibration failed (exit {proc.returncode}):\n"
                           + (proc.stderr or "")[-1200:])
    with open(out) as fh:
        return json.load(fh)


def load_calibration(path=None):
    """Read a calibration document written by run_calibration()."""
    with open(path or CALIBRATION_FILENAME) as fh:
        return json.load(fh)


def apply_calibration(doc, router=None, keys=None, verbose=True):
    """Write measured constants into the router's COST / VOLUME_MB_BY_REGIME.

    `router` defaults to the loaded nexrad-cloud-router helpers in the calling
    kernel. `keys` restricts which constants are overwritten -- useful when you
    trust the measurement's bandwidth but not its weather regime. Returns the
    before/after diff.
    """
    g = router if router is not None else globals()
    get = (lambda name: getattr(g, name)) if router is not None else g.get
    cost = get("COST")
    if cost is None:
        raise RuntimeError("load the nexrad-cloud-router skill first "
                           "(no COST dict in scope)")
    regimes = get("VOLUME_MB_BY_REGIME")

    diff = {}
    for k, v in (doc.get("COST") or {}).items():
        if keys and k not in keys:
            continue
        if k in cost and cost[k] != v:
            diff[k] = (cost[k], v)
        cost[k] = v
    if regimes is not None and not keys:
        for k, v in (doc.get("VOLUME_MB_BY_REGIME") or {}).items():
            if k in regimes and regimes[k] != v:
                diff[f"regime:{k}"] = (regimes[k], v)
            regimes[k] = v

    if verbose and diff:
        for k, (old, new) in sorted(diff.items()):
            pct = (new - old) / old * 100 if isinstance(old, (int, float)) and old else 0
            print(f"  {k:24s} {old!s:>8} -> {new!s:<8} ({pct:+.0f}%)")
    return diff


def calibration_report(doc, router=None):
    """Human-readable summary: what was measured, and what it implies."""
    cost = doc.get("COST", {})
    reg = doc.get("VOLUME_MB_BY_REGIME", {})
    prov = doc.get("provenance", {})
    lines = [
        f"site {prov.get('site')} measured {prov.get('measured_at')}",
        f"window {prov.get('window', ['?', '?'])[0]} .. "
        f"{prov.get('window', ['?', '?'])[1]}"
        f"  (mean volume {prov.get('window_mean_volume_MB')} MB"
        + (", QUICK mode" if prov.get("quick") else "") + ")",
        "",
        f"  bandwidth        {cost.get('raw_MB_per_s')} MB/s",
        f"  raw volume       {cost.get('raw_volume_MB')} MB "
        f"(quiet {reg.get('quiet')} / mixed {reg.get('mixed')} / "
        f"convective {reg.get('convective')})",
        f"  ARCO chunk       {cost.get('arco_chunk_s')}s bare, "
        f"{cost.get('arco_chunk_in_loop_s')}s in loop, "
        f"{cost.get('arco_probe_s')}s per probe",
        f"  lowsweeps scan   {cost.get('lowsweeps_scan_s')}s",
    ]
    g = router if router is not None else globals()
    fn = (getattr(g, "crossover_chunks", None) if router is not None
          else g.get("crossover_chunks"))
    if fn is not None:
        lines += ["",
                  "  crossover (sweep x field chunks) after applying: "
                  + ", ".join(f"{r} {fn(r)}" for r in ("quiet", "mixed",
                                                       "convective"))]
    return "\n".join(lines)


def compare_to_shipped(doc, router=None):
    """Which shipped constants this environment disagrees with, and by how much.

    Reports the ratio rather than a verdict: a 2x slower link is worth applying,
    a 10% difference is noise. Sorted by magnitude.
    """
    g = router if router is not None else globals()
    get = (lambda name: getattr(g, name)) if router is not None else g.get
    cost = get("COST")
    if cost is None:
        raise RuntimeError("load the nexrad-cloud-router skill first")
    rows = []
    for k, new in (doc.get("COST") or {}).items():
        old = cost.get(k)
        if not isinstance(old, (int, float)) or not isinstance(new, (int, float)):
            continue
        if not old:
            continue
        rows.append({"constant": k, "shipped": old, "measured": new,
                     "ratio": round(new / old, 2),
                     "sensitivity": CONSTANT_SENSITIVITY.get(k, "?")})
    rows.sort(key=lambda r: abs(r["ratio"] - 1.0), reverse=True)
    return rows


def should_recalibrate(router=None, threshold_ratio=1.3):
    """Cheap heuristic: is a full recalibration likely to change a decision?

    Runs no measurement itself -- it reports what to check. Recalibrate when
    the link differs materially from the shipped 1.2 MB/s, since bandwidth sets
    the raw-vs-ARCO crossover; a decision far from the crossover is insensitive
    to all of this.
    """
    g = router if router is not None else globals()
    get = (lambda name: getattr(g, name)) if router is not None else g.get
    cost = get("COST") or {}
    fn = (getattr(g, "crossover_chunks", None) if router is not None
          else g.get("crossover_chunks"))
    now = fn() if fn else None
    return {
        "shipped_bandwidth_MB_per_s": cost.get("raw_MB_per_s"),
        "current_crossover_chunks": now,
        "recalibrate_if": [
            "the link is not the machine the constants were measured on",
            f"a decision sits within {threshold_ratio:g}x of the crossover "
            f"({now} chunks)" if now else "a decision sits near the crossover",
            "you are costing a convective case with quiet-window constants",
        ],
        "cheapest_check": "run_calibration(quick=True) then compare_to_shipped()",
    }
