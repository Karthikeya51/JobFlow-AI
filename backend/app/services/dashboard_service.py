from collections import defaultdict
from datetime import datetime

from bson import ObjectId

from app.database import get_database
from app.models.application import ApplicationStatus


class DashboardService:
    def __init__(self):
        self.db = get_database()
        self.applications_collection = self.db["applications"]

    def get_dashboard_stats(self, user_id: str):
        user_object_id = ObjectId(user_id)
        query = {"user_id": user_object_id}

        status_values = [status.value for status in ApplicationStatus]

        summary = {
            "total": self.applications_collection.count_documents(query),
            "saved": self.applications_collection.count_documents({**query, "status": "Saved"}),
            "applied": self.applications_collection.count_documents({**query, "status": "Applied"}),
            "interview": self.applications_collection.count_documents({**query, "status": "Interview"}),
            "offer": self.applications_collection.count_documents({**query, "status": "Offer"}),
            "rejected": self.applications_collection.count_documents({**query, "status": "Rejected"}),
        }

        relevant = max(summary["applied"] + summary["interview"] + summary["offer"] + summary["rejected"], 1)
        interview_rate = ((summary["interview"] + summary["offer"]) / relevant) * 100 if relevant else 0.0
        offer_rate = (summary["offer"] / relevant) * 100 if relevant else 0.0

        status_distribution = [
            {"status": status, "count": summary[status.lower()]}
            for status in status_values
        ]

        trend = self._build_monthly_trend(user_object_id)

        recent_documents = list(
            self.applications_collection.find(query)
            .sort("updated_at", -1)
            .limit(5)
        )

        recent_applications = [
            {
                "_id": str(doc["_id"]),
                "company": doc["company"],
                "job_title": doc["job_title"],
                "status": doc.get("status", "Saved"),
                "applied_date": doc.get("applied_date").isoformat() if doc.get("applied_date") else None,
                "created_at": doc.get("created_at").isoformat() if doc.get("created_at") else None,
            }
            for doc in recent_documents
        ]

        return {
            "summary": summary,
            "conversion": {
                "interview_rate": round(interview_rate, 2),
                "offer_rate": round(offer_rate, 2),
            },
            "status_distribution": status_distribution,
            "monthly_trend": trend,
            "recent_applications": recent_applications,
        }

    def _build_monthly_trend(self, user_id: ObjectId):
        current = datetime.utcnow()
        months = []
        for index in range(5, -1, -1):
            year = current.year
            month = current.month - index
            while month <= 0:
                year -= 1
                month += 12
            while month > 12:
                year += 1
                month -= 12
            month_key = f"{year}-{month:02d}"
            months.append({"month": month_key, "count": 0})

        pipeline = [
            {"$match": {"user_id": user_id}},
            {
                "$project": {
                    "month": {
                        "$dateToString": {"format": "%Y-%m", "date": {"$ifNull": ["$applied_date", "$created_at"]}}
                    }
                }
            },
            {"$group": {"_id": "$month", "count": {"$sum": 1}}},
        ]

        grouped = {item["_id"]: item["count"] for item in self.applications_collection.aggregate(pipeline)}
        for month in months:
            month["count"] = grouped.get(month["month"], 0)
        return months
