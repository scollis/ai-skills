# Helpers for pyart-retrievals: dependency-ordered retrieval staging,
# safe temperature mapping, and product-argument conveniences.

HYDROCLASS_CODES = (
    (0, "NC", "not classified / below thresholds"),
    (1, "AG", "aggregates (dry snow)"),
    (2, "CR", "ice crystals"),
    (3, "LR", "light rain"),
    (4, "RP", "rimed particles / graupel"),
    (5, "RN", "rain"),
    (6, "VI", "vertically oriented ice"),
    (7, "WS", "wet snow (melting layer)"),
    (8, "MH", "melting hail"),
    (9, "IH/HDG", "ice hail / high-density graupel"),
)

RETRIEVAL_STEP_ORDER = ("attenuation", "kdp", "temperature", "classification", "qpe")

SOUNDING_FILL_FLOOR_MAGNITUDE = 500.0


def hydroclass_code_table():
    """Returns a list of (code, abbreviation, meaning) tuples for the
    hydroclass_semisupervised output classes, in Py-ART's own code order."""
    return list(HYDROCLASS_CODES)


def cfad_edges(vmin, vmax, step):
    """Returns a 1-D numpy array of monotonically increasing bin EDGES for
    pyart.retrieve.create_cfad, which rejects [nbins, min, max] triplets."""
    import numpy as np

    if step <= 0:
        raise ValueError("cfad_edges: step must be positive")
    if vmax <= vmin:
        raise ValueError("cfad_edges: vmax must exceed vmin")
    return np.arange(vmin, vmax + 0.5 * step, step, dtype="float64")


def reset_sweep_numbers(radar):
    """Returns the radar with sweep_number['data'] replaced by
    arange(nsweeps); required after extract_sweeps before
    composite_reflectivity or storm_relative_velocity, which index sweeps by
    their stored numbers and raise IndexError('Sweep out of range')."""
    import numpy as np

    radar.sweep_number["data"] = np.arange(radar.nsweeps, dtype="int32")
    return radar


def check_required_fields(radar, needed, step):
    """Returns None when every field name in `needed` is present on `radar`;
    otherwise raises KeyError naming ALL missing fields, the step that wants
    them, and the fields that are present."""
    missing = [f for f in needed if f is not None and f not in radar.fields]
    if missing:
        have = sorted(radar.fields)
        raise KeyError(
            "pyart-retrievals: step '%s' needs %s; missing %s. Present: %s"
            % (step, list(needed), missing, have)
        )
    return None


def as_field_dict(result, key=None):
    """Returns a single Py-ART field dict from a retrieval return value that
    may be a bare field dict, a dict of named field dicts (e.g.
    hydroclass_semisupervised -> {'hydro': ...}), or a tuple whose first
    element is the field dict."""
    if isinstance(result, tuple):
        result = result[0]
    if isinstance(result, dict) and "data" in result:
        return result
    if isinstance(result, dict):
        if key is not None:
            if key not in result:
                raise KeyError(
                    "as_field_dict: no '%s' in returned keys %s"
                    % (key, sorted(result))
                )
            return result[key]
        if len(result) == 1:
            return list(result.values())[0]
        raise KeyError(
            "as_field_dict: ambiguous return, pass key= one of %s" % sorted(result)
        )
    raise TypeError("as_field_dict: unrecognised return type %r" % type(result))


def map_temperature_to_gates(radar, heights_m, temperature_c,
                             field_name="temperature", fill_floor=None):
    """Returns the name of the temperature field added to `radar`, after
    dropping fill values and non-finite levels from the sounding profile.
    Guards the 'cannot reshape array of size 0' ValueError that
    map_profile_to_gates raises on an all-fill profile."""
    import numpy as np
    import pyart

    if fill_floor is None:
        fill_floor = -SOUNDING_FILL_FLOOR_MAGNITUDE
    h = np.ma.filled(np.ma.asarray(heights_m, dtype="float64"), np.nan).ravel()
    t = np.ma.filled(np.ma.asarray(temperature_c, dtype="float64"), np.nan).ravel()
    if h.size != t.size:
        raise ValueError(
            "map_temperature_to_gates: heights (%d) and temperature (%d) differ"
            % (h.size, t.size)
        )
    good = np.isfinite(h) & np.isfinite(t) & (h > fill_floor) & (t > fill_floor)
    if good.sum() < 2:
        raise ValueError(
            "map_temperature_to_gates: only %d valid levels of %d after masking "
            "fill (< %g). The sounding stream is empty at this radar time - "
            "check coverage or use another stream." % (good.sum(), h.size, fill_floor)
        )
    order = np.argsort(h[good])
    # map_profile_to_gates returns a 2-TUPLE (height_dict, field_dict), not one dict
    _height_dict, prof = pyart.retrieve.map_profile_to_gates(
        t[good][order], h[good][order], radar)
    radar.add_field(field_name, prof, replace_existing=True)
    return field_name


