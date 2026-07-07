import logging

from redis import Redis, RedisError

from app.core.config import settings

logger = logging.getLogger(__name__)


def create_redis_client() -> Redis:
    client = Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        health_check_interval=30,
        retry_on_timeout=True,
    )

    try:
        client.ping()
    except RedisError as exc:
        logger.exception("Redis health check failed.")
        raise RuntimeError(
            "Unable to connect to Redis. Verify REDIS_URL and Redis availability."
        ) from exc

    return client


redis_client = create_redis_client()
