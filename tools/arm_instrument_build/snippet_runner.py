"""Execute the code blocks in each ARM skill's data and QC sections, as written.

Textual symbol resolution proves a name exists. It does not prove the block runs. This
runs them: real credentials, real ARM Live, real files, the skill's own datastream and
its own example day. A reader's `start`/`end` are supplied (the blocks are written for a
reader who has a window in mind); nothing else is substituted except the local path of a
file the block just downloaded.

Usage (needs ARMUSER / ARMTOKEN in the environment):

    python tools/arm_instrument_build/snippet_runner.py                  # every skill
    python tools/arm_instrument_build/snippet_runner.py arm-instrument-met arm-vap-qcrad
    SNIPPET_MAX_MB=400 python tools/arm_instrument_build/snippet_runner.py   # raise the cap

Writes `snippet_run.json` beside the repo and prints a one-line summary per skill. What it
found on the first full run, none of which textual symbol-resolution could have caught:
three datastreams whose time units ACT cannot decode without `use_base_time=True`, one
whose day of files needs `combine="nested"`, four that are not netCDF at all, two whose
only `qc_` companion is `qc_time` (so the QC example filtered a dimension coordinate and
raised), one missing `flag_meanings`, one placeholder date shipped as if it were real, and
four datastreams ARM Live answers 403 for on every date.
"""

import io, json, os, re, shutil, sys, tempfile, time, traceback, contextlib
from pathlib import Path

SECTIONS = ("## Getting the data", "## Quality control in this")
MAX_MB = float(os.environ.get("SNIPPET_MAX_MB", "120"))


def blocks_of(text):
    """The python blocks inside the two sections we fixed, in document order."""
    out, pos = [], 0
    for head in ("## Getting the data",):
        i = text.find(head)
        if i < 0:
            continue
        j = text.find("## Known artifacts", i)
        seg = text[i: j if j > 0 else len(text)]
        out += re.findall(r"```python\n(.*?)```", seg, re.S)
    return out


def probe(ds_name, day, user, token):
    import requests
    r = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f"{user}:{token}", "ds": ds_name,
                             "start": day, "end": day, "wt": "json"}, timeout=90)
    r.raise_for_status()
    j = r.json()
    return j.get("num_found"), float(j.get("total_size") or 0)


def run_skill(skill_dir, user, token):
    text = (skill_dir / "SKILL.md").read_text()
    rec = {"skill": skill_dir.name, "blocks": 0, "ran": 0, "errors": [], "skipped": None}
    m = re.search(r'download_arm_data\(user, token, "([^"]+)", "([^"]+)", "\2"\)', text)
    if not m:
        rec["skipped"] = "no fetch block (no verified example)"
        return rec
    ds_name, day = m.groups()
    rec["datastream"], rec["day"] = ds_name, day
    try:
        n, size = probe(ds_name, day, user, token)
    except Exception as e:
        rec["errors"].append(f"probe: {type(e).__name__}: {e}"[:200])
        return rec
    rec["num_found"], rec["mb"] = n, round(size / 1e6, 2)
    if not n:
        rec["skipped"] = "ARM Live reports 0 files for the example day"
        return rec
    if size / 1e6 > MAX_MB:
        rec["skipped"] = f"{rec['mb']} MB exceeds the {MAX_MB} MB cap"
        return rec

    work = tempfile.mkdtemp(prefix="snip_")
    cwd = os.getcwd()
    ns = {"__name__": "__main__", "start": day, "end": day}
    try:
        os.chdir(work)
        for b in blocks_of(text):
            rec["blocks"] += 1
            src = b
            # a reader who downloaded the file has it locally; point Py-ART at where it is
            fn = re.search(r'pyart\.(?:io|aux_io)\.\w+\("([^"]+)"', src)
            if fn:
                hits = [os.path.join(dp, f) for dp, _, fs in os.walk(work)
                        for f in fs if f == fn.group(1)]
                if not hits:
                    rec["errors"].append(f"block {rec['blocks']}: {fn.group(1)} not downloaded")
                    continue
                src = src.replace(f'"{fn.group(1)}"', f'"{hits[0]}"')
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(src, f"<{skill_dir.name}:block{rec['blocks']}>", "exec"), ns)
                rec["ran"] += 1
            except Exception as e:
                rec["errors"].append(f"block {rec['blocks']}: {type(e).__name__}: {e}"[:300])
    finally:
        os.chdir(cwd)
        shutil.rmtree(work, ignore_errors=True)
    return rec


def main(argv):
    root = Path(__file__).resolve().parent.parent.parent
    skills = sorted(list((root / "skills" / "arm-instruments").glob("arm-instrument-*"))
                    + list((root / "skills" / "arm-vaps").glob("arm-vap-*")))
    if argv:
        wanted = set(argv)
        skills = [s for s in skills if s.name in wanted]
        missing = wanted - {s.name for s in skills}
        if missing:
            sys.exit(f"no such skill: {', '.join(sorted(missing))}")
    try:
        user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]
    except KeyError:
        sys.exit("set ARMUSER and ARMTOKEN (register at https://adc.arm.gov/armlive/)")

    out, t0 = [], time.time()
    for s in skills:
        try:
            rec = run_skill(s, user, token)
        except Exception:
            rec = {"skill": s.name, "blocks": 0, "ran": 0, "skipped": None,
                   "errors": [traceback.format_exc(limit=1)[:300]]}
        out.append(rec)
        state = ("skip: " + rec["skipped"]) if rec["skipped"] else \
                (f"{rec['ran']}/{rec['blocks']} blocks" + (" FAIL" if rec["errors"] else ""))
        print(f"{rec['skill']:32s} {state}", flush=True)
        for e in rec["errors"]:
            print(f"    ! {e}", flush=True)
    (root / "snippet_run.json").write_text(json.dumps(out, indent=1))
    clean = sum(1 for r in out if r["blocks"] and r["ran"] == r["blocks"])
    blocks = sum(r["ran"] for r in out), sum(r["blocks"] for r in out)
    print(f"\n{clean}/{len(out)} skills clean, {blocks[0]}/{blocks[1]} blocks executed, "
          f"{time.time() - t0:.0f}s")
    return 1 if any(r["errors"] for r in out) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
