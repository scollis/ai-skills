---
name: arm-vap-shallowcumulus
description: ARM Fair-Weather Shallow Cumulus Identification (shallowcumulus) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (flag_shcu, flag_st_shcu, flag_shcu_st, flag_ci_shcu, flag_shcu_ci, flag_ac_shcu), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpshcusummaryC1.c1) and the variable inventory of a real file. Use when working with shallowcumulus data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Cloud Properties. Triggers - shallowcumulus, Fair-Weather Shallow Cumulus Identification, sgpshcusummaryC1.c1, flag_shcu, flag_st_shcu, flag_shcu_st, flag_ci_shcu, flag_shcu_ci, Cloud Properties.
---

# SHALLOWCUMULUS - Fair-Weather Shallow Cumulus Identification

The Shallow Cumulus VAP automatically identifies periods of fair-weather shallow cumulus (and related transitional cloud-type periods) at the ARM SGP Central Facility on an hourly basis by combining cloud-type classifications from the CLDTYPE VAP (derived from ARSCL cloud boundaries), total sky imager (TSI) cloud fraction, and ceilometer cloud fraction.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 35 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `shallowcumulus` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-214 / D Flynn, Y Shi, K-S Lim, L Riihimaki / May 2018](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-214.pdf) |
| Category | Cloud Properties |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2000-07-01 to 2025-08-21 (retired) |
| Datastreams with data | 3 across 1 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/shallowcumulus |


## Credit

Everything this skill knows about the retrieval is the work of **D Flynn, Y Shi, K-S Lim, L Riihimaki** -
the ARM developers and mentors who wrote the technical report it derives from:

> D Flynn, Y Shi, K-S Lim, L Riihimaki. *Shallow Cumulus (SHALLOWCUMULUS) Value-Added Product Report*, DOE/SC-ARM-TR-214, May 2018.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-214.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

## How it is produced

The algorithm first uses the Cloud Type (CLDTYPE) VAP, which classifies cloud layers (derived from ARSCL cloud radar/lidar boundaries) into one of seven types based on top height, base height and layer thickness, to identify time periods of low-cloud-only or low-cloud-with-overlying-cirrus conditions, allowing at most two 1-minute detections of another cloud type within the period. A potential event requires low clouds to persist longer than 1.5 hours with at least two 1-minute detections of low cloud. Concurrent TSI and ceilometer cloud fraction measurements then filter potential events: TSI cloud fraction must be greater than 0.5% and less than 80%, and ceilometer cloud fraction must be greater than zero, distinguishing shallow cumulus from broken stratus decks or stratocumulus. Events separated by less than 2.5 hours are merged if the intervening period contains only cirrus or at most two other cloud-type detections. Finally, the five hours before and after an identified event are examined; if more than two hours of another cloud type occurs in that window, the event is flagged transitional (to or from stratus, cirrus, or altocumulus/altostratus), with the caveat that these transitional classifications are preliminary.

**Cadence.** input rate 1-minute cloud-type detections used as input; output every 1-hour time blocks (daily files); daily summary rolled into monthly files; averaging Hourly average cloud fractions for TSI and ceilometer; cloud-type tests applied per 1-hour block (hb p. 7).

## Inputs

The report names these instruments and sibling products: Cloud Type (CLDTYPE) VAP, Active Remotely Sensed Cloud Locations (ARSCL) VAP, Total Sky Imager (TSI), Ceilometer, Ka-Band ARM Zenith Radar (KAZR), Micropulse Lidar (MPL), Atmospheric Emitted Radiance Interferometer (AERI).

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| flag_shcu | unitless | 0,1,2 | - | (hb p. 8) |
| flag_st_shcu | unitless | 0,1 | - | (hb p. 9) |
| flag_shcu_st | unitless | 0,1 | - | (hb p. 9) |
| flag_ci_shcu | unitless | 0,1 | - | (hb p. 9) |
| flag_shcu_ci | unitless | 0,1 | - | (hb p. 10) |
| flag_ac_shcu | unitless | 0,1 | - | (hb p. 10) |
| flag_shcu_ac | unitless | 0,1 | - | (hb p. 10) |
| shcu_test_criteria | unitless (bit-packed) | bit_mask 1,2,4,8,16,32,64,128,256 | - | (hb p. 11) |
| cloud_fraction_tsi | % | - | - | (hb p. 11) |
| cloud_fraction_ceil | % | - | - | (hb p. 11) |
| major_cloud_type | unitless | 1-7 | - | (hb p. 12) |
| max_cloud_type | unitless | 1-7 | - | (hb p. 12) |
| shallowcumulus_event | unitless (bit-packed) | flag_masks 1,2,4,8,16,32,64 | - | (hb p. 14) |
| shallowcumulus_event_tests | unitless (bit-packed) | flag_masks 1,2,4,8 | - | (hb p. 14) |
| start_hour | unitless | - | - | (hb p. 15) |
| end_hour | unitless | - | - | (hb p. 15) |


## Retrieval settings

