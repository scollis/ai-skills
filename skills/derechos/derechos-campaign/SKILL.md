---
name: derechos-campaign
description: Authoritative reference for the DERECHOS campaign - the proposed two-year DOE ARM Mobile Facility deployment to the Iowa-Illinois Midwest (Midwest Baseline Array Earth System Observatory). Load for DERECHOS hypotheses H1-H4, science questions SQ1-SQ7, the science traceability matrix, the Muscatine MIRF/S1 or SERF/M1 sites, ARM redeployable profiling modules, the NIU Argonne Deployable Mast cluster, ATMOS or the Chicago Micronet, derecho and QLCS climatology, land-atmosphere coupling and evapotranspiration over managed croplands, Midwest freezing rain, agricultural aerosol (CCN, INP, dust, smoke), nocturnal low-level jets, wake lows and rear-inflow jets, the E3SM/SCREAM Midwest digital testbed, or DERECHOS AI plans (self-driving instrumentation, WaggleDop, domain-wide ET inference, anomaly detection, phenocam computer vision). Ships the machine-readable traceability matrix plus kernel helpers for instrument, science-question and site lookups.
---

# DERECHOS — campaign reference

**DERECHOS** = *Dynamics of Evapotranspiration, Radiative Exchange, and
Convection in High-impact Organized Storms*. A proposed **two-year ARM Mobile
Facility (AMF2) deployment** to the U.S. Midwest, submitted to DOE BER in
response to the ARM white-paper call. It forms the atmospheric anchor of the
**Midwest Baseline Array Earth System Observatory** ("the Array").

Lead author: Scott Collis (Argonne, Environmental Science Division). Co-authors
span Argonne, Northern Illinois University (NIU), UIUC, LLNL, Iowa State, and the
Illinois State Water Survey.

**Status: selected by DOE.** The white paper was accepted and the deployment is
going ahead, with Scott Collis leading it. Treat the science case - hypotheses,
science questions, the domain and the site concept - as the settled baseline for
planning and analysis work.

**But everything in this skill is still the white-paper text.** Dates, instrument
lists, site assignments and IOP counts were written as *requests* to ARM and will
move as the operations plan is negotiated: the July 2027 start was offered as
flexible, the redeployable profiling modules were "still under design" at writing,
and the traceability matrix has known gaps (see Errata). So: cite the science case
confidently, and treat any specific instrument, date or site number as
provisional-pending-the-ops-plan unless the user has told you it is fixed. When a
number matters operationally, ask rather than quoting the white paper at them.

## The pitch in three sentences

Organized convection — QLCSs and derechos — costs the Midwest billions annually,
including damage to the electric grid (the 2020 Midwest derecho alone: >$11B).
NWP with data assimilation handles these systems out to 3–5 days, then skill
collapses because models misrepresent the slow two-way coupling between the
atmosphere and *managed* land surfaces (row-crop agriculture, irrigation,
cover-cropping) and the resulting evapotranspiration. DERECHOS instruments a
land-use gradient from Ames, Iowa to Chicago, Illinois to close that
seasonal-to-annual (S2A) predictability gap and to give E3SM a Midwest process
benchmark.

## Hypotheses

| | Short form |
|---|---|
| **H1** | Managed land-surface heterogeneity and rural–urban gradients modulate convective organization. |
| **H2** | Bidirectional soil-moisture / convective-system coupling sets a critical limit on S2A predictability. |
| **H3** | Land-surface heterogeneity and aerosol effects control freezing-rain severity. |
| **H4** | Vegetation, crop type, and aerosol impact BL turbulence, clouds and extreme convection in the warm season. |

Full text: `derechos_hypotheses()`.

## Science questions

Seven SQs, grouped in three themes. Full text: `derechos_sq(n)`.

