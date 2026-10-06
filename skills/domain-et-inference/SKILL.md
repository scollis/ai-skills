---
name: domain-et-inference
description: "Inferring evapotranspiration and surface turbulent fluxes over large domains from satellite, model and flux-tower data. Covers the four method families (thermal one-source SEBAL/METRIC/SSEBop, two-source TSEB/ALEXI/DisALEXI, Priestley-Taylor and Penman-Monteith satellite models including MOD16/PT-JPL/GLEAM/BESS-STAIR, and machine-learning tower upscaling such as FLUXCOM), the documented cropland error floor, the NDVI and crop-type-to-ET question and its settled answer, NDVI crop coefficients, LAI sensitivity, land-surface-model ET, OpenET, and a validation protocol. Load when building, choosing, validating or auditing a gridded ET or flux product, or designing an ET digital twin. Triggers - evapotranspiration, ET upscaling, latent heat flux, surface energy balance, SEBAL, METRIC, SEBS, SSEBop, TSEB, ALEXI, DisALEXI, PT-JPL, MOD16, GLEAM, BESS-STAIR, OpenET, ECOSTRESS, FLUXCOM, flux upscaling, NDVI, EVI, LAI, crop coefficient, Kcb, Cropland Data Layer, SIF, NIRv, NLDAS, SMAP L4, ERA5-Land, ET digital twin."
---

# Domain-wide ET and surface-flux inference

Scaling evapotranspiration from a flux tower to a domain is a choice among four method
families that borrow different things from the observable world. Pick by the question,
not by availability, and expect a well-implemented product over row crops to land at
15-20 % monthly and 0.5-1.2 mm d-1 daily error. Anything claiming much better is a
developer self-assessment or a single favourable site.

## The four families

| Family | Borrows | Use when | Breaks when |
|---|---|---|---|
| **Thermal one-source residual** - SEBAL, METRIC, SEBS, SSEBop, geeSEBAL | LST, through LE = Rn - G - H | you need stress diagnosis with no soil-moisture input | the scene is uniformly green and humid: the hot endmember must be manufactured |
| **Thermal two-source** - TSEB, ALEXI, DisALEXI | LST partitioned between soil and canopy | partial canopy over hot soil - the normal row-crop case before closure | LST calibration bias (ALEXI evades this via the *morning rate of change*) |
| **PT / PM satellite** - PT-JPL, MOD16, GLEAM, BESS-STAIR | VI, meteorology, no LST | gap-free all-weather coverage is required | stress must re-enter through a proxy, and each does it differently |
| **ML tower upscaling** - FLUXCOM, X-BASE | the EC network itself | climatology and across-site gradients | anomalies, drought, interannual variability (see below) |
| **LSM / reanalysis / assimilation** - Noah-MP, NLDAS-2, SMAP L4 | model physics | internal consistency with the atmospheric model consuming the answer | no crop phenology or management by default |

