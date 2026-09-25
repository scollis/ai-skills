---
name: arm-instrument-ceil
description: ARM Ceilometer (ceil) - handbook-derived instrument reference. Measurement principle, reported quantities (Backscatter, first_cbh, second_cbh, third_cbh, vertical_visibility, bl_height_1, bl_height_2, bl_height_3), specifications, calibration, embedded QC coverage, and the known artifacts and failure modes documented by the instrument mentor. Includes a verified ARM Live example (sgpceil10mC1.b1) and the variable inventory of a real file. Use when working with ceil data, interpreting its variables or QC flags, judging whether an artifact is instrumental, or choosing a datastream for this measurement. Category - Cloud Properties. Triggers - ceil, Ceilometer, sgpceil10mC1.b1, Backscatter, first_cbh, second_cbh, third_cbh, vertical_visibility, bl_height_1, Cloud Properties, Vaisala CL31 (formerly Belfort 7013C and Vaisala CT25K), CEIL, DQPR.
---

# CEIL - Ceilometer

The CEIL is a self-contained, ground-based, active remote-sensing device that measures cloud-base height (up to three layers), vertical visibility, and potential aerosol backscatter, deployed vertically at ARM fixed and mobile sites.

Every number below is traceable to one of three sources, marked inline: the instrument
handbook (`hb p. N`, 26 pages), ARM's data-source catalog, or the example file
listed under **The data** - opened, not assumed. Verified 2026-09-23.

|  |  |
|---|---|
| ARM class code | `ceil` |
| Handbook | [DOE/SC-ARM-TR-020 / VR Morris / April 2016](https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf) |
| Measurement category | Cloud Properties |
| Manufacturer / model | Vaisala CL31 (formerly Belfort 7013C and Vaisala CT25K) |
| Primary measurements | Backscatter depolarization ratio; Backscattered radiation; Cloud base height; Lidar polarization |
| Record | 1996-10-11 to 2026-09-23 (active) |
| Datastreams with data | 87 across 34 sites |
| Sites | acx, anx, asi, awr, bnf, cor, crg, dst, ena, epc, fkb, gan, grw, guc |
| ARM page | https://www.arm.gov/capabilities/instruments/ceil |


## Credit

Everything this skill knows about the instrument is the work of **VR Morris** -
the ARM instrument mentor(s) who wrote the handbook it derives from:

> VR Morris. *Ceilometer Instrument Handbook*, DOE/SC-ARM-TR-020, April 2016.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf

Cite the handbook, not this skill, for any fact marked `hb p. N`. This file is a
navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the handbook the handbook is right.

## How it measures

The ceilometer transmits short pulses of near-infrared light from a pulsed diode laser and measures the time delay for backscattered light to return from clouds, precipitation, or aerosols, using h = ct/2 to convert time delay to height. The instantaneous return-signal magnitude provides backscatter information at each height, and since fog/precipitation attenuate the pulse, the cloud-base signal appears lower in magnitude and must be compensated for attenuation. Many laser pulses are summed to improve signal-to-noise ratio since ambient light noise otherwise exceeds the weak backscattered signal. The height-square power dependence of a clear atmosphere is removed by height normalization, and the volume backscatter coefficient beta(z) = k*sigma(z) relates backscatter to the extinction coefficient sigma, which itself relates to visibility (sigma = 3/V under the 5% contrast MOR definition), enabling inversion of the backscatter profile to obtain extinction and vertical-visibility estimates.

**Siting.** CEILs at ARM sites are normally operated in vertical orientation. Instruments are placed on a foundation: a concrete pad at least 200 mm thick (mounting bolt hole depth 160 mm), width 500 mm or larger (bolt spacing square pattern 283 mm on a side), usually oriented so one side points north-south. The shield is mounted onto the foundation so the door faces north in the northern hemisphere and south in the southern hemisphere, with the measurement unit installed into the shield afterward.

**Sampling.** native rate digitally samples return signal every 67 nanoseconds (ns) from 0 to 50 µs; measurement interval 2 s; reported every 16 s (message delivery interval) (hb p. 14).

