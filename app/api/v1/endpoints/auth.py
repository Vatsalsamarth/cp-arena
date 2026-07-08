import logging
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limiter import RateLimiter
from app.core.redis import get_redis_client
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

rate_limiter = RateLimiter(get_redis_client())


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate a user",
)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user and return a JWT access token.

    Includes brute-force protection with per-username rate limiting.
    """

    rate_limit_key = f"auth_attempt:{credentials.username}"

    is_allowed, ttl = rate_limiter.allow_request(
        key=rate_limit_key,
        limit=settings.AUTH_RATE_LIMIT_ATTEMPTS,
        window_seconds=settings.AUTH_RATE_LIMIT_WINDOW_SECONDS,
    )

    if not is_allowed:
        logger.warning(
            "login.rate_limited",
            extra={
                "username": credentials.username,
                "retry_after": ttl,
            },
        )
        raise HTTPException(
            status_code=HTTPStatus.TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {ttl} seconds.",
            headers={"Retry-After": str(ttl)},
        )

    try:
        service = AuthService(db)

        token = service.authenticate_user(
            username=credentials.username,
            password=credentials.password,
        )

        logger.info(
            "login.success",
            extra={"username": credentials.username},
        )

        return TokenResponse(**token)
    except Exception as exc:
        logger.error(
            "login.failed",
            extra={
                "username": credentials.username,
                "error": str(exc),
            },
        )
        raise
