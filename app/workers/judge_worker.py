import logging
import time

from redis import RedisError

from app.core.redis import redis_client
from app.db.session import SessionLocal
from app.services.judge_service import JudgeService

logger = logging.getLogger(__name__)
QUEUE_NAME = "submission_queue"


def run_worker() -> None:
    """
    Continuously consume submissions from Redis
    and delegate judging to the JudgeService.
    """

    logger.info("Judge worker started.")

    while True:
        try:
            item = redis_client.blpop(
                [QUEUE_NAME],
                timeout=0,
            )
        except RedisError as exc:
            logger.warning(
                "Redis queue unavailable in worker: %s. Retrying in 1s.",
                exc,
            )
            time.sleep(1)
            continue

        if item is None:
            continue

        if len(item) != 2:
            logger.warning("Unexpected queue payload: %s", item)
            continue

        _, submission_id = item

        db = SessionLocal()

        try:
            JudgeService(db).judge_submission(int(submission_id))
        except Exception:
            logger.exception(
                "Error while processing submission %s",
                submission_id,
            )
        finally:
            db.close()


if __name__ == "__main__":
    run_worker()
