"""Helpers for pyart-mapping: georeference verification, cone geometry, geodesic rings."""
import os


def setup_cartopy_cache(path="cartopy_data"):
    """Point cartopy's Natural Earth cache at a writable workspace dir.

    The default (~/.local/share/cartopy) is read-only in this sandbox and raises
    PermissionError on the first add_feature call. Call before any cartopy feature use.
    """
    import cartopy
    os.makedirs(path, exist_ok=True)
    ap = os.path.abspath(path)
    cartopy.config["data_dir"] = ap
    cartopy.config["pre_existing_data_dir"] = ap
    return ap


def haversine_km(lon1, lat1, lon2, lat2):
    """Great-circle distance in km between two lon/lat points."""
    import math
    R = 6371.0
    p = math.pi / 180
    a = (math.sin((lat2 - lat1) * p / 2) ** 2
         + math.cos(lat1 * p) * math.cos(lat2 * p) * math.sin((lon2 - lon1) * p / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def assert_no_datum_error(lon0=None, lat0=40.0, tol_m=100.0):
    """Demonstrate the PlateCarree vs Geodetic transform_points datum trap.

    Returns {'platecarree_error_m', 'geodetic_error_m', 'ok'}. PlateCarree is a SPHERE
    (+a=6378137 with no flattening); Geodetic is WGS84. Round-tripping the projection
    origin through PlateCarree lands ~21 km away. Never use PlateCarree as the SOURCE
    crs in transform_points on projected metres.
    """
    import numpy as np
    import cartopy.crs as ccrs
    if lon0 is None:
        lon0 = -100.0          # central CONUS; magnitude of the error is latitude-driven
    aeqd = ccrs.AzimuthalEquidistant(central_longitude=lon0, central_latitude=lat0)
    z = np.array([0.0])
    p_pc = ccrs.PlateCarree().transform_points(aeqd, z, z)[0]
    p_gd = ccrs.Geodetic().transform_points(aeqd, z, z)[0]
    e_pc = haversine_km(float(p_pc[0]), float(p_pc[1]), lon0, lat0) * 1000.0
    e_gd = haversine_km(float(p_gd[0]), float(p_gd[1]), lon0, lat0) * 1000.0
    return dict(platecarree_error_m=round(e_pc, 1),
                geodetic_error_m=round(e_gd, 1),
                ok=bool(e_gd < tol_m))


def gates_to_lonlat(radar, sweep=0):
    """(lon, lat) arrays for one sweep, straight from Py-ART's own georeferencing.

    Use these for pcolormesh with transform=ccrs.PlateCarree(). Do NOT reproject
    gate_x/gate_y yourself - see assert_no_datum_error.
    """
    sl = radar.get_slice(sweep)
    return radar.gate_longitude["data"][sl], radar.gate_latitude["data"][sl]


def cone_radius_km(radar, height_m, top_elev_deg=None):
    """Predicted cone-of-silence radius at a height, from the top tilt elevation.

    r = z / tan(top_elevation). Accurate to a few km: below ~4 km the gridded hole is
    smaller (ROI spreads data inward), above it larger (beam spreading between tilts).
    """
    import numpy as np
    if top_elev_deg is None:
        top_elev_deg = float(np.max(radar.fixed_angle["data"]))
    return float(height_m / np.tan(np.deg2rad(top_elev_deg)) / 1000.0)


def check_georeference(radar, sweep=None, n_inner=5, tol_m=500.0):
    """Verify the radar's blind zone sits on the radar coordinate.

    Measures the distance from radar lat/lon to the centroid of the innermost n_inner
    range gates of a sweep. Py-ART's own georeferencing gives sub-metre offsets; a result in
    the kilometres means the plotting/reprojection code is wrong.

    Returns {'offset_m', 'sweep', 'range0_m', 'ok'}.
    """
    import numpy as np
    if sweep is None:
        sweep = radar.nsweeps - 1        # top tilt: biggest cone
    lon0 = float(radar.longitude["data"][0])
    lat0 = float(radar.latitude["data"][0])
    sl = radar.get_slice(sweep)
    glon = radar.gate_longitude["data"][sl]
    glat = radar.gate_latitude["data"][sl]
    n = min(n_inner, glon.shape[1])
    off = haversine_km(float(np.nanmean(glon[:, :n])), float(np.nanmean(glat[:, :n])),
                  lon0, lat0) * 1000.0
    return dict(offset_m=round(off, 1), sweep=int(sweep),
                range0_m=round(float(radar.range["data"][0]), 1),
                ok=bool(off < tol_m))


def sampling_grid(radar, grid_shape=(21, 301, 301),
                  grid_limits=((0.0, 20000.0), (-150000.0, 150000.0), (-150000.0, 150000.0)),
                  grid_origin=None, nb=1.5, bsp=1.0, min_radius=500.0):
    """Grid a field of ones so coverage is PURELY geometric.

    Reflectivity holes mix clear air with unsampled volume; a constant field isolates
    the sampling geometry, which is what you want for cone-of-silence verification.
    """
    import numpy as np
    import pyart
    r1 = radar.extract_sweeps(list(range(radar.nsweeps)))
    r1.fields = {"ones": {"data": np.ma.ones((radar.nrays, radar.ngates)),
                          "units": "1", "long_name": "sampling indicator"}}
    kw = {} if grid_origin is None else dict(grid_origin=grid_origin)
    return pyart.map.grid_from_radars((r1,), grid_shape=grid_shape,
                                      grid_limits=grid_limits, fields=["ones"],
                                      roi_func="dist_beam", nb=nb, bsp=bsp,
                                      min_radius=min_radius, **kw)


def measure_cone(grid, level, field=None, search_radius_m=100000.0):
    """Locate the unsampled cone in a gridded field.

    Returns {'centroid_x','centroid_y','n_cells','max_radius_km','z_m'} in grid
    coordinates (metres from grid origin). For a grid centred on the radar the
    centroid should be within one cell of (0,0).
    """
    import numpy as np
    if field is None:
        field = list(grid.fields)[0]
    X, Y = np.meshgrid(grid.x["data"], grid.y["data"])
    R = np.hypot(X, Y)
    s = np.ma.filled(grid.fields[field]["data"][level], np.nan)
    hole = ~np.isfinite(s) & (R < search_radius_m)
    if hole.sum() == 0:
        return None
    return dict(centroid_x=round(float(X[hole].mean()), 1),
                centroid_y=round(float(Y[hole].mean()), 1),
                n_cells=int(hole.sum()),
                max_radius_km=round(float(np.hypot(X[hole], Y[hole]).max()) / 1000.0, 2),
                z_m=round(float(grid.z["data"][level]), 1))


def range_ring(lon, lat, km, n=181):
    """Geodesically exact range ring as an (n,2) lon/lat array.

    Uses cartopy.geodesic.Geodesic - verified to 0.0 m at 60 and 120 km. Do NOT use
    plt.Circle with a degree radius; that is only correct at the equator.
    """
    import numpy as np
    import cartopy.geodesic as cgeo
    geod = cgeo.Geodesic()
    return np.asarray(geod.circle(lon=lon, lat=lat, radius=km * 1000.0, n_samples=n))


def plain_map_ppi(radar, field, sweep=0, ax=None, gatefilter=None,
                  cmap="ChaseSpectral", vmin=None, vmax=None, extent_deg=1.0,
                  resolution="10m", colorbar_label=None, states=True):
    """plot_ppi_map with embellishment off and layout under your control.

    The default embellish=True adds features and a Gridliner that fight add_axes
    layouts. This wrapper turns all of that off, then adds STATES back.
    """
    import numpy as np
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import pyart
    import cmweather  # noqa: F401  - registers the colormaps
    lon0 = float(radar.longitude["data"][0])
    lat0 = float(radar.latitude["data"][0])
    disp = pyart.graph.RadarMapDisplay(radar)
    disp.plot_ppi_map(field, sweep=sweep, ax=ax, cmap=cmap, vmin=vmin, vmax=vmax,
                      gatefilter=gatefilter, resolution=resolution,
                      colorbar_label=colorbar_label, title_flag=False,
                      embellish=False, add_grid_lines=False,
                      lat_lines=[], lon_lines=[],
                      min_lon=lon0 - extent_deg, max_lon=lon0 + extent_deg,
                      min_lat=lat0 - extent_deg * 0.8, max_lat=lat0 + extent_deg * 0.8)
    if states and ax is not None:
        ax.add_feature(cfeature.STATES.with_scale(resolution), lw=0.4,
                       edgecolor="#999999")
        ax.plot(lon0, lat0, marker="+", ms=13, mew=2, color="k",
                transform=ccrs.Geodetic(), zorder=10)
    return disp
