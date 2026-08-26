import math

# --- Google Cloud public NEXRAD Level-II bucket (AWS fallback) ---
NEXRAD_GCS_HOST = "https://gcp-public-data-nexrad-l2.storage.googleapis.com"
# Marshall-Palmer Z-R relation: Z = A * R**B  (Z in linear mm^6 m^-3)
MARSHALL_PALMER_A = 200.0
MARSHALL_PALMER_B = 1.6


def scan_time(path):
    """Parse the UTC datetime from a NEXRAD key/filename (SITEyyyymmdd_HHMMSS...)."""
    import re, datetime as dt
    m = re.search(r"[A-Z]{4}(\d{8})_(\d{6})", str(path))
    if not m:
        raise ValueError("no NEXRAD timestamp in %r" % path)
    return dt.datetime.strptime(m.group(1) + m.group(2), "%Y%m%d%H%M%S")


def nexrad_gcs_keys(site, year, month, day, host=None, full_volumes_only=True):
    """List Level-II volume-scan object keys for one radar SITE on one UTC day
    from the Google Cloud public NEXRAD bucket. Returns a sorted list of keys.
    Requires network access to the bucket host (request_network_access)."""
    import urllib.request, xml.etree.ElementTree as ET
    if host is None:
        host = NEXRAD_GCS_HOST
    prefix = "%04d/%02d/%02d/%s/" % (int(year), int(month), int(day), site)
    keys, marker = [], ""
    while True:
        url = "%s/?prefix=%s&marker=%s" % (host, prefix, marker)
        with urllib.request.urlopen(url, timeout=60) as r:
            root = ET.fromstring(r.read())
        contents = root.findall("{*}Contents")
        if not contents:
            break
        for c in contents:
            keys.append(c.find("{*}Key").text)
        trunc = root.find("{*}IsTruncated")
        if trunc is None or (trunc.text or "").lower() != "true":
            break
        marker = keys[-1]
    if full_volumes_only:  # drop supplemental *_MDM message volumes
        keys = [k for k in keys if not k.endswith("_MDM")]
    return sorted(keys)


def download_nexrad(keys, dest_dir="nexrad_scans", host=None):
    """Download NEXRAD keys from the GCS bucket into dest_dir (skips existing).
    Returns local file paths sorted by scan time."""
    import os, urllib.request
    if host is None:
        host = NEXRAD_GCS_HOST
    os.makedirs(dest_dir, exist_ok=True)
    paths = []
    for k in keys:
        local = os.path.join(dest_dir, os.path.basename(k))
        if not os.path.exists(local):
            urllib.request.urlretrieve("%s/%s" % (host, k), local)
        paths.append(local)
    return sorted(paths, key=scan_time)


def read_radar_safe(path):
    """Read a NEXRAD archive with Py-ART; return None on a corrupt/unreadable file
    (some volume scans in the archive are truncated)."""
    import pyart
    try:
        return pyart.io.read_nexrad_archive(path)
    except Exception:
        return None


def setup_cmweather():
    """Register cmweather colormaps and fix the savefig bbox. Call once before plotting.
    figure-style's apply_figure_style() sets savefig.bbox='tight', which COLLAPSES a
    cartopy GeoAxes on save -- this resets it to 'standard'."""
    import cmweather  # noqa: F401  (import registers the colormaps)
    import matplotlib as mpl
    mpl.rcParams["savefig.bbox"] = "standard"
    return True


def dualpol_gatefilter(radar, rhohv_min=0.85, dbz_min=5.0, field="reflectivity"):
    """Standard dual-pol meteorological gate filter: drop low rho_HV, low dBZ, invalid."""
    import pyart
    gf = pyart.filters.GateFilter(radar)
    gf.exclude_below("cross_correlation_ratio", rhohv_min)
    gf.exclude_below(field, dbz_min)
    gf.exclude_invalid(field)
    return gf


