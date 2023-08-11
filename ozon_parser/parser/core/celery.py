import os
from celery import Celery

from ozon_parser.settings import CELERY_BACKEND


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core", backend=CELERY_BACKEND)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.set_default()
app.autodiscover_tasks()
