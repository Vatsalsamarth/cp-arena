from app.core.redis import redis_client


SUBMISSION_QUEUE = "submission_queue"


class RedisQueue:
    """
    Queue abstraction for submission processing.
    """

    def __init__(self):
        self.redis = redis_client

    def enqueue_submission(
        self,
        submission_id: int,
    ) -> None:
        """
        Push a submission ID onto the queue.
        """

        self.redis.rpush(
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

        submission_id = self.redis.lpop(
            SUBMISSION_QUEUE
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

        return self.redis.llen(
            SUBMISSION_QUEUE
        )