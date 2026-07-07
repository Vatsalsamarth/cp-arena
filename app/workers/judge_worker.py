from app.core.redis import redis_client
from app.db.session import SessionLocal
from app.services.judge_service import JudgeService

QUEUE_NAME = "submission_queue"


def run_worker() -> None:
    """
    Continuously consume submissions from Redis
    and delegate judging to the JudgeService.
    """

    print("Judge worker started.")

    while True:
        item = redis_client.blpop(
            QUEUE_NAME,
            timeout=0,
        )

        if item is None:
            continue

        _, submission_id = item

        db = SessionLocal()

        try:
            JudgeService(db).judge_submission(
                int(submission_id)
            )
        finally:
            db.close()


if __name__ == "__main__":
    run_worker()