web: gunicorn app:app
worker: celery -A app.celery worker
init: python db_create.py
upgrade: python db_upgrade.py