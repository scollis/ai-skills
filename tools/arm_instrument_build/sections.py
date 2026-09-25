"""The code blocks every ARM skill shows for fetching data and for QC.

Why this file exists
--------------------
The first cut of these sections opened with `import act` and then called `armlive_open`,
`armlive_list_files`, `act_qc_table` and `act_qc_apply`. Those four are helpers defined by
the `act-arm-live` and `act-qc` skills' kernel sidecars - they are **not** ACT functions.
A reader with a bare `act-atmos` install who copied a block got a NameError from what
looked like ACT's own API, in all 230 skills at once. A colleague found it.

So the blocks live here, once, and both composers emit them from this module. Only real
ACT, Py-ART and stdlib calls go in. The convenience wrappers are named in prose, in one
labelled paragraph (`helper_note`), so a reader who has those skills loaded still learns
the short form - but nothing in a code block depends on them.

Provenance: every call emitted here was **invoked** against ACT 2.3.4 before this file was
written, not merely looked up.

| call | executed against |
|---|---|
| `act.io.arm.read_arm_netcdf` (plain, `cleanup_qc=True`, `keep_variables=`) | bundled `sample_files.EXAMPLE_MET1`, 289 KB, no network |
| `ds.qcfilter.get_masked_data` (`return_nan_array`, `return_mask_only`) | same file |
| `ds.qcfilter.datafilter`, `get_qc_test_mask`, `add_greater_test` | same file |
| `ds.clean.cleanup`, `ds.qcfilter.create_qc_summary` | same file |
| `act.qc.print_dqr` | `sgp30ecorE14.b1` 2015-2019; returned two real DQRs (D151209.1, D170217.3) |
| `act.qc.arm.add_dqr_to_qc` | bundled `sample_files.EXAMPLE_ECORSF_E39` |
| `act.discovery.get_arm_doi` | `nsametC1.b1`, live |
| `act.discovery.download_arm_data` | `nsametC1.b1` 2026-09-22, live: 383 KB transferred, then read, masked, filtered and re-read with `keep_variables` in one pass - the whole block below, start to finish |

An earlier attempt at that same transfer returned HTTP 429. That is ARM Live throttling a
client that has been busy, not a broken call, and it is why `RATE_LIMIT_NOTE` exists.

ACT has no list-only call, which is why the ARM Live query endpoint is used directly for
the size probe: knowing the byte count before a transfer matters on a metered link.

`tests/test_act_api_calls.py` holds the line - it re-resolves every symbol these blocks
emit against the installed ACT, and fails if any skill's snippet calls a kernel helper.
`tests/test_sections_blocks.py` asserts the shipped skills carry exactly these blocks.
"""

import json

QUERY_URL = "https://adc.arm.gov/armlive/livedata/query"

HELPER_NOTE = (
    "The `act-arm-live` and `act-qc` skills wrap these calls in shorter helpers\n"
    "(`armlive_open`, `armlive_list_files`, `act_qc_table`, `act_qc_apply`). Those are helpers\n"
    "those skills define, **not** ACT functions - nothing below uses them, so every block here\n"
    "runs against a bare `act-atmos` install.\n"
)


def fetch_block(datastream, day):
    """Size, download, read, cite - the one block every skill opens with."""
    return (
        "```python\n"
        "import os, requests, act\n"
        "\n"
        'user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]\n'
        "\n"
        "# ACT has no list-only call, so size the request against ARM Live's query endpoint\n"
        "# before transferring anything.\n"
        f'avail = requests.get("{QUERY_URL}",\n'
        '                     params={"user": f"{user}:{token}", "ds": "%s",\n' % datastream
        + f'                             "start": "{day}", "end": "{day}", "wt": "json"}}).json()\n'
        'print(avail["num_found"], avail["total_size"])            # files, bytes\n'
        "\n"
        f"# Downloads into ./{datastream}/ unless you pass output=\n"
        f'files = act.discovery.download_arm_data(user, token, "{datastream}", "{day}", "{day}")\n'
        "ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)\n"
        f'print(act.discovery.get_arm_doi("{datastream}", "{day}", "{day}"))   # cite what you pulled\n'
        "```"
    )


def keep_variables_block(datastream, keep):
    """For wide datastreams: pull only the columns you need, plus their QC companions."""
    return (
        "```python\n"
        f'files = act.discovery.download_arm_data(user, token, "{datastream}", start, end)\n'
        f"ds = act.io.arm.read_arm_netcdf(files, keep_variables={json.dumps(list(keep))},\n"
        "                                cleanup_qc=True)\n"
        "```"
    )


def size_probe_block(datastream):
    """Used where no file was ever opened: show how to look before leaping."""
    return (
        "```python\n"
        "import os, requests\n"
        "\n"
        f'avail = requests.get("{QUERY_URL}",\n'
        '                     params={"user": f\'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}\',\n'
        f'                             "ds": "{datastream}", "start": start, "end": end,\n'
        '                             "wt": "json"}).json()\n'
        'print(avail["num_found"], avail["total_size"])\n'
        "```"
    )


def qc_filter_block(primary, variables):
    """Inspect what QC would remove, then remove it. Both assessment vocabularies."""
    return (
        "```python\n"
        "# What each test would remove, one variable at a time\n"
        f'print(ds["qc_{primary}"].attrs["flag_meanings"])\n'
        f'mask = ds.qcfilter.get_masked_data("{primary}", rm_assessments=["Bad", "Indeterminate"],\n'
        "                                  return_mask_only=True)\n"
        'print(int(mask.sum()), "of", mask.size, "points flagged")\n'
        "\n"
        "# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use\n"
        "# Incorrect/Suspect - pass every name you might meet.\n"
        f"ds.qcfilter.datafilter(variables={json.dumps(list(variables))},\n"
        '                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],\n'
        "                       del_qc_var=False)\n"
        "```"
    )


def single_qc_variable_block(qc_variable):
    """Some products carry one bare QC variable instead of `qc_<name>` companions."""
    return (
        "```python\n"
        f"# This file carries one QC variable, `{qc_variable}`, not a per-variable `qc_<name>`\n"
        "# companion - so the qcfilter methods that key off that naming have nothing to\n"
        "# match. Read it directly and work out the encoding from its own attributes.\n"
        f'print(ds["{qc_variable}"].attrs)\n'
        f'print(ds["{qc_variable}"].to_series().value_counts().head())\n'
        "```"
    )


def dqr_block(datastream, start_date, end_date):
    """DQRs carry the mentor's knowledge; no automated test substitutes for them."""
    return (
        "```python\n"
        f'act.qc.print_dqr("{datastream}", "{start_date}", "{end_date}")\n'
        "```"
    )


def dqr_to_qc_block(primary):
    """Fold DQRs into the QC variables themselves, so one filter call covers both."""
    return (
        "```python\n"
        "# Adds DQR assessments to the qc_ variables, then filter once for both sources.\n"
        f'ds = act.qc.arm.add_dqr_to_qc(ds, variable="{primary}")\n'
        f'ds.qcfilter.datafilter(variables=["{primary}"],\n'
        '                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"])\n'
        "```"
    )


RATE_LIMIT_NOTE = (
    "If `download_arm_data` prints `Unable to download file:` and returns an empty list,\n"
    "ARM Live is rate limiting (HTTP 429) rather than missing the data - the size probe\n"
    "above will still answer. Back off and retry; a0-level raw datastreams also return\n"
    "files that `read_arm_netcdf` cannot decode, so prefer b1 where one exists.\n"
)
