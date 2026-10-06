# Reusable pipeline for temporal interpolation of weather-radar volumes
# by optical-flow advection morphing on native gate geometry.
# See SKILL.md for the workflow. All functions take grid axes explicitly
# (zlev_m, y_m, x_m from a Py-ART Grid) so nothing depends on notebook globals.

import numpy as np

FLOOR_ABS = 10.0  # |floor| reflectivity for non-echo; negated at use (gate: no UnaryOp)

def fetch_arm_volume(stamp, user, token, datastream="sgpcsaprsurI7.00", datadir="data"):
    """Download + extract one ARM Live MDV-tar volume, return a Py-ART Radar.

    stamp: 'YYYYMMDD.HHMMSS' volume END timestamp (as in the ARM filename).
    Requires an ARM Live username + token (https://adc.arm.gov/armlive/).
    adc.arm.gov must be network-allowlisted.
    """
    import os, tarfile, requests, pyart
    os.makedirs(datadir, exist_ok=True)
    tar_name = "%s.%s.mdv.tar" % (datastream, stamp)
    dest = os.path.join(datadir, tar_name)
    if not os.path.exists(dest):
        url = "https://adc.arm.gov/armlive/data/saveData/user/%s:%s/%s" % (user, token, tar_name)
        r = requests.get(url, timeout=600); r.raise_for_status()
        with open(dest, "wb") as f: f.write(r.content)
    with tarfile.open(dest) as tf: tf.extractall(datadir)
    ymd, hms = stamp.split(".")
    return pyart.io.read_mdv(os.path.join(datadir, "sur", ymd, "%s.mdv" % hms))

def volume_midtime(radar):
    """Mean ray time of a volume as a single representative UTC datetime."""
    import datetime
    base = datetime.datetime.strptime(radar.time["units"].split("since")[1].strip(),
                                      "%Y-%m-%dT%H:%M:%SZ")
    return base + datetime.timedelta(seconds=float(np.mean(radar.time["data"])))

def grid_volume(radar, grid_shape=None, grid_limits=None, field="reflectivity"):
    """Grid one volume to a Cartesian stack (Barnes2 / dist_beam). Defaults:
    8 levels 1-8 km, +-120 km, 241x241. Returns a Py-ART Grid."""
    import pyart
    if grid_shape is None: grid_shape = (8, 241, 241)
    if grid_limits is None: grid_limits = ((1000., 8000.), (-120000., 120000.), (-120000., 120000.))
    return pyart.map.grid_from_radars(radar, grid_shape=grid_shape, grid_limits=grid_limits,
                                      fields=[field], weighting_function="Barnes2",
                                      roi_func="dist_beam", min_radius=1000.)

def norm_refl(A, lo=0., hi=60.):
    """Map reflectivity to [0,1] with non-echo at the floor, for optical flow."""
    return (np.clip(np.where(np.isfinite(A), A, -FLOOR_ABS), lo, hi) - lo) / (hi - lo)

def level_displacements(Za, Zb, y_m, x_m, attachment=15, tightness=0.3, num_warp=5, num_iter=10):
    """Per-level ECHO DISPLACEMENT (meters, a->b) as (U_east, V_north), each (z,y,x).

    Uses TV-L1 optical flow. optical_flow_tvl1(moving, reference) returns (v,u)
    mapping reference->moving, so echo displacement a->b is D = -flow.
    """
    from skimage.registration import optical_flow_tvl1
    dy = y_m[1] - y_m[0]; dx = x_m[1] - x_m[0]
    U = np.zeros_like(Za); V = np.zeros_like(Za)
    for kz in range(Za.shape[0]):
        fv, fu = optical_flow_tvl1(norm_refl(Za[kz]), norm_refl(Zb[kz]),
                                   attachment=attachment, tightness=tightness,
                                   num_warp=num_warp, num_iter=num_iter)
        V[kz] = (-fv) * dy
        U[kz] = (-fu) * dx
    return U, V

def build_flow_interpolators(U, V, echo_mask, zlev_m, y_m, x_m):
    """RegularGridInterpolators for east/north displacement over (z,y,x).
    Non-echo cells filled with the per-level mean so the field is defined everywhere."""
    from scipy.interpolate import RegularGridInterpolator
    Uf, Vf = U.copy(), V.copy()
    for kz in range(U.shape[0]):
        for Ff in (Uf, Vf):
            lvl, m = Ff[kz], echo_mask[kz]
            lvl[~m] = lvl[m].mean() if m.any() else 0.0
    kw = dict(bounds_error=False, fill_value=None)
    return (RegularGridInterpolator((zlev_m, y_m, x_m), Uf, **kw),
            RegularGridInterpolator((zlev_m, y_m, x_m), Vf, **kw))

