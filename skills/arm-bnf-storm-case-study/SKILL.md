---
name: arm-bnf-storm-case-study
description: "Build an end-to-end storm case study at ARM's Bankhead National Forest (BNF) site from C-SAPR2 dual-polarisation radar, optionally paired with NASA NALMA total lightning. Use whenever the user names a BNF or C-SAPR2 storm/date, asks for BNF radar data, wants dual-pol PPI or RHI plots, echo-top vs freezing-level analysis, hail-vs-rain discrimination, lightning-updraft comparison, or a reproducible notebook for such a case. Covers ARM Live staging, the single interleaved bnfcsapr2cfr datastream, sounding-derived 0/-20 C levels, KMZ site overlays, the CMR->GHRC->CloudFront Earthdata chain for NALMA, and RHI animations with VHF sources projected onto the scan plane. Ships kernel.py helpers for staging, gate filtering, echo tops, echo areas, sounding levels, NALMA parsing and RHI-plane projection. Triggers: BNF, Bankhead, C-SAPR2, CSAPR, ARM Live, NALMA, lightning mapping array, Earthdata, GHRC, dual-pol, Z_DR, rho_HV, echo top, RHI, squall line."
---

# ARM BNF storm case studies

Pair ARM's **C-SAPR2** dual-polarisation radar at Bankhead National Forest with
NASA's **NALMA** lightning array to characterise a convective event: what the
precipitation is, how deep the updraft got, and how the electrification
responded.

The helpers below encode the data-access paths and the handful of settings that
otherwise cost an afternoon to rediscover. The science reasoning is yours; these
just remove the friction.

## Data access

### C-SAPR2 radar (ARM Live)

```python
import datetime as dt
day   = dt.date(2026, 7, 1)
start = dt.datetime(2026, 7, 1, 18, 0)
end   = dt.datetime(2026, 7, 1, 21, 0)
paths = arm_stage_window("bnfcsapr2cfrS3.a1", day, start, end, "~/data/bnf/case")
ppi_files, rhi_files = split_ppi_rhi(paths)
```

**BNF publishes ONE interleaved datastream** — `bnfcsapr2cfrS3.a1` mixes 15-sweep
PPI volumes with single-sweep RHIs. There are no separate `cfrppi` / `cfrhsrhi`
streams as at other ARM sites, so guessing those names returns zero files.
`split_ppi_rhi` separates them on file size (~693 MB vs ~20 MB) without opening
each one.

Confirm the deployment year before assuming a date exists — BNF C-SAPR2 begins in
2026, so a "July 1st" case is 2026, not 2025. If a query returns nothing, probe
adjacent years with `arm_query` before concluding the data is missing.

Volumes are large: a 3-hour window is ~12 GB. `arm_fetch` skips files already on
disk, so re-running is cheap.

### NALMA lightning (NASA Earthdata)

```python
granules = cmr_granules("nalma", start, end)          # (title, url) pairs
for title, url in granules:
    earthdata_fetch(url, pathlib.Path(nalma_dir) / title)
```

Three hops, and the middle one is where people get stuck:

1. **CMR** — granule search. Query it rather than constructing filenames; it
   catches boundary granules a hand-built loop misses.
2. **GHRC** — the URL in each granule record, which 302s to Earthdata Login.
3. **CloudFront** — after authentication GHRC issues a *signed redirect* to a CDN
   host. Behind a network allowlist that third host must also be permitted;
   successful authentication is not sufficient. The signed URL carries
   `A-userid=<name>`, which is how you tell auth succeeded even while the
   download still fails.

Authentication is `.netrc` with the **short EDL username, not the email address**.
Supplying the email gives a 401 indistinguishable from a wrong password. The DAAC
must also be approved once under EDL profile -> Applications -> Authorized Apps,
which produces the same 401 when missing. Two failure modes, one symptom — check
both before assuming the password is wrong, and stop after one or two attempts
since repeated failures can lock an EDL account.

### Credentials

Read them at runtime; never write them into a notebook, script, or artifact.
`arm_credentials()` checks `ARM_USER`/`ARM_TOKEN`, then a credential store, then
`~/.arm_live_creds.json`. Earthdata uses `~/.netrc` (or `NETRC_PATH`), which the
**user** should create.

If a user offers a password in chat, decline it and point them at the credential
store or a `.netrc` they write themselves — anything you type into a cell is
persisted in the execution log. When you verify a file is credential-free, scan
using values pulled from the store at runtime; retyping a secret as a literal to
check for it defeats the purpose. If a secret does reach the transcript, say so
plainly and recommend rotation.

