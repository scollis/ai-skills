"""kernel.py for the arm-netcdf-standards skill.

Helpers to check netCDF files against the ARM Data File Standards
(DOE/SC-ARM-15-004 v1.3) and to write files that comply. Two halves:

checking   arm_check / arm_print / arm_check_tree / arm_findings_df
writing    arm_filename / arm_write_time / arm_skeleton

The writing half exists because most compliance failures in a locally produced
file are structural -- filename, unlimited time dimension, the
base_time/time_offset/time triple, lat/lon/alt -- and are far easier to get
right at creation than to retrofit.

The rule engine itself lives beside this sidecar in arm_standards_check.py and
is loaded on first use by arm_engine(). Nothing imports it at module scope: the
loader exec's this file rather than importing it, so there is no __file__ and no
package to import a sibling from.
"""
import datetime
import os
import re

import numpy as np

SKILL_DIRNAME = "arm-netcdf-standards"
ENGINE_FILENAME = "arm_standards_check.py"
ENGINE_ENV_VAR = "ARM_STANDARDS_CHECKER"
SEVERITY_ORDER = ("error", "warning", "info")


def engine_script_path(override=None):
    """Absolute path to arm_standards_check.py.

    Mirrors nexrad-cost-calibration's measure.py resolution: the loader
    compiles this sidecar with its real path, so the code object knows where it
    lives even though `__file__` is absent. Falls back to the working directory
    for the exec'd-from-a-string case.
    """
    candidates = [override, os.environ.get(ENGINE_ENV_VAR)]
    own = engine_script_path.__code__.co_filename
    if own and os.path.sep in own:
        candidates.append(os.path.join(os.path.dirname(own), ENGINE_FILENAME))
    candidates += [
        os.path.join(os.getcwd(), SKILL_DIRNAME, ENGINE_FILENAME),
        os.path.join(os.getcwd(), ENGINE_FILENAME),
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return os.path.abspath(path)
    raise FileNotFoundError(
        f"{ENGINE_FILENAME} not found. Set {ENGINE_ENV_VAR} to its path, or run "
        f"from a directory containing {SKILL_DIRNAME}/{ENGINE_FILENAME}."
    )


def arm_engine(override=None):
    """Load (once) and return the arm_standards_check module."""
    import importlib.util
    import sys
    mod = sys.modules.get("arm_standards_check")
    if mod is not None and hasattr(mod, "check_file"):
        return mod
    path = engine_script_path(override)
    spec = importlib.util.spec_from_file_location("arm_standards_check", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["arm_standards_check"] = mod
    spec.loader.exec_module(mod)
    return mod


def arm_standard_doc():
    """The standards document this checker encodes."""
    return arm_engine().STANDARD_DOC


# ---------------------------------------------------------------- checking

def arm_check(path, profile="adc", read_data=True):
    """Check one file. Returns a Report; ``.compliant`` is the verdict.

    profile "adc" (default) requires the twelve global attributes ARM's
    released files carry; "doc" requires every attribute in section 6.7.1.
    """
    return arm_engine().check_file(path, profile=profile, read_data=read_data)


def arm_print(path, profile="adc", severity="info"):
    """Check one file and print the grouped report with section citations."""
    rep = arm_check(path, profile=profile)
    print(rep.text(show=SEVERITY_ORDER[: SEVERITY_ORDER.index(severity) + 1]))
    return rep


def arm_check_tree(root, profile="adc", sample_per_datastream=False,
                   recursive=True, read_data=True):
    """Check every netCDF file under *root*, or one file per datastream."""
    eng = arm_engine()
    paths = eng.find_files(root, recursive=recursive,
                           sample_per_datastream=sample_per_datastream)
    return eng.check_files(paths, profile=profile, read_data=read_data)


def arm_summarise(reports):
    """Aggregate rule hits across many reports: the fleet view."""
    return arm_engine().summarise(reports)


def arm_findings_df(reports):
    """One row per finding, as a DataFrame. Accepts a Report or a list."""
    import pandas as pd
    if not isinstance(reports, (list, tuple)):
        reports = [reports]
    rows = [
        {"file": os.path.basename(r.path), "rule": f.rule, "severity": f.severity,
         "section": f.section, "target": f.target, "message": f.message}
        for r in reports for f in r.findings
    ]
    return pd.DataFrame(rows, columns=["file", "rule", "severity", "section",
                                       "target", "message"])


# ---------------------------------------------------------------- writing

def arm_filename(site, inst, facility, level, start, ext="nc"):
    """Build and validate an ARM filename (§5.1).

    >>> arm_filename("bnf", "arsclkazr1kollias", "M1", "c1",
    ...              datetime.datetime(2025, 5, 3))
    'bnfarsclkazr1kolliasM1.c1.20250503.000000.nc'

    Raises ValueError with the offending rule when the result would not comply,
    so a bad name fails at creation instead of at the ADC.
    """
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y%m%d%H%M%S" if len(start) == 14
                                      else "%Y%m%d")
    name = (f"{site}{inst}{facility}.{level}."
            f"{start:%Y%m%d}.{start:%H%M%S}.{ext}")
    if not re.fullmatch(r"[a-z]{3}", site):
        raise ValueError(f"site '{site}' must be three lower-case letters (§5.1)")
    if not re.fullmatch(r"[A-Z]\d{1,2}", facility):
        raise ValueError(f"facility '{facility}' must be a capital letter and "
                         "one or two digits (§5.1)")
    if not re.fullmatch(r"\d{2}|[a-z]\d", level):
        raise ValueError(f"data level '{level}' must be two digits or a "
                         "lower-case letter and a digit (§5.1.3)")
    if not re.fullmatch(r"[a-z0-9]+", inst):
        raise ValueError(f"instrument '{inst}' may contain only lower-case "
                         "letters and digits -- no underscores or dashes (§5.1)")
    if len(inst) > 24:
        raise ValueError(f"(inst)(qualifier)(temporal) is {len(inst)} characters; "
                         "the ADC limit is 24 (§5.1.1)")
    if len(f"{site}{inst}{facility}.{level}") > 33:
        raise ValueError("datastream exceeds the ADC limit of 33 characters (§5.1.1)")
    if len(name) > 60:
        raise ValueError(f"filename is {len(name)} characters; the ADC limit is "
                         "60 (§5.1.1)")
    assert arm_engine().FILENAME_RE.match(name), name
    return name


def arm_write_time(nc, times, base=None):
    """Write the required base_time / time_offset / time triple (§6.1.2-6.1.3).

    *nc* is an open netCDF4.Dataset in write mode with an unlimited ``time``
    dimension already defined.  *times* is a sequence of datetimes or a numpy
    datetime64 array.  *base* defaults to UTC midnight of the first sample,
    which is what the standard recommends.

    The filename timestamp must equal base_time + time_offset[0]; passing the
    same ``times[0]`` you used to build the filename keeps that true.
    """
    t = np.asarray(times)
    if np.issubdtype(t.dtype, np.datetime64):
        pyt = t.astype("datetime64[us]").astype(datetime.datetime)
    else:
        pyt = list(t)
    epoch = datetime.datetime(1970, 1, 1)
    secs = np.array([(x - epoch).total_seconds() for x in pyt], dtype="f8")
    first = pyt[0]
    if base is None:
        base = datetime.datetime(first.year, first.month, first.day)
    base_epoch = int((base - epoch).total_seconds())
    midnight = f"{base:%Y-%m-%d %H:%M:%S} 0:00"

    bt = nc.createVariable("base_time", "i4")
    bt.string = f"{first:%d-%b-%Y,%H:%M:%S} GMT"
    bt.long_name = "Base time in Epoch"
    bt.units = "seconds since 1970-1-1 0:00:00 0:00"
    bt.ancillary_variables = "time_offset"
    bt[...] = base_epoch

    to = nc.createVariable("time_offset", "f8", ("time",))
    to.long_name = "Time offset from base_time"
    to.units = f"seconds since {midnight}"
    to.ancillary_variables = "base_time"
    to[:] = secs - base_epoch

    tv = nc.createVariable("time", "f8", ("time",))
    tv.long_name = "Time offset from midnight"
    tv.units = f"seconds since {midnight}"
    tv.standard_name = "time"
    tv[:] = secs - base_epoch
    return bt, to, tv


def arm_skeleton(path, site, inst, facility, level, times, lat, lon, alt,
                 location_description, platform_id=None, dod_version="1.0",
                 process_version="unknown", command_line=None, doi="unknown",
                 extra_globals=None, fmt="NETCDF3_CLASSIC"):
    """Create a minimal ARM-compliant netCDF file and return its path.

    Writes the unlimited time dimension, the base_time/time_offset/time triple,
    lat/lon/alt with their required units and standard names, and the twelve
    global attributes ARM's released files carry.  Add data variables to the
    returned file with ``netCDF4.Dataset(path, "a")``, giving each a unique
    ``long_name`` and a UDUNITS ``units``.

    *path* may be a directory, in which case the compliant filename is built
    for you with :func:`arm_filename`.
    """
    import netCDF4
    platform_id = platform_id or inst
    if platform_id != inst:
        raise ValueError(
            f"platform_id '{platform_id}' must equal the instrument part of the "
            f"filename '{inst}': §6.7.1 makes datastream = site_id + platform_id "
            "+ facility_id + '.' + data_level, and that must match the filename")
    if isinstance(times, (list, tuple, np.ndarray)):
        t0 = np.asarray(times)[0]
    else:
        raise TypeError("times must be a sequence of datetimes")
    if np.issubdtype(np.asarray(times).dtype, np.datetime64):
        t0 = np.datetime64(t0, "us").astype(datetime.datetime)
    name = arm_filename(site, inst, facility, level, t0)
    if os.path.isdir(path):
        path = os.path.join(path, name)
    elif os.path.basename(path) != name:
        raise ValueError(f"filename must be '{name}' for these identifiers; "
                         f"got '{os.path.basename(path)}'")

    nc = netCDF4.Dataset(path, "w", format=fmt)
    try:
        nc.createDimension("time", None)
        arm_write_time(nc, times)
        for vname, sname, units, val, lname in (
            ("lat", "latitude", "degree_N", lat, "North latitude"),
            ("lon", "longitude", "degree_E", lon, "East longitude"),
            ("alt", "altitude", "m", alt, "Altitude above mean sea level"),
        ):
            v = nc.createVariable(vname, "f4")
            v.long_name = lname
            v.units = units
            v.standard_name = sname
            if vname in ("lat", "lon"):
                lim = 90.0 if vname == "lat" else 180.0
                v.valid_min = np.float32(-lim)
                v.valid_max = np.float32(lim)
            v[...] = np.float32(val)
        import sys
        nc.command_line = (command_line
                           or os.path.basename(sys.argv[0]) or "python")
        nc.Conventions = "ARM-1.3 CF-1.7"
        nc.process_version = process_version
        nc.dod_version = dod_version
        nc.site_id = site
        nc.platform_id = platform_id
        nc.facility_id = facility
        nc.data_level = level
        nc.location_description = location_description
        nc.datastream = f"{site}{platform_id}{facility}.{level}"
        nc.doi = doi
        for k, v in (extra_globals or {}).items():
            setattr(nc, k, v)
        nc.history = (f"created by user {os.environ.get('USER', 'unknown')} on "
                      f"{datetime.datetime.now(datetime.timezone.utc):%d-%b-%Y,%H:%M:%S} UTC")
    finally:
        nc.close()
    return path
