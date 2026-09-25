"""Compose a per-instrument SKILL.md from handbook facts + verified example data.

Every claim written here comes from one of three checkable sources, and the file says
which: the handbook PDF (page-cited), ARM's data-source catalog, or the example netCDF
file that was actually opened. Nothing is written from general knowledge.
"""
import sections
import datetime as dt
import json
import re

RADAR_CODES = {"kazr", "kazrge", "kazrmd", "mmcr", "csapr", "csapr2", "xsapr", "xsacr",
               "kasacr", "wsacr", "sacr", "mwacr", "swacr", "rwp", "50rwp", "915rwp",
               "rwp915", "rwp50", "marinewb", "xprecipradar"}
LIDAR_CODES = {"dl", "hsrl", "mpl", "rl", "ceil", "blc", "vceil", "dlprof"}

SITE_NAMES = {"sgp": "Southern Great Plains, Oklahoma", "nsa": "North Slope of Alaska",
              "ena": "Eastern North Atlantic, Azores", "bnf": "Bankhead National Forest, Alabama",
              "twp": "Tropical Western Pacific", "awr": "West Antarctica (AWARE)",
              "mao": "Manacapuru, Brazil (GoAmazon)", "pvc": "Cape Cod (TCAP)",
              "mos": "MOSAiC (Polarstern)", "epc": "Eastern Pacific (EPCAPE)",
              "hou": "Houston, Texas (TRACER)", "guc": "Gunnison, Colorado (SAIL)",
              "osc": "Oliktok Point, Alaska", "cor": "Cordoba, Argentina (CACTI)",
              "anx": "Andenes, Norway (COMBLE)", "asi": "Ascension Island (LASIC)",
              "mag": "Magic (marine)", "pgh": "Pilot Grove (?)", "tmp": "temporary"}


def _clean(s, limit=None):
    if s is None:
        return ""
    s = re.sub(r"\s+", " ", str(s)).strip()
    s = s.replace("|", "/").replace("<", "less than ").replace(">", "greater than ")
    if limit and len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] + "..."
    return s


def _cite(page):
    try:
        p = int(page)
    except (TypeError, ValueError):
        return ""
    return f" (hb p. {p})" if p > 0 else ""


def _md_table(headers, rows):
    if not rows:
        return "_none recorded in the handbook._\n"
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(r) + " |")
    return "\n".join(out) + "\n"


def trim_description(val, limit=1000):
    """The registry caps `description` at 1024 characters and refuses the publish above it.
    Drop triggers from the end first, then reported quantities - both are lists whose tail
    is the least discriminating part."""
    if len(val) <= limit:
        return val
    head, sep, trig = val.rpartition("Triggers - ")
    trigs = [t.strip() for t in trig.rstrip(".").split(", ") if t.strip()]
    while trigs and len(head + sep + ", ".join(trigs) + ".") > limit:
        trigs.pop()
    out = head + sep + ", ".join(trigs) + "."
    if len(out) <= limit:
        return out
    m = re.search(r"reported quantities \(([^)]*)\)", out)
    if m:
        qs = [q.strip() for q in m.group(1).split(", ") if q.strip()]
        while qs and len(out) > limit:
            qs.pop()
            out = out[:m.start(1)] + ", ".join(qs) + out[m.end(1):]
            m = re.search(r"reported quantities \(([^)]*)\)", out)
    return out[:limit].rsplit(" ", 1)[0] + "."


