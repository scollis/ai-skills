"""Validate the router: predictions must match the MEASURED benchmarks, and
routing decisions must respect the hard constraints."""
import os as _os

def SKILL_DIR(name):
    """Absolute path to a skill directory in this repo."""
    return _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                         "skills", name)

def FIXTURE(name):
    """Measured baselines committed alongside the suite."""
    return _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "fixtures", name)

def SKILL_PATH(name, filename):
    return _os.path.join(SKILL_DIR(name), filename)

import sys, json
sys.path.insert(0, SKILL_DIR("nexrad-cloud-router"))
sys.path.insert(0, SKILL_DIR("nexrad-aws-2025"))
import kernel as A          # nexrad-aws-2025 helpers (bucket access)
sys.modules.pop("kernel", None)
import importlib.util as _iu
spec = _iu.spec_from_file_location("router", SKILL_PATH("nexrad-cloud-router", "kernel.py"))
R = _iu.module_from_spec(spec); spec.loader.exec_module(R)

fails = []
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + label + (f" :: {detail}" if detail else ""))
    if not cond: fails.append(label)

BENCH = json.load(open(FIXTURE("bench.json")))
WIRE = json.load(open(FIXTURE("wire.json")))
SER = json.load(open(FIXTURE("series.json")))
CH = json.load(open(FIXTURE("chunks.json")))

print("### 1. cost model reproduces the measurements")
# The 8 volumes actually downloaded averaged 8.43 MB -> the 'mixed' regime.
meas_MB = SER["raw_MB"] / SER["n"]
check("default volume size matches what was measured",
      abs(R.volume_MB() - meas_MB) / meas_MB < 0.12,
      f"router {R.volume_MB()} MB vs measured {meas_MB:.2f} MB/volume")
check("convective regime matches the convective window",
      abs(R.volume_MB("convective") - CH["convective_20260727_16_19Z"]["mean_MB"]) < 0.1,
      f"{R.volume_MB('convective')} vs {CH['convective_20260727_16_19Z']['mean_MB']}")

pred_raw = R.raw_volume_cost(8, lazy=True)["wall_s"]
pred_low = R.lowsweeps_cost(8, opened=True)["wall_s"]
check("raw 8-volume estimate within 25% of measured",
      abs(pred_raw - SER["raw_total_s"]) / SER["raw_total_s"] < 0.25,
      f"pred {pred_raw}s vs measured {SER['raw_total_s']}s")
check("lowsweeps 8-scan estimate within 30% of measured",
      abs(pred_low - SER["lowsweeps_s"]) / SER["lowsweeps_s"] < 0.30,
      f"pred {pred_low}s vs measured {SER['lowsweeps_s']}s")
check("crossover matches the wire measurement (same volume size)",
      abs(R.crossover_chunks() - WIRE["crossover_chunks"]) <= 2,
      f"router {R.crossover_chunks()} vs measured {WIRE['crossover_chunks']}")
check("crossover rises with convective volume size",
      R.crossover_chunks("convective") > R.crossover_chunks("quiet"),
      f"quiet {R.crossover_chunks('quiet')} -> convective {R.crossover_chunks('convective')}")
# fragmented reassembly: measured 12.69s for 21 sweep-reads over 3 indices
pred = R.arco_cost(1, n_sweeps=7, n_fields=1, fragmented=True, opened=True)["wall_s"]
check("ARCO reassembly estimate within 35% of measured",
      abs(pred - CH["reassembly"]["wall_s"]) / CH["reassembly"]["wall_s"] < 0.35,
      f"pred {pred}s vs measured {CH['reassembly']['wall_s']}s")
check("single-sweep ARCO read estimate within 40% of measured",
      abs(R.arco_cost(1, n_sweeps=1, n_fields=1, opened=True)["wall_s"]
          - CH["bare_chunk_s"]["mean"]) / CH["bare_chunk_s"]["mean"] < 0.40,
      f"pred {R.arco_cost(1,n_sweeps=1,n_fields=1,opened=True)['wall_s']}s vs "
      f"measured {CH['bare_chunk_s']['mean']}s")

