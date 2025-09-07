from rest_framework import serializers
from .models import Property, User, Booking


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["id", "title", "description", "price", "location", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "joined_at"]


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    property = PropertySerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='user', queryset=User.objects.all())
    property_id = serializers.PrimaryKeyRelatedField(write_only=True, source='property', queryset=Property.objects.all())

    class Meta:
        model = Booking
        fields = ["id", "user", "property", "user_id", "property_id", "start_date", "end_date", "booked_at"]
