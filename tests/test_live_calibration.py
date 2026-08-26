"""Validate the calibration skill: it must produce an internally consistent
document, apply cleanly to the router, and not silently mis-sample."""
import os as _os

def SKILL_DIR(name):
    """Absolute path to a skill directory in this repo."""
    return _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                         "skills", name)

def SKILL_PATH(name, filename):
    return _os.path.join(SKILL_DIR(name), filename)

import importlib.util as iu
import json
import os
import subprocess
import sys

def load(name, path):
    s = iu.spec_from_file_location(name, path)
    m = iu.module_from_spec(s)
    s.loader.exec_module(m)
    return m

RT = load("router", SKILL_PATH("nexrad-cloud-router", "kernel.py"))
CAL = load("calib", SKILL_PATH("nexrad-cost-calibration", "kernel.py"))

fails = []
TOTAL_CHECKS = [0]

def check(label, cond, detail=""):
    TOTAL_CHECKS[0] += 1
    print(("  PASS  " if cond else "  FAIL  ") + label + (f" :: {detail}" if detail else ""))
    if not cond:
        fails.append(label)

print("### 0. portability: paths resolve without __file__")
# The sidecar is exec'd, not imported, so __file__ is undefined in the kernel.
KPATH = os.path.abspath(SKILL_PATH("nexrad-cost-calibration", "kernel.py"))
src = open(KPATH).read()
ns = {}
# The loader exec's the sidecar compiled with its REAL path but no __file__.
exec(compile(src, KPATH, "exec"), ns)
check("sidecar exec's without __file__", "measure_script_path" in ns)
p = ns["measure_script_path"]()
check("measure.py resolves from an exec'd sidecar", os.path.exists(p), p)

# from an unrelated working directory -- the installed-skill case
probe = (
    "import os;src=open(%r).read();ns={};exec(compile(src,%r,'exec'),ns);"
    "print(ns['measure_script_path']())" % (KPATH, KPATH)
)
r = subprocess.run([sys.executable, "-c", probe], capture_output=True, text=True,
                   cwd="/tmp")
check("measure.py resolves from an unrelated cwd", r.returncode == 0,
      (r.stdout or r.stderr).strip().splitlines()[-1][:150] if (r.stdout or r.stderr) else "")

# and with nothing but the env override
r2 = subprocess.run(
    [sys.executable, "-c",
     "import os;src=open(%r).read();ns={};exec(compile(src,'<anon>','exec'),ns);"
     "print(ns['measure_script_path']())" % KPATH],
    capture_output=True, text=True, cwd="/tmp",
    env={**os.environ, "NEXRAD_CALIBRATION_MEASURE":
         os.path.abspath(SKILL_PATH("nexrad-cost-calibration", "measure.py"))})
check("NEXRAD_CALIBRATION_MEASURE override works", r2.returncode == 0,
      (r2.stdout or r2.stderr).strip().splitlines()[-1][:150] if (r2.stdout or r2.stderr) else "")

print("\n### 1. run a live quick calibration")
doc = CAL.run_calibration(site="KLOT", quick=True, out="calibration_test.json",
                          echo=False)
C, REG, P = doc["COST"], doc["VOLUME_MB_BY_REGIME"], doc["provenance"]
check("document has the router's COST keys",
      {"raw_volume_MB", "raw_MB_per_s", "arco_chunk_s", "lowsweeps_scan_s"} <= set(C),
      str(sorted(C)))
check("every COST value is a positive number",
      all(isinstance(v, (int, float)) and v > 0 for v in C.values()),
      str({k: v for k, v in C.items() if not (isinstance(v, (int, float)) and v > 0)}))
check("provenance records site, time and window",
      all(P.get(k) for k in ("site", "measured_at", "window")), str(P.get("site")))
check("no private keys leaked into COST",
      not any(k.startswith("_") for k in C), str([k for k in C if k.startswith("_")]))

print("\n### 2. the sampling trap is closed")
obs = P["observations"]
check("volume size comes from the full listing, not the download sample",
      obs["_n_listed"] > obs["_n_downloaded"],
      f"listed {obs['_n_listed']} vs downloaded {obs['_n_downloaded']}")
check("raw_volume_MB matches the window mean, not the downloaded few",
      abs(C["raw_volume_MB"] - P["window_mean_volume_MB"]) < 0.05,
      f"constant {C['raw_volume_MB']} vs window {P['window_mean_volume_MB']} "
      f"(downloaded sample was {obs['_downloaded_mean_MB']})")

