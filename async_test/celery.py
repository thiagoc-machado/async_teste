from __future__ import absolute_import
import os
from celery import Celery

# Define o módulo settings padrão do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'async_test.settings')

app = Celery('async_test', broker='pyamqp://guest@localhost//')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()