## Reported quantities

As specified by the handbook. These are the physical quantities, not the netCDF
variable names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | resolution | source |
|---|---|---|---|---|---|
| Backscatter | 1/(srad*km*10000) | - | ± 0.1 * 10-3 srad-1 km-1 | - | (hb p. 6) |
| first_cbh (lowest cloud base height) | m | 0-7700 m | ± 5 m | 10 m | (hb p. 6) |
| second_cbh (second-lowest cloud base height) | m | 0-7700 m | ± 5 m | 10 m | (hb p. 6) |
| third_cbh (third cloud base height) | m | 0-7700 m | ± 5 m | 10 m | (hb p. 6) |
| vertical_visibility | m | 0-7700 m | ± 5 m | 10 m | (hb p. 6) |
| bl_height_1 (first boundary layer height candidate) | m | 0-4000 m | - | - | (hb p. 6) |
| bl_height_2 (second boundary layer height candidate) | m | 0-4000 m | - | - | (hb p. 6) |
| bl_height_3 (third boundary layer height candidate) | m | 0-4000 m | - | - | (hb p. 6) |


## Specifications

| parameter | value | source |
|---|---|---|
| Range | 0–7.5 km | (hb p. 15) |
| Vertical resolution | 10 m | (hb p. 15) |
| Accuracy (against reflector) | ±1% or ±5m | (hb p. 15) |
| Measurement interval | 2 s | (hb p. 15) |
| Reporting interval | 16 s | (hb p. 15) |
| Wavelength | 910 nm at 25°C | (hb p. 15) |
| Transmitter | Indium Gallium Arsenide pulsed diode laser | (hb p. 15) |
| Receiver | Silicon Avalanche Photodiode | (hb p. 15) |
| Field of view divergence | ±0.83 mrad | (hb p. 15) |
| Dimensions | 1190 x 335 x 324 mm | (hb p. 15) |
| Weight | 32 kg | (hb p. 15) |
| Power | 115 VAC, 310 W max. | (hb p. 15) |
| Maximum vertical range (Model CL31) | 7700 m | (hb p. 1) |


## The data

Verified example: **`sgpceil10mC1.b1`**, file `sgpceil10mC1.b1.20260918.000012.nc`
(17.48 MB), pulled from ARM Live and opened with ACT on 2026-09-23.

|  |  |
|---|---|
| Dimensions | `time`=5400, `bound`=2, `range`=770 |
| Data variables | 34 |
| QC variables | 11 (`qc_` companions) |
| Median time step | 16 s |
| File time span | 2026-09-18T00:00:12 to 2026-09-18T23:59:54 |
| sampling interval | 1/(10 kHz) |
| averaging interval | 16 seconds |
| dod version | ceil10m-b1-2.0 |
| process version | ingest-ceil-1.10-0.el9 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `alt_highest_signal` | m | time | yes | Altitude of highest signal |
| `background_light` | mV | time | yes | Background light |
| `first_cbh` | m | time | yes | Lowest cloud base height detected |
| `laser_pulse_energy` | % | time | yes | Laser pulse energy |
| `laser_temperature` | degC | time | yes | Laser temperature |
| `second_cbh` | m | time | yes | Second lowest cloud base height |
| `sum_backscatter` | 1/(sr*10000) | time | yes | Sum of detected and normalized backscatter |
| `third_cbh` | m | time | yes | Third cloud base height |
| `tilt_angle` | degree | time | yes | Tilt angle |
| `vertical_visibility` | m | time | yes | Vertical visibility |
| `window_transmission` | % | time | yes | Window transmission estimate |
| `backscatter` | 1/(sr*km*10000) | time,range | - | Backscatter |
| `detection_status` | 1 | time | - | Detection status |
| `measurement_parameters` | 1 | time | - | Instrument measurement parameters |
| `range` | m | range | - | Distance to the center of the corresponding range bin |
| `status_flag` | 1 | time | - | Ceilometer status indicator |
| `status_string` | 1 | time | - | Warning, alarm, and internal status information |
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
                     params={"user": f"{user}:{token}", "ds": "sgpceil10mC1.b1",
                             "start": "2026-09-18", "end": "2026-09-18", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpceil10mC1.b1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpceil10mC1.b1", "2026-09-18", "2026-09-18")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpceil10mC1.b1", "2026-09-18", "2026-09-18"))   # cite what you pulled
