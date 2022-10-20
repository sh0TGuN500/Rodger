from django.core.mail import send_mail, mail_admins
from djbook_test.settings import EMAIL_HOST_USER


def send(subject, message, user_email, from_email=EMAIL_HOST_USER):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=[user_email],
        fail_silently=False,
    )
    print(user_email, from_email)
    print('send email')


def admin_send(subject, message):
    mail_admins(subject, message)
    print('send admin email')
