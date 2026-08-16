from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status

from app.dependencies import get_auth_service, get_current_user
from app.models import User
from app.schemas import (
    ApplicationCreateSchema,
    ApplicationListResponseSchema,
    ApplicationResponseSchema,
    ApplicationUpdateSchema,
)
from app.services import ApplicationService

router = APIRouter(prefix="/api/applications", tags=["applications"])


def get_application_service() -> ApplicationService:
    return ApplicationService()


@router.post(
    "",
    response_model=ApplicationResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_application(
    request: ApplicationCreateSchema,
    current_user: User = Depends(get_current_user),
    application_service: ApplicationService = Depends(get_application_service),
):
    application = application_service.create_application(
        user_id=str(current_user._id),
        data=request.model_dump(exclude_none=True),
    )
    return {
        "_id": str(application._id),
        "company": application.company,
        "job_title": application.job_title,
        "location": application.location,
        "job_url": application.job_url,
        "job_description": application.job_description,
        "salary": application.salary,
        "status": application.status,
        "applied_date": application.applied_date,
        "notes": application.notes,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
    }


@router.get("", response_model=ApplicationListResponseSchema)
async def list_applications(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    search: str | None = None,
    status: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    current_user: User = Depends(get_current_user),
    application_service: ApplicationService = Depends(get_application_service),
):
    result = application_service.list_applications(
        user_id=str(current_user._id),
        page=page,
        limit=limit,
        search=search,
        status=status,
        sort_by=sort_by,
        sort_order=sort_order,
    )

    return {
        "items": [
            {
                "_id": str(item._id),
                "company": item.company,
                "job_title": item.job_title,
                "location": item.location,
                "job_url": item.job_url,
                "job_description": item.job_description,
                "salary": item.salary,
                "status": item.status,
                "applied_date": item.applied_date,
                "notes": item.notes,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in result["items"]
        ],
        "page": result["page"],
        "limit": result["limit"],
        "total": result["total"],
        "pages": result["pages"],
    }


@router.get("/{application_id}", response_model=ApplicationResponseSchema)
async def get_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    application_service: ApplicationService = Depends(get_application_service),
):
    application = application_service.get_application_for_user(
        application_id,
        str(current_user._id),
    )

    return {
        "_id": str(application._id),
        "company": application.company,
        "job_title": application.job_title,
        "location": application.location,
        "job_url": application.job_url,
        "job_description": application.job_description,
        "salary": application.salary,
        "status": application.status,
        "applied_date": application.applied_date,
        "notes": application.notes,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
    }


@router.put("/{application_id}", response_model=ApplicationResponseSchema)
async def update_application(
    application_id: str,
    request: ApplicationUpdateSchema,
    current_user: User = Depends(get_current_user),
    application_service: ApplicationService = Depends(get_application_service),
):
    application = application_service.update_application(
        application_id,
        str(current_user._id),
        request.model_dump(exclude_none=True),
    )

    return {
        "_id": str(application._id),
        "company": application.company,
        "job_title": application.job_title,
        "location": application.location,
        "job_url": application.job_url,
        "job_description": application.job_description,
        "salary": application.salary,
        "status": application.status,
        "applied_date": application.applied_date,
        "notes": application.notes,
        "created_at": application.created_at,
        "updated_at": application.updated_at,
    }


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    application_service: ApplicationService = Depends(get_application_service),
):
    application_service.delete_application(application_id, str(current_user._id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
