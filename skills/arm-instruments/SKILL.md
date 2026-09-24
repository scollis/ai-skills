---
name: arm-instruments
description: Index and access layer for DOE ARM facility instrumentation - 150 per-instrument handbook skills in this directory, plus ARM's own data-source catalog API (the only complete enumeration of ARM instrument classes), the two URL patterns instrument handbooks are filed under, and helpers that resolve an instrument code to its handbook, its datastreams and a verified example. Use when choosing an ARM instrument or datastream for a measurement, when asked what instrument measures a quantity, when an instrument code like kazr or ecor or aosmet needs resolving, when a handbook is wanted, or before building a new per-instrument skill. Triggers - ARM instrument, instrument handbook, instrument mentor, ARM instrument class, instrument code, ARM catalog, capabilities instruments, datastream for, which instrument measures, DOE SC ARM TR, ARM Data Center instrument, arm.gov handbook.
---

# ARM instrumentation

DOE's Atmospheric Radiation Measurement facility documents every deployed instrument in a
handbook written by its instrument mentor. This directory turns those handbooks into
loadable skills - **150 instruments**, each grounded in the handbook *and* in a real
data file pulled from ARM Live, so the prose and the variable names agree with what the
archive actually serves.

Load the per-instrument skill when you know the instrument. Load this one to find it, or
when you need the catalog itself.

ARM's **value-added products** - retrievals computed from these instruments - are a separate
tranche: load `arm-vaps` for its index, or `arm-vap-<code>` directly. Both tranches share the
`catalog.csv` and helpers in this skill; its `product_type` column says which a class is, and
`vap_inputs` names a product's input instruments.

## Credit

These skills are derived references. The instrument knowledge in them is the work of the
ARM instrument mentors who wrote the handbooks - 145 of the 150 name their
authors on the cover, and each skill credits its own in a Credit section with the DOE
report number and a link. 5 handbooks are issued by the facility with no
individual author named (`pass`, `surthref`, `thwaps`, `tps`, `wsi`); those skills say so
rather than leaving the section blank.

Cite the handbook, not the skill. The `authors` column in `catalog.csv` carries the
attribution in machine-readable form, and a structure test fails the build if any skill
ships without either an author list or an explicit statement that the cover names none.

## What is here

