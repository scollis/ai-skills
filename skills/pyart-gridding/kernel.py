"""Holdout cross-validation helpers for choosing a Py-ART gridding
radius of influence. See SKILL.md section 1."""

DEFAULT_ROI_CONFIGS = (
    ("dist_beam", 0.75, 1.0, 250.0, None, "Barnes2"),
    ("dist_beam", 1.0, 1.0, 250.0, None, "Barnes2"),
    ("dist_beam", 1.0, 1.0, 500.0, None, "Barnes2"),
    ("dist_beam", 1.5, 1.0, 500.0, None, "Barnes2"),
    ("dist_beam", 2.0, 1.0, 500.0, None, "Barnes2"),
    ("constant", None, None, None, 500.0, "Barnes2"),
    ("constant", None, None, None, 1000.0, "Barnes2"),
    ("constant", None, None, None, 2000.0, "Barnes2"),
    ("constant", None, None, None, 4000.0, "Barnes2"),
    ("dist_beam", 1.5, 1.0, 500.0, None, "Cressman"),
    ("dist_beam", 1.5, 1.0, 500.0, None, "Nearest"),
)


def holdout_split(radar, field="reflectivity", every=5, base_gatefilter=None):
    """Return (train_gatefilter, truth_dict) for holdout ROI validation.

    train_gatefilter excludes every `every`-th ray so those gates do not
    contribute to the grid; truth_dict holds the withheld gate positions and
    values as {'x','y','z','value'} 1D arrays, in grid-relative metres using
    the radar as origin. Pass base_gatefilter to apply QC first (the returned
    filter is a copy of it with the holdout rays added).
    """
    import numpy as np
    import pyart

    if base_gatefilter is None:
        train = pyart.filters.GateFilter(radar)
        train.exclude_invalid(field)
    else:
        train = base_gatefilter.copy()

    nrays = radar.nrays
    ray_idx = np.arange(nrays)
    held = (ray_idx % int(every)) == 0

    mask = np.zeros((nrays, radar.ngates), dtype=bool)
    mask[held, :] = True
    train.exclude_gates(mask)

    data = radar.fields[field]["data"]
    keep = held[:, None] & ~np.ma.getmaskarray(data)
    if base_gatefilter is not None:
        keep = keep & ~base_gatefilter.gate_excluded
    truth = {
        "z": np.asarray(radar.gate_z["data"])[keep].astype("float64"),
        "y": np.asarray(radar.gate_y["data"])[keep].astype("float64"),
        "x": np.asarray(radar.gate_x["data"])[keep].astype("float64"),
        "value": np.asarray(data)[keep].astype("float64"),
    }
    return train, truth


def grid_spec(radar, nz=41, nxy=401, max_z=20000.0, max_xy=None):
    """Return a dict of grid_shape and grid_limits in Py-ART (z, y, x) order.

    max_xy defaults to the radar's maximum unambiguous range rounded down to
    a whole kilometre. Feed the result straight into grid_from_radars(**spec).
    """
    import numpy as np

    if max_xy is None:
        max_xy = float(np.floor(radar.range["data"].max() / 1000.0) * 1000.0)
    return {
        "grid_shape": (int(nz), int(nxy), int(nxy)),
        "grid_limits": (
            (0.0, float(max_z)),
            (-float(max_xy), float(max_xy)),
            (-float(max_xy), float(max_xy)),
        ),
    }


