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
    if not m:  # the handful with no verified example show a size probe instead
        assert "armlive/livedata/query" in text, f"{skill.name}: no way to get data at all"
        pytest.skip("no-example skill: size probe only")
    assert sections.fetch_block(*m.groups()) in text, (
        f"{skill.name}: fetch block differs from sections.fetch_block() - regenerate it")


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