### Aerosols (42)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-acsm` | Aerosol Chemical Speciation Monitor | DOE/SC-ARM-TR-196 | `sgpaosacsmC1.b1` | 10 | - |
| `arm-instrument-aeth` | Aethalometer | DOE/SC-ARM-TR-156 | `dstaosaeth2spot1mM1.b1` | 12 | - |
| `arm-instrument-aos` | Aerosol Observing System | - | `sgpnoaaaosavgC1.b1` | 1 | - |
| `arm-instrument-aps` | Aerodynamic Particle Sizer | DOE/SC-ARM-TR-343 | `enaaosapsC1.b1` | 16 | - |
| `arm-instrument-caps-pmex` | Cavity Attenuated Phase Shift Extinction Monitor | DOE/SC-ARM-TR-155 | `enaaoscaps3wC1.b1` | 12 | - |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 | - |
| `arm-instrument-ccn` | Cloud Condensation Nuclei Particle Counter | DOE/SC-ARM-TR-168 | `sgpaosccn1colspectraC1.b1` | 12 | - |
| `arm-instrument-ccn-air` | Cloud Condensation Nuclei Particle Counter aboard Ai | DOE/SC-ARM-TR-225 | `sgpaafccn2colbF1.b1` | 14 | - |
| `arm-instrument-clap` | Continuous Light Absorption Photometer | - | `pvcaosclap3wM1.c1` | 21 | - |
| `arm-instrument-co-analyzer` | Carbon Monoxide Analyzer | DOE/SC-ARM-TR-159 | `enaaoscoC1.b1` | 19 | - |
| `arm-instrument-cpc` | Condensation Particle Counter | DOE/SC-ARM-TR-145 | `sgpaoscpcC1.b1` | 19 | - |
| `arm-instrument-cpc-air` | Condensation particle counter aboard aircraft | DOE/SC-ARM-TR-227 | `bnfaafmcpcU2.b1` | 15 | - |
| `arm-instrument-csphot` | Sunphotometer | DOE/SC-ARM/TR-056 | `sgpcsphotzenradv3C1.a1` | 12 | - |
| `arm-instrument-hsrl` | High Spectral Resolution Lidar | DOE/SC-ARM-TR-157 | `sgphsrlscanC1.a1` | 8 | - |
| `arm-instrument-htdma` | Humidified Tandem Differential Mobility Analyzer | DOE/SC-ARM-TR-161 | `enaaoshtdmaC1.b1` | 11 | - |
| `arm-instrument-ins` | Ice Nucleation Spectrometer for INP measurement | DOE/SC-ARM-TR-278 | `sgpinpC1.a1` | 17 | - |
| `arm-instrument-mpl` | Micropulse Lidar | DOE/SC-ARM-TR-019 | `sgpminimplC1.b1` | 16 | - |
| `arm-instrument-msems` | Miniatured Scanning Electrical Mobility Sizer | DOE/SC-ARM-TR-310 | `bnfminiaosmsemsM1.a1` | 4 | parent hb, class-specific |
| `arm-instrument-msems-air` | ARM Aerial Facility (AAF) Miniaturized Scanning Elec | DOE/SC-ARM-TR-310 | `bnfaafmsemsU2.b1` | 4 | - |
| `arm-instrument-nephelometer` | Nephelometer | - | `pvcaosnephwetM1.c1` | 10 | - |
| `arm-instrument-nephelometer-air` | 3-Wavelength integrating nephelometer aboard aircraf | DOE/SC-ARM-TR-248 | `nsaaafneph10sF1.b1` | 12 | - |
| `arm-instrument-nimfr` | Normal Incidence Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpnimfr7nchlangplotC1.c1` | 9 | - |
| `arm-instrument-opc` | Optical Particle Counter | DOE/SC-ARM-TR-343 | `bnfminiaosopcM1.b1` | 21 | **different instrument** |
| `arm-instrument-pass` | Photoacoustic Soot Spectrometer | DOE/SC-ARM-TR-123 | `sgpaospass3wC1.a1` | 15 | - |
| `arm-instrument-pcasp-air` | Passive cavity aerosol spectrometer aboard aircraft | DOE/SC-ARM-TR-241 | `sgpaafpcaspF1.b1` | 10 | - |
| `arm-instrument-pops` | portable or printed optical particle spectrometer | DOE/SC-ARM-TR-328 | `dstpops1mM1.b1` | 18 | - |
| `arm-instrument-pops-air` | portable optical particle spectrometer aboard an air | DOE/SC-ARM-TR-259 | `bnfaafpopsU2.b1` | 10 | - |
| `arm-instrument-psap` | Particle Soot Absorption Photometer | DOE/SC-ARM-TR-176 | `pvcaospsap3wM1.c1` | 16 | - |
| `arm-instrument-psap-air` | Particle soot absorption photometer aboard aircraft | DOE/SC-ARM-TR-262 | `enaaafpsap1sF1.b1` | 11 | - |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 | - |
| `arm-instrument-smps` | Scanning mobility particle sizer | DOE/SC-ARM-TR-147 | `enaaossmpsC1.b1` | 20 | - |
| `arm-instrument-smps-air` | Scanning mobility particle sizer aboard aircraft | DOE/SC-ARM-TR-310 | `coraafsmpsF1.b1` | 4 | - |
| `arm-instrument-sp2` | Single Particle Soot Photometer | DOE/SC-ARM-TR-169 | `bnfaossp2xrM1.b1` | 10 | - |
| `arm-instrument-sp2-air` | Single Particle Soot Photometer aboard aircraft | DOE/SC-ARM-TR-169 | `nsaaafsp2rbc10sF1.c1` | 9 | - |
| `arm-instrument-tap` | Tricolor Absorption Photometer | DOE/SC-ARM-TR-267 | `sgpaostapE13.b1` | 10 | - |
| `arm-instrument-tap-air` | Tricolor Absorption Photometer aboard aircraft | DOE/SC-ARM-TR-267 | `bnfaafstapU2.b1` | 10 | parent hb, system-level |
| `arm-instrument-tbscpc` | Condensation Particle Counter aboard Tethered Balloo | DOE/SC-ARM-TR-206 | `sgptbscpcC1.b1` | 9 | parent hb, class-specific |
| `arm-instrument-tbsins` | Ice Nucleation Spectrometer for INP measurements abo | DOE/SC-ARM-TR-206 | `sgptbsinpC1.a1` | 5 | parent hb, class-specific |
| `arm-instrument-tbspops` | Portable Optical Particle Spectrometer aboard Tether | DOE/SC-ARM-TR-206 | `sgptbspopsC1.b1` | 7 | parent hb, class-specific |
| `arm-instrument-tdma` | Tandem Differential Mobility Analyzer | DOE/SC-ARM-TR-090 | `sgptdmaapssizeC1.c1` | 20 | - |
| `arm-instrument-uhsas` | Ultra-High Sensitivity Aerosol Spectrometer | DOE/SC-ARM-TR-163 | `enaaosuhsasC1.b1` | 9 | - |
| `arm-instrument-uhsas-air` | Ultra-High Sensitivity Aerosol Spectrometer aboard a | DOE/SC-ARM-TR-250 | `sgpaafuhsasF1.b1` | 10 | - |

### Airborne Observations (39)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-2ds-air` | 2 Dimensional Stereo Probe aboard aircraft | DOE/SC-ARM-TR-233 | `sgpaaf2dsvF1.c1` | 12 | - |
| `arm-instrument-aimms20-air` | Aircraft Integrated Meteorological Measurement Syste | DOE/SC-ARM-TR-260 | `bnfaafnavaims100hzU2.a1` | 4 | - |
| `arm-instrument-cam-air` | Video camera aboard aircraft | DOE/SC-ARM-TR-231 | _not verified_ | 7 | - |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 | - |
| `arm-instrument-ccn-air` | Cloud Condensation Nuclei Particle Counter aboard Ai | DOE/SC-ARM-TR-225 | `sgpaafccn2colbF1.b1` | 14 | - |
| `arm-instrument-cip-air` | Cloud Imaging Probe aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcipF1.b1` | 10 | - |
| `arm-instrument-cmh-air` | Chilled Mirror Hygrometer aboard aircraft | DOE/SC-ARM-TR-235 | `sgpaafdewpointF1.b1` | 8 | - |
| `arm-instrument-co-air` | Carbon Monoxide- Airborne | DOE/SC-ARM/TR-072 | `sgpaafcoF1.c1` | 11 | parent hb, system-level |
| `arm-instrument-cpc-air` | Condensation particle counter aboard aircraft | DOE/SC-ARM-TR-227 | `bnfaafmcpcU2.b1` | 15 | - |
| `arm-instrument-fcdp-air` | Fast Cloud Droplet Probe aboard aircraft | DOE/SC-ARM-TR-238 | `sgpaaffcdpF1.c1` | 9 | - |
| `arm-instrument-gustprobe-air` | Gust Probe aboard aircraft | DOE/SC-ARM-TR-260 | `sgpaafgust1hzF1.a1` | 4 | - |
| `arm-instrument-hvps-air` | High Volume Precipitation Spectrometer aboard aircra | DOE/SC-ARM-TR-239 | `sgpaafhvpsF1.c1` | 11 | - |
| `arm-instrument-inletcvi-air` | Inlet for Counterflow Virtual Impactor aboard aircra | DOE/SC-ARM-TR-254 | `sgpaafinletcviF1.c1` | 21 | - |
| `arm-instrument-inletisok-air` | Isokinetic Inlet aboard aircraft | DOE/SC-ARM-TR-251 | `sgpaafinletisokF1.a1` | 11 | - |
| `arm-instrument-irt-air` | Infrared Thermometer - Airborne | DOE/SC-ARM-TR-015 | `bnfaafirtU2.b1` | 12 | parent hb, class-specific |
| `arm-instrument-met-air` | Meteorological Instrumentation aboard Aircraft | DOE/SC-ARM-TR-260 | `bnfaaftrhU2.b1` | 4 | - |
| `arm-instrument-mfr-air` | Multifilter Radiometer aboard aircraft | DOE/SC-ARM/TR-059 | `sgpmfraafF2.b1` | 8 | parent hb, class-specific |
| `arm-instrument-msems-air` | ARM Aerial Facility (AAF) Miniaturized Scanning Elec | DOE/SC-ARM-TR-310 | `bnfaafmsemsU2.b1` | 4 | - |
| `arm-instrument-nav-air` | Navigational Location, Motion, and Attitude for Airb | DOE/SC-ARM-TR-236 | `bnfaafnavU2.b1` | 14 | - |
| `arm-instrument-nephelometer-air` | 3-Wavelength integrating nephelometer aboard aircraf | DOE/SC-ARM-TR-248 | `nsaaafneph10sF1.b1` | 12 | - |
| `arm-instrument-ozone-air` | Ozone Monitor aboard Aircraft | DOE/SC-ARM-TR-179 | `sgpaafo3F1.c1` | 21 | - |
| `arm-instrument-pcasp-air` | Passive cavity aerosol spectrometer aboard aircraft | DOE/SC-ARM-TR-241 | `sgpaafpcaspF1.b1` | 10 | - |
| `arm-instrument-pops-air` | portable optical particle spectrometer aboard an air | DOE/SC-ARM-TR-259 | `bnfaafpopsU2.b1` | 10 | - |
| `arm-instrument-psap-air` | Particle soot absorption photometer aboard aircraft | DOE/SC-ARM-TR-262 | `enaaafpsap1sF1.b1` | 11 | - |
| `arm-instrument-smps-air` | Scanning mobility particle sizer aboard aircraft | DOE/SC-ARM-TR-310 | `coraafsmpsF1.b1` | 4 | - |
| `arm-instrument-so2-air` | Sulfur Dioxide Monitor aboard Aircraft | DOE/SC-ARM-TR-180 | `oscaafso2F1.c1` | 17 | - |
| `arm-instrument-sp2-air` | Single Particle Soot Photometer aboard aircraft | DOE/SC-ARM-TR-169 | `nsaaafsp2rbc10sF1.c1` | 9 | - |
| `arm-instrument-tap-air` | Tricolor Absorption Photometer aboard aircraft | DOE/SC-ARM-TR-267 | `bnfaafstapU2.b1` | 10 | parent hb, system-level |
| `arm-instrument-tbscpc` | Condensation Particle Counter aboard Tethered Balloo | DOE/SC-ARM-TR-206 | `sgptbscpcC1.b1` | 9 | parent hb, class-specific |
| `arm-instrument-tbsdts` | Distributed Temperature Sensing aboard Tethered Ball | DOE/SC-ARM-TR-206 | `sgptbsdtsch1C1.b1` | 10 | parent hb, class-specific |
| `arm-instrument-tbsground` | Tethered Balloon System Ground Measurement | DOE/SC-ARM-TR-206 | `sgptbsgroundC1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-tbsins` | Ice Nucleation Spectrometer for INP measurements abo | DOE/SC-ARM-TR-206 | `sgptbsinpC1.a1` | 5 | parent hb, class-specific |
| `arm-instrument-tbslws` | Leaf Wetness Sensor aboard Tethered Balloon System | DOE/SC-ARM-TR-206 | _not verified_ | 17 | parent hb, system-level |
| `arm-instrument-tbsmet` | Meteorological Instrumentation aboard TBS | DOE/SC-ARM-TR-206 | `sgptbsimetxq2C1.b1` | 7 | parent hb, class-specific |
| `arm-instrument-tbspops` | Portable Optical Particle Spectrometer aboard Tether | DOE/SC-ARM-TR-206 | `sgptbspopsC1.b1` | 7 | parent hb, class-specific |
| `arm-instrument-tbsslwc` | Supercooled Liquid Water Content Sondes aboard Tethe | DOE/SC-ARM-TR-206 | `olitbsslwcM1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-tbswind` | Anemometers aboard Tethered Balloon System | DOE/SC-ARM-TR-206 | `sgptbswindC1.b1` | 8 | parent hb, class-specific |
| `arm-instrument-uhsas-air` | Ultra-High Sensitivity Aerosol Spectrometer aboard a | DOE/SC-ARM-TR-250 | `sgpaafuhsasF1.b1` | 10 | - |
| `arm-instrument-wcm-air` | Water content meter aboard aircraft | DOE/SC-ARM-TR-261 | _not verified_ | 5 | - |

### Cloud Properties (34)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-2ds-air` | 2 Dimensional Stereo Probe aboard aircraft | DOE/SC-ARM-TR-233 | `sgpaaf2dsvF1.c1` | 12 | - |
| `arm-instrument-blc` | Belfort Laser Ceilometer | ARM TR-040 | `sgpblcprofC1.a1` | 17 | - |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 | - |
| `arm-instrument-ceil` | Ceilometer | DOE/SC-ARM-TR-020 | `sgpceil10mC1.b1` | 16 | - |
| `arm-instrument-cip-air` | Cloud Imaging Probe aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcipF1.b1` | 10 | - |
| `arm-instrument-csapr` | C-Band Scanning ARM Precipitation Radar | DOE/SC-ARM/TR-121 | `corcsapr2cfrzppiqcM1.b1` | 9 | - |
| `arm-instrument-dl` | Doppler Lidar | DOE/SC-ARM-TR-101 | `sgpdlppiC1.b1` | 15 | - |
| `arm-instrument-fcdp-air` | Fast Cloud Droplet Probe aboard aircraft | DOE/SC-ARM-TR-238 | `sgpaaffcdpF1.c1` | 9 | - |
| `arm-instrument-hsrl` | High Spectral Resolution Lidar | DOE/SC-ARM-TR-157 | `sgphsrlscanC1.a1` | 8 | - |
| `arm-instrument-hvps-air` | High Volume Precipitation Spectrometer aboard aircra | DOE/SC-ARM-TR-239 | `sgpaafhvpsF1.c1` | 11 | - |
| `arm-instrument-irsi` | Infra-Red Sky Imager | DOE/SC-ARM-TR-182 | `sgpirsivisC1.b1` | 7 | - |
| `arm-instrument-kasacr` | Ka-Band Scanning ARM Cloud Radar | DOE/SC-ARM/TR-113 | `enakasacrvpthrcC1.b1` | 11 | - |
| `arm-instrument-kazr` | Ka ARM Zenith Radar | DOE/SC-ARM/TR-106 | `sgpkazrcfrmdqcC1.b1` | 10 | - |
| `arm-instrument-mmcr` | Millimeter Wavelength Cloud Radar | ARM TR-018 | `sgpmmcrmomC1.b1` | 14 | - |
| `arm-instrument-mpl` | Micropulse Lidar | DOE/SC-ARM-TR-019 | `sgpminimplC1.b1` | 16 | - |
| `arm-instrument-mwacr` | Marine W-Band (95 GHz) ARM Cloud Radar | ARM-TR-073 | `kcgmwacrcfrqcM1.b1` | 11 | parent hb, system-level |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 | - |
| `arm-instrument-mwr3c` | Microwave Radiometer, 3 Channel | DOE/SC-ARM-TR-108 | `sgpmwr3cC1.b1` | 6 | - |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 | - |
| `arm-instrument-nfov` | Narrow Field of View Zenith Radiometer | DOE/SC-ARM/TR-060 | `sgpnfovC1.b1` | 7 | - |
| `arm-instrument-opc` | Optical Particle Counter | DOE/SC-ARM-TR-343 | `bnfminiaosopcM1.b1` | 21 | **different instrument** |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 | - |
| `arm-instrument-saprvad` | Scanning ARM Precipitation Radar (SAPR) Velocity Azi | DOE/SC-ARM/TR-121 | `sgpxsaprvadI6.c1` | 9 | parent hb, system-level |
| `arm-instrument-stereocam` | Stereo Cameras for Clouds | DOE/SC-ARM-TR-204 | _not verified_ | 10 | - |
| `arm-instrument-swacr` | W-Band (95 GHz) ARM Cloud Radar, mounted to scan | ARM-TR-073 | _not verified_ | 11 | parent hb, system-level |
| `arm-instrument-tbsins` | Ice Nucleation Spectrometer for INP measurements abo | DOE/SC-ARM-TR-206 | `sgptbsinpC1.a1` | 5 | parent hb, class-specific |
| `arm-instrument-tbsslwc` | Supercooled Liquid Water Content Sondes aboard Tethe | DOE/SC-ARM-TR-206 | `olitbsslwcM1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-tsi` | Total Sky Imager | ARM TR-017 | `sgptsiskycoverC1.b1` | 10 | - |
| `arm-instrument-wacr` | W-Band (95 GHz) ARM Cloud Radar | ARM-TR-073 | _not verified_ | 10 | - |
| `arm-instrument-wcm-air` | Water content meter aboard aircraft | DOE/SC-ARM-TR-261 | _not verified_ | 5 | - |
| `arm-instrument-wsacr` | W-band Scanning ARM Cloud Radar | DOE/SC-ARM/TR-113 | `anxwsacrcfrqcM1.b1` | 10 | - |
| `arm-instrument-wsi` | Whole Sky Imager | ARM TR-043 | _not verified_ | 23 | - |
| `arm-instrument-xsacr` | X-Band Scanning ARM  Cloud Radar | DOE/SC-ARM/TR-113 | `houxsacrcfrqcM1.b1` | 11 | - |
| `arm-instrument-xsapr` | X-Band Scanning ARM Precipitation Radar | DOE/SC-ARM/TR-117 | `nsaxsaprcfrqcC1.b1` | 9 | - |

### Radiometric (31)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-aeri` | Atmospheric Emitted Radiance Interferometer | DOE/SC-ARM-TR-054 | `sgpaerisummaryC1.b1` | 14 | - |
| `arm-instrument-amc` | Ameriflux Measurement Component | DOE/SC-ARM-TR-143 | `nsaamcC1.b1` | 7 | - |
| `arm-instrument-assist` | Atmospheric Sounder Spectrometer for Infrared Spectr | DOE/SC-ARM-TR-174 | `magassistsummaryM1.b1` | 20 | - |
| `arm-instrument-brs` | Broadband Radiometer Station | DOE/SC-ARM-TR-025 | `sgpbrs60sC1.b1` | 17 | - |
| `arm-instrument-csphot` | Sunphotometer | DOE/SC-ARM/TR-056 | `sgpcsphotzenradv3C1.a1` | 12 | - |
| `arm-instrument-ebbr` | Energy Balance Bowen Ratio Station | DOE/SC-ARM-TR-037 | `sgp5ebbrE13.b1` | 31 | - |
| `arm-instrument-gndmfr` | Ground Multifilter Radiometer | DOE/SC-ARM-TR-144 | `shbgndmfrC1.b1` | 11 | - |
| `arm-instrument-gndrad` | Ground Radiometers on Stand for Upwelling Radiation | ARM TR-027 | `sgpgndrad25m60sC1.b1` | 7 | - |
| `arm-instrument-gvr` | G-band (183 GHz) Vapor Radiometer | DOE/SC-ARM/TR-076 | `nsagvrC1.c1` | 10 | - |
| `arm-instrument-gvrp` | G-band (183 GHz) Vapor Radiometer Profiler | DOE/SC-ARM/TR-091 | `nsagvrpC1.b1` | 10 | - |
| `arm-instrument-irsi` | Infra-Red Sky Imager | DOE/SC-ARM-TR-182 | `sgpirsivisC1.b1` | 7 | - |
| `arm-instrument-irt` | Infrared Thermometer | - | `sgpirt25mC1.b1` | 12 | - |
| `arm-instrument-irt-air` | Infrared Thermometer - Airborne | DOE/SC-ARM-TR-015 | `bnfaafirtU2.b1` | 12 | parent hb, class-specific |
| `arm-instrument-mfr` | Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpmfr7nch25mC1.b1` | 10 | - |
| `arm-instrument-mfr-air` | Multifilter Radiometer aboard aircraft | DOE/SC-ARM/TR-059 | `sgpmfraafF2.b1` | 8 | parent hb, class-specific |
| `arm-instrument-mfrsr` | Multifilter Rotating Shadowband Radiometer | DOE/SC-ARM-TR-144 | `sgpmfrsr7nchC1.b1` | 12 | - |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 | - |
| `arm-instrument-mwr3c` | Microwave Radiometer, 3 Channel | DOE/SC-ARM-TR-108 | `sgpmwr3cC1.b1` | 6 | - |
| `arm-instrument-mwrhf` | Microwave Radiometer - High Frequency | DOE/SC-ARM-TR-080 | `sgpmwrhfC1.b1` | 9 | - |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 | - |
| `arm-instrument-nfov` | Narrow Field of View Zenith Radiometer | DOE/SC-ARM/TR-060 | `sgpnfovC1.b1` | 7 | - |
| `arm-instrument-nimfr` | Normal Incidence Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpnimfr7nchlangplotC1.c1` | 9 | - |
| `arm-instrument-par` | Photosynthetically Active Radiation Sensors | DOE/SC-ARM-TR-319 | `bnfparS14.b1` | 8 | - |
| `arm-instrument-prp` | Portable Radiation Package | DOE/SC-ARM-TR-198 | `acxprptcmM1.b1` | 19 | - |
| `arm-instrument-rss` | Rotating Shadowband Spectroradiometer | ARM TR-051 | `sgprssC1.b1` | 15 | - |
| `arm-instrument-sashe` | Shortwave Array Spectroradiometer-Hemispheric | - | `sgpsashevisC1.b1` | 21 | - |
| `arm-instrument-sasze` | Shortwave Array Spectroradiometer-Zenith | DOE/SC-ARM-TR-178 | `sgpsaszenirC1.a1` | 13 | - |
| `arm-instrument-sirs` | Solar and Infrared Radiation Station for Downwelling | DOE/SC-ARM-TR-025 | `sgpsirsC1.b1` | 17 | - |
| `arm-instrument-skyrad` | Sky Radiometers on Stand for Downwelling Radiation | ARM TR-026 | `nsaskyrad60sC1.b1` | 1 | - |
| `arm-instrument-smos` | Surface Meteorological Observation System Instrument | DOE/SC-ARM/TR-031 | `sgp30smosA5.a1` | 20 | - |
| `arm-instrument-sws` | Shortwave Spectroradiometer | DOE/SC-ARM/TR-062 | `sgpswsC1.b1` | 7 | - |

