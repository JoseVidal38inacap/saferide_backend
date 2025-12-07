from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "trip",
        "amount",
        "status",
        "method",
        "transaction_id",
        "processed_at",
        "created_at",
    )
    list_filter = ("status", "method")
    search_fields = ("trip__id", "transaction_id")
    readonly_fields = ("created_at", "updated_at")
