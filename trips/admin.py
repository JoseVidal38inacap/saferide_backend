from django.contrib import admin
from .models import Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "passenger",
        "driver",
        "vehicle",
        "origin",
        "destination",
        "status",
        "estimated_price",
        "final_price",
        "requested_at",
    )
    list_filter = ("status", "requested_at")
    search_fields = (
        "origin",
        "destination",
        "passenger__user__username",
        "driver__user__username",
    )
    date_hierarchy = "requested_at"
    readonly_fields = ("created_at", "updated_at", "requested_at")
