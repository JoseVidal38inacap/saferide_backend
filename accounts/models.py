from django.conf import settings
from django.db import models

from common.models import TimeStampedModel


class Passenger(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passenger_profile",
    )
    phone_number = models.CharField(max_length=20)
    emergency_contact = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"Passenger {self.user.username}"


class Driver(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="driver_profile",
    )
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=5.00,
        help_text="Rating promedio del conductor (1.00 a 5.00)",
    )

    def __str__(self) -> str:
        return f"Driver {self.user.username} ({self.license_number})"