## Analysis

### Gate filtering: quantitative vs display

```python
gf = dualpol_gatefilter(radar)                  # despeckle + SNR + rho_HV + Z floor
scan = read_rhi(path, filtered=True)            # quantitative
scan = read_rhi(path, filtered=False)           # display: raw Z_H
```

Filter for measurement; don't filter for display. `filtered=False` leaves Z_H
fully raw (~98% of gates populated vs ~10% filtered) and masks only sub-noise
gates in Z_DR and velocity, which are pure noise without signal and otherwise
swamp the panel. The filtered view discards real weak-echo anvil, shallow
low-level returns, and the clutter fan — fine for statistics, misleading as a
picture of the storm.

`pyart.correct.despeckle_field` is a module-level function that *returns* a
GateFilter; it is not a GateFilter method.

### Hail or heavy rain?

A 60 dBZ core at C band invites a hail reading. Test it rather than assuming:
hail tumbles and depolarises (low Z_DR, depressed rho_HV), while large oblate
raindrops give high Z_DR with rho_HV near unity. Report medians over the
`Z >= 50 dBZ` gates and the fraction meeting a hail signature — in the July 2026
BNF case that was Z_DR ~ 4.1 dB, rho_HV ~ 0.97, and ~1% hail-like, i.e. heavy
rain.

### Updraft depth against the charging zone

```python
z0   = sounding_temperature_level(sonde,   0.0, ref_alt_m=radar_alt)
zm20 = sounding_temperature_level(sonde, -20.0, ref_alt_m=radar_alt)
tops = [echo_top(read_rhi(f), 40.0) for f in rhi_files]
```

The 40 dBZ echo top means little in isolation; relative to the -20 C level from
the nearest pre-storm sounding it measures how far precipitation-sized particles
were lofted into the mixed-phase layer. Use the sonde launch *before* the event.

`echo_top` returns NaN when no gate reaches the threshold. Keep those as gaps —
plot only valid points so the line does not bridge scans where the azimuth missed
the convection, and say so in the figure.

### Growth vs intensification

`sweep_echo_areas` gives range-weighted areas above several thresholds. Rising
area above 40 dBZ while the 50 dBZ area holds steady means the system is
expanding its footprint, not intensifying its cores — a different claim from peak
reflectivity, and usually the more interesting one.

### Lightning on the RHI plane

```python
src   = np.vstack([read_nalma_sources(p) for p in nalma_paths])
good  = src[nalma_quality_mask(src)]                      # chi2<=1, >=7 stations
along, cross, alt, in_plane = project_sources_to_rhi_plane(
    good, radar_lon, radar_lat, azimuth=210.0, half_width_km=10.0)
```

QC first: the solver accepts chi2 <= 5, but scientific use wants chi2 <= 1 and
>= 7 contributing stations, which keeps ~13% over a full event window. Then
select sources within a few minutes of the scan and plot `along` vs `alt`.

Projecting a 3-D point cloud onto a 2-D cut inevitably includes sources from
convection beside the slice, so state the tolerance in the panel rather than
implying every point lies in the plane.

**Marker styling matters more than it sounds.** With thousands of sources per
frame, filled opaque markers become a white blob that hides the radar data.
Small black open circles (`s=4.5, facecolors="none", edgecolors="k",
linewidths=0.32, alpha=0.6`) stay readable over ChaseSpectral, balance, and the
rho_HV maps alike — a single colour that works on every background beats tuning
per panel.

### Interpreting the pairing

Source rate and echo-top height covarying (r ~ 0.85 in the BNF case) supports a
shared driver: the updraft lofting precipitation above -20 C is also driving
charge separation. It does **not** establish timing. With ~13 radar scans the
lagged correlations are flat and cannot resolve whether lightning leads or lags;
report covariation and say what would be needed for a timing claim.

## Plotting

Call `setup_radar_plotting()` before the first figure. It fixes two things that
fail confusingly:

- `savefig.bbox="tight"` silently mis-crops cartopy GeoAxes, dropping panels
  placed at explicit figure rectangles. Set it to `"standard"`.
- Cartopy caches shapefiles inside its package directory; if that is read-only
  you get `PermissionError`. Redirect to a writable path.

**Do not use `tight_layout` or `constrained_layout` with cartopy GeoAxes.** The
gridliner is evaluated at draw time and can raise `LinAlgError: Singular matrix`
or silently displace panels. Place axes at explicit rectangles
(`fig.add_axes([...])`) and add colorbars as their own axes. Set
`x_inline=False, y_inline=False` on gridlines or labels land inside the map.

