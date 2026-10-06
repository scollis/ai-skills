---
name: act-retrievals
description: Derive geophysical quantities from ARM data with ACT (act-atmos) - radiosonde precipitable water, CAPE/CIN/lifted index and Liu-Liang or Heffter boundary-layer height, lidar PBL gradient methods and Sobel cloud base, Doppler-lidar VAD winds, AERI brightness temperature, radiation products, instrument corrections (ceilometer, MPL, Doppler and Raman lidar, ship-motion wind), and unit, solar-geometry and precipitation-accumulation utilities. Use whenever an ARM sounding needs thermodynamic indices or a PBL height, a lidar profile needs cloud base or mixing height, radiation components need combining, or backscatter needs range correction. Triggers - ACT retrievals, precipitable water, PWV, CAPE, CIN, lifted index, LCL, stability indices, PBL height, boundary layer height, Liu-Liang, Heffter, mixing height, sobel cloud base, correct_ceil, correct_mpl, Doppler lidar winds, VAD, aeri2irt, net radiation, accumulate_precip, convert_units, potential temperature, solar elevation, sunrise sunset.
---

# Retrievals, corrections and utilities in ACT

The derived-quantity half of ACT. Companions: `act-arm-live` (data in), `act-qc`
(screen before you retrieve), `act-plotting` (show the result). Run in an env with
`act-atmos` installed.

## The one behaviour that surprises everyone

**ACT retrievals mutate the dataset you hand them and return that same object.**

```python
ds2 = act.retrievals.calculate_stability_indicies(ds, temp_name="tdry", ...)
ds2 is ds          # True — `ds` now carries the new variables too
```

Chaining several retrievals accumulates variables in one dataset, which is convenient
until you wanted the original untouched — or until you loop over soundings reusing a
variable name and the second pass sees the first pass's output. Work on
`ds.copy(deep=True)`, or use `act_retrieval_safe(func, ds, **kwargs)`.

Screen with `act-qc` *before* retrieving. A CAPE computed through a flagged
temperature profile is a number with no meaning attached.

## Radiosondes

`act_sonde_summary(ds)` returns `(summary_dict, augmented_dataset)` on a copy, running
the three sonde retrievals in one call:

```python
summary, aug = act_sonde_summary(sonde)
# {'precipitable_water_cm': 3.15, 'lifted_index': -5.63,
#  'surface_based_cape': 2164.35, 'surface_based_cin': 0.0,
#  'most_unstable_cape': 2164.35, 'most_unstable_cin': 0.0,
#  'lifted_condensation_level_temperature': 15.23,
#  'lifted_condensation_level_pressure': 831.15,
#  'pblht_liu_liang_m': 1640.5, 'pbl_regime': 'NRL', 'pblht_heffter_m': 1593.8}
```

The underlying calls, on ARM `sondewnpn` variable names:

- `calculate_precipitable_water(ds, temp_name='tdry', rh_name='rh', pres_name='pres')`
  -> a float in **cm**, not mm.
- `calculate_stability_indicies(ds, temp_name='tdry', td_name='dp', p_name='pres',
  moving_ave_window=0)` -> adds `lifted_index`, `surface_based_cape`/`_cin`,
  `most_unstable_cape`/`_cin`, `lifted_condensation_level_temperature`/`_pressure`.
  It takes no `rh_name`; it wants dewpoint. MetPy warns "Interpolation point out of
  data bounds" when a profile never reaches the LFC.
- `calculate_pbl_liu_liang(ds, temperature='tdry', pressure='pres', windspeed='wspd',
  height='alt', smooth_height=3, land_parameter=True, llj_max_alt=1500, llj_max_wspd=2)`
  -> `pblht_liu_liang` (m) plus `pblht_regime_liu_liang`, a regime label: `SBL`
  (stable), `CBL` (convective), `NRL` (neutral residual). The regime is as informative
  as the height — a nocturnal SBL of 600 m and an afternoon CBL of 1600 m from the
  same site are not comparable numbers.
- `calculate_pbl_heffter(ds, temperature='tdry', pressure='pres', height='alt',
  base=5.0)` -> `pblht_heffter` plus the `bottom_inversion`/`top_inversion` it keyed on.

Heffter and Liu-Liang disagree routinely; quoting both, as `act_sonde_summary` does,
is the honest presentation.

## Lidar, ceilometer and radar wind profiles

- `act.retrievals.generic_sobel_cbh(ds, variable=..., height_dim=..., var_thresh=...,
  edge_thresh=5.0, filter_type='uniform')` — Sobel edge detection for cloud base from
  any backscatter-like 2-D field.
- `act.retrievals.calculate_gradient_pbl(ds, parm='beta_att', dis_parm='range',
  min_height=100, smooth_dis=5)` and `calculate_modified_gradient_pbl(...,
  threshold=0.001)` — mixing height from attenuated backscatter gradients. (ACT's
  development branch adds wavelet, Tucker and profile-fit PBL methods; check
  `dir(act.retrievals.pbl_lidar)` for what your installed version actually has —
  2.3.4 ships only the two gradient methods.)
- `act.retrievals.compute_winds_from_ppi(ds, elevation_name='elevation',
  azimuth_name='azimuth', radial_velocity_name='radial_velocity',
  snr_name='signal_to_noise_ratio', snr_threshold=0.008)` — VAD winds from a
  Doppler-lidar PPI.

