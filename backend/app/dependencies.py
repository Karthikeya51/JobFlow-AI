from fastapi import Depends, Header
from app.utils import decode_access_token, InvalidTokenException, MissingTokenException
from app.services import AuthService


def get_auth_service() -> AuthService:
    return AuthService()


async def get_current_user(
    authorization: str = Header(None),
    auth_service: AuthService = Depends(get_auth_service),
):
    if not authorization:
        raise MissingTokenException()

    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise MissingTokenException()

    token = parts[1]

    # Decode token
    payload = decode_access_token(token)
    if not payload:
        raise InvalidTokenException()

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenException()

    # Get user from database
    user = auth_service.get_user_by_id(user_id)
    return user
