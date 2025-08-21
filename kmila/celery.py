import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kmila.settings")

celery_app = Celery("kmila")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()

celery_app.conf.enable_utc = False
celery_app.conf.timezone = settings.TIME_ZONE
