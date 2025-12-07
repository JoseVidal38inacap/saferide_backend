from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Extiende el manejador de DRF para agregar metadatos
    a los errores de la API SafeRide.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Nombre de la vista / endpoint donde falló
        view = context.get("view", None)
        view_name = view.__class__.__name__ if view else "UnknownView"

        response.data["service"] = "SafeRide API"
        response.data["view"] = view_name
        response.data["status_code"] = response.status_code

    return response
