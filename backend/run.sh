sleep 2 # waiting for DB
alembic upgrade head
gunicorn "src.app:app" -b 0.0.0.0:5000
