# alx_backend_caching_property_listings/celery.py
from __future__ import annotations
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_caching_property_listings.settings")

app = Celery("alx_backend_caching_property_listings")
# Read config from Django settings, CELERY_ prefixed settings are respected
app.config_from_object("django.conf:settings", namespace="CELERY")
# Auto-discover tasks.py in installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Celery debug task: {self.request!r}")