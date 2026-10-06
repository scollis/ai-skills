---
name: gpm-storm-targeted-radar-fetch
description: Use GPM DPR overpasses as the storm detector over a ground-radar domain, then fetch only the matching radar volumes from ARM Live. Screens NASA CMR for satellite passes containing a site, opens granules with gpm-api to count precipitating footprints within range, derives the true swath-crossing time, and pulls the handful of coincident ground-radar scans for spaceborne-ground (SR-GR) reflectivity calibration. Use for GPM overpass screening, DPR coincidence, satellite-radar matchup case selection, ARM Live targeted download, storm identification over a radar site, or building an SR-GR calibration dataset. Also covers download-integrity checks (Content-Length truncation, HEAD-based RHI/PPI classification, readability gating) and surviving ARM Live service degradation. Triggers GPM, DPR, 2AKu, overpass, CMR, gpm-api, volume_matching, ARM Live, ACT, C-SAPR2, SR-GR, spaceborne, coincidence, storm screening, matchup, truncated download, RHI filtering.
---

# GPM-targeted radar case selection

Selecting ground-radar data by satellite coincidence rather than by convenience. The
pipeline is: screen for overpasses, find which ones had rain over the domain, then fetch
only the few radar scans that bracket those crossings.

This is cheap because a DPR swath crosses a 115 km domain in about **30 seconds**. One
overpass therefore corresponds to one or two ground-radar volumes — but those volumes
can yield hundreds of matched footprints, so a handful of well-chosen scans beats weeks
of arbitrary data.

Helpers auto-load into the python kernel: `cmr_overpasses`, `dpr_domain_crossing`,
`armlive_query`, `armlive_file_size`, `select_scans_by_size`, `filename_time`,
`beam_height`, `ground_range_azimuth`.

## Credit

The SR-GR methodology follows the **ERAD 2026 short-course notebook "Spaceborne-Ground
Radar Calibration"** (openradarscience.org/erad2026/notebooks/gpm-api/sr-gr-calibration/),
authored by Alfonso Ladino, Anna del Moral Méndez, Brenda Javornik, Daniel Michelson,
**Gionata Ghiggi**, Hamid Ali Syed, Jen DeHart, Kai Mühlbauer, Maxwell Grover, Mike Dixon,
Robert Jackson, Scott Collis, Ting-Yu Cha and Zachary Sherman. It is part of the GPM-API
documentation, MIT licensed.

**GPM-API is developed by Gionata Ghiggi** and does the heavy lifting here — granule
opening, bin/height/temperature slicing, retrievals, and the frequency-conversion
utilities. Cite it and the notebook in any work built on this skill.

Underlying method papers:

- Schwaller, M. R., & Morris, K. R. (2011). A Ground Validation Network for the Global
  Precipitation Measurement Mission. *J. Atmos. Oceanic Technol.*, 28(3), 301-319.
  doi:10.1175/2010JTECHA1403.1 — the volume-matching approach.
- Warren, R. A., Protat, A., Siems, S. T., Ramsay, H. A., Louf, V., Manton, M. J., &
  Kane, T. A. (2018). Calibrating Ground-Based Radars against TRMM and GPM.
  *J. Atmos. Oceanic Technol.*, 35(2), 323-346. doi:10.1175/JTECH-D-17-0128.1 — the
  24-36 dBZ window and the adaptation the notebook implements.
- Cao, Q., et al. (2013). Empirical conversion of the vertical profile of reflectivity
  from Ku-band to S-band frequency. *JGR Atmos.*, 118, 1814-1825. doi:10.1002/jgrd.50138
  — behind gpm-api's `c_band_tan` style conversions.

Stratiform-only selection above the melting layer is credited in the notebook to
W. Petersen (2017, personal communication) as GPM DPR ground-validation practice — note
it is *not* from Warren et al.

## Surface gauges cannot do this job

The instinct is to find storms with the site's rain gauges and then look for overpasses.
That fails, and not marginally.

