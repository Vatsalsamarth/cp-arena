import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import (
    RateLimitMiddleware,
    RequestContextMiddleware,
    RequestSizeLimiterMiddleware,
)

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

logger.info(
    "startup.initialization",
    extra={
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    },
)

register_exception_handlers(app)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestSizeLimiterMiddleware)
app.add_middleware(RequestContextMiddleware)

app.include_router(
    api_router,
    prefix="/api",
)

logger.info("startup.complete")


@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }
