---
name: arm-instrument-ceilpblht
description: ARM Boundary-layer height data with CEIL (ceilpblht) - handbook-derived instrument reference. Measurement principle, reported quantities (bl_height_1, bl_height_2, bl_height_3, bl_index_1, bl_index_2, bl_index_3, backscatter), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpceilpblhtC1.b1) and the variable inventory of a real file. Use when working with ceilpblht data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Atmospheric Profiling. Triggers - ceilpblht, Boundary-layer height data with CEIL, sgpceilpblhtC1.b1, bl_height_1, bl_height_2, bl_height_3, bl_index_1, bl_index_2, bl_index_3, Atmospheric Profiling, Vaisala CL31 (BL-View software product ceilpblht, CEIL, DQPR, mrad, lidar.
---

# CEILPBLHT - Boundary-layer height data with CEIL

CEILPBLHT is the derived planetary boundary layer height product (bl_height_1/2/3, below 4000 m) computed by the Vaisala CL31 ceilometer's BL-View backscatter-gradient analysis from the same vertically-pointed, ground-based laser backscatter profiles used for cloud-base detection at ARM fixed and mobile sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ceilpblht` |
| Handbook | [DOE/SC-ARM-TR-020 / VR Morris / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf) |
| Measurement category | Atmospheric Profiling |
| Manufacturer / model | Vaisala CL31 (BL-View software product ceilpblht; parent hardware also deployed historically as Vaisala CT25K and originally Belfort 7013C, which did not produce this product) |
| Primary measurements | Planetary boundary layer height |
| Record | 2011-06-09 to 2026-09-24 (active) |
| Datastreams with data | 38 across 23 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, guc, hou, kcg, mag |
| ARM page | https://www.arm.gov/capabilities/instruments/ceilpblht |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Ceilometer Instrument Handbook*, DOE/SC-ARM-TR-020, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

> **Scope of this handbook.** For `ceilpblht`, ARM links no handbook to this class. The facts below come from the **Ceilometer** (`ceil`) handbook, which documents the parent system. Treat anything that must be per-instrument - a frequency, a detection limit, a serial number - as unverified for `ceilpblht` until checked against that document's own section for it.

## How it measures

The ceilometer transmits short pulses of near-infrared (910 nm) laser light vertically and measures the time delay of light backscattered by aerosols, haze, and cloud droplets, converting delay to height via h = ct/2. The stored backscatter profile (signal strength vs. height) is range- and sensitivity-normalized (multiplied by height-squared to remove the inverse-square falloff) to reveal the vertical structure of scattering layers. For the planetary boundary layer height product specifically, the BL-View software analyzes gradients/features in this normalized backscatter profile to identify candidate mixing-layer/aerosol-layer heights, reported as up to three boundary-layer height candidates (bl_height_1, bl_height_2, bl_height_3) each below 4000 m, with an associated quality index (bl_index_1/2/3) for each candidate. This backscatter-gradient PBL retrieval was enabled starting with the 2010 CL31 deployment, which included improved algorithms for mixing-layer height over the prior CT25K units.

**Siting.** The CEILs at ARM sites are normally operated in vertical orientation on a concrete foundation pad at least 200 mm thick (mounting-bolt hole depth 160 mm), pad width 500 mm or larger with a square bolt pattern 283 mm on a side; the pad is usually oriented with one side pointing north-south, and the shield door faces north in the northern hemisphere / south in the southern hemisphere. Critically for the PBL product, the automatic tilt-angle correction of heights (angle_corr) was disabled in 2013 (BCR-1916) specifically to enable derivation of the planetary boundary layer height, meaning reported bl_height and cloud-base heights are NOT corrected for the instrument's tilt angle.

**Sampling.** native rate digital sampling of return signal every 67 ns from 0 to 50 µs (measurement interval 2 s per Table 11); message/reporting interval 16 s; reported every 16 s (set message interval 16) (hb p. 14).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| bl_height_1 (first boundary layer height candidate) | m | below 4000 m | - | - | (hb p. 12) |
| bl_height_2 (second boundary layer height candidate) | m | below 4000 m | - | - | (hb p. 12) |
| bl_height_3 (third boundary layer height candidate,... | m | below 4000 m | - | - | (hb p. 12) |
| bl_index_1 (quality index for first BL height candidate) | unitless | - | - | - | (hb p. 13) |
| bl_index_2 (quality index for second BL height candidate) | unitless | - | - | - | (hb p. 14) |
| bl_index_3 (quality index for third BL height candidate) | unitless | - | - | - | (hb p. 14) |
| backscatter | 1/(srad*km*10000) | - | ± 0.1 * 10-3 srad-1 km-1 (range- and... | - | (hb p. 12) |


## Specifications

| parameter | value | source |
|---|---|---|
| Range | 0–7.5 km | (hb p. 21) |
| Vertical resolution | 10 m | (hb p. 21) |
| Accuracy (against reflector) | ±1% or ±5m | (hb p. 21) |
| Measurement interval | 2 s | (hb p. 21) |
| Reporting interval | 16 s | (hb p. 21) |
| Wavelength | 910 nm at 25°C | (hb p. 21) |
| Transmitter | Indium Gallium Arsenide pulsed diode laser | (hb p. 21) |
| Receiver | Silicon Avalanche Photodiode | (hb p. 21) |
| Field of view divergence | ±0.83 mrad | (hb p. 21) |
| Dimensions | 1190 x 335 x 324 mm | (hb p. 21) |
| Weight | 32 kg | (hb p. 21) |
| Power | 115 VAC, 310 W max. | (hb p. 21) |
| bl_height_1/2/3 min/max | 0 to 4000 m | (hb p. 14) |
| set message angle_corr | off (heights correction for tilt angle disabled; required for PBL height derivation, BCR-1916) | (hb p. 20) |


## The data

Verified example: **`sgpceilpblhtC1.b1`**, file `sgpceilpblhtC1.b1.20260919.000000.nc`
(0.4 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=5400 |
| Data variables | 19 |
| QC variables | 3 (`qc_` companions) |
| Median time step | 16 s |
| File time span | 2026-09-19T00:00:00 to 2026-09-19T23:59:44 |
| averaging interval | data_update_period * sample_count |
| dod version | ceilpblht-b1-2.0 |
| process version | ingest-ceilpblht-2.0-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `first_cbh` | m | time | yes | Lowest cloud base height detected |
| `second_cbh` | m | time | yes | Second lowest cloud base height detected |
| `third_cbh` | m | time | yes | Third lowest cloud base height detected |
| `bl_height_1` | m | time | - | First boundary layer height candidate |
| `bl_height_2` | m | time | - | Second boundary layer height candidate |
| `bl_height_3` | m | time | - | Third boundary layer height candidate |
| `bl_index_1` | 1 | time | - | Quality index for first boundary layer height candidate |
| `bl_index_2` | 1 | time | - | Quality index for second boundary layer height candidate |
| `bl_index_3` | 1 | time | - | Quality index for third boundary layer height candidate |
| `detection_status` | 1 | time | - | Detection status |
| `sample_count` | 1 | time | - | Number of samples averaged to calculate the current BL_HEIGHTs |
| `time` | - | time | - | Time offset from midnight |


## Getting the data

ARM Live needs `ARMUSER` / `ARMTOKEN` credentials; see the `act-arm-live` skill for the
service, datastream naming and the server-side subset endpoint.

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
                     params={"user": f"{user}:{token}", "ds": "sgpceilpblhtC1.b1",
                             "start": "2026-09-19", "end": "2026-09-19", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpceilpblhtC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpceilpblhtC1.b1", "2026-09-19", "2026-09-19")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpceilpblhtC1.b1", "2026-09-19", "2026-09-19"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("first_cbh", assessment_overplot=True)   # QC-flagged points in red/orange
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


## Quality control in this datastream

3 `qc_` companion variables cover 3 of the
19 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_first_cbh"].attrs.get("flag_meanings", "no flag_meanings"))
mask = ds.qcfilter.get_masked_data("first_cbh", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["first_cbh", "second_cbh", "third_cbh"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpceilpblhtC1.b1.20260919.000000.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `third_cbh` | Value is equal to missing_value. | 5397 | 99.9444 |
| `second_cbh` | Value is equal to missing_value. | 5383 | 99.6852 |
| `first_cbh` | Value is equal to missing_value. | 4954 | 91.7407 |
| `bl_height_1` | strong_layer | 4402 | 81.5185 |
| `bl_height_1` | significant_layer | 895 | 16.5741 |
| `bl_height_2` | significant_layer | 598 | 11.0741 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
try:
    act.qc.print_dqr("sgpceilpblhtC1.b1", "20110609", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The handbook's own note on data quality: Most fields, including bl_height_1/2/3, carry a companion qc_less than fieldnamegreater than  flag (values 0-15) encoding missing-data, below-minimum, above-maximum, and delta-check failures at the b1 level; thresholds for bl_height_1/2/3 are min 0 m, max 4000 m (no delta threshold specified, shown as '-'). A qc_time field (values 0,1,2,4) flags duplicate samples or samples outside the 14-16 s expected interval. Weekly, the instrument mentor inspects time-series plots comparing CEIL backscatter/cloud heights against the MPL, checks for internal consistency (cloud detection up to the 7.7 km...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Tilt-angle correction disabled for PBL derivation | Reported bl_height_1/2/3 and cloud-base heights are not corrected for actual instrument tilt; a diurnal oscillation of measured tilt angle from 0 to 3 degrees appears in tilt_angle... | Disabled intentionally in 2013 (BCR-1916) to allow PBL height determination; user should be aware heights are uncorrected for tilt | (hb p. 16) |
| status_flag 'Alarm' during daily window cleaning | Brief Alarm status in status_flag field coincides with daily maintenance window (water/alcohol cleaning) | None stated beyond noting cause | (hb p. 10) |
| CT25K vs CL31 transition changes tilt-angle handling and data continuity | CT25K tilt angle measurement was accurate and heights were automatically corrected; after replacement with CL31 in 2010 (BCR-1647), tilt-angle correction was disabled, creating a... | None beyond documenting the change | (hb p. 11) |
| Backscatter/cloud-height sensitivity drift with instrument aging | Instrument-derived cloud-ceiling height product may drift with time if relative sensitivity of the instrument degrades considerably; drift may not be noticed until differences arise... | Annual calibration check of laser transmitter to ensure 10 m range resolution | (hb p. 6) |
| Limited sensitivity relative to MPL for thin clouds / boundary-layer signal | CEIL (using vertical-visibility threshold of 100 m) will not classify thin cloud/aerosol layers that the more sensitive photon-counting MPL detects; CEIL usually reports slightly higher... | Use in combination with MPL; MPL comparison used as a Quality Measurement Experiment | (hb p. 10) |
| Daytime/nighttime sensitivity change | A change in daytime/nighttime sensitivity is present in the backscatter data, affecting comparability of layer/cloud detections between day and night | None stated beyond noting it when comparing MPL and CEIL | (hb p. 12) |
| Solar radiation exposure causing alarms | Direct solar radiation exposure may cause alarms and temporarily invalidate data even though optics are solar-protected | Optical filters protect transmitter/receiver diodes; no additional window protection needed, but data may still be temporarily invalid during such... | (hb p. 10) |
| Window contamination | Warning flags for window contamination appear during weekly mentor inspection of data; window transmission estimate (window_transmission %) diagnostic variable can show reduced values | Weekly inspection by instrument mentor for minimal warning flags for window contamination; daily cleaning of window | (hb p. 11) |
| Range/height ceiling of PBL product (4000 m) vs. cloud product ceiling (7700 m) | bl_height_1/2/3 values are bounded to 0-4000 m (QC max threshold), so any boundary-layer feature above 4000 m would not be captured/would fail max-value QC check, unlike cloud-base heights... | None stated; reflects instrument configuration for aerosol/mixing-layer application | (hb p. 14) |
| Heights not adjusted for altitude/AGL vs ASL ambiguity | Cloud/PBL height values are measured above the optics assembly and are not adjusted for site altitude (not distinguished as AGL vs ASL in the output) | None stated; user must be aware heights are relative to instrument, not sea level | (hb p. 10) |
| Data quality flag combinations for missing/min/max/delta failures | qc_less than fieldnamegreater than  flags (0-15) indicate missing data, below-minimum, above-maximum, or delta-check failures for bl_height_1/2/3 among other fields (min 0, max 4000 m... | Automated per-sample QC field qc_less than fieldnamegreater than  generated for each primary/diagnostic variable; DQPRs/DQRs submitted as needed | (hb p. 8) |
| Time quality / duplicate or missing sample timing | qc_time flag values 0-4 indicate duplicate samples (Dt=0), Dt below 14 s lower limit, or Dt above 16 s upper limit, signaling timing irregularities in the datastream | qc_time field supplied to help detect duplicate/missing samples or timing problems | (hb p. 9) |
| Beam overlap / near-range blind zone minimized but present | Overlapping transmit/receive optics improve detection of thin clouds/layers to about 10 m above the ceilometer, implying limited but nonzero blind range below that height | Overlapping optics design specifically to reduce this near-range limitation, relevant for Arctic low-cloud conditions | (hb p. 10) |
| Assumption of constant Lidar Ratio (k) in backscatter-to-extinction inversion | Errors in derived extinction/visibility (and by extension layer detection) arise if the assumed k (typically 0.03 srad-1, ranging 0.02-0.05 depending on humidity, wider range in... | None beyond noting that assumptions are 'fairly truthful' and adequate for cloud detection purposes | (hb p. 16) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Laser transmitter calibration checked against a known-distance hard target: measurement unit removed from shield, placed horizontally, tilt-angle correction turned off, and return detected from a solid object at least 300 m from the ceilometer to verify range resolution of 10 m; see also Vaisala 'CL31 verification of... (hb p. 17) |
| Calibration interval | Checked every year (hb p. 17) |
| Traceability | Comparison with MPL heights during low cloud situations can also be informative; per-unit calibration factors recorded in Table 12 with dates (e.g., F1040001/CLT321 F0550002, factor 2074, 03/08/2010) (hb p. 17) |
| Routine maintenance | Daily preventative maintenance includes cleaning the window with water and/or alcohol, during which the status_flag field is briefly set to 'Alarm'. (hb p. 10) |
| Maintenance interval | Daily (window cleaning); annual (calibration check) (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Micro Pulse Lidar (MPL), Vaisala CT25K Ceilometer (predecessor), Belfort 7013C Laser Ceilometer (original predecessor).

### Acronyms the handbook defines

| term | meaning |
|---|---|
| `AGL` | above ground level |
| `AMF` | ARM Mobile Facility |
| `ARM` | Atmospheric Radiation Measurement Climate Research Facility |
| `CEIL` | Ceilometer |
| `DQPR` | Data Quality Problem Report |
| `DQR` | Data Quality Report |
| `ENA` | Eastern North Atlantic, an ARM site |
| `MOR` | Meteorological Optical Range |
| `MPL` | Micro Pulse Lidar |
| `mrad` | milliradian |
| `NSA` | North Slope of Alaska, an ARM site |
| `QME` | Quality Measurement Experiment |
| `SGP` | Southern Great Plains, an ARM megasite |
| `VAP` | Value-Added Product |


### References the handbook cites

- Bowen, R., R Calhoun, and J Rasanen. 2002. "Ceilometer boundary layer measurements during the DOE/VTMX/URBAN Field Experiment in Salt Lake City." Fourth Symposium on Urban Environment, American Meteorological Society.
- Emeis, S, C Munkel, S Vogt, WJ Muller, and K Schafer. 2004. "Atmospheric boundary-layer structure from simultaneous SODAR, RASS, and ceilometer measurements." Atmospheric Environment 38(2): 273-286,...
- Emeis, S, K Schäfer, and C Münkel. 2009. "Observation of the structure of the urban boundary layer with different ceilometers and validation by RASS data." Meteorologische Zeitschrift 18(2): 149-154,...
- Münkel, C. 2007. "Mixing height determination with lidar ceilometers – results from Helsinki Testbed." Meteorologische Zeitschrift 16(4): 451-459, doi:10.1127/0941-2948/2007/0221.
- Münkel, C, N Eresmaa, J Rasanen, and A Karppinen. 2007. "Retrieval of mixing height and dust concentration with lidar ceilometer." Boundary-Layer Meteorology: doi:10.1007/s10546-006-9103-3.
- Van Tricht, K, IV Gorodetskaya, S Lhermitte, DD Turner, JH Schween, and NPM van Lipzig. 2014. "An improved algorithm for polar cloud-base detection by ceilometer over the ice sheets." Atmospheric Measurement Techniques...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf (26 pages, DOE/SC-ARM-TR-020, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=ceilpblht`, read 2026-09-24
- Example file: `sgpceilpblhtC1.b1.20260919.000000.nc` from `sgpceilpblhtC1.b1`, 0.4 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