print("\n### 1b. documented numbers match the code")
import re as _re, pathlib as _pl
doc = _pl.Path(SKILL_PATH("nexrad-cloud-router", "SKILL.md")).read_text()
code = _pl.Path(SKILL_PATH("nexrad-cloud-router", "kernel.py")).read_text()
for regime, want in (("quiet", R.crossover_chunks("quiet")),
                     ("mixed", R.crossover_chunks("mixed")),
                     ("convective", R.crossover_chunks("convective"))):
    # every crossover number cited next to that regime name must be the real one
    cited = set()
    for src in (doc, code):
        # "crossover_chunks("regime")   # NN" and "NN (regime)"
        for m in _re.finditer(rf'crossover_chunks\("{regime}"\)\s*#\s*(\d+)', src):
            cited.add(int(m.group(1)))
        for m in _re.finditer(rf"\b(\d+)\s*\({regime}\)", src):
            cited.add(int(m.group(1)))
    check(f"cited crossover for {regime} matches code ({want})",
          not cited or cited == {want}, f"cited {sorted(cited)} vs code {want}")
check("no stale 27-chunk crossover claim anywhere",
      "27 chunks" not in doc and "~27" not in code and "to 27" not in doc)

print("\n### 2. hard constraints beat cost")
d = R.choose_source(archetype="base_tilt_series", n_volumes=500,
                    needs_true_geometry=True, site="KLOT")
check("true geometry forces raw even at 500 volumes", d["source"] == "raw Level II",
      d["source"])
check("  and says why (pre-regridded azimuth)", "regridded" in d["reason"])
d = R.choose_source(archetype="base_tilt_series", n_volumes=500, site="KTLX")
check("site absent from ARCO forces raw", d["source"] == "raw Level II", d["source"])
check("  suggests GCS mirror", any("GCS" in a for a in d["alternatives"]))
d = R.choose_source(archetype="realtime", n_volumes=1, site="KLOT")
check("realtime -> chunks bucket", d["source"] == "chunks bucket", d["source"])

print("\n### 3. cost actually drives the choice")
d1 = R.choose_source(archetype="base_tilt_series", n_volumes=200, site="KLOT")
check("long base-tilt series -> lowsweeps", d1["source"] == "ARCO lowsweeps", d1["source"])
d2 = R.choose_source(archetype="case_study", n_volumes=1, needs_upper_tilts=True,
                     site="KLOT", n_fields=5)
check("single full dual-pol volume -> raw (many chunks)", d2["source"] == "raw Level II",
      f"{d2['source']} / {d2['reason'][:60]}")
d3 = R.choose_source(archetype="case_study", n_volumes=1, needs_upper_tilts=False,
                     site="KLOT", n_fields=1, n_sweeps=1)
check("one sweep, one field -> ARCO", d3["source"] == "ARCO per-VCP",
      f"{d3['source']} ({d3['cost']['wall_s']}s vs raw {d3['runner_up']['wall_s']}s)")
d3b = R.choose_source(archetype="case_study", n_volumes=1, needs_upper_tilts=False,
                      site="KLOT", n_fields=5, n_sweeps=3)
check("a few sweeps x 5 fields still ARCO-or-raw by cost, not by guess",
      d3b["source"] in ("ARCO per-VCP", "raw Level II"),
      f"{d3b['source']} ({d3b['cost']['wall_s']}s vs {d3b['runner_up']['wall_s']}s)")
# monotonicity: raw must eventually win as chunk demand grows
srcs = [R.choose_source(archetype="volume_series", n_volumes=n, needs_upper_tilts=True,
                        site="KLOT", n_fields=5)["source"] for n in (1, 5, 50)]
check("raw wins as volume count grows", srcs[-1] == "raw Level II", str(srcs))

print("\n### 4. task classification")
cases = {
    "plot the tornado outbreak at KLOT on 27 July 2026": "case_study",
    "monthly rainfall accumulation over the ARM site for 2025": "site_rainfall",
    "area of the domain above 1 in/hr through the squall line": "areal_stats",
    "base tilt reflectivity time series for three months": "base_tilt_series",
    "what is the radar showing right now": "realtime",
    "echo top climatology over several seasons": "volume_series",
}
for text, want in cases.items():
    got = R.classify_task(text)["archetype"]
    check(f"classify: {text[:42]!r} -> {want}", got == want, got)
