from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


def send_confirmation_mail(code, email):
    full_link = f'http://localhost:8000/api/account/active/{code}'
    send_mail(
        'Код для активации аккаунта',
        full_link,
        'shamuza0102@gmail.com',
        [email]
    )
