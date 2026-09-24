"""Compose a per-VAP SKILL.md from technical-report facts + verified example data.

A VAP is a derived product: it consumes instrument datastreams and applies a retrieval
or QC algorithm. The sections differ from an instrument skill accordingly - an algorithm
and its inputs instead of a measurement principle and a calibration schedule - but the
grounding rule is the same, and it is stated in every file: the report is the design
intent, the file is what the archive currently serves.

Reuses the helpers in compose.py so the two templates cannot drift apart.
"""
import datetime as dt

from compose import _clean, _cite, _md_table, no_example_block, trim_description


def vap_credit_block(facts, report_url, code):
    """Credit the report's authors - ARM's VAP developers and mentors. Deliberately not the
    instrument tranche's credit_block: a VAP cites a technical report, not a handbook, and
    its page marker is `tr p. N`, so reusing that wording would misdescribe the source."""
    authors = [_clean(a) for a in (facts.get("authors") or []) if _clean(a)]
    title = _clean(facts.get("title")) or f"{code} technical report"
    bits = [b for b in [_clean(facts.get("report_number")), _clean(facts.get("date"))] if b]
    tail = (", " + ", ".join(bits)) if bits else ""
    L = ["## Credit", ""]
    if authors:
        who = ", ".join(authors)
        L += [f"Everything this skill knows about the retrieval is the work of **{who}** -",
              "the ARM developers and mentors who wrote the technical report it derives from:", ""]
    else:
        who = "ARM Climate Research Facility"
        L += ["The technical report this skill derives from names no individual author on its",
              "cover; it is issued by the ARM facility. The algorithm knowledge in it is still the",
              "programme's work, not this file's:", ""]
    L += [f"> {who}. *{title}*{tail}.",
          "> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.",
          f"> {report_url}",
          "",
          "Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is",
          "a navigational layer over their document plus a measurement of one data file; it",
          "replaces neither, and where it is thinner than the report the report is right.",
          ""]
    return L


def vap_description(code, name, facts, cat, ex_ds, inputs, verified=True):
    quantities = ", ".join(x for x in (_clean(q.get("quantity")).split("(")[0].strip()
                                       for q in (facts.get("measured_quantities") or [])[:6])
                           if 1 < len(x) <= 34)
    trig = [code, name, ex_ds] + [f"{i} VAP" for i in inputs[:3]]
    trig += [x for x in (_clean(q.get("quantity")).split("(")[0].strip()
                         for q in (facts.get("measured_quantities") or [])[:5]) if 1 < len(x) <= 34]
    trig += [w for w in (cat or "").split("; ") if w]
    trig = [t for t in dict.fromkeys(t for t in trig if t) if 1 < len(t) < 60]
    ex_clause = (f"Includes a verified ARM Live example ({ex_ds}) and the variable inventory of a "
                 f"real file. " if verified else
                 "No data file could be verified for this product, and the skill says so in place "
                 "of a variable inventory. ")
    inp = (f"Derived from {', '.join(inputs[:4])}. " if inputs else "")
    d = (f"ARM {name} ({code}) - value-added product reference from its technical report. "
         f"{inp}The retrieval algorithm, reported quantities ({quantities}), retrieval settings, "
         f"input dependencies, embedded QC coverage, and the documented failure modes and "
         f"conditions where the retrieval is invalid or biased. " + ex_clause +
         f"Use when working with {code} data, deciding whether this product or its input "
         f"instrument answers a question, interpreting its variables, or judging whether a "
         f"feature is a retrieval artifact. Category - {cat}. Triggers - " + ", ".join(trig) + ".")
    return trim_description(_clean(d).replace(": ", " - "))


