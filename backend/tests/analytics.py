
from pathlib import Path

from app.analytics.repository import CSVPerformanceRepository
from app.analytics.service import AnalyticsService


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "event_performance.csv"
)


def test_performance_totals():
    service = AnalyticsService(
        CSVPerformanceRepository(DATA_PATH)
    )

    report = service.get_performance()

    assert report.total_views == 27000
    assert report.total_registrations == 3900
    assert report.total_ad_spend == 1770.0
    assert report.overall_conversion_rate == 14.44


def test_category_conversion_rates():
    service = AnalyticsService(
        CSVPerformanceRepository(DATA_PATH)
    )

    report = service.get_performance()

    categories = {
        item.category: item
        for item in report.categories
    }

    assert categories["Concerts"].conversion_rate == 15.0
    assert categories["Corporate"].conversion_rate == 20.0
    assert categories["Sports"].conversion_rate == 10.0

    assert categories["Concerts"].registrations == 1800
    assert categories["Corporate"].registrations == 1200
    assert categories["Sports"].registrations == 900
