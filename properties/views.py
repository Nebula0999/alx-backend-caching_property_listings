from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .models import Property, User, Booking
from .utils import get_redis_cache_metrics, get_all_properties
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin


@cache_page(60 * 15)  # cache for 15 minutes (view-level cache)
def property_list(request):
    # use helper that already uses the cache under key `all_properties`
    properties = get_all_properties()
    permission_classes = [IsAuthenticated]
    return JsonResponse({"data": properties})


def cache_metrics(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)


def user_list(request):
    """Return all users; cache the result in Redis under key `all_users`."""
    users = cache.get("all_users")
    permission_classes = [IsAuthenticated & IsOwnerOrAdmin]

    if users is None:
        users = list(User.objects.all().values(
            "id", "username", "first_name", "last_name", "email", "joined_at"
        ))
        cache.set("all_users", users, 60 * 60)  # 1 hour

    return JsonResponse({"data": users})


def booking_list(request):
    """Return all bookings; cache the result in Redis under key `all_bookings`."""
    bookings = cache.get("all_bookings")
    permission_classes = [IsAuthenticated & IsOwnerOrAdmin]

    if bookings is None:
        bookings = list(Booking.objects.all().values(
            "id", "user__username", "property__title", "start_date", "end_date", "booked_at"
        ))
        cache.set("all_bookings", bookings, 60 * 60)  # 1 hour

    return JsonResponse({"data": bookings})