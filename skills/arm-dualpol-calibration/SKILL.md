---
name: arm-dualpol-calibration
description: Calibrate reflectivity and differential reflectivity (ZDR) for ARM C-SAPR2 or similar dual-polarisation research radars. Covers clutter-based RCA relative-stability tracking, ZDR offset from light rain with PhiDP/attenuation screening, absolute Z offset against ARM LDQUANTS disdrometer data, and GPM DPR spaceborne-vs-ground (SR-GR) comparison via gpm.gv.volume_matching. Carries an acceptance test every offset estimator must pass (correlation, unit Deming slope, no intensity or range dependence) plus the selection biases that manufacture plausible wrong answers. Use for radar calibration, RCA time series, ZDR bias, engineering stability, disdrometer-radar matching, satellite overpass calibration, Earthdata/GES DISC granule download, or memory-lean passes over large CfRadial volume archives. Triggers ARM, C-SAPR2, CSAPR, RCA, relative calibration adjustment, ZDR calibration, LDQUANTS, disdrometer, GPM, DPR, Ku, SR-GR, clutter, reflectivity offset, dual-pol.
---

# ARM dual-pol radar calibration

Reflectivity and ZDR calibration for a research dual-pol radar, using four
independent methods. They answer *different* questions and it matters which you
reach for:

| Method | Gives you | Does NOT give you |
|---|---|---|
| Clutter RCA | relative stability over time | any absolute offset |
| Light-rain ZDR | absolute ZDR bias | reflectivity bias |
| LDQUANTS disdrometer | absolute Z offset (at the gauge) | anything away from the gauge |
| GPM DPR SR-GR | absolute Z offset (areal) | a long time series |

**RCA carries zero absolute information.** If the true Z bias is 3 dB, a
perfectly flat RCA series looks identical. Say so whenever you report one.

## One acceptance test, applied to every estimator

A receiver-gain error is multiplicative in linear power and therefore **constant in
dB**. That is a physical constraint, and it gives a test any claimed offset must pass
before you quote it:

1. **Correlation** between the two reflectivity estimates is high (>~0.8). Low
   correlation means you are comparing different volumes of air, not two views of one.
2. **Deming / RMA slope consistent with 1.** A slope away from 1 is a scaling error or
   regression dilution, not a gain offset.
3. **No intensity dependence** — regress the difference on mean reflectivity; the slope
   must be indistinguishable from zero.
4. **No range dependence** — same test against ground range.

Report the verdict, not just the number. **An estimator that fails is reported as a
failure or a bound, never as a correction constant with a caveat attached.** Several
failures in this workflow returned plausible numbers that would have been believed
without this test.

**A number matching your prior expectation deserves *more* scrutiny, not less.** Two
separate broken filters here produced values close to what was expected.

**Windowing on a noisy reference manufactures a large offset from nothing.** If you
select matched pairs by thresholding the *reference* radar's reflectivity over a
population that is mostly precipitation-free, you get an Eddington bias. Simulating a
radar with a true offset of **exactly 0 dB** reproduced an apparent **-7.8 dB** this
way. The diagnostic is a null test: push a known zero offset through your whole
estimator and confirm it returns zero. If it does not, the estimator is the finding.

**Cluster your uncertainty at the right level.** Matches within one volume, and volumes
within one storm, are not independent. In one case 191 of 245 blocks came from a single
storm. Bootstrap at the volume or storm level; a match-level interval on a single-storm
sample is not an interval on the calibration.

**Method-choice spread usually exceeds statistical error.** Passing estimators spanned
2.6 dB while individual error bars were 0.4-1.4 dB. When that happens, quote the range
across methods rather than one method's interval.

Helpers auto-load into the python kernel (`read_sweep`, `signal_mask`,
`sweep_bounds`, `beam_height`, `ground_range_azimuth`, `phidp_system_offset`,
`mad_sigma`, `grid_rays_to_azimuth`, `first_valid_gate`, `dpr_overpass_time`).

## Read one sweep, never a volume

ARM C-SAPR2 PPI volumes run ~700 MB (15 sweeps, ~14k rays). A several-hundred-file
pass is only feasible by slicing one sweep's contiguous ray block: ~0.1 s and
~16 MB per sweep-field, so a full-archive pass over 731 volumes takes minutes with
flat memory.

```python
d = read_sweep(path, sweep=0,
               fields=("reflectivity", "signal_to_noise_ratio_copolar_h",
                       "normalized_coherent_power"))
```

Structure long passes as: one disk pass extracting the *widest* candidate set you
might need into a small per-volume `.npz`, then derive every statistic, sub-mask and
sensitivity test in memory from those. Re-reading 500 GB to try a second threshold
is the mistake to avoid.

