from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ResumeUpdateSchema(BaseModel):
    resume_text: str = Field(..., min_length=10, max_length=20000)

    @field_validator("resume_text")
    @classmethod
    def validate_resume_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned or len(cleaned) < 10:
            raise ValueError("resume_text must contain a meaningful amount of content")
        return cleaned


class ResumeResponseSchema(BaseModel):
    id: str = Field(alias="_id")
    resume_text: str
    updated_at: datetime

    model_config = {"populate_by_name": True}
