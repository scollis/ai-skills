"""Helpers for validating a swapped numerical backend against a reference."""

import itertools
import os
import re
import subprocess
import sys
import time

MUTATION_PASS_MARKER = "seeded fault NOT caught"


def timed_total(build, run, min_seconds=0.4, warmup=1):
    """Time build and run separately; the honest cost is their sum.

    Backends move work between setup and the hot loop (a plan built in
    microseconds may spend it per call, a precomputed stencil the reverse), so
    timing only the inner call ranks them wrongly. Returns a dict with
    build_s, run_s, total_s and the run count.
    """
    for _ in range(warmup):
        run(build())
    started = time.perf_counter()
    builds = 0
    while time.perf_counter() - started < min_seconds:
        handle = build()
        builds += 1
    build_s = (time.perf_counter() - started) / builds

    handle = build()
    for _ in range(warmup):
        run(handle)
    started = time.perf_counter()
    runs = 0
    while time.perf_counter() - started < min_seconds:
        run(handle)
        runs += 1
    run_s = (time.perf_counter() - started) / runs
    return {
        "build_s": build_s,
        "run_s": run_s,
        "total_s": build_s + run_s,
        "n_build": builds,
        "n_run": runs,
    }


def relative_error(got, want, norm=None):
    """Max absolute deviation scaled by the peak-to-peak range of ``want``.

    Scaling by range rather than by norm keeps the figure comparable across
    fields with different offsets -- a constant field with a large DC term
    would otherwise report a flatteringly small relative error.
    """
    import numpy as np

    got = np.asarray(got)
    want = np.asarray(want)
    if norm is None:
        norm = float(np.ptp(want))
    return float(np.max(np.abs(got - want)) / max(abs(norm), 1e-300))


def three_way_error(candidate, reference, exact):
    """The table that decides whether a backend disagreement is a defect.

    A candidate-vs-reference number alone cannot say who is wrong. Measuring
    both against closed-form ``exact`` output separates the two cases:

    - reference_vs_exact is the REFERENCE's own approximation error, and it is
      the floor on any honest agreement tolerance. No backend can be expected
      to match the reference more closely than the reference matches truth.
    - candidate_vs_exact BELOW reference_vs_exact means the candidate is more
      accurate and the disagreement is the reference's error, not a bug.
    - candidate_vs_exact ABOVE it, or a candidate_vs_reference far larger than
      either, is a real defect (convention, scaling, indexing).
    """
    return {
        "candidate_vs_reference": relative_error(candidate, reference),
        "candidate_vs_exact": relative_error(candidate, exact),
        "reference_vs_exact": relative_error(reference, exact),
    }


def adjoint_consistency(forward, adjoint, shape_in, shape_out, weights=None, seed=0):
    """Relative mismatch of <A u, f>_W against <u, A^H f>; expect ~1e-16.

    NECESSARY BUT NOT SUFFICIENT. A forward and adjoint that are both wrong in
    the same way pass this perfectly -- a consistently wrong pair is still a
    consistent pair. Always pair it with a check against closed-form truth.
    """
    import numpy as np

    rng = np.random.default_rng(seed)
    u = rng.normal(size=shape_in)
    f = rng.normal(size=shape_out)
    w = 1.0 if weights is None else np.asarray(weights).reshape(-1, 1)
    lhs = float(np.sum(np.asarray(forward(u)) * f * w))
    rhs = float(np.sum(u * np.asarray(adjoint(f))))
    return float(abs(lhs - rhs) / max(abs(lhs), abs(rhs), 1e-300))


def probe_convention(transform, n_basis, predictions, atol=1e-8, indices=None):
    """Identify a library's sign/shift convention from unit-basis responses.

    Feed a delta at index k and compare the response against each candidate
    closed form. Cheaper and far more reliable than reading docs: conventions
    (exp(+i) vs exp(-i), fftshift applied or not, 0- vs centre-origin) are
    frequently undocumented or stated for a different version.

    transform: callable taking a length-n_basis unit vector, returning a vector.
    predictions: dict of {label: callable(k) -> expected response}.
    Returns {"match": label or None, "residuals": {label: max_abs_dev}}.
    """
    import numpy as np

    if indices is None:
        indices = [0, 1, n_basis // 2, n_basis - 1]
    residuals = {}
    for label, predict in predictions.items():
        worst = 0.0
        for k in indices:
            basis = np.zeros(n_basis, dtype=complex)
            basis[k] = 1.0
            got = np.asarray(transform(basis)).ravel()
            want = np.asarray(predict(k)).ravel()
            worst = max(worst, float(np.max(np.abs(got - want))))
        residuals[label] = worst
    best = min(residuals, key=residuals.get)
    return {
        "match": best if residuals[best] < atol else None,
        "residuals": residuals,
    }


def mutation_check(source_path, test_command, mutations, cwd=None, timeout=1800):
    """Seed faults into a source file; report which ones the tests fail to catch.

    A test suite that passes is not evidence it can fail. Each mutation is a
    one-line edit that SHOULD break a real behaviour; any that leaves the suite
    green marks either a missing test or -- worth checking before writing one --
    a line that does not actually do anything.

    mutations: list of (label, old_string, new_string). Each old_string must
    appear in the file; the first occurrence is replaced.
    Returns a list of dicts with label, caught (bool) and the summary line.
    """
    path = os.path.join(cwd or ".", source_path) if not os.path.isabs(source_path) else source_path
    original = open(path).read()
    results = []
    try:
        for label, old, new in mutations:
            if old not in original:
                results.append({"label": label, "caught": None,
                                "summary": "old_string not found"})
                continue
            open(path, "w").write(original.replace(old, new, 1))
            proc = subprocess.run(test_command, cwd=cwd, capture_output=True,
                                  text=True, shell=isinstance(test_command, str),
                                  timeout=timeout)
            lines = [ln for ln in proc.stdout.strip().splitlines()
                     if re.search(r"\b(passed|failed|error)\b", ln)]
            summary = lines[-1] if lines else "no summary"
            caught = proc.returncode != 0
            results.append({"label": label, "caught": caught,
                            "summary": summary if caught else
                            summary + "  <-- " + MUTATION_PASS_MARKER})
    finally:
        open(path, "w").write(original)
    return results


def pair_grid(engines, solvers):
    """Every (engine, solver) combination, so neither axis is assumed dominant.

    The axis that looks like the point of the exercise is often not the one
    that matters: swapping the backend may buy 2x while changing the solve
    strategy on top of it buys 30x. Benchmark the cross product before
    attributing a speedup or an accuracy gain to either axis alone.
    """
    return list(itertools.product(engines, solvers))
