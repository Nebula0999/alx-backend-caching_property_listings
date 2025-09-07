from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from .models import Property, User, Booking
from .serializers import PropertySerializer, UserSerializer, BookingSerializer
from .permissions import IsOwnerOrAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication


class PropertyViewSet(viewsets.ModelViewSet):
    """Public read; authenticated users may create/update if desired."""
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UserViewSet(viewsets.ModelViewSet):
    """User management restricted to admin users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class BookingViewSet(viewsets.ModelViewSet):
    """Bookings require authentication to create/list."""
    queryset = Booking.objects.select_related('user', 'property').all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrAdmin]