## Seven traps that will silently corrupt results

**1. UTC-midnight file splits.** ARM splits volumes at 00:00 UTC. The resulting
files keep a full-volume `sweep_start/end_ray_index` template while containing a
fraction of the rays, so slicing "sweep 0" by declared index returns a *high
elevation* beam. This presented as a 45-70 dB "reduced-power startup state" every
day until the geometry was audited. `read_sweep` raises on it by default; audit an
archive with `sweep_bounds` and compare `n_rays_actual` against the declared count.

**2. Unthresholded fields contain garbage, not fills.** `uncorrected_reflectivity_h`
and friends return values at gates with no signal — recognisable by Doppler pegged
at the Nyquist, spectral width saturated, and NCP ~ 0. Unscreened, they present as
50-60 dBZ of noise. Always `signal_mask(snr, ncp)` first.

**3. Corrected vs uncorrected is a real choice.** ARM's processed `reflectivity`
suppresses ground clutter by roughly 12 dB relative to the uncorrected field. Use
**uncorrected for clutter/RCA** and **corrected for precipitation**. Check whether
`unthresholded_power_copolar_h` is populated before relying on it — in some streams
it is entirely NaN.

**4. Near-range blanking.** T/R blanking can void the first ~2 km. Find it with
`first_valid_gate` rather than assuming; a clutter ring starting inside it reads all
NaN. An on-site disdrometer at range 0 is unusable for gate matching for this reason.

**5. PhiDP has a per-volume system offset, and it can WRAP.** It drifts volume to
volume and across months — a single site spanned -9 to +38 deg — so never reuse one
period's value as a constant. Solve it per volume with `phidp_system_offset` before
applying any absolute PhiDP threshold. Critically, when the offset sits just below
zero the field is bimodal at 0/360 and a **plain median returns ~352 deg**, which is
meaningless and silently corrupts every downstream threshold. Use a circular mean
(`phidp_system_offset` does); diagnose by histogramming PhiDP over clean rain gates
and looking for mass piled at both ends.

**6. Scan strategy can change between deployments.** Range coverage is not a site
constant: the same radar ran 496 gates x 117 m (58 km) in one month and 1050 x 108 m
(113 km) the next, trading range for azimuth sampling (20.9k vs 13.7k rays). File
size alone identifies which (270 vs 710 MB). This decides case usefulness — an
overpass with 585 precipitating footprints yielded only ~96 matchable ones because
the radar reached just 58 km that day. Check `range[-1]` against your target
geometry before ranking cases. **More footprints is not a better case.**

**7. Receiver gain does not survive a redeployment — never pool across epochs.**
Long downtimes split the record into epochs that do not share a calibration. At one
site the measured offset was about -2.5 dB in one campaign and -8 dB after the next
return to service, and roughly 1.9 dB of that step was a *processing-constant*
change rather than hardware. Epochs also differ in processor version, range-gate
geometry, ray count and even field names, while sharing identical site coordinates —
so overlap geometry carries over but gain must not be assumed to. Pooling hides
exactly the thing worth measuring. A useful control: a 210-day gap with no return to
service changed calibration by +0.001 dB (p=0.68) — **downtime alone does not
recalibrate a radar; a return to service can.** Check `process_version`, `range[-1]`
and the field list before treating two periods as one dataset.

## Clutter RCA

Build a persistent-clutter mask empirically; do not impose a range/height box. A
research radar's lowest sweep is often 1.5 deg rather than the 0.5 deg the classic
RCA literature assumes, so the clutter fan is thinner and terrain-dependent.

Selection that worked: occurrence frequency > 0.95 across clear-air volumes, beyond
the blanking and inside ~20 km, and a strong-return floor (`zmean > 40 dBZ`). Tune
the floor by *minimising diurnal sensitivity*, not by eye — biological scatterers
have a strong diurnal cycle and a low floor lets them in.

**Two scatterer populations coexist at strong near-range gates** and must not be
conflated: stationary ground clutter (velocity exactly 0, spectral width saturated,
NCP ~ 0, SNR ~ 55 dB) versus biota (velocity a few m/s, narrow spectral width,
coherent, diurnal cycle peaking late afternoon).

Prefer the **mean of the top-N strongest gates** over a percentile. In our test it
was mask-invariant (identical RCA across 122/260/374-gate masks) where p95 moved
0.2 dB, and it carried the smallest rain bias. Screen precipitation *over the
clutter fan specifically*, not just the far field.

