"""Helpers for ARM C-SAPR2 (and similar CfRadial) dual-pol calibration work.

Every reader here slices ONE sweep's contiguous ray block rather than loading a
volume, because ARM C-SAPR2 PPI volumes are ~700 MB each and a multi-hundred-file
pass is otherwise impossible on a laptop.
"""
import os
import numpy as np

UNTHRESHOLDED_FIELDS = ("uncorrected_reflectivity_h", "uncorrected_reflectivity_v",
                        "uncorrected_differential_reflectivity")
EARTH_R = 6371000.0


def sweep_bounds(ds, sweep=0):
    """Ray index bounds for one sweep, CLAMPED to the rays actually present.

    ARM splits volumes at UTC midnight, leaving files whose sweep_start/end_ray_index
    describe a full volume template while only a fraction of the rays exist. Slicing
    by the declared index then silently returns a different (higher) elevation, which
    masquerades as a sensitivity collapse. Returns (s0, s1, truncated).
    """
    ss = np.asarray(ds.variables["sweep_start_ray_index"][:]).astype(int).ravel()
    se = np.asarray(ds.variables["sweep_end_ray_index"][:]).astype(int).ravel()
    n_actual = ds.variables["elevation"].shape[0]
    n_declared = int(se[-1]) + 1
    s0 = int(ss[sweep])
    s1 = min(int(se[sweep]), n_actual - 1)
    return s0, s1, bool(n_actual < n_declared)


def read_sweep(path, sweep=0, fields=("reflectivity",), check_elevation=True,
               el_tol=0.5):
    """Read one sweep's fields as float32 with NaN fill. Memory-lean.

    check_elevation raises when the sliced rays' median elevation disagrees with the
    declared fixed_angle -- the signature of a truncated split file.
    """
    import netCDF4
    out = {}
    with netCDF4.Dataset(path) as ds:
        s0, s1, truncated = sweep_bounds(ds, sweep)
        if s1 < s0:
            raise ValueError("sweep %d absent from %s" % (sweep, os.path.basename(path)))
        fa = float(np.asarray(ds.variables["fixed_angle"][:]).ravel()[sweep])
        el = np.asarray(ds.variables["elevation"][s0:s1 + 1], "f4")
        el_med = float(np.median(el))
        if check_elevation and abs(el_med - fa) > el_tol:
            raise ValueError(
                "%s sweep %d: rays sit at %.2f deg but fixed_angle says %.2f deg "
                "-- truncated/split file" % (os.path.basename(path), sweep, el_med, fa))
        out["azimuth"] = np.asarray(ds.variables["azimuth"][s0:s1 + 1], "f4")
        out["elevation"] = el
        out["range"] = np.asarray(ds.variables["range"][:], "f4")
        out["fixed_angle"] = fa
        out["truncated"] = truncated
        out["n_rays"] = s1 - s0 + 1
        for f in fields:
            if f in ds.variables:
                out[f] = np.ma.filled(
                    ds.variables[f][s0:s1 + 1, :].astype("f4"), np.nan)
            else:
                out[f] = np.full((s1 - s0 + 1, len(out["range"])), np.nan, "f4")
    return out


def signal_mask(snr, ncp, snr_min=10.0, ncp_min=0.3):
    """Gates carrying real signal. REQUIRED before trusting any unthresholded field.

    Without this, no-signal gates (Doppler pegged at Nyquist, spectral width
    saturated, NCP~0) present as 50-60 dBZ of pure noise.
    """
    return np.isfinite(snr) & np.isfinite(ncp) & (snr > snr_min) & (ncp > ncp_min)


def grid_rays_to_azimuth(azimuth, values, n_az=360):
    """NaN-aware average of rays into fixed azimuth bins -> (n_az, n_range), counts."""
    n_r = values.shape[1]
    ab = np.mod(np.floor(azimuth).astype(np.int64), n_az)
    good = np.isfinite(values)
    s = np.zeros((n_az, n_r), "f8")
    c = np.zeros((n_az, n_r), "f8")
    np.add.at(s, ab, np.where(good, values, 0.0))
    np.add.at(c, ab, good.astype("f8"))
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(c > 0, s / np.maximum(c, 1), np.nan)
    return out.astype("f4"), c


def first_valid_gate(field2d, min_frac=0.5):
    """Index of the first range gate with data, i.e. past the T/R blanking."""
    frac = np.isfinite(field2d).mean(axis=0)
    idx = int(np.argmax(frac > min_frac))
    return idx if frac[idx] > min_frac else -1


