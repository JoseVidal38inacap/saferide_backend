from rest_framework import serializers
from .models import Passenger, Driver


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = [
            "id",
            "user",
            "phone_number",
            "emergency_contact",
            "created_at",
            "updated_at",
            "is_active",
        ]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = [
            "id",
            "user",
            "license_number",
            "phone_number",
            "rating",
            "created_at",
            "updated_at",
            "is_active",
        ]