### Surface Meteorology (21)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-aosmet` | Meteorological Measurements associated with the Aero | DOE/SC-ARM-TR-184 | `enaaosmetC1.a1` | 6 | - |
| `arm-instrument-disdrometer` | Impact Disdrometer | DOE/SC-ARM-TR-111 | `sgpdisdrometerC1.b1` | 10 | - |
| `arm-instrument-ldis` | Laser Disdrometer | DOE/SC-ARM-TR-137 | `sgpldC1.b1` | 8 | - |
| `arm-instrument-marinemet` | Marine Surface Meteorological Instrumentation | DOE/SC-ARM-TR-086 | `magmarinemet1sM1.b1` | 12 | parent hb, system-level |
| `arm-instrument-masc` | Multi-Angle Snowflake Camera | DOE/SC-ARM-TR-158 | `nsamascC1.b1` | 14 | - |
| `arm-instrument-maws` | Automatic Weather Station | DOE/SC-ARM-TR-195 | `sgpmawsC1.b1` | 8 | - |
| `arm-instrument-met` | Surface Meteorological Instrumentation | DOE/SC-ARM-TR-086 | `nsametC1.b1` | 12 | - |
| `arm-instrument-mettwr` | Surface and Tower Meteorological Instrumentation at  | - | `nsapwsC2.b1` | 0 | - |
| `arm-instrument-metwxt` | WXT520/530 Meteorological Instrument System | DOE/SC-ARM-TR-086 | `crgmetwxtM1.b1` | 12 | parent hb, system-level |
| `arm-instrument-org` | Optical Rain Gauge | DOE/SC-ARM-TR-153 | `sgporgC1.b1` | 3 | - |
| `arm-instrument-precipmet` | Precipitation Meteorological Instruments | DOE/SC-ARM-TR-226 | `sgpprecipmetI9.b1` | 9 | - |
| `arm-instrument-rain` | Rain Gauge | DOE/SC-ARM-TR-110 | `sgprainwbC1.b1` | 14 | - |
| `arm-instrument-smos` | Surface Meteorological Observation System Instrument | DOE/SC-ARM/TR-031 | `sgp30smosA5.a1` | 20 | - |
| `arm-instrument-surthref` | Surface Temperature and Humidity Reference System fo | DOE/SC-ARM/TR-068 | `sgpsurthrefC1.b1` | 6 | - |
| `arm-instrument-tbsdts` | Distributed Temperature Sensing aboard Tethered Ball | DOE/SC-ARM-TR-206 | `sgptbsdtsch1C1.b1` | 10 | parent hb, class-specific |
| `arm-instrument-tbsground` | Tethered Balloon System Ground Measurement | DOE/SC-ARM-TR-206 | `sgptbsgroundC1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-thwaps` | Temperature, Humidity, Wind and Pressure Sensors | ARM TR-030 | `sgpthwapsC1.b1` | 11 | - |
| `arm-instrument-tps` | Total Precipitation Sensor | DOE/SC-ARM/TR-094 | `nsatpsauxC1.b1` | 29 | - |
| `arm-instrument-twr` | Facility-specific multi-level Meteorological Instrum | DOE/SC-ARM/TR-050 | `sgptowermetC1.b1` | 18 | - |
| `arm-instrument-vdis` | Video Disdrometer | DOE/SC-ARM-TR-111 | `sgpvdisdropsC1.b1` | 7 | - |
| `arm-instrument-wb` | Weighing Bucket Precipitation Gauge | DOE/SC-ARM-TR-232 | `sgpwbpluvio2C1.a1` | 11 | - |

