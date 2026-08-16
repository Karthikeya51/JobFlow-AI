import re
from datetime import datetime

from bson import ObjectId

from app.database import get_database
from app.models.application import Application
from app.utils.errors import (
    ApplicationAccessDeniedException,
    ApplicationNotFoundException,
)


class ApplicationService:
    def __init__(self):
        self.db = get_database()
        self.applications_collection = self.db["applications"]

    @staticmethod
    def _to_object_id(value: str) -> ObjectId:
        try:
            return ObjectId(value)
        except Exception as exc:
            raise ApplicationNotFoundException() from exc

    def create_application(self, user_id: str, data: dict) -> Application:
        application = Application(
            user_id=ObjectId(user_id),
            company=data["company"],
            job_title=data["job_title"],
            location=data.get("location"),
            job_url=data.get("job_url"),
            job_description=data["job_description"],
            salary=data.get("salary"),
            status=data.get("status", "Saved"),
            applied_date=data.get("applied_date"),
            notes=data.get("notes"),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        result = self.applications_collection.insert_one(application.to_dict())
        application._id = result.inserted_id
        return application

    def list_applications(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):
        query = {"user_id": ObjectId(user_id)}

        if status:
            query["status"] = status

        if search:
            search_filter = {
                "$or": [
                    {"company": {"$regex": re.escape(search), "$options": "i"}},
                    {"job_title": {"$regex": re.escape(search), "$options": "i"}},
                    {"location": {"$regex": re.escape(search), "$options": "i"}},
                ]
            }
            query.update(search_filter)

        valid_sort_fields = {"created_at", "applied_date", "company", "job_title"}
        sort_field = sort_by if sort_by in valid_sort_fields else "created_at"
        sort_direction = -1 if sort_order.lower() == "desc" else 1

        total = self.applications_collection.count_documents(query)
        skip = (page - 1) * limit
        documents = list(
            self.applications_collection.find(query)
            .sort(sort_field, sort_direction)
            .skip(skip)
            .limit(limit)
        )

        items = [Application.from_dict(document) for document in documents]
        pages = (total + limit - 1) // limit if total else 0

        return {
            "items": items,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }

    def get_application_for_user(self, application_id: str, user_id: str) -> Application:
        object_id = self._to_object_id(application_id)
        document = self.applications_collection.find_one({"_id": object_id})

        if not document:
            raise ApplicationNotFoundException()

        if str(document["user_id"]) != str(user_id):
            raise ApplicationAccessDeniedException()

        return Application.from_dict(document)

    def update_application(
        self,
        application_id: str,
        user_id: str,
        data: dict,
    ) -> Application:
        existing = self.get_application_for_user(application_id, user_id)

        update_data = {}
        for key, value in data.items():
            if value is not None:
                update_data[key] = value

        if not update_data:
            return existing

        update_data["updated_at"] = datetime.utcnow()
        self.applications_collection.update_one(
            {"_id": existing._id},
            {"$set": update_data},
        )

        refreshed = self.applications_collection.find_one({"_id": existing._id})
        return Application.from_dict(refreshed)

    def delete_application(self, application_id: str, user_id: str) -> None:
        application = self.get_application_for_user(application_id, user_id)
        self.applications_collection.delete_one({"_id": application._id})
