from os import environ
from celery import Celery
from .settings import DEBUG, CELERY_BROKER_URL

if DEBUG:
    environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Set the default Django settings module for the 'celery' program.
environ.setdefault('DJANGO_SETTINGS_MODULE', 'djbook_test.settings')
app = Celery('djbook_test')

if not DEBUG:
    app.conf.update(BROKER_URL=CELERY_BROKER_URL,
                    CELERY_RESULT_BACKEND=CELERY_BROKER_URL)
    # app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": "optional"}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