Interpretation discipline: check the drift slope with day-level resampling. Adjacent
volumes are strongly autocorrelated (lag-1 ~ 0.5), so an OLS CI on hundreds of
volumes is far too tight — a nominally significant +0.1 dB/day slope had a
day-cluster CI spanning zero. Also compare disjoint azimuth sectors: low pairwise
correlation means clutter speckle, not gain, dominates the per-sector scatter.

## ZDR from light rain

In light rain intrinsic ZDR is small and tightly constrained (~0.1-0.3 dB), so the
departure is instrumental. Screen hard: corrected Z 15-30 dBZ, rho_HV > 0.98, SNR on
both channels > 15 dB, NCP > 0.5, modest spectral width, PhiDP near its per-volume
system offset, small along-ray dPhiDP/dr (differential attenuation), and beam height
below the melting level from the nearest sounding.

Prefer the **uncorrected** ZDR field. ARM's applied correction is close to a no-op
in the median but widens the distribution.

**Elevation and height are degenerate — a high-elevation sweep is NOT a birdbath
proxy.** A 15-sweep strategy reaching 42 deg looks like a free quasi-vertical
estimator. It is not: the observed ZDR drop from 1.5 to 42 deg was ~6x larger than
raindrop oblateness permits, because elevation and sampling height covary. Binning by
height showed the ZDR-vs-elevation slope vanishes at fixed height while ZDR falls
with height. Fitting a bias to the raw elevation curve yields a spurious -0.4 dB
offset. Control for height, or don't use the elevation signal.

Report systematic terms separately. With ~10^5 gates the statistical error is under
0.01 dB and irrelevant; day-to-day scatter, across-method spread, and the DSD
expectation (~0.1 dB, irreducible) dominate.

## Absolute Z against LDQUANTS

`bnfldquantsM1.c1`-style files give DSD-derived reflectivity per band at 1-min
resolution — use the field matching the radar's band (`reflectivity_factor_cband20c`
for C-band), plus `differential_reflectivity_cband20c`, `specific_attenuation_*`,
`rain_rate`, `med_diameter`, `lwc`. Stage with ACT
(`act.discovery.download_arm_data`).

**Beam height above the gauge is the dominant error term, not calibration.** A
disdrometer tens of km out sits ~1 km below the lowest beam centre, with a beam
several hundred metres deep. Signatures that the gradient is dominating: a
rain-rate-dependent offset, and a large measured vertical reflectivity gradient.
When you see those, the honest output is a bound plus the gradient, not an offset.
Check the matched-sample size early — a dry week can leave only a handful of usable
minutes, and that number governs everything downstream.

## GPM DPR SR-GR

Screen for overpasses with **NASA CMR**, not TLE propagation. A TLE more than a few
days from the target date is useless here: at ~7.3 km/s a 60 s propagation error
displaces the ground track ~440 km. Query CMR by `short_name` and `point` at the
radar coordinates; it returns the granules that actually intersect.

```python
info = dpr_overpass_time(ds["lat"].values, ds["lon"].values, ds["time"].values,
                         radar_lat, radar_lon)
```

**Indexing trap:** DPR `lat`/`lon` are `(cross_track, along_track)` while `time` is
indexed by along-track ONLY. `np.unravel_index(argmin(dist))` returns
`(i_cross, j_along)`, so the overpass time is `time[j]`. Using `time[i]` gave a
33-minute error that looked plausible because it fell inside the granule's 93-minute
window. `dpr_overpass_time` handles this.

### Do not hand-roll the match — gpm-api already implements it

`gpm.gv.volume_matching` performs the whole Schwaller & Morris geometry: parallax
correction, beam-volume intersection, aggregation in **linear** power, and Ku->C
band conversion. It returns the diagnostic columns you need to screen on. A
hand-rolled version of this produced the single worst error in this workflow (see
the bin-ordering trap below).

```python
dtree = pyart.io.read_cfradial(gr_file).to_xradar()
ds_gr = dtree["sweep_0"].to_dataset().rename({"uncorrected_reflectivity_h": "DBZH"})
df = gv.volume_matching(ds_gr=ds_gr, ds_sr=gpm.open_granule_dataset(granule, scan_mode="FS"),
                        radar_band="C", z_variable_gr="DBZH", beamwidth_gr=1.0,
                        max_gr_range=113_000, download_sr=False)
```

Screen on the returned columns rather than inventing thresholds:
`GR_fraction_covered_area > 0.7`, and `SR_fraction_no_precip`, `SR_fraction_clutter`,
`SR_fraction_melting_layer`, `SR_fraction_hail` all below ~0.1. Also available and
worth using: `SR_dataQuality == 0`, `SR_qualityFlag == 0`,
`SR_qualityTypePrecip == 1`. Treat `SR_reliabFlag` with suspicion — it has carried
bad values. `gv.calibration_summary` draws the diagnostic figure in one call.

