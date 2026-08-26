"""Helpers for velocity dealiasing with Py-ART (pyart-velocity-dealias)."""

VELOCITY_TEXTURE_WIND_SIZE = 3
VELOCITY_TEXTURE_THRESHOLD = 3.0
NYQUIST_RATIO_SUSPECT = 1.5
NYQUIST_RATIO_FAILED = 3.0
SONDE_FILL_FLOOR_MAGNITUDE = 500.0


def nyquist_summary(radar):
    """Return a dict describing the volume's Nyquist structure and the kwargs it implies.

    Keys: nyquist_min, nyquist_max, uniform (bool), nyquist_vel (scalar or None),
    check_nyquist_uniform (bool), check_nyq_uniform (bool). The last three are ready
    to pass straight to the dealiasers and to calculate_velocity_texture.
    Uniform-Nyquist research radars get a scalar; split-cut NEXRAD volumes get None
    plus the uniformity assertion switched off.
    """
    import numpy

    ip = radar.instrument_parameters or {}
    if "nyquist_velocity" not in ip:
        raise KeyError(
            "no instrument_parameters['nyquist_velocity'] in this volume; "
            "supply nyquist_vel explicitly"
        )
    nyq = numpy.ma.asanyarray(ip["nyquist_velocity"]["data"]).astype(float)
    nyq = nyq.compressed() if hasattr(nyq, "compressed") else nyq
    lo, hi = float(numpy.min(nyq)), float(numpy.max(nyq))
    uniform = lo == hi
    return {
        "nyquist_min": lo,
        "nyquist_max": hi,
        "uniform": uniform,
        "nyquist_vel": lo if uniform else None,
        "check_nyquist_uniform": uniform,
        "check_nyq_uniform": uniform,
    }


def nyquist_ratio(radar, field="corrected_velocity"):
    """Return a dict with max|v|, the Nyquist velocity, their ratio and a verdict string.

    Keys: field, max_abs_velocity, nyquist_max, ratio, verdict, n_valid. verdict is
    'clean' below 1.5x, 'inspect' from 1.5x to 3x, 'qc_leaked' above 3x. A ratio above
    3 means the gate filter let noise bridge two aliased regions; fix the filter and
    re-run rather than post-processing the output.
    """
    import numpy

    if field not in radar.fields:
        raise KeyError("field %r not in radar.fields" % field)
    data = radar.fields[field]["data"]
    valid = numpy.ma.count(data)
    nyq_hi = nyquist_summary(radar)["nyquist_max"]
    max_abs = float(numpy.abs(data).max()) if valid else float("nan")
    ratio = max_abs / nyq_hi if nyq_hi else float("nan")
    if not numpy.isfinite(ratio):
        verdict = "empty"
    elif ratio > NYQUIST_RATIO_FAILED:
        verdict = "qc_leaked"
    elif ratio > NYQUIST_RATIO_SUSPECT:
        verdict = "inspect"
    else:
        verdict = "clean"
    return {
        "field": field,
        "max_abs_velocity": max_abs,
        "nyquist_max": nyq_hi,
        "ratio": ratio,
        "verdict": verdict,
        "n_valid": int(valid),
    }


def mask_above_profile_top(radar, sim_vel, profile_top_m):
    """Return a copy of a simulated-velocity field dict masked above the profile top.

    simulated_vel_from_profile extrapolates without bound above the highest level of
    the wind profile it was given: on an ARM C-SAPR volume 38.9% of gates sat above a
    10.2 km sounding top and were assigned |v| up to 14,080 m/s, with no warning.
    Always route the simulated field through this before using it as ref_vel_field.
    Accepts either the field dict returned by simulated_vel_from_profile or a field
    name already present on the radar.
    """
    import copy

    import numpy

    if isinstance(sim_vel, str):
        sim_vel = radar.fields[sim_vel]
    out = copy.deepcopy(sim_vel)
    above = radar.gate_altitude["data"] > float(profile_top_m)
    out["data"] = numpy.ma.masked_where(above, numpy.ma.asanyarray(out["data"]))
    out["comment"] = (
        "masked where gate_altitude exceeds wind profile top of %.1f m"
        % float(profile_top_m)
    )
    return out