def beam_height(range_m, elevation_deg, radar_alt_m=0.0):
    """4/3-earth beam-centre height in metres MSL."""
    r = np.asarray(range_m, dtype="f8")
    ke = 4.0 / 3.0 * EARTH_R
    return (np.sqrt(r ** 2 + ke ** 2
                    + 2.0 * r * ke * np.sin(np.radians(elevation_deg)))
            - ke + radar_alt_m)


def ground_range_azimuth(lat0, lon0, lat1, lon1):
    """Great-circle distance (m) and forward azimuth (deg) from point 0 to point 1."""
    p1, p2 = np.radians(lat0), np.radians(lat1)
    dl = np.radians(lon1 - lon0)
    d = 2.0 * EARTH_R * np.arcsin(np.sqrt(
        np.sin((p2 - p1) / 2.0) ** 2
        + np.cos(p1) * np.cos(p2) * np.sin(dl / 2.0) ** 2))
    brg = np.degrees(np.arctan2(
        np.sin(dl) * np.cos(p2),
        np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl))) % 360.0
    return float(d), float(brg)


def phidp_system_offset(phidp, rng_m, snr, ncp, rhohv, max_range_m=15000.0,
                        rhohv_min=0.98):
    """Per-volume PhiDP system offset from clean near-range rain, WRAP-SAFE.

    This offset drifts between volumes, so solve it per volume before applying any
    absolute PhiDP threshold. Observed range across a single site: -9 to +38 deg --
    do NOT reuse one date's value as a constant.

    Uses a CIRCULAR mean, not a plain median, because the offset can sit just below
    zero and wrap. When it does, PhiDP is bimodal at 0/360 and a plain median returns
    ~352 deg -- meaningless, and it silently corrupts any absolute PhiDP threshold.
    (Real case, this function's own default window: 4430 clean gates split 1083 in the
    0-10 deg bin and 2269 in the 350-360 deg bin of a single volume; the plain median
    returns 350.24 deg while the circular mean gives -0.03 deg.)

    Returns degrees in (-180, 180].
    """
    near = rng_m < max_range_m
    m = (signal_mask(snr, ncp) & (rhohv > rhohv_min)
         & np.isfinite(phidp) & near[None, :])
    if m.sum() < 50:
        return float("nan")
    a = np.radians(np.asarray(phidp)[m])
    return float(np.degrees(np.arctan2(np.mean(np.sin(a)), np.mean(np.cos(a)))))


def mad_sigma(x):
    """Robust sigma: 1.4826 * median absolute deviation. Report alongside std."""
    a = np.asarray(x, dtype="f8")
    a = a[np.isfinite(a)]
    if a.size == 0:
        return float("nan")
    return float(1.4826 * np.median(np.abs(a - np.median(a))))


def dpr_overpass_time(dpr_lat, dpr_lon, dpr_time, site_lat, site_lon,
                      max_dist_km=115.0):
    """Closest approach and in-domain window for a GPM DPR granule.

    Guards the indexing trap: lat/lon are (cross_track, along_track) while `time`
    is indexed by ALONG-TRACK only, so the overpass time must be read with the
    along-track index. Using the cross-track index can be tens of minutes wrong.
    """
    lat = np.asarray(dpr_lat)
    lon = np.asarray(dpr_lon)
    t = np.asarray(dpr_time)
    if lat.ndim != 2:
        raise ValueError("expected 2-D (cross_track, along_track) lat/lon")
    ax_along = 1 if lat.shape[1] == t.shape[0] else 0
    d = np.hypot((lat - site_lat) * 111.0,
                 (lon - site_lon) * 111.0 * np.cos(np.radians(site_lat)))
    i, j = np.unravel_index(np.nanargmin(d), d.shape)
    j_along = j if ax_along == 1 else i
    inr = d < max_dist_km
    jj = np.where(inr.any(axis=0 if ax_along == 1 else 1))[0]
    return dict(min_dist_km=float(d[i, j]),
                idx_cross=int(i if ax_along == 1 else j),
                idx_along=int(j_along), time_closest=t[j_along],
                n_footprints_in_domain=int(inr.sum()),
                along_first=int(jj.min()) if jj.size else -1,
                along_last=int(jj.max()) if jj.size else -1,
                time_first=t[jj.min()] if jj.size else None,
                time_last=t[jj.max()] if jj.size else None)
