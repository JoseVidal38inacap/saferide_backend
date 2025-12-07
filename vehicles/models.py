from django.db import models

from common.models import TimeStampedModel
from accounts.models import Driver


class Vehicle(TimeStampedModel):
    driver = models.OneToOneField(
        Driver,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehicle",
        help_text="Conductor asignado actualmente al vehículo",
    )
    plate_number = models.CharField("Patente", max_length=10, unique=True)
    brand = models.CharField("Marca", max_length=50)
    model = models.CharField("Modelo", max_length=50)
    year = models.PositiveIntegerField("Año")
    color = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        indexes = [
            models.Index(fields=["plate_number"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.plate_number} - {self.brand} {self.model}"
