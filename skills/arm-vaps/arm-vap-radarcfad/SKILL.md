---
name: arm-vap-radarcfad
description: ARM Radar Contoured Frequency by Altitude Diagram (radarcfad) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Radar reflectivity, Relative occurrence frequency, Relative occurrence frequency, ARM radar reflectivity CFAD), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpkazrcfadC1.c1) and the variable inventory of a real file. Use when working with radarcfad data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - radarcfad, Radar Contoured Frequency by Altitude Diagram, sgpkazrcfadC1.c1, Radar reflectivity, Relative occurrence frequency, ARM radar reflectivity CFAD, Cloud Properties.
---

# RADARCFAD - Radar Contoured Frequency by Altitude Diagram

The Radar CFAD (Contoured Frequency by Altitude Diagram) is an ARM value-added product that produces hourly, 100 m vertical-resolution, 5-dBZ-binned reflectivity-height histograms from ARSCL ground-based cloud radar retrievals at ARM sites, used as the observational counterpart for evaluating a companion ARM cloud radar simulator applied to global climate model output.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 23 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `radarcfad` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-190 / Y Zhang, S Xie / September 2017](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-190.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2006-01-01 to 2020-05-31 (retired) |
| Datastreams with data | 16 across 6 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/radarcfad |


## Credit

Everything this skill knows about the retrieval is the work of **Y Zhang, S Xie** -
the ARM developers and mentors who wrote the technical report it derives from:

> Y Zhang, S Xie. *ARM Cloud Radar Simulator Package for Global Climate Models Value-Added Product*, DOE/SC-ARM-TR-190, September 2017.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-190.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The measurement-based CFAD is generated from the ARM value-added cloud product ARSCL (Active Remotely-Sensed Cloud Locations), which applies quality controls and includes only clouds detected by cloud radar. Reflectivity-height data are produced for every hour at 100 m vertical resolution to capture diurnal variability and detailed vertical cloud structure, with dBZ values binned every 5 dBZ over the range -50 dBZ to 25 dBZ. Daily and monthly mean CFADs are computed from the hourly data. The companion ARM cloud radar simulator (built on the QuickBeam/COSP framework) generates pseudo-ARM radar observations from model hydrometeor profiles at 35 GHz (Ka-band) with 100 m vertical resolution, applying the same minimum-sensitivity and saturation thresholds used when processing the real ARM radar observations, so that simulated and observed CFADs can be directly compared.

**Cadence.** output every hourly reflectivity-height data; daily and monthly means also produced; averaging monthly statistics generated from hourly radar CFAD data; monthly-mean joint histogram of reflectivity-height and occurrence frequency (hb p. 8).

## Inputs

The report names these instruments and sibling products: ARSCL (Active Remotely Sensed Cloud Locations), ARM Cloud Radar Simulator VAP, CloudSat simulator/QuickBeam (COSP).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Radar reflectivity (CFAD, joint reflectivity-height... | dBZ | -50 dBZ to 25 dBZ, binned every 5... | - | (hb p. 8) |
| Relative occurrence frequency (ROF) of non-precipitating... | - | reflectivity less than  -20 dBZ | - | (hb p. 12) |
| Relative occurrence frequency (ROF) of precipitating... | - | reflectivity greater than  -20 dBZ | - | (hb p. 13) |
| ARM radar reflectivity CFAD (simulator output,... | dBZ | - | - | (hb p. 12) |
| ARM radar reflectivity, attenuation-corrected (simulator... | dBZ | - | - | (hb p. 12) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| ARM_RADAR_FREQ (ARM Radar Frequency) | 35.0 GHz | (hb p. 11) |
| ARM_SURFACE_RADAR (ARM radar position, surface=1,... | 1 | (hb p. 11) |
| Vertical resolution of ARM simulator/CFAD | 100 m (compared to 500 m for CloudSat) | (hb p. 7) |
| Reflectivity bin width | 5 dBZ | (hb p. 8) |
| Reflectivity range | -50 dBZ to 25 dBZ | (hb p. 8) |
| Larmcfaddbze35 default | True | (hb p. 12) |
| Larmdbz35 default | true | (hb p. 12) |


## The data

Verified example: **`sgpkazrcfadC1.c1`**, file `sgpkazrcfadC1.c1.20170828.000000.nc`
(35.49 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=21600, `time_hour`=24, `range`=2, `height`=200, `dBZ`=15 |
| Data variables | 12 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 4 s |
| File time span | 2017-08-28T00:00:00 to 2017-08-28T23:59:56 |
| dod version | kazrcfad-c1-1.0 |
| process version |  |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `CFAD_high` | % | time_hour,dBZ,height | - | Joint histogram of equivalent reflectivity factor over height with... |
| `CFAD_low` | % | time_hour,dBZ,height | - | Joint histogram of equivalent reflectivity factor over height with... |
| `Reflectivity_BestEstimate` | dBZ | time,height | - | Best-estimate hydrometeor reflectivity statistically aligned with... |
| `Reflectivity_NoClutter` | dBZ | time,height | - | Best-estimate reflectivity statistically aligned with CloudSat with... |
| `dBZ` | dBZ | dBZ | - | dBZe at the middle point of the bin |
| `height` | m | height | - | Height at the middle point of the layer, above mean sea level |
| `time` | - | time | - | Time offset from midnight |
| `time_hour` | hour | time_hour | - | Hourly time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN`; see `act-arm-live` for the service, datastream
naming and the server-side subset endpoint.

The `act-arm-live` and `act-qc` skills wrap these calls in shorter helpers
(`armlive_open`, `armlive_list_files`, `act_qc_table`, `act_qc_apply`). Those are helpers
those skills define, **not** ACT functions - nothing below uses them, so every block here
runs against a bare `act-atmos` install.

```python
import os, requests, act

user, token = os.environ["ARMUSER"], os.environ["ARMTOKEN"]

# ACT has no list-only call, so size the request against ARM Live's query endpoint
# before transferring anything.
avail = requests.get("https://adc.arm.gov/armlive/livedata/query",
                     params={"user": f"{user}:{token}", "ds": "sgpkazrcfadC1.c1",
                             "start": "2017-08-28", "end": "2017-08-28", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpkazrcfadC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpkazrcfadC1.c1", "2017-08-28", "2017-08-28")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpkazrcfadC1.c1", "2017-08-28", "2017-08-28"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpkazrcfadC1.c1", "20060101", "20260924")
```

The report's own note on quality: The observational CFAD is built from ARSCL data with quality controls applied, using only clouds detected by cloud radar. The ARSCL qc_ReflectivityClutterFlag (1 = no evidence of clutter; 2 = potential unknown mixture of hydrometeors and clutter) is used to generate two parallel CFAD products bounding the impact of insect clutter contamination on cloud statistics.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Radar minimum sensitivity threshold (dBZ_min) | Simulated/observed reflectivity values below dBZ_min(h) = -50 + 20*log10(h) [h in km] are absent from the CFAD occurrence calculations, producing an apparent blind zone for weak/small... | Values below this threshold are eliminated from the occurrence calculations in both the simulator and when processing observations, since the ARM... | (hb p. 8) |
| Radar receiver saturation (dBZ_max) | Reflectivity values above dBZ_max(h) = 20 + 20*log10(h) [h in km] appear capped/clipped at the maximum value in the CFAD rather than showing the true (higher) reflectivity. | Values above dBZ_max are set to dBZ_max, representing the saturation limiting value that would actually be measured. | (hb p. 8) |
| Insect clutter contamination at low levels | Elevated/spurious echo below ~3 km, especially prominent during summertime at the SGP site; causes discrepancies of ~15% in non-precipitating low-cloud occurrence between clutter-inclusive... | Two CFAD data products are produced using ARSCL qc_ReflectivityClutterFlag: one using flag=1 (no evidence of clutter; may underestimate cloud amount... | (hb p. 9) |
| Ambiguous clutter/hydrometeor mixture (qc_ReflectivityClutterFlag=2) | Data flagged as flag=2 represent an unknown mixture of hydrometeors and clutter, introducing uncertainty in whether a given reflectivity bin represents real cloud/precipitation or... | Handled by producing two separate CFAD datasets (flag=1 only vs. flag=1&2) to bound the impact. | (hb p. 9) |
| Missing model input variables for simulator | Simulator can still run if certain hydrometeor variables (e.g., effective radius or graupel flux) are absent from the climate model output, though this changes what radar signal... | ARM cloud radar simulator automatically handles and runs satisfactorily even without all variables present. | (hb p. 12) |
| Spatial/representativeness mismatch between single-point radar and GCM grid cell | Direct comparison between ground-based single-point cloud radar measurements and large GCM grid-cell output shows systematic differences unless a subgrid-scale distribution/simulator... | The ARM cloud radar simulator converts model data into pseudo-ARM observations mimicking the narrow atmospheric column view of the radar, enabling... | (hb p. 7) |
| Model underestimation of shallow cumulus / boundary-layer clouds | In ACME v0 model-vs-observation comparison, modeled diurnal cycle of non-precipitating clouds fails to capture daytime shallow cumulus occurrence seen in observations (Figure 4a vs 4b). | - | (hb p. 12) |
| Model overestimation of precipitating hydrometeors and incorrect diurnal timing of... | Modeled precipitating-cloud ROF is too high at all levels and peaks near 4 PM LST, whereas observations show a nighttime peak near midnight linked to mesoscale convective systems that... | - | (hb p. 13) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Bodas-Salcedo, A., MJ Webb, S Bony, H Chepfer, J-L Dufresne, SA Clein, Y Zhang, and R Marchand. 2011. "COSP: Satellite simulation software for model assessment." Bulletin of the American Meteorological Society 92:...
- Haynes, JM, Z Luo, GL Stephens, RT Marchand, and A Bodas-Salcedo. 2007. "A multi-purpose radar simulation package: QuickBeam." Bulletin of the American Meteorological Society 88: 1723-1727,...
- Klein, SA, Y Zhang, MD Zelinka, R Pincus, J Boyle, and PJ Gleckler. 2013. "Are climate model simulations of clouds improving? An evaluation using the ISCCP simulator." Journal of Geophysical Research – Atmospheres...
- Luke, EP, P Kollias, KL Johnson, and EE Clothiaux. 2008. "A technique for the automatic detection of insect clutter in cloud radar returns." Journal of Atmospheric and Oceanic Technology 25(9): 1498-1513,...
- Marchand, RJ, J Haynes, GG Mace, T Ackerman, and G Stephens. 2009. "A comparison of simulated cloud radar output from the multiscale modeling framework global climate model with CloudSat cloud radar observations."...
- Zhang, Y, S. A Klein, J Boyle, and GC Mace. 2010. "Evaluation of tropical cloud and precipitation statistics of Community Atmosphere Model version 3 using CloudSat and CALIPSO data." Journal of Geophysical Research –...
- Zhang, Y., S Xie, et al. 2017. "The ARM cloud radar simulator for global climate models: A new tool for bridging field data and climate models." Submitted to BAMS.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-190.pdf (23 pages, DOE/SC-ARM-TR-190, by Y Zhang, S Xie)
- Catalog record: ARM data-source index, `instrument_class_code=radarcfad`, read 2026-09-24
- Example file: `sgpkazrcfadC1.c1.20170828.000000.nc` from `sgpkazrcfadC1.c1`, 35.49 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
