touch database.db
alembic upgrade head
export PYTHONPATH='.'
python src/main.py

