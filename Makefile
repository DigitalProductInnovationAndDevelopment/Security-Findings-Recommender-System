
.ONESHELL: # Applies to every targets in the file!

all:
	cd ~/some_dir
	pwd # Prints ~/some_dir if cd succeeded


db-schema:
ifeq ($(name),)
	@echo "Usage: make gen-schema name=<schema_name>"
else
	cd src && alembic revision --autogenerate -m "$(name)"
endif	
db-migrate:
	cd src && alembic upgrade head

db-migrate-down:
	cd src && alembic downgrade -1

db-migrate-down-base:
	cd src && alembic downgrade base


dev:
	cd src && uvicorn app:app --host 0.0.0.0 --port 8001 --reload 


start-worker:
	cd src && celery -A task.worker worker --loglevel=info --concurrency 1