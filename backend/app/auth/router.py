from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.auth.models import LoginRequest, RefreshRequest, TokenResponse, UserInfo
from app.auth.utils import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/login", response_model=TokenResponse, summary="Obtain JWT tokens")
def login(request: LoginRequest):
    """
    Authenticate with **username** and **password**.

    Returns an access token (valid for 300 s) and a refresh token (valid for 3600 s).
    """
    user = authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenResponse(
        access_token=create_access_token(user["username"]),
        refresh_token=create_refresh_token(user["username"]),
    )


@router.post("/refresh", response_model=TokenResponse, summary="Refresh JWT tokens")
def refresh(request: RefreshRequest):
    """
    Exchange a valid **refresh token** for a new pair of access/refresh tokens.
    """
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(request.refresh_token)
    except JWTError:
        raise credentials_error

    if payload.get("type") != "refresh":
        raise credentials_error

    username: str = payload.get("sub")
    if not username:
        raise credentials_error

    return TokenResponse(
        access_token=create_access_token(username),
        refresh_token=create_refresh_token(username),
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserInfo:
    """Dependency that extracts and validates the Bearer access token."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired access token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise credentials_error

    if payload.get("type") != "access":
        raise credentials_error

    username: str = payload.get("sub")
    if not username:
        raise credentials_error

    return UserInfo(username=username)
