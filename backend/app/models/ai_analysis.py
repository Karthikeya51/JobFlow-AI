from datetime import datetime

from bson import ObjectId


class AIAnalysis:
    def __init__(
        self,
        user_id: ObjectId,
        application_id: ObjectId,
        analysis_type: str,
        result: dict,
        created_at: datetime | None = None,
        _id: ObjectId | None = None,
    ):
        self._id = _id or ObjectId()
        self.user_id = user_id
        self.application_id = application_id
        self.analysis_type = analysis_type
        self.result = result
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "application_id": self.application_id,
            "analysis_type": self.analysis_type,
            "result": self.result,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return AIAnalysis(
            _id=data.get("_id"),
            user_id=data.get("user_id"),
            application_id=data.get("application_id"),
            analysis_type=data.get("analysis_type"),
            result=data.get("result", {}),
            created_at=data.get("created_at"),
        )
