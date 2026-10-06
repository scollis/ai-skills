"""Kernel helpers for ARM embedded quality control via ACT."""

ARM_ALL_ASSESSMENTS = ('Bad', 'Incorrect', 'Indeterminate', 'Suspect')


def act_qc_assessments(ds):
    """Every distinct assessment string present in the dataset's QC variables.

    Worth checking before filtering: `add_dqr_to_qc` renames Bad->Incorrect and
    Indeterminate->Suspect, so a hard-coded rm_assessments=['Bad'] can silently
    match nothing.
    """
    out = set()
    for name in ds.data_vars:
        for a in ds[name].attrs.get('flag_assessments', []) or []:
            out.add(str(a))
    return sorted(out)


def act_qc_variables(ds):
    """Map data variable -> its ancillary QC variable, for variables that have one."""
    pairs = {}
    for name in ds.data_vars:
        if str(name).startswith('qc_'):
            continue
        anc = ds[name].attrs.get('ancillary_variables', '')
        if isinstance(anc, (list, tuple)):
            anc = ' '.join(str(a) for a in anc)
        cands = [a for a in str(anc).split() if a in ds.data_vars]
        qc_name = 'qc_' + str(name)
        if qc_name in ds.data_vars and qc_name not in cands:
            cands.append(qc_name)
        for cand in cands:
            a = ds[cand].attrs
            if 'flag_masks' in a or 'flag_values' in a or str(cand).startswith('qc_'):
                pairs[str(name)] = cand
                break
    return pairs


def act_qc_table(ds, variables=None):
    """Per-test flagged-point counts as a DataFrame: variable, test, assessment, n, percent.

    Reads flag_masks/flag_meanings straight off the QC variables, so run
    `read_arm_netcdf(..., cleanup_qc=True)` (or `ds.clean.cleanup()`) first.
    """
    import numpy as np
    import pandas as pd

    rows = []
    pairs = act_qc_variables(ds)
    for var, qc_var in pairs.items():
        if variables is not None and var not in variables:
            continue
        attrs = ds[qc_var].attrs
        masks = attrs.get('flag_masks', None)
        values = attrs.get('flag_values', None)
        meanings = list(attrs.get('flag_meanings', []) or [])
        assessments = list(attrs.get('flag_assessments', []) or [])
        qcv = np.asarray(ds[qc_var].values)
        total = qcv.size
        codes = masks if masks is not None else values
        if codes is None:
            continue
        for i, code in enumerate(list(codes)):
            code = int(code)
            if masks is not None:
                n = int(np.count_nonzero(np.bitwise_and(qcv.astype('int64'), code)))
            else:
                n = int(np.count_nonzero(qcv == code))
            rows.append({
                'variable': var,
                'qc_variable': qc_var,
                'test': meanings[i] if i < len(meanings) else f'bit {code}',
                'assessment': assessments[i] if i < len(assessments) else '',
                'n_flagged': n,
                'percent': round(100.0 * n / total, 4) if total else 0.0,
                'n_total': total,
            })
    return pd.DataFrame(rows)


def act_qc_apply(ds, variables=None, assessments=None, del_qc_var=False):
    """Set every flagged point to NaN using ALL ARM assessment names, in place.

    ACT's `datafilter` matches assessment strings literally, and a dataset can carry
    both the raw vocabulary (Bad/Indeterminate) and the DQR-normalised one
    (Incorrect/Suspect) at once. Passing the full set avoids leaving flagged points
    in the data because only one vocabulary was named.
    """
    if assessments is None:
        assessments = list(ARM_ALL_ASSESSMENTS)
    ds.qcfilter.datafilter(
        variables=variables, rm_assessments=list(assessments), del_qc_var=del_qc_var
    )
    return ds


def act_qc_masked(ds, variable, assessments=None):
    """NaN-filled copy of one variable's values with flagged points removed."""
    if assessments is None:
        assessments = list(ARM_ALL_ASSESSMENTS)
    return ds.qcfilter.get_masked_data(
        variable, rm_assessments=list(assessments), return_nan_array=True
    )


def act_qc_with_dqr(ds, variable=None, normalize_assessment=True, **kwargs):
    """Fold ARM Data Quality Reports into the QC variables (needs dqr-web-service.arm.gov).

    Cleans the QC attributes on the way in, so it can be called on a freshly read
    dataset. With normalize_assessment=True (the default) the resulting assessments
    are Incorrect/Suspect, not Bad/Indeterminate.
    """
    import act

    return act.qc.arm.add_dqr_to_qc(
        ds, variable=variable, normalize_assessment=normalize_assessment, **kwargs
    )
