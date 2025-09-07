# properties/tasks.py
from celery import shared_task
from django.core.cache import cache
from .models import User, Booking

@shared_task
def clear_all_user_cache():
    cache.delete("all_users")

@shared_task
def clear_all_booking_cache():
    cache.delete("all_bookings")

@shared_task
def prewarm_user_and_booking_caches():
    users = list(User.objects.all().values("id","username","first_name","last_name","email","joined_at"))
    bookings = list(Booking.objects.all().values("id","user__username","property__title","start_date","end_date","booked_at"))
    cache.set("all_users", users, 3600)
    cache.set("all_bookings", bookings, 3600)
    return {"users": len(users), "bookings": len(bookings)}