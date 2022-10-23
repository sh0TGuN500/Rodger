web: gunicorn djbook_test.wsgi
worker: celery -A djbook_test worker -l info --app=tasks.app