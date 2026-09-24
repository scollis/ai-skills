"""Structured fact extraction from ARM instrument handbook PDFs.

Usage (in the python kernel, with `host` available):
    from extract import extract_handbook_facts
    facts = extract_handbook_facts(host, code, pages, catalog_row, inventory)

Returns a dict of handbook-derived facts with page citations. Never invents values:
every field is either grounded in the handbook text or omitted.
"""
import json
import re

def _s(desc, **kw):
    d = {"type": "string", "description": desc}
    d.update(kw)
    return d


def _arr(desc, props, required):
    return {"type": "array", "description": desc,
            "items": {"type": "object", "properties": props, "required": required}}


TOOL = {
    "name": "record_handbook_facts",
    "description": "Record reference facts extracted from an ARM instrument handbook.",
    "input_schema": {
        "type": "object",
        "properties": {
            "report_number": _s("DOE/SC-ARM-TR-nnn exactly as printed on the cover; empty string if absent"),
            "title": _s("handbook title as printed"),
            "authors": {"type": "array", "items": {"type": "string"},
                        "description": "authors as printed on the cover"},
            "date": _s("month and year as printed; empty string if absent"),
            "revision": _s("revision or version string from the cover or revision-history table; empty if none"),
            "one_line": _s("one sentence: what this instrument measures and how it is deployed"),
            "principle": _s("3-5 sentences on the measurement principle, in the handbook's own physics terms"),
            "measured_quantities": _arr(
                "the quantities this instrument reports",
                {"quantity": _s("name as printed"), "units": _s("unit string as printed"),
                 "range": _s("measurement range as printed, else empty"),
                 "uncertainty": _s("accuracy/uncertainty as printed, else empty"),
                 "resolution": _s("resolution as printed, else empty"),
                 "page": {"type": "integer", "description": "1-based page block the fact came from"}},
                ["quantity", "page"]),
            "specifications": _arr(
                "rows of the instrument specification table(s), parameter names as printed",
                {"parameter": _s("as printed"), "value": _s("as printed, with units"),
                 "page": {"type": "integer"}},
                ["parameter", "value", "page"]),
            "manufacturer_model": _s("vendor and model designation(s); empty if absent"),
            "sampling": {"type": "object", "description": "temporal sampling as described by the handbook",
                         "properties": {"native_rate": _s(""), "reported_interval": _s(""),
                                        "averaging": _s(""), "page": {"type": "integer"}}},
            "siting": _s("deployment, siting or orientation requirements that affect data interpretation; empty if absent"),
            "calibration": {"type": "object",
                            "properties": {"method": _s(""), "interval": _s(""),
                                           "traceability": _s(""), "page": {"type": "integer"}}},
            "maintenance": {"type": "object",
                            "properties": {"routine": _s(""), "interval": _s(""), "page": {"type": "integer"}}},
            "artifacts": _arr(
                "every known limitation, interference, failure mode, environmental sensitivity, "
                "calibration drift, saturation limit, blind range, contamination pathway or "
                "data-interpretation caveat the handbook mentions",
                {"issue": _s("named artifact, failure mode or limitation"),
                 "signature": _s("how it shows up in the data - what the analyst would notice in a plot or statistic"),
                 "mitigation": _s("what the handbook says to do about it; empty if it says nothing"),
                 "page": {"type": "integer"}},
                ["issue", "signature", "page"]),
            "qc_notes": _s("what the handbook says about quality control, flags or data-quality reports; empty if absent"),
            "data_products": {"type": "object",
                              "properties": {"datastreams": {"type": "array", "items": {"type": "string"}},
                                             "variables": {"type": "array", "items": {"type": "string"}},
                                             "page": {"type": "integer"}}},
            "definitions": _arr("acronyms or terms the handbook defines",
                                {"term": _s(""), "meaning": _s("")}, ["term", "meaning"]),
            "references": {"type": "array", "items": {"type": "string"},
                           "description": "short citations the handbook lists for the measurement technique"},
            "related_instruments": {"type": "array", "items": {"type": "string"},
                                    "description": "other ARM instruments this one complements or supersedes, as named in the handbook"},
        },
        "required": ["title", "one_line", "principle", "measured_quantities", "artifacts"],
    },
}

SCHEMA = """{
  "report_number": "DOE/SC-ARM-TR-nnn as printed on the cover, or null",
  "title": "handbook title as printed",
  "authors": ["as printed on the cover"],
  "date": "month year as printed, or null",
  "revision": "revision/version string if the cover or history table shows one, else null",
  "one_line": "one sentence: what this instrument measures and how it is deployed",
  "principle": "3-5 sentences on the measurement principle, in the handbook's own physics terms",
  "measured_quantities": [
    {"quantity": "", "units": "", "range": "", "uncertainty": "", "resolution": "", "page": 0}
  ],
  "specifications": [{"parameter": "", "value": "", "page": 0}],
  "manufacturer_model": "vendor and model designation(s), or null",
  "sampling": {"native_rate": "", "reported_interval": "", "averaging": "", "page": 0},
  "siting": "deployment/siting/orientation requirements that affect data interpretation, or null",
  "calibration": {"method": "", "interval": "", "traceability": "", "page": 0},
  "maintenance": {"routine": "", "interval": "", "page": 0},
  "artifacts": [
    {"issue": "named artifact, failure mode, or known limitation",
     "signature": "how it shows up in the data (what a user would see)",
     "mitigation": "what the handbook says to do about it, or null",
     "page": 0}
  ],
  "qc_notes": "what the handbook says about quality control, flags, or data-quality reports, or null",
  "data_products": {"datastreams": [], "variables": [], "page": 0},
  "definitions": [{"term": "", "meaning": ""}],
  "references": ["short citations the handbook lists for the measurement technique"],
  "related_instruments": ["other ARM instrument names/acronyms the handbook says this one complements or supersedes"]
}"""

