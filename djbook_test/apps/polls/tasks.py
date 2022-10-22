from djbook_test.celery import app

from .service import send, admin_send


@app.task
def send_task(message, subject, user_email):
    send(message, subject, user_email)


@app.task
def admin_send_task(subject, message):
    admin_send(subject, message)
