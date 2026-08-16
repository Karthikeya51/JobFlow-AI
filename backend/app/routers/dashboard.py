from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models import User
from app.schemas.dashboard import DashboardStatsResponseSchema
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def get_dashboard_service() -> DashboardService:
    return DashboardService()


@router.get("/stats", response_model=DashboardStatsResponseSchema)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    dashboard_service: DashboardService = Depends(get_dashboard_service),
):
    return dashboard_service.get_dashboard_stats(str(current_user._id))
