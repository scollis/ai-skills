"""DERECHOS IOP science scorecard - executable form of white-paper section 3.3.

Turns a gridded forecast over the Ames IA -> Chicago IL domain into a per-science-
question score, an IOP archetype label, and a go/hold decision that respects the
finite IOP budget, sounding-crew lead time and redeployable-module dwell.

Every threshold lives in DERECHOS_IOP_CONFIG (see iop_config / iop_dump_config).
"""

DERECHOS_CORRIDOR = {"lon": [-95.5, -86.5], "lat": [39.5, 43.5]}
# Box containing the fixed array (M1, S1, NIU) - gates are evaluated here so
# that a violent storm 400 km away does not open an IOP.
DERECHOS_ARRAY_BOX = {"lon": [-92.0, -88.3], "lat": [40.7, 42.3]}

# KDVN WSR-88D (41.6119 N, 90.5808 W); M1/S1 derived from the white paper's
# "33 miles" / "51 miles" southwest of Davenport on one radar radial.
DERECHOS_IOP_SITES = {
    "M1": [41.0879, -91.2733],
    "S1": [41.2733, -91.0302],
    "NIU": [41.929, -88.750],
    "NACHUSA": [41.858, -89.652],
    "ATMOS": [41.706, -87.982],
}

HRRR_SFC_FIELDS = [
    ["^REFC:entire atmosphere:", "refc", "dBZ"],
    ["^CAPE:surface:", "sbcape", "J/kg"], ["^CIN:surface:", "sbcin", "J/kg"],
    ["^CAPE:90-0 mb above ground:", "mlcape", "J/kg"],
    ["^CIN:90-0 mb above ground:", "mlcin", "J/kg"],
    ["^CAPE:255-0 mb above ground:", "mucape", "J/kg"],
    ["^CIN:255-0 mb above ground:", "mucin", "J/kg"],
    ["^VUCSH:0-6000 m above ground:", "ushr06", "m/s"],
    ["^VVCSH:0-6000 m above ground:", "vshr06", "m/s"],
    ["^VUCSH:0-1000 m above ground:", "ushr01", "m/s"],
    ["^VVCSH:0-1000 m above ground:", "vshr01", "m/s"],
    ["^HLCY:1000-0 m above ground:", "srh01", "m2/s2"],
    ["^HLCY:3000-0 m above ground:", "srh03", "m2/s2"],
    ["^PWAT:", "pwat", "kg/m2"], ["^HPBL:", "hpbl", "m"],
    ["^GUST:surface:", "gust", "m/s"], ["^PRES:surface:", "psfc", "Pa"],
    ["^TMP:2 m above ground:", "t2m", "K"], ["^DPT:2 m above ground:", "d2m", "K"],
    ["^UGRD:10 m above ground:", "u10", "m/s"], ["^VGRD:10 m above ground:", "v10", "m/s"],
    ["^UGRD:80 m above ground:", "u80", "m/s"], ["^VGRD:80 m above ground:", "v80", "m/s"],
    ["^UGRD:850 mb:", "u850", "m/s"], ["^VGRD:850 mb:", "v850", "m/s"],
    ["^UGRD:925 mb:", "u925", "m/s"], ["^VGRD:925 mb:", "v925", "m/s"],
    ["^UGRD:700 mb:", "u700", "m/s"], ["^VGRD:700 mb:", "v700", "m/s"],
    ["^UGRD:500 mb:", "u500", "m/s"], ["^VGRD:500 mb:", "v500", "m/s"],
    ["^SHTFL:surface:", "shtfl", "W/m2"], ["^LHTFL:surface:", "lhtfl", "W/m2"],
    ["^MSTAV:", "mstav", "%"], ["^SNOWC:", "snowc", "%"], ["^SNOD:", "snod", "m"],
    ["^VEG:surface:", "veg", "%"], ["^LAI:surface:", "lai", "-"],
    ["^CSNOW:", "csnow", "0/1"], ["^CICEP:", "cicep", "0/1"],
    ["^CFRZR:", "cfrzr", "0/1"], ["^CRAIN:", "crain", "0/1"],
    [r"^APCP:surface:\d+-\d+ hour acc", "apcp1h", "kg/m2"],
    [r"^FROZR:surface:\d+-\d+ hour acc", "frozr1h", "kg/m2"],
    ["^MASSDEN:8 m above ground:", "massden", "kg/m3"],
    ["^COLMD:", "colmd", "kg/m2"],
]

HRRR_PRS_RE = (r"^(HGT|TMP|RH|UGRD|VGRD):(500|525|550|575|600|625|650|675|700|725|"
               r"750|775|800|825|850|875|900|925|950|975|1000) mb:")