def wind_profile_from_sonde(height_m, u_ms, v_ms):
    """Return (HorizontalWindProfile, profile_top_m) with ARM fill values removed.

    Drops any level where height, u or v is non-finite or below
    -SONDE_FILL_FLOOR_MAGNITUDE
    (-500), which is what fetch_radar_time_profile hands back for ARM -9999 fill.
    Without this the profile inherits -9999 as a wind speed and every downstream
    simulated velocity is nonsense.
    """
    import numpy
    import pyart

    h = numpy.asarray(height_m, dtype=float)
    u = numpy.asarray(u_ms, dtype=float)
    v = numpy.asarray(v_ms, dtype=float)
    good = numpy.isfinite(h) & numpy.isfinite(u) & numpy.isfinite(v)
    floor = -SONDE_FILL_FLOOR_MAGNITUDE
    good &= (h > floor) & (u > floor) & (v > floor)
    if good.sum() < 2:
        raise ValueError("fewer than 2 valid sounding levels after fill masking")
    h, u, v = h[good], u[good], v[good]
    order = numpy.argsort(h)
    profile = pyart.core.HorizontalWindProfile.from_u_and_v(h[order], u[order], v[order])
    return profile, float(h[order][-1])


def velocity_gatefilter(
    radar,
    vel_field="velocity",
    refl_field="reflectivity",
    texture_field="velocity_texture",
    texture_threshold=3.0,
    wind_size=3,
    ncp_min=0.4,
):
    """Return (GateFilter, texture_field_dict) for velocity work, texture criterion included.

    Computes velocity texture on the RAW velocity field with check_nyq_uniform derived
    from the volume (False is required on NEXRAD split cuts, whose per-sweep Nyquist
    varies), adds it to the radar, then builds a filter with the texture criterion in
    place. The texture criterion is the difference between a usable wind field and
    22x-Nyquist garbage; a reflectivity-grade filter is not sufficient for velocity.
    normalized_coherent_power is used only when present - it exists on research radars
    and not on NEXRAD.
    """
    import pyart

    nyq = nyquist_summary(radar)
    texture = pyart.retrieve.calculate_velocity_texture(
        radar,
        vel_field=vel_field,
        wind_size=wind_size,
        check_nyq_uniform=nyq["check_nyq_uniform"],
    )
    radar.add_field(texture_field, texture, replace_existing=True)

    gf = pyart.filters.GateFilter(radar)
    gf.exclude_invalid(vel_field)
    if refl_field in radar.fields:
        gf.exclude_invalid(refl_field)
        gf.exclude_masked(refl_field)
    gf.exclude_above(texture_field, float(texture_threshold))
    if ncp_min is not None and "normalized_coherent_power" in radar.fields:
        gf.exclude_below("normalized_coherent_power", float(ncp_min))
    return gf, texture


def texture_and_dealias(
    radar,
    vel_field="velocity",
    refl_field="reflectivity",
    corr_vel_field="corrected_velocity",
    texture_threshold=3.0,
    wind_size=3,
    ncp_min=0.4,
    ref_vel_field=None,
    method="region",
    add_to_radar=True,
):
    """Return a dict with the dealiased field, the gate filter, and the Nyquist diagnostic.

    Keys: corrected_velocity (field dict), gatefilter, texture (field dict), nyquist
    (nyquist_summary output), diagnostic (nyquist_ratio output when add_to_radar).
    Runs the guarded sequence: texture on raw velocity -> filter including the texture
    criterion -> dealias with that filter passed EXPLICITLY. Never leaves gatefilter
    at None, which would make the dealiaser build a moment-based filter with no
    velocity criterion - the documented catastrophic case. method='region' uses
    dealias_region_based (conservative, the default choice); method='unwrap' uses
    dealias_unwrap_phase (roughly twice as fast, measurably less conservative - it
    reached 2.2x Nyquist on a volume region-based held at 1.0x). Check the returned
    diagnostic['verdict'] before using the output.
    """
    import pyart

    if method not in ("region", "unwrap"):
        raise ValueError("method must be 'region' or 'unwrap'")

    gf, texture = velocity_gatefilter(
        radar,
        vel_field=vel_field,
        refl_field=refl_field,
        texture_threshold=texture_threshold,
        wind_size=wind_size,
        ncp_min=ncp_min,
    )
    nyq = nyquist_summary(radar)
    kwargs = dict(
        gatefilter=gf,
        vel_field=vel_field,
        corr_vel_field=corr_vel_field,
        nyquist_vel=nyq["nyquist_vel"],
        check_nyquist_uniform=nyq["check_nyquist_uniform"],
    )
    if method == "region":
        if ref_vel_field is not None:
            kwargs["ref_vel_field"] = ref_vel_field
        dealiased = pyart.correct.dealias_region_based(radar, centered=True, **kwargs)
    else:
        dealiased = pyart.correct.dealias_unwrap_phase(radar, **kwargs)

    result = {
        "corrected_velocity": dealiased,
        "gatefilter": gf,
        "texture": texture,
        "nyquist": nyq,
        "diagnostic": None,
    }
    if add_to_radar:
        radar.add_field(corr_vel_field, dealiased, replace_existing=True)
        result["diagnostic"] = nyquist_ratio(radar, corr_vel_field)
    return result
