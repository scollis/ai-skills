---
name: derechos-iop-scorecard
description: Executable DERECHOS IOP science scorecard - turns a gridded forecast over the Ames IA to Chicago IL domain into per-science-question scores (SQ1-SQ7), an IOP archetype (warm QLCS/derecho, nocturnal low-level jet MCS, hot dry boundary layer, freezing rain, winter precipitation-type transition, aerosol-perturbed convection, null) and a GO/HOLD call respecting the 10-IOP-per-year budget, sounding-crew lead time and the redeployable modules' dwell and go/no-go break. Use for DERECHOS ARM Mobile Facility IOP planning and case selection - which forecast days are worth an IOP, which science questions a day serves, whether to spend one of ten, when to relocate R1, 3-hourly M1 sounding schedules. Also covers HRRR-on-AWS byte-range subsetting (.idx, s3://noaa-hrrr-bdp-pds) and MetPy DCAPE, Derecho Composite Parameter, Bonner low-level jet and Bourgouin wet-bulb melting energy. Triggers - IOP scorecard, science scorecard, IOP call, go/no-go, IOP budget, derecho forecast, freezing rain case, case selection.
---

# DERECHOS IOP science scorecard

Section 3.3 of the white paper promises a "science scorecard" and forecast for
the conditions where enhanced observations can address SQ1-SQ7. This skill is
that scorecard, made executable: **score per science question, not per storm.**

A day that scores on SQ4/SQ5 (aerosol-perturbed convection) is a *different* IOP
from one scoring on SQ6 (damaging winds), and both differ from a cold-season
SQ2/SQ3/SQ6 freezing-rain case. The output tells you which SQs a candidate would
actually serve, then whether it is worth one of the ten IOPs you get this year.

Load the `derechos-campaign` skill for the hypotheses, full SQ text, sites and
traceability matrix. This skill only does IOP selection.

## Four layers

1. **Predictors** (40). Each is a named statistic of the forecast over the
   corridor, mapped through a configurable ramp to 0-1. Every predictor carries
   the SQ(s) it serves and the provenance of its thresholds
   (`iop_predictor_table()`).
2. **Science-question tracks.** Each SQ is scored by one or more *tracks* - the
   physically distinct situations that can serve it. SQ1 is served either by a
   convective-lifecycle day or by a hot dry-soil boundary layer; SQ2 and SQ6
   each have a warm-season and a cold-season track. Track score =
   `prod(gates) x weighted mean(predictors)`; SQ score = best track.
3. **Archetype.** A label for what kind of IOP this would be, from the summary
   statistics and the SQ vector.
4. **Decision.** Marginal campaign utility (a fresh SQ is worth more than a
   fourth repeat) compared against an opportunity-cost threshold from a
   sequential-selection dynamic program on the remaining IOP budget and days,
   plus lead-time and module-dwell feasibility.

## Quick start

```python
sfc = iop_fetch_hrrr_sfc("20200810", 0, 18)          # HRRR 00Z run, f18 valid 18Z
prs = iop_fetch_hrrr_columns("20200810", 0, 18)      # site columns, 1000-500 hPa
summ = iop_summarize(sfc, prs, valid_time="2020-08-10T18:00:00")
sc = iop_score(summ)
print(sc["archetype"], sc["sq_scores"])

dec = iop_decide(sc, n_remaining=8, days_remaining=90, log=[], lead_time_h=18)
print(iop_report(sc, dec))
```

`log` is the list of IOPs already captured this season, each `{"sq_scores": {...}}`;
it drives the diminishing-returns term.

## Helpers

