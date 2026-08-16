from fastapi import APIRouter, Depends, status
from app.schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    TokenResponseSchema,
    UserResponseSchema,
)
from app.services import AuthService
from app.dependencies import get_auth_service, get_current_user
from app.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: UserRegisterSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    user = auth_service.register(
        name=request.name,
        email=request.email,
        password=request.password,
    )

    return {
        "_id": str(user._id),
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at.isoformat(),
    }


@router.post("/login", response_model=TokenResponseSchema)
async def login(
    request: UserLoginSchema,
    auth_service: AuthService = Depends(get_auth_service),
):
    user, token = auth_service.login(
        email=request.email,
        password=request.password,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "_id": str(user._id),
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat(),
        },
    }


@router.get("/me", response_model=UserResponseSchema)
async def get_current_user_endpoint(
    current_user: User = Depends(get_current_user),
):
    return {
        "_id": str(current_user._id),
        "name": current_user.name,
        "email": current_user.email,
        "created_at": current_user.created_at.isoformat(),
    }
