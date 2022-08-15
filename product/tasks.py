from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from market_place.celery import app
from product.models import Contact

User = get_user_model()

@app.task
def send_product_info(name):
    full_link = f'На сайте появился новый продукт!\nhttp://localhost:8000/product/'
    for user in User.objects.all():
        send_mail(
            'From shop project',
            full_link,
            'shamuza0102@gmail.com',
            [user.email],
        )
