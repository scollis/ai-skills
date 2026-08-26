# Contributing

## Layout

```
skills/<skill-name>/SKILL.md     prose the agent loads (YAML frontmatter: name, description)
skills/<skill-name>/kernel.py    helpers, exec'd into the kernel when the skill loads
tests/test_structure.py          offline; runs on every push
tests/test_live_*.py             hit live services; run weekly
tools/sync_skills.py             move skills between this repo and a registry
```

## The rule that matters

**Every numeric or factual claim in a `SKILL.md` should be traceable to something
a test can check.** Three separate bugs during this repo's first tranche were
prose that had drifted from behaviour — a crossover value left over from a
superseded constant, a check count that stopped matching its suite, a
recommendation pointing at a decommissioned bucket. Each is now an assertion.

If you write "17 chunks" or "22 checks pass" in a document, add the test that
compares that number against the code. If it cannot be checked, phrase it as an
observation with a date rather than a fact.

## `kernel.py` constraints

The loader `exec`s these files rather than importing them, so:

- no `__file__` — recover a path from `some_function.__code__.co_filename`
- top-level statements may only be functions, imports, and **literal**
  assignments (`re.compile(...)`, `dict(...)`, and even `-999.0` are rejected —
  the last parses as a unary operation, so store a positive threshold and negate
  at the call site)
- no `_`-prefixed top-level names; they are reserved
- no angle-bracket text in the `description` frontmatter — the registry reads it
  as markup

`pytest tests/test_structure.py` checks all of these.

## Before opening a PR

```bash
pytest tests/test_structure.py
pytest tests/test_live_*.py          # if you touched anything about access paths
```

Update the `Verified against` section with the date you re-ran the live suites.
That date is what tells a future reader when to stop trusting the document.

## Syncing with a registry

From a Claude Science `repl` cell:

```python
exec(open("tools/sync_skills.py").read())
status()                          # diff both directions, changes nothing
pull()                            # registry -> repo, then review with git diff
push(["nexrad-aws-2025"])         # repo -> registry, explicit names only
```

`push()` takes explicit names on purpose — publishing changes what every future
agent session loads.
