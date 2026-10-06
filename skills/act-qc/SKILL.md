---
name: act-qc
description: Work with ARM's embedded quality-control flags using ACT (act-atmos) - the bit-packed-to-CF cleanup that everything else depends on, the `ds.qcfilter` accessor (get_masked_data, datafilter, the add_*_test family, set_test/available_bit), Data Quality Report (DQR) ingestion from the ARM web service, QC summary variables, supplemental YAML QC, and the BSRN/radiometer comparison tests. Use this whenever ARM data needs to be screened, whenever a variable has a companion qc_ variable, when the user asks whether data are good/flagged/suspect, when applying limit or outlier tests to a time series, or when DQRs or data quality reports come up. Triggers - ACT QC, qcfilter, qc_ variable, flag_masks, flag_meanings, flag_assessments, cleanup_qc, ds.clean.cleanup, datafilter, get_masked_data, add_greater_test, add_gesd_test, IQR test, persistence test, step change test, DQR, data quality report, add_dqr_to_qc, print_dqr, qc summary, BSRN, bad indeterminate suspect incorrect.
---

# ARM embedded QC with ACT

ARM b1-level files ship a companion `qc_<variable>` for most measurements. Reading it
correctly is the difference between an honest time series and a plot of instrument
failures. This skill covers the whole path: clean -> inspect -> add your own tests ->
fold in DQRs -> apply.

Companions: `act-arm-live` (getting the data), `act-plotting` (`qc_flag_block_plot`,
assessment overplots), `act-retrievals`. Run everything in an env with `act-atmos`
installed (see `act-arm-live`).

## 1. Clean first — nothing works before this

Raw ARM QC variables carry bit-packed integers described by non-standard attributes:

```
bit_1_description: 'Value is equal to missing_value.'   bit_1_assessment: 'Bad'
bit_2_description: 'Value is less than valid_min.'      bit_2_assessment: 'Bad'
...
```

`qcfilter` and the QC block plot both read the CF form (`flag_masks`,
`flag_meanings`, `flag_assessments`), so the attributes have to be converted:

```python
ds = act.io.arm.read_arm_netcdf(files, cleanup_qc=True)   # or ds.clean.cleanup()
```

After cleanup the same variable reads
`flag_masks: [1, 2, 4, 8]`, `flag_assessments: ['Bad','Bad','Bad','Indeterminate']`,
plus the threshold attributes renamed `valid_min`/`valid_max`/`valid_delta` ->
`fail_min`/`fail_max`/`fail_delta`. Skipping cleanup does not raise — the filter
methods simply find nothing to act on, so flagged data pass through untouched.

`ds.clean.cleanup(...)` gives you the knobs `cleanup_qc=True` hides:
`cleanup_arm_qc`, `clean_arm_state_vars`, `handle_missing_value`,
`link_qc_variables`, `normalize_assessment`, `cleanup_cf_qc`.

## 2. Inspect before filtering

```python
act_qc_table(ds, variables=["temp_mean"])   # variable, test, assessment, n_flagged, percent
act_qc_assessments(ds)                      # e.g. ['Bad', 'Indeterminate']
act_qc_variables(ds)                        # data variable -> its qc_ variable
```

`act_qc_table` decodes each bit against the data and tells you what a filter is about
to remove. Reporting "3% of the record was flagged bad, all of it the missing-value
test" is far more useful to a scientist than a silently shortened series.

## 3. Assessments: the trap worth internalising

`get_masked_data` and `datafilter` match assessment strings **literally**. ARM uses
two vocabularies for the same thing:

| Raw automated QC | After DQR normalisation |
|---|---|
| `Bad` | `Incorrect` |
| `Indeterminate` | `Suspect` |

`act.qc.arm.add_dqr_to_qc` defaults to `normalize_assessment=True`, which rewrites the
existing assessments as well as the DQR ones. Measured on `sgp30ecorE14.b1` for
2015-11-26 to 11-30 with DQR D151209.1 applied to `h`:

```
rm_assessments=['Bad']        ->  102 of 240 points masked
rm_assessments=['Incorrect']  ->  199 of 240 points masked
```

A habitual `rm_assessments=['Bad']` therefore leaves 97 known-bad flux values in the
series and reports no error. Either pass the full vocabulary or check first:

```python
act_qc_apply(ds, variables=["h"])     # uses Bad + Incorrect + Indeterminate + Suspect
act_qc_assessments(ds)                # or look, then choose deliberately
```

Pass `normalize_assessment=False` to `add_dqr_to_qc` if you want the DQR flagged as
`Incorrect` while the automated tests stay `Bad`/`Indeterminate`.

## 4. Applying QC

Two shapes, both on the `ds.qcfilter` accessor:

```python
# non-destructive: values with flags become NaN in a returned array
vals = ds.qcfilter.get_masked_data("temp_mean", rm_assessments=["Bad", "Indeterminate"],
                                   return_nan_array=True)

# destructive: rewrite the variable in the dataset
ds.qcfilter.datafilter(variables=["temp_mean"], rm_assessments=["Bad"], del_qc_var=False)
```

