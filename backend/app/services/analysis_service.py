from datetime import datetime

from bson import ObjectId

from app.database import get_database
from app.models.ai_analysis import AIAnalysis
from app.models.application import Application
from app.models.resume import ResumeProfile
from app.services.ai_service import AIService, AIServiceError
from app.services.application_service import ApplicationService
from app.services.resume_service import ResumeService


class AnalysisService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db["ai_analyses"]
        self.application_service = ApplicationService()
        self.resume_service = ResumeService()
        self.ai_service = AIService()

    def _get_analysis_for_application(self, user_id: str, application_id: str, analysis_type: str):
        document = self.collection.find_one(
            {"user_id": ObjectId(user_id), "application_id": ObjectId(application_id), "analysis_type": analysis_type}
        )
        if not document:
            return None
        return AIAnalysis.from_dict(document)

    def get_application_analysis(self, user_id: str, application_id: str):
        application = self.application_service.get_application_for_user(application_id, user_id)
        analysis = {
            "job_analysis": None,
            "resume_match": None,
        }
        job_result = self._get_analysis_for_application(user_id, application_id, "job_analysis")
        match_result = self._get_analysis_for_application(user_id, application_id, "resume_match")
        if job_result:
            analysis["job_analysis"] = job_result.result
        if match_result:
            analysis["resume_match"] = match_result.result
        return analysis

    def generate_job_analysis(self, user_id: str, application_id: str):
        application = self.application_service.get_application_for_user(application_id, user_id)
        if not application.job_description or not application.job_description.strip():
            raise ValueError("Application job description is required for analysis.")

        existing = self._get_analysis_for_application(user_id, application_id, "job_analysis")
        if existing:
            return existing.result

        result = AIService.generate_job_analysis(application.job_description)
        analysis = AIAnalysis(
            user_id=ObjectId(user_id),
            application_id=ObjectId(application_id),
            analysis_type="job_analysis",
            result=result,
            created_at=datetime.utcnow(),
        )
        self.collection.insert_one(analysis.to_dict())
        return result

    def generate_resume_match(self, user_id: str, application_id: str):
        application = self.application_service.get_application_for_user(application_id, user_id)
        resume = self.resume_service.get_resume_for_user(user_id)
        if not resume:
            raise FileNotFoundError("Resume profile not found. Add a resume before analyzing the match.")
        if not application.job_description or not application.job_description.strip():
            raise ValueError("Application job description is required for analysis.")

        existing = self._get_analysis_for_application(user_id, application_id, "resume_match")
        if existing:
            return existing.result

        result = AIService.generate_resume_match(resume.resume_text, application.job_description)
        analysis = AIAnalysis(
            user_id=ObjectId(user_id),
            application_id=ObjectId(application_id),
            analysis_type="resume_match",
            result=result,
            created_at=datetime.utcnow(),
        )
        self.collection.insert_one(analysis.to_dict())
        return result