At an ARM site, one verified case had the DPR reporting **164 precipitating footprints
within 115 km while every surface gauge across four sites read exactly zero** for a full
hour either side. The rain was in the radar's view but not over the instruments — point
gauges sample a vanishing fraction of a 40,000 km² domain. A gauge-based screen would
have discarded the single overpass that turned out to be usable.

**Screen with the swath, not the gauges.** Gauge data remains valuable for
disdrometer-based calibration and rain-rate context; it is just the wrong storm detector
for a radar domain.

## Step 1: screen CMR for overpasses

```python
ov = cmr_overpasses(site_lat, site_lon, "2026-06-15", "2026-08-25",
                    short_name="GPM_2AKu", version="08")
```

CMR is authoritative. **Do not propagate a TLE for this** — at ~7.3 km/s a 60 s epoch
error displaces the ground track ~440 km, so a TLE more than a few days off the target
date cannot place a swath against a 115 km domain.

**The version string fails silently.** `version="07"` returns zero granules with HTTP 200
for a period where `version="08"` returns twenty. Always sanity-check the count against a
known pass, or pass `version=None`. Note the product version in the filename (`V08A`) is
not the CMR version token (`08`).

Expect roughly one overpass every 3-4 days at mid-latitudes — about 20 per 10 weeks.

## Step 2: find which overpasses had rain in the domain

Download each granule, count precipitating footprints inside the domain, discard the
file. The screen needs a handful of small variables, not the 200 MB granule, so peak disk
stays flat instead of accumulating gigabytes.

```python
ds = gpm.open_granule_dataset(path, scan_mode="FS")
info = dpr_domain_crossing(ds, site_lat, site_lon, domain_km=115.0)
```

Record `n_precip_domain`, `n_precip_60km` (inner domain, better geometry), the
stratiform/convective split from `typePrecip`, and a reflectivity percentile. Those
numbers rank the cases — and the count of qualifying passes tells you whether a
multi-overpass analysis is viable at all, which is worth knowing *before* staging radar
data.

Two traps, both of which produce plausible-looking wrong answers:

**The granule midpoint is not the crossing time.** A granule spans a full ~93 min orbit;
the domain crossing is a ~30 s moment that can sit anywhere inside it. In a verified case
the midpoint was **13.5 minutes** off.

**`time` is indexed along-track only.** `lat`/`lon` are `(cross_track, along_track)`, so
`np.unravel_index(np.nanargmin(dist), dist.shape)` returns `(i_cross, j_along)` and the
crossing time is `time[j_along]`. Using `time[i_cross]` gave a **33-minute** error that
looked plausible because it fell inside the granule window. `dpr_domain_crossing` guards
this.

Keep granule filenames at their canonical long form — gpm-api parses product metadata
from the filename and raises on a shortened name.

## Step 3: fetch only the coincident radar scans

```python
files = armlive_query(user, token, datastream, t0, t1)
ppis  = select_scans_by_size(user, token, files, min_bytes=20_000_000)
```

**Size the files before downloading them.** ARM datastreams can interleave scan types
with no scan-type token in the filename. One C-band datastream alternates ~200 MB PPI
volumes with ~3 MB RHIs on a ~16 min cycle; an unfiltered fetch pulls both.
`armlive_file_size` uses HTTP HEAD, so classification transfers no data.

**Bracket width.** A ±30 min bracket at a ~16 min volume cadence gives about five
volumes — two either side of the crossing. That matters because **time matching is
typically the limiting systematic** in single-overpass SR-GR: in one analysis, shifting
from the 1.9-min-offset volume to the ±8 min neighbours moved the derived offset by
1.5 dB. Without neighbouring volumes you cannot quantify that term. ±15 min is enough
only if you accept an unconstrained time-matching error.

**PPIs, not RHIs, for SR-GR.** An RHI is a single vertical plane and yields almost no
matched volumes against a 5 km footprint swath. RHIs are valuable separately: one C-band
RHI scanned the vertical plane along the radar-disdrometer baseline reaching 89.8°
elevation, with 32 rays above 85° — a genuine birdbath for ZDR calibration, at 3 MB per
file instead of 200 MB.

Fetch with ACT (`act.discovery.download_arm_data`) so the citation text is surfaced.

