from datetime import datetime

from bson import ObjectId


class ResumeProfile:
    def __init__(
        self,
        user_id: ObjectId,
        resume_text: str,
        updated_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.resume_text = resume_text
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "resume_text": self.resume_text,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data):
        return ResumeProfile(
            _id=data.get("_id"),
            user_id=data.get("user_id"),
            resume_text=data.get("resume_text", ""),
            updated_at=data.get("updated_at"),
        )
