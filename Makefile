.PHONY: run migrate revision upgrade downgrade lint format test

run:
	uvicorn app.main:app --reload --reload-dir app

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(MSG)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

lint:
	ruff check .

format:
	black .

test:
	pytest -v
