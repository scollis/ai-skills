"""Exercise every kernel.py helper against live buckets + local volumes."""
import os as _os

def SKILL_DIR(name):
    """Absolute path to a skill directory in this repo."""
    return _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                         "skills", name)

def SKILL_PATH(name, filename):
    return _os.path.join(SKILL_DIR(name), filename)

import sys, datetime as dt, glob, os
sys.path.insert(0, SKILL_DIR("nexrad-aws-2025"))
import kernel as K           # noqa: E402  (must precede any icechunk import)
K.ensure_ca()
import numpy as np           # noqa: E402

fails = []
def check(label, cond, detail=""):
    print(("  PASS  " if cond else "  FAIL  ") + label + (f" :: {detail}" if detail else ""))
    if not cond:
        fails.append(label)

print("### 1. archive bucket listing")
c = K.s3_anon()
keys = K.nexrad_keys("KLOT", dt.datetime(2026, 7, 27, 16, 0), dt.datetime(2026, 7, 27, 19, 0), client=c)
check("nexrad_keys returns volumes", len(keys) > 20, f"n={len(keys)}")
check("no MDM sidecars", not any(k["name"].endswith("_MDM") for k in keys))
check("all >=1.5MB", all(k["size"] >= 1_500_000 for k in keys),
      f"min={min(k['size'] for k in keys)}")
check("times sorted+in-window", all(keys[i]["time"] <= keys[i+1]["time"] for i in range(len(keys)-1)))
print("   first:", keys[0]["name"], keys[0]["time"], keys[0]["size"])

lv = K.latest_volume("KLOT", client=c)
lag = (dt.datetime.now(dt.timezone.utc) - lv["time"]).total_seconds() / 60
check("latest_volume fresh (<40 min)", lag < 40, f"{lv['name']} lag={lag:.1f} min")

sites = K.nexrad_sites(client=c)
check("nexrad_sites ~200", 150 < len(sites) < 260, f"n={len(sites)}")
check("KLOT in sites", "KLOT" in sites)

vols = K.realtime_chunks("KLOT", client=c)
check("realtime_chunks lists volumes", len(vols) > 5, f"n={len(vols)} e.g. {vols[:3]}")
ch = K.realtime_chunks("KLOT", client=c, volume=vols[-1])
check("chunk objects have kinds", set(x["kind"] for x in ch) <= set("SIE"),
      f"n={len(ch)} kinds={sorted(set(x['kind'] for x in ch))}")

print("\n### 2. VCP table + classifier")
check("VCP_TABLE has 212", K.vcp_info(212)["mode"] == "precip")
check("VCP 31 is clear-air long pulse", K.vcp_info(31)["mode"] == "clear-air")
cases = {
    "plain 212": ([0.48,0.48,0.88,0.88,1.27,1.27,1.8,2.42,3.08,4.0,5.1,6.42,8.0,10.02,12.48,15.6,19.51], "none"),
    "SAILSx2":   ([0.48,0.48,0.88,0.88,1.27,1.27,0.48,0.48,1.8,2.42,3.08,4.0,5.1,6.42,0.48,0.48,8.0,10.02,12.48,15.6,19.51], "SAILSx2"),
    "MRLE+4":    ([0.48,0.48,0.88,0.88,1.27,1.27,1.8,2.42,3.08,4.0,5.1,6.42,0.48,0.48,0.88,0.88,1.27,1.27,1.8,8.0,10.02,12.48,15.6,19.51], "MRLE+4"),
    "SAILSx1":   ([0.48,0.48,0.88,0.88,1.27,1.27,1.8,2.42,3.08,4.0,5.1,6.42,0.48,0.48,8.0,10.02,12.48,15.6,19.51], "SAILSx1"),
}
for lbl, (el, want) in cases.items():
    got = K.classify_scan(el, 212)
    check(f"classify {lbl} -> {want}", got["mode"] == want, got["mode"])
avs = K.classify_scan([0.48,0.48,0.88,0.88,1.27,1.27,1.8,2.42,3.08,4.0,5.1,6.42], 212)
check("AVSET truncation detected", avs["avset_active"] and avs["mode"] == "none",
      f"top={avs['backbone_top']} nominal={avs['nominal_top']}")
check("no false AVSET on full volume", not K.classify_scan(cases["plain 212"][0], 212)["avset_active"])

print("\n### 3. Py-ART volume helpers")
d = os.path.expanduser("~/data/REAL/klot_20260727")
files = sorted(glob.glob(d + "/*_V06"))
if files:
    r = K.read_nexrad_volume(files[0])
    df = K.scan_anatomy(r)
    check("scan_anatomy rows == nsweeps", len(df) == r.nsweeps, f"{len(df)}/{r.nsweeps}")
    check("split cuts paired", (df.split_partner >= 0).sum() == 6,
          f"paired={(df.split_partner>=0).sum()}")
    check("kinds sane", set(df.kind) <= {"surv","dop","batch"}, str(sorted(set(df.kind))))
    kept = K.dedup_split_cuts(r)
    check("dedup gives 14 unique elevs", len(kept) == 14, f"n={len(kept)}")
    check("dedup elevs strictly increasing",
          all(df.elev[kept[i]] < df.elev[kept[i+1]] for i in range(len(kept)-1)))
    check("dedup prefers surveillance", all(df.kind[k] in ("surv","batch") for k in kept),
          str([df.kind[k] for k in kept]))
    cls = K.classify_scan(r.fixed_angle["data"], r.metadata.get("vcp_pattern"))
    check("classify from Py-ART radar", cls["mode"] == "none" and cls["unique_elevs"] == 14, str(cls["mode"]))