### Atmospheric Profiling (19)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-50rwp` | Radar Wind Profiler (50 MHz) | ARM TR-045 | `sgp50rwpwindC1.b1` | 10 | - |
| `arm-instrument-ceilpblht` | Boundary-layer height data with CEIL | DOE/SC-ARM-TR-020 | `sgpceilpblhtC1.b1` | 14 | parent hb, class-specific |
| `arm-instrument-cfh` | Cryogenic Frostpoint Hygrometer | DOE/SC-ARM-TR-210 | `sgpcfhC1.b1` | 14 | - |
| `arm-instrument-cmh-air` | Chilled Mirror Hygrometer aboard aircraft | DOE/SC-ARM-TR-235 | `sgpaafdewpointF1.b1` | 8 | - |
| `arm-instrument-isssonde` | Integrated Sounding System | DOE/SC-ARM-TR-029 | `nsaisssonde10sC1.b1` | 5 | parent hb, system-level |
| `arm-instrument-met-air` | Meteorological Instrumentation aboard Aircraft | DOE/SC-ARM-TR-260 | `bnfaaftrhU2.b1` | 4 | - |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 | - |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 | - |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 | - |
| `arm-instrument-rwp` | Radar Wind Profiler | DOE/SC-ARM-TR-044 | `sgp915rwppreciploC1.b1` | 13 | - |
| `arm-instrument-sodar` | Mini Sound Detection and Ranging | DOE/SC-ARM-TR-154 | `anxsodarM1.b1` | 10 | - |
| `arm-instrument-sonde` | Balloon-Borne Sounding System | DOE/SC-ARM-TR-029 | `sgpsondewnpnC1.b1` | 5 | - |
| `arm-instrument-tbsdts` | Distributed Temperature Sensing aboard Tethered Ball | DOE/SC-ARM-TR-206 | `sgptbsdtsch1C1.b1` | 10 | parent hb, class-specific |
| `arm-instrument-tbsground` | Tethered Balloon System Ground Measurement | DOE/SC-ARM-TR-206 | `sgptbsgroundC1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-tbslws` | Leaf Wetness Sensor aboard Tethered Balloon System | DOE/SC-ARM-TR-206 | _not verified_ | 17 | parent hb, system-level |
| `arm-instrument-tbsmet` | Meteorological Instrumentation aboard TBS | DOE/SC-ARM-TR-206 | `sgptbsimetxq2C1.b1` | 7 | parent hb, class-specific |
| `arm-instrument-tbsslwc` | Supercooled Liquid Water Content Sondes aboard Tethe | DOE/SC-ARM-TR-206 | `olitbsslwcM1.b1` | 4 | parent hb, class-specific |
| `arm-instrument-tbswind` | Anemometers aboard Tethered Balloon System | DOE/SC-ARM-TR-206 | `sgptbswindC1.b1` | 8 | parent hb, class-specific |
| `arm-instrument-twr` | Facility-specific multi-level Meteorological Instrum | DOE/SC-ARM/TR-050 | `sgptowermetC1.b1` | 18 | - |

### Surface/Subsurface Properties (10)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-amc` | Ameriflux Measurement Component | DOE/SC-ARM-TR-143 | `nsaamcC1.b1` | 7 | - |
| `arm-instrument-ebbr` | Energy Balance Bowen Ratio Station | DOE/SC-ARM-TR-037 | `sgp5ebbrE13.b1` | 31 | - |
| `arm-instrument-ecor` | Eddy Correlation Flux Measurement System | DOE/SC-ARM-TR-052 | `enaecorsfC1.b1` | 22 | - |
| `arm-instrument-gndmfr` | Ground Multifilter Radiometer | DOE/SC-ARM-TR-144 | `shbgndmfrC1.b1` | 11 | - |
| `arm-instrument-irt` | Infrared Thermometer | - | `sgpirt25mC1.b1` | 12 | - |
| `arm-instrument-sebs` | Surface Energy Balance System | DOE/SC-ARM-TR-092 | `enasebsC1.b1` | 11 | - |
| `arm-instrument-stamp` | Soil Temperature and Moisture Profiles | DOE/SC-ARM-TR-186 | `bnfstamppcpS40.b1` | 12 | - |
| `arm-instrument-swats` | Soil Water and Temperature System | DOE/SC-ARM-TR-063 | `sgpswatsE13.b1` | 12 | - |
| `arm-instrument-tbsdts` | Distributed Temperature Sensing aboard Tethered Ball | DOE/SC-ARM-TR-206 | `sgptbsdtsch1C1.b1` | 10 | parent hb, class-specific |
| `arm-instrument-tbslws` | Leaf Wetness Sensor aboard Tethered Balloon System | DOE/SC-ARM-TR-206 | _not verified_ | 17 | parent hb, system-level |

### Atmospheric Carbon (9)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-co` | Carbon Monoxide Mixing Ratio System | DOE/SC-ARM/TR-072 | `sgpcoC1.b1` | 13 | - |
| `arm-instrument-co-air` | Carbon Monoxide- Airborne | DOE/SC-ARM/TR-072 | `sgpaafcoF1.c1` | 11 | parent hb, system-level |
| `arm-instrument-co-analyzer` | Carbon Monoxide Analyzer | DOE/SC-ARM-TR-159 | `enaaoscoC1.b1` | 19 | - |
| `arm-instrument-co2flx` | Carbon Dioxide Flux Measurement Systems | DOE/SC-ARM-TR-048 | `sgpco2flxwindC1.b1` | 14 | - |
| `arm-instrument-flask` | Flask Samplers for Carbon Cycle Gases and Isotopes | DOE/SC-ARM-TR-181 | `sgpghgisoflaskC1.b1` | 11 | - |
| `arm-instrument-ghg` | Greenhouse Gas Monitor | DOE/SC-ARM-TR-175 | `oliaosghgcoeffM1.b1` | 6 | - |
| `arm-instrument-pgs` | Precision Carbon Dioxide Mixing Ratio System | DOE/SC-ARM-TR-049 | `sgppgscoeffC1.b1` | 8 | - |
| `arm-instrument-pgsiso` | Precision Gas System Isotope Analyzer | DOE/SC-ARM-TR-237 | `sgppgsisocoeffC1.b1` | 12 | - |
| `arm-instrument-sp2` | Single Particle Soot Photometer | DOE/SC-ARM-TR-169 | `bnfaossp2xrM1.b1` | 10 | - |

