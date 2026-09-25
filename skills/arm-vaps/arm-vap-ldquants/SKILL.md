---
name: arm-vap-ldquants
description: ARM Laser Disdrometer Quantities (ldquants) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (differential_reflectivity, specific_differential_phase, specific_attenuation, specific_differential_attenuation, mean_doppler_vel), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpldquantsC1.c1) and the variable inventory of a real file. Use when working with ldquants data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface Meteorology. Triggers - ldquants, Laser Disdrometer Quantities, sgpldquantsC1.c1, differential_reflectivity, specific_differential_phase, specific_attenuation, specific_differential_attenuation, Surface Meteorology.
---

# LDQUANTS - Laser Disdrometer Quantities

LDQUANTS is an ARM value-added product that ingests laser (or video) disdrometer raw drop size distribution data (ld.b1), quality-filters it, and derives DSD parameters, rainfall quantities, and radar-equivalent polarimetric variables, output as a daily NetCDF file.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 12 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `ldquants` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-221 / J Hardin, SE Giangrande, A Zhou / April 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf) |
| Category | Surface Meteorology |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2014-02-27 to 2026-09-23 (active) |
| Datastreams with data | 24 across 11 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/ldquants |


## Credit

Everything this skill knows about the retrieval is the work of **J Hardin, SE Giangrande, A Zhou** -
the ARM developers and mentors who wrote the technical report it derives from:

> J Hardin, SE Giangrande, A Zhou. *Laser Disdrometer Quantities (LDQUANTS) and Video Disdrometer Quantities (VDISQUANTS) Value-Added Products Report*, DOE/SC-ARM-TR-221, April 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-221 is a shared report covering the laser-disdrometer and video-disdrometer quantities products, so it is shared with `vdisquants`.

> **Extraction coverage.** the report is 12 pages and states few caveats, so the failure-mode list is thin because the source is thin, not because the product has fewer. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

The VAP takes raw drop size distribution (raw_spectrum), precipitation intensity, diameter dimension (class_size_width), and calculated fall velocity from ld.b1 disdrometer files and performs quality control filtering, DSD parameter estimation, and radar scattering calculations. Quality control restricts DSD observations to drops falling within 50% of the terminal fall speed expected for that drop size, using a Lhermitte (2002) fall speed approximation, to remove spurious measurements from bouncing raindrops, insects, or other contamination. The cleaned drop spectrum is aggregated over the native 1-minute sampling resolution to produce a 2D time series of DSDs, from which parametric fits to gamma, normalized gamma, and exponential distributions are estimated using method of moments and other community algorithms. Finally, radar-equivalent quantities (Z, ZDR, KDP, specific attenuation, specific differential attenuation, mean Doppler velocity) are computed via T-Matrix scattering (Mishchenko et al. 1996) with wavelength, temperature, and drop shape assumptions (Thurai et al. 2007), implemented via the open source PyDSD library, for radar frequencies from S-band (NEXRAD, 10-cm) to W-band (WACR, 3-mm).

**Cadence.** input rate 1-minute; output every daily NetCDF file; averaging 1-minute temporal aggregations to reduce effects of outliers in the drop spectrum and reduce noisiness of data; total number of drops over that window is reported and can be used for additional filtering (hb p. 7).

## Inputs

The report names these instruments and sibling products: ld.b1 laser/video disdrometer, NEXRAD, WACR (W-band ARM Cloud Radar), rain gauges, radars.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| reflectivity_factor_sband20c / cband20c / xband20c /... | - | - | - | (hb p. 7) |
| differential_reflectivity (s/c/x/ka/w band, 20C) | - | - | - | (hb p. 7) |
| specific_differential_phase (s/c/x/ka/w band, 20C) | - | - | - | (hb p. 7) |
| specific_attenuation (s/c/x/ka/w band, 20C) | - | - | - | (hb p. 7) |
| specific_differential_attenuation (s/c/x/ka/w band, 20C) | - | - | - | (hb p. 7) |
| mean_doppler_vel (s/c/x/ka/w band, 20C) | - | - | - | (hb p. 8) |
| rain_rate | - | - | - | (hb p. 8) |
| gammapsd_slope | - | - | - | (hb p. 8) |
| gammapsd_shape | - | - | - | (hb p. 8) |
| num_concen | - | - | - | (hb p. 8) |
| nor_num_concen | - | - | - | (hb p. 8) |
| med_diameter | - | - | - | (hb p. 8) |
| mass_weighted_mean_diameter | - | - | - | (hb p. 8) |
| lwc (liquid water content) | - | - | - | (hb p. 8) |
| total_droplet_concentration | - | - | - | (hb p. 8) |


