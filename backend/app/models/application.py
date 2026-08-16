from datetime import datetime
from enum import Enum

from bson import ObjectId


class ApplicationStatus(str, Enum):
    SAVED = "Saved"
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"


class Application:
    def __init__(
        self,
        user_id: ObjectId,
        company: str,
        job_title: str,
        job_description: str,
        location: str | None = None,
        job_url: str | None = None,
        salary: str | None = None,
        status: str = ApplicationStatus.SAVED.value,
        applied_date: datetime | None = None,
        notes: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.company = company
        self.job_title = job_title
        self.location = location
        self.job_url = job_url
        self.job_description = job_description
        self.salary = salary
        self.status = status
        self.applied_date = applied_date
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or self.created_at

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "company": self.company,
            "job_title": self.job_title,
            "location": self.location,
            "job_url": self.job_url,
            "job_description": self.job_description,
            "salary": self.salary,
            "status": self.status,
            "applied_date": self.applied_date,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data):
        return Application(
            _id=data.get("_id"),
            user_id=data.get("user_id"),
            company=data.get("company"),
            job_title=data.get("job_title"),
            location=data.get("location"),
            job_url=data.get("job_url"),
            job_description=data.get("job_description"),
            salary=data.get("salary"),
            status=data.get("status", ApplicationStatus.SAVED.value),
            applied_date=data.get("applied_date"),
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