### Other (5)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-gps` | Global Positioning System | DOE/SC-ARM-TR-260 | `shbgpsC1.a1` | 3 | - |
| `arm-instrument-ozone` | Ozone Monitor | DOE/SC-ARM-TR-179 | `enaaoso3C1.b1` | 15 | - |
| `arm-instrument-ozone-air` | Ozone Monitor aboard Aircraft | DOE/SC-ARM-TR-179 | `sgpaafo3F1.c1` | 21 | - |
| `arm-instrument-so2` | Sulfur Dioxide Monitor | DOE/SC-ARM-TR-180 | `bnfaosso2M1.b1` | 15 | - |
| `arm-instrument-so2-air` | Sulfur Dioxide Monitor aboard Aircraft | DOE/SC-ARM-TR-180 | `oscaafso2F1.c1` | 17 | - |

### Ocean Observations (2)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-nav` | Navigational Location and Attitude | DOE/SC-ARM-TR-236 | `mosnavM1.a1` | 10 | - |
| `arm-instrument-s-table` | Stabilized Platform | DOE/SC-ARM-TR-166 | `marrphtiltM1.a1` | 12 | - |

### Derived Quantities and Models (1)

| skill | instrument | handbook | example datastream | artifacts | scope |
|---|---|---|---|---|---|
| `arm-instrument-saprvad` | Scanning ARM Precipitation Radar (SAPR) Velocity Azi | DOE/SC-ARM/TR-121 | `sgpxsaprvadI6.c1` | 9 | parent hb, system-level |

`catalog.csv` carries the
attribution in machine-readable form, and a structure test fails the build if any skill
ships without either an author list or an explicit statement that the cover names none.

## What is here

