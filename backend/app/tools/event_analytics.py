from datetime import date

from app.analytics.service import AnalyticsService


def get_event_performance(
    analytics: AnalyticsService,
    start_date: str | None = None,
    end_date: str | None = None,
) -> dict:
    start = date.fromisoformat(start_date) if start_date is not None else None
    end = date.fromisoformat(end_date) if end_date is not None else None

    if start and end and start > end:
        raise ValueError("start_date cannot be after end_date.")

    report = analytics.get_performance(start=start, end=end)

    return report.model_dump(mode="json")
