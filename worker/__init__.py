import os
from celery import Celery

from social import settings
from worker import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social.settings")

celery_app = Celery('social')
celery_app.config_from_object(config)
celery_app.autodiscover_tasks()