### Aerosols (36)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-acsm` | Aerosol Chemical Speciation Monitor | DOE/SC-ARM-TR-196 | `sgpaosacsmC1.b1` | 10 |
| `arm-instrument-aeth` | Aethalometer | DOE/SC-ARM-TR-156 | `dstaosaeth2spot1mM1.b1` | 12 |
| `arm-instrument-aos` | Aerosol Observing System | - | `sgpnoaaaosavgC1.b1` | 1 |
| `arm-instrument-aps` | Aerodynamic Particle Sizer | DOE/SC-ARM-TR-343 | `enaaosapsC1.b1` | 16 |
| `arm-instrument-caps-pmex` | Cavity Attenuated Phase Shift Extinction Monitor | DOE/SC-ARM-TR-155 | `enaaoscaps3wC1.b1` | 12 |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 |
| `arm-instrument-ccn` | Cloud Condensation Nuclei Particle Counter | DOE/SC-ARM-TR-168 | `sgpaosccn1colspectraC1.b1` | 12 |
| `arm-instrument-ccn-air` | Cloud Condensation Nuclei Particle Counter aboard Aircraft | DOE/SC-ARM-TR-225 | `sgpaafccn2colbF1.b1` | 14 |
| `arm-instrument-clap` | Continuous Light Absorption Photometer | - | `pvcaosclap3wM1.c1` | 21 |
| `arm-instrument-co-analyzer` | Carbon Monoxide Analyzer | DOE/SC-ARM-TR-159 | `enaaoscoC1.b1` | 19 |
| `arm-instrument-cpc` | Condensation Particle Counter | DOE/SC-ARM-TR-145 | `sgpaoscpcC1.b1` | 19 |
| `arm-instrument-cpc-air` | Condensation particle counter aboard aircraft | DOE/SC-ARM-TR-227 | `bnfaafmcpcU2.b1` | 15 |
| `arm-instrument-csphot` | Sunphotometer | DOE/SC-ARM/TR-056 | `sgpcsphotzenradv3C1.a1` | 12 |
| `arm-instrument-hsrl` | High Spectral Resolution Lidar | DOE/SC-ARM-TR-157 | `sgphsrlscanC1.a1` | 8 |
| `arm-instrument-htdma` | Humidified Tandem Differential Mobility Analyzer | DOE/SC-ARM-TR-161 | `enaaoshtdmaC1.b1` | 11 |
| `arm-instrument-ins` | Ice Nucleation Spectrometer for INP measurement | DOE/SC-ARM-TR-278 | `sgpinpC1.a1` | 17 |
| `arm-instrument-mpl` | Micropulse Lidar | DOE/SC-ARM-TR-019 | `sgpminimplC1.b1` | 16 |
| `arm-instrument-msems-air` | ARM Aerial Facility (AAF) Miniaturized Scanning Electrical | DOE/SC-ARM-TR-310 | `bnfaafmsemsU2.b1` | 4 |
| `arm-instrument-nephelometer` | Nephelometer | - | `pvcaosnephwetM1.c1` | 10 |
| `arm-instrument-nephelometer-air` | 3-Wavelength integrating nephelometer aboard aircraft | DOE/SC-ARM-TR-248 | `nsaaafneph10sF1.b1` | 12 |
| `arm-instrument-nimfr` | Normal Incidence Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpnimfr7nchlangplotC1.c1` | 9 |
| `arm-instrument-opc` | Optical Particle Counter | DOE/SC-ARM-TR-343 | `bnfminiaosopcM1.b1` | 21 |
| `arm-instrument-pass` | Photoacoustic Soot Spectrometer | DOE/SC-ARM-TR-123 | `sgpaospass3wC1.a1` | 15 |
| `arm-instrument-pcasp-air` | Passive cavity aerosol spectrometer aboard aircraft | DOE/SC-ARM-TR-241 | `sgpaafpcaspF1.b1` | 10 |
| `arm-instrument-pops` | portable or printed optical particle spectrometer | DOE/SC-ARM-TR-328 | `dstpops1mM1.b1` | 18 |
| `arm-instrument-psap` | Particle Soot Absorption Photometer | DOE/SC-ARM-TR-176 | `pvcaospsap3wM1.c1` | 16 |
| `arm-instrument-psap-air` | Particle soot absorption photometer aboard aircraft | DOE/SC-ARM-TR-262 | `enaaafpsap1sF1.b1` | 11 |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 |
| `arm-instrument-smps` | Scanning mobility particle sizer | DOE/SC-ARM-TR-147 | `enaaossmpsC1.b1` | 20 |
| `arm-instrument-smps-air` | Scanning mobility particle sizer aboard aircraft | DOE/SC-ARM-TR-310 | `coraafsmpsF1.b1` | 4 |
| `arm-instrument-sp2` | Single Particle Soot Photometer | DOE/SC-ARM-TR-169 | `bnfaossp2xrM1.b1` | 10 |
| `arm-instrument-sp2-air` | Single Particle Soot Photometer aboard aircraft | DOE/SC-ARM-TR-169 | `nsaaafsp2rbc10sF1.c1` | 9 |
| `arm-instrument-tap` | Tricolor Absorption Photometer | DOE/SC-ARM-TR-267 | `sgpaostapE13.b1` | 10 |
| `arm-instrument-tdma` | Tandem Differential Mobility Analyzer | DOE/SC-ARM-TR-090 | `sgptdmaapssizeC1.c1` | 20 |
| `arm-instrument-uhsas` | Ultra-High Sensitivity Aerosol Spectrometer | DOE/SC-ARM-TR-163 | `enaaosuhsasC1.b1` | 9 |
| `arm-instrument-uhsas-air` | Ultra-High Sensitivity Aerosol Spectrometer aboard aircraf | DOE/SC-ARM-TR-250 | `sgpaafuhsasF1.b1` | 10 |

### Cloud Properties (29)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-2ds-air` | 2 Dimensional Stereo Probe aboard aircraft | DOE/SC-ARM-TR-233 | `sgpaaf2dsvF1.c1` | 12 |
| `arm-instrument-blc` | Belfort Laser Ceilometer | ARM TR-040 | `sgpblcprofC1.a1` | 17 |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 |
| `arm-instrument-ceil` | Ceilometer | DOE/SC-ARM-TR-020 | `sgpceil10mC1.b1` | 16 |
| `arm-instrument-cip-air` | Cloud Imaging Probe aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcipF1.b1` | 10 |
| `arm-instrument-csapr` | C-Band Scanning ARM Precipitation Radar | DOE/SC-ARM/TR-121 | `corcsapr2cfrzppiqcM1.b1` | 9 |
| `arm-instrument-dl` | Doppler Lidar | DOE/SC-ARM-TR-101 | `sgpdlppiC1.b1` | 15 |
| `arm-instrument-fcdp-air` | Fast Cloud Droplet Probe aboard aircraft | DOE/SC-ARM-TR-238 | `sgpaaffcdpF1.c1` | 9 |
| `arm-instrument-hsrl` | High Spectral Resolution Lidar | DOE/SC-ARM-TR-157 | `sgphsrlscanC1.a1` | 8 |
| `arm-instrument-hvps-air` | High Volume Precipitation Spectrometer aboard aircraft | DOE/SC-ARM-TR-239 | `sgpaafhvpsF1.c1` | 11 |
| `arm-instrument-irsi` | Infra-Red Sky Imager | DOE/SC-ARM-TR-182 | `sgpirsivisC1.b1` | 7 |
| `arm-instrument-kasacr` | Ka-Band Scanning ARM Cloud Radar | DOE/SC-ARM/TR-113 | `enakasacrvpthrcC1.b1` | 11 |
| `arm-instrument-kazr` | Ka ARM Zenith Radar | DOE/SC-ARM/TR-106 | `sgpkazrcfrmdqcC1.b1` | 10 |
| `arm-instrument-mmcr` | Millimeter Wavelength Cloud Radar | ARM TR-018 | `sgpmmcrmomC1.b1` | 14 |
| `arm-instrument-mpl` | Micropulse Lidar | DOE/SC-ARM-TR-019 | `sgpminimplC1.b1` | 16 |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 |
| `arm-instrument-mwr3c` | Microwave Radiometer, 3 Channel | DOE/SC-ARM-TR-108 | `sgpmwr3cC1.b1` | 6 |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 |
| `arm-instrument-nfov` | Narrow Field of View Zenith Radiometer | DOE/SC-ARM/TR-060 | `sgpnfovC1.b1` | 7 |
| `arm-instrument-opc` | Optical Particle Counter | DOE/SC-ARM-TR-343 | `bnfminiaosopcM1.b1` | 21 |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 |
| `arm-instrument-stereocam` | Stereo Cameras for Clouds | DOE/SC-ARM-TR-204 | _not verified_ | 10 |
| `arm-instrument-tsi` | Total Sky Imager | ARM TR-017 | `sgptsiskycoverC1.b1` | 10 |
| `arm-instrument-wacr` | W-Band (95 GHz) ARM Cloud Radar | ARM-TR-073 | _not verified_ | 10 |
| `arm-instrument-wcm-air` | Water content meter aboard aircraft | DOE/SC-ARM-TR-261 | _not verified_ | 5 |
| `arm-instrument-wsacr` | W-band Scanning ARM Cloud Radar | DOE/SC-ARM/TR-113 | `anxwsacrcfrqcM1.b1` | 10 |
| `arm-instrument-wsi` | Whole Sky Imager | ARM TR-043 | _not verified_ | 23 |
| `arm-instrument-xsacr` | X-Band Scanning ARM  Cloud Radar | DOE/SC-ARM/TR-113 | `houxsacrcfrqcM1.b1` | 11 |
| `arm-instrument-xsapr` | X-Band Scanning ARM Precipitation Radar | DOE/SC-ARM/TR-117 | `nsaxsaprcfrqcC1.b1` | 9 |

### Radiometric (29)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-aeri` | Atmospheric Emitted Radiance Interferometer | DOE/SC-ARM-TR-054 | `sgpaerisummaryC1.b1` | 14 |
| `arm-instrument-amc` | Ameriflux Measurement Component | DOE/SC-ARM-TR-143 | `nsaamcC1.b1` | 7 |
| `arm-instrument-assist` | Atmospheric Sounder Spectrometer for Infrared Spectral Tec | DOE/SC-ARM-TR-174 | `magassistsummaryM1.b1` | 20 |
| `arm-instrument-brs` | Broadband Radiometer Station | DOE/SC-ARM-TR-025 | `sgpbrs60sC1.b1` | 17 |
| `arm-instrument-csphot` | Sunphotometer | DOE/SC-ARM/TR-056 | `sgpcsphotzenradv3C1.a1` | 12 |
| `arm-instrument-ebbr` | Energy Balance Bowen Ratio Station | DOE/SC-ARM-TR-037 | `sgp5ebbrE13.b1` | 31 |
| `arm-instrument-gndmfr` | Ground Multifilter Radiometer | DOE/SC-ARM-TR-144 | `shbgndmfrC1.b1` | 11 |
| `arm-instrument-gndrad` | Ground Radiometers on Stand for Upwelling Radiation | ARM TR-027 | `sgpgndrad25m60sC1.b1` | 7 |
| `arm-instrument-gvr` | G-band (183 GHz) Vapor Radiometer | DOE/SC-ARM/TR-076 | `nsagvrC1.c1` | 10 |
| `arm-instrument-gvrp` | G-band (183 GHz) Vapor Radiometer Profiler | DOE/SC-ARM/TR-091 | `nsagvrpC1.b1` | 10 |
| `arm-instrument-irsi` | Infra-Red Sky Imager | DOE/SC-ARM-TR-182 | `sgpirsivisC1.b1` | 7 |
| `arm-instrument-irt` | Infrared Thermometer | - | `sgpirt25mC1.b1` | 12 |
| `arm-instrument-mfr` | Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpmfr7nch25mC1.b1` | 10 |
| `arm-instrument-mfrsr` | Multifilter Rotating Shadowband Radiometer | DOE/SC-ARM-TR-144 | `sgpmfrsr7nchC1.b1` | 12 |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 |
| `arm-instrument-mwr3c` | Microwave Radiometer, 3 Channel | DOE/SC-ARM-TR-108 | `sgpmwr3cC1.b1` | 6 |
| `arm-instrument-mwrhf` | Microwave Radiometer - High Frequency | DOE/SC-ARM-TR-080 | `sgpmwrhfC1.b1` | 9 |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 |
| `arm-instrument-nfov` | Narrow Field of View Zenith Radiometer | DOE/SC-ARM/TR-060 | `sgpnfovC1.b1` | 7 |
| `arm-instrument-nimfr` | Normal Incidence Multifilter Radiometer | DOE/SC-ARM/TR-059 | `sgpnimfr7nchlangplotC1.c1` | 9 |
| `arm-instrument-par` | Photosynthetically Active Radiation Sensors | DOE/SC-ARM-TR-319 | `bnfparS14.b1` | 8 |
| `arm-instrument-prp` | Portable Radiation Package | DOE/SC-ARM-TR-198 | `acxprptcmM1.b1` | 19 |
| `arm-instrument-rss` | Rotating Shadowband Spectroradiometer | ARM TR-051 | `sgprssC1.b1` | 15 |
| `arm-instrument-sashe` | Shortwave Array Spectroradiometer-Hemispheric | - | `sgpsashevisC1.b1` | 21 |
| `arm-instrument-sasze` | Shortwave Array Spectroradiometer-Zenith | DOE/SC-ARM-TR-178 | `sgpsaszenirC1.a1` | 13 |
| `arm-instrument-sirs` | Solar and Infrared Radiation Station for Downwelling and U | DOE/SC-ARM-TR-025 | `sgpsirsC1.b1` | 17 |
| `arm-instrument-skyrad` | Sky Radiometers on Stand for Downwelling Radiation | ARM TR-026 | `nsaskyrad60sC1.b1` | 1 |
| `arm-instrument-smos` | Surface Meteorological Observation System Instruments for  | DOE/SC-ARM/TR-031 | `sgp30smosA5.a1` | 20 |
| `arm-instrument-sws` | Shortwave Spectroradiometer | DOE/SC-ARM/TR-062 | `sgpswsC1.b1` | 7 |

### Airborne Observations (25)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-2ds-air` | 2 Dimensional Stereo Probe aboard aircraft | DOE/SC-ARM-TR-233 | `sgpaaf2dsvF1.c1` | 12 |
| `arm-instrument-aimms20-air` | Aircraft Integrated Meteorological Measurement System aboa | DOE/SC-ARM-TR-260 | `bnfaafnavaims100hzU2.a1` | 4 |
| `arm-instrument-cam-air` | Video camera aboard aircraft | DOE/SC-ARM-TR-231 | _not verified_ | 7 |
| `arm-instrument-cas-air` | Cloud and Aerosol Spectrometer aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcasF1.b1` | 12 |
| `arm-instrument-ccn-air` | Cloud Condensation Nuclei Particle Counter aboard Aircraft | DOE/SC-ARM-TR-225 | `sgpaafccn2colbF1.b1` | 14 |
| `arm-instrument-cip-air` | Cloud Imaging Probe aboard aircraft | DOE/SC-ARM-TR-246 | `enaaafcipF1.b1` | 10 |
| `arm-instrument-cmh-air` | Chilled Mirror Hygrometer aboard aircraft | DOE/SC-ARM-TR-235 | `sgpaafdewpointF1.b1` | 8 |
| `arm-instrument-cpc-air` | Condensation particle counter aboard aircraft | DOE/SC-ARM-TR-227 | `bnfaafmcpcU2.b1` | 15 |
| `arm-instrument-fcdp-air` | Fast Cloud Droplet Probe aboard aircraft | DOE/SC-ARM-TR-238 | `sgpaaffcdpF1.c1` | 9 |
| `arm-instrument-gustprobe-air` | Gust Probe aboard aircraft | DOE/SC-ARM-TR-260 | `sgpaafgust1hzF1.a1` | 4 |
| `arm-instrument-hvps-air` | High Volume Precipitation Spectrometer aboard aircraft | DOE/SC-ARM-TR-239 | `sgpaafhvpsF1.c1` | 11 |
| `arm-instrument-inletcvi-air` | Inlet for Counterflow Virtual Impactor aboard aircraft | DOE/SC-ARM-TR-254 | `sgpaafinletcviF1.c1` | 21 |
| `arm-instrument-inletisok-air` | Isokinetic Inlet aboard aircraft | DOE/SC-ARM-TR-251 | `sgpaafinletisokF1.a1` | 11 |
| `arm-instrument-met-air` | Meteorological Instrumentation aboard Aircraft | DOE/SC-ARM-TR-260 | `bnfaaftrhU2.b1` | 4 |
| `arm-instrument-msems-air` | ARM Aerial Facility (AAF) Miniaturized Scanning Electrical | DOE/SC-ARM-TR-310 | `bnfaafmsemsU2.b1` | 4 |
| `arm-instrument-nav-air` | Navigational Location, Motion, and Attitude for Airborne P | DOE/SC-ARM-TR-236 | `bnfaafnavU2.b1` | 14 |
| `arm-instrument-nephelometer-air` | 3-Wavelength integrating nephelometer aboard aircraft | DOE/SC-ARM-TR-248 | `nsaaafneph10sF1.b1` | 12 |
| `arm-instrument-ozone-air` | Ozone Monitor aboard Aircraft | DOE/SC-ARM-TR-179 | `sgpaafo3F1.c1` | 21 |
| `arm-instrument-pcasp-air` | Passive cavity aerosol spectrometer aboard aircraft | DOE/SC-ARM-TR-241 | `sgpaafpcaspF1.b1` | 10 |
| `arm-instrument-psap-air` | Particle soot absorption photometer aboard aircraft | DOE/SC-ARM-TR-262 | `enaaafpsap1sF1.b1` | 11 |
| `arm-instrument-smps-air` | Scanning mobility particle sizer aboard aircraft | DOE/SC-ARM-TR-310 | `coraafsmpsF1.b1` | 4 |
| `arm-instrument-so2-air` | Sulfur Dioxide Monitor aboard Aircraft | DOE/SC-ARM-TR-180 | `oscaafso2F1.c1` | 17 |
| `arm-instrument-sp2-air` | Single Particle Soot Photometer aboard aircraft | DOE/SC-ARM-TR-169 | `nsaaafsp2rbc10sF1.c1` | 9 |
| `arm-instrument-uhsas-air` | Ultra-High Sensitivity Aerosol Spectrometer aboard aircraf | DOE/SC-ARM-TR-250 | `sgpaafuhsasF1.b1` | 10 |
| `arm-instrument-wcm-air` | Water content meter aboard aircraft | DOE/SC-ARM-TR-261 | _not verified_ | 5 |

### Surface Meteorology (17)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-aosmet` | Meteorological Measurements associated with the Aerosol Ob | DOE/SC-ARM-TR-184 | `enaaosmetC1.a1` | 6 |
| `arm-instrument-disdrometer` | Impact Disdrometer | DOE/SC-ARM-TR-111 | `sgpdisdrometerC1.b1` | 10 |
| `arm-instrument-ldis` | Laser Disdrometer | DOE/SC-ARM-TR-137 | `sgpldC1.b1` | 8 |
| `arm-instrument-masc` | Multi-Angle Snowflake Camera | DOE/SC-ARM-TR-158 | `nsamascC1.b1` | 14 |
| `arm-instrument-maws` | Automatic Weather Station | DOE/SC-ARM-TR-195 | `sgpmawsC1.b1` | 8 |
| `arm-instrument-met` | Surface Meteorological Instrumentation | DOE/SC-ARM-TR-086 | `nsametC1.b1` | 12 |
| `arm-instrument-mettwr` | Surface and Tower Meteorological Instrumentation at NSA | - | `nsapwsC2.b1` | 0 |
| `arm-instrument-org` | Optical Rain Gauge | DOE/SC-ARM-TR-153 | `sgporgC1.b1` | 3 |
| `arm-instrument-precipmet` | Precipitation Meteorological Instruments | DOE/SC-ARM-TR-226 | `sgpprecipmetI9.b1` | 9 |
| `arm-instrument-rain` | Rain Gauge | DOE/SC-ARM-TR-110 | `sgprainwbC1.b1` | 14 |
| `arm-instrument-smos` | Surface Meteorological Observation System Instruments for  | DOE/SC-ARM/TR-031 | `sgp30smosA5.a1` | 20 |
| `arm-instrument-surthref` | Surface Temperature and Humidity Reference System for Sond | DOE/SC-ARM/TR-068 | `sgpsurthrefC1.b1` | 6 |
| `arm-instrument-thwaps` | Temperature, Humidity, Wind and Pressure Sensors | ARM TR-030 | `sgpthwapsC1.b1` | 11 |
| `arm-instrument-tps` | Total Precipitation Sensor | DOE/SC-ARM/TR-094 | `nsatpsauxC1.b1` | 22 |
| `arm-instrument-twr` | Facility-specific multi-level Meteorological Instrumentati | DOE/SC-ARM/TR-050 | `sgptowermetC1.b1` | 18 |
| `arm-instrument-vdis` | Video Disdrometer | DOE/SC-ARM-TR-111 | `sgpvdisdropsC1.b1` | 7 |
| `arm-instrument-wb` | Weighing Bucket Precipitation Gauge | DOE/SC-ARM-TR-232 | `sgpwbpluvio2C1.a1` | 11 |

