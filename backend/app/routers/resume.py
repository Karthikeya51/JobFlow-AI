from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies import get_current_user
from app.models import User
from app.schemas.resume import ResumeResponseSchema, ResumeUpdateSchema
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/api", tags=["resume"])


def get_resume_service() -> ResumeService:
    return ResumeService()


@router.get("/resume", response_model=ResumeResponseSchema)
async def get_resume(
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    resume = resume_service.get_resume_for_user(str(current_user._id))
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume profile not found")
    return {
        "_id": str(resume._id),
        "resume_text": resume.resume_text,
        "updated_at": resume.updated_at,
    }


@router.put("/resume", response_model=ResumeResponseSchema)
async def upsert_resume(
    request: ResumeUpdateSchema,
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    resume = resume_service.upsert_resume(str(current_user._id), request.resume_text)
    return {
        "_id": str(resume._id),
        "resume_text": resume.resume_text,
        "updated_at": resume.updated_at,
    }


@router.delete("/resume", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    current_user: User = Depends(get_current_user),
    resume_service: ResumeService = Depends(get_resume_service),
):
    resume_service.delete_resume_for_user(str(current_user._id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
