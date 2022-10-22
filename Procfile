web: gunicorn djbook_test.wsgi
celery -A djbook_test worker -l info --app=tasks.app