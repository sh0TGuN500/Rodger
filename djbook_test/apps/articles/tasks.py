from djbook_test.celery import app

from .service import send, admin_send


@app.task
def send_task(subject, message, user_email):
    send(subject, message, user_email)


@app.task
def admin_send_task(subject, message):
    admin_send(subject, message)