PROMPT = """You are extracting reference facts from a U.S. DOE ARM facility instrument
handbook so that a data-analysis agent can work with this instrument's data correctly.

INSTRUMENT: {name} (ARM instrument class code: {code})
ARM catalog description: {desc}
ARM catalog measurement categories: {cats}

The handbook text follows, one page per delimited block.

=== HANDBOOK TEXT START ===
{text}
=== HANDBOOK TEXT END ===

Return ONLY a JSON object matching this schema, no prose, no markdown fence:

{schema}

Rules, in order of importance:
1. GROUNDING. Every value must come from the handbook text above. If the handbook does
   not state something, use null for a scalar field or omit the list entry. Never fill a
   field with general knowledge about this instrument type, and never guess a number.
2. PAGE NUMBERS. "page" is the 1-based index of the delimited page block the fact came
   from. If a fact spans pages, cite the first.
3. NUMBERS VERBATIM. Copy values, units and tolerances exactly as printed, including the
   unit string ("+/- 0.1 degC", "0-100 %RH", "1 min"). Do not convert or round.
4. ARTIFACTS ARE THE POINT. The "artifacts" list is the most valuable part of this
   extraction. Include every known limitation, interference, failure mode, environmental
   sensitivity, calibration drift, saturation limit, blind range, contamination pathway
   and data-interpretation caveat the handbook mentions - aim for completeness over
   brevity, and write "signature" as what the analyst would actually notice in a plot or
   a summary statistic. If the handbook mentions none, return an empty list.
5. SPECIFICATIONS. Pull the instrument specification table(s) if present. Keep parameter
   names as printed.
6. Prefer the handbook's own wording for technical terms. Do not editorialise, do not add
   recommendations of your own, and do not mention this prompt.
"""


def build_prompt(code, name, desc, cats, pages, max_chars=110000):
    blocks = []
    total = 0
    for i, p in enumerate(pages, 1):
        t = re.sub(r"\n{3,}", "\n\n", (p or "").strip())
        if not t:
            continue
        b = f"--- PAGE {i} ---\n{t}"
        if total + len(b) > max_chars:
            blocks.append(f"--- PAGE {i} ---\n[truncated]")
            break
        blocks.append(b)
        total += len(b)
    return PROMPT.format(name=name, code=code, desc=(desc or "")[:900],
                         cats=cats or "", text="\n\n".join(blocks), schema=SCHEMA)


def parse_json_reply(text):
    """Tolerate a stray markdown fence or leading prose around the JSON object."""
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        i, j = t.find("{"), t.rfind("}")
        if i >= 0 and j > i:
            return json.loads(t[i:j + 1])
        raise


def extract_batch(host, jobs, model=None, max_concurrency=4, max_tokens=16000):
    """jobs: list of dicts with code/name/desc/cats/pages. Returns {code: facts|{'error':...}}.

    Uses a forced tool call so the reply is schema-valid JSON rather than prose that has
    to survive json.loads - handbook values contain bare quote characters (inches, arcsec)
    that break free-text JSON generation.
    """
    reqs = [{"prompt": build_prompt(j["code"], j["name"], j.get("desc"), j.get("cats"), j["pages"]),
             "max_tokens": max_tokens,
             "tools": [TOOL],
             "tool_choice": {"type": "tool", "name": TOOL["name"]},
             "model": model or host.reasoning_model()} for j in jobs]
    replies = host.llm(reqs, max_concurrency=max_concurrency)
    out = {}
    for j, r in zip(jobs, replies):
        code = j["code"]
        if isinstance(r, dict) and r.get("error"):
            out[code] = {"error": str(r["error"])[:300]}
            continue
        tu = r.get("tool_use")
        if isinstance(tu, list):
            tu = tu[0] if tu else None
        if not tu:
            out[code] = {"error": f"no tool_use in reply (stop_reason={r.get('stop_reason')})"}
            continue
        out[code] = recover(tu.get("input", tu))
    return out


def recover(inp):
    """Some replies put the whole JSON document into one string field instead of filling
    the schema. The payload is intact, so parse it out rather than re-calling the model."""
    if not isinstance(inp, dict):
        return {"error": f"tool input was {type(inp).__name__}"}
    if isinstance(inp.get("artifacts"), list) or len(inp) > 3:
        return inp
    for v in inp.values():
        if isinstance(v, str) and v.lstrip().startswith("{"):
            try:
                return parse_json_reply(v)
            except Exception:
                pass
    return inp
