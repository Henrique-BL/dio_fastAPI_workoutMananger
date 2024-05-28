run:
	@uvicorn workout_api.main:app --reload
create-migration:
	@set PYTHONPATH=$(PYTHONPATH);$(CURDIR) && alembic revision --autogenerate -m "$(d)"

run-migrations:
	@set PYTHONPATH=$(PYTHONPATH);$(CURDIR) && alembic upgrade head