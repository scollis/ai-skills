---
name: arm-vaps
description: Index and access layer for DOE ARM value-added products (VAPs) - 80 per-product skills derived from ARM's own technical reports, each carrying the retrieval algorithm, reported quantities, retrieval settings, input instrument dependencies, embedded QC coverage and the documented conditions where the retrieval is invalid or biased, plus a verified ARM Live example. Use when choosing between a VAP and its input instrument, interpreting a retrieved quantity, deciding whether a feature is a retrieval artifact, or looking for an ARM product that already computes what you were about to compute. Covers ARSCL, KAZR-ARSCL, MWRRET, QCRAD, AOD, PBLHT, MICROBASE, LASSO, VARANAL, RADFLUXANAL, the Raman lidar and Doppler lidar profile products, the CMAC radar products and more. Triggers - ARM VAP, value-added product, ARM retrieval, derived product, ARSCL, MWRRET, QCRAD, MICROBASE, LASSO, VARANAL, INTERPSONDE, PBLHT, AOD VAP, CMAC, LDQUANTS, DOE SC ARM TR.
---

# ARM value-added products

ARM does not only publish instrument data. It publishes **value-added products**: retrievals
and quality-controlled composites computed from instrument datastreams, each documented in a
technical report. This directory turns 80 of them into loadable skills, built with the same
pipeline and the same grounding rule as the 150 instrument skills in `arm-instruments`.

Load a product's skill before computing something similar yourself - ARM has usually already
done it, with more care about the edge cases than a one-off script will have.

## The rule that matters most here

**A VAP inherits every limitation of its inputs.** When a retrieved value looks wrong, check
the input instrument's own skill and its DQRs before blaming the algorithm. Each skill lists
its declared input classes and links to `arm-instrument-<code>` for them.

The second rule: a VAP's output changes with its version. The report is the design intent, the
file is what the archive currently serves, and where they disagree the skill says so.

## Credit

These are derived references. The algorithm knowledge in them is the work of the ARM
developers and mentors who wrote the technical reports - **151 of them are credited** across
this tranche, each in the Credit section of the skills derived from their report, with the DOE
report number and a link. Cite the report, not the skill.

## What is here

