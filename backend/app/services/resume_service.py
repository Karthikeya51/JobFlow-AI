from datetime import datetime

from bson import ObjectId

from app.database import get_database
from app.models.resume import ResumeProfile


class ResumeService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["resume_profiles"]

    def get_resume_for_user(self, user_id: str) -> ResumeProfile | None:
        document = self.collection.find_one({"user_id": ObjectId(user_id)})
        if not document:
            return None
        return ResumeProfile.from_dict(document)

    def upsert_resume(self, user_id: str, resume_text: str) -> ResumeProfile:
        clean_text = resume_text.strip()
        profile = self.collection.find_one({"user_id": ObjectId(user_id)})
        updated_at = datetime.utcnow()

        if profile:
            self.collection.update_one(
                {"_id": profile["_id"]},
                {"$set": {"resume_text": clean_text, "updated_at": updated_at}},
            )
            profile["resume_text"] = clean_text
            profile["updated_at"] = updated_at
            return ResumeProfile.from_dict(profile)

        resume = ResumeProfile(user_id=ObjectId(user_id), resume_text=clean_text, updated_at=updated_at)
        result = self.collection.insert_one(resume.to_dict())
        resume._id = result.inserted_id
        return resume

    def delete_resume_for_user(self, user_id: str) -> bool:
        result = self.collection.delete_one({"user_id": ObjectId(user_id)})
        return result.deleted_count > 0