def compose_vap(code, facts, row, inv, qc, example, report_url, n_pages, inputs=(),
                scope_note=None, coverage_note=None, no_example_reason=None, verified_on=None):
    verified_on = verified_on or dt.date.today().isoformat()
    example = example or {}
    ex_ds = example.get("datastream") or row.get("ex_datastream") or ""
    name = row["name"]
    inputs = list(inputs)
    L = []
    A = L.append

    A("---")
    A(f"name: arm-vap-{code}")
    A("description: " + vap_description(code, name, facts, row.get("categories", ""), ex_ds,
                                        inputs, verified=not no_example_reason))
    A("---")
    A("")
    A(f"# {code.upper()} - {name}")
    A("")
    A(_clean(facts.get("one_line")) or name)
    A("")
    A("A **value-added product**: ARM computes it from instrument data rather than measuring it.")
    if no_example_reason:
        A(f"Facts below are marked with their source - the technical report (`tr p. N`, {n_pages} pages)")
        A(f"or ARM's data-source catalog. No data file could be verified; see **The data**.")
    else:
        A(f"Facts below are marked with their source - the technical report (`tr p. N`, {n_pages} pages),")
        A(f"ARM's catalog, or the example file under **The data**, which was opened rather than assumed.")
    A(f"Compiled {verified_on}.")
    A("")

    hb = [x for x in [facts.get("report_number"), ", ".join(facts.get("authors") or []),
                      facts.get("date")] if x]
    rows = [["ARM class code", f"`{code}`"],
            ["Product type", "value-added product (VAP)"],
            ["Technical report", f"[{_clean(' / '.join(hb)) or 'report'}]({report_url})"],
            ["Category", _clean(row.get("categories"))],
            ["Input instruments", ", ".join(f"`{i}`" for i in inputs) if inputs else
                                  "not declared in ARM's catalog - see Inputs below"],
            ["Record", f"{row.get('start_date')} to {row.get('end_date')}"
                       f" ({'active' if str(row.get('active')) == 'True' else 'retired'})"],
            ["Datastreams with data", f"{row.get('n_ds_with_data')} across {row.get('n_sites')} sites"],
            ["ARM page", f"https://www.arm.gov/capabilities/science-data-products/vaps/{code}"]]
    A(_md_table(["", ""], rows))
    A("")

    for line in vap_credit_block(facts, report_url, code):
        A(line)
    if scope_note:
        A(f"> **Scope of this report.** {scope_note}.")
        A("")
    if coverage_note:
        A(f"> **Extraction coverage.** {coverage_note}. Counts drawn from this skill's lists are")
        A("> lower bounds on what the report contains, not a complete inventory of it.")
        A("")

    A("## How it is produced")
    A("")
    A(_clean(facts.get("principle")))
    A("")
    smp = facts.get("sampling") or {}
    if any(smp.get(k) for k in ("native_rate", "reported_interval", "averaging")):
        bits = [f"input rate {_clean(smp['native_rate'])}" if smp.get("native_rate") else "",
                f"output every {_clean(smp['reported_interval'])}" if smp.get("reported_interval") else "",
                f"averaging {_clean(smp['averaging'])}" if smp.get("averaging") else ""]
        A("**Cadence.** " + "; ".join(b for b in bits if b) + _cite(smp.get("page")) + ".")
        A("")

    A("## Inputs")
    A("")
    rel = [_clean(r, 70) for r in (facts.get("related_instruments") or []) if r]
    if inputs:
        A("ARM's catalog declares these input instrument classes: " +
          ", ".join(f"`{i}`" for i in inputs) + ".")
        A("")
    if rel:
        A("The report names these instruments and sibling products: " + ", ".join(rel[:12]) + ".")
        A("")
    if not inputs and not rel:
        A("Neither ARM's catalog nor the report names the inputs explicitly - read the algorithm")
        A("section above, and check the `input_source` global attribute of a real file.")
        A("")
    A("A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check")
    A("the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding")
    A("the algorithm is at fault; the reverse is rarer.")
    A("")

    mq = facts.get("measured_quantities") or []
    if mq:
        A("## Reported quantities")
        A("")
        A("As specified by the report. These are the physical quantities, not the netCDF variable")
        A("names - those are in the next section, taken from a real file.")
        A("")
        A(_md_table(["quantity", "units", "range", "uncertainty", "source"],
                    [[_clean(q.get("quantity"), 60), _clean(q.get("units"), 26) or "-",
                      _clean(q.get("range"), 34) or "-", _clean(q.get("uncertainty"), 46) or "-",
                      _cite(q.get("page")).strip() or "-"] for q in mq[:22]]))
        A("")

    sp = facts.get("specifications") or []
    if sp:
        A("## Retrieval settings")
        A("")
        A(_md_table(["parameter", "value", "source"],
                    [[_clean(s.get("parameter"), 60), _clean(s.get("value"), 150),
                      _cite(s.get("page")).strip() or "-"] for s in sp[:26]]))
        if len(sp) > 26:
            A(f"\n_{len(sp) - 26} further rows in the report._")
        A("")

    va, prim = {}, []
    if no_example_reason:
        for line in no_example_block(code, row, no_example_reason):
            A(line)
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
        drow = [["Dimensions", dims], ["Data variables", str(inv.get("n_vars"))],
                ["QC variables", f"{inv.get('n_qc_vars')} (`qc_` companions)"],
                ["Median time step", f"{tres:g} s" if isinstance(tres, (int, float)) else "n/a"]]
        if inv.get("time_span"):
            drow.append(["File time span", " to ".join(inv["time_span"])])
        ga = inv.get("global_attrs") or {}
        for k in ("input_source", "dod_version", "process_version"):
            if ga.get(k):
                drow.append([k.replace("_", " "), _clean(ga[k], 120)])
        A(_md_table(["", ""], drow))
        A("")
        if ga.get("input_source"):
            A("Note the `input_source` attribute: for a VAP it records the actual input files, which")
            A("is the fastest way to find out which instrument and level a given output came from.")
            A("")
        import re as _re
        va = inv.get("variables") or {}
        skip = _re.compile(r"^(qc_|base_time$|time_offset$|.*_bounds$|lat$|lon$|alt$"
                           r"|latitude$|longitude$|altitude$)")
        prim = [(v, d) for v, d in va.items() if not skip.match(v) and d.get("long_name")]
        prim.sort(key=lambda kv: (not kv[1].get("has_qc"), kv[0]))
        if not prim:
            prim = sorted(((v, d) for v, d in va.items() if not skip.match(v)), key=lambda kv: kv[0])
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

    A("## Getting the data")
    A("")
    A("ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream")
    A("naming and the server-side subset endpoint.")
    A("")
    day = example.get("date") or str(row.get("ex_end") or "")[:10] or "YYYY-MM-DD"
    A("```python")
    A("import act")
    A(f'files = armlive_list_files("{ex_ds}", "{day}", "{day}")')
    A(f'ds = armlive_open("{ex_ds}", "{day}", "{day}", cleanup_qc=True)')
    A("```")
    A("")
    if inv.get("n_vars", 0) > 40:
        keep = [v for v, _ in prim[:3]]
        A(f"This product carries {inv.get('n_vars')} variables. Over any window longer than a day,")
        A("read only what you need, and ask for the QC companion at the same time:")
        A("")
        A("```python")
        A(f'ds = armlive_open("{ex_ds}", start, end,')
        A("                  keep_variables=" + repr(keep + [f"qc_{v}" for v in keep
                                                             if va.get(v, {}).get("has_qc")]) + ")")
        A("```")
        A("")

    A("## Quality control in this product")
    A("")
    nq = qc.get("n_qc_vars", 0)
    if no_example_reason:
        A("Not measured - no file was opened, so this skill cannot say which `qc_` variables this")
        A("product carries. Confirm with `act_qc_variables(ds)` once you have a file, and read")
        A("`act-qc` for the assessment-vocabulary trap before filtering.")
        A("")
    elif nq:
        A(f"{nq} `qc_` companion variables cover {len(qc.get('qc_covered') or [])} of the")
        A(f"{inv.get('n_vars')} data variables. Assessments present in the example file: "
          + ", ".join(f"`{a}`" for a in qc.get("assessments") or []) + ".")
        A("")
        A("A VAP's QC flags describe the retrieval, not the instrument: a value flagged here may")
        A("mean the algorithm refused to converge, or that an input was missing, rather than that")
        A("the sensor misbehaved. Read `flag_meanings` before interpreting a filtered series.")
        A("")
        A("```python")
        A("act_qc_table(ds)                       # what each bit would remove, per variable")
        A("act_qc_apply(ds, variables=[...])      # NaN-fill using all four assessment names")
        A("```")
        A("")
        top = [r for r in (qc.get("flagged_top") or []) if isinstance(r, dict) and "error" not in r]
        if top:
            A(f"Measured on the example file ({example['filename']}), the tests that fired:")
            A("")
            A(_md_table(["variable", "test", "flagged", "percent"],
                        [[f"`{_clean(r.get('variable'))}`", _clean(str(r.get('test')), 64),
                          str(r.get("n_flagged")), f"{r.get('percent')}"] for r in top]))
            A("")
        else:
            A("On the example file no test fired, so the machinery is present but unexercised")
            A("there - not a guarantee for other days.")
            A("")
    else:
        A("This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have")
        A("nothing to act on. Screening has to come from the product's own fields and from DQRs.")
        A("")
        masks = [v for v in (inv.get("variables") or {}) if "mask" in v or "flag" in v or "qual" in v]
        if masks:
            A("Mask, flag or quality fields in the verified file: " +
              ", ".join(f"`{m}`" for m in masks[:8]) + ".")
            A("")
    A("Check the DQRs before trusting a period - for a VAP they cover both the product and the")
    A("instruments feeding it:")
    A("")
    A("```python")
    A(f'act.qc.print_dqr("{ex_ds}", "{str(row.get("start_date") or "").replace("-", "")}", '
      f'"{dt.date.today().strftime("%Y%m%d")}")')
    A("```")
    A("")
    if facts.get("qc_notes"):
        A(f"The report's own note on quality: {_clean(facts['qc_notes'], 600)}")
        A("")

    A("## Documented failure modes")
    A("")
    arts = facts.get("artifacts") or []
    if arts:
        A("From the technical report. For a derived product these are mostly conditions where the")
        A("retrieval is invalid, biased, or silently falls back - read this before concluding that")
        A("a feature in the output is atmospheric.")
        A("")
        A(_md_table(["issue", "how it shows up", "what the report says to do", "source"],
                    [[_clean(a.get("issue"), 90), _clean(a.get("signature"), 190),
                      _clean(a.get("mitigation"), 150) or "-", _cite(a.get("page")).strip() or "-"]
                     for a in arts[:24]]))
        if len(arts) > 24:
            A(f"\n_{len(arts) - 24} further items in the report._")
    else:
        A("The report documents no failure modes explicitly. That is a gap in the report, not")
        A("evidence the retrieval has none.")
    A("")

    A("## Related")
    A("")
    A("| skill | why |")
    A("|---|---|")
    A("| `arm-vaps` | the index of these VAP skills |")
    A("| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |")
    A("| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |")
    A("| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |")
    A("| `act-plotting` | the Display family, QC block plots, time-height sections |")
    A("")
    for i in inputs:
        A(f"- input instrument `{i}`: load `arm-instrument-{i}` for its handbook facts and artifacts")
    if inputs:
        A("")
    refs = [_clean(r, 220) for r in (facts.get("references") or []) if r][:10]
    if refs:
        A("### References the report cites")
        A("")
        for r in refs:
            A(f"- {r}")
        A("")

    A("## Verified against")
    A("")
    auth = ", ".join(_clean(a) for a in (facts.get("authors") or []) if _clean(a))
    A(f"- Technical report: {report_url} ({n_pages} pages"
      + (f", {_clean(facts.get('report_number'))}" if facts.get("report_number") else "")
      + (f", by {auth}" if auth else ", no individual author named on the cover") + ")")
    A(f"- Catalog record: ARM data-source index, `instrument_class_code={code}`, read {verified_on}")
    if no_example_reason:
        A(f"- Example file: none - {no_example_reason}")
    else:
        A(f"- Example file: `{example['filename']}` from `{ex_ds}`, {example['size_mb']} MB,")
        A(f"  opened with ACT {example.get('act_version', '')} on {verified_on}")
    if coverage_note:
        A(f"- Extraction coverage: {coverage_note}")
    A("- Report facts were extracted from the PDF text and page-cited; data facts were measured")
    A("  from the example file. Where the two disagree the file is the current truth and the")
    A("  report the design intent - a VAP's output changes with its version.")
    A("")
    return "\n".join(L)