# ---------------------------------------------------------------------------
# Predictors.  Each entry: the summary statistic it reads, the ramp endpoints,
# the science questions it serves, and where the threshold comes from.
# kind: "ramp" (lo->hi, 0->1), "trap" (lo,lo2,hi2,hi -> 0,1,1,0), "linear".
# invert: high statistic -> low score.  optional: drop (renormalise) if absent.
# ---------------------------------------------------------------------------
DERECHOS_IOP_CONFIG = {
    "predictors": {
        "mlcape": {"stat": "mlcape_p90", "kind": "ramp", "lo": 500, "hi": 2500,
                   "units": "J/kg", "season": "warm",
                   "basis": "Craven & Brooks (2004) baseline climatology: most non-severe "
                            "thunderstorm proximity soundings fall below ~1100 J/kg MLCAPE; "
                            "2500 J/kg is the strongly-unstable tail."},
        "deep_shear": {"stat": "shear06_p90", "kind": "ramp", "lo": 12, "hi": 25,
                       "units": "m/s", "season": "warm",
                       "basis": "0-6 km bulk shear ~20 m/s (40 kt) is the conventional "
                                "organised/supercell discriminator; 12 m/s is the lower bound "
                                "for sustained multicell organisation."},
        "sigsvr": {"stat": "sigsvr_p90", "kind": "ramp", "lo": 10000, "hi": 30000,
                   "units": "m3/s3", "season": "warm",
                   "basis": "MLCAPE x 0-6 km shear (Craven-Brooks significant-severe "
                            "parameter); ~20000 m3/s3 separates significant-severe from "
                            "non-severe in their climatology."},
        "dcp": {"stat": "dcp_max", "kind": "ramp", "lo": 0.5, "hi": 3.0,
                "units": "-", "season": "warm",
                "basis": "SPC Derecho Composite Parameter (after Evans & Doswell 2001) = "
                         "(DCAPE/980)(MUCAPE/2000)(shear06/20kt)(meanwind06/16kt); values >1 "
                         "indicate an environment supporting a progressive derecho."},
        "dcape": {"stat": "dcape_max", "kind": "ramp", "lo": 600, "hi": 1200,
                  "units": "J/kg", "season": "warm",
                  "basis": "DCP normalises DCAPE by 980 J/kg (Evans & Doswell derecho "
                           "proximity median); 600-1200 brackets weak to strong cold-pool "
                           "generation potential."},
        "meanwind06": {"stat": "meanwind06_max", "kind": "ramp", "lo": 8, "hi": 16,
                       "units": "m/s", "season": "warm",
                       "basis": "DCP normalises 0-6 km mean wind by 16 kt (8.2 m/s); 16 m/s "
                                "is a fast-moving forward-propagating MCS."},
        "srh01": {"stat": "srh01_p90", "kind": "ramp", "lo": 100, "hi": 250,
                  "units": "m2/s2", "season": "warm",
                  "basis": "0-1 km SRH ~100-150 m2/s2 is the usual QLCS mesovortex / "
                           "tornado-potential floor in operational practice."},
        "gust": {"stat": "gust_p999", "kind": "ramp", "lo": 25, "hi": 40,
                 "units": "m/s", "season": "warm",
                 "basis": "NWS severe wind criterion 50 kt = 25.7 m/s; 40 m/s (~90 mph) is "
                          "the derecho-class tail. 99.9th percentile of the corridor - a "
                          "damaging-wind swath covers only a per-cent of the domain."},
        "wind80": {"stat": "wind80_p999", "kind": "ramp", "lo": 15, "hi": 30,
                   "units": "m/s", "season": "warm",
                   "basis": "80 m is the HRRR level nearest transmission-conductor height; "
                            "SQ6 asks for the vertical structure of wind extremes. 15-30 m/s "
                            "spans nuisance to structural loading."},
        "pwat": {"stat": "pwat_p90", "kind": "ramp", "lo": 25, "hi": 45,
                 "units": "kg/m2", "season": "both",
                 "basis": "Upper Midwest warm-season PWAT climatology: ~25 mm is near normal, "
                          "45 mm is near the record moist tail; SQ1 asks about the depth of "
                          "available moisture."},
        "cin_capping": {"stat": "mlcin_mag_p50", "kind": "trap", "lo": 25, "lo2": 75,
                        "hi2": 175, "hi": 350, "units": "J/kg", "season": "warm",
                        "basis": "SQ5 targets the capping inversion and shallow-to-deep "
                                 "transition: a cap must exist (>25 J/kg) but not be "
                                 "insurmountable (>350 J/kg suppresses the transition)."},
        "mixing_depth": {"stat": "hpbl_p90", "kind": "ramp", "lo": 1200, "hi": 2500,
                         "units": "m", "season": "warm",
                         "basis": "Deep dry-convective mixing is required for the aerosol-BL "
                                  "coupling in SQ5; 1200-2500 m spans a typical to deep "
                                  "Midwest summer afternoon PBL."},
        "hot_t2m": {"stat": "t2m_p90_c", "kind": "ramp", "lo": 30, "hi": 36,
                    "units": "degC", "season": "warm",
                    "basis": "SQ1's dry-soil/hot-BL regime driving summer electricity demand; "
                             "30 degC is the heat-advisory neighbourhood, 36 degC extreme."},
        "dry_soil": {"stat": "mstav_mean", "kind": "ramp", "lo": 60, "hi": 25,
                     "invert": True, "units": "%", "season": "warm",
                     "basis": "HRRR surface moisture availability; no established threshold - "
                              "60 -> 25 % chosen to span a well-watered Corn Belt summer to "
                              "the dry tail. REPLACE with SoilVue10-referenced soil moisture."},
        "sm_heterogeneity": {"stat": "site_mstav_range", "kind": "ramp", "lo": 5, "hi": 30,
                             "units": "%", "season": "both",
                             "basis": "Max-min surface moisture availability ACROSS THE ARRAY "
                                      "SITES (M1, S1, NIU, NACHUSA, ATMOS) - i.e. the contrast "
                                      "the instruments would actually resolve, not a domain "
                                      "variance dominated by water and urban pixels. Our "
                                      "reasoning; no established number."},
        "bowen_contrast": {"stat": "site_bowen_range", "kind": "ramp", "lo": 0.2, "hi": 1.2,
                           "units": "-", "season": "warm",
                           "basis": "Max-min Bowen ratio across the array sites (sites with "
                                    "|LH| < 20 W/m2 excluded as noise); our reasoning - the "
                                    "observable the ECOR/SEBS pairs at M1/S1/NIU resolve."},
        "veg_heterogeneity": {"stat": "lai_std", "kind": "ramp", "lo": 0.5, "hi": 2.0,
                              "units": "-", "season": "warm", "optional": True,
                              "basis": "HRRR LAI spatial sigma; corn/soy/urban contrast. "
                                       "Our reasoning. Absent in HRRRv3 (pre-2020-12)."},
        "smoke_near_sfc": {"stat": "massden_p99_ugm3", "kind": "ramp", "lo": 5, "hi": 35,
                           "units": "ug/m3", "season": "warm", "optional": True,
                           "basis": "HRRR-Smoke near-surface smoke mass density; 35 ug/m3 is "
                                    "the 24-h PM2.5 NAAQS, 5 ug/m3 a detectable perturbation."},
        "smoke_column": {"stat": "colmd_p99_mgm2", "kind": "ramp", "lo": 5, "hi": 50,
                         "units": "mg/m2", "season": "warm", "optional": True,
                         "basis": "HRRR-Smoke column-integrated mass density; our reasoning, "
                                  "scaled so a visible smoke pall saturates the predictor."},
        "dust_pollen_proxy": {"stat": "dust_proxy", "kind": "ramp", "lo": 0.2, "hi": 0.8,
                              "units": "-", "season": "warm",
                              "basis": "WEAK PROXY. 10 m wind x surface dryness, gated to the "
                                       "bare-soil tillage (1 Apr-20 May), pollen (1 May-30 "
                                       "Jun) and residue-burning (1 Oct-15 Nov) windows. No "
                                       "aerosol observation is involved - see open questions."},
        "llj_speed": {"stat": "llj_max", "kind": "ramp", "lo": 12, "hi": 20,
                      "units": "m/s", "season": "warm",
                      "basis": "Bonner (1968) criterion-1 LLJ speed floor is 12 m/s; 20 m/s "
                               "is a strong Great Plains-type jet."},
        "llj_bonner": {"stat": "llj_bonner_frac", "kind": "linear", "lo": 0, "hi": 1,
                       "units": "-", "season": "warm",
                       "basis": "Fraction of array sites whose profile meets Bonner (1968) "
                                "criterion 1: max wind >=12 m/s below 1.5 km AGL falling by "
                                ">=6 m/s to the minimum above, up to 3 km."},
        "elevated_mucape": {"stat": "mucape_p90", "kind": "ramp", "lo": 500, "hi": 2000,
                            "units": "J/kg", "season": "warm",
                            "basis": "Elevated instability above the nocturnal stable layer; "
                                     "500 J/kg is the usual floor for elevated convection."},
        "stable_sfc_layer": {"stat": "sbcin_mag_p50", "kind": "ramp", "lo": 50, "hi": 200,
                             "units": "J/kg", "season": "warm",
                             "basis": "Surface-based CIN as a proxy for nocturnal decoupling, "
                                      "the regime SQ7 targets. Our reasoning."},
        "storm_area": {"stat": "core_refc40_frac", "kind": "ramp", "lo": 0.002, "hi": 0.02,
                       "units": "fraction", "season": "both",
                       "basis": "Fraction of the ARRAY BOX with composite reflectivity >=40 "
                                "dBZ. 40 dBZ is the conventional convective-core threshold. "
                                "Calibrated on two archived HRRR forecasts: 1.5 %% of the box "
                                "for the 10 Aug 2020 derecho and 2.6 %% for the 22 Feb 2023 "
                                "winter storm (a freezing-rain event, not a QLCS), so 2 %% "
                                "saturates and 0.2 %% is the detection floor."},
        "aerosol_present": {"stat": "aerosol_index", "kind": "ramp", "lo": 0.15, "hi": 1.0,
                            "units": "-", "season": "warm",
                            "basis": "Gate for the aerosol tracks: max(near-surface smoke / "
                                     "15 ug m-3, column smoke / 40 mg m-2). Saturates at a "
                                     "smoke burden that is unambiguous in HRRR-Smoke "
                                     "(64 ug m-3 / 142 mg m-2 in the 27 Jun 2023 Canadian "
                                     "smoke episode); 0.15 is the detection floor. Absent "
                                     "entirely in HRRRv3, which zeroes SQ4/SQ5 by design."},
        "winter_precip_array": {"stat": "core_wintermix_frac", "kind": "ramp",
                                "lo": 0.01, "hi": 0.12, "units": "fraction", "season": "cold",
                                "basis": "Fraction of the ARRAY BOX with HRRR categorical "
                                         "snow, sleet or freezing rain - the gate for the "
                                         "cold-season tracks: the winter event has to be "
                                         "over the array, not merely somewhere in the "
                                         "corridor. CALIBRATED ON ONE EVENT (22 Feb 2023, "
                                         "9.6 %% of the box at the peak hour) - needs a "
                                         "multi-winter climatology."},
        "fzra_over_array": {"stat": "core_fzra_frac", "kind": "ramp", "lo": 0.01, "hi": 0.10,
                            "units": "fraction", "season": "cold",
                            "basis": "Fraction of the array box with categorical freezing "
                                     "rain or ice pellets; gate for the SQ6 ice-load track."},
        "et_contrast": {"stat": "site_lhtfl_range", "kind": "ramp", "lo": 30, "hi": 150,
                        "units": "W/m2", "season": "warm",
                        "basis": "Max-min latent heat flux across the array sites - the ET "
                                 "contrast H1/H2 and SQ1 are about, measured where the "
                                 "ECOR/SEBS pairs sit. Preferred over a Bowen-ratio spread, "
                                 "which blows up when fluxes are small. Our reasoning."},
        "convective_potential": {"stat": "mlcape_p90", "kind": "ramp", "lo": 250, "hi": 1000,
                                 "units": "J/kg", "season": "warm",
                                 "basis": "Gate for SQ5: the shallow-to-deep transition can only be\n"
                                          "observed in an environment with some convective "
                                          "potential. 250 J/kg is the usual floor for "
                                          "surface-based convection."},
        "melting_energy": {"stat": "me_max", "kind": "ramp", "lo": 2, "hi": 15,
                           "units": "J/kg", "season": "cold",
                           "basis": "Bourgouin (2000) / Birk et al. (2021): the elevated warm "
                                    "layer must exceed ~2 J/kg of wet-bulb melting energy "
                                    "before freezing rain or ice pellets are forecast; mixed "
                                    "cases containing snow cluster near 10 J/kg, so 15 J/kg "
                                    "is confident complete melting."},
        "refreezing_energy": {"stat": "re_mag_max", "kind": "ramp", "lo": 5, "hi": 50,
                              "units": "J/kg", "season": "cold",
                              "basis": "Magnitude of the sub-freezing wet-bulb energy below "
                                       "the warm nose. Deep refreezing favours ice pellets "
                                       "over freezing rain (Bourgouin 2000 separation curve); "
                                       "we score the presence of the transition, not the "
                                       "category - see open questions."},
        "sfc_tw_subfreezing": {"stat": "tw2m_sub0_frac", "kind": "ramp", "lo": 0.1, "hi": 0.6,
                               "units": "fraction", "season": "cold",
                               "basis": "Freezing rain requires a sub-freezing surface wet "
                                        "bulb; fraction of the corridor with Tw(2 m) <= 0 C."},
        "fzra_qpf": {"stat": "fzra_qpf_p95", "kind": "ramp", "lo": 0.5, "hi": 3.0,
                     "units": "kg/m2/h", "season": "cold",
                     "basis": "1-h precipitation where the HRRR categorical type is freezing "
                              "rain (NOT the FROZR field, which is frozen precipitation and "
                              "is non-zero in summer graupel). NWS ice-storm warning criteria "
                              "are commonly 0.25 in (~6 mm) accretion per event, so 3 mm/h "
                              "reaches warning level within a few hours."},
        "ptype_diversity": {"stat": "n_ptypes_3pct", "kind": "linear", "lo": 1, "hi": 3,
                            "units": "count", "season": "cold",
                            "basis": "SQ3 is explicitly about snow/sleet/freezing-rain "
                                     "TRANSITIONS: number of HRRR categorical types each "
                                     "covering >=3 % of the corridor."},
        "transition_near_array": {"stat": "transition_dist_km", "kind": "ramp", "lo": 150,
                                  "hi": 25, "invert": True, "units": "km", "season": "cold",
                                  "basis": "Distance from M1 to the nearest precipitation-type "
                                           "transition boundary. 25 km puts it inside the "
                                           "M1/S1 pair; 150 km is the R1 redeployment radius."},
        "snow_insulation": {"stat": "snod_p90", "kind": "ramp", "lo": 0.02, "hi": 0.15,
                            "units": "m", "season": "cold",
                            "basis": "SQ2's frozen-soil/snow-insulation clause; ~2 cm is "
                                     "continuous cover, 15 cm decouples soil from atmosphere. "
                                     "Our reasoning."},
        "snow_cover_contrast": {"stat": "snowc_std", "kind": "ramp", "lo": 5, "hi": 30,
                                "units": "%", "season": "cold",
                                "basis": "Spatial sigma of snow-cover fraction - the albedo "
                                         "and landcover contrast SQ3 asks about."},
        "ice_wind_load": {"stat": "wind80_in_fzra_p95", "kind": "ramp", "lo": 8, "hi": 18,
                          "units": "m/s", "season": "cold",
                          "basis": "80 m wind where freezing precipitation is occurring; "
                                   "combined ice-plus-wind loading is the outage mechanism in "
                                   "SQ6. Our reasoning."},
        "cold_sfc": {"stat": "core_t2m_sub0_frac", "kind": "ramp", "lo": 0.05, "hi": 0.50,
                     "units": "fraction", "season": "cold",
                     "basis": "Fraction of the ARRAY BOX at or below 0 C at 2 m. Winter "
                              "events are narrow: 50 %% of the box sub-freezing saturates."},
    },
    # Science-question tracks.  score(SQ) = max over tracks of
    #   prod(gates) * weighted mean of predictors.
    "tracks": {
        "SQ1": {
            "convective_lifecycle": {"gates": ["storm_area"],
                "weights": {"sm_heterogeneity": 1.0, "et_contrast": 1.0, "pwat": 0.8,
                            "mlcape": 0.5, "veg_heterogeneity": 0.6,
                            "bowen_contrast": 0.5}},
            "hot_dry_bl": {"gates": ["hot_t2m"],
                "weights": {"dry_soil": 1.0, "hot_t2m": 1.0, "mixing_depth": 0.6,
                            "et_contrast": 0.8, "sm_heterogeneity": 0.8,
                            "bowen_contrast": 0.4}},
        },
        "SQ2": {
            "upscale_growth": {"gates": ["storm_area"],
                "weights": {"sigsvr": 1.0, "deep_shear": 0.8, "mlcape": 0.6,
                            "sm_heterogeneity": 1.0, "et_contrast": 0.8,
                            "veg_heterogeneity": 0.5}},
            "frozen_surface_fluxes": {"gates": ["winter_precip_array"],
                "weights": {"snow_insulation": 1.0, "snow_cover_contrast": 0.8,
                            "sm_heterogeneity": 0.6, "fzra_qpf": 0.8, "cold_sfc": 0.6}},
        },
        "SQ3": {
            "winter_transition": {"gates": ["winter_precip_array"],
                "weights": {"melting_energy": 1.0, "refreezing_energy": 0.8,
                            "sfc_tw_subfreezing": 1.0, "ptype_diversity": 1.0,
                            "transition_near_array": 1.0, "snow_cover_contrast": 0.5,
                            "cold_sfc": 0.6}},
        },
        "SQ4": {
            "aerosol_convection": {"gates": ["storm_area", "aerosol_present"],
                "require_any": ["smoke_near_sfc", "smoke_column"],
                "weights": {"smoke_column": 1.0, "smoke_near_sfc": 0.8,
                            "dust_pollen_proxy": 0.6, "pwat": 0.5, "mlcape": 0.4,
                            "veg_heterogeneity": 0.5}},
        },
        "SQ5": {
            "aerosol_prestorm_bl": {"gates": ["aerosol_present"],
                "require_any": ["smoke_near_sfc", "smoke_column"],
                "weights": {"smoke_near_sfc": 1.0, "smoke_column": 0.8,
                            "cin_capping": 1.0, "mixing_depth": 0.8, "mlcape": 0.5,
                            "dust_pollen_proxy": 0.6, "convective_potential": 0.6}},
        },
        "SQ6": {
            "damaging_wind": {"gates": ["storm_area"],
                "weights": {"dcp": 1.0, "dcape": 0.8, "gust": 1.0, "wind80": 1.0,
                            "meanwind06": 0.6, "deep_shear": 0.6, "srh01": 0.4}},
            "ice_load": {"gates": ["fzra_over_array"],
                "weights": {"fzra_qpf": 1.0, "ice_wind_load": 1.0, "melting_energy": 0.6,
                            "sfc_tw_subfreezing": 0.8}},
        },
        "SQ7": {
            "nocturnal_llj": {"gates": ["is_night"],
                "weights": {"llj_speed": 1.0, "llj_bonner": 1.0, "elevated_mucape": 0.8,
                            "stable_sfc_layer": 0.6, "sm_heterogeneity": 0.8,
                            "et_contrast": 0.4, "deep_shear": 0.4}},
        },
    },
    "gates": {
        "is_night": {"utc_start": 3, "utc_end": 12,
                     "basis": "03-12 UTC is 21-06 local standard time in the domain: the "
                              "nocturnal LLJ / overnight-MCS window SQ7 targets."},
    },
    "aggregate": {
        "sq_weights": {"SQ1": 1.0, "SQ2": 1.0, "SQ3": 1.0, "SQ4": 1.0, "SQ5": 1.0,
                       "SQ6": 1.2, "SQ7": 1.0},
        "sq_weight_basis": "Equal by default; SQ6 up-weighted because the ARM workshop "
                           "report (Mather et al. 2026) ranks severe convective winds and "
                           "grid impact first. A campaign-lead decision.",
        "saturation_tau": 2.5,
        "saturation_basis": "Campaign utility per SQ is 1-exp(-C/tau) with C the summed "
                            "score of IOPs already captured; tau=2.5 means ~3 good IOPs "
                            "capture ~70 % of the attainable value for one SQ.",
        "value_metric": "marginal_utility",
    },
    "operations": {
        "iops_per_year": 10,
        "sounding_lead_h": 24,
        "sounding_cadence_h": 3,
        "iop_sounding_window_h": 12,
        "module_dwell_days_min": 7,
        "module_break_days_min": 3,
        "module_break_score": 0.25,
        "module_radius_km": 150,
        "score_prior": {"a": 1.2, "b": 12.0},
        "score_prior_basis": "PLACEHOLDER Beta(1.2,12) prior for the distribution of daily "
                             "iop_value (mean 0.09, 94.5th percentile 0.24). Located so "
                             "that (a) the implied selection rate matches 10 IOPs per "
                             "~180-day season, i.e. the top ~5.5 % of days, and (b) the "
                             "10 Aug 2020 derecho (value 0.41 over a 06Z+18Z window) is a "
                             "clear GO in mid-season while a 0.15 day is not. Replace with "
                             "a multi-year HRRR/ERA5 climatology of iop_value over the "
                             "domain before this drives real calls - see open question 1.",
    },
}

