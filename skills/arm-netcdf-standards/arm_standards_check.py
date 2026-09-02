"""ARM netCDF data-file metadata compliance checker.

Checks a netCDF file against the ARM Data File Standards, DOE/SC-ARM-15-004
(ARM Standards Committee, September 2020, version 1.3).  Every rule carries the
document section it comes from, so a finding can be argued from the source.

Severities
----------
error    a REQUIRED standard (section 2.1) is not met.  ARM will not publish
         the file in the ADC without a granted exception.
warning  a RECOMMENDED standard (section 2.2), or a required-with-conditions
         standard whose condition could not be verified automatically.
info     an OPTIONAL method (section 3.0), or an observation worth a human
         glance that is not a deviation.

Profiles
--------
adc      (default) required = the twelve global attributes ARM's own published
         files actually carry.  Calibrated against 111 released datastreams.
doc      literal reading of section 6.7.1.  Every one of the 24 global-attribute
         headings there is set bold-underline -- verified by measuring the drawn
         underline rule under each heading's bold run, not by eye -- and the
         section's legend makes bold-underline mean required.  Three of them
         (input_datastreams, input_source, serial_number) carry an inline
         parenthetical condition ("ingest only", "required only if reading RAW
         data", "required with stipulation"); those, plus sampling_interval,
         averaging_interval and sensor_height, are treated as conditional in
         both profiles because the document states a condition in the text.
         The rest become errors under this profile.

Usage
-----
    python arm_standards_check.py FILE [FILE ...] [--json out.json] [--profile doc]
    python arm_standards_check.py DIR --recursive --sample-per-datastream

    from arm_standards_check import check_file
    report = check_file("sgpmetE13.b1.20240101.000000.nc")
    print(report.text())
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field, asdict

import numpy as np

try:
    import netCDF4
except ImportError:  # pragma: no cover
    netCDF4 = None

STANDARD_DOC = "DOE/SC-ARM-15-004 v1.3 (September 2020)"


def here():
    """Directory holding this module.

    Uses the code object's filename rather than ``__file__`` so the module
    still finds its bundled CF table when it is exec'd rather than imported --
    which is how the skill's own test suite loads it.
    """
    own = here.__code__.co_filename
    if own and os.path.sep in own:
        return os.path.dirname(os.path.abspath(own))
    return os.getcwd()

# --------------------------------------------------------------------------
# reference data
# --------------------------------------------------------------------------

#: The twelve global attributes present in essentially every released ARM file.
#: Measured over one file from each of 138 released ARM datastreams
#: (a1/b1/c0/c1, six sites): each of these is present in 97-100% of them, and
#: the next most common global attribute (input_source) reaches only 70%.
CORE_GLOBAL_ATTRS = (
    "command_line",
    "Conventions",
    "process_version",
    "dod_version",
    "site_id",
    "platform_id",
    "facility_id",
    "data_level",
    "location_description",
    "datastream",
    "doi",
    "history",
)

#: Printed bold-underline in section 6.7.1 (therefore "required" by the
#: document's own legend) but rare in released files.  Warnings under the
#: default profile, errors under --profile doc.
DOC_GLOBAL_ATTRS = (
    "command_line_comment",
    "title",
    "institution",
    "description",
    "references",
    "doi_url",
)

#: Required only when the stated condition holds (section 6.7.1).
CONDITIONAL_GLOBAL_ATTRS = {
    "input_datastreams": "VAP or ingest reading an ARM datastream; may be omitted "
    "if source attributes or source variables describe the inputs",
    "input_source": "ingest only; required if reading RAW data",
    "serial_number": "ingest only; required if the serial number is known at "
    "runtime and can change",
    "sampling_interval": "records the expected sampling interval",
    "averaging_interval": "records the expected averaging interval",
    "sensor_height": "required at global level only if all sensors share a height "
    "and no variable-level sensor_height is given",
}

INSTITUTION_VALUE = (
    "United States Department of Energy - Atmospheric Radiation Measurement (ARM) program"
)

QC_BIT_DESCRIPTION = (
    "This variable contains bit packed integer values, where each bit represents "
    "a QC test on the data. Non-zero bits indicate the QC condition given in the "
    "description for those bits; a value of 0 (no bits set) indicates the data has "
    "not failed any QC tests."
)
QC_INT_DESCRIPTION = (
    "This variable contains integer values indicating the results of QC test on "
    "the data. Non-zero integers indicate the QC condition given in the description "
    "for those integers; a value of 0 indicates the data has not failed any QC tests."
)
QC_GLOBAL_POINTER_BIT = "See global attributes for individual QC bit descriptions."
QC_GLOBAL_POINTER_INT = "See global attributes for individual QC flag descriptions."

ASSESSMENTS = ("Bad", "Indeterminate")

TRANSFORM_TYPES = (
    "TRANS_BIN_AVERAGE",
    "TRANS_INTERPOLATE",
    "TRANS_SUBSAMPLE",
    "TRANS_PASSTHROUGH",
)

# Facility letters defined in section 5.1.2 (retired ones still legal in
# historical data, so all are accepted; unknown letters are flagged).
FACILITY_LETTERS = set("ABCDEFILMNQSUX")

# Temporal resolution unit abbreviations, section 5.1.
TEMPORAL_UNITS = ("ns", "us", "ms", "s", "m", "h", "d", "mo", "yr")

# --- UDUNITS symbol table -------------------------------------------------
# Enough of the UDUNITS-2 database to validate ARM unit strings offline, plus
# every symbol in Appendix C of the standard.  A symbol that is not here yields
# a warning (verify by hand), never an error -- a checker that cries wolf on
# legal units is worse than one that misses a few.
_UD_PREFIXES = {
    "yotta": 24, "zetta": 21, "exa": 18, "peta": 15, "tera": 12, "giga": 9,
    "mega": 6, "kilo": 3, "hecto": 2, "deca": 1, "deci": -1, "centi": -2,
    "milli": -3, "micro": -6, "nano": -9, "pico": -12, "femto": -15,
    "atto": -18, "zepto": -21, "yocto": -24,
    "Y": 24, "Z": 21, "E": 18, "P": 15, "T": 12, "G": 9, "M": 6, "k": 3,
    "h": 2, "da": 1, "d": -1, "c": -2, "m": -3, "u": -6, "n": -9, "p": -12,
    "f": -15, "a": -18, "z": -21, "y": -24,
}

_UD_UNITS = set("""
1 m meter metre s second sec kg gram g K kelvin degK A ampere mol mole cd candela
rad radian sr steradian Hz hertz N newton Pa pascal J joule W watt C coulomb
V volt F farad ohm S siemens Wb weber T tesla H henry lm lumen lx lux Bq becquerel
Gy gray Sv sievert kat katal
min minute hr hour h day d week month yr year a annum
L l liter litre t tonne ha hectare bar atm atmosphere Torr mmHg inHg psi
degC celsius Celsius degree_Celsius degF fahrenheit Fahrenheit degree_Fahrenheit
degree degrees deg arcdeg arcmin arcsec
degree_N degrees_north degree_north degrees_N degreeN degreesN
degree_S degrees_south degree_south degrees_S
degree_E degrees_east degree_east degrees_E degreeE degreesE
degree_W degrees_west degree_west degrees_W
percent % permille ppm ppmv ppb ppbv ppt pptv
count counts number dimensionless unity
dB dBZ dBm decibel bel B
in inch inches ft foot feet yd yard mi mile nmi
lb pound oz ounce
knot knots kt
gal gallon
dobson DU
mm cm km um nm pm mg ug ng kPa hPa mbar millibar
byte bit bits
e electron photon
shot shots profile profiles pulse pulses sample samples
volt volts amp amps
""".split())

# Symbols that appear in ARM files, are not UDUNITS, but are established ARM
# usage.  Treated as recognised; the standard's own Appendix C lists several.
_ARM_EXTRA_UNITS = set("""
fraction ratio
dBZ dBsm dBZe
cc
""".split())

_UNIT_TOKEN = re.compile(r"[A-Za-z_%°µ]+")


def _split_unit_symbols(units: str):
    """Yield the alphabetic symbols in a UDUNITS expression."""
    if units is None:
        return []
    s = str(units)
    # "<unit> since <timestamp>" -- only the leading unit is a unit
    m = re.match(r"^\s*([^\s]+)\s+since\s+", s, re.I)
    if m:
        s = m.group(1)
    return _UNIT_TOKEN.findall(s)


def unit_symbol_known(sym: str) -> bool:
    """Is *sym* a UDUNITS symbol, name, plural or prefixed form?

    UDUNITS accepts the plural of any spelled-out unit name ("seconds",
    "hours", "counts"), so strip a trailing 's' before giving up.
    """
    cands = [sym]
    if len(sym) > 2 and sym.endswith("s"):
        cands.append(sym[:-1])
    if len(sym) > 3 and sym.endswith("es"):
        cands.append(sym[:-2])
    for c in cands:
        if c in _UD_UNITS or c in _ARM_EXTRA_UNITS:
            return True
        for pfx in sorted(_UD_PREFIXES, key=len, reverse=True):
            if c.startswith(pfx) and len(c) > len(pfx) and c[len(pfx):] in _UD_UNITS:
                return True
    return False


def check_units_string(units):
    """Return a list of unrecognised symbols in a units string."""
    return [s for s in _split_unit_symbols(units) if not unit_symbol_known(s)]


_CF_NAMES = None


def cf_standard_names():
    """Load the bundled CF standard-name list (canonical names + aliases)."""
    global _CF_NAMES
    if _CF_NAMES is None:
        path = os.path.join(here(), "cf_standard_names.txt")
        if not os.path.exists(path):
            _CF_NAMES = frozenset()
        else:
            with open(path) as fh:
                _CF_NAMES = frozenset(
                    ln.strip() for ln in fh
                    if ln.strip() and not ln.startswith("#")
                )
    return _CF_NAMES


# --------------------------------------------------------------------------
# findings
# --------------------------------------------------------------------------

SEVERITIES = ("error", "warning", "info")


@dataclass
class Finding:
    rule: str
    severity: str
    section: str
    target: str
    message: str

    def __str__(self):
        return f"[{self.severity:7s}] {self.rule:9s} {self.target:28s} {self.message}  (§{self.section})"


@dataclass
class Report:
    path: str
    findings: list = field(default_factory=list)
    profile: str = "adc"
    info: dict = field(default_factory=dict)

    # -- construction ------------------------------------------------------
    def add(self, rule, severity, section, target, message):
        self.findings.append(Finding(rule, severity, section, target, message))

    # -- queries -----------------------------------------------------------
    def counts(self):
        c = Counter(f.severity for f in self.findings)
        return {s: c.get(s, 0) for s in SEVERITIES}

    @property
    def compliant(self):
        """True when no required standard was violated."""
        return self.counts()["error"] == 0

    def by_severity(self, severity):
        return [f for f in self.findings if f.severity == severity]

    # -- output ------------------------------------------------------------
    def text(self, show=("error", "warning", "info"), width=100, collapse=4):
        c = self.counts()
        head = (
            f"{os.path.basename(self.path)}\n"
            f"{'=' * min(width, len(os.path.basename(self.path)))}\n"
            f"standard : {STANDARD_DOC}   profile: {self.profile}\n"
            f"verdict  : {'COMPLIANT' if self.compliant else 'NOT COMPLIANT'}"
            f"   ({c['error']} error, {c['warning']} warning, {c['info']} info)\n"
        )
        if self.info:
            head += "".join(
                f"{k:9s}: {v}\n" for k, v in self.info.items()
            )
        lines = [head]
        for sev in show:
            group = self.by_severity(sev)
            if not group:
                continue
            lines.append(f"\n-- {sev.upper()} ({len(group)}) " + "-" * 40)
            # A rule that fires on many variables (valid_min on every data
            # variable, say) is one deviation, not fifty; collapse it so the
            # report stays readable.  The JSON keeps every finding.
            buckets = defaultdict(list)
            for f in group:
                buckets[(f.rule, f.section, f.message.split(";")[0])].append(f)
            for (rule, section, _), fs in sorted(buckets.items()):
                if len(fs) <= collapse:
                    for f in sorted(fs, key=lambda f: f.target):
                        lines.append(str(f))
                else:
                    tgts = sorted(f.target for f in fs)
                    lines.append(
                        f"[{sev:7s}] {rule:9s} {len(fs)} variables               "
                        f"{fs[0].message}  (§{section})")
                    lines.append(f"{'':32s}affects: {', '.join(tgts[:8])}"
                                 + (f", ... (+{len(tgts) - 8} more)" if len(tgts) > 8 else ""))
        return "\n".join(lines)

    def to_dict(self):
        return {
            "path": self.path,
            "standard": STANDARD_DOC,
            "profile": self.profile,
            "compliant": self.compliant,
            "counts": self.counts(),
            "info": self.info,
            "findings": [asdict(f) for f in self.findings],
        }


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

FILENAME_RE = re.compile(
    r"^(?P<datastream>(?P<site>[a-z]{3})(?P<inst>[a-z0-9]+?)(?P<fac>[A-Z]\d{1,2}))"
    r"\.(?P<level>\d{2}|[a-z]\d)"
    r"\.(?P<date>\d{8})\.(?P<time>\d{6})"
    r"\.(?P<ext>nc|cdf)$"
)


def _attr(obj, name, default=None):
    try:
        return obj.getncattr(name)
    except AttributeError:
        return default


def _has(obj, name):
    return name in obj.ncattrs()


def _as_scalar(v):
    if isinstance(v, (bytes, str)):
        return v
    a = np.asarray(v)
    return a.reshape(-1)[0] if a.size else None


def _numeric_kind(dtype):
    try:
        return np.dtype(dtype).kind
    except TypeError:
        return "O"


def _same_numeric_type(attr_value, var_dtype):
    """Does an attribute's stored type match the variable's type?

    The standard (6.6.7) requires the same *type* for attributes used directly
    with the values.  netCDF3 has no float64/float32 distinction in the eyes of
    most writers, so compare itemsize and kind.
    """
    try:
        av = np.asarray(attr_value)
        vd = np.dtype(var_dtype)
    except Exception:
        return True
    if av.dtype.kind in "SU" or vd.kind in "SU":
        return av.dtype.kind == vd.kind
    return av.dtype.kind == vd.kind and av.dtype.itemsize == vd.itemsize


def _count_flag_values(ref):
    """Count flag_values / flag_masks entries, tolerating a stringified array.

    Some writers emit the repr of an array ("[0 1 2 3]") into a character
    attribute.  That is a deviation in its own right (STA-008), but the count
    check should still say something useful rather than compare 1 with N.
    """
    if isinstance(ref, bytes):
        ref = ref.decode("utf-8", "replace")
    if isinstance(ref, str):
        nums = re.findall(r"-?\d+(?:\.\d+)?", ref)
        return len(nums) if nums else 1
    return int(np.asarray(ref).size)


def _bit_indices(attrs, prefix):
    """Return sorted bit/flag numbers declared via <prefix>_<n>_description."""
    out = []
    pat = re.compile(rf"^{prefix}_(-?\d+)_description$")
    for a in attrs:
        m = pat.match(a)
        if m:
            out.append(int(m.group(1)))
    return sorted(out)


def _is_coordinate_var(nc, name):
    v = nc.variables[name]
    return name in nc.dimensions and v.ndim == 1


def _monotonic(a):
    a = np.asarray(a, dtype="f8").ravel()
    a = a[np.isfinite(a)]
    if a.size < 2:
        return True
    d = np.diff(a)
    return bool(np.all(d > 0) or np.all(d < 0))


# --------------------------------------------------------------------------
# the checker
# --------------------------------------------------------------------------


class ArmStandardsChecker:
    def __init__(self, path, profile="adc", read_data=True, data_limit=5_000_000):
        self.path = path
        self.profile = profile
        self.read_data = read_data
        self.data_limit = data_limit
        self.report = Report(path=path, profile=profile)
        self.fname = os.path.basename(path)
        self.fn = None          # parsed filename groups
        self.nc = None

    # -- severity helper ---------------------------------------------------
    def _doc_sev(self):
        """Severity for standards the document marks required but the ADC
        does not enforce in released files."""
        return "error" if self.profile == "doc" else "warning"

    def add(self, rule, severity, section, target, message):
        self.report.add(rule, severity, section, target, message)

    # -- entry point -------------------------------------------------------
    def run(self):
        self.check_filename()
        if netCDF4 is None:
            self.add("SYS-001", "error", "-", "-",
                     "netCDF4 is not installed; only the filename was checked")
            return self.report
        try:
            self.nc = netCDF4.Dataset(self.path)
        except Exception as exc:
            self.add("FILE-001", "error", "4.0", self.fname,
                     f"file cannot be opened as netCDF: {exc}")
            return self.report
        try:
            self.nc.set_auto_maskandscale(False)
            self.collect_info()
            self.check_format()
            self.check_globals()
            self.check_dimensions()
            self.check_time()
            self.check_coordinates()
            self.check_location()
            self.check_variables()
            self.check_qc()
            self.check_state_vars()
            self.check_source()
            self.check_level_requirements()
        finally:
            self.nc.close()
        return self.report

    # -- 0. context --------------------------------------------------------
    def collect_info(self):
        nc = self.nc
        self.report.info = {
            "format": nc.file_format,
            "datastream": str(_attr(nc, "datastream", "<missing>")),
            "n_vars": len(nc.variables),
            "n_dims": len(nc.dimensions),
            "n_times": len(nc.dimensions["time"]) if "time" in nc.dimensions else None,
        }
        self.qc_vars = {}       # qc var name -> data var name(s)
        self.source_vars = set()
        self.bounds_vars = set()
        for name, var in nc.variables.items():
            if name.startswith("qc_"):
                self.qc_vars[name] = name[3:]
            if name.startswith("source_"):
                self.source_vars.add(name)
            b = _attr(var, "bounds")
            if isinstance(b, str) and b.strip():
                self.bounds_vars.add(b.strip())

    # -- 5.1 filename ------------------------------------------------------
    def check_filename(self):
        f = self.fname
        m = FILENAME_RE.match(f)
        if not m:
            self.add("FILE-002", "error", "5.1", f,
                     "filename does not match "
                     "(sss)(inst)(qualifier)(temporal)(Fn).(dl).(yyyymmdd).(hhmmss).nc")
            # still try the length rules on whatever we have
        else:
            self.fn = m.groupdict()
        if len(f) > 60:
            self.add("FILE-003", "error", "5.1.1", f,
                     f"filename is {len(f)} characters; the ADC limit is 60 "
                     "(4 are reserved for the archive version suffix)")
        if not re.fullmatch(r"[A-Za-z0-9.]+", f):
            bad = sorted(set(re.findall(r"[^A-Za-z0-9.]", f)))
            self.add("FILE-004", "error", "5.1", f,
                     f"illegal character(s) {bad} in filename; only a-z A-Z 0-9 and '.' are allowed")
        if not self.fn:
            return
        d = self.fn
        if len(d["datastream"]) + 1 + len(d["level"]) > 33:
            self.add("FILE-005", "error", "5.1.1", f,
                     f"datastream '{d['datastream']}.{d['level']}' is "
                     f"{len(d['datastream']) + 1 + len(d['level'])} characters; the ADC limit is 33")
        if len(d["inst"]) > 24:
            self.add("FILE-006", "error", "5.1.1", f,
                     f"instrument description '{d['inst']}' is {len(d['inst'])} "
                     "characters; the ADC limit is 24")
        if d["ext"] == "cdf":
            self.add("FILE-007", "warning", "5.1", f,
                     "'.cdf' is allowed for historical data only; use '.nc' for new "
                     "and reprocessed files")
        # date / time validity
        try:
            _dt.datetime.strptime(d["date"], "%Y%m%d")
        except ValueError:
            self.add("FILE-008", "error", "5.1", f,
                     f"'{d['date']}' is not a valid UTC yyyymmdd date")
        hh, mm, ss = int(d["time"][:2]), int(d["time"][2:4]), int(d["time"][4:])
        if hh > 23 or mm > 59 or ss > 59:
            self.add("FILE-009", "error", "5.1", f,
                     f"time '{d['time']}' exceeds 23:59:59, which breaks time-conversion tools")
        if d["fac"][0] not in FACILITY_LETTERS:
            self.add("FILE-010", "warning", "5.1.2", f,
                     f"facility letter '{d['fac'][0]}' is not one of the designations "
                     f"defined in section 5.1.2 ({''.join(sorted(FACILITY_LETTERS))})")
        if re.match(r"^0\d$", d["fac"][1:]):
            self.add("FILE-011", "info", "5.1.2", f,
                     f"facility '{d['fac']}' is zero-padded; '{d['fac'][0]}{int(d['fac'][1:])}' "
                     "is a different facility, and padding at fixed sites is not recommended")
        if re.search(r"\d$", d["inst"]):
            self.add("FILE-012", "info", "5.1", f,
                     f"instrument/qualifier '{d['inst']}' ends with a digit, which can be "
                     "confused with a temporal-resolution descriptor; allowed when the "
                     "digit enumerates instruments or versions")

    # -- 4.0 format --------------------------------------------------------
    def check_format(self):
        fmt = self.nc.file_format
        if fmt.startswith("NETCDF3"):
            return
        if fmt == "NETCDF4_CLASSIC":
            self.add("FMT-001", "info", "4.0", self.fname,
                     "netCDF-4 classic model: allowed for high-volume data to use "
                     "compression, and expected to reduce volume by at least 50%")
        elif fmt == "NETCDF4":
            self.add("FMT-002", "warning", "4.0", self.fname,
                     "netCDF-4 (extended model) is used; ARM's preferred final format is "
                     "the netCDF-3 model, with netCDF-4 *classic* allowed for compression")

    # -- 6.7 global attributes --------------------------------------------
    def check_globals(self):
        nc = self.nc
        present = list(nc.ncattrs())
        pset = set(present)

        for a in CORE_GLOBAL_ATTRS:
            if a not in pset:
                self.add("GLB-001", "error", "6.7.1", "global",
                         f"required global attribute '{a}' is missing")
        missing_doc = [a for a in DOC_GLOBAL_ATTRS if a not in pset]
        if missing_doc:
            self.add("GLB-002", self._doc_sev(), "6.7.1", "global",
                     f"absent: {', '.join(missing_doc)} -- printed bold-underline (therefore "
                     "required) in section 6.7.1, but ARM's own released files usually omit "
                     "these; run with --profile doc to treat them as errors")
        missing_cond = [a for a in CONDITIONAL_GLOBAL_ATTRS if a not in pset]
        if missing_cond:
            self.add("GLB-003", "info", "6.7.1", "global",
                     "absent, required only under their stated condition: "
                     + "; ".join(f"{a} ({CONDITIONAL_GLOBAL_ATTRS[a]})" for a in missing_cond))

        # every global attribute must have a value
        for a in present:
            v = _attr(nc, a)
            if isinstance(v, str) and not v.strip():
                self.add("GLB-004", "error", "6.7", "global",
                         f"global attribute '{a}' has an empty value; if unknown use "
                         "'unknown', -9999, or 'N/A'")

        # Conventions must carry the ARM version token
        conv = _attr(nc, "Conventions")
        if isinstance(conv, str) and conv:
            if not re.search(r"\bARM-\d+(\.\d+)?\b", conv):
                self.add("GLB-005", "error", "6.7.1", "global",
                         f"Conventions = '{conv}' does not contain an 'ARM-<version>' token "
                         "(e.g. 'ARM-1.3'); the ARM convention should be listed first")
            elif not conv.strip().startswith("ARM-"):
                self.add("GLB-006", "info", "6.7.1", "global",
                         "ARM convention is recommended to be listed first in Conventions")

        # datastream == site_id + platform_id + facility_id + '.' + data_level
        site, plat = _attr(nc, "site_id"), _attr(nc, "platform_id")
        fac, lvl = _attr(nc, "facility_id"), _attr(nc, "data_level")
        ds = _attr(nc, "datastream")
        fac_code = fac
        if isinstance(fac, str):
            _m = re.match(r"^([A-Z]\d{1,2})\s*(?::\s*(.+))?$", fac.strip())
            fac_code = _m.group(1) if _m else None
        if all(isinstance(x, str) for x in (site, plat, fac_code, lvl, ds)):
            expect = f"{site}{plat}{fac_code}.{lvl}"
            if ds != expect:
                self.add("GLB-007", "error", "6.7.1", "global",
                         f"datastream = '{ds}' but site_id+platform_id+facility_id.data_level "
                         f"gives '{expect}'")
        if isinstance(site, str) and not re.fullmatch(r"[a-z]{3}", site):
            self.add("GLB-008", "error", "6.7.1", "global",
                     f"site_id = '{site}' is not a three-letter lower-case site designation")
        if isinstance(fac, str):
            m = re.match(r"^([A-Z]\d{1,2})\s*(?::\s*(.+))?$", fac.strip())
            if not m:
                self.add("GLB-009", "error", "5.1/6.7.1", "global",
                         f"facility_id = '{fac}' does not start with a capital letter followed "
                         "by one or two digits")
                fac_code = None
            else:
                fac_code = m.group(1)
                if m.group(2):
                    self.add("GLB-009b", "warning", "6.7.1", "global",
                             f"facility_id = '{fac}' appends a description; the documented value "
                             f"is the identifier alone ('{fac_code}') -- the location belongs in "
                             "location_description. Some ARM ingests do carry this longer form")
        if isinstance(lvl, str) and not re.fullmatch(r"\d{2}|[a-z]\d", lvl):
            self.add("GLB-010", "error", "5.1.3", "global",
                     f"data_level = '{lvl}' is not two digits (RAW) or one lower-case "
                     "letter followed by one digit")

        # filename vs header
        if self.fn:
            if isinstance(ds, str) and ds and ds != f"{self.fn['datastream']}.{self.fn['level']}":
                self.add("GLB-011", "error", "6.7.1", "global",
                         f"datastream = '{ds}' disagrees with the filename datastream "
                         f"'{self.fn['datastream']}.{self.fn['level']}'")
            if isinstance(lvl, str) and lvl and lvl != self.fn["level"]:
                self.add("GLB-012", "error", "6.7.1", "global",
                         f"data_level = '{lvl}' disagrees with the filename data level "
                         f"'{self.fn['level']}'")
            if isinstance(fac_code, str) and fac_code and fac_code != self.fn["fac"]:
                self.add("GLB-013", "error", "6.7.1", "global",
                         f"facility_id = '{fac_code}' disagrees with the filename facility "
                         f"'{self.fn['fac']}'")
            if isinstance(site, str) and site and site != self.fn["site"]:
                self.add("GLB-014", "error", "6.7.1", "global",
                         f"site_id = '{site}' disagrees with the filename site '{self.fn['site']}'")

        # doi
        doi = _attr(nc, "doi")
        if isinstance(doi, str) and doi.strip() and doi.strip().lower() not in ("unknown", "n/a"):
            if not re.match(r"^(doi:)?10\.\d{4,9}/\S+$", doi.strip()):
                self.add("GLB-015", "warning", "6.7.1", "global",
                         f"doi = '{doi}' is not of the form '10.xxxx/yyyy'")
        inst = _attr(nc, "institution")
        if isinstance(inst, str) and inst and inst.strip() != INSTITUTION_VALUE:
            self.add("GLB-016", "warning", "6.7.1", "global",
                     "institution must match the value fixed by the standard exactly: "
                     f"'{INSTITUTION_VALUE}'")
        if "history" in pset and present[-1] != "history":
            self.add("GLB-017", "info", "6.7.1", "global",
                     f"history is strongly recommended to be the last global attribute "
                     f"(currently followed by '{present[-1]}')")
        for a, val in (("sampling_interval", _attr(nc, "sampling_interval")),
                       ("averaging_interval", _attr(nc, "averaging_interval"))):
            if isinstance(val, str) and val.strip() and val.strip().lower() not in ("unknown", "n/a"):
                if not re.fullmatch(r"-?\d+(\.\d+)?\s+\S+", val.strip()):
                    self.add("GLB-018", "warning", "6.7.1", "global",
                             f"{a} = '{val}' should be a value and a UDUNITS descriptor "
                             "separated by a single space (e.g. '400 us', '5 minute')")
                else:
                    bad = check_units_string(val.strip().split()[1])
                    if bad:
                        self.add("GLB-019", "warning", "6.7.1", "global",
                                 f"{a} = '{val}': unit '{bad[0]}' is not recognised as UDUNITS")
        sh = _attr(nc, "sensor_height")
        if isinstance(sh, str) and sh.strip():
            self._check_sensor_height("global", sh)
        ids = _attr(nc, "input_datastreams")
        if isinstance(ids, str) and ids.strip() and ":" not in ids:
            self.add("GLB-020", "warning", "6.7.1", "global",
                     "input_datastreams should itemise 'datastream : version : date-range' "
                     "entries separated by ' : ' and ' ;\\n '")
        loc = _attr(nc, "location_description")
        if isinstance(loc, str) and loc.strip() and "(" not in loc:
            self.add("GLB-021", "info", "6.7.1", "global",
                     "location_description is recommended to spell out the region or campaign "
                     "followed by its acronym in parentheses, then the nearest town")
        # QC declared at global level
        self.global_qc_bits = _bit_indices(pset, "qc_bit")
        self.global_qc_flags = _bit_indices(pset, "qc_flag")
        for kind, idx in (("bit", self.global_qc_bits), ("flag", self.global_qc_flags)):
            for n in idx:
                if f"qc_{kind}_{n}_assessment" not in pset:
                    self.add("GLB-022", "error", "6.8.7/6.8.12", "global",
                             f"qc_{kind}_{n}_description is declared without a matching "
                             f"qc_{kind}_{n}_assessment")
                else:
                    a = _attr(nc, f"qc_{kind}_{n}_assessment")
                    if isinstance(a, str) and a not in ASSESSMENTS:
                        self.add("GLB-023", "error", "6.8.3", "global",
                                 f"qc_{kind}_{n}_assessment = '{a}'; only 'Bad' and "
                                 "'Indeterminate' are allowed")

    def _check_sensor_height(self, target, value):
        parts = str(value).split()
        ok = len(parts) == 3 and parts[2] == "AGL"
        if ok:
            try:
                float(parts[0])
            except ValueError:
                ok = False
            if check_units_string(parts[1]):
                ok = False
        if not ok:
            self.add("ATT-020", "error", "6.6.6", target,
                     f"sensor_height = '{value}'; the format is "
                     "'<value> <udunits unit> AGL' separated by single spaces")

    # -- 6.1 dimensions ----------------------------------------------------
    def check_dimensions(self):
        nc = self.nc
        if "time" not in nc.dimensions:
            self.add("DIM-001", "error", "6.1.1", "dimensions",
                     "no 'time' dimension; the time dimension is required and defined as unlimited")
            return
        if not nc.dimensions["time"].isunlimited():
            self.add("DIM-002", "error", "6.1.1", "time",
                     "the time dimension must be declared UNLIMITED so files concatenate")
        # time must be the first dimension of any variable that uses it
        for name, v in nc.variables.items():
            if "time" in v.dimensions and v.dimensions[0] != "time":
                self.add("DIM-003", "error", "6.1.1", name,
                         f"dimensions are {v.dimensions}; 'time' must be the first dimension")
        order = list(nc.dimensions)
        if order and order[0] != "time":
            self.add("DIM-004", "info", "6.1.1", "dimensions",
                     f"dimension definitions are recommended to start with time "
                     f"(currently start with '{order[0]}')")

    # -- 6.1.2 / 6.1.3 time ------------------------------------------------
    def check_time(self):
        nc = self.nc
        v = nc.variables
        for name in ("base_time", "time_offset", "time"):
            if name not in v:
                self.add("TIM-001", "error", "6.1.2/6.1.3", name,
                         f"'{name}' is missing; both the base_time/time_offset and the CF "
                         "time formats must be declared in a processed netCDF file")
        # --- base_time
        if "base_time" in v:
            bt = v["base_time"]
            if bt.ndim != 0 and bt.size != 1:
                self.add("TIM-002", "error", "6.1.2", "base_time",
                         f"base_time must be a single scalar value (shape {bt.shape})")
            if _numeric_kind(bt.dtype) not in "iu":
                self.add("TIM-003", "error", "6.1.2", "base_time",
                         f"base_time must be a long integer (found {bt.dtype})")
            u = _attr(bt, "units", "")
            if not re.match(r"^seconds since 1970-0?1-0?1", str(u)):
                self.add("TIM-004", "error", "6.1.2", "base_time",
                         f"units = '{u}'; base_time is epoch time, "
                         "'seconds since 1970-1-1 0:00:00 0:00'")
            if not _has(bt, "string"):
                self.add("TIM-005", "warning", "6.1.2", "base_time",
                         "the 'string' attribute giving the human-readable base time "
                         "(e.g. '18-Sep-2012,00:00:00 GMT') is missing")
            if _attr(bt, "ancillary_variables") != "time_offset":
                self.add("TIM-006", "error", "6.1.2", "base_time",
                         "ancillary_variables must be set to 'time_offset' to link the pair")
            if not _has(bt, "long_name"):
                self.add("TIM-007", "error", "6.6.1", "base_time", "long_name is missing")
        # --- time_offset
        if "time_offset" in v:
            to = v["time_offset"]
            if to.dimensions != ("time",):
                self.add("TIM-008", "error", "6.1.2", "time_offset",
                         f"time_offset must be dimensioned by time (found {to.dimensions})")
            if _numeric_kind(to.dtype) != "f" or np.dtype(to.dtype).itemsize < 8:
                self.add("TIM-009", "warning", "6.1.2", "time_offset",
                         f"time_offset is stored as {to.dtype}; the standard specifies "
                         "double precision so microsecond steps are representable")
            if _attr(to, "ancillary_variables") != "base_time":
                self.add("TIM-010", "error", "6.1.2", "time_offset",
                         "ancillary_variables must be set to 'base_time' to link the pair")
        # --- time
        if "time" in v:
            t = v["time"]
            if "time" not in nc.dimensions or t.dimensions != ("time",):
                self.add("TIM-011", "error", "6.1.3", "time",
                         "time must be a coordinate variable: same name as the time dimension")
            u = str(_attr(t, "units", ""))
            if " since " not in u:
                self.add("TIM-012", "error", "6.1.3", "time",
                         f"units = '{u}'; a CF '<unit> since <timestamp>' form is required")
            elif not u.startswith("seconds since"):
                sev = "warning" if not u.startswith(("months since", "years since")) else "error"
                self.add("TIM-013", sev, "6.1.3", "time",
                         f"units = '{u}'; 'seconds since' is the recommended convention "
                         "('months since'/'years since' are not recommended unless explicitly defined)")
            if _attr(t, "standard_name") != "time":
                self.add("TIM-014", "error", "6.1.3", "time",
                         "standard_name = 'time' is required on the CF time coordinate")
            cal = _attr(t, "calendar")
            if cal is not None and str(cal).lower() not in ("gregorian", "standard", "proleptic_gregorian"):
                self.add("TIM-015", "warning", "6.1.1", "time",
                         f"calendar = '{cal}'; ARM uses the Gregorian calendar and deviating "
                         "from it is not recommended")
            if self.fn and " since " in u:
                mid = f"{self.fn['date'][:4]}-{self.fn['date'][4:6]}-{self.fn['date'][6:]}"
                if mid not in u:
                    self.add("TIM-016", "info", "6.1.1", "time",
                             f"units epoch '{u}' is not midnight of the file date {mid}; "
                             "starting time at UTC midnight is recommended")
        if not self.read_data:
            return
        # --- values
        nt = len(nc.dimensions["time"]) if "time" in nc.dimensions else 0
        if nt == 0 or nt > self.data_limit:
            return
        tvals = None
        if "time" in v:
            try:
                tvals = np.asarray(v["time"][:], dtype="f8").ravel()
            except Exception:
                tvals = None
        if tvals is not None and tvals.size:
            if not np.all(np.isfinite(tvals)):
                self.add("TIM-017", "error", "6.1.1", "time",
                         f"{int((~np.isfinite(tvals)).sum())} non-finite time value(s); the time "
                         "variable in any non-RAW file may not have a missing value or NaN")
            fin = tvals[np.isfinite(tvals)]
            if fin.size > 1:
                d = np.diff(fin)
                if np.any(d == 0):
                    self.add("TIM-018", "error", "6.1.1", "time",
                             f"{int((d == 0).sum())} repeated time value(s); time may not repeat")
                if np.any(d < 0):
                    self.add("TIM-019", "error", "6.1.1", "time",
                             f"time decreases at {int((d < 0).sum())} step(s); time must be increasing")
            mv = _attr(v["time"], "missing_value", _attr(v["time"], "_FillValue"))
            if mv is not None:
                self.add("TIM-020", "error", "6.6.2", "time",
                         "a coordinate variable may not declare missing_value or _FillValue")
        # base_time + time_offset[0] vs the filename timestamp
        if self.fn and "base_time" in v and "time_offset" in v:
            try:
                bt = float(_as_scalar(v["base_time"][...]))
                t0 = float(np.asarray(v["time_offset"][:1]).ravel()[0])
                stamp = _dt.datetime(1970, 1, 1) + _dt.timedelta(seconds=bt + t0)
                want = _dt.datetime.strptime(self.fn["date"] + self.fn["time"], "%Y%m%d%H%M%S")
                if abs((stamp - want).total_seconds()) >= 1:
                    self.add("TIM-021", "error", "6.1.2", "base_time",
                             f"base_time + time_offset[0] = {stamp:%Y-%m-%d %H:%M:%S} UTC but the "
                             f"filename says {want:%Y-%m-%d %H:%M:%S}; they must agree")
            except Exception:
                pass
        # time bounds
        if "time" in v:
            self._check_bounds("time")

    def _check_bounds(self, name):
        nc, v = self.nc, self.nc.variables
        b = _attr(v[name], "bounds")
        if b is None:
            cm = str(_attr(v[name], "cell_methods", ""))
            if name == "time":
                self.add("BND-001", "info", "6.1.4", "time",
                         "no time bounds variable; for all non-instantaneous data the "
                         "bounds of each averaging period are required")
            return
        if b not in v:
            self.add("BND-002", "error", "6.1.4/6.2.3", name,
                     f"bounds = '{b}' but no such variable exists")
            return
        bv = v[b]
        if bv.ndim != 2 or bv.dimensions[0] != name:
            self.add("BND-003", "error", "6.1.4", b,
                     f"a bounds variable must be dimensioned ({name}, bound); found {bv.dimensions}")
        elif len(nc.dimensions[bv.dimensions[1]]) != 2:
            self.add("BND-004", "error", "6.1.4", b,
                     f"the bounds dimension '{bv.dimensions[1]}' has length "
                     f"{len(nc.dimensions[bv.dimensions[1]])}; it must be 2")
        if _has(bv, "missing_value") or _has(bv, "_FillValue"):
            self.add("BND-005", "error", "6.1.4", b,
                     "a bounds variable may not have missing values")
        bo = _attr(bv, "bound_offsets")
        if bo is not None and np.asarray(bo).size != 2:
            self.add("BND-006", "warning", "6.1.4", b,
                     "bound_offsets declares the constant width of each range and must have "
                     "two values; omit it when the ranges are not consistent")

    # -- 6.2 coordinate dimensions ----------------------------------------
    def check_coordinates(self):
        nc = self.nc
        string_like = set()
        for name, var in nc.variables.items():
            if var.dtype == str or _numeric_kind(var.dtype) in "SU":
                string_like.update(var.dimensions[1:])
        for dim in nc.dimensions:
            if dim == "time":
                continue
            if dim in nc.variables:
                continue
            if dim in string_like or re.search(r"(string|strlen|char|bound|bnds|_len)", dim, re.I):
                continue  # index/string dimensions need no coordinate variable
            self.add("CRD-001", "warning", "6.2", dim,
                     "dimension has no same-named coordinate variable; one with long_name "
                     "and units is recommended unless the dimension is a string length or index")
        for name in nc.variables:
            if name in ("time", "time_offset", "base_time"):
                continue
            if not _is_coordinate_var(nc, name):
                continue
            var = nc.variables[name]
            # long_name / units on a coordinate variable are covered by
            # ATT-001 / ATT-003 (6.6.1); not repeated here.
            if _has(var, "missing_value") or _has(var, "_FillValue"):
                self.add("CRD-003", "error", "6.2", name,
                         "a coordinate variable may not have missing_value or _FillValue")
            if self.read_data and var.size and var.size <= self.data_limit:
                try:
                    vals = np.asarray(var[:], dtype="f8").ravel()
                except Exception:
                    vals = None
                if vals is not None and vals.size:
                    if not np.all(np.isfinite(vals)):
                        self.add("CRD-004", "error", "6.2", name,
                                 "coordinate variable contains NaN or non-finite values")
                    elif not _monotonic(vals):
                        self.add("CRD-005", "error", "6.2", name,
                                 "coordinate variable must be monotonically increasing or decreasing")
            # frame of reference for vertical coordinates
            u = str(_attr(var, "units", ""))
            sn = _attr(var, "standard_name")
            if re.fullmatch(r"(m|km|cm|mm|meter|metre|meters|metres|ft|feet)", u.strip()) \
                    and re.search(r"(height|alt|range|depth|level)", name, re.I):
                if sn is None:
                    self.add("CRD-006", "warning", "6.2.1/6.2.2", name,
                             "a vertical coordinate must document its frame of reference with "
                             "standard_name: 'height' for AGL, 'altitude' for MSL "
                             "(long_name is not the official method)")
                elif sn not in ("height", "altitude", "depth"):
                    self.add("CRD-007", "info", "6.2.1", name,
                             f"standard_name = '{sn}'; AGL is declared with 'height' and MSL "
                             "with 'altitude'")
            self._check_bounds(name)

    # -- 6.3 location variables -------------------------------------------
    def check_location(self):
        nc = self.nc
        wanted = {
            "lat": ("latitude", ("degree_N", "degrees_north", "degree_north", "degrees_N")),
            "lon": ("longitude", ("degree_E", "degrees_east", "degree_east", "degrees_E")),
            "alt": ("altitude", ("m", "meter", "metre", "meters")),
        }
        for name, (sn, units) in wanted.items():
            if name not in nc.variables:
                self.add("LOC-001", "error", "6.3", name,
                         f"location variable '{name}' is missing; the names lat, lon and alt "
                         "are required for consistency with historical data")
                continue
            var = nc.variables[name]
            u = str(_attr(var, "units", "")).strip()
            if u not in units:
                sev = "error" if name != "alt" else "warning"
                self.add("LOC-002", sev, "6.3", name,
                         f"units = '{u}'; the standard requires "
                         f"{' or '.join(units[:2])} for {name}")
            got = _attr(var, "standard_name")
            if got != sn:
                self.add("LOC-003", "error", "6.3", name,
                         f"standard_name = {got!r}; '{sn}' is required")
            if not _has(var, "long_name"):
                self.add("LOC-004", "error", "6.6.1", name, "long_name is missing")
            if name in ("lat", "lon") and self.read_data:
                lim = 90.0 if name == "lat" else 180.0
                try:
                    vals = np.asarray(var[...], dtype="f8").ravel()
                    vals = vals[np.isfinite(vals)]
                except Exception:
                    vals = np.array([])
                if vals.size and (np.nanmax(np.abs(vals)) > lim):
                    self.add("LOC-005", "error", "6.3", name,
                             f"values reach {np.nanmax(np.abs(vals)):.4g}, outside "
                             f"+/-{lim:g} {name}")
                for a, want in (("valid_min", -lim), ("valid_max", lim)):
                    if not _has(var, a):
                        self.add("LOC-006", "info", "6.3", name,
                                 f"{a} is not declared; the standard's example sets "
                                 f"{a} = {want:g} to mark the limits of usable values")

    # -- 6.4 / 6.6 variables ----------------------------------------------
    def check_variables(self):
        nc = self.nc
        cf = cf_standard_names()
        long_names = defaultdict(list)
        for name, var in nc.variables.items():
            # -- naming, 6.4
            if not re.match(r"^[A-Za-z]", name):
                self.add("VAR-001", "error", "6.4", name,
                         "the first character of a variable name must be a letter")
            if not re.fullmatch(r"[A-Za-z0-9_]+", name):
                self.add("VAR-002", "error", "6.4", name,
                         "only letters, numbers and underscores are allowed in a variable name")
            if len(name) > 64:
                self.add("VAR-003", "error", "6.4", name,
                         f"variable name is {len(name)} characters; the ADC limit is 64")
            if len(name) == 1:
                self.add("VAR-004", "info", "6.4", name, "single-character names are not recommended")
            if re.search(r"[A-Z]", name):
                self.add("VAR-005", "info", "6.4", name,
                         "upper-case letters should be used sparingly in variable names")

            is_coord = _is_coordinate_var(nc, name)
            is_qc = name in self.qc_vars
            is_src = name in self.source_vars
            # A bounds variable is exempt: 6.1.4 makes long_name recommended and
            # units not recommended; 6.2.3 makes both recommended, not required.
            is_bounds = name in self.bounds_vars

            # -- required attributes, 6.6.1
            ln = _attr(var, "long_name")
            if ln is None:
                self.add("ATT-001", "info" if is_bounds else "error", "6.6.1", name,
                         "long_name is recommended on a bounds variable" if is_bounds
                         else "long_name is required")
            else:
                long_names[str(ln).strip()].append(name)
                if str(ln)[:1].islower():
                    self.add("ATT-002", "info", "6.6.1", name,
                             "the first letter of long_name is recommended to be capitalised")
            u = _attr(var, "units")
            if u is None:
                if is_bounds:
                    pass            # 6.1.4: the units attribute is not recommended here
                elif _numeric_kind(var.dtype) in "SU" or var.dtype == str:
                    self.add("ATT-003", "warning", "6.6.1", name,
                             "units is required on every variable; character variables use '1'")
                else:
                    self.add("ATT-003", "error", "6.6.1", name, "units is required")
            else:
                us = str(u).strip()
                if us.lower() in ("unitless", "none", "na", "n/a", ""):
                    self.add("ATT-004", "error", "6.6.1", name,
                             f"units = '{u}'; unitless quantities are represented by the "
                             "UDUNITS value '1'")
                else:
                    bad = check_units_string(us)
                    if bad:
                        self.add("ATT-005", "warning", "6.6.1/App. C", name,
                                 f"units = '{us}': symbol(s) {bad} not recognised as UDUNITS; "
                                 "verify against the UDUNITS-2 database and Appendix C")

            # -- standard_name, 6.6.4
            sn = _attr(var, "standard_name")
            if sn is not None and cf:
                if str(sn) not in cf:
                    import difflib
                    near = difflib.get_close_matches(str(sn), cf, n=2, cutoff=0.75)
                    hint = f"; nearest CF name(s): {', '.join(near)}" if near else ""
                    self.add("ATT-006", "error", "6.6.4", name,
                             f"standard_name = '{sn}' is not in the CF standard-name table; "
                             f"inventing a new value is not allowed{hint}")

            # -- missing_value / _FillValue, 6.6.2 / 6.6.7
            mv, fv = _attr(var, "missing_value"), _attr(var, "_FillValue")
            if not is_coord:
                for a, val in (("missing_value", mv), ("_FillValue", fv)):
                    if val is None:
                        continue
                    if not _same_numeric_type(val, var.dtype):
                        self.add("ATT-007", "error", "6.6.7", name,
                                 f"{a} is stored as {np.asarray(val).dtype} but the variable is "
                                 f"{var.dtype}; attributes used directly with the values must "
                                 "match the variable type")
                if mv is not None and fv is not None:
                    try:
                        if float(_as_scalar(mv)) != float(_as_scalar(fv)):
                            self.add("ATT-008", "warning", "6.6.3", name,
                                     f"missing_value ({_as_scalar(mv)}) and _FillValue "
                                     f"({_as_scalar(fv)}) differ; using the same value for both "
                                     "is recommended so users mask one value, not two")
                    except (TypeError, ValueError):
                        pass
            for a in ("valid_min", "valid_max", "valid_range"):
                val = _attr(var, a)
                if val is None:
                    continue
                if not _same_numeric_type(val, var.dtype):
                    self.add("ATT-009", "error", "6.6.7", name,
                             f"{a} is stored as {np.asarray(val).dtype} but the variable is "
                             f"{var.dtype}; the types must match")
                if not is_coord and name not in ("lat", "lon", "alt") and not is_qc:
                    self.add("ATT-010", "warning", "6.8.8", name,
                             f"{a} is present on a data variable; valid_min/valid_max are "
                             "absolute limits of usable data, not QC limits -- use fail_min/"
                             "fail_max (or warn_min/warn_max) on the QC variable instead")
            # -- other ARM attributes
            if _has(var, "sensor_height"):
                self._check_sensor_height(name, _attr(var, "sensor_height"))
            for a in var.ncattrs():
                if a.startswith("_"):
                    continue
                if not re.fullmatch(r"[a-z][a-z0-9_]*", a):
                    self.add("ATT-011", "info", "6.6", name,
                             f"attribute '{a}': variable attribute names are lower case with "
                             "words separated by underscores")
            ncomment = sum(1 for a in var.ncattrs() if re.fullmatch(r"comment_\d+", a))
            if ncomment > 1:
                self.add("ATT-012", "info", "6.6", name,
                         f"{ncomment} comment_<#> attributes; a single lengthy comment, or "
                         "descriptively named comments, are preferred")
            # -- ancillary_variables must resolve, 6.8.2
            av = _attr(var, "ancillary_variables")
            if isinstance(av, str) and av.strip():
                for ref in av.split():
                    if ref not in nc.variables:
                        self.add("ATT-013", "error", "6.8.2", name,
                                 f"ancillary_variables references '{ref}', which is not a "
                                 "variable in this file")
            if _has(var, "ancillary_variable") and not _has(var, "ancillary_variables"):
                self.add("ATT-014", "warning", "6.8.2", name,
                         "attribute is spelled 'ancillary_variable'; the CF/ARM attribute is "
                         "'ancillary_variables' (plural)")
            # -- cell_methods / cell_transforms, 6.2.5 / 6.10
            cm = _attr(var, "cell_methods")
            if isinstance(cm, str) and cm.strip():
                for dim in re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", cm):
                    if dim not in nc.dimensions and dim not in ("interval", "comment", "area"):
                        self.add("ATT-015", "warning", "6.2.5", name,
                                 f"cell_methods names '{dim}', which is not a dimension of "
                                 "this file")
            ct = _attr(var, "cell_transforms")
            if isinstance(ct, str) and ct.strip():
                for tt in re.findall(r"TRANS_[A-Z_]+", ct):
                    if tt not in TRANSFORM_TYPES:
                        self.add("ATT-016", "error", "6.10.1", name,
                                 f"cell_transforms uses unknown transform type '{tt}'; "
                                 f"allowed: {', '.join(TRANSFORM_TYPES)}")
                if not re.search(r"TRANS_[A-Z_]+", ct):
                    self.add("ATT-017", "error", "6.10.1", name,
                             "cell_transforms must state a transform type per dimension "
                             "('dimension: TRANS_TYPE (param: value)')")
            # -- source attribute syntax, 6.9.1
            src = _attr(var, "source")
            if isinstance(src, str) and src.strip():
                self._check_source_attr(name, src)
        # -- long_name uniqueness, 6.6.1
        for ln, names in long_names.items():
            if len(names) > 1:
                self.add("ATT-018", "error", "6.6.1", ",".join(sorted(names)[:3]),
                         f"long_name '{ln}' is shared by {len(names)} variables; it must be "
                         "unique within the file")

    def _check_source_attr(self, name, src):
        nc = self.nc
        if src.strip() == "no_source_available":
            return
        for token in src.split():
            if ":" in token:
                ds, _, varname = token.partition(":")
                if not varname:
                    self.add("SRC-001", "warning", "6.9.1", name,
                             f"source token '{token}' has no variable after the colon; the "
                             "syntax is '<datastream>:<variable>' or "
                             "'<instrument_class>.<level>:<variable>'")
                elif "." not in ds:
                    self.add("SRC-002", "warning", "6.9.1", name,
                             f"source token '{token}': the datastream part should carry a "
                             "'.<level>' (e.g. 'mwr.b1:vap' or 'sgpmwrC1.b1:vap')")
            else:
                if token not in nc.variables:
                    self.add("SRC-003", "info", "6.9.1", name,
                             f"source token '{token}' matches no variable in this file, so it "
                             "is read as an algorithm name; algorithm identifiers must not "
                             "contain a colon")

    # -- 6.8 quality control ----------------------------------------------
    def check_qc(self):
        nc = self.nc
        gbits, gflags = self.global_qc_bits, self.global_qc_flags
        for qname, base in self.qc_vars.items():
            qv = nc.variables[qname]
            attrs = set(qv.ncattrs())
            multi = base not in nc.variables    # summarising several variables

            # link from the data variable
            if not multi:
                dv = nc.variables[base]
                av = str(_attr(dv, "ancillary_variables", "") or "")
                if qname not in av.split():
                    self.add("QC-001", "error", "6.8.2", base,
                             f"data variable does not list '{qname}' in its "
                             "ancillary_variables attribute, which is required to link the pair")
            else:
                users = [n for n, v in nc.variables.items()
                         if qname in str(_attr(v, "ancillary_variables", "") or "").split()]
                if not users:
                    self.add("QC-002", "error", "6.8.9", qname,
                             "no data variable references this QC variable in its "
                             "ancillary_variables attribute")

            if _numeric_kind(qv.dtype) not in "iu":
                self.add("QC-003", "error", "6.8.2", qname,
                         f"QC variables are type integer (32-bit recommended); found {qv.dtype}")
            if str(_attr(qv, "units", "")).strip() != "1":
                self.add("QC-004", "error", "6.8.2", qname,
                         f"units = {_attr(qv, 'units')!r}; a QC variable requires units = '1'")
            ln = str(_attr(qv, "long_name", "") or "")
            if multi:
                if ln.strip() != "Quality check results":
                    self.add("QC-005", "error", "6.8.9", qname,
                             f"long_name = '{ln}'; a QC variable summarising several data "
                             "variables requires long_name = 'Quality check results'")
            else:
                want = str(_attr(nc.variables[base], "long_name", "") or "")
                if ln.startswith("Quality check results on field:"):
                    self.add("QC-006b", "warning", "3.1/6.8.2", qname,
                             "long_name uses the legacy wording 'on field:'; version 1.3 of the "
                             "standard uses the term 'variable' only, so the form is "
                             "'Quality check results on variable: <data variable long_name>'")
                elif not ln.startswith("Quality check results on variable:"):
                    self.add("QC-006", "error", "6.8.2", qname,
                             f"long_name = '{ln}'; the required form is "
                             "'Quality check results on variable: <data variable long_name>'")
                elif want and ln.split(":", 1)[1].strip().lower() != want.strip().lower():
                    self.add("QC-007", "warning", "6.8.2", qname,
                             f"long_name trailer '{ln.split(':', 1)[1].strip()}' does not match "
                             f"the data variable long_name '{want}'")
            # flag_method
            fm = _attr(qv, "flag_method")
            bits = _bit_indices(attrs, "bit")
            flags = _bit_indices(attrs, "flag")
            if fm is None:
                self.add("QC-008", "error", "6.8.2/6.8.11", qname,
                         "flag_method is required and must be 'bit' (bit-packed) or "
                         "'integer' (single-state)")
            elif str(fm) not in ("bit", "integer"):
                self.add("QC-009", "error", "6.8.2", qname,
                         f"flag_method = '{fm}'; only 'bit' and 'integer' are defined")
            if bits and flags:
                self.add("QC-010", "error", "6.8.11", qname,
                         "bit_<#>_* and flag_<#>_* attributes are both present; a QC variable "
                         "uses one method, not a mixture")
            if str(fm) == "bit" and flags and not bits:
                self.add("QC-011", "error", "6.8.11", qname,
                         "flag_method = 'bit' but the tests are declared with flag_<#>_* "
                         "attributes")
            if str(fm) == "integer" and bits and not flags:
                self.add("QC-012", "error", "6.8.11", qname,
                         "flag_method = 'integer' but the tests are declared with bit_<#>_* "
                         "attributes")
            # description
            desc = str(_attr(qv, "description", "") or "")
            if not desc.strip():
                self.add("QC-013", "error", "6.8.2", qname,
                         "the description attribute is required; it either carries the standard "
                         "explanation of the packing or points the user to the global attributes")
            else:
                pointer = "global attribute" in desc.lower()
                if pointer and not (gbits or gflags):
                    self.add("QC-014", "error", "6.8.7", qname,
                             "description points to the global attributes, but no "
                             "qc_bit_<#>_description / qc_flag_<#>_description globals exist")
                if pointer and (bits or flags):
                    self.add("QC-015", "error", "6.8.2", qname,
                             "QC test definitions appear at both variable and global level; for "
                             "a single variable they may occur in only one location")
                if not pointer:
                    want = QC_BIT_DESCRIPTION if str(fm) != "integer" else QC_INT_DESCRIPTION
                    if _norm(desc) != _norm(want):
                        self.add("QC-016", "info", "6.8.2/6.8.11", qname,
                                 "description differs from the wording given in the standard; "
                                 "the exact sentence is what automated tools look for")
            # per-bit declarations
            kind = "flag" if (flags and not bits) else "bit"
            idx = flags if kind == "flag" else bits
            if not idx and not (gbits or gflags):
                self.add("QC-017", "error", "6.8.3", qname,
                         "no bit_<#>_description / flag_<#>_description attributes and no "
                         "global declarations; the QC tests are undocumented")
            for n in idx:
                a = f"{kind}_{n}_assessment"
                if a not in attrs:
                    self.add("QC-018", "error", "6.8.3", qname,
                             f"{kind}_{n}_description is declared without a matching {a}")
                else:
                    val = _attr(qv, a)
                    if isinstance(val, str) and val not in ASSESSMENTS:
                        self.add("QC-019", "error", "6.8.3", qname,
                                 f"{a} = '{val}'; the only options are 'Bad' and 'Indeterminate'")
                if n < 0:
                    self.add("QC-020", "error", "6.8.11", qname,
                             f"{kind} number {n} is negative; numbers must be >= 0 because some "
                             "languages map attribute names onto program variables")
                if kind == "bit" and n == 0:
                    self.add("QC-021", "warning", "6.8.3", qname,
                             "bit numbering starts at 1 (bit 1 = 2^0 = integer 1)")
                d = str(_attr(qv, f"{kind}_{n}_description", "") or "")
                if d.strip().lower() == "not used" and str(_attr(qv, a, "")) != "Bad":
                    self.add("QC-022", "warning", "6.8.5", qname,
                             f"{kind} {n} is declared 'Not used' so {a} must be 'Bad'")
            if kind == "bit" and idx:
                gaps = [n for n in range(1, max(idx) + 1) if n not in idx]
                if gaps:
                    self.add("QC-023", "info", "6.8.5", qname,
                             f"bit(s) {gaps} are undeclared below the highest declared bit "
                             f"{max(idx)}; an undeclared bit is free, but a bit that must be "
                             "reserved is declared 'Not used' / 'Bad'")
            # dimensions
            if not multi:
                dv = nc.variables[base]
                if qv.dimensions != dv.dimensions:
                    if set(qv.dimensions) < set(dv.dimensions):
                        self.add("QC-024", "info", "6.8.10", qname,
                                 f"QC is dimensionally summarised ({qv.dimensions} vs "
                                 f"{dv.dimensions}); the summarising method must be described "
                                 "in an attribute or a technical document")
                    else:
                        self.add("QC-025", "error", "6.8.2", qname,
                                 f"dimensions {qv.dimensions} do not match the data variable's "
                                 f"{dv.dimensions}")
            # QC limit attribute types
            if not multi:
                dv_dtype = nc.variables[base].dtype
                for a in ("fail_min", "fail_max", "warn_min", "warn_max"):
                    val = _attr(qv, a)
                    if val is not None and not _same_numeric_type(val, dv_dtype):
                        self.add("QC-026", "warning", "6.6.7", qname,
                                 f"{a} is stored as {np.asarray(val).dtype}; a QC limit is "
                                 f"compared with the data variable, which is {dv_dtype}")
            # do the data use bits nobody declared?
            if self.read_data and idx and kind == "bit" and qv.size and qv.size <= self.data_limit:
                try:
                    vals = np.asarray(qv[:]).ravel()
                except Exception:
                    vals = np.array([], dtype="i8")
                if vals.size:
                    vals = vals[vals > 0].astype("i8", copy=False)
                    if vals.size:
                        declared = 0
                        for n in idx + gbits:
                            if n >= 1:
                                declared |= 1 << (n - 1)
                        extra = int(np.bitwise_or.reduce(vals)) & ~declared
                        if extra:
                            got = [i + 1 for i in range(32) if extra >> i & 1]
                            self.add("QC-027", "error", "6.8.3", qname,
                                     f"data set bit(s) {got} that no bit_<#>_description "
                                     "declares; every set bit must have a description")
            if not _has(qv, "standard_name"):
                self.add("QC-028", "info", "6.8.2", qname,
                         "standard_name = 'quality_flag' is recommended for QC variables")
            elif str(_attr(qv, "standard_name")) != "quality_flag":
                self.add("QC-029", "info", "6.8.2", qname,
                         f"standard_name = '{_attr(qv, 'standard_name')}'; the recommendation "
                         "for a QC variable is 'quality_flag'")
        # a data variable whose ancillary_variables names a missing qc_ partner
        for name, var in nc.variables.items():
            if name.startswith(("qc_", "source_")):
                continue
            av = str(_attr(var, "ancillary_variables", "") or "")
            for ref in av.split():
                if ref.startswith("qc_") and ref not in nc.variables:
                    self.add("QC-030", "error", "6.8.2", name,
                             f"ancillary_variables names QC variable '{ref}', which does not exist")

    # -- 6.5 state indicator variables ------------------------------------
    def check_state_vars(self):
        nc = self.nc
        for name, var in nc.variables.items():
            if name in self.qc_vars or name in self.source_vars:
                continue
            fvals, fmasks = _attr(var, "flag_values"), _attr(var, "flag_masks")
            fmeans = _attr(var, "flag_meanings")
            if fvals is None and fmasks is None and fmeans is None:
                continue
            if fvals is not None and fmasks is not None:
                self.add("STA-001", "error", "6.5", name,
                         "flag_values (exclusive states) and flag_masks (inclusive, bit-packed "
                         "states) are both declared; a state variable uses one method")
            if (fvals is not None or fmasks is not None) and fmeans is None:
                self.add("STA-002", "error", "6.5.1/6.5.2", name,
                         "flag_meanings is required alongside flag_values / flag_masks")
            # flag_values / flag_masks must be a numeric array, not text
            for aname, val in (("flag_values", fvals), ("flag_masks", fmasks)):
                if isinstance(val, (str, bytes)):
                    self.add("STA-008", "error", "6.5.1/6.5.2", name,
                             f"{aname} = {val!r} is stored as a character attribute; it must be "
                             "a numeric array of the same type as the variable "
                             "(e.g. flag_values = 0, 1, 2)")
            if fmeans is not None:
                means = str(fmeans).split()
                if any("-" in m for m in means):
                    self.add("STA-003", "info", "6.5.1", name,
                             "individual flag meanings are words joined with underscores")
                ref = fvals if fvals is not None else fmasks
                if ref is not None:
                    nref = _count_flag_values(ref)
                    if nref != len(means):
                        self.add("STA-004", "error", "6.5.1", name,
                                 f"{nref} flag value(s)/mask(s) but {len(means)} space-separated "
                                 "flag_meanings; the counts must match and a meaning may not "
                                 "contain spaces")
            if fmasks is not None:
                bad = [int(m) for m in np.asarray(fmasks).ravel()
                       if int(m) <= 0 or (int(m) & (int(m) - 1)) != 0]
                if bad:
                    self.add("STA-005", "error", "6.5.2", name,
                             f"flag_masks values {bad} are not powers of two")
            if _numeric_kind(var.dtype) == "f" and fvals is not None and fmasks is None:
                # A float variable carrying flag_values is not a state indicator
                # variable: it is a data variable with state values mixed into
                # the data, which 6.8.8 discusses at length.
                vmin, vmax = _attr(var, "valid_min"), _attr(var, "valid_max")
                vr = _attr(var, "valid_range")
                self.add("STA-009", "warning", "6.8.8", name,
                         "flag_values are mixed into a floating-point data variable; mixing "
                         "state or QC information with the observed values is not recommended")
                if vmin is None and vr is None:
                    self.add("STA-010", "error", "6.8.8", name,
                             "state values are embedded in the data but no valid_min/valid_range "
                             "is declared, so software cannot exclude them; the flag_values must "
                             "lie outside the valid range")
                else:
                    try:
                        lo = float(_as_scalar(vmin)) if vmin is not None \
                            else float(np.asarray(vr).ravel()[0])
                        if isinstance(fvals, (str, bytes)):
                            raw = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", str(fvals))]
                        else:
                            raw = [float(x) for x in np.asarray(fvals).ravel()]
                        inside = [x for x in raw if x >= lo]
                        if inside:
                            self.add("STA-011", "error", "6.8.8", name,
                                     f"flag_values {inside} are not below valid_min ({lo:g}); "
                                     "state values must fall outside the valid range so they are "
                                     "removed from analysis automatically")
                    except (TypeError, ValueError):
                        pass
            elif _numeric_kind(var.dtype) not in "iu":
                self.add("STA-006", "error", "6.5", name,
                         f"a state indicator variable is byte, short or long integer; "
                         f"found {var.dtype}")
            for n in _bit_indices(set(var.ncattrs()), "flag"):
                if n < 0:
                    self.add("STA-007", "error", "6.5.1", name,
                             f"flag_{n}_description uses a negative number; flag numbers must "
                             "be >= 0 when flag_<#>_description attributes are used")

    # -- 6.9 source variables ---------------------------------------------
    def check_source(self):
        nc = self.nc
        for name in sorted(self.source_vars):
            var = nc.variables[name]
            attrs = set(var.ncattrs())
            ln = str(_attr(var, "long_name", "") or "")
            if not ln.startswith("Source for variable:"):
                self.add("SRC-010", "error", "6.9.4/6.9.5", name,
                         f"long_name = '{ln}'; the required form is 'Source for variable: "
                         "<data variable long_name or generic description>'")
            if str(_attr(var, "units", "")).strip() != "1":
                self.add("SRC-011", "error", "6.9.4", name,
                         f"units = {_attr(var, 'units')!r}; a source variable requires units = '1'")
            if not str(_attr(var, "description", "") or "").strip():
                self.add("SRC-012", "error", "6.9.4", name,
                         "the description attribute stating how the values are interpreted "
                         "is required")
            fm = str(_attr(var, "flag_method", "") or "")
            if fm not in ("integer", "bit"):
                self.add("SRC-013", "error", "6.9.4/6.9.5", name,
                         f"flag_method = '{fm}'; a source variable declares 'integer' or 'bit'")
            if _numeric_kind(var.dtype) not in "iu":
                self.add("SRC-014", "error", "6.9.4", name,
                         f"a source variable is type integer; found {var.dtype}")
            kind = "bit" if fm == "bit" else "flag"
            idx = _bit_indices(attrs, kind)
            if not idx:
                self.add("SRC-015", "error", "6.9.4/6.9.5", name,
                         f"no {kind}_<#>_description attributes; every possible source value "
                         "must be described")
            if any(n < 0 for n in idx):
                self.add("SRC-016", "error", "6.9.4", name,
                         "source flag numbers must be >= 0")
            if kind == "flag" and idx:
                descs = " ".join(str(_attr(var, f"flag_{n}_description", "")) for n in idx)
                if "no_source_available" not in descs:
                    self.add("SRC-017", "warning", "6.9.4", name,
                             "one integer source value must describe the no-source/default case "
                             "with flag_<#>_description = 'no_source_available'")
            users = [n for n, v in nc.variables.items()
                     if name in str(_attr(v, "ancillary_variables", "") or "").split()]
            if not users:
                self.add("SRC-018", "error", "6.9.3", name,
                         "no data variable links to this source variable through its "
                         "ancillary_variables attribute")

    # -- 5.1.3 data-level requirements ------------------------------------
    def check_level_requirements(self):
        lvl = None
        if self.fn:
            lvl = self.fn["level"]
        elif isinstance(_attr(self.nc, "data_level"), str):
            lvl = _attr(self.nc, "data_level")
        if not lvl:
            return
        real_qc = [q for q in self.qc_vars if q != "qc_time"]
        if lvl.startswith("b"):
            if not real_qc:
                self.add("LVL-001", "error", "5.1.3", f"data level {lvl}",
                         "a b-level datastream requires QC checks applied to at least one "
                         "measurement and stored in an accompanying QC variable (qc_time alone "
                         "does not make a datastream b-level)")
        if lvl.startswith("a") and real_qc:
            self.add("LVL-002", "info", "5.1.3", f"data level {lvl}",
                     f"an a-level file carries QC variable(s) {sorted(real_qc)[:3]}; if they "
                     "meet the b-level QC standards the datastream should be b-level")


def _norm(s):
    """Loose text match: case, whitespace and hyphenation are not deviations.

    ARM's own ingests write "bit-packed" where the standard prints "bit
    packed"; that is not worth a finding.
    """
    return re.sub(r"\s+", " ", str(s).replace("-", " ")).strip().lower()


# --------------------------------------------------------------------------
# public API
# --------------------------------------------------------------------------


def check_file(path, profile="adc", read_data=True):
    """Check one netCDF file.  Returns a :class:`Report`."""
    return ArmStandardsChecker(path, profile=profile, read_data=read_data).run()


def check_files(paths, profile="adc", read_data=True):
    return [check_file(p, profile=profile, read_data=read_data) for p in paths]


def find_files(root, recursive=True, sample_per_datastream=False):
    """Collect netCDF files under *root*, optionally one file per datastream."""
    if os.path.isfile(root):
        return [root]
    pat = "/**/*" if recursive else "/*"
    files = sorted(
        f for ext in (".nc", ".cdf")
        for f in glob.glob(root + pat + ext, recursive=recursive)
    )
    if not sample_per_datastream:
        return files
    seen = {}
    for f in files:
        parts = os.path.basename(f).split(".")
        key = ".".join(parts[:2]) if len(parts) >= 4 else os.path.basename(f)
        seen.setdefault(key, f)
    return sorted(seen.values())


def summarise(reports):
    """Aggregate rule hits across many reports -- the fleet view."""
    rows = Counter()
    bucket_files = defaultdict(set)
    rule_files = defaultdict(set)
    for r in reports:
        for f in r.findings:
            key = (f.rule, f.severity, f.section, f.message.split(";")[0][:70])
            rows[key] += 1
            # Count files for THIS message variant, not for the whole rule --
            # otherwise one variant's example text gets paired with the rule's
            # total and mislabels the other variants' files.
            bucket_files[key].add(os.path.basename(r.path))
            rule_files[f.rule].add(os.path.basename(r.path))
    out = []
    for key, n in rows.most_common():
        rule, sev, sec, msg = key
        out.append({
            "rule": rule, "severity": sev, "section": sec,
            "n_findings": n, "n_files": len(bucket_files[key]),
            "n_files_rule": len(rule_files[rule]),
            "example": msg,
        })
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Check netCDF files against the ARM Data File Standards "
                    f"({STANDARD_DOC}).")
    ap.add_argument("paths", nargs="+", help="netCDF files or directories")
    ap.add_argument("--profile", choices=("adc", "doc"), default="adc",
                    help="'adc' (default): required = the global attributes ARM's released "
                         "files carry. 'doc': every global attribute in section 6.7.1 is required.")
    ap.add_argument("--recursive", action="store_true", help="descend into directories")
    ap.add_argument("--sample-per-datastream", action="store_true",
                    help="check only the first file of each datastream")
    ap.add_argument("--severity", choices=SEVERITIES, default="info",
                    help="lowest severity to print (default info)")
    ap.add_argument("--json", metavar="PATH", help="write the full findings as JSON")
    ap.add_argument("--csv", metavar="PATH", help="write one row per finding as CSV")
    ap.add_argument("--quiet", action="store_true", help="print only the verdict lines")
    ap.add_argument("--no-data", action="store_true",
                    help="skip value-level checks (metadata only, much faster)")
    args = ap.parse_args(argv)

    paths = []
    for p in args.paths:
        paths.extend(find_files(p, args.recursive, args.sample_per_datastream))
    if not paths:
        print("no netCDF files found", file=sys.stderr)
        return 2

    show = SEVERITIES[: SEVERITIES.index(args.severity) + 1]
    reports = []
    for p in paths:
        rep = check_file(p, profile=args.profile, read_data=not args.no_data)
        reports.append(rep)
        c = rep.counts()
        if args.quiet or len(paths) > 1:
            print(f"{'FAIL' if not rep.compliant else 'pass'}  "
                  f"{c['error']:3d}E {c['warning']:3d}W {c['info']:3d}I  {os.path.basename(p)}")
        if not args.quiet and len(paths) == 1:
            print(rep.text(show=show))

    if len(paths) > 1 and not args.quiet:
        print("\n== rule summary " + "=" * 60)
        for row in summarise(reports):
            if row["severity"] not in show:
                continue
            print(f"{row['severity']:7s} {row['rule']:9s} "
                  f"{row['n_files']:4d} file(s) [{row['n_files_rule']:4d} for the rule]  "
                  f"§{row['section']:12s} {row['example']}")
        n_bad = sum(1 for r in reports if not r.compliant)
        print(f"\n{len(reports) - n_bad}/{len(reports)} files compliant "
              f"(profile {args.profile})")

    if args.json:
        with open(args.json, "w") as fh:
            json.dump({"standard": STANDARD_DOC, "profile": args.profile,
                       "reports": [r.to_dict() for r in reports],
                       "summary": summarise(reports)}, fh, indent=1)
    if args.csv:
        import csv
        with open(args.csv, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["file", "rule", "severity", "section", "target", "message"])
            for r in reports:
                for f in r.findings:
                    w.writerow([os.path.basename(r.path), f.rule, f.severity,
                                f.section, f.target, f.message])
    return 0 if all(r.compliant for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
