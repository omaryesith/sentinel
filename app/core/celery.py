import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "check-every-minute": {
        "task": "monitoring.tasks.check_all_domains_task",
        "schedule": 60.0,  # Execute every 60 seconds
    },
}