Endmember choice dominates forcing choice in the one-source family: biome-tuned endmember
percentiles cut error 36 %, while switching from ERA5-Land to in-situ meteorology moved
RMSD only 0.67 to 0.71 mm d-1
([geeSEBAL](https://doi.org/10.1016/j.isprsjprs.2021.05.018)). Consistent algorithm
signatures from the WACMOS-ET tower evaluation: PM-MOD underestimates, SEBS overestimates,
PT-JPL and GLEAM are best overall
([10.5194/hess-20-803-2016](https://doi.org/10.5194/hess-20-803-2016)).

`et_products()` returns the bundled 24-row table (`et_product_skill_table.csv`) with
inputs, native resolution, reported cropland RMSE and bias, validation DOI and principal
failure mode per product.

## The numbers to hard-code

- **Practical ceiling over cropland**: MAE **15.8 mm month-1** = 17 % of observed,
  MBE -5.3 mm month-1, r2 0.90, from 152 CONUS stations
  ([10.1038/s44221-023-00181-7](https://doi.org/10.1038/s44221-023-00181-7)). Per-model
  spread in the same ensemble: 13.6-21.6 mm month-1, daily MAE 0.74-1.07 mm d-1
  ([10.1111/1752-1688.12956](https://doi.org/10.1111/1752-1688.12956)).
- **Corn Belt benchmark to beat**: BESS-STAIR, 30 m daily, 12 maize/soybean sites, 85
  site-years - R2 0.75, RMSE **0.93 mm d-1**, 27.9 % relative, *calibration-free*
  ([10.5194/hess-24-1251-2020](https://doi.org/10.5194/hess-24-1251-2020)).
- **Field-size dependence, usually ignored**: fused Landsat-MODIS two-source ET gives
  0.5 mm d-1 on overpass dates, 0.9 mm d-1 daily at Mead NE (~50 ha fields) and
  1.5 mm d-1 at Bushland TX (~5 ha fields)
  ([10.1016/j.agrformet.2013.11.001](https://doi.org/10.1016/j.agrformet.2013.11.001)).
  **Error scales with field-size-to-pixel-size ratio, not with the algorithm.**
- **Climate-zone warning for the Midwest**: in a 30-tower comparison, TSEB-PT performed
  *worst* in warm-summer humid continental climate - daily RMSE 1.2 mm d-1 (MPBE -9 %) vs
  1.3 mm d-1 (+1 %) for a single-source model - and **averaging the two improved both**,
  because the errors are of opposite sign
  ([10.1029/2022wr032800](https://doi.org/10.1029/2022wr032800)). This is the empirical
  case for ensembling rather than picking a winner.
- **Resolution vs product error**: 1 km to 70 m pixels against the same towers increased
  correlation 85 % and cut RMSE 62 %
  ([10.1029/2019wr026058](https://doi.org/10.1029/2019wr026058)). Most of what coarse-pixel
  validation calls product error is representativeness error.

## The ML upscaling hard limit

Read this before proposing an ML ET twin. Skill is stratified by timescale, and the
stratification is **algorithm-invariant**: across 11 methods from four algorithm classes,
LE and H reach R2 > 0.7 - but that skill lives in the across-site gradient and the mean
seasonal cycle, while 8-day deviations *from* that cycle come in at R2 < 0.5
([10.5194/bg-13-4291-2016](https://doi.org/10.5194/bg-13-4291-2016)). The global product
shows the same split: modelling efficiency 0.64-0.84 across-site, 0.84-0.89 seasonal,
**0.29-0.52 monthly anomalies**
([10.1029/2010jg001566](https://doi.org/10.1029/2010jg001566)).

Because the result does not depend on the algorithm, the ceiling is in the **predictor set
and the network**, not in the regression. Greenness plus meteorological climatology tells
you what an average July looks like at a site; it does not tell you what *this* July did.
The consequence is documented flatness in interannual variability, acknowledged by the
developers in every generation - X-BASE states that very low IAV is common to
state-of-the-art data-driven products and remains **unsolved**
([10.5194/bg-21-5079-2024](https://doi.org/10.5194/bg-21-5079-2024)).

Two inherited defects. **Closure inheritance**: training targets understate available
energy by ~12 % across 194 CONUS stations
([10.1016/j.agrformet.2023.109307](https://doi.org/10.1016/j.agrformet.2023.109307));
FLUXCOM treats the closure correction as an explicit ensemble dimension rather than a
preprocessing decision - copy that. **Sparse-network extrapolation**: better over dense
vegetation than barren, better at temperate forest than under-represented biomes.

If a learned component is wanted, take the **hybrid** route: keep the Penman-Monteith
structure and learn only the resistances
([10.1088/1748-9326/acbbe0](https://doi.org/10.1088/1748-9326/acbbe0)). Caveat from that
same paper: inferring stomatal and aerodynamic resistance simultaneously admits equifinal
solutions. Learn one, prescribe the other.

## NDVI and crop type: the settled answer

**Vegetation indices carry most of the transferable information about cropland ET. Crop
type adds little to the LEVEL of ET once a VI is in the model, but carries real
information about TIMING and structure.**

- Transpiration fractions differ by crop (T/ET 0.69 corn vs 0.62 soybean), but **EVI alone
  explains 75 % of T/ET variation across 71 site-years**, with within-crop R2 0.84 (corn)
  and 0.82 (soybean)
  ([10.1002/2015wr017766](https://doi.org/10.1002/2015wr017766)). The between-crop
  difference is largely expressible as a difference in greenness trajectory.
- Where crop type earns its place is **phenological alignment**: aligning 30 m daily
  ET-fraction series by *days since planting* rather than calendar day materially improved
  correlation with maize yield at Mead
  ([10.1016/j.rse.2018.02.020](https://doi.org/10.1016/j.rse.2018.02.020)).
- Crop identity is a first-order control on *seasonal* water use - crop switching could cut
  consumption up to 93 % vs up to 11 % for practices leaving land cover unchanged
  ([10.1038/s41467-024-46031-2](https://doi.org/10.1038/s41467-024-46031-2)).
- **Recipe**: build the VI relation first; add the crop label as a categorical conditioner
  of phenological alignment and coefficient-curve shape (plus max height and harvest date),
  not as an additive level shift. A crop mask will not rescue a model with no stress
  mechanism.
- **Gap**: no retrieved study isolates the incremental skill of a CDL crop label against an
  otherwise identical VI-only ET model. The question is answerable with existing AmeriFlux
  and OpenET data and appears not to have been asked directly.

### Kcb-NDVI lineage

Origin for corn: [Bausch 1995](https://doi.org/10.1016/0378-3774%2895%2901125-3);
generalised via a density coefficient from fractional cover and height
([Allen & Pereira](https://doi.org/10.1007/s00271-009-0182-z), reviewed in
[10.1016/j.agwat.2020.106197](https://doi.org/10.1016/j.agwat.2020.106197)). Operational
instance: SIMS, 30 m daily, now an OpenET member. Skill: NDVI-to-Fc r2 0.96, daily basal ET
uncertainty < 0.5 mm d-1, seasonal 6-10 % across 49 fields and 18 crop types
([10.3390/rs4020439](https://doi.org/10.3390/rs4020439)); MODIS-NDVI dual-Kc over the High
Plains gives Kc r2 0.90-0.91, RMSE 0.16-0.19
([10.3390/rs5041588](https://doi.org/10.3390/rs5041588)).

**Two structural limits.** NDVI saturates at high LAI, so closed corn at LAI 4 and LAI 6 is
spectrally near-identical with different transpiration. More fundamentally, **a basal crop
coefficient describes ET under full water availability, so it has no stress mechanism** -
over rainfed Midwest cropland in drought it reports near-potential ET from a green-but-
stressed canopy, exactly the opposite of the thermal family's property. That is why the
crop-coefficient route is safer over irrigated California than over the rainfed Corn Belt,
and why the two families are complementary rather than redundant.

### LAI sensitivity is asymmetric - remember the sign

Propagating six satellite LAI approaches through a two-source model: **+50 % LAI error
produces up to 50 % change in ET, while -50 % error produces less than 10 %**
([10.1007/s00271-022-00798-8](https://doi.org/10.1007/s00271-022-00798-8)). An LAI product
that errs high is far more damaging than one that errs low. From the same paper:
locally-trained LAI regressions gave RMSE 0.3-0.48 but did **not** generalise between
sites. Do not port one to new fields.

### Carbon-water proxies and PhenoCam

Radiance-based NIRv explains 84 % (corn) and 78 % (soybean) of half-hourly GPP variance,
outperforming NIRv reflectance, EVI and far-red SIF760, consistently across irrigation
conditions ([10.1088/1748-9326/ab65cc](https://doi.org/10.1088/1748-9326/ab65cc)) - the
best crop-specific carbon proxy for the Corn Belt. Satellite SIF/PAR correlates with tower
transpiration at mean inter-site r 0.59
([10.3390/rs11040413](https://doi.org/10.3390/rs11040413)): real, not yet competitive
standalone. **There is no published PhenoCam-to-ET predictive model over Midwest row
crops** - the single retrieved PhenoCam-ET study uses greenness as a covariate in seasonal
attribution ([10.1029/2022jg006916](https://doi.org/10.1029/2022jg006916)). Treat PhenoCam
ET prediction as an open opportunity, not prior art.

## Validation protocol

1. **Closure-correct the tower reference** before using it as target or reference.
   Uncorrected EC is low by ~12 %, large enough to reverse a reported bias sign. Always
   check which convention a paper used before comparing error statistics across papers.
2. **Use footprint-weighted, not fixed-radius, predictors.** Fixed-extent target areas
   (radii 250-3000 m) bias EVI by 4-20 % and dominant land-cover fraction by 6-20 %
   ([10.1016/j.agrformet.2021.108350](https://doi.org/10.1016/j.agrformet.2021.108350)).
3. **Validate components, not just totals, and expect them to be much worse**: soil
   evaporation RMSD 90-114 %, interception 62-181 %, transpiration 54-114 %, against
   35-49 % for total ET
   ([Talsma et al. 2018](https://doi.org/10.1016/j.agrformet.2018.05.010)). Compensating
   component errors are what make totals look acceptable.
4. **Keep an independent water-balance check.** Family uncertainty ordering, south-central
   US: LSM ~5, satellite 10-15, GRACE water-balance 20-30 mm month-1
   ([10.1002/2013wr014581](https://doi.org/10.1002/2013wr014581)) - and finer resolution
   did *not* mean lower uncertainty. GRACE is too coarse to map but shares no error sources
   with towers or satellites.
5. **Watch downstream propagation.** Crop water productivity carries 7-22 % error from the
   remote-sensing products alone but 74-108 % once yield and ET uncertainty are both
   propagated ([10.1016/j.rse.2019.111413](https://doi.org/10.1016/j.rse.2019.111413)).

## The DERECHOS white-paper bias chain: three corrections

The white paper's section 4.2.2 cites Talsma 2018 and Mu 2011 for satellite ET missing
observed heterogeneity at ARM SGP, then Sullivan 2019a/b as the remedy. Retrieval says:

1. **Attribution.** The SGP heterogeneity finding and the -38 % number belong to
   [Sullivan et al. 2019a](https://doi.org/10.1029/2018jg004744), not to Talsma or Mu.
   [Mu et al. 2011](https://doi.org/10.1016/j.rse.2011.02.019) is the MOD16 algorithm paper
   - the *object* of the criticism, not a source of it.
   [Talsma et al. 2018](https://doi.org/10.1016/j.agrformet.2018.05.010) is a global
   *partitioning*-uncertainty evaluation, not an SGP heterogeneity study.
2. **Sign.** The MOD16 bias at SGP is **negative**: -38 % annual ET, from an overestimated
   dry-canopy surface resistance. A reader of the white paper as written could infer the
   bias is positive.
3. **"Largely remove that bias" holds only for the annual mean.** Bias -38 % to +1 % is
   decisive, but RMSE improved only 43 to 36 W m-2 and **temporal correlation did not
   improve at all** (0.75 vs 0.72, not significant). Fixing the vegetative-control
   parameterisation fixes the seasonal water budget without measurably improving the
   ability to track ET variability in time. For hypotheses about anomalies, drought and
   convective feedback, bias correction of this kind is necessary but demonstrably not
   sufficient.

On [Sullivan et al. 2019b](https://doi.org/10.1175/jhm-d-18-0259.1), the claim is stronger
than the white paper's gloss about forcing resolution: recomputing ET **offline** from
CMIP5 archived meteorology with Penman-Monteith plus satellite vegetation cut annual ET
bias from 38-73 % to -8 to +14 %. **The leverage is in the flux calculation, not in the
resolution of the meteorology** - the model's own ET scheme is what destroys information
already present in coarse output.

## Recommended architecture for a Midwest ET product

**Do**: a performance-weighted ensemble with a thermal member, a conductance member and a
crop-coefficient member. Six structurally different models converge over cropland (r2 0.90,
17 % monthly MAE) while diverging over shrubland and forest; single- and dual-source biases
are of opposite sign and cancel; performance weighting adds a further 8 % in agriculture
([10.1029/2024wr038899](https://doi.org/10.1029/2024wr038899)) - the *smallest* gain of any
land-cover class, because the models already agree there, so do not oversell weighting.

**Do not**: make a tower-trained ML model the primary estimator. Use it as a gap-filler and
a diagnostic, and report anomaly skill separately from climatological skill.

**Inputs**: Landsat C2 plus Sentinel-2 (HLS) reflectance and LAI; Landsat TIR supplemented
by sharpened VIIRS or ECOSTRESS for thermal continuity; gridded meteorology; CDL for the
crop mask; SMAP L4 for root-zone soil moisture, remembering its gains are in soil moisture
not flux; and the ALEXI-based Evaporative Stress Index as the thermal drought constraint
soil-moisture assimilation misses
([10.1175/2010jcli3812.1](https://doi.org/10.1175/2010jcli3812.1)).

**Pitfall ranking for a humid Midwest domain**: (1) no valid dry endmember in a
fully-vegetated summer scene; (2) senescent-but-green late-season corn, under which all
thermal partitioning schemes degrade
([10.5194/hess-18-1165-2014](https://doi.org/10.5194/hess-18-1165-2014)); (3) no stress
mechanism in the crop-coefficient member over rainfed fields; (4) flat anomaly response of
any learned member in exactly the drought years the coupling hypotheses need; (5)
compensating component errors masking bad partitions; (6) ALEXI's 5-10 km native scale
against a field mosaic, which is what disaggregation and fusion exist to bridge.

## What two EC sites plus a redeployable module can constrain

**Can**: anchor the absolute level and seasonal shape of ET over the two dominant
soil-crop combinations to closure-corrected tower accuracy - enough to calibrate a domain
product's bias. Precedent: one well-instrumented site converted a -38 % annual bias to
+1 % via a single parameterisation constraint. A soil-texture contrast constrains the
soil-evaporation component, which carries the largest documented model error. A
redeployable module moved along a land-use gradient within a season is the right instrument
for the between-field variance that dominates coarse-pixel validation.

**Cannot**: constrain temporal-anomaly skill. Two sites cannot separate a domain-wide
soil-moisture anomaly from local management, cannot populate anomaly-year training data to
fix the flat IAV response, and cannot validate sub-seasonal variability where every family
loses most of its skill. Two additions change the calculus: aggressive use of existing
AmeriFlux-registered towers in the domain as an extended validation network, and a
basin-scale water-balance closure check.

## Retrieval note

Mu et al. 2011 and 2007, Velpuri et al. 2013, Suyker & Verma 2009, Ershadi et al. 2014,
Kimball et al. 2019 and Carter & Liang 2019 are closed-access with no abstract in OpenAlex,
CrossRef or Semantic Scholar, and `fetch_article_fulltext` returns found=false. **Their
self-reported validation statistics are not retrievable through the standard toolchain** -
cite third-party evaluations for MOD16's cropland error rather than quoting Mu's own tables
from memory. `fetch_article_fulltext` does return a usable abstract for some closed Elsevier
DOIs even when full text fails, so it is worth one call; Semantic Scholar's graph API fills
some OpenAlex abstract gaps.

## Related skills

`cropland-et-measurement` for the tower side and the closure conventions this protocol
depends on; `derechos-campaign`, `derechos-data-sources` and `derechos-landuse-imagery` for
the DERECHOS domain.
