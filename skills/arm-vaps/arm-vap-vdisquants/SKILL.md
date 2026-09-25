---
name: arm-vap-vdisquants
description: ARM Video Disdrometer VAP (vdisquants) - value-added product reference from its technical report. The retrieval algorithm, reported quantities (Reflectivity factor, Differential reflectivity, Specific differential phase, Specific attenuation, Specific differential attenuation, Mean Doppler velocity), retrieval settings, input dependencies, embedded QC coverage, and the documented failure modes and conditions where the retrieval is invalid or biased. Includes a verified ARM Live example (sgpvdisquantsC1.c1) and the variable inventory of a real file. Use when working with vdisquants data, deciding whether this product or its input instrument answers a question, interpreting its variables, or judging whether a feature is a retrieval artifact. Category - Surface Meteorology. Triggers - vdisquants, Video Disdrometer VAP, sgpvdisquantsC1.c1, Reflectivity factor, Differential reflectivity, Specific differential phase, Specific attenuation, Specific differential attenuation.
---

# VDISQUANTS - Video Disdrometer VAP

VDISQUANTS is an ARM value-added product that ingests raw two-dimensional video disdrometer (vdis) drop size spectra and produces quality-controlled drop size distributions, DSD fit parameters, rain rates, and radar-equivalent polarimetric quantities on a daily basis for a fixed ground-based deployment site.

A **value-added product**: ARM computes it from instrument data rather than measuring it.
Facts below are marked with their source - the technical report (`tr p. N`, 12 pages),
ARM's catalog, or the example file under **The data**, which was opened rather than assumed.
Compiled 2026-09-24.

|  |  |
|---|---|
| ARM class code | `vdisquants` |
| Product type | value-added product (VAP) |
| Technical report | [DOE/SC-ARM-TR-221 / J Hardin, SE Giangrande, A Zhou / April 2020](https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf) |
| Category | Surface Meteorology |
| Input instruments | not declared in ARM's catalog - see Inputs below |
| Record | 2011-02-28 to 2026-09-22 (active) |
| Datastreams with data | 12 across 10 sites |
| ARM page | https://www.arm.gov/capabilities/science-data-products/vaps/vdisquants |


## Credit

Everything this skill knows about the retrieval is the work of **J Hardin, SE Giangrande, A Zhou** -
the ARM developers and mentors who wrote the technical report it derives from:

> J Hardin, SE Giangrande, A Zhou. *Laser Disdrometer Quantities (LDQUANTS) and Video Disdrometer Quantities (VDISQUANTS) Value-Added Products Report*, DOE/SC-ARM-TR-221, April 2020.
> U.S. Department of Energy, Atmospheric Radiation Measurement user facility.
> https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf

Cite the technical report, not this skill, for any fact marked `tr p. N`. This file is
a navigational layer over their document plus a measurement of one data file; it
replaces neither, and where it is thinner than the report the report is right.

> **Scope of this report.** DOE/SC-ARM-TR-221 is a shared report covering the laser-disdrometer and video-disdrometer quantities products, so it is shared with `ldquants`.

> **Extraction coverage.** the report is 12 pages and states few caveats, so the failure-mode list is thin because the source is thin, not because the product has fewer. Counts drawn from this skill's lists are
> lower bounds on what the report contains, not a complete inventory of it.

## How it is produced

The VAP takes the raw drop size distribution spectrum, precipitation intensity, diameter dimension, and calculated fall velocity from the ld.b1 disdrometer datastream and applies quality control filtering based on Tokay et al. (2013, 2014) methods that restrict observations to drops falling within 50% of terminal fall speed for their size, using a Lhermitte (2002) fall speed approximation, to remove spurious measurements from bouncing raindrops, insects, or other contamination. The filtered spectrum is aggregated over the native 1-minute sampling resolution to produce a time series of DSDs and reduce outlier noise. DSD parametric fits (gamma, normalized gamma, and exponential distributions) are then estimated using method of moments and other community algorithms, yielding parameters directly comparable to model outputs. Finally, radar-equivalent quantities (reflectivity Z, differential reflectivity ZDR, specific differential phase KDP, specific attenuation, specific differential attenuation, mean Doppler velocity) are computed via T-Matrix scattering (Mishchenko et al. 1996) using the open-source PyDSD library, with wavelength, temperature, and drop shape assumptions (Thurai et al. 2007), across S-, C-, X-, Ka-, and W-band frequencies at 20C.

**Cadence.** input rate 1-minute native sampling resolution; output every daily NetCDF output file; averaging 1-minute temporal aggregation of filtered drop spectrum; total number of drops over that window is reported and can be used for additional filtering (hb p. 7).

## Inputs

The report names these instruments and sibling products: LDQUANTS, NEXRAD, WACR.

A VAP inherits every limitation of its inputs. When a retrieved value looks wrong, check
the input instrument's own skill (`arm-instrument-<code>`) and its DQRs before concluding
the algorithm is at fault; the reverse is rarer.

## Reported quantities

As specified by the report. These are the physical quantities, not the netCDF variable
names - those are in the next section, taken from a real file.