def crude_temperature_field(radar, surface_temp_c, lapse_rate_c_per_km=6.5,
                            field_name="temperature", tropopause_m=16000.0,
                            tropopause_temp_drop_c=60.0):
    """Returns the name of a lapse-rate temperature field added to `radar`.

    Testing scaffold only - it has no melting-layer structure and no observed
    profile; do not use it for published QPE or hydrometeor ID. The profile is
    capped at tropopause_m / -tropopause_temp_drop_c because gate_altitude on a
    long-range high-tilt volume reaches >160 km, where an uncapped constant
    lapse rate returns temperatures near -1000 C and silently poisons every
    thermally-gated retrieval downstream."""
    import numpy as np
    import pyart

    base = float(radar.altitude["data"][0])
    # Cap the profile at a tropopause-like height. gate_altitude on a long-range
    # high-tilt volume can exceed 160 km, and a constant lapse rate taken that far
    # gives -1040 C. Below the cap the lapse rate applies; above it, isothermal.
    top = min(float(np.nanmax(radar.gate_altitude["data"])), base + tropopause_m)
    h = np.linspace(base, max(top, base + 1000.0), 200)
    t = surface_temp_c - lapse_rate_c_per_km * (h - base) / 1000.0
    t = np.maximum(t, -tropopause_temp_drop_c)
    # map_profile_to_gates returns a 2-TUPLE (height_dict, field_dict), not one dict
    _height_dict, temp_dict = pyart.retrieve.map_profile_to_gates(t, h, radar)
    temp_dict = dict(temp_dict)
    temp_dict["comment"] = "crude constant-lapse-rate profile, not an observed sounding"
    radar.add_field(field_name, temp_dict, replace_existing=True)
    return field_name


