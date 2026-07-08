from typing import Any


def set_tracked(
    redis_client: Any,
    tracking_set: str,
    key: str,
    value: str,
    ex: int | None = None,
) -> None:
    """Set `key` in Redis and add it to `tracking_set` for later invalidation.

    Uses a pipeline to ensure the key is set and tracked atomically.
    """
    try:
        pipeline = redis_client.pipeline()
        if ex is not None:
            pipeline.set(key, value, ex=ex)
        else:
            pipeline.set(key, value)
        pipeline.sadd(tracking_set, key)
        pipeline.execute()
    except Exception:
        # Non-fatal: caching should not break the application.
        try:
            # Best-effort fallback to simple set.
            if ex is not None:
                redis_client.set(key, value, ex=ex)
            else:
                redis_client.set(key, value)
        except Exception:
            pass


def invalidate_tracked(redis_client: Any, tracking_set: str) -> None:
    """Invalidate all keys tracked in `tracking_set` and remove the tracking set."""
    try:
        keys = redis_client.smembers(tracking_set) or set()

        if not keys:
            # Nothing to do; ensure the set is removed if empty.
            try:
                redis_client.delete(tracking_set)
            except Exception:
                pass
            return

        pipeline = redis_client.pipeline()
        for key in keys:
            pipeline.delete(key)
            pipeline.srem(tracking_set, key)
        pipeline.execute()

        try:
            redis_client.delete(tracking_set)
        except Exception:
            pass
    except Exception:
        # Swallow errors to avoid affecting core flows.
        pass
