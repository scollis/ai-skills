# ARM instrument skill build pipeline

Produces the per-instrument skills under `skills/arm-instruments/`. Run from a Claude
Science python cell with `host` available and `ARMUSER`/`ARMTOKEN` in the environment.

    extract.py   handbook PDF text -> page-cited structured facts (forced tool call,
                 so handbook values containing bare quote characters survive)
    compose.py   facts + catalog record + measured file inventory -> SKILL.md

The order that matters: fetch the catalog record, resolve and download the handbook,
extract facts, pull one real file from ARM Live and open it with ACT, then compose. The
data facts must come from the file, never from the handbook, because the two disagree
often enough to matter - a handbook describes the instrument as designed, the file
records what the ingest currently writes.

`skills/arm-instruments/kernel.py` carries the catalog and handbook-resolution helpers
both steps use.
