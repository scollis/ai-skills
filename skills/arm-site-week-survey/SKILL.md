---
name: arm-site-week-survey
description: "Survey what happened at an ARM site over a recent window (last 7 days, a campaign week, an arbitrary date range) by discovering which datastreams actually have data, staging the lightweight surface and profiling streams in bulk, and rendering a multi-panel week-overview figure plus a daily summary table. Use when the user asks what happened at an ARM site, wants a weekly or multi-day site survey, needs to know which instruments were reporting, or wants surface meteorology, precipitation, radiation, cloud base, PBL height and MWR water vapour pulled together over a period. Complements the per-event case-study skills: this one finds the events, those analyse one. Triggers: ARM Live, ARM site, BNF, SGP, ENA, NSA, AMF, last 7 days, weekly summary, what happened at, datastream discovery, site survey, met, ceilometer, disdrometer, sonde, MWR, pluvio."
---

# ARM site week survey

Find out what actually happened at an ARM site over a window, without knowing in
advance which instruments were running or where the interesting weather was.

The shape of the work is always the same: **discover which datastreams have data
-> bulk-stage the cheap ones -> read the weather off them -> only then decide
whether to pull radar.** Getting that order wrong means downloading tens of GB
before knowing which hour matters.

## Discovery: the catalog is not queryable, so probe

`adc.arm.gov/discovery` returns an HTML shell and the Solr endpoint 502s. The
working method is to probe the ARM Live query endpoint with constructed
datastream names, in parallel, and keep the hits:

```python
hits = discover_datastreams("bnf", ["M1", "S3", "S20", "S30", "S40"],
                            "2026-07-24", "2026-07-31")
```

`arm_query` returns an empty list for a name that does not exist, so a 1000-name
sweep costs a minute of threads and no errors. Roughly 3% of constructed names
hit — that is normal, not a sign the sweep is wrong.

Datastream names are `<site><instrument><facility>.<level>`, e.g.
`bnfmetS30.b1`. The default instrument and level lists in
`discover_datastreams` cover the common AMF loadout; extend `instruments=` for
site-specific gear. Level matters: `b1` is calibrated, `c1` is a derived VAP,
`a1`/`b0` are rawer. When both `a1` and `b1` exist for the same instrument,
take `b1`.

**Facility identity is not obvious from the name.** M1 is the main site; S-numbers
are supplementary and can sit tens of km away. Read `lat`/`lon` out of each met
file and compute range/bearing from the site centre before interpreting spatial
differences — at BNF the four met stations span 58 km, which is why weekly rain
totals differ 4x between them.

## Staging: split by file size, not by curiosity

Surface and profiling streams are 1-30 MB per day. Scanning radar is ~700 MB per
volume, and a week of it is over a terabyte. Stage them in separate passes:

```python
manifest = stage_datastreams(light_streams, start, end, dest, workers=8)
```

`arm_fetch` skips files already on disk, so re-running after an interruption is
cheap. Expect ~200 files / 2.5 GB for a week of a full AMF surface loadout, in
about 12 minutes on 8 threads — background the cell rather than blocking on it.

Radar comes last, targeted at the window the surface data identified, and even
then subsample: alternating volumes at ~16 min cadence usually resolves storm
evolution as well as every scan does.

## Reading the week

`load_datastream(dir, vars)` concatenates a datastream's daily files and applies
each variable's companion `qc_<var>` flag (keeping only `qc == 0`). Two habits
matter:

- **Reindex to a regular grid before plotting cumulative sums.** A gap in the
  files draws as a straight interpolated line across the missing day and looks
  like steady accumulation. `reindex(pd.date_range(...))` makes it a visible gap.
- **Aggregate precipitation across all facilities, not just M1.** Convective rain
  at a dispersed site is spatially patchy; the M1 gauge alone will understate the
  week.

For "what happened", the streams that carry the most signal per byte are:

| Stream | Reads |
|---|---|
| `met` (per facility) | temperature, wind, tipping-bucket rain |
| `ldquants` / `ld` | 1-min rain rate, drop size distribution |
| `ceil` | cloud base, and cloudy fraction as a proxy for regime |
| `sirs` | insolation — the cleanest discriminator of cloudy vs clear days |
| `mwr3c` | PWV and LWP — airmass moisture, better than surface RH |
| `sondewnpn`, `pblhtsonde1mcfarl` | soundings and PBL depth |

Cloudy fraction from the ceilometer and daily insolation from SIRS together
separate a week into regimes in one glance, which is usually the finding.

## The overview figure

`week_overview_figure` stacks six panels on a shared time axis: temperature,
cumulative precipitation with 1-min rain rate, wind, downwelling shortwave,
cloud base with sonde PBL top, and PWV/LWP. It returns the figure and axis list
so panels can be relabelled or extended.

Layout constraints worth keeping: place axes at explicit rectangles (a shared
x-axis stack fights `constrained_layout`), label facility series with coloured
text inside each panel rather than a legend box, and put day gridlines on every
panel so an event lines up vertically across all six.

Load the `figure-style` skill before rendering the deliverable version.

## Reporting

State the split the week actually shows rather than describing each panel in
turn. A useful summary names: the regime change and its date, the wettest
facility and how much of its total fell in one event, the last hour any gauge
recorded rain, and which streams had gaps. Put per-day numbers in a CSV, not in
prose.

Say which radar files exist versus which were staged — a week of C-SAPR2 at BNF
is 1511 files and staging 26 of them is a defensible choice, but only if stated.

## Caveats that recur

- **Partial days are normal.** A datastream reporting 6 files for a 7-day window
  usually means the current day has not been processed yet, not an outage.
- **`qc_` flags are per-variable.** Filtering the frame on one variable's flag
  silently drops good data from the others; filter each column separately.
- **Tipping buckets under-report light rain.** Where a disdrometer and a gauge
  disagree at low rates, trust the disdrometer for rate and the gauge for total.
- **MWR retrievals are unreliable during rain.** Discard the LWP spikes that
  coincide with rain rather than reading them as cloud liquid.
