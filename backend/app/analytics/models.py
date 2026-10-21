from datetime import date

from pydantic import BaseModel, Field


class CategoryPerformance(BaseModel):
    category: str
    views: int = Field(ge=0)
    registrations: int = Field(ge=0)
    ad_spend: float = Field(ge=0)
    conversion_rate: float
    cost_per_registration: float | None

    
class PerformanceReport(BaseModel):
    period_start: date
    period_end: date
    total_views: int
    total_registrations: int
    total_ad_spend: float
    overall_conversion_rate: float
    categories: list[CategoryPerformance]