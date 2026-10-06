---
name: backend-swap-validation
description: Validate replacing a hand-rolled numerical kernel with a library implementation (FFT/NUFFT, linear algebra, optimisation, GPU backends) behind an optional-dependency engine layer. Use when swapping in scipy/finufft/ducc0/torch/cupy alternatives to existing code, checking a new backend against a reference implementation, deciding whether a backend disagreement is a bug or an accuracy improvement, or benchmarking engine and solver choices without misattributing the speedup.
---

# Backend-swap validation

Replacing working hand-rolled numerics with a library call looks like a
mechanical substitution and is not. The library uses a different kernel,
a different convention, and a different accuracy knob, so the new answer
will *differ* from the old one — and the hard question is not whether it
differs but **which of the two is wrong**. This skill is the procedure for
answering that, and for not misattributing the speedup afterwards.

## The core problem

Three quantities, and you need all three:

| measurement | what it tells you |
|---|---|
| candidate vs reference | that they disagree — nothing about who is right |
| **reference vs exact** | the reference's OWN error: the floor on any honest tolerance |
| candidate vs exact | whether the candidate is better or worse than what it replaces |

A candidate-vs-reference number alone is uninterpretable. Get closed-form
`exact` output — computed with machinery that shares no code with either
implementation — and `three_way_error(candidate, reference, exact)` reads the
verdict off the three:

- `candidate_vs_exact` **below** `reference_vs_exact` → the candidate is more
  accurate; the disagreement is the *reference's* error. Report it that way.
- `candidate_vs_exact` **above** it, or `candidate_vs_reference` much larger
  than either → a real defect. Suspect convention, scaling, or indexing.

Never tighten a candidate-vs-reference tolerance below `reference_vs_exact`.
No backend can match the reference more closely than the reference matches
truth, and a test that demands it will fail on a *better* implementation.

## Workflow

1. **Profile the reference before choosing a backend.** The bottleneck is
   often not the transform. Unbuffered scatters (`np.add.at`), complex
   transforms on real data, and per-call setup routinely dominate — and each
   has an exact fix in the library you already depend on. Establish the
   dependency-free ceiling first; it may be most of the available win, and it
   costs nothing to install.
2. **Check the problem size against the library's assumptions.** Asymptotic
   advantages assume you are in the asymptotic regime. If the dimension is a
   sample count rather than an image dimension, the "obviously unaffordable"
   exact method (dense DFT, direct factorisation) may be both exact *and*
   fastest — measure before ruling it out.
3. **Pin the convention with a basis probe, not the docs.** Sign, origin, and
   shift conventions are frequently undocumented or stated for another
   version. `probe_convention(transform, n, {label: predict})` feeds a delta at
   index k and matches the response against candidate closed forms.
4. **Test self-consistency AND truth.** `adjoint_consistency` (or a
   round-trip / symmetry invariant) is necessary but **not sufficient**: a
   forward and adjoint both wrong in the same way pass it perfectly. This is
   the failure this skill exists for — a real backend sat 69% from the correct
   answer while passing its adjoint test at 1e-15, because a consistently
   wrong pair is still a consistent pair.
5. **Benchmark the cross product with `pair_grid`.** Time build and run
   separately (`timed_total`) and report the sum. Backends shuffle work
   between setup and the hot loop, so timing only the inner call ranks them
   wrongly.
6. **Mutation-check the tests.** `mutation_check` seeds one-line faults and
   reports which the suite fails to catch. A green suite is not evidence it
   can fail.

## Attributing the result

When there are two axes — which backend computes the primitive, and what
algorithm runs on top of it — a headline number belongs to the **pair**, not
to either axis. Two traps:

- **The smaller-looking axis may dominate.** Swapping the backend may buy 2x
  while changing the algorithm on top of it buys 30x. `pair_grid` prevents
  attributing the second to the first.
- **A better algorithm is capped by the primitive it runs on.** An exact solve
  converges to the *operator's* error, so a direct method on an approximate
  backend lands on that backend's kernel error and gains nothing, while the
  same method on an exact backend gains orders of magnitude. State the pair.

Write the test that pins each half. If a reader could take the headline figure
for a property of one axis alone, the suite should say otherwise explicitly.

## Shipping it as an engine layer

- **Default to the engine that reproduces the existing behaviour** to
  round-off. A faster default that shifts every existing caller's numbers
  trades their reproducibility for a speedup they did not ask for.
- **Resolve `auto` to a fixed default, not to the fastest installed backend.**
  An answer that changes with the contents of the environment is not
  reproducible across two machines running the same code.
- **Check availability at construction, never at import**, so a minimal
  install keeps working; raise an error naming the extra to install rather
  than letting an `ImportError` escape.
- **Keep the reference in the tree** as an engine, subclassing or delegating
  to the original rather than reimplementing it, so it cannot drift.
- **Document which engines are round-off equivalent and which shift the
  answer**, with the measured figure. "More accurate" is still a change.
- **Regularisation is not cosmetic.** A direct solve of a rank-deficient
  system fails outright; scale the ridge by `trace(B) / n` so it means the
  same thing at every problem size, and report the condition number.

## Reporting

Quote speed and accuracy separately, name the engine each figure belongs to,
and say what hardware timings came from. Ship the benchmark script so figures
can be regenerated rather than copied forward.
