import logging
import time

from redis import RedisError

from app.core.exceptions import QueueUnavailableError
from app.core.redis import redis_client

logger = logging.getLogger(__name__)


SUBMISSION_QUEUE = "submission_queue"


class RedisQueue:
    """
    Queue abstraction for submission processing.
    """

    def __init__(self):
        self.redis = redis_client

    def _execute_redis_call(self, func, *args, **kwargs):
        attempts = 2
        delay = 0.5

        for attempt in range(1, attempts + 1):
            try:
                return func(*args, **kwargs)
            except RedisError as exc:
                logger.warning(
                    "Redis queue attempt %s/%s failed: %s",
                    attempt,
                    attempts,
                    exc,
                )
                if attempt == attempts:
                    logger.exception("Redis queue is unavailable after retries.")
                    raise QueueUnavailableError(
                        "Redis queue is unavailable."
                    ) from exc
                time.sleep(delay)

    def enqueue_submission(
        self,
        submission_id: int,
    ) -> None:
        """
        Push a submission ID onto the queue.
        """

        self._execute_redis_call(
            self.redis.rpush,
            SUBMISSION_QUEUE,
            submission_id,
        )

    def dequeue_submission(
        self,
    ) -> int | None:
        """
        Pop the next submission ID from the queue.

        Returns None if the queue is empty.
        """

        submission_id = self._execute_redis_call(
            self.redis.lpop,
            SUBMISSION_QUEUE,
        )

        if submission_id is None:
            return None

        return int(submission_id)

    def queue_size(
        self,
    ) -> int:
        """
        Return the current queue length.
        """

        return self._execute_redis_call(
            self.redis.llen,
            SUBMISSION_QUEUE,
        )
