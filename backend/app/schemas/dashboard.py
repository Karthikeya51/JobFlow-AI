from pydantic import BaseModel, Field


class DashboardSummarySchema(BaseModel):
    total: int = 0
    saved: int = 0
    applied: int = 0
    interview: int = 0
    offer: int = 0
    rejected: int = 0


class DashboardConversionSchema(BaseModel):
    interview_rate: float = 0.0
    offer_rate: float = 0.0


class DashboardStatusDistributionSchema(BaseModel):
    status: str
    count: int = 0


class DashboardTrendPointSchema(BaseModel):
    month: str
    count: int = 0


class DashboardRecentApplicationSchema(BaseModel):
    id: str = Field(alias="_id")
    company: str
    job_title: str
    status: str
    applied_date: str | None = None
    created_at: str

    model_config = {"populate_by_name": True}


class DashboardStatsResponseSchema(BaseModel):
    summary: DashboardSummarySchema
    conversion: DashboardConversionSchema
    status_distribution: list[DashboardStatusDistributionSchema]
    monthly_trend: list[DashboardTrendPointSchema]
    recent_applications: list[DashboardRecentApplicationSchema]
