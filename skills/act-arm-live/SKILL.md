---
name: act-arm-live
description: Download and open DOE ARM observational data with the Atmospheric data Community Toolkit (ACT, act-atmos) - the ARM Live Data Webservice, datastream naming, the server-side concatenate/subset `mod` endpoint, DOI citation lookup, and `read_arm_netcdf`. Use this whenever the task involves pulling ARM data programmatically, resolving a datastream name like sgpmetE13.b1 or bnfceilM1.b1, checking which ARM files exist for a date range, citing ARM data, or reading ARM netCDF into xarray. Also covers ACT's other discovery services (ASOS, NOAA PSL, NEON, AmeriFlux, AirNow, SURFRAD, CropScape, MPLNET) and which of their hosts need a network-allowlist grant. Triggers - ACT, act-atmos, ARM Live, armlive, adc.arm.gov, ARM Data Center, ARM archive, datastream, download_arm_data, read_arm_netcdf, ARM DOI, ARM citation, SGP, ENA, NSA, AMF, BNF, ARM netCDF, .b1, .c1, ARM facility.
---

# ARM Live data access with ACT

ACT (`act-atmos`, imported as `act`) is ARM's own Python toolkit: discovery, IO, QC,
retrievals and plotting for atmospheric time-series. This skill covers getting data in.
Companion skills: `act-qc` (embedded quality flags), `act-plotting` (the Display family),
`act-retrievals` (soundings, PBL, radiation, unit and solar utilities). For a
task-level workflow that probes an entire site's instrument loadout over a week, see
`arm-site-week-survey`.

## Environment

`act-atmos` is not in the default env. Create one once:

```
manage_environments(mode="create", name="act", python_version="3.12",
                    packages=["xarray","netcdf4","matplotlib","pandas","scipy",
                              "requests","cartopy","metpy","dask","pint","cftime"])
manage_packages(mode="install", environment="act", packages=["act-atmos"], use_pip=True)
```

Then pass `environment="act"` on every python cell. ACT uses `lazy_loader`, so
`import act` is cheap and `act.discovery.download_arm_data` resolves on first use —
you do not need to import submodules explicitly.

## Credentials

ARM Live needs a username and an access token, registered at
<https://adc.arm.gov/armlive/>. In this workspace they arrive as the `ARMUSER` and
`ARMTOKEN` environment variables (`host.credentials.get("ARMUSER")` also works).
`armlive_credentials()` reads them and raises a pointed error if they are absent —
never hard-code or print them.

If a session has no ARM credentials configured, say so and point the user at
Customize -> Credentials -> Add Credential; there is no anonymous path to the archive.

## Datastream names

`<site><instrument class><facility>.<data level>` — `sgpmetE13.b1` is the surface
met station at SGP facility E13, processed to level b1.

| Level | Meaning |
|---|---|
| `a0` | raw converted to netCDF; **not generally discoverable through ARM Live** — the API prints a notice telling you to file a Help request |
| `a1` | calibrations applied |
| `b1` | calibrated + automated QC applied — the usual starting point |
| `c1`, `c2` | derived value-added products (VAPs) |
| `s1`, `m1` | statistical / summary products |

`arm_datastream_parts("sgpmetE13.b1.20240602.000000.cdf")` splits a name or filename
into its parts; `arm_facility_latlon("sgp", "E13")` returns
`{'sgp E13': {'latitude': 36.604937, 'longitude': -97.485561}}`. Facility position
matters more than it looks: supplementary S-facilities can sit tens of km from the
main M1/C1 site, so read `lat`/`lon` before interpreting spatial contrasts.

ARM Live itself has no catalog method, so the working way to find out whether a given
datastream exists is to ask it for that datastream's file list and see whether anything
comes back. But the instrument catalog behind it *is* queryable: arm.gov's instrument
pages are a JavaScript shell over a public Elasticsearch proxy at
`POST https://www.arm.gov/api/es/ds/_search`, which enumerates every ARM instrument
class with its handbook link and its full datastream list, per site and facility, with
date coverage. Load `arm-instruments` for that endpoint, its two parsing traps, and the
per-instrument handbook skills built on it - it is the right way to answer "which
instrument measures this" or "which datastreams exist for that instrument" without
guessing datastream names.

## Workflow

**1. Probe before downloading.** `armlive_list_files` returns the filenames the
archive holds without transferring anything, and returns `[]` both for "no data in
this window" and "no such datastream" — so a sweep over constructed candidate names
is cheap and error-free.

```python
armlive_list_files("sgpmetE13.b1", "2024-06-01", "2024-06-03")
# ['sgpmetE13.b1.20240601.000000.cdf', ..., 'sgpmetE13.b1.20240603.160000.cdf']
```

Note the last entry: a day can hold more than one file when the instrument restarts.
Do not assume one file per day when sizing a download.

**2. Download, or download-and-open.**

```python
paths = armlive_download("sgpmetE13.b1", "2024-06-01", "2024-06-03")   # -> ./data/<datastream>/
ds    = armlive_open("sgpmetE13.b1", "2024-06-01", "2024-06-03",
                     keep_variables=["temp_mean", "qc_temp_mean"])      # -> xarray.Dataset
```

`armlive_open` wraps download + `read_arm_netcdf` and defaults to `cleanup_qc=True`,
which is what makes the QC variables usable (see `act-qc`).

Underneath, `act.discovery.download_arm_data(username, token, datastream, startdate,
enddate, time=None, output=None)` returns the list of downloaded paths and prints the
citation. Dates accept `YYYY-MM-DD`, `YYYYMMDD`, `DD.MM.YYYY`, `DD/MM/YYYY`,
`YYYY/MM/DD`, optionally with `THH:MM:SS`. A start equal to the end is expanded to
cover that whole day.

