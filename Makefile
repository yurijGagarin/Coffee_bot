run:
	python experiment.py
db-up:
	alembic upgrade head
db-down:
	alembic downgrade -1
db-redo:
	alembic downgrade -1 && alembic upgrade head