IOP_ARCHETYPES = ["freezing_rain", "winter_transition", "winter_snow_wind",
                  "warm_qlcs_derecho", "nocturnal_llj_mcs", "hot_dry_bl",
                  "aerosol_perturbed_convection", "aerosol_perturbed_bl",
                  "generic_convective", "null"]


# ------------------------------------------------------------------ config ---

def iop_config(overrides=None):
    """Return a deep copy of the scorecard config, optionally deep-merged with
    `overrides` (a dict, or a path to a JSON file written by iop_dump_config)."""
    import copy, json, os
    cfg = copy.deepcopy(DERECHOS_IOP_CONFIG)
    if overrides is None:
        return cfg
    if isinstance(overrides, str):
        if not os.path.exists(overrides):
            raise FileNotFoundError(overrides)
        overrides = json.load(open(overrides))

    def merge(a, b):
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                merge(a[k], v)
            else:
                a[k] = v
    merge(cfg, overrides)
    return cfg


def iop_dump_config(path="derechos_iop_config.json", config=None):
    """Write the active config to JSON so a campaign lead can edit thresholds."""
    import json
    json.dump(config or DERECHOS_IOP_CONFIG, open(path, "w"), indent=1, sort_keys=True)
    return path


def iop_predictor_table(config=None):
    """Predictor -> science-question traceability table (list of dicts)."""
    cfg = config or DERECHOS_IOP_CONFIG
    rows = []
    for name, p in cfg["predictors"].items():
        sqs = {}
        for sq, tracks in cfg["tracks"].items():
            for tname, t in tracks.items():
                if name in t["weights"]:
                    sqs.setdefault(sq, []).append("%s(w=%.1f)" % (tname, t["weights"][name]))
                if name in t.get("gates", []):
                    sqs.setdefault(sq, []).append("%s(GATE)" % tname)
        rows.append(dict(predictor=name, statistic=p["stat"], units=p.get("units"),
                         season=p.get("season"), kind=p["kind"],
                         lo=p.get("lo"), hi=p.get("hi"),
                         optional=bool(p.get("optional")),
                         science_questions=sqs, basis=p["basis"]))
    return sorted(rows, key=lambda r: (r["season"] or "", r["predictor"]))


