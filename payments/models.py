from django.db import models

from common.models import TimeStampedModel
from trips.models import Trip


class Payment(TimeStampedModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"
        FAILED = "FAILED", "Fallido"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Efectivo"
        CARD = "CARD", "Tarjeta"
        WALLET = "WALLET", "Billetera digital"

    trip = models.OneToOneField(
        Trip,
        on_delete=models.CASCADE,
        related_name="payment",
    )
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        db_index=True,
    )
    method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        help_text="ID de la transacción entregado por el proveedor de pago",
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Fecha en que se completó el pago",
    )

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["method"]),
        ]

    def __str__(self) -> str:
        return f"Payment for Trip #{self.trip_id} - {self.amount} ({self.status})"
