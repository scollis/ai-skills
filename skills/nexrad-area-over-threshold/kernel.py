import math

# Imperial rainfall intensity bins (in/hr) and the mm<->in conversion.
RAIN_THRESHOLDS_IN = [0.25, 0.5, 1.0, 2.0, 3.0]
MM_PER_IN = 25.4


def area_over_thresholds(radar, extent, thresholds_in=None, rhohv_min=0.85,
                         dbz_min=5.0, hail_cap=53.0, zr_a=200.0, zr_b=1.6):
    """Domain area (km^2) exceeding each rain-rate threshold on the 0.5 deg sweep.

    Converts reflectivity to rain rate with Marshall-Palmer (Z = zr_a * R**zr_b),
    both hail-capped (dBZ clipped at hail_cap before Z->R) and uncapped, keeps
    gates passing a dual-pol filter (rhoHV >= rhohv_min, Z >= dbz_min) inside the
    lon/lat `extent`, and sums each gate's POLAR cell area (dr * r*dphi). Polar
    cells tile the sweep without overlap, so no Cartesian regridding is needed.

    extent = [lon_min, lon_max, lat_min, lat_max].
    thresholds_in : list of thresholds in in/hr (default RAIN_THRESHOLDS_IN).
    Returns dict: area_cap_<t>, area_raw_<t> (km^2) for each threshold, plus
    domain_area_km2 (total area with any rain >= dbz_min). Keys use str(t), e.g.
    'area_cap_0.25', 'area_cap_1.0'.
    """
    import numpy as np
    import numpy.ma as ma
    if thresholds_in is None:
        thresholds_in = RAIN_THRESHOLDS_IN
    thresh_mm = [t * MM_PER_IN for t in thresholds_in]
    sweep0 = radar.extract_sweeps([0])
    lons = sweep0.gate_longitude["data"]; lats = sweep0.gate_latitude["data"]
    rng = sweep0.range["data"]; az = sweep0.azimuth["data"]
    dbz = sweep0.fields["reflectivity"]["data"]
    rho = sweep0.fields["cross_correlation_ratio"]["data"]
    # per-gate polar cell area (km^2): range-gate depth * arc length (r*dphi)
    dr = float(np.median(np.diff(rng)))
    daz = np.abs(np.gradient(np.unwrap(np.deg2rad(az))))
    daz = np.clip(daz, 0, np.deg2rad(2.0))            # guard azimuth-wrap spikes
    R2, A2 = np.meshgrid(rng, daz)
    cell_area_km2 = (dr * (R2 * A2)) / 1e6
    lon0, lon1, lat0, lat1 = extent
    indomain = (lons >= lon0) & (lons <= lon1) & (lats >= lat0) & (lats <= lat1)
    good = (indomain & ~ma.getmaskarray(dbz) & (dbz >= dbz_min)
            & ~ma.getmaskarray(rho) & (rho >= rhohv_min))
    g = np.asarray(dbz)
    rr = (10.0 ** (g / 10.0) / zr_a) ** (1.0 / zr_b)
    rr_cap = (10.0 ** (np.minimum(g, hail_cap) / 10.0) / zr_a) ** (1.0 / zr_b)
    out = {}
    for t_in, t_mm in zip(thresholds_in, thresh_mm):
        key = str(t_in)
        out["area_raw_" + key] = float(cell_area_km2[good & (rr >= t_mm)].sum())
        out["area_cap_" + key] = float(cell_area_km2[good & (rr_cap >= t_mm)].sum())
    out["domain_area_km2"] = float(cell_area_km2[good].sum())
    return out


def sweep_rain_rate_capped(radar, rhohv_min=0.85, dbz_min=5.0, hail_cap=53.0,
                           zr_a=200.0, zr_b=1.6):
    """Hail-capped Marshall-Palmer rain rate (mm/hr) on the 0.5 deg sweep.

    Returns (gate_longitude, gate_latitude, rain_rate) arrays for the base sweep,
    masked outside the dual-pol filter. Feed these straight into a pcolormesh on a
    georeferenced axes (transform=PlateCarree) to map rain intensity.
    """
    import numpy as np
    import numpy.ma as ma
    sl = radar.get_slice(0)
    dbz = radar.get_field(0, "reflectivity")
    rho = radar.get_field(0, "cross_correlation_ratio")
    bad = (ma.getmaskarray(dbz) | (dbz < dbz_min)
           | ma.getmaskarray(rho) | (rho < rhohv_min))
    g = np.ma.masked_where(bad, dbz)
    rr = (10.0 ** (np.ma.minimum(g, hail_cap) / 10.0) / zr_a) ** (1.0 / zr_b)
    glon = radar.gate_longitude["data"][sl]
    glat = radar.gate_latitude["data"][sl]
    return glon, glat, rr


def rainfall_band_cmap(edges_in=None):
    """Discrete colormap + BoundaryNorm for imperial rainfall intensity bands.

    edges_in : bin EDGES in in/hr (default [0.1,0.25,0.5,1,2,3] -> 5 bands).
    Returns (cmap, norm, edges_mm) for pcolormesh(..., cmap=cmap, norm=norm);
    values below the first edge are transparent (set_under).
    """
    from matplotlib.colors import BoundaryNorm, ListedColormap
    if edges_in is None:
        edges_in = [0.1, 0.25, 0.5, 1.0, 2.0, 3.0]
    edges_mm = [e * MM_PER_IN for e in edges_in]
    band_colors = ["#c6dbef", "#6baed6", "#fdae61", "#f03b20", "#7a0177"]
    cmap = ListedColormap(band_colors[:len(edges_in) - 1])
    cmap.set_under((0, 0, 0, 0))
    norm = BoundaryNorm(edges_mm, cmap.N)
    return cmap, norm, edges_mm
