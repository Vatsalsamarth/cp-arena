from __future__ import annotations

import logging
import time
import uuid

from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.core.logging import set_request_id
from app.core.rate_limiter import RateLimiter
from app.core.redis import redis_client

logger = logging.getLogger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Adds a request ID to each request and logs structured request events."""

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        request_id = (
            request.headers.get("X-Request-ID")
            or str(uuid.uuid4())
        )
        set_request_id(request_id)
        request.state.request_id = request_id

        start = time.perf_counter()
        logger.info(
            "request.start",
            extra={
                "method": request.method,
                "path": request.url.path,
                "request_id": request_id,
            },
        )

        response = await call_next(request)

        latency_ms = int((time.perf_counter() - start) * 1000)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "request.end",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": latency_ms,
                "request_id": request_id,
            },
        )

        return response


class RequestSizeLimiterMiddleware(BaseHTTPMiddleware):
    """Blocks requests whose Content-Length exceeds the configured limit."""

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        content_length = request.headers.get("content-length")

        if content_length is not None:
            try:
                length = int(content_length)
            except ValueError:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid content-length header."},
                )

            if length > settings.MAX_REQUEST_BODY_SIZE_BYTES:
                logger.warning(
                    "request.too_large",
                    extra={
                        "path": request.url.path,
                        "content_length": length,
                    },
                )
                return JSONResponse(
                    status_code=413,
                    content={"detail": "Request payload too large."},
                )

        return await call_next(request)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Global rate limiting middleware for all incoming requests."""

    def __init__(self, app: Any, **kwargs: Any) -> None:
        super().__init__(app)
        self.rate_limiter = RateLimiter(redis_client)

    async def dispatch(
        self,
        request: Request,
        call_next: Any,
    ) -> Response:
        client_ip = (
            request.client.host
            if request.client is not None
            else "unknown"
        )
        key = f"rate:{client_ip}"
        allowed, ttl = self.rate_limiter.allow_request(
            key,
            settings.RATE_LIMIT_REQUESTS_PER_MINUTE,
            settings.RATE_LIMIT_WINDOW_SECONDS,
        )

        if not allowed:
            logger.warning(
                "rate.limit.exceeded",
                extra={
                    "path": request.url.path,
                    "client_ip": client_ip,
                    "retry_after": ttl,
                },
            )
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Try again later."},
                headers={"Retry-After": str(ttl)},
            )

        return await call_next(request)
