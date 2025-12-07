from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "plate_number",
        "brand",
        "model",
        "year",
        "color",
        "driver",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "brand", "year")
    search_fields = ("plate_number", "brand", "model", "driver__user__username")
    readonly_fields = ("created_at", "updated_at")
