from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from common.views import HomeView
from accounts.views import PassengerViewSet, DriverViewSet
from vehicles.views import VehicleViewSet
from trips.views import TripViewSet
from payments.views import PaymentViewSet

router = DefaultRouter()
router.register(r"passengers", PassengerViewSet, basename="passenger")
router.register(r"drivers", DriverViewSet, basename="driver")
router.register(r"vehicles", VehicleViewSet, basename="vehicle")
router.register(r"trips", TripViewSet, basename="trip")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    # Landing mejorada (front-end)
    path("", HomeView.as_view(), name="home"),

    # Admin Django
    path("admin/", admin.site.urls),

    # Esquema OpenAPI y Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

    # API REST registrada con router
    path("api/", include(router.urls)),
]