| quantity | units | range | uncertainty | source |
|---|---|---|---|---|
| Reflectivity factor (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 7) |
| Differential reflectivity (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 7) |
| Specific differential phase (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 7) |
| Specific attenuation (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 7) |
| Specific differential attenuation (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 7) |
| Mean Doppler velocity (S/C/X/Ka/W-band, 20C) | - | - | - | (hb p. 8) |
| Instantaneous rainfall rate of water flux (rain_rate) | - | - | - | (hb p. 8) |
| GammaPSD slope (gammapsd_slope) | - | - | - | (hb p. 8) |
| Shape parameter of modeled drop size distribution... | - | - | - | (hb p. 8) |
| Intercept parameter of modeled drop size distribution... | - | - | - | (hb p. 8) |
| Normalized intercept parameter of a normalized Gaussian... | - | - | - | (hb p. 8) |
| Median drop diameter (med_diameter) | - | - | - | (hb p. 8) |
| Mean drop diameter (mass_weighted_mean_diameter) | - | - | - | (hb p. 8) |
| Liquid water content (lwc) | - | - | - | (hb p. 8) |
| Total droplet concentration (total_droplet_concentration) | - | - | - | (hb p. 8) |


## The data

Verified example: **`sgpvdisquantsC1.c1`**, file `sgpvdisquantsC1.c1.20260921.000000.nc`
(0.45 MB), pulled from ARM Live and opened with ACT on 2026-09-24.

|  |  |
|---|---|
| Dimensions | `time`=1440 |
| Data variables | 42 |
| QC variables | 0 (`qc_` companions) |
| Median time step | 60 s |
| File time span | 2026-09-21T00:00:00 to 2026-09-21T23:59:00 |
| dod version | vdisquants-c1-1.2 |
| process version | vdisquants-2.0.1 |


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
                     params={"user": f"{user}:{token}", "ds": "sgpvdisquantsC1.c1",
                             "start": "2026-09-21", "end": "2026-09-21", "wt": "json"}).json()
print(avail["num_found"], avail["total_size"])            # files, bytes

# Downloads into ./sgpvdisquantsC1.c1/ unless you pass output=
files = act.discovery.download_arm_data(user, token, "sgpvdisquantsC1.c1", "2026-09-21", "2026-09-21")
assert files, "nothing transferred - ARM Live rate limits with HTTP 429; retry"
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)
print(act.discovery.get_arm_doi("sgpvdisquantsC1.c1", "2026-09-21", "2026-09-21"))   # cite what you pulled
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
files = act.discovery.download_arm_data(user, token, "sgpvdisquantsC1.c1", start, end)
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
    act.qc.print_dqr("sgpvdisquantsC1.c1", "20110228", "20260924")
except ValueError:
    print("no DQRs for this window")   # ACT raises rather than returning empty
```

The report's own note on quality: Quality control processing is based on Tokay et al. (2013, 2014) techniques that restrict DSD observations to drops falling within 50% of terminal fall speed for that drop size, using a Lhermitte (2002) fall speed approximation, removing spurious measurements caused by bouncing raindrops, insects, or other contamination. The 1-minute aggregation window reduces outlier effects and data noisiness; the total number of drops over that window is reported and can be used for additional filtering.

## Documented failure modes

From the technical report. For a derived product these are mostly conditions where the
retrieval is invalid, biased, or silently falls back - read this before concluding that
a feature in the output is atmospheric.

| issue | how it shows up | what the report says to do | source |
|---|---|---|---|
| Spurious drop measurements from bouncing raindrops, insects, or other contamination... | Anomalous drops in the raw spectrum with fall speeds inconsistent with terminal velocity for their diameter | Quality control filtering restricts observations to drops falling within 50% of terminal fall speed for that drop size, using a Lhermitte (2002) fall... | (hb p. 6) |
| Outlier noise in drop spectrum at native temporal resolution | Noisy, high-variance DSD estimates in raw per-sample data | 1-minute temporal aggregation window reduces the effects of outliers and reduces noisiness of the data; total number of drops over that window is... | (hb p. 7) |


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
- Lhermitte, RM. 2002. Centimeter and millimeter wavelength radars in meteorology. Lhermitte Publications.
- Testud, J, S Oury, RA Black, P Amayenc, and X Dou. 2001. Journal of Applied Meteorology and Climatology 40(6): 1118-1140.
- Giangrande, SE, MJ Bartholomew, M Pope, S Collis, and MP Jensen. 2014. Journal of Applied Meteorology and Climatology 53(5): 1213-1231.
- Thompson, JE, SA Rutledge, B Dolan, and M Thurai. 2015. Journal of the Atmospheric Sciences 72(11): 4091-4125.
- Thurai, M, GJ Huang, VN Bringi, WL Randeu, and M Schonhuber. 2007. Journal of Atmospheric and Oceanic Technology 24(6): 1019-1032.
- Mishchenko, MI, LD Travis, and DW Mackowski. 1996. Journal of Quantitative Spectroscopy and Radiative Transfer 55(5):535-575.
- Hardin, JC. 2014. PyDisdrometer v1.0, http://doi.org/10.5281/zenodo.9991

## Verified against

- Technical report: https://www.arm.gov/publications/tech_reports/doe-sc-arm-tr-221.pdf (12 pages, DOE/SC-ARM-TR-221, by J Hardin, SE Giangrande, A Zhou)
- Catalog record: ARM data-source index, `instrument_class_code=vdisquants`, read 2026-09-24
- Example file: `sgpvdisquantsC1.c1.20260921.000000.nc` from `sgpvdisquantsC1.c1`, 0.45 MB,
  opened with ACT 2.3.4 on 2026-09-24
- Extraction coverage: the report is 12 pages and states few caveats, so the failure-mode list is thin because the source is thin, not because the product has fewer
- Report facts were extracted from the PDF text and page-cited; data facts were measured
  from the example file. Where the two disagree the file is the current truth and the
  report the design intent - a VAP's output changes with its version.
