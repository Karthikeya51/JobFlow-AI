from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator

from app.models.application import ApplicationStatus


class ApplicationBaseSchema(BaseModel):
    company: str = Field(..., min_length=1, max_length=200)
    job_title: str = Field(..., min_length=1, max_length=200)
    location: Optional[str] = Field(None, max_length=200)
    job_url: Optional[str] = Field(None, max_length=500)
    job_description: str = Field(..., min_length=1, max_length=5000)
    salary: Optional[str] = Field(None, max_length=200)
    status: str = Field(default=ApplicationStatus.SAVED.value, max_length=50)
    applied_date: Optional[datetime] = None
    notes: Optional[str] = Field(None, max_length=2000)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        allowed = [status.value for status in ApplicationStatus]
        if value not in allowed:
            raise ValueError(
                f"Status must be one of: {', '.join(allowed)}"
            )
        return value

    @field_validator("job_url")
    @classmethod
    def validate_job_url(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value == "":
            return None
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("job_url must be a valid HTTP or HTTPS URL")
        return value


class ApplicationCreateSchema(ApplicationBaseSchema):
    pass


class ApplicationUpdateSchema(ApplicationBaseSchema):
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    job_title: Optional[str] = Field(None, min_length=1, max_length=200)
    job_description: Optional[str] = Field(None, min_length=1, max_length=5000)
    status: Optional[str] = Field(None, max_length=50)


class ApplicationResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    company: str
    job_title: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    job_description: str
    salary: Optional[str] = None
    status: str
    applied_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"populate_by_name": True}


class ApplicationListResponseSchema(BaseModel):
    items: list[ApplicationResponseSchema]
    page: int
    limit: int
    total: int
    pages: int