| parameter | value | source |
|---|---|---|
| Minimum low-cloud duration for potential event | greater than  1.5 hour | (hb p. 7) |
| Minimum low-cloud detections in period | at least two detections at 1-minute resolution | (hb p. 7) |
| Max allowed detections of other cloud types in... | at most two detections (at 1-minute time resolution) | (hb p. 1) |
| TSI cloud fraction lower bound (tsi_cldfra1) | greater than  0.5% | (hb p. 7) |
| TSI cloud fraction upper bound (tsi_cldfra2) | less than  80% | (hb p. 7) |
| Ceilometer cloud fraction requirement (c_cldfra1) | greater than  zero | (hb p. 7) |
| Event merge time gap | less than 2.5 hours (with only cirrus or at most two other cloud-type detections in between) | (hb p. 7) |
| Transitional status window | 5 hours prior to and subsequent to event | (hb p. 7) |
| Transitional classification threshold | more than two hours of another cloud type within the 5-hour window | (hb p. 7) |
| Cloud type classification scale... | 1=Low clouds, 2=Congestus, 3=Deep Convection, 4=Altocumulus, 5=Altostratus, 6=Cirrostratus/Anvil, 7=Cirrus | (hb p. 8) |
| Temporal resolution | hourly (1-hour time blocks) | (hb p. 1) |
| Maximum detected events per day | up to four detected events per day; more than one or two unusual | (hb p. 8) |
| TSI cloud fraction sensitivity test range explored | varying TSI cloud-fraction criteria between 70% and 80% | (hb p. 18) |
| Alternate time block tested | 30-minute time blocks vs. 60-minute blocks | (hb p. 18) |
| Operational deployment season | May through September (summer season) | (hb p. 16) |
| Operational site/facility | SGP Central Facility (C1) | (hb p. 16) |


## The data

