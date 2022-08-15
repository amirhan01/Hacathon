import time
from django.core.mail import send_mail
from market_place.celery import app


@app.task
def celery_order_mail(code, email):
    time.sleep(10)
    full_link = f'http://localhost:8000/api/v1/account/active/{code}'
    send_mail(
        'From shop project',
        full_link,
        'shamuza0102@gmail.com',
        [email]
    )
