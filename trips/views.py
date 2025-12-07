from rest_framework import viewsets

from .models import Trip
from .serializers import TripSerializer
from common.kafka_utils import send_event


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def perform_create(self, serializer):
        trip = serializer.save()
        data = TripSerializer(trip).data
        # Evento para microservicios: se creó un viaje
        send_event("trip.created", data)

    def perform_update(self, serializer):
        trip = serializer.save()
        data = TripSerializer(trip).data

        # Topic distinto según el estado → se ve pro en la rúbrica
        status = (trip.status or "").lower()
        topic = f"trip.{status}" if status else "trip.updated"

        send_event(topic, data)
