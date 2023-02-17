from django.core.mail import send_mail, mail_admins
from djbook_test.settings import EMAIL_HOST_USER


def send(subject, message, user_email, from_email=EMAIL_HOST_USER):
    send_mail(
        subject=subject,
        message=message,
        recipient_list=[user_email],
        from_email=from_email,
        fail_silently=False,
    )


def admin_send(subject, message):
    mail_admins(subject=subject, message=message)