| SQ | Theme | Hypotheses | Topics | Gist |
|---|---|---|---|---|
| SQ1 | Land surface & storm evolution | H1, H2 | ST1, ST2, ST5 | ET / soil-moisture / vegetation heterogeneity across the convective lifecycle; depth of available moisture; corn vs soy; runoff vs recharge; weeks-to-years predictability; dry-soil/hot-BL regime driving summer electricity demand |
| SQ2 | Land surface & storm evolution | H3, H4 | ST3, ST4 | Land-use heterogeneity → PBL stability, shallow cloud, upscale growth, wind/hail hazards; frozen soil and snow insulation controlling fluxes in freezing rain |
| SQ3 | Land surface & storm evolution | H3, H4 | ST2, ST4, ST5 | Thermodynamic profiles favouring snow / sleet / freezing-rain transitions; role of landcover, crops, albedo |
| SQ4 | Aerosol, cloud & storm properties | H1, H4 | ST3, ST4 | Managed-ecosystem aerosol (biogenic SOA, pollen, soil dust, ag burning) → CCN/INP, convective microphysics, precipitation efficiency; E3SM fidelity |
| SQ5 | Aerosol, cloud & storm properties | H1, H4 | ST1, ST3, ST4 | Light-absorbing ag dust and smoke → pre-storm BL thermodynamics, capping inversion, mixing depth, shallow-to-deep transition; E3SM fidelity |
| SQ6 | Energy-specific | H1, H3 | ST2, ST3 | Wake lows and rear-inflow jets; vertical structure of wind extremes for tall transmission vs 10 m distribution lines; freezing-rain outage risk |
| SQ7 | Energy-specific | H2, H4 | ST2, ST3 | Nocturnal low-level jets × surface heterogeneity → overnight organized convection; preconditions for grid-impacting night events; subseasonal prediction |

**Specific topics of interest** from the call (ST1–ST5): water availability for
energy; Midwest storms and their energy impact; convective lifecycles;
microphysical phase and energy impacts; complex land surface and implications for
water.

## The Array — four components

1. **Main cluster.** **M1** at the Iowa State **South East Research Farm (SERF)**,
   Crawfordsville — full AMF site plus AOS. Maize on poorly drained silty clay loam.
   **S1** at the **Muscatine Island Research Farm (MIRF)** — sandy soils, fruit
   crops, nearer the derecho hot spot, synoptically similar but a different
   microclimate. Both sit on the same WSR-88D radial from **KDVN** (Davenport, IA;
   0Z/18Z soundings), ~55 and 34 miles southwest of it respectively — so the main
   facility is now at the *far* end of that radial, where the 0.5 deg KDVN beam
   centre is ~1240 m AGL against ~650 m over S1. DERECHOS requests ECOR/SEBS at *both*
   sites and advocates SoilVue10 soil-moisture profiling as close to (ideally in)
   the farm fields as the farm managers allow.
2. **R1 — ARM redeployable profiling modules**, based at M1, deployed within
   150 km. Candidate hosts: Illinois Climate Network, the future Illinois 3D
   mesonet (co-author Nesbitt participates), Iowa Environmental Mesonet sites,
   Nachusa Grasslands (41.858 N, 89.652 W).
3. **Guest instrument cluster** at Argonne and **NIU** — Argonne-managed suite on
   the **Argonne Deployable Mast (ADM)** (10 m winch-up mast), plus flux towers
   and a SoilVue10. Duplicates ARM pod capability *except* AERI and MWR3C.
   Possible **C-Band On Wheels** deployment to NIU via Gensini's arrangement with
   the UAH Flexible Array of Radars and Mesonets.
4. **Mobile sounding crews** from NIU and UIUC — radiosondes and windsondes in
   the pre-convective environment, cold pools/outflows, and post-storm.
   Argonne: Sparv windsonde system + 10 sondes (in-kind, more to be procured).
   UIUC: two iMet systems.

Plus the **Chicago region**: ATMOS (Argonne Testbed for Multiscale Observational
Science) and the CROCUS-built **Chicago Micronet** — expected stewardship at
Villa Park, Downers Grove, and edge-computing sites at the Shedd Aquarium and
ATMOS; 10 m flux towers at ATMOS and downtown Chicago (with UIC), both
AmeriFlux-registered. All sites can host guest instrumentation.

