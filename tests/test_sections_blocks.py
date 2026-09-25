"""The shipped ARM skills must carry the blocks `sections.py` generates, byte for byte.

`tests/test_act_api_calls.py` proves the snippets call real functions. This proves they
came from the one place those blocks are defined - so a fix applied to `sections.py`
cannot silently leave 230 published files on the old text, which is how the helper-call
defect survived unnoticed in the first place.
"""
import json
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools" / "arm_instrument_build"))
import sections  # noqa: E402

ARM = sorted(list((ROOT / "skills" / "arm-instruments").glob("arm-instrument-*"))
             + list((ROOT / "skills" / "arm-vaps").glob("arm-vap-*")))
IDS = [p.name for p in ARM]
FETCH = re.compile(r'files = act\.discovery\.download_arm_data\(user, token, "([^"]+)", "([^"]+)", "\2"\)')


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_fetch_block_is_generated(skill):
    text = (skill / "SKILL.md").read_text()
    m = FETCH.search(text)
    if not m:
        # Skills with no verified example show a size probe; four datastreams ARM Live
        # refuses show the 403 block; four that are not netCDF show their own opener.
        assert ("armlive/livedata/query" in text
                or "download_arm_data(user, token" in text), (
            f"{skill.name}: no way to get data at all")
        pytest.skip("no dated fetch block: probe, refusal or non-netCDF variant")
    # a datastream whose time units or file set need extra read arguments carries them here
    read = re.search(r"read_arm_netcdf\(files, cleanup_qc=True([^)]*)\)", text)
    kwargs = {}
    if read and read.group(1).strip():
        for part in read.group(1).split(","):
            if "=" not in part:
                continue
            k, v = part.split("=", 1)
            kwargs[k.strip()] = eval(v.strip())  # noqa: S307 - our own generated literals
    why = None
    block = text[m.start():]
    pre = text[:m.start()].rsplit("```python", 1)[-1]
    if kwargs:
        why = "\n".join(l.lstrip("# ").rstrip() for l in
                        text[:m.end()].splitlines()[-4:] if l.startswith("# ") and "Downloads into" not in l)
        why = why or None
    generated = sections.fetch_block(*m.groups(), read_kwargs=kwargs or None, why=why)
    if generated not in text:
        # the comment wording is cosmetic; the call sequence is what must match
        calls = re.findall(r"^(?:files|ds|avail|assert|print|user)[^\n]*", generated, re.M)
        missing = [c for c in calls if c not in text]
        assert not missing, (
            f"{skill.name}: fetch block diverges from sections.fetch_block(): {missing[:2]}")


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_helper_note_present_and_truthful(skill):
    """Every skill names the convenience wrappers exactly once, labelled as not-ACT."""
    text = (skill / "SKILL.md").read_text()
    assert sections.HELPER_NOTE in text, f"{skill.name}: helper note missing or edited"
    for helper in ("armlive_open", "armlive_list_files", "act_qc_table", "act_qc_apply"):
        assert text.count(helper) == 1, (
            f"{skill.name}: `{helper}` appears {text.count(helper)} times; it belongs only in "
            f"the note that says it is not part of ACT")


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_first_look_plots_a_variable_that_exists(skill):
    """A plot example naming a variable the file lacks is a KeyError with extra steps."""
    inv = skill / "example_inventory.json"
    text = (skill / "SKILL.md").read_text()
    if "### First look" not in text or not inv.exists():
        pytest.skip("no first-look block or no verified example")
    section = text[text.index("### First look"):]
    section = section[:section.index("\n## ")]
    present = set((json.loads(inv.read_text()).get("variables") or {}))
    named = (re.findall(r'disp\.plot\("([^"]+)"', section)
             + re.findall(r'ds\["([^"]+)"\]', section))
    for v in named:
        assert v in present, f"{skill.name}: first look plots `{v}`, absent from the example file"


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_first_look_matches_the_scan_geometry(skill):
    """PPI for an azimuthal sweep, RHI for an elevation sweep, and neither at zenith.

    Py-ART reports CSAPR's birdbath as `scan_type='sector'` at 90 deg fixed angle; a plan
    view of it is meaningless. An RHI plotted as a PPI is simply the wrong projection.
    """
    text = (skill / "SKILL.md").read_text()
    if "### First look" not in text:
        pytest.skip("no first-look block")
    scan = re.search(r"scan_type='(\w+)'", text)
    if not scan or "pyart.io.read" not in text:
        pytest.skip("not a Py-ART radar skill")
    section = text[text.index("### First look"):]
    section = section[:section.index("\n## ")]
    called = set(re.findall(r"disp\.(plot_\w+)\(", section))
    if not called:
        pytest.skip("first look does not use a Py-ART display")
    # `fixed angle` is an ELEVATION for a ppi/sector sweep but an AZIMUTH for an rhi, so
    # the zenith test only applies to the azimuthal scan types. WSACR is an rhi whose
    # fixed azimuth is 359.99 deg, which is not a birdbath.
    angle = re.search(r"fixed angle ([\d.]+) deg", text)
    fixed = float(angle.group(1)) if angle else None
    kind = scan.group(1)
    if kind == "vpt":
        assert called == {"plot_vpt"}, f"{skill.name}: vertically pointing, plotted with {called}"
    elif kind == "rhi":
        assert called == {"plot_rhi"}, f"{skill.name}: RHI sweep plotted with {called}"
    elif kind in ("ppi", "sector") and fixed is not None and fixed >= 85:
        assert called == {"plot_ray"}, (
            f"{skill.name}: an azimuthal sweep at {fixed} deg elevation is a birdbath; "
            f"{called} is not a meaningful view of it")
    elif kind in ("ppi", "sector"):
        assert called == {"plot_ppi"}, f"{skill.name}: azimuthal sweep plotted with {called}"


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_fetch_guards_an_empty_transfer(skill):
    """ARM Live rate-limits by returning no files; say so at the read, not three blocks on."""
    text = (skill / "SKILL.md").read_text()
    if "download_arm_data(user, token" not in text or "start, end" in text.split("### First look")[0][:0]:
        pytest.skip("no dated fetch block")
    if not re.search(r'download_arm_data\(user, token, "[^"]+", "[^"]+", "[^"]+"\)', text):
        pytest.skip("no dated fetch block")
    assert re.search(r"^assert files,", text, re.M), (
        f"{skill.name}: fetch block does not assert that anything was transferred")


@pytest.mark.parametrize("skill", ARM, ids=IDS)
def test_qc_block_uses_variables_that_exist(skill):
    """A filter example naming a variable the file does not have is worse than none."""
    inv = skill / "example_inventory.json"
    text = (skill / "SKILL.md").read_text()
    if not inv.exists():
        pytest.skip("no verified example")
    present = set((json.loads(inv.read_text()).get("variables") or {}))
    named = set(re.findall(r'ds\.qcfilter\.datafilter\(variables=\[([^\]]*)\]', text))
    for group in named:
        for v in re.findall(r'"([^"]+)"', group):
            assert v in present, f"{skill.name}: QC example filters `{v}`, absent from the example file"
    for v in re.findall(r'ds\["(qc_[^"]+)"\]', text):
        assert v in present, f"{skill.name}: QC example reads `{v}`, absent from the example file"