else:
    print("  SKIP  no local volumes")

print("\n### 4. ARCO")
root = K.arco_open("KLOT")
inv = K.arco_vcps(root)
check("arco_vcps finds 12 VCPs", len(inv) == 12, f"n={len(inv)}")
check("VCP-35 busiest or near", inv.n_scans.iloc[0] > 200_000, f"top={inv.group.iloc[0]}:{inv.n_scans.iloc[0]}")
check("avset_enabled attr present on modern VCP",
      str(inv.set_index("group").loc["VCP-212","avset_enabled"]) == "True",
      str(inv.set_index("group").loc["VCP-212","avset_enabled"]))
print(inv[["group","vcp","n_sweeps","n_scans","avset_enabled","num_base_tilts","time_domain"]].to_string(index=False))

t = K.arco_times(root, "VCP-212")
check("arco_times monotonic", bool(np.all(np.diff(t) > np.timedelta64(0))))
check("arco_times spans 2015->2026", str(t[0])[:4] == "2015" and str(t[-1])[:4] == "2026",
      f"{str(t[0])[:19]} -> {str(t[-1])[:19]}")
i, ta = K.arco_nearest(root, "VCP-212", "2026-07-27T17:00:00")
check("arco_nearest within 5 min", abs((ta - np.datetime64("2026-07-27T17:00:00")) /
      np.timedelta64(1, "s")) < 300, f"idx={i} t={ta}")

ds = K.arco_sweep(root, "VCP-212", i, sweep=0)
check("arco_sweep has DBZH", "DBZH" in ds)
check("arco_sweep georeferenced", {"x","y","z"} <= set(ds.coords))
dbz = ds.DBZH.values
check("-999 masked out", np.nanmin(dbz) > -100, f"min={np.nanmin(dbz):.1f} max={np.nanmax(dbz):.1f}")
check("some valid gates", np.isfinite(dbz).mean() > 0.05, f"valid={np.isfinite(dbz).mean():.3f}")
print(f"   scan {ta}: DBZH {np.nanmin(dbz):.1f}..{np.nanmax(dbz):.1f} dBZ, "
      f"valid {np.isfinite(dbz).mean()*100:.1f}%, fixed_angle={ds.attrs['sweep_fixed_angle']}")

els = K.arco_scan_elevations(root, "VCP-212", i)
fin = [e["fixed_angle"] for e in els if e["recorded"]]
check("scan_elevations recorded subset", 0 < len(fin) <= len(els), f"{len(fin)}/{len(els)}")
print("   recorded elevs:", fin)
print("   classify:", K.classify_scan(fin, 212)["mode"],
      "avset:", K.classify_scan(fin, 212)["avset_active"])

print("\n### 4b. ARCO volume reassembly (SAILS fragmentation)")
# tornado window: SAILS active -> one volume spans 3 indices
vi = K.arco_volume_indices(root, "VCP-212", i)
allel = []
for k in vi:
    allel += [e["fixed_angle"] for e in K.arco_scan_elevations(root, "VCP-212", k)
              if e["recorded"] and e["fixed_angle"] is not None]
uniq = sorted(set(allel))
check("SAILS volume spans >1 index", len(vi) > 1, f"indices={vi}")
check("reassembled volume reaches 19.51", max(uniq) > 19.0, f"top={max(uniq)}")
check("reassembled covers 14 unique elevs", len(uniq) == 14, f"n={len(uniq)} {uniq}")
print(f"   idx {i} -> volume indices {vi}; elevs {uniq}")
# quiet window: single index is already whole
iq, tq = K.arco_nearest(root, "VCP-212", "2026-08-23T01:15:00")
vq = K.arco_volume_indices(root, "VCP-212", iq)
check("quiet-period volume is one index", len(vq) == 1, f"indices={vq}")

print("\n### 5. ARCO lowsweeps")
lroot = K.arco_open("KLOT", lowsweeps=True)
linv = K.arco_vcps(lroot)
check("lowsweeps has sweep_0/sweep_1", set(linv.group) == {"sweep_0","sweep_1"}, str(list(linv.group)))
lt = K.arco_times(lroot, "sweep_0")
check("lowsweeps time epoch correct (2015->2026)",
      str(lt[0])[:4] == "2015" and str(lt[-1])[:4] == "2026", f"{str(lt[0])[:19]} -> {str(lt[-1])[:19]}")
check("lowsweeps ~1M scans", lt.size > 900_000, f"n={lt.size}")
j, tj = K.arco_nearest(lroot, "sweep_0", "2026-07-27T17:00:00")
check("lowsweeps nearest within 5 min",
      abs((tj - np.datetime64("2026-07-27T17:00:00")) / np.timedelta64(1, "s")) < 300, f"idx={j} t={tj}")
lds = K.arco_sweep(lroot, "sweep_0", j)
check("lowsweeps sweep loads + masked", np.nanmin(lds.DBZH.values) > -100,
      f"min={np.nanmin(lds.DBZH.values):.1f} max={np.nanmax(lds.DBZH.values):.1f}")

print("\n=== " + (f"{len(fails)} FAILURES: {fails}" if fails else "ALL CHECKS PASSED"))