## Radiation and radiometry

- `calculate_net_radiation(ds, ush='up_short_hemisp', ulh='up_long_hemisp',
  dsh='down_short_hemisp', dlhs='down_long_hemisp_shaded', smooth=None)`
- `calculate_dsh_from_dsdh_sdn(ds, dsdh='down_short_diffuse_hemisp',
  sdn='short_direct_normal')` — reconstruct global horizontal from diffuse + direct
  normal, the standard consistency check on a radiometer triplet.
- `calculate_longwave_radiation(ds, temperature_var=..., vapor_pressure_var=...,
  met_ds=..., emiss_a=0.61, emiss_b=0.06)` — empirical clear-sky downwelling LW.
- `calculate_irradiance_stats(ds, variable, variable2, threshold=...)` — difference
  and ratio series between two irradiance measurements.
- `aeri2irt(aeri_ds, wnum_name='wnum', rad_name='mean_rad', hatch_name='hatchOpen')` —
  AERI spectral radiance to IRT-equivalent brightness temperature.
- `sst_from_irt(ds, sky_irt='sky_ir_temp', sfc_irt='sfc_ir_temp', emis=0.986)`.
- `act.utils.planck_converter(wnum=..., radiance=...)` — radiance <-> brightness
  temperature either direction (supply whichever of `radiance`/`temperature` you have).

SP2 black-carbon processing (`calc_sp2_diams_masses`, `process_sp2_psds`) needs the
optional `pysp2` package.

## Instrument corrections

All take the dataset and a variable name, and add a `*_corrected` style variable:

- `correct_ceil(ds, fill_value=1e-07, var_name='backscatter')` — log-scale the
  ceilometer backscatter and floor the zeros that would otherwise become `-inf`.
- `correct_dl(ds, var_name='attenuated_backscatter', range_normalize=True)` — Doppler
  lidar range correction.
- `correct_rl(ds, var_name='depolarization_counts_high')` — Raman lidar.
- `correct_mpl(ds, ...)` — micropulse lidar: afterpulse, overlap and range correction
  in one call; it needs the full set of calibration variables named in its signature.
- `correct_wind_for_ship_motion(ds, wspd_name, wdir_name, heading_name='yaw',
  cog_name='course_over_ground', sog_name='speed_over_ground')` — remove platform
  motion from shipborne winds, with `act.utils.calc_cog_sog` to derive course and
  speed over ground if the file lacks them.

## Utilities that save real work

```python
act_convert_units(ds, variables="temp_mean", desired_unit="degF")   # ds.utils accessor
ds, sun = act_solar_geometry(ds)   # sun_variable, solar_elevation, solar_azimuth + sunrise/noon/sunset
ds = act.utils.accumulate_precip(ds, "tbrg_precip_total")           # adds *_accumulated
```

- `act.utils.convert_units` / the `ds.utils.change_units` accessor use each variable's
  `units` attribute, so a variable with a missing or non-udunits string is skipped
  rather than mis-scaled.
- `add_solar_variable` documents `latitude`/`longitude` as `str` but indexes them as
  `latitude[0]` — pass a **list** of variable names (`latitude=['lat']`) or leave them
  `None` for auto-discovery. A bare string silently becomes its first character and a
  float raises `'float' object is not subscriptable`. `act_solar_geometry` handles it.
- `get_solar_azimuth_elevation(latitude, longitude, time)` returns
  `(elevation, azimuth, distance)` — elevation first.
- `get_sunrise_sunset_noon(lat, lon, 'YYYYMMDD')` -> arrays of datetimes;
  `is_sun_visible(...)` -> boolean per timestamp.
- `decode_present_weather(ds, variable='pwd_pw_code_inst')` — WMO present-weather
  codes to text, for the `pwd_*` variables in ARM met files.
- `convert_to_potential_temp`, `height_adjusted_temperature`,
  `height_adjusted_pressure` — thermodynamic adjustments to a reference height.
- `ts_weighted_average`, `convert_2d_to_1d`, `calculate_percentages`,
  `add_in_nan` (insert NaN across gaps so plotted lines break),
  `adjust_timestamp(ds, align='left'|'right'|'center')` for averaged-interval
  timestamps, `destination_azimuth_distance`, `generate_movie`.
- `act.utils.dates_between`, `date_parser`, `determine_time_delta`,
  `reduce_time_ranges` for date bookkeeping.

## Kernel helpers

- `act_sonde_summary(ds, temp='tdry', dewpoint='dp', pressure='pres', rh='rh', wspd='wspd', height='alt')` -> `(summary_dict, augmented_dataset)`, non-mutating
- `act_retrieval_safe(func, ds, **kwargs)` -> run any ACT retrieval on a deep copy
- `act_convert_units(ds, variables=None, desired_unit=None)`
- `act_solar_geometry(ds, lat_name='lat', lon_name='lon')` -> `(ds, {'sunrise','solar_noon','sunset','latitude','longitude'})`

Each retrieval failure in `act_sonde_summary` is caught and reported as an
`*_error` key rather than aborting the whole summary, so a profile that is too short
for CAPE still yields its PBL heights.