**3. Cite the data.** Every download prints an APA citation with a DOI, and ARM's
data-use policy expects it in any publication. Capture it rather than letting it
scroll past: `act.discovery.get_arm_doi(datastream, "2024-06-01", "2024-06-03")`
returns the same string. Put it in the report or methods section you produce.

## Server-side subsetting: the `mod` endpoint

For long records where you want two variables out of fifty, ARM will concatenate and
subset before sending. This is much cheaper than pulling whole daily files:

```python
files = armlive_list_files("sgpmetE13.b1", "2024-06-01", "2024-06-30")
path  = armlive_subset(files, variables=["temp_mean", "rh_mean"], filetype="csv")
```

`filetype` is `'csv'` or `'cdf'`. Two things the raw ACT call
(`act.discovery.download_arm_data_mod`) does that will trip you up, and that
`armlive_subset` handles: it needs **bare filenames** (no directory component), and
it returns only the filename, not the path it wrote to.

## Reading ARM netCDF

`act.io.arm.read_arm_netcdf(filenames, ...)` wraps `xarray.open_mfdataset` with
ARM-specific time handling. The options that matter:

- `keep_variables=[...]` — read only these. On a 51-variable met file this turns a
  multi-second read into a hundredth of a second, and it is the difference between a
  month of data fitting in memory and not. Ask for the QC variable too
  (`["temp_mean", "qc_temp_mean"]`) or you lose the flags.
- `cleanup_qc=True` — convert ARM's bit-packed QC attributes to CF
  `flag_masks`/`flag_meanings`/`flag_assessments`. Required before any `qcfilter`
  method or QC block plot works. It takes no options; for non-default cleanup call
  `ds.clean.cleanup(...)` yourself afterwards.
- `use_base_time=True` — for older files with a missing or malformed `time` units
  string, rebuild time from `base_time` + `time_offset`. Setting it forces
  `decode_times=False` and `use_cftime=False`.
- `combine`, `concat_dim`, `data_vars` — passed to xarray; the defaults
  (`combine='by_coords'`, `data_vars='all'`) suit same-datastream daily files.

Sort the file list before reading — ARM Live returns files in archive order, and
`by_coords` will complain about non-monotonic time if two files overlap.

Other IO entry points, all under `act.io`: `read_arm_mmcr`, `create_ds_from_arm_dod`
(build an empty dataset from an ARM Data Object Design template),
`check_arm_standards` / `act.utils.arm_standards_validator` (check a file against
ARM's file-format standards), `WriteDataset` via the `ds.write` accessor,
`check_if_tar_gz_file` plus `act.utils.unpack_tar` / `unpack_gzip` for the packed
products, and readers for ICARTT, NOAA GML/PSL, NEON, AmeriFlux, MPL and SP2.

## Other discovery services in ACT

`act.discovery` is not ARM-only. All of these follow the same shape — a function that
downloads to a directory and returns paths or a Dataset:

| Function | Source | Host reachable here |
|---|---|---|
| `download_arm_data`, `download_arm_data_mod`, `get_arm_doi` | ARM Data Center | yes (`adc.arm.gov`) |
| `download_noaa_psl_data` | NOAA PSL profilers | yes (`downloads.psl.noaa.gov`) |
| `get_asos_data` | Iowa Environmental Mesonet ASOS | needs allowlist (`mesonet.agron.iastate.edu`) |
| `get_airnow_obs`, `get_airnow_forecast`, `get_airnow_bounded_obs` | EPA AirNow (needs own API key) | needs allowlist (`www.airnowapi.org`) |
| `get_neon_site_products`, `download_neon_data` | NEON | needs allowlist (`data.neonscience.org`) |
| `download_ameriflux_data` | AmeriFlux (needs own account) | needs allowlist (`amfcdn.lbl.gov`) |
| `download_surfrad_data`, NOAA GML readers | NOAA SURFRAD/GML | needs allowlist (`gml.noaa.gov`) |
| `get_crop_type` | USDA CropScape | needs allowlist (`nassgeodata.gmu.edu`) |
| `download_mplnet_data`, `get_mplnet_meta` | NASA MPLNET (needs own token) | needs allowlist (`mplnet.gsfc.nasa.gov`) |
| `get_improve_data` | IMPROVE aerosol network | untested |

When one of these is blocked, call `request_network_access(domain=...)` rather than
reporting the source as unavailable.

## Kernel helpers

Loaded automatically with this skill:

- `armlive_credentials()` -> `(username, token)`
- `armlive_list_files(datastream, start, end)` -> filenames, `[]` if nothing
- `armlive_download(datastream, start, end, output=None, time=None)` -> paths
- `armlive_open(datastream, start, end, keep_variables=None, cleanup_qc=True)` -> Dataset or None
- `armlive_subset(filenames, variables=None, filetype='csv')` -> path to the concatenated file
- `arm_datastream_parts(name_or_path)` -> dict of site/class/facility/level/date/time
- `arm_facility_latlon(site_code, facility_code=None)` -> lat/lon dict

## Gotchas worth remembering

- **`time=` is a filename substring match, not a time selection.** `time="173300"`
  keeps only files whose name contains that literal string; a sounding launched at
  17:32 is silently skipped and you get an empty list back with no error.
- A wrong username or token surfaces as `ConnectionRefusedError('Error with user...')`,
  not an HTTP status.
- `download_arm_data` creates the output directory even when nothing is downloaded,
  so "the folder exists" is not evidence the fetch worked. Check the returned list.
- Requesting an `a0` datastream returns nothing plus an advisory notice — that is a
  policy restriction, not a bug in your date range.
- The DQR web service used by `act-qc` lives on a different host
  (`dqr-web-service.arm.gov`) and is allowlisted separately from `adc.arm.gov`.