# ---------------------------------------------------------------- ramps -----

def iop_ramp(x, lo, hi):
    """Linear 0->1 ramp between lo and hi (works if hi < lo, i.e. inverted)."""
    if x is None:
        return None
    if hi == lo:
        return 1.0 if x >= lo else 0.0
    v = (float(x) - lo) / (hi - lo)
    return max(0.0, min(1.0, v))


def iop_trapezoid(x, lo, lo2, hi2, hi):
    """0 below lo, 1 between lo2 and hi2, 0 above hi."""
    if x is None:
        return None
    x = float(x)
    if x <= lo or x >= hi:
        return 0.0
    if x < lo2:
        return (x - lo) / (lo2 - lo)
    if x <= hi2:
        return 1.0
    return (hi - x) / (hi - hi2)


def iop_predictor_value(name, summary, config=None):
    """Scaled 0-1 value of one predictor, or None if its statistic is missing."""
    cfg = config or DERECHOS_IOP_CONFIG
    p = cfg["predictors"][name]
    x = summary.get(p["stat"])
    if x is None:
        return None
    try:
        if x != x:      # NaN
            return None
    except TypeError:
        return None
    if p["kind"] == "trap":
        return iop_trapezoid(x, p["lo"], p["lo2"], p["hi2"], p["hi"])
    return iop_ramp(x, p["lo"], p["hi"])


# ------------------------------------------------------- HRRR ingest --------

def iop_hrrr_url(date, run, fxx, product="sfc"):
    return ("https://noaa-hrrr-bdp-pds.s3.amazonaws.com/hrrr.%s/conus/"
            "hrrr.t%02dz.wrf%sf%02d.grib2" % (date, run, product, fxx))


def iop_hrrr_idx(date, run, fxx, product="sfc"):
    """Parse the .idx sidecar -> [{n, start, end, desc}]."""
    import urllib.request
    url = iop_hrrr_url(date, run, fxx, product) + ".idx"
    with urllib.request.urlopen(url, timeout=120) as r:
        lines = [l for l in r.read().decode().splitlines() if l.strip()]
    starts = [int(l.split(":")[1]) for l in lines]
    out = []
    for i, l in enumerate(lines):
        p = l.split(":")
        out.append(dict(n=int(p[0]), start=starts[i],
                        end=(starts[i + 1] - 1 if i + 1 < len(lines) else None),
                        desc=":".join(p[3:])))
    return out


def iop_hrrr_messages(date, run, fxx, product, wanted, workers=16):
    """One ranged GET per wanted GRIB message.  wanted = [(regex, name), ...]."""
    import re, urllib.request
    from concurrent.futures import ThreadPoolExecutor
    rows = iop_hrrr_idx(date, run, fxx, product)
    url = iop_hrrr_url(date, run, fxx, product)
    jobs = []
    for pat, name in wanted:
        for r in rows:
            if re.search(pat, r["desc"]):
                jobs.append((name, r))
                break

    def one(job):
        name, r = job
        hdr = {"Range": "bytes=%d-%s" % (r["start"], "" if r["end"] is None else r["end"])}
        req = urllib.request.Request(url, headers=hdr)
        with urllib.request.urlopen(req, timeout=240) as resp:
            return name, resp.read()
    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, jobs))


def iop_grib_decode(blob):
    """One GRIB2 message -> (values2d, lats2d, lons2d)."""
    import numpy as np, eccodes as ec
    gid = ec.codes_new_from_message(blob)
    try:
        ni, nj = ec.codes_get(gid, "Ni"), ec.codes_get(gid, "Nj")
        vals = ec.codes_get_values(gid).reshape(nj, ni)
        lats = ec.codes_get_array(gid, "latitudes").reshape(nj, ni)
        lons = ec.codes_get_array(gid, "longitudes").reshape(nj, ni)
    finally:
        ec.codes_release(gid)
    return vals, lats, np.where(lons > 180, lons - 360, lons)


def iop_fetch_hrrr_sfc(date, run, fxx, box=None):
    """Surface/derived HRRR fields over the DERECHOS corridor as an xr.Dataset.

    date 'YYYYMMDD', run/fxx integers.  box defaults to DERECHOS_CORRIDOR.
    Missing fields (HRRRv3 has no VEG/LAI/MASSDEN/COLMD) are simply absent.
    """
    import numpy as np, xarray as xr
    box = box or DERECHOS_CORRIDOR
    blobs = iop_hrrr_messages(date, run, fxx, "sfc",
                              [(p, n) for p, n, _ in HRRR_SFC_FIELDS])
    data, lats, lons = {}, None, None
    for name, blob in blobs.items():
        v, la, lo = iop_grib_decode(blob)
        if lats is None:
            lats, lons = la, lo
        data[name] = v
    m = ((lats >= box["lat"][0]) & (lats <= box["lat"][1]) &
         (lons >= box["lon"][0]) & (lons <= box["lon"][1]))
    jj, ii = np.where(m.any(axis=1))[0], np.where(m.any(axis=0))[0]
    sl = (slice(jj.min(), jj.max() + 1), slice(ii.min(), ii.max() + 1))
    ds = xr.Dataset({k: (("y", "x"), v[sl]) for k, v in data.items()},
                    coords=dict(lat=(("y", "x"), lats[sl]), lon=(("y", "x"), lons[sl])))
    ds.attrs.update(hrrr_run="%s t%02dz" % (date, run), fxx=int(fxx),
                    source=iop_hrrr_url(date, run, fxx, "sfc"))
    return ds


def iop_fetch_hrrr_columns(date, run, fxx, sites=None):
    """Isobaric HGT/TMP/RH/UGRD/VGRD columns (1000-500 hPa) at the array sites."""
    import re, math, numpy as np, xarray as xr
    sites = sites or DERECHOS_IOP_SITES
    rows = iop_hrrr_idx(date, run, fxx, "prs")
    wanted = []
    for r in rows:
        m = re.match(HRRR_PRS_RE, r["desc"])
        if m:
            wanted.append((r"^%s:%s mb:" % (m.group(1), m.group(2)),
                           "%s_%s" % (m.group(1).lower(), m.group(2))))
    blobs = iop_hrrr_messages(date, run, fxx, "prs", wanted)
    fields, lats, lons = {}, None, None
    for name, blob in blobs.items():
        v, la, lo = iop_grib_decode(blob)
        if lats is None:
            lats, lons = la, lo
        fields[name] = v
    levs = sorted({int(k.split("_")[1]) for k in fields}, reverse=True)
    cols = {}
    for site, (la, lo) in sites.items():
        d = (lats - la) ** 2 + ((lons - lo) * math.cos(math.radians(la))) ** 2
        j, i = np.unravel_index(np.argmin(d), d.shape)
        for v in ("hgt", "tmp", "rh", "ugrd", "vgrd"):
            cols["%s_%s" % (site, v)] = ("level", np.array(
                [float(fields["%s_%d" % (v, L)][j, i]) for L in levs]))
        cols["%s_latlon" % site] = ("pair", np.array([lats[j, i], lons[j, i]]))
    out = xr.Dataset(cols, coords=dict(level=np.array(levs, float)))
    out.attrs.update(hrrr_run="%s t%02dz" % (date, run), fxx=int(fxx))
    return out


