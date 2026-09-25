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


def fetch_block(datastream, day, read_kwargs=None, why=None):
    """Size, download, read, cite - the one block every skill opens with.

    `read_kwargs` carries what THIS datastream needs beyond the default, with `why`
    printed above it as a comment. Executing these blocks against all 230 datastreams
    turned up three cases that the plain call cannot open at all: time units ACT's CF
    decoder rejects (`use_base_time=True`), and a day whose files will not concatenate on
    a shared index (`combine="nested", concat_dim="time"`). A skill that shipped a read
    call which fails on its own datastream is the same defect as one that calls a
    function that does not exist.

    The assert is on `files`, not on the dataset. Under a rate limit `download_arm_data`
    prints `Unable to download file:` and returns an empty list; `read_arm_netcdf([])`
    then raises `OSError: no files to open`, which says nothing about why. Asserting on
    the list first turns that into the actionable message while the raise is still ahead
    of it. (`read_arm_netcdf` does have return-None paths - `return_None=True` - but that
    is not the default, so a None dataset is not the failure mode to guard here.)
    """
    extra = ""
    if read_kwargs:
        kw = ", ".join(f"{k}={v!r}" for k, v in read_kwargs.items())
        extra = (f"# {why}\n" if why else "") + f"# {kw}\n"
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
        + 'assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"\n'
        + (("\n" + "\n".join(f"# {ln}" for ln in (why or "").splitlines()) + "\n") if why else "")
        + "ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True"
        + ("".join(f", {k}={v!r}" for k, v in (read_kwargs or {}).items()))
        + ")\n"
        f'print(act.discovery.get_arm_doi("{datastream}", "{day}", "{day}"))   # cite what you pulled\n'
        "```"
    )


def refused_datastream_block(datastream, status, reason):
    """ARM Live refuses some datastreams outright; say so instead of showing a download.

    Observed by executing the fetch block for every skill: four datastreams answer HTTP
    403 to the query endpoint on every date tried, so no download example can work.
    """
    return (
        "```python\n"
        "import os, requests\n"
        "\n"
        f"# ARM Live answers HTTP {status} for this datastream on every date tried\n"
        f"# ({reason}). The query below documents that rather than pretending otherwise;\n"
        "# order the data from Data Discovery at <https://adc.arm.gov/discovery/> instead.\n"
        f'r = requests.get("{QUERY_URL}",\n'
        '                 params={"user": f\'{os.environ["ARMUSER"]}:{os.environ["ARMTOKEN"]}\',\n'
        f'                         "ds": "{datastream}", "start": start, "end": end,\n'
        '                         "wt": "json"})\n'
        f'print(r.status_code)   # {status}\n'
        "```"
    )


def non_netcdf_block(datastream, container, opener):
    """Some ARM datastreams are not netCDF at all; `read_arm_netcdf` cannot open them.

    Found by execution: xarray reported no matching backend for these, and the file's
    magic bytes identify what it actually is.
    """
    return (
        "```python\n"
        "import os, requests, act\n"
        "\n"
        'user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]\n'
        f'files = act.discovery.download_arm_data(user, token, "{datastream}", start, end)\n'
        "\n"
        f"# These files are {container}, not netCDF - `read_arm_netcdf` fails with\n"
        "# \"did not find a match in any of xarray's currently installed IO backends\".\n"
        f"{opener}\n"
        "```"
    )