def extract_site_rainrate(radar, site_lat, site_lon, radius_km=2.0,
                          rhohv_min=0.85, dbz_min=5.0, zr_a=None, zr_b=None):
    """Mean reflectivity and Marshall-Palmer rain rate over a circular footprint
    around a site, from the lowest sweep. Averages in LINEAR Z then converts.
    Returns dict(mean_dbz, rain_rate_mmph, n_gates)."""
    import numpy as np, numpy.ma as ma
    if zr_a is None:
        zr_a = MARSHALL_PALMER_A
    if zr_b is None:
        zr_b = MARSHALL_PALMER_B
    sweep0 = radar.extract_sweeps([0])
    lats = sweep0.gate_latitude["data"]
    lons = sweep0.gate_longitude["data"]
    dy = (lats - site_lat) * 111.0
    dx = (lons - site_lon) * 111.0 * math.cos(math.radians(site_lat))
    near = np.sqrt(dx ** 2 + dy ** 2) <= radius_km
    dbz = sweep0.fields["reflectivity"]["data"]
    rho = sweep0.fields["cross_correlation_ratio"]["data"]
    good = (near & ~ma.getmaskarray(dbz) & (dbz >= dbz_min)
            & ~ma.getmaskarray(rho) & (rho >= rhohv_min))
    n = int(np.count_nonzero(good))
    if n == 0:
        return {"mean_dbz": float("nan"), "rain_rate_mmph": float("nan"), "n_gates": 0}
    zlin = 10.0 ** (np.asarray(dbz[good]) / 10.0)
    zmean = float(np.mean(zlin))
    return {"mean_dbz": 10.0 * math.log10(zmean),
            "rain_rate_mmph": float((zmean / zr_a) ** (1.0 / zr_b)),
            "n_gates": n}


def make_radar_geoaxes(fig, radar, rect=(0.05, 0.05, 0.9, 0.9), extent=None,
                       tiler=None, tile_zoom=9, tile_alpha=0.5):
    """Create a correctly-georeferenced GeoAxes for a radar PPI.

    Uses a MERCATOR projection. IMPORTANT georeferencing lesson: do NOT use a
    cartopy AzimuthalEquidistant centered on the radar. cartopy's aeqd transform
    is inaccurate at the origin for a non-zero central_latitude -- it maps the
    radar's own lon/lat to roughly (0, +21 km) instead of (0, 0), so the gate
    field (drawn on that projection) ends up shifted ~21 km south of the radar
    marker (which is plotted from true lon/lat). The symptom is a radar triangle
    sitting NORTH of the cone-of-silence blind zone. Mercator is well-behaved
    over a metro-scale extent, and we plot the data using Py-ART's OWN
    gate_longitude/gate_latitude (spherical, correct) via pcolormesh with a
    PlateCarree transform -- so no aeqd round-trip happens anywhere.

    rect   = [left, bottom, width, height] in figure fraction.
    extent = [lon_min, lon_max, lat_min, lat_max] (lon/lat); optional.
    tiler  = a cartopy.io.img_tiles source (e.g. cimgt.OSM(cache=True)) to draw a
             tiled basemap under the radar; requires network access to the tile
             host (for OSM: a/b/c.tile.openstreetmap.org). None = no basemap.
    Returns the GeoAxes. Draw data/markers with transform=ccrs.PlateCarree().
    """
    import cartopy.crs as ccrs
    proj = tiler.crs if tiler is not None else ccrs.Mercator()
    ax = fig.add_axes(list(rect), projection=proj)
    if extent is not None:
        ax.set_extent(extent, crs=ccrs.PlateCarree())
    if tiler is not None:
        try:
            ax.add_image(tiler, tile_zoom, alpha=tile_alpha)
        except Exception:
            pass  # tiles blocked/unavailable -- fall back to a bare basemap
    return ax