# ------------------------------------------------------- profile diagnostics -

def iop_profile_diagnostics(prs, site, psfc_pa=None):
    """MetPy-based column diagnostics at one array site.

    Returns DCAPE, 0-6 km mean wind, LLJ speed/Bonner flag, and the Bourgouin
    wet-bulb melting (ME) and refreezing (RE) energies in J/kg.
    """
    import numpy as np
    from metpy.units import units
    import metpy.calc as mpcalc
    lev = prs["level"].values.astype(float)
    z = prs["%s_hgt" % site].values.astype(float)
    t = prs["%s_tmp" % site].values.astype(float)
    rh = np.clip(prs["%s_rh" % site].values.astype(float), 1.0, 100.0)
    u = prs["%s_ugrd" % site].values.astype(float)
    v = prs["%s_vgrd" % site].values.astype(float)
    order = np.argsort(-lev)                      # descending pressure
    lev, z, t, rh, u, v = [a[order] for a in (lev, z, t, rh, u, v)]
    keep = np.ones(lev.shape, bool)
    if psfc_pa is not None:
        keep = lev <= psfc_pa / 100.0 + 1e-6
    lev, z, t, rh, u, v = [a[keep] for a in (lev, z, t, rh, u, v)]
    out = {}
    if lev.size < 5:
        return out
    p = lev * units.hPa
    T = t * units.kelvin
    Td = mpcalc.dewpoint_from_relative_humidity(T, rh / 100.0 * units.dimensionless)
    zagl = z - z[0]
    spd = np.hypot(u, v)
    try:
        dc = mpcalc.downdraft_cape(p, T, Td)[0]
        out["dcape"] = float(np.abs(dc.to("J/kg").magnitude))
    except Exception as exc:
        out["dcape_error"] = str(exc)[:120]
    low = zagl <= 6000
    if low.sum() >= 2:
        out["meanwind06"] = float(np.mean(spd[low]))
    jet = zagl <= 1500
    if jet.sum() >= 2:
        k = int(np.argmax(np.where(jet, spd, -1)))
        out["llj_speed"] = float(spd[k])
        above = (zagl > zagl[k]) & (zagl <= 3000)
        out["llj_bonner"] = bool(spd[k] >= 12.0 and above.any() and
                                 (spd[k] - float(np.min(spd[above]))) >= 6.0)
    # Bourgouin wet-bulb areas.  MetPy supplies Tw; the area integral
    # ME = R_d * int (Tw - 273.15) d(ln p) has no MetPy equivalent.
    try:
        tw = mpcalc.wet_bulb_temperature(p, T, Td).to("kelvin").magnitude
    except Exception as exc:
        out["wetbulb_error"] = str(exc)[:120]
        return out
    out["tw_sfc_c"] = float(tw[0] - 273.15)
    lnp = np.log(lev)
    dtw = tw - 273.15
    rd = 287.05

    def area(i0, i1, sign):
        """R_d * int (Tw-273.15) dlnp over levels i0..i1, keeping one sign."""
        tot = 0.0
        for i in range(i0, i1):
            seg = rd * 0.5 * (dtw[i] + dtw[i + 1]) * (lnp[i] - lnp[i + 1])
            if sign > 0:
                tot += max(seg, 0.0)
            else:
                tot += min(seg, 0.0)
        return tot

    warm = dtw > 0.0
    runs, i = [], 0
    n = len(dtw)
    while i < n:
        if warm[i]:
            j = i
            while j + 1 < n and warm[j + 1]:
                j += 1
            runs.append((i, j))
            i = j + 1
        else:
            i += 1
    elevated = [r for r in runs if r[0] > 0 and zagl[r[0]] > 100.0]
    if elevated:
        b, t_ = elevated[0]
        out["me"] = float(area(b, t_, +1))
        out["re_mag"] = float(abs(area(0, b, -1)))
        out["warm_nose"] = bool(dtw[0] <= 0.5)
        out["warm_nose_base_m"] = float(zagl[b])
        out["warm_nose_max_tw_c"] = float(np.max(dtw[b:t_ + 1]))
    else:
        out["me"], out["re_mag"], out["warm_nose"] = 0.0, 0.0, False
    return out


def iop_site_index(sfc, lat, lon):
    import math, numpy as np
    la, lo = sfc["lat"].values, sfc["lon"].values
    d = (la - lat) ** 2 + ((lo - lon) * math.cos(math.radians(lat))) ** 2
    return np.unravel_index(np.argmin(d), d.shape)