```

Lidar profile products are time-height; `act-plotting`'s `TimeSeriesDisplay` with
`plot_time_height_xsection_from_1d_data` or a direct `pcolormesh` on the range
coordinate is the usual view.

## Quality control in this datastream

11 `qc_` companion variables cover 11 of the
34 data variables. Assessments present in the example file: `Bad`.

`cleanup_qc=True` on read is what makes these usable - it rewrites ARM's flag
attributes into the form `qcfilter` expects. Remember that ARM uses two assessment vocabularies - `Bad`/`Indeterminate`
from the automated tests, `Incorrect`/`Suspect` after DQR normalisation - and that
filtering on only one of them silently keeps known-bad points.

```python
# What each test would remove, one variable at a time
print(ds["qc_first_cbh"].attrs["flag_meanings"])
mask = ds.qcfilter.get_masked_data("first_cbh", rm_assessments=["Bad", "Indeterminate"],
                                  return_mask_only=True)
print(int(mask.sum()), "of", mask.size, "points flagged")

# NaN-fill in place. ARM b1 files use Bad/Indeterminate, VAPs often use
# Incorrect/Suspect - pass every name you might meet.
ds.qcfilter.datafilter(variables=["first_cbh", "vertical_visibility", "second_cbh"],
                       rm_assessments=["Bad", "Indeterminate", "Incorrect", "Suspect"],
                       del_qc_var=False)