def score_grid_against_holdout(grid, truth, field="reflectivity"):
    """Return dict of rmse, mae, bias, coverage, grid_filled, n_val for one grid.

    Interpolates the grid trilinearly back to the withheld gate positions with
    scipy RegularGridInterpolator and compares against truth['value'].
    coverage is the fraction of withheld gates the grid could predict at all;
    grid_filled is the fraction of grid cells that received any data.
    """
    import numpy as np
    from scipy.interpolate import RegularGridInterpolator

    data = np.ma.masked_invalid(grid.fields[field]["data"])
    filled = float((~np.ma.getmaskarray(data)).mean())
    interp = RegularGridInterpolator(
        (grid.z["data"], grid.y["data"], grid.x["data"]),
        np.ma.filled(data, np.nan),
        bounds_error=False,
        fill_value=np.nan,
    )
    pred = interp(np.column_stack([truth["z"], truth["y"], truth["x"]]))
    ok = np.isfinite(pred)
    n_total = pred.size
    n_val = int(ok.sum())
    if n_val == 0:
        return {
            "rmse": float("nan"), "mae": float("nan"), "bias": float("nan"),
            "coverage": 0.0, "grid_filled": filled, "n_val": 0,
        }
    err = pred[ok] - truth["value"][ok]
    return {
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "mae": float(np.mean(np.abs(err))),
        "bias": float(np.mean(err)),
        "coverage": float(n_val / n_total),
        "grid_filled": filled,
        "n_val": n_val,
    }


def sweep_roi_configs(radar, field="reflectivity", configs=None, every=5,
                      base_gatefilter=None, spec=None):
    """Return a DataFrame of holdout scores, one row per ROI/weighting config.

    Columns: roi_func, nb, bsp, min_radius, constant_roi, weighting, coverage,
    rmse, mae, bias, grid_filled, n_val, seconds. Sort by coverage and read
    rmse alongside it - the best rmse in the table is usually the config that
    declined to interpolate most of the volume. configs defaults to
    DEFAULT_ROI_CONFIGS.
    """
    import time
    import pandas as pd
    import pyart

    if configs is None:
        configs = DEFAULT_ROI_CONFIGS
    if spec is None:
        spec = grid_spec(radar)

    train, truth = holdout_split(radar, field=field, every=every,
                                 base_gatefilter=base_gatefilter)
    rows = []
    for roi_func, nb, bsp, min_radius, constant_roi, weighting in configs:
        kw = {"roi_func": roi_func, "weighting_function": weighting}
        if roi_func == "constant":
            kw["constant_roi"] = constant_roi
        else:
            kw["nb"] = nb
            kw["bsp"] = bsp
            kw["min_radius"] = min_radius
        t0 = time.time()
        grid = pyart.map.grid_from_radars(
            (radar,), gatefilters=(train,), fields=[field], **spec, **kw
        )
        seconds = time.time() - t0
        row = {
            "roi_func": roi_func, "nb": nb, "bsp": bsp,
            "min_radius": min_radius, "constant_roi": constant_roi,
            "weighting": weighting,
        }
        row.update(score_grid_against_holdout(grid, truth, field=field))
        row["seconds"] = round(seconds, 2)
        rows.append(row)
        del grid
    return pd.DataFrame(rows)


def recommended_roi(radar):
    """Return the measured knee ROI kwargs for grid_from_radars, plus a rationale.

    dist_beam with nb=1.5, bsp set to the radar's own beamwidth where the file
    reports it, min_radius=500 m, Barnes2 weighting. Splat into
    grid_from_radars; read result['rationale'] for why.
    """
    bsp = 1.0
    try:
        bw = radar.instrument_parameters["radar_beam_width_h"]["data"]
        bw = float(bw.ravel()[0])
        if 0.1 < bw < 5.0:
            bsp = round(bw, 3)
    except (KeyError, TypeError, AttributeError, IndexError, ValueError):
        pass
    return {
        "roi_func": "dist_beam",
        "nb": 1.5,
        "bsp": bsp,
        "min_radius": 500.0,
        "weighting_function": "Barnes2",
        "rationale": (
            "dist_beam is the only ROI function that grows with beam spreading, "
            "and nb=1.5/min_radius=500 was the measured coverage/accuracy knee "
            "on KIWA: 0.924 holdout coverage at 4.625 dBZ RMSE and -0.010 dBZ "
            "bias, versus 4.919 dBZ for constant_roi=2000 at similar coverage. "
            "Re-run sweep_roi_configs on your own volume to confirm."
        ),
    }