def iop_summarize(sfc, prs=None, valid_time=None, config=None, tw_stride=3,
                  sites=None):
    """Reduce a gridded forecast over the corridor to the scorecard statistics.

    sfc : xr.Dataset of 2-D fields named as in HRRR_SFC_FIELDS, with 2-D
          `lat`/`lon` coords.  Units: K, m/s, J/kg, W/m2, Pa, kg/m2, %, m.
    prs : optional xr.Dataset of site columns from iop_fetch_hrrr_columns.
    valid_time : datetime or ISO string of the forecast VALID time (UTC).
    Returns a flat dict of named statistics (the `stat` keys of the predictors)
    plus `missing_fields`, `sites`, and diagnostic extras.
    """
    import datetime as dt, numpy as np
    from metpy.units import units
    import metpy.calc as mpcalc
    cfg = config or DERECHOS_IOP_CONFIG
    sites = sites or DERECHOS_IOP_SITES
    have = set(sfc.data_vars)
    s = {}

    def arr(name):
        return sfc[name].values.astype("float64") if name in have else None

    def pct(a, q):
        return float(np.nanpercentile(a, q)) if a is not None else None

    if isinstance(valid_time, str):
        valid_time = dt.datetime.fromisoformat(valid_time.replace("Z", ""))
    s["valid_time"] = valid_time.isoformat() if valid_time else None

    mlcape, mucape, sbcape = arr("mlcape"), arr("mucape"), arr("sbcape")
    s["mlcape_p90"], s["mucape_p90"] = pct(mlcape, 90), pct(mucape, 90)
    s["sbcape_p90"] = pct(sbcape, 90)
    mlcin, sbcin = arr("mlcin"), arr("sbcin")
    if mlcin is not None and mlcape is not None:
        m = mlcape > 250
        s["mlcin_mag_p50"] = float(np.nanmedian(np.abs(mlcin[m]))) if m.any() else 0.0
    if sbcin is not None and mucape is not None:
        m = mucape > 250
        s["sbcin_mag_p50"] = float(np.nanmedian(np.abs(sbcin[m]))) if m.any() else 0.0

    if arr("ushr06") is not None:
        shr06 = mpcalc.wind_speed(arr("ushr06") * units("m/s"),
                                  arr("vshr06") * units("m/s")).magnitude
        s["shear06_p90"] = pct(shr06, 90)
        if mlcape is not None:
            s["sigsvr_p90"] = pct(mlcape * shr06, 90)
    else:
        shr06 = None
    if arr("ushr01") is not None:
        s["shear01_p90"] = pct(mpcalc.wind_speed(arr("ushr01") * units("m/s"),
                                                 arr("vshr01") * units("m/s")).magnitude, 90)
    s["srh01_p90"] = pct(arr("srh01"), 90)
    s["srh03_p90"] = pct(arr("srh03"), 90)
    s["gust_p99"] = pct(arr("gust"), 99)
    s["gust_p999"] = pct(arr("gust"), 99.9)
    w80 = None
    if arr("u80") is not None:
        w80 = np.hypot(arr("u80"), arr("v80"))
        s["wind80_p99"] = pct(w80, 99)
        s["wind80_p999"] = pct(w80, 99.9)
    w10 = np.hypot(arr("u10"), arr("v10")) if arr("u10") is not None else None
    s["wind10_p90"] = pct(w10, 90)
    s["pwat_p90"] = pct(arr("pwat"), 90)
    s["hpbl_p90"] = pct(arr("hpbl"), 90)

    t2m, d2m, psfc = arr("t2m"), arr("d2m"), arr("psfc")
    if t2m is not None:
        s["t2m_p90_c"] = pct(t2m, 90) - 273.15
        s["t2m_sub0_frac"] = float(np.mean(t2m <= 273.15))
    mstav = arr("mstav")
    if mstav is not None:
        s["mstav_mean"], s["mstav_std"] = float(np.nanmean(mstav)), float(np.nanstd(mstav))
    sh, lh = arr("shtfl"), arr("lhtfl")
    if sh is not None and lh is not None:
        m = np.abs(lh) > 20
        if m.any():
            s["bowen_std"] = float(np.nanstd(np.clip(sh[m] / lh[m], -5, 5)))
            s["bowen_mean"] = float(np.nanmean(np.clip(sh[m] / lh[m], -5, 5)))
    if arr("lai") is not None:
        s["lai_std"] = float(np.nanstd(arr("lai")))
    # HRRR writes MASSDEN/COLMD with a version-dependent decimal scale factor:
    # 2021-12-15 comes back in ug/m3 (values 0.02-0.3), 2023-02-22 in kg/m3
    # (1e-10) for the same ~0.2 ug/m3 air.  Infer from magnitude and record it.
    if arr("massden") is not None:
        x = pct(arr("massden"), 99)
        s["massden_units_assumed"] = "ug/m3" if x > 1e-3 else "kg/m3"
        s["massden_p99_ugm3"] = x if x > 1e-3 else x * 1e9
    if arr("colmd") is not None:
        x = pct(arr("colmd"), 99)
        s["colmd_units_assumed"] = "mg/m2" if x > 1e-2 else "kg/m2"
        s["colmd_p99_mgm2"] = x if x > 1e-2 else x * 1e6
    ax = []
    if s.get("massden_p99_ugm3") is not None:
        ax.append(s["massden_p99_ugm3"] / 15.0)
    if s.get("colmd_p99_mgm2") is not None:
        ax.append(s["colmd_p99_mgm2"] / 40.0)
    if ax:
        s["aerosol_index"] = float(max(ax))
    if arr("refc") is not None:
        s["refc40_frac"] = float(np.mean(arr("refc") >= 40))
        s["refc_max"] = float(np.nanmax(arr("refc")))
    if arr("apcp1h") is not None:
        s["apcp1mm_frac"] = float(np.mean(arr("apcp1h") >= 1.0))

    # gates are evaluated over the array box, not the whole corridor
    la2, lo2 = sfc["lat"].values, sfc["lon"].values
    core = ((la2 >= DERECHOS_ARRAY_BOX["lat"][0]) & (la2 <= DERECHOS_ARRAY_BOX["lat"][1]) &
            (lo2 >= DERECHOS_ARRAY_BOX["lon"][0]) & (lo2 <= DERECHOS_ARRAY_BOX["lon"][1]))
    s["core_npts"] = int(core.sum())
    if arr("refc") is not None and core.any():
        s["core_refc40_frac"] = float(np.mean(arr("refc")[core] >= 40))
    if t2m is not None and core.any():
        s["core_t2m_sub0_frac"] = float(np.mean(t2m[core] <= 273.15))
    if arr("apcp1h") is not None and core.any():
        s["core_apcp1mm_frac"] = float(np.mean(arr("apcp1h")[core] >= 1.0))
    s["core_mask_sum"] = int(core.sum())

    # array-site contrasts: what the ECOR/SEBS/SoilVue pairs would actually see
    site_stats = {}
    for name, (la, lo) in sites.items():
        j, i = iop_site_index(sfc, la, lo)
        d = {}
        for v in ("mstav", "t2m", "shtfl", "lhtfl", "hpbl", "snod", "lai"):
            if v in have:
                d[v] = float(sfc[v].values[j, i])
        if "shtfl" in d and "lhtfl" in d and abs(d["lhtfl"]) > 20:
            d["bowen"] = max(-5.0, min(5.0, d["shtfl"] / d["lhtfl"]))
        site_stats[name] = d
    s["site_stats"] = site_stats
    for key, out in (("mstav", "site_mstav_range"), ("bowen", "site_bowen_range"),
                     ("lhtfl", "site_lhtfl_range"), ("hpbl", "site_hpbl_range")):
        vals = [d[key] for d in site_stats.values() if key in d]
        if len(vals) >= 2:
            s[out] = float(max(vals) - min(vals))

    # winter precipitation type structure
    ptypes, labels = {}, ["csnow", "cicep", "cfrzr", "crain"]
    for k in labels:
        a = arr(k)
        if a is not None:
            ptypes[k] = a > 0.5
            s["%s_frac" % k] = float(np.mean(ptypes[k]))
    if ptypes:
        mix = np.zeros(list(ptypes.values())[0].shape, bool)
        for k in ("csnow", "cicep", "cfrzr"):
            if k in ptypes:
                mix |= ptypes[k]
        icy = np.zeros(mix.shape, bool)
        for k in ("cicep", "cfrzr"):
            if k in ptypes:
                icy |= ptypes[k]
        s["core_wintermix_frac"] = float(np.mean(mix[core]))
        s["core_fzra_frac"] = float(np.mean(icy[core]))
        s["n_ptypes_3pct"] = int(sum(1 for k, v in ptypes.items() if v.mean() >= 0.03))
        s["transition_dist_km"] = iop_transition_distance(sfc, ptypes, sites.get("M1"))
    # Freezing-rain QPF from the categorical type, NOT from FROZR: HRRR's FROZR
    # is frozen precipitation (non-zero in summer graupel, verified on the
    # 10 Aug 2020 derecho at +20 C with zero CFRZR overlap).
    apcp = arr("apcp1h")
    if apcp is not None and ptypes.get("cfrzr") is not None:
        cf = ptypes["cfrzr"]
        s["fzra_qpf_p95"] = float(np.nanpercentile(apcp[cf], 95)) if cf.sum() >= 5 else 0.0
        s["fzra_qpf_max"] = float(np.nanmax(apcp[cf])) if cf.sum() else 0.0
    fz = arr("frozr1h")
    if fz is not None:
        nz = fz[fz > 0.05]
        s["frozr_p95_frozenprecip"] = float(np.nanpercentile(nz, 95)) if nz.size >= 5 else 0.0
        s["frozr_area_frac"] = float(np.mean(fz > 0.05))
    if w80 is not None and ptypes.get("cfrzr") is not None:
        icy = ptypes["cfrzr"] | ptypes.get("cicep", ptypes["cfrzr"])
        s["wind80_in_fzra_p95"] = float(np.nanpercentile(w80[icy], 95)) if icy.sum() >= 5 else None
    if arr("snod") is not None:
        s["snod_p90"] = pct(arr("snod"), 90)
    if arr("snowc") is not None:
        s["snowc_std"] = float(np.nanstd(arr("snowc")))
        s["snowc_mean"] = float(np.nanmean(arr("snowc")))

    # 2 m wet bulb (MetPy, strided - the iterative solver is expensive)
    if t2m is not None and d2m is not None and psfc is not None:
        sl = (slice(None, None, tw_stride), slice(None, None, tw_stride))
        tw = mpcalc.wet_bulb_temperature(psfc[sl] * units.Pa, t2m[sl] * units.kelvin,
                                         d2m[sl] * units.kelvin).to("kelvin").magnitude
        s["tw2m_sub0_frac"] = float(np.mean(tw <= 273.15))
        s["tw2m_min_c"] = float(np.nanmin(tw) - 273.15)
        s["tw_stride"] = tw_stride

    # aerosol season proxy (no aerosol observation involved)
    if valid_time is not None and mstav is not None and w10 is not None:
        s["dust_proxy"] = iop_dust_proxy(valid_time, s["wind10_p90"], s["mstav_mean"])

    # profile diagnostics at the array sites
    if prs is not None:
        prof, dcps = {}, []
        for site in sites:
            if "%s_tmp" % site not in prs.data_vars:
                continue
            j, i = iop_site_index(sfc, *sites[site])
            ps = float(psfc[j, i]) if psfc is not None else None
            d = iop_profile_diagnostics(prs, site, ps)
            if mucape is not None:
                d["mucape_site"] = float(mucape[j, i])
            if shr06 is not None:
                d["shear06_site"] = float(shr06[j, i])
            if all(k in d for k in ("dcape", "meanwind06", "mucape_site", "shear06_site")):
                d["dcp"] = ((d["dcape"] / 980.0) * (d["mucape_site"] / 2000.0) *
                            (d["shear06_site"] / 10.29) * (d["meanwind06"] / 8.23))
                dcps.append(d["dcp"])
            prof[site] = d
        s["profiles"] = prof
        def gather(key):
            return [v[key] for v in prof.values() if key in v and v[key] is not None]
        for key, out in (("dcape", "dcape_max"), ("meanwind06", "meanwind06_max"),
                         ("llj_speed", "llj_max"), ("me", "me_max"), ("re_mag", "re_mag_max")):
            vals = gather(key)
            if vals:
                s[out] = float(max(vals))
        if dcps:
            s["dcp_max"] = float(max(dcps))
        bon = [1.0 if v.get("llj_bonner") else 0.0 for v in prof.values() if "llj_speed" in v]
        if bon:
            s["llj_bonner_frac"] = float(sum(bon) / len(bon))

    s["missing_fields"] = sorted({n for _, n, _ in HRRR_SFC_FIELDS} - have)
    return s


def iop_transition_distance(sfc, ptypes, m1):
    """Distance (km) from M1 to the nearest precipitation-type transition point."""
    import numpy as np
    from scipy.ndimage import maximum_filter
    keys = [k for k, v in ptypes.items() if v.mean() >= 0.005]
    if len(keys) < 2 or m1 is None:
        return None
    dil = {k: maximum_filter(ptypes[k].astype(np.uint8), size=5) > 0 for k in keys}
    trans = np.zeros(ptypes[keys[0]].shape, bool)
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            trans |= dil[keys[a]] & dil[keys[b]]
    if not trans.any():
        return None
    la, lo = sfc["lat"].values, sfc["lon"].values
    d = np.hypot((la - m1[0]) * 111.2, (lo - m1[1]) * 111.2 * np.cos(np.radians(la)))
    return float(np.nanmin(d[trans]))


