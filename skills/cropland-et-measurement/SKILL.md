---
name: cropland-et-measurement
description: "Measuring and interpreting evapotranspiration and surface energy fluxes over managed croplands, with Corn Belt maize and soybean numbers. Covers eddy-covariance corrections, the energy-balance closure gap and its four residual conventions, flux footprints and the tower-to-pixel bias, Bowen-ratio and lysimeter alternatives, ONEFlux and REddyProc processing, E/T partitioning, measured Midwest ET and Bowen-ratio magnitudes, ARM ECOR/EBBR/QCECOR failure modes, and the flux partition that drives convective initiation. Load before quoting a cropland LE or ET number, calibrating a satellite ET product against towers, or siting a flux tower over row crops. Triggers - evapotranspiration, ET, latent heat flux, eddy covariance, energy balance closure, Bowen ratio, flux footprint, Kljun FFP, ECOR, EBBR, QCECOR, AmeriFlux, FLUXNET, lysimeter, scintillometer, WPL correction, REddyProc, transpiration partitioning, crop coefficient, corn, soybean, maize, Corn Belt, land-atmosphere coupling."
---

# Cropland ET measurement and interpretation

Evapotranspiration over row crops is measured well enough that the dominant error is
usually bookkeeping, not instrumentation. Three declarations decide whether a number
means anything, and most published disagreement traces to one of them being unstated.

## The three-question gate

Before quoting or comparing any cropland LE or ET value, establish:

1. **The closure convention** applied to the residual (four choices below, spanning up
   to 50 % in daily ET).
2. **The footprint** that produced it, and the surface composition of that footprint.
3. **Whether it is an energy flux or a water flux**, and over what integration period.

A source that states none of the three carries a floating 20-50 % offset. Say so rather
than propagating it.

## Closure: the numbers

Energy balance ratio EBR = (H + LE) / (Rn - G). Over cropland this is *not* one.

