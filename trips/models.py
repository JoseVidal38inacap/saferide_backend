from django.db import models

from common.models import TimeStampedModel
from accounts.models import Passenger, Driver
from vehicles.models import Vehicle


class Trip(TimeStampedModel):
    class TripStatus(models.TextChoices):
        CREATED = "CREATED", "Creado"
        ASSIGNED = "ASSIGNED", "Asignado"
        STARTED = "STARTED", "En curso"
        FINISHED = "FINISHED", "Finalizado"
        CANCELED = "CANCELED", "Cancelado"
        BILLED = "BILLED", "Facturado"

    passenger = models.ForeignKey(
        Passenger,
        on_delete=models.PROTECT,
        related_name="trips",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        related_name="trips",
        null=True,
        blank=True,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name="trips",
        null=True,
        blank=True,
    )

    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)

    requested_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    distance_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Distancia estimada o real en km",
    )
    estimated_duration_min = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duración estimada en minutos",
    )
    estimated_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    final_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=TripStatus.choices,
        default=TripStatus.CREATED,
        db_index=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["requested_at"]),
            models.Index(fields=["passenger", "status"]),
        ]
        ordering = ["-requested_at"]

    def __str__(self) -> str:
        return f"Trip #{self.id} - {self.origin} → {self.destination} ({self.status})"