def add_context_features(ax, extent, roads=True, airports=True, states=True,
                         label_interstates=True):
    """Overlay interstates, airports, and state borders on a radar GeoAxes.

    extent = [lon_min, lon_max, lat_min, lat_max]. Interstates (level=='Interstate')
    are drawn in red with route labels; beltways/expressways in orange; airports
    as navy diamonds with IATA/abbrev labels. All from Natural Earth 10m cultural
    layers (allowlisted CDN). Draw AFTER the radar pcolormesh so lines sit on top.
    """
    import cartopy.crs as ccrs, cartopy.feature as cfeature
    import cartopy.io.shapereader as shpreader
    from shapely.geometry import box
    pc = ccrs.PlateCarree()
    clip = box(extent[0], extent[2], extent[1], extent[3])
    if states:
        ax.add_feature(cfeature.STATES.with_scale("10m"), edgecolor="0.4", linewidth=0.6)
    if roads:
        rd = shpreader.Reader(shpreader.natural_earth(resolution="10m",
                              category="cultural", name="roads"))
        labeled = set()
        for rec in rd.records():
            g = rec.geometry
            if g is None or not g.intersects(clip):
                continue
            lvl = rec.attributes.get("level"); typ = rec.attributes.get("type")
            nm = str(rec.attributes.get("name", "")); gi = g.intersection(clip)
            if lvl == "Interstate":
                ax.add_geometries([gi], crs=pc, edgecolor="#b8231f",
                                  facecolor="none", linewidth=2.2, zorder=6)
                if label_interstates and nm and ("I", nm) not in labeled:
                    pt = gi.representative_point()
                    ax.text(pt.x, pt.y, "I-" + nm, fontsize=8, color="#b8231f",
                            fontweight="bold", transform=pc, zorder=9, ha="center",
                            bbox=dict(boxstyle="round,pad=0.1", fc="white",
                                      ec="none", alpha=0.7))
                    labeled.add(("I", nm))
            elif typ == "Beltway" or rec.attributes.get("expressway", 0) == 1:
                ax.add_geometries([gi], crs=pc, edgecolor="#e08214",
                                  facecolor="none", linewidth=1.3, zorder=6)
    if airports:
        ap = shpreader.Reader(shpreader.natural_earth(resolution="10m",
                              category="cultural", name="airports"))
        for rec in ap.records():
            g = rec.geometry
            if g is None or not g.within(clip):
                continue
            ax.plot(g.x, g.y, marker="D", color="#08306b", markersize=6,
                    transform=pc, zorder=8)
            nm = (rec.attributes.get("iata_code") or rec.attributes.get("abbrev")
                  or rec.attributes.get("name", ""))
            ax.annotate(str(nm), xy=(g.x, g.y), xytext=(4, 3),
                        textcoords="offset points", fontsize=7, color="#08306b",
                        fontweight="bold", transform=pc, zorder=8)


def plot_ppi_map(radar, ax, fig, field="reflectivity", sweep=0, extent=None,
                 cmap="ChaseSpectral", vmin=0.0, vmax=70.0, rhohv_min=0.85,
                 dbz_min=5.0, site=None, title="", colorbar_label=None,
                 alpha=0.85, add_colorbar=True, context=False):
    """Plot a dual-pol-filtered PPI field on a cartopy GeoAxes `ax`.

    extent = [lon_min, lon_max, lat_min, lat_max]; site = (lat, lon).
    Call setup_cmweather() once before the first plot.

    GEOREFERENCING (verified correct): the field is drawn with Py-ART's OWN
    radar.gate_longitude / radar.gate_latitude (spherical geometry, matches the
    true radar location to ~6 decimals) via ax.pcolormesh(..., transform=
    ccrs.PlateCarree()). This deliberately does NOT go through
    RadarMapDisplay.plot_ppi_map on a cartopy AzimuthalEquidistant axes: that
    path shifts the gate field ~21 km south of the radar marker because cartopy's
    aeqd transform is inaccurate at the origin for non-zero central_latitude.
    Build `ax` with make_radar_geoaxes(fig, radar, ...) (Mercator). Markers are
    drawn with transform=ccrs.PlateCarree() (lon/lat).

    context=True overlays interstates + airports + state borders via
    add_context_features(). Returns the QuadMesh from pcolormesh.
    """
    import numpy as np
    import cartopy.crs as ccrs
    pc = ccrs.PlateCarree()
    gf = dualpol_gatefilter(radar, rhohv_min, dbz_min, field)
    sl = radar.get_slice(sweep)
    data = radar.get_field(sweep, field)
    excl = gf.gate_excluded[sl]
    data = np.ma.masked_where(excl, data)
    glon = radar.gate_longitude["data"][sl]
    glat = radar.gate_latitude["data"][sl]
    pm = ax.pcolormesh(glon, glat, data, transform=pc, cmap=cmap,
                       vmin=vmin, vmax=vmax, alpha=alpha, shading="auto", zorder=5)
    if extent is not None:
        ax.set_extent(extent, crs=pc)
    if context and extent is not None:
        add_context_features(ax, extent)
    if add_colorbar:
        cb = fig.colorbar(pm, ax=ax, shrink=0.8, pad=0.02)
        cb.set_label(colorbar_label or field)
    if title:
        ax.set_title(title)
    if site is not None:
        ax.plot(site[1], site[0], marker="*", markersize=17, color="black",
                markerfacecolor="yellow", markeredgewidth=1.2, transform=pc, zorder=11)
    ax.plot(radar.longitude["data"][0], radar.latitude["data"][0],
            marker="^", markersize=10, color="black", markerfacecolor="white",
            markeredgewidth=1.2, transform=pc, zorder=11)
    return pm