### Atmospheric Profiling (11)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-50rwp` | Radar Wind Profiler (50 MHz) | ARM TR-045 | `sgp50rwpwindC1.b1` | 10 |
| `arm-instrument-cfh` | Cryogenic Frostpoint Hygrometer | DOE/SC-ARM-TR-210 | `sgpcfhC1.b1` | 14 |
| `arm-instrument-cmh-air` | Chilled Mirror Hygrometer aboard aircraft | DOE/SC-ARM-TR-235 | `sgpaafdewpointF1.b1` | 8 |
| `arm-instrument-met-air` | Meteorological Instrumentation aboard Aircraft | DOE/SC-ARM-TR-260 | `bnfaaftrhU2.b1` | 4 |
| `arm-instrument-mwr` | Microwave Radiometer | DOE/SC-ARM-TR-016 | `sgpmwrlosC1.b1` | 16 |
| `arm-instrument-mwrp` | Microwave Radiometer Profiler | DOE/SC-ARM-TR-057 | `nsamwrpC1.b1` | 11 |
| `arm-instrument-rl` | Raman Lidar | DOE/SC-ARM-TR-038 | _not verified_ | 16 |
| `arm-instrument-rwp` | Radar Wind Profiler | DOE/SC-ARM-TR-044 | `sgp915rwppreciploC1.b1` | 13 |
| `arm-instrument-sodar` | Mini Sound Detection and Ranging | DOE/SC-ARM-TR-154 | `anxsodarM1.b1` | 10 |
| `arm-instrument-sonde` | Balloon-Borne Sounding System | DOE/SC-ARM-TR-029 | `sgpsondewnpnC1.b1` | 5 |
| `arm-instrument-twr` | Facility-specific multi-level Meteorological Instrumentati | DOE/SC-ARM/TR-050 | `sgptowermetC1.b1` | 18 |

### Surface/Subsurface Properties (8)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-amc` | Ameriflux Measurement Component | DOE/SC-ARM-TR-143 | `nsaamcC1.b1` | 7 |
| `arm-instrument-ebbr` | Energy Balance Bowen Ratio Station | DOE/SC-ARM-TR-037 | `sgp5ebbrE13.b1` | 31 |
| `arm-instrument-ecor` | Eddy Correlation Flux Measurement System | DOE/SC-ARM-TR-052 | `enaecorsfC1.b1` | 22 |
| `arm-instrument-gndmfr` | Ground Multifilter Radiometer | DOE/SC-ARM-TR-144 | `shbgndmfrC1.b1` | 11 |
| `arm-instrument-irt` | Infrared Thermometer | - | `sgpirt25mC1.b1` | 12 |
| `arm-instrument-sebs` | Surface Energy Balance System | DOE/SC-ARM-TR-092 | `enasebsC1.b1` | 11 |
| `arm-instrument-stamp` | Soil Temperature and Moisture Profiles | DOE/SC-ARM-TR-186 | `bnfstamppcpS40.b1` | 12 |
| `arm-instrument-swats` | Soil Water and Temperature System | DOE/SC-ARM-TR-063 | `sgpswatsE13.b1` | 12 |

### Atmospheric Carbon (8)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-co` | Carbon Monoxide Mixing Ratio System | DOE/SC-ARM/TR-072 | `sgpcoC1.b1` | 13 |
| `arm-instrument-co-analyzer` | Carbon Monoxide Analyzer | DOE/SC-ARM-TR-159 | `enaaoscoC1.b1` | 19 |
| `arm-instrument-co2flx` | Carbon Dioxide Flux Measurement Systems | DOE/SC-ARM-TR-048 | `sgpco2flxwindC1.b1` | 14 |
| `arm-instrument-flask` | Flask Samplers for Carbon Cycle Gases and Isotopes | DOE/SC-ARM-TR-181 | `sgpghgisoflaskC1.b1` | 11 |
| `arm-instrument-ghg` | Greenhouse Gas Monitor | DOE/SC-ARM-TR-175 | `oliaosghgcoeffM1.b1` | 6 |
| `arm-instrument-pgs` | Precision Carbon Dioxide Mixing Ratio System | DOE/SC-ARM-TR-049 | `sgppgscoeffC1.b1` | 8 |
| `arm-instrument-pgsiso` | Precision Gas System Isotope Analyzer | DOE/SC-ARM-TR-237 | `sgppgsisocoeffC1.b1` | 12 |
| `arm-instrument-sp2` | Single Particle Soot Photometer | DOE/SC-ARM-TR-169 | `bnfaossp2xrM1.b1` | 10 |

