from __future__ import annotations

from typing import Tuple

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
    ) -> Tuple[bool, int]:
        """Return whether the request is allowed and remaining TTL."""
        current = self.redis.incr(key)
        if current == 1:
            self.redis.expire(key, window_seconds)

        ttl = self.redis.ttl(key)
        is_allowed = current <= limit

        return is_allowed, max(int(ttl), 0)