Use `cmweather` maps: `ChaseSpectral` for reflectivity, `balance` with
`TwoSlopeNorm(vcenter=0)` for signed fields, `cm_colorblind.CM_rhohv` for
correlation. Centre diverging maps on physical zero, not the data midpoint.

Py-ART may return `cftime` objects that matplotlib cannot plot; `to_datetime`
coerces them. `read_rhi` already does this.

### Map georeferencing — do not let Py-ART pick the projection

`pyart.graph.RadarMapDisplay.plot_ppi_map` sets up a cartopy
`AzimuthalEquidistant` axes centred on the radar. **That transform is inaccurate
at its own origin when `central_latitude != 0`**, so the whole gate field is
drawn displaced from the site. At BNF the site's own coordinates transform to
`(0, +21448 m)` instead of `(0, 0)` — every echo lands ~21 km too far south.

The tell is that the radar marker sits north of its own clutter fan / cone of
silence. It is not a data problem: Py-ART's `gate_longitude` / `gate_latitude`
are correct spherical-earth coordinates (they agree with the site metadata to
<50 m at range zero). Only the axes projection is wrong.

Build the axes yourself — Mercator, with gates and every marker drawn through
`PlateCarree` so no AEQD round-trip happens anywhere:

```python
ax = fig.add_axes(rect, projection=ccrs.Mercator(central_longitude=radar_lon))
ax.set_extent(extent, crs=ccrs.PlateCarree())
glon, glat, field = ppi_gate_latlon(radar, "reflectivity", sweep=0, gatefilter=gf)
ax.pcolormesh(glon, glat, field, transform=ccrs.PlateCarree(), cmap="ChaseSpectral")
ax.plot(radar_lon, radar_lat, marker="^", transform=ccrs.PlateCarree())
```

`aeqd_origin_offset(radar)` returns the displacement in metres for the radar at
hand — print it once to confirm the diagnosis rather than assuming 21 km, since
it scales with latitude. `ppi_gate_latlon` returns the sweep's gate coordinates
with the gatefilter already applied.

Verify after plotting, not before:

- the near-range clutter centroid coincides with the site (`clutter_centroid`),
- ground-site markers land on the echoes that their gauges recorded,
- state boundaries and rivers line up with storm structure.

The same rule applies to any Cartesian product derived for display. Quantitative
results computed from native gate geometry (`get_gate_x_y_z`, RHI range/height
arrays, per-gate field statistics) never touch the map projection and are
unaffected by this bug — say so explicitly when correcting a figure, or a reader
will assume the numbers moved too.

### Site overlays

`parse_bnf_kmz(dest)` returns the BNF placemarks (41 points, 40 unique names --
S10 appears twice), but ~30 are instruments within ~200 m at M1. Filter to the
spatially distinct facilities (M1, S3, S4, S20, S30, S40) plus nearby towns, and
let M1 stand for the instrument field.
The KMZ's S3 entry should coincide with the radar's own metadata — a free
geometry check worth printing.

Fetch the KMZ from the `github.com/.../raw/...` URL; `raw.githubusercontent.com`
returns a 404 stub for this path.

## Caveats to state in any writeup

These are real limits of the measurement, not boilerplate:

- **No attenuation correction** — C-band Z_H and Z_DR are biased low behind a
  60 dBZ core, visible as a negative Z_DR streak downrange. Correct before
  quantitative rain rates.
- **Velocity is aliased** at the +/- 16.3 m/s Nyquist; abrupt red-blue
  transitions aloft are folding, not shear. Dealias before kinematic work.
- **An RHI is a fixed azimuth** — apparent intensity changes partly reflect the
  storm translating across the plane. PPI-derived areas are the better growth
  measure.
- **NALMA geometry** — BNF sits ~76 km from the network centre, so source
  *altitudes* carry ~km-scale error while *rates* stay robust. Read vertical
  clustering as a layer, not a precise height.

## Producing a notebook

When the user wants a reproducible artifact, build the notebook with `nbformat`,
clear outputs, and verify it by extracting the code cells to a script and running
that end-to-end — `nbconvert --execute` needs to bind a kernel socket, which some
sandboxes block. Confirm the numbers in your prose match the executed output, and
scan the saved file for credentials before sharing.

For a PR into a notebook collection, match the repo's conventions: check whether
its READMEs are generated from an inventory file and update all of them
consistently, follow the local naming and `*_outputs/` layout, and put the science
findings in the PR body rather than a list of changed files. Verify pushed content
against the local copy instead of trusting the API response.
