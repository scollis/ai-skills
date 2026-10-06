"""Helpers for the NOAA MRMS CONUS hourly analysis Icechunk store (dynamical.org)."""
import os
import sys

MRMS_BUCKET = "dynamical-noaa-mrms"
MRMS_PREFIX = "noaa-mrms-conus-analysis-hourly/v0.3.0.icechunk"
MRMS_REGION = "us-west-2"
MRMS_PTYPE = {
    -3: "no coverage",
    0: "no precipitation",
    1: "warm stratiform rain",
    3: "snow",
    6: "convective rain",
    7: "rain mixed with hail",
    10: "cold stratiform rain",
    91: "tropical/stratiform rain mix",
    96: "tropical/convective rain mix",
}


def mrms_open(bucket=None, prefix=None, region=None):
    """Open the MRMS hourly Icechunk store read-only. Returns an xarray Dataset.

    Requires icechunk >= 2 (Icechunk v2 format), which needs Python >= 3.12.
    Anonymous S3 - no credentials.
    """
    import icechunk
    import xarray as xr
    if bucket is None:
        bucket = MRMS_BUCKET
    if prefix is None:
        prefix = MRMS_PREFIX
    if region is None:
        region = MRMS_REGION
    storage = icechunk.s3_storage(bucket=bucket, prefix=prefix, region=region, anonymous=True)
    repo = icechunk.Repository.open(storage)
    return xr.open_zarr(repo.readonly_session("main").store, chunks=None, consolidated=False)


def mrms_point(ds, lat, lon, var="precipitation_surface", start=None, end=None):
    """Nearest-gridpoint time series. Cheap: chunks span 648 hours, so long spans cost little."""
    da = ds[var].sel(latitude=lat, longitude=lon, method="nearest")
    if start is not None or end is not None:
        da = da.sel(time=slice(start, end))
    return da.load()


def mrms_box(ds, lat, lon, radius_km=120.0, var="precipitation_surface", start=None, end=None):
    """Subset a lat/lon box approximating a radius around a point.

    NOTE latitude is stored DESCENDING, so the slice runs high -> low; this handles it.
    Spatial reads are far more expensive than point reads (each chunk carries 648 time
    steps), so keep the time span short.
    """
    import math
    dlat = radius_km / 111.0
    dlon = radius_km / (111.0 * max(0.1, math.cos(math.radians(lat))))
    da = ds[var].sel(latitude=slice(lat + dlat, lat - dlat),
                     longitude=slice(lon - dlon, lon + dlon))
    if start is not None or end is not None:
        da = da.sel(time=slice(start, end))
    return da.load()


def mrms_ptype_labels(values):
    """Map categorical_precipitation_type_surface codes to human labels.

    There is NO freezing-rain and NO ice-pellet category - MRMS PrecipFlag cannot
    represent them, because freezing rain freezes at the surface and the radar sees
    liquid. Use mPING or ASOS present weather for those.
    """
    import numpy as np
    arr = np.asarray(values)
    flat = arr[np.isfinite(arr)].astype(int).ravel()
    out = {}
    for code in sorted(set(flat.tolist())):
        out[code] = MRMS_PTYPE.get(code, "unknown code %d" % code)
    return out


def mrms_ptype_counts(da):
    """Count hours (or cells) per precipitation-type category, labelled."""
    import numpy as np
    arr = np.asarray(da.values)
    arr = arr[np.isfinite(arr)].astype(int)
    codes, counts = np.unique(arr, return_counts=True)
    return {MRMS_PTYPE.get(int(c), "unknown %d" % int(c)): int(n) for c, n in zip(codes, counts)}


def mrms_mm_per_hour(da):
    """Convert a precipitation-rate variable (kg m-2 s-1) to mm/h."""
    out = da * 3600.0
    out.attrs["units"] = "mm h-1"
    return out


def mrms_accumulate_mm(da):
    """Total accumulation in mm over the time axis of an hourly rate variable."""
    return float((da * 3600.0).sum(dim="time").values) if da.ndim == 1 else (da * 3600.0).sum(dim="time")


def mrms_availability():
    """Per-variable availability, verified against the store on 2026-09-01."""
    return {
        "categorical_precipitation_type_surface": "2014-11-01 onward",
        "_usable_record_starts": "2015-03-01 - the axis begins 2014-11-01 but 2014-11..2015-02 is 4-42% valid CONUS-wide",
        "precipitation_surface": "2014-11-01 onward (source switches 2020-10-15; see _usable_record_starts)",
        "precipitation_radar_only_surface": "2014-11-01 onward",
        "precipitation_pass_1_surface": "2020-10-15 onward (NaN before)",
        "precipitation_pass_2_surface": "2020-10-15 onward (NaN before)",
        "flash_qpe_ffg_max_surface": "2020-10 onward (NaN before)",
    }