**Bin ordering (the expensive one).** DPR range bins run **top-down**: bin 0 is
~21.9 km altitude and the last bin is the surface. So slicing "up to
`binClutterFreeBottom`" spans the *whole column*, and a filter written as "above the
melting level" keeps **ice**, not rain. Written that way it sampled ice at 6.7 km and
returned a confident, entirely wrong -8.5 dB. The rain window is *below* the freezing
level with a bright-band margin. gpm-api's `slice_range_at_height`,
`slice_range_at_temperature` and `get_height_at_bin` avoid the whole class of error —
use them instead of index arithmetic.

Still your decisions: `zFactorFinal` (attenuation-corrected) vs `zFactorMeasured`, and
whether the Ku->C conversion the library applies suits your DSD assumptions. The
frequency difference (13.6 vs 5.6 GHz, non-Rayleigh in rain) remains a leading
systematic.

### Beam filling and time offset dominate the error budget

**Fill fraction is the largest single source of spurious offset.** Low-fill matches
are mostly no-signal gates being compared against a footprint the satellite called
precipitating. Adding a 0.7 floor moved the offset by several dB and lifted
correlation substantially. It is not an optional refinement.

**Time offset decorrelates fast, and this is measurable rather than assumed.** Within
one storm the per-volume median marched monotonically onto the true value as |dt|
shrank: +3.2 dB at -26 min, -0.7 at -10, **-5.3 at -1.9 min**. Pair each ground volume
with the crossing time and cut at ~12 min; distant volumes dilute the offset toward
zero and flatten the apparent intensity slope (regression dilution, not physics).

**Derive dt from the volume filename.** A matcher's `gr_time` column may hold the
*satellite* footprint time, identical across every ground volume matched to one
crossing; subtracting the crossing from it yields ~0 for everything and silently
destroys the analysis.

### Check for range dependence before quoting a constant

An offset is only a constant if it *is* constant. In a 286-match, 9-volume, 4-orbit
sample the difference rose with ground range at **+0.057 dB/km** (95% CI +0.043 to
+0.083, volume-cluster bootstrap) — about -6.6 dB near 40 km and -3 dB beyond 80 km.
The pooled median silently averages over that.

Two cautions from getting this wrong twice. A `<=90 km` cut chosen *after* seeing the
trend is post-hoc and looked like it worked only because the smaller sample lacked
power; with more data the same subset failed too. And the trend is **not**
between-orbit confounding — orbit fixed effects left the slope unchanged (+0.056,
p=0.0002), and an orbit that was not part of the data motivating the cut reproduced it
independently (+0.051, p=0.003). Note the **sign**: positive means the deficit shrinks
with range, the opposite of path attenuation, so attenuation is excluded by direction
alone. Beam broadening was also excluded (the GR/SR standard-deviation ratio does not
fall with range) and melting-layer contamination was ruled out (0% of matches above the
melting level). **The cause is unresolved** — treat a range-resolved offset as the
honest output and say the mechanism is unknown.

One overpass is one overpass. Report per-overpass offsets alongside the pooled value;
if they disagree by more than the quoted uncertainty, the pooling is the problem.

### Earthdata download

GES DISC needs three gates cleared, in order:

1. Allowlist `cmr.earthdata.nasa.gov`, `data.gesdisc.earthdata.nasa.gov`,
   `urs.earthdata.nasa.gov`.
2. Accept the data EULA once. Before that the server returns HTTP 403 with a JSON
   body naming `EULA Acceptance Failure` and a `resolution_url` — read the body,
   since the status alone looks like an auth failure.
3. Allowlist the signed CloudFront host in the redirect, which serves the bytes.

Use `curl -H "Authorization: Bearer $TOKEN" -L -b cookies -c cookies`. Plain
`urllib` re-sends the Authorization header to the redirect target and gets 403.
Read the token from the credential store at runtime; never write it to disk or into
a notebook. A successful auth is visible as `A-userid=` in the redirect URL.

`gpm-api` parses product metadata from the **filename**, so keep granules at their
canonical long names. It defaults to `storage='PPS'` (FTPS, separate registration),
which bypasses the GES DISC EULA path entirely.

## Reporting

State the sample size for every number. Give robust statistics (median, MAD-sigma)
next to mean/std — these distributions have outliers. Separate statistical from
systematic uncertainty and name which dominates. Where two independent methods
overlap, their agreement (or disagreement) is the actual evidence; report it rather
than averaging them into a single number.

Write per-file results incrementally and skip work whose output exists, so an
interrupted pass resumes. On macOS `setsid` is unavailable — detach long passes with
`nohup python script.py > log 2>&1 &` and poll the output count.
