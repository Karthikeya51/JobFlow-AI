import json
import logging

from google import genai

from app.config import settings
from app.schemas.ai_analysis import JobAnalysisResult, ResumeMatchResult

logger = logging.getLogger(__name__)

from app.services.prompts import JOB_ANALYSIS_PROMPT, RESUME_MATCH_PROMPT


class AIServiceError(RuntimeError):
    pass


class AIService:
    def __init__(self):
        self.api_key = settings.effective_gemini_api_key or None
        self.model = getattr(settings, "GEMINI_MODEL", None) or "gemini-flash-latest"
        self.client = None
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def _ensure_available(self):
        if not self.client:
            raise AIServiceError("AI service is not configured.")

    def _extract_text(self, response):
        text = getattr(response, "text", None)
        if text:
            return text
        candidate = getattr(response, "candidates", None)
        if candidate:
            part = getattr(candidate[0], "content", None)
            if part:
                parts = getattr(part, "parts", None)
                if parts:
                    texts = [getattr(item, "text", "") for item in parts if getattr(item, "text", None)]
                    if texts:
                        return "\n".join(texts)
        return ""

    def _parse_json_response(self, raw_text: str):
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        if not cleaned:
            raise ValueError("Empty Gemini response")
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValueError("Gemini returned malformed JSON") from exc

    def _generate(self, prompt: str):
        self._ensure_available()
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            text = self._extract_text(response)
            return self._parse_json_response(text)
        except AIServiceError:
            raise
        except Exception as exc:
            logger.warning("Gemini request failed: %s", exc)
            raise AIServiceError("AI service is temporarily unavailable.") from exc

    @staticmethod
    def generate_job_analysis(job_description: str):
        service = AIService()
        payload = service._generate(JOB_ANALYSIS_PROMPT.format(job_description=job_description or ""))
        validated = JobAnalysisResult.model_validate(payload)
        return validated.model_dump()

    @staticmethod
    def generate_resume_match(resume_text: str, job_description: str):
        service = AIService()
        payload = service._generate(
            RESUME_MATCH_PROMPT.format(
                resume_text=resume_text or "",
                job_description=job_description or "",
            )
        )
        validated = ResumeMatchResult.model_validate(payload)
        return validated.model_dump()
