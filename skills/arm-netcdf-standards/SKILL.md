---
name: arm-netcdf-standards
description: Make netCDF files comply with the ARM Data File Standards (DOE/SC-ARM-15-004 v1.3) and check that they do. Covers filename and datastream construction, the base_time/time_offset/time triple, coordinate and bounds variables, lat/lon/alt, variable naming, required variable attributes, UDUNITS and CF standard_name rules, bit-packed and integer quality-control variables, state and source variables, and the required global attributes -- with the deviations ARM's own released files actually contain. Ships arm_standards_check.py, a rule-by-rule compliance checker calibrated against 143 released datastreams. Use when writing, reviewing, or publishing an ARM netCDF product, preparing an ingest or VAP for the ADC, answering "is this file ARM-compliant", or fixing DQ/PCM metadata complaints. Triggers ARM standards, ARM metadata, DOE/SC-ARM-15-004, ADC, datastream naming, data level, b1, c1, qc_ variable, bit-packed QC, flag_method, bit_1_assessment, dod_version, base_time, time_offset, sensor_height.
---

# ARM netCDF data file standards

The governing document is **DOE/SC-ARM-15-004, "ARM Data File Standards
Version 1.3"** (ARM Standards Committee, September 2020). Everything below cites
its section numbers, so a finding can be argued from the source rather than from
recollection. Two tiers matter (§2): **required** standards must be met or the
data will not be published in the ADC without a granted exception, and
**recommended** standards, whose absence costs you automated DQ monitoring and
discoverability rather than publication. A third class, **optional methods**
(§3.0) -- quality control variables, state variables, source variables,
`cell_methods` -- are yours to adopt or not, but *once adopted the required
standards inside them apply*.

## Run the checker first

```bash
python arm_standards_check.py sgpmetE13.b1.20240101.000000.nc
python arm_standards_check.py /data/mydir --recursive --sample-per-datastream \
       --json findings.json --csv findings.csv
python arm_standards_check.py file.nc --profile doc      # strictest reading
python arm_standards_check.py file.nc --no-data          # metadata only, fast
```

```python
from arm_standards_check import check_file, check_files, find_files, summarise
rep = check_file("sgpmetE13.b1.20240101.000000.nc")
rep.compliant          # False iff a required standard was violated
rep.counts()           # {'error': 0, 'warning': 43, 'info': 21}
print(rep.text())      # grouped, with section citations
rep.to_dict()          # JSON-ready, one entry per finding
```

Exit status is 0 when every file checked is free of errors, 1 otherwise, so it
drops into CI or a pre-archive hook. Findings carry a rule id (`QC-019`), a
severity, the document section, the variable or attribute at fault, and what to
do. `severity == "error"` means a **required** standard; `warning` means
recommended, or required-with-conditions where the condition can't be verified
from the file alone; `info` means optional or worth a glance.

Two profiles exist because the document and ARM's practice disagree about the
global attributes -- see *The global attribute question* below. Default is
`adc`; `--profile doc` is the literal reading.

## What the standard actually requires

### Filename and datastream (§5.1)

    (sss)(inst)(qualifier)(temporal)(Fn).(dl).(yyyymmdd).(hhmmss).nc
    bnfceilM1.b1.20250508.000001.nc

