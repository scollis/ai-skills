"""Kernel helpers for ACT retrievals, corrections and unit/solar utilities."""


def act_sonde_summary(ds, temp='tdry', dewpoint='dp', pressure='pres', rh='rh',
                      wspd='wspd', height='alt', smooth_height=10):
    """Thermodynamic + PBL summary for one ARM radiosonde profile.

    ACT's retrieval functions mutate the dataset they are handed and return that same
    object, so this works on a deep copy and leaves `ds` untouched. Returns
    (summary_dict, augmented_dataset).
    """
    import numpy as np

    import act

    work = ds.copy(deep=True)
    out = {}
    try:
        out['precipitable_water_cm'] = float(
            act.retrievals.calculate_precipitable_water(
                work, temp_name=temp, rh_name=rh, pres_name=pressure
            )
        )
    except Exception as exc:
        out['precipitable_water_cm'] = None
        out['precipitable_water_error'] = f'{type(exc).__name__}: {exc}'
    try:
        work = act.retrievals.calculate_stability_indicies(
            work, temp_name=temp, td_name=dewpoint, p_name=pressure
        )
        for name in ('lifted_index', 'surface_based_cape', 'surface_based_cin',
                     'most_unstable_cape', 'most_unstable_cin',
                     'lifted_condensation_level_temperature',
                     'lifted_condensation_level_pressure'):
            if name in work:
                out[name] = float(np.asarray(work[name].values).ravel()[0])
    except Exception as exc:
        out['stability_error'] = f'{type(exc).__name__}: {exc}'
    try:
        work = act.retrievals.calculate_pbl_liu_liang(
            work, temperature=temp, pressure=pressure, windspeed=wspd,
            height=height, smooth_height=smooth_height,
        )
        out['pblht_liu_liang_m'] = float(work['pblht_liu_liang'].values)
        out['pbl_regime'] = str(work['pblht_regime_liu_liang'].values)
    except Exception as exc:
        out['pbl_liu_liang_error'] = f'{type(exc).__name__}: {exc}'
    try:
        work = act.retrievals.calculate_pbl_heffter(
            work, temperature=temp, pressure=pressure, height=height,
            smooth_height=smooth_height,
        )
        out['pblht_heffter_m'] = float(work['pblht_heffter'].values)
    except Exception as exc:
        out['pbl_heffter_error'] = f'{type(exc).__name__}: {exc}'
    return out, work


def act_retrieval_safe(func, ds, **kwargs):
    """Run any ACT retrieval on a deep copy so the caller's dataset is not mutated."""
    return func(ds.copy(deep=True), **kwargs)


def act_convert_units(ds, variables=None, desired_unit=None, **kwargs):
    """Convert variables to `desired_unit` in place via the `.utils` accessor.

    Uses each variable's `units` attribute, so a variable with a missing or
    non-udunits string is skipped rather than silently mis-scaled.
    """
    return ds.utils.change_units(variables=variables, desired_unit=desired_unit, **kwargs)


def act_solar_geometry(ds, lat_name='lat', lon_name='lon'):
    """Add a day/night flag plus solar elevation/azimuth, and return sunrise/noon/sunset.

    `add_solar_variable` documents latitude/longitude as str but indexes them as
    `latitude[0]`, so it needs a LIST of variable names; a bare 'lat' becomes 'l'
    and a float raises "'float' object is not subscriptable".
    """
    import numpy as np

    import act

    latitude = float(np.asarray(ds[lat_name].values).ravel()[0])
    longitude = float(np.asarray(ds[lon_name].values).ravel()[0])
    ds = act.utils.add_solar_variable(ds, latitude=[lat_name], longitude=[lon_name])
    elev, az, _ = act.utils.get_solar_azimuth_elevation(
        latitude=latitude, longitude=longitude, time=ds['time'].values
    )
    ds['solar_elevation'] = ('time', np.asarray(elev))
    ds['solar_azimuth'] = ('time', np.asarray(az))
    day = str(np.asarray(ds['time'].values).ravel()[0])[:10].replace('-', '')
    sunrise, sunset, noon = act.utils.get_sunrise_sunset_noon(latitude, longitude, day)
    return ds, {'sunrise': sunrise, 'solar_noon': noon, 'sunset': sunset,
                'latitude': latitude, 'longitude': longitude}
