import os

from celery import Celery

# Set the default settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Load configuration from settings.py using the CELERY namespace
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all apps
app.autodiscover_tasks()

# --- NEW: Schedule Definition (Beat) ---
app.conf.beat_schedule = {
    "check-every-minute": {
        "task": "monitoring.tasks.check_all_domains_task",
        "schedule": 60.0,  # Execute every 60 seconds
    },
}
