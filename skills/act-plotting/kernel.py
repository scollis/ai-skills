"""Kernel helpers for the ACT Display family."""


def act_timeseries(ds, variables, figsize=None, day_night=True, dsname=None,
                   assessment_overplot=False, **plot_kwargs):
    """One TimeSeriesDisplay panel per variable; returns the display.

    `display.fig` and `display.axes` are the matplotlib objects — save with
    `display.fig.savefig(...)` so figure lineage is tracked.
    """
    import act

    if isinstance(variables, str):
        variables = [variables]
    n = len(variables)
    if figsize is None:
        figsize = (12, 2.8 * n + 0.8)
    display = act.plotting.TimeSeriesDisplay(ds, figsize=figsize, subplot_shape=(n,))
    for i, var in enumerate(variables):
        display.plot(
            var, dsname=dsname, subplot_index=(i,), day_night_background=day_night,
            assessment_overplot=assessment_overplot, **plot_kwargs
        )
    display.fig.tight_layout()
    return display


def act_qc_panel(ds, variable, figsize=None, dsname=None, day_night=True):
    """Two-panel figure: the variable with flagged points overplotted, and its QC block plot.

    Needs cleaned QC attributes (`read_arm_netcdf(..., cleanup_qc=True)`), otherwise the
    block plot has no flag_meanings to lay out.
    """
    import act

    if figsize is None:
        figsize = (12, 7)
    display = act.plotting.TimeSeriesDisplay(ds, figsize=figsize, subplot_shape=(2,))
    display.plot(
        variable, dsname=dsname, subplot_index=(0,),
        day_night_background=day_night, assessment_overplot=True,
    )
    display.qc_flag_block_plot(variable, dsname=dsname, subplot_index=(1,))
    display.fig.tight_layout()
    return display


def act_compare_datasets(ds_dict, variable, figsize=None, day_night=False):
    """Overlay the same variable from several datasets on one axis.

    ds_dict maps a label -> Dataset; the labels become the legend entries and are the
    `dsname` values every Display method expects once more than one dataset is loaded.
    """
    import act

    if figsize is None:
        figsize = (12, 4)
    import numpy as np

    display = act.plotting.TimeSeriesDisplay(ds_dict, figsize=figsize, subplot_shape=(1,))
    for label in ds_dict:
        display.plot(variable, dsname=label, subplot_index=(0,), label=label,
                     day_night_background=day_night)
    # Each plot() call resets the x range to its own dataset, so restore the union.
    t0 = min(np.asarray(d['time'].values).min() for d in ds_dict.values())
    t1 = max(np.asarray(d['time'].values).max() for d in ds_dict.values())
    display.set_xrng([t0, t1], subplot_index=(0,))
    display.axes[0].legend(loc='best', fontsize=8)
    display.fig.tight_layout()
    return display


def act_save_display(display, path, dpi=150, close=True):
    """Save a Display's figure and return the path."""
    import matplotlib.pyplot as plt

    display.fig.savefig(path, dpi=dpi, bbox_inches='tight')
    if close:
        plt.close(display.fig)
    return path