def keep_variables_block(datastream, keep, read_kwargs=None):
    """For wide datastreams: pull only the columns you need, plus their QC companions.

    Pass the same variables the QC block goes on to filter. This block rebinds `ds`, so a
    reader working down the page hits a KeyError if the narrowed dataset does not contain
    what the next block reaches for - which is what it did for `ecor` until executing the
    blocks in order caught it.
    """
    kw = dict(read_kwargs or {})
    note = ""
    if kw.get("use_base_time"):
        note = ("# base_time and time_offset stay in the keep list because use_base_time reads\n"
                "# them - drop them and the read fails with KeyError: 'base_time'.\n")
    extra = "".join(f", {k}={v!r}" for k, v in kw.items())
    return (
        "```python\n"
        f'files = act.discovery.download_arm_data(user, token, "{datastream}", start, end)\n'
        + note +
        f"ds = act.io.arm.read_arm_netcdf(files, keep_variables={json.dumps(list(keep))},\n"
        f"                                cleanup_qc=True{extra})\n"
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
    """Inspect what QC would remove, then remove it. Both assessment vocabularies.

    `primary` must be a data variable, never a coordinate. `qc_time` exists in some ARM
    files, so a naive "variables that have a qc_ companion" scan picks `time` - and
    `datafilter` on a dimension coordinate raises "Cannot assign to the .values attribute
    of dimension coordinate". Executing these blocks caught it in `aeri`.

    `flag_meanings` is read with `.get`: cleanup does not always produce it, and a skill
    should not crash a reader's session over a missing attribute (caught in `diffcor`).
    """
    return (
        "```python\n"
        "# What each test would remove, one variable at a time\n"
        f'print(ds["qc_{primary}"].attrs.get("flag_meanings", "no flag_meanings"))\n'
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


def state_flag_qc_block(primary):
    """Some products encode QC as a state flag, not a bitmask - `datafilter` cannot use it.

    Found by execution, in `sphotcod`: its one QC companion is `qc_modis_white_sky_albedo`
    (there is no `qc_cloud_optical_depth` in the file at all - an earlier version of this
    docstring named that variable, which the run disproved). It carries `flag_values`
    "0, 1, 2, 3, 255" and `flag_assessments`
    ['Acceptable', 'Acceptable', 'Acceptable', 'Acceptable', 'Bad'], with `flag_masks`
    None. ACT's `qcfilter.datafilter` indexes flag_masks unconditionally and raises
    `TypeError: 'NoneType' object is not subscriptable`; `get_masked_data` handles the
    same variable correctly, so screen with that.
    """
    return (
        "```python\n"
        f'# `qc_{primary}` is a state flag - flag_values with flag_assessments, no flag_masks.\n'
        "# ACT's datafilter assumes a bitmask and raises TypeError on this encoding, so the\n"
        "# mask path is the one to use here.\n"
        f'print(ds["qc_{primary}"].attrs.get("flag_values"),\n'
        f'      ds["qc_{primary}"].attrs.get("flag_assessments"))\n'
        f'mask = ds.qcfilter.get_masked_data("{primary}", rm_assessments=["Bad", "Incorrect"],\n'
        "                                  return_mask_only=True)\n"
        'print(int(mask.sum()), "of", mask.size, "points flagged")\n'
        f'clean = ds["{primary}"].where(~mask)\n'
        "```"
    )


def dqr_block(datastream, start_date, end_date):
    """DQRs carry the mentor's knowledge; no automated test substitutes for them.

    `print_dqr` raises `ValueError("Check parameters - No DQRs found")` when nothing
    matches the window, rather than printing nothing - found by executing this block
    against every ARM skill's own datastream, where most clean windows raised. The
    try/except is in the emitted snippet so the example runs as written.
    """
    return (
        "```python\n"
        "try:\n"
        f'    act.qc.print_dqr("{datastream}", "{start_date}", "{end_date}")\n'
        "except ValueError:\n"
        "    print(\"no DQRs for this window\")   # ACT raises rather than returning empty\n"
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


def first_look_block(kind, primary, qc=False, field=None, sweep_var=None):
    """A plot that suits the shape of the data, not a generic one.

    No figure is committed to the repo: an image in a SKILL.md is invisible to an agent
    reading the skill, goes stale with the datastream, and would add tens of megabytes
    across the library. What a reader actually lacks is which display class fits - a 1-D
    time series, a profiler's time-height field, a scanning radar's PPI, a sonde's
    thermodynamic profile are four different calls - and which variable names exist.

    `assessment_overplot=True` draws the QC-flagged points over the series in red and
    orange, so the first look and the QC section answer the same question at once. It
    needs a `qc_` companion for the field, so it is only passed where one exists.

    Every variant is executed against the skill's own verified example file before it
    ships; `tools/arm_instrument_build/snippet_runner.py` is the harness.
    """
    if kind == "skewt":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "disp = act.plotting.SkewTDisplay(ds, figsize=(8, 8))\n"
            f'disp.plot_from_spd_and_dir("{primary["spd"]}", "{primary["dir"]}",\n'
            f'                           "{primary["p"]}", "{primary["t"]}", "{primary["td"]}")\n'
            'disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "ppi":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "disp = pyart.graph.RadarDisplay(radar)\n"
            "fig, ax = plt.subplots(figsize=(6.5, 5.5))\n"
            f'disp.plot_ppi("{field}", sweep=0, ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "rhi":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# A fixed-azimuth elevation sweep: range-height, not a plan view.\n"
            "disp = pyart.graph.RadarDisplay(radar)\n"
            "fig, ax = plt.subplots(figsize=(8, 4))\n"
            f'disp.plot_rhi("{field}", sweep=0, ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "birdbath":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# An azimuth sweep at 90 deg elevation (a birdbath scan, used for ZDR\n"
            "# calibration). Every ray points at zenith, so a plan view is meaningless -\n"
            "# one ray is a vertical profile, and the spread across rays is the signal.\n"
            "disp = pyart.graph.RadarDisplay(radar)\n"
            "fig, ax = plt.subplots(figsize=(6, 4))\n"
            f'disp.plot_ray("{field}", 0, ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "vpt":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# Vertically pointing: one sweep, so the time-height view is the useful one.\n"
            "disp = pyart.graph.RadarDisplay(radar)\n"
            "fig, ax = plt.subplots(figsize=(11, 4))\n"
            f'disp.plot_vpt("{field}", ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "slice":
        var, dims = primary
        keep2 = [d for d in dims if d == "time"][:1] + [d for d in dims if d != "time"][:1]
        fix = {d: 0 for d in dims if d not in keep2}
        sel = ", ".join(f"{d}=0" for d in fix)
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            f"# This field is {len(dims)}-D {tuple(dims)}, so a first look has to fix an axis.\n"
            "fig, ax = plt.subplots(figsize=(8, 4))\n"
            f'ds["{var}"].isel({sel}).plot(ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "profile":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# A skew-T is the conventional view, but ACT's SkewTDisplay goes through MetPy,\n"
            "# which raises InvalidSoundingError when the profile contains any pressure\n"
            "# reversal - and raw ARM soundings routinely do. Filter to monotonic pressure\n"
            "# first if you want the skew-T; this plain profile always runs.\n"
            "fig, ax = plt.subplots(figsize=(4.5, 6))\n"
            f'ax.plot(ds["{primary["t"]}"], ds["{primary["p"]}"], label="{primary["t"]}")\n'
            f'ax.plot(ds["{primary["td"]}"], ds["{primary["p"]}"], label="{primary["td"]}")\n'
            'ax.invert_yaxis()\n'
            f'ax.set_xlabel("degC"); ax.set_ylabel("{primary["p"]}"); ax.legend()\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "sparse":
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# Discrete samples, not a continuous record - a line plot of one or a few points\n"
            "# is meaningless (and ACT's TimeSeriesDisplay raises IndexError on a length-1\n"
            "# series), so plot the samples as markers.\n"
            "fig, ax = plt.subplots(figsize=(9, 3.5))\n"
            f'ax.plot(ds["time"], ds["{primary}"], marker="o", linestyle="none")\n'
            f'ax.set_ylabel("{primary}")\n'
            'fig.autofmt_xdate()\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "lines":
        var, other = primary
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            f"# `{var}` carries a few values per time step along `{other}`, so one line each\n"
            "# reads better than a pcolormesh with no meaningful vertical coordinate.\n"
            "fig, ax = plt.subplots(figsize=(10, 4))\n"
            f'ds["{var}"].plot.line(x="time", ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    if kind == "xr2d":
        var, isel = primary
        sel = f'.isel({isel})' if isel else ""
        return (
            "```python\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "# Plotted through xarray rather than ACT: this field is not time-major, or its\n"
            "# second dimension has a non-numeric coordinate, either of which sends ACT's\n"
            "# 2-D path into a dtype error.\n"
            "fig, ax = plt.subplots(figsize=(10, 4))\n"
            f'ds["{var}"]{sel}.plot(x="time", ax=ax)\n'
            'fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
            "```"
        )
    overplot = ", assessment_overplot=True" if qc else ""
    trailer = ("   # QC-flagged points in red/orange\n" if qc else "\n")
    return (
        "```python\n"
        "import matplotlib.pyplot as plt\n"
        "\n"
        "# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry\n"
        "# one, which otherwise sends a 1-D series through the 2-D plotting path.\n"
        f"disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, {4 if kind == 'timeseries' else 4.5}))\n"
        f'disp.plot("{primary}"{overplot})' + trailer +
        'disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")\n'
        "```"
    )


RATE_LIMIT_NOTE = (
    "If `download_arm_data` prints `Unable to download file:` and returns an empty list,\n"
    "ARM Live is rate limiting (HTTP 429) rather than missing the data - the size probe\n"
    "above will still answer. Back off and retry; a0-level raw datastreams also return\n"
    "files that `read_arm_netcdf` cannot decode, so prefer b1 where one exists.\n"
)
