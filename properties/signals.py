from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property, User, Booking
from .tasks import clear_all_user_cache, clear_all_booking_cache


@receiver(post_save, sender=Property)
def clear_cache_on_save(sender, instance, **kwargs):
    cache.delete("all_properties")


@receiver(post_delete, sender=Property)
def clear_cache_on_delete(sender, instance, **kwargs):
    cache.delete("all_properties")


from .models import User, Booking


@receiver(post_save, sender=User)
def clear_user_cache_on_save(sender, instance, **kwargs):
    clear_all_user_cache.delay()


@receiver(post_delete, sender=User)
def clear_user_cache_on_delete(sender, instance, **kwargs):
    clear_all_user_cache.delay()


@receiver(post_save, sender=Booking)
def clear_booking_cache_on_save(sender, instance, **kwargs):
    cache.delete("all_bookings")


@receiver(post_delete, sender=Booking)
def clear_booking_cache_on_delete(sender, instance, **kwargs):
    cache.delete("all_bookings")