### Other (5)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-gps` | Global Positioning System | DOE/SC-ARM-TR-260 | `shbgpsC1.a1` | 3 |
| `arm-instrument-ozone` | Ozone Monitor | DOE/SC-ARM-TR-179 | `enaaoso3C1.b1` | 15 |
| `arm-instrument-ozone-air` | Ozone Monitor aboard Aircraft | DOE/SC-ARM-TR-179 | `sgpaafo3F1.c1` | 21 |
| `arm-instrument-so2` | Sulfur Dioxide Monitor | DOE/SC-ARM-TR-180 | `bnfaosso2M1.b1` | 15 |
| `arm-instrument-so2-air` | Sulfur Dioxide Monitor aboard Aircraft | DOE/SC-ARM-TR-180 | `oscaafso2F1.c1` | 17 |

### Ocean Observations (2)

| skill | instrument | handbook | example datastream | artifacts |
|---|---|---|---|---|
| `arm-instrument-nav` | Navigational Location and Attitude | DOE/SC-ARM-TR-236 | `mosnavM1.a1` | 10 |
| `arm-instrument-s-table` | Stabilized Platform | DOE/SC-ARM-TR-166 | `marrphtiltM1.a1` | 12 |

`catalog.csv` carries the instrument classes the routing helpers need, with columns for
the handbook, authors, report number, the verified example and the datastream inventory -
so they work for instruments without a skill, not just the 150 with one. The copy
published with this skill holds the 279 classes that are ARM-observed or have a
handbook, with `pdf` as a bare filename, because the registry caps a file at 65,536
characters; the ai-skills repo carries all 594 classes with full URLs.
`arm_handbook_url()` accepts either form, and `arm_catalog(live=True)` re-reads ARM's
index when you need a class the shipped copy omits.

Each instrument skill carries: measurement principle in the handbook's own terms, reported
quantities with ranges and uncertainties, the specification table, sampling, calibration
and maintenance, the embedded-QC coverage measured on a real file, the variable inventory
of that file, and **the known artifacts and failure modes the mentor wrote down** -
1726 of them across the tranche, which is
the section that earns the skill, because it is the part no variable name tells you.

## Where the handbooks are

Handbooks live in one flat directory on arm.gov, under two naming conventions:

| pattern | example |
|---|---|
| `{code}_handbook.pdf` | `met_handbook.pdf`, `kazr_handbook.pdf` |
| DOE report number | `doe-sc-arm-tr-343.pdf` (Aerosol Observing System) |

Base URL: `https://www.arm.gov/publications/tech_reports/handbooks/`

`arm_handbook_url(code)` tries both and returns the one that resolves. There is no index
page listing them, and the report-number form cannot be guessed from the instrument code -
it comes out of the catalog record.

Measured 2026-09-23: of 594 instrument classes, **215** have a live
handbook or tech-report PDF, **193** are ARM-observed (`armobs`), and
**128** have all three of a handbook, ARM-observed status and a datastream holding data -
the set with a skill here.

**Some classes have no handbook of their own.** ARM links none to 60 of its ARM-observed
classes. For 21 of them a **parent handbook** was found - the `tbs*` subsystems are documented
in the Tethered Balloon System handbook, `swacr` and `mwacr` in the WACR handbook, `metwxt`
and `marinemet` in the MET handbook - and those skills open with a scope note naming the
parent and saying whether the document is class-specific about them (12 of them) or covers
only the parent system (9, established by full-text search, not assumed). ARM's own
`target_relations` field in the `ds` index is what makes the parent resolvable.

Five candidates were **rejected** rather than published on borrowed facts, each found by
reading the document rather than trusting the filename: `kzr` (K-band, 18-27 GHz - the KAZR
handbook is Ka-band 35 GHz), `navmet-air` (the nav handbook is ship-borne INS),
`nox` (the AOS handbook has no nitrogen-oxides content), `xprecipradar` (the X-SAPR handbook
does not name it), and `opc-air` (TR-343 is the Aerodynamic Particle Sizer handbook).
`catalog.csv` records the reason for each in `no_handbook_reason`. The same check downgraded
the already-published `opc`, whose linked handbook turns out to be the APS document.

**One handbook can cover several instrument classes.** 29 of these skills share a
document with a sibling - DOE/SC-ARM/TR-113 covers `kasacr`, `wsacr` and `xsacr` jointly;
DOE/SC-ARM-TR-260 covers four airborne classes - and each of those skills carries a scope
note saying which numbers are family-level rather than per-instrument. `tap` is the sharpest
case: ARM links it to the SGP Aerosol Observing System handbook, which mentions TAP only in
passing, and its skill says so.

## The catalog API

`arm.gov/capabilities/instruments` is a JavaScript shell over an Elasticsearch proxy, and
arm.gov serves no sitemap. The proxy is public and is the only complete enumeration:

```python
body = {"size": 1000, "query": {"match_all": {}}}
hits = arm_es_query("ds", body)["hits"]["hits"]          # 741 data-source records
```

Two indexes are reachable, named in `arm.gov/build/assets/config-measurements-*.js`:

| index | holds | shape |
|---|---|---|
| `ds` | 741 data sources | instrument classes have **no `type` field** and `_id == instrument_class_code`; typed records are VAPs, PI products and externally funded datasets |
| `measurements` | 129 primary measurement types | each with the instrument classes that supply it, per site |

Two traps. Nested fields (`datastreams`, `categories`, `measurements`, `source_classes`)
arrive as **Python-repr strings, not JSON** - `ast.literal_eval`, which is what
`arm_parse_field` does. And `url_techreport` is the string `"None"`, not null, when absent.

Each instrument-class record carries the full datastream list with per-site, per-facility
date coverage and a `data_available` flag, which is how each skill's example was chosen:
level `c1`/`b1` first, then a permanent facility (C1, M1), then most recent coverage.

## Routing helpers

```python
arm_instrument("kazr")                      # one catalog record
arm_find_instruments("cloud base")          # by name, measurement or category
arm_instruments_for_measurement("Cloud base height")   # live measurements index
arm_handbook_url("ecor")                    # resolved handbook PDF
arm_handbook_pages("ecor")                  # handbook text, page by page
arm_instrument_example("kazr")              # the datastream the skill was verified on
arm_skill_for("kazr")                       # 'arm-instrument-kazr', or None
```

`arm_catalog()` reads the shipped CSV (offline, instant); `arm_catalog(live=True)` re-reads
ARM's index. Prefer the live call when the question is whether something is still deployed.

## Getting the data

Every instrument skill ends in the same place: ARM Live. That machinery is not repeated
150 times - load `act-arm-live` for the service, datastream naming, the server-side
subset endpoint and DOI citation, `act-qc` for the `qc_` flags and Data Quality Reports,
`act-plotting` for the Display family. For the scanning and profiling radars, load
`pyart-foundations` and the `pyart-*` tranche; ARM's radar products are CfRadial and Py-ART
reads them directly.

## What "verified" does and does not mean

142 of the 150 skills were checked against a file that was actually opened. The
other 8 say so in place of a data section, with the reason - aircraft video
averaging 8.7 GB per file (`cam-air`), MPEG products (`stereocam`, `wsi`), datastreams
that exist only at level `a0` which ARM Live will not serve (`rl`), files ARM Live lists
but will not transfer (`wacr`), and a tar containing a nested zip (`wcm-air`). None of
those skills claim a QC or variable inventory it could not measure.

A verified example is one file on one day at one facility. It proves the variable names,
dimensions and QC coverage of that datastream; it is not a quality assessment of the
instrument and not a guarantee that another site's file has the same variables.

## Adding an instrument

`tools/arm_instrument_build/` holds the pipeline: `extract.py` turns handbook PDF text into
page-cited structured facts through a forced tool call, `compose.py` turns those facts plus
the catalog record plus a measured file inventory into a SKILL.md. The order matters -
handbook first, then the file, never the file's names inferred from the handbook.

The rule this directory follows: **the handbook is design intent, the file is current
truth.** Where they disagree, say so rather than picking one.

## Verified against

- ARM data-source catalog read 2026-09-23 - 594 instrument classes, 215 with a live PDF
- Handbook URL patterns probed across all 594 codes on 2026-09-23; 150 handbooks downloaded and text-extracted (including 21 parent handbooks for classes ARM links no handbook to)
- ARM Live queried with `ARMUSER`/`ARMTOKEN`, latest 2026-09-24; 142 files opened with ACT 2.3.4
- Py-ART 2.1.1 used for the radar read path (6 instruments read as Radar objects)
