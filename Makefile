

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
	cd src &&  gunicorn app:app -b 0.0.0.0:8001 --reload