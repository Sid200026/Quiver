from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def sendEmail(to, subject, message):
    # fmt: off
    email = EmailMessage(subject, message, to=[to, ])
    # fmt: on
    email.send(fail_silently=False)
