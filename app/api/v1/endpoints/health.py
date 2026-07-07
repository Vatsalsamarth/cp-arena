import logging
from datetime import datetime

from fastapi import APIRouter

from app.core.config import settings
from app.core.redis import redis_client
from app.db.database import engine

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> dict:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "CP Arena",
    }


@router.get("/ready")
async def readiness_probe() -> dict:
    """Readiness probe checks if all dependencies are available."""
    errors = []

    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception as exc:
        logger.error("Database readiness check failed: %s", exc)
        errors.append(f"database: {exc}")

    try:
        redis_client.ping()
    except Exception as exc:
        logger.error("Redis readiness check failed: %s", exc)
        errors.append(f"redis: {exc}")

    if errors:
        return {
            "status": "not_ready",
            "errors": errors,
        }

    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/live")
async def liveness_probe() -> dict:
    """Liveness probe; always returns 200 if the app is running."""
    return {
        "status": "alive",
        "version": settings.APP_VERSION,
    }