from rest_framework import serializers
from .models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "driver",
            "plate_number",
            "brand",
            "model",
            "year",
            "color",
            "is_active",
            "created_at",
            "updated_at",
        ]