def iop_dust_proxy(valid_time, wind10_p90, mstav_mean):
    """Calendar+surface-state proxy for managed-ecosystem aerosol source strength.

    WEAK: no aerosol measurement or model aerosol field is used.  Season windows
    are bare-soil tillage (1 Apr-20 May), pollen (1 May-30 Jun) and post-harvest
    residue burning (1 Oct-15 Nov).
    """
    doy = valid_time.timetuple().tm_yday
    windows = [(91, 140), (121, 181), (274, 319)]
    season = 1.0 if any(a <= doy <= b for a, b in windows) else 0.25
    if wind10_p90 is None or mstav_mean is None:
        return None
    wind = iop_ramp(wind10_p90, 5.0, 12.0)
    dry = iop_ramp(1.0 - mstav_mean / 100.0, 0.35, 0.70)
    return float(season * wind * dry)


# ------------------------------------------------------------------ scoring --

def iop_score(summary, config=None, valid_time=None):
    """Per-science-question scores from a summary dict (see iop_summarize).

    Returns {sq_scores, tracks, predictors, archetype, gates, dropped, ...}.
    Each SQ score is max over its tracks of  prod(gates) * weighted-mean(predictors).
    """
    import datetime as dt
    cfg = config or DERECHOS_IOP_CONFIG
    vt = valid_time or summary.get("valid_time")
    if isinstance(vt, str):
        vt = dt.datetime.fromisoformat(vt.replace("Z", ""))
    pv, dropped = {}, []
    for name in cfg["predictors"]:
        v = iop_predictor_value(name, summary, cfg)
        pv[name] = v
        if v is None:
            dropped.append(name)
    gates = {}
    gcfg = cfg["gates"]["is_night"]
    gates["is_night"] = (1.0 if (vt is not None and
                                 gcfg["utc_start"] <= vt.hour <= gcfg["utc_end"]) else 0.0)
    sq_scores, tracks = {}, {}
    for sq, tdefs in cfg["tracks"].items():
        best, bestname, detail = 0.0, None, {}
        for tname, t in tdefs.items():
            g = 1.0
            gvals = {}
            for gname in t.get("gates", []):
                gv = gates.get(gname, pv.get(gname))
                gv = 0.0 if gv is None else gv
                gvals[gname] = gv
                g *= gv
            req = t.get("require_any")
            if req and all(pv.get(r) is None for r in req):
                detail[tname] = dict(score=0.0, gate=0.0, gates=gvals, core=0.0,
                                     completeness=0.0,
                                     blocked="no data for any of %s" % ", ".join(req))
                continue
            num = den = avail = total = 0.0
            for pname, w in t["weights"].items():
                total += w
                v = pv.get(pname)
                if v is None:
                    continue
                avail += w
                num += w * v
                den += w
            core = (num / den) if den > 0 else 0.0
            sc = g * core
            detail[tname] = dict(score=sc, gate=g, gates=gvals, core=core,
                                 completeness=(avail / total if total else 0.0))
            if sc > best:
                best, bestname = sc, tname
        sq_scores[sq] = round(best, 4)
        tracks[sq] = dict(best_track=bestname, detail=detail)
    arch = iop_classify(summary, sq_scores, cfg)
    return dict(sq_scores=sq_scores, tracks=tracks, predictors=pv, gates=gates,
                dropped_predictors=dropped, archetype=arch[0], archetype_reason=arch[1],
                served_sqs=[k for k, v in sq_scores.items() if v >= 0.5],
                valid_time=(vt.isoformat() if vt else None),
                missing_fields=summary.get("missing_fields", []),
                summary=summary)


def iop_classify(summary, sq_scores, config=None):
    """Label the candidate IOP with an archetype (which kind of IOP it would be)."""
    g = summary.get
    cold = (g("core_t2m_sub0_frac") or 0) >= 0.05
    fz = (g("fzra_qpf_p95") or 0) >= 0.5 or (g("cfrzr_frac") or 0) >= 0.02
    n_pt = g("n_ptypes_3pct") or 0
    storm = (g("core_refc40_frac") or 0) >= 0.01
    if cold and fz and (g("me_max") or 0) >= 2:
        return "freezing_rain", "cold surface, freezing-rain QPF, elevated melting energy"
    if cold and n_pt >= 3:
        return "winter_transition", "three or more precipitation types over the corridor"
    if cold and (g("csnow_frac") or 0) >= 0.05 and (g("wind80_p99") or 0) >= 15:
        return "winter_snow_wind", "widespread snow with strong 80 m wind"
    if storm and (g("dcp_max") or 0) >= 1.0 and (g("gust_p99") or 0) >= 25:
        return "warm_qlcs_derecho", "DCP >= 1 with severe forecast gusts"
    if sq_scores.get("SQ7", 0) >= 0.5 and (g("llj_max") or 0) >= 12:
        return "nocturnal_llj_mcs", "nocturnal low-level jet with elevated instability"
    if (g("t2m_p90_c") or -99) >= 30 and (g("mstav_mean") or 100) <= 45:
        return "hot_dry_bl", "hot, dry-soil boundary layer (SQ1 energy-demand regime)"
    if storm and max(sq_scores.get("SQ4", 0), sq_scores.get("SQ5", 0)) >= 0.5:
        return "aerosol_perturbed_convection", "convection with an elevated aerosol burden"
    if (g("aerosol_index") or 0) >= 1.0 and sq_scores.get("SQ5", 0) >= 0.3:
        return "aerosol_perturbed_bl", ("smoke- or dust-laden boundary layer (aerosol "
                                       "index >= 1) without convection over the array")
    if storm:
        return "generic_convective", "convection present but no hazard signature dominant"
    return "null", "no convective or winter-precipitation signal in the corridor"


# ------------------------------------------------- campaign value & budget ---

def iop_campaign_utility(log, config=None):
    """Saturating campaign utility in [0,1] from a log of captured IOPs.

    log : list of per-IOP sq_score dicts (or dicts containing 'sq_scores').
    U = sum_SQ w_SQ (1 - exp(-C_SQ/tau)) / sum_SQ w_SQ, C_SQ = summed scores.
    """
    import math
    cfg = config or DERECHOS_IOP_CONFIG
    w = cfg["aggregate"]["sq_weights"]
    tau = cfg["aggregate"]["saturation_tau"]
    acc = {k: 0.0 for k in w}
    for e in (log or []):
        d = e.get("sq_scores", e)
        for k in acc:
            acc[k] += float(d.get(k, 0.0))
    num = sum(w[k] * (1.0 - math.exp(-acc[k] / tau)) for k in w)
    return num / sum(w.values()), acc


def iop_value(sq_scores, log=None, config=None):
    """Marginal campaign value of one candidate IOP, raw and normalised to [0,1].

    Normalisation is against a hypothetical IOP scoring 1.0 on every SQ given the
    same log, so that a fresh SQ is worth more than a fourth repeat of one.
    """
    cfg = config or DERECHOS_IOP_CONFIG
    u0, _ = iop_campaign_utility(log, cfg)
    u1, _ = iop_campaign_utility(list(log or []) + [{"sq_scores": sq_scores}], cfg)
    ones = {k: 1.0 for k in cfg["aggregate"]["sq_weights"]}
    umax, _ = iop_campaign_utility(list(log or []) + [{"sq_scores": ones}], cfg)
    raw = u1 - u0
    denom = umax - u0
    return dict(marginal_utility=raw, value=(raw / denom if denom > 0 else 0.0),
                utility_before=u0, utility_after=u1)


def iop_threshold(n_remaining, days_remaining, config=None, nbins=101):
    """Opportunity-cost threshold for spending one of a finite IOP budget.

    Sequential-selection dynamic program: with n IOPs left and d decision days
    left, accept a candidate of value s iff s >= V(n, d-1) - V(n-1, d-1), where
    V(n,d) = E_s[max(s + V(n-1,d-1), V(n,d-1))] under the daily value
    distribution (Beta prior in config['operations']['score_prior']).
    """
    import numpy as np
    from scipy.stats import beta as beta_dist
    cfg = config or DERECHOS_IOP_CONFIG
    pr = cfg["operations"]["score_prior"]
    n_remaining = int(max(0, n_remaining))
    days_remaining = int(max(0, days_remaining))
    x = (np.arange(nbins) + 0.5) / nbins
    pmf = beta_dist.pdf(x, pr["a"], pr["b"])
    pmf = pmf / pmf.sum()
    V = np.zeros((n_remaining + 1, days_remaining + 1))
    for d in range(1, days_remaining + 1):
        for n in range(1, n_remaining + 1):
            take = x + V[n - 1, d - 1]
            skip = V[n, d - 1]
            V[n, d] = float(np.sum(pmf * np.maximum(take, skip)))
    if n_remaining == 0 or days_remaining == 0:
        return dict(threshold=(1.0 if n_remaining == 0 else 0.0), V=V,
                    expected_total=float(V[n_remaining, days_remaining]))
    thr = float(V[n_remaining, days_remaining - 1] - V[n_remaining - 1, days_remaining - 1])
    return dict(threshold=max(0.0, min(1.0, thr)), V=V,
                expected_total=float(V[n_remaining, days_remaining]),
                expected_remaining_opportunities=float(
                    days_remaining * float(np.sum(pmf[x >= thr]))))