ATMOS is on the Argonne campus at Lemont, **41.7018N, 87.9963W** (232 m; AmeriFlux
`US-AMS`), 13.1 km from the KLOT WSR-88D - not in downtown Chicago, and not at the
city centroid some references use for "the Chicago region".

Regional leverage that is *not* ARM-supplied: Iowa Environmental Mesonet,
Illinois Climate Network, AmeriFlux, NEXRAD, USDA Cropland Data Layer,
Sentinel-2, urban air-quality networks.

Site details: `derechos_sites()`.

## Timeline and IOPs

- Preferred start **July 2027**, flexible. Two years — motivated by the derecho
  climatology of Li et al. (2025), whose hot spot averages ~**4 derechos/year**,
  so two seasons are needed to build a usable case library.
- **10 IOPs per year** (Appendix 2 refers to 20 IOPs over the deployment).
- IOP selection driven by a **"science scorecard"** plus forecast, targeting
  conditions that address SQ1–SQ7. Enhanced **3-hourly soundings** at M1 during
  IOPs; windsondes proposed for the 12Z/18Z flights since upper levels should
  resemble the DVN NWS office profile.
- Redeployable-module strawman: deploy to initial locations at the start of
  spring and fall; capture ≥1 week of storms; between storms, with a 3–4 day
  forecast break, make a go/no-go call to reconfigure. Week-plus deployments —
  these are redeployable, **not mobile**. Site priorities: safety/security, then
  power, then network; science priorities: east–west corridor alignment, varied
  land use, distinctness from S1/M1 land use.

## Science traceability matrix

Four tables, all machine-readable in `derechos_stm.json` (Table 1 also as
`derechos_stm_table1.csv`):

| Table | Content | Rows |
|---|---|---|
| 1 | Requested AMF instruments, mapped to SQ1–7 × sites M1/S1/R1 × priority | 32 |
| 2 | *Additional* ARM instruments requested at M1 (ACSM, SACR, SP2, INS, POPS, ExtLidar) | 6 |
| 3 | ANL-supplied guest instruments at NIU (on the ADM) | 8 |
| 4 | Selected ATMOS capabilities in the Chicago region | 7 categories |

Priority: ★★★ critical/core for the primary hypotheses; ★★ substantially
strengthens interpretation or process closure; ★ nice-to-have.

The white paper singles out **Doppler lidar (DL)** and **AERI** as the most
impactful profiling-module instruments — they time-resolve dynamics *and*
thermodynamics. Redeployable **ECOR** is flagged as highly impactful but not
expected in the initial module design. Soundings from the profiling modules are
possible during IOPs but will be requested sparingly (ARM staff logistics).

Query it:

```python
derechos_instruments(sq=3, min_priority=3)      # core instruments for SQ3
derechos_instruments(site="S1")                 # everything requested at MIRF (supplemental)
derechos_instruments(table=3)                   # ANL guest kit at NIU
derechos_traceability(sq=7)                     # SQ -> instrument listing
```

## Research strategy

**AI, four thrusts** (§4.2):

1. **Self-driving instrumentation.** *WaggleDop* (Jackson et al., 2026) —
   adaptive scanning for Halo Streamline Doppler lidars on cloud-native edge
   compute, triggering scan strategies from external sensors and data feeds.
   Combined with the Park et al. (2026) ML lake-breeze detector it already ran
   fully autonomous cross-front RHIs for two Argonne lake-breeze cases in
   spring 2026. DERECHOS will retrain that model for cold pools, gravity waves
   and similar features, use high-resolution storm modelling to design ideal
   lidar scan modes, and trigger mode changes off nearby WSR-88Ds or field
   research radars — starting with the NIU system. Extensible to scanning cloud
   radars if ARM is interested.
2. **Domain-wide inference.** ARM footprints are small; storm inflow spans
   states. Spaceborne ET is biased (Talsma et al., 2018; MODIS-based Mu et al.,
   2011 misses observed heterogeneity at SGP), but improved vegetative controls
   plus in-situ constraints (Sullivan et al., 2019a) or higher-fidelity model
   forcing instead of coarse reanalysis (Sullivan et al., 2019b) largely remove
   it. Plan: calibrate against DERECHOS eddy-covariance data to build a baseline
   domain ET product, then an AI/ML **ET digital twin** benchmarked on ARM,
   AmeriFlux and mesonet data.
