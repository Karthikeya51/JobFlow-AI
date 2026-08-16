from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_current_user
from app.models import User
from app.schemas.ai_analysis import AnalysisResponseSchema, JobAnalysisResult, ResumeMatchResult
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


def get_analysis_service() -> AnalysisService:
    return AnalysisService()


@router.post("/job/{application_id}", response_model=JobAnalysisResult)
async def analyze_job(
    application_id: str,
    current_user: User = Depends(get_current_user),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        result = analysis_service.generate_job_analysis(str(current_user._id), application_id)
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process AI analysis.") from exc


@router.post("/match/{application_id}", response_model=ResumeMatchResult)
async def analyze_match(
    application_id: str,
    current_user: User = Depends(get_current_user),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        result = analysis_service.generate_resume_match(str(current_user._id), application_id)
        return result
    except FileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process AI analysis.") from exc


@router.get("/application/{application_id}", response_model=AnalysisResponseSchema)
async def get_application_analysis(
    application_id: str,
    current_user: User = Depends(get_current_user),
    analysis_service: AnalysisService = Depends(get_analysis_service),
):
    try:
        return analysis_service.get_application_analysis(str(current_user._id), application_id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found") from exc
