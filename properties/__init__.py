# alx_backend_caching_property_listings/__init__.py
from alx_backend_caching_property_listings.celery import app as celery_app

__all__ = ("celery_app",)