| Quantity | Value | Source |
|---|---|---|
| Mean cropland EBR, 6 sites, 48 site-years | **0.75**, residual 41.6 W m-2, annual range 0.62-0.90 | [10.5194/bg-16-521-2019](https://doi.org/10.5194/bg-16-521-2019) |
| Two cropland sites, same crops | 82 % vs 67 % closure - site effect > crop type > phenological stage | [10.1016/j.agrformet.2021.108529](https://doi.org/10.1016/j.agrformet.2021.108529) |
| Best-instrumented field experiment (EBEX-2000) | ~10 % imbalance *after* full correction | [10.1007/s10546-020-00529-6](https://doi.org/10.1007/s10546-020-00529-6) |
| Effect of residual-treatment choice on daily ET | up to **50 %**; seasonally about a third of applied irrigation | [10.1007/s00271-022-00783-1](https://doi.org/10.1007/s00271-022-00783-1) |
| Closure-corrected EC vs weighing lysimeters | 3.8 % (19 mm) annually, < 8 % monthly in summer | [10.5194/hess-19-2145-2015](https://doi.org/10.5194/hess-19-2145-2015) |

Site had a statistically significant effect on closure; **crop type and region did not**.
So the gap is a property of the field and its surroundings: measure it at each site,
never transfer it from the literature. Working prior for a new Corn Belt tower: EBR
0.70-0.85, midday residual 30-60 W m-2.

### The four conventions

`closure_variants(H, LE, Rn, G)` returns all four for a given half-hour.

1. **No forcing.** Preserves the measurement; guaranteed biased low against any
   energy-conserving model.
2. **Bowen-ratio-preserving** - scale H and LE by the same factor
   ([Twine et al. 2000](https://doi.org/10.1016/s0168-1923%2800%2900123-4)). Evidence
   favours it for beta < 1 (closed mid-season canopy). Overestimates ET against lysimeters
   ([10.1002/hyp.11397](https://doi.org/10.1002/hyp.11397)).
3. **Buoyancy-flux-based** - assign the residual mostly to H
   ([Charuchittipan et al. 2014](https://doi.org/10.1007/s10546-014-9922-6)). Physically
   motivated: the unmeasured secondary-circulation transport is mainly sensible heat.
   Favoured for beta > 1 (bare soil, post-harvest, senescence). Underestimates ET against
   lysimeters.
4. **Residual-LE** - everything to LE. What remote-sensing energy-balance models
   effectively do, and it usually overestimates ET. Use to *emulate* a satellite
   product, never as a measurement.

A Corn Belt maize season crosses beta = 1 twice, so no single convention is right for the
whole year, and you cannot let the data choose: with extra independent measurements, up
to four of five closure scenarios performed similarly and all five were plausible in up
to 53 % of cases ([10.1016/j.agrformet.2012.10.006](https://doi.org/10.1016/j.agrformet.2012.10.006)).
Correct practice: archive uncorrected H and LE, the measured residual, and at least two
corrected variants; state which one a comparison used; apply correction on daily rather
than half-hourly factors.

### Why it does not close

Secondary circulations and boundary-layer eddies organised on scales longer than the
averaging interval ([10.1890/06-0922.1](https://doi.org/10.1890/06-0922.1),
[10.1175/jamc-d-14-0140.1](https://doi.org/10.1175/jamc-d-14-0140.1)); the imbalance
ratio scales with u-star and, for LE, with the Bowen ratio
([10.1371/journal.pone.0209022](https://doi.org/10.1371/journal.pone.0209022)). Soil heat
flux error dominates in dry, strongly heated surface layers
([10.1016/j.agrformet.2003.09.005](https://doi.org/10.1016/j.agrformet.2003.09.005)); over
annual crops G reaches 30 % of Rn when vegetation is low, so early-season and
post-harvest periods are where G errors propagate hardest. This is a **scale** problem,
not a calibration problem - it dictates siting, not post-processing.

Counter-intuitive and load-bearing: over maize the footprint *contracts* as the canopy
grows (the effective height above the displacement plane shrinks) and closure *improves*
through the season ([10.5194/bg-16-521-2019](https://doi.org/10.5194/bg-16-521-2019)).

## Footprints and the tower-to-pixel bias

Use the Kljun et al. 2015 FFP parameterisation
([10.5194/gmd-8-3695-2015](https://doi.org/10.5194/gmd-8-3695-2015)) - extent, crosswind
width and shape from u-star, sigma_v, Obukhov length, boundary-layer height, z0 and z-d;
both per-interval and climatology modes; author-distributed Python and R. Alternatives:
[Kormann & Meixner 2001](https://doi.org/10.1023/a:1018991015119),
[Hsieh et al. 2000](https://doi.org/10.1016/s0309-1708%2899%2900042-1),
[Horst & Weil 1992](https://doi.org/10.1007/bf00119817), and the backward-Lagrangian
LPDM-B ([10.1023/a:1014556300021](https://doi.org/10.1023/a:1014556300021)) when the full
boundary layer matters.

Over crops, `footprint_geometry(canopy_height_m, meas_height_m)` gives d = 0.67 h,
z0 ~ 0.1 h and the ARM fetch rules. **Update canopy height at least biweekly** - a fixed
displacement height is wrong by a factor of ~2 between bare soil and tasselling maize -
or infer aerodynamic canopy height continuously from the momentum flux
([10.1029/2018gl079306](https://doi.org/10.1029/2018gl079306)). Restrict footprint
computation to u-star > 0.1 m s-1 and zeta >= -15.5.

Scale magnitudes: monthly 80 % footprint climatologies span **1e3 to 1e7 m2** across 214
AmeriFlux sites. ARM's ECOR siting rule is 1:70 height-to-fetch (210 m at 3 m), EBBR's is
1:40 (120 m). A 2390 m scintillometer path samples ~2000 x 700 m where co-located EC
source areas lay within a 250 m radius
([10.5194/hess-15-1291-2011](https://doi.org/10.5194/hess-15-1291-2011)).

**The number to remember when calibrating a satellite product:** comparing tower flux
against a fixed-radius target area of 250-3000 m injects **4-20 % bias in vegetation
index and 6-20 % in dominant land-cover fraction**
([10.1016/j.agrformet.2021.108350](https://doi.org/10.1016/j.agrformet.2021.108350)). Over
a corn/soy mosaic this is not noise - it correlates with phenology, because the two crops
differ in greenness and Bowen ratio on the same date. Use footprint-weighted comparison,
as the OpenET benchmark did with static and dynamic hourly footprints per station
([10.1016/j.agrformet.2023.109307](https://doi.org/10.1016/j.agrformet.2023.109307)).

## Processing chain

High-frequency: EddyPro or the codes benchmarked in
[10.5194/bg-5-451-2008](https://doi.org/10.5194/bg-5-451-2008); follow the ICOS raw
specification ([10.1515/intag-2017-0043](https://doi.org/10.1515/intag-2017-0043)) to
remove processing degrees of freedom. Order: despike -> coordinate rotation (double
rotation or planar fit, [10.1023/a:1018966204465](https://doi.org/10.1023/a:1018966204465))
-> detrending or block averaging -> spectral/frequency response (incl. tube attenuation for
closed path) -> WPL density correction
([10.1002/qj.49710644707](https://doi.org/10.1002/qj.49710644707)) -> storage -> quality
flags. Expected effect of the whole chain, from ARM's own product: **LE +10-30 %, H ~+10 %**
([10.2172/1557426](https://doi.org/10.2172/1557426)).

Post-processing: ONEFlux
([10.1038/s41597-020-0534-3](https://doi.org/10.1038/s41597-020-0534-3)) is the reference
pipeline; REddyProc
([10.5194/bg-15-5015-2018](https://doi.org/10.5194/bg-15-5015-2018)) is the practical
open-source implementation for u-star threshold estimation, MDS gap-filling, partitioning
and uncertainty. u-star filtering is the largest single systematic term
([10.5194/bg-3-571-2006](https://doi.org/10.5194/bg-3-571-2006)).

**Cropland trap.** MDS borrows across a harvest step change because its time window
widens; u-star change-point detection reads canopy removal as a turbulence regime change;
annual windows blend maize and soybean years at rotation sites. **Process by phenological
period, never by calendar year, and never gap-fill across a harvest.**

## Partitioning ET into T and E

Do not trust a single method. Three carbon-water coupling methods over 251 FLUXNET sites
correlated at R 0.89-0.94 with each other yet gave **T/ET from 45 % to 77 %**
([10.1111/gcb.15314](https://doi.org/10.1111/gcb.15314)); spatial variability is 1.6x the
interannual and is driven by vegetation and soil, not climate. The assumption that ET is
approximately T under ideal transpiring conditions is ecosystem-dependent
([10.5194/bg-16-3747-2019](https://doi.org/10.5194/bg-16-3747-2019)). Independent
references: sap flow, isotopes over a C3/C4 managed system
([10.1016/j.agrformet.2005.06.005](https://doi.org/10.1016/j.agrformet.2005.06.005)),
micro-lysimeters for bare-soil evaporation, and the Ritchie two-stage row-crop scheme
([10.1029/wr008i005p01204](https://doi.org/10.1029/wr008i005p01204)) still underlying crop
models.

**No defensible seasonal T/ET curve for Corn Belt maize exists in the literature.** The
qualitative picture (E dominant from planting to canopy closure, T thereafter) is secure;
the numbers are not. Flag it as an open measurement target; do not invent a curve.

## Midwest crop numbers

`et_magnitudes()` returns the bundled 86-row table
(`midwest_cropland_et_magnitudes.csv`); filter by quantity, crop or site. Highlights:

- **Maize and soybean growing-season ET are statistically indistinguishable** in the humid
  Corn Belt: 471 +/- 47 mm (continuous maize), 469 +/- 51 (maize in rotation), 453 +/- 34 mm
  (soybean), May-Sep
  ([10.1016/j.agwat.2019.02.049](https://doi.org/10.1016/j.agwat.2019.02.049)); independent
  4-year maize mean 496 +/- 21 mm
  ([10.1088/1748-9326/10/6/064015](https://doi.org/10.1088/1748-9326/10/6/064015)). Both
  crops use essentially all available profile water. The C4/C3 difference appears in
  water-use **efficiency** (~4x: maize 25-27 vs soybean ~7 kg ha-1 mm-1) and in **timing**,
  not in total water use. Do not assert that maize transpires more over a season.
- **Rotation history beats crop identity for drought resilience.** In 2012, continuous
  maize ET fell 3 %, maize in rotation fell 20 %, soybean fell to 333 mm. Corn Belt drought
  is more VPD-driven than soil-moisture-driven
  ([10.1016/j.agrformet.2020.107930](https://doi.org/10.1016/j.agrformet.2020.107930)), so
  ET holds up for weeks on stored water before falling.
- Annual ET 480-639 mm for annual/perennial crops (45-77 % of 848-1063 mm precipitation)
  ([10.1111/gcbb.12239](https://doi.org/10.1111/gcbb.12239)). Peak ET/PET at Bondville 0.76
  in the 2012 drought vs 0.91 in a wet year; daily ET < 2 mm d-1 in Apr, May, Sep, Oct.
- Green LAI: maize 0-6.5, soybean 0-5.5 m2 m-2
  ([10.2134/agronj2012.0065](https://doi.org/10.2134/agronj2012.0065)).
- Bowen ratio: warm-season agricultural FLUXNET sites sit at **0.25-0.50**, the low end of
  the network. G = 30 % of Rn when vegetation is low; LE > 42 % of Rn in wet active-canopy
  seasons.
- Management: residue added to a cover crop significantly **lowers** ET (mulch effect)
  ([10.1061/%28asce%29ir.1943-4774.0001214](https://doi.org/10.1061/%28asce%29ir.1943-4774.0001214));
  irrigation cuts the Bowen ratio by 40 %
  ([10.1029/2021gl096822](https://doi.org/10.1029/2021gl096822)) and maximises LE at ~60 %
  irrigation fraction
  ([10.1175/jhm-d-21-0160.1](https://doi.org/10.1175/jhm-d-21-0160.1)); 50 % of root mass
  sits in the top 8-20 cm across 11 temperate crops
  ([10.1016/j.fcr.2016.02.013](https://doi.org/10.1016/j.fcr.2016.02.013)).
- **Tile drainage is a first-order Corn Belt water-balance term and appears in none of the
  retrieved tower ET budgets.** Do not close a field water balance without it.

Site coordinates for the Corn Belt flux network (US-Ne1/2/3, US-Bo1, US-Br1/3, US-IB1,
US-Ro1/2/3) are in the bundled table. **Provisional**: the two dedicated Mead ET papers
([10.1016/j.agrformet.2008.09.010](https://doi.org/10.1016/j.agrformet.2008.09.010),
[10.1016/j.agrformet.2010.01.020](https://doi.org/10.1016/j.agrformet.2010.01.020)) are
paywalled with no retrievable abstract, so irrigated-maize ET totals here come from
rain-fed Michigan and Illinois sites instead; read the PDFs before quoting Mead numbers.

## Units

With FAO-56 lambda = 2.45 MJ kg-1: **1 mm d-1 = 28.4 W m-2**; 1 W m-2 = 0.0353 mm d-1. The
temperature dependence is weak (28.95 at 0 C, 28.12 at 30 C), so a constant 28.4 is good
to ~2 % across a growing season. `et_units(value, "W/m2", "mm/day")` handles the
conversions. Two recurring errors: treating a midday LE as a daily mean (a 300 W m-2 peak
is **not** 10.6 mm d-1), and comparing closure-corrected ET in mm against uncorrected LE in
W m-2 without saying so, which silently inserts the 20-30 % residual.

## Cropland non-stationarity

Phenology is set by a farmer's planting date, so the phase of the seasonal cycle is a
management variable differing by weeks between adjacent fields. Harvest is a one-day step
change in roughness, albedo, LAI and surface conductance that abruptly shifts the
relationship between evaporative fraction and surface state
([10.1002/2017jd026740](https://doi.org/10.1002/2017jd026740)). Rotation means the same
tower reports maize physiology one year and soybean the next. At ARM SGP, land cover was
the dominant source of flux variation, with 50-100 % differences between
winter-spring-planted and summer-planted fields
([10.1175/ei231.1](https://doi.org/10.1175/ei231.1)). Methods tuned on natural ecosystems
assume none of this.

## Boundary layer and convective initiation

For convection the quantity is the **partition**, not ET: H grows the mixed layer, LE
moistens it. Convective triggering potential and the low-level humidity index determine
whether a wet or dry surface favours triggering, and much of the continental interior lies
in a regime where the sign of the soil-moisture feedback is set by the early-morning
profile rather than by the surface
([Findell & Eltahir 2003](https://doi.org/10.1175/1525-7541%282003%29004%3C0552:ACOSML%3E2.0.CO;2)).
Score observations against the coupling-metric taxonomy of
[Santanello et al. 2018](https://doi.org/10.1175/bams-d-17-0001.1). Landscape
heterogeneity in sensible-heat flux drives mesoscale circulations
([Segal & Arritt 1992](https://doi.org/10.1175/1520-0477%281992%29073%3C1593:NMCCBS%3E2.0.CO;2))
- the same physics that produces the closure residual.

**A shallower, moister boundary layer raises CAPE and lowers the LCL while also increasing
CIN, so the net initiation effect is not signable from surface flux alone.** Simultaneous
profiling is required. For framing the Corn Belt argument: observed 20th-century central US
summer rainfall increase, temperature decrease and humidity increase are attributed mainly
to agricultural intensification with GHG forcing secondary
([10.1002/2017gl075604](https://doi.org/10.1002/2017gl075604),
[10.1175/jcli-d-19-0096.1](https://doi.org/10.1175/jcli-d-19-0096.1)).

## ARM instruments

Per-instrument detail lives in `arm-instrument-ecor`, `arm-instrument-ebbr`,
`arm-vap-qcecor`, `arm-instrument-co2flx`. What matters here:

- **ECOR** ([handbook](https://doi.org/10.2172/1467448)): 30-min H, LE, momentum, CO2 from
  sonic + open-path IRGA at 10 Hz, normally 3 m on a boom. Stated 5 % LE / 6 % H. Documented
  flux shortfall **10-25 %, occasionally 35 %, largest over tall vegetation including
  corn**. Open-path window fouls in precipitation, fog, dew and frost (CO2 corrupts before
  LE); untrustworthy below ~1 m s-1.
  **Timestamp trap: ECOR marks the beginning of the half hour, ECORSF the end, while SMOS
  and EBBR mark the end. A naive merge is off by 30 minutes.**
- **QCECOR** ([10.2172/1557426](https://doi.org/10.2172/1557426), record 2003-09-09 to
  2025-11-30, retired): applies the full correction chain then three screens - range
  (rejects night |H| or |LE| > 150 W m-2, daytime < -100 W m-2 when insolation > 300 W m-2),
  4-sigma outlier, and temporal variability over +/-3 h at 25 W m-2. **These screens are
  aggressive enough to reject a real frontal flux excursion**, so inspect uncorrected fields
  alongside corrected ones for convective-initiation work.
- **EBBR** ([handbook](https://doi.org/10.2172/1020562)): 10 % on H and LE, 1:40 fetch,
  untilled surfaces only. Near-singular as the Bowen ratio approaches -1 at sunrise and
  sunset. Soil measurements represent only the top 5 cm - **not** a root-zone constraint.
  **Closes the energy balance by construction, so it cannot diagnose closure.**
- **The transferable SGP lesson:** method differences and footprint differences are
  confounded and the footprint wins. Twelve years of ECOR and EBBR agreed when their
  fetches were over the same surface type and diverged systematically when ECOR sampled
  winter wheat while EBBR sampled grassland - enough to change the large-scale forcing in a
  constrained variational analysis
  ([10.1029/2018jd029689](https://doi.org/10.1029/2018jd029689)).

## Benchmarks for calibrating a domain product

State of the art over Corn Belt cropland, which is simultaneously the bar to beat and the
noise floor:

- Landsat-MODIS fusion ET vs 12 cropland towers, 85 site-years: daily R2 0.75, RMSE
  **0.93 mm d-1** (26 W m-2), 27.9 % relative; monthly 0.48 mm d-1, 14.3 %
  ([10.5194/hess-24-1251-2020](https://doi.org/10.5194/hess-24-1251-2020)).
- OpenET ensemble vs 152 CONUS stations: cropland MAE **15.8 mm month-1** (17 % of observed),
  MBE -5.3 mm month-1, r2 0.90
  ([10.1038/s44221-023-00181-7](https://doi.org/10.1038/s44221-023-00181-7)).

So ~25-30 % daily and ~15 % monthly is current best practice - **the same order as the
energy-balance residual in the reference data**. A calibration reporting much better than
15 % monthly agreement should be suspected of having tuned to a closure convention rather
than to ET.

## Checklist for a new cropland deployment

1. Log canopy height at least biweekly, or derive aerodynamic canopy height from momentum flux.
2. Build a wind-direction by crop-type map of the surroundings; archive per-half-hour
   footprint-weighted crop composition alongside the fluxes.
3. Archive uncorrected H and LE, the residual, and at least two closure variants.
4. Measure G with replicate plates plus a storage correction for the layer above them;
   expect G to dominate the closure term early in the season.
5. Instrument one independent ET reference (micro-lysimeter, root-zone soil water profile,
   or scintillometer path) so closure conventions can be tested rather than assumed.
6. Process by phenological period; never gap-fill across a harvest.
7. Report ET in both mm d-1 and W m-2, stating lambda and the integration period.

## Related skills

`domain-et-inference` for upscaling these measurements to a domain;
`derechos-campaign` for the DERECHOS science case; `derechos-data-sources` and
`derechos-landuse-imagery` for getting the bytes.