```

Measured on the example file (sgpceil10mC1.b1.20260918.000012.nc), the tests that fired:

| variable | test | flagged | percent |
|---|---|---|---|
| `vertical_visibility` | Value is equal to missing_value. | 5400 | 100.0 |
| `alt_highest_signal` | Value is equal to missing_value. | 5400 | 100.0 |
| `third_cbh` | Value is equal to missing_value. | 5400 | 100.0 |
| `second_cbh` | Value is equal to missing_value. | 5397 | 99.9444 |
| `first_cbh` | Value is equal to missing_value. | 5306 | 98.2593 |


A single day is not a quality assessment of the instrument - it shows which tests
are live in this datastream and what a filter would do to the record.

Either way, check the DQRs before trusting a period - they carry the mentor's knowledge
of icing, misalignment and outages that no automated test catches:

```python
act.qc.print_dqr("sgpceil10mC1.b1", "19961011", "20260923")
```

The handbook's own note on data quality: Most fields have a corresponding sample-by-sample automated QC field named qc_less than fieldnamegreater than  in the b1 datastream (Table 5, values 0-15 indicating combinations of missing/min/max/delta failures). Minimum/maximum/delta thresholds are defined per field in Table 6 (e.g., first_cbh: 0-7700 m; laser_pulse_energy: 10-110%, delta 100; laser_temperature: -10 to 60°C, delta 5; tilt_angle: 0-4°, delta 1). A qc_time field also flags duplicate, missing, or time-shifted samples relative to a 14-16 s window. Data quality is monitored via DQ Explorer and NCVweb; weekly mentor review...

## Known artifacts and failure modes

From the handbook. This is the section to read before concluding that a feature in
the data is atmospheric.

| issue | how it shows up | what the handbook says to do | source |
|---|---|---|---|
| Window contamination / cleaning alarm | status_flag briefly set to 'Alarm' during daily preventative maintenance due to water/alcohol used to clean the window | Expected during scheduled maintenance; monitor warning flags for window contamination as part of routine review | (hb p. 10) |
| Tilt-angle diurnal oscillation artifact | Measured tilt angle shows a diurnal oscillation from 0 to 3 degrees, attributed to solar heating of the ceilometer rather than actual physical tilt change | Cloud base height is normally automatically compensated for tilt angle, but this option was disabled in 2013 (BCR-1916) to allow derivation of... | (hb p. 10) |
| Tilt-angle correction disabled for CL31 | Cloud heights are not corrected for tilt angle; comparisons with CT25K (which is tilt-corrected) may show discrepancies | None beyond disabling correction intentionally per BCR-1647 and BCR-1916; user should be aware heights are uncorrected | (hb p. 11) |
| Solar radiation-induced alarms | Direct solar radiation exposure may cause alarms and temporarily invalidate the data, though optics are not physically damaged | Optical filters provide solar protection so no additional protection of window needed; data during alarm periods should be treated as temporarily... | (hb p. 10) |
| CEIL vs MPL cloud detection threshold difference | CEIL uses a vertical visibility threshold of 100 m and will not classify thin cloud regions the MPL identifies; CEIL usually reports slightly higher cloud bottom height; MPL often reports... | Use both instruments together; MPL provides most sensitivity to thin clouds while CEIL provides higher resolution for lower-level clouds | (hb p. 10) |
| Daytime/nighttime sensitivity change | There is a change in daytime/nighttime sensitivity in the data when comparing MPL and CEIL | None stated beyond awareness during QME comparisons | (hb p. 12) |
| Range/vertical limit of 7700 m | Clouds above ~7.7 km cannot be detected; data quality checks flag values outside 0-7700 m range for cbh and vertical_visibility fields | Internal consistency checks examine whether clouds are observed at heights up to the system limit (7.7 km) | (hb p. 11) |
| Instrument sensitivity drift over time | Instrument-derived cloud-ceiling height product may drift with time if relative sensitivity of the instrument degrades considerably; in worst case, not observed until differences with MPL... | Annual calibration check of laser transmitter to ensure 10 m range resolution (Section 7.3) | (hb p. 6) |
| Fog/precipitation attenuation of cloud signal | Fog and precipitation attenuate the light pulse, causing the cloud base signal to appear lower in magnitude in the return echo; virtually any backscatter height profile is possible up to... | Fog/precipitation information provides data for estimating attenuation and computing compensation (extinction normalization), up to a limit | (hb p. 16) |
| Ambient light noise exceeding backscatter signal | Weak backscattered signal may be masked by ambient light noise in raw returns | Large number of laser pulses summed; signal-to-noise ratio improves as square root of number of samples (Gaussian noise cancellation), though gain... | (hb p. 16) |
| Height-normalization noise accentuation | After height normalization (multiplying by height squared to remove range dependence), noise (which is height-independent) becomes correspondingly accentuated with increasing height,... | None stated beyond awareness of the effect | (hb p. 16) |
| Lidar ratio (k) variability | Assumed constant k (Lidar Ratio) of 0.03 srad-1 for backscatter-to-extinction conversion varies with humidity (0.02 in high humidity to 0.05 in low humidity) and has a wider range in... | Accurate estimates require k to remain constant with height; assumptions considered accurate enough for cloud detection purposes | (hb p. 16) |
| Vertical visibility contrast threshold difference from horizontal MOR standard | 5% contrast threshold used for horizontal visibility (WMO MOR definition) is unsuitable for vertical measurement; ceilometer uses a different contrast threshold value tuned to match... | Ceilometer uses empirically-derived contrast threshold value found through testing to match human observer vertical visibility values | (hb p. 17) |
| Data quality flag failure codes | qc_less than fieldnamegreater than  values 1,2,3,4,5,7,8,9,10,11,12,14,15 indicate missing data, out-of-range (min/max), or delta-check failures for a given sample | Refer to Table 5/6 thresholds; min/max/delta thresholds defined per field (e.g., first_cbh 0-7700 m) | (hb p. 8) |
| Time quality issues (duplicate/missing samples) | qc_time field flags Dt=0 (duplicate sample), Dt less than lower limit (14 s), or Dt greater than upper limit (16 s) | qc_time field supplied to help detect duplicate samples, missing samples, or other sample time problems | (hb p. 9) |
| CT25K vs CL31 tilt-angle correction inconsistency (historical) | Older CT25K data have tilt-angle-corrected cloud heights while newer CL31 data (post-2010) do not, so a discontinuity in tilt-correction methodology exists across the site record | Documented via BCR-1647 and BCR-1916; users should be aware which model/period applies | (hb p. 11) |


## Calibration and maintenance

|  |  |
|---|---|
| Calibration method | Calibration verified by tilting the ceilometer at a hard target (solid object) of known distance (at least 300 m from ceilometer), with measurement unit removed from shield, placed horizontally, and tilt angle correction turned off; comparison with MPL heights during low cloud situations can also be informative.... (hb p. 17) |
| Calibration interval | Checked every year (annually) to ensure a range resolution of 10 m (hb p. 17) |
| Traceability | See Vaisala 'CL31 verification of proper operation' procedures (hb p. 17) |
| Routine maintenance | Daily preventative maintenance includes cleaning of the window using water and/or alcohol, during which status_flag is briefly set to 'Alarm' (hb p. 10) |
| Maintenance interval | Daily (window cleaning) (hb p. 10) |


Calibration history matters for trend work: a step at a calibration date is an
instrument event, not a climate signal.

## Related

| skill | why |
|---|---|
| `arm-instruments` | the index of these per-instrument skills and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, skew-T, wind rose, size distributions |

Instruments the handbook names as complements or predecessors: Micro Pulse Lidar (MPL), Belfort 7013C Laser Ceilometer, Vaisala CT25K Ceilometer.

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
| `NSA` | North Slope of Alaska, an ARM site |
| `QME` | Quality Measurement Experiment |
| `SGP` | Southern Great Plains, an ARM megasite |
| `VAP` | Value-Added Product |


### References the handbook cites

- Bowen, R., R Calhoun, and J Rasanen. 2002. 'Ceilometer boundary layer measurements during the DOE/VTMX/URBAN Field Experiment in Salt Lake City.' In Fourth Symposium on Urban Environment, American Meteorological Society.
- Emeis, S, C Munkel, S Vogt, WJ Muller, and K Schafer. 2004. 'Atmospheric boundary-layer structure from simultaneous SODAR, RASS, and ceilometer measurements.' Atmospheric Environment 38(2): 273-286,...
- Emeis, S, K Schäfer, and C Münkel. 2009. 'Observation of the structure of the urban boundary layer with different ceilometers and validation by RASS data.' Meteorologische Zeitschrift 18(2): 149-154,...
- Münkel, C. 2007. 'Mixing height determination with lidar ceilometers – results from Helsinki Testbed.' Meteorologische Zeitschrift 16(4): 451-459, doi:10.1127/0941-2948/2007/0221.
- Münkel, C, N Eresmaa, J Rasanen, and A Karppinen. 2007. 'Retrieval of mixing height and dust concentration with lidar ceilometer.' Boundary-Layer Meteorology: doi:10.1007/s10546-006-9103-3.
- Van Tricht, K, IV Gorodetskaya, S Lhermitte, DD Turner, JH Schween, and NPM van Lipzig. 2014. 'An improved algorithm for polar cloud-base detection by ceilometer over the ice sheets.' Atmospheric Measurement Techniques...

## Verified against

- Handbook: https://www.arm.gov/publications/tech_reports/handbooks/ceil_handbook.pdf (26 pages, DOE/SC-ARM-TR-020, by VR Morris)
- Catalog record: ARM data-source index, `instrument_class_code=ceil`, read 2026-09-23
- Example file: `sgpceil10mC1.b1.20260918.000012.nc` from `sgpceil10mC1.b1`, 17.48 MB,
  opened with ACT 2.3.4 on 2026-09-23
- Handbook facts in this file were extracted from the PDF text and page-cited; the data
  facts were measured from the example file. Numbers in the two groups are independent,
  and where they disagree the file is the current truth and the handbook the design intent.