3. **Anomaly detection and automated case flagging.** Clustering and ML anomaly
   detection over lidar/radar to classify atmospheric states and surface
   high-impact events, complementing ARM DQ; reuse of existing LLJ detection and
   rain-flag products.
4. **Computer vision for land-surface state.** Site cameras and phenocams;
   greenness metrics (green chromatic coordinate — Richardson et al., 2018;
   Seyednasrollah et al., 2019) extended by fine-tuned multimodal models to
   categorical labels: crop growth stage, canopy development, greenness
   transitions, bare ground, crop residue, snow cover, visible standing water
   (cf. VegAnn — Madec et al., 2023; Taylor & Browning, 2022). Paired with USDA
   CDL / Sentinel-2 to stratify storm cases by surface condition.

DERECHOS will interact with **Genesis Mission** projects and leverage the
**American Science Cloud (AmSC)**, registering datasets with its catalog.

**Midwest Digital E3SM Testbed** (§4.3): with the **THREAD SFA**, a multiscale
regionally-refined **SCREAM** (cloud-resolving E3SM) domain over the study
region, initialized and forced by **HRRR** (Dowell et al., 2022) and ERA5. Runs
before the campaign refine the measurement strategy; runs after selected IOPs
(compute via DOE federated LCF allocations, possibly through AmSC/Genesis)
support benchmarking against campaign products such as the §4.2.2 ET map. The
intent is a live **MODEX loop** — modelling teams test configurations and physics
and feed back to the measurement team *while the campaign is running*.

## Data and operations notes

- Data from all ARM-supported instrumentation goes to the **ARM Data Center**;
  the team will work with ARM to decide ingest vs PI product.
- **Coarse-mode aerosol** measurement limitations are acknowledged; the team is
  following DUSTIEAIM progress and wants to work with ARM on testing new
  agricultural-dust measurements.
- **Safety**: a comprehensive plan modelled on CROCUS Urban Canyons (Collis et
  al., 2026) and the Urban Flooding and Rainfall campaigns. Sounding crews launch
  only from sites near hotels with usable storm shelters; the I-80/I-88 corridors
  supply small towns adjacent to fields as an à la carte site menu. Argonne
  students at NIU maintain instruments to set procedures, including stowing the
  10 m winch mast ahead of extreme winds (hardening in progress).

## Errata in the white-paper draft (audited)

A systematic consistency pass over the draft found 20 issues; the full table lives
in `derechos_whitepaper_errata.csv` / `.md` in the project artifacts. The ones
that change how you should read the document:

- **Table 1 has no soil-moisture / soil-temperature profile row**, although H2 and
  SQ1 turn on soil-column moisture at depth and both §3.1 (SoilVue10 advocacy) and
  §4.1 ("soil moisture and temperature profiles") promise it at the core sites. If
  you are asked which instrument addresses soil moisture, the honest answer is that
  the submitted matrix does not trace it - do not silently substitute SEBS or ECOR.
- **Table 1 has no phenocam / site-camera row**, although §4.2.4 is an entire AI
  thrust built on ARM site cameras and phenocams. ASI is sky-facing.
- **SERF name**: "South East Research Farm (SERF)" (abstract, §3.1) vs "Southwest
  Research Farm" (deployment site key under Table 1, p. 12).
- **MIRF name**: four variants across the document (with and without "Island", with
  and without "and Demonstration").
- **Gallus and Harrold (2023)** is cited in §1 but absent from the reference list;
  **Barton et al. (2025)** is in the list but never cited, despite being the closest
  published support for H2.
