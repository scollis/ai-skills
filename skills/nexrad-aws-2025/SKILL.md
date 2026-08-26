---
name: nexrad-aws-2025
description: Access WSR-88D NEXRAD radar on AWS after the 2025 bucket migration - the Unidata Level II archive (s3://unidata-nexrad-level2), the real-time chunks bucket, Level III, and the NEXRAD ARCO Icechunk/Zarr stores (s3://nexrad-arco, including the new per-site "lowsweeps" base-tilt cubes). Use for the correct post-deprecation bucket names, VCP tables (11/12/21/31/32/34/35/112/121/211/212/215), detecting SAILS / MESO-SAILS / MRLE / AVSET dynamic scanning, NEXRAD split cuts, and the ARCO layout traps (SAILS volumes fragmented across scan indices, -999 fill, virtual chunk auth, TLS/CA, time epochs). Triggers - NEXRAD, WSR-88D, Level II, unidata-nexrad-level2, nexrad-arco, noaa-nexrad-level2, SAILS, MESO-SAILS, MRLE, AVSET, VCP, split cut, Py-ART, icechunk, radar datatree.
---

# NEXRAD on AWS after the 2025 migration

Everything here was verified against the live buckets on **2026-08-25** (see
"Verified against" at the end). `kernel.py` auto-loads into the python kernel
when this skill is loaded.

## 1. The buckets (the thing that changed)

| Purpose | Bucket | Key layout | Latency |
|---|---|---|---|
| **Level II archive** | `unidata-nexrad-level2` | `YYYY/MM/DD/SITE/SITEYYYYMMDD_HHMMSS_V06` | ~7 min |
| **Level II real-time** | `unidata-nexrad-level2-chunks` | `SITE/<volnum>/YYYYMMDD-HHMMSS-NNN-{S,I,E}` | seconds |
| **Level III products** | `unidata-nexrad-level3` | `SITE_PROD_YYYY_MM_DD_HH_MM_SS` (flat) | minutes |
| **ARCO (Zarr/Icechunk)** | `nexrad-arco` | `<SITE>/`, `<SITE>-lowsweeps/` | ~8 min |
| ~~legacy~~ | ~~`noaa-nexrad-level2`~~ | **DEAD** | — |

**`noaa-nexrad-level2` is gone.** Since the Sep-2025 deprecation it returns a
genuine S3 `AccessDenied` on both listing and object GET. That is *not* a
sandbox proxy artifact and *not* a permissions problem you can work around —
if you see it, you are using the old bucket name. Never code a fallback to it.

All buckets are `us-east-1` and **anonymous/unsigned** — no credentials.
`kernel.py`'s `s3_anon()` builds the right client; passing signed credentials
can *fail* where unsigned succeeds.

Sandbox note: the archive bucket is reachable by default. The others each need
a one-time network grant for `<bucket>.s3.amazonaws.com`, and the ARCO Rust
client specifically needs the **virtual-hosted regional** host
`nexrad-arco.s3.us-east-1.amazonaws.com`. Path-style `s3.amazonaws.com` is
denylisted and cannot be granted.

```python
c = s3_anon()
keys = nexrad_keys("KLOT", dt.datetime(2026,7,27,16), dt.datetime(2026,7,27,19), client=c)
path = download_volume(keys[0]["key"], "vols/")
radar = read_nexrad_volume(path)          # or pass the S3 key directly
sites = nexrad_sites()                     # 202 sites reporting
```

**Filter `*_V06_MDM` sidecars.** Each day carries a couple dozen MDM objects
that share a timestamp with a real volume but are 0.65-0.7 MB against 4-9 MB.
Passing one to Py-ART fails or yields a stub. `nexrad_keys` excludes them by
both suffix and a `min_bytes` floor — the size floor is the robust half.

Other archive-bucket facts: 37 year-prefixes, and `1970/01/` is a synthetic
TDWR placeholder (`*_V08`), not real 1970 data. Real coverage starts 1991.

The chunks bucket is the live LDM feed: `S`/`I`/`E` = start / intermediate /
end of volume, `volnum` cycles 1-999 so sort by the **timestamp**, not the
volume number. Use it only when you need sub-minute latency; otherwise the
archive bucket is simpler and complete.

## 2. VCPs

`vcp_info(212)` returns nominal elevations, mode, cycle time, and split-cut
count from `VCP_TABLE`. Elevations listed there are the **ascending backbone**:
split cuts collapsed, supplemental cuts excluded.

Precip patterns: **12** and **212** (14 tilts, ~4.2 min, dense low-level — the
convective workhorses), **215** (15 tilts, deep/tropical), **11**/**21**/
**121**/**211** (legacy). Clear-air: **31** (long pulse, most sensitive — best
for snow and light rain), **32**, **34**, **35**. The `2xx`/`1xx` families are
SZ-2 phase-coded and MPDA variants of their base pattern, which matters for
velocity dealiasing but not for reflectivity geometry.

## 3. Split cuts — the #1 source of silent wrong answers

In VCP 12/212/215 the three lowest tilts are each scanned **twice**: a
long-PRT **surveillance** cut (reflectivity + dual-pol, full unambiguous
range) and a **Doppler** cut (velocity, shorter range). A 17-sweep VCP-212
volume therefore holds only **14 distinct elevations**.

Two consequences:

- `pyart.xradar.Xradar.__init__` runs `np.unique` on `sweep_fixed_angle`, so
  `fixed_angle` comes back with 14 entries for 17 sweeps and any code indexing
  it by sweep number raises `IndexError`.
- **Never pick a sweep by "first field present."** Py-ART builds its field dict
  from a set, so under hash randomisation the first key differs *between
  processes for a byte-identical file*. On a split cut that flips which member
  you select — measured on KLOT VCP-212, gridded volume max alternated between
  67.60 and 86.86 dBZ across fresh processes, 9 of 20 taking the wrong sweep.
  Select by elevation and cut kind, never by field iteration order.

```python
df   = scan_anatomy(radar)               # per-sweep elev/rays/timing/kind + split partner
keep = dedup_split_cuts(radar, prefer="surv")   # 14 indices, one per elevation
```
Use `prefer="surv"` for reflectivity/dual-pol work, `"dop"` for velocity.

## 4. SAILS, MESO-SAILS, MRLE, AVSET

Modern RDA builds insert **supplemental** low-level cuts mid-volume and can
**truncate** upper tilts, so *sweep count is not fixed for a given VCP*.

- **SAILS** — one extra base-tilt cut mid-volume. **MESO-SAILS** — up to three
  (`SAILSx1..x3`), halving base-tilt revisit to ~2 min.
- **MRLE** — repeats the *lowest 2-4 tilts* as a block, not just the base tilt.
- **AVSET** — terminates the volume early once upper tilts hold no echo, so the
  top elevation falls short of the VCP's nominal top.

```python
cls = classify_scan(radar.fixed_angle["data"], radar.metadata["vcp_pattern"])
# -> {'mode': 'SAILSx2'|'MRLE+4'|'none', 'avset_active': bool, 'backbone': [...], ...}
```

`classify_scan` collapses split cuts, then treats every **descent** in the
elevation sequence as the start of a supplemental block: all-base-tilt blocks
are SAILS, multi-tilt blocks are MRLE, and a backbone top below the VCP's
nominal top sets `avset_active`.

Measured on 61 consecutive KLOT volumes (27 Jul 2026, all VCP-212) — one
radar produced **three different scan configurations in five hours**, which is
why this must be detected per volume rather than assumed:

| nsweeps | mode | supplemental cuts | count |
|---|---|---|---|
| 17 | `none` | — | 15 |
| 21 | `SAILSx2` | `[0.48]`, `[0.48]` | 29 |
| 24 | `MRLE+4` | `[0.48, 0.88, 1.27, 1.80]` | 17 |

Base-tilt revisit tightens accordingly: median 126 s during that outbreak
against 279 s in a quiet period. **Do not assume a uniform time step** in any
base-tilt time series.

## 5. NEXRAD ARCO (Icechunk / Zarr v3)

`s3://nexrad-arco` — WMO FM301 / CfRadial2-compliant analysis-ready NEXRAD,
maintained by AtmoScale, one **Icechunk V2** repo per site, grouped
`VCP-<id>/sweep_<n>`. Each sweep array is `(scan_index, azimuth, range)`
chunked `(1, nrays, ngates)` — one chunk per sweep per scan. Fields use ODIM
names: `DBZH`, `ZDR`, `RHOHV`, `PHIDP`, `VRADH`, `WRADH`, `CCORH`.

```python
root = arco_open("KLOT")                     # zarr root group, anonymous
inv  = arco_vcps(root)                       # one row per VCP + scan-config attrs
i, t = arco_nearest(root, "VCP-212", "2026-07-27T17:00")
ds   = arco_sweep(root, "VCP-212", i, sweep=0)   # georeferenced, -999 masked
```

Coverage is currently **site-limited** — the README advertises many sites but
as of verification the bucket holds only `KLOT/` and `KLOT-lowsweeps/`. Check
`s3_anon().list_objects_v2(Bucket="nexrad-arco", Delimiter="/")` before
assuming a site exists. KLOT holds 12 VCP groups spanning 2015 → within ~8
minutes of real time.

Modern VCP groups now carry scan-configuration attributes worth reading before
you analyse: `avset_enabled`, `num_base_tilts`, `dynamic_scan_type`,
`vcp_truncated`, `super_res_status`, `rda_build_number`. Groups written before
this addition report `None`.

### 5a. `<SITE>-lowsweeps` — the base-tilt cube

A **second, flat repo** per site: no VCP grouping, just `sweep_0`
(surveillance: `DBZH`, `ZDR`, `RHOHV`, `PHIDP`) and `sweep_1` (Doppler:
`DBZH`, `VRADH`, `WRADH`), each a single ~1.0M-scan time series of the 0.48°
cut spanning **2015-01-01 → now** across every VCP. This is the right store
for long base-tilt climatologies — one cube instead of stitching 12 VCP
groups. Group attrs carry per-cut provenance (`sails_cut`,
`sails_sequence_number`, `mrle_cut`, `base_tilt_cut`, `waveform_type`).

```python
lroot = arco_open("KLOT", lowsweeps=True)
t     = arco_times(lroot, "sweep_0")     # 2015-01-01 -> now, ~1.0M scans
```

### 5b. ARCO layout traps

**One physical volume can span several scan indices.** When SAILS is running,
the writer splits a volume across *consecutive* indices — measured on KLOT
VCP-212 during the 27 Jul 2026 outbreak, a repeating 3-index cycle:

```
idx 221845  16:59:45   0.48 0.48 0.88 0.88 1.27 1.27          <- low cuts
idx 221846  17:01:52   0.48 0.48 1.80 2.42 3.08 4.00 5.10 6.42 <- mid cuts
idx 221847  17:03:58   0.48 0.48 8.00 10.02 12.48 15.60 19.51  <- upper cuts
```

Grid `arco_sweep(root, "VCP-212", 221845)` alone and you have silently kept 6
of 17 sweeps and lost everything above 1.27°. Use
`arco_volume_indices(root, group, i)` — it returns `[221845, 221846, 221847]`
there and `[i]` in quiet periods, where an index *is* a whole volume.
Unrecorded sweeps at an index have a NaN `sweep_fixed_angle` and a
non-positive first-ray `time`; `arco_scan_elevations` reports both.

**`-999` is not masked for you.** Float fields store the sentinel `-999.0`,
and the `_FillValue` attribute is **base64-encoded** in the metadata, so
neither zarr nor xarray decodes it. In a low sweep ~75% of gates are `-999`;
unmasked they enter your analysis as -999 dBZ. `arco_sweep` masks by default;
otherwise call `arco_mask(array)`.

**Virtual chunk containers need authorization.** Some groups reference chunks
by `s3://nexrad-arco/` URL. Without explicit anonymous authorization, reads
raise *"a virtual chunk in this repository resolves to the url prefix..."*.
`arco_open` passes `authorize_virtual_chunk_access=containers_credentials({...})`.
Note the type: `s3_credentials(anonymous=True)`, **not** `s3_store(...)` —
passing the store config raises `'ObjectStoreConfig.S3' object is not an
instance of 'Credentials'`.

**TLS/CA must be fixed before the first `import icechunk`.** The Rust
`object_store` client does not read certifi and fails the handshake with
`invalid peer certificate: UnknownIssuer`. The native trust store initialises
**once per process and is cached** — `importlib.reload` does not reset it, so a
kernel that already imported icechunk without the fix must be restarted. Call
`ensure_ca()` (or just use `arco_open`) *before* any icechunk import.

**Two different time epochs.** Per-ray `time` arrays are `nanoseconds since
1950-01-01`; the lowsweeps `vcp_time` axis instead carries its own units
attribute (`nanoseconds since 2015-01-01 00:09:35.13...`). Decoding lowsweeps
against 1950 yields times in **1950-1961** — an obviously wrong answer that is
easy to miss. `arco_times` reads the `units` attribute and handles both. Note
that plain `xr.open_datatree` refuses these arrays outright ("unable to decode
time units 'nanoseconds since...'"), because CF/cftime does not accept
nanosecond units — pass `decode_times=False` if you go through xarray.

**Read `vcp_time` whole; never scan `time` by column.** `vcp_time` is coarsely
chunked (whole-array per VCP, ~62k for lowsweeps), so reading all 226k values
is one request and ~1.3 s — then `np.searchsorted`. The per-ray `time` array is
chunked `(1, nrays)`, so `time[:, 0]` over 226,560 scans issues that many S3
requests and never finishes.

**Prefer zarr over `xr.open_datatree` for discovery.** A site repo has ~12 VCP
groups x 8-20 sweeps; `open_datatree` eagerly opens and CF-decodes all of them
(minutes, and it hits the time-units error above). `arco_open` returns a lazy
zarr group instead.

**ARCO azimuths are pre-regridded.** Each sweep group stores azimuth as a
*shared* 1-D coordinate (720 or 360 values reused across all scans) on an exact
0.5°/1.0° grid. Raw Level II has real per-ray jitter (up to 0.19 of nominal
spacing on KLOT). So ARCO is unsuitable for testing anything sensitive to
azimuth non-uniformity (non-uniform FFT / spectral gridding paths) — use raw
Level II from `unidata-nexrad-level2` for that.

## 6. Choosing a source

- **Case study, a few volumes, need true ray geometry** → `unidata-nexrad-level2` + Py-ART.
- **Long time series at low tilts** → ARCO `<SITE>-lowsweeps`.
- **Full volumes over a long period, cloud-native** → ARCO `<SITE>/VCP-*` (mind §5b).
- **Sub-minute latency** → `unidata-nexrad-level2-chunks`.
- **Site not in ARCO** → raw Level II; ARCO coverage is still limited.

## Environment

`arm-pyart`, `xradar>=0.12`, `xarray`, `zarr>=3`, `icechunk>=2`, `boto3`,
`certifi`, `pandas`; `cmweather`/`cartopy` for plotting. In this project: env
`radar`. `rustytree-xarray` is optional — the helpers here use zarr directly.

Related skills: `nexrad-arco` (earlier ARCO workflow, Py-ART conversion,
METAR overlays), `nexrad-radar-gcs` (GCS mirror + plotting helpers),
`nexrad-site-rainfall`, `nexrad-area-over-threshold`.

## Verified against

Live buckets on **2026-08-25**: archive bucket 202 sites, KLOT latest volume
7 min old; ARCO KLOT 12 VCPs / 457 snapshots, current to ~8 min;
`KLOT-lowsweeps` 1,007,472 scans, 2015-01-01 → now. SAILS/MRLE/AVSET tables
measured on 61 KLOT VCP-212 volumes from 27 Jul 2026 and on ARCO scan indices
221843-221850 / 226557-226559. All 46 helper checks in the skill's test pass.
Re-verify bucket names and ARCO site coverage if much time has passed.
