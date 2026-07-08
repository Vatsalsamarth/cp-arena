from __future__ import annotations

from typing import Any

from redis import Redis


class RateLimiter:
    """Redis-backed fixed-window rate limiter."""

    def __init__(self, redis_client: Redis) -> None:
        self.redis = redis_client

    def allow_request(
        self,
        key: str,
        limit: int,
        window_seconds: int,
    ) -> tuple[bool, int]:
        """Return whether the request is allowed and remaining TTL."""
        current_raw: Any = self.redis.incr(key)
        current = int(current_raw)
        if current == 1:
            self.redis.expire(key, window_seconds)

        ttl_raw: Any = self.redis.ttl(key)
        ttl = int(ttl_raw)
        is_allowed = current <= limit

        return is_allowed, max(ttl, 0)
