from celery import shared_task

from django.core.mail import send_mail

from time import sleep

@shared_task
def send_email_task(email,subject,body):

    sleep(10)
    for e in email:
        send_mail(subject,
                  body,
                  'channel.developer.mail@gmail.com',
                  [e]
        )
    return None