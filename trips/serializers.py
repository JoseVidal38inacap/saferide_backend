from rest_framework import serializers
from .models import Trip


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = [
            "id",
            "passenger",
            "driver",
            "vehicle",
            "origin",
            "destination",
            "requested_at",
            "started_at",
            "finished_at",
            "distance_km",
            "estimated_duration_min",
            "estimated_price",
            "final_price",
            "status",
            "created_at",
            "updated_at",
        ]