### Cloud Properties (34)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-arscl` | Active Remote Sensing of CLouds | - | `mmcr`, `mpl` | `sgparsclcbh1clothC1.c1` | 22 |
| `arm-vap-cldtype` | Cloud Type Classification | DOE/SC-ARM-TR-200 | - | `sgpcldtypeC1.c1` | 19 |
| `arm-vap-cogs` | Clouds Optically Gridded by Stereo (COGS) prod | DOE/SC-ARM-TR-252 | - | `sgpcogsN1.c1` | 10 |
| `arm-vap-csapr2-cmac` | C-SAPR2 Corrected Moments in Antenna Coordinat | DOE/SC-ARM-TR-327 | - | `houcsapr2cmacS2.c1` | 15 |
| `arm-vap-csaprct` | C-Band Scanning ARM Precipitation Radar, Adapt | DOE/SC-ARM-TR-324 | - | `houcsapr2cfrqctobacmaskS2.c1` | 10 |
| `arm-vap-dlmc` | Doppler Lidar Mentor Corrected for Ship Motion | DOE/SC-ARM-TR-296 | - | `mosdlmcusrM1.c1` | 7 |
| `arm-vap-kazrarscl` | Active Remote Sensing of CLouds (ARSCL) produc | DOE Tech. Memo. ARM VAP-002.1 | - | `sgparsclkazrbnd1kolliasC1.c1` | 20 |
| `arm-vap-kazrarsclcloudsat` | KAZR-ARSCL, reflectivities aligned with CloudS | DOE/SC-ARM-TR-279 | - | `sgparsclkazrcloudsatC1.c1` | 13 |
| `arm-vap-kazrcor` | KAZR Corrected Data | DOE/SC-ARM-TR-203 | - | _not verified_ | 7 |
| `arm-vap-mascparticles` | Multi-Angle Snowflake Camera Particle Analysis | DOE/SC-ARM-TR-187 | `masc` | `nsamascparticlesavgC1.c1` | 41 |
| `arm-vap-microbase` | Continuous Baseline Microphysical Retrieval | DOE/SC-ARM-TR-095 | - | `sgpmicrobasepiavgC1.c1` | 21 |
| `arm-vap-mmcg` | Precipitation Radar Moments Mapped to a Cartes | DOE/SC-ARM-TR-243 | - | `sgpxsaprmmcgI5.c1` | 9 |
| `arm-vap-mplcmask` | Cloud mask from Micropulse Lidar | DOE/SC-ARM-TR-098 | `mpl` | `sgp30smplcmask1zwangC1.c1` | 17 |
| `arm-vap-mplcmaskml` | Micropulse Lidar Cloud Mask Machine Learning V | DOE/SC-ARM-TR-274 | - | `sgpmplcmaskmlC1.c1` | 12 |
| `arm-vap-mwrret` | MWR Retrievals | DOE/SC-ARM/TR-081.2 | `mwr` | `sgpmwrret1liljclouC1.c1` | 10 |
| `arm-vap-mwrretv2` | MWR Retrievals with MWRRET Version 2 | DOE/SC-ARM-TR-245 | - | `sgpmwrret2turnC1.c1` | 10 |
| `arm-vap-ndrop` | Droplet number concentration | DOE/SC-ARM-TR-140 | - | `sgpndropmfrsrC1.c1` | 15 |
| `arm-vap-pccp` | Stereo Reconstructed Point Cloud of Cloud Poin | DOE/SC-ARM-TR-252 | - | `sgppccpE45.c1` | 11 |
| `arm-vap-ppihyd` | hydrometeor field statistics dataset derived f | DOE/SC-ARM-TR-307 | - | _not verified_ | 13 |
| `arm-vap-radarcfad` | Radar Contoured Frequency by Altitude Diagram | DOE/SC-ARM-TR-190 | - | `sgpkazrcfadC1.c1` | 8 |
| `arm-vap-radclss` | Extracted Radar Columns and In-Situ Sensors (R | DOE/SC-ARM-TR-312 | - | `bnfcsapr2radclssS3.c2` | 10 |
| `arm-vap-ripbe` | Radiatively Important Parameters Best Estimate | DOE/SC-ARM-TR-097 | - | `sgpripbe1mcfarlaneC1.c1` | 18 |
| `arm-vap-rlprof` | Raman LIDAR Vertical Profiles | DOE/SC-ARM-TR-189 | `rl` | `sgp10rlprofbe1newsC1.c1` | 14 |
| `arm-vap-rlprof-fex` | Raman Lidar Vertical Profiles Feature Detectio | DOE/SC-ARM-TR-224 | - | `sgprlproffexext1thorC1.c0` | 13 |
| `arm-vap-rnccn` | Retrieved Number concentration of CCN | DOE/SC-ARM-TR-292 | - | `sgprnccnprof1kulkarniC1.c1` | 13 |
| `arm-vap-sacradvvad` | SACR Advance Velocity Azimuth Display | DOE/SC-ARM-TR-209 | - | `sgpkasacradvvadC1.c1` | 5 |
| `arm-vap-sfccldgrid` | Surface Cloud Grid | DOE/SC-ARM-TR-010 | - | `sgpsfccldgrid2longstationN1.c1` | 10 |
| `arm-vap-shallowcumulus` | Fair-Weather Shallow Cumulus Identification | DOE/SC-ARM-TR-214 | - | `sgpshcusummaryC1.c1` | 25 |
| `arm-vap-sphotcod` | Cloud optical depth retrieved from multi-chann | DOE/SC-ARM-TR-317 | - | `sgpsphotcod2chiuC1.c1` | 9 |
| `arm-vap-squire` | Surface QUantitatIve pRecipitation Estimation  | DOE/SC-ARM-TR-287 | - | `bnfcsapr2squireS3.c1` | 10 |
| `arm-vap-thermocldphase` | Thermodynamic Cloud Phase | DOE/SC-ARM-TR-325 | - | `sgpthermocldphaseC1.c1` | 11 |
| `arm-vap-xprecipcmac` | CSU X-Band Precip Radar (XPRECIPRADAR) PPI Cor | DOE/SC-ARM-TR 313 | - | `gucxprecipradarcmacppiS2.c1` | 20 |
| `arm-vap-xprecipradarhp` | Surface Hydrometeor Phase | DOE/SC-ARM-TR-334 | - | `gucxprecipradarhpS2.c1` | 7 |
| `arm-vap-xsapr-cmac` | X-SAPR Corrected Moments in Antenna Coordinate | DOE/SC-ARM-TR-283 | - | _not verified_ | 17 |

### Derived Quantities and Models (19)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-acsmcdce` | ACSM, corrected for composition-dependent coll | DOE/SC-ARM-TR-271 | - | `sgpacsmcdceC1.c1` | 11 |
| `arm-vap-aerioe` | AERIoe Thermodynamic Profile and Cloud Retriev | DOE/SC-ARM-TR-234 | - | `sgpaerioe1turnC1.c1` | 14 |
| `arm-vap-aeriprof` | AERI Profiles of Water Vapor and Temperature | DOE/SC-ARM/TR-066.1 | `aeri` | `sgpaeriprof3feltzC1.c1` | 24 |
| `arm-vap-aod-nimfr` | Aerosol Optical Depth (AOD) derived from NIMFR | DOE/SC-ARM-TR-129 | - | `sgpnimfr7nchaod1michC1.c1` | 13 |
| `arm-vap-ccnkappa` | CCN Counter derived hygroscopicity parameter k | DOE/SC-ARM-TR-272 | - | `enaaosccnsmpskappaC1.c1` | 10 |
| `arm-vap-ccnprof` | Cloud Condensation Nuclei Profile | DOE/SC-ARM/TR-103 | - | `sgprlccnprof1ghanC1.c1` | 18 |
| `arm-vap-csapr2-cmac` | C-SAPR2 Corrected Moments in Antenna Coordinat | DOE/SC-ARM-TR-327 | - | `houcsapr2cmacS2.c1` | 15 |
| `arm-vap-diffcor` | Correction of Diffuse Shortwave Measurements | DOE/SC-ARM/TR-009 | `brs`, `sirs`, `skyrad` | `sgpbrs1duttC1.c1` | 13 |
| `arm-vap-interpsonde` | Interpolated Sonde | DOE/SC-ARM-TR-183 | - | `sgpinterpolatedsondeC1.c1` | 10 |
| `arm-vap-lasso` | LES ARM Symbiotic Simulation and Observation ( | DOE/SC-ARM-TR-216 | - | _not verified_ | 53 |
| `arm-vap-lclheight` | Lifting Condensation Level Height | DOE/SC-ARM-TR-242 | - | `sgplclC1.c1` | 6 |
| `arm-vap-mwrret` | MWR Retrievals | DOE/SC-ARM/TR-081.2 | `mwr` | `sgpmwrret1liljclouC1.c1` | 10 |
| `arm-vap-mwrretv2` | MWR Retrievals with MWRRET Version 2 | DOE/SC-ARM-TR-245 | - | `sgpmwrret2turnC1.c1` | 10 |
| `arm-vap-radfluxanal` | Radiative Flux Analysis | DOE/SC-ARM-TR-228 | - | `sgpradfluxbrs1longC1.c1` | 14 |
| `arm-vap-ripbe` | Radiatively Important Parameters Best Estimate | DOE/SC-ARM-TR-097 | - | `sgpripbe1mcfarlaneC1.c1` | 18 |
| `arm-vap-sfccldgrid` | Surface Cloud Grid | DOE/SC-ARM-TR-010 | - | `sgpsfccldgrid2longstationN1.c1` | 10 |
| `arm-vap-varanal` | Constrained Variational Analysis | DOE/SC-ARM-TR-222 | - | `sgp60varanarapC1.c1` | 12 |
| `arm-vap-varanal3d` | Three-dimensional Constrained Variational Anal | DOE/SC-ARM-TR-253 | - | `sgp180varanal3drucC1.c1` | 13 |
| `arm-vap-xsapr-cmac` | X-SAPR Corrected Moments in Antenna Coordinate | DOE/SC-ARM-TR-283 | - | _not verified_ | 17 |

### Aerosols (18)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-acsmcdce` | ACSM, corrected for composition-dependent coll | DOE/SC-ARM-TR-271 | - | `sgpacsmcdceC1.c1` | 11 |
| `arm-vap-aerosolbe` | Aerosol Best Estimate | DOE/SC-ARM/TR-115 | - | `sgpaerosolbe1turnC1.c1` | 14 |
| `arm-vap-aip` | Aerosol Intensive Properties | DOE/SC-ARM-TR-201 | - | `sgpaipavg1ogrenC1.c1` | 7 |
| `arm-vap-aod-mfrsr` | Aerosol Optical Depth (AOD) derived from MFRSR | DOE/SC-ARM-TR-129 | - | `sgpmfrsr7nchcalC1.c1` | 12 |
| `arm-vap-aod-nimfr` | Aerosol Optical Depth (AOD) derived from NIMFR | DOE/SC-ARM-TR-129 | - | `sgpnimfr7nchaod1michC1.c1` | 13 |
| `arm-vap-aodbe` | Aerosol Optical Depth Best Estimate | DOE/SC-ARM-TR-247 | - | `sgpaodbe5chC1.c1` | 10 |
| `arm-vap-aop` | Aerosol Optical Properties | DOE/SC-ARM-TR-211 | - | `sgpaoppsap1flynn1mC1.c1` | 13 |
| `arm-vap-ccnkappa` | CCN Counter derived hygroscopicity parameter k | DOE/SC-ARM-TR-272 | - | `enaaosccnsmpskappaC1.c1` | 10 |
| `arm-vap-ccnprof` | Cloud Condensation Nuclei Profile | DOE/SC-ARM/TR-103 | - | `sgprlccnprof1ghanC1.c1` | 18 |
| `arm-vap-mergedaerosol` | Merged Aerosol VAP | DOE/SC-ARM-TR-338 | - | `epcmergedaerosolM1.c1` | 7 |
| `arm-vap-mergedsmpsaps` | merged size distribution from SMPS and APS | DOE/SC-ARM-TR-294 | - | `enamergedsmpsapsC1.c1` | 14 |
| `arm-vap-mfrsrcldod` | Cloud Optical Properties from MFRSR Using Min  | DOE/SC-ARM-TR-047 | `mfrsr` | `sgpmfrsrcldod1minC1.c1` | 13 |
| `arm-vap-oacomp` | Organic Aerosol Component | DOE/SC-ARM-TR-131 | - | `sgpoacomp1zhangC1.c1` | 18 |
| `arm-vap-ripbe` | Radiatively Important Parameters Best Estimate | DOE/SC-ARM-TR-097 | - | `sgpripbe1mcfarlaneC1.c1` | 18 |
| `arm-vap-rlprof` | Raman LIDAR Vertical Profiles | DOE/SC-ARM-TR-189 | `rl` | `sgp10rlprofbe1newsC1.c1` | 14 |
| `arm-vap-rlprof-fex` | Raman Lidar Vertical Profiles Feature Detectio | DOE/SC-ARM-TR-224 | - | `sgprlproffexext1thorC1.c0` | 13 |
| `arm-vap-rlprofmr` | Raman Lidar Mixing Ratio | DOE/SC-ARM-TR-218 | - | `sgp10rlprofmr1turnC1.c1` | 13 |
| `arm-vap-rlproftemp` | Raman Lidar Temperature VAP | DOE/SC-ARM-TR-218 | - | `sgprlproftemp2news10mC1.c0` | 12 |

### Atmospheric Profiling (16)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-armlagtraj` | Lagrangian large-scale forcing data following  | DOE/SC-ARM-TR-306 | - | _not verified_ | 6 |
| `arm-vap-armtraj` | Airmass trajectories to support studies using  | DOE/SC-ARM-TR-314 | - | `sgparmtrajpblC1.c1` | 13 |
| `arm-vap-armtraj-air` | Airmass trajectories to support studies using  | DOE/SC-ARM-TR-314 | - | `sgparmtrajtbsC1.c1` | 11 |
| `arm-vap-dlmcprof-wind` | Doppler Lidar Motion Correction (DLMC) Wind Pr | DOE/SC-ARM-TR-295 | - | `mosdlmcprofwindnewsM1.c1` | 8 |
| `arm-vap-dlprof-wind` | Doppler Lidar Wind | DOE/SC-ARM-TR-148 | - | `sgpdlprofwind4newsC1.c1` | 7 |
| `arm-vap-dlprof-wstats` | Doppler Lidar Vertical Velocity Statistics | DOE/SC-ARM-TR-149 | - | `sgpdlprofwstats4newsC1.c1` | 11 |
| `arm-vap-interpsonde` | Interpolated Sonde | DOE/SC-ARM-TR-183 | - | `sgpinterpolatedsondeC1.c1` | 10 |
| `arm-vap-mergesonde` | Merged Sounding | DOE/SC-ARM/TR-087 | - | `sgpmergesonde1maceC1.c1` | 10 |
| `arm-vap-pblht` | Planetary Boundary Layer Height | DOE/SC-ARM/TR-132 | - | `sgppblhtsonde1mcfarlC1.c1` | 18 |
| `arm-vap-rlprof` | Raman LIDAR Vertical Profiles | DOE/SC-ARM-TR-189 | `rl` | `sgp10rlprofbe1newsC1.c1` | 14 |
| `arm-vap-rlprof-fex` | Raman Lidar Vertical Profiles Feature Detectio | DOE/SC-ARM-TR-224 | - | `sgprlproffexext1thorC1.c0` | 13 |
| `arm-vap-rlprofmr` | Raman Lidar Mixing Ratio | DOE/SC-ARM-TR-218 | - | `sgp10rlprofmr1turnC1.c1` | 13 |
| `arm-vap-rlproftemp` | Raman Lidar Temperature VAP | DOE/SC-ARM-TR-218 | - | `sgprlproftemp2news10mC1.c0` | 12 |
| `arm-vap-sondeadjust` | Sonde Adjust | DOE/SC-ARM-TR-102 | - | `sgpsondeadjustC1.c1` | 12 |
| `arm-vap-sondegrid` | Gridded Sonde VAP Product | DOE/SC-ARM-TR-183 | - | `sgpgriddedsondeC1.c0` | 7 |
| `arm-vap-sondeparam` | convective parameters derived from radiosonde  | DOE/SC-ARM-TR-284 | - | `sgpsondeparamC1.c1` | 8 |

### Radiometric (11)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-aerinf` | AERI Noise Filtered | DOE/SC-ARM/TR-071 | `aeri` | `sgpaerich2nf1turnC1.c1` | 8 |
| `arm-vap-aeriprof` | AERI Profiles of Water Vapor and Temperature | DOE/SC-ARM/TR-066.1 | `aeri` | `sgpaeriprof3feltzC1.c1` | 24 |
| `arm-vap-aod-mfrsr` | Aerosol Optical Depth (AOD) derived from MFRSR | DOE/SC-ARM-TR-129 | - | `sgpmfrsr7nchcalC1.c1` | 12 |
| `arm-vap-aod-nimfr` | Aerosol Optical Depth (AOD) derived from NIMFR | DOE/SC-ARM-TR-129 | - | `sgpnimfr7nchaod1michC1.c1` | 13 |
| `arm-vap-beflux` | Best-Estimate Radiative Flux | DOE/SC-ARM/TR-008 | `brs`, `sirs` | `sgpqcflux1longC1.c1` | 15 |
| `arm-vap-mfrsrcldod` | Cloud Optical Properties from MFRSR Using Min  | DOE/SC-ARM-TR-047 | `mfrsr` | `sgpmfrsrcldod1minC1.c1` | 13 |
| `arm-vap-mwrret` | MWR Retrievals | DOE/SC-ARM/TR-081.2 | `mwr` | `sgpmwrret1liljclouC1.c1` | 10 |
| `arm-vap-mwrretv2` | MWR Retrievals with MWRRET Version 2 | DOE/SC-ARM-TR-245 | - | `sgpmwrret2turnC1.c1` | 10 |
| `arm-vap-qcrad` | Data Quality Assessment for ARM Radiation Data | DOE/SC-ARM/TR-074 | `gndrad`, `mfrsr`, `sirs`, `skyrad` | `sgpqcradbrs1longC1.c1` | 15 |
| `arm-vap-radfluxanal` | Radiative Flux Analysis | DOE/SC-ARM-TR-228 | - | `sgpradfluxbrs1longC1.c1` | 14 |
| `arm-vap-ripbe` | Radiatively Important Parameters Best Estimate | DOE/SC-ARM-TR-097 | - | `sgpripbe1mcfarlaneC1.c1` | 18 |

### Surface/Subsurface Properties (4)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-arealavealb` | Areal-Averaged Surface Albedo | DOE/SC-ARM-TR-309 | - | `sgparealavealbC1.c1` | 9 |
| `arm-vap-okmsoil` | Oklahoma Mesonet Soil Moisture | DOE/SC-ARM-TR-230 | - | _not verified_ | 4 |
| `arm-vap-qcecor` | Quality Controlled Eddy Correlation Flux Measu | DOE/SC-ARM-TR-223 | `ecor` | `ena30qcecorC1.c1` | 11 |
| `arm-vap-surfspecalb` | Surface Spectral Albedo | DOE/SC-ARM-TR-096 | - | `sgpsurfspecalb7nch1mlawerC1.c1` | 18 |

### Airborne Observations (3)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-aafmerged` | ARM Aerial Facility (AAF) Merged VAP for Histo | DOE/SC-ARM-TR-299 | - | `sgpaafmergedF1.c1` | 8 |
| `arm-vap-armtraj-air` | Airmass trajectories to support studies using  | DOE/SC-ARM-TR-314 | - | `sgparmtrajtbsC1.c1` | 11 |
| `arm-vap-tbsmerged` | Tethered Balloon System (TBS) Merged Data Prod | DOE/SC-ARM-TR-286 | - | `sgptbsmergedC1.c1` | 10 |

### Surface Meteorology (3)

| skill | product | report | inputs | example datastream | failure modes |
|---|---|---|---|---|---|
| `arm-vap-ldquants` | Laser Disdrometer Quantities | DOE/SC-ARM-TR-221 | - | `sgpldquantsC1.c1` | 2 |
| `arm-vap-vdisquants` | Video Disdrometer VAP | DOE/SC-ARM-TR-221 | - | `sgpvdisquantsC1.c1` | 2 |
| `arm-vap-xprecipradarhp` | Surface Hydrometeor Phase | DOE/SC-ARM-TR-334 | - | `gucxprecipradarhpS2.c1` | 7 |

## Honesty markers you will see

- **Scope of this report** - 10 products share a report with a sibling, or are covered by a
  report about a different member of the family. `arscl` and `kazrarscl` share the 2001
  MMCR-era ARSCL document, which predates the KAZR implementation entirely; `aod-mfrsr` and
  `aod-nimfr` share one AOD report; `ldquants` and `vdisquants` share one; `interpsonde` and
  `sondegrid` share one. Those skills say so rather than presenting the document as their own.
- **Extraction coverage** - 7 reports are longer than the extractor's window or thinner than
  its schema. LASSO is 171 pages of which 60 were read; ARMTRAJ and ARMTRAJ-AAF are 176 pages
  of which about a quarter was read; QCRAD's Appendix B field dump was not read; LDQUANTS,
  VDISQUANTS and MERGEDAEROSOL are 10-12 page reports with few stated caveats. Those skills
  mark their lists as lower bounds rather than inventories.
- **No example verified** - 6 products could not be opened: `armlagtraj` and `okmsoil` are
  served only at level a0, which ARM Live refuses; `kazrcor` and `ppihyd` serve files of 0.8-2.4
  GB; `lasso` serves a tar bundle that arrived truncated; `xsapr-cmac` failed to open with an
  HDF error on two separate files. Those skills carry the reason in place of a data section.

One product was **rejected** rather than published on the wrong document: `aod`, whose linked
report documents the SAS-He AOD product rather than the MFRSR/NIMFR one it serves. Use
`arm-vap-aod-mfrsr` or `arm-vap-aod-nimfr`, whose report is the right one. The reason is in
`catalog.csv` under `no_handbook_reason`.

## Finding a product

The catalog, helpers and ARM search API live in `arm-instruments` - one copy for both
tranches. `catalog.csv` there carries a `product_type` column (`instrument` or `vap`), a
`vap_inputs` column, and the `skill` name for every class that has one:

```python
arm_instrument("mwrret")        # catalog record, including skill name and inputs
arm_skill_for("kazrarscl")      # 'arm-vap-kazrarscl'
arm_find_instruments("cloud base height")   # instruments and products together
```

## Getting the data

Same as the instrument tranche: `act-arm-live` for ARM Live, datastream naming, server-side
subsetting and DOI citation; `act-qc` for the `qc_` flags and DQRs; `act-plotting` for the
Display family. For the radar products (`csapr2-cmac`, `xprecipcmac`, `xsapr-cmac`, `ppihyd`,
`sacradvvad`, `radarcfad`) load `pyart-foundations` and the `pyart-*` tranche, and `cmac-vap`
for CMAC's own machinery.

## Verified against

- ARM data-source catalog read 2026-09-24; 80 derived classes with a technical report and data
- 80 technical reports downloaded and text-extracted; page citations checked against each report's page count
- ARM Live queried with `ARMUSER`/`ARMTOKEN` on 2026-09-24; 74 files opened with ACT 2.3.4
- 1029 documented failure modes extracted across the tranche