def sweep_sampler(radar, k, field):
    """Return (az_sorted_deg, range_m, values, order) for sweep k."""
    s0, s1 = radar.get_start_end(k)
    az = radar.azimuth["data"][s0:s1 + 1]
    data = np.ma.filled(radar.fields[field]["data"][s0:s1 + 1].astype(float), np.nan)
    order = np.argsort(az)
    return az[order], radar.range["data"], data[order], order

def sample_native(az_q, rng_q, sampler):
    """Bilinear-sample a sweep at query azimuth(deg)/slant-range(m), wrapping azimuth."""
    from scipy.interpolate import RegularGridInterpolator
    az_s, rng_s, vals, _ = sampler
    az_ext = np.concatenate([az_s - 360, az_s, az_s + 360])
    val_ext = np.concatenate([vals, vals, vals], axis=0)
    rgi = RegularGridInterpolator((az_ext, rng_s), val_ext, bounds_error=False, fill_value=np.nan)
    return rgi(np.column_stack([az_q.ravel(), rng_q.ravel()])).reshape(az_q.shape)

def interp_native_volume(rA, rB, fU, fV, alpha, zlev_m, field="reflectivity"):
    """Reconstruct a full volume at fractional time alpha in (0,1) between rA (earlier)
    and rB (later), on rA's native geometry. fU,fV give TOTAL a->b displacement (m)
    as f(z,y,x). Forward-warp sign is +alpha*D (verified end-to-end)."""
    out = np.full((rA.nrays, rA.ngates), np.nan)
    gx_all, gy_all, gz_all = rA.gate_x["data"], rA.gate_y["data"], rA.gate_z["data"]
    zlo, zhi = zlev_m[0], zlev_m[-1]
    for k in range(rA.nsweeps):
        s0, s1 = rA.get_start_end(k)
        elev = np.deg2rad(rA.fixed_angle["data"][k]); ce = max(np.cos(elev), 1e-3)
        gx, gy, gz = gx_all[s0:s1 + 1], gy_all[s0:s1 + 1], gz_all[s0:s1 + 1]
        pts = np.column_stack([np.clip(gz, zlo, zhi).ravel(), gy.ravel(), gx.ravel()])
        Du = fU(pts).reshape(gx.shape); Dv = fV(pts).reshape(gx.shape)
        xa, ya = gx + alpha * Du, gy + alpha * Dv
        xb, yb = gx - (1 - alpha) * Du, gy - (1 - alpha) * Dv
        aza = np.rad2deg(np.arctan2(xa, ya)) % 360; ra = np.hypot(xa, ya) / ce
        azb = np.rad2deg(np.arctan2(xb, yb)) % 360; rb = np.hypot(xb, yb) / ce
        va = sample_native(aza, ra, sweep_sampler(rA, k, field))
        vb = sample_native(azb, rb, sweep_sampler(rB, k, field))
        both = np.isfinite(va) & np.isfinite(vb)
        out[s0:s1 + 1] = np.where(both, (1 - alpha) * va + alpha * vb,
                                  np.where(np.isfinite(va), va, vb))
    return out

def resample_to_geometry(rSrc, rTgt, field="reflectivity"):
    """Sample rSrc onto rTgt's native (az,range) geometry with NO advection
    (fair no-motion baseline for validation)."""
    out = np.full((rTgt.nrays, rTgt.ngates), np.nan)
    gx_all, gy_all = rTgt.gate_x["data"], rTgt.gate_y["data"]
    for k in range(rTgt.nsweeps):
        s0, s1 = rTgt.get_start_end(k)
        elev = np.deg2rad(rTgt.fixed_angle["data"][k]); ce = max(np.cos(elev), 1e-3)
        gx, gy = gx_all[s0:s1 + 1], gy_all[s0:s1 + 1]
        az = np.rad2deg(np.arctan2(gx, gy)) % 360; rng = np.hypot(gx, gy) / ce
        out[s0:s1 + 1] = sample_native(az, rng, sweep_sampler(rSrc, k, field))
    return out

def score_reconstruction(pred, truth, thresh=5.0):
    """Gate-by-gate error of pred vs truth over echo (truth>thresh)."""
    m = np.isfinite(pred) & np.isfinite(truth) & (truth > thresh)
    e = pred[m] - truth[m]
    return {"rmse": float(np.sqrt((e ** 2).mean())), "mae": float(np.abs(e).mean()),
            "bias": float(e.mean()), "cc": float(np.corrcoef(pred[m], truth[m])[0, 1]),
            "n": int(m.sum())}
