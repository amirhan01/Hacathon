import time
from django.core.mail import send_mail
from market_place.celery import app


@app.task
def celery_send_confirmation_email(code, email):
    time.sleep(5)
    full_link = f'http://localhost:8000/api/account/active/{code}'
    send_mail(
        'From shop project',
        full_link,
        'shamuza0102@gmail.com',
        [email]
    )