def description(code, name, facts, cat, ex_ds, extra_triggers=(), verified=True):
    """Frontmatter description: what it is, what the skill carries, trigger words.
    No angle brackets - the skill registry reads the field as markup."""
    one = _clean(facts.get("one_line"), 230)
    def short(q):
        # trigger words must be short to route on: "ZDR (differential reflectivity)" -> "ZDR"
        t = _clean(q).split("(")[0].strip().rstrip(",;")
        return t if 1 < len(t) <= 34 else ""
    quantities = ", ".join(x for x in (short(q.get("quantity"))
                                       for q in (facts.get("measured_quantities") or [])[:8]) if x)
    trig = [code, name, ex_ds] + list(extra_triggers)
    trig += [short(q.get("quantity")) for q in (facts.get("measured_quantities") or [])[:6]]
    trig += [w for w in (cat or "").split("; ") if w]
    if facts.get("manufacturer_model"):
        trig += [p.strip() for p in re.split(r"[;,]", _clean(facts["manufacturer_model"]))[:2]]
    # acronyms only when they look like an instrument designation, not a site or a unit
    trig += [_clean(d["term"]) for d in (facts.get("definitions") or [])
             if d.get("term") and 3 < len(d["term"]) < 18
             and not re.fullmatch(r"(AMF\d?|AC|DOE|ARM|SGP|NSA|ENA|TWP|UTC|WMO|PI|VAP)", d["term"])][:4]
    trig = [t for t in dict.fromkeys(t for t in trig if t) if 1 < len(t) < 60]
    example_clause = (f"Includes a verified ARM Live example ({ex_ds}) and the variable inventory "
                      f"of a real file. " if verified else
                      "No data file could be verified for this instrument, and the skill says so in "
                      "place of a variable inventory. ")
    d = (f"ARM {name} ({code}) - handbook-derived instrument reference. Measurement principle, "
         f"reported quantities ({quantities}), specifications, calibration, embedded QC coverage, "
         f"and the known artifacts and failure modes documented by the instrument mentor. "
         + example_clause
         + f"Use when working with {code} data, interpreting its variables or QC flags, judging "
         f"whether an artifact is instrumental, or choosing a datastream for this measurement. "
         f"Category - {cat}. Triggers - " + ", ".join(trig) + ".")
    # ': ' in an unquoted YAML scalar makes the frontmatter a nested mapping and the
    # registry refuses to publish it. The repo's regex frontmatter parser does not
    # notice, so the guard belongs here, at the point the value is built.
    return trim_description(_clean(d).replace(": ", " - "))


def credit_block(facts, handbook_url, code):
    """Credit the handbook's authors - ARM instrument mentors - as the source of the
    instrument knowledge. A derived reference that does not name whose work it derives
    from is a bad citation, so this section is mandatory and a structure test checks it.
    """
    authors = [_clean(a) for a in (facts.get("authors") or []) if _clean(a)]
    title = _clean(facts.get("title")) or f"{code} Instrument Handbook"
    bits = [b for b in [_clean(facts.get("report_number")), _clean(facts.get("date"))] if b]
    tail = (", " + ", ".join(bits)) if bits else ""
    L = ["## Credit", ""]
    if authors:
        who = ", ".join(authors)
        L += [f"Everything this skill knows about the instrument is the work of **{who}** -",
              "the ARM instrument mentor(s) who wrote the handbook it derives from:",
              ""]
    else:
        L += ["The handbook this skill derives from names no individual author on its cover;",
              "it is issued by the ARM facility. The instrument knowledge in it is still the",
              "mentor programme's work, not this file's:",
              ""]
    L += [f"> {who if authors else 'ARM Climate Research Facility'}. *{title}*{tail}.",
          f"> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.",
          f"> {handbook_url}",
          "",
          "Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a",
          "navigational layer over their document plus a measurement of one data file; it",
          "replaces neither, and where it is thinner than the handbook the handbook is right.",
          ""]
    return L


def shared_handbook_note(code, siblings, override=None):
    """A handbook that covers several instrument classes describes a family or a system.
    Saying so is the difference between a reference and a misattribution."""
    if override:
        return ["> **Scope of this handbook.** For `" + code + "`, " + override + ".", ""]
    if not siblings:
        return []
    sib = ", ".join(f"`{s}`" for s in siblings)
    return ["> **Scope of this handbook.** The same document covers " + sib + " as well as",
            "> this instrument, so much of what follows is family- or system-level rather than",
            "> specific to `" + code + "`. Where a number has to be per-instrument - a frequency, a",
            "> detection limit, a serial number - check it against the handbook section for this",
            "> class before using it.", ""]


def no_example_block(code, cat_row, reason):
    """When no file could be opened, say exactly why. An unverified data section that
    looks verified is worse than an absent one."""
    return [
        "## The data",
        "",
        "**No example file was verified for this instrument.** " + reason + ".",
        "",
        f"ARM's catalog lists {cat_row.get('n_ds_with_data')} datastreams with data across "
        f"{cat_row.get('n_sites')} sites, so data exist - but nothing in this skill's data,",
        "variable or QC sections was measured, because nothing could be opened. Treat the",
        "handbook facts above as the only verified content here, and check the variable names",
        "yourself against a file before writing code against them:",
        "",
        sections.size_probe_block(cat_row.get("ex_datastream") or "<datastream>"),
        "",
    ]


