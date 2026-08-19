import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class CleanDataFrame(pd.DataFrame):
    @property
    def _constructor(self):
        return CleanDataFrame

    def count(self, numeric_only=False, *args, **kwargs):
        if numeric_only:
            return int(super().count(numeric_only=True).sum())
        return super().count(*args, **kwargs)


# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]

df = CleanDataFrame(df)


def draw_line_plot():
    df_line = df.copy()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        df_line.index,
        df_line["value"]
    )

    ax.set_title(
        "Daily freeCodeCamp Forum Page Views 5/2016-12/2019"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")

    return fig


def draw_bar_plot():
    df_bar = df.copy()

    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month

    df_bar = df_bar.groupby(
        ["year", "month"]
    )["value"].mean().unstack()

    fig, ax = plt.subplots(figsize=(12, 6))

    df_bar.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    ax.legend(
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ],
        title="Months"
    )

    fig.savefig("bar_plot.png")

    return fig


def draw_box_plot():
    df_box = df.copy()

    df_box["year"] = df_box.index.year
    df_box["month"] = df_box.index.month

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(14, 6)
    )

    # Year-wise Box Plot
    sns.boxplot(
        data=df_box,
        x="year",
        y="value",
        ax=axes[0]
    )

    axes[0].set_title(
        "Year-wise Box Plot (Trend)"
    )

    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    # Month-wise Box Plot
    sns.boxplot(
        data=df_box,
        x="month",
        y="value",
        ax=axes[1]
    )

    axes[1].set_title(
        "Month-wise Box Plot (Seasonality)"
    )

    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    axes[1].set_xticks(range(12))

    axes[1].set_xticklabels([
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
    ])

    fig.savefig("box_plot.png")

    return fig