## The data

Verified example: **`sgpldquantsC1.c1`**, file `sgpldquantsC1.c1.20260920.000000.nc`
(0.45 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 42 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-20T00:00:00 to 2026-09-20T23:59:00 |
| dod version | ldquants-c1-1.4 |
| process version | ldquants-2.0.1 |


### Variables in that file

| variable | units | dims | qc | long_name |
|---|---|---|---|---|
| `bringi_conv_stra_flag` | 1 | time | - | Bringi Convective Stratiform Flag |
| `differential_reflectivity_cband20c` | dB | time | - | Estimated Differential Radar Reflectivity (H, V) from Drop Size... |
| `differential_reflectivity_kaband20c` | dB | time | - | Estimated Differential Radar Reflectivity (H, V) from Drop Size... |
| `differential_reflectivity_sband20c` | dB | time | - | Estimated Differential Radar Reflectivity (H, V) from Drop Size... |
| `differential_reflectivity_xband20c` | dB | time | - | Estimated Differential Radar Reflectivity (H, V) from Drop Size... |
| `exppsd_slope` | 1/mm | time | - | Distribution Slope Parameter |
| `gammapsd_shape` | 1 | time | - | Shape Parameter of Modeled Drop Size Distribution |
| `gammapsd_slope` | 1/mm | time | - | GammaPSD Slope |
| `lwc` | g/m^3 | time | - | Liquid Water Content |
| `mass_weighted_mean_diameter` | mm | time | - | Mean Drop Diameter |
| `mean_doppler_vel_cband20c` | m/s | time | - | Mean Doppler Velocity C-band when temperature is 20C |
| `mean_doppler_vel_kaband20c` | m/s | time | - | Mean Doppler Velocity Ka-band when temperature is 20C |
| `mean_doppler_vel_sband20c` | m/s | time | - | Mean Doppler Velocity S-band when temperature is 20C |
| `mean_doppler_vel_wband20c` | m/s | time | - | Mean Doppler Velocity W-band when temperature is 20C |
| `mean_doppler_vel_xband20c` | m/s | time | - | Mean Doppler Velocity X-band when temperature is 20C |
| `med_diameter` | mm | time | - | Median Drop Diameter |
| `norm_num_concen` | 1/(m^3 mm) | time | - | Normalized Intercept Parameter of a Normalized Gaussian Distribution |
| `num_concen` | 1/(m^3 mm) | time | - | Intercept Parameter of Modeled Drop Size Distribution |
| `rain_rate` | mm/hour | time | - | Instantaneous Rainfall Rate of Water Flux |
| `reflectivity_factor_cband20c` | dBZ | time | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `reflectivity_factor_kaband20c` | dBZ | time | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `reflectivity_factor_sband20c` | dBZ | time | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `reflectivity_factor_wband20c` | dBZ | time | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `reflectivity_factor_xband20c` | dBZ | time | - | Estimated Horizontal Radar Reflectivity from Drop Size Distribution... |
| `specific_attenuation_cband20c` | dB/km | time | - | Specific Attenuation C-Band when temperature is 20 degree C |
| `specific_attenuation_kaband20c` | dB/km | time | - | Specific Attenuation Ka-Band when temperature is 20 degree C |
| `specific_attenuation_sband20c` | dB/km | time | - | Specific Attenuation S-Band when temperature is 20 degree C |
| `specific_attenuation_xband20c` | dB/km | time | - | Specific Attenuation X-Band when temperature is 20 degree C |
| `specific_differential_attenuation_cband20c` | dB/km | time | - | Specific Differential Attenuation C-Band when temperature is 20... |
| `specific_differential_attenuation_kaband20c` | dB/km | time | - | Specific Differential Attenuation Ka-Band when temperature is 20... |


_8 more variables; the full inventory is in `example_inventory.json` beside this file._

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
                     params={"user": f"{user}:{token}", "ds": "sgpldquantsC1.c1",
                             "start": "2026-09-20", "end": "2026-09-20", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpldquantsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpldquantsC1.c1", "2026-09-20", "2026-09-20")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpldquantsC1.c1", "2026-09-20", "2026-09-20"))   # cite what you pulled
```
### First look

ARM data is time-first; this is the shape of the record, not a publication figure.

```python
import matplotlib.pyplot as plt