def stage_retrieval_chain(radar, steps=None, refl_field=None, zdr_field=None,
                          rhv_field=None, phidp_field=None, kdp_field=None,
                          temp_field=None, gatefilter=None, fzl=None,
                          radar_freq=None, qpe_method=None,
                          alphakdp=None, betakdp=None, profile=None,
                          hydro_field=None, verbose=True):
    """Returns a dict of {step: [field names added]} after running the
    retrieval chain in dependency order (attenuation -> kdp -> temperature ->
    classification -> qpe), raising a KeyError that names every missing
    prerequisite before the underlying Py-ART call can fail on one of them.
    `profile` is (heights_m, temperature_c) for the temperature step."""
    import pyart

    if steps is None:
        steps = RETRIEVAL_STEP_ORDER
    if refl_field is None:
        refl_field = "reflectivity"
    if zdr_field is None:
        zdr_field = "differential_reflectivity"
    if rhv_field is None:
        rhv_field = "cross_correlation_ratio"
    if phidp_field is None:
        phidp_field = "differential_phase"
    if kdp_field is None:
        kdp_field = "specific_differential_phase"
    if temp_field is None:
        temp_field = "temperature"
    if hydro_field is None:
        hydro_field = "radar_echo_classification"
    if qpe_method is None:
        qpe_method = "hydro"

    bad = [s for s in steps if s not in RETRIEVAL_STEP_ORDER]
    if bad:
        raise ValueError("stage_retrieval_chain: unknown steps %s" % bad)
    steps = [s for s in RETRIEVAL_STEP_ORDER if s in steps]
    added = {}

    for step in steps:
        if step == "attenuation":
            check_required_fields(radar, [refl_field, zdr_field, phidp_field], step)
            if fzl is None and temp_field not in radar.fields:
                raise KeyError(
                    "stage_retrieval_chain: attenuation needs either fzl= "
                    "(temp_ref='fixed_fzl') or a '%s' field on gates "
                    "(temp_ref='temperature'). Run the temperature step first "
                    "if you want the profile-based reference." % temp_field
                )
            out = pyart.correct.calculate_attenuation_zphi(
                radar, refl_field=refl_field, zdr_field=zdr_field,
                phidp_field=phidp_field, temp_field=temp_field,
                temp_ref="fixed_fzl" if fzl is not None else "temperature",
                fzl=fzl, gatefilter=gatefilter,
            )
            names = ["specific_attenuation", "path_integrated_attenuation",
                     "corrected_reflectivity",
                     "specific_differential_attenuation",
                     "path_integrated_differential_attenuation",
                     "corrected_differential_reflectivity"]
            got = []
            for name, fdict in zip(names, out):
                if fdict is not None:
                    radar.add_field(name, fdict, replace_existing=True)
                    got.append(name)
            added[step] = got

        elif step == "kdp":
            if kdp_field in radar.fields:
                added[step] = []
                continue
            check_required_fields(radar, [phidp_field], step)
            kdp, phi_out = pyart.retrieve.kdp_vulpiani(
                radar, gatefilter=gatefilter, phidp_field=phidp_field)
            radar.add_field(kdp_field, as_field_dict(kdp), replace_existing=True)
            added[step] = [kdp_field]

        elif step == "temperature":
            if temp_field in radar.fields:
                added[step] = []
                continue
            if profile is None:
                raise KeyError(
                    "stage_retrieval_chain: temperature step needs profile="
                    "(heights_m, temperature_c) or a '%s' field already on the "
                    "radar. Use crude_temperature_field for a test-only "
                    "stand-in." % temp_field)
            added[step] = [map_temperature_to_gates(
                radar, profile[0], profile[1], field_name=temp_field)]

        elif step == "classification":
            check_required_fields(
                radar, [refl_field, zdr_field, rhv_field, kdp_field, temp_field],
                step)
            kwargs = dict(refl_field=refl_field, zdr_field=zdr_field,
                          rhv_field=rhv_field, kdp_field=kdp_field,
                          temp_field=temp_field)
            if radar_freq is not None:
                kwargs["radar_freq"] = radar_freq
            res = pyart.retrieve.hydroclass_semisupervised(radar, **kwargs)
            radar.add_field(hydro_field, as_field_dict(res, key="hydro"),
                            replace_existing=True)
            added[step] = [hydro_field]

        elif step == "qpe":
            if qpe_method == "hydro":
                check_required_fields(
                    radar, [refl_field, kdp_field, "specific_attenuation",
                            hydro_field], step)
                # est_rain_rate_hydro takes NO kdp_field - it blends Z-R, Z-S and
                # A-R by hydrometeor class. Passing kdp_field raises TypeError.
                rr = pyart.retrieve.est_rain_rate_hydro(
                    radar, refl_field=refl_field,
                    a_field="specific_attenuation", hydro_field=hydro_field,
                    main_field=refl_field, thresh=40.0, thresh_max=True)
            elif qpe_method == "zkdp":
                if alphakdp is None or betakdp is None:
                    raise ValueError(
                        "stage_retrieval_chain: est_rain_rate_zkdp needs "
                        "alphakdp= and betakdp= explicitly; the defaults are "
                        "None and the comparison raises TypeError.")
                check_required_fields(radar, [refl_field, kdp_field], step)
                rr = pyart.retrieve.est_rain_rate_zkdp(
                    radar, refl_field=refl_field, kdp_field=kdp_field,
                    alphakdp=alphakdp, betakdp=betakdp)
            elif qpe_method == "a":
                check_required_fields(radar, ["specific_attenuation"], step)
                rr = pyart.retrieve.est_rain_rate_a(
                    radar, a_field="specific_attenuation")
            elif qpe_method == "kdp":
                check_required_fields(radar, [kdp_field], step)
                rr = pyart.retrieve.est_rain_rate_kdp(radar, kdp_field=kdp_field)
            elif qpe_method == "z":
                check_required_fields(radar, [refl_field], step)
                rr = pyart.retrieve.est_rain_rate_z(radar, refl_field=refl_field)
            else:
                raise ValueError(
                    "stage_retrieval_chain: qpe_method must be one of "
                    "z, kdp, a, zkdp, hydro")
            radar.add_field("rain_rate", as_field_dict(rr),
                            replace_existing=True)
            added[step] = ["rain_rate"]

        if verbose:
            print("%-14s -> %s" % (step, added.get(step)))
    return added
