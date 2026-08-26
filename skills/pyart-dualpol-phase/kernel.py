"""Sidecar helpers for pyart-dualpol-phase. See SKILL.md."""

import time

KDP_S_BAND_CEILING_DEG_PER_KM = 10.0
LP_ALIASES = ("lp", "phase_proc_lp", "phase_proc_lp_gf", "phase_proc_lp_ref")


def kdp_with_fallback(radar, gatefilter=None, method="vulpiani", band="S",
                      phidp_field=None, **kwargs):
    """Return {'kdp', 'aux', 'method', 'requested', 'seconds', 'note'} for a KDP retrieval.

    Routes around the Py-ART 2.2.5 phase_proc_lp_gf crash (cvxopt returns
    sol['x'] = None on infeasible rays and the extraction loop indexes it
    unguarded): any LP-flavoured request is redirected to kdp_vulpiani and the
    substitution is recorded in 'note'. 'aux' holds the estimator's extra
    outputs (PhiDP reconstruction etc.) when it returns more than one field.
    """
    import pyart

    requested = str(method).lower()
    note = ""
    if requested in LP_ALIASES:
        note = ("phase_proc_lp_gf is broken in Py-ART 2.2.5 (TypeError on "
                "infeasible cvxopt rays); substituted kdp_vulpiani")
        method = "vulpiani"
    else:
        method = requested

    if phidp_field is not None:
        kwargs.setdefault("psidp_field", phidp_field)

    t0 = time.time()
    if method == "vulpiani":
        out = pyart.retrieve.kdp_vulpiani(radar, gatefilter=gatefilter,
                                          band=band, **kwargs)
    elif method == "maesaka":
        out = pyart.retrieve.kdp_maesaka(radar, gatefilter=gatefilter, **kwargs)
    elif method == "schneebeli":
        note = (note + " " if note else "") + (
            "kdp_schneebeli measured at 146 s per sweep gatefiltered and 165 s "
            "unfiltered; the tail is unphysical either way (p99 37.65 and "
            "79.22 deg/km at S band) and needs post-clipping")
        out = pyart.retrieve.kdp_schneebeli(radar, gatefilter=gatefilter,
                                            band=band, **kwargs)
    else:
        raise ValueError(
            "method must be one of vulpiani, maesaka, schneebeli (or an LP "
            "alias, which is redirected); got %r" % (requested,))
    seconds = time.time() - t0

    if isinstance(out, tuple):
        kdp, aux = out[0], out[1:]
    else:
        kdp, aux = out, ()
    return {"kdp": kdp, "aux": aux, "method": method, "requested": requested,
            "seconds": seconds, "note": note}


def kdp_sanity(kdp_dict, band="S"):
    """Return a dict of KDP percentiles plus a physical-plausibility verdict.

    Keys: n_valid, fraction_valid, median, p90, p99, max, ceiling, band,
    plausible, verdict. The S-band ceiling of 10 deg/km is the measured
    anchor (kdp_vulpiani p99 1.19; kdp_schneebeli p99 79.22 unfiltered and
    37.65 with a RhoHV > 0.85 + Z > 5 dBZ gatefilter, same sweep); the C and X
    ceilings are wavelength-scaled from it, not measured.
    """
    import numpy as np

    ceilings = {"S": KDP_S_BAND_CEILING_DEG_PER_KM, "C": 18.0, "X": 31.0}
    key = str(band).upper()[:1]
    if key not in ceilings:
        raise ValueError("band must be S, C or X; got %r" % (band,))
    ceiling = ceilings[key]

    data = kdp_dict["data"] if isinstance(kdp_dict, dict) else kdp_dict
    arr = np.ma.masked_invalid(np.ma.asanyarray(data))
    vals = arr.compressed()
    n_total = int(arr.size)
    n_valid = int(vals.size)
    if n_valid == 0:
        return {"n_valid": 0, "fraction_valid": 0.0, "median": None,
                "p90": None, "p99": None, "max": None, "ceiling": ceiling,
                "band": key, "plausible": False,
                "verdict": "no valid gates - check the gatefilter and the "
                           "PhiDP field passed to the estimator"}

    med = float(np.median(vals))
    p90 = float(np.percentile(vals, 90))
    p99 = float(np.percentile(vals, 99))
    vmax = float(vals.max())
    plausible = p99 <= ceiling
    if not plausible:
        verdict = ("p99 %.2f deg/km exceeds the %s-band ceiling %.0f - phase "
                   "noise survived the gatefilter; tighten QC or clip"
                   % (p99, key, ceiling))
    elif med < 0.001:
        verdict = ("median %.2e deg/km is near zero over %d gates - "
                   "over-smoothed fill rather than retrieval" % (med, n_valid))
    else:
        verdict = "physically plausible for %s band" % key
    return {"n_valid": n_valid,
            "fraction_valid": (n_valid / n_total) if n_total else 0.0,
            "median": med, "p90": p90, "p99": p99, "max": vmax,
            "ceiling": ceiling, "band": key, "plausible": plausible,
            "verdict": verdict}


def attenuation_zphi_named(radar, temp_ref="fixed_fzl", fzl=None,
                           gatefilter=None, **kwargs):
    """Return calculate_attenuation_zphi's six-tuple as a named dict.

    Keys: specific_attenuation, pia, corrected_reflectivity,
    specific_differential_attenuation, pida, corrected_differential_reflectivity,
    plus 'none_entries' listing which came back None (several can, depending on
    temp_ref and which optional fields were supplied) and 'seconds'. Only
    'specific_attenuation' is required downstream by est_rain_rate_a and
    est_rain_rate_hydro. a_coef/beta/c/d default to S-band values - override
    them for C or X.
    """
    import pyart

    if temp_ref == "fixed_fzl" and fzl is None:
        raise ValueError("temp_ref='fixed_fzl' needs fzl in metres")
    t0 = time.time()
    out = pyart.correct.calculate_attenuation_zphi(
        radar, temp_ref=temp_ref, fzl=fzl, gatefilter=gatefilter, **kwargs)
    seconds = time.time() - t0
    names = ("specific_attenuation", "pia", "corrected_reflectivity",
             "specific_differential_attenuation", "pida",
             "corrected_differential_reflectivity")
    res = dict(zip(names, out))
    res["none_entries"] = [k for k in names if res[k] is None]
    res["seconds"] = seconds
    return res


def unfold_phidp_field(radar, phidp_field="differential_phase",
                       fold_below=0.0, offset=360.0, new_field_name=None):
    """Return (field_dict, n_offset) with folded PhiDP gates shifted by +offset.

    Gates below fold_below are treated as wrapped and get offset added; the
    C-SAPR MC3E volume folds this way (values below 0 deg need +360). Operates
    on a copy - the radar object is untouched unless new_field_name is given,
    in which case the copy is also added to the radar. n_offset is the count of
    gates changed; a large fraction of the volume means the threshold is wrong.
    """
    import copy
    import numpy as np

    src = radar.fields[phidp_field]
    out = copy.deepcopy(src)
    data = np.ma.masked_invalid(np.ma.asanyarray(out["data"]))
    folded = (data < fold_below) & ~np.ma.getmaskarray(data)
    n_offset = int(np.count_nonzero(folded))
    data[folded] = data[folded] + offset
    out["data"] = data
    out["comment"] = ("unfolded: %+g applied to %d gates below %g"
                      % (offset, n_offset, fold_below))
    if new_field_name is not None:
        radar.add_field(new_field_name, out, replace_existing=True)
    return out, n_offset