`get_masked_data` also does `return_mask_only`, `return_inverse` (keep only the
flagged points — handy for plotting what was removed), and `rm_tests=[1, 3]` to target
specific bit numbers instead of assessments. `datafilter` promotes integer variables
to float so NaN can be stored; keep `del_qc_var=False` unless you are writing a
finished product, since deleting the QC variable throws away the evidence.

## 5. Adding your own tests

Every test writes a new bit into the existing `qc_<var>` variable, with a description
and assessment, so a custom threshold becomes part of the same audit trail:

```python
ds.qcfilter.add_greater_test("temp_mean", 30.0, test_assessment="Indeterminate",
                             test_meaning="temp > 30 C")
```

The family, all `ds.qcfilter.add_*`:

| Group | Tests |
|---|---|
| Limits | `add_less_test`, `add_greater_test`, `add_less_equal_test`, `add_greater_equal_test`, `add_equal_to_test`, `add_not_equal_to_test`, `add_inside_test`, `add_outside_test` |
| Missing / delta | `add_missing_value_test`, `add_delta_test` |
| Outliers | `add_iqr_test` (interquartile), `add_gesd_test` (generalised extreme studentised deviate) |
| Behaviour in time | `add_persistence_test` (stuck sensor), `add_step_change_test`, `add_relative_variability_test` |
| Cross-instrument | `add_difference_test` (against a second dataset), `compare_time_series_trends` |
| Physical | `add_atmospheric_pressure_test` (pressure vs altitude) |

Shared keywords: `test_assessment` (default `'Bad'`, use `'Indeterminate'`/`'Suspect'`
for advisory tests), `test_meaning` (the human-readable string that lands in
`flag_meanings` — always write one), `test_number` to pin a bit, `limit_attr_name` to
read the threshold from a variable attribute instead of a literal, and `use_dask=True`
for large arrays. Low-level control: `available_bit`, `set_test`, `unset_test`,
`remove_test`, `create_qc_variable`, `merge_qc_variables`, `update_ancillary_variable`.

Radiation-specific suites live alongside: `ds.qcfilter.bsrn_limits_test`,
`bsrn_comparison_tests`, `normalized_rradiance_test`, and
`act.qc.fft_shading_test` for MFRSR shading artefacts.

## 6. Data Quality Reports

DQRs are human-written records of known instrument problems — icing, misalignment,
power loss — that automated tests cannot catch. They come from
`dqr-web-service.arm.gov`, a **different host from `adc.arm.gov`**; if the call raises
a proxy 403, call `request_network_access(domain="dqr-web-service.arm.gov")`.

```python
act.qc.print_dqr("sgp30ecorE14.b1", "20150101", "20190101")   # browse what exists
ds = act_qc_with_dqr(ds, variable="h")                        # fold into qc_h
```

The DQR arrives as an extra bit whose meaning is `"D151209.1 : Icing conditions
caused sensible and latent heat fluxes ... to be incorrect during much of this
period."` — the report ID is in the string, so it survives into any figure or table
you generate from `flag_meanings`. `add_dqr_to_qc` cleans QC attributes on the way in
(`cleanup_qc=True` by default), so it is safe on a freshly read dataset.

Useful arguments: `variable=` to limit the query, `assessment='incorrect,suspect'`
(the default; add `'missing'` to catch outage reports), `include`/`exclude` to filter
by DQR ID, and `dqr_link=True` to attach the web link.

## 7. Summarising

`ds.qcfilter.create_qc_summary()` collapses every bit into a single ranked
`flag_values` variable — 0 not failing, 1-2 suspect, 3-4 incorrect. It is the right
form for handing QC to a non-ARM consumer or an ML pipeline, but it is **lossy and
irreversible**: the per-test bits are gone afterwards, so run it on a copy if you
still need to know which test fired.

Supplemental QC from a YAML file — the way a scientist records "the instrument was
being serviced on these three afternoons" — is read with
`act.qc.read_yaml_supplemental_qc`; ACT's own
`examples/qc/sgpmfrsr7nchE11.b1.yaml` shows the schema.

## Kernel helpers

- `act_qc_variables(ds)` -> data variable -> QC variable mapping
- `act_qc_assessments(ds)` -> sorted list of assessment strings present
- `act_qc_table(ds, variables=None)` -> DataFrame of per-test flagged counts and percent
- `act_qc_apply(ds, variables=None, assessments=None)` -> in-place NaN fill using all four assessment names
- `act_qc_masked(ds, variable)` -> NaN-filled array for one variable
- `act_qc_with_dqr(ds, variable=None, normalize_assessment=True)` -> DQRs folded in

## Reporting QC honestly

When QC changes a result, say what it removed. "Mean sensible heat flux over the
period, after removing 199 of 240 half-hours flagged Incorrect by DQR D151209.1" is a
defensible sentence; the same mean with no caveat is not. If a filter removes most of
a record, that is the finding — surface it rather than reporting a mean over the
survivors.