def iop_sounding_plan(valid_time, lead_time_h, config=None, window_h=None):
    """3-hourly M1 sounding schedule for an IOP, with a lead-time feasibility flag."""
    import datetime as dt
    cfg = config or DERECHOS_IOP_CONFIG
    op = cfg["operations"]
    if isinstance(valid_time, str):
        valid_time = dt.datetime.fromisoformat(valid_time.replace("Z", ""))
    window_h = window_h or op["iop_sounding_window_h"]
    cad = op["sounding_cadence_h"]
    start = valid_time - dt.timedelta(hours=window_h / 2.0)
    start = start.replace(minute=0, second=0, microsecond=0)
    start -= dt.timedelta(hours=start.hour % cad)
    times = [start + dt.timedelta(hours=k) for k in range(0, int(window_h) + 1, int(cad))]
    return dict(launches=[t.isoformat() for t in times], n_launches=len(times),
                cadence_h=cad, window_h=window_h,
                lead_time_h=lead_time_h,
                required_lead_h=op["sounding_lead_h"],
                feasible=bool(lead_time_h is None or lead_time_h >= op["sounding_lead_h"]))


def iop_decide(scored, n_remaining, days_remaining, log=None, lead_time_h=None,
               config=None):
    """GO / HOLD decision for a candidate IOP against the remaining budget."""
    cfg = config or DERECHOS_IOP_CONFIG
    val = iop_value(scored["sq_scores"], log, cfg)
    thr = iop_threshold(n_remaining, days_remaining, cfg)
    plan = iop_sounding_plan(scored.get("valid_time"), lead_time_h, cfg) \
        if scored.get("valid_time") else None
    go = val["value"] >= thr["threshold"] and max(scored["sq_scores"].values()) > 0
    reasons = ["marginal value %.3f vs opportunity-cost threshold %.3f (%d IOPs / %d days "
               "left)" % (val["value"], thr["threshold"], n_remaining, days_remaining),
               "archetype %s: %s" % (scored["archetype"], scored["archetype_reason"]),
               "SQs served (>=0.5): %s" % (", ".join(scored["served_sqs"]) or "none")]
    caveats = []
    if plan is not None and not plan["feasible"]:
        caveats.append("lead time %s h is inside the %d h sounding-crew requirement: fixed "
                       "instruments and 3-hourly soundings cannot both be guaranteed" %
                       (lead_time_h, cfg["operations"]["sounding_lead_h"]))
    if scored["dropped_predictors"]:
        caveats.append("predictors unavailable in this forecast source: %s" %
                       ", ".join(scored["dropped_predictors"]))
    return dict(decision=("GO" if go else "HOLD"), value=val["value"],
                marginal_utility=val["marginal_utility"], threshold=thr["threshold"],
                expected_remaining_opportunities=thr.get("expected_remaining_opportunities"),
                archetype=scored["archetype"], sq_scores=scored["sq_scores"],
                served_sqs=scored["served_sqs"], reasons=reasons, caveats=caveats,
                sounding_plan=plan)


def iop_module_relocation(daily_values, dwell_days, config=None, candidates=None):
    """Redeployable-module go/no-go between storms (white paper appendix 2).

    daily_values : forecast IOP values for the next N days, day 1 first.
    dwell_days   : days the modules have already spent at the current site.
    """
    cfg = config or DERECHOS_IOP_CONFIG
    op = cfg["operations"]
    thr, need = op["module_break_score"], op["module_break_days_min"]
    run = 0
    for v in daily_values:
        if v is not None and v < thr:
            run += 1
        else:
            break
    quiet = run
    dwell_ok = dwell_days >= op["module_dwell_days_min"]
    go = quiet >= need and dwell_ok
    reasons = ["forecast quiet run %d day(s) below value %.2f (need %d)" % (quiet, thr, need),
               "dwell %d day(s) at current site (minimum %d)" % (dwell_days,
                                                                 op["module_dwell_days_min"])]
    if not go and quiet >= need and not dwell_ok:
        reasons.append("break is long enough but the site has not met minimum dwell: these "
                       "modules are redeployable, not mobile")
    return dict(decision=("RELOCATE" if go else "STAY"), quiet_days=quiet,
                dwell_days=dwell_days, break_threshold=thr, reasons=reasons,
                radius_km=op["module_radius_km"],
                candidate_hosts=(candidates or ["Nachusa Grasslands (41.858, -89.652)",
                                                "Illinois Climate Network site",
                                                "Iowa Environmental Mesonet site",
                                                "future Illinois 3D mesonet site"]))


def iop_report(scored, decision=None, config=None, top_n=6):
    """Markdown scorecard for one candidate IOP."""
    cfg = config or DERECHOS_IOP_CONFIG
    L = ["# DERECHOS IOP scorecard", ""]
    L.append("- valid time (UTC): %s" % scored.get("valid_time"))
    L.append("- archetype: **%s** (%s)" % (scored["archetype"], scored["archetype_reason"]))
    L.append("")
    L.append("| SQ | score | best track | gate |")
    L.append("|---|---|---|---|")
    for sq in sorted(scored["sq_scores"]):
        t = scored["tracks"][sq]
        bt = t["best_track"]
        g = t["detail"][bt]["gate"] if bt else 0.0
        L.append("| %s | %.2f | %s | %.2f |" % (sq, scored["sq_scores"][sq], bt or "-", g))
    L.append("")
    pv = {k: v for k, v in scored["predictors"].items() if v is not None}
    top = sorted(pv.items(), key=lambda kv: -kv[1])[:top_n]
    L.append("Top predictors: " + ", ".join("%s=%.2f (%s=%s)" % (
        k, v, cfg["predictors"][k]["stat"],
        iop_fmt(scored["summary"].get(cfg["predictors"][k]["stat"]))) for k, v in top))
    if scored["dropped_predictors"]:
        L.append("")
        L.append("Predictors with no data: " + ", ".join(scored["dropped_predictors"]))
    if decision:
        L += ["", "## Decision: %s" % decision["decision"]]
        L += ["- " + r for r in decision["reasons"]]
        L += ["- CAVEAT: " + c for c in decision["caveats"]]
        if decision.get("sounding_plan"):
            sp = decision["sounding_plan"]
            L.append("- soundings: %d launches at %d-hourly cadence, lead-time feasible=%s"
                     % (sp["n_launches"], sp["cadence_h"], sp["feasible"]))
    return "\n".join(L)


def iop_fmt(x):
    if x is None:
        return "n/a"
    if isinstance(x, float):
        return ("%.3g" % x)
    return str(x)


def iop_score_window(scored_list, config=None):
    """Aggregate several forecast hours of one candidate day into one IOP call.

    An IOP is a window, not an instant: on 10 Aug 2020 the HRRR 00Z run serves
    SQ7 at 06Z (nocturnal low-level jet) and SQ1/SQ2/SQ6 at 18Z (the derecho), so
    the day as a whole serves four science questions that no single hour does.
    Operationally, score every forecast hour in the candidate window and
    aggregate here.  Per-SQ score is the max over the window (an SQ is served if
    it is served at some point); the archetype and valid time come from the hour
    with the highest weighted total.
    """
    cfg = config or DERECHOS_IOP_CONFIG
    if not scored_list:
        return None
    w = cfg["aggregate"]["sq_weights"]
    sqs = sorted(w)
    best = {sq: 0.0 for sq in sqs}
    peak = {sq: None for sq in sqs}
    for sc in scored_list:
        for sq in sqs:
            v = sc["sq_scores"].get(sq, 0.0)
            if v > best[sq]:
                best[sq], peak[sq] = v, sc.get("valid_time")
    tot = [sum(w[sq] * sc["sq_scores"].get(sq, 0.0) for sq in sqs) for sc in scored_list]
    k = int(max(range(len(tot)), key=lambda i: tot[i]))
    lead = scored_list[k]
    return dict(sq_scores={sq: round(best[sq], 4) for sq in sqs},
                peak_hour_per_sq=peak,
                archetype=lead["archetype"], archetype_reason=lead["archetype_reason"],
                valid_time=lead.get("valid_time"),
                hours=[sc.get("valid_time") for sc in scored_list],
                served_sqs=[sq for sq in sqs if best[sq] >= 0.5],
                dropped_predictors=lead["dropped_predictors"],
                summary=lead["summary"], tracks=lead["tracks"],
                predictors=lead["predictors"])