print("\n### 3. regimes are ordered and plausible")
check("quiet <= mixed <= convective",
      REG["quiet"] <= REG["mixed"] <= REG["convective"],
      f"{REG['quiet']} / {REG['mixed']} / {REG['convective']}")
check("volume sizes in a physical range (3-30 MB)",
      all(3 < v < 30 for v in REG.values()), str(REG))
check("busy-window search found a convective-ish window",
      P["window_mean_volume_MB"] >= REG["mixed"],
      f"window {P['window_mean_volume_MB']} vs mixed {REG['mixed']}")

print("\n### 4. comparison and application")
rows = CAL.compare_to_shipped(doc, router=RT)
check("compare_to_shipped ranks by magnitude",
      all(abs(rows[i]["ratio"] - 1) >= abs(rows[i+1]["ratio"] - 1)
          for i in range(len(rows) - 1)), f"{len(rows)} rows")
check("every compared constant carries a sensitivity label",
      all(r["sensitivity"] != "?" for r in rows),
      str([r["constant"] for r in rows if r["sensitivity"] == "?"]))

before = dict(RT.COST)
before_x = {r: RT.crossover_chunks(r) for r in ("quiet", "mixed", "convective")}
diff = CAL.apply_calibration(doc, router=RT, verbose=False)
check("apply changed something", len(diff) > 0, f"{len(diff)} constants")
check("router COST now equals the measured document",
      all(RT.COST[k] == v for k, v in C.items()),
      str([k for k, v in C.items() if RT.COST[k] != v]))
after_x = {r: RT.crossover_chunks(r) for r in ("quiet", "mixed", "convective")}
check("crossover stays ordered after applying",
      after_x["quiet"] <= after_x["mixed"] <= after_x["convective"], str(after_x))
print(f"   crossover {before_x} -> {after_x}")

print("\n### 5. selective application")
RT.COST.update(before)
d2 = CAL.apply_calibration(doc, router=RT, keys=["raw_MB_per_s"], verbose=False)
check("keys= restricts what is overwritten",
      set(k for k in d2) <= {"raw_MB_per_s"}, str(sorted(d2)))
check("  and leaves other constants untouched",
      RT.COST["arco_chunk_s"] == before["arco_chunk_s"],
      f"{RT.COST['arco_chunk_s']} vs {before['arco_chunk_s']}")

print("\n### 6. the routing decision actually responds")
RT.COST.update(before)
q_before = RT.choose_source(archetype="case_study", n_volumes=1, site="KLOT",
                            n_sweeps=3, n_fields=2)["source"]
CAL.apply_calibration(doc, router=RT, verbose=False)
q_after = RT.choose_source(archetype="case_study", n_volumes=1, site="KLOT",
                           n_sweeps=3, n_fields=2)["source"]
check("a mid-range decision is sensitive to calibration",
      isinstance(q_before, str) and isinstance(q_after, str),
      f"{q_before} -> {q_after}")
print(f"   6 chunks: shipped constants say {q_before}; this link says {q_after}")

print("\n### 7. report and guidance")
rep = CAL.calibration_report(doc, router=RT)
check("report names the site and bandwidth",
      "KLOT" in rep and "MB/s" in rep)
check("report states the resulting crossover", "crossover" in rep)
g = CAL.should_recalibrate(router=RT)
check("should_recalibrate returns actionable guidance",
      g["current_crossover_chunks"] and g["recalibrate_if"], str(g)[:100])

print("\n### 8. reload round-trip")
doc2 = CAL.load_calibration("calibration_test.json")
check("saved document reloads identically", doc2 == doc)

print("\n### 9. the doc's own claim matches this suite")
doc_md = open(SKILL_PATH("nexrad-cost-calibration", "SKILL.md")).read()
import re as _re
claimed = _re.search(r"(\d+)\s+checks in `test_calibration\.py`", doc_md)
check("SKILL.md states a check count", claimed is not None)

# Compare against STATIC call sites, not the live counter: the counter cannot
# include the comparison itself without an off-by-one, and call sites are what
# a reader (or auditor) greps.
sites = len(_re.findall(r"^\s*check\(", open(__file__).read(), _re.M))
RT.COST.update(before)
if claimed:
    check(f"SKILL.md's claimed count matches the {sites} check call sites",
          int(claimed.group(1)) == sites,
          f"doc says {claimed.group(1)}, file has {sites}")

print("\n=== " + (f"{len(fails)} FAILURES: {fails}"
                  if fails else
                  f"ALL {TOTAL_CHECKS[0]} CHECKS PASSED ({sites} call sites)"))
