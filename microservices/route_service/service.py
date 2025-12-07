import json
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from kafka import KafkaConsumer, errors as kafka_errors

# Configuración básica de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("route_service")

KAFKA_BOOTSTRAP_SERVERS = ["localhost:9092"]
KAFKA_TOPIC = "trip.created"


def simulate_route_and_price(trip: dict) -> None:
    """
    Simula el cálculo de ruta: duración estimada y precio estimado.
    En un sistema real, esto podría llamar a un API de mapas.
    """
    try:
        distance = float(trip.get("distance_km") or 5.0)
    except (TypeError, ValueError):
        distance = 5.0

    base_price = 1000
    price_per_km = 500
    estimated_price = base_price + distance * price_per_km
    estimated_duration = max(int(distance * 3), 5)

    logger.info(
        "RouteService: calculada ruta para trip %s | distancia=%.2f km, "
        "duración=%s min, precio estimado=%s",
        trip.get("id"),
        distance,
        estimated_duration,
        estimated_price,
    )

    # Aquí podríamos enviar un PATCH a la API de Django para actualizar
    # el viaje con estos datos. Para mantenerlo simple en la evaluación,
    # solo lo dejamos registrado en logs.


def consume_trip_created() -> None:
    """
    Hilo principal del consumidor Kafka para el RouteService.
    """
    try:
        consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            group_id="route-service",
            auto_offset_reset="earliest",
        )
        logger.info("RouteService conectado a Kafka. Escuchando topic %s", KAFKA_TOPIC)
    except kafka_errors.NoBrokersAvailable as exc:
        logger.error("RouteService: Kafka no disponible: %s", exc)
        # Si Kafka está caído, dejamos de consumir pero el /health seguirá activo.
        return

    for message in consumer:
        trip = message.value
        logger.info("RouteService: evento recibido: %s", trip)
        simulate_route_and_price(trip)


class HealthHandler(BaseHTTPRequestHandler):
    """
    Servidor HTTP mínimo para health-check.
    """

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                b'{"status": "ok", "service": "route-service"}'
            )
        else:
            self.send_response(404)
            self.end_headers()


def run_health_server(port: int = 8001) -> None:
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    logger.info("RouteService health-check escuchando en http://localhost:%s/health", port)
    server.serve_forever()


if __name__ == "__main__":
    # Hilo daemon para el consumidor Kafka
    consumer_thread = threading.Thread(target=consume_trip_created, daemon=True)
    consumer_thread.start()

    # En el hilo principal levantamos el health-check HTTP
    run_health_server()
