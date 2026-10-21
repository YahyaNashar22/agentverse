from io import BytesIO

from matplotlib.figure import Figure

from app.analytics.models import PerformanceReport


def create_conversion_chart(report: PerformanceReport) -> bytes:
    categories = [item.category for item in report.categories]

    values = [item.conversion_rate for item in report.categories]

    fig = Figure(figsize=(9, 5), dpi=140)
    ax = fig.subplots()

    bars = ax.bar(categories, values)

    ax.set_title("Event Category Conversion Rates")
    ax.set_ylabel("Conversion Rate (%)")
    ax.set_ylim(0, max(values, default=0) * 1.2 + 1)

    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:.2f}%",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
        )

    fig.tight_layout()
    
    buffer = BytesIO()
    fig.savefig(buffer, format="png")

    return buffer.getvalue()
