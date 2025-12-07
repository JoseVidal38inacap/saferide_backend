from django.contrib import admin
from .models import Passenger, Driver


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "phone_number",
        "emergency_contact",
        "created_at",
        "is_active",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username", "user__email", "phone_number")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "license_number",
        "phone_number",
        "rating",
        "created_at",
        "is_active",
    )
    list_filter = ("is_active", "rating")
    search_fields = ("user__username", "user__email", "license_number")
    readonly_fields = ("created_at", "updated_at")