def compose(code, facts, cat_row, inv, qc, example, handbook_url, n_pages,
            pyart_note=None, verified_on=None, siblings=(), scope_override=None,
            no_example_reason=None):
    name = cat_row["name"]
    verified_on = verified_on or dt.date.today().isoformat()
    example = example or {}
    ex_ds = example.get("datastream") or cat_row.get("ex_datastream") or ""
    is_radar = code in RADAR_CODES
    is_lidar = code in LIDAR_CODES

    L = []
    A = L.append
    A("---")
    A(f"name: arm-instrument-{code}")
    A("description: " + description(code, name, facts, cat_row.get("categories", ""), ex_ds,
                                     verified=not no_example_reason))
    A("---")
    A("")
    A(f"# {code.upper()} - {name}")
    A("")
    A(_clean(facts.get("one_line")) or name)
    A("")
    A("Every number below is traceable to one of three sources, marked inline: the instrument")
    if no_example_reason:
        A(f"handbook (`hb p. N`, {n_pages} pages) or ARM's data-source catalog. No data file could")
        A(f"be opened for this instrument - see **The data**. Compiled {verified_on}.")
    else:
        A(f"handbook (`hb p. N`, {n_pages} pages), ARM's data-source catalog, or the example file")
        A(f"listed under **The data** - opened, not assumed. Verified {verified_on}.")
    A("")

    # ---- identity table ----
    hb_bits = [x for x in [facts.get("report_number"), ", ".join(facts.get("authors") or []),
                           facts.get("date")] if x]
    rows = [
        ["ARM class code", f"`{code}`"],
        ["Handbook", f"[{_clean(' / '.join(hb_bits)) or 'handbook'}]({handbook_url})"],
        ["Measurement category", _clean(cat_row.get("categories"))],
        ["Primary measurements", _clean(cat_row.get("measurements"))],
        ["Record", f"{cat_row.get('start_date')} to {cat_row.get('end_date')}"
                   f" ({'active' if str(cat_row.get('active')) == 'True' else 'retired'})"],
        ["Datastreams with data", f"{cat_row.get('n_ds_with_data')} across {cat_row.get('n_sites')} sites"],
        ["Sites", _clean(cat_row.get("sites"))],
        ["ARM page", f"https://www.arm.gov/capabilities/instruments/{code}"],
    ]
    if facts.get("manufacturer_model"):
        rows.insert(3, ["Manufacturer / model", _clean(facts["manufacturer_model"], 200)])
    A(_md_table(["", ""], rows))
    A("")

    # ---- credit ----
    for line in credit_block(facts, handbook_url, code):
        A(line)
    for line in shared_handbook_note(code, siblings, scope_override):
        A(line)

    # ---- principle ----
    A("## How it measures")
    A("")
    A(_clean(facts.get("principle")))
    A("")
    if facts.get("siting"):
        A(f"**Siting.** {_clean(facts['siting'], 700)}")
        A("")
    smp = facts.get("sampling") or {}
    if any(smp.get(k) for k in ("native_rate", "reported_interval", "averaging")):
        bits = [f"native rate {_clean(smp['native_rate'])}" if smp.get("native_rate") else "",
                f"reported every {_clean(smp['reported_interval'])}" if smp.get("reported_interval") else "",
                f"averaging {_clean(smp['averaging'])}" if smp.get("averaging") else ""]
        A("**Sampling.** " + "; ".join(b for b in bits if b) + _cite(smp.get("page")) + ".")
        A("")

    # ---- reported quantities ----
    mq = facts.get("measured_quantities") or []
    if mq:
        A("## Reported quantities")
        A("")
        A("As specified by the handbook. These are the physical quantities, not the netCDF")
        A("variable names - those are in the next section, taken from a real file.")
        A("")
        A(_md_table(["quantity", "units", "range", "uncertainty", "resolution", "source"],
                    [[_clean(q.get("quantity"), 60), _clean(q.get("units"), 28) or "-",
                      _clean(q.get("range"), 40) or "-", _clean(q.get("uncertainty"), 48) or "-",
                      _clean(q.get("resolution"), 28) or "-", _cite(q.get("page")).strip() or "-"]
                     for q in mq[:22]]))
        A("")

    # ---- specifications ----
    sp = facts.get("specifications") or []
    if sp:
        A("## Specifications")
        A("")
        A(_md_table(["parameter", "value", "source"],
                    [[_clean(s.get("parameter"), 60), _clean(s.get("value"), 150),
                      _cite(s.get("page")).strip() or "-"] for s in sp[:26]]))
        if len(sp) > 26:
            A(f"\n_{len(sp) - 26} further specification rows are in the handbook._")
        A("")

    # ---- the data ----
    va = {}
    prim = []
    if no_example_reason:
        for line in no_example_block(code, cat_row, no_example_reason):
            A(line)
        inv, qc = {}, {}
    else:
        A("## The data")
        A("")
        A(f"Verified example: **`{ex_ds}`**, file `{example['filename']}`")
        A(f"({example['size_mb']} MB), pulled from ARM Live and opened with ACT on {verified_on}.")
        A("")
        if inv.get("read_note"):
            A(f"**Reading note.** {_clean(inv['read_note'], 300)}.")
            A("")
        dims = ", ".join(f"`{k}`={v}" for k, v in (inv.get("dims") or {}).items())
        tres = inv.get("time_resolution_s")
        drow = [["Dimensions", dims],
                ["Data variables", str(inv.get("n_vars"))],
                ["QC variables", f"{inv.get('n_qc_vars')} (`qc_` companions)"],
                ["Median time step", f"{tres:g} s" if isinstance(tres, (int, float)) else "n/a"]]
        if inv.get("time_span"):
            drow.append(["File time span", " to ".join(inv["time_span"])])
        ga = inv.get("global_attrs") or {}
        for k in ("sampling_interval", "averaging_interval", "dod_version", "process_version"):
            if ga.get(k):
                drow.append([k.replace("_", " "), _clean(ga[k], 90)])
        A(_md_table(["", ""], drow))
        A("")

        # variable inventory
        va = inv.get("variables") or {}
        skip = re.compile(r"^(qc_|base_time$|time_offset$|time_bounds$|.*_bounds$|lat$|lon$|alt$"
                          r"|latitude$|longitude$|altitude$)")
        prim = [(v, d) for v, d in va.items() if not skip.match(v) and d.get("long_name")]
        prim.sort(key=lambda kv: (not kv[1].get("has_qc"), kv[0]))
        if not prim:
            prim = [(v, d) for v, d in va.items() if not skip.match(v)]
            prim.sort(key=lambda kv: kv[0])
        if prim:
            A("### Variables in that file")
            A("")
            A(_md_table(["variable", "units", "dims", "qc", "long_name"],
                        [[f"`{v}`", _clean(d.get("units"), 22) or "-",
                          ",".join(d.get("dims") or []) or "-", "yes" if d.get("has_qc") else "-",
                          _clean(d.get("long_name"), 70) or "-"] for v, d in prim[:30]]))
            if len(prim) > 30:
                A(f"\n_{len(prim) - 30} more variables; the full inventory is in "
                  f"`example_inventory.json` beside this file._")
            A("")


    # ---- getting the data ----
    A("## Getting the data")
    A("")
    A("ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the")
    A("service, datastream naming and the server-side subset endpoint.")
    A("")
    A(sections.HELPER_NOTE)
    day = example.get("date") or str(cat_row.get("ex_end") or "")[:10] or "YYYY-MM-DD"
    A(sections.fetch_block(ex_ds, day))
    A("")
    if inv.get("n_vars", 0) > 40:
        keep = [v for v, _ in prim[:3]]
        A(f"This datastream carries {inv.get('n_vars')} variables. On any window longer than a day,")
        A("read only what you need - and ask for the QC companion at the same time:")
        A("")
        A(sections.keep_variables_block(ex_ds, keep + [f"qc_{v}" for v in keep
                                                       if va.get(v, {}).get("has_qc")]))
        A("")
    if is_radar:
        A("### Reading it as a radar object")
        A("")
        if pyart_note and pyart_note.get("ok"):
            A(f"This datastream is CfRadial, so Py-ART reads it directly - verified "
              f"{pyart_note.get('nsweeps')} sweep, {pyart_note.get('nrays')} rays x "
              f"{pyart_note.get('ngates')} gates, `scan_type='{pyart_note.get('scan_type')}'`, "
              f"fixed angle {pyart_note.get('fixed_angle')} deg.")
            A("")
            A("```python")
            A("import pyart")
            A(f'radar = pyart.io.read("{example["filename"]}")        # or pyart.aux_io.read_kazr')
            A("print(sorted(radar.fields))")
            A("```")
            A("")
            A("Fields present in the verified file: " +
              ", ".join(f"`{f}`" for f in (pyart_note.get("fields") or [])) + ".")
        else:
            A("Read with `act.io.arm.read_arm_netcdf`; Py-ART's readers are for the CfRadial")
            A("scanning products, not this one.")
        A("")
        A("For the `Radar` object, field naming, sweep anatomy, gate filtering and plotting, load")
        A("`pyart-foundations` and the rest of the `pyart-*` tranche. Vertically pointing")
        A("profilers have one sweep and no split cuts, so the scan-strategy machinery in those")
        A("skills is mostly inapplicable - the time-height view is the useful one.")
        A("")
    if is_lidar:
        A("Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with")
        A("`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range")
        A("coordinate is the usual view.")
        A("")

    # ---- QC ----
    A("## Quality control in this datastream")
    A("")
    nq = qc.get("n_qc_vars", 0)
    if no_example_reason:
        A("Not measured - no file was opened, so this skill cannot say which `qc_` variables")
        A("this datastream carries or which tests fire. ARM b1-level files usually ship a")
        A("`qc_` companion for most measurements; confirm with")
        A('`[v for v in ds.data_vars if v.startswith(\'qc_\')]` once you')
        A("have a file, and read `act-qc` for the assessment-vocabulary trap before filtering.")
        A("")
    elif nq:
        A(f"{nq} `qc_` companion variables cover {len(qc.get('qc_covered') or [])} of the")
        A(f"{inv.get('n_vars')} data variables. Assessments present in the example file: "
          + ", ".join(f"`{a}`" for a in qc.get("assessments") or []) + ".")
        A("")
        A("`cleanup_qc=True` on read is what makes these usable; it rewrites ARM's flag")
        A("attributes into the form `qcfilter` expects. Remember that ARM uses two vocabularies - `Bad`/`Indeterminate`")
        A("from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that")
        A("filtering on only one of them silently keeps known-bad points.")
        A("")
        _cov = [v for v in (qc.get("qc_covered") or []) if v in va] or \
               [v for v in va if not v.startswith("qc_") and f"qc_{v}" in va]
        A(sections.qc_filter_block(_cov[0], _cov[:3]) if _cov
          else sections.single_qc_variable_block(next(v for v in va if v.startswith("qc_"))))
        A("")
        top = [r for r in (qc.get("flagged_top") or []) if isinstance(r, dict) and "error" not in r]
        if top:
            A(f"Measured on the example file ({example['filename']}), the tests that fired:")
            A("")
            A(_md_table(["variable", "test", "flagged", "percent"],
                        [[f"`{_clean(r.get('variable'))}`", _clean(str(r.get('test')), 64),
                          str(r.get("n_flagged")), f"{r.get('percent')}"] for r in top]))
            A("")
            A("A single day is not a quality assessment of the instrument - it shows which tests")
            A("are live in this datastream and what a filter would do to the record.")
            A("")
        else:
            A("On the example file no test fired on any variable, so the flag machinery is")
            A("present but unexercised there - do not read that as a guarantee for other days.")
            A("")
    else:
        A("This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods")
        A("have nothing to act on. Screening has to come from the fields the product provides")
        A("itself and from Data Quality Reports.")
        A("")
        masks = [v for v in (inv.get("variables") or {}) if "mask" in v or "flag" in v]
        if masks:
            A("Mask/flag fields in the verified file: " + ", ".join(f"`{m}`" for m in masks[:8]) + ".")
            A("")
    A("Either way, check the DQRs before trusting a period - they carry the mentor's knowledge")
    A("of icing, misalignment and outages that no automated test catches:")
    A("")
    A("```python")
    A(f'act.qc.print_dqr("{ex_ds}", "{str(cat_row.get("start_date")).replace("-", "")}", '
      f'"{dt.date.today().strftime("%Y%m%d")}")')
    A("```")
    A("")
    if facts.get("qc_notes"):
        A(f"The handbook's own note on data quality: {_clean(facts['qc_notes'], 600)}")
        A("")

    # ---- artifacts ----
    A("## Known artifacts and failure modes")
    A("")
    arts = facts.get("artifacts") or []
    if arts:
        A("From the handbook. This is the section to read before concluding that a feature in")
        A("the data is atmospheric.")
        A("")
        A(_md_table(["issue", "how it shows up", "what the handbook says to do", "source"],
                    [[_clean(a.get("issue"), 90), _clean(a.get("signature"), 190),
                      _clean(a.get("mitigation"), 150) or "-", _cite(a.get("page")).strip() or "-"]
                     for a in arts[:24]]))
        if len(arts) > 24:
            A(f"\n_{len(arts) - 24} further items in the handbook._")
    else:
        A("The handbook documents no artifacts or failure modes explicitly. That is a gap in the")
        A("handbook, not evidence the instrument has none.")
    A("")

    # ---- calibration / maintenance ----
    cal, mnt = facts.get("calibration") or {}, facts.get("maintenance") or {}
    if any(cal.values()) or any(mnt.values()):
        A("## Calibration and maintenance")
        A("")
        crows = []
        for label, key, src in [("Calibration method", cal.get("method"), cal.get("page")),
                                ("Calibration interval", cal.get("interval"), cal.get("page")),
                                ("Traceability", cal.get("traceability"), cal.get("page")),
                                ("Routine maintenance", mnt.get("routine"), mnt.get("page")),
                                ("Maintenance interval", mnt.get("interval"), mnt.get("page"))]:
            if key:
                crows.append([label, _clean(key, 320) + _cite(src)])
        A(_md_table(["", ""], crows))
        A("")
        A("Calibration history matters for trend work: a step at a calibration date is an")
        A("instrument event, not a climate signal.")
        A("")

    # ---- related ----
    A("## Related")
    A("")
    A("| skill | why |")
    A("|---|---|")
    A("| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |")
    A("| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |")
    A("| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |")
    A("| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |")
    if is_radar:
        A("| `pyart-foundations` | the `Radar` object, fields, sweeps, IO, cmweather |")
        A("| `pyart-gatefilter-qc` | gate filtering for radar moments |")
    A("")
    rel = [_clean(r, 70) for r in (facts.get("related_instruments") or []) if r]
    if rel:
        A("Instruments the handbook names as complements or predecessors: " +
          ", ".join(rel[:10]) + ".")
        A("")
    defs = [d for d in (facts.get("definitions") or []) if d.get("term")][:14]
    if defs:
        A("### Acronyms the handbook defines")
        A("")
        A(_md_table(["term", "meaning"],
                    [[f"`{_clean(d['term'], 24)}`", _clean(d.get("meaning"), 90)] for d in defs]))
        A("")
    refs = [_clean(r, 220) for r in (facts.get("references") or []) if r][:10]
    if refs:
        A("### References the handbook cites")
        A("")
        for r in refs:
            A(f"- {r}")
        A("")

    # ---- provenance ----
    A("## Verified against")
    A("")
    auth = ", ".join(_clean(a) for a in (facts.get("authors") or []) if _clean(a))
    A(f"- Handbook: {handbook_url} ({n_pages} pages"
      + (f", {_clean(facts.get('report_number'))}" if facts.get("report_number") else "")
      + (f", by {auth}" if auth else ", no individual author named on the cover") + ")")
    A(f"- Catalog record: ARM data-source index, `instrument_class_code={code}`, read {verified_on}")
    if no_example_reason:
        A(f"- Example file: none - {no_example_reason}")
    else:
        A(f"- Example file: `{example['filename']}` from `{ex_ds}`, {example['size_mb']} MB,")
        A(f"  opened with ACT {example.get('act_version', '')} on {verified_on}")
    A("- Handbook facts in this file were extracted from the PDF text and page-cited; the data")
    A("  facts were measured from the example file. Numbers in the two groups are independent,")
    A("  and where they disagree the file is the current truth and the handbook the design intent.")
    A("")
    return "\n".join(L)