- **SQ2 is tagged (H3, H4)** although its first half is the literal claim of H1.
- **S1-M1 separation: RESOLVED by measurement.** Using the co-located IEM ISUSM
  stations as site proxies (FRUI4 = S1, CRFI4 = M1), both sites sit on KDVN azimuth
  238.7 deg - confirming the white paper's "same radial" claim exactly - at 54.4 and
  88.7 km range, a separation of 34.3 km. So the abstract's 35 km is right and
  §3.1's "51 miles" for M1 is the error; it should read ~55 miles. Provisional at
  sub-kilometre precision until ARM/ISU survey the actual instrument pads.
- **S1's deep soil record is unusable across the ENTIRE archive**, not just recently.
  Measured over 2014-2026 at the co-located ISUSM station (FRUI4): soil24vwc reports
  negative volumetric water content on 79.8 % of its unpinned days (median -1.1 %) and
  soil50vwc on 86.5 % (median -3.8 %) - physically impossible - on top of pinning at
  1.00 % from 2015-12-14 and 2022-05-25 respectively. Both failure modes pass a
  completeness check. There is no window in which S1 deep soil moisture can be used.
  M1 (CRFI4) is clean at all three depths for the whole record (medians 44.8 / 44.9 /
  40.2 %). S1's 12 cm sensor reads a median 4.2 %, low but plausible for the site's
  sandy soils rather than broken. So: a decade-plus soil baseline exists free at M1
  and at 12 cm at S1, and **never** at depth at S1. Combined with Table 1 tracing no
  soil-moisture instrument at all, the §3.1 SoilVue10 advocacy is **not** an upgrade at
  S1 - it is the only way that site will ever have deep soil moisture. Note the
  consequence of the 2026 M1/S1 reassignment: the main facility (M1, CRFI4) already
  carries a clean 9-depth SoilVue profile to 132 cm installed 2025-08-15, so the
  request now argues for the *supplemental* site, not the main one. Gotcha: ISUSM uses
  **-99 as a missing sentinel** for VWC and the fetch helper does not map it to NaN.
- **Storm-to-soil recharge has a measured pre-campaign baseline** (M1, 402 warm-season
  events, MRMS QPE vs ISUSM): median apparent recharge efficiency 0.295 of event
  rainfall into 0-75 cm, and it does **not** vary with antecedent wetness (p=0.98) -
  but its *depth* does. On dry antecedent soil the 37-75 cm layer takes 11 % of the
  stored water (50 cm ΔVWC 0.08 pp); on wet soil 45 % (0.37 pp). The deep reservoir
  that sustains ET is refilled only when the column is already wet or by events above
  ~20-40 mm, which is a candidate mechanism for H2's S2A predictability limit. Caveat:
  M1 never dries below ~40 % VWC, so the genuinely dry limb H2 cares about is
  unsampled. MRMS QPE at the sites is good to 5-10 % in the warm season but exceeds
  the unheated gauges by ~30 % in winter (both sites - gauge under-catch of snow).
  See `h2_storm_soil_recharge.md`.
- Typos to expect when quoting: "course mode" for coarse mode (§3.1), "represent
  represent" (SQ5), "regeneratioon" (CPCu row of Table 1).

Checked and **consistent** (do not flag these): the IOP count - §3.3's 10 IOPs/year
over the two-year deployment is exactly Appendix 2's "20 IOPs"; TOC page numbers;
ECOR/SEBS requested at both core sites in text and matrix. The Table 1 MRR row
being R1-only while Table 3 places an MRR at NIU is the ARM-requested vs
Argonne-guest split, not a contradiction.

## Acronyms

