import os
from celery import Celery
from .settings import DEBUG, INSTALLED_APPS

if DEBUG:
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbook_test.settings')

app = Celery('djbook_test')

if not DEBUG:
    app.conf.update(BROKER_URL=os.environ['REDIS_URL'],
                    CELERY_RESULT_BACKEND=os.environ['REDIS_URL'])

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
