import time

from django.core.mail import send_mail


def order_mail(email, body):
    full_link = f'привет спасибо тебе за заказ \nмы с тобой свяжемся \n{body}'
    time.sleep(2)
    send_mail(
        'From shop project',
        full_link,
        'shamuza0102@gmail.com',
        [email]
    )