# squeeze drops ARM's size-1 sensor dimensions - the tethered-balloon files carry
# one, which otherwise sends a 1-D series through the 2-D plotting path.
disp = act.plotting.TimeSeriesDisplay(ds.squeeze(), figsize=(11, 4))
disp.plot("rain_rate")
disp.fig.savefig("first_look.png", dpi=120, bbox_inches="tight")
```


This product carries 42 variables. Over any window longer than a day,
read only what you need, and ask for the QC companion at the same time:

```python
files = act.discovery.download_arm_data(user, token, "sgpldquantsC1.c1", start, end)
ds = act.io.arm.read_arm_netcdf(files, keep_variables=['bringi_conv_stra_flag', 'differential_reflectivity_cband20c', 'differential_reflectivity_kaband20c'],
                                cleanup_qc=True)
```

## Quality control in this product

This datastream ships **no `qc_` companion variables**, so `act-qc`'s filter methods have
nothing to act on. Screening has to come from the product's own fields and from DQRs.

Mask, flag or quality fields in the verified file: `bringi_conv_stra_flag`.

Check the DQRs before trusting a period - for a VAP they cover both the product and the
instruments feeding it:

```python
try:
    act.qc.print_dqr("sgpldquantsC1.c1", "20140227", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Quality control processing follows Tokay et al. (2013, 2014) methods, filtering the DSD to drops within 50% of terminal fall speed for their diameter (per a Lhermitte 2002 fall speed approximation) to remove spurious measurements caused by bouncing raindrops, insects, or other contamination sources. After filtering, data are aggregated to 1-minute resolution, and the total number of drops within each aggregation window is reported so users can apply additional filtering.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Spurious drop measurements from bouncing raindrops, insects, or other contamination | Drops appearing with fall speeds inconsistent with terminal velocity expected for their size in the raw drop spectrum | Quality control filtering restricts DSD observations to drops falling within 50% of the terminal fall speed for that drop size, based on a Lhermitte... | (hb p. 6) |
| Outlier noise in short-interval drop spectra | Noisy, highly variable native-resolution DSD estimates | 1-minute temporal aggregation of the drop spectrum; total drop count per window reported for additional filtering | (hb p. 7) |


## Related

| skill | why |
|---|---|
| `arm-vaps` | the index of these VAP skills |
| `arm-instruments` | the instrument skills, including this product's inputs, and the ARM catalog API |
| `act-arm-live` | ARM Live access, datastream naming, server-side subsetting, DOI citation |
| `act-qc` | the `qc_` machinery, DQR ingestion, adding your own tests |
| `act-plotting` | the Display family, QC block plots, time-height sections |

### References the report cites

- Tokay, A, WA Petersen, P Gatlin, and M Wingo. 2013. Journal of Atmospheric and Oceanic Technology 30(8): 1672-1690.
- Tokay, A, RJ Roche, and PG Bashor. 2014. Journal of Hydrometeorology 15(2): 801-812.
- Testud, J, S Oury, RA Black, P Amayenc, and X Dou. 2001. Journal of Applied Meteorology and Climatology 40(6): 1118-1140.
- Giangrande, SE, MJ Bartholomew, M Pope, S Collis, and MP Jensen. 2014. Journal of Applied Meteorology and Climatology 53(5): 1213-1231.
- Thompson, JE, SA Rutledge, B Dolan, and M Thurai. 2015. Journal of the Atmospheric Sciences 72(11): 4091-4125.
- Thurai, M, GJ Huang, VN Bringi, WL Randeu, and M Schonhuber. 2007. Journal of Atmospheric and Oceanic Technology 24(6): 1019-1032.
- Mishchenko, MI, LD Travis, and DW Mackowski. 1996. Journal of Quantitative Spectroscopy and Radiative Transfer 55(5): 535-575.
- Lhermitte, RM. 2002. Centimeter and millimeter wavelength radars in meteorology.
- Hardin, JC. 2014. PyDisdrometer v1.0.

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf (12 pages, DOE/SC-ARM-TR-221, by J Hardin, SE Giangrande, A Zhou)
- Catalog record: ARM data-source index, `instrument_class_code=ldquants`, read 2026-09-24
- Example file: `sgpldquantsC1.c1.20260920.000000.nc` from `sgpldquantsC1.c1`, 0.45 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 12 pages and states few caveats, so the failure-mode list is thin because the source is thin, not because the product has fewer
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
