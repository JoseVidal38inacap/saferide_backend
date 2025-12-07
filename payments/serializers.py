from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "trip",
            "amount",
            "status",
            "method",
            "transaction_id",
            "processed_at",
            "created_at",
            "updated_at",
        ]
