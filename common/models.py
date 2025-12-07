from django.db import models


class TimeStampedModel(models.Model):
    """
    Modelo base con fechas de creación y actualización,
    y un flag de activo para soft-delete simple.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)