**A short file may be a complete RHI, not a torn PPI.** Sizes are datastream-specific:
one C-band stream's RHIs are ~3 MB against ~200 MB PPIs, another's are **17.5 MB against
690 MB**. A 17.5 MB download there is a *valid, complete* RHI — HDF5 magic bytes intact,
`Content-Length` matched, 347 rays in a single sweep. Classify by HEAD size against that
stream's own two modes; a bare size floor reports complete RHIs as failed downloads and
sends you chasing a non-existent transfer bug.

**Verify completeness against `Content-Length`, not a size floor.** A dropped connection
makes `read()` return EOF rather than raising, so a truncated body looks like a clean
finish. This silently produced 412 MB and 323 MB fragments of 719 MB volumes that passed
a 100 MB floor, carried valid HDF5 magic bytes, and only failed hours later at
`Dataset(path)` with `NetCDF: HDF error`. Compare bytes written against the header and
delete-and-retry on mismatch:

```python
with urllib.request.urlopen(url, timeout=1800) as r, open(tmp, "wb") as fh:
    expect = int(r.headers.get("Content-Length", 0))
    while (chunk := r.read(1 << 20)):
        fh.write(chunk)
if expect and os.path.getsize(tmp) != expect:
    os.remove(tmp)          # truncated — retry
else:
    os.replace(tmp, path)   # only now is it visible to restart logic
```

Write to a `.part` name and `os.replace` only on success, so a kill mid-transfer cannot
leave a file that restart-safe logic mistakes for complete. This check caught a real
575-of-721 MB truncation on its first live use.

**Gate on readability before analysis.** After a fetch pass, open every volume and
quarantine what fails — otherwise a corrupt file is silently skipped by the matcher and
you under-count the sample without noticing.

**Expect the service to degrade rather than fail cleanly.** Observed throughput on one
archive ranged 3.4 down to 0.28 MB/s, with `IncompleteRead` and 502s under load, then a
period where the listing endpoint returned HTTP 500 after a fixed 30 s for every query —
including one with deliberately invalid credentials, which should have failed auth
instantly. That pattern (instant 400 on a malformed query, 30 s 500 on a valid one) means
the archive lookup behind the endpoint is timing out; it is not your credentials and not
your network. Supervise long passes with a retry loop that sleeps between passes, and
make each pass restart-safe so waiting out an outage costs nothing.

**Survey the bracket before setting a fetch target.** Count PPIs per bracket by HEAD
first. One overpass with the most precipitating footprints in the whole set had exactly
**one** PPI in its bracket — already held — so it could not be improved by fetching at
all, while a supervisor loop with aspirational targets would have retried it all night.

## Step 4: the SR-GR comparison

**Call `gpm.gv.volume_matching` rather than assembling the geometry yourself.** It does
the parallax correction, beam-volume intersection, linear-power aggregation and Ku->C
conversion described below, and returns the very screening columns this section tells
you to use. Hand-rolling it is how the melting-level filter ended up inverted (keeping
ice, not rain) and returned a confident, wrong -8.5 dB.

```python
dtree = pyart.io.read_cfradial(gr_file).to_xradar()
ds_gr = dtree["sweep_0"].to_dataset().rename({"uncorrected_reflectivity_h": "DBZH"})
df = gv.volume_matching(ds_gr=ds_gr, ds_sr=gpm.open_granule_dataset(g, scan_mode="FS"),
                        radar_band="C", z_variable_gr="DBZH", beamwidth_gr=1.0,
                        max_gr_range=113_000, download_sr=False)
gv.calibration_summary(df, gr_z_column="GR_Z_mean",
                       sr_z_column="SR_zFactorFinal_Ku_mean")
```

The material below explains *why* each screen exists — worth reading before you relax
one. The gpm-api vocabulary for working with profiles directly:

```python
gpm.slice_range_at_bin(bins="binClutterFreeBottom")   # per-ray clutter masking
gpm.get_height_at_bin("binClutterFreeBottom")         # and binRealSurface
gpm.slice_range_at_temperature(temperature=275.15)    # melting-layer control
gpm.retrieve("flagPrecipitationType", method="major_rain_type")
```

