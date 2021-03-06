# License: BSD 3 clause

import numpy as np
from matplotlib.figure import Figure
from matplotlib.ticker import IndexLocator

from scalpel.core.cohort import Cohort
from scalpel.stats.decorators import title, xlabel, ylabel
from scalpel.stats.grouper import agg_by_col, event_duration_agg

registry = []


def register(f):
    registry.append(f)
    return f


@register
@xlabel("Number of Days")
@ylabel("Count (log)")
@title("duration distribution")
def plot_duration_distribution_per_day_as_line(
    figure: Figure, cohort: Cohort
) -> Figure:
    assert cohort.is_duration_events()

    df = event_duration_agg(cohort, "count").sort_values("duration")
    ax = figure.gca()
    ax.plot(df.duration, df["count(1)"])
    ax.set_yscale("log")

    major = IndexLocator(365, +0.0)
    minor = IndexLocator(30, +0.0)
    ax.xaxis.set_minor_locator(minor)
    ax.xaxis.set_major_locator(major)
    ax.grid(True, which="major", axis="x")
    return figure


@register
@ylabel("Count")
@xlabel("Duration in months")
@title("duration distribution")
def plot_duration_distribution_per_month_as_bar(
    figure: Figure, cohort: Cohort
) -> Figure:
    assert cohort.is_duration_events()

    df = event_duration_agg(cohort, "count").sort_values("duration")
    df.duration = np.ceil(df.duration / 30)
    df.duration = df.duration.astype("int32")
    df = df.groupby("duration").sum().reset_index()
    ax = figure.gca()
    ax.bar(range(len(df)), df["count(1)"].values)
    ax.set_xticklabels(df.duration.values)
    ax.set_xticks(range(len(df)))

    return figure


@register
@ylabel("Value")
@xlabel("Duration (in days)")
@title("mean duration per value")
def plot_mean_duration_per_value(figure: Figure, cohort: Cohort) -> Figure:
    assert cohort.is_duration_events()

    df = agg_by_col(
        cohort.events, frozenset(["value"]), "duration", "mean"
    ).sort_values("value")
    ax = figure.gca()
    ax.barh(range(len(df.value)), df["avg(duration)"].values)
    ax.set_yticklabels(df.value.values)
    ax.set_yticks(range(len(df.value)))
    return figure
