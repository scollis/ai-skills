# ai-skills

Agent skills for atmospheric and radar science, authored by **Scott Collis** with
**Claude** (Anthropic) and used with Claude Science.

A *skill* here is a directory holding a `SKILL.md` — prose an agent loads as
reference — and usually a `kernel.py` of helper functions that load alongside it.
The point of committing them is not the code volume; it is that **the factual
claims are checked**. Bucket names, cost constants, and layout quirks go stale
quietly, so the test suites in `tests/` re-verify them against live services and
the offline suite refuses documentation that has drifted from its own code.

## What is here

| skill | what it does |
|---|---|
| [`nexrad-aws-2025`](skills/nexrad-aws-2025/) | NEXRAD on AWS after the 2025 migration: bucket map, VCP/SAILS/AVSET detection, ARCO access primitives |
| [`nexrad-cloud-router`](skills/nexrad-cloud-router/) | Chooses among the four NEXRAD access paths on measured cost, and names the skill to load per step |
| [`nexrad-cost-calibration`](skills/nexrad-cost-calibration/) | Re-measures those cost constants for the local machine and link |
| [`nexrad-arco`](skills/nexrad-arco/) | ARCO Icechunk/Zarr store to Py-ART; QVPs, METAR overlays, animations |
| [`nexrad-radar-gcs`](skills/nexrad-radar-gcs/) | GCS mirror fallback when AWS is blocked, plus PPI / dual-pol plotting helpers |

This is the first tranche — NEXRAD cloud access and routing — chosen because the
2025 bucket migration broke most existing code and these five cross-reference
each other. Later tranches will add radar quantitative products, ARM observatory
workflows, and multi-platform event science.

Two skills referenced by this tranche are **not yet published here**:
`nexrad-site-rainfall` and `nexrad-area-over-threshold`. They belong to the next
tranche; until then those cross-references point at nothing in this repo.

## Using a skill

With Claude Science, load by name and the helpers arrive in your kernel:

```python
skill("nexrad-cloud-router")
plan = plan_analysis("three month base tilt series", site="KLOT", n_volumes=2000)
print(format_plan(plan))
```

Without it, `SKILL.md` is readable on its own and `kernel.py` imports as an
ordinary module:

```python
import sys; sys.path.insert(0, "skills/nexrad-aws-2025")
import kernel as nexrad
keys = nexrad.nexrad_keys("KLOT", start, end, client=nexrad.s3_anon())
```

The one thing to know: **`kernel.py` files are exec'd by the skill loader, not
imported**, so they define no `__file__` and may only contain functions, imports,
and literal top-level assignments. `tests/test_structure.py` enforces that.

## Tests

```bash
pip install -r requirements.txt
pytest tests/test_structure.py        # offline, seconds, runs on every push
pytest tests/test_live_*.py           # hits live buckets, runs weekly
```

The offline suite checks skill structure, the loader's constraints, absence of
secrets, and documentation-vs-code agreement. The live suites are the ones that
detect service drift — a changed bucket layout or store schema shows up as a
failing scheduled run rather than as a wrong answer in someone's analysis.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: edit under `skills/`, run the
offline suite, and keep every numeric claim in a `SKILL.md` derived from
something a test can check.

## Authors

- Scott Collis
- Claude (Anthropic) — co-author of the skills, helpers, and test suites

## License

[MIT](LICENSE). The skills describe public datasets (NOAA NEXRAD via the NSF
Unidata AWS buckets, the NEXRAD ARCO store, and the Google Cloud mirror); the
data carry their own terms.

_Skill contents last synced from the registry: 2026-08-26._
