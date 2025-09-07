from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import property_list, cache_metrics, user_list, booking_list
from .api import PropertyViewSet, UserViewSet, BookingViewSet

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'users', UserViewSet, basename='user')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', property_list, name='property_list'),
    path('metrics/', cache_metrics, name='cache_metrics'),
    path('users/', user_list, name='user_list'),
    path('bookings/', booking_list, name='booking_list'),
    path('api/', include(router.urls)),
]