Everything is lower case except the facility letter. Only `a-z A-Z 0-9 .` are
legal -- **no underscores or dashes anywhere**, which is the single most common
way a locally written product fails before anyone opens it. Three length limits,
all from the ADC database (§5.1.1): the whole filename **≤ 60** characters (four
more are reserved for the archive's `.v1` suffix), the datastream
`(sss)(inst)(qualifier)(temporal)(Fn).(dl)` **≤ 33**, and
`(inst)(qualifier)(temporal)` **≤ 24**.

- `(sss)` three-letter site; geographic for fixed sites, IATA airport code for
  AMF deployments, a campaign acronym for remote or moving platforms.
- `(Fn)` capital letter + one or two digits. `S01` and `S1` are **different
  facilities**; zero-padding is not recommended. Letters are defined in §5.1.2:
  C central, E extended, M mobile (M1 ≡ C1 for an AMF), S supplemental
  (port/starboard/bow/stern → S1/S2/S3/S4, location stated in the facility long
  name), I intermediate, F manned aircraft, U unmanned aircraft (U1 Data Hawk,
  U2 ArcticShark, U40+ recyclable), N network product, X external, D diagnostic
  (expert-only, not for distribution), and the retired A, B, L, Q.
- `(dl)` data level, one lower-case letter + one digit (§5.1.3). `00` raw;
  `a0` raw→netCDF, not for distribution; `a1` calibrated, geophysical units;
  `b0` intermediate QC; **`b1` requires QC checks on at least one measurement
  stored in an accompanying QC variable meeting the standards in §6.8 -- adding
  `qc_time` alone does not earn b level**; `c0` intermediate VAP; `c1` derived
  VAP; `s1` summary of a b/c parent with bad values set to missing; `m0`-`m9`
  model (LASSO). A level is not reached until every requirement of that level
  *and all levels below it* is met.
- `(temporal)` needs a unit: `ns us ms s m h d mo yr`, reduced to the lowest
  unit (60 s → `1m`, 60 min → `1h`). The primary end-user datastream is
  recommended not to carry an integration period at all.
- Date and time are UTC, of the **first data point**, zero-padded, sub-second
  truncated, and `hhmmss` may not exceed `235959`.
- `.nc`, not `.cdf`. `.cdf` survives for historical data and should be changed
  on reprocessing.
- Files span 24 hours over a UTC day (§5.1.5), and are expected to **split when
  metadata changes** mid-day (serial number, calibration).
- "be" in a name asserts a best estimate and needs an ECR (§5.1.4).

### Time (§6.1)

`time` is **unlimited** and the **first** dimension of every variable that uses
it -- netCDF3 requires it and concatenation depends on it. Time must be
increasing, must not repeat, and outside RAW must contain no missing value or
NaN. **All three of `base_time`, `time_offset` and `time` are required**: ARM's
historical pair plus the CF coordinate.

```
int base_time ;                       // scalar, long integer
    base_time:string = "18-Sep-2012,00:00:00 GMT" ;
    base_time:long_name = "Base time in Epoch" ;
    base_time:units = "seconds since 1970-1-1 0:00:00 0:00" ;
    base_time:ancillary_variables = "time_offset" ;
double time_offset(time) ;            // double precision
    time_offset:long_name = "Time offset from base_time" ;
    time_offset:units = "seconds since 2012-09-18 00:00:00 0:00" ;
    time_offset:ancillary_variables = "base_time" ;
double time(time) ;                   // coordinate variable
    time:long_name = "Time offset from midnight" ;
    time:units = "seconds since 2012-09-18 00:00:00 0:00" ;
    time:standard_name = "time" ;
```

`base_time + time_offset[0]` **is** the filename timestamp. The two variables
are cross-linked with `ancillary_variables`. `time` is recommended to start at
UTC midnight (dividing by 3600 then gives hours). `seconds since` is the
recommended form; `months since` / `years since` are not recommended.
Gregorian calendar; the `calendar` attribute is optional when it is Gregorian.

**Time bounds (§6.1.4).** For all non-instantaneous data the time ranges are
*required*: a `bounds` attribute naming a `(time, bound)` variable, with a new
dimension of length 2 (`bound` recommended). The bounds variable may not have
missing values, needs no `units` (not recommended) and `long_name` is only
recommended. A time bounds variable plus an `ARM-<#>` `Conventions` attribute
means *every* time-dimensioned variable is assumed averaged over the bounds
period unless its `cell_methods` says otherwise. `bound_offsets = -30., 30.`
optionally declares a constant width -- omit it when widths vary.

### Coordinates, bounds, location (§6.2, §6.3)

A coordinate dimension should have a same-named variable with `long_name` and
`units`; singular names, spelled out (`height`, `range`, `bin`, `depth`).
Dimensions used only for string length or indexing need no such variable. A
coordinate variable **may not have `missing_value`, `_FillValue` or NaN**, and
must be monotonic. Vertical coordinates **must declare their frame of reference
through `standard_name`**, not `long_name`: `height` for AGL, `altitude` for MSL
(§6.2.1-6.2.2). Binned coordinates take `bounds` exactly like time, with
`bin_bounds[i,0]` inclusive and `bin_bounds[i,1]` exclusive.

Location is three variables with **required** names `lat`, `lon`, `alt`, units
`degree_N`, `degree_E`, `m` (MSL), and `standard_name` `latitude`, `longitude`,
`altitude`. They may be vectors on mobile platforms. `alt` is ground level
relative to MSL; instrument height above ground is the separate `sensor_height`
attribute, and sensor height above MSL is `alt + sensor_height`. The `valid_min`
/`valid_max` on `lat`/`lon` in the standard's example are limits of *usable*
values, not QC limits.

### Variable names (§6.4)

First character a letter; only letters, digits, underscores; **≤ 64 characters**;
upper case sparingly; singular; no Greek letters or spelled-out formula symbols.
Prefer spelling out (`atmospheric_temperature` beats `temperature`, which could
be air, instrument or derived) and only abbreviate past ~25 characters, using
the §6.4.2 list (`temp snr lat lon alt navg aod precip rh wspd wdir`;
`std mean med var sum min max stderr log ln`; `up down long short pol hemisp
ref ir vis uv coef scat aux rot copol xpol depol diff anc`; prefixes
`inst fgp be qc aqc inter`). Qualifiers are joined by underscores in the §6.4.1
hierarchy: super-prefix, prefix, measurement, subcategory, medium,
height/depth, enumeration, source, algorithm, quantity -- giving
`qc_atmospheric_temperature_10m`, `qc_vapor_pressure_aeri_std`. Related
variables should repeat one pattern (`aot`, `aot_1020nm`,
`aot_1020nm_francis_mean_10min`) so users can see they are correlated.

### Variable attributes (§6.6)

**Required on every variable**: `long_name`, unique within the file, clear
enough to label a conference plot, first letter capitalised (recommended), and
**not changeable without a DOD version change**; and `units`, UDUNITS-compliant,
scientifically correct, with **`"1"` for unitless -- never `"unitless"`,
`"none"` or `""`**. Units multiply the data: CEIL backscatter in
`1/(sr*km*10000)` means a stored 100.0 is 0.01/(sr·km). Appendix C lists ARM's
preferred descriptors (`m`, `kPa`, `degC`, `m/s`, `W/m^2`, `g/m^3`, `g/kg`,
`degree`, `degree_N`, `%`, `mm`, `nm`, `count`, `dB`, `m^3/m^3`, `1`).

**Required with conditions**: `missing_value` **or** `_FillValue` if a single
value marks no-data (recommended -9999, outside the valid range, same type as
the variable, the same value for both if both appear, and **not on coordinate
variables**); and `standard_name` if the variable is primary and a CF name
exists. CF names must come from the CF standard-name table -- **inventing one is
not allowed** (§6.6.4). The checker validates against a bundled copy of the
table (`cf_standard_names.txt`) and suggests near matches.

`sensor_height` is `"<value> <udunit> AGL"`, exactly three space-separated
tokens, negative below ground; variable-level overrides global. Numeric
attributes used directly with the data (`_FillValue`, `missing_value`,
`valid_min`, `valid_max`, `valid_range`) **must match the variable's type**,
including after packing -- a `short` packed variable takes a `short`
`missing_value` while `scale_factor`/`add_offset` are the unpacked (float) type.
Other ARM attribute names: `resolution`, `comment`, `comment_<#>`, `precision`,
`accuracy`, `bit_<#>_description`, `flag_<#>_description`,
`bit_<#>_assessment`, `flag_<#>_assessment`, `corrections_applied`,
`sensor_height`, `wavelength`, `actual_wavelength`, `filter_wavelength`,
`source`. Attribute names are lower case with underscores; one long `comment`
beats several numbered ones.

### Quality control variables (§6.8)

Optional as a whole, tightly specified once used. Name is `qc_` + the data
variable name. Type integer (32-bit recommended). Linked **from the data
variable** by `ancillary_variables` -- the direction people get wrong.

```
float upwelling_broadband(time) ;
    upwelling_broadband:ancillary_variables = "qc_upwelling_broadband" ;
int qc_upwelling_broadband(time) ;
    qc_upwelling_broadband:long_name = "Quality check results on variable: Upwelling broadband radiation" ;
    qc_upwelling_broadband:units = "1" ;
    qc_upwelling_broadband:flag_method = "bit" ;
    qc_upwelling_broadband:description = "This variable contains bit packed integer values, ..." ;
    qc_upwelling_broadband:standard_name = "quality_flag" ;      // recommended
    qc_upwelling_broadband:fail_min = 0.f ;
    qc_upwelling_broadband:bit_1_description = "Value is equal to missing_value" ;
    qc_upwelling_broadband:bit_1_assessment = "Bad" ;
    qc_upwelling_broadband:bit_2_description = "Value is less than fail_min" ;
    qc_upwelling_broadband:bit_2_assessment = "Bad" ;
```

Required QC attributes: `long_name = "Quality check results on variable:
<data variable's long_name>"` (or exactly `"Quality check results"` when one QC
variable serves several data variables, §6.8.9, in which case its base name must
not match any data variable), `units = "1"`, `description` (the standard's fixed
sentence for the bit or integer method, or the pointer
`"See global attributes for individual QC bit descriptions."`), and
`flag_method`, either `"bit"` or `"integer"`. Never mix the two in one variable.

Bit numbering starts at **1** = 2^0 = integer 1. Each declared test needs both
`bit_<#>_description` and `bit_<#>_assessment`, and **the assessment may only be
`"Bad"` or `"Indeterminate"`**. An undeclared bit is free; a bit you must
reserve is declared `"Not used"` / `"Bad"` (§6.8.5). Standard ARM QC is the
missing / minimum / maximum trio on bits 1-3. Test definitions live at variable
level **or** global level (`qc_bit_1_description`, ...), never both for the same
variable, and variable level wins. Flag/bit numbers must be ≥ 0 -- a negative
number becomes an illegal identifier in languages that map attributes to
variables. Test *limits* belong on the QC variable as **`fail_min`/`fail_max`
(assessment "Bad") and `warn_min`/`warn_max` ("Indeterminate")**, not as
`valid_min`/`valid_max`. A limit that may change between DOD versions goes in a
separate attribute (`test_parameter_value`) referenced by the bit description,
because **a bit description may not change without a DOD change**.

`valid_min`/`valid_max`/`valid_range` mean something else entirely (§6.8.8):
CF treats them as absolute limits of usable data and third-party tools will
silently drop anything outside them, potentially before unpacking. Using them as
QC limits is the historical ARM practice the standard now argues against. Where
state values *are* mixed into a data variable (the `-8888`/`-7777` pattern),
they must sit **below `valid_min`** so software removes them automatically.

### State and source variables (§6.5, §6.9)

State variables are byte/short/int and CF-formatted. Mutually exclusive states
use `flag_values` (numeric array) + `flag_meanings` (space-separated,
underscore-joined words, one per value), optionally
`flag_<#>_description`/`_assessment`. Simultaneous states use `flag_masks`,
whose values are **always powers of two**, with optional
`bit_<#>_description`; list every state so automated software always matches,
and if 0 means "none of them", say so in a `comment`.

A `source` **attribute** is `"<datastream>:<variable>"`, or
`"<class>.<level>:<variable>"` when site and facility match the globals, or a
bare variable name for a variable in the same file, or an algorithm name --
which must contain no colon. `"no_source_available"` when there is none. A
time-varying source uses a `source_<var>` **variable** (integer, `units = "1"`,
`long_name = "Source for variable: ..."`, a `description`, a `flag_method`, and
a `flag_<#>_description` for every value including a `no_source_available`
default), linked from the data variable by `ancillary_variables`. Lower numbers
mean higher preference.

### ADI transforms (§6.10)

`cell_transforms = "time: TRANS_SUBSAMPLE (range: 300) distance:
TRANS_SUBSAMPLE (range: 5) qc_bad: 1,2,3"`. Transform type is required per
dimension, from `TRANS_BIN_AVERAGE`, `TRANS_INTERPOLATE`, `TRANS_SUBSAMPLE`,
`TRANS_PASSTHROUGH`; dimension order is order of operation; a parameter listed
at the end applies to all dimensions. `cell_methods` follows CF
(`"time: mean height: median"`, left-most first; `"time: sum (interval: 1 min)"`).

### Global attributes (§6.7)

Every global attribute must **have a value** -- `"unknown"`, `-9999`, `127` for
byte, or `"N/A"` if a required attribute can have no value. Recommended order:

`command_line`, `command_line_comment`, `Conventions`, `process_version`,
`dod_version`, `input_datastreams`, `input_source`, `site_id`, `platform_id`,
`facility_id`, `data_level`, `location_description`, `datastream`,
`serial_number`, `sampling_interval`, `averaging_interval`, `sensor_height`,
`title`, `institution`, `description`, `references`, `doi`, `doi_url`,
`history` (strongly recommended last).

Load-bearing details: `Conventions` carries `"ARM"` + this document's version
joined by a hyphen, listed first -- `"ARM-1.3 CF-1.7"`. `datastream` **must
equal** `site_id + platform_id + facility_id + "." + data_level`, and all of
them must agree with the filename. `doi` is required in baseline and evaluation
datastreams (radar may use instrument class ± level; LASSO one per Alpha
release) and is a character string. `institution`, if given, must be *exactly*
`"United States Department of Energy - Atmospheric Radiation Measurement (ARM)
program"`. `input_datastreams` itemises `datastream : version : date-range`
separated by `" : "`, entries by `" ;\n "`, ranges as
`yyyymmdd.hhmmss-yyyymmdd.hhmmss`. `sampling_interval` and
`averaging_interval` are a number and a UDUNITS descriptor separated by one
space (`"400 us"`, `"5 minute"`). `history` records user, machine and date, is
appended to rather than replaced, and keeps its original content.

## The global attribute question

Section 6.7.1 says required global attributes are printed **bold-underline**.
Measuring the drawn underline rule under each heading in the PDF shows that
**all 24 are bold-underline**, which read literally makes every one of them
required. ARM's own released files do not behave that way. Observed on
**2026-09-02**, over one file from each of 138 released, readable, ARM-named
datastreams (a1/b1/c0/c1, six sites, data dates 2025-2026). These counts are
not reproducible from this repo -- the ARM files are not in it -- so treat them
as a dated observation, and re-measure with
`arm_check_tree(root, sample_per_datastream=True)` if much time has passed:

| attribute | present | attribute | present |
|---|---|---|---|
| `history`, `site_id`, `dod_version`, `datastream`, `facility_id`, `command_line`, `process_version` | 100% | `input_source` | 70% |
| `data_level` | 99% | `sampling_interval` | 54% |
| `Conventions`, `location_description`, `doi`, `platform_id` | 97% | `serial_number` | 51% |
| | | `input_datastreams` | 30% |
| | | `averaging_interval` | 30% |
| | | `title`, `institution` | 4% |
| | | `references`, `doi_url` | 3% |
| | | `description`, `command_line_comment` | 0% |

The break is clean: twelve attributes at 97-100%, then nothing until 70%. So the
checker's default `adc` profile treats those twelve as errors and the rest as
warnings; `--profile doc` promotes the rare ones to errors. If you are preparing
a product for the ADC, clearing `adc` is the bar that matters; clearing `doc` is
what the document literally says. Say which one you ran.

## What released ARM files actually get wrong

Useful both as calibration and as a warning against assuming a released file is
a template. Observed **2026-09-02** over the 140 ARM-named files sampled,
default profile: **95 free of errors; by level b1 73/95, c1 15/24, a1 7/19,
c0 0/2**. Another dated observation, not a checkable fact. The recurring
deviations, with counts as (findings / files affected):

- **`valid_min`/`valid_max`/`valid_range` on data variables** -- the most
  widespread pattern by far (3149 / 105 files), exactly what §6.8.8 argues
  against.
- **`flag_method` missing** from QC variables (316 / 10 files -- every
  `mfrsr7nch` QC variable, which carries only `description`, `long_name`,
  `units`) though §6.8.2 lists it as required.
- **`units = "unitless"`** on data variables (246 / 20) and QC variables
  (179 / 11). Version 1.3 changed this to `"1"` (§3.1); older ingests were
  never updated.
- **`"Quality check results on field:"`** instead of `"on variable:"`
  (592 / 32 files) -- v1.2 wording that §3.1 retired.
- **Radar datastreams carry CfRadial `standard_name` values** absent from the CF
  table (161 / 6 files: `radar_doppler_spectrum_width`,
  `projection_range_coordinate`, `equivalent_reflectivity_factor_h`, ...).
  §6.6.4 forbids invented names, so these are real deviations -- but expect them
  in any CfRadial-derived product.
- **`.cdf` extension** on 50 of 140 files; allowed for historical data only.
- **netCDF-4 extended model** on 11 files where §4.0 prefers the netCDF-3 model
  or netCDF-4 classic.
- **`sensor_height` without the `AGL` token** (`"3.175 m"`, `"0 m"`) on 4 files
  (`bnfecorsf*`, `sgpceilpol`).
- **`facility_id = "M1: Bankhead National Forest, Alabama"`** on 4 files
  (`bnfmwrlosS40`, `bnfvdisM1`, `sgpaerich1C1`, `sgpvdisC1`) -- the location
  belongs in `location_description`.
- **QC data setting a bit nobody declared** -- `sgpsondewnpnC1.b1` sets bit 4 in
  `qc_asc` while describing only bits 1-3.
- **`_FillValue` on a coordinate variable** on 3 files, which §6.2 forbids.

## Failure modes of locally written products

What a hand-rolled or xarray-written file typically trips, in rough order of
frequency:

1. **Filename**: underscores, no facility/level, no timestamp
   (`arscl_repro_bnf_20250503.nc`). Nothing downstream works without this.
2. **Time**: `time` written as a plain dimension rather than unlimited, and no
   `base_time`/`time_offset` at all. xarray will not write an unlimited
   dimension unless told: `ds.to_netcdf(..., unlimited_dims=["time"])`.
3. **`_FillValue` on coordinate variables**, which xarray adds by default.
   Suppress it: `encoding={v: {"_FillValue": None} for v in ds.coords}`.
4. **Missing `long_name`/`units`** on every variable, and no `lat`/`lon`/`alt`.
5. **`flag_values` written as a character string** (`"[0 1 2 3]"`) because a
   numpy array was formatted rather than assigned. It must be a numeric array
   whose type matches the variable.
6. **State values mixed into float data** (`-2` = possible clear sky) without a
   `valid_min` below them, so no tool can exclude them.
7. **netCDF4 extended model** by default. ARM's preferred final format is the
   netCDF-3 model; netCDF-4 *classic* is allowed to gain compression and is
   expected to cut volume by at least half (§4.0).
8. **No global attributes**, hence no `datastream`, and no way for the ADC to
   place the file.

`arm_skeleton()` in `kernel.py` writes 1-4 and 8 correctly for you; `arm_check`
catches the rest.

One library quirk worth knowing: **netCDF4-python silently coerces
`missing_value` and `_FillValue` to the variable's type** on attribute
assignment, so you cannot create that particular type mismatch from Python at
all. If the checker reports `ATT-007`, the file was written by something else
(IDL, C, an older ingest). Attributes with any other name -- `valid_min`,
`fail_min` -- are *not* coerced and are the real risk: write them as
`np.float32(x)` when the variable is `f4`.

## Exceptions (§6.11-6.12)

If a required standard cannot be met, the developer requests an exception from
the Standards Committee (`standardscomm@arm.gov`) **early**, in writing, before
extensive development. A majority grants it; an approved product is published,
fully discoverable, and tagged with a Data Quality Report summarising the
deviation. Denial stops development under the proposed terms. Exceptions are
identified in the first place by the PCM tool at i.arm.gov validating the DOD,
and secondarily by DQO/ADC/mentor inspection. Do not treat this checker's output
as an exception request -- it is the evidence you would attach to one.

## Verified against

The standards document itself, on **2026-09-02**: every rule cites the section
it comes from, and the required/recommended split is the document's own
(§2.1/§2.2). The global-attribute profiles come from measuring the drawn
underline rule under each of the 24 headings in §6.7.1, not from reading the
page.

**20 checks in `test_arm_standards.py` pass**, offline. They include the drift
guards CONTRIBUTING asks for -- every rule id cited above must be one the engine
can emit, the twelve attributes named in the presence table must be the twelve
the default profile requires, and the corpus numbers must carry the date they
were measured -- plus a round trip asserting that a file written by
`arm_skeleton()` passes the checker with zero errors, and seeded-deviation
checks for 22 individual rules. The netCDF4-dependent checks skip when netCDF4
is absent, so the suite stays runnable in the pytest-only environment.

Calibrated on **2026-09-02** against one file from each of 143 datastreams in
six local trees (BNF, SGP; a1/b1/c0/c1). Five rules were relaxed or re-pointed
because released ARM files proved them wrong -- the `time_bounds` units
exemption alone accounted for 55 false positives. If you re-point a rule, add
the released-file case that justifies it to the test suite, as
`test_bounds_variable_needs_no_units` and
`test_facility_id_with_a_description_is_a_warning_not_an_error` do.

Not verified: the ADC's own PCM validator. This checker encodes the published
document, which is not the same artefact as the tool ARM runs at ingest, so a
clean report here is evidence for an exception request or a pre-submission
review, not a guarantee of acceptance.