| call | does |
|---|---|
| `iop_config(overrides)` | active config; `overrides` = dict or JSON path |
| `iop_dump_config(path)` | write the config out for editing |
| `iop_predictor_table()` | predictor -> SQ traceability + threshold provenance |
| `iop_fetch_hrrr_sfc(date, run, fxx, box=None)` | HRRR surface/derived fields, byte-range subset |
| `iop_fetch_hrrr_columns(date, run, fxx, sites=None)` | isobaric columns at M1/S1/NIU/NACHUSA/ATMOS |
| `iop_summarize(sfc, prs, valid_time)` | forecast -> statistics dict |
| `iop_profile_diagnostics(prs, site, psfc_pa)` | DCAPE, 0-6 km mean wind, Bonner LLJ, Bourgouin ME/RE |
| `iop_score(summary)` | per-SQ scores, tracks, archetype |
| `iop_score_window(scored_list)` | aggregate several forecast hours into one day's call |
| `iop_value(sq_scores, log)` | marginal campaign utility, normalised 0-1 |
| `iop_campaign_utility(log)` | saturating utility and per-SQ accumulated coverage |
| `iop_threshold(n_remaining, days_remaining)` | opportunity-cost threshold (DP) |
| `iop_decide(scored, n, days, log, lead_time_h)` | GO / HOLD with reasons and caveats |
| `iop_sounding_plan(valid_time, lead_time_h)` | 3-hourly M1 launch list + feasibility |
| `iop_module_relocation(daily_values, dwell_days)` | R1 go/no-go between storms |
| `iop_report(scored, decision)` | markdown scorecard |

## Input contract

`iop_summarize` takes an xarray Dataset of 2-D fields on any grid with 2-D
`lat`/`lon` coords. Names and units follow `HRRR_SFC_FIELDS`: `mlcape`, `mucape`,
`sbcape`, `mlcin`, `sbcin` (J/kg); `ushr06`/`vshr06`, `ushr01`/`vshr01`, `u10`,
`v10`, `u80`, `v80`, `gust` (m/s); `srh01`, `srh03` (m2/s2); `t2m`, `d2m` (K);
`psfc` (Pa); `pwat`, `apcp1h`, `frozr1h` (kg/m2); `hpbl`, `snod` (m); `mstav`,
`snowc`, `veg` (%); `lai` (-); `shtfl`, `lhtfl` (W/m2); `refc` (dBZ);
`csnow`/`cicep`/`cfrzr`/`crain` (0/1); `massden` (kg/m3), `colmd` (kg/m2).

Fields may be absent - HRRRv3 (before 2020-12-02) has no `veg`, `lai`,
`massden` or `colmd`, so the aerosol predictors drop out and SQ4/SQ5 are scored
on what remains. Dropped predictors are listed in
`scored["dropped_predictors"]` and echoed as a caveat by `iop_decide`; a low
SQ4 score on a HRRRv3 case means *not measured*, not *no aerosol*.

`prs` columns: variables `<SITE>_hgt|tmp|rh|ugrd|vgrd` on a `level` coordinate
in hPa (m, K, %, m/s). Without `prs` there is no DCAPE, DCP, LLJ or
melting-energy predictor, which knocks out most of SQ6 warm and SQ3.

## Thresholds

Established practice where it exists (Craven & Brooks 2004 CAPE/shear
climatology; SPC Derecho Composite Parameter after Evans & Doswell 2001; the
20 m/s 0-6 km shear organisation threshold; NWS 25.7 m/s severe-wind and
0.25 in ice-accretion criteria; Bonner 1968 criterion-1 LLJ; Bourgouin 2000 /
Birk et al. 2021 wet-bulb melting energy), our own reasoning elsewhere - each
predictor's `basis` string says which. Nothing is hard-coded: `iop_config()`
deep-merges overrides, e.g.

```python
cfg = iop_config({"predictors": {"gust": {"lo": 22, "hi": 38}},
                  "operations": {"sounding_lead_h": 36}})
```

### Calibration and validation status (measured 2026-09-02)

The scorecard has now been calibrated on a random day sample and validated against
observed MRMS precipitation in a case-control design. Summary:

- **The shipped Beta(1.2, 12) prior is ADEQUATE.** On 61 days scored at both 06Z and
  18Z with the day value taken as the maximum, KS D=0.145, p=0.14 - not rejected. An
  MLE fit gives Beta(1.61, 13.6) (mean 0.106 vs shipped 0.091), so the placeholder is
  slightly light in the mean but the right shape. Replacing it is a refinement, not a
  fix.
- **The 0.236 threshold over-selects mildly**: it picks ~14.8 IOPs per 180-day season
  against a target of 10. The threshold yielding 10 is 0.261. Raise it if you want the
  nominal budget.
- **The composite discriminates**: AUC 0.758 against observed organized convective
  swaths (39 case days vs 52 month-matched nulls). At the shipped threshold, sensitivity
  0.359 at specificity 0.981 - which selects ~15 of the ~39 swath days a season, the
  right order for a 10-IOP budget.
- **But `refc40_frac` alone beats the composite** (AUC 0.871, Youden J 0.72 vs 0.47).
  For a GO/HOLD gate on organized convection, gate on simulated-reflectivity coverage
  and use the composite to rank the days that pass. Do NOT use the composite as a
  convection detector - it is a multi-objective science-value score, and pooling in the
  SQ3/SQ4/SQ5 components (AUC 0.46/0.59/0.57 for this target) dilutes the convective
  signal.
- By SQ against warm-season organized convection: SQ6 0.79, SQ1 0.73, SQ7 0.72,
  SQ2 0.70, SQ4 0.59, SQ5 0.57, SQ3 0.46. SQ3's near-chance value means the outcome is
  wrong for it (it is a freezing-rain question), not that SQ3 scoring is broken.

**RETRACTED** (was published here on 2026-09-01): claims that the prior is "rejected,
KS p=3e-11", that the day-value distribution is "zero-inflated with 43.5 % zeros", and
that the threshold "under-selects by 2.5x". All three were artefacts of scoring only the
18Z hour; `iop_value` for a day is the maximum over hours, and a single snapshot often
catches nothing. With the day window, no day scores zero and the threshold error runs the
other way.

Still unvalidated: reliability (as opposed to discrimination), the cold-season/SQ3 gates,
SQ4/SQ5, sub-daily timing, and skill at forecast leads beyond f18. See
`scorecard_mrms_calibration.md`; `score_climatology.py` extends the sample and now works
in day units.

The `score_prior` Beta(1.2, 12) used by the budget DP is a **placeholder**,
located so the implied selection rate matches 10 IOPs per ~180-day season and so
the 10 Aug 2020 derecho is a clear GO in mid-season. Replace it with a multi-year
HRRR or ERA5 climatology of `iop_value` over the domain before the scorecard
drives real calls.

## Demonstrated on

Seven archived HRRR 00Z-run forecast hours over the corridor (6-24 h lead):

| forecast hour | scorecard result |
|---|---|
| 10 Aug 2020 06Z | `nocturnal_llj_mcs`, SQ7 = 0.58 |
| 10 Aug 2020 18Z | `warm_qlcs_derecho`, SQ1 0.68 / SQ2 0.73 / SQ6 0.62 |
| 10 Aug 2020 day window (06Z+18Z) | four SQs served, value 0.40 -> GO |
| 27 Jun 2023 18Z | `aerosol_perturbed_bl`, SQ5 = 0.39 (64 ug/m3 near-surface smoke) |
| 15 Dec 2021 18Z, 16 Dec 2021 00Z | null over the array: at 00Z the forecast 40+ dBZ line sat at 94.7-93.5 W, 100+ km west of the array box. The array-box gate working as designed - and a reminder that the right day still needs the right hours |
| 22 Feb 2023 18Z | `freezing_rain`, SQ6 = 0.81 / SQ3 = 0.51. Day identified from mPING reports (184 in-domain freezing-rain reports, top of five cold seasons) |
| 13 Oct 2022 18Z | `null`, all SQs 0.00 |

See `derechos_scorecard_methods.md` in the project artifacts for the full
predictor-to-SQ mapping, every threshold's justification, and the open design
questions a campaign lead must rule on.
