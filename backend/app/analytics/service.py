from datetime import date

import pandas as pd

from app.analytics.models import CategoryPerformance, PerformanceReport
from app.analytics.repository import CSVPerformanceRepository


class AnalyticsService:
    def __init__(self, repository: CSVPerformanceRepository) -> None:
        self._repository = repository

    def get_performance(
        self, start: date | None = None, end: date | None = None
    ) -> PerformanceReport:
        df = self._repository.load()

        if start is not None:
            df = df[df["date"].dt.date >= start]

        if end is not None:
            df = df[df["date"].dt.date <= end]

        if df.empty:
            raise ValueError("No analytics records for the selected period.")

        grouped = (
            df.groupby("category", as_index=False)
            .agg(
                views=("views", "sum"),
                registrations=("registrations", "sum"),
                ad_spend=("ad_spend", "sum"),
            )
            .sort_values("registrations", ascending=False)
        )

        categories: list[CategoryPerformance] = []

        for row in grouped.itertuples(index=False):
            views = int(row.views)
            registrations = int(row.registrations)
            ad_spend = float(row.ad_spend)

            conversion = registrations / views * 100 if views > 0 else 0.0

            cost_per_registration = (
                ad_spend / registrations if registrations > 0 else None
            )

            categories.append(
                CategoryPerformance(
                    category=str(row.category),
                    views=views,
                    registrations=registrations,
                    ad_spend=round(ad_spend, 2),
                    conversion_rate=round(conversion, 2),
                    cost_per_registration=(
                        round(cost_per_registration, 2)
                        if cost_per_registration is not None
                        else None
                    ),
                )
            )

        total_views = int(df["views"].sum())
        total_registrations = int(df["registrations"].sum())
        total_spend = float(df["ad_spend"].sum())

        overall_conversion = (
            total_registrations / total_views * 100 if total_views > 0 else 0.0
        )

        return PerformanceReport(
            period_start=df["date"].min().date(),
            period_end=df["date"].max().date(),
            total_views=total_views,
            total_registrations=total_registrations,
            total_ad_spend=round(total_spend, 2),
            overall_conversion_rate=round(overall_conversion, 2),
            categories=categories,
        )