AERI Atmospheric Emitted Radiance Interferometer · ADM Argonne Deployable Mast ·
AMF (ARM) Mobile Facility · AmSC American Science Cloud · AOS Aerosol
Observing System · ARM Atmospheric Radiation Measurement · ASI All-Sky Imager ·
ATMOS Argonne Testbed for Multiscale Observational Science · BER Biological and
Environmental Research · BL boundary layer · CCN cloud condensation nuclei ·
CDL Cropland Data Layer · CEIL ceilometer · CROCUS Community Research on
Climate and Urban Science · DL Doppler lidar · DQ data quality · E3SM Energy
Exascale Earth System Model · ECOR eddy correlation flux system · ET
evapotranspiration · HRRR High-Resolution Rapid Refresh · INP ice-nucleating
particle · IOP intensive observational period · KAZR Ka-band ARM Zenith Radar ·
KDVN Davenport IA WSR-88D · LDIS laser disdrometer · LLJ low-level jet ·
MIRF Muscatine Island Research Farm · MODEX model-experiment (loop) · MPL
micropulse lidar · MRR micro rain radar · MWR3C 3-channel microwave radiometer ·
NIU Northern Illinois University · PBL planetary boundary layer · QLCS
quasi-linear convective system · R1 redeployable · RWP radar wind profiler ·
S2A seasonal-to-annual · SACR scanning ARM cloud radar · SCREAM Simple
Cloud-Resolving E3SM Atmosphere Model · SEBS surface energy balance system ·
SERF South East Research Farm · SFA science focus area · SGP Southern Great
Plains · SOA secondary organic aerosol · SQ science question · ST specific
topic · STM science traceability matrix · UIUC University of Illinois
Urbana-Champaign · VDIS video disdrometer · WB weighing bucket (rain gauge)

## Key references

Foundational to the proposal's argument:

- **Li et al. 2025** — ML-based derecho climatology 2004–2021 (bow echoes),
  ESSD, doi:10.5194/essd-17-3721-2025. *Defines the hot spot the domain targets.*
- **Zhang et al. 2025** — Corn Belt moisture fuels more intense convective
  storms, Commun. Earth Environ., doi:10.1038/s43247-025-03089-0.
- **Barton et al. 2025** — Soil-moisture gradients strengthen MCSs by increasing
  wind shear, Nat. Geosci., doi:10.1038/s41561-025-01666-8.
- **Wagner et al. 2025** — Wind damage in the 10 Aug 2020 derecho from UAS,
  satellite and radar, WAF, doi:10.1175/WAF-D-24-0198.1.
- **Mather et al. 2026** — ARM workshop report, *Leveraging ARM Data to Improve
  Models for Predictive Understanding of Energy and Security Challenges*,
  DOE/SC-ARM-26-004, doi:10.2172/3014737. *Severe convective storms and high
  winds are its top priority; also the source for the redeployable modules.*
- **Donahue et al. 2024** — SCREAM, JAMES, doi:10.1029/2024MS004314.
- **Dowell et al. 2022** — HRRR Part I, WAF, doi:10.1175/WAF-D-21-0151.1.
- **Sullivan et al. 2019a,b**; **Mu et al. 2011**; **Talsma et al. 2018** — the
  satellite-ET bias chain behind the §4.2.2 ET digital twin.
- **Jackson et al. 2026** (WaggleDop, AMT); **Park et al. 2026** (ML lake-breeze
  fronts, AIES); **Muradyan et al. 2026** (CROCUS Micronet, BAMS, in revision);
  **Collis et al. 2026** (CROCUS Urban Canyons, BAMS, in review);
  **Dematties et al. 2023** (self-supervised cloud image analysis, AIES,
  doi:10.1175/AIES-D-22-0063.1).
- Land-surface CV: **Richardson et al. 2018**; **Seyednasrollah et al. 2019**;
  **Madec et al. 2023** (VegAnn); **Taylor & Browning 2022**.
- **Gallus & Harrold 2023** — cited for row-crop/irrigation/cover-crop coupling.

## Related skills in this catalog

`arm-dualpol-calibration` and `gpm-storm-targeted-radar-fetch` cover ARM
radar calibration and GPM-overpass-driven case selection — relevant if DERECHOS
work extends to C-SAPR2-class radar data or satellite–ground matchups.

## Provenance

Built from *DERECHOS AMF2 White Paper (shareable draft)*, 21 pp. The traceability
matrix SQ/site/priority markers were parsed from the PDF text layer, which
preserves each row's marker glyphs in document order; a vision pass over the
rendered tables disagreed with the text layer on 29 of 32 rows and was rejected.
Table prose was reassembled verbatim from the same text layer. If you get access
to a later version of the white paper, re-derive `derechos_stm.json` rather than
hand-editing it.
