import os
import django
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market_place.settings')
django.setup()
app = Celery('market_place')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'send_spam': {
        'task': 'product.tasks.send_product_info',
        'schedule': crontab(minute='*/5')
    }
}