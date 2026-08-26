"""Sync skills between this repository and a Claude Science skill registry.

The repository is the reviewable source of truth; the registry is where skills
are loaded and used. Keeping both without a sync step is how they diverge, so
this script moves them in either direction and reports a diff first.

Run from a Claude Science `repl` cell, where the `host` object is injected:

    exec(open("tools/sync_skills.py").read())
    status()                      # what differs, in both directions
    pull()                        # registry -> repo (then review the git diff)
    push(["nexrad-aws-2025"])     # repo -> registry, explicit names only

`push()` requires explicit skill names: publishing overwrites what an agent
loads in every future session, so it should never be a bulk default.
"""

import difflib
import json
import pathlib

SKILLS_DIR = pathlib.Path(__file__).resolve().parent.parent / "skills"


def repo_skills():
    """Skill directories present in the repository, with their file contents."""
    out = {}
    for d in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        files = {f.name: f.read_text() for f in sorted(d.iterdir())
                 if f.is_file() and not f.name.startswith(".")}
        if "SKILL.md" in files:
            out[d.name] = files
    return out


def registry_skills(host, names=None):
    """Skill contents as the registry currently holds them."""
    listed = {r["name"]: dict(r) for r in (dict(x) for x in host.skills.list())}
    out = {}
    for name in (names or listed):
        if name not in listed:
            continue
        doc = host.skills.read(name)
        files = {}
        for f in (doc.get("files") or ["SKILL.md"]):
            files[f] = (doc["content"] if f == "SKILL.md"
                        else host.skills.read(name, f)["content"])
        out[name] = files
    return out


def diff_one(a, b, name, path):
    """Unified diff between two versions of one file, or '' when identical."""
    if a == b:
        return ""
    return "".join(difflib.unified_diff(
        a.splitlines(keepends=True), b.splitlines(keepends=True),
        fromfile=f"registry/{name}/{path}", tofile=f"repo/{name}/{path}"))


def status(host=None, names=None, show_diff=False):
    """Report what differs between repo and registry. Changes nothing."""
    host = host or globals().get("host")
    repo = repo_skills()
    reg = registry_skills(host, names or list(repo))
    report = {"only_in_repo": [], "only_in_registry": [], "differs": {},
              "identical": []}
    for name in sorted(set(repo) | set(reg)):
        if name not in reg:
            report["only_in_repo"].append(name)
            continue
        if name not in repo:
            report["only_in_registry"].append(name)
            continue
        changed = []
        for path in sorted(set(repo[name]) | set(reg[name])):
            a, b = reg[name].get(path, ""), repo[name].get(path, "")
            if a != b:
                changed.append(path)
                if show_diff:
                    print(diff_one(a, b, name, path))
        (report["differs"].setdefault(name, changed) if changed
         else report["identical"].append(name))
    for k in ("only_in_repo", "only_in_registry"):
        if report[k]:
            print(f"{k}: {report[k]}")
    if report["differs"]:
        for name, files in report["differs"].items():
            print(f"differs: {name} -> {files}")
    print(f"identical: {len(report['identical'])}/{len(set(repo) | set(reg))}")
    return report


def pull(host=None, names=None):
    """Registry -> repo. Writes files; review with `git diff` before committing."""
    host = host or globals().get("host")
    reg = registry_skills(host, names)
    written = []
    for name, files in reg.items():
        dest = SKILLS_DIR / name
        dest.mkdir(parents=True, exist_ok=True)
        for path, content in files.items():
            target = dest / path
            if not target.exists() or target.read_text() != content:
                target.write_text(content)
                written.append(f"{name}/{path}")
    print(f"pulled {len(reg)} skills, {len(written)} files changed")
    for w in written:
        print("  ", w)
    return written


def push(names, host=None, publish=True):
    """Repo -> registry, for the named skills only.

    Edits each file, then publishes. A kernel.py that fails the sidecar gate
    blocks its skill's publish -- the gate verdict is printed, and other named
    skills still proceed.
    """
    if isinstance(names, str):
        names = [names]
    if not names:
        raise ValueError("push() requires explicit skill names")
    host = host or globals().get("host")
    repo = repo_skills()
    results = {}
    for name in names:
        if name not in repo:
            results[name] = {"error": "not in repo"}
            continue
        gate_ok, edited = True, []
        for path, content in repo[name].items():
            try:
                current = host.skills.read(name, path)["content"]
            except Exception:
                current = None
            if current == content:
                continue
            res = (host.skills.edit(name, path, content, old_string=current)
                   if current is not None else host.skills.edit(name, path, content))
            edited.append(path)
            gate = res.get("sidecar_gate")
            if gate and not gate.get("ok"):
                gate_ok = False
                print(f"  {name}/{path}: sidecar gate REJECTED -- {gate.get('error')}")
        if edited and publish and gate_ok:
            results[name] = {"edited": edited,
                             "publish": host.skills.publish(name, overwrite=True)
                             .get("status")}
        else:
            results[name] = {"edited": edited,
                             "publish": "skipped" if edited else "unchanged"}
        print(f"{name}: {results[name]}")
    return results


def manifest():
    """Machine-readable index of what the repo ships."""
    rows = []
    for name, files in sorted(repo_skills().items()):
        head = files["SKILL.md"].split("---")
        desc = ""
        if len(head) > 2:
            for line in head[1].splitlines():
                if line.startswith("description:"):
                    desc = line.split(":", 1)[1].strip()
        rows.append({"name": name, "files": sorted(files),
                     "bytes": sum(len(v) for v in files.values()),
                     "description": desc})
    return rows


if __name__ == "__main__":
    print(json.dumps(manifest(), indent=1))
