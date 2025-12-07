from rest_framework import viewsets
from .models import Passenger, Driver
from .serializers import PassengerSerializer, DriverSerializer


class PassengerViewSet(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