**Mask to bins above `binClutterFreeBottom` per ray.** This is not optional and not a
fixed height cut — the boundary varies with local zenith angle across the swath (spanning
1165-2379 m MSL in one case). Measured effect: enabling it halved the matched sample and
shifted the derived offset by **1.43 dB**, comparable to half the total uncertainty.

The notebook's `filter_matched_volumes` screens on more than clutter, and these are worth
copying rather than reinventing: `SR_dataQuality == 0`, `SR_qualityFlag == 0`
(1 = low quality, 2 = bad/missing), `SR_qualityTypePrecip == 1`,
`SR_fraction_no_precip` below ~0.1, `SR_fraction_clutter` below ~0.05, plus the
`GR_Z_fraction_above_<thr>dBZ` / `SR_zFactorFinal_Ku_fraction_above_<thr>dBZ` pairs for
beam-filling control. It also flags that `SR_reliabFlag` carried buggy values for its
event, so treat that one with suspicion.

Restrict to **stratiform above the melting layer** and to volume-averaged reflectivity in
**24-36 dBZ** (Warren et al. 2018), which simultaneously limits low SR sensitivity, SR
beam attenuation and non-Rayleigh scattering. Convective footprints are excluded because
of non-uniform beam filling, SR attenuation-correction bias, C/X-band beam attenuation,
and hail multiple scattering. (The notebook's own function defaults to a looser
`(18, 36)` than the 24-36 its text recommends — choose deliberately.)

**Frequency conversion is not always the dominant systematic.** Ku (13.6 GHz) versus
C-band differs systematically in rain, but confined below 36 dBZ the correction can be
small — Mie integration over local disdrometer DSDs gave only +0.09 dB below 30 dBZ,
rising to -2.8 dB above 40 dBZ. Derive it from local DSDs where possible and validate
against multi-band disdrometer reflectivity; the conventional wisdom that it dominates
is a consequence of including high reflectivities.

Also correct **parallax**: a DPR bin at height z is displaced z·tan(localZenithAngle)
toward nadir, which can be comparable to the footprint radius. Iterate, since the ground
beam height depends on the corrected ground range.

**The two terms that actually dominated, once the geometry was right.**

*Beam filling.* `GR_fraction_covered_area > 0.7` was the single largest source of
spurious offset — low-fill matches are mostly no-signal gates compared against a
footprint the satellite called precipitating. It moved the offset several dB and lifted
correlation substantially.

*Time offset.* Measured directly within one storm, the per-volume median marched onto the
true value as |dt| shrank: **+3.2 dB at -26 min, -0.7 at -10, -5.3 at -1.9 min.** Cut at
~12 min. Distant volumes dilute the offset toward zero and flatten the intensity slope —
regression dilution, not physics. Derive dt from the *volume filename*, since a matcher's
time column may hold the satellite footprint time (identical for every ground volume
matched to one crossing) and subtracting the crossing from it gives ~0 for everything.

**Test for range dependence before quoting a constant.** With enough matches the
difference here rose with ground range at +0.057 dB/km, so no single number described the
radar. A range cut chosen after seeing the trend is post-hoc and will look like it works
until the sample grows. Verify against an orbit that was not part of the data that
motivated the cut.

## Honesty about one overpass

A single 30 s crossing with a few dozen matched volumes cannot establish an absolute
calibration. Report the offset with a real uncertainty budget and state the bound rather
than issuing a correction constant. If the screen finds only one or two qualifying passes
in the record, that result — the site needs a longer archive — is the finding worth
reporting.

## Practical notes

Both passes are restart-safe by construction: append one row per granule and skip orbits
already present; skip radar files already on disk. Detach long passes with
`nohup python script.py > log 2>&1 &` (`setsid` does not exist on macOS) and poll the
output count. Filter macOS `._` AppleDouble files from every listing or counts will be
wrong. A partially-downloaded granule raises an HDF/NetCDF error from gpm-api — check
size before treating it as corrupt.