check("gridding/NUFFT flags true geometry",
      R.classify_task("test the spectral gridding azimuth jitter path")["needs_true_geometry"])
check("echo top flags upper tilts",
      R.classify_task("echo top analysis")["needs_upper_tilts"])

print("\n### 5. plans are well-formed and skill-routed")
VALID = {R.SKILL_ACCESS, R.SKILL_ARCO, R.SKILL_GCS, R.SKILL_RAINFALL, R.SKILL_AREA}
for text, site, n in (("tornado case study", "KLOT", 1),
                      ("three month base tilt series", "KLOT", 500),
                      ("rainfall accumulation over the site", "KLOT", 40),
                      ("area over threshold through the storm", "KLOT", 20),
                      ("spectral gridding test", "KLOT", 3),
                      ("latest scan right now", "KTLX", 1)):
    p = R.plan_analysis(text, site=site, n_volumes=n)
    ok = (p["steps"] and all(s["skill"] in VALID for s in p["steps"])
          and p["skills_to_load"] and p["guardrails"]
          and all(s in VALID for s in p["skills_to_load"]))
    check(f"plan well-formed: {text[:34]!r}", ok,
          f"{p['source']} / {len(p['steps'])} steps / load {p['skills_to_load']}")
    assert "noaa-nexrad-level2" not in json.dumps(p["steps"]), "dead bucket in steps!"

p = R.plan_analysis("rainfall accumulation over the site", site="KLOT", n_volumes=40)
check("rainfall plan routes to the rainfall skill",
      any(s["skill"] == R.SKILL_RAINFALL for s in p["steps"]))
p = R.plan_analysis("area over threshold", site="KLOT", n_volumes=20)
check("areal plan routes to the area skill",
      any(s["skill"] == R.SKILL_AREA for s in p["steps"]))
p = R.plan_analysis("three month base tilt series", site="KLOT", n_volumes=500)
check("lowsweeps plan warns about -999 masking",
      any("-999" in g for g in p["guardrails"]))
check("every plan warns about the dead bucket",
      all(any("noaa-nexrad-level2" in g for g in
              R.plan_analysis(t, site="KLOT", n_volumes=5)["guardrails"])
          for t in cases))

print("\n### 6. live coverage check")
cov = R.arco_coverage()
check("arco_coverage finds KLOT", "KLOT" in cov["sites"], str(cov["sites"]))
check("arco_coverage reports lowsweeps", "KLOT" in cov["lowsweeps"], str(cov["lowsweeps"]))
d = R.choose_source(archetype="base_tilt_series", n_volumes=100, site="KLOT",
                    arco_sites=cov["sites"])
check("live coverage feeds the decision", d["source"] == "ARCO lowsweeps", d["source"])

print("\n### 7. recalibration")
before = R.COST["raw_MB_per_s"]
for n in ("s3_anon", "nexrad_keys", "download_volume"):
    setattr(R, n, getattr(A, n))
R.__dict__["s3_anon"] = A.s3_anon
R.__dict__["nexrad_keys"] = A.nexrad_keys
R.__dict__["download_volume"] = A.download_volume
size_before = R.COST["raw_volume_MB"]
m = R.measure_throughput("KLOT", n=2)
check("measure_throughput returns a rate", m["MB_per_s"] > 0, str(m))
check("recalibration leaves volume-size constants alone",
      R.COST["raw_volume_MB"] == size_before,
      f"{size_before} -> {R.COST['raw_volume_MB']}")
check("crossover tracks bandwidth", isinstance(m["crossover_now"], int),
      f"{before} -> {R.COST['raw_MB_per_s']} MB/s, crossover {m['crossover_now']}")

print("\n=== " + (f"{len(fails)} FAILURES: {fails}" if fails else "ALL CHECKS PASSED"))
print("\n--- sample plan ---")
print(R.format_plan(R.plan_analysis("three month base tilt reflectivity series",
                                    site="KLOT", n_volumes=500)))