Verified example: **`sgpshcusummaryC1.c1`**, file `sgpshcusummaryC1.c1.20250801.000000.nc`
(0.01 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=21, `bound`=2, `event`=4 |
| Data variables | 10 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 86400 s |
| File time span | 2025-08-01T00:00:00 to 2025-08-21T00:00:00 |
| dod version | shcusummary-c1-1.1 |
| process version | shallowcumulus-1.6.2 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `end_hour` | hour | time,event | - | Ending hour when event is detected |
| `shallowcumulus_event` | unitless | time,event | - | Shallow cumulus event detected |
| `shallowcumulus_event_tests` | unitless | time,event | - | Shallow cumulus event tests |
| `start_hour` | hour | time,event | - | Starting hour when event is detected |
| `time` | - | time | - | Time offset from midnight |


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
                     params={"user": f"{user}:{token}", "ds": "sgpshcusummaryC1.c1",
                             "start": "2025-08-01", "end": "2025-08-01", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpshcusummaryC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpshcusummaryC1.c1", "2025-08-01", "2025-08-01")
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpshcusummaryC1.c1", "2025-08-01", "2025-08-01"))   # cite what you pulled
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
act.qc.print_dqr("sgpshcusummaryC1.c1", "20000701", "20260924")
```

The report's own note on quality: If no event is identified within a given hour, the shcu_test_criteria field (bit-packed, 9 flags) records which test/criteria failed or whether required input data was unavailable, at the daily file level. At the monthly level, shallowcumulus_events_test provides bit-packed flags for why a potential event was or was not detected (event detected with overlying cirrus, no low clouds found, short duration of low clouds, no input found). Quicklook plots color-code up to four potential daily events and flag them 0 (low clouds only), 1 (low clouds with cirrus), 3 (duration requirement not met), 4...

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| TSI not available during current hour | shcu_test_criteria bit_1 set; hour flagged as test failure rather than event detection | Flagged via bit-packed shcu_test_criteria field; no shallow cumulus determination possible for that hour | (hb p. 6) |
| Ceilometer not available during current hour | shcu_test_criteria bit_2 set | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| CLDTYPE VAP does not detect any cloud | shcu_test_criteria bit_3 set; no event flagged | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| Frequency of low clouds below threshold in the hour | shcu_test_criteria bit_4 set (frequency of low clouds less than = num_low) | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| TSI cloud fraction too low | shcu_test_criteria bit_5 set (cloud_fraction_tsi less than = tsi_cldfra1) | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| Ceilometer cloud fraction too low | shcu_test_criteria bit_6 set (cloud_fraction_ceil less than = c_cldfra1) | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| TSI cloud fraction too high (broken stratus/stratocumulus contamination) | shcu_test_criteria bit_7 set (cloud_fraction_tsi greater than = tsi_cldfra2), distinguishing shallow cumulus from broken stratus deck or stratocumulus with lifting | Events with TSI cloud fraction greater than = tsi_cldfra2 (80%) excluded | (hb p. 7) |
| Ambiguous/mid-range max cloud type | shcu_test_criteria bit_8 set (1 less than  max_cloud_type less than  7 during hour) | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| Missing input data for cloud type | shcu_test_criteria bit_9 set (cloudtype data not available due to missing input) | Flagged via bit-packed shcu_test_criteria field | (hb p. 6) |
| Radar/lidar noise producing false cloud layer detections | Small numbers (up to two) of spurious other-cloud-type detections within an otherwise low-cloud-only period | CLDTYPE VAP criteria allow at most two detections of other cloud types at 1-minute resolution before excluding the period | (hb p. 1) |
| Transitional classification unreliability / window sensitivity | Transitional type assignment (to/from stratus, cirrus, altocumulus/altostratus) changes depending on the length of the pre/post window used (1 vs 2 vs 3-4 hours); 17 of 32 test events... | Handbook states transitional classifications are preliminary and may not be a reliable indicator of meteorology; recommends using both shallow... | (hb p. 7) |
| Limited transitional cloud types supported | Only stratus, cirrus, and altocumulus/altostratus transitions are identified/labeled; other transition types are not classified | - | (hb p. 7) |
| MPL (micropulse lidar) signal-to-noise limitations missing cirrus/cloud detection | Cirrus layer not consistently detected due to MPL SNR; cases excluded by VAP unless cirrus layer allowed; MPL cloud mask missing some clouds; MPL misses clouds due to instrument... | - | (hb p. 22) |
| False radar cloud tops / insect clutter contamination | Radar shows false cloud tops or insect clutter layers (noted repeatedly in 2016/2017 case notes), causing possible misclassification or spurious cloud-type detections, especially above... | - | (hb p. 26) |
| Missing TSI data periods | TSI missing entirely for some hours/days (2017 cases: 20170504, 20170509, 20170516, 20170517), leaving VAP criteria undetermined | Flagged as event/test failure due to missing input (flag value 4 in quicklook, or shcu_test_criteria bit_1/shallowcumulus_events_test bit_4) | (hb p. 32) |
| Short-duration low cloud periods not meeting 1.5-hour criterion | Periods of low clouds identified but flagged 3 in quicklook (duration requirement not met); e.g., August 25, 2015 high-priority LASSO case missed by VAP due to short duration | Final algorithm version still misses such cases (e.g., noted August 26, 2015 miss); documented as a known limitation | (hb p. 18) |
| False positives from algorithm tuning | Final algorithm version includes cases that are likely false positives, in exchange for capturing more LASSO high-priority cases | Accepted trade-off noted by developers; no further mitigation given | (hb p. 18) |
| Aerosol misidentified as cloud | Case notes indicate possible misidentification of aerosol structure as cloud (e.g., significant aerosol structure noted on several 2015 dates; 20170716 case) | - | (hb p. 22) |
| Radar and lidar disagreement on cloud presence/height | Case note: 'radar and lidar disagree' for 20170706 event; 'radar doesn't see boundary layer clouds' for 20170524 | - | (hb p. 32) |
| KAZR (Ka-Band ARM Zenith Radar) outages | Notes such as 'KAZR out after 17 UTC' (20160614) and 'KAZR out for part of day' (20160712) leading to gaps in cloud-type input | - | (hb p. 27) |
| Missing MPL data periods | Case note 'Missing MPL data' for 20160720; 'MPL out for part of the period' (20160825) | - | (hb p. 30) |
| Precipitation/rain contamination of cloud fraction and classification | Case notes of rain on and off all day, mostly overcast (20160523), or precip noted alongside cloud events (20170716), complicating classification | - | (hb p. 25) |
| Complex or transitional synoptic situations misclassified as simple shallow cumulus | LASSO team notes describing cases with residual layer plus boundary-layer cloud, post-frontal conditions, MCS influence, or squall-line proximity that complicate attribution to... | Such cases flagged in LASSO decision notes as 'No' or 'complicated' for use in LES forcing; recommend caution in using purely VAP-flagged events for... | (hb p. 25) |
| Non-cirrus cloud intrusions splitting single events into two | Example: 'Non-cirrus clouds at 16UTC split event into two' (20160626) | - | (hb p. 28) |


_1 further items in the report._

## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Berg, LK, and EI Kassianov. 2008. "Temporal variability of fair-weather cumulus statistics at the ACRF SGP site." Journal of Climate 21: 3344-3358, doi:10.1175/2007JCLI2266.1.
- Yunyan, Z, and SA Klein. 2013. "Factors controlling the vertical extent of fair-weather shallow cumulus clouds over land: Investigation of diurnal-cycle observations collected at the ARM Southern Great Plains site."...
- Flynn, D, Y Shi, K Lim, and L Riihimaki. 2017. Cloud Type Classification (cldtype) Value-Added Product. ARM Research Facility. U.S. Department of Energy. DOE/SC-ARM-TR-200.
- Kyo-Sun Lim et al. "Long-term cloud type retrieval using a combination of active remote sensors and a total sky imager at the ARM SGP site," in progress.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-214.pdf (35 pages, DOE/SC-ARM-TR-214, by D Flynn, Y Shi, K-S Lim, L Riihimaki)
- Catalog record: ARM data-source index, `instrument_class_code=shallowcumulus`, read 2026-09-24
- Example file: `sgpshcusummaryC1.c1.20250801.000000.nc` from `sgpshcusummaryC1.c1`, 0.01 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
